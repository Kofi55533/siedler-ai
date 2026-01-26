# GEPLANTE ÄNDERUNGEN - Siedler AI

> **Erstellt:** 2026-01-26
> **Status:** In Diskussion - NOCH NICHT IMPLEMENTIERT
> **Letzte Aktualisierung:** 2026-01-26

---

## ÜBERSICHT

Dieses Dokument sammelt alle besprochenen Änderungen bevor sie implementiert werden.

| # | Änderung | Priorität | Status |
|---|----------|-----------|--------|
| 1 | Two-Step Bauplatz-System | Hoch | Besprochen |
| 2 | Lager-System für Refiner | Mittel | Offen |
| 3 | Dynamische Bauplätze | Hoch | Besprochen |

---

## 1. TWO-STEP BAUPLATZ-SYSTEM (Option 1: Autoregressive)

### Beschreibung
Der Agent entscheidet in **zwei Schritten** wo ein Gebäude gebaut wird:
- **Step 1:** WAS bauen? (aus 332 Actions)
- **Step 2:** WO bauen? (aus Top 30 Positionen)

### Warum diese Lösung?
- MultiDiscrete hat Probleme mit **abhängigen Masken** (Position hängt von Gebäude ab)
- Flat Action Space mit allen Kombinationen wäre zu groß (~61.600 Actions)
- Two-Step hält Action Space klein (332 + 30 = 362)

### Technische Details

#### Neue Attribute
```python
self.decision_phase = "action"  # oder "position"
self.pending_action = None
self.pending_building = None
self.pending_positions = []  # Gefilterte Positionen für Step 2

self.action_space_main = Discrete(332)
self.action_space_position = Discrete(30)  # Top 30 Positionen
```

#### Ablauf
```
Step 1 (phase="action"):
├─ Agent wählt Action aus 332
├─ Wenn Build-Action:
│   ├─ Speichere pending_building
│   ├─ Berechne valid_positions für dieses Gebäude
│   ├─ Wechsle zu phase="position"
│   └─ Return obs (kein Reward, keine Zeit-Advancement)
└─ Wenn andere Action:
    └─ Führe aus, advance time, return reward

Step 2 (phase="position"):
├─ Agent wählt Position aus Top 30
├─ Baue Gebäude an gewählter Position
├─ Wechsle zurück zu phase="action"
└─ Return obs, reward, advance time
```

#### Maske in Step 1 (WICHTIG!)
Die Maske in Step 1 muss **vorausschauend prüfen** ob mindestens 1 Position existiert:
```python
def _mask_phase_action(self):
    mask = np.zeros(332, dtype=bool)
    mask[0] = True  # Wait immer erlaubt

    for action_idx, building in enumerate(build_actions):
        if not self._can_afford(building):
            continue
        if not self._has_requirements(building):
            continue

        # NEU: Positions-Check!
        valid_positions = self._get_valid_positions_for(building)
        if len(valid_positions) == 0:
            continue  # Blockiert!

        mask[action_idx] = True

    return mask
```

#### Positions-Sortierung nach Gebäude-Typ
```python
def _get_valid_positions_for(self, building):
    # Minen: Nur an Schächten
    # Dorfzentrum: Nur an speziellen Slots
    # Wohnhaus/Bauernhof: Sortiert nach Nähe zu HQ
    # Schmiede: Sortiert nach Nähe zu Eisenmine
    # Alchimistenhütte: Sortiert nach Nähe zu Schwefelmine
    # etc.
```

### Offene Fragen
- [ ] Soll der Agent auch **Minen-Schacht** auswählen können (wenn mehrere frei)?
- [ ] Wie viele Positionen zeigen? (30? 50? dynamisch?)
- [ ] Soll Observation die Positions-Features enthalten?

---

## 2. LAGER-SYSTEM FÜR REFINER

### Beschreibung
Aktuell holen Refiner (Schmiede, Steinmetz, etc.) ihre Rohstoffe immer vom **HQ**.
Im echten Spiel gibt es **Lagerhäuser** die strategisch platziert werden können.

