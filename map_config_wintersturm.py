# -*- coding: utf-8 -*-
"""
EMS Wintersturm - Karten-Konfiguration
Extrahiert aus der echten Kartendatei
"""

# =============================================================================
# KARTEN-GRUNDDATEN
# =============================================================================

MAP_NAME = "EMS Wintersturm"
MAP_SIZE = (50480, 50496)  # Breite x Höhe in Spieleinheiten
PLAYERS = 4
GAME_MODE = "2v2"  # Teams: Spieler 1+2 vs Spieler 3+4

# =============================================================================
# SPIELER-STARTPOSITIONEN (Hauptquartier)
# =============================================================================

PLAYER_HQ_POSITIONS = {
    1: {"x": 41100, "y": 23100},
    2: {"x": 41100, "y": 28200},
    3: {"x": 10200, "y": 28200},
    4: {"x": 10200, "y": 23100},
}

# Teams
TEAMS = {
    "team_1": [1, 2],
    "team_2": [3, 4],
}

# =============================================================================
# STARTRESSOURCEN (aus EMS Config)
# =============================================================================

START_RESOURCES = {
    "GoldRoh": 500,
    "LehmRoh": 2400,
    "HolzRoh": 1750,
    "SteinRoh": 700,
    "EisenRoh": 50,
    "SchwefelRoh": 50,
}

# =============================================================================
# STARTGEBÄUDE PRO SPIELER (aus mapdata.xml extrahiert)
# =============================================================================

PLAYER_START_BUILDINGS = {
    1: [
        {"type": "Hauptquartier_1", "position": {"x": 41100, "y": 23100}},
        {"type": "Dorfzentrum_1", "position": {"x": 39400, "y": 24300}},
    ],
    2: [
        {"type": "Hauptquartier_1", "position": {"x": 41100, "y": 28200}},
        {"type": "Dorfzentrum_1", "position": {"x": 39400, "y": 27000}},
    ],
    3: [
        {"type": "Hauptquartier_1", "position": {"x": 10200, "y": 28200}},
        {"type": "Dorfzentrum_1", "position": {"x": 11900, "y": 27000}},
    ],
    4: [
        {"type": "Hauptquartier_1", "position": {"x": 10200, "y": 23100}},
        {"type": "Dorfzentrum_1", "position": {"x": 11900, "y": 24300}},
    ],
}

# =============================================================================
# DORFZENTREN-BAUPLÄTZE PRO SPIELER (XD_VillageCenter)
# Positionen wo Dorfzentren gebaut werden können
# =============================================================================

PLAYER_1_VILLAGE_CENTER_SLOTS = [
    {"x": 39400, "y": 24300, "distance_to_hq": 2080, "status": "built"},
    {"x": 34500, "y": 23700, "distance_to_hq": 6627, "status": "free"},
    {"x": 43500, "y": 9400, "distance_to_hq": 13908, "status": "free"},
]

# =============================================================================
# STOLLEN PRO SPIELER
# XD_Iron1, XD_Stone1, XD_Clay1, XD_Sulfur1
# WICHTIG: Das sind Serf-Sammelpunkte (nicht Mine-Bauplätze).
# =============================================================================

# Canonical engine semantics: XD_*1/2/3 are 400-unit resource nodes.
# They are collectable by serfs and are never mine construction sites.
PLAYER_1_SMALL_RESOURCE_NODES = {
    "Eisenmine": [
        {"x": 36275.84, "y": 8927.04, "amount": 400, "distance_to_hq": 14971},
        {"x": 37495.02, "y": 7801.38, "amount": 400, "distance_to_hq": 15717},
        {"x": 37784.37, "y": 7265.83, "amount": 400, "distance_to_hq": 16177},
    ],
    "Steinmine": [
        {"x": 40056.03, "y": 14890.56, "amount": 400, "distance_to_hq": 8275},
        {"x": 39320.85, "y": 14715.73, "amount": 400, "distance_to_hq": 8570},
        {"x": 38633.13, "y": 14720.38, "amount": 400, "distance_to_hq": 8735},
    ],
    "Lehmmine": [
        {"x": 35180.72, "y": 19552.98, "amount": 400, "distance_to_hq": 6900},
        {"x": 35106.41, "y": 18871.68, "amount": 400, "distance_to_hq": 7334},
        {"x": 34991.41, "y": 17996.99, "amount": 400, "distance_to_hq": 7959},
    ],
    "Schwefelmine": [
        {"x": 44304.14, "y": 21484.33, "amount": 400, "distance_to_hq": 3588},
        {"x": 44005.73, "y": 20978.49, "amount": 400, "distance_to_hq": 3597},
        {"x": 44576.42, "y": 22119.58, "amount": 400, "distance_to_hq": 3612},
    ],
}

