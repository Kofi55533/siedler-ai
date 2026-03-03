#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build complete worker behavior logic from worker_truth_model + original TaskLists.

Output:
- config/worker_behavior_logic.json
- config/worker_behavior_logic.md
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
import xml.etree.ElementTree as ET


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_TRUTH_MODEL = SCRIPT_DIR / "config" / "worker_truth_model.json"
DEFAULT_OUTPUT_JSON = SCRIPT_DIR / "config" / "worker_behavior_logic.json"
DEFAULT_OUTPUT_MD = SCRIPT_DIR / "config" / "worker_behavior_logic.md"


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


def _canonical_tasklist_name(name: str) -> str:
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


def _build_tasklist_index(config_roots: List[str]) -> Dict[str, Path]:
    index: Dict[str, Path] = {}
    for raw_root in config_roots:
        root = Path(raw_root)
        task_dir = root / "TaskLists"
        if not task_dir.exists():
            continue
        for file in task_dir.glob("*.xml"):
            # overlay semantics: later roots overwrite earlier roots
            index[file.name.lower()] = file
    return index


def _classify_task_types(task_counts: Dict[str, int]) -> Dict[str, List[str]]:
    all_types = sorted(task_counts.keys())
    checks = [t for t in all_types if t.startswith("TASK_CHECK_")]
    movement = [
        t
        for t in all_types
        if (
            "GO_TO" in t
            or t in {"TASK_WALK", "TASK_TURN_TO_TARGET_ORIENTATION", "TASK_GO_TO_CAMP"}
        )
    ]
    worktime = [
        t
        for t in all_types
        if (
            "WORK_TIME" in t
            or t
            in {
                "TASK_EAT_WAIT",
                "TASK_REST_WAIT",
                "TASK_WORK_WAIT_UNTIL",
                "TASK_WAIT_EXTRACTION_DELAY",
            }
        )
    ]
    resource = [
        t
        for t in all_types
        if (
            "RESOURCE" in t
            or t in {"TASK_EXTRACT_RESOURCE", "TASK_EXTRACT_WOOD"}
        )
    ]
    return {
        "checks": checks,
        "movement": movement,
        "worktime": worktime,
        "resource": resource,
    }


def _parse_tasklist(path: Path) -> Optional[Dict[str, Any]]:
    root = _parse_xml_safe(path)
    if root is None:
        return None

    task_counts: Dict[str, int] = {}
    sequence_head: List[str] = []
    set_targets: List[str] = []
    total_animation_wait_ms = 0
    total_wait_ms = 0

    for task in root.findall(".//Task"):
        task_type = (task.findtext("TaskType") or "").strip()
        if not task_type:
            continue
        task_counts[task_type] = task_counts.get(task_type, 0) + 1
        if len(sequence_head) < 60:
            sequence_head.append(task_type)

        if task_type == "TASK_SET_TASK_LIST":
            target = (task.findtext("TaskList") or "").strip()
            if target:
                set_targets.append(target)
        elif task_type == "TASK_WAIT_FOR_ANIM":
            total_animation_wait_ms += _safe_int(task.findtext("Thousandths"), 0)
        elif task_type == "TASK_WAIT":
            total_wait_ms += _safe_int(task.findtext("Thousandths"), 0)

    task_counts_sorted = dict(sorted(task_counts.items(), key=lambda kv: kv[0]))
    classes = _classify_task_types(task_counts_sorted)

    return {
        "file": path.name,
        "principal_task": (root.findtext(".//PrincipalTask") or "").strip(),
        "task_counts": task_counts_sorted,
        "task_sequence_head": sequence_head,
        "task_set_task_list_targets": sorted(set(set_targets)),
        "total_animation_wait_ms": total_animation_wait_ms,
        "total_wait_ms": total_wait_ms,
        "task_mined_resource_count": task_counts_sorted.get("TASK_MINED_RESOURCE", 0),
        "task_refine_resource_count": task_counts_sorted.get("TASK_REFINE_RESOURCE", 0),
        "task_change_work_time_work_count": task_counts_sorted.get(
            "TASK_CHANGE_WORK_TIME_WORK", 0
        ),
        "task_work_wait_until_count": task_counts_sorted.get("TASK_WORK_WAIT_UNTIL", 0),
        "classifications": classes,
    }


def _resolve_tasklist_path(tasklist_name: str, index: Dict[str, Path]) -> Optional[Path]:
    key = _canonical_tasklist_name(tasklist_name)
    if not key:
        return None
    return index.get(key)


