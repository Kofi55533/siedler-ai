# SIEDLER AI - AGENT STATUS

> **Letzte Aktualisierung**: 2026-01-28
> **Aktueller Task**: PHASE 0.1 FERTIG - Werte-Extraktion abgeschlossen
> **Status**: 332 Actions, KRITISCHE Werte-Abweichungen gefunden!

---

## NÄCHSTE SCHRITTE (Priorität)

1. [x] ~~**REALISTISCHE LEIBEIGENEN-MECHANIK**~~ ✅ (NEU!)
   - **Holz pro Baum: 75** (war falsch: 2, jetzt korrekt aus XD_Tree*.xml)
   - **Auto-Weitersammeln im Radius 4500** (aus PU_Serf.xml)
   - **Leibeigene bauen Gebäude** (nicht mehr automatisch!)
   - Neue Actions: `assign_build_x1/3/5` und `recall_build_x1/3/5`

2. [x] ~~**VEREINFACHTES BATCH-SYSTEM**~~ ✅
   - **KEINE Serf-IDs mehr** (zu komplex für das Modell)
   - Agent wählt: WAS (Kategorie) + WIEVIELE (1, 3, 5)
   - System verwaltet automatisch welche Position/Deposit

3. [ ] **Längeres Training (1M+ Steps)**
   - Empfohlen: 1M Steps für erste Ergebnisse
   - `python colab_training.py` oder `train_100k.py`

---

## LETZTE ÄNDERUNGEN

| Datum | Änderung |
|-------|----------|
| 28.01.2026 | **PHASE 0.1 FERTIG**: Werte-Extraktion aus Original-Spieldateien |
| 28.01.2026 | **KRITISCHE ABWEICHUNGEN**: Scharfschütze 5x zu billig, Hochschule falsche Ressourcen! |
| 28.01.2026 | **config/extracted_values.json**: 94 Gebäude, 12 Soldaten, 204 Technologien, Logic-Parameter |
| 28.01.2026 | **value_diff_report.md**: Detaillierter Vergleich aktuell vs. Original |
| 26.01.2026 | **HOLZ-ZONEN**: 6 strategische Zonen für Bauplatz-Schaffung (36 Actions) |
| 26.01.2026 | **STOLLEN-SAMMELN**: Serfs sammeln an Stollen (XD_Iron1), keine Mine baubbar |
| 26.01.2026 | **MINE-SERF ENTFERNT**: Serfs arbeiten NICHT an gebauten Minen (Worker tun das) |
| 26.01.2026 | **DEPOSIT-BLOCKADE**: Serf-Sammeln blockiert wenn Mine dort gebaut wurde |
| 26.01.2026 | **332 ACTIONS**: +30 durch Holz-Zonen (vorher 302) |
| 25.01.2026 | **PERFORMANCE 30x SCHNELLER**: Reset 97ms → 3ms durch Caching |
| 25.01.2026 | **CODE VEREINFACHT**: serf_id/serf_registry entfernt |
| 25.01.2026 | **ALLE 302 ACTIONS GETESTET**: Alle 12 Kategorien funktionieren korrekt |
| 25.01.2026 | **DEPOSIT/MINE UNTERSCHEIDUNG**: work_location unterscheidet deposit/mine/wood |
| 22.01.2026 | **LEIBEIGENE-BAU-SYSTEM**: Gebäude brauchen Leibeigene zum Bauen |
| 22.01.2026 | **HOLZ KORRIGIERT**: 75 Holz pro Baum (statt 2) aus XD_Tree*.xml |
| 22.01.2026 | **AUTO-WEITERSAMMELN**: Leibeigene suchen automatisch im 4500er Radius |
| 22.01.2026 | **NEUE ACTIONS**: assign_build_x1/3/5, recall_build_x1/3/5 (302 total) |
| 22.01.2026 | **BATCH-SYSTEM KOMPLETT**: Alle Actions mit Batch (1, 3, 5) |
| 22.01.2026 | **SERF-IDs ENTFERNT**: Vereinfachte Zähler statt komplexem ID-Tracking |
| 21.01.2026 | **TRAINING SETUP**: MaskablePPO, Reward-Shaping, 100k Test-Training |
| 21.01.2026 | **MECHANIKEN KOMPLETT**: Alle 7 Tests bestanden (test_mechanics.py) |
| 21.01.2026 | **PATHFINDING KOMPLETT**: Gebäude-Sync in _on_building_completed() |
| 21.01.2026 | **EXTRA2-KORREKTUREN**: Segen (5 Kat.), Alarm, Markt, Steuern |
| 18.01.2026 | A* Pfadfindung implementiert (`pathfinding.py`), WalkableGrid |

