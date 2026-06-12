from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from benchmark_learning_hypotheses import (
    RESULT_DIR,
    _aggregate_results,
    _candidate_from_dict,
    _save_csv,
    _save_json,
    _snapshot_run_context,
    build_baseline_candidates,
    train_and_measure,
)
from summarize_runs import main as summarize_main

SCRIPT_DIR = Path(__file__).resolve().parent
EXPERIMENT_ROOT = SCRIPT_DIR.parent
PROJECT_ROOT = EXPERIMENT_ROOT.parent
SESSION_ROOT = EXPERIMENT_ROOT / "research" / "adaptive_sessions"


def seed_specs() -> list[dict]:
    base_cfg = {
        "learning_rate": 0.00025,
        "n_steps": 64,
        "batch_size": 32,
        "n_epochs": 2,
        "gamma": 0.999,
        "ent_coef": 0.01,
    }
    return [
        {
            "name": "custom_unlock_balanced",
            "profile_name": "goal_v1",
            "family": "adaptive_reward",
            "reward_overrides": {
                "terminal_dependency_bonus": 2.0,
                "terminal_recruitable_bonus": 4.0,
                "step_delta_progress_bonus": 0.8,
                "step_delta_dependency_bonus": 0.4,
                "step_delta_research_bonus": 0.4,
                "step_delta_construction_bonus": 0.4,
                "step_unlock_recruitable_bonus": 8.0,
                "step_worker_growth_bonus": 0.05,
                "action_buy_serf_growth_bonus": 0.05,
                "action_assign_spawned_serf_bonus": 0.02,
                "step_time_penalty": 0.001,
            },
            "config_overrides": dict(base_cfg),
        },
        {
            "name": "custom_path_ready_bounty",
            "profile_name": "goal_v1",
            "family": "adaptive_reward",
            "reward_overrides": {
                "terminal_dependency_bonus": 2.0,
                "terminal_path_ready_bonus": 12.0,
                "terminal_recruitable_bonus": 2.0,
                "step_delta_progress_bonus": 0.5,
                "step_unlock_milestone_bonus": 3.0,
                "step_unlock_milestone_count": 6.0,
                "step_path_ready_bonus": 24.0,
                "step_required_building_complete_bonus": 8.0,
                "step_required_tech_complete_bonus": 10.0,
                "step_delta_research_bonus": 0.6,
                "step_delta_construction_bonus": 0.6,
                "step_time_penalty": 0.001,
            },
            "config_overrides": dict(base_cfg),
        },
        {
            "name": "custom_requirement_milestones",
            "profile_name": "goal_v1",
            "family": "adaptive_reward",
            "reward_overrides": {
                "terminal_dependency_bonus": 3.0,
                "terminal_path_ready_bonus": 8.0,
                "step_progress_mix_dependency": 1.0,
                "step_progress_mix_research": 2.0,
                "step_progress_mix_construction": 2.0,
                "step_delta_progress_bonus": 0.6,
                "step_unlock_milestone_bonus": 4.0,
                "step_unlock_milestone_count": 8.0,
                "step_required_building_complete_bonus": 7.0,
                "step_required_tech_complete_bonus": 9.0,
                "step_delta_research_bonus": 0.8,
                "step_delta_construction_bonus": 0.8,
                "step_time_penalty": 0.0015,
            },
            "config_overrides": dict(base_cfg),
        },
        {
            "name": "custom_income_bridge",
            "profile_name": "goal_v1",
            "family": "adaptive_reward",
            "reward_overrides": {
                "terminal_dependency_bonus": 1.5,
                "terminal_path_ready_bonus": 6.0,
                "terminal_potential_bonus_per_unit": 4.0,
                "step_delta_progress_bonus": 0.3,
                "step_required_building_complete_bonus": 3.0,
                "step_required_tech_complete_bonus": 4.0,
                "step_worker_growth_bonus": 0.12,
                "step_delta_taler_income_bonus": 0.04,
                "action_buy_serf_growth_bonus": 0.18,
                "action_assign_spawned_serf_bonus": 0.08,
                "step_path_ready_bonus": 10.0,
                "step_time_penalty": 0.0,
            },
            "config_overrides": {**base_cfg, "learning_rate": 0.0003, "ent_coef": 0.015},
        },
        {
            "name": "custom_short_unlock_curriculum",
            "profile_name": "curriculum_unlock",
            "family": "adaptive_reward",
            "reward_overrides": {
                "terminal_dependency_bonus": 3.0,
                "terminal_path_ready_bonus": 12.0,
                "step_delta_progress_bonus": 0.8,
                "step_unlock_milestone_bonus": 4.0,
                "step_unlock_milestone_count": 5.0,
                "step_required_building_complete_bonus": 10.0,
                "step_required_tech_complete_bonus": 12.0,
                "step_path_ready_bonus": 28.0,
                "step_delta_research_bonus": 1.0,
                "step_delta_construction_bonus": 1.0,
                "step_time_penalty": 0.001,
            },
            "config_overrides": {**base_cfg, "learning_rate": 0.0003, "ent_coef": 0.02},
            "runtime_overrides": {"max_time_override": 450, "count_completed_actions_only": True},
        },
        {
            "name": "custom_short_requirement_sprint",
            "profile_name": "curriculum_unlock",
            "family": "adaptive_reward",
            "reward_overrides": {
                "terminal_dependency_bonus": 2.0,
                "terminal_path_ready_bonus": 8.0,
                "step_delta_progress_bonus": 0.5,
                "step_unlock_milestone_bonus": 5.0,
                "step_unlock_milestone_count": 4.0,
                "step_required_building_complete_bonus": 12.0,
                "step_required_tech_complete_bonus": 12.0,
                "step_path_ready_bonus": 18.0,
                "step_time_penalty": 0.0,
            },
            "config_overrides": {**base_cfg, "learning_rate": 0.0003, "ent_coef": 0.02, "n_steps": 32},
            "runtime_overrides": {"max_time_override": 300, "count_completed_actions_only": True},
        },
        {
            "name": "custom_dual_phase_stock_after_path",
            "profile_name": "goal_v1",
            "family": "adaptive_reward",
            "reward_overrides": {
                "terminal_dependency_bonus": 1.5,
                "terminal_path_ready_bonus": 10.0,
                "terminal_potential_bonus_per_unit": 10.0,
                "step_delta_potential_bonus": 0.6,
                "step_new_resource_potential_unit_bonus": 1.0,
                "step_delta_progress_bonus": 0.3,
                "step_unlock_milestone_bonus": 2.5,
                "step_required_building_complete_bonus": 4.0,
                "step_required_tech_complete_bonus": 5.0,
                "step_path_ready_bonus": 20.0,
                "step_time_penalty": 0.001,
            },
            "config_overrides": {**base_cfg, "learning_rate": 0.0002},
        },
        {
            "name": "custom_unlock_research",
            "profile_name": "goal_v1",
            "family": "adaptive_reward",
            "reward_overrides": {
                "terminal_dependency_bonus": 2.5,
                "terminal_recruitable_bonus": 5.0,
                "step_progress_mix_dependency": 0.5,
                "step_progress_mix_research": 3.0,
                "step_progress_mix_construction": 1.0,
                "step_delta_progress_bonus": 0.9,
                "step_delta_research_bonus": 1.5,
                "step_delta_construction_bonus": 0.3,
                "step_delta_dependency_bonus": 0.3,
                "step_unlock_recruitable_bonus": 10.0,
                "step_time_penalty": 0.001,
            },
            "config_overrides": dict(base_cfg),
        },
        {
            "name": "custom_unlock_construction",
            "profile_name": "goal_v1",
            "family": "adaptive_reward",
            "reward_overrides": {
                "terminal_dependency_bonus": 2.5,
                "terminal_recruitable_bonus": 5.0,
                "step_progress_mix_dependency": 0.5,
                "step_progress_mix_research": 1.0,
                "step_progress_mix_construction": 3.0,
                "step_delta_progress_bonus": 0.9,
                "step_delta_research_bonus": 0.3,
                "step_delta_construction_bonus": 1.5,
                "step_delta_dependency_bonus": 0.3,
                "step_unlock_recruitable_bonus": 10.0,
                "step_time_penalty": 0.001,
            },
            "config_overrides": dict(base_cfg),
        },
        {
            "name": "custom_dependency_heavy",
            "profile_name": "goal_v1",
            "family": "adaptive_reward",
            "reward_overrides": {
                "terminal_dependency_bonus": 3.0,
                "terminal_recruitable_bonus": 6.0,
                "step_progress_mix_dependency": 3.0,
                "step_progress_mix_research": 1.0,
                "step_progress_mix_construction": 1.0,
                "step_delta_progress_bonus": 1.0,
                "step_delta_dependency_bonus": 1.8,
                "step_delta_research_bonus": 0.2,
                "step_delta_construction_bonus": 0.2,
                "step_unlock_recruitable_bonus": 12.0,
                "step_time_penalty": 0.001,
            },
            "config_overrides": dict(base_cfg),
        },
        {
            "name": "custom_economy_bootstrap",
            "profile_name": "goal_v1",
            "family": "adaptive_reward",
            "reward_overrides": {
                "terminal_dependency_bonus": 1.5,
                "terminal_recruitable_bonus": 3.0,
                "step_delta_progress_bonus": 0.4,
                "step_delta_dependency_bonus": 0.2,
                "step_delta_research_bonus": 0.2,
                "step_delta_construction_bonus": 0.2,
                "step_worker_growth_bonus": 0.12,
                "action_buy_serf_growth_bonus": 0.15,
                "action_assign_spawned_serf_bonus": 0.08,
                "step_unlock_recruitable_bonus": 6.0,
                "step_time_penalty": 0.0,
            },
            "config_overrides": {**base_cfg, "learning_rate": 0.0003, "ent_coef": 0.015},
        },
        {
            "name": "custom_hybrid_current",
            "profile_name": "goal_v1",
            "family": "adaptive_reward",
            "reward_overrides": {
                "terminal_dependency_bonus": 1.5,
                "terminal_recruitable_bonus": 4.0,
                "terminal_potential_bonus_per_unit": 8.0,
                "terminal_potential_use_cumulative_earnings": 0.0,
                "step_delta_potential_bonus": 0.8,
                "step_new_resource_potential_unit_bonus": 1.2,
                "step_potential_use_cumulative_earnings": 0.0,
                "step_delta_progress_bonus": 0.3,
                "step_delta_dependency_bonus": 0.2,
                "step_delta_research_bonus": 0.2,
                "step_delta_construction_bonus": 0.2,
                "step_unlock_recruitable_bonus": 4.0,
                "step_time_penalty": 0.001,
            },
            "config_overrides": {**base_cfg, "learning_rate": 0.0002},
        },
        {
            "name": "custom_hybrid_cumulative",
            "profile_name": "goal_v1",
            "family": "adaptive_reward",
            "reward_overrides": {
                "terminal_dependency_bonus": 1.5,
                "terminal_recruitable_bonus": 4.0,
                "terminal_potential_bonus_per_unit": 8.0,
                "terminal_potential_use_cumulative_earnings": 1.0,
                "step_delta_potential_bonus": 0.8,
                "step_new_resource_potential_unit_bonus": 1.2,
                "step_potential_use_cumulative_earnings": 1.0,
                "step_delta_progress_bonus": 0.3,
                "step_delta_dependency_bonus": 0.2,
                "step_delta_research_bonus": 0.2,
                "step_delta_construction_bonus": 0.2,
                "step_unlock_recruitable_bonus": 4.0,
                "step_time_penalty": 0.001,
            },
            "config_overrides": {**base_cfg, "learning_rate": 0.0002},
        },
        {
            "name": "custom_force_progress",
            "profile_name": "goal_v1",
            "family": "adaptive_reward",
            "reward_overrides": {
                "terminal_dependency_bonus": 2.0,
                "terminal_recruitable_bonus": 4.0,
                "step_delta_progress_bonus": 1.2,
                "step_delta_dependency_bonus": 0.7,
                "step_delta_research_bonus": 0.7,
                "step_delta_construction_bonus": 0.7,
                "step_unlock_recruitable_bonus": 12.0,
                "step_time_penalty": 0.003,
            },
            "config_overrides": {**base_cfg, "ent_coef": 0.015},
        },
    ]


