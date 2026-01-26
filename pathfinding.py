# -*- coding: utf-8 -*-
"""
Pfadfindung und Karten-Management für Siedler AI.

Dieses Modul enthält:
1. WalkableGrid - Verwaltet begehbare/blockierte Flächen
2. A* Pathfinding - Findet optimale Wege
3. BuildingManager - Verwaltet Gebäude und deren Blockierungen
4. Bauplatz-Validierung - Prüft ob Gebäude platziert werden können
"""

import numpy as np
import heapq
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Set
from enum import IntEnum
import json
import os

# =============================================================================
# KONSTANTEN
# =============================================================================

# Grid-Skalierung (aus der Kartenanalyse)
SCALE_X = 33.5  # 1 Grid-Pixel = 33.5 Spieleinheiten
SCALE_Y = 33.8  # 1 Grid-Pixel = 33.8 Spieleinheiten

# Gebäudegrößen in Spieleinheiten
BUILDING_SIZES = {
    # Kleine Gebäude
    "Wohnhaus": 400,
    "Bauernhof": 400,
    "Sägewerk": 400,
    "Steinmetz": 400,
    "Ziegelei": 400,
    "Alchemist": 400,

    # Mittlere Gebäude
    "Hochschule": 600,
    "Schmiede": 600,
    "Kaserne": 600,
    "Bogenmacher": 600,
    "Büchsenmacherei": 600,
    "Kirche": 600,
    "Bank": 600,

    # Große Gebäude
    "Hauptquartier": 800,
    "Dorfzentrum": 800,

    # Minen (feste Positionen)
    "Steinmine": 400,
    "Eisenmine": 400,
    "Lehmmine": 400,
    "Schwefelmine": 400,
}

# Bewegungsrichtungen für A* (8-direktional)
DIRECTIONS = [
    (0, 1),   # rechts
    (1, 0),   # unten
    (0, -1),  # links
    (-1, 0),  # oben
    (1, 1),   # diagonal unten-rechts
    (1, -1),  # diagonal unten-links
    (-1, 1),  # diagonal oben-rechts
    (-1, -1), # diagonal oben-links
]

# Bewegungskosten
COST_STRAIGHT = 10
COST_DIAGONAL = 14  # ~sqrt(2) * 10

# =============================================================================
# HILFSKLASSEN
# =============================================================================

class CellType(IntEnum):
    """Zellentypen im Grid."""
    WALKABLE = 0
    BLOCKED_TERRAIN = 1  # Berg, Wasser (permanent)
    BLOCKED_BUILDING = 2  # Gebäude (dynamisch)
    BLOCKED_TREE = 3      # Baum (dynamisch, kann gefällt werden)
    BLOCKED_RESOURCE = 4  # Ressourcen-Vorkommen


@dataclass
class GridPosition:
    """Position im Grid (Pixel-Koordinaten)."""
    x: int
    y: int

    def to_world(self) -> Tuple[float, float]:
        """Konvertiert zu Welt-Koordinaten."""
        return (self.x * SCALE_X, self.y * SCALE_Y)

    @staticmethod
    def from_world(world_x: float, world_y: float) -> 'GridPosition':
        """Erstellt GridPosition aus Welt-Koordinaten."""
        return GridPosition(
            x=int(world_x / SCALE_X),
            y=int(world_y / SCALE_Y)
        )

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


@dataclass
class PathResult:
    """Ergebnis einer Pfadsuche."""
    found: bool
    path: List[GridPosition] = field(default_factory=list)
    grid_distance: int = 0  # Distanz in Grid-Schritten
    world_distance: float = 0.0  # Distanz in Spieleinheiten

    def get_world_path(self) -> List[Tuple[float, float]]:
        """Gibt den Pfad in Welt-Koordinaten zurück."""
        return [pos.to_world() for pos in self.path]


# =============================================================================
# WALKABLE GRID
# =============================================================================

