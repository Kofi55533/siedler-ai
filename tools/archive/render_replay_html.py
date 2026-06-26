#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Exportiert ein interaktives HTML-Replay fuer die Expert-Opening-Simulation."""

from __future__ import annotations

import argparse
import html
import json
import math
import os
import shutil
import sys
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from environment import ActionPhase, SiedlerScharfschuetzenEnv
from expert_opening import ExpertOpeningController
from tools.archive.export_original_graphics import export_original_graphics_report
from tools.archive.render_wintersturm_background import (
    EXTRACTED_DIR,
    _render_texture_field,
    _texture_set,
    render_background as render_wintersturm_background,
)
from tools.archive import render_replay_mp4 as replay


def _parse_args():
    parser = argparse.ArgumentParser(description="Interaktives HTML-Replay fuer Siedler Expert Opening")
    parser.add_argument("--steps", type=int, default=260)
    parser.add_argument("--frame-every", type=int, default=1)
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--render-scale", type=int, default=5)
    parser.add_argument("--background", type=str, default="", help="Optionaler Kartenhintergrund. Leer = Wintersturm-Originalkarte automatisch rendern")
    parser.add_argument("--output-dir", type=str, default="analysis/replays/expert_opening_interactive")
    parser.add_argument("--strategy", choices=["expert_opening", "opening_v1", "random"], default="expert_opening")
    parser.add_argument("--sim-mode", choices=["full_sim", "fast_train", ""], default="full_sim")
    parser.add_argument("--viewport", choices=["full", "bottom_right"], default="full")
    parser.add_argument("--jpg-quality", type=int, default=88)
    parser.add_argument("--labels", action="store_true", help="Textlabels direkt ins Kartenbild zeichnen")
    parser.add_argument("--hud", action="store_true", help="HUD direkt ins Kartenbild zeichnen")
    parser.add_argument("--no-paths", action="store_true")
    parser.add_argument("--wintersturm-background-size", type=int, default=1536, help="Aufloesung der automatisch gerenderten Wintersturm-Karte")
    parser.add_argument("--no-wintersturm-background", action="store_true", help="Keine automatisch gerenderte Wintersturm-Karte verwenden")
    parser.add_argument("--entity-render-mode", choices=["sprite", "mesh", "gui", "none"], default="sprite", help="Karten-Entitaeten als DFF/DDS-Sprites, DFF-Mesh-Sprites, GUI-Icons oder gar nicht ueberblenden")
    parser.add_argument(
        "--game-root",
        type=str,
        default="",
        help="Pfad zur Siedler-5/Gold-Edition. Wenn gesetzt/gefunden, werden lokale Original-GUI-Assets genutzt.",
    )
    parser.add_argument("--no-game-assets", action="store_true", help="Keine Original-Spielgrafiken in das Replay kopieren")
    parser.add_argument("--no-game-icon-overlay", action="store_true", help="Keine Original-Entitaets-Overlays in die Kartenframes zeichnen")
    parser.add_argument("--bake-entity-overlay", action="store_true", help="Entitaeten zusaetzlich direkt in die JPG-Frames brennen")
    parser.add_argument("--no-original-graphics-report", action="store_true", help="Keinen DFF/DDS/ANM-Originalgrafik-Report erzeugen")
    parser.add_argument("--refresh-original-graphics-report", action="store_true", help="Originalgrafik-Report neu erzeugen, auch wenn er schon existiert")
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
            ROOT_DIR.parent / "The Settlers 5",
            ROOT_DIR.parent / "TheSettlers5",
            Path.home() / "Desktop" / "Gold edition",
            Path.home() / "Desktop" / "The Settlers 5",
            Path.home() / "Desktop" / "TheSettlers5",
        ]
    )
    seen: set[str] = set()
    unique: list[Path] = []
    for root in roots:
        key = str(root).lower()
        if key not in seen:
            seen.add(key)
            unique.append(root)
    return unique


def _find_game_root(explicit: str) -> Path | None:
    for root in _candidate_game_roots(explicit):
        if (root / "base" / "shr" / "graphics").exists():
            return root
    return None


def _copy_png_tree(src: Path, dst: Path) -> int:
    if not src.exists():
        return 0
    copied = 0
    for file_path in src.rglob("*.png"):
        rel = file_path.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.stat().st_mtime < file_path.stat().st_mtime:
            shutil.copy2(file_path, target)
        copied += 1
    return copied


def _rel_asset(output_dir: Path, asset_path: Path | None) -> str:
    if asset_path is None or not asset_path.exists():
        return ""
    return asset_path.relative_to(output_dir).as_posix()


def _first_existing(*paths: Path) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def _export_game_assets(output_dir: Path, game_root: Path | None, disabled: bool) -> dict:
    if disabled or game_root is None:
        return {"enabled": False, "copied": 0, "assets": {}, "payday_frames": []}

    assets_dir = output_dir / "assets" / "game"
    gui_roots = {
        "base_gui": game_root / "base" / "shr" / "graphics" / "Textures" / "GUI",
        "extra1_gui": game_root / "extra1" / "shr" / "graphics" / "textures" / "GUI",
        "extra2_gui": game_root / "extra2" / "shr" / "graphics" / "textures" / "GUI",
    }
    copied = 0
    for name, src in gui_roots.items():
        copied += _copy_png_tree(src, assets_dir / name)

    base_gui = assets_dir / "base_gui"
    extra2_gui = assets_dir / "extra2_gui"
    important = {
        "bg_top": _first_existing(base_gui / "bg_top.png", extra2_gui / "bg_top.png"),
        "bg_bottom": _first_existing(base_gui / "bg_bottom_dbg.png", base_gui / "bg_bottom.png"),
        "bg_window": _first_existing(base_gui / "bg_windowComplete.png", base_gui / "bg_statistics.png"),
        "bg_window_mm": _first_existing(base_gui / "bg_windowComplete_mm.png", base_gui / "minimapBGlarge.png"),
        "bg_tooltip": _first_existing(base_gui / "bg_tooltip.png", base_gui / "bg_tooltip_msg.png"),
        "slider": _first_existing(base_gui / "bg_slider.png"),
        "gold": _first_existing(base_gui / "i_res_gold.png", base_gui / "i_res_gold_large.png"),
        "wood": _first_existing(base_gui / "i_res_wood.png", base_gui / "i_res_wood_large.png"),
        "stone": _first_existing(base_gui / "i_res_stone.png", base_gui / "i_res_stone_large.png"),
        "mud": _first_existing(base_gui / "i_res_mud.png", base_gui / "i_res_mud_large.png"),
        "iron": _first_existing(base_gui / "i_res_iron.png", base_gui / "i_res_iron_large.png"),
        "sulfur": _first_existing(base_gui / "i_res_sulfur.png", base_gui / "i_res_sulfur_large.png"),
        "serf": _first_existing(base_gui / "b_select_serf.png", base_gui / "MO_CU_Serf.png"),
        "worker": _first_existing(base_gui / "i_workers.png", base_gui / "b_units_worker.png"),
        "site": _first_existing(base_gui / "b_generic_building.png"),
        "headquarter": _first_existing(base_gui / "b_headquarter.png"),
        "university": _first_existing(base_gui / "b_civil_university.png", extra2_gui / "b_civil_university.png"),
        "monastery": _first_existing(base_gui / "b_civil_church.png"),
        "village": _first_existing(base_gui / "b_civil_keep.png"),
        "farm": _first_existing(base_gui / "i_res_farms.png"),
        "residence": _first_existing(base_gui / "i_res_residences.png"),
        "mine": _first_existing(base_gui / "b_small_generic.png", base_gui / "b_generic_building.png"),
        "minimap_bg": _first_existing(base_gui / "minimapBGlarge.png", base_gui / "bg_windowComplete_mm.png"),
        "minimap_normal": _first_existing(base_gui / "b_minimap_normal.png"),
        "minimap_tactics": _first_existing(base_gui / "b_minimap_tactics.png"),
        "minimap_alchemy": _first_existing(base_gui / "b_minimap_alchemy.png"),
        "tab_build": _first_existing(base_gui / "Tab_BuildHouse_on.png", base_gui / "Tab_BuildHouse_off.png"),
        "tab_workers": _first_existing(base_gui / "Tab_Workers_on.png", base_gui / "Tab_Workers_off.png"),
        "tab_motivation": _first_existing(base_gui / "Tab_BuildMotiv_on.png", base_gui / "Tab_BuildMotiv_off.png"),
        "select_serf_button": _first_existing(base_gui / "b_select_serf.png", base_gui / "b_units_serf.png"),
        "select_worker_button": _first_existing(base_gui / "b_units_worker.png", base_gui / "i_workers.png"),
        "generic_settler": _first_existing(base_gui / "b_generic_settler.png"),
        "generic_building": _first_existing(base_gui / "b_generic_building.png"),
        "onscreen_worker": _first_existing(base_gui / "onScreen_Worker.png", base_gui / "onScreen_NoWorker.png"),
        "onscreen_serf": _first_existing(base_gui / "onScreen_Emotion_serf.png", base_gui / "MO_CU_Serf.png"),
        "trail_toggle": _first_existing(base_gui / "onScreen_NPCmarker.png", base_gui / "miniMap_Signal_0.png", base_gui / "MoveCamera.png"),
        "to_building": _first_existing(base_gui / "ToBuilding.png"),
        "to_worker": _first_existing(base_gui / "ToWorker.png"),
        "ok": _first_existing(base_gui / "ok.png", base_gui / "trade_ok.png"),
        "arrow": _first_existing(base_gui / "dbg_arrow.png", base_gui / "GCWindow" / "MoveCamera.png"),
        "plus": _first_existing(base_gui / "trade_plus.png"),
        "minus": _first_existing(base_gui / "trade_minus.png"),
    }
    payday_frames = sorted(base_gui.glob("payday*.png"))
    return {
        "enabled": copied > 0,
        "copied": copied,
        "root": str(game_root),
        "assets": {name: _rel_asset(output_dir, path) for name, path in important.items()},
        "payday_frames": [_rel_asset(output_dir, path) for path in payday_frames],
    }


def _compact_animation_manifest(entries: list[dict]) -> dict:
    by_role: dict[str, dict] = {}
    files: list[dict] = []
    for entry in entries:
        role = str(entry.get("role") or (entry.get("anm") or {}).get("role") or "other")
        anm = entry.get("anm") or {}
        record = {
            "name": str(entry.get("name") or ""),
            "role": role,
            "duration": float(anm.get("duration") or 0.0),
            "keyframes": int(anm.get("keyframes") or 0),
            "keyframe_bytes": int(anm.get("keyframe_bytes") or 0),
            "parsed": bool(anm.get("parsed")),
            "track_data": str(entry.get("track_data") or ""),
            "track_node_count": int(((anm.get("track_topology") or {}).get("node_count") or 0)),
        }
        files.append(record)
        if not record["parsed"]:
            continue
        existing = by_role.get(role)
        if existing is None or (
            bool(record["track_data"]) and not bool(existing.get("track_data"))
        ) or (
            bool(record["track_data"]) == bool(existing.get("track_data"))
            and role in {"idle", "walk", "run", "work"}
            and record["duration"] > 0
            and record["keyframes"] >= int(existing.get("keyframes", 0))
        ):
            by_role[role] = record
    return {"files": files, "by_role": by_role}


def _export_original_graphics(
    output_dir: Path,
    game_root: Path | None,
    disabled: bool,
    refresh: bool,
) -> dict:
    if disabled or game_root is None:
        return {"enabled": False}

    report_dir = output_dir / "original_graphics"
    manifest_path = report_dir / "manifest.json"
    index_path = report_dir / "index.html"
    if manifest_path.exists() and index_path.exists() and not refresh:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            manifest = export_original_graphics_report(game_root, report_dir, thumb_size=220)
    else:
        manifest = export_original_graphics_report(game_root, report_dir, thumb_size=220)

    sample_keys = ("serf_idle", "headquarters_1", "university_1", "tree_fir")
    sample_sprites: dict[str, str] = {}
    sample_meshes: dict[str, str] = {}
    sprite_by_key: dict[str, str] = {}
    mesh_by_key: dict[str, str] = {}
    model3d_by_key: dict[str, str] = {}
    embedded_model3d: dict[str, dict] = {}
    animation_by_key: dict[str, dict] = {}
    for entity in manifest.get("entities", []):
        key = str(entity.get("key", ""))
        compact_animation = _compact_animation_manifest(entity.get("animation_files") or [])
        for record in compact_animation.get("files") or []:
            track_data = str(record.get("track_data") or "")
            if track_data:
                record["track_data"] = _rel_asset(output_dir, report_dir / track_data)
        animation_by_key[key] = compact_animation
        model_3d = str(entity.get("model_3d", "") or "")
        model_3d_path = report_dir / model_3d if model_3d else None
        rel_model_3d = _rel_asset(output_dir, model_3d_path)
        if rel_model_3d:
            model3d_by_key[key] = rel_model_3d
            try:
                embedded_model3d[rel_model_3d] = json.loads((output_dir / rel_model_3d).read_text(encoding="utf-8"))
            except Exception:
                pass

        sprite = str(entity.get("sprite_preview", "") or "")
        sprite_path = report_dir / sprite if sprite else None
        rel_sprite = _rel_asset(output_dir, sprite_path)
        if rel_sprite:
            sprite_by_key[key] = rel_sprite
        if key in sample_keys:
            sample_sprites[key] = rel_sprite

        preview = str(entity.get("mesh_preview", "") or "")
        preview_path = report_dir / preview if preview else None
        rel_preview = _rel_asset(output_dir, preview_path)
        if rel_preview:
            mesh_by_key[key] = rel_preview
        if key in sample_keys:
            sample_meshes[key] = rel_preview

    return {
        "enabled": bool(manifest.get("enabled")),
        "index": _rel_asset(output_dir, index_path),
        "manifest": _rel_asset(output_dir, manifest_path),
        "summary": manifest.get("summary", {}),
        "sample_sprites": sample_sprites,
        "sample_meshes": sample_meshes,
        "sprite_by_key": sprite_by_key,
        "mesh_by_key": mesh_by_key,
        "model3d_by_key": model3d_by_key,
        "embedded_model3d": embedded_model3d,
        "animation_by_key": animation_by_key,
        "notes": manifest.get("notes", []),
    }


def _resolve_replay_background(args, output_dir: Path, game_root: Path | None) -> str:
    if args.background:
        return str(args.background)
    if args.no_wintersturm_background or game_root is None:
        fallback = ROOT_DIR / "training_p1_map_preview.png"
        return str(fallback) if fallback.exists() else ""

    target = output_dir / "assets" / "wintersturm_p1_original_map.png"
    if not target.exists():
        render_wintersturm_background(
            game_root,
            target,
            size=max(512, int(args.wintersturm_background_size)),
            draw_objects=True,
        )
    return str(target)


