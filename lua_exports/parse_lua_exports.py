# -*- coding: utf-8 -*-
"""
Parser für Lua Export Daten aus Game.log
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any


def parse_pathfinding_export(log_path: Path) -> Dict[str, Any]:
    """Parst PATHFINDING_EXPORT aus Game.log"""

    data = {
        "test_serf": None,
        "paths": []
    }

    in_section = False

    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if "PATHFINDING_EXPORT_START" in line:
                in_section = True
                continue
            if "PATHFINDING_EXPORT_END" in line:
                in_section = False
                continue

            if not in_section:
                continue

            # PATH_TEST_SERF|id
            if "PATH_TEST_SERF|" in line:
                match = re.search(r'PATH_TEST_SERF\|(\d+)', line)
                if match:
                    data["test_serf"] = int(match.group(1))

            # PATH|name|x|y|hqSector|targetSector|distance|sameSector|walkable
            if "PATH|" in line and "PATH_TEST" not in line and "PATH_ERROR" not in line:
                match = re.search(
                    r'PATH\|(\w+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|([\d.]+)\|(\d+)\|(\d+)',
                    line
                )
                if match:
                    data["paths"].append({
                        "name": match.group(1),
                        "x": int(match.group(2)),
                        "y": int(match.group(3)),
                        "hq_sector": int(match.group(4)),
                        "target_sector": int(match.group(5)),
                        "distance": float(match.group(6)),
                        "same_sector": match.group(7) == "1",
                        "walkable": match.group(8) == "1",
                    })

    return data


def parse_building_blocking_export(log_path: Path) -> Dict[str, Any]:
    """Parst BUILDING_BLOCKING_EXPORT aus Game.log"""

    data = {
        "building_count": 0,
        "buildings": [],
        "blocked_points": {}  # building_id -> list of (dx, dy)
    }

    in_section = False

    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if "BUILDING_BLOCKING_EXPORT_START" in line:
                in_section = True
                continue
            if "BUILDING_BLOCKING_EXPORT_END" in line:
                in_section = False
                continue

            if not in_section:
                continue

            # BUILDING_COUNT|n
            if "BUILDING_COUNT|" in line:
                match = re.search(r'BUILDING_COUNT\|(\d+)', line)
                if match:
                    data["building_count"] = int(match.group(1))

            # BUILDING|id|type|player|x|y|blockSize
            if line.strip().startswith("BUILDING|"):
                match = re.search(
                    r'BUILDING\|(\d+)\|(\w+)\|(\d+)\|([\d.]+)\|([\d.]+)\|(\d+)',
                    line
                )
                if match:
                    building_id = int(match.group(1))
                    data["buildings"].append({
                        "id": building_id,
                        "type": match.group(2),
                        "player": int(match.group(3)),
                        "x": float(match.group(4)),
                        "y": float(match.group(5)),
                        "block_size": int(match.group(6)),
                    })
                    data["blocked_points"][building_id] = []

            # BLOCKED|buildingId|dx|dy
            if "BLOCKED|" in line:
                match = re.search(r'BLOCKED\|(\d+)\|(-?\d+)\|(-?\d+)', line)
                if match:
                    building_id = int(match.group(1))
                    if building_id in data["blocked_points"]:
                        data["blocked_points"][building_id].append({
                            "dx": int(match.group(2)),
                            "dy": int(match.group(3)),
                        })

    return data


def parse_buildability_export(log_path: Path) -> Dict[str, Any]:
    """Parst BUILDABILITY_EXPORT aus Game.log"""

    data = {
        "building_types": {},
    }

    in_section = False
    current_type = None

    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if "BUILDABILITY_EXPORT_START" in line:
                in_section = True
                continue
            if "BUILDABILITY_EXPORT_END" in line:
                in_section = False
                continue

            if not in_section:
                continue

            # BUILDTYPE|name
            if "BUILDTYPE|" in line:
                match = re.search(r'BUILDTYPE\|(\w+)', line)
                if match:
                    current_type = match.group(1)
                    data["building_types"][current_type] = {
                        "positions": [],
                        "total": 0
                    }

            # CANBUILD|name|x|y
            if "CANBUILD|" in line:
                match = re.search(r'CANBUILD\|(\w+)\|(\d+)\|(\d+)', line)
                if match:
                    name = match.group(1)
                    if name in data["building_types"]:
                        data["building_types"][name]["positions"].append({
                            "x": int(match.group(2)),
                            "y": int(match.group(3)),
                        })

            # BUILDABLE_TOTAL|name|count
            if "BUILDABLE_TOTAL|" in line:
                match = re.search(r'BUILDABLE_TOTAL\|(\w+)\|(\d+)', line)
                if match:
                    name = match.group(1)
                    if name in data["building_types"]:
                        data["building_types"][name]["total"] = int(match.group(2))

    return data


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Parse Lua exports from Game.log")
    parser.add_argument("--log", required=True, help="Path to Game.log")
    parser.add_argument("--output", default="lua_export_data.json", help="Output JSON file")
    args = parser.parse_args()

    log_path = Path(args.log)

    if not log_path.exists():
        print(f"Error: {log_path} not found")
        return

    print(f"Parsing {log_path}...")

    result = {}

    # Parse all exports
    pathfinding = parse_pathfinding_export(log_path)
    if pathfinding["paths"]:
        result["pathfinding"] = pathfinding
        print(f"  - Pathfinding: {len(pathfinding['paths'])} paths")

    blocking = parse_building_blocking_export(log_path)
    if blocking["buildings"]:
        result["building_blocking"] = blocking
        print(f"  - Building blocking: {len(blocking['buildings'])} buildings")

    buildability = parse_buildability_export(log_path)
    if buildability["building_types"]:
        result["buildability"] = buildability
        print(f"  - Buildability: {len(buildability['building_types'])} types")

    # Save
    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nSaved to {output_path}")

    # Summary
    if "pathfinding" in result:
        print("\n=== Pathfinding Summary ===")
        reachable = sum(1 for p in result["pathfinding"]["paths"] if p["same_sector"])
        total = len(result["pathfinding"]["paths"])
        print(f"Reachable from HQ: {reachable}/{total}")

        for p in result["pathfinding"]["paths"]:
            status = "OK" if p["same_sector"] else "UNREACHABLE"
            print(f"  {p['name']}: {status} (dist: {p['distance']:.0f})")


if __name__ == "__main__":
    main()
