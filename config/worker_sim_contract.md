# Worker Simulation Contract

- Generated: 2026-02-11T20:34:10.403091+00:00
- Scope: worker/camp/path behavior contract for simulation

## Global Parameters

- logic_worktime: base=125, threshold_work=25, force_to_work_penalty=0.2
- logic_movement: worker_flight_distance=2500, leader_nudge_count=3
- default_walk_speed: 240
- camp_internal: slot_count=8, remove_delay_seconds=10.0
- camp_large_fire: num_blocked_points=2, snap_tolerance=30.0
- global_scalars_from_xml:
  - alarm_recharge_time_ms: 180000 (Logic.xml:root/AlarmRechargeTime)
  - max_distance_worker_to_farm: 8000 (PlayerAttraction.xml:root/MaximumDistanceWorkerToFarm)
  - max_distance_worker_to_residence: 8000 (PlayerAttraction.xml:root/MaximumDistanceWorkerToResidence)
  - reattach_worker_frequency: 10 (PlayerAttraction.xml:root/ReAttachWorkerFrequency)
  - worker_flight_distance: 2500 (Logic.xml:root/WorkerFlightDistance)

## Invariants

- worker_count: 18
- worktime_worker_count: 17
- non_worktime_workers: serf
- shared_core_tasklists_consistent: False

## Notable Variants

- farmer: EatTaskList=TL_FARMER_EAT, EatIdleTaskList=TL_FARMER_IDLE
- tavernbarkeeper: EatTaskList=TL_FARMER_EAT, EatIdleTaskList=TL_FARMER_IDLE

## Common State Machine Rules

### idle_start_to_idle
- when: cycle enters idle_start
- tasks: TASK_SET_ANIM -> TASK_LEAVE_BUILDING -> TASK_LEFT_BUILDING -> TASK_GO_TO_CAMP -> TASK_TURN_TO_TARGET_ORIENTATION -> TASK_SET_TASK_LIST
- key_tasks_required: ['TASK_GO_TO_CAMP', 'TASK_SET_TASK_LIST']
- effects: ['worker leaves current building context', 'worker goes to camp', 'worker orientation aligns to camp', 'task list transitions to idle loop']
- dependencies: ['camper_range', 'camp availability/pathing']

### idle_loop_camp_recovery
- when: worker is in idle loop
- tasks: TASK_SET_ANIM -> TASK_RANDOM_WAIT_FOR_ANIM -> TASK_SET_ANIM -> TASK_RANDOM_WAIT_FOR_ANIM -> TASK_SET_ANIM -> TASK_RANDOM_WAIT_FOR_ANIM -> TASK_SET_ANIM -> TASK_RANDOM_WAIT_FOR_ANIM -> TASK_SET_ANIM -> TASK_RANDOM_WAIT_FOR_ANIM -> TASK_CHANGE_WORK_TIME_CAMP -> TASK_ADVANCE_IN_CYCLE
- task_counts: {'TASK_ADVANCE_IN_CYCLE': 1, 'TASK_CHANGE_WORK_TIME_CAMP': 1, 'TASK_RANDOM_WAIT_FOR_ANIM': 5, 'TASK_SET_ANIM': 5}
- key_tasks_required: ['TASK_CHANGE_WORK_TIME_CAMP', 'TASK_ADVANCE_IN_CYCLE']
- effects: ['random idle animations', 'worktime receives camp delta', 'cycle advances to next decision state']
- dependencies: ['work_time_change_camp', 'worktime state variable']

### eat_start_path_and_check
- when: cycle chooses eat
- tasks: TASK_SET_ANIM -> TASK_LEAVE_BUILDING -> TASK_LEFT_BUILDING -> TASK_GO_TO_EAT_BUILDING -> TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS -> TASK_ENTER_BUILDING -> TASK_SET_TASK_LIST
- key_tasks_required: ['TASK_GO_TO_EAT_BUILDING', 'TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS', 'TASK_SET_TASK_LIST']
- effects: ['attempt move to eat building', 'branch on GO_TO_EAT success check', 'enter building and transition to eat loop']
- dependencies: ['eat building availability', 'pathfinding success']

