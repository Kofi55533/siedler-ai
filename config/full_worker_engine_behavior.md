# Full Worker Engine Behavior Extract

- Generated: `2026-06-10T12:17:09.159524+00:00`
- Source root: `C:\Users\marku\OneDrive\Desktop\Gold edition`
- Mode: `layered_game_root`
- Effective TaskLists parsed: `361`
- Worker/serf entities parsed: `21`
- Worker buildings parsed: `48`
- Worker-reachable TaskLists: `231`
- Unresolved worker TaskList refs: `0`
- Distinct task types: `153`

## Runtime Worker Values

| Worker | Speed | CamperRange | WorkWait | EatWait | RestWait | WorkTimeChanges/Cycle |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| alchemist | 320 | 5000 | 20000 | 2000 | 3000 | 2 |
| barkeeper | 320 | 5000 | 4000 | 2000 | 3000 | 1 |
| battleserf | 320 | 5000 |  |  |  | 1 |
| brickmaker | 320 | 5000 | 30000 | 2000 | 3000 | 2 |
| coiner | 320 | 2000 | 4000 | 500 | 500 | 1 |
| cu_serf | 320 | 2000 | 3000 | 3000 | 3000 | 1 |
| cu_trader | 320 | 2000 |  |  |  | 1 |
| engineer | 320 | 5000 | 4000 | 3000 | 2000 | 1 |
| farmer | 320 | 5000 | 4000 | 2000 | 3000 | 1 |
| gunsmith | 320 | 5000 | 30000 | 2000 | 3000 | 2 |
| master_builder | 320 | 5000 | 18000 | 2000 | 3000 | 1 |
| miner | 320 | 5000 | 30000 | 2000 | 3000 | 2 |
| priest | 320 | 5000 | 4000 | 2000 | 3000 | 2 |
| sawmill_worker | 320 | 5000 | 40000 | 2000 | 3000 | 2 |
| scholar | 320 | 5000 | 30000 | 2000 | 3000 | 2 |
| serf | 400 | 5000 |  |  |  | 1 |
| smelter | 320 | 5000 | 4000 | 3000 | 2000 | 1 |
| smith | 320 | 5000 | 30000 | 2000 | 3000 | 2 |
| stonecutter | 320 | 5000 | 15000 | 2000 | 3000 | 2 |
| trader | 320 | 5000 | 18000 | 2000 | 3000 | 2 |
| treasurer | 320 | 5000 | 15000 | 2000 | 3000 | 2 |

## Worker Entity Coverage

| Entity | Env name | WorkTime | Serf | Direct TaskList refs | Reachable TaskLists |
| --- | --- | ---: | ---: | ---: | ---: |
| cu_serf | cu_serf | yes | no | 7 | 28 |
| cu_trader | cu_trader | no | no | 2 | 2 |
| pu_alchemist | alchemist | yes | no | 8 | 18 |
| pu_battleserf | battleserf | no | no | 5 | 5 |
| pu_brickmaker | brickmaker | yes | no | 8 | 22 |
| pu_coiner | coiner | yes | no | 8 | 12 |
| pu_engineer | engineer | yes | no | 8 | 12 |
| pu_farmer | farmer | yes | no | 9 | 20 |
| pu_gunsmith | gunsmith | yes | no | 8 | 16 |
| pu_masterbuilder | master_builder | yes | no | 8 | 14 |
| pu_miner | miner | yes | no | 8 | 66 |
| pu_priest | priest | yes | no | 8 | 24 |
| pu_sawmillworker | sawmill_worker | yes | no | 8 | 16 |
| pu_scholar | scholar | yes | no | 8 | 24 |
| pu_serf | serf | no | yes | 6 | 7 |
| pu_smelter | smelter | yes | no | 7 | 17 |
| pu_smith | smith | yes | no | 8 | 24 |
| pu_stonecutter | stonecutter | yes | no | 8 | 20 |
| pu_tavernbarkeeper | barkeeper | yes | no | 9 | 16 |
| pu_trader | trader | yes | no | 8 | 20 |
| pu_treasurer | treasurer | yes | no | 8 | 16 |

## Worker Building Coverage

