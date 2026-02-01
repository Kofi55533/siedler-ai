# Siedler 5 - Werte-Vergleich: Aktuell vs. Original

**Datum**: 2026-01-28
**Quelle**: Extrahiert aus Siedler 5 Spieldateien (C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games\theSettlers5)
**Vergleich**: environment.py (aktuelle Werte) vs. extracted_values.json (Original)

---

## Executive Summary

**KRITISCHE ABWEICHUNGEN GEFUNDEN!**

Die aktuell in environment.py verwendeten Werte weichen **massiv** von den Original-Spieldateien ab.
Besonders betroffen: **Scharfschützen-Produktionspfad** (Hauptziel des Trainings!)

### Top 3 Abweichungen:

1. **Scharfschütze Level 1**: Kosten sind **80% niedriger** als im Original!
   - AKTUELL: 50 Gold + 40 Schwefel
   - ORIGINAL: 250 Gold + 70 Schwefel
   - DIFFERENZ: **+200 Gold, +30 Schwefel** fehlen!

2. **Hochschule Level 1**: Völlig falsche Ressourcen + 33% längere Bauzeit
   - AKTUELL: 300 Holz + 400 Stein, 120s
   - ORIGINAL: 200 Holz + 300 Lehm, 90s
   - DIFFERENZ: Stein statt Lehm (falscher Ressourcen-Typ!)

3. **Büchsenmacherei Level 1**: Extra 15 Gold (nicht im Original)
   - AKTUELL: 400 Stein + 300 Schwefel + **15 Gold**
   - ORIGINAL: 400 Stein + 300 Schwefel
   - DIFFERENZ: +15 Gold (fehlt im Original-XML)

---

## SCHARFSCHÜTZEN-PFAD (Höchste Priorität)

### 1. Scharfschütze Level 1 (PU_LeaderRifle1)

| Wert | AKTUELL (environment.py) | ORIGINAL (XML) | Abweichung |
|------|--------------------------|----------------|------------|
| **Rekrutierungs-Kosten** |
| Gold | 50 | **250** | **-80%** ❌ |
| Schwefel | 40 | **70** | **-43%** ❌ |
| **Trainingszeit** | 20s | ~20s (Archery) | ✓ |
| **Stats** |
| MaxHealth | ? | 150 | ? |
| Armor | ? | 1 | ? |
| Damage | ? | 16 | ? |
| MaxRange | ? | 2800 | ? |
| Speed | ? | 320 | ? |

**PROBLEM**: Der Agent lernt mit **völlig falschen Kosten**!
- Im Training: 50 Gold reichen für Scharfschützen
- Im echten Spiel: 250 Gold nötig → **5x teurer**!

### 2. Scharfschütze Level 2 (PU_LeaderRifle2)

| Wert | AKTUELL | ORIGINAL (XML) | Abweichung |
|------|---------|----------------|------------|
| **Rekrutierungs-Kosten** |
| Gold | ? | **300** | ? |
| Schwefel | ? | **80** | ? |
| **Stats** |
| MaxHealth | ? | 150 | ? |
| Armor | ? | 2 | ? |
| Damage | ? | 19 | ? |
| MaxRange | ? | 3000 | ? |

### 3. Büchsenmacherei Level 1 (PB_GunsmithWorkshop1)

| Wert | AKTUELL | ORIGINAL (XML) | Abweichung |
|------|---------|----------------|------------|
| **Baukosten** |
| Stein | 400 | 400 | ✓ |
| Schwefel | 300 | 300 | ✓ |
| Gold | **15** | **0** | +15 ❌ |
| **Bauzeit** | 110s | 110s | ✓ |
| **Max Workers** | ? | 2 | ? |
| **Max Health** | ? | 1200 | ? |

**HINWEIS**: Büchsenmacherei produziert KEINE Scharfschützen!
→ Hat `ResourceRefinerBehavior` für Schwefel (verfeinert Schwefel, nicht Soldaten)

### 4. Büchsenmacherei Level 2 (PB_GunsmithWorkshop2)

