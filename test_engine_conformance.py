# -*- coding: utf-8 -*-
"""Konformitaetstests fuer Action-Flow, Placement und Worker-Truth."""

import json
from pathlib import Path

import numpy as np

from environment import (
    ACTION_FLOWS,
    MAIN_ACTIONS,
    ActionPhase,
    SerfArea,
    SiedlerScharfschuetzenEnv,
    buildings_db,
)
from worker_simulation import (
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


def _grant_abundant_resources(env):
    for key in list(env.resources.keys()):
        env.resources[key] = 1_000_000


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


def test_worker_truth_alignment():
    assert WORKER_TRUTH_PATH.exists(), f"Fehlt: {WORKER_TRUTH_PATH}"

    with open(WORKER_TRUTH_PATH, "r", encoding="utf-8") as f:
        truth = json.load(f)

    logic = (truth.get("global_truth") or {}).get("logic_worktime") or {}

    assert WORKER_CONFIG_SOURCE in {"worker_truth_model", "defaults"}
    assert WORKTIME_BASE == _safe_int(logic.get("base"), WORKTIME_BASE)
    assert WORKTIME_THRESHOLD_WORK == _safe_int(
        logic.get("threshold_work"), WORKTIME_THRESHOLD_WORK
    )
    assert abs(
        FORCE_TO_WORK_PENALTY
        - _safe_float(logic.get("force_to_work_penalty"), FORCE_TO_WORK_PENALTY)
    ) < 1e-9

    workers = truth.get("workers") or {}
    for raw_name, data in workers.items():
        if not isinstance(data, dict):
            continue

        env_name = data.get("env_name") or raw_name
        worker_name = normalize_worker_type(str(env_name))
        movement = data.get("movement") or {}

        speed_truth = _safe_int(movement.get("speed"), 320)
        assert WORKER_SPEEDS.get(worker_name) == speed_truth, (
            f"Speed-Mismatch {worker_name}: sim={WORKER_SPEEDS.get(worker_name)} truth={speed_truth}"
        )

        camper_truth = _safe_int(movement.get("camper_range"), 5000)
        sim_camper = WORKER_CAMPER_RANGE.get(worker_name, 5000)
        assert sim_camper == camper_truth, (
            f"CamperRange-Mismatch {worker_name}: sim={sim_camper} truth={camper_truth}"
        )

        if not data.get("has_worktime", False):
            continue

        assert worker_name in WORKER_PARAMS, f"Worker-Params fehlen fuer {worker_name}"
        params = WORKER_PARAMS[worker_name]
        wt = data.get("worktime_truth") or {}

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

        expected_changes = _extract_truth_changes_per_cycle(data)
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


def test_assign_serf_main_action_allows_build_without_free_serfs():
    env = SiedlerScharfschuetzenEnv()
    env.reset()
    _grant_abundant_resources(env)

    env.total_leibeigene = 0
    env.free_leibeigene = 0
    for area in list(env.serf_areas.keys()):
        env.serf_areas[area]["count"] = 0

    assert any(env._can_build(building) for building in env.buildable_buildings)
    mask = env._mask_main_actions()
    assign_idx = MAIN_ACTIONS.index("assign_serf")
    assert bool(mask[assign_idx]), "assign_serf muss fuer Neubau moeglich bleiben"


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