### eat_loop_farm_recovery
- when: worker is in eat loop
- tasks: TASK_CHECK_FEAR -> TASK_RESET_TASK_LIST_TIMER -> TASK_VANISH -> TASK_EAT_WAIT -> TASK_CHANGE_WORK_TIME_FARM -> TASK_ADVANCE_IN_CYCLE
- task_counts: {'TASK_ADVANCE_IN_CYCLE': 1, 'TASK_CHANGE_WORK_TIME_FARM': 1, 'TASK_CHECK_FEAR': 1, 'TASK_EAT_WAIT': 1, 'TASK_RESET_TASK_LIST_TIMER': 1, 'TASK_VANISH': 1}
- key_tasks_required: ['TASK_EAT_WAIT', 'TASK_CHANGE_WORK_TIME_FARM']
- effects: ['eat wait', 'worktime receives farm delta', 'cycle advances']
- dependencies: ['work_time_change_farm', 'eat_wait']

### rest_start_path_and_check
- when: cycle chooses rest
- tasks: TASK_SET_ANIM -> TASK_LEAVE_BUILDING -> TASK_LEFT_BUILDING -> TASK_GO_TO_REST_BUILDING -> TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS -> TASK_ENTER_BUILDING -> TASK_SET_TASK_LIST
- key_tasks_required: ['TASK_GO_TO_REST_BUILDING', 'TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS', 'TASK_SET_TASK_LIST']
- effects: ['attempt move to rest building', 'branch on GO_TO_REST success check', 'enter building and transition to rest loop']
- dependencies: ['residence availability', 'pathfinding success']

### rest_loop_residence_recovery
- when: worker is in rest loop
- tasks: TASK_VANISH -> TASK_CHECK_FEAR -> TASK_RESET_TASK_LIST_TIMER -> TASK_REST_WAIT -> TASK_CHANGE_WORK_TIME_RESIDENCE -> TASK_ADVANCE_IN_CYCLE
- task_counts: {'TASK_ADVANCE_IN_CYCLE': 1, 'TASK_CHANGE_WORK_TIME_RESIDENCE': 1, 'TASK_CHECK_FEAR': 1, 'TASK_RESET_TASK_LIST_TIMER': 1, 'TASK_REST_WAIT': 1, 'TASK_VANISH': 1}
- key_tasks_required: ['TASK_REST_WAIT', 'TASK_CHANGE_WORK_TIME_RESIDENCE']
- effects: ['rest wait', 'worktime receives residence delta', 'cycle advances']
- dependencies: ['work_time_change_residence', 'rest_wait']

### work_start_path_and_check
- when: cycle chooses work
- tasks: -
- key_tasks_required: ['TASK_START_WORK_IF_AT_WORKPLACE', 'TASK_GO_TO_WORK_BUILDING', 'TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS', 'TASK_SET_TASK_LIST']
- effects: ['optionally collect supplier goods', 'attempt move to workplace', 'branch on GO_TO_WORK success check', 'transition to worker-specific work loop']
- dependencies: ['workplace assignment', 'supplier path (if needed)', 'pathfinding success']

### leave_settlement_path_and_check
- when: worker leaves settlement cycle
- tasks: TASK_SET_ANIM -> TASK_LEAVE_BUILDING -> TASK_LEFT_BUILDING -> TASK_GO_TO_LEAVE_BUILDING -> TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS -> TASK_ENTER_BUILDING -> TASK_LEAVE_SETTLEMENT -> TASK_LIST_DONE
- key_tasks_required: ['TASK_GO_TO_LEAVE_BUILDING', 'TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS', 'TASK_LEAVE_SETTLEMENT']
- effects: ['move to village center/leave building', 'branch on leave path success', 'leave settlement']
- dependencies: ['village center availability', 'pathfinding success']

### alarm_flee_interrupt
- when: fear/alarm branch activates
- tasks: TASK_SET_ANIM -> TASK_LEAVE_BUILDING -> TASK_LEFT_BUILDING -> TASK_FLEE -> TASK_SET_ANIM -> TASK_WAIT -> TASK_RETURN_TO_CYCLE
- key_tasks_required: ['TASK_FLEE', 'TASK_WAIT', 'TASK_RETURN_TO_CYCLE']
- effects: ['worker interrupts normal cycle', 'flee task executed', 'returns to cycle after wait']
- dependencies: ['alarm mode', 'worker_flight_distance', 'pathfinding']

