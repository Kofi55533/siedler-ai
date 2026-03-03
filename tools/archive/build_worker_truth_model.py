#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a consolidated worker truth model from engine_decoded.json.

This script is intentionally read-only on game data and does not require
starting the game client.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import xml.etree.ElementTree as ET


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ENGINE_JSON = SCRIPT_DIR / "config" / "engine_decoded.json"
DEFAULT_OUTPUT_JSON = SCRIPT_DIR / "config" / "worker_truth_model.json"

ENGINE_TO_ENV_WORKER_ALIASES = {
    "sawmillworker": "sawmill_worker",
    "tavernbarkeeper": "barkeeper",
    "masterbuilder": "master_builder",
}

TASKLIST_SECTIONS = (
    "tasklists",
    "mine_tasklists",
    "serf_tasklists",
    "worker_path_tasklists",
)


def _canonical_tasklist_filename(name: str) -> str:
    clean = (name or "").strip()
    if not clean:
        return ""
    if not clean.lower().endswith(".xml"):
        clean = f"{clean}.xml"
    return clean.lower()


def _tasklist_candidates(name: str) -> List[str]:
    canon = _canonical_tasklist_filename(name)
    if not canon:
        return []
    out = [canon]
    if canon.endswith("_start.xml"):
        out.append(canon.replace("_start.xml", ".xml"))
    # Keep order but remove duplicates.
    seen = set()
    dedup = []
    for item in out:
        if item in seen:
            continue
        seen.add(item)
        dedup.append(item)
    return dedup


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _summarize_tasklist(tasklist: Dict[str, Any]) -> Dict[str, Any]:
    mined = _safe_int(tasklist.get("task_mined_resource_count"), 0)
    refined = _safe_int(tasklist.get("task_refine_resource_count"), 0)
    return {
        "file": tasklist.get("_file"),
        "principal_task": tasklist.get("principal_task"),
        "resource_ops_per_cycle": mined + refined,
        "task_mined_resource_count": mined,
        "task_refine_resource_count": refined,
        "task_change_work_time_work_count": _safe_int(
            tasklist.get("task_change_work_time_work_count"), 0
        ),
        "task_work_wait_until_count": _safe_int(
            tasklist.get("task_work_wait_until_count"), 0
        ),
        "total_animation_wait_ms": _safe_int(tasklist.get("total_animation_wait_ms"), 0),
        "total_wait_ms": _safe_int(tasklist.get("total_wait_ms"), 0),
        "task_counts": tasklist.get("task_counts", {}),
        "task_sequence_head": tasklist.get("task_sequence_head", []),
        "task_set_task_list_targets": tasklist.get("task_set_task_list_targets", []),
    }


def _build_tasklist_lookup(engine: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    lookup: Dict[str, List[Dict[str, Any]]] = {}
    for section in TASKLIST_SECTIONS:
        section_data = engine.get(section, {})
        if not isinstance(section_data, dict):
            continue
        for key, tasklist in section_data.items():
            if not isinstance(tasklist, dict):
                continue
            filename = _canonical_tasklist_filename(str(tasklist.get("_file", "")))
            if not filename:
                continue
            lookup.setdefault(filename, []).append(
                {"section": section, "key": key, "tasklist": tasklist}
            )
    return lookup


def _parse_xml_safe(filepath: Path) -> Optional[ET.Element]:
    try:
        content = filepath.read_text(encoding="utf-8-sig")
        return ET.fromstring(content)
    except Exception:
        return None


def _parse_tasklist_file(filepath: Path) -> Optional[Dict[str, Any]]:
    root = _parse_xml_safe(filepath)
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
            ms = _safe_int(task.findtext("Thousandths"), 0)
            total_animation_wait_ms += ms
            animation_waits.append(ms)
        elif task_type == "TASK_WAIT":
            total_wait_ms += _safe_int(task.findtext("Thousandths"), 0)
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
        "task_mined_resource_count": counts_sorted.get("TASK_MINED_RESOURCE", 0),
        "task_refine_resource_count": counts_sorted.get("TASK_REFINE_RESOURCE", 0),
        "task_change_work_time_work_count": counts_sorted.get(
            "TASK_CHANGE_WORK_TIME_WORK", 0
        ),
        "task_work_wait_until_count": counts_sorted.get("TASK_WORK_WAIT_UNTIL", 0),
    }


