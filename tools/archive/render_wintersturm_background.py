#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Render a game-like Wintersturm player-1 background from extracted map data.

This is not a replacement for the Settlers 5 3D engine. It uses the extracted
Wintersturm terrain layers plus local original DDS terrain/object textures to
create a deterministic, high-resolution 2D map background for replay inspection.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from map_config_wintersturm import MAP_SIZE

EXTRACTED_DIR = ROOT_DIR / "map_extract" / "wintersturm_extracted"
MAP_JSON = ROOT_DIR / "config" / "wintersturm_map_data.json"

P1_X_MIN = MAP_SIZE[0] / 2.0
P1_X_MAX = float(MAP_SIZE[0])
P1_Y_MIN = 0.0
P1_Y_MAX = MAP_SIZE[1] / 2.0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rendert eine Wintersturm-P1-Karte aus Original-Assets")
    parser.add_argument("--game-root", type=str, default="")
    parser.add_argument("--output", type=str, default="analysis/replays/wintersturm_p1_original_map.png")
    parser.add_argument("--size", type=int, default=1536)
    parser.add_argument("--no-objects", action="store_true")
    return parser.parse_args()


def _candidate_game_roots(explicit: str) -> list[Path]:
    roots: list[Path] = []
    if explicit:
        roots.append(Path(explicit))
    env_root = os.environ.get("SIEDLER_GAME_ROOT") or os.environ.get("SETTLERS5_ROOT")
    if env_root:
        roots.append(Path(env_root))
    roots.extend(
        [
            ROOT_DIR.parent / "Gold edition",
            Path.home() / "Desktop" / "Gold edition",
            ROOT_DIR.parent / "The Settlers 5",
            Path.home() / "Desktop" / "The Settlers 5",
        ]
    )
    seen: set[str] = set()
    out: list[Path] = []
    for root in roots:
        key = str(root).lower()
        if key in seen:
            continue
        seen.add(key)
        if (root / "base" / "shr" / "graphics" / "Textures").exists():
            out.append(root)
    return out


def find_game_root(explicit: str = "") -> Path | None:
    candidates = _candidate_game_roots(explicit)
    return candidates[0] if candidates else None


def _load_texture(game_root: Path | None, rel: str, size: int = 192) -> Image.Image:
    fallback = Image.new("RGB", (size, size), (125, 128, 116))
    if game_root is None:
        return fallback
    path = game_root / "base" / "shr" / "graphics" / "Textures" / rel
    if not path.exists():
        path = game_root / "base" / "shr" / "graphics" / "TexturesLow" / rel
    if not path.exists():
        return fallback
    try:
        img = Image.open(path).convert("RGB")
    except Exception:
        return fallback
    if img.width < size or img.height < size:
        img = img.resize((size, size), Image.Resampling.BILINEAR)
    return img


def _texture_set(game_root: Path | None) -> dict[str, Image.Image]:
    names = {
        "snow1": "Terrain/Snow01.dds",
        "snow2": "Terrain/Snow02.dds",
        "snow3": "Terrain/Snow03.dds",
        "snow4": "Terrain/Snow04.dds",
        "rock_dark": "Terrain/RockDarkNorth01B.dds",
        "rock_light": "Terrain/RockLight01B.dds",
        "earth": "Terrain/EarthBrightNorth01B.dds",
        "mud": "Terrain/MudDark01B.dds",
        "ice": "Water/Ice01Base.dds",
    }
    return {key: _load_texture(game_root, rel) for key, rel in names.items()}


