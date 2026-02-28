# -*- coding: utf-8 -*-
"""
Siedler 5 - Scharfschuetzen Training Script fuer Google Colab.

Dieses Script kann in Google Colab ausgefuehrt werden.
Die Umgebung braucht mehrere Projektdateien, nicht nur 4 Dateien.

Verwendung in Colab:
1. Lade mindestens diese Dateien hoch:
   - colab_training.py
   - environment.py
   - multihead_policy.py
   - map_config_wintersturm.py
   - wood_zones_config.py
   - production_system.py
   - worker_simulation.py
   - pathfinding.py
   - player1_walkable.npy (oder player1_walkable_515.npy)
   - player1_resources.json
2. Optional fuer maximale Engine-Naehe:
   - config/worker_truth_model.json
3. Fuehre dieses Script aus.
"""

# =============================================================================
# INSTALLATION (nur in Colab nÃƒÂ¶tig)
# =============================================================================

def install_dependencies():
    """Installiert benÃƒÂ¶tigte Pakete in Colab"""
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

    print("Alle AbhÃƒÂ¤ngigkeiten installiert!")


def install_dependencies_robust():
    """Install dependencies from requirements-colab.txt with fallback."""
    import subprocess
    import sys
    import time
    from pathlib import Path

    req_file = Path(__file__).resolve().parent / "requirements-colab.txt"
    if req_file.exists():
        cmd = [sys.executable, "-m", "pip", "install", "-q", "-r", str(req_file)]
        for attempt in range(1, 4):
            try:
                subprocess.check_call(cmd)
                print(f"Alle Abhaengigkeiten installiert aus {req_file.name}.")
                return
            except subprocess.CalledProcessError:
                if attempt == 3:
                    raise
                print(f"pip install fehlgeschlagen (Versuch {attempt}/3), retry...")
                time.sleep(2)

    packages = [
        "gymnasium",
        "stable-baselines3",
        "sb3-contrib",
        "tensorboard",
    ]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", *packages])
    print("Alle Abhaengigkeiten installiert (Fallback-Paketliste).")


# =============================================================================
# IMPORTS
# =============================================================================

import os
import json
import inspect
import re
import numpy as np
import time
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple
import torch as th

try:
    import gymnasium as gym
    from sb3_contrib import MaskablePPO
    from sb3_contrib.common.maskable.callbacks import MaskableEvalCallback
    from stable_baselines3 import PPO
    from stable_baselines3.common.callbacks import CheckpointCallback, BaseCallback
    from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
except ImportError:
    print("Installiere AbhÃƒÂ¤ngigkeiten...")
    install_dependencies_robust()
    import gymnasium as gym
    from sb3_contrib import MaskablePPO
    from sb3_contrib.common.maskable.callbacks import MaskableEvalCallback
    from stable_baselines3 import PPO
    from stable_baselines3.common.callbacks import CheckpointCallback, BaseCallback
    from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv

# Importiere unser Environment
from environment import SiedlerScharfschuetzenEnv
from multihead_policy import MultiHeadMaskablePolicy, SpatialVectorExtractor
from training_profiles import build_training_config, get_train_profile


# =============================================================================
# CALLBACKS
# =============================================================================

th.backends.cudnn.benchmark = True
try:
    th.set_float32_matmul_precision("high")
except Exception:
    pass
th.backends.cuda.matmul.allow_tf32 = True


def _env_truthy(value: Optional[str]) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _resolve_sim_mode() -> str:
    mode = str(os.environ.get("SIEDLER_SIM_MODE", "")).strip().lower()
    if mode in {"fast_train", "full_sim"}:
        return mode
    return "fast_train" if _env_truthy(os.environ.get("SIEDLER_FAST_TRAIN", "0")) else "full_sim"


def _get_use_spatial_obs() -> bool:
    raw = os.environ.get("SIEDLER_USE_SPATIAL")
    if raw is not None:
        return _env_truthy(raw)
    return _resolve_sim_mode() != "fast_train"


def _tensorboard_enabled() -> bool:
    return _env_truthy(os.environ.get("SIEDLER_TENSORBOARD", "1"))


def _progress_bar_enabled() -> bool:
    return _env_truthy(os.environ.get("SIEDLER_PROGRESS_BAR", "1"))


def _prefer_speed_mode() -> bool:
    """
    Turbo-FPS Modus:
    - explizit ueber SIEDLER_TURBO_FPS steuerbar
    - sonst in fast_train standardmaessig aktiv
    """
    raw = os.environ.get("SIEDLER_TURBO_FPS")
    if raw is not None:
        return _env_truthy(raw)
    return _resolve_sim_mode() == "fast_train"


def _select_net_arch(obs_dim: int):
    if _prefer_speed_mode():
        if obs_dim >= 400:
            return [768, 384, 256]
        if obs_dim >= 250:
            return [512, 256, 256]
        return [384, 192, 192]
    if obs_dim >= 400:
        return [1024, 512, 512]
    if obs_dim >= 250:
        return [768, 512, 256]
    return [512, 256, 256]


def _detect_runtime_info() -> Dict[str, object]:
    is_colab = bool(
        os.environ.get("COLAB_RELEASE_TAG")
        or os.environ.get("COLAB_GPU")
        or os.environ.get("GCE_METADATA_TIMEOUT")
    )
    tpu_addr = os.environ.get("COLAB_TPU_ADDR") or os.environ.get("TPU_NAME")
    has_cuda = th.cuda.is_available()
    gpu_name = None
    gpu_mem_gb = 0.0
    if has_cuda:
        gpu_name = th.cuda.get_device_name(0)
        gpu_mem_gb = float(th.cuda.get_device_properties(0).total_memory) / (1024 ** 3)
    cpu_count = os.cpu_count() or 1
    return {
        "is_colab": is_colab,
        "has_tpu": bool(tpu_addr),
        "tpu_addr": tpu_addr,
        "has_cuda": has_cuda,
        "gpu_name": gpu_name,
        "gpu_mem_gb": gpu_mem_gb,
        "cpu_count": cpu_count,
    }


