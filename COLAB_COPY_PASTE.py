# ============================================================================
# SIEDLER AI - COLAB QUICKSTART (ONE CELL, AUTO-SYNC)
# Copy the whole block below into ONE Colab cell and run it.
# ============================================================================

from pathlib import Path
import os
import shutil
import subprocess
import sys
import zipfile


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


def copy_file_to_data_dir(src_path: Path, dst_name: str):
    dst = Path(DATA_DIR) / dst_name
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dst)
    print(f"Synced to DATA_DIR: {dst_name}")


def extract_file_from_zip_to_data_dir(zip_path: Path, dst_name: str) -> bool:
    if not zip_path.exists():
        return False
    dst = Path(DATA_DIR) / dst_name
    dst.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        members = [m for m in zf.namelist() if m.endswith("/" + dst_name) or m == dst_name]
        if not members:
            return False
        member = sorted(members, key=len)[0]
        with zf.open(member, "r") as src, open(dst, "wb") as dst_file:
            shutil.copyfileobj(src, dst_file)
    print(f"Extracted from ZIP to DATA_DIR: {dst_name}")
    return True


def ensure_data_file(dst_name: str, project_candidates):
    dst = Path(DATA_DIR) / dst_name
    if dst.exists():
        return True

    for candidate in project_candidates:
        src = Path(candidate)
        if src.exists():
            copy_file_to_data_dir(src, dst_name)
            return True

    if extract_file_from_zip_to_data_dir(Path(DRIVE_ZIP), dst_name):
        return True

    return False


# 4) INSTALL DEPENDENCIES
for package in ("gymnasium", "stable-baselines3", "sb3-contrib", "tensorboard"):
    run([sys.executable, "-m", "pip", "install", "-q", package])


# 5) AUTO-SYNC REQUIRED DATA TO GOOGLE DRIVE
if not ensure_data_file("player1_resources.json", ["player1_resources.json"]):
    raise FileNotFoundError(
        "Missing player1_resources.json. "
        "Expected in project root, DATA_DIR, or inside DRIVE_ZIP."
    )

walkable_candidates = ["player1_walkable_515.npy", "player1_walkable.npy"]
if not any((Path(DATA_DIR) / name).exists() for name in walkable_candidates):
    copied_walkable = False
    for name in walkable_candidates:
        if ensure_data_file(name, [name]):
            copied_walkable = True
            break
    if not copied_walkable:
        raise FileNotFoundError(
            "Missing walkable file. Expected player1_walkable_515.npy or "
            "player1_walkable.npy in project root, DATA_DIR, or inside DRIVE_ZIP."
        )

# Optional file for maximum engine parity
truth_src = Path("config/worker_truth_model.json")
truth_dst = Path(DATA_DIR) / "config" / "worker_truth_model.json"
if truth_src.exists() and not truth_dst.exists():
    truth_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(truth_src, truth_dst)
    print("Synced optional file to DATA_DIR: config/worker_truth_model.json")
elif not truth_dst.exists():
    extract_file_from_zip_to_data_dir(Path(DRIVE_ZIP), "config/worker_truth_model.json")


# 6) PREFLIGHT CHECK (clear message before long training start)
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
missing = [name for name in required_files if not Path(name).exists()]

walkable_in_data = any((Path(DATA_DIR) / name).exists() for name in walkable_candidates)
if not (Path(DATA_DIR) / "player1_resources.json").exists():
    missing.append("player1_resources.json (DATA_DIR)")
if not walkable_in_data:
    missing.append("player1_walkable_515.npy or player1_walkable.npy (DATA_DIR)")

if missing:
    raise FileNotFoundError(
        "Missing required files in project:\n- "
        + "\n- ".join(missing)
        + "\n\nIf SOURCE_MODE='git': commit/push missing files first.\n"
          "For large data files, upload once to DATA_DIR and keep SOURCE_MODE='git'."
    )


# 7) FORCE SAVE TO DRIVE
Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)
os.environ["SIEDLER_SAVE_DIR"] = SAVE_DIR
os.environ["SIEDLER_REQUIRE_DRIVE"] = "1"

# Optional overrides:
# os.environ["SIEDLER_NUM_ENVS"] = "8"
# os.environ["SIEDLER_SPATIAL_SIZE"] = "160"
# os.environ["SIEDLER_TRAIN_PROFILE"] = "sparse"

print(f"Model checkpoints/final model will be saved to: {SAVE_DIR}")
print(f"Code source mode: {SOURCE_MODE}")


# 8) START TRAINING
# Run as separate process (safer with multiprocessing/SubprocVecEnv in Colab).
try:
    run([sys.executable, "colab_training.py"])
except subprocess.CalledProcessError:
    if os.environ.get("SIEDLER_NUM_ENVS"):
        raise
    print("Training start failed with multiprocessing settings. Retrying with SIEDLER_NUM_ENVS=1 ...")
    os.environ["SIEDLER_NUM_ENVS"] = "1"
    run([sys.executable, "colab_training.py"])