def _initial_tasklist_seeds(worker_data: Dict[str, Any]) -> List[str]:
    seeds: List[str] = []
    declared = worker_data.get("declared_tasklists", {})
    for _, value in sorted(declared.items(), key=lambda kv: kv[0]):
        if value and value not in seeds:
            seeds.append(value)

    move_name = worker_data.get("movement", {}).get("move_task_list")
    if move_name and move_name not in seeds:
        seeds.append(move_name)

    primary = worker_data.get("work_cycle_truth", {}).get("primary_work_tasklist")
    if isinstance(primary, dict):
        file_name = primary.get("file")
        if file_name and file_name not in seeds:
            seeds.append(file_name)

    miner_lists = worker_data.get("work_cycle_truth", {}).get("miner_tasklists", {})
    if isinstance(miner_lists, dict):
        for _, entry in sorted(miner_lists.items(), key=lambda kv: kv[0]):
            file_name = (entry or {}).get("file")
            if file_name and file_name not in seeds:
                seeds.append(file_name)

    serf_extract = (worker_data.get("serf_extraction_truth") or {}).get(
        "extract_tasklists", {}
    )
    if isinstance(serf_extract, dict):
        for _, entry in sorted(serf_extract.items(), key=lambda kv: kv[0]):
            if not isinstance(entry, dict):
                continue
            file_name = entry.get("file")
            if file_name and file_name not in seeds:
                seeds.append(file_name)

    return seeds


def _build_task_graph(
    seeds: List[str],
    tasklist_index: Dict[str, Path],
    parse_cache: Dict[str, Optional[Dict[str, Any]]],
) -> Dict[str, Any]:
    queue: List[str] = list(seeds)
    visited: Set[str] = set()
    nodes: Dict[str, Dict[str, Any]] = {}
    unresolved: List[str] = []
    edges: List[Dict[str, str]] = []

    while queue:
        raw_name = queue.pop(0)
        key = _canonical_tasklist_name(raw_name)
        if not key or key in visited:
            continue
        visited.add(key)

        path = _resolve_tasklist_path(raw_name, tasklist_index)
        if path is None:
            unresolved.append(raw_name)
            continue

        if key not in parse_cache:
            parse_cache[key] = _parse_tasklist(path)
        parsed = parse_cache[key]
        if not isinstance(parsed, dict):
            unresolved.append(raw_name)
            continue

        node = {
            "file": parsed.get("file"),
            "principal_task": parsed.get("principal_task"),
            "task_counts": parsed.get("task_counts", {}),
            "task_sequence_head": parsed.get("task_sequence_head", []),
            "task_set_task_list_targets": parsed.get("task_set_task_list_targets", []),
            "total_animation_wait_ms": parsed.get("total_animation_wait_ms", 0),
            "total_wait_ms": parsed.get("total_wait_ms", 0),
            "task_mined_resource_count": parsed.get("task_mined_resource_count", 0),
            "task_refine_resource_count": parsed.get("task_refine_resource_count", 0),
            "task_change_work_time_work_count": parsed.get(
                "task_change_work_time_work_count", 0
            ),
            "task_work_wait_until_count": parsed.get("task_work_wait_until_count", 0),
            "classifications": parsed.get("classifications", {}),
            "source_path": str(path),
        }
        nodes[key] = node

        for target in node["task_set_task_list_targets"]:
            edges.append({"from": key, "to": _canonical_tasklist_name(target), "reason": "TASK_SET_TASK_LIST"})
            queue.append(target)

    dedup_edges: List[Dict[str, str]] = []
    seen_edge: Set[Tuple[str, str, str]] = set()
    for e in edges:
        signature = (e["from"], e["to"], e["reason"])
        if signature in seen_edge:
            continue
        seen_edge.add(signature)
        dedup_edges.append(e)

    unresolved_sorted = sorted(set(unresolved))
    return {
        "seeds": seeds,
        "nodes": nodes,
        "edges": dedup_edges,
        "unresolved_tasklists": unresolved_sorted,
        "stats": {
            "node_count": len(nodes),
            "edge_count": len(dedup_edges),
            "unresolved_count": len(unresolved_sorted),
        },
    }


