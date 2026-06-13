# -*- coding: utf-8 -*-
"""Konformitaetstests fuer Action-Flow, Placement und Worker-Truth."""

import json
from pathlib import Path

import numpy as np
import pytest

import pathfinding
from original_game_values import aliases_for_technology, load_building_geometry, load_technology_xml_values
from map_config_wintersturm import (
    PLAYER_1_SMALL_DEPOSITS,
    PLAYER_1_TREES_SUMMARY,
    PLAYER_1_VILLAGE_CENTER_SLOTS,
    PLAYER_HQ_POSITIONS,
    PLAYER_START_BUILDINGS,
    START_RESOURCES,
)
from environment import (
    ACTION_FLOWS,
    BUILD_CATEGORIES,
    COHORT_BASE_TYPES,
    COHORT_OBS_FEATURES_PER_SLOT,
    INITIAL_LEIBEIGENE,
    MAIN_ACTIONS,
    MAXIMUM_FAITH,
    MAX_COMPLETED_SERF_COHORTS,
    POSITION_MODES,
    QUANTITY_VALUES,
    SNOW_MOVE_SPEED_FACTOR,
    ActionPhase,
    SerfArea,
    SiedlerScharfschuetzenEnv,
    WEATHER_RAIN,
    WEATHER_SNOW,
    WEATHER_SUMMER,
    TECHNOLOGY_EFFECTS,
    buildings_db,
    technologies,
)
from production_system import Refiner, ResourceType
from worker_simulation import (
    Camp,
    Farm,
    FORCE_TO_WORK_PENALTY,
    Position,
    Residence,
    Worker,
    WorkerState,
    WORKER_CAMPER_RANGE,
    WORKER_CONFIG_SOURCE,
    WORKER_PARAMS,
    WORKER_SPEEDS,
    WORKTIME_BASE,
    WORKTIME_THRESHOLD_WORK,
    normalize_worker_type,
)


PROJECT_ROOT = Path(__file__).resolve().parent
WORKER_TRUTH_PATH = PROJECT_ROOT / "config" / "worker_truth_model.json"
FULL_WORKER_ENGINE_PATH = PROJECT_ROOT / "config" / "full_worker_engine_behavior.json"


def test_wintersturm_starts_without_free_serfs_but_can_buy_first_serf():
    env = SiedlerScharfschuetzenEnv(use_spatial_obs=False)
    env.reset(seed=0)

    assert INITIAL_LEIBEIGENE == 0
    assert env.total_leibeigene == 0
    assert env.free_leibeigene == 0
    assert env.serf_areas[SerfArea.FREE]["count"] == 0
    assert env._can_buy_serf()

    assert env.step(MAIN_ACTIONS.index("buy_serf"))[4].get("invalid_action") is not True
    assert env.step(0)[4].get("invalid_action") is not True

    assert env.total_leibeigene == 1
    assert env.free_leibeigene == 1
    assert env.serf_areas[SerfArea.FREE]["count"] == 1


def _safe_int(value, default):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _safe_float(value, default):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _extract_truth_changes_per_cycle(worker_truth):
    counts = []
    work_cycle = worker_truth.get("work_cycle_truth") or {}

    primary = work_cycle.get("primary_work_tasklist") or {}
    if isinstance(primary, dict):
        count = primary.get("task_change_work_time_work_count")
        if isinstance(count, int) and count > 0:
            counts.append(count)

    miner_tasklists = work_cycle.get("miner_tasklists") or {}
    if isinstance(miner_tasklists, dict):
        for tasklist in miner_tasklists.values():
            if not isinstance(tasklist, dict):
                continue
            count = tasklist.get("task_change_work_time_work_count")
            if isinstance(count, int) and count > 0:
                counts.append(count)

    return max(counts) if counts else 1


def _load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _grant_free_serfs(env, count=10):
    env.resources["Taler"] = max(float(env.resources.get("Taler", 0)), float(count * 100))
    while env.free_leibeigene < count:
        env._buy_serf()
    env.serf_areas[SerfArea.FREE]["count"] = env.free_leibeigene
    env._pending_spawned_unassigned_serfs = 0
    env._best_total_leibeigene = max(int(env._best_total_leibeigene), int(env.total_leibeigene))
    env._can_cache = {}


def _first_assignable_wood_specific(env, batch_size):
    available_free = max(int(env.free_leibeigene), int(batch_size))
    for specific_idx in range(env.target_specific_size):
        tree_idx = env._get_wood_zone_rank_tree_index(
            specific_idx,
            batch_size,
            mode="assign",
            available_free_override=available_free,
        )
        if tree_idx is not None:
            return specific_idx
    raise AssertionError("No assignable wood target found")


def _first_assignable_target_specific(env, target_cat, batch_size):
    previous_flow = env.current_flow
    previous_phase = env.current_phase
    previous_selections = dict(env.pending_selections)
    try:
        env.current_flow = "assign_serf"
        env.current_phase = ActionPhase.TARGET_SPECIFIC
        env.pending_selections = {
            ActionPhase.SOURCE_CATEGORY: 7,
            ActionPhase.SOURCE_SPECIFIC: 0,
            ActionPhase.QUANTITY: QUANTITY_VALUES.index(batch_size),
            ActionPhase.TARGET_CATEGORY: target_cat,
        }
        mask = env._mask_target_specific()
        valid = np.flatnonzero(mask)
        if len(valid):
            return int(valid[0])
    finally:
        env.current_flow = previous_flow
        env.current_phase = previous_phase
        env.pending_selections = previous_selections
    raise AssertionError(f"No assignable target for category {target_cat} and batch {batch_size}")


def _first_valid_build_position_selection(env, building, selections):
    full = dict(selections)
    full.setdefault(ActionPhase.POSITION_MODE, 0)
    valid_mask = env._get_build_position_valid_mask_for_selections(building, full)
    valid = np.flatnonzero(valid_mask)
    if len(valid) == 0:
        raise AssertionError(f"No valid build position for {building}")
    global_idx = int(valid[0])
    group_size = env.action_spaces[ActionPhase.POSITION_INDEX].n
    full[ActionPhase.POSITION_GROUP] = global_idx // group_size
    full[ActionPhase.POSITION_INDEX] = global_idx % group_size
    return full


