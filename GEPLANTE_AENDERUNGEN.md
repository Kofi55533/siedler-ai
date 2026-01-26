# GEPLANTE ÄNDERUNGEN - Siedler AI

> **Erstellt:** 2026-01-26
> **Status:** In Diskussion - NOCH NICHT IMPLEMENTIERT
> **Letzte Aktualisierung:** 2026-01-26

---

## ÜBERSICHT

Dieses Dokument sammelt alle besprochenen Änderungen bevor sie implementiert werden.

| # | Änderung | Priorität | Status |
|---|----------|-----------|--------|
| 1 | Multi-Step Action System | Hoch | Besprochen |
| 2 | Lager-System für Refiner | Mittel | Offen (später prüfen) |
| 3 | Dynamische Bauplätze | Hoch | Besprochen |
| 4 | Alle Arbeiter-Laufwege simulieren | Hoch | Besprochen |

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

### ALLE ACTION-TYPEN MIT MULTI-STEP FLOWS

#### Übersicht aller Flows

| Action-Typ | Step 1 | Step 2 | Step 3 | Step 4 |
|------------|--------|--------|--------|--------|
| Wait | "Wait" | - | - | - |
| Bauen | "Bauen" | Gebäude? | Position? | - |
| Upgrade | "Upgrade" | Gebäude? | Position?* | - |
| Forschen | "Forschen" | Technologie? | - | - |
| Rekrutieren | "Rekrutieren" | Soldaten-Typ? | Anzahl? | - |
| Leibeigene kaufen | "Serf kaufen" | Anzahl? | - | - |
| Leibeigene entlassen | "Serf entlassen" | Von wo?* | Anzahl? | - |
| Leibeigene zuweisen | "Zuweisen" | Von wo? | Anzahl? | Wohin? |
| Leibeigene abziehen | "Abziehen" | Von wo? | Anzahl? | - |
| Abreißen | "Abreißen" | Gebäude? | Position?* | - |
| Segnen | "Segnen" | Kategorie? | - | - |
| Steuern | "Steuern" | Stufe? | - | - |
| Alarm | "Alarm" | AN/AUS? | - | - |

*Position nur wenn mehrere Gebäude des gleichen Typs existieren

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
        Optionen: [Wohnhaus_1, Bauernhof_1, Hochschule_1, ...]
        Maske: Nur Gebäude die man sich leisten kann UND für die Position existiert
    ↓
Step 3: Wo bauen?
        Optionen: Top 30 Positionen, sortiert nach Nutzen für dieses Gebäude
        Maske: Nur verfügbare Positionen
    ↓
[ausführen, Zeit vorrücken]
```

**Spezialfälle:**
- **Minen**: Step 3 zeigt nur freie Schacht-Positionen
- **Dorfzentrum**: Step 3 zeigt nur Dorfzentrum-Slots

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

**Beispiel:**
- Nur 1 Wohnhaus_1 gebaut → Step 3 wird übersprungen
- 3 Wohnhaus_1 gebaut → Agent wählt welches upgraded wird

---

#### 4. FORSCHEN (2 Steps)
```
Step 1: "Forschen"
    ↓
Step 2: Welche Technologie?
        Optionen: [Mathematik, Fernglas, Luntenschloss, ...]
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
        Optionen: [Schwertkämpfer, Bogenschütze, Scharfschütze_1, Scharfschütze_2, ...]
        Maske: Nur Typen die rekrutierbar (Gebäude + Tech + Ressourcen)
    ↓
Step 3: Wie viele?
        Optionen: [1, 2, 3, 4, 5, 10, ...] oder dynamisch basierend auf Ressourcen
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

#### 7. LEIBEIGENE ENTLASSEN (2-3 Steps)
```
Step 1: "Leibeigene entlassen"
    ↓
Step 2: Von wo entlassen? (optional - für volle Kontrolle)
        Optionen: [Frei/Idle, Holz-Zone-1, Eisenmine, Baustelle-3, ...]
        Maske: Nur Positionen wo Leibeigene sind
    ↓
Step 3: Wie viele?
        Optionen: [1, 2, 3, 5, alle]
        Maske: Nur Anzahlen die an dieser Position verfügbar sind
    ↓
[ausführen, Zeit vorrücken]
```

---

