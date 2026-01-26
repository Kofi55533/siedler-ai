# -*- coding: utf-8 -*-
"""
Siedler 5 - Scharfschützen Training Script für Google Colab

Dieses Script kann in Google Colab ausgeführt werden.
Kopiere map_config_wintersturm.py und environment.py ebenfalls in Colab.

Verwendung in Colab:
1. Lade alle 3 Dateien hoch (map_config_wintersturm.py, environment.py, colab_training.py)
2. Führe dieses Script aus
"""

# =============================================================================
# INSTALLATION (nur in Colab nötig)
# =============================================================================

def install_dependencies():
    """Installiert benötigte Pakete in Colab"""
    import subprocess
    import sys

    packages = [
        "gymnasium",
        "stable-baselines3",
        "sb3-contrib",
        "tensorboard",
    ]

    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])

    print("Alle Abhängigkeiten installiert!")


# =============================================================================
# IMPORTS
# =============================================================================

import os
import json
import numpy as np
from datetime import datetime

try:
    import gymnasium as gym
    from sb3_contrib import MaskablePPO
    from sb3_contrib.common.wrappers import ActionMasker
    from sb3_contrib.common.maskable.callbacks import MaskableEvalCallback
    from stable_baselines3.common.callbacks import CheckpointCallback, BaseCallback
    from stable_baselines3.common.vec_env import DummyVecEnv
except ImportError:
    print("Installiere Abhängigkeiten...")
    install_dependencies()
    import gymnasium as gym
    from sb3_contrib import MaskablePPO
    from sb3_contrib.common.wrappers import ActionMasker
    from sb3_contrib.common.maskable.callbacks import MaskableEvalCallback
    from stable_baselines3.common.callbacks import CheckpointCallback, BaseCallback
    from stable_baselines3.common.vec_env import DummyVecEnv

# Importiere unser Environment
from environment import SiedlerScharfschuetzenEnv


# =============================================================================
# CALLBACKS
# =============================================================================

class ScharfschuetzenCallback(BaseCallback):
    """Custom Callback zum Tracken des Trainingsfortschritts"""

    def __init__(self, check_freq: int = 1000, verbose: int = 1):
        super().__init__(verbose)
        self.check_freq = check_freq
        self.best_scharfschuetzen = 0
        self.episode_rewards = []
        self.episode_scharfschuetzen = []

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:
            # Hole Infos aus dem Environment
            if hasattr(self.training_env, 'envs'):
                env = self.training_env.envs[0]
                if hasattr(env, 'unwrapped'):
                    env = env.unwrapped

                scharfschuetzen = getattr(env, 'scharfschuetzen', 0)

                if scharfschuetzen > self.best_scharfschuetzen:
                    self.best_scharfschuetzen = scharfschuetzen
                    if self.verbose > 0:
                        print(f"Neuer Rekord: {scharfschuetzen} Scharfschützen!")

            # Log zum TensorBoard
            if self.verbose > 0 and self.n_calls % (self.check_freq * 10) == 0:
                print(f"Step {self.n_calls}: Best Scharfschützen = {self.best_scharfschuetzen}")

        return True


# =============================================================================
# TRAINING KONFIGURATION
# =============================================================================

TRAINING_CONFIG = {
    # Timesteps - ERHÖHT für sparse rewards (nur Scharfschützen am Ende)
    "total_timesteps": 5_000_000,  # 5M Steps für sparse rewards

    # Modell-Hyperparameter
    "learning_rate": 0.0003,
    "n_steps": 2048,
    "batch_size": 64,
    "n_epochs": 10,
    "gamma": 0.995,  # Höher für langfristige Planung (30 Min Episode)
    "gae_lambda": 0.95,
    "clip_range": 0.2,
    "ent_coef": 0.02,  # Exploration für 188 Actions

    # Netzwerk
    "policy_kwargs": {
        "net_arch": [512, 256, 256],
    },

    # Checkpoints
    "checkpoint_freq": 250_000,
    "eval_freq": 50_000,
}


# =============================================================================
# TRAINING FUNKTION
# =============================================================================

def create_env():
    """Erstellt das Environment mit Action Masking"""
    env = SiedlerScharfschuetzenEnv(player_id=1)
    env = ActionMasker(env, lambda e: e.unwrapped.get_action_mask())
    return env


def train(config: dict = None, save_path: str = "./siedler_model"):
    """
    Trainiert das Modell

    Args:
        config: Training-Konfiguration (optional)
        save_path: Pfad zum Speichern des Modells

    Returns:
        Trainiertes Modell
    """
    if config is None:
        config = TRAINING_CONFIG

    print("=" * 60)
    print("Siedler 5 - Scharfschützen Training")
    print("=" * 60)
    print(f"Timesteps: {config['total_timesteps']:,}")
    print(f"Learning Rate: {config['learning_rate']}")
    print(f"Batch Size: {config['batch_size']}")
    print("=" * 60)

    # Environment erstellen
    env = create_env()
    eval_env = create_env()

    print(f"\nAction Space: {env.action_space}")
    print(f"Observation Space: {env.observation_space}")

    # Callbacks
    checkpoint_callback = CheckpointCallback(
        save_freq=config["checkpoint_freq"],
        save_path=save_path,
        name_prefix="siedler_checkpoint"
    )

    scharfschuetzen_callback = ScharfschuetzenCallback(check_freq=1000)

    # Modell erstellen
    model = MaskablePPO(
        "MlpPolicy",
        env,
        learning_rate=config["learning_rate"],
        n_steps=config["n_steps"],
        batch_size=config["batch_size"],
        n_epochs=config["n_epochs"],
        gamma=config["gamma"],
        gae_lambda=config["gae_lambda"],
        clip_range=config["clip_range"],
        ent_coef=config["ent_coef"],
        policy_kwargs=config.get("policy_kwargs"),
        verbose=1,
        tensorboard_log=f"{save_path}/tensorboard/",
    )

    print("\nTraining startet...")
    print("(Checkpoints werden automatisch gespeichert)")
    print("-" * 60)

    # Training
    model.learn(
        total_timesteps=config["total_timesteps"],
        callback=[checkpoint_callback, scharfschuetzen_callback],
        progress_bar=True,
    )

    # Finales Modell speichern
    final_path = f"{save_path}/siedler_final"
    model.save(final_path)
    print(f"\nModell gespeichert: {final_path}")

    # Beste Ergebnisse
    print(f"\nBeste erreichte Scharfschützen: {scharfschuetzen_callback.best_scharfschuetzen}")

    return model


