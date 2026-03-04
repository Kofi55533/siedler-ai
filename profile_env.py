# -*- coding: utf-8 -*-
"""
Siedler AI - Environment Performance Profiler

Misst welche Funktionen wie viel Zeit benoetigen.
Ausfuehren:  python profile_env.py
Oder mit mehr Steps: python profile_env.py 2000
"""

import cProfile
import io
import os
import pstats
import sys
import time

# Fast-Train Modus setzen (wie beim echten Training)
os.environ.setdefault("SIEDLER_FAST_TRAIN", "1")
os.environ.setdefault("SIEDLER_DISABLE_RUNTIME_PATHING", "1")
os.environ.setdefault("SIEDLER_USE_SPATIAL", "0")
os.environ.setdefault("SIEDLER_TRAIN_PROFILE", "legacy")

PROFILE_STEPS = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
TOP_N = 25  # Top N Funktionen anzeigen
BAR_WIDTH = 30


def _bar(fraction: float) -> str:
    filled = int(fraction * BAR_WIDTH)
    return "#" * filled + "." * (BAR_WIDTH - filled)


def run_steps(env, n_steps: int):
    """Fuehrt n_steps env.step()-Aufrufe durch (mit zufaelliger gueltiger Aktion)."""
    import numpy as np
    obs, _ = env.reset()
    for _ in range(n_steps):
        mask = env.action_masks()
        valid = np.where(mask)[0]
        action = int(np.random.choice(valid))
        obs, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            obs, _ = env.reset()


def main():
    print("=" * 60)
    print("SIEDLER AI — Environment Profiler")
    print(f"Steps: {PROFILE_STEPS}")
    print("=" * 60)

    # Environment erstellen
    print("Lade Environment...")
    t0 = time.perf_counter()
    from environment import SiedlerScharfschuetzenEnv
    env = SiedlerScharfschuetzenEnv(player_id=1, use_spatial_obs=False)
    env.reset(seed=42)
    load_time = time.perf_counter() - t0
    print(f"Environment geladen in {load_time:.1f}s\n")

    # Warmup (nicht gemessen)
    print("Warmup (100 Steps)...")
    import numpy as np
    for _ in range(100):
        mask = env.action_masks()
        valid = np.where(mask)[0]
        action = int(np.random.choice(valid))
        _, _, term, trunc, _ = env.step(action)
        if term or trunc:
            env.reset()

    # Profiling
    print(f"Profiling {PROFILE_STEPS} Steps...\n")
    pr = cProfile.Profile()

    t_start = time.perf_counter()
    pr.enable()
    run_steps(env, PROFILE_STEPS)
    pr.disable()
    elapsed = time.perf_counter() - t_start

    fps = PROFILE_STEPS / elapsed
    ms_per_step = elapsed / PROFILE_STEPS * 1000

    print("=" * 60)
    print(f"  FPS:          {fps:.1f}")
    print(f"  Gesamt:       {elapsed:.2f}s")
    print(f"  Pro Step:     {ms_per_step:.3f}ms")
    print("=" * 60)

    # Stats auswerten
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
    ps.print_stats(TOP_N)
    raw = s.getvalue()

    # Relevante Zeilen filtern (siedler-eigene Dateien + grosse Kostenstellen)
    keywords = [
        "environment", "production_system", "worker_simulation",
        "pathfinding", "map_config", "multihead_policy",
    ]

    lines = raw.split("\n")
    header_done = False
    results = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Header-Zeilen (ncalls, tottime, ...) einmalig uebernehmen
        if "ncalls" in stripped and not header_done:
            header_done = True
            continue
        # Nur Zeilen mit Zahlenwerten und relevanten Dateien
        parts = stripped.split()
        if len(parts) >= 6:
            try:
                cumtime = float(parts[3])
                if cumtime < 0.005:
                    continue
                # Alle Zeilen mit Zeit > 5ms behalten
                results.append((cumtime, stripped))
            except (ValueError, IndexError):
                pass

    # Nach cumtime sortieren
    results.sort(key=lambda x: -x[0])
    total_time = elapsed

    print(f"\nTop {min(TOP_N, len(results))} Funktionen nach kumulativer Zeit:\n")
    print(f"  {'Zeit':>7}  {'Anteil':>6}  {'Balken':<{BAR_WIDTH}}  Funktion")
    print("  " + "-" * (7 + 6 + BAR_WIDTH + 20))

    for cumtime, line in results[:TOP_N]:
        parts = line.split()
        if len(parts) < 6:
            continue
        frac = min(cumtime / total_time, 1.0)
        # Funktionsname aus letztem Teil extrahieren
        func_part = " ".join(parts[5:]) if len(parts) > 5 else line
        # Kurzen Namen extrahieren
        if "{" in func_part:
            fname = func_part
        else:
            fname = func_part.split("/")[-1] if "/" in func_part else func_part
            fname = fname.split("\\")[-1] if "\\" in fname else fname

        print(f"  {cumtime:>6.3f}s  {frac*100:>5.1f}%  {_bar(frac)}  {fname}")

    # Breakdown nach Kategorien
    print("\n")
    print("=" * 60)
    print("Kategorie-Breakdown (geschaetzt aus cProfile):\n")

    category_times = {}
    for cumtime, line in results:
        for kw in keywords:
            if kw in line.lower():
                category_times[kw] = category_times.get(kw, 0) + cumtime
                break

    # Deduplizieren (groesste Funktion einer Datei zaehlt)
    # Stattdessen: tottime statt cumtime summieren
    s2 = io.StringIO()
    ps2 = pstats.Stats(pr, stream=s2).sort_stats("tottime")
    ps2.print_stats(200)
    raw2 = s2.getvalue()

    cat_tottime = {}
    for line in raw2.split("\n"):
        parts = line.strip().split()
        if len(parts) < 6:
            continue
        try:
            tottime = float(parts[1])
            fname = " ".join(parts[5:]).lower()
            for kw in keywords:
                if kw in fname:
                    cat_tottime[kw] = cat_tottime.get(kw, 0) + tottime
                    break
        except (ValueError, IndexError):
            pass

    if cat_tottime:
        cat_total = sum(cat_tottime.values())
        for kw, t in sorted(cat_tottime.items(), key=lambda x: -x[1]):
            frac = t / total_time
            print(f"  {kw:<25} {t:>6.3f}s  {frac*100:>5.1f}%  {_bar(frac)}")

    print("\n" + "=" * 60)
    print("Tipp: Speichere Profil-Daten mit:")
    print("  import cProfile; cProfile.run('...', 'profile.prof')")
    print("  snakeviz profile.prof")
    print("=" * 60)


if __name__ == "__main__":
    main()
