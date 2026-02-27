# ============================================================================
# SIEDLER AI - COLAB QUICKSTART (ONE CELL, AUTO-SYNC)
# Copy the whole block below into ONE Colab cell and run it.
# ============================================================================

from pathlib import Path
import os
import shutil
import subprocess
import sys
import runpy


def run(cmd, cwd=None):
    print("$", " ".join(cmd))
    subprocess.check_call(cmd, cwd=cwd)


# 1) CONFIG
# Source mode:
#   "git" -> always clone latest from GitHub (recommended)
#   "zip" -> fallback to zip in MyDrive
SOURCE_MODE = "git"

REPO_URL = "https://github.com/Kofi55533/siedler-ai.git"
REPO_BRANCH = "main"

DRIVE_ZIP = "/content/drive/MyDrive/siedler_ai_colab_bundle.zip"
PROJECT_DIR = "/content/siedler_ai"
SAVE_DIR = "/content/drive/MyDrive/siedler_training"
DATA_DIR = "/content/drive/MyDrive/siedler_data"


# 2) MOUNT GOOGLE DRIVE
from google.colab import drive
drive.mount("/content/drive", force_remount=False)


# 3) PREPARE PROJECT SOURCE
if Path(PROJECT_DIR).exists():
    shutil.rmtree(PROJECT_DIR)

if SOURCE_MODE == "git":
    run(["git", "clone", "--depth", "1", "--branch", REPO_BRANCH, REPO_URL, PROJECT_DIR])
elif SOURCE_MODE == "zip":
    if not Path(DRIVE_ZIP).exists():
        raise FileNotFoundError(
            f"Zip not found: {DRIVE_ZIP}\n"
            "Upload siedler_ai_colab_bundle.zip to MyDrive or switch SOURCE_MODE='git'."
        )
    Path(PROJECT_DIR).mkdir(parents=True, exist_ok=True)
    print(f"Unpacking: {DRIVE_ZIP}")
    run(["unzip", "-q", DRIVE_ZIP, "-d", PROJECT_DIR])
else:
    raise ValueError("SOURCE_MODE must be 'git' or 'zip'")


# If zip contains a single top-level folder, flatten it to PROJECT_DIR.
entries = [p for p in Path(PROJECT_DIR).iterdir()]
if len(entries) == 1 and entries[0].is_dir() and SOURCE_MODE == "zip":
    nested_root = entries[0]
    for item in nested_root.iterdir():
        target = Path(PROJECT_DIR) / item.name
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        shutil.move(str(item), str(target))
    nested_root.rmdir()

os.chdir(PROJECT_DIR)
print(f"Project dir: {PROJECT_DIR}")
Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
os.environ["SIEDLER_DATA_DIR"] = DATA_DIR
print(f"Data dir: {DATA_DIR}")


# 4) INSTALL DEPENDENCIES
for package in ("gymnasium", "stable-baselines3", "sb3-contrib", "tensorboard"):
    run([sys.executable, "-m", "pip", "install", "-q", package])


# 5) PREFLIGHT CHECK (clear message before long training start)
required_files = [
    "colab_training.py",
    "environment.py",
    "multihead_policy.py",
    "training_profiles.py",
    "map_config_wintersturm.py",
    "wood_zones_config.py",
    "production_system.py",
    "worker_simulation.py",
    "pathfinding.py",
]
walkable_candidates = ["player1_walkable_515.npy", "player1_walkable.npy"]
missing = [name for name in required_files if not Path(name).exists()]

resources_in_project = Path("player1_resources.json").exists()
resources_in_data = (Path(DATA_DIR) / "player1_resources.json").exists()
if not (resources_in_project or resources_in_data):
    missing.append("player1_resources.json (project root or DATA_DIR)")

walkable_in_project = any(Path(name).exists() for name in walkable_candidates)
walkable_in_data = any((Path(DATA_DIR) / name).exists() for name in walkable_candidates)
if not (walkable_in_project or walkable_in_data):
    missing.append("player1_walkable_515.npy or player1_walkable.npy (project root or DATA_DIR)")

if missing:
    raise FileNotFoundError(
        "Missing required files in project:\n- "
        + "\n- ".join(missing)
        + "\n\nIf SOURCE_MODE='git': commit/push missing files first.\n"
          "For large data files, upload once to DATA_DIR and keep SOURCE_MODE='git'."
    )


# 6) FORCE SAVE TO DRIVE
Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)
os.environ["SIEDLER_SAVE_DIR"] = SAVE_DIR
os.environ["SIEDLER_REQUIRE_DRIVE"] = "1"

# Optional overrides:
# os.environ["SIEDLER_NUM_ENVS"] = "8"
# os.environ["SIEDLER_SPATIAL_SIZE"] = "160"
# os.environ["SIEDLER_TRAIN_PROFILE"] = "sparse"

print(f"Model checkpoints/final model will be saved to: {SAVE_DIR}")
print(f"Code source mode: {SOURCE_MODE}")


# 7) START TRAINING
# Run in-process so Colab shows the real traceback directly.
print(f"$ {sys.executable} colab_training.py")
runpy.run_path("colab_training.py", run_name="__main__")
