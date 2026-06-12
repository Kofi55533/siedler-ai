from __future__ import annotations

import argparse
import csv
import json
import random
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

import numpy as np
import torch as th

SCRIPT_DIR = Path(__file__).resolve().parent
EXPERIMENT_ROOT = SCRIPT_DIR.parent
PROJECT_ROOT = EXPERIMENT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from environment import SiedlerScharfschuetzenEnv
from macro_maskable_ppo import CompletedActionMaskablePPO
from multihead_policy import MultiHeadMaskablePolicy
from training_profiles import get_train_profile


RESULT_DIR = EXPERIMENT_ROOT / "runs"
SNAPSHOT_PATHS = [
    PROJECT_ROOT / "environment.py",
    PROJECT_ROOT / "training_profiles.py",
    PROJECT_ROOT / "colab_training.py",
    PROJECT_ROOT / "train_100k.py",
    PROJECT_ROOT / "train_quick_test.py",
    SCRIPT_DIR / "benchmark_learning_hypotheses.py",
]
MEASUREMENT_REWARD_PROFILE: Dict[str, float] = {
    "terminal_dependency_bonus": 0.0,
    "terminal_recruitable_bonus": 0.0,
    "terminal_potential_bonus_per_unit": 1.0,
    "terminal_potential_use_cumulative_earnings": 0.0,
    "terminal_potential_include_start_resources": 0.0,
    "terminal_potential_scharf_tier": 1.0,
    "terminal_potential_require_path_ready": 1.0,
    "step_delta_potential_bonus": 0.0,
    "step_new_resource_potential_unit_bonus": 0.0,
    "step_delta_progress_bonus": 0.0,
    "step_delta_dependency_bonus": 0.0,
    "step_delta_research_bonus": 0.0,
    "step_delta_construction_bonus": 0.0,
    "step_worker_growth_bonus": 0.0,
    "step_unlock_recruitable_bonus": 0.0,
    "step_time_penalty": 0.0,
    "action_buy_serf_growth_bonus": 0.0,
    "action_assign_spawned_serf_bonus": 0.0,
    "step_potential_use_cumulative_earnings": 0.0,
    "step_potential_include_start_resources": 0.0,
    "step_potential_scharf_tier": 1.0,
    "step_delta_positive_only": 1.0,
}

BASE_PPO_CONFIG: Dict[str, float | int] = {
    "learning_rate": 2e-4,
    "n_steps": 64,
    "batch_size": 32,
    "n_epochs": 1,
    "gamma": 0.999,
    "gae_lambda": 0.95,
    "clip_range": 0.2,
    "ent_coef": 0.01,
}
RUNTIME_DEFAULTS: Dict[str, object] = {
    "use_spatial_obs": False,
    "count_completed_actions_only": False,
    "net_arch": [64],
    "policy_mode": "ppo",
}
REWARD_SWEEP_CONFIG: Dict[str, float | int] = {
    "learning_rate": 2e-4,
    "n_steps": 64,
    "batch_size": 32,
    "n_epochs": 2,
    "gamma": 0.999,
    "ent_coef": 0.01,
}


@dataclass(frozen=True)
class Candidate:
    name: str
    profile_name: str
    reward_overrides: Dict[str, float]
    config_overrides: Dict[str, object]
    family: str
    runtime_overrides: Dict[str, object] = field(default_factory=dict)


def _seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    th.manual_seed(seed)


def _make_env(
    reward_profile: Dict[str, float],
    seed: int,
    max_time_override: int | None = None,
    use_spatial_obs: bool = False,
) -> SiedlerScharfschuetzenEnv:
    env = SiedlerScharfschuetzenEnv(
        use_spatial_obs=bool(use_spatial_obs),
        reward_profile=reward_profile,
    )
    env.reset(seed=seed)
    if max_time_override is not None:
        env.max_time = int(max_time_override)
    return env


def _build_policy_kwargs(env: SiedlerScharfschuetzenEnv, net_arch: Sequence[int] | None = None) -> Dict[str, object]:
    return {
        "net_arch": list(net_arch or [64]),
        "action_head_sizes": env.get_action_head_sizes(),
        "phase_dim": env.phase_dim,
    }


def _merge_reward_profile(profile_name: str, overrides: Dict[str, float]) -> Dict[str, float]:
    profile = get_train_profile(profile_name)
    reward_profile = dict(profile["reward_profile"])
    reward_profile.update(overrides)
    return reward_profile


