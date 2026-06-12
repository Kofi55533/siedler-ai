from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
EXPERIMENT_ROOT = SCRIPT_DIR.parent
BENCHMARK_SCRIPT = SCRIPT_DIR / "benchmark_learning_hypotheses.py"
ADAPTIVE_SCRIPT = SCRIPT_DIR / "adaptive_reward_search.py"
SUMMARY_SCRIPT = SCRIPT_DIR / "summarize_runs.py"
LOG_DIR = EXPERIMENT_ROOT / "logs"


def _suite_commands(mode: str) -> list[list[str]]:
    common = [sys.executable, "-u", str(BENCHMARK_SCRIPT)]
    if mode == "cpu_long":
        return [
            common
            + [
                "--group", "reward",
                "--timesteps", "8192",
                "--eval-episodes", "2",
                "--seeds", "0", "1",
                "--output-prefix", "long_reward_full",
            ],
            common
            + [
                "--group", "reward",
                "--timesteps", "4096",
                "--eval-episodes", "4",
                "--seeds", "0", "1", "2",
                "--max-time-override", "600",
                "--stochastic-eval",
                "--output-prefix", "long_reward_proxy600",
            ],
            common
            + [
                "--group", "hyper",
                "--best-reward-profile", "curriculum_unlock",
                "--timesteps", "8192",
                "--eval-episodes", "2",
                "--seeds", "0", "1",
                "--output-prefix", "long_hyper_unlock",
            ],
            common
            + [
                "--group", "reward",
                "--timesteps", "32768",
                "--eval-episodes", "2",
                "--seeds", "0", "1",
                "--candidates", "curriculum_unlock", "goal_v1",
                "--output-prefix", "long_headtohead",
            ],
        ]
    if mode == "cpu_48h_bootstrap":
        return [
            common
            + [
                "--group", "baseline",
                "--timesteps", "1",
                "--eval-episodes", "4",
                "--seeds", "0", "1", "2", "3",
                "--output-prefix", "baseline_full",
            ],
            common
            + [
                "--group", "reward",
                "--timesteps", "4096",
                "--eval-episodes", "4",
                "--seeds", "0", "1", "2", "3",
                "--max-time-override", "600",
                "--stochastic-eval",
                "--output-prefix", "reward_proxy600_a",
            ],
            common
            + [
                "--group", "reward",
                "--timesteps", "8192",
                "--eval-episodes", "2",
                "--seeds", "0", "1", "2", "3",
                "--output-prefix", "reward_full_a",
            ],
            common
            + [
                "--group", "runtime",
                "--best-reward-profile", "goal_v1",
                "--timesteps", "4096",
                "--eval-episodes", "4",
                "--seeds", "0", "1", "2", "3",
                "--max-time-override", "600",
                "--stochastic-eval",
                "--output-prefix", "runtime_goal_proxy600",
            ],
            common
            + [
                "--group", "runtime",
                "--best-reward-profile", "curriculum_unlock",
                "--timesteps", "4096",
                "--eval-episodes", "4",
                "--seeds", "0", "1", "2", "3",
                "--max-time-override", "600",
                "--stochastic-eval",
                "--output-prefix", "runtime_unlock_proxy600",
            ],
            common
            + [
                "--group", "hyper",
                "--best-reward-profile", "goal_v1",
                "--timesteps", "8192",
                "--eval-episodes", "2",
                "--seeds", "0", "1", "2", "3",
                "--output-prefix", "hyper_goal_full",
            ],
            common
            + [
                "--group", "hyper",
                "--best-reward-profile", "curriculum_unlock",
                "--timesteps", "8192",
                "--eval-episodes", "2",
                "--seeds", "0", "1", "2", "3",
                "--output-prefix", "hyper_unlock_full",
            ],
            common
            + [
                "--group", "reward",
                "--timesteps", "32768",
                "--eval-episodes", "2",
                "--seeds", "0", "1", "2", "3",
                "--candidates", "goal_v1", "curriculum_unlock", "unlock_extreme", "dense_v2",
                "--output-prefix", "headtohead_32k",
            ],
            common
            + [
                "--group", "reward",
                "--timesteps", "65536",
                "--eval-episodes", "2",
                "--seeds", "0", "1",
                "--candidates", "goal_v1", "curriculum_unlock", "unlock_extreme",
                "--output-prefix", "headtohead_65k",
            ],
            common
            + [
                "--group", "reward",
                "--timesteps", "4096",
                "--eval-episodes", "4",
                "--seeds", "4", "5", "6", "7",
                "--max-time-override", "600",
                "--stochastic-eval",
                "--output-prefix", "reward_proxy600_b",
            ],
            common
            + [
                "--group", "reward",
                "--timesteps", "8192",
                "--eval-episodes", "2",
                "--seeds", "4", "5", "6", "7",
                "--output-prefix", "reward_full_b",
            ],
        ]
    if mode == "cpu_48h_adaptive":
        return [
            [
                sys.executable,
                "-u",
                str(ADAPTIVE_SCRIPT),
                "--proxy-timesteps",
                "4096",
                "--full-timesteps",
                "8192",
                "--seeds",
                "0",
                "1",
                "2",
                "3",
            ],
            [
                sys.executable,
                "-u",
                str(ADAPTIVE_SCRIPT),
                "--proxy-timesteps",
                "4096",
                "--full-timesteps",
                "8192",
                "--seeds",
                "4",
                "5",
                "6",
                "7",
            ],
            [
                sys.executable,
                "-u",
                str(ADAPTIVE_SCRIPT),
                "--proxy-timesteps",
                "8192",
                "--full-timesteps",
                "16384",
                "--seeds",
                "0",
                "2",
                "4",
                "6",
            ],
            common
            + [
                "--group", "runtime",
                "--best-reward-profile", "goal_v1",
                "--timesteps", "4096",
                "--eval-episodes", "4",
                "--seeds", "0", "1", "2", "3",
                "--max-time-override", "600",
                "--stochastic-eval",
                "--output-prefix", "runtime_goal_proxy600",
            ],
            common
            + [
                "--group", "baseline",
                "--timesteps", "1",
                "--eval-episodes", "4",
                "--seeds", "4", "5", "6", "7",
                "--output-prefix", "baseline_repeat",
            ],
        ]
    raise ValueError(f"Unsupported mode: {mode}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run long experiment suites for Siedler AI.")
    parser.add_argument("--mode", default="cpu_48h_adaptive", choices=("cpu_long", "cpu_48h_bootstrap", "cpu_48h_adaptive"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    suite_dir = LOG_DIR / f"suite_{stamp}_{args.mode}"
    suite_dir.mkdir(parents=True, exist_ok=True)

    commands = _suite_commands(args.mode)
    manifest = {
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "mode": args.mode,
        "commands": commands,
    }
    (suite_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    for idx, command in enumerate(commands, start=1):
        log_path = suite_dir / f"{idx:02d}.log"
        print(f"[{idx}/{len(commands)}] {' '.join(command)}")
        with log_path.open("w", encoding="utf-8") as log_file:
            process = subprocess.run(
                command,
                cwd=str(EXPERIMENT_ROOT.parent),
                check=False,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                text=True,
            )
        if process.returncode != 0:
            print(f"FAILED step={idx} log={log_path}")
            return int(process.returncode)
        subprocess.run(
            [sys.executable, "-u", str(SUMMARY_SCRIPT)],
            cwd=str(EXPERIMENT_ROOT.parent),
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
        )

    print(f"Suite finished: {suite_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