def test_spawned_serf_cohort_can_be_split_for_exact_assignment():
    env = SiedlerScharfschuetzenEnv(use_spatial_obs=False)
    env.reset(seed=1)
    env.resources["Taler"] = 50_000
    env.buildings["Dorfzentrum_1"] = max(4, env.buildings.get("Dorfzentrum_1", 0))
    env._can_cache = {}

    env._execute_action("buy_serf", {ActionPhase.QUANTITY: 2})  # QUANTITY_VALUES[2] == 3

    assert env.total_leibeigene == 3
    assert env.free_leibeigene == 3
    assert len(env.free_serf_cohorts) == 1
    assert env.free_serf_cohorts[0]["base"] == "Rekrutiert"
    original_ids = set(env.free_serf_cohorts[0]["serf_ids"])
    assert len(original_ids) == 3

    env.current_flow = "assign_serf"
    env.current_phase = ActionPhase.QUANTITY
    env.pending_selections = {ActionPhase.SOURCE_CATEGORY: 7, ActionPhase.SOURCE_SPECIFIC: 0}
    qty_mask = env._mask_quantity()
    assert qty_mask[QUANTITY_VALUES.index(2)]
    assert not qty_mask[QUANTITY_VALUES.index(4)]
    env.current_flow = None
    env.current_phase = ActionPhase.MAIN
    env.pending_selections = {}

    wood_specific = _first_assignable_wood_specific(env, batch_size=2)
    env._execute_action(
        "assign_serf",
        {
            ActionPhase.SOURCE_CATEGORY: 7,
            ActionPhase.SOURCE_SPECIFIC: 0,
            ActionPhase.QUANTITY: 1,  # QUANTITY_VALUES[1] == 2
            ActionPhase.TARGET_CATEGORY: 1,
            ActionPhase.TARGET_SPECIFIC: wood_specific,
        },
    )

    assert env.wood_serfs == 2
    assert env.free_leibeigene == 1
    assert len(env.free_serf_cohorts) == 1
    remaining_ids = set(env.free_serf_cohorts[0]["serf_ids"])
    assert len(remaining_ids) == 1
    assert remaining_ids < original_ids


def test_spawned_serf_cohort_supports_one_to_twenty_and_repeated_splits():
    env = SiedlerScharfschuetzenEnv(use_spatial_obs=False)
    env.reset(seed=12)
    env.resources["Taler"] = 50_000
    env.buildings["Dorfzentrum_1"] = max(4, env.buildings.get("Dorfzentrum_1", 0))
    env._can_cache = {}

    env._execute_action("buy_serf", {ActionPhase.QUANTITY: QUANTITY_VALUES.index(20)})

    assert QUANTITY_VALUES == list(range(1, 21))
    assert env.total_leibeigene == 20
    assert env.free_leibeigene == 20
    assert len(env.free_serf_cohorts) == 1
    assert env.free_serf_cohorts[0]["count"] == 20

    env.current_flow = "assign_serf"
    env.current_phase = ActionPhase.QUANTITY
    env.pending_selections = {ActionPhase.SOURCE_CATEGORY: 7, ActionPhase.SOURCE_SPECIFIC: 0}
    qty_mask = env._mask_quantity()
    assert all(qty_mask[QUANTITY_VALUES.index(qty)] for qty in range(1, 21))
    env.current_flow = None
    env.current_phase = ActionPhase.MAIN
    env.pending_selections = {}

    splits = [(3, 2), (4, 3), (8, 4)]  # Eisen, Stein, Lehm
    expected_remaining = 20
    for qty, target_cat in splits:
        target_specific = _first_assignable_target_specific(env, target_cat, qty)
        env._execute_action(
            "assign_serf",
            {
                ActionPhase.SOURCE_CATEGORY: 7,
                ActionPhase.SOURCE_SPECIFIC: 0,
                ActionPhase.QUANTITY: QUANTITY_VALUES.index(qty),
                ActionPhase.TARGET_CATEGORY: target_cat,
                ActionPhase.TARGET_SPECIFIC: target_specific,
            },
        )
        expected_remaining -= qty
        assert len(env.free_serf_cohorts) == 1
        assert env.free_serf_cohorts[0]["count"] == expected_remaining
        assert env.free_leibeigene == expected_remaining


def test_free_serf_cohort_observation_exposes_type_count_and_position():
    env = SiedlerScharfschuetzenEnv(use_spatial_obs=False)
    env.reset(seed=13)
    env.resources["Taler"] = 50_000
    env.buildings["Dorfzentrum_1"] = max(4, env.buildings.get("Dorfzentrum_1", 0))
    env._can_cache = {}

    env._execute_action("buy_serf", {ActionPhase.QUANTITY: QUANTITY_VALUES.index(3)})

    values = []
    env._append_free_cohort_observation(values)
    assert len(values) == MAX_COMPLETED_SERF_COHORTS * COHORT_OBS_FEATURES_PER_SLOT

    first = values[:COHORT_OBS_FEATURES_PER_SLOT]
    assert first[0] == pytest.approx(1.0)
    assert first[1] == pytest.approx(3.0 / 20.0)
    assert first[2] > 0.0
    assert first[3] > 0.0
    base_start = 5
    assert first[base_start + COHORT_BASE_TYPES.index("Rekrutiert")] == pytest.approx(1.0)


def test_completed_building_cohort_can_partially_build_next_site():
    env = SiedlerScharfschuetzenEnv(use_spatial_obs=False)
    env.reset(seed=2)
    _grant_abundant_resources(env)
    _grant_free_serfs(env, 4)

    from worker_simulation import Position

    source_site = {
        "building": "Kloster_1",
        "position": {"x": int(env.hq_position[0] + 1200), "y": int(env.hq_position[1] + 800)},
        "total_time": 140.0,
        "remaining_work": 0.0,
        "serfs_assigned": 0,
        "site_id": 1001,
    }
    env.construction_sites.append(source_site)
    source_pos = Position(x=source_site["position"]["x"], y=source_site["position"]["y"])
    builders = env._select_idle_serfs_nearest_to(source_pos, 4)
    assert len(builders) == 4
    assert env._assign_specific_serfs_to_construction_site(builders, 0, quantity=4) == 4

    env._release_serfs_from_site(source_site, register_cohort=True)

    assert len(env.free_serf_cohorts) == 1
    assert env.free_serf_cohorts[0]["base"] == "Kloster"
    source_ids = set(env.free_serf_cohorts[0]["serf_ids"])
    assert len(source_ids) == 4

    env.current_flow = "build"
    env.current_phase = ActionPhase.QUANTITY
    env.pending_selections = {ActionPhase.SOURCE_CATEGORY: 7, ActionPhase.SOURCE_SPECIFIC: 0}
    qty_mask = env._mask_quantity()
    assert qty_mask[QUANTITY_VALUES.index(4)]
    env.current_flow = None
    env.current_phase = ActionPhase.MAIN
    env.pending_selections = {}

    building = "Wohnhaus_1"
    category_idx = env._get_build_category_index(building)
    category_buildings = env._get_buildings_for_build_category(category_idx)
    selections = _first_valid_build_position_selection(
        env,
        building,
        {
            ActionPhase.SOURCE_CATEGORY: 7,
            ActionPhase.SOURCE_SPECIFIC: 0,
            ActionPhase.QUANTITY: 1,  # QUANTITY_VALUES[1] == 2
            ActionPhase.BUILD_CATEGORY: category_idx,
            ActionPhase.BUILDING: category_buildings.index(building),
            ActionPhase.POSITION_MODE: 0,
        },
    )
    env._execute_action(
        "build",
        selections,
    )

    newest_site = env.construction_sites[-1]
    assert newest_site["building"] == building
    assert newest_site["serfs_assigned"] == 2
    assigned_ids = {
        env._ensure_serf_identity(serf)
        for serf in env.production_system.serfs
        if serf.build_site_id == newest_site["site_id"]
    }
    assert len(assigned_ids) == 2
    assert assigned_ids <= source_ids
    assert len(env.free_serf_cohorts) == 1
    assert set(env.free_serf_cohorts[0]["serf_ids"]) == source_ids - assigned_ids