# Legacy-Name: XD_*1/2/3 are collectable small resource nodes, not mine sites.
PLAYER_1_MINE_SHAFTS = PLAYER_1_SMALL_RESOURCE_NODES

# =============================================================================
# VORKOMMEN PRO SPIELER (XD_*Pit1)
# Diese Positionen sind die Mine-Bauplätze im Originalspiel.
# Leibeigene können dort sammeln, solange keine Mine gebaut wurde.
# Original defaults: Eisen/Lehm 12000, Stein 14000, Schwefel 8000.
# =============================================================================

PLAYER_1_MINE_PITS = {
    "Eisen": [
        {"x": 34325.0, "y": 7950.0, "amount": 12000, "distance_to_hq": 16595},
        {"x": 36325.0, "y": 6750.0, "amount": 12000, "distance_to_hq": 17033},
    ],
    "Stein": [
        {"x": 42800.0, "y": 15100.0, "amount": 14000, "distance_to_hq": 8178},
    ],
    "Lehm": [
        {"x": 31125.0, "y": 18750.0, "amount": 12000, "distance_to_hq": 10882},
    ],
    "Schwefel": [
        {"x": 48125.0, "y": 20950.0, "amount": 8000, "distance_to_hq": 7346},
        {"x": 47725.0, "y": 18550.0, "amount": 8000, "distance_to_hq": 8036},
    ],
}

# Legacy-Name retained for existing environment consumers. XD_*Pit1 are the
# actual mine build sites and pre-mine resource sources.
PLAYER_1_SMALL_DEPOSITS = PLAYER_1_MINE_PITS

# Zusammenfassung der Ressourcen pro Spieler
RESOURCES_PER_PLAYER = {
    "shafts": {
        "Eisenmine": 3,
        "Steinmine": 3,
        "Lehmmine": 3,
        "Schwefelmine": 3,
    },
    "small_resource_nodes": {
        "Eisen": {"count": 3, "total_amount": 1200},
        "Stein": {"count": 3, "total_amount": 1200},
        "Lehm": {"count": 3, "total_amount": 1200},
        "Schwefel": {"count": 3, "total_amount": 1200},
    },
    "mine_pits": {
        "Eisen": {"count": 2, "total_amount": 24000},
        "Stein": {"count": 1, "total_amount": 14000},
        "Lehm": {"count": 1, "total_amount": 12000},
        "Schwefel": {"count": 2, "total_amount": 16000},
    },
    "mine_build_slots": {
        "Eisen": {"count": 2, "total_amount": 24000},
        "Stein": {"count": 1, "total_amount": 14000},
        "Lehm": {"count": 1, "total_amount": 12000},
        "Schwefel": {"count": 2, "total_amount": 16000},
    },
    "trees": {"count": 202, "wood_per_tree": 75, "total_wood": 15150},
}

