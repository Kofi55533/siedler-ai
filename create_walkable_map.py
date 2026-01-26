# -*- coding: utf-8 -*-
"""
Erstellt eine vollständige Karte mit begehbaren Bereichen für EMS Wintersturm.
Kombiniert Terrain-Daten mit Ressourcen-Positionen.
"""

import struct
import numpy as np
import os
import json
import math

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.colors import LinearSegmentedColormap, ListedColormap
    from matplotlib.lines import Line2D
except ImportError:
    print("Matplotlib nicht verfügbar!")
    exit(1)

# Pfade
EXTRACTED_DIR = r"C:\Users\marku\OneDrive\Desktop\wintersturm_extracted"
TERRAIN_FILE = os.path.join(EXTRACTED_DIR, "file_0.bin")
MAP_DATA_FILE = r"c:\Users\marku\OneDrive\Desktop\siedler_ai\config\wintersturm_map_data.json"

# Karten-Dimensionen
MAP_WIDTH = 50480
MAP_HEIGHT = 50496

# Grid-Dimensionen (aus Analyse)
GRID_WIDTH = 1508
GRID_HEIGHT = 1496

# Skalierung
SCALE_X = MAP_WIDTH / GRID_WIDTH  # ~33.5
SCALE_Y = MAP_HEIGHT / GRID_HEIGHT  # ~33.8

# HQ Positionen
HQ_POSITIONS = {
    1: (41100, 23100),
    2: (41100, 28200),
    3: (10200, 28200),
    4: (10200, 23100),
}

# Dorfzentrum-Positionen (gebaut)
DZ_POSITIONS = {
    1: (39400, 24300),
    2: (39400, 27000),
    3: (11900, 27000),
    4: (11900, 24300),
}

# Alle DZ-Bauplätze
ALL_DZ_SLOTS = [
    (34500, 23700), (34500, 27600), (16800, 23700), (39400, 24300),
    (43500, 9400), (16800, 27600), (11900, 24300), (7800, 9400),
    (39400, 27000), (43500, 41900), (11900, 27000), (7800, 41900),
]


def load_terrain_data():
    """Lädt die Terrain-Daten aus der Binärdatei."""
    with open(TERRAIN_FILE, 'rb') as f:
        data = f.read()

    arr = np.frombuffer(data[:GRID_WIDTH * GRID_HEIGHT], dtype=np.uint8)
    arr = arr.reshape((GRID_HEIGHT, GRID_WIDTH))
    return arr