### Aktuelle Implementierung (Vereinfacht)
```python
# environment.py:3327-3332
refiner = Refiner(
    ...
    supplier_position=hq_pos,  # Immer HQ!
    ...
)
```

### Mögliche Änderung
```python
# Refiner holt vom nächsten Lager ODER HQ
def _get_supplier_for_refiner(self, refiner_pos, resource_type):
    candidates = [self.hq_position]

    for storehouse in self.storehouses:
        if storehouse.has_resource(resource_type):
            candidates.append(storehouse.position)

    # Nächstes zurückgeben
    return min(candidates, key=lambda p: distance(refiner_pos, p))
```

### Offene Fragen
- [ ] Soll Lager als baubares Gebäude hinzugefügt werden?
- [ ] Wie funktioniert Ressourcen-Verteilung zwischen Lagern?
- [ ] Lohnt sich die Komplexität für das Training?

### Status
**OFFEN** - Noch nicht detailliert besprochen

---

## 3. DYNAMISCHE BAUPLÄTZE

### Beschreibung
Bauplätze ändern sich dynamisch:
- Bäume fällen → neue Positionen werden frei
- Gebäude abreißen → Position wird wieder frei
- Gebäude bauen → Nachbar-Positionen evtl. blockiert

### Aktuelle Daten
```
Zone A (sofort bebaubar):     ~20 vordefinierte Positionen
Zone B (nach Holzfällen):     ~10 Positionen mit trees_to_remove
Laut Summary:
  - immediate_slots:          1962
  - after_logging_slots:      238
  - blocked_permanent:        290
  - trees_in_area:            538
```

### Benötigte Tracking-Logik
```python
# Beim Baum fällen
def _on_tree_removed(self, tree_position):
    # Prüfe ob neue Bauplätze frei werden
    for zone_b_pos in self.zone_b_positions:
        if zone_b_pos["blocking_tree"] == tree_position:
            zone_b_pos["trees_to_remove"] -= 1
            if zone_b_pos["trees_to_remove"] == 0:
                self.available_positions.append(zone_b_pos)

# Beim Gebäude abreißen
def _on_building_demolished(self, building, position):
    self.available_positions.append(position)

# Beim Gebäude bauen
def _on_building_placed(self, building, position):
    self.available_positions.remove(position)
    self.used_positions.append(position)
```

### Offene Fragen
- [ ] Wie genau sind die Zone B Positionen mit Bäumen verknüpft?
- [ ] Blockieren Gebäude Nachbar-Positionen?
- [ ] Wie groß ist ein Gebäude-Footprint?

---

## 4. WEITERE BESPROCHENE THEMEN

### 4.1 Worker-Laufwege (Bereits implementiert)
- Leibeigene (Serfs): Laufen zur Ressource, kein WorkTime
- Worker: Laufen zu Farm → Wohnhaus → Arbeit (WorkTime-System)
- Camp: Vereinfacht am Arbeitsplatz (nur +10% Regeneration)

### 4.2 Refiner-Transportwege (Bereits implementiert)
- Steinmetz läuft zur Mine und zurück
- Laufzeit = (Distanz × 2) / Speed
- Je weiter die Mine, desto langsamer die Produktion

---

## NÄCHSTE SCHRITTE

1. [ ] Weitere Änderungen besprechen und hier dokumentieren
2. [ ] Prioritäten festlegen
3. [ ] Abhängigkeiten klären (was muss zuerst implementiert werden?)
4. [ ] Implementierung starten

---

## ÄNDERUNGSHISTORIE

| Datum | Änderung |
|-------|----------|
| 2026-01-26 | Dokument erstellt |
| 2026-01-26 | Two-Step System dokumentiert |
| 2026-01-26 | Lager-System als offen markiert |
| 2026-01-26 | Dynamische Bauplätze dokumentiert |