---

# REFERENZ

## ARCHITEKTUR-ÜBERSICHT

```
┌─────────────────────────────────────────────────────────────────┐
│                    SiedlerScharfschuetzenEnv                     │
│                       (environment.py)                           │
│  - 188 Actions (Build, Upgrade, Research, Recruit, Worker, etc.) │
│  - Gymnasium-kompatibel                                          │
│  - Action Masking                                                │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ ProductionSys │  │ WorkforceMan  │  │  MapManager   │
│ (production_  │  │ (worker_      │  │ (pathfinding. │
│  system.py)   │  │  simulation.py)│  │  py)          │
│               │  │               │  │               │
│ - Minen       │  │ - WorkTime    │  │ - A* Pathfind │
│ - Refiner     │  │ - Pausen      │  │ - WalkableGrid│
│ - Serfs       │  │ - Effizienz   │  │ - Bauplätze   │
└───────────────┘  └───────────────┘  └───────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │   map_config_wintersturm │
              │         .py              │
              │                          │
              │ - Spieler-Positionen     │
              │ - Minen-Slots            │
              │ - Bäume                  │
              │ - Spielregeln            │
              └─────────────────────────┘
```

---

## DATEIEN

| Datei | Beschreibung | Wichtige Klassen/Funktionen |
|-------|--------------|----------------------------|
| `environment.py` | RL Environment (Gymnasium) | `SiedlerScharfschuetzenEnv`, `buildings_db`, `technologies`, `soldiers_db` |
| `production_system.py` | Produktions- und Leibeigene-Logik | `ProductionSystem`, `Mine`, `Refiner`, `Serf`, `SerfState` |
| `worker_simulation.py` | WorkTime-System für Worker | `Worker`, `WorkforceManager`, `Farm`, `Residence` |
| `pathfinding.py` | A* Pfadfindung | `MapManager`, `WalkableGrid`, `AStarPathfinder`, `PathResult` |
| `map_config_wintersturm.py` | Kartenkonfiguration | `PLAYER_HQ_POSITIONS`, `PLAYER_1_MINE_SHAFTS`, `PLAYER_1_TREES_NEAREST` |
| `wood_zones_config.py` | Holz-Zonen für Bauplätze | `WOOD_ZONES` (6 Zonen mit Bäumen) |
| `game_bridge.py` | Verbindung zum echten Spiel | (noch nicht integriert) |
| `data_extractor.py` | Extrahiert Daten aus Spieldateien | |
| `create_exact_map.py` | Erstellt exakte Kartendaten | |
| `colab_training.py` | Training für Google Colab | `train()`, `evaluate()`, `export_strategy()` |
| `train_100k.py` | Lokales Training (100k Steps) | Schneller Test-Lauf |
| `test_mechanics.py` | Tests für Spielmechaniken | 7 Tests für Segen, Motivation, Scholar, etc. |

### Datendateien

| Datei | Beschreibung |
|-------|--------------|
| `player1_walkable.npy` | Begehbarkeits-Grid (754x747 Pixel) |
| `player1_resources.json` | 909 Bäume + Minen + Vorkommen mit Koordinaten |
| `player1_terrain.npy` | Terrain-Daten |
| `config/game_data.json` | Spieldaten aus XMLs |
| `config/wintersturm_map_data.json` | Vollständige Kartendaten |

---

## TRAINING

### Schnellstart
```bash
# Schneller Test (10k Steps, ~30 Sekunden)
python train_quick_test.py

# Mittleres Training (100k Steps, ~8 Minuten)
python train_100k.py

# Volles Training (1M Steps, ~90 Minuten)
python colab_training.py
```