def _try_mount_google_drive() -> Optional[Path]:
    """
    Versucht in Colab Google Drive einzubinden.

    Rueckgabe:
        Path auf /content/drive/MyDrive bei Erfolg, sonst None.
    """
    mydrive = Path("/content/drive/MyDrive")
    if mydrive.exists():
        return mydrive

    runtime = _detect_runtime_info()
    if not runtime.get("is_colab"):
        return None

    auto_mount = str(os.environ.get("SIEDLER_AUTO_MOUNT_DRIVE", "1")).strip().lower()
    if auto_mount not in {"1", "true", "yes", "on"}:
        return None

    try:
        from google.colab import drive as colab_drive  # type: ignore

        print("Google Drive wird gemountet...")
        colab_drive.mount("/content/drive", force_remount=False)
    except Exception as exc:
        print(f"Warnung: Google Drive konnte nicht gemountet werden ({exc})")
        return None

    return mydrive if mydrive.exists() else None


def _resolve_training_save_path(requested_path: str = "./siedler_training") -> str:
    """
    Ermittelt den finalen Save-Pfad.

    Prioritaet:
      1) SIEDLER_SAVE_DIR (falls gesetzt)
      2) In Colab mit gemountetem Drive: /content/drive/MyDrive/<ordnername>
      3) Sonst lokaler Pfad (aktuelles Arbeitsverzeichnis)
    """
    env_save_dir = os.environ.get("SIEDLER_SAVE_DIR")
    if env_save_dir:
        requested_path = env_save_dir

    path = Path(requested_path).expanduser()
    runtime = _detect_runtime_info()
    drive_root = _try_mount_google_drive()
    require_drive_default = "1" if runtime.get("is_colab") else "0"
    require_drive = str(
        os.environ.get("SIEDLER_REQUIRE_DRIVE", require_drive_default)
    ).strip().lower() in {"1", "true", "yes", "on"}

    if runtime.get("is_colab") and require_drive and drive_root is None:
        raise RuntimeError(
            "Google Drive ist nicht verfuegbar. "
            "Bitte in Colab Drive mounten oder SIEDLER_REQUIRE_DRIVE=0 setzen."
        )

    if drive_root is not None:
        if path.is_absolute():
            final_path = path
        else:
            folder_name = path.name if path.name not in {"", "."} else "siedler_training"
            final_path = drive_root / folder_name
        final_path.mkdir(parents=True, exist_ok=True)
        return str(final_path)

    if path.is_absolute():
        final_path = path
    elif runtime.get("is_colab"):
        final_path = Path("/content") / path
    else:
        final_path = Path.cwd() / path
    final_path.mkdir(parents=True, exist_ok=True)
    return str(final_path)


def _extract_steps_from_checkpoint_path(path: Path) -> int:
    """
    Extrahiert Timesteps aus Dateinamen wie:
      siedler_checkpoint_250000_steps.zip
    """
    match = re.search(r"_(\d+)_steps$", path.stem)
    if not match:
        return 0
    try:
        return int(match.group(1))
    except ValueError:
        return 0


def _find_latest_checkpoint(save_path: str) -> Tuple[Optional[str], int]:
    """
    Findet den neuesten Checkpoint im Save-Ordner.
    Rueckgabe: (pfad_oder_none, timesteps_aus_dateiname)
    """
    root = Path(save_path)
    if not root.exists():
        return None, 0

    candidates = []
    for ckpt in root.glob("siedler_checkpoint_*_steps.zip"):
        steps = _extract_steps_from_checkpoint_path(ckpt)
        try:
            mtime = ckpt.stat().st_mtime
        except OSError:
            mtime = 0.0
        candidates.append((steps, mtime, ckpt))

    if not candidates:
        return None, 0

    best_steps, _, best_path = max(candidates, key=lambda item: (item[0], item[1]))
    return str(best_path), int(best_steps)


def _infer_colab_preset(runtime: Dict[str, object]) -> Dict[str, object]:
    gpu_name = str(runtime.get("gpu_name") or "").upper()
    cpu_count = int(runtime.get("cpu_count") or 1)
    cpu_cap_envs = max(1, cpu_count - 1)

    if "H100" in gpu_name:
        preset = {
            "name": "h100",
            "n_envs": 10,
            "spatial_size": 192,
            "n_steps": 4096,
            "batch_size": 1024,
            "n_epochs": 6,
            "learning_rate": 0.0002,
            "ent_coef": 0.012,
        }
    elif "A100" in gpu_name:
        preset = {
            "name": "a100",
            "n_envs": 8,
            "spatial_size": 160,
            "n_steps": 3072,
            "batch_size": 512,
            "n_epochs": 6,
            "learning_rate": 0.00025,
            "ent_coef": 0.015,
        }
    elif "L4" in gpu_name or "V100" in gpu_name:
        preset = {
            "name": "l4_v100",
            "n_envs": 6,
            "spatial_size": 128,
            "n_steps": 3072,
            "batch_size": 384,
            "n_epochs": 6,
            "learning_rate": 0.00025,
            "ent_coef": 0.015,
        }
    elif "T4" in gpu_name or "P100" in gpu_name:
        preset = {
            "name": "t4_p100",
            "n_envs": 4,
            "spatial_size": 128,
            "n_steps": 2048,
            "batch_size": 256,
            "n_epochs": 6,
            "learning_rate": 0.00025,
            "ent_coef": 0.02,
        }
    elif bool(runtime.get("has_cuda")):
        preset = {
            "name": "generic_cuda",
            "n_envs": 4,
            "spatial_size": 128,
            "n_steps": 2048,
            "batch_size": 256,
            "n_epochs": 6,
            "learning_rate": 0.00025,
            "ent_coef": 0.02,
        }
    else:
        preset = {
            "name": "cpu_only",
            "n_envs": 2,
            "spatial_size": 96,
            "n_steps": 1024,
            "batch_size": 128,
            "n_epochs": 4,
            "learning_rate": 0.0003,
            "ent_coef": 0.02,
        }

    preset["n_envs"] = int(max(1, min(int(preset["n_envs"]), cpu_cap_envs)))

    if _prefer_speed_mode() and preset["name"] in {"l4_v100", "t4_p100", "generic_cuda"}:
        # Reduziert PPO-Update-Overhead deutlich fuer hoehere effective FPS.
        preset["n_steps"] = 2048
        preset["batch_size"] = 1024
        preset["n_epochs"] = 4
        preset["learning_rate"] = 0.0003

    return preset


