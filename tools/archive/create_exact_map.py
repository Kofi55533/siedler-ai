# -*- coding: utf-8 -*-
"""
Erstellt eine exakte 1:1 Karte für die Siedler AI Simulation.
Extrahiert begehbare Flächen, Ressourcen, Bauplätze aus den echten Spieldaten.
"""

import numpy as np
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Tuple, Optional

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from map_extract_config import EXTRACTED_DIR

# =============================================================================
# KONFIGURATION
# =============================================================================

RAW_EXTRACT_FALLBACK_DIR = Path(
    os.environ.get("SIEDLER_RAW_MAP_EXTRACT_DIR", ROOT_DIR.parent / "wintersturm_extracted")
)


def _source_file(name: str) -> str:
    """Use the repository extraction first, then the local raw-map fallback."""
    primary = EXTRACTED_DIR / name
    if primary.exists():
        return str(primary)
    fallback = RAW_EXTRACT_FALLBACK_DIR / name
    return str(fallback if fallback.exists() else primary)


TERRAIN_FILE = _source_file("file_0.bin")
MAPDATA_FILE = _source_file("mapdata.xml")
OUTPUT_DIR = str(ROOT_DIR)

# Karten-Dimensionen (aus mapdata.xml)
MAP_WIDTH = 50480   # Spieleinheiten
MAP_HEIGHT = 50496  # Spieleinheiten

# Terrain-Grid Dimensionen (aus file_0.bin Analyse)
GRID_WIDTH = 1508
GRID_HEIGHT = 1496

# Skalierung: Spieleinheiten zu Grid-Pixel
SCALE_X = MAP_WIDTH / GRID_WIDTH    # ~33.5
SCALE_Y = MAP_HEIGHT / GRID_HEIGHT  # ~33.8

# Spieler 1 Quadrant (rechts unten auf der Karte)
# Y < MAP_HEIGHT/2 und X > MAP_WIDTH/2
PLAYER_1_QUADRANT = {
    "x_min": MAP_WIDTH / 2,   # 25240
    "x_max": MAP_WIDTH,       # 50480
    "y_min": 0,
    "y_max": MAP_HEIGHT / 2,  # 25248
}

SMALL_RESOURCE_NODE_AMOUNT = 400
MINE_PIT_DEFAULT_AMOUNTS = {
    "Eisen": 12000,
    "Stein": 14000,
    "Lehm": 12000,
    "Schwefel": 8000,
}


def _resource_amount(script_command: str, default: int) -> int:
    match = re.search(r"SetResourceDoodadGoodAmount\\([^,]+,(\\d+)\\)", script_command or "")
    return int(match.group(1)) if match else int(default)

# =============================================================================
# DATENKLASSEN
# =============================================================================

@dataclass
class Position:
    x: float
    y: float

    def to_grid(self) -> Tuple[int, int]:
        """Konvertiert Spielposition zu Grid-Koordinaten."""
        grid_x = int(self.x / SCALE_X)
        grid_y = int(self.y / SCALE_Y)
        return (grid_x, grid_y)

    def distance_to(self, other: 'Position') -> float:
        """Berechnet Distanz zu einer anderen Position."""
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

@dataclass
class Entity:
    entity_type: str
    position: Position
    player_id: int
    name: str = ""
    script_command: str = ""

    def is_tree(self) -> bool:
        return any(t in self.entity_type for t in ['Fir', 'Pine', 'DarkTree', 'Tree'])

    def is_small_resource_node(self) -> bool:
        return any(t in self.entity_type for t in ['XD_Iron', 'XD_Stone', 'XD_Clay', 'XD_Sulfur']) and 'Pit' not in self.entity_type

    def is_mine_pit(self) -> bool:
        return 'Pit' in self.entity_type

    # Historical names retained for existing consumers of this archive tool.
    def is_mine_shaft(self) -> bool:
        return self.is_small_resource_node()

    def is_small_deposit(self) -> bool:
        return self.is_mine_pit()

    def is_building_slot(self) -> bool:
        return 'VillageCenter' in self.entity_type or 'HQ' in self.entity_type

    def get_resource_type(self) -> Optional[str]:
        if 'Iron' in self.entity_type:
            return 'Eisen'
        elif 'Stone' in self.entity_type:
            return 'Stein'
        elif 'Clay' in self.entity_type:
            return 'Lehm'
        elif 'Sulfur' in self.entity_type:
            return 'Schwefel'
        elif self.is_tree():
            return 'Holz'
        return None