#### 8. LEIBEIGENE ZUWEISEN (4 Steps) - VOLLE KONTROLLE
```
Step 1: "Leibeigene zuweisen"
    ↓
Step 2: Von wo nehmen?
        Optionen: [Frei/Idle, Holz-Zone-1, Holz-Zone-2, Eisenmine, Baustelle-3, ...]
        Maske: Nur Positionen wo Leibeigene sind (inkl. "Frei")
    ↓
Step 3: Wie viele?
        Optionen: [1, 2, 3, 5, 10, alle]
        Maske: Nur Anzahlen die an Quell-Position verfügbar sind
    ↓
Step 4: Wohin schicken?
        Optionen: Alle Ziel-Positionen
          - Holz-Zonen: [HQ-Bereich, Schwefelmine-Zone, Lehmmine-Zone, ...]
          - Stollen: [Eisen-Stollen-1, Stein-Stollen-1, ...]
          - Vorkommen: [Eisen-Vorkommen-1, ...] (nur wenn keine Mine dort!)
          - Baustellen: [Baustelle-1, Baustelle-2, ...]
          - "Frei" (zurückrufen zu Idle)
        Maske: Nur gültige Ziele (nicht voll, nicht blockiert)
    ↓
[ausführen, Zeit vorrücken]
```

**Quell-Positionen (Step 2):**
- "Frei" = Idle Leibeigene beim HQ
- Holz-Zonen (6 Stück)
- Stollen (Eisen, Stein, Lehm, Schwefel × je 3)
- Vorkommen (kleine Deposits)
- Baustellen (aktive Bauprojekte)

**Ziel-Positionen (Step 4):**
- Gleiche Kategorien wie Quell-Positionen
- Plus spezielle Option "Frei" um Leibeigene zurückzurufen

---

#### 9. LEIBEIGENE ABZIEHEN (3 Steps)
```
Step 1: "Leibeigene abziehen"
    ↓
Step 2: Von wo abziehen?
        Optionen: [Holz-Zone-1, Eisenmine, Baustelle-3, ...]
        Maske: Nur Positionen wo Leibeigene arbeiten
    ↓
Step 3: Wie viele?
        Optionen: [1, 2, 3, 5, alle]
        Maske: Nur Anzahlen die dort arbeiten
    ↓
[ausführen, Leibeigene werden "Frei", Zeit vorrücken]
```

*Hinweis: "Abziehen" ist wie "Zuweisen" mit Ziel="Frei", könnte zusammengeführt werden*

---

#### 10. ABREISSEN (2-3 Steps)
```
Step 1: "Abreißen"
    ↓
Step 2: Welches Gebäude?
        Optionen: [Wohnhaus_1, Bauernhof_1, ...]
        Maske: Nur Gebäude die existieren
    ↓
Step 3: Welche Position? (NUR wenn mehrere vom gleichen Typ!)
        Optionen: Positionen dieses Gebäude-Typs
        Maske: Alle Positionen mit diesem Gebäude
    ↓
[ausführen, Position wird frei, 50% Ressourcen zurück, Zeit vorrücken]
```

---

#### 11. SEGNEN (2 Steps)
```
Step 1: "Segnen"
    ↓
Step 2: Welche Kategorie?
        Optionen: [Konstruktion, Forschung, Waffen, Finanzen, Kanonisierung]
        Maske: Nur wenn Kloster gebaut UND genug Faith UND nicht auf Cooldown
    ↓
[ausführen, Zeit vorrücken]
```

**Kategorien (aus extra2):**
| ID | Name | Betroffene Worker |
|----|------|-------------------|
| 1 | Konstruktion | Miner, Farmer, BrickMaker, Sawmillworker, Stonecutter |
| 2 | Forschung | Scholar, Priest, Engineer, MasterBuilder |
| 3 | Waffen | Smith, Alchemist, Smelter, Gunsmith |
| 4 | Finanzen | Trader, Treasurer |
| 5 | Kanonisierung | ALLE Worker |

---

#### 12. STEUERN (2 Steps)
```
Step 1: "Steuern"
    ↓
Step 2: Welche Stufe?
        Optionen: [0-Sehr niedrig, 1-Niedrig, 2-Normal, 3-Hoch, 4-Sehr hoch]
        Maske: Alle immer erlaubt
    ↓
[ausführen, Zeit vorrücken]
```

**Steuerstufen:**
| Stufe | Steuer | Motivation |
|-------|--------|------------|
| 0 | 0 | +0.20 |
| 1 | 5 | +0.08 |
| 2 | 10 | 0 (Start) |
| 3 | 15 | -0.08 |
| 4 | 20 | -0.12 |

---

#### 13. ALARM (2 Steps)
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

### ZUSAMMENFASSUNG ACTION SPACES

| Phase | Discrete Space Größe | Beschreibung |
|-------|---------------------|--------------|
| MAIN | ~15 | Haupt-Action-Kategorien |
| BUILDING | ~28 | Gebäude-Typen |
| POSITION | ~30-50 | Top Positionen |
| TECH | ~50 | Technologien |
| SOLDIER | ~22 | Soldaten-Typen |
| QUANTITY | ~10 | Anzahl (1,2,3,5,10,alle) |
| SOURCE | ~20 | Quell-Positionen für Leibeigene |
| TARGET | ~30 | Ziel-Positionen für Leibeigene |
| CATEGORY | 5 | Segen-Kategorien |
| TAX_LEVEL | 5 | Steuerstufen |
| ON_OFF | 2 | AN/AUS |

