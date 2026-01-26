# -*- coding: utf-8 -*-
"""
Analysiert Holz-Zonen basierend auf Minen-Standorten.
Für strategische Bauplatz-Schaffung bei Raffinerien.
"""

import json
import math
from pathlib import Path

# Lade Daten
base_dir = Path(r"c:\Users\marku\OneDrive\Desktop\siedler_ai")

with open(base_dir / "player1_resources.json", 'r') as f:
    resources = json.load(f)

trees = resources.get("trees_all", [])
hq = (41100, 23100)

# Minen-Positionen aus map_config (nächste Schächte pro Typ)
MINE_POSITIONS = {
    "Schwefelmine": {"pos": (44304, 21484), "raffinerie": "Alchimistenhütte", "dist_to_hq": 3588},
    "Lehmmine": {"pos": (35181, 19553), "raffinerie": "Lehmhütte", "dist_to_hq": 6901},
    "Steinmine": {"pos": (40056, 14891), "raffinerie": "Steinmetzhütte", "dist_to_hq": 8276},
    "Eisenmine": {"pos": (36276, 8927), "raffinerie": "Schmiede", "dist_to_hq": 14971},
}

# Zusätzliche wichtige Positionen
EXTRA_POSITIONS = {
    "HQ_Bereich": {"pos": hq, "raffinerie": "Wohnhäuser/Bauernhöfe", "dist_to_hq": 0},
    "Dorfzentrum": {"pos": (39400, 24300), "raffinerie": "Expansion", "dist_to_hq": 2081},
}

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def analyze_zones():
    """Analysiert welche Bäume in welcher Zone liegen."""

    # Zone-Radien (Bäume innerhalb dieses Radius gehören zur Zone)
    ZONE_RADIUS = {
        "HQ_Bereich": 3500,      # Nahe Bäume für Anfangs-Holz
        "Dorfzentrum": 2500,     # Für Expansion
        "Schwefelmine": 3000,    # Für Alchimistenhütte
        "Lehmmine": 3000,        # Für Lehmhütte
        "Steinmine": 3000,       # Für Steinmetzhütte
        "Eisenmine": 3000,       # Für Schmiede
    }

    # Alle Positionen kombinieren
    all_positions = {**MINE_POSITIONS, **EXTRA_POSITIONS}

    # Zonen-Analyse
    zones = {}
    assigned_trees = set()  # Bereits zugewiesene Bäume (nach Priorität)

    # Priorität: HQ -> Schwefel -> Lehm -> Stein -> Eisen -> Dorfzentrum
    priority_order = ["HQ_Bereich", "Schwefelmine", "Lehmmine", "Steinmine", "Dorfzentrum", "Eisenmine"]

    for zone_name in priority_order:
        if zone_name not in all_positions:
            continue

        zone_data = all_positions[zone_name]
        zone_pos = zone_data["pos"]
        zone_radius = ZONE_RADIUS.get(zone_name, 3000)

        zone_trees = []
        for i, tree in enumerate(trees):
            if i in assigned_trees:
                continue
            tree_pos = (tree["x"], tree["y"])
            dist = distance(zone_pos, tree_pos)
            if dist <= zone_radius:
                zone_trees.append({
                    "idx": i,
                    "x": tree["x"],
                    "y": tree["y"],
                    "type": tree["type"],
                    "dist_to_zone_center": dist,
                    "dist_to_hq": tree.get("distance_to_hq", distance(hq, tree_pos))
                })
                assigned_trees.add(i)

        # Sortiere nach Distanz zum Zonenzentrum
        zone_trees.sort(key=lambda t: t["dist_to_zone_center"])

        zones[zone_name] = {
            "center": zone_pos,
            "radius": zone_radius,
            "raffinerie": zone_data["raffinerie"],
            "dist_to_hq": zone_data["dist_to_hq"],
            "tree_count": len(zone_trees),
            "total_wood": len(zone_trees) * 75,  # 75 Holz pro Baum
            "trees": zone_trees
        }

    # Übrige Bäume (keiner Zone zugeordnet)
    remaining_trees = []
    for i, tree in enumerate(trees):
        if i not in assigned_trees:
            remaining_trees.append({
                "idx": i,
                "x": tree["x"],
                "y": tree["y"],
                "type": tree["type"],
                "dist_to_hq": tree.get("distance_to_hq", distance(hq, (tree["x"], tree["y"])))
            })

    zones["Sonstige"] = {
        "center": None,
        "radius": None,
        "raffinerie": "Reserve",
        "dist_to_hq": None,
        "tree_count": len(remaining_trees),
        "total_wood": len(remaining_trees) * 75,
        "trees": remaining_trees
    }

    return zones