def _auto_tune_for_colab(
    config: Dict[str, object],
    explicit_config: Optional[Dict[str, object]] = None,
) -> Dict[str, object]:
    """
    Auto-Tuning fuer Colab Pro/Pro+.

    - TPU wird nicht empfohlen (SB3/MaskablePPO ist auf CUDA ausgelegt).
    - GPU-Preset steuert n_envs/spatial_size und zentrale PPO-Parameter.
    - Explizit gesetzte Werte in explicit_config bleiben unberuehrt.
    """
    disable_auto = str(os.environ.get("SIEDLER_DISABLE_AUTO_TUNE", "")).strip().lower()
    if disable_auto in {"1", "true", "yes", "on"}:
        return {"enabled": False, "reason": "disabled_by_env"}

    runtime = _detect_runtime_info()
    preset = _infer_colab_preset(runtime)
    explicit_keys = set((explicit_config or {}).keys())

    # Setze Runtime-Defaults nur wenn User/Notebook nicht bereits gesetzt hat.
    if not os.environ.get("SIEDLER_NUM_ENVS"):
        os.environ["SIEDLER_NUM_ENVS"] = str(preset["n_envs"])
    if not os.environ.get("SIEDLER_SPATIAL_SIZE"):
        os.environ["SIEDLER_SPATIAL_SIZE"] = str(preset["spatial_size"])

    for key in ("n_steps", "batch_size", "n_epochs", "learning_rate", "ent_coef"):
        if key in explicit_keys:
            continue
        config[key] = preset[key]

    # Sicherheitscheck: Batch-Size darf Rollout-Batch nicht uebersteigen.
    n_envs = int(os.environ.get("SIEDLER_NUM_ENVS", preset["n_envs"]))
    n_steps = int(config.get("n_steps", preset["n_steps"]))
    rollout = max(1, n_envs * n_steps)
    batch_size = int(config.get("batch_size", preset["batch_size"]))
    if batch_size > rollout:
        # Naechste sinnvolle Potenz-von-2 unterhalb des Rollouts.
        new_batch = 1
        while new_batch * 2 <= rollout:
            new_batch *= 2
        config["batch_size"] = max(32, new_batch)

    return {
        "enabled": True,
        "runtime": runtime,
        "preset": preset,
        "effective_n_envs": int(os.environ.get("SIEDLER_NUM_ENVS", preset["n_envs"])),
        "effective_spatial_size": int(os.environ.get("SIEDLER_SPATIAL_SIZE", preset["spatial_size"])),
    }


def _select_extractor_dims() -> Dict[str, int]:
    if not th.cuda.is_available():
        return {"cnn_out_dim": 128, "vector_out_dim": 256}
    mem_gb = float(th.cuda.get_device_properties(0).total_memory) / (1024 ** 3)
    if mem_gb >= 60:
        return {"cnn_out_dim": 224, "vector_out_dim": 384}
    if mem_gb >= 30:
        return {"cnn_out_dim": 192, "vector_out_dim": 320}
    if mem_gb >= 20:
        return {"cnn_out_dim": 160, "vector_out_dim": 288}
    return {"cnn_out_dim": 128, "vector_out_dim": 256}


def print_runtime_recommendation():
    runtime = _detect_runtime_info()
    preset = _infer_colab_preset(runtime)
    drive_available = Path("/content/drive/MyDrive").exists()

    print("=" * 60)
    print("COLAB RUNTIME EMPFEHLUNG")
    print("=" * 60)
    print("Hardware-Accelerator: GPU (nicht TPU)")
    if runtime.get("has_cuda"):
        print(f"Erkannte GPU: {runtime.get('gpu_name')} ({float(runtime.get('gpu_mem_gb') or 0.0):.1f} GB)")
    else:
        print("Erkannte GPU: keine (CPU-Only Runtime)")
    if runtime.get("has_tpu"):
        print("TPU erkannt, aber SB3/MaskablePPO in diesem Projekt ist fuer CUDA optimiert.")
    print(f"Empfohlenes Preset: {preset.get('name')}")
    print(f"Empfohlenes n_envs: {preset.get('n_envs')}")
    print(f"Empfohlene Spatial-Size: {preset.get('spatial_size')}")
    if runtime.get("is_colab"):
        print(f"Google Drive gemountet: {'ja' if drive_available else 'nein'}")
        if not drive_available:
            print("Hinweis: Drive wird beim Trainingsstart automatisch gemountet.")
    print("=" * 60)

