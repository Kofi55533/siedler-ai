# Initial Findings - 2026-03-14

## Status

Die Reward- und Hyperparameter-Hypothesen wurden lokal auf CPU in mehreren Sweeps getestet.

## Bisher getestete Reward-Hypothesen

- `goal_v1`
- `goal_v1_cumulative`
- `goal_v1_no_path_gate`
- `dense_v2`
- `balanced`
- `sparse`
- `curriculum_unlock`
- `curriculum_stockpile`
- zusaetzlich `unlock_extreme`

## Bisher getestete Hyperparameter-Hypothesen

- `hyper_goal_default`
- `hyper_goal_explore`
- `hyper_goal_short_horizon`
- `hyper_goal_conservative`

## Ergebnis

Unter den bisher gefahrenen lokalen Budgets schlaegt kein Kandidat die `wait`-/maskiert-zufaellig-Baseline auf der eigentlichen Zielmetrik.

Gemeinsames Muster:

- `terminal_potential_metric = 0.0`
- `terminal_path_ready = 0.0`
- `scharf_dependency_progress = 0.5`
- `scharfschuetzen = 0`

## Interpretation

Das Problem ist aktuell nicht feines Reward-Tuning, sondern fehlender verhaltenswirksamer Lernfortschritt im gegebenen Sample-Budget.

## Naechste sinnvolle Hypothesen

1. Harte Unlock-Subtask-Umgebung mit reduziertem Action-Space
2. Automatisches Curriculum `unlock -> stockpile -> goal`
3. Behavior-Cloning oder Demonstrations-Warmstart fuer den Scharfschuetzen-Pfad
4. Laengere Multi-Seed-Sweeps auf schnellerer Hardware
