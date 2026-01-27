# GEPLANTE ÄNDERUNGEN - Siedler AI

> **Erstellt:** 2026-01-26
> **Status:** In Diskussion - NOCH NICHT IMPLEMENTIERT
> **Letzte Aktualisierung:** 2026-01-27

---

## ÜBERSICHT

Dieses Dokument sammelt alle besprochenen Änderungen bevor sie implementiert werden.

| # | Änderung | Priorität | Status |
|---|----------|-----------|--------|
| 1 | Multi-Step Action System | Hoch | Besprochen |
| 2 | Dynamische Positionen (nur verfügbare) | Hoch | Besprochen |
| 3 | Lager-System für Refiner | Mittel | Offen (später prüfen) |
| 4 | Dynamische Bauplätze | Hoch | Besprochen |
| 5 | Alle Arbeiter-Laufwege simulieren | Hoch | Besprochen |
| 6 | **Fehlende/Vereinfachte Effekte** | Hoch | **Mit Original abgleichen!** |
| 7 | **Kartendaten unvollständig** | Hoch | **Mit echten Spieldaten abgleichen!** |
| 8 | **Camp-System** | Hoch | **Mit Original abgleichen!** |
| 9 | **Offene Design-Fragen** | Hoch | **Benutzer muss entscheiden!** |
| 10 | **Worker-Spawn/Despawn** | Hoch | **Mit Original abgleichen!** |
| 11 | **Technologie-Effekte nicht angewendet** | Hoch | **Mit Original abgleichen!** |

---

## 1. MULTI-STEP ACTION SYSTEM (Volle Kontrolle)

### Grundprinzip
Statt einem flachen Action Space mit 332 vordefinierten Kombinationen:
**Agent trifft Entscheidungen in mehreren Steps nacheinander.**

### Warum Multi-Step?
- **Volle Kontrolle** für den Agent
- **Kleinerer Action Space** pro Step
- **Keine Masken-Probleme** (jeder Step hat eigenen Discrete Space)
- **Flexibler** - Agent lernt Zusammenhänge

---

### ALLE ACTION-TYPEN MIT MULTI-STEP FLOWS (12 Actions)

#### Übersicht aller Flows

| # | Action-Typ | Step 1 | Step 2 | Step 3 | Step 4 |
|---|------------|--------|--------|--------|--------|
| 1 | Wait | "Wait" | - | - | - |
| 2 | Bauen | "Bauen" | Gebäude? | Position? | - |
| 3 | Upgrade | "Upgrade" | Gebäude? | Position?* | - |
| 4 | Forschen | "Forschen" | Technologie? | - | - |
| 5 | Rekrutieren | "Rekrutieren" | Soldaten-Typ? | Anzahl? | - |
| 6 | Leibeigene kaufen | "Serf kaufen" | Anzahl? | - | - |
| 7 | Leibeigene entlassen | "Serf entlassen" | Von wo? | Anzahl? | - |
| 8 | Leibeigene zuweisen | "Zuweisen" | Von wo? | Anzahl? | Wohin? |
| 9 | Abreißen | "Abreißen" | Gebäude? | Position?* | - |
| 10 | Segnen | "Segnen" | Kategorie? | - | - |
| 11 | Steuern | "Steuern" | Stufe? | - | - |
| 12 | Alarm | "Alarm" | AN/AUS? | - | - |

*Position nur wenn mehrere Gebäude des gleichen Typs existieren

**HINWEIS:** "Abziehen" wurde ENTFERNT - ist jetzt Teil von "Zuweisen" mit Ziel="Frei"

---

### DETAILLIERTE FLOWS

#### 1. WAIT (1 Step)
```
Step 1: "Wait" → [ausführen, Zeit vorrücken]
```
- Keine weiteren Entscheidungen
- Immer erlaubt

---

#### 2. BAUEN (3 Steps)
```
Step 1: "Bauen"
    ↓
Step 2: Welches Gebäude?
        Optionen: Alle baubaren Gebäude-Typen
        Maske: Nur Gebäude die man sich leisten kann UND für die Position existiert
    ↓
Step 3: Wo bauen?
        Optionen: NUR AKTUELL VERFÜGBARE Positionen (dynamisch!)
        Maske: Nur Positionen die für dieses Gebäude gültig sind
    ↓
[ausführen, Zeit vorrücken]
```

**Spezialfälle:**
- **Minen**: Step 3 zeigt nur freie Schacht-Positionen (max 3 pro Typ)
- **Dorfzentrum**: Step 3 zeigt nur Dorfzentrum-Slots (max 3)
- **Normale Gebäude**: Alle verfügbaren Bauplätze

---

#### 3. UPGRADE (2-3 Steps)
```
Step 1: "Upgrade"
    ↓
Step 2: Welches Gebäude upgraden?
        Optionen: [Wohnhaus_1→2, Bauernhof_1→2, HQ_1→2, ...]
        Maske: Nur Gebäude die existieren + Ressourcen vorhanden + Voraussetzungen
    ↓
Step 3: Welche Position? (NUR wenn mehrere vom gleichen Typ!)
        Optionen: Positionen wo dieses Gebäude steht
        Maske: Alle Positionen mit diesem Gebäude
    ↓
[ausführen, Zeit vorrücken]
```

---

#### 4. FORSCHEN (2 Steps)
```
Step 1: "Forschen"
    ↓
Step 2: Welche Technologie?
        Optionen: Alle Technologien
        Maske: Nur Techs mit erfüllten Voraussetzungen + Ressourcen
    ↓
[ausführen, Zeit vorrücken]
```

---

#### 5. REKRUTIEREN - Soldaten (3 Steps)
```
Step 1: "Rekrutieren"
    ↓
Step 2: Welchen Soldaten-Typ?
        Optionen: Alle Soldaten-Typen
        Maske: Nur Typen die rekrutierbar (Gebäude + Tech + Ressourcen)
    ↓
Step 3: Wie viele?
        Optionen: [1, 2, 3, 5, 10, alle_leistbar]
        Maske: Nur Anzahlen die man sich leisten kann
    ↓
[ausführen, Zeit vorrücken]
```

---

#### 6. LEIBEIGENE KAUFEN (2 Steps)
```
Step 1: "Leibeigene kaufen"
    ↓
Step 2: Wie viele?
        Optionen: [1, 2, 3, 5, 10]
        Maske: Nur Anzahlen die man sich leisten kann (Taler)
    ↓
[ausführen, Zeit vorrücken]
```

---

