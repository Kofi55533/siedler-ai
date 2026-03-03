# -*- coding: utf-8 -*-
"""
Visualisiert die Wintersturm-Karte mit allen wichtigen Elementen:
- Begehbare Bereiche (aus Terrain-Analyse)
- Dorfzentren-Bauplätze
- Minenschächte
- Ressourcen
- HQ Positionen
"""

import json
import math
import os

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("WARNUNG: PIL nicht installiert. Versuche mit matplotlib...")

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.colors import LinearSegmentedColormap
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# Karten-Dimensionen
MAP_WIDTH = 50480
MAP_HEIGHT = 50496

# Spieler 1 Quadrant
P1_MIN_X = MAP_WIDTH / 2  # 25240
P1_MAX_Y = MAP_HEIGHT / 2  # 25248

# HQ Position Spieler 1
HQ_POS = (41100, 23100)

# Alle DZ-Bauplätze (aus mapdata.xml)
ALL_VILLAGE_CENTERS = [
    (34500, 23700),
    (34500, 27600),
    (16800, 23700),
    (39400, 24300),  # Spieler 1 - BEBAUT
    (43500, 9400),
    (16800, 27600),
    (11900, 24300),
    (7800, 9400),
    (39400, 27000),
    (43500, 41900),
    (11900, 27000),
    (7800, 41900),
]

# Spieler-Zuordnung
def get_player(x, y):
    cx, cy = MAP_WIDTH/2, MAP_HEIGHT/2
    if x > cx and y < cy:
        return 1
    elif x > cx and y >= cy:
        return 2
    elif x <= cx and y >= cy:
        return 3
    else:
        return 4


def load_map_config():
    """Lädt Karten-Konfiguration"""
    from map_config_wintersturm import (
        PLAYER_1_MINE_SHAFTS, PLAYER_1_SMALL_DEPOSITS,
        PLAYER_1_TREES_NEAREST, PLAYER_HQ_POSITIONS
    )
    return {
        "mine_shafts": PLAYER_1_MINE_SHAFTS,
        "deposits": PLAYER_1_SMALL_DEPOSITS,
        "trees": PLAYER_1_TREES_NEAREST,
        "hq": PLAYER_HQ_POSITIONS,
    }