### go_to_defendable_building
- when: defendable building branch activates
- tasks: TASK_SET_ANIM -> TASK_LEAVE_BUILDING -> TASK_LEFT_BUILDING -> TASK_MOVE_TO_DEFENDABLE_BUILDING -> TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS -> TASK_ENTER_BUILDING -> TASK_CHANGE_DEFENDABLE_BUILDING_ATTACHMENT -> TASK_VANISH -> TASK_DEFEND
- key_tasks_required: ['TASK_MOVE_TO_DEFENDABLE_BUILDING', 'TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS', 'TASK_DEFEND']
- effects: ['moves to defendable building', 'branches on path success', 'enters defend state']
- dependencies: ['defendable building availability', 'pathfinding success']

## Worker Profiles

### alchemist
- has_worktime: True
- movement: speed=320, rotation_speed=15, camper_range=5000, move_task_list=None
- worktime: wait_until=20000, delta_work=-50, delta_farm=0.7, delta_residence=0.5, delta_camp=0.1, max_farm=100, max_residence=400
- checks: eat_success=True, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_alchemist_work_start.xml']
- work_nodes: ['tl_alchemist_work.xml']

### brickmaker
- has_worktime: True
- movement: speed=320, rotation_speed=15, camper_range=5000, move_task_list=None
- worktime: wait_until=30000, delta_work=-50, delta_farm=0.7, delta_residence=0.5, delta_camp=0.1, max_farm=100, max_residence=400
- checks: eat_success=True, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_brickmaker_work_start.xml']
- work_nodes: ['tl_brickmaker_work.xml']

### coiner
- has_worktime: True
- movement: speed=320, rotation_speed=15, camper_range=2000, move_task_list=None
- worktime: wait_until=4000, delta_work=-100, delta_farm=0.1, delta_residence=0.1, delta_camp=0.2, max_farm=200, max_residence=200
- checks: eat_success=True, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_coiner_work_start.xml']
- work_nodes: ['tl_coiner_work.xml']

### engineer
- has_worktime: True
- movement: speed=320, rotation_speed=15, camper_range=5000, move_task_list=None
- worktime: wait_until=4000, delta_work=-50, delta_farm=0.7, delta_residence=0.5, delta_camp=0.1, max_farm=100, max_residence=400
- checks: eat_success=True, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_engineer_work_start.xml']
- work_nodes: ['tl_engineer_work.xml']

### farmer
- has_worktime: True
- movement: speed=320, rotation_speed=30, camper_range=5000, move_task_list=None
- worktime: wait_until=4000, delta_work=-50, delta_farm=0.7, delta_residence=0.5, delta_camp=0.1, max_farm=100, max_residence=400
- checks: eat_success=False, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_farmer_work_start.xml']
- work_nodes: ['tl_farmer_work.xml']

### gunsmith
- has_worktime: True
- movement: speed=320, rotation_speed=30, camper_range=5000, move_task_list=None
- worktime: wait_until=30000, delta_work=-50, delta_farm=0.7, delta_residence=0.5, delta_camp=0.1, max_farm=100, max_residence=400
- checks: eat_success=True, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_gunsmith_work_start.xml']
- work_nodes: ['tl_gunsmith_work.xml']

### masterbuilder
- has_worktime: True
- movement: speed=320, rotation_speed=15, camper_range=5000, move_task_list=None
- worktime: wait_until=18000, delta_work=-50, delta_farm=0.7, delta_residence=0.5, delta_camp=0.1, max_farm=100, max_residence=400
- checks: eat_success=True, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_master_builder_work1_start.xml']
- work_nodes: ['tl_master_builder_work1.xml']

### miner
- has_worktime: True
- movement: speed=320, rotation_speed=30, camper_range=5000, move_task_list=None
- worktime: wait_until=30000, delta_work=-50, delta_farm=0.7, delta_residence=0.5, delta_camp=0.1, max_farm=100, max_residence=400
- checks: eat_success=True, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_miner_work_start.xml']
- work_nodes: ['tl_miner_claymine_work.xml', 'tl_miner_claymine_work_inside.xml', 'tl_miner_ironmine_work.xml', 'tl_miner_ironmine_work_inside.xml', 'tl_miner_stonemine_work.xml', 'tl_miner_stonemine_work_inside.xml', 'tl_miner_sulfurmine_work.xml', 'tl_miner_sulfurmine_work_inside.xml', 'tl_miner_work.xml']