def _derive_behavior_flags(worker_data: Dict[str, Any], graph: Dict[str, Any]) -> Dict[str, Any]:
    has_worktime = bool(worker_data.get("has_worktime"))
    movement = worker_data.get("movement", {})
    worktime = worker_data.get("worktime_truth") or {}
    nodes = graph.get("nodes", {})

    def _node_for_declared(tag: str) -> Optional[Dict[str, Any]]:
        declared = worker_data.get("declared_tasklists", {}).get(tag)
        if not declared:
            return None
        return nodes.get(_canonical_tasklist_name(declared))

    eat_node = _node_for_declared("EatTaskList")
    rest_node = _node_for_declared("RestTaskList")
    work_idle_node = _node_for_declared("WorkIdleTaskList")
    eat_idle_node = _node_for_declared("EatIdleTaskList")
    rest_idle_node = _node_for_declared("RestIdleTaskList")

    idle_nodes = [n for n in (work_idle_node, eat_idle_node, rest_idle_node) if n]
    has_go_to_camp = any(
        _safe_int(node.get("task_counts", {}).get("TASK_GO_TO_CAMP"), 0) > 0 for node in idle_nodes
    )

    idle_targets: Set[str] = set()
    for node in idle_nodes:
        for t in node.get("task_set_task_list_targets", []):
            idle_targets.add(_canonical_tasklist_name(t))

    has_change_work_time_camp = False
    for key in idle_targets:
        idle_follow = nodes.get(key)
        if not idle_follow:
            continue
        if _safe_int(idle_follow.get("task_counts", {}).get("TASK_CHANGE_WORK_TIME_CAMP"), 0) > 0:
            has_change_work_time_camp = True
            break

    eat_has_success_check = (
        _safe_int((eat_node or {}).get("task_counts", {}).get("TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS"), 0)
        > 0
    )
    rest_has_success_check = (
        _safe_int((rest_node or {}).get("task_counts", {}).get("TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS"), 0)
        > 0
    )

    return {
        "has_worktime": has_worktime,
        "camper_range": movement.get("camper_range"),
        "work_time_change_camp": worktime.get("work_time_change_camp"),
        "work_wait_until_ms": worktime.get("work_wait_until"),
        "has_go_to_camp_in_idle_start": has_go_to_camp,
        "has_change_work_time_camp_in_idle_chain": has_change_work_time_camp,
        "eat_path_has_success_check": eat_has_success_check,
        "rest_path_has_success_check": rest_has_success_check,
    }


def build_logic_model(truth_model: Dict[str, Any]) -> Dict[str, Any]:
    meta = truth_model.get("meta", {})
    config_roots = meta.get("config_roots", [])
    tasklist_index = _build_tasklist_index(config_roots)
    parse_cache: Dict[str, Optional[Dict[str, Any]]] = {}

    workers_logic: Dict[str, Any] = {}
    for worker_name, worker_data in sorted(truth_model.get("workers", {}).items()):
        seeds = _initial_tasklist_seeds(worker_data)
        graph = _build_task_graph(seeds, tasklist_index, parse_cache)
        flags = _derive_behavior_flags(worker_data, graph)

        workers_logic[worker_name] = {
            "env_name": worker_data.get("env_name"),
            "source_file": worker_data.get("source_file"),
            "movement": worker_data.get("movement", {}),
            "worktime_truth": worker_data.get("worktime_truth"),
            "declared_tasklists": worker_data.get("declared_tasklists", {}),
            "task_graph": graph,
            "derived_flags": flags,
        }

    summary = {
        "worker_count": len(workers_logic),
        "workers_with_worktime": len(
            [w for w, d in workers_logic.items() if d.get("derived_flags", {}).get("has_worktime")]
        ),
        "workers_with_camp_idle_go_to": len(
            [
                w
                for w, d in workers_logic.items()
                if d.get("derived_flags", {}).get("has_go_to_camp_in_idle_start")
            ]
        ),
        "workers_with_camp_worktime_change": len(
            [
                w
                for w, d in workers_logic.items()
                if d.get("derived_flags", {}).get("has_change_work_time_camp_in_idle_chain")
            ]
        ),
        "workers_with_unresolved_tasklists": sorted(
            [
                w
                for w, d in workers_logic.items()
                if d.get("task_graph", {}).get("stats", {}).get("unresolved_count", 0) > 0
            ]
        ),
    }

    return {
        "meta": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "source_worker_truth_model": str(DEFAULT_TRUTH_MODEL),
            "config_roots": config_roots,
            "tasklist_file_count": len(tasklist_index),
            "notes": [
                "Logic graph is built from XML tasklists and declared worker behavior props.",
                "Low-level conditional branch internals inside task execution are engine-side.",
            ],
        },
        "global_truth": truth_model.get("global_truth", {}),
        "workers": workers_logic,
        "summary": summary,
    }


