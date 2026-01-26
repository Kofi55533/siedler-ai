# -*- coding: utf-8 -*-
"""
Siedler 5 - Game Bridge
Führt die trainierte Strategie im echten Spiel aus

WICHTIG: Dieses Script benötigt:
1. PyAutoGUI für Maus/Tastatur-Steuerung
2. Die exportierte strategy.json vom Training
3. Das Spiel muss im Fenster-Modus laufen
"""

import json
import time
import os
from typing import Dict, List, Optional

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("WARNUNG: pyautogui nicht installiert!")
    print("Installiere mit: pip install pyautogui")


# =============================================================================
# KONFIGURATION
# =============================================================================

# Spiel-Fenster Einstellungen (anpassen!)
GAME_WINDOW = {
    "title": "Die Siedler",  # Fenster-Titel
    "width": 1920,
    "height": 1080,
    "offset_x": 0,  # Falls nicht an Position 0,0
    "offset_y": 0,
}

# Karten-zu-Bildschirm Konvertierung
# Diese Werte müssen kalibriert werden!
MAP_TO_SCREEN = {
    "map_min_x": 0,
    "map_max_x": 50480,
    "map_min_y": 0,
    "map_max_y": 50496,
    "screen_game_area": {
        "x": 0,
        "y": 0,
        "width": 1600,
        "height": 900,
    },
}

# Hotkeys für das Spiel (Standard-Hotkeys)
HOTKEYS = {
    # Gebäude-Menü
    "building_menu": "b",

    # Gebäude (im Menü)
    "buildings": {
        "Hochschule_1": ["b", "5"],  # Beispiel: B für Menü, dann 5
        "Wohnhaus_1": ["b", "1"],
        "Sägemühle_1": ["b", "2"],
        "Steinmetz_1": ["b", "3"],
        "Steinmine_1": ["b", "m", "1"],  # B, dann M für Minen, dann 1
        "Eisenmine_1": ["b", "m", "2"],
        "Lehmmine_1": ["b", "m", "3"],
        "Schwefelmine_1": ["b", "m", "4"],
        "Büchsenmacherei_1": ["b", "6"],
    },

    # Forschung
    "research_menu": "t",
    "technologies": {
        "Mathematik": ["t", "1"],
        "Fernglas": ["t", "2"],
        "Luntenschloss": ["t", "3"],
    },

    # HQ Upgrade
    "hq_upgrade": ["h", "u"],

    # Rekrutierung
    "recruit_menu": "r",
    "units": {
        "Scharfschütze": ["r", "s"],
    },

    # Kamera
    "camera_to_hq": "h",
}

# Timing (in Sekunden)
TIMING = {
    "key_delay": 0.1,
    "click_delay": 0.2,
    "action_delay": 0.5,
    "build_confirm_delay": 0.3,
}


# =============================================================================
# GAME BRIDGE KLASSE
# =============================================================================