#### 7. LEIBEIGENE ENTLASSEN (3 Steps)
```
Step 1: "Leibeigene entlassen"
    ↓
Step 2: Von wo entlassen?
        Optionen: Alle Bereiche wo Leibeigene sind (siehe BEREICHE unten)
        Maske: Nur Bereiche wo mindestens 1 Leibeigener ist
    ↓
Step 3: Wie viele?
        Optionen: [1, 2, 3, 5, 10, alle]
        Maske: Nur Anzahlen die an dieser Position verfügbar sind
    ↓
[ausführen, Zeit vorrücken]
```

---

#### 8. LEIBEIGENE ZUWEISEN (4 Steps) - VOLLE KONTROLLE

**WICHTIG:** Diese Action ersetzt auch "Abziehen"! Ziel="Frei" = Abziehen

```
Step 1: "Leibeigene zuweisen"
    ↓
Step 2: Von wo nehmen?
        Optionen: Alle QUELL-BEREICHE (siehe unten)
        Maske: Nur Bereiche wo mindestens 1 Leibeigener ist
    ↓
Step 3: Wie viele?
        Optionen: [1, 2, 3, 5, 10, alle]
        Maske: Nur Anzahlen die an Quell-Position verfügbar sind
    ↓
Step 4: Wohin schicken?
        Optionen: Alle ZIEL-BEREICHE (siehe unten)
        Maske: Nur gültige Ziele (nicht erschöpft, nicht blockiert)
    ↓
[ausführen, Zeit vorrücken]
```

---

#### 9. ABREISSEN (2-3 Steps)
```
Step 1: "Abreißen"
    ↓
Step 2: Welches Gebäude?
        Optionen: Alle gebauten Gebäude-Typen
        Maske: Nur Gebäude die existieren
    ↓
Step 3: Welche Position? (NUR wenn mehrere vom gleichen Typ!)
        Optionen: Positionen dieses Gebäude-Typs
        Maske: Alle Positionen mit diesem Gebäude
    ↓
[ausführen, Position wird frei, 50% Ressourcen zurück, Zeit vorrücken]
```

---

#### 10. SEGNEN (2 Steps)
```
Step 1: "Segnen"
    ↓
Step 2: Welche Kategorie?
        Optionen: [Konstruktion, Forschung, Waffen, Finanzen, Kanonisierung]
        Maske: Nur wenn Kloster gebaut UND genug Faith UND nicht auf Cooldown
    ↓
[ausführen, Zeit vorrücken]
```

---

#### 11. STEUERN (2 Steps)
```
Step 1: "Steuern"
    ↓
Step 2: Welche Stufe?
        Optionen: [0-Sehr niedrig, 1-Niedrig, 2-Normal, 3-Hoch, 4-Sehr hoch]
        Maske: Alle immer erlaubt
    ↓
[ausführen, Zeit vorrücken]
```

---

#### 12. ALARM (2 Steps)
```
Step 1: "Alarm"
    ↓
Step 2: AN oder AUS?
        Optionen: [AN, AUS]
        Maske:
          - "AN" nur wenn Cooldown abgelaufen (180s)
          - "AUS" nur wenn Alarm gerade aktiv
    ↓
[ausführen, Zeit vorrücken]
```

---

## 2. BEREICHE FÜR LEIBEIGENE (Von wo / Wohin)

### VOLLSTÄNDIGE LISTE ALLER BEREICHE

#### QUELL-BEREICHE (Von wo nehmen?) - 26 feste + dynamische Baustellen

| # | Kategorie | Bereich-Name | Beschreibung |
|---|-----------|--------------|--------------|
| 0 | Idle | **Frei** | Leibeigene die nichts tun (beim HQ) |
| | | | |
| | **HOLZ-ZONEN (6)** | | |
| 1 | Holz | HQ_Bereich | 69 Bäume, für Wohnhäuser/Bauernhöfe |
| 2 | Holz | Schwefelmine_Zone | 14 Bäume, für Alchimistenhütte |
| 3 | Holz | Lehmmine_Zone | 66 Bäume, für Lehmhütte |
| 4 | Holz | Steinmine_Zone | 32 Bäume, für Steinmetzhütte |
| 5 | Holz | Dorfzentrum_Zone | 25 Bäume, für Expansion |
| 6 | Holz | Eisenmine_Zone | 72 Bäume, für Schmiede |
| | | | |
| | **EISEN-STOLLEN (3)** | | |
| 7 | Stollen | Eisen_Stollen_1 | Position (36276, 8927), 400 Ressourcen |
| 8 | Stollen | Eisen_Stollen_2 | Position (37495, 7801), 400 Ressourcen |
| 9 | Stollen | Eisen_Stollen_3 | Position (37784, 7266), 400 Ressourcen |
| | | | |
| | **STEIN-STOLLEN (3)** | | |
| 10 | Stollen | Stein_Stollen_1 | Position (40056, 14891), 400 Ressourcen |
| 11 | Stollen | Stein_Stollen_2 | Position (39321, 14716), 400 Ressourcen |
| 12 | Stollen | Stein_Stollen_3 | Position (38633, 14720), 400 Ressourcen |
| | | | |
| | **LEHM-STOLLEN (3)** | | |
| 13 | Stollen | Lehm_Stollen_1 | Position (35181, 19553), 400 Ressourcen |
| 14 | Stollen | Lehm_Stollen_2 | Position (35106, 18872), 400 Ressourcen |
| 15 | Stollen | Lehm_Stollen_3 | Position (34991, 17997), 400 Ressourcen |
| | | | |
| | **SCHWEFEL-STOLLEN (3)** | | |
| 16 | Stollen | Schwefel_Stollen_1 | Position (44304, 21484), 400 Ressourcen |
| 17 | Stollen | Schwefel_Stollen_2 | Position (44006, 20978), 400 Ressourcen |
| 18 | Stollen | Schwefel_Stollen_3 | Position (44576, 22120), 400 Ressourcen |
| | | | |
| | **VORKOMMEN (6)** | | Nur wenn KEINE Mine dort! |
| 19 | Vorkommen | Eisen_Vorkommen_1 | Position (34325, 7950), 4000 Ressourcen |
| 20 | Vorkommen | Eisen_Vorkommen_2 | Position (36325, 6750), 4000 Ressourcen |
| 21 | Vorkommen | Stein_Vorkommen_1 | Position (42800, 15100), 4000 Ressourcen |
| 22 | Vorkommen | Lehm_Vorkommen_1 | Position (31125, 18750), 4000 Ressourcen |
| 23 | Vorkommen | Schwefel_Vorkommen_1 | Position (48125, 20950), 4000 Ressourcen |
| 24 | Vorkommen | Schwefel_Vorkommen_2 | Position (47725, 18550), 4000 Ressourcen |
| | | | |
| | **BAUSTELLEN (dynamisch)** | | |
| 25+ | Baustelle | Baustelle_1, _2, ... | Aktive Bauprojekte (variiert) |

