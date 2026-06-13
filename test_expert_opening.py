# -*- coding: utf-8 -*-
"""Tests for the human opening expert used by behavior cloning."""

from environment import INCOME_CYCLE, MAIN_ACTIONS, QUANTITY_VALUES, ActionPhase, SiedlerScharfschuetzenEnv
from expert_opening import (
    FULL_SIM_FIRST_UNIVERSITY_START_TIME,
    ExpertOpeningController,
    collect_expert_opening_demonstrations,
)
from production_system import Serf, SerfState
from worker_simulation import Position


def test_expert_opening_starts_with_nine_serfs():
    env = SiedlerScharfschuetzenEnv(use_spatial_obs=False)
    obs, _info = env.reset(seed=7)
    controller = ExpertOpeningController()

    main_action = controller.act(env)
    assert MAIN_ACTIONS[main_action] == "buy_serf"

    obs, _reward, _terminated, _truncated, info = env.step(main_action)
    assert info.get("multi_step")
    assert env.current_phase == ActionPhase.QUANTITY

    quantity_action = controller.act(env)
    assert QUANTITY_VALUES[quantity_action] == 9

    obs, _reward, _terminated, _truncated, info = env.step(quantity_action)
    controller.observe_step(info)

    assert env.total_leibeigene == 9
    assert env.free_leibeigene == 9
    assert len(env.free_serf_cohorts) == 1
    assert env.free_serf_cohorts[0]["base"] == "Rekrutiert"
    assert env.free_serf_cohorts[0]["count"] == 9


def test_expert_opening_demo_collection_has_no_invalid_fallbacks():
    env = SiedlerScharfschuetzenEnv(use_spatial_obs=False)
    demos = collect_expert_opening_demonstrations(
        env,
        episodes=1,
        max_micro_steps=700,
        max_completed_actions=45,
        seed=8,
    )

    assert len(demos["actions"]) > 0
    assert demos["masks"].shape[0] == len(demos["actions"])
    assert int(demos["fallback_actions"]) == 0
    assert demos["episode_completed_actions"][0] == 45


def test_build_assignment_falls_back_when_astar_cannot_reach_exact_cell():
    env = SiedlerScharfschuetzenEnv(use_spatial_obs=False)
    env.reset(seed=9)
    env._find_path_world = lambda _start, _target: []

    start = Position(x=env.hq_position[0], y=env.hq_position[1])
    target = Position(x=env.hq_position[0] - 1200, y=env.hq_position[1] + 600)
    serf = Serf(position=Position(x=start.x, y=start.y))

    env._assign_serf_to_build(serf, "Hochschule_1", target, start, site_id=123)

    assert serf.state == SerfState.WALKING_TO_BUILD
    assert not serf.path_blocked
    assert serf.waypoint is not None
    before_x = serf.position.x
    serf.tick(1.0)
    assert serf.position.x != before_x


def test_full_sim_expert_opening_completes_mines_and_universities_before_first_payday(monkeypatch):
    monkeypatch.setenv("SIEDLER_SIM_MODE", "full_sim")
    monkeypatch.delenv("SIEDLER_DISABLE_RUNTIME_PATHING", raising=False)
    env = SiedlerScharfschuetzenEnv(use_spatial_obs=False)
    env.reset(seed=11)
    controller = ExpertOpeningController()

    first_payday = None
    first_university_start = None
    completion_times = {}
    required = {
        "Hochschule": 2,
        "Eisenmine": 2,
        "Schwefelmine": 2,
        "Steinmine": 1,
        "Lehmmine": 1,
    }
    for _micro_step in range(5000):
        if env.current_phase == ActionPhase.MAIN:
            plan = controller._make_next_plan(env)
            if (
                plan is not None
                and plan.reason.startswith("opening: start Hochschule")
                and first_university_start is None
            ):
                first_university_start = int(env.current_time)

        obs, _reward, terminated, truncated, info = env.step(controller.act(env))
        controller.observe_step(info)
        for base, count in required.items():
            if base not in completion_times and env._get_completed_base_delta(base) >= count:
                completion_times[base] = int(env.current_time)
        if env._first_worker_building_time is not None and first_payday is None:
            first_payday = env._first_worker_building_time + INCOME_CYCLE
        if first_payday is not None and env.current_time >= first_payday:
            break
        assert not terminated
        assert not truncated

    assert first_payday is not None
    assert first_university_start == FULL_SIM_FIRST_UNIVERSITY_START_TIME
    assert int(env._first_worker_building_time) == 76
    assert int(first_payday) == 196
    assert env.current_time >= first_payday
    for base, count in required.items():
        assert env._get_completed_base_delta(base) >= count
        assert completion_times[base] < first_payday