# =============================================================================
# TERRAIN LADEN
# =============================================================================

def load_terrain() -> np.ndarray:
    """Lädt die Terrain-/Höhenkarte."""
    with open(TERRAIN_FILE, 'rb') as f:
        data = f.read()

    arr = np.frombuffer(data, dtype=np.uint8)
    arr = arr.reshape((GRID_HEIGHT, GRID_WIDTH))
    return arr

def create_walkable_map(terrain: np.ndarray) -> np.ndarray:
    """
    Erstellt eine Begehbarkeits-Map aus der Höhenkarte.

    Die Terrain-Daten zeigen:
    - Wert ~128 = flaches, begehbares Terrain (gelb in Visualisierung)
    - Niedrige Werte (0-80) = Wasser/tiefe Bereiche (grün)
    - Hohe Werte (180-255) = Berge (braun/weiß)

    Für Siedler 5 ist das begehbare Terrain relativ flach.
    """
    # Begehbar = Werte zwischen 100 und 160 (das flache Plateau)
    walkable = np.zeros_like(terrain, dtype=np.uint8)

    # Hauptspielfeld (gelbes Plateau) hat Werte um 128
    walkable[(terrain >= 100) & (terrain <= 160)] = 1

    # Randkorrektur: Entferne isolierte Pixel
    from scipy import ndimage
    walkable = ndimage.binary_opening(walkable, iterations=1).astype(np.uint8)
    walkable = ndimage.binary_closing(walkable, iterations=1).astype(np.uint8)

    return walkable

# =============================================================================
# ENTITÄTEN AUS MAPDATA LADEN
# =============================================================================

