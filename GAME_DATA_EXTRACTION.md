# Siedler 5 - Game Data Extraction für RL Environment

## Übersicht

Dieses Dokument beschreibt welche Daten aus dem echten Spiel extrahiert werden können und wie sie im RL Environment verwendet werden.

## Extrahierbare Daten via S5Hook

### 1. Terrain-Daten (`S5Hook.GetTerrainInfo`)

| Wert | Beschreibung | Verwendung im RL |
|------|--------------|------------------|
| **Height** | Terrain-Höhe (Z-Koordinate) | Pathfinding-Kosten (Steigungen) |
| **Blocking** | Blockierungs-Wert (Bitfield) | Walkable-Grid (0=begehbar, >0=blockiert) |
| **Sector** | Sektor-Nummer | Erreichbarkeits-Check (gleicher Sektor = erreichbar) |
| **TerrainType** | Terrain-Typ (Gras, Wasser, etc.) | Bau-Einschränkungen, Bewegungskosten |

**Blocking-Werte:**
- `0` = Frei begehbar
- `1` = Blockiert (Gebäude, Felsen)
- `9` = Wasser/Unpassierbar

**Sektor-System:**
- Zusammenhängende begehbare Bereiche haben gleiche Sektor-Nr
- Wenn Start und Ziel verschiedene Sektoren → KEIN Pfad möglich
- Wichtig für schnelle Erreichbarkeits-Checks

### 2. Entity-Positionen (`S5Hook.EntityIterator`)

| Entity-Typ | Lua-Typ | Daten |
|------------|---------|-------|
| Bäume | `XD_Fir1..3, XD_Pine1..3, XD_Tree1..3` | Position, Holz-Menge, Typ |
| Stollen | `XD_Iron1, XD_Stone1, XD_Clay1, XD_Sulfur1` | Position, Ressourcen-Menge |
| Vorkommen | `XD_IronPit1, XD_StonePit1, etc.` | Position, Ressourcen-Menge |
| Gebäude | `Predicate.IsBuilding()` | Position, Spieler, Typ, HP |
| Siedler | `Predicate.IsSettler()` | Position, Spieler, Typ |

### 3. Spieler-Daten

| Wert | API | Verwendung |
|------|-----|------------|
| Ressourcen | `Logic.GetPlayersGlobalResource(player, type)` | Start-Ressourcen validieren |
| HQ-Position | `Logic.GetHeadquarters(player)` | Spawn-Positionen |
| Gebäude-Liste | `EntityIterator + OfPlayer` | Initialer Zustand |

## Export-Ablauf

### 1. EMS Config aktivieren
Die Datei `(4) ems wintersturm.lua` in `EMSconfigs/` enthält den Export-Code.

### 2. Map starten
```
1. Siedler 5 starten
2. Map "(4) EMS Wintersturm" laden
3. Warten auf "GAME DATA EXPORT FERTIG!"
4. Spiel beenden
```

### 3. Log parsen
```bash
cd C:\Users\marku\OneDrive\Desktop\siedler_ai
python parse_game_export.py
```

### 4. Mit Environment vergleichen
```bash
python compare_game_vs_env.py
```

## Ausgabe-Dateien

Nach dem Parsen werden folgende Dateien erstellt:

| Datei | Inhalt |
|-------|--------|
| `game_export_height.npy` | Höhen-Grid (numpy array) |
| `game_export_blocking.npy` | Blocking-Grid (numpy array) |
| `game_export_sector.npy` | Sektor-Grid (numpy array) |
| `game_export_terrain_type.npy` | Terrain-Typ-Grid (numpy array) |
| `game_export_entities.json` | Alle Entities (Bäume, Minen, Gebäude, etc.) |
| `game_export_report.json` | Zusammenfassung |

## Integration ins RL Environment

### Walkable-Grid aktualisieren
```python
# In pathfinding.py
blocking = np.load("map_extract/game_export_blocking.npy")
walkable = (blocking == 0).astype(np.uint8)
np.save("player1_walkable.npy", walkable)
```

### Sektor-basierte Erreichbarkeit
```python
# Schneller Check ob Pfad existiert
sector_grid = np.load("map_extract/game_export_sector.npy")

def can_reach(start, goal):
    sx, sy = world_to_grid(start)
    gx, gy = world_to_grid(goal)
    return sector_grid[sy, sx] == sector_grid[gy, gx]
```

### Ressourcen-Positionen aktualisieren
```python
import json

with open("map_extract/game_export_entities.json") as f:
    data = json.load(f)

# Bäume für Player 1 Quadrant
trees = [t for t in data["trees"] if 25000 < t["x"] < 51000]

# In map_config_wintersturm.py aktualisieren
PLAYER_1_TREES = [(t["x"], t["y"], t["amount"]) for t in trees]
```