def print_analysis(zones):
    """Gibt die Zonen-Analyse aus."""

    print("=" * 70)
    print("HOLZ-ZONEN ANALYSE - Strategische Bauplatz-Schaffung")
    print("=" * 70)

    total_trees = 0
    total_wood = 0

    for zone_name, zone_data in zones.items():
        total_trees += zone_data["tree_count"]
        total_wood += zone_data["total_wood"]

        print(f"\n{'-' * 70}")
        print(f"ZONE: {zone_name}")
        print(f"{'-' * 70}")

        if zone_data["center"]:
            print(f"  Zentrum: ({zone_data['center'][0]}, {zone_data['center'][1]})")
            print(f"  Radius: {zone_data['radius']} Einheiten")
            print(f"  Distanz zum HQ: {zone_data['dist_to_hq']}")

        print(f"  Raffinerie/Zweck: {zone_data['raffinerie']}")
        print(f"  Bäume: {zone_data['tree_count']}")
        print(f"  Holz gesamt: {zone_data['total_wood']}")

        if zone_data["trees"] and zone_name != "Sonstige":
            print(f"\n  Nächste 5 Bäume zur Zone:")
            for tree in zone_data["trees"][:5]:
                print(f"    ({tree['x']:.0f}, {tree['y']:.0f}) - "
                      f"Dist zum Zentrum: {tree['dist_to_zone_center']:.0f}, "
                      f"Dist zum HQ: {tree['dist_to_hq']:.0f}")

    print(f"\n{'=' * 70}")
    print(f"GESAMT: {total_trees} Bäume, {total_wood} Holz")
    print(f"{'=' * 70}")

    # Strategische Empfehlungen
    print("\n" + "=" * 70)
    print("STRATEGISCHE EMPFEHLUNGEN")
    print("=" * 70)

    for zone_name, zone_data in zones.items():
        if zone_name == "Sonstige" or zone_name == "HQ_Bereich":
            continue
        if zone_data["tree_count"] > 0:
            print(f"\n{zone_name}:")
            print(f"  -> Faelle {min(10, zone_data['tree_count'])} Baeume fuer {zone_data['raffinerie']}-Bauplatz")
            print(f"  -> Gewinn: {min(10, zone_data['tree_count']) * 75} Holz + Bauplatz")

def export_zones_config(zones):
    """Exportiert die Zonen als Python-Config."""

    output = """# -*- coding: utf-8 -*-
\"\"\"
Holz-Zonen für strategische Bauplatz-Schaffung.
Generiert von analyze_wood_zones.py
\"\"\"

# Zone-Definitionen
WOOD_ZONES = {
"""

    for zone_name, zone_data in zones.items():
        if zone_name == "Sonstige":
            continue

        output += f'    "{zone_name}": {{\n'
        output += f'        "center": {zone_data["center"]},\n'
        output += f'        "radius": {zone_data["radius"]},\n'
        output += f'        "raffinerie": "{zone_data["raffinerie"]}",\n'
        output += f'        "tree_count": {zone_data["tree_count"]},\n'
        output += f'        "total_wood": {zone_data["total_wood"]},\n'

        # Nur die ersten 20 Bäume pro Zone
        trees_limited = zone_data["trees"][:20]
        output += f'        "trees": [\n'
        for tree in trees_limited:
            output += f'            {{"x": {tree["x"]:.0f}, "y": {tree["y"]:.0f}, "dist": {tree["dist_to_zone_center"]:.0f}}},\n'
        output += f'        ],\n'
        output += f'    }},\n'

    output += "}\n"

    # Speichern
    with open(base_dir / "wood_zones_config.py", 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"\nZonen-Config exportiert: {base_dir / 'wood_zones_config.py'}")

def visualize_zones(zones):
    """Erstellt eine Visualisierung der Holz-Zonen."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle
    import numpy as np

    fig, ax = plt.subplots(figsize=(16, 14))

    # Farben für Zonen
    colors = {
        "HQ_Bereich": "blue",
        "Dorfzentrum": "cyan",
        "Schwefelmine": "yellow",
        "Lehmmine": "orange",
        "Steinmine": "gray",
        "Eisenmine": "silver",
        "Sonstige": "lightgreen",
    }

    # Alle Bäume nach Zone zeichnen
    for zone_name, zone_data in zones.items():
        color = colors.get(zone_name, "green")
        trees = zone_data["trees"]
        if trees:
            x = [t["x"] for t in trees]
            y = [t["y"] for t in trees]
            ax.scatter(x, y, c=color, s=20, alpha=0.6, label=f'{zone_name} ({len(trees)} Bäume)')

    # Zonenzentren und Kreise zeichnen
    for zone_name, zone_data in zones.items():
        if zone_data["center"] and zone_name != "Sonstige":
            cx, cy = zone_data["center"]
            color = colors.get(zone_name, "green")

            # Kreis für Zone
            circle = Circle((cx, cy), zone_data["radius"],
                           fill=False, edgecolor=color, linewidth=2, linestyle='--')
            ax.add_patch(circle)

            # Zentrum markieren
            marker = 's' if 'mine' in zone_name.lower() else 'o'
            ax.scatter(cx, cy, c=color, s=200, marker=marker, edgecolors='black', linewidth=2, zorder=10)

            # Beschriftung
            ax.annotate(f'{zone_name}\n{zone_data["raffinerie"]}',
                       (cx, cy), textcoords="offset points",
                       xytext=(10, 10), fontsize=8, fontweight='bold')

    # HQ markieren
    ax.scatter(hq[0], hq[1], c='red', s=300, marker='*', edgecolors='black', linewidth=2, zorder=15, label='HQ')

    ax.set_xlabel('X-Koordinate')
    ax.set_ylabel('Y-Koordinate')
    ax.set_title('Holz-Zonen für strategische Bauplatz-Schaffung\nJede Zone = Bäume die gefällt werden sollten für Raffinerie-Bauplatz')
    ax.legend(loc='upper right', fontsize=8)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(base_dir / "wood_zones_map.png", dpi=150, bbox_inches='tight')
    plt.close()

    print(f"\nVisualisierung gespeichert: {base_dir / 'wood_zones_map.png'}")


if __name__ == "__main__":
    zones = analyze_zones()
    print_analysis(zones)
    export_zones_config(zones)
    visualize_zones(zones)
