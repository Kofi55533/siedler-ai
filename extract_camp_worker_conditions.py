#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract camp placement/usage conditions from decoded worker truth and map data.

Goal:
- Make camp-related worker behavior explicit from XML-derived truth.
- Separate static map camps from dynamic worker camping behavior.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import xml.etree.ElementTree as ET


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_TRUTH_MODEL = SCRIPT_DIR / "config" / "worker_truth_model.json"
DEFAULT_MAPDATA = SCRIPT_DIR / "map_extract" / "wintersturm_extracted" / "mapdata.xml"
DEFAULT_OUTPUT_JSON = SCRIPT_DIR / "config" / "camp_worker_conditions.json"
DEFAULT_OUTPUT_MD = SCRIPT_DIR / "config" / "camp_worker_conditions.md"


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


def _canonical_tasklist_filename(name: str) -> str:
    clean = (name or "").strip()
    if not clean:
        return ""
    if not clean.lower().endswith(".xml"):
        clean = f"{clean}.xml"
    return clean.lower()


def _parse_xml_safe(path: Path) -> Optional[ET.Element]:
    try:
        content = path.read_text(encoding="utf-8-sig")
        return ET.fromstring(content)
    except Exception:
        return None


def _parse_tasklist_file(path: Path) -> Optional[Dict[str, Any]]:
    root = _parse_xml_safe(path)
    if root is None:
        return None

    task_counts: Dict[str, int] = {}
    sequence: List[str] = []
    set_targets: List[str] = []
    total_animation_wait_ms = 0
    total_wait_ms = 0

    for task in root.findall(".//Task"):
        task_type = (task.findtext("TaskType") or "").strip()
        if not task_type:
            continue
        task_counts[task_type] = task_counts.get(task_type, 0) + 1
        if len(sequence) < 40:
            sequence.append(task_type)
        if task_type == "TASK_WAIT_FOR_ANIM":
            total_animation_wait_ms += _safe_int(task.findtext("Thousandths"), 0)
        elif task_type == "TASK_WAIT":
            total_wait_ms += _safe_int(task.findtext("Thousandths"), 0)
        elif task_type == "TASK_SET_TASK_LIST":
            target = (task.findtext("TaskList") or "").strip()
            if target:
                set_targets.append(target)

    return {
        "file": path.name,
        "principal_task": (root.findtext(".//PrincipalTask") or "").strip(),
        "task_counts": dict(sorted(task_counts.items(), key=lambda kv: kv[0])),
        "task_sequence_head": sequence,
        "task_set_task_list_targets": sorted(set(set_targets)),
        "total_animation_wait_ms": total_animation_wait_ms,
        "total_wait_ms": total_wait_ms,
    }


def _build_overlay_tasklist_index(config_roots: List[str]) -> Dict[str, Path]:
    index: Dict[str, Path] = {}
    for raw_root in config_roots:
        root = Path(raw_root)
        tasklist_dir = root / "TaskLists"
        if not tasklist_dir.exists():
            continue
        for path in tasklist_dir.glob("*.xml"):
            index[path.name.lower()] = path
    return index


def _resolve_tasklist_by_name(
    name: str,
    overlay_index: Dict[str, Path],
    cache: Dict[str, Optional[Dict[str, Any]]],
) -> Optional[Dict[str, Any]]:
    key = _canonical_tasklist_filename(name)
    if not key:
        return None
    path = overlay_index.get(key)
    if path is None:
        return None
    if key not in cache:
        cache[key] = _parse_tasklist_file(path)
    return cache.get(key)