def score(row: dict) -> float:
    return (
        1000.0 * float(row.get("mean_terminal_potential_metric", 0.0))
        + 200.0 * float(row.get("mean_terminal_path_ready", 0.0))
        + 100.0 * float(row.get("mean_scharfschuetzen", 0.0))
        + 30.0 * float(row.get("mean_scharf_dependency_progress", 0.0))
        + 20.0 * float(row.get("mean_scharf_research_progress", 0.0))
        + 20.0 * float(row.get("mean_scharf_construction_progress", 0.0))
        + 30.0 * float(row.get("mean_step_unlock_progress_metric", 0.0))
        + 15.0 * float(row.get("mean_step_required_buildings_completed", 0.0))
        + 20.0 * float(row.get("mean_step_required_techs_completed", 0.0))
        + 0.2 * float(row.get("mean_step_taler_income_per_cycle", 0.0))
        - 0.02 * float(row.get("mean_train_seconds", 0.0))
    )


def mutate(spec: dict) -> list[dict]:
    reward = dict(spec.get("reward_overrides", {}) or {})
    config = dict(spec.get("config_overrides", {}) or {})
    runtime = dict(spec.get("runtime_overrides", {}) or {})
    name = str(spec["name"])
    return [
        {
            "name": f"{name}_unlock_x2",
            "profile_name": spec.get("profile_name", "goal_v1"),
            "family": "adaptive_reward_round",
            "reward_overrides": {
                **reward,
                "terminal_dependency_bonus": max(4.0, float(reward.get("terminal_dependency_bonus", 1.0)) * 2.0),
                "step_delta_progress_bonus": max(1.5, float(reward.get("step_delta_progress_bonus", 0.5)) * 2.0),
                "step_delta_dependency_bonus": max(1.0, float(reward.get("step_delta_dependency_bonus", 0.3)) * 2.0),
                "step_unlock_recruitable_bonus": max(16.0, float(reward.get("step_unlock_recruitable_bonus", 6.0)) * 2.0),
            },
            "config_overrides": {**config, "learning_rate": 0.0003, "ent_coef": 0.02},
            "runtime_overrides": dict(runtime),
        },
        {
            "name": f"{name}_research_focus",
            "profile_name": spec.get("profile_name", "goal_v1"),
            "family": "adaptive_reward_round",
            "reward_overrides": {
                **reward,
                "step_progress_mix_dependency": 0.5,
                "step_progress_mix_research": 3.0,
                "step_progress_mix_construction": 1.0,
                "step_delta_research_bonus": max(0.8, float(reward.get("step_delta_research_bonus", 0.3)) * 2.0),
            },
            "config_overrides": dict(config),
            "runtime_overrides": dict(runtime),
        },
        {
            "name": f"{name}_construction_focus",
            "profile_name": spec.get("profile_name", "goal_v1"),
            "family": "adaptive_reward_round",
            "reward_overrides": {
                **reward,
                "step_progress_mix_dependency": 0.5,
                "step_progress_mix_research": 1.0,
                "step_progress_mix_construction": 3.0,
                "step_delta_construction_bonus": max(0.8, float(reward.get("step_delta_construction_bonus", 0.3)) * 2.0),
            },
            "config_overrides": dict(config),
            "runtime_overrides": dict(runtime),
        },
        {
            "name": f"{name}_stock_probe",
            "profile_name": spec.get("profile_name", "goal_v1"),
            "family": "adaptive_reward_round",
            "reward_overrides": {
                **reward,
                "terminal_potential_use_cumulative_earnings": 0.0,
                "step_potential_use_cumulative_earnings": 0.0,
                "terminal_potential_bonus_per_unit": max(6.0, float(reward.get("terminal_potential_bonus_per_unit", 2.0)) * 1.5),
                "step_delta_potential_bonus": max(0.5, float(reward.get("step_delta_potential_bonus", 0.2)) * 1.5),
                "step_new_resource_potential_unit_bonus": max(1.0, float(reward.get("step_new_resource_potential_unit_bonus", 0.5)) * 1.5),
            },
            "config_overrides": dict(config),
            "runtime_overrides": dict(runtime),
        },
        {
            "name": f"{name}_path_ready_focus",
            "profile_name": spec.get("profile_name", "goal_v1"),
            "family": "adaptive_reward_round",
            "reward_overrides": {
                **reward,
                "terminal_path_ready_bonus": max(10.0, float(reward.get("terminal_path_ready_bonus", 4.0)) * 1.75),
                "step_path_ready_bonus": max(20.0, float(reward.get("step_path_ready_bonus", 8.0)) * 1.75),
                "step_required_building_complete_bonus": max(6.0, float(reward.get("step_required_building_complete_bonus", 2.0)) * 1.5),
                "step_required_tech_complete_bonus": max(8.0, float(reward.get("step_required_tech_complete_bonus", 2.0)) * 1.5),
            },
            "config_overrides": {**config, "ent_coef": max(0.012, float(config.get("ent_coef", 0.01)))},
            "runtime_overrides": dict(runtime),
        },
        {
            "name": f"{name}_milestone_focus",
            "profile_name": spec.get("profile_name", "goal_v1"),
            "family": "adaptive_reward_round",
            "reward_overrides": {
                **reward,
                "step_unlock_milestone_bonus": max(4.0, float(reward.get("step_unlock_milestone_bonus", 1.5)) * 1.75),
                "step_unlock_milestone_count": 6.0,
                "step_delta_progress_bonus": max(0.8, float(reward.get("step_delta_progress_bonus", 0.3)) * 1.5),
            },
            "config_overrides": dict(config),
            "runtime_overrides": dict(runtime),
        },
        {
            "name": f"{name}_income_focus",
            "profile_name": spec.get("profile_name", "goal_v1"),
            "family": "adaptive_reward_round",
            "reward_overrides": {
                **reward,
                "step_worker_growth_bonus": max(0.12, float(reward.get("step_worker_growth_bonus", 0.05)) * 1.75),
                "step_delta_taler_income_bonus": max(0.04, float(reward.get("step_delta_taler_income_bonus", 0.02)) * 1.75),
                "action_buy_serf_growth_bonus": max(0.12, float(reward.get("action_buy_serf_growth_bonus", 0.05)) * 1.5),
                "action_assign_spawned_serf_bonus": max(0.06, float(reward.get("action_assign_spawned_serf_bonus", 0.02)) * 1.5),
            },
            "config_overrides": {**config, "learning_rate": max(0.00025, float(config.get("learning_rate", 0.0002)))},
            "runtime_overrides": dict(runtime),
        },
        {
            "name": f"{name}_short_horizon",
            "profile_name": spec.get("profile_name", "goal_v1"),
            "family": "adaptive_reward_round",
            "reward_overrides": {
                **reward,
                "terminal_path_ready_bonus": max(8.0, float(reward.get("terminal_path_ready_bonus", 4.0))),
                "step_path_ready_bonus": max(16.0, float(reward.get("step_path_ready_bonus", 6.0))),
                "step_unlock_milestone_bonus": max(3.0, float(reward.get("step_unlock_milestone_bonus", 1.0)) * 1.5),
            },
            "config_overrides": {**config, "learning_rate": 0.0003, "ent_coef": 0.02},
            "runtime_overrides": {**runtime, "max_time_override": min(600, int(runtime.get("max_time_override", 600) or 600)), "count_completed_actions_only": True},
        },
    ]


