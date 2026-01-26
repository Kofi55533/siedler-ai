# -*- coding: utf-8 -*-
"""
Siedler 5 - Vollständige Trainingsumgebung für Scharfschützen-Optimierung
KOMPLETTE Spielsimulation mit ALLEN Aktionen aus dem echten Spiel

Basiert auf: Die Siedler - Erbe der Könige
Karte: EMS Wintersturm (4 Spieler, 2v2)

NEU: Integriert WorkTime/Pausen-System und 2-Tier Produktion
"""

import copy
import json
import os
import gymnasium as gym
import numpy as np
from typing import Dict, List, Optional, Tuple

# Importiere Karten-Konfiguration
from map_config_wintersturm import (
    START_RESOURCES, MINES_PER_PLAYER, BUILDING_ZONES_PLAYER_1,
    PLAYER_1_MINE_POSITIONS, PLAYER_1_MINE_SHAFTS, PLAYER_1_SMALL_DEPOSITS,
    PLAYER_1_TREES_SUMMARY, PLAYER_1_TREES_NEAREST,
    PLAYER_HQ_POSITIONS,
    GAME_RULES, SCHARFSCHUETZEN_PATH,
    get_building_positions_for_player
)

# Importiere Holz-Zonen für strategische Bauplatz-Schaffung
from wood_zones_config import WOOD_ZONES

# Importiere neue Simulationssysteme
from worker_simulation import (
    WorkforceManager, Worker, Farm, Residence, Camp,
    WorkerState, WORKER_PARAMS, WORKER_SPEEDS
)
from production_system import (
    ProductionSystem, Mine, Refiner, Serf, ResourceType,
    SERF_EXTRACTION
)

# NEU: Pfadfindung für exakte Laufwege
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

RESOURCE_NAMES = [RESOURCE_HOLZ, RESOURCE_STEIN, RESOURCE_LEHM, RESOURCE_EISEN, RESOURCE_SCHWEFEL, RESOURCE_TALER]
RESOURCE_MAP = [RESOURCE_HOLZ, RESOURCE_STEIN, RESOURCE_LEHM, RESOURCE_EISEN, RESOURCE_SCHWEFEL]

# Sammelraten pro Arbeiter pro Zeiteinheit
gather_rates = {
    RESOURCE_HOLZ: 1.038,
    RESOURCE_STEIN: 0.528,
    RESOURCE_LEHM: 0.528,
    RESOURCE_EISEN: 0.642,
    RESOURCE_SCHWEFEL: 0.642
}

# =============================================================================
# LEIBEIGENE-KONSTANTEN (aus PU_Serf.xml)
# =============================================================================
SERF_SEARCH_RADIUS = 4500  # ResourceSearchRadius aus PU_Serf.xml
WOOD_PER_TREE = 75  # ResourceAmount aus XD_Tree*.xml (Standard-Bäume)
WOOD_PER_EXTRACTION = 2  # Amount aus PU_Serf.xml
EXTRACTION_TIME_WOOD = 5.52  # Sekunden (4s delay + 1.52s animation)

# =============================================================================
# VOLLSTÄNDIGE GEBÄUDE-DATENBANK (80+ Gebäude)
# =============================================================================

