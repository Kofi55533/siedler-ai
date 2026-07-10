#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simuliert einen Durchlauf in der Siedler-Umgebung und rendert ein MP4-Replay
mit Overlay auf einer Player-1 Karte.

Beispiel:
  python render_replay_mp4.py --steps 1800 --output replay_1800.mp4
"""

from __future__ import annotations

import argparse
import os
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Tuple, Dict, List

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pathfinding
from environment import (
    ActionPhase,
    BUILDING_FOOTPRINTS,
    INCOME_CYCLE,
    MAIN_ACTIONS,
    RESEARCH_BUILDINGS,
    SiedlerScharfschuetzenEnv,
    get_base_building_name,
)
from expert_opening import ExpertOpeningController
from worker_simulation import WorkerState


MAIN_ACTION_WEIGHTS = {
    "wait": 0.10,
    "upgrade": 0.90,
    "research": 0.90,
    "recruit": 0.70,
    "buy_serf": 0.80,
    "dismiss_serf": 0.10,
    "assign_serf": 2.20,
    "demolish": 0.15,
    "bless": 0.25,
    "tax": 0.15,
    "alarm": 0.10,
}

PREFER_FIRST_PHASES = {
    ActionPhase.POSITION_GROUP,
    ActionPhase.POSITION_INDEX,
    ActionPhase.SOURCE_SPECIFIC,
    ActionPhase.TARGET_SPECIFIC,
}

QUANTITY_VALUES = [1, 2, 3, 5, 10, 20]
MAX_ASSIGN_QUANTITY_INDEX: Optional[int] = None
_RENDER_PATH_CACHE: Dict[Tuple[int, int, int, int, int], Tuple[List[Tuple[float, float]], List[float], float]] = {}


@dataclass
class OpeningPolicyState:
    last_payday_cycle: int = -1
    wood_zone_cursor: int = 0
    opening_done: bool = False
    initial_serf_target: Optional[int] = None


def _as_xy(pos) -> Optional[Tuple[float, float]]:
    if pos is None:
        return None
    if isinstance(pos, tuple):
        return float(pos[0]), float(pos[1])
    if isinstance(pos, dict):
        return float(pos.get("x", 0.0)), float(pos.get("y", 0.0))
    x = getattr(pos, "x", None)
    y = getattr(pos, "y", None)
    if x is None or y is None:
        return None
    return float(x), float(y)


def _normalize_name(value: str) -> str:
    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("ß", "ss").lower()
    return "".join(ch for ch in text if ch.isalnum() or ch == "_")


def _matches_any(value: str, aliases: Iterable[str]) -> bool:
    normalized = _normalize_name(value)
    alias_norm = [_normalize_name(a) for a in aliases]
    return any(normalized == a or normalized.startswith(a) or a in normalized for a in alias_norm)


def _highest_quantity_index(valid: np.ndarray) -> int:
    valid_set = {int(v) for v in valid}
    for idx in [5, 4, 3, 2, 1, 0]:
        if idx in valid_set:
            return idx
    return int(valid[0]) if len(valid) else 0


def _pick_quantity_index(valid: np.ndarray, max_index: Optional[int] = None) -> int:
    if len(valid) == 0:
        return 0
    if max_index is None:
        return _highest_quantity_index(valid)
    capped = [int(v) for v in valid if int(v) <= int(max_index)]
    if capped:
        return max(capped)
    return int(valid[0])


def _find_buildable_index(env: SiedlerScharfschuetzenEnv, aliases: Iterable[str]) -> Optional[int]:
    for idx, building in enumerate(env.buildable_buildings):
        if _matches_any(building, aliases):
            return idx
    return None


def _count_buildings_by_alias(env: SiedlerScharfschuetzenEnv, aliases: Iterable[str]) -> int:
    total = 0
    for building, count in env.buildings.items():
        if count > 0 and _matches_any(building, aliases):
            total += int(count)
    return total


def _count_buildings_and_sites(env: SiedlerScharfschuetzenEnv, aliases: Iterable[str]) -> int:
    total = _count_buildings_by_alias(env, aliases)
    for site in env.construction_sites:
        building = site.get("building", "")
        if _matches_any(building, aliases):
            total += 1
    return total


def _has_researched(env: SiedlerScharfschuetzenEnv, aliases: Iterable[str]) -> bool:
    return any(_matches_any(tech, aliases) for tech in env.researched_techs)


def _world_to_px(env: SiedlerScharfschuetzenEnv, x: float, y: float, width: int, height: int) -> Tuple[int, int]:
    local_x, local_y = env.map_manager.to_local_coords(x, y)
    # Match GridPosition.from_world(): pathfinding uses floor/int conversion.
    gx = int(local_x / pathfinding.SCALE_X)
    gy = int(local_y / pathfinding.SCALE_Y)
    gx = max(0, min(width - 1, gx))
    gy = max(0, min(height - 1, gy))
    return gx, gy


def _make_base_image(env: SiedlerScharfschuetzenEnv, background_path: Optional[str]) -> np.ndarray:
    grid_h = env.map_manager.grid.height
    grid_w = env.map_manager.grid.width

    if background_path and os.path.exists(background_path):
        img = Image.open(background_path).convert("RGB")
        # Optional: Vollkarten-PNG (4 Spieler) auf P1-Quadrant croppen.
        # P1 liegt auf Wintersturm oben rechts.
        if getattr(env, "_background_crop_p1", False):
            bw, bh = img.size
            img = img.crop((bw // 2, 0, bw, bh // 2))
        img = img.resize((grid_w, grid_h), Image.Resampling.BILINEAR)
        base = np.asarray(img, dtype=np.uint8)
    else:
        terrain = env.map_manager.grid.terrain_base
        trees = env.map_manager.grid.trees
        base = np.zeros((grid_h, grid_w, 3), dtype=np.uint8)
        base[terrain == 1] = np.array([82, 112, 88], dtype=np.uint8)
        base[terrain == 0] = np.array([52, 64, 76], dtype=np.uint8)
        base[trees == 1] = np.array([46, 100, 52], dtype=np.uint8)

    # MP4 codecs moegen gerade Bildgroessen.
    pad_h = base.shape[0] % 2
    pad_w = base.shape[1] % 2
    if pad_h or pad_w:
        base = np.pad(base, ((0, pad_h), (0, pad_w), (0, 0)), mode="edge")
    return base


def _choose_main_action(valid: np.ndarray, rng: np.random.Generator) -> int:
    if len(valid) == 1:
        return int(valid[0])
    weights = np.array([MAIN_ACTION_WEIGHTS.get(MAIN_ACTIONS[int(idx)], 1.0) for idx in valid], dtype=np.float64)
    weights = np.maximum(weights, 0.0)
    if weights.sum() <= 0:
        return int(valid[0])
    probs = weights / weights.sum()
    return int(rng.choice(valid, p=probs))


def _choose_phase_action(phase: ActionPhase, valid: np.ndarray, rng: np.random.Generator) -> int:
    if len(valid) == 0:
        return 0
    if phase in PREFER_FIRST_PHASES:
        return int(valid[0])
    if phase == ActionPhase.QUANTITY:
        # Kleine Batches sind stabiler fuer lange Sim-Replays.
        return int(valid[0])
    return int(rng.choice(valid))


def _run_flow(
    env: SiedlerScharfschuetzenEnv,
    rng: np.random.Generator,
    action_name: str,
    phase_selectors: Optional[dict] = None,
):
    phase_selectors = phase_selectors or {}
    main_choice = MAIN_ACTIONS.index(action_name)
    mask = env.action_masks()
    if main_choice >= len(mask) or not bool(mask[main_choice]):
        return None

    obs, reward, done, trunc, info = env.step(main_choice)

    while info.get("multi_step") and not done and not trunc:
        phase = env.current_phase
        mask = env.action_masks()
        valid = np.where(mask)[0]
        if len(valid) == 0:
            choice = 0
        else:
            selector = phase_selectors.get(phase)
            if callable(selector):
                choice = int(selector(env, phase, valid))
            elif isinstance(selector, int):
                choice = selector
            else:
                choice = None

            if choice not in valid:
                choice = _choose_phase_action(phase, valid, rng)

        obs, reward, done, trunc, info = env.step(choice)

    return obs, reward, done, trunc, info


def _run_random_decision(env: SiedlerScharfschuetzenEnv, rng: np.random.Generator):
    mask = env.action_masks()
    valid = np.where(mask)[0]
    main_choice = _choose_main_action(valid, rng)
    return _run_flow(env, rng, MAIN_ACTIONS[main_choice])


def _run_wait_decision(env: SiedlerScharfschuetzenEnv, rng: np.random.Generator):
    result = _run_flow(env, rng, "wait")
    if result is not None:
        return result
    return _run_random_decision(env, rng)


def _run_expert_decision(env: SiedlerScharfschuetzenEnv, controller: ExpertOpeningController):
    reason = ""
    action = controller.act(env)
    if getattr(controller, "active_plan", None) is not None:
        reason = str(controller.active_plan.reason or "")
    obs, reward, done, trunc, info = env.step(action)

    while info.get("multi_step") and not done and not trunc:
        action = controller.act(env)
        obs, reward, done, trunc, info = env.step(action)

    controller.observe_step(info)
    if reason:
        info["action_reason"] = reason
        info["action_name"] = f"{info.get('action_name', 'unknown')} | {reason}"
    return obs, reward, done, trunc, info


def _try_buy_serf(env: SiedlerScharfschuetzenEnv, rng: np.random.Generator):
    if not env._can_buy_serf():
        return None

    return _run_flow(
        env,
        rng,
        "buy_serf",
        phase_selectors={
            ActionPhase.QUANTITY: lambda _env, _phase, valid: _highest_quantity_index(valid),
        },
    )


def _try_set_tax_level(env: SiedlerScharfschuetzenEnv, rng: np.random.Generator, target_level: int):
    if env.current_tax_level == target_level:
        return None
    return _run_flow(
        env,
        rng,
        "tax",
        phase_selectors={ActionPhase.TAX_LEVEL: target_level},
    )


def _try_bless(env: SiedlerScharfschuetzenEnv, rng: np.random.Generator, preferred_category: int = 4):
    if not env._can_bless():
        return None

    def choose_category(_env, _phase, valid):
        if preferred_category in {int(v) for v in valid}:
            return preferred_category
        return int(valid[0])

    return _run_flow(
        env,
        rng,
        "bless",
        phase_selectors={ActionPhase.CATEGORY: choose_category},
    )


def _try_research(
    env: SiedlerScharfschuetzenEnv,
    rng: np.random.Generator,
    tech_aliases: Iterable[str],
    research_building_aliases: Iterable[str] = ("hochschule",),
):
    choice = None
    for rb_idx, rb_name in enumerate(RESEARCH_BUILDINGS):
        if not _matches_any(rb_name, research_building_aliases):
            continue
        techs = env.tech_by_building.get(rb_name, [])
        for tech_idx, tech_name in enumerate(techs):
            if _matches_any(tech_name, tech_aliases) and env._can_research(tech_name):
                choice = (rb_idx, tech_idx)
                break
        if choice is not None:
            break

    if choice is None:
        return None

    rb_idx, tech_idx = choice
    return _run_flow(
        env,
        rng,
        "research",
        phase_selectors={
            ActionPhase.TECH_BUILDING: rb_idx,
            ActionPhase.TECH: tech_idx,
        },
    )


def _try_build_from_free(
    env: SiedlerScharfschuetzenEnv,
    rng: np.random.Generator,
    building_aliases: Iterable[str],
):
    building_idx = _find_buildable_index(env, building_aliases)
    if building_idx is None:
        return None
    building = env.buildable_buildings[building_idx]
    if not env._can_build(building):
        return None

    def pick_source_category(_env, _phase, valid):
        valid_set = {int(v) for v in valid}
        # Prioritaet: Frei -> Holz -> Stein -> Lehm -> Eisen -> Schwefel -> Baustelle
        for cat in [0, 1, 3, 4, 2, 5, 6]:
            if cat in valid_set:
                return cat
        return int(valid[0])

    def pick_target_specific(_env, _phase, valid):
        valid_set = {int(v) for v in valid}
        if building_idx in valid_set:
            return building_idx
        return int(valid[0])

    return _run_flow(
        env,
        rng,
        "assign_serf",
        phase_selectors={
            ActionPhase.SOURCE_CATEGORY: pick_source_category,
            ActionPhase.SOURCE_SPECIFIC: lambda _env, _phase, valid: int(valid[0]),
            ActionPhase.QUANTITY: lambda _env, _phase, valid: _pick_quantity_index(valid, MAX_ASSIGN_QUANTITY_INDEX),
            ActionPhase.TARGET_CATEGORY: 7,  # Neubau
            ActionPhase.TARGET_SPECIFIC: pick_target_specific,
        },
    )


def _try_assign_free_to_category(
    env: SiedlerScharfschuetzenEnv,
    rng: np.random.Generator,
    target_category: int,
    target_specific: int = 0,
):
    if env.free_leibeigene <= 0:
        return None

    def pick_target_specific(_env, _phase, valid):
        valid_set = {int(v) for v in valid}
        if target_specific in valid_set:
            return target_specific
        return int(valid[0])

    return _run_flow(
        env,
        rng,
        "assign_serf",
        phase_selectors={
            ActionPhase.SOURCE_CATEGORY: 0,  # Frei
            ActionPhase.SOURCE_SPECIFIC: 0,
            ActionPhase.QUANTITY: lambda _env, _phase, valid: _pick_quantity_index(valid, MAX_ASSIGN_QUANTITY_INDEX),
            ActionPhase.TARGET_CATEGORY: target_category,
            ActionPhase.TARGET_SPECIFIC: pick_target_specific,
        },
    )


def _opening_goals_reached(env: SiedlerScharfschuetzenEnv) -> bool:
    return (
        _count_buildings_by_alias(env, ["hochschule"]) >= 1
        and _has_researched(env, ["bildung"])
        and _count_buildings_by_alias(env, ["kloster"]) >= 1
        and _count_buildings_by_alias(env, ["dorfzentrum"]) >= 2
        and _count_buildings_by_alias(env, ["lehmhutte", "lehmhuette"]) >= 12
        and _count_buildings_by_alias(env, ["steinmetzhutte", "steinmetzhuette"]) >= 4
        and _count_buildings_by_alias(env, ["alchimistenhutte", "alchimistenhuette"]) >= 4
    )


def _run_opening_decision(
    env: SiedlerScharfschuetzenEnv,
    rng: np.random.Generator,
    state: OpeningPolicyState,
):
    if state.opening_done:
        return _run_random_decision(env, rng)

    cycle = int(env.current_time // INCOME_CYCLE)
    new_payday = cycle > state.last_payday_cycle
    if new_payday:
        state.last_payday_cycle = cycle

    if state.initial_serf_target is None:
        state.initial_serf_target = max(env.total_leibeigene, int(env._get_total_village_capacity()))

    # Immer segnen sobald verfuegbar (Kategorie 4 = alle Worker).
    result = _try_bless(env, rng, preferred_category=4)
    if result is not None:
        return result

    # Startphase: auf initiales Maximum aufstocken.
    if env.total_leibeigene < state.initial_serf_target:
        result = _try_buy_serf(env, rng)
        if result is not None:
            return result

    # 1) Alle Minen-Slots belegen (soweit baubar).
    mine_alias_groups = [
        ["steinmine_1", "steinmine"],
        ["eisenmine_1", "eisenmine"],
        ["lehmmine_1", "lehmmine"],
        ["schwefelmine_1", "schwefelmine"],
    ]
    for aliases in mine_alias_groups:
        result = _try_build_from_free(env, rng, aliases)
        if result is not None:
            return result

    # 2) Hochschule frueh bauen.
    if _count_buildings_and_sites(env, ["hochschule"]) < 1:
        result = _try_build_from_free(env, rng, ["hochschule_1", "hochschule"])
        if result is not None:
            return result

    # 3) "Steuer-Freischalt"-Schritt naeherungsweise ueber Bildung,
    #    danach Steuerstufe auf hoch setzen.
    if not _has_researched(env, ["bildung"]):
        result = _try_research(env, rng, tech_aliases=["bildung"], research_building_aliases=["hochschule"])
        if result is not None:
            return result
    has_bildung = _has_researched(env, ["bildung"])
    if has_bildung and env.current_tax_level < 4:
        result = _try_set_tax_level(env, rng, target_level=4)
        if result is not None:
            return result

    # 4) Kloster + zweites Dorfzentrum.
    if has_bildung and _count_buildings_and_sites(env, ["kloster"]) < 1:
        result = _try_build_from_free(env, rng, ["kloster_1", "kloster"])
        if result is not None:
            return result
    if has_bildung and _count_buildings_and_sites(env, ["dorfzentrum"]) < 2:
        result = _try_build_from_free(env, rng, ["dorfzentrum_1", "dorfzentrum"])
        if result is not None:
            return result

    # Nach zweitem DZ: zu Zahltagen weiter aufstocken (fruehe Spielphase).
    if new_payday and _count_buildings_by_alias(env, ["dorfzentrum"]) >= 2:
        topup_target = min(int(env._get_total_village_capacity()), 180)
        if env.total_leibeigene < topup_target:
            result = _try_buy_serf(env, rng)
            if result is not None:
                return result

    # 5) Produktionskette erst NACH Kloster + zweitem DZ.
    ready_for_industry = (
        _count_buildings_and_sites(env, ["kloster"]) >= 1
        and _count_buildings_and_sites(env, ["dorfzentrum"]) >= 2
    )

    if ready_for_industry and _count_buildings_and_sites(env, ["lehmhutte", "lehmhuette"]) < 12:
        if not _has_researched(env, ["konstruktion"]):
            result = _try_research(env, rng, tech_aliases=["konstruktion"], research_building_aliases=["hochschule"])
            if result is not None:
                return result
        result = _try_build_from_free(env, rng, ["lehmhutte_1", "lehmhuette_1", "lehmhutte", "lehmhuette"])
        if result is not None:
            return result

    if ready_for_industry and _count_buildings_and_sites(env, ["steinmetzhutte", "steinmetzhuette"]) < 4:
        if not _has_researched(env, ["zahnrader"]):
            result = _try_research(env, rng, tech_aliases=["zahnrader"], research_building_aliases=["hochschule"])
            if result is not None:
                return result
        result = _try_build_from_free(
            env, rng, ["steinmetzhutte_1", "steinmetzhuette_1", "steinmetzhutte", "steinmetzhuette"]
        )
        if result is not None:
            return result

    if ready_for_industry and _count_buildings_and_sites(env, ["alchimistenhutte", "alchimistenhuette"]) < 4:
        if not _has_researched(env, ["alchimie"]):
            result = _try_research(env, rng, tech_aliases=["alchimie"], research_building_aliases=["hochschule"])
            if result is not None:
                return result
        result = _try_build_from_free(
            env, rng, ["alchimistenhutte_1", "alchimistenhuette_1", "alchimistenhutte", "alchimistenhuette"]
        )
        if result is not None:
            return result

    # 6) Freie Leibeigene primär auf Holz und Stein verteilen.
    if env.free_leibeigene > 0:
        wood_target = min(70, max(20, env.total_leibeigene // 2))
        stone_target = min(45, max(12, env.total_leibeigene // 3))
        current_wood = int(getattr(env, "wood_serfs", 0))
        current_stone = int(getattr(env, "shaft_categories", {}).get("Stein", {}).get("serfs_assigned", 0))
        current_stone += int(getattr(env, "deposit_categories", {}).get("Stein", {}).get("serfs_assigned", 0))

        if current_stone < stone_target:
            result = _try_assign_free_to_category(env, rng, target_category=3, target_specific=0)
            if result is not None:
                return result

        if current_wood < wood_target:
            zone_idx = state.wood_zone_cursor % 6
            result = _try_assign_free_to_category(env, rng, target_category=1, target_specific=zone_idx)
            if result is not None:
                state.wood_zone_cursor += 1
                return result

    if _opening_goals_reached(env) or env.current_time >= 1200:
        state.opening_done = True

    return _run_wait_decision(env, rng)


def _run_one_decision(
    env: SiedlerScharfschuetzenEnv,
    rng: np.random.Generator,
    strategy: str,
    opening_state: Optional[OpeningPolicyState],
    expert_controller: Optional[ExpertOpeningController] = None,
):
    if strategy == "expert_opening":
        return _run_expert_decision(env, expert_controller or ExpertOpeningController())
    if strategy == "opening_v1":
        return _run_opening_decision(env, rng, opening_state or OpeningPolicyState())
    return _run_random_decision(env, rng)


def _remaining_path_points(unit) -> Iterable[Tuple[float, float]]:
    curr = _as_xy(getattr(unit, "position", None))
    if curr is not None:
        yield curr

    path = getattr(unit, "path", None) or []
    idx = int(getattr(unit, "path_index", 0) or 0)
    for wp in path[idx:]:
        xy = _as_xy(wp)
        if xy is not None:
            yield xy

    if bool(getattr(unit, "path_blocked", False)):
        return

    final = _as_xy(getattr(unit, "final_destination", None))
    if final is None:
        final = _as_xy(getattr(unit, "target_position", None))
    if final is not None:
        yield final


def _short_building_label(name: str, max_len: int = 14) -> str:
    base = get_base_building_name(name)
    if len(base) <= max_len:
        return base
    return base[: max_len - 3] + "..."


def _path_cache_key(env: SiedlerScharfschuetzenEnv, start_xy: Tuple[float, float], end_xy: Tuple[float, float]) -> Tuple[int, int, int, int, int]:
    rev = 0
    if hasattr(env, "_get_routing_revision"):
        try:
            rev = int(env._get_routing_revision())
        except Exception:
            rev = 0
    return (
        int(round(start_xy[0])),
        int(round(start_xy[1])),
        int(round(end_xy[0])),
        int(round(end_xy[1])),
        rev,
    )


def _get_cached_path(env: SiedlerScharfschuetzenEnv, start_xy: Tuple[float, float], end_xy: Tuple[float, float]):
    key = _path_cache_key(env, start_xy, end_xy)
    cached = _RENDER_PATH_CACHE.get(key)
    if cached is not None:
        return cached
    try:
        start = type("P", (), {"x": start_xy[0], "y": start_xy[1]})()
        end = type("P", (), {"x": end_xy[0], "y": end_xy[1]})()
        path, _ = env._compute_path(start, end)
    except Exception:
        path = []
    if not path:
        return None
    points = [(float(p.x), float(p.y)) for p in path]
    cum: List[float] = [0.0]
    total = 0.0
    for i in range(len(points) - 1):
        dx = points[i + 1][0] - points[i][0]
        dy = points[i + 1][1] - points[i][1]
        total += (dx * dx + dy * dy) ** 0.5
        cum.append(total)
    cached = (points, cum, total)
    _RENDER_PATH_CACHE[key] = cached
    return cached


def _point_along_path(points: List[Tuple[float, float]], cum: List[float], distance: float) -> Tuple[float, float]:
    if not points:
        return (0.0, 0.0)
    if distance <= 0:
        return points[0]
    total = cum[-1] if cum else 0.0
    if total <= 0:
        return points[-1]
    if distance >= total:
        return points[-1]
    for i in range(len(cum) - 1):
        if cum[i] <= distance <= cum[i + 1]:
            seg = cum[i + 1] - cum[i]
            if seg <= 0:
                return points[i + 1]
            ratio = (distance - cum[i]) / seg
            x = points[i][0] + ratio * (points[i + 1][0] - points[i][0])
            y = points[i][1] + ratio * (points[i + 1][1] - points[i][1])
            return (x, y)
    return points[-1]


def _worker_color(worker_state: str) -> Tuple[int, int, int, int]:
    return {
        "working": (60, 210, 255, 230),
        "walking_to_farm": (80, 200, 120, 230),
        "eating": (60, 180, 90, 230),
        "walking_to_residence": (230, 170, 80, 230),
        "resting": (200, 140, 60, 230),
        "walking_to_camp": (240, 220, 60, 230),
        "camping": (220, 200, 90, 230),
        "walking_to_work": (90, 160, 255, 230),
        "idle": (180, 180, 180, 230),
    }.get(worker_state, (70, 220, 255, 230))


def _serf_color(serf_state: str) -> Tuple[int, int, int, int]:
    return {
        "walking_to_resource": (255, 205, 70, 230),
        "extracting": (255, 170, 70, 230),
        "walking_to_build": (255, 200, 120, 230),
        "building": (255, 150, 60, 230),
        "idle": (200, 200, 200, 230),
    }.get(serf_state, (255, 205, 70, 230))


def _draw_frame(
    env: SiedlerScharfschuetzenEnv,
    base: np.ndarray,
    step_idx: int,
    total_steps: int,
    draw_paths: bool,
    max_paths: int,
    action_label: str = "wait",
    label_entities: bool = True,
    show_worker_states: bool = True,
    show_worker_targets: bool = True,
    show_refiner_trips: bool = True,
    max_refiner_trips: int = 120,
    show_hud: bool = True,
    show_debug_markers: bool = True,
) -> np.ndarray:
    grid_h = env.map_manager.grid.height
    grid_w = env.map_manager.grid.width
    base_h, base_w = base.shape[:2]
    px_scale_x = float(base_w) / max(1.0, float(grid_w))
    px_scale_y = float(base_h) / max(1.0, float(grid_h))

    def to_px(x: float, y: float) -> Tuple[int, int]:
        gx, gy = _world_to_px(env, x, y, grid_w, grid_h)
        px = max(0, min(base_w - 1, int(round(gx * px_scale_x))))
        py = max(0, min(base_h - 1, int(round(gy * px_scale_y))))
        return px, py

    def px_len_x(world_len: float) -> int:
        return max(1, int(round((float(world_len) / pathfinding.SCALE_X) * px_scale_x)))

    def px_len_y(world_len: float) -> int:
        return max(1, int(round((float(world_len) / pathfinding.SCALE_Y) * px_scale_y)))

    img = Image.fromarray(base.copy(), mode="RGB")
    draw = ImageDraw.Draw(img, mode="RGBA")
    font = ImageFont.load_default()

    # Ressourcen-Labels (Deposits / Shafts / Mine-Slots)
    if show_debug_markers:
        for category, cat_data in getattr(env, "deposit_categories", {}).items():
            deposits = cat_data.get("deposits", [])
            for idx, dep in enumerate(deposits, start=1):
                if dep.get("remaining", 0) <= 0:
                    continue
                x, y = to_px(dep.get("x", 0), dep.get("y", 0))
                draw.rectangle((x - 2, y - 2, x + 2, y + 2), fill=(250, 225, 80, 230))
                if label_entities:
                    draw.text((x + 3, y - 9), f"D-{category[:1]}{idx}", fill=(255, 245, 180, 230), font=font)

        for category, cat_data in getattr(env, "shaft_categories", {}).items():
            shafts = cat_data.get("shafts", [])
            for idx, shaft in enumerate(shafts, start=1):
                if shaft.get("remaining", 0) <= 0:
                    continue
                x, y = to_px(shaft.get("x", 0), shaft.get("y", 0))
                draw.rectangle((x - 2, y - 2, x + 2, y + 2), fill=(255, 180, 70, 230))
                if label_entities:
                    draw.text((x + 3, y + 2), f"S-{category[:1]}{idx}", fill=(255, 215, 140, 230), font=font)

        for mine_type, slots in getattr(env, "mine_positions", {}).items():
            built_set = set()
            for pos in getattr(env, "built_mines", {}).get(mine_type, []):
                if isinstance(pos, dict):
                    built_set.add((int(round(pos.get("x", 0))), int(round(pos.get("y", 0)))))
                else:
                    built_set.add((int(round(pos[0])), int(round(pos[1]))))
            for idx, slot in enumerate(slots, start=1):
                sx = slot.get("x", 0) if isinstance(slot, dict) else slot[0]
                sy = slot.get("y", 0) if isinstance(slot, dict) else slot[1]
                x, y = to_px(sx, sy)
                is_built = (int(round(sx)), int(round(sy))) in built_set
                color = (255, 90, 90, 230) if is_built else (210, 90, 90, 150)
                draw.rectangle((x - 3, y - 3, x + 3, y + 3), outline=color, width=1)
                if label_entities:
                    status = "B" if is_built else "F"
                    draw.text((x + 3, y - 10), f"M-{mine_type[:1]}{idx}{status}", fill=(255, 170, 170, 220), font=font)

    # Gebaeude + Baustellen
    for key, pos in env.building_position_map.items():
        xy = _as_xy(pos)
        if xy is None:
            continue
        building_name = key.rsplit("_", 1)[0] if key.rsplit("_", 1)[-1].isdigit() else key
        base_name = get_base_building_name(building_name)
        bw, bh = BUILDING_FOOTPRINTS.get(base_name, (400, 400))
        cx, cy = to_px(xy[0], xy[1])
        rx = max(1, px_len_x(bw) // 2)
        ry = max(1, px_len_y(bh) // 2)
        if show_debug_markers:
            draw.rectangle((cx - rx, cy - ry, cx + rx, cy + ry), outline=(255, 90, 90, 220), width=1)
            if label_entities:
                draw.text((cx - rx, cy - ry - 9), _short_building_label(base_name), fill=(255, 220, 220, 230), font=font)

    for site in env.construction_sites:
        xy = _as_xy(site.get("position"))
        if xy is None:
            continue
        x, y = to_px(xy[0], xy[1])
        if show_debug_markers:
            draw.rectangle((x - 3, y - 3, x + 3, y + 3), fill=(255, 170, 40, 230))
            if label_entities:
                site_name = _short_building_label(site.get("building", "site"))
                draw.text((x + 4, y - 9), f"site:{site_name}", fill=(255, 210, 130, 230), font=font)

    # Pfade
    if draw_paths:
        path_count = 0
        for worker in env.workforce_manager.workers:
            if path_count >= max_paths:
                break
            points = [
                to_px(x, y)
                for x, y in _remaining_path_points(worker)
            ]
            if len(points) >= 2:
                draw.line(points, fill=(80, 180, 255, 105), width=1)
                path_count += 1

        for serf in env.production_system.serfs:
            if path_count >= max_paths:
                break
            points = [
                to_px(x, y)
                for x, y in _remaining_path_points(serf)
            ]
            if len(points) >= 2:
                draw.line(points, fill=(255, 180, 60, 95), width=1)
                path_count += 1

    # Refiner-Trips (visualisiert den berechneten Rohstoff-Transport)
    if show_refiner_trips and show_debug_markers:
        speed_bonus = getattr(env.workforce_manager, "speed_bonus", 0)
        trip_count = 0
        for refiner in env.production_system.refiners.values():
            if trip_count >= max_refiner_trips:
                break
            start_xy = _as_xy(getattr(refiner, "position", None))
            end_xy = _as_xy(getattr(refiner, "supplier_position", None))
            if not start_xy or not end_xy:
                continue
            cached = _get_cached_path(env, start_xy, end_xy)
            if not cached:
                continue
            points, cum, total = cached
            if total <= 0:
                continue
            cycle_time = refiner.get_cycle_time(speed_bonus=speed_bonus)
            if not cycle_time or cycle_time <= 0 or cycle_time == float("inf"):
                continue

            # Pfadlinie
            line_points = [to_px(x, y) for x, y in points]
            if len(line_points) >= 2:
                draw.line(line_points, fill=(255, 120, 120, 110), width=1)

            # Bewegungspunkte (ein oder mehrere, je nach Workerzahl)
            count = max(1, min(int(getattr(refiner, "current_workers", 0) or 0), 3))
            base_phase = (env.current_time % cycle_time) / cycle_time
            for i in range(count):
                phase = (base_phase + (i / count)) % 1.0
                if phase < 0.5:
                    d = total * (phase * 2.0)
                    px, py = _point_along_path(points, cum, d)
                else:
                    d = total * ((1.0 - phase) * 2.0)
                    px, py = _point_along_path(points, cum, total - d)
                rx, ry = to_px(px, py)
                draw.ellipse((rx - 2, ry - 2, rx + 2, ry + 2), fill=(255, 90, 90, 230))
            trip_count += 1

    # Einheiten
    for worker in env.workforce_manager.workers:
        xy = _as_xy(getattr(worker, "position", None))
        if xy is None:
            continue
        x, y = to_px(xy[0], xy[1])
        state_value = getattr(worker.state, "value", str(getattr(worker, "state", "working")))
        if show_debug_markers:
            color = _worker_color(state_value) if show_worker_states else (70, 220, 255, 230)
            draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=color)
            if label_entities:
                short_state = state_value[:2].upper()
                draw.text((x + 2, y - 2), f"W{short_state}", fill=(170, 240, 255, 230), font=font)
        if show_worker_targets and show_debug_markers:
            tgt = _as_xy(getattr(worker, "final_destination", None)) or _as_xy(getattr(worker, "target_position", None))
            if tgt is not None:
                tx, ty = to_px(tgt[0], tgt[1])
                draw.ellipse((tx - 2, ty - 2, tx + 2, ty + 2), outline=(120, 220, 255, 180), width=1)

    for serf in env.production_system.serfs:
        xy = _as_xy(getattr(serf, "position", None))
        if xy is None:
            continue
        x, y = to_px(xy[0], xy[1])
        state_value = getattr(serf.state, "value", str(getattr(serf, "state", "idle")))
        if show_debug_markers:
            color = _serf_color(state_value) if show_worker_states else (255, 205, 70, 230)
            draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=color)
            if label_entities:
                short_state = state_value[:2].upper()
                draw.text((x + 2, y + 1), f"S{short_state}", fill=(255, 228, 140, 230), font=font)
        if show_worker_targets and show_debug_markers:
            tgt = _as_xy(getattr(serf, "target_position", None))
            if tgt is not None:
                tx, ty = to_px(tgt[0], tgt[1])
                draw.ellipse((tx - 2, ty - 2, tx + 2, ty + 2), outline=(255, 200, 120, 180), width=1)

    if show_hud:
        hud_lines = [
            f"step {step_idx}/{total_steps}  time {env.current_time}s",
            f"action {action_label}",
            f"buildings {len(env.building_position_map)}  workers {len(env.workforce_manager.workers)}  serfs {len(env.production_system.serfs)}",
            f"res HolzRoh={int(env.resources.get('HolzRoh', 0))} EisenRoh={int(env.resources.get('EisenRoh', 0))} Taler={int(env.resources.get('Taler', 0))}",
        ]
        hud_text = "\n".join(hud_lines)
        draw.rectangle((6, 6, 620, 82), fill=(0, 0, 0, 155))
        draw.text((12, 10), hud_text, fill=(255, 255, 255, 230), font=font)

    return np.asarray(img, dtype=np.uint8)


def _apply_viewport(frame: np.ndarray, viewport: str) -> np.ndarray:
    if viewport == "full":
        return frame

    h, w = frame.shape[:2]
    if viewport == "bottom_right":
        cropped = frame[h // 2 :, w // 2 :, :]
    else:
        return frame

    # Zurueck auf Originalgroesse fuer konstante Video-Dims.
    img = Image.fromarray(cropped, mode="RGB")
    resized = img.resize((w, h), Image.Resampling.BILINEAR)
    return np.asarray(resized, dtype=np.uint8)


def _scale_frame(frame: np.ndarray, scale: int) -> np.ndarray:
    scale = max(1, int(scale))
    if scale <= 1:
        return frame
    h, w = frame.shape[:2]
    img = Image.fromarray(frame, mode="RGB")
    img = img.resize((w * scale, h * scale), Image.Resampling.NEAREST)
    return np.asarray(img, dtype=np.uint8)


def _parse_snapshot_times(raw: str) -> List[int]:
    result: List[int] = []
    for part in str(raw or "").split(","):
        part = part.strip()
        if not part:
            continue
        try:
            result.append(max(0, int(part)))
        except ValueError:
            continue
    return sorted(set(result))


def _maybe_write_snapshot(
    frame: np.ndarray,
    env: SiedlerScharfschuetzenEnv,
    snapshot_dir: str,
    snapshot_times: List[int],
    written: set,
) -> None:
    if not snapshot_dir or not snapshot_times:
        return
    current_time = int(getattr(env, "current_time", 0))
    due = [t for t in snapshot_times if t <= current_time and t not in written]
    if not due:
        return
    os.makedirs(snapshot_dir, exist_ok=True)
    for target_time in due:
        out_path = os.path.join(snapshot_dir, f"expert_opening_t{target_time:04d}.png")
        Image.fromarray(frame, mode="RGB").save(out_path)
        written.add(target_time)


def parse_args():
    parser = argparse.ArgumentParser(description="Render MP4 replay fuer Siedler-Env")
    parser.add_argument("--steps", type=int, default=1800, help="Anzahl Simulations-Schritte (z.B. 1800)")
    parser.add_argument("--frame-every", type=int, default=1, help="Nur jeden N-ten Schritt als Frame schreiben")
    parser.add_argument("--fps", type=int, default=24, help="FPS des MP4")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output", type=str, default="replay_player1.mp4", help="Output MP4 Pfad")
    parser.add_argument("--background", type=str, default="", help="Optionales Player-PNG als Hintergrund")
    parser.add_argument(
        "--sim-mode",
        type=str,
        choices=["", "fast_train", "full_sim"],
        default="",
        help="Simulationsmodus. Leer = Env-Default, expert_opening nutzt automatisch full_sim.",
    )
    parser.add_argument(
        "--render-scale",
        type=int,
        default=1,
        help="Pixel-Upscale fuer Video/Snapshots. 4 ist gut zum Pruefen.",
    )
    parser.add_argument(
        "--snapshot-dir",
        type=str,
        default="",
        help="Optionaler Ordner fuer PNG-Snapshots bei --snapshot-times.",
    )
    parser.add_argument(
        "--snapshot-times",
        type=str,
        default="",
        help="Kommagetrennte Sim-Zeiten fuer PNG-Snapshots, z.B. 0,30,76,147,195,196.",
    )
    parser.add_argument(
        "--background-crop-p1",
        action="store_true",
        help="Falls --background eine Vollkarten-PNG ist: auf P1-Quadrant (oben rechts) croppen",
    )
    parser.add_argument(
        "--strategy",
        type=str,
        choices=["expert_opening", "opening_v1", "random"],
        default="expert_opening",
        help="Policy fuer Entscheidungen: expert_opening, opening_v1 oder random",
    )
    parser.add_argument(
        "--viewport",
        type=str,
        choices=["full", "bottom_right"],
        default="full",
        help="Render-Viewport: vollstaendige P1-Flaeche oder nur unten rechts",
    )
    parser.add_argument("--no-paths", action="store_true", help="Pfade nicht zeichnen")
    parser.add_argument(
        "--no-entity-labels",
        action="store_true",
        help="Keine Textlabels fuer Gebaeude/Ressourcen/Einheiten zeichnen",
    )
    parser.add_argument(
        "--no-worker-states",
        action="store_true",
        help="Keine farbcodierten Worker/Serf-States zeichnen",
    )
    parser.add_argument(
        "--no-worker-targets",
        action="store_true",
        help="Keine Ziel-Markierungen fuer Worker/Serfs zeichnen",
    )
    parser.add_argument(
        "--no-refiner-trips",
        action="store_true",
        help="Keine Refinery-Transportpfade zeichnen",
    )
    parser.add_argument("--no-hud", action="store_true", help="HUD mit Zeit/Aktion/Ressourcen nicht zeichnen")
    parser.add_argument(
        "--max-refiner-trips",
        type=int,
        default=120,
        help="Maximal gezeichnete Refinery-Transportpfade pro Frame",
    )
    parser.add_argument(
        "--max-paths",
        type=int,
        default=1200,
        help="Maximal gezeichnete Pfade pro Frame (Performance/Lesbarkeit)",
    )
    parser.add_argument(
        "--assign-qty-max",
        type=int,
        default=-1,
        help="Maximaler QUANTITY-Index fuer assign_serf (0=1,1=2,2=3,3=5,4=10,5=20). -1 = Standard (max).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    sim_mode = str(args.sim_mode or "").strip()
    if not sim_mode and args.strategy == "expert_opening":
        sim_mode = "full_sim"
    if sim_mode:
        os.environ["SIEDLER_SIM_MODE"] = sim_mode
        if sim_mode == "full_sim":
            os.environ["SIEDLER_DISABLE_RUNTIME_PATHING"] = "0"

    global MAX_ASSIGN_QUANTITY_INDEX
    if args.assign_qty_max is not None and int(args.assign_qty_max) >= 0:
        MAX_ASSIGN_QUANTITY_INDEX = int(args.assign_qty_max)
    else:
        MAX_ASSIGN_QUANTITY_INDEX = None

    env = SiedlerScharfschuetzenEnv(render_mode=None, use_spatial_obs=False)
    env._background_crop_p1 = bool(args.background_crop_p1)
    env.reset(seed=args.seed)
    rng = np.random.default_rng(args.seed)
    opening_state = OpeningPolicyState() if args.strategy == "opening_v1" else None
    expert_controller = ExpertOpeningController() if args.strategy == "expert_opening" else None
    snapshot_times = _parse_snapshot_times(args.snapshot_times)
    written_snapshots = set()

    base = _make_base_image(env, args.background or None)
    out_dir = os.path.dirname(os.path.abspath(args.output))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    writer = imageio.get_writer(
        args.output,
        fps=max(1, int(args.fps)),
        codec="libx264",
        quality=8,
        macro_block_size=1,
    )

    try:
        last_action_label = "reset"
        # Initial frame
        frame0 = _draw_frame(
            env,
            base,
            0,
            args.steps,
            not args.no_paths,
            args.max_paths,
            action_label=last_action_label,
            label_entities=not args.no_entity_labels,
            show_worker_states=not args.no_worker_states,
            show_worker_targets=not args.no_worker_targets,
            show_refiner_trips=not args.no_refiner_trips,
            max_refiner_trips=args.max_refiner_trips,
            show_hud=not args.no_hud,
        )
        frame0 = _apply_viewport(frame0, args.viewport)
        frame0 = _scale_frame(frame0, args.render_scale)
        writer.append_data(frame0)
        _maybe_write_snapshot(frame0, env, args.snapshot_dir, snapshot_times, written_snapshots)

        decisions = 0
        done = False
        trunc = False
        while decisions < args.steps and not done and not trunc:
            result = _run_one_decision(env, rng, args.strategy, opening_state, expert_controller)
            if result is None:
                break
            _, _, done, trunc, info = result
            last_action_label = str(info.get("action_name", "unknown"))
            decisions += 1
            if decisions % max(1, args.frame_every) == 0:
                frame = _draw_frame(
                    env,
                    base,
                    decisions,
                    args.steps,
                    not args.no_paths,
                    args.max_paths,
                    action_label=last_action_label,
                    label_entities=not args.no_entity_labels,
                    show_worker_states=not args.no_worker_states,
                    show_worker_targets=not args.no_worker_targets,
                    show_refiner_trips=not args.no_refiner_trips,
                    max_refiner_trips=args.max_refiner_trips,
                    show_hud=not args.no_hud,
                )
                frame = _apply_viewport(frame, args.viewport)
                frame = _scale_frame(frame, args.render_scale)
                writer.append_data(frame)
                _maybe_write_snapshot(frame, env, args.snapshot_dir, snapshot_times, written_snapshots)
    finally:
        writer.close()

    print(f"Replay gespeichert: {args.output}")
    print(f"Schritte simuliert: {decisions}")
    print(f"Frame-Intervall: {max(1, args.frame_every)}")
    print(f"Strategie: {args.strategy}")
    print(f"Simulation mode: {env.sim_mode}")
    print(f"Viewport: {args.viewport}")
    if args.snapshot_dir:
        print(f"Snapshots: {args.snapshot_dir}")


if __name__ == "__main__":
    main()
