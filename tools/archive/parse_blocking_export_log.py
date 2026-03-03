# -*- coding: utf-8 -*-
"""
Parse S5Hook blocking export log lines and create a numpy grid.

Expected log lines (export_blocking_region.lua):
  BLOCKING_EXPORT_START,x_min,x_max,y_min,y_max,step
  BROW,y,val1,val2,...
  BLOCKING_EXPORT_END
"""

import argparse
import glob
import json
import os
from pathlib import Path

import numpy as np


DEFAULT_LOG_DIRS = [
    r"%USERPROFILE%\Documents\DIE SIEDLER - DEdK\Temp\Logs\Game",
    r"%USERPROFILE%\Documents\DIE SIEDLER - DEdK\Logs\Game",
    r"%USERPROFILE%\Documents\The Settlers 5\Temp\Logs\Game",
    r"%USERPROFILE%\Documents\The Settlers 5\Logs\Game",
]


def _expand_paths(paths):
    expanded = []
    for p in paths:
        expanded.append(os.path.expandvars(p))
    return expanded


def find_latest_log(paths):
    candidates = []
    for base in _expand_paths(paths):
        if not os.path.isdir(base):
            continue
        candidates.extend(glob.glob(os.path.join(base, "*.log")))
        candidates.extend(glob.glob(os.path.join(base, "*.txt")))
    if not candidates:
        return None
    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return candidates[0]


def _strip_to_marker(line, marker):
    idx = line.find(marker)
    if idx == -1:
        return None
    return line[idx:].strip()


def parse_export_blocks(lines):
    blocks = []
    current = None

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        start = _strip_to_marker(line, "BLOCKING_EXPORT_START")
        if start:
            parts = start.split(",")
            if len(parts) >= 6:
                _, x_min, x_max, y_min, y_max, step = parts[:6]
                current = {
                    "x_min": int(x_min),
                    "x_max": int(x_max),
                    "y_min": int(y_min),
                    "y_max": int(y_max),
                    "step": int(step),
                    "rows": [],
                    "y_values": [],
                }
            continue

        if current:
            brow = _strip_to_marker(line, "BROW,")
            if brow:
                parts = brow.split(",")
                if len(parts) >= 3:
                    y_val = int(parts[1])
                    row_vals = [int(v) for v in parts[2:] if v != ""]
                    current["y_values"].append(y_val)
                    current["rows"].append(row_vals)
                continue

            end = _strip_to_marker(line, "BLOCKING_EXPORT_END")
            if end:
                blocks.append(current)
                current = None

    if current:
        blocks.append(current)

    return blocks


def build_grid(block):
    rows = block["rows"]
    if not rows:
        raise ValueError("No BROW lines found in export block.")
    max_len = max(len(r) for r in rows)
    grid = np.full((len(rows), max_len), -1, dtype=np.int16)
    for i, r in enumerate(rows):
        grid[i, :len(r)] = np.array(r, dtype=np.int16)
    return grid


def write_outputs(block, grid, out_dir, prefix):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    x_min = block["x_min"]
    x_max = block["x_max"]
    y_min = block["y_min"]
    y_max = block["y_max"]
    step = block["step"]

    base = f"{prefix}_{x_min}_{x_max}_{y_min}_{y_max}_{step}"
    npy_path = out_dir / f"{base}.npy"
    np.save(npy_path, grid)

    report = {
        "x_min": x_min,
        "x_max": x_max,
        "y_min": y_min,
        "y_max": y_max,
        "step": step,
        "rows": int(grid.shape[0]),
        "cols": int(grid.shape[1]),
        "npy": str(npy_path),
        "walkable_count": int(np.sum(grid == 0)),
        "blocked_count": int(np.sum(grid > 0)),
        "unknown_count": int(np.sum(grid < 0)),
    }
    report_path = out_dir / f"{base}.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    return npy_path, report_path


def maybe_make_walkable_patch(block, grid, out_dir):
    # If step == 100, grid aligns to 515x grid (100 units per cell).
    if block["step"] != 100:
        return None

    x_min = block["x_min"]
    y_min = block["y_min"]
    gx0 = x_min // 100
    gy0 = y_min // 100

    # grid rows correspond to y ascending.
    patch = (grid == 0).astype(np.uint8)
    patch_path = Path(out_dir) / f"walkable_patch_515_{gx0}_{gy0}.npy"
    np.save(patch_path, patch)
    return patch_path


def main():
    parser = argparse.ArgumentParser(description="Parse S5Hook blocking export log.")
    parser.add_argument("--log", default=None, help="Path to log file. If omitted, auto-detect.")
    parser.add_argument("--out", default=None, help="Output directory. Defaults to map_extract/wintersturm_extracted or current dir.")
    parser.add_argument("--prefix", default="blocking_export", help="Output file prefix.")
    args = parser.parse_args()

    if args.log:
        log_path = args.log
    else:
        log_path = find_latest_log(DEFAULT_LOG_DIRS)

    if not log_path or not os.path.isfile(log_path):
        print("No log file found. Provide --log or run the map once so a log is created.")
        return

    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    blocks = parse_export_blocks(lines)
    if not blocks:
        print(f"No export blocks found in log: {log_path}")
        return

    block = blocks[-1]
    grid = build_grid(block)

    out_dir = args.out
    if not out_dir:
        default_dir = Path("map_extract") / "wintersturm_extracted"
        out_dir = str(default_dir) if default_dir.is_dir() else "."

    npy_path, report_path = write_outputs(block, grid, out_dir, args.prefix)
    patch_path = maybe_make_walkable_patch(block, grid, out_dir)

    print(f"Log: {log_path}")
    print(f"Grid: {grid.shape[1]}x{grid.shape[0]} step={block['step']}")
    print(f"Saved: {npy_path}")
    print(f"Report: {report_path}")
    if patch_path:
        print(f"Walkable patch (515 grid): {patch_path}")


if __name__ == "__main__":
    main()