def _grant_abundant_resources(env):
    for key in list(env.resources.keys()):
        env.resources[key] = 1_000_000
    _grant_free_serfs(env, 10)


def _prepare_env_for_action(env, action_name):
    _grant_abundant_resources(env)
    env.base_motivation = 1.0
    env.faith = 1_000_000
    env.current_researches = []
    env.researched_techs = set()
    env.bless_cooldowns = {k: 0 for k in env.bless_cooldowns}

    if action_name in {"upgrade", "demolish"}:
        env.buildings["Wohnhaus_1"] = max(1, env.buildings.get("Wohnhaus_1", 0))

    if action_name == "research":
        env.buildings["Hochschule_1"] = max(1, env.buildings.get("Hochschule_1", 0))

    if action_name == "recruit":
        env.buildings["Kaserne_1"] = max(1, env.buildings.get("Kaserne_1", 0))

    if action_name == "buy_serf":
        env.buildings["Dorfzentrum_1"] = max(4, env.buildings.get("Dorfzentrum_1", 0))
        env.total_leibeigene = min(env.total_leibeigene, 10)
        env.free_leibeigene = min(env.free_leibeigene, env.total_leibeigene)
        env.serf_areas[SerfArea.FREE]["count"] = env.free_leibeigene

    if action_name in {"dismiss_serf", "assign_serf"}:
        env.total_leibeigene = max(10, env.total_leibeigene)
        env.free_leibeigene = max(5, env.free_leibeigene)
        env.serf_areas[SerfArea.FREE]["count"] = env.free_leibeigene

    if action_name == "bless":
        env.buildings["Kloster_1"] = max(1, env.buildings.get("Kloster_1", 0))
        env.faith = 1_000_000

    if action_name == "tax":
        env.researched_techs.add("Bildung")

    if action_name == "cancel_build":
        env.construction_sites.append(
            {
                "building": "Wohnhaus_1",
                "position": {"x": env.hq_position[0] + 1000, "y": env.hq_position[1]},
                "total_time": 80.0,
                "remaining_work": 80.0,
                "serfs_assigned": 0,
                "site_id": 9876,
            }
        )

    if action_name == "cancel_research":
        env.buildings["Hochschule_1"] = max(1, env.buildings.get("Hochschule_1", 0))
        tech = next(t for t in env.tech_by_building["Hochschule"] if not technologies.get(t, {}).get("disabled"))
        env.current_researches = [(tech, 10.0)]
        env.researching_set.add(tech)

    if action_name == "cancel_recruit":
        soldier = env.soldier_types[0]
        env.recruit_queue = [(soldier, 10.0)]



def _first_valid(mask, size):
    valid = np.flatnonzero(mask[:size])
    if len(valid) == 0:
        return 0
    return int(valid[0])


def _choose_phase_action(env, action_name, phase, mask):
    size = env.action_spaces[phase].n

    if action_name in {"assign_serf", "dismiss_serf"} and phase == ActionPhase.SOURCE_CATEGORY:
        return 0 if size > 0 and mask[0] else _first_valid(mask, size)

    if action_name == "assign_serf" and phase == ActionPhase.SOURCE_SPECIFIC:
        return 0

    if action_name == "assign_serf" and phase == ActionPhase.TARGET_CATEGORY:
        if size > 7 and mask[7]:
            return 7
        return _first_valid(mask, size)

    if phase in {ActionPhase.POSITION_GROUP, ActionPhase.POSITION_INDEX, ActionPhase.QUANTITY}:
        return _first_valid(mask, size)

    return _first_valid(mask, size)


def _run_complete_flow(env, action_name):
    main_idx = MAIN_ACTIONS.index(action_name)
    main_size = env.action_spaces[ActionPhase.MAIN].n
    assert main_idx < main_size

    main_mask = env.action_masks()
    assert bool(main_mask[main_idx]), f"Main action {action_name} ist nicht legal maskiert"

    _, _, _, _, info = env.step(main_idx)

    guard = 0
    while info.get("multi_step"):
        guard += 1
        assert guard <= 32, f"Flow {action_name} endet nicht (guard reached)"

        phase = env.current_phase
        size = env.action_spaces[phase].n
        mask = env.action_masks()
        assert mask[:size].any(), f"Phase {phase.value} von {action_name} hat keine legalen Optionen"

        choice = _choose_phase_action(env, action_name, phase, mask)
        _, _, _, _, info = env.step(choice)

    assert env.current_phase == ActionPhase.MAIN
    assert env.current_flow is None


def test_full_worker_engine_behavior_extract_coverage():
    assert FULL_WORKER_ENGINE_PATH.exists(), f"Fehlt: {FULL_WORKER_ENGINE_PATH}"
    full = _load_json(FULL_WORKER_ENGINE_PATH)

    meta = full.get("meta") or {}
    counts = meta.get("source_file_counts") or {}
    assert meta.get("source_root", "").endswith("Gold edition")
    assert counts.get("tasklists_effective", 0) == len(full.get("tasklists") or {})
    assert counts.get("tasklist_layer_files", 0) >= counts.get("tasklists_effective", 0)
    assert counts.get("entity_layer_files", 0) >= counts.get("entities_effective", 0)
    assert meta.get("tasklist_count", 0) >= 300
    assert meta.get("worker_entity_count", 0) >= 18
    assert meta.get("worker_building_count", 0) >= 40
    assert meta.get("reachable_worker_tasklist_count", 0) >= 200
    assert full.get("unresolved_worker_tasklists") == []

    workers = full.get("worker_entities") or {}
    for required in ["pu_serf", "pu_farmer", "pu_miner", "pu_trader", "pu_tavernbarkeeper"]:
        assert required in workers
        assert workers[required].get("task_graph", {}).get("reachable_tasklists")

    market = (full.get("worker_buildings") or {}).get("pb_market2") or {}
    assert len(market.get("work_tasklists") or []) == 4
    assert (full.get("runtime") or {}).get("workers", {}).get("trader", {}).get(
        "worktime_changes_per_cycle"
    ) == 2


