"""
Siedler 5 - Worker Simulation
Simuliert das WorkTime-System mit Pausen und Laufwegen.

Kritische Mechaniken:
- Worker haben WorkTime (sinkt beim Arbeiten)
- Bei Hunger: Laufen zu Farm â†’ Essen â†’ Laufen zu Wohnhaus â†’ Ruhen
- Wenn kein Farm/Wohnhaus in 5000 Radius: Camp (nur 10% Regeneration!)
- ErschÃ¶pfte Worker (WorkTime=0): Nur 10% Effizienz!
- SERFS haben KEIN WorkTime-System!
"""

import json
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Dict, Optional, Tuple, Callable
from pathlib import Path


class WorkerState(Enum):
    """ZustÃ¤nde eines Workers."""
    IDLE = "idle"
    WORKING = "working"
    WALKING_TO_SUPPLIER = "walking_to_supplier"
    WALKING_FROM_SUPPLIER_TO_WORK = "walking_from_supplier_to_work"
    WALKING_TO_FARM = "walking_to_farm"
    EATING = "eating"
    WALKING_TO_RESIDENCE = "walking_to_residence"
    RESTING = "resting"
    WALKING_TO_CAMP = "walking_to_camp"
    CAMPING = "camping"
    WALKING_TO_WORK = "walking_to_work"


# Worker-Typ Normalisierung (XML/PU_Namen -> interne Namen)
WORKER_TYPE_ALIASES = {
    "sawmillworker": "sawmill_worker",
    "tavernbarkeeper": "barkeeper",
    "masterbuilder": "master_builder",
}


def normalize_worker_type(name: str) -> str:
    if not name:
        return ""
    w = name.lower()
    if w.startswith("pu_"):
        w = w[3:]
    return WORKER_TYPE_ALIASES.get(w, w)


@dataclass
class Position:
    """2D-Position."""
    x: float = 0.0
    y: float = 0.0

    def distance_to(self, other: 'Position') -> float:
        """Berechnet Distanz zu einer anderen Position."""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)



# === GLOBALE WORKTIME-PARAMETER (aus logic.xml) ===
# Diese Werte steuern das WorkTime-System fuer ALLE Worker
WORKTIME_BASE = 125  # Basis-WorkTime, multipliziert mit Motivation -> Max WorkTime
WORKTIME_THRESHOLD_WORK = 25  # WorkTime unter diesem Wert -> Worker geht essen/ruhen
FORCE_TO_WORK_PENALTY = 0.2  # Motivations-Malus wenn Worker zum Arbeiten gezwungen wird


@dataclass
class WorkTimeParams:
    """WorkTime-Parameter fuer einen Worker-Typ."""
    work_wait_until: int = 30000  # ms - Zeit pro Arbeitszyklus
    eat_wait: int = 2000  # ms - Zeit zum Essen
    rest_wait: int = 3000  # ms - Zeit zum Ruhen
    work_time_change_work: int = -50  # WorkTime-Aenderung pro TASK_CHANGE_WORK_TIME_WORK
    work_time_change_farm: float = 0.7  # +70% beim Essen
    work_time_change_residence: float = 0.5  # +50% beim Ruhen
    work_time_change_camp: float = 0.1  # +10% beim Campen
    work_time_max_farm: int = 100  # Max WorkTime-Cap beim Essen
    work_time_max_residence: int = 400  # Max WorkTime-Cap beim Ruhen
    exhausted_malus: float = 0.2  # Effizienz bei Erschoepfung
    # NEU: TaskList-Multiplier aus Engine-Dekodierung
    # Gibt an wie oft TASK_CHANGE_WORK_TIME_WORK pro Arbeitszyklus aufgerufen wird
    # Die meisten Worker haben 2x -> effektiver WorkTimeChange = work_time_change_work * 2
    worktime_changes_per_cycle: int = 1  # Default 1, wird pro Worker-Typ gesetzt


# Worker-spezifische Timing-Daten (aus extra2 XMLs + Engine-TaskList-Analyse)
# Jeder Worker-Typ hat eigene Parameter!
# worktime_changes_per_cycle: Aus tl_*_work.xml - wie oft TASK_CHANGE_WORK_TIME_WORK pro Zyklus
WORKER_PARAMS: Dict[str, WorkTimeParams] = {
    # FARMER - schneller Arbeitszyklus, Standard-Regeneration
    "farmer": WorkTimeParams(
        work_wait_until=4000,
        exhausted_malus=0.1,  # Nur 10% Malus!
        worktime_changes_per_cycle=1,  # tl_farmer_work: 1x
    ),
    # MINER - langer Arbeitszyklus (Bergbau dauert)
    "miner": WorkTimeParams(
        work_wait_until=30000,
        exhausted_malus=0.2,
        worktime_changes_per_cycle=2,  # tl_miner_*mine_work: 2x (mine-spezifische TaskLists!)
    ),
    # SAWMILL_WORKER - sehr langer Zyklus
    "sawmill_worker": WorkTimeParams(
        work_wait_until=40000,
        exhausted_malus=0.2,
        worktime_changes_per_cycle=2,  # tl_sawmillworker_work: 2x
    ),
    # BRICKMAKER - langer Zyklus (Ziegelherstellung)
    "brickmaker": WorkTimeParams(
        work_wait_until=30000,
        exhausted_malus=0.2,
        worktime_changes_per_cycle=2,  # tl_brickmaker_work: 2x
    ),
    # STONECUTTER
    "stonecutter": WorkTimeParams(
        work_wait_until=15000,
        exhausted_malus=0.2,
        worktime_changes_per_cycle=2,  # tl_stonecutter_work: 2x
    ),
    # SMITH - langer Zyklus
    "smith": WorkTimeParams(
        work_wait_until=30000,
        exhausted_malus=0.2,
        worktime_changes_per_cycle=2,  # tl_smith_work: 2x
    ),
    # ALCHEMIST - mittlerer Zyklus
    "alchemist": WorkTimeParams(
        work_wait_until=20000,
        exhausted_malus=0.2,
        worktime_changes_per_cycle=2,  # tl_alchemist_work: 2x
    ),
    # PRIEST
    "priest": WorkTimeParams(
        work_wait_until=4000,
        exhausted_malus=0.2,
        worktime_changes_per_cycle=2,  # tl_priest_work: 2x
    ),
    # TRADER
    "trader": WorkTimeParams(
        work_wait_until=18000,
        exhausted_malus=0.2,
        worktime_changes_per_cycle=1,  # tl_trader_work: 1x
    ),
    # TREASURER
    "treasurer": WorkTimeParams(
        work_wait_until=15000,
        exhausted_malus=0.2,
        worktime_changes_per_cycle=2,  # tl_treasurer_work: 2x
    ),
    # SMELTER (korrekt: work_wait_until=4000, spezielle eat/rest)
    "smelter": WorkTimeParams(
        work_wait_until=4000,
        eat_wait=3000,  # Laenger als Standard (2000)!
        rest_wait=2000,  # Kuerzer als Standard (3000)!
        exhausted_malus=0.2,
        worktime_changes_per_cycle=1,  # Kein tl_smelter_work gefunden, Default 1
    ),
    # SCHOLAR - Gelehrte (Hochschule)
    "scholar": WorkTimeParams(
        work_wait_until=30000,
        exhausted_malus=0.2,
        worktime_changes_per_cycle=2,  # tl_scholar_work: 2x
    ),
    # ENGINEER - SPEZIELL: laengere Esszeit, kuerzere Ruhezeit!
    "engineer": WorkTimeParams(
        work_wait_until=4000,
        eat_wait=3000,
        rest_wait=2000,
        exhausted_malus=0.2,
        worktime_changes_per_cycle=1,  # tl_engineer_work: 1x
    ),
    # MASTER_BUILDER
    "master_builder": WorkTimeParams(
        work_wait_until=18000,
        exhausted_malus=0.2,
        worktime_changes_per_cycle=1,  # Kein tl_masterbuilder_work gefunden, Default 1
    ),
    # GUNSMITH - Buechsenmacher
    "gunsmith": WorkTimeParams(
        work_wait_until=30000,
        exhausted_malus=0.2,
        worktime_changes_per_cycle=2,  # tl_gunsmith_work: 2x
    ),
    # BARKKEEPER - Taverne
    "barkeeper": WorkTimeParams(
        work_wait_until=4000,
        exhausted_malus=0.1,  # Korrigiert! Engine=0.1 (war 0.2 im Env)
        worktime_changes_per_cycle=1,  # tl_tavernbarkeeper_work: 1x
    ),
    # COINER - KOMPLETT ANDERS! (aus PU_Coiner.xml)
    # Hoher Energieverbrauch, aber sehr schnelle kurze Pausen
    "coiner": WorkTimeParams(
        work_wait_until=4000,
        work_time_change_work=-100,  # DOPPELT so viel Verbrauch!
        eat_wait=500,  # SEHR kurz (statt 2000)!
        rest_wait=500,  # SEHR kurz (statt 3000)!
        work_time_change_farm=0.1,  # Wenig Regeneration von Farm!
        work_time_change_residence=0.1,  # Wenig Regeneration von Wohnhaus!
        work_time_change_camp=0.2,  # DOPPELT so viel vom Camp!
        work_time_max_farm=200,
        work_time_max_residence=200,
        exhausted_malus=0.05,  # Nur 5% Malus!
        worktime_changes_per_cycle=1,  # tl_coiner_work: 1x
    ),
}

