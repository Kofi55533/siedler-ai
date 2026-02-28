#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static branch evidence extraction from SettlersHoK.exe.

This is a non-invasive, read-only string/RTTI evidence pass intended to
document internal worker/camp branch details that are not fully present in XML.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_EXE = Path(
    r"C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games\theSettlers5\bin\SettlersHoK.exe"
)
DEFAULT_JSON = SCRIPT_DIR / "config" / "engine_branch_evidence.json"
DEFAULT_MD = SCRIPT_DIR / "config" / "engine_branch_evidence.md"


ASCII_RE = re.compile(rb"[\x20-\x7E]{4,}")


def extract_ascii_strings(path: Path) -> List[Tuple[int, str]]:
    data = path.read_bytes()
    out: List[Tuple[int, str]] = []
    for m in ASCII_RE.finditer(data):
        s = m.group().decode("latin1", errors="ignore")
        out.append((m.start(), s))
    return out


def _collect_category_hits(
    strings_with_offsets: List[Tuple[int, str]],
    patterns: List[str],
) -> List[Dict[str, Any]]:
    hits: List[Dict[str, Any]] = []
    for i, (offset, text) in enumerate(strings_with_offsets):
        for pat in patterns:
            if pat in text:
                hits.append(
                    {
                        "index": i,
                        "offset": offset,
                        "text": text,
                        "pattern": pat,
                    }
                )
                break
    return hits


