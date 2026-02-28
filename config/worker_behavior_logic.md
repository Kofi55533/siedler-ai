# Worker Behavior Logic (Complete Extraction)

- Workers: 18
- Workers with worktime: 17
- Workers with `TASK_GO_TO_CAMP` in idle-start: 17
- Workers with `TASK_CHANGE_WORK_TIME_CAMP` in idle-chain: 17
- Workers with unresolved tasklists: 0

## alchemist
- Env name: alchemist
- Has worktime: True
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- WorkWaitUntil(ms): 20000
- Eat path success-check task: True
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 11 nodes, 4 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_WORKER_IDLE_START
- EatTaskList: TL_WORKER_EAT_START
- FlightTaskList: TL_WORKER_FLEE
- GoToDefendableBuildingTaskList: TL_WORKER_GO_TO_DEFENDABLE_BUILDING
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_ALCHEMIST_WORK_START

### Task Graph Nodes
- tl_alchemist_work.xml (Work)
  file: TL_ALCHEMIST_WORK.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_REFINE_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_alchemist_work_start.xml (Work)
  file: TL_ALCHEMIST_WORK_START.xml
  set_task_list_targets: TL_ALCHEMIST_WORK
  checks: TASK_CHECK_GO_TO_SUPPLIER_SUCCESS, TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_worker_eat.xml (Eat)
  file: TL_WORKER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_FARM, TASK_EAT_WAIT
- tl_worker_eat_start.xml (Eat)
  file: TL_WORKER_EAT_START.xml
  set_task_list_targets: TL_WORKER_EAT
  checks: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_go_to_defendable_building.xml ()
  file: TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml
  checks: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## brickmaker
- Env name: brickmaker
- Has worktime: True
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- WorkWaitUntil(ms): 30000
- Eat path success-check task: True
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 11 nodes, 4 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_WORKER_IDLE_START
- EatTaskList: TL_WORKER_EAT_START
- FlightTaskList: TL_WORKER_FLEE
- GoToDefendableBuildingTaskList: TL_WORKER_GO_TO_DEFENDABLE_BUILDING
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_BRICKMAKER_WORK_START

### Task Graph Nodes
- tl_brickmaker_work.xml (Work)
  file: TL_BRICKMAKER_WORK.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_REFINE_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_brickmaker_work_start.xml (Work)
  file: TL_BRICKMAKER_WORK_START.xml
  set_task_list_targets: TL_BRICKMAKER_WORK
  checks: TASK_CHECK_GO_TO_SUPPLIER_SUCCESS, TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_worker_eat.xml (Eat)
  file: TL_WORKER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_FARM, TASK_EAT_WAIT
- tl_worker_eat_start.xml (Eat)
  file: TL_WORKER_EAT_START.xml
  set_task_list_targets: TL_WORKER_EAT
  checks: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_go_to_defendable_building.xml ()
  file: TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml
  checks: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## coiner
- Env name: coiner
- Has worktime: True
- CamperRange: 2000
- WorkTimeChangeCamp: 0.2
- WorkWaitUntil(ms): 4000
- Eat path success-check task: True
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 11 nodes, 4 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_WORKER_IDLE_START
- EatTaskList: TL_WORKER_EAT_START
- FlightTaskList: TL_WORKER_FLEE
- GoToDefendableBuildingTaskList: TL_WORKER_GO_TO_DEFENDABLE_BUILDING
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_COINER_WORK_START

### Task Graph Nodes
- tl_coiner_work.xml (Work)
  file: TL_COINER_WORK.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_REFINE_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_coiner_work_start.xml (Work)
  file: TL_COINER_WORK_START.xml
  set_task_list_targets: TL_COINER_WORK
  checks: TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_worker_eat.xml (Eat)
  file: TL_WORKER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_FARM, TASK_EAT_WAIT
- tl_worker_eat_start.xml (Eat)
  file: TL_WORKER_EAT_START.xml
  set_task_list_targets: TL_WORKER_EAT
  checks: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_go_to_defendable_building.xml ()
  file: TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml
  checks: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## engineer