### Konfiguration (colab_training.py)
```python
TRAINING_CONFIG = {
    "total_timesteps": 1_000_000,
    "learning_rate": 0.0003,
    "n_steps": 2048,
    "batch_size": 64,
    "ent_coef": 0.02,  # Exploration
    "policy_kwargs": {"net_arch": [512, 256, 256]},
}
```

### Tensorboard
```bash
tensorboard --logdir siedler_training_100k/tensorboard
```

### Reward-Shaping
| Aktion | Reward |
|--------|--------|
| Scharfschütze rekrutieren | +5.0 |
| Büchsenmacherei bauen | +3.0 |
| HQ upgraden | +2.5 |
| Mathematik/Fernglas/Luntenschloss | +2.0 |
| Hochschule bauen | +2.0 |
| Eisen/Schwefelmine bauen | +1.5 |
| Finale Belohnung pro Scharfschütze | +10.0 |

---

## DATENSTRUKTUREN

### ResourceType (Enum)
```python
GOLD, WOOD, STONE, CLAY, IRON, SULFUR
```

### Ressourcen-Namen (Environment)
```python
RESOURCE_HOLZ = "Holz"
RESOURCE_STEIN = "Stein"
RESOURCE_LEHM = "Lehm"
RESOURCE_EISEN = "Eisen"
RESOURCE_SCHWEFEL = "Schwefel"
RESOURCE_TALER = "Taler"
```

### Startressourcen
```python
START_RESOURCES = {
    "Taler": 500,
    "Lehm": 2400,
    "Holz": 1750,
    "Stein": 700,
    "Eisen": 50,
    "Schwefel": 50,
}
```

### Gebäude (80+ in buildings_db)
- Hauptquartier (3 Level)
- Dorfzentrum (3 Level)
- Wohnhaus (3 Level)
- Bauernhof (3 Level)
- Hochschule (2 Level)
- Minen: Stein, Lehm, Eisen, Schwefel (je 3 Level)
- Produktionsgebäude: Sägemühle, Lehmhütte, Schmiede, etc.
- Militär: Kaserne, Schießplatz, Stall, Büchsenmacherei

### Technologien (55+ in technologies)
- Konstruktion-Zweig
- Alchimie-Zweig
- Bildung-Zweig
- Militär-Zweig
- **Scharfschützen-Pfad**: Mathematik → Fernglas → Luntenschloss

### Soldaten (40+ in soldiers_db)
- Schwertkämpfer (4 Level)
- Speerträger (4 Level)
- Bogenschützen (4 Level)
- Kavallerie
- **Scharfschützen** (2 Level) - HAUPTZIEL!

---

## SPIELMECHANIKEN

### Leibeigene-System (Serfs) - KORRIGIERT WIE IM ORIGINAL-SPIEL

