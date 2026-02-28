# -*- coding: utf-8 -*-
"""
Vergleicht exportierte Spieldaten mit environment.py Konfiguration.
Bei fehlenden Export-Dateien wird optional automatisch aus dem neuesten Spiel-Log geparst.
"""

import argparse
import json
import os
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


P1_X_MIN = 25000.0
P1_X_MAX = 51000.0
P1_Y_MIN = 0.0
P1_Y_MAX = 25500.0


def _is_in_player1_quadrant(entity: Dict[str, Any]) -> bool:
    x = float(entity.get("x", 0.0))
    y = float(entity.get("y", 0.0))
    return P1_X_MIN < x < P1_X_MAX and P1_Y_MIN < y < P1_Y_MAX


def _tree_xy(tree: Dict[str, Any]) -> Optional[Tuple[float, float]]:
    if not isinstance(tree, dict):
        return None
    if "x" in tree and "y" in tree:
        try:
            return float(tree.get("x", 0.0)), float(tree.get("y", 0.0))
        except (TypeError, ValueError):
            return None
    pos = tree.get("position")
    if isinstance(pos, dict) and "x" in pos and "y" in pos:
        try:
            return float(pos.get("x", 0.0)), float(pos.get("y", 0.0))
        except (TypeError, ValueError):
            return None
    return None


def _load_runtime_trees_from_resources(resources_file: str, allowed_types: set[str]) -> List[Dict[str, Any]]:
    if not resources_file or not os.path.exists(resources_file):
        return []
    try:
        with open(resources_file, "r", encoding="utf-8") as f:
            resources_data = json.load(f)
    except Exception:
        return []

    trees_all = resources_data.get("trees_all") or []
    runtime_trees: List[Dict[str, Any]] = []
    for tree in trees_all:
        if not isinstance(tree, dict):
            continue
        tree_type = str(tree.get("type", "")).strip()
        if allowed_types and tree_type not in allowed_types:
            continue
        try:
            amount = int(tree.get("amount", 0) or 0)
        except (TypeError, ValueError):
            amount = 0
        if amount <= 0:
            continue
        coords = _tree_xy(tree)
        if coords is None:
            continue
        x, y = coords
        if not (P1_X_MIN < x < P1_X_MAX and P1_Y_MIN < y < P1_Y_MAX):
            continue
        runtime_trees.append({"x": x, "y": y, "type": tree_type, "amount": amount})
    return runtime_trees


def _load_runtime_trees_from_map_data(base_dir: str, allowed_types: set[str]) -> List[Dict[str, Any]]:
    candidates = []
    if base_dir:
        candidates.append(os.path.join(base_dir, "config", "wintersturm_map_data.json"))
    candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "wintersturm_map_data.json"))

    for map_data_file in candidates:
        if not map_data_file or not os.path.exists(map_data_file):
            continue
        try:
            with open(map_data_file, "r", encoding="utf-8") as f:
                map_data = json.load(f)
        except Exception:
            continue
        trees = map_data.get("trees", [])
        runtime_trees: List[Dict[str, Any]] = []
        for tree in trees:
            if not isinstance(tree, dict):
                continue
            tree_type = str(tree.get("type", "")).strip()
            if allowed_types and tree_type not in allowed_types:
                continue
            coords = _tree_xy(tree)
            if coords is None:
                continue
            x, y = coords
            if not (P1_X_MIN < x < P1_X_MAX and P1_Y_MIN < y < P1_Y_MAX):
                continue
            runtime_trees.append({"x": x, "y": y, "type": tree_type})
        if runtime_trees:
            return runtime_trees
    return []


def _latest_file(paths: List[Path]) -> Optional[Path]:
    if not paths:
        return None
    return max(paths, key=lambda p: p.stat().st_mtime)


def _collect_export_files(export_dir: Path) -> Dict[str, Any]:
    entities_files = list(export_dir.rglob("*_entities.json"))
    entities_file = _latest_file(entities_files)
    if entities_file is None:
        return {}

    prefix = entities_file.name[: -len("_entities.json")]
    parent = entities_file.parent

    npy_files: Dict[str, Optional[Path]] = {}
    for name in ("blocking", "height", "sector", "terrain_type"):
        exact = parent / f"{prefix}_{name}.npy"
        if exact.exists():
            npy_files[name] = exact
            continue
        candidates = list(export_dir.rglob(f"*_{name}.npy"))
        npy_files[name] = _latest_file(candidates)

    return {
        "entities_file": entities_file,
        "prefix": prefix,
        "npy_files": npy_files,
    }