### priest
- has_worktime: True
- movement: speed=320, rotation_speed=15, camper_range=5000, move_task_list=None
- worktime: wait_until=4000, delta_work=-50, delta_farm=0.7, delta_residence=0.5, delta_camp=0.1, max_farm=100, max_residence=400
- checks: eat_success=True, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_priest_work_start.xml']
- work_nodes: ['tl_priest_work.xml']

### sawmillworker
- has_worktime: True
- movement: speed=320, rotation_speed=15, camper_range=5000, move_task_list=None
- worktime: wait_until=40000, delta_work=-50, delta_farm=0.7, delta_residence=0.5, delta_camp=0.1, max_farm=100, max_residence=400
- checks: eat_success=True, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_sawmillworker_work_start.xml']
- work_nodes: ['tl_sawmillworker_work.xml']

### scholar
- has_worktime: True
- movement: speed=320, rotation_speed=30, camper_range=5000, move_task_list=None
- worktime: wait_until=30000, delta_work=-50, delta_farm=0.7, delta_residence=0.5, delta_camp=0.1, max_farm=100, max_residence=400
- checks: eat_success=True, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_scholar_work_start.xml']
- work_nodes: ['tl_scholar_work.xml']

### serf
- has_worktime: False
- movement: speed=400, rotation_speed=30, camper_range=5000, move_task_list=TL_SERF_WALK
- worktime: wait_until=None, delta_work=None, delta_farm=None, delta_residence=None, delta_camp=None, max_farm=None, max_residence=None
- checks: eat_success=False, rest_success=False, idle_go_to_camp=False
- work_start_nodes: []
- work_nodes: []

### smelter
- has_worktime: True
- movement: speed=320, rotation_speed=30, camper_range=5000, move_task_list=None
- worktime: wait_until=4000, delta_work=-50, delta_farm=0.7, delta_residence=0.5, delta_camp=0.1, max_farm=100, max_residence=400
- checks: eat_success=True, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_smelter_work1.xml', 'tl_smelter_work1_start.xml']
- work_nodes: ['tl_smelter_work1_wait.xml']

### smith
- has_worktime: True
- movement: speed=320, rotation_speed=30, camper_range=5000, move_task_list=None
- worktime: wait_until=30000, delta_work=-50, delta_farm=0.7, delta_residence=0.5, delta_camp=0.1, max_farm=100, max_residence=400
- checks: eat_success=True, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_smith_work_start.xml']
- work_nodes: ['tl_smith_work.xml']

### stonecutter
- has_worktime: True
- movement: speed=320, rotation_speed=15, camper_range=5000, move_task_list=None
- worktime: wait_until=15000, delta_work=-50, delta_farm=0.7, delta_residence=0.5, delta_camp=0.1, max_farm=100, max_residence=400
- checks: eat_success=True, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_stonecutter_work_start.xml']
- work_nodes: ['tl_stonecutter_work.xml']

### tavernbarkeeper
- has_worktime: True
- movement: speed=320, rotation_speed=30, camper_range=5000, move_task_list=None
- worktime: wait_until=4000, delta_work=-50, delta_farm=0.7, delta_residence=0.5, delta_camp=0.1, max_farm=100, max_residence=400
- checks: eat_success=False, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_tavernbarkeeper_work_start.xml']
- work_nodes: ['tl_tavernbarkeeper_work.xml']

### trader
- has_worktime: True
- movement: speed=320, rotation_speed=15, camper_range=5000, move_task_list=None
- worktime: wait_until=18000, delta_work=-50, delta_farm=0.7, delta_residence=0.5, delta_camp=0.1, max_farm=100, max_residence=400
- checks: eat_success=True, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_trader_work_start.xml']
- work_nodes: ['tl_trader_work.xml']

### treasurer
- has_worktime: True
- movement: speed=320, rotation_speed=15, camper_range=5000, move_task_list=None
- worktime: wait_until=15000, delta_work=-50, delta_farm=0.7, delta_residence=0.5, delta_camp=0.1, max_farm=100, max_residence=400
- checks: eat_success=True, rest_success=True, idle_go_to_camp=True
- work_start_nodes: ['tl_treasurer_work_start.xml']
- work_nodes: ['tl_treasurer_work.xml']

## Branch Anchors