def _build_overlay_tasklist_index(config_roots: List[str]) -> Dict[str, Path]:
    index: Dict[str, Path] = {}
    for raw_root in config_roots:
        root = Path(raw_root)
        tasklist_dir = root / "TaskLists"
        if not tasklist_dir.exists():
            continue
        for filepath in tasklist_dir.glob("*.xml"):
            index[filepath.name.lower()] = filepath
    return index


def _resolve_tasklist(
    name: str,
    lookup: Dict[str, List[Dict[str, Any]]],
    overlay_files: Dict[str, Path],
    overlay_cache: Dict[str, Optional[Dict[str, Any]]],
) -> Optional[Dict[str, Any]]:
    for candidate in _tasklist_candidates(name):
        entries = lookup.get(candidate)
        if not entries:
            overlay_file = overlay_files.get(candidate)
            if overlay_file is None:
                continue
            if candidate not in overlay_cache:
                overlay_cache[candidate] = _parse_tasklist_file(overlay_file)
            parsed_overlay = overlay_cache[candidate]
            if not isinstance(parsed_overlay, dict):
                continue
            return {
                "requested_name": name,
                "resolved_file": parsed_overlay.get("_file"),
                "section": "overlay_tasklists",
                "key": overlay_file.stem.lower(),
                "source_path": str(overlay_file),
                "summary": _summarize_tasklist(parsed_overlay),
            }

        entry = entries[0]
        return {
            "requested_name": name,
            "resolved_file": entry["tasklist"].get("_file"),
            "section": entry["section"],
            "key": entry["key"],
            "summary": _summarize_tasklist(entry["tasklist"]),
        }
    return None


def _worker_env_name(worker_name: str) -> str:
    return ENGINE_TO_ENV_WORKER_ALIASES.get(worker_name, worker_name)


def _build_serf_extraction_truth(
    serf_data: Dict[str, Any], serf_tasklists: Dict[str, Dict[str, Any]]
) -> Dict[str, Any]:
    extract_resource = serf_tasklists.get("serf_extract_resource")
    extract_wood = serf_tasklists.get("serf_extract_wood")

    by_entity_type: Dict[str, Any] = {}
    for ext in serf_data.get("extraction_info", []):
        entity_type = str(ext.get("entity_type", ""))
        delay_seconds = _safe_float(ext.get("delay"), 0.0)
        amount = _safe_int(ext.get("amount"), 0)
        is_wood = "tree" in entity_type.lower()
        selected = extract_wood if is_wood else extract_resource
        selected_key = "serf_extract_wood" if is_wood else "serf_extract_resource"

        anim_ms = _safe_int(selected.get("total_animation_wait_ms"), 0) if selected else 0
        wait_ms = _safe_int(selected.get("total_wait_ms"), 0) if selected else 0
        cycle_seconds = delay_seconds + (anim_ms + wait_ms) / 1000.0
        amount_per_second = (amount / cycle_seconds) if cycle_seconds > 0 else None

        by_entity_type[entity_type] = {
            "delay_seconds": delay_seconds,
            "amount_per_cycle": amount,
            "selected_tasklist_key": selected_key,
            "selected_tasklist_file": (selected or {}).get("_file"),
            "selected_tasklist_animation_wait_ms": anim_ms,
            "selected_tasklist_wait_ms": wait_ms,
            "estimated_cycle_seconds": cycle_seconds,
            "estimated_amount_per_second": amount_per_second,
        }

    return {
        "resource_search_radius": serf_data.get("resource_search_radius"),
        "extraction_info": serf_data.get("extraction_info", []),
        "extract_tasklists": {
            "serf_extract_resource": (
                _summarize_tasklist(extract_resource) if isinstance(extract_resource, dict) else None
            ),
            "serf_extract_wood": (
                _summarize_tasklist(extract_wood) if isinstance(extract_wood, dict) else None
            ),
        },
        "by_entity_type": by_entity_type,
    }


