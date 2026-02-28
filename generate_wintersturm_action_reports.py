from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Tuple

from environment import (
    ActionPhase,
    CATEGORY_AREA_MAP,
    DEPOSIT_AREA_TO_SLOT,
    MAX_POSITION_SLOTS,
    SHAFT_AREA_TO_SLOT,
    SOURCE_CATEGORIES,
    TARGET_CATEGORIES,
    SiedlerScharfschuetzenEnv,
    buildings_db,
)


ROOT = Path(__file__).resolve().parent
SPECIFIC_REPORT = ROOT / "WINTERSTURM_SPECIFIC_INDEX_TABLE.md"
POSITION_REPORT = ROOT / "WINTERSTURM_BUILD_POSITION_AUDIT.md"


def repair_text(value: object) -> str:
    text = str(value)
    for _ in range(3):
        try:
            repaired = text.encode("latin1").decode("utf-8")
        except Exception:
            break
        if not repaired or repaired == text:
            break
        text = repaired
    return text


def md_table(headers: List[str], rows: Iterable[Iterable[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(repair_text(cell) for cell in row) + " |")
    return "\n".join(lines)


def get_slot_meta(env: SiedlerScharfschuetzenEnv, area) -> Tuple[str, str, str]:
    if area in SHAFT_AREA_TO_SLOT:
        category, slot_idx = SHAFT_AREA_TO_SLOT[area]
        shafts = env.shaft_categories.get(category, {}).get("shafts", [])
        if slot_idx < len(shafts):
            slot = shafts[slot_idx]
            return "Stollen", f"{slot['x']:.2f}, {slot['y']:.2f}", "Sammelpunkt"
        return "Stollen", "-", "unbenutzt auf Wintersturm"

    if area in DEPOSIT_AREA_TO_SLOT:
        category, slot_idx = DEPOSIT_AREA_TO_SLOT[area]
        deposits = env.deposit_categories.get(category, {}).get("deposits", [])
        if slot_idx < len(deposits):
            slot = deposits[slot_idx]
            return "Vorkommen", f"{slot['x']:.2f}, {slot['y']:.2f}", "Mine-Bauplatz + Sammelpunkt bis Mine steht"
        return "Vorkommen", "-", "unbenutzt auf Wintersturm"

    return "-", "-", "-"


def build_source_rows(env: SiedlerScharfschuetzenEnv) -> List[List[object]]:
    rows: List[List[object]] = []
    rows.append([0, SOURCE_CATEGORIES[0], 0, "FREE", "-", "Specific wird uebersprungen; 0 ist Fallback"])

    for idx, tree in enumerate(env.tree_list_internal):
        zone_name = tree.get("zone", "")
        rows.append(
            [
                1,
                SOURCE_CATEGORIES[1],
                idx,
                f"TREE_{idx}",
                f"{tree.get('x', 0):.0f}, {tree.get('y', 0):.0f}",
                f"zone={zone_name}; einzelner Baum",
            ]
        )

    for cat_idx in range(2, 6):
        for spec_idx, area in enumerate(CATEGORY_AREA_MAP.get(cat_idx, [])):
            slot_type, coords, note = get_slot_meta(env, area)
            rows.append([cat_idx, SOURCE_CATEGORIES[cat_idx], spec_idx, area.name, coords, f"{slot_type}; {note}"])

    rows.append([6, SOURCE_CATEGORIES[6], "0..N-1", "construction_sites[i]", "-", "dynamisch zur Laufzeit"])
    return rows


def build_target_rows(env: SiedlerScharfschuetzenEnv, build_counts: dict[str, int]) -> List[List[object]]:
    rows: List[List[object]] = []
    rows.append([0, TARGET_CATEGORIES[0], 0, "FREE", "-", "Specific wird uebersprungen; 0 ist Fallback"])

    for idx, tree in enumerate(env.tree_list_internal):
        zone_name = tree.get("zone", "")
        rows.append(
            [
                1,
                TARGET_CATEGORIES[1],
                idx,
                f"TREE_{idx}",
                f"{tree.get('x', 0):.0f}, {tree.get('y', 0):.0f}",
                f"zone={zone_name}; einzelner Baum",
            ]
        )

    for cat_idx in range(2, 6):
        for spec_idx, area in enumerate(CATEGORY_AREA_MAP.get(cat_idx, [])):
            slot_type, coords, note = get_slot_meta(env, area)
            rows.append([cat_idx, TARGET_CATEGORIES[cat_idx], spec_idx, area.name, coords, f"{slot_type}; {note}"])

    rows.append([6, TARGET_CATEGORIES[6], "0..N-1", "construction_sites[i]", "-", "dynamisch zur Laufzeit"])

    for idx, building in enumerate(env.buildable_buildings):
        currently_buildable = env._can_build(building)
        effective_count = build_counts.get(building, 0) if currently_buildable else 0
        rows.append(
            [
                7,
                TARGET_CATEGORIES[7],
                idx,
                building,
                "-",
                f"{effective_count} Baupositionen; maskiert={'ja' if currently_buildable else 'nein'}",
            ]
        )
    return rows


def building_class(env: SiedlerScharfschuetzenEnv, building: str) -> str:
    info = buildings_db.get(building, {})
    if info and info.get("mine_type"):
        return "Mine-Slot"
    if building.startswith("Dorfzentrum_"):
        return "Dorfzentrum-Slot"
    return "Kartenposition"


def sample_positions(candidates: List[dict]) -> str:
    if not candidates:
        return "-"
    sample = candidates[:3]
    return "; ".join(f"({int(pos['x'])}, {int(pos['y'])})" for pos in sample)


def generate_reports() -> None:
    env = SiedlerScharfschuetzenEnv()
    env.reset()

    build_counts: dict[str, int] = {}
    build_candidates: dict[str, List[dict]] = {}
    currently_buildable_count = 0
    for building in env.buildable_buildings:
        candidates = env._get_build_position_candidates(building)
        build_counts[building] = len(candidates)
        build_candidates[building] = candidates
        if env._can_build(building):
            currently_buildable_count += 1

    summary_rows = [
        ["source_specific_size", env.source_specific_size, "gepolsterter Head; Masken schalten pro Kategorie frei"],
        ["target_specific_size", env.target_specific_size, "Head-Groesse fuer exakte Holz-Baeume und Neubau-Ziele"],
        ["currently_masked_neubau_types", currently_buildable_count, "auf Wintersturm im Reset wirklich waehlbar"],
        ["wood_tree_count", len(env.tree_list_internal), "Holz ist jetzt einzelbaum-genau maskiert"],
        ["wood_zone_count", len(env.wood_zone_names), "nach Split grosser Holzgebiete"],
        ["position_group_count", env.action_spaces[ActionPhase.POSITION_GROUP].n, "44 Gruppen"],
        ["position_index_size", env.action_spaces[ActionPhase.POSITION_INDEX].n, "50 Indizes je Gruppe"],
        ["max_position_slots", MAX_POSITION_SLOTS, "harte Obergrenze pro Gebaeudetyp"],
    ]

    source_rows = build_source_rows(env)
    target_rows = build_target_rows(env, build_counts)

    specific_parts = [
        "# Wintersturm Specific Index Table",
        "",
        "Diese Tabelle zeigt die aktuelle, tatsaechlich maskierte Bedeutung von `source_specific` und `target_specific` auf Wintersturm.",
        "",
        "## Summary",
        "",
        md_table(["field", "value", "note"], summary_rows),
        "",
        "## Source Specific",
        "",
        md_table(
            ["source_category", "category_name", "specific_index", "entry", "coords", "note"],
            source_rows,
        ),
        "",
        "## Target Specific",
        "",
        md_table(
            ["target_category", "category_name", "specific_index", "entry", "coords", "note"],
            target_rows,
        ),
        "",
    ]
    SPECIFIC_REPORT.write_text("\n".join(specific_parts), encoding="utf-8")

    position_rows = []
    capped = 0
    for idx, building in enumerate(env.buildable_buildings):
        candidates = build_candidates[building]
        count = build_counts[building]
        buildable_now = env._can_build(building)
        effective_count = count if buildable_now else 0
        if count >= MAX_POSITION_SLOTS:
            capped += 1
        position_rows.append(
            [
                idx,
                building,
                building_class(env, building),
                "ja" if buildable_now else "nein",
                effective_count,
                "ja" if count >= MAX_POSITION_SLOTS else "nein",
                sample_positions(candidates if buildable_now else []),
            ]
        )

    position_parts = [
        "# Wintersturm Build Position Audit",
        "",
        "Diese Tabelle zeigt, wie viele konkrete Baupositionen der Agent pro baubarem Gebaeudetyp aktuell waehlen kann.",
        "",
        "## Summary",
        "",
        md_table(
            ["field", "value", "note"],
            [
                ["buildable_building_types", len(env.buildable_buildings), "alle `target_specific`-Eintraege fuer Neubau"],
                ["currently_buildable_types", currently_buildable_count, "nach Wintersturm-Regeln und Positionslogik"],
                ["position_cap_per_building", MAX_POSITION_SLOTS, "44 * 50"],
                ["buildings_hitting_cap", capped, "wenn > 0, dann ist der Positionsraum fuer diese Typen abgeschnitten"],
                ["full_map_search", "ja", "normale Gebaeude kommen aus `find_valid_building_positions(...)` ueber ganz P1"],
            ],
        ),
        "",
        "## Position Counts",
        "",
        md_table(
            ["build_idx", "building", "class", "buildable_now", "candidate_count", "hits_cap", "sample_positions"],
            position_rows,
        ),
        "",
    ]
    POSITION_REPORT.write_text("\n".join(position_parts), encoding="utf-8")

    print(f"Wrote {SPECIFIC_REPORT.name}")
    print(f"Wrote {POSITION_REPORT.name}")


if __name__ == "__main__":
    generate_reports()
