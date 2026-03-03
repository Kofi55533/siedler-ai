#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reconstruct instruction-level control-flow for worker/camp relevant engine paths.

This script performs:
- PE parsing
- target string address discovery
- .text xref discovery (immediate VA references)
- function start heuristics
- recursive basic-block CFG disassembly

Outputs:
- config/engine_instruction_cfg.json
- config/engine_instruction_cfg.md
"""

from __future__ import annotations

import argparse
import json
import struct
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_MODE_64
from capstone.x86 import X86_OP_IMM


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_EXE = Path(
    r"C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games\theSettlers5\bin\SettlersHoK.exe"
)
DEFAULT_JSON = SCRIPT_DIR / "config" / "engine_instruction_cfg.json"
DEFAULT_MD = SCRIPT_DIR / "config" / "engine_instruction_cfg.md"


TARGET_PATTERNS = [
    # Worktime thresholds
    "WorkTimeBase",
    "WorkTimeThresholdWork",
    "WorkTimeThresholdFarm",
    "WorkTimeThresholdResidence",
    "WorkTimeThresholdCampFire",
    # Worker distance/reassign
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
    # Camp behavior classes/predicates
    "CCampBehavior",
    "CCampBehaviorProperties",
    "CCamperBehavior",
    "CCamperBehaviorProperties",
    "CPotentialCampSitePredicate",
    "CCampWithFreeSlotPredicate",
    "CUnblockedSquarePredicate",
    # Task branch labels
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
    # Alarm/flee
    "WorkerAlarmMode",
    "EnterWorkerAlarmMode",
    "QuitWorkerAlarmMode",
    "WorkerFlightDistance",
    # Worker classes
    "CWorkerBehavior",
    "CWorkerBehaviorProps",
    "CWorkerFleeBehavior",
    "CWorkerFleeBehaviorProps",
    "CWorkerAlarmModeBehavior",
    "CWorkerAlarmModeBehaviorProps",
    # Pathfinding/blocking/navigation
    "IsPathingUsed",
    "FinePath",
    "CoarsePath",
    "WayPoints",
    "WaypointsCount",
    "NextWayPoint",
    "NextWaypointOrientation",
    "UpdateBlocking",
    "BlockingArea",
    "NumBlockedPoints",
    "CheckSettlerPlacement",
    "TASK_GO_TO_BLOCKED_PILE",
    "CPath",
    "CCoarsePath",
    "CAStar64",
    "CAStar64Normal",
    "CBlockingStatusPredicate",
    "CUnblockedInSectorPredicate",
    "CUnblockedInLargeSectorPredicate",
    "CUnblockedAreasPredicate",
    "CUnblockedBuildingAreasPredicate",
    "CBuildBlockedOnlyPredicate",
]


class PEView:
    def __init__(self, exe_path: Path) -> None:
        self.exe_path = exe_path
        self.pe = pefile.PE(str(exe_path), fast_load=False)
        self.image_base = self.pe.OPTIONAL_HEADER.ImageBase
        self.machine = self.pe.FILE_HEADER.Machine
        self.is_64 = self.machine == 0x8664
        self.ptr_size = 8 if self.is_64 else 4

        self.sections: List[Dict[str, Any]] = []
        self.text_section: Optional[Dict[str, Any]] = None

        for s in self.pe.sections:
            name = s.Name.rstrip(b"\x00").decode("ascii", errors="ignore")
            entry = {
                "name": name,
                "rva": int(s.VirtualAddress),
                "vsize": int(s.Misc_VirtualSize),
                "raw_size": int(s.SizeOfRawData),
                "raw_ptr": int(s.PointerToRawData),
                "va": int(self.image_base + s.VirtualAddress),
                "data": bytes(s.get_data()),
            }
            self.sections.append(entry)
            if name.lower().startswith(".text"):
                self.text_section = entry

        if self.text_section is None:
            raise RuntimeError("No .text section found")

    def read_va(self, va: int, size: int) -> bytes:
        if size <= 0:
            return b""
        for s in self.sections:
            start = s["va"]
            end = start + len(s["data"])
            if start <= va < end:
                inner = va - start
                if inner + size > len(s["data"]):
                    return b""
                return s["data"][inner : inner + size]
        return b""

    def read_pointer(self, va: int) -> Optional[int]:
        blob = self.read_va(va, self.ptr_size)
        if len(blob) != self.ptr_size:
            return None
        if self.ptr_size == 4:
            return int(struct.unpack("<I", blob)[0])
        return int(struct.unpack("<Q", blob)[0])

    def va_to_file_offset(self, va: int) -> Optional[int]:
        rva = va - self.image_base
        for s in self.sections:
            start = s["rva"]
            end = start + max(s["vsize"], s["raw_size"])
            if start <= rva < end:
                inner = rva - start
                return s["raw_ptr"] + inner
        return None

    def in_text(self, va: int) -> bool:
        text = self.text_section
        assert text is not None
        start = text["va"]
        end = start + len(text["data"])
        return start <= va < end

    def text_bounds(self) -> Tuple[int, int]:
        text = self.text_section
        assert text is not None
        start = text["va"]
        end = start + len(text["data"])
        return start, end


def find_target_strings(view: PEView, patterns: List[str]) -> List[Dict[str, Any]]:
    found: List[Dict[str, Any]] = []
    pattern_set = set(patterns)
    for s in view.sections:
        data = s["data"]
        for pat in pattern_set:
            pat_b = pat.encode("latin1", errors="ignore")
            start = 0
            while True:
                idx = data.find(pat_b, start)
                if idx < 0:
                    break

                # Expand to full printable string boundaries.
                l = idx
                while l > 0 and 0x20 <= data[l - 1] <= 0x7E:
                    l -= 1
                r = idx + len(pat_b)
                while r < len(data) and 0x20 <= data[r] <= 0x7E:
                    r += 1

                text = data[l:r].decode("latin1", errors="ignore")
                va = s["va"] + l
                found.append(
                    {
                        "pattern": pat,
                        "text": text,
                        "va": va,
                        "section": s["name"],
                    }
                )
                start = idx + len(pat_b)

    # Dedup by VA.
    dedup: Dict[int, Dict[str, Any]] = {}
    for item in found:
        dedup[item["va"]] = item
    return [dedup[k] for k in sorted(dedup.keys())]


def find_text_xrefs_to_va(view: PEView, target_va: int) -> List[int]:
    text = view.text_section
    assert text is not None
    data = text["data"]
    start_va = text["va"]

    # x86/x64 immediate references in little-endian.
    refs: List[int] = []
    if view.ptr_size == 4:
        needle = struct.pack("<I", target_va & 0xFFFFFFFF)
        off = 0
        while True:
            i = data.find(needle, off)
            if i < 0:
                break
            refs.append(start_va + i)
            off = i + 1
    else:
        needle = struct.pack("<Q", target_va & 0xFFFFFFFFFFFFFFFF)
        off = 0
        while True:
            i = data.find(needle, off)
            if i < 0:
                break
            refs.append(start_va + i)
            off = i + 1
    return refs


def find_va_references(
    view: PEView,
    target_va: int,
    section_prefixes: Optional[List[str]] = None,
    max_hits: int = 2000,
) -> List[int]:
    refs: List[int] = []
    prefixes = [p.lower() for p in (section_prefixes or [])]

    if view.ptr_size == 4:
        needle = struct.pack("<I", target_va & 0xFFFFFFFF)
    else:
        needle = struct.pack("<Q", target_va & 0xFFFFFFFFFFFFFFFF)

    for s in view.sections:
        if prefixes:
            s_name = s["name"].lower()
            if not any(s_name.startswith(p) for p in prefixes):
                continue
        data = s["data"]
        start_va = s["va"]
        off = 0
        while True:
            i = data.find(needle, off)
            if i < 0:
                break
            refs.append(start_va + i)
            if len(refs) >= max_hits:
                return refs
            off = i + 1
    return refs


def scan_direct_calls(view: PEView) -> List[Dict[str, int]]:
    text = view.text_section
    assert text is not None
    data = text["data"]
    start_va = text["va"]
    calls: List[Dict[str, int]] = []

    # x86/x64 near call: E8 rel32
    for i in range(0, max(0, len(data) - 4)):
        if data[i] != 0xE8:
            continue
        rel = struct.unpack_from("<i", data, i + 1)[0]
        site = start_va + i
        target = (site + 5 + rel) & 0xFFFFFFFFFFFFFFFF
        if view.in_text(target):
            calls.append({"site": site, "target": target})
    return calls


def build_caller_index(direct_calls: List[Dict[str, int]]) -> Dict[int, List[int]]:
    idx: Dict[int, List[int]] = {}
    for c in direct_calls:
        idx.setdefault(c["target"], []).append(c["site"])
    for target in list(idx.keys()):
        idx[target] = sorted(set(idx[target]))
    return idx


def find_callers_for_entry(
    caller_index: Dict[int, List[int]],
    entry_va: int,
    window: int = 0x20,
) -> List[int]:
    callers: Set[int] = set()
    for delta in range(-window, window + 1):
        tgt = entry_va + delta
        for site in caller_index.get(tgt, []):
            callers.add(site)
    return sorted(callers)


def scan_prologues(view: PEView) -> List[int]:
    text = view.text_section
    assert text is not None
    data = text["data"]
    base = text["va"]

    # Common x86/x64 prologue signatures.
    patterns = [
        b"\x55\x8B\xEC",  # push ebp; mov ebp, esp
        b"\x8B\xFF\x55\x8B\xEC",  # mov edi, edi; push ebp; mov ebp, esp
        b"\x53\x8B\xDC",  # push ebx; mov ebx, esp
        b"\x56\x8B\xF1",  # push esi; mov esi, ecx
        b"\x57\x8B\xF9",  # push edi; mov edi, ecx
        b"\x55\x48\x89\xE5",  # push rbp; mov rbp, rsp (x64)
    ]
    starts: Set[int] = set()
    for pat in patterns:
        off = 0
        while True:
            i = data.find(pat, off)
            if i < 0:
                break
            starts.add(base + i)
            off = i + 1
    return sorted(starts)


def guess_function_start(xref_va: int, prologues: List[int], max_back: int = 0x3000) -> int:
    # Nearest prologue before xref within max_back.
    candidate = xref_va
    for p in prologues:
        if p > xref_va:
            break
        if xref_va - p <= max_back:
            candidate = p
    return candidate


def extract_rtti_vtable_methods(
    view: PEView,
    strings: List[Dict[str, Any]],
    prologues: List[int],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    ptr = view.ptr_size
    td_name_offset = ptr * 2
    # x86 COL offset to pTypeDescriptor; x64 layout differs significantly.
    # SettlersHoK.exe in this setup is x86, so we keep this constrained.
    if ptr != 4:
        return out

    def _is_probably_col(col_va: int, expected_td_va: int) -> bool:
        sig = view.read_pointer(col_va)
        off = view.read_pointer(col_va + 4)
        cd_off = view.read_pointer(col_va + 8)
        td = view.read_pointer(col_va + 12)
        chd = view.read_pointer(col_va + 16)
        if None in {sig, off, cd_off, td, chd}:
            return False
        if int(sig) not in {0, 1}:
            return False
        if int(off) > 0x100000 or int(cd_off) > 0x100000:
            return False
        if int(td) != int(expected_td_va):
            return False
        # CHD usually points into .rdata/.data.
        has_chd = False
        for sec in view.sections:
            if not sec["name"].lower().startswith((".rdata", ".data")):
                continue
            s0 = sec["va"]
            s1 = s0 + len(sec["data"])
            if s0 <= int(chd) < s1:
                has_chd = True
                break
        return has_chd

    for s in strings:
        text = s.get("text", "")
        # Focus on concrete class RTTI names (e.g. .?AVCWorkerBehavior@GGL@@),
        # skip template-instantiated handler types to reduce noise.
        if not text.startswith(".?AVC"):
            continue

        class_name = text
        td_va = int(s["va"]) - td_name_offset
        td_refs = find_va_references(
            view, td_va, section_prefixes=[".rdata", ".data"], max_hits=256
        )
        # In MSVC x86 COL: signature, offset, cdOffset, pTypeDescriptor, pClassDesc
        for td_ref in td_refs:
            col_va = td_ref - 12
            if not _is_probably_col(col_va, td_va):
                continue
            col_refs = find_va_references(
                view, col_va, section_prefixes=[".rdata", ".data"], max_hits=256
            )
            for col_ref in col_refs:
                # vftable starts right after COL pointer
                vtable_start = col_ref + ptr
                methods: List[int] = []
                for slot in range(0, 96):
                    mptr = view.read_pointer(vtable_start + slot * ptr)
                    if mptr is None or not view.in_text(mptr):
                        break
                    methods.append(mptr)
                if len(methods) < 1:
                    continue
                for slot, mptr in enumerate(methods):
                    fstart = guess_function_start(mptr, prologues, max_back=0x2000)
                    out.append(
                        {
                            "function_start": fstart,
                            "method_target": mptr,
                            "slot": slot,
                            "class_name": class_name,
                            "type_descriptor_va": f"0x{td_va:08x}",
                            "complete_object_locator_va": f"0x{col_va:08x}",
                            "vtable_va": f"0x{vtable_start:08x}",
                        }
                    )
    return out


def disassemble_cfg(
    view: PEView,
    func_start: int,
    prologue_set: Set[int],
    max_func_span: int = 0x4000,
    max_insns_total: int = 20000,
) -> Dict[str, Any]:
    mode = CS_MODE_64 if view.is_64 else CS_MODE_32
    md = Cs(CS_ARCH_X86, mode)
    md.detail = True

    text = view.text_section
    assert text is not None
    text_va = text["va"]
    text_data = text["data"]
    text_end = text_va + len(text_data)

    def read_bytes(va: int, size: int) -> bytes:
        if va < text_va or va >= text_end:
            return b""
        off = va - text_va
        return text_data[off : off + size]

    def _tail_context(insns: List[Dict[str, Any]], count: int = 4) -> List[str]:
        out: List[str] = []
        for item in insns[-count:]:
            op = item.get("op_str", "")
            text = f"0x{item['address']:08x}: {item['mnemonic']}"
            if op:
                text += f" {op}"
            out.append(text)
        return out

    block_work: List[int] = [func_start]
    visited_blocks: Set[int] = set()
    blocks: Dict[int, Dict[str, Any]] = {}
    edges: List[Dict[str, Any]] = []
    total_insns = 0
    truncated = False

    while block_work:
        bstart = block_work.pop(0)
        if bstart in visited_blocks:
            continue
        if not view.in_text(bstart):
            continue
        if bstart - func_start > max_func_span:
            continue

        visited_blocks.add(bstart)
        insns_out: List[Dict[str, Any]] = []
        succ: List[int] = []

        va = bstart
        stop_reason = "fallthrough"
        while True:
            if total_insns >= max_insns_total:
                truncated = True
                stop_reason = "max_insns_total"
                break
            if va < text_va or va >= text_end:
                stop_reason = "out_of_text"
                break
            if va - func_start > max_func_span:
                stop_reason = "max_func_span"
                break
            if va != bstart and va in prologue_set:
                stop_reason = "hit_next_prologue"
                break

            blob = read_bytes(va, 16)
            if not blob:
                stop_reason = "no_bytes"
                break
            insn_list = list(md.disasm(blob, va, count=1))
            if not insn_list:
                stop_reason = "decode_fail"
                break
            insn = insn_list[0]
            total_insns += 1

            item = {
                "address": insn.address,
                "mnemonic": insn.mnemonic,
                "op_str": insn.op_str,
                "size": insn.size,
                "bytes": insn.bytes.hex(),
            }
            insns_out.append(item)

            mnem = insn.mnemonic.lower()

            # Return / stop instructions.
            if mnem.startswith("ret") or mnem in {"int3", "ud2", "hlt"}:
                stop_reason = "ret_or_stop"
                break

            # Jumps.
            if mnem.startswith("j"):
                if mnem == "jmp":
                    if insn.operands and insn.operands[0].type == X86_OP_IMM:
                        tgt = int(insn.operands[0].imm)
                        succ.append(tgt)
                        edges.append(
                            {
                                "from": bstart,
                                "to": tgt,
                                "type": "jmp",
                                "at": insn.address,
                                "mnemonic": mnem,
                                "context": _tail_context(insns_out),
                            }
                        )
                        block_work.append(tgt)
                    else:
                        edges.append(
                            {
                                "from": bstart,
                                "to": None,
                                "type": "jmp_indirect",
                                "at": insn.address,
                                "mnemonic": mnem,
                                "op_str": insn.op_str,
                                "context": _tail_context(insns_out),
                            }
                        )
                    stop_reason = "jmp"
                    break
                else:
                    # Conditional jump: target + fallthrough
                    if insn.operands and insn.operands[0].type == X86_OP_IMM:
                        tgt = int(insn.operands[0].imm)
                        succ.append(tgt)
                        edges.append(
                            {
                                "from": bstart,
                                "to": tgt,
                                "type": "jcc_true",
                                "at": insn.address,
                                "mnemonic": mnem,
                                "context": _tail_context(insns_out),
                            }
                        )
                        block_work.append(tgt)
                    fall = insn.address + insn.size
                    succ.append(fall)
                    edges.append(
                        {
                            "from": bstart,
                            "to": fall,
                            "type": "jcc_false",
                            "at": insn.address,
                            "mnemonic": mnem,
                            "context": _tail_context(insns_out),
                        }
                    )
                    block_work.append(fall)
                    stop_reason = "jcc"
                    break

            # Call (do not terminate block).
            if mnem == "call":
                if insn.operands and insn.operands[0].type == X86_OP_IMM:
                    tgt = int(insn.operands[0].imm)
                    edges.append(
                        {
                            "from": bstart,
                            "to": tgt,
                            "type": "call_direct",
                            "at": insn.address,
                            "mnemonic": mnem,
                        }
                    )
                else:
                    edges.append(
                        {
                            "from": bstart,
                            "to": None,
                            "type": "call_indirect",
                            "at": insn.address,
                            "mnemonic": mnem,
                            "op_str": insn.op_str,
                        }
                    )

            va = insn.address + insn.size

        blocks[bstart] = {
            "start": bstart,
            "insns": insns_out,
            "succ": sorted(set(succ)),
            "stop_reason": stop_reason,
        }

    # Aggregate stats.
    edge_types: Dict[str, int] = {}
    for e in edges:
        et = e["type"]
        edge_types[et] = edge_types.get(et, 0) + 1

    cond_branches = edge_types.get("jcc_true", 0)
    switch_candidates = edge_types.get("jmp_indirect", 0)

    # Dedup edges.
    dedup_edges: List[Dict[str, Any]] = []
    seen = set()
    for e in edges:
        key = (e.get("from"), e.get("to"), e.get("type"), e.get("at"), e.get("mnemonic"), e.get("op_str"))
        if key in seen:
            continue
        seen.add(key)
        dedup_edges.append(e)

    return {
        "entry": func_start,
        "blocks": {f"0x{k:08x}": v for k, v in sorted(blocks.items(), key=lambda kv: kv[0])},
        "edges": dedup_edges,
        "stats": {
            "block_count": len(blocks),
            "instruction_count": sum(len(v["insns"]) for v in blocks.values()),
            "edge_count": len(dedup_edges),
            "conditional_branches": cond_branches,
            "switch_candidates_indirect_jmp": switch_candidates,
            "edge_type_counts": edge_types,
            "truncated": truncated,
        },
    }


def build_report(exe_path: Path) -> Dict[str, Any]:
    view = PEView(exe_path)
    strings = find_target_strings(view, TARGET_PATTERNS)

    # Xrefs and function candidates.
    prologues = scan_prologues(view)
    prologue_set = set(prologues)
    direct_calls = scan_direct_calls(view)
    caller_index = build_caller_index(direct_calls)

    # Expansion controls.
    caller_expansion_depth = 3
    caller_match_window = 0x20
    max_callers_per_entry = 120
    max_functions = 500

    string_entries: List[Dict[str, Any]] = []
    function_to_reasons: Dict[int, List[Dict[str, Any]]] = {}

    for s in strings:
        va = s["va"]
        xrefs = find_text_xrefs_to_va(view, va)
        xrefs = sorted(set(xrefs))
        s_entry = dict(s)
        s_entry["xrefs"] = [f"0x{x:08x}" for x in xrefs[:400]]
        s_entry["xref_count"] = len(xrefs)
        string_entries.append(s_entry)

        for xr in xrefs[:400]:
            fstart = guess_function_start(xr, prologues)
            reason = {
                "reason_type": "string_xref",
                "string": s["text"],
                "pattern": s["pattern"],
                "string_va": f"0x{va:08x}",
                "xref_at": f"0x{xr:08x}",
            }
            function_to_reasons.setdefault(fstart, []).append(reason)

    # RTTI/VTable method anchors for classes where direct string xrefs are absent.
    rtti_method_anchors = extract_rtti_vtable_methods(view, strings, prologues)
    for item in rtti_method_anchors:
        fstart = item["function_start"]
        reason = {
            "reason_type": "rtti_vtable_method",
            "class_name": item["class_name"],
            "slot": item["slot"],
            "method_target": f"0x{int(item['method_target']):08x}",
            "type_descriptor_va": item["type_descriptor_va"],
            "complete_object_locator_va": item["complete_object_locator_va"],
            "vtable_va": item["vtable_va"],
        }
        function_to_reasons.setdefault(fstart, []).append(reason)

    # Expand around anchored functions by walking callers (reverse call-graph).
    queue: List[Tuple[int, int]] = [(f, 0) for f in sorted(function_to_reasons.keys())]
    best_depth: Dict[int, int] = {f: 0 for f in function_to_reasons.keys()}

    while queue:
        callee_entry, depth = queue.pop(0)
        if depth >= caller_expansion_depth:
            continue

        callers = find_callers_for_entry(
            caller_index, callee_entry, window=caller_match_window
        )
        if len(callers) > max_callers_per_entry:
            callers = callers[:max_callers_per_entry]

        for site in callers:
            caller_entry = guess_function_start(site, prologues)
            reason = {
                "reason_type": "caller_of_anchor_path",
                "depth": depth + 1,
                "callee_entry": f"0x{callee_entry:08x}",
                "call_site": f"0x{site:08x}",
            }
            function_to_reasons.setdefault(caller_entry, []).append(reason)
            if caller_entry not in best_depth or depth + 1 < best_depth[caller_entry]:
                best_depth[caller_entry] = depth + 1
                queue.append((caller_entry, depth + 1))

            # Keep the run bounded.
            if len(function_to_reasons) >= max_functions:
                queue.clear()
                break

    # Build CFGs.
    functions: Dict[str, Any] = {}
    for fstart in sorted(function_to_reasons.keys()):
        cfg = disassemble_cfg(view, fstart, prologue_set)
        functions[f"0x{fstart:08x}"] = {
            "entry": f"0x{fstart:08x}",
            "reasons": function_to_reasons[fstart],
            "cfg": cfg,
        }

    # Global stats.
    total_blocks = sum(v["cfg"]["stats"]["block_count"] for v in functions.values())
    total_insns = sum(v["cfg"]["stats"]["instruction_count"] for v in functions.values())
    total_cond = sum(v["cfg"]["stats"]["conditional_branches"] for v in functions.values())
    total_switch = sum(v["cfg"]["stats"]["switch_candidates_indirect_jmp"] for v in functions.values())

    return {
        "meta": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "binary": str(exe_path),
            "binary_size_bytes": exe_path.stat().st_size,
            "machine": hex(view.machine),
            "arch": "x64" if view.is_64 else "x86",
            "image_base": hex(view.image_base),
            "text_section_va_start": hex(view.text_bounds()[0]),
            "text_section_va_end": hex(view.text_bounds()[1]),
            "target_pattern_count": len(TARGET_PATTERNS),
            "matched_string_count": len(string_entries),
            "prologue_count": len(prologues),
            "direct_call_sites_in_text": len(direct_calls),
            "rtti_vtable_method_anchor_count": len(rtti_method_anchors),
            "rtti_class_count": len(
                {x.get("class_name") for x in rtti_method_anchors if x.get("class_name")}
            ),
            "caller_expansion_depth": caller_expansion_depth,
            "caller_match_window_bytes": caller_match_window,
            "max_callers_per_entry": max_callers_per_entry,
            "max_functions": max_functions,
            "limitations": [
                "Function starts are heuristic (prologue-based).",
                "Indirect control-flow targets are not fully resolved.",
                "This is static analysis without dynamic execution traces.",
            ],
        },
        "strings": string_entries,
        "functions": functions,
        "summary": {
            "function_count": len(functions),
            "total_blocks": total_blocks,
            "total_instructions": total_insns,
            "total_conditional_branches": total_cond,
            "total_switch_candidates_indirect_jmp": total_switch,
        },
    }


def build_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    meta = report["meta"]
    summary = report["summary"]

    lines.append("# Engine Instruction CFG Reconstruction")
    lines.append("")
    lines.append(f"- Binary: `{meta['binary']}`")
    lines.append(f"- Arch: `{meta['arch']}` (`machine={meta['machine']}`)")
    lines.append(f"- ImageBase: `{meta['image_base']}`")
    lines.append(
        f"- .text: `{meta['text_section_va_start']}` -> `{meta['text_section_va_end']}`"
    )
    lines.append(f"- Target patterns: {meta['target_pattern_count']}")
    lines.append(f"- Matched strings: {meta['matched_string_count']}")
    lines.append(f"- Direct call sites in .text: {meta['direct_call_sites_in_text']}")
    lines.append(
        f"- RTTI vtable method anchors: {meta.get('rtti_vtable_method_anchor_count', 0)} "
        f"(classes: {meta.get('rtti_class_count', 0)})"
    )
    lines.append(
        f"- Caller expansion: depth={meta['caller_expansion_depth']}, "
        f"window=0x{int(meta['caller_match_window_bytes']):x}, "
        f"max_callers/entry={meta['max_callers_per_entry']}, "
        f"max_functions={meta['max_functions']}"
    )
    lines.append(f"- Candidate functions: {summary['function_count']}")
    lines.append(f"- Total basic blocks: {summary['total_blocks']}")
    lines.append(f"- Total instructions: {summary['total_instructions']}")
    lines.append(f"- Conditional branches: {summary['total_conditional_branches']}")
    lines.append(
        f"- Switch candidates (indirect jmp): {summary['total_switch_candidates_indirect_jmp']}"
    )
    lines.append("")

    lines.append("## Matched Strings")
    lines.append("")
    for s in report["strings"]:
        lines.append(
            f"- `{s['text']}` (pattern `{s['pattern']}`, va `0x{s['va']:08x}`, xrefs {s['xref_count']})"
        )
    lines.append("")

    lines.append("## Functions")
    lines.append("")
    for faddr, f in report["functions"].items():
        stats = f["cfg"]["stats"]
        lines.append(f"### {faddr}")
        lines.append(
            f"- blocks={stats['block_count']}, insns={stats['instruction_count']}, "
            f"edges={stats['edge_count']}, jcc={stats['conditional_branches']}, "
            f"indirect_jmp={stats['switch_candidates_indirect_jmp']}, truncated={stats['truncated']}"
        )
        lines.append("- reasons:")
        for r in f["reasons"][:20]:
            if r.get("reason_type") == "string_xref":
                lines.append(
                    f"  - string_xref: {r['pattern']} via `{r['string']}` "
                    f"(string {r['string_va']}, xref {r['xref_at']})"
                )
            elif r.get("reason_type") == "caller_of_anchor_path":
                lines.append(
                    f"  - caller_of_anchor_path: depth {r.get('depth')} "
                    f"(calls {r.get('callee_entry')} at {r.get('call_site')})"
                )
            elif r.get("reason_type") == "rtti_vtable_method":
                lines.append(
                    f"  - rtti_vtable_method: {r.get('class_name')} slot {r.get('slot')} "
                    f"(target {r.get('method_target')}, vtable {r.get('vtable_va')})"
                )
            else:
                lines.append(f"  - {json.dumps(r, ensure_ascii=False)}")
        if len(f["reasons"]) > 20:
            lines.append(f"  - ... {len(f['reasons']) - 20} more")

        lines.append("- branch points:")
        branch_lines = []
        for e in f["cfg"]["edges"]:
            if e["type"] in {"jcc_true", "jcc_false", "jmp", "jmp_indirect"}:
                at = e.get("at")
                to = e.get("to")
                m = e.get("mnemonic")
                if to is None:
                    ctx = e.get("context", [])
                    ctx_text = f" | ctx: {' ; '.join(ctx)}" if ctx else ""
                    branch_lines.append(
                        f"  - 0x{at:08x}: {m} {e.get('op_str','')} -> <indirect>{ctx_text}"
                    )
                else:
                    ctx = e.get("context", [])
                    ctx_text = f" | ctx: {' ; '.join(ctx)}" if ctx else ""
                    branch_lines.append(
                        f"  - 0x{at:08x}: {m} -> 0x{int(to):08x} ({e['type']}){ctx_text}"
                    )
        if branch_lines:
            lines.extend(branch_lines[:80])
            if len(branch_lines) > 80:
                lines.append(f"  - ... {len(branch_lines) - 80} more")
        else:
            lines.append("  - none")
        lines.append("")

    lines.append("## Limits")
    lines.append("")
    for lim in meta["limitations"]:
        lines.append(f"- {lim}")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reconstruct instruction-level CFG from SettlersHoK.exe"
    )
    parser.add_argument(
        "--exe",
        type=Path,
        default=DEFAULT_EXE,
        help=f"Path to SettlersHoK.exe (default: {DEFAULT_EXE})",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=DEFAULT_JSON,
        help=f"Output JSON (default: {DEFAULT_JSON})",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=DEFAULT_MD,
        help=f"Output markdown (default: {DEFAULT_MD})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    exe_path = args.exe.resolve()
    out_json = args.output_json.resolve()
    out_md = args.output_md.resolve()

    if not exe_path.exists():
        raise FileNotFoundError(f"Binary not found: {exe_path}")

    report = build_report(exe_path)
    md = build_markdown(report)

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(md, encoding="utf-8")

    print("Instruction CFG reconstruction complete")
    print(f"Binary: {exe_path}")
    print(f"JSON: {out_json}")
    print(f"MD: {out_md}")
    print(f"Functions: {report['summary']['function_count']}")
    print(f"Blocks: {report['summary']['total_blocks']}")
    print(f"Instructions: {report['summary']['total_instructions']}")
    print(f"Conditional branches: {report['summary']['total_conditional_branches']}")
    print(
        "Switch candidates (indirect jmp): "
        f"{report['summary']['total_switch_candidates_indirect_jmp']}"
    )


if __name__ == "__main__":
    main()
