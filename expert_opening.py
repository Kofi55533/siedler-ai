# -*- coding: utf-8 -*-
"""Expert opening controller and optional behavior cloning pretraining.

This module is intentionally separate from the environment.  The environment
defines what is possible; this file defines one human opening line as a teacher.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import torch as th
from stable_baselines3.common.utils import obs_as_tensor

from environment import (
    MAIN_ACTIONS,
    POSITION_GROUP_SIZE,
    QUANTITY_VALUES,
    RESEARCH_BUILDINGS,
    TAX_LEVELS,
    ActionPhase,
    get_base_building_name,
)

FULL_SIM_FIRST_UNIVERSITY_START_TIME = 29


@dataclass
class ExpertPlan:
    action_name: str
    selections: Dict[ActionPhase, int]
    reason: str = ""


def _quantity_index(quantity: int) -> int:
    quantity = max(1, min(int(quantity), max(QUANTITY_VALUES)))
    if quantity in QUANTITY_VALUES:
        return int(QUANTITY_VALUES.index(quantity))
    return int(np.argmin([abs(v - quantity) for v in QUANTITY_VALUES]))


def _first_valid(mask: np.ndarray, fallback: int = 0) -> int:
    valid = np.flatnonzero(np.asarray(mask, dtype=bool).reshape(-1))
    return int(valid[0]) if valid.size else int(fallback)


def _normal_base(value: str) -> str:
    return str(value or "").lower().replace("_", "").replace(" ", "")


class ExpertOpeningController:
    """State-dependent expert for the known Wintersturm opening.

    The controller emits the same micro-actions the policy sees.  It does not
    expose absolute serf ids to the policy; it selects source categories/cohorts
    and quantities just like an RL action would.
    """

    def __init__(self) -> None:
        self.active_plan: Optional[ExpertPlan] = None
        self.completed_actions = 0
        self.fallback_actions = 0

    def reset(self) -> None:
        self.active_plan = None
        self.completed_actions = 0
        self.fallback_actions = 0

    def act(self, env) -> int:
        """Return the next expert action for the environment's current phase."""
        if env.current_phase == ActionPhase.MAIN:
            self.active_plan = self._make_next_plan(env)
            if self.active_plan is None:
                return self._masked_choice(env, self._main_action_index("wait"))
            return self._masked_choice(env, self._main_action_index(self.active_plan.action_name))

        plan = self.active_plan
        if plan is None or plan.action_name != getattr(env, "current_flow", None):
            self.fallback_actions += 1
            return _first_valid(env.action_masks())

        choice = int(plan.selections.get(env.current_phase, 0))
        return self._masked_choice(env, choice)

    def observe_step(self, info: dict) -> None:
        if not bool((info or {}).get("multi_step", False)):
            self.completed_actions += 1
            self.active_plan = None

    def is_done(self, env) -> bool:
        return (
            self._started_delta(env, "Lehmh") >= 3
            or self._expert_milestone(env) >= 17
        )

    def _masked_choice(self, env, choice: int) -> int:
        mask = np.asarray(env.action_masks(), dtype=bool).reshape(-1)
        if 0 <= int(choice) < mask.size and bool(mask[int(choice)]):
            return int(choice)
        self.fallback_actions += 1
        return _first_valid(mask)

    @staticmethod
    def _main_action_index(action_name: str) -> int:
        try:
            return int(MAIN_ACTIONS.index(action_name))
        except ValueError:
            return 0

    def _make_next_plan(self, env) -> Optional[ExpertPlan]:
        """Build one complete high-level action for the current state."""
        # 1) Start with exactly nine serfs if possible.
        if int(env.total_leibeigene) < 9:
            missing = 9 - int(env.total_leibeigene)
            if env._can_buy_serf_batch(max(1, min(20, missing))):
                return self._plan_buy_serfs(max(1, min(20, missing)), "opening: recruit 9 serfs")

        # 2) First mining economy + first university from the recruited cohort.
        first_sites = [
            ("Schwefelmine_1", "Schwefelmine", 2, 2),
            ("Eisenmine_1", "Eisenmine", 2, 2),
            ("Steinmine_1", "Steinmine", 1, 2),
            ("Lehmmine_1", "Lehmmine", 1, 2),
            ("Hochschule_1", "Hochschule", 3, 1),
        ]
        for building, base, qty, mode in first_sites:
            if base == "Hochschule" and self._should_delay_first_university(env):
                return None
            if self._started_delta(env, base) < 1 and self._can_build_with_source(env, building, qty):
                return self._plan_build(
                    env,
                    building=building,
                    quantity=qty,
                    position_mode=mode,
                    prefer_source_base="Rekrutiert",
                    reason=f"opening: start {base}",
                )

        # 3) Same university builders should start the second university.
        if (
            self._completed_delta(env, "Hochschule") >= 1
            and self._started_delta(env, "Hochschule") < 2
            and self._can_build_with_source(env, "Hochschule_1", 3, prefer_source_base="Hochschule")
        ):
            return self._plan_build(
                env,
                building="Hochschule_1",
                quantity=3,
                position_mode=1,
                prefer_source_base="Hochschule",
                reason="opening: second university with first university builders",
            )

        if (
            self._completed_delta(env, "Hochschule") >= 1
            and not self._tech_started_or_done(env, "Bildung")
            and env._can_research("Bildung")
        ):
            return self._plan_research(env, "Hochschule", "Bildung", "opening: research Bildung")

        # 4) Second iron and sulfur mines after the first ones are complete.
        for building, base in (("Eisenmine_1", "Eisenmine"), ("Schwefelmine_1", "Schwefelmine")):
            if (
                self._completed_delta(env, base) >= 1
                and self._started_delta(env, base) < 2
                and self._can_build_with_source(env, building, 2, prefer_source_base=base)
            ):
                return self._plan_build(
                    env,
                    building=building,
                    quantity=2,
                    position_mode=2,
                    prefer_source_base=base,
                    reason=f"opening: second {base}",
                )

        all_opening_mines_done = (
            self._completed_delta(env, "Eisenmine") >= 2
            and self._completed_delta(env, "Schwefelmine") >= 2
            and self._completed_delta(env, "Steinmine") >= 1
            and self._completed_delta(env, "Lehmmine") >= 1
        )

        # 5) Finished mine builders go to nearby wood when their mine chain is done.
        if all_opening_mines_done:
            plan = self._plan_idle_mine_cohort_to_wood(env)
            if plan is not None:
                return plan

        # 6) Highest taxes after Bildung.
        if "Bildung" in getattr(env, "researched_techs", set()):
            max_tax = max(TAX_LEVELS.keys())
            if int(getattr(env, "current_tax_level", 0)) < int(max_tax):
                return ExpertPlan(
                    "tax",
                    {ActionPhase.TAX_LEVEL: int(max_tax)},
                    "opening: set highest taxes after Bildung",
                )

        # 7) Buy toward the next worker breakpoints when money allows it.
        if all_opening_mines_done and int(env.total_leibeigene) < 16:
            missing = min(20, 16 - int(env.total_leibeigene))
            if env._can_buy_serf_batch(missing):
                return self._plan_buy_serfs(missing, "opening: recruit toward 16 serfs")

        if (
            all_opening_mines_done
            and int(env.total_leibeigene) >= 16
            and self._started_delta(env, "Kloster") < 1
            and self._can_build_with_source(env, "Kloster_1", 4)
        ):
            return self._plan_build(
                env,
                building="Kloster_1",
                quantity=4,
                position_mode=4,
                reason="opening: build monastery/cathedral expansion anchor",
            )

        if (
            self._completed_delta(env, "Kloster") >= 1
            and self._started_delta(env, "Dorfzentrum") < 1
            and self._can_build_with_source(env, "Dorfzentrum_1", 4, prefer_source_base="Kloster")
        ):
            return self._plan_build(
                env,
                building="Dorfzentrum_1",
                quantity=4,
                position_mode=4,
                prefer_source_base="Kloster",
                reason="opening: monastery builders continue to village center",
            )

        if self._completed_delta(env, "Dorfzentrum") >= 1:
            plan = self._plan_cohort_to_wood(env, preferred_bases=("Dorfzentrum", "Kloster"), reason="opening: DZ builders to wood")
            if plan is not None:
                return plan

        if (
            self._completed_delta(env, "Dorfzentrum") >= 1
            and not self._tech_started_or_done(env, "Konstruktion")
            and env._can_research("Konstruktion")
        ):
            return self._plan_research(env, "Hochschule", "Konstruktion", "opening: research Konstruktion")

        if self._tech_started_or_done(env, "Konstruktion") and int(env.total_leibeigene) < 25:
            missing = min(20, 25 - int(env.total_leibeigene))
            if env._can_buy_serf_batch(missing):
                return self._plan_buy_serfs(missing, "opening: recruit toward 25 serfs")

        if self._tech_started_or_done(env, "Konstruktion"):
            if self._started_delta(env, "Wohnhaus") < 1 and self._can_build_with_source(env, "Wohnhaus_1", 2):
                return self._plan_build(env, "Wohnhaus_1", 2, 3, reason="opening: build residence")
            if self._started_delta(env, "Bauernhof") < 1 and self._can_build_with_source(env, "Bauernhof_1", 2):
                return self._plan_build(env, "Bauernhof_1", 2, 3, reason="opening: build farm")

        if self._tech_started_or_done(env, "Konstruktion") and not self._tech_started_or_done(env, "Alchimie"):
            if env._can_research("Alchimie"):
                return self._plan_research(env, "Hochschule", "Alchimie", "opening: research Alchimie")

        clay_workshop = self._find_building(env, "Lehmh")
        if clay_workshop and self._tech_started_or_done(env, "Alchimie"):
            if self._started_delta(env, "Lehmh") < 3 and self._can_build_with_source(env, clay_workshop, 2):
                return self._plan_build(
                    env,
                    building=clay_workshop,
                    quantity=2,
                    position_mode=2,
                    reason="opening: build clay workshop",
                )

        return None

    def _plan_buy_serfs(self, quantity: int, reason: str) -> ExpertPlan:
        return ExpertPlan(
            "buy_serf",
            {ActionPhase.QUANTITY: _quantity_index(quantity)},
            reason,
        )

    def _plan_research(self, env, building_base: str, tech: str, reason: str) -> Optional[ExpertPlan]:
        if building_base not in RESEARCH_BUILDINGS:
            return None
        techs = env.tech_by_building.get(building_base, [])
        if tech not in techs:
            return None
        return ExpertPlan(
            "research",
            {
                ActionPhase.TECH_BUILDING: int(RESEARCH_BUILDINGS.index(building_base)),
                ActionPhase.TECH: int(techs.index(tech)),
            },
            reason,
        )

    def _plan_build(
        self,
        env,
        building: str,
        quantity: int,
        position_mode: int,
        reason: str,
        prefer_source_base: Optional[str] = None,
    ) -> Optional[ExpertPlan]:
        source = self._select_source(env, quantity, prefer_source_base=prefer_source_base)
        if source is None:
            return None
        category_idx = env._get_build_category_index(building)
        category_buildings = env._get_buildings_for_build_category(category_idx)
        if building not in category_buildings:
            return None
        selections = {
            ActionPhase.SOURCE_CATEGORY: int(source[0]),
            ActionPhase.SOURCE_SPECIFIC: int(source[1]),
            ActionPhase.QUANTITY: _quantity_index(quantity),
            ActionPhase.BUILD_CATEGORY: int(category_idx),
            ActionPhase.BUILDING: int(category_buildings.index(building)),
            ActionPhase.POSITION_MODE: int(position_mode),
        }
        pos_idx = self._select_position_index(env, "build", building, selections)
        selections[ActionPhase.POSITION_GROUP] = int(pos_idx // POSITION_GROUP_SIZE)
        selections[ActionPhase.POSITION_INDEX] = int(pos_idx % POSITION_GROUP_SIZE)
        return ExpertPlan("build", selections, reason)

    def _plan_idle_mine_cohort_to_wood(self, env) -> Optional[ExpertPlan]:
        return self._plan_cohort_to_wood(
            env,
            preferred_bases=("Lehmmine", "Schwefelmine", "Eisenmine", "Steinmine"),
            reason="opening: finished mine builders to nearby wood",
        )

    def _plan_cohort_to_wood(
        self,
        env,
        preferred_bases: Iterable[str],
        reason: str,
    ) -> Optional[ExpertPlan]:
        env._cleanup_free_serf_cohorts()
        for base in preferred_bases:
            idx = self._find_cohort_index(env, base, min_count=1)
            if idx is None:
                continue
            cohort = env.free_serf_cohorts[idx]
            quantity = min(int(cohort.get("count", 0) or 0), 3)
            if quantity <= 0:
                continue
            target_specific = self._select_wood_target_specific(
                env,
                quantity,
                preferred_zone=cohort.get("preferred_wood_zone"),
            )
            if target_specific is None:
                continue
            return ExpertPlan(
                "assign_serf",
                {
                    ActionPhase.SOURCE_CATEGORY: 7,
                    ActionPhase.SOURCE_SPECIFIC: int(idx),
                    ActionPhase.QUANTITY: _quantity_index(quantity),
                    ActionPhase.TARGET_CATEGORY: 1,
                    ActionPhase.TARGET_SPECIFIC: int(target_specific),
                },
                reason,
            )
        return None

    def _should_delay_first_university(self, env) -> bool:
        """Use the Full-Sim verified opening timing for the first university demo action."""
        if str(getattr(env, "sim_mode", "")) != "full_sim":
            return False
        if self._started_delta(env, "Hochschule") >= 1:
            return False
        return float(getattr(env, "current_time", 0.0)) < FULL_SIM_FIRST_UNIVERSITY_START_TIME

    def _select_position_index(self, env, flow_name: str, building: str, selections: Dict[ActionPhase, int]) -> int:
        previous_flow = env.current_flow
        previous_phase = env.current_phase
        previous_selections = dict(env.pending_selections)
        try:
            env.current_flow = flow_name
            env.current_phase = ActionPhase.POSITION_GROUP
            env.pending_selections = dict(selections)
            candidates = env._get_build_position_candidates_for_selections(building, selections)
            if not candidates:
                return 0
            if hasattr(env, "_get_build_position_valid_mask_for_selections"):
                valid_mask = env._get_build_position_valid_mask_for_selections(building, selections)
                valid = np.flatnonzero(valid_mask)
                if valid.size:
                    return int(valid[0])
            return 0
        finally:
            env.current_flow = previous_flow
            env.current_phase = previous_phase
            env.pending_selections = previous_selections

    def _select_source(
        self,
        env,
        quantity: int,
        prefer_source_base: Optional[str] = None,
    ) -> Optional[Tuple[int, int]]:
        env._cleanup_free_serf_cohorts()
        if prefer_source_base:
            idx = self._find_cohort_index(env, prefer_source_base, quantity)
            if idx is not None:
                return 7, idx
        idx = self._find_cohort_index(env, "Rekrutiert", quantity)
        if idx is not None:
            return 7, idx
        for idx, cohort in enumerate(getattr(env, "free_serf_cohorts", [])):
            if int(cohort.get("count", 0) or 0) >= int(quantity):
                return 7, idx
        if int(env.free_leibeigene) >= int(quantity):
            return 0, 0
        return None

    def _find_cohort_index(self, env, base_token: str, min_count: int) -> Optional[int]:
        token = _normal_base(base_token)
        for idx, cohort in enumerate(getattr(env, "free_serf_cohorts", [])):
            base = _normal_base(cohort.get("base", ""))
            label = _normal_base(cohort.get("label", ""))
            if int(cohort.get("count", 0) or 0) < int(min_count):
                continue
            if token in base or token in label:
                return int(idx)
        return None

    def _select_wood_target_specific(
        self,
        env,
        quantity: int,
        preferred_zone: Optional[str] = None,
    ) -> Optional[int]:
        available_free = max(int(env.free_leibeigene), int(quantity))
        if preferred_zone:
            preferred_norm = _normal_base(preferred_zone)
            candidates = []
            for tree_idx, tree in enumerate(getattr(env, "tree_list_internal", [])):
                zone_name = tree.get("zone")
                if preferred_norm and preferred_norm not in _normal_base(zone_name):
                    continue
                if env._can_assign_wood_tree_batch(
                    tree_idx,
                    quantity,
                    available_free_override=available_free,
                ):
                    candidates.append((float(tree.get("dist", 0.0)), int(tree_idx)))
            candidates.sort(key=lambda item: (item[0], item[1]))
            if candidates:
                return candidates[0][1]

        for specific in range(min(env._wood_specific_encoded_limit(), env.target_specific_size)):
            tree_idx = env._get_wood_zone_rank_tree_index(
                specific,
                quantity,
                mode="assign",
                available_free_override=available_free,
            )
            if tree_idx is not None:
                return int(specific)
        return None

    def _can_build_with_source(
        self,
        env,
        building: str,
        quantity: int,
        prefer_source_base: Optional[str] = None,
    ) -> bool:
        if not building or not env._can_build(building):
            return False
        source = self._select_source(env, quantity, prefer_source_base=prefer_source_base)
        if source is None:
            return False
        return bool(env._can_use_source_batch(source[0], source[1], quantity))

    def _started_delta(self, env, base_name: str) -> int:
        if hasattr(env, "_get_started_base_delta"):
            return int(env._get_started_base_delta(base_name))
        return 0

    def _completed_delta(self, env, base_name: str) -> int:
        if hasattr(env, "_get_completed_base_delta"):
            return int(env._get_completed_base_delta(base_name))
        return 0

    def _expert_milestone(self, env) -> int:
        if hasattr(env, "_get_expert_opening_milestone_level"):
            return int(env._get_expert_opening_milestone_level())
        return 0

    @staticmethod
    def _tech_started_or_done(env, tech_name: str) -> bool:
        return tech_name in getattr(env, "researched_techs", set()) or any(
            tech == tech_name for tech, _remaining in getattr(env, "current_researches", [])
        )

    @staticmethod
    def _find_building(env, token: str) -> Optional[str]:
        token_norm = _normal_base(token)
        for building in getattr(env, "buildable_buildings", []):
            base = _normal_base(get_base_building_name(building))
            name = _normal_base(building)
            if token_norm in base or token_norm in name:
                return building
        return None


def _copy_obs(obs):
    if isinstance(obs, dict):
        return {key: np.array(value, copy=True) for key, value in obs.items()}
    return np.array(obs, copy=True)


def _stack_obs(obs_items: List):
    if not obs_items:
        raise ValueError("No observations to stack")
    first = obs_items[0]
    if isinstance(first, dict):
        return {key: np.stack([obs[key] for obs in obs_items], axis=0) for key in first.keys()}
    return np.stack(obs_items, axis=0)


def _slice_obs(stacked_obs, indices: np.ndarray):
    if isinstance(stacked_obs, dict):
        return {key: value[indices] for key, value in stacked_obs.items()}
    return stacked_obs[indices]


def collect_expert_opening_demonstrations(
    env,
    episodes: int = 2,
    max_micro_steps: int = 12000,
    max_completed_actions: int = 1200,
    wait_sample_stride: int = 10,
    max_wait_samples: int = 400,
    seed: int = 123,
) -> Dict[str, object]:
    """Collect phase-level demonstrations from the expert controller."""
    controller = ExpertOpeningController()
    observations: List = []
    actions: List[int] = []
    masks: List[np.ndarray] = []
    episode_completed: List[int] = []
    fallback_actions = 0
    executed_wait_actions = 0
    recorded_wait_samples = 0
    recorded_non_wait_samples = 0

    for ep in range(max(1, int(episodes))):
        obs, _info = env.reset(seed=int(seed) + ep)
        controller.reset()
        completed = 0
        consecutive_wait_choices = 0
        for _step in range(max(1, int(max_micro_steps))):
            mask = np.asarray(env.action_masks(), dtype=bool).reshape(-1)
            action = int(controller.act(env))
            if not (0 <= action < mask.size and mask[action]):
                action = _first_valid(mask)
                fallback_actions += 1

            is_wait_choice = (
                env.current_phase == ActionPhase.MAIN
                and 0 <= action < len(MAIN_ACTIONS)
                and MAIN_ACTIONS[action] == "wait"
            )
            if is_wait_choice:
                consecutive_wait_choices += 1
                executed_wait_actions += 1
                should_record = (
                    recorded_wait_samples < int(max_wait_samples)
                    and (
                        consecutive_wait_choices == 1
                        or max(1, int(wait_sample_stride)) <= 1
                        or consecutive_wait_choices % max(1, int(wait_sample_stride)) == 0
                    )
                )
            else:
                consecutive_wait_choices = 0
                should_record = True

            if should_record:
                observations.append(_copy_obs(obs))
                actions.append(action)
                masks.append(mask.copy())
                if is_wait_choice:
                    recorded_wait_samples += 1
                else:
                    recorded_non_wait_samples += 1

            obs, _reward, terminated, truncated, info = env.step(action)
            controller.observe_step(info)
            if not bool((info or {}).get("multi_step", False)):
                completed += 1
            if terminated or truncated:
                break
            if completed >= int(max_completed_actions):
                break
            if controller.is_done(env) and env.current_phase == ActionPhase.MAIN:
                break
        episode_completed.append(completed)
        fallback_actions += controller.fallback_actions

    if not observations:
        raise RuntimeError("Expert controller did not produce any demonstration transitions")

    return {
        "observations": _stack_obs(observations),
        "actions": np.asarray(actions, dtype=np.int64),
        "masks": np.asarray(masks, dtype=bool),
        "episode_completed_actions": episode_completed,
        "fallback_actions": int(fallback_actions),
        "executed_wait_actions": int(executed_wait_actions),
        "recorded_wait_samples": int(recorded_wait_samples),
        "recorded_non_wait_samples": int(recorded_non_wait_samples),
    }


def behavior_cloning_pretrain(
    model,
    env,
    episodes: int = 2,
    max_micro_steps: int = 12000,
    max_completed_actions: int = 1200,
    wait_sample_stride: int = 10,
    max_wait_samples: int = 400,
    epochs: int = 3,
    batch_size: int = 512,
    learning_rate: float = 1e-4,
    seed: int = 123,
) -> Dict[str, float]:
    """Supervised pretraining on expert phase choices before PPO."""
    demos = collect_expert_opening_demonstrations(
        env,
        episodes=episodes,
        max_micro_steps=max_micro_steps,
        max_completed_actions=max_completed_actions,
        wait_sample_stride=wait_sample_stride,
        max_wait_samples=max_wait_samples,
        seed=seed,
    )
    observations = demos["observations"]
    actions = np.asarray(demos["actions"], dtype=np.int64)
    masks = np.asarray(demos["masks"], dtype=bool)
    n = int(actions.shape[0])
    if n <= 0:
        raise RuntimeError("No behavior cloning samples collected")

    optimizer = th.optim.Adam(model.policy.parameters(), lr=float(learning_rate))
    model.policy.set_training_mode(True)
    rng = np.random.default_rng(int(seed))
    losses: List[float] = []

    for _epoch in range(max(1, int(epochs))):
        order = rng.permutation(n)
        for start in range(0, n, max(1, int(batch_size))):
            batch_idx = order[start : start + max(1, int(batch_size))]
            obs_batch = _slice_obs(observations, batch_idx)
            obs_tensor = obs_as_tensor(obs_batch, model.device)
            action_tensor = th.as_tensor(actions[batch_idx], device=model.device).long()
            action_masks = masks[batch_idx]

            _values, log_prob, _entropy = model.policy.evaluate_actions(
                obs_tensor,
                action_tensor,
                action_masks=action_masks,
            )
            loss = -log_prob.mean()
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            th.nn.utils.clip_grad_norm_(model.policy.parameters(), max_norm=0.5)
            optimizer.step()
            losses.append(float(loss.detach().cpu().item()))

    return {
        "samples": float(n),
        "episodes": float(max(1, int(episodes))),
        "epochs": float(max(1, int(epochs))),
        "loss_start": float(losses[0]) if losses else 0.0,
        "loss_end": float(losses[-1]) if losses else 0.0,
        "fallback_actions": float(demos["fallback_actions"]),
        "avg_completed_actions": float(np.mean(demos["episode_completed_actions"])),
        "executed_wait_actions": float(demos["executed_wait_actions"]),
        "recorded_wait_samples": float(demos["recorded_wait_samples"]),
        "recorded_non_wait_samples": float(demos["recorded_non_wait_samples"]),
    }
