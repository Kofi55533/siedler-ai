# -*- coding: utf-8 -*-
"""
Schneller Training-Test für Siedler AI
Testet ob das Training-Setup funktioniert (10k Steps)
"""

import os
from datetime import datetime

import gymnasium as gym
import torch as th
from sb3_contrib import MaskablePPO
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv

from environment import SiedlerScharfschuetzenEnv
from multihead_policy import MultiHeadMaskablePolicy, SpatialVectorExtractor
from training_profiles import build_training_config


class ProgressCallback(BaseCallback):
    """Zeigt Fortschritt während des Trainings."""

    def __init__(self, check_freq: int = 1000):
        super().__init__()
        self.check_freq = check_freq
        self.best_scharfschuetzen = 0

    def _get_env_attr(self, name, default=None):
        if hasattr(self.training_env, "get_attr"):
            try:
                return self.training_env.get_attr(name)[0]
            except Exception:
                pass
        if hasattr(self.training_env, "envs"):
            env = self.training_env.envs[0]
            if hasattr(env, "unwrapped"):
                env = env.unwrapped
            return getattr(env, name, default)
        return default

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:
            scharfschuetzen = self._get_env_attr("scharfschuetzen", 0)
            current_time = self._get_env_attr("current_time", 0)
            researched = len(self._get_env_attr("researched_techs", set()))

            if scharfschuetzen > self.best_scharfschuetzen:
                self.best_scharfschuetzen = scharfschuetzen

            print(f"Step {self.n_calls}: Zeit={current_time}s, "
                  f"Techs={researched}, Scharfschuetzen={scharfschuetzen} "
                  f"(Best: {self.best_scharfschuetzen})")
        return True


