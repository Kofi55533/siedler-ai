# Siedler 5 Logic Conformance Audit

Stand: 2026-06-11

## Kurzfazit

Die Umgebung ist weiterhin **nicht vollstaendig 1:1 bewiesen**, aber die wichtigsten belegten Wirtschafts- und Worker-Parameter sind jetzt konsistent gegen die Gold-Edition-Quelle ausgerichtet. Worker-/Serf-/Arbeitsplatz-TaskLists werden jetzt zusaetzlich vollstaendig direkt aus den Originaldateien extrahiert und fuer die Runtime bevorzugt.

Kanonische Quelle fuer diesen Stand: `C:\Users\marku\OneDrive\Desktop\Gold edition`. Die Ubisoft-Installation bleibt als Vergleichsquelle dokumentiert, wird aber nicht als Wahrheit fuer die laufende Simulation verwendet.

## Gepruefte Quellen

- `C:\Users\marku\OneDrive\Desktop\Gold edition`
- `C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games\theSettlers5`
- Projektkonfiguration:
  - `config/engine_decoded.json`
  - `config/game_data.json`
  - `config/full_worker_engine_behavior.json`
  - `config/worker_truth_model.json`
  - `config/worker_behavior_logic.json`

Frisch erzeugte Audit-Artefakte:

- `analysis/engine_decoded_gold_edition.json`
- `analysis/engine_decoded_ubisoft.json`
- `analysis/game_data_gold_edition.json`
- `analysis/game_data_ubisoft.json`
- `config/engine_branch_evidence.json/.md`
- `config/engine_instruction_cfg.json/.md`
- `config/worker_camp_path_branch_matrix.json/.md`
- `config/ghidra_worker_decompile_evidence.json/.md`
- `config/engine_conformance_certificate.json/.md`

## Dekodierte Originaldaten

`engine_decoder.py` gegen beide Installationen:

| Bereich | Gold edition | Ubisoft |
| --- | ---: | ---: |
| Workers | 18 | 18 |
| Buildings | 69 | 69 |
| Deposits | 9 | 9 |
| Mine tasklists | 8 | 8 |
| Serf tasklists | 8 | 8 |
| Worker path tasklists | 4 | 4 |
| Camp files | 24 CB + 6 Miner | 24 CB + 6 Miner |

`data_extractor.py` gegen beide Installationen:

| Bereich | Gold edition | Ubisoft |
| --- | ---: | ---: |
| Worker-Typen | 11 | 11 |
| Gebaeude | 94 | 94 |
| Technologien | 199 | 199 |
| Einheiten | 47 | 47 |
| Helden | 17 | 17 |
| Kanonen | 4 | 4 |
| Logic-Parameter | 4 | 4 |

`extract_full_worker_engine_behavior.py` gegen Gold edition:

| Bereich | Wert |
| --- | ---: |
| Effektive TaskLists | 361 |
| TaskList-Layer-Dateien | 1041 |
| Effektive Entity-XMLs | 855 |
| Entity-Layer-Dateien | 2255 |
| Worker-/Serf-Entities | 21 |
| Worker-/Pausen-/Arbeitsplatz-Gebaeude | 48 |
| Von Workern/Serfs erreichbare TaskLists | 231 |
| Nicht aufgeloeste Worker-TaskList-Refs | 0 |
| Unterschiedliche TaskTypes | 153 |

Statische Binary-Analyse gegen `C:\Users\marku\OneDrive\Desktop\Gold edition\bin\SettlersHoK.exe`:

| Artefakt | Wert |
| --- | ---: |
| ASCII/RTTI-Strings im Branch-Evidence-Pass | 34212 |
| Instruction-CFG-Funktionen | 153 |
| Instruction-CFG-Basic-Blocks | 591 |
| Instruction-CFG-Instructions | 8761 |
| Instruction-CFG-Conditional-Branches | 275 |
| Worker/Camp/Path selektierte Funktionen | 130 |
| Worker/Camp/Path Anchor-Funktionen | 52 |
| Worker/Camp/Path Conditional-Branches | 215 |
| Sim-Contract Branch-Anker | 32 |

Ghidra Headless gegen dasselbe Gold-Binary:

| Bereich | Wert |
| --- | ---: |
| Ghidra-Version | 11.2.1 PUBLIC |
| Java/JDK | portable Temurin 21 in `.tools/` |
| Branch-Matrix-Zielfunktionen | 130 |
| Von Ghidra einer Funktion zugeordnet | 105 |
| Eindeutige Ghidra-Funktionen gematcht | 104 |
| Erfolgreich dekompiliert | 104 |
| Voller dekompilierter C-Code gespeichert | Nein |
| Gespeicherte Nachweise | Signaturen, C-Output-SHA256, P-Code-Histogramme, String-Refs |

## Aktueller Status

