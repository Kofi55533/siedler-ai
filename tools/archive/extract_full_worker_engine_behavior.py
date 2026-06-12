#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract the complete worker/serf-facing engine configuration from Settlers 5.

The existing decoder keeps curated lists for the values the simulation already
uses. This extractor is deliberately broader:
- scans the layered original config folders directly,
- parses every effective TaskList XML,
- parses every entity that declares worker/serf/camper behavior or worker
  building data,
- follows TaskList references recursively from workers and their workplaces.

It still cannot decompile hidden C++ runtime branches. The output records every
static XML task and argument that drives those engine branches.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple
import xml.etree.ElementTree as ET


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent

DEFAULT_GAME_ROOT_CANDIDATES = [
    r"C:\Users\marku\OneDrive\Desktop\Gold edition",
    r"C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games\theSettlers5",
]

DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "config" / "full_worker_engine_behavior.json"
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "config" / "full_worker_engine_behavior.md"

TASKLIST_RE = re.compile(r"\bTL_[A-Za-z0-9_]+\b")
_PARSE_WARNINGS_EMITTED: Set[Path] = set()

ENGINE_TO_ENV_WORKER_ALIASES = {
    "sawmillworker": "sawmill_worker",
    "tavernbarkeeper": "barkeeper",
    "masterbuilder": "master_builder",
}

WORKER_RELEVANT_BEHAVIORS = (
    "CWorkerBehaviorProps",
    "CSerfBehaviorProps",
    "CCamperBehaviorProperties",
    "CWorkerAlarmModeBehaviorProps",
    "CWorkerFleeBehaviorProps",
)

WORKER_BUILDING_HINTS = {
    "ATTACHMENT_WORKER_FARM",
    "ATTACHMENT_WORKER_RESIDENCE",
    "WORKER_RESIDENCE",
    "WORKER_FARM",
}

GLOBAL_LOGIC_KEYWORDS = (
    "Worker",
    "WorkTime",
    "ForceToWork",
    "Motivation",
    "Farm",
    "Residence",
    "Camp",
    "Serf",
    "MoveSpeed",
    "Move",
)


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(str(value).strip().rstrip("f")))
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(str(value).strip().rstrip("f"))
    except (TypeError, ValueError):
        return default


def _clean_text(value: Optional[str]) -> str:
    return (value or "").strip()


def _maybe_number(value: str) -> Any:
    text = _clean_text(value)
    if not text:
        return ""
    lowered = text.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    stripped = text.rstrip("f")
    try:
        if any(ch in stripped for ch in (".", "e", "E")):
            return float(stripped)
        return int(stripped)
    except ValueError:
        return text


def _layer_name(path: Path) -> str:
    parts = {part.lower(): part for part in path.parts}
    for layer in ("extra2", "extra1", "base"):
        if layer in parts:
            return layer
    return "config"


class OverlayPaths:
    def __init__(self, source_root: Path, config_roots: List[Path], mode: str) -> None:
        self.source_root = source_root
        self.config_roots = config_roots  # effective priority: highest to lowest
        self.mode = mode

    @staticmethod
    def _is_config_root(path: Path) -> bool:
        return (
            (path / "Logic.xml").exists()
            and (path / "Entities").exists()
            and (path / "TaskLists").exists()
        )

    @classmethod
    def _from_candidate(cls, candidate: Path) -> Optional["OverlayPaths"]:
        candidate = candidate.expanduser()
        if cls._is_config_root(candidate):
            return cls(candidate, [candidate], "single_config_root")

        roots: List[Path] = []
        for layer in ("extra2", "extra1", "base"):
            cfg = candidate / layer / "shr" / "config"
            if cls._is_config_root(cfg):
                roots.append(cfg)
        if roots:
            return cls(candidate, roots, "layered_game_root")
        return None

    @classmethod
    def detect(cls, user_path: Optional[str]) -> "OverlayPaths":
        candidates: List[Path] = []
        if user_path:
            candidates.append(Path(user_path))
        env_root = os.environ.get("SIEDLER5_ROOT")
        if env_root:
            candidates.append(Path(env_root))
        candidates.extend(Path(p) for p in DEFAULT_GAME_ROOT_CANDIDATES)

        for candidate in candidates:
            resolved = cls._from_candidate(candidate)
            if resolved is not None:
                return resolved

        tried = "\n".join(f"  - {p}" for p in candidates)
        raise FileNotFoundError(f"No Settlers 5 config root found.\nChecked:\n{tried}")

    def effective_files(self, subdir: str, pattern: str = "*.xml") -> Dict[str, Path]:
        merged: Dict[str, Path] = {}
        # Apply low-to-high so extra2 wins over extra1/base.
        for cfg in reversed(self.config_roots):
            folder = cfg / subdir
            if not folder.exists():
                continue
            for file in folder.glob(pattern):
                merged[file.name.lower()] = file
        return dict(sorted(merged.items()))

    def source_layers(self, subdir: str, pattern: str = "*.xml") -> Dict[str, List[Dict[str, str]]]:
        layers: Dict[str, List[Dict[str, str]]] = defaultdict(list)
        for cfg in self.config_roots:
            folder = cfg / subdir
            if not folder.exists():
                continue
            for file in sorted(folder.glob(pattern), key=lambda p: p.name.lower()):
                layers[file.name.lower()].append(
                    {
                        "layer": _layer_name(file),
                        "path": str(file),
                    }
                )
        return dict(sorted(layers.items()))

    def resolve(self, *relative_parts: str) -> Optional[Path]:
        rel = Path(*relative_parts)
        for cfg in self.config_roots:
            candidate = cfg / rel
            if candidate.exists():
                return candidate
        return None

    def debug_info(self) -> Dict[str, Any]:
        return {
            "mode": self.mode,
            "source_root": str(self.source_root),
            "config_roots": [str(p) for p in self.config_roots],
        }