def _make_html_base_image(env, args) -> np.ndarray:
    grid_h = env.map_manager.grid.height
    grid_w = env.map_manager.grid.width
    render_scale = max(1, int(getattr(args, "render_scale", 1) or 1))
    background_path = str(getattr(args, "_resolved_background", "") or "")
    if background_path and Path(background_path).exists():
        img = Image.open(background_path).convert("RGB")
        if getattr(env, "_background_crop_p1", False):
            bw, bh = img.size
            img = img.crop((bw // 2, 0, bw, bh // 2))
        target_size = (grid_w * render_scale, grid_h * render_scale)
        img = img.resize(target_size, Image.Resampling.BILINEAR)
        args._base_render_scaled = True
        return np.asarray(img, dtype=np.uint8)

    args._base_render_scaled = False
    return replay._make_base_image(env, background_path or None)


def _crop_p1_array(array: np.ndarray) -> np.ndarray:
    height, width = array.shape[:2]
    return array[: height // 2, width // 2 :]


def _make_terrain3d_payload(env, args) -> dict:
    height_path = EXTRACTED_DIR / "height_map_515.npy"
    walkable_path = EXTRACTED_DIR / "walkable_map_515.npy"
    if not height_path.exists():
        return {"enabled": False, "reason": "height_map_515.npy missing"}
    try:
        height = np.load(height_path).astype(np.float32)
        walkable = np.load(walkable_path).astype(np.float32) if walkable_path.exists() else np.ones_like(height)
    except Exception as exc:
        return {"enabled": False, "reason": f"terrain load failed: {exc}"}

    grid_h = int(env.map_manager.grid.height)
    grid_w = int(env.map_manager.grid.width)
    render_scale = max(1, int(getattr(args, "render_scale", 1) or 1))
    target_w = grid_w * render_scale
    target_h = grid_h * render_scale
    full_rows = int(height.shape[0])
    full_cols = int(height.shape[1])
    p1_row_start = 0
    p1_col_start = full_cols // 2
    p1_rows = max(1, full_rows // 2)
    p1_cols = max(1, full_cols - p1_col_start)
    x_min = -target_w / 2.0 - target_w * (p1_col_start / p1_cols)
    x_max = target_w / 2.0
    z_min = -target_h / 2.0
    z_max = target_h / 2.0 + target_h * ((full_rows - (p1_row_start + p1_rows)) / p1_rows)

    # WebGL 1 only guarantees 16-bit element indices. Keep this below 65,536
    # vertices even when OES_element_index_uint is unavailable, otherwise
    # terrain indices wrap and create visibly torn/black terrain patches.
    max_rows = min(int(height.shape[0]), 255)
    max_cols = min(int(height.shape[1]), 255)
    row_indices = np.linspace(0, height.shape[0] - 1, max_rows).round().astype(np.int32)
    col_indices = np.linspace(0, height.shape[1] - 1, max_cols).round().astype(np.int32)
    height_s = height[np.ix_(row_indices, col_indices)]
    walk_s = walkable[np.ix_(row_indices, col_indices)]
    rows, cols = height_s.shape
    h_min = float(np.min(height_s))
    h_max = float(np.max(height_s))
    h_span = max(1.0, h_max - h_min)
    vertical_scale = 185.0

    positions: list[float] = []
    normals: list[float] = []
    uvs: list[float] = []
    walk_flags: list[int] = []
    height_y = ((height_s - h_min) / h_span) * vertical_scale - 18.0
    step_world_x = (x_max - x_min) / max(1, cols - 1)
    step_world_z = (z_max - z_min) / max(1, rows - 1)
    for row in range(rows):
        z = z_min + (row / max(1, rows - 1)) * (z_max - z_min)
        for col in range(cols):
            x = x_min + (col / max(1, cols - 1)) * (x_max - x_min)
            y = float(height_y[row, col])
            positions.extend([round(x, 4), round(y, 4), round(z, 4)])
            left = float(height_y[row, max(0, col - 1)])
            right = float(height_y[row, min(cols - 1, col + 1)])
            up = float(height_y[max(0, row - 1), col])
            down = float(height_y[min(rows - 1, row + 1), col])
            tangent_x = (2.0 * step_world_x, right - left, 0.0)
            tangent_z = (0.0, down - up, 2.0 * step_world_z)
            nx = tangent_z[1] * tangent_x[2] - tangent_z[2] * tangent_x[1]
            ny = tangent_z[2] * tangent_x[0] - tangent_z[0] * tangent_x[2]
            nz = tangent_z[0] * tangent_x[1] - tangent_z[1] * tangent_x[0]
            length = max(1e-8, float(np.sqrt(nx * nx + ny * ny + nz * nz)))
            normals.extend([round(nx / length, 5), round(ny / length, 5), round(nz / length, 5)])
            uvs.extend([round(col / max(1, cols - 1), 6), round(row / max(1, rows - 1), 6)])
            walk_flags.append(1 if float(walk_s[row, col]) >= 0.5 else 0)

    indices: list[int] = []
    for row in range(rows - 1):
        for col in range(cols - 1):
            i0 = row * cols + col
            i1 = i0 + 1
            i2 = i0 + cols
            i3 = i2 + 1
            indices.extend([i0, i2, i1, i1, i2, i3])

    return {
        "enabled": True,
        "rows": int(rows),
        "cols": int(cols),
        "vertex_count": int(rows * cols),
        "source_shape": [int(height.shape[0]), int(height.shape[1])],
        "height_min": round(h_min, 3),
        "height_max": round(h_max, 3),
        "vertical_scale": vertical_scale,
        "x_min": round(x_min, 4),
        "x_max": round(x_max, 4),
        "z_min": round(z_min, 4),
        "z_max": round(z_max, 4),
        "p1_col_start": int(p1_col_start),
        "p1_row_start": int(p1_row_start),
        "p1_cols": int(p1_cols),
        "p1_rows": int(p1_rows),
        "positions": positions,
        "normals": normals,
        "uvs": uvs,
        "indices": indices,
        "walkable": walk_flags,
    }


def _make_full_terrain_texture(args, output_dir: Path, game_root: Path | None) -> str:
    target = output_dir / "terrain_full.jpg"
    size = max(1024, int(getattr(args, "wintersturm_background_size", 1536) or 1536) * 2)
    try:
        height = np.load(EXTRACTED_DIR / "height_map_515.npy")
        walkable = np.load(EXTRACTED_DIR / "walkable_map_515.npy")
        lowres = np.load(EXTRACTED_DIR / "terrain_lowres_131.npy")
        image = _render_texture_field(lowres, height, walkable, _texture_set(game_root), size)
        target.parent.mkdir(parents=True, exist_ok=True)
        image.save(target, quality=92)
        return target.name
    except Exception:
        fallback = output_dir / "terrain_base.jpg"
        return fallback.name if fallback.exists() else ""


def _frame_xy(env, args, x: float, y: float) -> tuple[int, int]:
    grid_h = env.map_manager.grid.height
    grid_w = env.map_manager.grid.width
    render_scale = max(1, int(getattr(args, "render_scale", 1) or 1))
    px, py = replay._world_to_px(env, x, y, grid_w, grid_h)
    return int(round(px * render_scale)), int(round(py * render_scale))


def _entity_snapshot(env, args) -> list[dict]:
    entities: list[dict] = []

    def frame_xy_from_position(xy) -> tuple[int, int] | None:
        pos = replay._as_xy(xy)
        if pos is None:
            return None
        return _frame_xy(env, args, pos[0], pos[1])

    def target_for_object(obj, state: str = ""):
        for attr in ("target_position", "waypoint", "final_destination"):
            xy = replay._as_xy(getattr(obj, attr, None))
            if xy is not None:
                return xy
        state_l = state.lower()
        if "working" in state_l or state_l == "working":
            route = getattr(obj, "work_route", None) or []
            route_index = int(getattr(obj, "work_route_index", 0) or 0)
            if 0 <= route_index < len(route):
                xy = replay._as_xy(route[route_index])
                if xy is not None:
                    return xy
        for attr in ("supplier_position", "workplace_position", "assigned_farm", "assigned_residence"):
            value = getattr(obj, attr, None)
            xy = replay._as_xy(getattr(value, "position", value))
            if xy is not None:
                return xy
        return None

    def animation_role(kind: str, state: str, sprite_key: str) -> str:
        state_l = state.lower()
        if "walking" in state_l:
            return "walk"
        if any(token in state_l for token in ("building", "construction", "extracting", "working", "eating", "resting", "camping")):
            return "work"
        if kind in {"building", "site"}:
            return "built"
        if sprite_key in {"serf_wood", "serf_build", "serf_mine"} and state_l:
            return "work"
        return "idle"

    def orientation_deg_from_position(xy) -> float | None:
        if not isinstance(xy, dict):
            return None
        for key in ("orientation", "Orientation", "rotation", "Rotation", "r", "R"):
            if key not in xy:
                continue
            try:
                return float(xy.get(key))
            except (TypeError, ValueError):
                return None
        return None

    def add_entity(
        entity_id: str,
        kind: str,
        sprite_key: str,
        xy,
        size: int,
        label: str,
        state: str = "",
        anchor_y: float = 0.72,
        target_xy=None,
        orientation_deg: float | None = None,
    ) -> None:
        pos = replay._as_xy(xy)
        if pos is None:
            return
        px, py = _frame_xy(env, args, pos[0], pos[1])
        record = {
            "id": entity_id,
            "kind": kind,
            "sprite_key": sprite_key,
            "x": px,
            "y": py,
            "size": int(size),
            "label": label,
            "state": state,
            "anchor_y": float(anchor_y),
            "anim_role": animation_role(kind, state, sprite_key),
            "anim_seed": sum((idx + 1) * ord(char) for idx, char in enumerate(entity_id)) % 1000,
        }
        if orientation_deg is not None:
            record["orientation_deg"] = round(float(orientation_deg), 4)
            record["angle"] = round(math.radians(float(orientation_deg)), 5)
        target_frame = frame_xy_from_position(target_xy)
        if target_frame is not None:
            tx, ty = target_frame
            record["target_x"] = tx
            record["target_y"] = ty
            dx = tx - px
            dy = ty - py
            if abs(dx) + abs(dy) > 0.5:
                record["angle"] = round(math.atan2(dx, dy), 5)
        entities.append(record)

    occupied_mine_points: list[tuple[int, int]] = []
    for key, pos in getattr(env, "building_position_map", {}).items():
        building_name = key.rsplit("_", 1)[0] if key.rsplit("_", 1)[-1].isdigit() else key
        if "mine" not in _building_mesh_key(building_name):
            continue
        point = frame_xy_from_position(pos)
        if point is not None:
            occupied_mine_points.append(point)
    for site in getattr(env, "construction_sites", []):
        building_name = str(site.get("building", ""))
        if "mine" not in _building_mesh_key(building_name):
            continue
        point = frame_xy_from_position(site.get("position"))
        if point is not None:
            occupied_mine_points.append(point)

    def covered_by_mine(px: int, py: int, radius: float = 58.0) -> bool:
        return any(math.hypot(px - ox, py - oy) <= radius for ox, oy in occupied_mine_points)

    render_scale = max(1, int(getattr(args, "render_scale", 1) or 1))
    for tree_id, grid_pos in sorted(getattr(env.map_manager.grid, "tree_positions", {}).items()):
        gx = getattr(grid_pos, "x", None)
        gy = getattr(grid_pos, "y", None)
        if gx is None or gy is None:
            continue
        px = int(round((float(gx) + 0.5) * render_scale))
        py = int(round((float(gy) + 0.5) * render_scale))
        tree_entity_id = f"tree:{tree_id}"
        entities.append(
            {
                "id": tree_entity_id,
                "kind": "tree",
                "sprite_key": "tree_fir",
                "x": px,
                "y": py,
                "size": 46,
                "label": f"Baum {tree_id}",
                "state": "standing",
                "anchor_y": 0.90,
                "anim_role": "idle",
                "anim_seed": sum((idx + 1) * ord(char) for idx, char in enumerate(tree_entity_id)) % 1000,
            }
        )

    for category, cat_data in sorted(getattr(env, "deposit_categories", {}).items()):
        for deposit_index, deposit in enumerate(cat_data.get("deposits", [])):
            if float(deposit.get("remaining", 0) or 0) <= 0:
                continue
            px, py = _frame_xy(env, args, float(deposit.get("x", 0)), float(deposit.get("y", 0)))
            if covered_by_mine(px, py):
                continue
            resource_entity_id = f"resource:{category}:{deposit_index}"
            entities.append(
                {
                    "id": resource_entity_id,
                    "kind": "resource",
                    "sprite_key": _resource_mesh_key(category),
                    "x": px,
                    "y": py,
                    "size": 48,
                    "label": f"{category} Vorkommen",
                    "state": f"remaining {int(float(deposit.get('remaining', 0) or 0))}",
                    "anchor_y": 0.78,
                    "anim_role": "idle",
                    "anim_seed": sum((idx + 1) * ord(char) for idx, char in enumerate(resource_entity_id)) % 1000,
                }
            )

    for category, cat_data in sorted(getattr(env, "shaft_categories", {}).items()):
        for shaft_index, shaft in enumerate(cat_data.get("shafts", [])):
            if float(shaft.get("remaining", 0) or 0) <= 0:
                continue
            px, py = _frame_xy(env, args, float(shaft.get("x", 0)), float(shaft.get("y", 0)))
            if covered_by_mine(px, py, radius=38.0):
                continue
            shaft_entity_id = f"shaft:{category}:{shaft_index}"
            entities.append(
                {
                    "id": shaft_entity_id,
                    "kind": "shaft",
                    "sprite_key": "generic_mine_site",
                    "x": px,
                    "y": py,
                    "size": 42,
                    "label": f"{category} Stollen",
                    "state": f"remaining {int(float(shaft.get('remaining', 0) or 0))}",
                    "anchor_y": 0.76,
                    "anim_role": "idle",
                    "anim_seed": sum((idx + 1) * ord(char) for idx, char in enumerate(shaft_entity_id)) % 1000,
                }
            )

    for key, pos in getattr(env, "building_position_map", {}).items():
        building_name = key.rsplit("_", 1)[0] if key.rsplit("_", 1)[-1].isdigit() else key
        add_entity(
            f"building:{key}",
            "building",
            _building_mesh_key(building_name),
            pos,
            _building_sprite_size(building_name),
            building_name,
            "built",
            0.62,
            orientation_deg=orientation_deg_from_position(pos),
        )

    for index, site in enumerate(getattr(env, "construction_sites", [])):
        building_name = str(site.get("building", "Baustelle"))
        site_id = site.get("site_id", index)
        progress = site.get("progress", 0)
        site_position = site.get("position")
        add_entity(
            f"site:{site_id}",
            "site",
            _building_mesh_key(building_name),
            site_position,
            _building_sprite_size(building_name, construction=True),
            f"{building_name} Baustelle {int(progress)}",
            "construction",
            0.62,
            orientation_deg=orientation_deg_from_position(site_position),
        )

    for index, worker in enumerate(getattr(env.workforce_manager, "workers", [])):
        worker_type = str(getattr(worker, "worker_type", "worker") or "worker")
        state = str(getattr(getattr(worker, "state", None), "value", getattr(worker, "state", "")) or "")
        add_entity(
            f"worker:{index}:{worker_type}",
            "worker",
            _worker_mesh_key(worker),
            getattr(worker, "position", None),
            34,
            f"{worker_type} {state}",
            state,
            0.84,
            target_for_object(worker, state),
        )

    for index, serf in enumerate(getattr(env.production_system, "serfs", [])):
        serf_id = getattr(serf, "serf_id", None)
        state = str(getattr(getattr(serf, "state", None), "value", getattr(serf, "state", "")) or "")
        add_entity(
            f"serf:{serf_id if serf_id is not None else index}",
            "serf",
            _serf_mesh_key(serf),
            getattr(serf, "position", None),
            34,
            f"Serf {serf_id if serf_id is not None else index} {state}",
            state,
            0.84,
            target_for_object(serf, state),
        )

    entities.sort(key=lambda item: (int(item["y"]), 0 if item["kind"] in {"building", "site"} else 1, item["id"]))
    return entities


def _timeline_entry(env, frame_name: str, decision: int, action_label: str, args=None) -> dict:
    first_payday = None
    last_payday = None
    next_payday = None
    payday_countdown = None
    current_time = int(getattr(env, "current_time", 0))
    if getattr(env, "_first_worker_building_time", None) is not None:
        first_payday = int(env._first_worker_building_time + replay.INCOME_CYCLE)
        if current_time >= first_payday:
            elapsed = max(0, current_time - int(env._first_worker_building_time))
            completed_cycles = max(1, elapsed // replay.INCOME_CYCLE)
            last_payday = int(env._first_worker_building_time + completed_cycles * replay.INCOME_CYCLE)
            next_payday = int(last_payday + replay.INCOME_CYCLE)
        else:
            next_payday = first_payday
        payday_countdown = max(0, int(next_payday - current_time)) if next_payday is not None else None
    return {
        "frame": frame_name,
        "decision": int(decision),
        "time": current_time,
        "action": str(action_label),
        "serfs": int(len(getattr(env.production_system, "serfs", []))),
        "workers": int(len(getattr(env.workforce_manager, "workers", []))),
        "buildings": int(len(getattr(env, "building_position_map", {}))),
        "sites": int(len(getattr(env, "construction_sites", []))),
        "taler": int(env.resources.get("Taler", 0)),
        "holz": int(env.resources.get("Holz", 0)),
        "stein": int(env.resources.get("Stein", 0)),
        "lehm": int(env.resources.get("Lehm", 0)),
        "eisen": int(env.resources.get("Eisen", 0)),
        "schwefel": int(env.resources.get("Schwefel", 0)),
        "holz_roh": int(env.resources.get("HolzRoh", 0)),
        "stein_roh": int(env.resources.get("SteinRoh", 0)),
        "lehm_roh": int(env.resources.get("LehmRoh", 0)),
        "eisen_roh": int(env.resources.get("EisenRoh", 0)),
        "schwefel_roh": int(env.resources.get("SchwefelRoh", 0)),
        "first_payday": first_payday,
        "last_payday": last_payday,
        "next_payday": next_payday,
        "payday_countdown": payday_countdown,
        "tax_level": int(getattr(env, "current_tax_level", 0)),
        "entities": _entity_snapshot(env, args) if args is not None else [],
    }


_ICON_CACHE: dict[tuple[str, int, str], Image.Image] = {}


def _asset_path_for_render(args, key: str) -> Path | None:
    manifest = getattr(args, "_game_assets", None) or {}
    rel_path = (manifest.get("assets") or {}).get(key) or ""
    if not rel_path:
        return None
    path = Path(getattr(args, "_output_dir", ".")) / rel_path
    return path if path.exists() else None


def _mesh_path_for_render(args, key: str) -> Path | None:
    manifest = getattr(args, "_game_assets", None) or {}
    original_graphics = manifest.get("original_graphics") or {}
    rel_path = (original_graphics.get("mesh_by_key") or {}).get(key) or ""
    if not rel_path:
        return None
    path = Path(getattr(args, "_output_dir", ".")) / rel_path
    return path if path.exists() else None


def _sprite_path_for_render(args, key: str) -> Path | None:
    manifest = getattr(args, "_game_assets", None) or {}
    original_graphics = manifest.get("original_graphics") or {}
    rel_path = (original_graphics.get("sprite_by_key") or {}).get(key) or ""
    if not rel_path:
        return None
    path = Path(getattr(args, "_output_dir", ".")) / rel_path
    return path if path.exists() else None


def _load_render_icon(args, key: str, size: int, *, mesh: bool = False, sprite: bool = False) -> Image.Image | None:
    if sprite:
        path = _sprite_path_for_render(args, key)
    elif mesh:
        path = _mesh_path_for_render(args, key)
    else:
        path = _asset_path_for_render(args, key)
    if path is None:
        return None
    cache_key = (str(path), int(size), "sprite" if sprite else "mesh" if mesh else "asset")
    cached = _ICON_CACHE.get(cache_key)
    if cached is not None:
        return cached
    try:
        icon = Image.open(path).convert("RGBA")
    except Exception:
        return None
    w, h = icon.size
    if h > w and w > 0:
        icon = icon.crop((0, 0, w, min(h, w)))
    elif w > h and h > 0:
        left = max(0, (w - h) // 2)
        icon = icon.crop((left, 0, left + h, h))
    icon.thumbnail((size, size), Image.Resampling.LANCZOS)
    _ICON_CACHE[cache_key] = icon
    return icon


def _building_mesh_key(building_name: str) -> str:
    normalized = replay.get_base_building_name(building_name).lower()
    if "hauptquartier" in normalized or "headquarter" in normalized:
        return "headquarters_1"
    if "hochschule" in normalized or "university" in normalized:
        return "university_1"
    if "kloster" in normalized or "monastery" in normalized:
        return "monastery_1"
    if "dorfzentrum" in normalized or "village" in normalized:
        return "village_center_1"
    if "wohnhaus" in normalized or "residence" in normalized:
        return "residence_1"
    if "bauernhof" in normalized or "farm" in normalized:
        return "farm_1"
    if "lehm" in normalized:
        return "clay_mine_1"
    if "eisen" in normalized:
        return "iron_mine_1"
    if "stein" in normalized:
        return "stone_mine_1"
    if "schwefel" in normalized or "sulfur" in normalized:
        return "sulfur_mine_1"
    if "mine" in normalized or "grube" in normalized:
        return "generic_mine_site"
    return "headquarters_1"


def _worker_mesh_key(worker) -> str:
    worker_type = str(getattr(worker, "worker_type", "") or "").lower()
    if "miner" in worker_type:
        return "worker_miner"
    if "sawmill" in worker_type:
        return "worker_sawmill"
    if "stone" in worker_type:
        return "worker_stonecutter"
    if "brick" in worker_type:
        return "worker_brickmaker"
    if "farmer" in worker_type:
        return "worker_farmer"
    if "scholar" in worker_type:
        return "worker_scholar"
    if "priest" in worker_type:
        return "worker_priest"
    return "worker_sawmill"


def _serf_mesh_key(serf) -> str:
    state = str(getattr(getattr(serf, "state", None), "value", getattr(serf, "state", ""))).lower()
    target_resource = getattr(serf, "target_resource", "")
    resource = str(
        getattr(serf, "assigned_resource", "")
        or getattr(serf, "resource", "")
        or getattr(target_resource, "value", target_resource)
        or getattr(serf, "work_location", "")
        or ""
    ).lower()
    if "build" in state:
        return "serf_build"
    if "wood" in resource or "wood" in state or "holz" in resource:
        return "serf_wood"
    if any(token in resource for token in ("stone", "clay", "iron", "sulfur", "stein", "lehm", "eisen", "schwefel")):
        return "serf_mine"
    return "serf_idle"


def _resource_mesh_key(category: str) -> str:
    normalized = str(category or "").lower()
    if "eisen" in normalized or "iron" in normalized:
        return "iron_resource"
    if "stein" in normalized or "stone" in normalized:
        return "stone_resource"
    if "lehm" in normalized or "clay" in normalized:
        return "clay_resource"
    if "schwefel" in normalized or "sulfur" in normalized:
        return "sulfur_resource"
    return "stone_resource"


def _building_icon_key(building_name: str) -> str:
    normalized = replay.get_base_building_name(building_name).lower()
    if "hauptquartier" in normalized or "headquarter" in normalized:
        return "headquarter"
    if "hochschule" in normalized or "university" in normalized:
        return "university"
    if "kloster" in normalized or "monastery" in normalized:
        return "monastery"
    if "dorfzentrum" in normalized or "village" in normalized:
        return "village"
    if "wohnhaus" in normalized or "residence" in normalized:
        return "residence"
    if "bauernhof" in normalized or "farm" in normalized:
        return "farm"
    if "mine" in normalized or "grube" in normalized:
        return "mine"
    return "site"


def _building_sprite_size(building_name: str, *, construction: bool = False) -> int:
    key = _building_mesh_key(building_name)
    if key == "headquarters_1":
        size = 112
    elif key in {"university_1", "monastery_1", "village_center_1"}:
        size = 92
    elif key in {"residence_1", "farm_1"}:
        size = 72
    elif "mine" in key:
        size = 68
    else:
        size = 78
    return int(size * 0.82) if construction else size


def _paste_centered_icon(canvas: Image.Image, icon: Image.Image | None, x: int, y: int) -> None:
    if icon is None:
        return
    canvas.alpha_composite(icon, (int(x - icon.width / 2), int(y - icon.height / 2)))


def _overlay_game_icons(env, frame: np.ndarray, args) -> np.ndarray:
    manifest = getattr(args, "_game_assets", None) or {}
    mode = str(getattr(args, "entity_render_mode", "sprite") or "sprite")
    if not manifest.get("enabled") or getattr(args, "no_game_icon_overlay", False) or mode == "none":
        return frame
    if getattr(args, "viewport", "full") != "full":
        return frame
    original_graphics = manifest.get("original_graphics") or {}
    use_sprite = mode == "sprite" and bool(original_graphics.get("sprite_by_key"))
    use_mesh = mode == "mesh" and bool(original_graphics.get("mesh_by_key"))

    grid_h = env.map_manager.grid.height
    grid_w = env.map_manager.grid.width
    render_scale = max(1, int(getattr(args, "render_scale", 1) or 1))
    canvas = Image.fromarray(frame, mode="RGB").convert("RGBA")

    def world_to_frame(x: float, y: float) -> tuple[int, int]:
        px, py = replay._world_to_px(env, x, y, grid_w, grid_h)
        return int(px * render_scale), int(py * render_scale)

    # Building icons first, then moving units above them.
    for key, pos in getattr(env, "building_position_map", {}).items():
        xy = replay._as_xy(pos)
        if xy is None:
            continue
        building_name = key.rsplit("_", 1)[0] if key.rsplit("_", 1)[-1].isdigit() else key
        x, y = world_to_frame(xy[0], xy[1])
        graphics_key = _building_mesh_key(building_name)
        if use_sprite:
            icon = (
                _load_render_icon(args, graphics_key, _building_sprite_size(building_name), sprite=True)
                or _load_render_icon(args, graphics_key, _building_sprite_size(building_name), mesh=True)
            )
        elif use_mesh:
            icon = _load_render_icon(args, graphics_key, 58, mesh=True)
        else:
            icon = _load_render_icon(args, _building_icon_key(building_name), 34)
        _paste_centered_icon(canvas, icon, x, y)

    for site in getattr(env, "construction_sites", []):
        xy = replay._as_xy(site.get("position"))
        if xy is None:
            continue
        x, y = world_to_frame(xy[0], xy[1])
        building_name = str(site.get("building", ""))
        graphics_key = _building_mesh_key(building_name)
        if use_sprite:
            icon = (
                _load_render_icon(args, graphics_key, _building_sprite_size(building_name, construction=True), sprite=True)
                or _load_render_icon(args, graphics_key, _building_sprite_size(building_name, construction=True), mesh=True)
            )
        elif use_mesh:
            icon = _load_render_icon(args, graphics_key, 48, mesh=True)
        else:
            icon = _load_render_icon(args, "site", 30)
        _paste_centered_icon(canvas, icon, x, y)

    for worker in getattr(env.workforce_manager, "workers", []):
        xy = replay._as_xy(getattr(worker, "position", None))
        if xy is None:
            continue
        x, y = world_to_frame(xy[0], xy[1])
        graphics_key = _worker_mesh_key(worker)
        if use_sprite:
            worker_icon = (
                _load_render_icon(args, graphics_key, 34, sprite=True)
                or _load_render_icon(args, graphics_key, 28, mesh=True)
                or _load_render_icon(args, "worker", 18)
            )
        elif use_mesh:
            worker_icon = _load_render_icon(args, graphics_key, 24, mesh=True)
        else:
            worker_icon = _load_render_icon(args, "worker", 18)
        _paste_centered_icon(canvas, worker_icon, x, y)

    for serf in getattr(env.production_system, "serfs", []):
        xy = replay._as_xy(getattr(serf, "position", None))
        if xy is None:
            continue
        x, y = world_to_frame(xy[0], xy[1])
        graphics_key = _serf_mesh_key(serf)
        if use_sprite:
            serf_icon = (
                _load_render_icon(args, graphics_key, 34, sprite=True)
                or _load_render_icon(args, graphics_key, 28, mesh=True)
                or _load_render_icon(args, "serf", 20)
            )
        elif use_mesh:
            serf_icon = _load_render_icon(args, graphics_key, 24, mesh=True)
        else:
            serf_icon = _load_render_icon(args, "serf", 20)
        _paste_centered_icon(canvas, serf_icon, x, y)

    return np.asarray(canvas.convert("RGB"), dtype=np.uint8)


def _render_frame(env, base, decision: int, total: int, action_label: str, args) -> np.ndarray:
    frame = replay._draw_frame(
        env,
        base,
        decision,
        total,
        draw_paths=(not args.no_paths) and bool(args.labels),
        max_paths=1200,
        action_label=action_label,
        label_entities=bool(args.labels),
        show_worker_states=True,
        show_worker_targets=True,
        show_refiner_trips=True,
        max_refiner_trips=120,
        show_hud=bool(args.hud),
        show_debug_markers=bool(args.labels or args.hud),
    )
    frame = replay._apply_viewport(frame, args.viewport)
    if not bool(getattr(args, "_base_render_scaled", False)):
        frame = replay._scale_frame(frame, args.render_scale)
    if bool(getattr(args, "bake_entity_overlay", False)):
        frame = _overlay_game_icons(env, frame, args)
    return frame


def _write_html(output_dir: Path, timeline: list[dict], width: int, height: int, game_assets: dict | None = None) -> None:
    timeline_json = json.dumps(timeline, ensure_ascii=False).replace("</", "<\\/")
    game_assets = game_assets or {"enabled": False, "assets": {}, "payday_frames": []}
    game_assets_json = json.dumps(game_assets, ensure_ascii=False).replace("</", "<\\/")
    assets = game_assets.get("assets") or {}
    original_graphics = game_assets.get("original_graphics") or {}
    graphics_summary_data = original_graphics.get("summary") or {}
    sample_sprites = original_graphics.get("sample_sprites") or {}
    sample_meshes = original_graphics.get("sample_meshes") or {}
    if original_graphics.get("enabled"):
        graphics_report_class = ""
        graphics_report_link = original_graphics.get("index") or "#"
        graphics_report_summary = (
            f"{int(graphics_summary_data.get('with_model', 0))} Modelle, "
            f"{int(graphics_summary_data.get('with_texture', 0))} Texturen, "
            f"{int(graphics_summary_data.get('with_sprite_preview', 0))} Sprites, "
            f"{int(graphics_summary_data.get('with_animation', 0))} Animationsgruppen"
        )
    else:
        graphics_report_class = "hidden"
        graphics_report_link = "#"
        graphics_report_summary = "Originalgrafik-Report nicht erzeugt"
    title = "Siedler Expert Opening Replay"
    html_text = """<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__TITLE__</title>
  <style>
    :root {
      --wood: #5b3d24;
      --wood-dark: #2f2117;
      --wood-line: #8a6642;
      --stone: #283039;
      --stone-light: #40505d;
      --gold: #d7b663;
      --green: #77b06a;
      --red: #c86955;
    }
    html, body {
      margin: 0;
      height: 100%;
      background: #080b0c;
      color: #f5ead2;
      font-family: Georgia, "Times New Roman", serif;
    }
    body {
      display: grid;
      grid-template-rows: auto auto minmax(0, 1fr);
      min-width: 0;
      overflow: hidden;
    }
    .resourcebar {
      grid-row: 1;
      display: grid;
      grid-template-columns: minmax(190px, 250px) 1fr minmax(230px, 310px);
      gap: 10px;
      align-items: stretch;
      padding: 8px 10px 6px;
      background:
        linear-gradient(180deg, rgba(255,255,255,.08), rgba(0,0,0,.16)),
        linear-gradient(90deg, #1e1711, #3c2819 18%, #241910 100%);
      border-bottom: 2px solid #0f0b08;
      box-shadow: 0 2px 0 rgba(255,255,255,.08) inset, 0 3px 14px rgba(0,0,0,.45);
    }
    body.has-game-assets .resourcebar {
      background-image: linear-gradient(180deg, rgba(24,15,7,.28), rgba(24,15,7,.08)), url("__ASSET_BG_TOP__");
      background-size: 100% 100%, 100% 100%;
      background-position: center;
    }
    .crest, .payday, .resource-chip, .toolbutton, select {
      border: 1px solid rgba(238, 210, 148, .45);
      box-shadow: 0 1px 0 rgba(255,255,255,.12) inset, 0 2px 7px rgba(0,0,0,.28);
    }
    .crest {
      display: flex;
      flex-direction: column;
      justify-content: center;
      min-height: 48px;
      padding: 6px 12px;
      border-radius: 4px;
      background: linear-gradient(180deg, #6a4427, #2b1b11);
      color: #ffe2a2;
      text-transform: uppercase;
      letter-spacing: .04em;
      font-weight: 700;
    }
    .crest small {
      color: #d9c89d;
      font: 600 11px/1.2 system-ui, sans-serif;
      letter-spacing: 0;
      text-transform: none;
    }
    .resources {
      display: grid;
      grid-template-columns: repeat(6, minmax(86px, 1fr));
      gap: 6px;
      align-content: center;
    }
    .resource-chip {
      display: grid;
      grid-template-columns: 28px 1fr;
      gap: 6px;
      align-items: center;
      min-height: 48px;
      padding: 4px 7px;
      border-radius: 4px;
      background: linear-gradient(180deg, rgba(103,75,44,.96), rgba(40,29,19,.97));
      color: #ffe8bb;
      min-width: 0;
    }
    .res-icon {
      display: grid;
      place-items: center;
      width: 26px;
      height: 26px;
      border-radius: 50%;
      background: radial-gradient(circle at 32% 28%, rgba(255,255,255,.42), rgba(255,255,255,0) 34%), #8d683d;
      color: #1e160f;
      font: 800 14px/1 system-ui, sans-serif;
    }
    body.has-game-assets .res-icon {
      background-color: transparent;
      background-image: var(--asset-icon);
      background-size: contain;
      background-position: center;
      background-repeat: no-repeat;
      border-radius: 0;
      color: transparent;
      box-shadow: none;
    }
    .resource-chip .name {
      color: #cfbf98;
      font: 700 11px/1.1 system-ui, sans-serif;
    }
    .resource-chip .value {
      color: #fff4cd;
      font: 800 17px/1.05 system-ui, sans-serif;
      white-space: nowrap;
    }
    .resource-chip .raw {
      color: #bba97e;
      font: 700 10px/1 system-ui, sans-serif;
      white-space: nowrap;
    }
    .payday {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
      align-items: center;
      min-height: 48px;
      padding: 5px 10px;
      border-radius: 4px;
      background: linear-gradient(180deg, #3d4650, #1b2027);
      color: #e9f1f3;
    }
    body.has-game-assets .payday {
      background-image: linear-gradient(180deg, rgba(13,20,25,.72), rgba(13,20,25,.90)), url("__ASSET_TOOLTIP__");
      background-size: 100% 100%, 100% 100%;
    }
    .payday-icon {
      width: 44px;
      height: 44px;
      object-fit: contain;
      margin-right: 6px;
      filter: drop-shadow(0 2px 3px rgba(0,0,0,.55));
    }
    .payday-info {
      display: flex;
      align-items: center;
      min-width: 0;
    }
    .payday .label {
      color: #b6c4ca;
      font: 700 11px/1.1 system-ui, sans-serif;
      text-transform: uppercase;
      letter-spacing: .03em;
    }
    .payday .main {
      color: #fff0bc;
      font: 800 18px/1.1 system-ui, sans-serif;
    }
    .payday .sub {
      color: #cbd4d8;
      font: 600 11px/1.15 system-ui, sans-serif;
    }
    .tax-pill {
      min-width: 64px;
      padding: 8px;
      text-align: center;
      border-radius: 4px;
      background: rgba(0,0,0,.25);
      color: #ffd989;
      font: 800 18px/1 system-ui, sans-serif;
    }
    .controlbar {
      grid-row: 2;
      display: grid;
      grid-template-columns: auto auto auto minmax(260px, 1fr) auto auto auto auto;
      gap: 8px;
      align-items: center;
      padding: 6px 10px;
      background: linear-gradient(180deg, #252d33, #11161a);
      border-bottom: 1px solid #34404a;
      font-family: system-ui, Segoe UI, sans-serif;
    }
    body.has-game-assets .controlbar {
      background-image: linear-gradient(180deg, rgba(0,0,0,.10), rgba(0,0,0,.38)), url("__ASSET_BG_BOTTOM__");
      background-size: 100% 100%, 100% auto;
      background-position: center top;
    }
    .toolbutton, select {
      min-height: 32px;
      border-radius: 4px;
      background: linear-gradient(180deg, #59636d, #26313a);
      color: #fff3d2;
      font: 700 13px/1 system-ui, sans-serif;
      padding: 0 11px;
    }
    .toolbutton:hover, select:hover {
      filter: brightness(1.13);
    }
    .toolbutton.active {
      background: linear-gradient(180deg, #8f7141, #4b301b);
      color: #fff0b5;
    }
    .keycap {
      padding: 5px 8px;
      border-radius: 4px;
      background: #151b20;
      border: 1px solid #4c5964;
      color: #c8d2d8;
      font: 700 12px/1 system-ui, sans-serif;
    }
    input[type="range"] {
      width: 100%;
      accent-color: var(--gold);
    }
    .stage {
      grid-row: 3;
      position: relative;
      min-height: 0;
      overflow: hidden;
      cursor: grab;
      background:
        radial-gradient(circle at 25% 20%, rgba(95, 120, 84, .20), transparent 26%),
        radial-gradient(circle at 72% 58%, rgba(83, 69, 40, .20), transparent 28%),
        #080b0c;
    }
    .stage.dragging {
      cursor: grabbing;
    }
    .stage.mode3d.hovering-entity {
      cursor: pointer;
    }
    .stage.selecting {
      cursor: crosshair;
    }
    .selection-rect {
      position: absolute;
      display: none;
      pointer-events: none;
      border: 1px solid rgba(255, 231, 150, .95);
      background: rgba(255, 210, 90, .12);
      box-shadow: inset 0 0 0 1px rgba(28, 22, 8, .72), 0 0 9px rgba(255, 224, 128, .38);
      z-index: 8;
    }
    .stage.selecting .selection-rect {
      display: block;
    }
    .path-overlay {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      overflow: visible;
      z-index: 2;
    }
    .path-overlay .movement-trail {
      fill: none;
      stroke: rgba(255, 232, 132, 1);
      stroke-width: 3.1;
      stroke-linecap: round;
      stroke-linejoin: round;
      filter: drop-shadow(0 1px 1px rgba(0,0,0,.78));
    }
    .path-overlay .movement-trail.worker {
      stroke: rgba(132, 221, 255, 1);
    }
    .path-overlay .movement-trail-shadow {
      fill: none;
      stroke: rgba(10, 22, 30, .93);
      stroke-width: 6.4;
      stroke-linecap: round;
      stroke-linejoin: round;
      filter: drop-shadow(0 1px 1px rgba(0,0,0,.86));
    }
    .path-overlay .movement-target-line {
      fill: none;
      stroke: rgba(255, 246, 195, .72);
      stroke-width: 1.6;
      stroke-dasharray: 5 4;
      filter: drop-shadow(0 1px 1px rgba(0,0,0,.74));
    }
    .path-overlay .movement-target {
      fill: rgba(255, 231, 134, .94);
      stroke: rgba(48, 36, 13, .98);
      stroke-width: 1.4;
    }
    #world {
      position: absolute;
      left: 0;
      top: 0;
      width: __WIDTH__px;
      height: __HEIGHT__px;
      transform-origin: 0 0;
      will-change: transform;
      z-index: 0;
    }
    #map {
      position: absolute;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      image-rendering: auto;
      user-select: none;
      -webkit-user-drag: none;
      filter: saturate(1.05) contrast(1.03);
    }
    #webglScene {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      display: none;
      background: #080b0c;
      z-index: 0;
    }
    .stage.mode3d #world {
      display: none;
    }
    .stage.mode3d #webglScene {
      display: block;
    }
    .entity-layer {
      position: absolute;
      inset: 0;
      pointer-events: none;
      overflow: visible;
      z-index: 1;
    }
    .entity-sprite {
      --anchor-y: .78;
      --flip: 1;
      position: absolute;
      object-fit: contain;
      image-rendering: auto;
      transform: translate(-50%, calc(-1 * var(--anchor-y) * 100%)) scaleX(var(--flip));
      transform-origin: 50% 86%;
      filter: drop-shadow(0 4px 4px rgba(0,0,0,.52));
      user-select: none;
      -webkit-user-drag: none;
      pointer-events: auto;
      cursor: pointer;
    }
    .entity-sprite.selected {
      filter:
        drop-shadow(0 0 5px rgba(255,230,120,.95))
        drop-shadow(0 5px 5px rgba(0,0,0,.58));
    }
    .entity-sprite.building,
    .entity-sprite.site {
      filter: drop-shadow(0 6px 6px rgba(0,0,0,.48));
    }
    .entity-sprite.site {
      opacity: .88;
      mix-blend-mode: normal;
    }
    .entity-sprite.walking_to_resource,
    .entity-sprite.walking_to_build,
    .entity-sprite.walking_to_work,
    .entity-sprite.walking_to_supplier,
    .entity-sprite.walking_from_supplier_to_work,
    .entity-sprite.walking_to_farm,
    .entity-sprite.walking_to_residence,
    .entity-sprite.walking_to_camp {
      animation: entityWalk .54s steps(2, end) infinite;
    }
    .entity-sprite.serf.building,
    .entity-sprite.extracting,
    .entity-sprite.working,
    .entity-sprite.construction {
      animation: entityWork 1.1s ease-in-out infinite;
    }
    .sidehud {
      position: absolute;
      right: 12px;
      top: 12px;
      width: min(360px, calc(100vw - 32px));
      display: grid;
      gap: 10px;
      pointer-events: none;
      font-family: system-ui, Segoe UI, sans-serif;
    }
    .sidehud.compact {
      top: 76px;
      width: min(292px, calc(100vw - 32px));
      opacity: .94;
    }
    .panel, .minimap {
      pointer-events: auto;
      border-radius: 4px;
      border: 1px solid rgba(238, 210, 148, .42);
      background: linear-gradient(180deg, rgba(54,41,26,.92), rgba(20,18,15,.92));
      box-shadow: 0 0 0 1px rgba(0,0,0,.35), 0 8px 24px rgba(0,0,0,.35);
      color: #f5ead2;
    }
    body.has-game-assets .panel,
    body.has-game-assets .minimap {
      background-image: linear-gradient(180deg, rgba(31,24,16,.60), rgba(15,12,9,.86)), url("__ASSET_WINDOW__");
      background-size: 100% 100%, 100% 100%;
      border-color: rgba(255, 224, 143, .55);
    }
    .panel {
      padding: 10px 12px;
    }
    .panel .big {
      font-size: 18px;
      font-weight: 800;
      color: #fff1bd;
      margin-bottom: 4px;
    }
    .actionline {
      color: #f4f7e8;
      font-size: 13px;
      line-height: 1.35;
      overflow-wrap: anywhere;
    }
    .statgrid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      margin-top: 8px;
    }
    .stat {
      padding: 6px;
      border-radius: 3px;
      background: rgba(0,0,0,.24);
      text-align: center;
    }
    .stat b {
      display: block;
      color: #fff0bc;
      font-size: 15px;
    }
    .stat span {
      color: #bcae8c;
      font-size: 10px;
      text-transform: uppercase;
    }
    .minimap {
      padding: 8px;
    }
    .minimap-title {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
      color: #dbc894;
      font: 700 12px/1 system-ui, sans-serif;
      text-transform: uppercase;
      letter-spacing: .04em;
    }
    .minimap-inner {
      position: relative;
      width: 100%;
      aspect-ratio: __WIDTH__ / __HEIGHT__;
      max-height: 210px;
      overflow: hidden;
      background: #111;
      border: 1px solid rgba(255,255,255,.18);
      cursor: crosshair;
    }
    body.has-game-assets .minimap-inner {
      background-image: url("__ASSET_MINIMAP_BG__");
      background-size: 100% 100%;
      padding: 7px;
      box-sizing: border-box;
    }
    #mini {
      display: block;
      width: 100%;
      height: 100%;
      object-fit: contain;
      image-rendering: pixelated;
    }
    #miniMarkers {
      position: absolute;
      pointer-events: none;
      overflow: visible;
      z-index: 2;
    }
    #miniMarkers circle {
      stroke: rgba(13, 12, 10, .95);
      stroke-width: 1.1;
      paint-order: stroke;
    }
    #miniMarkers .mini-building { fill: #f7d77d; }
    #miniMarkers .mini-site { fill: #ff9d42; }
    #miniMarkers .mini-serf { fill: #7ccfff; }
    #miniMarkers .mini-worker { fill: #f0f4ff; }
    #miniMarkers .mini-resource,
    #miniMarkers .mini-shaft { fill: #79d85d; }
    #miniMarkers .mini-selected {
      fill: #fff3a2;
      stroke: #2b2109;
      stroke-width: 1.8;
    }
    #miniView {
      position: absolute;
      border: 2px solid #ffe47c;
      box-shadow: 0 0 0 1px #111, 0 0 9px rgba(255,224,110,.75);
      pointer-events: none;
      z-index: 3;
    }
    .playing-dot {
      display: inline-block;
      width: 9px;
      height: 9px;
      margin-right: 6px;
      border-radius: 50%;
      background: var(--red);
      box-shadow: 0 0 8px rgba(200,105,85,.5);
      vertical-align: middle;
    }
    .asset-strip {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      margin-top: 8px;
    }
    .asset-badge {
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 30px;
      border-radius: 3px;
      background: rgba(0,0,0,.24);
    }
    .asset-badge img {
      width: 24px;
      height: 24px;
      object-fit: contain;
      filter: drop-shadow(0 1px 2px rgba(0,0,0,.55));
    }
    .graphics-report {
      margin-top: 10px;
      padding: 8px;
      border-radius: 4px;
      background: rgba(0,0,0,.23);
      border: 1px solid rgba(238, 210, 148, .24);
    }
    .graphics-report.hidden {
      display: none !important;
    }
    .graphics-report a {
      color: #ffe39d;
      font: 700 12px/1.2 system-ui, sans-serif;
      text-decoration: none;
      text-transform: uppercase;
      letter-spacing: .04em;
    }
    .graphics-report p {
      margin: 4px 0 7px;
      color: #d8c59c;
      font: 12px/1.35 system-ui, sans-serif;
    }
    .mesh-strip {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 5px;
    }
    .mesh-strip img {
      width: 100%;
      aspect-ratio: 1;
      object-fit: contain;
      background: #0d1010;
      border: 1px solid rgba(255,255,255,.13);
      border-radius: 3px;
    }
    .bottomhud {
      position: absolute;
      left: 10px;
      right: 10px;
      bottom: 8px;
      display: grid;
      grid-template-columns: minmax(230px, 300px) minmax(380px, 1fr) minmax(230px, 320px);
      gap: 10px;
      align-items: end;
      pointer-events: none;
      font-family: system-ui, Segoe UI, sans-serif;
    }
    .selection-panel,
    .command-panel,
    .replay-panel {
      pointer-events: auto;
      min-height: 112px;
      border: 1px solid rgba(238, 210, 148, .44);
      border-radius: 4px;
      background: linear-gradient(180deg, rgba(49,37,24,.94), rgba(15,13,10,.96));
      box-shadow: 0 0 0 1px rgba(0,0,0,.45), 0 8px 22px rgba(0,0,0,.48);
      color: #f7e8c6;
    }
    body.has-game-assets .selection-panel,
    body.has-game-assets .command-panel,
    body.has-game-assets .replay-panel {
      background-image: linear-gradient(180deg, rgba(24,17,9,.45), rgba(7,6,5,.78)), url("__ASSET_BG_BOTTOM__");
      background-size: 100% 100%, 100% auto;
      background-position: center top;
    }
    .selection-panel {
      display: grid;
      grid-template-columns: 76px 1fr;
      gap: 10px;
      padding: 10px;
    }
    .portrait {
      width: 68px;
      height: 68px;
      display: grid;
      place-items: center;
      border: 1px solid rgba(255,226,147,.42);
      border-radius: 4px;
      background: rgba(0,0,0,.32);
      overflow: hidden;
    }
    .portrait img {
      max-width: 66px;
      max-height: 66px;
      object-fit: contain;
      filter: drop-shadow(0 3px 3px rgba(0,0,0,.55));
    }
    .selection-title {
      color: #fff1bd;
      font: 800 15px/1.18 system-ui, sans-serif;
      min-height: 18px;
      overflow-wrap: anywhere;
    }
    .selection-meta {
      color: #d7c49a;
      font: 700 11px/1.35 system-ui, sans-serif;
      margin-top: 4px;
    }
    .selection-actions {
      display: flex;
      gap: 6px;
      margin-top: 9px;
      flex-wrap: wrap;
    }
    .command-panel {
      padding: 9px 11px;
      display: grid;
      grid-template-columns: auto 1fr;
      gap: 10px;
      align-items: start;
    }
    .command-tabs {
      display: grid;
      grid-auto-flow: row;
      gap: 6px;
    }
    .tab-icon {
      width: 42px;
      height: 34px;
      border: 1px solid rgba(255,226,147,.32);
      border-radius: 3px;
      background: rgba(0,0,0,.32);
      display: grid;
      place-items: center;
    }
    .tab-icon img {
      max-width: 38px;
      max-height: 30px;
      object-fit: contain;
    }
    .command-grid {
      display: grid;
      grid-template-columns: repeat(9, minmax(34px, 42px));
      gap: 6px;
      align-content: start;
    }
    .command-slot {
      width: 40px;
      height: 40px;
      border: 1px solid rgba(255,226,147,.34);
      border-radius: 3px;
      background: linear-gradient(180deg, rgba(93,67,39,.78), rgba(22,17,12,.92));
      display: grid;
      place-items: center;
      color: #ffe2a0;
      font: 800 11px/1 system-ui, sans-serif;
      cursor: pointer;
    }
    .command-slot img {
      max-width: 30px;
      max-height: 30px;
      object-fit: contain;
      filter: drop-shadow(0 2px 2px rgba(0,0,0,.55));
    }
    .command-slot img.flip-x {
      transform: scaleX(-1);
    }
    .command-slot img.rotate-left {
      transform: rotate(90deg);
    }
    .command-slot img.rotate-right {
      transform: rotate(-90deg);
    }
    .command-slot img.small-icon {
      max-width: 22px;
      max-height: 22px;
    }
    .command-slot:disabled {
      opacity: .38;
      cursor: default;
    }
    .command-slot.active {
      border-color: rgba(255,232,132,.82);
      background: linear-gradient(180deg, rgba(128,92,47,.95), rgba(54,35,17,.98));
      box-shadow: inset 0 0 0 1px rgba(255,232,132,.24), 0 0 12px rgba(255,216,105,.22);
    }
    .replay-panel {
      padding: 10px;
      display: grid;
      gap: 8px;
    }
    .replay-line {
      color: #ffe8ad;
      font: 800 13px/1.25 system-ui, sans-serif;
      overflow-wrap: anywhere;
    }
    .replay-buttons {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
    }
    .camera-hint {
      color: #bfae87;
      font: 700 10px/1.25 system-ui, sans-serif;
    }
    .debug-only {
      display: none !important;
    }
    body.debug-mode .debug-only {
      display: block !important;
    }
    body.debug-mode .asset-strip.debug-only {
      display: grid !important;
    }
    body.debug-mode .controlbar.debug-only {
      display: grid !important;
    }
    .screen-message {
      position: absolute;
      left: 50%;
      top: 86px;
      transform: translateX(-50%);
      min-width: 310px;
      max-width: min(620px, calc(100vw - 36px));
      display: none;
      grid-template-columns: 42px 1fr;
      gap: 9px;
      align-items: center;
      padding: 8px 12px;
      border: 1px solid rgba(255,229,146,.42);
      border-radius: 4px;
      background: linear-gradient(180deg, rgba(43,33,20,.88), rgba(14,12,9,.92));
      color: #fff1c2;
      box-shadow: 0 8px 24px rgba(0,0,0,.42);
      font: 800 13px/1.25 system-ui, sans-serif;
      pointer-events: none;
      opacity: .94;
    }
    .screen-message.visible {
      display: grid;
    }
    body.has-game-assets .screen-message {
      background-image: linear-gradient(180deg, rgba(34,25,15,.48), rgba(8,7,5,.78)), url("__ASSET_TOOLTIP__");
      background-size: 100% 100%, 100% 100%;
    }
    .screen-message img {
      width: 36px;
      height: 36px;
      object-fit: contain;
    }
    .stage.playing .playing-dot {
      background: var(--green);
      animation: pulse 1s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: .65; transform: scale(.92); }
      50% { opacity: 1; transform: scale(1.15); }
    }
    @keyframes entityWalk {
      0%, 100% { margin-top: 0; }
      50% { margin-top: -2px; }
    }
    @keyframes entityWork {
      0%, 100% { filter: drop-shadow(0 4px 4px rgba(0,0,0,.52)) brightness(1); }
      50% { filter: drop-shadow(0 4px 4px rgba(0,0,0,.52)) brightness(1.08); }
    }
  </style>
</head>
<body class="__GAME_ASSET_CLASS__">
  <div class="resourcebar">
    <div class="crest">
      Wintersturm
      <small>Expert Opening Full-Sim</small>
    </div>
    <div class="resources">
      <div class="resource-chip"><div class="res-icon" style="--asset-icon:url('__ICON_GOLD__')">T</div><div><div class="name">Taler</div><div id="resTaler" class="value">0</div><div class="raw">Kasse</div></div></div>
      <div class="resource-chip"><div class="res-icon" style="--asset-icon:url('__ICON_WOOD__')">H</div><div><div class="name">Holz</div><div id="resHolz" class="value">0</div><div id="rawHolz" class="raw">Roh 0</div></div></div>
      <div class="resource-chip"><div class="res-icon" style="--asset-icon:url('__ICON_STONE__')">S</div><div><div class="name">Stein</div><div id="resStein" class="value">0</div><div id="rawStein" class="raw">Roh 0</div></div></div>
      <div class="resource-chip"><div class="res-icon" style="--asset-icon:url('__ICON_MUD__')">L</div><div><div class="name">Lehm</div><div id="resLehm" class="value">0</div><div id="rawLehm" class="raw">Roh 0</div></div></div>
      <div class="resource-chip"><div class="res-icon" style="--asset-icon:url('__ICON_IRON__')">E</div><div><div class="name">Eisen</div><div id="resEisen" class="value">0</div><div id="rawEisen" class="raw">Roh 0</div></div></div>
      <div class="resource-chip"><div class="res-icon" style="--asset-icon:url('__ICON_SULFUR__')">G</div><div><div class="name">Schwefel</div><div id="resSchwefel" class="value">0</div><div id="rawSchwefel" class="raw">Roh 0</div></div></div>
    </div>
    <div class="payday">
      <div class="payday-info">
        <img id="paydayIcon" class="payday-icon" src="__PAYDAY_ICON__" alt="">
        <div>
          <div class="label">Zahltag</div>
          <div id="paydayMain" class="main">nicht gesetzt</div>
          <div id="paydaySub" class="sub">erster Worker fehlt</div>
        </div>
      </div>
      <div>
        <div class="label">Steuer</div>
        <div id="taxLevel" class="tax-pill">0</div>
      </div>
    </div>
  </div>
  <div class="controlbar debug-only">
    <button class="toolbutton" id="prev">Zurueck</button>
    <button class="toolbutton" id="play">Play</button>
    <button class="toolbutton" id="next">Weiter</button>
    <input id="slider" type="range" min="0" max="__MAX_INDEX__" value="0">
    <select id="speed">
      <option value="1500">0.66x</option>
      <option value="1000" selected>1x Echtzeit</option>
      <option value="500">2x</option>
      <option value="250">4x</option>
    </select>
    <button class="toolbutton" id="fullscreen">Vollbild</button>
    <button class="toolbutton" id="mode3d">3D</button>
    <span class="keycap">Space</span>
  </div>
  <div id="stage" class="stage">
    <div id="world">
      <img id="map" src="" width="__WIDTH__" height="__HEIGHT__" alt="Replay frame">
      <div id="entityLayer" class="entity-layer"></div>
    </div>
    <canvas id="webglScene"></canvas>
    <svg id="pathOverlay" class="path-overlay" aria-hidden="true"></svg>
    <div id="selectionRect" class="selection-rect"></div>
    <div id="screenMessage" class="screen-message">
      <img id="messageIcon" src="__ICON_ONSCREEN_WORKER__" alt="">
      <div id="messageText">Expert Opening bereit</div>
    </div>
    <div class="sidehud compact">
      <div class="panel">
        <div id="headline" class="big"></div>
        <div id="action" class="actionline"></div>
        <div class="statgrid">
          <div class="stat"><b id="statBuildings">0</b><span>Gebaeude</span></div>
          <div class="stat"><b id="statSites">0</b><span>Baustellen</span></div>
          <div class="stat"><b id="statSerfs">0</b><span>Serfs</span></div>
          <div class="stat"><b id="statWorkers">0</b><span>Worker</span></div>
        </div>
        <div class="asset-strip debug-only">
          <div class="asset-badge"><img src="__ICON_SERF__" alt="Serf"></div>
          <div class="asset-badge"><img src="__ICON_WORKER__" alt="Worker"></div>
          <div class="asset-badge"><img src="__ICON_UNIVERSITY__" alt="Hochschule"></div>
          <div class="asset-badge"><img src="__ICON_HEADQUARTER__" alt="Hauptquartier"></div>
        </div>
        <div class="graphics-report __GRAPHICS_REPORT_CLASS__ debug-only">
          <a href="__GRAPHICS_REPORT_LINK__" target="_blank" rel="noreferrer">Originalgrafik-Report</a>
          <p>__GRAPHICS_REPORT_SUMMARY__</p>
          <div class="mesh-strip">
            <img src="__MESH_SERF__" alt="Serf Mesh">
            <img src="__MESH_HEADQUARTER__" alt="HQ Mesh">
            <img src="__MESH_UNIVERSITY__" alt="Hochschule Mesh">
            <img src="__MESH_TREE__" alt="Baum Mesh">
          </div>
        </div>
        <button class="toolbutton" id="fit" style="margin-top:10px;">HQ Kamera</button>
      </div>
      <div class="minimap">
        <div class="minimap-title"><span>Karte</span><span id="zoomLevel">100%</span></div>
        <div id="miniBox" class="minimap-inner">
          <img id="mini" src="" alt="">
          <svg id="miniMarkers" aria-hidden="true"></svg>
          <div id="miniView"></div>
        </div>
      </div>
    </div>
    <div class="bottomhud">
      <div class="selection-panel">
        <div class="portrait"><img id="selectedPortrait" src="__ICON_SERF__" alt=""></div>
        <div>
          <div id="selectedTitle" class="selection-title">Keine Auswahl</div>
          <div id="selectedMeta" class="selection-meta"></div>
          <div id="selectedCoords" class="selection-meta"></div>
          <div class="selection-actions">
            <button class="toolbutton" id="focusSelected">Fokus</button>
            <button class="toolbutton" id="clearSelected">Abwahl</button>
          </div>
        </div>
      </div>
      <div class="command-panel">
        <div class="command-tabs">
          <div class="tab-icon"><img src="__ICON_TAB_BUILD__" alt=""></div>
          <div class="tab-icon"><img src="__ICON_TAB_WORKERS__" alt=""></div>
          <div class="tab-icon"><img src="__ICON_TAB_MOTIVATION__" alt=""></div>
        </div>
        <div id="commandGrid" class="command-grid">
          <button class="command-slot" id="cmdPrev" title="Vorige Auswahl"><img src="__ICON_TO_WORKER__" alt=""><span class="debug-only">&lt;</span></button>
          <button class="command-slot" id="cmdNext" title="Naechste Auswahl"><img src="__ICON_TO_BUILDING__" alt=""><span class="debug-only">&gt;</span></button>
          <button class="command-slot" id="cmdHQ" title="Hauptquartier"><img src="__ICON_HEADQUARTER__" alt=""><span class="debug-only">HQ</span></button>
          <button class="command-slot" id="cmdTrails" title="Laufwege"><img src="__ICON_TRAILS__" alt=""><span class="debug-only">Weg</span></button>
          <button class="command-slot" id="cmdPlay" title="Play/Pause"><img src="__ICON_OK__" alt=""><span class="debug-only">Play</span></button>
          <button class="command-slot" id="cmdStepBack" title="Ein Schritt zurueck"><img class="small-icon rotate-left" src="__ICON_ARROW__" alt=""><span class="debug-only">-1</span></button>
          <button class="command-slot" id="cmdStepForward" title="Ein Schritt vor"><img class="small-icon rotate-right" src="__ICON_ARROW__" alt=""><span class="debug-only">+1</span></button>
          <button class="command-slot" id="cmdZoomIn" title="Zoom rein"><img class="small-icon" src="__ICON_PLUS__" alt=""><span class="debug-only">+</span></button>
          <button class="command-slot" id="cmdZoomOut" title="Zoom raus"><img class="small-icon" src="__ICON_MINUS__" alt=""><span class="debug-only">-</span></button>
        </div>
      </div>
      <div class="replay-panel">
        <div id="bottomAction" class="replay-line">Aktion 0</div>
        <input id="bottomSlider" type="range" min="0" max="__MAX_INDEX__" value="0">
        <div class="replay-buttons">
          <button class="toolbutton" id="bottomPrev">Zurueck</button>
          <button class="toolbutton" id="bottomPlay">Play</button>
          <button class="toolbutton" id="bottomNext">Weiter</button>
          <button class="toolbutton" id="bottomHQ">HQ</button>
        </div>
        <div class="camera-hint debug-only">WASD/Rand scrollt, Mausrad zoomt, Klick waehlt Entity.</div>
      </div>
    </div>
  </div>
  <script>
    const timeline = __TIMELINE__;
    const gameAssets = __GAME_ASSETS__;
    window.gameAssets = gameAssets;
    const originalGraphics = gameAssets.original_graphics || {};
    const spriteByKey = originalGraphics.sprite_by_key || {};
    const meshByKey = originalGraphics.mesh_by_key || {};
    const model3dByKey = originalGraphics.model3d_by_key || {};
    const embeddedModel3d = originalGraphics.embedded_model3d || {};
    const animationByKey = originalGraphics.animation_by_key || {};
    const assetByKey = gameAssets.assets || {};
    const terrain3d = gameAssets.terrain3d || { enabled: false };
    const terrainTexture = gameAssets.terrain_texture || '';
    const minimapTexture = gameAssets.minimap_texture || terrainTexture || '';
    const paydayFrames = gameAssets.payday_frames || [];
    const MAP_WIDTH = __WIDTH__;
    const MAP_HEIGHT = __HEIGHT__;
    const world = document.getElementById('world');
    const img = document.getElementById('map');
    const webglScene = document.getElementById('webglScene');
    const entityLayer = document.getElementById('entityLayer');
    const pathOverlay = document.getElementById('pathOverlay');
    const selectionRect = document.getElementById('selectionRect');
    const mini = document.getElementById('mini');
    const miniBox = document.getElementById('miniBox');
    const miniMarkers = document.getElementById('miniMarkers');
    const miniView = document.getElementById('miniView');
    const stage = document.getElementById('stage');
    const slider = document.getElementById('slider');
    const playBtn = document.getElementById('play');
    const fullscreenBtn = document.getElementById('fullscreen');
    const mode3dBtn = document.getElementById('mode3d');
    const speed = document.getElementById('speed');
    const headline = document.getElementById('headline');
    const action = document.getElementById('action');
    const zoomLevel = document.getElementById('zoomLevel');
    const paydayIcon = document.getElementById('paydayIcon');
    const bottomSlider = document.getElementById('bottomSlider');
    const bottomAction = document.getElementById('bottomAction');
    const bottomPlay = document.getElementById('bottomPlay');
    const selectedPortrait = document.getElementById('selectedPortrait');
    const selectedTitle = document.getElementById('selectedTitle');
    const selectedMeta = document.getElementById('selectedMeta');
    const selectedCoords = document.getElementById('selectedCoords');
    const screenMessage = document.getElementById('screenMessage');
    const messageIcon = document.getElementById('messageIcon');
    const messageText = document.getElementById('messageText');
    const resIds = {
      taler: document.getElementById('resTaler'),
      holz: document.getElementById('resHolz'),
      stein: document.getElementById('resStein'),
      lehm: document.getElementById('resLehm'),
      eisen: document.getElementById('resEisen'),
      schwefel: document.getElementById('resSchwefel'),
      holz_roh: document.getElementById('rawHolz'),
      stein_roh: document.getElementById('rawStein'),
      lehm_roh: document.getElementById('rawLehm'),
      eisen_roh: document.getElementById('rawEisen'),
      schwefel_roh: document.getElementById('rawSchwefel'),
    };
    let idx = 0;
    let timer = null;
    let scale = 1;
    let tx = 0;
    let ty = 0;
    let dragging = false;
    let lastX = 0;
    let lastY = 0;
    const entityNodes = new Map();
    const entityData = new Map();
    let selectedEntityIds = new Set();
    let selectedEntityId = null;
    let hoveredEntityId = null;
    let messageTimer = null;
    let suppressModeMessage = false;
    let mouseX = 0;
    let mouseY = 0;
    let edgePanActive = false;
    let edgePanFrame = null;
    let selectingBox = false;
    let selectionMoved = false;
    let selectionStartX = 0;
    let selectionStartY = 0;
    let suppressNextClick = false;
    let mode3d = false;
    let renderer3d = null;
    let rotatingCamera = false;
    const CAMERA_DEFAULT_YAW = -0.553;
    const CAMERA_DEFAULT_PITCH = 0.733;
    let cameraYaw = CAMERA_DEFAULT_YAW;
    let cameraPitch = CAMERA_DEFAULT_PITCH;
    let showAllTrails = false;
    const INITIAL_CAMERA_X = __INITIAL_CAMERA_X__;
    const INITIAL_CAMERA_Y = __INITIAL_CAMERA_Y__;
    const INITIAL_CAMERA_SCALE = __INITIAL_CAMERA_SCALE__;
    window.replayDebug = {
      timeline,
      gameAssets,
      get index() { return idx; },
      get mode3d() { return mode3d; },
      stats() {
        const canvas = document.getElementById('webglScene');
        return {
          index: idx,
          time: (timeline[idx] || {}).time,
          mode3d,
          drawnModels: canvas && canvas.dataset.drawnModels,
          totalEntities: canvas && canvas.dataset.totalEntities,
          modelsLoaded: canvas && canvas.dataset.modelsLoaded,
          modelErrors: canvas && canvas.dataset.modelErrors,
          showAllTrails,
          terrain: canvas && canvas.dataset.terrain,
          lighting: canvas && canvas.dataset.lighting,
          animation: canvas && canvas.dataset.animation,
          animationKeys: canvas && canvas.dataset.animationKeys,
          originalAnimationDrawn: canvas && canvas.dataset.originalAnimationDrawn,
          originalAnimationPending: canvas && canvas.dataset.originalAnimationPending,
          originalAnimationMaxDisplacement: canvas && canvas.dataset.originalAnimationMaxDisplacement,
          originalAnimationAssets: canvas && canvas.dataset.originalAnimationAssets,
          originalAnimationErrors: canvas && canvas.dataset.originalAnimationErrors,
          orientedEntities: canvas && canvas.dataset.orientedEntities,
          selectedEntity: canvas && canvas.dataset.selectedEntity,
          selectedEntities: canvas && canvas.dataset.selectedEntities,
          selectionCount: canvas && canvas.dataset.selectionCount,
          hoveredEntity: canvas && canvas.dataset.hoveredEntity,
          cameraYawDeg: canvas && canvas.dataset.cameraYawDeg,
          cameraPitchDeg: canvas && canvas.dataset.cameraPitchDeg,
        };
      },
      setFrame(frameIndex) {
        show(Number(frameIndex || 0));
        return this.stats();
      },
      setMode3d(enabled = true) {
        if (Boolean(enabled) !== mode3d) mode3dBtn.click();
        return this.stats();
      },
      select(entityId, additive = false) {
        selectEntity(String(entityId || ''), false, Boolean(additive));
        return this.stats();
      },
      focus(entityId) {
        const entity = ((timeline[idx] || {}).entities || []).find(item => item.id === entityId);
        if (entity) {
          selectEntity(entity.id, false, false);
          centerOnFramePoint(entity.x, entity.y, Math.max(scale, 2.4));
        }
        return this.stats();
      },
      setCamera(options = {}) {
        if (Number.isFinite(Number(options.scale))) scale = clamp(Number(options.scale), 0.15, 12);
        if (Number.isFinite(Number(options.tx))) tx = Number(options.tx);
        if (Number.isFinite(Number(options.ty))) ty = Number(options.ty);
        if (Number.isFinite(Number(options.x)) && Number.isFinite(Number(options.y))) {
          tx = stage.clientWidth / 2 - Number(options.x) * scale;
          ty = stage.clientHeight / 2 - Number(options.y) * scale;
        }
        if (Number.isFinite(Number(options.yaw))) cameraYaw = Number(options.yaw);
        if (Number.isFinite(Number(options.pitch))) cameraPitch = clampCameraPitch(Number(options.pitch));
        applyTransform();
        return this.stats();
      },
      setModelCulling(enabled = true) {
        if (renderer3d && renderer3d.setModelCulling) renderer3d.setModelCulling(Boolean(enabled));
        if (mode3d && renderer3d) renderer3d.render(timeline[idx]);
        return this.stats();
      },
    };

    function clamp(value, min, max) {
      return Math.max(min, Math.min(max, value));
    }
    function fmt(value) {
      if (value === null || value === undefined) return '-';
      return Number(value).toLocaleString('de-DE');
    }
    function fmtTime(seconds) {
      if (seconds === null || seconds === undefined) return '-';
      const s = Math.max(0, Number(seconds));
      const m = Math.floor(s / 60);
      const rest = Math.floor(s % 60);
      return `${m}:${String(rest).padStart(2, '0')}`;
    }
    function setText(id, value) {
      document.getElementById(id).textContent = value;
    }
    function minimapContentArea() {
      const boxRect = miniBox.getBoundingClientRect();
      const imageRect = mini.getBoundingClientRect();
      const width = imageRect.width || miniBox.clientWidth;
      const height = imageRect.height || miniBox.clientHeight;
      return {
        left: Math.max(0, imageRect.left - boxRect.left),
        top: Math.max(0, imageRect.top - boxRect.top),
        width,
        height,
      };
    }
    function placeMinimapOverlay() {
      const area = minimapContentArea();
      miniMarkers.style.left = `${area.left}px`;
      miniMarkers.style.top = `${area.top}px`;
      miniMarkers.style.width = `${area.width}px`;
      miniMarkers.style.height = `${area.height}px`;
      miniMarkers.setAttribute('viewBox', `0 0 ${area.width} ${area.height}`);
      miniMarkers.setAttribute('width', String(area.width));
      miniMarkers.setAttribute('height', String(area.height));
      return area;
    }
    function updateMinimap() {
      if (!miniBox.clientWidth || !miniBox.clientHeight) return;
      zoomLevel.textContent = `${Math.round(scale * 100)}%`;
      const area = placeMinimapOverlay();
      const sx = area.width / MAP_WIDTH;
      const sy = area.height / MAP_HEIGHT;
      const visibleX = clamp(-tx / scale, 0, MAP_WIDTH);
      const visibleY = clamp(-ty / scale, 0, MAP_HEIGHT);
      const visibleW = clamp(stage.clientWidth / scale, 0, MAP_WIDTH);
      const visibleH = clamp(stage.clientHeight / scale, 0, MAP_HEIGHT);
      miniView.style.left = `${area.left + clamp(visibleX * sx, 0, area.width)}px`;
      miniView.style.top = `${area.top + clamp(visibleY * sy, 0, area.height)}px`;
      miniView.style.width = `${clamp(visibleW * sx, 8, area.width)}px`;
      miniView.style.height = `${clamp(visibleH * sy, 8, area.height)}px`;
    }
    function updateMiniMarkers(f) {
      const area = placeMinimapOverlay();
      miniMarkers.replaceChildren();
      const kinds = new Set(['building', 'site', 'serf', 'worker', 'resource', 'shaft']);
      const svgNs = 'http://www.w3.org/2000/svg';
      for (const entity of (f.entities || [])) {
        if (!kinds.has(entity.kind)) continue;
        const cx = clamp((Number(entity.x || 0) / MAP_WIDTH) * area.width, 0, area.width);
        const cy = clamp((Number(entity.y || 0) / MAP_HEIGHT) * area.height, 0, area.height);
        const marker = document.createElementNS(svgNs, 'circle');
        const selected = selectedEntityIds.has(entity.id);
        marker.setAttribute('cx', String(Math.round(cx * 10) / 10));
        marker.setAttribute('cy', String(Math.round(cy * 10) / 10));
        marker.setAttribute('r', selected ? '4.1' : (entity.kind === 'building' || entity.kind === 'site' ? '3.2' : '2.4'));
        marker.setAttribute('class', `mini-${sanitizeClass(entity.kind)}${selected ? ' mini-selected' : ''}`);
        miniMarkers.appendChild(marker);
      }
    }
    function constrainTransform() {
      const mapW = MAP_WIDTH * scale;
      const mapH = MAP_HEIGHT * scale;
      if (mapW <= stage.clientWidth) {
        tx = (stage.clientWidth - mapW) / 2;
      } else {
        tx = clamp(tx, stage.clientWidth - mapW, 0);
      }
      if (mapH <= stage.clientHeight) {
        ty = (stage.clientHeight - mapH) / 2;
      } else {
        ty = clamp(ty, stage.clientHeight - mapH, 0);
      }
    }
    function applyTransform() {
      constrainTransform();
      world.style.transform = `translate(${tx}px, ${ty}px) scale(${scale})`;
      updateMinimap();
      if (mode3d && renderer3d) renderer3d.render(timeline[idx]);
      renderMovementTrails();
    }
    function clampCameraPitch(value) {
      return clamp(value, 0.38, 1.18);
    }
    function resetCameraAngles() {
      cameraYaw = CAMERA_DEFAULT_YAW;
      cameraPitch = CAMERA_DEFAULT_PITCH;
    }
    function rotateCamera(deltaYaw, deltaPitch = 0) {
      cameraYaw += deltaYaw;
      cameraPitch = clampCameraPitch(cameraPitch + deltaPitch);
      if (mode3d && renderer3d) renderer3d.render(timeline[idx]);
    }
    function panBy(dx, dy) {
      tx += dx;
      ty += dy;
      applyTransform();
    }
    function zoomAt(screenX, screenY, factor) {
      const beforeX = (screenX - tx) / scale;
      const beforeY = (screenY - ty) / scale;
      scale = Math.max(0.15, Math.min(12, scale * factor));
      tx = screenX - beforeX * scale;
      ty = screenY - beforeY * scale;
      applyTransform();
    }
    function centerOnFramePoint(x, y, targetScale) {
      if (targetScale) scale = Math.max(0.15, Math.min(12, targetScale));
      tx = stage.clientWidth / 2 - Number(x || 0) * scale;
      ty = stage.clientHeight / 2 - Number(y || 0) * scale;
      applyTransform();
    }
    function selectedEntity() {
      return selectedEntityId ? entityData.get(selectedEntityId) : null;
    }
    function selectedEntities() {
      return Array.from(selectedEntityIds)
        .map(id => entityData.get(id))
        .filter(Boolean);
    }
    function normalizeSelection(ids) {
      const clean = [];
      const seen = new Set();
      for (const id of ids || []) {
        if (!id || seen.has(id) || !entityData.has(id)) continue;
        seen.add(id);
        clean.push(id);
      }
      return clean;
    }
    function selectedKindSummary(entities) {
      const counts = new Map();
      for (const entity of entities) {
        const key = entity.kind || 'entity';
        counts.set(key, (counts.get(key) || 0) + 1);
      }
      return Array.from(counts.entries())
        .map(([kind, count]) => `${kind}: ${count}`)
        .join(', ');
    }
    function selectionBounds(entities) {
      if (!entities.length) return null;
      let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
      for (const entity of entities) {
        const size = Math.max(16, Number(entity.size || 32));
        const x = Number(entity.x || 0);
        const y = Number(entity.y || 0);
        minX = Math.min(minX, x - size * .5);
        minY = Math.min(minY, y - size * .5);
        maxX = Math.max(maxX, x + size * .5);
        maxY = Math.max(maxY, y + size * .5);
      }
      return { minX, minY, maxX, maxY, width: maxX - minX, height: maxY - minY };
    }
    function focusSelection() {
      const entities = selectedEntities();
      if (!entities.length) return;
      if (entities.length === 1) {
        centerOnFramePoint(entities[0].x, entities[0].y, Math.max(scale, 2.4));
        return;
      }
      const bounds = selectionBounds(entities);
      if (!bounds) return;
      const pad = 260;
      const targetScale = Math.min(
        4.2,
        Math.max(0.2, stage.clientWidth / Math.max(1, bounds.width + pad)),
        Math.max(0.2, stage.clientHeight / Math.max(1, bounds.height + pad))
      );
      centerOnFramePoint((bounds.minX + bounds.maxX) / 2, (bounds.minY + bounds.maxY) / 2, Math.max(targetScale, 0.6));
    }
    function applySelection(ids, primaryId = null, focus = false) {
      const clean = normalizeSelection(ids);
      selectedEntityIds = new Set(clean);
      selectedEntityId = primaryId && selectedEntityIds.has(primaryId) ? primaryId : (clean[0] || null);
      for (const [nodeId, node] of entityNodes.entries()) {
        node.classList.toggle('selected', selectedEntityIds.has(nodeId));
      }
      renderSelection();
      updateMiniMarkers(timeline[idx] || {});
      if (focus) focusSelection();
      if (mode3d && renderer3d) renderer3d.render(timeline[idx]);
      renderMovementTrails();
    }
    function setHoveredEntity(id) {
      const nextId = id && entityData.has(id) ? id : null;
      if (hoveredEntityId === nextId) return;
      hoveredEntityId = nextId;
      stage.classList.toggle('hovering-entity', Boolean(hoveredEntityId));
      if (mode3d && renderer3d) renderer3d.render(timeline[idx]);
    }
    function setMessage(text, icon, options = {}) {
      if (!screenMessage || options.silent || !text) {
        if (screenMessage) screenMessage.classList.remove('visible');
        if (messageTimer) clearTimeout(messageTimer);
        messageTimer = null;
        return;
      }
      if (messageText) messageText.textContent = text || '';
      if (messageIcon && icon) messageIcon.src = icon;
      screenMessage.classList.add('visible');
      if (messageTimer) clearTimeout(messageTimer);
      const timeout = Number.isFinite(Number(options.timeout)) ? Number(options.timeout) : 2600;
      if (timeout > 0) {
        messageTimer = setTimeout(() => {
          screenMessage.classList.remove('visible');
          messageTimer = null;
        }, timeout);
      }
    }
    function sanitizeClass(value) {
      return String(value || '').toLowerCase().replace(/[^a-z0-9_-]+/g, '_');
    }
    function entityFallbackAsset(kind) {
      if (kind === 'serf') return assetByKey.serf || '';
      if (kind === 'worker') return assetByKey.worker || '';
      if (kind === 'tree') return assetByKey.wood || '';
      if (kind === 'resource') return assetByKey.stone || assetByKey.mine || '';
      if (kind === 'shaft') return assetByKey.mine || assetByKey.stone || '';
      if (kind === 'site') return assetByKey.site || assetByKey.mine || '';
      return assetByKey.headquarter || assetByKey.site || '';
    }
    function entitySpriteSrc(entity) {
      return spriteByKey[entity.sprite_key] || meshByKey[entity.sprite_key] || entityFallbackAsset(entity.kind);
    }
    const SVG_NS = 'http://www.w3.org/2000/svg';
    const TRAIL_HISTORY_FRAMES = 36;
    const TRAIL_ENTITY_LIMIT = 8;
    const TRAIL_ALL_ENTITY_LIMIT = 48;
    function createOverlayNode(name, attributes) {
      const node = document.createElementNS(SVG_NS, name);
      for (const [key, value] of Object.entries(attributes || {})) {
        node.setAttribute(key, String(value));
      }
      return node;
    }
    function projectOverlayPoint(entity) {
      if (!entity) return null;
      if (mode3d && renderer3d && renderer3d.projectEntity) {
        return renderer3d.projectEntity(entity);
      }
      return {
        x: Number(entity.x || 0) * scale + tx,
        y: Number(entity.y || 0) * scale + ty,
      };
    }
    function movementHistory(entityId) {
      const start = Math.max(0, idx - TRAIL_HISTORY_FRAMES);
      const history = [];
      for (let frameIndex = start; frameIndex <= idx; frameIndex += 1) {
        const entry = ((timeline[frameIndex] || {}).entities || []).find(entity => entity.id === entityId);
        if (entry) history.push(entry);
      }
      return history;
    }
    function appendMovementTarget(entity, point) {
      if (entity.target_x === undefined || entity.target_y === undefined || !point) return;
      const target = projectOverlayPoint({ ...entity, x: entity.target_x, y: entity.target_y });
      if (!target || Math.hypot(target.x - point.x, target.y - point.y) < 8) return;
      pathOverlay.appendChild(createOverlayNode('path', {
        class: 'movement-target-line',
        d: `M ${point.x.toFixed(1)} ${point.y.toFixed(1)} L ${target.x.toFixed(1)} ${target.y.toFixed(1)}`,
      }));
      pathOverlay.appendChild(createOverlayNode('circle', {
        class: 'movement-target',
        cx: target.x.toFixed(1),
        cy: target.y.toFixed(1),
        r: 4.2,
      }));
    }
    function renderMovementTrails() {
      if (!pathOverlay) return;
      const overlayWidth = Math.max(1, stage.clientWidth);
      const overlayHeight = Math.max(1, stage.clientHeight);
      pathOverlay.setAttribute('viewBox', `0 0 ${overlayWidth} ${overlayHeight}`);
      pathOverlay.replaceChildren();
      const sourceEntities = showAllTrails ? (((timeline[idx] || {}).entities) || []) : selectedEntities();
      const movingEntities = sourceEntities
        .filter(entity => entity.kind === 'serf' || entity.kind === 'worker')
        .slice(0, showAllTrails ? TRAIL_ALL_ENTITY_LIMIT : TRAIL_ENTITY_LIMIT);
      for (const entity of movingEntities) {
        const points = [];
        for (const historicEntity of movementHistory(entity.id)) {
          const point = projectOverlayPoint(historicEntity);
          const lastPoint = points[points.length - 1];
          if (!point || (lastPoint && Math.hypot(point.x - lastPoint.x, point.y - lastPoint.y) < .7)) continue;
          points.push(point);
        }
        if (points.length > 1) {
          const d = points
            .map((point, pointIndex) => `${pointIndex ? 'L' : 'M'} ${point.x.toFixed(1)} ${point.y.toFixed(1)}`)
            .join(' ');
          pathOverlay.appendChild(createOverlayNode('path', {
            class: 'movement-trail-shadow',
            d,
          }));
          pathOverlay.appendChild(createOverlayNode('path', {
            class: `movement-trail ${sanitizeClass(entity.kind)}`,
            d,
          }));
        }
        appendMovementTarget(entity, points[points.length - 1] || projectOverlayPoint(entity));
      }
    }
    function createReplay3DRenderer(canvas) {
      const gl = canvas.getContext('webgl', { alpha: false, antialias: true });
      if (!gl) return null;
      const uintIndexExt = gl.getExtension('OES_element_index_uint');

      const vertexSource = `
        attribute vec3 a_position;
        attribute vec3 a_normal;
        attribute vec2 a_uv;
        uniform mat4 u_matrix;
        uniform mat4 u_world;
        varying vec2 v_uv;
        varying vec3 v_normal;
        void main() {
          v_uv = a_uv;
          v_normal = normalize((u_world * vec4(a_normal, 0.0)).xyz);
          gl_Position = u_matrix * vec4(a_position, 1.0);
        }
      `;
      const fragmentSource = `
        precision mediump float;
        varying vec2 v_uv;
        varying vec3 v_normal;
        uniform sampler2D u_texture;
        uniform vec3 u_light_dir;
        uniform float u_ambient;
        void main() {
          vec4 color = texture2D(u_texture, v_uv);
          if (color.a < 0.08) discard;
          float diffuse = max(dot(normalize(v_normal), normalize(u_light_dir)), 0.0);
          float light = clamp(u_ambient + diffuse * 0.58, 0.32, 1.18);
          color.rgb *= light;
          gl_FragColor = color;
        }
      `;

      function compile(type, source) {
        const shader = gl.createShader(type);
        gl.shaderSource(shader, source);
        gl.compileShader(shader);
        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
          throw new Error(gl.getShaderInfoLog(shader) || 'shader compile failed');
        }
        return shader;
      }
      const program = gl.createProgram();
      gl.attachShader(program, compile(gl.VERTEX_SHADER, vertexSource));
      gl.attachShader(program, compile(gl.FRAGMENT_SHADER, fragmentSource));
      gl.linkProgram(program);
      if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        throw new Error(gl.getProgramInfoLog(program) || 'program link failed');
      }
      const locations = {
        position: gl.getAttribLocation(program, 'a_position'),
        normal: gl.getAttribLocation(program, 'a_normal'),
        uv: gl.getAttribLocation(program, 'a_uv'),
        matrix: gl.getUniformLocation(program, 'u_matrix'),
        world: gl.getUniformLocation(program, 'u_world'),
        texture: gl.getUniformLocation(program, 'u_texture'),
        lightDir: gl.getUniformLocation(program, 'u_light_dir'),
        ambient: gl.getUniformLocation(program, 'u_ambient'),
      };

      const modelCache = new Map();
      const textureCache = new Map();
      const animationCache = new Map();
      let lastStats = { drawnModels: 0, totalEntities: 0, modelsCached: 0, texturesCached: 0, canvas: [0, 0] };
      const terrainRows = Number(terrain3d.rows || 0);
      const terrainCols = Number(terrain3d.cols || 0);
      const terrainPositions = terrain3d.positions || [];
      const terrainXMin = Number.isFinite(Number(terrain3d.x_min)) ? Number(terrain3d.x_min) : -MAP_WIDTH / 2;
      const terrainXMax = Number.isFinite(Number(terrain3d.x_max)) ? Number(terrain3d.x_max) : MAP_WIDTH / 2;
      const terrainZMin = Number.isFinite(Number(terrain3d.z_min)) ? Number(terrain3d.z_min) : -MAP_HEIGHT / 2;
      const terrainZMax = Number.isFinite(Number(terrain3d.z_max)) ? Number(terrain3d.z_max) : MAP_HEIGHT / 2;
      const terrainPad = Math.max(terrainXMax - terrainXMin, terrainZMax - terrainZMin, MAP_WIDTH, MAP_HEIGHT) * 0.10;
      const terrainBackplate = createStaticMesh(
        [
          terrainXMin - terrainPad, -26, terrainZMin - terrainPad,
          terrainXMax + terrainPad, -26, terrainZMin - terrainPad,
          terrainXMax + terrainPad, -26, terrainZMax + terrainPad,
          terrainXMin - terrainPad, -26, terrainZMax + terrainPad,
        ],
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 1, 0, 1],
        [0, 1, 2, 0, 2, 3]
      );
      const mapQuad = createStaticMesh(
        [
          -MAP_WIDTH / 2, -1, -MAP_HEIGHT / 2,
           MAP_WIDTH / 2, -1, -MAP_HEIGHT / 2,
           MAP_WIDTH / 2, -1,  MAP_HEIGHT / 2,
          -MAP_WIDTH / 2, -1,  MAP_HEIGHT / 2,
        ],
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 1, 0, 1],
        [0, 1, 2, 0, 2, 3]
      );
      const terrainMesh = terrain3d.enabled
        ? createStaticMesh(terrain3d.positions || [], terrain3d.normals || [], terrain3d.uvs || [], terrain3d.indices || [])
        : mapQuad;
      const selectionMesh = createStaticMesh(
        [
          -1, 0, -1,
           1, 0, -1,
           1, 0,  1,
          -1, 0,  1,
        ],
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 1, 0, 1],
        [0, 1, 2, 0, 2, 3]
      );
      let cullEntityModels = false;
      const allowRigidAtomicAnimation = false;
      const shadowTexture = createTexture(shadowTextureDataUrl());
      const selectionTexture = createTexture(ringTextureDataUrl('#f6d66f', '#3a2108', 10, 4, 0.96, 0.85));
      const hoverTexture = createTexture(ringTextureDataUrl('#d9f0ff', '#132536', 7, 3, 0.78, 0.72));

      function shadowTextureDataUrl() {
        const shadowCanvas = document.createElement('canvas');
        shadowCanvas.width = 128;
        shadowCanvas.height = 128;
        const ctx = shadowCanvas.getContext('2d');
        ctx.clearRect(0, 0, shadowCanvas.width, shadowCanvas.height);
        const gradient = ctx.createRadialGradient(64, 64, 4, 64, 64, 58);
        gradient.addColorStop(0, 'rgba(0,0,0,.34)');
        gradient.addColorStop(0.58, 'rgba(0,0,0,.20)');
        gradient.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.save();
        ctx.translate(64, 64);
        ctx.scale(1, 0.48);
        ctx.translate(-64, -64);
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(64, 64, 58, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
        return shadowCanvas.toDataURL('image/png');
      }

      function ringTextureDataUrl(primary, secondary, primaryWidth, secondaryWidth, primaryAlpha, secondaryAlpha) {
        const ringCanvas = document.createElement('canvas');
        ringCanvas.width = 128;
        ringCanvas.height = 128;
        const ctx = ringCanvas.getContext('2d');
        ctx.clearRect(0, 0, ringCanvas.width, ringCanvas.height);
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.globalAlpha = primaryAlpha;
        ctx.strokeStyle = primary;
        ctx.lineWidth = primaryWidth;
        ctx.beginPath();
        ctx.ellipse(64, 64, 54, 34, 0, 0, Math.PI * 2);
        ctx.stroke();
        ctx.globalAlpha = secondaryAlpha;
        ctx.strokeStyle = secondary;
        ctx.lineWidth = secondaryWidth;
        ctx.beginPath();
        ctx.ellipse(64, 64, 44, 25, 0, 0, Math.PI * 2);
        ctx.stroke();
        ctx.globalAlpha = 1;
        return ringCanvas.toDataURL('image/png');
      }

      function createTexture(url) {
        if (textureCache.has(url)) return textureCache.get(url);
        const texture = gl.createTexture();
        gl.bindTexture(gl.TEXTURE_2D, texture);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([82, 91, 74, 255]));
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
        const record = { texture, loaded: false };
        textureCache.set(url, record);
        const image = new Image();
        image.onload = () => {
          gl.bindTexture(gl.TEXTURE_2D, texture);
          gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
          gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
          record.loaded = true;
          if (mode3d) render(timeline[idx]);
        };
        image.src = url;
        return record;
      }

      function createStaticMesh(positions, normals, uvs, indices) {
        const positionBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positions), gl.STATIC_DRAW);
        const normalValues = normals && normals.length === positions.length
          ? normals
          : Array.from({ length: positions.length / 3 }, () => [0, 1, 0]).flat();
        const normalBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, normalBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(normalValues), gl.STATIC_DRAW);
        const uvBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, uvBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(uvs), gl.STATIC_DRAW);
        const indexBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);
        const maxIndex = indices.reduce((max, value) => Math.max(max, Number(value || 0)), 0);
        const useUint32 = Boolean(uintIndexExt) && maxIndex > 65535;
        gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, useUint32 ? new Uint32Array(indices) : new Uint16Array(indices), gl.STATIC_DRAW);
        return { positionBuffer, normalBuffer, uvBuffer, indexBuffer, indexType: useUint32 ? gl.UNSIGNED_INT : gl.UNSIGNED_SHORT, count: indices.length, maxSpan: Math.max(MAP_WIDTH, MAP_HEIGHT) };
      }

      function loadJson(url) {
        return new Promise((resolve, reject) => {
          const xhr = new XMLHttpRequest();
          xhr.open('GET', url, true);
          xhr.overrideMimeType('application/json');
          xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 300) {
              try {
                resolve(JSON.parse(xhr.responseText));
              } catch (error) {
                reject(error);
              }
            } else {
              reject(new Error(`HTTP ${xhr.status} ${url}`));
            }
          };
          xhr.onerror = () => reject(new Error(`XHR failed ${url}`));
          xhr.send();
        });
      }

      async function loadModel(modelUrl) {
        const data = embeddedModel3d[modelUrl] || await loadJson(modelUrl);
        const basePositions = new Float32Array(data.positions || []);
        const baseNormals = data.normals && data.normals.length === data.positions.length
          ? new Float32Array(data.normals)
          : new Float32Array(Array.from({ length: (data.positions || []).length / 3 }, () => [0, 1, 0]).flat());
        const skinning = data.skinning && (data.skinning.geometry_skins || []).length ? data.skinning : null;
        const sourcePositions = data.source_positions && data.source_positions.length === data.positions.length
          ? new Float32Array(data.source_positions)
          : null;
        const sourceNormals = data.source_normals && data.source_normals.length === data.positions.length
          ? new Float32Array(data.source_normals)
          : null;
        const objectFrames = data.object_frames && (data.object_frames.atomic_bindings || []).length
          ? data.object_frames
          : null;
        const dynamicGeometry = Boolean(skinning);
        const positionBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, basePositions, dynamicGeometry ? gl.DYNAMIC_DRAW : gl.STATIC_DRAW);
        const normalBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, normalBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, baseNormals, dynamicGeometry ? gl.DYNAMIC_DRAW : gl.STATIC_DRAW);
        const uvBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, uvBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(data.uvs || []), gl.STATIC_DRAW);
        const root = modelUrl.slice(0, modelUrl.indexOf('/models3d/') + 1);
        const submeshes = [];
        for (const submesh of (data.submeshes || [])) {
          const indexBuffer = gl.createBuffer();
          gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);
          const rawIndices = submesh.indices || [];
          const maxIndex = rawIndices.reduce((max, value) => Math.max(max, Number(value || 0)), 0);
          const useUint32 = Boolean(uintIndexExt) && maxIndex > 65535;
          const indices = useUint32 ? new Uint32Array(rawIndices) : new Uint16Array(rawIndices);
          gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, indices, gl.STATIC_DRAW);
          const textureUrl = submesh.texture ? root + submesh.texture : '';
          submeshes.push({
            indexBuffer,
            count: indices.length,
            indexType: useUint32 ? gl.UNSIGNED_INT : gl.UNSIGNED_SHORT,
            texture: createTexture(textureUrl || 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII='),
          });
        }
        return {
          positionBuffer,
          normalBuffer,
          uvBuffer,
          submeshes,
          basePositions,
          baseNormals,
          sourcePositions,
          sourceNormals,
          skinning,
          objectFrames,
          sourceBounds: data.bounds || {},
          maxSpan: Number((data.bounds || {}).max_span || 100),
        };
      }

      function ensureAnimation(animationUrl) {
        if (!animationUrl) return null;
        if (!animationCache.has(animationUrl)) {
          const record = { loaded: false, data: null };
          animationCache.set(animationUrl, record);
          loadJson(animationUrl)
            .then(data => {
              record.loaded = true;
              record.data = data;
              if (mode3d) render(timeline[idx]);
            })
            .catch(error => {
              record.error = String(error && error.message || error || 'animation load failed');
              console.warn('ANM track load failed', animationUrl, record.error);
            });
        }
        return animationCache.get(animationUrl);
      }

      function ensureModel(modelUrl) {
        if (!modelUrl) return null;
        if (!modelCache.has(modelUrl)) {
          const record = { loaded: false, model: null };
          modelCache.set(modelUrl, record);
          loadModel(modelUrl)
            .then(model => {
              record.loaded = true;
              record.model = model;
              canvas.dataset.loadCompletions = String(Number(canvas.dataset.loadCompletions || 0) + 1);
              if (mode3d) render(timeline[idx]);
            })
            .catch(error => {
              record.loaded = false;
              record.error = String(error && error.message || error || 'model load failed');
              canvas.dataset.loadErrors = String(Number(canvas.dataset.loadErrors || 0) + 1);
              console.warn('3D model load failed', modelUrl, record.error);
            });
        }
        return modelCache.get(modelUrl);
      }

      function m4Identity() {
        return new Float32Array([
          1, 0, 0, 0,
          0, 1, 0, 0,
          0, 0, 1, 0,
          0, 0, 0, 1,
        ]);
      }
      function m4FromQuatTranslation(qx, qy, qz, qw, tx, ty, tz) {
        const xx = qx * qx, yy = qy * qy, zz = qz * qz;
        const xy = qx * qy, xz = qx * qz, yz = qy * qz;
        const wx = qw * qx, wy = qw * qy, wz = qw * qz;
        return new Float32Array([
          1 - 2 * (yy + zz), 2 * (xy + wz), 2 * (xz - wy), 0,
          2 * (xy - wz), 1 - 2 * (xx + zz), 2 * (yz + wx), 0,
          2 * (xz + wy), 2 * (yz - wx), 1 - 2 * (xx + yy), 0,
          tx, ty, tz, 1,
        ]);
      }
      function m4TransformPoint(matrix, x, y, z) {
        return [
          matrix[0] * x + matrix[4] * y + matrix[8] * z + matrix[12],
          matrix[1] * x + matrix[5] * y + matrix[9] * z + matrix[13],
          matrix[2] * x + matrix[6] * y + matrix[10] * z + matrix[14],
        ];
      }
      function m4TransformDirection(matrix, x, y, z) {
        return [
          matrix[0] * x + matrix[4] * y + matrix[8] * z,
          matrix[1] * x + matrix[5] * y + matrix[9] * z,
          matrix[2] * x + matrix[6] * y + matrix[10] * z,
        ];
      }
      function m4AffineInverse(matrix) {
        const inverse = new Float32Array([
          matrix[0], matrix[4], matrix[8], 0,
          matrix[1], matrix[5], matrix[9], 0,
          matrix[2], matrix[6], matrix[10], 0,
          0, 0, 0, 1,
        ]);
        inverse[12] = -(inverse[0] * matrix[12] + inverse[4] * matrix[13] + inverse[8] * matrix[14]);
        inverse[13] = -(inverse[1] * matrix[12] + inverse[5] * matrix[13] + inverse[9] * matrix[14]);
        inverse[14] = -(inverse[2] * matrix[12] + inverse[6] * matrix[13] + inverse[10] * matrix[14]);
        return inverse;
      }
      function quaternionSlerp(a, b, amount) {
        let bx = b[0], by = b[1], bz = b[2], bw = b[3];
        let cosine = a[0] * bx + a[1] * by + a[2] * bz + a[3] * bw;
        if (cosine < 0) {
          cosine = -cosine;
          bx = -bx; by = -by; bz = -bz; bw = -bw;
        }
        let left;
        let right;
        if (cosine > 0.9995) {
          left = 1 - amount;
          right = amount;
        } else {
          const angle = Math.acos(Math.max(-1, Math.min(1, cosine)));
          const sine = Math.sin(angle) || 1;
          left = Math.sin((1 - amount) * angle) / sine;
          right = Math.sin(amount * angle) / sine;
        }
        const x = a[0] * left + bx * right;
        const y = a[1] * left + by * right;
        const z = a[2] * left + bz * right;
        const w = a[3] * left + bw * right;
        const length = Math.hypot(x, y, z, w) || 1;
        return [x / length, y / length, z / length, w / length];
      }
      function bindMatrixForBone(bone) {
        const bind = (bone && bone.bind_local) || {};
        const right = bind.right || [1, 0, 0];
        const up = bind.up || [0, 1, 0];
        const at = bind.at || [0, 0, 1];
        const position = bind.position || [0, 0, 0];
        return new Float32Array([
          right[0], right[1], right[2], 0,
          up[0], up[1], up[2], 0,
          at[0], at[1], at[2], 0,
          position[0], position[1], position[2], 1,
        ]);
      }
      function sampleAnimationTrack(track, duration, time) {
        if (!track || !track.length) return null;
        if (track.length === 1) return track[0];
        const clipDuration = Math.max(0.001, Number(duration || track[track.length - 1][0] || 1));
        const localTime = ((Number(time || 0) % clipDuration) + clipDuration) % clipDuration;
        let rightIndex = track.findIndex(frame => Number(frame[0]) >= localTime);
        if (rightIndex < 0) rightIndex = 0;
        const right = track[rightIndex];
        const left = rightIndex > 0 ? track[rightIndex - 1] : track[track.length - 1];
        const leftTime = rightIndex > 0 ? Number(left[0]) : Number(left[0]) - clipDuration;
        const rightTime = rightIndex > 0 ? Number(right[0]) : Number(right[0]) + clipDuration;
        const sampleTime = rightIndex > 0 ? localTime : localTime + clipDuration;
        const amount = Math.max(0, Math.min(1, (sampleTime - leftTime) / Math.max(1e-6, rightTime - leftTime)));
        const q = quaternionSlerp([left[1], left[2], left[3], left[4]], [right[1], right[2], right[3], right[4]], amount);
        return m4FromQuatTranslation(
          q[0], q[1], q[2], q[3],
          Number(left[5]) + (Number(right[5]) - Number(left[5])) * amount,
          Number(left[6]) + (Number(right[6]) - Number(left[6])) * amount,
          Number(left[7]) + (Number(right[7]) - Number(left[7])) * amount,
        );
      }
      function applyOriginalSkinning(model, clip, animationTime) {
        const skinning = model && model.skinning;
        const bones = skinning && skinning.bones;
        const geometrySkins = skinning && skinning.geometry_skins;
        const tracks = clip && clip.tracks;
        if (!model || !model.sourcePositions || !model.sourceNormals || !bones || !geometrySkins || !tracks) return false;
        if (Number(clip.node_count || 0) !== bones.length || tracks.length !== bones.length) return false;
        const localMatrices = new Array(bones.length);
        const worldMatrices = new Array(bones.length);
        for (let boneIndex = 0; boneIndex < bones.length; boneIndex += 1) {
          const bone = bones[boneIndex];
          localMatrices[boneIndex] = sampleAnimationTrack(tracks[boneIndex], clip.duration, animationTime) || bindMatrixForBone(bone);
          const parentIndex = Number(bone.parent_index);
          worldMatrices[boneIndex] = parentIndex >= 0 && worldMatrices[parentIndex]
            ? m4Multiply(worldMatrices[parentIndex], localMatrices[boneIndex])
            : localMatrices[boneIndex];
        }

        const skinnedPositions = new Float32Array(model.basePositions);
        const skinnedNormals = new Float32Array(model.baseNormals);
        const bounds = model.sourceBounds || {};
        const min = bounds.min || [0, 0, 0];
        const max = bounds.max || [0, 0, 0];
        const centerX = (Number(min[0]) + Number(max[0])) * .5;
        const centerY = (Number(min[1]) + Number(max[1])) * .5;
        const minZ = Number(min[2]);
        let vertexOffset = 0;
        let maxDisplacement = 0;
        for (const geometrySkin of geometrySkins) {
          const palettes = (geometrySkin.inverse_bind_matrices || []).map((inverseBind, boneIndex) => {
            const world = worldMatrices[boneIndex] || m4Identity();
            return m4Multiply(world, new Float32Array(inverseBind));
          });
          const vertexCount = Number(geometrySkin.vertex_count || 0);
          for (let vertexIndex = 0; vertexIndex < vertexCount; vertexIndex += 1) {
            const sourceIndex = (vertexOffset + vertexIndex) * 3;
            const sourcePosition = [
              model.sourcePositions[sourceIndex],
              model.sourcePositions[sourceIndex + 1],
              model.sourcePositions[sourceIndex + 2],
            ];
            const sourceNormal = [
              model.sourceNormals[sourceIndex],
              model.sourceNormals[sourceIndex + 1],
              model.sourceNormals[sourceIndex + 2],
            ];
            const indices = (geometrySkin.bone_indices || [])[vertexIndex] || [];
            const weights = (geometrySkin.weights || [])[vertexIndex] || [];
            let px = 0, py = 0, pz = 0;
            let nx = 0, ny = 0, nz = 0;
            let totalWeight = 0;
            for (let influence = 0; influence < 4; influence += 1) {
              const weight = Number(weights[influence] || 0);
              const palette = palettes[Number(indices[influence])];
              if (weight <= 0 || !palette) continue;
              const point = m4TransformPoint(palette, sourcePosition[0], sourcePosition[1], sourcePosition[2]);
              const normal = m4TransformDirection(palette, sourceNormal[0], sourceNormal[1], sourceNormal[2]);
              px += point[0] * weight; py += point[1] * weight; pz += point[2] * weight;
              nx += normal[0] * weight; ny += normal[1] * weight; nz += normal[2] * weight;
              totalWeight += weight;
            }
            if (totalWeight <= 1e-6) continue;
            const normal = normalize([nx, ny, nz]);
            skinnedPositions[sourceIndex] = px - centerX;
            skinnedPositions[sourceIndex + 1] = pz - minZ;
            skinnedPositions[sourceIndex + 2] = -(py - centerY);
            skinnedNormals[sourceIndex] = normal[0];
            skinnedNormals[sourceIndex + 1] = normal[2];
            skinnedNormals[sourceIndex + 2] = -normal[1];
            maxDisplacement = Math.max(
              maxDisplacement,
              Math.hypot(
                skinnedPositions[sourceIndex] - model.basePositions[sourceIndex],
                skinnedPositions[sourceIndex + 1] - model.basePositions[sourceIndex + 1],
                skinnedPositions[sourceIndex + 2] - model.basePositions[sourceIndex + 2],
              )
            );
          }
          vertexOffset += vertexCount;
        }
        gl.bindBuffer(gl.ARRAY_BUFFER, model.positionBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, skinnedPositions, gl.DYNAMIC_DRAW);
        gl.bindBuffer(gl.ARRAY_BUFFER, model.normalBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, skinnedNormals, gl.DYNAMIC_DRAW);
        model.lastSkinMaxDisplacement = maxDisplacement;
        return true;
      }
      function applyOriginalRigidAnimation(model, clip, animationTime) {
        const objectFrames = model && model.objectFrames;
        const skeleton = objectFrames && objectFrames.animation_skeleton;
        const bones = skeleton && skeleton.bones;
        const geometryRanges = objectFrames && objectFrames.geometry_ranges;
        const tracks = clip && clip.tracks;
        if (!model || !model.sourcePositions || !model.sourceNormals || !bones || !geometryRanges || !tracks) return false;
        if (Number(clip.node_count || 0) !== bones.length || tracks.length !== bones.length) return false;
        const worldMatrices = new Array(bones.length);
        for (let boneIndex = 0; boneIndex < bones.length; boneIndex += 1) {
          const bone = bones[boneIndex];
          const bindLocal = bindMatrixForBone(bone);
          const initial = sampleAnimationTrack(tracks[boneIndex], clip.duration, 0) || bindLocal;
          const sampled = sampleAnimationTrack(tracks[boneIndex], clip.duration, animationTime) || initial;
          // Rigid building ANMs encode motion relative to their first pose. Anchor
          // that delta to the DFF bind frame, otherwise the whole model is moved.
          const local = m4Multiply(bindLocal, m4Multiply(sampled, m4AffineInverse(initial)));
          const parentIndex = Number(bone.parent_index);
          worldMatrices[boneIndex] = parentIndex >= 0 && worldMatrices[parentIndex]
            ? m4Multiply(worldMatrices[parentIndex], local)
            : local;
        }
        const rigidPositions = new Float32Array(model.basePositions);
        const rigidNormals = new Float32Array(model.baseNormals);
        const bounds = model.sourceBounds || {};
        const min = bounds.min || [0, 0, 0];
        const max = bounds.max || [0, 0, 0];
        const centerX = (Number(min[0]) + Number(max[0])) * .5;
        const centerY = (Number(min[1]) + Number(max[1])) * .5;
        const minZ = Number(min[2]);
        let maxDisplacement = 0;
        for (const geometryRange of geometryRanges) {
          const boneIndex = Number(geometryRange.bone_index);
          const matrix = worldMatrices[boneIndex];
          if (!matrix) continue;
          const vertexOffset = Number(geometryRange.vertex_offset || 0);
          const vertexCount = Number(geometryRange.vertex_count || 0);
          for (let vertexIndex = 0; vertexIndex < vertexCount; vertexIndex += 1) {
            const sourceIndex = (vertexOffset + vertexIndex) * 3;
            const point = m4TransformPoint(
              matrix,
              model.sourcePositions[sourceIndex],
              model.sourcePositions[sourceIndex + 1],
              model.sourcePositions[sourceIndex + 2],
            );
            const rawNormal = m4TransformDirection(
              matrix,
              model.sourceNormals[sourceIndex],
              model.sourceNormals[sourceIndex + 1],
              model.sourceNormals[sourceIndex + 2],
            );
            const normal = normalize(rawNormal);
            rigidPositions[sourceIndex] = point[0] - centerX;
            rigidPositions[sourceIndex + 1] = point[2] - minZ;
            rigidPositions[sourceIndex + 2] = -(point[1] - centerY);
            rigidNormals[sourceIndex] = normal[0];
            rigidNormals[sourceIndex + 1] = normal[2];
            rigidNormals[sourceIndex + 2] = -normal[1];
            maxDisplacement = Math.max(
              maxDisplacement,
              Math.hypot(
                rigidPositions[sourceIndex] - model.basePositions[sourceIndex],
                rigidPositions[sourceIndex + 1] - model.basePositions[sourceIndex + 1],
                rigidPositions[sourceIndex + 2] - model.basePositions[sourceIndex + 2],
              )
            );
          }
        }
        gl.bindBuffer(gl.ARRAY_BUFFER, model.positionBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, rigidPositions, gl.DYNAMIC_DRAW);
        gl.bindBuffer(gl.ARRAY_BUFFER, model.normalBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, rigidNormals, gl.DYNAMIC_DRAW);
        model.lastRigidMaxDisplacement = maxDisplacement;
        return true;
      }
      function restoreModelBindPose(model) {
        if (!model || !model.basePositions || !model.baseNormals) return;
        gl.bindBuffer(gl.ARRAY_BUFFER, model.positionBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, model.basePositions, gl.DYNAMIC_DRAW);
        gl.bindBuffer(gl.ARRAY_BUFFER, model.normalBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, model.baseNormals, gl.DYNAMIC_DRAW);
      }

      function m4Multiply(a, b) {
        const out = new Float32Array(16);
        for (let col = 0; col < 4; col++) {
          for (let row = 0; row < 4; row++) {
            out[col * 4 + row] =
              a[0 * 4 + row] * b[col * 4 + 0] +
              a[1 * 4 + row] * b[col * 4 + 1] +
              a[2 * 4 + row] * b[col * 4 + 2] +
              a[3 * 4 + row] * b[col * 4 + 3];
          }
        }
        return out;
      }
      function m4Ortho(left, right, bottom, top, near, far) {
        return new Float32Array([
          2 / (right - left), 0, 0, 0,
          0, 2 / (top - bottom), 0, 0,
          0, 0, -2 / (far - near), 0,
          -(right + left) / (right - left), -(top + bottom) / (top - bottom), -(far + near) / (far - near), 1,
        ]);
      }
      function normalize(v) {
        const len = Math.hypot(v[0], v[1], v[2]) || 1;
        return [v[0] / len, v[1] / len, v[2] / len];
      }
      function cross(a, b) {
        return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
      }
      function dot(a, b) {
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
      }
      function m4LookAt(eye, target, up) {
        const z = normalize([eye[0] - target[0], eye[1] - target[1], eye[2] - target[2]]);
        const x = normalize(cross(up, z));
        const y = cross(z, x);
        return new Float32Array([
          x[0], y[0], z[0], 0,
          x[1], y[1], z[1], 0,
          x[2], y[2], z[2], 0,
          -dot(x, eye), -dot(y, eye), -dot(z, eye), 1,
        ]);
      }
      function m4Transform(x, y, z, s, yaw = 0, scaleY = 1) {
        const c = Math.cos(yaw);
        const r = Math.sin(yaw);
        const sy = s * Math.max(0.25, Number(scaleY || 1));
        return new Float32Array([
          c * s, 0, -r * s, 0,
          0, sy, 0, 0,
          r * s, 0, c * s, 0,
          x, y, z, 1,
        ]);
      }
      function animationInfoFor(entity) {
        const role = String(entity.anim_role || '').toLowerCase();
        const entry = animationByKey[entity.sprite_key] || {};
        const byRole = entry.by_role || {};
        return byRole[role] || byRole.walk || byRole.work || byRole.idle || null;
      }
      function defaultAnimationDuration(role) {
        if (role === 'walk') return 1.0;
        if (role === 'run') return 0.7;
        if (role === 'work') return 1.2;
        return 2.4;
      }
      function entityMotion(entity, frameTime, usingOriginalAnimation = false) {
        const role = String(entity.anim_role || '').toLowerCase();
        const state = String(entity.state || '').toLowerCase();
        const info = animationInfoFor(entity);
        const duration = Math.max(0.18, Number((info && info.duration) || defaultAnimationDuration(role)));
        const seed = Number(entity.anim_seed || 0) / 1000;
        const phase = (((Number(frameTime || 0) + seed) % duration) / duration) * Math.PI * 2;
        let yaw = Number(entity.angle || 0);
        let y = 0;
        let scaleY = 1;
        if (usingOriginalAnimation) {
          return { yaw, y, scaleY, duration, source: info ? info.name : '' };
        }
        if (role === 'walk' || role === 'run' || state.includes('walking')) {
          const stride = role === 'run' ? 2.5 : 2.0;
          y = Math.abs(Math.sin(phase * stride)) * (role === 'run' ? 5.0 : 3.4);
          scaleY = 1.0 + Math.sin(phase * stride + 1.1) * 0.025;
        } else if (role === 'work' || state.includes('working') || state.includes('building') || state.includes('extracting')) {
          yaw += Math.sin(phase) * 0.11;
          y = Math.max(0, Math.sin(phase * 2.0)) * 1.8;
          scaleY = 1.0 + Math.sin(phase * 2.0 + 0.6) * 0.018;
        } else if (role === 'idle') {
          scaleY = 1.0 + Math.sin(phase) * 0.01;
        }
        return { yaw, y, scaleY, duration, source: info ? info.name : '' };
      }
      function terrainHeightAt(frameX, frameY) {
        if (!terrain3d.enabled || !terrainRows || !terrainCols || !terrainPositions.length) return 0;
        const worldX = Number(frameX || 0) - MAP_WIDTH / 2;
        const worldZ = Number(frameY || 0) - MAP_HEIGHT / 2;
        const col = Math.max(0, Math.min(terrainCols - 1, Math.round(((worldX - terrainXMin) / Math.max(1, terrainXMax - terrainXMin)) * (terrainCols - 1))));
        const row = Math.max(0, Math.min(terrainRows - 1, Math.round(((worldZ - terrainZMin) / Math.max(1, terrainZMax - terrainZMin)) * (terrainRows - 1))));
        const index = (row * terrainCols + col) * 3 + 1;
        return Number(terrainPositions[index] || 0);
      }
      function projectWorldToCanvas(vp, x, y, z) {
        const clipX = vp[0] * x + vp[4] * y + vp[8] * z + vp[12];
        const clipY = vp[1] * x + vp[5] * y + vp[9] * z + vp[13];
        const clipZ = vp[2] * x + vp[6] * y + vp[10] * z + vp[14];
        const clipW = vp[3] * x + vp[7] * y + vp[11] * z + vp[15];
        if (!Number.isFinite(clipW) || Math.abs(clipW) < 1e-6) return null;
        const ndcX = clipX / clipW;
        const ndcY = clipY / clipW;
        const ndcZ = clipZ / clipW;
        if (ndcX < -1.15 || ndcX > 1.15 || ndcY < -1.15 || ndcY > 1.15 || ndcZ < -1.25 || ndcZ > 1.25) {
          return null;
        }
        return {
          x: ((ndcX + 1) * 0.5) * canvas.clientWidth,
          y: ((1 - ndcY) * 0.5) * canvas.clientHeight,
          z: ndcZ,
        };
      }
      function entityScreenPoint(entity, vp) {
        const worldX = Number(entity.x || 0) - MAP_WIDTH / 2;
        const worldZ = Number(entity.y || 0) - MAP_HEIGHT / 2;
        const groundY = terrainHeightAt(entity.x, entity.y);
        const lift = Math.max(8, Number(entity.size || 32) * 0.28);
        return projectWorldToCanvas(vp, worldX, groundY + lift, worldZ);
      }
      function projectEntity(entity) {
        resize();
        return entityScreenPoint(entity, cameraMatrix());
      }
      function pickEntity(screenX, screenY, frame) {
        resize();
        const vp = cameraMatrix();
        const entities = ((frame && frame.entities) || []).slice().sort((a, b) => Number(b.y || 0) - Number(a.y || 0));
        let best = null;
        let bestScore = Infinity;
        for (const entity of entities) {
          const modelUrl = model3dByKey[entity.sprite_key];
          if (!modelUrl) continue;
          const point = entityScreenPoint(entity, vp);
          if (!point) continue;
          const radius = Math.max(18, Math.min(58, Number(entity.size || 32) * 0.62));
          const dx = point.x - screenX;
          const dy = point.y - screenY;
          const distance = Math.hypot(dx, dy);
          if (distance > radius) continue;
          const score = distance + Math.max(0, point.z + 1) * 3;
          if (score < bestScore) {
            bestScore = score;
            best = entity;
          }
        }
        canvas.dataset.lastPick = best ? best.id : "";
        return best;
      }
      function pickEntitiesInRect(left, top, right, bottom, frame) {
        resize();
        const vp = cameraMatrix();
        const minX = Math.min(left, right);
        const maxX = Math.max(left, right);
        const minY = Math.min(top, bottom);
        const maxY = Math.max(top, bottom);
        const ids = [];
        const entities = ((frame && frame.entities) || []).slice().sort((a, b) => Number(a.y || 0) - Number(b.y || 0));
        for (const entity of entities) {
          const modelUrl = model3dByKey[entity.sprite_key];
          if (!modelUrl) continue;
          const point = entityScreenPoint(entity, vp);
          if (!point) continue;
          if (point.x >= minX && point.x <= maxX && point.y >= minY && point.y <= maxY) {
            ids.push(entity.id);
          }
        }
        canvas.dataset.lastBoxPickCount = String(ids.length);
        return ids;
      }

      function resize() {
        const width = Math.max(1, stage.clientWidth);
        const height = Math.max(1, stage.clientHeight);
        const dpr = Math.min(2, window.devicePixelRatio || 1);
        const targetW = Math.floor(width * dpr);
        const targetH = Math.floor(height * dpr);
        if (canvas.width !== targetW || canvas.height !== targetH) {
          canvas.width = targetW;
          canvas.height = targetH;
        }
        canvas.style.width = `${width}px`;
        canvas.style.height = `${height}px`;
        gl.viewport(0, 0, canvas.width, canvas.height);
      }

      function cameraMatrix() {
        const centerX = (stage.clientWidth / 2 - tx) / scale - MAP_WIDTH / 2;
        const centerZ = (stage.clientHeight / 2 - ty) / scale - MAP_HEIGHT / 2;
        const viewW = stage.clientWidth / Math.max(0.1, scale);
        const viewH = stage.clientHeight / Math.max(0.1, scale);
        const distance = Math.max(620, viewH * 1.08);
        const horizontalDistance = distance * Math.cos(cameraPitch);
        const eye = [
          centerX + Math.sin(cameraYaw) * horizontalDistance,
          distance * Math.sin(cameraPitch),
          centerZ + Math.cos(cameraYaw) * horizontalDistance,
        ];
        const target = [centerX, 0, centerZ];
        const view = m4LookAt(eye, target, [0, 1, 0]);
        const proj = m4Ortho(-viewW / 2, viewW / 2, -viewH / 2, viewH / 2, 1, 6000);
        return m4Multiply(proj, view);
      }

      function bindMesh(mesh) {
        gl.bindBuffer(gl.ARRAY_BUFFER, mesh.positionBuffer);
        gl.enableVertexAttribArray(locations.position);
        gl.vertexAttribPointer(locations.position, 3, gl.FLOAT, false, 0, 0);
        gl.bindBuffer(gl.ARRAY_BUFFER, mesh.normalBuffer);
        gl.enableVertexAttribArray(locations.normal);
        gl.vertexAttribPointer(locations.normal, 3, gl.FLOAT, false, 0, 0);
        gl.bindBuffer(gl.ARRAY_BUFFER, mesh.uvBuffer);
        gl.enableVertexAttribArray(locations.uv);
        gl.vertexAttribPointer(locations.uv, 2, gl.FLOAT, false, 0, 0);
      }

      function drawSubmesh(vp, mesh, submesh, matrix) {
        gl.uniformMatrix4fv(locations.matrix, false, m4Multiply(vp, matrix));
        gl.uniformMatrix4fv(locations.world, false, matrix);
        gl.uniform3f(locations.lightDir, -0.42, 0.72, 0.54);
        gl.uniform1f(locations.ambient, 0.48);
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, submesh.texture.texture);
        gl.uniform1i(locations.texture, 0);
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, submesh.indexBuffer);
        gl.drawElements(gl.TRIANGLES, submesh.count, submesh.indexType || gl.UNSIGNED_SHORT, 0);
      }

      function render(frame) {
        resize();
        gl.useProgram(program);
        gl.enable(gl.DEPTH_TEST);
        gl.enable(gl.BLEND);
        gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
        gl.disable(gl.CULL_FACE);
        gl.clearColor(0.10, 0.12, 0.12, 1);
        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
        const vp = cameraMatrix();

        const mapTexture = createTexture(terrainTexture || ((frame && frame.frame) || ''));
        bindMesh(terrainBackplate);
        drawSubmesh(vp, terrainBackplate, { indexBuffer: terrainBackplate.indexBuffer, indexType: terrainBackplate.indexType, count: terrainBackplate.count, texture: mapTexture }, new Float32Array([
          1, 0, 0, 0,
          0, 1, 0, 0,
          0, 0, 1, 0,
          0, 0, 0, 1,
        ]));

        bindMesh(terrainMesh);
        drawSubmesh(vp, terrainMesh, { indexBuffer: terrainMesh.indexBuffer, indexType: terrainMesh.indexType, count: terrainMesh.count, texture: mapTexture }, new Float32Array([
          1, 0, 0, 0,
          0, 1, 0, 0,
          0, 0, 1, 0,
          0, 0, 0, 1,
        ]));

        const entities = ((frame && frame.entities) || []).slice().sort((a, b) => Number(a.y || 0) - Number(b.y || 0));
        let drawnModels = 0;
        let originalAnimationDrawn = 0;
        let originalRigidAnimationDrawn = 0;
        let originalAnimationPending = 0;
        let originalAnimationMaxDisplacement = 0;
        for (const entity of entities) {
          const modelUrl = model3dByKey[entity.sprite_key];
          const record = ensureModel(modelUrl);
          if (!record || !record.loaded || !record.model) continue;
          const model = record.model;
          const worldX = Number(entity.x || 0) - MAP_WIDTH / 2;
          const worldZ = Number(entity.y || 0) - MAP_HEIGHT / 2;
          const groundY = terrainHeightAt(entity.x, entity.y);
          const isSelected3d = selectedEntityIds.has(entity.id);
          const isHovered3d = entity.id === hoveredEntityId && !isSelected3d;
          bindMesh(selectionMesh);
          const shadowScale = Math.max(16, Number(entity.size || 32) * (entity.kind === 'building' || entity.kind === 'site' ? 0.68 : 0.46));
          const shadowMatrix = m4Transform(worldX, groundY + 0.85, worldZ, shadowScale, Number(entity.angle || 0), 1);
          drawSubmesh(
            vp,
            selectionMesh,
            {
              indexBuffer: selectionMesh.indexBuffer,
              indexType: selectionMesh.indexType,
              count: selectionMesh.count,
              texture: shadowTexture,
            },
            shadowMatrix
          );
          if (isSelected3d || isHovered3d) {
            bindMesh(selectionMesh);
            const ringScale = Math.max(22, Number(entity.size || 32) * (isSelected3d ? 0.68 : 0.58));
            const ringMatrix = m4Transform(worldX, groundY + 2.2, worldZ, ringScale, Number(entity.angle || 0), 1);
            drawSubmesh(
              vp,
              selectionMesh,
              {
                indexBuffer: selectionMesh.indexBuffer,
                indexType: selectionMesh.indexType,
                count: selectionMesh.count,
                texture: isSelected3d ? selectionTexture : hoverTexture,
              },
              ringMatrix
            );
          }
          const animationInfo = animationInfoFor(entity);
          const canAnimateEntity = Boolean(model.skinning) || Boolean(
            allowRigidAtomicAnimation
            && model.objectFrames
            && model.objectFrames.animation_skeleton
            && (model.objectFrames.animation_skeleton.bones || []).length
          );
          const animationRecord = canAnimateEntity && animationInfo && animationInfo.track_data
            ? ensureAnimation(animationInfo.track_data)
            : null;
          let usingOriginalAnimation = false;
          if (animationRecord && animationRecord.loaded && animationRecord.data) {
            const duration = Math.max(0.001, Number(animationRecord.data.duration || animationInfo.duration || 1));
            const seedOffset = (Number(entity.anim_seed || 0) / 1000) * duration;
            // Units may start the same walk cycle at different phases. Building
            // atomics instead share the simulation clock, as in the original.
            const animationTime = Number((frame && frame.time) || 0) + (model.skinning ? seedOffset : 0);
            usingOriginalAnimation = model.skinning
              ? applyOriginalSkinning(model, animationRecord.data, animationTime)
              : applyOriginalRigidAnimation(model, animationRecord.data, animationTime);
          } else if (model.skinning || (allowRigidAtomicAnimation && model.objectFrames)) {
            restoreModelBindPose(model);
            if (animationRecord && !animationRecord.error) originalAnimationPending += 1;
          }
          if (usingOriginalAnimation) {
            originalAnimationDrawn += 1;
            originalAnimationMaxDisplacement = Math.max(originalAnimationMaxDisplacement, Number(model.lastSkinMaxDisplacement || 0));
            originalAnimationMaxDisplacement = Math.max(originalAnimationMaxDisplacement, Number(model.lastRigidMaxDisplacement || 0));
            if (model.objectFrames && !model.skinning) originalRigidAnimationDrawn += 1;
          }
          bindMesh(model);
          if (cullEntityModels) {
            gl.enable(gl.CULL_FACE);
            gl.cullFace(gl.BACK);
            gl.frontFace(gl.CCW);
          } else {
            gl.disable(gl.CULL_FACE);
          }
          const modelScale = Math.max(0.08, (Number(entity.size || 32) * 1.45) / Math.max(1, model.maxSpan));
          const motion = entityMotion(entity, frame && frame.time, usingOriginalAnimation);
          const matrix = m4Transform(worldX, groundY + motion.y, worldZ, modelScale, motion.yaw, motion.scaleY);
          for (const submesh of model.submeshes) {
            if (submesh.count > 0) drawSubmesh(vp, model, submesh, matrix);
          }
          gl.disable(gl.CULL_FACE);
          drawnModels += 1;
        }
        lastStats = {
          drawnModels,
          totalEntities: entities.length,
          modelsCached: modelCache.size,
          modelsLoaded: Array.from(modelCache.values()).filter(record => record.loaded).length,
          modelErrors: Array.from(modelCache.values()).filter(record => record.error).length,
          texturesCached: textureCache.size,
          terrain: terrain3d.enabled ? `${terrainRows}x${terrainCols}` : 'flat',
          animation: originalAnimationDrawn
            ? (originalRigidAnimationDrawn ? 'original_hanim_cpu_skinning_and_rigid_atomics' : 'original_hanim_cpu_skinning')
            : (Object.keys(animationByKey).length ? 'anm_timing_state_motion' : 'state_motion'),
          originalAnimationDrawn,
          originalRigidAnimationDrawn,
          originalAnimationPending,
          originalAnimationMaxDisplacement: Math.round(originalAnimationMaxDisplacement * 1000) / 1000,
          originalAnimationAssets: Array.from(animationCache.values()).filter(record => record.loaded).length,
          originalAnimationErrors: Array.from(animationCache.values()).filter(record => record.error).length,
          orientedEntities: entities.filter(entity => entity.orientation_deg !== undefined).length,
          selectedEntity: selectedEntityId || "",
          selectedEntities: Array.from(selectedEntityIds).join(","),
          selectionCount: selectedEntityIds.size,
          hoveredEntity: hoveredEntityId || "",
          cameraYawDeg: Math.round((cameraYaw * 180 / Math.PI) * 10) / 10,
          cameraPitchDeg: Math.round((cameraPitch * 180 / Math.PI) * 10) / 10,
          canvas: [canvas.width, canvas.height, canvas.clientWidth, canvas.clientHeight],
        };
        canvas.dataset.drawnModels = String(lastStats.drawnModels);
        canvas.dataset.totalEntities = String(lastStats.totalEntities);
        canvas.dataset.modelsCached = String(lastStats.modelsCached);
        canvas.dataset.modelsLoaded = String(lastStats.modelsLoaded);
        canvas.dataset.modelErrors = String(lastStats.modelErrors);
        canvas.dataset.texturesCached = String(lastStats.texturesCached);
        canvas.dataset.terrain = String(lastStats.terrain);
        canvas.dataset.lighting = "directional_normals";
        canvas.dataset.animation = String(lastStats.animation);
        canvas.dataset.animationKeys = String(Object.keys(animationByKey).length);
        canvas.dataset.originalAnimationDrawn = String(lastStats.originalAnimationDrawn);
        canvas.dataset.originalRigidAnimationDrawn = String(lastStats.originalRigidAnimationDrawn);
        canvas.dataset.originalAnimationPending = String(lastStats.originalAnimationPending);
        canvas.dataset.originalAnimationMaxDisplacement = String(lastStats.originalAnimationMaxDisplacement);
        canvas.dataset.originalAnimationAssets = String(lastStats.originalAnimationAssets);
        canvas.dataset.originalAnimationErrors = String(lastStats.originalAnimationErrors);
        canvas.dataset.orientedEntities = String(lastStats.orientedEntities);
        canvas.dataset.selectedEntity = String(lastStats.selectedEntity);
        canvas.dataset.selectedEntities = String(lastStats.selectedEntities);
        canvas.dataset.selectionCount = String(lastStats.selectionCount);
        canvas.dataset.hoveredEntity = String(lastStats.hoveredEntity);
        canvas.dataset.cameraYawDeg = String(lastStats.cameraYawDeg);
        canvas.dataset.cameraPitchDeg = String(lastStats.cameraPitchDeg);
      }

      let renderQueued = false;
      function requestRender() {
        if (!mode3d || renderQueued) return;
        renderQueued = true;
        requestAnimationFrame(() => {
          renderQueued = false;
          render(timeline[idx]);
        });
      }

      return {
        render,
        requestRender,
        pickEntity,
        pickEntitiesInRect,
        projectEntity,
        stats: () => lastStats,
        setModelCulling(value) { cullEntityModels = Boolean(value); },
      };
    }
    function selectionFallbackSrc(entity) {
      if (!entity) return assetByKey.serf || '';
      if (entity.kind === 'serf') return spriteByKey[entity.sprite_key] || assetByKey.serf || '';
      if (entity.kind === 'worker') return spriteByKey[entity.sprite_key] || assetByKey.worker || '';
      if (entity.kind === 'tree') return spriteByKey[entity.sprite_key] || assetByKey.wood || '';
      if (entity.kind === 'resource' || entity.kind === 'shaft') return spriteByKey[entity.sprite_key] || assetByKey.mine || assetByKey.stone || '';
      if (entity.kind === 'site') return spriteByKey[entity.sprite_key] || assetByKey.site || '';
      return spriteByKey[entity.sprite_key] || assetByKey.generic_building || assetByKey.headquarter || '';
    }
    function renderSelection() {
      const entity = selectedEntity();
      const entities = selectedEntities();
      if (!entities.length) {
        selectedTitle.textContent = 'Keine Auswahl';
        selectedMeta.textContent = '';
        selectedCoords.textContent = '';
        selectedPortrait.src = assetByKey.serf || '';
        return;
      }
      if (entities.length > 1) {
        const bounds = selectionBounds(entities);
        selectedTitle.textContent = `${entities.length} Entitaeten ausgewaehlt`;
        selectedMeta.textContent = selectedKindSummary(entities);
        selectedCoords.textContent = bounds
          ? `Bereich x=${Math.round(bounds.minX)}-${Math.round(bounds.maxX)} y=${Math.round(bounds.minY)}-${Math.round(bounds.maxY)}`
          : 'Mehrfachauswahl';
        selectedPortrait.src = entity ? selectionFallbackSrc(entity) : (assetByKey.serf || '');
        setMessage(`${entities.length} Entitaeten ausgewaehlt`, assetByKey.onscreen_worker || selectedPortrait.src);
        return;
      }
      selectedTitle.textContent = entity.label || entity.kind || entity.id;
      selectedMeta.textContent = `${entity.kind || ''} ${entity.state || ''}`.trim();
      selectedCoords.textContent = `x=${Math.round(Number(entity.x || 0))} y=${Math.round(Number(entity.y || 0))}`;
      selectedPortrait.src = selectionFallbackSrc(entity);
      setMessage(entity.label || entity.id, entity.kind === 'serf' ? (assetByKey.onscreen_serf || selectedPortrait.src) : (assetByKey.onscreen_worker || selectedPortrait.src));
    }
    function selectEntity(id, focus = false, additive = false) {
      if (!id || !entityData.has(id)) {
        if (!additive) applySelection([], null, false);
        return;
      }
      if (!additive) {
        applySelection([id], id, focus);
        return;
      }
      const ids = normalizeSelection(Array.from(selectedEntityIds));
      const index = ids.indexOf(id);
      if (index >= 0) {
        ids.splice(index, 1);
        applySelection(ids, selectedEntityId === id ? null : selectedEntityId, focus);
      } else {
        ids.push(id);
        applySelection(ids, id, focus);
      }
    }
    function cycleEntity(direction) {
      const current = timeline[idx] || {};
      const entities = current.entities || [];
      if (!entities.length) return;
      const currentIndex = Math.max(0, entities.findIndex(entity => entity.id === selectedEntityId));
      const nextIndex = (currentIndex + direction + entities.length) % entities.length;
      selectEntity(entities[nextIndex].id, true);
    }
    function updateEntities(f) {
      const keep = new Set();
      entityData.clear();
      const duration = timer ? Math.max(120, Number(speed.value) * .88) : 120;
      for (const entity of (f.entities || [])) {
        const id = entity.id;
        keep.add(id);
        entityData.set(id, entity);
        let node = entityNodes.get(id);
        const src = entitySpriteSrc(entity);
        if (!src) continue;
        if (!node) {
          node = document.createElement('img');
          node.decoding = 'async';
          node.loading = 'eager';
          node.draggable = false;
          entityLayer.appendChild(node);
          entityNodes.set(id, node);
          node.addEventListener('click', event => {
            event.stopPropagation();
            selectEntity(node.dataset.entityId, false, event.shiftKey || event.ctrlKey || event.metaKey);
          });
          node.addEventListener('dblclick', event => {
            event.stopPropagation();
            selectEntity(node.dataset.entityId, true, event.shiftKey || event.ctrlKey || event.metaKey);
          });
        }
        const previousX = Number(node.dataset.x || entity.x);
        const flip = Number(entity.x) < previousX ? -1 : 1;
        node.dataset.x = String(entity.x);
        node.dataset.entityId = id;
        if (node.getAttribute('src') !== src) node.src = src;
        const kindClass = sanitizeClass(entity.kind);
        const stateClass = sanitizeClass(entity.state);
        node.className = `entity-sprite ${kindClass} ${stateClass}`;
        node.alt = entity.label || entity.kind || '';
        node.title = entity.label || '';
        node.style.left = `${Number(entity.x || 0)}px`;
        node.style.top = `${Number(entity.y || 0)}px`;
        node.style.width = `${Number(entity.size || 32)}px`;
        node.style.height = `${Number(entity.size || 32)}px`;
        node.style.zIndex = String(1000 + Number(entity.y || 0));
        node.style.transitionProperty = 'left, top';
        node.style.transitionTimingFunction = 'linear';
        node.style.transitionDuration = `${duration}ms`;
        node.style.setProperty('--anchor-y', String(entity.anchor_y || .78));
        node.style.setProperty('--flip', String(flip));
        node.classList.toggle('selected', selectedEntityIds.has(id));
      }
      for (const [id, node] of entityNodes.entries()) {
        if (keep.has(id)) continue;
        node.remove();
        entityNodes.delete(id);
      }
      if (selectedEntityId && !entityData.has(selectedEntityId)) {
        selectedEntityId = null;
      }
      const aliveSelectedIds = normalizeSelection(Array.from(selectedEntityIds));
      selectedEntityIds = new Set(aliveSelectedIds);
      if (!selectedEntityId || !selectedEntityIds.has(selectedEntityId)) {
        selectedEntityId = aliveSelectedIds[0] || null;
      }
      if (hoveredEntityId && !entityData.has(hoveredEntityId)) {
        setHoveredEntity(null);
      }
      renderSelection();
    }
    function fit() {
      const sx = stage.clientWidth / MAP_WIDTH;
      const sy = stage.clientHeight / MAP_HEIGHT;
      scale = Math.min(sx, sy) * 0.98;
      tx = (stage.clientWidth - MAP_WIDTH * scale) / 2;
      ty = (stage.clientHeight - MAP_HEIGHT * scale) / 2;
      applyTransform();
    }
    function focusInitialCamera() {
      resetCameraAngles();
      const fullFit = Math.min(stage.clientWidth / MAP_WIDTH, stage.clientHeight / MAP_HEIGHT);
      scale = Math.max(fullFit * 1.05, INITIAL_CAMERA_SCALE);
      tx = stage.clientWidth / 2 - INITIAL_CAMERA_X * scale;
      ty = stage.clientHeight / 2 - INITIAL_CAMERA_Y * scale;
      applyTransform();
    }
    function updatePayday(f) {
      const main = document.getElementById('paydayMain');
      const sub = document.getElementById('paydaySub');
      if (paydayFrames.length && paydayIcon) {
        const cycle = 120;
        const remaining = f.payday_countdown === null || f.payday_countdown === undefined ? cycle : Number(f.payday_countdown);
        const phase = ((cycle - remaining) % cycle + cycle) % cycle;
        const frameIdx = Math.floor((phase / cycle) * paydayFrames.length);
        paydayIcon.src = paydayFrames[Math.max(0, Math.min(paydayFrames.length - 1, frameIdx))];
        paydayIcon.style.display = '';
      } else if (paydayIcon && !paydayIcon.getAttribute('src')) {
        paydayIcon.style.display = 'none';
      }
      if (f.next_payday == null) {
        main.textContent = 'nicht gesetzt';
        sub.textContent = 'Timer startet mit erstem Worker-Gebaeude';
      } else {
        main.textContent = `in ${fmtTime(f.payday_countdown)}`;
        const last = f.last_payday == null ? 'noch keiner' : `t=${f.last_payday}s`;
        sub.textContent = `naechster t=${f.next_payday}s, letzter ${last}, erster t=${f.first_payday}s`;
      }
      document.getElementById('taxLevel').textContent = f.tax_level;
    }
    function updateResources(f) {
      resIds.taler.textContent = fmt(f.taler);
      resIds.holz.textContent = fmt(f.holz);
      resIds.stein.textContent = fmt(f.stein);
      resIds.lehm.textContent = fmt(f.lehm);
      resIds.eisen.textContent = fmt(f.eisen);
      resIds.schwefel.textContent = fmt(f.schwefel);
      resIds.holz_roh.textContent = `Roh ${fmt(f.holz_roh)}`;
      resIds.stein_roh.textContent = `Roh ${fmt(f.stein_roh)}`;
      resIds.lehm_roh.textContent = `Roh ${fmt(f.lehm_roh)}`;
      resIds.eisen_roh.textContent = `Roh ${fmt(f.eisen_roh)}`;
      resIds.schwefel_roh.textContent = `Roh ${fmt(f.schwefel_roh)}`;
    }
    function show(i) {
      if (!timeline.length) return;
      idx = Math.max(0, Math.min(timeline.length - 1, i));
      const f = timeline[idx];
      img.src = f.frame;
      if (!mini.getAttribute('src')) mini.src = minimapTexture || f.frame;
      slider.value = idx;
      bottomSlider.value = idx;
      const lastDecision = timeline[timeline.length - 1].decision;
      headline.innerHTML = `<span class="playing-dot"></span>Simzeit ${fmtTime(f.time)}`;
      action.textContent = `Aktion ${f.decision}/${lastDecision}: ${f.action}`;
      bottomAction.textContent = `t=${fmtTime(f.time)} | ${f.action}`;
      setText('statBuildings', fmt(f.buildings));
      setText('statSites', fmt(f.sites));
      setText('statSerfs', fmt(f.serfs));
      setText('statWorkers', fmt(f.workers));
      updateResources(f);
      updatePayday(f);
      updateEntities(f);
      updateMinimap();
      updateMiniMarkers(f);
      if (mode3d && renderer3d) renderer3d.render(f);
      renderMovementTrails();
    }
    function step(delta) {
      show(idx + delta);
    }
    function stopPlayback() {
      if (!timer) return;
      clearInterval(timer);
      timer = null;
      playBtn.textContent = 'Play';
      bottomPlay.textContent = 'Play';
      playBtn.classList.remove('active');
      bottomPlay.classList.remove('active');
      stage.classList.remove('playing');
    }
    function play() {
      if (timer) {
        stopPlayback();
        return;
      }
      playBtn.textContent = 'Pause';
      bottomPlay.textContent = 'Pause';
      playBtn.classList.add('active');
      bottomPlay.classList.add('active');
      stage.classList.add('playing');
      timer = setInterval(() => {
        if (idx >= timeline.length - 1) {
          stopPlayback();
          return;
        }
        step(1);
      }, Number(speed.value));
    }
    function showSelectionRect(left, top, right, bottom) {
      const x = Math.min(left, right);
      const y = Math.min(top, bottom);
      const width = Math.abs(right - left);
      const height = Math.abs(bottom - top);
      selectionRect.style.left = `${x}px`;
      selectionRect.style.top = `${y}px`;
      selectionRect.style.width = `${width}px`;
      selectionRect.style.height = `${height}px`;
    }
    function hideSelectionRect() {
      stage.classList.remove('selecting');
      selectionRect.style.width = '0px';
      selectionRect.style.height = '0px';
    }
    function pick2dEntitiesInRect(left, top, right, bottom) {
      const minX = Math.min(left, right);
      const maxX = Math.max(left, right);
      const minY = Math.min(top, bottom);
      const maxY = Math.max(top, bottom);
      const ids = [];
      for (const entity of ((timeline[idx] || {}).entities || [])) {
        if (!entitySpriteSrc(entity)) continue;
        const screenX = Number(entity.x || 0) * scale + tx;
        const screenY = Number(entity.y || 0) * scale + ty;
        const radius = Math.max(10, Number(entity.size || 32) * scale * .36);
        if (screenX + radius < minX || screenX - radius > maxX) continue;
        if (screenY + radius < minY || screenY - radius > maxY) continue;
        ids.push(entity.id);
      }
      return ids;
    }
    function pickEntitiesInSelectionRect(left, top, right, bottom) {
      if (mode3d && renderer3d && renderer3d.pickEntitiesInRect) {
        return renderer3d.pickEntitiesInRect(left, top, right, bottom, timeline[idx]);
      }
      return pick2dEntitiesInRect(left, top, right, bottom);
    }
    function applyBoxSelection(left, top, right, bottom, additive) {
      const ids = pickEntitiesInSelectionRect(left, top, right, bottom);
      const nextIds = additive ? normalizeSelection([...selectedEntityIds, ...ids]) : ids;
      applySelection(nextIds, ids[0] || (additive ? selectedEntityId : null), false);
      if (ids.length) {
        setMessage(`${ids.length} Entitaeten markiert`, assetByKey.onscreen_worker || assetByKey.worker || '');
      }
    }
    document.getElementById('prev').onclick = () => step(-1);
    document.getElementById('next').onclick = () => step(1);
    playBtn.onclick = play;
    document.getElementById('bottomPrev').onclick = () => step(-1);
    document.getElementById('bottomNext').onclick = () => step(1);
    document.getElementById('bottomHQ').onclick = focusInitialCamera;
    bottomPlay.onclick = play;
    document.getElementById('cmdPrev').onclick = () => cycleEntity(-1);
    document.getElementById('cmdNext').onclick = () => cycleEntity(1);
    document.getElementById('cmdHQ').onclick = focusInitialCamera;
    document.getElementById('cmdTrails').onclick = () => {
      showAllTrails = !showAllTrails;
      document.getElementById('cmdTrails').classList.toggle('active', showAllTrails);
      renderMovementTrails();
      setMessage(showAllTrails ? 'Laufwege sichtbar' : 'Laufwege ausgeblendet', assetByKey.onscreen_worker || assetByKey.worker || '');
    };
    document.getElementById('cmdPlay').onclick = play;
    document.getElementById('cmdStepBack').onclick = () => step(-1);
    document.getElementById('cmdStepForward').onclick = () => step(1);
    document.getElementById('cmdZoomIn').onclick = () => zoomAt(stage.clientWidth / 2, stage.clientHeight / 2, 1.18);
    document.getElementById('cmdZoomOut').onclick = () => zoomAt(stage.clientWidth / 2, stage.clientHeight / 2, 1 / 1.18);
    document.getElementById('focusSelected').onclick = focusSelection;
    document.getElementById('clearSelected').onclick = () => selectEntity(null, false);
    fullscreenBtn.onclick = async () => {
      if (!document.fullscreenElement) {
        await document.documentElement.requestFullscreen();
      } else {
        await document.exitFullscreen();
      }
    };
    mode3dBtn.onclick = () => {
      mode3d = !mode3d;
      stage.classList.toggle('mode3d', mode3d);
      mode3dBtn.textContent = mode3d ? '2D' : '3D';
      mode3dBtn.classList.toggle('active', mode3d);
      if (mode3d && !renderer3d) {
        try {
          renderer3d = createReplay3DRenderer(webglScene);
          window.replay3dRenderer = renderer3d;
          webglScene.dataset.modelKeys = String(Object.keys(model3dByKey).length);
        } catch (error) {
          mode3d = false;
          stage.classList.remove('mode3d');
          mode3dBtn.textContent = '3D';
          setMessage('WebGL konnte nicht gestartet werden', assetByKey.onscreen_worker || assetByKey.worker || '');
          return;
        }
      }
      if (mode3d && renderer3d) {
        renderer3d.render(timeline[idx]);
        if (!suppressModeMessage) setMessage('3D-Ansicht aktiv', assetByKey.onscreen_worker || assetByKey.worker || '');
      } else {
        setHoveredEntity(null);
        if (!suppressModeMessage) setMessage('2D-Ansicht aktiv', assetByKey.onscreen_worker || assetByKey.worker || '');
      }
      renderMovementTrails();
    };
    speed.onchange = () => {
      if (!timer) return;
      stopPlayback();
      play();
    };
    slider.oninput = e => show(Number(e.target.value));
    bottomSlider.oninput = e => show(Number(e.target.value));
    document.getElementById('fit').onclick = focusInitialCamera;
    stage.addEventListener('wheel', e => {
      e.preventDefault();
      const rect = stage.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;
      zoomAt(mx, my, e.deltaY < 0 ? 1.15 : 1 / 1.15);
    }, { passive: false });
    miniBox.addEventListener('click', e => {
      const rect = miniBox.getBoundingClientRect();
      const area = minimapContentArea();
      const localX = clamp(e.clientX - rect.left - area.left, 0, area.width);
      const localY = clamp(e.clientY - rect.top - area.top, 0, area.height);
      const worldX = (localX / Math.max(1, area.width)) * MAP_WIDTH;
      const worldY = (localY / Math.max(1, area.height)) * MAP_HEIGHT;
      tx = stage.clientWidth / 2 - worldX * scale;
      ty = stage.clientHeight / 2 - worldY * scale;
      applyTransform();
    });
    stage.addEventListener('mousedown', e => {
      if (e.target.closest('.sidehud')) return;
      if (e.target.closest('.bottomhud')) return;
      if (e.target.closest('.entity-sprite')) return;
      if (mode3d && (e.button === 1 || e.button === 2 || e.altKey)) {
        e.preventDefault();
        rotatingCamera = true;
        stage.classList.add('dragging');
        lastX = e.clientX;
        lastY = e.clientY;
        return;
      }
      if (e.button === 0 && !e.altKey) {
        e.preventDefault();
        const rect = stage.getBoundingClientRect();
        selectingBox = true;
        selectionMoved = false;
        selectionStartX = e.clientX - rect.left;
        selectionStartY = e.clientY - rect.top;
        showSelectionRect(selectionStartX, selectionStartY, selectionStartX, selectionStartY);
        stage.classList.add('selecting');
        return;
      }
      e.preventDefault();
      dragging = true;
      stage.classList.add('dragging');
      lastX = e.clientX;
      lastY = e.clientY;
    });
    window.addEventListener('mouseup', e => {
      if (selectingBox) {
        const rect = stage.getBoundingClientRect();
        const endX = clamp(e.clientX - rect.left, 0, stage.clientWidth);
        const endY = clamp(e.clientY - rect.top, 0, stage.clientHeight);
        selectingBox = false;
        hideSelectionRect();
        if (selectionMoved) {
          suppressNextClick = true;
          applyBoxSelection(selectionStartX, selectionStartY, endX, endY, e.shiftKey || e.ctrlKey || e.metaKey);
        }
        return;
      }
      dragging = false;
      rotatingCamera = false;
      stage.classList.remove('dragging');
    });
    window.addEventListener('mousemove', e => {
      if (selectingBox) {
        const rect = stage.getBoundingClientRect();
        const endX = clamp(e.clientX - rect.left, 0, stage.clientWidth);
        const endY = clamp(e.clientY - rect.top, 0, stage.clientHeight);
        if (Math.hypot(endX - selectionStartX, endY - selectionStartY) > 5) {
          selectionMoved = true;
        }
        showSelectionRect(selectionStartX, selectionStartY, endX, endY);
        return;
      }
      if (!dragging && !rotatingCamera) return;
      if (rotatingCamera) {
        setHoveredEntity(null);
        rotateCamera((e.clientX - lastX) * 0.006, -(e.clientY - lastY) * 0.004);
        lastX = e.clientX;
        lastY = e.clientY;
        return;
      }
      setHoveredEntity(null);
      tx += e.clientX - lastX;
      ty += e.clientY - lastY;
      lastX = e.clientX;
      lastY = e.clientY;
      applyTransform();
    });
    stage.addEventListener('mousemove', e => {
      const rect = stage.getBoundingClientRect();
      mouseX = e.clientX - rect.left;
      mouseY = e.clientY - rect.top;
      if (mode3d && renderer3d && !dragging && !rotatingCamera && !selectingBox) {
        const hovered = renderer3d.pickEntity(mouseX, mouseY, timeline[idx]);
        setHoveredEntity(hovered ? hovered.id : null);
      }
    });
    stage.addEventListener('mouseenter', () => {
      edgePanActive = true;
      if (!edgePanFrame) edgePanLoop();
    });
    stage.addEventListener('mouseleave', () => {
      edgePanActive = false;
      setHoveredEntity(null);
    });
    stage.addEventListener('click', e => {
      if (suppressNextClick) {
        suppressNextClick = false;
        return;
      }
      if (e.target.closest('.sidehud') || e.target.closest('.bottomhud') || e.target.closest('.entity-sprite')) return;
      if (mode3d && renderer3d) {
        const rect = stage.getBoundingClientRect();
        const picked = renderer3d.pickEntity(e.clientX - rect.left, e.clientY - rect.top, timeline[idx]);
        if (picked) {
          setHoveredEntity(picked.id);
          selectEntity(picked.id, false, e.shiftKey || e.ctrlKey || e.metaKey);
          return;
        }
      }
      setHoveredEntity(null);
      selectEntity(null, false, e.shiftKey || e.ctrlKey || e.metaKey);
    });
    stage.addEventListener('dblclick', e => {
      if (e.target.closest('.sidehud') || e.target.closest('.bottomhud') || e.target.closest('.entity-sprite')) return;
      if (!mode3d || !renderer3d) return;
      const rect = stage.getBoundingClientRect();
      const picked = renderer3d.pickEntity(e.clientX - rect.left, e.clientY - rect.top, timeline[idx]);
      if (!picked) return;
      e.preventDefault();
      setHoveredEntity(picked.id);
      selectEntity(picked.id, true, e.shiftKey || e.ctrlKey || e.metaKey);
    });
    stage.addEventListener('contextmenu', e => {
      e.preventDefault();
    });
    function edgePanLoop() {
      edgePanFrame = requestAnimationFrame(edgePanLoop);
      if (!edgePanActive || dragging || rotatingCamera || selectingBox) return;
      const margin = 26;
      const speedPx = 13;
      let dx = 0;
      let dy = 0;
      if (mouseX < margin) dx += speedPx;
      if (mouseX > stage.clientWidth - margin) dx -= speedPx;
      if (mouseY < margin) dy += speedPx;
      if (mouseY > stage.clientHeight - margin) dy -= speedPx;
      if (dx || dy) panBy(dx, dy);
    }
    window.addEventListener('keydown', e => {
      if (e.key === ' ') {
        e.preventDefault();
        play();
      }
      const key = e.key.toLowerCase();
      if (key === 'arrowleft') {
        e.shiftKey ? step(-1) : panBy(80, 0);
      }
      if (key === 'arrowright') {
        e.shiftKey ? step(1) : panBy(-80, 0);
      }
      if (key === 'arrowup') panBy(0, 80);
      if (key === 'arrowdown') panBy(0, -80);
      if (key === 'a') panBy(80, 0);
      if (key === 'd') panBy(-80, 0);
      if (key === 'w') panBy(0, 80);
      if (key === 's') panBy(0, -80);
      if (key === '+') zoomAt(stage.clientWidth / 2, stage.clientHeight / 2, 1.18);
      if (key === '-') zoomAt(stage.clientWidth / 2, stage.clientHeight / 2, 1 / 1.18);
      if (mode3d && key === 'q') {
        e.preventDefault();
        rotateCamera(-Math.PI / 18, 0);
      }
      if (mode3d && key === 'e') {
        e.preventDefault();
        rotateCamera(Math.PI / 18, 0);
      }
      if (mode3d && e.key === 'PageUp') {
        e.preventDefault();
        rotateCamera(0, 0.08);
      }
      if (mode3d && e.key === 'PageDown') {
        e.preventDefault();
        rotateCamera(0, -0.08);
      }
      if (key === 'escape') selectEntity(null, false);
    });
    window.addEventListener('resize', () => {
      focusInitialCamera();
      updateMiniMarkers(timeline[idx] || {});
      if (renderer3d) renderer3d.requestRender();
    });
    mini.addEventListener('load', () => {
      updateMinimap();
      updateMiniMarkers(timeline[idx] || {});
    });
    function applyStartupParams() {
      const params = new URLSearchParams(window.location.search || '');
      const debugMode = params.get('debug') === '1' || params.get('debug') === 'true';
      document.body.classList.toggle('debug-mode', debugMode);
      const requestedFrame = Number(params.get('frame') || params.get('idx') || 0);
      if (Number.isFinite(requestedFrame) && requestedFrame > 0) {
        show(clamp(Math.round(requestedFrame), 0, Math.max(0, timeline.length - 1)));
      }
      const requestedMode = String(params.get('mode') || params.get('view') || '').toLowerCase();
      const force2d = requestedMode === '2d' || requestedMode === 'flat' || params.get('3d') === '0';
      const force3d = requestedMode === '3d' || params.get('3d') === '1';
      if ((force3d || !force2d) && !mode3d) {
        suppressModeMessage = true;
        try {
          mode3dBtn.onclick();
        } finally {
          suppressModeMessage = false;
        }
      }
      if (params.get('trails') === '1' || params.get('paths') === '1') {
        showAllTrails = true;
        document.getElementById('cmdTrails').classList.add('active');
        renderMovementTrails();
      }
      const requestedYaw = params.has('yaw') ? Number(params.get('yaw')) : NaN;
      if (Number.isFinite(requestedYaw)) {
        cameraYaw = requestedYaw * Math.PI / 180;
      }
      const requestedPitch = params.has('pitch') ? Number(params.get('pitch')) : NaN;
      if (Number.isFinite(requestedPitch)) {
        cameraPitch = clampCameraPitch(requestedPitch * Math.PI / 180);
      }
      const requestedSelection = String(params.get('select') || '')
        .split(',')
        .map(value => value.trim())
        .filter(Boolean);
      if (requestedSelection.length) {
        applySelection(requestedSelection, requestedSelection[0], params.get('focus') === '1');
      }
      if (mode3d && renderer3d) renderer3d.render(timeline[idx]);
      renderMovementTrails();
    }
    show(0);
    focusInitialCamera();
    applyStartupParams();
    requestAnimationFrame(() => {
      if (mode3d && renderer3d) renderer3d.render(timeline[idx]);
      renderMovementTrails();
    });
  </script>
</body>
</html>
"""
    replacements = {
        "__TITLE__": html.escape(title),
        "__WIDTH__": str(int(width)),
        "__HEIGHT__": str(int(height)),
        "__MAX_INDEX__": str(max(0, len(timeline) - 1)),
        "__GAME_ASSET_CLASS__": "has-game-assets" if game_assets.get("enabled") else "",
        "__INITIAL_CAMERA_X__": str(int(round(width * ((41100.0 - 25240.0) / 25240.0)))),
        "__INITIAL_CAMERA_Y__": str(int(round(height * (23100.0 / 25248.0)))),
        "__INITIAL_CAMERA_SCALE__": "2.15",
    }
    blank_asset = "data:image/gif;base64,R0lGODlhAQABAAAAACw="
    asset_replacements = {
        "__ASSET_BG_TOP__": assets.get("bg_top") or blank_asset,
        "__ASSET_BG_BOTTOM__": assets.get("bg_bottom") or blank_asset,
        "__ASSET_WINDOW__": assets.get("bg_window") or blank_asset,
        "__ASSET_MINIMAP_BG__": assets.get("minimap_bg") or blank_asset,
        "__ASSET_TOOLTIP__": assets.get("bg_tooltip") or blank_asset,
        "__ICON_GOLD__": assets.get("gold") or blank_asset,
        "__ICON_WOOD__": assets.get("wood") or blank_asset,
        "__ICON_STONE__": assets.get("stone") or blank_asset,
        "__ICON_MUD__": assets.get("mud") or blank_asset,
        "__ICON_IRON__": assets.get("iron") or blank_asset,
        "__ICON_SULFUR__": assets.get("sulfur") or blank_asset,
        "__ICON_SERF__": assets.get("serf") or blank_asset,
        "__ICON_WORKER__": assets.get("worker") or blank_asset,
        "__ICON_UNIVERSITY__": assets.get("university") or blank_asset,
        "__ICON_HEADQUARTER__": assets.get("headquarter") or blank_asset,
        "__ICON_TAB_BUILD__": assets.get("tab_build") or blank_asset,
        "__ICON_TAB_WORKERS__": assets.get("tab_workers") or blank_asset,
        "__ICON_TAB_MOTIVATION__": assets.get("tab_motivation") or blank_asset,
        "__ICON_ONSCREEN_WORKER__": assets.get("onscreen_worker") or assets.get("worker") or blank_asset,
        "__ICON_TO_BUILDING__": assets.get("to_building") or assets.get("generic_building") or blank_asset,
        "__ICON_TO_WORKER__": assets.get("to_worker") or assets.get("generic_settler") or blank_asset,
        "__ICON_TRAILS__": assets.get("trail_toggle") or assets.get("to_worker") or blank_asset,
        "__ICON_OK__": assets.get("ok") or blank_asset,
        "__ICON_ARROW__": assets.get("arrow") or assets.get("trail_toggle") or blank_asset,
        "__ICON_PLUS__": assets.get("plus") or assets.get("ok") or blank_asset,
        "__ICON_MINUS__": assets.get("minus") or assets.get("ok") or blank_asset,
        "__PAYDAY_ICON__": (game_assets.get("payday_frames") or [blank_asset])[0],
        "__GRAPHICS_REPORT_CLASS__": graphics_report_class,
        "__GRAPHICS_REPORT_LINK__": graphics_report_link,
        "__GRAPHICS_REPORT_SUMMARY__": graphics_report_summary,
        "__MESH_SERF__": sample_sprites.get("serf_idle") or sample_meshes.get("serf_idle") or blank_asset,
        "__MESH_HEADQUARTER__": sample_sprites.get("headquarters_1") or sample_meshes.get("headquarters_1") or blank_asset,
        "__MESH_UNIVERSITY__": sample_sprites.get("university_1") or sample_meshes.get("university_1") or blank_asset,
        "__MESH_TREE__": sample_sprites.get("tree_fir") or sample_meshes.get("tree_fir") or blank_asset,
    }
    replacements.update({key: html.escape(value, quote=True) for key, value in asset_replacements.items()})
    for key, value in replacements.items():
        html_text = html_text.replace(key, value)
    html_text = html_text.replace("__TIMELINE__", timeline_json)
    html_text = html_text.replace("__GAME_ASSETS__", game_assets_json)
    (output_dir / "index.html").write_text(html_text, encoding="utf-8")


def main() -> None:
    args = _parse_args()
    if args.sim_mode:
        os.environ["SIEDLER_SIM_MODE"] = args.sim_mode
        if args.sim_mode == "full_sim":
            os.environ["SIEDLER_DISABLE_RUNTIME_PATHING"] = "0"

    output_dir = Path(args.output_dir)
    frames_dir = output_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    game_root = _find_game_root(args.game_root)
    args._resolved_background = _resolve_replay_background(args, output_dir, game_root)
    game_assets = _export_game_assets(output_dir, game_root, bool(args.no_game_assets))
    game_assets["original_graphics"] = _export_original_graphics(
        output_dir,
        game_root,
        bool(args.no_game_assets or args.no_original_graphics_report),
        bool(args.refresh_original_graphics_report),
    )
    args._game_assets = game_assets
    args._output_dir = output_dir

    env = SiedlerScharfschuetzenEnv(render_mode=None, use_spatial_obs=False)
    env.reset(seed=args.seed)
    rng = np.random.default_rng(args.seed)
    base = _make_html_base_image(env, args)
    terrain_texture_name = "terrain_base.jpg"
    imageio.imwrite(
        output_dir / terrain_texture_name,
        base,
        quality=max(1, min(100, int(args.jpg_quality))),
    )
    game_assets["minimap_texture"] = terrain_texture_name
    game_assets["terrain_texture"] = _make_full_terrain_texture(args, output_dir, game_root) or terrain_texture_name
    game_assets["terrain3d"] = _make_terrain3d_payload(env, args)
    controller = ExpertOpeningController() if args.strategy == "expert_opening" else None
    opening_state = replay.OpeningPolicyState() if args.strategy == "opening_v1" else None

    timeline: list[dict] = []
    last_action = "reset"
    frame = _render_frame(env, base, 0, args.steps, last_action, args)
    frame_name = "frames/frame_0000.jpg"
    imageio.imwrite(frames_dir / "frame_0000.jpg", frame, quality=max(1, min(100, int(args.jpg_quality))))
    timeline.append(_timeline_entry(env, frame_name, 0, last_action, args))
    height, width = frame.shape[:2]

    done = False
    trunc = False
    decisions = 0
    while decisions < args.steps and not done and not trunc:
        result = replay._run_one_decision(env, rng, args.strategy, opening_state, controller)
        if result is None:
            break
        _obs, _reward, done, trunc, info = result
        decisions += 1
        last_action = str(info.get("action_name", "unknown"))
        if decisions % max(1, int(args.frame_every)) != 0:
            continue
        frame = _render_frame(env, base, decisions, args.steps, last_action, args)
        frame_name = f"frames/frame_{len(timeline):04d}.jpg"
        imageio.imwrite(frames_dir / Path(frame_name).name, frame, quality=max(1, min(100, int(args.jpg_quality))))
        timeline.append(_timeline_entry(env, frame_name, decisions, last_action, args))

    (output_dir / "timeline.json").write_text(json.dumps(timeline, indent=2, ensure_ascii=False), encoding="utf-8")
    _write_html(output_dir, timeline, width, height, game_assets=game_assets)

    print(f"Interactive replay: {output_dir / 'index.html'}")
    print(f"Frames: {len(timeline)}")
    print(f"Last sim time: {timeline[-1]['time'] if timeline else 0}s")
    if game_assets.get("enabled"):
        print(f"Game assets: {game_assets.get('copied', 0)} PNGs from {game_assets.get('root', '')}")
    else:
        print("Game assets: disabled or not found")
    original_graphics = game_assets.get("original_graphics") or {}
    if original_graphics.get("enabled"):
        print(f"Original graphics report: {output_dir / original_graphics.get('index', '')}")


if __name__ == "__main__":
    main()
