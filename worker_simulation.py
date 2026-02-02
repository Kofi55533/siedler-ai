"""
Siedler 5 - Worker Simulation
Simuliert das WorkTime-System mit Pausen und Laufwegen.

Kritische Mechaniken:
- Worker haben WorkTime (sinkt beim Arbeiten)
- Bei Hunger: Laufen zu Farm → Essen → Laufen zu Wohnhaus → Ruhen
- Wenn kein Farm/Wohnhaus in 5000 Radius: Camp (nur 10% Regeneration!)
- Erschöpfte Worker (WorkTime=0): Nur 10% Effizienz!
- SERFS haben KEIN WorkTime-System!
"""

import json
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple
from pathlib import Path


class WorkerState(Enum):
    """Zustände eines Workers."""
    IDLE = "idle"
    WORKING = "working"
    WALKING_TO_FARM = "walking_to_farm"
    EATING = "eating"
    WALKING_TO_RESIDENCE = "walking_to_residence"
    RESTING = "resting"
    WALKING_TO_CAMP = "walking_to_camp"
    CAMPING = "camping"
    WALKING_TO_WORK = "walking_to_work"


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


@dataclass
class WorkTimeParams:
    """WorkTime-Parameter für einen Worker-Typ."""
    work_wait_until: int = 30000  # ms - Zeit pro Arbeitszyklus
    eat_wait: int = 2000  # ms - Zeit zum Essen
    rest_wait: int = 3000  # ms - Zeit zum Ruhen
    work_time_change_work: int = -50  # WorkTime-Änderung pro Zyklus
    work_time_change_farm: float = 0.7  # +70% beim Essen
    work_time_change_residence: float = 0.5  # +50% beim Ruhen
    work_time_change_camp: float = 0.1  # +10% beim Campen
    work_time_max_farm: int = 100  # Max WorkTime-Cap beim Essen
    work_time_max_residence: int = 400  # Max WorkTime-Cap beim Ruhen
    exhausted_malus: float = 0.2  # Effizienz bei Erschöpfung (20%, aus PU_Gunsmith.xml: ExhaustedWorkMotivationMalus=0.2)


