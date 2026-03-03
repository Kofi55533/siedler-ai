# -*- coding: utf-8 -*-
"""
Trainings- und Reward-Profile fuer reproduzierbares Colab-Training.
"""

import copy
import os
from typing import Dict, Optional, Tuple

DEFAULT_TRAIN_PROFILE = "sparse"


TRAIN_PROFILES = {
    "legacy": {
        "description": "Historisches Verhalten (alte Reward-Gewichte).",
        "config_overrides": {},
        "reward_profile": {
            # Legacy bekommt explizites Serf-Economy-Shaping:
            # Kaufen bleibt growth-basiert.
            "action_buy_serf_growth_bonus": 1.0,
            # Wie dense_v2: +1 je neuem Taxable-Worker-Highscore.
            "step_worker_growth_bonus": 1.0,
        },
    },
    "balanced": {
        "description": "Empfohlen fuer stabiles Colab-Training.",
        "config_overrides": {
            "learning_rate": 0.00025,
            "gamma": 0.997,
            "ent_coef": 0.015,
            "batch_size": 128,
        },
        "reward_profile": {},
    },
    "aggressive": {
        "description": "Schnellere Exploration mit dichterem Reward.",
        "config_overrides": {
            "learning_rate": 0.00035,
            "gamma": 0.995,
            "ent_coef": 0.02,
        },
        "reward_profile": {},
    },
    "sparse": {
        "description": "Nahe am Endziel mit wenig dichten Shaping-Rewards.",
        "config_overrides": {
            "learning_rate": 0.0002,
            "gamma": 0.999,
            "ent_coef": 0.02,
            "batch_size": 128,
        },
        "reward_profile": {},
    },
    "dense_v2": {
        "description": "Event-Reward fuer Potential + Steuerbasis/Taler-Income-Wachstum.",
        "config_overrides": {
            "learning_rate": 0.00025,
            "gamma": 0.997,
            "ent_coef": 0.015,
            "batch_size": 128,
        },
        "reward_profile": {
            # +1 Reward je neuem Highscore bei potenziell rekrutierbaren T2-Scharfschuetzen.
            "step_new_resource_potential_unit_bonus": 1.0,
            "step_potential_scharf_tier": 2.0,
            "step_worker_growth_bonus": 1.0,
        },
    },
}

PROFILE_ALIASES = {
    "default": DEFAULT_TRAIN_PROFILE,
    "stable": "balanced",
    "colab": "sparse",
    "fast": "aggressive",
    "dense": "dense_v2",
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