**Gesamt feste Bereiche:** 25 (1 Frei + 6 Holz + 12 Stollen + 6 Vorkommen)
**Plus dynamische Baustellen:** 0-10+ (je nach aktiven Bauprojekten)

---

#### ZIEL-BEREICHE (Wohin schicken?) - Gleiche Liste + Bedingungen

| # | Bereich-Name | Bedingung für Ziel |
|---|--------------|-------------------|
| 0 | **Frei** | Immer möglich (= ABZIEHEN!) |
| | | |
| 1-6 | Holz-Zonen | Wenn noch Bäume in Zone vorhanden |
| | | |
| 7-18 | Stollen | Immer möglich (Stollen erschöpfen nicht für Spieler) |
| | | |
| 19-24 | Vorkommen | NUR wenn: |
| | | - KEINE Mine dort gebaut wurde |
| | | - Noch Ressourcen vorhanden (>0) |
| | | |
| 25+ | Baustellen | Wenn Bauprojekt aktiv |

---

### MASKEN-LOGIK FÜR BEREICHE

```python
def _mask_source_areas(self):
    """Maske für Step 2: Von wo nehmen?"""
    mask = np.zeros(MAX_AREAS, dtype=bool)

    # Frei: Wenn idle Leibeigene existieren
    if self.free_leibeigene > 0:
        mask[0] = True

    # Holz-Zonen: Wenn Leibeigene dort arbeiten
    for i, zone in enumerate(self.wood_zones):
        if zone.assigned_serfs > 0:
            mask[1 + i] = True

    # Stollen: Wenn Leibeigene dort arbeiten
    for i, shaft in enumerate(self.shafts):
        if shaft.assigned_serfs > 0:
            mask[7 + i] = True

    # Vorkommen: Wenn Leibeigene dort arbeiten
    for i, deposit in enumerate(self.deposits):
        if deposit.assigned_serfs > 0:
            mask[19 + i] = True

    # Baustellen: Wenn Leibeigene dort arbeiten
    for i, site in enumerate(self.construction_sites):
        if site.assigned_serfs > 0:
            mask[25 + i] = True

    return mask

def _mask_target_areas(self):
    """Maske für Step 4: Wohin schicken?"""
    mask = np.zeros(MAX_AREAS, dtype=bool)

    # Frei: Immer möglich (= Abziehen)
    mask[0] = True

    # Holz-Zonen: Wenn noch Bäume vorhanden
    for i, zone in enumerate(self.wood_zones):
        if zone.remaining_trees > 0:
            mask[1 + i] = True

    # Stollen: Immer möglich
    for i in range(12):
        mask[7 + i] = True

    # Vorkommen: Nur wenn keine Mine dort UND Ressourcen > 0
    for i, deposit in enumerate(self.deposits):
        if not deposit.has_mine_built and deposit.remaining > 0:
            mask[19 + i] = True

    # Baustellen: Wenn Bauprojekt aktiv
    for i, site in enumerate(self.construction_sites):
        if site.is_active:
            mask[25 + i] = True

    return mask
```

---

## 3. DYNAMISCHE POSITIONEN FÜR BAUEN

### Prinzip: Alle möglichen Positionen, nur verfügbare in Maske (Option C)

Der Agent hat Zugriff auf **ALLE möglichen Positionen** - die Maske filtert auf aktuell verfügbare!

**Keine künstliche Begrenzung!**

```python
# Alle Positionen sind im Action Space
# Zone A: ~1962 sofort bebaubar
# Zone B: ~238 nach Holzfällen
# Gesamt: ~2200 mögliche Positionen

MAX_POSITIONS = 2200  # Alle möglichen Positionen!
```

### Gymnasium Action Space (fest) + Maske (dynamisch)

```python
class ActionPhase:
    POSITION = "position"

# Action Space ist FEST (alle möglichen Positionen)
self.action_spaces[ActionPhase.POSITION] = Discrete(MAX_POSITIONS)  # 2200

def _mask_position(self):
    """Maske zeigt nur aktuell verfügbare Positionen."""
    mask = np.zeros(MAX_POSITIONS, dtype=bool)

    available = self._get_available_positions_for(self.pending_building)

    # Nur verfügbare Positionen sind True
    for pos in available:
        pos_index = self.position_to_index[pos]  # Feste Index-Zuordnung
        mask[pos_index] = True

    return mask
```

### Feste Index-Zuordnung für Positionen

Jede Position hat einen **festen Index** - ändert sich nie:

```python
# Beim Environment-Init: Alle Positionen bekommen festen Index
self.all_positions = []  # Liste aller ~2200 Positionen
self.position_to_index = {}  # Position -> Index Mapping
self.index_to_position = {}  # Index -> Position Mapping

# Zone A Positionen (0 - 1961)
for i, pos in enumerate(zone_a_positions):
    self.all_positions.append(pos)
    self.position_to_index[pos] = i
    self.index_to_position[i] = pos

# Zone B Positionen (1962 - 2199)
for i, pos in enumerate(zone_b_positions):
    idx = 1962 + i
    self.all_positions.append(pos)
    self.position_to_index[pos] = idx
    self.index_to_position[idx] = pos
```

### Positions-Typen je nach Gebäude

| Gebäude-Typ | Verfügbare Positionen | Maske |
|-------------|----------------------|-------|
| Normale Gebäude | Alle freien Bauplätze | ~1962-2200 möglich |
| Minen | Nur freie Schacht-Positionen | max 3 True |
| Dorfzentrum | Nur Dorfzentrum-Slots | max 3 True |

### Warum feste Indices wichtig sind

Der Agent lernt: **"Position 1542 ist nahe HQ, gut für Wohnhaus"**

Wenn Indices sich ändern würden, könnte der Agent nichts lernen!

---

## 4. ZUSAMMENFASSUNG ACTION SPACES

| Phase | Discrete Space Größe | Beschreibung |
|-------|---------------------|--------------|
| MAIN | 12 | Haupt-Action-Kategorien |
| BUILDING | ~28 | Gebäude-Typen |
| POSITION | **~2200** | Alle Positionen (Maske filtert verfügbare) |
| TECH | ~50 | Technologien |
| SOLDIER | ~22 | Soldaten-Typen |
| QUANTITY | 6 | Anzahl [1,2,3,5,10,alle] |
| SOURCE | ~35 | Quell-Bereiche (25 fest + Baustellen) |
| TARGET | ~35 | Ziel-Bereiche (25 fest + Baustellen) |
| CATEGORY | 5 | Segen-Kategorien |
| TAX_LEVEL | 5 | Steuerstufen |
| ON_OFF | 2 | AN/AUS |

