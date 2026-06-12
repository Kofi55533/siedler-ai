from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
EXPERIMENT_ROOT = SCRIPT_DIR.parent
RUNS_DIR = EXPERIMENT_ROOT / "runs"
RESEARCH_DIR = EXPERIMENT_ROOT / "research"


def _load_run_summaries() -> list[dict]:
    rows: list[dict] = []
    for summary_path in sorted(RUNS_DIR.glob("*/summary.json")):
        try:
            data = json.loads(summary_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not isinstance(data, list):
            continue
        run_name = summary_path.parent.name
        for row in data:
            if not isinstance(row, dict):
                continue
            row = dict(row)
            row["run_name"] = run_name
            rows.append(row)
    return rows


def _aggregate(rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("candidate"))].append(row)

    out: list[dict] = []
    for candidate, items in grouped.items():
        out.append(
            {
                "candidate": candidate,
                "families": sorted({str(item.get("family")) for item in items}),
                "runs": len(items),
                "avg_terminal_potential": float(
                    np.mean([float(item.get("mean_terminal_potential_metric", 0.0)) for item in items])
                ),
                "avg_path_ready": float(
                    np.mean([float(item.get("mean_terminal_path_ready", 0.0)) for item in items])
                ),
                "avg_dependency_progress": float(
                    np.mean([float(item.get("mean_scharf_dependency_progress", 0.0)) for item in items])
                ),
                "avg_research_progress": float(
                    np.mean([float(item.get("mean_scharf_research_progress", 0.0)) for item in items])
                ),
                "avg_construction_progress": float(
                    np.mean([float(item.get("mean_scharf_construction_progress", 0.0)) for item in items])
                ),
                "avg_unlock_progress": float(
                    np.mean([float(item.get("mean_step_unlock_progress_metric", 0.0)) for item in items])
                ),
                "avg_required_buildings_completed": float(
                    np.mean([float(item.get("mean_step_required_buildings_completed", 0.0)) for item in items])
                ),
                "avg_required_techs_completed": float(
                    np.mean([float(item.get("mean_step_required_techs_completed", 0.0)) for item in items])
                ),
                "avg_taler_income_per_cycle": float(
                    np.mean([float(item.get("mean_step_taler_income_per_cycle", 0.0)) for item in items])
                ),
                "avg_scharfschuetzen": float(
                    np.mean([float(item.get("mean_scharfschuetzen", 0.0)) for item in items])
                ),
                "avg_train_seconds": float(
                    np.mean([float(item.get("mean_train_seconds", 0.0)) for item in items])
                ),
                "source_runs": sorted({str(item.get("run_name")) for item in items}),
            }
        )

    out.sort(
        key=lambda row: (
            float(row["avg_terminal_potential"]),
            float(row["avg_path_ready"]),
            float(row["avg_dependency_progress"]),
            float(row["avg_research_progress"]),
            float(row["avg_construction_progress"]),
            float(row["avg_unlock_progress"]),
            float(row["avg_required_buildings_completed"]),
            float(row["avg_required_techs_completed"]),
        ),
        reverse=True,
    )
    return out


def _render_markdown(rows: list[dict]) -> str:
    lines = [
        "# Latest Experiment Summary",
        "",
        f"Runs scanned: {len(list(RUNS_DIR.glob('*/summary.json')))}",
        "",
        "## Ranking",
        "",
        "| Rank | Candidate | Family | Potential | Path Ready | Dependency | Research | Construction | Unlock | Req Buildings | Req Techs | Taler/Cycle | Scharfschuetzen | Avg Train Seconds |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for idx, row in enumerate(rows[:20], start=1):
        lines.append(
            "| "
            f"{idx} | {row['candidate']} | {', '.join(row['families'])} | "
            f"{float(row['avg_terminal_potential']):.3f} | "
            f"{float(row['avg_path_ready']):.2f} | "
            f"{float(row['avg_dependency_progress']):.3f} | "
            f"{float(row['avg_research_progress']):.3f} | "
            f"{float(row['avg_construction_progress']):.3f} | "
            f"{float(row['avg_unlock_progress']):.3f} | "
            f"{float(row['avg_required_buildings_completed']):.2f} | "
            f"{float(row['avg_required_techs_completed']):.2f} | "
            f"{float(row['avg_taler_income_per_cycle']):.2f} | "
            f"{float(row['avg_scharfschuetzen']):.3f} | "
            f"{float(row['avg_train_seconds']):.1f} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    rows = _load_run_summaries()
    aggregated = _aggregate(rows)
    (RESEARCH_DIR / "latest_summary.json").write_text(json.dumps(aggregated, indent=2), encoding="utf-8")
    (RESEARCH_DIR / "latest_summary.md").write_text(_render_markdown(aggregated), encoding="utf-8")
    print(f"Wrote {RESEARCH_DIR / 'latest_summary.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