```
RESSOURCEN-SAMMELN (KORRIGIERT):
1. Agent wählt Kategorie (Holz-Zone/Stollen/Vorkommen) + Batch (1/3/5)
2. System weist Leibeigene automatisch zu verfügbaren Ressourcen zu
3. Leibeigener LÄUFT zur Ressource (A* Pfadfindung, Speed = 400)
4. Leibeigener extrahiert Ressourcen (2 Holz alle 5.52s, etc.)
5. AUTOMATISCHES WEITERSAMMELN im Radius 4500 (aus PU_Serf.xml!)
6. Nur wenn NICHTS im Radius → Leibeigener wird frei

KORREKTE RESSOURCEN-MECHANIK (aus Spieldateien):
┌─────────────────────────────────────────────────────────────────────┐
│ STOLLEN (XD_Iron1, XD_Stone1, etc.)                                 │
│   - 400 Ressourcen pro Stollen                                      │
│   - Serfs können IMMER hier sammeln                                 │
│   - Keine Mine kann auf Stollen gebaut werden!                      │
├─────────────────────────────────────────────────────────────────────┤
│ VORKOMMEN (XD_IronPit1, etc.) - wo Minen GEBAUT werden              │
│   - 12000 Ressourcen (oder 4000 bei kleinen Deposits)               │
│   - Serfs sammeln NUR wenn KEINE Mine dort gebaut ist               │
│   - Sobald Mine gebaut → Serf-Sammeln BLOCKIERT                     │
│   - Worker (PU_Miner) übernehmen dann                               │
├─────────────────────────────────────────────────────────────────────┤
│ GEBAUTE MINEN (PB_IronMine1, etc.)                                  │
│   - Serfs arbeiten NICHT an Minen!                                  │
│   - Nur Worker (Miner) arbeiten hier                                │
│   - BuildOn: XD_IronPit1 (Mine wird auf Vorkommen gebaut)           │
└─────────────────────────────────────────────────────────────────────┘

HOLZ-ZONEN - STRATEGISCH FÜR BAUPLÄTZE:
- 6 Zonen um Minen-Positionen für Raffinerie-Bauplätze
- Schwefelmine-Zone → Alchimistenhütte bauen
- Lehmmine-Zone → Lehmhütte bauen
- Steinmine-Zone → Steinmetzhütte bauen
- Eisenmine-Zone → Schmiede bauen
- Deterministische Zuweisung (nächster Baum zum Zonenzentrum)
- Serfs verteilen sich auf verschiedene Bäume (spread)

WORK_LOCATION TRACKING:
- "wood_zone_XXX": Serf arbeitet in Holz-Zone XXX
- "shaft": Serf arbeitet an Stollen
- "deposit": Serf arbeitet an Vorkommen (nur wenn keine Mine!)
- Recall-Funktionen prüfen work_location für korrekte Unterscheidung

BAUM-DATEN (aus XD_Tree*.xml):
- Standard-Bäume (Fir, Pine, Tree): 75 Holz pro Baum
- Zypressen, Weiden: 50 Holz pro Baum
- Tote Bäume: 10-75 Holz variabel
- Extraktion: 2 Holz alle 5.52s = ~204 Sekunden pro Baum

GEBÄUDE-BAU (NEU - wie im echten Spiel!):
1. Agent startet Bau (Ressourcen werden abgezogen)
2. Agent MUSS Leibeigene zur Baustelle zuweisen (assign_build_x1/3/5)
3. Mehr Leibeigene = schnellerer Bau (1 + 0.5 * (n-1) effektive Worker)
4. Ohne Leibeigene wird NICHT gebaut!

Extraktionsraten (inkl. Animation-Zeit aus extra2):
- Holz: 2 Einheiten alle 5.52s (4s delay + 1.52s animation)
- Eisen: 1 Einheit alle 4.54s (3s delay + 1.54s animation)
- Stein/Lehm: 1 Einheit alle 5.54s (4s delay + 1.54s animation)
- Schwefel: 1 Einheit alle 4.54s (3s delay + 1.54s animation)
```

### WorkTime-System (für reguläre Worker, NICHT Serfs)

```
- Worker haben WorkTime (sinkt beim Arbeiten)
- Bei Hunger: Laufen zu Farm → Essen → Laufen zu Wohnhaus → Ruhen
- Wenn kein Farm/Wohnhaus in 5000 Radius: Camp (nur 10% Regeneration!)
- Erschöpfte Worker (WorkTime=0): Nur 10% Effizienz!
```

### Produktions-System (2-Tier)

**Tier 1: Minen (CMineBehavior)**
- Worker arbeiten lokal
- AmountToMine: 4-6 pro Zyklus (je nach Level)
- Ressourcen sofort gutgeschrieben

**Tier 2: Refiner (CResourceRefinerBehavior)**
- Worker transportiert Rohstoffe
- Laufzeit = Distanz × 2 / Speed
- TransportAmount: 5 Einheiten pro Trip

### Pfadfindung (A* System)

