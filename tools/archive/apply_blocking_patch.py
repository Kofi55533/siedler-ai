#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Apply a blocking/walkable patch (from S5Hook export) to the 515x515 walkable map.

Updates:
- walkable_map_515.npy (full map)
- player1_walkable_515.npy (player quadrant)
- optional walkable_map_1508.npy (upsampled)
- optional root player1_walkable.npy (upsampled + cropped)

Also writes a diff report and a visual diff PNG.
"""

import argparse
import json
import re
from pathlib import Path

import numpy as np

from map_extract_config import EXTRACTED_DIR


MAP_WIDTH = 50480
MAP_HEIGHT = 50496
TARGET_GRID_W = 1508
TARGET_GRID_H = 1496


def parse_patch_origin(patch_path: Path):
    match = re.search(r"walkable_patch_515_(\d+)_(\d+)\.npy$", patch_path.name)
    if not match:
        raise ValueError(f"Could not parse patch origin from filename: {patch_path.name}")
    return int(match.group(1)), int(match.group(2))


def upsample_nearest(src: np.ndarray, target_h: int, target_w: int) -> np.ndarray:
    y_idx = np.linspace(0, src.shape[0] - 1, target_h).round().astype(int)
    x_idx = np.linspace(0, src.shape[1] - 1, target_w).round().astype(int)
    return src[y_idx][:, x_idx]


def crop_player1_quadrant(grid: np.ndarray, grid_w: int, grid_h: int) -> np.ndarray:
    scale_x = MAP_WIDTH / grid_w
    scale_y = MAP_HEIGHT / grid_h
    x_start = int((MAP_WIDTH / 2) / scale_x)
    y_end = int((MAP_HEIGHT / 2) / scale_y)
    return grid[:y_end, x_start:]


def main():
    parser = argparse.ArgumentParser(description="Apply blocking export patch to walkable grids.")
    parser.add_argument(
        "--walkable",
        default=str(EXTRACTED_DIR / "walkable_map_515.npy"),
        help="Path to base walkable_map_515.npy",
    )
    parser.add_argument(
        "--patch",
        default=str(Path("config") / "wintersturm_map_data_from_log.json" / "walkable_patch_515_255_45.npy"),
        help="Path to walkable_patch_515_*.npy from export log",
    )
    parser.add_argument(
        "--out-dir",
        default=str(EXTRACTED_DIR),
        help="Output directory for updated map_extract files",
    )
    parser.add_argument("--report", default="walkable_export_diff_report.md")
    parser.add_argument("--json-report", default="walkable_export_diff_report.json")
    parser.add_argument("--diff-png", default="walkable_export_diff.png")
    parser.add_argument("--update-1508", action="store_true", help="Also update walkable_map_1508.npy")
    parser.add_argument("--update-root", action="store_true", help="Also update root player1_walkable.npy")
    args = parser.parse_args()

    walkable_path = Path(args.walkable)
    patch_path = Path(args.patch)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    base = np.load(walkable_path)
    patch = np.load(patch_path)

    gx0, gy0 = parse_patch_origin(patch_path)
    gy1 = gy0 + patch.shape[0]
    gx1 = gx0 + patch.shape[1]

    if gy1 > base.shape[0] or gx1 > base.shape[1]:
        raise ValueError("Patch exceeds base walkable map bounds.")

    updated = base.copy()
    updated[gy0:gy1, gx0:gx1] = patch.astype(np.uint8)

    changed = updated != base
    to_walkable = (base == 0) & (updated == 1)
    to_blocked = (base == 1) & (updated == 0)

    def bbox(mask):
        ys, xs = np.where(mask)
        if len(xs) == 0:
            return None
        return {
            "x_min": int(xs.min()),
            "x_max": int(xs.max()),
            "y_min": int(ys.min()),
            "y_max": int(ys.max()),
        }

    report = {
        "base_path": str(walkable_path),
        "patch_path": str(patch_path),
        "grid_shape": [int(base.shape[0]), int(base.shape[1])],
        "patch_origin": {"gx0": gx0, "gy0": gy0},
        "patch_shape": [int(patch.shape[0]), int(patch.shape[1])],
        "changed_cells": int(np.sum(changed)),
        "changed_to_walkable": int(np.sum(to_walkable)),
        "changed_to_blocked": int(np.sum(to_blocked)),
        "changed_bbox": bbox(changed),
        "walkable_ratio_before": float(base.mean()),
        "walkable_ratio_after": float(updated.mean()),
    }

    # Save updated 515 grid
    np.save(walkable_path, updated)

    # Save updated player1 515 grid
    p1_walkable = crop_player1_quadrant(updated, base.shape[1], base.shape[0])
    np.save(out_dir / "player1_walkable_515.npy", p1_walkable)

    # Optional: update 1508 grid and root player1_walkable.npy
    if args.update_1508 or args.update_root:
        up = upsample_nearest(updated, TARGET_GRID_H, TARGET_GRID_W)
        if args.update_1508:
            np.save(out_dir / "walkable_map_1508.npy", up)
        if args.update_root:
            p1_up = crop_player1_quadrant(up, TARGET_GRID_W, TARGET_GRID_H)
            np.save(Path(__file__).resolve().parent / "player1_walkable.npy", p1_up)

    # Write reports
    Path(args.json_report).write_text(json.dumps(report, indent=2), encoding="utf-8")
    md = [
        "# Walkable Export Diff Report",
        "",
        f"- Base: `{walkable_path}`",
        f"- Patch: `{patch_path}`",
        f"- Grid: {report['grid_shape'][1]}x{report['grid_shape'][0]}",
        f"- Patch origin (gx0, gy0): {gx0}, {gy0}",
        f"- Patch shape: {patch.shape[1]}x{patch.shape[0]}",
        f"- Changed cells: {report['changed_cells']}",
        f"- To walkable: {report['changed_to_walkable']}",
        f"- To blocked: {report['changed_to_blocked']}",
        f"- Walkable ratio: {report['walkable_ratio_before']:.4f} -> {report['walkable_ratio_after']:.4f}",
    ]
    if report["changed_bbox"]:
        bb = report["changed_bbox"]
        md.append(f"- Changed bbox (grid): x={bb['x_min']}..{bb['x_max']}, y={bb['y_min']}..{bb['y_max']}")
    Path(args.report).write_text("\n".join(md) + "\n", encoding="utf-8")

    # Render diff PNG
    try:
        import matplotlib.pyplot as plt
        from matplotlib.colors import ListedColormap

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(base, cmap="Greys", origin="lower", alpha=0.6)

        # Overlay changes
        overlay = np.zeros_like(base, dtype=np.uint8)
        overlay[to_walkable] = 1
        overlay[to_blocked] = 2
        cmap = ListedColormap(["none", "lime", "red"])
        ax.imshow(overlay, cmap=cmap, origin="lower", alpha=0.9)

        ax.set_title("Walkable Patch Diff (green=walkable, red=blocked)")
        ax.set_xticks([])
        ax.set_yticks([])
        fig.tight_layout()
        fig.savefig(args.diff_png, dpi=180)
        plt.close(fig)
    except Exception as exc:
        print(f"Diff PNG failed: {exc}")


if __name__ == "__main__":
    main()