- Env name: engineer
- Has worktime: True
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- WorkWaitUntil(ms): 4000
- Eat path success-check task: True
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 11 nodes, 4 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_WORKER_IDLE_START
- EatTaskList: TL_WORKER_EAT_START
- FlightTaskList: TL_WORKER_FLEE
- GoToDefendableBuildingTaskList: TL_WORKER_GO_TO_DEFENDABLE_BUILDING
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_ENGINEER_WORK_START

### Task Graph Nodes
- tl_engineer_work.xml (Work)
  file: TL_ENGINEER_WORK.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_engineer_work_start.xml (Work)
  file: TL_ENGINEER_WORK_START.xml
  set_task_list_targets: TL_ENGINEER_WORK
  checks: TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_worker_eat.xml (Eat)
  file: TL_WORKER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_FARM, TASK_EAT_WAIT
- tl_worker_eat_start.xml (Eat)
  file: TL_WORKER_EAT_START.xml
  set_task_list_targets: TL_WORKER_EAT
  checks: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_go_to_defendable_building.xml ()
  file: TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml
  checks: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## farmer
- Env name: farmer
- Has worktime: True
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- WorkWaitUntil(ms): 4000
- Eat path success-check task: False
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 11 nodes, 3 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_FARMER_IDLE
- EatTaskList: TL_FARMER_EAT
- FlightTaskList: TL_WORKER_FLEE
- GoToDefendableBuildingTaskList: TL_WORKER_GO_TO_DEFENDABLE_BUILDING
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_FARMER_WORK_START

### Task Graph Nodes
- tl_farmer_eat.xml (Eat)
  file: TL_FARMER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RELATIVE, TASK_EAT_WAIT
- tl_farmer_idle.xml (Idle)
  file: TL_FARMER_IDLE.xml
- tl_farmer_work.xml (Work)
  file: TL_FARMER_WORK.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_farmer_work_start.xml (Work)
  file: TL_FARMER_WORK_START.xml
  set_task_list_targets: TL_FARMER_WORK
  checks: TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_go_to_defendable_building.xml ()
  file: TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml
  checks: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## gunsmith
- Env name: gunsmith
- Has worktime: True
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- WorkWaitUntil(ms): 30000
- Eat path success-check task: True
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 11 nodes, 4 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_WORKER_IDLE_START
- EatTaskList: TL_WORKER_EAT_START
- FlightTaskList: TL_WORKER_FLEE
- GoToDefendableBuildingTaskList: TL_WORKER_GO_TO_DEFENDABLE_BUILDING
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_GUNSMITH_WORK_START

### Task Graph Nodes
- tl_gunsmith_work.xml (Work)
  file: TL_GUNSMITH_WORK.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_MINED_RESOURCE, TASK_REFINE_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_gunsmith_work_start.xml (Work)
  file: TL_GUNSMITH_WORK_START.xml
  set_task_list_targets: TL_GUNSMITH_WORK
  checks: TASK_CHECK_GO_TO_SUPPLIER_SUCCESS, TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_worker_eat.xml (Eat)
  file: TL_WORKER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_FARM, TASK_EAT_WAIT
- tl_worker_eat_start.xml (Eat)
  file: TL_WORKER_EAT_START.xml
  set_task_list_targets: TL_WORKER_EAT
  checks: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_go_to_defendable_building.xml ()
  file: TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml
  checks: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## masterbuilder
- Env name: master_builder
- Has worktime: True
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- WorkWaitUntil(ms): 18000
- Eat path success-check task: True
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 11 nodes, 4 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_WORKER_IDLE_START
- EatTaskList: TL_WORKER_EAT_START
- FlightTaskList: TL_WORKER_FLEE
- GoToDefendableBuildingTaskList: TL_WORKER_GO_TO_DEFENDABLE_BUILDING
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_MASTER_BUILDER_WORK1_START

### Task Graph Nodes
- tl_master_builder_work1.xml (Work)
  file: TL_MASTER_BUILDER_WORK1.xml
  checks: TASK_CHECK_FEAR, TASK_CHECK_GO_TO_BRIDGE_SUCCESS, TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_master_builder_work1_start.xml (Work)
  file: TL_MASTER_BUILDER_WORK1_START.xml
  set_task_list_targets: TL_MASTER_BUILDER_WORK1
  checks: TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_worker_eat.xml (Eat)
  file: TL_WORKER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_FARM, TASK_EAT_WAIT
