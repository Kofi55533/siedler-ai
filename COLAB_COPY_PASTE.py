# ============================================================================
# SIEDLER AI - COLAB QUICKSTART (ONE CELL, AUTO-SYNC)
# Copy the whole block below into ONE Colab cell and run it.
# ============================================================================

from pathlib import Path
import os
import re
import shutil
import subprocess
import sys
import zipfile


def run(cmd, cwd=None, env=None):
    print("$", " ".join(cmd))
    subprocess.check_call(cmd, cwd=cwd, env=env)


def run_capture(cmd, cwd=None, env=None, timeout_sec=240):
    print("$", " ".join(cmd))
    return subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        timeout=timeout_sec,
    )


def infer_target_n_envs():
    cpu_cap = max(1, (os.cpu_count() or 1) - 1)
    target = min(cpu_cap, 4)
    gpu_name = "CPU"
    try:
        import torch as th

        if th.cuda.is_available():
            gpu_name = th.cuda.get_device_name(0).upper()
            if "H100" in gpu_name:
                target = 10
            elif "A100" in gpu_name:
                target = 8
            elif "L4" in gpu_name or "V100" in gpu_name:
                target = 6
            elif "T4" in gpu_name or "P100" in gpu_name:
                target = 4
            else:
                target = 4
        else:
            target = 2
    except Exception:
        target = 2

    return max(1, min(cpu_cap, target)), gpu_name, cpu_cap


def build_n_env_candidates():
    target, gpu_name, cpu_cap = infer_target_n_envs()
    raw = [min(cpu_cap, target + 2), target, target - 1, target - 2, 8, 6, 4, 3, 2, 1]
    seen = set()
    ordered = []
    for n in raw:
        if 1 <= n <= cpu_cap and n not in seen:
            seen.add(n)
            ordered.append(n)
    ordered.sort(reverse=True)
    if 1 not in ordered:
        ordered.append(1)
    return ordered, target, gpu_name


def parse_probe_sps(stdout_text: str):
    match = re.search(r"ENV_PROBE_RESULT\s+n_envs=(\d+)\s+throughput_sps=([0-9.]+)", stdout_text or "")
    if not match:
        return None, None
    return int(match.group(1)), float(match.group(2))


def auto_select_fastest_n_envs():
    if os.environ.get("SIEDLER_NUM_ENVS"):
        manual = max(1, int(os.environ["SIEDLER_NUM_ENVS"]))
        print(f"Using manual SIEDLER_NUM_ENVS={manual}")
        return manual, True

    candidates, target, gpu_name = build_n_env_candidates()
    print("Auto benchmark for n_envs started")
    print(f"GPU: {gpu_name}")
    print(f"Probe candidates: {candidates} (target={target})")

    successful = []
    for n_envs in candidates:
        probe_env = os.environ.copy()
        probe_env["SIEDLER_NUM_ENVS"] = str(n_envs)
        probe_env["SIEDLER_PROBE_ENV_ONLY"] = "1"
        probe_env["SIEDLER_PROBE_STEPS"] = "96"

        try:
            result = run_capture(
                [sys.executable, "colab_training.py"],
                cwd=PROJECT_DIR,
                env=probe_env,
                timeout_sec=300,
            )
        except subprocess.TimeoutExpired:
            print(f"Probe timeout for n_envs={n_envs}")
            continue
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

        if result.returncode != 0:
            print(f"Probe failed for n_envs={n_envs}")
            continue

        parsed_n, sps = parse_probe_sps(result.stdout or "")
        eff_n = parsed_n if parsed_n is not None else n_envs
        eff_sps = sps if sps is not None else 0.0
        successful.append((eff_n, eff_sps))
        print(f"Probe success: n_envs={eff_n}, throughput_sps={eff_sps:.2f}")

    if not successful:
        raise RuntimeError("No stable n_envs found during auto benchmark.")

    best_n, best_sps = max(successful, key=lambda item: (item[1], item[0]))
    os.environ["SIEDLER_NUM_ENVS"] = str(best_n)
    print(f"Selected fastest stable n_envs={best_n} (throughput_sps={best_sps:.2f})")
    return best_n, False


def build_fallback_n_envs(start_n: int):
    raw = [start_n, start_n - 1, start_n - 2, max(1, start_n // 2), 1]
    ordered = []
    seen = set()
    for n in raw:
        n = max(1, int(n))
        if n not in seen:
            seen.add(n)
            ordered.append(n)
    return ordered


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

# 8) AUTO-SELECT FASTEST STABLE N_ENVS
selected_n_envs, manual_override = auto_select_fastest_n_envs()
print(f"Effective SIEDLER_NUM_ENVS={selected_n_envs}")

# 9) START TRAINING (with guarded fallback)
fallback_chain = [selected_n_envs] if manual_override else build_fallback_n_envs(selected_n_envs)
last_error = None
for idx, n_envs in enumerate(fallback_chain):
    os.environ["SIEDLER_NUM_ENVS"] = str(n_envs)
    print(f"Training attempt {idx + 1}/{len(fallback_chain)} with SIEDLER_NUM_ENVS={n_envs}")
    try:
        run([sys.executable, "colab_training.py"])
        last_error = None
        break
    except subprocess.CalledProcessError as exc:
        last_error = exc
        if idx == len(fallback_chain) - 1:
            raise
        print(f"Training crashed for n_envs={n_envs}; retrying with fewer envs...")

if last_error is None:
    print("Training finished successfully.")
