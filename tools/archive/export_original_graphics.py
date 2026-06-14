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

from PIL import Image, ImageDraw

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


@dataclass(frozen=True)
class EntitySpec:
    key: str
    label: str
    group: str
    model_globs: tuple[str, ...] = ()
    texture_globs: tuple[str, ...] = ()
    animation_globs: tuple[str, ...] = ()
    gui_globs: tuple[str, ...] = ()


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
    EntitySpec("clay_mine_1", "Lehmmine 1", "mines", ("PB_ClayMine1.dff",), ("PB_ClayMine1.dds",), ("PB_ClayMine*.anm",), ("b_small_generic.png",)),
    EntitySpec("iron_mine_1", "Eisenmine 1", "mines", ("PB_IronMine1.dff",), ("PB_IronMine1.dds",), ("PB_IronMine*.anm",), ("b_small_generic.png",)),
    EntitySpec("stone_mine_1", "Steinmine 1", "mines", ("PB_StoneMine1.dff",), ("PB_StoneMine1.dds",), ("PB_StoneMine*.anm",), ("b_small_generic.png",)),
    EntitySpec("sulfur_mine_1", "Schwefelmine 1", "mines", ("PB_SulfurMine1.dff",), ("PB_SulfurMine1.dds",), ("PB_SulfurMine*.anm",), ("b_small_generic.png",)),
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
    offset += 8 * vertex_count * uv_sets

    triangles: list[tuple[int, int, int]] = []
    for index in range(triangle_count):
        tri_offset = offset + index * 8
        if tri_offset + 8 > len(payload):
            break
        v2, v1, _material, v3 = struct.unpack_from("<HHHH", payload, tri_offset)
        if v1 < vertex_count and v2 < vertex_count and v3 < vertex_count:
            triangles.append((v1, v2, v3))
    offset += 8 * triangle_count

    vertices: list[tuple[float, float, float]] = []
    if offset + 24 <= len(payload):
        offset += 16  # bounding sphere center/radius
        has_vertices, has_normals = struct.unpack_from("<II", payload, offset)
        offset += 8
        if has_vertices and offset + 12 * vertex_count <= len(payload):
            vertices = [
                struct.unpack_from("<fff", payload, offset + index * 12)
                for index in range(vertex_count)
            ]
        if has_normals:
            offset += 12 * vertex_count

    return {
        "flags": int(flags),
        "num_uv_sets": int(num_uv_sets),
        "native_flags": int(native_flags),
        "triangles": int(triangle_count),
        "vertices": int(vertex_count),
        "morph_targets": int(morph_count),
        "parsed_triangles": triangles,
        "parsed_vertices": vertices,
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
                geometry.pop("parsed_vertices", None)
                geometries.append(geometry)
    return {
        "bytes": path.stat().st_size,
        "root_chunk_type": int(root[2]) if root else None,
        "rw_version": f"0x{root[4]:08x}" if root else "",
        "chunk_count": len(chunks),
        "geometry_count": len(geometries),
        "geometries": geometries,
    }


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


def _file_entries(game_root: Path, paths: list[Path]) -> list[dict]:
    return [{"name": path.name, "path": _rel_to_game(game_root, path), "bytes": path.stat().st_size} for path in paths]


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
        dff_info = inspect_dff(models[0]) if models else None

        entities.append(
            {
                "key": spec.key,
                "label": spec.label,
                "group": spec.group,
                "status": _status_for(models, textures, animations, gui),
                "model_files": _file_entries(game_root, models),
                "texture_files": _file_entries(game_root, textures),
                "animation_files": _file_entries(game_root, animations),
                "gui_files": _file_entries(game_root, gui),
                "texture_preview": _rel_to_output(output_dir, texture_preview),
                "mesh_preview": _rel_to_output(output_dir, mesh_preview),
                "dff": dff_info,
            }
        )

    summary = {
        "entities": len(entities),
        "with_model": sum(1 for entity in entities if entity["model_files"]),
        "with_texture": sum(1 for entity in entities if entity["texture_files"]),
        "with_animation": sum(1 for entity in entities if entity["animation_files"]),
        "with_gui": sum(1 for entity in entities if entity["gui_files"]),
        "with_mesh_preview": sum(1 for entity in entities if entity["mesh_preview"]),
        "with_texture_preview": sum(1 for entity in entities if entity["texture_preview"]),
    }
    manifest = {
        "enabled": True,
        "game_root": str(game_root),
        "thumb_size": int(thumb_size),
        "summary": summary,
        "entities": entities,
        "notes": [
            "DDS texture atlases are converted to local PNG previews.",
            "DFF static mesh previews are untextured projections of the original model geometry.",
            "ANM files are inventoried; full skeletal/object animation playback still requires a RenderWare animation renderer.",
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


def _write_html(output_dir: Path, manifest: dict) -> None:
    entities = manifest.get("entities") or []
    summary = manifest.get("summary") or {}
    rows = []
    for entity in entities:
        texture_preview = entity.get("texture_preview") or ""
        mesh_preview = entity.get("mesh_preview") or ""
        texture_img = f'<img src="{html.escape(texture_preview)}" alt="Textur">' if texture_preview else '<div class="empty">keine Textur</div>'
        mesh_img = f'<img src="{html.escape(mesh_preview)}" alt="Mesh">' if mesh_preview else '<div class="empty">kein Mesh</div>'
        dff = entity.get("dff") or {}
        geometry_count = dff.get("geometry_count", 0)
        vertices = sum(int(g.get("vertices", 0)) for g in dff.get("geometries", []))
        triangles = sum(int(g.get("triangles", 0)) for g in dff.get("geometries", []))
        rows.append(
            f"""
            <article class="card">
              <div class="thumbs">
                <div>{mesh_img}<span>Mesh</span></div>
                <div>{texture_img}<span>Textur</span></div>
              </div>
              <h2>{html.escape(entity.get("label", ""))}</h2>
              <div class="meta">{html.escape(entity.get("group", ""))} · {html.escape(entity.get("status", ""))}</div>
              <dl>
                <dt>DFF</dt><dd>{_short_file_list(entity.get("model_files") or [])}</dd>
                <dt>DDS/PNG</dt><dd>{_short_file_list(entity.get("texture_files") or [])}</dd>
                <dt>ANM</dt><dd>{_short_file_list(entity.get("animation_files") or [])}</dd>
                <dt>GUI</dt><dd>{_short_file_list(entity.get("gui_files") or [])}</dd>
                <dt>Geometrie</dt><dd>{geometry_count} Chunks, {vertices} Vertices, {triangles} Dreiecke</dd>
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
    main {{ padding:18px; display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:14px; }}
    .card {{ background:#1c1f1f; border:1px solid #4f4635; border-radius:6px; padding:12px; box-shadow:0 8px 22px rgba(0,0,0,.28); }}
    .thumbs {{ display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:10px; }}
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
      <span>Mesh-Previews: {int(summary.get("with_mesh_preview", 0))}</span>
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
