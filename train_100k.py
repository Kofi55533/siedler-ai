# -*- coding: utf-8 -*-
"""
Siedler AI - Training mit 100k Steps
Starte dieses Skript für ein erstes sinnvolles Training.
"""

import os
from datetime import datetime

from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker
from stable_baselines3.common.callbacks import BaseCallback, CheckpointCallback

from environment import SiedlerScharfschuetzenEnv

# Pfad für Modelle
SAVE_PATH = "./siedler_training_100k"
os.makedirs(SAVE_PATH, exist_ok=True)


class DetailedCallback(BaseCallback):
    """Detaillierter Fortschritts-Callback."""

    def __init__(self, check_freq: int = 5000):
        super().__init__()
        self.check_freq = check_freq
        self.best_scharfschuetzen = 0
        self.episode_count = 0

    def _on_step(self) -> bool:
        # Episode-Ende erkennen
        if self.locals.get("dones", [False])[0]:
            self.episode_count += 1

        if self.n_calls % self.check_freq == 0:
            if hasattr(self.training_env, 'envs'):
                env = self.training_env.envs[0]
                if hasattr(env, 'unwrapped'):
                    env = env.unwrapped

                scharfschuetzen = getattr(env, 'scharfschuetzen', 0)
                current_time = getattr(env, 'current_time', 0)
                researched = list(getattr(env, 'researched_techs', set()))
                buildings = {k: v for k, v in getattr(env, 'buildings', {}).items() if v > 0}

                if scharfschuetzen > self.best_scharfschuetzen:
                    self.best_scharfschuetzen = scharfschuetzen
                    print(f"[NEUER REKORD] {scharfschuetzen} Scharfschuetzen!")

                print(f"\n--- Step {self.n_calls} (Episode ~{self.episode_count}) ---")
                print(f"  Zeit: {current_time}s")
                print(f"  Techs: {researched[:5]}{'...' if len(researched) > 5 else ''}")
                print(f"  Scharfschuetzen: {scharfschuetzen} (Best: {self.best_scharfschuetzen})")
                print(f"  Gebaeude: {list(buildings.keys())[:5]}")

        return True


def create_env():
    """Erstellt Environment mit Action Masking."""
    env = SiedlerScharfschuetzenEnv(player_id=1)
    env = ActionMasker(env, lambda e: e.unwrapped.get_action_mask())
    return env


def train():
    """Training mit 100k Steps."""
    print("=" * 70)
    print("SIEDLER AI - 100K TRAINING")
    print("=" * 70)
    print(f"Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Save Path: {SAVE_PATH}")
    print("=" * 70)

    env = create_env()
    print(f"Action Space: {env.action_space.n}")
    print(f"Observation Space: {env.observation_space.shape}")

    # Modell erstellen
    model = MaskablePPO(
        "MlpPolicy",
        env,
        learning_rate=0.0003,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.02,  # Mehr Exploration
        policy_kwargs={"net_arch": [512, 256, 256]},
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

    total_scharfschuetzen = 0
    for ep in range(3):
        obs, _ = env.reset()
        done = False
        reward_sum = 0

        while not done:
            action_mask = env.unwrapped.get_action_mask()
            action, _ = model.predict(obs, deterministic=True, action_masks=action_mask)
            obs, reward, terminated, truncated, info = env.step(action)
            reward_sum += reward
            done = terminated or truncated

        final_env = env.unwrapped
        total_scharfschuetzen += final_env.scharfschuetzen
        print(f"Episode {ep+1}: Scharfschuetzen={final_env.scharfschuetzen}, "
              f"Techs={len(final_env.researched_techs)}, Reward={reward_sum:.1f}")

    print(f"\nDurchschnitt: {total_scharfschuetzen/3:.1f} Scharfschuetzen")
    print(f"Beste je erreicht: {progress_callback.best_scharfschuetzen}")

    print("\n" + "=" * 70)
    print(f"TRAINING ABGESCHLOSSEN")
    print(f"Ende: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    return model


if __name__ == "__main__":
    train()
