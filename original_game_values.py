"""Runtime-Zugriff auf aus dem Originalspiel extrahierte Werte."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


PROJECT_ROOT = Path(__file__).resolve().parent
GAME_DATA_JSON = PROJECT_ROOT / "config" / "game_data.json"
ALL_ORIGINAL_VALUES_JSONL = PROJECT_ROOT / "config" / "all_original_values.jsonl"


ENTITY_BASE_ALIASES = {
    "pb_headquarters": ("Hauptquartier",),
    "pb_villagecenter": ("Dorfzentrum",),
    "pb_residence": ("Wohnhaus",),
    "pb_farm": ("Bauernhof",),
    "pb_university": ("Hochschule",),
    "pb_sawmill": ("S\u00e4gem\u00fchle",),
    "pb_stonemason": ("Steinmetzh\u00fctte",),
    "pb_blacksmith": ("Schmiede",),
    "pb_brickworks": ("Lehmh\u00fctte",),
    "pb_alchemist": ("Alchimistenh\u00fctte",),
    "pb_gunsmithworkshop": ("B\u00fcchsenmacherei",),
    "pb_foundry": ("Kanongie\u00dferei",),
    "pb_ironmine": ("Eisenmine",),
    "pb_stonemine": ("Steinmine",),
    "pb_claymine": ("Lehmmine",),
    "pb_sulfurmine": ("Schwefelmine",),
    "pb_barracks": ("Kaserne",),
    "pb_archery": ("Schie\u00dfplatz",),
    "pb_stable": ("Stall",),
    "pb_tower": ("Turm",),
    "pb_bank": ("Bank",),
    "pb_monastery": ("Kloster",),
    "pb_market": ("Markt",),
    "pb_tavern": ("Taverne",),
    "pb_masterbuilderworkshop": ("Architektenstube",),
    "pb_powerplant": ("Wetterkraftwerk",),
    "pb_weathertower": ("Wetterturm",),
}

RESOURCE_NAME_MAP = {
    "gold": "Taler",
    "wood": "Holz",
    "stone": "Stein",
    "clay": "Lehm",
    "iron": "Eisen",
    "sulfur": "Schwefel",
}

TECH_ID_ALIASES = {
    "gt_beautification": ("GT_Beautification",),
    "gt_construction": ("Konstruktion",),
    "gt_gearwheel": ("Zahnr\u00e4der",),
    "gt_chainblock": ("Flaschenzug",),
    "gt_architecture": ("Architektur",),
    "gt_alchemy": ("Alchimie",),
    "gt_alloying": ("Legierungen",),
    "gt_metallurgy": ("Metallurgie",),
    "gt_chemistry": ("Chemie",),
    "gt_literacy": ("Bildung",),
    "gt_trading": ("Handelswesen",),
    "gt_printing": ("Buchdruck",),
    "gt_library": ("B\u00fcchereien",),
    "gt_mercenaries": ("Wehrpflicht",),
    "gt_standingarmy": ("Stehendes Heer",),
    "gt_tactics": ("Taktiken",),
    "gt_strategies": ("Pferdezucht",),
    "gt_mathematics": ("Mathematik",),
    "gt_binocular": ("Fernglas",),
    "gt_matchlock": ("Luntenschloss",),
    "gt_pulledbarrel": ("Gezogener Lauf",),
    "t_leathermailarmor": ("Lederr\u00fcstung",),
    "t_chainmailarmor": ("Kettenr\u00fcstung",),
    "t_platemailarmor": ("Plattenr\u00fcstung",),
    "t_masonry": ("Maurerarbeit",),
    "t_lightbricks": ("Leichte Ziegel",),
    "t_fletching": ("Pfeilherstellung",),
    "t_bodkinarrow": ("Panzerbrechende Pfeile",),
    "t_enhancedgunpowder": ("Verbessertes Schie\u00dfpulver",),
    "t_blisteringcannonballs": ("Gl\u00fchende Kanonenkugeln",),
    "t_masterofsmithery": ("Schmiedekunst",),
    "t_ironcasting": ("Eisenguss",),
    "t_softarcherarmor": ("Weiche R\u00fcstung",),
    "t_paddedarcherarmor": ("Wattierte R\u00fcstung",),
    "t_leatherarcherarmor": ("Leder-Bogensch\u00fctzenr\u00fcstung",),
    "t_woodaging": ("Holzalterung",),
    "t_turnery": ("Drechselei",),
    "t_weatherforecast": ("T_WeatherForecast", "Wettervorhersage"),
    "t_changeweather": ("T_ChangeWeather", "Wettermanipulation"),
    "t_debenture": ("Schuldschein",),
    "t_bookkeeping": ("Buchf\u00fchrung",),
    "t_scale": ("Waage",),
    "t_coinage": ("M\u00fcnzpr\u00e4gung",),
    "t_townguard": ("Stadtwache",),
    "t_cityguard": ("T_CityGuard",),
    "t_loom": ("Webstuhl",),
    "t_shoes": ("Schuhe",),
    "t_adjusttaxes": ("T_AdjustTaxes",),
    "t_blesssettlers1": ("T_BlessSettlers1",),
    "t_blesssettlers2": ("T_BlessSettlers2",),
    "t_bettertrainingbarracks": ("Kasernentraining",),
    "t_bettertrainingarchery": ("Schie\u00dftraining",),
    "t_shoeing": ("Hufbeschlag",),
    "t_betterchassis": ("Verbessertes Fahrgestell",),
    "t_cropcycle": ("T_CropCycle",),
    "t_spinningwheel": ("T_SpinningWheel",),
    "t_pickaxe": ("T_PickAxe",),
    "t_marketclay": ("T_MarketClay",),
    "t_marketgold": ("T_MarketGold",),
    "t_marketiron": ("T_MarketIron",),
    "t_marketstone": ("T_MarketStone",),
    "t_marketsulfur": ("T_MarketSulfur",),
    "t_marketwood": ("T_MarketWood",),
    "t_minimapnormalview": ("T_MinimapNormalView",),
    "t_minimapresouceview": ("T_MinimapResouceView",),
    "t_minimaptacticview": ("T_MinimapTacticView",),
    "t_onlinehelp": ("T_OnlineHelp",),
    "t_supertechnology": ("T_SuperTechnology",),
    "t_test": ("T_Test",),
    "t_test2": ("T_Test2",),
    "t_fleecearmor": ("T_FleeceArmor",),
    "t_fleecelinedleatherarmor": ("T_FleeceLinedLeatherArmor",),
    "t_leadshot": ("T_LeadShot",),
    "t_sights": ("T_Sights",),
    "t_upgraderifle1": ("T_UpgradeRifle1",),
    "mu_leaderrifle": ("MU_LeaderRifle",),
    "mu_thief": ("MU_Thief",),
    "t_scoutfindresources": ("T_ScoutFindResources",),
    "t_scouttorches": ("T_ScoutTorches",),
    "t_thiefsabotage": ("T_ThiefSabotage",),
    "b_bridge": ("B_Bridge",),
    "t_blesssettlers3": ("T_BlessSettlers3",),
    "t_blesssettlers4": ("T_BlessSettlers4",),
    "t_blesssettlers5": ("T_BlessSettlers5",),
    "t_makerain": ("T_MakeRain",),
    "t_makesnow": ("T_MakeSnow",),
    "t_makesummer": ("T_MakeSummer",),
    "t_tracking": ("T_Tracking",),
    "up2_headquarter": ("UP2_Headquarter",),
}

TECH_MODIFIER_EFFECT_KEYS = {
    "SpeedModifier": "speed_modifier",
    "ExplorationModifier": "exploration_modifier",
    "ArmorModifier": "armor_modifier",
    "DamageModifier": "damage_modifier",
    "DamageBonusModifier": "damage_bonus_modifier",
    "MaxRangeModifier": "max_range_modifier",
    "MinRangeModifier": "min_range_modifier",
    "HitpointModifier": "hitpoint_modifier",
    "DodgeModifier": "dodge_modifier",
    "GroupLimitModifier": "group_limit_modifier",
}


def _load_game_data() -> Dict:
    try:
        with GAME_DATA_JSON.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError, json.JSONDecodeError):
        return {}


def _mojibake_cp1252(text: str, rounds: int) -> str:
    result = text
    for _ in range(rounds):
        try:
            result = result.encode("utf-8").decode("cp1252")
        except UnicodeError:
            return text
    return result


def _aliases_with_legacy_encodings(names: Iterable[str]) -> Iterable[str]:
    for name in names:
        yield name
        yield _mojibake_cp1252(name, 1)
        yield _mojibake_cp1252(name, 2)
        yield _mojibake_cp1252(name, 3)


def _entity_base(entity_name: str) -> str:
    lowered = entity_name.lower()
    if lowered.startswith("pb_beautification"):
        return lowered
    return re.sub(r"\d+$", "", lowered)


def _aliases_for_entity(entity_name: str) -> Tuple[str, ...]:
    lowered = entity_name.lower()
    if lowered.startswith("pb_beautification"):
        suffix = lowered.replace("pb_beautification", "")
        return (f"PB_Beautification{suffix}",)
    return ENTITY_BASE_ALIASES.get(_entity_base(lowered), ())


def aliases_for_building_entity(entity_name: str) -> Tuple[str, ...]:
    """Liefert Sim-Namensvarianten fuer ein Original-Gebaeude."""
    lowered = str(entity_name).lower()
    suffix_match = re.search(r"(\d+)$", lowered)
    suffix = suffix_match.group(1) if suffix_match else ""
    aliases: List[str] = []
    for base in _aliases_with_legacy_encodings(_aliases_for_entity(lowered)):
        aliases.append(base)
        if suffix:
            aliases.append(f"{base}_{suffix}")
    return tuple(dict.fromkeys(aliases))


def aliases_for_technology(tech_id: str) -> Tuple[str, ...]:
    """Liefert Sim-Namensvarianten fuer eine Original-Technologie."""
    lowered = str(tech_id).lower()
    aliases: List[str] = [str(tech_id)]
    for alias in TECH_ID_ALIASES.get(lowered, ()):
        aliases.extend(_aliases_with_legacy_encodings((alias,)))
    return tuple(dict.fromkeys(aliases))


def load_building_footprints() -> Dict[str, Tuple[int, int]]:
    """Liefert Footprints aus config/game_data.json als Sim-Namensmapping."""
    data = _load_game_data()
    buildings = data.get("buildings") or {}
    result: Dict[str, Tuple[int, int]] = {}

    for entity_name, building in buildings.items():
        if not isinstance(building, dict):
            continue
        footprint = building.get("footprint") or {}
        try:
            width = int(footprint.get("width", 0))
            height = int(footprint.get("height", 0))
        except (TypeError, ValueError):
            continue
        if width <= 0 or height <= 0:
            continue

        aliases = _aliases_for_entity(str(entity_name))
        for alias in _aliases_with_legacy_encodings(aliases):
            result[alias] = (width, height)

    return result


def _point_tuple(point: object) -> Optional[Tuple[int, int]]:
    if not isinstance(point, dict):
        return None
    try:
        return int(point.get("x", 0)), int(point.get("y", 0))
    except (TypeError, ValueError):
        return None


def load_building_geometry() -> Dict[str, Dict[str, object]]:
    """Liefert Original-Blocked/Approach/Door/Leave-Geometrie als Sim-Namensmapping."""
    data = _load_game_data()
    buildings = data.get("buildings") or {}
    result: Dict[str, Dict[str, object]] = {}

    for entity_name, building in buildings.items():
        if not isinstance(building, dict):
            continue

        geometry: Dict[str, object] = {"entity": str(entity_name)}

        footprint = building.get("footprint") or {}
        try:
            width = int(footprint.get("width", 0))
            height = int(footprint.get("height", 0))
        except (TypeError, ValueError):
            width = 0
            height = 0
        if width > 0 and height > 0:
            geometry["footprint"] = (width, height)

        blocked1 = _point_tuple(building.get("blocked1"))
        blocked2 = _point_tuple(building.get("blocked2"))
        if blocked1 and blocked2:
            x1, y1 = blocked1
            x2, y2 = blocked2
            geometry["blocked"] = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

        for key in ("approach_pos", "door_pos", "leave_pos"):
            point = _point_tuple(building.get(key))
            if point is not None:
                geometry[key] = point

        if len(geometry) <= 1:
            continue

        for alias in aliases_for_building_entity(str(entity_name)):
            result[alias] = dict(geometry)

    return result


def _load_technology_modifier_effects() -> Dict[str, Dict[str, float]]:
    """Liest XML-Modifier wie SpeedModifier/ExplorationModifier aus dem Roh-Manifest."""
    if not ALL_ORIGINAL_VALUES_JSONL.exists():
        return {}

    raw: Dict[str, Dict[str, List[Dict[str, object]]]] = {}
    try:
        with ALL_ORIGINAL_VALUES_JSONL.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except (TypeError, ValueError, json.JSONDecodeError):
                    continue
                file_name = str(entry.get("file", ""))
                if not file_name.lower().startswith("technologies/"):
                    continue
                parts = str(entry.get("path", "")).split("/")
                if len(parts) < 3:
                    continue
                modifier = parts[1]
                field = parts[2]
                if modifier not in TECH_MODIFIER_EFFECT_KEYS or field not in {"Value", "Operation"}:
                    continue
                tech_id = Path(file_name).stem.lower()
                bucket = raw.setdefault(tech_id, {}).setdefault(modifier, [])
                if field == "Value":
                    bucket.append({"value": entry.get("value"), "operation": "+"})
                elif bucket:
                    bucket[-1]["operation"] = entry.get("value") or "+"
    except OSError:
        return {}

    result: Dict[str, Dict[str, float]] = {}
    for tech_id, modifiers in raw.items():
        effects: Dict[str, float] = {}
        for modifier, values in modifiers.items():
            effect_key = TECH_MODIFIER_EFFECT_KEYS.get(modifier)
            if not effect_key:
                continue
            for item in values:
                try:
                    value = float(item.get("value", 0) or 0)
                except (TypeError, ValueError):
                    continue
                operation = str(item.get("operation") or "+").strip()
                key = effect_key if operation == "+" else f"{effect_key}_{operation}"
                effects[key] = effects.get(key, 0.0) + value
        if effects:
            result[tech_id] = effects
    return result


def load_technology_xml_values() -> Dict[str, Dict]:
    """Liefert belegte Technologie-Werte aus config/game_data.json."""
    data = _load_game_data()
    technologies = data.get("technologies") or {}
    modifier_effects = _load_technology_modifier_effects()
    result: Dict[str, Dict] = {}

    for tech_id, tech in technologies.items():
        if not isinstance(tech, dict):
            continue
        cost = {
            RESOURCE_NAME_MAP[resource]: int(amount)
            for resource, amount in (tech.get("cost") or {}).items()
            if resource in RESOURCE_NAME_MAP and int(amount) > 0
        }
        tech_required: List[str] = []
        entity_conditions: List[Dict] = []
        for cond in tech.get("conditions") or []:
            if not isinstance(cond, dict):
                continue
            if cond.get("type") == "technology":
                value = cond.get("value")
                if value:
                    tech_required.append(str(value))
            elif cond.get("type") == "building":
                value = cond.get("value")
                if value:
                    entity_conditions.append(
                        {
                            "entity": str(value),
                            "amount": int(cond.get("amount", 1) or 1),
                        }
                    )
        result[str(tech_id)] = {
            "cost": cost,
            "research_time": int(tech.get("time", 0) or 0),
            "tech_required_ids": tech_required,
            "entity_conditions": entity_conditions,
            "required_entity_conditions": tech.get("required_entity_conditions"),
            "effects": modifier_effects.get(str(tech_id).lower(), {}),
        }

    return result