def _dedup_hits(hits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out: List[Dict[str, Any]] = []
    for h in hits:
        key = h["text"]
        if key in seen:
            continue
        seen.add(key)
        out.append(h)
    return out


def _attach_context(
    strings_with_offsets: List[Tuple[int, str]],
    hits: List[Dict[str, Any]],
    window: int = 4,
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    n = len(strings_with_offsets)
    for h in hits:
        i = h["index"]
        lo = max(0, i - window)
        hi = min(n, i + window + 1)
        context = []
        for j in range(lo, hi):
            off, txt = strings_with_offsets[j]
            context.append(
                {
                    "offset": off,
                    "text": txt,
                    "is_hit": j == i,
                }
            )
        item = dict(h)
        item["context"] = context
        out.append(item)
    return out


def build_evidence(strings_with_offsets: List[Tuple[int, str]], exe_path: Path) -> Dict[str, Any]:
    categories = {
        "worktime_thresholds": [
            "WorkTimeBase",
            "WorkTimeThresholdWork",
            "WorkTimeThresholdFarm",
            "WorkTimeThresholdResidence",
            "WorkTimeThresholdCampFire",
        ],
        "worker_distance_and_assignment": [
            "MaximumDistanceWorkerToFarm",
            "MaximumDistanceWorkerToResidence",
            "ReAttachWorkerFrequency",
            "GetNextWorkerWithoutFarmOrResidence",
            "GetNextWorkerWithoutFarm",
            "GetNextWorkerWithoutResidence",
            "GetSettlersFarm",
            "GetSettlersResidence",
            "IsSettlerAtFarm",
            "IsSettlerAtResidence",
            "SetWorkTaskListsPerCycle",
        ],
        "camp_behavior_classes": [
            "CCampBehaviorProperties",
            "CCampBehavior",
            "CCamperBehaviorProperties",
            "CCamperBehavior",
            "CPotentialCampSitePredicate",
            "CCampWithFreeSlotPredicate",
            "CUnblockedSquarePredicate",
            "CEventGetPositionFromID",
        ],
        "worker_behavior_classes": [
            "CWorkerBehaviorProps",
            "CWorkerBehavior",
            "CWorkerFleeBehaviorProps",
            "CWorkerFleeBehavior",
            "CWorkerAlarmModeBehaviorProps",
            "CWorkerAlarmModeBehavior",
            "CSerfBehaviorProps",
            "CSerfBehavior",
        ],
        "task_ids_worker_camp": [
            "TASK_GO_TO_CAMP",
            "TASK_LEAVE_CAMP",
            "TASK_CHANGE_WORK_TIME_CAMP",
            "TASK_GO_TO_EAT_BUILDING",
            "TASK_GO_TO_REST_BUILDING",
            "TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS",
            "TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS",
            "TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS",
            "TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS",
            "TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS",
        ],
        "worker_alarm_and_flight": [
            "WorkerAlarmMode",
            "EnterWorkerAlarmMode",
            "QuitWorkerAlarmMode",
            "WorkerFlightDistance",
        ],
        "attachments_and_entities": [
            "ATTACHMENT_WORKER_FARM",
            "ATTACHMENT_WORKER_RESIDENCE",
            "ATTACHMENT_CAMP_SETTLER",
            "XD_Camp_Internal",
            "TaskLists",
        ],
    }

    categories_out: Dict[str, Any] = {}
    for category, pats in categories.items():
        hits = _collect_category_hits(strings_with_offsets, pats)
        hits = _dedup_hits(hits)
        hits_with_ctx = _attach_context(strings_with_offsets, hits, window=3)
        categories_out[category] = {
            "pattern_count": len(pats),
            "hit_count": len(hits_with_ctx),
            "hits": hits_with_ctx,
        }

    inferences = [
        {
            "id": "worker_threshold_family",
            "confidence": "high",
            "statement": "Engine contains distinct thresholds for Work/Farm/Residence/CampFire and shared WorkTimeBase.",
            "evidence_category": "worktime_thresholds",
        },
        {
            "id": "distance_based_worker_assignment",
            "confidence": "high",
            "statement": "Worker assignment/reassignment logic uses explicit max distance fields for Farm and Residence plus reattach frequency.",
            "evidence_category": "worker_distance_and_assignment",
        },
        {
            "id": "camp_site_selection_predicates",
            "confidence": "medium",
            "statement": "Camp placement/selection appears predicate-driven (potential site, free slot, unblocked square) under CCamp/CCamper behavior classes.",
            "evidence_category": "camp_behavior_classes",
        },
        {
            "id": "task_branch_success_checks",
            "confidence": "high",
            "statement": "Worker eat/rest/work transitions include explicit success-check task IDs for GO_TO_* branches.",
            "evidence_category": "task_ids_worker_camp",
        },
        {
            "id": "alarm_and_flee_branching",
            "confidence": "high",
            "statement": "Dedicated worker alarm/flee behavior classes and command names indicate separate alarm branch flow from regular worker cycle.",
            "evidence_category": "worker_alarm_and_flight",
        },
    ]

    return {
        "meta": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "binary": str(exe_path),
            "binary_size_bytes": exe_path.stat().st_size,
            "extraction_mode": "ascii_strings_with_context",
            "limitations": [
                "Static string/RTTI evidence only, no instruction-level control-flow graph.",
                "Mangled handler names expose event/task wiring but not exact branch predicates.",
            ],
        },
        "categories": categories_out,
        "inferences": inferences,
    }


def build_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    meta = report.get("meta", {})
    lines.append("# Engine Branch Evidence")
    lines.append("")
    lines.append(f"- Binary: `{meta.get('binary')}`")
    lines.append(f"- Size: {meta.get('binary_size_bytes')} bytes")
    lines.append(f"- Generated: {meta.get('generated_at_utc')}")
    lines.append("")

    lines.append("## Inferences")
    lines.append("")
    for inf in report.get("inferences", []):
        lines.append(f"- [{inf.get('confidence')}] {inf.get('statement')}")
        lines.append(f"  evidence: `{inf.get('evidence_category')}`")
    lines.append("")

    for category, data in report.get("categories", {}).items():
        lines.append(f"## {category}")
        lines.append("")
        lines.append(
            f"- patterns: {data.get('pattern_count', 0)} | hits: {data.get('hit_count', 0)}"
        )
        lines.append("")
        for hit in data.get("hits", []):
            lines.append(
                f"- hit: `{hit.get('text')}` (pattern `{hit.get('pattern')}`, offset `0x{hit.get('offset', 0):08x}`)"
            )
            lines.append("  context:")
            for ctx in hit.get("context", []):
                prefix = ">>" if ctx.get("is_hit") else "  "
                lines.append(
                    f"  {prefix} [0x{ctx.get('offset', 0):08x}] `{ctx.get('text')}`"
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
        description="Extract static branch evidence from SettlersHoK.exe"
    )
    parser.add_argument(
        "--exe",
        type=Path,
        default=DEFAULT_EXE,
        help=f"Path to game binary (default: {DEFAULT_EXE})",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=DEFAULT_JSON,
        help=f"Output JSON path (default: {DEFAULT_JSON})",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=DEFAULT_MD,
        help=f"Output markdown path (default: {DEFAULT_MD})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    exe_path = args.exe.resolve()
    out_json = args.output_json.resolve()
    out_md = args.output_md.resolve()

    if not exe_path.exists():
        raise FileNotFoundError(f"Binary not found: {exe_path}")

    strings_with_offsets = extract_ascii_strings(exe_path)
    report = build_evidence(strings_with_offsets, exe_path)
    md = build_markdown(report)

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(md, encoding="utf-8")

    print("Engine branch evidence generated")
    print(f"Binary: {exe_path}")
    print(f"JSON: {out_json}")
    print(f"MD: {out_md}")
    print(f"Extracted strings: {len(strings_with_offsets)}")
    for category, data in report.get("categories", {}).items():
        print(f"- {category}: {data.get('hit_count', 0)} hits")


if __name__ == "__main__":
    main()

