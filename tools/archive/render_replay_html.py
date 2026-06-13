#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Exportiert ein interaktives HTML-Replay fuer die Expert-Opening-Simulation."""

from __future__ import annotations

import argparse
import html
import json
import os
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
from tools.archive import render_replay_mp4 as replay


def _parse_args():
    parser = argparse.ArgumentParser(description="Interaktives HTML-Replay fuer Siedler Expert Opening")
    parser.add_argument("--steps", type=int, default=260)
    parser.add_argument("--frame-every", type=int, default=1)
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--render-scale", type=int, default=5)
    parser.add_argument("--background", type=str, default="training_p1_map_preview.png")
    parser.add_argument("--output-dir", type=str, default="analysis/replays/expert_opening_interactive")
    parser.add_argument("--strategy", choices=["expert_opening", "opening_v1", "random"], default="expert_opening")
    parser.add_argument("--sim-mode", choices=["full_sim", "fast_train", ""], default="full_sim")
    parser.add_argument("--viewport", choices=["full", "bottom_right"], default="full")
    parser.add_argument("--jpg-quality", type=int, default=88)
    parser.add_argument("--labels", action="store_true", help="Textlabels direkt ins Kartenbild zeichnen")
    parser.add_argument("--hud", action="store_true", help="HUD direkt ins Kartenbild zeichnen")
    parser.add_argument("--no-paths", action="store_true")
    return parser.parse_args()


def _timeline_entry(env, frame_name: str, decision: int, action_label: str) -> dict:
    first_payday = None
    if getattr(env, "_first_worker_building_time", None) is not None:
        first_payday = int(env._first_worker_building_time + replay.INCOME_CYCLE)
    return {
        "frame": frame_name,
        "decision": int(decision),
        "time": int(getattr(env, "current_time", 0)),
        "action": str(action_label),
        "serfs": int(len(getattr(env.production_system, "serfs", []))),
        "workers": int(len(getattr(env.workforce_manager, "workers", []))),
        "buildings": int(len(getattr(env, "building_position_map", {}))),
        "sites": int(len(getattr(env, "construction_sites", []))),
        "taler": int(env.resources.get("Taler", 0)),
        "holz_roh": int(env.resources.get("HolzRoh", 0)),
        "stein_roh": int(env.resources.get("SteinRoh", 0)),
        "first_payday": first_payday,
    }


def _render_frame(env, base, decision: int, total: int, action_label: str, args) -> np.ndarray:
    frame = replay._draw_frame(
        env,
        base,
        decision,
        total,
        draw_paths=not args.no_paths,
        max_paths=1200,
        action_label=action_label,
        label_entities=bool(args.labels),
        show_worker_states=True,
        show_worker_targets=True,
        show_refiner_trips=True,
        max_refiner_trips=120,
        show_hud=bool(args.hud),
    )
    frame = replay._apply_viewport(frame, args.viewport)
    frame = replay._scale_frame(frame, args.render_scale)
    return frame


