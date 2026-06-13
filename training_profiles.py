# -*- coding: utf-8 -*-
"""
Trainings- und Reward-Profile fuer reproduzierbares Colab-Training.
"""

import copy
import os
from typing import Dict, Optional, Tuple

DEFAULT_TRAIN_PROFILE = "guided_v1"


TRAIN_PROFILES = {
    "legacy": {
        "description": "Historisches Verhalten (alte Reward-Gewichte).",
        "config_overrides": {},
        "reward_profile": {
            # Legacy bekommt explizites Serf-Economy-Shaping:
            # Kaufen bleibt growth-basiert.
            "action_buy_serf_growth_bonus": 1.0,
            # Einmalig pro neu gekauftem/spawned FREE-Serf bei erster Zuweisung.
            "action_assign_spawned_serf_bonus": 1.0,
            # Wie dense_v2: +1 je neuem Taxable-Worker-Highscore.
            "step_worker_growth_bonus": 1.0,
        },
    },
    "balanced": {
        "description": "Stabiles Training mit zielnaher, aber noch relativ dichter Belohnung.",
        "config_overrides": {
            "learning_rate": 0.00025,
            "gamma": 0.999,
            "ent_coef": 0.015,
            "batch_size": 256,
            "n_epochs": 4,
        },
        "reward_profile": {
            "terminal_dependency_bonus": 0.5,
            "terminal_recruitable_bonus": 2.0,
            "terminal_potential_bonus_per_unit": 8.0,
            "terminal_potential_use_cumulative_earnings": 0.0,
            "terminal_potential_include_start_resources": 0.0,
            "terminal_potential_scharf_tier": 1.0,
            "terminal_potential_require_path_ready": 1.0,
            "step_potential_use_cumulative_earnings": 0.0,
            "step_potential_include_start_resources": 0.0,
            "step_potential_scharf_tier": 1.0,
            "step_delta_potential_bonus": 0.4,
            "step_new_resource_potential_unit_bonus": 0.75,
            "step_delta_progress_bonus": 0.2,
            "step_delta_dependency_bonus": 0.1,
            "step_delta_research_bonus": 0.1,
            "step_delta_construction_bonus": 0.1,
            "step_worker_growth_bonus": 0.015,
            "step_unlock_recruitable_bonus": 2.0,
            "step_time_penalty": 0.001,
            "action_buy_serf_growth_bonus": 0.01,
            "action_assign_spawned_serf_bonus": 0.005,
        },
    },
    "aggressive": {
        "description": "Mehr Exploration und dichteres Shaping fuer fruehe Unlock-Fortschritte.",
        "config_overrides": {
            "learning_rate": 0.00035,
            "gamma": 0.999,
            "ent_coef": 0.02,
            "batch_size": 256,
            "n_epochs": 4,
        },
        "reward_profile": {
            "terminal_dependency_bonus": 0.75,
            "terminal_recruitable_bonus": 3.0,
            "terminal_potential_bonus_per_unit": 6.0,
            "terminal_potential_use_cumulative_earnings": 0.0,
            "terminal_potential_include_start_resources": 0.0,
            "terminal_potential_scharf_tier": 1.0,
            "terminal_potential_require_path_ready": 1.0,
            "step_potential_use_cumulative_earnings": 0.0,
            "step_potential_include_start_resources": 0.0,
            "step_potential_scharf_tier": 1.0,
            "step_delta_potential_bonus": 0.5,
            "step_new_resource_potential_unit_bonus": 1.0,
            "step_delta_progress_bonus": 0.35,
            "step_delta_dependency_bonus": 0.2,
            "step_delta_research_bonus": 0.2,
            "step_delta_construction_bonus": 0.2,
            "step_worker_growth_bonus": 0.02,
            "step_unlock_recruitable_bonus": 3.0,
            "step_time_penalty": 0.001,
            "action_buy_serf_growth_bonus": 0.015,
            "action_assign_spawned_serf_bonus": 0.0075,
        },
    },
    "sparse": {
        "description": "Fast nur das Endziel: finales rekrutierbares Scharfschuetzen-Potential.",
        "config_overrides": {
            "learning_rate": 0.0002,
            "gamma": 0.999,
            "ent_coef": 0.015,
            "batch_size": 256,
            "n_epochs": 4,
        },
        "reward_profile": {
            "terminal_potential_bonus_per_unit": 10.0,
            "terminal_potential_use_cumulative_earnings": 0.0,
            "terminal_potential_include_start_resources": 0.0,
            "terminal_potential_scharf_tier": 1.0,
            "terminal_potential_require_path_ready": 1.0,
        },
    },
    "dense_v2": {
        "description": "Dichteres Current-Stock-Shaping fuer Scharfschuetzen-Potential.",
        "config_overrides": {
            "learning_rate": 0.00025,
            "gamma": 0.999,
            "ent_coef": 0.015,
            "batch_size": 256,
            "n_epochs": 4,
        },
        "reward_profile": {
            "terminal_dependency_bonus": 0.5,
            "terminal_recruitable_bonus": 2.0,
            "terminal_potential_bonus_per_unit": 8.0,
            "terminal_potential_use_cumulative_earnings": 0.0,
            "terminal_potential_include_start_resources": 0.0,
            "terminal_potential_scharf_tier": 1.0,
            "terminal_potential_require_path_ready": 1.0,
            "step_new_resource_potential_unit_bonus": 1.0,
            "step_delta_potential_bonus": 0.5,
            "step_potential_use_cumulative_earnings": 0.0,
            "step_potential_include_start_resources": 0.0,
            "step_potential_scharf_tier": 1.0,
            "step_worker_growth_bonus": 0.02,
            "step_unlock_recruitable_bonus": 2.0,
            "step_time_penalty": 0.001,
        },
    },
    "curriculum_unlock": {
        "description": "Phase 1: Wirtschaft stabilisieren und Scharfschuetzen-Pfad freischalten.",
        "config_overrides": {
            "learning_rate": 0.00025,
            "gamma": 0.999,
            "ent_coef": 0.02,
            "batch_size": 256,
            "n_epochs": 4,
        },
        "reward_profile": {
            "terminal_dependency_bonus": 1.0,
            "terminal_recruitable_bonus": 4.0,
            "terminal_potential_bonus_per_unit": 2.0,
            "terminal_potential_use_cumulative_earnings": 0.0,
            "terminal_potential_include_start_resources": 0.0,
            "terminal_potential_scharf_tier": 1.0,
            "terminal_potential_require_path_ready": 1.0,
            "step_potential_use_cumulative_earnings": 0.0,
            "step_potential_include_start_resources": 0.0,
            "step_potential_scharf_tier": 1.0,
            "step_delta_potential_bonus": 0.15,
            "step_delta_progress_bonus": 0.6,
            "step_delta_dependency_bonus": 0.4,
            "step_delta_research_bonus": 0.4,
            "step_delta_construction_bonus": 0.4,
            "step_worker_growth_bonus": 0.03,
            "step_unlock_recruitable_bonus": 5.0,
            "step_expert_opening_milestone_bonus": 8.0,
            "step_time_penalty": 0.00075,
            "action_buy_serf_growth_bonus": 0.025,
            "action_assign_spawned_serf_bonus": 0.01,
        },
    },
    "curriculum_stockpile": {
        "description": "Phase 2: Nach dem Unlock Taler/Schwefel fuer viele Scharfschuetzen ansparen.",
        "config_overrides": {
            "learning_rate": 0.0002,
            "gamma": 0.999,
            "ent_coef": 0.012,
            "batch_size": 256,
            "n_epochs": 4,
        },
        "reward_profile": {
            "terminal_dependency_bonus": 0.5,
            "terminal_recruitable_bonus": 3.0,
            "terminal_potential_bonus_per_unit": 10.0,
            "terminal_potential_use_cumulative_earnings": 0.0,
            "terminal_potential_include_start_resources": 0.0,
            "terminal_potential_scharf_tier": 1.0,
            "terminal_potential_require_path_ready": 1.0,
            "step_potential_use_cumulative_earnings": 0.0,
            "step_potential_include_start_resources": 0.0,
            "step_potential_scharf_tier": 1.0,
            "step_delta_potential_bonus": 0.6,
            "step_new_resource_potential_unit_bonus": 1.0,
            "step_delta_progress_bonus": 0.15,
            "step_delta_dependency_bonus": 0.05,
            "step_delta_research_bonus": 0.05,
            "step_delta_construction_bonus": 0.05,
            "step_worker_growth_bonus": 0.01,
            "step_unlock_recruitable_bonus": 2.0,
            "step_time_penalty": 0.001,
            "action_buy_serf_growth_bonus": 0.01,
            "action_assign_spawned_serf_bonus": 0.005,
        },
    },
    "guided_v1": {
        "description": "Empfohlen: zielgefuehrtes Training mit kleinerem Suchraum und fruehem Ressourcen-/Baupfad-Shaping.",
        "config_overrides": {
            "learning_rate": 0.00025,
            "gamma": 0.999,
            "ent_coef": 0.008,
            "batch_size": 256,
            "n_epochs": 4,
        },
        "reward_profile": {
            "goal_action_pruning": 1.0,
            "goal_pruning_max_tree_targets": 32.0,
            "terminal_dependency_bonus": 0.5,
            "terminal_path_ready_bonus": 10.0,
            "terminal_recruitable_bonus": 3.0,
            "terminal_potential_bonus_per_unit": 12.0,
            "terminal_scharf_count_bonus": 25.0,
            "terminal_potential_use_cumulative_earnings": 0.0,
            "terminal_potential_include_start_resources": 0.0,
            "terminal_potential_scharf_tier": 1.0,
            "terminal_potential_require_path_ready": 1.0,
            "step_potential_use_cumulative_earnings": 0.0,
            "step_potential_include_start_resources": 0.0,
            "step_potential_scharf_tier": 1.0,
            "step_delta_potential_bonus": 0.2,
            "step_new_resource_potential_unit_bonus": 0.5,
            "step_goal_resource_progress_bonus": 2.5,
            "step_delta_progress_bonus": 0.2,
            "step_delta_dependency_bonus": 0.08,
            "step_delta_research_bonus": 0.08,
            "step_delta_construction_bonus": 0.08,
            "step_required_building_affordable_bonus": 2.0,
            "step_required_building_started_bonus": 5.0,
            "step_required_building_complete_bonus": 8.0,
            "step_required_tech_complete_bonus": 4.0,
            "step_path_ready_bonus": 12.0,
            "step_expert_opening_milestone_bonus": 6.0,
            "step_scharf_recruited_bonus": 30.0,
            "step_worker_growth_bonus": 0.01,
            "step_unlock_recruitable_bonus": 3.0,
            "step_time_penalty": 0.0005,
            "action_buy_serf_growth_bonus": 0.006,
            "action_assign_spawned_serf_bonus": 0.003,
        },
    },
    "goal_v1": {
        "description": "Empfohlen: maximiert das finale Potential sofort rekrutierbarer Scharfschuetzen.",
        "config_overrides": {
            "learning_rate": 0.0002,
            "gamma": 0.999,
            "ent_coef": 0.01,
            "batch_size": 256,
            "n_epochs": 4,
        },
        "reward_profile": {
            "terminal_dependency_bonus": 0.25,
            "terminal_recruitable_bonus": 2.0,
            "terminal_potential_bonus_per_unit": 12.0,
            "terminal_potential_use_cumulative_earnings": 0.0,
            "terminal_potential_include_start_resources": 0.0,
            "terminal_potential_scharf_tier": 1.0,
            "terminal_potential_require_path_ready": 1.0,
            "step_potential_use_cumulative_earnings": 0.0,
            "step_potential_include_start_resources": 0.0,
            "step_potential_scharf_tier": 1.0,
            "step_delta_potential_bonus": 0.25,
            "step_new_resource_potential_unit_bonus": 0.5,
            "step_delta_progress_bonus": 0.08,
            "step_delta_dependency_bonus": 0.04,
            "step_delta_research_bonus": 0.04,
            "step_delta_construction_bonus": 0.04,
            "step_worker_growth_bonus": 0.008,
            "step_unlock_recruitable_bonus": 1.5,
            "step_time_penalty": 0.001,
            "action_buy_serf_growth_bonus": 0.005,
            "action_assign_spawned_serf_bonus": 0.0025,
        },
    },
}

