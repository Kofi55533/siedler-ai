#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build focused branch/condition matrix for worker/camp/pathfinding engine logic.

Input:
- config/engine_instruction_cfg.json

Outputs:
- config/worker_camp_path_branch_matrix.json
- config/worker_camp_path_branch_matrix.md
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CFG_JSON = SCRIPT_DIR / "config" / "engine_instruction_cfg.json"
DEFAULT_OUT_JSON = SCRIPT_DIR / "config" / "worker_camp_path_branch_matrix.json"
DEFAULT_OUT_MD = SCRIPT_DIR / "config" / "worker_camp_path_branch_matrix.md"


INTEREST_PATTERNS = {
    "TASK_GO_TO_CAMP",
    "TASK_CHANGE_WORK_TIME_CAMP",
    "TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS",
    "TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS",
    "TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS",
    "TASK_GO_TO_BLOCKED_PILE",
    "ReAttachWorkerFrequency",
    "MaximumDistanceWorkerToFarm",
    "MaximumDistanceWorkerToResidence",
    "WorkerAlarmMode",
    "EnterWorkerAlarmMode",
    "QuitWorkerAlarmMode",
    "FinePath",
    "CoarsePath",
    "IsPathingUsed",
    "WayPoints",
    "WaypointsCount",
    "NextWayPoint",
    "NextWaypointOrientation",
    "UpdateBlocking",
    "BlockingArea",
    "NumBlockedPoints",
    "CheckSettlerPlacement",
}


INTEREST_CLASSES = {
    ".?AVCCampBehavior@GGL@@",
    ".?AVCCampBehaviorProperties@GGL@@",
    ".?AVCCamperBehavior@GGL@@",
    ".?AVCCamperBehaviorProperties@GGL@@",
    ".?AVCPotentialCampSitePredicate@GGL@@",
    ".?AVCCampWithFreeSlotPredicate@GGL@@",
    ".?AVCWorkerBehavior@GGL@@",
    ".?AVCWorkerBehaviorProps@GGL@@",
    ".?AVCWorkerFleeBehavior@GGL@@",
    ".?AVCWorkerFleeBehaviorProps@GGL@@",
    ".?AVCWorkerAlarmModeBehavior@GGL@@",
    ".?AVCWorkerAlarmModeBehaviorProps@GGL@@",
    ".?AVCPath@EGL@@",
    ".?AVCCoarsePath@EGL@@",
    ".?AVCAStar64@EGL@@",
    ".?AVCAStar64Normal@EGL@@",
    ".?AVCBlockingStatusPredicate@EGL@@",
    ".?AVCUnblockedAreasPredicate@EGL@@",
    ".?AVCUnblockedBuildingAreasPredicate@EGL@@",
    ".?AVCUnblockedInSectorPredicate@EGL@@",
    ".?AVCUnblockedInLargeSectorPredicate@EGL@@",
    ".?AVCBuildBlockedOnlyPredicate@?A0xe5557549@GGL@@",
}


def _hex_to_int(addr: Any) -> Optional[int]:
    if isinstance(addr, int):
        return addr
    if isinstance(addr, str):
        try:
            return int(addr, 16)
        except ValueError:
            return None
    return None