# Legacy-Kompatibilität (wird noch von environment.py verwendet)
PLAYER_1_MINE_BUILD_SLOTS = {
    "Eisenmine": PLAYER_1_MINE_PITS["Eisen"],
    "Steinmine": PLAYER_1_MINE_PITS["Stein"],
    "Lehmmine": PLAYER_1_MINE_PITS["Lehm"],
    "Schwefelmine": PLAYER_1_MINE_PITS["Schwefel"],
}
PLAYER_1_MINE_POSITIONS = PLAYER_1_MINE_BUILD_SLOTS  # Alias (genutzt von environment.py)
MINES_PER_PLAYER = {
    "Steinmine": {"count": 1, "capacity": 14000},
    "Eisenmine": {"count": 2, "capacity": 24000},
    "Lehmmine": {"count": 1, "capacity": 12000},
    "Schwefelmine": {"count": 2, "capacity": 16000},
}
DEPOSITS_PER_PLAYER = {
    "Stein": {"count": 1, "capacity": 14000},
    "Eisen": {"count": 2, "capacity": 24000},
    "Lehm": {"count": 1, "capacity": 12000},
    "Schwefel": {"count": 2, "capacity": 16000},
}

# =============================================================================
# BÄUME (HOLZ) PRO SPIELER
# Extrahiert aus mapdata.xml - Spieler 1 Quadrant
# Jeder Baum hat ResourceAmount=75, jede Extraktion gibt 2 Holz
# = 37 Extraktionen pro Baum, dann verschwindet er
# =============================================================================

PLAYER_1_TREES_SUMMARY = {
    "total_trees": 202,
    "wood_per_tree": 75,
    "extractions_per_tree": 37,  # 75 / 2 = 37 (abgerundet)
    "estimated_wood": 15150,  # 202 * 75
    "tree_types": {
        "XD_Fir1": 97,
        "XD_Fir2": 105,
    },
    "nearest_tree_distance": 1542,
    "average_distance": 12599,
}