def test_worker_truth_alignment():
    assert WORKER_CONFIG_SOURCE in {
        "full_worker_engine_behavior",
        "worker_truth_model",
        "defaults",
    }
    if WORKER_CONFIG_SOURCE == "full_worker_engine_behavior":
        assert FULL_WORKER_ENGINE_PATH.exists(), f"Fehlt: {FULL_WORKER_ENGINE_PATH}"
        truth = _load_json(FULL_WORKER_ENGINE_PATH)
        logic = (truth.get("runtime") or {}).get("global_worktime") or {}
        workers = (truth.get("runtime") or {}).get("workers") or {}
        full_runtime = True
    else:
        assert WORKER_TRUTH_PATH.exists(), f"Fehlt: {WORKER_TRUTH_PATH}"
        truth = _load_json(WORKER_TRUTH_PATH)
        logic = (truth.get("global_truth") or {}).get("logic_worktime") or {}
        workers = truth.get("workers") or {}
        full_runtime = False

    assert WORKTIME_BASE == _safe_int(logic.get("base"), WORKTIME_BASE)
    assert WORKTIME_THRESHOLD_WORK == _safe_int(
        logic.get("threshold_work"), WORKTIME_THRESHOLD_WORK
    )
    assert abs(
        FORCE_TO_WORK_PENALTY
        - _safe_float(logic.get("force_to_work_penalty"), FORCE_TO_WORK_PENALTY)
    ) < 1e-9

    for raw_name, data in workers.items():
        if not isinstance(data, dict):
            continue

        env_name = data.get("env_name") or raw_name
        worker_name = normalize_worker_type(str(env_name))

        if full_runtime:
            speed_truth = _safe_int(data.get("speed"), 320)
            camper_truth = _safe_int(data.get("camper_range"), 5000)
        else:
            movement = data.get("movement") or {}
            speed_truth = _safe_int(movement.get("speed"), 320)
            camper_truth = _safe_int(movement.get("camper_range"), 5000)

        assert WORKER_SPEEDS.get(worker_name) == speed_truth, (
            f"Speed-Mismatch {worker_name}: sim={WORKER_SPEEDS.get(worker_name)} truth={speed_truth}"
        )

        sim_camper = WORKER_CAMPER_RANGE.get(worker_name, 5000)
        assert sim_camper == camper_truth, (
            f"CamperRange-Mismatch {worker_name}: sim={sim_camper} truth={camper_truth}"
        )

        if not data.get("has_worktime", False):
            continue

        assert worker_name in WORKER_PARAMS, f"Worker-Params fehlen fuer {worker_name}"
        params = WORKER_PARAMS[worker_name]
        wt = data.get("worktime") if full_runtime else data.get("worktime_truth")
        wt = wt or {}

        assert params.work_wait_until == _safe_int(wt.get("work_wait_until"), params.work_wait_until)
        assert params.eat_wait == _safe_int(wt.get("eat_wait"), params.eat_wait)
        assert params.rest_wait == _safe_int(wt.get("rest_wait"), params.rest_wait)
        assert params.work_time_change_work == _safe_int(
            wt.get("work_time_change_work"), params.work_time_change_work
        )
        assert abs(
            params.work_time_change_farm
            - _safe_float(wt.get("work_time_change_farm"), params.work_time_change_farm)
        ) < 1e-9
        assert abs(
            params.work_time_change_residence
            - _safe_float(wt.get("work_time_change_residence"), params.work_time_change_residence)
        ) < 1e-9
        assert abs(
            params.work_time_change_camp
            - _safe_float(wt.get("work_time_change_camp"), params.work_time_change_camp)
        ) < 1e-9
        assert params.work_time_max_farm == _safe_int(
            wt.get("work_time_max_farm"), params.work_time_max_farm
        )
        assert params.work_time_max_residence == _safe_int(
            wt.get("work_time_max_residence"), params.work_time_max_residence
        )
        assert abs(
            params.exhausted_malus - _safe_float(wt.get("exhausted_malus"), params.exhausted_malus)
        ) < 1e-9

        expected_changes = (
            _safe_int(data.get("worktime_changes_per_cycle"), 1)
            if full_runtime
            else _extract_truth_changes_per_cycle(data)
        )
        assert params.worktime_changes_per_cycle == expected_changes, (
            f"worktime_changes_per_cycle mismatch {worker_name}: "
            f"sim={params.worktime_changes_per_cycle}, truth={expected_changes}"
        )



def test_main_action_flows_have_legal_path():
    for action_name in MAIN_ACTIONS:
        env = SiedlerScharfschuetzenEnv()
        env.reset()

        assert action_name in ACTION_FLOWS
        assert ACTION_FLOWS[action_name][0] == ActionPhase.MAIN

        _prepare_env_for_action(env, action_name)
        _run_complete_flow(env, action_name)


def test_observation_contains_pending_flow_context():
    env = SiedlerScharfschuetzenEnv(use_spatial_obs=False)
    obs, _ = env.reset()
    _grant_abundant_resources(env)

    base_dim = env.vector_obs_size - env.flow_context_dim - env.phase_dim
    flow_slice = slice(base_dim, base_dim + env.flow_context_dim)
    phase_slice = slice(env.vector_obs_size - env.phase_dim, env.vector_obs_size)

    assert obs.shape == env.observation_space.shape
    assert env.flow_context_dim > 0
    assert not np.any(obs[flow_slice])
    assert int(np.argmax(obs[phase_slice])) == env.phase_index[ActionPhase.MAIN]

    assign_idx = MAIN_ACTIONS.index("assign_serf")
    assert bool(env.action_masks()[assign_idx])
    obs_after_main, _, _, _, info = env.step(assign_idx)
    assert info.get("multi_step")
    assert env.current_phase == ActionPhase.SOURCE_CATEGORY

    flow_after_main = obs_after_main[flow_slice]
    main_offset = 2
    assert flow_after_main[0] == 1.0
    assert flow_after_main[main_offset + assign_idx] == 1.0
    assert int(np.argmax(obs_after_main[phase_slice])) == env.phase_index[ActionPhase.SOURCE_CATEGORY]

    source_mask = env.action_masks()
    source_choice = _first_valid(source_mask, env.action_spaces[env.current_phase].n)
    obs_after_source, _, _, _, info = env.step(source_choice)
    assert info.get("multi_step")
    assert env.current_phase == ActionPhase.QUANTITY

    flow_after_source = obs_after_source[flow_slice]
    source_offset = main_offset + len(MAIN_ACTIONS) + len(BUILD_CATEGORIES)
    assert not np.array_equal(flow_after_main, flow_after_source)
    assert flow_after_source[source_offset + source_choice] == 1.0
    assert int(np.argmax(obs_after_source[phase_slice])) == env.phase_index[ActionPhase.QUANTITY]


def test_build_main_action_replaces_assign_serf_neubau_path():
    env = SiedlerScharfschuetzenEnv()
    env.reset()
    _grant_abundant_resources(env)

    mask = env._mask_main_actions()
    build_idx = MAIN_ACTIONS.index("build")
    assign_idx = MAIN_ACTIONS.index("assign_serf")
    assert bool(mask[build_idx]), "build muss fuer Neubau moeglich sein"
    assert bool(mask[assign_idx]), "assign_serf bleibt fuer Ressourcen/Baustellen moeglich"

    env.total_leibeigene = 0
    env.free_leibeigene = 0
    for area in list(env.serf_areas.keys()):
        env.serf_areas[area]["count"] = 0
    env._can_cache = {}

    assert any(env._can_build(building) for building in env.buildable_buildings)
    mask = env._mask_main_actions()
    assert not bool(mask[build_idx]), "build braucht freie Leibeigene fuer Builder-Zuweisung"