def parse_mapdata() -> List[Entity]:
    """Parst alle Entitäten aus mapdata.xml."""
    entities = []

    with open(MAPDATA_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex für Entity-Blöcke
    entity_pattern = re.compile(
        r'<Entity[^>]*>.*?'
        r'<Type>([^<]+)</Type>.*?'
        r'<X>([^<]+)</X>.*?'
        r'<Y>([^<]+)</Y>.*?'
        r'<PlayerID>(\d+)</PlayerID>.*?'
        r'(?:<Name>([^<]*)</Name>)?.*?'
        r'(?:<ScriptCommandLine>([^<]*)</ScriptCommandLine>)?.*?'
        r'</Entity>',
        re.DOTALL
    )

    for match in entity_pattern.finditer(content):
        entity_type = match.group(1)
        x = float(match.group(2))
        y = float(match.group(3))
        player_id = int(match.group(4))
        name = match.group(5) or ""
        script = match.group(6) or ""

        entities.append(Entity(
            entity_type=entity_type,
            position=Position(x, y),
            player_id=player_id,
            name=name,
            script_command=script
        ))

    print(f"Gesamt: {len(entities)} Entitäten geladen")
    return entities

def filter_player1_quadrant(entities: List[Entity]) -> List[Entity]:
    """Filtert Entitäten im Spieler-1-Quadrant."""
    q = PLAYER_1_QUADRANT
    filtered = []

    for e in entities:
        if (q["x_min"] <= e.position.x <= q["x_max"] and
            q["y_min"] <= e.position.y <= q["y_max"]):
            filtered.append(e)

    return filtered

# =============================================================================
# RESSOURCEN EXTRAHIEREN
# =============================================================================

def extract_resources(entities: List[Entity], hq_pos: Position) -> Dict:
    """Extrahiert alle Ressourcen für Spieler 1."""

    trees = []
    small_resource_nodes = {"Eisen": [], "Stein": [], "Lehm": [], "Schwefel": []}
    mine_pits = {"Eisen": [], "Stein": [], "Lehm": [], "Schwefel": []}

    for e in entities:
        dist = e.position.distance_to(hq_pos)

        if e.is_tree():
            trees.append({
                "x": e.position.x,
                "y": e.position.y,
                "type": e.entity_type,
                "distance_to_hq": round(dist, 0)
            })

        elif e.is_small_resource_node():
            res_type = e.get_resource_type()
            if res_type and res_type in small_resource_nodes:
                small_resource_nodes[res_type].append({
                    "x": e.position.x,
                    "y": e.position.y,
                    "amount": _resource_amount(e.script_command, SMALL_RESOURCE_NODE_AMOUNT),
                    "original_type": e.entity_type,
                    "entity_kind": "small_resource_node",
                    "distance_to_hq": round(dist, 0)
                })

        elif e.is_mine_pit():
            res_type = e.get_resource_type()
            if res_type and res_type in mine_pits:
                mine_pits[res_type].append({
                    "x": e.position.x,
                    "y": e.position.y,
                    "amount": _resource_amount(e.script_command, MINE_PIT_DEFAULT_AMOUNTS[res_type]),
                    "original_type": e.entity_type,
                    "entity_kind": "mine_pit",
                    "distance_to_hq": round(dist, 0)
                })

    # Sortiere nach Distanz
    trees.sort(key=lambda t: t["distance_to_hq"])
    for res_type in small_resource_nodes:
        small_resource_nodes[res_type].sort(key=lambda node: node["distance_to_hq"])
    for res_type in mine_pits:
        mine_pits[res_type].sort(key=lambda pit: pit["distance_to_hq"])

    return {
        "trees": trees,
        "small_resource_nodes": small_resource_nodes,
        "mine_pits": mine_pits,
        # Legacy aliases preserve the current environment input contract.
        "mine_shafts": small_resource_nodes,
        "deposits": mine_pits,
    }

# =============================================================================
# VISUALISIERUNG
# =============================================================================

def visualize_map(terrain: np.ndarray, walkable: np.ndarray,
                  resources: Dict, hq_pos: Position, output_name: str):
    """Erstellt eine detaillierte Kartenvisualisierung."""

    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Circle, Rectangle
        from matplotlib.colors import LinearSegmentedColormap
    except ImportError:
        print("Matplotlib nicht verfügbar!")
        return

    fig, axes = plt.subplots(1, 2, figsize=(20, 10))

    # === Linkes Bild: Terrain + Begehbarkeit ===
    ax1 = axes[0]

    # Terrain als Hintergrund
    terrain_cmap = LinearSegmentedColormap.from_list('terrain',
        ['darkblue', 'blue', 'green', 'yellow', 'orange', 'brown', 'white'])
    ax1.imshow(terrain, cmap=terrain_cmap, alpha=0.7)

    # Begehbare Fläche als Overlay
    walkable_overlay = np.ma.masked_where(walkable == 0, walkable)
    ax1.imshow(walkable_overlay, cmap='Greens', alpha=0.3)

    ax1.set_title('Terrain + Begehbare Flächen')
    ax1.set_xlabel(f'X (1 Pixel = {SCALE_X:.1f} Einheiten)')
    ax1.set_ylabel(f'Y (1 Pixel = {SCALE_Y:.1f} Einheiten)')

    # === Rechtes Bild: Spieler 1 Quadrant mit Ressourcen ===
    ax2 = axes[1]

    # Nur Spieler 1 Quadrant (rechte untere Ecke)
    q = PLAYER_1_QUADRANT
    x_start = int(q["x_min"] / SCALE_X)
    x_end = int(q["x_max"] / SCALE_X)
    y_start = int(q["y_min"] / SCALE_Y)
    y_end = int(q["y_max"] / SCALE_Y)

    quadrant_terrain = terrain[y_start:y_end, x_start:x_end]
    quadrant_walkable = walkable[y_start:y_end, x_start:x_end]

    ax2.imshow(quadrant_terrain, cmap=terrain_cmap, alpha=0.5)

    # Markiere Ressourcen
    # HQ
    hq_grid = hq_pos.to_grid()
    hq_local = (hq_grid[0] - x_start, hq_grid[1] - y_start)
    ax2.plot(hq_local[0], hq_local[1], 'r*', markersize=20, label='HQ')

    # Bäume (nur erste 100)
    tree_xs = [(t["x"] / SCALE_X) - x_start for t in resources["trees"][:100]]
    tree_ys = [(t["y"] / SCALE_Y) - y_start for t in resources["trees"][:100]]
    ax2.scatter(tree_xs, tree_ys, c='darkgreen', s=10, alpha=0.7, label=f'Bäume ({len(resources["trees"])})')

    # Kleine Ressourcenklumpen (XD_*1/2/3, nicht bebaubar)
    colors = {"Eisen": "gray", "Stein": "brown", "Lehm": "orange", "Schwefel": "yellow"}
    for res_type, nodes in resources["small_resource_nodes"].items():
        if nodes:
            xs = [(node["x"] / SCALE_X) - x_start for node in nodes]
            ys = [(node["y"] / SCALE_Y) - y_start for node in nodes]
            ax2.scatter(xs, ys, c=colors.get(res_type, 'black'), s=100,
                       marker='s', edgecolors='black', label=f'{res_type}klumpen ({len(nodes)})')

    # Minengruben (XD_*Pit1, bebaubare Mineplaetze)
    for res_type, pits in resources["mine_pits"].items():
        if pits:
            xs = [(pit["x"] / SCALE_X) - x_start for pit in pits]
            ys = [(pit["y"] / SCALE_Y) - y_start for pit in pits]
            ax2.scatter(xs, ys, c=colors.get(res_type, 'black'), s=60,
                       marker='o', edgecolors='black', alpha=0.7,
                       label=f'{res_type}gruben ({len(pits)})')

    ax2.set_title('Spieler 1 Quadrant - Ressourcen')
    ax2.legend(loc='upper left', fontsize=8)
    ax2.set_xlabel('X (lokal)')
    ax2.set_ylabel('Y (lokal)')

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, output_name)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Visualisierung gespeichert: {output_path}")