class WalkableGrid:
    """
    Verwaltet die begehbaren und blockierten Flächen der Karte.

    Das Grid hat mehrere Layer:
    - terrain_base: Statische Terrain-Blockierungen (Berge, Wasser)
    - buildings: Dynamische Gebäude-Blockierungen
    - trees: Dynamische Baum-Blockierungen
    - resources: Ressourcen-Positionen (Vorkommen)
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        # Basis-Terrain (statisch)
        self.terrain_base = np.ones((height, width), dtype=np.uint8)

        # Dynamische Layer
        self.buildings = np.zeros((height, width), dtype=np.uint8)
        self.trees = np.zeros((height, width), dtype=np.uint8)
        self.resources = np.zeros((height, width), dtype=np.uint8)

        # Gebäude-Tracking
        self.building_positions: Dict[int, Tuple[GridPosition, str, int]] = {}
        self.next_building_id = 1

        # Baum-Tracking
        self.tree_positions: Dict[int, GridPosition] = {}
        self.next_tree_id = 1

        # Cache für Pfade (optional)
        self.path_cache: Dict[Tuple[GridPosition, GridPosition], PathResult] = {}
        self.cache_valid = True

    def copy_fresh(self) -> 'WalkableGrid':
        """Erstellt eine frische Kopie mit nur dem Basis-Terrain (für schnelles Reset)."""
        new_grid = WalkableGrid(self.width, self.height)
        new_grid.terrain_base = self.terrain_base.copy()  # Statisches Terrain kopieren
        # Dynamische Layer bleiben leer (buildings, trees, resources = 0)
        return new_grid

    def load_terrain_from_file(self, terrain_file: str, walkable_threshold: Tuple[int, int] = (100, 160)):
        """
        Lädt Terrain-Daten aus einer Binärdatei.

        Args:
            terrain_file: Pfad zur Terrain-Datei (file_0.bin)
            walkable_threshold: (min, max) Werte für begehbares Terrain
        """
        with open(terrain_file, 'rb') as f:
            data = f.read()

        terrain = np.frombuffer(data, dtype=np.uint8)

        # Reshape auf Grid-Größe
        if len(terrain) == self.width * self.height:
            terrain = terrain.reshape((self.height, self.width))
        else:
            # Versuche passende Dimensionen zu finden
            total = len(terrain)
            # Bekannte Größe: 1508 x 1496 = 2,255,968
            if total == 2255968:
                terrain = terrain.reshape((1496, 1508))
                # Resize wenn nötig
                if terrain.shape != (self.height, self.width):
                    from scipy.ndimage import zoom
                    zoom_y = self.height / terrain.shape[0]
                    zoom_x = self.width / terrain.shape[1]
                    terrain = zoom(terrain, (zoom_y, zoom_x), order=0)

        # Setze begehbare Bereiche
        min_val, max_val = walkable_threshold
        self.terrain_base = ((terrain >= min_val) & (terrain <= max_val)).astype(np.uint8)

        print(f"Terrain geladen: {self.width}x{self.height}")
        print(f"  Begehbar: {np.sum(self.terrain_base)} Pixel ({100*np.mean(self.terrain_base):.1f}%)")

    def load_terrain_from_array(self, walkable_array: np.ndarray):
        """Lädt Terrain direkt aus einem NumPy Array."""
        if walkable_array.shape != (self.height, self.width):
            raise ValueError(f"Array-Größe {walkable_array.shape} passt nicht zu Grid {self.height}x{self.width}")
        self.terrain_base = walkable_array.astype(np.uint8)

    def is_walkable(self, x: int, y: int) -> bool:
        """Prüft ob eine Zelle begehbar ist."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        return (self.terrain_base[y, x] == 1 and
                self.buildings[y, x] == 0 and
                self.trees[y, x] == 0)

    def is_walkable_pos(self, pos: GridPosition) -> bool:
        """Prüft ob eine GridPosition begehbar ist."""
        return self.is_walkable(pos.x, pos.y)

    def get_walkable_grid(self) -> np.ndarray:
        """Gibt das kombinierte begehbare Grid zurück."""
        return (self.terrain_base &
                (1 - self.buildings) &
                (1 - self.trees)).astype(np.uint8)

    # -------------------------------------------------------------------------
    # Gebäude-Management
    # -------------------------------------------------------------------------

    def add_building(self, world_x: float, world_y: float, building_type: str) -> int:
        """
        Fügt ein Gebäude hinzu und blockiert die entsprechenden Zellen.

        Returns:
            Building ID für späteres Entfernen
        """
        size = BUILDING_SIZES.get(building_type, 400)
        size_in_grid = max(1, int(size / SCALE_X))

        # Grid-Position (Zentrum)
        center = GridPosition.from_world(world_x, world_y)

        # Blockiere alle Zellen im Bereich
        half_size = size_in_grid // 2
        for dy in range(-half_size, half_size + 1):
            for dx in range(-half_size, half_size + 1):
                gx, gy = center.x + dx, center.y + dy
                if 0 <= gx < self.width and 0 <= gy < self.height:
                    self.buildings[gy, gx] = 1

        # Tracking
        building_id = self.next_building_id
        self.next_building_id += 1
        self.building_positions[building_id] = (center, building_type, size_in_grid)

        # Cache invalidieren
        self.cache_valid = False

        return building_id

    def remove_building(self, building_id: int):
        """Entfernt ein Gebäude und gibt die Zellen frei."""
        if building_id not in self.building_positions:
            return

        center, building_type, size_in_grid = self.building_positions[building_id]

        half_size = size_in_grid // 2
        for dy in range(-half_size, half_size + 1):
            for dx in range(-half_size, half_size + 1):
                gx, gy = center.x + dx, center.y + dy
                if 0 <= gx < self.width and 0 <= gy < self.height:
                    self.buildings[gy, gx] = 0

        del self.building_positions[building_id]
        self.cache_valid = False

    # -------------------------------------------------------------------------
    # Baum-Management
    # -------------------------------------------------------------------------

    def add_tree(self, world_x: float, world_y: float) -> int:
        """Fügt einen Baum hinzu."""
        pos = GridPosition.from_world(world_x, world_y)

        if 0 <= pos.x < self.width and 0 <= pos.y < self.height:
            self.trees[pos.y, pos.x] = 1

        tree_id = self.next_tree_id
        self.next_tree_id += 1
        self.tree_positions[tree_id] = pos

        self.cache_valid = False
        return tree_id

    def add_trees_batch(self, tree_list: List[Dict]) -> List[int]:
        """Fügt mehrere Bäume auf einmal hinzu (effizienter)."""
        tree_ids = []
        for tree in tree_list:
            tree_id = self.add_tree(tree["x"], tree["y"])
            tree_ids.append(tree_id)
        return tree_ids

    def remove_tree(self, tree_id: int):
        """Entfernt einen Baum (gefällt)."""
        if tree_id not in self.tree_positions:
            return

        pos = self.tree_positions[tree_id]
        if 0 <= pos.x < self.width and 0 <= pos.y < self.height:
            self.trees[pos.y, pos.x] = 0

        del self.tree_positions[tree_id]
        self.cache_valid = False

    def get_nearest_tree(self, world_x: float, world_y: float) -> Optional[Tuple[int, float]]:
        """Findet den nächsten Baum zu einer Position."""
        if not self.tree_positions:
            return None

        start = GridPosition.from_world(world_x, world_y)

        min_dist = float('inf')
        nearest_id = None

        for tree_id, pos in self.tree_positions.items():
            dist = abs(pos.x - start.x) + abs(pos.y - start.y)  # Manhattan
            if dist < min_dist:
                min_dist = dist
                nearest_id = tree_id

        if nearest_id is not None:
            world_dist = min_dist * ((SCALE_X + SCALE_Y) / 2)
            return (nearest_id, world_dist)
        return None

    # -------------------------------------------------------------------------
    # Bauplatz-Validierung
    # -------------------------------------------------------------------------

    def can_build_at(self, world_x: float, world_y: float, building_type: str) -> bool:
        """
        Prüft ob ein Gebäude an einer Position gebaut werden kann.

        Bedingungen:
        1. Alle Zellen im Bereich müssen terrain-begehbar sein
        2. Keine anderen Gebäude im Weg
        3. Keine Bäume im Weg (müssen erst gefällt werden)
        """
        size = BUILDING_SIZES.get(building_type, 400)
        size_in_grid = max(1, int(size / SCALE_X))

        center = GridPosition.from_world(world_x, world_y)
        half_size = size_in_grid // 2

        for dy in range(-half_size, half_size + 1):
            for dx in range(-half_size, half_size + 1):
                gx, gy = center.x + dx, center.y + dy

                # Außerhalb der Karte?
                if not (0 <= gx < self.width and 0 <= gy < self.height):
                    return False

                # Terrain nicht begehbar?
                if self.terrain_base[gy, gx] == 0:
                    return False

                # Gebäude im Weg?
                if self.buildings[gy, gx] == 1:
                    return False

        return True

    def get_trees_blocking_building(self, world_x: float, world_y: float,
                                     building_type: str) -> List[int]:
        """Gibt Liste der Bäume zurück, die für den Bau gefällt werden müssen."""
        size = BUILDING_SIZES.get(building_type, 400)
        size_in_grid = max(1, int(size / SCALE_X))

        center = GridPosition.from_world(world_x, world_y)
        half_size = size_in_grid // 2

        blocking_trees = []

        for tree_id, tree_pos in self.tree_positions.items():
            # Ist der Baum im Baubereich?
            if (center.x - half_size <= tree_pos.x <= center.x + half_size and
                center.y - half_size <= tree_pos.y <= center.y + half_size):
                blocking_trees.append(tree_id)

        return blocking_trees

    def find_valid_building_positions(self, building_type: str,
                                       near_x: float, near_y: float,
                                       search_radius: float = 5000,
                                       max_results: int = 10) -> List[Tuple[float, float, float]]:
        """
        Findet gültige Baupositionen in der Nähe.

        Returns:
            Liste von (x, y, distance) Tupeln, sortiert nach Distanz
        """
        size = BUILDING_SIZES.get(building_type, 400)
        size_in_grid = max(1, int(size / SCALE_X))
        half_size = size_in_grid // 2

        center = GridPosition.from_world(near_x, near_y)
        search_grid = int(search_radius / SCALE_X)

        valid_positions = []

        # Spiralsuche vom Zentrum aus
        for radius in range(0, search_grid, size_in_grid):
            for dy in range(-radius, radius + 1, size_in_grid):
                for dx in range(-radius, radius + 1, size_in_grid):
                    if abs(dx) != radius and abs(dy) != radius:
                        continue  # Nur Rand der Spirale

                    gx, gy = center.x + dx, center.y + dy
                    world_x, world_y = gx * SCALE_X, gy * SCALE_Y

                    if self.can_build_at(world_x, world_y, building_type):
                        dist = np.sqrt((world_x - near_x)**2 + (world_y - near_y)**2)
                        blocking = len(self.get_trees_blocking_building(world_x, world_y, building_type))
                        valid_positions.append((world_x, world_y, dist, blocking))

                        if len(valid_positions) >= max_results * 2:
                            break

        # Sortiere nach Distanz (und weniger Bäume zum Fällen)
        valid_positions.sort(key=lambda p: (p[3], p[2]))  # Erst Bäume, dann Distanz

        return [(p[0], p[1], p[2]) for p in valid_positions[:max_results]]