**Maximale Step-Tiefe:** 4 (bei Leibeigene zuweisen)

**WICHTIG:** POSITION hat feste Größe (~2200), aber Maske ist meist sehr sparse (wenige True)!

---

## 5. TECHNISCHE IMPLEMENTIERUNG

### Phase-Tracking
```python
class ActionPhase(Enum):
    MAIN = "main"
    BUILDING = "building"
    POSITION = "position"
    TECH = "tech"
    SOLDIER = "soldier"
    QUANTITY = "quantity"
    SOURCE = "source"
    TARGET = "target"
    CATEGORY = "category"
    TAX_LEVEL = "tax_level"
    ON_OFF = "on_off"
```

### Flow-Definitionen (12 Actions, "Abziehen" entfernt!)
```python
ACTION_FLOWS = {
    "wait": [ActionPhase.MAIN],
    "build": [ActionPhase.MAIN, ActionPhase.BUILDING, ActionPhase.POSITION],
    "upgrade": [ActionPhase.MAIN, ActionPhase.BUILDING, ActionPhase.POSITION],
    "research": [ActionPhase.MAIN, ActionPhase.TECH],
    "recruit": [ActionPhase.MAIN, ActionPhase.SOLDIER, ActionPhase.QUANTITY],
    "buy_serf": [ActionPhase.MAIN, ActionPhase.QUANTITY],
    "dismiss_serf": [ActionPhase.MAIN, ActionPhase.SOURCE, ActionPhase.QUANTITY],
    "assign_serf": [ActionPhase.MAIN, ActionPhase.SOURCE, ActionPhase.QUANTITY, ActionPhase.TARGET],
    # "recall_serf" ENTFERNT - jetzt Teil von assign_serf mit target=Frei!
    "demolish": [ActionPhase.MAIN, ActionPhase.BUILDING, ActionPhase.POSITION],
    "bless": [ActionPhase.MAIN, ActionPhase.CATEGORY],
    "tax": [ActionPhase.MAIN, ActionPhase.TAX_LEVEL],
    "alarm": [ActionPhase.MAIN, ActionPhase.ON_OFF],
}
```

### MAIN Action Indices
```python
MAIN_ACTIONS = {
    0: "wait",
    1: "build",
    2: "upgrade",
    3: "research",
    4: "recruit",
    5: "buy_serf",
    6: "dismiss_serf",
    7: "assign_serf",  # Inkludiert jetzt auch "abziehen" (Ziel=Frei)
    8: "demolish",
    9: "bless",
    10: "tax",
    11: "alarm",
}
```

---

## 6. LAGER-SYSTEM FÜR REFINER

### Status
**OFFEN** - Muss mit echten Spieldateien überprüft werden

### Zu prüfen
- [ ] Wie funktioniert Ressourcen-Fluss im echten Spiel?
- [ ] Gibt es Lager-Gebäude?
- [ ] Woher holen Refiner ihre Input-Ressourcen?

---

## 7. DYNAMISCHE BAUPLÄTZE

### Beschreibung
- Bäume fällen → neue Positionen werden frei
- Gebäude abreißen → Position wird wieder frei
- Gebäude bauen → Position wird belegt

---

## 8. ALLE ARBEITER-LAUFWEGE SIMULIEREN

### Zu erweitern
- **Refiner-Worker**: Laufen zur Ressourcen-Quelle und zurück
- **Auswirkung**: Platzierung wichtig (Schmiede nahe Eisenmine = schneller)

---

## 9. OFFENE FRAGEN - VOM BENUTZER ZU BEANTWORTEN

> **Diese Fragen müssen beantwortet werden bevor implementiert wird!**

---

### 9.1 Multi-Step System
- [x] ~~"Abziehen" mit "Zuweisen" zusammenführen~~ ✓ ERLEDIGT
- [x] ~~Positionen: Top N oder alle?~~ ✓ ERLEDIGT - ALLE ~2200 Positionen, Maske filtert
- [x] **Observation**: ✓ ENTSCHIEDEN - **Erweiterte Observation** (Phase + bisherige Auswahlen)
- [x] **Reward**: ✓ ENTSCHIEDEN - **Nur am Ende des Flows** (sparse reward, Agent lernt selbst)
- [x] **Reset**: ✓ ENTSCHIEDEN - **Flow zu Ende führen** (bisschen über 30 Min ist OK)

---

### 9.2 Leibeigene
- [x] **Maximale Anzahl**: ✓ ENTSCHIEDEN - Durch **Dorfzentrum-Kapazität** limitiert
- [ ] **Kosten** pro Leibeigener? → Mit Original abgleichen
- [x] **Sterben**: ✓ ENTSCHIEDEN - **NEIN**, Leibeigene können NICHT sterben
- [x] **Essen/Motivation**: ✓ ENTSCHIEDEN - **NEIN**, Leibeigene brauchen NICHTS davon

---

### 9.3 Camp-System (MIT ORIGINAL ABGLEICHEN!)

> **⚠️ Aktuell vereinfacht - muss mit Spieldaten abgeglichen werden!**

**Aktuell implementiert:**
```python
# Worker campen am Arbeitsplatz wenn kein Bauernhof in Nähe
# Nur +10% Regeneration statt voller Erholung
```

**Offene Fragen für Original-Abgleich:**
- [ ] **Wo werden Camps platziert?** (am Arbeitsplatz? Separate Position?)
- [ ] **Wer platziert Camps?** (automatisch vom Spiel? Spieler muss bauen?)
- [ ] **Camp-Kapazität?** (wie viele Worker pro Camp?)
- [ ] **Camp-Reichweite?** (wie weit darf Arbeitsplatz entfernt sein?)
- [ ] **Regenerations-Rate im Camp?** (aktuell: 10% - ist das korrekt?)
- [ ] **Sind Camps Gebäude?** (oder nur virtuell?)
- [ ] **Kosten/Bauzeit für Camps?**

**Zu prüfen in Spieldateien:**
- [ ] `entities/Buildings/B_Camp/` oder ähnlich
- [ ] `logic.xml` - Worker-Verhalten ohne Bauernhof
- [ ] Wie entscheidet das Spiel wo Worker schlafen?

---

### 9.4 Worker-Verhalten
- [ ] **Wohin gehen Worker zum Essen?** (Bauernhof? Wohnhaus? Taverne?)
- [ ] **Wie weit laufen Worker maximal?** (Radius vom Arbeitsplatz?)
- [ ] **Priorität**: Arbeiten vs. Essen vs. Schlafen?
- [ ] **Erschöpfung**: Was passiert bei 0% WorkTime? (Streik? Langsamer?)

