#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a reproducible conformance certificate for the Settlers 5 simulation.

This is not a theorem prover. It records:
- exact source binary/config hashes,
- extracted XML/tasklist coverage,
- static binary CFG/branch coverage,
- current engine-vs-runtime diff status,
- the remaining proof gap between static evidence and full runtime equivalence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent

DEFAULT_BINARY = Path(r"C:\Users\marku\OneDrive\Desktop\Gold edition\bin\SettlersHoK.exe")
DEFAULT_FULL_WORKER = PROJECT_ROOT / "config" / "full_worker_engine_behavior.json"
DEFAULT_CFG = PROJECT_ROOT / "config" / "engine_instruction_cfg.json"
DEFAULT_BRANCH = PROJECT_ROOT / "config" / "worker_camp_path_branch_matrix.json"
DEFAULT_CONTRACT = PROJECT_ROOT / "config" / "worker_sim_contract.json"
DEFAULT_GHIDRA = PROJECT_ROOT / "config" / "ghidra_worker_decompile_evidence.json"
DEFAULT_DIFF_REPORT = PROJECT_ROOT / "config" / "engine_env_diff_report.md"
DEFAULT_OUT_JSON = PROJECT_ROOT / "config" / "engine_conformance_certificate.json"
DEFAULT_OUT_MD = PROJECT_ROOT / "config" / "engine_conformance_certificate.md"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def extract_diff_summary(path: Path) -> Dict[str, Optional[int]]:
    if not path.exists():
        return {"critical": None, "warnings": None}
    text = path.read_text(encoding="utf-8", errors="ignore")
    critical = None
    warnings = None
    m = re.search(r"Kritische Punkte:\s*(\d+)", text)
    if m:
        critical = int(m.group(1))
    m = re.search(r"Warnungen:\s*(\d+)", text)
    if m:
        warnings = int(m.group(1))
    return {"critical": critical, "warnings": warnings}