# =============================================================================
# EVALUATION FUNKTION
# =============================================================================

def evaluate(model, n_episodes: int = 10, render: bool = False):
    """
    Evaluiert das trainierte Modell

    Args:
        model: Trainiertes Modell
        n_episodes: Anzahl der Evaluations-Episoden
        render: Ob der Output gerendert werden soll

    Returns:
        Dictionary mit Evaluations-Ergebnissen
    """
    env = create_env()
    results = {
        "rewards": [],
        "scharfschuetzen": [],
        "times": [],
        "action_histories": [],
    }

    for episode in range(n_episodes):
        obs, _ = env.reset()
        total_reward = 0
        done = False

        while not done:
            action_mask = env.unwrapped.get_action_mask()
            action, _ = model.predict(obs, deterministic=True, action_masks=action_mask)
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            done = terminated or truncated

            if render and episode == 0:
                env.unwrapped.render()

        # Ergebnisse speichern
        results["rewards"].append(total_reward)
        results["scharfschuetzen"].append(env.unwrapped.scharfschuetzen)
        results["times"].append(env.unwrapped.current_time)
        results["action_histories"].append(env.unwrapped.get_action_history())

        print(f"Episode {episode + 1}: Reward={total_reward:.2f}, Scharfschützen={env.unwrapped.scharfschuetzen}")

    # Zusammenfassung
    print("\n" + "=" * 60)
    print("EVALUATION ZUSAMMENFASSUNG")
    print("=" * 60)
    print(f"Durchschnittliche Scharfschützen: {np.mean(results['scharfschuetzen']):.2f}")
    print(f"Maximum Scharfschützen: {np.max(results['scharfschuetzen'])}")
    print(f"Durchschnittlicher Reward: {np.mean(results['rewards']):.2f}")

    return results


# =============================================================================
# EXPORT FÜR ECHTES SPIEL
# =============================================================================

def export_strategy(model, save_path: str = "./strategy_export.json"):
    """
    Exportiert die beste Strategie für das echte Spiel

    Args:
        model: Trainiertes Modell
        save_path: Pfad für den Export
    """
    env = create_env()
    obs, _ = env.reset()
    done = False

    strategy = {
        "map": "EMS Wintersturm",
        "player": 1,
        "goal": "Maximale Scharfschützen in 30 Minuten",
        "actions": [],
        "building_positions": [],
    }

    while not done:
        action_mask = env.unwrapped.get_action_mask()
        action, _ = model.predict(obs, deterministic=True, action_masks=action_mask)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated

        # Nur relevante Aktionen speichern (keine "wait" Aktionen)
        if info.get("action_name") != "wait":
            strategy["actions"].append({
                "time_seconds": env.unwrapped.current_time,
                "time_formatted": f"{env.unwrapped.current_time // 60}:{env.unwrapped.current_time % 60:02d}",
                "action": info.get("action_name"),
            })

    strategy["building_positions"] = env.unwrapped.get_building_positions()
    strategy["final_scharfschuetzen"] = env.unwrapped.scharfschuetzen
    strategy["final_resources"] = dict(env.unwrapped.resources)
    strategy["final_buildings"] = {k: v for k, v in env.unwrapped.buildings.items() if v > 0}

    # Speichern
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(strategy, f, indent=2, ensure_ascii=False)

    print(f"Strategie exportiert: {save_path}")
    print(f"Scharfschützen erreicht: {strategy['final_scharfschuetzen']}")
    print(f"Anzahl Aktionen: {len(strategy['actions'])}")

    return strategy


# =============================================================================
# HAUPTPROGRAMM
# =============================================================================

if __name__ == "__main__":
    # Pfad für Modelle
    SAVE_PATH = "./siedler_training"

    # Erstelle Ordner falls nicht vorhanden
    os.makedirs(SAVE_PATH, exist_ok=True)

    # Training
    print("\n" + "=" * 60)
    print("PHASE 1: TRAINING")
    print("=" * 60 + "\n")

    model = train(
        config=TRAINING_CONFIG,
        save_path=SAVE_PATH
    )

    # Evaluation
    print("\n" + "=" * 60)
    print("PHASE 2: EVALUATION")
    print("=" * 60 + "\n")

    results = evaluate(model, n_episodes=5, render=True)

    # Export
    print("\n" + "=" * 60)
    print("PHASE 3: STRATEGIE EXPORT")
    print("=" * 60 + "\n")

    strategy = export_strategy(model, save_path=f"{SAVE_PATH}/strategy.json")

    print("\n" + "=" * 60)
    print("TRAINING ABGESCHLOSSEN!")
    print("=" * 60)
    print(f"\nModell gespeichert in: {SAVE_PATH}")
    print(f"Strategie exportiert in: {SAVE_PATH}/strategy.json")
    print("\nNächste Schritte:")
    print("1. Modell herunterladen")
    print("2. strategy.json für das echte Spiel nutzen")
    print("3. Game-Bridge ausführen")
