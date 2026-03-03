# ============================================================================
# SIEDLER AI - COLAB QUICKSTART (ONE CELL, AUTO-SYNC)
# Copy the whole block below into ONE Colab cell and run it.
# ============================================================================

from pathlib import Path
import json
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile

# Reduce TensorFlow/CUDA log spam in spawned training subprocesses.
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("PYTHONWARNINGS", "ignore")


NOISY_LOG_PATTERNS = (
    "computation_placer.cc:177",
    "Unable to register cuDNN factory",
    "Unable to register cuBLAS factory",
    "Unable to register cuFFT factory",
    "WARNING: All log messages before absl::InitializeLog() is called are written to STDERR",
    "Gym has been unmaintained since 2022",
    "Please upgrade to Gymnasium",
    "See the migration guide at https://gymnasium.farama.org/introduction/migration_guide/",
    "tensorflow/core/platform/cpu_feature_guard.cc",
    "tensorflow/core/util/port.cc",
)


def _is_noisy_runtime_line(line: str) -> bool:
    text = str(line or "").strip()
    if not text:
        return False
    return any(pattern in text for pattern in NOISY_LOG_PATTERNS)


def _print_filtered_text(text: str):
    if not text:
        return
    for raw_line in str(text).splitlines():
        if _is_noisy_runtime_line(raw_line):
            continue
        print(raw_line)


def _env_truthy(value):
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _prepare_cmd_env(cmd, env=None):
    cmd = list(cmd)
    exe_name = Path(cmd[0]).name.lower() if cmd else ""
    if cmd and (cmd[0] == sys.executable or exe_name.startswith("python")) and "-u" not in cmd[1:]:
        cmd.insert(1, "-u")

    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    merged_env.setdefault("PYTHONUNBUFFERED", "1")
    return cmd, merged_env


def run(cmd, cwd=None, env=None):
    cmd, merged_env = _prepare_cmd_env(cmd, env=env)
    print("$", " ".join(cmd))
    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        env=merged_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    if proc.stdout is None:
        raise RuntimeError("Failed to capture subprocess output stream.")

    start_ts = time.time()
    last_line_ts = start_ts
    last_heartbeat_ts = start_ts

    while True:
        line = proc.stdout.readline()
        if line:
            if not _is_noisy_runtime_line(line):
                print(line, end="")
            last_line_ts = time.time()
            continue

        if proc.poll() is not None:
            break

        now = time.time()
        if now - last_heartbeat_ts >= 30:
            silent_for = int(now - last_line_ts)
            running_for = int(now - start_ts)
            print(
                f"[runner] command still running ({running_for}s), "
                f"no new output for {silent_for}s..."
            )
            last_heartbeat_ts = now
        time.sleep(0.2)

    returncode = proc.wait()
    if returncode != 0:
        raise subprocess.CalledProcessError(returncode, cmd)


def run_capture(cmd, cwd=None, env=None, timeout_sec=240):
    cmd, merged_env = _prepare_cmd_env(cmd, env=env)
    print("$", " ".join(cmd))
    return subprocess.run(
        cmd,
        cwd=cwd,
        env=merged_env,
        text=True,
        capture_output=True,
        timeout=timeout_sec,
    )


def print_repo_revision(repo_dir: str):
    result = run_capture(["git", "log", "-1", "--pretty=format:%h %cs %s"], cwd=repo_dir, timeout_sec=30)
    if result.returncode == 0 and result.stdout:
        print(f"Repo revision: {result.stdout.strip()}")
    else:
        print("Repo revision: unknown")


def pip_install_with_retry(packages, retries=3):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            run([sys.executable, "-m", "pip", "install", "-q", *packages])
            return
        except subprocess.CalledProcessError as exc:
            last_error = exc
            if attempt == retries:
                raise
            print(f"pip install failed (attempt {attempt}/{retries}); retrying...")
            time.sleep(2)
    if last_error is not None:
        raise last_error


def install_colab_dependencies():
    req_file = Path(PROJECT_DIR) / "requirements-colab.txt"
    if req_file.exists():
        print(f"Installing dependencies from {req_file.name}")
        pip_install_with_retry(["-r", str(req_file)])
        return

    print("requirements-colab.txt not found; using fallback package list.")
    pip_install_with_retry(["gymnasium", "stable-baselines3", "sb3-contrib", "tensorboard"])