### Behoben in diesem Durchlauf

1. Referenzkonflikt `PB_Tavern2`

   - Gold edition: `PB_Tavern2` hat `Worker=PU_Farmer`.
   - Ubisoft: `PB_Tavern2` hat `Worker=PU_TavernBarkeeper`.
   - Projektstand: `config/engine_decoded.json`, `config/game_data.json` und abgeleitete Worker-Truth-Dateien wurden aus Gold edition neu erzeugt.

   Ergebnis: Die Umgebung ist fuer diesen Stand konsistent auf Gold edition ausgerichtet.

2. Wetter/Schnee-Bewegung

   - `SnowMoveSpeedFactor=0.85` ist als Wetterfaktor modelliert.
   - Worker-, Serf- und Refiner-Laufzeiten verwenden jetzt denselben Speed-Multiplier.
   - Wintersturm nutzt den extrahierten Lua-Schedule fuer die ersten 40 Minuten: Sommer 15m, Regen 3m, Sommer 12m, Regen 2m, Sommer 8m.

3. Faith-Limit

   - `MaximumFaith` ist auf den Engine-Wert `5000` gesetzt.
   - Faith-Generierung durch Priester kappt jetzt bei `5000`, nicht mehr bei `RequiredFaith * 5`.

4. Engine-Diff

   - `python engine_vs_env_diff.py`: 0 kritische Punkte, 0 Warnungen.

5. Placement-/Gebaeude-Geometrie

   - `data_extractor.py` extrahiert jetzt `Blocked1/Blocked2`, `TerrainPos1/2`, `ApproachPos`, `DoorPos`, `LeavePos` und `BuilderSlot` aus den Original-XMLs.
   - `config/game_data.json` enthaelt diese Werte fuer die Gold Edition.
   - `original_game_values.py` stellt Footprints, `Blocked1/Blocked2` und `ApproachPos`/`DoorPos`/`LeavePos` als Sim-Namensmapping bereit.
   - `environment.py` und `pathfinding.py` laden Gebaeude-Footprints und asymmetrische `Blocked1/Blocked2`-AABBs zur Laufzeit aus `config/game_data.json`.
   - Worker-Pausenwege zu Bauernhof/Wohnhaus verwenden jetzt den originalen `ApproachPos` statt des Gebaeudemittelpunkts.
   - Korrigierte Original-Footprints umfassen u.a. Bank `900x800`, Kloster `1300x1500`, Taverne `900x1200`, Turm `200x200`, Architektenstube `900x800`, Wetterkraftwerk `500x500`, Wetterturm `400x400`, Beautification01 `100x100`.

6. Forschungs-XML-Werte

   - Belegte Originalwerte aus `config/game_data.json` werden zur Laufzeit auf `technologies` ueberlagert: Kosten, Forschungszeit, Tech-Voraussetzungen, Gebaeude-Voraussetzungen und `RequiredEntityConditions`.
   - Beispiel: `Wettermanipulation` nutzt jetzt den XML-Wert `40s` statt `50s`.
   - Alternative Gebaeude-Voraussetzungen werden korrekt uebernommen, z.B. `Fernglas` mit `Hauptquartier_2` **oder** `Hauptquartier_3`.

7. Vollstaendige Worker-/Serf-Engine-Extraktion

   - Neuer Extractor: `tools/archive/extract_full_worker_engine_behavior.py`.
   - Output: `config/full_worker_engine_behavior.json` und `config/full_worker_engine_behavior.md`.
   - Der Extractor liest direkt aus `C:\Users\marku\OneDrive\Desktop\Gold edition`, nicht aus vorhandenen Extracts.
   - Er parsed alle effektiv ueberlagerten TaskLists, alle worker-/serf-relevanten Entities, Worker-Arbeitsplatz-Gebaeude, Farm/Residence/Camp-Anhaenge und rekursive `TASK_SET_TASK_LIST`-Kanten.
   - `worker_simulation.py` bevorzugt diese Voll-Extraktion fuer Speed, CamperRange, WorkTime-Werte und `TASK_CHANGE_WORK_TIME_WORK`-Zaehlungen.
   - Beispielkorrektur aus dem Voll-Graph: `PU_Trader` hat ueber `PB_Market2` vier Arbeitsplatz-TaskList-Bloecke; relevante Work-Zyklen enthalten `2` WorkTime-Changes pro Zyklus.

