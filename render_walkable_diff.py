#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Render a debug overlay to highlight borderline walkable areas.
Shows where land is blocked only due to slope threshold (near-threshold).
"""

import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from map_extract_config import EXTRACTED_DIR
from map_config_wintersturm import MAP_SIZE


REPORT_PATH = EXTRACTED_DIR / "walkable_from_height_report.json"
HEIGHT_PATH = EXTRACTED_DIR / "height_map_515.npy"
WALKABLE_PATH = EXTRACTED_DIR / "walkable_map_515.npy"
OUTPUT_PATH = Path(__file__).resolve().parent / "walkable_diff.png"


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


def main():
    height = np.load(HEIGHT_PATH)
    walkable = np.load(WALKABLE_PATH)
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))

    water = report["water_level"]
    # near-threshold range
    lo = 80
    hi = 120

    max_diff = compute_max_neighbor_diff(height)
    land = height > water
    near = land & (walkable == 0) & (max_diff >= lo) & (max_diff <= hi)

    h, w = walkable.shape
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.imshow(walkable, cmap="Greens", origin="lower")
    ax.imshow(near, cmap="Reds", origin="lower", alpha=0.7)
    ax.set_title("Walkable (grün) + near-threshold block (rot)")
    ax.set_xticks([])
    ax.set_yticks([])

    # Draw player1 quadrant box
    scale_x = MAP_SIZE[0] / (w - 1)
    scale_y = MAP_SIZE[1] / (h - 1)
    p1_x = int(round((MAP_SIZE[0] / 2) / scale_x))
    p1_y = int(round((MAP_SIZE[1] / 2) / scale_y))
    ax.plot([p1_x, w - 1], [p1_y, p1_y], color="yellow", linewidth=1.5)
    ax.plot([p1_x, p1_x], [0, p1_y], color="yellow", linewidth=1.5)

    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=180)
    plt.close(fig)
    print(f"Gespeichert: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