def build_worker_truth_model(engine: Dict[str, Any], source_path: Path) -> Dict[str, Any]:
    workers = engine.get("workers", {})
    tasklists = engine.get("tasklists", {})
    mine_tasklists = engine.get("mine_tasklists", {})
    serf_tasklists = engine.get("serf_tasklists", {})
    path_tasklists = engine.get("worker_path_tasklists", {})
    path_snapshot = engine.get("pathfinding_snapshot", {})
    logic = engine.get("logic", {})
    camps = engine.get("camp_mechanics", {})
    source_meta = engine.get("engine_source", {})

    tasklist_lookup = _build_tasklist_lookup(engine)
    overlay_tasklist_files = _build_overlay_tasklist_index(
        source_meta.get("config_roots", [])
    )
    overlay_tasklist_cache: Dict[str, Optional[Dict[str, Any]]] = {}
    unresolved_declared_tasklists: Dict[str, Dict[str, str]] = {}
    workers_missing_primary_work_profile: List[str] = []

    worker_models: Dict[str, Any] = {}
    for worker_name, worker_data in sorted(workers.items()):
        env_name = _worker_env_name(worker_name)
        declared_tasklists = worker_data.get("tasklists", {})
        resolved_declared_tasklists: Dict[str, Any] = {}
        unresolved_for_worker: Dict[str, str] = {}

        for tag, declared_name in declared_tasklists.items():
            resolved = _resolve_tasklist(
                str(declared_name),
                tasklist_lookup,
                overlay_tasklist_files,
                overlay_tasklist_cache,
            )
            if resolved is not None:
                resolved_declared_tasklists[tag] = resolved
            else:
                unresolved_for_worker[tag] = str(declared_name)

        move_task_name = worker_data.get("move_task_list")
        if isinstance(move_task_name, str) and move_task_name.strip():
            move_resolved = _resolve_tasklist(
                move_task_name,
                tasklist_lookup,
                overlay_tasklist_files,
                overlay_tasklist_cache,
            )
            if move_resolved is not None:
                resolved_declared_tasklists["MoveTaskList"] = move_resolved
            else:
                unresolved_for_worker["MoveTaskList"] = move_task_name

        if unresolved_for_worker:
            unresolved_declared_tasklists[worker_name] = unresolved_for_worker

        primary_work_profile = tasklists.get(worker_name)
        miner_profiles = (
            {
                key: _summarize_tasklist(value)
                for key, value in sorted(mine_tasklists.items())
                if isinstance(value, dict)
            }
            if worker_name == "miner"
            else {}
        )
        if worker_name != "serf" and not isinstance(primary_work_profile, dict):
            workers_missing_primary_work_profile.append(worker_name)

        path_worker_snapshot = (path_snapshot.get("workers", {}) or {}).get(worker_name, {})

        worktime_truth = None
        if worker_data.get("has_worktime"):
            worktime_truth = {
                "work_wait_until": worker_data.get("work_wait_until"),
                "work_time_change_work": worker_data.get("work_time_change_work"),
                "work_time_change_farm": worker_data.get("work_time_change_farm"),
                "work_time_change_residence": worker_data.get("work_time_change_residence"),
                "work_time_change_camp": worker_data.get("work_time_change_camp"),
                "work_time_max_farm": worker_data.get("work_time_max_farm"),
                "work_time_max_residence": worker_data.get("work_time_max_residence"),
                "eat_wait": worker_data.get("eat_wait"),
                "rest_wait": worker_data.get("rest_wait"),
                "exhausted_malus": worker_data.get("exhausted_malus"),
            }

        worker_models[worker_name] = {
            "env_name": env_name,
            "source_file": worker_data.get("_file"),
            "has_worktime": bool(worker_data.get("has_worktime")),
            "movement": {
                "speed": worker_data.get("speed"),
                "rotation_speed": worker_data.get("rotation_speed"),
                "move_task_list": worker_data.get("move_task_list"),
                "camper_range": worker_data.get("camper_range"),
                "resource_search_radius": worker_data.get("resource_search_radius"),
                "path_snapshot": path_worker_snapshot,
            },
            "worktime_truth": worktime_truth,
            "work_cycle_truth": {
                "primary_work_tasklist": (
                    _summarize_tasklist(primary_work_profile)
                    if isinstance(primary_work_profile, dict)
                    else None
                ),
                "miner_tasklists": miner_profiles,
            },
            "declared_tasklists": declared_tasklists,
            "resolved_declared_tasklists": resolved_declared_tasklists,
            "serf_extraction_truth": (
                _build_serf_extraction_truth(worker_data, serf_tasklists)
                if worker_name == "serf"
                else None
            ),
        }

    env_to_engine = {
        env_name: engine_name
        for engine_name, env_name in sorted(
            ((k, _worker_env_name(k)) for k in worker_models.keys()),
            key=lambda item: item[1],
        )
    }

    return {
        "meta": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "source_engine_decoded": str(source_path),
            "source_mode": source_meta.get("mode"),
            "source_root": source_meta.get("source_root"),
            "config_roots": source_meta.get("config_roots", []),
            "worker_count": len(worker_models),
            "limitations": [
                "Static XML extraction only.",
                "Binary runtime internals of the path solver are not directly exposed in config files.",
            ],
        },
        "global_truth": {
            "logic_worktime": logic.get("worktime", {}),
            "logic_movement": logic.get("movement", {}),
            "weather_speed_factors": path_snapshot.get("weather_speed_factors", {}),
            "default_walk_speed": path_snapshot.get("default_walk_speed"),
            "terrain_blocking": path_snapshot.get("terrain_blocking", {}),
            "camp_mechanics_summary": camps.get("summary", {}),
            "camp_internal": camps.get("internal_camp", {}),
            "camp_large_fire": camps.get("large_camp_fire", {}),
            "worker_path_tasklists": {
                key: _summarize_tasklist(value)
                for key, value in sorted(path_tasklists.items())
                if isinstance(value, dict)
            },
            "serf_tasklists": {
                key: _summarize_tasklist(value)
                for key, value in sorted(serf_tasklists.items())
                if isinstance(value, dict)
            },
        },
        "name_mapping": {
            "engine_to_env": {name: _worker_env_name(name) for name in sorted(worker_models)},
            "env_to_engine": env_to_engine,
        },
        "workers": worker_models,
        "checks": {
            "workers_missing_primary_work_profile": workers_missing_primary_work_profile,
            "workers_with_unresolved_declared_tasklists": sorted(unresolved_declared_tasklists.keys()),
            "unresolved_declared_tasklists": unresolved_declared_tasklists,
            "overlay_tasklists_parsed": len(
                [x for x in overlay_tasklist_cache.values() if isinstance(x, dict)]
            ),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build consolidated worker truth model from engine_decoded.json"
    )
    parser.add_argument(
        "--engine-json",
        type=Path,
        default=DEFAULT_ENGINE_JSON,
        help=f"Input engine JSON (default: {DEFAULT_ENGINE_JSON})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_JSON,
        help=f"Output truth model JSON (default: {DEFAULT_OUTPUT_JSON})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    engine_path = args.engine_json.resolve()
    output_path = args.output.resolve()

    if not engine_path.exists():
        raise FileNotFoundError(f"Engine JSON not found: {engine_path}")

    engine = json.loads(engine_path.read_text(encoding="utf-8"))
    truth_model = build_worker_truth_model(engine, engine_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(truth_model, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    checks = truth_model.get("checks", {})
    unresolved = checks.get("workers_with_unresolved_declared_tasklists", [])
    missing_work = checks.get("workers_missing_primary_work_profile", [])

    print("Worker truth model generated")
    print(f"Source: {engine_path}")
    print(f"Output: {output_path}")
    print(f"Workers: {truth_model['meta']['worker_count']}")
    print(f"Workers missing primary work tasklist: {len(missing_work)}")
    print(f"Workers with unresolved declared tasklists: {len(unresolved)}")


if __name__ == "__main__":
    main()