def _try_auto_parse(export_dir: Path, log_path: Optional[str]) -> Optional[Dict[str, str]]:
    """Versucht fehlende Exportdaten direkt aus dem neuesten Log zu erzeugen."""
    try:
        from parse_game_export import (
            DEFAULT_LOG_DIRS,
            GameDataParser,
            find_latest_log,
            save_outputs,
        )
    except Exception as exc:
        print(f"Warnung: parse_game_export Import fehlgeschlagen: {exc}")
        return None

    selected_log = log_path or find_latest_log(DEFAULT_LOG_DIRS)
    if not selected_log:
        return None

    parser = GameDataParser()
    parser.parse_file(selected_log)

    has_data = bool(parser.terrain_params or parser.trees or parser.shafts or parser.deposits or parser.buildings)
    if not has_data:
        return None

    export_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"live_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    save_outputs(parser, str(export_dir), prefix=prefix)
    return {"log": selected_log, "prefix": prefix}


def load_export_data(
    export_dir: str = "map_extract",
    auto_parse: bool = True,
    log_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Lädt Exportdaten; optional mit automatischer Live-Log-Extraktion."""
    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)

    data: Dict[str, Any] = {
        "entities": None,
        "blocking": None,
        "height": None,
        "sector": None,
        "terrain_type": None,
        "_meta": {},
    }

    files = _collect_export_files(export_path)
    if not files and auto_parse:
        parse_info = _try_auto_parse(export_path, log_path)
        if parse_info:
            print(f"Auto-Parse erfolgreich: {parse_info['log']}")
            files = _collect_export_files(export_path)
            data["_meta"]["auto_parsed"] = parse_info

    if not files:
        return data

    entities_file: Path = files["entities_file"]
    with open(entities_file, "r", encoding="utf-8") as f:
        data["entities"] = json.load(f)
    data["_meta"]["entities_file"] = str(entities_file)
    data["_meta"]["prefix"] = files["prefix"]

    npy_files: Dict[str, Optional[Path]] = files["npy_files"]
    for name, npy_file in npy_files.items():
        if npy_file and npy_file.exists():
            data[name] = np.load(npy_file)
            data["_meta"][f"{name}_file"] = str(npy_file)

    return data


def load_env_config() -> Dict[str, Any]:
    """Lädt relevante Konfiguration aus map_config_wintersturm.py/environment.py."""
    config: Dict[str, Any] = {}

    try:
        from map_config_wintersturm import (
            PLAYER_HQ_POSITIONS,
            PLAYER_1_MINE_SHAFTS,
            PLAYER_1_DEPOSITS,
            PLAYER_1_TREES_NEAREST,
            PLAYER_1_TREES_SUMMARY,
            START_RESOURCES as MAP_START_RESOURCES,
        )
        config["hq_positions"] = PLAYER_HQ_POSITIONS
        config["mine_shafts"] = PLAYER_1_MINE_SHAFTS
        config["deposits"] = PLAYER_1_DEPOSITS
        config["trees"] = PLAYER_1_TREES_NEAREST
        config["tree_summary"] = PLAYER_1_TREES_SUMMARY
        config["start_resources_map"] = MAP_START_RESOURCES
    except ImportError as exc:
        print(f"Warnung: map_config_wintersturm.py unvollstaendig: {exc}")

    tree_summary = config.get("tree_summary") or {}
    expected_tree_types: set[str] = set()
    summary_types = tree_summary.get("tree_types", {}) if isinstance(tree_summary, dict) else {}
    if isinstance(summary_types, dict):
        expected_tree_types = {
            str(tree_type).strip()
            for tree_type, count in summary_types.items()
            if int(count or 0) > 0
        }

    try:
        from environment import HARVESTABLE_TREE_TYPES, START_RESOURCES as ENV_START_RESOURCES
        config["start_resources"] = ENV_START_RESOURCES
        config["harvestable_tree_types"] = set(HARVESTABLE_TREE_TYPES)
    except ImportError:
        pass

    if not expected_tree_types:
        expected_tree_types = set(config.get("harvestable_tree_types") or [])
    config["resource_tree_types"] = set(expected_tree_types)

    base_dir = os.environ.get("SIEDLER_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
    resources_file = os.path.join(base_dir, "player1_resources.json")
    runtime_trees = _load_runtime_trees_from_resources(resources_file, set(expected_tree_types))
    if runtime_trees:
        config["runtime_tree_count"] = len(runtime_trees)
        config["runtime_tree_types"] = dict(Counter(t.get("type", "") for t in runtime_trees))
    else:
        map_data_trees = _load_runtime_trees_from_map_data(base_dir, set(expected_tree_types))
        if map_data_trees:
            config["runtime_tree_count"] = len(map_data_trees)
            config["runtime_tree_types"] = dict(Counter(t.get("type", "") for t in map_data_trees))

    return config


def _env_pos_to_xy(pos: Any) -> Tuple[float, float]:
    if isinstance(pos, dict):
        return float(pos.get("x", 0.0)), float(pos.get("y", 0.0))
    if isinstance(pos, (list, tuple)) and len(pos) >= 2:
        return float(pos[0]), float(pos[1])
    return 0.0, 0.0


def _get_env_resource_value(env_resources: Dict[str, Any], game_key: str) -> float:
    candidates = {
        "gold": ["Taler", "GoldRoh", "Gold"],
        "clay": ["Lehm", "LehmRoh", "Clay"],
        "wood": ["Holz", "HolzRoh", "Wood"],
        "stone": ["Stein", "SteinRoh", "Stone"],
        "iron": ["Eisen", "EisenRoh", "Iron"],
        "sulfur": ["Schwefel", "SchwefelRoh", "Sulfur"],
    }.get(game_key, [])

    for key in candidates:
        if key in env_resources:
            return float(env_resources.get(key, 0))
    return 0.0


def compare_hq_positions(export_data: Dict[str, Any], env_config: Dict[str, Any]) -> List[str]:
    issues: List[str] = []

    if not export_data.get("entities"):
        return ["Keine Entity-Daten exportiert"]

    player_hqs = export_data["entities"].get("player_hqs", {})
    env_hqs = env_config.get("hq_positions", {})

    for player, pos in player_hqs.items():
        player_int = int(player)
        if player_int not in env_hqs:
            issues.append(f"HQ Player {player}: im Spiel vorhanden, aber nicht in env_config")
            continue

        ex, ey = _env_pos_to_xy(env_hqs[player_int])
        gx = float(pos.get("x", 0))
        gy = float(pos.get("y", 0))
        dx = abs(gx - ex)
        dy = abs(gy - ey)
        if dx > 100 or dy > 100:
            issues.append(
                f"HQ Player {player}: Spiel=({gx:.0f},{gy:.0f}) vs Env=({ex:.0f},{ey:.0f}) "
                f"Abweichung=({dx:.0f},{dy:.0f})"
            )
        else:
            print(f"OK HQ Player {player}: ({gx:.0f}, {gy:.0f})")

    return issues


def compare_resources(export_data: Dict[str, Any], env_config: Dict[str, Any]) -> List[str]:
    issues: List[str] = []

    if not export_data.get("entities"):
        return ["Keine Entity-Daten exportiert"]

    player_res = export_data["entities"].get("player_resources", {})
    env_res = env_config.get("start_resources") or env_config.get("start_resources_map") or {}
    game_res = player_res.get("1") or player_res.get(1)

    if not game_res:
        return issues

    keys = ("gold", "clay", "wood", "stone", "iron", "sulfur")
    if all(float(game_res.get(k, 0)) == 0.0 for k in keys):
        print("Hinweis: Player-1 Ressourcen im Export sind alle 0; Startressourcen-Vergleich wird uebersprungen.")
        return issues

    for game_key in keys:
        game_val = float(game_res.get(game_key, 0))
        env_val = _get_env_resource_value(env_res, game_key)
        if game_val != env_val:
            issues.append(f"Ressource {game_key}: Spiel={game_val:.0f} vs Env={env_val:.0f}")
        else:
            print(f"OK {game_key}: {game_val:.0f}")

    return issues


def compare_trees(export_data: Dict[str, Any], env_config: Dict[str, Any]) -> List[str]:
    issues: List[str] = []

    if not export_data.get("entities"):
        return ["Keine Entity-Daten exportiert"]

    trees = export_data["entities"].get("trees", [])
    p1_trees = [t for t in trees if _is_in_player1_quadrant(t)]
    print(f"\nBaeume im Player-1-Quadrant: {len(p1_trees)}")

    if p1_trees:
        wood_amounts = [int(t.get("amount", 0)) for t in p1_trees if int(t.get("amount", 0)) > 0]
        if wood_amounts:
            avg_wood = sum(wood_amounts) / len(wood_amounts)
            print(f"Holz pro Baum: min={min(wood_amounts)}, max={max(wood_amounts)}, avg={avg_wood:.1f}")
            if avg_wood < 70 or avg_wood > 80:
                issues.append(f"Holz pro Baum: Spiel avg={avg_wood:.1f}, erwartet ~75")
            print(f"Gesamtholz gescannt: {sum(wood_amounts)}")

    tree_summary = env_config.get("tree_summary") or {}
    expected_count = int(env_config.get("runtime_tree_count", 0) or tree_summary.get("total_trees", 0))
    if expected_count > 0:
        strict_runtime_trees = bool(env_config.get("runtime_tree_count"))
        if strict_runtime_trees:
            print(f"Env erwartete Baumanzahl (harvestable runtime): {expected_count}")
        else:
            print(f"Env erwartete Baumanzahl: {expected_count}")
        tolerance = 0 if strict_runtime_trees else 50
        if abs(len(p1_trees) - expected_count) > tolerance:
            issues.append(f"Baum-Anzahl: Spiel={len(p1_trees)} vs Env={expected_count}")

    game_tree_types = Counter(str(t.get("type", "")).strip() for t in p1_trees)
    expected_tree_types = tree_summary.get("tree_types") if isinstance(tree_summary, dict) else None
    if not expected_tree_types:
        expected_tree_types = env_config.get("runtime_tree_types")
    if isinstance(expected_tree_types, dict) and expected_tree_types:
        print("Baumtypen (Spiel):", dict(game_tree_types))
        print("Baumtypen (Env):", dict(expected_tree_types))
        for tree_type, expected_value in expected_tree_types.items():
            try:
                expected_int = int(expected_value)
            except (TypeError, ValueError):
                continue
            game_count = int(game_tree_types.get(str(tree_type).strip(), 0))
            if game_count != expected_int:
                issues.append(f"Baumtyp {tree_type}: Spiel={game_count} vs Env={expected_int}")

        unexpected_types = sorted(
            tree_type for tree_type, count in game_tree_types.items()
            if count > 0 and tree_type not in expected_tree_types
        )
        if unexpected_types:
            issues.append(f"Unerwartete Baumtypen im Spiel-Export: {', '.join(unexpected_types)}")

    return issues


def _normalize_res_name(name: str) -> str:
    value = str(name).strip().lower()
    mapping = {
        "iron": "eisen",
        "stone": "stein",
        "clay": "lehm",
        "sulfur": "schwefel",
        "eisen": "eisen",
        "stein": "stein",
        "lehm": "lehm",
        "schwefel": "schwefel",
    }
    return mapping.get(value, value)


def compare_shafts_and_deposits(export_data: Dict[str, Any], env_config: Dict[str, Any]) -> List[str]:
    issues: List[str] = []

    if not export_data.get("entities"):
        return ["Keine Entity-Daten exportiert"]

    all_shafts = export_data["entities"].get("shafts", [])
    all_deposits = export_data["entities"].get("deposits", [])
    shafts = [s for s in all_shafts if _is_in_player1_quadrant(s)]
    deposits = [d for d in all_deposits if _is_in_player1_quadrant(d)]
    print(
        f"\nPlayer-1-Quadrant Filter: "
        f"shafts={len(shafts)}/{len(all_shafts)}, deposits={len(deposits)}/{len(all_deposits)}"
    )

    print("\n=== STOLLEN ===")
    shaft_count_game: Dict[str, int] = {}
    for shaft in shafts:
        key = _normalize_res_name(shaft.get("resource", ""))
        shaft_count_game[key] = shaft_count_game.get(key, 0) + 1

    env_shafts = env_config.get("mine_shafts", {})
    shaft_count_env = { _normalize_res_name(k.replace("mine", "").replace("Mine", "")): len(v) for k, v in env_shafts.items() }

    for key in sorted(set(shaft_count_game) | set(shaft_count_env)):
        gv = shaft_count_game.get(key, 0)
        ev = shaft_count_env.get(key, 0)
        print(f"{key}: Spiel={gv}, Env={ev}")
        if gv != ev:
            issues.append(f"Stollen-Anzahl {key}: Spiel={gv} vs Env={ev}")

    print("\n=== VORKOMMEN ===")
    dep_count_game: Dict[str, int] = {}
    dep_amount_game: Dict[str, int] = {}
    for dep in deposits:
        key = _normalize_res_name(dep.get("resource", ""))
        dep_count_game[key] = dep_count_game.get(key, 0) + 1
        dep_amount_game[key] = dep_amount_game.get(key, 0) + int(dep.get("amount", 0))

    env_deposits = env_config.get("deposits", {})
    dep_count_env: Dict[str, int] = {}
    dep_amount_env: Dict[str, int] = {}
    for key, dep_list in env_deposits.items():
        norm = _normalize_res_name(key)
        dep_count_env[norm] = len(dep_list)
        dep_amount_env[norm] = sum(int(dep.get("amount", 0)) for dep in dep_list)

    for key in sorted(set(dep_count_game) | set(dep_count_env)):
        gc = dep_count_game.get(key, 0)
        ec = dep_count_env.get(key, 0)
        ga = dep_amount_game.get(key, 0)
        ea = dep_amount_env.get(key, 0)
        print(f"{key}: Spiel count={gc}, Env count={ec}, Spiel amount={ga}, Env amount={ea}")
        if gc != ec:
            issues.append(f"Vorkommen-Anzahl {key}: Spiel={gc} vs Env={ec}")
        if ga != ea:
            issues.append(f"Vorkommen-Menge {key}: Spiel={ga} vs Env={ea}")

    return issues


def compare_buildings(export_data: Dict[str, Any]) -> List[str]:
    issues: List[str] = []

    if not export_data.get("entities"):
        return ["Keine Entity-Daten exportiert"]

    buildings = export_data["entities"].get("buildings", [])
    print("\n=== GEBAEUDE PRO SPIELER ===")
    for player in range(1, 5):
        player_blds = [b for b in buildings if int(b.get("player", -1)) == player]
        if player_blds:
            print(f"Spieler {player}: {len(player_blds)} Gebaeude")
    return issues


def analyze_terrain(export_data: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    print("\n=== TERRAIN ANALYSE ===")

    if export_data.get("blocking") is not None:
        blocking = export_data["blocking"]
        print(f"Blocking Grid: {blocking.shape}")
        unique, counts = np.unique(blocking, return_counts=True)
        for v, c in zip(unique, counts):
            pct = 100 * c / blocking.size
            print(f"  value={v}: {c} ({pct:.1f}%)")

    if export_data.get("height") is not None:
        height = export_data["height"]
        print(f"Height Grid: {height.shape}, min={height.min()}, max={height.max()}, mean={height.mean():.1f}")

    if export_data.get("sector") is not None:
        sector = export_data["sector"]
        print(f"Sector Grid: {sector.shape}, unique={len(np.unique(sector))}")

    if export_data.get("terrain_type") is not None:
        terrain = export_data["terrain_type"]
        print(f"Terrain-Type Grid: {terrain.shape}, unique={len(np.unique(terrain))}")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Vergleich: Spiel-Export vs Environment")
    parser.add_argument("--export-dir", default="map_extract", help="Ordner mit *_entities.json und *_*.npy")
    parser.add_argument("--log", default=None, help="Optionaler Pfad zur .log-Datei fuer Auto-Parse")
    parser.add_argument("--no-auto-parse", action="store_true", help="Kein automatisches Parsen aus Logs")
    args = parser.parse_args()

    print("=" * 60)
    print("VERGLEICH: SPIEL-EXPORT vs ENVIRONMENT")
    print("=" * 60)

    export_data = load_export_data(
        export_dir=args.export_dir,
        auto_parse=not args.no_auto_parse,
        log_path=args.log,
    )
    env_config = load_env_config()

    if export_data.get("_meta"):
        print("\nVerwendete Export-Dateien:")
        for key, value in export_data["_meta"].items():
            print(f"  {key}: {value}")

    if not export_data.get("entities") and export_data.get("blocking") is None:
        print("\nKeine Export-Daten gefunden.")
        print("Loesung:")
        print("1. Spiel-Export im laufenden Match ausfuehren (Lua/S5Hook).")
        print("2. Danach dieses Script erneut starten (oder --log <datei.log> angeben).")
        print("3. Alternativ manuell: python parse_game_export.py --compare")
        return

    all_issues: List[str] = []
    all_issues.extend(compare_hq_positions(export_data, env_config))
    all_issues.extend(compare_resources(export_data, env_config))
    all_issues.extend(compare_trees(export_data, env_config))
    all_issues.extend(compare_shafts_and_deposits(export_data, env_config))
    all_issues.extend(compare_buildings(export_data))
    all_issues.extend(analyze_terrain(export_data))

    print("\n" + "=" * 60)
    print("ZUSAMMENFASSUNG")
    print("=" * 60)
    if all_issues:
        print(f"\n{len(all_issues)} Abweichungen gefunden:")
        for issue in all_issues:
            print(f"  - {issue}")
    else:
        print("\nKeine relevanten Abweichungen gefunden.")


if __name__ == "__main__":
    main()
