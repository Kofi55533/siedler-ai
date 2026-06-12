# Worker Simulation Contract

- Generated: 2026-06-10T22:46:50.869403+00:00
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

### 0x004a71d5
- purpose: blocking/placement branch
- jcc=1, blocks=3, insns=395
- 0x004a71e2: jne true=0x004a7785 false=0x004a71e8
  predicate_hint: `0x004a71db: test byte ptr [0x85e170], 1`

### 0x004af71e
- purpose: worker alarm/flee branch
- jcc=1, blocks=3, insns=273
- 0x004af72b: jne true=0x004afaf0 false=0x004af731
  predicate_hint: `0x004af724: test byte ptr [0x85fc30], 1`

### 0x004b208c
- purpose: worker/camp/path selected branch
- jcc=1, blocks=3, insns=1164
- 0x004b2099: jne true=0x004b30d8 false=0x004b209f
  predicate_hint: `0x004b2092: test byte ptr [0x8614f0], 1`

### 0x004b7c82
- purpose: worker alarm/flee branch
- jcc=1, blocks=3, insns=412
- 0x004b7c8f: jne true=0x004b825f false=0x004b7c95
  predicate_hint: `0x004b7c88: test byte ptr [0x862d34], 1`

### 0x004cb80b
- purpose: worker/camp/path selected branch
- jcc=3, blocks=6, insns=122
- 0x004cb896: jne true=0x004cb852 false=0x004cb898
  predicate_hint: `0x004cb894: test al, al`
- 0x004cb927: jne true=0x004cb934 false=0x004cb929
  predicate_hint: `0x004cb925: test al, al`

### 0x004cbbbf
- purpose: worker/camp/path selected branch
- jcc=1, blocks=3, insns=53
- 0x004cbbcc: jne true=0x004cbc59 false=0x004cbbd2
  predicate_hint: `0x004cbbc5: test byte ptr [0x86a824], 1`

### 0x004cf6d6
- purpose: CWorkerBehavior vtable branch
- jcc=16, blocks=31, insns=235
- 0x004cf6e7: je true=0x004cf8eb false=0x004cf6ed
  predicate_hint: `0x004cf6e6: push edi`
- 0x004cf6ee: je true=0x004cf872 false=0x004cf6f4
  predicate_hint: `0x004cf6ed: dec eax`
- 0x004cf6f5: je true=0x004cf7d3 false=0x004cf6fb
  predicate_hint: `0x004cf6f4: dec eax`
- 0x004cf6fc: je true=0x004cf708 false=0x004cf6fe
  predicate_hint: `0x004cf6fb: dec eax`
- 0x004cf717: je true=0x004cf790 false=0x004cf719
  predicate_hint: `0x004cf70e: test al, al`
- 0x004cf737: jle true=0x004cf73c false=0x004cf739
  predicate_hint: `0x004cf734: cmp dword ptr [esi + 0x14], eax`
- 0x004cf74a: jge true=0x004cf74f false=0x004cf74c
  predicate_hint: `0x004cf747: cmp dword ptr [esi + 0x14], eax`
- 0x004cf7ae: jle true=0x004cf7b3 false=0x004cf7b0
  predicate_hint: `0x004cf7ab: cmp dword ptr [esi + 0x14], eax`
- 0x004cf7c1: jge true=0x004cf7c6 false=0x004cf7c3
  predicate_hint: `0x004cf7be: cmp dword ptr [esi + 0x14], eax`
- 0x004cf7e2: je true=0x004cf845 false=0x004cf7e4
  predicate_hint: `0x004cf7d9: test al, al`

### 0x004d2925
- purpose: worker/camp/path selected branch
- jcc=4, blocks=7, insns=48
- 0x004d292c: jne true=0x004d2995 false=0x004d292e
  predicate_hint: `0x004d2928: cmp dword ptr [edi + 0x44], 9`
- 0x004d2942: jne true=0x004d2995 false=0x004d2944
  predicate_hint: `0x004d2940: test eax, eax`
- 0x004d2954: je true=0x004d2994 false=0x004d2956
  predicate_hint: `0x004d2952: test ebx, ebx`
- 0x004d2964: je true=0x004d2994 false=0x004d2966
  predicate_hint: `0x004d2962: test al, al`

### 0x004d34c9
- purpose: worker/camp/path selected branch
- jcc=3, blocks=5, insns=53
- 0x004d34d8: jne true=0x004d34e1 false=0x004d34da
  predicate_hint: `0x004d34d6: test al, al`
- 0x004d34ff: jne true=0x004d351d false=0x004d3501
  predicate_hint: `0x004d34fd: test eax, eax`

### 0x004da815
- purpose: pathfinding/runtime waypoint branch
- jcc=1, blocks=3, insns=219
- 0x004da822: jne true=0x004dab1f false=0x004da828
  predicate_hint: `0x004da81b: test byte ptr [0x86e8a8], 1`

