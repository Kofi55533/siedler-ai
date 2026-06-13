"""
Siedler 5 - Production System
2-Tier Produktionssystem mit Minen und Refinern.

TIER 1: MINEN (CMineBehavior)
- Worker arbeiten lokal
- AmountToMine: 4-6 pro Zyklus (je nach Level)
- KEIN Transport nötig
- Ressourcen sofort gutgeschrieben

TIER 2: REFINER (CResourceRefinerBehavior)
- Worker transportiert Rohstoffe zur Verarbeitung
- Laufzeit = Distanz × 2 / Speed (hin und zurück)
- Verarbeitung mit InitialFactor (z.B. 4 für Schmiede)
- TransportAmount: 5 Einheiten pro Trip

SERFS:
- Extrahieren Ressourcen direkt (sofort gutgeschrieben)
- Delay: 3-4 Sekunden pro Extraktion
- Holz: 2 Einheiten, Rest: 1 Einheit
"""

import json
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum
from pathlib import Path
from worker_simulation import Position, Worker, WorkerState, WorkforceManager, normalize_worker_type


class ResourceType(Enum):
    """Ressourcen-Typen."""
    GOLD = "gold"
    GOLD_RAW = "gold_raw"
    WOOD = "wood"
    WOOD_RAW = "wood_raw"
    STONE = "stone"
    STONE_RAW = "stone_raw"
    CLAY = "clay"
    CLAY_RAW = "clay_raw"
    IRON = "iron"
    IRON_RAW = "iron_raw"
    SULFUR = "sulfur"
    SULFUR_RAW = "sulfur_raw"


# Serf-Extraktion (aus extra2 XMLs)
# VOLLSTÄNDIG: Delay + Animation-Zeit = Gesamtzeit pro Extraktion
# Animation-Zeiten aus TL_SERF_EXTRACT_*.xml:
#   - Holz: 520ms + 1000ms = 1.52s Animation
#   - Minen: 540ms + 1000ms = 1.54s Animation
SERF_EXTRACTION = {
    ResourceType.IRON_RAW: {"delay": 3.0, "animation": 1.54, "amount": 1},    # Total: 4.54s
    ResourceType.STONE_RAW: {"delay": 4.0, "animation": 1.54, "amount": 1},   # Total: 5.54s
    ResourceType.CLAY_RAW: {"delay": 4.0, "animation": 1.54, "amount": 1},    # Total: 5.54s
    ResourceType.SULFUR_RAW: {"delay": 3.0, "animation": 1.54, "amount": 1},  # Total: 4.54s
    ResourceType.WOOD_RAW: {"delay": 4.0, "animation": 1.52, "amount": 2},    # Total: 5.52s, gibt 2 Holz!
}

# ResourceSearchRadius für Serfs (aus PU_Serf.xml)
SERF_RESOURCE_SEARCH_RADIUS = 4500  # cm - Serfs suchen Ressourcen in diesem Radius


# Refiner-Operationen pro Zyklus (task_refine_resource_count + task_mined_resource_count)
# Fallback-Werte fuer fehlendes Truth-Modell.
DEFAULT_REFINER_RESOURCE_OPS_PER_CYCLE = {
    "sawmill_worker": 2,
    "brickmaker": 2,
    "stonecutter": 2,
    "smith": 2,
    "alchemist": 2,
    "gunsmith": 2,
    "treasurer": 2,
    "coiner": 1,
}


def _safe_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _load_refiner_resource_ops_per_cycle() -> Dict[str, int]:
    """Liest Refiner-Multiplikatoren aus config/worker_truth_model.json."""
    result = dict(DEFAULT_REFINER_RESOURCE_OPS_PER_CYCLE)
    truth_path = Path(__file__).resolve().parent / "config" / "worker_truth_model.json"
    if not truth_path.exists():
        return result

    try:
        with open(truth_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError, json.JSONDecodeError):
        return result

    workers = data.get("workers") or {}
    if not isinstance(workers, dict):
        return result

    for raw_name, worker_data in workers.items():
        if not isinstance(worker_data, dict):
            continue

        env_name = worker_data.get("env_name") or raw_name
        worker_name = normalize_worker_type(str(env_name))
        if not worker_name:
            continue

        work_cycle = worker_data.get("work_cycle_truth") or {}
        primary = work_cycle.get("primary_work_tasklist") or {}
        if not isinstance(primary, dict):
            continue

        refine_count = _safe_int(primary.get("task_refine_resource_count"), 0)
        mined_count = _safe_int(primary.get("task_mined_resource_count"), 0)
        total_ops = refine_count + mined_count
        if total_ops > 0:
            result[worker_name] = total_ops

    return result


REFINER_RESOURCE_OPS_PER_CYCLE = _load_refiner_resource_ops_per_cycle()


def get_refiner_resource_ops_per_cycle(worker_type: str, fallback: int = 2) -> int:
    """Gibt die Anzahl Ressourcen-Operationen pro Refiner-Zyklus zurueck."""
    normalized = normalize_worker_type(worker_type)
    value = REFINER_RESOURCE_OPS_PER_CYCLE.get(normalized, fallback)
    return max(1, int(value))