```
┌─────────────────────────────────────────────────────┐
│ WalkableGrid (754x747 Pixel)                        │
│   └─ terrain_base: Statisch (Berge=blockiert)       │
│   └─ buildings: Dynamisch (Gebäude blockieren)      │
│   └─ trees: Dynamisch (Bäume blockieren, fällbar)   │
├─────────────────────────────────────────────────────┤
│ AStarPathfinder                                     │
│   └─ 8-direktionale Bewegung                        │
│   └─ find_path(start, goal) → PathResult            │
│   └─ Kosten: Gerade=10, Diagonal=14                 │
├─────────────────────────────────────────────────────┤
│ MapManager                                          │
│   └─ Koordinaten-Konvertierung (Welt ↔ Grid)        │
│   └─ Bauplatz-Validierung                           │
│   └─ Baum-Tracking mit Welt-Koordinaten             │
└─────────────────────────────────────────────────────┘

Grid-Skalierung:
- SCALE_X = 33.5 (1 Grid-Pixel = 33.5 Spieleinheiten)
- SCALE_Y = 33.8 (1 Grid-Pixel = 33.8 Spieleinheiten)
- Quadrant-Offset: (25240, 0) für Spieler 1
```

---

## KARTENDATEN (Wintersturm)

### Grunddaten
```python
MAP_NAME = "EMS Wintersturm"
MAP_SIZE = (50480, 50496)  # Breite x Höhe
PLAYERS = 4
GAME_MODE = "2v2"  # Teams: 1+2 vs 3+4
```

### Spieler 1 HQ Position
```python
HQ: (41100, 23100)
Dorfzentrum: (39400, 24300)
```

### Minenschächte (Spieler 1)
| Typ | Anzahl | Nächste Position | Distanz zum HQ |
|-----|--------|------------------|----------------|
| Schwefelmine | 3 | (44304, 21484) | 3588 |
| Lehmmine | 3 | (35181, 19553) | 6901 |
| Steinmine | 3 | (40056, 14891) | 8276 |
| Eisenmine | 3 | (36276, 8927) | 14971 |

### Kleine Vorkommen (erschöpfbar, 4000 Einheiten)
| Ressource | Anzahl | Nächste Position | Distanz |
|-----------|--------|------------------|---------|
| Schwefel | 2 | (48125, 20950) | 7347 |
| Stein | 1 | (42800, 15100) | 8179 |
| Lehm | 1 | (31125, 18750) | 10882 |
| Eisen | 2 | (34325, 7950) | 16596 |

### Bäume (Holz) - KORRIGIERT
- **Anzahl**: 888 (909 im Grid geladen)
- **Holz pro Baum**: **75 Einheiten** (aus XD_Tree*.xml)
- **Geschätztes Holz**: **66.600** (888 × 75)
- **Zeit pro Baum**: ~204 Sekunden (37 Extraktionen × 5.52s)
- **Nächster Baum**: (42330, 24030) - Distanz 1542
- **Auto-Suchradius**: 4500 Einheiten (aus PU_Serf.xml)

---

## ACTION SPACE (332 Actions) ✅

| Offset | Kategorie | Anzahl | Beschreibung |
|--------|-----------|--------|--------------|
| 0 | Wait | 1 | Nichts tun |
| 1 | Build Batch | 84 | Gebäude bauen (28 × 3 Batches) |
| 85 | Upgrade | 35 | Gebäude upgraden |
| 120 | Research | 50 | Technologien erforschen |
| 170 | Recruit | 22 | Soldaten rekrutieren |
| 192 | Resource Batch | 84 | Ressourcen-Zuweisung (Holz-Zonen/Vorkommen/Stollen) |
| 276 | Serf | 6 | Leibeigene kaufen/entlassen (1x,3x,5x) |
| 282 | Batch Recruit | 4 | Scharfschützen batch (3x,5x × 2 Level) |
| 286 | Demolish | 28 | Gebäude abreißen |
| 314 | Bless | 5 | Segnen (5 Kategorien) |
| 319 | Tax | 5 | Steuerstufe setzen (0-4) |
| 324 | Alarm | 2 | Alarm AN/AUS |
| 326 | Build Serf | 6 | Leibeigene zu Baustellen zuweisen |

### NEU: Bau-Serfs zuweisen (6 Actions)

| Offset | Action | Beschreibung |
|--------|--------|--------------|
| 296 | assign_build_x1 | 1 Leibeigenen zur Baustelle schicken |
| 297 | assign_build_x3 | 3 Leibeigene zur Baustelle schicken |
| 298 | assign_build_x5 | 5 Leibeigene zur Baustelle schicken |
| 299 | recall_build_x1 | 1 Leibeigenen von Baustelle zurückrufen |
| 300 | recall_build_x3 | 3 Leibeigene von Baustelle zurückrufen |
| 301 | recall_build_x5 | 5 Leibeigene von Baustelle zurückrufen |