# Worker-Geschwindigkeiten (aus extra2 XMLs)
WORKER_SPEEDS: Dict[str, int] = {
    "serf": 400,  # KORRIGIERT! (aus PU_Serf.xml: Speed=400)
    "farmer": 320,
    "miner": 320,
    "sawmill_worker": 320,
    "brickmaker": 320,
    "stonecutter": 320,
    "smith": 320,
    "alchemist": 320,
    "priest": 320,
    "trader": 320,
    "treasurer": 320,
    "smelter": 320,
    "scholar": 320,
    "engineer": 320,
    "master_builder": 320,
    "gunsmith": 320,
    "coiner": 320,
    "barkeeper": 320,
}

# Coiner hat spezielle CamperRange (2000 statt 5000)
WORKER_CAMPER_RANGE: Dict[str, int] = {
    "coiner": 2000,  # Muss nÃ¤her bei GebÃ¤uden sein!
    # Alle anderen: Standard (5000)
}

# Konstanten (aus Logic.xml)
CAMPER_RANGE = 5000  # Max-Distanz fÃ¼r Pausen-GebÃ¤ude
WORK_TIME_BASE = 125  # WorkTimeBase aus Logic.xml
WORK_TIME_THRESHOLD_WORK = 25  # WorkTimeThresholdWork aus Logic.xml
WORK_TIME_THRESHOLD_FARM = 0.4  # WorkTimeThresholdFarm aus Logic.xml
WORK_TIME_THRESHOLD_RESIDENCE = 0.6  # WorkTimeThresholdResidence aus Logic.xml
WORK_TIME_START = WORK_TIME_BASE  # Startwert WorkTime
EXHAUSTED_THRESHOLD = 0  # Ab wann erschÃ¶pft
# MotivationMillisecondsWithoutJob aus Logic.xml
JOBLESS_LEAVE_MS = 30000


def _clone_worktime_params_map(params: Dict[str, WorkTimeParams]) -> Dict[str, WorkTimeParams]:
    """Erstellt eine tiefe Kopie von WorkTimeParams-Mappings."""
    cloned: Dict[str, WorkTimeParams] = {}
    for name, value in params.items():
        cloned[name] = WorkTimeParams(**vars(value))
    return cloned


DEFAULT_WORKER_PARAMS = _clone_worktime_params_map(WORKER_PARAMS)
DEFAULT_WORKER_SPEEDS = dict(WORKER_SPEEDS)
DEFAULT_WORKER_CAMPER_RANGE = dict(WORKER_CAMPER_RANGE)
DEFAULT_WORKTIME_BASE = WORKTIME_BASE
DEFAULT_WORKTIME_THRESHOLD_WORK = WORKTIME_THRESHOLD_WORK
DEFAULT_FORCE_TO_WORK_PENALTY = FORCE_TO_WORK_PENALTY
DEFAULT_CAMPER_RANGE = CAMPER_RANGE


def _safe_int(value: Any, default: int) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _extract_worktime_changes_per_cycle(worker_truth: Dict[str, Any], fallback: int) -> int:
    """Leitet TASK_CHANGE_WORK_TIME_WORK-Aufrufe pro Zyklus aus dem Truth-Modell ab."""
    counts: List[int] = []
    work_cycle = worker_truth.get("work_cycle_truth") or {}

    primary = work_cycle.get("primary_work_tasklist") or {}
    if isinstance(primary, dict):
        count = primary.get("task_change_work_time_work_count")
        if isinstance(count, int) and count > 0:
            counts.append(count)

    miner_tasklists = work_cycle.get("miner_tasklists") or {}
    if isinstance(miner_tasklists, dict):
        for tasklist in miner_tasklists.values():
            if not isinstance(tasklist, dict):
                continue
            count = tasklist.get("task_change_work_time_work_count")
            if isinstance(count, int) and count > 0:
                counts.append(count)

    if not counts:
        return max(1, fallback)
    return max(1, max(counts))


def _load_json_dict(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError, json.JSONDecodeError):
        return None
    if isinstance(data, dict):
        return data
    return None


def _load_worker_truth_model(path: Path) -> Optional[Dict[str, Any]]:
    return _load_json_dict(path)


def _apply_full_worker_engine_behavior(
    full_behavior: Dict[str, Any],
    params: Dict[str, WorkTimeParams],
    speeds: Dict[str, int],
    camper_ranges: Dict[str, int],
    worktime_base: int,
    threshold_work: int,
    force_to_work_penalty: float,
    global_camper_range: int,
) -> Tuple[int, int, float, int]:
    runtime = full_behavior.get("runtime") or {}
    global_worktime = runtime.get("global_worktime") or {}
    if not global_worktime:
        global_worktime = (full_behavior.get("global_logic") or {}).get("worktime") or {}

    worktime_base = _safe_int(global_worktime.get("base"), worktime_base)
    threshold_work = _safe_int(global_worktime.get("threshold_work"), threshold_work)
    force_to_work_penalty = _safe_float(
        global_worktime.get("force_to_work_penalty"), force_to_work_penalty
    )

    workers = runtime.get("workers") or {}
    if not isinstance(workers, dict):
        return worktime_base, threshold_work, force_to_work_penalty, global_camper_range

    for raw_name, worker_data in workers.items():
        if not isinstance(worker_data, dict):
            continue
        env_name = worker_data.get("env_name") or raw_name
        worker_name = normalize_worker_type(str(env_name))
        if not worker_name:
            continue

        speed = _safe_int(worker_data.get("speed"), speeds.get(worker_name, 320))
        if speed > 0:
            speeds[worker_name] = speed

        camper = _safe_int(worker_data.get("camper_range"), global_camper_range)
        if camper > 0:
            if camper == global_camper_range:
                camper_ranges.pop(worker_name, None)
            else:
                camper_ranges[worker_name] = camper

        if not worker_data.get("has_worktime", False):
            continue

        current = params.get(worker_name, WorkTimeParams())
        worktime = worker_data.get("worktime") or {}
        changes_per_cycle = _safe_int(
            worker_data.get("worktime_changes_per_cycle"),
            current.worktime_changes_per_cycle,
        )

        params[worker_name] = WorkTimeParams(
            work_wait_until=_safe_int(worktime.get("work_wait_until"), current.work_wait_until),
            eat_wait=_safe_int(worktime.get("eat_wait"), current.eat_wait),
            rest_wait=_safe_int(worktime.get("rest_wait"), current.rest_wait),
            work_time_change_work=_safe_int(
                worktime.get("work_time_change_work"), current.work_time_change_work
            ),
            work_time_change_farm=_safe_float(
                worktime.get("work_time_change_farm"), current.work_time_change_farm
            ),
            work_time_change_residence=_safe_float(
                worktime.get("work_time_change_residence"), current.work_time_change_residence
            ),
            work_time_change_camp=_safe_float(
                worktime.get("work_time_change_camp"), current.work_time_change_camp
            ),
            work_time_max_farm=_safe_int(
                worktime.get("work_time_max_farm"), current.work_time_max_farm
            ),
            work_time_max_residence=_safe_int(
                worktime.get("work_time_max_residence"), current.work_time_max_residence
            ),
            exhausted_malus=_safe_float(
                worktime.get("exhausted_malus"), current.exhausted_malus
            ),
            worktime_changes_per_cycle=max(1, changes_per_cycle),
        )

    return worktime_base, threshold_work, force_to_work_penalty, global_camper_range