def artifact_entry(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "exists": False}
    return {
        "path": str(path),
        "exists": True,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def build_certificate(args: argparse.Namespace) -> Dict[str, Any]:
    binary = Path(args.binary)
    full_worker = Path(args.full_worker)
    cfg_path = Path(args.cfg)
    branch_path = Path(args.branch)
    contract_path = Path(args.contract)
    ghidra_path = Path(args.ghidra)
    diff_report = Path(args.diff_report)

    full = load_json(full_worker)
    cfg = load_json(cfg_path)
    branch = load_json(branch_path)
    contract = load_json(contract_path)
    ghidra = load_json(ghidra_path)
    diff_summary = extract_diff_summary(diff_report)

    full_meta = full.get("meta", {}) or {}
    cfg_meta = cfg.get("meta", {}) or {}
    cfg_summary = cfg.get("summary", {}) or {}
    branch_summary = branch.get("summary", {}) or {}
    contract_meta = contract.get("meta", {}) or {}
    ghidra_meta = ghidra.get("meta", {}) or {}

    exact_xml = (
        full_meta.get("unresolved_worker_tasklist_count") == 0
        and int(full_meta.get("tasklist_count", 0)) > 0
        and int(full_meta.get("reachable_worker_tasklist_count", 0)) > 0
    )
    static_binary_ok = (
        int(cfg_summary.get("function_count", 0)) > 0
        and int(branch_summary.get("selected_total_conditional_branches", 0)) > 0
    )
    ghidra_ok = (
        int(ghidra_meta.get("matched_function_count", 0)) > 0
        and int(ghidra_meta.get("decompiled_ok_count", 0)) > 0
    )
    diff_clean = diff_summary.get("critical") == 0 and diff_summary.get("warnings") == 0

    proof_status = {
        "xml_tasklist_extraction": "machine_checked_exact_extract" if exact_xml else "incomplete",
        "runtime_worker_values": "machine_checked_against_extract" if diff_clean else "has_diffs",
        "static_binary_cfg": "heuristic_static_disassembly" if static_binary_ok else "missing",
        "ghidra_decompiler_evidence": "available_hashes_and_pcode_histograms" if ghidra_ok else "missing",
        "full_runtime_equivalence": "not_formally_proven",
        "pathfinding_equivalence": "not_formally_proven",
    }

    return {
        "meta": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "certificate_schema": "siedler5_engine_conformance_v1",
        },
        "source_binary": artifact_entry(binary),
        "artifacts": {
            "full_worker_engine_behavior": artifact_entry(full_worker),
            "engine_instruction_cfg": artifact_entry(cfg_path),
            "worker_camp_path_branch_matrix": artifact_entry(branch_path),
            "worker_sim_contract": artifact_entry(contract_path),
            "ghidra_worker_decompile_evidence": artifact_entry(ghidra_path),
            "engine_env_diff_report": artifact_entry(diff_report),
        },
        "coverage": {
            "full_worker_engine_behavior": {
                "source_root": full_meta.get("source_root"),
                "tasklist_count": full_meta.get("tasklist_count"),
                "worker_entity_count": full_meta.get("worker_entity_count"),
                "worker_building_count": full_meta.get("worker_building_count"),
                "reachable_worker_tasklist_count": full_meta.get(
                    "reachable_worker_tasklist_count"
                ),
                "unresolved_worker_tasklist_count": full_meta.get(
                    "unresolved_worker_tasklist_count"
                ),
                "source_file_counts": full_meta.get("source_file_counts", {}),
            },
            "engine_instruction_cfg": {
                "binary": cfg_meta.get("binary"),
                "function_count": cfg_summary.get("function_count"),
                "total_blocks": cfg_summary.get("total_blocks"),
                "total_instructions": cfg_summary.get("total_instructions"),
                "total_conditional_branches": cfg_summary.get("total_conditional_branches"),
                "total_switch_candidates_indirect_jmp": cfg_summary.get(
                    "total_switch_candidates_indirect_jmp"
                ),
            },
            "worker_camp_path_branch_matrix": branch_summary,
            "worker_sim_contract": {
                "generated_at_utc": contract_meta.get("generated_at_utc"),
                "branch_anchor_count": len(contract.get("branch_anchors", {}) or {}),
                "worker_profile_count": len(contract.get("worker_profiles", {}) or {}),
            },
            "ghidra_worker_decompile_evidence": {
                "program_name": ghidra_meta.get("program_name"),
                "executable_path": ghidra_meta.get("executable_path"),
                "language_id": ghidra_meta.get("language_id"),
                "compiler_spec_id": ghidra_meta.get("compiler_spec_id"),
                "target_address_count": ghidra_meta.get(
                    "target_address_count", ghidra_meta.get("target_function_count")
                ),
                "matched_target_address_count": ghidra_meta.get(
                    "matched_target_address_count"
                ),
                "unmatched_target_address_count": ghidra_meta.get(
                    "unmatched_target_address_count"
                ),
                "matched_function_count": ghidra_meta.get("matched_function_count"),
                "decompiled_ok_count": ghidra_meta.get("decompiled_ok_count"),
                "stores_full_decompiled_code": ghidra_meta.get("stores_full_decompiled_code"),
            },
            "engine_env_diff_report": diff_summary,
        },
        "proof_status": proof_status,
        "formal_equivalence_requirements": [
            "A compiler/CPU semantic model for the exact x86 binary.",
            "Verified function boundaries and typed memory layout for all relevant engine objects.",
            "A decompiled or lifted IR for every task/path/worker function used by the simulation.",
            "A formal relation between engine state and simulation state.",
            "Exhaustive or theorem-proved transition equivalence for every reachable state.",
            "Runtime trace validation for nondeterministic choices, timing, floating point, and OS-dependent pathing.",
        ],
        "limits": [
            "Static CFG extraction is evidence, not a mathematical proof of semantic equivalence.",
            "TaskList/XML extraction is exact for the parsed files, but task execution semantics live in the binary.",
            "The local simulation pathfinder is not proven equivalent to the engine path solver.",
            "No complete proprietary high-level decompiler output is stored in this repository.",
        ],
    }


