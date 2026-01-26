# -*- coding: utf-8 -*-
"""
Analysiert die Wintersturm-Karte:
1. Alle Dorfzentren-Bauplätze
2. Begehbare Bereiche (Terrain/Höhenkarte)
"""

import xml.etree.ElementTree as ET
import json
import struct
import os
import math

# Karten-Dimensionen
MAP_WIDTH = 50480
MAP_HEIGHT = 50496

# Spieler 1 Quadrant: rechts oben
# x > MAP_WIDTH/2, y < MAP_HEIGHT/2
PLAYER_1_MIN_X = MAP_WIDTH / 2  # 25240
PLAYER_1_MAX_Y = MAP_HEIGHT / 2  # 25248

# HQ Positionen
PLAYER_HQ = {
    1: (41100, 23100),
    2: (41100, 28200),
    3: (10200, 28200),
    4: (10200, 23100),
}


def extract_village_centers(mapdata_path):
    """Extrahiert alle Dorfzentren-Bauplätze aus mapdata.xml"""
    tree = ET.parse(mapdata_path)
    root = tree.getroot()

    village_centers = []

    for entity in root.iter():
        # Suche nach Entities mit ScriptName="XD_VillageCenter"
        script_name = entity.find('.//ScriptName')
        if script_name is not None and script_name.text == "XD_VillageCenter":
            pos = entity.find('.//Position')
            if pos is not None:
                x = float(pos.get('X', 0))
                y = float(pos.get('Y', 0))
                village_centers.append({
                    "x": x,
                    "y": y,
                })

    # Alternative Suche: Alle Entities mit dem Namen durchgehen
    if len(village_centers) < 12:
        for entity in root.findall('.//Entity'):
            for child in entity:
                if child.tag == 'ScriptName' and child.text == 'XD_VillageCenter':
                    pos = entity.find('.//Position')
                    if pos is not None:
                        x = float(pos.get('X', 0))
                        y = float(pos.get('Y', 0))
                        entry = {"x": x, "y": y}
                        if entry not in village_centers:
                            village_centers.append(entry)

    return village_centers


def assign_to_player(x, y):
    """Weist eine Position einem Spieler zu basierend auf Quadrant"""
    center_x = MAP_WIDTH / 2
    center_y = MAP_HEIGHT / 2

    if x > center_x and y < center_y:
        return 1  # Rechts oben
    elif x > center_x and y > center_y:
        return 2  # Rechts unten
    elif x < center_x and y > center_y:
        return 3  # Links unten
    else:
        return 4  # Links oben


