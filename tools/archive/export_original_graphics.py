#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Export local Settlers 5 original-graphics evidence and previews.

The exporter does not copy raw proprietary model/animation files into git-tracked
paths. It creates an ignored local report under analysis/replays/... that proves
which original assets were found and converts selected DDS texture atlases plus
static DFF mesh projections into PNG previews.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import os
import struct
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageChops, ImageDraw

ROOT_DIR = Path(__file__).resolve().parents[2]

RW_STRUCT = 0x0001
RW_STRING = 0x0002
RW_EXTENSION = 0x0003
RW_TEXTURE = 0x0006
RW_MATERIAL = 0x0007
RW_MATERIAL_LIST = 0x0008
RW_FRAME_LIST = 0x000E
RW_GEOMETRY = 0x000F
RW_CLUMP = 0x0010
RW_ATOMIC = 0x0014
RW_GEOMETRY_LIST = 0x001A
RW_ANIMATION = 0x001B
RW_SKIN_PLUGIN = 0x0116
RW_HANIM_PLUGIN = 0x011E

RW_CONTAINER_TYPES = {
    RW_EXTENSION,
    RW_TEXTURE,
    RW_MATERIAL,
    RW_MATERIAL_LIST,
    RW_FRAME_LIST,
    RW_GEOMETRY,
    RW_CLUMP,
    RW_ATOMIC,
    RW_GEOMETRY_LIST,
}

_TEXTURE_INDEX_CACHE: dict[str, dict[str, Path]] = {}
_TEXTURE_IMAGE_CACHE: dict[str, Image.Image | None] = {}


@dataclass(frozen=True)
class EntitySpec:
    key: str
    label: str
    group: str
    model_globs: tuple[str, ...] = ()
    texture_globs: tuple[str, ...] = ()
    animation_globs: tuple[str, ...] = ()
    gui_globs: tuple[str, ...] = ()


def _pb_spec(
    key: str,
    label: str,
    group: str,
    stem: str,
    animation_globs: tuple[str, ...] = (),
    gui_globs: tuple[str, ...] = (),
) -> EntitySpec:
    return EntitySpec(key, label, group, (f"{stem}.dff",), (f"{stem}*.dds",), animation_globs, gui_globs)


ENTITY_SPECS: tuple[EntitySpec, ...] = (
    EntitySpec(
        "serf_idle",
        "Leibeigener",
        "units",
        ("PU_Serf.dff",),
        ("PU_Serf.dds",),
        ("PU_Serf_Idle*.anm", "PU_Serf_Walk.anm", "PU_Serf_Run.anm"),
        ("MO_CU_Serf.png", "b_select_serf.png", "b_units_serf.png"),
    ),
    EntitySpec(
        "serf_wood",
        "Leibeigener mit Axt",
        "units",
        ("PU_SerfAxe.dff",),
        ("PU_Serf.dds",),
        ("PU_SerfAxe_*.anm",),
        ("MO_CU_Serf.png", "b_select_serf.png"),
    ),
    EntitySpec(
        "serf_build",
        "Leibeigener mit Hammer",
        "units",
        ("PU_SerfHammer.dff",),
        ("PU_Serf.dds",),
        ("PU_SerfHammer_*.anm",),
        ("MO_CU_Serf.png", "b_select_serf.png"),
    ),
    EntitySpec(
        "serf_mine",
        "Leibeigener mit Spitzhacke",
        "units",
        ("PU_SerfPickax.dff",),
        ("PU_Serf.dds",),
        ("PU_SerfPickax_*.anm",),
        ("MO_CU_Serf.png", "b_select_serf.png"),
    ),
    EntitySpec("worker_miner", "Minenarbeiter", "workers", ("PU_Miner.dff",), ("PU_Miner.dds",), ("PU_Miner_*.anm",), ("MO_PU_Miner.png",)),
    EntitySpec(
        "worker_sawmill",
        "Saegemuehlenarbeiter",
        "workers",
        ("Pu_Sawmillworker.dff", "PU_SawmillworkerCarry.dff"),
        ("PU_SawmillWorker.dds",),
        ("PU_Sawmillworker*.anm",),
        ("MO_PU_Sawmillworker.png",),
    ),
    EntitySpec(
        "worker_stonecutter",
        "Steinmetzarbeiter",
        "workers",
        ("PU_Stonecutter.dff", "PU_StonecutterCarry.dff"),
        ("Pu_Stonemason.dds",),
        ("PU_Stonecutter*.anm",),
        ("MO_PU_Stonecutter.png",),
    ),
    EntitySpec(
        "worker_brickmaker",
        "Ziegelarbeiter",
        "workers",
        ("Pu_BrickMaker.dff", "PU_BrickMakerCarry.dff"),
        ("PU_BrickMaker.dds",),
        ("PU_BrickMaker*.anm",),
        ("MO_PU_BrickMaker.png",),
    ),
    EntitySpec("worker_farmer", "Farmer", "workers", ("PU_Farmer.dff",), ("PU_Farmer.dds",), ("PU_Farmer*.anm",), ("MO_PU_Farmer.png",)),
    EntitySpec("worker_scholar", "Gelehrter", "workers", ("PU_Scholar.dff",), ("PU_Scholar.dds",), ("PU_Scholar*.anm",), ("MO_PU_Scholar.png",)),
    EntitySpec("worker_priest", "Priester", "workers", ("PU_Priest.dff",), ("PU_Priest.dds",), ("PU_Priest*.anm",), ("MO_PU_Priest.png",)),
    EntitySpec("headquarters_1", "Hauptquartier 1", "buildings", ("PB_Headquarters1.dff",), ("PB_Headquarters1*.dds",), (), ("b_headquarter.png",)),
    EntitySpec("university_1", "Hochschule 1", "buildings", ("PB_University1.dff",), ("PB_University1.dds",), (), ("b_civil_university.png",)),
    EntitySpec("monastery_1", "Kloster 1", "buildings", ("PB_Monastery1.dff",), ("PB_Monastery1.dds", "Monastery.dds"), (), ("b_civil_church.png",)),
    EntitySpec("village_center_1", "Dorfzentrum 1", "buildings", ("PB_VillageCenter1.dff",), ("PB_VillageCenter1*.dds", "XD_VillageCenter.dds"), (), ("b_civil_keep.png",)),
    EntitySpec("residence_1", "Wohnhaus 1", "buildings", ("PB_Residence1.dff",), ("PB_Residence1*.dds",), (), ("i_res_residences.png",)),
    EntitySpec("farm_1", "Bauernhof 1", "buildings", ("PB_Farm1.dff",), ("PB_Farm1.dds",), (), ("i_res_farms.png",)),
    _pb_spec("headquarters_2", "Hauptquartier 2", "buildings", "PB_Headquarters2", gui_globs=("b_headquarter.png",)),
    _pb_spec("headquarters_3", "Hauptquartier 3", "buildings", "PB_Headquarters3", gui_globs=("b_headquarter.png",)),
    _pb_spec("university_2", "Hochschule 2", "buildings", "PB_University2", gui_globs=("b_civil_university.png",)),
    _pb_spec("monastery_2", "Kloster 2", "buildings", "PB_Monastery2", gui_globs=("b_civil_church.png",)),
    _pb_spec("monastery_3", "Kloster 3", "buildings", "PB_Monastery3", gui_globs=("b_civil_church.png",)),
    _pb_spec("village_center_2", "Dorfzentrum 2", "buildings", "PB_VillageCenter2", gui_globs=("b_civil_keep.png",)),
    _pb_spec("village_center_3", "Dorfzentrum 3", "buildings", "PB_VillageCenter3", gui_globs=("b_civil_keep.png",)),
    _pb_spec("residence_2", "Wohnhaus 2", "buildings", "PB_Residence2", gui_globs=("i_res_residences.png",)),
    _pb_spec("residence_3", "Wohnhaus 3", "buildings", "PB_Residence3", gui_globs=("i_res_residences.png",)),
    _pb_spec("farm_2", "Bauernhof 2", "buildings", "PB_Farm2", gui_globs=("i_res_farms.png",)),
    _pb_spec("farm_3", "Bauernhof 3", "buildings", "PB_Farm3", gui_globs=("i_res_farms.png",)),
    _pb_spec("sawmill_1", "Saegemuehle 1", "worker_buildings", "PB_Sawmill1"),
    _pb_spec("sawmill_2", "Saegemuehle 2", "worker_buildings", "PB_Sawmill2"),
    _pb_spec("stonemason_1", "Steinmetzhuette 1", "worker_buildings", "PB_StoneMason1"),
    _pb_spec("stonemason_2", "Steinmetzhuette 2", "worker_buildings", "PB_StoneMason2"),
    _pb_spec("brickworks_1", "Lehmhuette 1", "worker_buildings", "PB_Brickworks1"),
    _pb_spec("brickworks_2", "Lehmhuette 2", "worker_buildings", "PB_Brickworks2"),
    _pb_spec("alchemist_1", "Alchimistenhuette 1", "worker_buildings", "PB_Alchemist1"),
    _pb_spec("alchemist_2", "Alchimistenhuette 2", "worker_buildings", "PB_Alchemist2"),
    _pb_spec("blacksmith_1", "Schmiede 1", "worker_buildings", "PB_Blacksmith1"),
    _pb_spec("blacksmith_2", "Schmiede 2", "worker_buildings", "PB_Blacksmith2"),
    _pb_spec("blacksmith_3", "Schmiede 3", "worker_buildings", "PB_Blacksmith3"),
    _pb_spec("bank_1", "Bank 1", "worker_buildings", "PB_Bank1"),
    _pb_spec("bank_2", "Bank 2", "worker_buildings", "PB_Bank2"),
    _pb_spec("market_1", "Markt 1", "worker_buildings", "PB_Market1"),
    _pb_spec("market_2", "Markt 2", "worker_buildings", "PB_Market2"),
    _pb_spec("barracks_1", "Kaserne 1", "military_buildings", "PB_Barracks1"),
    _pb_spec("barracks_2", "Kaserne 2", "military_buildings", "PB_Barracks2"),
    _pb_spec("archery_1", "Schiessplatz 1", "military_buildings", "PB_Archery1"),
    _pb_spec("archery_2", "Schiessplatz 2", "military_buildings", "PB_Archery2"),
    _pb_spec("stable_1", "Stall 1", "military_buildings", "PB_Stable1"),
    _pb_spec("stable_2", "Stall 2", "military_buildings", "PB_Stable2"),
    _pb_spec("foundry_1", "Kanongiesserei 1", "military_buildings", "PB_Foundry1"),
    _pb_spec("foundry_2", "Kanongiesserei 2", "military_buildings", "PB_Foundry2"),
    _pb_spec("gunsmith_1", "Buechsenmacherei 1", "military_buildings", "PB_GunsmithWorkshop1"),
    _pb_spec("gunsmith_2", "Buechsenmacherei 2", "military_buildings", "PB_GunsmithWorkshop2"),
    _pb_spec("tavern_1", "Taverne 1", "worker_buildings", "PB_Tavern1"),
    _pb_spec("tavern_2", "Taverne 2", "worker_buildings", "PB_Tavern2"),
    _pb_spec("tower_1", "Turm 1", "military_buildings", "PB_Tower1"),
    _pb_spec("tower_2", "Turm 2", "military_buildings", "PB_Tower2"),
    _pb_spec("tower_3", "Turm 3", "military_buildings", "PB_Tower3"),
    _pb_spec("weather_tower_1", "Wetterturm", "buildings", "PB_WeatherTower1"),
    _pb_spec("power_plant_1", "Wetterkraftwerk", "buildings", "PB_PowerPlant1"),
    _pb_spec("master_builder_workshop", "Architektenstube", "buildings", "PB_MasterBuilderWorkshop"),
    _pb_spec("bridge_1", "Bruecke", "buildings", "PB_Bridge1"),
    *tuple(
        _pb_spec(f"beautification_{index:02d}", f"Dekoration {index:02d}", "buildings", f"PB_Beautification{index:02d}")
        for index in range(1, 13)
    ),
    EntitySpec("clay_mine_1", "Lehmmine 1", "mines", ("PB_ClayMine1.dff",), ("PB_ClayMine1.dds",), ("PB_ClayMine*.anm",), ("b_small_generic.png",)),
    EntitySpec("iron_mine_1", "Eisenmine 1", "mines", ("PB_IronMine1.dff",), ("PB_IronMine1.dds",), ("PB_IronMine*.anm",), ("b_small_generic.png",)),
    EntitySpec("stone_mine_1", "Steinmine 1", "mines", ("PB_StoneMine1.dff",), ("PB_StoneMine1.dds",), ("PB_StoneMine*.anm",), ("b_small_generic.png",)),
    EntitySpec("sulfur_mine_1", "Schwefelmine 1", "mines", ("PB_SulfurMine1.dff",), ("PB_SulfurMine1.dds",), ("PB_SulfurMine*.anm",), ("b_small_generic.png",)),
    _pb_spec("clay_mine_2", "Lehmmine 2", "mines", "PB_ClayMine2", animation_globs=("PB_ClayMine*.anm",), gui_globs=("b_small_generic.png",)),
    _pb_spec("clay_mine_3", "Lehmmine 3", "mines", "PB_ClayMine3", animation_globs=("PB_ClayMine*.anm",), gui_globs=("b_small_generic.png",)),
    _pb_spec("iron_mine_2", "Eisenmine 2", "mines", "PB_IronMine2", animation_globs=("PB_IronMine*.anm",), gui_globs=("b_small_generic.png",)),
    _pb_spec("iron_mine_3", "Eisenmine 3", "mines", "PB_IronMine3", animation_globs=("PB_IronMine*.anm",), gui_globs=("b_small_generic.png",)),
    _pb_spec("stone_mine_2", "Steinmine 2", "mines", "PB_StoneMine2", animation_globs=("PB_StoneMine*.anm",), gui_globs=("b_small_generic.png",)),
    _pb_spec("stone_mine_3", "Steinmine 3", "mines", "PB_StoneMine3", animation_globs=("PB_StoneMine*.anm",), gui_globs=("b_small_generic.png",)),
    _pb_spec("sulfur_mine_2", "Schwefelmine 2", "mines", "PB_SulfurMine2", animation_globs=("PB_SulfurMine*.anm",), gui_globs=("b_small_generic.png",)),
    _pb_spec("sulfur_mine_3", "Schwefelmine 3", "mines", "PB_SulfurMine3", animation_globs=("PB_SulfurMine*.anm",), gui_globs=("b_small_generic.png",)),
    EntitySpec("generic_mine_site", "Minen-Baustelle/Slot", "mines", ("PB_GenericMine.dff",), ("PB_GenericMine.dds",), (), ("b_small_generic.png",)),
    EntitySpec("tree_fir", "Tanne/Fichte", "resources", ("XD_Fir1.dff", "XD_Fir2.dff"), ("XD_Fir1.dds", "XD_Fir1Snow.dds"), (), ("i_res_wood.png",)),
    EntitySpec("tree_pine", "Kiefer", "resources", ("XD_Pine*.dff",), ("XD_Pine*.dds",), (), ("i_res_wood.png",)),
    EntitySpec("tree_leaf", "Laubbaum", "resources", ("XD_Tree*.dff",), ("XD_Tree*.dds",), (), ("i_res_wood.png",)),
    EntitySpec("stone_resource", "Steinressource", "resources", ("XD_Stone*.dff",), ("XD_Stone*.dds", "XD_RessourceStone1.dds"), (), ("i_res_stone.png",)),
    EntitySpec("clay_resource", "Lehmressource", "resources", ("XD_Clay*.dff",), ("XD_Clay*.dds", "XD_RessourceClay1.dds"), (), ("i_res_mud.png",)),
    EntitySpec("iron_resource", "Eisenressource", "resources", ("XD_Iron*.dff",), ("XD_Iron*.dds", "XD_RessourceIron1.dds"), (), ("i_res_iron.png",)),
    EntitySpec("sulfur_resource", "Schwefelressource", "resources", ("XD_Sulfur*.dff",), ("XD_Sulfur*.dds", "XD_RessourceSulfur1.dds"), (), ("i_res_sulfur.png",)),
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exportiert Originalgrafik-Report/Previews aus Siedler 5")
    parser.add_argument("--game-root", type=str, default="", help="Pfad zur Gold Edition / The Settlers 5")
    parser.add_argument("--output-dir", type=str, default="analysis/replays/original_graphics_report")
    parser.add_argument("--thumb-size", type=int, default=256)
    return parser.parse_args()


def _candidate_game_roots(explicit: str) -> list[Path]:
    roots: list[Path] = []
    if explicit:
        roots.append(Path(explicit))
    env_root = os.environ.get("SIEDLER_GAME_ROOT") or os.environ.get("SETTLERS5_ROOT")
    if env_root:
        roots.append(Path(env_root))
    roots.extend(
        [
            ROOT_DIR.parent / "Gold edition",
            ROOT_DIR.parent / "The Settlers 5",
            ROOT_DIR.parent / "TheSettlers5",
            Path.home() / "Desktop" / "Gold edition",
            Path.home() / "Desktop" / "The Settlers 5",
            Path.home() / "Desktop" / "TheSettlers5",
        ]
    )
    seen: set[str] = set()
    unique: list[Path] = []
    for root in roots:
        key = str(root).lower()
        if key not in seen:
            seen.add(key)
            unique.append(root)
    return unique


def find_game_root(explicit: str = "") -> Path | None:
    for root in _candidate_game_roots(explicit):
        if (root / "base" / "shr" / "graphics").exists():
            return root
    return None


def _graphics_roots(game_root: Path) -> list[Path]:
    roots: list[Path] = []
    for package in ("base", "extra1", "extra2"):
        pkg_root = game_root / package / "shr" / "graphics"
        if pkg_root.exists():
            roots.append(pkg_root)
    return roots


def _iter_graphics_files(game_root: Path, suffixes: tuple[str, ...]) -> Iterable[Path]:
    suffixes_l = tuple(s.lower() for s in suffixes)
    for root in _graphics_roots(game_root):
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in suffixes_l:
                yield path


def _find_matching(game_root: Path, patterns: tuple[str, ...], suffixes: tuple[str, ...], limit: int = 999) -> list[Path]:
    if not patterns:
        return []
    files = list(_iter_graphics_files(game_root, suffixes))
    out: list[Path] = []
    seen: set[str] = set()
    for pattern in patterns:
        pattern_l = pattern.lower()
        for path in files:
            if path.match(pattern) or path.name.lower() == pattern_l or path.name.lower().startswith(pattern_l.rstrip("*").lower()):
                key = str(path).lower()
                if key not in seen:
                    seen.add(key)
                    out.append(path)
                    if len(out) >= limit:
                        return sorted(out, key=lambda p: p.name.lower())
    return sorted(out, key=lambda p: p.name.lower())


def _rel_to_game(game_root: Path, path: Path) -> str:
    try:
        return path.relative_to(game_root).as_posix()
    except ValueError:
        return path.as_posix()


def _rel_to_output(output_dir: Path, path: Path | None) -> str:
    if path is None or not path.exists():
        return ""
    return path.relative_to(output_dir).as_posix()


def _safe_name(path: Path) -> str:
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in path.stem)