def _get_n_envs():
    env_val = os.environ.get("SIEDLER_NUM_ENVS")
    if env_val:
        return max(1, int(env_val))
    cpu = os.cpu_count() or 1
    return max(1, min(8, cpu // 2))


def _get_spatial_size():
    size_val = os.environ.get("SIEDLER_SPATIAL_SIZE")
    if size_val:
        return max(16, int(size_val))
    return 128


def make_env(
    rank: int,
    seed: int = 0,
    use_spatial_obs: bool = True,
    spatial_size: int = 128,
    reward_profile: dict = None,
):
    def _init():
        env = SiedlerScharfschuetzenEnv(
            player_id=1,
            use_spatial_obs=use_spatial_obs,
            spatial_size=spatial_size,
            reward_profile=reward_profile,
        )
        env.reset(seed=seed + rank)
        return env
    return _init


def create_env(use_spatial_obs: bool = True, spatial_size: int = 128, reward_profile: dict = None):
    """Erstellt (ggf.) vektorisierte Environments."""
    n_envs = _get_n_envs()
    if n_envs > 1:
        return SubprocVecEnv([
            make_env(
                i,
                use_spatial_obs=use_spatial_obs,
                spatial_size=spatial_size,
                reward_profile=reward_profile,
            )
            for i in range(n_envs)
        ])
    return DummyVecEnv([
        make_env(
            0,
            use_spatial_obs=use_spatial_obs,
            spatial_size=spatial_size,
            reward_profile=reward_profile,
        )
    ])


def _select_net_arch(obs_dim: int):
    if obs_dim >= 400:
        return [1024, 512, 512]
    if obs_dim >= 250:
        return [768, 512, 256]
    return [512, 256, 256]


def quick_test():
    """Schneller Trainings-Test (10k Steps)."""
    print("=" * 60)
    print("SIEDLER AI - SCHNELLER TRAININGS-TEST")
    print("=" * 60)
    base_config = {
        "learning_rate": 0.0003,
        "n_steps": 512,
        "batch_size": 64,
        "n_epochs": 5,
        "gamma": 0.99,
        "ent_coef": 0.01,
    }
    config, profile = build_training_config(base_config)
    reward_profile = profile["reward_profile"]
    print(f"Train-Profil: {profile['name']} ({profile['description']})")

    use_spatial_obs = True
    spatial_size = _get_spatial_size()
    env = create_env(
        use_spatial_obs=use_spatial_obs,
        spatial_size=spatial_size,
        reward_profile=reward_profile,
    )
    n_envs = getattr(env, "num_envs", 1)
    print(f"Envs: {n_envs}")
    print(f"Action Space: {env.action_space.n}")
    if isinstance(env.observation_space, gym.spaces.Dict):
        print(f"Observation Space: vector={env.observation_space['vector'].shape}, "
              f"spatial={env.observation_space['spatial'].shape}")
    else:
        print(f"Observation Space: {env.observation_space.shape}")
    device = "cuda" if th.cuda.is_available() else "cpu"
    print(f"Device: {device}")
    print(
        "PPO: "
        f"lr={config['learning_rate']} "
        f"gamma={config['gamma']} "
        f"n_steps={config['n_steps']} "
        f"batch={config['batch_size']} "
        f"epochs={config['n_epochs']} "
        f"ent={config['ent_coef']}"
    )

    # Modell erstellen
    head_sizes = env.env_method("get_action_head_sizes")[0]
    phase_dim = env.get_attr("phase_dim")[0]
    if isinstance(env.observation_space, gym.spaces.Dict):
        obs_dim = env.observation_space["vector"].shape[0]
    else:
        obs_dim = env.observation_space.shape[0]
    net_arch = _select_net_arch(obs_dim)
    policy_kwargs = {
        "net_arch": net_arch,
        "action_head_sizes": head_sizes,
        "phase_dim": phase_dim,
    }
    if isinstance(env.observation_space, gym.spaces.Dict):
        policy_kwargs.update({
            "features_extractor_class": SpatialVectorExtractor,
            "features_extractor_kwargs": {
                "cnn_out_dim": 128,
                "vector_out_dim": 256,
            },
        })
    model = MaskablePPO(
        MultiHeadMaskablePolicy,
        env,
        learning_rate=config["learning_rate"],
        n_steps=config["n_steps"],
        batch_size=config["batch_size"],
        n_epochs=config["n_epochs"],
        gamma=config["gamma"],
        ent_coef=config["ent_coef"],
        policy_kwargs=policy_kwargs,
        device=device,
        verbose=0,
    )

    print("\nStarte Training (10.000 Steps)...")
    print("-" * 60)

    callback = ProgressCallback(check_freq=1000)

    model.learn(
        total_timesteps=10_000,
        callback=callback,
        progress_bar=True,
    )

    print("-" * 60)
    print(f"Training abgeschlossen!")
    print(f"Beste Scharfschuetzen: {callback.best_scharfschuetzen}")

    # Kurze Evaluation
    print("\n" + "=" * 60)
    print("EVALUATION (1 Episode)")
    print("=" * 60)

    eval_env = SiedlerScharfschuetzenEnv(
        player_id=1,
        use_spatial_obs=use_spatial_obs,
        spatial_size=spatial_size,
        reward_profile=reward_profile,
    )
    obs, _ = eval_env.reset()
    done = False
    total_reward = 0
    steps = 0

    while not done:
        action_mask = eval_env.get_action_mask()
        action, _ = model.predict(obs, deterministic=True, action_masks=action_mask)
        obs, reward, terminated, truncated, info = eval_env.step(action)
        total_reward += reward
        done = terminated or truncated
        steps += 1

    print(f"Steps: {steps}")
    print(f"Zeit: {eval_env.current_time}s / {eval_env.max_time}s")
    print(f"Reward: {total_reward:.2f}")
    print(f"Scharfschuetzen: {eval_env.scharfschuetzen}")
    print(f"Erforschte Techs: {len(eval_env.researched_techs)}")
    print(f"Techs: {eval_env.researched_techs}")

    # Gebaeude-Uebersicht
    built = {k: v for k, v in eval_env.buildings.items() if v > 0}
    print(f"Gebaeude: {built}")

    return model


if __name__ == "__main__":
    quick_test()