def _parse_xml_safe(path: Path) -> Optional[ET.Element]:
    try:
        return ET.fromstring(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        if path not in _PARSE_WARNINGS_EMITTED:
            _PARSE_WARNINGS_EMITTED.add(path)
            print(f"WARNING: cannot parse {path}: {exc}")
        return None


def _add_multi(mapping: Dict[str, Any], key: str, value: Any) -> None:
    if key not in mapping:
        mapping[key] = value
        return
    existing = mapping[key]
    if not isinstance(existing, list):
        mapping[key] = [existing]
    mapping[key].append(value)


def _element_value(element: ET.Element) -> Any:
    children = list(element)
    if not children:
        return _maybe_number(element.text or "")
    out: Dict[str, Any] = {}
    for child in children:
        _add_multi(out, child.tag, _element_value(child))
    return out


def _collect_tasklist_refs_from_text(text: str) -> List[str]:
    return sorted(set(match.group(0) for match in TASKLIST_RE.finditer(text or "")))


def _collect_tasklist_refs(element: ET.Element, path: str = "") -> List[Dict[str, str]]:
    refs: List[Dict[str, str]] = []
    tag_path = f"{path}/{element.tag}" if path else element.tag
    text = _clean_text(element.text)
    matches = _collect_tasklist_refs_from_text(text)
    for value in matches:
        refs.append({"path": tag_path, "value": value})
    for child in list(element):
        refs.extend(_collect_tasklist_refs(child, tag_path))
    return refs


def _canonical_tasklist_name(name: str) -> str:
    clean = _clean_text(name)
    if not clean:
        return ""
    if not clean.lower().endswith(".xml"):
        clean = f"{clean}.xml"
    return clean.lower()


def _tasklist_candidates(name: str) -> List[str]:
    canonical = _canonical_tasklist_name(name)
    if not canonical:
        return []
    candidates = [canonical]
    if canonical.endswith("_start.xml"):
        candidates.append(canonical.replace("_start.xml", ".xml"))
    seen: Set[str] = set()
    out: List[str] = []
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        out.append(candidate)
    return out


def _resolve_tasklist_name(name: str, tasklists: Dict[str, Dict[str, Any]]) -> Optional[str]:
    for candidate in _tasklist_candidates(name):
        if candidate in tasklists:
            return candidate
    return None


def _classify_task_type(task_type: str) -> str:
    if task_type.startswith("TASK_CHECK_"):
        return "branch_check"
    if "GO_TO" in task_type or task_type in {
        "TASK_WALK",
        "TASK_GO_TO_CAMP",
        "TASK_TURN_TO_TARGET_ORIENTATION",
        "TASK_SET_POS",
        "TASK_LEAVE_BUILDING",
        "TASK_ENTER_BUILDING",
        "TASK_LEFT_BUILDING",
    }:
        return "movement"
    if (
        "WORK_TIME" in task_type
        or task_type
        in {
            "TASK_EAT_WAIT",
            "TASK_REST_WAIT",
            "TASK_WORK_WAIT_UNTIL",
            "TASK_WAIT_EXTRACTION_DELAY",
        }
    ):
        return "worktime"
    if "RESOURCE" in task_type or task_type in {"TASK_EXTRACT_WOOD", "TASK_EXTRACT_RESOURCE"}:
        return "resource"
    if "WAIT" in task_type:
        return "wait"
    if "ANIM" in task_type:
        return "animation"
    if "BATTLE" in task_type or "ATTACK" in task_type:
        return "combat"
    return "other"


def parse_tasklist(path: Path, layers: Sequence[Dict[str, str]]) -> Optional[Dict[str, Any]]:
    root = _parse_xml_safe(path)
    if root is None:
        return None

    tasks: List[Dict[str, Any]] = []
    counts: Counter[str] = Counter()
    class_counts: Counter[str] = Counter()
    set_tasklist_targets: List[str] = []
    refs: List[Dict[str, str]] = []
    waits: List[Dict[str, Any]] = []
    categories: Dict[str, List[str]] = defaultdict(list)
    total_wait_ms = 0
    total_animation_wait_ms = 0

    for index, task in enumerate(root.findall("./Task")):
        task_type = _clean_text(task.findtext("TaskType"))
        classname = _clean_text(task.get("classname"))
        classid = _clean_text(task.get("classid"))
        args: Dict[str, Any] = {}
        task_refs: List[Dict[str, str]] = []

        for child in list(task):
            if child.tag == "TaskType":
                continue
            _add_multi(args, child.tag, _element_value(child))
            task_refs.extend(_collect_tasklist_refs(child, child.tag))

        if task_type:
            counts[task_type] += 1
            category = _classify_task_type(task_type)
            categories[category].append(task_type)
        if classname:
            class_counts[classname] += 1

        thousandths = _safe_int(args.get("Thousandths"), 0)
        if task_type == "TASK_WAIT":
            total_wait_ms += thousandths
            waits.append({"index": index, "task_type": task_type, "ms": thousandths})
        elif task_type == "TASK_WAIT_FOR_ANIM":
            total_animation_wait_ms += thousandths
            waits.append({"index": index, "task_type": task_type, "ms": thousandths})

        for ref in task_refs:
            if ref["value"] not in set_tasklist_targets:
                set_tasklist_targets.append(ref["value"])
        refs.extend({"index": index, **ref} for ref in task_refs)

        tasks.append(
            {
                "index": index,
                "task_type": task_type,
                "category": _classify_task_type(task_type),
                "classname": classname,
                "classid": classid,
                "args": args,
                "tasklist_refs": task_refs,
            }
        )

    sequence = [task["task_type"] for task in tasks if task["task_type"]]
    return {
        "file": path.name,
        "canonical_name": path.name.lower(),
        "source_path": str(path),
        "source_layer": _layer_name(path),
        "source_layers": list(layers),
        "principal_task": _clean_text(root.findtext("PrincipalTask")),
        "task_count": len(tasks),
        "task_counts": dict(sorted(counts.items())),
        "task_class_counts": dict(sorted(class_counts.items())),
        "task_categories": {
            key: sorted(set(value)) for key, value in sorted(categories.items())
        },
        "task_sequence": sequence,
        "tasks": tasks,
        "tasklist_refs": refs,
        "task_set_task_list_targets": sorted(set(set_tasklist_targets)),
        "waits": waits,
        "total_wait_ms": total_wait_ms,
        "total_animation_wait_ms": total_animation_wait_ms,
        "task_change_work_time_work_count": counts.get("TASK_CHANGE_WORK_TIME_WORK", 0),
        "task_work_wait_until_count": counts.get("TASK_WORK_WAIT_UNTIL", 0),
        "task_mined_resource_count": counts.get("TASK_MINED_RESOURCE", 0),
        "task_refine_resource_count": counts.get("TASK_REFINE_RESOURCE", 0),
        "task_wait_extraction_delay_count": counts.get("TASK_WAIT_EXTRACTION_DELAY", 0),
        "is_combat_related": any(
            "BATTLE" in task_type or "ATTACK" in task_type for task_type in counts
        ),
    }


def _direct_child_values(element: Optional[ET.Element]) -> Dict[str, Any]:
    if element is None:
        return {}
    out: Dict[str, Any] = {}
    for child in list(element):
        _add_multi(out, child.tag, _element_value(child))
    return out


def _xy_from(parent: ET.Element, tag: str) -> Optional[Dict[str, int]]:
    elem = parent.find(tag)
    if elem is None:
        return None
    return {"x": _safe_int(elem.findtext("X")), "y": _safe_int(elem.findtext("Y"))}


def _entity_worker_key(stem: str) -> str:
    clean = stem.lower()
    if clean.startswith("pu_"):
        clean = clean[3:]
    return ENGINE_TO_ENV_WORKER_ALIASES.get(clean, clean)


def _extract_behavior_blocks(root: ET.Element) -> List[Dict[str, Any]]:
    behaviors: List[Dict[str, Any]] = []
    for index, behavior in enumerate(root.findall("./Behavior")):
        logic = behavior.find("Logic")
        display = behavior.find("Display")
        logic_classname = _clean_text(logic.get("classname")) if logic is not None else ""
        block = {
            "index": index,
            "logic_classname": logic_classname,
            "logic_class": _clean_text(logic.findtext("Class")) if logic is not None else "",
            "logic_fields": _direct_child_values(logic),
            "display_classname": _clean_text(display.get("classname")) if display is not None else "",
            "display_fields": _direct_child_values(display),
            "tasklist_refs": _collect_tasklist_refs(logic, "Behavior/Logic") if logic is not None else [],
        }
        behaviors.append(block)
    return behaviors


def _extract_primary_logic(root: ET.Element) -> Dict[str, Any]:
    logic = root.find("./Logic")
    if logic is None:
        return {}
    categories = [
        _clean_text(cat.text)
        for cat in logic.findall("Category")
        if _clean_text(cat.text)
    ]
    return {
        "classname": _clean_text(logic.get("classname")),
        "class": _clean_text(logic.findtext("Class")),
        "fields": _direct_child_values(logic),
        "categories": categories,
        "tasklist_refs": _collect_tasklist_refs(logic, "Logic"),
    }


def parse_worker_entity(path: Path, layers: Sequence[Dict[str, str]]) -> Optional[Dict[str, Any]]:
    root = _parse_xml_safe(path)
    if root is None:
        return None

    logic = _extract_primary_logic(root)
    behaviors = _extract_behavior_blocks(root)
    behavior_classnames = [b["logic_classname"] for b in behaviors]
    worker_behaviors = [
        b for b in behaviors if "CWorkerBehaviorProps" in b["logic_classname"]
    ]
    serf_behaviors = [
        b for b in behaviors if "CSerfBehaviorProps" in b["logic_classname"]
    ]
    camper_behaviors = [
        b for b in behaviors if "CCamperBehaviorProperties" in b["logic_classname"]
    ]
    movement_behaviors = [
        b for b in behaviors if "CMovementBehaviorProps" in b["logic_classname"]
    ]

    refs: List[Dict[str, str]] = []
    refs.extend(logic.get("tasklist_refs", []))
    for behavior in behaviors:
        refs.extend(behavior.get("tasklist_refs", []))

    categories = set(logic.get("categories", []))
    relevant = (
        any(any(marker in classname for marker in WORKER_RELEVANT_BEHAVIORS) for classname in behavior_classnames)
        or "Worker" in categories
        or path.stem.lower() in {"pu_serf", "pu_battleserf"}
    )
    if not relevant:
        return None

    movement_fields = movement_behaviors[0]["logic_fields"] if movement_behaviors else {}
    worker_fields = worker_behaviors[0]["logic_fields"] if worker_behaviors else {}
    serf_fields = serf_behaviors[0]["logic_fields"] if serf_behaviors else {}
    camper_fields = camper_behaviors[0]["logic_fields"] if camper_behaviors else {}
    env_name = _entity_worker_key(path.stem)

    worktime_truth = {}
    if worker_fields:
        worktime_truth = {
            "work_wait_until": _safe_int(worker_fields.get("WorkWaitUntil")),
            "work_time_change_work": _safe_int(worker_fields.get("WorkTimeChangeWork"), -50),
            "exhausted_malus": _safe_float(worker_fields.get("ExhaustedWorkMotivationMalus"), 0.2),
            "eat_wait": _safe_int(worker_fields.get("EatWait"), 2000),
            "rest_wait": _safe_int(worker_fields.get("RestWait"), 3000),
            "work_time_change_farm": _safe_float(worker_fields.get("WorkTimeChangeFarm"), 0.7),
            "work_time_change_residence": _safe_float(worker_fields.get("WorkTimeChangeResidence"), 0.5),
            "work_time_change_camp": _safe_float(worker_fields.get("WorkTimeChangeCamp"), 0.1),
            "work_time_max_farm": _safe_int(worker_fields.get("WorkTimeMaxChangeFarm"), 100),
            "work_time_max_residence": _safe_int(worker_fields.get("WorkTimeMaxChangeResidence"), 400),
        }

    movement = {}
    if movement_fields:
        movement = {
            "speed": _safe_int(movement_fields.get("Speed"), 320),
            "rotation_speed": _safe_int(movement_fields.get("RotationSpeed"), 30),
            "move_idle_anim": movement_fields.get("MoveIdleAnim", ""),
            "move_task_list": movement_fields.get("MoveTaskList", ""),
        }
    if camper_fields:
        movement["camper_range"] = _safe_int(camper_fields.get("Range"), 5000)

    extraction_info: List[Dict[str, Any]] = []
    raw_extraction = serf_fields.get("ExtractionInfo")
    raw_extraction_items = raw_extraction if isinstance(raw_extraction, list) else [raw_extraction]
    for item in raw_extraction_items:
        if not isinstance(item, dict):
            continue
        extraction_info.append(
            {
                "resource_entity_type": item.get("ResourceEntityType", ""),
                "delay_seconds": _safe_float(item.get("Delay")),
                "amount": _safe_int(item.get("Amount"), 1),
            }
        )

    return {
        "entity": path.stem,
        "env_name": env_name,
        "file": path.name,
        "source_path": str(path),
        "source_layer": _layer_name(path),
        "source_layers": list(layers),
        "logic": logic,
        "behavior_classnames": sorted(set(behavior_classnames)),
        "behaviors": behaviors,
        "tasklist_refs": refs,
        "tasklist_ref_values": sorted(set(ref["value"] for ref in refs)),
        "has_worktime": bool(worker_fields),
        "has_serf_logic": bool(serf_fields),
        "movement": movement,
        "worktime_truth": worktime_truth,
        "serf_extraction_info": extraction_info,
        "worker_behavior_fields": worker_fields,
        "serf_behavior_fields": serf_fields,
        "camper_behavior_fields": camper_fields,
    }


def parse_worker_building(path: Path, layers: Sequence[Dict[str, str]]) -> Optional[Dict[str, Any]]:
    root = _parse_xml_safe(path)
    if root is None:
        return None

    logic_elem = root.find("./Logic")
    logic = _extract_primary_logic(root)
    behaviors = _extract_behavior_blocks(root)
    refs: List[Dict[str, str]] = []
    refs.extend(logic.get("tasklist_refs", []))
    for behavior in behaviors:
        refs.extend(behavior.get("tasklist_refs", []))

    logic_fields = logic.get("fields", {})
    worker_type = _clean_text(str(logic_fields.get("Worker", "")))
    work_tasklists: List[Dict[str, str]] = []
    work_tasklist_values: List[str] = []
    work_tasklist_elems = logic_elem.findall("WorkTaskList") if logic_elem is not None else []
    for work_tasklists_elem in work_tasklist_elems:
        group: Dict[str, str] = {}
        for child in list(work_tasklists_elem):
            value = _clean_text(child.text)
            if value:
                group[child.tag] = value
                work_tasklist_values.append(value)
        if group:
            work_tasklists.append(group)

    attachment_limits: Dict[str, int] = {}
    for behavior in behaviors:
        fields = behavior.get("logic_fields", {})
        raw_attachments = fields.get("Attachment")
        attachments = raw_attachments if isinstance(raw_attachments, list) else [raw_attachments]
        for attachment in attachments:
            if not isinstance(attachment, dict):
                continue
            attachment_type = str(attachment.get("Type", ""))
            limit = _safe_int(attachment.get("Limit"))
            if attachment_type:
                attachment_limits[attachment_type] = limit

    has_worker_attachment = any(
        any(hint in key for hint in WORKER_BUILDING_HINTS)
        for key in attachment_limits.keys()
    )
    logic_classname = str(logic.get("classname", ""))
    lower_stem = path.stem.lower()
    is_building_entity = (
        "CGLBuildingProps" in logic_classname
        or lower_stem.startswith(("pb_", "cb_"))
        or lower_stem in {"xd_camp", "xd_camp_internal"}
    )
    relevant = is_building_entity and bool(
        worker_type or work_tasklists or has_worker_attachment or lower_stem in {"xd_camp", "xd_camp_internal"}
    )
    if not relevant:
        return None

    blocked1 = _xy_from(logic_elem, "Blocked1") if logic_elem is not None else None
    blocked2 = _xy_from(logic_elem, "Blocked2") if logic_elem is not None else None
    footprint = None
    if blocked1 and blocked2:
        footprint = {
            "width": abs(blocked2["x"] - blocked1["x"]),
            "height": abs(blocked2["y"] - blocked1["y"]),
        }

    return {
        "entity": path.stem,
        "file": path.name,
        "source_path": str(path),
        "source_layer": _layer_name(path),
        "source_layers": list(layers),
        "worker_type": worker_type,
        "worker_env_name": _entity_worker_key(worker_type) if worker_type else "",
        "max_workers": _safe_int(logic_fields.get("MaxWorkers")),
        "initial_max_workers": _safe_int(logic_fields.get("InitialMaxWorkers")),
        "build_on": logic_fields.get("BuildOn", ""),
        "approach_pos": _xy_from(logic_elem, "ApproachPos") if logic_elem is not None else None,
        "door_pos": _xy_from(logic_elem, "DoorPos") if logic_elem is not None else None,
        "leave_pos": _xy_from(logic_elem, "LeavePos") if logic_elem is not None else None,
        "blocked1": blocked1,
        "blocked2": blocked2,
        "footprint": footprint,
        "work_tasklists": work_tasklists,
        "work_tasklist_values": sorted(set(work_tasklist_values)),
        "attachment_limits": attachment_limits,
        "logic": logic,
        "behavior_classnames": sorted(set(b["logic_classname"] for b in behaviors)),
        "behaviors": behaviors,
        "tasklist_refs": refs,
        "tasklist_ref_values": sorted(set([*work_tasklist_values, *(ref["value"] for ref in refs)])),
    }


def parse_global_logic(paths: OverlayPaths) -> Dict[str, Any]:
    logic_path = paths.resolve("Logic.xml")
    if logic_path is None:
        return {}
    root = _parse_xml_safe(logic_path)
    if root is None:
        return {}

    scalars: Dict[str, Any] = {}
    for elem in root.iter():
        if list(elem):
            continue
        text = _clean_text(elem.text)
        if not text:
            continue
        if any(keyword in elem.tag for keyword in GLOBAL_LOGIC_KEYWORDS):
            scalars[elem.tag] = _maybe_number(text)

    return {
        "file": logic_path.name,
        "source_path": str(logic_path),
        "source_layer": _layer_name(logic_path),
        "scalars": dict(sorted(scalars.items())),
        "worktime": {
            "base": _safe_int(scalars.get("WorkTimeBase"), 125),
            "threshold_work": _safe_int(scalars.get("WorkTimeThresholdWork"), 25),
            "force_to_work_penalty": _safe_float(scalars.get("ForceToWorkPenalty"), 0.2),
        },
        "movement": {
            "worker_flight_distance": _safe_int(scalars.get("WorkerFlightDistance"), 2500),
        },
    }


def _collect_seed_tasklists(
    worker: Dict[str, Any],
    worker_buildings: Dict[str, Dict[str, Any]],
) -> List[str]:
    seeds = list(worker.get("tasklist_ref_values", []))
    env_name = worker.get("env_name")
    entity_name = worker.get("entity", "")
    for building in worker_buildings.values():
        worker_type = str(building.get("worker_type", ""))
        building_env = building.get("worker_env_name", "")
        if not worker_type and not building_env:
            continue
        if (
            building_env == env_name
            or worker_type.lower() == entity_name.lower()
            or _entity_worker_key(worker_type) == env_name
        ):
            seeds.extend(building.get("work_tasklist_values", []))
            seeds.extend(building.get("tasklist_ref_values", []))
    return sorted(set(seed for seed in seeds if seed))


def _build_reachable_task_graph(
    seeds: Iterable[str],
    tasklists: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    queue: deque[str] = deque()
    unresolved: Set[str] = set()
    seed_map: Dict[str, Optional[str]] = {}

    for seed in seeds:
        resolved = _resolve_tasklist_name(seed, tasklists)
        seed_map[seed] = resolved
        if resolved:
            queue.append(resolved)
        else:
            unresolved.add(seed)

    visited: Set[str] = set()
    edges: List[Dict[str, str]] = []
    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        tasklist = tasklists[current]
        for ref in tasklist.get("task_set_task_list_targets", []):
            resolved = _resolve_tasklist_name(ref, tasklists)
            if resolved is None:
                unresolved.add(ref)
                continue
            edges.append({"from": current, "to": resolved, "via": ref})
            if resolved not in visited:
                queue.append(resolved)

    return {
        "seed_tasklists": seed_map,
        "reachable_tasklists": sorted(visited),
        "edges": edges,
        "unresolved_tasklists": sorted(unresolved),
    }


def _derive_runtime_worker_values(
    worker: Dict[str, Any],
    graph: Dict[str, Any],
    tasklists: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    work_counts: List[int] = []
    for name in graph.get("reachable_tasklists", []):
        tasklist = tasklists.get(name, {})
        count = _safe_int(tasklist.get("task_change_work_time_work_count"))
        if count <= 0:
            continue
        principal = str(tasklist.get("principal_task", "")).lower()
        if principal == "work" or "work" in name:
            work_counts.append(count)

    movement = worker.get("movement", {})
    return {
        "env_name": worker.get("env_name"),
        "has_worktime": bool(worker.get("has_worktime")),
        "speed": _safe_int(movement.get("speed"), 320),
        "rotation_speed": _safe_int(movement.get("rotation_speed"), 30),
        "camper_range": _safe_int(movement.get("camper_range"), 5000),
        "worktime": worker.get("worktime_truth", {}),
        "worktime_changes_per_cycle": max(work_counts) if work_counts else 1,
        "work_tasklists_with_change_count": {
            name: tasklists[name].get("task_change_work_time_work_count", 0)
            for name in graph.get("reachable_tasklists", [])
            if tasklists.get(name, {}).get("task_change_work_time_work_count", 0)
        },
    }


def build_full_behavior(paths: OverlayPaths) -> Dict[str, Any]:
    tasklist_sources = paths.source_layers("TaskLists", "*.xml")
    entity_sources = paths.source_layers("Entities", "*.xml")
    effective_tasklist_files = paths.effective_files("TaskLists", "*.xml")
    effective_entity_files = paths.effective_files("Entities", "*.xml")

    tasklists: Dict[str, Dict[str, Any]] = {}
    for key, path in effective_tasklist_files.items():
        parsed = parse_tasklist(path, tasklist_sources.get(key, []))
        if parsed:
            tasklists[key] = parsed

    worker_entities: Dict[str, Dict[str, Any]] = {}
    worker_buildings: Dict[str, Dict[str, Any]] = {}
    for key, path in effective_entity_files.items():
        parsed_worker = parse_worker_entity(path, entity_sources.get(key, []))
        if parsed_worker:
            worker_entities[path.stem.lower()] = parsed_worker
            continue
        parsed_building = parse_worker_building(path, entity_sources.get(key, []))
        if parsed_building:
            worker_buildings[path.stem.lower()] = parsed_building

    per_worker_graphs: Dict[str, Dict[str, Any]] = {}
    runtime_workers: Dict[str, Dict[str, Any]] = {}
    global_reachable: Set[str] = set()
    global_unresolved: Set[str] = set()
    for key, worker in worker_entities.items():
        seeds = _collect_seed_tasklists(worker, worker_buildings)
        graph = _build_reachable_task_graph(seeds, tasklists)
        per_worker_graphs[key] = graph
        worker["task_graph"] = graph
        worker["runtime"] = _derive_runtime_worker_values(worker, graph, tasklists)
        runtime_workers[str(worker["env_name"])] = worker["runtime"]
        global_reachable.update(graph["reachable_tasklists"])
        global_unresolved.update(graph["unresolved_tasklists"])

    all_task_types = sorted(
        {
            task_type
            for tasklist in tasklists.values()
            for task_type in tasklist.get("task_counts", {}).keys()
        }
    )
    task_type_counts: Counter[str] = Counter()
    for tasklist in tasklists.values():
        task_type_counts.update(tasklist.get("task_counts", {}))

    source_file_counts = {
        "tasklists_effective": len(effective_tasklist_files),
        "entities_effective": len(effective_entity_files),
        "tasklist_layer_files": sum(len(v) for v in tasklist_sources.values()),
        "entity_layer_files": sum(len(v) for v in entity_sources.values()),
    }

    return {
        "meta": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            **paths.debug_info(),
            "extractor": str(Path(__file__).resolve()),
            "source_file_counts": source_file_counts,
            "worker_entity_count": len(worker_entities),
            "worker_building_count": len(worker_buildings),
            "tasklist_count": len(tasklists),
            "reachable_worker_tasklist_count": len(global_reachable),
            "unresolved_worker_tasklist_count": len(global_unresolved),
            "limitations": [
                "Static XML extraction of all effective worker/serf-facing config files.",
                "C++ engine internals such as exact path solver branches remain binary runtime behavior.",
            ],
        },
        "global_logic": parse_global_logic(paths),
        "runtime": {
            "global_worktime": parse_global_logic(paths).get("worktime", {}),
            "workers": runtime_workers,
        },
        "task_type_catalog": {
            "task_type_count": len(all_task_types),
            "task_types": all_task_types,
            "global_task_type_counts": dict(sorted(task_type_counts.items())),
        },
        "worker_entities": dict(sorted(worker_entities.items())),
        "worker_buildings": dict(sorted(worker_buildings.items())),
        "reachable_worker_tasklists": {
            name: {
                "file": tasklists[name]["file"],
                "principal_task": tasklists[name]["principal_task"],
                "task_count": tasklists[name]["task_count"],
                "task_counts": tasklists[name]["task_counts"],
                "task_set_task_list_targets": tasklists[name]["task_set_task_list_targets"],
            }
            for name in sorted(global_reachable)
        },
        "unresolved_worker_tasklists": sorted(global_unresolved),
        "tasklists": tasklists,
    }


def write_markdown(data: Dict[str, Any], path: Path) -> None:
    meta = data.get("meta", {})
    task_catalog = data.get("task_type_catalog", {})
    workers = data.get("worker_entities", {})
    buildings = data.get("worker_buildings", {})
    lines = [
        "# Full Worker Engine Behavior Extract",
        "",
        f"- Generated: `{meta.get('generated_at_utc')}`",
        f"- Source root: `{meta.get('source_root')}`",
        f"- Mode: `{meta.get('mode')}`",
        f"- Effective TaskLists parsed: `{meta.get('tasklist_count')}`",
        f"- Worker/serf entities parsed: `{meta.get('worker_entity_count')}`",
        f"- Worker buildings parsed: `{meta.get('worker_building_count')}`",
        f"- Worker-reachable TaskLists: `{meta.get('reachable_worker_tasklist_count')}`",
        f"- Unresolved worker TaskList refs: `{meta.get('unresolved_worker_tasklist_count')}`",
        f"- Distinct task types: `{task_catalog.get('task_type_count')}`",
        "",
        "## Runtime Worker Values",
        "",
        "| Worker | Speed | CamperRange | WorkWait | EatWait | RestWait | WorkTimeChanges/Cycle |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    runtime_workers = data.get("runtime", {}).get("workers", {})
    for worker_name, runtime in sorted(runtime_workers.items()):
        wt = runtime.get("worktime", {})
        lines.append(
            "| {name} | {speed} | {camper} | {work_wait} | {eat_wait} | {rest_wait} | {changes} |".format(
                name=worker_name,
                speed=runtime.get("speed", ""),
                camper=runtime.get("camper_range", ""),
                work_wait=wt.get("work_wait_until", ""),
                eat_wait=wt.get("eat_wait", ""),
                rest_wait=wt.get("rest_wait", ""),
                changes=runtime.get("worktime_changes_per_cycle", ""),
            )
        )

    lines.extend(
        [
            "",
            "## Worker Entity Coverage",
            "",
            "| Entity | Env name | WorkTime | Serf | Direct TaskList refs | Reachable TaskLists |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for key, worker in sorted(workers.items()):
        graph = worker.get("task_graph", {})
        lines.append(
            "| {entity} | {env} | {worktime} | {serf} | {refs} | {reachable} |".format(
                entity=key,
                env=worker.get("env_name", ""),
                worktime="yes" if worker.get("has_worktime") else "no",
                serf="yes" if worker.get("has_serf_logic") else "no",
                refs=len(worker.get("tasklist_ref_values", [])),
                reachable=len(graph.get("reachable_tasklists", [])),
            )
        )

    lines.extend(
        [
            "",
            "## Worker Building Coverage",
            "",
            "| Building | Worker | Work TaskLists | Attachments | Footprint |",
            "| --- | --- | ---: | ---: | --- |",
        ]
    )
    for key, building in sorted(buildings.items()):
        footprint = building.get("footprint") or {}
        footprint_text = ""
        if footprint:
            footprint_text = f"{footprint.get('width')}x{footprint.get('height')}"
        lines.append(
            "| {entity} | {worker} | {work_tl} | {attachments} | {footprint} |".format(
                entity=key,
                worker=building.get("worker_type", ""),
                work_tl=len(building.get("work_tasklists", [])),
                attachments=len(building.get("attachment_limits", {})),
                footprint=footprint_text,
            )
        )

    unresolved = data.get("unresolved_worker_tasklists", [])
    lines.extend(["", "## Unresolved Worker TaskList References", ""])
    if unresolved:
        lines.extend(f"- `{item}`" for item in unresolved)
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- The JSON contains every parsed task with args under `tasklists`.",
            "- `reachable_worker_tasklists` is the recursive worker/serf/workplace subset.",
            "- Combat-related tasklists are still parsed, but runtime integration can ignore them.",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract full Settlers 5 worker/serf engine XML behavior."
    )
    parser.add_argument(
        "--game-root",
        default=None,
        help="Settlers 5 root or config root. Defaults to SIEDLER5_ROOT / known installs.",
    )
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_OUTPUT_MD))
    args = parser.parse_args()

    paths = OverlayPaths.detect(args.game_root)
    data = build_full_behavior(paths)

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False),
        encoding="utf-8",
    )
    write_markdown(data, Path(args.output_md))

    meta = data["meta"]
    print(f"Source root: {meta['source_root']}")
    print(f"TaskLists parsed: {meta['tasklist_count']}")
    print(f"Worker entities parsed: {meta['worker_entity_count']}")
    print(f"Worker buildings parsed: {meta['worker_building_count']}")
    print(f"Worker-reachable TaskLists: {meta['reachable_worker_tasklist_count']}")
    print(f"Unresolved refs: {meta['unresolved_worker_tasklist_count']}")
    print(f"Wrote: {output_json}")
    print(f"Wrote: {args.output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
