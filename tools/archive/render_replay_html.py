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
    timeline_json = json.dumps(timeline, ensure_ascii=False).replace("</", "<\\/")
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
      min-width: 860px;
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
      grid-template-columns: auto auto auto minmax(260px, 1fr) auto auto;
      gap: 8px;
      align-items: center;
      padding: 6px 10px;
      background: linear-gradient(180deg, #252d33, #11161a);
      border-bottom: 1px solid #34404a;
      font-family: system-ui, Segoe UI, sans-serif;
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
<body>
  <div class="resourcebar">
    <div class="crest">
      Wintersturm
      <small>Expert Opening Full-Sim</small>
    </div>
    <div class="resources">
      <div class="resource-chip"><div class="res-icon">T</div><div><div class="name">Taler</div><div id="resTaler" class="value">0</div><div class="raw">Kasse</div></div></div>
      <div class="resource-chip"><div class="res-icon">H</div><div><div class="name">Holz</div><div id="resHolz" class="value">0</div><div id="rawHolz" class="raw">Roh 0</div></div></div>
      <div class="resource-chip"><div class="res-icon">S</div><div><div class="name">Stein</div><div id="resStein" class="value">0</div><div id="rawStein" class="raw">Roh 0</div></div></div>
      <div class="resource-chip"><div class="res-icon">L</div><div><div class="name">Lehm</div><div id="resLehm" class="value">0</div><div id="rawLehm" class="raw">Roh 0</div></div></div>
      <div class="resource-chip"><div class="res-icon">E</div><div><div class="name">Eisen</div><div id="resEisen" class="value">0</div><div id="rawEisen" class="raw">Roh 0</div></div></div>
      <div class="resource-chip"><div class="res-icon">G</div><div><div class="name">Schwefel</div><div id="resSchwefel" class="value">0</div><div id="rawSchwefel" class="raw">Roh 0</div></div></div>
    </div>
    <div class="payday">
      <div>
        <div class="label">Zahltag</div>
        <div id="paydayMain" class="main">nicht gesetzt</div>
        <div id="paydaySub" class="sub">erster Worker fehlt</div>
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
      <option value="1200">sehr langsam</option>
      <option value="700" selected>langsam</option>
      <option value="350">normal</option>
      <option value="120">schnell</option>
    </select>
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
        <button class="toolbutton" id="fit" style="margin-top:10px;">Ansicht reset</button>
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
    const MAP_WIDTH = __WIDTH__;
    const MAP_HEIGHT = __HEIGHT__;
    const img = document.getElementById('map');
    const mini = document.getElementById('mini');
    const miniBox = document.getElementById('miniBox');
    const miniView = document.getElementById('miniView');
    const stage = document.getElementById('stage');
    const slider = document.getElementById('slider');
    const playBtn = document.getElementById('play');
    const speed = document.getElementById('speed');
    const headline = document.getElementById('headline');
    const action = document.getElementById('action');
    const zoomLevel = document.getElementById('zoomLevel');
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
    function updatePayday(f) {
      const main = document.getElementById('paydayMain');
      const sub = document.getElementById('paydaySub');
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
      headline.innerHTML = `<span class="playing-dot"></span>t=${f.time}s - Step ${f.decision}/${lastDecision}`;
      action.textContent = f.action;
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
    speed.onchange = () => {
      if (!timer) return;
      stopPlayback();
      play();
    };
    slider.oninput = e => show(Number(e.target.value));
    document.getElementById('fit').onclick = fit;
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
    window.addEventListener('resize', fit);
    show(0);
    fit();
  </script>
</body>
</html>
"""
    replacements = {
        "__TITLE__": html.escape(title),
        "__WIDTH__": str(int(width)),
        "__HEIGHT__": str(int(height)),
        "__MAX_INDEX__": str(max(0, len(timeline) - 1)),
    }
    for key, value in replacements.items():
        html_text = html_text.replace(key, value)
    html_text = html_text.replace("__TIMELINE__", timeline_json)
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
