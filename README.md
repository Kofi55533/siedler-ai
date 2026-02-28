# Siedler AI - Colab Quickstart

Dieses Projekt ist auf `Google Colab` mit `Git-Quelle (main)` und maximaler Trainings-FPS eingestellt.

## Schnellstart

1. In Colab eine neue Notebook-Session starten (GPU Runtime).
2. Den kompletten Inhalt aus `COLAB_COPY_PASTE.py` in **eine** Zelle kopieren.
3. Zelle ausfuehren.

Standardmaessig passiert dann:
- Clone vom neuesten `main` Branch
- Daten-Sync nach `MyDrive/siedler_data`
- Save nach `MyDrive/siedler_training`
- `fast_train` Mode (auf FPS optimiert)
- Auto-Benchmark fuer `SIEDLER_NUM_ENVS`
- Training startet

## Checkpoints (einfach erklaert)

- Beim **ersten Run** hast du noch keine Checkpoints: Das ist normal.
- Dann startet Training automatisch mit einem **neuen Modell**.
- Sobald waehrend des Trainings Checkpoints geschrieben wurden, kann ein spaeterer Run automatisch weitermachen (`SIEDLER_RESUME=1`).

Wichtige Punkte:
- Keine Checkpoints vorhanden -> kein Fehler, normaler Fresh-Start.
- Checkpoints liegen im Save-Ordner (standard: `/content/drive/MyDrive/siedler_training`).

## Wichtige Schalter

Im `COLAB_COPY_PASTE.py` sind diese Defaults aktiv:
- `TRAIN_MODE="fast_train"`
- `SIEDLER_BENCHMARK_AUTO_ENVS=1`
- `SIEDLER_RESUME=1`
- `SIEDLER_RUN_EVAL=0`
- `SIEDLER_RUN_EXPORT=0`

Optional:
- Evaluation aktivieren: `os.environ["SIEDLER_RUN_EVAL"] = "1"`
- Export aktivieren: `os.environ["SIEDLER_RUN_EXPORT"] = "1"`
- Resume deaktivieren (immer neu starten): `os.environ["SIEDLER_RESUME"] = "0"`

## Troubleshooting Kurz

- Wenn Import-Fehler kommen: Runtime neu starten und Zelle erneut ausfuehren.
- Wenn `n_envs` zu hoch instabil ist: manuell setzen, z. B. `os.environ["SIEDLER_NUM_ENVS"]="2"`.
- Wenn Daten fehlen: `player1_resources.json` und `player1_walkable_515.npy` (oder `player1_walkable.npy`) in `DATA_DIR` sicherstellen.