### 0x004dab46
- purpose: pathfinding/runtime waypoint branch
- jcc=1, blocks=3, insns=128
- 0x004dab53: jne true=0x004dad0a false=0x004dab59
  predicate_hint: `0x004dab4c: test byte ptr [0x86e9f0], 1`

### 0x004dad86
- purpose: pathfinding/runtime waypoint branch
- jcc=1, blocks=3, insns=92
- 0x004dad93: jne true=0x004daea1 false=0x004dad99
  predicate_hint: `0x004dad8c: test byte ptr [0x86eb20], 1`

### 0x004daf1d
- purpose: path/blocking predicate vtable branch
- jcc=1, blocks=3, insns=23
- 0x004daf20: jne true=0x004daf2c false=0x004daf22
  predicate_hint: `0x004daf1e: mov edi, ecx`

### 0x004daf73
- purpose: path/blocking predicate vtable branch
- jcc=1, blocks=3, insns=14
- 0x004daf80: je true=0x004daf89 false=0x004daf82
  predicate_hint: `0x004daf7b: test byte ptr [esp + 8], 1`

### 0x004e3324
- purpose: CWorkerBehavior vtable branch
- jcc=1, blocks=3, insns=14
- 0x004e3331: je true=0x004e333a false=0x004e3333
  predicate_hint: `0x004e332c: test byte ptr [esp + 8], 1`

### 0x004e3340
- purpose: CWorkerBehavior vtable branch
- jcc=1, blocks=3, insns=14
- 0x004e334d: je true=0x004e3356 false=0x004e334f
  predicate_hint: `0x004e3348: test byte ptr [esp + 8], 1`

### 0x004e5c2c
- purpose: worker/camp/path selected branch
- jcc=1, blocks=3, insns=130
- 0x004e5c39: jne true=0x004e5de9 false=0x004e5c3f
  predicate_hint: `0x004e5c32: test byte ptr [0x871d88], 1`

### 0x004ffe1f
- purpose: camp/camper behavior vtable branch
- jcc=1, blocks=3, insns=23
- 0x004ffe22: jne true=0x004ffe2e false=0x004ffe24
  predicate_hint: `0x004ffe20: mov edi, ecx`

### 0x004fff0d
- purpose: camp/camper behavior vtable branch
- jcc=1, blocks=3, insns=14
- 0x004fff1a: je true=0x004fff23 false=0x004fff1c
  predicate_hint: `0x004fff15: test byte ptr [esp + 8], 1`

### 0x005000d8
- purpose: camp/camper behavior vtable branch
- jcc=1, blocks=3, insns=14
- 0x005000e5: je true=0x005000ee false=0x005000e7
  predicate_hint: `0x005000e0: test byte ptr [esp + 8], 1`

### 0x00500a1d
- purpose: camp/camper behavior vtable branch
- jcc=1, blocks=3, insns=44
- 0x00500a34: je true=0x00500a80 false=0x00500a36
  predicate_hint: `0x00500a32: test eax, eax`

### 0x00500c65
- purpose: camp/camper behavior vtable branch
- jcc=1, blocks=3, insns=14
- 0x00500c72: je true=0x00500c7b false=0x00500c74
  predicate_hint: `0x00500c6d: test byte ptr [esp + 8], 1`

### 0x00500cea
- purpose: camp/camper behavior vtable branch
- jcc=1, blocks=3, insns=14
- 0x00500cf7: je true=0x00500d00 false=0x00500cf9
  predicate_hint: `0x00500cf2: test byte ptr [esp + 8], 1`

### 0x00508a9b
- purpose: worker/camp/path selected branch
- jcc=1, blocks=3, insns=14
- 0x00508aa8: je true=0x00508ab1 false=0x00508aaa
  predicate_hint: `0x00508aa3: test byte ptr [esp + 8], 1`

### 0x00516ab2
- purpose: pathfinding/runtime waypoint branch
- jcc=1, blocks=3, insns=44
- 0x00516abf: jne true=0x00516b33 false=0x00516ac1
  predicate_hint: `0x00516ab8: test byte ptr [0x87e1f8], 1`

### 0x0052b39d
- purpose: CWorkerBehavior vtable branch
- jcc=5, blocks=7, insns=101
- 0x0052b3ce: jle true=0x0052b476 false=0x0052b3d4
  predicate_hint: `0x0052b3cb: cmp dword ptr [ebp + 8], ebx`
- 0x0052b425: je true=0x0052b44c false=0x0052b427
  predicate_hint: `0x0052b424: dec eax`
- 0x0052b428: jne true=0x0052b46c false=0x0052b42a
  predicate_hint: `0x0052b427: dec eax`
- 0x0052b470: jl true=0x0052b3d4 false=0x0052b476
  predicate_hint: `0x0052b46d: cmp ebx, dword ptr [ebp + 8]`