# =============================================================================
# EXAKTE DATEN EXPORTIEREN
# =============================================================================

def export_exact_map_data(terrain: np.ndarray, walkable: np.ndarray,
                          resources: Dict, hq_pos: Position):
    """Exportiert die exakten Kartendaten als NumPy-Dateien."""

    # Spieler 1 Quadrant extrahieren
    q = PLAYER_1_QUADRANT
    x_start = int(q["x_min"] / SCALE_X)
    x_end = int(q["x_max"] / SCALE_X)
    y_start = int(q["y_min"] / SCALE_Y)
    y_end = int(q["y_max"] / SCALE_Y)

    quadrant_walkable = walkable[y_start:y_end, x_start:x_end]
    quadrant_terrain = terrain[y_start:y_end, x_start:x_end]

    # Speichern
    np.save(os.path.join(OUTPUT_DIR, "player1_walkable.npy"), quadrant_walkable)
    np.save(os.path.join(OUTPUT_DIR, "player1_terrain.npy"), quadrant_terrain)

    print(f"Walkable Map: {quadrant_walkable.shape}")
    print(f"  Begehbar: {np.sum(quadrant_walkable)} Pixel ({100*np.mean(quadrant_walkable):.1f}%)")

    # Ressourcen als kompaktes Dict speichern
    import json

    resources_export = {
        "hq_position": {"x": hq_pos.x, "y": hq_pos.y},
        "grid_scale": {"x": SCALE_X, "y": SCALE_Y},
        "quadrant_offset": {"x": q["x_min"], "y": q["y_min"]},
        "trees_count": len(resources["trees"]),
        "trees_all": resources["trees"],  # ALLE Bäume exportieren
        "small_resource_nodes": resources["small_resource_nodes"],
        "mine_pits": resources["mine_pits"],
        "resource_semantics": {
            "small_resource_nodes": "XD_*1/2/3, direct collection, not a mine build slot",
            "mine_pits": "XD_*Pit1, mine build slot and pre-mine resource source",
            "legacy_aliases": {
                "mine_shafts": "small_resource_nodes",
                "deposits": "mine_pits",
            },
        },
        # Legacy aliases retained for environment.py and earlier reports.
        "mine_shafts": resources["mine_shafts"],
        "deposits": resources["deposits"],
    }

    with open(os.path.join(OUTPUT_DIR, "player1_resources.json"), 'w') as f:
        json.dump(resources_export, f, indent=2)

    print(f"Ressourcen exportiert: player1_resources.json")
    print(f"  - {len(resources['trees'])} Bäume")
    for res_type in resources["small_resource_nodes"]:
        print(f"  - {len(resources['small_resource_nodes'][res_type])} {res_type}klumpen")
        print(f"  - {len(resources['mine_pits'][res_type])} {res_type}gruben")

    return quadrant_walkable, quadrant_terrain

