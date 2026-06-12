"""
Siedler 5 - Data Extractor
Extrahiert alle Spieldaten aus den XML-Dateien des Spiels.

Verwendung:
    python data_extractor.py --game-path "C:/Users/marku/OneDrive/Desktop/Gold edition"

Ausgabe:
    config/game_data.json - Alle extrahierten Spieldaten
"""

import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional
import re
import argparse


class SiedlerDataExtractor:
    """Extrahiert alle relevanten Spieldaten aus den XML-Dateien."""

    def __init__(self, game_path: str):
        self.game_path = Path(game_path)
        self.data = {
            "workers": {},
            "buildings": {},
            "technologies": {},
            "units": {},
            "heroes": {},
            "cannons": {},
            "resources": ["Gold", "Wood", "Stone", "Clay", "Iron", "Sulfur"],
            "constants": {},
            "logic": {},  # NEU: Zahltag, Steuern, Motivation, etc.
            "scharfschuetzen_path": {},  # NEU: Kritischer Pfad für Training
        }

        # Worker-Dateien (werden separat extrahiert)
        self.worker_files = [
            ("serf", "pu_serf.xml"),
            ("farmer", "pu_farmer.xml"),
            ("miner", "pu_miner.xml"),
            ("sawmillworker", "pu_sawmillworker.xml"),
            ("stonecutter", "pu_stonecutter.xml"),
            ("smith", "pu_smith.xml"),
            ("alchemist", "pu_alchemist.xml"),
            ("priest", "pu_priest.xml"),
            ("treasurer", "pu_treasurer.xml"),
            ("trader", "pu_trader.xml"),
            ("smelter", "pu_smelter.xml"),
        ]

        # Config-Pfade (base/extra1/extra2)
        self.config_paths = [
            self.game_path / "base/shr/config",
            self.game_path / "extra1/shr/config",
            self.game_path / "extra2/shr/config",
        ]

        # Pfade zu den Config-Ordnern (inkl. extra2!)
        self.entity_paths = [
            self.game_path / "base/shr/config/entities",
            self.game_path / "extra1/shr/config/entities",
            self.game_path / "extra2/shr/config/entities",
        ]
        self.tech_paths = [
            self.game_path / "base/shr/config/technologies",
            self.game_path / "extra1/shr/config/technologies",
            self.game_path / "extra2/shr/config/technologies",
        ]
        self.logic_paths = [
            self.game_path / "extra2/shr/config/logic.xml",
        ]

        # Erlaubte Entities aus Entities.xml (nur Original-Entitaeten)
        self.allowed_entities = self._load_allowed_entities()

    def extract_all(self) -> Dict[str, Any]:
        """Extrahiert alle Daten."""
        print("Starte Daten-Extraktion...")

        self._extract_workers()
        self._extract_buildings()
        self._extract_technologies()
        self._extract_military_units()
        self._extract_heroes()
        self._extract_cannons()
        self._extract_other_units()
        self._extract_logic_params()  # NEU!
        self._extract_scharfschuetzen_path()  # NEU!
        self._extract_constants()

        print(f"\n=== Extraktion abgeschlossen ===")
        print(f"  - {len(self.data['workers'])} Worker-Typen")
        print(f"  - {len(self.data['buildings'])} Gebäude")
        print(f"  - {len(self.data['technologies'])} Technologien")
        print(f"  - {len(self.data['units'])} Einheiten")
        print(f"  - {len(self.data['heroes'])} Helden")
        print(f"  - {len(self.data['cannons'])} Kanonen")
        print(f"  - {len(self.data['logic'])} Logic-Parameter")
        print(f"  - Scharfschützen-Pfad: {len(self.data['scharfschuetzen_path'])} Einträge")

        return self.data

    def _parse_xml(self, filepath: Path) -> Optional[ET.Element]:
        """Parst eine XML-Datei sicher."""
        try:
            tree = ET.parse(filepath)
            return tree.getroot()
        except Exception as e:
            # Einige XMLs haben BOM oder andere Encoding-Probleme
            try:
                with open(filepath, 'r', encoding='utf-8-sig') as f:
                    content = f.read()
                return ET.fromstring(content)
            except:
                return None

    def _load_allowed_entities(self) -> set:
        """Lädt erlaubte Entity-IDs aus Entities.xml (base+extra1+extra2)."""
        allowed = set()
        for cfg in self.config_paths:
            entities_xml = cfg / "Entities.xml"
            if not entities_xml.exists():
                continue
            root = self._parse_xml(entities_xml)
            if root is None:
                continue
            for ent in root.findall(".//Entity"):
                if ent.text:
                    allowed.add(ent.text.strip().upper())
        return allowed

    def _get_text(self, element: ET.Element, path: str, default: str = "") -> str:
        """Holt Text aus einem XML-Element."""
        el = element.find(path)
        if el is not None and el.text:
            return el.text.strip()
        return default

    def _get_float(self, element: ET.Element, path: str, default: float = 0.0) -> float:
        """Holt Float-Wert aus einem XML-Element."""
        text = self._get_text(element, path)
        if text:
            # Entferne 'f' suffix (z.B. "250.0f")
            text = text.replace('f', '').replace('F', '')
            try:
                return float(text)
            except:
                pass
        return default

    def _get_int(self, element: ET.Element, path: str, default: int = 0) -> int:
        """Holt Integer-Wert aus einem XML-Element."""
        return int(self._get_float(element, path, default))

    def _extract_cost(self, element: ET.Element, cost_path: str = "Cost") -> Dict[str, int]:
        """Extrahiert Kosten aus einem Element."""
        cost = {}
        cost_el = element.find(cost_path)
        if cost_el is not None:
            for resource in ["Gold", "Wood", "Stone", "Clay", "Iron", "Sulfur"]:
                val = self._get_int(cost_el, resource)
                if val > 0:
                    cost[resource.lower()] = val
        return cost

    def _extract_xy(self, element: ET.Element, path: str) -> Optional[Dict[str, int]]:
        """Extrahiert X/Y-Koordinaten aus einem Unterelement."""
        xy_el = element.find(path)
        if xy_el is None:
            return None
        return {
            "x": self._get_int(xy_el, "X", 0),
            "y": self._get_int(xy_el, "Y", 0),
        }

    def _extract_builder_slots(self, construction: ET.Element) -> List[Dict[str, Any]]:
        """Extrahiert BuilderSlot-Positionen einer ConstructionInfo."""
        slots: List[Dict[str, Any]] = []
        for slot in construction.findall("BuilderSlot"):
            pos = self._extract_xy(slot, "Position")
            if pos is None:
                continue
            slots.append(
                {
                    "position": pos,
                    "orientation": self._get_int(slot, "Orientation", 0),
                }
            )
        return slots

    # ==================== WORKERS ====================

    def _extract_workers(self):
        """Extrahiert alle Worker-Daten."""
        print("  Extrahiere Worker...")

        for worker_name, filename in self.worker_files:
            for entity_path in self.entity_paths:
                filepath = entity_path / filename
                if filepath.exists():
                    self._parse_worker(worker_name, filepath)
                    break

    def _parse_worker(self, name: str, filepath: Path):
        """Parst eine Worker-XML-Datei."""
        if filepath.stem.upper() not in self.allowed_entities:
            return
        root = self._parse_xml(filepath)
        if root is None:
            return

        worker = {
            "name": name,
            "speed": 320,  # Default
            "has_worktime_system": name != "serf",  # Serfs haben KEIN WorkTime!
            "worktime": {},
        }

        # Logic-Daten
        logic = root.find("Logic")
        if logic is not None:
            worker["max_health"] = self._get_int(logic, "MaxHealth", 100)
            worker["exploration"] = self._get_int(logic, "Exploration", 10)

        # Movement-Behavior für Speed
        for behavior in root.findall("Behavior"):
            logic_el = behavior.find("Logic")
            if logic_el is not None:
                classname = logic_el.get("classname", "")

                # Speed aus Movement
                if "MovementBehavior" in classname:
                    worker["speed"] = self._get_int(logic_el, "Speed", 320)

                # WorkTime-System aus WorkerBehavior
                if "WorkerBehavior" in classname:
                    worker["worktime"] = {
                        "work_wait_until": self._get_int(logic_el, "WorkWaitUntil", 0),
                        "eat_wait": self._get_int(logic_el, "EatWait", 2000),
                        "rest_wait": self._get_int(logic_el, "RestWait", 3000),
                        "work_time_change_work": self._get_int(logic_el, "WorkTimeChangeWork", -50),
                        "work_time_change_farm": self._get_float(logic_el, "WorkTimeChangeFarm", 0.7),
                        "work_time_change_residence": self._get_float(logic_el, "WorkTimeChangeResidence", 0.5),
                        "work_time_change_camp": self._get_float(logic_el, "WorkTimeChangeCamp", 0.1),
                        "work_time_max_farm": self._get_int(logic_el, "WorkTimeMaxChangeFarm", 100),
                        "work_time_max_residence": self._get_int(logic_el, "WorkTimeMaxChangeResidence", 400),
                        "exhausted_malus": self._get_float(logic_el, "ExhaustedWorkMotivationMalus", 0.1),
                    }
                    worker["has_worktime_system"] = True

                # Camper-Range
                if "CamperBehavior" in classname:
                    worker["camper_range"] = self._get_int(logic_el, "Range", 5000)

                # Serf-spezifische Extraktion
                if "SerfBehavior" in classname:
                    worker["extraction"] = {
                        "search_radius": self._get_int(logic_el, "ResourceSearchRadius", 4500),
                    }

        self.data["workers"][name] = worker

    # ==================== BUILDINGS ====================

    def _extract_buildings(self):
        """Extrahiert alle Gebäude-Daten."""
        print("  Extrahiere Gebäude...")

        for entity_path in self.entity_paths:
            if not entity_path.exists():
                continue

            for filepath in entity_path.glob("pb_*.xml"):
                self._parse_building(filepath)

    def _parse_building(self, filepath: Path):
        """Parst eine Gebäude-XML-Datei."""
        if filepath.stem.upper() not in self.allowed_entities:
            return
        root = self._parse_xml(filepath)
        if root is None:
            return

        name = filepath.stem  # z.B. "pb_farm1"

        building = {
            "name": name,
            "categories": [],
            "cost": {},
            "build_time": 0,
            "max_health": 0,
            "armor": 0,
            "max_workers": 0,
            "worker_type": None,
            "upgrade": None,
            "behaviors": [],
            "blocked1": None,
            "blocked2": None,
            "terrain_pos1": None,
            "terrain_pos2": None,
            "approach_pos": None,
            "door_pos": None,
            "leave_pos": None,
            "footprint": None,
            "builder_slots": [],
        }

        # Logic-Daten
        logic = root.find("Logic")
        if logic is not None:
            building["max_health"] = self._get_int(logic, "MaxHealth", 1000)
            building["armor"] = self._get_int(logic, "ArmorAmount", 0)
            building["exploration"] = self._get_int(logic, "Exploration", 20)
            building["max_workers"] = self._get_int(logic, "MaxWorkers", 0)
            building["worker_type"] = self._get_text(logic, "Worker")
            building["build_on"] = self._get_text(logic, "BuildOn")
            building["approach_pos"] = self._extract_xy(logic, "ApproachPos")
            building["door_pos"] = self._extract_xy(logic, "DoorPos")
            building["leave_pos"] = self._extract_xy(logic, "LeavePos")
            building["blocked1"] = self._extract_xy(logic, "Blocked1")
            building["blocked2"] = self._extract_xy(logic, "Blocked2")
            building["terrain_pos1"] = self._extract_xy(logic, "TerrainPos1")
            building["terrain_pos2"] = self._extract_xy(logic, "TerrainPos2")
            if building["blocked1"] and building["blocked2"]:
                building["footprint"] = {
                    "width": abs(building["blocked2"]["x"] - building["blocked1"]["x"]),
                    "height": abs(building["blocked2"]["y"] - building["blocked1"]["y"]),
                }

            # Kategorien
            for cat in logic.findall("Category"):
                if cat.text:
                    building["categories"].append(cat.text.strip())

            # Baukosten und -zeit
            constr = logic.find("ConstructionInfo")
            if constr is not None:
                building["build_time"] = self._get_int(constr, "Time", 60)
                building["cost"] = self._extract_cost(constr)
                building["builder_slots"] = self._extract_builder_slots(constr)

            # Upgrade-Info
            upgrade = logic.find("Upgrade")
            if upgrade is not None:
                upgrade_type = self._get_text(upgrade, "Type")
                if upgrade_type:
                    building["upgrade"] = {
                        "to": upgrade_type,
                        "time": self._get_int(upgrade, "Time", 30),
                        "cost": self._extract_cost(upgrade),
                    }

        # Behaviors extrahieren
        for behavior in root.findall("Behavior"):
            logic_el = behavior.find("Logic")
            if logic_el is not None:
                class_name = self._get_text(logic_el, "Class")
                if class_name:
                    behavior_info = {"class": class_name}

                    # Mine-Behavior
                    if "MineBehavior" in class_name:
                        behavior_info["amount_to_mine"] = self._get_int(logic_el, "AmountToMine", 4)
                        behavior_info["resource_type"] = self._get_text(logic_el, "ResourceType")
                        building["behaviors"].append(behavior_info)

                    # Refiner-Behavior
                    elif "ResourceRefiner" in class_name:
                        behavior_info["resource_type"] = self._get_text(logic_el, "ResourceType")
                        behavior_info["initial_factor"] = self._get_int(logic_el, "InitialFactor", 4)
                        behavior_info["supplier_category"] = self._get_text(logic_el, "SupplierCategory")
                        building["behaviors"].append(behavior_info)

                    # Farm-Attachment (Essen-Kapazität)
                    elif "LimitedAttachment" in class_name:
                        for attach in logic_el.findall("Attachment"):
                            attach_type = self._get_text(attach, "Type")
                            limit = self._get_int(attach, "Limit", 0)
                            if "FARM" in attach_type.upper():
                                building["eat_capacity"] = limit
                            elif "RESIDENCE" in attach_type.upper():
                                building["live_capacity"] = limit
                            elif "DEFENDER" in attach_type.upper():
                                building["defender_capacity"] = limit

                    # Motivation-Effekt (Kloster)
                    elif "AffectMotivation" in class_name:
                        behavior_info["motivation_effect"] = self._get_float(logic_el, "MotivationEffect", 0)
                        building["behaviors"].append(behavior_info)

                    # Foundry (Kanonen)
                    elif "Foundry" in class_name:
                        cannons = []
                        for cannon_info in logic_el.findall("CannonInfo"):
                            cannons.append(self._get_text(cannon_info, "Cannon"))
                        behavior_info["cannons"] = cannons
                        building["behaviors"].append(behavior_info)

        self.data["buildings"][name] = building

    # ==================== TECHNOLOGIES ====================

    def _extract_technologies(self):
        """Extrahiert alle Technologie-Daten."""
        print("  Extrahiere Technologien...")

        # Nur Technologien, die in Technologies.xml gelistet sind (base+extra1+extra2)
        allowed = set()
        tech_lists = [
            self.game_path / "base/shr/config/Technologies.xml",
            self.game_path / "extra1/shr/config/Technologies.xml",
            self.game_path / "extra2/shr/config/Technologies.xml",
        ]
        for tech_list in tech_lists:
            if not tech_list.exists():
                continue
            root = self._parse_xml(tech_list)
            if root is None:
                continue
            for tech in root.findall(".//Technology"):
                if tech.text:
                    allowed.add(tech.text.strip().lower())

        for tech_path in self.tech_paths:
            if not tech_path.exists():
                continue

            for filepath in tech_path.glob("*.xml"):
                if filepath.stem.lower() not in allowed:
                    continue
                self._parse_technology(filepath)

    def _parse_technology(self, filepath: Path):
        """Parst eine Technologie-XML-Datei."""
        root = self._parse_xml(filepath)
        if root is None:
            return

        name = filepath.stem  # z.B. "gt_mathematics"

        tech = {
            "name": name,
            "category": self._get_text(root, "TecCategoryType", "TC_Technologies"),
            "time": self._get_int(root, "TimeToResearch", 30),
            "cost": {},
            "conditions": [],
            "effects": [],
            "required_entity_conditions": None,
        }

        # Kosten
        costs = root.find("ResourceCosts")
        if costs is not None:
            for resource in ["Gold", "Wood", "Stone", "Clay", "Iron", "Sulfur"]:
                val = self._get_int(costs, resource)
                if val > 0:
                    tech["cost"][resource.lower()] = val

        # Bedingungen
        conditions = root.find("Conditions")
        if conditions is not None:
            required_entities = self._get_int(conditions, "RequiredEntityConditions", 0)
            if required_entities > 0:
                tech["required_entity_conditions"] = required_entities

            # Tech-Bedingungen
            for tec_cond in conditions.findall("TecCondition"):
                req_tech = self._get_text(tec_cond, "TecType")
                if req_tech:
                    tech["conditions"].append({"type": "technology", "value": req_tech})

            # Entity-Bedingungen
            for entity_cond in conditions.findall("EntityCondition"):
                entity_type = self._get_text(entity_cond, "EntityType")
                amount = self._get_int(entity_cond, "Amount", 1)
                if entity_type:
                    tech["conditions"].append({
                        "type": "building",
                        "value": entity_type,
                        "amount": amount
                    })

        self.data["technologies"][name] = tech

    # ==================== MILITARY UNITS ====================

    def _extract_military_units(self):
        """Extrahiert alle Militär-Einheiten."""
        print("  Extrahiere Militär-Einheiten...")

        unit_patterns = [
            "pu_leaderbow*.xml",
            "pu_leadersword*.xml",
            "pu_leaderspear*.xml",
            "pu_leaderrifle*.xml",
            "pu_leaderlightcavalry*.xml",
            "pu_leaderheavycavalry*.xml",
        ]

        for entity_path in self.entity_paths:
            if not entity_path.exists():
                continue

            for pattern in unit_patterns:
                for filepath in entity_path.glob(pattern):
                    unit = self._parse_unit(filepath)
                    if unit:
                        self.data["units"][unit["name"]] = unit

    def _parse_unit(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Parst eine Einheiten-XML-Datei (Leader/Soldier/sonstige)."""
        if filepath.stem.upper() not in self.allowed_entities:
            return None
        root = self._parse_xml(filepath)
        if root is None:
            return None

        name = filepath.stem

        unit = {
            "name": name,
            "cost": {},
            "max_health": 0,
            "armor": 0,
            "damage": 0,
            "max_range": 0,
            "speed": 0,
            "soldier_type": "",
            "attachment_limit": 0,
            "max_random_damage": 0,
            "min_range": 0.0,
            "miss_chance": 0,
        }

        # Logic-Daten
        logic = root.find("Logic")
        if logic is not None:
            unit["max_health"] = self._get_int(logic, "MaxHealth", 100)
            unit["armor"] = self._get_int(logic, "ArmorAmount", 0)
            unit["cost"] = self._extract_cost(logic)

        # Behaviors
        for behavior in root.findall("Behavior"):
            logic_el = behavior.find("Logic")
            if logic_el is not None:
                classname = logic_el.get("classname", "")

                # Movement
                if "Movement" in classname:
                    unit["speed"] = self._get_int(logic_el, "Speed", 360)

                # Leader- oder Soldier-Behavior
                if "LeaderBehavior" in classname or "SoldierBehavior" in classname:
                    unit["damage"] = self._get_int(logic_el, "DamageAmount", 10)
                    unit["max_random_damage"] = self._get_int(logic_el, "MaxRandomDamageBonus", unit["max_random_damage"])
                    unit["max_range"] = self._get_float(logic_el, "MaxRange", 250)
                    unit["min_range"] = self._get_float(logic_el, "MinRange", unit["min_range"])
                    unit["miss_chance"] = self._get_int(logic_el, "MissChance", unit["miss_chance"])
                    soldier_type = self._get_text(logic_el, "SoldierType")
                    if soldier_type:
                        unit["soldier_type"] = soldier_type

                # Attachment-Limit
                if "LimitedAttachment" in classname:
                    for attach in logic_el.findall("Attachment"):
                        if "SOLDIER" in self._get_text(attach, "Type").upper():
                            unit["attachment_limit"] = self._get_int(attach, "Limit", 4)

        return unit

    # ==================== HEROES ====================

    def _extract_heroes(self):
        """Extrahiert alle Helden-Daten."""
        print("  Extrahiere Helden...")

        for entity_path in self.entity_paths:
            if not entity_path.exists():
                continue

            for filepath in entity_path.glob("pu_hero*.xml"):
                self._parse_hero(filepath)

    def _parse_hero(self, filepath: Path):
        """Parst eine Helden-XML-Datei."""
        if filepath.stem.upper() not in self.allowed_entities:
            return
        root = self._parse_xml(filepath)
        if root is None:
            return

        name = filepath.stem

        hero = {
            "name": name,
            "max_health": 600,
            "armor": 0,
            "damage": 0,
            "speed": 400,
            "abilities": [],
        }

        # Logic
        logic = root.find("Logic")
        if logic is not None:
            hero["max_health"] = self._get_int(logic, "MaxHealth", 600)
            hero["armor"] = self._get_int(logic, "ArmorAmount", 3)
            hero["exploration"] = self._get_int(logic, "Exploration", 22)

        # Behaviors / Abilities
        for behavior in root.findall("Behavior"):
            logic_el = behavior.find("Logic")
            if logic_el is not None:
                classname = logic_el.get("classname", "")
                class_text = self._get_text(logic_el, "Class")

                # Speed
                if "Movement" in classname:
                    hero["speed"] = self._get_int(logic_el, "Speed", 400)

                # Damage
                if "LeaderBehavior" in classname:
                    hero["damage"] = self._get_int(logic_el, "DamageAmount", 16)
                    hero["max_random_damage"] = self._get_int(logic_el, "MaxRandomDamageBonus", 4)
                    hero["max_range"] = self._get_float(logic_el, "MaxRange", 250)

                # Abilities
                if "Hawk" in class_text:
                    hero["abilities"].append({
                        "type": "hawk",
                        "cooldown": self._get_int(logic_el, "RechargeTimeSeconds", 60)
                    })
                elif "BombPlacer" in class_text:
                    hero["abilities"].append({
                        "type": "bomb_placer",
                        "cooldown": self._get_int(logic_el, "RechargeTimeSeconds", 60)
                    })
                elif "CannonBuilder" in class_text:
                    hero["abilities"].append({
                        "type": "cannon_builder",
                        "cooldown": self._get_int(logic_el, "RechargeTimeSeconds", 180)
                    })
                elif "RangedEffectAbility" in class_text:
                    hero["abilities"].append({
                        "type": "ranged_effect",
                        "cooldown": self._get_int(logic_el, "RechargeTimeSeconds", 120),
                        "range": self._get_float(logic_el, "Range", 1000),
                        "duration": self._get_int(logic_el, "DurationInSeconds", 60),
                        "damage_factor": self._get_float(logic_el, "DamageFactor", 1.0),
                        "armor_factor": self._get_float(logic_el, "ArmorFactor", 1.0),
                        "health_recovery": self._get_float(logic_el, "HealthRecoveryFactor", 0),
                    })
                elif "CircularAttack" in class_text:
                    hero["abilities"].append({
                        "type": "circular_attack",
                        "cooldown": self._get_int(logic_el, "RechargeTimeSeconds", 120),
                        "damage": self._get_int(logic_el, "DamageAmount", 80),
                        "range": self._get_float(logic_el, "Range", 400),
                    })
                elif "Camouflage" in class_text:
                    hero["abilities"].append({
                        "type": "camouflage",
                        "cooldown": self._get_int(logic_el, "RechargeTimeSeconds", 180),
                        "duration": self._get_int(logic_el, "DurationSeconds", 90),
                    })
                elif "Summon" in class_text:
                    hero["abilities"].append({
                        "type": "summon",
                        "cooldown": self._get_int(logic_el, "RechargeTimeSeconds", 180),
                        "count": self._get_int(logic_el, "NumberOfSummonedEntities", 3),
                    })
                elif "ConvertSettler" in class_text:
                    hero["abilities"].append({
                        "type": "convert_settler",
                        "cooldown": self._get_int(logic_el, "RechargeTimeSeconds", 60),
                        "start_range": self._get_float(logic_el, "ConversionStartRange", 1400),
                        "max_range": self._get_float(logic_el, "ConversionMaxRange", 2800),
                    })

        self.data["heroes"][name] = hero

    # ==================== CANNONS ====================

    def _extract_cannons(self):
        """Extrahiert alle Kanonen-Daten."""
        print("  Extrahiere Kanonen...")

        for entity_path in self.entity_paths:
            if not entity_path.exists():
                continue

            for filepath in entity_path.glob("pv_cannon*.xml"):
                self._parse_cannon(filepath)

    def _parse_cannon(self, filepath: Path):
        """Parst eine Kanonen-XML-Datei."""
        if filepath.stem.upper() not in self.allowed_entities:
            return
        root = self._parse_xml(filepath)
        if root is None:
            return

        name = filepath.stem

        cannon = {
            "name": name,
            "cost": {},
            "max_health": 190,
            "damage": 0,
            "damage_range": 0,
            "max_range": 0,
            "min_range": 0,
            "speed": 0,
            "upkeep": 20,
        }

        # Logic
        logic = root.find("Logic")
        if logic is not None:
            cannon["max_health"] = self._get_int(logic, "MaxHealth", 190)
            cannon["armor"] = self._get_int(logic, "ArmorAmount", 2)
            cannon["cost"] = self._extract_cost(logic)
            cannon["attraction_slots"] = self._get_int(logic, "AttractionSlots", 5)

        # Behaviors
        for behavior in root.findall("Behavior"):
            logic_el = behavior.find("Logic")
            if logic_el is not None:
                classname = logic_el.get("classname", "")

                if "Movement" in classname:
                    cannon["speed"] = self._get_int(logic_el, "Speed", 240)

                if "LeaderBehavior" in classname:
                    cannon["damage"] = self._get_int(logic_el, "DamageAmount", 30)
                    cannon["max_random_damage"] = self._get_int(logic_el, "MaxRandomDamageBonus", 8)
                    cannon["damage_range"] = self._get_int(logic_el, "DamageRange", 150)
                    cannon["max_range"] = self._get_float(logic_el, "MaxRange", 2400)
                    cannon["min_range"] = self._get_float(logic_el, "MinRange", 1000)
                    cannon["battle_wait"] = self._get_int(logic_el, "BattleWaitUntil", 3500)
                    cannon["upkeep"] = self._get_int(logic_el, "UpkeepCost", 20)
                    cannon["damage_class"] = self._get_text(logic_el, "DamageClass", "DC_Strike")

        self.data["cannons"][name] = cannon

    # ==================== SONSTIGE EINHEITEN ====================

    def _extract_other_units(self):
        """Extrahiert alle weiteren Einheiten (PU_*/PV_*), die nicht Worker/Held/Kanone sind."""
        print("  Extrahiere weitere Einheiten...")

        existing_units = {k.lower() for k in self.data["units"].keys()}
        existing_heroes = {k.lower() for k in self.data["heroes"].keys()}
        existing_cannons = {k.lower() for k in self.data["cannons"].keys()}

        worker_xml = {fname.replace(".xml", "").lower() for _, fname in self.worker_files}

        for entity_path in self.entity_paths:
            if not entity_path.exists():
                continue

            # PU_*
            for filepath in entity_path.glob("pu_*.xml"):
                name = filepath.stem.lower()
                if name in existing_units or name in existing_heroes or name in worker_xml:
                    continue
                unit = self._parse_unit(filepath)
                if unit:
                    self.data["units"][unit["name"]] = unit
                    existing_units.add(name)

            # PV_* (außer Kanonen)
            for filepath in entity_path.glob("pv_*.xml"):
                name = filepath.stem.lower()
                if name in existing_cannons or name in existing_units:
                    continue
                unit = self._parse_unit(filepath)
                if unit:
                    self.data["units"][unit["name"]] = unit
                    existing_units.add(name)

    # ==================== LOGIC PARAMETERS ====================

    def _extract_logic_params(self):
        """Extrahiert Spiel-Parameter aus extra2/shr/config/logic.xml."""
        print("  Extrahiere Logic-Parameter...")

        for logic_path in self.logic_paths:
            if not logic_path.exists():
                continue

            root = self._parse_xml(logic_path)
            if root is None:
                continue

            # Steuern
            tax_levels = []
            for tax_el in root.findall("TaxationLevel"):
                tax_levels.append({
                    "regular_tax": self._get_int(tax_el, "RegularTax", 10),
                    "motivation_change": self._get_float(tax_el, "MotivationChange", 0),
                })

            # Motivation
            motivation = {
                "threshold_happy": self._get_float(root, "MotivationThresholdHappy", 1.5),
                "threshold_sad": self._get_float(root, "MotivationThresholdSad", 1.0),
                "threshold_angry": self._get_float(root, "MotivationThresholdAngry", 0.7),
                "threshold_leave": self._get_float(root, "MotivationThresholdLeave", 0.25),
                "absolute_max": self._get_float(root, "MotivationAbsoluteMaxMotivation", 3.0),
                "game_start_max": self._get_float(root, "MotivationGameStartMaxMotivation", 1.0),
            }

            # WorkTime
            worktime = {
                "base": self._get_int(root, "WorkTimeBase", 125),
                "threshold_work": self._get_int(root, "WorkTimeThresholdWork", 25),
            }

            # Zahltag
            payday = {
                "tax_amount": self._get_int(root, "TaxAmount", 5),
                "initial_tax_level": self._get_int(root, "InitialTaxLevel", 2),
            }

            self.data["logic"] = {
                "tax_levels": tax_levels,
                "motivation": motivation,
                "worktime": worktime,
                "payday": payday,
            }

            break  # Nur erste logic.xml nutzen

    # ==================== SCHARFSCHÜTZEN-PFAD ====================

    def _extract_scharfschuetzen_path(self):
        """Extrahiert ALLE Werte für den Scharfschützen-Produktionspfad."""
        print("  Extrahiere Scharfschützen-Pfad (HÖCHSTE PRIORITÄT)...")

        path_data = {
            "soldiers": {},
            "buildings": {},
            "technologies": {},
        }

        # Scharfschützen (PU_LeaderRifle1.xml, PU_LeaderRifle2.xml)
        rifle_files = ["PU_LeaderRifle1.xml", "PU_LeaderRifle2.xml"]
        for filename in rifle_files:
            for entity_path in self.entity_paths:
                filepath = entity_path / filename
                if filepath.exists():
                    unit_data = self._parse_military_unit_detailed(filepath)
                    if unit_data:
                        path_data["soldiers"][filename.replace(".xml", "")] = unit_data
                    break

        # Büchsenmacherei (PB_GunsmithWorkshop1.xml, PB_GunsmithWorkshop2.xml)
        gunsmith_files = ["PB_GunsmithWorkshop1.xml", "PB_GunsmithWorkshop2.xml"]
        for filename in gunsmith_files:
            for entity_path in self.entity_paths:
                filepath = entity_path / filename
                if filepath.exists():
                    building_data = self._parse_building_detailed(filepath)
                    if building_data:
                        path_data["buildings"][filename.replace(".xml", "")] = building_data
                    break

        # Hochschule (PB_University1.xml, PB_University2.xml)
        uni_files = ["PB_University1.xml", "PB_University2.xml"]
        for filename in uni_files:
            for entity_path in self.entity_paths:
                filepath = entity_path / filename
                if filepath.exists():
                    building_data = self._parse_building_detailed(filepath)
                    if building_data:
                        path_data["buildings"][filename.replace(".xml", "")] = building_data
                    break

        # Technologien (in Technologies-Ordner als separate XMLs? Oder in Entities?)
        # HINWEIS: Technologien haben KEINE Effekte in den XMLs - nur Kosten/Zeiten!
        # Effekte sind wahrscheinlich im Code hardcodiert.

        self.data["scharfschuetzen_path"] = path_data

        # Zusammenfassung
        print(f"    - {len(path_data['soldiers'])} Scharfschuetzen-Einheiten")
        print(f"    - {len(path_data['buildings'])} Gebaeude (Buechsenmacherei, Hochschule)")
        print(f"    - {len(path_data['technologies'])} Technologien (falls vorhanden)")

    def _parse_building_detailed(self, filepath: Path) -> Dict[str, Any]:
        """Parst ein Gebäude mit ALLEN Details (für Scharfschützen-Pfad)."""
        root = self._parse_xml(filepath)
        if root is None:
            return None

        building = {
            "name": filepath.stem,
            "cost": {},
            "build_time": 0,
            "max_workers": 0,
            "max_health": 0,
            "upgrade": None,
        }

        logic = root.find("Logic")
        if logic is not None:
            building["max_health"] = self._get_int(logic, "MaxHealth", 1000)
            building["max_workers"] = self._get_int(logic, "MaxWorkers", 0)

            # Baukosten und -zeit
            constr = logic.find("ConstructionInfo")
            if constr is not None:
                building["build_time"] = self._get_int(constr, "Time", 60)
                building["cost"] = self._extract_cost(constr)

            # Upgrade-Info
            upgrade = logic.find("Upgrade")
            if upgrade is not None:
                building["upgrade"] = {
                    "to": self._get_text(upgrade, "Type"),
                    "time": self._get_int(upgrade, "Time", 30),
                    "cost": self._extract_cost(upgrade),
                }

        return building

    def _parse_military_unit_detailed(self, filepath: Path) -> Dict[str, Any]:
        """Parst eine Militär-Einheit mit ALLEN Details (für Scharfschützen-Pfad)."""
        root = self._parse_xml(filepath)
        if root is None:
            return None

        unit = {
            "name": filepath.stem,
            "cost": {},
            "training_time": 0,
            "max_health": 0,
            "armor": 0,
            "damage": 0,
            "max_range": 0,
            "speed": 0,
        }

        logic = root.find("Logic")
        if logic is not None:
            unit["max_health"] = self._get_int(logic, "MaxHealth", 100)
            unit["armor"] = self._get_int(logic, "ArmorAmount", 0)
            unit["cost"] = self._extract_cost(logic)

            # Trainingszeit (falls in Logic/ConstructionInfo)
            constr = logic.find("ConstructionInfo")
            if constr is not None:
                unit["training_time"] = self._get_int(constr, "Time", 20)

        # Behaviors
        for behavior in root.findall("Behavior"):
            logic_el = behavior.find("Logic")
            if logic_el is not None:
                classname = logic_el.get("classname", "")

                if "Movement" in classname:
                    unit["speed"] = self._get_int(logic_el, "Speed", 360)

                if "LeaderBehavior" in classname:
                    unit["damage"] = self._get_int(logic_el, "DamageAmount", 10)
                    unit["max_range"] = self._get_float(logic_el, "MaxRange", 250)

        return unit

    # ==================== CONSTANTS ====================

    def _extract_constants(self):
        """Extrahiert globale Spielkonstanten."""
        print("  Setze Konstanten...")

        self.data["constants"] = {
            # Radius-System
            "camper_range": 5000,
            "resource_search_radius": 4500,
            "home_radius": 1500,

            # WorkTime-System
            "work_time_default": 100,
            "work_time_max_residence": 400,
            "exhausted_efficiency": 0.1,

            # Serf-Extraktion
            "serf_extraction": {
                "iron": {"delay": 3, "amount": 1},
                "stone": {"delay": 4, "amount": 1},
                "clay": {"delay": 4, "amount": 1},
                "sulfur": {"delay": 3, "amount": 1},
                "wood": {"delay": 4, "amount": 2},
            },

            # Bau-Konstanten
            "serf_build_cycle": 8.4,  # Sekunden pro Bau-Zyklus
            "repair_factor": 0.3,

            # Kapazitäten
            "residence_capacity": {1: 6, 2: 9, 3: 12},
            "farm_eat_capacity": {1: 8, 2: 10, 3: 12},
        }

    def save(self, output_path: str):
        """Speichert die extrahierten Daten als JSON."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

        print(f"\nDaten gespeichert: {output_file}")
        print(f"Dateigröße: {output_file.stat().st_size / 1024:.1f} KB")


def main():
    parser = argparse.ArgumentParser(description="Siedler 5 Data Extractor")
    parser.add_argument(
        "--game-path",
        default="C:/Users/marku/OneDrive/Desktop/Gold edition",
        help="Pfad zum Spielverzeichnis"
    )
    parser.add_argument(
        "--output",
        default="config/game_data.json",
        help="Ausgabedatei"
    )

    args = parser.parse_args()

    extractor = SiedlerDataExtractor(args.game_path)
    extractor.extract_all()
    extractor.save(args.output)


if __name__ == "__main__":
    main()
