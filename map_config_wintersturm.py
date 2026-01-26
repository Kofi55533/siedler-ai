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
    "Taler": 500,
    "Lehm": 2400,
    "Holz": 1750,
    "Stein": 700,
    "Eisen": 50,
    "Schwefel": 50,
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
    {"x": 39400, "y": 24300, "distance_to_hq": 2081, "status": "built"},  # Bereits gebaut!
    {"x": 34500, "y": 23700, "distance_to_hq": 6627, "status": "free"},
    {"x": 43500, "y": 9400, "distance_to_hq": 13909, "status": "free"},
]

# =============================================================================
# MINENSCHÄCHTE/STOLLEN PRO SPIELER (wo Minen-Gebäude gebaut werden können)
# Extrahiert aus mapdata.xml - nur Spieler 1 Quadrant
# XD_Iron1, XD_Stone1, etc. = Schächte für Minen-Gebäude
# =============================================================================

# Schächte sind feste Positionen auf der Karte wo Minen-Gebäude gebaut werden MÜSSEN
PLAYER_1_MINE_SHAFTS = {
    "Eisenmine": [
        {"x": 36276, "y": 8927, "distance_to_hq": 14971},
        {"x": 37495, "y": 7801, "distance_to_hq": 15718},
        {"x": 37784, "y": 7266, "distance_to_hq": 16178},
    ],
    "Steinmine": [
        {"x": 40056, "y": 14891, "distance_to_hq": 8276},
        {"x": 39321, "y": 14716, "distance_to_hq": 8571},
        {"x": 38633, "y": 14720, "distance_to_hq": 8735},
    ],
    "Lehmmine": [
        {"x": 35181, "y": 19553, "distance_to_hq": 6901},
        {"x": 35106, "y": 18872, "distance_to_hq": 7335},
        {"x": 34991, "y": 17997, "distance_to_hq": 7960},
    ],
    "Schwefelmine": [
        {"x": 44304, "y": 21484, "distance_to_hq": 3588},
        {"x": 44006, "y": 20978, "distance_to_hq": 3598},
        {"x": 44576, "y": 22120, "distance_to_hq": 3612},
    ],
}

# =============================================================================
# KLEINE VORKOMMEN PRO SPIELER (sammelbar durch Leibeigene OHNE Mine)
# XD_IronPit1, XD_StonePit1, etc. = Kleine Vorkommen
# Diese verschwinden wenn leer! Kapazität = 4000 Einheiten
# =============================================================================

PLAYER_1_SMALL_DEPOSITS = {
    "Eisen": [
        {"x": 34325, "y": 7950, "amount": 4000, "distance_to_hq": 16596},
        {"x": 36325, "y": 6750, "amount": 4000, "distance_to_hq": 17033},
    ],
    "Stein": [
        {"x": 42800, "y": 15100, "amount": 4000, "distance_to_hq": 8179},
    ],
    "Lehm": [
        {"x": 31125, "y": 18750, "amount": 4000, "distance_to_hq": 10882},
    ],
    "Schwefel": [
        {"x": 48125, "y": 20950, "amount": 4000, "distance_to_hq": 7347},
        {"x": 47725, "y": 18550, "amount": 4000, "distance_to_hq": 8037},
    ],
}

# Zusammenfassung der Ressourcen pro Spieler
RESOURCES_PER_PLAYER = {
    "mine_shafts": {  # Schächte wo Minen gebaut werden können
        "Eisenmine": 3,
        "Steinmine": 3,
        "Lehmmine": 3,
        "Schwefelmine": 3,
    },
    "small_deposits": {  # Kleine Vorkommen (erschöpfbar)
        "Eisen": {"count": 2, "total_amount": 8000},
        "Stein": {"count": 1, "total_amount": 4000},
        "Lehm": {"count": 1, "total_amount": 4000},
        "Schwefel": {"count": 2, "total_amount": 8000},
    },
    "trees": 888,  # Bäume für Holz
}

# Legacy-Kompatibilität (wird noch von environment.py verwendet)
PLAYER_1_MINE_POSITIONS = PLAYER_1_MINE_SHAFTS
PLAYER_1_MINE_SLOTS = PLAYER_1_MINE_SHAFTS  # Alias
PLAYER_1_DEPOSITS = PLAYER_1_SMALL_DEPOSITS  # Alias
MINES_PER_PLAYER = {
    "Steinmine": {"count": 3, "capacity": 100000},
    "Eisenmine": {"count": 3, "capacity": 100000},
    "Lehmmine": {"count": 3, "capacity": 100000},
    "Schwefelmine": {"count": 3, "capacity": 100000},
}
DEPOSITS_PER_PLAYER = {
    "Stein": {"count": 1, "capacity": 4000},
    "Eisen": {"count": 2, "capacity": 8000},
    "Lehm": {"count": 1, "capacity": 4000},
    "Schwefel": {"count": 2, "capacity": 8000},
}