- tl_worker_eat_start.xml (Eat)
  file: TL_WORKER_EAT_START.xml
  set_task_list_targets: TL_WORKER_EAT
  checks: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_go_to_defendable_building.xml ()
  file: TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml
  checks: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## miner
- Env name: miner
- Has worktime: True
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- WorkWaitUntil(ms): 30000
- Eat path success-check task: True
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 19 nodes, 4 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_WORKER_IDLE_START
- EatTaskList: TL_WORKER_EAT_START
- FlightTaskList: TL_WORKER_FLEE
- GoToDefendableBuildingTaskList: TL_WORKER_GO_TO_DEFENDABLE_BUILDING
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_MINER_WORK_START

### Task Graph Nodes
- tl_miner_claymine_work.xml (Work)
  file: TL_MINER_CLAYMINE_WORK.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_MINED_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_miner_claymine_work_inside.xml (Work)
  file: TL_MINER_CLAYMINE_WORK_INSIDE.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_MINED_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_miner_ironmine_work.xml (Work)
  file: TL_MINER_IRONMINE_WORK.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_MINED_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_ABSOLUTE, TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_miner_ironmine_work_inside.xml (Work)
  file: TL_MINER_IRONMINE_WORK_INSIDE.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_MINED_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_miner_stonemine_work.xml (Work)
  file: TL_MINER_STONEMINE_WORK.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_MINED_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_miner_stonemine_work_inside.xml (Work)
  file: TL_MINER_STONEMINE_WORK_INSIDE.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_MINED_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_miner_sulfurmine_work.xml (Work)
  file: TL_MINER_SULFURMINE_WORK.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_MINED_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_miner_sulfurmine_work_inside.xml (Work)
  file: TL_MINER_SULFURMINE_WORK_INSIDE.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_MINED_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_miner_work.xml (Work)
  file: TL_MINER_WORK.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_MINED_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_miner_work_start.xml (Work)
  file: TL_MINER_WORK_START.xml
  set_task_list_targets: TL_MINER_WORK
  checks: TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_worker_eat.xml (Eat)
  file: TL_WORKER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_FARM, TASK_EAT_WAIT
- tl_worker_eat_start.xml (Eat)
  file: TL_WORKER_EAT_START.xml
  set_task_list_targets: TL_WORKER_EAT
  checks: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_go_to_defendable_building.xml ()
  file: TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml
  checks: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## priest
- Env name: priest
- Has worktime: True
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- WorkWaitUntil(ms): 4000
- Eat path success-check task: True
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 11 nodes, 4 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_WORKER_IDLE_START
- EatTaskList: TL_WORKER_EAT_START
- FlightTaskList: TL_WORKER_FLEE
- GoToDefendableBuildingTaskList: TL_WORKER_GO_TO_DEFENDABLE_BUILDING
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_PRIEST_WORK_START

### Task Graph Nodes
- tl_priest_work.xml (Work)
  file: TL_PRIEST_WORK.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_priest_work_start.xml (Work)
  file: TL_PRIEST_WORK_START.xml
  set_task_list_targets: TL_PRIEST_WORK
  checks: TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_worker_eat.xml (Eat)
  file: TL_WORKER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_FARM, TASK_EAT_WAIT
- tl_worker_eat_start.xml (Eat)
  file: TL_WORKER_EAT_START.xml
  set_task_list_targets: TL_WORKER_EAT
  checks: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_go_to_defendable_building.xml ()
  file: TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml
  checks: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## sawmillworker
- Env name: sawmill_worker
- Has worktime: True
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- WorkWaitUntil(ms): 40000
- Eat path success-check task: True
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 11 nodes, 4 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_WORKER_IDLE_START
- EatTaskList: TL_WORKER_EAT_START
- FlightTaskList: TL_WORKER_FLEE
- GoToDefendableBuildingTaskList: TL_WORKER_GO_TO_DEFENDABLE_BUILDING
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_SAWMILLWORKER_WORK_START