---

### 9.5 Worker-Spawn/Despawn (MIT ORIGINAL ABGLEICHEN!)

> **⚠️ Wichtig für korrekte Simulation!**

**Offene Fragen:**

1. **Woher kommen Worker?**
   - [ ] Spawnen aus Dorfzentrum?
   - [ ] Oder aus Wohnhaus?
   - [ ] Oder einfach "erscheinen" sie am Arbeitsplatz?

2. **Welches Dorfzentrum?**
   - [ ] Nächstes zum Arbeitsplatz?
   - [ ] Das mit freier Kapazität?
   - [ ] Zufällig?

3. **Laufweg beim Spawn?**
   - [ ] Laufen Worker vom Dorfzentrum zum Arbeitsplatz? (Zeit simulieren!)
   - [ ] Oder erscheinen sie sofort am Arbeitsplatz?
   - [ ] Wie lange dauert das?

4. **Despawn bei Abriss:**
   - [ ] Verschwinden Worker zurück ins Dorfzentrum?
   - [ ] Laufen sie zurück? (Zeit?)
   - [ ] Oder werden sie sofort "frei"?
   - [ ] Können sie einem anderen Gebäude zugewiesen werden?

5. **Gebäude fertig gebaut:**
   - [ ] Wann spawnen Worker? (Sofort nach Bau? Nach Verzögerung?)
   - [ ] Laufen sie zum Gebäude?

**Auswirkungen auf Simulation:**
- Gebäude weit vom Dorfzentrum = längere Zeit bis Worker arbeiten
- Abriss = Worker müssen erst zurücklaufen bevor sie neu zugewiesen werden können
- Platzierung wichtig für Effizienz!

**Zu prüfen in Spieldateien:**
- [ ] `logic.xml` - Worker-Spawn Logik
- [ ] `entities/Workers/` - Spawn-Verhalten
- [ ] Wie berechnet das Spiel welches DZ zuständig ist?

---

### 9.5 Produktions-Ketten
- [ ] **Lager-System**: Woher holen Refiner ihre Input-Ressourcen?
  - Direkt von Mine?
  - Aus zentralem Lager?
  - Leibeigene transportieren?
- [ ] **Output-Transport**: Wohin gehen fertige Waren?
- [ ] **Puffer**: Haben Gebäude interne Lager?

---

### 9.6 Soldaten-Rekrutierung
- [ ] **Woher kommen Rekruten?** (Leibeigene werden Soldaten? Oder separate?)
- [ ] **Ausbildungszeit?** (wie lange dauert Rekrutierung?)
- [ ] **Kaserne-Kapazität?** (wie viele gleichzeitig ausbilden?)
- [ ] **Ausrüstung**: Automatisch oder muss produziert werden?

---

## 10. FEHLENDE/VEREINFACHTE EFFEKTE

> **⚠️ WICHTIG: Mit Original-Spieldateien abgleichen!**
>
> Die folgenden Effekte sind entweder nicht implementiert oder stark vereinfacht.
> Vor der Implementierung müssen die echten Werte aus den Spieldateien (XML, LUA) extrahiert werden.

---

### 10.1 KAPELLE (NICHT IMPLEMENTIERT)

**Status:** ❌ Komplett fehlend

**Im Original-Spiel:**
- Kapelle = einfacheres religiöses Gebäude
- Produziert Faith (weniger als Kloster)
- Kann KEINE Segen sprechen (nur Kloster kann das)
- Motivation-Effekt? (zu prüfen)

**Zu prüfen in Spieldateien:**
- [ ] `entities/Buildings/B_ChurchVillage/` - Kapelle-Daten
- [ ] Faith-Produktion pro Sekunde
- [ ] Motivation-Effekt falls vorhanden
- [ ] Kosten und Bauzeit
- [ ] Worker-Anzahl

---

### 10.2 SEGEN-EFFEKTE (VEREINFACHT)

**Status:** ⚠️ Teilweise implementiert

**Aktuell implementiert:**
```python
# Nur GLOBALER Motivation-Bonus!
for cat in BLESS_CATEGORIES:
    if self.bless_active_times.get(cat, 0) > 0:
        motivation += BLESS_MOTIVATION_BONUS  # +30% global
```

**Problem:** Die `worker_types` Liste wird **IGNORIERT**!

**Im Original-Spiel:**
- Segen wirkt NUR auf Worker der jeweiligen Kategorie
- Nicht alle Worker bekommen +30%!

**5 Segen-Kategorien und ihre Worker:**

| # | Kategorie | Worker-Typen | Aktuell |
|---|-----------|--------------|---------|
| 0 | Construction | Miner, Farmer, BrickMaker, Sawmillworker, Stonecutter | ❌ Ignoriert |
| 1 | Research | Scholar, Priest, Engineer, MasterBuilder | ❌ Ignoriert |
| 2 | Weapons | Smith, Alchemist, Smelter, Gunsmith | ❌ Ignoriert |
| 3 | Financial | Trader, Treasurer | ❌ Ignoriert |
| 4 | Canonisation | ALLE Worker | ✓ Korrekt (da global) |

**Zu implementieren:**
```python
def _get_worker_motivation(self, worker_type):
    """Motivation für spezifischen Worker-Typ."""
    base_motivation = self._get_base_motivation()

    # Segen-Bonus nur wenn dieser Worker-Typ gesegnet
    for cat, info in BLESS_CATEGORIES.items():
        if self.bless_active_times.get(cat, 0) > 0:
            if "ALL" in info["worker_types"] or worker_type in info["worker_types"]:
                base_motivation += BLESS_MOTIVATION_BONUS
                break  # Nur einmal Bonus!

    return base_motivation
```

**Zu prüfen in Spieldateien:**
- [ ] `extra2/logic.xml` - BlessingBonus Details
- [ ] Welche Worker-Typen existieren genau?
- [ ] Stapeln sich Segen (mehrere Kategorien)?
- [ ] Was passiert bei Canonisation + andere Kategorie?

---

### 10.3 FORSCHUNGS-QUEUES (VEREINFACHT)

**Status:** ⚠️ Vereinfacht - nur eine globale Queue

**Aktuell implementiert:**
- Eine einzige `active_research` Variable
- Alle Forschungen laufen im gleichen "Slot"
- `requires_building` prüft nur Voraussetzung

**Im Original-Spiel:**
- **Hochschule**: Allgemeine Technologien
- **Schmiede**: Waffen/Rüstungs-Technologien
- **Alchimistenhütte**: Schießpulver/Bomben
- **Hauptquartier**: Militär-Strategien
- **Bank**: Wirtschafts-Forschungen