**WICHTIG - Neues Bau-System:**
- Gebäude werden NICHT mehr automatisch gebaut!
- Agent muss Leibeigene zur Baustelle schicken (assign_build_xN)
- Mehr Leibeigene = schnellerer Bau: 1 + 0.5 × (n-1) effektive Arbeiter
- 1 Serf = 1× Baugeschwindigkeit, 3 Serfs = 2× Geschwindigkeit, 5 Serfs = 3× Geschwindigkeit

### Ressourcen-Batch-Actions (84 Actions) - NEU!

**Holz-Zonen (36 Actions) - STRATEGISCH FÜR BAUPLÄTZE:**
| Zone | Raffinerie | Bäume | Actions |
|------|------------|-------|---------|
| HQ_Bereich | Wohnhäuser/Bauernhöfe | 69 | assign/recall × 1/3/5 |
| Schwefelmine | Alchimistenhütte | 14 | assign/recall × 1/3/5 |
| Lehmmine | Lehmhütte | 66 | assign/recall × 1/3/5 |
| Steinmine | Steinmetzhütte | 32 | assign/recall × 1/3/5 |
| Dorfzentrum | Expansion | 25 | assign/recall × 1/3/5 |
| Eisenmine | Schmiede | 72 | assign/recall × 1/3/5 |

**Vorkommen (24 Actions):**
- assign/recall für Eisen/Stein/Lehm/Schwefel × 1/3/5
- **WICHTIG**: Serfs können NUR sammeln wenn KEINE Mine dort gebaut wurde!
- Sobald Mine gebaut → Serf-Sammeln blockiert, Worker übernehmen

**Stollen (24 Actions) - IMMER VERFÜGBAR:**
- assign/recall für Eisen/Stein/Lehm/Schwefel × 1/3/5
- Stollen (XD_Iron1 etc.) haben 400 Ressourcen
- Keine Mine kann auf Stollen gebaut werden!
- Serfs können hier IMMER sammeln

**ENTFERNT - Mine-Serf-Zuweisung:**
- Serfs arbeiten NICHT an gebauten Minen!
- Gebaute Minen werden von Workern (PU_Miner) betrieben

**Auto-Weitersammeln:**
- Nach Baum-Fällung: Serf sucht automatisch nächsten Baum im 4500er Radius
- Nach Deposit-Erschöpfung: Serf sucht automatisch nächstes Deposit
- Nur wenn NICHTS im Radius → Serf wird frei

### SEGEN-KATEGORIEN (aus extra2/logic.xml)
| ID | Name | Betroffene Worker |
|----|------|-------------------|
| 1 | Construction | Miner, Farmer, BrickMaker, Sawmillworker, Stonecutter |
| 2 | Research | Scholar, Priest, Engineer, MasterBuilder |
| 3 | Weapons | Smith, Alchemist, Smelter, Gunsmith |
| 4 | Financial | Trader, Treasurer |
| 5 | Canonisation | ALLE Worker (Kombination) |

**Segen-Parameter (extra2):**
- BlessingBonus: +0.3 (+30% Motivation)
- BlessingBonusTime: 180 Sekunden
- BlessingCost: 0 Faith
- RequiredFaith: 5000 pro Kategorie

### Action Masking
- Prüft Ressourcen-Verfügbarkeit
- Prüft Tech-Voraussetzungen
- Prüft Gebäude-Voraussetzungen
- **Tree Assign**: Baum muss existieren + kein Serf zugewiesen + freie Leibeigene
- **Tree Recall**: Serf muss diesem Baum zugewiesen sein
- **Deposit Assign**: Deposit muss Ressourcen haben + kein Serf zugewiesen + freie Leibeigene
- **Deposit Recall**: Serf muss diesem Deposit zugewiesen sein
- **Segen**: Nur wenn Kloster gebaut UND genug Faith

---

## OBSERVATION SPACE