# =============================================================================
# BÄUME (HOLZ) PRO SPIELER
# Extrahiert aus mapdata.xml - Spieler 1 Quadrant
# Jeder Baum gibt 2 Holz bei Extraktion, verschwindet danach
# =============================================================================

PLAYER_1_TREES_SUMMARY = {
    "total_trees": 888,
    "estimated_wood": 1776,  # 888 * 2 Holz pro Baum
    "tree_types": {
        "XD_Fir2_small": 298,
        "XD_Fir1_small": 267,
        "XD_Fir2": 105,
        "XD_Fir1": 96,
        "XD_PineNorth3": 35,
        "XD_PineNorth1": 28,
        "XD_PineNorth2": 23,
        "XD_DarkTree": 36,  # Verschiedene DarkTree-Typen zusammen
    },
    "nearest_tree_distance": 1542,  # Nächster Baum zum HQ
    "average_distance": 8000,  # Geschätzt
}

# Die 50 nächsten Bäume zum HQ (für schnelles Holzsammeln am Anfang)
PLAYER_1_TREES_NEAREST = [
    {"x": 42330, "y": 24030, "type": "XD_PineNorth3", "distance_to_hq": 1542},
    {"x": 41745, "y": 21626, "type": "XD_Fir1_small", "distance_to_hq": 1609},
    {"x": 42424, "y": 22173, "type": "XD_Fir2_small", "distance_to_hq": 1616},
    {"x": 42280, "y": 21879, "type": "XD_Fir1_small", "distance_to_hq": 1698},
    {"x": 41780, "y": 21532, "type": "XD_Fir2", "distance_to_hq": 1709},
    {"x": 41854, "y": 21529, "type": "XD_Fir2_small", "distance_to_hq": 1742},
    {"x": 42934, "y": 23180, "type": "XD_Fir2_small", "distance_to_hq": 1836},
    {"x": 42920, "y": 22820, "type": "XD_Fir1_small", "distance_to_hq": 1841},
    {"x": 42920, "y": 23420, "type": "XD_Fir2", "distance_to_hq": 1848},
    {"x": 42948, "y": 23124, "type": "XD_Fir2_small", "distance_to_hq": 1848},
    {"x": 43076, "y": 23120, "type": "XD_Fir2_small", "distance_to_hq": 1976},
    {"x": 43109, "y": 23270, "type": "XD_PineNorth2", "distance_to_hq": 2017},
    {"x": 41169, "y": 21057, "type": "XD_Fir1", "distance_to_hq": 2044},
    {"x": 43170, "y": 23270, "type": "XD_PineNorth2", "distance_to_hq": 2077},
    {"x": 43180, "y": 23080, "type": "XD_Fir1_small", "distance_to_hq": 2080},
    {"x": 43180, "y": 23180, "type": "XD_Fir2_small", "distance_to_hq": 2081},
    {"x": 40980, "y": 20980, "type": "XD_Fir2_small", "distance_to_hq": 2123},
    {"x": 43223, "y": 23476, "type": "XD_PineNorth2", "distance_to_hq": 2156},
    {"x": 41853, "y": 21052, "type": "XD_Fir1_small", "distance_to_hq": 2182},
    {"x": 42980, "y": 21953, "type": "XD_Fir1_small", "distance_to_hq": 2202},
    {"x": 43326, "y": 23632, "type": "XD_PineNorth1", "distance_to_hq": 2280},
    {"x": 41420, "y": 20880, "type": "XD_Fir2_small", "distance_to_hq": 2283},
    {"x": 43340, "y": 23536, "type": "XD_PineNorth2", "distance_to_hq": 2286},
    {"x": 43380, "y": 23680, "type": "XD_Fir1_small", "distance_to_hq": 2347},
    {"x": 43396, "y": 23655, "type": "XD_PineNorth3", "distance_to_hq": 2355},
    {"x": 43443, "y": 23568, "type": "XD_Fir1_small", "distance_to_hq": 2381},
    {"x": 43455, "y": 22833, "type": "XD_Fir1_small", "distance_to_hq": 2382},
    {"x": 43320, "y": 22880, "type": "XD_Fir2_small", "distance_to_hq": 2384},
    {"x": 40620, "y": 20880, "type": "XD_Fir2_small", "distance_to_hq": 2290},
    {"x": 43380, "y": 23080, "type": "XD_Fir2_small", "distance_to_hq": 2280},
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
