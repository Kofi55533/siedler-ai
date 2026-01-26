# SIEDLER AI - Claude Code Anweisungen

## Projektübersicht
Dies ist ein Reinforcement Learning Projekt für "Die Siedler 5 - Erbe der Könige".
Ziel: AI trainieren die optimale Scharfschützen-Produktion lernt.

## Kontext-Management

### Nach /clear oder neuer Session
1. **IMMER ZUERST `agent.md` lesen** - enthält vollständigen Projektstatus
2. Status-Sektion (oben) gibt Überblick über aktuelle Aufgaben
3. Referenz-Sektion (unten) enthält technische Details

### Bei langen Sessions
- Wenn der Chat lang wird, schlage `/clear` vor
- Nach `/clear`: Lies `agent.md` für vollständigen Kontext
- Der SessionStart-Hook lädt automatisch den Status aus agent.md

### agent.md aktuell halten
Nach signifikanten Änderungen:
1. Aktualisiere "Letzte Aktualisierung" Datum
2. Aktualisiere "Aktueller Task"
3. Füge Änderung zu "LETZTE ÄNDERUNGEN" hinzu
4. Aktualisiere "NÄCHSTE SCHRITTE" wenn nötig
5. Markiere erledigte TODOs in "BEKANNTE ISSUES"

## Wichtige Dateien

| Priorität | Datei | Wann lesen |
|-----------|-------|------------|
| 1 | `agent.md` | Immer zuerst! |
| 2 | `environment.py` | Bei Environment-Änderungen |
| 3 | `pathfinding.py` | Bei Pfadfindungs-Fragen |
| 4 | `production_system.py` | Bei Produktions-Logik |
| 5 | `map_config_wintersturm.py` | Bei Kartendaten-Fragen |

## Projektstruktur
```
siedler_ai/
├── agent.md                    # HAUPTDOKUMENTATION
├── CLAUDE.md                   # Diese Datei
├── environment.py              # RL Environment (179 Actions)
├── production_system.py        # Produktions- und Serf-Logik
├── worker_simulation.py        # WorkTime-System
├── pathfinding.py              # A* Pfadfindung
├── map_config_wintersturm.py   # Kartenkonfiguration
├── player1_walkable.npy        # Begehbarkeits-Grid
├── player1_resources.json      # Ressourcen-Positionen
├── config/
│   ├── game_data.json
│   └── wintersturm_map_data.json
└── .claude/
    ├── hooks/
    │   └── context-reminder.py # SessionStart/Stop Hook
    └── settings.local.json     # Hook-Konfiguration
```

## Coding-Richtlinien

### Python Style
- UTF-8 Encoding Header: `# -*- coding: utf-8 -*-`
- Deutsche Kommentare/Docstrings sind OK (Projekt ist auf Deutsch)
- Type Hints verwenden wo sinnvoll

### Gymnasium Environment
- `step()` gibt `(obs, reward, terminated, truncated, info)` zurück
- Action Masking über `action_masks()` Methode
- Observation Space ist Box mit float32

### Datenstrukturen
- Positionen: `(x, y)` Tupel oder `Position` dataclass
- Ressourcen: String-Keys ("Holz", "Stein", etc.) oder `ResourceType` Enum
- Gebäude: String-Keys mit Level ("Wohnhaus_1", "Wohnhaus_2")

## Bekannte Eigenheiten

1. **Leibeigene vs Worker**: Leibeigene haben KEIN WorkTime-System
2. **Grid-Koordinaten**: Offset (25240, 0) für Spieler 1 Quadrant
3. **Bäume**: Geben 2 Holz und verschwinden dann
4. **Minen-Slots**: Feste Positionen, Minen können NUR dort gebaut werden

## Hooks

Der SessionStart-Hook lädt automatisch den agent.md Status.
Der Stop-Hook erinnert daran, agent.md zu aktualisieren.

Falls Hooks nicht funktionieren, manuell `agent.md` lesen!