**Maximale Step-Tiefe:** 4 (bei Leibeigene zuweisen)

---

### TECHNISCHE IMPLEMENTIERUNG

#### Phase-Tracking
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

class SiedlerEnvMultiStep(gym.Env):
    def __init__(self):
        self.current_phase = ActionPhase.MAIN
        self.pending_main_action = None
        self.pending_building = None
        self.pending_source = None
        self.pending_quantity = None
        # ... weitere pending states

        # Action Spaces für jede Phase
        self.action_spaces = {
            ActionPhase.MAIN: Discrete(15),
            ActionPhase.BUILDING: Discrete(28),
            ActionPhase.POSITION: Discrete(50),
            ActionPhase.TECH: Discrete(50),
            ActionPhase.SOLDIER: Discrete(22),
            ActionPhase.QUANTITY: Discrete(10),
            ActionPhase.SOURCE: Discrete(20),
            ActionPhase.TARGET: Discrete(30),
            ActionPhase.CATEGORY: Discrete(5),
            ActionPhase.TAX_LEVEL: Discrete(5),
            ActionPhase.ON_OFF: Discrete(2),
        }

    @property
    def action_space(self):
        return self.action_spaces[self.current_phase]
```

#### Flow-Definitionen
```python
ACTION_FLOWS = {
    "wait": [ActionPhase.MAIN],
    "build": [ActionPhase.MAIN, ActionPhase.BUILDING, ActionPhase.POSITION],
    "upgrade": [ActionPhase.MAIN, ActionPhase.BUILDING, ActionPhase.POSITION],  # Position optional
    "research": [ActionPhase.MAIN, ActionPhase.TECH],
    "recruit": [ActionPhase.MAIN, ActionPhase.SOLDIER, ActionPhase.QUANTITY],
    "buy_serf": [ActionPhase.MAIN, ActionPhase.QUANTITY],
    "dismiss_serf": [ActionPhase.MAIN, ActionPhase.SOURCE, ActionPhase.QUANTITY],
    "assign_serf": [ActionPhase.MAIN, ActionPhase.SOURCE, ActionPhase.QUANTITY, ActionPhase.TARGET],
    "recall_serf": [ActionPhase.MAIN, ActionPhase.SOURCE, ActionPhase.QUANTITY],
    "demolish": [ActionPhase.MAIN, ActionPhase.BUILDING, ActionPhase.POSITION],  # Position optional
    "bless": [ActionPhase.MAIN, ActionPhase.CATEGORY],
    "tax": [ActionPhase.MAIN, ActionPhase.TAX_LEVEL],
    "alarm": [ActionPhase.MAIN, ActionPhase.ON_OFF],
}
```

#### Masken-Berechnung
```python
def action_masks(self):
    if self.current_phase == ActionPhase.MAIN:
        return self._mask_main()
    elif self.current_phase == ActionPhase.BUILDING:
        return self._mask_building()
    elif self.current_phase == ActionPhase.POSITION:
        return self._mask_position()
    # ... etc

def _mask_main(self):
    """Maske für Haupt-Actions - prüft ob Folge-Steps möglich sind."""
    mask = np.zeros(15, dtype=bool)

    mask[0] = True  # Wait immer erlaubt

    # Bauen: Gibt es Gebäude die baubar sind UND Positionen haben?
    if self._has_any_buildable_with_position():
        mask[1] = True

    # Upgrade: Gibt es Gebäude die upgradebar sind?
    if self._has_any_upgradeable():
        mask[2] = True

    # Forschen: Gibt es Techs die erforschbar sind?
    if self._has_any_researchable():
        mask[3] = True

    # Rekrutieren: Gibt es Soldaten die rekrutierbar sind?
    if self._has_any_recruitable():
        mask[4] = True

    # Leibeigene kaufen: Genug Taler?
    if self.resources["Taler"] >= SERF_COST:
        mask[5] = True

    # Leibeigene entlassen: Gibt es Leibeigene?
    if self.total_leibeigene > 0:
        mask[6] = True

    # Leibeigene zuweisen: Gibt es Leibeigene UND Ziele?
    if self._has_serfs_to_assign() and self._has_assignment_targets():
        mask[7] = True

    # Leibeigene abziehen: Gibt es arbeitende Leibeigene?
    if self._has_working_serfs():
        mask[8] = True

    # Abreißen: Gibt es Gebäude?
    if self._has_any_building():
        mask[9] = True

    # Segnen: Kloster gebaut + Faith + kein Cooldown?
    if self._can_bless():
        mask[10] = True

    # Steuern: Immer erlaubt
    mask[11] = True

    # Alarm: Cooldown prüfen
    if self._can_toggle_alarm():
        mask[12] = True

    return mask