8. Gold-Binary-Branch-/CFG-Belege

   - `analyze_engine_branch_details.py`, `reconstruct_instruction_cfg.py` und `build_worker_camp_path_branch_matrix.py` wurden gegen die Gold-Edition-Binary regeneriert.
   - Ghidra Headless wurde mit `ExportWorkerDecompileEvidence.java` gegen das analysierte Gold-Projekt ausgefuehrt.
   - `config/worker_sim_contract.json/.md` nutzt jetzt dynamische Gold-Binary-Branch-Anker statt alter fest codierter Ubisoft-Adressen.
   - `config/engine_conformance_certificate.json/.md` enthaelt SHA256-Hashes der Binary und aller Nachweis-Artefakte sowie den Proof-Status.
   - Aktueller Zertifikat-Status: XML-/TaskList-Extraktion maschinengeprueft exakt, Runtime-Worker-Werte gegen Extract sauber, statische Binary-CFG plus Ghidra-Decompiler-Evidence vorhanden, vollstaendige Runtime-/Pathfinding-Aequivalenz nicht formal bewiesen.

### Weiterhin offen

1. Technologieeffekte

   `config/tech_effects_coverage_report.md` meldet:

   - 80 originale `T_` Technologien mit Effekten
   - 31 implementiert
   - 49 fehlen
   - davon 32 nicht-kampfbezogen

   Kosten, Zeiten und Voraussetzungen werden jetzt aus XML uebernommen. Fuer deinen Scope (alles ausser Kampfmechanik) bleiben aber Gameplay-Effekte relevant, die in den Technologie-XMLs keinen Zahlenwert tragen, z.B. Markt-, Wetter-, Blessing-, Scout-/Utility- und einige Economy-Effekte.

2. Map-/Placement-Abgleich nicht belastbar

   `compare_game_vs_env.py` nutzt aktuell nur einen sehr kleinen `2x2` Live-Export aus `map_extract/live_export_20260226_195940_*`. Damit ist kein echter Wintersturm-Conformance-Test moeglich.

   Zusaetzlich erwartet das Archiv-Skript `PLAYER_1_DEPOSITS` aus `map_config_wintersturm.py`, diese Struktur existiert dort aktuell nicht in der erwarteten Form.

3. Pfadfindung nicht binary-exakt

   `pathfinding.py` nutzt ein eigenes A*-Modell ueber Walkable-Grid. Gebaeude-Blockflaechen und Farm-/Wohnhaus-Zielpunkte sind jetzt naeher am Original (`Blocked1/2`, `ApproachPos`), aber der Pfadsolver selbst ist nicht nachgewiesen identisch mit der internen Siedler-5-Engine. `GAME_DATA_EXTRACTION.md` dokumentiert selbst, dass die low-level Pfadheuristik in den Engine-Binaries liegt.

   In `fast_train` ist Runtime-Pathing zudem deaktiviert; das ist effizient, aber nicht 1:1.

4. Mathematische Vollbeweisbarkeit

Eine echte mathematische Gleichheit zur proprietaeren Engine ist durch die aktuelle statische Analyse nicht erreicht. Dafuer braeuchte es mindestens: verifizierte Funktionsgrenzen, typisierte Engine-Objektlayouts, eine formal semantische x86-IR/Lifter-Kette, eine State-Relation Engine<->Simulation und beweisbare Transitionsaequivalenz fuer alle erreichbaren Zustaende. Aktuell ist das ein reproduzierbarer Evidence-/Conformance-Stand, kein vollstaendiger Theorem-Proof.

   Ghidra verbessert die Beweislage, ersetzt aber den formalen Beweis nicht: 105/130 Branch-Matrix-Zieladressen wurden einer Ghidra-Funktion zugeordnet; 104 eindeutige Funktionen wurden erfolgreich dekompiliert. Die uebrigen 25 Zieladressen sind nicht automatisch falsch, sondern liegen an unterschiedlichen Funktionsgrenzen/Entry-Heuristiken zwischen Capstone-Matrix und Ghidra.

## Positive Deckung

Der vorhandene `engine_vs_env_diff.py`-Abgleich bestaetigt bereits viele zentrale Wirtschaftsparameter:

- Mine-Tasklisten: relevante `TASK_MINED_RESOURCE` / `TASK_CHANGE_WORK_TIME_WORK` Counts OK.
- Refiner: Ressourcenoperationen pro Zyklus OK, inklusive `coiner=1`, die meisten anderen `=2`.
- Serf ResourceSearchRadius: Engine `4500`, Env `4500`.
- WorkTime-Basiswerte: `base=125`, `threshold_work=25`, `force_to_work_penalty=0.2`.
- Steuerwerte: `TaxAmount=5`, `TaxPenalty=0.1`, `InitialTaxLevel=2`.
- Blessing: `BlessingBonus=0.3`, `BlessingBonusTime=180`.
- Worker-Parameter: 17 Worker plus Serf sind im Report OK.

`config/full_worker_engine_behavior.md` meldet ausserdem:

- 361 effektive TaskLists aus 1041 Layer-Dateien extrahiert
- 21 Worker-/Serf-Entities extrahiert
- 48 Worker-/Pausen-/Arbeitsplatz-Gebaeude extrahiert
- 231 von Workern/Serfs erreichbare TaskLists
- 0 unresolved Worker-TaskList-Refs

