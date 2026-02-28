# -*- coding: utf-8 -*-
"""
Siedler AI - Training mit 100k Steps
Starte dieses Skript für ein erstes sinnvolles Training.
"""

import os
from datetime import datetime

import gymnasium as gym
import torch as th
from sb3_contrib import MaskablePPO
from stable_baselines3.common.callbacks import BaseCallback, CheckpointCallback
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv

from environment import SiedlerScharfschuetzenEnv
from multihead_policy import MultiHeadMaskablePolicy, SpatialVectorExtractor
from training_profiles import get_train_profile

# Pfad für Modelle
SAVE_PATH = "./siedler_training_100k"
os.makedirs(SAVE_PATH, exist_ok=True)

# Performance
th.backends.cudnn.benchmark = True


def _select_net_arch(obs_dim: int):
    if obs_dim >= 400:
        return [1024, 512, 512]
    if obs_dim >= 250:
        return [768, 512, 256]
    return [512, 256, 256]


class DetailedCallback(BaseCallback):
    """Detaillierter Fortschritts-Callback."""

    def __init__(self, check_freq: int = 5000):
        super().__init__()
        self.check_freq = check_freq
        self.best_scharfschuetzen = 0
        self.episode_count = 0

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
        # Episode-Ende erkennen
        if self.locals.get("dones", [False])[0]:
            self.episode_count += 1

        if self.n_calls % self.check_freq == 0:
            scharfschuetzen = self._get_env_attr("scharfschuetzen", 0)
            current_time = self._get_env_attr("current_time", 0)
            researched = list(self._get_env_attr("researched_techs", set()))
            buildings = {k: v for k, v in self._get_env_attr("buildings", {}).items() if v > 0}

            if scharfschuetzen > self.best_scharfschuetzen:
                self.best_scharfschuetzen = scharfschuetzen
                print(f"[NEUER REKORD] {scharfschuetzen} Scharfschuetzen!")

            print(f"\n--- Step {self.n_calls} (Episode ~{self.episode_count}) ---")
            print(f"  Zeit: {current_time}s")
            print(f"  Techs: {researched[:5]}{'...' if len(researched) > 5 else ''}")
            print(f"  Scharfschuetzen: {scharfschuetzen} (Best: {self.best_scharfschuetzen})")
            print(f"  Gebaeude: {list(buildings.keys())[:5]}")

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


def train():
    """Training mit 100k Steps."""
    print("=" * 70)
    print("SIEDLER AI - 100K TRAINING")
    print("=" * 70)
    print(f"Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Save Path: {SAVE_PATH}")
    print("=" * 70)
    profile = get_train_profile()
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
        learning_rate=0.0003,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.02,  # Mehr Exploration
        policy_kwargs=policy_kwargs,
        device=device,
        verbose=0,
        tensorboard_log=f"{SAVE_PATH}/tensorboard/",
    )

    # Callbacks
    checkpoint_callback = CheckpointCallback(
        save_freq=25_000,
        save_path=SAVE_PATH,
        name_prefix="siedler"
    )
    progress_callback = DetailedCallback(check_freq=5000)

    print("\nStarte Training (100.000 Steps)...")
    print("-" * 70)

    model.learn(
        total_timesteps=100_000,
        callback=[checkpoint_callback, progress_callback],
        progress_bar=True,
    )

    # Speichern
    model.save(f"{SAVE_PATH}/siedler_100k_final")
    print(f"\nModell gespeichert: {SAVE_PATH}/siedler_100k_final")

    # Finale Evaluation
    print("\n" + "=" * 70)
    print("FINALE EVALUATION (3 Episoden)")
    print("=" * 70)

    eval_env = SiedlerScharfschuetzenEnv(
        player_id=1,
        use_spatial_obs=use_spatial_obs,
        spatial_size=spatial_size,
        reward_profile=reward_profile,
    )

    total_scharfschuetzen = 0
    for ep in range(3):
        obs, _ = eval_env.reset()
        done = False
        reward_sum = 0

        while not done:
            action_mask = eval_env.get_action_mask()
            action, _ = model.predict(obs, deterministic=True, action_masks=action_mask)
            obs, reward, terminated, truncated, info = eval_env.step(action)
            reward_sum += reward
            done = terminated or truncated

        total_scharfschuetzen += eval_env.scharfschuetzen
        print(f"Episode {ep+1}: Scharfschuetzen={eval_env.scharfschuetzen}, "
              f"Techs={len(eval_env.researched_techs)}, Reward={reward_sum:.1f}")

    print(f"\nDurchschnitt: {total_scharfschuetzen/3:.1f} Scharfschuetzen")
    print(f"Beste je erreicht: {progress_callback.best_scharfschuetzen}")

    print("\n" + "=" * 70)
    print(f"TRAINING ABGESCHLOSSEN")
    print(f"Ende: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    return model


if __name__ == "__main__":
    train()
