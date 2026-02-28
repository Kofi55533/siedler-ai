# -*- coding: utf-8 -*-
"""
Training-Test mit Ressourcen-basiertem Reward-System

Reward nur am Ende der Episode:
- Basiert auf kumulativ gesammeltem Schwefel und erhaltenen Talern
- Berechnet: Wie viele Scharfschuetzen koennte man damit kaufen?
- Scharfschuetzen_1 Kosten: 250 Taler + 70 Schwefel
"""

import os
import time
from datetime import datetime

import gymnasium as gym
from gymnasium import spaces
import numpy as np
import torch as th

from sb3_contrib import MaskablePPO
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv

from environment import SiedlerScharfschuetzenEnv


# =============================================================================
# SCHARFSCHUETZEN KOSTEN (aus environment.py)
# =============================================================================
SCHARFSCHUETZEN_TALER_COST = 250
SCHARFSCHUETZEN_SCHWEFEL_COST = 70


# =============================================================================
# CUSTOM ENVIRONMENT MIT RESSOURCEN-REWARD
# =============================================================================
class ResourceRewardEnv(SiedlerScharfschuetzenEnv):
    """
    Environment mit Reward nur am Ende basierend auf gesammelten Ressourcen.

    Reward = Potentielle Scharfschuetzen die man mit den Ressourcen kaufen koennte
           = min(kumulativ_taler / 250, kumulativ_schwefel / 70)

    Trackt alle Ressourcen die jemals ins Lager gekommen sind (nicht nur Zuwachs).
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Tracking fuer kumulative Ressourcen (TOTAL gesammelt/produziert)
        self.total_taler_earned = 0.0
        self.total_schwefel_earned = 0.0
        # Start-Werte speichern
        self.start_taler = 0.0
        self.start_schwefel = 0.0
        # Peak-Werte fuer besseres Tracking
        self.peak_taler = 0.0
        self.peak_schwefel = 0.0

    def reset(self, **kwargs):
        obs, info = super().reset(**kwargs)
        # Start-Werte merken
        self.start_taler = float(self.resources.get("Taler", 0))
        self.start_schwefel = float(self.resources.get("Schwefel", 0))
        # Peaks initialisieren
        self.peak_taler = self.start_taler
        self.peak_schwefel = self.start_schwefel
        # Total reset
        self.total_taler_earned = 0.0
        self.total_schwefel_earned = 0.0
        return obs, info

    def step(self, action):
        obs, _, terminated, truncated, info = super().step(action)

        # Aktuelle Ressourcen
        current_taler = float(self.resources.get("Taler", 0))
        current_schwefel = float(self.resources.get("Schwefel", 0))

        # Track wenn neue Peaks erreicht werden (= neue Ressourcen gesammelt)
        if current_taler > self.peak_taler:
            self.total_taler_earned += (current_taler - self.peak_taler)
            self.peak_taler = current_taler
        if current_schwefel > self.peak_schwefel:
            self.total_schwefel_earned += (current_schwefel - self.peak_schwefel)
            self.peak_schwefel = current_schwefel

        # Expose fuer Callback
        self.cumulative_taler = self.total_taler_earned
        self.cumulative_schwefel = self.total_schwefel_earned

        # Reward NUR am Ende der Episode
        reward = 0.0
        if terminated or truncated:
            # Potentielle Scharfschuetzen basierend auf TOTAL gesammelten Ressourcen
            # Inkludiert auch Start-Ressourcen (die man "hat")
            total_taler = self.start_taler + self.total_taler_earned
            total_schwefel = self.start_schwefel + self.total_schwefel_earned

            potential_by_taler = total_taler / SCHARFSCHUETZEN_TALER_COST
            potential_by_schwefel = total_schwefel / SCHARFSCHUETZEN_SCHWEFEL_COST

            # Minimum der beiden (limitierender Faktor)
            reward = min(potential_by_taler, potential_by_schwefel)

            # Info erweitern
            info["start_taler"] = self.start_taler
            info["start_schwefel"] = self.start_schwefel
            info["earned_taler"] = self.total_taler_earned
            info["earned_schwefel"] = self.total_schwefel_earned
            info["total_taler"] = total_taler
            info["total_schwefel"] = total_schwefel
            info["potential_scharfschuetzen"] = reward

        return obs, reward, terminated, truncated, info


# =============================================================================
# CALLBACKS
# =============================================================================
class ResourceTrackingCallback(BaseCallback):
    """Callback zum Tracken des Ressourcen-Fortschritts."""

    def __init__(self, check_freq: int = 1000):
        super().__init__()
        self.check_freq = check_freq
        self.best_potential = 0.0
        self.episode_count = 0
        self.episode_potentials = []

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
            earned_taler = self._get_env_attr("total_taler_earned", 0)
            earned_schwefel = self._get_env_attr("total_schwefel_earned", 0)
            start_taler = self._get_env_attr("start_taler", 500)
            start_schwefel = self._get_env_attr("start_schwefel", 50)
            current_time = self._get_env_attr("current_time", 0)

            total_taler = start_taler + earned_taler
            total_schwefel = start_schwefel + earned_schwefel

            potential = min(
                total_taler / SCHARFSCHUETZEN_TALER_COST,
                total_schwefel / SCHARFSCHUETZEN_SCHWEFEL_COST
            )

            print(f"Step {self.n_calls}: Zeit={current_time:.0f}s, "
                  f"Taler={total_taler:.0f} (+{earned_taler:.0f}), "
                  f"Schwefel={total_schwefel:.0f} (+{earned_schwefel:.0f}), "
                  f"Potential={potential:.2f} (Best: {self.best_potential:.2f})")
        return True

    def _on_rollout_end(self):
        # Am Ende eines Rollouts prüfen wir die Ergebnisse
        cum_taler = self._get_env_attr("cumulative_taler", 0)
        cum_schwefel = self._get_env_attr("cumulative_schwefel", 0)

        potential = min(
            cum_taler / SCHARFSCHUETZEN_TALER_COST if cum_taler > 0 else 0,
            cum_schwefel / SCHARFSCHUETZEN_SCHWEFEL_COST if cum_schwefel > 0 else 0
        )

        if potential > self.best_potential:
            self.best_potential = potential
            print(f"  >>> NEUER REKORD: {potential:.2f} potentielle Scharfschuetzen!")


# =============================================================================
# ENVIRONMENT FACTORY
# =============================================================================
def make_resource_env(rank: int, seed: int = 0, use_spatial_obs: bool = False, spatial_size: int = 64):
    def _init():
        env = ResourceRewardEnv(
            player_id=1,
            use_spatial_obs=use_spatial_obs,
            spatial_size=spatial_size,
        )
        env.reset(seed=seed + rank)
        return env
    return _init


def create_resource_env(n_envs: int = 1, use_spatial_obs: bool = False, spatial_size: int = 64):
    """Erstellt vektorisierte Resource-Reward Environments."""
    if n_envs > 1:
        return SubprocVecEnv([
            make_resource_env(i, use_spatial_obs=use_spatial_obs, spatial_size=spatial_size)
            for i in range(n_envs)
        ])
    return DummyVecEnv([make_resource_env(0, use_spatial_obs=use_spatial_obs, spatial_size=spatial_size)])


# =============================================================================
# TRAINING TEST
# =============================================================================
def test_training(timesteps: int = 10_000, n_envs: int = 1, use_spatial_obs: bool = False):
    """
    Testet das Training mit dem Ressourcen-Reward-System.

    Args:
        timesteps: Anzahl der Trainings-Steps
        n_envs: Anzahl paralleler Environments
        use_spatial_obs: Ob räumliche Observations genutzt werden

    Returns:
        dict mit Ergebnissen
    """
    print("=" * 70)
    print("TRAINING TEST - RESSOURCEN-BASIERTER REWARD")
    print("=" * 70)
    print(f"Timesteps: {timesteps:,}")
    print(f"Environments: {n_envs}")
    print(f"Spatial Obs: {use_spatial_obs}")
    print(f"Reward: min(Taler/{SCHARFSCHUETZEN_TALER_COST}, Schwefel/{SCHARFSCHUETZEN_SCHWEFEL_COST})")
    print("=" * 70)

    # Environment erstellen
    start_time = time.time()
    env = create_resource_env(n_envs=n_envs, use_spatial_obs=use_spatial_obs)
    env_creation_time = time.time() - start_time
    print(f"\nEnvironment erstellt in {env_creation_time:.2f}s")

    print(f"Action Space: {env.action_space.n}")
    if isinstance(env.observation_space, gym.spaces.Dict):
        print(f"Observation Space: Dict (vector + spatial)")
    else:
        print(f"Observation Space: {env.observation_space.shape}")

    device = "cuda" if th.cuda.is_available() else "cpu"
    print(f"Device: {device}")

    # Modell erstellen
    try:
        from multihead_policy import MultiHeadMaskablePolicy, SpatialVectorExtractor
        head_sizes = env.env_method("get_action_head_sizes")[0]
        phase_dim = env.get_attr("phase_dim")[0]

        policy_kwargs = {
            "net_arch": [512, 256, 256],
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
            n_steps=512,
            batch_size=64,
            n_epochs=5,
            gamma=0.99,
            ent_coef=0.02,
            policy_kwargs=policy_kwargs,
            device=device,
            verbose=0,
        )
        print("MultiHeadMaskablePolicy verwendet")
    except ImportError:
        model = MaskablePPO(
            "MlpPolicy",
            env,
            learning_rate=0.0003,
            n_steps=512,
            batch_size=64,
            n_epochs=5,
            gamma=0.99,
            ent_coef=0.02,
            policy_kwargs={"net_arch": [512, 256, 256]},
            device=device,
            verbose=0,
        )
        print("Standard MlpPolicy verwendet")

    # Training
    print("\n" + "-" * 70)
    print("TRAINING STARTET...")
    print("-" * 70)

    callback = ResourceTrackingCallback(check_freq=2000)

    train_start = time.time()
    model.learn(
        total_timesteps=timesteps,
        callback=callback,
        progress_bar=True,
    )
    train_time = time.time() - train_start

    print("-" * 70)
    print(f"Training abgeschlossen in {train_time:.2f}s")
    print(f"Steps/Sekunde: {timesteps / train_time:.1f}")
    print(f"Beste potentielle Scharfschuetzen: {callback.best_potential:.2f}")

    # Evaluation
    print("\n" + "=" * 70)
    print("EVALUATION (3 Episoden)")
    print("=" * 70)

    eval_env = ResourceRewardEnv(player_id=1, use_spatial_obs=use_spatial_obs)
    eval_results = []

    for ep in range(3):
        obs, _ = eval_env.reset()
        done = False
        total_reward = 0
        steps = 0

        while not done:
            action_mask = eval_env.get_action_mask()
            action, _ = model.predict(obs, deterministic=True, action_masks=action_mask)
            # Convert numpy array to int if needed
            if hasattr(action, 'item'):
                action = action.item()
            elif isinstance(action, np.ndarray):
                action = int(action.flatten()[0])
            obs, reward, terminated, truncated, info = eval_env.step(action)
            total_reward += reward
            done = terminated or truncated
            steps += 1

        total_taler = eval_env.start_taler + eval_env.total_taler_earned
        total_schwefel = eval_env.start_schwefel + eval_env.total_schwefel_earned

        result = {
            "episode": ep + 1,
            "steps": steps,
            "time": eval_env.current_time,
            "reward": total_reward,
            "start_taler": eval_env.start_taler,
            "start_schwefel": eval_env.start_schwefel,
            "earned_taler": eval_env.total_taler_earned,
            "earned_schwefel": eval_env.total_schwefel_earned,
            "total_taler": total_taler,
            "total_schwefel": total_schwefel,
            "potential_scharfschuetzen": min(
                total_taler / SCHARFSCHUETZEN_TALER_COST,
                total_schwefel / SCHARFSCHUETZEN_SCHWEFEL_COST
            ),
            "actual_scharfschuetzen": eval_env.scharfschuetzen,
        }
        eval_results.append(result)

        print(f"\nEpisode {ep + 1}:")
        print(f"  Zeit: {result['time']:.0f}s / {eval_env.max_time}s")
        print(f"  Start-Taler: {result['start_taler']:.0f}, verdient: +{result['earned_taler']:.0f}")
        print(f"  Start-Schwefel: {result['start_schwefel']:.0f}, verdient: +{result['earned_schwefel']:.0f}")
        print(f"  Total Taler: {result['total_taler']:.0f}")
        print(f"  Total Schwefel: {result['total_schwefel']:.0f}")
        print(f"  Potentielle Scharfschuetzen: {result['potential_scharfschuetzen']:.2f}")
        print(f"  Tatsaechliche Scharfschuetzen: {result['actual_scharfschuetzen']}")
        print(f"  Reward: {result['reward']:.2f}")

    # Zusammenfassung
    print("\n" + "=" * 70)
    print("ZUSAMMENFASSUNG")
    print("=" * 70)

    avg_potential = np.mean([r["potential_scharfschuetzen"] for r in eval_results])
    avg_taler = np.mean([r["total_taler"] for r in eval_results])
    avg_schwefel = np.mean([r["total_schwefel"] for r in eval_results])
    avg_earned_taler = np.mean([r["earned_taler"] for r in eval_results])
    avg_earned_schwefel = np.mean([r["earned_schwefel"] for r in eval_results])

    summary = {
        "timesteps": timesteps,
        "n_envs": n_envs,
        "train_time_seconds": train_time,
        "steps_per_second": timesteps / train_time,
        "best_potential_during_training": callback.best_potential,
        "avg_potential_eval": avg_potential,
        "avg_cumulative_taler": avg_taler,
        "avg_cumulative_schwefel": avg_schwefel,
        "device": device,
    }

    print(f"Training Zeit: {train_time:.2f}s")
    print(f"Steps/Sekunde: {summary['steps_per_second']:.1f}")
    print(f"Durchschnittlich Total Taler: {avg_taler:.0f} (verdient: +{avg_earned_taler:.0f})")
    print(f"Durchschnittlich Total Schwefel: {avg_schwefel:.0f} (verdient: +{avg_earned_schwefel:.0f})")
    print(f"Durchschnittliche potentielle Scharfschuetzen: {avg_potential:.2f}")

    return summary, model


# =============================================================================
# PERFORMANCE BENCHMARK
# =============================================================================
def benchmark_performance():
    """Benchmark verschiedener Konfigurationen."""
    print("\n" + "=" * 70)
    print("PERFORMANCE BENCHMARK")
    print("=" * 70)

    results = []

    # Test 1: Single Env, ohne Spatial
    print("\n>>> Test 1: 1 Env, ohne Spatial Obs")
    summary1, _ = test_training(timesteps=5_000, n_envs=1, use_spatial_obs=False)
    results.append(("1 Env, Vector", summary1))

    # Test 2: Multi Env (falls verfügbar)
    n_cpus = os.cpu_count() or 1
    if n_cpus >= 4:
        print("\n>>> Test 2: 4 Envs, ohne Spatial Obs")
        summary2, _ = test_training(timesteps=5_000, n_envs=4, use_spatial_obs=False)
        results.append(("4 Envs, Vector", summary2))

    # Ergebnis-Vergleich
    print("\n" + "=" * 70)
    print("BENCHMARK ERGEBNISSE")
    print("=" * 70)
    print(f"{'Konfiguration':<25} {'Steps/s':>10} {'Potential':>12}")
    print("-" * 50)
    for name, summary in results:
        print(f"{name:<25} {summary['steps_per_second']:>10.1f} {summary['avg_potential_eval']:>12.2f}")

    return results


# =============================================================================
# COLAB SETUP
# =============================================================================
def setup_colab():
    """Setup fuer Google Colab mit GPU."""
    import subprocess
    import sys

    print("Installing dependencies for Colab...")
    packages = ["gymnasium", "stable-baselines3", "sb3-contrib", "tensorboard"]
    for pkg in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])
    print("Done!")


def is_colab():
    """Check if running in Google Colab."""
    try:
        import google.colab
        return True
    except ImportError:
        return False


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    import sys

    # Auto-detect Colab
    IN_COLAB = is_colab()

    if IN_COLAB:
        print("=" * 70)
        print("GOOGLE COLAB DETECTED - GPU TRAINING")
        print("=" * 70)
        setup_colab()

        # Colab-optimierte Einstellungen
        n_envs = 8  # Mehr parallele Envs
        timesteps = 100_000  # Mehr Steps

        import torch as th
        if th.cuda.is_available():
            print(f"GPU: {th.cuda.get_device_name(0)}")
            print(f"CUDA Version: {th.version.cuda}")
        else:
            print("WARNING: Keine GPU gefunden! Runtime -> Change runtime type -> GPU")

        summary, model = test_training(timesteps=timesteps, n_envs=n_envs, use_spatial_obs=False)

        # Modell speichern
        model.save("siedler_resource_reward_model")
        print("\nModell gespeichert: siedler_resource_reward_model.zip")

    elif len(sys.argv) > 1 and sys.argv[1] == "--benchmark":
        benchmark_performance()

    elif len(sys.argv) > 1 and sys.argv[1] == "--gpu":
        # Lokaler GPU-Test
        import torch as th
        if th.cuda.is_available():
            print(f"GPU: {th.cuda.get_device_name(0)}")
            n_envs = min(8, (os.cpu_count() or 4))
            summary, model = test_training(timesteps=50_000, n_envs=n_envs, use_spatial_obs=False)
        else:
            print("Keine GPU verfuegbar, nutze CPU")
            summary, model = test_training(timesteps=10_000, n_envs=1, use_spatial_obs=False)

    else:
        # Standard-Test: 10k Steps lokal
        print("\n[INFO] Starte Training-Test mit 10.000 Steps (lokal/CPU)")
        print("[INFO] Optionen:")
        print("  --benchmark : Performance-Vergleich")
        print("  --gpu       : Lokaler GPU-Test (50k Steps)")
        print("  In Colab    : Automatisch GPU + 100k Steps\n")

        summary, model = test_training(timesteps=10_000, n_envs=1, use_spatial_obs=False)

        print("\n" + "=" * 70)
        print("TEST ERFOLGREICH ABGESCHLOSSEN")
        print("=" * 70)