def _merge_config(profile_name: str, overrides: Dict[str, float | int]) -> Dict[str, float | int]:
    profile = get_train_profile(profile_name)
    merged = dict(BASE_PPO_CONFIG)
    merged.update(profile["config_overrides"])
    merged.update(overrides)
    return merged


def _merge_runtime(overrides: Dict[str, object]) -> Dict[str, object]:
    merged = dict(RUNTIME_DEFAULTS)
    merged.update(overrides)
    return merged


def _candidate_from_dict(raw: Dict[str, object]) -> Candidate:
    return Candidate(
        name=str(raw.get("name")),
        profile_name=str(raw.get("profile_name", "goal_v1")),
        reward_overrides=dict(raw.get("reward_overrides", {}) or {}),
        config_overrides=dict(raw.get("config_overrides", {}) or {}),
        family=str(raw.get("family", "spec")),
        runtime_overrides=dict(raw.get("runtime_overrides", {}) or {}),
    )


def _load_candidates_from_spec(spec_path: Path) -> List[Candidate]:
    payload = json.loads(spec_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Candidate spec must be a JSON list")
    return [_candidate_from_dict(item) for item in payload if isinstance(item, dict)]


def build_reward_candidates() -> List[Candidate]:
    return [
        Candidate("goal_v1", "goal_v1", {}, dict(REWARD_SWEEP_CONFIG), "reward"),
        Candidate(
            "goal_v1_cumulative",
            "goal_v1",
            {
                "terminal_potential_use_cumulative_earnings": 1.0,
                "step_potential_use_cumulative_earnings": 1.0,
            },
            dict(REWARD_SWEEP_CONFIG),
            "reward",
        ),
        Candidate(
            "goal_v1_no_path_gate",
            "goal_v1",
            {
                "terminal_potential_require_path_ready": 0.0,
            },
            dict(REWARD_SWEEP_CONFIG),
            "reward",
        ),
        Candidate("dense_v2", "dense_v2", {}, dict(REWARD_SWEEP_CONFIG), "reward"),
        Candidate("balanced", "balanced", {}, dict(REWARD_SWEEP_CONFIG), "reward"),
        Candidate("sparse", "sparse", {}, dict(REWARD_SWEEP_CONFIG), "reward"),
        Candidate("curriculum_unlock", "curriculum_unlock", {}, dict(REWARD_SWEEP_CONFIG), "reward"),
        Candidate("curriculum_stockpile", "curriculum_stockpile", {}, dict(REWARD_SWEEP_CONFIG), "reward"),
        Candidate(
            "unlock_extreme",
            "curriculum_unlock",
            {
                "terminal_dependency_bonus": 5.0,
                "terminal_recruitable_bonus": 10.0,
                "terminal_potential_bonus_per_unit": 2.0,
                "step_delta_progress_bonus": 2.0,
                "step_delta_dependency_bonus": 1.0,
                "step_delta_research_bonus": 1.0,
                "step_delta_construction_bonus": 1.0,
                "step_worker_growth_bonus": 0.1,
                "step_unlock_recruitable_bonus": 20.0,
                "action_buy_serf_growth_bonus": 0.1,
                "action_assign_spawned_serf_bonus": 0.05,
                "step_time_penalty": 0.0,
            },
            {
                **dict(REWARD_SWEEP_CONFIG),
                "learning_rate": 3e-4,
                "ent_coef": 0.02,
            },
            "reward",
        ),
    ]


def build_hyper_candidates(best_reward_profile: str = "goal_v1") -> List[Candidate]:
    return [
        Candidate(
            "hyper_goal_default",
            best_reward_profile,
            {},
            {
                "learning_rate": 2e-4,
                "n_steps": 64,
                "batch_size": 32,
                "gamma": 0.999,
                "ent_coef": 0.01,
            },
            "hyper",
        ),
        Candidate(
            "hyper_goal_explore",
            best_reward_profile,
            {},
            {
                "learning_rate": 3e-4,
                "n_steps": 64,
                "batch_size": 32,
                "gamma": 0.999,
                "ent_coef": 0.02,
            },
            "hyper",
        ),
        Candidate(
            "hyper_goal_short_horizon",
            best_reward_profile,
            {},
            {
                "learning_rate": 2.5e-4,
                "n_steps": 64,
                "batch_size": 32,
                "gamma": 0.995,
                "ent_coef": 0.015,
            },
            "hyper",
        ),
        Candidate(
            "hyper_goal_conservative",
            best_reward_profile,
            {},
            {
                "learning_rate": 1e-4,
                "n_steps": 64,
                "batch_size": 32,
                "gamma": 0.999,
                "ent_coef": 0.005,
            },
            "hyper",
        ),
        Candidate(
            "hyper_goal_longrollout",
            best_reward_profile,
            {},
            {
                "learning_rate": 2e-4,
                "n_steps": 128,
                "batch_size": 64,
                "gamma": 0.999,
                "ent_coef": 0.01,
            },
            "hyper",
        ),
        Candidate(
            "hyper_goal_fastupdates",
            best_reward_profile,
            {},
            {
                "learning_rate": 2.5e-4,
                "n_steps": 32,
                "batch_size": 32,
                "gamma": 0.999,
                "ent_coef": 0.015,
            },
            "hyper",
        ),
    ]


def build_runtime_candidates(best_reward_profile: str = "goal_v1") -> List[Candidate]:
    return [
        Candidate(
            "runtime_default",
            best_reward_profile,
            {},
            {
                "learning_rate": 2e-4,
                "n_steps": 64,
                "batch_size": 32,
                "n_epochs": 2,
                "gamma": 0.999,
                "ent_coef": 0.01,
            },
            "runtime",
            runtime_overrides={"count_completed_actions_only": False, "net_arch": [64]},
        ),
        Candidate(
            "runtime_completed_steps",
            best_reward_profile,
            {},
            {
                "learning_rate": 2e-4,
                "n_steps": 64,
                "batch_size": 32,
                "n_epochs": 2,
                "gamma": 0.999,
                "ent_coef": 0.01,
            },
            "runtime",
            runtime_overrides={"count_completed_actions_only": True, "net_arch": [64]},
        ),
        Candidate(
            "runtime_medium_net",
            best_reward_profile,
            {},
            {
                "learning_rate": 2e-4,
                "n_steps": 64,
                "batch_size": 32,
                "n_epochs": 2,
                "gamma": 0.999,
                "ent_coef": 0.01,
            },
            "runtime",
            runtime_overrides={"count_completed_actions_only": False, "net_arch": [128, 64]},
        ),
        Candidate(
            "runtime_completed_medium_net",
            best_reward_profile,
            {},
            {
                "learning_rate": 2e-4,
                "n_steps": 64,
                "batch_size": 32,
                "n_epochs": 2,
                "gamma": 0.999,
                "ent_coef": 0.01,
            },
            "runtime",
            runtime_overrides={"count_completed_actions_only": True, "net_arch": [128, 64]},
        ),
    ]


def build_baseline_candidates() -> List[Candidate]:
    return [
        Candidate(
            "baseline_wait",
            "goal_v1",
            {},
            {},
            "baseline",
            runtime_overrides={"policy_mode": "wait"},
        ),
        Candidate(
            "baseline_random",
            "goal_v1",
            {},
            {},
            "baseline",
            runtime_overrides={"policy_mode": "random"},
        ),
    ]


def evaluate_model(
    model: CompletedActionMaskablePPO | None,
    eval_episodes: int,
    seed_base: int,
    max_time_override: int | None = None,
    deterministic: bool = True,
    runtime: Dict[str, object] | None = None,
) -> Dict[str, float]:
    runtime = runtime or {}
    policy_mode = str(runtime.get("policy_mode", "ppo"))
    use_spatial_obs = bool(runtime.get("use_spatial_obs", False))
    metrics = {
        "terminal_potential_metric": [],
        "terminal_path_ready": [],
        "scharf_dependency_progress": [],
        "scharf_research_progress": [],
        "scharf_construction_progress": [],
        "step_unlock_progress_metric": [],
        "step_required_buildings_completed": [],
        "step_required_techs_completed": [],
        "step_taler_income_per_cycle": [],
        "scharfschuetzen": [],
        "episode_length": [],
    }

    for ep in range(eval_episodes):
        env = _make_env(
            MEASUREMENT_REWARD_PROFILE,
            seed=seed_base + ep,
            max_time_override=max_time_override,
            use_spatial_obs=use_spatial_obs,
        )
        obs, _ = env.reset(seed=seed_base + ep)
        if max_time_override is not None:
            env.max_time = int(max_time_override)
        done = False
        final_info: Dict[str, float] = {}
        steps = 0
        while not done:
            action_mask = env.get_action_mask()
            if policy_mode == "wait":
                action = 0
            elif policy_mode == "random":
                valid = [i for i, flag in enumerate(action_mask.tolist()) if flag]
                action = int(random.choice(valid))
            else:
                assert model is not None
                action, _ = model.predict(obs, deterministic=deterministic, action_masks=action_mask)
            obs, _, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            final_info = info
            steps += 1

        metrics["terminal_potential_metric"].append(float(final_info.get("terminal_potential_metric", 0.0)))
        metrics["terminal_path_ready"].append(1.0 if final_info.get("terminal_path_ready", False) else 0.0)
        metrics["scharf_dependency_progress"].append(float(final_info.get("scharf_dependency_progress", 0.0)))
        metrics["scharf_research_progress"].append(float(final_info.get("scharf_research_progress", 0.0)))
        metrics["scharf_construction_progress"].append(float(final_info.get("scharf_construction_progress", 0.0)))
        metrics["step_unlock_progress_metric"].append(float(final_info.get("step_unlock_progress_metric", 0.0)))
        metrics["step_required_buildings_completed"].append(float(final_info.get("step_required_buildings_completed", 0.0)))
        metrics["step_required_techs_completed"].append(float(final_info.get("step_required_techs_completed", 0.0)))
        metrics["step_taler_income_per_cycle"].append(float(final_info.get("step_taler_income_per_cycle", 0.0)))
        metrics["scharfschuetzen"].append(float(env.scharfschuetzen))
        metrics["episode_length"].append(float(steps))
        env.close()

    return {f"mean_{key}": float(np.mean(values)) for key, values in metrics.items()}


def train_and_measure(
    candidate: Candidate,
    timesteps: int,
    eval_episodes: int,
    seed: int,
    max_time_override: int | None = None,
    deterministic_eval: bool = True,
) -> Dict[str, object]:
    _seed_everything(seed)
    reward_profile = _merge_reward_profile(candidate.profile_name, candidate.reward_overrides)
    config = _merge_config(candidate.profile_name, candidate.config_overrides)
    runtime = _merge_runtime(candidate.runtime_overrides)
    use_spatial_obs = bool(runtime.get("use_spatial_obs", False))
    policy_mode = str(runtime.get("policy_mode", "ppo"))
    net_arch = runtime.get("net_arch", [64])
    count_completed_actions_only = bool(runtime.get("count_completed_actions_only", False))
    runtime_max_time = runtime.get("max_time_override", max_time_override)
    effective_max_time_override = None
    if runtime_max_time is not None:
        try:
            runtime_max_time_int = int(runtime_max_time)
        except (TypeError, ValueError):
            runtime_max_time_int = 0
        if runtime_max_time_int > 0:
            effective_max_time_override = runtime_max_time_int

    started = time.time()
    model: CompletedActionMaskablePPO | None = None
    if policy_mode == "ppo":
        env = _make_env(
            reward_profile,
            seed=seed,
            max_time_override=effective_max_time_override,
            use_spatial_obs=use_spatial_obs,
        )
        policy_kwargs = _build_policy_kwargs(env, net_arch=net_arch if isinstance(net_arch, Sequence) else [64])
        model = CompletedActionMaskablePPO(
            MultiHeadMaskablePolicy,
            env,
            learning_rate=float(config["learning_rate"]),
            n_steps=int(config["n_steps"]),
            batch_size=int(config["batch_size"]),
            n_epochs=int(config["n_epochs"]),
            gamma=float(config["gamma"]),
            gae_lambda=float(config["gae_lambda"]),
            clip_range=float(config["clip_range"]),
            ent_coef=float(config["ent_coef"]),
            policy_kwargs=policy_kwargs,
            device="cpu",
            verbose=0,
            seed=seed,
            count_completed_actions_only=count_completed_actions_only,
        )
        model.learn(total_timesteps=timesteps, progress_bar=False)
        env.close()
    train_seconds = float(time.time() - started)
    metrics = evaluate_model(
        model,
        eval_episodes=eval_episodes,
        seed_base=10_000 + seed * 100,
        max_time_override=effective_max_time_override,
        deterministic=deterministic_eval,
        runtime=runtime,
    )

    return {
        "candidate": candidate.name,
        "family": candidate.family,
        "profile_name": candidate.profile_name,
        "seed": int(seed),
        "timesteps": int(timesteps),
        "train_seconds": train_seconds,
        "reward_overrides": dict(candidate.reward_overrides),
        "config_overrides": dict(candidate.config_overrides),
        "runtime_overrides": dict(candidate.runtime_overrides),
        "effective_config": config,
        "effective_runtime": runtime,
        **metrics,
    }


def _aggregate_results(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    grouped: Dict[str, List[Dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["candidate"]), []).append(row)

    summary_rows: List[Dict[str, object]] = []
    for candidate_name, items in grouped.items():
        summary = {
            "candidate": candidate_name,
            "family": items[0]["family"],
            "profile_name": items[0]["profile_name"],
            "runs": len(items),
            "mean_terminal_potential_metric": float(
                np.mean([float(item["mean_terminal_potential_metric"]) for item in items])
            ),
            "mean_terminal_path_ready": float(
                np.mean([float(item["mean_terminal_path_ready"]) for item in items])
            ),
            "mean_scharf_dependency_progress": float(
                np.mean([float(item["mean_scharf_dependency_progress"]) for item in items])
            ),
            "mean_scharf_research_progress": float(
                np.mean([float(item["mean_scharf_research_progress"]) for item in items])
            ),
            "mean_scharf_construction_progress": float(
                np.mean([float(item["mean_scharf_construction_progress"]) for item in items])
            ),
            "mean_step_unlock_progress_metric": float(
                np.mean([float(item["mean_step_unlock_progress_metric"]) for item in items])
            ),
            "mean_step_required_buildings_completed": float(
                np.mean([float(item["mean_step_required_buildings_completed"]) for item in items])
            ),
            "mean_step_required_techs_completed": float(
                np.mean([float(item["mean_step_required_techs_completed"]) for item in items])
            ),
            "mean_step_taler_income_per_cycle": float(
                np.mean([float(item["mean_step_taler_income_per_cycle"]) for item in items])
            ),
            "mean_scharfschuetzen": float(
                np.mean([float(item["mean_scharfschuetzen"]) for item in items])
            ),
            "mean_train_seconds": float(np.mean([float(item["train_seconds"]) for item in items])),
        }
        summary_rows.append(summary)

    summary_rows.sort(
        key=lambda row: (
            float(row["mean_terminal_potential_metric"]),
            float(row["mean_terminal_path_ready"]),
            float(row["mean_scharf_dependency_progress"]),
            float(row["mean_step_unlock_progress_metric"]),
            float(row["mean_step_required_buildings_completed"]),
            float(row["mean_step_required_techs_completed"]),
        ),
        reverse=True,
    )
    return summary_rows


def _save_json(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    path.write_text(json.dumps(list(rows), indent=2), encoding="utf-8")


def _save_csv(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _run_text(*args: str) -> str:
    try:
        completed = subprocess.run(
            args,
            cwd=str(PROJECT_ROOT),
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return f"FAILED TO RUN {' '.join(args)}: {exc}\n"
    output = completed.stdout or ""
    error = completed.stderr or ""
    if error:
        output = f"{output}\n[stderr]\n{error}"
    return output


def _snapshot_run_context(
    run_dir: Path,
    args: argparse.Namespace,
    candidates: Sequence[Candidate],
    candidate_spec_path: Path | None = None,
) -> None:
    snapshot_dir = run_dir / "snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "project_root": str(PROJECT_ROOT),
        "experiment_root": str(EXPERIMENT_ROOT),
        "args": vars(args),
        "candidates": [candidate.name for candidate in candidates],
    }
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (run_dir / "git_status.txt").write_text(_run_text("git", "status", "--short"), encoding="utf-8")
    (run_dir / "git_diff.txt").write_text(_run_text("git", "diff", "--"), encoding="utf-8")

    for path in SNAPSHOT_PATHS:
        if not path.exists():
            continue
        target = snapshot_dir / path.name
        shutil.copy2(path, target)
    if candidate_spec_path is not None and candidate_spec_path.exists():
        shutil.copy2(candidate_spec_path, snapshot_dir / candidate_spec_path.name)


def _print_summary(rows: Sequence[Dict[str, object]]) -> None:
    print("\n=== Ranking ===")
    for idx, row in enumerate(rows, start=1):
        print(
            f"{idx:02d}. {row['candidate']:<24} "
            f"potential={float(row['mean_terminal_potential_metric']):6.3f} "
            f"path_ready={float(row['mean_terminal_path_ready']):5.2f} "
            f"dep={float(row['mean_scharf_dependency_progress']):5.3f} "
            f"unlock={float(row.get('mean_step_unlock_progress_metric', 0.0)):5.3f} "
            f"req_b={float(row.get('mean_step_required_buildings_completed', 0.0)):4.1f} "
            f"req_t={float(row.get('mean_step_required_techs_completed', 0.0)):4.1f} "
            f"train_s={float(row['mean_train_seconds']):6.1f}"
        )


def _iter_candidates(group: str, best_reward_profile: str) -> Iterable[Candidate]:
    if group == "spec":
        return
    if group == "baseline":
        yield from build_baseline_candidates()
        return
    if group == "reward":
        yield from build_reward_candidates()
        return
    if group == "hyper":
        yield from build_hyper_candidates(best_reward_profile=best_reward_profile)
        return
    if group == "runtime":
        yield from build_runtime_candidates(best_reward_profile=best_reward_profile)
        return
    if group == "all":
        yield from build_baseline_candidates()
        yield from build_reward_candidates()
        yield from build_hyper_candidates(best_reward_profile=best_reward_profile)
        yield from build_runtime_candidates(best_reward_profile=best_reward_profile)
        return
    raise ValueError(f"Unsupported group: {group}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark reward and PPO hypotheses for Siedler AI.")
    parser.add_argument("--group", choices=("spec", "baseline", "reward", "hyper", "runtime", "all"), default="reward")
    parser.add_argument("--timesteps", type=int, default=2048)
    parser.add_argument("--eval-episodes", type=int, default=2)
    parser.add_argument("--seeds", type=int, nargs="+", default=[0])
    parser.add_argument("--best-reward-profile", type=str, default="goal_v1")
    parser.add_argument("--candidates", type=str, nargs="*", default=[])
    parser.add_argument("--candidate-spec", type=str, default="")
    parser.add_argument("--max-time-override", type=int, default=0)
    parser.add_argument("--stochastic-eval", action="store_true")
    parser.add_argument("--output-prefix", type=str, default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    prefix = f"{args.output_prefix}_" if args.output_prefix else ""

    max_time_override = int(args.max_time_override) if int(args.max_time_override) > 0 else None
    all_rows: List[Dict[str, object]] = []
    candidate_spec_path: Path | None = None
    if str(args.candidate_spec).strip():
        spec_path = Path(args.candidate_spec).expanduser()
        if not spec_path.is_absolute():
            spec_path = (PROJECT_ROOT / spec_path).resolve()
        candidate_spec_path = spec_path
        candidates = _load_candidates_from_spec(spec_path)
    else:
        candidates = list(_iter_candidates(args.group, args.best_reward_profile))
    if args.candidates:
        allowed = set(args.candidates)
        candidates = [candidate for candidate in candidates if candidate.name in allowed]
        if not candidates:
            raise SystemExit("No candidates matched --candidates")

    run_dir = RESULT_DIR / f"{stamp}_{prefix}{args.group}"
    run_dir.mkdir(parents=True, exist_ok=True)
    _snapshot_run_context(run_dir, args, candidates, candidate_spec_path=candidate_spec_path)

    total_runs = len(candidates) * len(args.seeds)
    run_index = 0

    for candidate in candidates:
        for seed in args.seeds:
            run_index += 1
            print(
                f"[{run_index}/{total_runs}] candidate={candidate.name} "
                f"group={candidate.family} seed={seed} timesteps={args.timesteps}"
            )
            row = train_and_measure(
                candidate,
                timesteps=args.timesteps,
                eval_episodes=args.eval_episodes,
                seed=seed,
                max_time_override=max_time_override,
                deterministic_eval=not args.stochastic_eval,
            )
            all_rows.append(row)
            print(
                "  result: "
                f"potential={float(row['mean_terminal_potential_metric']):.3f} "
                f"path_ready={float(row['mean_terminal_path_ready']):.2f} "
                f"dep={float(row['mean_scharf_dependency_progress']):.3f} "
                f"unlock={float(row.get('mean_step_unlock_progress_metric', 0.0)):.3f} "
                f"req_b={float(row.get('mean_step_required_buildings_completed', 0.0)):.2f} "
                f"req_t={float(row.get('mean_step_required_techs_completed', 0.0)):.2f} "
                f"train_s={float(row['train_seconds']):.1f}"
            )

    summary_rows = _aggregate_results(all_rows)
    _print_summary(summary_rows)

    detail_json = run_dir / "detail.json"
    detail_csv = run_dir / "detail.csv"
    summary_json = run_dir / "summary.json"
    summary_csv = run_dir / "summary.csv"

    _save_json(detail_json, all_rows)
    _save_csv(detail_csv, all_rows)
    _save_json(summary_json, summary_rows)
    _save_csv(summary_csv, summary_rows)

    print(f"\nSaved run dir: {run_dir}")
    print(f"Saved detail: {detail_json}")
    print(f"Saved summary: {summary_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