```

---

## 2. LAGER-SYSTEM FÜR REFINER

### Status
**OFFEN** - Muss mit echten Spieldateien überprüft werden

### Vermutete Mechanik (zu verifizieren)
Arbeiter holen Ressourcen von:
1. **Gebaute Minen** (wenn Mine auf Schacht gebaut UND Worker dort arbeiten)
2. **Lager** (wenn vorhanden und Ressourcen dort gelagert)
3. **HQ** (Fallback)

### Zu prüfen
- [ ] Wie funktioniert Ressourcen-Fluss im echten Spiel?
- [ ] Gibt es Lager-Gebäude?
- [ ] Woher holen Refiner ihre Input-Ressourcen?

---

## 3. DYNAMISCHE BAUPLÄTZE

### Beschreibung
Bauplätze ändern sich dynamisch:
- Bäume fällen → neue Positionen werden frei
- Gebäude abreißen → Position wird wieder frei
- Gebäude bauen → Position wird belegt

### Aktuelle Daten
```
Zone A (sofort bebaubar):     ~1962 Positionen
Zone B (nach Holzfällen):     ~238 Positionen
Permanent blockiert:          ~290 Positionen
Bäume im Gebiet:              ~538
```

### Benötigte Tracking-Logik
```python
# Beim Baum fällen
def _on_tree_removed(self, tree_position):
    # Prüfe ob neue Bauplätze frei werden
    for zone_b_pos in self.zone_b_positions:
        if tree_position in zone_b_pos["blocking_trees"]:
            zone_b_pos["blocking_trees"].remove(tree_position)
            if len(zone_b_pos["blocking_trees"]) == 0:
                self.available_positions.append(zone_b_pos)

# Beim Gebäude abreißen
def _on_building_demolished(self, building, position):
    self.available_positions.append(position)
    self.used_positions.remove(position)

# Beim Gebäude bauen
def _on_building_placed(self, building, position):
    self.available_positions.remove(position)
    self.used_positions.append(position)
```

---

## 4. ALLE ARBEITER-LAUFWEGE SIMULIEREN

### Beschreibung
Jeder Arbeiter (nicht nur Leibeigene) soll realistische Laufwege haben.

### Bereits implementiert
- **Leibeigene (Serfs)**: Laufen zur Ressource, kein WorkTime
- **Worker mit WorkTime**: Laufen zu Farm → Wohnhaus → Arbeit

### Zu erweitern
- **Refiner-Worker**: Laufen zur Ressourcen-Quelle (Mine/Lager/HQ) und zurück
- **Transporte**: Ressourcen-Transport zwischen Gebäuden

### Auswirkung auf Gameplay
- **Platzierung wichtig**: Schmiede nahe Eisenmine = schnellere Produktion
- **Lager strategisch**: Kann Laufwege verkürzen
- **Agent lernt**: Optimale Gebäude-Platzierung

---

## 5. OFFENE FRAGEN

### Multi-Step System
- [ ] Soll "Abziehen" mit "Zuweisen" zusammengeführt werden (Ziel="Frei")?
- [ ] Observation: Was sieht der Agent in jedem Step?
- [ ] Reward: Wann gibt es Reward (nur am Ende? Zwischen-Rewards?)?
- [ ] Reset: Was passiert bei Episode-Ende mitten im Flow?

### Positionen
- [ ] Wie viele Positionen maximal zeigen? (30? 50? dynamisch?)
- [ ] Positions-Features in Observation?
- [ ] Sortierung der Positionen (nach Distanz? Nutzen?)

### Leibeigene
- [ ] Maximale Anzahl Leibeigene?
- [ ] Kosten pro Leibeigener?
- [ ] Können Leibeigene sterben/verschwinden?

---

## NÄCHSTE SCHRITTE

1. [ ] Weitere Änderungen besprechen und hier dokumentieren
2. [ ] Lager-System mit echtem Spiel verifizieren
3. [ ] Prioritäten festlegen
4. [ ] Abhängigkeiten klären
5. [ ] Implementierung starten

---

## ÄNDERUNGSHISTORIE

| Datum | Änderung |
|-------|----------|
| 2026-01-26 | Dokument erstellt |
| 2026-01-26 | Two-Step System dokumentiert |
| 2026-01-26 | Lager-System als offen markiert |
| 2026-01-26 | Dynamische Bauplätze dokumentiert |
| 2026-01-26 | **GROSSES UPDATE**: Multi-Step für ALLE Actions dokumentiert |
| 2026-01-26 | Alle 13 Action-Typen mit Flows definiert |
| 2026-01-26 | Technische Implementierung skizziert |
| 2026-01-26 | Arbeiter-Laufwege als Anforderung hinzugefügt |