@dataclass
class Mine:
    """
    Tier 1: Mine (CMineBehavior)

    - Worker arbeiten lokal
    - Produktion = Workers × AmountToMine × mines_per_cycle × Effizienz
    - mines_per_cycle=2: Aus Engine-TaskLists (tl_miner_*mine_work.xml)
      haben ALLE Minen 2x TASK_MINED_RESOURCE pro Arbeitszyklus
    - WorkTimeChange ebenfalls 2x pro Zyklus -> Worker erschoepfen doppelt schnell
    """
    name: str
    position: Position
    resource_type: ResourceType
    worker_type: str = "miner"
    level: int = 1
    max_workers: int = 5
    current_workers: int = 0
    amount_to_mine: int = 4  # Pro TASK_MINED_RESOURCE Aufruf
    mines_per_cycle: int = 2  # 2x TASK_MINED_RESOURCE pro Zyklus (aus Engine-TaskLists!)
    worktime_changes_per_cycle: int = 2  # 2x TASK_CHANGE_WORK_TIME_WORK pro Zyklus
    efficiency_override: Optional[float] = None

    @property
    def workers_by_level(self) -> int:
        """Max Workers nach Level."""
        base = {1: 5, 2: 6, 3: 7}
        return base.get(self.level, 5)

    @property
    def amount_by_level(self) -> int:
        """AmountToMine nach Level (pro TASK_MINED_RESOURCE)."""
        base = {1: 4, 2: 5, 3: 6}
        return base.get(self.level, 4)

    def get_production_rate(self, worker_efficiency: float) -> float:
        """
        Berechnet Produktionsrate pro Sekunde.

        Formel: Workers × AmountToMine × mines_per_cycle × Effizienz / WorkWaitUntil
        WorkWaitUntil fuer Miner = 30 Sekunden
        mines_per_cycle = 2 (aus Engine-TaskLists: 2x TASK_MINED_RESOURCE)
        """
        if self.current_workers == 0:
            return 0.0

        work_cycle = 30.0  # Sekunden (WorkWaitUntil aus pu_miner.xml)
        return (self.current_workers * self.amount_by_level * self.mines_per_cycle * worker_efficiency) / work_cycle


@dataclass
class Refiner:
    """
    Tier 2: Refiner (CResourceRefinerBehavior)

    - Worker holt Rohstoffe von Supplier
    - Laufzeit abhaengig von Distanz
    - Verarbeitung mit InitialFactor
    - refines_per_cycle: Aus Engine-TaskLists (tl_*_work.xml)
      Die meisten Refiner rufen TASK_REFINE_RESOURCE 2x pro Zyklus auf!
    """
    name: str
    position: Position
    resource_type: ResourceType
    input_resource: ResourceType
    supplier_position: Position
    worker_type: str = "sawmill_worker"
    level: int = 1
    max_workers: int = 4
    current_workers: int = 0
    initial_factor: int = 4  # Umwandlungsrate (4 Roh -> 1 Verarbeitet)
    transport_amount: int = 5  # Pro Trip
    worker_speed: int = 320
    work_wait_until: float = 5.0  # Sekunden Arbeitszeit pro Zyklus (WorkWaitUntil)
    # Gesamtzahl Ressourcen-Operationen pro Zyklus (refine + mined aus TaskLists)
    refines_per_cycle: int = 2
    worktime_changes_per_cycle: int = 2  # Meist 2x TASK_CHANGE_WORK_TIME_WORK pro Zyklus
    path_distance: Optional[float] = None  # Optionaler A* Pfad (Wegstrecke)
    efficiency_override: Optional[float] = None

    def get_cycle_time(self, speed_bonus: int = 0, speed_multiplier: float = 1.0) -> float:
        """
        Berechnet Zykluszeit fuer einen Transport-Zyklus.

        Zyklus = Hin + Verarbeitung + Zurueck
        """
        distance = self.path_distance
        if distance is None:
            distance = self.position.distance_to(self.supplier_position)
        worker_speed = max(1.0, (self.worker_speed + speed_bonus) * max(0.01, float(speed_multiplier)))
        walk_time = (distance * 2) / worker_speed  # Hin und zurueck
        work_time = self.work_wait_until if self.work_wait_until else 0.0
        return walk_time + work_time

    def get_production_rate(self, worker_efficiency: float, speed_bonus: int = 0,
                            speed_multiplier: float = 1.0) -> float:
        """
        Berechnet Produktionsrate pro Sekunde.

        Formel: Workers × TransportAmount × refines_per_cycle × Effizienz / CycleTime
        refines_per_cycle = 2 fuer die meisten Refiner (aus Engine-TaskLists)
        """
        if self.current_workers == 0:
            return 0.0

        cycle_time = self.get_cycle_time(speed_bonus=speed_bonus, speed_multiplier=speed_multiplier)
        if cycle_time <= 0:
            return 0.0

        return (self.current_workers * self.transport_amount * self.refines_per_cycle * worker_efficiency) / cycle_time

    def get_input_consumption_rate(self, worker_efficiency: float, speed_bonus: int = 0,
                                   speed_multiplier: float = 1.0) -> float:
        """
        Berechnet Input-Verbrauch pro Sekunde.

        InitialFactor gibt das Verhaeltnis an (z.B. 4 = 4:1)
        """
        production = self.get_production_rate(
            worker_efficiency,
            speed_bonus=speed_bonus,
            speed_multiplier=speed_multiplier,
        )
        return production * self.initial_factor


class SerfState(Enum):
    """Zustände eines Leibeigenen."""
    IDLE = "idle"
    WALKING_TO_RESOURCE = "walking_to_resource"
    EXTRACTING = "extracting"
    WALKING_TO_BUILD = "walking_to_build"  # NEU: Läuft zum Bauplatz
    BUILDING = "building"  # NEU: Baut ein Gebäude


