#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a simulation-ready worker behavior contract from extracted engine artifacts.

Inputs:
- config/worker_truth_model.json
- config/worker_behavior_logic.json
- config/camp_worker_conditions.json
- config/worker_camp_path_branch_matrix.json
- config/all_original_values.jsonl (optional, for global scalar keys)

Outputs:
- config/worker_sim_contract.json
- config/worker_sim_contract.md
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent

DEFAULT_TRUTH = SCRIPT_DIR / "config" / "worker_truth_model.json"
DEFAULT_LOGIC = SCRIPT_DIR / "config" / "worker_behavior_logic.json"
DEFAULT_CAMP = SCRIPT_DIR / "config" / "camp_worker_conditions.json"
DEFAULT_BRANCH = SCRIPT_DIR / "config" / "worker_camp_path_branch_matrix.json"
DEFAULT_VALUES = SCRIPT_DIR / "config" / "all_original_values.jsonl"

DEFAULT_OUT_JSON = SCRIPT_DIR / "config" / "worker_sim_contract.json"
DEFAULT_OUT_MD = SCRIPT_DIR / "config" / "worker_sim_contract.md"


GLOBAL_KEY_PATTERNS = {
    "WorkerFlightDistance": "worker_flight_distance",
    "AlarmRechargeTime": "alarm_recharge_time_ms",
    "ReAttachWorkerFrequency": "reattach_worker_frequency",
    "MaximumDistanceWorkerToFarm": "max_distance_worker_to_farm",
    "MaximumDistanceWorkerToResidence": "max_distance_worker_to_residence",
}


ANCHOR_FUNCTIONS = {
    "0x004ed68d": "TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS branch",
    "0x004ed9e7": "TASK_GO_TO_CAMP anchor",
    "0x004ed50a": "TASK_CHANGE_WORK_TIME_CAMP anchor",
    "0x006781a8": "worker reattach/distance checks",
    "0x0063201a": "path runtime: next waypoint / orientation / pathing used",
    "0x00631e3d": "path runtime: fine/coarse path",
    "0x0062767a": "dynamic blocking area / blocked points",
    "0x00645c1c": "CCampBehavior branch",
    "0x00645e98": "CCamperBehavior branch",
    "0x0069c652": "CWorkerBehavior branching hub",
    "0x0069ce8f": "CWorkerFleeBehavior branching hub",
}


def _safe_int(v: Any) -> Optional[int]:
    try:
        return int(v)
    except Exception:
        return None


def _safe_float(v: Any) -> Optional[float]:
    try:
        return float(v)
    except Exception:
        return None


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_global_scalars(values_jsonl: Path) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    if not values_jsonl.exists():
        return out

    with values_jsonl.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            try:
                item = json.loads(line)
            except Exception:
                continue
            path = str(item.get("path", ""))
            value = item.get("value")
            for needle, key in GLOBAL_KEY_PATTERNS.items():
                if needle in path and key not in out:
                    out[key] = {
                        "key": needle,
                        "value_raw": value,
                        "value_int": _safe_int(value),
                        "value_float": _safe_float(value),
                        "file": item.get("file"),
                        "path": path,
                    }
    return out