def test_construction_assignment_uses_nearest_idle_serfs():
    env = SiedlerScharfschuetzenEnv()
    env.reset()
    _grant_free_serfs(env, 2)
    assert len(env.production_system.serfs) >= 2

    site_id = 4242
    env.construction_sites.append(
        {
            "building": "Wohnhaus_1",
            "position": {"x": 1000, "y": 1000},
            "total_time": 40.0,
            "remaining_work": 40.0,
            "serfs_assigned": 0,
            "site_id": site_id,
        }
    )
    env.production_system.serfs[0].position = Position(5000, 5000)
    env.production_system.serfs[1].position = Position(1010, 1010)

    assigned = env._assign_serf_to_construction_site(SerfArea.FREE, 1, len(env.construction_sites) - 1)

    assert assigned == 1
    assert env.production_system.serfs[1].build_site_id == site_id
    assert env.production_system.serfs[0].build_site_id is None


def test_build_uses_selected_source_serfs_not_nearest_free_serfs():
    env = SiedlerScharfschuetzenEnv()
    env.reset()
    _grant_abundant_resources(env)
    assert len(env.production_system.serfs) >= 2

    old_site_id = 31337
    env.construction_sites.append(
        {
            "building": "Wohnhaus_1",
            "position": {"x": 5000, "y": 5000},
            "total_time": 40.0,
            "remaining_work": 40.0,
            "serfs_assigned": 1,
            "site_id": old_site_id,
        }
    )
    selected_from_old_site = env.production_system.serfs[0]
    nearer_free_serf = env.production_system.serfs[1]
    selected_from_old_site.build_site_id = old_site_id
    selected_from_old_site.position = Position(5000, 5000)
    nearer_free_serf.position = Position(1000, 1000)
    env.free_leibeigene = max(0, env.free_leibeigene - 1)
    env.serf_areas[SerfArea.FREE]["count"] = env.free_leibeigene

    building = "Wohnhaus_1"
    category_idx = env._get_build_category_index(building)
    building_idx = env._get_buildings_for_build_category(category_idx).index(building)
    selections = _first_valid_build_position_selection(
        env,
        building,
        {
            ActionPhase.SOURCE_CATEGORY: 6,
            ActionPhase.SOURCE_SPECIFIC: 0,
            ActionPhase.QUANTITY: 0,
            ActionPhase.BUILD_CATEGORY: category_idx,
            ActionPhase.BUILDING: building_idx,
            ActionPhase.POSITION_MODE: 0,
        },
    )

    reward = env._execute_action(
        "build",
        selections,
    )

    assert reward == 0.0
    new_site = env.construction_sites[-1]
    assert new_site["site_id"] != old_site_id
    assert selected_from_old_site.build_site_id == new_site["site_id"]
    assert nearer_free_serf.build_site_id is None
    assert env.construction_sites[0]["serfs_assigned"] == 0


def test_build_category_mask_allows_selected_nonfree_source():
    env = SiedlerScharfschuetzenEnv()
    env.reset()
    _grant_abundant_resources(env)
    assert len(env.production_system.serfs) >= 1

    old_site_id = 42424
    env.construction_sites.append(
        {
            "building": "Wohnhaus_1",
            "position": {"x": 5000, "y": 5000},
            "total_time": 40.0,
            "remaining_work": 40.0,
            "serfs_assigned": 1,
            "site_id": old_site_id,
        }
    )
    env.production_system.serfs[0].build_site_id = old_site_id
    env.free_leibeigene = 0
    env.serf_areas[SerfArea.FREE]["count"] = 0

    building = "Wohnhaus_1"
    category_idx = env._get_build_category_index(building)
    env.current_flow = "build"
    env.current_phase = ActionPhase.BUILD_CATEGORY
    env.pending_selections = {
        ActionPhase.SOURCE_CATEGORY: 6,
        ActionPhase.SOURCE_SPECIFIC: 0,
        ActionPhase.QUANTITY: 0,
    }
    env._can_cache = {}

    category_mask = env.action_masks()[: env.action_spaces[ActionPhase.BUILD_CATEGORY].n]

    assert bool(category_mask[category_idx])


def test_multistep_cancel_slot_resets_without_tick():
    env = SiedlerScharfschuetzenEnv()
    env.reset()
    _grant_abundant_resources(env)

    env.step(MAIN_ACTIONS.index("build"))
    assert env.current_phase == ActionPhase.SOURCE_CATEGORY
    current_time = env.current_time
    mask = env.action_masks()
    assert bool(mask[env.cancel_action_index])

    _obs, reward, terminated, truncated, info = env.step(env.cancel_action_index)

    assert reward == 0.0
    assert not terminated
    assert not truncated
    assert info["multi_step_cancelled"]
    assert env.current_phase == ActionPhase.MAIN
    assert env.current_flow is None
    assert env.current_time == current_time


def test_multihead_policy_can_sample_cancel_slot_in_subflows():
    from sb3_contrib import MaskablePPO

    from multihead_policy import MultiHeadMaskablePolicy

    env = SiedlerScharfschuetzenEnv(use_spatial_obs=False)
    env.reset()
    _grant_abundant_resources(env)
    model = MaskablePPO(
        MultiHeadMaskablePolicy,
        env,
        n_steps=8,
        batch_size=4,
        policy_kwargs={
            "net_arch": [64, 64],
            "action_head_sizes": env.get_action_head_sizes(),
            "phase_dim": env.phase_dim,
        },
        verbose=0,
    )

    obs, _reward, _terminated, _truncated, _info = env.step(MAIN_ACTIONS.index("build"))
    mask = env.action_masks()

    assert env.current_phase != ActionPhase.MAIN
    assert bool(mask[env.cancel_action_index])

    obs_tensor, _ = model.policy.obs_to_tensor(obs)
    dist = model.policy.get_distribution(obs_tensor, action_masks=mask.reshape(1, -1))
    cancel_prob = float(dist.distribution.probs[0, env.cancel_action_index].detach().cpu().item())

    assert cancel_prob > 0.0


def test_wood_specific_uses_stable_flat_tree_ids():
    env = SiedlerScharfschuetzenEnv()
    env.reset()
    _grant_abundant_resources(env)

    assert env.action_spaces[ActionPhase.TARGET_SPECIFIC].n >= PLAYER_1_TREES_SUMMARY["total_trees"]
    env.current_flow = "assign_serf"
    env.current_phase = ActionPhase.TARGET_SPECIFIC
    env.pending_selections = {
        ActionPhase.SOURCE_CATEGORY: 0,
        ActionPhase.SOURCE_SPECIFIC: 0,
        ActionPhase.QUANTITY: 0,
        ActionPhase.TARGET_CATEGORY: 1,
    }
    env._can_cache = {}

    mask = env.action_masks()[: env.action_spaces[ActionPhase.TARGET_SPECIFIC].n]
    valid = np.flatnonzero(mask)
    assert len(valid) > 0
    assert int(valid.max()) < PLAYER_1_TREES_SUMMARY["total_trees"]
    assert env._wood_specific_encoded_limit() == PLAYER_1_TREES_SUMMARY["total_trees"]

    first_specific = int(valid[0])
    tree_idx = env._get_wood_zone_rank_tree_index(
        first_specific,
        1,
        mode="assign",
        available_free_override=env.free_leibeigene,
    )
    assert tree_idx == first_specific
    expected_tree = env.tree_list_internal[first_specific]

    env._assign_serfs_to_selection(1, first_specific, 1, env.pending_selections)

    assert expected_tree["serfs_assigned"] == 1