class ScharfschuetzenCallback(BaseCallback):
    """Custom Callback zum Tracken des Trainingsfortschritts"""

    def __init__(
        self,
        check_freq: int = 1000,
        status_every_sec: int = 5,
        compact_status: bool = True,
        status_bar_width: int = 24,
        verbose: int = 1,
    ):
        super().__init__(verbose)
        self.check_freq = check_freq
        self.status_every_sec = max(1, int(status_every_sec))
        self._requested_compact_status = bool(compact_status)
        self._tty_capable = bool(hasattr(sys.stdout, "isatty") and sys.stdout.isatty())
        # In Colab/Subprocess ist carriage-return oft unzuverlaessig -> automatisch Zeilenmodus.
        self.compact_status = bool(self._requested_compact_status and self._tty_capable)
        self.status_bar_width = max(10, int(status_bar_width))
        self.best_scharfschuetzen = 0
        self.episode_rewards = []
        self.episode_scharfschuetzen = []
        self._train_start_time = None
        self._last_status_time = None
        self._last_status_steps = 0
        self._last_status_line_len = 0

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

    def _on_training_start(self) -> None:
        now = time.perf_counter()
        self._train_start_time = now
        self._last_status_time = now
        self._last_status_steps = int(self.num_timesteps)
        if self.verbose > 0 and self._requested_compact_status and not self._tty_capable:
            print("Status-Ausgabe: Zeilenmodus (Colab/Subprocess-kompatibel).")

    @staticmethod
    def _format_seconds(total_seconds: float) -> str:
        sec = max(0, int(total_seconds))
        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def _render_status_line(
        self,
        total_steps: int,
        target_steps: int,
        inst_fps: float,
        avg_fps: float,
        eta_sec: float,
        remaining_steps: int,
    ) -> str:
        bar_width = self.status_bar_width
        if target_steps > 0:
            pct_ratio = max(0.0, min(1.0, float(total_steps) / float(target_steps)))
            pct = 100.0 * pct_ratio
            filled = int(round(bar_width * pct_ratio))
            bar = "-" * filled + " " * max(0, bar_width - filled)
            progress = f"{total_steps:,}/{target_steps:,}"
        else:
            pct = 0.0
            bar = "-" * bar_width
            progress = f"{total_steps:,}"
        eta_text = self._format_seconds(eta_sec) if math.isfinite(eta_sec) else "--:--:--"
        return (
            "[TRAIN] "
            f"[{bar}] "
            f"{pct:5.1f}% | "
            f"fps={inst_fps:6.1f} | "
            f"avg={avg_fps:6.1f} | "
            f"left={remaining_steps:,} | "
            f"eta={eta_text} | "
            f"steps={progress}"
        )

    def _maybe_print_runtime_status(self) -> None:
        if self.verbose <= 0:
            return
        now = time.perf_counter()
        if self._last_status_time is None or self._train_start_time is None:
            self._on_training_start()
            return

        elapsed_since_last = now - self._last_status_time
        if elapsed_since_last < self.status_every_sec:
            return

        total_steps = int(self.num_timesteps)
        step_delta = max(0, total_steps - self._last_status_steps)
        inst_fps = step_delta / max(1e-6, elapsed_since_last)

        elapsed_total = max(1e-6, now - self._train_start_time)
        avg_fps = total_steps / elapsed_total

        target_steps = int(getattr(self.model, "_total_timesteps", 0) or 0)
        if target_steps > 0:
            remaining_steps = max(0, target_steps - total_steps)
            eta_sec = remaining_steps / max(1e-6, avg_fps)
        else:
            remaining_steps = 0
            eta_sec = float("inf")

        line = self._render_status_line(
            total_steps=total_steps,
            target_steps=target_steps,
            inst_fps=inst_fps,
            avg_fps=avg_fps,
            eta_sec=eta_sec,
            remaining_steps=remaining_steps,
        )

        if self.compact_status:
            clear_pad = " " * max(0, self._last_status_line_len - len(line))
            print(f"\r{line}{clear_pad}", end="", flush=True)
            self._last_status_line_len = len(line)
        else:
            print(line)

        self._last_status_time = now
        self._last_status_steps = total_steps

    def _on_step(self) -> bool:
        self._maybe_print_runtime_status()

        if self.n_calls % self.check_freq == 0:
            scharfschuetzen = self._get_env_attr("scharfschuetzen", 0)

            if scharfschuetzen > self.best_scharfschuetzen:
                self.best_scharfschuetzen = scharfschuetzen
                if self.verbose > 0:
                    print(f"Neuer Rekord: {scharfschuetzen} Scharfschuetzen!")

            if self.verbose > 0 and self.n_calls % (self.check_freq * 10) == 0:
                print(f"Step {self.n_calls}: Best Scharfschuetzen = {self.best_scharfschuetzen}")

        return True

    def _on_training_end(self) -> None:
        if self.compact_status and self.verbose > 0:
            print("")


# =============================================================================
# TRAINING KONFIGURATION
# =============================================================================

TRAINING_CONFIG = {
    # Timesteps - ERHÃƒâ€“HT fÃƒÂ¼r sparse rewards (nur ScharfschÃƒÂ¼tzen am Ende)
    "total_timesteps": 5_000_000,  # 5M Steps fÃƒÂ¼r sparse rewards

    # Modell-Hyperparameter
    "learning_rate": 0.0003,
    "n_steps": 2048,
    "batch_size": 64,
    "n_epochs": 10,
    "gamma": 0.995,  # HÃƒÂ¶her fÃƒÂ¼r langfristige Planung (30 Min Episode)
    "gae_lambda": 0.95,
    "clip_range": 0.2,
    "ent_coef": 0.02,  # Exploration fÃƒÂ¼r 188 Actions

    # Netzwerk
    "policy_kwargs": {
        "net_arch": [1024, 512, 512],
    },
    "auto_scale_arch": True,

    # Checkpoints
    "checkpoint_freq": 250_000,
    "eval_freq": 50_000,
}



