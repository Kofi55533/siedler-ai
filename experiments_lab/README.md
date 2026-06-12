# Experiments Lab

Dieser Ordner ist die getrennte Experimentierflaeche fuer Reward-, Curriculum- und PPO-Tests.

## Ziel

- Das Hauptprojekt bleibt der Referenzstand.
- Alle laengeren Sweeps, Zwischenergebnisse und Research-Notizen landen hier.
- Jeder Benchmark-Run archiviert Metadaten, Git-Status, Git-Diff und Snapshots der relevanten Python-Dateien.

## Struktur

- `scripts/benchmark_learning_hypotheses.py`: reproduzierbarer Reward-/Hyperparameter-Sweep
- `scripts/run_long_suite.py`: laengere Benchmark-Sequenzen fuer mehrstuendige Tests
- `scripts/summarize_runs.py`: schreibt eine Gesamtauswertung nach `research/latest_summary.md`
- `runs/`: einzelne Benchmark-Runs mit `meta.json`, `git_status.txt`, `git_diff.txt`, `detail.json`, `summary.json`
- `research/`: laufende Notizen, Interpretationen, naechste Hypothesen
- `logs/`: Langlauf-Logs und Suite-Manifeste

## Starten

Einzelner Sweep:

```powershell
python -u experiments_lab\scripts\benchmark_learning_hypotheses.py --group reward --timesteps 8192 --eval-episodes 2 --seeds 0 1
```

Laengere Suite:

```powershell
python -u experiments_lab\scripts\run_long_suite.py --mode cpu_48h_bootstrap
```

Gesamtauswertung aktualisieren:

```powershell
python -u experiments_lab\scripts\summarize_runs.py
```

## Hinweis

Die bisherigen lokalen CPU-Tests zeigen noch keinen Kandidaten, der die `wait`-/Random-Baseline klar schlaegt. Deshalb werden hier gezielt weitere strukturelle Hypothesen archiviert und nicht nur kleine Reward-Gewichte variiert.

Fuer lange Hintergrundlaeufe muss der Rechner wach bleiben. Wenn Windows in Sleep geht, stoppt der Fortschritt effektiv.