def hyper_variants(spec: dict) -> list[dict]:
    reward = dict(spec.get("reward_overrides", {}) or {})
    profile_name = str(spec.get("profile_name", "goal_v1"))
    return [
        {
            "name": "winner_default",
            "profile_name": profile_name,
            "family": "adaptive_hyper",
            "reward_overrides": dict(reward),
            "config_overrides": {"learning_rate": 0.0002, "n_steps": 64, "batch_size": 32, "n_epochs": 2, "gamma": 0.999, "ent_coef": 0.01},
        },
        {
            "name": "winner_explore",
            "profile_name": profile_name,
            "family": "adaptive_hyper",
            "reward_overrides": dict(reward),
            "config_overrides": {"learning_rate": 0.0003, "n_steps": 64, "batch_size": 32, "n_epochs": 2, "gamma": 0.999, "ent_coef": 0.02},
        },
        {
            "name": "winner_longrollout",
            "profile_name": profile_name,
            "family": "adaptive_hyper",
            "reward_overrides": dict(reward),
            "config_overrides": {"learning_rate": 0.0002, "n_steps": 128, "batch_size": 64, "n_epochs": 2, "gamma": 0.999, "ent_coef": 0.01},
        },
        {
            "name": "winner_completed_steps",
            "profile_name": profile_name,
            "family": "adaptive_runtime",
            "reward_overrides": dict(reward),
            "config_overrides": {"learning_rate": 0.0002, "n_steps": 64, "batch_size": 32, "n_epochs": 2, "gamma": 0.999, "ent_coef": 0.01},
            "runtime_overrides": {"count_completed_actions_only": True},
        },
        {
            "name": "winner_medium_net",
            "profile_name": profile_name,
            "family": "adaptive_runtime",
            "reward_overrides": dict(reward),
            "config_overrides": {"learning_rate": 0.0002, "n_steps": 64, "batch_size": 32, "n_epochs": 2, "gamma": 0.999, "ent_coef": 0.01},
            "runtime_overrides": {"net_arch": [128, 64]},
        },
        {
            "name": "winner_short_horizon",
            "profile_name": profile_name,
            "family": "adaptive_runtime",
            "reward_overrides": dict(reward),
            "config_overrides": {"learning_rate": 0.0003, "n_steps": 64, "batch_size": 32, "n_epochs": 2, "gamma": 0.999, "ent_coef": 0.02},
            "runtime_overrides": {"max_time_override": 600, "count_completed_actions_only": True},
        },
    ]


