# -*- coding: utf-8 -*-
"""
Parse complete game data export from Siedler 5 log files.

Parses:
- Terrain data (height, blocking, sector, terrain type)
- Entity positions (trees, shafts, deposits, buildings, settlers)
- Player data (resources, HQ positions)
"""

import argparse
import glob
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

import numpy as np


DEFAULT_LOG_DIRS = [
    r"%USERPROFILE%\Documents\DIE SIEDLER - DEdK\Temp\Logs\Game",
    r"%USERPROFILE%\Documents\DIE SIEDLER - DEdK\Logs\Game",
    r"%USERPROFILE%\Documents\The Settlers 5\Temp\Logs\Game",
]


def expand_paths(paths: List[str]) -> List[str]:
    return [os.path.expandvars(p) for p in paths]


def find_latest_log(paths: List[str]) -> Optional[str]:
    candidates = []
    for base in expand_paths(paths):
        if not os.path.isdir(base):
            continue
        candidates.extend(glob.glob(os.path.join(base, "*.log")))
    if not candidates:
        return None
    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return candidates[0]


def strip_to_marker(line: str, marker: str) -> Optional[str]:
    idx = line.find(marker)
    if idx == -1:
        return None
    return line[idx:].strip()


class GameDataParser:
    def __init__(self):
        self.terrain_params = {}
        self.height_rows = []
        self.blocking_rows = []
        self.sector_rows = []
        self.terrain_rows = []
        self.y_values = []

        self.trees = []
        self.shafts = []
        self.deposits = []
        self.buildings = []
        self.settlers = []

        self.player_resources = {}
        self.player_hqs = {}
        self.map_name = "unknown"

    def parse_file(self, log_path: str):
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        in_terrain = False
        in_entities = False
        in_player_data = False

        for raw in lines:
            line = raw.strip()
            if not line:
                continue

            # Map name
            if "MAP_NAME," in line:
                parts = line.split(",", 1)
                if len(parts) > 1:
                    self.map_name = parts[1]

            # Terrain section
            start = strip_to_marker(line, "TERRAIN_EXPORT_START")
            if start:
                parts = start.split(",")
                if len(parts) >= 6:
                    self.terrain_params = {
                        "x_min": int(parts[1]),
                        "x_max": int(parts[2]),
                        "y_min": int(parts[3]),
                        "y_max": int(parts[4]),
                        "step": int(parts[5]),
                    }
                in_terrain = True
                continue

            if "TERRAIN_EXPORT_END" in line:
                in_terrain = False
                continue

            if in_terrain:
                self._parse_terrain_row(line)

            # Entity section
            if "ENTITY_EXPORT_START" in line:
                in_entities = True
                continue
            if "ENTITY_EXPORT_END" in line:
                in_entities = False
                continue

            if in_entities:
                self._parse_entity(line)

            # Player data section
            if "PLAYER_DATA_START" in line:
                in_player_data = True
                continue
            if "PLAYER_DATA_END" in line:
                in_player_data = False
                continue

            if in_player_data:
                self._parse_player_data(line)

    def _parse_terrain_row(self, line: str):
        if line.startswith("THEIGHT,"):
            parts = line.split(",")
            y = int(parts[1])
            if y not in self.y_values:
                self.y_values.append(y)
            self.height_rows.append([int(v) for v in parts[2:] if v])
        elif line.startswith("TBLOCK,"):
            parts = line.split(",")
            self.blocking_rows.append([int(v) for v in parts[2:] if v])
        elif line.startswith("TSECTOR,"):
            parts = line.split(",")
            self.sector_rows.append([int(v) for v in parts[2:] if v])
        elif line.startswith("TTERRAIN,"):
            parts = line.split(",")
            self.terrain_rows.append([int(v) for v in parts[2:] if v])

    def _parse_entity(self, line: str):
        if line.startswith("TREE,"):
            parts = line.split(",")
            if len(parts) >= 6:
                self.trees.append({
                    "id": int(parts[1]),
                    "x": float(parts[2]),
                    "y": float(parts[3]),
                    "amount": int(parts[4]),
                    "type": parts[5],
                })
        elif line.startswith("SHAFT,"):
            parts = line.split(",")
            if len(parts) >= 6:
                self.shafts.append({
                    "id": int(parts[1]),
                    "x": float(parts[2]),
                    "y": float(parts[3]),
                    "amount": int(parts[4]),
                    "resource": parts[5],
                })
        elif line.startswith("DEPOSIT,"):
            parts = line.split(",")
            if len(parts) >= 6:
                self.deposits.append({
                    "id": int(parts[1]),
                    "x": float(parts[2]),
                    "y": float(parts[3]),
                    "amount": int(parts[4]),
                    "resource": parts[5],
                })
        elif line.startswith("BUILDING,"):
            parts = line.split(",")
            if len(parts) >= 8:
                self.buildings.append({
                    "id": int(parts[1]),
                    "x": float(parts[2]),
                    "y": float(parts[3]),
                    "player": int(parts[4]),
                    "type": parts[5],
                    "hp": int(parts[6]),
                    "max_hp": int(parts[7]),
                })
        elif line.startswith("SETTLER,"):
            parts = line.split(",")
            if len(parts) >= 6:
                self.settlers.append({
                    "id": int(parts[1]),
                    "x": float(parts[2]),
                    "y": float(parts[3]),
                    "player": int(parts[4]),
                    "type": parts[5],
                })

    def _parse_player_data(self, line: str):
        if line.startswith("PLAYER_RES,"):
            parts = line.split(",")
            if len(parts) >= 8:
                player = int(parts[1])
                self.player_resources[player] = {
                    "gold": int(parts[2]),
                    "clay": int(parts[3]),
                    "wood": int(parts[4]),
                    "stone": int(parts[5]),
                    "iron": int(parts[6]),
                    "sulfur": int(parts[7]),
                }
        elif line.startswith("PLAYER_HQ,"):
            parts = line.split(",")
            if len(parts) >= 4:
                player = int(parts[1])
                self.player_hqs[player] = {
                    "x": float(parts[2]),
                    "y": float(parts[3]),
                }

    def build_terrain_grids(self) -> Dict[str, np.ndarray]:
        grids = {}

        if self.height_rows:
            max_len = max(len(r) for r in self.height_rows)
            grid = np.full((len(self.height_rows), max_len), -1, dtype=np.int16)
            for i, r in enumerate(self.height_rows):
                grid[i, :len(r)] = np.array(r, dtype=np.int16)
            grids["height"] = grid

        if self.blocking_rows:
            max_len = max(len(r) for r in self.blocking_rows)
            grid = np.full((len(self.blocking_rows), max_len), -1, dtype=np.int16)
            for i, r in enumerate(self.blocking_rows):
                grid[i, :len(r)] = np.array(r, dtype=np.int16)
            grids["blocking"] = grid

        if self.sector_rows:
            max_len = max(len(r) for r in self.sector_rows)
            grid = np.full((len(self.sector_rows), max_len), -1, dtype=np.int16)
            for i, r in enumerate(self.sector_rows):
                grid[i, :len(r)] = np.array(r, dtype=np.int16)
            grids["sector"] = grid

        if self.terrain_rows:
            max_len = max(len(r) for r in self.terrain_rows)
            grid = np.full((len(self.terrain_rows), max_len), -1, dtype=np.int16)
            for i, r in enumerate(self.terrain_rows):
                grid[i, :len(r)] = np.array(r, dtype=np.int16)
            grids["terrain_type"] = grid

        return grids

    def get_entities_by_player(self, player: int) -> Dict[str, List]:
        """Get all entities for a specific player."""
        return {
            "buildings": [b for b in self.buildings if b["player"] == player],
            "settlers": [s for s in self.settlers if s["player"] == player],
        }

    def get_resources_near(self, x: float, y: float, radius: float = 5000) -> Dict[str, List]:
        """Get resources within radius of a position."""
        def dist(e):
            return ((e["x"] - x) ** 2 + (e["y"] - y) ** 2) ** 0.5

        return {
            "trees": sorted([t for t in self.trees if dist(t) < radius], key=dist),
            "shafts": sorted([s for s in self.shafts if dist(s) < radius], key=dist),
            "deposits": sorted([d for d in self.deposits if dist(d) < radius], key=dist),
        }


