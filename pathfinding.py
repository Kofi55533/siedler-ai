# -*- coding: utf-8 -*-
"""
Pfadfindung und Karten-Management fÃ¼r Siedler AI.

Dieses Modul enthÃ¤lt:
1. WalkableGrid - Verwaltet begehbare/blockierte FlÃ¤chen
2. A* Pathfinding - Findet optimale Wege
3. BuildingManager - Verwaltet GebÃ¤ude und deren Blockierungen
4. Bauplatz-Validierung - PrÃ¼ft ob GebÃ¤ude platziert werden kÃ¶nnen
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
# Default: alte 1508x1496 Grid-GrÃ¶ÃŸe. Kann zur Laufzeit Ã¼berschrieben werden.
SCALE_X = 33.5  # 1 Grid-Pixel = 33.5 Spieleinheiten
SCALE_Y = 33.8  # 1 Grid-Pixel = 33.8 Spieleinheiten


def set_grid_scale(scale_x: float, scale_y: float):
    """Setzt die globale Grid-Skalierung (Welt -> Grid)."""
    global SCALE_X, SCALE_Y
    SCALE_X = float(scale_x)
    SCALE_Y = float(scale_y)


def get_grid_scale() -> Tuple[float, float]:
    """Gibt die aktuelle Grid-Skalierung zurÃ¼ck."""
    return SCALE_X, SCALE_Y

# GebÃ¤ude-Footprints in Spieleinheiten (width, height)
# Werte aus Entity-XMLs (Blocked2 - Blocked1) Ã¼bernommen.
BUILDING_FOOTPRINTS = {
    # Kern-GebÃ¤ude
    "Hauptquartier": (1200, 1200),
    "Dorfzentrum": (1200, 1100),
    "Wohnhaus": (400, 500),
    "Bauernhof": (600, 1000),
    # Produktions-GebÃ¤ude
    "Hochschule": (1300, 1500),
    "SÃ¤gemÃ¼hle": (900, 1600),
    "SteinmetzhÃ¼tte": (800, 1000),
    "Schmiede": (900, 700),
    "LehmhÃ¼tte": (750, 1010),
    "AlchimistenhÃ¼tte": (800, 1400),
    "BÃ¼chsenmacherei": (1000, 1000),
    "KanongieÃŸerei": (1500, 1300),
    # Minen
    "Eisenmine": (920, 1070),
    "Steinmine": (1000, 1000),
    "Lehmmine": (1220, 970),
    "Schwefelmine": (920, 970),
    # MilitÃ¤r
    "Kaserne": (1400, 1400),
    "SchieÃŸplatz": (1300, 1500),
    "Stall": (1600, 1800),
    "Turm": (600, 600),
    # Spezial
    "Bank": (900, 900),
    "Kloster": (1200, 1400),
    "Markt": (1200, 1200),
    "Taverne": (800, 1000),
    "Architektenstube": (600, 600),
    "BrÃ¼cke": (400, 1200),
    # Schmuck (Beautification)
    "PB_Beautification01": (300, 300),
    "PB_Beautification02": (500, 500),
    "PB_Beautification03": (300, 300),
    "PB_Beautification04": (300, 300),
    "PB_Beautification05": (300, 300),
    "PB_Beautification06": (300, 300),
    "PB_Beautification07": (300, 300),
    "PB_Beautification08": (300, 300),
    "PB_Beautification09": (300, 300),
    "PB_Beautification10": (300, 300),
    "PB_Beautification11": (300, 300),
    "PB_Beautification12": (300, 300),
}


def get_building_footprint(building_type: str) -> Tuple[int, int]:
    """Gibt (width, height) des GebÃ¤udes zurÃ¼ck (Fallback: 400x400)."""
    return BUILDING_FOOTPRINTS.get(building_type, (400, 400))

# Bewegungsrichtungen fÃ¼r A* (8-direktional)
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
# Schutz gegen Worst-Case A* (Performance-Fallback)
MAX_ASTAR_EXPANSIONS = 200000

# =============================================================================
# HILFSKLASSEN
# =============================================================================

class CellType(IntEnum):
    """Zellentypen im Grid."""
    WALKABLE = 0
    BLOCKED_TERRAIN = 1  # Berg, Wasser (permanent)
    BLOCKED_BUILDING = 2  # GebÃ¤ude (dynamisch)
    BLOCKED_TREE = 3      # Baum (dynamisch, kann gefÃ¤llt werden)
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
        """Gibt den Pfad in Welt-Koordinaten zurÃ¼ck."""
        return [pos.to_world() for pos in self.path]


# =============================================================================
# WALKABLE GRID
# =============================================================================

class WalkableGrid:
    """
    Verwaltet die begehbaren und blockierten FlÃ¤chen der Karte.

    Das Grid hat mehrere Layer:
    - terrain_base: Statische Terrain-Blockierungen (Berge, Wasser)
    - buildings: Dynamische GebÃ¤ude-Blockierungen
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

        # GebÃ¤ude-Tracking
        self.building_positions: Dict[int, Tuple[GridPosition, str, int, int]] = {}
        self.next_building_id = 1

        # Baum-Tracking
        self.tree_positions: Dict[int, GridPosition] = {}
        self.next_tree_id = 1
        # KDTree fuer O(log n) nearest-tree Suche (lazy rebuild bei Aenderungen)
        self._tree_kd_tree = None  # scipy.spatial.KDTree oder None
        self._tree_kd_ids: List[int] = []  # Mapping KDTree-Index -> tree_id
        self._tree_kd_dirty = True

        # Cache fÃ¼r Pfade (optional)
        self.path_cache: Dict[Tuple[GridPosition, GridPosition], PathResult] = {}
        self.cache_valid = True
        self.revision = 0
        # FÃ¼r laufende Einheiten: nur erhÃ¶hen wenn bestehende Pfade potenziell ungÃ¼ltig werden.
        self.routing_revision = 0

    def copy_fresh(self) -> 'WalkableGrid':
        """Erstellt eine frische Kopie mit nur dem Basis-Terrain (fÃ¼r schnelles Reset)."""
        new_grid = WalkableGrid(self.width, self.height)
        new_grid.terrain_base = self.terrain_base.copy()  # Statisches Terrain kopieren
        # Dynamische Layer bleiben leer (buildings, trees, resources = 0)
        return new_grid

    def load_terrain_from_file(self, terrain_file: str, walkable_threshold: Tuple[int, int] = (100, 160)):
        """
        LÃ¤dt Terrain-Daten aus einer BinÃ¤rdatei.

        Args:
            terrain_file: Pfad zur Terrain-Datei (file_0.bin)
            walkable_threshold: (min, max) Werte fÃ¼r begehbares Terrain
        """
        with open(terrain_file, 'rb') as f:
            data = f.read()

        terrain = np.frombuffer(data, dtype=np.uint8)

        # Reshape auf Grid-GrÃ¶ÃŸe
        if len(terrain) == self.width * self.height:
            terrain = terrain.reshape((self.height, self.width))
        else:
            # Versuche passende Dimensionen zu finden
            total = len(terrain)
            # Bekannte GrÃ¶ÃŸe: 1508 x 1496 = 2,255,968
            if total == 2255968:
                terrain = terrain.reshape((1496, 1508))
                # Resize wenn nÃ¶tig
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
        """LÃ¤dt Terrain direkt aus einem NumPy Array."""
        if walkable_array.shape != (self.height, self.width):
            raise ValueError(f"Array-GrÃ¶ÃŸe {walkable_array.shape} passt nicht zu Grid {self.height}x{self.width}")
        self.terrain_base = walkable_array.astype(np.uint8)

    def is_walkable(self, x: int, y: int) -> bool:
        """PrÃ¼ft ob eine Zelle begehbar ist."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        return (self.terrain_base[y, x] == 1 and
                self.buildings[y, x] == 0 and
                self.trees[y, x] == 0)

    def is_walkable_pos(self, pos: GridPosition) -> bool:
        """PrÃ¼ft ob eine GridPosition begehbar ist."""
        return self.is_walkable(pos.x, pos.y)

    def get_walkable_grid(self) -> np.ndarray:
        """Gibt das kombinierte begehbare Grid zurÃ¼ck."""
        return (self.terrain_base &
                (1 - self.buildings) &
                (1 - self.trees)).astype(np.uint8)

    # -------------------------------------------------------------------------
    # GebÃ¤ude-Management
    # -------------------------------------------------------------------------

    def add_building(self, world_x: float, world_y: float, building_type: str) -> int:
        """
        FÃ¼gt ein GebÃ¤ude hinzu und blockiert die entsprechenden Zellen.

        Returns:
            Building ID fÃ¼r spÃ¤teres Entfernen
        """
        width, height = get_building_footprint(building_type)
        size_x = max(1, int(width / SCALE_X))
        size_y = max(1, int(height / SCALE_Y))

        # Grid-Position (Zentrum)
        center = GridPosition.from_world(world_x, world_y)

        # Blockiere alle Zellen im Bereich (Numpy-Slicing statt nested Python-Loops)
        half_x = size_x // 2
        half_y = size_y // 2
        y1 = max(0, center.y - half_y)
        y2 = min(self.height, center.y + half_y + 1)
        x1 = max(0, center.x - half_x)
        x2 = min(self.width, center.x + half_x + 1)
        if y1 < y2 and x1 < x2:
            self.buildings[y1:y2, x1:x2] = 1

        # Tracking
        building_id = self.next_building_id
        self.next_building_id += 1
        self.building_positions[building_id] = (center, building_type, size_x, size_y)

        # Cache invalidieren
        self.cache_valid = False
        self.revision += 1
        self.routing_revision += 1

        return building_id

    def remove_building(self, building_id: int):
        """Entfernt ein GebÃ¤ude und gibt die Zellen frei."""
        if building_id not in self.building_positions:
            return

        center, building_type, size_x, size_y = self.building_positions[building_id]

        half_x = size_x // 2
        half_y = size_y // 2
        y1 = max(0, center.y - half_y)
        y2 = min(self.height, center.y + half_y + 1)
        x1 = max(0, center.x - half_x)
        x2 = min(self.width, center.x + half_x + 1)
        if y1 < y2 and x1 < x2:
            self.buildings[y1:y2, x1:x2] = 0

        del self.building_positions[building_id]
        self.cache_valid = False
        self.revision += 1
        self.routing_revision += 1

    # -------------------------------------------------------------------------
    # Baum-Management
    # -------------------------------------------------------------------------

    def add_tree(self, world_x: float, world_y: float) -> int:
        """FÃ¼gt einen Baum hinzu."""
        pos = GridPosition.from_world(world_x, world_y)

        if 0 <= pos.x < self.width and 0 <= pos.y < self.height:
            self.trees[pos.y, pos.x] = 1

        tree_id = self.next_tree_id
        self.next_tree_id += 1
        self.tree_positions[tree_id] = pos
        self._tree_kd_dirty = True

        self.cache_valid = False
        self.revision += 1
        self.routing_revision += 1
        return tree_id

    def add_trees_batch(self, tree_list: List[Dict]) -> List[int]:
        """FÃ¼gt mehrere BÃ¤ume auf einmal hinzu (effizienter)."""
        tree_ids = []
        for tree in tree_list:
            tree_id = self.add_tree(tree["x"], tree["y"])
            tree_ids.append(tree_id)
        return tree_ids

    def remove_tree(self, tree_id: int):
        """Entfernt einen Baum (gefÃ¤llt)."""
        if tree_id not in self.tree_positions:
            return

        pos = self.tree_positions[tree_id]
        if 0 <= pos.x < self.width and 0 <= pos.y < self.height:
            self.trees[pos.y, pos.x] = 0

        del self.tree_positions[tree_id]
        self._tree_kd_dirty = True
        self.cache_valid = False
        self.revision += 1

    def _rebuild_tree_kd(self):
        """Baut KDTree aus aktuellen Baum-Positionen neu (lazy, nur bei Bedarf)."""
        if not self.tree_positions:
            self._tree_kd_tree = None
            self._tree_kd_ids = []
            self._tree_kd_dirty = False
            return
        try:
            from scipy.spatial import KDTree
            ids = list(self.tree_positions.keys())
            coords = np.array([(self.tree_positions[i].x, self.tree_positions[i].y) for i in ids], dtype=np.float32)
            self._tree_kd_tree = KDTree(coords)
            self._tree_kd_ids = ids
        except ImportError:
            self._tree_kd_tree = None
        self._tree_kd_dirty = False

    def get_nearest_tree(self, world_x: float, world_y: float) -> Optional[Tuple[int, float]]:
        """Findet den naechsten Baum zu einer Position (O(log n) via KDTree)."""
        if not self.tree_positions:
            return None

        start = GridPosition.from_world(world_x, world_y)

        # KDTree-Pfad: O(log n) statt O(n) lineare Suche
        if self._tree_kd_dirty:
            self._rebuild_tree_kd()

        if self._tree_kd_tree is not None:
            dist, idx = self._tree_kd_tree.query([start.x, start.y])
            nearest_id = self._tree_kd_ids[int(idx)]
            world_dist = float(dist) * ((SCALE_X + SCALE_Y) / 2)
            return (nearest_id, world_dist)

        # Fallback: lineare Suche (wenn scipy nicht verfuegbar)
        min_dist = float('inf')
        nearest_id = None
        for tree_id, pos in self.tree_positions.items():
            dist = abs(pos.x - start.x) + abs(pos.y - start.y)
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
        PrÃ¼ft ob ein GebÃ¤ude an einer Position gebaut werden kann.

        Bedingungen:
        1. Alle Zellen im Bereich mÃ¼ssen terrain-begehbar sein
        2. Keine anderen GebÃ¤ude im Weg
        3. Keine BÃ¤ume im Weg (mÃ¼ssen erst gefÃ¤llt werden)
        """
        width, height = get_building_footprint(building_type)
        size_x = max(1, int(width / SCALE_X))
        size_y = max(1, int(height / SCALE_Y))

        center = GridPosition.from_world(world_x, world_y)
        half_x = size_x // 2
        half_y = size_y // 2

        # Pruefe ob Bereich innerhalb der Karte liegt
        if (center.x - half_x < 0 or center.x + half_x >= self.width or
                center.y - half_y < 0 or center.y + half_y >= self.height):
            return False

        # Numpy-Slicing statt nested Python-Loops
        y1 = center.y - half_y
        y2 = center.y + half_y + 1
        x1 = center.x - half_x
        x2 = center.x + half_x + 1
        region_terrain = self.terrain_base[y1:y2, x1:x2]
        region_buildings = self.buildings[y1:y2, x1:x2]
        region_trees = self.trees[y1:y2, x1:x2]

        if not np.all(region_terrain == 1):
            return False
        if np.any(region_buildings == 1):
            return False
        if np.any(region_trees == 1):
            return False

        return True

    def get_trees_blocking_building(self, world_x: float, world_y: float,
                                     building_type: str) -> List[int]:
        """Gibt Liste der BÃ¤ume zurÃ¼ck, die fÃ¼r den Bau gefÃ¤llt werden mÃ¼ssen."""
        width, height = get_building_footprint(building_type)
        size_x = max(1, int(width / SCALE_X))
        size_y = max(1, int(height / SCALE_Y))

        center = GridPosition.from_world(world_x, world_y)
        half_x = size_x // 2
        half_y = size_y // 2

        blocking_trees = []

        for tree_id, tree_pos in self.tree_positions.items():
            # Ist der Baum im Baubereich?
            if (center.x - half_x <= tree_pos.x <= center.x + half_x and
                center.y - half_y <= tree_pos.y <= center.y + half_y):
                blocking_trees.append(tree_id)

        return blocking_trees

    def find_valid_building_positions(self, building_type: str,
                                       near_x: float, near_y: float,
                                       search_radius: float = 5000,
                                       max_results: int = 10) -> List[Tuple[float, float, float]]:
        """
        Findet gÃ¼ltige Baupositionen in der NÃ¤he.

        Returns:
            Liste von (x, y, distance) Tupeln, sortiert nach Distanz
        """
        width, height = get_building_footprint(building_type)
        size_x = max(1, int(width / SCALE_X))
        size_y = max(1, int(height / SCALE_Y))
        step = max(1, min(size_x, size_y))

        center = GridPosition.from_world(near_x, near_y)
        search_grid = int(search_radius / SCALE_X)

        valid_positions = []

        # Spiralsuche vom Zentrum aus
        for radius in range(0, search_grid, step):
            for dy in range(-radius, radius + 1, step):
                for dx in range(-radius, radius + 1, step):
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

        # Sortiere nach Distanz (und weniger BÃ¤ume zum FÃ¤llen)
        valid_positions.sort(key=lambda p: (p[3], p[2]))  # Erst BÃ¤ume, dann Distanz

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
    - Optional: Pfad-GlÃ¤ttung
    """

    def __init__(self, grid: WalkableGrid):
        self.grid = grid
        # Pre-allocate A* arrays einmalig (verhindert ~2.2MB Allokation pro find_path()-Aufruf)
        h, w = grid.height, grid.width
        self._astar_inf = np.iinfo(np.int32).max
        self._g_score = np.full((h, w), self._astar_inf, dtype=np.int32)
        self._came_x = np.full((h, w), -1, dtype=np.int16)
        self._came_y = np.full((h, w), -1, dtype=np.int16)

    def _heuristic(self, a: GridPosition, b: GridPosition) -> int:
        """Diagonale Distanz Heuristik (Octile distance)."""
        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)
        return COST_STRAIGHT * (dx + dy) + (COST_DIAGONAL - 2 * COST_STRAIGHT) * min(dx, dy)

    def find_path(self, start_world: Tuple[float, float],
                  goal_world: Tuple[float, float]) -> PathResult:
        """
        Findet den kuerzesten Pfad zwischen zwei Welt-Positionen.

        Args:
            start_world: (x, y) Startposition in Spieleinheiten
            goal_world: (x, y) Zielposition in Spieleinheiten

        Returns:
            PathResult mit Pfad und Distanz
        """
        start = GridPosition.from_world(start_world[0], start_world[1])
        goal = GridPosition.from_world(goal_world[0], goal_world[1])

        # Pruefe ob Start und Ziel gueltig sind
        if not self.grid.is_walkable_pos(start):
            start = self._find_nearest_walkable(start)
            if start is None:
                return PathResult(found=False)

        if not self.grid.is_walkable_pos(goal):
            goal = self._find_nearest_walkable(goal)
            if goal is None:
                return PathResult(found=False)

        width = self.grid.width
        height = self.grid.height
        terrain = self.grid.terrain_base
        buildings = self.grid.buildings
        trees = self.grid.trees

        def is_walkable_xy(x: int, y: int) -> bool:
            if x < 0 or y < 0 or x >= width or y >= height:
                return False
            return terrain[y, x] == 1 and buildings[y, x] == 0 and trees[y, x] == 0

        sx, sy = start.x, start.y
        gx, gy = goal.x, goal.y

        # A* Algorithmus (array-basiert, schneller)
        # Verwende pre-allozierte Arrays und reset per fill() statt np.full()
        inf = self._astar_inf
        g_score = self._g_score
        came_x = self._came_x
        came_y = self._came_y
        g_score.fill(inf)
        came_x.fill(-1)
        came_y.fill(-1)

        def heuristic_xy(x: int, y: int) -> int:
            dx = abs(x - gx)
            dy = abs(y - gy)
            return COST_STRAIGHT * (dx + dy) + (COST_DIAGONAL - 2 * COST_STRAIGHT) * min(dx, dy)

        g_score[sy, sx] = 0
        open_set = []
        heapq.heappush(open_set, (heuristic_xy(sx, sy), 0, sx, sy))
        expansions = 0

        while open_set:
            _, g_curr, x, y = heapq.heappop(open_set)
            if g_curr != g_score[y, x]:
                continue

            expansions += 1
            if MAX_ASTAR_EXPANSIONS and expansions > MAX_ASTAR_EXPANSIONS:
                return PathResult(found=False)

            if x == gx and y == gy:
                # Pfad rekonstruieren
                path: List[GridPosition] = [GridPosition(x, y)]
                while True:
                    px = int(came_x[y, x])
                    py = int(came_y[y, x])
                    if px < 0 or py < 0:
                        break
                    path.append(GridPosition(px, py))
                    x, y = px, py
                path.reverse()
                grid_dist = int(g_score[gy, gx])
                world_dist = grid_dist * ((SCALE_X + SCALE_Y) / 2) / COST_STRAIGHT
                return PathResult(
                    found=True,
                    path=path,
                    grid_distance=grid_dist,
                    world_distance=world_dist,
                )

            for dx, dy in DIRECTIONS:
                nx = x + dx
                ny = y + dy
                if not is_walkable_xy(nx, ny):
                    continue
                if dx != 0 and dy != 0:
                    if not (is_walkable_xy(x + dx, y) and is_walkable_xy(x, y + dy)):
                        continue
                move_cost = COST_DIAGONAL if (dx != 0 and dy != 0) else COST_STRAIGHT
                tentative_g = g_curr + move_cost
                if tentative_g < g_score[ny, nx]:
                    g_score[ny, nx] = tentative_g
                    came_x[ny, nx] = x
                    came_y[ny, nx] = y
                    f_score = tentative_g + heuristic_xy(nx, ny)
                    heapq.heappush(open_set, (f_score, tentative_g, nx, ny))

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

    def _find_nearest_walkable(self, pos: GridPosition, max_radius: int = 80) -> Optional[GridPosition]:
        """Findet die nÃ¤chste begehbare Zelle."""
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
        """Gibt nur die Pfaddistanz zurÃ¼ck (schneller wenn Pfad nicht benÃ¶tigt)."""
        result = self.find_path(start_world, goal_world)
        return result.world_distance if result.found else float('inf')


# =============================================================================
# MAP MANAGER (Kombiniert alles)
# =============================================================================

class MapManager:
    """
    Hauptklasse die Grid, Pfadfindung und GebÃ¤ude-Management kombiniert.

    WICHTIG: Alle externen Methoden arbeiten mit WELT-Koordinaten.
    Intern werden diese zu lokalen Grid-Koordinaten konvertiert.
    """

    def __init__(self, width: int = 754, height: int = 747):
        """
        Initialisiert den MapManager.

        Args:
            width: Grid-Breite (Standard: Spieler-1-Quadrant)
            height: Grid-HÃ¶he
        """
        self.grid = WalkableGrid(width, height)
        self.pathfinder = AStarPathfinder(self.grid)

        # Quadrant-Offset (fÃ¼r Spieler 1)
        # Das sind die Welt-Koordinaten des Grid-Ursprungs (0,0)
        self.offset_x = 25240.0
        self.offset_y = 0.0

        # Baum-Tracking (Welt-Koordinaten -> Tree-ID)
        self.tree_world_positions: Dict[int, Tuple[float, float]] = {}

    def load_from_files(self,
                        walkable_file: str = None,
                        resources_file: str = None):
        """
        LÃ¤dt Kartendaten aus den exportierten Dateien.
        """
        base_dir = os.environ.get(
            "SIEDLER_DATA_DIR",
            os.path.dirname(os.path.abspath(__file__)),
        )

        # Walkable Grid laden
        if walkable_file is None:
            walkable_file = os.path.join(base_dir, "player1_walkable.npy")

        if os.path.exists(walkable_file):
            walkable = np.load(walkable_file)
            # Falls Grid-GrÃ¶ÃŸe nicht passt, initialisiere neu
            if walkable.shape != (self.grid.height, self.grid.width):
                self.grid = WalkableGrid(walkable.shape[1], walkable.shape[0])
                self.pathfinder = AStarPathfinder(self.grid)
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

            # BÃ¤ume laden - WICHTIG: Konvertiere Welt- zu lokalen Koordinaten
            # Versuche zuerst alle BÃ¤ume, dann Fallback auf nearest_50
            trees = resources.get("trees_all", resources.get("trees_nearest_50", []))
            tree_count = resources.get("trees_count", len(trees))

            for tree in trees:
                # Originale Welt-Koordinaten
                world_x, world_y = tree["x"], tree["y"]
                # Konvertiere zu lokalen Koordinaten fÃ¼r das Grid
                local_x, local_y = self.to_local_coords(world_x, world_y)
                # FÃ¼ge zum Grid hinzu
                tree_id = self.grid.add_tree(local_x, local_y)
                # Speichere Welt-Position fÃ¼r spÃ¤teres Lookup
                self.tree_world_positions[tree_id] = (world_x, world_y)

            print(f"BÃ¤ume geladen: {len(trees)} (von {tree_count} total)")

    def _load_trees_from_data(self, trees: list):
        """LÃ¤dt BÃ¤ume aus gecachten Daten (fÃ¼r schnelles Reset)."""
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
        """Gibt nur die Pfaddistanz zurÃ¼ck."""
        result = self.find_path(start_world, goal_world)
        return result.world_distance if result.found else float('inf')

    def add_building(self, world_x: float, world_y: float, building_type: str) -> int:
        """FÃ¼gt ein GebÃ¤ude hinzu."""
        local_x, local_y = self.to_local_coords(world_x, world_y)
        return self.grid.add_building(local_x, local_y, building_type)

    def can_build_at(self, world_x: float, world_y: float, building_type: str) -> bool:
        """PrÃ¼ft ob ein GebÃ¤ude gebaut werden kann."""
        local_x, local_y = self.to_local_coords(world_x, world_y)
        return self.grid.can_build_at(local_x, local_y, building_type)

    def remove_tree(self, tree_id: int):
        """Entfernt einen Baum."""
        self.grid.remove_tree(tree_id)
        if tree_id in self.tree_world_positions:
            del self.tree_world_positions[tree_id]

    def get_nearest_tree(self, world_x: float, world_y: float) -> Optional[Tuple[int, float, Tuple[float, float]]]:
        """
        Findet den nÃ¤chsten Baum zu einer Welt-Position.

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
        """Gibt alle BÃ¤ume zurÃ¼ck als Liste von (id, world_x, world_y)."""
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

    # Test: Pfad vom HQ zum nÃ¤chsten Baum
    hq_pos = (41100, 23100)

    print(f"\nHQ Position: {hq_pos}")
    print(f"Quadrant-Offset: ({manager.offset_x}, {manager.offset_y})")
    print(f"HQ lokal: {manager.to_local_coords(*hq_pos)}")

    # NÃ¤chster Baum
    nearest = manager.get_nearest_tree(hq_pos[0], hq_pos[1])
    if nearest:
        tree_id, distance, tree_world_pos = nearest

        print(f"\nNÃ¤chster Baum:")
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
            # Debug: PrÃ¼fe warum
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
        (42000, 22000, "SÃ¤gewerk"),       # Etwas weiter weg
        (42330, 24030, "SÃ¤gewerk"),       # Bei einem Baum
    ]

    for x, y, building in test_positions:
        can_build = manager.can_build_at(x, y, building)
        blocking_trees = manager.grid.get_trees_blocking_building(
            *manager.to_local_coords(x, y), building
        )
        print(f"  {building} bei ({x}, {y}): {'JA' if can_build else 'NEIN'} "
              f"(BÃ¤ume im Weg: {len(blocking_trees)})")

    # Test: Zeige einige BÃ¤ume
    print(f"\n" + "-" * 60)
    print("BÃ„UME (erste 5)")
    print("-" * 60)
    trees = manager.get_all_trees()[:5]
    for tid, tx, ty in trees:
        dist = np.sqrt((tx - hq_pos[0])**2 + (ty - hq_pos[1])**2)
        print(f"  Baum {tid}: ({tx:.0f}, {ty:.0f}), Distanz: {dist:.0f}")


if __name__ == "__main__":
    test_pathfinding()