class GameBridge:
    """
    Führt trainierte Aktionen im echten Siedler 5 aus
    """

    def __init__(self, strategy_path: str, hotkeys: Dict = None):
        """
        Args:
            strategy_path: Pfad zur strategy.json
            hotkeys: Optionale Hotkey-Konfiguration
        """
        self.hotkeys = hotkeys or HOTKEYS

        # Lade Strategie
        with open(strategy_path, 'r', encoding='utf-8') as f:
            self.strategy = json.load(f)

        self.actions = self.strategy["actions"]
        self.building_positions = self.strategy["building_positions"]

        print(f"Strategie geladen: {len(self.actions)} Aktionen")
        print(f"Ziel: {self.strategy['goal']}")

        # Status
        self.current_action_idx = 0
        self.game_start_time = None
        self.paused = False

    def map_to_screen(self, map_x: float, map_y: float) -> tuple:
        """
        Konvertiert Karten-Koordinaten zu Bildschirm-Koordinaten

        WICHTIG: Diese Funktion muss kalibriert werden!
        """
        config = MAP_TO_SCREEN

        # Normalisiere Map-Koordinaten (0-1)
        norm_x = (map_x - config["map_min_x"]) / (config["map_max_x"] - config["map_min_x"])
        norm_y = (map_y - config["map_min_y"]) / (config["map_max_y"] - config["map_min_y"])

        # Konvertiere zu Bildschirm
        area = config["screen_game_area"]
        screen_x = area["x"] + norm_x * area["width"]
        screen_y = area["y"] + norm_y * area["height"]

        # Offset hinzufügen
        screen_x += GAME_WINDOW["offset_x"]
        screen_y += GAME_WINDOW["offset_y"]

        return int(screen_x), int(screen_y)

    def press_keys(self, keys: List[str]):
        """Drückt eine Sequenz von Tasten"""
        if not PYAUTOGUI_AVAILABLE:
            print(f"  [SIMULATION] Tasten: {keys}")
            return

        for key in keys:
            pyautogui.press(key)
            time.sleep(TIMING["key_delay"])

    def click_at(self, x: int, y: int, button: str = "left"):
        """Klickt an einer Bildschirm-Position"""
        if not PYAUTOGUI_AVAILABLE:
            print(f"  [SIMULATION] Klick: ({x}, {y})")
            return

        pyautogui.click(x, y, button=button)
        time.sleep(TIMING["click_delay"])

    def execute_action(self, action: Dict) -> bool:
        """
        Führt eine einzelne Aktion aus

        Returns:
            True wenn erfolgreich
        """
        action_name = action["action"]
        time_str = action["time_formatted"]

        print(f"\n[{time_str}] Ausführe: {action_name}")

        # Gebäude bauen
        if action_name.startswith("build_"):
            building = action_name.replace("build_", "")
            return self._build_building(building)

        # Technologie forschen
        elif action_name.startswith("research_"):
            tech = action_name.replace("research_", "")
            return self._research_tech(tech)

        # Arbeiter zuweisen
        elif action_name.startswith("worker_add_"):
            resource = action_name.replace("worker_add_", "")
            return self._assign_worker(resource, add=True)

        elif action_name.startswith("worker_remove_"):
            resource = action_name.replace("worker_remove_", "")
            return self._assign_worker(resource, add=False)

        # HQ upgraden
        elif action_name == "upgrade_hq":
            return self._upgrade_hq()

        # Scharfschütze rekrutieren
        elif action_name == "recruit_scharfschuetze":
            return self._recruit_scharfschuetze()

        # Unbekannte Aktion
        else:
            print(f"  WARNUNG: Unbekannte Aktion: {action_name}")
            return False

    def _build_building(self, building: str) -> bool:
        """Baut ein Gebäude"""
        # Finde Position für dieses Gebäude
        position = None
        for bp in self.building_positions:
            if bp["building"] == building and "used" not in bp:
                position = bp["position"]
                bp["used"] = True
                break

        if position is None:
            print(f"  WARNUNG: Keine Position für {building} gefunden!")
            return False

        # Hotkeys drücken
        keys = self.hotkeys["buildings"].get(building)
        if keys:
            self.press_keys(keys)
            time.sleep(TIMING["action_delay"])

        # An Position klicken
        screen_x, screen_y = self.map_to_screen(position["x"], position["y"])
        print(f"  Position: Map({position['x']}, {position['y']}) -> Screen({screen_x}, {screen_y})")
        self.click_at(screen_x, screen_y)

        time.sleep(TIMING["build_confirm_delay"])
        return True

    def _research_tech(self, tech: str) -> bool:
        """Forscht eine Technologie"""
        keys = self.hotkeys["technologies"].get(tech)
        if keys:
            self.press_keys(keys)
            print(f"  Forschung gestartet: {tech}")
            return True
        return False

    def _assign_worker(self, resource: str, add: bool) -> bool:
        """Weist einen Arbeiter zu oder entfernt ihn"""
        # Diese Funktion ist komplex im echten Spiel
        # Muss über das Arbeiter-Menü gemacht werden
        action = "hinzufügen" if add else "entfernen"
        print(f"  Arbeiter {action} für {resource}")
        print(f"  [MANUELL] Bitte Arbeiter manuell {action}!")
        return True

    def _upgrade_hq(self) -> bool:
        """Upgraded das Hauptquartier"""
        keys = self.hotkeys["hq_upgrade"]
        self.press_keys(keys)
        print("  HQ Upgrade gestartet")
        return True

    def _recruit_scharfschuetze(self) -> bool:
        """Rekrutiert einen Scharfschützen"""
        keys = self.hotkeys["units"].get("Scharfschütze")
        if keys:
            self.press_keys(keys)
            print("  Scharfschütze rekrutiert")
            return True
        return False

    def run(self, dry_run: bool = True):
        """
        Führt die komplette Strategie aus

        Args:
            dry_run: Wenn True, werden keine echten Eingaben gemacht
        """
        print("\n" + "=" * 60)
        print("SIEDLER 5 - GAME BRIDGE")
        print("=" * 60)
        print(f"Karte: {self.strategy['map']}")
        print(f"Spieler: {self.strategy['player']}")
        print(f"Aktionen: {len(self.actions)}")
        print(f"Dry Run: {dry_run}")
        print("=" * 60)

        if dry_run:
            print("\n[DRY RUN MODUS - Keine echten Eingaben]")
            global PYAUTOGUI_AVAILABLE
            PYAUTOGUI_AVAILABLE = False

        input("\nDrücke ENTER wenn das Spiel bereit ist...")

        self.game_start_time = time.time()
        last_action_time = 0

        for i, action in enumerate(self.actions):
            self.current_action_idx = i

            # Warte bis zur richtigen Zeit
            target_time = action["time_seconds"]
            wait_time = target_time - last_action_time

            if wait_time > 0:
                print(f"\nWarte {wait_time} Sekunden...")
                time.sleep(wait_time if not dry_run else 0.1)

            # Aktion ausführen
            self.execute_action(action)
            last_action_time = target_time

        print("\n" + "=" * 60)
        print("STRATEGIE ABGESCHLOSSEN!")
        print("=" * 60)
        print(f"Erwartete Scharfschützen: {self.strategy['final_scharfschuetzen']}")