def save_outputs(parser: GameDataParser, out_dir: str, prefix: str = "game_export"):
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # Save terrain grids
    grids = parser.build_terrain_grids()
    for name, grid in grids.items():
        np.save(out_path / f"{prefix}_{name}.npy", grid)
        print(f"Saved: {prefix}_{name}.npy ({grid.shape})")

    # Save entities as JSON
    entities = {
        "map_name": parser.map_name,
        "terrain_params": parser.terrain_params,
        "trees": parser.trees,
        "shafts": parser.shafts,
        "deposits": parser.deposits,
        "buildings": parser.buildings,
        "settlers": parser.settlers,
        "player_resources": parser.player_resources,
        "player_hqs": parser.player_hqs,
    }

    json_path = out_path / f"{prefix}_entities.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(entities, f, indent=2, ensure_ascii=False)
    print(f"Saved: {json_path}")

    # Summary report
    report = {
        "map_name": parser.map_name,
        "terrain": parser.terrain_params,
        "terrain_grid_shape": grids["blocking"].shape if "blocking" in grids else None,
        "tree_count": len(parser.trees),
        "shaft_count": len(parser.shafts),
        "deposit_count": len(parser.deposits),
        "building_count": len(parser.buildings),
        "settler_count": len(parser.settlers),
        "players": list(parser.player_hqs.keys()),
    }

    report_path = out_path / f"{prefix}_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Saved: {report_path}")

    return report