**Mögliche Auswirkungen:**
- Parallel forschen? (zu prüfen)
- Jedes Gebäude hat eigene Gelehrte?

**Zu prüfen in Spieldateien:**
- [ ] `Technologies.xml` - Alle Technologien und ihre Gebäude
- [ ] Kann man parallel forschen an verschiedenen Orten?
- [ ] Welche Gebäude haben Forschungs-Slots?
- [ ] Wie viele Gelehrte pro Gebäude?

---

### 10.4 FAITH-PRODUKTION (VEREINFACHT)

**Status:** ⚠️ Stark vereinfacht

**Aktuell implementiert:**
```python
# Vereinfacht: 6 Priester pro Kloster, Faith linear
priests = total_monasteries * 6
self.faith = min(self.faith + priests * TIME_STEP, ...)
```

**Im Original-Spiel:**
- Priester = echte Worker mit WorkTime
- Faith-Produktion hängt von Priester-Effizienz ab
- Kapelle produziert auch Faith (weniger)

**Zu prüfen in Spieldateien:**
- [ ] `entities/Buildings/B_Monastery/` - Kloster-Daten
- [ ] Faith pro Priester pro Sekunde
- [ ] Wie viele Priester maximal?
- [ ] Priester-WorkTime Einfluss

---

### 10.5 KLOSTER MOTIVATION-EFFEKT (ZU VERIFIZIEREN)

**Status:** ✓ Implementiert, aber Werte prüfen

**Aktuell implementiert:**
```python
"Kloster_1": motivation_effect=0.08  # +8%
"Kloster_2": motivation_effect=0.10  # +10%
"Kloster_3": motivation_effect=0.15  # +15%
```

**Zu prüfen in Spieldateien:**
- [ ] `extra2/logic.xml` - Monastery MotivationEffect
- [ ] Sind die Werte 0.08/0.10/0.15 korrekt?
- [ ] Gilt Effekt für alle Worker oder nur bestimmte?

---

### 10.6 TECHNOLOGIE-EFFEKTE (NICHT ANGEWENDET!)

**Status:** ❌ **KRITISCH** - Effekte sind definiert aber werden NIRGENDS angewendet!

**Problem:**
Die Technologie-Datenbank in `environment.py` (Zeile 521-652) definiert 55+ Technologien mit `effects`-Dictionaries.
Aber wenn eine Forschung abgeschlossen wird (Zeile 3209), passiert NUR:
```python
self.researched_techs.add(tech)  # Nur in Set gespeichert!
self.current_research = None
# KEIN Code der effects anwendet!
```

**Keine der folgenden Effekte wird jemals angewendet:**

#### TRAINING-RELEVANT → MÜSSEN implementiert + abgeglichen werden!

| Effekt-Typ | Technologien | Was es tun SOLLTE | Warum relevant |
|-----------|-------------|-------------------|----------------|
| `build_speed_bonus` | Ziegelbrennen (+15) | Schneller bauen | Bauzeit = Engpass in Produktionskette! |
| `worker_speed_bonus` | Straßenbau (+20) | Worker laufen schneller | Laufzeit beeinflusst ALLE Produktions-Zyklen! |
| `archer_training_speed` | Schützenschule (+20) | Schnellere Schützen-Rekrutierung | **DIREKT relevant für Scharfschützen-Ziel!** |
| `infantry_training_speed` | Infanterie-Ausbildung (+20) | Schnellere Infanterie-Rekrutierung | Soldaten-Produktion beschleunigen |
| `payday_bonus` | Lohnbuchhaltung (+10), Finanzplanung (+20) | Lohn-Kosten reduzieren | Wirtschaft = mehr Ressourcen für Produktion |
| `trade_bonus` | Handelsrecht (+5), Handelsgilden (+10) | Handelsgewinne erhöhen | Wirtschaft = mehr Taler |

#### MILITÄR-RELEVANT → Implementieren wenn Kampf simuliert wird

| Effekt-Typ | Technologien | Was es tun SOLLTE |
|-----------|-------------|-------------------|
| `armor_bonus` | Kettenpanzer (+5), Lederrüstung (+2), Kettenrüstung (+4), Plattenpanzer (+6) | Rüstung von Nahkämpfern erhöhen |
| `speed_bonus` | Pferdezucht (+50) | Kavallerie-Geschwindigkeit |
| `building_armor_bonus` | Mauerbau (+3) | Gebäude-Verteidigung erhöhen |
| `bow_damage_bonus` | Langbögen (+2), Kompositbögen (+4) | Bogenschaden erhöhen |
| `cannon_damage_bonus` | Schwarzpulver (+3), Sprengstoff (+5) | Kanonenschaden erhöhen |
| `melee_damage_bonus` | Schwertschmied (+2), Waffenmeister (+4) | Nahkampfschaden erhöhen |
| `archer_armor_bonus` | Schützenrüstung (+1/+2/+3) | Schützen-Rüstung erhöhen |
| `spear_damage_bonus` | Speerträger (+2), Hellebarden (+4) | Speer-Schaden erhöhen |
| `cavalry_speed_bonus` | Reitkunst (+50) | Kavallerie schneller |
| `cannon_speed_bonus` | Artillerie-Training (+30) | Kanonen schneller |

#### UNKLAR → Relevanz klären

| Effekt-Typ | Technologien | Was es tun SOLLTE |
|-----------|-------------|-------------------|
| `exploration_bonus` | Kartographie (+5) | Erkundung verbessern? |
| `worker_armor_bonus` | Bürgerwehr (+1) | Worker-Rüstung (relevant bei Angriffen?) |

**Zusätzlich: `game_data.json` hat LEERE Effekte!**
- Alle 204 Technologie-Einträge in `game_data.json` haben `"effects": []`
- Die Effekt-Werte in `environment.py` sind **manuell geschätzt**, NICHT aus Spieldateien!
- **→ Alle Werte MÜSSEN mit dem Original-Spiel abgeglichen werden!**

**Zu prüfen in Spieldateien:**
- [ ] Welche Effekte existieren WIRKLICH im Original?
- [ ] Exakte Werte für jeden Effekt (die aktuellen Werte sind geraten!)
- [ ] Wie werden Effekte angewendet? (Multiplikator? Addiert? Prozent?)
- [ ] Gibt es Effekte die NICHT in der Datenbank stehen?
- [ ] `Technologies.xml` oder `logic.xml` - Effekt-Definitionen
- [ ] Gelten `training_speed` Boni auch für Scharfschützen?

