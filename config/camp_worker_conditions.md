# Camp And Worker Condition Report

- Workers with worktime: 17
- Workers with `TASK_GO_TO_CAMP` in idle-start: 17
- Workers with `TASK_CHANGE_WORK_TIME_CAMP` in idle-chain: 17

## Global Parameters

- WorkTimeBase: 125
- WorkTimeThresholdWork: 25
- ForceToWorkPenalty: 0.2
- Camp Slot Count (`XD_Camp_Internal`): 8
- Camp RemoveDelay: 10.0s

## Map Camp Entities

- mapdata: `C:\Users\marku\OneDrive\Desktop\siedler_ai\map_extract\wintersturm_extracted\mapdata.xml`
- camp-entity count: 10
- CB_Camp: 0
- CB_MinerCamp: 0
- XD_Camp: 0
- XD_Camp_Internal: 0
- XD_LargeCampFire: 4
- other_camp_named: 6

## Worker Highlights

### alchemist
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: True
- Rest path has success check: True

### brickmaker
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: True
- Rest path has success check: True

### coiner
- CamperRange: 2000
- WorkTimeChangeCamp: 0.2
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: True
- Rest path has success check: True

### engineer
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: True
- Rest path has success check: True

### farmer
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: False
- Rest path has success check: True

### gunsmith
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: True
- Rest path has success check: True

### masterbuilder
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: True
- Rest path has success check: True

### miner
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: True
- Rest path has success check: True

### priest
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: True
- Rest path has success check: True

### sawmillworker
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: True
- Rest path has success check: True

### scholar
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: True
- Rest path has success check: True

### smelter
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: True
- Rest path has success check: True

### smith
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: True
- Rest path has success check: True

### stonecutter
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: True
- Rest path has success check: True

### tavernbarkeeper
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: False
- Rest path has success check: True

### trader
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: True
- Rest path has success check: True

### treasurer
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- Idle has TASK_GO_TO_CAMP: True
- Idle chain has TASK_CHANGE_WORK_TIME_CAMP: True
- Eat path has success check: True
- Rest path has success check: True

## Interpretation

- Worker camping is primarily task-driven (`TASK_GO_TO_CAMP` + `TASK_CHANGE_WORK_TIME_CAMP`) and parameterized by `CamperRange` + worktime values.
- Static map camps (`CB_Camp*`/`CB_MinerCamp*`) are separate from worker rest logic and may be absent on a specific map.
- If a map has no `CB_Camp*` placements, worker camp behavior still exists via dynamic camp tasks.
- Exact branch internals for task success/failure checks are engine-side and not fully encoded in XML.