def distance(p1, p2):
    """Berechnet Distanz zwischen zwei Punkten"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def analyze_terrain_binary(bin_path):
    """
    Versucht die Terrain-/Höhendaten aus der .bin Datei zu lesen.
    Format ist unklar, wir versuchen verschiedene Interpretationen.
    """
    if not os.path.exists(bin_path):
        print(f"WARNUNG: {bin_path} nicht gefunden")
        return None

    file_size = os.path.getsize(bin_path)
    print(f"Terrain-Datei: {bin_path}")
    print(f"Dateigröße: {file_size} bytes")

    # Mögliche Interpretationen:
    # 1. Höhenkarte als 16-bit oder 8-bit Werte
    # 2. Blocking-Map als Bitmap

    # Berechne mögliche Dimensionen
    possible_dims = []
    for bits in [8, 16, 32]:
        bytes_per_pixel = bits // 8
        total_pixels = file_size // bytes_per_pixel

        # Suche nach passenden Dimensionen
        for w in range(100, 2000):
            if total_pixels % w == 0:
                h = total_pixels // w
                if 100 < h < 2000:
                    possible_dims.append((w, h, bits))

    print(f"Mögliche Dimensionen: {possible_dims[:10]}")

    # Lese erste Bytes zur Analyse
    with open(bin_path, 'rb') as f:
        header = f.read(100)
        print(f"Erste 100 Bytes (hex): {header[:50].hex()}")

        # Versuche als Höhenwerte zu interpretieren
        f.seek(0)
        data = f.read()

        # Als 8-bit unsigned
        values_8bit = list(data[:1000])
        unique_8bit = len(set(values_8bit))
        print(f"Erste 1000 Bytes als uint8: min={min(values_8bit)}, max={max(values_8bit)}, unique={unique_8bit}")

        # Als 16-bit unsigned little-endian
        values_16bit = struct.unpack(f'<{len(data)//2}H', data[:len(data)//2*2])[:500]
        unique_16bit = len(set(values_16bit))
        print(f"Erste 500 Werte als uint16: min={min(values_16bit)}, max={max(values_16bit)}, unique={unique_16bit}")

    return None


def main():
    mapdata_path = r"C:\Users\marku\OneDrive\Desktop\wintersturm_extracted\mapdata.xml"
    terrain_path = r"C:\Users\marku\OneDrive\Desktop\wintersturm_extracted\file_0.bin"

    print("=" * 60)
    print("DORFZENTREN-BAUPLÄTZE")
    print("=" * 60)

    # Extrahiere alle DZ-Bauplätze
    village_centers = extract_village_centers(mapdata_path)
    print(f"\nGefunden: {len(village_centers)} Dorfzentren-Bauplätze\n")

    # Sortiere nach Spieler
    by_player = {1: [], 2: [], 3: [], 4: []}

    for vc in village_centers:
        player = assign_to_player(vc["x"], vc["y"])
        hq = PLAYER_HQ[player]
        dist = distance((vc["x"], vc["y"]), hq)
        vc["player"] = player
        vc["distance_to_hq"] = int(dist)
        by_player[player].append(vc)

    # Ausgabe pro Spieler
    for player in [1, 2, 3, 4]:
        print(f"\n--- Spieler {player} ---")
        print(f"HQ: {PLAYER_HQ[player]}")
        slots = sorted(by_player[player], key=lambda x: x["distance_to_hq"])
        for i, slot in enumerate(slots):
            print(f"  DZ-Slot {i+1}: ({slot['x']:.0f}, {slot['y']:.0f}) - Distanz: {slot['distance_to_hq']}")

    print("\n" + "=" * 60)
    print("SPIELER 1 - DORFZENTREN DETAILS")
    print("=" * 60)

    p1_slots = sorted(by_player[1], key=lambda x: x["distance_to_hq"])

    # Prüfe welcher Slot bereits bebaut ist (Dorfzentrum_1 bei 39400, 24300)
    built_dz = (39400, 24300)

    print("\n| # | Position | Distanz | Status |")
    print("|---|----------|---------|--------|")
    for i, slot in enumerate(p1_slots):
        is_built = abs(slot['x'] - built_dz[0]) < 100 and abs(slot['y'] - built_dz[1]) < 100
        status = "GEBAUT" if is_built else "frei"
        print(f"| {i+1} | ({slot['x']:.0f}, {slot['y']:.0f}) | {slot['distance_to_hq']} | {status} |")

    # Speichere für map_config
    print("\n\n# Python-Code für map_config_wintersturm.py:")
    print("PLAYER_1_VILLAGE_CENTER_SLOTS = [")
    for slot in p1_slots:
        is_built = abs(slot['x'] - built_dz[0]) < 100 and abs(slot['y'] - built_dz[1]) < 100
        status = '"built"' if is_built else '"free"'
        print(f'    {{"x": {int(slot["x"])}, "y": {int(slot["y"])}, "distance_to_hq": {slot["distance_to_hq"]}, "status": {status}}},')
    print("]")

    print("\n" + "=" * 60)
    print("TERRAIN-ANALYSE")
    print("=" * 60)

    analyze_terrain_binary(terrain_path)

    # Versuche auch die anderen bin-Dateien
    for fname in ["file_1.bin", "block_5.bin", "data_2.bin"]:
        fpath = os.path.join(r"C:\Users\marku\OneDrive\Desktop\wintersturm_extracted", fname)
        if os.path.exists(fpath):
            print(f"\n--- {fname} ---")
            size = os.path.getsize(fpath)
            print(f"Größe: {size} bytes")
            with open(fpath, 'rb') as f:
                header = f.read(50)
                print(f"Header: {header[:30].hex()}")


if __name__ == "__main__":
    main()
