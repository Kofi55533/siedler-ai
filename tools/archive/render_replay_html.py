#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Exportiert ein interaktives HTML-Replay fuer die Expert-Opening-Simulation."""

from __future__ import annotations

import argparse
import html
import json
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
from tools.archive.render_wintersturm_background import render_background as render_wintersturm_background
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
    parser.add_argument("--entity-render-mode", choices=["mesh", "gui", "none"], default="mesh", help="Karten-Entitaeten als DFF-Mesh-Sprites, GUI-Icons oder gar nicht ueberblenden")
    parser.add_argument(
        "--game-root",
        type=str,
        default="",
        help="Pfad zur Siedler-5/Gold-Edition. Wenn gesetzt/gefunden, werden lokale Original-GUI-Assets genutzt.",
    )
    parser.add_argument("--no-game-assets", action="store_true", help="Keine Original-Spielgrafiken in das Replay kopieren")
    parser.add_argument("--no-game-icon-overlay", action="store_true", help="Keine Original-Entitaets-Overlays in die Kartenframes zeichnen")
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
    }
    payday_frames = sorted(base_gui.glob("payday*.png"))
    return {
        "enabled": copied > 0,
        "copied": copied,
        "root": str(game_root),
        "assets": {name: _rel_asset(output_dir, path) for name, path in important.items()},
        "payday_frames": [_rel_asset(output_dir, path) for path in payday_frames],
    }


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
    sample_meshes: dict[str, str] = {}
    mesh_by_key: dict[str, str] = {}
    for entity in manifest.get("entities", []):
        key = str(entity.get("key", ""))
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
        "sample_meshes": sample_meshes,
        "mesh_by_key": mesh_by_key,
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


def _timeline_entry(env, frame_name: str, decision: int, action_label: str) -> dict:
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
    }


_ICON_CACHE: dict[tuple[str, int, int], Image.Image] = {}


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


def _load_render_icon(args, key: str, size: int, *, mesh: bool = False) -> Image.Image | None:
    path = _mesh_path_for_render(args, key) if mesh else _asset_path_for_render(args, key)
    if path is None:
        return None
    cache_key = (str(path), int(size), int(bool(mesh)))
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
    resource = str(getattr(serf, "assigned_resource", "") or getattr(serf, "resource", "") or "").lower()
    if "build" in state:
        return "serf_build"
    if "wood" in resource or "wood" in state or "holz" in resource:
        return "serf_wood"
    if any(token in resource for token in ("stone", "clay", "iron", "sulfur", "stein", "lehm", "eisen", "schwefel")):
        return "serf_mine"
    return "serf_idle"


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


def _paste_centered_icon(canvas: Image.Image, icon: Image.Image | None, x: int, y: int) -> None:
    if icon is None:
        return
    canvas.alpha_composite(icon, (int(x - icon.width / 2), int(y - icon.height / 2)))