def smoke_check_training_imports():
    smoke_script = Path(PROJECT_DIR) / "smoke_check.py"
    if smoke_script.exists():
        smoke_cmd = [sys.executable, "-u", str(smoke_script), "--check-deps"]
    else:
        smoke_code = (
            "import production_system as ps\n"
            "import worker_simulation as ws\n"
            "print('SMOKE has_refiner_ops=', hasattr(ps, 'get_refiner_resource_ops_per_cycle'))\n"
            "print('SMOKE has_force_to_work_penalty=', hasattr(ws, 'FORCE_TO_WORK_PENALTY'))\n"
            "import colab_training\n"
            "print('SMOKE_IMPORT_OK')\n"
        )
        smoke_cmd = [sys.executable, "-u", "-c", smoke_code]

    result = run_capture(
        smoke_cmd,
        cwd=PROJECT_DIR,
        timeout_sec=180,
    )
    if result.stdout:
        _print_filtered_text(result.stdout)
    if result.stderr:
        _print_filtered_text(result.stderr)
    if result.returncode != 0:
        raise RuntimeError(
            "Preflight import smoke-check failed. "
            "Restart runtime and rerun cell. If it still fails, check repo commit output above."
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
                target = 10
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
    top_probe = min(cpu_cap, max(12, target + 6))
    raw = list(range(top_probe, max(0, top_probe - 10), -1)) + [target, target - 1, target - 2, 8, 6, 4, 3, 2, 1]
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


def infer_gpu_training_preset():
    _, gpu_name, cpu_cap = infer_target_n_envs()
    gpu_upper = (gpu_name or "").upper()
    fast_mode = _env_truthy(os.environ.get("SIEDLER_FAST_TRAIN")) or (
        str(os.environ.get("SIEDLER_SIM_MODE", "")).strip().lower() == "fast_train"
    )

    if "H100" in gpu_upper:
        n_envs, spatial_size = cpu_cap, 192
    elif "A100" in gpu_upper:
        n_envs, spatial_size = cpu_cap, 160
    elif "L4" in gpu_upper or "V100" in gpu_upper:
        n_envs, spatial_size = cpu_cap, 128
    elif "T4" in gpu_upper or "P100" in gpu_upper:
        n_envs, spatial_size = cpu_cap, 128
    else:
        n_envs, spatial_size = cpu_cap, 96

    n_envs = max(1, min(cpu_cap, int(n_envs)))
    if fast_mode:
        spatial_size = min(spatial_size, 96)
    return {"gpu_name": gpu_name, "n_envs": n_envs, "spatial_size": spatial_size}


def apply_auto_gpu_overrides():
    preset = infer_gpu_training_preset()
    os.environ.pop("SIEDLER_NUM_ENVS_AUTO", None)
    os.environ.pop("SIEDLER_SPATIAL_SIZE_AUTO", None)

    if not os.environ.get("SIEDLER_NUM_ENVS"):
        os.environ["SIEDLER_NUM_ENVS"] = str(preset["n_envs"])
        os.environ["SIEDLER_NUM_ENVS_AUTO"] = "1"
    if not os.environ.get("SIEDLER_SPATIAL_SIZE"):
        os.environ["SIEDLER_SPATIAL_SIZE"] = str(preset["spatial_size"])
        os.environ["SIEDLER_SPATIAL_SIZE_AUTO"] = "1"

    print(
        "Auto GPU preset: "
        f"{preset['gpu_name']} -> "
        f"SIEDLER_NUM_ENVS={os.environ.get('SIEDLER_NUM_ENVS')}, "
        f"SIEDLER_SPATIAL_SIZE={os.environ.get('SIEDLER_SPATIAL_SIZE')}"
    )


def parse_probe_sps(stdout_text: str):
    match = re.search(r"ENV_PROBE_RESULT\s+n_envs=(\d+)\s+throughput_sps=([0-9.]+)", stdout_text or "")
    if not match:
        return None, None
    return int(match.group(1)), float(match.group(2))


def auto_select_fastest_n_envs():
    if os.environ.get("SIEDLER_NUM_ENVS"):
        manual = max(1, int(os.environ["SIEDLER_NUM_ENVS"]))
        is_auto = os.environ.get("SIEDLER_NUM_ENVS_AUTO") == "1"
        benchmark_auto = _env_truthy(os.environ.get("SIEDLER_BENCHMARK_AUTO_ENVS", "0"))
        if is_auto and not benchmark_auto:
            print(f"Using auto GPU SIEDLER_NUM_ENVS={manual}")
            return manual, False
        if is_auto and benchmark_auto:
            print(
                f"Auto GPU preset SIEDLER_NUM_ENVS={manual} detected; "
                "running benchmark override for max throughput."
            )
            cpu_cap = max(1, (os.cpu_count() or 1) - 1)
            top_probe = min(cpu_cap, max(12, manual + 6))
            raw = list(range(top_probe, max(0, top_probe - 10), -1)) + [
                manual + 2,
                manual + 1,
                manual,
                manual - 1,
                manual - 2,
                8,
                6,
                4,
                3,
                2,
                1,
            ]
            seen = set()
            candidates = []
            for n in raw:
                if 1 <= n <= cpu_cap and n not in seen:
                    seen.add(n)
                    candidates.append(n)
            candidates.sort(reverse=True)
            target = manual
            gpu_name = infer_target_n_envs()[1]
        else:
            print(f"Using manual SIEDLER_NUM_ENVS={manual}")
            return manual, True
    else:
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
            _print_filtered_text(result.stdout)
        if result.stderr:
            _print_filtered_text(result.stderr)

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
# Training mode:
#   "fast_train" -> maximale FPS (weniger Simulations-Treue)
#   "full_sim"   -> volle Simulations-Treue (langsamer)
TRAIN_MODE = "fast_train"
# Reward-/Trainingsprofil (z. B. legacy, sparse, dense_v2, balanced, aggressive)
TRAIN_PROFILE = "legacy"
# Fester Parallelisierungsgrad fuer Training (None = automatisch nach GPU/CPU).
# Setze auf eine Zahl (z. B. 10) um den Wert manuell zu fixieren.
FIXED_NUM_ENVS = None
# Ziel-Timesteps fuer diesen Run
TRAIN_TOTAL_TIMESTEPS = 5_000_000
# Nach dem Training automatisch Modellverhalten analysieren.
RUN_POST_ANALYSIS = True
# Anzahl Analyse-Episoden (deterministische Policy mit Action-Mask).
POST_ANALYSIS_EPISODES = 8
# Modell-Prioritaet fuer Analyse: "best_first" oder "final_first".
POST_ANALYSIS_MODEL_PREF = "best_first"

REPO_URL = "https://github.com/Kofi55533/siedler-ai.git"
REPO_BRANCH = "main"

DRIVE_ZIP = "/content/drive/MyDrive/siedler_ai_colab_bundle.zip"
PROJECT_DIR = "/content/siedler_ai"
SAVE_DIR = "/content/drive/MyDrive/siedler_training"
DATA_DIR = "/content/drive/MyDrive/siedler_data"


def build_train_overrides():
    """
    Explizite Train-Overrides fuer reproduzierbare Runs aus dieser One-Cell.
    """
    total_steps = max(1, int(TRAIN_TOTAL_TIMESTEPS))
    cfg = {
        "total_timesteps": total_steps,
        "checkpoint_freq": max(50_000, total_steps // 5),
        "eval_freq": max(50_000, total_steps // 5),
    }

    profile = str(TRAIN_PROFILE).strip().lower()
    mode = str(TRAIN_MODE).strip().lower()
    if mode == "fast_train" and profile == "legacy":
        # High-End fast_train Preset fuer Legacy.
        cfg.update({
            "learning_rate": 0.0002,
            "n_steps": 4096,
            "batch_size": 1024,
            "n_epochs": 6,
            "gamma": 0.995,
            "gae_lambda": 0.95,
            "clip_range": 0.2,
            "ent_coef": 0.012,
        })
    return cfg


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
print_repo_revision(PROJECT_DIR)
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


def sync_legacy_env_data_layout():
    """
    Kompatibilitaet fuer alte environment.py-Versionen mit hart codiertem Windows-Pfad.
    """
    legacy_root = Path(PROJECT_DIR) / r"c:\Users\marku\OneDrive\Desktop\siedler_ai"
    legacy_root.mkdir(parents=True, exist_ok=True)

    walkable_sources = [
        Path(DATA_DIR) / "player1_walkable.npy",
        Path(DATA_DIR) / "player1_walkable_515.npy",
        Path(PROJECT_DIR) / "player1_walkable.npy",
        Path(PROJECT_DIR) / "player1_walkable_515.npy",
    ]
    walkable_src = next((p for p in walkable_sources if p.exists()), None)
    if walkable_src is not None:
        shutil.copy2(walkable_src, legacy_root / "player1_walkable.npy")

    resources_sources = [
        Path(DATA_DIR) / "player1_resources.json",
        Path(PROJECT_DIR) / "player1_resources.json",
    ]
    resources_src = next((p for p in resources_sources if p.exists()), None)
    if resources_src is not None:
        shutil.copy2(resources_src, legacy_root / "player1_resources.json")

    print(f"Legacy env data mirror: {legacy_root}")


# 4) INSTALL DEPENDENCIES
install_colab_dependencies()


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

# Legacy-Path fuer alte Environment-Versionen bereitstellen.
if _env_truthy(os.environ.get("SIEDLER_ENABLE_LEGACY_MIRROR", "0")):
    sync_legacy_env_data_layout()
else:
    print("Legacy env data mirror: disabled (set SIEDLER_ENABLE_LEGACY_MIRROR=1 to enable)")


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

smoke_check_training_imports()


# 7) FORCE SAVE TO DRIVE
Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)
os.environ["SIEDLER_SAVE_DIR"] = SAVE_DIR
os.environ["SIEDLER_REQUIRE_DRIVE"] = "1"
os.environ["SIEDLER_SIM_MODE"] = TRAIN_MODE

if TRAIN_MODE == "fast_train":
    # Hart setzen, damit alte Notebook-Env-Werte nie unbemerkt fast_train ausbremsen.
    os.environ["SIEDLER_FAST_TRAIN"] = "1"
    os.environ["SIEDLER_TURBO_FPS"] = "1"
    os.environ["SIEDLER_DISABLE_RUNTIME_PATHING"] = "1"
    os.environ["SIEDLER_USE_SPATIAL"] = "0"
    os.environ["SIEDLER_RUNTIME_STATUS"] = "0"
    os.environ["SIEDLER_SB3_VERBOSE"] = "1"
    os.environ["SIEDLER_BENCHMARK_AUTO_ENVS"] = "0"
    os.environ["SIEDLER_PROGRESS_BAR"] = "0"
    os.environ["SIEDLER_TENSORBOARD"] = "0"
    os.environ["SIEDLER_TRAIN_PROFILE"] = TRAIN_PROFILE
else:
    os.environ["SIEDLER_FAST_TRAIN"] = "0"
    os.environ["SIEDLER_TURBO_FPS"] = "0"
    os.environ["SIEDLER_DISABLE_RUNTIME_PATHING"] = "0"
    os.environ["SIEDLER_USE_SPATIAL"] = "1"
    os.environ["SIEDLER_RUNTIME_STATUS"] = "0"
    os.environ["SIEDLER_SB3_VERBOSE"] = "1"
    os.environ["SIEDLER_BENCHMARK_AUTO_ENVS"] = "0"
    os.environ["SIEDLER_PROGRESS_BAR"] = "1"
    os.environ["SIEDLER_TENSORBOARD"] = "1"
    os.environ["SIEDLER_TRAIN_PROFILE"] = TRAIN_PROFILE

# Fuer diese One-Cell immer explizit setzen (ueberschreibt eventuell alte Notebook-Env-Werte).
os.environ["SIEDLER_TRAIN_PROFILE"] = TRAIN_PROFILE

# Robustheit fuer Colab-Disconnects + klarer Fresh-Start.
# Immer neu trainieren (kein Resume von alten Checkpoints).
os.environ["SIEDLER_RESUME"] = "0"
os.environ["SIEDLER_CLEAN_CHECKPOINTS_ON_FRESH"] = "1"
os.environ.pop("SIEDLER_RESUME_PATH", None)
os.environ["SIEDLER_RUN_EVAL"] = "0"
os.environ["SIEDLER_RUN_EXPORT"] = "0"
os.environ["SIEDLER_EVAL_RENDER"] = "0"

# Kein FPS-Benchmark: n_envs automatisch nach GPU/CPU oder manuell fixiert.
cpu_cap = max(1, (os.cpu_count() or 1) - 1)
if FIXED_NUM_ENVS is None:
    _gpu_preset = infer_gpu_training_preset()
    effective_n_envs = _gpu_preset["n_envs"]
    _spatial_size = _gpu_preset["spatial_size"]
else:
    effective_n_envs = max(1, min(int(FIXED_NUM_ENVS), cpu_cap))
    _spatial_size = 96
os.environ["SIEDLER_BENCHMARK_AUTO_ENVS"] = "0"
os.environ["SIEDLER_NUM_ENVS"] = str(effective_n_envs)
os.environ["SIEDLER_SPATIAL_SIZE"] = str(_spatial_size)
train_overrides = build_train_overrides()
print(f"Simulation mode: {TRAIN_MODE}")
print(f"Training profile: {os.environ.get('SIEDLER_TRAIN_PROFILE')}")
print(f"Fixed n_envs: {effective_n_envs} (cpu_cap={cpu_cap})")
print(
    "Effective fast flags: "
    f"FAST={os.environ.get('SIEDLER_FAST_TRAIN')} "
    f"SPATIAL={os.environ.get('SIEDLER_USE_SPATIAL')} "
    f"PATHING_OFF={os.environ.get('SIEDLER_DISABLE_RUNTIME_PATHING')} "
    f"TURBO={os.environ.get('SIEDLER_TURBO_FPS')}"
)
print(f"Total timesteps: {int(train_overrides.get('total_timesteps', 0))}")
print(f"Post analysis enabled: {int(bool(RUN_POST_ANALYSIS))} (episodes={POST_ANALYSIS_EPISODES})")
print(f"Resume enabled: {os.environ.get('SIEDLER_RESUME')}")
print(
    "Post-train phases: "
    f"eval={os.environ.get('SIEDLER_RUN_EVAL')} "
    f"export={os.environ.get('SIEDLER_RUN_EXPORT')}"
)

# 7b) Keine Auto-Benchmark-/Auto-GPU-Ueberschreibung aktiv.

# Optionale manuelle Overrides (nur falls du bewusst testen willst):
# os.environ["SIEDLER_NUM_ENVS"] = "3"
# os.environ["SIEDLER_SPATIAL_SIZE"] = "128"
# os.environ["SIEDLER_STATUS_EVERY_SEC"] = "5"   # Live-Status: Schritte/FPS alle X Sekunden
# os.environ["SIEDLER_COMPACT_STATUS"] = "0"     # 0=Zeilenmodus (zuverlaessig in Colab)
# os.environ["SIEDLER_STATUS_BAR_WIDTH"] = "24"  # Breite des Fortschritt-Balkens
# os.environ["SIEDLER_TRAIN_PROFILE"] = "sparse"   # terminal-lastig
# os.environ["SIEDLER_TRAIN_PROFILE"] = "dense_v2" # zustandsaenderungs-basiertes Dense-Shaping

os.environ.setdefault("SIEDLER_STATUS_EVERY_SEC", "10")
os.environ.setdefault("SIEDLER_COMPACT_STATUS", "0")
os.environ.setdefault("SIEDLER_STATUS_BAR_WIDTH", "24")

print(f"Model checkpoints/final model will be saved to: {SAVE_DIR}")
print(f"Code source mode: {SOURCE_MODE}")

# 8) START TRAINING (fixed n_envs, no FPS benchmark/fallback loop)
train_overrides_json = json.dumps(train_overrides)
train_entry_code = (
    "import json, os\n"
    "import colab_training as ct\n"
    "cfg = json.loads(os.environ['SIEDLER_TRAIN_OVERRIDES_JSON'])\n"
    "profile = os.environ.get('SIEDLER_TRAIN_PROFILE')\n"
    "save_dir = os.environ.get('SIEDLER_SAVE_DIR', './siedler_training')\n"
    "ct.train(config=cfg, save_path=save_dir, profile_name=profile)\n"
)
last_error = None
print(f"Training with fixed SIEDLER_NUM_ENVS={os.environ.get('SIEDLER_NUM_ENVS')}")
try:
    run(
        [sys.executable, "-u", "-c", train_entry_code],
        env={"SIEDLER_TRAIN_OVERRIDES_JSON": train_overrides_json},
    )
except subprocess.CalledProcessError as exc:
    last_error = exc
    raise

if last_error is None:
    print("Training finished successfully.")
    if RUN_POST_ANALYSIS:
        post_analysis_code = (
            "import json, os\n"
            "from pathlib import Path\n"
            "from collections import Counter\n"
            "import numpy as np\n"
            "import torch as th\n"
            "from sb3_contrib import MaskablePPO\n"
            "import colab_training as ct\n"
            "\n"
            "def _env_truthy(v):\n"
            "    return str(v).strip().lower() in {'1', 'true', 'yes', 'on'}\n"
            "\n"
            "def _to_jsonable(obj):\n"
            "    import numpy as _np\n"
            "    if isinstance(obj, dict):\n"
            "        return {str(k): _to_jsonable(v) for k, v in obj.items()}\n"
            "    if isinstance(obj, (list, tuple)):\n"
            "        return [_to_jsonable(v) for v in obj]\n"
            "    if isinstance(obj, _np.generic):\n"
            "        return obj.item()\n"
            "    return obj\n"
            "\n"
            "save_dir = os.environ.get('SIEDLER_SAVE_DIR', './siedler_training')\n"
            "profile = os.environ.get('SIEDLER_TRAIN_PROFILE')\n"
            "episodes = max(1, int(os.environ.get('SIEDLER_POST_ANALYSIS_EPISODES', '8')))\n"
            "model_pref = os.environ.get('SIEDLER_POST_ANALYSIS_MODEL', 'best_first').strip().lower()\n"
            "use_spatial = _env_truthy(os.environ.get('SIEDLER_USE_SPATIAL', '0'))\n"
            "spatial_size = max(16, int(os.environ.get('SIEDLER_SPATIAL_SIZE', '96')))\n"
            "device = 'cuda' if th.cuda.is_available() else 'cpu'\n"
            "root = Path(save_dir)\n"
            "if model_pref in {'best_first', 'best', 'best_reward'}:\n"
            "    candidates = [root / 'siedler_best_reward.zip', root / 'siedler_final.zip']\n"
            "else:\n"
            "    candidates = [root / 'siedler_final.zip', root / 'siedler_best_reward.zip']\n"
            "model_path = next((p for p in candidates if p.exists()), None)\n"
            "if model_path is None:\n"
            "    raise FileNotFoundError(\n"
            "        f'No model found in {root} (expected siedler_final.zip or siedler_best_reward.zip)'\n"
            "    )\n"
            "\n"
            "reward_profile = ct.get_train_profile(profile)['reward_profile']\n"
            "env = ct._create_env_instance(\n"
            "    player_id=1,\n"
            "    use_spatial_obs=use_spatial,\n"
            "    spatial_size=spatial_size,\n"
            "    reward_profile=reward_profile,\n"
            ")\n"
            "model = MaskablePPO.load(str(model_path), env=env, device=device)\n"
            "\n"
            "global_actions = Counter()\n"
            "episodes_out = []\n"
            "for ep in range(episodes):\n"
            "    obs, _ = env.reset(seed=7000 + ep)\n"
            "    total_reward = 0.0\n"
            "    done = False\n"
            "    step_count = 0\n"
            "    local_actions = Counter()\n"
            "    first_action_time = {}\n"
            "    scharf_growth_curve = []\n"
            "    prev_scharf = int(getattr(env, 'scharfschuetzen', 0))\n"
            "\n"
            "    while not done:\n"
            "        action_mask = env.get_action_mask()\n"
            "        action, _ = ct._predict_with_optional_mask(model, obs, action_mask)\n"
            "        obs, reward, terminated, truncated, info = env.step(action)\n"
            "        total_reward += float(reward)\n"
            "        step_count += 1\n"
            "        done = bool(terminated or truncated)\n"
            "\n"
            "        action_name = str((info or {}).get('action_name', 'unknown'))\n"
            "        local_actions[action_name] += 1\n"
            "        global_actions[action_name] += 1\n"
            "        if action_name not in first_action_time:\n"
            "            first_action_time[action_name] = int(getattr(env, 'current_time', 0))\n"
            "\n"
            "        current_scharf = int(getattr(env, 'scharfschuetzen', 0))\n"
            "        if current_scharf > prev_scharf:\n"
            "            scharf_growth_curve.append({\n"
            "                'time_sec': int(getattr(env, 'current_time', 0)),\n"
            "                'scharfschuetzen': current_scharf,\n"
            "            })\n"
            "            prev_scharf = current_scharf\n"
            "\n"
            "    action_history = env.get_action_history() if hasattr(env, 'get_action_history') else []\n"
            "    episodes_out.append({\n"
            "        'episode_index': int(ep + 1),\n"
            "        'reward': float(total_reward),\n"
            "        'steps': int(step_count),\n"
            "        'final_time_sec': int(getattr(env, 'current_time', 0)),\n"
            "        'final_scharfschuetzen': int(getattr(env, 'scharfschuetzen', 0)),\n"
            "        'local_top_actions': local_actions.most_common(12),\n"
            "        'first_action_time_sec': _to_jsonable(first_action_time),\n"
            "        'scharf_growth_curve': _to_jsonable(scharf_growth_curve),\n"
            "        'action_history_first_40': _to_jsonable(list(action_history)[:40]),\n"
            "        'final_resources': _to_jsonable(dict(getattr(env, 'resources', {}))),\n"
            "        'final_buildings': _to_jsonable({\n"
            "            k: int(v)\n"
            "            for k, v in dict(getattr(env, 'buildings', {})).items()\n"
            "            if int(v) > 0\n"
            "        }),\n"
            "    })\n"
            "\n"
            "env.close()\n"
            "rewards = [float(e['reward']) for e in episodes_out]\n"
            "scharfs = [int(e['final_scharfschuetzen']) for e in episodes_out]\n"
            "summary = {\n"
            "    'model_path': str(model_path),\n"
            "    'profile': profile,\n"
            "    'sim_mode': os.environ.get('SIEDLER_SIM_MODE'),\n"
            "    'episodes': int(episodes),\n"
            "    'reward_mean': float(np.mean(rewards)),\n"
            "    'reward_std': float(np.std(rewards)),\n"
            "    'scharfs_mean': float(np.mean(scharfs)),\n"
            "    'scharfs_max': int(np.max(scharfs)),\n"
            "    'scharfs_min': int(np.min(scharfs)),\n"
            "    'global_top_actions': global_actions.most_common(20),\n"
            "    'episodes_detail': _to_jsonable(episodes_out),\n"
            "}\n"
            "\n"
            "analysis_path = root / 'post_training_analysis.json'\n"
            "with open(analysis_path, 'w', encoding='utf-8') as f:\n"
            "    json.dump(summary, f, ensure_ascii=False, indent=2)\n"
            "\n"
            "print('=' * 72)\n"
            "print('POST-TRAINING ANALYSE')\n"
            "print('=' * 72)\n"
            "print(f'Model: {model_path}')\n"
            "print(f'Profile: {profile}')\n"
            "print(f'Episodes: {episodes}')\n"
            "print(f\"Reward mean/std: {summary['reward_mean']:.2f} / {summary['reward_std']:.2f}\")\n"
            "print(f\"Scharfs mean/max/min: {summary['scharfs_mean']:.2f} / {summary['scharfs_max']} / {summary['scharfs_min']}\")\n"
            "print(f\"Top actions overall: {summary['global_top_actions'][:10]}\")\n"
            "print(f'Saved analysis JSON: {analysis_path}')\n"
        )
        try:
            run(
                [sys.executable, "-u", "-c", post_analysis_code],
                env={
                    "SIEDLER_POST_ANALYSIS_EPISODES": str(POST_ANALYSIS_EPISODES),
                    "SIEDLER_POST_ANALYSIS_MODEL": str(POST_ANALYSIS_MODEL_PREF),
                },
            )
        except subprocess.CalledProcessError as exc:
            print(f"Post-analysis failed (non-fatal): {exc}")