def compare_with_environment(parser: GameDataParser, env_config_path: str = None):
    """Compare exported data with environment.py configuration."""
    print("\n=== VERGLEICH MIT ENVIRONMENT ===\n")

    # Player 1 data
    if 1 in parser.player_hqs:
        hq = parser.player_hqs[1]
        print(f"Player 1 HQ Position: ({hq['x']:.0f}, {hq['y']:.0f})")

    # Resources
    if 1 in parser.player_resources:
        res = parser.player_resources[1]
        print(f"Player 1 Start-Ressourcen: Gold={res['gold']}, Clay={res['clay']}, Wood={res['wood']}, Stone={res['stone']}, Iron={res['iron']}, Sulfur={res['sulfur']}")

    # Trees
    p1_trees = [t for t in parser.trees if 25000 < t['x'] < 51000 and 0 < t['y'] < 25500]
    print(f"\nBäume im Player 1 Quadrant: {len(p1_trees)}")
    if p1_trees:
        total_wood = sum(t['amount'] for t in p1_trees)
        print(f"Gesamtes Holz verfügbar: {total_wood}")

    # Shafts by type
    print("\nStollen (Shafts):")
    for res_type in ["Iron", "Stone", "Clay", "Sulfur"]:
        shafts = [s for s in parser.shafts if s['resource'] == res_type]
        if shafts:
            print(f"  {res_type}: {len(shafts)} Stollen")
            for s in shafts[:3]:
                print(f"    - ({s['x']:.0f}, {s['y']:.0f}) - {s['amount']} Einheiten")

    # Deposits
    print("\nVorkommen (Deposits):")
    for res_type in ["Iron", "Stone", "Clay", "Sulfur"]:
        deps = [d for d in parser.deposits if d['resource'] == res_type]
        if deps:
            print(f"  {res_type}: {len(deps)} Vorkommen")
            for d in deps[:3]:
                print(f"    - ({d['x']:.0f}, {d['y']:.0f}) - {d['amount']} Einheiten")

    # Buildings by player
    print("\nGebäude pro Spieler:")
    for player in range(1, 5):
        blds = [b for b in parser.buildings if b['player'] == player]
        if blds:
            print(f"  Spieler {player}: {len(blds)} Gebäude")
            types = {}
            for b in blds:
                types[b['type']] = types.get(b['type'], 0) + 1
            for t, c in sorted(types.items(), key=lambda x: -x[1])[:5]:
                print(f"    - {t}: {c}")


def main():
    parser = argparse.ArgumentParser(description="Parse Siedler 5 game data export.")
    parser.add_argument("--log", default=None, help="Path to log file")
    parser.add_argument("--out", default="map_extract", help="Output directory")
    parser.add_argument("--prefix", default="game_export", help="Output file prefix")
    parser.add_argument("--compare", action="store_true", help="Compare with environment")
    args = parser.parse_args()

    log_path = args.log or find_latest_log(DEFAULT_LOG_DIRS)

    if not log_path or not os.path.isfile(log_path):
        print("Kein Log gefunden. Verwende --log oder starte erst das Spiel mit Export.")
        return

    print(f"Parsing: {log_path}\n")

    game_parser = GameDataParser()
    game_parser.parse_file(log_path)

    if not game_parser.terrain_params and not game_parser.trees:
        print("Keine Export-Daten im Log gefunden!")
        print("Stelle sicher dass der Export im Spiel gelaufen ist.")
        return

    report = save_outputs(game_parser, args.out, args.prefix)

    print(f"\n=== ZUSAMMENFASSUNG ===")
    print(f"Map: {report['map_name']}")
    print(f"Terrain Grid: {report['terrain_grid_shape']}")
    print(f"Bäume: {report['tree_count']}")
    print(f"Stollen: {report['shaft_count']}")
    print(f"Vorkommen: {report['deposit_count']}")
    print(f"Gebäude: {report['building_count']}")
    print(f"Siedler: {report['settler_count']}")

    if args.compare:
        compare_with_environment(game_parser)


if __name__ == "__main__":
    main()