def build_markdown(model: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# Worker Behavior Logic (Complete Extraction)")
    lines.append("")
    summary = model.get("summary", {})
    lines.append(f"- Workers: {summary.get('worker_count', 0)}")
    lines.append(f"- Workers with worktime: {summary.get('workers_with_worktime', 0)}")
    lines.append(
        f"- Workers with `TASK_GO_TO_CAMP` in idle-start: {summary.get('workers_with_camp_idle_go_to', 0)}"
    )
    lines.append(
        f"- Workers with `TASK_CHANGE_WORK_TIME_CAMP` in idle-chain: {summary.get('workers_with_camp_worktime_change', 0)}"
    )
    unresolved_workers = summary.get("workers_with_unresolved_tasklists", [])
    lines.append(f"- Workers with unresolved tasklists: {len(unresolved_workers)}")
    lines.append("")

    for worker_name, data in sorted(model.get("workers", {}).items()):
        flags = data.get("derived_flags", {})
        graph = data.get("task_graph", {})
        lines.append(f"## {worker_name}")
        lines.append(f"- Env name: {data.get('env_name')}")
        lines.append(f"- Has worktime: {flags.get('has_worktime')}")
        lines.append(f"- CamperRange: {flags.get('camper_range')}")
        lines.append(f"- WorkTimeChangeCamp: {flags.get('work_time_change_camp')}")
        lines.append(f"- WorkWaitUntil(ms): {flags.get('work_wait_until_ms')}")
        lines.append(
            f"- Eat path success-check task: {flags.get('eat_path_has_success_check')}"
        )
        lines.append(
            f"- Rest path success-check task: {flags.get('rest_path_has_success_check')}"
        )
        lines.append(
            f"- Idle has GO_TO_CAMP: {flags.get('has_go_to_camp_in_idle_start')}"
        )
        lines.append(
            f"- Idle chain has CHANGE_WORK_TIME_CAMP: {flags.get('has_change_work_time_camp_in_idle_chain')}"
        )
        lines.append(
            f"- Task graph: {graph.get('stats', {}).get('node_count', 0)} nodes, "
            f"{graph.get('stats', {}).get('edge_count', 0)} edges, "
            f"{graph.get('stats', {}).get('unresolved_count', 0)} unresolved"
        )
        lines.append("")
        lines.append("### Entry Tasklists")
        for tag, name in sorted(data.get("declared_tasklists", {}).items()):
            lines.append(f"- {tag}: {name}")
        move_task = data.get("movement", {}).get("move_task_list")
        if move_task:
            lines.append(f"- MoveTaskList: {move_task}")
        lines.append("")

        lines.append("### Task Graph Nodes")
        nodes = graph.get("nodes", {})
        for key, node in sorted(nodes.items()):
            lines.append(f"- {key} ({node.get('principal_task')})")
            lines.append(f"  file: {node.get('file')}")
            transitions = node.get("task_set_task_list_targets", [])
            if transitions:
                lines.append(f"  set_task_list_targets: {', '.join(transitions)}")
            checks = node.get("classifications", {}).get("checks", [])
            if checks:
                lines.append(f"  checks: {', '.join(checks)}")
            resource = node.get("classifications", {}).get("resource", [])
            if resource:
                lines.append(f"  resource tasks: {', '.join(resource)}")
            worktime = node.get("classifications", {}).get("worktime", [])
            if worktime:
                lines.append(f"  worktime tasks: {', '.join(worktime)}")
        unresolved = graph.get("unresolved_tasklists", [])
        if unresolved:
            lines.append("")
            lines.append("### Unresolved")
            for name in unresolved:
                lines.append(f"- {name}")
        lines.append("")

    lines.append("## Limitation")
    lines.append("- XML/tasklists expose most behavior structure and parameters.")
    lines.append("- Exact internal branch semantics per task execution remain in engine code.")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build complete behavior logic model for all workers."
    )
    parser.add_argument(
        "--truth-model",
        type=Path,
        default=DEFAULT_TRUTH_MODEL,
        help=f"Input worker truth model JSON (default: {DEFAULT_TRUTH_MODEL})",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=DEFAULT_OUTPUT_JSON,
        help=f"Output JSON path (default: {DEFAULT_OUTPUT_JSON})",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=DEFAULT_OUTPUT_MD,
        help=f"Output markdown path (default: {DEFAULT_OUTPUT_MD})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    truth_path = args.truth_model.resolve()
    out_json = args.output_json.resolve()
    out_md = args.output_md.resolve()

    if not truth_path.exists():
        raise FileNotFoundError(f"truth model not found: {truth_path}")

    truth_model = json.loads(truth_path.read_text(encoding="utf-8"))
    model = build_logic_model(truth_model)
    md = build_markdown(model)

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(model, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(md, encoding="utf-8")

    summary = model.get("summary", {})
    print("Worker behavior logic model generated")
    print(f"Input: {truth_path}")
    print(f"JSON: {out_json}")
    print(f"MD: {out_md}")
    print(f"Workers: {summary.get('worker_count', 0)}")
    print(f"Workers with worktime: {summary.get('workers_with_worktime', 0)}")
    print(
        "Workers with camp idle go-to: "
        f"{summary.get('workers_with_camp_idle_go_to', 0)}"
    )
    print(
        "Workers with camp worktime-change: "
        f"{summary.get('workers_with_camp_worktime_change', 0)}"
    )
    print(
        "Workers with unresolved tasklists: "
        f"{len(summary.get('workers_with_unresolved_tasklists', []))}"
    )


if __name__ == "__main__":
    main()