# =============================================================================
# HAUPTPROGRAMM
# =============================================================================

def main():
    print("=" * 70)
    print("EXAKTE KARTENEXTRAKTION FÜR SIEDLER AI")
    print("=" * 70)

    # 1. Terrain laden
    print("\n[1] Lade Terrain-Daten...")
    terrain = load_terrain()
    print(f"    Terrain: {terrain.shape}")

    # 2. Begehbare Map erstellen
    print("\n[2] Erstelle Begehbarkeits-Map...")
    try:
        walkable = create_walkable_map(terrain)
    except ImportError:
        print("    scipy nicht installiert - verwende einfache Methode")
        walkable = ((terrain >= 100) & (terrain <= 160)).astype(np.uint8)
    print(f"    Begehbar: {np.sum(walkable)} von {walkable.size} Pixeln ({100*np.mean(walkable):.1f}%)")

    # 3. Entitäten laden
    print("\n[3] Lade Entitäten aus mapdata.xml...")
    all_entities = parse_mapdata()

    # 4. Spieler 1 Quadrant filtern
    print("\n[4] Filtere Spieler 1 Quadrant...")
    p1_entities = filter_player1_quadrant(all_entities)
    print(f"    Entitäten im P1-Quadrant: {len(p1_entities)}")

    # HQ Position
    hq_pos = Position(41100, 23100)

    # 5. Ressourcen extrahieren
    print("\n[5] Extrahiere Ressourcen...")
    resources = extract_resources(p1_entities, hq_pos)

    print(f"    Bäume: {len(resources['trees'])}")
    for res_type in resources["small_resource_nodes"]:
        nodes = resources["small_resource_nodes"][res_type]
        pits = resources["mine_pits"][res_type]
        print(f"    {res_type}: {len(nodes)} Klumpen, {len(pits)} Gruben")

    # 6. Visualisierung
    print("\n[6] Erstelle Visualisierung...")
    visualize_map(terrain, walkable, resources, hq_pos, "exact_map_player1.png")

    # 7. Daten exportieren
    print("\n[7] Exportiere exakte Kartendaten...")
    export_exact_map_data(terrain, walkable, resources, hq_pos)

    print("\n" + "=" * 70)
    print("FERTIG!")
    print("=" * 70)

if __name__ == "__main__":
    main()