# =============================================================================
# KALIBRIERUNG
# =============================================================================

def calibrate_screen():
    """
    Hilft bei der Kalibrierung der Bildschirm-Koordinaten

    Führe diese Funktion aus um die MAP_TO_SCREEN Werte zu ermitteln.
    """
    if not PYAUTOGUI_AVAILABLE:
        print("pyautogui nicht verfügbar!")
        return

    print("=" * 60)
    print("BILDSCHIRM KALIBRIERUNG")
    print("=" * 60)
    print("\nBewege die Maus zu verschiedenen Punkten im Spiel.")
    print("Drücke STRG+C zum Beenden.\n")

    try:
        while True:
            x, y = pyautogui.position()
            print(f"Maus-Position: ({x}, {y})    ", end="\r")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\nKalibrierung beendet.")


# =============================================================================
# HAUPTPROGRAMM
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Siedler 5 Game Bridge")
    parser.add_argument("--strategy", "-s", default="./siedler_training/strategy.json",
                        help="Pfad zur strategy.json")
    parser.add_argument("--calibrate", "-c", action="store_true",
                        help="Kalibrierungsmodus starten")
    parser.add_argument("--dry-run", "-d", action="store_true",
                        help="Dry Run (keine echten Eingaben)")
    parser.add_argument("--live", "-l", action="store_true",
                        help="Live Modus (echte Eingaben)")

    args = parser.parse_args()

    if args.calibrate:
        calibrate_screen()
    else:
        if not os.path.exists(args.strategy):
            print(f"FEHLER: strategy.json nicht gefunden: {args.strategy}")
            print("Führe zuerst das Training aus!")
            exit(1)

        bridge = GameBridge(args.strategy)

        if args.live:
            print("\n⚠️  LIVE MODUS - Echte Eingaben werden gemacht!")
            confirm = input("Bist du sicher? (ja/nein): ")
            if confirm.lower() == "ja":
                bridge.run(dry_run=False)
            else:
                print("Abgebrochen.")
        else:
            bridge.run(dry_run=True)