### Task Graph Nodes
- tl_sawmillworker_work.xml (Work)
  file: TL_SAWMILLWORKER_WORK.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_REFINE_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_sawmillworker_work_start.xml (Work)
  file: TL_SAWMILLWORKER_WORK_START.xml
  set_task_list_targets: TL_SAWMILLWORKER_WORK
  checks: TASK_CHECK_GO_TO_SUPPLIER_SUCCESS, TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_worker_eat.xml (Eat)
  file: TL_WORKER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_FARM, TASK_EAT_WAIT
- tl_worker_eat_start.xml (Eat)
  file: TL_WORKER_EAT_START.xml
  set_task_list_targets: TL_WORKER_EAT
  checks: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_go_to_defendable_building.xml ()
  file: TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml
  checks: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## scholar
- Env name: scholar
- Has worktime: True
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- WorkWaitUntil(ms): 30000
- Eat path success-check task: True
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 11 nodes, 4 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_WORKER_IDLE_START
- EatTaskList: TL_WORKER_EAT_START
- FlightTaskList: TL_WORKER_FLEE
- GoToDefendableBuildingTaskList: TL_WORKER_GO_TO_DEFENDABLE_BUILDING
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_SCHOLAR_WORK_START

### Task Graph Nodes
- tl_scholar_work.xml (Work)
  file: TL_SCHOLAR_WORK.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_scholar_work_start.xml (Work)
  file: TL_SCHOLAR_WORK_START.xml
  set_task_list_targets: TL_SCHOLAR_WORK
  checks: TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_worker_eat.xml (Eat)
  file: TL_WORKER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_FARM, TASK_EAT_WAIT
- tl_worker_eat_start.xml (Eat)
  file: TL_WORKER_EAT_START.xml
  set_task_list_targets: TL_WORKER_EAT
  checks: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_go_to_defendable_building.xml ()
  file: TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml
  checks: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## serf
- Env name: serf
- Has worktime: False
- CamperRange: 5000
- WorkTimeChangeCamp: None
- WorkWaitUntil(ms): None
- Eat path success-check task: False
- Rest path success-check task: False
- Idle has GO_TO_CAMP: False
- Idle chain has CHANGE_WORK_TIME_CAMP: False
- Task graph: 7 nodes, 1 edges, 0 unresolved

### Entry Tasklists
- ApproachConstructionSiteTaskList: TL_SERF_GO_TO_CONSTRUCTION_SITE
- BattleTaskList: TL_BATTLE
- TurnIntoBattleSerfTaskList: TL_SERF_TURN_INTO_BATTLE_SERF
- MoveTaskList: TL_SERF_WALK

### Task Graph Nodes
- tl_battle.xml ()
  file: TL_BATTLE.xml
  checks: TASK_CHECK_RANGE
- tl_serf_build.xml ()
  file: TL_SERF_BUILD.xml
- tl_serf_extract_resource.xml ()
  file: TL_SERF_EXTRACT_RESOURCE.xml
  resource tasks: TASK_EXTRACT_RESOURCE
  worktime tasks: TASK_WAIT_EXTRACTION_DELAY
- tl_serf_extract_wood.xml ()
  file: TL_SERF_EXTRACT_WOOD.xml
  resource tasks: TASK_EXTRACT_RESOURCE
  worktime tasks: TASK_WAIT_EXTRACTION_DELAY
- tl_serf_go_to_construction_site.xml ()
  file: TL_SERF_GO_TO_CONSTRUCTION_SITE.xml
  set_task_list_targets: TL_SERF_BUILD
- tl_serf_turn_into_battle_serf.xml ()
  file: TL_SERF_TURN_INTO_BATTLE_SERF.xml
- tl_serf_walk.xml ()
  file: TL_SERF_WALK.xml

## smelter
- Env name: smelter
- Has worktime: True
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- WorkWaitUntil(ms): 4000
- Eat path success-check task: True
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 11 nodes, 5 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_WORKER_IDLE_START
- EatTaskList: TL_WORKER_EAT_START
- FlightTaskList: TL_WORKER_FLEE
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_SMELTER_WORK1_START