def _reason_tags(reasons: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    patterns: Set[str] = set()
    classes: Set[str] = set()
    reason_types: Set[str] = set()
    for r in reasons:
        rt = r.get("reason_type")
        if rt:
            reason_types.add(str(rt))
        p = r.get("pattern")
        if isinstance(p, str):
            patterns.add(p)
        c = r.get("class_name")
        if isinstance(c, str):
            classes.add(c)
    return {
        "patterns": sorted(patterns),
        "classes": sorted(classes),
        "reason_types": sorted(reason_types),
    }


def _extract_branch_conditions(edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_site: Dict[int, Dict[str, Any]] = {}
    direct_jumps: List[Dict[str, Any]] = []
    indirect_jumps: List[Dict[str, Any]] = []

    for e in edges:
        et = e.get("type")
        at = e.get("at")
        if not isinstance(at, int):
            continue

        if et in {"jcc_true", "jcc_false"}:
            entry = by_site.setdefault(
                at,
                {
                    "at": at,
                    "mnemonic": e.get("mnemonic"),
                    "true_target": None,
                    "false_target": None,
                    "context": e.get("context", []),
                },
            )
            if et == "jcc_true":
                entry["true_target"] = e.get("to")
            elif et == "jcc_false":
                entry["false_target"] = e.get("to")
            if not entry.get("context") and e.get("context"):
                entry["context"] = e.get("context", [])
            if not entry.get("mnemonic") and e.get("mnemonic"):
                entry["mnemonic"] = e.get("mnemonic")
        elif et == "jmp":
            direct_jumps.append(
                {
                    "at": at,
                    "mnemonic": e.get("mnemonic"),
                    "target": e.get("to"),
                    "context": e.get("context", []),
                }
            )
        elif et == "jmp_indirect":
            indirect_jumps.append(
                {
                    "at": at,
                    "mnemonic": e.get("mnemonic"),
                    "op_str": e.get("op_str", ""),
                    "context": e.get("context", []),
                }
            )

    conds: List[Dict[str, Any]] = []
    for at in sorted(by_site.keys()):
        item = by_site[at]
        ctx = item.get("context", []) or []
        predicate_hint = ""
        if ctx:
            for line in reversed(ctx):
                line = str(line)
                if ": " in line and (" cmp " in line or " test " in line):
                    predicate_hint = line
                    break
            if not predicate_hint:
                for line in reversed(ctx):
                    line = str(line)
                    if ": " in line and not line.split(": ", 1)[1].startswith("j"):
                        predicate_hint = line
                        break

        conds.append(
            {
                "at": at,
                "mnemonic": item.get("mnemonic"),
                "true_target": item.get("true_target"),
                "false_target": item.get("false_target"),
                "predicate_hint": predicate_hint,
                "context": ctx,
            }
        )

    direct_jumps = sorted(direct_jumps, key=lambda x: x["at"])
    indirect_jumps = sorted(indirect_jumps, key=lambda x: x["at"])

    return {
        "conditional_sites": conds,
        "direct_jumps": direct_jumps,
        "indirect_jumps": indirect_jumps,
    }


def _has_interest_reason(reasons: List[Dict[str, Any]]) -> bool:
    for r in reasons:
        if r.get("pattern") in INTEREST_PATTERNS:
            return True
        if r.get("class_name") in INTEREST_CLASSES:
            return True
    return False


def _collect_anchor_functions(functions: Dict[str, Any]) -> Set[str]:
    anchors: Set[str] = set()
    for faddr, fobj in functions.items():
        reasons = fobj.get("reasons", [])
        if _has_interest_reason(reasons):
            anchors.add(faddr)
    return anchors


def _collect_related_functions(functions: Dict[str, Any], anchors: Set[str]) -> Set[str]:
    selected = set(anchors)

    # Add explicit callers of anchor-path and one more hop of caller chain.
    for faddr, fobj in functions.items():
        reasons = fobj.get("reasons", [])
        stats = (fobj.get("cfg") or {}).get("stats", {})
        jcc = int(stats.get("conditional_branches", 0))

        for r in reasons:
            if r.get("reason_type") != "caller_of_anchor_path":
                continue
            callee = r.get("callee_entry")
            if not isinstance(callee, str):
                continue
            depth = int(r.get("depth", 0))
            if callee in anchors:
                selected.add(faddr)
                break
            if depth <= 2 and jcc > 0:
                selected.add(faddr)
                break

    return selected


def _score_function(entry: Dict[str, Any]) -> Tuple[int, int, int, str]:
    stats = entry["stats"]
    tags = entry["tags"]
    # Sort by branch density/importance first, then by amount of direct matching reasons.
    direct_interest_reasons = len(
        [p for p in tags["patterns"] if p in INTEREST_PATTERNS]
    ) + len([c for c in tags["classes"] if c in INTEREST_CLASSES])
    return (
        int(stats.get("conditional_branches", 0)),
        direct_interest_reasons,
        int(stats.get("instruction_count", 0)),
        entry["function"],
    )


def build_matrix(cfg: Dict[str, Any]) -> Dict[str, Any]:
    functions = cfg.get("functions", {})
    anchors = _collect_anchor_functions(functions)
    selected = _collect_related_functions(functions, anchors)

    rows: List[Dict[str, Any]] = []
    for faddr in sorted(selected):
        fobj = functions.get(faddr, {})
        cfg_obj = fobj.get("cfg", {})
        stats = cfg_obj.get("stats", {})
        reasons = fobj.get("reasons", [])
        tags = _reason_tags(reasons)
        branches = _extract_branch_conditions(cfg_obj.get("edges", []))

        rows.append(
            {
                "function": faddr,
                "entry": fobj.get("entry", faddr),
                "stats": {
                    "block_count": int(stats.get("block_count", 0)),
                    "instruction_count": int(stats.get("instruction_count", 0)),
                    "edge_count": int(stats.get("edge_count", 0)),
                    "conditional_branches": int(stats.get("conditional_branches", 0)),
                    "switch_candidates_indirect_jmp": int(
                        stats.get("switch_candidates_indirect_jmp", 0)
                    ),
                    "truncated": bool(stats.get("truncated", False)),
                },
                "tags": tags,
                "reasons": reasons,
                "branches": branches,
            }
        )

    rows_sorted = sorted(rows, key=_score_function, reverse=True)

    summary = {
        "selected_function_count": len(rows_sorted),
        "anchor_function_count": len(anchors),
        "selected_with_conditional_branches": len(
            [r for r in rows_sorted if r["stats"]["conditional_branches"] > 0]
        ),
        "selected_total_conditional_branches": sum(
            r["stats"]["conditional_branches"] for r in rows_sorted
        ),
        "selected_switch_candidates_indirect_jmp": sum(
            r["stats"]["switch_candidates_indirect_jmp"] for r in rows_sorted
        ),
    }

    return {
        "meta": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "source_cfg_generated_at_utc": cfg.get("meta", {}).get("generated_at_utc"),
            "source_binary": cfg.get("meta", {}).get("binary"),
            "selection_basis": {
                "interest_patterns": sorted(INTEREST_PATTERNS),
                "interest_classes": sorted(INTEREST_CLASSES),
                "include_anchor_callers": True,
            },
            "limitations": [
                "Static CFG only; no runtime traces.",
                "Function boundaries and call-chain context are heuristic.",
                "Predicate hints are inferred from nearby disassembly text.",
            ],
        },
        "summary": summary,
        "functions": rows_sorted,
    }


def build_markdown(matrix: Dict[str, Any]) -> str:
    meta = matrix["meta"]
    summary = matrix["summary"]
    funcs = matrix["functions"]

    lines: List[str] = []
    lines.append("# Worker/Camp/Path Branch Matrix")
    lines.append("")
    lines.append(f"- Binary: `{meta.get('source_binary')}`")
    lines.append(f"- Source CFG Generated: {meta.get('source_cfg_generated_at_utc')}")
    lines.append(f"- Generated: {meta.get('generated_at_utc')}")
    lines.append(f"- Selected functions: {summary.get('selected_function_count', 0)}")
    lines.append(f"- Anchor functions: {summary.get('anchor_function_count', 0)}")
    lines.append(
        f"- Selected functions with conditional branches: {summary.get('selected_with_conditional_branches', 0)}"
    )
    lines.append(
        f"- Total conditional branches (selected): {summary.get('selected_total_conditional_branches', 0)}"
    )
    lines.append(
        f"- Switch candidates (selected): {summary.get('selected_switch_candidates_indirect_jmp', 0)}"
    )
    lines.append("")

    lines.append("## Functions")
    lines.append("")
    for f in funcs:
        stats = f["stats"]
        lines.append(f"### {f['function']}")
        lines.append(
            f"- blocks={stats['block_count']}, insns={stats['instruction_count']}, "
            f"edges={stats['edge_count']}, jcc={stats['conditional_branches']}, "
            f"switch_indirect={stats['switch_candidates_indirect_jmp']}, truncated={stats['truncated']}"
        )
        if f["tags"]["patterns"]:
            lines.append("- patterns:")
            for p in f["tags"]["patterns"]:
                lines.append(f"  - {p}")
        if f["tags"]["classes"]:
            lines.append("- classes:")
            for c in f["tags"]["classes"]:
                lines.append(f"  - {c}")

        lines.append("- branch conditions:")
        conds = f["branches"]["conditional_sites"]
        if not conds:
            lines.append("  - none")
        else:
            for c in conds:
                at = c["at"]
                tru = c.get("true_target")
                fal = c.get("false_target")
                pred = c.get("predicate_hint", "")
                lines.append(
                    f"  - 0x{at:08x}: {c.get('mnemonic')} | true=0x{int(tru):08x} "
                    f"| false=0x{int(fal):08x}"
                )
                if pred:
                    lines.append(f"    predicate_hint: `{pred}`")

        ind = f["branches"]["indirect_jumps"]
        if ind:
            lines.append("- indirect jumps:")
            for j in ind:
                lines.append(
                    f"  - 0x{j['at']:08x}: {j.get('mnemonic')} {j.get('op_str', '')}"
                )
        lines.append("")

    lines.append("## Limits")
    lines.append("")
    for lim in meta.get("limitations", []):
        lines.append(f"- {lim}")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build worker/camp/path branch matrix from engine_instruction_cfg.json"
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_CFG_JSON,
        help=f"Input CFG JSON (default: {DEFAULT_CFG_JSON})",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=DEFAULT_OUT_JSON,
        help=f"Output JSON (default: {DEFAULT_OUT_JSON})",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=DEFAULT_OUT_MD,
        help=f"Output markdown (default: {DEFAULT_OUT_MD})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    in_path = args.input.resolve()
    out_json = args.output_json.resolve()
    out_md = args.output_md.resolve()

    if not in_path.exists():
        raise FileNotFoundError(f"Input not found: {in_path}")

    cfg = json.loads(in_path.read_text(encoding="utf-8"))
    matrix = build_matrix(cfg)
    md = build_markdown(matrix)

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(matrix, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(md, encoding="utf-8")

    print("Worker/Camp/Path branch matrix generated")
    print(f"Input: {in_path}")
    print(f"JSON: {out_json}")
    print(f"MD: {out_md}")
    print(f"Selected functions: {matrix['summary']['selected_function_count']}")
    print(
        "Selected conditional branches: "
        f"{matrix['summary']['selected_total_conditional_branches']}"
    )
    print(
        "Selected switch candidates: "
        f"{matrix['summary']['selected_switch_candidates_indirect_jmp']}"
    )


if __name__ == "__main__":
    main()