| Wert | AKTUELL | ORIGINAL (XML) | Abweichung |
|------|---------|----------------|------------|
| **Upgrade-Kosten** | ? | 300 Stein + 200 Schwefel | ? |
| **Upgrade-Zeit** | ? | 40s | ? |
| **Max Workers** | ? | 4 | ? |
| **Max Health** | ? | 1700 | ? |

### 5. Hochschule Level 1 (PB_University1)

| Wert | AKTUELL | ORIGINAL (XML) | Abweichung |
|------|---------|----------------|------------|
| **Baukosten** |
| Holz | 300 | **200** | +50% ❌ |
| Stein | **400** | **0** | Falsche Ressource! ❌ |
| Lehm | **0** | **300** | Fehlt! ❌ |
| **Bauzeit** | 120s | **90s** | +33% ❌ |
| **Max Workers** | ? | 6 | ? |
| **Max Health** | ? | 2000 | ? |

**PROBLEM**: Völlig falsche Ressourcen!
- AKTUELL: Holz + **Stein** (wie eine Mine)
- ORIGINAL: Holz + **Lehm** (wie ein normales Gebäude)

### 6. Hochschule Level 2 (PB_University2)

| Wert | AKTUELL | ORIGINAL (XML) | Abweichung |
|------|---------|----------------|------------|
| **Upgrade-Kosten** | ? | 100 Stein + 100 Lehm + 150 Gold | ? |
| **Upgrade-Zeit** | ? | 50s | ? |
| **Max Workers** | ? | 8 | ? |
| **Max Health** | ? | 3500 | ? |

---

## TECHNOLOGIEN (Scharfschützen-Pfad)

**PROBLEM**: Technologie-XMLs enthalten **KEINE Effekte**!
→ Effekte sind wahrscheinlich im Code hardcodiert (nicht in XMLs)

### Mathematik (GT_Mathematics?)

| Wert | AKTUELL | ORIGINAL (XML) | Abweichung |
|------|---------|----------------|------------|
| Forschungs-Kosten | 100 Gold + 200 Holz? | **???** | ❓ |
| Forschungszeit | 20s? | **???** | ❓ |
| **Effekte** | ? | **NICHT IN XMLs** | ❌ |

**HINWEIS**: Technologie-Dateien fehlen in extracted_values.json!
→ Muss manuell gesucht werden (GT_* in Technologies-Ordner)

### Fernglas (GT_Binoculars?)

| Wert | AKTUELL | ORIGINAL (XML) | Abweichung |
|------|---------|----------------|------------|
| Forschungs-Kosten | 300 Gold + 300 Eisen? | **???** | ❓ |
| Forschungszeit | 30s? | **???** | ❓ |
| Voraussetzung | HQ Level 2? | **???** | ❓ |

### Luntenschloss (GT_Flintlock?)

| Wert | AKTUELL | ORIGINAL (XML) | Abweichung |
|------|---------|----------------|------------|
| Forschungs-Kosten | 300 Eisen + 300 Schwefel? | **???** | ❓ |
| Forschungszeit | 50s? | **???** | ❓ |

---

## WEITERE GEBÄUDE (Top 20 Abweichungen)

### Hauptquartier (Headquarters)

**Extrahiert**: 94 Gebäude total
**TODO**: Systematischer Vergleich aller 94 Gebäude

### Eisenmine, Schwefelmine, etc.

**TODO**: Mine-Werte validieren (AmountToMine, MaxWorkers)

---

## LOGIC-PARAMETER (Zahltag, Steuern, Motivation)

### Steuern (Tax Levels)

| Level | Steuer/Worker | Motivation-Änderung |
|-------|---------------|---------------------|
| 0 (Very Low) | 0 Gold | +0.20 |
| 1 (Low) | 5 Gold | +0.08 |
| 2 (Normal) | **10 Gold** | 0.00 |
| 3 (High) | 15 Gold | -0.08 |
| 4 (Very High) | 20 Gold | -0.12 |

