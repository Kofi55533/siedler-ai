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
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from worker_simulation import Position, Worker, WorkerState, WorkforceManager


class ResourceType(Enum):
    """Ressourcen-Typen."""
    GOLD = "gold"
    WOOD = "wood"
    STONE = "stone"
    CLAY = "clay"
    IRON = "iron"
    SULFUR = "sulfur"


# Serf-Extraktion (aus extra2 XMLs)
# VOLLSTÄNDIG: Delay + Animation-Zeit = Gesamtzeit pro Extraktion
# Animation-Zeiten aus TL_SERF_EXTRACT_*.xml:
#   - Holz: 520ms + 1000ms = 1.52s Animation
#   - Minen: 540ms + 1000ms = 1.54s Animation
SERF_EXTRACTION = {
    ResourceType.IRON: {"delay": 3.0, "animation": 1.54, "amount": 1},    # Total: 4.54s
    ResourceType.STONE: {"delay": 4.0, "animation": 1.54, "amount": 1},   # Total: 5.54s
    ResourceType.CLAY: {"delay": 4.0, "animation": 1.54, "amount": 1},    # Total: 5.54s
    ResourceType.SULFUR: {"delay": 3.0, "animation": 1.54, "amount": 1},  # Total: 4.54s
    ResourceType.WOOD: {"delay": 4.0, "animation": 1.52, "amount": 2},    # Total: 5.52s, gibt 2 Holz!
}

# ResourceSearchRadius für Serfs (aus PU_Serf.xml)
SERF_RESOURCE_SEARCH_RADIUS = 4500  # cm - Serfs suchen Ressourcen in diesem Radius


@dataclass
class Mine:
    """
    Tier 1: Mine (CMineBehavior)

    - Worker arbeiten lokal
    - Produktion = Workers × AmountToMine × Effizienz
    """
    name: str
    position: Position
    resource_type: ResourceType
    level: int = 1
    max_workers: int = 5
    current_workers: int = 0
    amount_to_mine: int = 4  # Pro Arbeitszyklus

    @property
    def workers_by_level(self) -> int:
        """Max Workers nach Level."""
        base = {1: 5, 2: 6, 3: 7}
        return base.get(self.level, 5)

    @property
    def amount_by_level(self) -> int:
        """AmountToMine nach Level."""
        base = {1: 4, 2: 5, 3: 6}
        return base.get(self.level, 4)

    def get_production_rate(self, worker_efficiency: float) -> float:
        """
        Berechnet Produktionsrate pro Sekunde.

        Formel: Workers × AmountToMine × Effizienz / WorkWaitUntil
        WorkWaitUntil für Miner = 30 Sekunden
        """
        if self.current_workers == 0:
            return 0.0

        work_cycle = 30.0  # Sekunden (aus XML)
        return (self.current_workers * self.amount_by_level * worker_efficiency) / work_cycle