def _validate_runtime_files():
    """Prueft, ob alle benoetigten Projektdateien verfuegbar sind."""
    root_dir = Path(__file__).resolve().parent
    data_dir = Path(os.environ.get("SIEDLER_DATA_DIR", str(root_dir)))

    required_python = [
        "environment.py",
        "multihead_policy.py",
        "map_config_wintersturm.py",
        "wood_zones_config.py",
        "production_system.py",
        "worker_simulation.py",
        "pathfinding.py",
    ]
    missing = [name for name in required_python if not (root_dir / name).exists()]

    walkable_candidates = [
        data_dir / "player1_walkable_515.npy",
        data_dir / "player1_walkable.npy",
        root_dir / "player1_walkable_515.npy",
        root_dir / "player1_walkable.npy",
    ]
    if not any(path.exists() for path in walkable_candidates):
        missing.append(
            "player1_walkable_515.npy oder player1_walkable.npy "
            f"(im Datenordner: {data_dir} oder Projektordner: {root_dir})"
        )

    resources_candidates = [
        data_dir / "player1_resources.json",
        root_dir / "player1_resources.json",
    ]
    if not any(path.exists() for path in resources_candidates):
        missing.append(
            "player1_resources.json "
            f"(im Datenordner: {data_dir} oder Projektordner: {root_dir})"
        )

    if missing:
        formatted = "\n".join(f"  - {item}" for item in missing)
        raise FileNotFoundError(
            "Fehlende Pflichtdateien fuer Training:\n"
            f"{formatted}\n\n"
            "Hinweis: Setze optional SIEDLER_DATA_DIR auf den Ordner mit den Kartendaten."
        )


# =============================================================================
# TRAINING FUNKTION
# =============================================================================

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


def _get_env_init_param_names() -> set:
    try:
        sig = inspect.signature(SiedlerScharfschuetzenEnv.__init__)
        return set(sig.parameters.keys())
    except Exception:
        return set()


def _create_env_instance(
    player_id: int = 1,
    use_spatial_obs: bool = True,
    spatial_size: int = 128,
    reward_profile: dict = None,
):
    """
    Erstellt Environment robust fuer alte/neue Environment-APIs.
    """
    params = _get_env_init_param_names()
    kwargs = {"player_id": player_id}
    if "use_spatial_obs" in params:
        kwargs["use_spatial_obs"] = use_spatial_obs
    if "spatial_size" in params:
        kwargs["spatial_size"] = spatial_size
    if "reward_profile" in params:
        kwargs["reward_profile"] = reward_profile
    return SiedlerScharfschuetzenEnv(**kwargs)


def _get_base_env(env):
    base = env
    if hasattr(base, "envs") and base.envs:
        base = base.envs[0]
    if hasattr(base, "unwrapped"):
        base = base.unwrapped
    return base


def _get_multihead_metadata(env):
    """
    Liefert (action_head_sizes, phase_dim) robust fuer Dummy/SubprocVecEnv.
    """
    if hasattr(env, "env_method") and hasattr(env, "get_attr"):
        try:
            head_sizes_list = env.env_method("get_action_head_sizes")
            phase_dim_list = env.get_attr("phase_dim")
            if head_sizes_list and phase_dim_list:
                head_sizes = head_sizes_list[0]
                phase_dim = int(phase_dim_list[0])
                if head_sizes is not None and phase_dim > 0:
                    return list(head_sizes), phase_dim
        except Exception:
            pass

    base = _get_base_env(env)
    if hasattr(base, "get_action_head_sizes") and hasattr(base, "phase_dim"):
        try:
            head_sizes = base.get_action_head_sizes()
            phase_dim = int(base.phase_dim)
            if head_sizes is not None and phase_dim > 0:
                return list(head_sizes), phase_dim
        except Exception:
            pass

    return None, None