## Was NICHT via S5Hook extrahiert werden kann

Diese Werte müssen aus den XML-Dateien kommen:

| Wert | Quelle |
|------|--------|
| Gebäude-Kosten | `Entities/PB_*.xml` |
| Technologie-Kosten | `Technologies.xml` |
| Soldaten-Stats | `Entities/PU_*.xml` |
| WorkTime-Parameter | `Entities/PU_*.xml` |
| Produktions-Zeiten | `Entities/PB_*.xml` |

Diese sind bereits in `config/game_data.json` extrahiert.

## Automatisierung

### Export bei jedem Map-Start
Der Export läuft automatisch wenn die EMS Config aktiv ist.

### Export deaktivieren
In `(4) ems wintersturm.lua` den Export-Block auskommentieren:
```lua
--[[ EXPORT DEAKTIVIERT
if InstallS5Hook and InstallS5Hook() then
    ...
end
--]]
```

## Bekannte Limitierungen

1. **Nur bei Map-Start**: Export läuft nur einmal beim Laden
2. **Keine Echtzeit-Sync**: Änderungen während des Spiels werden nicht erfasst
3. **History Edition**: S5Hook funktioniert NICHT mit der History Edition
4. **Version 1.06**: Nur Patch 1.06.0217 wird unterstützt

## Engine XML decoder (base + extra1 + extra2)

Use this to decode original worker/building/tasklist values directly from the Ubisoft install:

```bash
cd C:\Users\marku\OneDrive\Desktop\siedler_ai
python engine_decoder.py --game-root "C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games\theSettlers5"
```

Output:
- `config/engine_decoded.json`

New sections include:
- `serf_tasklists`: exact `TL_SERF_*` task flows (`GO_TO_RESOURCE`, `EXTRACT_RESOURCE`, `BUILD`, etc.)
- `worker_path_tasklists`: worker flee/leave/defend movement tasklists
- `pathfinding_snapshot`: movement speeds, path-related logic params, terrain blocking summary
- `camp_mechanics`: camp slots/removal delay and camp building footprints

### Important limit

The low-level pathfinding algorithm itself (internal route search implementation) is in engine binaries, not in XML.
So XML + S5Hook can reproduce parameters, task flows, sectors, and blocking logic very accurately,
but exact binary-internal routing heuristics require runtime/binary reverse engineering.

## Worker truth model (1:1 worker behavior reference)

Build a consolidated worker model for the RL environment from the decoded engine data:

```bash
cd C:\Users\marku\OneDrive\Desktop\siedler_ai
python build_worker_truth_model.py
```

Output:
- `config/worker_truth_model.json`

Contains:
- per-worker movement truth (`speed`, `rotation_speed`, `move_task_list`, camp/resource ranges)
- per-worker worktime truth (`work_wait_until`, worktime deltas, eat/rest/camp behavior)
- tasklist multipliers per cycle (`resource_ops_per_cycle`, `task_change_work_time_work_count`, animation waits)
- miner mine-specific tasklists (`iron/stone/clay/sulfur`, inside/outside)
- serf extraction truth including delay + animation timing based cycle estimates
- resolved mapping from engine names to env names (`sawmillworker -> sawmill_worker`, etc.)

## Camp/Worker condition analyzer

Use this to extract camp trigger evidence and map/static-camp presence:

```bash
cd C:\Users\marku\OneDrive\Desktop\siedler_ai
python extract_camp_worker_conditions.py
```

Outputs:
- `config/camp_worker_conditions.json`
- `config/camp_worker_conditions.md`

What it reports:
- worker-specific `CamperRange` + `WorkTimeChangeCamp`
- evidence that idle chains contain `TASK_GO_TO_CAMP` and `TASK_CHANGE_WORK_TIME_CAMP`
- eat/rest path checks (`TASK_CHECK_GO_TO_*_BUILDING_SUCCESS`) where present
- map entity check for static camp objects (`CB_Camp*`, `CB_MinerCamp*`, `XD_LargeCampFire`)

## Complete worker behavior logic export

Build a full task-graph based logic report for all workers:

```bash
cd C:\Users\marku\OneDrive\Desktop\siedler_ai
python build_worker_behavior_logic.py
```

Outputs:
- `config/worker_behavior_logic.json`
- `config/worker_behavior_logic.md`

Contains:
- full declared tasklist set per worker
- recursively resolved tasklist graph (`TASK_SET_TASK_LIST` transitions)
- per-tasklist checks, movement/worktime/resource task categories
- derived behavior flags (camp idle/go-to, worktime-camp change, eat/rest success checks)
- unresolved tasklist diagnostics (should be `0` when config data is complete)