@dataclass
class Serf:
    """
    Serf (Leibeigener) für Ressourcen-Extraktion UND Gebäude-Bau.

    WICHTIG - Korrektes Spielverhalten:
    - Leibeigene werden zu einer Ressource GESCHICKT
    - Sie LAUFEN zur Ressource (Zeit = Distanz / Speed)
    - Bei HOLZ: Einmalig extrahieren (2 Holz), dann IDLE (Baum gefällt!)
    - Bei anderen Ressourcen: ENDLOS extrahieren (Minen, Vorkommen)
    - KEIN WorkTime-System (arbeitet ohne Pausen)
    - Delay: 3-4 Sekunden pro Extraktion

    NEU - Gebäude-Bau:
    - Leibeigene können zu Bauplätzen geschickt werden
    - Sie laufen zum Bauplatz und bauen dann
    - Mehrere Leibeigene = schnellerer Bau
    """
    position: Position
    target_resource: Optional[ResourceType] = None
    target_position: Optional[Position] = None
    serf_id: Optional[int] = None  # Stable environment-side identity for exact source selection.
    extraction_timer: float = 0.0
    state: SerfState = SerfState.IDLE
    speed: int = 400  # Serf-Geschwindigkeit (aus PU_Serf.xml: Speed=400)
    tree_id: Optional[int] = None  # ID des zugewiesenen Baums (für Holz)
    # NEU: Unterscheidung zwischen Vorkommen und Mine
    work_location: Optional[str] = None  # "deposit", "mine", oder "wood"
    # NEU: Bau-spezifische Felder
    build_target: Optional[str] = None  # Name des zu bauenden Gebäudes
    build_site_id: Optional[int] = None  # ID des Bauplatzes
    path: List[Position] = field(default_factory=list)
    path_index: int = 0
    path_distance: Optional[float] = None
    waypoint: Optional[Position] = None
    path_revision: int = -1
    path_blocked: bool = False
    speed_bonus: int = 0
    speed_multiplier: float = 1.0

    def tick(self, dt: float,
             pathfinder: Optional[Callable[[Position, Position], List[Position]]] = None,
             path_revision: Optional[int] = None) -> Optional[Tuple[ResourceType, int]]:
        """
        Simuliert einen Zeitschritt.

        Returns:
            (ResourceType, Menge) wenn Extraktion fertig, sonst None
            Für Bau-States wird ("BUILD", build_progress) zurückgegeben
        """
        self._pathfinder = pathfinder
        self._path_revision = path_revision
        if self.state == SerfState.IDLE:
            return None

        elif self.state == SerfState.WALKING_TO_RESOURCE:
            return self._tick_walking(dt)

        elif self.state == SerfState.EXTRACTING:
            return self._tick_extracting(dt)

        elif self.state == SerfState.WALKING_TO_BUILD:
            return self._tick_walking_to_build(dt)

        elif self.state == SerfState.BUILDING:
            return self._tick_building(dt)

        return None

    def _tick_walking(self, dt: float) -> None:
        """Läuft zur Ressource."""
        self._maybe_repath()
        if self.path_blocked and self.waypoint is None:
            return None
        if self.waypoint is None:
            self.state = SerfState.IDLE
            return None

        remaining = self._effective_speed() * dt
        epsilon = 1e-6

        # Verbraucht die komplette Bewegungsdistanz im Tick (wichtig bei dt=1s).
        while remaining > epsilon and self.waypoint is not None:
            distance = self.position.distance_to(self.waypoint)

            if distance <= epsilon:
                self.position = Position(self.waypoint.x, self.waypoint.y)
                if self.path and self.path_index + 1 < len(self.path):
                    self.path_index += 1
                    self.waypoint = self.path[self.path_index]
                    continue
                self.waypoint = self.target_position
                self.path = []
                self.path_index = 0
                self.state = SerfState.EXTRACTING
                self.extraction_timer = 0.0
                return None

            if remaining >= distance:
                self.position = Position(self.waypoint.x, self.waypoint.y)
                remaining -= distance
                if self.path and self.path_index + 1 < len(self.path):
                    self.path_index += 1
                    self.waypoint = self.path[self.path_index]
                    continue
                self.waypoint = self.target_position
                self.path = []
                self.path_index = 0
                self.state = SerfState.EXTRACTING
                self.extraction_timer = 0.0
                return None

            ratio = remaining / distance
            self.position.x += ratio * (self.waypoint.x - self.position.x)
            self.position.y += ratio * (self.waypoint.y - self.position.y)
            remaining = 0.0

        return None

    def _tick_extracting(self, dt: float) -> Optional[Tuple[ResourceType, int]]:
        """Extrahiert Ressourcen (mit Animations-Zeit!)."""
        if self.target_resource is None:
            return None

        extraction_data = SERF_EXTRACTION.get(self.target_resource)
        if not extraction_data:
            return None

        self.extraction_timer += dt

        # Gesamtzeit = Delay + Animation (aus extra2 XMLs)
        total_extraction_time = extraction_data["delay"] + extraction_data.get("animation", 0.0)

        if self.extraction_timer >= total_extraction_time:
            # Extraktion fertig!
            self.extraction_timer = 0.0
            result = (self.target_resource, extraction_data["amount"])

            # HOLZ: Serf extrahiert MEHRFACH vom gleichen Baum!
            # Der Baum hat ResourceAmount=75, jede Extraktion gibt Amount=2.
            # Erst wenn resource_remaining <= 0 wird der Serf IDLE.
            # Das Tracking passiert in environment._tick_time() die
            # resource_remaining dekrementiert und den Serf stoppt wenn leer.
            #
            # WICHTIG: Serf bleibt im EXTRACTING-State und extrahiert weiter!
            # (kein automatisches IDLE mehr hier)

            return result

        return None

    def _tick_walking_to_build(self, dt: float) -> None:
        """Läuft zum Bauplatz."""
        self._maybe_repath()
        if self.path_blocked and self.waypoint is None:
            return None
        if self.waypoint is None:
            self.state = SerfState.IDLE
            return None

        remaining = self._effective_speed() * dt
        epsilon = 1e-6

        # Verbraucht die komplette Bewegungsdistanz im Tick (wichtig bei dt=1s).
        while remaining > epsilon and self.waypoint is not None:
            distance = self.position.distance_to(self.waypoint)

            if distance <= epsilon:
                self.position = Position(self.waypoint.x, self.waypoint.y)
                if self.path and self.path_index + 1 < len(self.path):
                    self.path_index += 1
                    self.waypoint = self.path[self.path_index]
                    continue
                self.waypoint = self.target_position
                self.path = []
                self.path_index = 0
                self.state = SerfState.BUILDING
                return None

            if remaining >= distance:
                self.position = Position(self.waypoint.x, self.waypoint.y)
                remaining -= distance
                if self.path and self.path_index + 1 < len(self.path):
                    self.path_index += 1
                    self.waypoint = self.path[self.path_index]
                    continue
                self.waypoint = self.target_position
                self.path = []
                self.path_index = 0
                self.state = SerfState.BUILDING
                return None

            ratio = remaining / distance
            self.position.x += ratio * (self.waypoint.x - self.position.x)
            self.position.y += ratio * (self.waypoint.y - self.position.y)
            remaining = 0.0

        return None

    def _tick_building(self, dt: float) -> Optional[Tuple[str, float]]:
        """
        Baut am Gebäude.

        Returns:
            ("BUILD", dt) um anzuzeigen wie viel Bau-Fortschritt gemacht wurde
        """
        if self.build_target is None:
            self.state = SerfState.IDLE
            return None

        # Gib Bau-Fortschritt zurück (dt Sekunden Arbeit)
        # Die tatsächliche Bauzeit-Reduktion wird in environment.py berechnet
        return ("BUILD", dt)

    def assign_to_build(self, building_name: str, build_position: Position,
                        start_position: Position, build_site_id: int = None,
                        path: Optional[List[Position]] = None):
        """
        Weist Leibeigenen einem Bauprojekt zu.

        Args:
            building_name: Name des zu bauenden Gebäudes
            build_position: Position des Bauplatzes
            start_position: Aktuelle Position des Leibeigenen
            build_site_id: ID des Bauplatzes (für Tracking)
        """
        self.build_target = building_name
        self._set_target(build_position, path)
        self.position = start_position
        self.state = SerfState.WALKING_TO_BUILD
        self.build_site_id = build_site_id
        # Reset Ressourcen-bezogene Felder
        self.target_resource = None
        self.extraction_timer = 0.0
        self.tree_id = None

    def is_building(self) -> bool:
        """Prüft ob Serf gerade baut."""
        return self.state in (SerfState.WALKING_TO_BUILD, SerfState.BUILDING)

    def set_speed_context(self, speed_bonus: int = 0, speed_multiplier: float = 1.0):
        """Setzt Bewegungsboni fuer Projektionen und laufende Bewegung."""
        self.speed_bonus = int(speed_bonus)
        try:
            self.speed_multiplier = max(0.01, float(speed_multiplier))
        except (TypeError, ValueError):
            self.speed_multiplier = 1.0

    def _effective_speed(self) -> float:
        return max(1.0, (self.speed + self.speed_bonus) * self.speed_multiplier)

    def _set_target(self, target: Position, path: Optional[List[Position]] = None):
        """Setzt Zielposition und optionalen Pfad."""
        self.target_position = target
        self.path = []
        self.path_index = 0
        self.waypoint = None
        self.path_blocked = False
        path_was_provided = path is not None
        if path:
            # Entferne Startknoten falls nahezu identisch
            if self.position.distance_to(path[0]) < 1.0:
                path = path[1:]
            if path:
                self.path = path
                self.path_index = 0
                self.waypoint = self.path[0]
        if self.waypoint is None:
            has_pathfinder = getattr(self, "_pathfinder", None) is not None
            if (path_was_provided or has_pathfinder) and self.target_position is not None and self.position.distance_to(self.target_position) > 1.0:
                # Kein valider Pfad verfuegbar: warten bis Repathing einen Weg findet.
                self.path_blocked = True
            else:
                self.waypoint = self.target_position
        current_rev = getattr(self, "_path_revision", None)
        if current_rev is not None:
            self.path_revision = current_rev

    def _maybe_repath(self):
        """Aktualisiert den Pfad wenn sich die Umgebung geÃ¤ndert hat."""
        pathfinder = getattr(self, "_pathfinder", None)
        current_rev = getattr(self, "_path_revision", None)
        if not pathfinder or current_rev is None:
            return
        if self.target_position is None:
            return
        if self.path_revision == current_rev:
            # Nur neu planen wenn sich die Umgebung geÃ¤ndert hat.
            return
        try:
            path = pathfinder(self.position, self.target_position) or []
        except Exception:
            path = []
        if path and self.position.distance_to(path[0]) < 1.0:
            path = path[1:]
        if path:
            self.path = path
            self.path_index = 0
            self.waypoint = self.path[0]
            self.path_blocked = False
        else:
            self.path = []
            self.path_index = 0
            if self.position.distance_to(self.target_position) <= 1.0:
                self.waypoint = self.target_position
                self.path_blocked = False
            else:
                self.waypoint = None
                self.path_blocked = True
        self.path_revision = current_rev

    def assign_to_resource(self, resource: ResourceType, resource_position: Position,
                           start_position: Position, path_distance: float = None,
                           tree_id: int = None, path: Optional[List[Position]] = None):
        """
        Weist Leibeigenen einer Ressource zu.

        Args:
            resource: Typ der Ressource (WOOD, IRON, etc.)
            resource_position: Position der Ressource auf der Karte
            start_position: Aktuelle Position des Leibeigenen (z.B. HQ)
            path_distance: (NEU) Exakte Pfaddistanz von A* (optional).
                          Wenn None, wird Luftlinie berechnet.
            tree_id: (NEU) ID des Baums (nur für WOOD), für Tracking
        """
        self.target_resource = resource
        self._set_target(resource_position, path)
        self.position = start_position
        self.state = SerfState.WALKING_TO_RESOURCE
        self.extraction_timer = 0.0

        # NEU: Speichere exakte Pfaddistanz wenn verfügbar
        self.path_distance = path_distance

        # NEU: Speichere Baum-ID für Holz-Extraktion
        if resource in (ResourceType.WOOD, ResourceType.WOOD_RAW):
            self.tree_id = tree_id
        else:
            self.tree_id = None

    def get_walk_time(self) -> float:
        """
        Berechnet die Laufzeit zur Ressource in Sekunden.

        NEU: Verwendet path_distance wenn verfügbar (A* Pfad),
        ansonsten Fallback auf Luftlinie.
        """
        if self.target_position is None:
            return 0.0

        # Verwende A* Distanz wenn verfügbar
        if hasattr(self, 'path_distance') and self.path_distance is not None:
            distance = self.path_distance
        else:
            # Fallback: Luftlinie
            distance = self.position.distance_to(self.target_position)

        return distance / self._effective_speed()

    def get_time_until_first_extraction(self) -> float:
        """Berechnet Zeit bis zur ersten Extraktion (Laufzeit + Extraktionsdelay)."""
        if self.target_resource is None:
            return float('inf')

        walk_time = self.get_walk_time()
        extraction_data = SERF_EXTRACTION.get(self.target_resource)
        if not extraction_data:
            return float('inf')

        # Gesamtzeit = Laufzeit + Delay + Animation
        total_extraction_time = extraction_data["delay"] + extraction_data.get("animation", 0.0)
        return walk_time + total_extraction_time

    def stop(self):
        """Stoppt den Leibeigenen (Extraktion oder Bau)."""
        self.state = SerfState.IDLE
        self.target_resource = None
        self.target_position = None
        self.build_target = None
        self.build_site_id = None
        self.work_location = None  # NEU: Reset work_location
        self.path = []
        self.path_index = 0
        self.path_distance = None
        self.waypoint = None
        self.path_revision = -1
        self.path_blocked = False

    def is_extracting(self) -> bool:
        """Prüft ob Leibeigener gerade extrahiert."""
        return self.state == SerfState.EXTRACTING

    def is_walking(self) -> bool:
        """Prüft ob Leibeigener gerade zur Ressource läuft."""
        return self.state == SerfState.WALKING_TO_RESOURCE

    def is_idle(self) -> bool:
        """Prüft ob Leibeigener untätig ist."""
        return self.state == SerfState.IDLE