### Task Graph Nodes
- tl_smelter_work1.xml (Work)
  file: TL_SMELTER_WORK1.xml
  set_task_list_targets: TL_SMELTER_WORK1_WAIT
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_smelter_work1_start.xml (Work)
  file: TL_SMELTER_WORK1_START.xml
  set_task_list_targets: TL_SMELTER_WORK1_WAIT
  checks: TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_smelter_work1_wait.xml (Work)
  file: TL_SMELTER_WORK1_WAIT.xml
- tl_worker_eat.xml (Eat)
  file: TL_WORKER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_FARM, TASK_EAT_WAIT
- tl_worker_eat_start.xml (Eat)
  file: TL_WORKER_EAT_START.xml
  set_task_list_targets: TL_WORKER_EAT
  checks: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## smith
- Env name: smith
- Has worktime: True
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- WorkWaitUntil(ms): 30000
- Eat path success-check task: True
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 11 nodes, 4 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_WORKER_IDLE_START
- EatTaskList: TL_WORKER_EAT_START
- FlightTaskList: TL_WORKER_FLEE
- GoToDefendableBuildingTaskList: TL_WORKER_GO_TO_DEFENDABLE_BUILDING
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_SMITH_WORK_START

### Task Graph Nodes
- tl_smith_work.xml (Work)
  file: TL_SMITH_WORK.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_MINED_RESOURCE, TASK_REFINE_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_smith_work_start.xml (Work)
  file: TL_SMITH_WORK_START.xml
  set_task_list_targets: TL_SMITH_WORK
  checks: TASK_CHECK_GO_TO_SUPPLIER_SUCCESS, TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_worker_eat.xml (Eat)
  file: TL_WORKER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_FARM, TASK_EAT_WAIT
- tl_worker_eat_start.xml (Eat)
  file: TL_WORKER_EAT_START.xml
  set_task_list_targets: TL_WORKER_EAT
  checks: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_go_to_defendable_building.xml ()
  file: TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml
  checks: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## stonecutter
- Env name: stonecutter
- Has worktime: True
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- WorkWaitUntil(ms): 15000
- Eat path success-check task: True
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 11 nodes, 4 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_WORKER_IDLE_START
- EatTaskList: TL_WORKER_EAT_START
- FlightTaskList: TL_WORKER_FLEE
- GoToDefendableBuildingTaskList: TL_WORKER_GO_TO_DEFENDABLE_BUILDING
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_STONECUTTER_WORK_START

### Task Graph Nodes
- tl_stonecutter_work.xml (Work)
  file: TL_STONECUTTER_WORK.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_REFINE_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_stonecutter_work_start.xml (Work)
  file: TL_STONECUTTER_WORK_START.xml
  set_task_list_targets: TL_STONECUTTER_WORK
  checks: TASK_CHECK_GO_TO_SUPPLIER_SUCCESS, TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_worker_eat.xml (Eat)
  file: TL_WORKER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_FARM, TASK_EAT_WAIT
- tl_worker_eat_start.xml (Eat)
  file: TL_WORKER_EAT_START.xml
  set_task_list_targets: TL_WORKER_EAT
  checks: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_go_to_defendable_building.xml ()
  file: TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml
  checks: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## tavernbarkeeper
- Env name: barkeeper
- Has worktime: True
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- WorkWaitUntil(ms): 4000
- Eat path success-check task: False
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 11 nodes, 3 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_FARMER_IDLE
- EatTaskList: TL_FARMER_EAT
- FlightTaskList: TL_WORKER_FLEE
- GoToDefendableBuildingTaskList: TL_WORKER_GO_TO_DEFENDABLE_BUILDING
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_TAVERNBARKEEPER_WORK_START

### Task Graph Nodes
- tl_farmer_eat.xml (Eat)
  file: TL_FARMER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RELATIVE, TASK_EAT_WAIT
- tl_farmer_idle.xml (Idle)
  file: TL_FARMER_IDLE.xml
- tl_tavernbarkeeper_work.xml (Work)
  file: TL_TAVERNBARKEEPER_WORK.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_tavernbarkeeper_work_start.xml (Work)
  file: TL_TAVERNBARKEEPER_WORK_START.xml
  set_task_list_targets: TL_TAVERNBARKEEPER_WORK
  checks: TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_go_to_defendable_building.xml ()
  file: TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml
  checks: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## trader