def load_map_data():
    """Lädt die Kartendaten (Ressourcen, Gebäude)."""
    with open(MAP_DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def game_to_grid(x, y):
    """Konvertiert Spielkoordinaten zu Grid-Koordinaten."""
    return int(x / SCALE_X), int(y / SCALE_Y)


def grid_to_game(gx, gy):
    """Konvertiert Grid-Koordinaten zu Spielkoordinaten."""
    return gx * SCALE_X, gy * SCALE_Y


def create_walkable_mask(terrain, threshold=None):
    """
    Erstellt eine Maske der begehbaren Bereiche.

    WICHTIG: Die Binärdatei enthält NICHT direkt Blocking-Daten!
    Der Wert 128 ist der häufigste Wert (flaches, begehbares Terrain).
    Werte nahe 128 sind wahrscheinlich auch begehbar.

    Interpretation:
    - 128 = Flaches begehbares Terrain (Hauptbereich)
    - Werte weit von 128 entfernt = möglicherweise Berge/Wasser

    ABER: Alle Ressourcen-Positionen im Spiel SIND begehbar!
    Diese Visualisierung zeigt nur die TERRAIN-Höhe, nicht die Blocking-Map.
    """
    # Begehbar = Werte nahe 128 (Standardterrain)
    # Wir verwenden einen breiteren Bereich
    center = 128
    range_val = 50  # +/- 50 vom Zentrum

    walkable = np.abs(terrain.astype(np.int16) - center) < range_val

    # Alternative: Alles unter einem hohen Schwellenwert ist begehbar
    # (außer sehr niedrige Werte die Wasser sein könnten)
    walkable_alt = (terrain > 10) & (terrain < 220)

    return walkable_alt  # Verwende die alternative Methode


def create_full_map_visualization(terrain, map_data, output_path):
    """Erstellt die vollständige Kartenvisualisierung."""

    fig, axes = plt.subplots(2, 2, figsize=(24, 24))

    # === OBEN LINKS: Ganze Karte mit Terrain ===
    ax1 = axes[0, 0]
    create_terrain_view(ax1, terrain, map_data, "Gesamte Karte - Terrain & Ressourcen")

    # === OBEN RECHTS: Begehbarkeits-Karte ===
    ax2 = axes[0, 1]
    create_walkability_view(ax2, terrain, map_data, "Begehbare Bereiche (Grün = begehbar)")

    # === UNTEN LINKS: Spieler 1 Detail ===
    ax3 = axes[1, 0]
    create_player1_detail(ax3, terrain, map_data, "Spieler 1 - Detail mit Terrain")

    # === UNTEN RECHTS: Spieler 1 Begehbarkeit ===
    ax4 = axes[1, 1]
    create_player1_walkability(ax4, terrain, map_data, "Spieler 1 - Begehbare Wege")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#1a1a1a')
    plt.close()
    print(f"Karte gespeichert: {output_path}")


def create_terrain_view(ax, terrain, map_data, title):
    """Zeigt die Terrain-Höhenkarte mit Ressourcen."""

    # Terrain als Hintergrund
    cmap = LinearSegmentedColormap.from_list('terrain', [
        '#1a4d1a',  # Dunkelgrün (niedrig/begehbar)
        '#2d6b2d',  # Grün
        '#4a8c4a',  # Hellgrün
        '#8b8b4a',  # Gelbgrün
        '#8b6b4a',  # Braun
        '#6b4a2d',  # Dunkelbraun (Berge)
        '#4a2d1a',  # Sehr dunkel
    ])

    # Terrain auf Spielkoordinaten skalieren
    extent = [0, MAP_WIDTH, MAP_HEIGHT, 0]
    ax.imshow(terrain, cmap=cmap, extent=extent, origin='upper', alpha=0.8)

    # Quadrant-Grenzen
    ax.axhline(y=MAP_HEIGHT/2, color='white', linestyle='--', alpha=0.5, linewidth=2)
    ax.axvline(x=MAP_WIDTH/2, color='white', linestyle='--', alpha=0.5, linewidth=2)

    # HQs und DZs
    colors = {1: '#4169E1', 2: '#32CD32', 3: '#DC143C', 4: '#FFA500'}
    for player, pos in HQ_POSITIONS.items():
        ax.scatter(pos[0], pos[1], c=colors[player], s=300, marker='s',
                  edgecolors='white', linewidths=2, zorder=10)
        ax.annotate(f'HQ{player}', (pos[0], pos[1]), color='white', fontsize=10,
                   fontweight='bold', ha='center', va='bottom', xytext=(0, 15),
                   textcoords='offset points')

    for player, pos in DZ_POSITIONS.items():
        ax.scatter(pos[0], pos[1], c=colors[player], s=150, marker='D',
                  edgecolors='white', linewidths=1, zorder=9)

    # DZ-Bauplätze
    for pos in ALL_DZ_SLOTS:
        if pos not in DZ_POSITIONS.values():
            ax.scatter(pos[0], pos[1], c='cyan', s=80, marker='D',
                      edgecolors='white', linewidths=1, zorder=8, alpha=0.7)

    # Ressourcen aus map_data
    add_resources_to_axis(ax, map_data, alpha=0.7)

    ax.set_xlim(0, MAP_WIDTH)
    ax.set_ylim(MAP_HEIGHT, 0)
    ax.set_title(title, fontsize=14, fontweight='bold', color='white')
    ax.set_xlabel('X', color='white')
    ax.set_ylabel('Y', color='white')
    ax.tick_params(colors='white')


def create_walkability_view(ax, terrain, map_data, title):
    """Zeigt die begehbaren Bereiche."""

    walkable = create_walkable_mask(terrain, threshold=135)

    # Binäre Colormap: Grün = begehbar, Rot = blockiert
    cmap = ListedColormap(['#8B0000', '#228B22'])  # Dunkelrot, Grün

    extent = [0, MAP_WIDTH, MAP_HEIGHT, 0]
    ax.imshow(walkable.astype(int), cmap=cmap, extent=extent, origin='upper', alpha=0.8)

    # HQs markieren
    colors = {1: 'white', 2: 'white', 3: 'white', 4: 'white'}
    for player, pos in HQ_POSITIONS.items():
        ax.scatter(pos[0], pos[1], c='gold', s=200, marker='s',
                  edgecolors='white', linewidths=2, zorder=10)
        ax.annotate(f'HQ{player}', (pos[0], pos[1]), color='white', fontsize=9,
                   fontweight='bold', ha='center', va='bottom', xytext=(0, 10),
                   textcoords='offset points')

    # Statistik berechnen
    total = walkable.size
    walkable_count = np.sum(walkable)
    blocked_count = total - walkable_count

    ax.set_xlim(0, MAP_WIDTH)
    ax.set_ylim(MAP_HEIGHT, 0)
    ax.set_title(f"{title}\n(Begehbar: {100*walkable_count/total:.1f}%, Blockiert: {100*blocked_count/total:.1f}%)",
                fontsize=14, fontweight='bold', color='white')
    ax.set_xlabel('X', color='white')
    ax.set_ylabel('Y', color='white')
    ax.tick_params(colors='white')

    # Legende
    legend_elements = [
        patches.Patch(facecolor='#228B22', label='Begehbar'),
        patches.Patch(facecolor='#8B0000', label='Blockiert (Berge/Wasser)'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)


def create_player1_detail(ax, terrain, map_data, title):
    """Zeigt Spieler 1 Quadrant im Detail."""

    # Spieler 1 Bereich
    p1_x_min = int(MAP_WIDTH / 2)
    p1_y_max = int(MAP_HEIGHT / 2)

    # Grid-Bereich für Spieler 1
    g_x_min = int(p1_x_min / SCALE_X)
    g_y_max = int(p1_y_max / SCALE_Y)

    # Terrain-Ausschnitt
    terrain_p1 = terrain[:g_y_max, g_x_min:]

    cmap = LinearSegmentedColormap.from_list('terrain', [
        '#1a4d1a', '#2d6b2d', '#4a8c4a', '#8b8b4a', '#8b6b4a', '#6b4a2d', '#4a2d1a',
    ])

    extent = [p1_x_min, MAP_WIDTH, p1_y_max, 0]
    ax.imshow(terrain_p1, cmap=cmap, extent=extent, origin='upper', alpha=0.8)

    # HQ Spieler 1
    hq = HQ_POSITIONS[1]
    ax.scatter(hq[0], hq[1], c='gold', s=500, marker='s',
              edgecolors='white', linewidths=3, zorder=10)
    ax.annotate('HQ', (hq[0], hq[1]), color='black', fontsize=14,
               fontweight='bold', ha='center', va='center')

    # DZ
    dz = DZ_POSITIONS[1]
    ax.scatter(dz[0], dz[1], c='orange', s=300, marker='D',
              edgecolors='white', linewidths=2, zorder=9)
    ax.annotate('DZ', (dz[0], dz[1]), color='black', fontsize=12,
               fontweight='bold', ha='center', va='center')

    # DZ-Bauplätze für Spieler 1
    p1_dz_slots = [(34500, 23700), (43500, 9400)]  # Ohne das gebaute
    for pos in p1_dz_slots:
        ax.scatter(pos[0], pos[1], c='yellow', s=200, marker='D',
                  edgecolors='white', linewidths=2, zorder=8)
        dist = math.sqrt((pos[0]-hq[0])**2 + (pos[1]-hq[1])**2)
        ax.annotate(f'DZ-Slot\n{dist:.0f}', (pos[0], pos[1]),
                   color='white', fontsize=8, ha='center', va='top',
                   xytext=(0, -20), textcoords='offset points')

    # Ressourcen
    add_resources_to_axis(ax, map_data, player=1, show_labels=True)

    ax.set_xlim(p1_x_min - 2000, MAP_WIDTH + 1000)
    ax.set_ylim(p1_y_max + 2000, -1000)
    ax.set_title(title, fontsize=14, fontweight='bold', color='white')
    ax.set_xlabel('X', color='white')
    ax.set_ylabel('Y', color='white')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.3, color='white')


def create_player1_walkability(ax, terrain, map_data, title):
    """Zeigt begehbare Bereiche für Spieler 1."""

    walkable = create_walkable_mask(terrain, threshold=135)

    # Spieler 1 Bereich
    p1_x_min = int(MAP_WIDTH / 2)
    p1_y_max = int(MAP_HEIGHT / 2)

    g_x_min = int(p1_x_min / SCALE_X)
    g_y_max = int(p1_y_max / SCALE_Y)

    walkable_p1 = walkable[:g_y_max, g_x_min:]

    cmap = ListedColormap(['#4a1a1a', '#1a4a1a'])  # Dunkelrot, Dunkelgrün

    extent = [p1_x_min, MAP_WIDTH, p1_y_max, 0]
    ax.imshow(walkable_p1.astype(int), cmap=cmap, extent=extent, origin='upper', alpha=0.7)

    # HQ mit Radius-Kreisen für Distanzen
    hq = HQ_POSITIONS[1]
    ax.scatter(hq[0], hq[1], c='gold', s=400, marker='s',
              edgecolors='white', linewidths=3, zorder=10)

    # Distanz-Kreise
    for radius in [5000, 10000, 15000, 20000]:
        circle = plt.Circle((hq[0], hq[1]), radius, fill=False,
                            color='white', linestyle='--', alpha=0.5, linewidth=1)
        ax.add_patch(circle)
        ax.annotate(f'{radius/1000:.0f}km', (hq[0] + radius*0.7, hq[1] - radius*0.7),
                   color='white', fontsize=8, alpha=0.7)

    # Ressourcen mit Verbindungslinien
    add_resources_to_axis(ax, map_data, player=1, show_labels=True, show_connections=True, hq=hq)

    # Prüfe Begehbarkeit der Ressourcen
    check_resource_walkability(ax, map_data, walkable, player=1)

    ax.set_xlim(p1_x_min - 2000, MAP_WIDTH + 1000)
    ax.set_ylim(p1_y_max + 2000, -1000)
    ax.set_title(title, fontsize=14, fontweight='bold', color='white')
    ax.set_xlabel('X', color='white')
    ax.set_ylabel('Y', color='white')
    ax.tick_params(colors='white')

    # Legende
    legend_elements = [
        patches.Patch(facecolor='#1a4a1a', label='Begehbar'),
        patches.Patch(facecolor='#4a1a1a', label='Blockiert'),
        Line2D([0], [0], marker='s', color='gold', label='HQ', markersize=10, linestyle='None'),
        Line2D([0], [0], marker='^', color='gray', label='Minenschacht', markersize=10, linestyle='None'),
        Line2D([0], [0], marker='o', color='gold', label='Kl. Vorkommen', markersize=10, linestyle='None'),
        Line2D([0], [0], marker='^', color='green', label='Bäume', markersize=8, linestyle='None'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=9)


def add_resources_to_axis(ax, map_data, player=None, show_labels=False, show_connections=False, hq=None, alpha=1.0):
    """Fügt Ressourcen zum Plot hinzu."""

    p1_x_min = MAP_WIDTH / 2
    p1_y_max = MAP_HEIGHT / 2

    def in_player1(x, y):
        return x > p1_x_min and y < p1_y_max

    colors_mine = {'iron': '#8B4513', 'stone': '#696969', 'clay': '#CD853F', 'sulfur': '#FFD700'}
    colors_dep = {'iron': '#A0522D', 'stone': '#A9A9A9', 'clay': '#DEB887', 'sulfur': '#FFEC8B'}

    # Minenschächte
    for resource, slots in map_data['mine_slots'].items():
        for s in slots:
            x, y = s['position']['x'], s['position']['y']
            if player == 1 and not in_player1(x, y):
                continue
            ax.scatter(x, y, c=colors_mine[resource], s=150, marker='^',
                      edgecolors='white', linewidths=1, zorder=8, alpha=alpha)
            if show_labels:
                dist = math.sqrt((x - hq[0])**2 + (y - hq[1])**2) if hq else 0
                ax.annotate(f'{resource[:2].upper()}\n{dist:.0f}', (x, y),
                           color='white', fontsize=7, ha='center', va='top',
                           xytext=(0, -15), textcoords='offset points')
            if show_connections and hq:
                ax.plot([hq[0], x], [hq[1], y], color=colors_mine[resource],
                       linestyle=':', alpha=0.4, linewidth=1)

    # Kleine Vorkommen
    for resource, deps in map_data['deposits'].items():
        for d in deps:
            x, y = d['position']['x'], d['position']['y']
            if player == 1 and not in_player1(x, y):
                continue
            ax.scatter(x, y, c=colors_dep[resource], s=120, marker='o',
                      edgecolors='white', linewidths=1, zorder=8, alpha=alpha)
            if show_labels:
                dist = math.sqrt((x - hq[0])**2 + (y - hq[1])**2) if hq else 0
                ax.annotate(f'{resource[:2].upper()}\n{d["amount"]}\n{dist:.0f}', (x, y),
                           color='white', fontsize=6, ha='center', va='top',
                           xytext=(0, -15), textcoords='offset points')
            if show_connections and hq:
                ax.plot([hq[0], x], [hq[1], y], color=colors_dep[resource],
                       linestyle=':', alpha=0.3, linewidth=1)

    # Bäume (nur die nächsten 100)
    trees = [(t['position']['x'], t['position']['y']) for t in map_data['trees'][:200]]
    if player == 1:
        trees = [(x, y) for x, y in trees if in_player1(x, y)]

    if trees:
        tree_x, tree_y = zip(*trees[:100])
        ax.scatter(tree_x, tree_y, c='darkgreen', s=15, marker='^',
                  alpha=0.6, zorder=7)


def check_resource_walkability(ax, map_data, walkable, player=1):
    """
    Prüft ob Ressourcen-Positionen begehbar sind.

    HINWEIS: Alle Ressourcen-Positionen SIND im echten Spiel begehbar!
    Die Terrain-Datei zeigt nur Höhen, nicht die tatsächliche Blocking-Map.
    """

    p1_x_min = MAP_WIDTH / 2
    p1_y_max = MAP_HEIGHT / 2

    def in_player1(x, y):
        return x > p1_x_min and y < p1_y_max

    print("\n=== RESSOURCEN-POSITIONEN (alle sind begehbar!) ===")
    print("HINWEIS: Die Terrain-Datei zeigt Höhen, NICHT die Blocking-Map.")
    print("         Alle platzierten Ressourcen sind im Spiel erreichbar.\n")

    # Minenschächte
    print("Minenschächte (Spieler 1):")
    for resource, slots in map_data['mine_slots'].items():
        for s in slots:
            x, y = s['position']['x'], s['position']['y']
            if player == 1 and not in_player1(x, y):
                continue
            hq = HQ_POSITIONS[1]
            dist = math.sqrt((x-hq[0])**2 + (y-hq[1])**2)
            walk_time = dist / 360  # Serf speed
            print(f"  {resource}: ({x:.0f}, {y:.0f}) - Distanz: {dist:.0f} - Laufzeit: {walk_time:.1f}s")

    # Kleine Vorkommen
    print("\nKleine Vorkommen (Spieler 1):")
    for resource, deps in map_data['deposits'].items():
        for d in deps:
            x, y = d['position']['x'], d['position']['y']
            if player == 1 and not in_player1(x, y):
                continue
            hq = HQ_POSITIONS[1]
            dist = math.sqrt((x-hq[0])**2 + (y-hq[1])**2)
            walk_time = dist / 360
            print(f"  {resource}: ({x:.0f}, {y:.0f}) - Distanz: {dist:.0f} - Laufzeit: {walk_time:.1f}s")


def main():
    print("=" * 60)
    print("VOLLSTÄNDIGE KARTEN-VISUALISIERUNG")
    print("Mit Terrain und begehbaren Bereichen")
    print("=" * 60)

    print("\nLade Terrain-Daten...")
    terrain = load_terrain_data()
    print(f"  Terrain-Grid: {terrain.shape}")

    print("\nLade Kartendaten...")
    map_data = load_map_data()
    print(f"  Bäume: {len(map_data['trees'])}")

    print("\nErstelle Visualisierung...")
    output_path = r"c:\Users\marku\OneDrive\Desktop\siedler_ai\map_visualization.png"
    create_full_map_visualization(terrain, map_data, output_path)

    # Zusätzliche Statistik
    walkable = create_walkable_mask(terrain, threshold=135)
    print(f"\n=== TERRAIN-STATISTIK ===")
    print(f"Begehbar: {100*np.sum(walkable)/walkable.size:.1f}%")
    print(f"Blockiert: {100*(1-np.sum(walkable)/walkable.size):.1f}%")


if __name__ == "__main__":
    main()