@dataclass
class ProductionSystem:
    """
    Vollständiges Produktionssystem mit 2-Tier Logik.

    Verwaltet:
    - Minen (Tier 1)
    - Refiner (Tier 2)
    - Serfs (Extraktion)
    - Ressourcen-Lager
    """
    mines: Dict[str, Mine] = field(default_factory=dict)
    refiners: Dict[str, Refiner] = field(default_factory=dict)
    serfs: List[Serf] = field(default_factory=list)
    resources: Dict[ResourceType, float] = field(default_factory=dict)
    workforce_manager: Optional[WorkforceManager] = None

    def __post_init__(self):
        # Ressourcen initialisieren
        for resource in ResourceType:
            if resource not in self.resources:
                self.resources[resource] = 0.0
        self.last_serf_events: List[dict] = []

    def tick(self, dt: float,
             pathfinder: Optional[Callable[[Position, Position], List[Position]]] = None,
             path_revision: Optional[int] = None) -> Dict[ResourceType, float]:
        """
        Simuliert einen Zeitschritt für alle Produktions-Einheiten.

        Args:
            dt: Delta-Zeit in Sekunden

        Returns:
            Dict mit produzierten Ressourcen in diesem Tick
        """
        produced = defaultdict(float)

        # Worker-Effizienz holen
        efficiency = 1.0
        efficiency_by_type = None
        speed_bonus = 0
        speed_multiplier = 1.0
        if self.workforce_manager:
            efficiency = self.workforce_manager.get_average_efficiency()
            efficiency_by_type = self.workforce_manager.get_efficiency_by_type()
            speed_bonus = self.workforce_manager.speed_bonus
            speed_multiplier = getattr(self.workforce_manager, "speed_multiplier", 1.0)

        # Aktive Mine-Typen einmal vorberechnen (verhindert O(N*M) in _tick_refiners)
        active_mine_types = frozenset(
            m.resource_type for m in self.mines.values() if m.current_workers > 0
        )

        # Minen produzieren
        mine_production = self._tick_mines(dt, efficiency, efficiency_by_type)
        for resource, amount in mine_production.items():
            produced[resource] += amount
            self.resources[resource] += amount

        # Refiner produzieren
        refiner_production = self._tick_refiners(
            dt,
            efficiency,
            efficiency_by_type,
            speed_bonus,
            active_mine_types,
            speed_multiplier=speed_multiplier,
        )
        for resource, amount in refiner_production.items():
            produced[resource] += amount
            self.resources[resource] += amount

        # Serfs extrahieren
        serf_production, serf_events = self._tick_serfs(
            dt,
            pathfinder=pathfinder,
            path_revision=path_revision,
            speed_bonus=speed_bonus,
            speed_multiplier=speed_multiplier,
        )
        for resource, amount in serf_production.items():
            produced[resource] += amount
            self.resources[resource] += amount
        self.last_serf_events = serf_events

        return produced

    def _tick_mines(self, dt: float, efficiency: float,
                    efficiency_by_type: Optional[Dict[str, float]] = None) -> Dict[ResourceType, float]:
        """Tick fuer alle Minen."""
        production: Dict[ResourceType, float] = defaultdict(float)

        for mine in self.mines.values():
            if mine.efficiency_override is not None:
                eff = mine.efficiency_override
            else:
                eff = efficiency if efficiency_by_type is None else efficiency_by_type.get(mine.worker_type, 0.0)
            production[mine.resource_type] += mine.get_production_rate(eff) * dt

        return production

    def _tick_refiners(self, dt: float, efficiency: float,
                       efficiency_by_type: Optional[Dict[str, float]] = None,
                       speed_bonus: int = 0,
                       active_mine_types: Optional[frozenset] = None,
                       speed_multiplier: float = 1.0) -> Dict[ResourceType, float]:
        """Tick fuer alle Refiner."""
        production: Dict[ResourceType, float] = defaultdict(float)

        # Fallback: aktive Mine-Typen berechnen wenn nicht uebergeben
        if active_mine_types is None:
            active_mine_types = frozenset(
                m.resource_type for m in self.mines.values() if m.current_workers > 0
            )

        for refiner in self.refiners.values():
            if refiner.efficiency_override is not None:
                eff = refiner.efficiency_override
            else:
                eff = efficiency if efficiency_by_type is None else efficiency_by_type.get(refiner.worker_type, 0.0)
            # Wenn Input == Output (z.B. Eisen -> Eisen): Kein Input-Verbrauch!
            # Im echten Spiel holen Refiner Rohstoffe von der Mine (lokaler Speicher),
            # aber da unsere Minen direkt in den globalen Pool produzieren,
            # wuerde Input-Verbrauch bei gleicher Ressource einen Netto-Verlust erzeugen.
            # Refiner agieren hier als Zusatz-Produzenten, aber NUR wenn eine
            # zugehoerige Mine aktiv ist (mit Workern). Ohne aktive Mine produziert
            # der Refiner nichts - er "veredelt" ja das Minen-Output.
            if refiner.input_resource == refiner.resource_type:
                # Nutze pre-computetes Set statt O(N) any()-Schleife
                if refiner.resource_type not in active_mine_types:
                    continue  # Ohne aktive Mine kein Refiner-Output

                # Zusatz-Produzent - kein Input-Verbrauch, aber nur mit aktiver Mine
                production[refiner.resource_type] += refiner.get_production_rate(
                    eff,
                    speed_bonus=speed_bonus,
                    speed_multiplier=speed_multiplier,
                ) * dt
            else:
                # Verschiedene Input/Output Ressourcen - normaler Verbrauch
                input_rate = refiner.get_input_consumption_rate(
                    eff,
                    speed_bonus=speed_bonus,
                    speed_multiplier=speed_multiplier,
                )
                input_needed = input_rate * dt

                available = self.resources.get(refiner.input_resource, 0)
                if available < input_needed:
                    # Nicht genug Input - proportional reduzieren
                    ratio = available / input_needed if input_needed > 0 else 0
                    input_needed = available
                else:
                    ratio = 1.0

                # Input verbrauchen und Output produzieren
                self.resources[refiner.input_resource] -= input_needed
                production[refiner.resource_type] += refiner.get_production_rate(
                    eff,
                    speed_bonus=speed_bonus,
                    speed_multiplier=speed_multiplier,
                ) * dt * ratio

        return production

    def _tick_serfs(self, dt: float,
                    pathfinder: Optional[Callable[[Position, Position], List[Position]]] = None,
                    path_revision: Optional[int] = None,
                    speed_bonus: int = 0,
                    speed_multiplier: float = 1.0) -> Tuple[Dict[ResourceType, float], List[dict]]:
        """Tick für alle Serfs."""
        production: Dict[ResourceType, float] = {}
        events: List[dict] = []

        for serf in self.serfs:
            serf.set_speed_context(speed_bonus=speed_bonus, speed_multiplier=speed_multiplier)
            result = serf.tick(dt, pathfinder=pathfinder, path_revision=path_revision)
            if result:
                resource, amount = result
                # BUILD-Ergebnisse ignorieren - werden in environment.py behandelt
                if resource == "BUILD":
                    continue
                if resource not in production:
                    production[resource] = 0.0
                production[resource] += amount
                events.append({
                    "serf": serf,
                    "resource": resource,
                    "amount": amount,
                    "position": serf.target_position or serf.position,
                    "tree_id": serf.tree_id,
                    "work_location": serf.work_location,
                })

        return production, events

    # ==================== GEBÄUDE-MANAGEMENT ====================

    def add_mine(self, name: str, position: Position, resource: ResourceType,
                 level: int = 1, worker_type: str = "miner") -> Mine:
        """Fügt eine Mine hinzu."""
        mine = Mine(
            name=name,
            position=position,
            resource_type=resource,
            worker_type=worker_type,
            level=level,
        )
        self.mines[name] = mine
        return mine

    def add_refiner(self, name: str, position: Position, output: ResourceType,
                    input_res: ResourceType, supplier_pos: Position,
                    initial_factor: int = 4, level: int = 1,
                    work_wait_until: float = 5.0, worker_type: str = "sawmill_worker",
                    max_workers: Optional[int] = None,
                    refines_per_cycle: Optional[int] = None) -> Refiner:
        """Fügt einen Refiner hinzu."""
        if refines_per_cycle is None:
            refines_per_cycle = get_refiner_resource_ops_per_cycle(worker_type)

        refiner = Refiner(
            name=name,
            position=position,
            resource_type=output,
            input_resource=input_res,
            supplier_position=supplier_pos,
            worker_type=worker_type,
            initial_factor=initial_factor,
            level=level,
            max_workers=max_workers if max_workers is not None else 4,
            work_wait_until=work_wait_until,
            refines_per_cycle=refines_per_cycle,
        )
        self.refiners[name] = refiner
        return refiner

    def add_serf(self, position: Position) -> Serf:
        """Fügt einen Serf hinzu."""
        serf = Serf(position=position)
        self.serfs.append(serf)
        return serf

    def assign_workers_to_mine(self, mine_name: str, count: int) -> int:
        """Weist Worker einer Mine zu."""
        if mine_name not in self.mines:
            return 0

        mine = self.mines[mine_name]
        available = mine.workers_by_level - mine.current_workers
        assigned = min(count, available)
        mine.current_workers += assigned
        return assigned

    def assign_workers_to_refiner(self, refiner_name: str, count: int) -> int:
        """Weist Worker einem Refiner zu."""
        if refiner_name not in self.refiners:
            return 0

        refiner = self.refiners[refiner_name]
        available = refiner.max_workers - refiner.current_workers
        assigned = min(count, available)
        refiner.current_workers += assigned
        return assigned

    # ==================== STATISTIKEN ====================

    def get_production_rates(self, efficiency: float = 1.0,
                             efficiency_by_type: Optional[Dict[str, float]] = None,
                             speed_bonus: int = 0,
                             speed_multiplier: float = 1.0) -> Dict[ResourceType, float]:
        """Gibt Produktionsraten pro Sekunde für alle Ressourcen zurück."""
        rates = {r: 0.0 for r in ResourceType}
        if efficiency_by_type is None and self.workforce_manager:
            efficiency_by_type = self.workforce_manager.get_efficiency_by_type()
            speed_bonus = self.workforce_manager.speed_bonus
            speed_multiplier = getattr(self.workforce_manager, "speed_multiplier", 1.0)

        for mine in self.mines.values():
            if mine.efficiency_override is not None:
                eff = mine.efficiency_override
            else:
                eff = efficiency if efficiency_by_type is None else efficiency_by_type.get(mine.worker_type, 0.0)
            rate = mine.get_production_rate(eff)
            rates[mine.resource_type] += rate

        for refiner in self.refiners.values():
            # Bei Input==Output: Nur zaehlen wenn aktive Mine vorhanden
            if refiner.input_resource == refiner.resource_type:
                has_active_mine = any(
                    m.resource_type == refiner.resource_type and m.current_workers > 0
                    for m in self.mines.values()
                )
                if not has_active_mine:
                    continue
            if refiner.efficiency_override is not None:
                eff = refiner.efficiency_override
            else:
                eff = efficiency if efficiency_by_type is None else efficiency_by_type.get(refiner.worker_type, 0.0)
            rate = refiner.get_production_rate(
                eff,
                speed_bonus=speed_bonus,
                speed_multiplier=speed_multiplier,
            )
            rates[refiner.resource_type] += rate

        # Serfs (nur wenn sie tatsächlich extrahieren, nicht beim Laufen)
        for serf in self.serfs:
            if serf.is_extracting() and serf.target_resource:
                data = SERF_EXTRACTION.get(serf.target_resource)
                if data:
                    # Gesamtzeit = Delay + Animation
                    total_time = data["delay"] + data.get("animation", 0.0)
                    rates[serf.target_resource] += data["amount"] / total_time

        return rates

    def get_consumption_rates(self, efficiency: float = 1.0,
                              efficiency_by_type: Optional[Dict[str, float]] = None,
                              speed_bonus: int = 0,
                              speed_multiplier: float = 1.0) -> Dict[ResourceType, float]:
        """Gibt Verbrauchsraten pro Sekunde für alle Ressourcen zurück."""
        rates = {r: 0.0 for r in ResourceType}
        if efficiency_by_type is None and self.workforce_manager:
            efficiency_by_type = self.workforce_manager.get_efficiency_by_type()
            speed_bonus = self.workforce_manager.speed_bonus
            speed_multiplier = getattr(self.workforce_manager, "speed_multiplier", 1.0)

        for refiner in self.refiners.values():
            # Kein Verbrauch wenn Input == Output (siehe _tick_refiners)
            if refiner.input_resource == refiner.resource_type:
                continue
            eff = efficiency if efficiency_by_type is None else efficiency_by_type.get(refiner.worker_type, 0.0)
            rate = refiner.get_input_consumption_rate(
                eff,
                speed_bonus=speed_bonus,
                speed_multiplier=speed_multiplier,
            )
            rates[refiner.input_resource] += rate

        return rates

    def get_net_rates(self, efficiency: float = 1.0,
                      efficiency_by_type: Optional[Dict[str, float]] = None,
                      speed_bonus: int = 0,
                      speed_multiplier: float = 1.0) -> Dict[ResourceType, float]:
        """Gibt Netto-Raten (Produktion - Verbrauch) zurück."""
        production = self.get_production_rates(
            efficiency,
            efficiency_by_type,
            speed_bonus,
            speed_multiplier,
        )
        consumption = self.get_consumption_rates(
            efficiency,
            efficiency_by_type,
            speed_bonus,
            speed_multiplier,
        )

        net = {}
        for resource in ResourceType:
            net[resource] = production.get(resource, 0) - consumption.get(resource, 0)

        return net

    def get_bottleneck(self, efficiency: float = 1.0) -> Optional[ResourceType]:
        """Findet die Ressource mit dem niedrigsten Netto-Rate (Engpass)."""
        net = self.get_net_rates(efficiency)

        # Nur negative oder niedrige Raten betrachten
        bottleneck = None
        min_rate = float('inf')

        for resource, rate in net.items():
            if rate < min_rate:
                min_rate = rate
                bottleneck = resource

        return bottleneck

    def get_stats(self) -> Dict:
        """Gibt alle wichtigen Statistiken zurück."""
        efficiency = 1.0
        if self.workforce_manager:
            efficiency = self.workforce_manager.get_average_efficiency()

        return {
            "resources": {r.value: v for r, v in self.resources.items()},
            "production_rates": {r.value: v for r, v in self.get_production_rates(efficiency).items()},
            "consumption_rates": {r.value: v for r, v in self.get_consumption_rates(efficiency).items()},
            "net_rates": {r.value: v for r, v in self.get_net_rates(efficiency).items()},
            "mines": len(self.mines),
            "refiners": len(self.refiners),
            "serfs": len(self.serfs),
            "bottleneck": self.get_bottleneck(efficiency).value if self.get_bottleneck(efficiency) else None,
        }


