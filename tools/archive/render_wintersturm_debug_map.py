#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Render a reproducible Wintersturm debug map for RL/action-space audits."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pathfinding
from environment import SiedlerScharfschuetzenEnv
from map_config_wintersturm import PLAYER_HQ_POSITIONS, PLAYER_1_VILLAGE_CENTER_SLOTS


DEFAULT_BUILDINGS = [
    "Wohnhaus_1",
    "Bauernhof_1",
    "Hochschule_1",
    "Kloster_1",
    "Eisenmine_1",
    "Schwefelmine_1",
    "Lehmmine_1",
    "Steinmine_1",
]

BUILD_COLORS = {
    "Wohnhaus_1": (67, 142, 255),
    "Bauernhof_1": (91, 214, 124),
    "Hochschule_1": (151, 107, 255),
    "Kloster_1": (227, 93, 194),
    "Eisenmine_1": (168, 176, 190),
    "Schwefelmine_1": (235, 210, 66),
    "Lehmmine_1": (203, 126, 66),
    "Steinmine_1": (196, 196, 186),
}

RESOURCE_COLORS = {
    "Eisen": (125, 145, 165),
    "Stein": (176, 176, 166),
    "Lehm": (188, 112, 62),
    "Schwefel": (222, 200, 52),
}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render Wintersturm walkability/action-space debug map")
    parser.add_argument("--output", default="analysis/wintersturm_debug_map.png")
    parser.add_argument("--json-output", default="analysis/wintersturm_debug_map.json")
    parser.add_argument("--scale", type=int, default=8, help="Pixels per 515-grid cell")
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--buildings", nargs="*", default=DEFAULT_BUILDINGS)
    return parser.parse_args()


def _font(size: int = 12) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()


def _world_to_grid(env: SiedlerScharfschuetzenEnv, x: float, y: float) -> tuple[float, float]:
    local_x, local_y = env.map_manager.to_local_coords(float(x), float(y))
    return local_x / pathfinding.SCALE_X, local_y / pathfinding.SCALE_Y


def _world_to_px(env: SiedlerScharfschuetzenEnv, x: float, y: float, scale: int) -> tuple[int, int]:
    gx, gy = _world_to_grid(env, x, y)
    return int(round(gx * scale)), int(round(gy * scale))


def _draw_point(draw: ImageDraw.ImageDraw, x: int, y: int, color: tuple[int, int, int], radius: int = 2) -> None:
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color, outline=(24, 24, 22))


def _draw_cross(draw: ImageDraw.ImageDraw, x: int, y: int, color: tuple[int, int, int], radius: int = 5) -> None:
    draw.line((x - radius, y, x + radius, y), fill=color, width=2)
    draw.line((x, y - radius, x, y + radius), fill=color, width=2)


def _draw_grid_overlay(draw: ImageDraw.ImageDraw, width: int, height: int, scale: int) -> None:
    if scale < 6:
        return
    line_color = (188, 198, 184, 34)
    for x in range(0, width, scale):
        draw.line((x, 0, x, height), fill=line_color)
    for y in range(0, height, scale):
        draw.line((0, y, width, y), fill=line_color)


def _terrain_panel(env: SiedlerScharfschuetzenEnv, scale: int) -> Image.Image:
    grid = env.map_manager.grid
    terrain = np.asarray(grid.terrain_base, dtype=np.uint8)
    trees = np.asarray(grid.trees, dtype=np.uint8)
    buildings = np.asarray(grid.buildings, dtype=np.uint8)

    rgb = np.zeros((grid.height, grid.width, 3), dtype=np.uint8)
    rgb[terrain == 1] = (219, 226, 209)
    rgb[terrain == 0] = (38, 45, 43)
    rgb[(terrain == 1) & (trees == 1)] = (50, 116, 70)
    rgb[(terrain == 1) & (buildings == 1)] = (112, 112, 105)

    panel = Image.fromarray(rgb, mode="RGB").resize((grid.width * scale, grid.height * scale), Image.Resampling.NEAREST)
    draw = ImageDraw.Draw(panel, "RGBA")
    _draw_grid_overlay(draw, panel.width, panel.height, scale)
    return panel