- Env name: trader
- Has worktime: True
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- WorkWaitUntil(ms): 18000
- Eat path success-check task: True
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 11 nodes, 4 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_WORKER_IDLE_START
- EatTaskList: TL_WORKER_EAT_START
- FlightTaskList: TL_WORKER_FLEE
- GoToDefendableBuildingTaskList: TL_WORKER_GO_TO_DEFENDABLE_BUILDING
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_TRADER_WORK_START

### Task Graph Nodes
- tl_trader_work.xml (Work)
  file: TL_TRADER_WORK.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_trader_work_start.xml (Work)
  file: TL_TRADER_WORK_START.xml
  set_task_list_targets: TL_TRADER_WORK
  checks: TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_worker_eat.xml (Eat)
  file: TL_WORKER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_FARM, TASK_EAT_WAIT
- tl_worker_eat_start.xml (Eat)
  file: TL_WORKER_EAT_START.xml
  set_task_list_targets: TL_WORKER_EAT
  checks: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_go_to_defendable_building.xml ()
  file: TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml
  checks: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## treasurer
- Env name: treasurer
- Has worktime: True
- CamperRange: 5000
- WorkTimeChangeCamp: 0.1
- WorkWaitUntil(ms): 15000
- Eat path success-check task: True
- Rest path success-check task: True
- Idle has GO_TO_CAMP: True
- Idle chain has CHANGE_WORK_TIME_CAMP: True
- Task graph: 11 nodes, 4 edges, 0 unresolved

### Entry Tasklists
- EatIdleTaskList: TL_WORKER_IDLE_START
- EatTaskList: TL_WORKER_EAT_START
- FlightTaskList: TL_WORKER_FLEE
- GoToDefendableBuildingTaskList: TL_WORKER_GO_TO_DEFENDABLE_BUILDING
- LeaveTaskList: TL_WORKER_LEAVE
- RestIdleTaskList: TL_WORKER_IDLE_START
- RestTaskList: TL_WORKER_REST_START
- WorkIdleTaskList: TL_WORKER_IDLE_START
- WorkTaskList: TL_TREASURER_WORK_START

### Task Graph Nodes
- tl_treasurer_work.xml (Work)
  file: TL_TREASURER_WORK.xml
  checks: TASK_CHECK_FEAR
  resource tasks: TASK_REFINE_RESOURCE
  worktime tasks: TASK_CHANGE_WORK_TIME_WORK, TASK_WORK_WAIT_UNTIL
- tl_treasurer_work_start.xml (Work)
  file: TL_TREASURER_WORK_START.xml
  set_task_list_targets: TL_TREASURER_WORK
  checks: TASK_CHECK_GO_TO_SUPPLIER_SUCCESS, TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- tl_worker_eat.xml (Eat)
  file: TL_WORKER_EAT.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_FARM, TASK_EAT_WAIT
- tl_worker_eat_start.xml (Eat)
  file: TL_WORKER_EAT_START.xml
  set_task_list_targets: TL_WORKER_EAT
  checks: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- tl_worker_flee.xml ()
  file: TL_WORKER_FLEE.xml
- tl_worker_go_to_defendable_building.xml ()
  file: TL_WORKER_GO_TO_DEFENDABLE_BUILDING.xml
  checks: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS
- tl_worker_idle.xml (Idle)
  file: TL_WORKER_IDLE.xml
  worktime tasks: TASK_CHANGE_WORK_TIME_CAMP
- tl_worker_idle_start.xml (Idle)
  file: TL_WORKER_IDLE_START.xml
  set_task_list_targets: TL_WORKER_IDLE
- tl_worker_leave.xml (Leave)
  file: TL_WORKER_LEAVE.xml
  checks: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS
- tl_worker_rest.xml (Rest)
  file: TL_WORKER_REST.xml
  checks: TASK_CHECK_FEAR
  worktime tasks: TASK_CHANGE_WORK_TIME_RESIDENCE, TASK_REST_WAIT
- tl_worker_rest_start.xml (Rest)
  file: TL_WORKER_REST_START.xml
  set_task_list_targets: TL_WORKER_REST
  checks: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS

## Limitation
- XML/tasklists expose most behavior structure and parameters.
- Exact internal branch semantics per task execution remain in engine code.
