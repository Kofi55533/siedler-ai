import pytest
import numpy as np

from environment import (
    ActionPhase,
    BUILD_CATEGORIES,
    MAIN_ACTIONS,
    RESOURCE_SCHWEFEL,
    RESOURCE_TALER,
    SiedlerScharfschuetzenEnv,
)
from training_profiles import get_train_profile


WAIT_ACTION = MAIN_ACTIONS.index("wait")
TEST_REWARD_PROFILE = {
    "terminal_dependency_bonus": 0.0,
    "terminal_recruitable_bonus": 0.0,
    "terminal_potential_bonus_per_unit": 5.0,
    "terminal_potential_use_cumulative_earnings": 0.0,
    "terminal_potential_include_start_resources": 0.0,
    "terminal_potential_scharf_tier": 1.0,
    "terminal_potential_require_path_ready": 1.0,
}


def _make_env() -> SiedlerScharfschuetzenEnv:
    env = SiedlerScharfschuetzenEnv(
        use_spatial_obs=False,
        reward_profile=TEST_REWARD_PROFILE,
    )
    env.reset(seed=0)
    return env


def _finish_episode(env: SiedlerScharfschuetzenEnv):
    env.current_time = env.max_time - 1
    _, reward, terminated, truncated, info = env.step(WAIT_ACTION)
    assert terminated is True
    assert truncated is False
    return reward, info


def _find_gunsmith_key(env: SiedlerScharfschuetzenEnv) -> str:
    for key in env.buildings.keys():
        if "chsenmacherei_1" in key:
            return key
    raise AssertionError("Buechsenmacherei_1 key not found in environment")


def _find_required_tech(env: SiedlerScharfschuetzenEnv) -> str:
    _, required_techs = env._get_scharf_requirements_for_tier(1)
    required = sorted(str(item) for item in required_techs)
    if not required:
        raise AssertionError("No required Scharfschuetzen tech found in environment")
    return required[0]


def test_terminal_potential_requires_unlocked_path():
    env = _make_env()
    env.resources[RESOURCE_TALER] = 1000
    env.resources[RESOURCE_SCHWEFEL] = 280

    reward, info = _finish_episode(env)

    assert info["terminal_path_ready"] is False
    assert info["terminal_potential_metric"] == pytest.approx(0.0)
    assert info["terminal_potential_reward"] == pytest.approx(0.0)
    assert reward == pytest.approx(0.0)


def test_terminal_potential_counts_current_stock_once_path_is_ready():
    env = _make_env()
    env.buildings[_find_gunsmith_key(env)] = 1
    env.resources[RESOURCE_TALER] = 1000
    env.resources[RESOURCE_SCHWEFEL] = 280

    reward, info = _finish_episode(env)
    taler_cost, sulfur_cost = env._get_scharf_costs(target_tier=1)
    expected_units = min(
        env._get_total_resource(RESOURCE_TALER) / taler_cost,
        env._get_total_resource(RESOURCE_SCHWEFEL) / sulfur_cost,
    )

    assert info["terminal_path_ready"] is True
    assert info["terminal_potential_source"] == "current_stock"
    assert info["terminal_potential_metric"] == pytest.approx(expected_units)
    assert info["terminal_potential_reward"] == pytest.approx(expected_units * 5.0)
    assert reward == pytest.approx(expected_units * 5.0)


def test_sparse_profile_is_no_longer_zero_reward():
    profile = get_train_profile("sparse")

    assert profile["reward_profile"]["terminal_potential_bonus_per_unit"] > 0.0
    assert profile["reward_profile"]["terminal_potential_use_cumulative_earnings"] == pytest.approx(0.0)


def test_step_requirement_and_path_bonuses_fire_once():
    env = SiedlerScharfschuetzenEnv(
        use_spatial_obs=False,
        reward_profile={
            "step_path_ready_bonus": 11.0,
            "step_required_building_complete_bonus": 7.0,
            "step_delta_positive_only": 1.0,
        },
    )
    env.reset(seed=0)
    env.buildings[_find_gunsmith_key(env)] = 1

    _, reward, terminated, truncated, info = env.step(WAIT_ACTION)

    assert terminated is False
    assert truncated is False
    assert info["step_path_ready"] is True
    assert info["step_new_required_buildings"] == 1
    assert reward == pytest.approx(18.0)


def test_step_required_tech_bonus_tracks_new_completion():
    env = SiedlerScharfschuetzenEnv(
        use_spatial_obs=False,
        reward_profile={
            "step_required_tech_complete_bonus": 9.0,
            "step_delta_positive_only": 1.0,
        },
    )
    env.reset(seed=0)
    env.researched_techs.add(_find_required_tech(env))

    _, reward, terminated, truncated, info = env.step(WAIT_ACTION)

    assert terminated is False
    assert truncated is False
    assert info["step_new_required_techs"] == 1
    assert reward == pytest.approx(9.0)


def test_terminal_path_ready_bonus_applies_without_resource_potential():
    env = SiedlerScharfschuetzenEnv(
        use_spatial_obs=False,
        reward_profile={
            "terminal_path_ready_bonus": 3.5,
            "terminal_potential_bonus_per_unit": 0.0,
            "terminal_dependency_bonus": 0.0,
            "terminal_recruitable_bonus": 0.0,
        },
    )
    env.reset(seed=0)
    env.buildings[_find_gunsmith_key(env)] = 1
    env.current_time = env.max_time - 1

    _, reward, terminated, truncated, info = env.step(WAIT_ACTION)

    assert terminated is True
    assert truncated is False
    assert info["terminal_path_ready"] is True
    assert info["terminal_potential_reward"] == pytest.approx(3.5)
    assert reward == pytest.approx(3.5)


