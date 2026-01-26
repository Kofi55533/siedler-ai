# -*- coding: utf-8 -*-
"""
Schneller Training-Test für Siedler AI
Testet ob das Training-Setup funktioniert (10k Steps)
"""

import os
from datetime import datetime

from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker
from stable_baselines3.common.callbacks import BaseCallback

from environment import SiedlerScharfschuetzenEnv


class ProgressCallback(BaseCallback):
    """Zeigt Fortschritt während des Trainings."""

    def __init__(self, check_freq: int = 1000):
        super().__init__()
        self.check_freq = check_freq
        self.best_scharfschuetzen = 0

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:
            if hasattr(self.training_env, 'envs'):
                env = self.training_env.envs[0]
                if hasattr(env, 'unwrapped'):
                    env = env.unwrapped

                scharfschuetzen = getattr(env, 'scharfschuetzen', 0)
                current_time = getattr(env, 'current_time', 0)
                researched = len(getattr(env, 'researched_techs', set()))

                if scharfschuetzen > self.best_scharfschuetzen:
                    self.best_scharfschuetzen = scharfschuetzen

                print(f"Step {self.n_calls}: Zeit={current_time}s, "
                      f"Techs={researched}, Scharfschuetzen={scharfschuetzen} "
                      f"(Best: {self.best_scharfschuetzen})")
        return True


def create_env():
    """Erstellt Environment mit Action Masking."""
    env = SiedlerScharfschuetzenEnv(player_id=1)
    env = ActionMasker(env, lambda e: e.unwrapped.get_action_mask())
    return env


def quick_test():
    """Schneller Trainings-Test (10k Steps)."""
    print("=" * 60)
    print("SIEDLER AI - SCHNELLER TRAININGS-TEST")
    print("=" * 60)

    env = create_env()
    print(f"Action Space: {env.action_space.n}")
    print(f"Observation Space: {env.observation_space.shape}")

    # Modell erstellen
    model = MaskablePPO(
        "MlpPolicy",
        env,
        learning_rate=0.0003,
        n_steps=512,
        batch_size=64,
        n_epochs=5,
        gamma=0.99,
        ent_coef=0.01,
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

    obs, _ = env.reset()
    done = False
    total_reward = 0
    steps = 0

    while not done:
        action_mask = env.unwrapped.get_action_mask()
        action, _ = model.predict(obs, deterministic=True, action_masks=action_mask)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        done = terminated or truncated
        steps += 1

    final_env = env.unwrapped
    print(f"Steps: {steps}")
    print(f"Zeit: {final_env.current_time}s / {final_env.max_time}s")
    print(f"Reward: {total_reward:.2f}")
    print(f"Scharfschuetzen: {final_env.scharfschuetzen}")
    print(f"Erforschte Techs: {len(final_env.researched_techs)}")
    print(f"Techs: {final_env.researched_techs}")

    # Gebäude-Übersicht
    built = {k: v for k, v in final_env.buildings.items() if v > 0}
    print(f"Gebäude: {built}")

    return model


if __name__ == "__main__":
    quick_test()