def make_env(
    rank: int,
    seed: int = 0,
    use_spatial_obs: bool = True,
    spatial_size: int = 128,
    reward_profile: dict = None,
):
    def _init():
        env = _create_env_instance(
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


def probe_env_throughput(profile_name: str = None, probe_steps: int = 96):
    """
    Kurzer Stabilitaets-/Throughput-Test fuer die aktuelle n_envs-Einstellung.

    Wird ueber SIEDLER_PROBE_ENV_ONLY=1 im __main__ aktiviert.
    """
    custom_config = {}
    config, profile = build_training_config(
        TRAINING_CONFIG,
        custom_config=custom_config,
        profile_name=profile_name,
    )
    _auto_tune_for_colab(config, explicit_config=custom_config)
    _validate_runtime_files()

    reward_profile = profile["reward_profile"]
    spatial_size = _get_spatial_size()
    use_spatial_obs = _get_use_spatial_obs()
    env = create_env(
        use_spatial_obs=use_spatial_obs,
        spatial_size=spatial_size,
        reward_profile=reward_profile,
    )

    n_envs = int(getattr(env, "num_envs", 1))
    steps = max(8, int(probe_steps))
    total_env_steps = 0
    start = time.perf_counter()

    try:
        env.reset()
        for _ in range(steps):
            actions = np.asarray([env.action_space.sample() for _ in range(n_envs)])
            env.step(actions)
            total_env_steps += n_envs
    finally:
        env.close()

    elapsed = max(1e-6, time.perf_counter() - start)
    throughput_sps = float(total_env_steps) / elapsed

    print(
        f"ENV_PROBE_RESULT n_envs={n_envs} "
        f"throughput_sps={throughput_sps:.2f} spatial={spatial_size} "
        f"use_spatial={int(use_spatial_obs)}"
    )
    return {
        "n_envs": n_envs,
        "throughput_sps": throughput_sps,
        "spatial_size": spatial_size,
        "steps": steps,
    }


def _predict_with_optional_mask(model, obs, action_mask=None):
    """
    Kompatibel mit MaskablePPO und PPO.
    """
    try:
        if action_mask is not None:
            return model.predict(obs, deterministic=True, action_masks=action_mask)
    except TypeError:
        pass
    return model.predict(obs, deterministic=True)


def train(config: dict = None, save_path: str = "./siedler_model", profile_name: str = None):
    """
    Trainiert das Modell

    Args:
        config: Training-Konfiguration (optional)
        save_path: Pfad zum Speichern des Modells

    Returns:
        Trainiertes Modell
    """
    custom_config = dict(config or {})
    # Guard: Das Basis-Config-Dict soll Profile/Auto-Tuning nicht als "expliziter Override" blockieren.
    if custom_config == TRAINING_CONFIG:
        custom_config = {}
    config, profile = build_training_config(
        TRAINING_CONFIG,
        custom_config=custom_config,
        profile_name=profile_name,
    )
    tuning_info = _auto_tune_for_colab(config, explicit_config=custom_config)
    reward_profile = profile["reward_profile"]
    save_path = _resolve_training_save_path(save_path)
    sim_mode = _resolve_sim_mode()
    use_spatial_obs = _get_use_spatial_obs()
    tensorboard_enabled = _tensorboard_enabled()
    progress_bar_enabled = _progress_bar_enabled()

    _validate_runtime_files()

    print("=" * 60)
    print("Siedler 5 - ScharfschÃƒÂ¼tzen Training")
    print("=" * 60)
    print(f"Timesteps: {config['total_timesteps']:,}")
    print(f"Learning Rate: {config['learning_rate']}")
    print(f"Batch Size: {config['batch_size']}")
    print(f"n_steps: {config['n_steps']}")
    print(f"Save Path: {save_path}")
    print(f"Sim Mode: {sim_mode}")
    print(f"Spatial Obs: {use_spatial_obs}")
    print(f"TensorBoard: {tensorboard_enabled}")
    print(f"Progress Bar: {progress_bar_enabled}")
    print(f"Profil: {profile['name']} ({profile['description']})")
    terminal_dependency_bonus = float(reward_profile.get("terminal_dependency_bonus", 0.0))
    terminal_bonus = float(reward_profile.get("terminal_recruitable_bonus", 0.0))
    terminal_potential_bonus = float(reward_profile.get("terminal_potential_bonus_per_unit", 0.0))
    print(
        "Reward-Profil: terminal_dependency_bonus="
        f"{terminal_dependency_bonus}, "
        "terminal_recruitable_bonus="
        f"{terminal_bonus}, "
        "terminal_potential_bonus_per_unit="
        f"{terminal_potential_bonus}"
    )
    device = "cuda" if th.cuda.is_available() else "cpu"
    print(f"Device: {device}")
    if tuning_info.get("enabled"):
        runtime = tuning_info.get("runtime", {})
        preset = tuning_info.get("preset", {})
        print(
            "Auto-Tuning: "
            f"preset={preset.get('name')} "
            f"gpu={runtime.get('gpu_name')} "
            f"vram={float(runtime.get('gpu_mem_gb') or 0.0):.1f}GB "
            f"n_envs={tuning_info.get('effective_n_envs')} "
            f"spatial={tuning_info.get('effective_spatial_size')}"
        )
        if runtime.get("has_tpu"):
            print("Hinweis: TPU erkannt, aber dieses Projekt ist fuer CUDA/GPU optimiert.")
    print("=" * 60)

    # Environment erstellen
    spatial_size = _get_spatial_size()
    env = create_env(
        use_spatial_obs=use_spatial_obs,
        spatial_size=spatial_size,
        reward_profile=reward_profile,
    )
    n_envs = getattr(env, "num_envs", 1)

    print(f"\nEnvs: {n_envs}")
    print(f"Action Space: {env.action_space}")
    if isinstance(env.observation_space, gym.spaces.Dict):
        print(f"Observation Space: vector={env.observation_space['vector'].shape}, "
              f"spatial={env.observation_space['spatial'].shape}")
    else:
        print(f"Observation Space: {env.observation_space}")

    head_sizes, phase_dim = _get_multihead_metadata(env)
    if head_sizes is None or phase_dim is None:
        env.close()
        raise RuntimeError(
            "Action-Masking ist verpflichtend, aber Multi-Head API wurde nicht erkannt. "
            "Erwartet: get_action_head_sizes(), phase_dim und get_action_mask(). "
            "Bitte neuesten Repo-Stand nutzen und Runtime neu starten."
        )

    policy_kwargs = dict(config.get("policy_kwargs") or {})
    if config.get("auto_scale_arch", False):
        if isinstance(env.observation_space, gym.spaces.Dict):
            obs_dim = env.observation_space["vector"].shape[0]
        else:
            obs_dim = env.observation_space.shape[0]
        policy_kwargs["net_arch"] = _select_net_arch(obs_dim)
    policy_kwargs.update({
        "action_head_sizes": head_sizes,
        "phase_dim": phase_dim,
    })
    policy_cls = MultiHeadMaskablePolicy
    model_cls = MaskablePPO

    if isinstance(env.observation_space, gym.spaces.Dict):
        extractor_dims = _select_extractor_dims()
        policy_kwargs.update({
            "features_extractor_class": SpatialVectorExtractor,
            "features_extractor_kwargs": {
                "cnn_out_dim": extractor_dims["cnn_out_dim"],
                "vector_out_dim": extractor_dims["vector_out_dim"],
            },
        })

    # Callbacks
    checkpoint_freq_steps = max(1, int(config["checkpoint_freq"]))
    checkpoint_freq_calls = max(1, checkpoint_freq_steps // max(1, int(n_envs)))
    checkpoint_callback = CheckpointCallback(
        save_freq=checkpoint_freq_calls,
        save_path=save_path,
        name_prefix="siedler_checkpoint"
    )
    print(
        "Checkpoint cadence: "
        f"~{checkpoint_freq_calls * max(1, int(n_envs))} env-steps "
        f"(callback every {checkpoint_freq_calls} calls)"
    )

    status_every_sec = max(1, int(os.environ.get("SIEDLER_STATUS_EVERY_SEC", "5")))
    status_bar_width = max(10, int(os.environ.get("SIEDLER_STATUS_BAR_WIDTH", "24")))
    compact_status = str(os.environ.get("SIEDLER_COMPACT_STATUS", "0")).strip().lower() not in {
        "0", "false", "no", "off"
    }
    scharfschuetzen_callback = ScharfschuetzenCallback(
        check_freq=1000,
        status_every_sec=status_every_sec,
        compact_status=compact_status,
        status_bar_width=status_bar_width,
    )

    # Modell erstellen oder Resume von Checkpoint
    resume_enabled = _env_truthy(os.environ.get("SIEDLER_RESUME", "1"))
    resume_path_raw = str(os.environ.get("SIEDLER_RESUME_PATH", "")).strip()
    resume_path = None
    resume_steps = 0
    if resume_enabled:
        if resume_path_raw:
            candidate = Path(resume_path_raw).expanduser()
            if candidate.exists():
                resume_path = str(candidate)
                resume_steps = _extract_steps_from_checkpoint_path(candidate)
        if resume_path is None:
            resume_path, resume_steps = _find_latest_checkpoint(save_path)

    model = None
    if resume_path:
        try:
            print(f"Resume: lade Checkpoint {resume_path}")
            model = model_cls.load(resume_path, env=env, device=device)
            loaded_steps = int(getattr(model, "num_timesteps", 0) or 0)
            if loaded_steps > 0:
                resume_steps = max(resume_steps, loaded_steps)
            print(f"Resume: checkpoint_steps={resume_steps}")
        except Exception as exc:
            print(f"Resume fehlgeschlagen ({exc}); starte neues Modell.")
            model = None
            resume_steps = 0

    if model is None:
        model = model_cls(
            policy_cls,
            env,
            learning_rate=config["learning_rate"],
            n_steps=config["n_steps"],
            batch_size=config["batch_size"],
            n_epochs=config["n_epochs"],
            gamma=config["gamma"],
            gae_lambda=config["gae_lambda"],
            clip_range=config["clip_range"],
            ent_coef=config["ent_coef"],
            policy_kwargs=policy_kwargs,
            device=device,
            verbose=1,
            tensorboard_log=(f"{save_path}/tensorboard/" if tensorboard_enabled else None),
        )

    print("\nTraining startet...")
    print("(Checkpoints werden automatisch gespeichert)")
    print("-" * 60)

    configured_total = int(config["total_timesteps"])
    remaining_timesteps = configured_total
    if resume_steps > 0:
        remaining_timesteps = max(0, configured_total - resume_steps)
        if remaining_timesteps <= 0:
            print(
                "Resume-Hinweis: Checkpoint hat bereits >= total_timesteps. "
                "Ueberspringe weitere Learn-Phase."
            )

    # Training
    learn_kwargs = {
        "total_timesteps": remaining_timesteps,
        "callback": [checkpoint_callback, scharfschuetzen_callback],
        "progress_bar": progress_bar_enabled,
        "reset_num_timesteps": False if resume_steps > 0 else True,
    }
    if remaining_timesteps > 0:
        model.learn(**learn_kwargs)

    # Finales Modell speichern
    final_path = f"{save_path}/siedler_final"
    model.save(final_path)
    print(f"\nModell gespeichert: {final_path}")

    # Beste Ergebnisse
    print(f"\nBeste erreichte ScharfschÃƒÂ¼tzen: {scharfschuetzen_callback.best_scharfschuetzen}")

    return model


# =============================================================================
# EVALUATION FUNKTION
# =============================================================================

def evaluate(
    model,
    n_episodes: int = 10,
    render: bool = False,
    use_spatial_obs: bool = True,
    spatial_size: int = 128,
    reward_profile: dict = None,
    profile_name: str = None,
):
    """
    Evaluiert das trainierte Modell

    Args:
        model: Trainiertes Modell
        n_episodes: Anzahl der Evaluations-Episoden
        render: Ob der Output gerendert werden soll

    Returns:
        Dictionary mit Evaluations-Ergebnissen
    """
    if reward_profile is None:
        reward_profile = get_train_profile(profile_name)["reward_profile"]
    env = _create_env_instance(
        player_id=1,
        use_spatial_obs=use_spatial_obs,
        spatial_size=spatial_size,
        reward_profile=reward_profile,
    )
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
            action_mask = env.get_action_mask()
            action, _ = _predict_with_optional_mask(model, obs, action_mask)
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            done = terminated or truncated

            if render and episode == 0:
                env.render()

        # Ergebnisse speichern
        results["rewards"].append(total_reward)
        results["scharfschuetzen"].append(env.scharfschuetzen)
        results["times"].append(env.current_time)
        results["action_histories"].append(env.get_action_history())

        print(f"Episode {episode + 1}: Reward={total_reward:.2f}, ScharfschÃƒÂ¼tzen={env.scharfschuetzen}")

    # Zusammenfassung
    print("\n" + "=" * 60)
    print("EVALUATION ZUSAMMENFASSUNG")
    print("=" * 60)
    print(f"Durchschnittliche ScharfschÃƒÂ¼tzen: {np.mean(results['scharfschuetzen']):.2f}")
    print(f"Maximum ScharfschÃƒÂ¼tzen: {np.max(results['scharfschuetzen'])}")
    print(f"Durchschnittlicher Reward: {np.mean(results['rewards']):.2f}")

    return results


# =============================================================================
# EXPORT FÃƒÅ“R ECHTES SPIEL
# =============================================================================

def export_strategy(
    model,
    save_path: str = "./strategy_export.json",
    use_spatial_obs: bool = True,
    spatial_size: int = 128,
    reward_profile: dict = None,
    profile_name: str = None,
):
    """
    Exportiert die beste Strategie fÃƒÂ¼r das echte Spiel

    Args:
        model: Trainiertes Modell
        save_path: Pfad fÃƒÂ¼r den Export
    """
    if reward_profile is None:
        reward_profile = get_train_profile(profile_name)["reward_profile"]
    env = _create_env_instance(
        player_id=1,
        use_spatial_obs=use_spatial_obs,
        spatial_size=spatial_size,
        reward_profile=reward_profile,
    )
    obs, _ = env.reset()
    done = False

    strategy = {
        "map": "EMS Wintersturm",
        "player": 1,
        "goal": "Maximale ScharfschÃƒÂ¼tzen in 30 Minuten",
        "actions": [],
        "building_positions": [],
    }

    while not done:
        action_mask = env.get_action_mask()
        action, _ = _predict_with_optional_mask(model, obs, action_mask)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated

        # Nur relevante Aktionen speichern (keine "wait" Aktionen)
        if info.get("action_name") != "wait":
            strategy["actions"].append({
                "time_seconds": env.current_time,
                "time_formatted": f"{env.current_time // 60}:{env.current_time % 60:02d}",
                "action": info.get("action_name"),
            })

    strategy["building_positions"] = env.get_building_positions()
    strategy["final_scharfschuetzen"] = env.scharfschuetzen
    strategy["final_resources"] = dict(env.resources)
    strategy["final_buildings"] = {k: v for k, v in env.buildings.items() if v > 0}

    # Speichern
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(strategy, f, indent=2, ensure_ascii=False)

    print(f"Strategie exportiert: {save_path}")
    print(f"ScharfschÃƒÂ¼tzen erreicht: {strategy['final_scharfschuetzen']}")
    print(f"Anzahl Aktionen: {len(strategy['actions'])}")

    return strategy


# =============================================================================
# HAUPTPROGRAMM
# =============================================================================

if __name__ == "__main__":
    probe_only = str(os.environ.get("SIEDLER_PROBE_ENV_ONLY", "")).strip().lower()
    if probe_only in {"1", "true", "yes", "on"}:
        profile_name = get_train_profile()["name"]
        probe_steps = int(os.environ.get("SIEDLER_PROBE_STEPS", "96"))
        probe_env_throughput(profile_name=profile_name, probe_steps=probe_steps)
        raise SystemExit(0)

    # Pfad fÃƒÂ¼r Modelle
    SAVE_PATH = _resolve_training_save_path("./siedler_training")
    active_profile = get_train_profile()
    use_spatial_obs = _get_use_spatial_obs()
    spatial_size = _get_spatial_size()
    sim_mode = _resolve_sim_mode()

    print_runtime_recommendation()
    print(f"Aktiver Save-Pfad: {SAVE_PATH}")
    print(f"Simulation mode: {sim_mode}")
    print(f"use_spatial_obs={use_spatial_obs} spatial_size={spatial_size}")

    # Erstelle Ordner falls nicht vorhanden
    os.makedirs(SAVE_PATH, exist_ok=True)

    # Training
    print("\n" + "=" * 60)
    print("PHASE 1: TRAINING")
    print("=" * 60 + "\n")

    model = train(
        config=None,
        save_path=SAVE_PATH,
        profile_name=active_profile["name"],
    )

    run_eval = _env_truthy(os.environ.get("SIEDLER_RUN_EVAL", "0"))
    run_export = _env_truthy(os.environ.get("SIEDLER_RUN_EXPORT", "0"))
    eval_render = _env_truthy(os.environ.get("SIEDLER_EVAL_RENDER", "0"))
    eval_episodes = max(1, int(os.environ.get("SIEDLER_EVAL_EPISODES", "3")))

    if run_eval:
        print("\n" + "=" * 60)
        print("PHASE 2: EVALUATION")
        print("=" * 60 + "\n")
        evaluate(
            model,
            n_episodes=eval_episodes,
            render=eval_render,
            use_spatial_obs=use_spatial_obs,
            spatial_size=spatial_size,
            reward_profile=active_profile["reward_profile"],
        )
    else:
        print("\nPHASE 2: EVALUATION (uebersprungen, SIEDLER_RUN_EVAL=0)")

    if run_export:
        print("\n" + "=" * 60)
        print("PHASE 3: STRATEGIE EXPORT")
        print("=" * 60 + "\n")
        export_strategy(
            model,
            save_path=f"{SAVE_PATH}/strategy.json",
            use_spatial_obs=use_spatial_obs,
            spatial_size=spatial_size,
            reward_profile=active_profile["reward_profile"],
        )
    else:
        print("PHASE 3: STRATEGIE EXPORT (uebersprungen, SIEDLER_RUN_EXPORT=0)")

    print("\n" + "=" * 60)
    print("TRAINING ABGESCHLOSSEN!")
    print("=" * 60)
    print(f"\nModell gespeichert in: {SAVE_PATH}")
    if run_export:
        print(f"Strategie exportiert in: {SAVE_PATH}/strategy.json")
    print("\nNÃƒÂ¤chste Schritte:")
    print("1. Modell herunterladen")
    print("2. strategy.json fÃƒÂ¼r das echte Spiel nutzen")
    print("3. Game-Bridge ausfÃƒÂ¼hren")