def _make_dds_preview(source: Path, output_dir: Path, thumb_size: int) -> Path | None:
    target = output_dir / "textures" / f"{_safe_name(source)}.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        image = Image.open(source).convert("RGBA")
    except Exception:
        return None
    image.thumbnail((thumb_size, thumb_size), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (thumb_size, thumb_size), (22, 18, 14, 255))
    pos = ((thumb_size - image.width) // 2, (thumb_size - image.height) // 2)
    canvas.alpha_composite(image, pos)
    canvas.convert("RGB").save(target, quality=92)
    return target


def _read_chunks(data: bytes, start: int, end: int, depth: int = 0) -> list[tuple[int, int, int, int, int]]:
    chunks: list[tuple[int, int, int, int, int]] = []
    offset = start
    while offset + 12 <= end:
        chunk_type, size, version = struct.unpack_from("<III", data, offset)
        payload_end = offset + 12 + size
        if size < 0 or payload_end > end:
            break
        chunks.append((depth, offset, chunk_type, size, version))
        if chunk_type in RW_CONTAINER_TYPES and size > 0:
            chunks.extend(_read_chunks(data, offset + 12, payload_end, depth + 1))
        offset = payload_end
    return chunks


def _read_immediate_chunks(data: bytes, start: int, end: int) -> list[tuple[int, int, int, int]]:
    chunks: list[tuple[int, int, int, int]] = []
    offset = start
    while offset + 12 <= end:
        chunk_type, size, version = struct.unpack_from("<III", data, offset)
        payload_end = offset + 12 + size
        if payload_end > end:
            break
        chunks.append((offset, chunk_type, size, version))
        offset = payload_end
    return chunks


def _decode_rw_string(data: bytes, offset: int, size: int) -> str:
    raw = data[offset + 12 : offset + 12 + size].split(b"\x00", 1)[0].strip()
    if not raw:
        return ""
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(encoding).strip()
        except UnicodeDecodeError:
            continue
    return ""


def _extract_material_textures(data: bytes, chunk_offset: int, chunk_size: int) -> list[str]:
    payload_start = chunk_offset + 12
    payload_end = payload_start + chunk_size
    textures: list[str] = []
    for child_offset, child_type, child_size, _version in _read_immediate_chunks(data, payload_start, payload_end):
        if child_type != RW_MATERIAL_LIST:
            continue
        material_list_start = child_offset + 12
        material_list_end = material_list_start + child_size
        for material_offset, material_type, material_size, _material_version in _read_immediate_chunks(
            data, material_list_start, material_list_end
        ):
            if material_type != RW_MATERIAL:
                continue
            material_payload_start = material_offset + 12
            material_payload_end = material_payload_start + material_size
            names: list[str] = []
            for _depth, string_offset, string_type, string_size, _string_version in _read_chunks(
                data, material_payload_start, material_payload_end
            ):
                if string_type == RW_STRING:
                    name = _decode_rw_string(data, string_offset, string_size)
                    if name:
                        names.append(name)
            textures.append(names[0] if names else "")
    return textures


def _extract_geometry(data: bytes, chunk_offset: int, chunk_size: int) -> dict | None:
    struct_offset = chunk_offset + 12
    if struct_offset + 12 > len(data):
        return None
    chunk_type, struct_size, _version = struct.unpack_from("<III", data, struct_offset)
    if chunk_type != RW_STRUCT:
        return None
    payload = data[struct_offset + 12 : struct_offset + 12 + struct_size]
    if len(payload) < 16:
        return None

    flags, num_uv_sets, native_flags = struct.unpack_from("<HBB", payload, 0)
    triangle_count, vertex_count, morph_count = struct.unpack_from("<III", payload, 4)
    offset = 16
    if flags & 0x08:  # prelit colors
        offset += 4 * vertex_count
    uv_sets = num_uv_sets or (2 if flags & 0x80 else (1 if flags & 0x04 else 0))
    uvs: list[tuple[float, float]] = []
    for uv_set in range(uv_sets):
        if offset + 8 * vertex_count > len(payload):
            break
        current_uvs = [
            struct.unpack_from("<ff", payload, offset + index * 8)
            for index in range(vertex_count)
        ]
        if uv_set == 0:
            uvs = current_uvs
        offset += 8 * vertex_count

    triangles: list[tuple[int, int, int]] = []
    triangle_materials: list[int] = []
    for index in range(triangle_count):
        tri_offset = offset + index * 8
        if tri_offset + 8 > len(payload):
            break
        v2, v1, material, v3 = struct.unpack_from("<HHHH", payload, tri_offset)
        if v1 < vertex_count and v2 < vertex_count and v3 < vertex_count:
            triangles.append((v1, v2, v3))
            triangle_materials.append(int(material))
    offset += 8 * triangle_count

    vertices: list[tuple[float, float, float]] = []
    normals: list[tuple[float, float, float]] = []
    if offset + 24 <= len(payload):
        offset += 16  # bounding sphere center/radius
        has_vertices, has_normals = struct.unpack_from("<II", payload, offset)
        offset += 8
        if has_vertices and offset + 12 * vertex_count <= len(payload):
            vertices = [
                struct.unpack_from("<fff", payload, offset + index * 12)
                for index in range(vertex_count)
            ]
            offset += 12 * vertex_count
        if has_normals and offset + 12 * vertex_count <= len(payload):
            normals = [
                struct.unpack_from("<fff", payload, offset + index * 12)
                for index in range(vertex_count)
            ]
            offset += 12 * vertex_count

    return {
        "flags": int(flags),
        "num_uv_sets": int(num_uv_sets),
        "native_flags": int(native_flags),
        "triangles": int(triangle_count),
        "vertices": int(vertex_count),
        "morph_targets": int(morph_count),
        "parsed_triangles": triangles,
        "parsed_triangle_materials": triangle_materials,
        "parsed_vertices": vertices,
        "parsed_normals": normals,
        "parsed_uvs": uvs,
        "material_textures": _extract_material_textures(data, chunk_offset, chunk_size),
    }


def _extract_hanim_hierarchies(data: bytes, chunks: list[tuple[int, int, int, int, int]]) -> list[dict]:
    """Read RenderWare HAnim hierarchy headers and node records from DFF extensions."""
    hierarchies: list[dict] = []
    for _depth, offset, chunk_type, size, _version in chunks:
        if chunk_type != RW_HANIM_PLUGIN or size < 20 or offset + 12 + size > len(data):
            continue
        version, hierarchy_id, node_count, flags, keyframe_size = struct.unpack_from("<IIIII", data, offset + 12)
        node_bytes = int(node_count) * 12
        if node_count <= 0 or 20 + node_bytes > size:
            continue
        nodes = [
            {
                "id": int(node_id),
                "index": int(node_index),
                "flags": int(node_flags),
            }
            for node_id, node_index, node_flags in (
                struct.unpack_from("<III", data, offset + 32 + node_index * 12)
                for node_index in range(int(node_count))
            )
        ]
        hierarchies.append(
            {
                "offset": int(offset),
                "bytes": int(size),
                "version": int(version),
                "hierarchy_id": int(hierarchy_id),
                "node_count": int(node_count),
                "flags": int(flags),
                "keyframe_size": int(keyframe_size),
                "nodes": nodes,
            }
        )
    return hierarchies


def _extract_skin_plugins(data: bytes, chunks: list[tuple[int, int, int, int, int]]) -> list[dict]:
    """Read the unambiguous Skin-plugin header and used-bone table.

    The subsequent inverse-bind matrices and per-vertex weight sections are
    layout-dependent. Keeping their byte offsets explicit makes later skinning
    work auditable without guessing at matrix alignment.
    """
    skins: list[dict] = []
    for _depth, offset, chunk_type, size, _version in chunks:
        if chunk_type != RW_SKIN_PLUGIN or size < 4 or offset + 12 + size > len(data):
            continue
        payload_start = offset + 12
        bone_count, used_bone_count, max_weights, platform = struct.unpack_from("<BBBB", data, payload_start)
        used_start = payload_start + 4
        used_end = min(payload_start + size, used_start + int(used_bone_count))
        used_bones = [int(value) for value in data[used_start:used_end]]
        matrix_offset = (4 + int(used_bone_count) + 3) & ~3
        skins.append(
            {
                "offset": int(offset),
                "bytes": int(size),
                "bone_count": int(bone_count),
                "used_bone_count": int(used_bone_count),
                "max_vertex_weights": int(max_weights),
                "platform": int(platform),
                "used_bones": used_bones,
                "inverse_bind_matrix_offset": int(matrix_offset),
                "inverse_bind_matrix_bytes": int(size - matrix_offset) if matrix_offset <= size else 0,
            }
        )
    return skins


def _extract_frame_list(data: bytes, chunks: list[tuple[int, int, int, int, int]]) -> list[dict]:
    """Read the RenderWare frame list as local bind transforms."""
    frame_chunk = next((chunk for chunk in chunks if chunk[2] == RW_FRAME_LIST), None)
    if frame_chunk is None:
        return []
    payload_start = frame_chunk[1] + 12
    payload_end = payload_start + frame_chunk[3]
    struct_chunk = next(
        (
            chunk
            for chunk in _read_immediate_chunks(data, payload_start, payload_end)
            if chunk[1] == RW_STRUCT
        ),
        None,
    )
    if struct_chunk is None:
        return []
    struct_offset, _chunk_type, struct_size, _version = struct_chunk
    struct_start = struct_offset + 12
    if struct_size < 4 or struct_start + struct_size > len(data):
        return []
    frame_count = int(struct.unpack_from("<I", data, struct_start)[0])
    if frame_count <= 0 or 4 + frame_count * 56 > struct_size:
        return []
    frames: list[dict] = []
    for frame_index in range(frame_count):
        offset = struct_start + 4 + frame_index * 56
        matrix = struct.unpack_from("<12f", data, offset)
        parent, flags = struct.unpack_from("<ii", data, offset + 48)
        frames.append(
            {
                "index": int(frame_index),
                "right": [_round_float(value) for value in matrix[0:3]],
                "up": [_round_float(value) for value in matrix[3:6]],
                "at": [_round_float(value) for value in matrix[6:9]],
                "position": [_round_float(value) for value in matrix[9:12]],
                "parent": int(parent),
                "flags": int(flags),
            }
        )
    return frames


def _extract_frame_hanim_ids(data: bytes, chunks: list[tuple[int, int, int, int, int]]) -> list[int]:
    """Return HAnim IDs in frame-list order (root frame itself has no entry)."""
    ids: list[int] = []
    for _depth, offset, chunk_type, size, _version in chunks:
        if chunk_type != RW_HANIM_PLUGIN or size < 12 or offset + 24 > len(data):
            continue
        _version_value, hierarchy_id, _flags = struct.unpack_from("<III", data, offset + 12)
        ids.append(int(hierarchy_id))
    return ids


def _extract_skinning_payload(
    data: bytes,
    chunks: list[tuple[int, int, int, int, int]],
    vertex_counts: list[int],
) -> list[dict]:
    """Read vertex bone indices, weights, and 4x4 inverse-bind matrices."""
    skin_chunks = [chunk for chunk in chunks if chunk[2] == RW_SKIN_PLUGIN]
    payloads: list[dict] = []
    for geometry_index, chunk in enumerate(skin_chunks):
        if geometry_index >= len(vertex_counts):
            break
        vertex_count = int(vertex_counts[geometry_index])
        payload_start = chunk[1] + 12
        payload_end = payload_start + chunk[3]
        if vertex_count <= 0 or chunk[3] < 4 or payload_end > len(data):
            continue
        raw = data[payload_start:payload_end]
        bone_count, used_bone_count, max_weights, platform = struct.unpack_from("<BBBB", raw, 0)
        indices_start = 4 + int(used_bone_count)
        weights_start = indices_start + vertex_count * 4
        matrices_start = weights_start + vertex_count * 16
        matrices_end = matrices_start + int(bone_count) * 64
        if matrices_end > len(raw):
            continue
        bone_indices = [
            [int(value) for value in raw[indices_start + vertex_index * 4 : indices_start + vertex_index * 4 + 4]]
            for vertex_index in range(vertex_count)
        ]
        weights = [
            [_round_float(value) for value in struct.unpack_from("<4f", raw, weights_start + vertex_index * 16)]
            for vertex_index in range(vertex_count)
        ]
        inverse_bind_matrices = [
            [_round_float(value) for value in struct.unpack_from("<16f", raw, matrices_start + bone_index * 64)]
            for bone_index in range(int(bone_count))
        ]
        payloads.append(
            {
                "geometry_index": int(geometry_index),
                "vertex_count": vertex_count,
                "bone_count": int(bone_count),
                "used_bones": [int(value) for value in raw[4 : 4 + int(used_bone_count)]],
                "max_vertex_weights": int(max_weights),
                "platform": int(platform),
                "bone_indices": bone_indices,
                "weights": weights,
                "inverse_bind_matrices": inverse_bind_matrices,
                "trailing_bytes": int(len(raw) - matrices_end),
            }
        )
    return payloads


def _extract_model_skinning(source: Path, vertex_counts: list[int]) -> dict:
    """Join DFF frame/HAnim/skin data into a renderer-ready source payload."""
    data = source.read_bytes()
    chunks = _read_chunks(data, 0, len(data))
    hierarchies = _extract_hanim_hierarchies(data, chunks)
    frames = _extract_frame_list(data, chunks)
    skins = _extract_skinning_payload(data, chunks, vertex_counts)
    if not hierarchies or not frames or not skins:
        return {}

    hierarchy = hierarchies[0]
    nodes = hierarchy.get("nodes") or []
    node_by_id = {int(node["id"]): node for node in nodes}
    frame_hanim_ids = _extract_frame_hanim_ids(data, chunks)
    frame_to_bone: dict[int, int] = {}
    for frame_index, hierarchy_id in enumerate(frame_hanim_ids, start=1):
        node = node_by_id.get(int(hierarchy_id))
        if node is not None:
            frame_to_bone[frame_index] = int(node["index"])

    bones: list[dict] = []
    for node in sorted(nodes, key=lambda item: int(item["index"])):
        bone_index = int(node["index"])
        frame_index = next((index for index, mapped_bone in frame_to_bone.items() if mapped_bone == bone_index), -1)
        frame = frames[frame_index] if 0 <= frame_index < len(frames) else None
        parent_frame = int(frame["parent"]) if frame else -1
        bones.append(
            {
                "index": bone_index,
                "id": int(node["id"]),
                "flags": int(node["flags"]),
                "frame_index": int(frame_index),
                "parent_index": int(frame_to_bone.get(parent_frame, -1)),
                "bind_local": {
                    "right": (frame or {}).get("right", [1.0, 0.0, 0.0]),
                    "up": (frame or {}).get("up", [0.0, 1.0, 0.0]),
                    "at": (frame or {}).get("at", [0.0, 0.0, 1.0]),
                    "position": (frame or {}).get("position", [0.0, 0.0, 0.0]),
                },
            }
        )
    return {
        "coordinate_system": "renderware_dff_source",
        "node_count": int(hierarchy["node_count"]),
        "keyframe_size": int(hierarchy["keyframe_size"]),
        "bones": bones,
        "geometry_skins": skins,
    }


def _extract_atomics(data: bytes, chunks: list[tuple[int, int, int, int, int]]) -> list[dict]:
    """Map DFF geometry indices to their owning frame indices."""
    atomics: list[dict] = []
    for _depth, offset, chunk_type, size, _version in chunks:
        if chunk_type != RW_ATOMIC:
            continue
        payload_start = offset + 12
        payload_end = payload_start + size
        struct_chunk = next(
            (
                child
                for child in _read_immediate_chunks(data, payload_start, payload_end)
                if child[1] == RW_STRUCT and child[2] >= 16
            ),
            None,
        )
        if struct_chunk is None:
            continue
        struct_offset = struct_chunk[0] + 12
        frame_index, geometry_index, flags, unused = struct.unpack_from("<iiii", data, struct_offset)
        atomics.append(
            {
                "frame_index": int(frame_index),
                "geometry_index": int(geometry_index),
                "flags": int(flags),
                "unused": int(unused),
            }
        )
    return atomics


def _m4_identity() -> list[float]:
    return [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]


def _m4_multiply(a: list[float], b: list[float]) -> list[float]:
    out = [0.0] * 16
    for col in range(4):
        for row in range(4):
            out[col * 4 + row] = sum(a[k * 4 + row] * b[col * 4 + k] for k in range(4))
    return out


def _m4_transform_point(matrix: list[float], vertex: tuple[float, float, float]) -> tuple[float, float, float]:
    x, y, z = vertex
    return (
        matrix[0] * x + matrix[4] * y + matrix[8] * z + matrix[12],
        matrix[1] * x + matrix[5] * y + matrix[9] * z + matrix[13],
        matrix[2] * x + matrix[6] * y + matrix[10] * z + matrix[14],
    )


def _m4_transform_direction(matrix: list[float], normal: tuple[float, float, float]) -> tuple[float, float, float]:
    x, y, z = normal
    return _normalize_vector(
        matrix[0] * x + matrix[4] * y + matrix[8] * z,
        matrix[1] * x + matrix[5] * y + matrix[9] * z,
        matrix[2] * x + matrix[6] * y + matrix[10] * z,
    )


def _frame_matrix(frame: dict) -> list[float]:
    right = frame.get("right") or [1.0, 0.0, 0.0]
    up = frame.get("up") or [0.0, 1.0, 0.0]
    at = frame.get("at") or [0.0, 0.0, 1.0]
    position = frame.get("position") or [0.0, 0.0, 0.0]
    return [
        float(right[0]), float(right[1]), float(right[2]), 0.0,
        float(up[0]), float(up[1]), float(up[2]), 0.0,
        float(at[0]), float(at[1]), float(at[2]), 0.0,
        float(position[0]), float(position[1]), float(position[2]), 1.0,
    ]


def _extract_object_frame_payload(source: Path) -> dict:
    """Build bind and HAnim metadata for rigid DFF atomic meshes."""
    data = source.read_bytes()
    chunks = _read_chunks(data, 0, len(data))
    frames = _extract_frame_list(data, chunks)
    atomics = _extract_atomics(data, chunks)
    if not frames or not atomics:
        return {}
    hierarchies = _extract_hanim_hierarchies(data, chunks)
    hierarchy = hierarchies[0] if hierarchies else {}
    nodes = hierarchy.get("nodes") or []
    node_by_id = {int(node["id"]): node for node in nodes}
    frame_to_bone: dict[int, int] = {}
    for frame_index, hierarchy_id in enumerate(_extract_frame_hanim_ids(data, chunks), start=1):
        node = node_by_id.get(int(hierarchy_id))
        if node is not None:
            frame_to_bone[frame_index] = int(node["index"])
    world_matrices: list[list[float] | None] = [None] * len(frames)

    def resolve(frame_index: int) -> list[float]:
        if not 0 <= frame_index < len(frames):
            return _m4_identity()
        cached = world_matrices[frame_index]
        if cached is not None:
            return cached
        frame = frames[frame_index]
        local = _frame_matrix(frame)
        parent = int(frame.get("parent", -1))
        world = _m4_multiply(resolve(parent), local) if parent >= 0 else local
        world_matrices[frame_index] = world
        return world

    bindings = []
    for atomic in atomics:
        frame_index = int(atomic["frame_index"])
        bindings.append(
            {
                **atomic,
                "bone_index": int(frame_to_bone.get(frame_index, -1)),
                "bind_world": [_round_float(value) for value in resolve(frame_index)],
            }
        )
    bones: list[dict] = []
    for node in sorted(nodes, key=lambda item: int(item["index"])):
        bone_index = int(node["index"])
        frame_index = next((index for index, mapped_bone in frame_to_bone.items() if mapped_bone == bone_index), -1)
        frame = frames[frame_index] if 0 <= frame_index < len(frames) else None
        parent_frame = int(frame["parent"]) if frame else -1
        bones.append(
            {
                "index": bone_index,
                "id": int(node["id"]),
                "frame_index": int(frame_index),
                "parent_index": int(frame_to_bone.get(parent_frame, -1)),
                "bind_local": {
                    "right": (frame or {}).get("right", [1.0, 0.0, 0.0]),
                    "up": (frame or {}).get("up", [0.0, 1.0, 0.0]),
                    "at": (frame or {}).get("at", [0.0, 0.0, 1.0]),
                    "position": (frame or {}).get("position", [0.0, 0.0, 0.0]),
                },
            }
        )
    return {
        "coordinate_system": "renderware_dff_source",
        "frame_count": len(frames),
        "atomic_bindings": bindings,
        "animation_skeleton": {
            "node_count": int(hierarchy.get("node_count") or 0),
            "bones": bones,
        },
    }


def inspect_dff(path: Path) -> dict:
    data = path.read_bytes()
    chunks = _read_chunks(data, 0, len(data))
    root = chunks[0] if chunks else None
    geometries: list[dict] = []
    for _depth, offset, chunk_type, size, _version in chunks:
        if chunk_type == RW_GEOMETRY:
            geometry = _extract_geometry(data, offset, size)
            if geometry:
                vertices = geometry.get("parsed_vertices") or []
                if vertices:
                    bounds = []
                    for axis in range(3):
                        values = [float(v[axis]) for v in vertices]
                        bounds.append([round(min(values), 3), round(max(values), 3)])
                    geometry["bounds"] = bounds
                geometry.pop("parsed_triangles", None)
                geometry.pop("parsed_triangle_materials", None)
                geometry.pop("parsed_vertices", None)
                geometry.pop("parsed_normals", None)
                geometry.pop("parsed_uvs", None)
                geometries.append(geometry)
    return {
        "bytes": path.stat().st_size,
        "root_chunk_type": int(root[2]) if root else None,
        "rw_version": f"0x{root[4]:08x}" if root else "",
        "chunk_count": len(chunks),
        "geometry_count": len(geometries),
        "geometries": geometries,
        "hanim_hierarchies": _extract_hanim_hierarchies(data, chunks),
        "skin_plugins": _extract_skin_plugins(data, chunks),
    }


def _animation_role(path: Path) -> str:
    name = path.stem.lower()
    if "walk" in name:
        return "walk"
    if "run" in name:
        return "run"
    if "work" in name or "conveyor" in name or "pit_" in name or "door" in name:
        return "work"
    if "idle" in name:
        return "idle"
    if "ladder" in name:
        return "ladder"
    if "dying" in name or "death" in name:
        return "death"
    if "hit" in name:
        return "hit"
    if "attack" in name:
        return "attack"
    return "other"


def _decode_anm_tracks(data: bytes, keyframes: int, keyframe_bytes: int, node_count: int) -> dict:
    """Reconstruct RenderWare keyframe ownership from its prev-frame offsets.

    Settlers 5 ANMs start with one keyframe per HAnim node. Every later
    keyframe stores the byte offset of its predecessor, so following that
    offset assigns it to the same bone track even when different bones use
    different sampling times.
    """
    if node_count <= 0 or keyframe_bytes < 36 or keyframes < node_count:
        return {"parsed": False, "reason": "missing compatible HAnim node count", "tracks": []}

    owners: list[int | None] = []
    track_counts = [0] * node_count
    tracks: list[list[list[float]]] = [[] for _ in range(node_count)]
    linked = 0
    unresolved = 0
    last_times = [-float("inf")] * node_count
    monotonic_violations = 0
    max_time = 0.0
    for keyframe_index in range(keyframes):
        offset = 32 + keyframe_index * keyframe_bytes
        if offset + 36 > len(data):
            unresolved += 1
            owners.append(None)
            continue
        time = float(struct.unpack_from("<f", data, offset)[0])
        previous_offset = int(struct.unpack_from("<I", data, offset + 32)[0])
        owner: int | None
        if keyframe_index < node_count:
            owner = keyframe_index
        elif previous_offset % keyframe_bytes == 0 and 0 <= previous_offset // keyframe_bytes < keyframe_index:
            owner = owners[previous_offset // keyframe_bytes]
            linked += 1
        else:
            owner = None
            unresolved += 1
        owners.append(owner)
        if owner is None or owner < 0 or owner >= node_count:
            continue
        if time + 1e-6 < last_times[owner]:
            monotonic_violations += 1
        last_times[owner] = max(last_times[owner], time)
        max_time = max(max_time, time)
        track_counts[owner] += 1
        quaternion = struct.unpack_from("<4f", data, offset + 4)
        translation = struct.unpack_from("<3f", data, offset + 20)
        tracks[owner].append(
            [
                _round_float(time),
                *[_round_float(value) for value in quaternion],
                *[_round_float(value) for value in translation],
            ]
        )

    return {
        "parsed": True,
        "node_count": int(node_count),
        "track_count": int(sum(1 for count in track_counts if count > 0)),
        "track_keyframes_min": int(min(track_counts) if track_counts else 0),
        "track_keyframes_max": int(max(track_counts) if track_counts else 0),
        "linked_keyframes": int(linked),
        "unresolved_keyframes": int(unresolved),
        "monotonic_time_violations": int(monotonic_violations),
        "max_keyframe_time": round(float(max_time), 6),
        "tracks": tracks,
    }


def _analyze_anm_tracks(data: bytes, keyframes: int, keyframe_bytes: int, node_count: int, duration: float) -> dict:
    decoded = _decode_anm_tracks(data, keyframes, keyframe_bytes, node_count)
    if not decoded.get("parsed"):
        return {"parsed": False, "reason": decoded.get("reason", "track decode failed")}
    return {
        "parsed": True,
        "node_count": int(decoded["node_count"]),
        "track_count": int(decoded["track_count"]),
        "track_keyframes_min": int(decoded["track_keyframes_min"]),
        "track_keyframes_max": int(decoded["track_keyframes_max"]),
        "linked_keyframes": int(decoded["linked_keyframes"]),
        "unresolved_keyframes": int(decoded["unresolved_keyframes"]),
        "monotonic_time_violations": int(decoded["monotonic_time_violations"]),
        "max_keyframe_time": float(decoded["max_keyframe_time"]),
        "duration_delta": round(abs(float(duration) - float(decoded["max_keyframe_time"])), 6),
    }


def inspect_anm(path: Path, expected_node_count: int = 0) -> dict:
    """Parse the RenderWare ANM chunk header.

    Settlers 5 animation files are RenderWare chunk type 0x1b. The first
    20 payload bytes are enough to identify interpolation id, keyframe count
    and original animation duration. Full skinning still needs the matching
    HAnim hierarchy/skin data from the model.
    """
    data = path.read_bytes()
    chunks = _read_chunks(data, 0, len(data))
    root = chunks[0] if chunks else None
    info: dict = {
        "bytes": path.stat().st_size,
        "root_chunk_type": int(root[2]) if root else None,
        "rw_version": f"0x{root[4]:08x}" if root else "",
        "chunk_count": len(chunks),
        "role": _animation_role(path),
        "parsed": False,
    }
    if not root or root[2] != RW_ANIMATION or root[3] < 20 or len(data) < 32:
        return info

    version, interp_id, keyframes, flags, duration = struct.unpack_from("<IIIIf", data, 12)
    payload_bytes = int(root[3])
    keyframe_bytes = 0
    if keyframes > 0:
        remaining = payload_bytes - 20
        keyframe_bytes = int(remaining // keyframes) if remaining >= 0 and remaining % keyframes == 0 else 0

    info.update(
        {
            "parsed": True,
            "anim_version": int(version),
            "interp_id": int(interp_id),
            "keyframes": int(keyframes),
            "flags": int(flags),
            "duration": round(float(duration), 6),
            "keyframe_bytes": keyframe_bytes,
        }
    )
    if expected_node_count > 0:
        info["track_topology"] = _analyze_anm_tracks(
            data,
            int(keyframes),
            int(keyframe_bytes),
            int(expected_node_count),
            float(duration),
        )
    return info


def _make_anm_track_json(source: Path, output_dir: Path, node_count: int) -> Path | None:
    """Export decoded original HAnim tracks in a compact, browser-loadable JSON file."""
    info = inspect_anm(source, node_count)
    topology = info.get("track_topology") or {}
    if not info.get("parsed") or not topology.get("parsed"):
        return None
    data = source.read_bytes()
    decoded = _decode_anm_tracks(
        data,
        int(info["keyframes"]),
        int(info["keyframe_bytes"]),
        int(node_count),
    )
    if not decoded.get("parsed"):
        return None
    target = output_dir / "animations" / f"{_safe_name(source)}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": source.name,
        "format": "s5_rwanim_hanim_tracks_v1",
        "role": _animation_role(source),
        "duration": float(info["duration"]),
        "node_count": int(node_count),
        "keyframe_bytes": int(info["keyframe_bytes"]),
        "keyframe_layout": ["time", "qx", "qy", "qz", "qw", "tx", "ty", "tz"],
        "track_topology": {
            key: value
            for key, value in decoded.items()
            if key != "tracks"
        },
        "tracks": decoded["tracks"],
    }
    target.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return target


def _collect_meshes(path: Path) -> list[dict]:
    data = path.read_bytes()
    meshes: list[dict] = []
    for _depth, offset, chunk_type, size, _version in _read_chunks(data, 0, len(data)):
        if chunk_type == RW_GEOMETRY:
            geometry = _extract_geometry(data, offset, size)
            if geometry and geometry.get("parsed_vertices") and geometry.get("parsed_triangles"):
                meshes.append(geometry)
    return meshes


def _project_vertex(vertex: tuple[float, float, float]) -> tuple[float, float]:
    x, y, z = vertex
    return (x - y) * 0.72, (x + y) * 0.38 - z * 0.92


def _make_mesh_preview(source: Path, output_dir: Path, thumb_size: int) -> Path | None:
    try:
        meshes = _collect_meshes(source)
    except Exception:
        return None
    vertices_2d: list[tuple[float, float]] = []
    for mesh in meshes:
        vertices_2d.extend(_project_vertex(v) for v in mesh.get("parsed_vertices", []))
    if not vertices_2d:
        return None

    min_x = min(p[0] for p in vertices_2d)
    max_x = max(p[0] for p in vertices_2d)
    min_y = min(p[1] for p in vertices_2d)
    max_y = max(p[1] for p in vertices_2d)
    span_x = max(1.0, max_x - min_x)
    span_y = max(1.0, max_y - min_y)
    margin = thumb_size * 0.08
    scale = min((thumb_size - margin * 2) / span_x, (thumb_size - margin * 2) / span_y)

    def transform(point: tuple[float, float]) -> tuple[float, float]:
        px = margin + (point[0] - min_x) * scale
        py = margin + (point[1] - min_y) * scale
        return px, py

    canvas = Image.new("RGBA", (thumb_size, thumb_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas, "RGBA")
    colors = [
        (185, 156, 99, 66),
        (110, 151, 118, 58),
        (108, 136, 162, 52),
        (172, 123, 103, 54),
    ]
    line = (238, 218, 171, 90)
    for mesh_index, mesh in enumerate(meshes):
        vertices = mesh.get("parsed_vertices", [])
        projected = [transform(_project_vertex(v)) for v in vertices]
        fill = colors[mesh_index % len(colors)]
        triangles = mesh.get("parsed_triangles", [])
        max_triangles = 7500
        step = max(1, math.ceil(len(triangles) / max_triangles))
        for v1, v2, v3 in triangles[::step]:
            try:
                points = [projected[v1], projected[v2], projected[v3]]
            except IndexError:
                continue
            draw.polygon(points, fill=fill)
            draw.line([points[0], points[1], points[2], points[0]], fill=line, width=1)

    target = output_dir / "meshes" / f"{_safe_name(source)}.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(target)
    return target


def _texture_index(game_root: Path) -> dict[str, Path]:
    cache_key = str(game_root.resolve()).lower()
    cached = _TEXTURE_INDEX_CACHE.get(cache_key)
    if cached is not None:
        return cached

    index: dict[str, Path] = {}
    for package in ("base", "extra1", "extra2"):
        graphics_root = game_root / package / "shr" / "graphics"
        if not graphics_root.exists():
            continue
        for suffix in ("*.dds", "*.png"):
            for path in graphics_root.rglob(suffix):
                path_key = path.name.lower()
                stem_key = path.stem.lower()
                index.setdefault(path_key, path)
                index.setdefault(stem_key, path)
    _TEXTURE_INDEX_CACHE[cache_key] = index
    return index


def _find_texture_by_name(game_root: Path, texture_name: str) -> Path | None:
    clean = str(texture_name or "").replace("\\", "/").rsplit("/", 1)[-1].strip()
    if not clean:
        return None
    index = _texture_index(game_root)
    candidates = [clean.lower(), Path(clean).stem.lower()]
    for candidate in candidates:
        path = index.get(candidate)
        if path is not None and path.exists():
            return path
    return None


def _load_texture_image(path: Path | None) -> Image.Image | None:
    if path is None:
        return None
    cache_key = str(path.resolve()).lower()
    if cache_key in _TEXTURE_IMAGE_CACHE:
        return _TEXTURE_IMAGE_CACHE[cache_key]
    try:
        image = Image.open(path).convert("RGBA")
    except Exception:
        image = None
    _TEXTURE_IMAGE_CACHE[cache_key] = image
    return image


def _fallback_material_color(material_index: int) -> tuple[int, int, int, int]:
    colors = (
        (156, 126, 82, 235),
        (104, 137, 92, 235),
        (133, 137, 146, 235),
        (118, 89, 64, 235),
        (92, 108, 124, 235),
    )
    return colors[int(material_index) % len(colors)]


def _texture_sample(texture: Image.Image | None, uv_values: list[tuple[float, float]], fallback: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    if texture is None or not uv_values:
        return fallback
    width, height = texture.size
    if width <= 0 or height <= 0:
        return fallback
    centroid = (
        sum(float(uv[0]) for uv in uv_values) / len(uv_values),
        sum(float(uv[1]) for uv in uv_values) / len(uv_values),
    )
    candidates = [centroid, *uv_values]
    for flip_v in (True, False):
        for u, v in candidates:
            uu = float(u) % 1.0
            vv = float(v) % 1.0
            if flip_v:
                vv = 1.0 - vv
            x = max(0, min(width - 1, int(round(uu * (width - 1)))))
            y = max(0, min(height - 1, int(round(vv * (height - 1)))))
            color = texture.getpixel((x, y))
            if len(color) == 3:
                return int(color[0]), int(color[1]), int(color[2]), 235
            if int(color[3]) > 12:
                return int(color[0]), int(color[1]), int(color[2]), min(245, max(120, int(color[3])))
    return fallback


def _polygon_area(points: list[tuple[float, float]]) -> float:
    return abs(
        points[0][0] * (points[1][1] - points[2][1])
        + points[1][0] * (points[2][1] - points[0][1])
        + points[2][0] * (points[0][1] - points[1][1])
    ) * 0.5


def _affine_coefficients(
    dst_points: list[tuple[float, float]],
    src_points: list[tuple[float, float]],
) -> tuple[float, float, float, float, float, float] | None:
    (x0, y0), (x1, y1), (x2, y2) = dst_points
    (u0, v0), (u1, v1), (u2, v2) = src_points
    det = x0 * (y1 - y2) + x1 * (y2 - y0) + x2 * (y0 - y1)
    if abs(det) < 1e-6:
        return None

    def solve(a0: float, a1: float, a2: float) -> tuple[float, float, float]:
        a = (a0 * (y1 - y2) + a1 * (y2 - y0) + a2 * (y0 - y1)) / det
        b = (a0 * (x2 - x1) + a1 * (x0 - x2) + a2 * (x1 - x0)) / det
        c = (
            a0 * (x1 * y2 - x2 * y1)
            + a1 * (x2 * y0 - x0 * y2)
            + a2 * (x0 * y1 - x1 * y0)
        ) / det
        return a, b, c

    a, b, c = solve(u0, u1, u2)
    d, e, f = solve(v0, v1, v2)
    return a, b, c, d, e, f


def _uv_to_texture_points(texture: Image.Image, uv_values: list[tuple[float, float]]) -> list[tuple[float, float]]:
    width, height = texture.size
    points: list[tuple[float, float]] = []
    for u, v in uv_values:
        uu = float(u) % 1.0
        vv = 1.0 - (float(v) % 1.0)
        points.append((uu * max(1, width - 1), vv * max(1, height - 1)))
    return points


def _draw_textured_triangle(
    canvas: Image.Image,
    texture: Image.Image,
    points: list[tuple[float, float]],
    uv_values: list[tuple[float, float]],
) -> bool:
    if len(points) != 3 or len(uv_values) != 3 or texture.width <= 0 or texture.height <= 0:
        return False
    min_x = max(0, int(math.floor(min(point[0] for point in points))))
    max_x = min(canvas.width, int(math.ceil(max(point[0] for point in points))) + 1)
    min_y = max(0, int(math.floor(min(point[1] for point in points))))
    max_y = min(canvas.height, int(math.ceil(max(point[1] for point in points))) + 1)
    if max_x <= min_x or max_y <= min_y:
        return False

    local_points = [(point[0] - min_x, point[1] - min_y) for point in points]
    tex_points = _uv_to_texture_points(texture, uv_values)
    coeffs = _affine_coefficients(local_points, tex_points)
    if coeffs is None:
        return False

    width = max_x - min_x
    height = max_y - min_y
    try:
        patch = texture.transform(
            (width, height),
            Image.Transform.AFFINE,
            coeffs,
            resample=Image.Resampling.BILINEAR,
        ).convert("RGBA")
    except Exception:
        return False

    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).polygon(local_points, fill=255)
    alpha = ImageChops.multiply(patch.getchannel("A"), mask)
    patch.putalpha(alpha)
    canvas.alpha_composite(patch, (min_x, min_y))
    return True


def _make_textured_sprite(source: Path, game_root: Path, output_dir: Path, thumb_size: int) -> Path | None:
    try:
        meshes = _collect_meshes(source)
    except Exception:
        return None

    vertices_2d: list[tuple[float, float]] = []
    for mesh in meshes:
        vertices_2d.extend(_project_vertex(v) for v in mesh.get("parsed_vertices", []))
    if not vertices_2d:
        return None

    min_x = min(p[0] for p in vertices_2d)
    max_x = max(p[0] for p in vertices_2d)
    min_y = min(p[1] for p in vertices_2d)
    max_y = max(p[1] for p in vertices_2d)
    span_x = max(1.0, max_x - min_x)
    span_y = max(1.0, max_y - min_y)
    margin = thumb_size * 0.07
    scale = min((thumb_size - margin * 2) / span_x, (thumb_size - margin * 2) / span_y)

    def transform(point: tuple[float, float]) -> tuple[float, float]:
        px = margin + (point[0] - min_x) * scale
        py = margin + (point[1] - min_y) * scale
        return px, py

    canvas = Image.new("RGBA", (thumb_size, thumb_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas, "RGBA")
    shadow_w = thumb_size * min(0.82, max(0.26, span_x / max(span_y, 1.0) * 0.36))
    shadow_h = thumb_size * 0.11
    shadow_y = thumb_size * 0.82
    draw.ellipse(
        (
            (thumb_size - shadow_w) / 2,
            shadow_y - shadow_h / 2,
            (thumb_size + shadow_w) / 2,
            shadow_y + shadow_h / 2,
        ),
        fill=(0, 0, 0, 42),
    )

    draw_items: list[
        tuple[
            float,
            list[tuple[float, float]],
            Image.Image | None,
            list[tuple[float, float]],
            tuple[int, int, int, int],
        ]
    ] = []
    fallback_texture = _load_texture_image(_find_texture_by_name(game_root, source.stem))
    for mesh_index, mesh in enumerate(meshes):
        vertices = mesh.get("parsed_vertices", [])
        triangles = mesh.get("parsed_triangles", [])
        triangle_materials = mesh.get("parsed_triangle_materials", [])
        uvs = mesh.get("parsed_uvs", [])
        projected = [transform(_project_vertex(v)) for v in vertices]
        material_textures = mesh.get("material_textures") or []
        material_images = [_load_texture_image(_find_texture_by_name(game_root, str(name))) for name in material_textures]

        max_triangles = 12000
        step = max(1, math.ceil(len(triangles) / max_triangles))
        for original_index in range(0, len(triangles), step):
            v1, v2, v3 = triangles[original_index]
            try:
                points = [projected[v1], projected[v2], projected[v3]]
            except IndexError:
                continue
            if _polygon_area(points) < 0.08:
                continue
            material_index = triangle_materials[original_index] if original_index < len(triangle_materials) else 0
            texture = material_images[material_index] if 0 <= material_index < len(material_images) else fallback_texture
            uv_values = [uvs[v1], uvs[v2], uvs[v3]] if max(v1, v2, v3) < len(uvs) else []
            color = _texture_sample(texture, uv_values, _fallback_material_color(material_index + mesh_index))
            depth = (points[0][1] + points[1][1] + points[2][1]) / 3.0 + mesh_index * 0.001
            draw_items.append((depth, points, texture, uv_values, color))

    for _depth, points, texture, uv_values, color in sorted(draw_items, key=lambda item: item[0]):
        if texture is None or not uv_values or not _draw_textured_triangle(canvas, texture, points, uv_values):
            draw.polygon(points, fill=color)

    target = output_dir / "sprites" / f"{_safe_name(source)}.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(target)
    return target


def _convert_texture_for_web(source: Path | None, output_dir: Path, max_size: int = 1024) -> Path | None:
    if source is None:
        return None
    target = output_dir / "textures_web" / f"{_safe_name(source)}.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_mtime >= source.stat().st_mtime:
        return target
    try:
        image = Image.open(source).convert("RGBA")
    except Exception:
        return None
    if max(image.size) > max_size:
        image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    image.save(target)
    return target


def _round_float(value: float) -> float:
    return round(float(value), 5)


def _normalize_vector(x: float, y: float, z: float) -> tuple[float, float, float]:
    length = math.sqrt(x * x + y * y + z * z)
    if length <= 1e-8:
        return 0.0, 1.0, 0.0
    return x / length, y / length, z / length


def _make_model3d_json(source: Path, game_root: Path, output_dir: Path) -> Path | None:
    try:
        meshes = _collect_meshes(source)
    except Exception:
        return None
    if not meshes:
        return None

    dff_info = inspect_dff(source)
    skeleton = {
        "hanim_hierarchies": dff_info.get("hanim_hierarchies") or [],
        "skin_plugins": dff_info.get("skin_plugins") or [],
    }
    skinning = _extract_model_skinning(source, [len(mesh.get("parsed_vertices", [])) for mesh in meshes])
    object_frames = _extract_object_frame_payload(source)
    atomic_bindings = {
        int(binding["geometry_index"]): binding
        for binding in (object_frames.get("atomic_bindings") or [])
    }
    export_meshes: list[dict] = []
    for mesh_index, mesh in enumerate(meshes):
        transformed = dict(mesh)
        binding = atomic_bindings.get(mesh_index)
        bind_world = binding.get("bind_world") if binding and not skinning else None
        if bind_world:
            transformed["parsed_vertices"] = [
                _m4_transform_point(bind_world, vertex)
                for vertex in (mesh.get("parsed_vertices") or [])
            ]
            transformed["parsed_normals"] = [
                _m4_transform_direction(bind_world, normal)
                for normal in (mesh.get("parsed_normals") or [])
            ]
        export_meshes.append(transformed)

    all_vertices = [vertex for mesh in export_meshes for vertex in mesh.get("parsed_vertices", [])]
    if not all_vertices:
        return None

    min_x = min(float(v[0]) for v in all_vertices)
    max_x = max(float(v[0]) for v in all_vertices)
    min_y = min(float(v[1]) for v in all_vertices)
    max_y = max(float(v[1]) for v in all_vertices)
    min_z = min(float(v[2]) for v in all_vertices)
    max_z = max(float(v[2]) for v in all_vertices)
    center_x = (min_x + max_x) / 2.0
    center_y = (min_y + max_y) / 2.0
    span_x = max(1.0, max_x - min_x)
    span_y = max(1.0, max_y - min_y)
    span_z = max(1.0, max_z - min_z)

    positions: list[float] = []
    normals: list[float] = []
    uvs: list[float] = []
    source_positions: list[float] = []
    source_normals: list[float] = []
    geometry_ranges: list[dict] = []
    submesh_map: dict[tuple[int, int, str], dict] = {}
    vertex_offset = 0
    for mesh_index, mesh in enumerate(export_meshes):
        vertices = mesh.get("parsed_vertices", [])
        mesh_normals = mesh.get("parsed_normals", [])
        raw_mesh = meshes[mesh_index] if mesh_index < len(meshes) else mesh
        raw_vertices = raw_mesh.get("parsed_vertices", [])
        raw_normals = raw_mesh.get("parsed_normals", [])
        mesh_uvs = mesh.get("parsed_uvs", [])
        triangles = mesh.get("parsed_triangles", [])
        triangle_materials = mesh.get("parsed_triangle_materials", [])
        material_textures = [str(name or "") for name in (mesh.get("material_textures") or [])]

        for vertex_index, vertex in enumerate(vertices):
            # WebGL scene is Y-up. The original DFF local X/Y plane becomes X/Z, original Z becomes height.
            raw_vertex = raw_vertices[vertex_index] if vertex_index < len(raw_vertices) else vertex
            source_positions.extend(
                [
                    _round_float(float(raw_vertex[0])),
                    _round_float(float(raw_vertex[1])),
                    _round_float(float(raw_vertex[2])),
                ]
            )
            positions.extend(
                [
                    _round_float(float(vertex[0]) - center_x),
                    _round_float(float(vertex[2]) - min_z),
                    _round_float(-(float(vertex[1]) - center_y)),
                ]
            )
            if vertex_index < len(mesh_normals):
                normal = mesh_normals[vertex_index]
                raw_normal = raw_normals[vertex_index] if vertex_index < len(raw_normals) else normal
                source_normals.extend(
                    [
                        _round_float(float(raw_normal[0])),
                        _round_float(float(raw_normal[1])),
                        _round_float(float(raw_normal[2])),
                    ]
                )
                nx, ny, nz = _normalize_vector(float(normal[0]), float(normal[2]), -float(normal[1]))
                normals.extend([_round_float(nx), _round_float(ny), _round_float(nz)])
            else:
                source_normals.extend([0.0, 0.0, 1.0])
                normals.extend([0.0, 1.0, 0.0])
            if vertex_index < len(mesh_uvs):
                u, v = mesh_uvs[vertex_index]
                uvs.extend([_round_float(float(u) % 1.0), _round_float(1.0 - (float(v) % 1.0))])
            else:
                uvs.extend([0.0, 0.0])

        for triangle_index, (v1, v2, v3) in enumerate(triangles):
            material_index = triangle_materials[triangle_index] if triangle_index < len(triangle_materials) else 0
            texture_name = material_textures[material_index] if 0 <= material_index < len(material_textures) else source.stem
            key = (mesh_index, int(material_index), texture_name or source.stem)
            if key not in submesh_map:
                texture_source = _find_texture_by_name(game_root, texture_name or source.stem)
                texture_png = _convert_texture_for_web(texture_source, output_dir)
                submesh_map[key] = {
                    "name": f"mesh{mesh_index}_mat{int(material_index)}",
                    "material_index": int(material_index),
                    "texture_name": texture_name or source.stem,
                    "texture": _rel_to_output(output_dir, texture_png),
                    "indices": [],
                }
            submesh_map[key]["indices"].extend([vertex_offset + int(v1), vertex_offset + int(v2), vertex_offset + int(v3)])

        binding = atomic_bindings.get(mesh_index)
        geometry_ranges.append(
            {
                "geometry_index": int(mesh_index),
                "vertex_offset": int(vertex_offset),
                "vertex_count": int(len(vertices)),
                "bone_index": int((binding or {}).get("bone_index", -1)),
            }
        )
        vertex_offset += len(vertices)

    if object_frames:
        object_frames["geometry_ranges"] = geometry_ranges

    target = output_dir / "models3d" / f"{_safe_name(source)}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": source.name,
        "format": "s5_dff_atomic_bind_and_rigid_animation_metadata_v1",
        "positions": positions,
        "normals": normals,
        "uvs": uvs,
        "source_positions": source_positions,
        "source_normals": source_normals,
        "submeshes": list(submesh_map.values()),
        "bounds": {
            "min": [_round_float(min_x), _round_float(min_y), _round_float(min_z)],
            "max": [_round_float(max_x), _round_float(max_y), _round_float(max_z)],
            "span": [_round_float(span_x), _round_float(span_y), _round_float(span_z)],
            "max_span": _round_float(max(span_x, span_y, span_z)),
        },
        "skeleton": skeleton,
        "skinning": skinning,
        "object_frames": object_frames,
        "notes": "DFF geometry is converted with Atomic bind transforms, HAnim metadata, Skin data, and rigid-atomic frame mappings for the local WebGL replay renderer.",
    }
    target.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return target


def _file_entries(game_root: Path, paths: list[Path]) -> list[dict]:
    return [{"name": path.name, "path": _rel_to_game(game_root, path), "bytes": path.stat().st_size} for path in paths]


def _animation_file_entries(
    game_root: Path,
    paths: list[Path],
    expected_node_count: int = 0,
    output_dir: Path | None = None,
    model_stem: str = "",
) -> list[dict]:
    records: list[tuple[Path, dict]] = []
    for path in paths:
        entry = {"name": path.name, "path": _rel_to_game(game_root, path), "bytes": path.stat().st_size}
        try:
            entry["role"] = _animation_role(path)
            entry["anm"] = inspect_anm(path, expected_node_count)
        except Exception as exc:
            entry["role"] = _animation_role(path)
            entry["anm"] = {"parsed": False, "error": str(exc)}
        records.append((path, entry))

    if output_dir is not None and expected_node_count > 0:
        for role in ("idle", "walk", "run", "work"):
            candidates = [
                record
                for record in records
                if record[1].get("role") == role
                and (record[1].get("anm") or {}).get("parsed")
                and ((record[1].get("anm") or {}).get("track_topology") or {}).get("parsed")
            ]
            if not candidates:
                continue
            exact_model_candidates = [
                record
                for record in candidates
                if model_stem and record[0].stem.lower().startswith(f"{model_stem.lower()}_")
            ]
            if exact_model_candidates:
                candidates = exact_model_candidates
            source, entry = max(
                candidates,
                key=lambda record: (
                    int((record[1].get("anm") or {}).get("keyframes", 0)),
                    str(record[0].name).lower(),
                ),
            )
            track_data = _make_anm_track_json(source, output_dir, expected_node_count)
            if track_data is not None:
                entry["track_data"] = _rel_to_output(output_dir, track_data)
    return [entry for _path, entry in records]


def _animation_summary(entries: list[dict]) -> dict:
    by_role: dict[str, dict] = {}
    parsed = 0
    for entry in entries:
        role = str(entry.get("role") or "other")
        anm = entry.get("anm") or {}
        if not anm.get("parsed"):
            continue
        parsed += 1
        duration = float(anm.get("duration") or 0.0)
        keyframes = int(anm.get("keyframes") or 0)
        current = by_role.get(role)
        if current is None:
            by_role[role] = {
                "count": 1,
                "min_duration": round(duration, 6),
                "max_duration": round(duration, 6),
                "max_keyframes": keyframes,
                "sample": entry.get("name", ""),
            }
            continue
        current["count"] = int(current.get("count", 0)) + 1
        current["min_duration"] = round(min(float(current.get("min_duration", duration)), duration), 6)
        current["max_duration"] = round(max(float(current.get("max_duration", duration)), duration), 6)
        current["max_keyframes"] = max(int(current.get("max_keyframes", 0)), keyframes)
    return {"files": len(entries), "parsed": parsed, "by_role": by_role}


def _mapped_asset_paths(entities: list[dict]) -> set[str]:
    mapped: set[str] = set()
    for entity in entities:
        for key in ("model_files", "texture_files", "animation_files", "gui_files"):
            for item in entity.get(key) or []:
                path = str(item.get("path") or "").replace("\\", "/").lower()
                if path:
                    mapped.add(path)
    return mapped


def _write_asset_inventory(game_root: Path, output_dir: Path, entities: list[dict]) -> dict:
    mapped_paths = _mapped_asset_paths(entities)
    suffixes = (".dff", ".anm", ".dds", ".png")
    files: list[dict] = []
    by_extension: dict[str, dict] = {}
    unmapped_samples: dict[str, list[dict]] = {}

    for path in sorted(_iter_graphics_files(game_root, suffixes), key=lambda item: _rel_to_game(game_root, item).lower()):
        rel = _rel_to_game(game_root, path)
        rel_key = rel.lower()
        ext = path.suffix.lower().lstrip(".")
        mapped = rel_key in mapped_paths
        size = int(path.stat().st_size)
        entry = {
            "name": path.name,
            "path": rel,
            "extension": ext,
            "stem": path.stem,
            "bytes": size,
            "mapped_to_replay": mapped,
        }
        files.append(entry)

        ext_summary = by_extension.setdefault(ext, {"files": 0, "mapped": 0, "unmapped": 0, "bytes": 0})
        ext_summary["files"] = int(ext_summary["files"]) + 1
        ext_summary["bytes"] = int(ext_summary["bytes"]) + size
        if mapped:
            ext_summary["mapped"] = int(ext_summary["mapped"]) + 1
        else:
            ext_summary["unmapped"] = int(ext_summary["unmapped"]) + 1
            samples = unmapped_samples.setdefault(ext, [])
            if len(samples) < 60:
                samples.append({"name": path.name, "path": rel, "bytes": size})

    mapped_count = sum(1 for item in files if item["mapped_to_replay"])
    summary = {
        "total_files": len(files),
        "mapped_files": mapped_count,
        "unmapped_files": len(files) - mapped_count,
        "bytes": sum(int(item["bytes"]) for item in files),
        "by_extension": dict(sorted(by_extension.items())),
        "unmapped_samples": dict(sorted(unmapped_samples.items())),
    }
    payload = {
        "game_root": str(game_root),
        "summary": summary,
        "files": files,
    }
    target = output_dir / "asset_inventory.json"
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"path": _rel_to_output(output_dir, target), "summary": summary}


def _status_for(models: list[Path], textures: list[Path], animations: list[Path], gui: list[Path]) -> str:
    if models and textures and animations:
        return "model_texture_animation"
    if models and textures:
        return "model_texture"
    if gui:
        return "gui_only"
    if models or textures or animations:
        return "partial"
    return "missing"


def export_original_graphics_report(game_root: Path | None, output_dir: Path, thumb_size: int = 256) -> dict:
    if game_root is None:
        manifest = {
            "enabled": False,
            "reason": "game root not found",
            "entities": [],
            "summary": {"entities": 0, "with_model": 0, "with_texture": 0, "with_animation": 0, "with_gui": 0},
        }
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        _write_html(output_dir, manifest)
        return manifest

    output_dir.mkdir(parents=True, exist_ok=True)
    entities: list[dict] = []
    for spec in ENTITY_SPECS:
        models = _find_matching(game_root, spec.model_globs, (".dff",), limit=16)
        textures = _find_matching(game_root, spec.texture_globs, (".dds", ".png"), limit=16)
        animations = _find_matching(game_root, spec.animation_globs, (".anm",), limit=48)
        gui = _find_matching(game_root, spec.gui_globs, (".png",), limit=8)

        texture_preview = _make_dds_preview(textures[0], output_dir, thumb_size) if textures and textures[0].suffix.lower() == ".dds" else None
        mesh_preview = _make_mesh_preview(models[0], output_dir, thumb_size) if models else None
        sprite_preview = _make_textured_sprite(models[0], game_root, output_dir, thumb_size) if models else None
        dff_info = inspect_dff(models[0]) if models else None
        model_3d = _make_model3d_json(models[0], game_root, output_dir) if models else None
        hierarchies = (dff_info or {}).get("hanim_hierarchies") or []
        expected_node_count = int(hierarchies[0].get("node_count", 0)) if hierarchies else 0
        animation_files = _animation_file_entries(
            game_root,
            animations,
            expected_node_count,
            output_dir,
            models[0].stem if models else "",
        )

        entities.append(
            {
                "key": spec.key,
                "label": spec.label,
                "group": spec.group,
                "status": _status_for(models, textures, animations, gui),
                "model_files": _file_entries(game_root, models),
                "texture_files": _file_entries(game_root, textures),
                "animation_files": animation_files,
                "animation_summary": _animation_summary(animation_files),
                "gui_files": _file_entries(game_root, gui),
                "texture_preview": _rel_to_output(output_dir, texture_preview),
                "mesh_preview": _rel_to_output(output_dir, mesh_preview),
                "sprite_preview": _rel_to_output(output_dir, sprite_preview),
                "model_3d": _rel_to_output(output_dir, model_3d),
                "dff": dff_info,
            }
        )

    summary = {
        "entities": len(entities),
        "with_model": sum(1 for entity in entities if entity["model_files"]),
        "with_texture": sum(1 for entity in entities if entity["texture_files"]),
        "with_animation": sum(1 for entity in entities if entity["animation_files"]),
        "with_gui": sum(1 for entity in entities if entity["gui_files"]),
        "with_model_3d": sum(1 for entity in entities if entity["model_3d"]),
        "with_mesh_preview": sum(1 for entity in entities if entity["mesh_preview"]),
        "with_sprite_preview": sum(1 for entity in entities if entity["sprite_preview"]),
        "with_texture_preview": sum(1 for entity in entities if entity["texture_preview"]),
        "with_animation_metadata": sum(1 for entity in entities if (entity.get("animation_summary") or {}).get("parsed", 0) > 0),
    }
    asset_inventory = _write_asset_inventory(game_root, output_dir, entities)
    inventory_summary = asset_inventory.get("summary") or {}
    summary["raw_asset_files"] = int(inventory_summary.get("total_files", 0))
    summary["raw_asset_mapped_files"] = int(inventory_summary.get("mapped_files", 0))
    summary["raw_asset_unmapped_files"] = int(inventory_summary.get("unmapped_files", 0))
    manifest = {
        "enabled": True,
        "game_root": str(game_root),
        "thumb_size": int(thumb_size),
        "summary": summary,
        "asset_inventory": asset_inventory,
        "entities": entities,
        "notes": [
            "DDS texture atlases are converted to local PNG previews.",
            "DFF static sprite previews are projected from original model geometry and affine-mapped from original DDS textures.",
            "DFF static geometry is exported as WebGL-ready JSON plus local PNG textures for the replay 3D mode.",
            "DFF mesh previews are also kept as untextured geometry-debug projections.",
            "DFF HAnim hierarchies and Skin-plugin headers are extracted with node IDs, used bones, and weight limits.",
            "ANM RenderWare headers are parsed for role, duration and keyframe counts; full skeletal/object skinning still requires a HAnim renderer.",
        ],
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    _write_html(output_dir, manifest)
    return manifest


def _short_file_list(files: list[dict], limit: int = 6) -> str:
    names = [html.escape(str(item.get("name", ""))) for item in files[:limit]]
    if len(files) > limit:
        names.append(f"+{len(files) - limit} weitere")
    return ", ".join(names) if names else "fehlt"


def _short_animation_summary(summary: dict) -> str:
    if not summary or not summary.get("parsed"):
        return "fehlt"
    parts = []
    for role, data in sorted((summary.get("by_role") or {}).items()):
        count = int(data.get("count", 0))
        min_duration = float(data.get("min_duration", 0.0))
        max_duration = float(data.get("max_duration", 0.0))
        if abs(max_duration - min_duration) < 0.001:
            duration_text = f"{max_duration:.2f}s"
        else:
            duration_text = f"{min_duration:.2f}-{max_duration:.2f}s"
        parts.append(f"{html.escape(role)}: {count}x {duration_text}")
    return ", ".join(parts[:6]) if parts else "fehlt"


def _write_html(output_dir: Path, manifest: dict) -> None:
    entities = manifest.get("entities") or []
    summary = manifest.get("summary") or {}
    inventory = manifest.get("asset_inventory") or {}
    inventory_path = str(inventory.get("path") or "")
    inventory_link = f'<a href="{html.escape(inventory_path)}">Asset-Inventar JSON</a>' if inventory_path else ""
    rows = []
    for entity in entities:
        texture_preview = entity.get("texture_preview") or ""
        mesh_preview = entity.get("mesh_preview") or ""
        sprite_preview = entity.get("sprite_preview") or ""
        model_3d = entity.get("model_3d") or ""
        texture_img = f'<img src="{html.escape(texture_preview)}" alt="Textur">' if texture_preview else '<div class="empty">keine Textur</div>'
        mesh_img = f'<img src="{html.escape(mesh_preview)}" alt="Mesh">' if mesh_preview else '<div class="empty">kein Mesh</div>'
        sprite_img = f'<img src="{html.escape(sprite_preview)}" alt="Sprite">' if sprite_preview else '<div class="empty">kein Sprite</div>'
        dff = entity.get("dff") or {}
        geometry_count = dff.get("geometry_count", 0)
        vertices = sum(int(g.get("vertices", 0)) for g in dff.get("geometries", []))
        triangles = sum(int(g.get("triangles", 0)) for g in dff.get("geometries", []))
        hierarchies = dff.get("hanim_hierarchies") or []
        skins = dff.get("skin_plugins") or []
        skeleton_text = "kein HAnim"
        if hierarchies:
            node_count = int(hierarchies[0].get("node_count", 0))
            keyframe_size = int(hierarchies[0].get("keyframe_size", 0))
            skin_text = "ohne Skin"
            if skins:
                skin = skins[0]
                skin_text = f"Skin {int(skin.get('bone_count', 0))} Knochen, max. {int(skin.get('max_vertex_weights', 0))} Gewichte"
            skeleton_text = f"HAnim {node_count} Knoten, Keyframe {keyframe_size} Byte; {skin_text}"
        animation_summary = entity.get("animation_summary") or {}
        rows.append(
            f"""
            <article class="card">
              <div class="thumbs">
                <div>{sprite_img}<span>Sprite</span></div>
                <div>{mesh_img}<span>Mesh</span></div>
                <div>{texture_img}<span>Textur</span></div>
              </div>
              <h2>{html.escape(entity.get("label", ""))}</h2>
              <div class="meta">{html.escape(entity.get("group", ""))} · {html.escape(entity.get("status", ""))}</div>
              <dl>
                <dt>DFF</dt><dd>{_short_file_list(entity.get("model_files") or [])}</dd>
                <dt>DDS/PNG</dt><dd>{_short_file_list(entity.get("texture_files") or [])}</dd>
                <dt>ANM</dt><dd>{_short_file_list(entity.get("animation_files") or [])}</dd>
                <dt>ANM-Timing</dt><dd>{_short_animation_summary(animation_summary)}</dd>
                <dt>GUI</dt><dd>{_short_file_list(entity.get("gui_files") or [])}</dd>
                <dt>Geometrie</dt><dd>{geometry_count} Chunks, {vertices} Vertices, {triangles} Dreiecke</dd>
                <dt>Skelett</dt><dd>{html.escape(skeleton_text)}</dd>
                <dt>WebGL</dt><dd>{html.escape(model_3d) if model_3d else "fehlt"}</dd>
              </dl>
            </article>
            """
        )

    html_text = f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Siedler Originalgrafik Report</title>
  <style>
    html, body {{ margin:0; background:#111313; color:#efe4cf; font-family: system-ui, sans-serif; }}
    header {{ position:sticky; top:0; z-index:1; padding:16px 20px; background:#24180f; border-bottom:1px solid #7b5c36; }}
    h1 {{ margin:0 0 6px; font-size:22px; }}
    .summary {{ display:flex; gap:14px; flex-wrap:wrap; color:#d6c29a; font-size:13px; }}
    .summary a {{ color:#ffe09a; text-decoration:none; }}
    .summary a:hover {{ text-decoration:underline; }}
    main {{ padding:18px; display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:14px; }}
    .card {{ background:#1c1f1f; border:1px solid #4f4635; border-radius:6px; padding:12px; box-shadow:0 8px 22px rgba(0,0,0,.28); }}
    .thumbs {{ display:grid; grid-template-columns:repeat(3, 1fr); gap:8px; margin-bottom:10px; }}
    .thumbs > div {{ min-height:156px; display:flex; align-items:center; justify-content:center; position:relative; background:#0b0d0e; border:1px solid #363d3d; border-radius:4px; overflow:hidden; }}
    .thumbs img {{ max-width:100%; max-height:180px; object-fit:contain; image-rendering:auto; }}
    .thumbs span {{ position:absolute; left:6px; bottom:5px; padding:2px 5px; background:rgba(0,0,0,.62); border-radius:3px; color:#e6d5b2; font-size:11px; }}
    h2 {{ margin:0; font-size:17px; }}
    .meta {{ margin:4px 0 10px; color:#bda776; font-size:12px; text-transform:uppercase; letter-spacing:.05em; }}
    dl {{ display:grid; grid-template-columns:78px 1fr; gap:4px 8px; margin:0; font-size:12px; }}
    dt {{ color:#caa86a; }}
    dd {{ margin:0; color:#ddd0b6; overflow-wrap:anywhere; }}
    .empty {{ color:#7f7f7f; font-size:12px; }}
  </style>
</head>
<body>
  <header>
    <h1>Siedler 5 Originalgrafik Report</h1>
    <div class="summary">
      <span>Root: {html.escape(str(manifest.get("game_root", manifest.get("reason", ""))))}</span>
      <span>Entities: {int(summary.get("entities", 0))}</span>
      <span>Modelle: {int(summary.get("with_model", 0))}</span>
      <span>Texturen: {int(summary.get("with_texture", 0))}</span>
      <span>Animationen: {int(summary.get("with_animation", 0))}</span>
      <span>ANM-Metadaten: {int(summary.get("with_animation_metadata", 0))}</span>
      <span>WebGL-Modelle: {int(summary.get("with_model_3d", 0))}</span>
      <span>Sprites: {int(summary.get("with_sprite_preview", 0))}</span>
      <span>Mesh-Previews: {int(summary.get("with_mesh_preview", 0))}</span>
      <span>Rohdateien: {int(summary.get("raw_asset_files", 0))}</span>
      <span>Ungemappt: {int(summary.get("raw_asset_unmapped_files", 0))}</span>
      <span>{inventory_link}</span>
    </div>
  </header>
  <main>
    {''.join(rows)}
  </main>
</body>
</html>
"""
    (output_dir / "index.html").write_text(html_text, encoding="utf-8")


def main() -> None:
    args = _parse_args()
    game_root = find_game_root(args.game_root)
    manifest = export_original_graphics_report(game_root, Path(args.output_dir), thumb_size=args.thumb_size)
    print(f"Original graphics report: {Path(args.output_dir) / 'index.html'}")
    print(json.dumps(manifest.get("summary", {}), ensure_ascii=False))


if __name__ == "__main__":
    main()