def test_position_mode_changes_candidate_order_without_changing_validity():
    env = SiedlerScharfschuetzenEnv()
    env.reset()
    _grant_abundant_resources(env)
    hq_x, hq_y = env.hq_position
    worker_cluster = {"x": hq_x + 12000, "y": hq_y + 3000}
    env.building_position_map["Schmiede_1_mode"] = worker_cluster
    env._placement_cache = {}

    building = "Wohnhaus_1"
    auto = env._get_build_position_candidates_for_selections(
        building,
        {ActionPhase.POSITION_MODE: 0},
    )
    worker = env._get_build_position_candidates_for_selections(
        building,
        {ActionPhase.POSITION_MODE: 3},
    )

    assert auto
    assert worker
    assert len(auto) == len(worker)
    assert _xy(auto[0]) != _xy(worker[0])


def test_build_position_indices_stay_stable_when_position_becomes_blocked():
    env = SiedlerScharfschuetzenEnv()
    env.reset()
    _grant_abundant_resources(env)

    building = "Wohnhaus_1"
    selections = {ActionPhase.POSITION_MODE: 1}
    candidates_before = env._get_build_position_candidates_for_selections(building, selections)
    valid_before = env._get_build_position_valid_mask_for_selections(building, selections)
    valid_indices = np.flatnonzero(valid_before)

    assert len(candidates_before) > 0
    assert len(valid_indices) > 0

    selected_idx = int(valid_indices[0])
    selected = dict(candidates_before[selected_idx])
    env._build_building(building, position=selected)

    candidates_after = env._get_build_position_candidates_for_selections(building, selections)
    valid_after = env._get_build_position_valid_mask_for_selections(building, selections)

    assert [_xy(pos) for pos in candidates_after[:200]] == [_xy(pos) for pos in candidates_before[:200]]
    assert _xy(candidates_after[selected_idx]) == _xy(selected)
    assert bool(valid_before[selected_idx])
    assert not bool(valid_after[selected_idx])


def test_queue_cancel_actions_remove_selected_items_and_refund():
    env = SiedlerScharfschuetzenEnv()
    env.reset()
    _grant_abundant_resources(env)

    site_cost = dict(buildings_db["Wohnhaus_1"]["cost"])
    before_resources = dict(env.resources)
    site = {
        "building": "Wohnhaus_1",
        "position": {"x": env.hq_position[0] + 1000, "y": env.hq_position[1]},
        "total_time": 80.0,
        "remaining_work": 80.0,
        "serfs_assigned": 0,
        "site_id": 111,
    }
    env.construction_sites.append(site)
    env._cancel_construction_site(0)
    assert not env.construction_sites
    for resource, amount in site_cost.items():
        assert env.resources[resource] == before_resources.get(resource, 0) + int(amount * 0.5)

    tech = next(t for t in env.tech_by_building["Hochschule"] if not technologies.get(t, {}).get("disabled"))
    env.current_researches = [(tech, 10.0)]
    env.researching_set.add(tech)
    env._cancel_research(tech)
    assert not env.current_researches
    assert tech not in env.researching_set

    soldier = env.soldier_types[0]
    env.recruit_queue = [(soldier, 10.0)]
    env._cancel_recruit(soldier)
    assert not env.recruit_queue


def test_wintersturm_weather_schedule_and_speed_factor():
    env = SiedlerScharfschuetzenEnv()
    env.reset()
    env._weather_schedule_enabled = True

    env.current_time = 0
    assert env._update_current_weather() == WEATHER_SUMMER
    assert env._get_weather_move_speed_multiplier() == 1.0

    env.current_time = 15 * 60
    assert env._update_current_weather() == WEATHER_RAIN
    assert env._get_weather_move_speed_multiplier() == 1.0

    env._set_weather(WEATHER_SNOW)
    assert env._get_weather_move_speed_multiplier() == SNOW_MOVE_SPEED_FACTOR


def test_refiner_cycle_time_uses_weather_speed_multiplier():
    refiner = Refiner(
        name="test_sawmill",
        position=Position(0, 0),
        supplier_position=Position(340, 0),
        resource_type=ResourceType.WOOD,
        input_resource=ResourceType.WOOD_RAW,
        worker_type="sawmill_worker",
        current_workers=1,
        work_wait_until=0.0,
    )

    normal = refiner.get_cycle_time(speed_multiplier=1.0)
    snowy = refiner.get_cycle_time(speed_multiplier=SNOW_MOVE_SPEED_FACTOR)
    assert snowy > normal
    assert abs(snowy - (normal / SNOW_MOVE_SPEED_FACTOR)) < 1e-9


def test_building_footprints_use_original_blocked_rectangles():
    expected = {
        "Bank": (900, 800),
        "Kloster": (1300, 1500),
        "Taverne": (900, 1200),
        "Turm": (200, 200),
        "Architektenstube": (900, 800),
        "Wetterkraftwerk": (500, 500),
        "Wetterturm": (400, 400),
        "PB_Beautification01": (100, 100),
        "PB_Beautification02": (300, 300),
    }

    for building, footprint in expected.items():
        assert pathfinding.get_building_footprint(building) == footprint


def test_research_xml_costs_and_times_are_overlaid_from_original():
    matched = 0
    for original_id, values in load_technology_xml_values().items():
        tech_name = next(
            (alias for alias in aliases_for_technology(original_id) if alias in technologies),
            None,
        )
        if not tech_name:
            continue
        matched += 1
        assert technologies[tech_name]["cost"] == values["cost"]
        if values["research_time"] > 0:
            assert technologies[tech_name]["research_time"] == values["research_time"]

    assert matched >= 60


def test_original_research_entity_condition_alternatives_are_used():
    env = SiedlerScharfschuetzenEnv()
    env.reset()
    _grant_abundant_resources(env)

    env.buildings["Hochschule_1"] = 1
    env.buildings["Hauptquartier_2"] = 0
    env.buildings["Hauptquartier_3"] = 1
    env.researched_techs.add("Mathematik")
    env.current_researches = []

    assert env._can_research("Fernglas")


def test_faith_caps_at_original_maximum():
    env = SiedlerScharfschuetzenEnv()
    env.reset()
    env.faith = MAXIMUM_FAITH - 0.1
    priest = Worker(
        worker_type="priest",
        position=Position(0, 0),
        workplace_position=Position(0, 0),
        work_time=WORKTIME_BASE,
    )
    priest.state = WorkerState.WORKING
    env.workforce_manager.workers.append(priest)

    env._tick_time()
    assert env.faith == MAXIMUM_FAITH