PROFILE_ALIASES = {
    "default": DEFAULT_TRAIN_PROFILE,
    "recommended": DEFAULT_TRAIN_PROFILE,
    "guided": "guided_v1",
    "goal": "goal_v1",
    "stable": "balanced",
    "colab": "sparse",
    "fast": "aggressive",
    "dense": "dense_v2",
    "unlock": "curriculum_unlock",
    "stockpile": "curriculum_stockpile",
}


def resolve_profile_name(profile_name: Optional[str] = None) -> str:
    raw = profile_name if profile_name is not None else os.environ.get("SIEDLER_TRAIN_PROFILE")
    candidate = (raw or DEFAULT_TRAIN_PROFILE).strip().lower()
    candidate = PROFILE_ALIASES.get(candidate, candidate)
    if candidate not in TRAIN_PROFILES:
        return DEFAULT_TRAIN_PROFILE
    return candidate


def get_train_profile(profile_name: Optional[str] = None) -> Dict[str, object]:
    name = resolve_profile_name(profile_name)
    spec = TRAIN_PROFILES[name]
    return {
        "name": name,
        "description": spec["description"],
        "config_overrides": copy.deepcopy(spec.get("config_overrides", {})),
        "reward_profile": copy.deepcopy(spec.get("reward_profile", {})),
    }


def build_training_config(
    base_config: Dict[str, object],
    custom_config: Optional[Dict[str, object]] = None,
    profile_name: Optional[str] = None,
) -> Tuple[Dict[str, object], Dict[str, object]]:
    profile = get_train_profile(profile_name)
    merged = copy.deepcopy(base_config)
    merged.update(profile["config_overrides"])
    if custom_config:
        merged.update(custom_config)
    return merged, profile
