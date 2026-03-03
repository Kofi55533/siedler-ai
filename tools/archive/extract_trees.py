# -*- coding: utf-8 -*-
"""
Extrahiert Baum-Positionen für Spieler 1 aus der wintersturm_map_data.json
"""

import json
from pathlib import Path

MAP_DATA_PATH = Path(r"c:\Users\marku\OneDrive\Desktop\siedler_ai\config\wintersturm_map_data.json")

def main():
    with open(MAP_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Karten-Dimensionen
    MAP_WIDTH = 50480
    MAP_HEIGHT = 50496

    # HQ Position Spieler 1
    hq_x, hq_y = 41100, 23100

    # Spieler 1 Quadrant Filter
    def in_player1_quadrant(pos):
        return pos['x'] > MAP_WIDTH / 2 and pos['y'] < MAP_HEIGHT / 2

    # Bäume im Spieler 1 Bereich
    p1_trees = [t for t in data['trees'] if in_player1_quadrant(t['position'])]

    # Nach Distanz sortieren
    p1_trees_sorted = sorted(p1_trees,
        key=lambda t: ((t['position']['x']-hq_x)**2 + (t['position']['y']-hq_y)**2)**0.5)

    print(f"Bäume im Spieler 1 Quadrant: {len(p1_trees)}")

    # Baum-Typen zählen
    tree_types = {}
    for t in p1_trees:
        tt = t['type']
        tree_types[tt] = tree_types.get(tt, 0) + 1

    print("\nBaum-Typen:")
    for tt, count in sorted(tree_types.items(), key=lambda x: -x[1]):
        print(f"  {tt}: {count}")

    # Nächste 20 Bäume ausgeben
    print("\n20 nächste Bäume zum HQ:")
    for i, t in enumerate(p1_trees_sorted[:20]):
        dist = ((t['position']['x']-hq_x)**2 + (t['position']['y']-hq_y)**2)**0.5
        print(f"  {i+1}. ({t['position']['x']:.0f}, {t['position']['y']:.0f}) - {t['type']} - Distanz: {dist:.0f}")

    # Holz-Statistik
    # Jeder Baum gibt ca. 2 Holz bei Extraktion
    total_wood = len(p1_trees) * 2
    print(f"\nGeschätzte Holzmenge: {total_wood} Einheiten (bei 2 Holz pro Baum)")

    # Python-Code für map_config generieren
    print("\n\n=== CODE FÜR map_config_wintersturm.py ===\n")

    print("# Bäume für Spieler 1 (nach Distanz zum HQ sortiert)")
    print(f"PLAYER_1_TREES = [")

    for t in p1_trees_sorted:
        dist = ((t['position']['x']-hq_x)**2 + (t['position']['y']-hq_y)**2)**0.5
        print(f'    {{"x": {t["position"]["x"]:.0f}, "y": {t["position"]["y"]:.0f}, "type": "{t["type"]}", "distance_to_hq": {dist:.0f}}},')

    print("]")
    print(f"\n# Zusammenfassung: {len(p1_trees)} Bäume, ca. {total_wood} Holz")


if __name__ == "__main__":
    main()
