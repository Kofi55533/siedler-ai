#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Erstellt eine klare Ãœbersichtsgrafik der Wintersturm-Karte:
1) Heightmap (515x515)
2) Walkable-Map (515x515)
3) Low-Res Terrain (131x131, hochskaliert)
4) Spieler-1-Quadrant mit Ressourcen/HQ/DZ
"""

import json
import os
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from map_extract_config import EXTRACTED_DIR
from map_config_wintersturm import MAP_SIZE, PLAYER_HQ_POSITIONS, PLAYER_1_VILLAGE_CENTER_SLOTS


ROOT_DIR = Path(__file__).resolve().parent
MAP_DATA_PATH = ROOT_DIR / "config" / "wintersturm_map_data.json"

HEIGHT_PATH = EXTRACTED_DIR / "height_map_515.npy"
WALKABLE_PATH = EXTRACTED_DIR / "walkable_map_515.npy"
LOWRES_PATH = EXTRACTED_DIR / "terrain_lowres_131.npy"

OUTPUT_PATH = ROOT_DIR / "map_overview.png"
OUTPUT_PATH_2 = ROOT_DIR / "map_visualization.png"


def upsample_nearest(src: np.ndarray, target_h: int, target_w: int) -> np.ndarray:
    ys = np.linspace(0, src.shape[0] - 1, target_h).round().astype(int)
    xs = np.linspace(0, src.shape[1] - 1, target_w).round().astype(int)
    return src[ys][:, xs]


def world_to_grid(x: float, y: float, grid_w: int, grid_h: int):
    scale_x = MAP_SIZE[0] / (grid_w - 1)
    scale_y = MAP_SIZE[1] / (grid_h - 1)
    gx = int(round(x / scale_x))
    gy = int(round(y / scale_y))
    return gx, gy


def main():
    if not HEIGHT_PATH.exists() or not WALKABLE_PATH.exists():
        raise SystemExit("Height/Walkable Layer fehlen. Bitte decode + build_walkable zuerst ausfÃ¼hren.")

    height = np.load(HEIGHT_PATH)
    walkable = np.load(WALKABLE_PATH)
    lowres = np.load(LOWRES_PATH) if LOWRES_PATH.exists() else None

    grid_h, grid_w = height.shape
    p1_min_x = MAP_SIZE[0] / 2
    p1_max_y = MAP_SIZE[1] / 2
    x_start = int(round(p1_min_x / (MAP_SIZE[0] / (grid_w - 1))))
    y_end = int(round(p1_max_y / (MAP_SIZE[1] / (grid_h - 1))))

    # Load map data (resources)
    with open(MAP_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    fig, axes = plt.subplots(2, 2, figsize=(18, 16))

    # Panel 1: Heightmap
    ax = axes[0, 0]
    im = ax.imshow(height, cmap="terrain", origin="lower")
    ax.set_title("Heightmap (515x515)")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    # Panel 2: Walkable
    ax = axes[0, 1]
    ax.imshow(walkable, cmap="Greens", origin="lower")
    ax.set_title("Walkable (515x515)")

    # Panel 3: Low-Res Terrain (upsampled)
    ax = axes[1, 0]
    if lowres is not None:
        low_up = upsample_nearest(lowres, grid_h, grid_w)
        ax.imshow(low_up, cmap="tab20", origin="lower")
        ax.set_title("Low-Res Terrain (131x131 -> 515x515)")
    else:
        ax.text(0.5, 0.5, "Low-Res Terrain nicht gefunden", ha="center", va="center")
        ax.set_title("Low-Res Terrain")

    # Panel 4: Player-1 Quadrant Overlay
    ax = axes[1, 1]
    quad = walkable[:y_end, x_start:]
    ax.imshow(quad, cmap="Greens", origin="lower")
    ax.set_title("Spieler 1 Quadrant (Walkable + Ressourcen)")

    # HQ and DZ (Player 1)
    hq1 = PLAYER_HQ_POSITIONS[1]
    hq_gx, hq_gy = world_to_grid(hq1["x"], hq1["y"], grid_w, grid_h)
    ax.plot(hq_gx - x_start, hq_gy, "y*", markersize=12, label="HQ")

    for dz in PLAYER_1_VILLAGE_CENTER_SLOTS:
        gx, gy = world_to_grid(dz["x"], dz["y"], grid_w, grid_h)
        ax.plot(gx - x_start, gy, "co", markersize=6, label="DZ-Slot")

    # Mine slots & deposits (Player 1 quadrant)
    for resource, slots in data.get("mine_slots", {}).items():
        for s in slots:
            if s["position"]["x"] > p1_min_x and s["position"]["y"] < p1_max_y:
                gx, gy = world_to_grid(s["position"]["x"], s["position"]["y"], grid_w, grid_h)
                ax.plot(gx - x_start, gy, "r^", markersize=5)

    for resource, deps in data.get("deposits", {}).items():
        for d in deps:
            if d["position"]["x"] > p1_min_x and d["position"]["y"] < p1_max_y:
                gx, gy = world_to_grid(d["position"]["x"], d["position"]["y"], grid_w, grid_h)
                ax.plot(gx - x_start, gy, "mo", markersize=4)

    # De-duplicate legend entries
    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    if unique:
        ax.legend(unique.values(), unique.keys(), loc="upper right", fontsize=8)

    for ax in axes.flat:
        ax.set_xticks([])
        ax.set_yticks([])

    plt.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=160)
    fig.savefig(OUTPUT_PATH_2, dpi=160)
    plt.close(fig)

    print(f"Gespeichert: {OUTPUT_PATH}")
    print(f"Gespeichert: {OUTPUT_PATH_2}")


if __name__ == "__main__":
    main()