### 0x004ed50a
- purpose: TASK_CHANGE_WORK_TIME_CAMP anchor
- jcc=0, blocks=1, insns=10

### 0x004ed68d
- purpose: TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS branch
- jcc=1, blocks=3, insns=18
- 0x004ed68d: jo true=0x004ed694 false=0x004ed68f

### 0x004ed9e7
- purpose: TASK_GO_TO_CAMP anchor
- jcc=0, blocks=1, insns=10

### 0x0062767a
- purpose: dynamic blocking area / blocked points
- jcc=2, blocks=4, insns=417
- 0x0062769a: jg true=0x006276a5 false=0x0062769c
  predicate_hint: `0x00627694: cmp eax, dword ptr [ecx + 0x3adc]`
- 0x006276b7: jne true=0x0062769c false=0x006276b9
  predicate_hint: `0x006276af: cmp dword ptr [0xf583c4], -1`

### 0x00631e3d
- purpose: path runtime: fine/coarse path
- jcc=2, blocks=4, insns=102
- 0x00631e5d: jg true=0x00631e68 false=0x00631e5f
  predicate_hint: `0x00631e57: cmp eax, dword ptr [ecx + 0x3adc]`
- 0x00631e7a: jne true=0x00631e5f false=0x00631e7c
  predicate_hint: `0x00631e72: cmp dword ptr [0xf5cc34], -1`

### 0x0063201a
- purpose: path runtime: next waypoint / orientation / pathing used
- jcc=2, blocks=4, insns=235
- 0x0063203a: jg true=0x00632045 false=0x0063203c
  predicate_hint: `0x00632034: cmp eax, dword ptr [ecx + 0x3adc]`
- 0x00632057: jne true=0x0063203c false=0x00632059
  predicate_hint: `0x0063204f: cmp dword ptr [0xf5cc30], -1`

### 0x00645c1c
- purpose: CCampBehavior branch
- jcc=1, blocks=3, insns=18
- 0x00645c28: je true=0x00645c34 false=0x00645c2a
  predicate_hint: `0x00645c24: test byte ptr [ebp + 8], 1`

### 0x00645e98
- purpose: CCamperBehavior branch
- jcc=1, blocks=3, insns=18
- 0x00645ea8: je true=0x00645eb4 false=0x00645eaa
  predicate_hint: `0x00645ea2: mov dword ptr [esi], 0xbbe3c8`

### 0x006781a8
- purpose: worker reattach/distance checks
- jcc=2, blocks=4, insns=141
- 0x006781c8: jg true=0x006781d3 false=0x006781ca
  predicate_hint: `0x006781c2: cmp eax, dword ptr [ecx + 0x3adc]`
- 0x006781e5: jne true=0x006781ca false=0x006781e7
  predicate_hint: `0x006781dd: cmp dword ptr [0xf6eaf8], -1`

### 0x0069c652
- purpose: CWorkerBehavior branching hub
- jcc=7, blocks=8, insns=63
- 0x0069c677: je true=0x0069c6ab false=0x0069c679
  predicate_hint: `0x0069c675: test ebx, ebx`
- 0x0069c6c1: jne true=0x0069c6d6 false=0x0069c6c3
  predicate_hint: `0x0069c6bd: cmp dword ptr [edi + 0x20], -1`
- 0x0069c6cb: jne true=0x0069c6d0 false=0x0069c6cd
  predicate_hint: `0x0069c6c3: cmp dword ptr [esi*4 + 0xbe1434], -1`
- 0x0069c6d4: jl true=0x0069c6bd false=0x0069c6d6
  predicate_hint: `0x0069c6d1: cmp esi, 6`

### 0x0069ce8f
- purpose: CWorkerFleeBehavior branching hub
- jcc=2, blocks=6, insns=52
- 0x0069ceaf: jle true=0x0069ceb4 false=0x0069ceb1
  predicate_hint: `0x0069cea9: cmp eax, dword ptr [ecx + 0x3adc]`
- 0x0069ced1: jne true=0x0069ceb3 false=0x0069ced3
  predicate_hint: `0x0069cec9: cmp dword ptr [0xf78020], -1`

## Limits

- CFG branch extraction is static and heuristic; indirect targets may be incomplete.
- Some low-level formulas (exact arithmetic order/clamps) need further disassembly validation.