@dataclass
class Refiner:
    """
    Tier 2: Refiner (CResourceRefinerBehavior)

    - Worker holt Rohstoffe von Supplier
    - Laufzeit abhängig von Distanz
    - Verarbeitung mit InitialFactor
    """
    name: str
    position: Position
    resource_type: ResourceType
    input_resource: ResourceType
    supplier_position: Position
    level: int = 1
    max_workers: int = 4
    current_workers: int = 0
    initial_factor: int = 4  # Umwandlungsrate
    transport_amount: int = 5  # Pro Trip
    worker_speed: int = 320

    def get_cycle_time(self) -> float:
        """
        Berechnet Zykluszeit für einen Transport-Zyklus.

        Zyklus = Hin + Verarbeitung + Zurück
        """
        distance = self.position.distance_to(self.supplier_position)
        walk_time = (distance * 2) / self.worker_speed  # Hin und zurück
        work_time = 5.0  # Verarbeitungszeit (geschätzt)
        return walk_time + work_time

    def get_production_rate(self, worker_efficiency: float) -> float:
        """
        Berechnet Produktionsrate pro Sekunde.

        Formel: Workers × TransportAmount × Effizienz / CycleTime
        """
        if self.current_workers == 0:
            return 0.0

        cycle_time = self.get_cycle_time()
        if cycle_time <= 0:
            return 0.0

        return (self.current_workers * self.transport_amount * worker_efficiency) / cycle_time

    def get_input_consumption_rate(self, worker_efficiency: float) -> float:
        """
        Berechnet Input-Verbrauch pro Sekunde.

        InitialFactor gibt das Verhältnis an (z.B. 4 = 4:1)
        """
        production = self.get_production_rate(worker_efficiency)
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
    extraction_timer: float = 0.0
    state: SerfState = SerfState.IDLE
    speed: int = 400  # Serf-Geschwindigkeit (aus PU_Serf.xml: Speed=400)
    tree_id: Optional[int] = None  # ID des zugewiesenen Baums (für Holz)
    # NEU: Unterscheidung zwischen Vorkommen und Mine
    work_location: Optional[str] = None  # "deposit", "mine", oder "wood"
    # NEU: Bau-spezifische Felder
    build_target: Optional[str] = None  # Name des zu bauenden Gebäudes
    build_site_id: Optional[int] = None  # ID des Bauplatzes

    def tick(self, dt: float) -> Optional[Tuple[ResourceType, int]]:
        """
        Simuliert einen Zeitschritt.

        Returns:
            (ResourceType, Menge) wenn Extraktion fertig, sonst None
            Für Bau-States wird ("BUILD", build_progress) zurückgegeben
        """
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
        if self.target_position is None:
            self.state = SerfState.IDLE
            return None

        # Distanz berechnen
        distance = self.position.distance_to(self.target_position)
        walk_distance = self.speed * dt

        if walk_distance >= distance:
            # Angekommen! Starte Extraktion
            self.position = Position(self.target_position.x, self.target_position.y)
            self.state = SerfState.EXTRACTING
            self.extraction_timer = 0.0
        else:
            # Noch unterwegs - Position updaten
            ratio = walk_distance / distance
            self.position.x += ratio * (self.target_position.x - self.position.x)
            self.position.y += ratio * (self.target_position.y - self.position.y)

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
        if self.target_position is None:
            self.state = SerfState.IDLE
            return None

        # Distanz berechnen
        distance = self.position.distance_to(self.target_position)
        walk_distance = self.speed * dt

        if walk_distance >= distance:
            # Angekommen! Starte Bau
            self.position = Position(self.target_position.x, self.target_position.y)
            self.state = SerfState.BUILDING
        else:
            # Noch unterwegs - Position updaten
            ratio = walk_distance / distance
            self.position.x += ratio * (self.target_position.x - self.position.x)
            self.position.y += ratio * (self.target_position.y - self.position.y)

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
                        start_position: Position, build_site_id: int = None):
        """
        Weist Leibeigenen einem Bauprojekt zu.

        Args:
            building_name: Name des zu bauenden Gebäudes
            build_position: Position des Bauplatzes
            start_position: Aktuelle Position des Leibeigenen
            build_site_id: ID des Bauplatzes (für Tracking)
        """
        self.build_target = building_name
        self.target_position = build_position
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

    def assign_to_resource(self, resource: ResourceType, resource_position: Position,
                           start_position: Position, path_distance: float = None,
                           tree_id: int = None):
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
        self.target_position = resource_position
        self.position = start_position
        self.state = SerfState.WALKING_TO_RESOURCE
        self.extraction_timer = 0.0

        # NEU: Speichere exakte Pfaddistanz wenn verfügbar
        self.path_distance = path_distance

        # NEU: Speichere Baum-ID für Holz-Extraktion
        self.tree_id = tree_id if resource == ResourceType.WOOD else None

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

        return distance / self.speed

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

    def is_extracting(self) -> bool:
        """Prüft ob Leibeigener gerade extrahiert."""
        return self.state == SerfState.EXTRACTING

    def is_walking(self) -> bool:
        """Prüft ob Leibeigener gerade zur Ressource läuft."""
        return self.state == SerfState.WALKING_TO_RESOURCE

    def is_idle(self) -> bool:
        """Prüft ob Leibeigener untätig ist."""
        return self.state == SerfState.IDLE

    # Legacy-Kompatibilität
    def start_extraction(self, resource: ResourceType, position: Position):
        """Legacy: Startet Extraktion sofort an Position."""
        self.assign_to_resource(resource, position, position)
        self.state = SerfState.EXTRACTING  # Sofort extrahieren

    def stop_extraction(self):
        """Legacy: Stoppt Extraktion."""
        self.stop()


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

    def tick(self, dt: float) -> Dict[ResourceType, float]:
        """
        Simuliert einen Zeitschritt für alle Produktions-Einheiten.

        Args:
            dt: Delta-Zeit in Sekunden

        Returns:
            Dict mit produzierten Ressourcen in diesem Tick
        """
        produced = {r: 0.0 for r in ResourceType}

        # Worker-Effizienz holen
        efficiency = 1.0
        if self.workforce_manager:
            efficiency = self.workforce_manager.get_average_efficiency()

        # Minen produzieren
        mine_production = self._tick_mines(dt, efficiency)
        for resource, amount in mine_production.items():
            produced[resource] += amount
            self.resources[resource] += amount

        # Refiner produzieren
        refiner_production = self._tick_refiners(dt, efficiency)
        for resource, amount in refiner_production.items():
            produced[resource] += amount
            self.resources[resource] += amount

        # Serfs extrahieren
        serf_production = self._tick_serfs(dt)
        for resource, amount in serf_production.items():
            produced[resource] += amount
            self.resources[resource] += amount

        return produced

    def _tick_mines(self, dt: float, efficiency: float) -> Dict[ResourceType, float]:
        """Tick für alle Minen."""
        production = {}

        for mine in self.mines.values():
            rate = mine.get_production_rate(efficiency)
            amount = rate * dt

            if mine.resource_type not in production:
                production[mine.resource_type] = 0.0
            production[mine.resource_type] += amount

        return production

    def _tick_refiners(self, dt: float, efficiency: float) -> Dict[ResourceType, float]:
        """Tick für alle Refiner."""
        production = {}

        for refiner in self.refiners.values():
            # Prüfen ob genug Input-Ressource vorhanden
            input_rate = refiner.get_input_consumption_rate(efficiency)
            input_needed = input_rate * dt

            available = self.resources.get(refiner.input_resource, 0)
            if available < input_needed:
                # Nicht genug Input - proportional reduzieren
                if input_needed > 0:
                    ratio = available / input_needed
                else:
                    ratio = 0
                input_needed = available
            else:
                ratio = 1.0

            # Input verbrauchen
            self.resources[refiner.input_resource] -= input_needed

            # Output produzieren
            output_rate = refiner.get_production_rate(efficiency)
            amount = output_rate * dt * ratio

            if refiner.resource_type not in production:
                production[refiner.resource_type] = 0.0
            production[refiner.resource_type] += amount

        return production

    def _tick_serfs(self, dt: float) -> Dict[ResourceType, float]:
        """Tick für alle Serfs."""
        production = {}

        for serf in self.serfs:
            result = serf.tick(dt)
            if result:
                resource, amount = result
                # BUILD-Ergebnisse ignorieren - werden in environment.py behandelt
                if resource == "BUILD":
                    continue
                if resource not in production:
                    production[resource] = 0.0
                production[resource] += amount

        return production

    # ==================== GEBÄUDE-MANAGEMENT ====================

    def add_mine(self, name: str, position: Position, resource: ResourceType, level: int = 1) -> Mine:
        """Fügt eine Mine hinzu."""
        mine = Mine(
            name=name,
            position=position,
            resource_type=resource,
            level=level,
        )
        self.mines[name] = mine
        return mine

    def add_refiner(self, name: str, position: Position, output: ResourceType,
                    input_res: ResourceType, supplier_pos: Position,
                    initial_factor: int = 4, level: int = 1) -> Refiner:
        """Fügt einen Refiner hinzu."""
        refiner = Refiner(
            name=name,
            position=position,
            resource_type=output,
            input_resource=input_res,
            supplier_position=supplier_pos,
            initial_factor=initial_factor,
            level=level,
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

    def get_production_rates(self, efficiency: float = 1.0) -> Dict[ResourceType, float]:
        """Gibt Produktionsraten pro Sekunde für alle Ressourcen zurück."""
        rates = {r: 0.0 for r in ResourceType}

        for mine in self.mines.values():
            rate = mine.get_production_rate(efficiency)
            rates[mine.resource_type] += rate

        for refiner in self.refiners.values():
            rate = refiner.get_production_rate(efficiency)
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

    def get_consumption_rates(self, efficiency: float = 1.0) -> Dict[ResourceType, float]:
        """Gibt Verbrauchsraten pro Sekunde für alle Ressourcen zurück."""
        rates = {r: 0.0 for r in ResourceType}

        for refiner in self.refiners.values():
            rate = refiner.get_input_consumption_rate(efficiency)
            rates[refiner.input_resource] += rate

        return rates

    def get_net_rates(self, efficiency: float = 1.0) -> Dict[ResourceType, float]:
        """Gibt Netto-Raten (Produktion - Verbrauch) zurück."""
        production = self.get_production_rates(efficiency)
        consumption = self.get_consumption_rates(efficiency)

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