def _overlay_game_icons(env, frame: np.ndarray, args) -> np.ndarray:
    manifest = getattr(args, "_game_assets", None) or {}
    mode = str(getattr(args, "entity_render_mode", "mesh") or "mesh")
    if not manifest.get("enabled") or getattr(args, "no_game_icon_overlay", False) or mode == "none":
        return frame
    if getattr(args, "viewport", "full") != "full":
        return frame
    use_mesh = mode == "mesh" and bool((manifest.get("original_graphics") or {}).get("mesh_by_key"))

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
        if use_mesh:
            icon = _load_render_icon(args, _building_mesh_key(building_name), 58, mesh=True)
        else:
            icon = _load_render_icon(args, _building_icon_key(building_name), 34)
        _paste_centered_icon(canvas, icon, x, y)

    for site in getattr(env, "construction_sites", []):
        xy = replay._as_xy(site.get("position"))
        if xy is None:
            continue
        x, y = world_to_frame(xy[0], xy[1])
        if use_mesh:
            icon = _load_render_icon(args, _building_mesh_key(site.get("building", "")), 48, mesh=True)
        else:
            icon = _load_render_icon(args, "site", 30)
        _paste_centered_icon(canvas, icon, x, y)

    for worker in getattr(env.workforce_manager, "workers", []):
        xy = replay._as_xy(getattr(worker, "position", None))
        if xy is None:
            continue
        x, y = world_to_frame(xy[0], xy[1])
        worker_icon = (
            _load_render_icon(args, _worker_mesh_key(worker), 24, mesh=True)
            if use_mesh
            else _load_render_icon(args, "worker", 18)
        )
        _paste_centered_icon(canvas, worker_icon, x, y)

    for serf in getattr(env.production_system, "serfs", []):
        xy = replay._as_xy(getattr(serf, "position", None))
        if xy is None:
            continue
        x, y = world_to_frame(xy[0], xy[1])
        serf_icon = (
            _load_render_icon(args, _serf_mesh_key(serf), 24, mesh=True)
            if use_mesh
            else _load_render_icon(args, "serf", 20)
        )
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
    frame = _overlay_game_icons(env, frame, args)
    return frame


