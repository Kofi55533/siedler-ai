# -*- coding: utf-8 -*-
"""
Vergleicht dynamische Blocking-Änderungen aus dem Spiel mit dem Environment.

Workflow:
1. Spiel mit export_dynamic_blocking.lua spielen
2. Logs parsen
3. Events im Environment nachspielen
4. Blocking-Zustand vergleichen
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple


def parse_dynamic_blocking_log(log_path: Path) -> Dict[str, Any]:
    """Parst die dynamischen Blocking-Logs."""

    data = {
        "config": {},
        "snapshots": [],
        "events": [],
        "initial_blocked": [],
    }

    current_snapshot = None

    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # Config
            if "GRID_STEP|" in line:
                match = re.search(r'GRID_STEP\|(\d+)', line)
                if match:
                    data["config"]["grid_step"] = int(match.group(1))

            if "INTERVAL|" in line:
                match = re.search(r'INTERVAL\|(\d+)', line)
                if match:
                    data["config"]["interval"] = int(match.group(1))

            # Snapshot Start
            if "SNAPSHOT_" in line and "_START|" in line:
                match = re.search(r'SNAPSHOT_(\d+)_START\|([\d.]+)', line)
                if match:
                    current_snapshot = {
                        "id": int(match.group(1)),
                        "time": float(match.group(2)),
                        "changes": [],
                    }

            # Snapshot End
            if "SNAPSHOT_" in line and "_END" in line:
                if current_snapshot:
                    data["snapshots"].append(current_snapshot)
                    current_snapshot = None

            # Initial blocked
            if "INITIAL_BLOCKED|" in line:
                match = re.search(r'INITIAL_BLOCKED\|(\d+)\|(\d+)\|(\d+)\|(\d+)', line)
                if match:
                    data["initial_blocked"].append({
                        "x": int(match.group(1)),
                        "y": int(match.group(2)),
                        "blocking": int(match.group(3)),
                        "sector": int(match.group(4)),
                    })

            # Changes
            if "CHANGE|" in line:
                match = re.search(r'CHANGE\|(\d+)\|(\d+)\|(\d+)_(\d+)\|(\d+)_(\d+)', line)
                if match and current_snapshot:
                    current_snapshot["changes"].append({
                        "x": int(match.group(1)),
                        "y": int(match.group(2)),
                        "old_blocking": int(match.group(3)),
                        "old_sector": int(match.group(4)),
                        "new_blocking": int(match.group(5)),
                        "new_sector": int(match.group(6)),
                    })

            # Snapshot Summary
            if "SNAPSHOT_SUMMARY|" in line:
                match = re.search(r'SNAPSHOT_SUMMARY\|(\d+)\|([\d.]+)\|(\d+)', line)
                if match and current_snapshot:
                    current_snapshot["total_changes"] = int(match.group(3))

            # Entity Count
            if "ENTITY_COUNT|" in line:
                match = re.search(r'ENTITY_COUNT\|(\d+)\|(\d+)\|(\d+)', line)
                if match and current_snapshot:
                    current_snapshot["buildings"] = int(match.group(2))
                    current_snapshot["trees"] = int(match.group(3))

            # Build Events
            if "EVENT_BUILD|" in line:
                match = re.search(r'EVENT_BUILD\|([\d.]+)\|(\d+)\|(\w+)\|([\d.]+)\|([\d.]+)', line)
                if match:
                    data["events"].append({
                        "type": "build",
                        "time": float(match.group(1)),
                        "entity_id": int(match.group(2)),
                        "building_type": match.group(3),
                        "x": float(match.group(4)),
                        "y": float(match.group(5)),
                    })

            # Destroy Events
            if "EVENT_DESTROY|" in line:
                match = re.search(r'EVENT_DESTROY\|([\d.]+)\|(\d+)', line)
                if match:
                    data["events"].append({
                        "type": "destroy",
                        "time": float(match.group(1)),
                        "entity_id": int(match.group(2)),
                    })

    return data


def analyze_blocking_changes(data: Dict[str, Any]) -> None:
    """Analysiert die Blocking-Änderungen."""

    print("\n=== BLOCKING-ÄNDERUNGEN ANALYSE ===\n")

    print(f"Config: Grid={data['config'].get('grid_step', '?')},"
          f" Interval={data['config'].get('interval', '?')}s")
    print(f"Initial blockierte Punkte: {len(data['initial_blocked'])}")
    print(f"Snapshots: {len(data['snapshots'])}")
    print(f"Build/Destroy Events: {len(data['events'])}")

    print("\n--- Snapshots ---")
    for snap in data["snapshots"]:
        buildings = snap.get("buildings", "?")
        trees = snap.get("trees", "?")
        changes = snap.get("total_changes", len(snap.get("changes", [])))

        print(f"  #{snap['id']} @ {snap['time']:.0f}s: "
              f"{changes} Änderungen, {buildings} Gebäude, {trees} Bäume")

        # Zeige erste paar Änderungen
        for change in snap.get("changes", [])[:3]:
            old = f"block={change['old_blocking']}"
            new = f"block={change['new_blocking']}"
            print(f"    ({change['x']}, {change['y']}): {old} → {new}")

        if len(snap.get("changes", [])) > 3:
            print(f"    ... und {len(snap['changes']) - 3} weitere")

    print("\n--- Events ---")
    for event in data["events"][:10]:
        if event["type"] == "build":
            print(f"  {event['time']:.0f}s: BUILD {event['building_type']} "
                  f"@ ({event['x']:.0f}, {event['y']:.0f})")
        else:
            print(f"  {event['time']:.0f}s: DESTROY entity {event['entity_id']}")

    if len(data["events"]) > 10:
        print(f"  ... und {len(data['events']) - 10} weitere Events")


def generate_validation_report(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generiert einen Validierungsbericht."""

    report = {
        "total_snapshots": len(data["snapshots"]),
        "total_changes": sum(s.get("total_changes", 0) for s in data["snapshots"]),
        "build_events": len([e for e in data["events"] if e["type"] == "build"]),
        "destroy_events": len([e for e in data["events"] if e["type"] == "destroy"]),
        "change_positions": [],
    }

    # Sammle alle geänderten Positionen
    changed_positions = set()
    for snap in data["snapshots"]:
        for change in snap.get("changes", []):
            changed_positions.add((change["x"], change["y"]))

    report["unique_changed_positions"] = len(changed_positions)
    report["change_positions"] = list(changed_positions)[:100]  # Max 100

    return report


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Analyze dynamic blocking logs")
    parser.add_argument("--log", required=True, help="Path to Game.log")
    parser.add_argument("--output", default="dynamic_blocking_analysis.json")
    args = parser.parse_args()

    log_path = Path(args.log)

    if not log_path.exists():
        print(f"Error: {log_path} not found")
        return

    print(f"Parsing {log_path}...")
    data = parse_dynamic_blocking_log(log_path)

    # Analyse ausgeben
    analyze_blocking_changes(data)

    # Report speichern
    report = generate_validation_report(data)
    report["raw_data"] = data

    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\nGespeichert: {output_path}")

    # Zusammenfassung für Environment-Vergleich
    print("\n=== FÜR ENVIRONMENT-VERGLEICH ===")
    print("1. Spiele dieselben Build-Events im Environment nach")
    print("2. Vergleiche Blocking an den geänderten Positionen")
    print(f"3. Zu prüfende Positionen: {report['unique_changed_positions']}")


if __name__ == "__main__":
    main()
