# -*- coding: utf-8 -*-
"""
Siedler 5 - VollstÃƒÆ’Ã‚Â¤ndige Trainingsumgebung fÃƒÆ’Ã‚Â¼r ScharfschÃƒÆ’Ã‚Â¼tzen-Optimierung
KOMPLETTE Spielsimulation mit ALLEN Aktionen aus dem echten Spiel

Basiert auf: Die Siedler - Erbe der KÃƒÆ’Ã‚Â¶nige
Karte: EMS Wintersturm (4 Spieler, 2v2)

NEU: Integriert WorkTime/Pausen-System und 2-Tier Produktion
"""

import copy
import re
import json
import os
import unicodedata
from enum import Enum
import gymnasium as gym
import numpy as np
from gymnasium import spaces
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    from map_extract_config import EXTRACTED_DIR as MAP_EXTRACT_DIR
except Exception:
    MAP_EXTRACT_DIR = None


def _env_truthy(value: Optional[str]) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _resolve_sim_mode_from_env() -> str:
    mode = str(os.environ.get("SIEDLER_SIM_MODE", "")).strip().lower()
    if mode in {"fast_train", "full_sim"}:
        return mode
    return "fast_train" if _env_truthy(os.environ.get("SIEDLER_FAST_TRAIN", "0")) else "full_sim"


# ============================================================================
# MULTI-STEP ACTION SYSTEM (NEU - aus GEPLANTE_AENDERUNGEN.md)
# ============================================================================

class ActionPhase(Enum):
    """Phase im Multi-Step Action Flow."""
    MAIN = "main"                       # Haupt-Aktion wÃƒÆ’Ã‚Â¤hlen (11 Optionen)
    BUILDING = "building"               # GebÃƒÆ’Ã‚Â¤ude-Typ wÃƒÆ’Ã‚Â¤hlen
    POSITION_GROUP = "position_group"   # Positions-Gruppe wÃƒÆ’Ã‚Â¤hlen (z.B. 44)
    POSITION_INDEX = "position_index"   # Index innerhalb der Gruppe (z.B. 50)
    TECH_BUILDING = "tech_building"     # Forschungs-GebÃƒÆ’Ã‚Â¤ude wÃƒÆ’Ã‚Â¤hlen (Hochschule/Schmiede/etc.)
    TECH = "tech"                       # Technologie wÃƒÆ’Ã‚Â¤hlen (innerhalb des GebÃƒÆ’Ã‚Â¤udes)
    SOLDIER = "soldier"                 # Soldaten-Typ wÃƒÆ’Ã‚Â¤hlen
    QUANTITY = "quantity"               # Menge wÃƒÆ’Ã‚Â¤hlen (1,2,3,5,10,20)
    SOURCE_CATEGORY = "source_category" # Quell-Kategorie (Frei/Holz/Eisen/Stein/Lehm/Schwefel/Baustelle)
    SOURCE_SPECIFIC = "source_specific" # Spezifischer Quell-Ort innerhalb der Kategorie
    TARGET_CATEGORY = "target_category" # Ziel-Kategorie (Holz/.../Baustelle/Neubau; Frei als Ziel deaktiviert)
    TARGET_SPECIFIC = "target_specific" # Spezifischer Ziel-Ort innerhalb der Kategorie
    CATEGORY = "category"               # Segen-Kategorie
    TAX_LEVEL = "tax_level"             # Steuerstufe
    ON_OFF = "on_off"                   # Alarm an/aus


# =============================================================================
# HIERARCHISCHE SERF-KATEGORIEN
# =============================================================================
SOURCE_CATEGORIES = {
    0: "Frei",
    1: "Holz",
    2: "Eisen",
    3: "Stein",
    4: "Lehm",
    5: "Schwefel",
    6: "Baustelle",
}

TARGET_CATEGORIES = {
    0: "Frei (deaktiviert)",
    1: "Holz",
    2: "Eisen",
    3: "Stein",
    4: "Lehm",
    5: "Schwefel",
    6: "Baustelle",
    7: "Neubau",  # Erstellt Baustelle + weist Serfs direkt zu
}

MAX_SPECIFIC_OPTIONS = 28  # Max(6 Holz-Zonen, 5 Eisen, 10 Baustellen, 28 GebÃƒÆ’Ã‚Â¤ude)
MAX_POSITION_SLOTS = 2200
POSITION_GROUP_SIZE = 50
POSITION_GROUP_COUNT = (MAX_POSITION_SLOTS + POSITION_GROUP_SIZE - 1) // POSITION_GROUP_SIZE
QUANTITY_VALUES = [1, 2, 3, 5, 10, 20]

# Forschungs-GebÃƒÆ’Ã‚Â¤ude: In welchem GebÃƒÆ’Ã‚Â¤ude wird welche Technologie erforscht?
# Jede Technologie hat ein "requires_building" - wir gruppieren nach Basis-GebÃƒÆ’Ã‚Â¤ude
RESEARCH_BUILDINGS = [
    "Hochschule",       # 0: Haupt-Research (Konstruktion/Alchimie/Bildung/MilitÃƒÆ’Ã‚Â¤r/Mathe + Fernglas/Luntenschloss/Gezogener Lauf)
    "Schmiede",         # 1: 8 Techs (RÃƒÆ’Ã‚Â¼stungen, Nahkampf, BogenschÃƒÆ’Ã‚Â¼tzen-RÃƒÆ’Ã‚Â¼stung)
    "AlchimistenhÃƒÆ’Ã‚Â¼tte", # 2: 4 Techs (Artillerie, Wetter)
    "Bank",             # 3: 4 Techs (Finanzen)
    "SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle",        # 4: 4 Techs (Fernkampf, Speer)
    "Dorfzentrum",      # 5: 3 Techs (Stadtwache, Webstuhl, Schuhe)
    "Hauptquartier",    # 6: HQ-Research nur wenn Techs dort existieren (z.B. Tracking)
    "Kaserne",          # 7: 1 Tech (Kasernentraining)
    "SchieÃƒÆ’Ã…Â¸platz",      # 8: 1 Tech (SchieÃƒÆ’Ã…Â¸training)
    "Stall",            # 9: 1 Tech (Hufbeschlag)
    "KanongieÃƒÆ’Ã…Â¸erei",    # 10: 1 Tech (Verbessertes Fahrgestell)
    "SteinmetzhÃƒÆ’Ã‚Â¼tte",   # 11: 1 Tech (Maurerarbeit)
    "LehmhÃƒÆ’Ã‚Â¼tte",        # 12: 1 Tech (Leichte Ziegel)
    # --- Addon/Original Tech-GebÃƒÆ’Ã‚Â¤ude (aus base/extra1/extra2 Technologies.xml) ---
    "BÃƒÆ’Ã‚Â¼chsenmacherei",  # PB_GunsmithWorkshop (ScharfschÃƒÆ’Ã‚Â¼tzen-Techs)
    "Taverne",          # PB_Tavern (SpÃƒÆ’Ã‚Â¤her/Dieb-Techs)
    "Architektenstube", # PB_MasterBuilderWorkshop (BrÃƒÆ’Ã‚Â¼cke)
    "Kloster",          # PB_Monastery (Segnungs-Techs)
    "Wetterkraftwerk",  # PB_PowerPlant (Wetterzauber-Techs)
]
MAX_TECHS_PER_BUILDING = 40  # Hochschule hat die meisten (erweitert durch Utility-Techs)


# Definiert welche Phasen fÃƒÆ’Ã‚Â¼r jede Haupt-Aktion durchlaufen werden
# "build" ist in "assign_serf" integriert (TARGET_CATEGORY=Neubau)
ACTION_FLOWS = {
    "wait": [ActionPhase.MAIN],
    "upgrade": [ActionPhase.MAIN, ActionPhase.BUILDING, ActionPhase.POSITION_GROUP, ActionPhase.POSITION_INDEX],
    "research": [ActionPhase.MAIN, ActionPhase.TECH_BUILDING, ActionPhase.TECH],
    "recruit": [ActionPhase.MAIN, ActionPhase.SOLDIER, ActionPhase.QUANTITY],
    "buy_serf": [ActionPhase.MAIN, ActionPhase.QUANTITY],
    "dismiss_serf": [ActionPhase.MAIN, ActionPhase.SOURCE_CATEGORY, ActionPhase.SOURCE_SPECIFIC, ActionPhase.QUANTITY],
    "assign_serf": [
        ActionPhase.MAIN,
        ActionPhase.SOURCE_CATEGORY,
        ActionPhase.SOURCE_SPECIFIC,
        ActionPhase.QUANTITY,
        ActionPhase.TARGET_CATEGORY,
        ActionPhase.TARGET_SPECIFIC,
        ActionPhase.POSITION_GROUP,
        ActionPhase.POSITION_INDEX,
    ],
    "demolish": [ActionPhase.MAIN, ActionPhase.BUILDING, ActionPhase.POSITION_GROUP, ActionPhase.POSITION_INDEX],
    "bless": [ActionPhase.MAIN, ActionPhase.CATEGORY],
    "tax": [ActionPhase.MAIN, ActionPhase.TAX_LEVEL],
    "alarm": [ActionPhase.MAIN, ActionPhase.ON_OFF],
}

MAIN_ACTIONS = list(ACTION_FLOWS.keys())


# ============================================================================
# SERF AREA SYSTEM (NEU - 26 feste Bereiche + dynamische Baustellen)
# ============================================================================

class SerfArea(Enum):
    """Bereiche fÃƒÆ’Ã‚Â¼r Leibeigene-Zuweisung."""
    FREE = 0            # Frei (nicht zugewiesen)
    # Holz-Zonen (6)
    WOOD_HQ = 1         # Holz nahe HQ
    WOOD_SULFUR = 2     # Holz nahe Schwefel
    WOOD_CLAY = 3       # Holz nahe Lehm
    WOOD_STONE = 4      # Holz nahe Stein
    WOOD_VILLAGE = 5    # Holz nahe Dorf
    WOOD_IRON = 6       # Holz nahe Eisen
    # Eisen-Stollen (3)
    SHAFT_IRON_1 = 7
    SHAFT_IRON_2 = 8
    SHAFT_IRON_3 = 9
    # Stein-Stollen (3)
    SHAFT_STONE_1 = 10
    SHAFT_STONE_2 = 11
    SHAFT_STONE_3 = 12
    # Lehm-Stollen (3)
    SHAFT_CLAY_1 = 13
    SHAFT_CLAY_2 = 14
    SHAFT_CLAY_3 = 15
    # Schwefel-Stollen (3)
    SHAFT_SULFUR_1 = 16
    SHAFT_SULFUR_2 = 17
    SHAFT_SULFUR_3 = 18
    # Vorkommen (7)
    DEPOSIT_IRON_1 = 19
    DEPOSIT_IRON_2 = 20
    DEPOSIT_STONE_1 = 21
    DEPOSIT_STONE_2 = 22
    DEPOSIT_CLAY_1 = 23
    DEPOSIT_SULFUR_1 = 24
    DEPOSIT_SULFUR_2 = 25


# Mapping: Kategorie-Index ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Liste von SerfArea-Enums
# Wird fÃƒÆ’Ã‚Â¼r _resolve_area() und Mask-Methoden verwendet
CATEGORY_AREA_MAP = {
    0: [SerfArea.FREE],
    1: [SerfArea.WOOD_HQ, SerfArea.WOOD_SULFUR, SerfArea.WOOD_CLAY, SerfArea.WOOD_STONE, SerfArea.WOOD_VILLAGE, SerfArea.WOOD_IRON],
    2: [SerfArea.SHAFT_IRON_1, SerfArea.SHAFT_IRON_2, SerfArea.SHAFT_IRON_3, SerfArea.DEPOSIT_IRON_1, SerfArea.DEPOSIT_IRON_2],
    3: [SerfArea.SHAFT_STONE_1, SerfArea.SHAFT_STONE_2, SerfArea.SHAFT_STONE_3, SerfArea.DEPOSIT_STONE_1, SerfArea.DEPOSIT_STONE_2],
    4: [SerfArea.SHAFT_CLAY_1, SerfArea.SHAFT_CLAY_2, SerfArea.SHAFT_CLAY_3, SerfArea.DEPOSIT_CLAY_1],
    5: [SerfArea.SHAFT_SULFUR_1, SerfArea.SHAFT_SULFUR_2, SerfArea.SHAFT_SULFUR_3, SerfArea.DEPOSIT_SULFUR_1, SerfArea.DEPOSIT_SULFUR_2],
    # 6 = Baustelle (dynamisch, wird separat behandelt)
    # 7 = Neubau (nur TARGET, wird separat behandelt)
}

SHAFT_AREA_TO_SLOT = {
    SerfArea.SHAFT_IRON_1: ("Eisen", 0),
    SerfArea.SHAFT_IRON_2: ("Eisen", 1),
    SerfArea.SHAFT_IRON_3: ("Eisen", 2),
    SerfArea.SHAFT_STONE_1: ("Stein", 0),
    SerfArea.SHAFT_STONE_2: ("Stein", 1),
    SerfArea.SHAFT_STONE_3: ("Stein", 2),
    SerfArea.SHAFT_CLAY_1: ("Lehm", 0),
    SerfArea.SHAFT_CLAY_2: ("Lehm", 1),
    SerfArea.SHAFT_CLAY_3: ("Lehm", 2),
    SerfArea.SHAFT_SULFUR_1: ("Schwefel", 0),
    SerfArea.SHAFT_SULFUR_2: ("Schwefel", 1),
    SerfArea.SHAFT_SULFUR_3: ("Schwefel", 2),
}

DEPOSIT_AREA_TO_SLOT = {
    SerfArea.DEPOSIT_IRON_1: ("Eisen", 0),
    SerfArea.DEPOSIT_IRON_2: ("Eisen", 1),
    SerfArea.DEPOSIT_STONE_1: ("Stein", 0),
    SerfArea.DEPOSIT_STONE_2: ("Stein", 1),
    SerfArea.DEPOSIT_CLAY_1: ("Lehm", 0),
    SerfArea.DEPOSIT_SULFUR_1: ("Schwefel", 0),
    SerfArea.DEPOSIT_SULFUR_2: ("Schwefel", 1),
}


# ============================================================================
# TECHNOLOGY EFFECTS SYSTEM (NEU - Effekte werden jetzt angewendet!)
# ============================================================================

# Hinweis: Die exakten Effekt-Werte sind im C++ Code des Spiels hardcoded,
# nicht in den XML-Dateien. Diese Werte basieren auf Gameplay-Analyse.
# Technologie-Effekte basierend auf Original-XMLs (SpeedModifier, ArmorModifier, etc.)
# Werte sind ADDITIVE Boni aus den XML-Tags (Operation="+")
TECHNOLOGY_EFFECTS = {
    # === Kaserne: SpeedModifier (Schwert+Speer Geschwindigkeit) ===
    "Kasernentraining": {"speed_modifier": 30},     # T_BetterTrainingBarracks: +30

    # === SchieÃƒÆ’Ã…Â¸platz: SpeedModifier (Bogen-Geschwindigkeit) ===
    "SchieÃƒÆ’Ã…Â¸training": {"speed_modifier": 40},        # T_BetterTrainingArchery: +40

    # === Stall: SpeedModifier (Kavallerie-Geschwindigkeit) ===
    "Hufbeschlag": {"speed_modifier": 50},           # T_Shoeing: +50

    # === KanongieÃƒÆ’Ã…Â¸erei: SpeedModifier (Kanonen-Geschwindigkeit) ===
    "Verbessertes Fahrgestell": {"speed_modifier": 30},  # T_BetterChassis: +30

    # === Dorfzentrum: ===
    "Stadtwache": {"exploration_modifier": 5},       # T_TownGuard: ExplorationModifier +5
    "Webstuhl": {"armor_modifier": 2},               # T_Loom: ArmorModifier +2 (Worker/Serf)
    "Schuhe": {"speed_modifier": 20},                # T_Shoes: SpeedModifier +20 (Worker/Serf)

    # === LehmhÃƒÆ’Ã‚Â¼tte: Leichte Ziegel (kein XML-Modifier, Bau-Speed Effekt) ===
    "Leichte Ziegel": {"build_speed_bonus": 15},     # T_LightBricks (aus Spielmechanik)

    # === SteinmetzhÃƒÆ’Ã‚Â¼tte: Mauerbau ===
    "Maurerarbeit": {"building_armor_bonus": 3},     # T_Masonry: ArmorModifier fÃƒÆ’Ã‚Â¼r GebÃƒÆ’Ã‚Â¤ude

    # === Schmiede: RÃƒÆ’Ã‚Â¼stungen (Nahkampf: Schwert+Schwere Kavallerie) ===
    "LederrÃƒÆ’Ã‚Â¼stung": {"melee_armor": 2},              # T_LeatherMailArmor
    "KettenrÃƒÆ’Ã‚Â¼stung": {"melee_armor": 4},             # T_ChainMailArmor
    "PlattenrÃƒÆ’Ã‚Â¼stung": {"melee_armor": 6},            # T_PlateMailArmor
    # Schmiede: RÃƒÆ’Ã‚Â¼stungen (Fernkampf: Bogen+Leichte Kav+Speer)
    "SchÃƒÆ’Ã‚Â¼tzenrÃƒÆ’Ã‚Â¼stung": {"ranged_armor": 1},          # T_SoftArcherArmor
    "Gepolsterte SchÃƒÆ’Ã‚Â¼tzenrÃƒÆ’Ã‚Â¼stung": {"ranged_armor": 2},  # T_PaddedArcherArmor
    "Lederne SchÃƒÆ’Ã‚Â¼tzenrÃƒÆ’Ã‚Â¼stung": {"ranged_armor": 3},  # T_LeatherArcherArmor
    # Schmiede: Nahkampf-Schaden (Schwert+Schwere Kavallerie)
    "Schwertschmied": {"melee_damage": 2},           # T_MasterOfSmithery
    "Waffenmeister": {"melee_damage": 4},            # T_IronCasting

    # === SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle: Bogen-Schaden ===
    "Pfeilherstellung": {"bow_damage": 2},           # T_Fletching
    "Panzerbrechende Pfeile": {"bow_damage": 4},     # T_BodkinArrow
    # SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle: Speer-Schaden
    "Holzalterung": {"spear_damage": 2},             # T_WoodAging
    "Drechselei": {"spear_damage": 2},               # T_Turnery

    # === AlchimistenhÃƒÆ’Ã‚Â¼tte: Kanonen-Schaden ===
    "Verbessertes SchieÃƒÆ’Ã…Â¸pulver": {"cannon_damage": 3},  # T_EnhancedGunPowder
    "Sprenggeschosse": {"cannon_damage": 5},         # T_BlisteringCannonballs

    # === Bank: Keine XML-Modifier (Effekte in LUA-Skripten) ===
    "Schuldschein": {"payday_bonus": True},          # T_Debenture
    "BuchfÃƒÆ’Ã‚Â¼hrung": {"payday_bonus_2": True},         # T_BookKeeping
    "Waage": {"trade_bonus": True},                  # T_Scale
    "MÃƒÆ’Ã‚Â¼nzprÃƒÆ’Ã‚Â¤gung": {"trade_bonus_2": True},          # T_Coinage

    # === ScharfschÃƒÆ’Ã‚Â¼tzen-Pfad (extra1 AddOn) ===
    "Mathematik": {"university_level2_unlock": True},   # GT_Mathematics
    "Fernglas": {"rifle_unlock": True},                 # GT_Binocular
    "Luntenschloss": {"gunsmith_unlock": True},         # GT_Matchlock
    "Gezogener Lauf": {"rifle_upgrade_unlock": True},   # GT_PulledBarrel

    # === ScharfschÃƒÆ’Ã‚Â¼tzen-RÃƒÆ’Ã‚Â¼stung (extra1, in BÃƒÆ’Ã‚Â¼chsenmacherei) ===
    "VliesrÃƒÆ’Ã‚Â¼stung": {"rifle_armor": 1},              # T_FleeceArmor
    "VliesgefÃƒÆ’Ã‚Â¼tterte LederrÃƒÆ’Ã‚Â¼stung": {"rifle_armor": 2},  # T_FleeceLinedLeatherArmor
    # ScharfschÃƒÆ’Ã‚Â¼tzen-Schaden
    "Bleikugeln": {"rifle_damage": 2},               # T_LeadShot
    "Zielfernrohr": {"rifle_damage": 4},             # T_Sights

}

# Importiere Karten-Konfiguration
from map_config_wintersturm import (
    START_RESOURCES, MINES_PER_PLAYER, BUILDING_ZONES_PLAYER_1,
    PLAYER_1_MINE_POSITIONS, PLAYER_1_MINE_SHAFTS, PLAYER_1_SMALL_DEPOSITS,
    PLAYER_1_TREES_SUMMARY, PLAYER_1_TREES_NEAREST,
    PLAYER_1_VILLAGE_CENTER_SLOTS,
    PLAYER_HQ_POSITIONS, MAP_SIZE,
    GAME_RULES, SCHARFSCHUETZEN_PATH,
    get_building_positions_for_player
)

# Importiere Holz-Zonen fÃƒÆ’Ã‚Â¼r strategische Bauplatz-Schaffung
from wood_zones_config import WOOD_ZONES

# Importiere neue Simulationssysteme
from worker_simulation import (
    Position, WorkforceManager, Worker, Farm, Residence, Camp,
    WorkerState, WORKER_PARAMS, WORKER_SPEEDS,
)

try:
    from worker_simulation import FORCE_TO_WORK_PENALTY as WORKER_FORCE_TO_WORK_PENALTY
except ImportError:
    WORKER_FORCE_TO_WORK_PENALTY = 0.2
from production_system import (
    ProductionSystem, Mine, Refiner, Serf, SerfState, ResourceType,
    SERF_EXTRACTION,
)

try:
    from production_system import get_refiner_resource_ops_per_cycle
except ImportError:
    def get_refiner_resource_ops_per_cycle(worker_type: str, fallback: int = 2) -> int:
        return max(1, int(fallback))

# NEU: Pfadfindung fÃƒÆ’Ã‚Â¼r exakte Laufwege
import pathfinding
from pathfinding import MapManager, PathResult

# =============================================================================
# RESSOURCEN-DEFINITIONEN
# =============================================================================

RESOURCE_HOLZ = "Holz"
RESOURCE_STEIN = "Stein"
RESOURCE_LEHM = "Lehm"
RESOURCE_EISEN = "Eisen"
RESOURCE_SCHWEFEL = "Schwefel"
RESOURCE_TALER = "Taler"

# Rohstoffe (Raw)
RESOURCE_HOLZ_ROH = "HolzRoh"
RESOURCE_STEIN_ROH = "SteinRoh"
RESOURCE_LEHM_ROH = "LehmRoh"
RESOURCE_EISEN_ROH = "EisenRoh"
RESOURCE_SCHWEFEL_ROH = "SchwefelRoh"
RESOURCE_GOLD_ROH = "GoldRoh"

RESOURCE_REFINED = [RESOURCE_HOLZ, RESOURCE_STEIN, RESOURCE_LEHM, RESOURCE_EISEN, RESOURCE_SCHWEFEL]
RESOURCE_RAW = [
    RESOURCE_HOLZ_ROH,
    RESOURCE_STEIN_ROH,
    RESOURCE_LEHM_ROH,
    RESOURCE_EISEN_ROH,
    RESOURCE_SCHWEFEL_ROH,
    RESOURCE_GOLD_ROH,
]
RESOURCE_NAMES = RESOURCE_REFINED + RESOURCE_RAW + [RESOURCE_TALER]
RESOURCE_MAP = RESOURCE_RAW + RESOURCE_REFINED + [RESOURCE_TALER]
REFINED_TO_RAW = {
    RESOURCE_HOLZ: RESOURCE_HOLZ_ROH,
    RESOURCE_STEIN: RESOURCE_STEIN_ROH,
    RESOURCE_LEHM: RESOURCE_LEHM_ROH,
    RESOURCE_EISEN: RESOURCE_EISEN_ROH,
    RESOURCE_SCHWEFEL: RESOURCE_SCHWEFEL_ROH,
    RESOURCE_TALER: RESOURCE_GOLD_ROH,
}
RAW_TO_REFINED = {raw: refined for refined, raw in REFINED_TO_RAW.items()}

# Statische Mappings fuer _get_production_rate() – einmal definiert, nie neu erstellt
# (ResourceType bereits importiert, RESOURCE_* Strings oben definiert)
def _build_resource_type_map():
    try:
        return {
            RESOURCE_HOLZ: ResourceType.WOOD,
            RESOURCE_STEIN: ResourceType.STONE,
            RESOURCE_LEHM: ResourceType.CLAY,
            RESOURCE_EISEN: ResourceType.IRON,
            RESOURCE_SCHWEFEL: ResourceType.SULFUR,
            RESOURCE_TALER: ResourceType.GOLD,
            RESOURCE_HOLZ_ROH: ResourceType.WOOD_RAW,
            RESOURCE_STEIN_ROH: ResourceType.STONE_RAW,
            RESOURCE_LEHM_ROH: ResourceType.CLAY_RAW,
            RESOURCE_EISEN_ROH: ResourceType.IRON_RAW,
            RESOURCE_SCHWEFEL_ROH: ResourceType.SULFUR_RAW,
            RESOURCE_GOLD_ROH: ResourceType.GOLD_RAW,
        }
    except AttributeError:
        return {}
_RESOURCE_TYPE_MAP = _build_resource_type_map()
_RESOURCE_KEY_MAP = {
    RESOURCE_HOLZ: "wood",
    RESOURCE_STEIN: "stone",
    RESOURCE_LEHM: "clay",
    RESOURCE_EISEN: "iron",
    RESOURCE_SCHWEFEL: "sulfur",
    RESOURCE_TALER: "gold",
}

# Worker-Typ Normalisierung (XML/PU_Namen -> interne Namen)
WORKER_TYPE_ALIASES = {
    "sawmillworker": "sawmill_worker",
    "tavernbarkeeper": "barkeeper",
    "masterbuilder": "master_builder",
}


def normalize_worker_type(name: str) -> str:
    if not name:
        return ""
    w = name.lower()
    if w.startswith("pu_"):
        w = w[3:]
    return WORKER_TYPE_ALIASES.get(w, w)


def _pos_key(pos) -> Tuple[int, int]:
    if isinstance(pos, dict):
        x = pos.get("x", 0)
        y = pos.get("y", 0)
    elif isinstance(pos, tuple):
        x, y = pos
    else:
        x = getattr(pos, "x", 0)
        y = getattr(pos, "y", 0)
    return (int(round(x)), int(round(y)))

# Sammelraten pro Arbeiter pro Zeiteinheit
gather_rates = {
    RESOURCE_HOLZ_ROH: 1.038,
    RESOURCE_STEIN_ROH: 0.528,
    RESOURCE_LEHM_ROH: 0.528,
    RESOURCE_EISEN_ROH: 0.642,
    RESOURCE_SCHWEFEL_ROH: 0.642
}

# =============================================================================
# LEIBEIGENE-KONSTANTEN (aus PU_Serf.xml)
# =============================================================================
SERF_SEARCH_RADIUS = 4500  # ResourceSearchRadius aus PU_Serf.xml
WOOD_PER_TREE = 75  # ResourceAmount aus XD_Tree*.xml (Standard-BÃƒÆ’Ã‚Â¤ume)
WOOD_PER_EXTRACTION = 2  # Amount aus PU_Serf.xml
EXTRACTION_TIME_WOOD = 5.52  # Sekunden (4s delay + 1.52s animation)
# StabilitÃƒÆ’Ã‚Â¤t/Performance: begrenzt Extreme bei Massen-Zuweisungen auf einen Baum.
MAX_SERFS_PER_TREE = 3

# =============================================================================
# VOLLSTÃƒÆ’Ã¢â‚¬Å¾NDIGE GEBÃƒÆ’Ã¢â‚¬Å¾UDE-DATENBANK (80+ GebÃƒÆ’Ã‚Â¤ude)
# =============================================================================

RESOURCE_PRODUCTION_BASES = {
    "Steinmine", "Lehmmine", "Eisenmine", "Schwefelmine",
    "SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle", "LehmhÃƒÆ’Ã‚Â¼tte", "Schmiede", "AlchimistenhÃƒÆ’Ã‚Â¼tte", "SteinmetzhÃƒÆ’Ã‚Â¼tte",
    "Bank", "BÃƒÆ’Ã‚Â¼chsenmacherei",
}

# Worker-Typen pro GebÃƒÆ’Ã‚Â¤ude-Basisname (aus XMLs)
BUILDING_WORKER_TYPES = {
    # Minen
    "Steinmine": "miner",
    "Lehmmine": "miner",
    "Eisenmine": "miner",
    "Schwefelmine": "miner",
    # Refiner/Produktion
    "SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle": "sawmill_worker",
    "LehmhÃƒÆ’Ã‚Â¼tte": "brickmaker",
    "Schmiede": "smith",
    "AlchimistenhÃƒÆ’Ã‚Â¼tte": "alchemist",
    "SteinmetzhÃƒÆ’Ã‚Â¼tte": "stonecutter",
    "Bank": "treasurer",
    "BÃƒÆ’Ã‚Â¼chsenmacherei": "gunsmith",
    # Sonstige Worker-GebÃƒÆ’Ã‚Â¤ude
    "Hochschule": "scholar",
    "Bauernhof": "farmer",
    "Kloster": "priest",
    "Markt": "trader",
    "Wetterkraftwerk": "engineer",
    "Architektenstube": "master_builder",
    "Taverne": "barkeeper",
    "KanongieÃƒÆ’Ã…Â¸erei": "smelter",
}

_raw_buildings_db = {
    # === HAUPTQUARTIER (3 Level) - aus PB_Headquarters1/2/3.xml ===
    "Hauptquartier_1": {
        "build_time": 110, "cost": {RESOURCE_LEHM: 1000, RESOURCE_STEIN: 1000},  # Clay 1000, Stone 1000
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 0, "worker_capacity": 100,
        "upgrade_to": "Hauptquartier_2",
        "upgrade_cost": {RESOURCE_TALER: 300, RESOURCE_STEIN: 300, RESOURCE_LEHM: 250},  # Gold 300, Stone 300, Clay 250
        "upgrade_time": 90
    },
    "Hauptquartier_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 0, "worker_capacity": 150,
        "upgrade_to": "Hauptquartier_3",
        "upgrade_cost": {RESOURCE_TALER: 500, RESOURCE_STEIN: 500, RESOURCE_LEHM: 400},  # Gold 500, Stone 500, Clay 400
        "upgrade_time": 120
    },
    "Hauptquartier_3": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 0, "worker_capacity": 200,
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === DORFZENTRUM (3 Level) - aus PB_VillageCenter1/2/3.xml ===
    "Dorfzentrum_1": {
        "build_time": 110, "cost": {RESOURCE_HOLZ: 300, RESOURCE_STEIN: 200},  # Wood 300, Stone 200
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 0, "worker_capacity": 75,  # AttractableSettlers=75
        "upgrade_to": "Dorfzentrum_2",
        "upgrade_cost": {RESOURCE_TALER: 150, RESOURCE_STEIN: 300, RESOURCE_LEHM: 100}, "upgrade_time": 40
    },
    "Dorfzentrum_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 0, "worker_capacity": 100,  # AttractableSettlers=100
        "upgrade_to": "Dorfzentrum_3",
        "upgrade_cost": {RESOURCE_TALER: 200, RESOURCE_STEIN: 400, RESOURCE_LEHM: 150}, "upgrade_time": 40
    },
    "Dorfzentrum_3": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 0, "worker_capacity": 125,  # AttractableSettlers=125 (WAR 150, KORRIGIERT!)
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === WOHNHAUS (3 Level) - aus PB_Residence1/2/3.xml ===
    "Wohnhaus_1": {
        "build_time": 80, "cost": {RESOURCE_HOLZ: 150, RESOURCE_LEHM: 100},  # Wood 150, Clay 100
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 0, "worker_capacity": 6,  # WorkerResidenceSlots=6
        "upgrade_to": "Wohnhaus_2",
        "upgrade_cost": {RESOURCE_HOLZ: 50, RESOURCE_STEIN: 150}, "upgrade_time": 40  # Wood 50, Stone 150
    },
    "Wohnhaus_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 0, "worker_capacity": 9,  # WorkerResidenceSlots=9
        "upgrade_to": "Wohnhaus_3",
        "upgrade_cost": {RESOURCE_HOLZ: 150, RESOURCE_STEIN: 200}, "upgrade_time": 50  # Wood 150, Stone 200
    },
    "Wohnhaus_3": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 0, "worker_capacity": 12,  # WorkerResidenceSlots=12
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === BAUERNHOF (3 Level) - aus PB_Farm1/2/3.xml ===
    "Bauernhof_1": {
        "build_time": 80, "cost": {RESOURCE_HOLZ: 200, RESOURCE_LEHM: 150},  # Wood 200, Clay 150
        "taler_income": 0, "resource_output": {}, "tech_required": None, "max_workers": 1,  # MaxWorkers=1 (KORRIGIERT!)
        "upgrade_to": "Bauernhof_2",
        "upgrade_cost": {RESOURCE_HOLZ: 50, RESOURCE_STEIN: 100}, "upgrade_time": 40  # Wood 50, Stone 100
    },
    "Bauernhof_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 0, "resource_output": {}, "tech_required": None, "max_workers": 2,  # MaxWorkers=2 (KORRIGIERT!)
        "upgrade_to": "Bauernhof_3",
        "upgrade_cost": {RESOURCE_HOLZ: 150, RESOURCE_STEIN: 300}, "upgrade_time": 50  # Wood 150, Stone 300
    },
    "Bauernhof_3": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 0, "resource_output": {}, "tech_required": None, "max_workers": 3,  # MaxWorkers=3 (KORRIGIERT!)
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === HOCHSCHULE (2 Level) - aus PB_University1/2.xml ===
    "Hochschule_1": {
        "build_time": 90, "cost": {RESOURCE_LEHM: 300, RESOURCE_HOLZ: 200},  # Clay 300, Wood 200
        "taler_income": 35, "resource_output": {}, "tech_required": None,
        "max_workers": 6, "research_speed": 1.0,  # MaxWorkers=6, InitialWorkAmount=1.0
        "upgrade_to": "Hochschule_2",
        "upgrade_cost": {RESOURCE_TALER: 150, RESOURCE_STEIN: 100, RESOURCE_LEHM: 100}, "upgrade_time": 50
    },
    "Hochschule_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 50, "resource_output": {}, "tech_required": None,
        "max_workers": 8, "research_speed": 1.5,  # MaxWorkers=8
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === MINEN (3 Level jede) - aus PB_*Mine1/2/3.xml ===
    # Minen haben cost:{} da auf Mine-Slots gebaut, AmountToMine = 4/5/6 (KORRIGIERT von 2/3/4!)
    "Steinmine_1": {
        "build_time": 80, "cost": {},
        "taler_income": 20, "resource_output": {RESOURCE_STEIN: 4}, "tech_required": None,  # AmountToMine=4
        "max_workers": 5, "mine_type": "Steinmine",
        "upgrade_to": "Steinmine_2",
        "upgrade_cost": {RESOURCE_LEHM: 150, RESOURCE_HOLZ: 200}, "upgrade_time": 40  # Clay 150, Wood 200
    },
    "Steinmine_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 30, "resource_output": {RESOURCE_STEIN: 5}, "tech_required": None,  # AmountToMine=5
        "max_workers": 6, "mine_type": "Steinmine",
        "upgrade_to": "Steinmine_3",
        "upgrade_cost": {RESOURCE_LEHM: 200, RESOURCE_EISEN: 200}, "upgrade_time": 50  # Clay 200, Iron 200
    },
    "Steinmine_3": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 40, "resource_output": {RESOURCE_STEIN: 6}, "tech_required": None,  # AmountToMine=6
        "max_workers": 7, "mine_type": "Steinmine",
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "Lehmmine_1": {
        "build_time": 80, "cost": {},
        "taler_income": 10, "resource_output": {RESOURCE_LEHM: 4}, "tech_required": None,  # AmountToMine=4
        "max_workers": 5, "mine_type": "Lehmmine",
        "upgrade_to": "Lehmmine_2",
        "upgrade_cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 150}, "upgrade_time": 40  # Wood 200, Stone 150
    },
    "Lehmmine_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 15, "resource_output": {RESOURCE_LEHM: 5}, "tech_required": None,  # AmountToMine=5
        "max_workers": 6, "mine_type": "Lehmmine",
        "upgrade_to": "Lehmmine_3",
        "upgrade_cost": {RESOURCE_HOLZ: 250, RESOURCE_STEIN: 300}, "upgrade_time": 50  # Wood 250, Stone 300
    },
    "Lehmmine_3": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 20, "resource_output": {RESOURCE_LEHM: 6}, "tech_required": None,  # AmountToMine=6
        "max_workers": 7, "mine_type": "Lehmmine",
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "Eisenmine_1": {
        "build_time": 80, "cost": {},
        "taler_income": 25, "resource_output": {RESOURCE_EISEN: 4}, "tech_required": None,  # AmountToMine=4
        "max_workers": 5, "mine_type": "Eisenmine",
        "upgrade_to": "Eisenmine_2",
        "upgrade_cost": {RESOURCE_LEHM: 150, RESOURCE_HOLZ: 200}, "upgrade_time": 40  # Clay 150, Wood 200
    },
    "Eisenmine_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 35, "resource_output": {RESOURCE_EISEN: 5}, "tech_required": None,  # AmountToMine=5
        "max_workers": 6, "mine_type": "Eisenmine",
        "upgrade_to": "Eisenmine_3",
        "upgrade_cost": {RESOURCE_LEHM: 300, RESOURCE_HOLZ: 300}, "upgrade_time": 50  # Clay 300, Wood 300
    },
    "Eisenmine_3": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 45, "resource_output": {RESOURCE_EISEN: 6}, "tech_required": None,  # AmountToMine=6
        "max_workers": 7, "mine_type": "Eisenmine",
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "Schwefelmine_1": {
        "build_time": 110, "cost": {},
        "taler_income": 25, "resource_output": {RESOURCE_SCHWEFEL: 4}, "tech_required": None,  # AmountToMine=4
        "max_workers": 5, "mine_type": "Schwefelmine",
        "upgrade_to": "Schwefelmine_2",
        "upgrade_cost": {RESOURCE_HOLZ: 150, RESOURCE_STEIN: 150}, "upgrade_time": 40  # Wood 150, Stone 150
    },
    "Schwefelmine_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 35, "resource_output": {RESOURCE_SCHWEFEL: 5}, "tech_required": None,  # AmountToMine=5
        "max_workers": 6, "mine_type": "Schwefelmine",
        "upgrade_to": "Schwefelmine_3",
        "upgrade_cost": {RESOURCE_LEHM: 200, RESOURCE_STEIN: 200}, "upgrade_time": 50  # Clay 200, Stone 200
    },
    "Schwefelmine_3": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 45, "resource_output": {RESOURCE_SCHWEFEL: 6}, "tech_required": None,  # AmountToMine=6
        "max_workers": 7, "mine_type": "Schwefelmine",
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === PRODUKTIONSGEBÃƒÆ’Ã¢â‚¬Å¾UDE (Refiner-GebÃƒÆ’Ã‚Â¤ude) - aus PB_*.xml ===
    # InitialFactor=4 fÃƒÆ’Ã‚Â¼r alle Refiner (ResourceRefinerBehavior)
    "SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle_1": {
        "build_time": 110, "cost": {RESOURCE_LEHM: 200, RESOURCE_STEIN: 150},  # Clay 200, Stone 150
        "taler_income": 12, "resource_output": {RESOURCE_HOLZ: 4}, "tech_required": "Konstruktion",
        "max_workers": 4, "upgrade_to": "SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle_2",  # MaxWorkers=4 (KORRIGIERT von 6!)
        "upgrade_cost": {RESOURCE_LEHM: 150, RESOURCE_STEIN: 100}, "upgrade_time": 40
    },
    "SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 18, "resource_output": {RESOURCE_HOLZ: 4}, "tech_required": "Konstruktion",
        "max_workers": 6, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "LehmhÃƒÆ’Ã‚Â¼tte_1": {
        "build_time": 110, "cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 150},  # Wood 200, Stone 150
        "taler_income": 12, "resource_output": {RESOURCE_LEHM: 4}, "tech_required": "Konstruktion",
        "max_workers": 4, "upgrade_to": "LehmhÃƒÆ’Ã‚Â¼tte_2",  # MaxWorkers=4 (KORRIGIERT von 6!)
        "upgrade_cost": {RESOURCE_HOLZ: 150, RESOURCE_STEIN: 200}, "upgrade_time": 40
    },
    "LehmhÃƒÆ’Ã‚Â¼tte_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 18, "resource_output": {RESOURCE_LEHM: 4}, "tech_required": "Konstruktion",
        "max_workers": 6, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "Schmiede_1": {
        "build_time": 110, "cost": {RESOURCE_LEHM: 400, RESOURCE_HOLZ: 300},  # Clay 400, Wood 300
        "taler_income": 12, "resource_output": {RESOURCE_EISEN: 4}, "tech_required": "Alchimie",
        "max_workers": 2, "upgrade_to": "Schmiede_2",  # MaxWorkers=2 (KORRIGIERT!)
        "upgrade_cost": {RESOURCE_LEHM: 100, RESOURCE_STEIN: 200}, "upgrade_time": 40
    },
    "Schmiede_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 18, "resource_output": {RESOURCE_EISEN: 4}, "tech_required": "Alchimie",
        "max_workers": 6, "upgrade_to": "Schmiede_3",
        "upgrade_cost": {RESOURCE_LEHM: 150, RESOURCE_STEIN: 300}, "upgrade_time": 50
    },
    "Schmiede_3": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 24, "resource_output": {RESOURCE_EISEN: 4}, "tech_required": "Alchimie",
        "max_workers": 6, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "AlchimistenhÃƒÆ’Ã‚Â¼tte_1": {
        "build_time": 80, "cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 400},  # Wood 200, Stone 400
        "taler_income": 12, "resource_output": {RESOURCE_SCHWEFEL: 4}, "tech_required": "Alchimie",
        "max_workers": 4, "upgrade_to": "AlchimistenhÃƒÆ’Ã‚Â¼tte_2",
        "upgrade_cost": {RESOURCE_STEIN: 250, RESOURCE_EISEN: 100}, "upgrade_time": 40
    },
    "AlchimistenhÃƒÆ’Ã‚Â¼tte_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 18, "resource_output": {RESOURCE_SCHWEFEL: 4}, "tech_required": "Alchimie",
        "max_workers": 6, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "SteinmetzhÃƒÆ’Ã‚Â¼tte_1": {
        "build_time": 80, "cost": {RESOURCE_LEHM: 300, RESOURCE_HOLZ: 200},  # Clay 300, Wood 200
        "taler_income": 12, "resource_output": {RESOURCE_STEIN: 4}, "tech_required": "ZahnrÃƒÆ’Ã‚Â¤der",
        "max_workers": 4, "upgrade_to": "SteinmetzhÃƒÆ’Ã‚Â¼tte_2",  # MaxWorkers=4 (KORRIGIERT von 6!)
        "upgrade_cost": {RESOURCE_LEHM: 150, RESOURCE_STEIN: 150}, "upgrade_time": 40
    },
    "SteinmetzhÃƒÆ’Ã‚Â¼tte_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 18, "resource_output": {RESOURCE_STEIN: 4}, "tech_required": "ZahnrÃƒÆ’Ã‚Â¤der",
        "max_workers": 6, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === SPEZIALGEBÃƒÆ’Ã¢â‚¬Å¾UDE ===
    "Bank_1": {
        "build_time": 130, "cost": {RESOURCE_HOLZ: 500, RESOURCE_STEIN: 500},
        "taler_income": 30, "resource_output": {RESOURCE_TALER: 2}, "tech_required": "Buchdruck",
        "max_workers": 4, "upgrade_to": "Bank_2",
        "upgrade_cost": {RESOURCE_STEIN: 300, RESOURCE_TALER: 200}, "upgrade_time": 40
    },
    "Bank_2": {
        "build_time": 60, "cost": {},
        "taler_income": 45, "resource_output": {RESOURCE_TALER: 4}, "tech_required": "Buchdruck",
        "max_workers": 6, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === KAPELLE ENTFERNT - existiert NICHT im Original-Spiel! ===
    # (Kein PB_ChurchVillage in Spieldateien gefunden)

    # === KLOSTER (Monastery) - aus extra2 ===
    # Produziert Faith, kann Segen sprechen (5 Kategorien)
    # MotivationEffect: 0.08 / 0.10 / 0.15 pro Level
    "Kloster_1": {
        "build_time": 140, "cost": {RESOURCE_HOLZ: 500, RESOURCE_STEIN: 550},
        "taler_income": 0, "resource_output": {}, "tech_required": "Bildung",
        "max_workers": 6, "motivation_effect": 0.08,
        "upgrade_to": "Kloster_2",
        "upgrade_cost": {RESOURCE_LEHM: 400, RESOURCE_STEIN: 500, RESOURCE_TALER: 200}, "upgrade_time": 60
    },
    "Kloster_2": {
        "build_time": 60, "cost": {},
        "taler_income": 0, "resource_output": {}, "tech_required": "Bildung",
        "max_workers": 8, "motivation_effect": 0.10,
        "upgrade_to": "Kloster_3",
        "upgrade_cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 600, RESOURCE_TALER: 300}, "upgrade_time": 90
    },
    "Kloster_3": {
        "build_time": 60, "cost": {},
        "taler_income": 0, "resource_output": {}, "tech_required": "Bildung",
        "max_workers": 10, "motivation_effect": 0.15,
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === MARKT/LAGER (aus extra2) ===
    # Ist ein Supplier fÃƒÆ’Ã‚Â¼r ALLE Ressourcen - Serfs kÃƒÆ’Ã‚Â¶nnen dort Ressourcen abholen
    # Level 1: Keine Arbeiter (Trade auskommentiert in extra2)
    # Level 2: 6 Trader (fÃƒÆ’Ã‚Â¼r Handel, aber wir nutzen nur als Lager)
    "Markt_1": {
        "build_time": 80, "cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 400},
        "taler_income": 0, "resource_output": {}, "tech_required": "Handelswesen",
        "max_workers": 0, "is_supplier": True,  # Kann als Ressourcen-Quelle dienen
        "supplier_resources": ["Holz", "Stein", "Lehm", "Eisen", "Schwefel", "Taler"],
        "upgrade_to": "Markt_2",
        "upgrade_cost": {RESOURCE_LEHM: 100, RESOURCE_STEIN: 200}, "upgrade_time": 40
    },
    "Markt_2": {
        "build_time": 60, "cost": {},
        "taler_income": 0, "resource_output": {}, "tech_required": "Handelswesen",
        "max_workers": 6, "is_supplier": True,
        "supplier_resources": ["Holz", "Stein", "Lehm", "Eisen", "Schwefel", "Taler"],
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === MILITÃƒÆ’Ã¢â‚¬Å¾RGEBÃƒÆ’Ã¢â‚¬Å¾UDE ===
    "Kaserne_1": {
        "build_time": 90, "cost": {RESOURCE_HOLZ: 300, RESOURCE_STEIN: 350},
        "taler_income": 0, "resource_output": {}, "tech_required": "Wehrpflicht",
        "max_workers": 0, "upgrade_to": "Kaserne_2",
        "upgrade_cost": {RESOURCE_STEIN: 300, RESOURCE_LEHM: 200}, "upgrade_time": 40
    },
    "Kaserne_2": {
        "build_time": 60, "cost": {},
        "taler_income": 0, "resource_output": {}, "tech_required": "Wehrpflicht",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "SchieÃƒÆ’Ã…Â¸platz_1": {
        "build_time": 90, "cost": {RESOURCE_HOLZ: 300, RESOURCE_STEIN: 350},
        "taler_income": 0, "resource_output": {}, "tech_required": "Stehendes Heer",
        "max_workers": 0, "upgrade_to": "SchieÃƒÆ’Ã…Â¸platz_2",
        "upgrade_cost": {RESOURCE_STEIN: 200, RESOURCE_LEHM: 100}, "upgrade_time": 40
    },
    "SchieÃƒÆ’Ã…Â¸platz_2": {
        "build_time": 60, "cost": {},
        "taler_income": 0, "resource_output": {}, "tech_required": "Stehendes Heer",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "Stall_1": {
        "build_time": 120, "cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 350},
        "taler_income": 0, "resource_output": {}, "tech_required": "Taktiken",
        "max_workers": 0, "upgrade_to": "Stall_2",
        "upgrade_cost": {RESOURCE_STEIN: 300, RESOURCE_LEHM: 150}, "upgrade_time": 40
    },
    "Stall_2": {
        "build_time": 60, "cost": {},
        "taler_income": 0, "resource_output": {}, "tech_required": "Taktiken",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "KanongieÃƒÆ’Ã…Â¸erei_1": {
        "build_time": 110, "cost": {RESOURCE_LEHM: 500, RESOURCE_HOLZ: 300},  # Clay 500, Wood 300
        "taler_income": 5, "resource_output": {}, "tech_required": "Metallurgie",
        "max_workers": 1, "upgrade_to": "KanongieÃƒÆ’Ã…Â¸erei_2",  # CannonSlots=2
        "upgrade_cost": {RESOURCE_LEHM: 150, RESOURCE_STEIN: 200}, "upgrade_time": 40
    },
    "KanongieÃƒÆ’Ã…Â¸erei_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 10, "resource_output": {}, "tech_required": "Metallurgie",
        "max_workers": 1, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None  # CannonSlots=4
    },

    # === TÃƒÆ’Ã…â€œRME ===
    "Turm_1": {
        "build_time": 80, "cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 200},
        "taler_income": 0, "resource_output": {}, "tech_required": "Konstruktion",
        "max_workers": 0, "upgrade_to": "Turm_2",
        "upgrade_cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 300}, "upgrade_time": 15
    },
    "Turm_2": {
        "build_time": 60, "cost": {},
        "taler_income": 0, "resource_output": {}, "tech_required": "Konstruktion",
        "max_workers": 0, "upgrade_to": "Turm_3",
        "upgrade_cost": {RESOURCE_STEIN: 200, RESOURCE_SCHWEFEL: 200}, "upgrade_time": 15
    },
    "Turm_3": {
        "build_time": 60, "cost": {},
        "taler_income": 0, "resource_output": {}, "tech_required": "Konstruktion",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # Aussichtsturm entfernt - existiert nicht im echten Spiel!
    # (pb_darktower ist nur fÃƒÆ’Ã‚Â¼r KI/Feinde)

    # === WETTERGEBÃƒÆ’Ã¢â‚¬Å¾UDE ===
    "Wetterturm": {
        "build_time": 40, "cost": {RESOURCE_HOLZ: 500, RESOURCE_SCHWEFEL: 500},
        "taler_income": 0, "resource_output": {}, "tech_required": "Fernglas",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },
    "Wetterkraftwerk": {
        "build_time": 40, "cost": {RESOURCE_HOLZ: 500, RESOURCE_STEIN: 300},
        "taler_income": 10, "resource_output": {}, "tech_required": "Chemie",
        "max_workers": 4, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === ADDON-GEBÃƒÆ’Ã¢â‚¬Å¾UDE ===
    "Taverne_1": {
        "build_time": 90, "cost": {RESOURCE_TALER: 400, RESOURCE_HOLZ: 300},  # Gold 400, Wood 300
        "taler_income": 25, "resource_output": {}, "tech_required": "Fernglas",
        "max_workers": 1, "upgrade_to": "Taverne_2",
        "upgrade_cost": {RESOURCE_TALER: 500, RESOURCE_STEIN: 300}, "upgrade_time": 60  # Gold 500, Stone 300
    },
    "Taverne_2": {
        "build_time": 90, "cost": {RESOURCE_TALER: 400, RESOURCE_HOLZ: 300},
        "taler_income": 40, "resource_output": {}, "tech_required": "Fernglas",
        "max_workers": 1, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "BÃƒÆ’Ã‚Â¼chsenmacherei_1": {
        "build_time": 110, "cost": {RESOURCE_STEIN: 400, RESOURCE_SCHWEFEL: 300},  # Kein Eisen! (aus PB_GunsmithWorkshop1.xml)
        "taler_income": 15, "resource_output": {}, "tech_required": "Luntenschloss",
        "max_workers": 2, "upgrade_to": "BÃƒÆ’Ã‚Â¼chsenmacherei_2",  # MaxWorkers=2 (aus XML)
        "upgrade_cost": {RESOURCE_STEIN: 300, RESOURCE_SCHWEFEL: 200}, "upgrade_time": 40  # UpgradeTime=40 (aus XML)
    },
    "BÃƒÆ’Ã‚Â¼chsenmacherei_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 25, "resource_output": {}, "tech_required": "Luntenschloss",
        "max_workers": 4, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None  # MaxWorkers=4 aus XML
    },

    "Architektenstube": {
        "build_time": 80, "cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 400},
        "taler_income": 10, "resource_output": {}, "tech_required": "Mathematik",
        "max_workers": 2, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "BrÃƒÆ’Ã‚Â¼cke": {
        "build_time": 80, "cost": {RESOURCE_HOLZ: 5, RESOURCE_STEIN: 5, RESOURCE_LEHM: 5},
        "taler_income": 0, "resource_output": {}, "tech_required": "Mathematik",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === SCHMUCKGEBÃƒÆ’Ã¢â‚¬Å¾UDE (Beautification, aus PB_Beautification01-12.xml) ===
    "PB_Beautification01": {
        "build_time": 20, "cost": {RESOURCE_STEIN: 100, RESOURCE_TALER: 200},
        "taler_income": 0, "resource_output": {}, "tech_required": "GT_Beautification",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None,
        "exploration": 12, "motivation_effect": 0.04
    },
    "PB_Beautification02": {
        "build_time": 20, "cost": {RESOURCE_STEIN: 100, RESOURCE_TALER: 200},
        "taler_income": 0, "resource_output": {}, "tech_required": "GT_Beautification",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None,
        "exploration": 12, "motivation_effect": 0.04
    },
    "PB_Beautification03": {
        "build_time": 40, "cost": {RESOURCE_STEIN: 200, RESOURCE_TALER: 400},
        "taler_income": 0, "resource_output": {}, "tech_required": "GT_Beautification",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None,
        "exploration": 12, "motivation_effect": 0.06
    },
    "PB_Beautification04": {
        "build_time": 10, "cost": {RESOURCE_LEHM: 100, RESOURCE_TALER: 100},
        "taler_income": 0, "resource_output": {}, "tech_required": "GT_Beautification",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None,
        "exploration": 12, "motivation_effect": 0.02
    },
    "PB_Beautification05": {
        "build_time": 30, "cost": {RESOURCE_STEIN: 100, RESOURCE_TALER: 300},
        "taler_income": 0, "resource_output": {}, "tech_required": "GT_Beautification",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None,
        "exploration": 12, "motivation_effect": 0.05
    },
    "PB_Beautification06": {
        "build_time": 10, "cost": {RESOURCE_TALER: 100, RESOURCE_EISEN: 100},
        "taler_income": 0, "resource_output": {}, "tech_required": "GT_Beautification",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None,
        "exploration": 12, "motivation_effect": 0.02
    },
    "PB_Beautification07": {
        "build_time": 30, "cost": {RESOURCE_HOLZ: 100, RESOURCE_TALER: 300},
        "taler_income": 0, "resource_output": {}, "tech_required": "GT_Beautification",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None,
        "exploration": 12, "motivation_effect": 0.05
    },
    "PB_Beautification08": {
        "build_time": 30, "cost": {RESOURCE_STEIN: 100, RESOURCE_TALER: 300},
        "taler_income": 0, "resource_output": {}, "tech_required": "GT_Beautification",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None,
        "exploration": 12, "motivation_effect": 0.05
    },
    "PB_Beautification09": {
        "build_time": 10, "cost": {RESOURCE_HOLZ: 100, RESOURCE_TALER: 100},
        "taler_income": 0, "resource_output": {}, "tech_required": "GT_Beautification",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None,
        "exploration": 12, "motivation_effect": 0.02
    },
    "PB_Beautification10": {
        "build_time": 40, "cost": {RESOURCE_TALER: 400, RESOURCE_EISEN: 200},
        "taler_income": 0, "resource_output": {}, "tech_required": "GT_Beautification",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None,
        "exploration": 12, "motivation_effect": 0.06
    },
    "PB_Beautification11": {
        "build_time": 40, "cost": {RESOURCE_STEIN: 200, RESOURCE_TALER: 400},
        "taler_income": 0, "resource_output": {}, "tech_required": "GT_Beautification",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None,
        "exploration": 12, "motivation_effect": 0.06
    },
    "PB_Beautification12": {
        "build_time": 20, "cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 100},
        "taler_income": 0, "resource_output": {}, "tech_required": "GT_Beautification",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None,
        "exploration": 12, "motivation_effect": 0.04
    },
}

# GebÃƒÆ’Ã‚Â¤ude-Datenbank (ohne Multiplikator - echte Spielwerte)
buildings_db = copy.deepcopy(_raw_buildings_db)

# Strict XML: keine passiven Income/Output-Werte in Entity-XMLs
for _b_info in buildings_db.values():
    _b_info["taler_income"] = 0
    _b_info["resource_output"] = {}

# Fehlende Worker-Typen aus GebÃƒÆ’Ã‚Â¤ude-Basis ableiten.
for _b_name, _b_info in buildings_db.items():
    _base = _b_name.rsplit("_", 1)[0] if _b_name.rsplit("_", 1)[-1].isdigit() else _b_name
    _worker_type = BUILDING_WORKER_TYPES.get(_base)
    if _worker_type and not _b_info.get("worker_type"):
        _b_info["worker_type"] = _worker_type

# XML-Sonderfall: Tavern2 nutzt PU_Farmer als Worker.
if "Taverne_2" in buildings_db:
    buildings_db["Taverne_2"]["worker_type"] = "farmer"
# XML-Sonderfall: Markt_1 hat keinen Worker-Typ (erst Markt_2 hat Trader).
if "Markt_1" in buildings_db:
    buildings_db["Markt_1"]["worker_type"] = ""


# =============================================================================
# VOLLSTÃƒÆ’Ã¢â‚¬Å¾NDIGE TECHNOLOGIE-DATENBANK (55+ Technologien)
# =============================================================================

technologies = {
    "GT_Beautification": {"cost": {RESOURCE_TALER: 1000}, "tech_required": [],
                          "unlocks_buildings": [], "research_time": 90, "auto_research": True},
    "Konstruktion": {"cost": {RESOURCE_HOLZ: 200, RESOURCE_LEHM: 150}, "tech_required": [],
        "research_buildings": ["Hochschule"],
                    "unlocks_buildings": ["SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle_1", "LehmhÃƒÆ’Ã‚Â¼tte_1", "Turm_1"], "research_time": 20},
    "ZahnrÃƒÆ’Ã‚Â¤der": {"cost": {RESOURCE_STEIN: 400, RESOURCE_EISEN: 200}, "tech_required": ["Konstruktion"],
        "research_buildings": ["Hochschule"],
                 "unlocks_buildings": ["SteinmetzhÃƒÆ’Ã‚Â¼tte_1"], "research_time": 40},
    "Flaschenzug": {"cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 300}, "tech_required": ["ZahnrÃƒÆ’Ã‚Â¤der"],
        "research_buildings": ["Hochschule"],
                   "unlocks_buildings": [], "research_time": 40},
    "Architektur": {"cost": {RESOURCE_STEIN: 600, RESOURCE_EISEN: 500}, "tech_required": ["Flaschenzug"],
        "research_buildings": ["Hochschule"],
                   "unlocks_buildings": [], "research_time": 80, "effects": {"armor_bonus": 5}},
    "Alchimie": {"cost": {RESOURCE_HOLZ: 50, RESOURCE_SCHWEFEL: 150}, "tech_required": [],
        "research_buildings": ["Hochschule"],
                "unlocks_buildings": ["AlchimistenhÃƒÆ’Ã‚Â¼tte_1", "Schmiede_1"], "research_time": 20},
    "Legierungen": {"cost": {RESOURCE_EISEN: 200, RESOURCE_SCHWEFEL: 300}, "tech_required": ["Alchimie"],
        "research_buildings": ["Hochschule"],
                   "unlocks_buildings": [], "research_time": 40},
    "Metallurgie": {"cost": {RESOURCE_EISEN: 400, RESOURCE_SCHWEFEL: 400}, "tech_required": ["Legierungen"],
        "research_buildings": ["Hochschule"],
                   "unlocks_buildings": ["KanongieÃƒÆ’Ã…Â¸erei_1"], "research_time": 60},
    "Chemie": {"cost": {RESOURCE_EISEN: 500, RESOURCE_SCHWEFEL: 600}, "tech_required": ["Metallurgie"],
        "research_buildings": ["Hochschule"],
              "unlocks_buildings": ["Wetterkraftwerk"], "research_time": 80},
    "Bildung": {"cost": {RESOURCE_TALER: 50, RESOURCE_HOLZ: 150}, "tech_required": [],
        "research_buildings": ["Hochschule"],
               "unlocks_buildings": ["Kloster_1"], "research_time": 20},
    "Handelswesen": {"cost": {RESOURCE_TALER: 300}, "tech_required": ["Bildung"],
        "research_buildings": ["Hochschule"],
                    "unlocks_buildings": ["Markt_1"], "research_time": 40},
    "Buchdruck": {"cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 200}, "tech_required": ["Handelswesen"],
        "research_buildings": ["Hochschule"],
                 "unlocks_buildings": ["Bank_1"], "research_time": 40},
    "BÃƒÆ’Ã‚Â¼chereien": {"cost": {RESOURCE_TALER: 500, RESOURCE_HOLZ: 300}, "tech_required": ["Buchdruck"],
        "research_buildings": ["Hochschule"],
                  "unlocks_buildings": [], "research_time": 80},
    "Wehrpflicht": {"cost": {RESOURCE_TALER: 50, RESOURCE_HOLZ: 150}, "tech_required": [],
        "research_buildings": ["Hochschule"],
                   "unlocks_buildings": ["Kaserne_1"], "research_time": 20},
    "Stehendes Heer": {"cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 200}, "tech_required": ["Wehrpflicht"],
        "research_buildings": ["Hochschule"],
                      "unlocks_buildings": ["SchieÃƒÆ’Ã…Â¸platz_1"], "research_time": 40},
    "Taktiken": {"cost": {RESOURCE_TALER: 400, RESOURCE_EISEN: 400}, "tech_required": ["Stehendes Heer"],
        "research_buildings": ["Hochschule"],
                "unlocks_buildings": ["Stall_1"], "research_time": 60, "effects": {"speed_bonus": 50}},
    "Pferdezucht": {"cost": {RESOURCE_TALER: 600, RESOURCE_EISEN: 600}, "tech_required": ["Taktiken"],
        "research_buildings": ["Hochschule"],
                   "unlocks_buildings": [], "research_time": 80},
    "Mathematik": {"cost": {RESOURCE_TALER: 100, RESOURCE_HOLZ: 200}, "tech_required": [],
        "research_buildings": ["Hochschule"],
                  "unlocks_buildings": ["Architektenstube"], "research_time": 20},
    "Fernglas": {"cost": {RESOURCE_TALER: 300, RESOURCE_EISEN: 300}, "tech_required": ["Mathematik"],
        "research_buildings": ["Hochschule"],
                "unlocks_buildings": ["Wetterturm", "Taverne_1"], "research_time": 30, "requires_building": "Hauptquartier_2"},
    "Luntenschloss": {"cost": {RESOURCE_EISEN: 300, RESOURCE_SCHWEFEL: 300}, "tech_required": ["Fernglas"],
        "research_buildings": ["Hochschule"],
                     "unlocks_buildings": ["BÃƒÆ’Ã‚Â¼chsenmacherei_1"], "research_time": 50, "requires_building": "Hauptquartier_2"},
    "Gezogener Lauf": {"cost": {RESOURCE_EISEN: 500, RESOURCE_SCHWEFEL: 400}, "tech_required": ["Luntenschloss"],
        "research_buildings": ["Hochschule"],
                      "unlocks_buildings": [], "research_time": 70, "requires_building": "Hauptquartier_3"},  # TimeToResearch=70, braucht HQ3!
    "LederrÃƒÆ’Ã‚Â¼stung": {"cost": {RESOURCE_TALER: 100, RESOURCE_EISEN: 100}, "tech_required": [],
        "research_buildings": ["Schmiede"],
                    "unlocks_buildings": [], "research_time": 15, "effects": {"armor_bonus": 2}, "requires_building": "Schmiede_1"},
    "KettenrÃƒÆ’Ã‚Â¼stung": {"cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 200}, "tech_required": ["LederrÃƒÆ’Ã‚Â¼stung"],
        "research_buildings": ["Schmiede"],
                     "unlocks_buildings": [], "research_time": 20, "effects": {"armor_bonus": 2}, "requires_building": "Schmiede_2"},  # +2 (KORRIGIERT von +4), 20s (KORRIGIERT von 25)
    "PlattenrÃƒÆ’Ã‚Â¼stung": {"cost": {RESOURCE_TALER: 300, RESOURCE_EISEN: 300}, "tech_required": ["KettenrÃƒÆ’Ã‚Â¼stung"],
        "research_buildings": ["Schmiede"],
                      "unlocks_buildings": [], "research_time": 25, "effects": {"armor_bonus": 2}, "requires_building": "Schmiede_3"},  # +2 (KORRIGIERT von +6), 25s (KORRIGIERT von 35)
    "Maurerarbeit": {"cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 400}, "tech_required": [],
        "research_buildings": ["SteinmetzhÃƒÆ’Ã‚Â¼tte"],
                    "unlocks_buildings": [], "research_time": 20, "effects": {"building_armor_bonus": 3}, "requires_building": "SteinmetzhÃƒÆ’Ã‚Â¼tte_2"},
    "Leichte Ziegel": {"cost": {RESOURCE_TALER: 200, RESOURCE_LEHM: 400, RESOURCE_HOLZ: 100}, "tech_required": [],
        "research_buildings": ["LehmhÃƒÆ’Ã‚Â¼tte"],
        "disabled": True,
                      "unlocks_buildings": [], "research_time": 20, "effects": {"build_speed_bonus": 15}, "requires_building": "LehmhÃƒÆ’Ã‚Â¼tte_2"},  # T_LightBricks: Gold 200, Clay 400, Wood 100
    "Pfeilherstellung": {"cost": {RESOURCE_TALER: 100, RESOURCE_HOLZ: 100}, "tech_required": [],
        "research_buildings": ["SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle"],
                        "unlocks_buildings": [], "research_time": 20, "effects": {"bow_range_bonus": 300, "exploration_bonus": 3}, "requires_building": "SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle_2"},  # T_Fletching: +300 range, +3 exploration
    "Panzerbrechende Pfeile": {"cost": {RESOURCE_TALER: 200, RESOURCE_HOLZ: 200}, "tech_required": ["Pfeilherstellung"],
        "research_buildings": ["SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle"],
                              "unlocks_buildings": [], "research_time": 25, "effects": {"bow_damage_bonus": 2}, "requires_building": "SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle_2"},  # T_BodkinArrow: +2 damage (KORRIGIERT von +4)
    "Verbessertes SchieÃƒÆ’Ã…Â¸pulver": {"cost": {RESOURCE_TALER: 200, RESOURCE_SCHWEFEL: 200}, "tech_required": [],
        "research_buildings": ["AlchimistenhÃƒÆ’Ã‚Â¼tte"],
                                  "unlocks_buildings": [], "research_time": 20, "effects": {"cannon_damage_bonus": 4}, "requires_building": "AlchimistenhÃƒÆ’Ã‚Â¼tte_2"},  # +4 damage (KORRIGIERT von +3)
    "GlÃƒÆ’Ã‚Â¼hende Kanonenkugeln": {"cost": {RESOURCE_TALER: 200, RESOURCE_SCHWEFEL: 400}, "tech_required": ["Verbessertes SchieÃƒÆ’Ã…Â¸pulver"],
        "research_buildings": ["AlchimistenhÃƒÆ’Ã‚Â¼tte"],
                              "unlocks_buildings": [], "research_time": 20, "effects": {"cannon_damage_bonus": 4}, "requires_building": "AlchimistenhÃƒÆ’Ã‚Â¼tte_2"},  # +4 damage (KORRIGIERT von +5)
    "Schmiedekunst": {"cost": {RESOURCE_TALER: 300, RESOURCE_EISEN: 200}, "tech_required": [],
        "research_buildings": ["Schmiede"],
                     "unlocks_buildings": [], "research_time": 20, "effects": {"melee_damage_bonus": 2}, "requires_building": "Schmiede_2"},  # Gold 300, Iron 200
    "Eisenguss": {"cost": {RESOURCE_TALER: 500, RESOURCE_EISEN: 400}, "tech_required": ["Schmiedekunst"],
        "research_buildings": ["Schmiede"],
                 "unlocks_buildings": [], "research_time": 25, "effects": {"melee_damage_bonus": 2}, "requires_building": "Schmiede_2"},  # +2 (KORRIGIERT von +4), Gold 500, Iron 400
    "Weiche RÃƒÆ’Ã‚Â¼stung": {"cost": {RESOURCE_TALER: 100, RESOURCE_EISEN: 50}, "tech_required": [],
        "research_buildings": ["Schmiede"],
                      "unlocks_buildings": [], "research_time": 15, "effects": {"archer_armor_bonus": 2}, "requires_building": "Schmiede_1"},  # +2 (KORRIGIERT von +1), Iron 50
    "Wattierte RÃƒÆ’Ã‚Â¼stung": {"cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 200}, "tech_required": ["Weiche RÃƒÆ’Ã‚Â¼stung"],
        "research_buildings": ["Schmiede"],
                         "unlocks_buildings": [], "research_time": 20, "effects": {"archer_armor_bonus": 2}, "requires_building": "Schmiede_2"},  # +2
    "Leder-BogenschÃƒÆ’Ã‚Â¼tzenrÃƒÆ’Ã‚Â¼stung": {"cost": {RESOURCE_TALER: 300, RESOURCE_EISEN: 300}, "tech_required": ["Wattierte RÃƒÆ’Ã‚Â¼stung"],
        "research_buildings": ["Schmiede"],
                                   "unlocks_buildings": [], "research_time": 25, "effects": {"archer_armor_bonus": 2}, "requires_building": "Schmiede_3"},  # +2 (KORRIGIERT von +3)
    "Holzalterung": {"cost": {RESOURCE_TALER: 50, RESOURCE_HOLZ: 200}, "tech_required": [],
        "research_buildings": ["SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle"],
                    "unlocks_buildings": [], "research_time": 20, "effects": {"spear_damage_bonus": 2}, "requires_building": "SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle_2"},  # T_WoodAging: Gold 50, Wood 200, requires Sawmill2
    "Drechselei": {"cost": {RESOURCE_TALER: 100, RESOURCE_HOLZ: 300}, "tech_required": ["Holzalterung"],
        "research_buildings": ["SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle"],
                  "unlocks_buildings": [], "research_time": 25, "effects": {"spear_damage_bonus": 2}, "requires_building": "SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle_2"},  # T_Turnery: +2 (KORRIGIERT von +4), Gold 100, Wood 300
    "Wettervorhersage": {"cost": {RESOURCE_SCHWEFEL: 200, RESOURCE_TALER: 200}, "tech_required": [],
        "research_buildings": ["AlchimistenhÃƒÆ’Ã‚Â¼tte"],
                        "unlocks_buildings": [], "research_time": 30, "requires_building": "AlchimistenhÃƒÆ’Ã‚Â¼tte_1"},
    "Wettermanipulation": {"cost": {RESOURCE_SCHWEFEL: 400, RESOURCE_TALER: 400}, "tech_required": ["Wettervorhersage"],
        "research_buildings": ["AlchimistenhÃƒÆ’Ã‚Â¼tte"],
                          "unlocks_buildings": [], "research_time": 50, "requires_building": "AlchimistenhÃƒÆ’Ã‚Â¼tte_2"},
    "Schuldschein": {"cost": {RESOURCE_TALER: 300}, "tech_required": [],
        "research_buildings": ["Bank"],
        "disabled": True,
                    "unlocks_buildings": [], "research_time": 20, "effects": {"payday_bonus": 10}, "requires_building": "Bank_1"},  # T_Debenture: Gold 300, 20s (KORRIGIERT von 30s)
    "BuchfÃƒÆ’Ã‚Â¼hrung": {"cost": {RESOURCE_TALER: 400}, "tech_required": ["Schuldschein"],
        "research_buildings": ["Bank"],
        "disabled": True,
                   "unlocks_buildings": [], "research_time": 25, "effects": {"payday_bonus": 20}, "requires_building": "Bank_2"},  # T_BookKeeping: Gold 400 (KORRIGIERT von 500), 25s (KORRIGIERT von 40s)
    "Waage": {"cost": {RESOURCE_TALER: 200, RESOURCE_HOLZ: 50}, "tech_required": [],
        "research_buildings": ["Bank"],
        "disabled": True,
              "unlocks_buildings": [], "research_time": 20, "effects": {"trade_bonus": 5}, "requires_building": "Bank_1"},  # T_Scale: Gold 200, Wood 50 (KORRIGIERT: war Iron 100)
    "MÃƒÆ’Ã‚Â¼nzprÃƒÆ’Ã‚Â¤gung": {"cost": {RESOURCE_TALER: 300, RESOURCE_EISEN: 200}, "tech_required": ["Waage"],
        "disabled": True,
        "research_buildings": ["Bank"],
                   "unlocks_buildings": [], "research_time": 25, "effects": {"trade_bonus": 10}, "requires_building": "Bank_2"},  # T_Coinage: Gold 300 (KORRIGIERT von 400), Iron 200, 25s (KORRIGIERT von 30s)
    "Stadtwache": {"cost": {RESOURCE_TALER: 400}, "tech_required": [],
        "research_buildings": ["Dorfzentrum"],
                  "unlocks_buildings": [], "research_time": 20, "effects": {"exploration_bonus": 5}, "requires_building": "Dorfzentrum_1"},  # T_TownGuard: Gold 400 only (KORRIGIERT), 20s, requires VillageCenter1+
    "Webstuhl": {"cost": {RESOURCE_TALER: 200, RESOURCE_HOLZ: 100}, "tech_required": [],
        "research_buildings": ["Dorfzentrum"],
                "unlocks_buildings": [], "research_time": 20, "effects": {"worker_armor_bonus": 2}, "requires_building": "Dorfzentrum_2"},  # T_Loom: Gold 200, Wood 100, +2 (KORRIGIERT von +1), requires VillageCenter2+
    "Schuhe": {"cost": {RESOURCE_TALER: 300}, "tech_required": ["Webstuhl"],
        "research_buildings": ["Dorfzentrum"],
              "unlocks_buildings": [], "research_time": 25, "effects": {"worker_speed_bonus": 20}, "requires_building": "Dorfzentrum_3"},  # T_Shoes: Gold 300 only (KORRIGIERT), requires VillageCenter3
    "Kasernentraining": {"cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 200}, "tech_required": [],
        "research_buildings": ["Kaserne"],
                        "unlocks_buildings": [], "research_time": 50, "effects": {"infantry_training_speed": 30}, "requires_building": "Kaserne_2"},  # T_BetterTrainingBarracks: Gold 200 (KORRIGIERT von 300), Iron 200, 50s (KORRIGIERT von 30s), +30 (KORRIGIERT von +20)
    "SchieÃƒÆ’Ã…Â¸training": {"cost": {RESOURCE_TALER: 200, RESOURCE_HOLZ: 200}, "tech_required": [],
        "research_buildings": ["SchieÃƒÆ’Ã…Â¸platz"],
                      "unlocks_buildings": [], "research_time": 50, "effects": {"archer_training_speed": 40}, "requires_building": "SchieÃƒÆ’Ã…Â¸platz_2"},  # T_BetterTrainingArchery: Gold 200 (KORRIGIERT von 300), Wood 200, 50s (KORRIGIERT von 30s), +40 (KORRIGIERT von +20)
    "Hufbeschlag": {"cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 200}, "tech_required": [],
        "research_buildings": ["Stall"],
                   "unlocks_buildings": [], "research_time": 50, "effects": {"cavalry_speed_bonus": 50}, "requires_building": "Stall_2"},  # T_Shoeing: Gold 200, Iron 200, 50s ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦
    "Verbessertes Fahrgestell": {"cost": {RESOURCE_HOLZ: 200, RESOURCE_EISEN: 200}, "tech_required": [],
        "research_buildings": ["KanongieÃƒÆ’Ã…Â¸erei"],
                                 "unlocks_buildings": [], "research_time": 50, "effects": {"cannon_speed_bonus": 30}, "requires_building": "KanongieÃƒÆ’Ã…Â¸erei_2"},  # T_BetterChassis: Wood 200, Iron 200 (KORRIGIERT), 50s (KORRIGIERT von 40s)
    "T_FleeceArmor": {
        "cost": {RESOURCE_TALER: 100, RESOURCE_EISEN: 50},
        "tech_required": [],
        "unlocks_buildings": [],
        "research_time": 15,
        "effects": {"armor_modifier": 2},
        "entity_conditions": [{"building": "BÃƒÆ’Ã‚Â¼chsenmacherei_1", "amount": 1},
                              {"building": "BÃƒÆ’Ã‚Â¼chsenmacherei_2", "amount": 1}],
        "required_entity_conditions": 1,
        "research_buildings": ["BÃƒÆ’Ã‚Â¼chsenmacherei"],
    },  # T_FleeceArmor.xml
    "T_FleeceLinedLeatherArmor": {
        "cost": {RESOURCE_TALER: 200, RESOURCE_SCHWEFEL: 100},
        "tech_required": ["T_FleeceArmor"],
        "unlocks_buildings": [],
        "research_time": 30,
        "effects": {"armor_modifier": 2},
        "entity_conditions": [{"building": "BÃƒÆ’Ã‚Â¼chsenmacherei_2", "amount": 1}],
        "research_buildings": ["BÃƒÆ’Ã‚Â¼chsenmacherei"],
    },  # T_FleeceLinedLeatherArmor.xml
    "T_LeadShot": {
        "cost": {RESOURCE_TALER: 100, RESOURCE_SCHWEFEL: 50},
        "tech_required": [],
        "unlocks_buildings": [],
        "research_time": 15,
        "effects": {"damage_modifier": 3, "max_range_modifier": 300, "exploration_modifier": 3},
        "research_buildings": ["BÃƒÆ’Ã‚Â¼chsenmacherei"],
    },  # T_LeadShot.xml
    "T_Sights": {
        "cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 200},
        "tech_required": ["T_LeadShot"],
        "unlocks_buildings": [],
        "research_time": 30,
        "effects": {"max_range_modifier": 300, "exploration_modifier": 3},
        "entity_conditions": [{"building": "BÃƒÆ’Ã‚Â¼chsenmacherei_2", "amount": 1}],
        "required_entity_conditions": 1,
        "research_buildings": ["BÃƒÆ’Ã‚Â¼chsenmacherei"],
    },  # T_Sights.xml
    "T_UpgradeRifle1": {
        "cost": {RESOURCE_TALER: 300, RESOURCE_EISEN: 100, RESOURCE_SCHWEFEL: 200},
        "tech_required": [],
        "unlocks_buildings": [],
        "research_time": 100,
        "entity_conditions": [{"building": "SchieÃƒÆ’Ã…Â¸platz_2", "amount": 1},
                              {"building": "BÃƒÆ’Ã‚Â¼chsenmacherei_2", "amount": 1}],
        "research_buildings": ["SchieÃƒÆ’Ã…Â¸platz", "BÃƒÆ’Ã‚Â¼chsenmacherei"],
    },  # T_UpgradeRifle1.xml
    "MU_LeaderRifle": {
        "cost": {RESOURCE_LEHM: 100},
        "tech_required": [],
        "unlocks_buildings": [],
        "research_time": 1,
        "entity_conditions": [{"building": "BÃƒÆ’Ã‚Â¼chsenmacherei_1", "amount": 1},
                              {"building": "BÃƒÆ’Ã‚Â¼chsenmacherei_2", "amount": 1}],
        "required_entity_conditions": 1,
        "research_buildings": ["BÃƒÆ’Ã‚Â¼chsenmacherei"],
    },  # MU_LeaderRifle.xml
    "MU_Thief": {
        "cost": {RESOURCE_LEHM: 100},
        "tech_required": [],
        "unlocks_buildings": [],
        "research_time": 1,
        "entity_conditions": [{"building": "Taverne_2", "amount": 1}],
        "research_buildings": ["Taverne"],
    },  # MU_Thief.xml
    "T_ScoutFindResources": {
        "cost": {RESOURCE_TALER: 20, RESOURCE_STEIN: 20, RESOURCE_LEHM: 20, RESOURCE_EISEN: 20, RESOURCE_SCHWEFEL: 10},
        "tech_required": [],
        "unlocks_buildings": [],
        "research_time": 30,
        "research_buildings": ["Taverne"],
    },  # T_ScoutFindResources.xml
    "T_ScoutTorches": {
        "cost": {RESOURCE_TALER: 100, RESOURCE_SCHWEFEL: 100},
        "tech_required": ["T_ScoutFindResources"],
        "unlocks_buildings": [],
        "research_time": 40,
        "entity_conditions": [{"building": "Taverne_2", "amount": 1}],
        "research_buildings": ["Taverne"],
    },  # T_ScoutTorches.xml
    "T_ThiefSabotage": {
        "cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 100, RESOURCE_SCHWEFEL: 200},
        "tech_required": [],
        "unlocks_buildings": [],
        "research_time": 60,
        "entity_conditions": [{"building": "Taverne_2", "amount": 1}],
        "research_buildings": ["Taverne"],
    },  # T_ThiefSabotage.xml
    "B_Bridge": {
        "cost": {RESOURCE_LEHM: 100},
        "tech_required": ["Mathematik"],
        "unlocks_buildings": [],
        "research_time": 3,
        "entity_conditions": [{"building": "Architektenstube", "amount": 1}],
        "research_buildings": ["Architektenstube"],
    },  # B_Bridge.xml
    "T_BlessSettlers3": {
        "cost": {RESOURCE_LEHM: 100},
        "tech_required": [],
        "unlocks_buildings": [],
        "research_time": 1,
        "entity_conditions": [{"building": "Kloster_2", "amount": 1},
                              {"building": "Kloster_3", "amount": 1}],
        "required_entity_conditions": 1,
        "research_buildings": ["Kloster"],
    },  # T_BlessSettlers3.xml
    "T_BlessSettlers4": {
        "cost": {RESOURCE_LEHM: 100},
        "tech_required": [],
        "unlocks_buildings": [],
        "research_time": 1,
        "entity_conditions": [{"building": "Kloster_2", "amount": 1},
                              {"building": "Kloster_3", "amount": 1}],
        "required_entity_conditions": 1,
        "research_buildings": ["Kloster"],
    },  # T_BlessSettlers4.xml
    "T_BlessSettlers5": {
        "cost": {RESOURCE_LEHM: 100},
        "tech_required": [],
        "unlocks_buildings": [],
        "research_time": 1,
        "entity_conditions": [{"building": "Kloster_3", "amount": 1}],
        "required_entity_conditions": 1,
        "research_buildings": ["Kloster"],
    },  # T_BlessSettlers5.xml
    "T_MakeRain": {
        "cost": {},
        "tech_required": [],
        "unlocks_buildings": [],
        "research_time": 30,
        "entity_conditions": [{"building": "Wetterkraftwerk", "amount": 1}],
        "research_buildings": ["Wetterkraftwerk"],
    },  # T_MakeRain.xml
    "T_MakeSnow": {
        "cost": {},
        "tech_required": [],
        "unlocks_buildings": [],
        "research_time": 30,
        "entity_conditions": [{"building": "Wetterkraftwerk", "amount": 1}],
        "research_buildings": ["Wetterkraftwerk"],
    },  # T_MakeSnow.xml
    "T_MakeSummer": {
        "cost": {},
        "tech_required": [],
        "unlocks_buildings": [],
        "research_time": 30,
        "entity_conditions": [{"building": "Wetterkraftwerk", "amount": 1}],
        "research_buildings": ["Wetterkraftwerk"],
    },  # T_MakeSummer.xml
    "UP2_Headquarter": {
        "cost": {RESOURCE_LEHM: 100},
        "tech_required": [],
        "unlocks_buildings": [],
        "research_time": 3,
        "entity_conditions": [{"building": "Schmiede_1", "amount": 1},
                              {"building": "Schmiede_2", "amount": 1},
                              {"building": "Schmiede_3", "amount": 1},
                              {"building": "SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle_1", "amount": 1},
                              {"building": "SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle_2", "amount": 1},
                              {"building": "AlchimistenhÃƒÆ’Ã‚Â¼tte_1", "amount": 1},
                              {"building": "AlchimistenhÃƒÆ’Ã‚Â¼tte_2", "amount": 1},
                              {"building": "SteinmetzhÃƒÆ’Ã‚Â¼tte_1", "amount": 1},
                              {"building": "SteinmetzhÃƒÆ’Ã‚Â¼tte_2", "amount": 1},
                              {"building": "LehmhÃƒÆ’Ã‚Â¼tte_1", "amount": 1},
                              {"building": "LehmhÃƒÆ’Ã‚Â¼tte_2", "amount": 1},
                              {"building": "BÃƒÆ’Ã‚Â¼chsenmacherei_1", "amount": 1},
                              {"building": "BÃƒÆ’Ã‚Â¼chsenmacherei_2", "amount": 1}],
        "required_entity_conditions": 3,
        "research_buildings": ["LehmhÃƒÆ’Ã‚Â¼tte"],
    },  # UP2_Headquarter.xml
}


# =============================================================================
# VOLLSTÃƒÆ’Ã¢â‚¬Å¾NDIGE SOLDATEN-DATENBANK (40+ Einheiten)
# =============================================================================

soldiers_db = {
    # === SCHWERTKÃƒÆ’Ã¢â‚¬Å¾MPFER (4 Level) - aus PU_LeaderSword1-4.xml ===
    # TrainingTime kommt vom GEBÃƒÆ’Ã¢â‚¬Å¾UDE: Barracks1=20s, Barracks2=30s
    "SchwertkÃƒÆ’Ã‚Â¤mpfer_1": {"cost": {RESOURCE_TALER: 100, RESOURCE_EISEN: 50}, "requirements": ["Kaserne_1"],
                         "population_cost": 1, "train_time": 20, "upgrade_to": "SchwertkÃƒÆ’Ã‚Â¤mpfer_2"},
    "SchwertkÃƒÆ’Ã‚Â¤mpfer_2": {"cost": {RESOURCE_TALER: 150, RESOURCE_EISEN: 60}, "requirements": ["Kaserne_1"],
                         "population_cost": 1, "train_time": 20, "upgrade_to": "SchwertkÃƒÆ’Ã‚Â¤mpfer_3"},
    "SchwertkÃƒÆ’Ã‚Â¤mpfer_3": {"cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 70}, "requirements": ["Kaserne_2"],
                         "population_cost": 1, "train_time": 30, "upgrade_to": "SchwertkÃƒÆ’Ã‚Â¤mpfer_4"},
    "SchwertkÃƒÆ’Ã‚Â¤mpfer_4": {"cost": {RESOURCE_TALER: 250, RESOURCE_EISEN: 80}, "requirements": ["Kaserne_2"],
                         "population_cost": 1, "train_time": 30, "upgrade_to": None},

    # === SPEERTRÃƒÆ’Ã¢â‚¬Å¾GER (4 Level) - aus PU_LeaderPoleArm1-4.xml ===
    "SpeertrÃƒÆ’Ã‚Â¤ger_1": {"cost": {RESOURCE_TALER: 80, RESOURCE_HOLZ: 50}, "requirements": ["Kaserne_1"],
                      "population_cost": 1, "train_time": 20, "upgrade_to": "SpeertrÃƒÆ’Ã‚Â¤ger_2"},
    "SpeertrÃƒÆ’Ã‚Â¤ger_2": {"cost": {RESOURCE_TALER: 120, RESOURCE_HOLZ: 60}, "requirements": ["Kaserne_1"],
                      "population_cost": 1, "train_time": 20, "upgrade_to": "SpeertrÃƒÆ’Ã‚Â¤ger_3"},
    "SpeertrÃƒÆ’Ã‚Â¤ger_3": {"cost": {RESOURCE_TALER: 160, RESOURCE_HOLZ: 70}, "requirements": ["Kaserne_2"],
                      "population_cost": 1, "train_time": 30, "upgrade_to": "SpeertrÃƒÆ’Ã‚Â¤ger_4"},
    "SpeertrÃƒÆ’Ã‚Â¤ger_4": {"cost": {RESOURCE_TALER: 200, RESOURCE_HOLZ: 80}, "requirements": ["Kaserne_2"],
                      "population_cost": 1, "train_time": 30, "upgrade_to": None},

    # === BOGENSCHÃƒÆ’Ã…â€œTZEN (3 Level) - aus PU_LeaderBow1-3.xml ===
    "BogenschÃƒÆ’Ã‚Â¼tzen_1": {"cost": {RESOURCE_TALER: 150, RESOURCE_HOLZ: 60}, "requirements": ["SchieÃƒÆ’Ã…Â¸platz_1"],
                        "population_cost": 1, "train_time": 20, "upgrade_to": "BogenschÃƒÆ’Ã‚Â¼tzen_2"},
    "BogenschÃƒÆ’Ã‚Â¼tzen_2": {"cost": {RESOURCE_TALER: 200, RESOURCE_HOLZ: 70}, "requirements": ["SchieÃƒÆ’Ã…Â¸platz_1"],
                        "population_cost": 1, "train_time": 20, "upgrade_to": "BogenschÃƒÆ’Ã‚Â¼tzen_3"},
    "BogenschÃƒÆ’Ã‚Â¼tzen_3": {"cost": {RESOURCE_TALER: 250, RESOURCE_EISEN: 70}, "requirements": ["SchieÃƒÆ’Ã…Â¸platz_2"],
                        "population_cost": 1, "train_time": 30, "upgrade_to": None},

    # === LEICHTE KAVALLERIE (2 Level) - aus PU_LeaderCavalry1-2.xml ===
    "Leichte Kavallerie_1": {"cost": {RESOURCE_TALER: 200, RESOURCE_HOLZ: 60}, "requirements": ["Stall_1"],
                              "population_cost": 2, "train_time": 20, "upgrade_to": "Leichte Kavallerie_2"},
    "Leichte Kavallerie_2": {"cost": {RESOURCE_TALER: 250, RESOURCE_HOLZ: 70}, "requirements": ["Stall_2"],
                              "population_cost": 2, "train_time": 20, "upgrade_to": None},

    # === SCHWERE KAVALLERIE (2 Level) - aus PU_LeaderHeavyCavalry1-2.xml ===
    "Schwere Kavallerie_1": {"cost": {RESOURCE_TALER: 250, RESOURCE_EISEN: 80}, "requirements": ["Stall_1", "Taktiken"],
                              "population_cost": 3, "train_time": 20, "upgrade_to": "Schwere Kavallerie_2"},
    "Schwere Kavallerie_2": {"cost": {RESOURCE_TALER: 350, RESOURCE_EISEN: 90}, "requirements": ["Stall_2", "Pferdezucht"],
                              "population_cost": 3, "train_time": 20, "upgrade_to": None},

    # === KANONEN (4 Level) - aus PV_Cannon1-4.xml ===
    "Kanonen_1": {"cost": {RESOURCE_TALER: 150, RESOURCE_EISEN: 50, RESOURCE_SCHWEFEL: 100}, "requirements": ["KanongieÃƒÆ’Ã…Â¸erei_1"],
                  "population_cost": 5, "train_time": 60, "upgrade_to": "Kanonen_2"},
    "Kanonen_2": {"cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 50, RESOURCE_SCHWEFEL: 120}, "requirements": ["KanongieÃƒÆ’Ã…Â¸erei_1"],
                  "population_cost": 5, "train_time": 60, "upgrade_to": "Kanonen_3"},
    "Kanonen_3": {"cost": {RESOURCE_TALER: 300, RESOURCE_EISEN: 100, RESOURCE_SCHWEFEL: 150}, "requirements": ["KanongieÃƒÆ’Ã…Â¸erei_2"],
                  "population_cost": 5, "train_time": 60, "upgrade_to": "Kanonen_4"},
    "Kanonen_4": {"cost": {RESOURCE_TALER: 300, RESOURCE_EISEN: 200, RESOURCE_SCHWEFEL: 200}, "requirements": ["KanongieÃƒÆ’Ã…Â¸erei_2"],
                  "population_cost": 5, "train_time": 60, "upgrade_to": None},

    # === SCHARFSCHÃƒÆ’Ã…â€œTZEN (2 Level) - HAUPTZIEL! ===
    # Kosten aus PU_LeaderRifle1.xml: Gold=250, Sulfur=70 (KORRIGIERT! War vorher 50/40)
    "ScharfschÃƒÆ’Ã‚Â¼tzen": {"cost": {RESOURCE_TALER: 250, RESOURCE_SCHWEFEL: 70}, "requirements": ["BÃƒÆ’Ã‚Â¼chsenmacherei_1"],
                       "population_cost": 1, "train_time": 20, "upgrade_to": "ScharfschÃƒÆ’Ã‚Â¼tzen_2"},
    # Kosten aus PU_LeaderRifle2.xml: Gold=300, Sulfur=80 (war bereits korrekt)
    "ScharfschÃƒÆ’Ã‚Â¼tzen_2": {"cost": {RESOURCE_TALER: 300, RESOURCE_SCHWEFEL: 80}, "requirements": ["BÃƒÆ’Ã‚Â¼chsenmacherei_2", "Gezogener Lauf"],
                         "population_cost": 1, "train_time": 30, "upgrade_to": None},

    # === SPEZIALEINHEITEN ===
    "Dieb": {"cost": {RESOURCE_TALER: 300, RESOURCE_EISEN: 30}, "requirements": ["Taverne_2"],
             "population_cost": 5, "train_time": 45, "upgrade_to": None},
    "SpÃƒÆ’Ã‚Â¤her": {"cost": {RESOURCE_TALER: 100, RESOURCE_EISEN: 50}, "requirements": ["Taverne_1"],
               "population_cost": 1, "train_time": 15, "upgrade_to": None},

    # === LEIBEIGENE (Arbeiter-Rekrutierung) ===
    "Leibeigener": {"cost": {RESOURCE_TALER: 50}, "requirements": ["Hauptquartier_1"],
                    "population_cost": 1, "train_time": 10, "upgrade_to": None},
}


# =============================================================================
# SPIELKONSTANTEN
# =============================================================================

TIME_STEP = 1
INCOME_CYCLE = 40
TOTAL_SIM_TIME = 1800  # 30 Minuten
MAX_POSSIBLE_LEIBEIGENE = 400
# TL_SERF_BUILD.xml: ein Hammerschlag besteht aus 400ms + 1000ms.
SERF_BUILD_SWING_SECONDS = 1.4
# ZB_ConstructionSite*.xml: MaxWorkers=4 fuer Bau-/Upgrade-Baustellen.
MAX_ACTIVE_BUILDERS_PER_SITE = 4

# Passives GebÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¤ude-Output (pro INCOME_CYCLE, um DoppelzÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¤hlung zu vermeiden)
PASSIVE_OUTPUT_CYCLE = INCOME_CYCLE
PASSIVE_OUTPUT_EXCLUDE_BASES = set(RESOURCE_PRODUCTION_BASES)

# =============================================================================
# LEIBEIGENE & STEUER-KONSTANTEN
# =============================================================================

# Kosten fÃƒÆ’Ã‚Â¼r Leibeigene kaufen (im echten Spiel: 50 Taler)
SERF_BUY_COST = 50

# =============================================================================
# STEUERSYSTEM (aus extra2/logic.xml)
# =============================================================================
# TaxAmount = 5 pro Worker pro Tick
# RegularTax = fester Betrag pro Worker (NICHT Multiplikator!)
# MotivationChange = ÃƒÆ’Ã¢â‚¬Å¾nderung der Motivation pro Tick
TAX_AMOUNT_PER_WORKER = 5  # Basis-Steuerbetrag pro Worker
TAX_PENALTY = 0.1  # Extra Motivationsstrafe beim Steuereintreiben (Logic.xml: TaxPenalty=0.1)

TAX_LEVELS = {
    0: {"name": "Keine Steuern", "regular_tax": 0, "motivation_change": 0.20},
    1: {"name": "Niedrige Steuern", "regular_tax": 5, "motivation_change": 0.08},
    2: {"name": "Normale Steuern", "regular_tax": 10, "motivation_change": 0.0},
    3: {"name": "Hohe Steuern", "regular_tax": 15, "motivation_change": -0.08},
    4: {"name": "Sehr hohe Steuern", "regular_tax": 20, "motivation_change": -0.12},
}
INITIAL_TAX_LEVEL = 2  # Normale Steuern als Start

# =============================================================================
# SEGEN-SYSTEM (aus extra2/logic.xml)
# =============================================================================
# BlessingBonus = 0.3 (+30% Motivation)
# BlessingBonusTime = 180 Sekunden
# BlessingCost = 0 Faith (kostenlos in extra2)
# RequiredFaith = 5000 pro Kategorie

BLESS_COOLDOWN = 180  # 3 Minuten Cooldown wie im Original (extra2/logic.xml)
BLESS_DURATION = 180  # Sekunden wie lange der Bonus hÃƒÆ’Ã‚Â¤lt (aus extra2!)
BLESS_MOTIVATION_BONUS = 0.3  # +30% Motivation (aus extra2!)
BLESS_REQUIRED_FAITH = 5000  # BenÃƒÆ’Ã‚Â¶tigter Glaube pro Kategorie

# 5 Segen-Kategorien (aus extra2/logic.xml)
BLESS_CATEGORIES = {
    0: {
        "name": "Construction",
        "worker_types": ["Miner", "Farmer", "BrickMaker", "Sawmillworker", "Stonecutter", "TavernBarkeeper"],
        "description": "Bau-Arbeiter segnen"
    },
    1: {
        "name": "Research",
        "worker_types": ["Scholar", "Priest", "Engineer", "MasterBuilder"],
        "description": "Forschungs-Arbeiter segnen"
    },
    2: {
        "name": "Weapons",
        "worker_types": ["Smith", "Alchemist", "Smelter", "Gunsmith"],
        "description": "Waffen-Arbeiter segnen"
    },
    3: {
        "name": "Financial",
        "worker_types": ["Trader", "Treasurer"],
        "description": "Finanz-Arbeiter segnen"
    },
    4: {
        "name": "Canonisation",
        "worker_types": ["ALL"],  # Alle Worker
        "description": "Alle Arbeiter segnen (Heiligsprechung)"
    },
}

# Tech-Voraussetzungen fÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¼r Segen-Kategorien (aus T_BlessSettlers1-5)

# =============================================================================
# ALARM-MODUS (aus extra2/logic.xml)
# =============================================================================
# AlarmRechargeTime = 180000 ms (3 Minuten Cooldown)
# Worker gehen zu DefendableBuildings bei Alarm
ALARM_RECHARGE_TIME = 180  # Sekunden (3 Minuten) - AlarmRechargeTime=180000ms
ALARM_ACTIVE = False  # StandardmÃƒÆ’Ã‚Â¤ÃƒÆ’Ã…Â¸ig aus

# OvertimeRechargeTimeInMs = 240000 ms (4 Minuten Cooldown fÃƒÆ’Ã‚Â¼r ÃƒÆ’Ã…â€œberstunden)
OVERTIME_RECHARGE_TIME = 240  # Sekunden

# Unter diesem Durchschnitts-Motivationswert werden keine neuen Worker/Soldaten angezogen
# AverageMotivationVillageCenterLockThreshold = 0.3
VILLAGE_CENTER_LOCK_THRESHOLD = 0.3

# ForceToWorkPenalty = 0.2 - Motivations-Strafe wenn Worker zur Arbeit gezwungen wird
FORCE_TO_WORK_PENALTY = WORKER_FORCE_TO_WORK_PENALTY

# MotivationMillisecondsWithoutJob = 30000 - 30s bevor Worker wegen Joblosigkeit geht
MOTIVATION_MS_WITHOUT_JOB = 30000

# CompensationOnBuildingSale = 50% - RÃƒÆ’Ã‚Â¼ckerstattung beim Abriss
BUILDING_SALE_COMPENSATION = 0.5

# BuildingPlacementSnapDistance = 900 - Maximale Snap-Distanz bei Platzierung
BUILDING_SNAP_DISTANCE = 900

# =============================================================================
# GEBAEUDE-FOOTPRINTS (aus Entity-XMLs: Blocked1/Blocked2)
# =============================================================================
# Format: (width, height) in Game-Units (Blocked2 - Blocked1)
BUILDING_FOOTPRINTS = {
    # Kern-GebÃƒÆ’Ã‚Â¤ude
    "Hauptquartier": (1200, 1200),
    "Dorfzentrum": (1200, 1100),
    "Wohnhaus": (400, 500),
    "Bauernhof": (600, 1000),
    # Produktions-GebÃƒÆ’Ã‚Â¤ude
    "Hochschule": (1300, 1500),
    "SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle": (900, 1600),
    "SteinmetzhÃƒÆ’Ã‚Â¼tte": (800, 1000),
    "Schmiede": (900, 700),
    "LehmhÃƒÆ’Ã‚Â¼tte": (750, 1010),
    "AlchimistenhÃƒÆ’Ã‚Â¼tte": (800, 1400),
    "BÃƒÆ’Ã‚Â¼chsenmacherei": (1000, 1000),
    "KanongieÃƒÆ’Ã…Â¸erei": (1500, 1300),
    # Minen
    "Eisenmine": (920, 1070),
    "Steinmine": (1000, 1000),
    "Lehmmine": (1220, 970),
    "Schwefelmine": (920, 970),
    # MilitÃƒÆ’Ã‚Â¤r
    "Kaserne": (1400, 1400),
    "SchieÃƒÆ’Ã…Â¸platz": (1300, 1500),
    "Stall": (1600, 1800),
    "Turm": (600, 600),
    # Spezial
    "Bank": (900, 900),
    "Kloster": (1200, 1400),
    "Markt": (1200, 1200),
    "Taverne": (800, 1000),
    "Architektenstube": (600, 600),
    "BrÃƒÆ’Ã‚Â¼cke": (400, 1200),
    # Schmuck (Beautification)
    "PB_Beautification01": (300, 300),
    "PB_Beautification02": (500, 500),
    "PB_Beautification03": (300, 300),
    "PB_Beautification04": (300, 300),
    "PB_Beautification05": (300, 300),
    "PB_Beautification06": (300, 300),
    "PB_Beautification07": (300, 300),
    "PB_Beautification08": (300, 300),
    "PB_Beautification09": (300, 300),
    "PB_Beautification10": (300, 300),
    "PB_Beautification11": (300, 300),
    "PB_Beautification12": (300, 300),
}

# Worker-KapazitÃƒÆ’Ã‚Â¤t wird durch DORFZENTRUM bestimmt (VILLAGE_CENTER_CAPACITY)!

# =============================================================================
# KAPAZITÃƒÆ’Ã¢â‚¬Å¾TS-SYSTEM (aus XML-Analyse)
# =============================================================================

# DORFZENTRUM = Bestimmt maximale Anzahl Arbeiter/Bewohner!
# Dies ist das HARTE LIMIT fÃƒÆ’Ã‚Â¼r die BevÃƒÆ’Ã‚Â¶lkerung
VILLAGE_CENTER_CAPACITY = {
    "Dorfzentrum_1": 75,   # Level 1: max 75 Arbeiter (AttractableSettlers=75)
    "Dorfzentrum_2": 100,  # Level 2: max 100 Arbeiter (AttractableSettlers=100)
    "Dorfzentrum_3": 125,  # Level 3: max 125 Arbeiter (AttractableSettlers=125, KORRIGIERT von 150!)
}

# Wohnhaus = NUR fÃƒÆ’Ã‚Â¼r RUHEN (WorkTime +50%)
# Begrenzt wie viele Arbeiter GLEICHZEITIG ruhen kÃƒÆ’Ã‚Â¶nnen
# Arbeiter kÃƒÆ’Ã‚Â¶nnen auch OHNE Wohnhaus existieren (dann nur Camp +10%)
RESIDENCE_CAPACITY = {
    "Wohnhaus_1": 6,   # Level 1: 6 kÃƒÆ’Ã‚Â¶nnen gleichzeitig ruhen
    "Wohnhaus_2": 9,   # Level 2: 9 kÃƒÆ’Ã‚Â¶nnen gleichzeitig ruhen
    "Wohnhaus_3": 12,  # Level 3: 12 kÃƒÆ’Ã‚Â¶nnen gleichzeitig ruhen
}

# Bauernhof = NUR fÃƒÆ’Ã‚Â¼r ESSEN (WorkTime +70%)
# Begrenzt wie viele Arbeiter GLEICHZEITIG essen kÃƒÆ’Ã‚Â¶nnen
# Arbeiter kÃƒÆ’Ã‚Â¶nnen auch OHNE Bauernhof existieren (dann nur Camp +10%)
FARM_EAT_CAPACITY = {
    "Bauernhof_1": 8,   # Level 1: 8 kÃƒÆ’Ã‚Â¶nnen gleichzeitig essen
    "Bauernhof_2": 10,  # Level 2: 10 kÃƒÆ’Ã‚Â¶nnen gleichzeitig essen
    "Bauernhof_3": 12,  # Level 3: 12 kÃƒÆ’Ã‚Â¶nnen gleichzeitig essen
}

# Bauernhof max Workers (Farmer die dort arbeiten)
FARM_WORKER_CAPACITY = {
    "Bauernhof_1": 1,
    "Bauernhof_2": 2,
    "Bauernhof_3": 3,
}

# Camper-Range fÃƒÆ’Ã‚Â¼r Pausen (5000 Einheiten im Spiel)
CAMPER_RANGE = 5000

# Worker-Typen zu GebÃƒÆ’Ã‚Â¤ude-Mapping
WORKER_BUILDING_MAP = {
    "miner": ["Steinmine", "Lehmmine", "Eisenmine", "Schwefelmine"],
    "sawmill_worker": ["SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle"],
    "brickmaker": ["LehmhÃƒÆ’Ã‚Â¼tte"],  # ZiegelhÃƒÆ’Ã‚Â¼tte - verarbeitet Lehm
    "stonecutter": ["SteinmetzhÃƒÆ’Ã‚Â¼tte"],
    "smith": ["Schmiede"],
    "alchemist": ["AlchimistenhÃƒÆ’Ã‚Â¼tte"],
    "farmer": ["Bauernhof"],
}

HARVESTABLE_TREE_TYPES = {
    "XD_Fir1",
    "XD_Fir2",
    "XD_Fir3",
    "XD_Pine1",
    "XD_Pine2",
    "XD_Pine3",
    "XD_Tree1",
    "XD_Tree2",
    "XD_Tree3",
    "XD_Cypress1",
    "XD_Cypress2",
    "XD_Willow1",
    "XD_Willow2",
}

P1_X_MIN = 25000.0
P1_X_MAX = 51000.0
P1_Y_MIN = 0.0
P1_Y_MAX = 25500.0


# =============================================================================
# HILFSFUNKTIONEN
# =============================================================================

def get_base_building_name(building_name):
    if "_" in building_name and building_name.split("_")[-1].isdigit():
        return "_".join(building_name.split("_")[:-1])
    return building_name

def get_building_level(building_name):
    if "_" in building_name and building_name.split("_")[-1].isdigit():
        return int(building_name.split("_")[-1])
    return 1


def _is_harvestable_tree_type(tree_type: str) -> bool:
    return str(tree_type or "").strip() in HARVESTABLE_TREE_TYPES


def _get_expected_resource_tree_types() -> Set[str]:
    tree_summary = PLAYER_1_TREES_SUMMARY if isinstance(PLAYER_1_TREES_SUMMARY, dict) else {}
    tree_types = tree_summary.get("tree_types", {})
    if isinstance(tree_types, dict):
        expected = {str(name).strip() for name, count in tree_types.items() if int(count or 0) > 0}
        if expected:
            return expected
    return set(HARVESTABLE_TREE_TYPES)


def _extract_tree_xy(tree: Dict[str, Any]) -> Optional[Tuple[float, float]]:
    if not isinstance(tree, dict):
        return None

    if "x" in tree and "y" in tree:
        try:
            return float(tree.get("x", 0.0)), float(tree.get("y", 0.0))
        except (TypeError, ValueError):
            return None

    position = tree.get("position")
    if isinstance(position, dict) and "x" in position and "y" in position:
        try:
            return float(position.get("x", 0.0)), float(position.get("y", 0.0))
        except (TypeError, ValueError):
            return None
    return None


def _is_player1_quadrant_xy(x: float, y: float) -> bool:
    return P1_X_MIN < x < P1_X_MAX and P1_Y_MIN < y < P1_Y_MAX


def _normalize_tree_record(tree: Dict[str, Any], tree_type: str, amount_default: int = 0) -> Optional[Dict[str, Any]]:
    coords = _extract_tree_xy(tree)
    if coords is None:
        return None

    x, y = coords
    normalized: Dict[str, Any] = {
        "x": x,
        "y": y,
        "type": str(tree_type or "").strip(),
    }

    try:
        amount = int(tree.get("amount", amount_default) or amount_default)
    except (TypeError, ValueError):
        amount = amount_default
    if amount > 0:
        normalized["amount"] = amount

    if "distance_to_hq" in tree:
        try:
            normalized["distance_to_hq"] = float(tree.get("distance_to_hq", 0.0))
        except (TypeError, ValueError):
            pass

    return normalized


def _filter_harvestable_trees(tree_list, allowed_types: Optional[Set[str]] = None, require_positive_amount: bool = False):
    allowed = {str(t).strip() for t in (allowed_types or HARVESTABLE_TREE_TYPES)}
    filtered = []
    for tree in tree_list or []:
        if not isinstance(tree, dict):
            continue
        tree_type = str(tree.get("type", "")).strip()
        if tree_type not in allowed:
            continue
        if require_positive_amount:
            try:
                amount = int(tree.get("amount", 0) or 0)
            except (TypeError, ValueError):
                amount = 0
            if amount <= 0:
                continue

        normalized = _normalize_tree_record(tree, tree_type)
        if normalized is not None:
            filtered.append(normalized)
    return filtered


def _load_map_data_resource_trees(base_dir: str) -> List[Dict[str, Any]]:
    expected_types = _get_expected_resource_tree_types()
    if not expected_types:
        return []

    map_data_candidates = []
    if base_dir:
        map_data_candidates.append(os.path.join(base_dir, "config", "wintersturm_map_data.json"))
    map_data_candidates.append(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "wintersturm_map_data.json")
    )

    tree_summary = PLAYER_1_TREES_SUMMARY if isinstance(PLAYER_1_TREES_SUMMARY, dict) else {}
    wood_per_tree = int(tree_summary.get("wood_per_tree", 75) or 75)

    for map_data_file in map_data_candidates:
        if not map_data_file or not os.path.exists(map_data_file):
            continue
        try:
            with open(map_data_file, "r", encoding="utf-8") as f:
                map_data = json.load(f)
        except Exception:
            continue

        trees = map_data.get("trees", [])
        result = []
        for tree in trees:
            if not isinstance(tree, dict):
                continue
            tree_type = str(tree.get("type", "")).strip()
            if tree_type not in expected_types:
                continue

            coords = _extract_tree_xy(tree)
            if coords is None:
                continue
            x, y = coords
            if not _is_player1_quadrant_xy(x, y):
                continue

            normalized = _normalize_tree_record(tree, tree_type, amount_default=wood_per_tree)
            if normalized is not None:
                result.append(normalized)

        if result:
            return result
    return []


def _select_resource_trees(resources_data: Dict[str, Any], base_dir: str) -> List[Dict[str, Any]]:
    expected_types = _get_expected_resource_tree_types()
    raw_cached_trees = resources_data.get(
        "trees_all",
        resources_data.get("trees_nearest_50", []),
    )

    # Primary source: runtime exports with positive amounts.
    runtime_trees = _filter_harvestable_trees(
        raw_cached_trees,
        allowed_types=expected_types,
        require_positive_amount=True,
    )
    if runtime_trees:
        return runtime_trees

    # Canonical fallback: static map extract (player-1, resource tree types only).
    map_data_trees = _load_map_data_resource_trees(base_dir)
    if map_data_trees:
        return map_data_trees

    # Legacy fallback: known tree types without amount information.
    typed_trees = _filter_harvestable_trees(raw_cached_trees, allowed_types=expected_types)
    if typed_trees:
        return typed_trees

    fallback_trees = _filter_harvestable_trees(
        PLAYER_1_TREES_NEAREST,
        allowed_types=expected_types,
    )
    if fallback_trees:
        return fallback_trees
    return list(PLAYER_1_TREES_NEAREST)


DEFAULT_REWARD_PROFILE = {
    # Dense shaping on state deltas (off by default to preserve sparse behavior).
    "step_delta_potential_bonus": 0.0,
    # Event bonus when cumulative resource potential crosses the next whole-unit threshold.
    "step_new_resource_potential_unit_bonus": 0.0,
    # Optional single progress channel (weighted mix of dependency/research/construction).
    "step_delta_progress_bonus": 0.0,
    "step_progress_mix_dependency": 1.0,
    "step_progress_mix_research": 1.0,
    "step_progress_mix_construction": 1.0,
    "step_delta_dependency_bonus": 0.0,
    "step_delta_research_bonus": 0.0,
    "step_delta_construction_bonus": 0.0,
    # Reward per newly reached taxable worker (episode high-water mark).
    "step_worker_growth_bonus": 0.0,
    "step_unlock_recruitable_bonus": 0.0,
    "step_time_penalty": 0.0,
    # Event rewards for serf economy growth (episode high-water marks).
    "action_buy_serf_growth_bonus": 0.0,
    # One-time reward for assigning newly bought/spawned unassigned serfs from FREE.
    "action_assign_spawned_serf_bonus": 0.0,
    "step_potential_use_cumulative_earnings": 1.0,
    "step_potential_include_start_resources": 0.0,
    # Which Scharfschuetzen tier to use for step potential conversion (1=min-tier fallback, 2=T2).
    "step_potential_scharf_tier": 1.0,
    "step_delta_positive_only": 1.0,
}


def _resolve_reward_profile(overrides: Optional[Dict[str, float]] = None) -> Dict[str, float]:
    profile = dict(DEFAULT_REWARD_PROFILE)
    if not overrides:
        return profile
    for key, value in overrides.items():
        if key not in profile or value is None:
            continue
        try:
            profile[key] = float(value)
        except (TypeError, ValueError):
            continue
    return profile


# =============================================================================
# ENVIRONMENT KLASSE - KOMPLETTE SIEDLER 5 SIMULATION
# =============================================================================

class SiedlerScharfschuetzenEnv(gym.Env):
    """
    VollstÃƒÆ’Ã‚Â¤ndige Siedler 5 Trainingsumgebung mit ALLEN Spielaktionen
    """

    metadata = {"render_modes": ["human", "ansi"]}

    def __init__(
        self,
        player_id: int = 1,
        render_mode: str = None,
        use_spatial_obs: bool = True,
        spatial_size: int = 128,
        reward_profile: Optional[Dict[str, float]] = None,
    ):
        super().__init__()

        self.player_id = player_id
        self.render_mode = render_mode
        self.use_spatial_obs = bool(use_spatial_obs)
        self.spatial_size = int(spatial_size)
        self.sim_mode = _resolve_sim_mode_from_env()
        disable_runtime_pathing_raw = os.environ.get("SIEDLER_DISABLE_RUNTIME_PATHING")
        if disable_runtime_pathing_raw is None:
            self.disable_runtime_pathing = self.sim_mode == "fast_train"
        else:
            self.disable_runtime_pathing = _env_truthy(disable_runtime_pathing_raw)
        self.reward_profile = _resolve_reward_profile(reward_profile)
        self._start_scharf_resource_potential = 0.0
        self._start_scharf_dependency_progress = 0.0
        self._start_scharf_recruitable = False
        self._last_scharf_resource_potential = 0.0
        self._last_scharf_dependency_progress = 0.0
        self._last_step_potential_metric = 0.0
        self._last_step_potential_units = 0
        self._last_step_unlock_progress = 0.0
        self._best_step_taxable_workers = 0.0
        self._last_scharf_research_progress = 0.0
        self._last_scharf_construction_progress = 0.0
        self._last_scharf_recruitable = False
        self._terminal_start_total_taler = 0.0
        self._terminal_start_total_schwefel = 0.0
        self._terminal_prev_total_taler = 0.0
        self._terminal_prev_total_schwefel = 0.0
        self._terminal_cumulative_taler_earned = 0.0
        self._terminal_cumulative_schwefel_earned = 0.0
        self._best_total_leibeigene = 0
        self._pending_spawned_unassigned_serfs = 0
        self._scharf_required_buildings, self._scharf_required_techs = self._get_scharf_requirements()

        # GebÃƒÆ’Ã‚Â¤ude-Listen fÃƒÆ’Ã‚Â¼r Actions
        self.buildable_buildings = [b for b in buildings_db.keys() if get_building_level(b) == 1]
        self.upgradeable_buildings = [b for b in buildings_db.keys() if buildings_db[b].get("upgrade_to")]
        self.demolishable_buildings = [b for b in buildings_db.keys() if "Hauptquartier" not in b]
        self.tech_list = list(technologies.keys())
        self.soldier_types = list(soldiers_db.keys())

        # Action Space berechnen
        self.n_build_actions = len(self.buildable_buildings)
        self.n_upgrade_actions = len(self.upgradeable_buildings)
        self.n_tech_actions = len(self.tech_list)
        self.n_recruit_actions = len(self.soldier_types)

        # =====================================================================
        # RESSOURCEN-ACTIONS (HYBRID: BÃƒÆ’Ã‚Â¤ume einzeln, Vorkommen/Minen kategorie-basiert)
        # =====================================================================

        # =================================================================
        # VEREINFACHTES BATCH-SYSTEM (ohne Serf-IDs)
        # Agent wÃƒÆ’Ã‚Â¤hlt: WAS (Kategorie) + WIEVIELE (1, 3, 5)
        # System wÃƒÆ’Ã‚Â¤hlt automatisch die beste Position
        # =================================================================

        # Batch-GrÃƒÆ’Ã‚Â¶ÃƒÆ’Ã…Â¸en fÃƒÆ’Ã‚Â¼r alle Ressourcen-Zuweisungen
        self.resource_batch_sizes = [1, 3, 5]

        # BÃƒÆ’Ã¢â‚¬Å¾UME: ZONEN-basierte Zuweisung fÃƒÆ’Ã‚Â¼r strategische Bauplatz-Schaffung
        # Jede Zone muss fÃƒÆ’Ã‚Â¼r bestimmte Raffinerie-GebÃƒÆ’Ã‚Â¤ude gerodet werden
        self.resource_trees = list(PLAYER_1_TREES_NEAREST)  # Fallback fÃƒÆ’Ã‚Â¼r generische BÃƒÆ’Ã‚Â¤ume
        self.wood_zone_names = list(WOOD_ZONES.keys())  # 6 Zonen: HQ_Bereich, Schwefelmine, Lehmmine, Steinmine, Dorfzentrum, Eisenmine

        # VORKOMMEN (Deposits): 4 Kategorien mit Batch
        # Serfs kÃƒÆ’Ã‚Â¶nnen hier sammeln SOLANGE keine Mine dort gebaut wurde
        self.deposit_category_names = ["Eisen", "Stein", "Lehm", "Schwefel"]

        # STOLLEN (Shafts): 4 Kategorien mit Batch - Serfs kÃƒÆ’Ã‚Â¶nnen IMMER hier sammeln
        # (XD_Iron1, XD_Stone1, etc. - 400 Ressourcen pro Stollen, keine Mine baubbar)
        self.shaft_category_names = ["Eisen", "Stein", "Lehm", "Schwefel"]

        # LEGACY: Mine-Kategorien (DEAKTIVIERT - Serfs arbeiten nicht an gebauten Minen!)
        self.mine_category_names = ["Eisenmine", "Steinmine", "Lehmmine", "Schwefelmine"]

        # Ressourcen-Actions:
        # - Holz-Zonen: 6 Zonen ÃƒÆ’Ã¢â‚¬â€ 6 (assign/recall ÃƒÆ’Ã¢â‚¬â€ batch) = 36 Actions
        # - Vorkommen: 4 ÃƒÆ’Ã¢â‚¬â€ 6 (assign/recall ÃƒÆ’Ã¢â‚¬â€ batch) = 24 Actions
        # - Stollen: 4 ÃƒÆ’Ã¢â‚¬â€ 6 (assign/recall ÃƒÆ’Ã¢â‚¬â€ batch) = 24 Actions
        # Total: 84 Actions (statt 54)
        n_batch = len(self.resource_batch_sizes)
        self.n_wood_zone_batch_actions = len(self.wood_zone_names) * n_batch * 2  # 36 (6 Zonen ÃƒÆ’Ã¢â‚¬â€ 6)
        self.n_tree_batch_actions = self.n_wood_zone_batch_actions  # Legacy alias
        self.n_deposit_batch_actions = len(self.deposit_category_names) * n_batch * 2  # 24
        self.n_shaft_batch_actions = len(self.shaft_category_names) * n_batch * 2  # 24 (NEU: Stollen statt Mine)
        self.n_mine_batch_actions = self.n_shaft_batch_actions  # Legacy alias
        self.n_resource_position_actions = (
            self.n_wood_zone_batch_actions +  # Holz-Zonen (36)
            self.n_deposit_batch_actions +    # Vorkommen (24)
            self.n_shaft_batch_actions        # Stollen (24)
        )  # 84 Actions

        # =================================================================
        # BATCH-ACTIONS FÃƒÆ’Ã…â€œR GEBÃƒÆ’Ã¢â‚¬Å¾UDE
        # Agent kann 1, 3, oder 5 GebÃƒÆ’Ã‚Â¤ude auf einmal bauen
        # =================================================================
        self.build_batch_sizes = [1, 3, 5]
        # GebÃƒÆ’Ã‚Â¤ude-Batch: 28 GebÃƒÆ’Ã‚Â¤ude ÃƒÆ’Ã¢â‚¬â€ 3 Batch-GrÃƒÆ’Ã‚Â¶ÃƒÆ’Ã…Â¸en = 84 Actions
        # ERSETZT die alten n_build_actions (28)
        self.n_build_batch_actions = len(self.buildable_buildings) * len(self.build_batch_sizes)

        # NEUE ACTIONS:
        # Batch-Actions fÃƒÆ’Ã‚Â¼r Leibeigene: 1x, 3x, 5x kaufen + 1x, 3x, 5x entlassen
        self.serf_batch_sizes = [1, 3, 5]
        self.n_serf_actions = len(self.serf_batch_sizes) * 2  # 6 Actions (3 kaufen + 3 entlassen)

        # Batch-Actions fÃƒÆ’Ã‚Â¼r ScharfschÃƒÆ’Ã‚Â¼tzen-Rekrutierung: 3x, 5x (1x ist bereits in n_recruit_actions)
        # FÃƒÆ’Ã‚Â¼r beide ScharfschÃƒÆ’Ã‚Â¼tzen-Typen: ScharfschÃƒÆ’Ã‚Â¼tzen (Level 1) und ScharfschÃƒÆ’Ã‚Â¼tzen_2 (Level 2)
        self.scharfschuetzen_batch_sizes = [3, 5]  # 1x ist bereits standard
        self.scharfschuetzen_types = ["ScharfschÃƒÆ’Ã‚Â¼tzen", "ScharfschÃƒÆ’Ã‚Â¼tzen_2"]
        self.n_batch_recruit_actions = len(self.scharfschuetzen_batch_sizes) * len(self.scharfschuetzen_types)  # 4 Actions

        self.n_demolish_actions = len(self.demolishable_buildings)  # Alle GebÃƒÆ’Ã‚Â¤ude (auÃƒÆ’Ã…Â¸er HQ) kÃƒÆ’Ã‚Â¶nnen abgerissen werden
        self.n_bless_actions = len(BLESS_CATEGORIES)  # 5 Segen-Kategorien (aus extra2)
        self.n_tax_actions = len(TAX_LEVELS)  # Steuerstufen (0-4)
        self.n_alarm_actions = 2  # Alarm AN / Alarm AUS

        # NEU: Bau-Serfs zuweisen/zurÃƒÆ’Ã‚Â¼ckrufen (1x, 3x, 5x fÃƒÆ’Ã‚Â¼r beide)
        self.build_serf_batch_sizes = [1, 3, 5]
        self.n_build_serf_actions = len(self.build_serf_batch_sizes) * 2  # 6 Actions

        # TOTAL ACTIONS (mit Batch-Build statt einzeln):
        # 1 (wait) + 84 (build batch) + 35 (upgrade) + 50 (tech) + 22 (recruit) +
        # 54 (resource batch) + 6 (serf) + 4 (batch recruit) + 28 (demolish) +
        # 5 (bless) + 5 (tax) + 2 (alarm) + 6 (build serf) = 302 Actions
        self.total_actions = (1 + self.n_build_batch_actions + self.n_upgrade_actions +
                             self.n_tech_actions + self.n_recruit_actions +
                             self.n_resource_position_actions +
                             self.n_serf_actions + self.n_batch_recruit_actions + self.n_demolish_actions +
                             self.n_bless_actions + self.n_tax_actions + self.n_alarm_actions +
                             self.n_build_serf_actions)

        # Legacy action space (wird durch Multi-Step action_space property ueberschrieben)
        self._legacy_action_space = gym.spaces.Discrete(self.total_actions)

        # Action Offsets (mit Batch-Build)
        self.offset_build_batch = 1  # GebÃƒÆ’Ã‚Â¤ude-Batch-Bau
        self.offset_upgrade = self.offset_build_batch + self.n_build_batch_actions
        self.offset_tech = self.offset_upgrade + self.n_upgrade_actions
        self.offset_recruit = self.offset_tech + self.n_tech_actions
        # Ressourcen-Batch-Actions
        self.offset_resource_batch = self.offset_recruit + self.n_recruit_actions
        self.offset_serf = self.offset_resource_batch + self.n_resource_position_actions
        self.offset_batch_recruit = self.offset_serf + self.n_serf_actions
        self.offset_demolish = self.offset_batch_recruit + self.n_batch_recruit_actions
        self.offset_bless = self.offset_demolish + self.n_demolish_actions
        self.offset_tax = self.offset_bless + self.n_bless_actions
        self.offset_alarm = self.offset_tax + self.n_tax_actions
        self.offset_build_serf = self.offset_alarm + self.n_alarm_actions  # NEU

        # Legacy-KompatibilitÃƒÆ’Ã‚Â¤t (fÃƒÆ’Ã‚Â¼r alten Code der offset_build verwendet)
        self.offset_build = self.offset_build_batch
        self.offset_resource_pos = self.offset_resource_batch

        # =================================================================
        # MULTI-STEP ACTION SYSTEM (Phase 4.2-4.4)
        # =================================================================
        self.current_phase = ActionPhase.MAIN
        self.current_flow = None
        self.flow_step = 0
        self.pending_selections = {}

        # Technologien nach Forschungs-GebÃƒÆ’Ã‚Â¤ude gruppieren
        import re
        self.tech_by_building = {b: [] for b in RESEARCH_BUILDINGS}
        for tech_name in self.tech_list:
            tech_info = technologies[tech_name]
            targets = tech_info.get("research_buildings")
            if targets:
                for target in targets:
                    base = re.sub(r'_\d+$', '', target)
                    if base in self.tech_by_building:
                        self.tech_by_building[base].append(tech_name)
                    else:
                        self.tech_by_building["Hochschule"].append(tech_name)
                continue

            req = tech_info.get("research_building") or tech_info.get("requires_building", "Hochschule_1")
            base = re.sub(r'_\d+$', '', req)
            if base in self.tech_by_building:
                self.tech_by_building[base].append(tech_name)
            else:
                self.tech_by_building["Hochschule"].append(tech_name)

        # Action Spaces pro Phase
        self.building_selection_size = max(len(self.upgradeable_buildings), len(self.demolishable_buildings))
        tree_specific_size = int(PLAYER_1_TREES_SUMMARY.get("total_trees", len(self.resource_trees)))
        self.source_specific_size = max(MAX_SPECIFIC_OPTIONS, tree_specific_size)
        self.target_specific_size = max(MAX_SPECIFIC_OPTIONS, len(self.buildable_buildings), tree_specific_size)
        self.action_spaces = {
            ActionPhase.MAIN: spaces.Discrete(len(MAIN_ACTIONS)),  # 11 (build entfernt)
            ActionPhase.BUILDING: spaces.Discrete(self.building_selection_size),
            ActionPhase.POSITION_GROUP: spaces.Discrete(POSITION_GROUP_COUNT),
            ActionPhase.POSITION_INDEX: spaces.Discrete(POSITION_GROUP_SIZE),
            ActionPhase.TECH_BUILDING: spaces.Discrete(len(RESEARCH_BUILDINGS)),  # 13 Forschungs-GebÃƒÆ’Ã‚Â¤ude
            ActionPhase.TECH: spaces.Discrete(MAX_TECHS_PER_BUILDING),  # max 17 (Hochschule)
            ActionPhase.SOLDIER: spaces.Discrete(len(self.soldier_types)),
            ActionPhase.QUANTITY: spaces.Discrete(6),
            ActionPhase.SOURCE_CATEGORY: spaces.Discrete(len(SOURCE_CATEGORIES)),  # 7
            ActionPhase.SOURCE_SPECIFIC: spaces.Discrete(self.source_specific_size),
            ActionPhase.TARGET_CATEGORY: spaces.Discrete(len(TARGET_CATEGORIES)),  # 8
            ActionPhase.TARGET_SPECIFIC: spaces.Discrete(self.target_specific_size),
            ActionPhase.CATEGORY: spaces.Discrete(len(BLESS_CATEGORIES)),
            ActionPhase.TAX_LEVEL: spaces.Discrete(len(TAX_LEVELS)),
            ActionPhase.ON_OFF: spaces.Discrete(2),
        }
        self.phase_list = list(ActionPhase)
        self.phase_index = {phase: idx for idx, phase in enumerate(self.phase_list)}
        self.phase_dim = len(self.phase_list)
        self.max_action_size = max(space.n for space in self.action_spaces.values())

        # Gymnasium-kompatible action_space Property (fixe GrÃƒÆ’Ã‚Â¶ÃƒÆ’Ã…Â¸e)
        self.action_space = gym.spaces.Discrete(self.max_action_size)

        # Serf Areas tracking
        self.serf_areas = {area: {"count": 0} for area in SerfArea}
        self.serf_areas[SerfArea.FREE]["count"] = 30  # Start-Leibeigene

        # Tech Effects (wird in reset() zurueckgesetzt)
        self.active_tech_effects = {}

        # Observation Space (ERWEITERT mit WorkTime-System)
        n_resource_obs = len(RESOURCE_NAMES)
        n_worker_obs = len(RESOURCE_MAP) + 2
        n_building_obs = len(self.buildable_buildings) * 2
        n_upgrade_obs = len(self.upgradeable_buildings)
        n_tech_obs = len(self.tech_list) * 2
        n_research_building_obs = len(RESEARCH_BUILDINGS)
        n_soldier_obs = len(self.soldier_types)
        n_time_obs = 2
        # Produktionsraten pro Ressource + effektive Taler-Rate (inkl. Handels-Multiplikator)
        n_production_obs = len(RESOURCE_MAP) + 1
        n_phase_obs = self.phase_dim
        # Queue-/Kapazitaets-Stats + Bauplaetze + Motivation + Walkable-Stats
        # + zielgerichtete Scharfschuetzen-/Ressourcen-Features
        n_macro_obs = 31

        # NEU: WorkTime-System Observations
        n_worktime_obs = 12  # avg_work_time, exhausted_ratio, eating, resting, working,
                             # walking, farm_capacity, farm_util, res_capacity, res_util,
                             # overall_efficiency, serf_count

        # NEU: Observations fÃƒÆ’Ã‚Â¼r neue Actions
        # tax_level, alarm_active, alarm_cooldown, faith
        # + 5x bless_cooldown (pro Kategorie) + 5x bless_active (pro Kategorie)
        n_new_action_obs = 4 + len(BLESS_CATEGORIES) * 2  # 4 + 10 = 14

        total_obs = (n_resource_obs + n_worker_obs + n_building_obs + n_upgrade_obs +
                    n_tech_obs + n_research_building_obs + n_soldier_obs + n_time_obs +
                    n_production_obs + n_worktime_obs + n_new_action_obs + n_macro_obs +
                    n_phase_obs)

        self.vector_obs_size = total_obs
        self.vector_observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=(total_obs,), dtype=np.float32
        )

        # Baupositionen laden
        self.building_zones = get_building_positions_for_player(player_id)
        self.mine_positions = PLAYER_1_MINE_POSITIONS if player_id == 1 else {}

        # =====================================================================
        # PERFORMANCE: Map-Daten einmal laden und cachen (nicht bei jedem Reset!)
        # =====================================================================
        hq_data = PLAYER_HQ_POSITIONS.get(player_id, {"x": 0, "y": 0})
        self.hq_position = (hq_data["x"], hq_data["y"])

        # Numpy-Daten einmal laden und cachen
        base_dir = os.environ.get(
            "SIEDLER_DATA_DIR",
            os.path.dirname(os.path.abspath(__file__)),
        )
        # Bevorzugt: native 515-Grid (player1_walkable_515.npy) aus Map-Extract
        walkable_candidates = []
        if MAP_EXTRACT_DIR:
            walkable_candidates.append(os.path.join(str(MAP_EXTRACT_DIR), "player1_walkable_515.npy"))
            walkable_candidates.append(os.path.join(str(MAP_EXTRACT_DIR), "player1_walkable.npy"))
        walkable_candidates.append(os.path.join(base_dir, "player1_walkable_515.npy"))
        walkable_candidates.append(os.path.join(base_dir, "player1_walkable.npy"))

        walkable_file = next(
            (p for p in walkable_candidates if p and os.path.exists(p)),
            walkable_candidates[-1],
        )
        resources_file = os.path.join(base_dir, "player1_resources.json")

        self._cached_walkable = np.load(walkable_file)
        self._cached_walkable_file = walkable_file

        # Optional: Low-Res Terrain Layer (131x131) aus Map-Extract
        self._cached_lowres_terrain = None
        lowres_candidates = []
        if MAP_EXTRACT_DIR:
            lowres_candidates.append(os.path.join(str(MAP_EXTRACT_DIR), "terrain_lowres_131.npy"))
        lowres_candidates.append(os.path.join(base_dir, "terrain_lowres_131.npy"))
        for p in lowres_candidates:
            if p and os.path.exists(p):
                self._cached_lowres_terrain = np.load(p)
                break

        with open(resources_file, 'r') as f:
            self._cached_resources = json.load(f)

        # PERFORMANCE: VollstÃƒÆ’Ã‚Â¤ndigen MapManager mit BÃƒÆ’Ã‚Â¤umen einmal aufbauen und cachen
        # Grid-Skalierung anhand der geladenen Walkable-Map setzen (Player-Quadrant)
        grid_h, grid_w = self._cached_walkable.shape
        world_w = MAP_SIZE[0] / 2
        world_h = MAP_SIZE[1] / 2
        scale_x = world_w / grid_w
        scale_y = world_h / grid_h
        pathfinding.set_grid_scale(scale_x, scale_y)

        self._cached_map_manager = MapManager(width=grid_w, height=grid_h)
        self._cached_map_manager.grid.load_terrain_from_array(self._cached_walkable)
        cached_trees = _select_resource_trees(self._cached_resources, base_dir)
        self.resource_trees = list(cached_trees)
        self._cached_map_manager._load_trees_from_data(cached_trees)

        # Cache die Grid-Arrays fÃƒÆ’Ã‚Â¼r schnelles Reset
        self._cached_terrain_base = self._cached_map_manager.grid.terrain_base.copy()
        self._cached_trees_layer = self._cached_map_manager.grid.trees.copy()
        self._cached_tree_positions = dict(self._cached_map_manager.grid.tree_positions)
        self._cached_tree_world_positions = dict(self._cached_map_manager.tree_world_positions)

        # PERFORMANCE: Tree-ID Mapping einmal berechnen (war 95% der Reset-Zeit!)
        self._cached_tree_id_mapping = {}
        trees_list = list(PLAYER_1_TREES_NEAREST)
        for i, tree in enumerate(trees_list):
            nearest = self._cached_map_manager.get_nearest_tree(tree["x"], tree["y"])
            if nearest:
                self._cached_tree_id_mapping[i] = nearest[0]

        print(f"Walkable Grid geladen: {self._cached_walkable.shape}")
        print(f"BÃƒÆ’Ã‚Â¤ume geladen: {len(cached_trees)} (gecached, harvestable)")

        # Spatial Observation Setup (optional)
        self._grid_height, self._grid_width = self._cached_walkable.shape
        self._spatial_channels = []
        self._spatial_static_layers = {}
        if self.use_spatial_obs:
            self._init_spatial_layers()
            spatial_shape = (len(self._spatial_channels), self.spatial_size, self.spatial_size)
            self.observation_space = spaces.Dict({
                "vector": self.vector_observation_space,
                "spatial": spaces.Box(low=0.0, high=1.0, shape=spatial_shape, dtype=np.float32),
            })
        else:
            self.observation_space = self.vector_observation_space

        # Initial-Ressourcen-Summen fuer ratio-features im Observation-Space.
        self._deposit_initial_totals = {}
        self._shaft_initial_totals = {}

        self.reset()

    def _build_dynamic_wood_zone_categories(self):
        """Erstellt Holz-Zonen mit allen verfuegbaren Kartenbaeumen (statt fixer Teilmenge)."""
        zone_categories = {}
        zone_centers = {}

        for zone_name, zone_data in WOOD_ZONES.items():
            center_raw = zone_data.get("center", {"x": self.hq_position[0], "y": self.hq_position[1]})
            if isinstance(center_raw, dict):
                cx = float(center_raw.get("x", self.hq_position[0]))
                cy = float(center_raw.get("y", self.hq_position[1]))
            elif isinstance(center_raw, (list, tuple)) and len(center_raw) >= 2:
                cx = float(center_raw[0])
                cy = float(center_raw[1])
            else:
                cx = float(self.hq_position[0])
                cy = float(self.hq_position[1])
            center = {"x": cx, "y": cy}
            zone_centers[zone_name] = center
            zone_categories[zone_name] = {
                "center": center,
                "radius": zone_data.get("radius", 0),
                "raffinerie": zone_data.get("raffinerie", ""),
                "trees": [],
                "serfs_assigned": 0,
                "total_trees": 0,
            }

        trees_all = list(self.resource_trees)
        if not trees_all:
            for zone_name, zone_data in WOOD_ZONES.items():
                zone_trees = []
                for tree in zone_data.get("trees", []):
                    zone_trees.append(
                        {
                            "x": float(tree.get("x", 0.0)),
                            "y": float(tree.get("y", 0.0)),
                            "dist": float(tree.get("dist", 0.0)),
                            "resource_remaining": 75,
                            "serfs_assigned": 0,
                        }
                    )
                zone_categories[zone_name]["trees"] = zone_trees
                zone_categories[zone_name]["total_trees"] = len(zone_trees)
            return zone_categories

        for tree in trees_all:
            tx = float(tree.get("x", 0.0))
            ty = float(tree.get("y", 0.0))
            amount = max(0, int(tree.get("amount", 75)))

            best_zone = None
            best_dist_sq = float("inf")
            for zone_name, center in zone_centers.items():
                dx = tx - float(center.get("x", 0.0))
                dy = ty - float(center.get("y", 0.0))
                dist_sq = dx * dx + dy * dy
                if dist_sq < best_dist_sq:
                    best_dist_sq = dist_sq
                    best_zone = zone_name

            if best_zone is None:
                continue

            zone_categories[best_zone]["trees"].append(
                {
                    "x": tx,
                    "y": ty,
                    "dist": float(best_dist_sq ** 0.5),
                    "resource_remaining": amount,
                    "serfs_assigned": 0,
                }
            )

        for zone_name, zone in zone_categories.items():
            zone["trees"].sort(key=lambda t: t["dist"])
            zone["total_trees"] = len(zone["trees"])

        return self._split_wood_zone_categories(zone_categories)

    def _split_wood_zone_categories(self, zone_categories: Dict[str, dict]) -> Dict[str, dict]:
        """Teilt grosse Holz-Zonen in mehrere Action-Zonen fuer feinere Serf-Steuerung."""
        expanded = {}
        for zone_name, zone in zone_categories.items():
            trees = list(zone.get("trees", []))
            if not trees:
                expanded[zone_name] = dict(zone)
                continue

            chunk_count = 1
            if len(trees) > 48:
                chunk_count = 3
            elif len(trees) > 18:
                chunk_count = 2

            chunk_size = max(1, int(np.ceil(len(trees) / float(chunk_count))))
            for idx in range(chunk_count):
                chunk = trees[idx * chunk_size:(idx + 1) * chunk_size]
                if not chunk:
                    continue
                if chunk_count == 1:
                    sub_name = zone_name
                else:
                    sub_name = f"{zone_name}_{idx + 1}"
                expanded[sub_name] = {
                    "center": dict(zone.get("center", {})),
                    "radius": zone.get("radius", 0),
                    "raffinerie": zone.get("raffinerie", ""),
                    "trees": chunk,
                    "serfs_assigned": 0,
                    "total_trees": len(chunk),
                    "parent_zone": zone_name,
                }

        return expanded

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.resources = dict(START_RESOURCES)
        # Strict XML: Startressourcen als Rohstoffe behandeln
        for refined, raw in REFINED_TO_RAW.items():
            amount = self.resources.get(refined, 0)
            if amount:
                self.resources[raw] = self.resources.get(raw, 0) + amount
                self.resources[refined] = 0
        # Rohstoffe initialisieren (Raw-Resources)
        for raw_name in RESOURCE_RAW:
            self.resources.setdefault(raw_name, 0)
        self.resources.setdefault(RESOURCE_GOLD_ROH, 0)
        self.total_leibeigene = 30
        # Worker-KapazitÃƒÆ’Ã‚Â¤t wird durch WohnhÃƒÆ’Ã‚Â¤user bestimmt, nicht HQ
        self.free_leibeigene = self.total_leibeigene
        self.resource_workers = {r: 0 for r in RESOURCE_MAP}

        # Multi-Step System zuruecksetzen
        self.current_phase = ActionPhase.MAIN
        self.current_flow = None
        self.flow_step = 0
        self.pending_selections = {}
        self.serf_areas = {area: {"count": 0} for area in SerfArea}
        self.serf_areas[SerfArea.FREE]["count"] = self.total_leibeigene


        self.buildings = {b: 0 for b in buildings_db.keys()}
        self.buildings["Hauptquartier_1"] = 1

        self.construction_queue = []  # Legacy: [(building, remaining_time, position)]
        self.upgrade_queue = []
        self.upgrading_positions = set()
        self.current_researches = []
        self.researching_set: set = set()  # Maintained set fuer O(1) Lookup in _get_observation
        self.recruit_queue = []

        # NEU: Realistisches Bau-System mit Leibeigenen-Zuweisung
        # Format: [{
        #   "building": str,           # GebÃƒÆ’Ã‚Â¤ude-Name
        #   "position": (x, y),        # Bauplatz-Position
        #   "total_time": float,       # Basis-Bauzeit
        #   "remaining_work": float,   # Verbleibende Arbeit
        #   "serfs_assigned": int,     # Anzahl zugewiesener Leibeigener
        #   "site_id": int,            # Eindeutige ID
        # }]
        self.construction_sites = []
        self.next_site_id = 0

        # Serf-Tracking (vereinfacht - keine IDs mehr nÃƒÆ’Ã‚Â¶tig)

        self.researched_techs = set()
        # Auto-Forschung (z.B. GT_Beautification) direkt setzen
        for tech_name, tech_info in technologies.items():
            if tech_info.get("auto_research"):
                self.researched_techs.add(tech_name)
        self.active_tech_effects = {}  # NEU: Technologie-Effekte (aus GEPLANTE_AENDERUNGEN.md)
        if self.researched_techs:
            self._apply_technology_effects()
        self.soldiers = {s: 0 for s in self.soldier_types}
        self.scharfschuetzen = 0

        self.current_time = 0
        self.max_time = TOTAL_SIM_TIME

        self.available_positions = list(self.building_zones["zone_a_immediate"])
        self.zone_b_positions = list(self.building_zones.get("zone_b_after_logging", []))
        self.used_positions = []
        self.building_position_map = {}  # "building_N" -> position dict
        self.building_grid_ids = {}  # "building_N" -> WalkableGrid building_id
        self.building_runtime = {}  # "building_N" -> runtime data (workers/mine/refiner)
        self._build_check_cache_time = None
        self._build_check_cache = {}
        self._build_batch_cache = {}
        self._research_check_cache_time = None
        self._research_check_cache = {}
        self._research_any_cache = None
        self._obs_cache_time = None
        self._obs_cache_base = None
        self._spatial_cache_time = None
        self._spatial_cache = None
        self._can_cache_time = None
        self._can_cache = {}
        self._path_cache_revision = None
        self._path_cache = {}
        self._placement_cache_signature = None
        self._placement_cache = {}
        self._building_block_revision = 0
        self._infrastructure_dirty = True
        # DZ-Slots: Feste Positionen fÃƒÆ’Ã‚Â¼r Dorfzentren (aus MapData.xml)
        self.dz_slots = [dict(s) for s in PLAYER_1_VILLAGE_CENTER_SLOTS]

        self.built_mines = {"Steinmine": [], "Eisenmine": [], "Lehmmine": [], "Schwefelmine": []}
        self.action_history = []

        # =================================================================
        # RESSOURCEN-VERFÃƒÆ’Ã…â€œGBARKEIT (fÃƒÆ’Ã‚Â¼r korrektes Action Masking)
        # =================================================================
        # Kleine Vorkommen: erschÃƒÆ’Ã‚Â¶pfbar, Leibeigene sammeln direkt
        # Format: {resource: [{position, remaining_amount}, ...]}
        self.small_deposits = {
            "Eisen": [{"x": d["x"], "y": d["y"], "remaining": d["amount"]}
                      for d in PLAYER_1_SMALL_DEPOSITS.get("Eisen", [])],
            "Stein": [{"x": d["x"], "y": d["y"], "remaining": d["amount"]}
                      for d in PLAYER_1_SMALL_DEPOSITS.get("Stein", [])],
            "Lehm": [{"x": d["x"], "y": d["y"], "remaining": d["amount"]}
                     for d in PLAYER_1_SMALL_DEPOSITS.get("Lehm", [])],
            "Schwefel": [{"x": d["x"], "y": d["y"], "remaining": d["amount"]}
                         for d in PLAYER_1_SMALL_DEPOSITS.get("Schwefel", [])],
        }
        self._small_deposit_by_pos = {}
        for category, deps in self.small_deposits.items():
            pos_map = {}
            for dep in deps:
                key = (int(dep.get("x", 0)), int(dep.get("y", 0)))
                pos_map[key] = dep
            self._small_deposit_by_pos[category] = pos_map

        # BÃƒÆ’Ã‚Â¤ume: fÃƒÆ’Ã‚Â¼r Holz
        # ResourceAmount: 75 pro Baum, Amount: 2 pro Extraktion = 37 Extraktionen pro Baum!
        self.available_trees = len(self.resource_trees)
        self.trees_list = list(self.resource_trees)

        # =================================================================
        # VEREINFACHTES RESSOURCEN-TRACKING (ohne Serf-IDs!)
        # Agent wÃƒÆ’Ã‚Â¤hlt Kategorie + Batch-GrÃƒÆ’Ã‚Â¶ÃƒÆ’Ã…Â¸e, System verwaltet Details
        # =================================================================

        # HOLZ-ZONEN: Strategische Zonen fÃƒÆ’Ã‚Â¼r Bauplatz-Schaffung
        self.wood_serfs = 0  # Anzahl Serfs die aktuell Holz sammeln (gesamt)
        self.wood_zone_categories = self._build_dynamic_wood_zone_categories()
        self.wood_zone_names = list(self.wood_zone_categories.keys())

        # Legacy: tree_list_internal fÃƒÆ’Ã‚Â¼r KompatibilitÃƒÆ’Ã‚Â¤t (alle BÃƒÆ’Ã‚Â¤ume flach)
        # Nutzt die gleichen Dict-Objekte wie die Zonen-Listen, damit Updates konsistent bleiben.
        self.tree_list_internal = []
        for zone_name, zone_cat in self.wood_zone_categories.items():
            for tree in zone_cat["trees"]:
                tree["zone"] = zone_name  # ZusÃƒÆ’Ã‚Â¤tzliches Feld fÃƒÆ’Ã‚Â¼r Zonen-Tracking
                self.tree_list_internal.append(tree)
        self.available_tree_count = len(self.tree_list_internal)
        self._tree_by_pos = {}
        for tree in self.tree_list_internal:
            key = (int(tree.get("x", 0)), int(tree.get("y", 0)))
            self._tree_by_pos[key] = tree

        # VORKOMMEN: ZÃƒÆ’Ã‚Â¤hler pro Kategorie (keine IDs!)
        self.deposit_categories = {
            "Eisen": {
                "deposits": [{"x": d["x"], "y": d["y"], "remaining": d["amount"]}
                             for d in PLAYER_1_SMALL_DEPOSITS.get("Eisen", [])],
                "serfs_assigned": 0,
            },
            "Stein": {
                "deposits": [{"x": d["x"], "y": d["y"], "remaining": d["amount"]}
                             for d in PLAYER_1_SMALL_DEPOSITS.get("Stein", [])],
                "serfs_assigned": 0,
            },
            "Lehm": {
                "deposits": [{"x": d["x"], "y": d["y"], "remaining": d["amount"]}
                             for d in PLAYER_1_SMALL_DEPOSITS.get("Lehm", [])],
                "serfs_assigned": 0,
            },
            "Schwefel": {
                "deposits": [{"x": d["x"], "y": d["y"], "remaining": d["amount"]}
                             for d in PLAYER_1_SMALL_DEPOSITS.get("Schwefel", [])],
                "serfs_assigned": 0,
            },
        }
        self._deposit_by_pos = {}
        for category, cat_data in self.deposit_categories.items():
            pos_map = {}
            for dep in cat_data.get("deposits", []):
                key = (int(dep.get("x", 0)), int(dep.get("y", 0)))
                pos_map[key] = dep
            self._deposit_by_pos[category] = pos_map

        # STOLLEN (Shafts): Wo Serfs IMMER sammeln kÃƒÆ’Ã‚Â¶nnen (XD_Iron1, XD_Stone1, etc.)
        # Diese haben 400 Ressourcen pro Stollen und kÃƒÆ’Ã‚Â¶nnen NICHT bebaut werden.
        # Lade aus player1_resources.json (mine_shafts = echte Stollen)
        shaft_data = self._cached_resources.get("mine_shafts", {})
        self.shaft_categories = {
            "Eisen": {
                "shafts": [{"x": s["x"], "y": s["y"], "remaining": 400, "serfs_assigned": 0}
                          for s in shaft_data.get("Eisen", [])],
                "serfs_assigned": 0,
            },
            "Stein": {
                "shafts": [{"x": s["x"], "y": s["y"], "remaining": 400, "serfs_assigned": 0}
                          for s in shaft_data.get("Stein", [])],
                "serfs_assigned": 0,
            },
            "Lehm": {
                "shafts": [{"x": s["x"], "y": s["y"], "remaining": 400, "serfs_assigned": 0}
                          for s in shaft_data.get("Lehm", [])],
                "serfs_assigned": 0,
            },
            "Schwefel": {
                "shafts": [{"x": s["x"], "y": s["y"], "remaining": 400, "serfs_assigned": 0}
                          for s in shaft_data.get("Schwefel", [])],
                "serfs_assigned": 0,
            },
        }
        self._shaft_by_pos = {}
        for category, shaft_data in self.shaft_categories.items():
            pos_map = {}
            for shaft in shaft_data.get("shafts", []):
                key = (int(shaft.get("x", 0)), int(shaft.get("y", 0)))
                pos_map[key] = shaft
            self._shaft_by_pos[category] = pos_map

        self._deposit_initial_totals = {
            category: float(sum(max(0, d.get("remaining", 0)) for d in cat_data.get("deposits", [])))
            for category, cat_data in self.deposit_categories.items()
        }
        self._shaft_initial_totals = {
            category: float(sum(max(0, s.get("remaining", 0)) for s in cat_data.get("shafts", [])))
            for category, cat_data in self.shaft_categories.items()
        }

        # PrÃƒÆ’Ã‚Â¤zise Serf-Area Maps (Zonen/Deposits/Shafts)
        self._init_serf_area_maps()

        # LEGACY: mine_categories fÃƒÆ’Ã‚Â¼r KompatibilitÃƒÆ’Ã‚Â¤t (DEAKTIVIERT - Serfs arbeiten nicht an Minen!)
        # Gebaute Minen werden von Workern (PU_Miner) betrieben.
        self.mine_categories = {
            "Eisenmine": {"serfs_assigned": 0, "mines_built": 0, "max_serfs_per_mine": 0},
            "Steinmine": {"serfs_assigned": 0, "mines_built": 0, "max_serfs_per_mine": 0},
            "Lehmmine": {"serfs_assigned": 0, "mines_built": 0, "max_serfs_per_mine": 0},
            "Schwefelmine": {"serfs_assigned": 0, "mines_built": 0, "max_serfs_per_mine": 0},
        }

        # Legacy-KompatibilitÃƒÆ’Ã‚Â¤t: resource_workers nicht mehr verwendet fÃƒÆ’Ã‚Â¼r Zuweisung
        # aber noch fÃƒÆ’Ã‚Â¼r Berechnung der Produktionsraten
        self.resource_workers = {r: 0 for r in RESOURCE_MAP}

        # MinenschÃƒÆ’Ã‚Â¤chte: wo Minen-GebÃƒÆ’Ã‚Â¤ude gebaut werden KÃƒÆ’Ã¢â‚¬â€œNNEN
        self.mine_shafts = {
            "Eisenmine": [s.copy() for s in PLAYER_1_MINE_SHAFTS.get("Eisenmine", [])],
            "Steinmine": [s.copy() for s in PLAYER_1_MINE_SHAFTS.get("Steinmine", [])],
            "Lehmmine": [s.copy() for s in PLAYER_1_MINE_SHAFTS.get("Lehmmine", [])],
            "Schwefelmine": [s.copy() for s in PLAYER_1_MINE_SHAFTS.get("Schwefelmine", [])],
        }

        # NEU: WorkTime/Pausen-System initialisieren
        self.workforce_manager = WorkforceManager()

        # NEU: Produktionssystem initialisieren
        self.production_system = ProductionSystem(workforce_manager=self.workforce_manager)

        # =====================================================================
        # PERFORMANCE: Map-Daten aus Cache verwenden (schnelles Array-Copy!)
        # =====================================================================
        self.map_manager = MapManager()
        # Direkt gecachte Arrays kopieren (VIEL schneller als neu aufbauen!)
        self.map_manager.grid.terrain_base = self._cached_terrain_base.copy()
        self.map_manager.grid.trees = self._cached_trees_layer.copy()
        self.map_manager.grid.tree_positions = dict(self._cached_tree_positions)
        self.map_manager.tree_world_positions = dict(self._cached_tree_world_positions)
        self.map_manager.grid.next_tree_id = max(self._cached_tree_positions.keys()) + 1 if self._cached_tree_positions else 1
        self.map_manager.grid.revision = 0
        self.map_manager.grid.routing_revision = 0

        # Map tree world-positions to tree IDs for quick removal updates.
        self.tree_id_by_position = {}
        for tree_id, (wx, wy) in self.map_manager.tree_world_positions.items():
            self.tree_id_by_position[(int(round(wx)), int(round(wy)))] = tree_id

        # StartgebÃƒÆ’Ã‚Â¤ude aus Map-Logik registrieren (HQ + gebaute DZ-Slots)
        self._register_starting_buildings()
        self._walkable_dirty = True
        self._walkable_ratio = 0.0
        self._dynamic_blocked_ratio = 0.0

        # PERFORMANCE: Tree-ID Mapping aus Cache (nicht neu berechnen!)
        self.tree_id_mapping = dict(self._cached_tree_id_mapping)

        # Initiale Serfs erstellen (30 Leibeigene zu Start)
        # VEREINFACHT: Keine IDs mehr, nur Z?hler
        from worker_simulation import Position
        has_built_dz = any(slot.get("status") == "built" for slot in self.dz_slots)
        if not has_built_dz:
            self.total_leibeigene = 0
            self.free_leibeigene = 0
            self.serf_areas[SerfArea.FREE]["count"] = 0
        self._best_total_leibeigene = int(self.total_leibeigene)
        # Start-Serfs sind keine "neu gekauften" Serfs -> keine initialen Pending-Tokens.
        self._pending_spawned_unassigned_serfs = 0
        hq_pos = Position(x=self.hq_position[0], y=self.hq_position[1])
        for i in range(self.total_leibeigene):
            serf = Serf(
                position=Position(x=hq_pos.x, y=hq_pos.y),
                target_resource=None,  # Idle serf
            )
            self.production_system.serfs.append(serf)

        
        # NEU: Steuer-System (aus extra2)
        self.current_tax_level = INITIAL_TAX_LEVEL  # Normale Steuern als Standard

        # NEU: Segnungs-System (5 Kategorien, aus extra2)
        # Cooldown und aktive Zeit pro Kategorie
        self.bless_cooldowns = {cat: 0 for cat in BLESS_CATEGORIES}
        self.bless_active_times = {cat: 0 for cat in BLESS_CATEGORIES}

        # NEU: Glaube (Faith) fÃƒÆ’Ã‚Â¼r Segnen
        self.faith = 0  # Startwert

        # NEU: Alarm-Modus
        self.alarm_active = False
        self.alarm_cooldown = 0  # Zeit bis Alarm wieder mÃƒÆ’Ã‚Â¶glich

        # NEU: Motivation (beeinflusst WorkTime-Regeneration)
        # Aus extra2: MotivationGameStartMaxMotivation = 1.0, MotivationAbsoluteMaxMotivation = 3.0
        self.base_motivation = 1.0  # 1.0 = 100% normal

        if self.use_spatial_obs and hasattr(self, "_spatial_dynamic_dirty"):
            for name in self._dynamic_layer_names:
                self._spatial_dynamic_dirty[name] = True
            self._walkable_dirty = True

        self._start_scharf_resource_potential = self._get_scharf_resource_potential()
        self._start_scharf_dependency_progress = self._get_scharf_dependency_progress()
        self._start_scharf_recruitable = self._is_scharf_recruitable_now()

        self._last_scharf_resource_potential = self._start_scharf_resource_potential
        self._last_scharf_dependency_progress = self._start_scharf_dependency_progress
        self._reset_terminal_cumulative_tracker()
        current_research_progress = self._get_scharf_research_progress_metric()
        current_construction_progress = self._get_scharf_construction_progress_metric()
        self._last_scharf_research_progress = current_research_progress
        self._last_scharf_construction_progress = current_construction_progress
        self._last_step_unlock_progress = self._get_step_unlock_progress_metric(
            dependency_progress=self._last_scharf_dependency_progress,
            research_progress=current_research_progress,
            construction_progress=current_construction_progress,
        )
        self._last_scharf_recruitable = self._start_scharf_recruitable

        use_step_cumulative = float(
            self.reward_profile.get("step_potential_use_cumulative_earnings", 1.0)
        ) > 0.0
        step_include_start = float(
            self.reward_profile.get("step_potential_include_start_resources", 0.0)
        ) > 0.0
        step_potential_tier = self._get_reward_profile_scharf_tier(
            "step_potential_scharf_tier",
            default=1,
        )
        if use_step_cumulative:
            self._last_step_potential_metric = float(
                self._get_scharf_cumulative_resource_potential(
                    include_start_resources=step_include_start,
                    target_tier=step_potential_tier,
                )
            )
        else:
            self._last_step_potential_metric = self._get_scharf_resource_potential(
                target_tier=step_potential_tier
            )
        self._last_step_potential_units = int(max(0, int(np.floor(self._last_step_potential_metric))))
        self._best_step_taxable_workers = float(self._get_taxable_worker_count())

        return self._get_observation(), {}

    def _downsample_grid(self, grid: np.ndarray) -> np.ndarray:
        out = np.zeros((self.spatial_size, self.spatial_size), dtype=np.float32)
        ys = (np.arange(grid.shape[0]) * self.spatial_size // grid.shape[0]).astype(np.int32)
        xs = (np.arange(grid.shape[1]) * self.spatial_size // grid.shape[1]).astype(np.int32)
        np.maximum.at(out, (ys[:, None], xs[None, :]), grid)
        return out

    def _resize_grid_nearest(self, grid: np.ndarray) -> np.ndarray:
        """Nearest-Neighbor Resize auf spatial_size (fÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¼r kategoriale Layer)."""
        ys = np.linspace(0, grid.shape[0] - 1, self.spatial_size).round().astype(np.int32)
        xs = np.linspace(0, grid.shape[1] - 1, self.spatial_size).round().astype(np.int32)
        return grid[ys][:, xs]

    def _world_to_spatial(self, x: float, y: float):
        local_x, local_y = self._cached_map_manager.to_local_coords(x, y)
        gx = int(local_x / pathfinding.SCALE_X)
        gy = int(local_y / pathfinding.SCALE_Y)
        if gx < 0 or gy < 0 or gx >= self._grid_width or gy >= self._grid_height:
            return None
        sx = int(gx * self.spatial_size / self._grid_width)
        sy = int(gy * self.spatial_size / self._grid_height)
        if sx < 0 or sy < 0 or sx >= self.spatial_size or sy >= self.spatial_size:
            return None
        return sy, sx

    def _positions_to_layer(self, positions):
        layer = np.zeros((self.spatial_size, self.spatial_size), dtype=np.float32)
        if not positions:
            return layer

        arr = np.asarray(positions, dtype=np.float32)
        if arr.ndim != 2 or arr.shape[1] < 2:
            return layer

        xs = arr[:, 0]
        ys = arr[:, 1]

        offset_x = self._cached_map_manager.offset_x
        offset_y = self._cached_map_manager.offset_y
        local_x = xs - offset_x
        local_y = ys - offset_y

        gx = (local_x / pathfinding.SCALE_X).astype(np.int32)
        gy = (local_y / pathfinding.SCALE_Y).astype(np.int32)

        in_bounds = (
            (gx >= 0) & (gy >= 0) &
            (gx < self._grid_width) & (gy < self._grid_height)
        )
        if not np.any(in_bounds):
            return layer

        gx = gx[in_bounds]
        gy = gy[in_bounds]

        sx = (gx * self.spatial_size // self._grid_width).astype(np.int32)
        sy = (gy * self.spatial_size // self._grid_height).astype(np.int32)

        in_spatial = (
            (sx >= 0) & (sy >= 0) &
            (sx < self.spatial_size) & (sy < self.spatial_size)
        )
        if not np.any(in_spatial):
            return layer

        layer[sy[in_spatial], sx[in_spatial]] = 1.0
        return layer

    def _mark_spatial_dirty(self, *names: str) -> None:
        if not self.use_spatial_obs:
            return
        if not hasattr(self, "_spatial_dynamic_dirty"):
            return
        for name in names:
            if name in self._spatial_dynamic_dirty:
                self._spatial_dynamic_dirty[name] = True

    def _mark_infrastructure_dirty(self) -> None:
        self._infrastructure_dirty = True

    def _register_starting_buildings(self) -> None:
        """Registriert StartgebÃƒÆ’Ã‚Â¤ude (HQ + gebaute Dorfzentrum-Slots) im State und Grid."""
        # HQ sicherstellen
        hq_x, hq_y = self.hq_position
        hq_key = "Hauptquartier_1_0"
        hq_pos = {"x": hq_x, "y": hq_y}
        self.buildings["Hauptquartier_1"] = 1
        self.building_position_map[hq_key] = hq_pos
        self.building_grid_ids[hq_key] = self.map_manager.add_building(hq_x, hq_y, "Hauptquartier")

        # Gebaute DZ-Slots auf der Karte als echte StartgebÃƒÆ’Ã‚Â¤ude fÃƒÆ’Ã‚Â¼hren.
        built_slots = [slot for slot in self.dz_slots if slot.get("status") == "built"]
        self.buildings["Dorfzentrum_1"] = len(built_slots)
        for idx, slot in enumerate(built_slots):
            key = f"Dorfzentrum_1_{idx}"
            pos = {"x": slot["x"], "y": slot["y"]}
            self.building_position_map[key] = pos
            self.building_grid_ids[key] = self.map_manager.add_building(pos["x"], pos["y"], "Dorfzentrum")

        self._building_block_revision += 1

    def _init_spatial_layers(self):
        self._spatial_static_layers = {}
        self._spatial_static_names = []

        walkable = self._downsample_grid(self._cached_walkable.astype(np.float32))
        self._spatial_static_layers["walkable"] = walkable
        self._spatial_static_names.append("walkable")

        blocked = 1.0 - walkable
        self._spatial_static_layers["blocked"] = blocked
        self._spatial_static_names.append("blocked")

        # Low-Res Terrain (kategorial, aus Map-Extract)
        if self._cached_lowres_terrain is not None:
            terrain_layer = self._resize_grid_nearest(
                self._cached_lowres_terrain.astype(np.float32)
            )
            max_val = float(np.max(terrain_layer)) if np.max(terrain_layer) > 0 else 1.0
            terrain_layer = terrain_layer / max_val
            self._spatial_static_layers["terrain_lowres"] = terrain_layer
            self._spatial_static_names.append("terrain_lowres")

        mine_positions = []
        for slots in PLAYER_1_MINE_SHAFTS.values():
            for slot in slots:
                mine_positions.append((slot["x"], slot["y"]))
        self._spatial_static_layers["mine_shafts"] = self._positions_to_layer(mine_positions)
        self._spatial_static_names.append("mine_shafts")

        slot_positions = []
        for pos in self.building_zones.get("zone_a_immediate", []):
            slot_positions.append((pos["x"], pos["y"]))
        for pos in self.building_zones.get("zone_b_after_logging", []):
            slot_positions.append((pos["x"], pos["y"]))
        self._spatial_static_layers["build_slots"] = self._positions_to_layer(slot_positions)
        self._spatial_static_names.append("build_slots")

        # Final channel order (static + dynamic)
        self._spatial_channels = list(self._spatial_static_names)
        self._dynamic_layer_names = [
            "trees",
            "deposits",
            "buildings",
            "available_slots",
            "construction_sites",
        ]
        self._spatial_channels.extend(self._dynamic_layer_names)

        self._spatial_dynamic_layers = {
            name: np.zeros((self.spatial_size, self.spatial_size), dtype=np.float32)
            for name in self._dynamic_layer_names
        }
        self._spatial_dynamic_dirty = {name: True for name in self._dynamic_layer_names}

    def _get_spatial_observation(self) -> np.ndarray:
        layers = []
        if "walkable" in self._spatial_static_layers:
            self._refresh_walkable_cache()
        for name in self._spatial_static_names:
            layers.append(self._spatial_static_layers[name])
        self._refresh_dynamic_layers()
        for name in self._dynamic_layer_names:
            layers.append(self._spatial_dynamic_layers[name])

        return np.stack(layers, axis=0)

    def _get_observation(self):
        phase_idx = self.phase_index.get(self.current_phase, 0)
        phase_vec = np.zeros(self.phase_dim, dtype=np.float32)
        phase_vec[phase_idx] = 1.0

        if getattr(self, "_obs_cache_time", None) == self.current_time and self._obs_cache_base is not None:
            base = self._obs_cache_base
        else:
            obs = []

            for r in RESOURCE_NAMES:
                obs.append(self._normalize_resource_for_obs(r, self.resources.get(r, 0)))

            for r in RESOURCE_MAP:
                obs.append(self.resource_workers.get(r, 0) / 50.0)
            obs.append(self.free_leibeigene / 100.0)
            obs.append(self.total_leibeigene / 100.0)

            construction_counts = {}
            if self.construction_queue:
                for building, _, _ in self.construction_queue:
                    construction_counts[building] = construction_counts.get(building, 0) + 1
            if self.construction_sites:
                for site in self.construction_sites:
                    building = site.get("building")
                    if building:
                        construction_counts[building] = construction_counts.get(building, 0) + 1

            for b in self.buildable_buildings:
                obs.append(self.buildings.get(b, 0) / 10.0)
                in_construction = construction_counts.get(b, 0)
                obs.append(in_construction / 5.0)

            for b in self.upgradeable_buildings:
                obs.append(self.buildings.get(b, 0) / 5.0)

            for t in self.tech_list:
                obs.append(1.0 if t in self.researched_techs else 0.0)
                obs.append(1.0 if t in self.researching_set else 0.0)

            for s in self.soldier_types:
                obs.append(self.soldiers.get(s, 0) / 50.0)

            obs.append(self.current_time / self.max_time)
            obs.append((self.max_time - self.current_time) / self.max_time)

            for r in RESOURCE_MAP:
                obs.append(self._get_production_rate(r) / 10.0)
            obs.append((self._get_taler_income() * self._get_trade_income_multiplier()) / 100.0)

            # WorkTime-System Observations
            workforce_stats = self.workforce_manager.get_stats()
            obs.append(workforce_stats.get("avg_work_time", 100) / 400.0)  # Max WorkTime ist 400
            obs.append(workforce_stats.get("exhausted_ratio", 0))
            obs.append(workforce_stats.get("eating_workers", 0) / 50.0)
            obs.append(workforce_stats.get("resting_workers", 0) / 50.0)
            obs.append(workforce_stats.get("working_workers", 0) / 50.0)
            obs.append(workforce_stats.get("walking_workers", 0) / 50.0)

            # Kapazitaets-Stats
            total_farm_capacity = self._get_total_farm_capacity()
            total_residence_capacity = self._get_total_residence_capacity()
            obs.append(total_farm_capacity / 50.0)
            obs.append(len(self.workforce_manager.workers) / max(1, total_farm_capacity))  # Farm-Auslastung
            obs.append(total_residence_capacity / 50.0)
            obs.append(len(self.workforce_manager.workers) / max(1, total_residence_capacity))  # Wohnhaus-Auslastung

            # Effizienz und Serf-Count
            obs.append(self.workforce_manager.get_average_efficiency())
            obs.append(len(self.production_system.serfs) / 100.0)

            # Observations fuer neue Actions (erweitert fuer 5 Kategorien + Alarm)
            obs.append(self.current_tax_level / 4.0)  # Normalisiert auf 0-1
            obs.append(1.0 if self.alarm_active else 0.0)  # Alarm aktiv?
            obs.append(self.alarm_cooldown / self._get_alarm_recharge_time())  # Alarm-Cooldown
            required_faith = max(1, self._get_bless_required_faith())
            obs.append(self.faith / required_faith)  # Faith normalisiert

            # Segen pro Kategorie (5x Cooldown + 5x aktiv)
            for cat in BLESS_CATEGORIES:
                obs.append(self.bless_cooldowns.get(cat, 0) / BLESS_COOLDOWN)
            for cat in BLESS_CATEGORIES:
                obs.append(1.0 if self.bless_active_times.get(cat, 0) > 0 else 0.0)

            # Forschungs-Gebaeude-Status (Anzahl unerforschter Techs, normalisiert)
            for building in RESEARCH_BUILDINGS:
                techs = self.tech_by_building.get(building, [])
                remaining = sum(1 for t in techs if t not in self.researched_techs)
                obs.append(remaining / max(1, MAX_TECHS_PER_BUILDING))

            # Makro- und Queue-Stats (Training-Qualitaet)
            village_capacity = self._get_total_village_capacity()
            free_capacity = max(0, village_capacity - self.total_leibeigene)
            obs.append(village_capacity / MAX_POSSIBLE_LEIBEIGENE)
            obs.append(free_capacity / MAX_POSSIBLE_LEIBEIGENE)

            construction_len = len(self.construction_queue) + len(self.construction_sites)
            upgrade_len = len(self.upgrade_queue)
            research_len = len(self.current_researches)
            obs.append(construction_len / 20.0)
            obs.append(upgrade_len / 20.0)
            obs.append(research_len / 10.0)

            remaining_construction = [c[1] for c in self.construction_queue]
            remaining_construction.extend(
                [site.get("remaining_work", 0.0) for site in self.construction_sites]
            )
            avg_construction = np.mean(remaining_construction) if remaining_construction else 0.0
            avg_upgrade = np.mean([u[2] for u in self.upgrade_queue]) if self.upgrade_queue else 0.0
            avg_research = np.mean([r[1] for r in self.current_researches]) if self.current_researches else 0.0
            obs.append(avg_construction / self.max_time)
            obs.append(avg_upgrade / self.max_time)
            obs.append(avg_research / self.max_time)

            site_count = len(self.construction_sites)
            site_serfs = sum(site.get("serfs_assigned", 0) for site in self.construction_sites)
            obs.append(site_count / 10.0)
            obs.append(site_serfs / 50.0)

            total_positions = len(self.available_positions) + len(self.zone_b_positions)
            obs.append(len(self.available_positions) / max(1, total_positions))

            obs.append(self._get_total_motivation() / 3.0)

            # Dynamische Walkable-Info (Grid-Status)
            self._refresh_walkable_cache()
            obs.append(getattr(self, "_walkable_ratio", 0.0))
            obs.append(getattr(self, "_dynamic_blocked_ratio", 0.0))

            # Zielnahe Features fuer stabileres Scharfschuetzen-Lernen.
            obs.extend(self._get_goal_observation_features())

            expected_base_obs = self.vector_obs_size - self.phase_dim
            if len(obs) != expected_base_obs:
                raise RuntimeError(
                    f"Observation length mismatch: got {len(obs)} expected {expected_base_obs}"
                )

            base = np.array(obs, dtype=np.float32)
            self._obs_cache_base = base
            self._obs_cache_time = self.current_time

        vector_obs = np.concatenate([base, phase_vec])
        if self.use_spatial_obs:
            use_cache = (
                getattr(self, "_spatial_cache_time", None) == self.current_time
                and not getattr(self, "_walkable_dirty", True)
                and hasattr(self, "_spatial_dynamic_dirty")
                and not any(self._spatial_dynamic_dirty.values())
                and self._spatial_cache is not None
            )
            if use_cache:
                spatial_obs = self._spatial_cache
            else:
                spatial_obs = self._get_spatial_observation()
                self._spatial_cache = spatial_obs
                self._spatial_cache_time = self.current_time
            return {"vector": vector_obs, "spatial": spatial_obs}
        return vector_obs

    def _get_production_rate(self, resource):
        if not hasattr(self, "production_system"):
            return 0.0

        res_type = _RESOURCE_TYPE_MAP.get(resource)
        if not res_type:
            return 0.0

        efficiency = self.workforce_manager.get_average_efficiency() if hasattr(self, "workforce_manager") else 1.0
        rates = self.production_system.get_production_rates(efficiency)
        rate = rates.get(res_type, 0.0)

        # Output-Bonus nur auf veredelte Ressourcen anwenden
        resource_key = _RESOURCE_KEY_MAP.get(resource)
        if resource_key:
            bonus_pct = self._get_resource_output_bonus_pct(resource_key)
            rate *= (1.0 + (bonus_pct / 100.0))
        return rate

    def _apply_passive_building_outputs(self, dt: float) -> None:
        """Wendet passives GebÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¤ude-Output an (ohne Mines/Refiner-DoppelzÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¤hlung)."""
        if dt <= 0:
            return

        outputs = {}
        for b_name, count in self.buildings.items():
            if count <= 0:
                continue
            base = get_base_building_name(b_name)
            if base in PASSIVE_OUTPUT_EXCLUDE_BASES:
                continue
            output = buildings_db.get(b_name, {}).get("resource_output", {})
            if not output:
                continue
            for res_name, amount in output.items():
                if amount <= 0:
                    continue
                outputs[res_name] = outputs.get(res_name, 0.0) + (amount * count)

        if not outputs:
            return

        cycle = max(1.0, float(PASSIVE_OUTPUT_CYCLE))
        resource_key_map = {
            RESOURCE_HOLZ: "wood",
            RESOURCE_STEIN: "stone",
            RESOURCE_LEHM: "clay",
            RESOURCE_EISEN: "iron",
            RESOURCE_SCHWEFEL: "sulfur",
            RESOURCE_TALER: "gold",
        }
        for res_name, amount_per_cycle in outputs.items():
            amount = (amount_per_cycle / cycle) * dt
            resource_key = resource_key_map.get(res_name)
            bonus_pct = self._get_resource_output_bonus_pct(resource_key) if resource_key else 0.0
            adjusted = amount * (1.0 + (bonus_pct / 100.0))
            self.resources[res_name] = self.resources.get(res_name, 0) + adjusted

    def _get_total_motivation(self) -> float:
        """Berechnet die Basis-Motivation (ohne Segen, der ist pro Worker-Typ).

        Aus extra2/logic.xml:
        - MotivationThresholdHappy = 1.5 (sehr glÃƒÆ’Ã‚Â¼cklich)
        - MotivationThresholdSad = 1.0 (traurig)
        - MotivationThresholdAngry = 0.7 (wÃƒÆ’Ã‚Â¼tend)
        - MotivationThresholdLeave = 0.25 (verlÃƒÆ’Ã‚Â¤sst Settlement!)
        - MotivationAbsoluteMaxMotivation = 3.0
        """
        cache_key = ("total_motivation",)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return float(cached)

        motivation = self.base_motivation

        # Motivation aus GebÃƒÆ’Ã‚Â¤uden (z.B. Kloster, Schmuck)
        for b_name, count in self.buildings.items():
            effect = buildings_db.get(b_name, {}).get("motivation_effect")
            if effect:
                motivation += effect * count

        # Segen-Bonus jetzt PRO WORKER-TYP (nicht mehr global!)
        # Wird ÃƒÆ’Ã‚Â¼ber _get_blessed_worker_types() an WorkforceManager ÃƒÆ’Ã‚Â¼bergeben

        # Clamp auf gÃƒÆ’Ã‚Â¼ltige Werte
        result = max(0.25, min(3.0, motivation))
        self._set_can_cache(cache_key, float(result))
        return float(result)

    def _get_blessed_worker_types(self) -> set:
        """Gibt die Menge aller aktuell gesegneten Worker-Typen zurÃƒÆ’Ã‚Â¼ck.

        Basierend auf aktiven Segen-Kategorien und deren worker_types.
        Aus extra2/logic.xml: Segen wirkt NUR auf Worker der Kategorie!
        """
        blessed = set()
        for cat, info in BLESS_CATEGORIES.items():
            if self.bless_active_times.get(cat, 0) > 0:
                for wt in info["worker_types"]:
                    if wt.upper() == "ALL":
                        blessed.add("all")
                    else:
                        blessed.add(normalize_worker_type(wt))
        return blessed

    # -----------------------------------------------------------------
    # Tech-Effekt Helper (vereinfachte, aber konsistente Anwendung)
    # -----------------------------------------------------------------
    def _get_bless_required_faith(self) -> int:
        reduction = self.active_tech_effects.get("bless_faith_reduction", 0)
        return max(0, BLESS_REQUIRED_FAITH - int(reduction))

    def _get_bless_duration(self) -> int:
        bonus = self.active_tech_effects.get("bless_duration_bonus", 0)
        return max(1, BLESS_DURATION + int(bonus))

    def _get_alarm_recharge_time(self) -> int:
        reduction = self.active_tech_effects.get("alarm_recharge_reduction", 0)
        return max(1, ALARM_RECHARGE_TIME - int(reduction))

    def _get_tax_income_multiplier(self) -> float:
        bonus = self.active_tech_effects.get("tax_income_bonus", 0.0)
        bonus += self.active_tech_effects.get("payday_bonus", 0.0)
        return 1.0 + (bonus / 100.0)

    def _get_trade_income_multiplier(self) -> float:
        bonus = self.active_tech_effects.get("trade_bonus", 0.0)
        return 1.0 + (bonus / 100.0)

    def _get_tax_penalty(self) -> float:
        reduction = self.active_tech_effects.get("tax_penalty_reduction", 0.0)
        return max(0.0, TAX_PENALTY - reduction)

    def _get_farm_capacity_bonus(self) -> int:
        return int(self.active_tech_effects.get("farm_capacity_bonus", 0))

    def _get_residence_capacity_bonus(self) -> int:
        return int(self.active_tech_effects.get("residence_capacity_bonus", 0))

    def _get_effective_serf_search_radius(self) -> int:
        bonus = self.active_tech_effects.get("serf_search_radius_bonus", 0)
        return int(SERF_SEARCH_RADIUS + bonus)

    def _get_effective_serf_resource_search_radius(self) -> int:
        bonus = self.active_tech_effects.get("serf_resource_search_radius_bonus", 0)
        return int(SERF_RESOURCE_SEARCH_RADIUS + bonus)

    def _get_resource_output_bonus_pct(self, resource_key: str) -> float:
        """Gibt Prozent-Bonus fÃƒÆ’Ã‚Â¼r eine Ressource zurÃƒÆ’Ã‚Â¼ck (z.B. 'wood')."""
        base_bonus = self.active_tech_effects.get("resource_output_bonus_all", 0.0)
        specific = self.active_tech_effects.get(f"resource_output_bonus_{resource_key}", 0.0)
        return base_bonus + specific

    def _get_total_resource(self, resource: str) -> float:
        """Summiert Raw + Refined fÃƒÆ’Ã‚Â¼r KostenprÃƒÆ’Ã‚Â¼fung (Original-UI Logik)."""
        raw = REFINED_TO_RAW.get(resource)
        if raw:
            return self.resources.get(resource, 0) + self.resources.get(raw, 0)
        refined = RAW_TO_REFINED.get(resource)
        if refined:
            return self.resources.get(resource, 0) + self.resources.get(refined, 0)
        return self.resources.get(resource, 0)

    def _normalize_resource_for_obs(self, resource: str, value: float) -> float:
        """Skaliert Ressourcen robust in [0, 1] fuer stabileres Training."""
        caps = {
            RESOURCE_HOLZ: 6000.0,
            RESOURCE_STEIN: 6000.0,
            RESOURCE_LEHM: 6000.0,
            RESOURCE_EISEN: 4000.0,
            RESOURCE_SCHWEFEL: 4000.0,
            RESOURCE_HOLZ_ROH: 15000.0,
            RESOURCE_STEIN_ROH: 15000.0,
            RESOURCE_LEHM_ROH: 15000.0,
            RESOURCE_EISEN_ROH: 15000.0,
            RESOURCE_SCHWEFEL_ROH: 15000.0,
            RESOURCE_GOLD_ROH: 8000.0,
            RESOURCE_TALER: 8000.0,
        }
        cap = max(1.0, float(caps.get(resource, 8000.0)))
        v = max(0.0, float(value))
        return float(min(1.0, np.log1p(v) / np.log1p(cap)))

    @staticmethod
    def _remaining_ratio_from_entries(entries: List[dict], initial_total: float) -> float:
        if initial_total <= 0:
            return 0.0
        current = float(sum(max(0.0, float(e.get("remaining", 0.0))) for e in entries))
        return float(max(0.0, min(1.0, current / initial_total)))

    def _get_scharf_costs(self, target_tier: Optional[int] = None) -> Tuple[float, float]:
        """Liefert Scharfschuetzen-Kosten (Taler, Schwefel), optional tier-spezifisch."""
        candidates: List[Tuple[int, float, float]] = []
        for name, cfg in soldiers_db.items():
            if "Scharf" not in str(name):
                continue
            cost = cfg.get("cost", {})
            taler = float(cost.get(RESOURCE_TALER, 1e9))
            sulfur = float(cost.get(RESOURCE_SCHWEFEL, 1e9))
            tier = 1
            match = re.search(r"_(\d+)$", str(name))
            if match:
                try:
                    tier = max(1, int(match.group(1)))
                except (TypeError, ValueError):
                    tier = 1
            candidates.append((tier, taler, sulfur))
        if not candidates:
            return 250.0, 70.0

        if target_tier is not None:
            tier_candidates = [(taler, sulfur) for tier, taler, sulfur in candidates if tier == int(target_tier)]
            if tier_candidates:
                taler_cost, sulfur_cost = min(tier_candidates, key=lambda x: x[0])
                return max(1.0, taler_cost), max(1.0, sulfur_cost)

        taler_cost, sulfur_cost = min(
            [(taler, sulfur) for _, taler, sulfur in candidates],
            key=lambda x: x[0],
        )
        return max(1.0, taler_cost), max(1.0, sulfur_cost)

    def _get_reward_profile_scharf_tier(self, key: str, default: int = 1) -> int:
        raw_value = self.reward_profile.get(key, float(default))
        try:
            parsed = int(round(float(raw_value)))
        except (TypeError, ValueError):
            parsed = int(default)
        return max(1, parsed)

    def _reward_for_buy_serf_growth(self) -> float:
        current_total = max(0, int(self.total_leibeigene))
        previous_best = int(self._best_total_leibeigene)
        gained = max(0, current_total - previous_best)
        if current_total > previous_best:
            self._best_total_leibeigene = current_total
        return float(gained) * float(self.reward_profile.get("action_buy_serf_growth_bonus", 0.0))

    def _reward_for_assigning_spawned_serfs(self, assigned_from_free: int) -> float:
        """Einmaliger Reward fuer frisch gespawnte/gekaufte FREE-Serfs beim ersten Assign."""
        assigned = max(0, int(assigned_from_free))
        if assigned <= 0:
            return 0.0
        pending = max(0, int(getattr(self, "_pending_spawned_unassigned_serfs", 0)))
        rewarded_units = min(assigned, pending)
        if rewarded_units <= 0:
            return 0.0
        self._pending_spawned_unassigned_serfs = max(0, pending - rewarded_units)
        bonus = float(self.reward_profile.get("action_assign_spawned_serf_bonus", 0.0))
        return float(rewarded_units) * bonus

    def _get_scharf_soldier_types(self) -> List[str]:
        soldier_types = getattr(self, "soldier_types", None)
        if soldier_types is None:
            soldier_types = list(soldiers_db.keys())
        return [soldier for soldier in soldier_types if "Scharf" in str(soldier)]

    def _get_scharf_requirements(self) -> Tuple[Set[str], Set[str]]:
        """Ermittelt fuer Scharfschuetzen relevante Gebaeude- und Technologie-Anforderungen."""
        req_buildings: Set[str] = set()
        req_techs: Set[str] = set()
        for soldier in self._get_scharf_soldier_types():
            for req in soldiers_db.get(soldier, {}).get("requirements", []):
                if req in buildings_db:
                    req_buildings.add(req)
                elif req in technologies:
                    req_techs.add(req)
        return req_buildings, req_techs

    def _get_scharf_resource_potential(self, target_tier: Optional[int] = None) -> float:
        """Theoretisch rekrutierbare Scharfschuetzen nur aus Taler+Schwefel."""
        taler_cost, sulfur_cost = self._get_scharf_costs(target_tier=target_tier)
        taler_total = float(self._get_total_resource(RESOURCE_TALER))
        sulfur_total = float(self._get_total_resource(RESOURCE_SCHWEFEL))
        return float(max(0.0, min(taler_total / taler_cost, sulfur_total / sulfur_cost)))

    def _get_scharf_research_progress_metric(self) -> float:
        """
        Fortschrittsmetrik (0..1) fuer scharf-relevante Forschung.
        Belohnt auch laengere Forschungen bereits waehrend sie laufen.
        """
        required_techs = self._scharf_required_techs or set()
        if not required_techs:
            return 0.0

        in_progress: Dict[str, float] = {}
        for tech, remaining in self.current_researches:
            if tech not in required_techs:
                continue
            total = float(technologies.get(tech, {}).get("research_time", 0.0))
            if total <= 0.0:
                continue
            progress = max(0.0, min(1.0, 1.0 - (float(remaining) / total)))
            prev = in_progress.get(tech, 0.0)
            if progress > prev:
                in_progress[tech] = progress

        score = 0.0
        for tech in required_techs:
            if tech in self.researched_techs:
                score += 1.0
            else:
                score += float(in_progress.get(tech, 0.0))

        return float(max(0.0, min(1.0, score / max(1, len(required_techs)))))

    def _get_scharf_construction_progress_metric(self) -> float:
        """
        Fortschrittsmetrik (0..1) fuer scharf-relevante Gebaeude.
        Beruecksichtigt bereits laufende Baustellen.
        """
        required_buildings = self._scharf_required_buildings or set()
        if not required_buildings:
            return 0.0

        score = 0.0
        for building in required_buildings:
            if self.buildings.get(building, 0) >= 1:
                score += 1.0
                continue

            progress = 0.0
            for site in self.construction_sites:
                if site.get("building") != building:
                    continue
                total = float(site.get("total_time", 0.0))
                if total <= 0.0:
                    continue
                remaining = float(site.get("remaining_work", total))
                site_progress = max(0.0, min(1.0, 1.0 - (remaining / total)))
                if site_progress > progress:
                    progress = site_progress

            for item in self.construction_queue:
                if len(item) < 2:
                    continue
                queued_building = item[0]
                if queued_building != building:
                    continue
                total = float(buildings_db.get(building, {}).get("build_time", 0.0))
                if total <= 0.0:
                    continue
                remaining = float(item[1])
                queued_progress = max(0.0, min(1.0, 1.0 - (remaining / total)))
                if queued_progress > progress:
                    progress = queued_progress

            score += progress

        return float(max(0.0, min(1.0, score / max(1, len(required_buildings)))))

    def _reset_terminal_cumulative_tracker(self) -> None:
        """Initialisiert Tracking fuer kumulierte Episode-Einnahmen (Taler/Schwefel)."""
        self._terminal_start_total_taler = float(self._get_total_resource(RESOURCE_TALER))
        self._terminal_start_total_schwefel = float(self._get_total_resource(RESOURCE_SCHWEFEL))
        self._terminal_prev_total_taler = self._terminal_start_total_taler
        self._terminal_prev_total_schwefel = self._terminal_start_total_schwefel
        self._terminal_cumulative_taler_earned = 0.0
        self._terminal_cumulative_schwefel_earned = 0.0

    def _update_terminal_cumulative_tracker(self) -> None:
        """Akkumuliert positive Delta-Zugaenge je Step (sparse reward bleibt unveraendert)."""
        current_taler = float(self._get_total_resource(RESOURCE_TALER))
        current_schwefel = float(self._get_total_resource(RESOURCE_SCHWEFEL))

        delta_taler = current_taler - float(self._terminal_prev_total_taler)
        delta_schwefel = current_schwefel - float(self._terminal_prev_total_schwefel)

        if delta_taler > 0.0:
            self._terminal_cumulative_taler_earned += float(delta_taler)
        if delta_schwefel > 0.0:
            self._terminal_cumulative_schwefel_earned += float(delta_schwefel)

        self._terminal_prev_total_taler = current_taler
        self._terminal_prev_total_schwefel = current_schwefel

    def _get_scharf_cumulative_resource_potential(
        self,
        include_start_resources: bool = False,
        target_tier: Optional[int] = None,
    ) -> float:
        """Scharfschuetzen-Potential aus kumulierten Episode-Einnahmen."""
        taler_cost, sulfur_cost = self._get_scharf_costs(target_tier=target_tier)
        taler_total = float(self._terminal_cumulative_taler_earned)
        sulfur_total = float(self._terminal_cumulative_schwefel_earned)
        if include_start_resources:
            taler_total += float(self._terminal_start_total_taler)
            sulfur_total += float(self._terminal_start_total_schwefel)
        return float(max(0.0, min(taler_total / taler_cost, sulfur_total / sulfur_cost)))

    def _get_scharf_dependency_progress(self) -> float:
        """
        Fortschritt auf dem Rekrutierungs-Pfad (0..1), ohne Ressourcen:
        - Requirements (Gebaeude/Techs)
        - Motivation-Gate (VillageCenterLockThreshold)
        """
        scharf_units = self._get_scharf_soldier_types()
        if not scharf_units:
            return 0.0

        threshold = max(1e-6, float(VILLAGE_CENTER_LOCK_THRESHOLD))
        motivation_ratio = float(max(0.0, min(1.0, self._get_total_motivation() / threshold)))
        best_progress = 0.0

        for soldier in scharf_units:
            reqs = soldiers_db.get(soldier, {}).get("requirements", [])
            req_total = 0
            req_met = 0.0

            for req in reqs:
                if req in buildings_db:
                    req_total += 1
                    if self.buildings.get(req, 0) >= 1:
                        req_met += 1.0
                elif req in technologies:
                    req_total += 1
                    if req in self.researched_techs:
                        req_met += 1.0

            denominator = float(max(1, req_total + 1))  # +1 fuer Motivation-Gate
            progress = (req_met + motivation_ratio) / denominator
            best_progress = max(best_progress, progress)

        return float(max(0.0, min(1.0, best_progress)))

    def _get_step_unlock_progress_metric(
        self,
        dependency_progress: float,
        research_progress: float,
        construction_progress: float,
    ) -> float:
        """Kompakter Fortschrittswert (0..1) fuer Step-Shaping."""
        dep_weight = max(0.0, float(self.reward_profile.get("step_progress_mix_dependency", 1.0)))
        research_weight = max(0.0, float(self.reward_profile.get("step_progress_mix_research", 1.0)))
        construction_weight = max(0.0, float(self.reward_profile.get("step_progress_mix_construction", 1.0)))
        total_weight = dep_weight + research_weight + construction_weight

        dep = float(max(0.0, min(1.0, dependency_progress)))
        research = float(max(0.0, min(1.0, research_progress)))
        construction = float(max(0.0, min(1.0, construction_progress)))

        if total_weight <= 1e-9:
            return dep

        metric = (
            dep * dep_weight
            + research * research_weight
            + construction * construction_weight
        ) / total_weight
        return float(max(0.0, min(1.0, metric)))

    def _is_scharf_recruitable_now(self) -> bool:
        for soldier in self._get_scharf_soldier_types():
            if self._can_recruit(soldier):
                return True
        return False

    def _get_goal_observation_features(self) -> List[float]:
        """
        Zielnahe Features fuer den Scharfschuetzen-Pfad.
        Anzahl Rueckgabewerte: 17 (muss zu n_macro_obs passen).
        """
        taler_cost, sulfur_cost = self._get_scharf_costs()
        taler_total = self._get_total_resource(RESOURCE_TALER)
        sulfur_total = self._get_total_resource(RESOURCE_SCHWEFEL)

        potential_by_taler = taler_total / taler_cost
        potential_by_sulfur = sulfur_total / sulfur_cost
        potential_bottleneck = min(potential_by_taler, potential_by_sulfur)

        scharf_queue_remaining = [
            float(remaining)
            for soldier, remaining in self.recruit_queue
            if "Scharf" in str(soldier)
        ]
        queued_scharf_count = float(len(scharf_queue_remaining))
        avg_scharf_eta = float(np.mean(scharf_queue_remaining)) if scharf_queue_remaining else 0.0

        if isinstance(SCHARFSCHUETZEN_PATH, dict):
            milestone_techs = list(SCHARFSCHUETZEN_PATH.get("required_techs", []))
        else:
            milestone_techs = []
        if not milestone_techs:
            milestone_techs = ["Mathematik", "Fernglas", "Luntenschloss", "Gezogener Lauf"]
        key_tech_progress = (
            sum(1 for tech in milestone_techs if tech in self.researched_techs)
            / max(1, len(milestone_techs))
        )

        features: List[float] = [
            min(1.0, float(self.scharfschuetzen) / 60.0),
            min(1.0, queued_scharf_count / 20.0),
            min(1.0, avg_scharf_eta / 180.0),
            min(1.0, potential_by_taler / 60.0),
            min(1.0, potential_by_sulfur / 60.0),
            min(1.0, potential_bottleneck / 60.0),
            min(1.0, potential_by_taler),
            min(1.0, potential_by_sulfur),
            float(max(0.0, min(1.0, key_tech_progress))),
        ]

        for category in ["Eisen", "Stein", "Lehm", "Schwefel"]:
            entries = self.deposit_categories.get(category, {}).get("deposits", [])
            initial = float(self._deposit_initial_totals.get(category, 0.0))
            features.append(self._remaining_ratio_from_entries(entries, initial))

        for category in ["Eisen", "Stein", "Lehm", "Schwefel"]:
            entries = self.shaft_categories.get(category, {}).get("shafts", [])
            initial = float(self._shaft_initial_totals.get(category, 0.0))
            features.append(self._remaining_ratio_from_entries(entries, initial))

        return features

    def _spend_resource(self, resource: str, amount: float) -> None:
        """Verbraucht Ressourcen, erst Refined dann Raw (kombinierter Pool)."""
        if amount <= 0:
            return
        raw = REFINED_TO_RAW.get(resource)
        if raw:
            refined_amount = self.resources.get(resource, 0)
            if refined_amount >= amount:
                self.resources[resource] = refined_amount - amount
                return
            self.resources[resource] = 0
            remaining = amount - refined_amount
            self.resources[raw] = max(0, self.resources.get(raw, 0) - remaining)
            return
        refined = RAW_TO_REFINED.get(resource)
        if refined:
            raw_amount = self.resources.get(resource, 0)
            if raw_amount >= amount:
                self.resources[resource] = raw_amount - amount
                return
            self.resources[resource] = 0
            remaining = amount - raw_amount
            self.resources[refined] = max(0, self.resources.get(refined, 0) - remaining)
            return
        self.resources[resource] = self.resources.get(resource, 0) - amount

    def _spend_costs(self, costs: dict) -> None:
        for resource, amount in costs.items():
            self._spend_resource(resource, amount)

    def _get_scholar_efficiency(self) -> float:
        """Berechnet die Gesamteffizienz aller Gelehrten.

        Gelehrte mit niedriger WorkTime arbeiten langsamer (nur 10% bei ErschÃƒÆ’Ã‚Â¶pfung).
        Returns: Summe der Effizienzen (0.0 wenn keine Gelehrten)
        """
        scholars = [w for w in self.workforce_manager.workers
                    if w.worker_type == "scholar"]
        if not scholars:
            # Keine Gelehrten = keine Forschung
            return 0.0
        total_efficiency = sum(w.get_efficiency() for w in scholars)
        return total_efficiency

    def _get_can_cache(self, key):
        if getattr(self, "_can_cache_time", None) != self.current_time:
            self._can_cache_time = self.current_time
            self._can_cache = {}
        return self._can_cache.get(key, None)

    def _set_can_cache(self, key, value):
        if getattr(self, "_can_cache_time", None) != self.current_time:
            self._can_cache_time = self.current_time
            self._can_cache = {}
        self._can_cache[key] = value
        return value

    def _can_buy_serf(self) -> bool:
        """PrÃƒÆ’Ã‚Â¼ft ob ein Leibeigener gekauft werden kann."""
        return self._can_buy_serf_batch(1)

    def _can_buy_serf_batch(self, count: int) -> bool:
        """PrÃƒÆ’Ã‚Â¼ft ob mehrere Leibeigene gekauft werden kÃƒÆ’Ã‚Â¶nnen."""
        cache_key = ("buy_serf_batch", count)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return cached
        # VillageCenterLockThreshold: Unter 0.3 Motivation keine neuen Worker/Serfs!
        if self._get_total_motivation() < VILLAGE_CENTER_LOCK_THRESHOLD:
            return self._set_can_cache(cache_key, False)
        # Genug Taler fÃƒÆ’Ã‚Â¼r alle?
        if self._get_total_resource(RESOURCE_TALER) < SERF_BUY_COST * count:
            return self._set_can_cache(cache_key, False)
        # Population-Limit erlaubt alle?
        village_capacity = self._get_total_village_capacity()
        if self.total_leibeigene + count > village_capacity:
            return self._set_can_cache(cache_key, False)
        # Max Leibeigene nicht ÃƒÆ’Ã‚Â¼berschritten?
        if self.total_leibeigene + count > MAX_POSSIBLE_LEIBEIGENE:
            return self._set_can_cache(cache_key, False)
        return self._set_can_cache(cache_key, True)

    def _can_dismiss_serf(self) -> bool:
        """Pr??ft ob ein Leibeigener entlassen werden kann."""
        cache_key = ("dismiss_serf",)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return cached
        return self._set_can_cache(cache_key, self.total_leibeigene > 0)

    def _can_dismiss_serf_batch(self, count: int) -> bool:
        """Pr??ft ob mehrere Leibeigene entlassen werden k??nnen."""
        cache_key = ("dismiss_serf_batch", count)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return cached
        return self._set_can_cache(cache_key, self.total_leibeigene >= count)

    def _can_dismiss_serf_from_area(self, area: SerfArea) -> bool:
        """Pr??ft ob in diesem Bereich ein Serf entlassen werden kann."""
        cache_key = ("dismiss_serf_area", area)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return cached
        if area == SerfArea.FREE:
            return self._set_can_cache(cache_key, self.free_leibeigene > 0)
        return self._set_can_cache(cache_key, self.serf_areas.get(area, {}).get("count", 0) > 0)

    def _can_demolish(self, building: str) -> bool:
        """PrÃƒÆ’Ã‚Â¼ft ob ein GebÃƒÆ’Ã‚Â¤ude abgerissen werden kann."""
        cache_key = ("can_demolish", building)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return bool(cached)

        # GebÃƒÆ’Ã‚Â¤ude muss existieren
        if self.buildings.get(building, 0) < 1:
            return self._set_can_cache(cache_key, False)
        if not self._get_building_instance_keys(building):
            return self._set_can_cache(cache_key, False)
        # HQ kann nicht abgerissen werden
        if "Hauptquartier" in building:
            return self._set_can_cache(cache_key, False)
        return self._set_can_cache(cache_key, True)

    def _can_bless(self, category: int = None) -> bool:
        """PrÃƒÆ’Ã‚Â¼ft ob Segnung mÃƒÆ’Ã‚Â¶glich ist.

        Args:
            category: Segen-Kategorie (0-4). Wenn None, prÃƒÆ’Ã‚Â¼ft allgemein.
        """
        # Kloster (Monastery) muss gebaut sein (nicht Kapelle!)
        total_monasteries = (self.buildings.get("Kloster_1", 0) +
                            self.buildings.get("Kloster_2", 0) +
                            self.buildings.get("Kloster_3", 0))
        if total_monasteries < 1:
            return False

        # Faith muss ausreichen (Tech-Boni beruecksichtigt)
        if self.faith < self._get_bless_required_faith():
            return False

        # Kategorie-spezifischer Cooldown
        if category is not None:
            if self.bless_cooldowns.get(category, 0) > 0:
                return False

        return True

    def _get_taler_income(self):
        income = 0
        for b_name, count in self.buildings.items():
            if count > 0:
                income += buildings_db.get(b_name, {}).get("taler_income", 0) * count
        return income

    def _get_taxable_worker_count(self) -> int:
        return int(len(self.workforce_manager.workers))

    def _get_taler_income_per_cycle(self) -> float:
        tax_info = TAX_LEVELS.get(self.current_tax_level, TAX_LEVELS[2])
        taxable_workers = float(self._get_taxable_worker_count())
        tax_income = float(tax_info["regular_tax"]) * taxable_workers
        tax_income *= float(self._get_tax_income_multiplier())
        building_income = float(self._get_taler_income()) * float(self._get_trade_income_multiplier())
        return float(max(0.0, tax_income + building_income))

    def _get_total_village_capacity(self) -> int:
        """Berechnet die maximale Arbeiter-KapazitÃƒÆ’Ã‚Â¤t aller Dorfzentren.
        Dies ist das HARTE LIMIT fÃƒÆ’Ã‚Â¼r die BevÃƒÆ’Ã‚Â¶lkerung!"""
        total = 0
        for vc_type, capacity in VILLAGE_CENTER_CAPACITY.items():
            total += self.buildings.get(vc_type, 0) * capacity
        return total

    def _get_total_farm_capacity(self) -> int:
        """Berechnet wie viele Arbeiter GLEICHZEITIG essen kÃƒÆ’Ã‚Â¶nnen.
        NUR fÃƒÆ’Ã‚Â¼r WorkTime-Regeneration, NICHT fÃƒÆ’Ã‚Â¼r BevÃƒÆ’Ã‚Â¶lkerungs-Limit!"""
        total = 0
        bonus = self._get_farm_capacity_bonus()
        for farm_type, capacity in FARM_EAT_CAPACITY.items():
            total += self.buildings.get(farm_type, 0) * (capacity + bonus)
        return total

    def _get_total_residence_capacity(self) -> int:
        """Berechnet wie viele Arbeiter GLEICHZEITIG ruhen kÃƒÆ’Ã‚Â¶nnen.
        NUR fÃƒÆ’Ã‚Â¼r WorkTime-Regeneration, NICHT fÃƒÆ’Ã‚Â¼r BevÃƒÆ’Ã‚Â¶lkerungs-Limit!"""
        total = 0
        bonus = self._get_residence_capacity_bonus()
        for res_type, capacity in RESIDENCE_CAPACITY.items():
            total += self.buildings.get(res_type, 0) * (capacity + bonus)
        return total

    def _sync_workforce_infrastructure(self):
        """Synchronisiert Farms/Residences/Camps mit dem WorkforceManager"""
        from worker_simulation import Position
        if not getattr(self, "_infrastructure_dirty", True):
            return

        # Helper: Position in Position-Objekt umwandeln
        def to_position(raw_pos):
            if isinstance(raw_pos, Position):
                return raw_pos
            elif isinstance(raw_pos, dict):
                return Position(x=raw_pos.get('x', 0), y=raw_pos.get('y', 0))
            elif isinstance(raw_pos, tuple):
                return Position(x=raw_pos[0], y=raw_pos[1])
            else:
                return Position(x=0, y=0)

        def positions_for_type(building_type: str):
            items = [
                (key, pos) for key, pos in self.building_position_map.items()
                if key.startswith(f"{building_type}_")
            ]
            items.sort(key=lambda kv: kv[0])
            return [pos for _, pos in items]

        # DORFZENTRUM-KAPAZITÃƒÆ’Ã¢â‚¬Å¾T setzen (bestimmt max. Arbeiter!)
        village_capacity = self._get_total_village_capacity()
        self.workforce_manager.set_village_capacity(village_capacity)

        # Tech-Boni fÃƒÆ’Ã‚Â¼r KapazitÃƒÆ’Ã‚Â¤ten
        farm_capacity_bonus = self._get_farm_capacity_bonus()
        residence_capacity_bonus = self._get_residence_capacity_bonus()

        # Farms synchronisieren (fÃƒÆ’Ã‚Â¼r Essen/WorkTime-Regeneration)
        self.workforce_manager.farms.clear()
        for farm_type in FARM_EAT_CAPACITY.keys():
            level = get_building_level(farm_type)
            for raw_pos in positions_for_type(farm_type):
                pos_obj = to_position(raw_pos)
                farm = Farm(position=pos_obj, level=level, capacity_bonus=farm_capacity_bonus)
                self.workforce_manager.farms.append(farm)

        # Residences synchronisieren
        self.workforce_manager.residences.clear()
        for res_type in RESIDENCE_CAPACITY.keys():
            level = get_building_level(res_type)
            for raw_pos in positions_for_type(res_type):
                pos_obj = to_position(raw_pos)
                residence = Residence(position=pos_obj, level=level, capacity_bonus=residence_capacity_bonus)
                self.workforce_manager.residences.append(residence)

        # Kein erzwungenes HQ-Camp: ohne explizite Camps campen Worker lokal am Arbeitsplatz.

        # Refiner-Supplier aktualisieren (Markt/HQ/Aussenposten oder Mine als Supplier)
        self._sync_refiner_suppliers()

        self._infrastructure_dirty = False

    def _get_active_workplaces(self) -> set:
        """Gibt aktive Arbeitsplatz-Positionen (fÃƒÆ’Ã‚Â¼r Jobloss-Logik)."""
        active = set()
        for key, pos in self.building_position_map.items():
            building_name = "_".join(key.split("_")[:-1])
            base = get_base_building_name(building_name)
            if base in BUILDING_WORKER_TYPES:
                active.add(_pos_key(pos))
        return active

    def _get_supplier_position(self, resource_type: ResourceType, consumer_pos) -> Position:
        """Waehlt den naechsten XML-konformen Supplier fuer die angeforderte Rohressource."""
        from worker_simulation import Position

        supplier_category_by_resource = {
            ResourceType.WOOD_RAW: "WoodSupplier",
            ResourceType.STONE_RAW: "StoneSupplier",
            ResourceType.CLAY_RAW: "ClaySupplier",
            ResourceType.IRON_RAW: "IronSupplier",
            ResourceType.SULFUR_RAW: "SulfurSupplier",
            ResourceType.GOLD_RAW: "GoldSupplier",
        }
        building_supplier_categories = {
            # PB_Headquarters* / PB_Outpost*
            "Hauptquartier": {
                "WoodSupplier", "StoneSupplier", "ClaySupplier",
                "IronSupplier", "SulfurSupplier", "GoldSupplier",
            },
            "Aussenposten": {
                "WoodSupplier", "StoneSupplier", "ClaySupplier",
                "IronSupplier", "SulfurSupplier", "GoldSupplier",
            },
            "Outpost": {
                "WoodSupplier", "StoneSupplier", "ClaySupplier",
                "IronSupplier", "SulfurSupplier", "GoldSupplier",
            },
            # PB_Market*
            "Markt": {
                "WoodSupplier", "StoneSupplier", "ClaySupplier",
                "IronSupplier", "SulfurSupplier", "GoldSupplier",
            },
            # PB_*Mine*
            "Steinmine": {"StoneSupplier"},
            "Lehmmine": {"ClaySupplier"},
            "Eisenmine": {"IronSupplier"},
            "Schwefelmine": {"SulfurSupplier"},
            "Goldmine": {"GoldSupplier"},
        }
        mine_bases = {"Steinmine", "Lehmmine", "Eisenmine", "Schwefelmine", "Goldmine"}

        def to_position(value) -> Position:
            if isinstance(value, Position):
                return Position(x=value.x, y=value.y)
            if isinstance(value, tuple):
                return Position(x=value[0], y=value[1])
            if isinstance(value, dict):
                return Position(x=value.get("x", 0), y=value.get("y", 0))
            return Position(x=0, y=0)

        c_pos = to_position(consumer_pos)
        required_category = supplier_category_by_resource.get(resource_type)

        candidate_positions: List[Position] = []
        if required_category:
            for key, pos in self.building_position_map.items():
                building_name = "_".join(key.split("_")[:-1])
                base = get_base_building_name(building_name)
                categories = building_supplier_categories.get(base, ())
                if required_category in categories:
                    candidate_positions.append(to_position(pos))

            # Runtime-Minen mitnehmen, falls building_position_map noch nicht synchron ist.
            mine_category_by_resource = {
                ResourceType.STONE_RAW: "StoneSupplier",
                ResourceType.CLAY_RAW: "ClaySupplier",
                ResourceType.IRON_RAW: "IronSupplier",
                ResourceType.SULFUR_RAW: "SulfurSupplier",
                ResourceType.GOLD_RAW: "GoldSupplier",
            }
            if hasattr(self, "production_system"):
                for mine in self.production_system.mines.values():
                    mine_category = mine_category_by_resource.get(mine.resource_type)
                    if mine_category == required_category:
                        candidate_positions.append(to_position(mine.position))

        if candidate_positions:
            return min(candidate_positions, key=lambda p: c_pos.distance_to(p))

        # Fallback: HQ-Position
        return to_position(self.hq_position)
    def _sync_refiner_suppliers(self):
        """Aktualisiert Supplier-Positionen aller Refiner."""
        if not hasattr(self, "production_system"):
            return
        for refiner in self.production_system.refiners.values():
            refiner.supplier_position = self._get_supplier_position(refiner.input_resource, refiner.position)
            _, dist = self._compute_path(refiner.position, refiner.supplier_position)
            refiner.path_distance = dist

    def _sync_refiner_path_distances(self):
        """Aktualisiert Pfad-Distanzen aller Refiner (ohne Supplier-Wechsel)."""
        if not hasattr(self, "production_system"):
            return
        for refiner in self.production_system.refiners.values():
            _, dist = self._compute_path(refiner.position, refiner.supplier_position)
            refiner.path_distance = dist

    def _get_routing_revision(self) -> int:
        """Revision fÃƒÆ’Ã‚Â¼r Repathing laufender Einheiten (nicht fÃƒÆ’Ã‚Â¼r jeden Cache-Invalidator)."""
        if not hasattr(self, "map_manager") or not self.map_manager:
            return 0
        grid = self.map_manager.grid
        return getattr(grid, "routing_revision", getattr(grid, "revision", 0))

    def _find_path_world(self, start_pos: Position, goal_pos: Position) -> List[Position]:
        """Berechnet einen Pfad in Welt-Koordinaten (A*)."""
        if int(round(start_pos.x)) == int(round(goal_pos.x)) and int(round(start_pos.y)) == int(round(goal_pos.y)):
            return [Position(x=goal_pos.x, y=goal_pos.y)]
        try:
            result = self.map_manager.find_path((start_pos.x, start_pos.y), (goal_pos.x, goal_pos.y))
        except Exception:
            return []
        if not result.found or not result.path:
            return []
        world_path: List[Position] = []
        for grid_pos in result.path:
            # Zellzentrum statt Zellkante fuer visuell/statisch sauberere Laufwege.
            local_world = (
                (grid_pos.x + 0.5) * pathfinding.SCALE_X,
                (grid_pos.y + 0.5) * pathfinding.SCALE_Y,
            )
            wx, wy = self.map_manager.to_world_coords(local_world[0], local_world[1])
            world_path.append(Position(x=wx, y=wy))
        return world_path

    def _compute_path(self, start_pos: Position, target_pos: Position) -> Tuple[List[Position], float]:
        """Berechnet Pfad + Distanz zwischen zwei Welt-Positionen."""
        grid_revision = getattr(self.map_manager.grid, "revision", 0)
        if getattr(self, "_path_cache_revision", None) != grid_revision:
            self._path_cache_revision = grid_revision
            self._path_cache = {}
        key = (
            int(round(start_pos.x)),
            int(round(start_pos.y)),
            int(round(target_pos.x)),
            int(round(target_pos.y)),
        )
        cached = self._path_cache.get(key)
        if cached is not None:
            return list(cached[0]), cached[1]

        path = self._find_path_world(start_pos, target_pos)
        if not path:
            # Kein valider A*-Pfad => Distanz unendlich (nicht Luftlinie erzwingen).
            dist = float("inf")
            self._path_cache[key] = ([], dist)
            return [], dist
        dist = 0.0
        for i in range(len(path) - 1):
            dist += path[i].distance_to(path[i + 1])
        self._path_cache[key] = (list(path), dist)
        return path, dist

    def _assign_serf_to_resource_pathing(self, serf: Serf, resource_type: ResourceType,
                                         target_pos: Position, start_pos: Position,
                                         tree_id: int = None):
        path, dist = self._compute_path(start_pos, target_pos)
        serf.assign_to_resource(resource_type, target_pos, start_pos, dist, tree_id, path=path)
        serf.path_revision = self._get_routing_revision()

    def _assign_serf_to_build(self, serf: Serf, building_name: str,
                              build_pos: Position, start_pos: Position,
                              site_id: int = None):
        path, _ = self._compute_path(start_pos, build_pos)
        serf.assign_to_build(building_name, build_pos, start_pos, site_id, path=path)
        serf.path_revision = self._get_routing_revision()

    def _prune_runtime_workers(self):
        """Entfernt verlassene Worker aus building_runtime."""
        if not self.building_runtime:
            return
        active_ids = {id(w) for w in self.workforce_manager.workers}
        for runtime in self.building_runtime.values():
            workers = runtime.get("workers")
            if not workers:
                continue
            runtime["workers"] = [w for w in workers if id(w) in active_ids]

    def _sync_workplace_worker_counts(self):
        """Synchronisiert Mine/Refiner-Worker-Zahlen mit echten Worker-Objekten."""
        if not hasattr(self, "production_system"):
            return
        mines_by_pos = {_pos_key(m.position): m for m in self.production_system.mines.values()}
        refiners_by_pos = {_pos_key(r.position): r for r in self.production_system.refiners.values()}
        for mine in self.production_system.mines.values():
            mine.current_workers = 0
            mine.efficiency_override = None
        for refiner in self.production_system.refiners.values():
            refiner.current_workers = 0
            refiner.efficiency_override = None
        mine_eff_sum: Dict[Tuple[int, int], float] = {}
        mine_eff_count: Dict[Tuple[int, int], int] = {}
        ref_eff_sum: Dict[Tuple[int, int], float] = {}
        ref_eff_count: Dict[Tuple[int, int], int] = {}
        for worker in self.workforce_manager.workers:
            if worker.state != WorkerState.WORKING:
                continue
            key = _pos_key(worker.workplace_position)
            mine = mines_by_pos.get(key)
            if mine and worker.worker_type == mine.worker_type:
                mine.current_workers += 1
                mine_eff_sum[key] = mine_eff_sum.get(key, 0.0) + worker.get_efficiency()
                mine_eff_count[key] = mine_eff_count.get(key, 0) + 1
                continue
            refiner = refiners_by_pos.get(key)
            if refiner and worker.worker_type == refiner.worker_type:
                refiner.current_workers += 1
                ref_eff_sum[key] = ref_eff_sum.get(key, 0.0) + worker.get_efficiency()
                ref_eff_count[key] = ref_eff_count.get(key, 0) + 1

        for mine in self.production_system.mines.values():
            key = _pos_key(mine.position)
            count = mine_eff_count.get(key, 0)
            if count > 0:
                mine.efficiency_override = mine_eff_sum.get(key, 0.0) / count

        for refiner in self.production_system.refiners.values():
            key = _pos_key(refiner.position)
            count = ref_eff_count.get(key, 0)
            if count > 0:
                refiner.efficiency_override = ref_eff_sum.get(key, 0.0) / count

    def _remove_one_worker_due_to_motivation(self):
        """Entfernt einen Worker bei sehr niedriger Motivation."""
        for worker in list(self.workforce_manager.workers):
            if worker.worker_type == "serf":
                continue
            self.workforce_manager.workers.remove(worker)
            for runtime in self.building_runtime.values():
                if worker in runtime.get("workers", []):
                    runtime["workers"].remove(worker)
            break

    def _get_legacy_action_mask(self):
        mask = np.zeros(self.total_actions, dtype=np.int8)
        mask[0] = 1  # Wait immer mÃƒÆ’Ã‚Â¶glich

        # =================================================================
        # GEBÃƒÆ’Ã¢â‚¬Å¾UDE-BATCH-BAU (1x, 3x, 5x pro GebÃƒÆ’Ã‚Â¤ude)
        # =================================================================
        for i, building in enumerate(self.buildable_buildings):
            for j, batch_size in enumerate(self.build_batch_sizes):
                action_idx = self.offset_build_batch + i * len(self.build_batch_sizes) + j
                if self._can_build_batch(building, batch_size):
                    mask[action_idx] = 1

        # Upgrades (unverÃƒÆ’Ã‚Â¤ndert)
        for i, building in enumerate(self.upgradeable_buildings):
            if self._can_upgrade(building):
                mask[self.offset_upgrade + i] = 1

        # Technologien (unverÃƒÆ’Ã‚Â¤ndert)
        for i, tech in enumerate(self.tech_list):
            if self._can_research(tech):
                mask[self.offset_tech + i] = 1

        # Soldaten (unverÃƒÆ’Ã‚Â¤ndert)
        for i, soldier in enumerate(self.soldier_types):
            if self._can_recruit(soldier):
                mask[self.offset_recruit + i] = 1

        # =================================================================
        # RESSOURCEN-BATCH-ACTIONS (1x, 3x, 5x)
        # =================================================================
        n_batch = len(self.resource_batch_sizes)
        offset = self.offset_resource_batch

        # Holz-Zonen: Zuweisen und Entfernen (6 Zonen ÃƒÆ’Ã¢â‚¬â€ 3 Batch ÃƒÆ’Ã¢â‚¬â€ 2)
        # Layout: [Zone0_assign_x1, Zone0_assign_x3, Zone0_assign_x5, Zone1_assign_x1, ...]
        for i, zone_name in enumerate(self.wood_zone_names):
            for j, batch_size in enumerate(self.resource_batch_sizes):
                if self._can_assign_wood_zone_batch(zone_name, batch_size):
                    mask[offset + i * n_batch + j] = 1
        offset += len(self.wood_zone_names) * n_batch

        # Entfernen aus Holz-Zonen
        for i, zone_name in enumerate(self.wood_zone_names):
            for j, batch_size in enumerate(self.resource_batch_sizes):
                if self._can_recall_wood_zone_batch(zone_name, batch_size):
                    mask[offset + i * n_batch + j] = 1
        offset += len(self.wood_zone_names) * n_batch

        # Vorkommen-Kategorien: Zuweisen und Entfernen
        for i, category in enumerate(self.deposit_category_names):
            for j, batch_size in enumerate(self.resource_batch_sizes):
                if self._can_assign_deposit_batch(category, batch_size):
                    mask[offset + i * n_batch + j] = 1
        offset += len(self.deposit_category_names) * n_batch

        for i, category in enumerate(self.deposit_category_names):
            for j, batch_size in enumerate(self.resource_batch_sizes):
                if self._can_recall_deposit_batch(category, batch_size):
                    mask[offset + i * n_batch + j] = 1
        offset += len(self.deposit_category_names) * n_batch

        # Stollen-Kategorien: Zuweisen und Entfernen (ersetzt alte Mine-Serf-Zuweisung)
        for i, shaft_type in enumerate(self.shaft_category_names):
            for j, batch_size in enumerate(self.resource_batch_sizes):
                if self._can_assign_shaft_batch(shaft_type, batch_size):
                    mask[offset + i * n_batch + j] = 1
        offset += len(self.shaft_category_names) * n_batch

        for i, shaft_type in enumerate(self.shaft_category_names):
            for j, batch_size in enumerate(self.resource_batch_sizes):
                if self._can_recall_shaft_batch(shaft_type, batch_size):
                    mask[offset + i * n_batch + j] = 1

        # Leibeigene kaufen/entlassen (Batch-Actions: 1x, 3x, 5x)
        for i, batch_size in enumerate(self.serf_batch_sizes):
            if self._can_buy_serf_batch(batch_size):
                mask[self.offset_serf + i] = 1
            if self._can_dismiss_serf_batch(batch_size):
                mask[self.offset_serf + len(self.serf_batch_sizes) + i] = 1

        # Batch-Rekrutierung fÃƒÆ’Ã‚Â¼r ScharfschÃƒÆ’Ã‚Â¼tzen (3x, 5x)
        action_idx = 0
        for soldier_type in self.scharfschuetzen_types:
            for batch_size in self.scharfschuetzen_batch_sizes:
                if self._can_recruit_batch(soldier_type, batch_size):
                    mask[self.offset_batch_recruit + action_idx] = 1
                action_idx += 1

        # GebÃƒÆ’Ã‚Â¤ude abreiÃƒÆ’Ã…Â¸en
        for i, building in enumerate(self.demolishable_buildings):
            if self._can_demolish(building):
                mask[self.offset_demolish + i] = 1

        # Segnen (5 Kategorien)
        for cat in BLESS_CATEGORIES:
            if self._can_bless(cat):
                mask[self.offset_bless + cat] = 1

        # Steuern (immer mÃƒÆ’Ã‚Â¶glich, auÃƒÆ’Ã…Â¸er aktuelles Level)
        for i in range(len(TAX_LEVELS)):
            if i != self.current_tax_level:
                mask[self.offset_tax + i] = 1

        # Alarm (AN wenn aus und kein Cooldown, AUS wenn an)
        if not self.alarm_active and self.alarm_cooldown <= 0:
            mask[self.offset_alarm] = 1
        if self.alarm_active:
            mask[self.offset_alarm + 1] = 1

        # NEU: Bau-Serfs zuweisen/zurÃƒÆ’Ã‚Â¼ckrufen
        for i, batch_size in enumerate(self.build_serf_batch_sizes):
            # Zuweisen mÃƒÆ’Ã‚Â¶glich wenn freie Serfs und Baustellen vorhanden
            if self._can_assign_build_batch(batch_size):
                mask[self.offset_build_serf + i] = 1
            # ZurÃƒÆ’Ã‚Â¼ckrufen mÃƒÆ’Ã‚Â¶glich wenn Serfs auf Baustellen arbeiten
            if self._can_recall_build_batch(batch_size):
                mask[self.offset_build_serf + len(self.build_serf_batch_sizes) + i] = 1

        return mask

    def get_action_mask(self):
        """KompatibilitÃƒÆ’Ã‚Â¤ts-Wrapper fÃƒÆ’Ã‚Â¼r MaskablePPO (Multi-Step Maske)."""
        return self.action_masks()

    def _get_placement_cache_signature(self):
        """Signatur fÃƒÆ’Ã‚Â¼r Bauplatz-Cache (nur gebÃƒÆ’Ã‚Â¤uderelevante ÃƒÆ’Ã¢â‚¬Å¾nderungen)."""
        grid_revision = 0
        if hasattr(self, "map_manager") and self.map_manager and hasattr(self.map_manager, "grid"):
            grid_revision = int(getattr(self.map_manager.grid, "revision", 0))
        return (
            getattr(self, "_building_block_revision", 0),
            len(self.available_positions),
            len(self.zone_b_positions),
            len(self.building_position_map),
            len(self.construction_sites),
            grid_revision,
        )

    def _normalize_building_name(self, value: str) -> str:
        text = str(value)
        replacements = {
            "ÃƒÆ’Ã‚Â¼": "Ã¼",
            "ÃƒÂ¼": "Ã¼",
            "ÃƒÆ’Ã‚Â¶": "Ã¶",
            "ÃƒÂ¶": "Ã¶",
            "ÃƒÆ’Ã‚Â¤": "Ã¤",
            "ÃƒÂ¤": "Ã¤",
            "ÃƒÆ’Ã…Â¸": "ÃŸ",
            "ÃƒÅ¸": "ÃŸ",
        }
        for bad, good in replacements.items():
            text = text.replace(bad, good)
        for _ in range(3):
            try:
                repaired = text.encode("latin1").decode("utf-8")
            except Exception:
                break
            if not repaired or repaired == text:
                break
            text = repaired
        text = unicodedata.normalize("NFKD", text)
        text = "".join(ch for ch in text if not unicodedata.combining(ch))
        text = text.replace("ÃŸ", "ss").lower()
        return "".join(ch for ch in text if ch.isalnum() or ch == "_")

    def _is_building_forbidden_by_rules(self, building: str) -> bool:
        base_name = get_base_building_name(building)
        norm_base = self._normalize_building_name(base_name)
        for forbidden in GAME_RULES.get("forbidden", []):
            if self._normalize_building_name(forbidden) == norm_base:
                return True
        return False

    def _get_build_anchor_positions(self, building: str) -> List[Tuple[float, float]]:
        """Liefert priorisierte Ankerpositionen fÃƒÆ’Ã‚Â¼r Platzierungssuche."""
        hq_anchor = (float(self.hq_position[0]), float(self.hq_position[1]))
        base_name = get_base_building_name(building)
        norm = self._normalize_building_name(base_name)

        # GebÃƒÆ’Ã‚Â¤ude, die bevorzugt bei ihren Minen platziert werden.
        mine_anchor_map = {
            "lehmhutte": "Lehmmine",
            "steinmetzhutte": "Steinmine",
            "alchimistenhutte": "Schwefelmine",
            "schmiede": "Eisenmine",
            "buchsenmacherei": "Eisenmine",
            "kanongiesserei": "Schwefelmine",
        }

        anchors: List[Tuple[float, float]] = []
        mine_type = mine_anchor_map.get(norm)
        if mine_type:
            mine_positions = self.built_mines.get(mine_type, []) or self.mine_positions.get(mine_type, [])
            for pos in mine_positions:
                if isinstance(pos, dict):
                    anchors.append((float(pos.get("x", 0.0)), float(pos.get("y", 0.0))))
                elif isinstance(pos, tuple):
                    anchors.append((float(pos[0]), float(pos[1])))

        # Dorfzentren bevorzugt auf Slots, sonst HQ-NÃƒÆ’Ã‚Â¤he.
        if norm == "dorfzentrum":
            for slot in self.dz_slots:
                if slot.get("status") == "free":
                    anchors.append((float(slot.get("x", 0.0)), float(slot.get("y", 0.0))))

        anchors.append(hq_anchor)

        # Duplikate entfernen, Reihenfolge erhalten.
        unique: List[Tuple[float, float]] = []
        seen = set()
        for ax, ay in anchors:
            key = (int(round(ax)), int(round(ay)))
            if key in seen:
                continue
            seen.add(key)
            unique.append((ax, ay))
        return unique or [hq_anchor]

    def _find_candidate_build_positions(self, building: str, limit: int = 1) -> List[dict]:
        """Sucht freie Baupositionen (Slots zuerst, dann dynamisch auf ganz P1)."""
        if limit <= 0:
            return []

        signature = self._get_placement_cache_signature()
        if getattr(self, "_placement_cache_signature", None) != signature:
            self._placement_cache_signature = signature
            self._placement_cache = {}

        cache_key = ("positions", building, int(limit))
        cached = self._placement_cache.get(cache_key)
        if cached is not None:
            return [
                {"x": int(px), "y": int(py), "_slot_candidate": bool(slot_flag)}
                for px, py, slot_flag in cached
            ]

        anchor_positions = self._get_build_anchor_positions(building)
        primary_anchor = anchor_positions[0]
        placements: List[dict] = []
        reserved: List[Tuple[float, float, str]] = []
        seen = set()

        def _try_add(px: float, py: float, slot_candidate: bool) -> bool:
            key = (int(round(px)), int(round(py)))
            if key in seen:
                return False
            if not self._is_position_free(key[0], key[1], building, extra_reserved=reserved):
                return False
            seen.add(key)
            placements.append(
                {
                    "x": key[0],
                    "y": key[1],
                    "_slot_candidate": bool(slot_candidate),
                }
            )
            reserved.append((key[0], key[1], building))
            return True

        # 1) Erst bekannte Slot-Kandidaten (nahe am PrimÃƒÆ’Ã‚Â¤r-Anker).
        slot_candidates = []
        for pos in self.available_positions:
            if isinstance(pos, dict):
                px, py = pos.get("x", 0), pos.get("y", 0)
            else:
                px, py = pos[0], pos[1]
            dist = abs(px - primary_anchor[0]) + abs(py - primary_anchor[1])
            slot_candidates.append((dist, float(px), float(py)))
        slot_candidates.sort(key=lambda item: item[0])

        for _, px, py in slot_candidates:
            _try_add(px, py, slot_candidate=True)
            if len(placements) >= limit:
                break

        # 2) Falls nÃƒÆ’Ã‚Â¶tig: dynamische Suche ÃƒÆ’Ã‚Â¼ber das Walkable-Grid auf ganz P1.
        if len(placements) < limit and hasattr(self, "map_manager") and self.map_manager:
            base_name = get_base_building_name(building)
            search_radius = (max(MAP_SIZE[0], MAP_SIZE[1]) / 2.0) + 2000.0
            max_results = max(40, limit * 24)
            for anchor_x, anchor_y in anchor_positions:
                local_x, local_y = self.map_manager.to_local_coords(anchor_x, anchor_y)
                dynamic_positions = self.map_manager.grid.find_valid_building_positions(
                    base_name,
                    local_x,
                    local_y,
                    search_radius=search_radius,
                    max_results=max_results,
                )
                for local_pos_x, local_pos_y, _ in dynamic_positions:
                    world_x, world_y = self.map_manager.to_world_coords(local_pos_x, local_pos_y)
                    _try_add(world_x, world_y, slot_candidate=False)
                    if len(placements) >= limit:
                        break
                if len(placements) >= limit:
                    break

        self._placement_cache[cache_key] = [
            (int(p["x"]), int(p["y"]), bool(p.get("_slot_candidate", False)))
            for p in placements
        ]
        return placements

    def _count_free_build_positions(self, building: str, limit: int = 1) -> int:
        """ZÃƒÆ’Ã‚Â¤hlt freie Positionen fÃƒÆ’Ã‚Â¼r building bis max. limit (persistent gecached)."""
        if limit <= 0:
            return 0

        signature = self._get_placement_cache_signature()
        if getattr(self, "_placement_cache_signature", None) != signature:
            self._placement_cache_signature = signature
            self._placement_cache = {}

        cache_key = (building, int(limit))
        cached = self._placement_cache.get(cache_key)
        if cached is not None:
            return cached

        free_count = len(self._find_candidate_build_positions(building, limit=limit))
        self._placement_cache[cache_key] = free_count
        return free_count

    def _can_build(self, building):
        if getattr(self, "_build_check_cache_time", None) != self.current_time:
            self._build_check_cache_time = self.current_time
            self._build_check_cache = {}
            self._build_batch_cache = {}
        if building in self._build_check_cache:
            return self._build_check_cache[building]

        b_info = buildings_db.get(building)
        if not b_info:
            self._build_check_cache[building] = False
            return False

        for resource, amount in b_info["cost"].items():
            if self._get_total_resource(resource) < amount:
                self._build_check_cache[building] = False
                return False

        tech_req = b_info.get("tech_required")
        if tech_req and tech_req not in self.researched_techs:
            self._build_check_cache[building] = False
            return False

        base_name = get_base_building_name(building)
        if self._is_building_forbidden_by_rules(building):
            self._build_check_cache[building] = False
            return False

        if b_info.get("mine_type"):
            mine_type = b_info["mine_type"]
            available = self.mine_positions.get(mine_type, [])
            built = len(self.built_mines.get(mine_type, []))
            if built >= len(available):
                self._build_check_cache[building] = False
                return False
        elif base_name == "Dorfzentrum":
            # DZ: Nur an freien DZ-Slots
            if not any(s.get("status") == "free" for s in self.dz_slots):
                self._build_check_cache[building] = False
                return False
        else:
            # Normale GebÃƒÆ’Ã‚Â¤ude: PlatzprÃƒÆ’Ã‚Â¼fung ÃƒÆ’Ã‚Â¼ber persistenten Positions-Cache
            if self._count_free_build_positions(building, limit=1) <= 0:
                self._build_check_cache[building] = False
                return False

        self._build_check_cache[building] = True
        return True

    def _can_build_batch(self, building: str, batch_size: int) -> bool:
        """Pr??ft ob batch_size Geb??ude gebaut werden k??nnen."""
        if getattr(self, "_build_check_cache_time", None) != self.current_time:
            self._build_check_cache_time = self.current_time
            self._build_check_cache = {}
            self._build_batch_cache = {}
        cache_key = (building, batch_size)
        if cache_key in self._build_batch_cache:
            return self._build_batch_cache[cache_key]

        b_info = buildings_db.get(building)
        if not b_info:
            self._build_batch_cache[cache_key] = False
            return False

        # Ressourcen f??r alle Geb??ude pr??fen
        for resource, amount in b_info["cost"].items():
            if self._get_total_resource(resource) < amount * batch_size:
                self._build_batch_cache[cache_key] = False
                return False

        # Tech-Voraussetzung pr??fen
        tech_req = b_info.get("tech_required")
        if tech_req and tech_req not in self.researched_techs:
            self._build_batch_cache[cache_key] = False
            return False

        # Positionen pr??fen
        if b_info.get("mine_type"):
            mine_type = b_info["mine_type"]
            available = self.mine_positions.get(mine_type, [])
            built = len(self.built_mines.get(mine_type, []))
            if built + batch_size > len(available):
                self._build_batch_cache[cache_key] = False
                return False
        elif get_base_building_name(building) == "Dorfzentrum":
            free_slots = sum(1 for s in self.dz_slots if s.get("status") == "free")
            if free_slots < batch_size:
                self._build_batch_cache[cache_key] = False
                return False
        else:
            free_count = self._count_free_build_positions(building, limit=batch_size)
            if free_count < batch_size:
                self._build_batch_cache[cache_key] = False
                return False

        self._build_batch_cache[cache_key] = True
        return True


    def _can_upgrade(self, building):
        cache_key = ("can_upgrade", building)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return bool(cached)

        if self.buildings.get(building, 0) < 1:
            return self._set_can_cache(cache_key, False)
        if not self._get_building_instance_keys(building):
            return self._set_can_cache(cache_key, False)

        b_info = buildings_db.get(building)
        if not b_info or not b_info.get("upgrade_to"):
            return self._set_can_cache(cache_key, False)

        for resource, amount in b_info.get("upgrade_cost", {}).items():
            if self._get_total_resource(resource) < amount:
                return self._set_can_cache(cache_key, False)

        return self._set_can_cache(cache_key, True)

    def _can_research(self, tech):
        if getattr(self, "_research_check_cache_time", None) != self.current_time:
            self._research_check_cache_time = self.current_time
            self._research_check_cache = {}
            self._research_any_cache = None
        if tech in self._research_check_cache:
            return self._research_check_cache[tech]

        if tech in self.researched_techs:
            self._research_check_cache[tech] = False
            return False
        # Parallelforschung: Slots = Anzahl Hochschulen
        max_slots = self.buildings.get("Hochschule_1", 0) + self.buildings.get("Hochschule_2", 0)
        if len(self.current_researches) >= max_slots:
            self._research_check_cache[tech] = False
            return False

        tech_info = technologies.get(tech)
        if not tech_info:
            self._research_check_cache[tech] = False
            return False
        if tech_info.get("disabled"):
            self._research_check_cache[tech] = False
            return False

        for resource, amount in tech_info["cost"].items():
            if self._get_total_resource(resource) < amount:
                self._research_check_cache[tech] = False
                return False

        for req_tech in tech_info.get("tech_required", []):
            if req_tech not in self.researched_techs:
                self._research_check_cache[tech] = False
                return False

        entity_conditions = tech_info.get("entity_conditions", [])
        if entity_conditions:
            required = tech_info.get("required_entity_conditions")
            if required is None:
                required = len(entity_conditions)
            satisfied = 0
            for cond in entity_conditions:
                b_name = cond.get("building")
                amount = cond.get("amount", 1)
                if b_name and self.buildings.get(b_name, 0) >= amount:
                    satisfied += 1
            if satisfied < required:
                self._research_check_cache[tech] = False
                return False
        else:
            req_building = tech_info.get("requires_building")
            if req_building and self.buildings.get(req_building, 0) < 1:
                self._research_check_cache[tech] = False
                return False

        # Forschung nur moeglich, wenn das passende Forschungsgebaeude existiert.
        # Falls keine Zuordnung vorhanden ist, faellt es auf Hochschule zurueck.
        research_buildings = tech_info.get("research_buildings")
        if not research_buildings:
            req = tech_info.get("research_building") or tech_info.get("requires_building")
            if req:
                research_buildings = [req]
            else:
                research_buildings = ["Hochschule"]
        has_research_building = False
        for rb in research_buildings:
            base = re.sub(r'_\d+$', '', rb)
            if any(self.buildings.get(b, 0) > 0 for b in self.buildings if get_base_building_name(b) == base):
                has_research_building = True
                break
        if not has_research_building:
            self._research_check_cache[tech] = False
            return False

        self._research_check_cache[tech] = True
        return True

    def _can_research_any(self) -> bool:
        if getattr(self, "_research_check_cache_time", None) != self.current_time:
            self._research_check_cache_time = self.current_time
            self._research_check_cache = {}
            self._research_any_cache = None
        if self._research_any_cache is not None:
            return self._research_any_cache
        for tech in self.tech_list:
            if self._can_research(tech):
                self._research_any_cache = True
                return True
        self._research_any_cache = False
        return False

    def _can_recruit(self, soldier):
        cache_key = ("recruit", soldier)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return cached

        s_info = soldiers_db.get(soldier)
        if not s_info:
            return self._set_can_cache(cache_key, False)
        # VillageCenterLockThreshold: Unter 0.3 Motivation keine neuen Soldaten!
        if self._get_total_motivation() < VILLAGE_CENTER_LOCK_THRESHOLD:
            return self._set_can_cache(cache_key, False)

        for resource, amount in s_info["cost"].items():
            if self._get_total_resource(resource) < amount:
                return self._set_can_cache(cache_key, False)

        for req in s_info.get("requirements", []):
            if req in buildings_db:
                if self.buildings.get(req, 0) < 1:
                    return self._set_can_cache(cache_key, False)
            elif req in technologies:
                if req not in self.researched_techs:
                    return self._set_can_cache(cache_key, False)

        unit_rules = GAME_RULES.get("units", {})
        base_name = get_base_building_name(soldier)
        if base_name in unit_rules and unit_rules[base_name] == 0:
            return self._set_can_cache(cache_key, False)

        return self._set_can_cache(cache_key, True)

    def _can_recruit_batch(self, soldier: str, count: int) -> bool:
        """PrÃƒÆ’Ã‚Â¼ft ob mehrere Soldaten gleichzeitig rekrutiert werden kÃƒÆ’Ã‚Â¶nnen."""
        cache_key = ("recruit_batch", soldier, count)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return cached
        s_info = soldiers_db.get(soldier)
        if not s_info:
            return self._set_can_cache(cache_key, False)

        # Genug Ressourcen fÃƒÆ’Ã‚Â¼r alle?
        for resource, amount in s_info["cost"].items():
            if self._get_total_resource(resource) < amount * count:
                return self._set_can_cache(cache_key, False)

        # Requirements erfÃƒÆ’Ã‚Â¼llt?
        for req in s_info.get("requirements", []):
            if req in buildings_db:
                if self.buildings.get(req, 0) < 1:
                    return self._set_can_cache(cache_key, False)
            elif req in technologies:
                if req not in self.researched_techs:
                    return self._set_can_cache(cache_key, False)

        # Unit Rules prÃƒÆ’Ã‚Â¼fen
        unit_rules = GAME_RULES.get("units", {})
        base_name = get_base_building_name(soldier)
        if base_name in unit_rules and unit_rules[base_name] == 0:
            return self._set_can_cache(cache_key, False)

        return self._set_can_cache(cache_key, True)

    def _can_assign_worker_to_resource(self, resource: str) -> bool:
        """
        PrÃƒÆ’Ã‚Â¼ft ob ein Leibeigener einer Ressource zugewiesen werden kann.

        Regeln:
        - Ressource muss INNERHALB des ResourceSearchRadius (4500) liegen!
        - Holz: BÃƒÆ’Ã‚Â¤ume mÃƒÆ’Ã‚Â¼ssen verfÃƒÆ’Ã‚Â¼gbar sein
        - Minen-Ressourcen (Stein, Lehm, Eisen, Schwefel):
          ENTWEDER eine Mine ist gebaut ODER kleine Vorkommen sind verfÃƒÆ’Ã‚Â¼gbar

        Returns:
            True wenn Ressource gesammelt werden kann
        """
        # NEU: PrÃƒÆ’Ã‚Â¼fe ob _get_resource_collection_position eine Position findet
        # Diese Methode berÃƒÆ’Ã‚Â¼cksichtigt bereits den ResourceSearchRadius!
        target_pos = self._get_resource_collection_position(resource)
        return target_pos is not None

    def _get_resource_collection_position(self, resource: str):
        """
        Gibt die beste Position fÃƒÆ’Ã‚Â¼r Ressourcensammlung zurÃƒÆ’Ã‚Â¼ck.

        PrioritÃƒÆ’Ã‚Â¤t:
        1. Gebaute Mine (unbegrenzte KapazitÃƒÆ’Ã‚Â¤t)
        2. Kleine Vorkommen (bis erschÃƒÆ’Ã‚Â¶pft)
        3. BÃƒÆ’Ã‚Â¤ume (fÃƒÆ’Ã‚Â¼r Holz)

        NEU: BerÃƒÆ’Ã‚Â¼cksichtigt ResourceSearchRadius (4500) aus PU_Serf.xml
        Serfs suchen nur Ressourcen innerhalb dieses Radius!

        Returns:
            Position oder None
        """
        from worker_simulation import Position
        from production_system import SERF_RESOURCE_SEARCH_RADIUS
        import math

        # HQ als Referenzpunkt fÃƒÆ’Ã‚Â¼r Distanz-Berechnung
        hq_x, hq_y = self.hq_position
        radius = self._get_effective_serf_resource_search_radius()

        def is_in_search_radius(x, y) -> bool:
            """PrÃƒÆ’Ã‚Â¼ft ob Position innerhalb des Serf-Suchradius liegt."""
            dist = math.sqrt((x - hq_x)**2 + (y - hq_y)**2)
            return dist <= radius

        if resource in (RESOURCE_HOLZ, RESOURCE_HOLZ_ROH):
            # NÃƒÆ’Ã‚Â¤chster verfÃƒÆ’Ã‚Â¼gbarer Baum INNERHALB des Suchradius
            for tree in self.trees_list:
                if is_in_search_radius(tree["x"], tree["y"]):
                    return Position(x=tree["x"], y=tree["y"])
            return None

        mine_type_map = {
            RESOURCE_STEIN: "Steinmine",
            RESOURCE_LEHM: "Lehmmine",
            RESOURCE_EISEN: "Eisenmine",
            RESOURCE_SCHWEFEL: "Schwefelmine",
            RESOURCE_STEIN_ROH: "Steinmine",
            RESOURCE_LEHM_ROH: "Lehmmine",
            RESOURCE_EISEN_ROH: "Eisenmine",
            RESOURCE_SCHWEFEL_ROH: "Schwefelmine",
        }

        mine_type = mine_type_map.get(resource)

        # PrioritÃƒÆ’Ã‚Â¤t 1: Gebaute Mine (innerhalb Suchradius)
        built = self.built_mines.get(mine_type, [])
        for pos in built:
            if is_in_search_radius(pos["x"], pos["y"]):
                return Position(x=pos["x"], y=pos["y"])

        # PrioritÃƒÆ’Ã‚Â¤t 2: Kleine Vorkommen (innerhalb Suchradius)
        # Raw-Namen auf raffinierte Kategorien abbilden
        raw_to_refined = {
            RESOURCE_STEIN_ROH: RESOURCE_STEIN,
            RESOURCE_LEHM_ROH: RESOURCE_LEHM,
            RESOURCE_EISEN_ROH: RESOURCE_EISEN,
            RESOURCE_SCHWEFEL_ROH: RESOURCE_SCHWEFEL,
        }
        refined_key = raw_to_refined.get(resource, resource)
        deposits = self.small_deposits.get(refined_key, [])
        for deposit in deposits:
            if deposit.get("remaining", 0) > 0:
                if is_in_search_radius(deposit["x"], deposit["y"]):
                    return Position(x=deposit["x"], y=deposit["y"])

        return None

    def _assign_serf_to_resource(self, resource: str):
        """
        Weist einen freien Serf einer Ressource zu.
        Der Serf lÃƒÆ’Ã‚Â¤uft zur Ressource und bleibt dort.

        NEU: Verwendet A* Pfadfindung fÃƒÆ’Ã‚Â¼r exakte Laufwege!
        HOLZ: Baum wird aus trees_list entfernt (reserviert)
        """
        from worker_simulation import Position
        from production_system import ResourceType, SerfState

        # Finde einen freien (IDLE) Serf
        idle_serf = None
        for serf in self.production_system.serfs:
            if serf.is_idle():
                idle_serf = serf
                break

        if not idle_serf:
            return  # Kein freier Serf

        # Konvertiere Ressourcen-Name zu ResourceType
        resource_type_map = {
            RESOURCE_HOLZ: ResourceType.WOOD_RAW,
            RESOURCE_STEIN: ResourceType.STONE_RAW,
            RESOURCE_LEHM: ResourceType.CLAY_RAW,
            RESOURCE_EISEN: ResourceType.IRON_RAW,
            RESOURCE_SCHWEFEL: ResourceType.SULFUR_RAW,
            RESOURCE_HOLZ_ROH: ResourceType.WOOD_RAW,
            RESOURCE_STEIN_ROH: ResourceType.STONE_RAW,
            RESOURCE_LEHM_ROH: ResourceType.CLAY_RAW,
            RESOURCE_EISEN_ROH: ResourceType.IRON_RAW,
            RESOURCE_SCHWEFEL_ROH: ResourceType.SULFUR_RAW,
        }
        resource_type = resource_type_map.get(resource)
        if not resource_type:
            return

        # Hole Position der Ressource und ggf. tree_id
        tree_id = None
        if resource in (RESOURCE_HOLZ, RESOURCE_HOLZ_ROH):
            # Holz: Baum aus Liste nehmen und reservieren
            if not self.trees_list:
                return
            tree = self.trees_list.pop(0)  # Ersten Baum nehmen und entfernen
            self.available_trees -= 1
            target_pos = Position(x=tree["x"], y=tree["y"])

            # Tree-ID fÃƒÆ’Ã‚Â¼r MapManager ermitteln
            nearest = self.map_manager.get_nearest_tree(tree["x"], tree["y"])
            if nearest:
                tree_id = nearest[0]
        else:
            target_pos = self._get_resource_collection_position(resource)
            if not target_pos:
                return

        # Aktuelle Serf-Position als Startpunkt (kein Teleport zum HQ)
        start_pos = Position(x=idle_serf.position.x, y=idle_serf.position.y)

        # Serf zur Ressource schicken mit korrektem Pfad und tree_id
        self._assign_serf_to_resource_pathing(idle_serf, resource_type, target_pos, start_pos, tree_id)

    def _recall_serf_from_resource(self, resource: str):
        """
        Ruft einen Serf von einer Ressource zurÃƒÆ’Ã‚Â¼ck.
        Der Serf wird auf IDLE gesetzt.
        (Legacy-Funktion - nicht mehr direkt verwendet)
        """
        from production_system import ResourceType

        # Konvertiere Ressourcen-Name zu ResourceType
        resource_type_map = {
            RESOURCE_HOLZ: ResourceType.WOOD_RAW,
            RESOURCE_STEIN: ResourceType.STONE_RAW,
            RESOURCE_LEHM: ResourceType.CLAY_RAW,
            RESOURCE_EISEN: ResourceType.IRON_RAW,
            RESOURCE_SCHWEFEL: ResourceType.SULFUR_RAW,
            RESOURCE_HOLZ_ROH: ResourceType.WOOD_RAW,
            RESOURCE_STEIN_ROH: ResourceType.STONE_RAW,
            RESOURCE_LEHM_ROH: ResourceType.CLAY_RAW,
            RESOURCE_EISEN_ROH: ResourceType.IRON_RAW,
            RESOURCE_SCHWEFEL_ROH: ResourceType.SULFUR_RAW,
        }
        resource_type = resource_type_map.get(resource)
        if not resource_type:
            return

        # Finde einen Serf der diese Ressource sammelt
        for serf in self.production_system.serfs:
            if serf.target_resource == resource_type and not serf.is_idle():
                serf.stop()
                return

    # =================================================================
    # NEU: POSITIONSBASIERTE SERF-ZUWEISUNG
    # Jeder Leibeigene wird einer SPEZIFISCHEN Position zugewiesen!
    # =================================================================

    # =================================================================
    # VEREINFACHTES BATCH-SYSTEM (ohne Serf-IDs)
    # Agent wÃƒÆ’Ã‚Â¤hlt: WAS + WIEVIELE (1, 3, 5)
    # =================================================================

    # --- HOLZ (BÃƒÆ’Ã‚Â¤ume) ---
    def _can_assign_wood_batch(self, batch_size: int) -> bool:
        """PrÃƒÆ’Ã‚Â¼ft ob batch_size Serfs zu BÃƒÆ’Ã‚Â¤umen zugewiesen werden kÃƒÆ’Ã‚Â¶nnen."""
        if self.free_leibeigene < batch_size:
            return False
        # Mindestens ein Baum mit verfÃƒÆ’Ã‚Â¼gbarer ArbeitskapazitÃƒÆ’Ã‚Â¤t.
        available = sum(
            1 for t in self.tree_list_internal
            if t["resource_remaining"] > 0 and t.get("serfs_assigned", 0) < MAX_SERFS_PER_TREE
        )
        return available > 0  # Mindestens 1 Baum muss verfÃƒÆ’Ã‚Â¼gbar sein

    def _can_recall_wood_batch(self, batch_size: int) -> bool:
        """PrÃƒÆ’Ã‚Â¼ft ob batch_size Serfs von Holz-Arbeit zurÃƒÆ’Ã‚Â¼ckgerufen werden kÃƒÆ’Ã‚Â¶nnen."""
        return self.wood_serfs >= batch_size

    def _assign_wood_batch(self, batch_size: int):
        """Weist batch_size Serfs zum Holzsammeln zu."""
        from worker_simulation import Position
        from production_system import ResourceType

        available_trees = [
            t for t in self.tree_list_internal
            if t["resource_remaining"] > 0 and t.get("serfs_assigned", 0) < MAX_SERFS_PER_TREE
        ]
        if not available_trees:
            return

        assigned = 0
        tree_idx = 0
        for serf in self.production_system.serfs:
            if assigned >= batch_size:
                break
            if serf.is_idle():
                chosen_tree = None
                checked = 0
                while checked < len(available_trees):
                    tree = available_trees[tree_idx % len(available_trees)]
                    tree_idx += 1
                    checked += 1
                    if tree["resource_remaining"] > 0 and tree.get("serfs_assigned", 0) < MAX_SERFS_PER_TREE:
                        chosen_tree = tree
                        break

                if not chosen_tree:
                    break

                # Serf zuweisen (vereinfacht, ohne ID-Tracking)
                target_pos = Position(x=chosen_tree["x"], y=chosen_tree["y"])
                start_pos = Position(x=serf.position.x, y=serf.position.y)
                self._assign_serf_to_resource_pathing(serf, ResourceType.WOOD_RAW, target_pos, start_pos)
                serf.work_location = "wood"  # Markiere als Holz-Serf
                chosen_tree["serfs_assigned"] += 1
                assigned += 1

        self.wood_serfs += assigned
        self.free_leibeigene -= assigned
        self.resource_workers[RESOURCE_HOLZ_ROH] = self.resource_workers.get(RESOURCE_HOLZ_ROH, 0) + assigned

    def _recall_wood_batch(self, batch_size: int):
        """Ruft batch_size Serfs vom Holzsammeln zurÃƒÆ’Ã‚Â¼ck."""
        recalled = 0
        for serf in self.production_system.serfs:
            if recalled >= batch_size:
                break
            # Konsistenz: PrÃƒÆ’Ã‚Â¼fe auch work_location
            if (serf.target_resource and
                serf.target_resource.value == "wood_raw" and
                serf.work_location == "wood"):
                serf.stop()
                recalled += 1

        self.wood_serfs = max(0, self.wood_serfs - recalled)
        self.free_leibeigene += recalled
        self.resource_workers[RESOURCE_HOLZ_ROH] = max(0, self.resource_workers.get(RESOURCE_HOLZ_ROH, 0) - recalled)

    # --- HOLZ-ZONEN (strategische Bauplatz-Schaffung) ---
    def _can_assign_wood_zone_batch(self, zone_name: str, batch_size: int) -> bool:
        """
        PrÃƒÆ’Ã‚Â¼ft ob batch_size Serfs zu einer Holz-Zone zugewiesen werden kÃƒÆ’Ã‚Â¶nnen.
        Jede Zone muss fÃƒÆ’Ã‚Â¼r bestimmte Raffinerie-GebÃƒÆ’Ã‚Â¤ude gerodet werden.
        """
        cache_key = ("assign_wood_zone", zone_name, batch_size)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return cached
        if zone_name not in self.wood_zone_categories:
            return self._set_can_cache(cache_key, False)
        if self.free_leibeigene < batch_size:
            return self._set_can_cache(cache_key, False)
        # Mindestens 1 Baum mit Ressourcen + freiem Serf-Slot in dieser Zone.
        zone_data = self.wood_zone_categories[zone_name]
        return self._set_can_cache(
            cache_key,
            any(
                t["resource_remaining"] > 0 and t.get("serfs_assigned", 0) < MAX_SERFS_PER_TREE
                for t in zone_data["trees"]
            )
        )

    def _can_recall_wood_zone_batch(self, zone_name: str, batch_size: int) -> bool:
        """PrÃƒÆ’Ã‚Â¼ft ob batch_size Serfs von einer Holz-Zone zurÃƒÆ’Ã‚Â¼ckgerufen werden kÃƒÆ’Ã‚Â¶nnen."""
        cache_key = ("recall_wood_zone", zone_name, batch_size)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return cached
        if zone_name not in self.wood_zone_categories:
            return self._set_can_cache(cache_key, False)
        return self._set_can_cache(
            cache_key,
            self.wood_zone_categories[zone_name]["serfs_assigned"] >= batch_size
        )

    def _assign_wood_zone_batch(self, zone_name: str, batch_size: int):
        """
        Weist batch_size Serfs zu einer spezifischen Holz-Zone zu.
        Serfs werden zu den nÃƒÆ’Ã‚Â¤chsten BÃƒÆ’Ã‚Â¤umen in der Zone geschickt (deterministic).
        """
        from worker_simulation import Position
        from production_system import ResourceType

        zone_data = self.wood_zone_categories.get(zone_name)
        if not zone_data:
            return

        # Finde verfÃƒÆ’Ã‚Â¼gbare BÃƒÆ’Ã‚Â¤ume, sortiert nach Distanz zum Zonenzentrum (nÃƒÆ’Ã‚Â¤chste zuerst)
        available_trees = [
            t for t in zone_data["trees"]
            if t["resource_remaining"] > 0 and t.get("serfs_assigned", 0) < MAX_SERFS_PER_TREE
        ]
        available_trees.sort(key=lambda t: t["dist"])

        if not available_trees:
            return

        assigned = 0
        tree_idx = 0
        for serf in self.production_system.serfs:
            if assigned >= batch_size:
                break
            if serf.is_idle():
                # Verteile Serfs auf verschiedene BÃƒÆ’Ã‚Â¤ume (spread) mit KapazitÃƒÆ’Ã‚Â¤tslimit
                chosen_tree = None
                checked = 0
                while checked < len(available_trees):
                    tree = available_trees[tree_idx % len(available_trees)]
                    tree_idx += 1
                    checked += 1
                    if tree["resource_remaining"] > 0 and tree.get("serfs_assigned", 0) < MAX_SERFS_PER_TREE:
                        chosen_tree = tree
                        break

                if not chosen_tree:
                    break

                target_pos = Position(x=chosen_tree["x"], y=chosen_tree["y"])
                start_pos = Position(x=serf.position.x, y=serf.position.y)
                self._assign_serf_to_resource_pathing(serf, ResourceType.WOOD_RAW, target_pos, start_pos)
                serf.work_location = f"wood_zone_{zone_name}"  # Zone-spezifisch
                chosen_tree["serfs_assigned"] += 1
                assigned += 1

        zone_data["serfs_assigned"] += assigned
        self.wood_serfs += assigned
        self.free_leibeigene -= assigned
        self.resource_workers[RESOURCE_HOLZ_ROH] = self.resource_workers.get(RESOURCE_HOLZ_ROH, 0) + assigned

    def _can_assign_wood_tree_batch(
        self,
        tree_idx: int,
        batch_size: int,
        available_free_override: Optional[int] = None,
    ) -> bool:
        available_free = self.free_leibeigene if available_free_override is None else int(available_free_override)
        if batch_size <= 0 or available_free < batch_size:
            return False
        if tree_idx < 0 or tree_idx >= len(self.tree_list_internal):
            return False
        tree = self.tree_list_internal[tree_idx]
        return (
            tree.get("resource_remaining", 0) > 0
            and tree.get("serfs_assigned", 0) + batch_size <= MAX_SERFS_PER_TREE
        )

    def _can_recall_wood_tree_batch(self, tree_idx: int, batch_size: int) -> bool:
        if batch_size <= 0:
            return False
        if tree_idx < 0 or tree_idx >= len(self.tree_list_internal):
            return False
        tree = self.tree_list_internal[tree_idx]
        return tree.get("serfs_assigned", 0) >= batch_size

    def _assign_wood_tree_batch(self, tree_idx: int, batch_size: int) -> int:
        from worker_simulation import Position
        from production_system import ResourceType

        if not self._can_assign_wood_tree_batch(tree_idx, batch_size):
            return 0

        tree = self.tree_list_internal[tree_idx]
        target_pos = Position(x=tree["x"], y=tree["y"])
        zone_name = tree.get("zone")
        assigned = 0
        for serf in self.production_system.serfs:
            if assigned >= batch_size:
                break
            if serf.is_idle():
                start_pos = Position(x=serf.position.x, y=serf.position.y)
                self._assign_serf_to_resource_pathing(serf, ResourceType.WOOD_RAW, target_pos, start_pos)
                if zone_name:
                    serf.work_location = f"wood_zone_{zone_name}"
                else:
                    serf.work_location = "wood"
                assigned += 1

        if assigned:
            tree["serfs_assigned"] = tree.get("serfs_assigned", 0) + assigned
            if zone_name in self.wood_zone_categories:
                self.wood_zone_categories[zone_name]["serfs_assigned"] = (
                    self.wood_zone_categories[zone_name].get("serfs_assigned", 0) + assigned
                )
            self.wood_serfs += assigned
            self.free_leibeigene -= assigned
            self.resource_workers[RESOURCE_HOLZ_ROH] = self.resource_workers.get(RESOURCE_HOLZ_ROH, 0) + assigned
        return assigned

    def _recall_wood_tree_batch(self, tree_idx: int, batch_size: int) -> int:
        if not self._can_recall_wood_tree_batch(tree_idx, batch_size):
            return 0

        tree = self.tree_list_internal[tree_idx]
        target_x = int(tree.get("x", 0))
        target_y = int(tree.get("y", 0))
        zone_name = tree.get("zone")
        recalled = 0
        for serf in self.production_system.serfs:
            if recalled >= batch_size:
                break
            if (
                serf.target_resource
                and serf.target_resource.value == "wood_raw"
                and serf.target_position
                and int(serf.target_position.x) == target_x
                and int(serf.target_position.y) == target_y
            ):
                serf.stop()
                recalled += 1

        if recalled:
            tree["serfs_assigned"] = max(0, tree.get("serfs_assigned", 0) - recalled)
            if zone_name in self.wood_zone_categories:
                self.wood_zone_categories[zone_name]["serfs_assigned"] = max(
                    0,
                    self.wood_zone_categories[zone_name].get("serfs_assigned", 0) - recalled,
                )
            self.wood_serfs = max(0, self.wood_serfs - recalled)
            self.free_leibeigene += recalled
            self.resource_workers[RESOURCE_HOLZ_ROH] = max(
                0,
                self.resource_workers.get(RESOURCE_HOLZ_ROH, 0) - recalled,
            )
        return recalled

    def _recall_wood_zone_batch(self, zone_name: str, batch_size: int):
        """Ruft batch_size Serfs von einer spezifischen Holz-Zone zurÃƒÆ’Ã‚Â¼ck."""
        zone_data = self.wood_zone_categories.get(zone_name)
        if not zone_data:
            return

        work_location = f"wood_zone_{zone_name}"
        recalled = 0
        for serf in self.production_system.serfs:
            if recalled >= batch_size:
                break
            if (serf.target_resource and
                serf.target_resource.value == "wood_raw" and
                serf.work_location == work_location):
                serf.stop()
                recalled += 1

        zone_data["serfs_assigned"] = max(0, zone_data["serfs_assigned"] - recalled)
        self.wood_serfs = max(0, self.wood_serfs - recalled)
        self.free_leibeigene += recalled
        self.resource_workers[RESOURCE_HOLZ_ROH] = max(0, self.resource_workers.get(RESOURCE_HOLZ_ROH, 0) - recalled)

    def _auto_reassign_wood_serfs(self, from_x: float, from_y: float, num_serfs: int) -> int:
        """
        Automatisches Weitersammeln: Suche naechsten Baum im SERF_SEARCH_RADIUS.
        Wie im echten Spiel (PU_Serf.xml: ResourceSearchRadius = 4500).

        Returns: Anzahl erfolgreich zugewiesener Serfs
        """
        import math
        reassigned = 0
        radius = self._get_effective_serf_search_radius()

        def _match_pos(pos, x, y):
            return pos is not None and int(pos.x) == int(x) and int(pos.y) == int(y)

        # Nur Serfs vom erschoepften Baum umleiten
        candidate_serfs = []
        for serf in self.production_system.serfs:
            if serf.target_resource and serf.target_resource.value == "wood_raw":
                if _match_pos(serf.target_position, from_x, from_y):
                    candidate_serfs.append(serf)

        if not candidate_serfs:
            return 0

        # Finde alle Baeume im Suchradius, sortiert nach Distanz
        trees_in_radius = []
        for i, tree in enumerate(self.tree_list_internal):
            if tree["resource_remaining"] > 0 and tree.get("serfs_assigned", 0) < MAX_SERFS_PER_TREE:
                dx = tree["x"] - from_x
                dy = tree["y"] - from_y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance <= radius:
                    trees_in_radius.append((distance, i, tree))

        # Sortiere nach Distanz (naechster zuerst)
        trees_in_radius.sort(key=lambda x: x[0])

        # Weise Serfs den naechsten Baeumen zu
        serf_idx = 0
        for _, tree_idx, tree in trees_in_radius:
            if reassigned >= num_serfs:
                break
            if serf_idx >= len(candidate_serfs):
                break
            if tree.get("serfs_assigned", 0) >= MAX_SERFS_PER_TREE:
                continue
            serf = candidate_serfs[serf_idx]
            serf_idx += 1
            # Serf zum neuen Baum schicken
            from worker_simulation import Position
            from production_system import ResourceType
            target_pos = Position(x=tree["x"], y=tree["y"])
            # FÃƒÆ’Ã‚Â¼r Cache-Hits alle Reassigns von derselben Quellposition aus berechnen.
            start_pos = Position(x=from_x, y=from_y)
            prev_location = serf.work_location or "wood"
            self._assign_serf_to_resource_pathing(serf, ResourceType.WOOD_RAW, target_pos, start_pos)
            serf.work_location = prev_location  # Zone-Info behalten, falls vorhanden
            tree["serfs_assigned"] += 1
            reassigned += 1

        return reassigned

    def _auto_reassign_wood_serf(self, serf: Serf, from_x: float, from_y: float) -> bool:
        """Weist einen einzelnen Serf dem naechsten Baum im Radius zu."""
        import math
        from worker_simulation import Position
        from production_system import ResourceType
        radius = self._get_effective_serf_search_radius()
        best_tree = None
        best_distance = float("inf")
        for tree in self.tree_list_internal:
            if tree.get("resource_remaining", 0) > 0 and tree.get("serfs_assigned", 0) < MAX_SERFS_PER_TREE:
                dx = tree["x"] - from_x
                dy = tree["y"] - from_y
                distance = math.sqrt(dx * dx + dy * dy)
                if distance <= radius and distance < best_distance:
                    best_distance = distance
                    best_tree = tree
        if not best_tree:
            return False
        target_pos = Position(x=best_tree["x"], y=best_tree["y"])
        # FÃƒÆ’Ã‚Â¼r Cache-Hits immer von der erschÃƒÆ’Ã‚Â¶pften Baumposition aus replannen.
        start_pos = Position(x=from_x, y=from_y)
        prev_location = serf.work_location or "wood"
        self._assign_serf_to_resource_pathing(serf, ResourceType.WOOD_RAW, target_pos, start_pos)
        serf.work_location = prev_location
        best_tree["serfs_assigned"] = best_tree.get("serfs_assigned", 0) + 1
        return True

    def _auto_reassign_deposit_serf_for(self, serf: Serf, category: str, from_x: float, from_y: float) -> bool:
        """Weist einen Serf dem naechsten Deposit im Radius zu."""
        import math
        from worker_simulation import Position
        from production_system import ResourceType
        resource_type_map = {
            "Eisen": ResourceType.IRON_RAW,
            "Stein": ResourceType.STONE_RAW,
            "Lehm": ResourceType.CLAY_RAW,
            "Schwefel": ResourceType.SULFUR_RAW,
        }
        resource_type = resource_type_map.get(category)
        if not resource_type:
            return False
        radius = self._get_effective_serf_search_radius()
        best_deposit = None
        best_distance = float("inf")
        for deposit in self.deposit_categories.get(category, {}).get("deposits", []):
            if deposit.get("remaining", 0) > 0 and not self._is_mine_built_at_deposit(
                deposit["x"], deposit["y"], category
            ):
                dx = deposit["x"] - from_x
                dy = deposit["y"] - from_y
                distance = math.sqrt(dx * dx + dy * dy)
                if distance <= radius and distance < best_distance:
                    best_distance = distance
                    best_deposit = deposit
        if not best_deposit:
            return False
        target_pos = Position(x=best_deposit["x"], y=best_deposit["y"])
        start_pos = Position(x=from_x, y=from_y)
        self._assign_serf_to_resource_pathing(serf, resource_type, target_pos, start_pos)
        serf.work_location = "deposit"
        return True

    def _auto_reassign_shaft_serf_for(self, serf: Serf, category: str, from_x: float, from_y: float) -> bool:
        """Weist einen Serf dem naechsten Stollen im Radius zu."""
        import math
        from worker_simulation import Position
        from production_system import ResourceType
        resource_type_map = {
            "Eisen": ResourceType.IRON_RAW,
            "Stein": ResourceType.STONE_RAW,
            "Lehm": ResourceType.CLAY_RAW,
            "Schwefel": ResourceType.SULFUR_RAW,
        }
        resource_type = resource_type_map.get(category)
        if not resource_type:
            return False
        radius = self._get_effective_serf_search_radius()
        best_shaft = None
        best_distance = float("inf")
        for shaft in self.shaft_categories.get(category, {}).get("shafts", []):
            if shaft.get("remaining", 0) > 0:
                dx = shaft["x"] - from_x
                dy = shaft["y"] - from_y
                distance = math.sqrt(dx * dx + dy * dy)
                if distance <= radius and distance < best_distance:
                    best_distance = distance
                    best_shaft = shaft
        if not best_shaft:
            return False
        target_pos = Position(x=best_shaft["x"], y=best_shaft["y"])
        start_pos = Position(x=from_x, y=from_y)
        self._assign_serf_to_resource_pathing(serf, resource_type, target_pos, start_pos)
        serf.work_location = "shaft"
        return True

    def _handle_tree_depleted(self, tree: dict) -> bool:
        if tree.get("depleted"):
            return False
        tree["resource_remaining"] = 0
        tree["serfs_assigned"] = 0
        tree["depleted"] = True
        self._remove_tree_from_grid(tree)
        from production_system import ResourceType
        serfs_here = [
            s for s in self.production_system.serfs
            if s.target_resource and s.target_resource == ResourceType.WOOD_RAW
            and s.target_position
            and int(s.target_position.x) == int(tree.get("x", 0))
            and int(s.target_position.y) == int(tree.get("y", 0))
        ]
        reassigned = self._auto_reassign_wood_serfs(tree["x"], tree["y"], len(serfs_here))
        if reassigned < len(serfs_here):
            for serf in serfs_here:
                if (serf.target_resource == ResourceType.WOOD_RAW and serf.target_position and
                        int(serf.target_position.x) == int(tree.get("x", 0)) and
                        int(serf.target_position.y) == int(tree.get("y", 0))):
                    serf.stop()
        return True

    def _handle_deposit_depleted(self, category: str, deposit: dict) -> bool:
        if deposit.get("depleted"):
            return False
        deposit["remaining"] = 0
        deposit["depleted"] = True
        key = (int(deposit.get("x", 0)), int(deposit.get("y", 0)))
        if hasattr(self, "_small_deposit_by_pos"):
            small = self._small_deposit_by_pos.get(category, {}).get(key)
            if small is not None:
                small["remaining"] = 0
        from production_system import ResourceType
        resource_type_map = {
            "Eisen": ResourceType.IRON_RAW,
            "Stein": ResourceType.STONE_RAW,
            "Lehm": ResourceType.CLAY_RAW,
            "Schwefel": ResourceType.SULFUR_RAW,
        }
        res_type = resource_type_map.get(category)
        serfs_here = [
            s for s in self.production_system.serfs
            if s.target_resource and s.target_resource == res_type
            and s.work_location in ("deposit", "mine")
            and s.target_position
            and int(s.target_position.x) == int(deposit.get("x", 0))
            and int(s.target_position.y) == int(deposit.get("y", 0))
        ]
        for serf in serfs_here:
            if not self._auto_reassign_deposit_serf_for(serf, category, deposit["x"], deposit["y"]):
                serf.stop()
        return True

    def _handle_shaft_depleted(self, category: str, shaft: dict) -> bool:
        if shaft.get("depleted"):
            return False
        shaft["remaining"] = 0
        shaft["depleted"] = True
        from production_system import ResourceType
        resource_type_map = {
            "Eisen": ResourceType.IRON_RAW,
            "Stein": ResourceType.STONE_RAW,
            "Lehm": ResourceType.CLAY_RAW,
            "Schwefel": ResourceType.SULFUR_RAW,
        }
        res_type = resource_type_map.get(category)
        serfs_here = [
            s for s in self.production_system.serfs
            if s.target_resource and s.target_resource == res_type
            and s.work_location == "shaft"
            and s.target_position
            and int(s.target_position.x) == int(shaft.get("x", 0))
            and int(s.target_position.y) == int(shaft.get("y", 0))
        ]
        for serf in serfs_here:
            if not self._auto_reassign_shaft_serf_for(serf, category, shaft["x"], shaft["y"]):
                serf.stop()
        return True

    def _process_serf_events(self, events: List[dict]):
        """Verarbeitet Serf-Extraktionen und aktualisiert Ressourcen-Remaining exakt."""
        if not events:
            return
        from production_system import ResourceType
        tree_changed = False
        deposit_changed = False
        resource_to_category = {
            ResourceType.IRON_RAW: "Eisen",
            ResourceType.STONE_RAW: "Stein",
            ResourceType.CLAY_RAW: "Lehm",
            ResourceType.SULFUR_RAW: "Schwefel",
        }
        for event in events:
            resource = event.get("resource")
            amount = event.get("amount", 0)
            pos = event.get("position")
            if not resource or not pos:
                continue
            key = (int(pos.x), int(pos.y))
            if resource == ResourceType.WOOD_RAW:
                tree = getattr(self, "_tree_by_pos", {}).get(key)
                if not tree:
                    continue
                if tree.get("resource_remaining", 0) <= 0:
                    continue
                tree["resource_remaining"] = max(0, tree["resource_remaining"] - amount)
                if tree["resource_remaining"] <= 0:
                    if self._handle_tree_depleted(tree):
                        tree_changed = True
                continue

            category = resource_to_category.get(resource)
            if not category:
                continue
            work_location = event.get("work_location") or "deposit"
            if work_location == "shaft":
                shaft = getattr(self, "_shaft_by_pos", {}).get(category, {}).get(key)
                if not shaft:
                    continue
                if shaft.get("remaining", 0) <= 0:
                    continue
                shaft["remaining"] = max(0, shaft["remaining"] - amount)
                if shaft["remaining"] <= 0:
                    if self._handle_shaft_depleted(category, shaft):
                        deposit_changed = True
            else:
                deposit = getattr(self, "_deposit_by_pos", {}).get(category, {}).get(key)
                if not deposit:
                    continue
                if deposit.get("remaining", 0) <= 0:
                    continue
                deposit["remaining"] = max(0, deposit["remaining"] - amount)
                if hasattr(self, "_small_deposit_by_pos"):
                    small = self._small_deposit_by_pos.get(category, {}).get(key)
                    if small is not None:
                        small["remaining"] = deposit["remaining"]
                if deposit["remaining"] <= 0:
                    if self._handle_deposit_depleted(category, deposit):
                        deposit_changed = True

        if tree_changed:
            self._check_zone_b_unlock()
        if deposit_changed:
            self._mark_spatial_dirty("deposits")

    def _stop_wood_serfs_at(self, x: float, y: float, count: int) -> int:
        """Stoppt bis zu count Holz-Serfs an einer spezifischen Baum-Position."""
        stopped = 0
        for serf in self.production_system.serfs:
            if stopped >= count:
                break
            if serf.target_resource and serf.target_resource.value == "wood_raw":
                if serf.target_position and int(serf.target_position.x) == int(x) and int(serf.target_position.y) == int(y):
                    if serf.work_location and serf.work_location.startswith("wood_zone_"):
                        zone_name = serf.work_location[len("wood_zone_"):]
                        zone_data = self.wood_zone_categories.get(zone_name)
                        if zone_data:
                            zone_data["serfs_assigned"] = max(0, zone_data.get("serfs_assigned", 0) - 1)
                    serf.stop()
                    stopped += 1
        return stopped

    def _stop_deposit_serfs_at(self, category: str, x: float, y: float, count: int) -> int:
        """Stoppt bis zu count Deposit-Serfs an einer spezifischen Deposit-Position."""
        resource_type_map = {
            "Eisen": "iron_raw",
            "Stein": "stone_raw",
            "Lehm": "clay_raw",
            "Schwefel": "sulfur_raw",
        }
        target_value = resource_type_map.get(category)
        if not target_value:
            return 0

        stopped = 0
        for serf in self.production_system.serfs:
            if stopped >= count:
                break
            if serf.work_location == "deposit" and serf.target_resource and serf.target_resource.value == target_value:
                if serf.target_position and int(serf.target_position.x) == int(x) and int(serf.target_position.y) == int(y):
                    serf.stop()
                    stopped += 1

        # Fallback: falls keine exakte Position gefunden wurde
        if stopped < count:
            for serf in self.production_system.serfs:
                if stopped >= count:
                    break
                if serf.work_location == "deposit" and serf.target_resource and serf.target_resource.value == target_value:
                    serf.stop()
                    stopped += 1

        return stopped

    def _stop_shaft_serfs_at(self, category: str, x: float, y: float, count: int) -> int:
        """Stoppt bis zu count Stollen-Serfs an einer spezifischen Slot-Position."""
        resource_type_map = {
            "Eisen": "iron_raw",
            "Stein": "stone_raw",
            "Lehm": "clay_raw",
            "Schwefel": "sulfur_raw",
        }
        target_value = resource_type_map.get(category)
        if not target_value:
            return 0

        stopped = 0
        for serf in self.production_system.serfs:
            if stopped >= count:
                break
            if serf.work_location == "shaft" and serf.target_resource and serf.target_resource.value == target_value:
                if serf.target_position and int(serf.target_position.x) == int(x) and int(serf.target_position.y) == int(y):
                    serf.stop()
                    stopped += 1

        return stopped

    def _can_assign_serf_to_specific_area(
        self,
        area: SerfArea,
        batch_size: int,
        available_free_override: Optional[int] = None,
    ) -> bool:
        available_free = self.free_leibeigene if available_free_override is None else int(available_free_override)
        if batch_size <= 0 or available_free < batch_size:
            return False
        if area in SHAFT_AREA_TO_SLOT:
            category, slot_idx = SHAFT_AREA_TO_SLOT[area]
            shafts = self.shaft_categories.get(category, {}).get("shafts", [])
            return slot_idx < len(shafts) and shafts[slot_idx].get("remaining", 0) > 0
        if area in DEPOSIT_AREA_TO_SLOT:
            category, slot_idx = DEPOSIT_AREA_TO_SLOT[area]
            deposits = self.deposit_categories.get(category, {}).get("deposits", [])
            if slot_idx >= len(deposits):
                return False
            dep = deposits[slot_idx]
            return dep.get("remaining", 0) > 0 and not self._is_mine_built_at_deposit(dep["x"], dep["y"], category)
        return False

    def _assign_serfs_to_specific_area(self, area: SerfArea, quantity: int) -> int:
        from worker_simulation import Position
        from production_system import ResourceType

        actual_quantity = min(int(quantity), self.free_leibeigene)
        if actual_quantity <= 0:
            return 0

        if area in SHAFT_AREA_TO_SLOT:
            category, slot_idx = SHAFT_AREA_TO_SLOT[area]
            shafts = self.shaft_categories.get(category, {}).get("shafts", [])
            if slot_idx >= len(shafts):
                return 0
            shaft = shafts[slot_idx]
            if shaft.get("remaining", 0) <= 0:
                return 0
            resource_type = {
                "Eisen": ResourceType.IRON_RAW,
                "Stein": ResourceType.STONE_RAW,
                "Lehm": ResourceType.CLAY_RAW,
                "Schwefel": ResourceType.SULFUR_RAW,
            }.get(category)
            if resource_type is None:
                return 0

            assigned = 0
            for serf in self.production_system.serfs:
                if assigned >= actual_quantity:
                    break
                if serf.is_idle():
                    target_pos = Position(x=shaft["x"], y=shaft["y"])
                    start_pos = Position(x=serf.position.x, y=serf.position.y)
                    self._assign_serf_to_resource_pathing(serf, resource_type, target_pos, start_pos)
                    serf.work_location = "shaft"
                    shaft["serfs_assigned"] = shaft.get("serfs_assigned", 0) + 1
                    assigned += 1
            if assigned:
                self.shaft_categories[category]["serfs_assigned"] = self.shaft_categories[category].get("serfs_assigned", 0) + assigned
                self.free_leibeigene -= assigned
                raw_name = {
                    "Eisen": RESOURCE_EISEN_ROH,
                    "Stein": RESOURCE_STEIN_ROH,
                    "Lehm": RESOURCE_LEHM_ROH,
                    "Schwefel": RESOURCE_SCHWEFEL_ROH,
                }.get(category, category)
                self.resource_workers[raw_name] = self.resource_workers.get(raw_name, 0) + assigned
            return assigned

        if area in DEPOSIT_AREA_TO_SLOT:
            category, slot_idx = DEPOSIT_AREA_TO_SLOT[area]
            deposits = self.deposit_categories.get(category, {}).get("deposits", [])
            if slot_idx >= len(deposits):
                return 0
            deposit = deposits[slot_idx]
            if deposit.get("remaining", 0) <= 0 or self._is_mine_built_at_deposit(deposit["x"], deposit["y"], category):
                return 0
            resource_type = {
                "Eisen": ResourceType.IRON_RAW,
                "Stein": ResourceType.STONE_RAW,
                "Lehm": ResourceType.CLAY_RAW,
                "Schwefel": ResourceType.SULFUR_RAW,
            }.get(category)
            if resource_type is None:
                return 0

            assigned = 0
            for serf in self.production_system.serfs:
                if assigned >= actual_quantity:
                    break
                if serf.is_idle():
                    target_pos = Position(x=deposit["x"], y=deposit["y"])
                    start_pos = Position(x=serf.position.x, y=serf.position.y)
                    self._assign_serf_to_resource_pathing(serf, resource_type, target_pos, start_pos)
                    serf.work_location = "deposit"
                    assigned += 1
            if assigned:
                self.deposit_categories[category]["serfs_assigned"] = self.deposit_categories[category].get("serfs_assigned", 0) + assigned
                self.free_leibeigene -= assigned
                raw_name = {
                    "Eisen": RESOURCE_EISEN_ROH,
                    "Stein": RESOURCE_STEIN_ROH,
                    "Lehm": RESOURCE_LEHM_ROH,
                    "Schwefel": RESOURCE_SCHWEFEL_ROH,
                }.get(category, category)
                self.resource_workers[raw_name] = self.resource_workers.get(raw_name, 0) + assigned
            return assigned

        return 0

    def _recall_serfs_from_specific_area(self, area: SerfArea, quantity: int) -> int:
        actual_quantity = max(0, int(quantity))
        if actual_quantity <= 0:
            return 0

        if area in SHAFT_AREA_TO_SLOT:
            category, slot_idx = SHAFT_AREA_TO_SLOT[area]
            shafts = self.shaft_categories.get(category, {}).get("shafts", [])
            if slot_idx >= len(shafts):
                return 0
            shaft = shafts[slot_idx]
            recalled = self._stop_shaft_serfs_at(category, shaft["x"], shaft["y"], actual_quantity)
            if recalled:
                shaft["serfs_assigned"] = max(0, shaft.get("serfs_assigned", 0) - recalled)
                self.shaft_categories[category]["serfs_assigned"] = max(0, self.shaft_categories[category].get("serfs_assigned", 0) - recalled)
                self.free_leibeigene += recalled
                raw_name = {
                    "Eisen": RESOURCE_EISEN_ROH,
                    "Stein": RESOURCE_STEIN_ROH,
                    "Lehm": RESOURCE_LEHM_ROH,
                    "Schwefel": RESOURCE_SCHWEFEL_ROH,
                }.get(category, category)
                self.resource_workers[raw_name] = max(0, self.resource_workers.get(raw_name, 0) - recalled)
            return recalled

        if area in DEPOSIT_AREA_TO_SLOT:
            category, slot_idx = DEPOSIT_AREA_TO_SLOT[area]
            deposits = self.deposit_categories.get(category, {}).get("deposits", [])
            if slot_idx >= len(deposits):
                return 0
            dep = deposits[slot_idx]
            recalled = self._stop_deposit_serfs_at(category, dep["x"], dep["y"], actual_quantity)
            if recalled:
                self.deposit_categories[category]["serfs_assigned"] = max(0, self.deposit_categories[category].get("serfs_assigned", 0) - recalled)
                self.free_leibeigene += recalled
                raw_name = {
                    "Eisen": RESOURCE_EISEN_ROH,
                    "Stein": RESOURCE_STEIN_ROH,
                    "Lehm": RESOURCE_LEHM_ROH,
                    "Schwefel": RESOURCE_SCHWEFEL_ROH,
                }.get(category, category)
                self.resource_workers[raw_name] = max(0, self.resource_workers.get(raw_name, 0) - recalled)
            return recalled

        return 0

    def _refresh_walkable_cache(self) -> None:
        """Aktualisiert Walkable/Blocked-Cache nur wenn das Grid geÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¤ndert wurde."""
        if not getattr(self, "_walkable_dirty", True):
            return
        if not (hasattr(self, "map_manager") and self.map_manager):
            return

        walkable_grid = self.map_manager.grid.get_walkable_grid().astype(np.float32)
        if walkable_grid.size:
            self._walkable_ratio = float(np.mean(walkable_grid))
            self._spatial_static_layers["walkable"] = self._downsample_grid(walkable_grid)
            self._spatial_static_layers["blocked"] = 1.0 - self._spatial_static_layers["walkable"]
        else:
            self._walkable_ratio = 0.0
            self._spatial_static_layers["walkable"] = self._downsample_grid(walkable_grid)
            self._spatial_static_layers["blocked"] = 1.0 - self._spatial_static_layers["walkable"]

        dynamic_blocked = np.maximum(self.map_manager.grid.buildings, self.map_manager.grid.trees)
        if dynamic_blocked.size:
            self._dynamic_blocked_ratio = float(np.mean(dynamic_blocked))
        else:
            self._dynamic_blocked_ratio = 0.0

        self._sync_refiner_path_distances()
        self._walkable_dirty = False

    def _refresh_dynamic_layers(self) -> None:
        """Aktualisiert dynamische Spatial-Layer nur wenn nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¶tig."""
        if not self.use_spatial_obs:
            return
        if not hasattr(self, "_spatial_dynamic_layers"):
            return

        if self._spatial_dynamic_dirty.get("trees"):
            tree_positions = []
            if hasattr(self, "tree_list_internal") and self.tree_list_internal:
                for tree in self.tree_list_internal:
                    if tree.get("resource_remaining", 0) > 0:
                        tree_positions.append((tree["x"], tree["y"]))
            elif hasattr(self, "trees_list") and self.trees_list:
                tree_positions = [(t["x"], t["y"]) for t in self.trees_list]
            self._spatial_dynamic_layers["trees"] = self._positions_to_layer(tree_positions)
            self._spatial_dynamic_dirty["trees"] = False

        if self._spatial_dynamic_dirty.get("deposits"):
            deposit_positions = []
            for res_list in self.small_deposits.values():
                for dep in res_list:
                    if dep.get("remaining", 0) > 0:
                        deposit_positions.append((dep["x"], dep["y"]))
            self._spatial_dynamic_layers["deposits"] = self._positions_to_layer(deposit_positions)
            self._spatial_dynamic_dirty["deposits"] = False

        if self._spatial_dynamic_dirty.get("buildings"):
            building_positions = [self.hq_position]
            for pos in self.building_position_map.values():
                if isinstance(pos, dict):
                    building_positions.append((pos["x"], pos["y"]))
                elif isinstance(pos, tuple):
                    building_positions.append((pos[0], pos[1]))
            self._spatial_dynamic_layers["buildings"] = self._positions_to_layer(building_positions)
            self._spatial_dynamic_dirty["buildings"] = False

        if self._spatial_dynamic_dirty.get("available_slots"):
            available_positions = []
            for pos in getattr(self, "available_positions", []):
                if isinstance(pos, dict):
                    available_positions.append((pos["x"], pos["y"]))
                elif isinstance(pos, tuple):
                    available_positions.append((pos[0], pos[1]))
            self._spatial_dynamic_layers["available_slots"] = self._positions_to_layer(available_positions)
            self._spatial_dynamic_dirty["available_slots"] = False

        if self._spatial_dynamic_dirty.get("construction_sites"):
            construction_positions = []
            for site in getattr(self, "construction_sites", []):
                pos = site.get("position")
                if pos:
                    if isinstance(pos, dict):
                        construction_positions.append((pos["x"], pos["y"]))
                    elif isinstance(pos, tuple):
                        construction_positions.append((pos[0], pos[1]))
            self._spatial_dynamic_layers["construction_sites"] = self._positions_to_layer(construction_positions)
            self._spatial_dynamic_dirty["construction_sites"] = False

    def _remove_tree_from_grid(self, tree: dict) -> None:
        """Entfernt einen gefaellten Baum aus dem Walkable-Grid (Pfadfindung)."""
        if tree.get("grid_removed"):
            return
        tree["grid_removed"] = True

        x = int(round(tree.get("x", 0)))
        y = int(round(tree.get("y", 0)))
        if hasattr(self, "_tree_by_pos"):
            self._tree_by_pos.pop((x, y), None)

        tree_id = None
        if hasattr(self, "tree_id_by_position"):
            tree_id = self.tree_id_by_position.get((x, y))
            if tree_id is not None:
                self.tree_id_by_position.pop((x, y), None)

        if tree_id is None:
            nearest = self.map_manager.get_nearest_tree(x, y)
            if nearest:
                tree_id = nearest[0]

        if tree_id is not None:
            self.map_manager.remove_tree(tree_id)
            self._walkable_dirty = True
            self._mark_spatial_dirty("trees")

    # --- VORKOMMEN (Deposits) ---
    def _is_mine_built_at_deposit(self, deposit_x: float, deposit_y: float, category: str) -> bool:
        """
        PrÃƒÆ’Ã‚Â¼ft ob an dieser Deposit-Position eine Mine gebaut wurde.
        Wenn ja, kÃƒÆ’Ã‚Â¶nnen Serfs dort NICHT mehr sammeln - nur noch Worker.
        """
        import math
        # Mapping: Ressourcen-Kategorie -> Mine-Typ
        category_to_mine = {
            "Eisen": "Eisenmine",
            "Stein": "Steinmine",
            "Lehm": "Lehmmine",
            "Schwefel": "Schwefelmine",
        }
        mine_type = category_to_mine.get(category)
        if not mine_type:
            return False

        # PrÃƒÆ’Ã‚Â¼fe ob eine Mine in der NÃƒÆ’Ã‚Â¤he gebaut wurde (Toleranz fÃƒÆ’Ã‚Â¼r Positionsungenauigkeit)
        POSITION_TOLERANCE = 500  # Spieleinheiten
        for mine_pos in self.built_mines.get(mine_type, []):
            dx = mine_pos["x"] - deposit_x
            dy = mine_pos["y"] - deposit_y
            distance = math.sqrt(dx*dx + dy*dy)
            if distance < POSITION_TOLERANCE:
                return True
        return False

    def _can_assign_deposit_batch(self, category: str, batch_size: int) -> bool:
        """
        PrÃƒÆ’Ã‚Â¼ft ob batch_size Serfs zu einer Vorkommen-Kategorie zugewiesen werden kÃƒÆ’Ã‚Â¶nnen.
        WICHTIG: Serfs kÃƒÆ’Ã‚Â¶nnen nur an Deposits sammeln wo KEINE Mine gebaut wurde!
        """
        cache_key = ("assign_deposit", category, batch_size)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return cached
        if category not in self.deposit_categories:
            return self._set_can_cache(cache_key, False)
        if self.free_leibeigene < batch_size:
            return self._set_can_cache(cache_key, False)
        # Mindestens ein Deposit mit Ressourcen UND ohne gebaute Mine
        cat_data = self.deposit_categories[category]
        return self._set_can_cache(
            cache_key,
            any(
                d["remaining"] > 0 and not self._is_mine_built_at_deposit(d["x"], d["y"], category)
                for d in cat_data["deposits"]
            )
        )

    def _can_recall_deposit_batch(self, category: str, batch_size: int) -> bool:
        """PrÃƒÆ’Ã‚Â¼ft ob batch_size Serfs von einer Vorkommen-Kategorie zurÃƒÆ’Ã‚Â¼ckgerufen werden kÃƒÆ’Ã‚Â¶nnen."""
        cache_key = ("recall_deposit", category, batch_size)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return cached
        if category not in self.deposit_categories:
            return self._set_can_cache(cache_key, False)
        return self._set_can_cache(
            cache_key,
            self.deposit_categories[category]["serfs_assigned"] >= batch_size
        )

    def _assign_deposit_batch(self, category: str, batch_size: int):
        """Weist batch_size Serfs zu einer Vorkommen-Kategorie zu."""
        from worker_simulation import Position
        from production_system import ResourceType
        import random

        resource_type_map = {
            "Eisen": ResourceType.IRON_RAW,
            "Stein": ResourceType.STONE_RAW,
            "Lehm": ResourceType.CLAY_RAW,
            "Schwefel": ResourceType.SULFUR_RAW,
        }
        resource_type = resource_type_map.get(category)
        if not resource_type:
            return

        cat_data = self.deposit_categories[category]
        # Filter: Nur Deposits mit Ressourcen UND ohne gebaute Mine
        available_deposits = [
            d for d in cat_data["deposits"]
            if d["remaining"] > 0 and not self._is_mine_built_at_deposit(d["x"], d["y"], category)
        ]
        if not available_deposits:
            return

        assigned = 0
        for serf in self.production_system.serfs:
            if assigned >= batch_size:
                break
            if serf.is_idle():
                # ZufÃƒÆ’Ã‚Â¤llig ein Deposit wÃƒÆ’Ã‚Â¤hlen
                deposit = random.choice(available_deposits)
                target_pos = Position(x=deposit["x"], y=deposit["y"])
                start_pos = Position(x=serf.position.x, y=serf.position.y)
                self._assign_serf_to_resource_pathing(serf, resource_type, target_pos, start_pos)
                serf.work_location = "deposit"  # NEU: Markiere als Vorkommen-Serf
                assigned += 1

        cat_data["serfs_assigned"] += assigned
        self.free_leibeigene -= assigned
        raw_name_map = {
            "Eisen": RESOURCE_EISEN_ROH,
            "Stein": RESOURCE_STEIN_ROH,
            "Lehm": RESOURCE_LEHM_ROH,
            "Schwefel": RESOURCE_SCHWEFEL_ROH,
        }
        raw_name = raw_name_map.get(category, category)
        self.resource_workers[raw_name] = self.resource_workers.get(raw_name, 0) + assigned

    def _recall_deposit_batch(self, category: str, batch_size: int):
        """Ruft batch_size Serfs von einer Vorkommen-Kategorie zurÃƒÆ’Ã‚Â¼ck."""
        resource_type_map = {
            "Eisen": "iron_raw",
            "Stein": "stone_raw",
            "Lehm": "clay_raw",
            "Schwefel": "sulfur_raw",
        }
        target_resource_value = resource_type_map.get(category)

        recalled = 0
        for serf in self.production_system.serfs:
            if recalled >= batch_size:
                break
            # NEU: PrÃƒÆ’Ã‚Â¼fe work_location um Deposit- von Minen-Serfs zu unterscheiden
            if (serf.target_resource and
                serf.target_resource.value == target_resource_value and
                serf.work_location == "deposit"):
                serf.stop()
                recalled += 1

        cat_data = self.deposit_categories[category]
        cat_data["serfs_assigned"] = max(0, cat_data["serfs_assigned"] - recalled)
        self.free_leibeigene += recalled
        raw_name_map = {
            "Eisen": RESOURCE_EISEN_ROH,
            "Stein": RESOURCE_STEIN_ROH,
            "Lehm": RESOURCE_LEHM_ROH,
            "Schwefel": RESOURCE_SCHWEFEL_ROH,
        }
        raw_name = raw_name_map.get(category, category)
        self.resource_workers[raw_name] = max(0, self.resource_workers.get(raw_name, 0) - recalled)

    def _auto_reassign_deposit_serf(self, category: str, from_x: float, from_y: float) -> bool:
        """
        Automatisches Weitersammeln fuer Vorkommen: Suche naechstes Deposit im Radius.

        Returns: True wenn Serf erfolgreich zu neuem Deposit zugewiesen wurde
        """
        import math
        from worker_simulation import Position
        from production_system import ResourceType

        cat_data = self.deposit_categories.get(category)
        if not cat_data:
            return False

        resource_type_map = {
            "Eisen": ResourceType.IRON_RAW,
            "Stein": ResourceType.STONE_RAW,
            "Lehm": ResourceType.CLAY_RAW,
            "Schwefel": ResourceType.SULFUR_RAW,
        }
        resource_type = resource_type_map.get(category)
        if not resource_type:
            return False

        # Finde naechstes Deposit mit Ressourcen im Radius
        best_deposit = None
        best_distance = float('inf')
        radius = self._get_effective_serf_search_radius()

        for deposit in cat_data["deposits"]:
            if deposit["remaining"] > 0 and not self._is_mine_built_at_deposit(
                deposit["x"], deposit["y"], category
            ):
                dx = deposit["x"] - from_x
                dy = deposit["y"] - from_y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance <= radius and distance < best_distance:
                    best_distance = distance
                    best_deposit = deposit

        if best_deposit:
            # Serf zum neuen Deposit schicken (bleibt in derselben Kategorie)
            target_serf = None
            for serf in self.production_system.serfs:
                if serf.work_location == "deposit" and serf.target_resource == resource_type:
                    if serf.target_position and int(serf.target_position.x) == int(from_x) and int(serf.target_position.y) == int(from_y):
                        target_serf = serf
                        break
            if target_serf is None:
                for serf in self.production_system.serfs:
                    if serf.work_location == "deposit" and serf.target_resource == resource_type:
                        target_serf = serf
                        break

            if target_serf is None:
                return False

            target_pos = Position(x=best_deposit["x"], y=best_deposit["y"])
            start_pos = target_serf.position
            if not isinstance(start_pos, Position):
                if isinstance(start_pos, dict):
                    start_pos = Position(x=start_pos.get("x", 0), y=start_pos.get("y", 0))
                elif isinstance(start_pos, tuple):
                    start_pos = Position(x=start_pos[0], y=start_pos[1])
                else:
                    start_pos = Position(x=0, y=0)
            self._assign_serf_to_resource_pathing(target_serf, resource_type, target_pos, start_pos)
            target_serf.work_location = "deposit"
            return True

        return False

        # Finde nÃƒÆ’Ã‚Â¤chstes Deposit mit Ressourcen im Radius
        best_deposit = None
        best_distance = float('inf')
        radius = self._get_effective_serf_search_radius()

        for deposit in cat_data["deposits"]:
            if deposit["remaining"] > 0:
                dx = deposit["x"] - from_x
                dy = deposit["y"] - from_y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance <= radius and distance < best_distance:
                    best_distance = distance
                    best_deposit = deposit

        if best_deposit:
            # Serf zum neuen Deposit schicken (bleibt in derselben Kategorie)
            # Der serfs_assigned ZÃƒÆ’Ã‚Â¤hler bleibt gleich, da Serf weitermacht
            return True

        return False

    # --- STOLLEN (Shafts) - Serfs kÃƒÆ’Ã‚Â¶nnen hier IMMER sammeln ---
    # HINWEIS: "mine_categories" wird jetzt fÃƒÆ’Ã‚Â¼r STOLLEN verwendet, nicht fÃƒÆ’Ã‚Â¼r gebaute Minen!
    # Stollen (XD_Iron1 etc.) sind separate Ressourcen-Punkte wo Serfs sammeln.
    # Gebaute Minen werden von Workern (Miner) betrieben, nicht von Serfs!

    def _can_assign_shaft_batch(self, shaft_type: str, batch_size: int) -> bool:
        """
        PrÃƒÆ’Ã‚Â¼ft ob batch_size Serfs zu einem Stollen-Typ zugewiesen werden kÃƒÆ’Ã‚Â¶nnen.
        Stollen sind IMMER verfÃƒÆ’Ã‚Â¼gbar - keine Mine kann dort gebaut werden.
        (XD_Iron1 = Eisenstollen, XD_Stone1 = Steinstollen, etc.)
        """
        cache_key = ("assign_shaft", shaft_type, batch_size)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return cached
        if shaft_type not in self.shaft_categories:
            return self._set_can_cache(cache_key, False)
        if self.free_leibeigene < batch_size:
            return self._set_can_cache(cache_key, False)
        # Stollen haben begrenzte KapazitÃƒÆ’Ã‚Â¤t (400 Ressourcen pro Stollen)
        # PrÃƒÆ’Ã‚Â¼fe ob mindestens ein Stollen mit Ressourcen existiert
        shaft_data = self.shaft_categories[shaft_type]
        return self._set_can_cache(
            cache_key,
            any(s.get("remaining", 400) > 0 for s in shaft_data.get("shafts", []))
        )

    def _can_recall_shaft_batch(self, shaft_type: str, batch_size: int) -> bool:
        """PrÃƒÆ’Ã‚Â¼ft ob batch_size Serfs von einem Stollen-Typ zurÃƒÆ’Ã‚Â¼ckgerufen werden kÃƒÆ’Ã‚Â¶nnen."""
        cache_key = ("recall_shaft", shaft_type, batch_size)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return cached
        if shaft_type not in self.shaft_categories:
            return self._set_can_cache(cache_key, False)
        return self._set_can_cache(
            cache_key,
            self.shaft_categories[shaft_type].get("serfs_assigned", 0) >= batch_size
        )

    def _assign_shaft_batch(self, shaft_type: str, batch_size: int):
        """
        Weist batch_size Serfs zu einem Stollen-Typ zu.
        Stollen (XD_Iron1 etc.) haben jeweils 400 Ressourcen und sind IMMER verfÃƒÆ’Ã‚Â¼gbar.
        """
        from worker_simulation import Position
        from production_system import ResourceType

        shaft_to_resource = {
            "Eisen": ResourceType.IRON_RAW,
            "Stein": ResourceType.STONE_RAW,
            "Lehm": ResourceType.CLAY_RAW,
            "Schwefel": ResourceType.SULFUR_RAW,
        }
        resource_type = shaft_to_resource.get(shaft_type)
        if not resource_type:
            return

        shaft_data = self.shaft_categories.get(shaft_type)
        if not shaft_data:
            return

        # Finde Stollen mit verfÃƒÆ’Ã‚Â¼gbaren Ressourcen
        available_shafts = [s for s in shaft_data.get("shafts", []) if s.get("remaining", 400) > 0]
        if not available_shafts:
            return

        assigned = 0
        for serf in self.production_system.serfs:
            if assigned >= batch_size:
                break
            if serf.is_idle():
                # Zum nÃƒÆ’Ã‚Â¤chsten verfÃƒÆ’Ã‚Â¼gbaren Stollen mit wenigsten Serfs schicken
                available_shafts.sort(key=lambda s: s.get("serfs_assigned", 0))
                shaft = available_shafts[0]
                target_pos = Position(x=shaft["x"], y=shaft["y"])
                start_pos = Position(x=serf.position.x, y=serf.position.y)
                self._assign_serf_to_resource_pathing(serf, resource_type, target_pos, start_pos)
                serf.work_location = "shaft"  # Markiere als Stollen-Serf
                shaft["serfs_assigned"] = shaft.get("serfs_assigned", 0) + 1
                assigned += 1

        shaft_data["serfs_assigned"] = shaft_data.get("serfs_assigned", 0) + assigned
        self.free_leibeigene -= assigned
        raw_name_map = {
            "Eisen": RESOURCE_EISEN_ROH,
            "Stein": RESOURCE_STEIN_ROH,
            "Lehm": RESOURCE_LEHM_ROH,
            "Schwefel": RESOURCE_SCHWEFEL_ROH,
        }
        raw_name = raw_name_map.get(shaft_type, shaft_type)
        self.resource_workers[raw_name] = self.resource_workers.get(raw_name, 0) + assigned

    def _recall_shaft_batch(self, shaft_type: str, batch_size: int):
        """Ruft batch_size Serfs von einem Stollen-Typ zurÃƒÆ’Ã‚Â¼ck."""
        shaft_to_resource_value = {
            "Eisen": "iron_raw",
            "Stein": "stone_raw",
            "Lehm": "clay_raw",
            "Schwefel": "sulfur_raw",
        }
        target_resource_value = shaft_to_resource_value.get(shaft_type)

        recalled = 0
        for serf in self.production_system.serfs:
            if recalled >= batch_size:
                break
            # PrÃƒÆ’Ã‚Â¼fe work_location um Stollen- von Deposit-Serfs zu unterscheiden
            if (serf.target_resource and
                serf.target_resource.value == target_resource_value and
                serf.work_location == "shaft"):
                serf.stop()
                recalled += 1

        shaft_data = self.shaft_categories.get(shaft_type)
        if shaft_data:
            shaft_data["serfs_assigned"] = max(0, shaft_data.get("serfs_assigned", 0) - recalled)
        self.free_leibeigene += recalled
        raw_name_map = {
            "Eisen": RESOURCE_EISEN_ROH,
            "Stein": RESOURCE_STEIN_ROH,
            "Lehm": RESOURCE_LEHM_ROH,
            "Schwefel": RESOURCE_SCHWEFEL_ROH,
        }
        raw_name = raw_name_map.get(shaft_type, shaft_type)
        self.resource_workers[raw_name] = max(0, self.resource_workers.get(raw_name, 0) - recalled)

    # ENTFERNT: Alte Mine-Serf-Zuweisung - Serfs arbeiten NICHT an gebauten Minen!
    # Gebaute Minen werden von Workern (PU_Miner) betrieben.
    def _can_assign_mine_batch(self, mine_type: str, batch_size: int) -> bool:
        """DEAKTIVIERT: Serfs arbeiten nicht an gebauten Minen - nur Worker tun das."""
        return False  # Immer False - Serfs kÃƒÆ’Ã‚Â¶nnen nicht an Minen arbeiten

    def _can_recall_mine_batch(self, mine_type: str, batch_size: int) -> bool:
        """DEAKTIVIERT: Serfs arbeiten nicht an gebauten Minen."""
        return False  # Immer False

    def _assign_mine_batch(self, mine_type: str, batch_size: int):
        """Weist batch_size Serfs zu einer Mine-Kategorie zu."""
        from worker_simulation import Position
        from production_system import ResourceType

        mine_to_resource = {
            "Eisenmine": ResourceType.IRON_RAW,
            "Steinmine": ResourceType.STONE_RAW,
            "Lehmmine": ResourceType.CLAY_RAW,
            "Schwefelmine": ResourceType.SULFUR_RAW,
        }
        resource_type = mine_to_resource.get(mine_type)
        if not resource_type:
            return

        mine_to_name = {
            "Eisenmine": RESOURCE_EISEN_ROH,
            "Steinmine": RESOURCE_STEIN_ROH,
            "Lehmmine": RESOURCE_LEHM_ROH,
            "Schwefelmine": RESOURCE_SCHWEFEL_ROH,
        }
        resource_name = mine_to_name.get(mine_type)

        # Finde eine gebaute Mine-Position
        mine_positions = self.built_mines.get(mine_type, [])
        if not mine_positions:
            return

        assigned = 0
        for serf in self.production_system.serfs:
            if assigned >= batch_size:
                break
            if serf.is_idle():
                # Zur ersten gebauten Mine schicken
                mine_pos = mine_positions[0]
                target_pos = Position(x=mine_pos["x"], y=mine_pos["y"])
                start_pos = Position(x=serf.position.x, y=serf.position.y)
                self._assign_serf_to_resource_pathing(serf, resource_type, target_pos, start_pos)
                serf.work_location = "mine"  # NEU: Markiere als Minen-Serf
                assigned += 1

        mine_data = self.mine_categories[mine_type]
        mine_data["serfs_assigned"] += assigned
        self.free_leibeigene -= assigned
        if resource_name:
            self.resource_workers[resource_name] = self.resource_workers.get(resource_name, 0) + assigned

    def _recall_mine_batch(self, mine_type: str, batch_size: int):
        """Ruft batch_size Serfs von einer Mine-Kategorie zurÃƒÆ’Ã‚Â¼ck."""
        mine_to_resource = {
            "Eisenmine": "iron_raw",
            "Steinmine": "stone_raw",
            "Lehmmine": "clay_raw",
            "Schwefelmine": "sulfur_raw",
        }
        target_resource_value = mine_to_resource.get(mine_type)

        mine_to_name = {
            "Eisenmine": RESOURCE_EISEN_ROH,
            "Steinmine": RESOURCE_STEIN_ROH,
            "Lehmmine": RESOURCE_LEHM_ROH,
            "Schwefelmine": RESOURCE_SCHWEFEL_ROH,
        }
        resource_name = mine_to_name.get(mine_type)

        recalled = 0
        for serf in self.production_system.serfs:
            if recalled >= batch_size:
                break
            # NEU: PrÃƒÆ’Ã‚Â¼fe work_location um Minen- von Deposit-Serfs zu unterscheiden
            if (serf.target_resource and
                serf.target_resource.value == target_resource_value and
                serf.work_location == "mine"):
                serf.stop()
                recalled += 1

        mine_data = self.mine_categories[mine_type]
        mine_data["serfs_assigned"] = max(0, mine_data["serfs_assigned"] - recalled)
        self.free_leibeigene += recalled
        if resource_name:
            self.resource_workers[resource_name] = max(0, self.resource_workers.get(resource_name, 0) - recalled)

    # --- BAUSTELLEN-SYSTEM ---
    def _can_assign_build_batch(self, batch_size: int) -> bool:
        """PrÃƒÆ’Ã‚Â¼ft ob batch_size Serfs zu Baustellen zugewiesen werden kÃƒÆ’Ã‚Â¶nnen."""
        cache_key = ("assign_build", batch_size)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return cached
        # Braucht freie Leibeigene und mindestens eine Baustelle
        if self.free_leibeigene < batch_size:
            return self._set_can_cache(cache_key, False)
        return self._set_can_cache(cache_key, len(self.construction_sites) > 0)

    def _assign_build_batch(self, batch_size: int):
        """Weist batch_size Serfs zur ersten wartenden Baustelle zu."""
        from worker_simulation import Position

        if not self.construction_sites:
            return

        # Finde Baustelle mit wenigsten Serfs (oder erste ohne Serfs)
        target_site = None
        for site in self.construction_sites:
            if target_site is None or site["serfs_assigned"] < target_site["serfs_assigned"]:
                target_site = site

        if target_site is None:
            return

        assigned = 0
        for serf in self.production_system.serfs:
            if assigned >= batch_size:
                break
            if serf.is_idle():
                # Serf zur Baustelle schicken
                pos = target_site["position"]
                if pos:
                    build_pos = Position(x=pos["x"], y=pos["y"])
                else:
                    # Fallback: HQ Position
                    build_pos = Position(x=self.hq_position[0], y=self.hq_position[1])
                serf_pos = Position(x=serf.position.x, y=serf.position.y)
                self._assign_serf_to_build(
                    serf,
                    target_site["building"],
                    build_pos,
                    serf_pos,
                    target_site["site_id"]
                )
                assigned += 1

        target_site["serfs_assigned"] += assigned
        self.free_leibeigene -= assigned

    def _can_recall_build_batch(self, batch_size: int) -> bool:
        """PrÃƒÆ’Ã‚Â¼ft ob batch_size Serfs von Baustellen zurÃƒÆ’Ã‚Â¼ckgerufen werden kÃƒÆ’Ã‚Â¶nnen."""
        cache_key = ("recall_build", batch_size)
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return cached
        total_building_serfs = sum(s["serfs_assigned"] for s in self.construction_sites)
        return self._set_can_cache(cache_key, total_building_serfs >= batch_size)

    def _recall_build_batch(self, batch_size: int):
        """Ruft batch_size Serfs von Baustellen zurÃƒÆ’Ã‚Â¼ck."""
        recalled = 0
        for serf in self.production_system.serfs:
            if recalled >= batch_size:
                break
            if serf.is_building():
                # Finde zugehÃƒÆ’Ã‚Â¶rige Baustelle und reduziere ZÃƒÆ’Ã‚Â¤hler
                for site in self.construction_sites:
                    if site["site_id"] == serf.build_site_id:
                        site["serfs_assigned"] = max(0, site["serfs_assigned"] - 1)
                        break
                serf.stop()
                recalled += 1

        self.free_leibeigene += recalled

    def _release_serfs_from_site(self, site: dict):
        """Gibt alle Serfs einer fertiggestellten Baustelle frei."""
        released = 0
        for serf in self.production_system.serfs:
            if serf.build_site_id == site["site_id"]:
                serf.stop()
                released += 1
        self.free_leibeigene += released

    def _get_active_construction_sites(self) -> int:
        """Gibt Anzahl aktiver Baustellen zurÃƒÆ’Ã‚Â¼ck."""
        return len(self.construction_sites)

    @staticmethod
    def _to_int_choice(value, default: int = 0) -> int:
        """Normalisiert Action-/Selection-Werte robust auf int."""
        try:
            if isinstance(value, np.ndarray):
                arr = np.asarray(value).reshape(-1)
                if arr.size <= 0:
                    return int(default)
                return int(arr[0])
            if isinstance(value, (list, tuple)):
                if len(value) <= 0:
                    return int(default)
                return int(value[0])
            return int(value)
        except Exception:
            return int(default)

    def step(self, action):
        """Multi-Step Action Flow."""
        # =================================================================
        # MULTI-STEP FLOW MANAGEMENT
        # =================================================================
        action = self._to_int_choice(action, default=0)
        phase_size = self.action_spaces[self.current_phase].n
        local_mask = np.asarray(self._get_local_action_mask(), dtype=bool).reshape(-1)
        is_in_range = 0 <= action < phase_size
        is_mask_valid = bool(local_mask[action]) if is_in_range and action < local_mask.size else False
        if not is_mask_valid:
            valid_indices = np.flatnonzero(local_mask[:phase_size])
            if valid_indices.size > 0:
                action = int(valid_indices[0])
            else:
                if self.current_phase != ActionPhase.MAIN:
                    # Failsafe: ungültigen Subflow hart abbrechen statt No-Op auszuführen.
                    self.current_phase = ActionPhase.MAIN
                    self.current_flow = None
                    self.flow_step = 0
                    self.pending_selections = {}
                    obs = self._get_observation()
                    return obs, 0.0, False, False, {"blocked_invalid_action": True, "phase_reset": "main"}
                action = 0
        if self.current_phase == ActionPhase.MAIN:
            action_name = MAIN_ACTIONS[action]
            self.current_flow = action_name
            self.flow_step = 0
            self.pending_selections = {ActionPhase.MAIN: int(action)}
            flow_phases = ACTION_FLOWS[action_name]
            if len(flow_phases) == 1:
                reward = self._execute_action(action_name, self.pending_selections)
                self.current_phase = ActionPhase.MAIN
                self.current_flow = None
                self.pending_selections = {}
            else:
                self.flow_step = 1
                self.current_phase = flow_phases[1]
                obs = self._get_observation()
                return obs, 0.0, False, False, {"multi_step": True, "phase": self.current_phase.value}
        else:
            action_name = self.current_flow
            self.pending_selections[self.current_phase] = int(action)
            self.flow_step += 1

            # Sonderfall: "Frei" (Kategorie 0) ÃƒÆ’Ã‚Â¼berspringt die SPECIFIC-Phase
            if self.current_phase == ActionPhase.SOURCE_CATEGORY and action == 0:
                self.pending_selections[ActionPhase.SOURCE_SPECIFIC] = 0
                self.flow_step += 1  # SOURCE_SPECIFIC ÃƒÆ’Ã‚Â¼berspringen
            elif (
                self.current_phase == ActionPhase.TARGET_CATEGORY
                and action == 0
                and self.current_flow != "assign_serf"
            ):
                self.pending_selections[ActionPhase.TARGET_SPECIFIC] = 0
                self.flow_step += 1  # TARGET_SPECIFIC ÃƒÆ’Ã‚Â¼berspringen
            elif (
                self.current_flow == "assign_serf"
                and self.current_phase == ActionPhase.TARGET_SPECIFIC
                and self.pending_selections.get(ActionPhase.TARGET_CATEGORY) != 7
            ):
                self.pending_selections[ActionPhase.POSITION_GROUP] = 0
                self.pending_selections[ActionPhase.POSITION_INDEX] = 0
                self.flow_step += 2

            flow_phases = ACTION_FLOWS[self.current_flow]
            if self.flow_step >= len(flow_phases):
                reward = self._execute_action(self.current_flow, self.pending_selections)
                self.current_phase = ActionPhase.MAIN
                self.current_flow = None
                self.pending_selections = {}
            else:
                self.current_phase = flow_phases[self.flow_step]
                obs = self._get_observation()
                return obs, 0.0, False, False, {"multi_step": True, "phase": self.current_phase.value}

        # Zeitsimulation (nur wenn Aktion komplett)
        info = {}
        self._tick_time()
        efficiency = self.workforce_manager.get_average_efficiency()
        exhausted_ratio = self.workforce_manager.get_exhausted_ratio()
        completed_action = action_name
        self.action_history.append({"time": self.current_time, "action": completed_action})
        info["action_name"] = completed_action
        info["efficiency"] = efficiency
        info["exhausted_ratio"] = exhausted_ratio

        resource_potential_now = self._get_scharf_resource_potential()
        dependency_progress_now = self._get_scharf_dependency_progress()
        self._update_terminal_cumulative_tracker()
        research_progress_now = self._get_scharf_research_progress_metric()
        construction_progress_now = self._get_scharf_construction_progress_metric()
        recruitable_now = self._is_scharf_recruitable_now()
        taxable_workers_now = float(self._get_taxable_worker_count())
        taler_income_per_cycle_now = float(self._get_taler_income_per_cycle())

        info["scharf_resource_potential"] = resource_potential_now
        info["scharf_dependency_progress"] = dependency_progress_now
        info["scharf_research_progress"] = research_progress_now
        info["scharf_construction_progress"] = construction_progress_now

        # Dense shaping aus reinen Zustandsaenderungen (aktionsagnostisch).
        step_use_cumulative_potential = float(
            self.reward_profile.get("step_potential_use_cumulative_earnings", 1.0)
        ) > 0.0
        step_include_start_resources = float(
            self.reward_profile.get("step_potential_include_start_resources", 0.0)
        ) > 0.0
        step_potential_tier = self._get_reward_profile_scharf_tier(
            "step_potential_scharf_tier",
            default=1,
        )
        if step_use_cumulative_potential:
            step_potential_metric_now = float(
                self._get_scharf_cumulative_resource_potential(
                    include_start_resources=step_include_start_resources,
                    target_tier=step_potential_tier,
                )
            )
        else:
            step_potential_metric_now = float(self._get_scharf_resource_potential(target_tier=step_potential_tier))

        step_delta_potential = step_potential_metric_now - float(self._last_step_potential_metric)
        step_potential_units_now = int(max(0, int(np.floor(step_potential_metric_now))))
        step_new_potential_units = max(0, step_potential_units_now - int(self._last_step_potential_units))
        step_delta_dependency = float(dependency_progress_now) - float(self._last_scharf_dependency_progress)
        step_delta_research = float(research_progress_now) - float(self._last_scharf_research_progress)
        step_delta_construction = float(construction_progress_now) - float(self._last_scharf_construction_progress)
        # Anti-exploit: reward only for surpassing the episode-high taxable worker count.
        step_worker_growth = max(0.0, float(taxable_workers_now) - float(self._best_step_taxable_workers))
        step_unlock_progress_now = self._get_step_unlock_progress_metric(
            dependency_progress=dependency_progress_now,
            research_progress=research_progress_now,
            construction_progress=construction_progress_now,
        )
        step_delta_progress = step_unlock_progress_now - float(self._last_step_unlock_progress)
        step_unlock_recruitable = bool(recruitable_now and (not self._last_scharf_recruitable))

        step_positive_only = float(self.reward_profile.get("step_delta_positive_only", 1.0)) > 0.0
        if step_positive_only:
            step_delta_potential = max(0.0, step_delta_potential)
            step_delta_progress = max(0.0, step_delta_progress)
            step_delta_dependency = max(0.0, step_delta_dependency)
            step_delta_research = max(0.0, step_delta_research)
            step_delta_construction = max(0.0, step_delta_construction)
            step_worker_growth = max(0.0, step_worker_growth)

        step_reward = 0.0
        step_reward += step_delta_potential * float(self.reward_profile.get("step_delta_potential_bonus", 0.0))
        step_reward += float(step_new_potential_units) * float(
            self.reward_profile.get("step_new_resource_potential_unit_bonus", 0.0)
        )
        step_reward += step_delta_progress * float(self.reward_profile.get("step_delta_progress_bonus", 0.0))
        step_reward += step_delta_dependency * float(self.reward_profile.get("step_delta_dependency_bonus", 0.0))
        step_reward += step_delta_research * float(self.reward_profile.get("step_delta_research_bonus", 0.0))
        step_reward += step_delta_construction * float(self.reward_profile.get("step_delta_construction_bonus", 0.0))
        step_reward += step_worker_growth * float(
            self.reward_profile.get("step_worker_growth_bonus", 0.0)
        )
        if step_unlock_recruitable:
            step_reward += float(self.reward_profile.get("step_unlock_recruitable_bonus", 0.0))
        step_reward -= abs(float(self.reward_profile.get("step_time_penalty", 0.0)))
        reward += step_reward

        info["step_potential_source"] = (
            "cumulative_earnings" if step_use_cumulative_potential else "current_stock"
        )
        info["step_potential_scharf_tier"] = int(step_potential_tier)
        info["step_potential_include_start_resources"] = bool(step_include_start_resources)
        info["step_delta_positive_only"] = bool(step_positive_only)
        info["step_potential_metric"] = float(step_potential_metric_now)
        info["step_potential_units"] = int(step_potential_units_now)
        info["step_new_potential_units"] = int(step_new_potential_units)
        info["step_taxable_workers"] = float(taxable_workers_now)
        info["step_taler_income_per_cycle"] = float(taler_income_per_cycle_now)
        info["step_delta_potential"] = float(step_delta_potential)
        info["step_unlock_progress_metric"] = float(step_unlock_progress_now)
        info["step_delta_unlock_progress"] = float(step_delta_progress)
        info["step_delta_dependency"] = float(step_delta_dependency)
        info["step_delta_research"] = float(step_delta_research)
        info["step_delta_construction"] = float(step_delta_construction)
        info["step_worker_growth"] = float(step_worker_growth)
        info["step_unlock_recruitable"] = bool(step_unlock_recruitable)
        info["step_reward"] = float(step_reward)
        info["pending_spawned_unassigned_serfs"] = int(
            max(0, int(getattr(self, "_pending_spawned_unassigned_serfs", 0)))
        )

        self._last_step_potential_metric = float(step_potential_metric_now)
        self._last_step_potential_units = int(step_potential_units_now)
        self._best_step_taxable_workers = max(float(self._best_step_taxable_workers), float(taxable_workers_now))
        self._last_scharf_resource_potential = resource_potential_now
        self._last_scharf_dependency_progress = dependency_progress_now
        self._last_scharf_research_progress = research_progress_now
        self._last_scharf_construction_progress = construction_progress_now
        self._last_step_unlock_progress = step_unlock_progress_now
        self._last_scharf_recruitable = recruitable_now

        terminated = self.current_time >= self.max_time
        # Terminal reward logic intentionally disabled.
        return self._get_observation(), reward, terminated, False, info

    def _resolve_area(self, category, specific):
        """Mappt (Kategorie, Spezifisch) auf SerfArea enum."""
        if category == 6:  # Baustelle
            return SerfArea.FREE
        areas = CATEGORY_AREA_MAP.get(category, [SerfArea.FREE])
        if specific < len(areas):
            return areas[specific]
        return areas[0] if areas else SerfArea.FREE

    def _pos_key_from_xy(self, x, y):
        return (int(round(x)), int(round(y)))

    def _pos_key_from_position(self, pos):
        if pos is None:
            return None
        if hasattr(pos, "x") and hasattr(pos, "y"):
            return self._pos_key_from_xy(pos.x, pos.y)
        if isinstance(pos, dict):
            return self._pos_key_from_xy(pos.get("x", 0), pos.get("y", 0))
        if isinstance(pos, tuple):
            return self._pos_key_from_xy(pos[0], pos[1])
        return None

    def _resource_value_to_category(self, value: str):
        return {
            "iron": "Eisen",
            "iron_raw": "Eisen",
            "stone": "Stein",
            "stone_raw": "Stein",
            "clay": "Lehm",
            "clay_raw": "Lehm",
            "sulfur": "Schwefel",
            "sulfur_raw": "Schwefel",
            "wood": "Holz",
            "wood_raw": "Holz",
            "gold": "Gold",
            "gold_raw": "Gold",
        }.get(value)

    def _init_serf_area_maps(self):
        """Initialisiert Positions-Maps fÃƒÆ’Ã‚Â¼r prÃƒÆ’Ã‚Â¤zises Serf-Area Tracking."""
        wood_area_order = [
            SerfArea.WOOD_HQ,
            SerfArea.WOOD_SULFUR,
            SerfArea.WOOD_CLAY,
            SerfArea.WOOD_STONE,
            SerfArea.WOOD_VILLAGE,
            SerfArea.WOOD_IRON,
        ]

        def zone_area_from_name(zone_name: str):
            name = zone_name.lower()
            if "hq" in name:
                return SerfArea.WOOD_HQ
            if "schwefel" in name:
                return SerfArea.WOOD_SULFUR
            if "lehm" in name:
                return SerfArea.WOOD_CLAY
            if "stein" in name:
                return SerfArea.WOOD_STONE
            if "dorf" in name or "village" in name:
                return SerfArea.WOOD_VILLAGE
            if "eisen" in name:
                return SerfArea.WOOD_IRON
            return None

        self._wood_zone_area_map = {}
        self._wood_area_to_zone_name = {}
        for idx, zone_name in enumerate(self.wood_zone_names):
            area = zone_area_from_name(zone_name)
            if area is None and idx < len(wood_area_order):
                area = wood_area_order[idx]
            if area:
                self._wood_zone_area_map[zone_name] = area
                self._wood_area_to_zone_name[area] = zone_name

        # Tree-Positionen -> Area
        self._wood_tree_area_by_pos = {}
        for tree in getattr(self, "tree_list_internal", []):
            zone_name = tree.get("zone")
            area = self._wood_zone_area_map.get(zone_name)
            if area:
                key = self._pos_key_from_xy(tree.get("x", 0), tree.get("y", 0))
                self._wood_tree_area_by_pos[key] = area

        # Deposits -> Area (per Kategorie)
        deposit_area_lists = {
            "Eisen": [SerfArea.DEPOSIT_IRON_1, SerfArea.DEPOSIT_IRON_2],
            "Stein": [SerfArea.DEPOSIT_STONE_1, SerfArea.DEPOSIT_STONE_2],
            "Lehm": [SerfArea.DEPOSIT_CLAY_1],
            "Schwefel": [SerfArea.DEPOSIT_SULFUR_1, SerfArea.DEPOSIT_SULFUR_2],
        }
        self._deposit_area_by_pos = {}
        self._deposit_area_fallback = {}
        for category, area_list in deposit_area_lists.items():
            if not area_list:
                continue
            self._deposit_area_fallback[category] = area_list[0]
            pos_map = {}
            for idx, dep in enumerate(self.deposit_categories.get(category, {}).get("deposits", [])):
                area = area_list[min(idx, len(area_list) - 1)]
                key = self._pos_key_from_xy(dep.get("x", 0), dep.get("y", 0))
                pos_map[key] = area
            self._deposit_area_by_pos[category] = pos_map

        # Shafts -> Area (per Kategorie)
        shaft_area_lists = {
            "Eisen": [SerfArea.SHAFT_IRON_1, SerfArea.SHAFT_IRON_2, SerfArea.SHAFT_IRON_3],
            "Stein": [SerfArea.SHAFT_STONE_1, SerfArea.SHAFT_STONE_2, SerfArea.SHAFT_STONE_3],
            "Lehm": [SerfArea.SHAFT_CLAY_1, SerfArea.SHAFT_CLAY_2, SerfArea.SHAFT_CLAY_3],
            "Schwefel": [SerfArea.SHAFT_SULFUR_1, SerfArea.SHAFT_SULFUR_2, SerfArea.SHAFT_SULFUR_3],
        }
        self._shaft_area_by_pos = {}
        self._shaft_area_fallback = {}
        for category, area_list in shaft_area_lists.items():
            if not area_list:
                continue
            self._shaft_area_fallback[category] = area_list[0]
            pos_map = {}
            for idx, shaft in enumerate(self.shaft_categories.get(category, {}).get("shafts", [])):
                area = area_list[min(idx, len(area_list) - 1)]
                key = self._pos_key_from_xy(shaft.get("x", 0), shaft.get("y", 0))
                pos_map[key] = area
            self._shaft_area_by_pos[category] = pos_map

    def _infer_serf_area(self, serf: Serf):
        """Leitet den SerfArea aus Work-Location + Zielposition ab."""
        if serf is None:
            return None
        if serf.is_building():
            return None

        work_loc = serf.work_location or ""
        if work_loc.startswith("wood_zone_"):
            zone_name = work_loc[len("wood_zone_"):]
            return self._wood_zone_area_map.get(zone_name, SerfArea.WOOD_HQ)

        if serf.target_resource:
            res_value = serf.target_resource.value
            if res_value == "wood_raw":
                pos_key = self._pos_key_from_position(serf.target_position)
                if pos_key and pos_key in getattr(self, "_wood_tree_area_by_pos", {}):
                    return self._wood_tree_area_by_pos[pos_key]
                return SerfArea.WOOD_HQ

            category = self._resource_value_to_category(res_value)
            pos_key = self._pos_key_from_position(serf.target_position)
            if work_loc == "deposit":
                area_map = getattr(self, "_deposit_area_by_pos", {}).get(category, {})
                if pos_key and pos_key in area_map:
                    return area_map[pos_key]
                return getattr(self, "_deposit_area_fallback", {}).get(category, SerfArea.FREE)
            if work_loc == "shaft":
                area_map = getattr(self, "_shaft_area_by_pos", {}).get(category, {})
                if pos_key and pos_key in area_map:
                    return area_map[pos_key]
                return getattr(self, "_shaft_area_fallback", {}).get(category, SerfArea.FREE)
            if work_loc == "mine":
                return getattr(self, "_deposit_area_fallback", {}).get(category, SerfArea.FREE)

        return SerfArea.FREE

    def _recount_serf_areas(self):
        """Rekonstruiert SerfArea-ZÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¤hler aus echten Serf-Objekten."""
        if not hasattr(self, "production_system"):
            return

        counts = {area: 0 for area in SerfArea}
        idle_count = 0
        building_count = 0

        zone_counts = {name: 0 for name in getattr(self, "wood_zone_names", [])}
        deposit_counts = {cat: 0 for cat in getattr(self, "deposit_categories", {}).keys()}
        shaft_counts = {cat: 0 for cat in getattr(self, "shaft_categories", {}).keys()}
        resource_counts_raw = {
            RESOURCE_HOLZ_ROH: 0,
            RESOURCE_STEIN_ROH: 0,
            RESOURCE_LEHM_ROH: 0,
            RESOURCE_EISEN_ROH: 0,
            RESOURCE_SCHWEFEL_ROH: 0,
            RESOURCE_GOLD_ROH: 0,
        }

        category_to_raw = {
            "Eisen": RESOURCE_EISEN_ROH,
            "Stein": RESOURCE_STEIN_ROH,
            "Lehm": RESOURCE_LEHM_ROH,
            "Schwefel": RESOURCE_SCHWEFEL_ROH,
        }

        tree_serfs_by_pos = {}
        shaft_serfs_by_pos = {cat: {} for cat in shaft_counts.keys()}

        for serf in self.production_system.serfs:
            if serf.is_idle():
                idle_count += 1
                continue
            if serf.is_building():
                building_count += 1
                continue

            area = self._infer_serf_area(serf)
            if area in counts:
                counts[area] += 1

            if serf.target_resource:
                res_value = serf.target_resource.value
                if res_value == "wood_raw":
                    resource_counts_raw[RESOURCE_HOLZ_ROH] += 1
                    zone_name = self._wood_area_to_zone_name.get(area)
                    if zone_name:
                        zone_counts[zone_name] = zone_counts.get(zone_name, 0) + 1
                    pos_key = self._pos_key_from_position(serf.target_position)
                    if pos_key:
                        tree_serfs_by_pos[pos_key] = tree_serfs_by_pos.get(pos_key, 0) + 1
                else:
                    category = self._resource_value_to_category(res_value)
                    if category:
                        raw_name = category_to_raw.get(category)
                        if raw_name:
                            resource_counts_raw[raw_name] = resource_counts_raw.get(raw_name, 0) + 1
                        if serf.work_location in ("deposit", "mine"):
                            deposit_counts[category] = deposit_counts.get(category, 0) + 1
                        elif serf.work_location == "shaft":
                            shaft_counts[category] = shaft_counts.get(category, 0) + 1
                            pos_key = self._pos_key_from_position(serf.target_position)
                            if pos_key:
                                cat_map = shaft_serfs_by_pos.setdefault(category, {})
                                cat_map[pos_key] = cat_map.get(pos_key, 0) + 1

        for area in SerfArea:
            if area not in self.serf_areas:
                self.serf_areas[area] = {"count": 0}
            self.serf_areas[area]["count"] = counts.get(area, 0)

        # FREIE Serfs = wirklich idle
        self.serf_areas[SerfArea.FREE]["count"] = idle_count
        self.free_leibeigene = idle_count

        # Holz-Zonen und BÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¤ume
        for zone_name, zone_data in getattr(self, "wood_zone_categories", {}).items():
            zone_data["serfs_assigned"] = zone_counts.get(zone_name, 0)
        # Resource worker counts neu aufbauen
        self.resource_workers = {r: 0 for r in RESOURCE_MAP}

        self.wood_serfs = resource_counts_raw.get(RESOURCE_HOLZ_ROH, 0)
        self.resource_workers[RESOURCE_HOLZ_ROH] = self.wood_serfs

        if hasattr(self, "tree_list_internal"):
            for tree in self.tree_list_internal:
                key = self._pos_key_from_xy(tree.get("x", 0), tree.get("y", 0))
                tree["serfs_assigned"] = tree_serfs_by_pos.get(key, 0)

        # Deposits
        for category, cat_data in getattr(self, "deposit_categories", {}).items():
            cat_data["serfs_assigned"] = deposit_counts.get(category, 0)

        # Shafts
        for category, shaft_data in getattr(self, "shaft_categories", {}).items():
            shaft_data["serfs_assigned"] = shaft_counts.get(category, 0)
            pos_map = shaft_serfs_by_pos.get(category, {})
            for shaft in shaft_data.get("shafts", []):
                key = self._pos_key_from_xy(shaft.get("x", 0), shaft.get("y", 0))
                shaft["serfs_assigned"] = pos_map.get(key, 0)

        for category in ["Eisen", "Stein", "Lehm", "Schwefel"]:
            raw_name = category_to_raw.get(category)
            if raw_name:
                self.resource_workers[raw_name] = resource_counts_raw.get(raw_name, 0)

        # Miner zu Rohstoff-Workern addieren
        raw_type_to_name = {
            ResourceType.WOOD_RAW: RESOURCE_HOLZ_ROH,
            ResourceType.STONE_RAW: RESOURCE_STEIN_ROH,
            ResourceType.CLAY_RAW: RESOURCE_LEHM_ROH,
            ResourceType.IRON_RAW: RESOURCE_EISEN_ROH,
            ResourceType.SULFUR_RAW: RESOURCE_SCHWEFEL_ROH,
            ResourceType.GOLD_RAW: RESOURCE_GOLD_ROH,
        }
        for mine in getattr(self.production_system, "mines", {}).values():
            res_name = raw_type_to_name.get(mine.resource_type)
            if res_name and res_name in self.resource_workers:
                self.resource_workers[res_name] += mine.current_workers

        # Refiner-Worker fÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¼r veredelte Ressourcen
        refined_type_to_name = {
            ResourceType.WOOD: RESOURCE_HOLZ,
            ResourceType.STONE: RESOURCE_STEIN,
            ResourceType.CLAY: RESOURCE_LEHM,
            ResourceType.IRON: RESOURCE_EISEN,
            ResourceType.SULFUR: RESOURCE_SCHWEFEL,
            ResourceType.GOLD: RESOURCE_TALER,
        }
        for refiner in getattr(self.production_system, "refiners", {}).values():
            res_name = refined_type_to_name.get(refiner.resource_type)
            if res_name and res_name in self.resource_workers:
                self.resource_workers[res_name] += refiner.current_workers

        self._building_serfs_count = building_count

    def _build_and_assign(self, source_area, quantity, building, build_position: Optional[dict] = None):
        """Baut Gebaeude und weist Leibeigene direkt der neuen Baustelle zu."""
        if not self._can_build(building):
            return 0.0
        site_count_before = len(self.construction_sites)
        reward = self._build_building(building, position=build_position)

        # Zaehler nicht nur umbuchen: echte Serf-Objekte zur Baustelle schicken.
        if len(self.construction_sites) > site_count_before and source_area == SerfArea.FREE:
            available = self.serf_areas.get(source_area, {}).get("count", 0)
            actual = min(quantity, available)
            if actual > 0:
                newest_site_index = len(self.construction_sites) - 1
                self._assign_serf_to_construction_site(SerfArea.FREE, actual, newest_site_index)

        return reward

    def _recall_serfs_from_construction_site(self, site_index: int, quantity: int) -> int:
        if site_index < 0 or site_index >= len(self.construction_sites):
            return 0
        site = self.construction_sites[site_index]
        recalled = 0
        for serf in self.production_system.serfs:
            if recalled >= quantity:
                break
            if serf.build_site_id == site.get("site_id"):
                serf.stop()
                recalled += 1
        if recalled:
            site["serfs_assigned"] = max(0, int(site.get("serfs_assigned", 0) or 0) - recalled)
            self.free_leibeigene += recalled
        return recalled

    def _recall_serfs_from_selection(self, src_cat: int, src_spec: int, quantity: int) -> int:
        quantity = max(0, int(quantity))
        if quantity <= 0:
            return 0
        if src_cat == 0:
            return min(quantity, self.free_leibeigene)
        if src_cat == 1:
            return self._recall_wood_tree_batch(src_spec, quantity)
        if src_cat in CATEGORY_AREA_MAP:
            area = self._resolve_area(src_cat, src_spec)
            return self._recall_serfs_from_specific_area(area, quantity)
        if src_cat == 6:
            return self._recall_serfs_from_construction_site(src_spec, quantity)
        return 0

    def _assign_serfs_to_selection(self, tgt_cat: int, tgt_spec: int, quantity: int, selections: dict) -> float:
        quantity = max(0, int(quantity))
        if quantity <= 0:
            return 0.0
        if tgt_cat == 0:
            return 0.0
        if tgt_cat == 1:
            if tgt_spec < len(self.tree_list_internal):
                self._assign_wood_tree_batch(tgt_spec, quantity)
            return 0.0
        if tgt_cat in CATEGORY_AREA_MAP:
            area = self._resolve_area(tgt_cat, tgt_spec)
            self._assign_serfs_to_specific_area(area, quantity)
            return 0.0
        if tgt_cat == 6:
            self._assign_serf_to_construction_site(SerfArea.FREE, quantity, tgt_spec)
            return 0.0
        if tgt_cat == 7:
            if tgt_spec >= len(self.buildable_buildings):
                return 0.0
            building = self.buildable_buildings[tgt_spec]
            build_pos = self._select_build_position(building, selections)
            if build_pos is None:
                return 0.0
            return self._build_and_assign(SerfArea.FREE, quantity, building, build_position=build_pos)
        return 0.0

    def _execute_action(self, action_name, selections):
        """Fuehrt die komplette Aktion aus basierend auf Selections."""
        if action_name == "wait":
            return 0.0
        elif action_name == "upgrade":
            building_idx = self._to_int_choice(selections.get(ActionPhase.BUILDING, 0), 0)
            if building_idx < len(self.upgradeable_buildings):
                building = self.upgradeable_buildings[building_idx]
                if self._can_upgrade(building):
                    pos_key = self._select_building_instance_key(building, selections)
                    return self._upgrade_building(building, pos_key)
            return 0.0
        elif action_name == "research":
            building_idx = self._to_int_choice(selections.get(ActionPhase.TECH_BUILDING, 0), 0)
            tech_idx = self._to_int_choice(selections.get(ActionPhase.TECH, 0), 0)
            building = RESEARCH_BUILDINGS[min(building_idx, len(RESEARCH_BUILDINGS) - 1)]
            techs = self.tech_by_building.get(building, [])
            if tech_idx < len(techs):
                tech = techs[tech_idx]
                if self._can_research(tech):
                    return self._research_tech(tech)
            return 0.0
        elif action_name == "recruit":
            soldier_idx = self._to_int_choice(selections.get(ActionPhase.SOLDIER, 0), 0)
            quantity_idx = self._to_int_choice(selections.get(ActionPhase.QUANTITY, 0), 0)
            quantity = [1, 2, 3, 5, 10, 20][min(quantity_idx, 5)]
            if soldier_idx < len(self.soldier_types):
                soldier = self.soldier_types[soldier_idx]
                reward = 0.0
                for _ in range(quantity):
                    if self._can_recruit(soldier):
                        reward += self._recruit_soldier(soldier)
                return reward
            return 0.0
        elif action_name == "buy_serf":
            quantity_idx = self._to_int_choice(selections.get(ActionPhase.QUANTITY, 0), 0)
            quantity = [1, 2, 3, 5, 10, 20][min(quantity_idx, 5)]
            reward = 0.0
            for _ in range(quantity):
                if self._can_buy_serf():
                    reward += self._buy_serf()
            return reward
        elif action_name == "dismiss_serf":
            src_cat = self._to_int_choice(selections.get(ActionPhase.SOURCE_CATEGORY, 0), 0)
            src_spec = self._to_int_choice(selections.get(ActionPhase.SOURCE_SPECIFIC, 0), 0)
            quantity_idx = self._to_int_choice(selections.get(ActionPhase.QUANTITY, 0), 0)
            quantity = [1, 2, 3, 5, 10, 20][min(quantity_idx, 5)]
            if src_cat == 0:
                reward = 0.0
                for _ in range(quantity):
                    if self._can_dismiss_serf_from_area(SerfArea.FREE):
                        reward += self._dismiss_serf_from_area(SerfArea.FREE)
                return reward
            recalled = self._recall_serfs_from_selection(src_cat, src_spec, quantity)
            reward = 0.0
            for _ in range(recalled):
                if self._can_dismiss_serf_from_area(SerfArea.FREE):
                    reward += self._dismiss_serf_from_area(SerfArea.FREE)
            return reward
        elif action_name == "assign_serf":
            src_cat = self._to_int_choice(selections.get(ActionPhase.SOURCE_CATEGORY, 0), 0)
            src_spec = self._to_int_choice(selections.get(ActionPhase.SOURCE_SPECIFIC, 0), 0)
            qty_idx = self._to_int_choice(selections.get(ActionPhase.QUANTITY, 0), 0)
            tgt_cat = self._to_int_choice(selections.get(ActionPhase.TARGET_CATEGORY, 0), 0)
            tgt_spec = self._to_int_choice(selections.get(ActionPhase.TARGET_SPECIFIC, 0), 0)
            quantity = [1, 2, 3, 5, 10, 20][min(qty_idx, 5)]
            if src_cat == 0:
                free_before = int(self.free_leibeigene)
                reward = float(self._assign_serfs_to_selection(tgt_cat, tgt_spec, quantity, selections))
                assigned_from_free = max(0, free_before - int(self.free_leibeigene))
                reward += self._reward_for_assigning_spawned_serfs(assigned_from_free)
                return reward
            if tgt_cat == 0:
                return 0.0
            moved = self._recall_serfs_from_selection(src_cat, src_spec, quantity)
            return self._assign_serfs_to_selection(tgt_cat, tgt_spec, moved, selections)
        elif action_name == "demolish":
            building_idx = self._to_int_choice(selections.get(ActionPhase.BUILDING, 0), 0)
            if building_idx < len(self.demolishable_buildings):
                building = self.demolishable_buildings[building_idx]
                if self._can_demolish(building):
                    pos_key = self._select_building_instance_key(building, selections)
                    return self._demolish_building(building, pos_key)
            return 0.0
        elif action_name == "bless":
            category_idx = self._to_int_choice(selections.get(ActionPhase.CATEGORY, 0), 0)
            if category_idx in BLESS_CATEGORIES and self._can_bless(category_idx):
                return self._bless(category_idx)
            return 0.0
        elif action_name == "tax":
            tax_level = self._to_int_choice(selections.get(ActionPhase.TAX_LEVEL, 0), 0)
            if tax_level != self.current_tax_level and tax_level in TAX_LEVELS:
                return self._set_tax_level(tax_level)
            return 0.0
        elif action_name == "alarm":
            on_off = self._to_int_choice(selections.get(ActionPhase.ON_OFF, 0), 0)
            if on_off == 0:
                if not self.alarm_active and self.alarm_cooldown <= 0:
                    self.alarm_active = True
                    # ForceToWorkPenalty (Logic.xml): Motivation sinkt wenn Worker zur Arbeit gezwungen werden
                    if any(w.state != WorkerState.WORKING for w in self.workforce_manager.workers):
                        self.base_motivation = max(0.25, self.base_motivation - FORCE_TO_WORK_PENALTY)
            else:
                if self.alarm_active:
                    self.alarm_active = False
                    self.alarm_cooldown = self._get_alarm_recharge_time()
            return 0.0
        return 0.0

    def _do_assign_serf(self, source_idx, quantity, target_idx):
        """Leibeigene von source_area nach target_area verschieben."""
        source_area = next((a for a in SerfArea if a.value == source_idx), None)
        target_area = next((a for a in SerfArea if a.value == target_idx), None)
        if source_area is None or target_area is None:
            return 0.0

        available = self.serf_areas.get(source_area, {}).get("count", 0)
        actual_quantity = min(quantity, available)
        if actual_quantity <= 0:
            return 0.0

        wood_zone_map = {
            SerfArea.WOOD_HQ: 0,
            SerfArea.WOOD_SULFUR: 1,
            SerfArea.WOOD_CLAY: 2,
            SerfArea.WOOD_STONE: 3,
            SerfArea.WOOD_VILLAGE: 4,
            SerfArea.WOOD_IRON: 5,
        }
        shaft_type_map = {
            SerfArea.SHAFT_IRON_1: "Eisen",
            SerfArea.SHAFT_IRON_2: "Eisen",
            SerfArea.SHAFT_IRON_3: "Eisen",
            SerfArea.SHAFT_STONE_1: "Stein",
            SerfArea.SHAFT_STONE_2: "Stein",
            SerfArea.SHAFT_STONE_3: "Stein",
            SerfArea.SHAFT_CLAY_1: "Lehm",
            SerfArea.SHAFT_CLAY_2: "Lehm",
            SerfArea.SHAFT_CLAY_3: "Lehm",
            SerfArea.SHAFT_SULFUR_1: "Schwefel",
            SerfArea.SHAFT_SULFUR_2: "Schwefel",
            SerfArea.SHAFT_SULFUR_3: "Schwefel",
        }
        deposit_type_map = {
            SerfArea.DEPOSIT_IRON_1: "Eisen",
            SerfArea.DEPOSIT_IRON_2: "Eisen",
            SerfArea.DEPOSIT_STONE_1: "Stein",
            SerfArea.DEPOSIT_STONE_2: "Stein",
            SerfArea.DEPOSIT_CLAY_1: "Lehm",
            SerfArea.DEPOSIT_SULFUR_1: "Schwefel",
            SerfArea.DEPOSIT_SULFUR_2: "Schwefel",
        }

        # Quelle "Frei" -> echte Assign-Operationen fÃƒÆ’Ã‚Â¼r Holz/Deposits/Shafts ausfÃƒÆ’Ã‚Â¼hren.
        if source_area == SerfArea.FREE:
            if target_area in wood_zone_map:
                zone_idx = wood_zone_map[target_area]
                if zone_idx < len(self.wood_zone_names):
                    zone_name = self.wood_zone_names[zone_idx]
                    if self._can_assign_wood_zone_batch(zone_name, actual_quantity):
                        self._assign_wood_zone_batch(zone_name, actual_quantity)
                return 0.0
            if target_area in shaft_type_map:
                shaft_type = shaft_type_map[target_area]
                if self._can_assign_shaft_batch(shaft_type, actual_quantity):
                    self._assign_shaft_batch(shaft_type, actual_quantity)
                return 0.0
            if target_area in deposit_type_map:
                deposit_type = deposit_type_map[target_area]
                if self._can_assign_deposit_batch(deposit_type, actual_quantity):
                    self._assign_deposit_batch(deposit_type, actual_quantity)
                return 0.0

        # Ziel "Frei" -> echte Recall-Operationen ausfÃƒÆ’Ã‚Â¼hren.
        if target_area == SerfArea.FREE:
            if source_area in wood_zone_map:
                zone_idx = wood_zone_map[source_area]
                if zone_idx < len(self.wood_zone_names):
                    zone_name = self.wood_zone_names[zone_idx]
                    if self._can_recall_wood_zone_batch(zone_name, actual_quantity):
                        self._recall_wood_zone_batch(zone_name, actual_quantity)
                return 0.0
            if source_area in shaft_type_map:
                shaft_type = shaft_type_map[source_area]
                if self._can_recall_shaft_batch(shaft_type, actual_quantity):
                    self._recall_shaft_batch(shaft_type, actual_quantity)
                return 0.0
            if source_area in deposit_type_map:
                deposit_type = deposit_type_map[source_area]
                if self._can_recall_deposit_batch(deposit_type, actual_quantity):
                    self._recall_deposit_batch(deposit_type, actual_quantity)
                return 0.0

        # Fallback: reine ZÃƒÆ’Ã‚Â¤hler-Umbuchung fÃƒÆ’Ã‚Â¼r sonstige Kombinationen.
        self.serf_areas[source_area]["count"] = max(0, self.serf_areas[source_area].get("count", 0) - actual_quantity)
        if target_area not in self.serf_areas:
            self.serf_areas[target_area] = {"count": 0}
        self.serf_areas[target_area]["count"] += actual_quantity

        if source_area == SerfArea.FREE:
            self.free_leibeigene = max(0, self.free_leibeigene - actual_quantity)
        if target_area == SerfArea.FREE:
            self.free_leibeigene += actual_quantity
        return 0.0

    def _assign_serf_to_construction_site(self, source_area: SerfArea, quantity: int, site_index: int) -> int:
        """Weist Serfs zu einer spezifischen Baustelle zu."""
        from worker_simulation import Position

        if source_area != SerfArea.FREE:
            return 0
        if site_index < 0 or site_index >= len(self.construction_sites):
            return 0
        if self.free_leibeigene <= 0:
            return 0

        target_site = self.construction_sites[site_index]
        already_assigned = int(target_site.get("serfs_assigned", 0) or 0)
        capacity_left = max(0, MAX_ACTIVE_BUILDERS_PER_SITE - already_assigned)
        if capacity_left <= 0:
            return 0

        requested = min(int(quantity), capacity_left)
        assigned = 0
        for serf in self.production_system.serfs:
            if assigned >= requested:
                break
            if serf.is_idle():
                pos = target_site.get("position")
                if pos:
                    build_pos = Position(x=pos["x"], y=pos["y"])
                else:
                    build_pos = Position(x=self.hq_position[0], y=self.hq_position[1])
                serf_pos = Position(x=serf.position.x, y=serf.position.y)
                self._assign_serf_to_build(
                    serf,
                    target_site["building"],
                    build_pos,
                    serf_pos,
                    target_site["site_id"]
                )
                assigned += 1

        if assigned <= 0:
            return 0

        target_site["serfs_assigned"] += assigned
        self.free_leibeigene = max(0, self.free_leibeigene - assigned)
        self.serf_areas[SerfArea.FREE]["count"] = self.free_leibeigene
        return int(assigned)

    def _get_local_action_mask_raw(self) -> np.ndarray:
        """Dynamische Maske fuer die aktuelle Phase (ohne zusaetzliche Zukunfts-Pruefung)."""
        if self.current_phase == ActionPhase.MAIN:
            return self._mask_main_actions()
        if self.current_phase == ActionPhase.BUILDING:
            return self._mask_buildings()
        if self.current_phase == ActionPhase.POSITION_GROUP:
            return self._mask_position_group()
        if self.current_phase == ActionPhase.POSITION_INDEX:
            return self._mask_position_index()
        if self.current_phase == ActionPhase.TECH_BUILDING:
            return self._mask_tech_building()
        if self.current_phase == ActionPhase.TECH:
            return self._mask_technologies()
        if self.current_phase == ActionPhase.SOLDIER:
            return self._mask_soldiers()
        if self.current_phase == ActionPhase.QUANTITY:
            return self._mask_quantity()
        if self.current_phase == ActionPhase.SOURCE_CATEGORY:
            return self._mask_source_category()
        if self.current_phase == ActionPhase.SOURCE_SPECIFIC:
            return self._mask_source_specific()
        if self.current_phase == ActionPhase.TARGET_CATEGORY:
            return self._mask_target_category()
        if self.current_phase == ActionPhase.TARGET_SPECIFIC:
            return self._mask_target_specific()
        if self.current_phase == ActionPhase.CATEGORY:
            return self._mask_bless_categories()
        if self.current_phase == ActionPhase.TAX_LEVEL:
            return self._mask_tax_levels()
        if self.current_phase == ActionPhase.ON_OFF:
            return self._mask_alarm_on_off()
        size = self.action_spaces[self.current_phase].n
        return np.ones(size, dtype=bool)

    def _get_flow_feasibility_cache(self) -> Dict[Tuple, bool]:
        cache_key = ("flow_feasibility_cache",)
        cache = self._get_can_cache(cache_key)
        if not isinstance(cache, dict):
            cache = {}
            self._set_can_cache(cache_key, cache)
        return cache

    def _serialize_flow_selections(self, flow_name: str, selections: Dict[ActionPhase, int]) -> Tuple[Tuple[str, int], ...]:
        flow_phases = ACTION_FLOWS.get(flow_name, [])
        serialized: List[Tuple[str, int]] = []
        for phase in flow_phases:
            if phase in selections:
                serialized.append((phase.value, self._to_int_choice(selections.get(phase, 0), 0)))
        return tuple(serialized)

    def _phase_feasibility_resolved_by_local_mask(
        self,
        flow_name: str,
        phase: ActionPhase,
        selections: Dict[ActionPhase, int],
    ) -> bool:
        """
        True, wenn eine lokale Phasenmaske bereits garantiert, dass ein gueltiger
        Choice zu einem vollstaendig ausfuehrbaren Flow fuehrt.
        """
        _ = selections
        if flow_name == "wait":
            return True
        if flow_name == "research":
            return phase in {ActionPhase.TECH_BUILDING, ActionPhase.TECH}
        if flow_name == "recruit":
            return phase in {ActionPhase.SOLDIER, ActionPhase.QUANTITY}
        if flow_name == "buy_serf":
            return phase == ActionPhase.QUANTITY
        if flow_name == "dismiss_serf":
            return phase == ActionPhase.QUANTITY
        if flow_name == "assign_serf":
            return phase in {
                ActionPhase.QUANTITY,
                ActionPhase.TARGET_CATEGORY,
                ActionPhase.TARGET_SPECIFIC,
                ActionPhase.POSITION_GROUP,
                ActionPhase.POSITION_INDEX,
            }
        if flow_name in {"upgrade", "demolish"}:
            return phase in {ActionPhase.BUILDING, ActionPhase.POSITION_GROUP, ActionPhase.POSITION_INDEX}
        if flow_name == "bless":
            return phase == ActionPhase.CATEGORY
        if flow_name == "tax":
            return phase == ActionPhase.TAX_LEVEL
        if flow_name == "alarm":
            return phase == ActionPhase.ON_OFF
        return False

    def _get_phase_mask_for_feasibility(
        self,
        flow_name: str,
        phase: ActionPhase,
        selections: Dict[ActionPhase, int],
    ) -> np.ndarray:
        cache = self._get_flow_feasibility_cache()
        mask_cache_key = (
            "phase_mask",
            flow_name,
            phase.value,
            self._serialize_flow_selections(flow_name, selections),
        )
        cached_mask = cache.get(mask_cache_key)
        if isinstance(cached_mask, np.ndarray):
            return np.asarray(cached_mask, dtype=bool).reshape(-1).copy()

        old_phase = self.current_phase
        old_flow = self.current_flow
        old_step = self.flow_step
        old_pending = dict(self.pending_selections)
        try:
            self.current_phase = phase
            self.current_flow = flow_name
            self.pending_selections = {
                key: self._to_int_choice(value, 0)
                for key, value in dict(selections).items()
            }
            mask = np.asarray(self._get_local_action_mask_raw(), dtype=bool).reshape(-1)
            cache[mask_cache_key] = mask.copy()
            return mask
        finally:
            self.current_phase = old_phase
            self.current_flow = old_flow
            self.flow_step = old_step
            self.pending_selections = old_pending

    def _advance_flow_prefix(
        self,
        flow_name: str,
        phase_idx: int,
        selections: Dict[ActionPhase, int],
        choice: int,
    ) -> Tuple[Dict[ActionPhase, int], int]:
        flow_phases = ACTION_FLOWS.get(flow_name, [])
        if phase_idx < 0 or phase_idx >= len(flow_phases):
            return dict(selections), len(flow_phases)

        current_phase = flow_phases[phase_idx]
        next_selections = {
            key: self._to_int_choice(value, 0)
            for key, value in dict(selections).items()
        }
        next_selections[current_phase] = int(choice)
        next_phase_idx = phase_idx + 1

        if current_phase == ActionPhase.SOURCE_CATEGORY and int(choice) == 0:
            next_selections[ActionPhase.SOURCE_SPECIFIC] = 0
            next_phase_idx += 1
        elif (
            current_phase == ActionPhase.TARGET_CATEGORY
            and int(choice) == 0
            and flow_name != "assign_serf"
        ):
            next_selections[ActionPhase.TARGET_SPECIFIC] = 0
            next_phase_idx += 1
        elif flow_name == "assign_serf" and current_phase == ActionPhase.TARGET_SPECIFIC:
            target_cat = self._to_int_choice(next_selections.get(ActionPhase.TARGET_CATEGORY, 0), 0)
            if target_cat != 7:
                next_selections[ActionPhase.POSITION_GROUP] = 0
                next_selections[ActionPhase.POSITION_INDEX] = 0
                next_phase_idx += 2

        return next_selections, next_phase_idx

    def _get_selected_batch_size_from_selections(self, selections: Dict[ActionPhase, int]) -> int:
        qty_idx = self._to_int_choice(selections.get(ActionPhase.QUANTITY, 0), 0)
        qty_idx = max(0, min(qty_idx, len(QUANTITY_VALUES) - 1))
        return int(QUANTITY_VALUES[qty_idx])

    def _get_available_free_for_assign(
        self,
        src_cat: int,
        batch_size: int,
    ) -> int:
        if src_cat == 0:
            return int(self.free_leibeigene)
        return int(max(self.free_leibeigene, batch_size))

    def _is_complete_flow_selection_feasible(
        self,
        flow_name: str,
        selections: Dict[ActionPhase, int],
    ) -> bool:
        if flow_name == "wait":
            return True

        if flow_name == "upgrade":
            building_idx = self._to_int_choice(selections.get(ActionPhase.BUILDING, 0), 0)
            if building_idx < 0 or building_idx >= len(self.upgradeable_buildings):
                return False
            building = self.upgradeable_buildings[building_idx]
            if not self._can_upgrade(building):
                return False
            return self._select_building_instance_key(building, selections) is not None

        if flow_name == "research":
            building_idx = self._to_int_choice(selections.get(ActionPhase.TECH_BUILDING, 0), 0)
            tech_idx = self._to_int_choice(selections.get(ActionPhase.TECH, 0), 0)
            if not RESEARCH_BUILDINGS:
                return False
            building = RESEARCH_BUILDINGS[min(max(0, building_idx), len(RESEARCH_BUILDINGS) - 1)]
            techs = self.tech_by_building.get(building, [])
            if tech_idx < 0 or tech_idx >= len(techs):
                return False
            return self._can_research(techs[tech_idx])

        if flow_name == "recruit":
            soldier_idx = self._to_int_choice(selections.get(ActionPhase.SOLDIER, 0), 0)
            if soldier_idx < 0 or soldier_idx >= len(self.soldier_types):
                return False
            soldier = self.soldier_types[soldier_idx]
            quantity = self._get_selected_batch_size_from_selections(selections)
            return self._can_recruit_batch(soldier, quantity)

        if flow_name == "buy_serf":
            quantity = self._get_selected_batch_size_from_selections(selections)
            return self._can_buy_serf_batch(quantity)

        if flow_name == "dismiss_serf":
            src_cat = self._to_int_choice(selections.get(ActionPhase.SOURCE_CATEGORY, 0), 0)
            src_spec = self._to_int_choice(selections.get(ActionPhase.SOURCE_SPECIFIC, 0), 0)
            quantity = self._get_selected_batch_size_from_selections(selections)
            return self._can_use_source_batch(src_cat, src_spec, quantity)

        if flow_name == "assign_serf":
            src_cat = self._to_int_choice(selections.get(ActionPhase.SOURCE_CATEGORY, 0), 0)
            src_spec = self._to_int_choice(selections.get(ActionPhase.SOURCE_SPECIFIC, 0), 0)
            tgt_cat = self._to_int_choice(selections.get(ActionPhase.TARGET_CATEGORY, 0), 0)
            tgt_spec = self._to_int_choice(selections.get(ActionPhase.TARGET_SPECIFIC, 0), 0)
            quantity = self._get_selected_batch_size_from_selections(selections)

            if not self._can_use_source_batch(src_cat, src_spec, quantity):
                return False

            if tgt_cat == 0:
                return False

            available_free = self._get_available_free_for_assign(src_cat=src_cat, batch_size=quantity)
            if available_free <= 0:
                return False

            if tgt_cat == 1:
                if tgt_spec < 0 or tgt_spec >= len(self.tree_list_internal):
                    return False
                return self._can_assign_wood_tree_batch(
                    tgt_spec,
                    quantity,
                    available_free_override=available_free,
                )

            if tgt_cat in CATEGORY_AREA_MAP:
                areas = CATEGORY_AREA_MAP.get(tgt_cat, [])
                if tgt_spec < 0 or tgt_spec >= len(areas):
                    return False
                return self._can_assign_serf_to_specific_area(
                    areas[tgt_spec],
                    quantity,
                    available_free_override=available_free,
                )

            if tgt_cat == 6:
                if tgt_spec < 0 or tgt_spec >= len(self.construction_sites):
                    return False
                already_assigned = int(self.construction_sites[tgt_spec].get("serfs_assigned", 0) or 0)
                return already_assigned < MAX_ACTIVE_BUILDERS_PER_SITE

            if tgt_cat == 7:
                if tgt_spec < 0 or tgt_spec >= len(self.buildable_buildings):
                    return False
                building = self.buildable_buildings[tgt_spec]
                if not self._can_build(building):
                    return False
                return self._select_build_position(building, selections) is not None

            return False

        if flow_name == "demolish":
            building_idx = self._to_int_choice(selections.get(ActionPhase.BUILDING, 0), 0)
            if building_idx < 0 or building_idx >= len(self.demolishable_buildings):
                return False
            building = self.demolishable_buildings[building_idx]
            if not self._can_demolish(building):
                return False
            return self._select_building_instance_key(building, selections) is not None

        if flow_name == "bless":
            category_idx = self._to_int_choice(selections.get(ActionPhase.CATEGORY, 0), 0)
            return category_idx in BLESS_CATEGORIES and self._can_bless(category_idx)

        if flow_name == "tax":
            tax_level = self._to_int_choice(selections.get(ActionPhase.TAX_LEVEL, 0), 0)
            return tax_level != self.current_tax_level and tax_level in TAX_LEVELS

        if flow_name == "alarm":
            on_off = self._to_int_choice(selections.get(ActionPhase.ON_OFF, 0), 0)
            if on_off == 0:
                return (not self.alarm_active) and (self.alarm_cooldown <= 0)
            if on_off == 1:
                return bool(self.alarm_active)
            return False

        return False

    def _has_feasible_flow_completion(
        self,
        flow_name: str,
        phase_idx: int,
        selections: Dict[ActionPhase, int],
        cache: Dict[Tuple, bool],
    ) -> bool:
        flow_phases = ACTION_FLOWS.get(flow_name, [])
        if phase_idx >= len(flow_phases):
            return self._is_complete_flow_selection_feasible(flow_name, selections)

        cache_key = (
            "flow_completion",
            flow_name,
            int(phase_idx),
            self._serialize_flow_selections(flow_name, selections),
        )
        cached = cache.get(cache_key)
        if cached is not None:
            return bool(cached)

        phase = flow_phases[phase_idx]
        mask = self._get_phase_mask_for_feasibility(flow_name, phase, selections)
        if self._phase_feasibility_resolved_by_local_mask(flow_name, phase, selections):
            feasible = bool(np.any(mask))
            cache[cache_key] = bool(feasible)
            return bool(feasible)

        feasible = False
        for choice in np.flatnonzero(mask):
            next_selections, next_phase_idx = self._advance_flow_prefix(
                flow_name=flow_name,
                phase_idx=phase_idx,
                selections=selections,
                choice=int(choice),
            )
            if self._has_feasible_flow_completion(flow_name, next_phase_idx, next_selections, cache):
                feasible = True
                break
        cache[cache_key] = bool(feasible)
        return bool(feasible)

    def _filter_mask_by_future_feasibility(self, mask: np.ndarray) -> np.ndarray:
        """Filtert aktuelle Maskenwerte auf echte Zukunfts-Erreichbarkeit."""
        mask = np.asarray(mask, dtype=bool).reshape(-1)
        if mask.size <= 0:
            return mask

        filtered = np.zeros_like(mask, dtype=bool)
        cache = self._get_flow_feasibility_cache()

        if self.current_phase == ActionPhase.MAIN:
            # Die MAIN-Maske ist bereits ueber spezifische _can_* Checks vollstaendig
            # zukunftsfeasible; rekursive Nachpruefung waere redundant.
            return mask

        flow_name = self.current_flow
        flow_phases = ACTION_FLOWS.get(flow_name, []) if flow_name else []
        if not flow_name or self.current_phase not in flow_phases:
            return mask

        phase_idx = flow_phases.index(self.current_phase)
        selections = {
            key: self._to_int_choice(value, 0)
            for key, value in dict(self.pending_selections).items()
        }
        if self._phase_feasibility_resolved_by_local_mask(flow_name, self.current_phase, selections):
            return mask

        for idx in np.flatnonzero(mask):
            idx = int(idx)
            next_selections, next_phase_idx = self._advance_flow_prefix(
                flow_name=flow_name,
                phase_idx=phase_idx,
                selections=selections,
                choice=idx,
            )
            filtered[idx] = self._has_feasible_flow_completion(
                flow_name=flow_name,
                phase_idx=next_phase_idx,
                selections=next_selections,
                cache=cache,
            )
        return filtered

    def _get_local_action_mask(self) -> np.ndarray:
        """Dynamische Maske fuer die aktuelle Phase mit kompletter Zukunfts-Pruefung."""
        pending_serialized: Tuple[Tuple[str, int], ...] = tuple(
            sorted(
                (str(getattr(key, "value", key)), self._to_int_choice(value, 0))
                for key, value in dict(self.pending_selections).items()
            )
        )
        cache_key = (
            "local_action_mask",
            str(getattr(self.current_phase, "value", self.current_phase)),
            str(self.current_flow) if self.current_flow is not None else "",
            int(self.flow_step),
            pending_serialized,
        )
        cached = self._get_can_cache(cache_key)
        if isinstance(cached, np.ndarray):
            return np.asarray(cached, dtype=bool).copy()

        raw_mask = self._get_local_action_mask_raw()
        filtered = self._filter_mask_by_future_feasibility(raw_mask)
        self._set_can_cache(cache_key, np.asarray(filtered, dtype=bool).copy())
        return filtered

    def _pad_action_mask(self, mask: np.ndarray) -> np.ndarray:
        """Pad/clip mask to fixed action_space size."""
        full = np.zeros(self.max_action_size, dtype=bool)
        size = min(len(mask), self.max_action_size)
        if size > 0:
            full[:size] = mask[:size]
        if not full.any():
            full[0] = True
        return full

    def action_masks(self):
        """Dynamische Maske basierend auf aktueller Phase (auf max size gepadded)."""
        local = self._get_local_action_mask()
        return self._pad_action_mask(local)

    def get_action_head_sizes(self):
        """Gibt die Action-GrÃƒÆ’Ã‚Â¶ÃƒÆ’Ã…Â¸en pro Phase in Enum-Reihenfolge zurÃƒÆ’Ã‚Â¼ck."""
        return [self.action_spaces[phase].n for phase in self.phase_list]

    def _mask_main_actions(self):
        """Maske fuer die 11 Hauptaktionen (build in assign_serf integriert)."""
        cache_key = ("mask_main_actions",)
        cached = self._get_can_cache(cache_key)
        if isinstance(cached, np.ndarray):
            return np.asarray(cached, dtype=bool).copy()

        # MAIN_ACTIONS = [wait, upgrade, research, recruit, buy_serf, dismiss_serf, assign_serf, demolish, bless, tax, alarm]
        n = len(MAIN_ACTIONS)
        mask = np.ones(n, dtype=bool)
        can_upgrade_any = any(self._can_upgrade(b) for b in self.upgradeable_buildings)
        has_university = (
            self.buildings.get("Hochschule_1", 0) > 0
            or self.buildings.get("Hochschule_2", 0) > 0
        )
        can_research_any = has_university and self._can_research_any()
        can_recruit_any = any(self._can_recruit(s) for s in self.soldier_types)
        can_demolish_any = any(self._can_demolish(b) for b in self.demolishable_buildings)
        for i, action_name in enumerate(MAIN_ACTIONS):
            if action_name == "wait":
                mask[i] = True
            elif action_name == "upgrade":
                mask[i] = can_upgrade_any
            elif action_name == "research":
                mask[i] = can_research_any
            elif action_name == "recruit":
                mask[i] = can_recruit_any
            elif action_name == "buy_serf":
                mask[i] = self._can_buy_serf()
            elif action_name == "dismiss_serf":
                mask[i] = self._can_dismiss_serf()
            elif action_name == "assign_serf":
                mask[i] = self._can_assign_serf_action(batch_size=1)
            elif action_name == "demolish":
                mask[i] = can_demolish_any
            elif action_name == "bless":
                mask[i] = self._can_bless()
            elif action_name == "tax":
                mask[i] = any(level != self.current_tax_level for level in TAX_LEVELS.keys())
            elif action_name == "alarm":
                mask[i] = (self.alarm_active or (not self.alarm_active and self.alarm_cooldown <= 0))
        self._set_can_cache(cache_key, mask.copy())
        return mask

    def _mask_buildings(self):
        """Maske fuer Gebaeude-Auswahl (upgrade/demolish)."""
        cache_key = ("mask_buildings", str(self.current_flow))
        cached = self._get_can_cache(cache_key)
        if isinstance(cached, np.ndarray):
            return np.asarray(cached, dtype=bool).copy()

        size = self.action_spaces[ActionPhase.BUILDING].n
        if self.current_flow == "upgrade":
            mask = np.zeros(size, dtype=bool)
            for i, b in enumerate(self.upgradeable_buildings):
                if i < size:
                    mask[i] = self._can_upgrade(b)
            self._set_can_cache(cache_key, mask.copy())
            return mask
        elif self.current_flow == "demolish":
            mask = np.zeros(size, dtype=bool)
            for i, b in enumerate(self.demolishable_buildings):
                if i < size:
                    mask[i] = self._can_demolish(b)
            self._set_can_cache(cache_key, mask.copy())
            return mask
        mask = np.ones(size, dtype=bool)
        self._set_can_cache(cache_key, mask.copy())
        return mask

    def _get_building_instance_keys(self, building: str) -> List[str]:
        """Gibt alle Instanz-Keys fuer ein Gebaeude in stabiler Reihenfolge (mit Caching)."""
        cache_key = ("building_keys", building, frozenset(self.upgrading_positions))
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return cached
        result = [
            key
            for key in self.building_position_map.keys()
            if key.startswith(building) and key not in self.upgrading_positions
        ]
        self._set_can_cache(cache_key, result)
        return result

    def _get_position_phase_building(self, building_idx: int) -> Optional[str]:
        """Loest Building-Index fuer Positionsphasen (upgrade/demolish/build) auf."""
        if self.current_flow == "upgrade":
            building_list = self.upgradeable_buildings
        elif self.current_flow == "demolish":
            building_list = self.demolishable_buildings
        elif self.current_flow == "assign_serf":
            if self.pending_selections.get(ActionPhase.TARGET_CATEGORY) != 7:
                return None
            building_list = self.buildable_buildings
            building_idx = self.pending_selections.get(ActionPhase.TARGET_SPECIFIC, 0)
        else:
            return None
        if building_idx < len(building_list):
            return building_list[building_idx]
        return None

    def _get_build_position_candidates(self, building: str) -> List[dict]:
        if self._is_building_forbidden_by_rules(building):
            return []
        b_info = buildings_db.get(building, {})
        base_name = get_base_building_name(building)
        candidates = []
        seen = set()

        def _add_candidate(x, y, slot_candidate=False):
            key = (int(round(x)), int(round(y)))
            if key in seen:
                return
            seen.add(key)
            candidates.append({"x": key[0], "y": key[1], "_slot_candidate": bool(slot_candidate)})

        if b_info.get("mine_type"):
            mine_type = b_info["mine_type"]
            built_keys = {
                self._pos_key_from_position(pos)
                for pos in self.built_mines.get(mine_type, [])
            }
            for pos in self.mine_positions.get(mine_type, []):
                pos_key = self._pos_key_from_position(pos)
                if pos_key in built_keys:
                    continue
                _add_candidate(pos["x"], pos["y"], slot_candidate=True)
            return candidates

        if base_name == "Dorfzentrum":
            for slot in self.dz_slots:
                if slot.get("status") == "free":
                    _add_candidate(slot["x"], slot["y"], slot_candidate=True)
            return candidates

        return self._find_candidate_build_positions(building, limit=MAX_POSITION_SLOTS)

    def _mask_position_group(self):
        """Maske fuer Positions-Gruppen (upgrade/demolish/build)."""
        mask = np.zeros(POSITION_GROUP_COUNT, dtype=bool)
        building = self._get_position_phase_building(self.pending_selections.get(ActionPhase.BUILDING, 0))
        if building:
            if self.current_flow == "assign_serf":
                count = len(self._get_build_position_candidates(building))
            else:
                count = len(self._get_building_instance_keys(building))
            if count > 0:
                group_count = (count + POSITION_GROUP_SIZE - 1) // POSITION_GROUP_SIZE
                group_count = min(group_count, POSITION_GROUP_COUNT)
                for i in range(group_count):
                    mask[i] = True

        if not mask.any():
            mask[0] = True  # Fallback
        return mask

    def _mask_position_index(self):
        """Maske fuer Positions-Index innerhalb der gewaehlten Gruppe."""
        mask = np.zeros(POSITION_GROUP_SIZE, dtype=bool)
        group_idx = self.pending_selections.get(ActionPhase.POSITION_GROUP, 0)
        building = self._get_position_phase_building(self.pending_selections.get(ActionPhase.BUILDING, 0))
        if building:
            if self.current_flow == "assign_serf":
                keys = self._get_build_position_candidates(building)
            else:
                keys = self._get_building_instance_keys(building)
            start = max(0, group_idx) * POSITION_GROUP_SIZE
            available = max(0, min(POSITION_GROUP_SIZE, len(keys) - start))
            for i in range(available):
                mask[i] = True

        if not mask.any():
            mask[0] = True  # Fallback
        return mask

    def _select_building_instance_key(self, building: str, selections: dict) -> Optional[str]:
        """Waehlt einen Instanz-Key basierend auf Gruppen/Index-Auswahl."""
        keys = self._get_building_instance_keys(building)
        if not keys:
            return None
        group_idx = selections.get(ActionPhase.POSITION_GROUP, 0)
        index_idx = selections.get(ActionPhase.POSITION_INDEX, 0)
        global_idx = max(0, group_idx) * POSITION_GROUP_SIZE + max(0, index_idx)
        if global_idx >= len(keys):
            global_idx = len(keys) - 1
        return keys[global_idx]

    def _select_build_position(self, building: str, selections: dict) -> Optional[dict]:
        """Waehlt eine konkrete Bauposition basierend auf Gruppen/Index-Auswahl."""
        candidates = self._get_build_position_candidates(building)
        if not candidates:
            return None
        group_idx = selections.get(ActionPhase.POSITION_GROUP, 0)
        index_idx = selections.get(ActionPhase.POSITION_INDEX, 0)
        global_idx = max(0, group_idx) * POSITION_GROUP_SIZE + max(0, index_idx)
        if global_idx >= len(candidates):
            global_idx = len(candidates) - 1
        pos = candidates[global_idx]
        return {
            "x": int(round(pos["x"])),
            "y": int(round(pos["y"])),
            "_slot_candidate": bool(pos.get("_slot_candidate", False)),
        }

    def _update_building_position_key(self, old_key: str, new_building: str) -> Optional[str]:
        """Aktualisiert building_position_map bei Upgrade (gleicher Ort, neuer Typ)."""
        if old_key not in self.building_position_map:
            return None
        pos = self.building_position_map.pop(old_key)
        parts = old_key.rsplit("_", 1)
        if len(parts) == 2 and parts[1].isdigit():
            new_key = f"{new_building}_{parts[1]}"
        else:
            new_key = f"{new_building}_{len(self.building_position_map)}"
        if new_key in self.building_position_map:
            new_key = f"{new_building}_{len(self.building_position_map)}"
        self.building_position_map[new_key] = pos
        if old_key in self.building_grid_ids:
            self.building_grid_ids[new_key] = self.building_grid_ids.pop(old_key)
        if old_key in self.building_runtime:
            self.building_runtime[new_key] = self.building_runtime.pop(old_key)
            self.building_runtime[new_key]["building"] = new_building
        self._mark_spatial_dirty("buildings")
        return new_key

    def _get_building_bounds(self, pos_x: float, pos_y: float, building_type: str) -> Tuple[float, float, float, float]:
        """World-AABB fÃƒÆ’Ã‚Â¼r ein GebÃƒÆ’Ã‚Â¤udezentrum (x, y) berechnen."""
        base_name = get_base_building_name(building_type)
        width, height = BUILDING_FOOTPRINTS.get(base_name, (400, 400))
        half_w = float(width) / 2.0
        half_h = float(height) / 2.0
        return (
            float(pos_x) - half_w,
            float(pos_y) - half_h,
            float(pos_x) + half_w,
            float(pos_y) + half_h,
        )

    def _bounds_overlap(
        self,
        bounds_a: Tuple[float, float, float, float],
        bounds_b: Tuple[float, float, float, float],
    ) -> bool:
        ax1, ay1, ax2, ay2 = bounds_a
        bx1, by1, bx2, by2 = bounds_b
        return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1

    def _is_position_free(
        self,
        pos_x,
        pos_y,
        building_type,
        extra_reserved: Optional[List[Tuple[float, float, str]]] = None,
    ):
        """PrÃƒÆ’Ã‚Â¼ft, ob ein GebÃƒÆ’Ã‚Â¤ude am Standort gebaut werden kann (Terrain + Kollisionen)."""
        base_name = get_base_building_name(building_type)

        # Terrain-/Tree-/GebÃƒÆ’Ã‚Â¤ude-Check direkt auf dem Walkable-Grid.
        if hasattr(self, "map_manager") and self.map_manager:
            if not self.map_manager.can_build_at(float(pos_x), float(pos_y), base_name):
                return False

        new_bounds = self._get_building_bounds(pos_x, pos_y, building_type)

        # Baustellen reservieren FlÃƒÆ’Ã‚Â¤che bereits wÃƒÆ’Ã‚Â¤hrend des Baus.
        for site in self.construction_sites:
            site_pos = site.get("position")
            if not site_pos:
                continue
            sx = site_pos.get("x", 0) if isinstance(site_pos, dict) else site_pos[0]
            sy = site_pos.get("y", 0) if isinstance(site_pos, dict) else site_pos[1]
            site_building = site.get("building", "")
            site_bounds = self._get_building_bounds(sx, sy, site_building)
            if self._bounds_overlap(new_bounds, site_bounds):
                return False

        # ZusÃƒÆ’Ã‚Â¤tzliche reservierte Kandidaten (fÃƒÆ’Ã‚Â¼r Batch-ZÃƒÆ’Ã‚Â¤hlung).
        if extra_reserved:
            for rx, ry, r_building in extra_reserved:
                r_bounds = self._get_building_bounds(rx, ry, r_building)
                if self._bounds_overlap(new_bounds, r_bounds):
                    return False

        return True

    def _check_zone_b_unlock(self):
        """Prueft ob Zone-B Positionen freigeschaltet werden koennen.

        Zone-B Positionen werden frei wenn genuegend Baeume in der Naehe
        gefaellt wurden (trees_to_remove).
        """
        if not self.zone_b_positions:
            return

        # Zaehle gefaellte Baeume (leere Baeume in tree_list_internal)
        felled_positions = set()
        for tree in getattr(self, "tree_list_internal", []):
            if tree.get("resource_remaining", 1) <= 0:
                felled_positions.add((tree["x"], tree["y"]))

        # Pruefe jede Zone-B Position
        unlocked = []
        for i, pos in enumerate(self.zone_b_positions):
            trees_needed = pos.get("trees_to_remove", 1)
            px, py = pos["x"], pos["y"]

            # Zaehle gefaellte Baeume im Radius von 500 um die Position
            nearby_felled = 0
            for fx, fy in felled_positions:
                dist = abs(fx - px) + abs(fy - py)  # Manhattan-Distanz
                if dist < 1000:  # Radius fuer "nahe genug"
                    nearby_felled += 1

            if nearby_felled >= trees_needed:
                unlocked.append(i)

        # Freigeschaltete Positionen nach available_positions verschieben
        for i in reversed(unlocked):
            pos = self.zone_b_positions.pop(i)
            self.available_positions.append(pos)
        if unlocked:
            self._mark_spatial_dirty("available_slots")

    def _mask_tech_building(self):
        """Maske fuer Forschungs-Gebaeude-Auswahl: Welches Gebaeude hat erforschbare Techs?"""
        mask = np.zeros(len(RESEARCH_BUILDINGS), dtype=bool)
        for i, building in enumerate(RESEARCH_BUILDINGS):
            techs = self.tech_by_building.get(building, [])
            mask[i] = any(self._can_research(t) for t in techs)
        if not mask.any():
            mask[0] = True
        return mask

    def _mask_technologies(self):
        """Maske fuer Technologie-Auswahl innerhalb des gewaehlten Forschungs-Gebaeudes."""
        building_idx = self.pending_selections.get(ActionPhase.TECH_BUILDING, 0)
        building = RESEARCH_BUILDINGS[min(building_idx, len(RESEARCH_BUILDINGS) - 1)]
        techs = self.tech_by_building.get(building, [])
        mask = np.zeros(MAX_TECHS_PER_BUILDING, dtype=bool)
        for i, tech in enumerate(techs):
            if i < MAX_TECHS_PER_BUILDING:
                mask[i] = self._can_research(tech)
        if not mask.any():
            mask[0] = True
        return mask

    def _mask_soldiers(self):
        """Maske fuer Soldaten-Auswahl."""
        mask = np.zeros(len(self.soldier_types), dtype=bool)
        for i, soldier in enumerate(self.soldier_types):
            if i < mask.shape[0]:
                mask[i] = self._can_recruit(soldier)
        if not mask.any():
            mask[0] = True
        return mask

    def _mask_quantity(self):
        """Maske fuer Mengen-Auswahl (1,2,3,5,10,20)."""
        mask = np.zeros(len(QUANTITY_VALUES), dtype=bool)

        if self.current_flow == "buy_serf":
            for i, batch_size in enumerate(QUANTITY_VALUES):
                mask[i] = self._can_buy_serf_batch(batch_size)
            return mask

        if self.current_flow == "recruit":
            soldier_idx = self.pending_selections.get(ActionPhase.SOLDIER, 0)
            if 0 <= soldier_idx < len(self.soldier_types):
                soldier = self.soldier_types[soldier_idx]
                for i, batch_size in enumerate(QUANTITY_VALUES):
                    mask[i] = self._can_recruit_batch(soldier, batch_size)
            return mask

        if self.current_flow in {"dismiss_serf", "assign_serf"}:
            src_cat = int(self.pending_selections.get(ActionPhase.SOURCE_CATEGORY, 0) or 0)
            src_spec = int(self.pending_selections.get(ActionPhase.SOURCE_SPECIFIC, 0) or 0)
            for i, batch_size in enumerate(QUANTITY_VALUES):
                if not self._can_use_source_batch(src_cat, src_spec, batch_size):
                    continue
                if self.current_flow == "dismiss_serf":
                    mask[i] = True
                    continue

                if src_cat == 0:
                    available_free = self.free_leibeigene
                    mask[i] = self._has_assign_target_for_batch(
                        batch_size=batch_size,
                        available_free=available_free,
                        allow_target_free=False,  # FREE -> FREE waere ein No-Op.
                    )
                else:
                    available_free = max(self.free_leibeigene, batch_size)
                    mask[i] = self._has_assign_target_for_batch(
                        batch_size=batch_size,
                        available_free=available_free,
                        allow_target_free=False,
                    )
            return mask

        mask[:] = True
        return mask

    def _get_selected_batch_size(self) -> int:
        qty_idx = int(self.pending_selections.get(ActionPhase.QUANTITY, 0) or 0)
        return QUANTITY_VALUES[min(qty_idx, len(QUANTITY_VALUES) - 1)]

    def _can_use_source_batch(self, src_cat: int, src_spec: int, batch_size: int) -> bool:
        """Prueft, ob aus der gewaehlten Source mindestens `batch_size` Serfs bewegt werden koennen."""
        if batch_size <= 0:
            return False
        if src_cat == 0:
            return self.serf_areas.get(SerfArea.FREE, {}).get("count", 0) >= batch_size
        if src_cat == 1:
            return self._can_recall_wood_tree_batch(src_spec, batch_size)
        if src_cat in CATEGORY_AREA_MAP:
            area = self._resolve_area(src_cat, src_spec)
            return self._can_recall_from_specific_area(area, batch_size)
        if src_cat == 6:
            if src_spec < 0 or src_spec >= len(self.construction_sites):
                return False
            return int(self.construction_sites[src_spec].get("serfs_assigned", 0) or 0) >= batch_size
        return False

    def _has_nonfree_source_for_batch(self, batch_size: int) -> bool:
        cache_key = ("nonfree_source_batch", int(batch_size))
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return bool(cached)
        if batch_size <= 0:
            return self._set_can_cache(cache_key, False)
        if any(tree.get("serfs_assigned", 0) >= batch_size for tree in self.tree_list_internal):
            return self._set_can_cache(cache_key, True)
        for cat_idx in range(2, 6):
            for area in CATEGORY_AREA_MAP.get(cat_idx, []):
                if self._can_recall_from_specific_area(area, batch_size):
                    return self._set_can_cache(cache_key, True)
        if any(int(site.get("serfs_assigned", 0) or 0) >= batch_size for site in self.construction_sites):
            return self._set_can_cache(cache_key, True)
        return self._set_can_cache(cache_key, False)

    def _has_assignable_tree_for_batch(self, batch_size: int) -> bool:
        cache_key = ("assignable_tree_batch", int(batch_size))
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return bool(cached)
        if batch_size <= 0:
            return self._set_can_cache(cache_key, False)
        for tree in self.tree_list_internal:
            if (
                tree.get("resource_remaining", 0) > 0
                and tree.get("serfs_assigned", 0) + batch_size <= MAX_SERFS_PER_TREE
            ):
                return self._set_can_cache(cache_key, True)
        return self._set_can_cache(cache_key, False)

    def _has_assign_target_for_batch(self, batch_size: int, available_free: int, allow_target_free: bool) -> bool:
        """Prueft, ob fuer die Menge mindestens ein sinnvolles Ziel existiert."""
        cache_key = ("assign_target_batch", int(batch_size), int(available_free))
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return bool(cached)
        if batch_size <= 0:
            return self._set_can_cache(cache_key, False)
        # Frei als Ziel ist deaktiviert; Parameter bleibt nur aus API-Kompatibilitaet erhalten.
        _ = allow_target_free
        if available_free >= batch_size and self._has_assignable_tree_for_batch(batch_size):
            return self._set_can_cache(cache_key, True)
        for cat_idx in range(2, 6):
            areas = CATEGORY_AREA_MAP.get(cat_idx, [])
            if any(
                self._can_assign_serf_to_specific_area(area, batch_size, available_free_override=available_free)
                for area in areas
            ):
                return self._set_can_cache(cache_key, True)
        if available_free > 0 and any(
            int(site.get("serfs_assigned", 0) or 0) < MAX_ACTIVE_BUILDERS_PER_SITE
            for site in self.construction_sites
        ):
            return self._set_can_cache(cache_key, True)
        if available_free > 0 and any(self._can_build(b) for b in self.buildable_buildings):
            return self._set_can_cache(cache_key, True)
        return self._set_can_cache(cache_key, False)

    def _can_assign_serf_action(self, batch_size: int = 1) -> bool:
        cache_key = ("assign_serf_action", int(batch_size))
        cached = self._get_can_cache(cache_key)
        if cached is not None:
            return bool(cached)
        if batch_size <= 0:
            return self._set_can_cache(cache_key, False)
        if self.free_leibeigene >= batch_size and self._has_assign_target_for_batch(
            batch_size=batch_size,
            available_free=self.free_leibeigene,
            allow_target_free=False,
        ):
            return self._set_can_cache(cache_key, True)
        if self._has_nonfree_source_for_batch(batch_size) and self._has_assign_target_for_batch(
            batch_size=batch_size,
            available_free=max(self.free_leibeigene, batch_size),
            allow_target_free=False,
        ):
            return self._set_can_cache(cache_key, True)
        return self._set_can_cache(cache_key, False)

    def _can_recall_from_specific_area(self, area: SerfArea, batch_size: int) -> bool:
        if batch_size <= 0:
            return False
        if area in SHAFT_AREA_TO_SLOT:
            category, slot_idx = SHAFT_AREA_TO_SLOT[area]
            shafts = self.shaft_categories.get(category, {}).get("shafts", [])
            return slot_idx < len(shafts) and shafts[slot_idx].get("serfs_assigned", 0) >= batch_size
        if area in DEPOSIT_AREA_TO_SLOT:
            category, slot_idx = DEPOSIT_AREA_TO_SLOT[area]
            deposits = self.deposit_categories.get(category, {}).get("deposits", [])
            if slot_idx >= len(deposits):
                return False
            dep = deposits[slot_idx]
            target_x = int(dep.get("x", 0))
            target_y = int(dep.get("y", 0))
            assigned = 0
            for serf in self.production_system.serfs:
                if (
                    serf.target_resource
                    and serf.target_position
                    and int(serf.target_position.x) == target_x
                    and int(serf.target_position.y) == target_y
                ):
                    assigned += 1
            return assigned >= batch_size
        return False

    def _get_target_phase_available_free(self, batch_size: int) -> int:
        if self.current_flow != "assign_serf":
            return self.free_leibeigene
        src_cat = self.pending_selections.get(ActionPhase.SOURCE_CATEGORY, 0)
        if src_cat == 0:
            return self.free_leibeigene
        return max(self.free_leibeigene, batch_size)

    def _mask_source_category(self):
        """Kategorie-Auswahl: Von welcher Kategorie Leibeigene nehmen?"""
        batch_size = self._get_selected_batch_size()
        mask = np.zeros(len(SOURCE_CATEGORIES), dtype=bool)
        # 0=Frei: nur wenn freie Leibeigene vorhanden
        mask[0] = self.serf_areas.get(SerfArea.FREE, {}).get("count", 0) >= batch_size
        # 1-5: Ressource-Kategorien (Holz, Eisen, Stein, Lehm, Schwefel)
        mask[1] = any(tree.get("serfs_assigned", 0) >= batch_size for tree in self.tree_list_internal)
        for cat_idx in range(2, 6):
            areas = CATEGORY_AREA_MAP.get(cat_idx, [])
            mask[cat_idx] = any(self._can_recall_from_specific_area(area, batch_size) for area in areas)
        # 6=Baustelle: nur wenn Serfs an Baustellen
        mask[6] = any(site.get("serfs_assigned", 0) >= batch_size for site in self.construction_sites)
        if not mask.any():
            mask[0] = True  # Fallback
        return mask

    def _mask_source_specific(self):
        """Spezifische Auswahl innerhalb der gewÃƒÆ’Ã‚Â¤hlten Source-Kategorie."""
        cat = self.pending_selections.get(ActionPhase.SOURCE_CATEGORY, 0)
        batch_size = self._get_selected_batch_size()
        mask = np.zeros(self.source_specific_size, dtype=bool)
        if cat == 0:  # Frei (sollte ÃƒÆ’Ã‚Â¼bersprungen werden, Fallback)
            mask[0] = True
        elif cat == 1:
            for i, tree in enumerate(self.tree_list_internal[:self.source_specific_size]):
                if i < self.source_specific_size:
                    mask[i] = tree.get("serfs_assigned", 0) >= batch_size
        elif cat in CATEGORY_AREA_MAP:
            areas = CATEGORY_AREA_MAP[cat]
            for i, area in enumerate(areas):
                if i < self.source_specific_size:
                    mask[i] = self._can_recall_from_specific_area(area, batch_size)
        elif cat == 6:  # Baustelle
            for i, site in enumerate(self.construction_sites[:self.source_specific_size]):
                if site.get("serfs_assigned", 0) >= batch_size:
                    mask[i] = True
        if not mask.any():
            mask[0] = True
        return mask

    def _mask_target_category(self):
        """Kategorie-Auswahl: Wohin Leibeigene schicken?"""
        batch_size = self._get_selected_batch_size()
        available_free = self._get_target_phase_available_free(batch_size)
        mask = np.zeros(len(TARGET_CATEGORIES), dtype=bool)
        mask[0] = False  # Frei als Zielkategorie ist deaktiviert.
        mask[1] = available_free >= batch_size and self._has_assignable_tree_for_batch(batch_size)
        for cat_idx in range(2, 6):
            areas = CATEGORY_AREA_MAP.get(cat_idx, [])
            mask[cat_idx] = any(
                self._can_assign_serf_to_specific_area(area, batch_size, available_free_override=available_free)
                for area in areas
            )
        mask[6] = available_free > 0 and any(
            int(site.get("serfs_assigned", 0) or 0) < MAX_ACTIVE_BUILDERS_PER_SITE
            for site in self.construction_sites
        )
        mask[7] = available_free > 0 and any(self._can_build(b) for b in self.buildable_buildings)
        return mask

    def _mask_target_specific(self):
        """Spezifische Auswahl innerhalb der gewÃƒÆ’Ã‚Â¤hlten Target-Kategorie."""
        cat = self.pending_selections.get(ActionPhase.TARGET_CATEGORY, 0)
        batch_size = self._get_selected_batch_size()
        available_free = self._get_target_phase_available_free(batch_size)
        mask = np.zeros(self.target_specific_size, dtype=bool)
        if cat == 1:
            for i, _tree in enumerate(self.tree_list_internal[:self.target_specific_size]):
                mask[i] = self._can_assign_wood_tree_batch(i, batch_size, available_free_override=available_free)
        elif cat in CATEGORY_AREA_MAP:
            for i, area in enumerate(CATEGORY_AREA_MAP[cat]):
                if i < self.target_specific_size:
                    mask[i] = self._can_assign_serf_to_specific_area(
                        area,
                        batch_size,
                        available_free_override=available_free,
                    )
        elif cat == 6:  # Baustelle
            for i, site in enumerate(self.construction_sites[:self.target_specific_size]):
                already_assigned = int(site.get("serfs_assigned", 0) or 0)
                if available_free > 0 and already_assigned < MAX_ACTIVE_BUILDERS_PER_SITE:
                    mask[i] = True
        elif cat == 7:  # Neubau
            for i, b in enumerate(self.buildable_buildings):
                if i < self.target_specific_size and available_free > 0 and self._can_build(b):
                    mask[i] = True
        if not mask.any():
            if cat == 0:
                return mask
            mask[0] = True
        return mask

    def _mask_bless_categories(self):
        """Maske fuer Segen-Kategorien."""
        mask = np.zeros(len(BLESS_CATEGORIES), dtype=bool)
        for i in range(len(BLESS_CATEGORIES)):
            if i in BLESS_CATEGORIES:
                mask[i] = self._can_bless(i)
        if not mask.any():
            mask[0] = True
        return mask

    def _mask_tax_levels(self):
        """Maske fuer Steuerstufen."""
        mask = np.zeros(len(TAX_LEVELS), dtype=bool)
        for level in TAX_LEVELS.keys():
            if 0 <= level < len(mask):
                mask[level] = (level != self.current_tax_level)
        return mask

    def _mask_alarm_on_off(self):
        """Maske fuer Alarm an/aus ohne No-Op-Auswahl."""
        mask = np.zeros(2, dtype=bool)
        mask[0] = (not self.alarm_active) and (self.alarm_cooldown <= 0)  # einschalten
        mask[1] = bool(self.alarm_active)  # ausschalten
        return mask

    def _build_building(self, building, position: Optional[dict] = None):
        """
        Startet ein Bauprojekt. Erstellt eine Baustelle die Leibeigene braucht.

        Gebaeude werden NICHT automatisch gebaut - Agent muss Leibeigene zuweisen.
        Positionsauswahl: Minen -> Vorkommen-Slots, DZ -> DZ-Slots, Normal -> freie Kartenposition
        mit AABB-Kollisionspruefung via BUILDING_FOOTPRINTS.
        """
        b_info = buildings_db[building]
        base_name = get_base_building_name(building)

        chosen_position = None
        mine_type = None
        dz_slot = None
        selected_idx = None
        slot_candidate = False

        if b_info.get("mine_type"):
            # Minen: Feste Vorkommen-Slots
            mine_type = b_info["mine_type"]
            candidates = self._get_build_position_candidates(building)
            if position is not None:
                desired_key = self._pos_key_from_position(position)
                for candidate in candidates:
                    if self._pos_key_from_position(candidate) == desired_key:
                        chosen_position = {"x": int(round(candidate["x"])), "y": int(round(candidate["y"]))}
                        slot_candidate = True
                        break
            elif candidates:
                candidate = candidates[0]
                chosen_position = {"x": int(round(candidate["x"])), "y": int(round(candidate["y"]))}
                slot_candidate = True

        elif base_name == "Dorfzentrum":
            # Dorfzentrum: Feste DZ-Slots
            desired_key = self._pos_key_from_position(position) if position is not None else None
            for slot in self.dz_slots:
                if slot.get("status") != "free":
                    continue
                slot_key = self._pos_key_from_xy(slot["x"], slot["y"])
                if desired_key is not None and slot_key != desired_key:
                    continue
                chosen_position = {"x": int(round(slot["x"])), "y": int(round(slot["y"]))}
                dz_slot = slot
                slot_candidate = True
                break

        else:
            # Normale Gebaeude: Agent waehlt eine konkrete freie Kartenposition.
            if position is not None:
                pos_x = int(round(position.get("x", 0))) if isinstance(position, dict) else int(round(position[0]))
                pos_y = int(round(position.get("y", 0))) if isinstance(position, dict) else int(round(position[1]))
                if self._is_position_free(pos_x, pos_y, building):
                    chosen_position = {"x": pos_x, "y": pos_y}
                    slot_candidate = any(
                        self._pos_key_from_position(pos) == (pos_x, pos_y)
                        for pos in self.available_positions
                    )
            else:
                candidates = self._find_candidate_build_positions(building, limit=1)
                if candidates:
                    candidate = candidates[0]
                    chosen_position = {"x": int(round(candidate["x"])), "y": int(round(candidate["y"]))}
                    slot_candidate = bool(candidate.get("_slot_candidate", False))

        if chosen_position is None:
            return 0.0

        # Ressourcen erst abziehen wenn ein Platz wirklich existiert
        self._spend_costs(b_info["cost"])

        if mine_type:
            self.built_mines[mine_type].append({"x": chosen_position["x"], "y": chosen_position["y"]})
            mine_category = {
                "Eisenmine": "Eisen",
                "Steinmine": "Stein",
                "Lehmmine": "Lehm",
                "Schwefelmine": "Schwefel",
            }.get(mine_type)
            if mine_category:
                self._stop_deposit_serfs_at(
                    mine_category,
                    chosen_position["x"],
                    chosen_position["y"],
                    len(self.production_system.serfs),
                )
                self._recount_serf_areas()
        elif dz_slot is not None:
            dz_slot["status"] = "built"
        elif slot_candidate:
            target_x = int(round(chosen_position["x"]))
            target_y = int(round(chosen_position["y"]))
            for i, pos in enumerate(self.available_positions):
                px = int(round(pos["x"])) if isinstance(pos, dict) else int(round(pos[0]))
                py = int(round(pos["y"])) if isinstance(pos, dict) else int(round(pos[1]))
                if px == target_x and py == target_y:
                    selected_idx = i
                    break
            if selected_idx is not None:
                self.available_positions.pop(selected_idx)
                self.used_positions.append({"x": target_x, "y": target_y})
                self._mark_spatial_dirty("available_slots")

        # Erstelle Baustelle (Build-Speed Boni berÃƒÆ’Ã‚Â¼cksichtigen)
        build_time = self._get_effective_build_time(building)
        site = {
            "building": building,
            "position": chosen_position,
            "total_time": build_time,
            "remaining_work": build_time,
            "serfs_assigned": 0,
            "site_id": self.next_site_id,
        }
        self.construction_sites.append(site)
        self.next_site_id += 1
        self._mark_spatial_dirty("construction_sites")

        return 0.0

    def _deactivate_building_for_upgrade(self, building: str, pos_key: Optional[str]) -> bool:
        if not pos_key or pos_key not in self.building_position_map:
            return False
        if pos_key in self.upgrading_positions:
            return False

        runtime = self.building_runtime.get(pos_key)
        if runtime:
            for worker in list(runtime.get("workers", [])):
                try:
                    self.workforce_manager.workers.remove(worker)
                except ValueError:
                    pass
            runtime["workers"] = []

            mine_key = runtime.get("mine_key")
            if mine_key and mine_key in self.production_system.mines:
                self.production_system.mines[mine_key].current_workers = 0

            refiner_key = runtime.get("refiner_key")
            if refiner_key and refiner_key in self.production_system.refiners:
                self.production_system.refiners[refiner_key].current_workers = 0

        self.buildings[building] = max(0, self.buildings.get(building, 0) - 1)
        self.upgrading_positions.add(pos_key)
        self.workforce_manager.set_village_capacity(self._get_total_village_capacity())
        self._mark_infrastructure_dirty()
        return True

    def _upgrade_building(self, building, pos_key: Optional[str] = None):
        b_info = buildings_db[building]
        new_building = b_info["upgrade_to"]

        if not pos_key:
            keys = self._get_building_instance_keys(building)
            pos_key = keys[0] if keys else None
        if not self._deactivate_building_for_upgrade(building, pos_key):
            return 0.0

        self._spend_costs(b_info["upgrade_cost"])
        self.upgrade_queue.append((building, new_building, b_info["upgrade_time"], pos_key))

        # MINIMALER REWARD: Agent soll selbst die optimale Strategie finden
        return 0.0

    def _apply_technology_effects(self):
        """Wendet aktive Technologie-Effekte an (NEU - aus GEPLANTE_AENDERUNGEN.md).

        Wird nach jedem Forschungsabschluss aufgerufen.
        Akkumuliert alle Effekte der erforschten Technologien.
        """
        self.active_tech_effects = {}
        for tech_name in self.researched_techs:
            tech_info = technologies.get(tech_name, {})
            effect_sources = (
                tech_info.get("effects", {}),
                TECHNOLOGY_EFFECTS.get(tech_name, {}),
            )
            seen_effects = set()
            for effects in effect_sources:
                for effect_type, value in effects.items():
                    if effect_type in seen_effects:
                        continue
                    seen_effects.add(effect_type)
                    existing = self.active_tech_effects.get(effect_type)
                    if isinstance(value, bool):
                        if existing is None or isinstance(existing, bool):
                            self.active_tech_effects[effect_type] = bool(existing) or value
                        else:
                            # Numerischer Wert vorhanden -> Bool ignorieren
                            continue
                    else:
                        if existing is None or isinstance(existing, bool):
                            self.active_tech_effects[effect_type] = value
                        else:
                            self.active_tech_effects[effect_type] = existing + value
        self._mark_infrastructure_dirty()

    def _get_effective_build_time(self, building):
        """Berechnet effektive Bauzeit mit Tech-Boni."""
        base_time = buildings_db[building]["build_time"]
        speed_bonus = getattr(self, 'active_tech_effects', {}).get("build_speed_bonus", 0)
        return base_time / (1 + speed_bonus) if speed_bonus else base_time

    def _research_tech(self, tech):
        tech_info = technologies[tech]

        self._spend_costs(tech_info["cost"])

        self.current_researches.append((tech, tech_info["research_time"]))
        self.researching_set.add(tech)

        # MINIMALER REWARD: Agent soll selbst die optimale Strategie finden
        return 0.0

    def _recruit_soldier(self, soldier):
        s_info = soldiers_db[soldier]

        self._spend_costs(s_info["cost"])

        self.recruit_queue.append((soldier, s_info.get("train_time", 20)))

        # Reward erfolgt ueber Ressourcen-Potenzial + Abhaengigkeits-Fortschritt im step().
        return 0.0

    def _buy_serf(self):
        """Kauft einen neuen Leibeigenen."""
        from worker_simulation import Position

        self._spend_resource(RESOURCE_TALER, SERF_BUY_COST)
        self.total_leibeigene += 1
        self.free_leibeigene += 1
        self._pending_spawned_unassigned_serfs = max(0, int(self._pending_spawned_unassigned_serfs)) + 1

        # Neuen Serf erstellen (vereinfacht - keine IDs mehr)
        hq_pos = Position(x=self.hq_position[0], y=self.hq_position[1])
        serf = Serf(position=Position(x=hq_pos.x, y=hq_pos.y), target_resource=None)
        self.production_system.serfs.append(serf)

        return self._reward_for_buy_serf_growth()

    def _find_serf_index_for_area(self, area: SerfArea):
        """Sucht einen Serf passend zum Bereich (Best-Effort)."""
        for i, serf in enumerate(self.production_system.serfs):
            inferred = self._infer_serf_area(serf)
            if inferred == area:
                return i

        wood_zone_map = {
            SerfArea.WOOD_HQ: 0,
            SerfArea.WOOD_SULFUR: 1,
            SerfArea.WOOD_CLAY: 2,
            SerfArea.WOOD_STONE: 3,
            SerfArea.WOOD_VILLAGE: 4,
            SerfArea.WOOD_IRON: 5,
        }
        if area in wood_zone_map:
            zone_idx = wood_zone_map[area]
            if zone_idx < len(self.wood_zone_names):
                zone_name = self.wood_zone_names[zone_idx]
                target_location = f"wood_zone_{zone_name}"
                for i, serf in enumerate(self.production_system.serfs):
                    if serf.work_location == target_location:
                        return i

        deposit_resource_map = {
            SerfArea.DEPOSIT_IRON_1: "iron_raw",
            SerfArea.DEPOSIT_IRON_2: "iron_raw",
            SerfArea.DEPOSIT_STONE_1: "stone_raw",
            SerfArea.DEPOSIT_STONE_2: "stone_raw",
            SerfArea.DEPOSIT_CLAY_1: "clay_raw",
            SerfArea.DEPOSIT_SULFUR_1: "sulfur_raw",
            SerfArea.DEPOSIT_SULFUR_2: "sulfur_raw",
        }
        if area in deposit_resource_map:
            target_resource = deposit_resource_map[area]
            for i, serf in enumerate(self.production_system.serfs):
                if (serf.target_resource and
                    serf.target_resource.value == target_resource and
                    serf.work_location == "deposit"):
                    return i

        shaft_resource_map = {
            SerfArea.SHAFT_IRON_1: "iron_raw",
            SerfArea.SHAFT_IRON_2: "iron_raw",
            SerfArea.SHAFT_IRON_3: "iron_raw",
            SerfArea.SHAFT_STONE_1: "stone_raw",
            SerfArea.SHAFT_STONE_2: "stone_raw",
            SerfArea.SHAFT_STONE_3: "stone_raw",
            SerfArea.SHAFT_CLAY_1: "clay_raw",
            SerfArea.SHAFT_CLAY_2: "clay_raw",
            SerfArea.SHAFT_CLAY_3: "clay_raw",
            SerfArea.SHAFT_SULFUR_1: "sulfur_raw",
            SerfArea.SHAFT_SULFUR_2: "sulfur_raw",
            SerfArea.SHAFT_SULFUR_3: "sulfur_raw",
        }
        if area in shaft_resource_map:
            target_resource = shaft_resource_map[area]
            for i, serf in enumerate(self.production_system.serfs):
                if (serf.target_resource and
                    serf.target_resource.value == target_resource and
                    serf.work_location == "shaft"):
                    return i

        return None

    def _decrement_area_counters_for_dismiss(self, area: SerfArea):
        """Reduziert area-spezifische Z??hler nach Dismiss."""
        wood_zone_map = {
            SerfArea.WOOD_HQ: 0,
            SerfArea.WOOD_SULFUR: 1,
            SerfArea.WOOD_CLAY: 2,
            SerfArea.WOOD_STONE: 3,
            SerfArea.WOOD_VILLAGE: 4,
            SerfArea.WOOD_IRON: 5,
        }
        if area in wood_zone_map:
            zone_idx = wood_zone_map[area]
            if zone_idx < len(self.wood_zone_names):
                zone_name = self.wood_zone_names[zone_idx]
                zone_data = self.wood_zone_categories.get(zone_name)
                if zone_data:
                    zone_data["serfs_assigned"] = max(0, zone_data.get("serfs_assigned", 0) - 1)
            self.wood_serfs = max(0, self.wood_serfs - 1)
            self.resource_workers[RESOURCE_HOLZ_ROH] = max(0, self.resource_workers.get(RESOURCE_HOLZ_ROH, 0) - 1)
            return

        deposit_category_map = {
            SerfArea.DEPOSIT_IRON_1: "Eisen",
            SerfArea.DEPOSIT_IRON_2: "Eisen",
            SerfArea.DEPOSIT_STONE_1: "Stein",
            SerfArea.DEPOSIT_STONE_2: "Stein",
            SerfArea.DEPOSIT_CLAY_1: "Lehm",
            SerfArea.DEPOSIT_SULFUR_1: "Schwefel",
            SerfArea.DEPOSIT_SULFUR_2: "Schwefel",
        }
        if area in deposit_category_map:
            category = deposit_category_map[area]
            cat_data = self.deposit_categories.get(category)
            if cat_data:
                cat_data["serfs_assigned"] = max(0, cat_data.get("serfs_assigned", 0) - 1)
            raw_name_map = {
                "Eisen": RESOURCE_EISEN_ROH,
                "Stein": RESOURCE_STEIN_ROH,
                "Lehm": RESOURCE_LEHM_ROH,
                "Schwefel": RESOURCE_SCHWEFEL_ROH,
            }
            raw_name = raw_name_map.get(category, category)
            self.resource_workers[raw_name] = max(0, self.resource_workers.get(raw_name, 0) - 1)
            return

        shaft_type_map = {
            SerfArea.SHAFT_IRON_1: "Eisen",
            SerfArea.SHAFT_IRON_2: "Eisen",
            SerfArea.SHAFT_IRON_3: "Eisen",
            SerfArea.SHAFT_STONE_1: "Stein",
            SerfArea.SHAFT_STONE_2: "Stein",
            SerfArea.SHAFT_STONE_3: "Stein",
            SerfArea.SHAFT_CLAY_1: "Lehm",
            SerfArea.SHAFT_CLAY_2: "Lehm",
            SerfArea.SHAFT_CLAY_3: "Lehm",
            SerfArea.SHAFT_SULFUR_1: "Schwefel",
            SerfArea.SHAFT_SULFUR_2: "Schwefel",
            SerfArea.SHAFT_SULFUR_3: "Schwefel",
        }
        if area in shaft_type_map:
            shaft_type = shaft_type_map[area]
            shaft_data = self.shaft_categories.get(shaft_type)
            if shaft_data:
                shaft_data["serfs_assigned"] = max(0, shaft_data.get("serfs_assigned", 0) - 1)
            raw_name_map = {
                "Eisen": RESOURCE_EISEN_ROH,
                "Stein": RESOURCE_STEIN_ROH,
                "Lehm": RESOURCE_LEHM_ROH,
                "Schwefel": RESOURCE_SCHWEFEL_ROH,
            }
            raw_name = raw_name_map.get(shaft_type, shaft_type)
            self.resource_workers[raw_name] = max(0, self.resource_workers.get(raw_name, 0) - 1)
            return

    def _dismiss_serf_from_area(self, area: SerfArea):
        """Entl??sst einen Serf aus einem bestimmten Bereich."""
        if area == SerfArea.FREE:
            return self._dismiss_serf()

        if not self._can_dismiss_serf_from_area(area):
            return 0.0

        if area in self.serf_areas:
            self.serf_areas[area]["count"] = max(0, self.serf_areas[area].get("count", 0) - 1)

        self.total_leibeigene -= 1

        serf_idx = self._find_serf_index_for_area(area)
        if serf_idx is None:
            for i, serf in enumerate(self.production_system.serfs):
                if serf.is_idle():
                    serf_idx = i
                    break

        if serf_idx is not None:
            self.production_system.serfs.pop(serf_idx)

        self._decrement_area_counters_for_dismiss(area)
        return 0.0

    def _dismiss_serf(self):
        """EntlÃƒÆ’Ã‚Â¤sst einen freien Leibeigenen."""
        if self.free_leibeigene <= 0:
            return 0.0

        self.total_leibeigene -= 1
        self.free_leibeigene -= 1
        # Ohne stabile Serf-IDs konservativ gegen Ghost-Tokens absichern.
        self._pending_spawned_unassigned_serfs = max(
            0,
            int(getattr(self, "_pending_spawned_unassigned_serfs", 0)) - 1,
        )

        # Einen idle Serf entfernen (vereinfacht)
        for i, serf in enumerate(self.production_system.serfs):
            if serf.is_idle():
                self.production_system.serfs.pop(i)
                break

        return 0.0  # MINIMALER REWARD

    def _demolish_building(self, building: str, pos_key: Optional[str] = None):
        """Reisst ein Gebaeude ab. Position wird wieder freigegeben."""
        if self.buildings.get(building, 0) < 1:
            return 0.0

        self.buildings[building] -= 1
        base_name = get_base_building_name(building)
        self._mark_infrastructure_dirty()

        # Ressourcen zurueckgeben (CompensationOnBuildingSale aus Logic.xml)
        b_info = buildings_db.get(building, {})
        for resource, amount in b_info.get("cost", {}).items():
            refund = int(amount * BUILDING_SALE_COMPENSATION)
            self.resources[resource] = self.resources.get(resource, 0) + refund

        # Position wieder freigeben
        target_key = pos_key if pos_key in self.building_position_map else None
        if target_key and not target_key.startswith(building):
            target_key = None
        if target_key is None:
            for key in self.building_position_map.keys():
                if key.startswith(building):
                    target_key = key
                    break
        if target_key:
            pos = self.building_position_map.get(target_key)
            grid_id = self.building_grid_ids.pop(target_key, None)
            if grid_id is not None:
                self.map_manager.grid.remove_building(grid_id)
                self._building_block_revision += 1
                self._walkable_dirty = True
                self._mark_spatial_dirty("buildings")

            runtime = self.building_runtime.pop(target_key, None)
            if runtime:
                for worker in runtime.get("workers", []):
                    try:
                        self.workforce_manager.workers.remove(worker)
                    except ValueError:
                        pass
                mine_key = runtime.get("mine_key")
                if mine_key and mine_key in self.production_system.mines:
                    del self.production_system.mines[mine_key]
                refiner_key = runtime.get("refiner_key")
                if refiner_key and refiner_key in self.production_system.refiners:
                    del self.production_system.refiners[refiner_key]
            else:
                # Fallback: remove any mine/refiner at this position
                if pos is not None:
                    from worker_simulation import Position as WPosition
                    if isinstance(pos, dict):
                        pos_obj = WPosition(x=pos.get("x", 0), y=pos.get("y", 0))
                    elif isinstance(pos, tuple):
                        pos_obj = WPosition(x=pos[0], y=pos[1])
                    else:
                        pos_obj = pos

                    def _same_pos(a, b):
                        return a and b and int(a.x) == int(b.x) and int(a.y) == int(b.y)

                    for key, mine in list(self.production_system.mines.items()):
                        if _same_pos(mine.position, pos_obj):
                            del self.production_system.mines[key]
                            break
                    for key, refiner in list(self.production_system.refiners.items()):
                        if _same_pos(refiner.position, pos_obj):
                            del self.production_system.refiners[key]
                            break
                    for worker in list(self.workforce_manager.workers):
                        if _same_pos(worker.workplace_position, pos_obj):
                            try:
                                self.workforce_manager.workers.remove(worker)
                            except ValueError:
                                pass

            # Minen-Tracking bereinigen
            if base_name in self.built_mines and pos is not None:
                px = pos.get("x", 0) if isinstance(pos, dict) else pos[0]
                py = pos.get("y", 0) if isinstance(pos, dict) else pos[1]
                for i, mpos in enumerate(self.built_mines.get(base_name, [])):
                    mx = mpos.get("x", 0) if isinstance(mpos, dict) else mpos[0]
                    my = mpos.get("y", 0) if isinstance(mpos, dict) else mpos[1]
                    if mx == px and my == py:
                        self.built_mines[base_name].pop(i)
                        break
                if base_name in self.mine_categories:
                    self.mine_categories[base_name]["mines_built"] = max(
                        0, self.mine_categories[base_name].get("mines_built", 0) - 1
                    )

            if base_name == "Dorfzentrum":
                # DZ-Slot wieder freigeben
                px = pos.get("x", 0) if isinstance(pos, dict) else pos[0]
                py = pos.get("y", 0) if isinstance(pos, dict) else pos[1]
                for slot in self.dz_slots:
                    if slot["x"] == px and slot["y"] == py:
                        slot["status"] = "free"
                        break
            else:
                px = int(round(pos.get("x", 0))) if isinstance(pos, dict) else int(round(pos[0]))
                py = int(round(pos.get("y", 0))) if isinstance(pos, dict) else int(round(pos[1]))
                slot_pools = (
                    self.building_zones.get("zone_a_immediate", []),
                    self.building_zones.get("zone_b_after_logging", []),
                )
                is_known_slot = False
                for pool in slot_pools:
                    for slot in pool:
                        sx = int(round(slot.get("x", 0))) if isinstance(slot, dict) else int(round(slot[0]))
                        sy = int(round(slot.get("y", 0))) if isinstance(slot, dict) else int(round(slot[1]))
                        if sx == px and sy == py:
                            is_known_slot = True
                            break
                    if is_known_slot:
                        break

                if is_known_slot:
                    already_available = any(
                        (
                            int(round(ap.get("x", 0))) if isinstance(ap, dict) else int(round(ap[0]))
                        ) == px
                        and (
                            int(round(ap.get("y", 0))) if isinstance(ap, dict) else int(round(ap[1]))
                        ) == py
                        for ap in self.available_positions
                    )
                    if not already_available:
                        self.available_positions.append({"x": px, "y": py})
                    self.used_positions = [
                        up for up in self.used_positions
                        if (
                            (int(round(up.get("x", 0))) if isinstance(up, dict) else int(round(up[0])) != px)
                            or (int(round(up.get("y", 0))) if isinstance(up, dict) else int(round(up[1])) != py)
                        )
                    ]
                    self._mark_spatial_dirty("available_slots")
            del self.building_position_map[target_key]

        return 0.0

    def _bless(self, category: int):
        """Segnet Worker einer Kategorie (Kloster-Aktion).

        Args:
            category: Segen-Kategorie (0-4, aus BLESS_CATEGORIES)
        """
        if not self._can_bless(category):
            return 0.0

        # BlessingCost = 0 im Original (Logic.xml) - Faith wird NICHT verbraucht!
        # RequiredFaith = 5000 ist nur der Schwellwert, kein Verbrauch.
        # self.faith -= BLESS_REQUIRED_FAITH  # ENTFERNT: Original hat BlessingCost=0

        # Cooldown und aktive Zeit fÃƒÆ’Ã‚Â¼r diese Kategorie setzen
        self.bless_cooldowns[category] = BLESS_COOLDOWN
        self.bless_active_times[category] = self._get_bless_duration()

        # Motivation-Bonus fÃƒÆ’Ã‚Â¼r betroffene Worker
        cat_info = BLESS_CATEGORIES.get(category, {})
        # In extra2: BlessingBonus = 0.3 (+30% Motivation)
        # Wird in _tick_time() auf Worker angewendet

        return 0.0  # MINIMALER REWARD

    def _set_tax_level(self, level: int):
        """Setzt die Steuerstufe."""
        old_level = self.current_tax_level
        self.current_tax_level = level

        return 0.0  # MINIMALER REWARD

    def _tick_time(self):
        self.current_time += TIME_STEP

        # NEU: Segnungs-Cooldown und Dauer ticken (pro Kategorie)
        for cat in BLESS_CATEGORIES:
            if self.bless_cooldowns.get(cat, 0) > 0:
                self.bless_cooldowns[cat] = max(0, self.bless_cooldowns[cat] - TIME_STEP)
            if self.bless_active_times.get(cat, 0) > 0:
                self.bless_active_times[cat] = max(0, self.bless_active_times[cat] - TIME_STEP)

        # NEU: Alarm-Cooldown ticken
        if self.alarm_cooldown > 0:
            self.alarm_cooldown = max(0, self.alarm_cooldown - TIME_STEP)

        # NEU: Faith generieren (durch Priester im Kloster)
        priest_workers = [w for w in self.workforce_manager.workers if w.worker_type == "priest"]
        if priest_workers:
            # Faith pro Sekunde = Summe der Priester-Effizienz
            priests_eff = sum(w.get_efficiency() for w in priest_workers)
            self.faith = min(self.faith + priests_eff * TIME_STEP, self._get_bless_required_faith() * 5)

        # NEU: Infrastruktur synchronisieren
        self._sync_workforce_infrastructure()

        # Motivation auf WorkTime-Regeneration anwenden
        total_motivation = self._get_total_motivation()
        self.workforce_manager.set_motivation_modifier(total_motivation)

        # Segen Worker-Filter: Welche Worker-Typen sind gesegnet?
        blessed_types = self._get_blessed_worker_types()
        self.workforce_manager.set_blessed_types(blessed_types, BLESS_MOTIVATION_BONUS)

        # Speed-Bonus aus Technologie (T_Shoes: +20 fÃƒÆ’Ã‚Â¼r Worker/Serfs)
        shoes_speed = self.active_tech_effects.get("speed_modifier", 0)
        self.workforce_manager.set_speed_bonus(shoes_speed)

        runtime_pathfinder = None if self.disable_runtime_pathing else self._find_path_world
        grid_revision = None if runtime_pathfinder is None else self._get_routing_revision()

        # WorkTime-System ticken (Worker Pausen-Simulation)
        self.workforce_manager.tick(
            TIME_STEP,
            active_workplaces=self._get_active_workplaces(),
            pathfinder=runtime_pathfinder,
            path_revision=grid_revision
        )
        self._prune_runtime_workers()
        self._sync_workplace_worker_counts()

        # Produktionssystem ticken (mit WorkTime-Effizienz)
        resource_name_map = {
            ResourceType.WOOD: RESOURCE_HOLZ,
            ResourceType.STONE: RESOURCE_STEIN,
            ResourceType.CLAY: RESOURCE_LEHM,
            ResourceType.IRON: RESOURCE_EISEN,
            ResourceType.SULFUR: RESOURCE_SCHWEFEL,
            ResourceType.GOLD: RESOURCE_TALER,
            ResourceType.WOOD_RAW: RESOURCE_HOLZ_ROH,
            ResourceType.STONE_RAW: RESOURCE_STEIN_ROH,
            ResourceType.CLAY_RAW: RESOURCE_LEHM_ROH,
            ResourceType.IRON_RAW: RESOURCE_EISEN_ROH,
            ResourceType.SULFUR_RAW: RESOURCE_SCHWEFEL_ROH,
            ResourceType.GOLD_RAW: RESOURCE_GOLD_ROH,
        }
        resource_key_map = {
            ResourceType.WOOD: "wood",
            ResourceType.STONE: "stone",
            ResourceType.CLAY: "clay",
            ResourceType.IRON: "iron",
            ResourceType.SULFUR: "sulfur",
            ResourceType.GOLD: "gold",
        }
        # Ressourcen-Pool synchronisieren (ProductionSystem nutzt ResourceType-Keys)
        self.production_system.resources = {
            res_type: float(self.resources.get(res_name, 0))
            for res_type, res_name in resource_name_map.items()
        }
        production_output = self.production_system.tick(
            TIME_STEP,
            pathfinder=runtime_pathfinder,
            path_revision=grid_revision
        )

        # Nach Tick: Verbrauch/Output (ohne Boni) ins Inventar ÃƒÆ’Ã‚Â¼bernehmen
        for res_type, res_name in resource_name_map.items():
            self.resources[res_name] = self.production_system.resources.get(res_type, 0.0)

        # Bonus-Anteil auf Output addieren (ohne DoppelzÃƒÆ’Ã‚Â¤hlung)
        for res_type, amount in production_output.items():
            res_name = resource_name_map.get(res_type)
            if res_name:
                resource_key = resource_key_map.get(res_type)
                bonus_pct = self._get_resource_output_bonus_pct(resource_key) if resource_key else 0.0
                if bonus_pct:
                    self.resources[res_name] = self.resources.get(res_name, 0) + (amount * (bonus_pct / 100.0))

        # Passives GebÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¤ude-Output (ohne Mines/Refiner)
        self._apply_passive_building_outputs(TIME_STEP)

        # EXAKTES TRACKING: Ressourcen-Ersch?pfung basiert auf Serf-Extraktionen
        serf_events = getattr(self.production_system, "last_serf_events", [])
        self._process_serf_events(serf_events)

        # Steuer-Einkommen (aus extra2/logic.xml)
        # RegularTax = fester Betrag PRO WORKER (nicht Multiplikator!)
        if self.current_time % INCOME_CYCLE == 0:
            tax_info = TAX_LEVELS.get(self.current_tax_level, TAX_LEVELS[2])
            # ZÃƒÆ’Ã‚Â¤hle alle arbeitenden Worker
            total_workers = len(self.workforce_manager.workers)
            # Steuer-Einkommen = RegularTax pro Worker
            tax_income = tax_info["regular_tax"] * total_workers
            tax_income = int(tax_income * self._get_tax_income_multiplier())
            # GebÃƒÆ’Ã‚Â¤ude-Einkommen (taler_income aus buildings_db)
            building_income = self._get_taler_income() * self._get_trade_income_multiplier()
            self.resources[RESOURCE_TALER] += tax_income + building_income

            # Motivation-ÃƒÆ’Ã¢â‚¬Å¾nderung anwenden
            motivation_change = tax_info["motivation_change"]
            # TaxPenalty: Extra Motivationsstrafe wenn Steuern erhoben werden (Logic.xml: TaxPenalty=0.1)
            if tax_info["regular_tax"] > 0:
                motivation_change -= self._get_tax_penalty()
            self.base_motivation = max(0.25, min(3.0, self.base_motivation + motivation_change))

            # MotivationThresholdLeave: bei sehr niedriger Motivation verlÃƒÆ’Ã‚Â¤sst ein Worker die Siedlung
            if self._get_total_motivation() <= 0.25:
                self._remove_one_worker_due_to_motivation()

        # NEU: Baustellen mit Leibeigenen-System verarbeiten
        completed_sites = []
        for i, site in enumerate(self.construction_sites):
            site_id = site.get("site_id")
            active_builders = 0
            for serf in self.production_system.serfs:
                if serf.build_site_id == site_id and serf.state == SerfState.BUILDING:
                    active_builders += 1
            if active_builders > 0:
                # TL_SERF_BUILD.xml: Bauarbeit erfolgt in wiederholten Hammerschlaegen.
                # Fortschritt linear pro aktivem Builder, aber auf Baustellen-Slots begrenzt.
                effective_builders = min(active_builders, MAX_ACTIVE_BUILDERS_PER_SITE)
                work_done = (TIME_STEP * effective_builders) / SERF_BUILD_SWING_SECONDS
                site["remaining_work"] -= work_done

                if site["remaining_work"] <= 0:
                    # GebÃƒÆ’Ã‚Â¤ude fertig!
                    building = site["building"]
                    pos = site["position"]
                    self.buildings[building] = self.buildings.get(building, 0) + 1
                    pos_key = None
                    if pos:
                        pos_key = f"{building}_{len(self.building_position_map)}"
                        self.building_position_map[pos_key] = pos
                    # Bei GebÃƒÆ’Ã‚Â¤ude-Fertigstellung Worker/Mine/Refiner erstellen
                    self._on_building_completed(building, pos, pos_key=pos_key)
                    # Serfs werden frei
                    self._release_serfs_from_site(site)
                    completed_sites.append(i)

        for i in reversed(completed_sites):
            self.construction_sites.pop(i)
        if completed_sites:
            self._mark_spatial_dirty("construction_sites")

        # Legacy: Alte Bau-Queue verarbeiten (falls noch EintrÃƒÆ’Ã‚Â¤ge vorhanden)
        completed = []
        for i, (building, remaining, pos) in enumerate(self.construction_queue):
            remaining -= TIME_STEP
            if remaining <= 0:
                self.buildings[building] = self.buildings.get(building, 0) + 1
                pos_key = None
                if pos:
                    pos_key = f"{building}_{len(self.building_position_map)}"
                    self.building_position_map[pos_key] = pos
                self._on_building_completed(building, pos, pos_key=pos_key)
                completed.append(i)
            else:
                self.construction_queue[i] = (building, remaining, pos)
        for i in reversed(completed):
            self.construction_queue.pop(i)

        # Upgrade-Queue verarbeiten
        completed = []
        for i, item in enumerate(self.upgrade_queue):
            if len(item) == 4:
                old_b, new_b, remaining, pos_key = item
            else:
                old_b, new_b, remaining = item
                pos_key = None
            remaining -= TIME_STEP
            if remaining <= 0:
                self.buildings[new_b] = self.buildings.get(new_b, 0) + 1
                if pos_key:
                    old_pos_key = pos_key
                    pos_key = self._update_building_position_key(pos_key, new_b)
                    self.upgrading_positions.discard(old_pos_key)
                # Upgrade in ProductionSystem propagieren
                self._on_upgrade_completed(old_b, new_b, pos_key=pos_key)
                completed.append(i)
            else:
                if pos_key:
                    self.upgrade_queue[i] = (old_b, new_b, remaining, pos_key)
                else:
                    self.upgrade_queue[i] = (old_b, new_b, remaining)
        for i in reversed(completed):
            self.upgrade_queue.pop(i)

        # Forschung verarbeiten (abh?ngig von Gelehrten-Effizienz)
        if self.current_researches:
            scholar_efficiency = self._get_scholar_efficiency()
            updated = []
            completed_any = False
            for tech, remaining in self.current_researches:
                remaining -= TIME_STEP * scholar_efficiency
                if remaining <= 0:
                    self.researched_techs.add(tech)
                    self.researching_set.discard(tech)
                    completed_any = True
                else:
                    updated.append((tech, remaining))
            self.current_researches = updated
            if completed_any:
                # NEU: Technologie-Effekte anwenden (aus GEPLANTE_AENDERUNGEN.md)
                self._apply_technology_effects()

        # Rekrutierung verarbeiten
        completed = []
        for i, (soldier, remaining) in enumerate(self.recruit_queue):
            remaining -= TIME_STEP
            if remaining <= 0:
                self.soldiers[soldier] = self.soldiers.get(soldier, 0) + 1
                if "ScharfschÃƒÆ’Ã‚Â¼tzen" in soldier:
                    self.scharfschuetzen += 1
                completed.append(i)
            else:
                self.recruit_queue[i] = (soldier, remaining)
        for i in reversed(completed):
            self.recruit_queue.pop(i)

        # Serf-Areas aus echten Serf-Objekten rekonstruieren
        self._recount_serf_areas()

    def _get_nearest_worker_spawn_position(self, pos_x, pos_y):
        """Gibt die Position des naechsten Dorfzentrums zurueck (HQ ausgeschlossen)."""
        from worker_simulation import Position
        import math

        candidates = []
        # 1) Gebaute DZ-Slots
        dz_positions = [slot for slot in self.dz_slots if slot.get("status") == "built"]
        for slot in dz_positions:
            candidates.append(Position(x=slot["x"], y=slot["y"]))
        # 2) Fallback: bereits registrierte Dorfzentren (z.B. dynamisch gebaut)
        for key, pos in self.building_position_map.items():
            if not key.startswith("Dorfzentrum_"):
                continue
            if isinstance(pos, dict):
                candidates.append(Position(x=pos.get("x", 0), y=pos.get("y", 0)))
            elif isinstance(pos, tuple):
                candidates.append(Position(x=pos[0], y=pos[1]))
            elif isinstance(pos, Position):
                candidates.append(Position(x=pos.x, y=pos.y))

        if not candidates:
            return None

        best_pos = candidates[0]
        min_dist = math.sqrt((pos_x - best_pos.x) ** 2 + (pos_y - best_pos.y) ** 2)
        for slot in candidates[1:]:
            dist = math.sqrt(
                (pos_x - slot.x) ** 2 + (pos_y - slot.y) ** 2
            )
            if dist < min_dist:
                min_dist = dist
                best_pos = slot
        return best_pos

    def _get_nearest_dz_distance(self, pos_x, pos_y):
        """Berechnet Distanz zum naechsten Dorfzentrum oder HQ."""
        import math
        spawn_pos = self._get_nearest_worker_spawn_position(pos_x, pos_y)
        if spawn_pos is None:
            return float("inf")
        return math.sqrt(
            (pos_x - spawn_pos.x) ** 2 + (pos_y - spawn_pos.y) ** 2
        )

    def _on_building_completed(self, building: str, position, pos_key: Optional[str] = None):
        """Callback wenn ein Gebaeude fertig wird - erstellt Worker/Minen/Refiner.

        Worker spawnen mit Laufweg-Delay vom naechsten Dorfzentrum (HQ ausgeschlossen).
        """
        from worker_simulation import Position, WorkerState

        base_name = get_base_building_name(building)
        level = get_building_level(building)
        self._mark_infrastructure_dirty()

        if position is None:
            position = self.hq_position

        # Position in Position-Objekt umwandeln
        if isinstance(position, dict):
            pos_obj = Position(x=position.get('x', 0), y=position.get('y', 0))
        elif isinstance(position, tuple):
            pos_obj = Position(x=position[0], y=position[1])
        else:
            pos_obj = position

        # Worker spawnen am naechsten DZ/HQ und laufen zum Arbeitsplatz
        spawn_pos = self._get_nearest_worker_spawn_position(pos_obj.x, pos_obj.y)
        spawn_path = []
        if spawn_pos is not None:
            spawn_path = self._find_path_world(spawn_pos, pos_obj)
            if spawn_path and spawn_pos.distance_to(spawn_path[0]) < 1.0:
                spawn_path = spawn_path[1:]

        runtime = None
        if pos_key is not None:
            runtime = self.building_runtime.setdefault(
                pos_key,
                {"workers": [], "mine_key": None, "refiner_key": None, "building": building},
            )

        # Dorfzentrum-KapazitÃƒÆ’Ã‚Â¤t vor Worker-Spawn aktualisieren
        self.workforce_manager.set_village_capacity(self._get_total_village_capacity())

        def spawn_workers(worker_type: str, count: int) -> int:
            worker_type = normalize_worker_type(worker_type)
            spawned = 0
            for _ in range(max(0, int(count))):
                if spawn_pos is None:
                    break
                start_pos = Position(x=spawn_pos.x, y=spawn_pos.y)
                worker = self.workforce_manager.add_worker(worker_type, start_pos, pos_obj)
                if not worker:
                    break
                worker.state = WorkerState.WALKING_TO_WORK
                worker.state_timer = 0.0
                worker.path = list(spawn_path) if spawn_path else []
                worker.path_index = 0
                if worker.path:
                    worker.target_position = worker.path[0]
                else:
                    worker.target_position = Position(x=pos_obj.x, y=pos_obj.y)
                worker.final_destination = Position(x=pos_obj.x, y=pos_obj.y)
                worker.path_revision = self._get_routing_revision()
                spawned += 1
                if runtime is not None:
                    runtime["workers"].append(worker)
            return spawned

        # Gebaeude im MapManager-Grid blockieren (fuer Pfadfindung)
        building_id = self.map_manager.add_building(pos_obj.x, pos_obj.y, base_name)
        if pos_key is not None:
            self.building_grid_ids[pos_key] = building_id
        self._building_block_revision += 1
        self._walkable_dirty = True
        self._mark_spatial_dirty("buildings")

        # Minen erstellen
        if "mine" in building.lower() or base_name in ["Steinmine", "Lehmmine", "Eisenmine", "Schwefelmine"]:
            resource_map = {
                "Steinmine": ResourceType.STONE_RAW,
                "Lehmmine": ResourceType.CLAY_RAW,
                "Eisenmine": ResourceType.IRON_RAW,
                "Schwefelmine": ResourceType.SULFUR_RAW,
            }
            resource_type = resource_map.get(base_name)
            if resource_type:
                # Mine erstellen (Werte aus XML)
                max_workers_by_level = {1: 5, 2: 6, 3: 7}
                amount_by_level = {1: 4, 2: 5, 3: 6}
                max_workers = buildings_db.get(building, {}).get("max_workers",
                                                                max_workers_by_level.get(level, 5))
                mine = Mine(
                    name=f"{base_name}_{level}",
                    resource_type=resource_type,
                    position=pos_obj,
                    worker_type="miner",
                    level=level,
                    max_workers=max_workers,
                    amount_to_mine=amount_by_level.get(level, 4)
                )
                mine_key = pos_key or f"{base_name}_{level}_{len(self.production_system.mines)}"
                self.production_system.mines[mine_key] = mine
                if runtime is not None:
                    runtime["mine_key"] = mine_key

                # Worker fuer Mine erstellen (Miner haben WorkTime!)
                spawned = spawn_workers("miner", max_workers)
                mine.current_workers += spawned

                # NEU: mine_categories fÃƒÆ’Ã‚Â¼r Serf-Zuweisung aktualisieren
                if base_name in self.mine_categories:
                    self.mine_categories[base_name]["mines_built"] += 1

        # Raffinerien erstellen (SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle, Schmiede, LehmhÃƒÆ’Ã‚Â¼tte, etc.)
        elif base_name in ["SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle", "Schmiede", "AlchimistenhÃƒÆ’Ã‚Â¼tte", "SteinmetzhÃƒÆ’Ã‚Â¼tte", "LehmhÃƒÆ’Ã‚Â¼tte", "Bank", "BÃƒÆ’Ã‚Â¼chsenmacherei"]:
            # Output-Ressource und Input-Ressource Mapping
            refiner_config = {
                "SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle": {
                    "output": ResourceType.WOOD,
                    "input": ResourceType.WOOD_RAW,  # Holz verarbeiten
                    "initial_factor": 4,
                    "transport_amount": 5,
                    "work_wait_until": 40.0,
                    "worker_type": "sawmill_worker"
                },
                "LehmhÃƒÆ’Ã‚Â¼tte": {
                    "output": ResourceType.CLAY,
                    "input": ResourceType.CLAY_RAW,  # Lehm verarbeiten (zu Ziegel)
                    "initial_factor": 4,
                    "transport_amount": 5,
                    "work_wait_until": 30.0,
                    "worker_type": "brickmaker"
                },
                "Schmiede": {
                    "output": ResourceType.IRON,
                    "input": ResourceType.IRON_RAW,  # Eisen verarbeiten
                    "initial_factor": 4,
                    "transport_amount": 5,
                    "work_wait_until": 30.0,
                    "worker_type": "smith"
                },
                "AlchimistenhÃƒÆ’Ã‚Â¼tte": {
                    "output": ResourceType.SULFUR,
                    "input": ResourceType.SULFUR_RAW,
                    "initial_factor": 4,
                    "transport_amount": 5,
                    "work_wait_until": 20.0,
                    "worker_type": "alchemist"
                },
                "SteinmetzhÃƒÆ’Ã‚Â¼tte": {
                    "output": ResourceType.STONE,
                    "input": ResourceType.STONE_RAW,
                    "initial_factor": 4,
                    "transport_amount": 5,
                    "work_wait_until": 15.0,
                    "worker_type": "stonecutter"
                },
                "Bank": {
                    "output": ResourceType.GOLD,
                    "input": ResourceType.GOLD_RAW,
                    "initial_factor": 2,
                    "transport_amount": 5,
                    "work_wait_until": 15.0,
                    "worker_type": "treasurer"
                },
                "BÃƒÆ’Ã‚Â¼chsenmacherei": {
                    "output": ResourceType.SULFUR,
                    "input": ResourceType.SULFUR_RAW,
                    "initial_factor": 4,
                    "transport_amount": 5,
                    "work_wait_until": 30.0,
                    "worker_type": "gunsmith"
                },
            }
            config = refiner_config.get(base_name)
            if config:
                max_workers = buildings_db.get(building, {}).get("max_workers")
                if not max_workers:
                    max_workers = 4
                # Supplier-Position (HQ/DZ/Markt als Lager)
                supplier_pos = self._get_supplier_position(config["input"], pos_obj)

                refiner = Refiner(
                    name=f"{base_name}_{level}",
                    resource_type=config["output"],
                    input_resource=config["input"],
                    position=pos_obj,
                    supplier_position=supplier_pos,
                    worker_type=config["worker_type"],
                    level=level,
                    max_workers=max_workers,
                    initial_factor=config["initial_factor"],
                    transport_amount=config["transport_amount"],
                    work_wait_until=config.get("work_wait_until", 5.0),
                    refines_per_cycle=get_refiner_resource_ops_per_cycle(config["worker_type"]),
                )
                _, dist = self._compute_path(pos_obj, supplier_pos)
                refiner.path_distance = dist
                refiner_key = pos_key or f"{base_name}_{level}_{len(self.production_system.refiners)}"
                self.production_system.refiners[refiner_key] = refiner
                if runtime is not None:
                    runtime["refiner_key"] = refiner_key

                # Worker erstellen mit Spawn-Delay
                spawned = spawn_workers(config["worker_type"], max_workers)
                refiner.current_workers += spawned

        # Sonstige Worker-GebÃƒÆ’Ã‚Â¤ude (Hochschule, Kloster, Markt, etc.)
        else:
            worker_type = buildings_db.get(building, {}).get("worker_type") or BUILDING_WORKER_TYPES.get(base_name)
            if worker_type:
                max_workers = buildings_db.get(building, {}).get("max_workers", 0)
                spawn_workers(worker_type, max_workers)

    def _on_upgrade_completed(self, old_building: str, new_building: str, pos_key: Optional[str] = None):
        """Propagiert Upgrade-Effekte in ProductionSystem und Kapazit??ten."""
        from worker_simulation import Position, WorkerState
        old_base = get_base_building_name(old_building)
        new_base = get_base_building_name(new_building)
        new_level = get_building_level(new_building)
        runtime = self.building_runtime.get(pos_key) if pos_key else None
        self._mark_infrastructure_dirty()

        # Position fÃƒÆ’Ã‚Â¼r Worker-Spawn bestimmen
        raw_pos = self.building_position_map.get(pos_key) if pos_key else None
        if raw_pos is None:
            raw_pos = self.hq_position
        if isinstance(raw_pos, Position):
            pos_obj = raw_pos
        elif isinstance(raw_pos, dict):
            pos_obj = Position(x=raw_pos.get('x', 0), y=raw_pos.get('y', 0))
        elif isinstance(raw_pos, tuple):
            pos_obj = Position(x=raw_pos[0], y=raw_pos[1])
        else:
            pos_obj = Position(x=0, y=0)

        spawn_pos = self._get_nearest_worker_spawn_position(pos_obj.x, pos_obj.y)
        spawn_path = []
        if spawn_pos is not None:
            spawn_path = self._find_path_world(spawn_pos, pos_obj)
            if spawn_path and spawn_pos.distance_to(spawn_path[0]) < 1.0:
                spawn_path = spawn_path[1:]

        # Dorfzentrum-KapazitÃƒÆ’Ã‚Â¤t vor Worker-Spawn aktualisieren
        self.workforce_manager.set_village_capacity(self._get_total_village_capacity())

        def spawn_workers(worker_type: str, count: int) -> int:
            worker_type = normalize_worker_type(worker_type)
            spawned = 0
            for _ in range(max(0, int(count))):
                if spawn_pos is None:
                    break
                start_pos = Position(x=spawn_pos.x, y=spawn_pos.y)
                worker = self.workforce_manager.add_worker(worker_type, start_pos, pos_obj)
                if not worker:
                    break
                worker.state = WorkerState.WALKING_TO_WORK
                worker.state_timer = 0.0
                worker.path = list(spawn_path) if spawn_path else []
                worker.path_index = 0
                if worker.path:
                    worker.target_position = worker.path[0]
                else:
                    worker.target_position = Position(x=pos_obj.x, y=pos_obj.y)
                worker.final_destination = Position(x=pos_obj.x, y=pos_obj.y)
                worker.path_revision = self._get_routing_revision()
                spawned += 1
                if runtime is not None:
                    runtime["workers"].append(worker)
            return spawned

        # --- Minen upgraden ---
        if old_base in ["Steinmine", "Lehmmine", "Eisenmine", "Schwefelmine"]:
            mine = None
            if runtime:
                mine_key = runtime.get("mine_key")
                if mine_key in self.production_system.mines:
                    mine = self.production_system.mines[mine_key]
            if mine is None:
                old_key = f"{old_base}_{get_building_level(old_building)}"
                mine = self.production_system.mines.get(old_key)
            if mine:
                mine.level = new_level
                max_workers_by_level = {1: 5, 2: 6, 3: 7}
                max_workers = buildings_db.get(new_building, {}).get("max_workers",
                                                                max_workers_by_level.get(new_level, 5))
                mine.max_workers = max_workers
                mine.amount_to_mine = mine.amount_by_level  # Nutzt property
                mine.name = f"{new_base}_{new_level}"
                missing = max(0, mine.max_workers - mine.current_workers)
                if missing:
                    mine.current_workers += spawn_workers("miner", missing)

        # --- Refiner upgraden ---
        elif old_base in ["SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle", "Schmiede", "AlchimistenhÃƒÆ’Ã‚Â¼tte", "SteinmetzhÃƒÆ’Ã‚Â¼tte", "LehmhÃƒÆ’Ã‚Â¼tte", "Bank", "BÃƒÆ’Ã‚Â¼chsenmacherei"]:
            refiner = None
            if runtime:
                refiner_key = runtime.get("refiner_key")
                if refiner_key in self.production_system.refiners:
                    refiner = self.production_system.refiners[refiner_key]
            if refiner is None:
                old_key = f"{old_base}_{get_building_level(old_building)}"
                refiner = self.production_system.refiners.get(old_key)
            if refiner:
                refiner.level = new_level
                # MaxWorkers aus buildings_db (falls vorhanden), sonst Fallback
                max_workers = buildings_db.get(new_building, {}).get("max_workers")
                if max_workers:
                    refiner.max_workers = max_workers
                else:
                    max_workers_by_level = {1: 4, 2: 6, 3: 8}
                    refiner.max_workers = max_workers_by_level.get(new_level, refiner.max_workers)
                refiner.name = f"{new_base}_{new_level}"
                _, dist = self._compute_path(refiner.position, refiner.supplier_position)
                refiner.path_distance = dist
                missing = max(0, refiner.max_workers - refiner.current_workers)
                if missing:
                    refiner.current_workers += spawn_workers(refiner.worker_type, missing)

        # --- Sonstige Worker-GebÃƒÆ’Ã‚Â¤ude upgraden ---
        else:
            worker_type = buildings_db.get(new_building, {}).get("worker_type") or BUILDING_WORKER_TYPES.get(new_base)
            if worker_type:
                max_workers = buildings_db.get(new_building, {}).get("max_workers", 0)
                current_workers = len(runtime.get("workers", [])) if runtime else 0
                missing = max(0, max_workers - current_workers)
                if missing:
                    spawn_workers(worker_type, missing)


    def get_action_history(self):
        return self.action_history

    def get_building_positions(self):
        positions = []
        for building_id, pos in self.building_position_map.items():
            building_name = "_".join(building_id.split("_")[:-1])
            positions.append({"building": building_name, "position": pos})
        return positions

    def render(self):
        if self.render_mode in ["human", "ansi"]:
            print(f"\n=== Zeit: {self.current_time // 60}:{self.current_time % 60:02d} ===")
            print(f"ScharfschÃƒÆ’Ã‚Â¼tzen: {self.scharfschuetzen}")
            print(f"Ressourcen: {self.resources}")
            print(f"Arbeiter frei: {self.free_leibeigene}/{self.total_leibeigene}")

            # NEU: WorkTime-Stats
            stats = self.workforce_manager.get_stats()
            print(f"\n--- WorkTime-System ---")
            print(f"Worker gesamt: {stats.get('total_workers', 0)}")
            print(f"Arbeitend: {stats.get('working_workers', 0)}, "
                  f"Essend: {stats.get('eating_workers', 0)}, "
                  f"Ruhend: {stats.get('resting_workers', 0)}")
            print(f"Durchschn. WorkTime: {stats.get('avg_work_time', 0):.1f}")
            print(f"Effizienz: {self.workforce_manager.get_average_efficiency():.1%}")
            print(f"ErschÃƒÆ’Ã‚Â¶pft: {self.workforce_manager.get_exhausted_ratio():.1%}")

            # KapazitÃƒÆ’Ã‚Â¤ten
            print(f"\n--- KapazitÃƒÆ’Ã‚Â¤ten ---")
            print(f"Farm-KapazitÃƒÆ’Ã‚Â¤t: {self._get_total_farm_capacity()} Esser")
            print(f"Wohnhaus-KapazitÃƒÆ’Ã‚Â¤t: {self._get_total_residence_capacity()} Bewohner")

            # Produktion
            print(f"\n--- Produktion ---")
            print(f"Minen: {len(self.production_system.mines)}")
            print(f"Raffinerien: {len(self.production_system.refiners)}")
            print(f"Serfs: {len(self.production_system.serfs)}")

            # NEU: Steuern & Segnung
            print(f"\n--- Steuern & Motivation ---")
            tax_info = TAX_LEVELS.get(self.current_tax_level, TAX_LEVELS[2])
            print(f"Steuerstufe: {self.current_tax_level} ({tax_info['name']})")
            print(f"Einkommens-Multiplikator: {tax_info['income_multiplier']:.1f}x")
            active_any = any(t > 0 for t in self.bless_active_times.values())
            cooldown_any = any(c > 0 for c in self.bless_cooldowns.values())
            print(f"Segnung aktiv: {'Ja' if active_any else 'Nein'}")
            if active_any:
                max_active = max(self.bless_active_times.values())
                print(f"  Verbleibende Zeit: {max_active}s")
            if cooldown_any:
                max_cd = max(self.bless_cooldowns.values())
                print(f"Segnung Cooldown: {max_cd}s")
            print(f"Gesamtmotivation: {self._get_total_motivation()}%")

    def close(self):
        pass


# =============================================================================
# STATISTIKEN
# =============================================================================

print(f"Geladene GebÃƒÆ’Ã‚Â¤ude: {len(buildings_db)}")
print(f"Geladene Technologien: {len(technologies)}")
print(f"Geladene Einheiten: {len(soldiers_db)}")
print(f"Baubare GebÃƒÆ’Ã‚Â¤ude (Level 1): {len([b for b in buildings_db.keys() if get_building_level(b) == 1])}")
print(f"Upgradeable GebÃƒÆ’Ã‚Â¤ude: {len([b for b in buildings_db.keys() if buildings_db[b].get('upgrade_to')])}")

if __name__ == "__main__":
    env = SiedlerScharfschuetzenEnv()
    print(f"\n--- Multi-Step Action System ---")
    print(f"MAIN Actions: {len(MAIN_ACTIONS)}")
    for i, a in enumerate(MAIN_ACTIONS):
        flow = ACTION_FLOWS.get(a, [])
        phases = " -> ".join(p.value for p in flow)
        print(f"  {i}: {a} [{phases}]")
    print(f"\n--- Action Spaces pro Phase ---")
    for phase, space in env.action_spaces.items():
        print(f"  {phase.value}: Discrete({space.n})")
    print(f"\n--- Forschung nach Gebaeude ---")
    for building in RESEARCH_BUILDINGS:
        techs = env.tech_by_building.get(building, [])
        print(f"  {building}: {len(techs)} Techs")
    print(f"\nObservation Space: {env.observation_space}")