def _build_runtime_worker_config(
    worker_truth_model: Optional[Dict[str, Any]],
    full_worker_behavior: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Baut Runtime-Config aus Original-Extracts mit sicheren Defaults."""
    params = _clone_worktime_params_map(DEFAULT_WORKER_PARAMS)
    speeds = dict(DEFAULT_WORKER_SPEEDS)
    camper_ranges = dict(DEFAULT_WORKER_CAMPER_RANGE)

    worktime_base = DEFAULT_WORKTIME_BASE
    threshold_work = DEFAULT_WORKTIME_THRESHOLD_WORK
    force_to_work_penalty = DEFAULT_FORCE_TO_WORK_PENALTY
    global_camper_range = DEFAULT_CAMPER_RANGE

    source = "defaults"
    if not worker_truth_model and not full_worker_behavior:
        return {
            "source": source,
            "params": params,
            "speeds": speeds,
            "camper_ranges": camper_ranges,
            "worktime_base": worktime_base,
            "threshold_work": threshold_work,
            "force_to_work_penalty": force_to_work_penalty,
            "camper_range": global_camper_range,
        }

    if worker_truth_model:
        source = "worker_truth_model"
        global_truth = worker_truth_model.get("global_truth") or {}
        logic_worktime = global_truth.get("logic_worktime") or {}

        worktime_base = _safe_int(logic_worktime.get("base"), worktime_base)
        threshold_work = _safe_int(logic_worktime.get("threshold_work"), threshold_work)
        force_to_work_penalty = _safe_float(
            logic_worktime.get("force_to_work_penalty"), force_to_work_penalty
        )

        workers = worker_truth_model.get("workers") or {}
        if isinstance(workers, dict):
            for raw_name, worker_data in workers.items():
                if not isinstance(worker_data, dict):
                    continue

                env_name = worker_data.get("env_name") or raw_name
                worker_name = normalize_worker_type(str(env_name))
                if not worker_name:
                    continue

                movement = worker_data.get("movement") or {}
                speed = _safe_int(movement.get("speed"), speeds.get(worker_name, 320))
                if speed > 0:
                    speeds[worker_name] = speed

                camper = _safe_int(movement.get("camper_range"), global_camper_range)
                if camper > 0:
                    if camper == global_camper_range:
                        camper_ranges.pop(worker_name, None)
                    else:
                        camper_ranges[worker_name] = camper

                if not worker_data.get("has_worktime", False):
                    continue

                current = params.get(worker_name, WorkTimeParams())
                worktime = worker_data.get("worktime_truth") or {}
                changes_per_cycle = _extract_worktime_changes_per_cycle(
                    worker_data, current.worktime_changes_per_cycle
                )

                params[worker_name] = WorkTimeParams(
                    work_wait_until=_safe_int(worktime.get("work_wait_until"), current.work_wait_until),
                    eat_wait=_safe_int(worktime.get("eat_wait"), current.eat_wait),
                    rest_wait=_safe_int(worktime.get("rest_wait"), current.rest_wait),
                    work_time_change_work=_safe_int(
                        worktime.get("work_time_change_work"), current.work_time_change_work
                    ),
                    work_time_change_farm=_safe_float(
                        worktime.get("work_time_change_farm"), current.work_time_change_farm
                    ),
                    work_time_change_residence=_safe_float(
                        worktime.get("work_time_change_residence"), current.work_time_change_residence
                    ),
                    work_time_change_camp=_safe_float(
                        worktime.get("work_time_change_camp"), current.work_time_change_camp
                    ),
                    work_time_max_farm=_safe_int(
                        worktime.get("work_time_max_farm"), current.work_time_max_farm
                    ),
                    work_time_max_residence=_safe_int(
                        worktime.get("work_time_max_residence"), current.work_time_max_residence
                    ),
                    exhausted_malus=_safe_float(
                        worktime.get("exhausted_malus"), current.exhausted_malus
                    ),
                    worktime_changes_per_cycle=changes_per_cycle,
                )

    if full_worker_behavior:
        source = "full_worker_engine_behavior"
        (
            worktime_base,
            threshold_work,
            force_to_work_penalty,
            global_camper_range,
        ) = _apply_full_worker_engine_behavior(
            full_worker_behavior,
            params,
            speeds,
            camper_ranges,
            worktime_base,
            threshold_work,
            force_to_work_penalty,
            global_camper_range,
        )

    return {
        "source": source,
        "params": params,
        "speeds": speeds,
        "camper_ranges": camper_ranges,
        "worktime_base": worktime_base,
        "threshold_work": threshold_work,
        "force_to_work_penalty": force_to_work_penalty,
        "camper_range": global_camper_range,
    }


_WORKER_TRUTH_MODEL_PATH = Path(__file__).resolve().parent / "config" / "worker_truth_model.json"
_FULL_WORKER_ENGINE_BEHAVIOR_PATH = (
    Path(__file__).resolve().parent / "config" / "full_worker_engine_behavior.json"
)
_WORKER_RUNTIME_CONFIG = _build_runtime_worker_config(
    _load_worker_truth_model(_WORKER_TRUTH_MODEL_PATH),
    _load_json_dict(_FULL_WORKER_ENGINE_BEHAVIOR_PATH),
)

# Runtime-Werte (Voll-Engine-Extract bevorzugt, Truth-Modell/Defaults als Fallback)
WORKER_CONFIG_SOURCE = _WORKER_RUNTIME_CONFIG["source"]
WORKER_PARAMS = _WORKER_RUNTIME_CONFIG["params"]
WORKER_SPEEDS = _WORKER_RUNTIME_CONFIG["speeds"]
WORKER_CAMPER_RANGE = _WORKER_RUNTIME_CONFIG["camper_ranges"]
WORKTIME_BASE = _WORKER_RUNTIME_CONFIG["worktime_base"]
WORKTIME_THRESHOLD_WORK = _WORKER_RUNTIME_CONFIG["threshold_work"]
FORCE_TO_WORK_PENALTY = _WORKER_RUNTIME_CONFIG["force_to_work_penalty"]

CAMPER_RANGE = _WORKER_RUNTIME_CONFIG["camper_range"]
WORK_TIME_BASE = WORKTIME_BASE
WORK_TIME_THRESHOLD_WORK = WORKTIME_THRESHOLD_WORK
WORK_TIME_START = WORK_TIME_BASE


def _tasklist_file_name(tasklist_name: Any) -> str:
    name = str(tasklist_name or "").strip().lower()
    if not name:
        return ""
    return name if name.endswith(".xml") else f"{name}.xml"


def _point_from_task_args(args: Dict[str, Any]) -> Optional[Tuple[float, float]]:
    point = args.get("Position") if isinstance(args, dict) else None
    if not isinstance(point, dict):
        return None
    try:
        return float(point.get("X", point.get("x", 0))), float(point.get("Y", point.get("y", 0)))
    except (TypeError, ValueError):
        return None


def _load_original_worker_routes(full_behavior: Optional[Dict[str, Any]]) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """Extrahiert Supplier-Starts und lokale TASK_GO_TO_POS-Routen aus den Original-TaskLists."""
    routes_by_building: Dict[str, Dict[str, Any]] = {}
    routes_by_worker: Dict[str, Dict[str, Any]] = {}
    if not isinstance(full_behavior, dict):
        return routes_by_building, routes_by_worker

    tasklists = full_behavior.get("tasklists") or {}
    worker_buildings = full_behavior.get("worker_buildings") or {}
    if not isinstance(tasklists, dict) or not isinstance(worker_buildings, dict):
        return routes_by_building, routes_by_worker

    def aliases_for_entity(entity_name: str) -> List[str]:
        aliases = [entity_name]
        try:
            from original_game_values import aliases_for_building_entity
            aliases.extend(aliases_for_building_entity(entity_name))
        except Exception:
            pass
        return list(dict.fromkeys(str(alias) for alias in aliases if alias))

    def extract_route(start_name: str, work_name: str) -> Dict[str, Any]:
        start_file = _tasklist_file_name(start_name)
        work_file = _tasklist_file_name(work_name)
        start_tl = tasklists.get(start_file) if start_file else None
        work_tl = tasklists.get(work_file) if work_file else None

        start_tasks = start_tl.get("tasks") if isinstance(start_tl, dict) else []
        work_tasks = work_tl.get("tasks") if isinstance(work_tl, dict) else []
        requires_supplier = any(
            task.get("task_type") == "TASK_GO_TO_SUPPLIER"
            for task in (start_tasks or [])
            if isinstance(task, dict)
        )

        start_offset: Optional[Tuple[float, float]] = None
        waypoints: List[Tuple[float, float]] = []
        refine_ops = 0
        worktime_changes = 0
        for task in (work_tasks or []):
            if not isinstance(task, dict):
                continue
            task_type = task.get("task_type")
            args = task.get("args") or {}
            if task_type == "TASK_SET_POS" and start_offset is None:
                start_offset = _point_from_task_args(args)
            elif task_type == "TASK_GO_TO_POS":
                point = _point_from_task_args(args)
                if point is not None:
                    waypoints.append(point)
            elif task_type in {"TASK_REFINE_RESOURCE", "TASK_MINED_RESOURCE"}:
                refine_ops += 1
            elif task_type == "TASK_CHANGE_WORK_TIME_WORK":
                worktime_changes += 1

        return {
            "start_tasklist": start_file,
            "work_tasklist": work_file,
            "requires_supplier": requires_supplier,
            "work_start_offset": start_offset,
            "work_route_offsets": tuple(waypoints),
            "resource_ops_per_cycle": max(1, refine_ops),
            "worktime_changes_per_cycle": max(1, worktime_changes),
        }

    for entity_name, building_data in worker_buildings.items():
        if not isinstance(building_data, dict):
            continue
        worker_name = normalize_worker_type(
            str(building_data.get("worker_env_name") or building_data.get("worker_type") or "")
        )
        work_pairs = building_data.get("work_tasklists") or []
        if not worker_name or not isinstance(work_pairs, list):
            continue

        chosen_route: Optional[Dict[str, Any]] = None
        for pair in work_pairs:
            if not isinstance(pair, dict):
                continue
            work_name = str(pair.get("Work") or "")
            # The *_INSIDE lists are non-visible fallbacks; prefer visible exterior/local routes.
            if "INSIDE" in work_name.upper() and len(work_pairs) > 1:
                continue
            chosen_route = extract_route(str(pair.get("Start") or ""), work_name)
            break
        if chosen_route is None and work_pairs:
            pair = work_pairs[0] if isinstance(work_pairs[0], dict) else {}
            chosen_route = extract_route(str(pair.get("Start") or ""), str(pair.get("Work") or ""))
        if chosen_route is None:
            continue

        chosen_route = dict(chosen_route)
        chosen_route["worker_type"] = worker_name
        chosen_route["building_entity"] = str(entity_name)

        for alias in aliases_for_entity(str(entity_name)):
            routes_by_building[alias] = dict(chosen_route)
        routes_by_worker.setdefault(worker_name, dict(chosen_route))

    return routes_by_building, routes_by_worker


_ORIGINAL_WORK_ROUTES_BY_BUILDING, _ORIGINAL_WORK_ROUTES_BY_WORKER = _load_original_worker_routes(
    _load_json_dict(_FULL_WORKER_ENGINE_BEHAVIOR_PATH)
)


def get_original_work_route(building_type: str, worker_type: str = "") -> Optional[Dict[str, Any]]:
    """Liefert die Original-Supplier-/Arbeitsroute fuer ein Sim-Gebaeude."""
    candidates = []
    if building_type:
        candidates.append(str(building_type))
        base = str(building_type).rsplit("_", 1)
        if len(base) == 2 and base[1].isdigit():
            candidates.append(base[0])
    for candidate in candidates:
        route = _ORIGINAL_WORK_ROUTES_BY_BUILDING.get(candidate)
        if route:
            return dict(route)

    normalized_worker = normalize_worker_type(worker_type)
    if normalized_worker:
        route = _ORIGINAL_WORK_ROUTES_BY_WORKER.get(normalized_worker)
        if route:
            return dict(route)
    return None


@dataclass
class Farm:
    """Bauernhof fÃ¼r Essen."""
    position: Position
    level: int = 1
    current_eaters: int = 0
    capacity_bonus: int = 0
    has_farmer: bool = True
    approach_offset: Optional[Position] = None
    door_offset: Optional[Position] = None
    leave_offset: Optional[Position] = None

    @property
    def eat_capacity(self) -> int:
        """Essen-KapazitÃ¤t nach Level."""
        base = {1: 8, 2: 10, 3: 12}.get(self.level, 8)
        return max(1, base + self.capacity_bonus)

    def has_space(self) -> bool:
        return self.current_eaters < self.eat_capacity

    def _with_offset(self, offset: Optional[Position]) -> Position:
        if offset is None:
            return Position(x=self.position.x, y=self.position.y)
        return Position(x=self.position.x + offset.x, y=self.position.y + offset.y)

    def approach_position(self) -> Position:
        """Original-ApproachPos als Laufziel, Fallback auf Gebaeudezentrum."""
        return self._with_offset(self.approach_offset)

    def door_position(self) -> Position:
        return self._with_offset(self.door_offset)

    def leave_position(self) -> Position:
        return self._with_offset(self.leave_offset)


@dataclass
class Residence:
    """Wohnhaus fÃ¼r Ruhen."""
    position: Position
    level: int = 1
    current_residents: int = 0
    capacity_bonus: int = 0
    approach_offset: Optional[Position] = None
    door_offset: Optional[Position] = None
    leave_offset: Optional[Position] = None

    @property
    def live_capacity(self) -> int:
        """Wohn-KapazitÃ¤t nach Level."""
        base = {1: 6, 2: 9, 3: 12}.get(self.level, 6)
        return max(1, base + self.capacity_bonus)

    def has_space(self) -> bool:
        return self.current_residents < self.live_capacity

    def _with_offset(self, offset: Optional[Position]) -> Position:
        if offset is None:
            return Position(x=self.position.x, y=self.position.y)
        return Position(x=self.position.x + offset.x, y=self.position.y + offset.y)

    def approach_position(self) -> Position:
        """Original-ApproachPos als Laufziel, Fallback auf Gebaeudezentrum."""
        return self._with_offset(self.approach_offset)

    def door_position(self) -> Position:
        return self._with_offset(self.door_offset)

    def leave_position(self) -> Position:
        return self._with_offset(self.leave_offset)


@dataclass
class Camp:
    """Dynamisch gespawntes Notfall-Camp (wie XD_Camp_Internal im Spiel).
    Bis zu CAMP_MAX_SLOTS Worker teilen sich ein Camp.
    Verschwindet CAMP_REMOVE_DELAY Sekunden nach dem letzten Worker."""
    position: Position
    current_occupants: int = 0      # Aktuelle Worker im Camp
    idle_time: float = 0.0          # Sekunden seit letztem Occupant (fuer Remove-Delay)
    slot_occupied: List[bool] = field(default_factory=list)

    def __post_init__(self):
        if not self.slot_occupied:
            occupied = min(CAMP_MAX_SLOTS, max(0, int(self.current_occupants)))
            self.slot_occupied = [index < occupied for index in range(CAMP_MAX_SLOTS)]
        elif len(self.slot_occupied) < CAMP_MAX_SLOTS:
            self.slot_occupied.extend([False] * (CAMP_MAX_SLOTS - len(self.slot_occupied)))
        self.current_occupants = sum(1 for slot in self.slot_occupied if slot)

    def has_space(self) -> bool:
        return self.current_occupants < CAMP_MAX_SLOTS and any(not used for used in self.slot_occupied)

    def assign_slot(self) -> Optional[int]:
        for index, used in enumerate(self.slot_occupied):
            if not used:
                self.slot_occupied[index] = True
                self.current_occupants = sum(1 for slot in self.slot_occupied if slot)
                self.idle_time = 0.0
                return index
        return None

    def release_slot(self, slot_index: Optional[int]):
        if slot_index is not None and 0 <= slot_index < len(self.slot_occupied):
            self.slot_occupied[slot_index] = False
        self.current_occupants = sum(1 for slot in self.slot_occupied if slot)

    def slot_position(self, slot_index: Optional[int]) -> Position:
        if slot_index is None or not (0 <= slot_index < len(CAMP_SLOT_OFFSETS)):
            return Position(x=self.position.x, y=self.position.y)
        offset = CAMP_SLOT_OFFSETS[slot_index]
        return Position(x=self.position.x + offset.x, y=self.position.y + offset.y)

CAMP_MAX_SLOTS: int = 8            # XD_Camp_Internal hat 8 Slots
CAMP_REMOVE_DELAY: float = 10.0    # Sekunden bis Camp verschwindet (aus Spieldaten)
CAMP_SLOT_OFFSETS: Tuple[Position, ...] = (
    Position(-198, -185),
    Position(-6, -230),
    Position(151, -114),
    Position(174, 31),
    Position(119, 127),
    Position(-61, 156),
    Position(-188, 111),
    Position(-288, -70),
)


@dataclass
class Worker:
    """
    Simuliert einen einzelnen Arbeiter mit WorkTime und Pausen-Laufwegen.

    WICHTIG: Serfs haben KEIN WorkTime-System und werden separat behandelt!
    """
    worker_type: str
    position: Position
    workplace_position: Position
    work_time: float = WORK_TIME_START
    state: WorkerState = WorkerState.IDLE
    state_timer: float = 0.0  # in Sekunden
    target_position: Optional[Position] = None
    assigned_farm: Optional[Farm] = None
    assigned_residence: Optional[Residence] = None
    jobless_time_ms: float = 0.0
    camp_next_state: Optional[str] = None
    path: List[Position] = field(default_factory=list)
    path_index: int = 0
    final_destination: Optional[Position] = None
    path_revision: int = -1
    path_blocked: bool = False
    supplier_position: Optional[Position] = None
    requires_supplier_trip: bool = False
    supplier_stock_loaded: bool = False
    work_start_offset: Optional[Position] = None
    work_route_offsets: List[Position] = field(default_factory=list)
    work_route: List[Position] = field(default_factory=list)
    work_route_index: int = 0
    work_route_initialized: bool = False
    workplace_orientation: float = 0.0
    assigned_camp_slot: Optional[int] = None

    def __post_init__(self):
        """Initialisiert Worker-spezifische Parameter."""
        self.worker_type = normalize_worker_type(self.worker_type)
        self.params = WORKER_PARAMS.get(self.worker_type, WorkTimeParams())
        self.speed = WORKER_SPEEDS.get(self.worker_type, 320)
        self.has_worktime_system = self.worker_type != "serf"

    def configure_original_work_cycle(
        self,
        route: Optional[Dict[str, Any]] = None,
        supplier_position: Optional[Position] = None,
        workplace_orientation: Optional[float] = None,
    ):
        """Konfiguriert Supplier-Lauf und lokale Arbeitsroute aus Original-TaskLists."""
        if supplier_position is not None:
            self.supplier_position = Position(x=supplier_position.x, y=supplier_position.y)
        if workplace_orientation is not None:
            try:
                self.workplace_orientation = float(workplace_orientation)
            except (TypeError, ValueError):
                self.workplace_orientation = 0.0

        if not route:
            return

        self.requires_supplier_trip = bool(route.get("requires_supplier"))
        start_offset = route.get("work_start_offset")
        if isinstance(start_offset, (list, tuple)) and len(start_offset) == 2:
            self.work_start_offset = Position(x=float(start_offset[0]), y=float(start_offset[1]))

        offsets: List[Position] = []
        for point in route.get("work_route_offsets") or []:
            if isinstance(point, (list, tuple)) and len(point) == 2:
                offsets.append(Position(x=float(point[0]), y=float(point[1])))
        self.work_route_offsets = offsets

    def tick(self, dt: float, farms: List[Farm], residences: List[Residence], camps: List[Camp],
             motivation_mod: float = 1.0, speed_bonus: int = 0,
             speed_multiplier: float = 1.0,
             pathfinder: Optional[Callable[[Position, Position], List[Position]]] = None,
             path_revision: Optional[int] = None,
             spawn_camp_fn=None, camper_range: float = None):
        # Speed-Bonus als Instanzvariable speichern fÃ¼r _tick_walking
        self._speed_bonus = speed_bonus
        self._speed_multiplier = max(0.01, float(speed_multiplier))
        self._last_camps = camps
        self._pathfinder = pathfinder
        self._path_revision = path_revision
        self._motivation_mod = motivation_mod
        self._spawn_camp_fn = spawn_camp_fn
        if camper_range is not None:
            self._camper_range = camper_range
        """
        Simuliert einen Zeitschritt.

        Args:
            dt: Delta-Zeit in Sekunden
            farms: Liste aller Farms
            residences: Liste aller WohnhÃ¤user
            camps: Liste aller Camps
            motivation_mod: Motivation-Modifier fÃ¼r Regeneration (1.0 = normal)
        """
        if not self.has_worktime_system:
            # Serfs arbeiten ENDLOS ohne Pausen!
            self.state = WorkerState.WORKING
            return

        if self.state == WorkerState.WORKING:
            self._tick_working(dt, farms)

        elif self.state == WorkerState.WALKING_TO_SUPPLIER:
            if self._tick_walking(dt, WorkerState.WALKING_FROM_SUPPLIER_TO_WORK):
                self._start_return_from_supplier()

        elif self.state == WorkerState.WALKING_FROM_SUPPLIER_TO_WORK:
            self._tick_walking(dt, WorkerState.WORKING)

        elif self.state == WorkerState.WALKING_TO_FARM:
            self._tick_walking(dt, WorkerState.EATING)

        elif self.state == WorkerState.EATING:
            self._tick_eating(dt, residences, motivation_mod)

        elif self.state == WorkerState.WALKING_TO_RESIDENCE:
            self._tick_walking(dt, WorkerState.RESTING)

        elif self.state == WorkerState.RESTING:
            self._tick_resting(dt, motivation_mod)

        elif self.state == WorkerState.WALKING_TO_CAMP:
            self._tick_walking(dt, WorkerState.CAMPING)

        elif self.state == WorkerState.CAMPING:
            self._tick_camping(dt, residences, motivation_mod)

        elif self.state == WorkerState.WALKING_TO_WORK:
            self._tick_walking(dt, WorkerState.WORKING)

        elif self.state == WorkerState.IDLE:
            # Idle Worker starten Arbeit
            self.state = WorkerState.WORKING
            self.state_timer = 0.0

    def _tick_working(self, dt: float, farms: List[Farm]):
        """Arbeits-Phase."""
        if self._needs_supplier_trip():
            if self._start_supplier_trip():
                return

        self.state_timer += dt * 1000  # ms

        # WorkTime sinkt kontinuierlich
        work_progress = (dt * 1000) / self.params.work_wait_until
        self.work_time += self.params.work_time_change_work * self.params.worktime_changes_per_cycle * work_progress

        self._ensure_work_route_started()
        self._advance_work_route(dt)

        # Hunger-Check: Nach einem Arbeitszyklus oder wenn WorkTime niedrig
        mot = max(0.1, getattr(self, "_motivation_mod", 1.0))
        max_farm = self.params.work_time_max_farm * mot
        threshold_farm = WORK_TIME_THRESHOLD_WORK + (
            (max_farm - WORK_TIME_THRESHOLD_WORK) * WORK_TIME_THRESHOLD_FARM
        )
        if self.state_timer >= self.params.work_wait_until or self.work_time <= threshold_farm:
            self._reset_work_cycle_for_next_cycle()
            self._find_farm(farms)
            self.state_timer = 0.0

    def _tick_eating(self, dt: float, residences: List[Residence], motivation_mod: float = 1.0):
        """Essen-Phase."""
        self.state_timer += dt * 1000  # ms

        if self.state_timer >= self.params.eat_wait:
            # WorkTime regenerieren: +70% von (Max - Aktuell) Ã— Motivation
            mot = max(0.1, getattr(self, "_motivation_mod", 1.0))
            max_val = self.params.work_time_max_farm * mot
            regen_rate = self.params.work_time_change_farm * motivation_mod
            self.work_time += regen_rate * (max_val - self.work_time)

            # Farm freigeben
            if self.assigned_farm:
                self.assigned_farm.current_eaters -= 1
                self.assigned_farm = None

            # NÃ¤chstes: Wohnhaus suchen (nur wenn WorkTime niedrig genug)
            max_res = self.params.work_time_max_residence * mot
            threshold_res = WORK_TIME_THRESHOLD_WORK + (
                (max_res - WORK_TIME_THRESHOLD_WORK) * WORK_TIME_THRESHOLD_RESIDENCE
            )
            if self.work_time <= threshold_res:
                self._find_residence(residences)
            else:
                self._return_to_work()
            self.state_timer = 0.0

    def _tick_resting(self, dt: float, motivation_mod: float = 1.0):
        """Ruhe-Phase."""
        self.state_timer += dt * 1000  # ms

        if self.state_timer >= self.params.rest_wait:
            # WorkTime regenerieren: +50% von (Max - Aktuell) Ã— Motivation
            mot = max(0.1, getattr(self, "_motivation_mod", 1.0))
            max_val = self.params.work_time_max_residence * mot
            regen_rate = self.params.work_time_change_residence * motivation_mod
            self.work_time += regen_rate * (max_val - self.work_time)

            # Wohnhaus freigeben
            if self.assigned_residence:
                self.assigned_residence.current_residents -= 1
                self.assigned_residence = None

            # ZurÃ¼ck zur Arbeit
            self._return_to_work()
            self.state_timer = 0.0

    def _tick_camping(self, dt: float, residences: List[Residence], motivation_mod: float = 1.0):
        """Camping-Phase (Notfall - nur +10% Regeneration)."""
        self.state_timer += dt * 1000  # ms

        # Camping dauert so lange wie Essen + Ruhen zusammen
        camp_duration = self.params.eat_wait + self.params.rest_wait

        if self.state_timer >= camp_duration:
            # Nur +10% Regeneration Ã— Motivation
            mot = max(0.1, getattr(self, "_motivation_mod", 1.0))
            max_val = self.params.work_time_max_farm * mot
            regen_rate = self.params.work_time_change_camp * motivation_mod
            self.work_time += regen_rate * (max_val - self.work_time)

            # Camp-Slot freigeben
            assigned = getattr(self, "_assigned_camp", None)
            if assigned is not None:
                assigned.release_slot(self.assigned_camp_slot)
                self._assigned_camp = None
                self.assigned_camp_slot = None

            # Camp ersetzt fehlende Phase(n)
            next_state = self.camp_next_state or "work"
            self.camp_next_state = None
            if next_state == "residence":
                self._find_residence(residences)
            else:
                self._return_to_work()
            self.state_timer = 0.0

    def _needs_supplier_trip(self) -> bool:
        return (
            self.requires_supplier_trip
            and self.supplier_position is not None
            and not self.supplier_stock_loaded
        )

    def _start_supplier_trip(self) -> bool:
        if self.supplier_position is None:
            self.supplier_stock_loaded = True
            return False
        self.work_route_initialized = False
        self.work_route = []
        self.work_route_index = 0
        self._set_target(self.supplier_position)
        self.state = WorkerState.WALKING_TO_SUPPLIER
        return True

    def _start_return_from_supplier(self):
        self.supplier_stock_loaded = True
        self._set_target(self.workplace_position)
        self.state = WorkerState.WALKING_FROM_SUPPLIER_TO_WORK

    def _absolute_work_point(self, offset: Position) -> Position:
        # Original TASK_GO_TO_POS offsets are relative to the oriented building origin.
        angle = math.radians(float(getattr(self, "workplace_orientation", 0.0) or 0.0))
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        rotated_x = offset.x * cos_a - offset.y * sin_a
        rotated_y = offset.x * sin_a + offset.y * cos_a
        return Position(x=self.workplace_position.x + rotated_x, y=self.workplace_position.y + rotated_y)

    def _ensure_work_route_started(self):
        if self.work_route_initialized:
            return
        self.work_route_initialized = True
        if self.work_start_offset is not None:
            self.position = self._absolute_work_point(self.work_start_offset)
        self.work_route = [self._absolute_work_point(point) for point in self.work_route_offsets]
        self.work_route_index = 0
        while self.work_route_index < len(self.work_route):
            if self.position.distance_to(self.work_route[self.work_route_index]) > 1.0:
                break
            self.work_route_index += 1

    def _advance_work_route(self, dt: float):
        if self.work_route_index >= len(self.work_route):
            return
        effective_speed = max(
            1.0,
            (self.speed + getattr(self, '_speed_bonus', 0))
            * getattr(self, "_speed_multiplier", 1.0),
        )
        remaining = effective_speed * dt
        epsilon = 1e-6
        while remaining > epsilon and self.work_route_index < len(self.work_route):
            target = self.work_route[self.work_route_index]
            distance = self.position.distance_to(target)
            if distance <= epsilon:
                self.position = Position(target.x, target.y)
                self.work_route_index += 1
                continue
            if remaining >= distance:
                self.position = Position(target.x, target.y)
                remaining -= distance
                self.work_route_index += 1
                continue
            ratio = remaining / distance
            self.position.x += ratio * (target.x - self.position.x)
            self.position.y += ratio * (target.y - self.position.y)
            remaining = 0.0

    def _reset_work_cycle_for_next_cycle(self):
        self.supplier_stock_loaded = False
        self.work_route_initialized = False
        self.work_route = []
        self.work_route_index = 0

    def is_work_cycle_active(self) -> bool:
        return self.state in {
            WorkerState.WORKING,
            WorkerState.WALKING_TO_SUPPLIER,
            WorkerState.WALKING_FROM_SUPPLIER_TO_WORK,
        }

    def get_work_cycle_efficiency(self) -> float:
        if not self.has_worktime_system:
            return 1.0
        if not self.is_work_cycle_active():
            return 0.0
        if self.work_time <= EXHAUSTED_THRESHOLD:
            return self.params.exhausted_malus
        return 1.0

    def _tick_walking(self, dt: float, next_state: WorkerState) -> bool:
        """Lauf-Phase."""
        self._maybe_repath()
        if self.path_blocked and self.target_position is None:
            return False
        if self.target_position is None:
            self.state = next_state
            return True

        effective_speed = max(
            1.0,
            (self.speed + getattr(self, '_speed_bonus', 0))
            * getattr(self, "_speed_multiplier", 1.0),
        )
        remaining = effective_speed * dt
        epsilon = 1e-6

        # Verbraucht die komplette Bewegungsdistanz im Tick (wichtig bei dt=1s).
        while remaining > epsilon and self.target_position is not None:
            distance = self.position.distance_to(self.target_position)

            if distance <= epsilon:
                self.position = Position(self.target_position.x, self.target_position.y)
                if self.path and self.path_index + 1 < len(self.path):
                    self.path_index += 1
                    self.target_position = self.path[self.path_index]
                    continue
                self.target_position = None
                self.path = []
                self.path_index = 0
                self.final_destination = None
                self.path_blocked = False
                self.state = next_state
                self.state_timer = 0.0
                return True

            if remaining >= distance:
                self.position = Position(self.target_position.x, self.target_position.y)
                remaining -= distance
                if self.path and self.path_index + 1 < len(self.path):
                    self.path_index += 1
                    self.target_position = self.path[self.path_index]
                    continue
                self.target_position = None
                self.path = []
                self.path_index = 0
                self.final_destination = None
                self.path_blocked = False
                self.state = next_state
                self.state_timer = 0.0
                return True

            ratio = remaining / distance
            self.position.x += ratio * (self.target_position.x - self.position.x)
            self.position.y += ratio * (self.target_position.y - self.position.y)
            remaining = 0.0
        return False

    def _get_camper_range(self) -> int:
        """Gibt die Worker-spezifische CamperRange zurueck."""
        return WORKER_CAMPER_RANGE.get(self.worker_type, CAMPER_RANGE)

    @staticmethod
    def _path_length(path: List[Position]) -> float:
        """Approximate path length for candidate selection."""
        if not path:
            return float("inf")
        if len(path) == 1:
            return 0.0
        length = 0.0
        prev = path[0]
        for current in path[1:]:
            length += prev.distance_to(current)
            prev = current
        return length

    def _find_farm(self, farms: List[Farm]):
        """Findet naechsten Bauernhof in Worker-spezifischer CAMPER_RANGE."""
        camper_range = self._get_camper_range()
        pathfinder = getattr(self, "_pathfinder", None)

        # Schritt 1: Filter + Euclidean-Sort, nur Top-5 Kandidaten fuer A*
        candidates = []
        for farm in farms:
            if not (farm.has_farmer and farm.has_space()):
                continue
            dist = self.position.distance_to(farm.position)
            if dist < camper_range:
                candidates.append((dist, farm))
        candidates.sort(key=lambda x: x[0])
        candidates = candidates[:5]  # Nur Top-5 per Euclidean-Distanz an A* weitergeben

        nearest = None
        min_path_cost = float("inf")
        min_dist = camper_range

        for dist, farm in candidates:
            path_cost = dist
            target = farm.approach_position()
            if pathfinder:
                try:
                    path = pathfinder(self.position, target) or []
                except Exception:
                    path = []
                if not path:
                    continue
                path_cost = self._path_length(path)

            if (
                nearest is None
                or path_cost < min_path_cost
                or (abs(path_cost - min_path_cost) <= 1e-6 and dist < min_dist)
            ):
                nearest = farm
                min_dist = dist
                min_path_cost = path_cost

        if nearest:
            self._set_target(nearest.approach_position())
            self.state = WorkerState.WALKING_TO_FARM
            self.assigned_farm = nearest
            nearest.current_eaters += 1
        else:
            # Kein Bauernhof in Reichweite -> Camp suchen
            self.camp_next_state = "residence"
            self._go_to_camp()

    def _find_residence(self, residences: List[Residence]):
        """Findet naechstes Wohnhaus in Worker-spezifischer CAMPER_RANGE."""
        camper_range = self._get_camper_range()
        pathfinder = getattr(self, "_pathfinder", None)

        # Schritt 1: Filter + Euclidean-Sort, nur Top-5 Kandidaten fuer A*
        candidates = []
        for residence in residences:
            if not residence.has_space():
                continue
            dist = self.position.distance_to(residence.position)
            if dist < camper_range:
                candidates.append((dist, residence))
        candidates.sort(key=lambda x: x[0])
        candidates = candidates[:5]  # Nur Top-5 per Euclidean-Distanz an A* weitergeben

        nearest = None
        min_path_cost = float("inf")
        min_dist = camper_range

        for dist, residence in candidates:
            path_cost = dist
            target = residence.approach_position()
            if pathfinder:
                try:
                    path = pathfinder(self.position, target) or []
                except Exception:
                    path = []
                if not path:
                    continue
                path_cost = self._path_length(path)

            if (
                nearest is None
                or path_cost < min_path_cost
                or (abs(path_cost - min_path_cost) <= 1e-6 and dist < min_dist)
            ):
                nearest = residence
                min_dist = dist
                min_path_cost = path_cost

        if nearest:
            self._set_target(nearest.approach_position())
            self.state = WorkerState.WALKING_TO_RESIDENCE
            self.assigned_residence = nearest
            nearest.current_residents += 1
        else:
            # Kein Wohnhaus in Reichweite -> Camp suchen
            self.camp_next_state = "work"
            self._go_to_camp()

    def _go_to_camp(self):
        """Geht zum naechsten Camp oder spawnt ein neues am Arbeitsplatz."""
        camps = getattr(self, "_last_camps", None) or []
        camper_range = getattr(self, "_camper_range", CAMPER_RANGE)

        # Bestehendes Camp mit freiem Slot suchen (innerhalb Camper-Range)
        best_camp = None
        best_dist = float("inf")
        for camp in camps:
            dist = self.position.distance_to(camp.position)
            if dist <= camper_range and camp.has_space():
                if dist < best_dist:
                    best_dist = dist
                    best_camp = camp

        if best_camp is not None:
            slot = best_camp.assign_slot()
            self._assigned_camp = best_camp
            self.assigned_camp_slot = slot
            self._set_target(best_camp.slot_position(slot))
        else:
            # Neues Camp am Arbeitsplatz spawnen (wie im echten Spiel)
            spawn_fn = getattr(self, "_spawn_camp_fn", None)
            new_camp = None
            if spawn_fn is not None:
                new_camp = spawn_fn(self.workplace_position)
            if new_camp is not None:
                slot = new_camp.assign_slot()
                self._assigned_camp = new_camp
                self.assigned_camp_slot = slot
                self._set_target(new_camp.slot_position(slot))
            else:
                # Fallback: direkt zum Arbeitsplatz (kein Camp-Objekt verfuegbar)
                self._assigned_camp = None
                self.assigned_camp_slot = None
                self._set_target(self.workplace_position)

        self.state = WorkerState.WALKING_TO_CAMP

    def _return_to_work(self):
        """Kehrt zum Arbeitsplatz zurÃ¼ck."""
        self.work_route_initialized = False
        self.work_route = []
        self.work_route_index = 0
        self._set_target(self.workplace_position)
        self.state = WorkerState.WALKING_TO_WORK

    def _set_target(self, target: Position):
        """Setzt Zielposition und optionalen Pfad."""
        self.final_destination = target
        self.target_position = target
        self.path = []
        self.path_index = 0
        self.path_blocked = False
        pathfinder = getattr(self, "_pathfinder", None)
        if pathfinder:
            try:
                path = pathfinder(self.position, target) or []
            except Exception:
                path = []
            if path:
                # Entferne Startknoten falls nahezu identisch
                if self.position.distance_to(path[0]) < 1.0:
                    path = path[1:]
            if path:
                self.path = path
                self.path_index = 0
                self.target_position = self.path[0]
            elif self.position.distance_to(target) > 1.0:
                # Kein valider Pfad verfuegbar: warten bis Repathing einen Weg findet.
                self.target_position = None
                self.path_blocked = True
        current_rev = getattr(self, "_path_revision", None)
        if current_rev is not None:
            self.path_revision = current_rev

    def _maybe_repath(self):
        """Aktualisiert den Pfad wenn sich die Umgebung geÃƒÂ¤ndert hat."""
        pathfinder = getattr(self, "_pathfinder", None)
        current_rev = getattr(self, "_path_revision", None)
        if not pathfinder or current_rev is None:
            return
        if self.final_destination is None:
            return
        if self.path_revision == current_rev:
            # Nur neu planen wenn sich die Umgebung geÃƒÂ¤ndert hat.
            return
        try:
            path = pathfinder(self.position, self.final_destination) or []
        except Exception:
            path = []
        if path and self.position.distance_to(path[0]) < 1.0:
            path = path[1:]
        if path:
            self.path = path
            self.path_index = 0
            self.target_position = self.path[0]
            self.path_blocked = False
        else:
            self.path = []
            self.path_index = 0
            if self.position.distance_to(self.final_destination) <= 1.0:
                self.target_position = self.final_destination
                self.path_blocked = False
            else:
                self.target_position = None
                self.path_blocked = True
        self.path_revision = current_rev

    def get_efficiency(self) -> float:
        """
        Berechnet aktuelle Effizienz basierend auf WorkTime und Zustand.

        Returns:
            0.0 - 1.0 (1.0 = volle Effizienz)
        """
        if not self.has_worktime_system:
            # Serfs haben immer 100% Effizienz (arbeiten endlos)
            return 1.0

        if self.state != WorkerState.WORKING:
            # Nicht arbeitend = keine Produktion
            return 0.0

        if self.work_time <= EXHAUSTED_THRESHOLD:
            # ErschÃ¶pft = nur 10% Effizienz
            return self.params.exhausted_malus

        # Volle Effizienz
        return 1.0

    def is_working(self) -> bool:
        """PrÃ¼ft ob Worker gerade arbeitet."""
        return self.state == WorkerState.WORKING

    def is_exhausted(self) -> bool:
        """PrÃ¼ft ob Worker erschÃ¶pft ist."""
        return self.work_time <= EXHAUSTED_THRESHOLD


@dataclass
class WorkforceManager:
    """
    Verwaltet alle Arbeiter mit KapazitÃ¤ten und Laufwegen.

    Trackt:
    - Alle Worker mit WorkTime-Status
    - Alle Farms mit Essen-KapazitÃ¤t
    - Alle WohnhÃ¤user mit Wohn-KapazitÃ¤t
    - Gesamt-Effizienz der Belegschaft
    """
    workers: List[Worker] = field(default_factory=list)
    farms: List[Farm] = field(default_factory=list)
    residences: List[Residence] = field(default_factory=list)
    camps: List[Camp] = field(default_factory=list)
    # Max Workers wird durch Dorfzentrum bestimmt (von environment gesetzt)
    max_workers_from_village: int = 0
    # NEU: Motivation-Modifier beeinflusst WorkTime-Regeneration
    motivation_modifier: float = 1.0
    # NEU: Speed-Bonus aus Technologie (T_Shoes: +20 fÃ¼r Worker/Serfs)
    speed_bonus: int = 0
    # Wetterfaktor aus Logic.xml, z.B. Schnee=0.85.
    speed_multiplier: float = 1.0
    # NEU: Segen Worker-Filter (nur gesegnete Typen bekommen Bonus)
    blessed_worker_types: set = field(default_factory=set)
    blessing_bonus: float = 0.0

    def set_motivation_modifier(self, motivation: float):
        """Setzt den globalen Motivation-Modifier fÃ¼r alle Worker.

        HÃ¶here Motivation = schnellere WorkTime-Regeneration.
        """
        self.motivation_modifier = motivation

    def set_speed_bonus(self, bonus: int):
        """Setzt den Speed-Bonus aus Technologien (z.B. T_Shoes +20)."""
        self.speed_bonus = bonus

    def set_speed_multiplier(self, multiplier: float):
        """Setzt den globalen Bewegungsfaktor aus Wettereffekten."""
        try:
            self.speed_multiplier = max(0.01, float(multiplier))
        except (TypeError, ValueError):
            self.speed_multiplier = 1.0

    def set_blessed_types(self, blessed_types: set, bonus: float):
        """Setzt die gesegneten Worker-Typen und den Bonus.

        Aus extra2/logic.xml: Segen wirkt NUR auf Worker der Kategorie!
        "ALL" = alle Worker (Canonisation).
        """
        self.blessed_worker_types = blessed_types
        self.blessing_bonus = bonus

    def _pos_key(self, pos: Position) -> Tuple[int, int]:
        return (int(round(pos.x)), int(round(pos.y)))

    def _update_farm_worker_flags(self):
        """Aktualisiert Farm-Flags: Nur Farms mit Farmer liefern Nahrung."""
        if not self.farms:
            return
        farms_by_pos = {self._pos_key(f.position): f for f in self.farms}
        for farm in self.farms:
            farm.has_farmer = False
        for worker in self.workers:
            if worker.worker_type == "farmer":
                key = self._pos_key(worker.workplace_position)
                farm = farms_by_pos.get(key)
                if farm:
                    farm.has_farmer = True

    def tick(self, dt: float, active_workplaces: Optional[set] = None,
             pathfinder: Optional[Callable[[Position, Position], List[Position]]] = None,
             path_revision: Optional[int] = None):
        """Simuliert alle Worker fÃ¼r einen Zeitschritt.

        active_workplaces: Set[(x,y)] von aktiven Arbeitsplatz-Positionen.
        """
        self._update_farm_worker_flags()

        # Dynamische Camps: Remove-Delay ticken, leere Camps entfernen
        active_camps: List[Camp] = []
        for camp in self.camps:
            if camp.current_occupants > 0:
                camp.idle_time = 0.0
                active_camps.append(camp)
            else:
                camp.idle_time += dt
                if camp.idle_time < CAMP_REMOVE_DELAY:
                    active_camps.append(camp)
                # sonst: Camp verschwindet (wie im echten Spiel nach 10s)
        self.camps = active_camps

        def _spawn_camp(position: Position) -> Camp:
            """Spawnt neues Camp an gegebener Position (wie XD_Camp_Internal)."""
            camp = Camp(position=Position(x=position.x, y=position.y))
            self.camps.append(camp)
            return camp

        survivors: List[Worker] = []
        for worker in self.workers:
            if active_workplaces is not None and worker.worker_type != "serf":
                key = self._pos_key(worker.workplace_position)
                if key not in active_workplaces:
                    worker.jobless_time_ms += dt * 1000
                    if worker.jobless_time_ms >= JOBLESS_LEAVE_MS:
                        continue
                else:
                    worker.jobless_time_ms = 0.0
            # Segen Worker-Filter: Nur gesegnete Typen bekommen Bonus
            effective_motivation = self.motivation_modifier
            if self.blessed_worker_types:
                is_blessed = ("all" in self.blessed_worker_types or
                              worker.worker_type in self.blessed_worker_types)
                if is_blessed:
                    effective_motivation += self.blessing_bonus
            # Camper-Range je Worker-Typ (Coiner=2000, alle anderen=5000)
            camper_range = float(WORKER_CAMPER_RANGE.get(worker.worker_type, CAMPER_RANGE))
            worker.tick(dt, self.farms, self.residences, self.camps,
                       motivation_mod=effective_motivation,
                       speed_bonus=self.speed_bonus,
                       speed_multiplier=self.speed_multiplier,
                       pathfinder=pathfinder,
                       path_revision=path_revision,
                       spawn_camp_fn=_spawn_camp,
                       camper_range=camper_range)
            survivors.append(worker)
        self.workers = survivors

    def set_village_capacity(self, capacity: int):
        """Setzt die maximale Worker-KapazitÃ¤t basierend auf Dorfzentren."""
        self.max_workers_from_village = capacity

    def add_worker(self, worker_type: str, position: Position, workplace: Position) -> Optional[Worker]:
        """
        FÃ¼gt einen neuen Worker hinzu, wenn Dorfzentrum-KapazitÃ¤t verfÃ¼gbar.

        Returns:
            Worker-Objekt oder None wenn kein Platz
        """
        if not self.can_add_worker():
            return None

        worker = Worker(
            worker_type=worker_type,
            position=position,
            workplace_position=workplace,
        )
        self.workers.append(worker)
        return worker

    def can_add_worker(self) -> bool:
        """PrÃ¼ft ob Dorfzentrum-KapazitÃ¤t fÃ¼r einen weiteren Worker verfÃ¼gbar ist.
        WohnhÃ¤user begrenzen NICHT die BevÃ¶lkerung - nur Dorfzentren!"""
        current_workers = len([w for w in self.workers if w.worker_type != "serf"])
        return current_workers < self.max_workers_from_village

    def add_farm(self, position: Position, level: int = 1) -> Farm:
        """FÃ¼gt einen Bauernhof hinzu."""
        farm = Farm(position=position, level=level)
        self.farms.append(farm)
        return farm

    def add_residence(self, position: Position, level: int = 1) -> Residence:
        """FÃ¼gt ein Wohnhaus hinzu."""
        residence = Residence(position=position, level=level)
        self.residences.append(residence)
        return residence

    def add_camp(self, position: Position) -> Camp:
        """FÃ¼gt ein Camp hinzu."""
        camp = Camp(position=position)
        self.camps.append(camp)
        return camp

    # ==================== STATISTIKEN ====================

    def get_total_residence_capacity(self) -> int:
        """Gesamt-WohnkapazitÃ¤t."""
        return sum(r.live_capacity for r in self.residences)

    def get_total_farm_capacity(self) -> int:
        """Gesamt-Essen-KapazitÃ¤t."""
        return sum(f.eat_capacity for f in self.farms)

    def get_current_workers(self) -> int:
        """Anzahl aktuelle Worker (ohne Serfs)."""
        return len([w for w in self.workers if w.worker_type != "serf"])

    def get_working_workers(self) -> int:
        """Anzahl arbeitender Worker."""
        return sum(1 for w in self.workers if w.state == WorkerState.WORKING)

    def get_exhausted_workers(self) -> int:
        """Anzahl erschoepfter Worker."""
        return sum(1 for w in self.workers if w.work_time <= EXHAUSTED_THRESHOLD)

    def get_average_efficiency(self, worker_type: Optional[str] = None) -> float:
        """Durchschnittliche Effizienz aller Worker oder eines Typs."""
        if worker_type is None:
            if not self.workers:
                return 1.0
            return sum(w.get_efficiency() for w in self.workers) / len(self.workers)
        type_workers = [w for w in self.workers if w.worker_type == worker_type]
        if not type_workers:
            return 0.0
        return sum(w.get_efficiency() for w in type_workers) / len(type_workers)

    def get_efficiency_by_type(self) -> Dict[str, float]:
        """Effizienz pro Worker-Typ (Durchschnitt)."""
        totals: Dict[str, float] = {}
        counts: Dict[str, int] = {}
        for worker in self.workers:
            if not worker.is_work_cycle_active():
                continue
            totals[worker.worker_type] = totals.get(worker.worker_type, 0.0) + worker.get_work_cycle_efficiency()
            counts[worker.worker_type] = counts.get(worker.worker_type, 0) + 1
        return {w_type: totals[w_type] / counts[w_type] for w_type in totals}

    def get_average_worktime(self) -> float:
        """Durchschnittliche WorkTime aller Worker."""
        worktime_workers = [w for w in self.workers if w.has_worktime_system]
        if not worktime_workers:
            return 100.0
        return sum(w.work_time for w in worktime_workers) / len(worktime_workers)

    def get_workers_by_state(self) -> Dict[WorkerState, int]:
        """Anzahl Worker pro Zustand."""
        counts = {state: 0 for state in WorkerState}
        for worker in self.workers:
            counts[worker.state] += 1
        return counts

    def get_residence_utilization(self) -> float:
        """Auslastung der WohnhÃ¤user (0.0 - 1.0)."""
        capacity = self.get_total_residence_capacity()
        if capacity == 0:
            return 1.0
        return self.get_current_workers() / capacity

    def get_farm_utilization(self) -> float:
        """Auslastung der BauernhÃ¶fe (0.0 - 1.0)."""
        capacity = self.get_total_farm_capacity()
        if capacity == 0:
            return 1.0
        eating = len([w for w in self.workers if w.state == WorkerState.EATING])
        return eating / capacity

    def get_exhausted_ratio(self) -> float:
        """Anteil der erschÃ¶pften Worker (0.0 - 1.0)."""
        if len(self.workers) == 0:
            return 0.0
        return self.get_exhausted_workers() / len(self.workers)

    def get_stats(self) -> Dict[str, float]:
        """Gibt alle wichtigen Statistiken zurueck (Single-Pass optimiert)."""
        _WALKING_STATES = frozenset({
            WorkerState.WALKING_TO_SUPPLIER,
            WorkerState.WALKING_FROM_SUPPLIER_TO_WORK,
            WorkerState.WALKING_TO_FARM,
            WorkerState.WALKING_TO_RESIDENCE,
            WorkerState.WALKING_TO_CAMP,
            WorkerState.WALKING_TO_WORK,
        })
        eating = resting = walking = camping = working = exhausted = 0
        eff_sum = 0.0
        wt_sum = 0.0
        wt_count = 0
        for w in self.workers:
            s = w.state
            if s == WorkerState.EATING:
                eating += 1
            elif s == WorkerState.RESTING:
                resting += 1
            elif s in _WALKING_STATES:
                walking += 1
            elif s == WorkerState.CAMPING:
                camping += 1
            elif s == WorkerState.WORKING:
                working += 1
            if w.work_time <= EXHAUSTED_THRESHOLD:
                exhausted += 1
            eff_sum += w.get_efficiency()
            if w.has_worktime_system:
                wt_sum += w.work_time
                wt_count += 1

        total = len(self.workers)
        avg_eff = eff_sum / total if total else 1.0
        avg_wt = wt_sum / wt_count if wt_count else 100.0
        exhausted_ratio = exhausted / total if total else 0.0

        farm_capacity = self.get_total_farm_capacity()
        residence_capacity = self.get_total_residence_capacity()
        farm_util = (eating / farm_capacity) if farm_capacity else 1.0
        residence_util = self.get_current_workers() / residence_capacity if residence_capacity else 1.0

        return {
            "total_workers": total,
            "working_workers": working,
            "eating_workers": eating,
            "resting_workers": resting,
            "walking_workers": walking,
            "camping_workers": camping,
            "exhausted_workers": exhausted,
            "exhausted_ratio": exhausted_ratio,
            "average_efficiency": avg_eff,
            "avg_work_time": avg_wt,
            "average_worktime": avg_wt,
            "residence_capacity": residence_capacity,
            "residence_utilization": residence_util,
            "farm_capacity": farm_capacity,
            "farm_utilization": farm_util,
        }


# ==================== HELPER FUNCTIONS ====================

def load_worker_params_from_game_data(game_data_path: str) -> Dict[str, WorkTimeParams]:
    """LÃ¤dt Worker-Parameter aus der extrahierten game_data.json."""
    with open(game_data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    params = {}
    for worker_name, worker_data in data.get("workers", {}).items():
        if worker_data.get("has_worktime_system", False):
            wt = worker_data.get("worktime", {})
            params[normalize_worker_type(worker_name)] = WorkTimeParams(
                work_wait_until=wt.get("work_wait_until", 30000),
                eat_wait=wt.get("eat_wait", 2000),
                rest_wait=wt.get("rest_wait", 3000),
                work_time_change_work=wt.get("work_time_change_work", -50),
                work_time_change_farm=wt.get("work_time_change_farm", 0.7),
                work_time_change_residence=wt.get("work_time_change_residence", 0.5),
                work_time_change_camp=wt.get("work_time_change_camp", 0.1),
                work_time_max_farm=wt.get("work_time_max_farm", 100),
                work_time_max_residence=wt.get("work_time_max_residence", 400),
                exhausted_malus=wt.get("exhausted_malus", 0.1),
            )
    return params


# ==================== TEST ====================

def test_worker_simulation():
    """Testet die Worker-Simulation."""
    print("=== Worker Simulation Test ===\n")

    # Manager erstellen
    manager = WorkforceManager()

    # GebÃ¤ude hinzufÃ¼gen
    manager.add_residence(Position(0, 0), level=1)  # 6 PlÃ¤tze
    manager.add_farm(Position(500, 0), level=1)  # 8 Esser

    # Worker hinzufÃ¼gen
    for i in range(3):
        manager.add_worker("miner", Position(1000, i * 100), Position(1000, i * 100))

    print(f"Initial: {manager.get_stats()}\n")

    # Simulation fÃ¼r 60 Sekunden
    dt = 0.1  # 100ms Schritte
    for t in range(600):  # 60 Sekunden
        manager.tick(dt)

        if t % 100 == 0:  # Alle 10 Sekunden
            stats = manager.get_stats()
            print(f"t={t * dt:.0f}s: Effizienz={stats['average_efficiency']:.2f}, "
                  f"WorkTime={stats['average_worktime']:.0f}, "
                  f"Working={stats['working_workers']}/{stats['total_workers']}")

    print(f"\nFinal: {manager.get_stats()}")


if __name__ == "__main__":
    test_worker_simulation()