## Teststatus

Ausgefuehrte Checks:

- `python smoke_check.py`: OK
- `python engine_vs_env_diff.py`: OK, 0 kritische Punkte, 0 Warnungen
- `python tools/archive/build_engine_conformance_certificate.py`: OK
- Ghidra Headless `ExportWorkerDecompileEvidence.java`: OK, 105/130 Zieladressen gematcht, 104 Funktionen dekompiliert
- `python test_all_actions.py`: 1 Fehler (`TAX: Steuerwechsel fehlgeschlagen`)
- `python -m pytest test_engine_conformance.py test_mechanics.py -q`: 22 passed
- Neue Regressionstests fuer Voll-Worker-Extraktion, Worker-Runtime-Abgleich, Wetter-Schedule, Schnee-Speed auf Refiner-Zyklen, `MaximumFaith`, Original-Footprints, Original-Blocked-AABBs, Worker-Approach-Ziele und Original-Forschungs-XML-Werte sind OK.

Fehlende/fehlgeschlagene Tests:

- `test_main_action_flows_have_legal_path`: `recruit` ist im vorbereiteten Testzustand nicht legal maskiert.
- `test_assign_serf_main_action_allows_build_without_free_serfs`: `assign_serf` fuer Neubau ist ohne freie Serfs nicht legal.
- `test_monastery_motivation`: direkter Kloster-State im Test aendert wegen Cache nicht sichtbar die Motivation.
- `test_tax_motivation`: Steuer-Motivation aendert sich im Test nicht, weil der Income-Zyklus an `_first_worker_building_time` gekoppelt ist.
- `python -m pytest test_training_resource_reward.py test_goal_reward_structure.py -q`: Timeout nach 124s, daher nicht bewertet.

## Bewertung nach Scope

| Bereich | Status | Kommentar |
| --- | --- | --- |
| Wirtschaftsressourcen | Teilweise stark | Viele Originalwerte und Produktionscounts passen, aber Tech-/Wettereffekte fehlen. |
| Serfs/Leibeigene | Gut, aber nicht voll bewiesen | Original-Serf-Behavior, TaskLists, Extraktionszeiten und Suchradius sind voll aus XML extrahiert; exakte Engine-Taskbranching/Pathing nicht voll blackbox-validiert. |
| Worker | Stark bei extrahierter Logik | Voller Worker-TaskList-Graph, WorkTime, Farm/Residence/Camp-Pausen, Camp-Slots, Arbeitsplatz-TaskLists und Wetter-Speed sind modelliert; dynamisches Verhalten muss weiter runtime-validiert werden. |
| Gebaeude-Kosten/Buildzeiten | Stark | `game_data.json` ist gegen Gold edition deckungsgleich. |
| Gebaeude-Placement | Deutlich besser | Footprints kommen jetzt aus `Blocked1/Blocked2` der Original-XMLs; Terrain-/Sektor-/Snap-Sonderfaelle brauchen weiter Runtime-Abgleich. |
| Laufwege | Nicht 1:1 bewiesen | Eigenes A* statt Engine-internem Routing; `fast_train` vereinfacht bewusst. |
| Technologien | Teilweise | Kosten, Zeiten und Preconditions kommen aus XML; nicht-kampfbezogene Runtime-Effekte ohne XML-Wert fehlen teilweise. |
| Wetter | Teilweise | Original-Speedfaktoren und Wintersturm-Schedule sind modelliert; Wetterzauber/Energie sind noch nicht vollstaendig gameplay-validiert. |
| Map-Daten Wintersturm | Nicht ausreichend belegt | Aktueller Live-Export ist nur 2x2 und fuer Vollabgleich unbrauchbar. |

## Naechste technische Schritte

1. Vollstaendigen Wintersturm-Runtime-Export erneuern:
   - `blocking`, `height`, `sector`, `terrain_type`, Entities, Ressourcen, Gebaeude und HQs.
   - Danach `compare_game_vs_env.py` gegen echte Map-Daten laufen lassen.

2. Nicht-kampfbezogene Tech-Effekte aus `tech_effects_coverage_report.md` priorisieren und implementieren oder explizit als irrelevant fuer Training markieren.

3. Runtime-Conformance-Tests fuer Pfade und Placement aufbauen:
   - Serf von HQ zu Baeumen/Deposits/Minen.
   - Worker von Arbeitsplatz zu Farm/Residence/Camp/Supplier.
   - Buildability/Blocking fuer alle relevanten Gebaeude auf echten Engine-Testpunkten.

4. Roten Teststatus bereinigen:
   - Entweder Tests an reale Preconditions anpassen.
   - Oder Env-Masken/Cache/Tax-Zeitlogik korrigieren, falls die Tests das gewuenschte Verhalten abbilden.