def test_worker_prefers_shorter_path_targets():
    worker = Worker(
        worker_type="farmer",
        position=Position(0, 0),
        workplace_position=Position(0, 0),
    )
    worker._path_revision = 1
    worker._last_camps = []

    farm_a = Farm(position=Position(100, 0))
    farm_b = Farm(position=Position(200, 0))

    residence_a = Residence(position=Position(120, 0))
    residence_b = Residence(position=Position(240, 0))

    def fake_pathfinder(start, target):
        if int(target.x) == 100:
            return [Position(0, 0), Position(1000, 0), Position(100, 0)]
        if int(target.x) == 200:
            return [Position(0, 0), Position(200, 0)]
        if int(target.x) == 120:
            return [Position(0, 0), Position(900, 0), Position(120, 0)]
        if int(target.x) == 240:
            return [Position(0, 0), Position(240, 0)]
        return []

    worker._pathfinder = fake_pathfinder
    worker._find_farm([farm_a, farm_b])
    assert worker.assigned_farm is farm_b
    assert worker.state == WorkerState.WALKING_TO_FARM

    worker.state = WorkerState.EATING
    worker.position = Position(0, 0)
    worker._find_residence([residence_a, residence_b])
    assert worker.assigned_residence is residence_b
    assert worker.state == WorkerState.WALKING_TO_RESIDENCE


def test_original_building_geometry_drives_grid_blocking():
    geometry = load_building_geometry()

    assert geometry["Bauernhof_1"]["approach_pos"] == (-400, 300)
    assert geometry["Wohnhaus_1"]["approach_pos"] == (-100, -400)
    assert pathfinding.get_building_block_offsets("Bauernhof_1") == (-300, -400, 300, 600)

    grid = pathfinding.WalkableGrid(120, 120)
    building_id = grid.add_building(2000, 2000, "Bauernhof_1")

    inside_offset = pathfinding.GridPosition.from_world(2000, 2000 + 550)
    outside_offset = pathfinding.GridPosition.from_world(2000, 2000 - 450)
    assert grid.buildings[inside_offset.y, inside_offset.x] == 1
    assert grid.buildings[outside_offset.y, outside_offset.x] == 0

    grid.remove_building(building_id)
    assert grid.buildings[inside_offset.y, inside_offset.x] == 0


def test_worker_pause_paths_use_original_approach_offsets():
    geometry = load_building_geometry()
    farm_offset = geometry["Bauernhof_1"]["approach_pos"]
    residence_offset = geometry["Wohnhaus_1"]["approach_pos"]

    worker = Worker(
        worker_type="farmer",
        position=Position(0, 0),
        workplace_position=Position(0, 0),
    )
    worker._last_camps = []

    farm = Farm(
        position=Position(1000, 1000),
        approach_offset=Position(farm_offset[0], farm_offset[1]),
    )
    residence = Residence(
        position=Position(2000, 2000),
        approach_offset=Position(residence_offset[0], residence_offset[1]),
    )
    seen_targets = []

    def fake_pathfinder(start, target):
        seen_targets.append((int(target.x), int(target.y)))
        return [Position(start.x, start.y), Position(target.x, target.y)]

    worker._pathfinder = fake_pathfinder
    worker._find_farm([farm])
    assert worker.assigned_farm is farm
    assert worker.final_destination == Position(600, 1300)
    assert seen_targets[-1] == (600, 1300)

    worker.position = Position(0, 0)
    worker._find_residence([residence])
    assert worker.assigned_residence is residence
    assert worker.final_destination == Position(1900, 1600)
    assert seen_targets[-1] == (1900, 1600)


def test_worker_runtime_callbacks_are_cleared_after_tick_for_subproc_pickle():
    import pickle

    worker = Worker(
        worker_type="farmer",
        position=Position(0, 0),
        workplace_position=Position(1000, 1000),
        work_time=1,
    )
    worker.state = WorkerState.WORKING

    def local_pathfinder(start, target):
        return [Position(start.x, start.y), Position(target.x, target.y)]

    def local_spawn_camp(position):
        return Camp(position=Position(position.x, position.y))

    worker.tick(
        1.0,
        farms=[],
        residences=[],
        camps=[],
        pathfinder=local_pathfinder,
        path_revision=1,
        spawn_camp_fn=local_spawn_camp,
    )

    assert getattr(worker, "_pathfinder", None) is None
    assert getattr(worker, "_path_revision", None) is None
    assert getattr(worker, "_spawn_camp_fn", None) is None
    pickle.dumps(worker)


def test_workforce_sync_applies_original_pause_building_offsets():
    env = SiedlerScharfschuetzenEnv()
    env.reset()
    env.building_position_map["Bauernhof_1_test"] = {"x": 1000, "y": 1000}
    env.building_position_map["Wohnhaus_1_test"] = {"x": 2000, "y": 2000}
    env._mark_infrastructure_dirty()

    env._sync_workforce_infrastructure()

    farm = next(f for f in env.workforce_manager.farms if int(f.position.x) == 1000)
    residence = next(r for r in env.workforce_manager.residences if int(r.position.x) == 2000)
    assert farm.approach_position() == Position(600, 1300)
    assert residence.approach_position() == Position(1900, 1600)


def test_pause_building_anchors_prioritize_worker_cluster():
    env = SiedlerScharfschuetzenEnv()
    env.reset()
    hq_x, hq_y = env.hq_position
    worker_cluster = {"x": hq_x + 12000, "y": hq_y + 3000}
    env.building_position_map["Schmiede_1_anchor"] = worker_cluster

    residence_anchor = env._get_build_anchor_positions("Wohnhaus_1")[0]
    farm_anchor = env._get_build_anchor_positions("Bauernhof_1")[0]

    def dist(anchor, pos):
        return ((anchor[0] - pos["x"]) ** 2 + (anchor[1] - pos["y"]) ** 2) ** 0.5

    assert dist(residence_anchor, worker_cluster) < dist((hq_x, hq_y), worker_cluster)
    assert dist(farm_anchor, worker_cluster) < dist((hq_x, hq_y), worker_cluster)


def test_oriented_original_offsets_are_rotated():
    env = SiedlerScharfschuetzenEnv()
    env.reset()

    target = env._building_attachment_position(
        "Bauernhof_1",
        {"x": 1000, "y": 1000, "orientation": 90},
        "approach_pos",
    )
    assert target == Position(700, 600)

    worker = Worker(
        worker_type="farmer",
        position=Position(0, 0),
        workplace_position=Position(1000, 1000),
    )
    worker.configure_original_work_cycle(
        {
            "requires_supplier": False,
            "work_start_offset": (100, 0),
            "work_route_offsets": [(0, 100)],
        },
        workplace_orientation=90,
    )
    worker._ensure_work_route_started()
    assert worker.position == Position(1000, 1100)
    assert worker.work_route == [Position(900, 1000)]


