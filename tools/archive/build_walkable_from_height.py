#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Build a walkable grid from a decoded height map (height_map_*.npy).

Heuristic:
- water level = most frequent height value (mode)
- walkable if height > water_level and max neighbor diff <= slope_threshold

Outputs:
- full walkable grid (same size as height map)
- player1 quadrant walkable/terrain for training
- optional upsampled grids to target size (default 1508x1496)
"""

import argparse
import json
import pathlib

import numpy as np

from map_extract_config import EXTRACTED_DIR

DEFAULT_HEIGHT = EXTRACTED_DIR / "height_map_515.npy"
DEFAULT_TERRAIN_LOWRES = EXTRACTED_DIR / "terrain_lowres_131.npy"
DEFAULT_ENGINE_DECODED = pathlib.Path(__file__).resolve().parents[2] / "config" / "engine_decoded.json"
DEFAULT_OUT = pathlib.Path(__file__).resolve().parent

MAP_WIDTH = 50480
MAP_HEIGHT = 50496

# Old training grid size (for compatibility)
TARGET_GRID_W = 1508
TARGET_GRID_H = 1496


def compute_max_neighbor_diff(height: np.ndarray) -> np.ndarray:
    h = height.astype(np.int32)
    padded = np.pad(h, 1, mode="edge")
    center = padded[1:-1, 1:-1]
    max_diff = np.zeros_like(center, dtype=np.int32)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            neigh = padded[1 + dy:1 + dy + h.shape[0], 1 + dx:1 + dx + h.shape[1]]
            diff = np.abs(center - neigh)
            max_diff = np.maximum(max_diff, diff)
    return max_diff


def upsample_nearest(src: np.ndarray, target_h: int, target_w: int) -> np.ndarray:
    """Nearest-neighbor upsample to (target_h, target_w)."""
    src_h, src_w = src.shape
    y_idx = np.linspace(0, src_h - 1, target_h).round().astype(int)
    x_idx = np.linspace(0, src_w - 1, target_w).round().astype(int)
    return src[y_idx][:, x_idx]


def crop_player1_quadrant(grid: np.ndarray, grid_w: int, grid_h: int):
    scale_x = MAP_WIDTH / grid_w
    scale_y = MAP_HEIGHT / grid_h
    x_start = int((MAP_WIDTH / 2) / scale_x)
    x_end = int(MAP_WIDTH / scale_x)
    y_start = 0
    y_end = int((MAP_HEIGHT / 2) / scale_y)
    return grid[y_start:y_end, x_start:x_end]


def load_blocked_terrain_values(path: pathlib.Path) -> set[int]:
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    terrain = data.get("terrain") or {}
    values = set()
    for item in terrain.get("blocked_types") or []:
        try:
            values.add(int(item.get("value")))
        except (AttributeError, TypeError, ValueError):
            continue
    return values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--height", default=str(DEFAULT_HEIGHT))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--terrain-lowres", default=str(DEFAULT_TERRAIN_LOWRES))
    parser.add_argument("--engine-decoded", default=str(DEFAULT_ENGINE_DECODED))
    parser.add_argument("--no-terrain-blocking", action="store_true")
    parser.add_argument("--water-level", type=int, default=None)
    parser.add_argument("--slope-threshold", type=int, default=None)
    parser.add_argument("--slope-quantile", type=float, default=0.8)
    parser.add_argument("--upsample", action="store_true", help="Also write 1508x1496 grids")
    args = parser.parse_args()

    height_path = pathlib.Path(args.height)
    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    height = np.load(height_path)
    h, w = height.shape

    # Water level = mode by default
    if args.water_level is None:
        vals, counts = np.unique(height, return_counts=True)
        water_level = int(vals[counts.argmax()])
    else:
        water_level = args.water_level

    max_diff = compute_max_neighbor_diff(height)
    land_mask = height > water_level

    if args.slope_threshold is None:
        md_land = max_diff[land_mask]
        slope_threshold = int(np.quantile(md_land, args.slope_quantile))
    else:
        slope_threshold = args.slope_threshold

    walkable = (height > water_level) & (max_diff <= slope_threshold)

    terrain_blocking_report = None
    if not args.no_terrain_blocking:
        terrain_path = pathlib.Path(args.terrain_lowres)
        engine_path = pathlib.Path(args.engine_decoded)
        blocked_values = load_blocked_terrain_values(engine_path)
        if terrain_path.exists() and blocked_values:
            terrain_lowres = np.load(terrain_path)
            terrain_at_height = upsample_nearest(terrain_lowres, h, w)
            terrain_blocked = np.isin(terrain_at_height, list(blocked_values))
            before = int(np.sum(walkable))
            walkable = walkable & (~terrain_blocked)
            terrain_blocking_report = {
                "terrain_lowres": str(terrain_path),
                "engine_decoded": str(engine_path),
                "blocked_values": sorted(int(v) for v in blocked_values),
                "blocked_values_present": sorted(
                    int(v) for v in set(np.unique(terrain_lowres).astype(int)) & blocked_values
                ),
                "blocked_cells_at_height_grid": int(np.sum(terrain_blocked)),
                "walkable_cells_removed": int(before - np.sum(walkable)),
            }

    walkable = walkable.astype(np.uint8)

    # Save full grids
    full_walkable_path = out_dir / f"walkable_map_{h}.npy"
    np.save(full_walkable_path, walkable)

    # Player 1 quadrant (native grid)
    p1_walkable_native = crop_player1_quadrant(walkable, w, h)
    p1_height_native = crop_player1_quadrant(height, w, h)
    np.save(out_dir / f"player1_walkable_{h}.npy", p1_walkable_native)
    np.save(out_dir / f"player1_terrain_{h}.npy", p1_height_native)

    report = {
        "height_shape": [int(h), int(w)],
        "water_level": int(water_level),
        "slope_threshold": int(slope_threshold),
        "walkable_ratio_full": float(walkable.mean()),
        "walkable_ratio_land": float(walkable[land_mask].mean()) if land_mask.any() else 0.0,
        "player1_shape_native": list(p1_walkable_native.shape),
        "terrain_blocking": terrain_blocking_report,
    }

    # Optional upsample to legacy training grid
    if args.upsample:
        up_walkable = upsample_nearest(walkable, TARGET_GRID_H, TARGET_GRID_W)
        up_height = upsample_nearest(height, TARGET_GRID_H, TARGET_GRID_W)

        p1_walkable = crop_player1_quadrant(up_walkable, TARGET_GRID_W, TARGET_GRID_H)
        p1_height = crop_player1_quadrant(up_height, TARGET_GRID_W, TARGET_GRID_H)

        np.save(out_dir / "walkable_map_1508.npy", up_walkable)
        np.save(out_dir / "terrain_map_1508.npy", up_height)

        # Overwrite training files in repo root
        np.save(DEFAULT_OUT / "player1_walkable.npy", p1_walkable)
        np.save(DEFAULT_OUT / "player1_terrain.npy", p1_height)

        report["upsample"] = {
            "target_shape": [TARGET_GRID_H, TARGET_GRID_W],
            "player1_shape": list(p1_walkable.shape),
        }

    report_path = out_dir / "walkable_from_height_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("Walkable map built:")
    print(f"  full walkable: {full_walkable_path}")
    print(f"  player1 (native): {out_dir / f'player1_walkable_{h}.npy'}")
    if args.upsample:
        print(f"  player1 (upsampled): {DEFAULT_OUT / 'player1_walkable.npy'}")
    print(f"  report: {report_path}")


if __name__ == "__main__":
    main()