_raw_buildings_db = {
    # === HAUPTQUARTIER (3 Level) ===
    "Hauptquartier_1": {
        "build_time": 110, "cost": {RESOURCE_HOLZ: 500, RESOURCE_STEIN: 500, RESOURCE_LEHM: 500},
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 0, "worker_capacity": 100,
        "upgrade_to": "Hauptquartier_2",
        "upgrade_cost": {RESOURCE_STEIN: 800, RESOURCE_LEHM: 300, RESOURCE_TALER: 500},
        "upgrade_time": 90
    },
    "Hauptquartier_2": {
        "build_time": 180, "cost": {RESOURCE_HOLZ: 800, RESOURCE_STEIN: 800, RESOURCE_LEHM: 800},
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 0, "worker_capacity": 150,
        "upgrade_to": "Hauptquartier_3",
        "upgrade_cost": {RESOURCE_STEIN: 1200, RESOURCE_LEHM: 500, RESOURCE_TALER: 1000},
        "upgrade_time": 120
    },
    "Hauptquartier_3": {
        "build_time": 300, "cost": {RESOURCE_HOLZ: 1200, RESOURCE_STEIN: 1200, RESOURCE_LEHM: 1200},
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 0, "worker_capacity": 200,
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === DORFZENTRUM (3 Level) ===
    "Dorfzentrum_1": {
        "build_time": 100, "cost": {RESOURCE_HOLZ: 250, RESOURCE_STEIN: 200, RESOURCE_LEHM: 200},
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 3, "worker_capacity": 75,
        "upgrade_to": "Dorfzentrum_2",
        "upgrade_cost": {RESOURCE_STEIN: 200, RESOURCE_LEHM: 150}, "upgrade_time": 40
    },
    "Dorfzentrum_2": {
        "build_time": 150, "cost": {RESOURCE_HOLZ: 450, RESOURCE_STEIN: 400, RESOURCE_LEHM: 400},
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 5, "worker_capacity": 100,
        "upgrade_to": "Dorfzentrum_3",
        "upgrade_cost": {RESOURCE_STEIN: 350, RESOURCE_LEHM: 250}, "upgrade_time": 50
    },
    "Dorfzentrum_3": {
        "build_time": 220, "cost": {RESOURCE_HOLZ: 700, RESOURCE_STEIN: 600, RESOURCE_LEHM: 600},
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 6, "worker_capacity": 150,
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === WOHNHAUS (3 Level) ===
    "Wohnhaus_1": {
        "build_time": 60, "cost": {RESOURCE_HOLZ: 150, RESOURCE_STEIN: 100, RESOURCE_LEHM: 100},
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 2, "worker_capacity": 10,
        "upgrade_to": "Wohnhaus_2",
        "upgrade_cost": {RESOURCE_STEIN: 100, RESOURCE_LEHM: 50}, "upgrade_time": 30
    },
    "Wohnhaus_2": {
        "build_time": 100, "cost": {RESOURCE_HOLZ: 250, RESOURCE_STEIN: 200, RESOURCE_LEHM: 200},
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 4, "worker_capacity": 20,
        "upgrade_to": "Wohnhaus_3",
        "upgrade_cost": {RESOURCE_STEIN: 200, RESOURCE_LEHM: 100}, "upgrade_time": 40
    },
    "Wohnhaus_3": {
        "build_time": 150, "cost": {RESOURCE_HOLZ: 400, RESOURCE_STEIN: 400, RESOURCE_LEHM: 400},
        "taler_income": 0, "resource_output": {}, "tech_required": None,
        "max_workers": 8, "worker_capacity": 30,
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === BAUERNHOF (3 Level) ===
    "Bauernhof_1": {
        "build_time": 80, "cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 100, RESOURCE_LEHM: 150},
        "taler_income": 0, "resource_output": {}, "tech_required": None, "max_workers": 2,
        "upgrade_to": "Bauernhof_2",
        "upgrade_cost": {RESOURCE_STEIN: 150, RESOURCE_LEHM: 100}, "upgrade_time": 35
    },
    "Bauernhof_2": {
        "build_time": 120, "cost": {RESOURCE_HOLZ: 350, RESOURCE_STEIN: 200, RESOURCE_LEHM: 300},
        "taler_income": 0, "resource_output": {}, "tech_required": None, "max_workers": 4,
        "upgrade_to": "Bauernhof_3",
        "upgrade_cost": {RESOURCE_STEIN: 300, RESOURCE_LEHM: 200}, "upgrade_time": 45
    },
    "Bauernhof_3": {
        "build_time": 180, "cost": {RESOURCE_HOLZ: 550, RESOURCE_STEIN: 400, RESOURCE_LEHM: 500},
        "taler_income": 0, "resource_output": {}, "tech_required": None, "max_workers": 6,
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === HOCHSCHULE (2 Level) - aus pb_university1.xml/pb_university2.xml ===
    "Hochschule_1": {
        "build_time": 90, "cost": {RESOURCE_HOLZ: 200, RESOURCE_LEHM: 300},  # Wood:200, Clay:300
        "taler_income": 35, "resource_output": {}, "tech_required": None,
        "max_workers": 6, "research_speed": 1.0,  # MaxWorkers=6!
        "upgrade_to": "Hochschule_2",
        "upgrade_cost": {RESOURCE_TALER: 150, RESOURCE_STEIN: 100, RESOURCE_LEHM: 100}, "upgrade_time": 50
    },
    "Hochschule_2": {
        "build_time": 60, "cost": {},  # Upgrade-only
        "taler_income": 50, "resource_output": {}, "tech_required": None,
        "max_workers": 8, "research_speed": 1.5,  # MaxWorkers=8!
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === MINEN (3 Level jede) ===
    "Steinmine_1": {
        "build_time": 120, "cost": {RESOURCE_HOLZ: 300, RESOURCE_LEHM: 200},
        "taler_income": 20, "resource_output": {RESOURCE_STEIN: 2}, "tech_required": None,
        "max_workers": 4, "mine_type": "Steinmine",
        "upgrade_to": "Steinmine_2",
        "upgrade_cost": {RESOURCE_STEIN: 300, RESOURCE_LEHM: 250}, "upgrade_time": 40
    },
    "Steinmine_2": {
        "build_time": 180, "cost": {RESOURCE_HOLZ: 400, RESOURCE_STEIN: 200, RESOURCE_LEHM: 300},
        "taler_income": 30, "resource_output": {RESOURCE_STEIN: 3}, "tech_required": None,
        "max_workers": 6, "mine_type": "Steinmine",
        "upgrade_to": "Steinmine_3",
        "upgrade_cost": {RESOURCE_STEIN: 400, RESOURCE_LEHM: 350}, "upgrade_time": 50
    },
    "Steinmine_3": {
        "build_time": 240, "cost": {RESOURCE_HOLZ: 500, RESOURCE_STEIN: 300, RESOURCE_LEHM: 500},
        "taler_income": 40, "resource_output": {RESOURCE_STEIN: 4}, "tech_required": None,
        "max_workers": 8, "mine_type": "Steinmine",
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "Lehmmine_1": {
        "build_time": 120, "cost": {RESOURCE_HOLZ: 350, RESOURCE_STEIN: 250},
        "taler_income": 10, "resource_output": {RESOURCE_LEHM: 2}, "tech_required": None,
        "max_workers": 4, "mine_type": "Lehmmine",
        "upgrade_to": "Lehmmine_2",
        "upgrade_cost": {RESOURCE_STEIN: 250, RESOURCE_LEHM: 200}, "upgrade_time": 40
    },
    "Lehmmine_2": {
        "build_time": 180, "cost": {RESOURCE_HOLZ: 450, RESOURCE_STEIN: 350, RESOURCE_LEHM: 100},
        "taler_income": 15, "resource_output": {RESOURCE_LEHM: 3}, "tech_required": None,
        "max_workers": 6, "mine_type": "Lehmmine",
        "upgrade_to": "Lehmmine_3",
        "upgrade_cost": {RESOURCE_STEIN: 350, RESOURCE_LEHM: 300}, "upgrade_time": 50
    },
    "Lehmmine_3": {
        "build_time": 240, "cost": {RESOURCE_HOLZ: 550, RESOURCE_STEIN: 450, RESOURCE_LEHM: 200},
        "taler_income": 20, "resource_output": {RESOURCE_LEHM: 4}, "tech_required": None,
        "max_workers": 8, "mine_type": "Lehmmine",
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "Eisenmine_1": {
        "build_time": 120, "cost": {RESOURCE_HOLZ: 300, RESOURCE_STEIN: 300},
        "taler_income": 25, "resource_output": {RESOURCE_EISEN: 2}, "tech_required": None,
        "max_workers": 4, "mine_type": "Eisenmine",
        "upgrade_to": "Eisenmine_2",
        "upgrade_cost": {RESOURCE_STEIN: 300, RESOURCE_LEHM: 200}, "upgrade_time": 40
    },
    "Eisenmine_2": {
        "build_time": 180, "cost": {RESOURCE_HOLZ: 400, RESOURCE_STEIN: 450, RESOURCE_LEHM: 200},
        "taler_income": 35, "resource_output": {RESOURCE_EISEN: 3}, "tech_required": None,
        "max_workers": 6, "mine_type": "Eisenmine",
        "upgrade_to": "Eisenmine_3",
        "upgrade_cost": {RESOURCE_STEIN: 400, RESOURCE_LEHM: 300}, "upgrade_time": 50
    },
    "Eisenmine_3": {
        "build_time": 240, "cost": {RESOURCE_HOLZ: 500, RESOURCE_STEIN: 600, RESOURCE_LEHM: 400},
        "taler_income": 45, "resource_output": {RESOURCE_EISEN: 4}, "tech_required": None,
        "max_workers": 8, "mine_type": "Eisenmine",
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "Schwefelmine_1": {
        "build_time": 120, "cost": {RESOURCE_HOLZ: 300, RESOURCE_STEIN: 200, RESOURCE_LEHM: 300},
        "taler_income": 25, "resource_output": {RESOURCE_SCHWEFEL: 2}, "tech_required": None,
        "max_workers": 4, "mine_type": "Schwefelmine",
        "upgrade_to": "Schwefelmine_2",
        "upgrade_cost": {RESOURCE_STEIN: 300, RESOURCE_LEHM: 250}, "upgrade_time": 40
    },
    "Schwefelmine_2": {
        "build_time": 180, "cost": {RESOURCE_HOLZ: 400, RESOURCE_STEIN: 300, RESOURCE_LEHM: 400},
        "taler_income": 35, "resource_output": {RESOURCE_SCHWEFEL: 3}, "tech_required": None,
        "max_workers": 6, "mine_type": "Schwefelmine",
        "upgrade_to": "Schwefelmine_3",
        "upgrade_cost": {RESOURCE_STEIN: 400, RESOURCE_LEHM: 350}, "upgrade_time": 50
    },
    "Schwefelmine_3": {
        "build_time": 240, "cost": {RESOURCE_HOLZ: 500, RESOURCE_STEIN: 400, RESOURCE_LEHM: 600},
        "taler_income": 45, "resource_output": {RESOURCE_SCHWEFEL: 4}, "tech_required": None,
        "max_workers": 8, "mine_type": "Schwefelmine",
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === PRODUKTIONSGEBÄUDE ===
    "Sägemühle_1": {
        "build_time": 100, "cost": {RESOURCE_STEIN: 300, RESOURCE_LEHM: 150},
        "taler_income": 12, "resource_output": {RESOURCE_HOLZ: 3}, "tech_required": "Konstruktion",
        "max_workers": 6, "upgrade_to": "Sägemühle_2",
        "upgrade_cost": {RESOURCE_STEIN: 200, RESOURCE_LEHM: 100}, "upgrade_time": 40
    },
    "Sägemühle_2": {
        "build_time": 160, "cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 400, RESOURCE_LEHM: 300},
        "taler_income": 18, "resource_output": {RESOURCE_HOLZ: 5}, "tech_required": "Konstruktion",
        "max_workers": 6, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "Lehmhütte_1": {
        "build_time": 110, "cost": {RESOURCE_HOLZ: 400, RESOURCE_STEIN: 300},
        "taler_income": 12, "resource_output": {RESOURCE_LEHM: 3}, "tech_required": "Konstruktion",
        "max_workers": 6, "upgrade_to": "Lehmhütte_2",
        "upgrade_cost": {RESOURCE_STEIN: 200, RESOURCE_LEHM: 150}, "upgrade_time": 40
    },
    "Lehmhütte_2": {
        "build_time": 170, "cost": {RESOURCE_HOLZ: 500, RESOURCE_STEIN: 400, RESOURCE_LEHM: 200},
        "taler_income": 18, "resource_output": {RESOURCE_LEHM: 5}, "tech_required": "Konstruktion",
        "max_workers": 6, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "Schmiede_1": {
        "build_time": 110, "cost": {RESOURCE_HOLZ: 400, RESOURCE_STEIN: 300},
        "taler_income": 12, "resource_output": {RESOURCE_EISEN: 1}, "tech_required": "Alchimie",
        "max_workers": 4, "upgrade_to": "Schmiede_2",
        "upgrade_cost": {RESOURCE_STEIN: 200, RESOURCE_LEHM: 150}, "upgrade_time": 40
    },
    "Schmiede_2": {
        "build_time": 160, "cost": {RESOURCE_HOLZ: 500, RESOURCE_STEIN: 400, RESOURCE_LEHM: 200},
        "taler_income": 18, "resource_output": {RESOURCE_EISEN: 2}, "tech_required": "Alchimie",
        "max_workers": 5, "upgrade_to": "Schmiede_3",
        "upgrade_cost": {RESOURCE_STEIN: 300, RESOURCE_LEHM: 250}, "upgrade_time": 50
    },
    "Schmiede_3": {
        "build_time": 220, "cost": {RESOURCE_HOLZ: 600, RESOURCE_STEIN: 500, RESOURCE_LEHM: 400},
        "taler_income": 24, "resource_output": {RESOURCE_EISEN: 3}, "tech_required": "Alchimie",
        "max_workers": 6, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "Alchimistenhütte_1": {
        "build_time": 120, "cost": {RESOURCE_HOLZ: 300, RESOURCE_STEIN: 400, RESOURCE_LEHM: 100},
        "taler_income": 12, "resource_output": {RESOURCE_SCHWEFEL: 3}, "tech_required": "Alchimie",
        "max_workers": 4, "upgrade_to": "Alchimistenhütte_2",
        "upgrade_cost": {RESOURCE_STEIN: 250, RESOURCE_LEHM: 150}, "upgrade_time": 45
    },
    "Alchimistenhütte_2": {
        "build_time": 180, "cost": {RESOURCE_HOLZ: 400, RESOURCE_STEIN: 500, RESOURCE_LEHM: 300},
        "taler_income": 18, "resource_output": {RESOURCE_SCHWEFEL: 5}, "tech_required": "Alchimie",
        "max_workers": 6, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "Steinmetzhütte_1": {
        "build_time": 110, "cost": {RESOURCE_HOLZ: 300, RESOURCE_LEHM: 200},
        "taler_income": 12, "resource_output": {RESOURCE_STEIN: 3}, "tech_required": "Zahnräder",
        "max_workers": 6, "upgrade_to": "Steinmetzhütte_2",
        "upgrade_cost": {RESOURCE_STEIN: 200, RESOURCE_LEHM: 100}, "upgrade_time": 40
    },
    "Steinmetzhütte_2": {
        "build_time": 170, "cost": {RESOURCE_HOLZ: 400, RESOURCE_STEIN: 200, RESOURCE_LEHM: 400},
        "taler_income": 18, "resource_output": {RESOURCE_STEIN: 5}, "tech_required": "Zahnräder",
        "max_workers": 6, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === SPEZIALGEBÄUDE ===
    "Bank_1": {
        "build_time": 130, "cost": {RESOURCE_HOLZ: 500, RESOURCE_STEIN: 500},
        "taler_income": 30, "resource_output": {RESOURCE_TALER: 2}, "tech_required": "Buchdruck",
        "max_workers": 4, "upgrade_to": "Bank_2",
        "upgrade_cost": {RESOURCE_STEIN: 300, RESOURCE_TALER: 200}, "upgrade_time": 40
    },
    "Bank_2": {
        "build_time": 200, "cost": {RESOURCE_HOLZ: 600, RESOURCE_STEIN: 600, RESOURCE_LEHM: 200},
        "taler_income": 45, "resource_output": {RESOURCE_TALER: 4}, "tech_required": "Buchdruck",
        "max_workers": 6, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

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
        "build_time": 210, "cost": {RESOURCE_HOLZ: 650, RESOURCE_STEIN: 700, RESOURCE_LEHM: 300},
        "taler_income": 0, "resource_output": {}, "tech_required": "Bildung",
        "max_workers": 8, "motivation_effect": 0.10,
        "upgrade_to": "Kloster_3",
        "upgrade_cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 600, RESOURCE_TALER: 300}, "upgrade_time": 90
    },
    "Kloster_3": {
        "build_time": 300, "cost": {RESOURCE_HOLZ: 800, RESOURCE_STEIN: 900, RESOURCE_LEHM: 500},
        "taler_income": 0, "resource_output": {}, "tech_required": "Bildung",
        "max_workers": 10, "motivation_effect": 0.15,
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === MARKT/LAGER (aus extra2) ===
    # Ist ein Supplier für ALLE Ressourcen - Serfs können dort Ressourcen abholen
    # Level 1: Keine Arbeiter (Trade auskommentiert in extra2)
    # Level 2: 6 Trader (für Handel, aber wir nutzen nur als Lager)
    "Markt_1": {
        "build_time": 80, "cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 400},
        "taler_income": 0, "resource_output": {}, "tech_required": "Handelswesen",
        "max_workers": 0, "is_supplier": True,  # Kann als Ressourcen-Quelle dienen
        "supplier_resources": ["Holz", "Stein", "Lehm", "Eisen", "Schwefel", "Taler"],
        "upgrade_to": "Markt_2",
        "upgrade_cost": {RESOURCE_LEHM: 100, RESOURCE_STEIN: 200}, "upgrade_time": 40
    },
    "Markt_2": {
        "build_time": 120, "cost": {RESOURCE_HOLZ: 350, RESOURCE_STEIN: 550, RESOURCE_LEHM: 150},
        "taler_income": 0, "resource_output": {}, "tech_required": "Handelswesen",
        "max_workers": 6, "is_supplier": True,
        "supplier_resources": ["Holz", "Stein", "Lehm", "Eisen", "Schwefel", "Taler"],
        "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === MILITÄRGEBÄUDE ===
    "Kaserne_1": {
        "build_time": 90, "cost": {RESOURCE_HOLZ: 300, RESOURCE_STEIN: 350},
        "taler_income": 0, "resource_output": {}, "tech_required": "Wehrpflicht",
        "max_workers": 0, "upgrade_to": "Kaserne_2",
        "upgrade_cost": {RESOURCE_STEIN: 300, RESOURCE_LEHM: 200}, "upgrade_time": 40
    },
    "Kaserne_2": {
        "build_time": 150, "cost": {RESOURCE_HOLZ: 450, RESOURCE_STEIN: 500, RESOURCE_LEHM: 300},
        "taler_income": 0, "resource_output": {}, "tech_required": "Wehrpflicht",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "Schießplatz_1": {
        "build_time": 90, "cost": {RESOURCE_HOLZ: 300, RESOURCE_STEIN: 350, RESOURCE_LEHM: 100},
        "taler_income": 0, "resource_output": {}, "tech_required": "Stehendes Heer",
        "max_workers": 0, "upgrade_to": "Schießplatz_2",
        "upgrade_cost": {RESOURCE_STEIN: 300, RESOURCE_LEHM: 200}, "upgrade_time": 40
    },
    "Schießplatz_2": {
        "build_time": 150, "cost": {RESOURCE_HOLZ: 450, RESOURCE_STEIN: 500, RESOURCE_LEHM: 300},
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
        "build_time": 180, "cost": {RESOURCE_HOLZ: 350, RESOURCE_STEIN: 450, RESOURCE_LEHM: 200},
        "taler_income": 0, "resource_output": {}, "tech_required": "Taktiken",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "Kanongießerei_1": {
        "build_time": 110, "cost": {RESOURCE_HOLZ: 300, RESOURCE_LEHM: 500},
        "taler_income": 5, "resource_output": {}, "tech_required": "Metallurgie",
        "max_workers": 1, "upgrade_to": "Kanongießerei_2",
        "upgrade_cost": {RESOURCE_STEIN: 200, RESOURCE_LEHM: 150}, "upgrade_time": 40
    },
    "Kanongießerei_2": {
        "build_time": 150, "cost": {RESOURCE_HOLZ: 400, RESOURCE_STEIN: 100, RESOURCE_LEHM: 600},
        "taler_income": 10, "resource_output": {}, "tech_required": "Metallurgie",
        "max_workers": 1, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # === TÜRME ===
    "Turm_1": {
        "build_time": 80, "cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 200},
        "taler_income": 0, "resource_output": {}, "tech_required": "Konstruktion",
        "max_workers": 0, "upgrade_to": "Turm_2",
        "upgrade_cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 300}, "upgrade_time": 15
    },
    "Turm_2": {
        "build_time": 120, "cost": {RESOURCE_HOLZ: 300, RESOURCE_STEIN: 300, RESOURCE_LEHM: 100},
        "taler_income": 0, "resource_output": {}, "tech_required": "Konstruktion",
        "max_workers": 0, "upgrade_to": "Turm_3",
        "upgrade_cost": {RESOURCE_HOLZ: 250, RESOURCE_STEIN: 400, RESOURCE_LEHM: 50}, "upgrade_time": 25
    },
    "Turm_3": {
        "build_time": 180, "cost": {RESOURCE_HOLZ: 400, RESOURCE_STEIN: 450, RESOURCE_LEHM: 200},
        "taler_income": 0, "resource_output": {}, "tech_required": "Konstruktion",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    # Aussichtsturm entfernt - existiert nicht im echten Spiel!
    # (pb_darktower ist nur für KI/Feinde)

    # === WETTERGEBÄUDE ===
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

    # === ADDON-GEBÄUDE ===
    "Taverne_1": {
        "build_time": 100, "cost": {RESOURCE_STEIN: 400, RESOURCE_HOLZ: 300, RESOURCE_LEHM: 100},
        "taler_income": 25, "resource_output": {}, "tech_required": "Fernglas",
        "max_workers": 3, "upgrade_to": "Taverne_2",
        "upgrade_cost": {RESOURCE_STEIN: 300, RESOURCE_LEHM: 200}, "upgrade_time": 50
    },
    "Taverne_2": {
        "build_time": 150, "cost": {RESOURCE_STEIN: 600, RESOURCE_HOLZ: 400, RESOURCE_LEHM: 300},
        "taler_income": 40, "resource_output": {}, "tech_required": "Fernglas",
        "max_workers": 5, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "Büchsenmacherei_1": {
        "build_time": 110, "cost": {RESOURCE_STEIN: 400, RESOURCE_SCHWEFEL: 300},  # Kein Eisen! (aus PB_GunsmithWorkshop1.xml)
        "taler_income": 15, "resource_output": {}, "tech_required": "Luntenschloss",
        "max_workers": 2, "upgrade_to": "Büchsenmacherei_2",  # MaxWorkers=2 (aus XML)
        "upgrade_cost": {RESOURCE_STEIN: 300, RESOURCE_SCHWEFEL: 200}, "upgrade_time": 40  # UpgradeTime=40 (aus XML)
    },
    "Büchsenmacherei_2": {
        "build_time": 180, "cost": {RESOURCE_STEIN: 600, RESOURCE_SCHWEFEL: 500, RESOURCE_EISEN: 300},
        "taler_income": 25, "resource_output": {}, "tech_required": "Luntenschloss",
        "max_workers": 4, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None  # MaxWorkers=4 aus XML
    },

    "Architektenstube": {
        "build_time": 100, "cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 400},
        "taler_income": 10, "resource_output": {}, "tech_required": "Mathematik",
        "max_workers": 3, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },

    "Brücke": {
        "build_time": 60, "cost": {RESOURCE_HOLZ: 300, RESOURCE_STEIN: 200},
        "taler_income": 0, "resource_output": {}, "tech_required": "Mathematik",
        "max_workers": 0, "upgrade_to": None, "upgrade_cost": None, "upgrade_time": None
    },
}

# Gebäude-Datenbank (ohne Multiplikator - echte Spielwerte)
buildings_db = copy.deepcopy(_raw_buildings_db)


# =============================================================================
# VOLLSTÄNDIGE TECHNOLOGIE-DATENBANK (55+ Technologien)
# =============================================================================

technologies = {
    # === KONSTRUKTION-ZWEIG ===
    "Konstruktion": {"cost": {RESOURCE_HOLZ: 200, RESOURCE_LEHM: 150}, "tech_required": [],
                    "unlocks_buildings": ["Sägemühle_1", "Lehmhütte_1", "Turm_1"], "research_time": 20},
    "Zahnräder": {"cost": {RESOURCE_STEIN: 400, RESOURCE_EISEN: 200}, "tech_required": ["Konstruktion"],
                 "unlocks_buildings": ["Steinmetzhütte_1"], "research_time": 40},
    "Flaschenzug": {"cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 300}, "tech_required": ["Zahnräder"],
                   "unlocks_buildings": [], "research_time": 40},
    "Architektur": {"cost": {RESOURCE_STEIN: 600, RESOURCE_EISEN: 500}, "tech_required": ["Flaschenzug"],
                   "unlocks_buildings": [], "research_time": 80, "effects": {"armor_bonus": 5}},

    # === ALCHIMIE-ZWEIG ===
    "Alchimie": {"cost": {RESOURCE_HOLZ: 50, RESOURCE_SCHWEFEL: 150}, "tech_required": [],
                "unlocks_buildings": ["Alchimistenhütte_1", "Schmiede_1"], "research_time": 20},
    "Legierungen": {"cost": {RESOURCE_EISEN: 200, RESOURCE_SCHWEFEL: 300}, "tech_required": ["Alchimie"],
                   "unlocks_buildings": [], "research_time": 40},
    "Metallurgie": {"cost": {RESOURCE_EISEN: 400, RESOURCE_SCHWEFEL: 400}, "tech_required": ["Legierungen"],
                   "unlocks_buildings": ["Kanongießerei_1"], "research_time": 60},
    "Chemie": {"cost": {RESOURCE_EISEN: 500, RESOURCE_SCHWEFEL: 600}, "tech_required": ["Metallurgie"],
              "unlocks_buildings": ["Wetterkraftwerk"], "research_time": 80},

    # === BILDUNG-ZWEIG ===
    "Bildung": {"cost": {RESOURCE_TALER: 50, RESOURCE_HOLZ: 150}, "tech_required": [],
               "unlocks_buildings": ["Kloster_1"], "research_time": 20},
    "Handelswesen": {"cost": {RESOURCE_TALER: 300}, "tech_required": ["Bildung"],
                    "unlocks_buildings": ["Markt_1"], "research_time": 40},
    "Buchdruck": {"cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 200}, "tech_required": ["Handelswesen"],
                 "unlocks_buildings": ["Bank_1"], "research_time": 40},
    "Büchereien": {"cost": {RESOURCE_TALER: 500, RESOURCE_HOLZ: 300}, "tech_required": ["Buchdruck"],
                  "unlocks_buildings": [], "research_time": 80},

    # === MILITÄR-ZWEIG ===
    "Wehrpflicht": {"cost": {RESOURCE_TALER: 50, RESOURCE_HOLZ: 150}, "tech_required": [],
                   "unlocks_buildings": ["Kaserne_1"], "research_time": 20},
    "Stehendes Heer": {"cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 200}, "tech_required": ["Wehrpflicht"],
                      "unlocks_buildings": ["Schießplatz_1"], "research_time": 40},
    "Taktiken": {"cost": {RESOURCE_TALER: 400, RESOURCE_EISEN: 400}, "tech_required": ["Stehendes Heer"],
                "unlocks_buildings": ["Stall_1"], "research_time": 60, "effects": {"speed_bonus": 50}},
    "Strategien": {"cost": {RESOURCE_TALER: 600, RESOURCE_EISEN: 600}, "tech_required": ["Taktiken"],
                  "unlocks_buildings": [], "research_time": 80, "requires_building": "Hauptquartier_3"},
    "Pferdezucht": {"cost": {RESOURCE_TALER: 600, RESOURCE_EISEN: 600}, "tech_required": ["Strategien"],
                   "unlocks_buildings": [], "research_time": 80},

    # === MATHEMATIK/WISSENSCHAFT-ZWEIG (Scharfschützen-Pfad) ===
    "Mathematik": {"cost": {RESOURCE_TALER: 100, RESOURCE_HOLZ: 200}, "tech_required": [],
                  "unlocks_buildings": ["Architektenstube"], "research_time": 20},
    "Fernglas": {"cost": {RESOURCE_TALER: 300, RESOURCE_EISEN: 300}, "tech_required": ["Mathematik"],
                "unlocks_buildings": ["Wetterturm", "Taverne_1"], "research_time": 30, "requires_building": "Hauptquartier_2"},
    "Luntenschloss": {"cost": {RESOURCE_EISEN: 300, RESOURCE_SCHWEFEL: 300}, "tech_required": ["Fernglas"],
                     "unlocks_buildings": ["Büchsenmacherei_1"], "research_time": 50, "requires_building": "Hauptquartier_2"},
    "Gezogener Lauf": {"cost": {RESOURCE_EISEN: 500, RESOURCE_SCHWEFEL: 400}, "tech_required": ["Luntenschloss"],
                      "unlocks_buildings": [], "research_time": 70, "requires_building": "Hauptquartier_3"},  # TimeToResearch=70, braucht HQ3!

    # === RÜSTUNGS-TECHNOLOGIEN ===
    "Lederrüstung": {"cost": {RESOURCE_TALER: 100, RESOURCE_EISEN: 100}, "tech_required": [],
                    "unlocks_buildings": [], "research_time": 15, "effects": {"armor_bonus": 2}, "requires_building": "Schmiede_1"},
    "Kettenrüstung": {"cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 200}, "tech_required": ["Lederrüstung"],
                     "unlocks_buildings": [], "research_time": 25, "effects": {"armor_bonus": 4}, "requires_building": "Schmiede_2"},
    "Plattenrüstung": {"cost": {RESOURCE_TALER: 300, RESOURCE_EISEN: 300}, "tech_required": ["Kettenrüstung"],
                      "unlocks_buildings": [], "research_time": 35, "effects": {"armor_bonus": 6}, "requires_building": "Schmiede_3"},

    # === GEBÄUDE-TECHNOLOGIEN ===
    "Maurerarbeit": {"cost": {RESOURCE_HOLZ: 200, RESOURCE_STEIN: 400}, "tech_required": [],
                    "unlocks_buildings": [], "research_time": 20, "effects": {"building_armor_bonus": 3}, "requires_building": "Steinmetzhütte_2"},
    "Leichte Ziegel": {"cost": {RESOURCE_LEHM: 300, RESOURCE_HOLZ: 100}, "tech_required": [],
                      "unlocks_buildings": [], "research_time": 20, "effects": {"build_speed_bonus": 15}, "requires_building": "Lehmhütte_2"},

    # === FERNKAMPF-TECHNOLOGIEN ===
    "Pfeilherstellung": {"cost": {RESOURCE_HOLZ: 200, RESOURCE_EISEN: 100}, "tech_required": [],
                        "unlocks_buildings": [], "research_time": 15, "effects": {"bow_damage_bonus": 2}, "requires_building": "Sägemühle_1"},
    "Panzerbrechende Pfeile": {"cost": {RESOURCE_HOLZ: 300, RESOURCE_EISEN: 200}, "tech_required": ["Pfeilherstellung"],
                              "unlocks_buildings": [], "research_time": 25, "effects": {"bow_damage_bonus": 4}, "requires_building": "Sägemühle_2"},

    # === ARTILLERIE-TECHNOLOGIEN ===
    "Verbessertes Schießpulver": {"cost": {RESOURCE_SCHWEFEL: 400, RESOURCE_EISEN: 200}, "tech_required": [],
                                  "unlocks_buildings": [], "research_time": 30, "effects": {"cannon_damage_bonus": 3}, "requires_building": "Alchimistenhütte_1"},
    "Glühende Kanonenkugeln": {"cost": {RESOURCE_SCHWEFEL: 500, RESOURCE_EISEN: 300}, "tech_required": ["Verbessertes Schießpulver"],
                              "unlocks_buildings": [], "research_time": 40, "effects": {"cannon_damage_bonus": 5}, "requires_building": "Alchimistenhütte_2"},

    # === NAHKAMPF-TECHNOLOGIEN ===
    "Schmiedekunst": {"cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 200}, "tech_required": [],
                     "unlocks_buildings": [], "research_time": 20, "effects": {"melee_damage_bonus": 2}, "requires_building": "Schmiede_1"},
    "Eisenguss": {"cost": {RESOURCE_TALER: 300, RESOURCE_EISEN: 300}, "tech_required": ["Schmiedekunst"],
                 "unlocks_buildings": [], "research_time": 30, "effects": {"melee_damage_bonus": 4}, "requires_building": "Schmiede_2"},

    # === BOGENSCHÜTZEN-RÜSTUNG ===
    "Weiche Rüstung": {"cost": {RESOURCE_TALER: 100, RESOURCE_EISEN: 100}, "tech_required": [],
                      "unlocks_buildings": [], "research_time": 15, "effects": {"archer_armor_bonus": 1}, "requires_building": "Schmiede_1"},
    "Wattierte Rüstung": {"cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 200}, "tech_required": ["Weiche Rüstung"],
                         "unlocks_buildings": [], "research_time": 20, "effects": {"archer_armor_bonus": 2}, "requires_building": "Schmiede_2"},
    "Leder-Bogenschützenrüstung": {"cost": {RESOURCE_TALER: 300, RESOURCE_EISEN: 300}, "tech_required": ["Wattierte Rüstung"],
                                   "unlocks_buildings": [], "research_time": 25, "effects": {"archer_armor_bonus": 3}, "requires_building": "Schmiede_3"},

    # === SPEERTRÄGER-TECHNOLOGIEN ===
    "Holzalterung": {"cost": {RESOURCE_HOLZ: 200, RESOURCE_TALER: 100}, "tech_required": [],
                    "unlocks_buildings": [], "research_time": 20, "effects": {"spear_damage_bonus": 2}, "requires_building": "Sägemühle_1"},
    "Drechselei": {"cost": {RESOURCE_HOLZ: 300, RESOURCE_TALER: 200}, "tech_required": ["Holzalterung"],
                  "unlocks_buildings": [], "research_time": 25, "effects": {"spear_damage_bonus": 4}, "requires_building": "Sägemühle_2"},

    # === WETTER-TECHNOLOGIEN ===
    "Wettervorhersage": {"cost": {RESOURCE_SCHWEFEL: 200, RESOURCE_TALER: 200}, "tech_required": [],
                        "unlocks_buildings": [], "research_time": 30, "requires_building": "Alchimistenhütte_1"},
    "Wettermanipulation": {"cost": {RESOURCE_SCHWEFEL: 400, RESOURCE_TALER: 400}, "tech_required": ["Wettervorhersage"],
                          "unlocks_buildings": [], "research_time": 50, "requires_building": "Alchimistenhütte_2"},

    # === BANK-TECHNOLOGIEN ===
    "Schuldschein": {"cost": {RESOURCE_TALER: 300}, "tech_required": [],
                    "unlocks_buildings": [], "research_time": 30, "effects": {"payday_bonus": 10}, "requires_building": "Bank_1"},
    "Buchführung": {"cost": {RESOURCE_TALER: 500}, "tech_required": ["Schuldschein"],
                   "unlocks_buildings": [], "research_time": 40, "effects": {"payday_bonus": 20}, "requires_building": "Bank_2"},
    "Waage": {"cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 100}, "tech_required": [],
              "unlocks_buildings": [], "research_time": 20, "effects": {"trade_bonus": 5}, "requires_building": "Bank_1"},
    "Münzprägung": {"cost": {RESOURCE_TALER: 400, RESOURCE_EISEN: 200}, "tech_required": ["Waage"],
                   "unlocks_buildings": [], "research_time": 30, "effects": {"trade_bonus": 10}, "requires_building": "Bank_2"},

    # === DORFZENTRUM-TECHNOLOGIEN ===
    "Stadtwache": {"cost": {RESOURCE_TALER: 200, RESOURCE_HOLZ: 200}, "tech_required": [],
                  "unlocks_buildings": [], "research_time": 25, "effects": {"exploration_bonus": 5}, "requires_building": "Dorfzentrum_2"},
    "Webstuhl": {"cost": {RESOURCE_HOLZ: 200, RESOURCE_TALER: 100}, "tech_required": [],
                "unlocks_buildings": [], "research_time": 20, "effects": {"worker_armor_bonus": 1}, "requires_building": "Dorfzentrum_1"},
    "Schuhe": {"cost": {RESOURCE_HOLZ: 300, RESOURCE_TALER: 200}, "tech_required": ["Webstuhl"],
              "unlocks_buildings": [], "research_time": 25, "effects": {"worker_speed_bonus": 20}, "requires_building": "Dorfzentrum_2"},

    # === MILITÄRGEBÄUDE-TECHNOLOGIEN ===
    "Kasernentraining": {"cost": {RESOURCE_TALER: 300, RESOURCE_EISEN: 200}, "tech_required": [],
                        "unlocks_buildings": [], "research_time": 30, "effects": {"infantry_training_speed": 20}, "requires_building": "Kaserne_2"},
    "Schießtraining": {"cost": {RESOURCE_TALER: 300, RESOURCE_HOLZ: 200}, "tech_required": [],
                      "unlocks_buildings": [], "research_time": 30, "effects": {"archer_training_speed": 20}, "requires_building": "Schießplatz_2"},
    "Hufbeschlag": {"cost": {RESOURCE_TALER: 200, RESOURCE_EISEN: 200}, "tech_required": [],
                   "unlocks_buildings": [], "research_time": 50, "effects": {"cavalry_speed_bonus": 50}, "requires_building": "Stall_2"},
    "Verbessertes Fahrgestell": {"cost": {RESOURCE_EISEN: 300, RESOURCE_HOLZ: 200}, "tech_required": [],
                                 "unlocks_buildings": [], "research_time": 40, "effects": {"cannon_speed_bonus": 30}, "requires_building": "Kanongießerei_2"},
}


# =============================================================================
# VOLLSTÄNDIGE SOLDATEN-DATENBANK (40+ Einheiten)
# =============================================================================

soldiers_db = {
    # === SCHWERTKÄMPFER (4 Level) ===
    "Schwertkämpfer_1": {"cost": {RESOURCE_TALER: 30, RESOURCE_EISEN: 20}, "requirements": ["Kaserne_1"],
                         "population_cost": 1, "train_time": 15, "upgrade_to": "Schwertkämpfer_2"},
    "Schwertkämpfer_2": {"cost": {RESOURCE_TALER: 40, RESOURCE_EISEN: 30}, "requirements": ["Kaserne_1"],
                         "population_cost": 1, "train_time": 20, "upgrade_to": "Schwertkämpfer_3"},
    "Schwertkämpfer_3": {"cost": {RESOURCE_TALER: 50, RESOURCE_EISEN: 40}, "requirements": ["Kaserne_2"],
                         "population_cost": 1, "train_time": 25, "upgrade_to": "Schwertkämpfer_4"},
    "Schwertkämpfer_4": {"cost": {RESOURCE_TALER: 60, RESOURCE_EISEN: 50}, "requirements": ["Kaserne_2"],
                         "population_cost": 1, "train_time": 30, "upgrade_to": None},

    # === SPEERTRÄGER (4 Level) ===
    "Speerträger_1": {"cost": {RESOURCE_TALER: 30, RESOURCE_HOLZ: 20}, "requirements": ["Kaserne_1"],
                      "population_cost": 1, "train_time": 15, "upgrade_to": "Speerträger_2"},
    "Speerträger_2": {"cost": {RESOURCE_TALER: 40, RESOURCE_HOLZ: 30}, "requirements": ["Kaserne_1"],
                      "population_cost": 1, "train_time": 20, "upgrade_to": "Speerträger_3"},
    "Speerträger_3": {"cost": {RESOURCE_TALER: 50, RESOURCE_HOLZ: 40}, "requirements": ["Kaserne_2"],
                      "population_cost": 1, "train_time": 25, "upgrade_to": "Speerträger_4"},
    "Speerträger_4": {"cost": {RESOURCE_TALER: 60, RESOURCE_HOLZ: 50}, "requirements": ["Kaserne_2"],
                      "population_cost": 1, "train_time": 30, "upgrade_to": None},

    # === BOGENSCHÜTZEN (4 Level) ===
    "Bogenschützen_1": {"cost": {RESOURCE_TALER: 30, RESOURCE_HOLZ: 30}, "requirements": ["Schießplatz_1"],
                        "population_cost": 1, "train_time": 15, "upgrade_to": "Bogenschützen_2"},
    "Bogenschützen_2": {"cost": {RESOURCE_TALER: 40, RESOURCE_HOLZ: 40}, "requirements": ["Schießplatz_1"],
                        "population_cost": 1, "train_time": 20, "upgrade_to": "Bogenschützen_3"},
    "Bogenschützen_3": {"cost": {RESOURCE_TALER: 50, RESOURCE_EISEN: 40}, "requirements": ["Schießplatz_2"],
                        "population_cost": 1, "train_time": 25, "upgrade_to": "Bogenschützen_4"},
    "Bogenschützen_4": {"cost": {RESOURCE_TALER: 60, RESOURCE_EISEN: 50}, "requirements": ["Schießplatz_2"],
                        "population_cost": 1, "train_time": 30, "upgrade_to": None},

    # === LEICHTE KAVALLERIE (2 Level) ===
    "Leichte Kavallerie_1": {"cost": {RESOURCE_TALER: 80, RESOURCE_EISEN: 30}, "requirements": ["Stall_1"],
                              "population_cost": 2, "train_time": 30, "upgrade_to": "Leichte Kavallerie_2"},
    "Leichte Kavallerie_2": {"cost": {RESOURCE_TALER: 100, RESOURCE_EISEN: 40}, "requirements": ["Stall_2"],
                              "population_cost": 2, "train_time": 40, "upgrade_to": None},

    # === SCHWERE KAVALLERIE (2 Level) ===
    "Schwere Kavallerie_1": {"cost": {RESOURCE_TALER: 120, RESOURCE_EISEN: 40}, "requirements": ["Stall_1", "Taktiken"],
                              "population_cost": 3, "train_time": 40, "upgrade_to": "Schwere Kavallerie_2"},
    "Schwere Kavallerie_2": {"cost": {RESOURCE_TALER: 150, RESOURCE_EISEN: 50}, "requirements": ["Stall_2", "Pferdezucht"],
                              "population_cost": 3, "train_time": 50, "upgrade_to": None},

    # === KANONEN ===
    "Kanonen": {"cost": {RESOURCE_TALER: 100, RESOURCE_EISEN: 100}, "requirements": ["Kanongießerei_1"],
                "population_cost": 5, "train_time": 60, "upgrade_to": None},

    # === SCHARFSCHÜTZEN (2 Level) - HAUPTZIEL! ===
    # Kosten aus PU_SoldierRifle1.xml: Gold=50, Sulfur=40
    "Scharfschützen": {"cost": {RESOURCE_TALER: 50, RESOURCE_SCHWEFEL: 40}, "requirements": ["Büchsenmacherei_1"],
                       "population_cost": 1, "train_time": 20, "upgrade_to": "Scharfschützen_2"},
    # Kosten aus PU_LeaderRifle1.xml: Gold=300, Sulfur=80
    "Scharfschützen_2": {"cost": {RESOURCE_TALER: 300, RESOURCE_SCHWEFEL: 80}, "requirements": ["Büchsenmacherei_2", "Gezogener Lauf"],
                         "population_cost": 1, "train_time": 30, "upgrade_to": None},

    # === SPEZIALEINHEITEN ===
    "Dieb": {"cost": {RESOURCE_TALER: 300, RESOURCE_EISEN: 30}, "requirements": ["Taverne_2"],
             "population_cost": 5, "train_time": 45, "upgrade_to": None},
    "Späher": {"cost": {RESOURCE_TALER: 100, RESOURCE_EISEN: 50}, "requirements": ["Taverne_1"],
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
MAX_POSSIBLE_LEIBEIGENE = 300

# =============================================================================
# LEIBEIGENE & STEUER-KONSTANTEN
# =============================================================================

# Kosten für Leibeigene kaufen (im echten Spiel: 50 Taler)
SERF_BUY_COST = 50

# =============================================================================
# STEUERSYSTEM (aus extra2/logic.xml)
# =============================================================================
# TaxAmount = 5 pro Worker pro Tick
# RegularTax = fester Betrag pro Worker (NICHT Multiplikator!)
# MotivationChange = Änderung der Motivation pro Tick
TAX_AMOUNT_PER_WORKER = 5  # Basis-Steuerbetrag pro Worker

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
BLESS_DURATION = 180  # Sekunden wie lange der Bonus hält (aus extra2!)
BLESS_MOTIVATION_BONUS = 0.3  # +30% Motivation (aus extra2!)
BLESS_REQUIRED_FAITH = 5000  # Benötigter Glaube pro Kategorie

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

# =============================================================================
# ALARM-MODUS (aus extra2/logic.xml)
# =============================================================================
# AlarmRechargeTime = 180000 ms (3 Minuten Cooldown)
# Worker gehen zu DefendableBuildings bei Alarm
ALARM_RECHARGE_TIME = 180  # Sekunden (3 Minuten)
ALARM_ACTIVE = False  # Standardmäßig aus

# Worker-Kapazität wird durch DORFZENTRUM bestimmt (VILLAGE_CENTER_CAPACITY)!

# =============================================================================
# KAPAZITÄTS-SYSTEM (aus XML-Analyse)
# =============================================================================

# DORFZENTRUM = Bestimmt maximale Anzahl Arbeiter/Bewohner!
# Dies ist das HARTE LIMIT für die Bevölkerung
VILLAGE_CENTER_CAPACITY = {
    "Dorfzentrum_1": 75,   # Level 1: max 75 Arbeiter
    "Dorfzentrum_2": 100,  # Level 2: max 100 Arbeiter
    "Dorfzentrum_3": 150,  # Level 3: max 150 Arbeiter
}

# Wohnhaus = NUR für RUHEN (WorkTime +50%)
# Begrenzt wie viele Arbeiter GLEICHZEITIG ruhen können
# Arbeiter können auch OHNE Wohnhaus existieren (dann nur Camp +10%)
RESIDENCE_CAPACITY = {
    "Wohnhaus_1": 6,   # Level 1: 6 können gleichzeitig ruhen
    "Wohnhaus_2": 9,   # Level 2: 9 können gleichzeitig ruhen
    "Wohnhaus_3": 12,  # Level 3: 12 können gleichzeitig ruhen
}

# Bauernhof = NUR für ESSEN (WorkTime +70%)
# Begrenzt wie viele Arbeiter GLEICHZEITIG essen können
# Arbeiter können auch OHNE Bauernhof existieren (dann nur Camp +10%)
FARM_EAT_CAPACITY = {
    "Bauernhof_1": 8,   # Level 1: 8 können gleichzeitig essen
    "Bauernhof_2": 10,  # Level 2: 10 können gleichzeitig essen
    "Bauernhof_3": 12,  # Level 3: 12 können gleichzeitig essen
}

# Bauernhof max Workers (Farmer die dort arbeiten)
FARM_WORKER_CAPACITY = {
    "Bauernhof_1": 1,
    "Bauernhof_2": 2,
    "Bauernhof_3": 3,
}

# Camper-Range für Pausen (5000 Einheiten im Spiel)
CAMPER_RANGE = 5000

# Worker-Typen zu Gebäude-Mapping
WORKER_BUILDING_MAP = {
    "miner": ["Steinmine", "Lehmmine", "Eisenmine", "Schwefelmine"],
    "sawmill_worker": ["Sägemühle"],
    "brickmaker": ["Lehmhütte"],  # Ziegelhütte - verarbeitet Lehm
    "stonecutter": ["Steinmetzhütte"],
    "smith": ["Schmiede"],
    "alchemist": ["Alchimistenhütte"],
    "farmer": ["Bauernhof"],
}


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


# =============================================================================
# ENVIRONMENT KLASSE - KOMPLETTE SIEDLER 5 SIMULATION
# =============================================================================

class SiedlerScharfschuetzenEnv(gym.Env):
    """
    Vollständige Siedler 5 Trainingsumgebung mit ALLEN Spielaktionen
    """

    metadata = {"render_modes": ["human", "ansi"]}

    def __init__(self, player_id: int = 1, render_mode: str = None):
        super().__init__()

        self.player_id = player_id
        self.render_mode = render_mode

        # Gebäude-Listen für Actions
        self.buildable_buildings = [b for b in buildings_db.keys() if get_building_level(b) == 1]
        self.upgradeable_buildings = [b for b in buildings_db.keys() if buildings_db[b].get("upgrade_to")]
        self.tech_list = list(technologies.keys())
        self.soldier_types = list(soldiers_db.keys())

        # Action Space berechnen
        self.n_build_actions = len(self.buildable_buildings)
        self.n_upgrade_actions = len(self.upgradeable_buildings)
        self.n_tech_actions = len(self.tech_list)
        self.n_recruit_actions = len(self.soldier_types)

        # =====================================================================
        # RESSOURCEN-ACTIONS (HYBRID: Bäume einzeln, Vorkommen/Minen kategorie-basiert)
        # =====================================================================

        # =================================================================
        # VEREINFACHTES BATCH-SYSTEM (ohne Serf-IDs)
        # Agent wählt: WAS (Kategorie) + WIEVIELE (1, 3, 5)
        # System wählt automatisch die beste Position
        # =================================================================

        # Batch-Größen für alle Ressourcen-Zuweisungen
        self.resource_batch_sizes = [1, 3, 5]

        # BÄUME: ZONEN-basierte Zuweisung für strategische Bauplatz-Schaffung
        # Jede Zone muss für bestimmte Raffinerie-Gebäude gerodet werden
        self.resource_trees = list(PLAYER_1_TREES_NEAREST)  # Fallback für generische Bäume
        self.wood_zone_names = list(WOOD_ZONES.keys())  # 6 Zonen: HQ_Bereich, Schwefelmine, Lehmmine, Steinmine, Dorfzentrum, Eisenmine

        # VORKOMMEN (Deposits): 4 Kategorien mit Batch
        # Serfs können hier sammeln SOLANGE keine Mine dort gebaut wurde
        self.deposit_category_names = ["Eisen", "Stein", "Lehm", "Schwefel"]

        # STOLLEN (Shafts): 4 Kategorien mit Batch - Serfs können IMMER hier sammeln
        # (XD_Iron1, XD_Stone1, etc. - 400 Ressourcen pro Stollen, keine Mine baubbar)
        self.shaft_category_names = ["Eisen", "Stein", "Lehm", "Schwefel"]

        # LEGACY: Mine-Kategorien (DEAKTIVIERT - Serfs arbeiten nicht an gebauten Minen!)
        self.mine_category_names = ["Eisenmine", "Steinmine", "Lehmmine", "Schwefelmine"]

        # Ressourcen-Actions:
        # - Holz-Zonen: 6 Zonen × 6 (assign/recall × batch) = 36 Actions
        # - Vorkommen: 4 × 6 (assign/recall × batch) = 24 Actions
        # - Stollen: 4 × 6 (assign/recall × batch) = 24 Actions
        # Total: 84 Actions (statt 54)
        n_batch = len(self.resource_batch_sizes)
        self.n_wood_zone_batch_actions = len(self.wood_zone_names) * n_batch * 2  # 36 (6 Zonen × 6)
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
        # BATCH-ACTIONS FÜR GEBÄUDE
        # Agent kann 1, 3, oder 5 Gebäude auf einmal bauen
        # =================================================================
        self.build_batch_sizes = [1, 3, 5]
        # Gebäude-Batch: 28 Gebäude × 3 Batch-Größen = 84 Actions
        # ERSETZT die alten n_build_actions (28)
        self.n_build_batch_actions = len(self.buildable_buildings) * len(self.build_batch_sizes)

        # NEUE ACTIONS:
        # Batch-Actions für Leibeigene: 1x, 3x, 5x kaufen + 1x, 3x, 5x entlassen
        self.serf_batch_sizes = [1, 3, 5]
        self.n_serf_actions = len(self.serf_batch_sizes) * 2  # 6 Actions (3 kaufen + 3 entlassen)

        # Batch-Actions für Scharfschützen-Rekrutierung: 3x, 5x (1x ist bereits in n_recruit_actions)
        # Für beide Scharfschützen-Typen: Scharfschützen (Level 1) und Scharfschützen_2 (Level 2)
        self.scharfschuetzen_batch_sizes = [3, 5]  # 1x ist bereits standard
        self.scharfschuetzen_types = ["Scharfschützen", "Scharfschützen_2"]
        self.n_batch_recruit_actions = len(self.scharfschuetzen_batch_sizes) * len(self.scharfschuetzen_types)  # 4 Actions

        self.n_demolish_actions = len(self.buildable_buildings)  # Jedes Gebäude kann abgerissen werden
        self.n_bless_actions = len(BLESS_CATEGORIES)  # 5 Segen-Kategorien (aus extra2)
        self.n_tax_actions = len(TAX_LEVELS)  # Steuerstufen (0-4)
        self.n_alarm_actions = 2  # Alarm AN / Alarm AUS

        # NEU: Bau-Serfs zuweisen/zurückrufen (1x, 3x, 5x für beide)
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

        self.action_space = gym.spaces.Discrete(self.total_actions)

        # Action Offsets (mit Batch-Build)
        self.offset_build_batch = 1  # Gebäude-Batch-Bau
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

        # Legacy-Kompatibilität (für alten Code der offset_build verwendet)
        self.offset_build = self.offset_build_batch
        self.offset_resource_pos = self.offset_resource_batch

        # Observation Space (ERWEITERT mit WorkTime-System)
        n_resource_obs = 6
        n_worker_obs = len(RESOURCE_MAP) + 2
        n_building_obs = len(self.buildable_buildings) * 2
        n_upgrade_obs = len(self.upgradeable_buildings)
        n_tech_obs = len(self.tech_list) * 2
        n_soldier_obs = len(self.soldier_types)
        n_time_obs = 2
        n_production_obs = 6

        # NEU: WorkTime-System Observations
        n_worktime_obs = 12  # avg_work_time, exhausted_ratio, eating, resting, working,
                             # walking, farm_capacity, farm_util, res_capacity, res_util,
                             # overall_efficiency, serf_count

        # NEU: Observations für neue Actions
        # tax_level, alarm_active, alarm_cooldown, faith
        # + 5x bless_cooldown (pro Kategorie) + 5x bless_active (pro Kategorie)
        n_new_action_obs = 4 + len(BLESS_CATEGORIES) * 2  # 4 + 10 = 14

        total_obs = (n_resource_obs + n_worker_obs + n_building_obs + n_upgrade_obs +
                    n_tech_obs + n_soldier_obs + n_time_obs + n_production_obs + n_worktime_obs +
                    n_new_action_obs)

        self.observation_space = gym.spaces.Box(
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
        import os
        import copy
        base_dir = r"c:\Users\marku\OneDrive\Desktop\siedler_ai"
        walkable_file = os.path.join(base_dir, "player1_walkable.npy")
        resources_file = os.path.join(base_dir, "player1_resources.json")

        self._cached_walkable = np.load(walkable_file)
        with open(resources_file, 'r') as f:
            self._cached_resources = json.load(f)

        # PERFORMANCE: Vollständigen MapManager mit Bäumen einmal aufbauen und cachen
        self._cached_map_manager = MapManager()
        self._cached_map_manager.grid.load_terrain_from_array(self._cached_walkable)
        cached_trees = self._cached_resources.get('trees_all', self._cached_resources.get('trees_nearest_50', []))
        self._cached_map_manager._load_trees_from_data(cached_trees)

        # Cache die Grid-Arrays für schnelles Reset
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
        print(f"Bäume geladen: {len(cached_trees)} (gecached)")

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.resources = dict(START_RESOURCES)
        self.total_leibeigene = 30
        # Worker-Kapazität wird durch Wohnhäuser bestimmt, nicht HQ
        self.free_leibeigene = self.total_leibeigene
        self.resource_workers = {r: 0 for r in RESOURCE_MAP}

        self.buildings = {b: 0 for b in buildings_db.keys()}
        self.buildings["Hauptquartier_1"] = 1

        self.construction_queue = []  # Legacy: [(building, remaining_time, position)]
        self.upgrade_queue = []
        self.current_research = None
        self.recruit_queue = []

        # NEU: Realistisches Bau-System mit Leibeigenen-Zuweisung
        # Format: [{
        #   "building": str,           # Gebäude-Name
        #   "position": (x, y),        # Bauplatz-Position
        #   "total_time": float,       # Basis-Bauzeit
        #   "remaining_work": float,   # Verbleibende Arbeit
        #   "serfs_assigned": int,     # Anzahl zugewiesener Leibeigener
        #   "site_id": int,            # Eindeutige ID
        # }]
        self.construction_sites = []
        self.next_site_id = 0

        # Serf-Tracking (vereinfacht - keine IDs mehr nötig)

        self.researched_techs = set()
        self.soldiers = {s: 0 for s in self.soldier_types}
        self.scharfschuetzen = 0

        self.current_time = 0
        self.max_time = TOTAL_SIM_TIME

        self.available_positions = list(self.building_zones["zone_a_immediate"])
        self.used_positions = []
        self.building_position_map = {}

        self.built_mines = {"Steinmine": [], "Eisenmine": [], "Lehmmine": [], "Schwefelmine": []}
        self.action_history = []

        # =================================================================
        # RESSOURCEN-VERFÜGBARKEIT (für korrektes Action Masking)
        # =================================================================
        # Kleine Vorkommen: erschöpfbar, Leibeigene sammeln direkt
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

        # Bäume: für Holz
        # ResourceAmount: 75 pro Baum, Amount: 2 pro Extraktion = 37 Extraktionen pro Baum!
        self.available_trees = PLAYER_1_TREES_SUMMARY.get("total_trees", 888)
        self.trees_list = list(PLAYER_1_TREES_NEAREST)  # Kopie der nächsten Bäume

        # =================================================================
        # VEREINFACHTES RESSOURCEN-TRACKING (ohne Serf-IDs!)
        # Agent wählt Kategorie + Batch-Größe, System verwaltet Details
        # =================================================================

        # HOLZ-ZONEN: Strategische Zonen für Bauplatz-Schaffung
        self.wood_serfs = 0  # Anzahl Serfs die aktuell Holz sammeln (gesamt)
        self.wood_zone_categories = {}
        for zone_name, zone_data in WOOD_ZONES.items():
            self.wood_zone_categories[zone_name] = {
                "center": zone_data["center"],
                "radius": zone_data["radius"],
                "raffinerie": zone_data.get("raffinerie", ""),
                "trees": [
                    {"x": t["x"], "y": t["y"], "dist": t["dist"],
                     "resource_remaining": 75, "serfs_assigned": 0}
                    for t in zone_data.get("trees", [])
                ],
                "serfs_assigned": 0,
                "total_trees": zone_data.get("tree_count", 0),
            }

        # Legacy: Alte tree_list_internal für Kompatibilität (alle Bäume flach)
        self.tree_list_internal = []
        for zone_name, zone_cat in self.wood_zone_categories.items():
            for tree in zone_cat["trees"]:
                self.tree_list_internal.append({
                    "x": tree["x"], "y": tree["y"],
                    "resource_remaining": tree["resource_remaining"],
                    "serfs_assigned": tree["serfs_assigned"],
                    "zone": zone_name  # Zusätzliches Feld für Zonen-Tracking
                })
        self.available_tree_count = len(self.tree_list_internal)

        # VORKOMMEN: Zähler pro Kategorie (keine IDs!)
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

        # STOLLEN (Shafts): Wo Serfs IMMER sammeln können (XD_Iron1, XD_Stone1, etc.)
        # Diese haben 400 Ressourcen pro Stollen und können NICHT bebaut werden.
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

        # LEGACY: mine_categories für Kompatibilität (DEAKTIVIERT - Serfs arbeiten nicht an Minen!)
        # Gebaute Minen werden von Workern (PU_Miner) betrieben.
        self.mine_categories = {
            "Eisenmine": {"serfs_assigned": 0, "mines_built": 0, "max_serfs_per_mine": 0},
            "Steinmine": {"serfs_assigned": 0, "mines_built": 0, "max_serfs_per_mine": 0},
            "Lehmmine": {"serfs_assigned": 0, "mines_built": 0, "max_serfs_per_mine": 0},
            "Schwefelmine": {"serfs_assigned": 0, "mines_built": 0, "max_serfs_per_mine": 0},
        }

        # Legacy-Kompatibilität: resource_workers nicht mehr verwendet für Zuweisung
        # aber noch für Berechnung der Produktionsraten
        self.resource_workers = {r: 0 for r in RESOURCE_MAP}

        # Minenschächte: wo Minen-Gebäude gebaut werden KÖNNEN
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

        # HQ als erstes Gebäude im Grid blockieren
        self.map_manager.add_building(self.hq_position[0], self.hq_position[1], "Hauptquartier")

        # PERFORMANCE: Tree-ID Mapping aus Cache (nicht neu berechnen!)
        self.tree_id_mapping = dict(self._cached_tree_id_mapping)

        # Initiale Serfs erstellen (30 Leibeigene zu Start)
        # VEREINFACHT: Keine IDs mehr, nur Zähler
        from worker_simulation import Position
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

        # NEU: Glaube (Faith) für Segnen
        self.faith = 0  # Startwert

        # NEU: Alarm-Modus
        self.alarm_active = False
        self.alarm_cooldown = 0  # Zeit bis Alarm wieder möglich

        # NEU: Motivation (beeinflusst WorkTime-Regeneration)
        # Aus extra2: MotivationGameStartMaxMotivation = 1.0, MotivationAbsoluteMaxMotivation = 3.0
        self.base_motivation = 1.0  # 1.0 = 100% normal

        return self._get_observation(), {}

    def _get_observation(self):
        obs = []

        for r in RESOURCE_NAMES:
            obs.append(self.resources.get(r, 0) / 1000.0)

        for r in RESOURCE_MAP:
            obs.append(self.resource_workers.get(r, 0) / 50.0)
        obs.append(self.free_leibeigene / 100.0)
        obs.append(self.total_leibeigene / 100.0)

        for b in self.buildable_buildings:
            obs.append(self.buildings.get(b, 0) / 10.0)
            in_construction = sum(1 for c in self.construction_queue if c[0] == b)
            obs.append(in_construction / 5.0)

        for b in self.upgradeable_buildings:
            obs.append(self.buildings.get(b, 0) / 5.0)

        for t in self.tech_list:
            obs.append(1.0 if t in self.researched_techs else 0.0)
            obs.append(1.0 if self.current_research and self.current_research[0] == t else 0.0)

        for s in self.soldier_types:
            obs.append(self.soldiers.get(s, 0) / 50.0)

        obs.append(self.current_time / self.max_time)
        obs.append((self.max_time - self.current_time) / self.max_time)

        for r in RESOURCE_MAP:
            obs.append(self._get_production_rate(r) / 10.0)
        obs.append(self._get_taler_income() / 100.0)

        # NEU: WorkTime-System Observations
        workforce_stats = self.workforce_manager.get_stats()
        obs.append(workforce_stats.get("avg_work_time", 100) / 400.0)  # Max WorkTime ist 400
        obs.append(workforce_stats.get("exhausted_ratio", 0))
        obs.append(workforce_stats.get("eating_workers", 0) / 50.0)
        obs.append(workforce_stats.get("resting_workers", 0) / 50.0)
        obs.append(workforce_stats.get("working_workers", 0) / 50.0)
        obs.append(workforce_stats.get("walking_workers", 0) / 50.0)

        # Kapazitäts-Stats
        total_farm_capacity = self._get_total_farm_capacity()
        total_residence_capacity = self._get_total_residence_capacity()
        obs.append(total_farm_capacity / 50.0)
        obs.append(len(self.workforce_manager.workers) / max(1, total_farm_capacity))  # Farm-Auslastung
        obs.append(total_residence_capacity / 50.0)
        obs.append(len(self.workforce_manager.workers) / max(1, total_residence_capacity))  # Wohnhaus-Auslastung

        # Effizienz und Serf-Count
        obs.append(self.workforce_manager.get_average_efficiency())
        obs.append(len(self.production_system.serfs) / 100.0)

        # NEU: Observations für neue Actions (erweitert für 5 Kategorien + Alarm)
        obs.append(self.current_tax_level / 4.0)  # Normalisiert auf 0-1
        obs.append(1.0 if self.alarm_active else 0.0)  # Alarm aktiv?
        obs.append(self.alarm_cooldown / ALARM_RECHARGE_TIME)  # Alarm-Cooldown
        obs.append(self.faith / BLESS_REQUIRED_FAITH)  # Faith normalisiert

        # Segen pro Kategorie (5x Cooldown + 5x aktiv)
        for cat in BLESS_CATEGORIES:
            obs.append(self.bless_cooldowns.get(cat, 0) / BLESS_COOLDOWN)
        for cat in BLESS_CATEGORIES:
            obs.append(1.0 if self.bless_active_times.get(cat, 0) > 0 else 0.0)

        return np.array(obs, dtype=np.float32)

    def _get_production_rate(self, resource):
        rate = 0.0
        workers = self.resource_workers.get(resource, 0)
        if workers > 0:
            rate += workers * gather_rates.get(resource, 0.5)
        for b_name, count in self.buildings.items():
            if count > 0:
                output = buildings_db.get(b_name, {}).get("resource_output", {})
                if resource in output:
                    rate += output[resource] * count
        return rate

    def _get_total_motivation(self) -> float:
        """Berechnet die Gesamtmotivation basierend auf Kloster und Segnung.

        Aus extra2/logic.xml:
        - MotivationThresholdHappy = 1.5 (sehr glücklich)
        - MotivationThresholdSad = 1.0 (traurig)
        - MotivationThresholdAngry = 0.7 (wütend)
        - MotivationThresholdLeave = 0.25 (verlässt Settlement!)
        - MotivationAbsoluteMaxMotivation = 3.0
        """
        motivation = self.base_motivation

        # NEU: Kloster-Motivation-Effekt (aus buildings_db)
        # Jedes Kloster erhöht dauerhaft die Motivation
        motivation += self.buildings.get("Kloster_1", 0) * 0.08
        motivation += self.buildings.get("Kloster_2", 0) * 0.10
        motivation += self.buildings.get("Kloster_3", 0) * 0.15

        # Segnungs-Bonus (pro aktive Kategorie)
        # BlessingBonus = 0.3 (+30% Motivation)
        for cat in BLESS_CATEGORIES:
            if self.bless_active_times.get(cat, 0) > 0:
                motivation += BLESS_MOTIVATION_BONUS

        # Clamp auf gültige Werte
        return max(0.25, min(3.0, motivation))

    def _get_scholar_efficiency(self) -> float:
        """Berechnet die durchschnittliche Effizienz aller Gelehrten.

        Gelehrte mit niedriger WorkTime arbeiten langsamer (nur 10% bei Erschöpfung).
        Returns: 0.1 (alle erschöpft) bis 1.0 (alle fit)
        """
        scholars = [w for w in self.workforce_manager.workers
                    if w.worker_type == "scholar"]
        if not scholars:
            # Keine Gelehrten = volle Geschwindigkeit (Fallback)
            return 1.0
        total_efficiency = sum(w.get_efficiency() for w in scholars)
        return total_efficiency / len(scholars)

    def _can_buy_serf(self) -> bool:
        """Prüft ob ein Leibeigener gekauft werden kann."""
        return self._can_buy_serf_batch(1)

    def _can_buy_serf_batch(self, count: int) -> bool:
        """Prüft ob mehrere Leibeigene gekauft werden können."""
        # Genug Taler für alle?
        if self.resources.get(RESOURCE_TALER, 0) < SERF_BUY_COST * count:
            return False
        # Population-Limit erlaubt alle?
        village_capacity = self._get_total_village_capacity()
        if self.total_leibeigene + count > village_capacity:
            return False
        # Max Leibeigene nicht überschritten?
        if self.total_leibeigene + count > MAX_POSSIBLE_LEIBEIGENE:
            return False
        return True

    def _can_dismiss_serf(self) -> bool:
        """Prüft ob ein Leibeigener entlassen werden kann."""
        return self._can_dismiss_serf_batch(1)

    def _can_dismiss_serf_batch(self, count: int) -> bool:
        """Prüft ob mehrere Leibeigene entlassen werden können."""
        return self.free_leibeigene >= count

    def _can_demolish(self, building: str) -> bool:
        """Prüft ob ein Gebäude abgerissen werden kann."""
        # Gebäude muss existieren
        if self.buildings.get(building, 0) < 1:
            return False
        # HQ kann nicht abgerissen werden
        if "Hauptquartier" in building:
            return False
        return True

    def _can_bless(self, category: int = None) -> bool:
        """Prüft ob Segnung möglich ist.

        Args:
            category: Segen-Kategorie (0-4). Wenn None, prüft allgemein.
        """
        # Kloster (Monastery) muss gebaut sein (nicht Kapelle!)
        total_monasteries = (self.buildings.get("Kloster_1", 0) +
                            self.buildings.get("Kloster_2", 0) +
                            self.buildings.get("Kloster_3", 0))
        if total_monasteries < 1:
            return False

        # Faith muss ausreichen
        if self.faith < BLESS_REQUIRED_FAITH:
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

    def _get_total_village_capacity(self) -> int:
        """Berechnet die maximale Arbeiter-Kapazität aller Dorfzentren.
        Dies ist das HARTE LIMIT für die Bevölkerung!"""
        total = 0
        for vc_type, capacity in VILLAGE_CENTER_CAPACITY.items():
            total += self.buildings.get(vc_type, 0) * capacity
        return total

    def _get_total_farm_capacity(self) -> int:
        """Berechnet wie viele Arbeiter GLEICHZEITIG essen können.
        NUR für WorkTime-Regeneration, NICHT für Bevölkerungs-Limit!"""
        total = 0
        for farm_type, capacity in FARM_EAT_CAPACITY.items():
            total += self.buildings.get(farm_type, 0) * capacity
        return total

    def _get_total_residence_capacity(self) -> int:
        """Berechnet wie viele Arbeiter GLEICHZEITIG ruhen können.
        NUR für WorkTime-Regeneration, NICHT für Bevölkerungs-Limit!"""
        total = 0
        for res_type, capacity in RESIDENCE_CAPACITY.items():
            total += self.buildings.get(res_type, 0) * capacity
        return total

    def _sync_workforce_infrastructure(self):
        """Synchronisiert Farms/Residences/Camps mit dem WorkforceManager"""
        from worker_simulation import Position

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

        # DORFZENTRUM-KAPAZITÄT setzen (bestimmt max. Arbeiter!)
        village_capacity = self._get_total_village_capacity()
        self.workforce_manager.set_village_capacity(village_capacity)

        # Farms synchronisieren (für Essen/WorkTime-Regeneration)
        self.workforce_manager.farms.clear()
        for farm_type in FARM_EAT_CAPACITY.keys():
            count = self.buildings.get(farm_type, 0)
            level = get_building_level(farm_type)
            for i in range(count):
                pos_key = f"{farm_type}_{i}"
                raw_pos = self.building_position_map.get(pos_key, self.hq_position)
                pos_obj = to_position(raw_pos)
                farm = Farm(position=pos_obj, level=level)
                self.workforce_manager.farms.append(farm)

        # Residences synchronisieren
        self.workforce_manager.residences.clear()
        for res_type in RESIDENCE_CAPACITY.keys():
            count = self.buildings.get(res_type, 0)
            level = get_building_level(res_type)
            for i in range(count):
                pos_key = f"{res_type}_{i}"
                raw_pos = self.building_position_map.get(pos_key, self.hq_position)
                pos_obj = to_position(raw_pos)
                residence = Residence(position=pos_obj, level=level)
                self.workforce_manager.residences.append(residence)

        # Ein Camp beim HQ (Fallback wenn keine Farm/Residence in Reichweite)
        if not self.workforce_manager.camps:
            hq_pos = to_position(self.hq_position)
            self.workforce_manager.camps.append(Camp(position=hq_pos))

    def get_action_mask(self):
        mask = np.zeros(self.total_actions, dtype=np.int8)
        mask[0] = 1  # Wait immer möglich

        # =================================================================
        # GEBÄUDE-BATCH-BAU (1x, 3x, 5x pro Gebäude)
        # =================================================================
        for i, building in enumerate(self.buildable_buildings):
            for j, batch_size in enumerate(self.build_batch_sizes):
                action_idx = self.offset_build_batch + i * len(self.build_batch_sizes) + j
                if self._can_build_batch(building, batch_size):
                    mask[action_idx] = 1

        # Upgrades (unverändert)
        for i, building in enumerate(self.upgradeable_buildings):
            if self._can_upgrade(building):
                mask[self.offset_upgrade + i] = 1

        # Technologien (unverändert)
        for i, tech in enumerate(self.tech_list):
            if self._can_research(tech):
                mask[self.offset_tech + i] = 1

        # Soldaten (unverändert)
        for i, soldier in enumerate(self.soldier_types):
            if self._can_recruit(soldier):
                mask[self.offset_recruit + i] = 1

        # =================================================================
        # RESSOURCEN-BATCH-ACTIONS (1x, 3x, 5x)
        # =================================================================
        n_batch = len(self.resource_batch_sizes)
        offset = self.offset_resource_batch

        # Holz-Zonen: Zuweisen und Entfernen (6 Zonen × 3 Batch × 2)
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

        # Batch-Rekrutierung für Scharfschützen (3x, 5x)
        action_idx = 0
        for soldier_type in self.scharfschuetzen_types:
            for batch_size in self.scharfschuetzen_batch_sizes:
                if self._can_recruit_batch(soldier_type, batch_size):
                    mask[self.offset_batch_recruit + action_idx] = 1
                action_idx += 1

        # Gebäude abreißen
        for i, building in enumerate(self.buildable_buildings):
            if self._can_demolish(building):
                mask[self.offset_demolish + i] = 1

        # Segnen (5 Kategorien)
        for cat in BLESS_CATEGORIES:
            if self._can_bless(cat):
                mask[self.offset_bless + cat] = 1

        # Steuern (immer möglich, außer aktuelles Level)
        for i in range(len(TAX_LEVELS)):
            if i != self.current_tax_level:
                mask[self.offset_tax + i] = 1

        # Alarm (AN wenn aus und kein Cooldown, AUS wenn an)
        if not self.alarm_active and self.alarm_cooldown <= 0:
            mask[self.offset_alarm] = 1
        if self.alarm_active:
            mask[self.offset_alarm + 1] = 1

        # NEU: Bau-Serfs zuweisen/zurückrufen
        for i, batch_size in enumerate(self.build_serf_batch_sizes):
            # Zuweisen möglich wenn freie Serfs und Baustellen vorhanden
            if self._can_assign_build_batch(batch_size):
                mask[self.offset_build_serf + i] = 1
            # Zurückrufen möglich wenn Serfs auf Baustellen arbeiten
            if self._can_recall_build_batch(batch_size):
                mask[self.offset_build_serf + len(self.build_serf_batch_sizes) + i] = 1

        return mask

    def _can_build(self, building):
        b_info = buildings_db.get(building)
        if not b_info:
            return False

        for resource, amount in b_info["cost"].items():
            if self.resources.get(resource, 0) < amount:
                return False

        tech_req = b_info.get("tech_required")
        if tech_req and tech_req not in self.researched_techs:
            return False

        if b_info.get("mine_type"):
            mine_type = b_info["mine_type"]
            available = self.mine_positions.get(mine_type, [])
            built = len(self.built_mines.get(mine_type, []))
            if built >= len(available):
                return False
        else:
            if len(self.available_positions) == 0:
                return False

        return True

    def _can_build_batch(self, building: str, batch_size: int) -> bool:
        """Prüft ob batch_size Gebäude gebaut werden können."""
        b_info = buildings_db.get(building)
        if not b_info:
            return False

        # Ressourcen für alle Gebäude prüfen
        for resource, amount in b_info["cost"].items():
            if self.resources.get(resource, 0) < amount * batch_size:
                return False

        # Tech-Voraussetzung prüfen
        tech_req = b_info.get("tech_required")
        if tech_req and tech_req not in self.researched_techs:
            return False

        # Positionen prüfen
        if b_info.get("mine_type"):
            mine_type = b_info["mine_type"]
            available = self.mine_positions.get(mine_type, [])
            built = len(self.built_mines.get(mine_type, []))
            if built + batch_size > len(available):
                return False
        else:
            if len(self.available_positions) < batch_size:
                return False

        return True

    def _can_upgrade(self, building):
        if self.buildings.get(building, 0) < 1:
            return False

        b_info = buildings_db.get(building)
        if not b_info or not b_info.get("upgrade_to"):
            return False

        for resource, amount in b_info.get("upgrade_cost", {}).items():
            if self.resources.get(resource, 0) < amount:
                return False

        return True

    def _can_research(self, tech):
        if tech in self.researched_techs:
            return False
        if self.current_research:
            return False

        tech_info = technologies.get(tech)
        if not tech_info:
            return False

        for resource, amount in tech_info["cost"].items():
            if self.resources.get(resource, 0) < amount:
                return False

        for req_tech in tech_info.get("tech_required", []):
            if req_tech not in self.researched_techs:
                return False

        req_building = tech_info.get("requires_building")
        if req_building and self.buildings.get(req_building, 0) < 1:
            return False

        if self.buildings.get("Hochschule_1", 0) + self.buildings.get("Hochschule_2", 0) < 1:
            return False

        return True

    def _can_recruit(self, soldier):
        s_info = soldiers_db.get(soldier)
        if not s_info:
            return False

        for resource, amount in s_info["cost"].items():
            if self.resources.get(resource, 0) < amount:
                return False

        for req in s_info.get("requirements", []):
            if req in buildings_db:
                if self.buildings.get(req, 0) < 1:
                    return False
            elif req in technologies:
                if req not in self.researched_techs:
                    return False

        unit_rules = GAME_RULES.get("units", {})
        base_name = get_base_building_name(soldier)
        if base_name in unit_rules and unit_rules[base_name] == 0:
            return False

        return True

    def _can_recruit_batch(self, soldier: str, count: int) -> bool:
        """Prüft ob mehrere Soldaten gleichzeitig rekrutiert werden können."""
        s_info = soldiers_db.get(soldier)
        if not s_info:
            return False

        # Genug Ressourcen für alle?
        for resource, amount in s_info["cost"].items():
            if self.resources.get(resource, 0) < amount * count:
                return False

        # Requirements erfüllt?
        for req in s_info.get("requirements", []):
            if req in buildings_db:
                if self.buildings.get(req, 0) < 1:
                    return False
            elif req in technologies:
                if req not in self.researched_techs:
                    return False

        # Unit Rules prüfen
        unit_rules = GAME_RULES.get("units", {})
        base_name = get_base_building_name(soldier)
        if base_name in unit_rules and unit_rules[base_name] == 0:
            return False

        return True

    def _can_assign_worker_to_resource(self, resource: str) -> bool:
        """
        Prüft ob ein Leibeigener einer Ressource zugewiesen werden kann.

        Regeln:
        - Ressource muss INNERHALB des ResourceSearchRadius (4500) liegen!
        - Holz: Bäume müssen verfügbar sein
        - Minen-Ressourcen (Stein, Lehm, Eisen, Schwefel):
          ENTWEDER eine Mine ist gebaut ODER kleine Vorkommen sind verfügbar

        Returns:
            True wenn Ressource gesammelt werden kann
        """
        # NEU: Prüfe ob _get_resource_collection_position eine Position findet
        # Diese Methode berücksichtigt bereits den ResourceSearchRadius!
        target_pos = self._get_resource_collection_position(resource)
        return target_pos is not None

    def _get_resource_collection_position(self, resource: str):
        """
        Gibt die beste Position für Ressourcensammlung zurück.

        Priorität:
        1. Gebaute Mine (unbegrenzte Kapazität)
        2. Kleine Vorkommen (bis erschöpft)
        3. Bäume (für Holz)

        NEU: Berücksichtigt ResourceSearchRadius (4500) aus PU_Serf.xml
        Serfs suchen nur Ressourcen innerhalb dieses Radius!

        Returns:
            Position oder None
        """
        from worker_simulation import Position
        from production_system import SERF_RESOURCE_SEARCH_RADIUS
        import math

        # HQ als Referenzpunkt für Distanz-Berechnung
        hq_x, hq_y = self.hq_position

        def is_in_search_radius(x, y) -> bool:
            """Prüft ob Position innerhalb des Serf-Suchradius liegt."""
            dist = math.sqrt((x - hq_x)**2 + (y - hq_y)**2)
            return dist <= SERF_RESOURCE_SEARCH_RADIUS

        if resource == RESOURCE_HOLZ:
            # Nächster verfügbarer Baum INNERHALB des Suchradius
            for tree in self.trees_list:
                if is_in_search_radius(tree["x"], tree["y"]):
                    return Position(x=tree["x"], y=tree["y"])
            return None

        mine_type_map = {
            RESOURCE_STEIN: "Steinmine",
            RESOURCE_LEHM: "Lehmmine",
            RESOURCE_EISEN: "Eisenmine",
            RESOURCE_SCHWEFEL: "Schwefelmine",
        }

        mine_type = mine_type_map.get(resource)

        # Priorität 1: Gebaute Mine (innerhalb Suchradius)
        built = self.built_mines.get(mine_type, [])
        for pos in built:
            if is_in_search_radius(pos["x"], pos["y"]):
                return Position(x=pos["x"], y=pos["y"])

        # Priorität 2: Kleine Vorkommen (innerhalb Suchradius)
        deposits = self.small_deposits.get(resource, [])
        for deposit in deposits:
            if deposit.get("remaining", 0) > 0:
                if is_in_search_radius(deposit["x"], deposit["y"]):
                    return Position(x=deposit["x"], y=deposit["y"])

        return None

    def _assign_serf_to_resource(self, resource: str):
        """
        Weist einen freien Serf einer Ressource zu.
        Der Serf läuft zur Ressource und bleibt dort.

        NEU: Verwendet A* Pfadfindung für exakte Laufwege!
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
            RESOURCE_HOLZ: ResourceType.WOOD,
            RESOURCE_STEIN: ResourceType.STONE,
            RESOURCE_LEHM: ResourceType.CLAY,
            RESOURCE_EISEN: ResourceType.IRON,
            RESOURCE_SCHWEFEL: ResourceType.SULFUR,
        }
        resource_type = resource_type_map.get(resource)
        if not resource_type:
            return

        # Hole Position der Ressource und ggf. tree_id
        tree_id = None
        if resource == RESOURCE_HOLZ:
            # Holz: Baum aus Liste nehmen und reservieren
            if not self.trees_list:
                return
            tree = self.trees_list.pop(0)  # Ersten Baum nehmen und entfernen
            self.available_trees -= 1
            target_pos = Position(x=tree["x"], y=tree["y"])

            # Tree-ID für MapManager ermitteln
            nearest = self.map_manager.get_nearest_tree(tree["x"], tree["y"])
            if nearest:
                tree_id = nearest[0]
        else:
            target_pos = self._get_resource_collection_position(resource)
            if not target_pos:
                return

        # HQ Position als Startpunkt
        hq_pos = Position(x=self.hq_position[0], y=self.hq_position[1])

        # NEU: A* Pfadfindung für exakte Distanz
        path_result = self.map_manager.find_path(
            (hq_pos.x, hq_pos.y),
            (target_pos.x, target_pos.y)
        )

        # Berechne echte Laufdistanz (A* Pfad statt Luftlinie)
        if path_result.found:
            real_distance = path_result.world_distance
        else:
            # Fallback auf Luftlinie wenn kein Pfad gefunden
            import math
            real_distance = math.sqrt(
                (target_pos.x - hq_pos.x)**2 + (target_pos.y - hq_pos.y)**2
            )

        # Serf zur Ressource schicken mit korrekter Distanz und tree_id
        idle_serf.assign_to_resource(resource_type, target_pos, hq_pos, real_distance, tree_id)

    def _recall_serf_from_resource(self, resource: str):
        """
        Ruft einen Serf von einer Ressource zurück.
        Der Serf wird auf IDLE gesetzt.
        (Legacy-Funktion - nicht mehr direkt verwendet)
        """
        from production_system import ResourceType

        # Konvertiere Ressourcen-Name zu ResourceType
        resource_type_map = {
            RESOURCE_HOLZ: ResourceType.WOOD,
            RESOURCE_STEIN: ResourceType.STONE,
            RESOURCE_LEHM: ResourceType.CLAY,
            RESOURCE_EISEN: ResourceType.IRON,
            RESOURCE_SCHWEFEL: ResourceType.SULFUR,
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
    # Agent wählt: WAS + WIEVIELE (1, 3, 5)
    # =================================================================

    # --- HOLZ (Bäume) ---
    def _can_assign_wood_batch(self, batch_size: int) -> bool:
        """Prüft ob batch_size Serfs zu Bäumen zugewiesen werden können."""
        if self.free_leibeigene < batch_size:
            return False
        # Mindestens batch_size Bäume mit Ressourcen verfügbar
        available = sum(1 for t in self.tree_list_internal if t["resource_remaining"] > 0)
        return available > 0  # Mindestens 1 Baum muss verfügbar sein

    def _can_recall_wood_batch(self, batch_size: int) -> bool:
        """Prüft ob batch_size Serfs von Holz-Arbeit zurückgerufen werden können."""
        return self.wood_serfs >= batch_size

    def _assign_wood_batch(self, batch_size: int):
        """Weist batch_size Serfs zum Holzsammeln zu."""
        assigned = 0
        for serf in self.production_system.serfs:
            if assigned >= batch_size:
                break
            if serf.is_idle():
                # Finde nächsten verfügbaren Baum
                for tree in self.tree_list_internal:
                    if tree["resource_remaining"] > 0:
                        # Serf zuweisen (vereinfacht, ohne ID-Tracking)
                        from worker_simulation import Position
                        from production_system import ResourceType
                        target_pos = Position(x=tree["x"], y=tree["y"])
                        hq_pos = Position(x=self.hq_position[0], y=self.hq_position[1])
                        serf.assign_to_resource(ResourceType.WOOD, target_pos, hq_pos, None)
                        serf.work_location = "wood"  # Markiere als Holz-Serf
                        tree["serfs_assigned"] += 1
                        assigned += 1
                        break

        self.wood_serfs += assigned
        self.free_leibeigene -= assigned
        self.resource_workers[RESOURCE_HOLZ] = self.resource_workers.get(RESOURCE_HOLZ, 0) + assigned

    def _recall_wood_batch(self, batch_size: int):
        """Ruft batch_size Serfs vom Holzsammeln zurück."""
        recalled = 0
        for serf in self.production_system.serfs:
            if recalled >= batch_size:
                break
            # Konsistenz: Prüfe auch work_location
            if (serf.target_resource and
                serf.target_resource.value == "wood" and
                serf.work_location == "wood"):
                serf.stop()
                recalled += 1

        self.wood_serfs = max(0, self.wood_serfs - recalled)
        self.free_leibeigene += recalled
        self.resource_workers[RESOURCE_HOLZ] = max(0, self.resource_workers.get(RESOURCE_HOLZ, 0) - recalled)

    # --- HOLZ-ZONEN (strategische Bauplatz-Schaffung) ---
    def _can_assign_wood_zone_batch(self, zone_name: str, batch_size: int) -> bool:
        """
        Prüft ob batch_size Serfs zu einer Holz-Zone zugewiesen werden können.
        Jede Zone muss für bestimmte Raffinerie-Gebäude gerodet werden.
        """
        if zone_name not in self.wood_zone_categories:
            return False
        if self.free_leibeigene < batch_size:
            return False
        # Mindestens 1 Baum mit Ressourcen in dieser Zone
        zone_data = self.wood_zone_categories[zone_name]
        return any(t["resource_remaining"] > 0 for t in zone_data["trees"])

    def _can_recall_wood_zone_batch(self, zone_name: str, batch_size: int) -> bool:
        """Prüft ob batch_size Serfs von einer Holz-Zone zurückgerufen werden können."""
        if zone_name not in self.wood_zone_categories:
            return False
        return self.wood_zone_categories[zone_name]["serfs_assigned"] >= batch_size

    def _assign_wood_zone_batch(self, zone_name: str, batch_size: int):
        """
        Weist batch_size Serfs zu einer spezifischen Holz-Zone zu.
        Serfs werden zu den nächsten Bäumen in der Zone geschickt (deterministic).
        """
        from worker_simulation import Position
        from production_system import ResourceType

        zone_data = self.wood_zone_categories.get(zone_name)
        if not zone_data:
            return

        # Finde verfügbare Bäume, sortiert nach Distanz zum Zonenzentrum (nächste zuerst)
        available_trees = [t for t in zone_data["trees"] if t["resource_remaining"] > 0]
        available_trees.sort(key=lambda t: t["dist"])

        if not available_trees:
            return

        assigned = 0
        tree_idx = 0
        for serf in self.production_system.serfs:
            if assigned >= batch_size:
                break
            if serf.is_idle():
                # Verteile Serfs auf verschiedene Bäume (spread)
                tree = available_trees[tree_idx % len(available_trees)]
                target_pos = Position(x=tree["x"], y=tree["y"])
                hq_pos = Position(x=self.hq_position[0], y=self.hq_position[1])
                serf.assign_to_resource(ResourceType.WOOD, target_pos, hq_pos, None)
                serf.work_location = f"wood_zone_{zone_name}"  # Zone-spezifisch
                tree["serfs_assigned"] += 1
                assigned += 1
                tree_idx += 1

        zone_data["serfs_assigned"] += assigned
        self.wood_serfs += assigned
        self.free_leibeigene -= assigned
        self.resource_workers[RESOURCE_HOLZ] = self.resource_workers.get(RESOURCE_HOLZ, 0) + assigned

    def _recall_wood_zone_batch(self, zone_name: str, batch_size: int):
        """Ruft batch_size Serfs von einer spezifischen Holz-Zone zurück."""
        zone_data = self.wood_zone_categories.get(zone_name)
        if not zone_data:
            return

        work_location = f"wood_zone_{zone_name}"
        recalled = 0
        for serf in self.production_system.serfs:
            if recalled >= batch_size:
                break
            if (serf.target_resource and
                serf.target_resource.value == "wood" and
                serf.work_location == work_location):
                serf.stop()
                recalled += 1

        zone_data["serfs_assigned"] = max(0, zone_data["serfs_assigned"] - recalled)
        self.wood_serfs = max(0, self.wood_serfs - recalled)
        self.free_leibeigene += recalled
        self.resource_workers[RESOURCE_HOLZ] = max(0, self.resource_workers.get(RESOURCE_HOLZ, 0) - recalled)

    def _auto_reassign_wood_serfs(self, from_x: float, from_y: float, num_serfs: int) -> int:
        """
        Automatisches Weitersammeln: Suche nächsten Baum im SERF_SEARCH_RADIUS.
        Wie im echten Spiel (PU_Serf.xml: ResourceSearchRadius = 4500).

        Returns: Anzahl erfolgreich zugewiesener Serfs
        """
        import math
        reassigned = 0

        # Finde alle Bäume im Suchradius, sortiert nach Distanz
        trees_in_radius = []
        for i, tree in enumerate(self.tree_list_internal):
            if tree["resource_remaining"] > 0:
                dx = tree["x"] - from_x
                dy = tree["y"] - from_y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance <= SERF_SEARCH_RADIUS:
                    trees_in_radius.append((distance, i, tree))

        # Sortiere nach Distanz (nächster zuerst)
        trees_in_radius.sort(key=lambda x: x[0])

        # Weise Serfs den nächsten Bäumen zu
        for _, tree_idx, tree in trees_in_radius:
            if reassigned >= num_serfs:
                break
            # Finde einen arbeitenden Serf der umgeleitet werden kann
            for serf in self.production_system.serfs:
                if reassigned >= num_serfs:
                    break
                if serf.target_resource and serf.target_resource.value == "wood":
                    # Serf zum neuen Baum schicken
                    from worker_simulation import Position
                    from production_system import ResourceType
                    target_pos = Position(x=tree["x"], y=tree["y"])
                    hq_pos = Position(x=self.hq_position[0], y=self.hq_position[1])
                    serf.assign_to_resource(ResourceType.WOOD, target_pos, hq_pos, None)
                    serf.work_location = "wood"  # Behalte work_location
                    tree["serfs_assigned"] += 1
                    reassigned += 1
                    break

        return reassigned

    # --- VORKOMMEN (Deposits) ---
    def _is_mine_built_at_deposit(self, deposit_x: float, deposit_y: float, category: str) -> bool:
        """
        Prüft ob an dieser Deposit-Position eine Mine gebaut wurde.
        Wenn ja, können Serfs dort NICHT mehr sammeln - nur noch Worker.
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

        # Prüfe ob eine Mine in der Nähe gebaut wurde (Toleranz für Positionsungenauigkeit)
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
        Prüft ob batch_size Serfs zu einer Vorkommen-Kategorie zugewiesen werden können.
        WICHTIG: Serfs können nur an Deposits sammeln wo KEINE Mine gebaut wurde!
        """
        if category not in self.deposit_categories:
            return False
        if self.free_leibeigene < batch_size:
            return False
        # Mindestens ein Deposit mit Ressourcen UND ohne gebaute Mine
        cat_data = self.deposit_categories[category]
        return any(
            d["remaining"] > 0 and not self._is_mine_built_at_deposit(d["x"], d["y"], category)
            for d in cat_data["deposits"]
        )

    def _can_recall_deposit_batch(self, category: str, batch_size: int) -> bool:
        """Prüft ob batch_size Serfs von einer Vorkommen-Kategorie zurückgerufen werden können."""
        if category not in self.deposit_categories:
            return False
        return self.deposit_categories[category]["serfs_assigned"] >= batch_size

    def _assign_deposit_batch(self, category: str, batch_size: int):
        """Weist batch_size Serfs zu einer Vorkommen-Kategorie zu."""
        from worker_simulation import Position
        from production_system import ResourceType
        import random

        resource_type_map = {
            "Eisen": ResourceType.IRON,
            "Stein": ResourceType.STONE,
            "Lehm": ResourceType.CLAY,
            "Schwefel": ResourceType.SULFUR,
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
                # Zufällig ein Deposit wählen
                deposit = random.choice(available_deposits)
                target_pos = Position(x=deposit["x"], y=deposit["y"])
                hq_pos = Position(x=self.hq_position[0], y=self.hq_position[1])
                serf.assign_to_resource(resource_type, target_pos, hq_pos, None)
                serf.work_location = "deposit"  # NEU: Markiere als Vorkommen-Serf
                assigned += 1

        cat_data["serfs_assigned"] += assigned
        self.free_leibeigene -= assigned
        self.resource_workers[category] = self.resource_workers.get(category, 0) + assigned

    def _recall_deposit_batch(self, category: str, batch_size: int):
        """Ruft batch_size Serfs von einer Vorkommen-Kategorie zurück."""
        resource_type_map = {
            "Eisen": "iron",
            "Stein": "stone",
            "Lehm": "clay",
            "Schwefel": "sulfur",
        }
        target_resource_value = resource_type_map.get(category)

        recalled = 0
        for serf in self.production_system.serfs:
            if recalled >= batch_size:
                break
            # NEU: Prüfe work_location um Deposit- von Minen-Serfs zu unterscheiden
            if (serf.target_resource and
                serf.target_resource.value == target_resource_value and
                serf.work_location == "deposit"):
                serf.stop()
                recalled += 1

        cat_data = self.deposit_categories[category]
        cat_data["serfs_assigned"] = max(0, cat_data["serfs_assigned"] - recalled)
        self.free_leibeigene += recalled
        self.resource_workers[category] = max(0, self.resource_workers.get(category, 0) - recalled)

    def _auto_reassign_deposit_serf(self, category: str, from_x: float, from_y: float) -> bool:
        """
        Automatisches Weitersammeln für Vorkommen: Suche nächstes Deposit im Radius.

        Returns: True wenn Serf erfolgreich zu neuem Deposit zugewiesen wurde
        """
        import math

        cat_data = self.deposit_categories.get(category)
        if not cat_data:
            return False

        # Finde nächstes Deposit mit Ressourcen im Radius
        best_deposit = None
        best_distance = float('inf')

        for deposit in cat_data["deposits"]:
            if deposit["remaining"] > 0:
                dx = deposit["x"] - from_x
                dy = deposit["y"] - from_y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance <= SERF_SEARCH_RADIUS and distance < best_distance:
                    best_distance = distance
                    best_deposit = deposit

        if best_deposit:
            # Serf zum neuen Deposit schicken (bleibt in derselben Kategorie)
            # Der serfs_assigned Zähler bleibt gleich, da Serf weitermacht
            return True

        return False

    # --- STOLLEN (Shafts) - Serfs können hier IMMER sammeln ---
    # HINWEIS: "mine_categories" wird jetzt für STOLLEN verwendet, nicht für gebaute Minen!
    # Stollen (XD_Iron1 etc.) sind separate Ressourcen-Punkte wo Serfs sammeln.
    # Gebaute Minen werden von Workern (Miner) betrieben, nicht von Serfs!

    def _can_assign_shaft_batch(self, shaft_type: str, batch_size: int) -> bool:
        """
        Prüft ob batch_size Serfs zu einem Stollen-Typ zugewiesen werden können.
        Stollen sind IMMER verfügbar - keine Mine kann dort gebaut werden.
        (XD_Iron1 = Eisenstollen, XD_Stone1 = Steinstollen, etc.)
        """
        if shaft_type not in self.shaft_categories:
            return False
        if self.free_leibeigene < batch_size:
            return False
        # Stollen haben begrenzte Kapazität (400 Ressourcen pro Stollen)
        # Prüfe ob mindestens ein Stollen mit Ressourcen existiert
        shaft_data = self.shaft_categories[shaft_type]
        return any(s.get("remaining", 400) > 0 for s in shaft_data.get("shafts", []))

    def _can_recall_shaft_batch(self, shaft_type: str, batch_size: int) -> bool:
        """Prüft ob batch_size Serfs von einem Stollen-Typ zurückgerufen werden können."""
        if shaft_type not in self.shaft_categories:
            return False
        return self.shaft_categories[shaft_type].get("serfs_assigned", 0) >= batch_size

    def _assign_shaft_batch(self, shaft_type: str, batch_size: int):
        """
        Weist batch_size Serfs zu einem Stollen-Typ zu.
        Stollen (XD_Iron1 etc.) haben jeweils 400 Ressourcen und sind IMMER verfügbar.
        """
        from worker_simulation import Position
        from production_system import ResourceType

        shaft_to_resource = {
            "Eisen": ResourceType.IRON,
            "Stein": ResourceType.STONE,
            "Lehm": ResourceType.CLAY,
            "Schwefel": ResourceType.SULFUR,
        }
        resource_type = shaft_to_resource.get(shaft_type)
        if not resource_type:
            return

        shaft_data = self.shaft_categories.get(shaft_type)
        if not shaft_data:
            return

        # Finde Stollen mit verfügbaren Ressourcen
        available_shafts = [s for s in shaft_data.get("shafts", []) if s.get("remaining", 400) > 0]
        if not available_shafts:
            return

        assigned = 0
        for serf in self.production_system.serfs:
            if assigned >= batch_size:
                break
            if serf.is_idle():
                # Zum nächsten verfügbaren Stollen mit wenigsten Serfs schicken
                available_shafts.sort(key=lambda s: s.get("serfs_assigned", 0))
                shaft = available_shafts[0]
                target_pos = Position(x=shaft["x"], y=shaft["y"])
                hq_pos = Position(x=self.hq_position[0], y=self.hq_position[1])
                serf.assign_to_resource(resource_type, target_pos, hq_pos, None)
                serf.work_location = "shaft"  # Markiere als Stollen-Serf
                shaft["serfs_assigned"] = shaft.get("serfs_assigned", 0) + 1
                assigned += 1

        shaft_data["serfs_assigned"] = shaft_data.get("serfs_assigned", 0) + assigned
        self.free_leibeigene -= assigned
        self.resource_workers[shaft_type] = self.resource_workers.get(shaft_type, 0) + assigned

    def _recall_shaft_batch(self, shaft_type: str, batch_size: int):
        """Ruft batch_size Serfs von einem Stollen-Typ zurück."""
        shaft_to_resource_value = {
            "Eisen": "iron",
            "Stein": "stone",
            "Lehm": "clay",
            "Schwefel": "sulfur",
        }
        target_resource_value = shaft_to_resource_value.get(shaft_type)

        recalled = 0
        for serf in self.production_system.serfs:
            if recalled >= batch_size:
                break
            # Prüfe work_location um Stollen- von Deposit-Serfs zu unterscheiden
            if (serf.target_resource and
                serf.target_resource.value == target_resource_value and
                serf.work_location == "shaft"):
                serf.stop()
                recalled += 1

        shaft_data = self.shaft_categories.get(shaft_type)
        if shaft_data:
            shaft_data["serfs_assigned"] = max(0, shaft_data.get("serfs_assigned", 0) - recalled)
        self.free_leibeigene += recalled
        self.resource_workers[shaft_type] = max(0, self.resource_workers.get(shaft_type, 0) - recalled)

    # ENTFERNT: Alte Mine-Serf-Zuweisung - Serfs arbeiten NICHT an gebauten Minen!
    # Gebaute Minen werden von Workern (PU_Miner) betrieben.
    def _can_assign_mine_batch(self, mine_type: str, batch_size: int) -> bool:
        """DEAKTIVIERT: Serfs arbeiten nicht an gebauten Minen - nur Worker tun das."""
        return False  # Immer False - Serfs können nicht an Minen arbeiten

    def _can_recall_mine_batch(self, mine_type: str, batch_size: int) -> bool:
        """DEAKTIVIERT: Serfs arbeiten nicht an gebauten Minen."""
        return False  # Immer False

    def _assign_mine_batch(self, mine_type: str, batch_size: int):
        """Weist batch_size Serfs zu einer Mine-Kategorie zu."""
        from worker_simulation import Position
        from production_system import ResourceType

        mine_to_resource = {
            "Eisenmine": ResourceType.IRON,
            "Steinmine": ResourceType.STONE,
            "Lehmmine": ResourceType.CLAY,
            "Schwefelmine": ResourceType.SULFUR,
        }
        resource_type = mine_to_resource.get(mine_type)
        if not resource_type:
            return

        mine_to_name = {
            "Eisenmine": "Eisen",
            "Steinmine": "Stein",
            "Lehmmine": "Lehm",
            "Schwefelmine": "Schwefel",
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
                hq_pos = Position(x=self.hq_position[0], y=self.hq_position[1])
                serf.assign_to_resource(resource_type, target_pos, hq_pos, None)
                serf.work_location = "mine"  # NEU: Markiere als Minen-Serf
                assigned += 1

        mine_data = self.mine_categories[mine_type]
        mine_data["serfs_assigned"] += assigned
        self.free_leibeigene -= assigned
        if resource_name:
            self.resource_workers[resource_name] = self.resource_workers.get(resource_name, 0) + assigned

    def _recall_mine_batch(self, mine_type: str, batch_size: int):
        """Ruft batch_size Serfs von einer Mine-Kategorie zurück."""
        mine_to_resource = {
            "Eisenmine": "iron",
            "Steinmine": "stone",
            "Lehmmine": "clay",
            "Schwefelmine": "sulfur",
        }
        target_resource_value = mine_to_resource.get(mine_type)

        mine_to_name = {
            "Eisenmine": "Eisen",
            "Steinmine": "Stein",
            "Lehmmine": "Lehm",
            "Schwefelmine": "Schwefel",
        }
        resource_name = mine_to_name.get(mine_type)

        recalled = 0
        for serf in self.production_system.serfs:
            if recalled >= batch_size:
                break
            # NEU: Prüfe work_location um Minen- von Deposit-Serfs zu unterscheiden
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
        """Prüft ob batch_size Serfs zu Baustellen zugewiesen werden können."""
        # Braucht freie Leibeigene und mindestens eine Baustelle
        if self.free_leibeigene < batch_size:
            return False
        return len(self.construction_sites) > 0

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
                serf.assign_to_build(
                    target_site["building"],
                    build_pos,
                    serf_pos,
                    target_site["site_id"]
                )
                assigned += 1

        target_site["serfs_assigned"] += assigned
        self.free_leibeigene -= assigned

    def _can_recall_build_batch(self, batch_size: int) -> bool:
        """Prüft ob batch_size Serfs von Baustellen zurückgerufen werden können."""
        total_building_serfs = sum(s["serfs_assigned"] for s in self.construction_sites)
        return total_building_serfs >= batch_size

    def _recall_build_batch(self, batch_size: int):
        """Ruft batch_size Serfs von Baustellen zurück."""
        recalled = 0
        for serf in self.production_system.serfs:
            if recalled >= batch_size:
                break
            if serf.is_building():
                # Finde zugehörige Baustelle und reduziere Zähler
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
        """Gibt Anzahl aktiver Baustellen zurück."""
        return len(self.construction_sites)

    def step(self, action):
        reward = 0.0
        action_name = "wait"
        info = {}

        if action == 0:
            action_name = "wait"

        # =================================================================
        # GEBÄUDE-BATCH-BAU (1x, 3x, 5x)
        # =================================================================
        elif action < self.offset_upgrade:
            batch_action = action - self.offset_build_batch
            building_idx = batch_action // len(self.build_batch_sizes)
            batch_idx = batch_action % len(self.build_batch_sizes)
            building = self.buildable_buildings[building_idx]
            batch_size = self.build_batch_sizes[batch_idx]

            if self._can_build_batch(building, batch_size):
                for _ in range(batch_size):
                    reward += self._build_building(building)
                action_name = f"build_{building}_x{batch_size}"

        elif action < self.offset_tech:
            building = self.upgradeable_buildings[action - self.offset_upgrade]
            if self._can_upgrade(building):
                reward += self._upgrade_building(building)
                action_name = f"upgrade_{building}"

        elif action < self.offset_recruit:
            tech = self.tech_list[action - self.offset_tech]
            if self._can_research(tech):
                reward += self._research_tech(tech)
                action_name = f"research_{tech}"

        elif action < self.offset_resource_batch:
            soldier = self.soldier_types[action - self.offset_recruit]
            if self._can_recruit(soldier):
                reward += self._recruit_soldier(soldier)
                action_name = f"recruit_{soldier}"

        # =================================================================
        # RESSOURCEN-BATCH-ACTIONS (1x, 3x, 5x)
        # Holz-Zonen: 6 Kategorien mit Batch
        # Vorkommen: 4 Kategorien mit Batch
        # Stollen: 4 Kategorien mit Batch
        # =================================================================
        elif action < self.offset_serf:
            res_action = action - self.offset_resource_batch
            n_batch = len(self.resource_batch_sizes)
            n_zones = len(self.wood_zone_names)

            # Action-Layout (NEU mit Holz-Zonen):
            # [0..17]  = Holz-Zonen zuweisen (6 Zonen × 3 Batch)
            # [18..35] = Holz-Zonen entfernen (6 Zonen × 3 Batch)
            # [36..47] = Vorkommen zuweisen (4 Kategorien × 3 Batch)
            # [48..59] = Vorkommen entfernen (4 Kategorien × 3 Batch)
            # [60..71] = Stollen zuweisen (4 Kategorien × 3 Batch)
            # [72..83] = Stollen entfernen (4 Kategorien × 3 Batch)

            if res_action < n_zones * n_batch:
                # Holz-Zone zuweisen
                zone_action = res_action
                zone_idx = zone_action // n_batch
                batch_idx = zone_action % n_batch
                zone_name = self.wood_zone_names[zone_idx]
                batch_size = self.resource_batch_sizes[batch_idx]
                if self._can_assign_wood_zone_batch(zone_name, batch_size):
                    self._assign_wood_zone_batch(zone_name, batch_size)
                    action_name = f"assign_wood_{zone_name}_x{batch_size}"

            elif res_action < n_zones * n_batch * 2:
                # Holz-Zone entfernen
                zone_action = res_action - n_zones * n_batch
                zone_idx = zone_action // n_batch
                batch_idx = zone_action % n_batch
                zone_name = self.wood_zone_names[zone_idx]
                batch_size = self.resource_batch_sizes[batch_idx]
                if self._can_recall_wood_zone_batch(zone_name, batch_size):
                    self._recall_wood_zone_batch(zone_name, batch_size)
                    action_name = f"recall_wood_{zone_name}_x{batch_size}"

            elif res_action < n_zones * n_batch * 2 + len(self.deposit_category_names) * n_batch:
                # Vorkommen zuweisen
                dep_action = res_action - n_zones * n_batch * 2
                cat_idx = dep_action // n_batch
                batch_idx = dep_action % n_batch
                category = self.deposit_category_names[cat_idx]
                batch_size = self.resource_batch_sizes[batch_idx]
                if self._can_assign_deposit_batch(category, batch_size):
                    self._assign_deposit_batch(category, batch_size)
                    action_name = f"assign_deposit_{category}_x{batch_size}"

            elif res_action < n_zones * n_batch * 2 + len(self.deposit_category_names) * n_batch * 2:
                # Vorkommen entfernen
                dep_action = res_action - n_zones * n_batch * 2 - len(self.deposit_category_names) * n_batch
                cat_idx = dep_action // n_batch
                batch_idx = dep_action % n_batch
                category = self.deposit_category_names[cat_idx]
                batch_size = self.resource_batch_sizes[batch_idx]
                if self._can_recall_deposit_batch(category, batch_size):
                    self._recall_deposit_batch(category, batch_size)
                    action_name = f"recall_deposit_{category}_x{batch_size}"

            elif res_action < n_zones * n_batch * 2 + len(self.deposit_category_names) * n_batch * 2 + len(self.shaft_category_names) * n_batch:
                # Stollen zuweisen (ersetzt alte Mine-Serf-Zuweisung)
                shaft_action = res_action - n_zones * n_batch * 2 - len(self.deposit_category_names) * n_batch * 2
                shaft_idx = shaft_action // n_batch
                batch_idx = shaft_action % n_batch
                shaft_type = self.shaft_category_names[shaft_idx]
                batch_size = self.resource_batch_sizes[batch_idx]
                if self._can_assign_shaft_batch(shaft_type, batch_size):
                    self._assign_shaft_batch(shaft_type, batch_size)
                    action_name = f"assign_shaft_{shaft_type}_x{batch_size}"

            else:
                # Stollen entfernen
                shaft_action = res_action - n_zones * n_batch * 2 - len(self.deposit_category_names) * n_batch * 2 - len(self.shaft_category_names) * n_batch
                shaft_idx = shaft_action // n_batch
                batch_idx = shaft_action % n_batch
                shaft_type = self.shaft_category_names[shaft_idx]
                batch_size = self.resource_batch_sizes[batch_idx]
                if self._can_recall_shaft_batch(shaft_type, batch_size):
                    self._recall_shaft_batch(shaft_type, batch_size)
                    action_name = f"recall_shaft_{shaft_type}_x{batch_size}"

        # Leibeigene kaufen/entlassen (Batch-Actions: 1x, 3x, 5x)
        elif action < self.offset_batch_recruit:
            serf_action = action - self.offset_serf
            n_batches = len(self.serf_batch_sizes)

            if serf_action < n_batches:  # Kaufen (0, 1, 2 = 1x, 3x, 5x)
                batch_size = self.serf_batch_sizes[serf_action]
                if self._can_buy_serf_batch(batch_size):
                    for _ in range(batch_size):
                        reward += self._buy_serf()
                    action_name = f"buy_serf_x{batch_size}"
            else:  # Entlassen (3, 4, 5 = 1x, 3x, 5x)
                batch_idx = serf_action - n_batches
                batch_size = self.serf_batch_sizes[batch_idx]
                if self._can_dismiss_serf_batch(batch_size):
                    for _ in range(batch_size):
                        reward += self._dismiss_serf()
                    action_name = f"dismiss_serf_x{batch_size}"

        # NEU: Batch-Rekrutierung für Scharfschützen (3x, 5x)
        elif action < self.offset_demolish:
            batch_action = action - self.offset_batch_recruit
            # Action layout: [Scharfschützen_x3, Scharfschützen_x5, Scharfschützen_2_x3, Scharfschützen_2_x5]
            soldier_idx = batch_action // len(self.scharfschuetzen_batch_sizes)
            batch_idx = batch_action % len(self.scharfschuetzen_batch_sizes)
            soldier_type = self.scharfschuetzen_types[soldier_idx]
            batch_size = self.scharfschuetzen_batch_sizes[batch_idx]

            if self._can_recruit_batch(soldier_type, batch_size):
                for _ in range(batch_size):
                    reward += self._recruit_soldier(soldier_type)
                action_name = f"recruit_{soldier_type}_x{batch_size}"

        # NEU: Gebäude abreißen
        elif action < self.offset_bless:
            building_idx = action - self.offset_demolish
            building = self.buildable_buildings[building_idx]
            if self._can_demolish(building):
                reward += self._demolish_building(building)
                action_name = f"demolish_{building}"

        # NEU: Segnen (5 Kategorien)
        elif action < self.offset_tax:
            bless_category = action - self.offset_bless
            if bless_category in BLESS_CATEGORIES and self._can_bless(bless_category):
                reward += self._bless(bless_category)
                action_name = f"bless_{BLESS_CATEGORIES[bless_category]['name']}"

        # NEU: Steuern einstellen
        elif action < self.offset_alarm:
            tax_level = action - self.offset_tax
            if tax_level != self.current_tax_level and tax_level in TAX_LEVELS:
                reward += self._set_tax_level(tax_level)
                action_name = f"set_tax_{tax_level}"

        # NEU: Alarm-Modus
        elif action < self.offset_build_serf:
            alarm_action = action - self.offset_alarm
            if alarm_action == 0:  # Alarm AN
                if not self.alarm_active and self.alarm_cooldown <= 0:
                    self.alarm_active = True
                    action_name = "alarm_on"
            else:  # Alarm AUS
                if self.alarm_active:
                    self.alarm_active = False
                    self.alarm_cooldown = ALARM_RECHARGE_TIME
                    action_name = "alarm_off"

        # NEU: Bau-Serfs zuweisen/zurückrufen
        else:
            build_serf_action = action - self.offset_build_serf
            n_batches = len(self.build_serf_batch_sizes)
            if build_serf_action < n_batches:
                # Zuweisen
                batch_size = self.build_serf_batch_sizes[build_serf_action]
                if self._can_assign_build_batch(batch_size):
                    self._assign_build_batch(batch_size)
                    action_name = f"assign_build_x{batch_size}"
            else:
                # Zurückrufen
                batch_idx = build_serf_action - n_batches
                batch_size = self.build_serf_batch_sizes[batch_idx]
                if self._can_recall_build_batch(batch_size):
                    self._recall_build_batch(batch_size)
                    action_name = f"recall_build_x{batch_size}"

        self._tick_time()

        # Info für Debugging (keine Rewards mehr!)
        efficiency = self.workforce_manager.get_average_efficiency()
        exhausted_ratio = self.workforce_manager.get_exhausted_ratio()

        self.action_history.append({"time": self.current_time, "action": action_name})
        info["action_name"] = action_name
        info["efficiency"] = efficiency
        info["exhausted_ratio"] = exhausted_ratio

        # MINIMALER REWARD: Nur Scharfschützen am Ende zählen!
        # Agent muss selbst herausfinden welche Strategie optimal ist
        terminated = self.current_time >= self.max_time
        if terminated:
            # EINZIGER REWARD: Anzahl Scharfschützen × 20
            reward += self.scharfschuetzen * 20.0

        return self._get_observation(), reward, terminated, False, info

    def _build_building(self, building):
        """
        Startet ein Bauprojekt. Erstellt eine Baustelle die Leibeigene braucht.

        NEU: Gebäude werden NICHT mehr automatisch gebaut!
        Der Agent muss Leibeigene zur Baustelle zuweisen.
        """
        b_info = buildings_db[building]

        for resource, amount in b_info["cost"].items():
            self.resources[resource] -= amount

        position = None
        if b_info.get("mine_type"):
            mine_type = b_info["mine_type"]
            positions = self.mine_positions.get(mine_type, [])
            built_count = len(self.built_mines.get(mine_type, []))
            if built_count < len(positions):
                position = positions[built_count]
                self.built_mines[mine_type].append(position)
        else:
            if self.available_positions:
                position = self.available_positions.pop(0)
                self.used_positions.append(position)

        # NEU: Erstelle Baustelle statt direkt zur Queue
        site = {
            "building": building,
            "position": position,
            "total_time": b_info["build_time"],
            "remaining_work": b_info["build_time"],  # Arbeit in Sekunden
            "serfs_assigned": 0,
            "site_id": self.next_site_id,
        }
        self.construction_sites.append(site)
        self.next_site_id += 1

        # MINIMALER REWARD: Agent soll selbst die optimale Strategie finden
        return 0.0

    def _upgrade_building(self, building):
        b_info = buildings_db[building]
        new_building = b_info["upgrade_to"]

        for resource, amount in b_info["upgrade_cost"].items():
            self.resources[resource] -= amount

        self.upgrade_queue.append((building, new_building, b_info["upgrade_time"]))

        # MINIMALER REWARD: Agent soll selbst die optimale Strategie finden
        return 0.0

    def _research_tech(self, tech):
        tech_info = technologies[tech]

        for resource, amount in tech_info["cost"].items():
            self.resources[resource] -= amount

        self.current_research = (tech, tech_info["research_time"])

        # MINIMALER REWARD: Agent soll selbst die optimale Strategie finden
        return 0.0

    def _recruit_soldier(self, soldier):
        s_info = soldiers_db[soldier]

        for resource, amount in s_info["cost"].items():
            self.resources[resource] -= amount

        self.recruit_queue.append((soldier, s_info.get("train_time", 20)))

        # HAUPT-REWARD: Nur Scharfschützen zählen!
        if "Scharfschützen" in soldier:
            return 10.0  # Großer Reward für das Hauptziel
        return 0.0

    def _buy_serf(self):
        """Kauft einen neuen Leibeigenen."""
        from worker_simulation import Position

        self.resources[RESOURCE_TALER] -= SERF_BUY_COST
        self.total_leibeigene += 1
        self.free_leibeigene += 1

        # Neuen Serf erstellen (vereinfacht - keine IDs mehr)
        hq_pos = Position(x=self.hq_position[0], y=self.hq_position[1])
        serf = Serf(position=Position(x=hq_pos.x, y=hq_pos.y), target_resource=None)
        self.production_system.serfs.append(serf)

        return 0.0  # MINIMALER REWARD

    def _dismiss_serf(self):
        """Entlässt einen freien Leibeigenen."""
        if self.free_leibeigene <= 0:
            return 0.0

        self.total_leibeigene -= 1
        self.free_leibeigene -= 1

        # Einen idle Serf entfernen (vereinfacht)
        for i, serf in enumerate(self.production_system.serfs):
            if serf.is_idle():
                self.production_system.serfs.pop(i)
                break

        return 0.0  # MINIMALER REWARD

    def _demolish_building(self, building: str):
        """Reißt ein Gebäude ab."""
        if self.buildings.get(building, 0) < 1:
            return 0.0

        self.buildings[building] -= 1

        # Ressourcen zurückgeben (50% der Baukosten)
        b_info = buildings_db.get(building, {})
        for resource, amount in b_info.get("cost", {}).items():
            refund = int(amount * 0.5)
            self.resources[resource] = self.resources.get(resource, 0) + refund

        # Position wieder freigeben
        for pos_key, pos in list(self.building_position_map.items()):
            if pos_key.startswith(building):
                self.available_positions.append(pos)
                del self.building_position_map[pos_key]
                break

        return 0.0  # MINIMALER REWARD

    def _bless(self, category: int):
        """Segnet Worker einer Kategorie (Kloster-Aktion).

        Args:
            category: Segen-Kategorie (0-4, aus BLESS_CATEGORIES)
        """
        # Faith abziehen
        self.faith -= BLESS_REQUIRED_FAITH

        # Cooldown und aktive Zeit für diese Kategorie setzen
        self.bless_cooldowns[category] = BLESS_COOLDOWN
        self.bless_active_times[category] = BLESS_DURATION

        # Motivation-Bonus für betroffene Worker
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
        total_monasteries = (self.buildings.get("Kloster_1", 0) +
                            self.buildings.get("Kloster_2", 0) +
                            self.buildings.get("Kloster_3", 0))
        if total_monasteries > 0:
            # Faith pro Sekunde = Anzahl Priester (vereinfacht)
            priests = total_monasteries * 6  # Vereinfacht: 6 pro Kloster
            self.faith = min(self.faith + priests * TIME_STEP, BLESS_REQUIRED_FAITH * 5)

        # NEU: Infrastruktur synchronisieren
        self._sync_workforce_infrastructure()

        # NEU: Motivation auf WorkTime-Regeneration anwenden
        total_motivation = self._get_total_motivation()
        self.workforce_manager.set_motivation_modifier(total_motivation)

        # NEU: WorkTime-System ticken (Worker Pausen-Simulation)
        self.workforce_manager.tick(TIME_STEP)

        # Produktionssystem ticken (mit WorkTime-Effizienz)
        production_output = self.production_system.tick(TIME_STEP)

        # Produzierte Ressourcen zu Inventar hinzufügen
        resource_name_map = {
            ResourceType.WOOD: RESOURCE_HOLZ,
            ResourceType.STONE: RESOURCE_STEIN,
            ResourceType.CLAY: RESOURCE_LEHM,
            ResourceType.IRON: RESOURCE_EISEN,
            ResourceType.SULFUR: RESOURCE_SCHWEFEL,
            ResourceType.GOLD: RESOURCE_TALER,
        }
        for res_type, amount in production_output.items():
            res_name = resource_name_map.get(res_type)
            if res_name:
                self.resources[res_name] = self.resources.get(res_name, 0) + amount

        # VEREINFACHTES TRACKING: Ressourcen-Erschöpfung
        # Bäume: Reduziere resource_remaining basierend auf aktiven Holz-Serfs
        if self.wood_serfs > 0:
            # 2 Holz pro ~5.5s = ~0.36 Holz pro Sekunde pro Serf
            wood_per_second = WOOD_PER_EXTRACTION / EXTRACTION_TIME_WOOD
            total_wood_extracted = self.wood_serfs * wood_per_second * TIME_STEP
            # Verteile auf Bäume (vereinfacht: erster nicht-leerer Baum)
            for i, tree in enumerate(self.tree_list_internal):
                if total_wood_extracted <= 0:
                    break
                if tree["resource_remaining"] > 0:
                    extracted = min(tree["resource_remaining"], total_wood_extracted)
                    tree["resource_remaining"] -= extracted
                    total_wood_extracted -= extracted
                    # Wenn Baum leer, versuche automatisches Weitersammeln
                    if tree["resource_remaining"] <= 0 and tree["serfs_assigned"] > 0:
                        serfs_to_reassign = tree["serfs_assigned"]
                        tree["serfs_assigned"] = 0
                        # AUTOMATISCHES WEITERSAMMELN: Suche nächsten Baum im Radius
                        reassigned = self._auto_reassign_wood_serfs(
                            tree["x"], tree["y"], serfs_to_reassign
                        )
                        # Nur nicht-zugewiesene Serfs werden frei
                        freed_serfs = serfs_to_reassign - reassigned
                        if freed_serfs > 0:
                            self.wood_serfs = max(0, self.wood_serfs - freed_serfs)
                            self.free_leibeigene += freed_serfs
                            self.resource_workers[RESOURCE_HOLZ] = max(0,
                                self.resource_workers.get(RESOURCE_HOLZ, 0) - freed_serfs)

        # Vorkommen-Erschöpfung (vereinfacht)
        for category, cat_data in self.deposit_categories.items():
            if cat_data["serfs_assigned"] > 0:
                # Extraktionsrate basierend auf Kategorie
                extraction_rates = {"Eisen": 1.0/4.54, "Stein": 1.0/5.54, "Lehm": 1.0/5.54, "Schwefel": 1.0/4.54}
                rate = extraction_rates.get(category, 0.2)
                total_extracted = cat_data["serfs_assigned"] * rate * TIME_STEP
                # Verteile auf Deposits
                for deposit in cat_data["deposits"]:
                    if total_extracted <= 0:
                        break
                    if deposit["remaining"] > 0:
                        extracted = min(deposit["remaining"], total_extracted)
                        deposit["remaining"] -= extracted
                        total_extracted -= extracted
                        # Wenn Deposit leer, versuche automatisches Weitersammeln
                        if deposit["remaining"] <= 0:
                            # AUTOMATISCHES WEITERSAMMELN: Suche nächstes Deposit im Radius
                            reassigned = self._auto_reassign_deposit_serf(
                                category, deposit["x"], deposit["y"]
                            )
                            if not reassigned:
                                # Kein Deposit im Radius gefunden -> Serf wird frei
                                cat_data["serfs_assigned"] = max(0, cat_data["serfs_assigned"] - 1)
                                self.free_leibeigene += 1
                                self.resource_workers[category] = max(0,
                                    self.resource_workers.get(category, 0) - 1)

        # Steuer-Einkommen (aus extra2/logic.xml)
        # RegularTax = fester Betrag PRO WORKER (nicht Multiplikator!)
        if self.current_time % INCOME_CYCLE == 0:
            tax_info = TAX_LEVELS.get(self.current_tax_level, TAX_LEVELS[2])
            # Zähle alle arbeitenden Worker
            total_workers = len(self.workforce_manager.workers)
            # Steuer-Einkommen = RegularTax pro Worker
            tax_income = tax_info["regular_tax"] * total_workers
            self.resources[RESOURCE_TALER] += tax_income

            # Motivation-Änderung anwenden
            motivation_change = tax_info["motivation_change"]
            self.base_motivation = max(0.25, min(3.0, self.base_motivation + motivation_change))

        # NEU: Baustellen mit Leibeigenen-System verarbeiten
        completed_sites = []
        for i, site in enumerate(self.construction_sites):
            if site["serfs_assigned"] > 0:
                # Bau-Fortschritt: Mehr Serfs = schnellerer Bau
                # Formel: 1 Serf = normale Geschwindigkeit, jeder weitere +50% (abnehmend)
                # Effektive Serfs: 1 + 0.5 * (n-1) für n Serfs
                n_serfs = site["serfs_assigned"]
                effective_workers = 1.0 + 0.5 * (n_serfs - 1)
                work_done = TIME_STEP * effective_workers
                site["remaining_work"] -= work_done

                if site["remaining_work"] <= 0:
                    # Gebäude fertig!
                    building = site["building"]
                    pos = site["position"]
                    self.buildings[building] = self.buildings.get(building, 0) + 1
                    if pos:
                        self.building_position_map[f"{building}_{len(self.building_position_map)}"] = pos
                    # Bei Gebäude-Fertigstellung Worker/Mine/Refiner erstellen
                    self._on_building_completed(building, pos)
                    # Serfs werden frei
                    self._release_serfs_from_site(site)
                    completed_sites.append(i)

        for i in reversed(completed_sites):
            self.construction_sites.pop(i)

        # Legacy: Alte Bau-Queue verarbeiten (falls noch Einträge vorhanden)
        completed = []
        for i, (building, remaining, pos) in enumerate(self.construction_queue):
            remaining -= TIME_STEP
            if remaining <= 0:
                self.buildings[building] = self.buildings.get(building, 0) + 1
                if pos:
                    self.building_position_map[f"{building}_{len(self.building_position_map)}"] = pos
                self._on_building_completed(building, pos)
                completed.append(i)
            else:
                self.construction_queue[i] = (building, remaining, pos)
        for i in reversed(completed):
            self.construction_queue.pop(i)

        # Upgrade-Queue verarbeiten
        completed = []
        for i, (old_b, new_b, remaining) in enumerate(self.upgrade_queue):
            remaining -= TIME_STEP
            if remaining <= 0:
                self.buildings[old_b] = max(0, self.buildings.get(old_b, 0) - 1)
                self.buildings[new_b] = self.buildings.get(new_b, 0) + 1
                completed.append(i)
            else:
                self.upgrade_queue[i] = (old_b, new_b, remaining)
        for i in reversed(completed):
            self.upgrade_queue.pop(i)

        # Forschung verarbeiten (abhängig von Gelehrten-Effizienz)
        if self.current_research:
            tech, remaining = self.current_research
            # NEU: Forschungsgeschwindigkeit hängt von Gelehrten-WorkTime ab
            scholar_efficiency = self._get_scholar_efficiency()
            remaining -= TIME_STEP * scholar_efficiency
            if remaining <= 0:
                self.researched_techs.add(tech)
                self.current_research = None
            else:
                self.current_research = (tech, remaining)

        # Rekrutierung verarbeiten
        completed = []
        for i, (soldier, remaining) in enumerate(self.recruit_queue):
            remaining -= TIME_STEP
            if remaining <= 0:
                self.soldiers[soldier] = self.soldiers.get(soldier, 0) + 1
                if "Scharfschützen" in soldier:
                    self.scharfschuetzen += 1
                completed.append(i)
            else:
                self.recruit_queue[i] = (soldier, remaining)
        for i in reversed(completed):
            self.recruit_queue.pop(i)

    def _on_building_completed(self, building: str, position):
        """Callback wenn ein Gebäude fertig wird - erstellt Worker/Minen/Refiner"""
        from worker_simulation import Position

        base_name = get_base_building_name(building)
        level = get_building_level(building)

        if position is None:
            position = self.hq_position

        # Position in Position-Objekt umwandeln
        if isinstance(position, dict):
            pos_obj = Position(x=position.get('x', 0), y=position.get('y', 0))
        elif isinstance(position, tuple):
            pos_obj = Position(x=position[0], y=position[1])
        else:
            pos_obj = position

        # NEU: Gebäude im MapManager-Grid blockieren (für Pfadfindung)
        self.map_manager.add_building(pos_obj.x, pos_obj.y, base_name)

        # Minen erstellen
        if "mine" in building.lower() or base_name in ["Steinmine", "Lehmmine", "Eisenmine", "Schwefelmine"]:
            resource_map = {
                "Steinmine": ResourceType.STONE,
                "Lehmmine": ResourceType.CLAY,
                "Eisenmine": ResourceType.IRON,
                "Schwefelmine": ResourceType.SULFUR,
            }
            resource_type = resource_map.get(base_name)
            if resource_type:
                # Mine erstellen (Werte aus XML)
                max_workers_by_level = {1: 5, 2: 6, 3: 7}
                amount_by_level = {1: 4, 2: 5, 3: 6}
                mine = Mine(
                    name=f"{base_name}_{level}",
                    resource_type=resource_type,
                    position=pos_obj,
                    level=level,
                    max_workers=max_workers_by_level.get(level, 5),
                    amount_to_mine=amount_by_level.get(level, 4)
                )
                mine_key = f"{base_name}_{level}"
                self.production_system.mines[mine_key] = mine

                # Worker für Mine erstellen (Miner haben WorkTime!)
                worker = self.workforce_manager.add_worker("miner", pos_obj, pos_obj)
                if worker:
                    mine.current_workers += 1

                # NEU: mine_categories für Serf-Zuweisung aktualisieren
                if base_name in self.mine_categories:
                    self.mine_categories[base_name]["mines_built"] += 1

        # Raffinerien erstellen (Sägemühle, Schmiede, Lehmhütte, etc.)
        elif base_name in ["Sägemühle", "Schmiede", "Alchimistenhütte", "Steinmetzhütte", "Lehmhütte"]:
            # Output-Ressource und Input-Ressource Mapping
            refiner_config = {
                "Sägemühle": {
                    "output": ResourceType.WOOD,
                    "input": ResourceType.WOOD,  # Holz verarbeiten
                    "initial_factor": 4,
                    "transport_amount": 5,
                    "worker_type": "sawmill_worker"
                },
                "Lehmhütte": {
                    "output": ResourceType.CLAY,
                    "input": ResourceType.CLAY,  # Lehm verarbeiten (zu Ziegel)
                    "initial_factor": 4,
                    "transport_amount": 5,
                    "worker_type": "brickmaker"
                },
                "Schmiede": {
                    "output": ResourceType.IRON,
                    "input": ResourceType.IRON,  # Eisen verarbeiten
                    "initial_factor": 4,
                    "transport_amount": 5,
                    "worker_type": "smith"
                },
                "Alchimistenhütte": {
                    "output": ResourceType.SULFUR,
                    "input": ResourceType.SULFUR,
                    "initial_factor": 3,
                    "transport_amount": 5,
                    "worker_type": "alchemist"
                },
                "Steinmetzhütte": {
                    "output": ResourceType.STONE,
                    "input": ResourceType.STONE,
                    "initial_factor": 4,
                    "transport_amount": 5,
                    "worker_type": "stonecutter"
                },
            }
            config = refiner_config.get(base_name)
            if config:
                # HQ Position als Position-Objekt
                hq_pos = Position(x=self.hq_position[0], y=self.hq_position[1]) if isinstance(self.hq_position, tuple) else self.hq_position

                refiner = Refiner(
                    name=f"{base_name}_{level}",
                    resource_type=config["output"],
                    input_resource=config["input"],
                    position=pos_obj,
                    supplier_position=hq_pos,  # Vereinfacht: HQ als Quelle
                    level=level,
                    initial_factor=config["initial_factor"],
                    transport_amount=config["transport_amount"]
                )
                refiner_key = f"{base_name}_{level}"
                self.production_system.refiners[refiner_key] = refiner

                # Worker erstellen
                worker = self.workforce_manager.add_worker(config["worker_type"], pos_obj, pos_obj)
                if worker:
                    refiner.current_workers += 1

        # NEU: Scholar für Hochschule erstellen (für Forschung)
        elif base_name == "Hochschule":
            # Hochschule Level 1: 1 Scholar, Level 2: 2 Scholars
            scholars_by_level = {1: 1, 2: 2}
            num_scholars = scholars_by_level.get(level, 1)
            for _ in range(num_scholars):
                self.workforce_manager.add_worker("scholar", pos_obj, pos_obj)

        # NEU: Gunsmith für Büchsenmacherei erstellen
        elif base_name == "Büchsenmacherei":
            self.workforce_manager.add_worker("gunsmith", pos_obj, pos_obj)

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
            print(f"Scharfschützen: {self.scharfschuetzen}")
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
            print(f"Erschöpft: {self.workforce_manager.get_exhausted_ratio():.1%}")

            # Kapazitäten
            print(f"\n--- Kapazitäten ---")
            print(f"Farm-Kapazität: {self._get_total_farm_capacity()} Esser")
            print(f"Wohnhaus-Kapazität: {self._get_total_residence_capacity()} Bewohner")

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
            print(f"Segnung aktiv: {'Ja' if self.bless_active_time > 0 else 'Nein'}")
            if self.bless_active_time > 0:
                print(f"  Verbleibende Zeit: {self.bless_active_time}s")
            if self.bless_cooldown > 0:
                print(f"Segnung Cooldown: {self.bless_cooldown}s")
            print(f"Gesamtmotivation: {self._get_total_motivation()}%")

    def close(self):
        pass


# =============================================================================
# STATISTIKEN
# =============================================================================

print(f"Geladene Gebäude: {len(buildings_db)}")
print(f"Geladene Technologien: {len(technologies)}")
print(f"Geladene Einheiten: {len(soldiers_db)}")
print(f"Baubare Gebäude (Level 1): {len([b for b in buildings_db.keys() if get_building_level(b) == 1])}")
print(f"Upgradeable Gebäude: {len([b for b in buildings_db.keys() if buildings_db[b].get('upgrade_to')])}")

if __name__ == "__main__":
    env = SiedlerScharfschuetzenEnv()
    print(f"\nAction Space: {env.action_space}")
    print(f"Total Actions: {env.total_actions}")
    print(f"  - Wait: 1")
    print(f"  - Build: {env.n_build_actions}")
    print(f"  - Upgrade: {env.n_upgrade_actions}")
    print(f"  - Research: {env.n_tech_actions}")
    print(f"  - Recruit: {env.n_recruit_actions}")
    print(f"  - Resource Positions: {env.n_resource_position_actions}")
    print(f"    - Trees (assign/recall): {env.n_tree_actions * 2} (50 Bäume × 2)")
    print(f"    - Deposits (assign/recall): {env.n_deposit_actions * 2} (6 Deposits × 2)")
    print(f"  - Serf (buy/dismiss batch): {env.n_serf_actions} (1x,3x,5x kaufen + 1x,3x,5x entlassen)")
    print(f"  - Batch Recruit (Scharfschützen): {env.n_batch_recruit_actions} (3x,5x für beide Level)")
    print(f"  - Demolish: {env.n_demolish_actions}")
    print(f"  - Bless: {env.n_bless_actions}")
    print(f"  - Tax levels: {env.n_tax_actions}")
    print(f"\nObservation Space: {env.observation_space}")
    print(f"\n--- Action Offsets ---")
    print(f"  Build: {env.offset_build}")
    print(f"  Upgrade: {env.offset_upgrade}")
    print(f"  Tech: {env.offset_tech}")
    print(f"  Recruit: {env.offset_recruit}")
    print(f"  Resource Positions: {env.offset_resource_pos}")
    print(f"  Serf: {env.offset_serf}")
    print(f"  Batch Recruit: {env.offset_batch_recruit}")
    print(f"  Demolish: {env.offset_demolish}")
    print(f"  Bless: {env.offset_bless}")
    print(f"  Tax: {env.offset_tax}")