def _crop_p1(arr: np.ndarray) -> np.ndarray:
    h, w = arr.shape[:2]
    return arr[: h // 2, w // 2 :]


def _upsample_nearest(arr: np.ndarray, size: int) -> np.ndarray:
    src_h, src_w = arr.shape[:2]
    ys = np.linspace(0, src_h - 1, size).round().astype(np.int32)
    xs = np.linspace(0, src_w - 1, size).round().astype(np.int32)
    return arr[ys][:, xs]


def _render_texture_field(lowres: np.ndarray, height: np.ndarray, walkable: np.ndarray, textures: dict[str, Image.Image], size: int) -> Image.Image:
    terrain = _upsample_nearest(lowres, size)
    height_u = _upsample_nearest(height, size).astype(np.float32)
    walk_u = _upsample_nearest(walkable, size).astype(bool)
    h_norm = (height_u - float(height_u.min())) / max(1.0, float(height_u.max() - height_u.min()))

    # Deterministic terrain classification. The exact engine texture-splat map is
    # not decoded here, so this combines the extracted terrain IDs, height, and
    # walkability with original winter/rock/ice textures.
    categories = np.full((size, size), "snow1", dtype=object)
    categories[(terrain % 5) == 0] = "snow2"
    categories[(terrain % 7) == 0] = "snow3"
    categories[(terrain % 11) == 0] = "snow4"
    categories[(terrain < 30) & walk_u] = "earth"
    categories[(terrain >= 100) & walk_u] = "snow2"
    categories[(~walk_u) & (h_norm > 0.42)] = "rock_dark"
    categories[(~walk_u) & (h_norm > 0.66)] = "rock_light"
    categories[(~walk_u) & (h_norm <= 0.42)] = "ice"
    categories[(terrain == 25) | (terrain == 26)] = "mud"

    out = Image.new("RGB", (size, size), (190, 194, 185))
    tile = 96
    arr = np.zeros((size, size, 3), dtype=np.uint8)
    tex_arrays = {key: np.asarray(img.resize((tile, tile), Image.Resampling.BILINEAR), dtype=np.uint8) for key, img in textures.items()}
    yy = np.arange(size)[:, None] % tile
    xx = np.arange(size)[None, :] % tile
    for key, tex_arr in tex_arrays.items():
        mask = categories == key
        if not mask.any():
            continue
        sampled = tex_arr[yy, xx]
        arr[mask] = sampled[mask]

    shade = (0.70 + h_norm * 0.42).clip(0.55, 1.14)
    # Make blocked cliffs stronger and walkable snow softer.
    shade[~walk_u] *= 0.82
    shade[walk_u] *= 1.04
    arr = np.clip(arr.astype(np.float32) * shade[:, :, None], 0, 255).astype(np.uint8)
    out = Image.fromarray(arr, mode="RGB")
    out = ImageEnhance.Contrast(out).enhance(1.10)
    out = ImageEnhance.Color(out).enhance(0.92)
    return out


def _world_to_image(x: float, y: float, size: int) -> tuple[int, int]:
    nx = (float(x) - P1_X_MIN) / max(1.0, P1_X_MAX - P1_X_MIN)
    ny = (float(y) - P1_Y_MIN) / max(1.0, P1_Y_MAX - P1_Y_MIN)
    px = int(round(nx * (size - 1)))
    py = int(round(ny * (size - 1)))
    return max(0, min(size - 1, px)), max(0, min(size - 1, py))


def _in_p1(pos: dict[str, Any]) -> bool:
    x = float(pos.get("x", 0.0))
    y = float(pos.get("y", 0.0))
    return P1_X_MIN <= x <= P1_X_MAX and P1_Y_MIN <= y <= P1_Y_MAX


def _draw_objects(img: Image.Image, game_root: Path | None, size: int) -> None:
    if not MAP_JSON.exists():
        return
    data = json.loads(MAP_JSON.read_text(encoding="utf-8"))
    draw = ImageDraw.Draw(img, "RGBA")

    # Draw trees first, as small deterministic conifer marks.
    for tree in data.get("trees", []):
        pos = tree.get("position") or {}
        if not _in_p1(pos):
            continue
        x, y = _world_to_image(pos.get("x", 0), pos.get("y", 0), size)
        scale = 0.85 if "small" in str(tree.get("type", "")).lower() else 1.0
        r = max(2, int(round(size / 420 * scale)))
        draw.polygon([(x, y - r * 2), (x - r, y + r), (x + r, y + r)], fill=(42, 83, 56, 210), outline=(182, 203, 178, 80))
        draw.line((x, y + r, x, y + r * 2), fill=(76, 58, 37, 160), width=1)

    resource_colors = {
        "iron": (128, 92, 66, 225),
        "stone": (150, 151, 145, 225),
        "clay": (179, 118, 71, 225),
        "sulfur": (218, 184, 55, 225),
    }
    for key, items in data.get("deposits", {}).items():
        for item in items:
            pos = item.get("position") or {}
            if not _in_p1(pos):
                continue
            x, y = _world_to_image(pos.get("x", 0), pos.get("y", 0), size)
            r = max(5, int(size / 145))
            color = resource_colors.get(key, (220, 200, 100, 225))
            draw.ellipse((x - r, y - r, x + r, y + r), fill=color, outline=(45, 38, 28, 180), width=1)

    for key, items in data.get("mine_slots", {}).items():
        for item in items:
            pos = item.get("position") or {}
            if not _in_p1(pos):
                continue
            x, y = _world_to_image(pos.get("x", 0), pos.get("y", 0), size)
            r = max(6, int(size / 128))
            color = resource_colors.get(key, (180, 100, 90, 225))
            draw.rectangle((x - r, y - r, x + r, y + r), fill=(*color[:3], 150), outline=(250, 230, 170, 190), width=1)

    for slot in data.get("village_center_slots", []):
        pos = slot.get("position") or {}
        if not _in_p1(pos):
            continue
        x, y = _world_to_image(pos.get("x", 0), pos.get("y", 0), size)
        r = max(7, int(size / 118))
        draw.rectangle((x - r, y - r, x + r, y + r), outline=(230, 192, 83, 210), width=max(1, int(size / 512)))

    for building in (data.get("players", {}).get("1", {}).get("buildings", []) or []):
        pos = building.get("position") or {}
        if not _in_p1(pos):
            continue
        x, y = _world_to_image(pos.get("x", 0), pos.get("y", 0), size)
        r = max(11, int(size / 70))
        draw.rectangle((x - r, y - r, x + r, y + r), fill=(130, 68, 45, 170), outline=(244, 207, 107, 230), width=max(2, int(size / 420)))


def render_background(game_root: Path | None, output: Path, size: int = 1536, draw_objects: bool = True) -> Path:
    height = _crop_p1(np.load(EXTRACTED_DIR / "height_map_515.npy"))
    walkable = _crop_p1(np.load(EXTRACTED_DIR / "walkable_map_515.npy"))
    lowres = _crop_p1(np.load(EXTRACTED_DIR / "terrain_lowres_131.npy"))

    textures = _texture_set(game_root)
    image = _render_texture_field(lowres, height, walkable, textures, int(size))
    if draw_objects:
        _draw_objects(image, game_root, int(size))

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, quality=94)
    return output


def main() -> None:
    args = _parse_args()
    root = find_game_root(args.game_root)
    output = render_background(root, Path(args.output), int(args.size), draw_objects=not args.no_objects)
    print(f"Wintersturm map background: {output}")
    print(f"Game root: {root if root else 'not found'}")


if __name__ == "__main__":
    main()