# Die 50 nächsten Bäume zum HQ (für schnelles Holzsammeln am Anfang)
PLAYER_1_TREES_NEAREST = [
    {"x": 42330.0, "y": 24030.0, "type": "XD_PineNorth3", "distance_to_hq": 1542},
    {"x": 41745.01, "y": 21625.85, "type": "XD_Fir1_small", "distance_to_hq": 1609},
    {"x": 42423.56, "y": 22173.18, "type": "XD_Fir2_small", "distance_to_hq": 1616},
    {"x": 42280.0, "y": 21879.22, "type": "XD_Fir1_small", "distance_to_hq": 1698},
    {"x": 41780.0, "y": 21531.76, "type": "XD_Fir2", "distance_to_hq": 1709},
    {"x": 41854.17, "y": 21529.4, "type": "XD_Fir2_small", "distance_to_hq": 1742},
    {"x": 42934.41, "y": 23180.0, "type": "XD_Fir2_small", "distance_to_hq": 1836},
    {"x": 42920.0, "y": 22820.0, "type": "XD_Fir1_small", "distance_to_hq": 1841},
    {"x": 42948.17, "y": 23123.9, "type": "XD_Fir2_small", "distance_to_hq": 1848},
    {"x": 42920.0, "y": 23420.0, "type": "XD_Fir2", "distance_to_hq": 1848},
    {"x": 43075.51, "y": 23120.0, "type": "XD_Fir2_small", "distance_to_hq": 1976},
    {"x": 43109.36, "y": 23270.0, "type": "XD_PineNorth2", "distance_to_hq": 2017},
    {"x": 41169.3, "y": 21056.69, "type": "XD_Fir1", "distance_to_hq": 2044},
    {"x": 43170.0, "y": 23270.0, "type": "XD_PineNorth2", "distance_to_hq": 2077},
    {"x": 43180.0, "y": 23080.0, "type": "XD_Fir1_small", "distance_to_hq": 2080},
    {"x": 43179.96, "y": 23180.0, "type": "XD_Fir2_small", "distance_to_hq": 2081},
    {"x": 40980.0, "y": 20980.0, "type": "XD_Fir2_small", "distance_to_hq": 2123},
    {"x": 43223.4, "y": 23475.51, "type": "XD_PineNorth2", "distance_to_hq": 2156},
    {"x": 41852.76, "y": 21052.08, "type": "XD_Fir1_small", "distance_to_hq": 2182},
    {"x": 42980.0, "y": 21953.13, "type": "XD_Fir1_small", "distance_to_hq": 2202},
    {"x": 43135.46, "y": 23954.63, "type": "XD_Fir1_small", "distance_to_hq": 2208},
    {"x": 41023.74, "y": 20880.0, "type": "XD_Fir2_small", "distance_to_hq": 2221},
    {"x": 43228.61, "y": 23880.0, "type": "XD_Fir1_small", "distance_to_hq": 2267},
    {"x": 42580.0, "y": 21380.0, "type": "XD_Fir2_small", "distance_to_hq": 2269},
    {"x": 43254.34, "y": 23945.36, "type": "XD_Fir2_small", "distance_to_hq": 2314},
    {"x": 42874.47, "y": 21580.0, "type": "XD_Fir2_small", "distance_to_hq": 2336},
    {"x": 42320.0, "y": 21058.2, "type": "XD_Fir2_small", "distance_to_hq": 2379},
    {"x": 42780.0, "y": 21380.0, "type": "XD_Fir2", "distance_to_hq": 2404},
    {"x": 42420.0, "y": 21080.0, "type": "XD_Fir1_small", "distance_to_hq": 2413},
    {"x": 42880.0, "y": 21454.35, "type": "XD_Fir1_small", "distance_to_hq": 2424},
    {"x": 43403.15, "y": 24006.23, "type": "XD_PineNorth2", "distance_to_hq": 2475},
    {"x": 43469.97, "y": 23820.0, "type": "XD_Fir2", "distance_to_hq": 2477},
    {"x": 41380.0, "y": 20560.69, "type": "XD_Fir2", "distance_to_hq": 2555},
    {"x": 42262.39, "y": 20820.0, "type": "XD_Fir2_small", "distance_to_hq": 2559},
    {"x": 43220.0, "y": 21657.26, "type": "XD_Fir1", "distance_to_hq": 2564},
    {"x": 43460.07, "y": 24180.0, "type": "XD_Fir1_small", "distance_to_hq": 2595},
    {"x": 43680.0, "y": 22659.26, "type": "XD_Fir1_small", "distance_to_hq": 2617},
    {"x": 42435.5, "y": 20847.56, "type": "XD_Fir2_small", "distance_to_hq": 2619},
    {"x": 41730.0, "y": 20530.0, "type": "XD_DarkTree6", "distance_to_hq": 2646},
    {"x": 43520.0, "y": 24178.24, "type": "XD_Fir2", "distance_to_hq": 2649},
    {"x": 41820.0, "y": 20545.95, "type": "XD_Fir1", "distance_to_hq": 2654},
    {"x": 43380.0, "y": 21720.0, "type": "XD_Fir2_small", "distance_to_hq": 2665},
    {"x": 42880.0, "y": 21078.44, "type": "XD_Fir2_small", "distance_to_hq": 2694},
    {"x": 43552.17, "y": 24220.7, "type": "XD_Fir2_small", "distance_to_hq": 2696},
    {"x": 43456.44, "y": 24420.7, "type": "XD_Fir1_small", "distance_to_hq": 2701},
    {"x": 43520.0, "y": 24330.11, "type": "XD_Fir2_small", "distance_to_hq": 2715},
    {"x": 43620.0, "y": 24171.56, "type": "XD_Fir1_small", "distance_to_hq": 2738},
    {"x": 43742.58, "y": 22346.54, "type": "XD_Fir1_small", "distance_to_hq": 2748},
    {"x": 43033.99, "y": 21120.0, "type": "XD_Fir1_small", "distance_to_hq": 2768},
    {"x": 43720.0, "y": 24037.17, "type": "XD_Fir2_small", "distance_to_hq": 2783},
]

# =============================================================================
# SPIELREGELN (aus EMS Config)
# =============================================================================

