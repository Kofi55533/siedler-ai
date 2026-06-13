# -*- coding: utf-8 -*-
"""Tests for the human opening expert used by behavior cloning."""

from environment import MAIN_ACTIONS, QUANTITY_VALUES, ActionPhase, SiedlerScharfschuetzenEnv
from expert_opening import ExpertOpeningController, collect_expert_opening_demonstrations
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
        max_micro_steps=220,
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
