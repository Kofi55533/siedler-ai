# Engine vs Environment Diff Report

Automatisch generiert von engine_vs_env_diff.py

Worker-Parameter werden gegen `config/full_worker_engine_behavior.json` verglichen, weil dieser Extract alle Arbeitsplatz-TaskLists rekursiv einbezieht.

## 1. Minen-Produktion

- OK: claymine_work: mine_ops=2, worktime_ops=2
- OK: claymine_work_inside: mine_ops=2, worktime_ops=2
- OK: ironmine_work: mine_ops=2, worktime_ops=2
- OK: ironmine_work_inside: mine_ops=2, worktime_ops=2
- OK: stonemine_work: mine_ops=2, worktime_ops=1
- OK: stonemine_work_inside: mine_ops=2, worktime_ops=2
- OK: sulfurmine_work: mine_ops=2, worktime_ops=2
- OK: sulfurmine_work_inside: mine_ops=2, worktime_ops=2

## 2. Refiner/Verarbeiter

- OK: alchemist: resource_ops=2
- OK: brickmaker: resource_ops=2
- OK: coiner: resource_ops=1
- OK: gunsmith: resource_ops=2
- OK: miner: resource_ops=1
- OK: sawmillworker: resource_ops=2
- OK: smith: resource_ops=2
- OK: stonecutter: resource_ops=2
- OK: treasurer: resource_ops=2

## 3. Deposit-Mengen

- OK: xd_clay1: 400
- INFO: xd_claypit1: Engine=12000 vs Env=4000 (Map-Override plausibel: runtime_export=4000)
- OK: xd_iron1: 400
- INFO: xd_ironpit1: Engine=12000 vs Env=4000 (Map-Override plausibel: runtime_export=4000)
- INFO: xd_resourcetree: Engine=0, Env=nicht definiert
- OK: xd_stone1: 400
- INFO: xd_stonepit1: Engine=14000 vs Env=4000 (Map-Override plausibel: runtime_export=4000)
- OK: xd_sulfur1: 400
- INFO: xd_sulfurpit1: Engine=8000 vs Env=4000 (Map-Override plausibel: runtime_export=4000)

## 4. Worker-Parameter

- OK: alchemist
- OK: brickmaker
- OK: coiner
- OK: engineer
- OK: farmer
- OK: gunsmith
- OK: masterbuilder
- OK: miner
- OK: priest
- OK: sawmillworker
- OK: scholar
- OK: smelter
- OK: smith
- OK: stonecutter
- OK: tavernbarkeeper
- OK: trader
- OK: treasurer

## 5. Serf und Logik

- Serf ResourceSearchRadius: Engine=4500, Env=4500 [OK]
- OK: worktime_base: 125
- OK: worktime_threshold_work: 25
- OK: force_to_work_penalty: 0.2
- TaxAmount: Engine=5, Env=5 [OK]
- TaxPenalty: Engine=0.1, Env=0.1 [OK]
- InitialTaxLevel: Engine=2, Env=2 [OK]
- BlessingBonus: Engine=0.3, Env=0.3 [OK]
- BlessingBonusTime: Engine=180, Env=180 [OK]
- MaximumFaith: Engine=5000, Env=5000 [OK]
- OK: Blessing worker filter ist modelliert
- SnowMoveSpeedFactor: Engine=0.85, Env=0.85 [OK]

---

## Zusammenfassung

- Kritische Punkte: 0
- Warnungen: 0