def test_noncombat_original_technology_coverage_is_closed():
    noncombat_ids = {
        "t_adjusttaxes",
        "t_blesssettlers1",
        "t_blesssettlers2",
        "t_blesssettlers3",
        "t_blesssettlers4",
        "t_blesssettlers5",
        "t_changeweather",
        "t_cityguard",
        "t_cropcycle",
        "t_makerain",
        "t_makesnow",
        "t_makesummer",
        "t_marketclay",
        "t_marketgold",
        "t_marketiron",
        "t_marketstone",
        "t_marketsulfur",
        "t_marketwood",
        "t_minimapnormalview",
        "t_minimapresouceview",
        "t_minimaptacticview",
        "t_onlinehelp",
        "t_pickaxe",
        "t_scoutfindresources",
        "t_scouttorches",
        "t_spinningwheel",
        "t_supertechnology",
        "t_thiefsabotage",
        "t_tracking",
        "t_weatherforecast",
    }
    absent_test_ids = {"t_test", "t_test2"}

    xml_values = load_technology_xml_values()
    assert not (absent_test_ids & set(xml_values))
    for original_id in noncombat_ids:
        assert original_id in xml_values
        aliases = list(aliases_for_technology(original_id))
        assert any(alias in technologies for alias in aliases), original_id
        assert any(
            alias in TECHNOLOGY_EFFECTS or technologies.get(alias, {}).get("effects")
            for alias in aliases
        ), original_id

    assert xml_values["t_tracking"]["effects"]["exploration_modifier"] == 10.0
    assert xml_values["t_cityguard"]["effects"]["exploration_modifier"] == 5.0


def test_weather_technology_completion_sets_weather():
    env = SiedlerScharfschuetzenEnv()
    env.reset()

    env._on_technology_completed("T_MakeSnow")
    assert env.current_weather == WEATHER_SNOW
    assert env._weather_schedule_enabled is False

    env._on_technology_completed("T_MakeRain")
    assert env.current_weather == WEATHER_RAIN

    env._on_technology_completed("T_MakeSummer")
    assert env.current_weather == WEATHER_SUMMER


def test_wintersturm_player1_map_data_matches_extract():
    env = SiedlerScharfschuetzenEnv(player_id=1)
    env.reset()

    hq = PLAYER_HQ_POSITIONS[1]
    assert env.hq_position == (hq["x"], hq["y"])
    assert env.resources == START_RESOURCES

    start_buildings = {
        item["type"]: item["position"]
        for item in PLAYER_START_BUILDINGS[1]
    }
    assert env.buildings["Hauptquartier_1"] == 1
    assert env.buildings["Dorfzentrum_1"] == 1
    assert _xy(env.building_position_map["Hauptquartier_1_0"]) == _xy(start_buildings["Hauptquartier_1"])
    assert _xy(env.building_position_map["Dorfzentrum_1_0"]) == _xy(start_buildings["Dorfzentrum_1"])

    assert len(env.tree_list_internal) == PLAYER_1_TREES_SUMMARY["total_trees"] == 202
    assert len(env.map_manager.tree_world_positions) == 202
    assert len(env.map_manager.grid.tree_positions) == 202

    walkable_path = PROJECT_ROOT / "map_extract" / "wintersturm_extracted" / "player1_walkable_515.npy"
    assert Path(env._cached_walkable_file).resolve() == walkable_path.resolve()
    walkable = np.load(walkable_path)
    assert env.map_manager.grid.terrain_base.shape == walkable.shape == (257, 258)
    assert np.array_equal(env.map_manager.grid.terrain_base, walkable.astype(np.uint8))
    assert env.map_manager.offset_x == 25240.0
    assert env.map_manager.offset_y == 0.0

    village_centers = [
        (int(slot["x"]), int(slot["y"]))
        for slot in PLAYER_1_VILLAGE_CENTER_SLOTS
    ]
    assert [
        _xy(pos)
        for pos in env._get_build_position_candidates("Dorfzentrum_1")
    ] == village_centers

    mine_buildings = {
        "Eisenmine_1": "Eisen",
        "Steinmine_1": "Stein",
        "Lehmmine_1": "Lehm",
        "Schwefelmine_1": "Schwefel",
    }
    for building, category in mine_buildings.items():
        expected = [
            (int(dep["x"]), int(dep["y"]))
            for dep in PLAYER_1_SMALL_DEPOSITS[category]
        ]
        assert [_xy(pos) for pos in env._get_build_position_candidates(building)] == expected
        deposits = env.deposit_categories[category]["deposits"]
        assert len(deposits) == len(expected)
        assert sum(int(dep["remaining"]) for dep in deposits) == 4000 * len(expected)


def _xy(position):
    if isinstance(position, dict):
        return int(round(position.get("x", 0))), int(round(position.get("y", 0)))
    return int(round(position[0])), int(round(position[1]))



def test_build_placement_determinism_and_special_cases():
    env = SiedlerScharfschuetzenEnv()
    env.reset()
    _grant_abundant_resources(env)

    # 1) Normale Gebaeude-Kandidaten sind deterministisch innerhalb eines Zustands.
    normal_building = "Wohnhaus_1"
    if normal_building in env.buildable_buildings and env._can_build(normal_building):
        c1 = env._find_candidate_build_positions(normal_building, limit=6)
        c2 = env._find_candidate_build_positions(normal_building, limit=6)
        assert c1 == c2, "Kandidatenreihenfolge ist nicht deterministisch"

    # 2) Minen folgen den festen Schacht-Slots in Reihenfolge.
    mine_building = next(
        (
            b
            for b in env.buildable_buildings
            if buildings_db.get(b, {}).get("mine_type") and env._can_build(b)
        ),
        None,
    )
    if mine_building is not None:
        mine_type = buildings_db[mine_building]["mine_type"]
        before_count = len(env.built_mines.get(mine_type, []))
        expected_slot = env.mine_positions[mine_type][before_count]

        env._build_building(mine_building)

        assert len(env.built_mines[mine_type]) == before_count + 1
        assert _xy(env.built_mines[mine_type][-1]) == _xy(expected_slot)

    # 3) Dorfzentrum nutzt freie DZ-Slots.
    if "Dorfzentrum_1" in env.buildable_buildings and env._can_build("Dorfzentrum_1"):
        free_before = sum(1 for s in env.dz_slots if s.get("status") == "free")
        env._build_building("Dorfzentrum_1")
        free_after = sum(1 for s in env.dz_slots if s.get("status") == "free")
        assert free_after == max(0, free_before - 1)


if __name__ == "__main__":
    print("=" * 60)
    print("ENGINE CONFORMANCE TESTS")
    print("=" * 60)

    try:
        test_worker_truth_alignment()
        print("[OK] Worker truth alignment")

        test_main_action_flows_have_legal_path()
        print("[OK] Main action flows")

        test_assign_serf_main_action_allows_build_without_free_serfs()
        print("[OK] assign_serf build fallback")

        test_worker_prefers_shorter_path_targets()
        print("[OK] worker path target preference")

        test_build_placement_determinism_and_special_cases()
        print("[OK] Build placement")

        print("=" * 60)
        print("ALLE CONFORMANCE-TESTS BESTANDEN")
        print("=" * 60)
    except AssertionError as exc:
        print(f"[FEHLER] {exc}")
        raise