# Worker-spezifische Timing-Daten (aus extra2 XMLs - VOLLSTÄNDIG)
# Jeder Worker-Typ hat eigene Parameter!
WORKER_PARAMS: Dict[str, WorkTimeParams] = {
    # FARMER - schneller Arbeitszyklus, Standard-Regeneration
    "farmer": WorkTimeParams(
        work_wait_until=4000,
        exhausted_malus=0.1,  # Nur 10% Malus!
    ),
    # MINER - langer Arbeitszyklus (Bergbau dauert)
    "miner": WorkTimeParams(
        work_wait_until=30000,
        exhausted_malus=0.2,
    ),
    # SAWMILL_WORKER - sehr langer Zyklus
    "sawmill_worker": WorkTimeParams(
        work_wait_until=40000,
        exhausted_malus=0.2,
    ),
    # BRICKMAKER - langer Zyklus (Ziegelherstellung)
    "brickmaker": WorkTimeParams(
        work_wait_until=30000,  # Korrigiert von 40000!
        exhausted_malus=0.2,
    ),
    # STONECUTTER
    "stonecutter": WorkTimeParams(
        work_wait_until=15000,
        exhausted_malus=0.2,
    ),
    # SMITH - langer Zyklus
    "smith": WorkTimeParams(
        work_wait_until=30000,
        exhausted_malus=0.2,
    ),
    # ALCHEMIST - mittlerer Zyklus
    "alchemist": WorkTimeParams(
        work_wait_until=20000,
        exhausted_malus=0.2,
    ),
    # PRIEST
    "priest": WorkTimeParams(
        work_wait_until=4000,
        exhausted_malus=0.2,
    ),
    # TRADER
    "trader": WorkTimeParams(
        work_wait_until=18000,
        exhausted_malus=0.2,
    ),
    # TREASURER
    "treasurer": WorkTimeParams(
        work_wait_until=15000,
        exhausted_malus=0.2,
    ),
    # SMELTER - KORRIGIERT aus extracted_values.json! (war work_wait_until=30000)
    "smelter": WorkTimeParams(
        work_wait_until=4000,  # Korrigiert! (war 30000)
        eat_wait=3000,  # Länger als Standard (2000)!
        rest_wait=2000,  # Kürzer als Standard (3000)!
        exhausted_malus=0.2,
    ),
    # SCHOLAR - Gelehrte (Hochschule)
    "scholar": WorkTimeParams(
        work_wait_until=4000,
        exhausted_malus=0.2,
    ),
    # ENGINEER - SPEZIELL: längere Esszeit, kürzere Ruhezeit!
    "engineer": WorkTimeParams(
        work_wait_until=4000,
        eat_wait=3000,  # Länger als Standard (2000)!
        rest_wait=2000,  # Kürzer als Standard (3000)!
        exhausted_malus=0.2,
    ),
    # MASTER_BUILDER
    "master_builder": WorkTimeParams(
        work_wait_until=4000,
        exhausted_malus=0.2,
    ),
    # GUNSMITH - Büchsenmacher
    "gunsmith": WorkTimeParams(
        work_wait_until=20000,
        exhausted_malus=0.2,
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
        work_time_max_farm=200,  # Höherer Cap
        work_time_max_residence=200,  # Niedrigerer Cap als andere!
        exhausted_malus=0.05,  # Nur 5% Malus - weniger anfällig!
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
}

# Coiner hat spezielle CamperRange (2000 statt 5000)
WORKER_CAMPER_RANGE: Dict[str, int] = {
    "coiner": 2000,  # Muss näher bei Gebäuden sein!
    # Alle anderen: Standard (5000)
}

# Konstanten
CAMPER_RANGE = 5000  # Max-Distanz für Pausen-Gebäude
WORK_TIME_START = 100  # Startwert WorkTime
EXHAUSTED_THRESHOLD = 0  # Ab wann erschöpft


@dataclass
class Farm:
    """Bauernhof für Essen."""
    position: Position
    level: int = 1
    current_eaters: int = 0

    @property
    def eat_capacity(self) -> int:
        """Essen-Kapazität nach Level."""
        return {1: 8, 2: 10, 3: 12}.get(self.level, 8)

    def has_space(self) -> bool:
        return self.current_eaters < self.eat_capacity


@dataclass
class Residence:
    """Wohnhaus für Ruhen."""
    position: Position
    level: int = 1
    current_residents: int = 0

    @property
    def live_capacity(self) -> int:
        """Wohn-Kapazität nach Level."""
        return {1: 6, 2: 9, 3: 12}.get(self.level, 6)

    def has_space(self) -> bool:
        return self.current_residents < self.live_capacity


@dataclass
class Camp:
    """Camp für Notfall-Pausen (nur +10% WorkTime)."""
    position: Position


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

    def __post_init__(self):
        """Initialisiert Worker-spezifische Parameter."""
        self.params = WORKER_PARAMS.get(self.worker_type, WorkTimeParams())
        self.speed = WORKER_SPEEDS.get(self.worker_type, 320)
        self.has_worktime_system = self.worker_type != "serf"

    def tick(self, dt: float, farms: List[Farm], residences: List[Residence], camps: List[Camp],
             motivation_mod: float = 1.0):
        """
        Simuliert einen Zeitschritt.

        Args:
            dt: Delta-Zeit in Sekunden
            farms: Liste aller Farms
            residences: Liste aller Wohnhäuser
            camps: Liste aller Camps
            motivation_mod: Motivation-Modifier für Regeneration (1.0 = normal)
        """
        if not self.has_worktime_system:
            # Serfs arbeiten ENDLOS ohne Pausen!
            self.state = WorkerState.WORKING
            return

        if self.state == WorkerState.WORKING:
            self._tick_working(dt, farms)

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
            self._tick_camping(dt, motivation_mod)

        elif self.state == WorkerState.WALKING_TO_WORK:
            self._tick_walking(dt, WorkerState.WORKING)

        elif self.state == WorkerState.IDLE:
            # Idle Worker starten Arbeit
            self.state = WorkerState.WORKING
            self.state_timer = 0.0

    def _tick_working(self, dt: float, farms: List[Farm]):
        """Arbeits-Phase."""
        self.state_timer += dt * 1000  # ms

        # WorkTime sinkt kontinuierlich
        work_progress = (dt * 1000) / self.params.work_wait_until
        self.work_time += self.params.work_time_change_work * work_progress

        # Hunger-Check: Nach einem Arbeitszyklus oder wenn WorkTime niedrig
        if self.state_timer >= self.params.work_wait_until or self.work_time <= 20:
            self._find_farm(farms)
            self.state_timer = 0.0

    def _tick_eating(self, dt: float, residences: List[Residence], motivation_mod: float = 1.0):
        """Essen-Phase."""
        self.state_timer += dt * 1000  # ms

        if self.state_timer >= self.params.eat_wait:
            # WorkTime regenerieren: +70% von (Max - Aktuell) × Motivation
            max_val = self.params.work_time_max_farm
            regen_rate = self.params.work_time_change_farm * motivation_mod
            self.work_time += regen_rate * (max_val - self.work_time)

            # Farm freigeben
            if self.assigned_farm:
                self.assigned_farm.current_eaters -= 1
                self.assigned_farm = None

            # Nächstes: Wohnhaus suchen
            self._find_residence(residences)
            self.state_timer = 0.0

    def _tick_resting(self, dt: float, motivation_mod: float = 1.0):
        """Ruhe-Phase."""
        self.state_timer += dt * 1000  # ms

        if self.state_timer >= self.params.rest_wait:
            # WorkTime regenerieren: +50% von (Max - Aktuell) × Motivation
            max_val = self.params.work_time_max_residence
            regen_rate = self.params.work_time_change_residence * motivation_mod
            self.work_time += regen_rate * (max_val - self.work_time)

            # Wohnhaus freigeben
            if self.assigned_residence:
                self.assigned_residence.current_residents -= 1
                self.assigned_residence = None

            # Zurück zur Arbeit
            self._return_to_work()
            self.state_timer = 0.0

    def _tick_camping(self, dt: float, motivation_mod: float = 1.0):
        """Camping-Phase (Notfall - nur +10% Regeneration)."""
        self.state_timer += dt * 1000  # ms

        # Camping dauert so lange wie Essen + Ruhen zusammen
        camp_duration = self.params.eat_wait + self.params.rest_wait

        if self.state_timer >= camp_duration:
            # Nur +10% Regeneration × Motivation
            max_val = self.params.work_time_max_farm
            regen_rate = self.params.work_time_change_camp * motivation_mod
            self.work_time += regen_rate * (max_val - self.work_time)

            # Zurück zur Arbeit
            self._return_to_work()
            self.state_timer = 0.0

    def _tick_walking(self, dt: float, next_state: WorkerState):
        """Lauf-Phase."""
        if self.target_position is None:
            self.state = next_state
            return

        distance = self.position.distance_to(self.target_position)
        walk_distance = self.speed * dt

        if walk_distance >= distance:
            # Angekommen
            self.position = Position(self.target_position.x, self.target_position.y)
            self.target_position = None
            self.state = next_state
            self.state_timer = 0.0
        else:
            # Noch unterwegs - Position updaten
            ratio = walk_distance / distance
            self.position.x += ratio * (self.target_position.x - self.position.x)
            self.position.y += ratio * (self.target_position.y - self.position.y)

    def _get_camper_range(self) -> int:
        """Gibt die Worker-spezifische CamperRange zurück."""
        return WORKER_CAMPER_RANGE.get(self.worker_type, CAMPER_RANGE)

    def _find_farm(self, farms: List[Farm]):
        """Findet nächsten Bauernhof in Worker-spezifischer CAMPER_RANGE."""
        nearest = None
        camper_range = self._get_camper_range()
        min_dist = camper_range

        for farm in farms:
            if farm.has_space():
                dist = self.position.distance_to(farm.position)
                if dist < min_dist:
                    nearest = farm
                    min_dist = dist

        if nearest:
            self.target_position = nearest.position
            self.state = WorkerState.WALKING_TO_FARM
            self.assigned_farm = nearest
            nearest.current_eaters += 1
        else:
            # Kein Bauernhof in Reichweite -> Camp suchen
            self._go_to_camp()

    def _find_residence(self, residences: List[Residence]):
        """Findet nächstes Wohnhaus in Worker-spezifischer CAMPER_RANGE."""
        nearest = None
        camper_range = self._get_camper_range()
        min_dist = camper_range

        for residence in residences:
            if residence.has_space():
                dist = self.position.distance_to(residence.position)
                if dist < min_dist:
                    nearest = residence
                    min_dist = dist

        if nearest:
            self.target_position = nearest.position
            self.state = WorkerState.WALKING_TO_RESIDENCE
            self.assigned_residence = nearest
            nearest.current_residents += 1
        else:
            # Kein Wohnhaus in Reichweite -> Direkt zur Arbeit
            self._return_to_work()

    def _go_to_camp(self):
        """Geht zum Camp (Notfall-Pause mit nur +10%)."""
        # Vereinfacht: Camp ist am Arbeitsplatz
        self.target_position = self.workplace_position
        self.state = WorkerState.WALKING_TO_CAMP

    def _return_to_work(self):
        """Kehrt zum Arbeitsplatz zurück."""
        self.target_position = self.workplace_position
        self.state = WorkerState.WALKING_TO_WORK

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
            # Erschöpft = nur 10% Effizienz
            return self.params.exhausted_malus

        # Volle Effizienz
        return 1.0

    def is_working(self) -> bool:
        """Prüft ob Worker gerade arbeitet."""
        return self.state == WorkerState.WORKING

    def is_exhausted(self) -> bool:
        """Prüft ob Worker erschöpft ist."""
        return self.work_time <= EXHAUSTED_THRESHOLD


@dataclass
class WorkforceManager:
    """
    Verwaltet alle Arbeiter mit Kapazitäten und Laufwegen.

    Trackt:
    - Alle Worker mit WorkTime-Status
    - Alle Farms mit Essen-Kapazität
    - Alle Wohnhäuser mit Wohn-Kapazität
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

    def set_motivation_modifier(self, motivation: float):
        """Setzt den globalen Motivation-Modifier für alle Worker.

        Höhere Motivation = schnellere WorkTime-Regeneration.
        """
        self.motivation_modifier = motivation

    def tick(self, dt: float):
        """Simuliert alle Worker für einen Zeitschritt."""
        for worker in self.workers:
            worker.tick(dt, self.farms, self.residences, self.camps,
                       motivation_mod=self.motivation_modifier)

    def set_village_capacity(self, capacity: int):
        """Setzt die maximale Worker-Kapazität basierend auf Dorfzentren."""
        self.max_workers_from_village = capacity

    def add_worker(self, worker_type: str, position: Position, workplace: Position) -> Optional[Worker]:
        """
        Fügt einen neuen Worker hinzu, wenn Dorfzentrum-Kapazität verfügbar.

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
        """Prüft ob Dorfzentrum-Kapazität für einen weiteren Worker verfügbar ist.
        Wohnhäuser begrenzen NICHT die Bevölkerung - nur Dorfzentren!"""
        current_workers = len([w for w in self.workers if w.worker_type != "serf"])
        return current_workers < self.max_workers_from_village

    def add_farm(self, position: Position, level: int = 1) -> Farm:
        """Fügt einen Bauernhof hinzu."""
        farm = Farm(position=position, level=level)
        self.farms.append(farm)
        return farm

    def add_residence(self, position: Position, level: int = 1) -> Residence:
        """Fügt ein Wohnhaus hinzu."""
        residence = Residence(position=position, level=level)
        self.residences.append(residence)
        return residence

    def add_camp(self, position: Position) -> Camp:
        """Fügt ein Camp hinzu."""
        camp = Camp(position=position)
        self.camps.append(camp)
        return camp

    # ==================== STATISTIKEN ====================

    def get_total_residence_capacity(self) -> int:
        """Gesamt-Wohnkapazität."""
        return sum(r.live_capacity for r in self.residences)

    def get_total_farm_capacity(self) -> int:
        """Gesamt-Essen-Kapazität."""
        return sum(f.eat_capacity for f in self.farms)

    def get_current_workers(self) -> int:
        """Anzahl aktuelle Worker (ohne Serfs)."""
        return len([w for w in self.workers if w.worker_type != "serf"])

    def get_working_workers(self) -> int:
        """Anzahl arbeitender Worker."""
        return len([w for w in self.workers if w.is_working()])

    def get_exhausted_workers(self) -> int:
        """Anzahl erschöpfter Worker."""
        return len([w for w in self.workers if w.is_exhausted()])

    def get_average_efficiency(self) -> float:
        """Durchschnittliche Effizienz aller Worker."""
        if not self.workers:
            return 1.0
        return sum(w.get_efficiency() for w in self.workers) / len(self.workers)

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
        """Auslastung der Wohnhäuser (0.0 - 1.0)."""
        capacity = self.get_total_residence_capacity()
        if capacity == 0:
            return 1.0
        return self.get_current_workers() / capacity

    def get_farm_utilization(self) -> float:
        """Auslastung der Bauernhöfe (0.0 - 1.0)."""
        capacity = self.get_total_farm_capacity()
        if capacity == 0:
            return 1.0
        eating = len([w for w in self.workers if w.state == WorkerState.EATING])
        return eating / capacity

    def get_exhausted_ratio(self) -> float:
        """Anteil der erschöpften Worker (0.0 - 1.0)."""
        if len(self.workers) == 0:
            return 0.0
        return self.get_exhausted_workers() / len(self.workers)

    def get_stats(self) -> Dict[str, float]:
        """Gibt alle wichtigen Statistiken zurück."""
        # Zähle Worker nach Zustand
        eating_workers = len([w for w in self.workers if w.state == WorkerState.EATING])
        resting_workers = len([w for w in self.workers if w.state == WorkerState.RESTING])
        walking_workers = len([w for w in self.workers if w.state in [
            WorkerState.WALKING_TO_FARM, WorkerState.WALKING_TO_RESIDENCE, WorkerState.WALKING_TO_CAMP
        ]])
        camping_workers = len([w for w in self.workers if w.state == WorkerState.CAMPING])

        return {
            "total_workers": len(self.workers),
            "working_workers": self.get_working_workers(),
            "eating_workers": eating_workers,
            "resting_workers": resting_workers,
            "walking_workers": walking_workers,
            "camping_workers": camping_workers,
            "exhausted_workers": self.get_exhausted_workers(),
            "exhausted_ratio": self.get_exhausted_ratio(),
            "average_efficiency": self.get_average_efficiency(),
            "avg_work_time": self.get_average_worktime(),  # Alias für environment.py
            "average_worktime": self.get_average_worktime(),
            "residence_capacity": self.get_total_residence_capacity(),
            "residence_utilization": self.get_residence_utilization(),
            "farm_capacity": self.get_total_farm_capacity(),
            "farm_utilization": self.get_farm_utilization(),
        }


# ==================== HELPER FUNCTIONS ====================

def load_worker_params_from_game_data(game_data_path: str) -> Dict[str, WorkTimeParams]:
    """Lädt Worker-Parameter aus der extrahierten game_data.json."""
    with open(game_data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    params = {}
    for worker_name, worker_data in data.get("workers", {}).items():
        if worker_data.get("has_worktime_system", False):
            wt = worker_data.get("worktime", {})
            params[worker_name] = WorkTimeParams(
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

    # Gebäude hinzufügen
    manager.add_residence(Position(0, 0), level=1)  # 6 Plätze
    manager.add_farm(Position(500, 0), level=1)  # 8 Esser

    # Worker hinzufügen
    for i in range(3):
        manager.add_worker("miner", Position(1000, i * 100), Position(1000, i * 100))

    print(f"Initial: {manager.get_stats()}\n")

    # Simulation für 60 Sekunden
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