| Bereich | Features | Normalisierung |
|---------|----------|----------------|
| Ressourcen | 6 (Holz, Stein, Lehm, Eisen, Schwefel, Taler) | / 1000 |
| Worker | 7 (5 Ressourcen + free + total Leibeigene) | / 50-100 |
| Gebäude | 54 (27 Typen × 2: count + in_construction) | / 5-10 |
| Upgrades | 34 | / 5 |
| Technologien | 100 (50 × 2: researched + in_progress) | boolean |
| Soldaten | 22 | / 50 |
| Zeit | 2 (current_time, time_remaining) | / max_time |
| Produktion | 6 (Produktionsraten) | / 10 |
| WorkTime | 12 (avg_work_time, efficiency, etc.) | varies |
| Neue Actions | 4 (tax_level, bless_cooldown, etc.) | varies |

---

## SCHARFSCHÜTZEN-PFAD (Optimale Reihenfolge)

### Technologien
1. **Mathematik** - 20s, 100 Taler + 200 Holz
2. **Fernglas** - 30s, 300 Taler + 300 Eisen (benötigt HQ Level 2)
3. **Luntenschloss** - 50s, 300 Eisen + 300 Schwefel

### Gebäude
1. **Hochschule_1** - 120s, 300 Holz + 400 Stein
2. **Hauptquartier_2** (Upgrade) - 90s, 800 Stein + 300 Lehm + 500 Taler
3. **Büchsenmacherei_1** - 120s, 400 Stein + 300 Schwefel + 200 Eisen

### Kritische Ressourcen
- **Eisen**: Start 50, Benötigt 800, Defizit 750
- **Schwefel**: Start 50, Benötigt 650, Defizit 600

---

## SPIELREGELN (EMS Wintersturm)

```python
GAME_RULES = {
    "peacetime_minutes": 40,
    "max_time_minutes": 30,  # Trainingsziel

    "units": {
        "Schwert": 0,  # VERBOTEN
        "Bogen": 4,
        "Speer": 4,
        "SchwereKavallerie": 0,  # VERBOTEN
        "LeichteKavallerie": 0,  # VERBOTEN
        "Scharfschütze": 2,  # Max Level 2
        "Dieb": 1,
        "Kundschafter": 1,
    },

    "forbidden": ["Markt", "Brücke", "Kanone"],
    "tower_level": 1,
    "heroes_per_player": 0,
}
```

---

## BEKANNTE ISSUES / TODOS

### Offen
- [ ] **Motivation Leave**: Threshold <0.25 -> Worker verlassen Settlement (optional)

### Erledigt - MECHANIKEN WIE IM ORIGINAL
- [x] Segen-Cooldown 180s (statt 60s)
- [x] Kloster-Motivation-Effekt (+0.08/0.10/0.15)
- [x] Motivation beeinflusst WorkTime-Regeneration
- [x] Forschung abhängig von Gelehrten-Effizienz
- [x] Scholar bei Hochschule-Bau erstellt
- [x] Gunsmith bei Büchsenmacherei-Bau erstellt
- [x] Fehlende Worker-Typen (scholar, engineer, master_builder, gunsmith)

### Erledigt - Pathfinding
- [x] ~~Pathfinding in Environment integriert~~ ✅ (A* wird genutzt)
- [x] ~~Bäume verschwinden nach Fällung~~ ✅ (map_manager.remove_tree())
- [x] ~~Gebäude blockieren Grid~~ ✅ (map_manager.add_building())

### Erledigt
- [x] A* Pfadfindung implementiert
- [x] 909 Bäume in Grid geladen
- [x] Leibeigene-Logik (laufen, bleiben, extrahieren)
- [x] Action Masking Grundgerüst
- [x] Neue Actions (Serf kaufen/entlassen, Abreißen, Segnen, Steuern)
- [x] Original extra2-Dateien analysiert (Segen, Steuern, Alarm, Kloster)

---

## EXTRA2 REFERENZ-WERTE

### Steuern (logic.xml)
```python
TAX_LEVELS = {
    0: {"tax": 0, "motivation": +0.20},   # Sehr niedrig
    1: {"tax": 5, "motivation": +0.08},   # Niedrig
    2: {"tax": 10, "motivation": 0},      # Normal (Start)
    3: {"tax": 15, "motivation": -0.08},  # Hoch
    4: {"tax": 20, "motivation": -0.12},  # Sehr hoch
}
TaxAmount = 5  # Pro Worker pro Tick
InitialTaxLevel = 2
```