def run_spec_round(session_dir: Path, round_name: str, specs: list[dict], timesteps: int, eval_episodes: int, seeds: list[int], max_time_override: int = 0, stochastic_eval: bool = False) -> tuple[Path, list[dict]]:
    specs_dir = session_dir / "specs"
    logs_dir = session_dir / "logs"
    specs_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    spec_path = specs_dir / f"{round_name}.json"
    spec_path.write_text(json.dumps(specs, indent=2), encoding="utf-8")
    stamp = time.strftime("%Y%m%d_%H%M%S")
    run_dir = RESULT_DIR / f"{stamp}_{round_name}_spec"
    run_dir.mkdir(parents=True, exist_ok=True)
    candidates = [_candidate_from_dict(spec) for spec in specs]
    run_args = argparse.Namespace(
        group="spec",
        timesteps=int(timesteps),
        eval_episodes=int(eval_episodes),
        seeds=list(seeds),
        best_reward_profile="goal_v1",
        candidates=[candidate.name for candidate in candidates],
        candidate_spec=str(spec_path),
        max_time_override=int(max_time_override),
        stochastic_eval=bool(stochastic_eval),
        output_prefix=round_name,
    )
    _snapshot_run_context(run_dir, run_args, candidates, candidate_spec_path=spec_path)
    log_path = logs_dir / f"{round_name}.log"
    log_path.write_text("", encoding="utf-8")

    def append_log(line: str) -> None:
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(f"{line}\n")

    all_rows = []
    total_runs = len(candidates) * len(seeds)
    run_index = 0
    for candidate in candidates:
        for seed in seeds:
            run_index += 1
            candidate_max_time = candidate.runtime_overrides.get("max_time_override", max_time_override)
            append_log(
                f"[{run_index}/{total_runs}] candidate={candidate.name} family={candidate.family} seed={seed} timesteps={timesteps} max_time={candidate_max_time}"
            )
            row = train_and_measure(
                candidate,
                timesteps=int(timesteps),
                eval_episodes=int(eval_episodes),
                seed=int(seed),
                max_time_override=(int(max_time_override) if int(max_time_override) > 0 else None),
                deterministic_eval=not bool(stochastic_eval),
            )
            all_rows.append(row)
            append_log(
                "  result: "
                f"potential={float(row['mean_terminal_potential_metric']):.3f} "
                f"path_ready={float(row['mean_terminal_path_ready']):.2f} "
                f"dep={float(row['mean_scharf_dependency_progress']):.3f} "
                f"unlock={float(row.get('mean_step_unlock_progress_metric', 0.0)):.3f} "
                f"req_b={float(row.get('mean_step_required_buildings_completed', 0.0)):.2f} "
                f"req_t={float(row.get('mean_step_required_techs_completed', 0.0)):.2f} "
                f"taler={float(row.get('mean_step_taler_income_per_cycle', 0.0)):.2f} "
                f"train_s={float(row['train_seconds']):.1f}"
            )
            partial_summary = _aggregate_results(all_rows)
            _save_json(run_dir / "detail.json", all_rows)
            _save_csv(run_dir / "detail.csv", all_rows)
            _save_json(run_dir / "summary.json", partial_summary)
            _save_csv(run_dir / "summary.csv", partial_summary)
    summary = _aggregate_results(all_rows)
    _save_json(run_dir / "detail.json", all_rows)
    _save_csv(run_dir / "detail.csv", all_rows)
    _save_json(run_dir / "summary.json", summary)
    _save_csv(run_dir / "summary.csv", summary)
    append_log(f"completed round={round_name} candidates={len(candidates)} seeds={len(seeds)}")
    return run_dir, summary


