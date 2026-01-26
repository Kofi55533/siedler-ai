# -*- coding: utf-8 -*-
"""
Extrahiert und analysiert die Blocking-Map / Höhenkarte aus den Siedler 5 Kartendaten.
Ziel: Begehbare vs. nicht-begehbare Bereiche identifizieren.
"""

import struct
import numpy as np
import os

# Pfade
EXTRACTED_DIR = r"C:\Users\marku\OneDrive\Desktop\wintersturm_extracted"
TERRAIN_FILE = os.path.join(EXTRACTED_DIR, "file_0.bin")

# Karten-Dimensionen (aus mapdata.xml)
MAP_WIDTH = 50480
MAP_HEIGHT = 50496


def analyze_terrain_file():
    """Analysiert die Terrain-Datei und versucht das Format zu erkennen."""

    if not os.path.exists(TERRAIN_FILE):
        print(f"FEHLER: {TERRAIN_FILE} nicht gefunden!")
        return None

    file_size = os.path.getsize(TERRAIN_FILE)
    print(f"Terrain-Datei: {TERRAIN_FILE}")
    print(f"Dateigröße: {file_size:,} bytes")

    # Siedler 5 verwendet typischerweise eine Terrain-Grid-Auflösung
    # Die Karte ist 50480x50496 Spieleinheiten
    # Typische Grid-Größen: 100, 200, 400 Einheiten pro Zelle

    possible_grids = []
    for cell_size in [100, 200, 400, 500, 800, 1000]:
        grid_w = MAP_WIDTH // cell_size
        grid_h = MAP_HEIGHT // cell_size
        pixels = grid_w * grid_h

        # Prüfe verschiedene Bytes pro Pixel
        for bpp in [1, 2, 4]:
            expected_size = pixels * bpp
            if expected_size == file_size:
                possible_grids.append({
                    "cell_size": cell_size,
                    "grid_w": grid_w,
                    "grid_h": grid_h,
                    "bpp": bpp,
                    "match": "EXACT"
                })
            elif abs(expected_size - file_size) < 1000:
                possible_grids.append({
                    "cell_size": cell_size,
                    "grid_w": grid_w,
                    "grid_h": grid_h,
                    "bpp": bpp,
                    "match": "CLOSE",
                    "diff": expected_size - file_size
                })

    print(f"\nMögliche Grid-Konfigurationen:")
    for g in possible_grids:
        print(f"  Cell: {g['cell_size']}, Grid: {g['grid_w']}x{g['grid_h']}, "
              f"BPP: {g['bpp']}, Match: {g['match']}")

    # Lade die Datei
    with open(TERRAIN_FILE, 'rb') as f:
        data = f.read()

    # Header-Analyse
    print(f"\nHeader-Analyse (erste 64 Bytes):")
    header = data[:64]
    print(f"  Hex: {header[:32].hex()}")

    # Versuche als verschiedene Integer-Typen
    print(f"\n  Als uint32 (LE): {struct.unpack('<16I', header)}")
    print(f"  Als uint16 (LE): {struct.unpack('<32H', header)[:16]}")

    # Suche nach bekannten Magic Numbers oder Patterns
    # Siedler 5 .s5x Dateien könnten spezielle Header haben

    # Versuche die Daten als 8-bit Höhenkarte zu interpretieren
    # und prüfe die Verteilung
    print(f"\nWert-Analyse (als uint8):")
    arr = np.frombuffer(data, dtype=np.uint8)
    print(f"  Min: {arr.min()}, Max: {arr.max()}")
    print(f"  Mean: {arr.mean():.2f}, Std: {arr.std():.2f}")
    print(f"  Unique values: {len(np.unique(arr))}")

    # Histogramm der Werte
    hist, edges = np.histogram(arr, bins=16)
    print(f"\n  Histogramm (16 bins):")
    for i, count in enumerate(hist):
        low = int(edges[i])
        high = int(edges[i+1])
        bar = '#' * (count * 50 // max(hist))
        print(f"    {low:3d}-{high:3d}: {bar} ({count:,})")

    # Prüfe ob es eine Blocking-Map sein könnte (viele 0/1 oder 0/255 Werte)
    zero_count = np.sum(arr == 0)
    one_count = np.sum(arr == 1)
    max_count = np.sum(arr == 255)

    print(f"\n  Spezielle Werte:")
    print(f"    Nullen (0): {zero_count:,} ({100*zero_count/len(arr):.1f}%)")
    print(f"    Einsen (1): {one_count:,} ({100*one_count/len(arr):.1f}%)")
    print(f"    Max (255): {max_count:,} ({100*max_count/len(arr):.1f}%)")

    return data, arr


def try_visualize_as_heightmap(data, width, height, output_name):
    """Versucht die Daten als Höhenkarte zu visualisieren."""
    try:
        import matplotlib.pyplot as plt
        from matplotlib.colors import LinearSegmentedColormap
    except ImportError:
        print("Matplotlib nicht verfügbar!")
        return

    expected_size = width * height

    if len(data) >= expected_size:
        # Als uint8
        arr = np.frombuffer(data[:expected_size], dtype=np.uint8)
        arr = arr.reshape((height, width))

        fig, ax = plt.subplots(figsize=(12, 12))

        # Terrain-Colormap (grün = niedrig/begehbar, braun = hoch/Berge)
        cmap = LinearSegmentedColormap.from_list('terrain',
            ['darkgreen', 'green', 'yellowgreen', 'yellow', 'orange', 'brown', 'white'])

        im = ax.imshow(arr, cmap=cmap, origin='upper')
        plt.colorbar(im, ax=ax, label='Höhe/Blocking-Wert')

        ax.set_title(f'Terrain-Visualisierung ({width}x{height})')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        output_path = f"terrain_{output_name}.png"
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        plt.close()
        print(f"Visualisierung gespeichert: {output_path}")

        return arr
    else:
        print(f"Nicht genug Daten für {width}x{height}")
        return None


def analyze_blocking_patterns(arr, threshold=128):
    """Analysiert begehbare vs. blockierte Bereiche."""

    # Annahme: niedrige Werte = begehbar, hohe Werte = blockiert
    walkable = arr < threshold
    blocked = arr >= threshold

    walkable_count = np.sum(walkable)
    blocked_count = np.sum(blocked)
    total = len(arr.flatten())

    print(f"\nBlocking-Analyse (Threshold={threshold}):")
    print(f"  Begehbar: {walkable_count:,} ({100*walkable_count/total:.1f}%)")
    print(f"  Blockiert: {blocked_count:,} ({100*blocked_count/total:.1f}%)")

    return walkable, blocked


def main():
    print("=" * 60)
    print("TERRAIN / BLOCKING-MAP ANALYSE")
    print("=" * 60)

    result = analyze_terrain_file()
    if result is None:
        return

    data, arr = result

    # Versuche verschiedene Grid-Größen
    print("\n" + "=" * 60)
    print("VISUALISIERUNG")
    print("=" * 60)

    # Basierend auf Dateigröße 2,255,968 bytes:
    # sqrt(2255968) ≈ 1502 -> könnte 1502x1502 sein (aber nicht genau)
    # 2255968 / 2 = 1127984 -> sqrt ≈ 1062
    # Oder: 1504 x 1500 = 2,256,000 (fast!)
    # Oder: 1508 x 1496 = 2,255,968 EXACT!

    print("\nVersuche 1508 x 1496 Grid...")
    arr_grid = try_visualize_as_heightmap(data, 1508, 1496, "1508x1496")

    if arr_grid is not None:
        analyze_blocking_patterns(arr_grid, threshold=128)

        # Berechne Skalierung zur Spielkarte
        scale_x = MAP_WIDTH / 1508
        scale_y = MAP_HEIGHT / 1496
        print(f"\n  Skalierung: 1 Grid-Pixel = {scale_x:.1f} x {scale_y:.1f} Spieleinheiten")

        # Mappe HQ-Position auf Grid
        hq_x, hq_y = 41100, 23100
        grid_x = int(hq_x / scale_x)
        grid_y = int(hq_y / scale_y)
        print(f"  HQ ({hq_x}, {hq_y}) -> Grid ({grid_x}, {grid_y})")
        if 0 <= grid_x < 1508 and 0 <= grid_y < 1496:
            print(f"  Wert bei HQ: {arr_grid[grid_y, grid_x]}")


if __name__ == "__main__":
    main()