def _write_html(output_dir: Path, timeline: list[dict], width: int, height: int) -> None:
    timeline_json = json.dumps(timeline, ensure_ascii=False)
    title = "Siedler Expert Opening Replay"
    html_text = f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    html, body {{ margin: 0; height: 100%; background: #171b20; color: #eceff1; font-family: system-ui, Segoe UI, sans-serif; }}
    body {{ display: grid; grid-template-rows: auto 1fr; overflow: hidden; }}
    .topbar {{ display: grid; grid-template-columns: auto auto auto 1fr auto; gap: 10px; align-items: center; padding: 10px 12px; background: #101418; border-bottom: 1px solid #303943; }}
    button, select {{ background: #26313a; color: #fff; border: 1px solid #52606b; border-radius: 6px; padding: 7px 10px; }}
    button:hover {{ background: #33424d; }}
    input[type="range"] {{ width: 100%; }}
    .stage {{ position: relative; overflow: hidden; cursor: grab; background: #0b0e11; }}
    .stage.dragging {{ cursor: grabbing; }}
    #map {{ position: absolute; left: 0; top: 0; transform-origin: 0 0; image-rendering: pixelated; user-select: none; -webkit-user-drag: none; }}
    .panel {{ position: absolute; right: 12px; top: 12px; min-width: 320px; max-width: 460px; background: rgba(10, 13, 16, .82); border: 1px solid rgba(255,255,255,.18); border-radius: 8px; padding: 10px 12px; backdrop-filter: blur(4px); }}
    .panel .big {{ font-size: 18px; font-weight: 700; margin-bottom: 4px; }}
    .panel .muted {{ color: #aeb8c2; }}
    .kbd {{ font-size: 12px; color: #aeb8c2; }}
  </style>
</head>
<body>
  <div class="topbar">
    <button id="prev">Zurück</button>
    <button id="play">Play</button>
    <button id="next">Weiter</button>
    <input id="slider" type="range" min="0" max="{max(0, len(timeline)-1)}" value="0">
    <select id="speed">
      <option value="1200">sehr langsam</option>
      <option value="700" selected>langsam</option>
      <option value="350">normal</option>
      <option value="120">schnell</option>
    </select>
  </div>
  <div id="stage" class="stage">
    <img id="map" src="" width="{width}" height="{height}" alt="Replay frame">
    <div class="panel">
      <div id="headline" class="big"></div>
      <div id="action"></div>
      <div id="stats" class="muted"></div>
      <div class="kbd">Mausrad: Zoom · Ziehen: Verschieben · Leertaste: Play/Pause · Pfeile: Schritt</div>
      <button id="fit" style="margin-top:8px;">Ansicht zurücksetzen</button>
    </div>
  </div>
  <script>
    const timeline = {timeline_json};
    const img = document.getElementById('map');
    const stage = document.getElementById('stage');
    const slider = document.getElementById('slider');
    const playBtn = document.getElementById('play');
    const speed = document.getElementById('speed');
    const headline = document.getElementById('headline');
    const action = document.getElementById('action');
    const stats = document.getElementById('stats');
    let idx = 0, timer = null, scale = 1, tx = 0, ty = 0, dragging = false, lastX = 0, lastY = 0;

    function applyTransform() {{ img.style.transform = `translate(${{tx}}px, ${{ty}}px) scale(${{scale}})`; }}
    function fit() {{
      const sx = stage.clientWidth / {width};
      const sy = stage.clientHeight / {height};
      scale = Math.min(sx, sy) * 0.98;
      tx = (stage.clientWidth - {width} * scale) / 2;
      ty = (stage.clientHeight - {height} * scale) / 2;
      applyTransform();
    }}
    function show(i) {{
      idx = Math.max(0, Math.min(timeline.length - 1, i));
      const f = timeline[idx];
      img.src = f.frame;
      slider.value = idx;
      headline.textContent = `t=${{f.time}}s · Step ${{f.decision}}/${{timeline[timeline.length-1].decision}}`;
      action.textContent = f.action;
      const payday = f.first_payday == null ? 'noch nicht gesetzt' : `t=${{f.first_payday}}s`;
      stats.textContent = `Gebäude ${{f.buildings}} · Baustellen ${{f.sites}} · Worker ${{f.workers}} · Serfs ${{f.serfs}} · HolzRoh ${{f.holz_roh}} · SteinRoh ${{f.stein_roh}} · Taler ${{f.taler}} · erster Payday: ${{payday}}`;
    }}
    function step(delta) {{ show(idx + delta); }}
    function play() {{
      if (timer) {{ clearInterval(timer); timer = null; playBtn.textContent = 'Play'; return; }}
      playBtn.textContent = 'Pause';
      timer = setInterval(() => {{
        if (idx >= timeline.length - 1) {{ play(); return; }}
        step(1);
      }}, Number(speed.value));
    }}
    document.getElementById('prev').onclick = () => step(-1);
    document.getElementById('next').onclick = () => step(1);
    playBtn.onclick = play;
    slider.oninput = e => show(Number(e.target.value));
    document.getElementById('fit').onclick = fit;
    stage.addEventListener('wheel', e => {{
      e.preventDefault();
      const rect = stage.getBoundingClientRect();
      const mx = e.clientX - rect.left, my = e.clientY - rect.top;
      const beforeX = (mx - tx) / scale, beforeY = (my - ty) / scale;
      scale *= e.deltaY < 0 ? 1.15 : 1 / 1.15;
      scale = Math.max(0.15, Math.min(12, scale));
      tx = mx - beforeX * scale; ty = my - beforeY * scale;
      applyTransform();
    }}, {{ passive: false }});
    stage.addEventListener('mousedown', e => {{ dragging = true; stage.classList.add('dragging'); lastX = e.clientX; lastY = e.clientY; }});
    window.addEventListener('mouseup', () => {{ dragging = false; stage.classList.remove('dragging'); }});
    window.addEventListener('mousemove', e => {{
      if (!dragging) return;
      tx += e.clientX - lastX; ty += e.clientY - lastY; lastX = e.clientX; lastY = e.clientY; applyTransform();
    }});
    window.addEventListener('keydown', e => {{
      if (e.key === ' ') {{ e.preventDefault(); play(); }}
      if (e.key === 'ArrowLeft') step(-1);
      if (e.key === 'ArrowRight') step(1);
    }});
    window.addEventListener('resize', fit);
    show(0); fit();
  </script>
</body>
</html>
"""
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

    env = SiedlerScharfschuetzenEnv(render_mode=None, use_spatial_obs=False)
    env.reset(seed=args.seed)
    rng = np.random.default_rng(args.seed)
    base = replay._make_base_image(env, args.background)
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
    _write_html(output_dir, timeline, width, height)

    print(f"Interactive replay: {output_dir / 'index.html'}")
    print(f"Frames: {len(timeline)}")
    print(f"Last sim time: {timeline[-1]['time'] if timeline else 0}s")


if __name__ == "__main__":
    main()
