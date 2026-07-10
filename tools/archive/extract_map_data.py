# -*- coding: utf-8 -*-
"""
Extrahiert Kartendaten aus der mapdata.xml von EMS Wintersturm
"""

import re
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from map_extract_config import EXTRACTED_DIR

MAP_DATA_PATH = EXTRACTED_DIR / "mapdata.xml"
OUTPUT_PATH = ROOT_DIR / "config" / "wintersturm_map_data.json"

RESOURCE_KEYS = ("iron", "stone", "clay", "sulfur")
PIT_DEFAULT_AMOUNTS = {
    "iron": 12000,
    "stone": 14000,
    "clay": 12000,
    "sulfur": 8000,
}
SMALL_NODE_DEFAULT_AMOUNT = 400


def _resource_buckets():
    return {resource: [] for resource in RESOURCE_KEYS}


def _resource_amount(script: str, default: int) -> int:
    match = re.search(r"SetResourceDoodadGoodAmount\\([^,]+,(\\d+)\\)", script or "")
    return int(match.group(1)) if match else int(default)

def parse_entities():
    """Parst alle Entities aus der mapdata.xml"""

    content = MAP_DATA_PATH.read_text(encoding='utf-8')

    # Regex für Entity-Blöcke
    entity_pattern = re.compile(
        r'<Entity[^>]*>.*?'
        r'<Type>([^<]+)</Type>.*?'
        r'<X>([^<]+)</X>.*?'
        r'<Y>([^<]+)</Y>.*?'
        r'<PlayerID>(\d+)</PlayerID>.*?'
        r'(?:<ScriptCommandLine>([^<]*)</ScriptCommandLine>)?.*?'
        r'</Entity>',
        re.DOTALL
    )

    # Kategorisierte Daten
    data = {
        "players": {
            1: {"buildings": [], "units": []},
            2: {"buildings": [], "units": []},
            3: {"buildings": [], "units": []},
            4: {"buildings": [], "units": []},
        },
        "mine_pits": _resource_buckets(),
        "small_resource_nodes": _resource_buckets(),
        "trees": [],
        "summary": {}
    }

    # Gebäude-Typen die uns interessieren
    building_types = {
        "PB_Headquarters1": "Hauptquartier_1",
        "PB_Headquarters2": "Hauptquartier_2",
        "PB_Headquarters3": "Hauptquartier_3",
        "PB_VillageCenter1": "Dorfzentrum_1",
        "PB_VillageCenter2": "Dorfzentrum_2",
        "PB_VillageCenter3": "Dorfzentrum_3",
        "PB_Farm1": "Bauernhof_1",
        "PB_Farm2": "Bauernhof_2",
        "PB_Farm3": "Bauernhof_3",
        "PB_Residence1": "Wohnhaus_1",
        "PB_Residence2": "Wohnhaus_2",
        "PB_Residence3": "Wohnhaus_3",
        "PB_Storehouse1": "Lagerhaus_1",
        "PB_University1": "Hochschule_1",
        "PB_University2": "Hochschule_2",
    }

    # XD_*Pit1 are the large mine pits. Original PB_*Mine entities use them
    # via <BuildOn>, while serfs may gather there before a mine exists.
    mine_pit_types = {
        "XD_IronPit1": "iron",
        "XD_StonePit1": "stone",
        "XD_ClayPit1": "clay",
        "XD_SulfurPit1": "sulfur",
    }

    # XD_*1/2/3 are small 400-unit resource nodes, not mine build slots.
    small_resource_node_types = {
        "XD_Iron1": "iron",
        "XD_Stone1": "stone",
        "XD_Clay1": "clay",
        "XD_Sulfur1": "sulfur",
    }

    # Baum-Typen
    tree_types = ["XD_Fir", "XD_Tree", "XD_DarkTree", "XD_Pine"]

    # Dorfzentren-Bauplätze (noch nicht bebaut)
    village_center_slot = "XD_VillageCenter"

    # Einheiten-Typen
    unit_types = {
        "PU_Serf": "Leibeigener",
    }

    # Dorfzentren-Bauplätze Liste
    data["village_center_slots"] = []

    for match in entity_pattern.finditer(content):
        entity_type = match.group(1)
        x = float(match.group(2))
        y = float(match.group(3))
        player_id = int(match.group(4))
        script = match.group(5) or ""

        position = {"x": x, "y": y}

        # Gebäude
        if entity_type in building_types:
            if player_id in data["players"]:
                data["players"][player_id]["buildings"].append({
                    "type": building_types[entity_type],
                    "original_type": entity_type,
                    "position": position
                })

        # Large mine pit: the original PB_*Mine entity is built on it.
        elif entity_type in mine_pit_types:
            resource = mine_pit_types[entity_type]
            data["mine_pits"][resource].append({
                "position": position,
                "amount": _resource_amount(script, PIT_DEFAULT_AMOUNTS[resource]),
                "original_type": entity_type,
                "entity_kind": "mine_pit",
                "buildable_mine": resource,
            })

        # Small resource node: directly collectable but not a mine build slot.
        elif entity_type in small_resource_node_types:
            resource = small_resource_node_types[entity_type]
            data["small_resource_nodes"][resource].append({
                "position": position,
                "amount": _resource_amount(script, SMALL_NODE_DEFAULT_AMOUNT),
                "original_type": entity_type,
                "entity_kind": "small_resource_node",
            })

        # Bäume
        elif any(entity_type.startswith(tt) for tt in tree_types):
            data["trees"].append({
                "position": position,
                "type": entity_type
            })

        # Dorfzentren-Bauplätze
        elif entity_type == village_center_slot:
            data["village_center_slots"].append({
                "position": position,
                "type": entity_type
            })

        # Einheiten
        elif entity_type in unit_types:
            if player_id in data["players"]:
                data["players"][player_id]["units"].append({
                    "type": unit_types[entity_type],
                    "original_type": entity_type,
                    "position": position
                })

    # Keep the historical keys as aliases so older map consumers continue to
    # read the same coordinate sets, while canonical keys describe the engine
    # entities correctly.
    data["deposits"] = data["mine_pits"]
    data["mine_slots"] = data["small_resource_nodes"]

    mine_pit_summary = {resource: len(data["mine_pits"][resource]) for resource in RESOURCE_KEYS}
    small_node_summary = {resource: len(data["small_resource_nodes"][resource]) for resource in RESOURCE_KEYS}
    data["summary"] = {
        "total_trees": len(data["trees"]),
        "mine_pits": mine_pit_summary,
        "small_resource_nodes": small_node_summary,
        "deposits": mine_pit_summary,
        "mine_slots": small_node_summary,
        "legacy_aliases": {
            "deposits": "mine_pits",
            "mine_slots": "small_resource_nodes",
        },
    }

    for player_id in [1, 2, 3, 4]:
        data["summary"][f"player_{player_id}_buildings"] = len(data["players"][player_id]["buildings"])
        data["summary"][f"player_{player_id}_units"] = len(data["players"][player_id]["units"])

    return data


