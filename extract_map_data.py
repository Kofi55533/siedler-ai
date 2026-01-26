# -*- coding: utf-8 -*-
"""
Extrahiert Kartendaten aus der mapdata.xml von EMS Wintersturm
"""

import re
import json
from pathlib import Path

MAP_DATA_PATH = Path(r"C:\Users\marku\OneDrive\Desktop\wintersturm_extracted\mapdata.xml")
OUTPUT_PATH = Path(r"c:\Users\marku\OneDrive\Desktop\siedler_ai\config\wintersturm_map_data.json")

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
        "deposits": {
            "iron": [],
            "stone": [],
            "clay": [],
            "sulfur": [],
        },
        "mine_slots": {
            "iron": [],
            "stone": [],
            "clay": [],
            "sulfur": [],
        },
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

    # Deposit-Typen (kleine sammelbare Vorkommen)
    deposit_types = {
        "XD_IronPit1": "iron",
        "XD_StonePit1": "stone",
        "XD_ClayPit1": "clay",
        "XD_SulfurPit1": "sulfur",
    }

    # Minen-Slots (wo man Minen bauen kann) - XD_Iron1, XD_Stone1, etc.
    mine_slot_types = {
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

        # Deposits (sammelbare Ressourcen)
        elif entity_type in deposit_types:
            resource = deposit_types[entity_type]
            # Extrahiere Menge aus Script
            amount = 4000  # Default
            amount_match = re.search(r'SetResourceDoodadGoodAmount\([^,]+,(\d+)\)', script)
            if amount_match:
                amount = int(amount_match.group(1))

            data["deposits"][resource].append({
                "position": position,
                "amount": amount
            })

        # Minen-Slots (exakter Match, nicht startswith - da XD_Iron1 != XD_IronPit1)
        elif entity_type in mine_slot_types:
            resource = mine_slot_types[entity_type]
            data["mine_slots"][resource].append({
                "position": position,
                "type": entity_type
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

    # Zusammenfassung
    data["summary"] = {
        "total_trees": len(data["trees"]),
        "deposits": {
            "iron": len(data["deposits"]["iron"]),
            "stone": len(data["deposits"]["stone"]),
            "clay": len(data["deposits"]["clay"]),
            "sulfur": len(data["deposits"]["sulfur"]),
        },
        "mine_slots": {
            "iron": len(data["mine_slots"]["iron"]),
            "stone": len(data["mine_slots"]["stone"]),
            "clay": len(data["mine_slots"]["clay"]),
            "sulfur": len(data["mine_slots"]["sulfur"]),
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
    print(f"\nDeposits (sammelbar ohne Mine):")
    for res, count in data['summary']['deposits'].items():
        if count > 0:
            print(f"  {res}: {count}")
    print(f"\nMinen-Slots (baubar):")
    for res, count in data['summary']['mine_slots'].items():
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

    print("\n=== MINEN-SLOTS (Spieler 1 Bereich) ===")
    for resource in ["iron", "stone", "clay", "sulfur"]:
        slots = [s for s in data["mine_slots"][resource] if in_player1_quadrant(s['position'])]
        if slots:
            print(f"\n{resource.upper()} Minen-Slots ({len(slots)} Stück):")
            for s in sorted(slots, key=lambda x: ((x['position']['x']-hq_x)**2 + (x['position']['y']-hq_y)**2)**0.5):
                dist = ((s['position']['x']-hq_x)**2 + (s['position']['y']-hq_y)**2)**0.5
                print(f"  ({s['position']['x']:.0f}, {s['position']['y']:.0f}) - Distanz: {dist:.0f}")

    print("\n=== DEPOSIT-DETAILS (Spieler 1 Bereich) ===")
    for resource in ["iron", "stone", "clay", "sulfur"]:
        deposits = [d for d in data["deposits"][resource] if in_player1_quadrant(d['position'])]
        if deposits:
            print(f"\n{resource.upper()} Deposits ({len(deposits)} Stück):")
            for d in sorted(deposits, key=lambda x: ((x['position']['x']-hq_x)**2 + (x['position']['y']-hq_y)**2)**0.5):
                dist = ((d['position']['x']-hq_x)**2 + (d['position']['y']-hq_y)**2)**0.5
                print(f"  ({d['position']['x']:.0f}, {d['position']['y']:.0f}) - {d['amount']} Einheiten - Distanz: {dist:.0f}")


if __name__ == "__main__":
    main()