def _camp_evidence_from_tasklists(
    worker_data: Dict[str, Any],
    overlay_index: Dict[str, Path],
    overlay_cache: Dict[str, Optional[Dict[str, Any]]],
) -> Dict[str, Any]:
    resolved = worker_data.get("resolved_declared_tasklists", {})

    idle_tags = ("WorkIdleTaskList", "EatIdleTaskList", "RestIdleTaskList")
    idle_tasklists: Dict[str, Any] = {}
    has_go_to_camp_in_idle_start = False
    has_change_work_time_camp_in_idle_chain = False
    idle_followup_candidates: List[str] = []
    idle_followups: Dict[str, Any] = {}

    for tag in idle_tags:
        entry = resolved.get(tag)
        if not isinstance(entry, dict):
            continue
        summary = entry.get("summary", {})
        task_counts = summary.get("task_counts", {})
        if _safe_int(task_counts.get("TASK_GO_TO_CAMP"), 0) > 0:
            has_go_to_camp_in_idle_start = True
        targets = summary.get("task_set_task_list_targets", []) or []
        for target in targets:
            if target not in idle_followup_candidates:
                idle_followup_candidates.append(target)
        idle_tasklists[tag] = {
            "file": entry.get("resolved_file"),
            "section": entry.get("section"),
            "task_counts": task_counts,
            "task_set_task_list_targets": targets,
        }

    for target in idle_followup_candidates:
        parsed = _resolve_tasklist_by_name(target, overlay_index, overlay_cache)
        if not isinstance(parsed, dict):
            continue
        idle_followups[target] = parsed
        if _safe_int(parsed.get("task_counts", {}).get("TASK_CHANGE_WORK_TIME_CAMP"), 0) > 0:
            has_change_work_time_camp_in_idle_chain = True

    # Evidence for "try building first, then fallback logic".
    eat_start = resolved.get("EatTaskList", {}).get("summary", {})
    rest_start = resolved.get("RestTaskList", {}).get("summary", {})
    eat_counts = eat_start.get("task_counts", {})
    rest_counts = rest_start.get("task_counts", {})

    has_eat_success_check = _safe_int(
        eat_counts.get("TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS"), 0
    ) > 0
    has_rest_success_check = _safe_int(
        rest_counts.get("TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS"), 0
    ) > 0

    return {
        "idle_tasklists": idle_tasklists,
        "idle_followups": idle_followups,
        "has_go_to_camp_in_idle_start": has_go_to_camp_in_idle_start,
        "has_change_work_time_camp_in_idle_chain": has_change_work_time_camp_in_idle_chain,
        "has_eat_building_success_check": has_eat_success_check,
        "has_rest_building_success_check": has_rest_success_check,
    }


def _extract_map_camps(mapdata_path: Path) -> Dict[str, Any]:
    if not mapdata_path.exists():
        return {"mapdata_found": False}

    root = ET.parse(mapdata_path).getroot()
    camps: List[Dict[str, Any]] = []
    for ent in root.findall(".//Entity"):
        etype = (ent.findtext("Type") or "").strip()
        name = (ent.findtext("Name") or "").strip()
        text = f"{etype} {name}".lower()
        if "camp" not in text:
            continue
        x = _safe_float(ent.findtext("Position/X"), 0.0)
        y = _safe_float(ent.findtext("Position/Y"), 0.0)
        camps.append(
            {
                "type": etype,
                "name": name,
                "x": x,
                "y": y,
                "player_id": _safe_int(ent.findtext("PlayerID"), 0),
            }
        )

    by_prefix: Dict[str, int] = {
        "CB_Camp": 0,
        "CB_MinerCamp": 0,
        "XD_Camp": 0,
        "XD_Camp_Internal": 0,
        "XD_LargeCampFire": 0,
        "other_camp_named": 0,
    }
    for c in camps:
        typ = c["type"]
        if typ.startswith("CB_Camp"):
            by_prefix["CB_Camp"] += 1
        elif typ.startswith("CB_MinerCamp"):
            by_prefix["CB_MinerCamp"] += 1
        elif typ == "XD_Camp":
            by_prefix["XD_Camp"] += 1
        elif typ == "XD_Camp_Internal":
            by_prefix["XD_Camp_Internal"] += 1
        elif typ == "XD_LargeCampFire":
            by_prefix["XD_LargeCampFire"] += 1
        else:
            by_prefix["other_camp_named"] += 1

    return {
        "mapdata_found": True,
        "mapdata_path": str(mapdata_path),
        "camp_entity_count": len(camps),
        "camp_type_counts": by_prefix,
        "camp_entities": camps,
    }