**Zu implementieren:**
```python
def _apply_tech_effects(self):
    """Berechne aktive Tech-Effekte aus erforschten Technologien."""
    self.active_effects = {}
    for tech in self.researched_techs:
        tech_info = technologies.get(tech, {})
        effects = tech_info.get("effects", {})
        for effect_name, value in effects.items():
            self.active_effects[effect_name] = (
                self.active_effects.get(effect_name, 0) + value
            )

# Dann in relevanten Berechnungen nutzen:
def _get_build_speed(self):
    bonus = self.active_effects.get("build_speed_bonus", 0)
    return BASE_BUILD_SPEED * (1 + bonus / 100)

def _get_worker_speed(self):
    bonus = self.active_effects.get("worker_speed_bonus", 0)
    return BASE_WORKER_SPEED * (1 + bonus / 100)

def _get_training_speed(self, unit_type):
    if "infantry" in unit_type:
        bonus = self.active_effects.get("infantry_training_speed", 0)
    elif "archer" in unit_type or "Scharfschütze" in unit_type:
        bonus = self.active_effects.get("archer_training_speed", 0)
    # etc.
    return BASE_TRAIN_TIME * (1 - bonus / 100)
```

---

### 10.7 CHECKLISTE: MIT ORIGINAL ABGLEICHEN

**Spieldateien zu analysieren:**

| Datei | Zu prüfen | Status |
|-------|-----------|--------|
| `extra2/logic.xml` | Segen, Motivation, Timing | ⬜ Offen |
| `Technologies.xml` | Alle Techs, Forschungs-Orte | ⬜ Offen |
| `entities/Buildings/B_ChurchVillage/` | Kapelle-Daten | ⬜ Offen |
| `entities/Buildings/B_Monastery/` | Kloster-Daten, Priester | ⬜ Offen |
| `entities/Workers/` | Worker-Typen, Kategorien | ⬜ Offen |

**Fragen für Original-Abgleich:**

1. **Kapelle:**
   - [ ] Existiert Kapelle? Welche Effekte?
   - [ ] Faith-Produktion?
   - [ ] Motivation-Bonus?

2. **Segen:**
   - [ ] Wirkt Segen nur auf bestimmte Worker?
   - [ ] Stapeln sich mehrere Segen?
   - [ ] Exakte Bonus-Werte?

3. **Forschung:**
   - [ ] Parallele Forschung möglich?
   - [ ] Separate Queues pro Gebäude?
   - [ ] Gelehrte pro Gebäude?

4. **Faith:**
   - [ ] Faith pro Priester?
   - [ ] Priester-WorkTime Einfluss?
   - [ ] Max Faith Cap?

---

## 11. KARTENDATEN - MIT ECHTEN SPIELDATEN ABGLEICHEN

> **⚠️ KRITISCH: Kartendaten sind unvollständig/approximiert!**
>
> Die aktuellen Kartendaten müssen mit den **ECHTEN Spieldateien** abgeglichen werden.
> Ohne korrekte Daten kann der Agent keine realistischen Entscheidungen lernen.

---

### 11.1 BEGEHBARKEITS-GRID (NICHT ECHT!)

**Status:** ❌ **KRITISCH** - Nur Terrain-Höhe, KEINE echte Blocking-Map!

**Aktuell vorhanden:**
```python
# create_walkable_map.py Kommentar:
# WICHTIG: Die Binärdatei enthält NICHT direkt Blocking-Daten!
# Die Terrain-Datei zeigt nur Höhen, nicht die tatsächliche Blocking-Map.
# HINWEIS: Alle Ressourcen-Positionen SIND im echten Spiel begehbar!
```

**Problem:**
- `walkable_grid.png` zeigt nur Terrain-Höhen (approximiert)
- Keine echte Blocking-Map aus Spieldateien
- Pfadfindung basiert nur auf Luftlinien-Distanz

**Auswirkungen:**
- Worker-Laufzeiten sind UNGENAU
- Keine Kollisionsvermeidung mit Bergen/Wasser
- A* Pfadfindung kann nicht korrekt arbeiten

**Zu extrahieren aus Spieldateien:**
- [ ] Echte Blocking-Map (welche Tiles sind begehbar?)
- [ ] Terrain-Typen (Wasser, Berg, Wald, etc.)
- [ ] Passierbarkeit pro Tile

---

### 11.2 GEBÄUDE-GRÖßEN (NUR GESCHÄTZT)

**Status:** ⚠️ Geschätzte Werte, nicht verifiziert

**Aktuell implementiert:**
```python
BUILDING_FOOTPRINT = {
    "small": 400,   # Wohnhaus, Bauernhof, etc.
    "medium": 600,  # Hochschule, Schmiede, etc.
    "large": 800,   # Hauptquartier, Dorfzentrum
}
```

**Problem:**
- Werte sind GESCHÄTZT, nicht aus Spieldateien
- Gebäude-Kollision nicht implementiert
- Unklar: Welche Tiles blockiert ein Gebäude?

**Zu extrahieren aus Spieldateien:**
- [ ] Exakte Gebäude-Größen (pro Gebäude-Typ)
- [ ] Blocking-Bereich pro Gebäude (welche Tiles werden blockiert?)
- [ ] Bau-Anforderungen (freie Fläche, Terrain-Typ)

---

### 11.3 BAUPLATZ-POSITIONEN (UNVOLLSTÄNDIG)

**Status:** ⚠️ Nur ~20 Beispiel-Positionen, nicht alle ~2200

**Aktuell vorhanden:**
```python
# map_config_wintersturm.py
BUILDING_ZONES_PLAYER_1 = {
    "zone_a_immediate": [
        # Nur die 20 nächsten freien Bauplätze!
        {"x": 40900, "y": 22900, "distance": 283},
        ...
    ],
    "summary": {
        "immediate_slots": 1962,  # Behauptet 1962, aber nur 20 gelistet!
        "after_logging_slots": 238,
    }
}
```

**Problem:**
- Summary sagt 1962 Positionen, aber nur ~20 sind gelistet
- Woher kommen die ~2200 Positionen für Multi-Step System?
- Bauplatz-Grid muss aus Spieldateien extrahiert werden

**Zu extrahieren aus Spieldateien:**
- [ ] Alle bebaubaren Positionen im Spieler 1 Quadrant
- [ ] Welche Positionen werden durch Bäume blockiert?
- [ ] Grid-Auflösung für Bauplätze (400x400? 100x100?)

---

### 11.4 BÄUME (POSITIONEN VORHANDEN)

**Status:** ✅ 909 Bäume mit exakten Positionen

**Aktuell vorhanden:**
```python
# player1_resources.json
{
    "trees_count": 909,
    "trees_all": [
        {"x": 42330.0, "y": 24030.0, "type": "XD_PineNorth3", "distance_to_hq": 1542.0},
        ...
    ]
}
```