| Building | Worker | Work TaskLists | Attachments | Footprint |
| --- | --- | ---: | ---: | --- |
| cb_monasterybuildingsite1 | CU_Serf | 10 | 0 | 1300x1500 |
| pb_alchemist1 | PU_Alchemist | 2 | 1 | 800x1400 |
| pb_alchemist2 | PU_Alchemist | 3 | 1 | 800x1400 |
| pb_bank1 | PU_Treasurer | 2 | 1 | 900x800 |
| pb_bank2 | PU_Treasurer | 2 | 1 | 900x800 |
| pb_blacksmith1 | PU_Smith | 3 | 1 | 900x700 |
| pb_blacksmith2 | PU_Smith | 3 | 1 | 900x700 |
| pb_blacksmith3 | PU_Smith | 3 | 1 | 900x700 |
| pb_brickworks1 | PU_BrickMaker | 3 | 1 | 750x1010 |
| pb_brickworks2 | PU_BrickMaker | 4 | 1 | 750x1010 |
| pb_claymine1 | PU_Miner | 2 | 1 | 1220x970 |
| pb_claymine2 | PU_Miner | 2 | 1 | 1220x970 |
| pb_claymine3 | PU_Miner | 2 | 1 | 1220x970 |
| pb_farm1 | PU_Farmer | 1 | 2 | 600x1000 |
| pb_farm2 | PU_Farmer | 1 | 2 | 600x1000 |
| pb_farm3 | PU_Farmer | 1 | 2 | 600x1000 |
| pb_foundry1 | PU_Smelter | 3 | 0 | 1500x1300 |
| pb_foundry2 | PU_Smelter | 5 | 0 | 1500x1300 |
| pb_gunsmithworkshop1 | PU_Gunsmith | 2 | 1 | 1000x1000 |
| pb_gunsmithworkshop2 | PU_Gunsmith | 2 | 1 | 1000x1000 |
| pb_ironmine1 | PU_Miner | 2 | 1 | 920x1070 |
| pb_ironmine2 | PU_Miner | 3 | 1 | 920x1070 |
| pb_ironmine3 | PU_Miner | 3 | 1 | 920x1070 |
| pb_market2 | PU_Trader | 4 | 1 | 1200x1200 |
| pb_masterbuilderworkshop | PU_MasterBuilder | 2 | 0 | 900x800 |
| pb_monastery1 | PU_Priest | 3 | 1 | 1300x1500 |
| pb_monastery2 | PU_Priest | 3 | 1 | 1300x1500 |
| pb_monastery3 | PU_Priest | 3 | 1 | 1300x1500 |
| pb_powerplant1 | PU_Engineer | 1 | 1 | 500x500 |
| pb_residence1 |  | 0 | 2 | 400x500 |
| pb_residence2 |  | 0 | 2 | 400x500 |
| pb_residence3 |  | 0 | 2 | 400x500 |
| pb_sawmill1 | PU_Sawmillworker | 2 | 1 | 900x1600 |
| pb_sawmill2 | PU_Sawmillworker | 2 | 1 | 900x1600 |
| pb_stonemason1 | PU_Stonecutter | 3 | 1 | 800x1000 |
| pb_stonemason2 | PU_Stonecutter | 3 | 1 | 800x1000 |
| pb_stonemine1 | PU_Miner | 4 | 1 | 1000x1000 |
| pb_stonemine2 | PU_Miner | 4 | 1 | 1000x1000 |
| pb_stonemine3 | PU_Miner | 5 | 1 | 1000x1000 |
| pb_sulfurmine1 | PU_Miner | 2 | 1 | 920x970 |
| pb_sulfurmine2 | PU_Miner | 3 | 1 | 920x970 |
| pb_sulfurmine3 | PU_Miner | 3 | 1 | 920x970 |
| pb_tavern1 | PU_TavernBarkeeper | 1 | 2 | 900x1200 |
| pb_tavern2 | PU_Farmer | 1 | 2 | 900x1200 |
| pb_university1 | PU_Scholar | 4 | 1 | 1300x1500 |
| pb_university2 | PU_Scholar | 4 | 1 | 1300x1500 |
| xd_camp |  | 0 | 0 |  |
| xd_camp_internal |  | 0 | 0 |  |

## Unresolved Worker TaskList References

- none

## Notes

- The JSON contains every parsed task with args under `tasklists`.
- `reachable_worker_tasklists` is the recursive worker/serf/workplace subset.
- Combat-related tasklists are still parsed, but runtime integration can ignore them.