def build_conditions(
    truth_model: Dict[str, Any],
    mapdata_path: Path,
) -> Dict[str, Any]:
    meta = truth_model.get("meta", {})
    source_roots = meta.get("config_roots", [])
    overlay_index = _build_overlay_tasklist_index(source_roots)
    overlay_cache: Dict[str, Optional[Dict[str, Any]]] = {}

    workers = truth_model.get("workers", {})
    logic_worktime = truth_model.get("global_truth", {}).get("logic_worktime", {})
    camp_internal = truth_model.get("global_truth", {}).get("camp_internal", {})
    camp_large_fire = truth_model.get("global_truth", {}).get("camp_large_fire", {})

    worker_conditions: Dict[str, Any] = {}
    for worker_name, worker_data in sorted(workers.items()):
        movement = worker_data.get("movement", {})
        worktime = worker_data.get("worktime_truth")
        camp_task_evidence = _camp_evidence_from_tasklists(
            worker_data, overlay_index, overlay_cache
        )

        worker_conditions[worker_name] = {
            "env_name": worker_data.get("env_name"),
            "has_worktime": worker_data.get("has_worktime"),
            "camper_range": movement.get("camper_range"),
            "work_time_change_camp": (worktime or {}).get("work_time_change_camp"),
            "work_time_threshold_global": logic_worktime.get("threshold_work"),
            "work_time_base_global": logic_worktime.get("base"),
            "decision_dependencies": [
                "worker has worktime and falls into eat/rest/idle cycle",
                "farm/residence availability and reachability checks in tasklists",
                "camper range limit from CCamperBehaviorProperties.Range",
                "idle path uses TASK_GO_TO_CAMP then TASK_CHANGE_WORK_TIME_CAMP",
            ]
            if worker_data.get("has_worktime")
            else [
                "no worker worktime cycle (serf/non-worker behavior)",
            ],
            "camp_task_evidence": camp_task_evidence,
        }

    map_camp_info = _extract_map_camps(mapdata_path)

    summary = {
        "workers_with_worktime": len(
            [w for w, d in worker_conditions.items() if d.get("has_worktime")]
        ),
        "workers_with_go_to_camp_in_idle_start": len(
            [
                w
                for w, d in worker_conditions.items()
                if d.get("camp_task_evidence", {}).get("has_go_to_camp_in_idle_start")
            ]
        ),
        "workers_with_change_work_time_camp_in_idle_chain": len(
            [
                w
                for w, d in worker_conditions.items()
                if d.get("camp_task_evidence", {}).get("has_change_work_time_camp_in_idle_chain")
            ]
        ),
    }

    return {
        "meta": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "source_worker_truth_model": str(DEFAULT_TRUTH_MODEL),
            "source_config_roots": source_roots,
            "notes": [
                "This is XML/tasklist-derived evidence.",
                "Exact low-level branch handling inside tasks (e.g. success/fail internals) may be implemented in engine code.",
            ],
        },
        "global_camp_parameters": {
            "logic_worktime": logic_worktime,
            "camp_internal": camp_internal,
            "camp_large_fire": camp_large_fire,
        },
        "worker_camp_conditions": worker_conditions,
        "map_camp_entities": map_camp_info,
        "summary": summary,
    }