def top_rows(summary: list[dict], k: int) -> list[dict]:
    rows = [dict(row, adaptive_score=score(row)) for row in summary]
    rows.sort(key=lambda row: float(row["adaptive_score"]), reverse=True)
    return rows[:k]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Adaptive reward search for Siedler AI.")
    parser.add_argument("--proxy-timesteps", type=int, default=4096)
    parser.add_argument("--full-timesteps", type=int, default=8192)
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    SESSION_ROOT.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    session_dir = SESSION_ROOT / f"adaptive_{stamp}"
    session_dir.mkdir(parents=True, exist_ok=True)
    (session_dir / "logs").mkdir(parents=True, exist_ok=True)
    (session_dir / "specs").mkdir(parents=True, exist_ok=True)

    journal = [f"# Adaptive Reward Search {stamp}", ""]
    seed_list = list(args.seeds)

    baseline_specs = [
        {
            "name": candidate.name,
            "profile_name": candidate.profile_name,
            "family": candidate.family,
            "reward_overrides": dict(candidate.reward_overrides),
            "config_overrides": dict(candidate.config_overrides),
            "runtime_overrides": dict(candidate.runtime_overrides),
        }
        for candidate in build_baseline_candidates()
    ]
    baseline_dir, _ = run_spec_round(
        session_dir,
        "adaptive_baseline",
        baseline_specs,
        1,
        4,
        seed_list,
        max_time_override=0,
        stochastic_eval=False,
    )
    journal += ["## Baseline", "", f"- Run: `{baseline_dir.name}`", ""]

    round1_specs = seed_specs()
    round1_dir, round1_summary = run_spec_round(
        session_dir, "round1_proxy", round1_specs, int(args.proxy_timesteps), 4, seed_list, max_time_override=600, stochastic_eval=True
    )
    round1_top = top_rows(round1_summary, 3)
    journal += ["## Round 1", "", f"- Run: `{round1_dir.name}`"]
    journal += [
        f"- {row['candidate']}: score={float(row['adaptive_score']):.2f}, dep={float(row['mean_scharf_dependency_progress']):.3f}, "
        f"unlock={float(row.get('mean_step_unlock_progress_metric', 0.0)):.3f}, req_b={float(row.get('mean_step_required_buildings_completed', 0.0)):.2f}, "
        f"req_t={float(row.get('mean_step_required_techs_completed', 0.0)):.2f}, taler={float(row.get('mean_step_taler_income_per_cycle', 0.0)):.2f}"
        for row in round1_top
    ]
    journal.append("")

    lookup = {str(spec["name"]): spec for spec in round1_specs}
    round2_specs: list[dict] = []
    for row in round1_top[:2]:
        round2_specs.extend(mutate(lookup[str(row["candidate"])]))
    dedup = {str(spec["name"]): spec for spec in round2_specs}
    round2_specs = list(dedup.values())
    round2_dir, round2_summary = run_spec_round(
        session_dir, "round2_proxy", round2_specs, int(args.proxy_timesteps), 4, seed_list, max_time_override=600, stochastic_eval=True
    )
    round2_top = top_rows(round2_summary, 3)
    journal += ["## Round 2", "", f"- Run: `{round2_dir.name}`"]
    journal += [
        f"- {row['candidate']}: score={float(row['adaptive_score']):.2f}, dep={float(row['mean_scharf_dependency_progress']):.3f}, "
        f"unlock={float(row.get('mean_step_unlock_progress_metric', 0.0)):.3f}, req_b={float(row.get('mean_step_required_buildings_completed', 0.0)):.2f}, "
        f"req_t={float(row.get('mean_step_required_techs_completed', 0.0)):.2f}, taler={float(row.get('mean_step_taler_income_per_cycle', 0.0)):.2f}"
        for row in round2_top
    ]
    journal.append("")

    finalists = {str(spec["name"]): spec for spec in (round1_specs + round2_specs)}
    final_dir, final_summary = run_spec_round(
        session_dir, "final_full", list(finalists.values()), int(args.full_timesteps), 2, seed_list, max_time_override=0, stochastic_eval=False
    )
    final_top = top_rows(final_summary, 3)
    journal += ["## Final Full Horizon", "", f"- Run: `{final_dir.name}`"]
    journal += [
        f"- {row['candidate']}: score={float(row['adaptive_score']):.2f}, potential={float(row['mean_terminal_potential_metric']):.3f}, "
        f"path_ready={float(row['mean_terminal_path_ready']):.2f}, dep={float(row['mean_scharf_dependency_progress']):.3f}, "
        f"unlock={float(row.get('mean_step_unlock_progress_metric', 0.0)):.3f}"
        for row in final_top
    ]
    journal.append("")

    winner = finalists[str(final_top[0]["candidate"])] if final_top else round1_specs[0]
    hyper_dir, hyper_summary = run_spec_round(
        session_dir, "winner_hyper", hyper_variants(winner), int(args.full_timesteps), 2, seed_list, max_time_override=0, stochastic_eval=False
    )
    hyper_top = top_rows(hyper_summary, 3)
    journal += ["## Winner Hyper Runtime", "", f"- Run: `{hyper_dir.name}`"]
    journal += [
        f"- {row['candidate']}: score={float(row['adaptive_score']):.2f}, potential={float(row['mean_terminal_potential_metric']):.3f}, "
        f"path_ready={float(row['mean_terminal_path_ready']):.2f}, dep={float(row['mean_scharf_dependency_progress']):.3f}, "
        f"unlock={float(row.get('mean_step_unlock_progress_metric', 0.0)):.3f}"
        for row in hyper_top
    ]
    journal.append("")

    summarize_main()
    (session_dir / "journal.md").write_text("\n".join(journal), encoding="utf-8")
    (session_dir / "manifest.json").write_text(json.dumps({"started_at": stamp, "args": vars(args), "winner_candidate": winner["name"]}, indent=2), encoding="utf-8")
    print(f"Adaptive session finished: {session_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