**Start-Level**: 2 (Normal)

### Zahltag

| Parameter | Wert |
|-----------|------|
| TaxAmount | 5 Gold pro Worker |
| Initial Tax Level | 2 (Normal) |

### Motivation

| Threshold | Wert | Bedeutung |
|-----------|------|-----------|
| Happy | 1.5 | Sehr glücklich / ekstatisch |
| Sad | 1.0 | Traurig |
| Angry | 0.7 | Wütend |
| **Leave** | **0.25** | Worker VERLÄSST Settlement! |
| Absolute Max | 3.0 | Maximum |
| Game Start Max | 1.0 | Initial |

### WorkTime

| Parameter | Wert |
|-----------|------|
| WorkTimeBase | 125 |
| WorkTimeThresholdWork | 25 |

---

## EMPFEHLUNGEN

### 🔴 KRITISCH - Sofort fixen:

1. **Scharfschütze Level 1 Kosten korrigieren**:
   - Von: 50 Gold + 40 Schwefel
   - Zu: **250 Gold + 70 Schwefel**
   - Auswirkung: **5x teurer** → Training muss Ressourcen-Management lernen!

2. **Hochschule Level 1 Ressourcen korrigieren**:
   - Von: 300 Holz + 400 Stein, 120s
   - Zu: **200 Holz + 300 Lehm, 90s**
   - Auswirkung: Stein ist knapp → falsche Ressource führt zu falscher Strategie!

### 🟡 WICHTIG - Bald fixen:

3. **Büchsenmacherei Gold-Kosten entfernen**:
   - Von: 400 Stein + 300 Schwefel + 15 Gold
   - Zu: **400 Stein + 300 Schwefel**

4. **Alle 94 Gebäude systematisch validieren**:
   - Nutze extracted_values.json
   - Erstelle automatisches Patch-Script

5. **Technologie-Effekte recherchieren**:
   - XMLs enthalten KEINE Effekte
   - Vermutlich in Modifier.xml oder Code hardcodiert
   - Muss manuell aus Spiel extrahiert werden (oder via Gameplay-Tests)

### 🟢 Optional - Nice to have:

6. **Scharfschütze Stats validieren** (MaxHealth, Armor, Damage, Range)
7. **Alle 12 Soldaten-Typen validieren**
8. **WorkTime/Motivation-System an Original anpassen**

---

## VERIFIZIERUNG

### ✅ Erfolgreich extrahiert:

- 94 Gebäude (base + extra1 + extra2)
- 12 Militär-Einheiten
- 204 Technologien (nur Kosten/Zeiten, KEINE Effekte)
- 11 Worker-Typen
- 6 Helden
- 4 Kanonen
- Logic-Parameter (Steuern, Motivation, WorkTime)

### ❌ Noch fehlend:

- **Technologie-Effekte** (nicht in XMLs!)
- Trainingszeiten für Soldaten (vermutlich in Barracks/Archery-Behavior)
- Produktions-Raten (AmountToMine, TransportAmount - teilweise in extracted_values)
- Zahltag-Intervall (wann startet erster Zahltag?)
- Militär-Unterhalt (kosten Soldaten Sold?)

---

## FAZIT

**Die aktuellen Werte in environment.py sind NICHT korrekt!**

Besonders kritisch für das Trainingsziel (Scharfschützen-Produktion):
- **Scharfschütze 5x zu billig** → Agent lernt unrealistische Strategie
- **Hochschule falsche Ressourcen** → Agent optimiert falsche Ressourcen-Kette
- **Effekte fehlen** → Technologien haben keinen Nutzen!

**Empfehlung**:
1. PHASE 2.1 durchführen (Scharfschützen-Pfad validieren)
2. environment.py mit extracted_values.json patchen
3. Training neu starten mit korrekten Werten

---

**Generiert von**: data_extractor.py + manueller Analyse
**Original-Daten**: config/extracted_values.json (140.2 KB)
**Nächste Schritte**: Siehe PHASE 2.1 in playful-wibbling-eclipse.md