GAME_RULES = {
    "peacetime_minutes": 40,
    "max_time_minutes": 30,  # Unser Trainingsziel: 30 Min

    # Erlaubte Einheiten und deren Max-Level
    "units": {
        "Schwert": 0,  # VERBOTEN
        "Bogen": 4,
        "Speer": 4,
        "SchwereKavallerie": 0,  # VERBOTEN
        "LeichteKavallerie": 0,  # VERBOTEN
        "Scharfschütze": 2,  # Max Level 2
        "Dieb": 1,
        "Kundschafter": 1,
    },

    # Verbotene Gebäude/Features
    "forbidden": [
        "Markt",
        "Brücke",
        "Kanone",
    ],

    # Türme
    "tower_level": 1,  # Nur Wachtürme

    # Helden
    "heroes_per_player": 0,
}

# =============================================================================
# BAUZONEN FÜR SPIELER 1 (extrahiert aus MapData.xml)
# =============================================================================

# Sofort bebaubare Positionen (Zone A) - sortiert nach Distanz zum HQ
BUILDING_ZONES_PLAYER_1 = {
    "zone_a_immediate": [
        # Die 20 nächsten freien Bauplätze
        {"x": 40900, "y": 22900, "distance": 283},
        {"x": 40900, "y": 23300, "distance": 283},
        {"x": 41300, "y": 22900, "distance": 283},
        {"x": 40500, "y": 22900, "distance": 632},
        {"x": 40500, "y": 23300, "distance": 632},
        {"x": 40900, "y": 22500, "distance": 632},
        {"x": 40900, "y": 23700, "distance": 632},
        {"x": 41300, "y": 22500, "distance": 632},
        {"x": 41300, "y": 23700, "distance": 632},
        {"x": 41700, "y": 22900, "distance": 632},
        {"x": 41700, "y": 23300, "distance": 632},
        {"x": 40500, "y": 22500, "distance": 849},
        {"x": 40500, "y": 23700, "distance": 849},
        {"x": 41700, "y": 22500, "distance": 849},
        {"x": 41700, "y": 23700, "distance": 849},
        {"x": 40100, "y": 22900, "distance": 1000},
        {"x": 40100, "y": 23300, "distance": 1000},
        {"x": 42100, "y": 22900, "distance": 1000},
        {"x": 42100, "y": 23300, "distance": 1000},
        {"x": 40900, "y": 22100, "distance": 1000},
    ],

    # Positionen die nach Holzfällen frei werden (Zone B)
    "zone_b_after_logging": [
        {"x": 42100, "y": 21700, "distance": 1720, "trees_to_remove": 1},
        {"x": 42500, "y": 22100, "distance": 1720, "trees_to_remove": 1},
        {"x": 42500, "y": 24100, "distance": 1720, "trees_to_remove": 1},
        {"x": 42900, "y": 22900, "distance": 1811, "trees_to_remove": 1},
        {"x": 40900, "y": 20900, "distance": 2209, "trees_to_remove": 2},
        {"x": 42900, "y": 21700, "distance": 2280, "trees_to_remove": 1},
        {"x": 42900, "y": 21300, "distance": 2546, "trees_to_remove": 3},
        {"x": 41300, "y": 20500, "distance": 2608, "trees_to_remove": 1},
        {"x": 43300, "y": 21700, "distance": 2608, "trees_to_remove": 2},
        {"x": 43700, "y": 22500, "distance": 2668, "trees_to_remove": 2},
    ],

    # Zusammenfassung
    "summary": {
        "immediate_slots": 1962,
        "after_logging_slots": 238,
        "blocked_permanent": 290,
        "trees_in_area": 538,
        "rocks_in_area": 524,
    }
}

# =============================================================================
# GEBÄUDE-GRÖßEN (für Platzierungslogik)
# =============================================================================