def _canonical_shared_state_nodes(workers_logic: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    # Use first non-serf worktime worker as canonical source for shared nodes.
    canonical: Dict[str, Dict[str, Any]] = {}
    ordered = sorted(workers_logic.items(), key=lambda kv: kv[0])
    for _, w in ordered:
        if not w.get("derived_flags", {}).get("has_worktime", False):
            continue
        nodes = w.get("task_graph", {}).get("nodes", {})
        for key in [
            "tl_worker_idle_start.xml",
            "tl_worker_idle.xml",
            "tl_worker_eat_start.xml",
            "tl_worker_eat.xml",
            "tl_worker_rest_start.xml",
            "tl_worker_rest.xml",
            "tl_worker_leave.xml",
            "tl_worker_flee.xml",
            "tl_worker_go_to_defendable_building.xml",
        ]:
            if key in nodes:
                canonical[key] = nodes[key]
        break
    return canonical


def _check_shared_consistency(workers_logic: Dict[str, Any], node_names: List[str]) -> Dict[str, Any]:
    mismatches: List[Dict[str, Any]] = []
    base: Dict[str, Dict[str, int]] = {}

    for wname, w in sorted(workers_logic.items()):
        if not w.get("derived_flags", {}).get("has_worktime", False):
            continue
        nodes = w.get("task_graph", {}).get("nodes", {})
        for node_name in node_names:
            if node_name not in nodes:
                mismatches.append(
                    {"worker": wname, "node": node_name, "issue": "missing_node"}
                )
                continue
            counts = nodes[node_name].get("task_counts", {})
            if node_name not in base:
                base[node_name] = counts
                continue
            if counts != base[node_name]:
                mismatches.append(
                    {
                        "worker": wname,
                        "node": node_name,
                        "issue": "task_counts_mismatch",
                    }
                )

    return {
        "is_consistent": len(mismatches) == 0,
        "mismatches": mismatches,
    }


def _build_common_rules(canonical_nodes: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    rules: List[Dict[str, Any]] = []

    def node_seq(name: str) -> List[str]:
        return list((canonical_nodes.get(name, {}) or {}).get("task_sequence_head", []))

    def node_counts(name: str) -> Dict[str, int]:
        return dict((canonical_nodes.get(name, {}) or {}).get("task_counts", {}))

    rules.append(
        {
            "id": "idle_start_to_idle",
            "when": "cycle enters idle_start",
            "tasks": node_seq("tl_worker_idle_start.xml"),
            "key_tasks_required": ["TASK_GO_TO_CAMP", "TASK_SET_TASK_LIST"],
            "effects": [
                "worker leaves current building context",
                "worker goes to camp",
                "worker orientation aligns to camp",
                "task list transitions to idle loop",
            ],
            "dependencies": ["camper_range", "camp availability/pathing"],
        }
    )
    rules.append(
        {
            "id": "idle_loop_camp_recovery",
            "when": "worker is in idle loop",
            "tasks": node_seq("tl_worker_idle.xml"),
            "task_counts": node_counts("tl_worker_idle.xml"),
            "key_tasks_required": ["TASK_CHANGE_WORK_TIME_CAMP", "TASK_ADVANCE_IN_CYCLE"],
            "effects": [
                "random idle animations",
                "worktime receives camp delta",
                "cycle advances to next decision state",
            ],
            "dependencies": ["work_time_change_camp", "worktime state variable"],
        }
    )
    rules.append(
        {
            "id": "eat_start_path_and_check",
            "when": "cycle chooses eat",
            "tasks": node_seq("tl_worker_eat_start.xml"),
            "key_tasks_required": [
                "TASK_GO_TO_EAT_BUILDING",
                "TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS",
                "TASK_SET_TASK_LIST",
            ],
            "effects": [
                "attempt move to eat building",
                "branch on GO_TO_EAT success check",
                "enter building and transition to eat loop",
            ],
            "dependencies": ["eat building availability", "pathfinding success"],
        }
    )
    rules.append(
        {
            "id": "eat_loop_farm_recovery",
            "when": "worker is in eat loop",
            "tasks": node_seq("tl_worker_eat.xml"),
            "task_counts": node_counts("tl_worker_eat.xml"),
            "key_tasks_required": ["TASK_EAT_WAIT", "TASK_CHANGE_WORK_TIME_FARM"],
            "effects": [
                "eat wait",
                "worktime receives farm delta",
                "cycle advances",
            ],
            "dependencies": ["work_time_change_farm", "eat_wait"],
        }
    )
    rules.append(
        {
            "id": "rest_start_path_and_check",
            "when": "cycle chooses rest",
            "tasks": node_seq("tl_worker_rest_start.xml"),
            "key_tasks_required": [
                "TASK_GO_TO_REST_BUILDING",
                "TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS",
                "TASK_SET_TASK_LIST",
            ],
            "effects": [
                "attempt move to rest building",
                "branch on GO_TO_REST success check",
                "enter building and transition to rest loop",
            ],
            "dependencies": ["residence availability", "pathfinding success"],
        }
    )
    rules.append(
        {
            "id": "rest_loop_residence_recovery",
            "when": "worker is in rest loop",
            "tasks": node_seq("tl_worker_rest.xml"),
            "task_counts": node_counts("tl_worker_rest.xml"),
            "key_tasks_required": ["TASK_REST_WAIT", "TASK_CHANGE_WORK_TIME_RESIDENCE"],
            "effects": [
                "rest wait",
                "worktime receives residence delta",
                "cycle advances",
            ],
            "dependencies": ["work_time_change_residence", "rest_wait"],
        }
    )
    rules.append(
        {
            "id": "work_start_path_and_check",
            "when": "cycle chooses work",
            "tasks": "worker-specific TL_*_WORK_START",
            "key_tasks_required": [
                "TASK_START_WORK_IF_AT_WORKPLACE",
                "TASK_GO_TO_WORK_BUILDING",
                "TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS",
                "TASK_SET_TASK_LIST",
            ],
            "effects": [
                "optionally collect supplier goods",
                "attempt move to workplace",
                "branch on GO_TO_WORK success check",
                "transition to worker-specific work loop",
            ],
            "dependencies": ["workplace assignment", "supplier path (if needed)", "pathfinding success"],
        }
    )
    rules.append(
        {
            "id": "leave_settlement_path_and_check",
            "when": "worker leaves settlement cycle",
            "tasks": node_seq("tl_worker_leave.xml"),
            "key_tasks_required": [
                "TASK_GO_TO_LEAVE_BUILDING",
                "TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS",
                "TASK_LEAVE_SETTLEMENT",
            ],
            "effects": [
                "move to village center/leave building",
                "branch on leave path success",
                "leave settlement",
            ],
            "dependencies": ["village center availability", "pathfinding success"],
        }
    )
    rules.append(
        {
            "id": "alarm_flee_interrupt",
            "when": "fear/alarm branch activates",
            "tasks": node_seq("tl_worker_flee.xml"),
            "key_tasks_required": ["TASK_FLEE", "TASK_WAIT", "TASK_RETURN_TO_CYCLE"],
            "effects": [
                "worker interrupts normal cycle",
                "flee task executed",
                "returns to cycle after wait",
            ],
            "dependencies": ["alarm mode", "worker_flight_distance", "pathfinding"],
        }
    )
    rules.append(
        {
            "id": "go_to_defendable_building",
            "when": "defendable building branch activates",
            "tasks": node_seq("tl_worker_go_to_defendable_building.xml"),
            "key_tasks_required": [
                "TASK_MOVE_TO_DEFENDABLE_BUILDING",
                "TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS",
                "TASK_DEFEND",
            ],
            "effects": [
                "moves to defendable building",
                "branches on path success",
                "enters defend state",
            ],
            "dependencies": ["defendable building availability", "pathfinding success"],
        }
    )

    return rules


def _summarize_worker_profiles(
    truth_workers: Dict[str, Any],
    logic_workers: Dict[str, Any],
    camp_workers: Dict[str, Any],
) -> Dict[str, Any]:
    profiles: Dict[str, Any] = {}
    for wname in sorted(truth_workers.keys()):
        tw = truth_workers[wname]
        lw = logic_workers.get(wname, {})
        cw = camp_workers.get(wname, {})

        movement = tw.get("movement", {}) or {}
        worktime = tw.get("worktime_truth", {}) or {}
        flags = lw.get("derived_flags", {}) or {}
        task_graph = lw.get("task_graph", {}) or {}
        nodes = task_graph.get("nodes", {}) or {}

        work_start_nodes: List[str] = []
        work_nodes: List[str] = []
        for node_name, node in nodes.items():
            principal = str(node.get("principal_task", "") or "").strip().lower()
            if principal != "work":
                continue
            counts = node.get("task_counts", {}) or {}
            # Start nodes typically transition via TASK_SET_TASK_LIST after GO_TO/CHECK.
            if "TASK_SET_TASK_LIST" in counts:
                work_start_nodes.append(node_name)
            else:
                work_nodes.append(node_name)
        work_start_nodes = sorted(set(work_start_nodes))
        work_nodes = sorted(set(work_nodes))

        profiles[wname] = {
            "env_name": tw.get("env_name"),
            "source_file": tw.get("source_file"),
            "has_worktime": bool(tw.get("has_worktime", False)),
            "movement": {
                "speed": movement.get("speed"),
                "rotation_speed": movement.get("rotation_speed"),
                "move_task_list": movement.get("move_task_list"),
                "camper_range": movement.get("camper_range"),
                "resource_search_radius": movement.get("resource_search_radius"),
            },
            "worktime": {
                "work_wait_until": worktime.get("work_wait_until"),
                "work_time_change_work": worktime.get("work_time_change_work"),
                "work_time_change_farm": worktime.get("work_time_change_farm"),
                "work_time_change_residence": worktime.get("work_time_change_residence"),
                "work_time_change_camp": worktime.get("work_time_change_camp"),
                "work_time_max_farm": worktime.get("work_time_max_farm"),
                "work_time_max_residence": worktime.get("work_time_max_residence"),
                "eat_wait": worktime.get("eat_wait"),
                "rest_wait": worktime.get("rest_wait"),
            },
            "declared_tasklists": tw.get("declared_tasklists", {}),
            "derived_flags": {
                "has_go_to_camp_in_idle_start": flags.get("has_go_to_camp_in_idle_start"),
                "has_change_work_time_camp_in_idle_chain": flags.get(
                    "has_change_work_time_camp_in_idle_chain"
                ),
                "eat_path_has_success_check": flags.get("eat_path_has_success_check"),
                "rest_path_has_success_check": flags.get("rest_path_has_success_check"),
            },
            "work_task_nodes": {
                "work_start_nodes": work_start_nodes,
                "work_nodes": work_nodes,
            },
            "camp_dependencies": {
                "camper_range": cw.get("camper_range"),
                "work_time_change_camp": cw.get("work_time_change_camp"),
                "decision_dependencies": cw.get("decision_dependencies", []),
            },
        }
    return profiles


def _select_branch_anchors(branch_matrix: Dict[str, Any]) -> Dict[str, Any]:
    by_fn = {f["function"]: f for f in branch_matrix.get("functions", [])}
    out: Dict[str, Any] = {}
    for fn, purpose in ANCHOR_FUNCTIONS.items():
        item = by_fn.get(fn)
        if not item:
            continue
        conds = item.get("branches", {}).get("conditional_sites", []) or []
        out[fn] = {
            "purpose": purpose,
            "stats": item.get("stats", {}),
            "tags": item.get("tags", {}),
            "top_conditions": [
                {
                    "at": c.get("at"),
                    "mnemonic": c.get("mnemonic"),
                    "true_target": c.get("true_target"),
                    "false_target": c.get("false_target"),
                    "predicate_hint": c.get("predicate_hint"),
                }
                for c in conds[:10]
            ],
        }
    return out


def build_contract(
    truth: Dict[str, Any],
    logic: Dict[str, Any],
    camp: Dict[str, Any],
    branch: Dict[str, Any],
    global_scalars: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    truth_workers = truth.get("workers", {})
    logic_workers = logic.get("workers", {})
    camp_workers = camp.get("worker_camp_conditions", {})

    canonical_nodes = _canonical_shared_state_nodes(logic_workers)
    consistency = _check_shared_consistency(
        logic_workers,
        [
            "tl_worker_idle_start.xml",
            "tl_worker_idle.xml",
            "tl_worker_eat_start.xml",
            "tl_worker_eat.xml",
            "tl_worker_rest_start.xml",
            "tl_worker_rest.xml",
            "tl_worker_leave.xml",
        ],
    )

    common_rules = _build_common_rules(canonical_nodes)
    worker_profiles = _summarize_worker_profiles(truth_workers, logic_workers, camp_workers)
    branch_anchors = _select_branch_anchors(branch)

    worktime_workers = [
        w for w, d in worker_profiles.items() if d.get("has_worktime", False)
    ]
    no_worktime_workers = [
        w for w, d in worker_profiles.items() if not d.get("has_worktime", False)
    ]

    notable_variants: List[Dict[str, Any]] = []
    for wname, p in sorted(worker_profiles.items()):
        declared = p.get("declared_tasklists", {}) or {}
        variant_reasons: List[str] = []
        eat_tl = declared.get("EatTaskList")
        eat_idle_tl = declared.get("EatIdleTaskList")
        rest_tl = declared.get("RestTaskList")
        if eat_tl and eat_tl != "TL_WORKER_EAT_START":
            variant_reasons.append(f"EatTaskList={eat_tl}")
        if eat_idle_tl and eat_idle_tl != "TL_WORKER_IDLE_START":
            variant_reasons.append(f"EatIdleTaskList={eat_idle_tl}")
        if rest_tl and rest_tl != "TL_WORKER_REST_START":
            variant_reasons.append(f"RestTaskList={rest_tl}")
        if variant_reasons:
            notable_variants.append({"worker": wname, "reasons": variant_reasons})

    return {
        "meta": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "sources": {
                "worker_truth_model": str(DEFAULT_TRUTH),
                "worker_behavior_logic": str(DEFAULT_LOGIC),
                "camp_worker_conditions": str(DEFAULT_CAMP),
                "worker_camp_path_branch_matrix": str(DEFAULT_BRANCH),
                "all_original_values": str(DEFAULT_VALUES),
            },
            "scope": "worker/camp/path behavior contract for simulation",
        },
        "global_parameters": {
            "logic_worktime": truth.get("global_truth", {}).get("logic_worktime", {}),
            "logic_movement": truth.get("global_truth", {}).get("logic_movement", {}),
            "weather_speed_factors": truth.get("global_truth", {}).get("weather_speed_factors", {}),
            "default_walk_speed": truth.get("global_truth", {}).get("default_walk_speed"),
            "camp_internal": camp.get("global_camp_parameters", {}).get("camp_internal", {}),
            "camp_large_fire": camp.get("global_camp_parameters", {}).get("camp_large_fire", {}),
            "global_scalars_from_xml": global_scalars,
        },
        "invariants": {
            "worker_count": len(worker_profiles),
            "worktime_worker_count": len(worktime_workers),
            "non_worktime_worker_count": len(no_worktime_workers),
            "non_worktime_workers": no_worktime_workers,
            "shared_core_tasklists_consistency": consistency,
            "summary_from_logic_model": logic.get("summary", {}),
            "summary_from_camp_model": camp.get("summary", {}),
        },
        "notable_worker_variants": notable_variants,
        "common_state_machine_rules": common_rules,
        "worker_profiles": worker_profiles,
        "branch_anchors": branch_anchors,
        "implementation_notes": [
            "Use declared/resolved tasklists as authoritative state transitions.",
            "Apply worktime deltas from TASK_CHANGE_WORK_TIME_* tasks in corresponding loops.",
            "For eat/rest/work/leave transitions, branch on TASK_CHECK_GO_TO_*_SUCCESS outcomes.",
            "Use camper_range plus pathing availability to determine camp reachability.",
            "Respect global distance limits (farm/residence) and reattach frequency for assignment logic.",
            "Integrate alarm/flee as interrupt branch with worker_flight_distance dependency.",
        ],
        "known_limits": [
            "CFG branch extraction is static and heuristic; indirect targets may be incomplete.",
            "Some low-level formulas (exact arithmetic order/clamps) need further disassembly validation.",
        ],
    }


def _fmt_task_list(seq: Any, limit: int = 14) -> str:
    if not isinstance(seq, list) or not seq:
        return "-"
    return " -> ".join(str(x) for x in seq[:limit])


def build_markdown(contract: Dict[str, Any]) -> str:
    lines: List[str] = []
    meta = contract["meta"]
    glob = contract["global_parameters"]
    inv = contract["invariants"]

    lines.append("# Worker Simulation Contract")
    lines.append("")
    lines.append(f"- Generated: {meta.get('generated_at_utc')}")
    lines.append(f"- Scope: {meta.get('scope')}")
    lines.append("")

    lines.append("## Global Parameters")
    lines.append("")
    lw = glob.get("logic_worktime", {})
    lines.append(
        f"- logic_worktime: base={lw.get('base')}, threshold_work={lw.get('threshold_work')}, "
        f"force_to_work_penalty={lw.get('force_to_work_penalty')}"
    )
    lm = glob.get("logic_movement", {})
    lines.append(
        f"- logic_movement: worker_flight_distance={lm.get('worker_flight_distance')}, "
        f"leader_nudge_count={lm.get('leader_nudge_count')}"
    )
    lines.append(f"- default_walk_speed: {glob.get('default_walk_speed')}")
    ci = glob.get("camp_internal", {})
    lines.append(
        f"- camp_internal: slot_count={ci.get('slot_count')}, remove_delay_seconds={ci.get('remove_delay_seconds')}"
    )
    clf = glob.get("camp_large_fire", {})
    lines.append(
        f"- camp_large_fire: num_blocked_points={clf.get('num_blocked_points')}, "
        f"snap_tolerance={clf.get('snap_tolerance')}"
    )

    gs = glob.get("global_scalars_from_xml", {})
    if gs:
        lines.append("- global_scalars_from_xml:")
        for key in sorted(gs.keys()):
            item = gs[key]
            value = item.get("value_int")
            if value is None:
                value = item.get("value_float")
            if value is None:
                value = item.get("value_raw")
            lines.append(f"  - {key}: {value} ({item.get('file')}:{item.get('path')})")
    lines.append("")

    lines.append("## Invariants")
    lines.append("")
    lines.append(f"- worker_count: {inv.get('worker_count')}")
    lines.append(f"- worktime_worker_count: {inv.get('worktime_worker_count')}")
    lines.append(
        f"- non_worktime_workers: {', '.join(inv.get('non_worktime_workers', [])) or '-'}"
    )
    cons = inv.get("shared_core_tasklists_consistency", {})
    lines.append(f"- shared_core_tasklists_consistent: {cons.get('is_consistent')}")
    lines.append("")

    variants = contract.get("notable_worker_variants", [])
    if variants:
        lines.append("## Notable Variants")
        lines.append("")
        for v in variants:
            lines.append(f"- {v.get('worker')}: {', '.join(v.get('reasons', []))}")
        lines.append("")

    lines.append("## Common State Machine Rules")
    lines.append("")
    for rule in contract.get("common_state_machine_rules", []):
        lines.append(f"### {rule.get('id')}")
        lines.append(f"- when: {rule.get('when')}")
        lines.append(f"- tasks: {_fmt_task_list(rule.get('tasks'))}")
        if rule.get("task_counts"):
            lines.append(f"- task_counts: {rule.get('task_counts')}")
        lines.append(f"- key_tasks_required: {rule.get('key_tasks_required')}")
        lines.append(f"- effects: {rule.get('effects')}")
        lines.append(f"- dependencies: {rule.get('dependencies')}")
        lines.append("")

    lines.append("## Worker Profiles")
    lines.append("")
    for wname, p in sorted(contract.get("worker_profiles", {}).items()):
        w = p.get("worktime", {})
        m = p.get("movement", {})
        flags = p.get("derived_flags", {})
        lines.append(f"### {wname}")
        lines.append(f"- has_worktime: {p.get('has_worktime')}")
        lines.append(
            f"- movement: speed={m.get('speed')}, rotation_speed={m.get('rotation_speed')}, "
            f"camper_range={m.get('camper_range')}, move_task_list={m.get('move_task_list')}"
        )
        lines.append(
            f"- worktime: wait_until={w.get('work_wait_until')}, "
            f"delta_work={w.get('work_time_change_work')}, delta_farm={w.get('work_time_change_farm')}, "
            f"delta_residence={w.get('work_time_change_residence')}, delta_camp={w.get('work_time_change_camp')}, "
            f"max_farm={w.get('work_time_max_farm')}, max_residence={w.get('work_time_max_residence')}"
        )
        lines.append(
            f"- checks: eat_success={flags.get('eat_path_has_success_check')}, "
            f"rest_success={flags.get('rest_path_has_success_check')}, "
            f"idle_go_to_camp={flags.get('has_go_to_camp_in_idle_start')}"
        )
        work_nodes = p.get("work_task_nodes", {})
        lines.append(f"- work_start_nodes: {work_nodes.get('work_start_nodes', [])}")
        lines.append(f"- work_nodes: {work_nodes.get('work_nodes', [])}")
        lines.append("")

    lines.append("## Branch Anchors")
    lines.append("")
    for fn, b in sorted(contract.get("branch_anchors", {}).items()):
        stats = b.get("stats", {})
        lines.append(f"### {fn}")
        lines.append(f"- purpose: {b.get('purpose')}")
        lines.append(
            f"- jcc={stats.get('conditional_branches')}, blocks={stats.get('block_count')}, "
            f"insns={stats.get('instruction_count')}"
        )
        for c in b.get("top_conditions", []):
            at = c.get("at")
            if at is None:
                continue
            true_t = c.get("true_target")
            false_t = c.get("false_target")
            lines.append(
                f"- 0x{int(at):08x}: {c.get('mnemonic')} true=0x{int(true_t):08x} "
                f"false=0x{int(false_t):08x}"
            )
            if c.get("predicate_hint"):
                lines.append(f"  predicate_hint: `{c.get('predicate_hint')}`")
        lines.append("")

    lines.append("## Limits")
    lines.append("")
    for lim in contract.get("known_limits", []):
        lines.append(f"- {lim}")
    lines.append("")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build worker simulation contract from extracted engine artifacts."
    )
    parser.add_argument("--truth", type=Path, default=DEFAULT_TRUTH)
    parser.add_argument("--logic", type=Path, default=DEFAULT_LOGIC)
    parser.add_argument("--camp", type=Path, default=DEFAULT_CAMP)
    parser.add_argument("--branch", type=Path, default=DEFAULT_BRANCH)
    parser.add_argument("--values", type=Path, default=DEFAULT_VALUES)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUT_MD)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    truth = _load_json(args.truth.resolve())
    logic = _load_json(args.logic.resolve())
    camp = _load_json(args.camp.resolve())
    branch = _load_json(args.branch.resolve())
    global_scalars = _load_global_scalars(args.values.resolve())

    contract = build_contract(truth, logic, camp, branch, global_scalars)
    md = build_markdown(contract)

    out_json = args.output_json.resolve()
    out_md = args.output_md.resolve()
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(contract, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(md, encoding="utf-8")

    print("Worker simulation contract generated")
    print(f"JSON: {out_json}")
    print(f"MD: {out_md}")
    print(
        "Workers: "
        f"{contract['invariants']['worker_count']} "
        f"(worktime={contract['invariants']['worktime_worker_count']}, "
        f"no_worktime={contract['invariants']['non_worktime_worker_count']})"
    )
    print(f"Branch anchors: {len(contract.get('branch_anchors', {}))}")


if __name__ == "__main__":
    main()