### 0x0057efde
- purpose: path/blocking predicate vtable branch
- jcc=15, blocks=20, insns=235
- 0x0057efeb: jne true=0x0057eff8 false=0x0057efed
  predicate_hint: `0x0057efe9: test eax, eax`
- 0x0057eff2: je true=0x0057f1dc false=0x0057eff8
  predicate_hint: `0x0057eff0: cmp dword ptr [ecx], eax`
- 0x0057effe: je true=0x0057f1db false=0x0057f004
  predicate_hint: `0x0057effc: test esi, esi`
- 0x0057f026: jge true=0x0057f060 false=0x0057f028
  predicate_hint: `0x0057f01b: cmp esi, 0xffa60000`
- 0x0057f05e: jne true=0x0057f043 false=0x0057f060
  predicate_hint: `0x0057f05b: mov dword ptr [ebp - 0x14], ecx`
- 0x0057f066: jle true=0x0057f09f false=0x0057f068
  predicate_hint: `0x0057f060: cmp esi, 0x5a0000`
- 0x0057f09d: jne true=0x0057f082 false=0x0057f09f
  predicate_hint: `0x0057f09a: mov dword ptr [ebp - 0x14], ecx`
- 0x0057f0a5: jge true=0x0057f0d0 false=0x0057f0a7
  predicate_hint: `0x0057f09f: test esi, esi`
- 0x0057f124: jge true=0x0057f152 false=0x0057f126
  predicate_hint: `0x0057f122: test esi, esi`
- 0x0057f18d: jle true=0x0057f115 false=0x0057f18f
  predicate_hint: `0x0057f186: cmp dword ptr [ebp - 4], 0x16`

### 0x0057f2e1
- purpose: path/blocking predicate vtable branch
- jcc=1, blocks=3, insns=14
- 0x0057f2ee: je true=0x0057f2f7 false=0x0057f2f0
  predicate_hint: `0x0057f2e9: test byte ptr [esp + 8], 1`

### 0x0057fe7c
- purpose: path/blocking predicate vtable branch
- jcc=1, blocks=3, insns=14
- 0x0057fe89: je true=0x0057fe92 false=0x0057fe8b
  predicate_hint: `0x0057fe84: test byte ptr [esp + 8], 1`

### 0x0058051f
- purpose: path/blocking predicate vtable branch
- jcc=1, blocks=3, insns=14
- 0x0058052c: je true=0x00580535 false=0x0058052e
  predicate_hint: `0x00580527: test byte ptr [esp + 8], 1`

### 0x00582db4
- purpose: path/blocking predicate vtable branch
- jcc=8, blocks=12, insns=81
- 0x00582dd9: jne true=0x00582de2 false=0x00582ddb
  predicate_hint: `0x00582dd7: mov ecx, esi`
- 0x00582dfb: je true=0x00582e6b false=0x00582dfd
  predicate_hint: `0x00582df9: test eax, eax`
- 0x00582e07: je true=0x00582e3f false=0x00582e09
  predicate_hint: `0x00582e04: cmp eax, 1`
- 0x00582e0d: je true=0x00582e45 false=0x00582e0f
  predicate_hint: `0x00582e09: cmp dword ptr [ebp + 0x10], 1`
- 0x00582e28: jne true=0x00582e6b false=0x00582e2a
  predicate_hint: `0x00582e26: test al, al`
- 0x00582e43: jne true=0x00582e60 false=0x00582e45
  predicate_hint: `0x00582e3f: cmp dword ptr [ebp + 0x10], 1`
- 0x00582e5e: jne true=0x00582e6b false=0x00582e60
  predicate_hint: `0x00582e5c: test al, al`

### 0x00589a1d
- purpose: path/blocking predicate vtable branch
- jcc=7, blocks=9, insns=54
- 0x00589a3f: jg true=0x00589a72 false=0x00589a41
  predicate_hint: `0x00589a3c: mov dword ptr [ebp - 4], edx`
- 0x00589a48: jge true=0x00589a55 false=0x00589a4a
  predicate_hint: `0x00589a45: cmp esi, dword ptr [ebp + 8]`
- 0x00589a52: jbe true=0x00589a55 false=0x00589a54
  predicate_hint: `0x00589a4e: cmp edx, dword ptr [ecx + esi*8 + 0xc]`
- 0x00589a5b: jbe true=0x00589a71 false=0x00589a5d
  predicate_hint: `0x00589a59: cmp edi, dword ptr [edx]`
- 0x00589a6f: jle true=0x00589a42 false=0x00589a71
  predicate_hint: `0x00589a6d: mov eax, esi`

## Limits

- CFG branch extraction is static and heuristic; indirect targets may be incomplete.
- Some low-level formulas (exact arithmetic order/clamps) need further disassembly validation.
