# -*- coding: utf-8 -*-
"""
Settlers 5 engine decoder.

Reads XML config data directly from a Settlers 5 installation and writes
`config/engine_decoded.json` for the local RL environment.

Important:
- Supports layered config lookup (base + extra1 + extra2).
- Extracts worker/building/deposit data as before.
- Adds explicit pathfinding/camp/serf taskflow extraction.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional
import xml.etree.ElementTree as ET


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = SCRIPT_DIR / "config" / "engine_decoded.json"

DEFAULT_GAME_ROOT_CANDIDATES = [
    r"C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games\theSettlers5",
    r"C:\Users\marku\OneDrive\Desktop\Gold edition",
]


WORKER_FILES = [
    "PU_Serf.xml",
    "PU_Miner.xml",
    "PU_Farmer.xml",
    "PU_Sawmillworker.xml",
    "PU_Smith.xml",
    "PU_Alchemist.xml",
    "PU_Priest.xml",
    "PU_Stonecutter.xml",
    "PU_BrickMaker.xml",
    "PU_Smelter.xml",
    "PU_Trader.xml",
    "PU_Treasurer.xml",
    "PU_Scholar.xml",
    "PU_Engineer.xml",
    "PU_MasterBuilder.xml",
    "PU_Gunsmith.xml",
    "PU_TavernBarkeeper.xml",
    "PU_Coiner.xml",
]

BUILDING_PATTERNS = [
    "PB_Headquarters",
    "PB_VillageCenter",
    "PB_Residence",
    "PB_Farm",
    "PB_University",
    "PB_Blacksmith",
    "PB_Alchemist",
    "PB_Sawmill",
    "PB_StoneMason",
    "PB_Brickworks",
    "PB_Bank",
    "PB_Monastery",
    "PB_Market",
    "PB_Gunworks",
    "PB_Tavern",
    "PB_Foundry",
    "PB_Barracks",
    "PB_Archery",
    "PB_Stable",
    "PB_IronMine",
    "PB_StoneMine",
    "PB_ClayMine",
    "PB_SulfurMine",
    "PB_Tower",
    "PB_Beautification",
]

DEPOSIT_FILES = [
    "XD_IronPit1.xml",
    "XD_StonePit.xml",
    "XD_StonePit1.xml",
    "XD_ClayPit1.xml",
    "XD_SulfurPit1.xml",
    "XD_Iron1.xml",
    "XD_Stone1.xml",
    "XD_Clay1.xml",
    "XD_Sulfur1.xml",
    "XD_ResourceTree.xml",
]

TASKLIST_WORK_FILES = {
    "miner": "TL_MINER_WORK.xml",
    "sawmillworker": "TL_SAWMILLWORKER_WORK.xml",
    "smith": "TL_SMITH_WORK.xml",
    "alchemist": "TL_ALCHEMIST_WORK.xml",
    "brickmaker": "TL_BRICKMAKER_WORK.xml",
    "stonecutter": "TL_STONECUTTER_WORK.xml",
    "smelter": "TL_SMELTER_WORK1.xml",
    "farmer": "TL_FARMER_WORK.xml",
    "scholar": "TL_SCHOLAR_WORK.xml",
    "gunsmith": "TL_GUNSMITH_WORK.xml",
    "coiner": "TL_COINER_WORK.xml",
    "engineer": "TL_ENGINEER_WORK.xml",
    "priest": "TL_PRIEST_WORK.xml",
    "trader": "TL_TRADER_WORK.xml",
    "treasurer": "TL_TREASURER_WORK.xml",
    "tavernbarkeeper": "TL_TAVERNBARKEEPER_WORK.xml",
    "masterbuilder": "TL_MASTER_BUILDER_WORK1.xml",
}

TASKLIST_WORK_INSIDE_FILES = {
    "miner_inside": "TL_MINER_WORK_START.xml",
    "sawmillworker_inside": "TL_SAWMILLWORKER_WORK_INSIDE.xml",
    "smith_inside": "TL_SMITH_WORK_INSIDE.xml",
    "alchemist_inside": "TL_ALCHEMIST_WORK_INSIDE.xml",
    "brickmaker_inside": "TL_BRICKMAKER_WORK_INSIDE.xml",
}

MINE_TASKLIST_FILES = {
    "ironmine_work": "TL_MINER_IRONMINE_WORK.xml",
    "ironmine_work_inside": "TL_MINER_IRONMINE_WORK_INSIDE.xml",
    "stonemine_work": "TL_MINER_STONEMINE_WORK.xml",
    "stonemine_work_inside": "TL_MINER_STONEMINE_WORK_INSIDE.xml",
    "claymine_work": "TL_MINER_CLAYMINE_WORK.xml",
    "claymine_work_inside": "TL_MINER_CLAYMINE_WORK_INSIDE.xml",
    "sulfurmine_work": "TL_MINER_SULFURMINE_WORK.xml",
    "sulfurmine_work_inside": "TL_MINER_SULFURMINE_WORK_INSIDE.xml",
}

SERF_TASKLIST_FILES = {
    "serf_walk": "TL_SERF_WALK.xml",
    "serf_go_to_resource": "TL_SERF_GO_TO_RESOURCE.xml",
    "serf_go_to_tree": "TL_SERF_GO_TO_TREE.xml",
    "serf_extract_resource": "TL_SERF_EXTRACT_RESOURCE.xml",
    "serf_extract_wood": "TL_SERF_EXTRACT_WOOD.xml",
    "serf_go_to_construction_site": "TL_SERF_GO_TO_CONSTRUCTION_SITE.xml",
    "serf_build": "TL_SERF_BUILD.xml",
    "serf_idle": "TL_SERF_IDLE.xml",
}

WORKER_PATH_TASKLIST_FILES = {
    "worker_flee": "TL_WORKER_FLEE.xml",
    "worker_go_to_defendable_building": "TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml",
    "worker_leave": "TL_WORKER_LEAVE.xml",
    "generic_walk": "TL_WALK.xml",
}


def safe_float(text: Optional[str], default: float = 0.0) -> float:
    if text is None:
        return default
    text = text.strip().rstrip("f")
    try:
        return float(text)
    except (ValueError, TypeError):
        return default


def safe_int(text: Optional[str], default: int = 0) -> int:
    if text is None:
        return default
    text = text.strip()
    try:
        return int(float(text))
    except (ValueError, TypeError):
        return default


def safe_bool(text: Optional[str], default: bool = False) -> bool:
    if text is None:
        return default
    return text.strip().lower() in {"1", "true", "yes"}


def parse_xml_safe(filepath: Path) -> Optional[ET.Element]:
    try:
        content = filepath.read_text(encoding="utf-8-sig")
        return ET.fromstring(content)
    except ET.ParseError as exc:
        print(f"  WARNING: XML parse error in {filepath}: {exc}")
        return None
    except Exception as exc:
        print(f"  WARNING: failed to read {filepath}: {exc}")
        return None


def xy_from(parent: ET.Element, tag: str) -> Optional[Dict[str, int]]:
    elem = parent.find(tag)
    if elem is None:
        return None
    return {
        "x": safe_int(elem.findtext("X")),
        "y": safe_int(elem.findtext("Y")),
    }


@dataclass
class OverlayPaths:
    source_root: Path
    config_roots: List[Path]
    mode: str

    @staticmethod
    def _is_config_root(path: Path) -> bool:
        return (
            (path / "Logic.xml").exists()
            and (path / "Entities").exists()
            and (path / "TaskLists").exists()
        )

    @staticmethod
    def _layer_config_root(game_root: Path, layer: str) -> Optional[Path]:
        cfg = game_root / layer / "shr" / "config"
        return cfg if OverlayPaths._is_config_root(cfg) else None

    @classmethod
    def _from_candidate(cls, candidate: Path) -> Optional["OverlayPaths"]:
        if cls._is_config_root(candidate):
            return cls(
                source_root=candidate,
                config_roots=[candidate],
                mode="single_config_root",
            )

        layers = []
        for layer in ("extra2", "extra1", "base"):
            cfg = cls._layer_config_root(candidate, layer)
            if cfg is not None:
                layers.append(cfg)

        if layers:
            return cls(
                source_root=candidate,
                config_roots=layers,
                mode="layered_game_root",
            )
        return None

    @classmethod
    def detect(cls, user_path: Optional[str]) -> "OverlayPaths":
        candidates: List[Path] = []
        if user_path:
            candidates.append(Path(user_path))
        env_root = os.environ.get("SIEDLER5_ROOT")
        if env_root:
            candidates.append(Path(env_root))
        for default_root in DEFAULT_GAME_ROOT_CANDIDATES:
            candidates.append(Path(default_root))

        for candidate in candidates:
            resolved = cls._from_candidate(candidate)
            if resolved is not None:
                return resolved

        tried = "\n".join(f"  - {p}" for p in candidates)
        raise FileNotFoundError(
            "No valid Settlers 5 config root found.\n"
            "Checked candidates:\n"
            f"{tried}"
        )

    def resolve(self, *relative_parts: str) -> Optional[Path]:
        rel = Path(*relative_parts)
        for cfg in self.config_roots:
            full = cfg / rel
            if full.exists():
                return full
        return None

    def list_overlay_files(self, subdir: str, pattern: str) -> List[Path]:
        # base -> extra1 -> extra2 so newest layer wins by filename
        merged: Dict[str, Path] = {}
        for cfg in reversed(self.config_roots):
            folder = cfg / subdir
            if not folder.exists():
                continue
            for file in folder.glob(pattern):
                merged[file.name.lower()] = file
        return [merged[name] for name in sorted(merged)]

    def debug_info(self) -> Dict[str, object]:
        return {
            "mode": self.mode,
            "source_root": str(self.source_root),
            "config_roots": [str(p) for p in self.config_roots],
        }


def parse_worker(filepath: Path) -> Optional[Dict[str, object]]:
    root = parse_xml_safe(filepath)
    if root is None:
        return None

    data: Dict[str, object] = {"_file": filepath.name}
    logic = root.find(".//Logic[@classname='GGL::CGLSettlerProps']")
    if logic is None:
        logic = root.find(".//Logic")

    if logic is not None:
        data["max_health"] = safe_int(logic.findtext("MaxHealth"), 100)
        data["armor_class"] = (logic.findtext("ArmorClass") or "").strip()
        data["armor_amount"] = safe_int(logic.findtext("ArmorAmount"), 0)
        data["exploration"] = safe_int(logic.findtext("Exploration"), 10)
        data["category"] = (logic.findtext("Category") or "").strip()

        cost_elem = logic.find("Cost")
        if cost_elem is not None:
            cost: Dict[str, int] = {}
            for child in cost_elem:
                val = safe_int(child.text, 0)
                if val > 0:
                    cost[child.tag.lower()] = val
            data["cost"] = cost

        modify_speed = logic.find("ModifySpeed")
        if modify_speed is not None:
            data["speed_techs"] = [
                t.text.strip() for t in modify_speed.findall("Technology") if t.text
            ]

        modify_armor = logic.find("ModifyArmor")
        if modify_armor is not None:
            data["armor_techs"] = [
                t.text.strip() for t in modify_armor.findall("Technology") if t.text
            ]

    worker_tasklists: Dict[str, str] = {}

    for behavior in root.findall(".//Behavior"):
        logic_b = behavior.find("Logic")
        if logic_b is None:
            continue
        classname = logic_b.get("classname", "")

        if "CMovementBehaviorProps" in classname:
            data["speed"] = safe_int(logic_b.findtext("Speed"), 320)
            data["rotation_speed"] = safe_int(logic_b.findtext("RotationSpeed"), 30)
            move_task = (logic_b.findtext("MoveTaskList") or "").strip()
            if move_task:
                data["move_task_list"] = move_task

        if "CWorkerBehaviorProps" in classname:
            data["has_worktime"] = True
            data["work_wait_until"] = safe_int(logic_b.findtext("WorkWaitUntil"), 0)
            data["work_time_change_work"] = safe_int(
                logic_b.findtext("WorkTimeChangeWork"), -50
            )
            data["exhausted_malus"] = safe_float(
                logic_b.findtext("ExhaustedWorkMotivationMalus"), 0.2
            )
            data["eat_wait"] = safe_int(logic_b.findtext("EatWait"), 2000)
            data["rest_wait"] = safe_int(logic_b.findtext("RestWait"), 3000)
            data["work_time_change_farm"] = safe_float(
                logic_b.findtext("WorkTimeChangeFarm"), 0.7
            )
            data["work_time_change_residence"] = safe_float(
                logic_b.findtext("WorkTimeChangeResidence"), 0.5
            )
            data["work_time_change_camp"] = safe_float(
                logic_b.findtext("WorkTimeChangeCamp"), 0.1
            )
            data["work_time_max_farm"] = safe_int(
                logic_b.findtext("WorkTimeMaxChangeFarm"), 100
            )
            data["work_time_max_residence"] = safe_int(
                logic_b.findtext("WorkTimeMaxChangeResidence"), 400
            )
            data["amount_researched"] = safe_float(
                logic_b.findtext("AmountResearched"), 0
            )
            data["resource_to_refine"] = (logic_b.findtext("ResourceToRefine") or "").strip()
            data["transport_amount"] = safe_int(logic_b.findtext("TransportAmount"), 0)

            for tag in (
                "WorkTaskList",
                "WorkIdleTaskList",
                "EatTaskList",
                "EatIdleTaskList",
                "RestTaskList",
                "RestIdleTaskList",
                "LeaveTaskList",
            ):
                val = (logic_b.findtext(tag) or "").strip()
                if val:
                    worker_tasklists[tag] = val

        if "CSerfBehaviorProps" in classname:
            data["has_worktime"] = False
            data["resource_search_radius"] = safe_int(
                logic_b.findtext("ResourceSearchRadius"), 0
            )
            data["extraction_info"] = []
            for ext in logic_b.findall("ExtractionInfo"):
                data["extraction_info"].append(
                    {
                        "entity_type": (ext.findtext("ResourceEntityType") or "").strip(),
                        "delay": safe_int(ext.findtext("Delay"), 0),
                        "amount": safe_int(ext.findtext("Amount"), 1),
                    }
                )
            for tag in (
                "ApproachConstructionSiteTaskList",
                "TurnIntoBattleSerfTaskList",
            ):
                val = (logic_b.findtext(tag) or "").strip()
                if val:
                    worker_tasklists[tag] = val

        if "CCamperBehaviorProperties" in classname:
            data["camper_range"] = safe_int(logic_b.findtext("Range"), 5000)

        if "CWorkerAlarmModeBehaviorProps" in classname:
            val = (logic_b.findtext("GoToDefendableBuildingTaskList") or "").strip()
            if val:
                worker_tasklists["GoToDefendableBuildingTaskList"] = val

        if "CWorkerFleeBehaviorProps" in classname:
            val = (logic_b.findtext("FlightTaskList") or "").strip()
            if val:
                worker_tasklists["FlightTaskList"] = val

        if "CSerfBattleBehaviorProps" in classname:
            val = (logic_b.findtext("BattleTaskList") or "").strip()
            if val:
                worker_tasklists["BattleTaskList"] = val

    if worker_tasklists:
        data["tasklists"] = worker_tasklists

    return data


def parse_all_workers(paths: OverlayPaths) -> Dict[str, Dict[str, object]]:
    workers: Dict[str, Dict[str, object]] = {}
    for filename in WORKER_FILES:
        filepath = paths.resolve("Entities", filename)
        if filepath is None:
            print(f"  WARNING: worker file not found: {filename}")
            continue
        key = filepath.stem.replace("PU_", "").lower()
        print(f"  Parsing worker: {filepath.name}")
        data = parse_worker(filepath)
        if data:
            workers[key] = data
    return workers


def parse_building(filepath: Path) -> Optional[Dict[str, object]]:
    root = parse_xml_safe(filepath)
    if root is None:
        return None

    data: Dict[str, object] = {"_file": filepath.name}
    logic = root.find(".//Logic[@classname='GGL::CGLBuildingProps']")
    if logic is None:
        logic = root.find(".//Logic")
    if logic is None:
        return None

    data["max_health"] = safe_int(logic.findtext("MaxHealth"), 0)
    data["armor_class"] = (logic.findtext("ArmorClass") or "").strip()
    data["armor_amount"] = safe_int(logic.findtext("ArmorAmount"), 0)
    data["exploration"] = safe_int(logic.findtext("Exploration"), 0)
    data["categories"] = [
        cat.text.strip() for cat in logic.findall("Category") if cat.text
    ]

    data["worker_type"] = (logic.findtext("Worker") or "").strip()
    data["max_workers"] = safe_int(logic.findtext("MaxWorkers"), 0)
    data["initial_max_workers"] = safe_int(logic.findtext("InitialMaxWorkers"), 0)
    data["build_on"] = (logic.findtext("BuildOn") or "").strip()

    approach_pos = xy_from(logic, "ApproachPos")
    if approach_pos:
        data["approach_pos"] = approach_pos
    approach_r = safe_float(logic.findtext("ApproachR"), 0.0)
    if approach_r != 0:
        data["approach_r"] = approach_r
    door_pos = xy_from(logic, "DoorPos")
    if door_pos:
        data["door_pos"] = door_pos
    leave_pos = xy_from(logic, "LeavePos")
    if leave_pos:
        data["leave_pos"] = leave_pos

    work_tasklist = logic.find("WorkTaskList")
    if work_tasklist is not None:
        building_work_tasklists = {}
        for child in work_tasklist:
            val = (child.text or "").strip()
            if val:
                building_work_tasklists[child.tag.lower()] = val
        if building_work_tasklists:
            data["work_tasklists"] = building_work_tasklists

    upgrade = logic.find("Upgrade")
    if upgrade is not None:
        upgrade_data = {
            "category": (upgrade.findtext("Category") or "").strip(),
            "time": safe_float(upgrade.findtext("Time"), 0),
            "type": (upgrade.findtext("Type") or "").strip(),
            "cost": {},
        }
        cost = upgrade.find("Cost")
        if cost is not None:
            for child in cost:
                val = safe_int(child.text, 0)
                if val > 0:
                    upgrade_data["cost"][child.tag.lower()] = val
        data["upgrade"] = upgrade_data

    constr = logic.find("ConstructionInfo")
    if constr is not None:
        data["build_time"] = safe_int(constr.findtext("Time"), 0)
        data["build_cost"] = {}
        cost = constr.find("Cost")
        if cost is not None:
            for child in cost:
                val = safe_int(child.text, 0)
                if val > 0:
                    data["build_cost"][child.tag.lower()] = val
        data["builder_slots"] = len(constr.findall("BuilderSlot"))

    blocked1 = xy_from(logic, "Blocked1")
    blocked2 = xy_from(logic, "Blocked2")
    if blocked1 and blocked2:
        data["blocked1"] = blocked1
        data["blocked2"] = blocked2
        data["footprint"] = {
            "width": abs(blocked2["x"] - blocked1["x"]),
            "height": abs(blocked2["y"] - blocked1["y"]),
        }

    data["behaviors"] = []
    for behavior in root.findall(".//Behavior"):
        logic_b = behavior.find("Logic")
        if logic_b is None:
            continue
        classname = logic_b.get("classname", "")

        if "CMineBehaviorProperties" in classname:
            data["behaviors"].append(
                {
                    "type": "CMineBehavior",
                    "amount_to_mine": safe_int(logic_b.findtext("AmountToMine"), 0),
                }
            )

        if "CResourceRefinerBehaviorProperties" in classname:
            data["behaviors"].append(
                {
                    "type": "CResourceRefinerBehavior",
                    "resource_type": (logic_b.findtext("ResourceType") or "").strip(),
                    "initial_factor": safe_int(logic_b.findtext("InitialFactor"), 4),
                    "supplier_category": (logic_b.findtext("SupplierCategory") or "").strip(),
                }
            )

        if "CLimitedAttachmentBehaviorProperties" in classname:
            for att in logic_b.findall("Attachment"):
                att_type = (att.findtext("Type") or "").strip()
                att_limit = safe_int(att.findtext("Limit"), 0)
                if "WORKER_RESIDENCE" in att_type:
                    data["residence_capacity"] = att_limit
                elif "WORKER_FARM" in att_type:
                    data["farm_capacity"] = att_limit
                elif "DEFENDER" in att_type:
                    data["defender_capacity"] = att_limit

    return data


def parse_all_buildings(paths: OverlayPaths) -> Dict[str, Dict[str, object]]:
    buildings: Dict[str, Dict[str, object]] = {}
    for pattern in BUILDING_PATTERNS:
        suffixes: Iterable[str]
        if pattern == "PB_Beautification":
            suffixes = (f"{idx:02d}" for idx in range(1, 13))
        else:
            suffixes = (str(idx) for idx in range(1, 5))

        for suffix in suffixes:
            filename = f"{pattern}{suffix}.xml"
            filepath = paths.resolve("Entities", filename)
            if filepath is None:
                continue
            print(f"  Parsing building: {filepath.name}")
            data = parse_building(filepath)
            if data:
                buildings[filepath.stem.lower()] = data
    return buildings


def parse_deposit(filepath: Path) -> Optional[Dict[str, object]]:
    root = parse_xml_safe(filepath)
    if root is None:
        return None

    data: Dict[str, object] = {"_file": filepath.name}
    logic = root.find(".//Logic[@classname='GGL::CResourceDoodadProperties']")
    if logic is None:
        logic = root.find(".//Logic")

    if logic is not None:
        data["radius"] = safe_int(logic.findtext("Radius"), 0)
        data["category"] = (logic.findtext("Category") or "").strip()
        blocked1 = xy_from(logic, "Blocked1")
        blocked2 = xy_from(logic, "Blocked2")
        if blocked1 and blocked2:
            data["blocked1"] = blocked1
            data["blocked2"] = blocked2

    for behavior in root.findall(".//Behavior"):
        logic_b = behavior.find("Logic")
        if logic_b is None:
            continue
        classname = logic_b.get("classname", "")
        if "CGLResourceDoodadBehaviorProps" not in classname:
            continue
        resource = logic_b.find("Resource")
        if resource is None:
            continue
        data["resource_good"] = (resource.findtext("Good") or "").strip()
        data["resource_amount"] = safe_int(resource.findtext("Amount"), 0)

    return data


def parse_all_deposits(paths: OverlayPaths) -> Dict[str, Dict[str, object]]:
    deposits: Dict[str, Dict[str, object]] = {}
    for filename in DEPOSIT_FILES:
        filepath = paths.resolve("Entities", filename)
        if filepath is None:
            print(f"  WARNING: deposit file not found: {filename}")
            continue
        print(f"  Parsing deposit: {filepath.name}")
        data = parse_deposit(filepath)
        if data:
            deposits[filepath.stem.lower()] = data
    return deposits


def parse_tasklist(filepath: Path) -> Optional[Dict[str, object]]:
    root = parse_xml_safe(filepath)
    if root is None:
        return None

    task_counts: Dict[str, int] = defaultdict(int)
    animation_waits: List[int] = []
    set_tasklist_targets: List[str] = []
    task_sequence_head: List[str] = []
    total_animation_wait_ms = 0
    total_wait_ms = 0

    for task in root.findall(".//Task"):
        task_type = (task.findtext("TaskType") or "").strip()
        if not task_type:
            continue
        task_counts[task_type] += 1

        if len(task_sequence_head) < 25:
            task_sequence_head.append(task_type)

        if task_type == "TASK_WAIT_FOR_ANIM":
            ms = safe_int(task.findtext("Thousandths"), 0)
            total_animation_wait_ms += ms
            animation_waits.append(ms)
        elif task_type == "TASK_WAIT":
            total_wait_ms += safe_int(task.findtext("Thousandths"), 0)
        elif task_type == "TASK_SET_TASK_LIST":
            target = (task.findtext("TaskList") or "").strip()
            if target:
                set_tasklist_targets.append(target)

    counts_sorted = dict(sorted(task_counts.items(), key=lambda kv: kv[0]))
    return {
        "_file": filepath.name,
        "principal_task": (root.findtext(".//PrincipalTask") or "").strip(),
        "task_counts": counts_sorted,
        "task_sequence_head": task_sequence_head,
        "task_set_task_list_targets": sorted(set(set_tasklist_targets)),
        "total_animation_wait_ms": total_animation_wait_ms,
        "total_wait_ms": total_wait_ms,
        "animation_waits": animation_waits,
        # Backward-compatible fields used by existing diff scripts:
        "task_mined_resource_count": counts_sorted.get("TASK_MINED_RESOURCE", 0),
        "task_refine_resource_count": counts_sorted.get("TASK_REFINE_RESOURCE", 0),
        "task_change_work_time_work_count": counts_sorted.get(
            "TASK_CHANGE_WORK_TIME_WORK", 0
        ),
        "task_work_wait_until_count": counts_sorted.get("TASK_WORK_WAIT_UNTIL", 0),
    }


def parse_named_tasklists(
    paths: OverlayPaths, mapping: Dict[str, str], label: str
) -> Dict[str, Dict[str, object]]:
    result: Dict[str, Dict[str, object]] = {}
    for key, filename in mapping.items():
        filepath = paths.resolve("TaskLists", filename)
        if filepath is None:
            print(f"  WARNING: missing {label} tasklist: {filename}")
            continue
        print(f"  Parsing {label} tasklist: {filepath.name}")
        parsed = parse_tasklist(filepath)
        if parsed:
            result[key] = parsed
    return result


def parse_logic(paths: OverlayPaths) -> Dict[str, object]:
    filepath = paths.resolve("Logic.xml")
    if filepath is None:
        print("  WARNING: Logic.xml not found")
        return {}
    root = parse_xml_safe(filepath)
    if root is None:
        return {}

    print("  Parsing Logic.xml")
    data: Dict[str, object] = {}

    data["buildings"] = {
        "compensation_on_sale": safe_int(root.findtext("CompensationOnBuildingSale"), 50),
        "placement_snap_distance": safe_int(
            root.findtext("BuildingPlacementSnapDistance"), 900
        ),
        "construction_site_health_factor": safe_float(
            root.findtext("ConstructionSiteHealthFactor"), 0.25
        ),
        "closed_health_factor": safe_float(
            root.findtext("BuildingClosedHealthFactor"), 0.2
        ),
        "under_construction_exploration_factor": safe_float(
            root.findtext("BuildingUnderConstructionExplorationFactor"), 0.25
        ),
    }

    data["weather"] = {
        "rain_move_speed_factor": safe_float(
            root.findtext("WeatherMoveSpeedRainFactor"), 1.0
        ),
        "snow_move_speed_factor": safe_float(
            root.findtext("WeatherMoveSpeedSnowFactor"), 1.0
        ),
        "rain_exploration_building_factor": safe_float(
            root.findtext("WeatherExplorationBuildingRainFactor"), 1.0
        ),
        "rain_exploration_settler_factor": safe_float(
            root.findtext("WeatherExplorationSettlerRainFactor"), 1.0
        ),
        "snow_exploration_building_factor": safe_float(
            root.findtext("WeatherExplorationBuildingSnowFactor"), 1.0
        ),
        "snow_exploration_settler_factor": safe_float(
            root.findtext("WeatherExplorationSettlerSnowFactor"), 1.0
        ),
    }

    data["taxes"] = {
        "tax_amount": safe_int(root.findtext("TaxAmount"), 5),
        "tax_penalty": safe_float(root.findtext("TaxPenalty"), 0.1),
        "initial_tax_level": safe_int(root.findtext("InitialTaxLevel"), 2),
        "levels": [],
    }
    for level_elem in root.findall("TaxationLevel"):
        data["taxes"]["levels"].append(
            {
                "regular_tax": safe_int(level_elem.findtext("RegularTax"), 0),
                "motivation_change": safe_float(level_elem.findtext("MotivationChange"), 0),
            }
        )

    data["motivation"] = {
        "threshold_happy": safe_float(root.findtext("MotivationThresholdHappy"), 1.5),
        "threshold_sad": safe_float(root.findtext("MotivationThresholdSad"), 1.0),
        "threshold_angry": safe_float(root.findtext("MotivationThresholdAngry"), 0.7),
        "threshold_leave": safe_float(root.findtext("MotivationThresholdLeave"), 0.25),
        "absolute_max": safe_float(root.findtext("MotivationAbsoluteMaxMotivation"), 3.0),
        "game_start_max": safe_float(
            root.findtext("MotivationGameStartMaxMotivation"), 1.0
        ),
        "village_center_lock_threshold": safe_float(
            root.findtext("AverageMotivationVillageCenterLockThreshold"), 0.3
        ),
        "milliseconds_without_job": safe_int(
            root.findtext("MotivationMillisecondsWithoutJob"), 30000
        ),
    }

    data["worktime"] = {
        "base": safe_int(root.findtext("WorkTimeBase"), 125),
        "threshold_work": safe_int(root.findtext("WorkTimeThresholdWork"), 25),
        "force_to_work_penalty": safe_float(root.findtext("ForceToWorkPenalty"), 0.2),
    }

    data["blessing"] = {
        "bonus": safe_float(root.findtext("BlessingBonus"), 0.3),
        "bonus_time": safe_int(root.findtext("BlessingBonusTime"), 180),
        "maximum_faith": safe_int(root.findtext("MaximumFaith"), 5000),
        "cost": {},
        "categories": [],
    }
    blessing_cost = root.find("BlessingCost")
    if blessing_cost is not None:
        for child in blessing_cost:
            data["blessing"]["cost"][child.tag.lower()] = safe_int(child.text, 0)
    for cat_elem in root.findall("BlessCategory"):
        data["blessing"]["categories"].append(
            {
                "name": (cat_elem.findtext("Name") or "").strip(),
                "required_faith": safe_int(cat_elem.findtext("RequiredFaith"), 5000),
                "entity_types": [
                    et.text.strip() for et in cat_elem.findall("EntityType") if et.text
                ],
            }
        )

    data["trade"] = []
    for trade_elem in root.findall("TradeResource"):
        data["trade"].append(
            {
                "resource_type": (trade_elem.findtext("ResourceType") or "").strip(),
                "base_price": safe_float(trade_elem.findtext("BasePrice"), 1.0),
                "min_price": safe_float(trade_elem.findtext("MinPrice"), 0.2),
                "max_price": safe_float(trade_elem.findtext("MaxPrice"), 2.8),
                "inflation": safe_float(trade_elem.findtext("Inflation"), 0.0001),
                "deflation": safe_float(trade_elem.findtext("Deflation"), 0.0001),
                "work_amount": safe_float(trade_elem.findtext("WorkAmount"), 0.1),
            }
        )

    data["building_upgrades"] = []
    for upgrade_elem in root.findall("BuildingUpgrade"):
        data["building_upgrades"].append(
            {
                "category": (upgrade_elem.findtext("Category") or "").strip(),
                "first_building": (upgrade_elem.findtext("FirstBuilding") or "").strip(),
            }
        )

    data["resources"] = {
        "doodad_warn_amount": safe_int(root.findtext("ResourceDoodadWarnAmount"), 800),
    }

    data["defender"] = {
        "ms_per_shot": safe_int(root.findtext("DefenderMSPerShot"), 4000),
        "max_range": safe_int(root.findtext("DefenderMaxRange"), 3000),
        "damage": safe_int(root.findtext("DefenderProjectileDamage"), 5),
        "miss_chance": safe_int(root.findtext("DefenderMissChance"), 8),
    }

    data["movement"] = {
        "worker_flight_distance": safe_int(root.findtext("WorkerFlightDistance"), 2500),
        "leader_nudge_count": safe_int(root.findtext("LeaderNudgeCount"), 3),
        "leader_approach_range": safe_float(root.findtext("LeaderApproachRange"), 200.0),
        "attack_move_range": safe_int(root.findtext("AttackMoveRange"), 2000),
        "guard_max_distance_building": safe_float(
            root.findtext("GuardMaxDistanceBuilding"), 1000.0
        ),
        "guard_move_distance_building": safe_float(
            root.findtext("GuardMoveDistanceBuilding"), 900.0
        ),
        "guard_max_distance_other": safe_float(
            root.findtext("GuardMaxDistanceOther"), 600.0
        ),
        "guard_move_distance_other": safe_float(
            root.findtext("GuardMoveDistanceOther"), 300.0
        ),
    }

    return data


def parse_entities_manifest(paths: OverlayPaths) -> Dict[str, object]:
    filepath = paths.resolve("Entities.xml")
    if filepath is None:
        return {}
    root = parse_xml_safe(filepath)
    if root is None:
        return {}

    default_walk_speed = safe_int(root.findtext("Logic/DefaultWalkSpeed"), 0)
    entities = [e.text.strip() for e in root.findall("Entity") if e.text]
    camp_entities = [name for name in entities if "Camp" in name]

    return {
        "default_walk_speed": default_walk_speed,
        "entity_count": len(entities),
        "camp_entities_count": len(camp_entities),
        "camp_entities": camp_entities,
    }


def parse_terrain_summary(paths: OverlayPaths) -> Dict[str, object]:
    filepath = paths.resolve("Terrain.xml")
    if filepath is None:
        return {}
    root = parse_xml_safe(filepath)
    if root is None:
        return {}

    blocked_types = []
    unblocked_count = 0
    walk_modifier_types = []

    for terr in root.findall("TerrainType"):
        terr_id = terr.get("id", "")
        value = safe_int(terr.get("value"), -1)
        logic = terr.find("Logic")
        if logic is None:
            continue
        blocked = safe_bool(logic.findtext("Blocked"), False)
        if blocked:
            blocked_types.append({"id": terr_id, "value": value})
        else:
            unblocked_count += 1

        walk_modifier = logic.findtext("WalkModifier")
        if walk_modifier is not None:
            walk_modifier_types.append(
                {"id": terr_id, "value": value, "walk_modifier": safe_float(walk_modifier)}
            )

    return {
        "terrain_type_count": len(blocked_types) + unblocked_count,
        "blocked_type_count": len(blocked_types),
        "unblocked_type_count": unblocked_count,
        "blocked_types": blocked_types,
        "walk_modifier_entries": walk_modifier_types,
        "has_explicit_walk_modifiers": bool(walk_modifier_types),
    }


def parse_camp_mechanics(paths: OverlayPaths) -> Dict[str, object]:
    result: Dict[str, object] = {}

    camp_internal = paths.resolve("Entities", "XD_Camp_Internal.xml")
    if camp_internal is not None:
        root = parse_xml_safe(camp_internal)
        if root is not None:
            camp_logic = root.find(".//Logic[@classname='GGL::CCampBehaviorProperties']")
            if camp_logic is not None:
                slots = []
                for slot in camp_logic.findall("Slot"):
                    slots.append(
                        {
                            "x": safe_int(slot.findtext("X"), 0),
                            "y": safe_int(slot.findtext("Y"), 0),
                        }
                    )
                result["internal_camp"] = {
                    "slot_count": len(slots),
                    "slots": slots,
                    "remove_delay_seconds": safe_float(
                        camp_logic.findtext("RemoveDelay"), 10.0
                    ),
                }

    large_camp_fire = paths.resolve("Entities", "XD_LargeCampFire.xml")
    if large_camp_fire is not None:
        root = parse_xml_safe(large_camp_fire)
        if root is not None:
            logic = root.find(".//Logic[@classname='EGL::CGLEEntityProps']")
            if logic is not None:
                result["large_camp_fire"] = {
                    "num_blocked_points": safe_int(logic.findtext("NumBlockedPoints"), 0),
                    "snap_tolerance": safe_float(logic.findtext("SnapTolerance"), 0.0),
                }

    camp_buildings = {}
    for filepath in paths.list_overlay_files("Entities", "CB_Camp*.xml"):
        root = parse_xml_safe(filepath)
        if root is None:
            continue
        logic = root.find(".//Logic[@classname='GGL::CGLBuildingProps']")
        if logic is None:
            continue
        blocked1 = xy_from(logic, "Blocked1")
        blocked2 = xy_from(logic, "Blocked2")
        entry = {
            "max_health": safe_int(logic.findtext("MaxHealth"), 0),
            "approach_pos": xy_from(logic, "ApproachPos"),
            "door_pos": xy_from(logic, "DoorPos"),
            "exploration": safe_int(logic.findtext("Exploration"), 0),
        }
        if blocked1 and blocked2:
            entry["blocked1"] = blocked1
            entry["blocked2"] = blocked2
            entry["footprint"] = {
                "width": abs(blocked2["x"] - blocked1["x"]),
                "height": abs(blocked2["y"] - blocked1["y"]),
            }
        camp_buildings[filepath.stem] = entry

    miner_camps = {}
    for filepath in paths.list_overlay_files("Entities", "CB_MinerCamp*.xml"):
        root = parse_xml_safe(filepath)
        if root is None:
            continue
        logic = root.find(".//Logic[@classname='GGL::CGLBuildingProps']")
        if logic is None:
            continue
        blocked1 = xy_from(logic, "Blocked1")
        blocked2 = xy_from(logic, "Blocked2")
        entry = {
            "max_health": safe_int(logic.findtext("MaxHealth"), 0),
            "approach_pos": xy_from(logic, "ApproachPos"),
            "door_pos": xy_from(logic, "DoorPos"),
            "exploration": safe_int(logic.findtext("Exploration"), 0),
        }
        if blocked1 and blocked2:
            entry["blocked1"] = blocked1
            entry["blocked2"] = blocked2
            entry["footprint"] = {
                "width": abs(blocked2["x"] - blocked1["x"]),
                "height": abs(blocked2["y"] - blocked1["y"]),
            }
        miner_camps[filepath.stem] = entry

    result["cb_camps"] = camp_buildings
    result["cb_miner_camps"] = miner_camps
    result["summary"] = {
        "cb_camp_count": len(camp_buildings),
        "cb_miner_camp_count": len(miner_camps),
    }
    return result


def build_pathfinding_snapshot(
    workers: Dict[str, Dict[str, object]],
    logic: Dict[str, object],
    entities_manifest: Dict[str, object],
    terrain: Dict[str, object],
) -> Dict[str, object]:
    worker_movement = {}
    for name, data in sorted(workers.items()):
        worker_movement[name] = {
            "speed": data.get("speed"),
            "rotation_speed": data.get("rotation_speed"),
            "move_task_list": data.get("move_task_list"),
            "camper_range": data.get("camper_range"),
            "resource_search_radius": data.get("resource_search_radius"),
            "work_time_change_camp": data.get("work_time_change_camp"),
            "tasklists": data.get("tasklists", {}),
        }

    return {
        "logic_movement": logic.get("movement", {}),
        "weather_speed_factors": logic.get("weather", {}),
        "default_walk_speed": entities_manifest.get("default_walk_speed"),
        "terrain_blocking": {
            "blocked_type_count": terrain.get("blocked_type_count"),
            "unblocked_type_count": terrain.get("unblocked_type_count"),
        },
        "workers": worker_movement,
    }


def print_summary(result: Dict[str, object]) -> None:
    workers = result.get("workers", {})
    buildings = result.get("buildings", {})
    deposits = result.get("deposits", {})
    tasklists = result.get("tasklists", {})
    mine_tasklists = result.get("mine_tasklists", {})
    serf_tasklists = result.get("serf_tasklists", {})
    worker_path_tasklists = result.get("worker_path_tasklists", {})
    camps = result.get("camp_mechanics", {}).get("summary", {})
    source = result.get("engine_source", {})

    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"Source mode: {source.get('mode')}")
    print(f"Source root: {source.get('source_root')}")
    print(f"Config roots: {source.get('config_roots')}")
    print()
    print(f"Workers: {len(workers)}")
    print(f"Buildings: {len(buildings)}")
    print(f"Deposits: {len(deposits)}")
    print(f"Tasklists (work): {len(tasklists)}")
    print(f"Tasklists (mine): {len(mine_tasklists)}")
    print(f"Tasklists (serf): {len(serf_tasklists)}")
    print(f"Tasklists (worker path): {len(worker_path_tasklists)}")
    print(
        f"Camp files: CB={camps.get('cb_camp_count', 0)}, Miner={camps.get('cb_miner_camp_count', 0)}"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Settlers 5 engine decoder")
    parser.add_argument(
        "--game-root",
        default=None,
        help=(
            "Optional path to game root (contains base/extra1/extra2) "
            "or directly to a config root (contains Logic.xml, Entities, TaskLists)."
        ),
    )
    parser.add_argument(
        "--output",
        default=str(OUTPUT_FILE),
        help=f"Output JSON path (default: {OUTPUT_FILE})",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    out_path = Path(args.output).resolve()

    print("=" * 72)
    print("SETTLERS 5 ENGINE DECODER")
    print("=" * 72)

    paths = OverlayPaths.detect(args.game_root)
    print(f"Source mode: {paths.mode}")
    print(f"Source root: {paths.source_root}")
    print(f"Config roots (priority high->low):")
    for cfg in paths.config_roots:
        print(f"  - {cfg}")
    print(f"Output: {out_path}")
    print()

    result: Dict[str, object] = {
        "engine_source": paths.debug_info(),
    }

    print("[1/11] Parsing worker parameters...")
    result["workers"] = parse_all_workers(paths)
    print(f"  -> {len(result['workers'])} workers parsed\n")

    print("[2/11] Parsing building parameters...")
    result["buildings"] = parse_all_buildings(paths)
    print(f"  -> {len(result['buildings'])} buildings parsed\n")

    print("[3/11] Parsing deposits...")
    result["deposits"] = parse_all_deposits(paths)
    print(f"  -> {len(result['deposits'])} deposits parsed\n")

    print("[4/11] Parsing worker tasklists...")
    result["tasklists"] = parse_named_tasklists(paths, TASKLIST_WORK_FILES, "work")
    print(f"  -> {len(result['tasklists'])} worker tasklists parsed\n")

    print("[5/11] Parsing mine tasklists...")
    result["mine_tasklists"] = parse_named_tasklists(
        paths, MINE_TASKLIST_FILES, "mine"
    )
    print(f"  -> {len(result['mine_tasklists'])} mine tasklists parsed\n")

    print("[6/11] Parsing serf tasklists...")
    result["serf_tasklists"] = parse_named_tasklists(
        paths, SERF_TASKLIST_FILES, "serf"
    )
    print(f"  -> {len(result['serf_tasklists'])} serf tasklists parsed\n")

    print("[7/11] Parsing worker path tasklists...")
    result["worker_path_tasklists"] = parse_named_tasklists(
        paths, WORKER_PATH_TASKLIST_FILES, "worker path"
    )
    print(
        f"  -> {len(result['worker_path_tasklists'])} worker path tasklists parsed\n"
    )

    print("[8/11] Parsing global logic...")
    result["logic"] = parse_logic(paths)
    print()

    print("[9/11] Parsing entities manifest + terrain...")
    result["entities_manifest"] = parse_entities_manifest(paths)
    result["terrain"] = parse_terrain_summary(paths)
    print()

    print("[10/11] Parsing camp mechanics...")
    result["camp_mechanics"] = parse_camp_mechanics(paths)
    print()

    print("[11/11] Building pathfinding snapshot...")
    result["pathfinding_snapshot"] = build_pathfinding_snapshot(
        result["workers"],
        result["logic"],
        result["entities_manifest"],
        result["terrain"],
    )
    print()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote output: {out_path}\n")

    print_summary(result)


if __name__ == "__main__":
    main()