def _write_html(output_dir: Path, timeline: list[dict], width: int, height: int, game_assets: dict | None = None) -> None:
    timeline_json = json.dumps(timeline, ensure_ascii=False).replace("</", "<\\/")
    game_assets = game_assets or {"enabled": False, "assets": {}, "payday_frames": []}
    game_assets_json = json.dumps(game_assets, ensure_ascii=False).replace("</", "<\\/")
    assets = game_assets.get("assets") or {}
    original_graphics = game_assets.get("original_graphics") or {}
    graphics_summary_data = original_graphics.get("summary") or {}
    sample_meshes = original_graphics.get("sample_meshes") or {}
    if original_graphics.get("enabled"):
        graphics_report_class = ""
        graphics_report_link = original_graphics.get("index") or "#"
        graphics_report_summary = (
            f"{int(graphics_summary_data.get('with_model', 0))} Modelle, "
            f"{int(graphics_summary_data.get('with_texture', 0))} Texturen, "
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
      grid-template-rows: auto auto 1fr;
      min-width: 0;
      overflow: hidden;
    }
    .resourcebar {
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
      display: grid;
      grid-template-columns: auto auto auto minmax(260px, 1fr) auto auto auto;
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
      position: relative;
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
    #map {
      position: absolute;
      left: 0;
      top: 0;
      transform-origin: 0 0;
      image-rendering: pixelated;
      user-select: none;
      -webkit-user-drag: none;
      filter: saturate(1.05) contrast(1.03);
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
    #miniView {
      position: absolute;
      border: 2px solid #ffe47c;
      box-shadow: 0 0 0 1px #111, 0 0 9px rgba(255,224,110,.75);
      pointer-events: none;
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
      display: none;
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
    .stage.playing .playing-dot {
      background: var(--green);
      animation: pulse 1s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: .65; transform: scale(.92); }
      50% { opacity: 1; transform: scale(1.15); }
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
  <div class="controlbar">
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
    <span class="keycap">Space</span>
  </div>
  <div id="stage" class="stage">
    <img id="map" src="" width="__WIDTH__" height="__HEIGHT__" alt="Replay frame">
    <div class="sidehud">
      <div class="panel">
        <div id="headline" class="big"></div>
        <div id="action" class="actionline"></div>
        <div class="statgrid">
          <div class="stat"><b id="statBuildings">0</b><span>Gebaeude</span></div>
          <div class="stat"><b id="statSites">0</b><span>Baustellen</span></div>
          <div class="stat"><b id="statSerfs">0</b><span>Serfs</span></div>
          <div class="stat"><b id="statWorkers">0</b><span>Worker</span></div>
        </div>
        <div class="asset-strip">
          <div class="asset-badge"><img src="__ICON_SERF__" alt="Serf"></div>
          <div class="asset-badge"><img src="__ICON_WORKER__" alt="Worker"></div>
          <div class="asset-badge"><img src="__ICON_UNIVERSITY__" alt="Hochschule"></div>
          <div class="asset-badge"><img src="__ICON_HEADQUARTER__" alt="Hauptquartier"></div>
        </div>
        <div class="graphics-report __GRAPHICS_REPORT_CLASS__">
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
          <div id="miniView"></div>
        </div>
      </div>
    </div>
  </div>
  <script>
    const timeline = __TIMELINE__;
    const gameAssets = __GAME_ASSETS__;
    const paydayFrames = gameAssets.payday_frames || [];
    const MAP_WIDTH = __WIDTH__;
    const MAP_HEIGHT = __HEIGHT__;
    const img = document.getElementById('map');
    const mini = document.getElementById('mini');
    const miniBox = document.getElementById('miniBox');
    const miniView = document.getElementById('miniView');
    const stage = document.getElementById('stage');
    const slider = document.getElementById('slider');
    const playBtn = document.getElementById('play');
    const fullscreenBtn = document.getElementById('fullscreen');
    const speed = document.getElementById('speed');
    const headline = document.getElementById('headline');
    const action = document.getElementById('action');
    const zoomLevel = document.getElementById('zoomLevel');
    const paydayIcon = document.getElementById('paydayIcon');
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
    const INITIAL_CAMERA_X = __INITIAL_CAMERA_X__;
    const INITIAL_CAMERA_Y = __INITIAL_CAMERA_Y__;
    const INITIAL_CAMERA_SCALE = __INITIAL_CAMERA_SCALE__;

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
    function updateMinimap() {
      if (!miniBox.clientWidth || !miniBox.clientHeight) return;
      zoomLevel.textContent = `${Math.round(scale * 100)}%`;
      const sx = miniBox.clientWidth / MAP_WIDTH;
      const sy = miniBox.clientHeight / MAP_HEIGHT;
      const visibleX = clamp(-tx / scale, 0, MAP_WIDTH);
      const visibleY = clamp(-ty / scale, 0, MAP_HEIGHT);
      const visibleW = clamp(stage.clientWidth / scale, 0, MAP_WIDTH);
      const visibleH = clamp(stage.clientHeight / scale, 0, MAP_HEIGHT);
      miniView.style.left = `${clamp(visibleX * sx, 0, miniBox.clientWidth)}px`;
      miniView.style.top = `${clamp(visibleY * sy, 0, miniBox.clientHeight)}px`;
      miniView.style.width = `${clamp(visibleW * sx, 8, miniBox.clientWidth)}px`;
      miniView.style.height = `${clamp(visibleH * sy, 8, miniBox.clientHeight)}px`;
    }
    function applyTransform() {
      img.style.transform = `translate(${tx}px, ${ty}px) scale(${scale})`;
      updateMinimap();
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
      mini.src = f.frame;
      slider.value = idx;
      const lastDecision = timeline[timeline.length - 1].decision;
      headline.innerHTML = `<span class="playing-dot"></span>Simzeit ${fmtTime(f.time)}`;
      action.textContent = `Aktion ${f.decision}/${lastDecision}: ${f.action}`;
      setText('statBuildings', fmt(f.buildings));
      setText('statSites', fmt(f.sites));
      setText('statSerfs', fmt(f.serfs));
      setText('statWorkers', fmt(f.workers));
      updateResources(f);
      updatePayday(f);
      updateMinimap();
    }
    function step(delta) {
      show(idx + delta);
    }
    function stopPlayback() {
      if (!timer) return;
      clearInterval(timer);
      timer = null;
      playBtn.textContent = 'Play';
      playBtn.classList.remove('active');
      stage.classList.remove('playing');
    }
    function play() {
      if (timer) {
        stopPlayback();
        return;
      }
      playBtn.textContent = 'Pause';
      playBtn.classList.add('active');
      stage.classList.add('playing');
      timer = setInterval(() => {
        if (idx >= timeline.length - 1) {
          stopPlayback();
          return;
        }
        step(1);
      }, Number(speed.value));
    }
    document.getElementById('prev').onclick = () => step(-1);
    document.getElementById('next').onclick = () => step(1);
    playBtn.onclick = play;
    fullscreenBtn.onclick = async () => {
      if (!document.fullscreenElement) {
        await document.documentElement.requestFullscreen();
      } else {
        await document.exitFullscreen();
      }
    };
    speed.onchange = () => {
      if (!timer) return;
      stopPlayback();
      play();
    };
    slider.oninput = e => show(Number(e.target.value));
    document.getElementById('fit').onclick = focusInitialCamera;
    stage.addEventListener('wheel', e => {
      e.preventDefault();
      const rect = stage.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;
      const beforeX = (mx - tx) / scale;
      const beforeY = (my - ty) / scale;
      scale *= e.deltaY < 0 ? 1.15 : 1 / 1.15;
      scale = Math.max(0.15, Math.min(12, scale));
      tx = mx - beforeX * scale;
      ty = my - beforeY * scale;
      applyTransform();
    }, { passive: false });
    miniBox.addEventListener('click', e => {
      const rect = miniBox.getBoundingClientRect();
      const worldX = ((e.clientX - rect.left) / rect.width) * MAP_WIDTH;
      const worldY = ((e.clientY - rect.top) / rect.height) * MAP_HEIGHT;
      tx = stage.clientWidth / 2 - worldX * scale;
      ty = stage.clientHeight / 2 - worldY * scale;
      applyTransform();
    });
    stage.addEventListener('mousedown', e => {
      if (e.target.closest('.sidehud')) return;
      dragging = true;
      stage.classList.add('dragging');
      lastX = e.clientX;
      lastY = e.clientY;
    });
    window.addEventListener('mouseup', () => {
      dragging = false;
      stage.classList.remove('dragging');
    });
    window.addEventListener('mousemove', e => {
      if (!dragging) return;
      tx += e.clientX - lastX;
      ty += e.clientY - lastY;
      lastX = e.clientX;
      lastY = e.clientY;
      applyTransform();
    });
    window.addEventListener('keydown', e => {
      if (e.key === ' ') {
        e.preventDefault();
        play();
      }
      if (e.key === 'ArrowLeft') step(-1);
      if (e.key === 'ArrowRight') step(1);
    });
    window.addEventListener('resize', focusInitialCamera);
    show(0);
    focusInitialCamera();
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
        "__PAYDAY_ICON__": (game_assets.get("payday_frames") or [blank_asset])[0],
        "__GRAPHICS_REPORT_CLASS__": graphics_report_class,
        "__GRAPHICS_REPORT_LINK__": graphics_report_link,
        "__GRAPHICS_REPORT_SUMMARY__": graphics_report_summary,
        "__MESH_SERF__": sample_meshes.get("serf_idle") or blank_asset,
        "__MESH_HEADQUARTER__": sample_meshes.get("headquarters_1") or blank_asset,
        "__MESH_UNIVERSITY__": sample_meshes.get("university_1") or blank_asset,
        "__MESH_TREE__": sample_meshes.get("tree_fir") or blank_asset,
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
    controller = ExpertOpeningController() if args.strategy == "expert_opening" else None
    opening_state = replay.OpeningPolicyState() if args.strategy == "opening_v1" else None

    timeline: list[dict] = []
    last_action = "reset"
    frame = _render_frame(env, base, 0, args.steps, last_action, args)
    frame_name = "frames/frame_0000.jpg"
    imageio.imwrite(frames_dir / "frame_0000.jpg", frame, quality=max(1, min(100, int(args.jpg_quality))))
    timeline.append(_timeline_entry(env, frame_name, 0, last_action))
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
        timeline.append(_timeline_entry(env, frame_name, decisions, last_action))

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
