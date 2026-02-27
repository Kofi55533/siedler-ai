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
            "terminal_scharfschuetzen_bonus": 20.0,
            "recruit_scharfschuetzen_bonus": 10.0,
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
        "reward_profile": {
            "terminal_scharfschuetzen_bonus": 30.0,
            "recruit_scharfschuetzen_bonus": 3.0,
        },
    },
    "aggressive": {
        "description": "Schnellere Exploration mit dichterem Reward.",
        "config_overrides": {
            "learning_rate": 0.00035,
            "gamma": 0.995,
            "ent_coef": 0.02,
        },
        "reward_profile": {
            "terminal_scharfschuetzen_bonus": 22.0,
            "recruit_scharfschuetzen_bonus": 8.0,
        },
    },
    "sparse": {
        "description": "Nahe am Endziel: fast nur terminale Bewertung.",
        "config_overrides": {
            "learning_rate": 0.0002,
            "gamma": 0.999,
            "ent_coef": 0.02,
            "batch_size": 128,
        },
        "reward_profile": {
            "terminal_scharfschuetzen_bonus": 35.0,
            "recruit_scharfschuetzen_bonus": 0.0,
        },
    },
}

PROFILE_ALIASES = {
    "default": DEFAULT_TRAIN_PROFILE,
    "stable": "balanced",
    "colab": "sparse",
    "fast": "aggressive",
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
