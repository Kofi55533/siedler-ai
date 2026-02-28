# Lua Export Skripte

## Verwendung

### 1. Skript in EMS Config einfügen

Öffne `(4) ems wintersturm.lua` und füge am Ende von `Callback_OnGameStart` ein:

```lua
Callback_OnGameStart = function()
    OnGameStart()

    -- Export starten (wähle eines oder beide)
    Script.Load("maps/externalmap/export_pathfinding.lua")
    -- Script.Load("maps/externalmap/export_building_blocking.lua")
end,
```

### 2. Lua-Dateien kopieren

Kopiere die gewünschten `.lua` Dateien nach:
```
C:\Users\marku\OneDrive\Desktop\Gold edition\extra1\maps\externalmap\
```

### 3. Karte starten

1. Starte Siedler 5
2. Lade "(4) EMS Wintersturm"
3. Drücke Start
4. Warte 2-3 Sekunden
5. Spiel kann abstürzen (normal) oder du beendest es

### 4. Log parsen

```bash
python lua_exports/parse_lua_exports.py \
    --log "C:/Users/marku/Documents/Siedler5/Logs/Game.log" \
    --output lua_export_data.json
```

## Export-Skripte

### export_pathfinding.lua

Testet Erreichbarkeit (Sektoren) zwischen:
- HQ und allen Bäumen (nächste 3)
- HQ und allen Minen-Schächten (12 total)
- HQ und allen kleinen Vorkommen (6 total)
- HQ und allen Dorfzentrum-Slots (3 total)

**Output:**
```
PATH|Tree1|42330|24030|5|5|1542|1|1
      ^name ^x    ^y   ^hq ^target ^dist ^same ^walkable
```

### export_building_blocking.lua

Exportiert:
- Alle Gebäude auf der Karte
- Welche Terrain-Punkte sie blockieren
- Optional: Wo Gebäude gebaut werden können

**Output:**
```
BUILDING|67739|PB_Headquarters1|1|41100|23100|15
         ^id   ^type            ^player ^x ^y  ^blocked_points
```

### export_runtime_pathing.lua

Schickt einen echten `PU_Serf` (Spieler 1) nacheinander zu Zielpunkten und loggt:
- Start-/Zielposition
- Positions-Samples entlang des echten Laufwegs
- Ergebnis pro Ziel (`DONE` oder `FAIL` inkl. Zeit)

Das ist ein echter Runtime-Test der Engine-Entscheidung (Blackbox), nicht nur Sektor-Check.

**Output-Beispiele:**
```
RPATH|CMD|1|Tree1|41100|23100|42330|24030|true
RPATH|POS|1|Tree1|2.50|41700|23580|820.3
RPATH|DONE|1|Tree1|5.75|0.0
```

Parser:
```bash
python lua_exports/parse_runtime_pathing.py \
  --log "C:/Users/marku/Documents/Siedler5/Logs/Game.log" \
  --output lua_exports/runtime_pathing_data.json
```

## Ergebnisse

Nach dem Parsen enthält `lua_export_data.json`:

```json
{
  "pathfinding": {
    "paths": [
      {"name": "Tree1", "same_sector": true, "distance": 1542}
    ]
  },
  "building_blocking": {
    "buildings": [
      {"type": "PB_Headquarters1", "x": 41100, "y": 23100}
    ]
  }
}
```

## Validierung

Die Pathfinding-Daten können mit `environment.py` verglichen werden:
- `same_sector: true` = Serf kann diesen Punkt erreichen
- Wenn Sektor-Nummern übereinstimmen = verbundene Bereiche
