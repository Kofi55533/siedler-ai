# -*- coding: utf-8 -*-
"""
Dump all original Settlers 5 XML values (offline, no game runtime required).

Writes:
- JSONL with one value per line (path + value + source file)
- Manifest JSON with source and statistics
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
import xml.etree.ElementTree as ET

from engine_decoder import OverlayPaths


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUT_JSONL = SCRIPT_DIR / "config" / "all_original_values.jsonl"
DEFAULT_OUT_MANIFEST = SCRIPT_DIR / "config" / "all_original_values_manifest.json"


def safe_text(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip()
    return text if text else None


def element_label(elem: ET.Element) -> str:
    # Use stable labels so paths remain understandable in large dumps.
    for attr in ("id", "name", "classname", "Class"):
        if attr in elem.attrib:
            val = elem.attrib[attr].replace("'", "\\'")
            return f"{elem.tag}[@{attr}='{val}']"
    return elem.tag


def iter_element_values(
    elem: ET.Element, path_prefix: str
) -> Iterable[Tuple[str, str, str, str]]:
    label = element_label(elem)
    base_path = f"{path_prefix}/{label}" if path_prefix else label

    for attr_key, attr_val in sorted(elem.attrib.items(), key=lambda kv: kv[0]):
        yield (base_path, "attr", attr_key, attr_val)

    text = safe_text(elem.text)
    if text is not None:
        yield (base_path, "text", "#text", text)

    for child in list(elem):
        yield from iter_element_values(child, base_path)


def build_overlay_file_map(paths: OverlayPaths) -> Dict[str, Dict[str, str]]:
    # Merge base -> extra1 -> extra2 by relative path key.
    merged: Dict[str, Dict[str, str]] = {}
    for cfg in reversed(paths.config_roots):
        for xml_file in cfg.rglob("*.xml"):
            rel = xml_file.relative_to(cfg).as_posix()
            key = rel.lower()
            merged[key] = {
                "relative_path": rel,
                "absolute_path": str(xml_file),
                "layer_root": str(cfg),
            }
    return merged


def dump_all_values(game_root: str | None, out_jsonl: Path, out_manifest: Path) -> None:
    paths = OverlayPaths.detect(game_root)
    files = build_overlay_file_map(paths)

    out_jsonl.parent.mkdir(parents=True, exist_ok=True)

    total_values = 0
    parsed_files = 0
    failed_files = 0
    file_stats: List[Dict[str, object]] = []

    with out_jsonl.open("w", encoding="utf-8") as sink:
        for key in sorted(files.keys()):
            entry = files[key]
            rel = entry["relative_path"]
            abs_path = Path(entry["absolute_path"])

            file_info: Dict[str, object] = {
                "relative_path": rel,
                "absolute_path": str(abs_path),
            }
            try:
                raw = abs_path.read_bytes()
                sha1 = hashlib.sha1(raw).hexdigest()
                file_info["sha1"] = sha1

                try:
                    text = raw.decode("utf-8-sig")
                except UnicodeDecodeError:
                    text = raw.decode("latin-1")

                root = ET.fromstring(text)
                local_count = 0

                for value_path, value_kind, value_key, value in iter_element_values(root, ""):
                    line = {
                        "file": rel,
                        "path": value_path,
                        "kind": value_kind,
                        "key": value_key,
                        "value": value,
                    }
                    sink.write(json.dumps(line, ensure_ascii=False) + "\n")
                    local_count += 1
                    total_values += 1

                file_info["value_count"] = local_count
                file_info["status"] = "ok"
                parsed_files += 1
            except Exception as exc:
                # Fallback: salvage simple tag-text pairs from malformed XML.
                local_count = 0
                try:
                    text = abs_path.read_text(encoding="utf-8-sig", errors="ignore")
                except Exception:
                    text = ""

                for tag, value in re.findall(r"<([A-Za-z0-9_:-]+)>\s*([^<]+?)\s*</\1>", text):
                    line = {
                        "file": rel,
                        "path": f"FALLBACK/{tag}",
                        "kind": "fallback_text",
                        "key": "#text",
                        "value": value.strip(),
                    }
                    sink.write(json.dumps(line, ensure_ascii=False) + "\n")
                    local_count += 1
                    total_values += 1

                if local_count > 0:
                    file_info["status"] = "fallback_regex"
                    file_info["value_count"] = local_count
                    file_info["parse_error"] = str(exc)
                    parsed_files += 1
                else:
                    file_info["status"] = "error"
                    file_info["error"] = str(exc)
                    failed_files += 1

            file_stats.append(file_info)

    manifest = {
        "engine_source": paths.debug_info(),
        "outputs": {
            "values_jsonl": str(out_jsonl),
            "manifest_json": str(out_manifest),
        },
        "summary": {
            "merged_xml_files": len(files),
            "parsed_files": parsed_files,
            "failed_files": failed_files,
            "total_values": total_values,
        },
        "files": file_stats,
    }
    out_manifest.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Done. Files={len(files)} parsed={parsed_files} failed={failed_files}")
    print(f"Total values dumped: {total_values}")
    print(f"Values JSONL: {out_jsonl}")
    print(f"Manifest: {out_manifest}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Dump all original Settlers 5 XML values (offline)."
    )
    parser.add_argument(
        "--game-root",
        default=None,
        help=(
            "Path to game root (contains base/extra1/extra2) or config root "
            "(contains Logic.xml, Entities, TaskLists)."
        ),
    )
    parser.add_argument(
        "--out-jsonl",
        default=str(DEFAULT_OUT_JSONL),
        help=f"Output JSONL file (default: {DEFAULT_OUT_JSONL})",
    )
    parser.add_argument(
        "--out-manifest",
        default=str(DEFAULT_OUT_MANIFEST),
        help=f"Output manifest JSON (default: {DEFAULT_OUT_MANIFEST})",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    dump_all_values(
        game_root=args.game_root,
        out_jsonl=Path(args.out_jsonl).resolve(),
        out_manifest=Path(args.out_manifest).resolve(),
    )


if __name__ == "__main__":
    main()