**Zu prüfen:**
- [ ] Sind alle 909 Bäume korrekt? (mit Spiel vergleichen)
- [ ] Welchen Bereich blockiert ein Baum?
- [ ] Wachsen Bäume nach? (wahrscheinlich nicht in EMS)

---

### 11.5 GEBÄUDE-KOLLISION (NICHT IMPLEMENTIERT)

**Status:** ❌ Komplett fehlend

**Aktuell:**
- Keine Prüfung ob Gebäude sich überlappen
- Keine dynamische Blockierung nach Bau

**Benötigt:**
```python
def _is_position_free(self, x, y, building_type):
    """Prüft ob Position frei ist für Gebäude."""
    footprint = BUILDING_FOOTPRINTS[building_type]

    # Prüfe alle gebauten Gebäude
    for building, positions in self.building_positions.items():
        for pos in positions:
            if self._overlaps(x, y, footprint, pos, BUILDING_FOOTPRINTS[building]):
                return False

    # Prüfe Bäume
    for tree in self.remaining_trees:
        if self._in_footprint(tree, x, y, footprint):
            return False

    return True
```

---

### 11.6 PFADFINDUNG (VEREINFACHT)

**Status:** ⚠️ Nur Luftlinien-Distanz

**Aktuell implementiert:**
```python
# Laufzeit = Distanz / Geschwindigkeit
walk_time = distance / SERF_SPEED  # Gerade Linie!
```

**Problem:**
- Keine Hindernisse berücksichtigt
- Keine A* Pfadfindung um Berge/Gebäude
- Worker "fliegen" durch Hindernisse

**Benötigt (nach echten Blocking-Daten):**
- [ ] A* Pfadfindung mit echter Blocking-Map
- [ ] Dynamische Pfade (um neue Gebäude herum)
- [ ] Verschiedene Geschwindigkeiten pro Terrain?

---

### 11.7 CHECKLISTE: ECHTE KARTENDATEN EXTRAHIEREN

**Benötigte Spieldateien:**

| Datei | Zu extrahieren | Status |
|-------|----------------|--------|
| `terrain.bin` / `blocking.bin` | Echte Begehbarkeits-Map | ⬜ Offen |
| `entities/Buildings/*/` | Gebäude-Größen, Footprints | ⬜ Offen |
| `mapdata.xml` | Alle Bauplatz-Positionen | ⬜ Teilweise |
| `logic.xml` | Grid-Auflösung, Bau-Regeln | ⬜ Offen |

**Fragen für Karten-Abgleich:**

1. **Begehbarkeit:**
   - [ ] Wo ist die echte Blocking-Map?
   - [ ] Welches Format? (Binary, XML?)
   - [ ] Wie groß ist ein Tile?

2. **Gebäude:**
   - [ ] Exakte Größe pro Gebäude-Typ?
   - [ ] Welche Tiles blockiert ein Gebäude?
   - [ ] Mindestabstand zwischen Gebäuden?

3. **Bauplätze:**
   - [ ] Wie werden Bauplätze im Spiel berechnet?
   - [ ] Grid-basiert oder frei platzierbar?
   - [ ] Welche Terrain-Typen sind bebaubar?

4. **Pfadfindung:**
   - [ ] Welchen Algorithmus nutzt das Spiel?
   - [ ] Verschiedene Geschwindigkeiten pro Terrain?
   - [ ] Maximale Pfadlänge?

---

## ÄNDERUNGSHISTORIE

| Datum | Änderung |
|-------|----------|
| 2026-01-26 | Dokument erstellt |
| 2026-01-26 | Multi-Step für alle Actions dokumentiert |
| 2026-01-26 | **"Abziehen" ENTFERNT** - in "Zuweisen" integriert (Ziel=Frei) |
| 2026-01-26 | **Dynamische Positionen** - nur aktuell verfügbare (Option C) |
| 2026-01-26 | **Vollständige Bereichs-Liste** für Leibeigene (26 feste + Baustellen) |
| 2026-01-26 | Masken-Logik für Quell/Ziel-Bereiche dokumentiert |
| 2026-01-26 | **POSITION korrigiert**: ~2200 alle Positionen (keine Begrenzung!) |
| 2026-01-26 | Feste Index-Zuordnung für Positionen dokumentiert |
| 2026-01-27 | **NEU: Abschnitt 10** - Fehlende/Vereinfachte Effekte dokumentiert |
| 2026-01-27 | Kapelle fehlt komplett, Segen ignoriert worker_types |
| 2026-01-27 | Forschungs-Queues vereinfacht (nur global), Faith-Produktion vereinfacht |
| 2026-01-27 | **Checkliste für Original-Abgleich** mit Spieldateien hinzugefügt |
| 2026-01-27 | **NEU: Abschnitt 11** - Kartendaten müssen mit echten Spieldaten abgeglichen werden |
| 2026-01-27 | Begehbarkeits-Grid ist NICHT echt (nur Terrain-Höhe approximiert) |
| 2026-01-27 | Gebäude-Größen nur geschätzt, Kollision nicht implementiert |
| 2026-01-27 | Bauplatz-Positionen unvollständig (~20 statt ~2200) |
| 2026-01-27 | Pfadfindung nur Luftlinie, keine A* mit Hindernissen |
| 2026-01-27 | **Abschnitt 9 erweitert** - Offene Fragen für Benutzer-Entscheidungen |
| 2026-01-27 | Camp-System muss mit Original abgeglichen werden |
| 2026-01-27 | Worker-Verhalten, Produktions-Ketten, Soldaten-Rekrutierung als offene Fragen |
| 2026-01-27 | **Multi-Step ENTSCHIEDEN**: Erweiterte Obs, Reward nur am Ende, Flow zu Ende führen |
| 2026-01-27 | **Leibeigene ENTSCHIEDEN**: Kein Sterben, kein Essen/Motivation, DZ-Kapazität limitiert |
| 2026-01-27 | **NEU: Abschnitt 9.5** - Worker-Spawn/Despawn muss mit Original abgeglichen werden |
| 2026-01-27 | Fragen: Woher kommen Worker? Welches DZ? Laufweg simulieren? Despawn bei Abriss? |
| 2026-01-27 | **NEU: Abschnitt 10.6** - Technologie-Effekte definiert aber NIRGENDS angewendet! |
| 2026-01-27 | 18 verschiedene Effekt-Typen, keiner wird beim Forschungs-Abschluss aktiviert |
| 2026-01-27 | game_data.json hat leere Effekte - environment.py Werte sind manuell geschätzt |
| 2026-01-27 | Relevante Effekte für AI: build_speed, worker_speed, training_speed, payday |