# =============================================================================
# A* PATHFINDING
# =============================================================================

class AStarPathfinder:
    """
    A* Pfadfindung auf dem WalkableGrid.

    Features:
    - 8-direktionale Bewegung
    - Diagonale Kosten korrekt berechnet
    - Optional: Pfad-Caching
    - Optional: Pfad-Glättung
    """

    def __init__(self, grid: WalkableGrid):
        self.grid = grid

    def _heuristic(self, a: GridPosition, b: GridPosition) -> int:
        """Diagonale Distanz Heuristik (Octile distance)."""
        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)
        return COST_STRAIGHT * (dx + dy) + (COST_DIAGONAL - 2 * COST_STRAIGHT) * min(dx, dy)

    def find_path(self, start_world: Tuple[float, float],
                  goal_world: Tuple[float, float]) -> PathResult:
        """
        Findet den kürzesten Pfad zwischen zwei Welt-Positionen.

        Args:
            start_world: (x, y) Startposition in Spieleinheiten
            goal_world: (x, y) Zielposition in Spieleinheiten

        Returns:
            PathResult mit Pfad und Distanz
        """
        start = GridPosition.from_world(start_world[0], start_world[1])
        goal = GridPosition.from_world(goal_world[0], goal_world[1])

        # Prüfe ob Start und Ziel gültig sind
        if not self.grid.is_walkable_pos(start):
            # Finde nächste begehbare Zelle
            start = self._find_nearest_walkable(start)
            if start is None:
                return PathResult(found=False)

        if not self.grid.is_walkable_pos(goal):
            goal = self._find_nearest_walkable(goal)
            if goal is None:
                return PathResult(found=False)

        # A* Algorithmus
        open_set = []
        heapq.heappush(open_set, (0, id(start), start))

        came_from: Dict[GridPosition, GridPosition] = {}
        g_score: Dict[GridPosition, int] = {start: 0}
        f_score: Dict[GridPosition, int] = {start: self._heuristic(start, goal)}

        open_set_hash: Set[GridPosition] = {start}

        while open_set:
            _, _, current = heapq.heappop(open_set)
            open_set_hash.discard(current)

            if current == goal:
                # Pfad rekonstruieren
                path = self._reconstruct_path(came_from, current)
                grid_dist = g_score[current]
                world_dist = grid_dist * ((SCALE_X + SCALE_Y) / 2) / COST_STRAIGHT

                return PathResult(
                    found=True,
                    path=path,
                    grid_distance=grid_dist,
                    world_distance=world_dist
                )

            for dx, dy in DIRECTIONS:
                neighbor = GridPosition(current.x + dx, current.y + dy)

                if not self.grid.is_walkable_pos(neighbor):
                    continue

                # Diagonale Bewegung: Prüfe ob Ecken frei sind
                if dx != 0 and dy != 0:
                    if not (self.grid.is_walkable(current.x + dx, current.y) and
                            self.grid.is_walkable(current.x, current.y + dy)):
                        continue

                # Bewegungskosten
                move_cost = COST_DIAGONAL if (dx != 0 and dy != 0) else COST_STRAIGHT
                tentative_g = g_score[current] + move_cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._heuristic(neighbor, goal)

                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], id(neighbor), neighbor))
                        open_set_hash.add(neighbor)

        # Kein Pfad gefunden
        return PathResult(found=False)

    def _reconstruct_path(self, came_from: Dict[GridPosition, GridPosition],
                          current: GridPosition) -> List[GridPosition]:
        """Rekonstruiert den Pfad vom Ziel zum Start."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def _find_nearest_walkable(self, pos: GridPosition, max_radius: int = 10) -> Optional[GridPosition]:
        """Findet die nächste begehbare Zelle."""
        for radius in range(1, max_radius + 1):
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if abs(dx) != radius and abs(dy) != radius:
                        continue

                    neighbor = GridPosition(pos.x + dx, pos.y + dy)
                    if self.grid.is_walkable_pos(neighbor):
                        return neighbor
        return None

    def get_path_distance(self, start_world: Tuple[float, float],
                          goal_world: Tuple[float, float]) -> float:
        """Gibt nur die Pfaddistanz zurück (schneller wenn Pfad nicht benötigt)."""
        result = self.find_path(start_world, goal_world)
        return result.world_distance if result.found else float('inf')


# =============================================================================
# MAP MANAGER (Kombiniert alles)
# =============================================================================

class MapManager:
    """
    Hauptklasse die Grid, Pfadfindung und Gebäude-Management kombiniert.

    WICHTIG: Alle externen Methoden arbeiten mit WELT-Koordinaten.
    Intern werden diese zu lokalen Grid-Koordinaten konvertiert.
    """

    def __init__(self, width: int = 754, height: int = 747):
        """
        Initialisiert den MapManager.

        Args:
            width: Grid-Breite (Standard: Spieler-1-Quadrant)
            height: Grid-Höhe
        """
        self.grid = WalkableGrid(width, height)
        self.pathfinder = AStarPathfinder(self.grid)

        # Quadrant-Offset (für Spieler 1)
        # Das sind die Welt-Koordinaten des Grid-Ursprungs (0,0)
        self.offset_x = 25240.0
        self.offset_y = 0.0

        # Baum-Tracking (Welt-Koordinaten -> Tree-ID)
        self.tree_world_positions: Dict[int, Tuple[float, float]] = {}

    def load_from_files(self,
                        walkable_file: str = None,
                        resources_file: str = None):
        """
        Lädt Kartendaten aus den exportierten Dateien.
        """
        base_dir = r"c:\Users\marku\OneDrive\Desktop\siedler_ai"

        # Walkable Grid laden
        if walkable_file is None:
            walkable_file = os.path.join(base_dir, "player1_walkable.npy")

        if os.path.exists(walkable_file):
            walkable = np.load(walkable_file)
            self.grid.load_terrain_from_array(walkable)
            print(f"Walkable Grid geladen: {walkable.shape}")

        # Ressourcen laden
        if resources_file is None:
            resources_file = os.path.join(base_dir, "player1_resources.json")

        if os.path.exists(resources_file):
            with open(resources_file, 'r') as f:
                resources = json.load(f)

            # Offset setzen
            self.offset_x = resources.get("quadrant_offset", {}).get("x", 25240.0)
            self.offset_y = resources.get("quadrant_offset", {}).get("y", 0.0)

            # Bäume laden - WICHTIG: Konvertiere Welt- zu lokalen Koordinaten
            # Versuche zuerst alle Bäume, dann Fallback auf nearest_50
            trees = resources.get("trees_all", resources.get("trees_nearest_50", []))
            tree_count = resources.get("trees_count", len(trees))

            for tree in trees:
                # Originale Welt-Koordinaten
                world_x, world_y = tree["x"], tree["y"]
                # Konvertiere zu lokalen Koordinaten für das Grid
                local_x, local_y = self.to_local_coords(world_x, world_y)
                # Füge zum Grid hinzu
                tree_id = self.grid.add_tree(local_x, local_y)
                # Speichere Welt-Position für späteres Lookup
                self.tree_world_positions[tree_id] = (world_x, world_y)

            print(f"Bäume geladen: {len(trees)} (von {tree_count} total)")

    def _load_trees_from_data(self, trees: list):
        """Lädt Bäume aus gecachten Daten (für schnelles Reset)."""
        for tree in trees:
            world_x, world_y = tree["x"], tree["y"]
            local_x, local_y = self.to_local_coords(world_x, world_y)
            tree_id = self.grid.add_tree(local_x, local_y)
            self.tree_world_positions[tree_id] = (world_x, world_y)

    def to_local_coords(self, world_x: float, world_y: float) -> Tuple[float, float]:
        """Konvertiert Welt-Koordinaten zu lokalen Quadrant-Koordinaten."""
        return (world_x - self.offset_x, world_y - self.offset_y)

    def to_world_coords(self, local_x: float, local_y: float) -> Tuple[float, float]:
        """Konvertiert lokale Quadrant-Koordinaten zu Welt-Koordinaten."""
        return (local_x + self.offset_x, local_y + self.offset_y)

    def find_path(self, start_world: Tuple[float, float],
                  goal_world: Tuple[float, float]) -> PathResult:
        """Findet Pfad zwischen zwei Welt-Positionen."""
        # Konvertiere zu lokalen Koordinaten
        start_local = self.to_local_coords(start_world[0], start_world[1])
        goal_local = self.to_local_coords(goal_world[0], goal_world[1])

        return self.pathfinder.find_path(start_local, goal_local)

    def get_path_distance(self, start_world: Tuple[float, float],
                          goal_world: Tuple[float, float]) -> float:
        """Gibt nur die Pfaddistanz zurück."""
        result = self.find_path(start_world, goal_world)
        return result.world_distance if result.found else float('inf')

    def add_building(self, world_x: float, world_y: float, building_type: str) -> int:
        """Fügt ein Gebäude hinzu."""
        local_x, local_y = self.to_local_coords(world_x, world_y)
        return self.grid.add_building(local_x, local_y, building_type)

    def can_build_at(self, world_x: float, world_y: float, building_type: str) -> bool:
        """Prüft ob ein Gebäude gebaut werden kann."""
        local_x, local_y = self.to_local_coords(world_x, world_y)
        return self.grid.can_build_at(local_x, local_y, building_type)

    def remove_tree(self, tree_id: int):
        """Entfernt einen Baum."""
        self.grid.remove_tree(tree_id)
        if tree_id in self.tree_world_positions:
            del self.tree_world_positions[tree_id]

    def get_nearest_tree(self, world_x: float, world_y: float) -> Optional[Tuple[int, float, Tuple[float, float]]]:
        """
        Findet den nächsten Baum zu einer Welt-Position.

        Returns:
            (tree_id, distance, (world_x, world_y)) oder None
        """
        if not self.tree_world_positions:
            return None

        min_dist = float('inf')
        nearest_id = None

        for tree_id, (tx, ty) in self.tree_world_positions.items():
            dist = np.sqrt((tx - world_x)**2 + (ty - world_y)**2)
            if dist < min_dist:
                min_dist = dist
                nearest_id = tree_id

        if nearest_id is not None:
            return (nearest_id, min_dist, self.tree_world_positions[nearest_id])
        return None

    def get_all_trees(self) -> List[Tuple[int, float, float]]:
        """Gibt alle Bäume zurück als Liste von (id, world_x, world_y)."""
        return [(tid, pos[0], pos[1]) for tid, pos in self.tree_world_positions.items()]


# =============================================================================
# TEST
# =============================================================================

def test_pathfinding():
    """Testet die Pfadfindung."""
    print("=" * 60)
    print("PATHFINDING TEST")
    print("=" * 60)

    # Manager erstellen und laden
    manager = MapManager()
    manager.load_from_files()

    # Test: Pfad vom HQ zum nächsten Baum
    hq_pos = (41100, 23100)

    print(f"\nHQ Position: {hq_pos}")
    print(f"Quadrant-Offset: ({manager.offset_x}, {manager.offset_y})")
    print(f"HQ lokal: {manager.to_local_coords(*hq_pos)}")

    # Nächster Baum
    nearest = manager.get_nearest_tree(hq_pos[0], hq_pos[1])
    if nearest:
        tree_id, distance, tree_world_pos = nearest

        print(f"\nNächster Baum:")
        print(f"  ID: {tree_id}")
        print(f"  Welt-Position: ({tree_world_pos[0]:.0f}, {tree_world_pos[1]:.0f})")
        print(f"  Luftlinie-Distanz: {distance:.0f} Einheiten")

        # Pfad finden
        result = manager.find_path(hq_pos, tree_world_pos)

        if result.found:
            print(f"\nPfad gefunden!")
            print(f"  Wegpunkte: {len(result.path)}")
            print(f"  Grid-Distanz: {result.grid_distance}")
            print(f"  Welt-Distanz: {result.world_distance:.0f} Einheiten")
            print(f"  Laufzeit (Speed 360): {result.world_distance / 360:.1f} Sekunden")

            # Zeige erste und letzte Wegpunkte
            if len(result.path) > 2:
                print(f"  Start-Grid: ({result.path[0].x}, {result.path[0].y})")
                print(f"  Ziel-Grid: ({result.path[-1].x}, {result.path[-1].y})")
        else:
            print(f"\nKein Pfad gefunden!")
            # Debug: Prüfe warum
            start_local = manager.to_local_coords(*hq_pos)
            goal_local = manager.to_local_coords(*tree_world_pos)
            start_grid = GridPosition.from_world(start_local[0], start_local[1])
            goal_grid = GridPosition.from_world(goal_local[0], goal_local[1])
            print(f"  Debug - Start-Grid: ({start_grid.x}, {start_grid.y})")
            print(f"  Debug - Ziel-Grid: ({goal_grid.x}, {goal_grid.y})")
            print(f"  Start walkable: {manager.grid.is_walkable_pos(start_grid)}")
            print(f"  Ziel walkable: {manager.grid.is_walkable_pos(goal_grid)}")

    # Test: Bauplatz-Validierung
    print(f"\n" + "-" * 60)
    print("BAUPLATZ-TEST")
    print("-" * 60)

    test_positions = [
        (41100, 23100, "Hauptquartier"),  # HQ Position
        (40900, 22900, "Wohnhaus"),       # Nahe am HQ
        (42000, 22000, "Sägewerk"),       # Etwas weiter weg
        (42330, 24030, "Sägewerk"),       # Bei einem Baum
    ]

    for x, y, building in test_positions:
        can_build = manager.can_build_at(x, y, building)
        blocking_trees = manager.grid.get_trees_blocking_building(
            *manager.to_local_coords(x, y), building
        )
        print(f"  {building} bei ({x}, {y}): {'JA' if can_build else 'NEIN'} "
              f"(Bäume im Weg: {len(blocking_trees)})")

    # Test: Zeige einige Bäume
    print(f"\n" + "-" * 60)
    print("BÄUME (erste 5)")
    print("-" * 60)
    trees = manager.get_all_trees()[:5]
    for tid, tx, ty in trees:
        dist = np.sqrt((tx - hq_pos[0])**2 + (ty - hq_pos[1])**2)
        print(f"  Baum {tid}: ({tx:.0f}, {ty:.0f}), Distanz: {dist:.0f}")


if __name__ == "__main__":
    test_pathfinding()
