# -*- coding: utf-8 -*-
"""
Parse runtime pathing logs exported by lua_exports/export_runtime_pathing.lua.
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any


PAT_CMD = re.compile(
    r"RPATH\|CMD\|(\d+)\|([^|]+)\|(-?\d+)\|(-?\d+)\|(-?\d+)\|(-?\d+)\|([^|\r\n]+)"
)
PAT_POS = re.compile(
    r"RPATH\|POS\|(\d+)\|([^|]+)\|([0-9.]+)\|(-?\d+)\|(-?\d+)\|([0-9.]+)"
)
PAT_DONE = re.compile(r"RPATH\|DONE\|(\d+)\|([^|]+)\|([0-9.]+)\|([0-9.]+)")
PAT_FAIL = re.compile(
    r"RPATH\|FAIL\|(\d+)\|([^|]+)\|([^|]+)\|([0-9.]+)\|([0-9.]+)"
)
PAT_START = re.compile(r"RPATH\|START\|serf=(\d+)\|x=(-?\d+)\|y=(-?\d+)\|targets=(\d+)")
PAT_END = re.compile(r"RPATH\|END\|all_targets_done")


def parse_log(path: Path) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "start": None,
        "targets": {},
        "completed": False,
    }

    def get_target(idx: int, name: str) -> Dict[str, Any]:
        key = str(idx)
        if key not in data["targets"]:
            data["targets"][key] = {
                "idx": idx,
                "name": name,
                "cmd": None,
                "samples": [],
                "result": None,
            }
        return data["targets"][key]

    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = PAT_START.search(line)
            if m:
                data["start"] = {
                    "serf_id": int(m.group(1)),
                    "x": int(m.group(2)),
                    "y": int(m.group(3)),
                    "targets": int(m.group(4)),
                }
                continue

            if PAT_END.search(line):
                data["completed"] = True
                continue

            m = PAT_CMD.search(line)
            if m:
                idx = int(m.group(1))
                name = m.group(2)
                t = get_target(idx, name)
                t["cmd"] = {
                    "start_x": int(m.group(3)),
                    "start_y": int(m.group(4)),
                    "target_x": int(m.group(5)),
                    "target_y": int(m.group(6)),
                    "command_result": m.group(7).strip(),
                }
                continue

            m = PAT_POS.search(line)
            if m:
                idx = int(m.group(1))
                name = m.group(2)
                t = get_target(idx, name)
                t["samples"].append(
                    {
                        "t": float(m.group(3)),
                        "x": int(m.group(4)),
                        "y": int(m.group(5)),
                        "dist": float(m.group(6)),
                    }
                )
                continue

            m = PAT_DONE.search(line)
            if m:
                idx = int(m.group(1))
                name = m.group(2)
                t = get_target(idx, name)
                t["result"] = {
                    "status": "done",
                    "elapsed": float(m.group(3)),
                    "min_dist": float(m.group(4)),
                }
                continue

            m = PAT_FAIL.search(line)
            if m:
                idx = int(m.group(1))
                name = m.group(2)
                t = get_target(idx, name)
                t["result"] = {
                    "status": "fail",
                    "reason": m.group(3),
                    "elapsed": float(m.group(4)),
                    "min_dist": float(m.group(5)),
                }
                continue

    # Build summary
    done = 0
    fail = 0
    avg_time = 0.0
    times: List[float] = []
    for target in data["targets"].values():
        result = target.get("result")
        if not result:
            continue
        if result["status"] == "done":
            done += 1
            times.append(result["elapsed"])
        else:
            fail += 1
    if times:
        avg_time = sum(times) / len(times)

    data["summary"] = {
        "target_count": len(data["targets"]),
        "done_count": done,
        "fail_count": fail,
        "avg_done_time": avg_time,
    }
    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True, help="Path to Game.log")
    parser.add_argument("--output", default="lua_exports/runtime_pathing_data.json")
    args = parser.parse_args()

    log_path = Path(args.log)
    out_path = Path(args.output)

    if not log_path.exists():
        raise SystemExit(f"Log file not found: {log_path}")

    parsed = parse_log(log_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8")

    s = parsed["summary"]
    print(f"Saved: {out_path}")
    print(
        f"Targets={s['target_count']} done={s['done_count']} fail={s['fail_count']} "
        f"avg_done_time={s['avg_done_time']:.2f}s"
    )


if __name__ == "__main__":
    main()