def main():
    print("Extrahiere Kartendaten aus mapdata.xml...")

    data = parse_entities()

    # Ausgabe
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nDaten gespeichert in: {OUTPUT_PATH}")
    print("\n=== ZUSAMMENFASSUNG ===")
    print(f"Bäume: {data['summary']['total_trees']}")
    print(f"\nMinenplaetze/Gruben (baubar, vor Mine sammelbar):")
    for res, count in data['summary']['mine_pits'].items():
        if count > 0:
            print(f"  {res}: {count}")
    print(f"\nKleine Ressourcenklumpen (nicht baubar):")
    for res, count in data['summary']['small_resource_nodes'].items():
        if count > 0:
            print(f"  {res}: {count}")

    print("\n=== SPIELER-STARTGEBÄUDE ===")
    for player_id in [1, 2, 3, 4]:
        buildings = data["players"][player_id]["buildings"]
        units = data["players"][player_id]["units"]
        if buildings or units:
            print(f"\nSpieler {player_id}:")
            for b in buildings:
                print(f"  - {b['type']} @ ({b['position']['x']:.0f}, {b['position']['y']:.0f})")
            for u in units:
                print(f"  - {u['type']} @ ({u['position']['x']:.0f}, {u['position']['y']:.0f})")

    # Karten-Dimensionen (symmetrisch)
    MAP_WIDTH = 50480
    MAP_HEIGHT = 50496

    # Spieler 1 ist im Quadrant: x > MAP_WIDTH/2, y < MAP_HEIGHT/2 (rechts unten auf Karte)
    # Aber die Y-Achse ist invertiert, also: x > 25240, y < 25248

    print("\n=== SPIELER 1 QUADRANT (rechte untere Hälfte) ===")
    print(f"Quadrant: x > {MAP_WIDTH/2:.0f}, y < {MAP_HEIGHT/2:.0f}")

    hq_x, hq_y = 41100, 23100

    # Filtere nur Spieler 1 Quadrant
    def in_player1_quadrant(pos):
        # Spieler 1: rechte Seite (x > Mitte) UND untere Hälfte (y < Mitte)
        # HQ1 = (41100, 23100), HQ2 = (41100, 28200)
        # Spieler 1 hat y < 25248, Spieler 2 hat y > 25248
        return pos['x'] > MAP_WIDTH / 2 and pos['y'] < MAP_HEIGHT / 2

    print("\n=== KLEINE RESSOURCENKLUMPEN (Spieler 1 Bereich) ===")
    for resource in ["iron", "stone", "clay", "sulfur"]:
        slots = [s for s in data["small_resource_nodes"][resource] if in_player1_quadrant(s['position'])]
        if slots:
            print(f"\n{resource.upper()} Klumpen ({len(slots)} Stück):")
            for s in sorted(slots, key=lambda x: ((x['position']['x']-hq_x)**2 + (x['position']['y']-hq_y)**2)**0.5):
                dist = ((s['position']['x']-hq_x)**2 + (s['position']['y']-hq_y)**2)**0.5
                print(f"  ({s['position']['x']:.0f}, {s['position']['y']:.0f}) - Distanz: {dist:.0f}")

    print("\n=== MINENGRUBEN-DETAILS (Spieler 1 Bereich) ===")
    for resource in ["iron", "stone", "clay", "sulfur"]:
        deposits = [d for d in data["mine_pits"][resource] if in_player1_quadrant(d['position'])]
        if deposits:
            print(f"\n{resource.upper()} Gruben ({len(deposits)} Stück):")
            for d in sorted(deposits, key=lambda x: ((x['position']['x']-hq_x)**2 + (x['position']['y']-hq_y)**2)**0.5):
                dist = ((d['position']['x']-hq_x)**2 + (d['position']['y']-hq_y)**2)**0.5
                print(f"  ({d['position']['x']:.0f}, {d['position']['y']:.0f}) - {d['amount']} Einheiten - Distanz: {dist:.0f}")


if __name__ == "__main__":
    main()