def _draw_static_objects(env: SiedlerScharfschuetzenEnv, image: Image.Image, scale: int) -> None:
    draw = ImageDraw.Draw(image, "RGBA")

    for tree_id, pos in getattr(env.map_manager.grid, "tree_positions", {}).items():
        x = int(round(pos.x * scale))
        y = int(round(pos.y * scale))
        _draw_point(draw, x, y, (23, 143, 72), radius=max(1, scale // 4))

    for category, cat_data in getattr(env, "deposit_categories", {}).items():
        color = RESOURCE_COLORS.get(str(category), (230, 210, 80))
        for deposit in cat_data.get("deposits", []):
            x, y = _world_to_px(env, deposit.get("x", 0), deposit.get("y", 0), scale)
            _draw_point(draw, x, y, color, radius=max(3, scale // 2))

    for category, cat_data in getattr(env, "shaft_categories", {}).items():
        color = RESOURCE_COLORS.get(str(category), (230, 210, 80))
        for shaft in cat_data.get("shafts", []):
            x, y = _world_to_px(env, shaft.get("x", 0), shaft.get("y", 0), scale)
            _draw_cross(draw, x, y, color, radius=max(4, scale // 2))

    hq = PLAYER_HQ_POSITIONS[1]
    hqx, hqy = _world_to_px(env, hq["x"], hq["y"], scale)
    _draw_point(draw, hqx, hqy, (255, 220, 70), radius=max(5, scale))
    draw.text((hqx + 8, hqy + 4), "HQ", fill=(20, 20, 18), font=_font(12))

    for idx, slot in enumerate(PLAYER_1_VILLAGE_CENTER_SLOTS):
        x, y = _world_to_px(env, slot["x"], slot["y"], scale)
        _draw_point(draw, x, y, (64, 218, 230), radius=max(4, scale // 2))
        draw.text((x + 6, y + 3), f"DZ{idx}", fill=(15, 45, 50), font=_font(10))


def _iter_positions(positions: Iterable[dict], env: SiedlerScharfschuetzenEnv, scale: int):
    for pos in positions:
        yield _world_to_px(env, pos.get("x", 0), pos.get("y", 0), scale), pos


def _candidate_panel(env: SiedlerScharfschuetzenEnv, scale: int, buildings: list[str]) -> tuple[Image.Image, dict]:
    panel = _terrain_panel(env, scale)
    draw = ImageDraw.Draw(panel, "RGBA")
    summary: dict[str, dict] = {}

    for building in buildings:
        candidates = list(env._get_build_position_candidates(building))
        valid = [pos for pos in candidates if env._is_build_position_candidate_valid(building, pos)]
        color = BUILD_COLORS.get(building, (120, 160, 255))
        summary[building] = {
            "universe_candidates": len(candidates),
            "currently_valid": len(valid),
            "color_rgb": list(color),
        }

        for (x, y), pos in _iter_positions(candidates, env, scale):
            draw.point((x, y), fill=(*color, 52))
        for (x, y), pos in _iter_positions(valid, env, scale):
            radius = 1 if len(valid) > 2000 else max(2, scale // 3)
            draw.rectangle((x - radius, y - radius, x + radius, y + radius), fill=(*color, 180))

    return panel, summary


def _legend(entries: list[tuple[str, tuple[int, int, int]]], width: int) -> Image.Image:
    line_h = 20
    pad = 12
    height = pad * 2 + line_h * max(1, len(entries))
    image = Image.new("RGB", (width, height), (242, 241, 234))
    draw = ImageDraw.Draw(image, "RGBA")
    font = _font(12)
    x = pad
    y = pad
    for label, color in entries:
        draw.rectangle((x, y + 3, x + 12, y + 15), fill=color, outline=(35, 35, 32))
        draw.text((x + 18, y), label, fill=(30, 30, 28), font=font)
        y += line_h
    return image


def main() -> None:
    args = _parse_args()
    os.environ.setdefault("SIEDLER_SIM_MODE", "full_sim")
    env = SiedlerScharfschuetzenEnv(render_mode=None, use_spatial_obs=False)
    env.reset(seed=args.seed)

    scale = max(2, min(20, int(args.scale)))
    left = _terrain_panel(env, scale)
    _draw_static_objects(env, left, scale)
    right, build_summary = _candidate_panel(env, scale, list(args.buildings))
    _draw_static_objects(env, right, scale)

    title_h = 44
    gap = 24
    legend_entries = [
        ("walkable terrain", (219, 226, 209)),
        ("blocked terrain", (38, 45, 43)),
        ("tree blockers", (23, 143, 72)),
        ("resource deposits/shafts", (222, 200, 52)),
        ("HQ / village-center slots", (255, 220, 70)),
    ]
    for building in args.buildings:
        legend_entries.append((f"{building}: universe faint, valid solid", BUILD_COLORS.get(building, (120, 160, 255))))
    legend = _legend(legend_entries, left.width + right.width + gap)

    out_w = left.width + right.width + gap
    out_h = title_h + left.height + legend.height
    output = Image.new("RGB", (out_w, out_h), (242, 241, 234))
    draw = ImageDraw.Draw(output, "RGBA")
    title_font = _font(15)
    draw.text((10, 12), "Wintersturm P1: walkability, resources, trees and build-position candidates", fill=(24, 24, 22), font=title_font)
    draw.text((10, 30), "Left: current terrain blockers. Right: stable action-space universe + currently valid build positions.", fill=(70, 70, 64), font=_font(11))
    output.paste(left, (0, title_h))
    output.paste(right, (left.width + gap, title_h))
    output.paste(legend, (0, title_h + left.height))

    out_path = ROOT_DIR / args.output
    json_path = ROOT_DIR / args.json_output
    out_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    output.save(out_path)

    grid = env.map_manager.grid
    report = {
        "grid_shape": [int(grid.height), int(grid.width)],
        "scale_px_per_cell": scale,
        "walkable_cells_static": int(np.sum(grid.terrain_base == 1)),
        "blocked_cells_static": int(np.sum(grid.terrain_base == 0)),
        "tree_cells": int(np.sum(grid.trees == 1)),
        "tree_count": int(len(getattr(grid, "tree_positions", {}))),
        "deposit_count": int(sum(len(v.get("deposits", [])) for v in getattr(env, "deposit_categories", {}).values())),
        "shaft_count": int(sum(len(v.get("shafts", [])) for v in getattr(env, "shaft_categories", {}).values())),
        "build_layers": build_summary,
        "outputs": {
            "png": out_path.relative_to(ROOT_DIR).as_posix(),
            "json": json_path.relative_to(ROOT_DIR).as_posix(),
        },
    }
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Debug map: {out_path}")
    print(f"Report: {json_path}")


if __name__ == "__main__":
    main()