### Motivation (logic.xml)
```python
MotivationThresholdHappy = 1.5   # Sehr glücklich
MotivationThresholdSad = 1.0    # Traurig
MotivationThresholdAngry = 0.7  # Wütend
MotivationThresholdLeave = 0.25 # VERLÄSST Settlement!
MotivationAbsoluteMax = 3.0     # Maximum
```

### Alarm (logic.xml)
```python
AlarmRechargeTime = 180000  # 3 Minuten Cooldown
# Worker gehen zu DefendableBuildings
```

### Kloster/Monastery (pb_monastery1-3.xml)
```python
MONASTERY = {
    1: {"workers": 6, "motivation_effect": 0.08, "hp": 2000},
    2: {"workers": 8, "motivation_effect": 0.10, "hp": 3500},
    3: {"workers": 10, "motivation_effect": 0.15, "hp": 4500},
}
```

### WorkTime-System (pu_priest.xml)
```python
WORKER_WORKTIME = {
    "WorkWaitUntil": 4000,      # ms bevor Arbeit startet
    "WorkTimeChangeWork": -50,   # Reduktion pro Arbeitszyklus
    "EatWait": 2000,            # ms Essenszeit
    "RestWait": 3000,           # ms Ruhezeit
    "WorkTimeChangeFarm": 0.7,  # Regeneration beim Essen
    "WorkTimeChangeResidence": 0.5,  # Regeneration beim Ruhen
    "CamperRange": 5000,        # Wenn kein Gebäude in Reichweite → Camp
}
```

---

## VERWENDUNG

### Environment starten
```python
from environment import SiedlerScharfschuetzenEnv

env = SiedlerScharfschuetzenEnv(player_id=1)
obs, info = env.reset()

# Action ausführen
action = 1  # Erstes Gebäude bauen
obs, reward, done, truncated, info = env.step(action)
```

### Pfadfindung nutzen
```python
from pathfinding import MapManager

manager = MapManager()
manager.load_from_files()

# Pfad finden
result = manager.find_path((41100, 23100), (42330, 24030))
print(f"Distanz: {result.world_distance:.0f} Einheiten")
print(f"Laufzeit: {result.world_distance / 360:.1f} Sekunden")

# Bauplatz prüfen
can_build = manager.can_build_at(40900, 22900, "Wohnhaus")
```

### Produktionssystem testen
```python
from production_system import ProductionSystem, Serf, ResourceType
from worker_simulation import Position

system = ProductionSystem()
hq = Position(41100, 23100)
tree = Position(42330, 24030)

serf = Serf(position=hq)
serf.assign_to_resource(ResourceType.WOOD, tree, hq)

# Simulation
for _ in range(300):
    system.tick(0.1)
```

---

## TERMINOLOGIE

| Begriff | Bedeutung |
|---------|-----------|
| **Stollen (XD_Iron1)** | Ressourcen-Punkte mit 400 Einheiten - Serfs sammeln IMMER, keine Mine baubbar |
| **Vorkommen (XD_IronPit1)** | Große Deposits mit 12000 Einheiten - Minen werden HIER gebaut |
| **Mine (PB_IronMine1)** | Gebäude auf Vorkommen - Worker (nicht Serfs!) arbeiten hier |
| Kleine Vorkommen/Deposits | Sammelbare Ressourcen mit 4000 Einheiten - Serfs nur wenn keine Mine |
| Leibeigene/Serfs | Arbeiter die Ressourcen sammeln (kein WorkTime-System) |
| Holz-Zone | Strategischer Bereich um Mine für Raffinerie-Bauplätze |
| Dorfzentren-Bauplätze | Positionen wo Dorfzentren gebaut werden können |
| WorkTime | Arbeitszeit-System für reguläre Worker (nicht Serfs) |

---

*Diese Datei wird vom AI-Agenten gepflegt. Nach /clear immer zuerst diese Datei lesen!*