def test_guided_profile_prunes_noisy_actions_and_decorations():
    profile = get_train_profile("guided_v1")
    env = SiedlerScharfschuetzenEnv(
        use_spatial_obs=False,
        reward_profile=profile["reward_profile"],
    )
    env.reset(seed=0)

    main_mask = env.action_masks()[: env.action_spaces[ActionPhase.MAIN].n]
    valid_main = {MAIN_ACTIONS[i] for i, flag in enumerate(main_mask) if flag}
    assert valid_main == {"wait", "build", "upgrade", "buy_serf", "assign_serf"}

    env.step(MAIN_ACTIONS.index("build"))
    env.step(0)  # source free, source-specific is skipped
    quantity_mask = env.action_masks()[: env.action_spaces[env.current_phase].n]
    env.step(int(np.flatnonzero(quantity_mask)[0]))
    category_mask = env.action_masks()[: env.action_spaces[env.current_phase].n]
    assert not bool(category_mask[5])  # beautification category

    valid_buildings = []
    for category_idx in np.flatnonzero(category_mask):
        env.current_phase = ActionPhase.BUILDING
        env.pending_selections[ActionPhase.BUILD_CATEGORY] = int(category_idx)
        env._can_cache = {}
        building_mask = env.action_masks()[: env.action_spaces[env.current_phase].n]
        category_buildings = env._get_buildings_for_build_category(int(category_idx))
        valid_buildings.extend(
            category_buildings[i]
            for i in np.flatnonzero(building_mask)
            if i < len(category_buildings)
        )
    assert valid_buildings
    assert all(not building.startswith("PB_Beautification") for building in valid_buildings)


def test_guided_tier_one_keeps_complete_transitive_goal_path():
    profile = get_train_profile("guided_v1")
    env = SiedlerScharfschuetzenEnv(
        use_spatial_obs=False,
        reward_profile=profile["reward_profile"],
    )
    env.reset(seed=0)

    required_buildings, required_techs = env._get_scharf_requirements_for_tier(1)

    assert any("chsenmacherei_1" in building for building in required_buildings)
    assert "Hauptquartier_1" in required_buildings
    assert "Hauptquartier_2" in required_buildings
    assert "Hauptquartier_3" not in required_buildings
    assert "Hochschule_1" in required_buildings
    assert {"Mathematik", "Fernglas", "Luntenschloss"}.issubset(required_techs)
    assert "Gezogener Lauf" not in required_techs
    assert env._is_goal_relevant_upgrade("Hauptquartier_1")


def test_guided_build_mask_can_reach_gunsmith_after_required_techs():
    profile = get_train_profile("guided_v1")
    env = SiedlerScharfschuetzenEnv(
        use_spatial_obs=False,
        reward_profile=profile["reward_profile"],
    )
    env.reset(seed=0)
    env.researched_techs.update({"Mathematik", "Fernglas", "Luntenschloss"})
    env.resources[RESOURCE_SCHWEFEL] = env.resources.get(RESOURCE_SCHWEFEL, 0) + 500.0
    env._can_cache = {}
    env._build_check_cache = {}
    env._build_batch_cache = {}
    env._build_check_cache_time = env.current_time

    military_category = next(
        idx for idx, name in BUILD_CATEGORIES.items() if name == "military"
    )
    env.current_flow = "build"
    env.current_phase = ActionPhase.BUILDING
    env.pending_selections[ActionPhase.BUILD_CATEGORY] = military_category
    building_mask = env.action_masks()[: env.action_spaces[env.current_phase].n]
    category_buildings = env._get_buildings_for_build_category(military_category)
    valid_buildings = [
        category_buildings[i]
        for i in np.flatnonzero(building_mask)
        if i < len(category_buildings)
    ]

    assert any("chsenmacherei_1" in building for building in valid_buildings)


def test_goal_resource_progress_reward_uses_reset_baseline():
    env = SiedlerScharfschuetzenEnv(
        use_spatial_obs=False,
        reward_profile={
            "step_goal_resource_progress_bonus": 10.0,
            "step_delta_positive_only": 1.0,
        },
    )
    env.reset(seed=0)

    _, reward, _, _, info = env.step(WAIT_ACTION)
    assert info["step_delta_goal_resource_progress"] == pytest.approx(0.0)
    assert reward == pytest.approx(0.0)

    env.resources[RESOURCE_SCHWEFEL] = env.resources.get(RESOURCE_SCHWEFEL, 0) + 100.0
    _, reward, _, _, info = env.step(WAIT_ACTION)
    assert info["step_delta_goal_resource_progress"] > 0.0
    assert reward > 0.0


def test_required_building_started_bonus_tracks_new_site():
    env = SiedlerScharfschuetzenEnv(
        use_spatial_obs=False,
        reward_profile={
            "step_required_building_started_bonus": 5.0,
            "step_delta_positive_only": 1.0,
        },
    )
    env.reset(seed=0)
    building = _find_gunsmith_key(env)
    env.construction_sites.append(
        {
            "building": building,
            "position": {"x": 0, "y": 0},
            "total_time": 100.0,
            "remaining_work": 100.0,
            "serfs_assigned": 0,
            "site_id": 999,
        }
    )

    _, reward, _, _, info = env.step(WAIT_ACTION)

    assert info["step_new_required_buildings_started"] == 1
    assert reward == pytest.approx(5.0)
