# -*- coding: utf-8 -*-
"""
Visualisiert die EMS Wintersturm Karte mit allen Ressourcen
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# Kartendaten laden
MAP_DATA_PATH = Path(r"c:\Users\marku\OneDrive\Desktop\siedler_ai\config\wintersturm_map_data.json")

def load_map_data():
    with open(MAP_DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def visualize_map():
    data = load_map_data()

    # Karten-Dimensionen
    MAP_WIDTH = 50480
    MAP_HEIGHT = 50496

    # HQ Positionen
    hq_positions = {
        1: (41100, 23100),
        2: (41100, 28200),
        3: (10200, 28200),
        4: (10200, 23100),
    }

    # Dorfzentrum Positionen
    dz_positions = {
        1: (39400, 24300),
        2: (39400, 27000),
        3: (11900, 27000),
        4: (11900, 24300),
    }

    # Spieler 1 Quadrant
    p1_min_x = MAP_WIDTH / 2
    p1_max_y = MAP_HEIGHT / 2

    # Figure erstellen
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))

    # === LINKES BILD: Ganze Karte ===
    ax1 = axes[0]
    ax1.set_xlim(0, MAP_WIDTH)
    ax1.set_ylim(0, MAP_HEIGHT)
    ax1.set_aspect('equal')
    ax1.set_title('EMS Wintersturm - Gesamte Karte', fontsize=14, fontweight='bold')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')

    # Quadranten markieren
    ax1.axhline(y=MAP_HEIGHT/2, color='gray', linestyle='--', alpha=0.5)
    ax1.axvline(x=MAP_WIDTH/2, color='gray', linestyle='--', alpha=0.5)

    # Spieler-Quadranten beschriften
    ax1.text(MAP_WIDTH*0.75, MAP_HEIGHT*0.25, 'Spieler 1', fontsize=12, ha='center', color='blue', fontweight='bold')
    ax1.text(MAP_WIDTH*0.75, MAP_HEIGHT*0.75, 'Spieler 2', fontsize=12, ha='center', color='green', fontweight='bold')
    ax1.text(MAP_WIDTH*0.25, MAP_HEIGHT*0.75, 'Spieler 3', fontsize=12, ha='center', color='red', fontweight='bold')
    ax1.text(MAP_WIDTH*0.25, MAP_HEIGHT*0.25, 'Spieler 4', fontsize=12, ha='center', color='orange', fontweight='bold')

    # HQs zeichnen
    for player, pos in hq_positions.items():
        colors = {1: 'blue', 2: 'green', 3: 'red', 4: 'orange'}
        ax1.scatter(pos[0], pos[1], c=colors[player], s=200, marker='s', edgecolors='black', linewidths=2, zorder=10)
        ax1.annotate(f'HQ{player}', (pos[0], pos[1]), textcoords="offset points", xytext=(10,10), fontsize=8)

    # Dorfzentren
    for player, pos in dz_positions.items():
        colors = {1: 'blue', 2: 'green', 3: 'red', 4: 'orange'}
        ax1.scatter(pos[0], pos[1], c=colors[player], s=100, marker='D', edgecolors='black', linewidths=1, zorder=9)

    # Alle Bäume (kleine grüne Punkte)
    tree_x = [t['position']['x'] for t in data['trees']]
    tree_y = [t['position']['y'] for t in data['trees']]
    ax1.scatter(tree_x, tree_y, c='darkgreen', s=1, alpha=0.3, label=f'Bäume ({len(tree_x)})')

    # Alle Minen-Slots
    colors_mine = {'iron': 'darkgray', 'stone': 'gray', 'clay': 'brown', 'sulfur': 'yellow'}
    for resource, slots in data['mine_slots'].items():
        x = [s['position']['x'] for s in slots]
        y = [s['position']['y'] for s in slots]
        ax1.scatter(x, y, c=colors_mine[resource], s=80, marker='^', edgecolors='black', linewidths=1, zorder=8)

    # Alle Deposits
    colors_dep = {'iron': 'silver', 'stone': 'lightgray', 'clay': 'peru', 'sulfur': 'gold'}
    for resource, deps in data['deposits'].items():
        x = [d['position']['x'] for d in deps]
        y = [d['position']['y'] for d in deps]
        ax1.scatter(x, y, c=colors_dep[resource], s=120, marker='o', edgecolors='black', linewidths=2, zorder=8)

    # === RECHTES BILD: Nur Spieler 1 Quadrant (Zoom) ===
    ax2 = axes[1]

    # Spieler 1 Bereich mit etwas Rand
    margin = 3000
    ax2.set_xlim(p1_min_x - margin, MAP_WIDTH + margin)
    ax2.set_ylim(0 - margin, p1_max_y + margin)
    ax2.set_aspect('equal')
    ax2.set_title('Spieler 1 Quadrant (Detail)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')

    # Quadrant-Grenzen
    ax2.axhline(y=p1_max_y, color='red', linestyle='--', alpha=0.7, linewidth=2, label='Quadrant-Grenze')
    ax2.axvline(x=p1_min_x, color='red', linestyle='--', alpha=0.7, linewidth=2)

    # HQ Spieler 1
    hq1 = hq_positions[1]
    ax2.scatter(hq1[0], hq1[1], c='blue', s=400, marker='s', edgecolors='black', linewidths=3, zorder=10)
    ax2.annotate('HQ', (hq1[0], hq1[1]), textcoords="offset points", xytext=(15,15), fontsize=12, fontweight='bold')

    # Dorfzentrum Spieler 1
    dz1 = dz_positions[1]
    ax2.scatter(dz1[0], dz1[1], c='blue', s=200, marker='D', edgecolors='black', linewidths=2, zorder=9)
    ax2.annotate('DZ', (dz1[0], dz1[1]), textcoords="offset points", xytext=(15,15), fontsize=10)

    # Bäume im Spieler 1 Bereich
    p1_trees = [(t['position']['x'], t['position']['y']) for t in data['trees']
                if t['position']['x'] > p1_min_x and t['position']['y'] < p1_max_y]
    if p1_trees:
        tree_x, tree_y = zip(*p1_trees)
        ax2.scatter(tree_x, tree_y, c='darkgreen', s=5, alpha=0.5, label=f'Bäume ({len(p1_trees)})')

    # Minenschächte/Stollen im Spieler 1 Bereich (wo Minen-Gebäude gebaut werden können)
    # KORREKTUR: mine_slots = Schächte/Stollen (XD_Iron1 etc.)
    labels_mine = {'iron': 'Eisen-Schacht', 'stone': 'Stein-Schacht', 'clay': 'Lehm-Schacht', 'sulfur': 'Schwefel-Schacht'}
    for resource, slots in data['mine_slots'].items():
        p1_slots = [s for s in slots if s['position']['x'] > p1_min_x and s['position']['y'] < p1_max_y]
        if p1_slots:
            x = [s['position']['x'] for s in p1_slots]
            y = [s['position']['y'] for s in p1_slots]
            ax2.scatter(x, y, c=colors_mine[resource], s=150, marker='^', edgecolors='black', linewidths=2,
                       zorder=8, label=f'{labels_mine[resource]} ({len(p1_slots)})')
            # Beschriftung
            for s in p1_slots:
                dist = ((s['position']['x']-hq1[0])**2 + (s['position']['y']-hq1[1])**2)**0.5
                ax2.annotate(f'{resource[0].upper()}-Schacht\n{dist:.0f}',
                           (s['position']['x'], s['position']['y']),
                           textcoords="offset points", xytext=(10,5), fontsize=7, ha='left')

    # Kleine Vorkommen im Spieler 1 Bereich (sammelbar durch Leibeigene)
    # KORREKTUR: deposits = Kleine Vorkommen/Pits (XD_IronPit1 etc.)
    labels_dep = {'iron': 'Eisen-Vork.', 'stone': 'Stein-Vork.', 'clay': 'Lehm-Vork.', 'sulfur': 'Schwefel-Vork.'}
    for resource, deps in data['deposits'].items():
        p1_deps = [d for d in deps if d['position']['x'] > p1_min_x and d['position']['y'] < p1_max_y]
        if p1_deps:
            x = [d['position']['x'] for d in p1_deps]
            y = [d['position']['y'] for d in p1_deps]
            ax2.scatter(x, y, c=colors_dep[resource], s=200, marker='o', edgecolors='black', linewidths=2,
                       zorder=8, label=f'{labels_dep[resource]} ({len(p1_deps)})')
            # Beschriftung
            for d in p1_deps:
                dist = ((d['position']['x']-hq1[0])**2 + (d['position']['y']-hq1[1])**2)**0.5
                ax2.annotate(f'{resource[0].upper()}-Vork.\n{d["amount"]}\n{dist:.0f}m',
                           (d['position']['x'], d['position']['y']),
                           textcoords="offset points", xytext=(10,5), fontsize=7, ha='left')

    # Dorfzentren-Bauplätze (noch nicht bebaut)
    if 'village_center_slots' in data:
        p1_dz_slots = [s for s in data['village_center_slots']
                       if s['position']['x'] > p1_min_x and s['position']['y'] < p1_max_y]
        if p1_dz_slots:
            x = [s['position']['x'] for s in p1_dz_slots]
            y = [s['position']['y'] for s in p1_dz_slots]
            ax2.scatter(x, y, c='cyan', s=150, marker='D', edgecolors='black', linewidths=2,
                       zorder=7, label=f'DZ-Bauplatz ({len(p1_dz_slots)})', alpha=0.7)
            for s in p1_dz_slots:
                dist = ((s['position']['x']-hq1[0])**2 + (s['position']['y']-hq1[1])**2)**0.5
                ax2.annotate(f'DZ-Platz\n{dist:.0f}',
                           (s['position']['x'], s['position']['y']),
                           textcoords="offset points", xytext=(10,5), fontsize=7, ha='left')

    # Verbindungslinien vom HQ zu Ressourcen
    for resource, slots in data['mine_slots'].items():
        p1_slots = [s for s in slots if s['position']['x'] > p1_min_x and s['position']['y'] < p1_max_y]
        for s in p1_slots:
            ax2.plot([hq1[0], s['position']['x']], [hq1[1], s['position']['y']],
                    color=colors_mine[resource], linestyle=':', alpha=0.3, linewidth=1)

    for resource, deps in data['deposits'].items():
        p1_deps = [d for d in deps if d['position']['x'] > p1_min_x and d['position']['y'] < p1_max_y]
        for d in p1_deps:
            ax2.plot([hq1[0], d['position']['x']], [hq1[1], d['position']['y']],
                    color=colors_dep[resource], linestyle=':', alpha=0.3, linewidth=1)

    ax2.legend(loc='upper left', fontsize=8)

    # Grid
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    # Speichern (ohne Anzeige)
    output_path = Path(r"c:\Users\marku\OneDrive\Desktop\siedler_ai\map_visualization.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Karte gespeichert: {output_path}")

    # Statistik ausgeben
    print("\n=== SPIELER 1 RESSOURCEN-ÜBERSICHT ===")
    print(f"\nBäume im Quadrant: {len(p1_trees)}")

    print("\nMinen-Slots (wo Minen gebaut werden können):")
    for resource, slots in data['mine_slots'].items():
        p1_slots = [s for s in slots if s['position']['x'] > p1_min_x and s['position']['y'] < p1_max_y]
        print(f"  {resource}: {len(p1_slots)} Slots")
        for s in p1_slots:
            dist = ((s['position']['x']-hq1[0])**2 + (s['position']['y']-hq1[1])**2)**0.5
            print(f"    ({s['position']['x']:.0f}, {s['position']['y']:.0f}) - Distanz: {dist:.0f}")

    print("\nDeposits (sammelbar ohne Mine, erschöpfbar):")
    for resource, deps in data['deposits'].items():
        p1_deps = [d for d in deps if d['position']['x'] > p1_min_x and d['position']['y'] < p1_max_y]
        if p1_deps:
            print(f"  {resource}: {len(p1_deps)} Deposits")
            for d in p1_deps:
                dist = ((d['position']['x']-hq1[0])**2 + (d['position']['y']-hq1[1])**2)**0.5
                print(f"    ({d['position']['x']:.0f}, {d['position']['y']:.0f}) - {d['amount']} Einheiten - Distanz: {dist:.0f}")


def visualize_walkable_grid():
    """
    Visualisiert das Begehbarkeits-Grid und zeigt wie Gebäude es beeinflussen.
    """
    import numpy as np
    from matplotlib.colors import ListedColormap
    import os

    base_dir = r"c:\Users\marku\OneDrive\Desktop\siedler_ai"
    walkable = np.load(os.path.join(base_dir, "player1_walkable.npy"))

    # Grid-Skalierung
    SCALE_X = 33.5
    SCALE_Y = 33.8
    OFFSET_X = 25240.0

    def world_to_grid(world_x, world_y):
        local_x = world_x - OFFSET_X
        local_y = world_y
        return int(local_x / SCALE_X), int(local_y / SCALE_Y)

    fig, axes = plt.subplots(1, 2, figsize=(18, 8))

    # Farbkarte: 0=blockiert (rot), 1=begehbar (grün)
    cmap = ListedColormap(['#8B0000', '#228B22'])

    # === LINKES BILD: Walkable Grid ===
    ax1 = axes[0]
    im1 = ax1.imshow(walkable, cmap=cmap, origin='lower', aspect='auto')

    # HQ markieren
    hq_grid = world_to_grid(41100, 23100)
    ax1.plot(hq_grid[0], hq_grid[1], 'y*', markersize=20, label='HQ')

    # Nächste Bäume
    from map_config_wintersturm import PLAYER_1_TREES_NEAREST
    for i, tree in enumerate(PLAYER_1_TREES_NEAREST[:10]):
        gx, gy = world_to_grid(tree["x"], tree["y"])
        ax1.plot(gx, gy, 'c^', markersize=8 if i > 0 else 12)
    ax1.plot([], [], 'c^', markersize=8, label='Bäume')

    # Statistik
    walkable_pct = np.mean(walkable) * 100
    ax1.set_title(f'Begehbarkeits-Grid (Spieler 1)\nGrün={walkable_pct:.1f}% begehbar, Rot=blockiert')
    ax1.set_xlabel(f'Grid X ({walkable.shape[1]} Pixel)')
    ax1.set_ylabel(f'Grid Y ({walkable.shape[0]} Pixel)')
    ax1.legend(loc='upper right')

    # === RECHTES BILD: Zoom auf HQ-Bereich ===
    ax2 = axes[1]

    # Zoom-Bereich um HQ
    zoom = 150
    x1, x2 = max(0, hq_grid[0]-zoom), min(walkable.shape[1], hq_grid[0]+zoom)
    y1, y2 = max(0, hq_grid[1]-zoom), min(walkable.shape[0], hq_grid[1]+zoom)

    im2 = ax2.imshow(walkable[y1:y2, x1:x2], cmap=cmap, origin='lower', aspect='auto')

    # HQ im Zoom
    ax2.plot(hq_grid[0]-x1, hq_grid[1]-y1, 'y*', markersize=25, label='HQ')

    # Bauplätze
    from map_config_wintersturm import BUILDING_ZONES_PLAYER_1
    for pos in BUILDING_ZONES_PLAYER_1["zone_a_immediate"][:15]:
        gx, gy = world_to_grid(pos["x"], pos["y"])
        if x1 <= gx < x2 and y1 <= gy < y2:
            rect = plt.Rectangle((gx-x1-5, gy-y1-5), 10, 10,
                                 linewidth=2, edgecolor='cyan', facecolor='none')
            ax2.add_patch(rect)
    ax2.plot([], [], 'c-', linewidth=2, label='Bauplätze')

    # Bäume im Zoom
    for tree in PLAYER_1_TREES_NEAREST[:20]:
        gx, gy = world_to_grid(tree["x"], tree["y"])
        if x1 <= gx < x2 and y1 <= gy < y2:
            ax2.plot(gx-x1, gy-y1, 'lime', marker='^', markersize=10)
    ax2.plot([], [], 'g^', markersize=10, label='Bäume')

    ax2.set_title('Zoom: HQ-Bereich\nCyan=verfügbare Bauplätze')
    ax2.legend(loc='upper right')

    plt.tight_layout()

    output_path = Path(r"c:\Users\marku\OneDrive\Desktop\siedler_ai\walkable_grid.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nBegehbarkeits-Grid gespeichert: {output_path}")

    # Info ausgeben
    print(f"\n=== WALKABLE GRID INFO ===")
    print(f"Grid-Größe: {walkable.shape[1]} x {walkable.shape[0]} Pixel")
    print(f"Begehbar: {walkable_pct:.1f}%")
    print(f"Skalierung: 1 Pixel = {SCALE_X:.1f} x {SCALE_Y:.1f} Spieleinheiten")
    print(f"Quadrant-Offset: ({OFFSET_X}, 0)")


def visualize_building_impact():
    """
    Zeigt wie ein Gebäude die Begehbarkeit verändert.
    """
    import numpy as np
    from matplotlib.colors import ListedColormap
    import os
    from pathfinding import MapManager, BUILDING_SIZES

    base_dir = r"c:\Users\marku\OneDrive\Desktop\siedler_ai"
    walkable = np.load(os.path.join(base_dir, "player1_walkable.npy"))

    SCALE_X = 33.5
    OFFSET_X = 25240.0

    def world_to_grid(world_x, world_y):
        local_x = world_x - OFFSET_X
        return int(local_x / SCALE_X), int(world_y / 33.8)

    # Gebäude-Position (erster Bauplatz)
    building_pos = (40900, 22900)
    building_type = "Wohnhaus"

    # Manager erstellen
    manager = MapManager()
    manager.grid.load_terrain_from_array(walkable.copy())

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    cmap = ListedColormap(['#8B0000', '#228B22'])

    # Grid VORHER
    grid_before = manager.grid.get_walkable_grid()

    # Gebäude hinzufügen
    local_x, local_y = manager.to_local_coords(building_pos[0], building_pos[1])
    building_id = manager.grid.add_building(local_x, local_y, building_type)

    # Grid NACHHER
    grid_after = manager.grid.get_walkable_grid()

    # Differenz
    diff = grid_before.astype(int) - grid_after.astype(int)

    # Zoom auf Gebäude
    gx, gy = world_to_grid(building_pos[0], building_pos[1])
    zoom = 40
    x1, x2 = max(0, gx-zoom), min(walkable.shape[1], gx+zoom)
    y1, y2 = max(0, gy-zoom), min(walkable.shape[0], gy+zoom)

    # VORHER
    axes[0].imshow(grid_before[y1:y2, x1:x2], cmap=cmap, origin='lower')
    axes[0].axhline(gy-y1, color='yellow', linestyle='--', alpha=0.7)
    axes[0].axvline(gx-x1, color='yellow', linestyle='--', alpha=0.7)
    axes[0].set_title('VORHER\n(ohne Gebäude)')

    # NACHHER
    axes[1].imshow(grid_after[y1:y2, x1:x2], cmap=cmap, origin='lower')
    axes[1].axhline(gy-y1, color='yellow', linestyle='--', alpha=0.7)
    axes[1].axvline(gx-x1, color='yellow', linestyle='--', alpha=0.7)
    axes[1].set_title(f'NACHHER\n(mit {building_type})')

    # DIFFERENZ
    cmap_diff = ListedColormap(['white', 'red'])
    axes[2].imshow(diff[y1:y2, x1:x2], cmap=cmap_diff, origin='lower')
    axes[2].axhline(gy-y1, color='blue', linestyle='--', alpha=0.7)
    axes[2].axvline(gx-x1, color='blue', linestyle='--', alpha=0.7)
    blocked = np.sum(diff > 0)
    axes[2].set_title(f'DIFFERENZ\n(Rot = {blocked} neu blockierte Zellen)')

    size = BUILDING_SIZES.get(building_type, 400)
    fig.suptitle(f'Gebäude-Impact: {building_type} bei ({building_pos[0]}, {building_pos[1]})\n'
                f'Gebäudegröße: {size} Einheiten → blockiert {blocked} Grid-Zellen', fontsize=12)

    plt.tight_layout()

    output_path = Path(r"c:\Users\marku\OneDrive\Desktop\siedler_ai\building_impact.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nGebäude-Impact gespeichert: {output_path}")

    print(f"\n=== GEBÄUDE-IMPACT ===")
    print(f"Gebäudetyp: {building_type}")
    print(f"Position: {building_pos}")
    print(f"Größe: {size} Spieleinheiten")
    print(f"Blockierte Zellen: {blocked}")
    print(f"\n→ JA, Gebäude blockieren die Begehbarkeit!")


if __name__ == "__main__":
    print("=" * 60)
    print("SIEDLER AI - MAP VISUALISIERUNG")
    print("=" * 60)

    # 1. Ressourcen-Karte
    print("\n1. Erstelle Ressourcen-Karte...")
    visualize_map()

    # 2. Begehbarkeits-Grid
    print("\n2. Erstelle Begehbarkeits-Grid...")
    visualize_walkable_grid()

    # 3. Gebäude-Impact
    print("\n3. Erstelle Gebäude-Impact Visualisierung...")
    visualize_building_impact()

    print("\n" + "=" * 60)
    print("FERTIG! Alle Visualisierungen wurden gespeichert.")
    print("=" * 60)