BUILDING_SIZES = {
    # Kleine Gebäude (400x400 Einheiten)
    "small": ["Wohnhaus", "Bauernhof", "Sägemühle", "Steinmetz"],

    # Mittlere Gebäude (600x600 Einheiten)
    "medium": ["Hochschule", "Schmiede", "Büchsenmacherei", "Kaserne", "Bogenmacher"],

    # Große Gebäude (800x800 Einheiten)
    "large": ["Hauptquartier", "Dorfzentrum"],

    # Minen (an festen Positionen)
    "mine": ["Steinmine", "Eisenmine", "Lehmmine", "Schwefelmine"],
}

BUILDING_FOOTPRINT = {
    "small": 400,
    "medium": 600,
    "large": 800,
}

# =============================================================================
# SCHARFSCHÜTZEN-PFAD (optimale Reihenfolge)
# =============================================================================

SCHARFSCHUETZEN_PATH = {
    "technologies": [
        {"name": "Mathematik", "time": 20, "cost": {"Taler": 100, "Holz": 200}},
        {"name": "Fernglas", "time": 30, "cost": {"Taler": 300, "Eisen": 300}, "requires_building": "Hauptquartier_2"},
        {"name": "Luntenschloss", "time": 50, "cost": {"Eisen": 300, "Schwefel": 300}},
    ],

    "buildings": [
        {"name": "Hochschule_1", "time": 120, "cost": {"Holz": 300, "Stein": 400}},
        {"name": "Hauptquartier_2", "time": 90, "cost": {"Stein": 800, "Lehm": 300, "Taler": 500}, "is_upgrade": True},
        {"name": "Büchsenmacherei_1", "time": 120, "cost": {"Stein": 400, "Schwefel": 300, "Eisen": 200}},
    ],

    "unit": {
        "name": "Scharfschütze",
        "cost": {"Taler": 100, "Schwefel": 50},
        "building_required": "Büchsenmacherei_1",
    },

    # Kritische Ressourcen die gesammelt werden müssen
    "critical_resources": {
        "Eisen": {"start": 50, "needed": 800, "deficit": 750},
        "Schwefel": {"start": 50, "needed": 650, "deficit": 600},
    }
}

# =============================================================================
# HILFS-FUNKTIONEN
# =============================================================================

def get_mirrored_position(pos, player_id):
    """Spiegelt eine Position für andere Spieler basierend auf Spieler 1"""
    map_center_x = MAP_SIZE[0] / 2
    map_center_y = MAP_SIZE[1] / 2

    if player_id == 1:
        return pos
    elif player_id == 2:
        # Spieler 2: Gespiegelt an Y-Achse (gleiche X, andere Y)
        return {"x": pos["x"], "y": map_center_y + (map_center_y - pos["y"])}
    elif player_id == 3:
        # Spieler 3: Gespiegelt an beiden Achsen
        return {"x": map_center_x - (pos["x"] - map_center_x), "y": map_center_y + (map_center_y - pos["y"])}
    elif player_id == 4:
        # Spieler 4: Gespiegelt an X-Achse
        return {"x": map_center_x - (pos["x"] - map_center_x), "y": pos["y"]}

    return pos

def get_building_positions_for_player(player_id):
    """Gibt die Baupositionen für einen bestimmten Spieler zurück"""
    if player_id == 1:
        return BUILDING_ZONES_PLAYER_1
    else:
        # Spiegele alle Positionen
        mirrored = {"zone_a_immediate": [], "zone_b_after_logging": []}

        for pos in BUILDING_ZONES_PLAYER_1["zone_a_immediate"]:
            new_pos = get_mirrored_position(pos, player_id)
            new_pos["distance"] = pos["distance"]
            mirrored["zone_a_immediate"].append(new_pos)

        for pos in BUILDING_ZONES_PLAYER_1["zone_b_after_logging"]:
            new_pos = get_mirrored_position(pos, player_id)
            new_pos["distance"] = pos["distance"]
            new_pos["trees_to_remove"] = pos["trees_to_remove"]
            mirrored["zone_b_after_logging"].append(new_pos)

        mirrored["summary"] = BUILDING_ZONES_PLAYER_1["summary"]
        return mirrored