def write_markdown(cert: Dict[str, Any], path: Path) -> None:
    lines: List[str] = []
    lines.append("# Engine Conformance Certificate")
    lines.append("")
    lines.append(f"- Generated: `{cert['meta']['generated_at_utc']}`")
    src = cert.get("source_binary", {})
    lines.append(f"- Source binary: `{src.get('path')}`")
    lines.append(f"- Source binary SHA256: `{src.get('sha256')}`")
    lines.append("")

    lines.append("## Coverage")
    lines.append("")
    fw = cert["coverage"]["full_worker_engine_behavior"]
    lines.append(
        f"- Worker XML/TaskLists: {fw.get('tasklist_count')} TaskLists, "
        f"{fw.get('worker_entity_count')} worker/serf entities, "
        f"{fw.get('worker_building_count')} worker buildings, "
        f"{fw.get('reachable_worker_tasklist_count')} reachable TaskLists, "
        f"{fw.get('unresolved_worker_tasklist_count')} unresolved refs"
    )
    cfg = cert["coverage"]["engine_instruction_cfg"]
    lines.append(
        f"- Static CFG: {cfg.get('function_count')} functions, "
        f"{cfg.get('total_blocks')} blocks, "
        f"{cfg.get('total_instructions')} instructions, "
        f"{cfg.get('total_conditional_branches')} conditional branches"
    )
    br = cert["coverage"]["worker_camp_path_branch_matrix"]
    lines.append(
        f"- Worker/Camp/Path matrix: {br.get('selected_function_count')} selected functions, "
        f"{br.get('anchor_function_count')} anchors, "
        f"{br.get('selected_total_conditional_branches')} selected conditional branches"
    )
    con = cert["coverage"]["worker_sim_contract"]
    lines.append(
        f"- Simulation contract: {con.get('worker_profile_count')} worker profiles, "
        f"{con.get('branch_anchor_count')} branch anchors"
    )
    gh = cert["coverage"]["ghidra_worker_decompile_evidence"]
    lines.append(
        f"- Ghidra decompiler: {gh.get('matched_target_address_count')}/"
        f"{gh.get('target_address_count')} target addresses matched, "
        f"{gh.get('matched_function_count')} functions matched, "
        f"{gh.get('decompiled_ok_count')} decompiled OK, "
        f"full code stored={gh.get('stores_full_decompiled_code')}"
    )
    diff = cert["coverage"]["engine_env_diff_report"]
    lines.append(
        f"- Engine-vs-env diff: critical={diff.get('critical')}, warnings={diff.get('warnings')}"
    )
    lines.append("")

    lines.append("## Proof Status")
    lines.append("")
    for key, value in cert.get("proof_status", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")

    lines.append("## Formal Equivalence Requirements")
    lines.append("")
    for item in cert.get("formal_equivalence_requirements", []):
        lines.append(f"- {item}")
    lines.append("")

    lines.append("## Limits")
    lines.append("")
    for item in cert.get("limits", []):
        lines.append(f"- {item}")
    lines.append("")

    lines.append("## Artifact Hashes")
    lines.append("")
    for name, artifact in cert.get("artifacts", {}).items():
        if not artifact.get("exists"):
            lines.append(f"- `{name}`: missing `{artifact.get('path')}`")
            continue
        lines.append(
            f"- `{name}`: sha256 `{artifact.get('sha256')}`, "
            f"size {artifact.get('size_bytes')} bytes"
        )
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build reproducible Settlers 5 engine conformance certificate."
    )
    parser.add_argument("--binary", type=Path, default=DEFAULT_BINARY)
    parser.add_argument("--full-worker", type=Path, default=DEFAULT_FULL_WORKER)
    parser.add_argument("--cfg", type=Path, default=DEFAULT_CFG)
    parser.add_argument("--branch", type=Path, default=DEFAULT_BRANCH)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--ghidra", type=Path, default=DEFAULT_GHIDRA)
    parser.add_argument("--diff-report", type=Path, default=DEFAULT_DIFF_REPORT)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUT_MD)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cert = build_certificate(args)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(cert, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_markdown(cert, args.output_md)

    diff = cert["coverage"]["engine_env_diff_report"]
    print("Engine conformance certificate generated")
    print(f"JSON: {args.output_json.resolve()}")
    print(f"MD: {args.output_md.resolve()}")
    print(f"Diff critical={diff.get('critical')} warnings={diff.get('warnings')}")
    print(f"Full runtime equivalence: {cert['proof_status']['full_runtime_equivalence']}")


if __name__ == "__main__":
    main()