def build_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# Camp And Worker Condition Report")
    lines.append("")
    summary = report.get("summary", {})
    lines.append(f"- Workers with worktime: {summary.get('workers_with_worktime', 0)}")
    lines.append(
        f"- Workers with `TASK_GO_TO_CAMP` in idle-start: {summary.get('workers_with_go_to_camp_in_idle_start', 0)}"
    )
    lines.append(
        f"- Workers with `TASK_CHANGE_WORK_TIME_CAMP` in idle-chain: {summary.get('workers_with_change_work_time_camp_in_idle_chain', 0)}"
    )
    lines.append("")

    global_params = report.get("global_camp_parameters", {})
    logic_worktime = global_params.get("logic_worktime", {})
    lines.append("## Global Parameters")
    lines.append("")
    lines.append(f"- WorkTimeBase: {logic_worktime.get('base')}")
    lines.append(f"- WorkTimeThresholdWork: {logic_worktime.get('threshold_work')}")
    lines.append(f"- ForceToWorkPenalty: {logic_worktime.get('force_to_work_penalty')}")
    camp_internal = global_params.get("camp_internal", {})
    lines.append(f"- Camp Slot Count (`XD_Camp_Internal`): {camp_internal.get('slot_count')}")
    lines.append(f"- Camp RemoveDelay: {camp_internal.get('remove_delay_seconds')}s")
    lines.append("")

    lines.append("## Map Camp Entities")
    lines.append("")
    map_info = report.get("map_camp_entities", {})
    if not map_info.get("mapdata_found"):
        lines.append("- mapdata.xml not found")
    else:
        lines.append(f"- mapdata: `{map_info.get('mapdata_path')}`")
        lines.append(f"- camp-entity count: {map_info.get('camp_entity_count')}")
        counts = map_info.get("camp_type_counts", {})
        for key in (
            "CB_Camp",
            "CB_MinerCamp",
            "XD_Camp",
            "XD_Camp_Internal",
            "XD_LargeCampFire",
            "other_camp_named",
        ):
            lines.append(f"- {key}: {counts.get(key, 0)}")
    lines.append("")

    lines.append("## Worker Highlights")
    lines.append("")
    for worker_name, data in sorted(report.get("worker_camp_conditions", {}).items()):
        if not data.get("has_worktime"):
            continue
        evidence = data.get("camp_task_evidence", {})
        lines.append(f"### {worker_name}")
        lines.append(f"- CamperRange: {data.get('camper_range')}")
        lines.append(f"- WorkTimeChangeCamp: {data.get('work_time_change_camp')}")
        lines.append(
            f"- Idle has TASK_GO_TO_CAMP: {evidence.get('has_go_to_camp_in_idle_start')}"
        )
        lines.append(
            f"- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: {evidence.get('has_change_work_time_camp_in_idle_chain')}"
        )
        lines.append(
            f"- Eat path has success check: {evidence.get('has_eat_building_success_check')}"
        )
        lines.append(
            f"- Rest path has success check: {evidence.get('has_rest_building_success_check')}"
        )
        lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "- Worker camping is primarily task-driven (`TASK_GO_TO_CAMP` + `TASK_CHANGE_WORK_TIME_CAMP`) and parameterized by `CamperRange` + worktime values."
    )
    lines.append(
        "- Static map camps (`CB_Camp*`/`CB_MinerCamp*`) are separate from worker rest logic and may be absent on a specific map."
    )
    lines.append(
        "- If a map has no `CB_Camp*` placements, worker camp behavior still exists via dynamic camp tasks."
    )
    lines.append(
        "- Exact branch internals for task success/failure checks are engine-side and not fully encoded in XML."
    )
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract camp placement/usage conditions from worker truth and map data."
    )
    parser.add_argument(
        "--truth-model",
        type=Path,
        default=DEFAULT_TRUTH_MODEL,
        help=f"Input worker truth model JSON (default: {DEFAULT_TRUTH_MODEL})",
    )
    parser.add_argument(
        "--mapdata",
        type=Path,
        default=DEFAULT_MAPDATA,
        help=f"Input mapdata XML (default: {DEFAULT_MAPDATA})",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=DEFAULT_OUTPUT_JSON,
        help=f"Output JSON report (default: {DEFAULT_OUTPUT_JSON})",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=DEFAULT_OUTPUT_MD,
        help=f"Output markdown report (default: {DEFAULT_OUTPUT_MD})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    truth_path = args.truth_model.resolve()
    mapdata_path = args.mapdata.resolve()
    out_json = args.output_json.resolve()
    out_md = args.output_md.resolve()

    if not truth_path.exists():
        raise FileNotFoundError(f"worker truth model not found: {truth_path}")

    truth_model = json.loads(truth_path.read_text(encoding="utf-8"))
    report = build_conditions(truth_model, mapdata_path)
    md = build_markdown(report)

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(md, encoding="utf-8")

    summary = report.get("summary", {})
    print("Camp/worker condition report generated")
    print(f"Truth model: {truth_path}")
    print(f"Mapdata: {mapdata_path if mapdata_path.exists() else 'not found'}")
    print(f"JSON: {out_json}")
    print(f"MD: {out_md}")
    print(f"Workers with worktime: {summary.get('workers_with_worktime', 0)}")
    print(
        "Workers with TASK_GO_TO_CAMP in idle-start: "
        f"{summary.get('workers_with_go_to_camp_in_idle_start', 0)}"
    )
    print(
        "Workers with TASK_CHANGE_WORK_TIME_CAMP in idle-chain: "
        f"{summary.get('workers_with_change_work_time_camp_in_idle_chain', 0)}"
    )


if __name__ == "__main__":
    main()