# ==================== BUILDING DEFINITIONS ====================

# Mine-Definitionen (aus game_data.json)
MINE_TYPES = {
    "pb_ironmine": ResourceType.IRON,
    "pb_stonemine": ResourceType.STONE,
    "pb_claymine": ResourceType.CLAY,
    "pb_sulfurmine": ResourceType.SULFUR,
}

# Refiner-Definitionen
REFINER_TYPES = {
    "pb_blacksmith": {
        "output": ResourceType.IRON,  # Verarbeitetes Eisen
        "input": ResourceType.IRON,
        "factor": 4,
    },
    "pb_sawmill": {
        "output": ResourceType.WOOD,  # Verarbeitetes Holz
        "input": ResourceType.WOOD,
        "factor": 4,
    },
    "pb_bank": {
        "output": ResourceType.GOLD,
        "input": ResourceType.GOLD,
        "factor": 2,  # 2:1 Umwandlung!
    },
}


# ==================== TEST ====================

def test_production_system():
    """Testet das Produktionssystem mit korrekter Leibeigenen-Logik."""
    print("=== Production System Test ===\n")
    print("LEIBEIGENE: Laufen zur Ressource, bleiben dort, extrahieren endlos!\n")

    # System erstellen
    system = ProductionSystem()

    # Start-Ressourcen
    system.resources[ResourceType.IRON] = 100
    system.resources[ResourceType.GOLD] = 500

    # Mine hinzufügen
    mine = system.add_mine("iron_mine_1", Position(0, 0), ResourceType.IRON, level=1)
    system.assign_workers_to_mine("iron_mine_1", 3)

    # ============================================
    # LEIBEIGENE TEST: Realistische Distanzen
    # ============================================
    # HQ Position (Spieler 1): (41100, 23100)
    # Nächster Baum: ca. 1542 Einheiten entfernt
    # Serf-Speed: 360 Einheiten/Sekunde
    # Laufzeit: 1542 / 360 = 4.28 Sekunden

    hq_position = Position(41100, 23100)
    tree_position = Position(42330, 24030)  # Nächster Baum

    serf = system.add_serf(hq_position)
    serf.assign_to_resource(ResourceType.WOOD, tree_position, hq_position)

    walk_time = serf.get_walk_time()
    print(f"Leibeigener startet am HQ: ({hq_position.x}, {hq_position.y})")
    print(f"Ziel: Baum bei ({tree_position.x}, {tree_position.y})")
    print(f"Distanz: {hq_position.distance_to(tree_position):.0f} Einheiten")
    print(f"Geschätzte Laufzeit: {walk_time:.1f} Sekunden")
    print(f"Zeit bis erste Extraktion: {serf.get_time_until_first_extraction():.1f} Sekunden\n")

    print(f"Initial: Serf-Status = {serf.state.value}")
    print(f"Initial Resources: {system.get_stats()['resources']}\n")

    # Simulation für 30 Sekunden
    dt = 0.1
    last_state = serf.state
    wood_collected = 0

    for t in range(300):
        old_wood = system.resources[ResourceType.WOOD]
        system.tick(dt)
        new_wood = system.resources[ResourceType.WOOD]

        if new_wood > old_wood:
            wood_collected += (new_wood - old_wood)

        # Status-Änderung anzeigen
        if serf.state != last_state:
            print(f"t={t * dt:.1f}s: Serf-Status: {last_state.value} -> {serf.state.value}")
            if serf.state == SerfState.EXTRACTING:
                print(f"         Leibeigener ist angekommen und extrahiert jetzt!")
            last_state = serf.state

        # Alle 5 Sekunden Status ausgeben
        if t % 50 == 0 and t > 0:
            stats = system.get_stats()
            print(f"t={t * dt:.0f}s: Wood={stats['resources']['wood']:.1f}, "
                  f"Serf={serf.state.value}, "
                  f"Position=({serf.position.x:.0f}, {serf.position.y:.0f})")

    print(f"\n=== ERGEBNIS nach 30 Sekunden ===")
    print(f"Holz gesammelt: {wood_collected:.0f}")
    print(f"Serf-Status: {serf.state.value}")
    print(f"Serf bleibt bei: ({serf.position.x:.0f}, {serf.position.y:.0f})")
    print(f"Final: {system.get_stats()}")


if __name__ == "__main__":
    test_production_system()