def create_map_visualization():
    """Erstellt eine Visualisierung mit matplotlib"""
    if not HAS_MATPLOTLIB:
        print("Matplotlib nicht verfügbar!")
        return

    config = load_map_config()

    # Nur Spieler 1 Quadrant zeigen
    fig, ax = plt.subplots(1, 1, figsize=(16, 14))

    # Hintergrund
    ax.set_facecolor('#2d4a2d')  # Dunkelgrün für Wald

    # Quadrant-Grenzen für Spieler 1
    # x: 25240 bis 50480
    # y: 0 bis 25248
    ax.set_xlim(P1_MIN_X - 1000, MAP_WIDTH + 1000)
    ax.set_ylim(-1000, P1_MAX_Y + 1000)

    # Spieler 1 Quadrant markieren
    quad_rect = patches.Rectangle(
        (P1_MIN_X, 0), MAP_WIDTH - P1_MIN_X, P1_MAX_Y,
        linewidth=3, edgecolor='white', facecolor='#3d5a3d', alpha=0.3
    )
    ax.add_patch(quad_rect)

    # HQ markieren (großes Quadrat)
    hq = HQ_POS
    hq_rect = patches.Rectangle(
        (hq[0]-500, hq[1]-500), 1000, 1000,
        linewidth=3, edgecolor='gold', facecolor='gold', alpha=0.8
    )
    ax.add_patch(hq_rect)
    ax.annotate('HQ', (hq[0], hq[1]), fontsize=12, ha='center', va='center',
                fontweight='bold', color='black')

    # Dorfzentren-Bauplätze
    for vc in ALL_VILLAGE_CENTERS:
        player = get_player(vc[0], vc[1])
        if player == 1:
            # Prüfe ob bebaut
            is_built = abs(vc[0] - 39400) < 100 and abs(vc[1] - 24300) < 100
            color = 'orange' if is_built else 'yellow'
            label = 'DZ (gebaut)' if is_built else 'DZ-Slot'

            rect = patches.Rectangle(
                (vc[0]-400, vc[1]-400), 800, 800,
                linewidth=2, edgecolor=color, facecolor=color, alpha=0.6
            )
            ax.add_patch(rect)

            dist = math.sqrt((vc[0]-hq[0])**2 + (vc[1]-hq[1])**2)
            ax.annotate(f'{label}\n{dist:.0f}m', (vc[0], vc[1]-600),
                       fontsize=8, ha='center', color='white')

    # Minenschächte
    colors_mine = {
        'Eisenmine': '#8B4513',
        'Steinmine': '#808080',
        'Lehmmine': '#CD853F',
        'Schwefelmine': '#FFD700',
    }

    for mine_type, shafts in config["mine_shafts"].items():
        for shaft in shafts:
            color = colors_mine.get(mine_type, 'white')
            circle = patches.Circle(
                (shaft["x"], shaft["y"]), 400,
                linewidth=2, edgecolor=color, facecolor=color, alpha=0.7
            )
            ax.add_patch(circle)
            ax.annotate(mine_type[:4], (shaft["x"], shaft["y"]),
                       fontsize=7, ha='center', va='center', color='white')

    # Kleine Vorkommen (Deposits)
    colors_dep = {
        'Eisen': '#8B4513',
        'Stein': '#808080',
        'Lehm': '#CD853F',
        'Schwefel': '#FFD700',
    }

    for res_type, deposits in config["deposits"].items():
        for dep in deposits:
            color = colors_dep.get(res_type, 'white')
            circle = patches.Circle(
                (dep["x"], dep["y"]), 300,
                linewidth=2, edgecolor=color, facecolor='none', linestyle='--'
            )
            ax.add_patch(circle)
            ax.annotate(f'{res_type[:2]}\n4000', (dep["x"], dep["y"]+400),
                       fontsize=6, ha='center', color=color)

    # Bäume (nur die nächsten 50)
    for tree in config["trees"][:50]:
        ax.plot(tree["x"], tree["y"], 'g^', markersize=4, alpha=0.6)

    # Begehbarkeits-Hinweis (vereinfacht)
    # Die Karte hat Berge an den Rändern und im Zentrum Täler
    # Wir zeichnen grobe Bereiche

    # Nicht-begehbare Bereiche (Berge/Wasser) - geschätzt
    blocked_areas = [
        # Oberer Rand (Berge)
        patches.Rectangle((25000, 0), 26000, 5000, alpha=0.3, facecolor='brown'),
        # Rechter Rand
        patches.Rectangle((48000, 0), 3000, 26000, alpha=0.3, facecolor='brown'),
    ]

    for area in blocked_areas:
        ax.add_patch(area)

    # Legende
    legend_elements = [
        patches.Patch(facecolor='gold', edgecolor='gold', label='Hauptquartier'),
        patches.Patch(facecolor='orange', edgecolor='orange', label='Dorfzentrum (gebaut)'),
        patches.Patch(facecolor='yellow', edgecolor='yellow', label='DZ-Bauplatz (frei)'),
        patches.Patch(facecolor='#8B4513', label='Eisen-Mine/Deposit'),
        patches.Patch(facecolor='#808080', label='Stein-Mine/Deposit'),
        patches.Patch(facecolor='#CD853F', label='Lehm-Mine/Deposit'),
        patches.Patch(facecolor='#FFD700', label='Schwefel-Mine/Deposit'),
        plt.Line2D([0], [0], marker='^', color='g', label='Bäume', linestyle='None'),
        patches.Patch(facecolor='brown', alpha=0.3, label='Nicht begehbar (geschätzt)'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=8)

    # Titel und Labels
    ax.set_title('EMS Wintersturm - Spieler 1 Quadrant\n(Alle Ressourcen und Bauplätze)', fontsize=14)
    ax.set_xlabel('X-Koordinate')
    ax.set_ylabel('Y-Koordinate')

    # Grid
    ax.grid(True, alpha=0.3, color='white')
    ax.set_aspect('equal')

    # Invertiere Y-Achse (0 oben)
    ax.invert_yaxis()

    # Speichern
    output_path = 'map_player1_complete.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#1a1a1a')
    plt.close()

    print(f"Karte gespeichert: {output_path}")

    # Zusätzlich: Textbasierte Übersicht
    print("\n" + "="*60)
    print("SPIELER 1 - KOMPLETTE ÜBERSICHT")
    print("="*60)

    print(f"\nHQ Position: {HQ_POS}")

    print("\nDORFZENTREN-BAUPLÄTZE:")
    p1_vcs = [(vc, math.sqrt((vc[0]-hq[0])**2 + (vc[1]-hq[1])**2))
              for vc in ALL_VILLAGE_CENTERS if get_player(vc[0], vc[1]) == 1]
    p1_vcs.sort(key=lambda x: x[1])

    for vc, dist in p1_vcs:
        is_built = abs(vc[0] - 39400) < 100 and abs(vc[1] - 24300) < 100
        status = "GEBAUT" if is_built else "frei"
        print(f"  ({vc[0]}, {vc[1]}) - Distanz: {dist:.0f} - {status}")

    print("\nMINEN-SCHÄCHTE (wo Minen gebaut werden können):")
    for mine_type, shafts in config["mine_shafts"].items():
        print(f"  {mine_type}:")
        for shaft in sorted(shafts, key=lambda x: x["distance_to_hq"]):
            print(f"    ({shaft['x']}, {shaft['y']}) - Distanz: {shaft['distance_to_hq']}")

    print("\nKLEINE VORKOMMEN (erschöpfbar, 4000 Einheiten):")
    for res_type, deposits in config["deposits"].items():
        print(f"  {res_type}:")
        for dep in sorted(deposits, key=lambda x: x["distance_to_hq"]):
            print(f"    ({dep['x']}, {dep['y']}) - Distanz: {dep['distance_to_hq']}")

    print(f"\nBÄUME: ~888 (nächster bei Distanz {config['trees'][0]['distance_to_hq']})")


if __name__ == "__main__":
    create_map_visualization()
