# Engine Instruction CFG Reconstruction

- Binary: `C:\Users\marku\OneDrive\Desktop\Gold edition\bin\SettlersHoK.exe`
- Arch: `x86` (`machine=0x14c`)
- ImageBase: `0x400000`
- .text: `0x401000` -> `0x760000`
- Target patterns: 65
- Matched strings: 177
- Direct call sites in .text: 84522
- RTTI vtable method anchors: 91 (classes: 22)
- Caller expansion: depth=3, window=0x20, max_callers/entry=120, max_functions=500
- Candidate functions: 153
- Total basic blocks: 591
- Total instructions: 8761
- Conditional branches: 275
- Switch candidates (indirect jmp): 0

## Matched Strings

- `NumBlockedPoints` (pattern `NumBlockedPoints`, va `0x0076e5ac`, xrefs 1)
- `BlockingArea` (pattern `BlockingArea`, va `0x0076e5c0`, xrefs 1)
- `WorkerAlarmModeActive` (pattern `WorkerAlarmMode`, va `0x0076ee00`, xrefs 1)
- `WorkerFlightDistance` (pattern `WorkerFlightDistance`, va `0x0076f19c`, xrefs 1)
- `WorkTimeThresholdCampFire` (pattern `WorkTimeThresholdCampFire`, va `0x0076f384`, xrefs 1)
- `WorkTimeThresholdResidence` (pattern `WorkTimeThresholdResidence`, va `0x0076f3a0`, xrefs 1)
- `WorkTimeThresholdFarm` (pattern `WorkTimeThresholdFarm`, va `0x0076f3bc`, xrefs 1)
- `WorkTimeThresholdWork` (pattern `WorkTimeThresholdWork`, va `0x0076f3d4`, xrefs 1)
- `WorkTimeBase` (pattern `WorkTimeBase`, va `0x0076f3ec`, xrefs 1)
- `WorkerAlarmMode` (pattern `WorkerAlarmMode`, va `0x0076fda0`, xrefs 1)
- `TASK_GO_TO_BLOCKED_PILE` (pattern `TASK_GO_TO_BLOCKED_PILE`, va `0x0077163c`, xrefs 1)
- `TASK_GO_TO_CAMP` (pattern `TASK_GO_TO_CAMP`, va `0x00771788`, xrefs 1)
- `TASK_LEAVE_CAMP` (pattern `TASK_LEAVE_CAMP`, va `0x00771798`, xrefs 1)
- `TASK_GO_TO_EAT_BUILDING` (pattern `TASK_GO_TO_EAT_BUILDING`, va `0x00771a88`, xrefs 1)
- `TASK_GO_TO_REST_BUILDING` (pattern `TASK_GO_TO_REST_BUILDING`, va `0x00771aa0`, xrefs 1)
- `TASK_CHANGE_WORK_TIME_CAMP` (pattern `TASK_CHANGE_WORK_TIME_CAMP`, va `0x00771d24`, xrefs 1)
- `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS` (pattern `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS`, va `0x00771d9c`, xrefs 1)
- `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS` (pattern `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS`, va `0x00771dc4`, xrefs 1)
- `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS` (pattern `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS`, va `0x00771dec`, xrefs 1)
- `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS` (pattern `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS`, va `0x00771e14`, xrefs 1)
- `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS` (pattern `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS`, va `0x00771e3c`, xrefs 1)
- `SetWorkTaskListsPerCycle` (pattern `SetWorkTaskListsPerCycle`, va `0x00773e7c`, xrefs 0)
- `GetSettlersResidence` (pattern `GetSettlersResidence`, va `0x00773f28`, xrefs 0)
- `GetSettlersFarm` (pattern `GetSettlersFarm`, va `0x00773f40`, xrefs 0)
- `IsSettlerAtResidence` (pattern `IsSettlerAtResidence`, va `0x00773f60`, xrefs 0)
- `IsSettlerAtFarm` (pattern `IsSettlerAtFarm`, va `0x00773f78`, xrefs 0)
- `CheckSettlerPlacement` (pattern `CheckSettlerPlacement`, va `0x00774240`, xrefs 0)
- `GetNextWorkerWithoutFarmOrResidence` (pattern `GetNextWorkerWithoutFarmOrResidence`, va `0x007742f4`, xrefs 0)
- `GetNextWorkerWithoutFarm` (pattern `GetNextWorkerWithoutFarm`, va `0x00774318`, xrefs 0)
- `GetNextWorkerWithoutResidence` (pattern `GetNextWorkerWithoutResidence`, va `0x00774334`, xrefs 0)
- `IsPathingUsed` (pattern `IsPathingUsed`, va `0x00774420`, xrefs 1)
- `NextWaypointOrientation` (pattern `NextWaypointOrientation`, va `0x00774450`, xrefs 1)
- `NextWayPoint` (pattern `NextWayPoint`, va `0x00774468`, xrefs 1)
- `WaypointsCount` (pattern `WaypointsCount`, va `0x007744b4`, xrefs 1)
- `WayPoints` (pattern `WayPoints`, va `0x007744dc`, xrefs 2)
- `CoarsePath` (pattern `CoarsePath`, va `0x00774510`, xrefs 1)
- `FinePath` (pattern `FinePath`, va `0x0077451c`, xrefs 1)
- `MaximumDistanceWorkerToResidence` (pattern `MaximumDistanceWorkerToResidence`, va `0x0077569c`, xrefs 1)
- `MaximumDistanceWorkerToFarm` (pattern `MaximumDistanceWorkerToFarm`, va `0x007756c0`, xrefs 1)
- `ReAttachWorkerFrequency` (pattern `ReAttachWorkerFrequency`, va `0x007756f0`, xrefs 1)
- `EnterWorkerAlarmMode` (pattern `WorkerAlarmMode`, va `0x0077de6c`, xrefs 0)
- `QuitWorkerAlarmMode` (pattern `QuitWorkerAlarmMode`, va `0x0077de84`, xrefs 0)
- `UpdateBlocking` (pattern `UpdateBlocking`, va `0x007858cc`, xrefs 0)
- `.?AVCBuildBlockedOnlyPredicate@?A0xfc60cb98@GGL@@` (pattern `CBuildBlockedOnlyPredicate`, va `0x00810eec`, xrefs 0)
- `.?AVCWorkerFleeBehaviorProps@GGL@@` (pattern `CWorkerFleeBehaviorProps`, va `0x00813754`, xrefs 0)
- `.?AVCWorkerFleeBehavior@GGL@@` (pattern `CWorkerFleeBehavior`, va `0x008137a0`, xrefs 0)
- `.?AV?$THandler@$0BFAAO@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@` (pattern `CWorkerFleeBehavior`, va `0x008137c8`, xrefs 0)
- `.?AV?$THandler@$0BDABP@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@` (pattern `CWorkerFleeBehavior`, va `0x00813830`, xrefs 0)
- `.?AV?$THandler@$0IN@VCGLETaskArgs@EGL@@V12@VCWorkerFleeBehavior@GGL@@H@EGL@@` (pattern `CWorkerFleeBehavior`, va `0x008138a8`, xrefs 0)
- `.?AVCWorkerBehavior@GGL@@` (pattern `CWorkerBehavior`, va `0x00813b24`, xrefs 0)
- `.?AVCWorkerBehaviorProps@GGL@@` (pattern `CWorkerBehaviorProps`, va `0x00813b48`, xrefs 0)
- `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00813b90`, xrefs 0)
- `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00813be8`, xrefs 0)
- `.?AV?$THandler@$0DO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00813c50`, xrefs 0)
- `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00813ca8`, xrefs 0)
- `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00813d10`, xrefs 0)
- `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00813d78`, xrefs 0)
- `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00813de0`, xrefs 0)
- `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00813e48`, xrefs 0)
- `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00813eb0`, xrefs 0)
- `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00813f18`, xrefs 0)
- `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00813f80`, xrefs 0)
- `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00813fe8`, xrefs 0)
- `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814050`, xrefs 0)
- `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x008140b8`, xrefs 0)
- `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814120`, xrefs 0)
- `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814188`, xrefs 0)
- `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x008141f0`, xrefs 0)
- `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814258`, xrefs 0)
- `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x008142c0`, xrefs 0)
- `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814328`, xrefs 0)
- `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814390`, xrefs 0)
- `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x008143f8`, xrefs 0)
- `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814458`, xrefs 0)
- `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x008144b0`, xrefs 0)
- `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814508`, xrefs 0)
- `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814560`, xrefs 0)
- `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x008145b8`, xrefs 0)
- `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814610`, xrefs 0)
- `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814668`, xrefs 0)
- `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x008146c0`, xrefs 0)
- `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814718`, xrefs 0)
- `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814770`, xrefs 0)
- `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x008147c8`, xrefs 0)
- `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814820`, xrefs 0)
- `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814878`, xrefs 0)
- `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x008148d0`, xrefs 0)
- `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814928`, xrefs 0)
- `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814980`, xrefs 0)
- `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x008149e8`, xrefs 0)
- `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814a50`, xrefs 0)
- `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814ab8`, xrefs 0)
- `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814b20`, xrefs 0)
- `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814b78`, xrefs 0)
- `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814bd0`, xrefs 0)
- `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814c28`, xrefs 0)
- `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814c80`, xrefs 0)
- `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814cd8`, xrefs 0)
- `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814d30`, xrefs 0)
- `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814d88`, xrefs 0)
- `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814df0`, xrefs 0)
- `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814e48`, xrefs 0)
- `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814ea0`, xrefs 0)
- `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814ef8`, xrefs 0)
- `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814f50`, xrefs 0)
- `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00814fa8`, xrefs 0)
- `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00815008`, xrefs 0)
- `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00815070`, xrefs 0)
- `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x008150e0`, xrefs 0)
- `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00815150`, xrefs 0)
- `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x008151a8`, xrefs 0)
- `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00815200`, xrefs 0)
- `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815258`, xrefs 0)
- `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x008152b8`, xrefs 0)
- `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815318`, xrefs 0)
- `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815378`, xrefs 0)
- `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@` (pattern `CWorkerBehavior`, va `0x008153e8`, xrefs 0)
- `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815450`, xrefs 0)
- `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x008154c0`, xrefs 0)
- `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815530`, xrefs 0)
- `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x008155a0`, xrefs 0)
- `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x008155f0`, xrefs 0)
- `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815640`, xrefs 0)
- `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815690`, xrefs 0)
- `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x008156e0`, xrefs 0)
- `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815750`, xrefs 0)
- `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x008157c0`, xrefs 0)
- `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815810`, xrefs 0)
- `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815860`, xrefs 0)
- `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x008158d0`, xrefs 0)
- `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815940`, xrefs 0)
- `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x008159b0`, xrefs 0)
- `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815a20`, xrefs 0)
- `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815a80`, xrefs 0)
- `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815ae0`, xrefs 0)
- `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815b50`, xrefs 0)
- `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815bc0`, xrefs 0)
- `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815c20`, xrefs 0)
- `.?AV?$THandler@$0BDACC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815c90`, xrefs 0)
- `.?AV?$THandler@$0BDACF@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00815d00`, xrefs 0)
- `.?AV?$TStateHandler@VCWorkerBehavior@GGL@@@EGL@@` (pattern `CWorkerBehavior`, va `0x00815d60`, xrefs 0)
- `.?AVCWorkerAlarmModeBehaviorProps@GGL@@` (pattern `CWorkerAlarmModeBehaviorProps`, va `0x008164bc`, xrefs 0)
- `.?AVCWorkerAlarmModeBehavior@GGL@@` (pattern `WorkerAlarmMode`, va `0x008164ec`, xrefs 0)
- `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `WorkerAlarmMode`, va `0x00816518`, xrefs 0)
- `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `WorkerAlarmMode`, va `0x00816570`, xrefs 0)
- `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `WorkerAlarmMode`, va `0x008165c8`, xrefs 0)
- `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `WorkerAlarmMode`, va `0x00816630`, xrefs 0)
- `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `WorkerAlarmMode`, va `0x00816690`, xrefs 0)
- `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `WorkerAlarmMode`, va `0x008166f0`, xrefs 0)
- `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `WorkerAlarmMode`, va `0x00816750`, xrefs 0)
- `.?AVCPath@EGL@@` (pattern `CPath`, va `0x00818e6c`, xrefs 0)
- `.?AVCPath@GGL@@` (pattern `CPath`, va `0x00818e84`, xrefs 0)
- `.?AVCCamperBehavior@GGL@@` (pattern `CCamperBehavior`, va `0x00823728`, xrefs 0)
- `.?AVCUnblockedSquarePredicate@EGL@@` (pattern `CUnblockedSquarePredicate`, va `0x0082374c`, xrefs 0)
- `.?AVCCampBehaviorProperties@GGL@@` (pattern `CCampBehaviorProperties`, va `0x00823778`, xrefs 0)
- `.?AVCPotentialCampSitePredicate@GGL@@` (pattern `CPotentialCampSitePredicate`, va `0x008237a4`, xrefs 0)
- `.?AVCCamperBehaviorProperties@GGL@@` (pattern `CCamperBehaviorProperties`, va `0x008237d4`, xrefs 0)
- `.?AVCCampWithFreeSlotPredicate@GGL@@` (pattern `CCampWithFreeSlotPredicate`, va `0x00823800`, xrefs 0)
- `.?AV?$THandler@$0BDABA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCCampBehavior@GGL@@X@EGL@@` (pattern `CCampBehavior`, va `0x008238b0`, xrefs 0)
- `.?AV?$THandler@$0BDAAN@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCampBehavior@GGL@@X@EGL@@` (pattern `CCampBehavior`, va `0x00823920`, xrefs 0)
- `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@` (pattern `CCampBehavior`, va `0x00823990`, xrefs 0)
- `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@` (pattern `CCampBehavior`, va `0x008239f8`, xrefs 0)
- `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@` (pattern `CCampBehavior`, va `0x00823a58`, xrefs 0)
- `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@` (pattern `CCampBehavior`, va `0x00823ab4`, xrefs 0)
- `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@` (pattern `CCamperBehavior`, va `0x00823af0`, xrefs 0)
- `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@` (pattern `CCamperBehavior`, va `0x00823b48`, xrefs 0)
- `.?AV?$THandler@$0BDABC@VCEvent@BB@@V12@VCCamperBehavior@GGL@@X@EGL@@` (pattern `CCamperBehavior`, va `0x00823ba0`, xrefs 0)
- `.?AV?$THandler@$0BDABB@VCEvent@BB@@VCEvent1Entity@EGL@@VCCamperBehavior@GGL@@X@EGL@@` (pattern `CCamperBehavior`, va `0x00823bf0`, xrefs 0)
- `.?AVCCampBehavior@GGL@@` (pattern `CCampBehavior`, va `0x00823c50`, xrefs 0)
- `.?AVCCoarsePath@EGL@@` (pattern `CoarsePath`, va `0x00826338`, xrefs 0)
- `.?AVCAStar64@EGL@@` (pattern `CAStar64`, va `0x00829bbc`, xrefs 0)
- `.?AVCAStar64Normal@EGL@@` (pattern `CAStar64Normal`, va `0x00829bd8`, xrefs 0)
- `.?AVCBlockingStatusPredicate@EGL@@` (pattern `CBlockingStatusPredicate`, va `0x00835998`, xrefs 0)
- `.?AVCUnblockedInSectorPredicate@EGL@@` (pattern `CUnblockedInSectorPredicate`, va `0x00836768`, xrefs 0)
- `.?AVCUnblockedInLargeSectorPredicate@EGL@@` (pattern `CUnblockedInLargeSectorPredicate`, va `0x00836798`, xrefs 0)
- `.?AVCUnblockedAreasPredicate@EGL@@` (pattern `CUnblockedAreasPredicate`, va `0x008367cc`, xrefs 0)
- `.?AVCUnblockedBuildingAreasPredicate@EGL@@` (pattern `CUnblockedBuildingAreasPredicate`, va `0x008367f8`, xrefs 0)

## Functions

### 0x0049c2a4
- blocks=11, insns=98, edges=30, jcc=8, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004af71e at 0x0049c6f4)
- branch points:
  - 0x0049c2b2: je -> 0x0049c3bd (jcc_true) | ctx: 0x0049c2aa: push ebx ; 0x0049c2ab: call 0x49840a ; 0x0049c2b0: test al, al ; 0x0049c2b2: je 0x49c3bd
  - 0x0049c2b2: je -> 0x0049c2b8 (jcc_false) | ctx: 0x0049c2aa: push ebx ; 0x0049c2ab: call 0x49840a ; 0x0049c2b0: test al, al ; 0x0049c2b2: je 0x49c3bd
  - 0x0049c2d6: je -> 0x0049c3bd (jcc_true) | ctx: 0x0049c2cd: mov ebx, eax ; 0x0049c2cf: call 0x4faabd ; 0x0049c2d4: test al, al ; 0x0049c2d6: je 0x49c3bd
  - 0x0049c2d6: je -> 0x0049c2dc (jcc_false) | ctx: 0x0049c2cd: mov ebx, eax ; 0x0049c2cf: call 0x4faabd ; 0x0049c2d4: test al, al ; 0x0049c2d6: je 0x49c3bd
  - 0x0049c2e6: je -> 0x0049c3bd (jcc_true) | ctx: 0x0049c2dd: mov ecx, esi ; 0x0049c2df: call 0x4faae3 ; 0x0049c2e4: test eax, eax ; 0x0049c2e6: je 0x49c3bd
  - 0x0049c2e6: je -> 0x0049c2ec (jcc_false) | ctx: 0x0049c2dd: mov ecx, esi ; 0x0049c2df: call 0x4faae3 ; 0x0049c2e4: test eax, eax ; 0x0049c2e6: je 0x49c3bd
  - 0x0049c2f7: je -> 0x0049c3bd (jcc_true) | ctx: 0x0049c2f2: mov esi, eax ; 0x0049c2f4: test esi, esi ; 0x0049c2f6: pop ecx ; 0x0049c2f7: je 0x49c3bd
  - 0x0049c2f7: je -> 0x0049c2fd (jcc_false) | ctx: 0x0049c2f2: mov esi, eax ; 0x0049c2f4: test esi, esi ; 0x0049c2f6: pop ecx ; 0x0049c2f7: je 0x49c3bd
  - 0x0049c308: je -> 0x0049c38f (jcc_true) | ctx: 0x0049c300: call 0x4aac63 ; 0x0049c305: test eax, eax ; 0x0049c307: pop ecx ; 0x0049c308: je 0x49c38f
  - 0x0049c308: je -> 0x0049c30e (jcc_false) | ctx: 0x0049c300: call 0x4aac63 ; 0x0049c305: test eax, eax ; 0x0049c307: pop ecx ; 0x0049c308: je 0x49c38f
  - 0x0049c39b: je -> 0x0049c3bd (jcc_true) | ctx: 0x0049c391: lea ecx, [esi + 0x38] ; 0x0049c394: call 0x44b115 ; 0x0049c399: test eax, eax ; 0x0049c39b: je 0x49c3bd
  - 0x0049c39b: je -> 0x0049c39d (jcc_false) | ctx: 0x0049c391: lea ecx, [esi + 0x38] ; 0x0049c394: call 0x44b115 ; 0x0049c399: test eax, eax ; 0x0049c39b: je 0x49c3bd
  - 0x0049c31c: je -> 0x0049c3bd (jcc_true) | ctx: 0x0049c314: push eax ; 0x0049c315: call 0x4b0114 ; 0x0049c31a: test eax, eax ; 0x0049c31c: je 0x49c3bd
  - 0x0049c31c: je -> 0x0049c322 (jcc_false) | ctx: 0x0049c314: push eax ; 0x0049c315: call 0x4b0114 ; 0x0049c31a: test eax, eax ; 0x0049c31c: je 0x49c3bd
  - 0x0049c332: je -> 0x0049c3bd (jcc_true) | ctx: 0x0049c328: mov edi, eax ; 0x0049c32a: cmp byte ptr [edi + 0x13d], 0 ; 0x0049c331: pop ecx ; 0x0049c332: je 0x49c3bd
  - 0x0049c332: je -> 0x0049c338 (jcc_false) | ctx: 0x0049c328: mov edi, eax ; 0x0049c32a: cmp byte ptr [edi + 0x13d], 0 ; 0x0049c331: pop ecx ; 0x0049c332: je 0x49c3bd
  - 0x0049c38d: jmp -> 0x0049c3bd (jmp) | ctx: 0x0049c384: push eax ; 0x0049c385: lea ecx, [ebx + 0x5c] ; 0x0049c388: call 0x4a9791 ; 0x0049c38d: jmp 0x49c3bd

### 0x004a71d5
- blocks=3, insns=395, edges=14, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: NumBlockedPoints via `NumBlockedPoints` (string 0x0076e5ac, xref 0x004a7391)
  - string_xref: BlockingArea via `BlockingArea` (string 0x0076e5c0, xref 0x004a7365)
- branch points:
  - 0x004a71e2: jne -> 0x004a7785 (jcc_true) | ctx: 0x004a71d6: mov ebp, esp ; 0x004a71d8: sub esp, 0x24 ; 0x004a71db: test byte ptr [0x85e170], 1 ; 0x004a71e2: jne 0x4a7785
  - 0x004a71e2: jne -> 0x004a71e8 (jcc_false) | ctx: 0x004a71d6: mov ebp, esp ; 0x004a71d8: sub esp, 0x24 ; 0x004a71db: test byte ptr [0x85e170], 1 ; 0x004a71e2: jne 0x4a7785

### 0x004a7e8d
- blocks=3, insns=379, edges=24, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004a71d5 at 0x004a7eaa)
- branch points:
  - 0x004a7e9a: jne -> 0x004a8406 (jcc_true) | ctx: 0x004a7e8e: mov ebp, esp ; 0x004a7e90: sub esp, 0x24 ; 0x004a7e93: test byte ptr [0x85e5e4], 1 ; 0x004a7e9a: jne 0x4a8406
  - 0x004a7e9a: jne -> 0x004a7ea0 (jcc_false) | ctx: 0x004a7e8e: mov ebp, esp ; 0x004a7e90: sub esp, 0x24 ; 0x004a7e93: test byte ptr [0x85e5e4], 1 ; 0x004a7e9a: jne 0x4a8406

### 0x004a85a1
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x004a7e8d at 0x004a85b2)
- branch points:
  - 0x004a85a4: jne -> 0x004a85b0 (jcc_true) | ctx: 0x004a85a1: push edi ; 0x004a85a2: mov edi, ecx ; 0x004a85a4: jne 0x4a85b0
  - 0x004a85a4: jne -> 0x004a85a6 (jcc_false) | ctx: 0x004a85a1: push edi ; 0x004a85a2: mov edi, ecx ; 0x004a85a4: jne 0x4a85b0

### 0x004aa09a
- blocks=6, insns=48, edges=10, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCBuildBlockedOnlyPredicate@?A0xfc60cb98@GGL@@ slot 1 (target 0x004aa09a, vtable 0x0076ea58)
- branch points:
  - 0x004aa0f3: jne -> 0x004aa0fb (jcc_true) | ctx: 0x004aa0ef: pop esi ; 0x004aa0f0: test bl, bl ; 0x004aa0f2: pop ebx ; 0x004aa0f3: jne 0x4aa0fb
  - 0x004aa0f3: jne -> 0x004aa0f5 (jcc_false) | ctx: 0x004aa0ef: pop esi ; 0x004aa0f0: test bl, bl ; 0x004aa0f2: pop ebx ; 0x004aa0f3: jne 0x4aa0fb
  - 0x004aa0fd: je -> 0x004aa104 (jcc_true) | ctx: 0x004aa0fb: test al, al ; 0x004aa0fd: je 0x4aa104
  - 0x004aa0fd: je -> 0x004aa0ff (jcc_false) | ctx: 0x004aa0fb: test al, al ; 0x004aa0fd: je 0x4aa104
  - 0x004aa0f9: je -> 0x004aa104 (jcc_true) | ctx: 0x004aa0f5: cmp byte ptr [ebp - 2], 0 ; 0x004aa0f9: je 0x4aa104
  - 0x004aa0f9: je -> 0x004aa0fb (jcc_false) | ctx: 0x004aa0f5: cmp byte ptr [ebp - 2], 0 ; 0x004aa0f9: je 0x4aa104
  - 0x004aa102: jmp -> 0x004aa106 (jmp) | ctx: 0x004aa0ff: xor eax, eax ; 0x004aa101: inc eax ; 0x004aa102: jmp 0x4aa106

### 0x004adddb
- blocks=6, insns=88, edges=15, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 3 (calls 0x00579a40 at 0x004adfef)
- branch points:
  - 0x004ade8d: jne -> 0x004ade97 (jcc_true) | ctx: 0x004ade7e: mov byte ptr [esi + 0x11c], al ; 0x004ade84: mov edi, dword ptr [edi + 0x88] ; 0x004ade8a: cmp edi, 0x13 ; 0x004ade8d: jne 0x4ade97
  - 0x004ade8d: jne -> 0x004ade8f (jcc_false) | ctx: 0x004ade7e: mov byte ptr [esi + 0x11c], al ; 0x004ade84: mov edi, dword ptr [edi + 0x88] ; 0x004ade8a: cmp edi, 0x13 ; 0x004ade8d: jne 0x4ade97
  - 0x004adeb6: jmp -> 0x004adee0 (jmp) | ctx: 0x004adeab: mov dword ptr [ebp - 4], ebx ; 0x004adeae: call 0x44b46d ; 0x004adeb3: mov edi, dword ptr [ebp - 0x18] ; 0x004adeb6: jmp 0x4adee0
  - 0x004adeb6: jmp -> 0x004adee0 (jmp) | ctx: 0x004adeab: mov dword ptr [ebp - 4], ebx ; 0x004adeae: call 0x44b46d ; 0x004adeb3: mov edi, dword ptr [ebp - 0x18] ; 0x004adeb6: jmp 0x4adee0
  - 0x004adee3: jne -> 0x004adeb8 (jcc_true) | ctx: 0x004adee0: cmp edi, dword ptr [ebp - 0x14] ; 0x004adee3: jne 0x4adeb8
  - 0x004adee3: jne -> 0x004adee5 (jcc_false) | ctx: 0x004adee0: cmp edi, dword ptr [ebp - 0x14] ; 0x004adee3: jne 0x4adeb8
  - 0x004adee3: jne -> 0x004adeb8 (jcc_true) | ctx: 0x004aded6: mov dword ptr [ebp - 0x2c], 0x7620f0 ; 0x004adedd: add edi, 4 ; 0x004adee0: cmp edi, dword ptr [ebp - 0x14] ; 0x004adee3: jne 0x4adeb8
  - 0x004adee3: jne -> 0x004adee5 (jcc_false) | ctx: 0x004aded6: mov dword ptr [ebp - 0x2c], 0x7620f0 ; 0x004adedd: add edi, 4 ; 0x004adee0: cmp edi, dword ptr [ebp - 0x14] ; 0x004adee3: jne 0x4adeb8

### 0x004ae78f
- blocks=3, insns=70, edges=6, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004a71d5 at 0x004ae7ac)
  - caller_of_anchor_path: depth 2 (calls 0x004ae78f at 0x004ae9ec)
- branch points:
  - 0x004ae79c: jne -> 0x004ae87e (jcc_true) | ctx: 0x004ae790: mov ebp, esp ; 0x004ae792: sub esp, 0x24 ; 0x004ae795: test byte ptr [0x85f580], 1 ; 0x004ae79c: jne 0x4ae87e
  - 0x004ae79c: jne -> 0x004ae7a2 (jcc_false) | ctx: 0x004ae790: mov ebp, esp ; 0x004ae792: sub esp, 0x24 ; 0x004ae795: test byte ptr [0x85f580], 1 ; 0x004ae79c: jne 0x4ae87e

### 0x004af71e
- blocks=3, insns=273, edges=9, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: WorkerAlarmMode via `WorkerAlarmModeActive` (string 0x0076ee00, xref 0x004af9f0)
- branch points:
  - 0x004af72b: jne -> 0x004afaf0 (jcc_true) | ctx: 0x004af71f: mov ebp, esp ; 0x004af721: sub esp, 0x24 ; 0x004af724: test byte ptr [0x85fc30], 1 ; 0x004af72b: jne 0x4afaf0
  - 0x004af72b: jne -> 0x004af731 (jcc_false) | ctx: 0x004af71f: mov ebp, esp ; 0x004af721: sub esp, 0x24 ; 0x004af724: test byte ptr [0x85fc30], 1 ; 0x004af72b: jne 0x4afaf0

### 0x004afaff
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004af71e at 0x004afb10)
- branch points:
  - 0x004afb02: jne -> 0x004afb0e (jcc_true) | ctx: 0x004afaff: push edi ; 0x004afb00: mov edi, ecx ; 0x004afb02: jne 0x4afb0e
  - 0x004afb02: jne -> 0x004afb04 (jcc_false) | ctx: 0x004afaff: push edi ; 0x004afb00: mov edi, ecx ; 0x004afb02: jne 0x4afb0e

### 0x004b208c
- blocks=3, insns=1164, edges=26, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: WorkerFlightDistance via `WorkerFlightDistance` (string 0x0076f19c, xref 0x004b2d02)
  - string_xref: WorkTimeThresholdCampFire via `WorkTimeThresholdCampFire` (string 0x0076f384, xref 0x004b2964)
  - string_xref: WorkTimeThresholdResidence via `WorkTimeThresholdResidence` (string 0x0076f3a0, xref 0x004b2931)
  - string_xref: WorkTimeThresholdFarm via `WorkTimeThresholdFarm` (string 0x0076f3bc, xref 0x004b28fd)
  - string_xref: WorkTimeThresholdWork via `WorkTimeThresholdWork` (string 0x0076f3d4, xref 0x004b28c9)
  - string_xref: WorkTimeBase via `WorkTimeBase` (string 0x0076f3ec, xref 0x004b2897)
  - caller_of_anchor_path: depth 1 (calls 0x004b208c at 0x004b219d)
- branch points:
  - 0x004b2099: jne -> 0x004b30d8 (jcc_true) | ctx: 0x004b208d: mov ebp, esp ; 0x004b208f: sub esp, 0x24 ; 0x004b2092: test byte ptr [0x8614f0], 1 ; 0x004b2099: jne 0x4b30d8
  - 0x004b2099: jne -> 0x004b209f (jcc_false) | ctx: 0x004b208d: mov ebp, esp ; 0x004b208f: sub esp, 0x24 ; 0x004b2092: test byte ptr [0x8614f0], 1 ; 0x004b2099: jne 0x4b30d8

### 0x004b30e7
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004b208c at 0x004b30f8)
- branch points:
  - 0x004b30ea: jne -> 0x004b30f6 (jcc_true) | ctx: 0x004b30e7: push edi ; 0x004b30e8: mov edi, ecx ; 0x004b30ea: jne 0x4b30f6
  - 0x004b30ea: jne -> 0x004b30ec (jcc_false) | ctx: 0x004b30e7: push edi ; 0x004b30e8: mov edi, ecx ; 0x004b30ea: jne 0x4b30f6

### 0x004b43a9
- blocks=5, insns=42, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 3 (calls 0x00579a40 at 0x004b4703)
  - caller_of_anchor_path: depth 3 (calls 0x00579a40 at 0x004b487d)
  - caller_of_anchor_path: depth 3 (calls 0x004c7e91 at 0x004b4534)
- branch points:
  - 0x004b43e8: je -> 0x004b43f2 (jcc_true) | ctx: 0x004b43de: call 0x4b3fc0 ; 0x004b43e3: add esp, 0x14 ; 0x004b43e6: test al, al ; 0x004b43e8: je 0x4b43f2
  - 0x004b43e8: je -> 0x004b43ea (jcc_false) | ctx: 0x004b43de: call 0x4b3fc0 ; 0x004b43e3: add esp, 0x14 ; 0x004b43e6: test al, al ; 0x004b43e8: je 0x4b43f2
  - 0x004b43ec: jne -> 0x004b43f2 (jcc_true) | ctx: 0x004b43ea: test bl, bl ; 0x004b43ec: jne 0x4b43f2
  - 0x004b43ec: jne -> 0x004b43ee (jcc_false) | ctx: 0x004b43ea: test bl, bl ; 0x004b43ec: jne 0x4b43f2
  - 0x004b43f0: jmp -> 0x004b43f5 (jmp) | ctx: 0x004b43ee: xor eax, eax ; 0x004b43f0: jmp 0x4b43f5

### 0x004b7c82
- blocks=3, insns=412, edges=14, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: WorkerAlarmMode via `WorkerAlarmMode` (string 0x0076fda0, xref 0x004b7e98)
- branch points:
  - 0x004b7c8f: jne -> 0x004b825f (jcc_true) | ctx: 0x004b7c83: mov ebp, esp ; 0x004b7c85: sub esp, 0x24 ; 0x004b7c88: test byte ptr [0x862d34], 1 ; 0x004b7c8f: jne 0x4b825f
  - 0x004b7c8f: jne -> 0x004b7c95 (jcc_false) | ctx: 0x004b7c83: mov ebp, esp ; 0x004b7c85: sub esp, 0x24 ; 0x004b7c88: test byte ptr [0x862d34], 1 ; 0x004b7c8f: jne 0x4b825f

### 0x004b826e
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004b7c82 at 0x004b827f)
- branch points:
  - 0x004b8271: jne -> 0x004b827d (jcc_true) | ctx: 0x004b826e: push edi ; 0x004b826f: mov edi, ecx ; 0x004b8271: jne 0x4b827d
  - 0x004b8271: jne -> 0x004b8273 (jcc_false) | ctx: 0x004b826e: push edi ; 0x004b826f: mov edi, ecx ; 0x004b8271: jne 0x4b827d

### 0x004b8a24
- blocks=3, insns=138, edges=13, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x004ae78f at 0x004b8a41)
- branch points:
  - 0x004b8a31: jne -> 0x004b8c04 (jcc_true) | ctx: 0x004b8a25: mov ebp, esp ; 0x004b8a27: sub esp, 0x24 ; 0x004b8a2a: test byte ptr [0x863724], 1 ; 0x004b8a31: jne 0x4b8c04
  - 0x004b8a31: jne -> 0x004b8a37 (jcc_false) | ctx: 0x004b8a25: mov ebp, esp ; 0x004b8a27: sub esp, 0x24 ; 0x004b8a2a: test byte ptr [0x863724], 1 ; 0x004b8a31: jne 0x4b8c04

### 0x004b8c13
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 3 (calls 0x004b8a24 at 0x004b8c24)
- branch points:
  - 0x004b8c16: jne -> 0x004b8c22 (jcc_true) | ctx: 0x004b8c13: push edi ; 0x004b8c14: mov edi, ecx ; 0x004b8c16: jne 0x4b8c22
  - 0x004b8c16: jne -> 0x004b8c18 (jcc_false) | ctx: 0x004b8c13: push edi ; 0x004b8c14: mov edi, ecx ; 0x004b8c16: jne 0x4b8c22

### 0x004b9179
- blocks=3, insns=53, edges=6, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004af71e at 0x004b9196)
- branch points:
  - 0x004b9186: jne -> 0x004b9216 (jcc_true) | ctx: 0x004b917a: mov ebp, esp ; 0x004b917c: sub esp, 0x24 ; 0x004b917f: test byte ptr [0x8638c4], 1 ; 0x004b9186: jne 0x4b9216
  - 0x004b9186: jne -> 0x004b918c (jcc_false) | ctx: 0x004b917a: mov ebp, esp ; 0x004b917c: sub esp, 0x24 ; 0x004b917f: test byte ptr [0x8638c4], 1 ; 0x004b9186: jne 0x4b9216

### 0x004b9225
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x004b9179 at 0x004b9236)
- branch points:
  - 0x004b9228: jne -> 0x004b9234 (jcc_true) | ctx: 0x004b9225: push edi ; 0x004b9226: mov edi, ecx ; 0x004b9228: jne 0x4b9234
  - 0x004b9228: jne -> 0x004b922a (jcc_false) | ctx: 0x004b9225: push edi ; 0x004b9226: mov edi, ecx ; 0x004b9228: jne 0x4b9234

### 0x004bd1ef
- blocks=6, insns=47, edges=13, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 3 (calls 0x004c7e91 at 0x004bd38e)
- branch points:
  - 0x004bd20f: jl -> 0x004bd259 (jcc_true) | ctx: 0x004bd205: mov bl, 1 ; 0x004bd207: call 0x5758fb ; 0x004bd20c: cmp dword ptr [ebp + 8], eax ; 0x004bd20f: jl 0x4bd259
  - 0x004bd20f: jl -> 0x004bd211 (jcc_false) | ctx: 0x004bd205: mov bl, 1 ; 0x004bd207: call 0x5758fb ; 0x004bd20c: cmp dword ptr [ebp + 8], eax ; 0x004bd20f: jl 0x4bd259
  - 0x004bd21b: jg -> 0x004bd259 (jcc_true) | ctx: 0x004bd211: mov ecx, esi ; 0x004bd213: call 0x575904 ; 0x004bd218: cmp dword ptr [ebp + 8], eax ; 0x004bd21b: jg 0x4bd259
  - 0x004bd21b: jg -> 0x004bd21d (jcc_false) | ctx: 0x004bd211: mov ecx, esi ; 0x004bd213: call 0x575904 ; 0x004bd218: cmp dword ptr [ebp + 8], eax ; 0x004bd21b: jg 0x4bd259
  - 0x004bd231: je -> 0x004bd257 (jcc_true) | ctx: 0x004bd228: call 0x575895 ; 0x004bd22d: mov esi, eax ; 0x004bd22f: test esi, esi ; 0x004bd231: je 0x4bd257
  - 0x004bd231: je -> 0x004bd233 (jcc_false) | ctx: 0x004bd228: call 0x575895 ; 0x004bd22d: mov esi, eax ; 0x004bd22f: test esi, esi ; 0x004bd231: je 0x4bd257
  - 0x004bd255: jmp -> 0x004bd259 (jmp) | ctx: 0x004bd24b: push dword ptr [ebp - 8] ; 0x004bd24e: call 0x4bd183 ; 0x004bd253: mov bl, al ; 0x004bd255: jmp 0x4bd259

### 0x004c7d64
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x004ae78f at 0x004c7d75)
- branch points:
  - 0x004c7d67: jne -> 0x004c7d73 (jcc_true) | ctx: 0x004c7d64: push edi ; 0x004c7d65: mov edi, ecx ; 0x004c7d67: jne 0x4c7d73
  - 0x004c7d67: jne -> 0x004c7d69 (jcc_false) | ctx: 0x004c7d64: push edi ; 0x004c7d65: mov edi, ecx ; 0x004c7d67: jne 0x4c7d73

### 0x004c7e91
- blocks=4, insns=104, edges=15, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0058024d at 0x004c7f20)
- branch points:
  - 0x004c7f5b: je -> 0x004c7f76 (jcc_true) | ctx: 0x004c7f52: mov dword ptr [ebp + 8], ecx ; 0x004c7f55: test ecx, ecx ; 0x004c7f57: mov byte ptr [ebp - 4], 3 ; 0x004c7f5b: je 0x4c7f76
  - 0x004c7f5b: je -> 0x004c7f5d (jcc_false) | ctx: 0x004c7f52: mov dword ptr [ebp + 8], ecx ; 0x004c7f55: test ecx, ecx ; 0x004c7f57: mov byte ptr [ebp - 4], 3 ; 0x004c7f5b: je 0x4c7f76
  - 0x004c7f74: jmp -> 0x004c7f78 (jmp) | ctx: 0x004c7f68: push dword ptr [ebp + 0x10] ; 0x004c7f6b: mov byte ptr [ebp + 0xf], 1 ; 0x004c7f6f: call 0x5804c9 ; 0x004c7f74: jmp 0x4c7f78

### 0x004cb80b
- blocks=6, insns=122, edges=17, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerFleeBehavior@GGL@@ slot 1 (target 0x004cb959, vtable 0x007729fc)
  - rtti_vtable_method: .?AVCWorkerFleeBehavior@GGL@@ slot 4 (target 0x004cb988, vtable 0x007729fc)
  - rtti_vtable_method: .?AVCWorkerFleeBehavior@GGL@@ slot 5 (target 0x004cb988, vtable 0x007729fc)
- branch points:
  - 0x004cb850: jmp -> 0x004cb878 (jmp) | ctx: 0x004cb847: fld dword ptr [ebp - 4] ; 0x004cb84a: fsub dword ptr [ebp - 0xc] ; 0x004cb84d: fstp dword ptr [ebp - 4] ; 0x004cb850: jmp 0x4cb878
  - 0x004cb896: jne -> 0x004cb852 (jcc_true) | ctx: 0x004cb88e: push eax ; 0x004cb88f: call 0x4cb7b0 ; 0x004cb894: test al, al ; 0x004cb896: jne 0x4cb852
  - 0x004cb896: jne -> 0x004cb898 (jcc_false) | ctx: 0x004cb88e: push eax ; 0x004cb88f: call 0x4cb7b0 ; 0x004cb894: test al, al ; 0x004cb896: jne 0x4cb852
  - 0x004cb896: jne -> 0x004cb852 (jcc_true) | ctx: 0x004cb88e: push eax ; 0x004cb88f: call 0x4cb7b0 ; 0x004cb894: test al, al ; 0x004cb896: jne 0x4cb852
  - 0x004cb896: jne -> 0x004cb898 (jcc_false) | ctx: 0x004cb88e: push eax ; 0x004cb88f: call 0x4cb7b0 ; 0x004cb894: test al, al ; 0x004cb896: jne 0x4cb852
  - 0x004cb927: jne -> 0x004cb934 (jcc_true) | ctx: 0x004cb91d: mov dword ptr [esi + 4], eax ; 0x004cb920: call 0x5785bc ; 0x004cb925: test al, al ; 0x004cb927: jne 0x4cb934
  - 0x004cb927: jne -> 0x004cb929 (jcc_false) | ctx: 0x004cb91d: mov dword ptr [esi + 4], eax ; 0x004cb920: call 0x5785bc ; 0x004cb925: test al, al ; 0x004cb927: jne 0x4cb934

### 0x004cba77
- blocks=1, insns=9, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerFleeBehaviorProps@GGL@@ slot 1 (target 0x004cba94, vtable 0x00772a60)
- branch points:
  - none

### 0x004cbb29
- blocks=6, insns=43, edges=12, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004cb80b at 0x004cbb5f)
- branch points:
  - 0x004cbb3b: je -> 0x004cbb7c (jcc_true) | ctx: 0x004cbb35: call dword ptr [eax] ; 0x004cbb37: mov esi, eax ; 0x004cbb39: test esi, esi ; 0x004cbb3b: je 0x4cbb7c
  - 0x004cbb3b: je -> 0x004cbb3d (jcc_false) | ctx: 0x004cbb35: call dword ptr [eax] ; 0x004cbb37: mov esi, eax ; 0x004cbb39: test esi, esi ; 0x004cbb3b: je 0x4cbb7c
  - 0x004cbb4e: je -> 0x004cbb7b (jcc_true) | ctx: 0x004cbb45: mov ecx, ebx ; 0x004cbb47: call 0x4faabd ; 0x004cbb4c: test al, al ; 0x004cbb4e: je 0x4cbb7b
  - 0x004cbb4e: je -> 0x004cbb50 (jcc_false) | ctx: 0x004cbb45: mov ecx, ebx ; 0x004cbb47: call 0x4faabd ; 0x004cbb4c: test al, al ; 0x004cbb4e: je 0x4cbb7b
  - 0x004cbb5a: je -> 0x004cbb7b (jcc_true) | ctx: 0x004cbb51: mov ecx, ebx ; 0x004cbb53: call 0x4faae3 ; 0x004cbb58: test eax, eax ; 0x004cbb5a: je 0x4cbb7b
  - 0x004cbb5a: je -> 0x004cbb5c (jcc_false) | ctx: 0x004cbb51: mov ecx, ebx ; 0x004cbb53: call 0x4faae3 ; 0x004cbb58: test eax, eax ; 0x004cbb5a: je 0x4cbb7b

### 0x004cbbbf
- blocks=3, insns=53, edges=6, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerFleeBehavior@GGL@@ slot 3 (target 0x004cbc60, vtable 0x007729fc)
- branch points:
  - 0x004cbbcc: jne -> 0x004cbc59 (jcc_true) | ctx: 0x004cbbc0: mov ebp, esp ; 0x004cbbc2: sub esp, 0x24 ; 0x004cbbc5: test byte ptr [0x86a824], 1 ; 0x004cbbcc: jne 0x4cbc59
  - 0x004cbbcc: jne -> 0x004cbbd2 (jcc_false) | ctx: 0x004cbbc0: mov ebp, esp ; 0x004cbbc2: sub esp, 0x24 ; 0x004cbbc5: test byte ptr [0x86a824], 1 ; 0x004cbbcc: jne 0x4cbc59

### 0x004cbe29
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004cbbbf at 0x004cbe3a)
- branch points:
  - 0x004cbe2c: jne -> 0x004cbe38 (jcc_true) | ctx: 0x004cbe29: push edi ; 0x004cbe2a: mov edi, ecx ; 0x004cbe2c: jne 0x4cbe38
  - 0x004cbe2c: jne -> 0x004cbe2e (jcc_false) | ctx: 0x004cbe29: push edi ; 0x004cbe2a: mov edi, ecx ; 0x004cbe2c: jne 0x4cbe38

### 0x004cc478
- blocks=1, insns=23, edges=5, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerBehavior@GGL@@ slot 1 (target 0x004cc51c, vtable 0x00772b30)
  - rtti_vtable_method: .?AVCWorkerBehavior@GGL@@ slot 5 (target 0x004cc524, vtable 0x00772b30)
- branch points:
  - none

### 0x004cc9c4
- blocks=1, insns=38, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerBehaviorProps@GGL@@ slot 1 (target 0x004cca3f, vtable 0x00772b90)
- branch points:
  - none

### 0x004cf5c3
- blocks=5, insns=32, edges=8, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004cf6d6 at 0x004cf69d)
- branch points:
  - 0x004cf5ca: jne -> 0x004cf613 (jcc_true) | ctx: 0x004cf5c3: push edi ; 0x004cf5c4: mov edi, ecx ; 0x004cf5c6: cmp byte ptr [edi + 0x3d], 0 ; 0x004cf5ca: jne 0x4cf613
  - 0x004cf5ca: jne -> 0x004cf5cc (jcc_false) | ctx: 0x004cf5c3: push edi ; 0x004cf5c4: mov edi, ecx ; 0x004cf5c6: cmp byte ptr [edi + 0x3d], 0 ; 0x004cf5ca: jne 0x4cf613
  - 0x004cf5fb: je -> 0x004cf612 (jcc_true) | ctx: 0x004cf5f1: lea ecx, [eax + 0x5c] ; 0x004cf5f4: call 0x4a971f ; 0x004cf5f9: test al, al ; 0x004cf5fb: je 0x4cf612
  - 0x004cf5fb: je -> 0x004cf5fd (jcc_false) | ctx: 0x004cf5f1: lea ecx, [eax + 0x5c] ; 0x004cf5f4: call 0x4a971f ; 0x004cf5f9: test al, al ; 0x004cf5fb: je 0x4cf612

### 0x004cf6d6
- blocks=31, insns=235, edges=71, jcc=16, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerBehavior@GGL@@ slot 4 (target 0x004cf8f9, vtable 0x00772b30)
- branch points:
  - 0x004cf6e7: je -> 0x004cf8eb (jcc_true) | ctx: 0x004cf6dc: mov eax, dword ptr [eax*4 + 0x772ac8] ; 0x004cf6e3: sub eax, 0 ; 0x004cf6e6: push edi ; 0x004cf6e7: je 0x4cf8eb
  - 0x004cf6e7: je -> 0x004cf6ed (jcc_false) | ctx: 0x004cf6dc: mov eax, dword ptr [eax*4 + 0x772ac8] ; 0x004cf6e3: sub eax, 0 ; 0x004cf6e6: push edi ; 0x004cf6e7: je 0x4cf8eb
  - 0x004cf6ee: je -> 0x004cf872 (jcc_true) | ctx: 0x004cf6ed: dec eax ; 0x004cf6ee: je 0x4cf872
  - 0x004cf6ee: je -> 0x004cf6f4 (jcc_false) | ctx: 0x004cf6ed: dec eax ; 0x004cf6ee: je 0x4cf872
  - 0x004cf879: je -> 0x004cf8c8 (jcc_true) | ctx: 0x004cf872: call 0x4cf468 ; 0x004cf877: test al, al ; 0x004cf879: je 0x4cf8c8
  - 0x004cf879: je -> 0x004cf87b (jcc_false) | ctx: 0x004cf872: call 0x4cf468 ; 0x004cf877: test al, al ; 0x004cf879: je 0x4cf8c8
  - 0x004cf6f5: je -> 0x004cf7d3 (jcc_true) | ctx: 0x004cf6f4: dec eax ; 0x004cf6f5: je 0x4cf7d3
  - 0x004cf6f5: je -> 0x004cf6fb (jcc_false) | ctx: 0x004cf6f4: dec eax ; 0x004cf6f5: je 0x4cf7d3
  - 0x004cf8cc: jne -> 0x004cf8eb (jcc_true) | ctx: 0x004cf8c8: cmp byte ptr [esi + 0x3d], 0 ; 0x004cf8cc: jne 0x4cf8eb
  - 0x004cf8cc: jne -> 0x004cf8ce (jcc_false) | ctx: 0x004cf8c8: cmp byte ptr [esi + 0x3d], 0 ; 0x004cf8cc: jne 0x4cf8eb
  - 0x004cf8c6: jmp -> 0x004cf8e6 (jmp) | ctx: 0x004cf8be: call 0x4ce75a ; 0x004cf8c3: push eax ; 0x004cf8c4: mov ecx, edi ; 0x004cf8c6: jmp 0x4cf8e6
  - 0x004cf7e2: je -> 0x004cf845 (jcc_true) | ctx: 0x004cf7d9: test al, al ; 0x004cf7db: mov eax, dword ptr [0x85a3e0] ; 0x004cf7e0: mov ecx, esi ; 0x004cf7e2: je 0x4cf845
  - 0x004cf7e2: je -> 0x004cf7e4 (jcc_false) | ctx: 0x004cf7d9: test al, al ; 0x004cf7db: mov eax, dword ptr [0x85a3e0] ; 0x004cf7e0: mov ecx, esi ; 0x004cf7e2: je 0x4cf845
  - 0x004cf6fc: je -> 0x004cf708 (jcc_true) | ctx: 0x004cf6fb: dec eax ; 0x004cf6fc: je 0x4cf708
  - 0x004cf6fc: je -> 0x004cf6fe (jcc_false) | ctx: 0x004cf6fb: dec eax ; 0x004cf6fc: je 0x4cf708
  - 0x004cf863: jle -> 0x004cf868 (jcc_true) | ctx: 0x004cf858: mov dword ptr [esi + 0x14], eax ; 0x004cf85b: call 0x4ce866 ; 0x004cf860: cmp dword ptr [esi + 0x14], eax ; 0x004cf863: jle 0x4cf868
  - 0x004cf863: jle -> 0x004cf865 (jcc_false) | ctx: 0x004cf858: mov dword ptr [esi + 0x14], eax ; 0x004cf85b: call 0x4ce866 ; 0x004cf860: cmp dword ptr [esi + 0x14], eax ; 0x004cf863: jle 0x4cf868
  - 0x004cf802: jle -> 0x004cf807 (jcc_true) | ctx: 0x004cf7f7: mov dword ptr [esi + 0x14], eax ; 0x004cf7fa: call 0x4ce866 ; 0x004cf7ff: cmp dword ptr [esi + 0x14], eax ; 0x004cf802: jle 0x4cf807
  - 0x004cf802: jle -> 0x004cf804 (jcc_false) | ctx: 0x004cf7f7: mov dword ptr [esi + 0x14], eax ; 0x004cf7fa: call 0x4ce866 ; 0x004cf7ff: cmp dword ptr [esi + 0x14], eax ; 0x004cf802: jle 0x4cf807
  - 0x004cf717: je -> 0x004cf790 (jcc_true) | ctx: 0x004cf70e: test al, al ; 0x004cf710: mov eax, dword ptr [0x85a3e0] ; 0x004cf715: mov ecx, esi ; 0x004cf717: je 0x4cf790
  - 0x004cf717: je -> 0x004cf719 (jcc_false) | ctx: 0x004cf70e: test al, al ; 0x004cf710: mov eax, dword ptr [0x85a3e0] ; 0x004cf715: mov ecx, esi ; 0x004cf717: je 0x4cf790
  - 0x004cf703: jmp -> 0x004cf8eb (jmp) | ctx: 0x004cf6fe: call 0x4cf61f ; 0x004cf703: jmp 0x4cf8eb
  - 0x004cf870: jmp -> 0x004cf8dd (jmp) | ctx: 0x004cf868: mov eax, dword ptr [esi + 0x1c] ; 0x004cf86b: push 1 ; 0x004cf86d: push dword ptr [eax + 0x24] ; 0x004cf870: jmp 0x4cf8dd
  - 0x004cf870: jmp -> 0x004cf8dd (jmp) | ctx: 0x004cf868: mov eax, dword ptr [esi + 0x1c] ; 0x004cf86b: push 1 ; 0x004cf86d: push dword ptr [eax + 0x24] ; 0x004cf870: jmp 0x4cf8dd
  - 0x004cf843: jmp -> 0x004cf8c4 (jmp) | ctx: 0x004cf837: push 1 ; 0x004cf839: mov dword ptr [ebp - 0x1c], 0x7620f0 ; 0x004cf840: push dword ptr [eax + 0x20] ; 0x004cf843: jmp 0x4cf8c4
  - 0x004cf843: jmp -> 0x004cf8c4 (jmp) | ctx: 0x004cf837: push 1 ; 0x004cf839: mov dword ptr [ebp - 0x1c], 0x7620f0 ; 0x004cf840: push dword ptr [eax + 0x20] ; 0x004cf843: jmp 0x4cf8c4
  - 0x004cf7ae: jle -> 0x004cf7b3 (jcc_true) | ctx: 0x004cf7a3: mov dword ptr [esi + 0x14], eax ; 0x004cf7a6: call 0x4ce866 ; 0x004cf7ab: cmp dword ptr [esi + 0x14], eax ; 0x004cf7ae: jle 0x4cf7b3
  - 0x004cf7ae: jle -> 0x004cf7b0 (jcc_false) | ctx: 0x004cf7a3: mov dword ptr [esi + 0x14], eax ; 0x004cf7a6: call 0x4ce866 ; 0x004cf7ab: cmp dword ptr [esi + 0x14], eax ; 0x004cf7ae: jle 0x4cf7b3
  - 0x004cf737: jle -> 0x004cf73c (jcc_true) | ctx: 0x004cf72c: mov dword ptr [esi + 0x14], eax ; 0x004cf72f: call 0x4ce866 ; 0x004cf734: cmp dword ptr [esi + 0x14], eax ; 0x004cf737: jle 0x4cf73c
  - 0x004cf737: jle -> 0x004cf739 (jcc_false) | ctx: 0x004cf72c: mov dword ptr [esi + 0x14], eax ; 0x004cf72f: call 0x4ce866 ; 0x004cf734: cmp dword ptr [esi + 0x14], eax ; 0x004cf737: jle 0x4cf73c
  - 0x004cf8c6: jmp -> 0x004cf8e6 (jmp) | ctx: 0x004cf8c4: mov ecx, edi ; 0x004cf8c6: jmp 0x4cf8e6
  - 0x004cf7c1: jge -> 0x004cf7c6 (jcc_true) | ctx: 0x004cf7b3: mov eax, dword ptr [0x85a3e0] ; 0x004cf7b8: mov eax, dword ptr [eax + 0x12c] ; 0x004cf7be: cmp dword ptr [esi + 0x14], eax ; 0x004cf7c1: jge 0x4cf7c6
  - 0x004cf7c1: jge -> 0x004cf7c3 (jcc_false) | ctx: 0x004cf7b3: mov eax, dword ptr [0x85a3e0] ; 0x004cf7b8: mov eax, dword ptr [eax + 0x12c] ; 0x004cf7be: cmp dword ptr [esi + 0x14], eax ; 0x004cf7c1: jge 0x4cf7c6
  - 0x004cf7c1: jge -> 0x004cf7c6 (jcc_true) | ctx: 0x004cf7b3: mov eax, dword ptr [0x85a3e0] ; 0x004cf7b8: mov eax, dword ptr [eax + 0x12c] ; 0x004cf7be: cmp dword ptr [esi + 0x14], eax ; 0x004cf7c1: jge 0x4cf7c6
  - 0x004cf7c1: jge -> 0x004cf7c3 (jcc_false) | ctx: 0x004cf7b3: mov eax, dword ptr [0x85a3e0] ; 0x004cf7b8: mov eax, dword ptr [eax + 0x12c] ; 0x004cf7be: cmp dword ptr [esi + 0x14], eax ; 0x004cf7c1: jge 0x4cf7c6
  - 0x004cf74a: jge -> 0x004cf74f (jcc_true) | ctx: 0x004cf73c: mov eax, dword ptr [0x85a3e0] ; 0x004cf741: mov eax, dword ptr [eax + 0x12c] ; 0x004cf747: cmp dword ptr [esi + 0x14], eax ; 0x004cf74a: jge 0x4cf74f
  - 0x004cf74a: jge -> 0x004cf74c (jcc_false) | ctx: 0x004cf73c: mov eax, dword ptr [0x85a3e0] ; 0x004cf741: mov eax, dword ptr [eax + 0x12c] ; 0x004cf747: cmp dword ptr [esi + 0x14], eax ; 0x004cf74a: jge 0x4cf74f
  - 0x004cf74a: jge -> 0x004cf74f (jcc_true) | ctx: 0x004cf73c: mov eax, dword ptr [0x85a3e0] ; 0x004cf741: mov eax, dword ptr [eax + 0x12c] ; 0x004cf747: cmp dword ptr [esi + 0x14], eax ; 0x004cf74a: jge 0x4cf74f
  - 0x004cf74a: jge -> 0x004cf74c (jcc_false) | ctx: 0x004cf73c: mov eax, dword ptr [0x85a3e0] ; 0x004cf741: mov eax, dword ptr [eax + 0x12c] ; 0x004cf747: cmp dword ptr [esi + 0x14], eax ; 0x004cf74a: jge 0x4cf74f
  - 0x004cf7ce: jmp -> 0x004cf8dd (jmp) | ctx: 0x004cf7c6: mov eax, dword ptr [esi + 0x1c] ; 0x004cf7c9: push 1 ; 0x004cf7cb: push dword ptr [eax + 0x30] ; 0x004cf7ce: jmp 0x4cf8dd
  - 0x004cf7ce: jmp -> 0x004cf8dd (jmp) | ctx: 0x004cf7c6: mov eax, dword ptr [esi + 0x1c] ; 0x004cf7c9: push 1 ; 0x004cf7cb: push dword ptr [eax + 0x30] ; 0x004cf7ce: jmp 0x4cf8dd
  - 0x004cf78b: jmp -> 0x004cf8c4 (jmp) | ctx: 0x004cf77f: push 1 ; 0x004cf781: mov dword ptr [ebp - 0x14], 0x7620f0 ; 0x004cf788: push dword ptr [eax + 0x2c] ; 0x004cf78b: jmp 0x4cf8c4
  - 0x004cf78b: jmp -> 0x004cf8c4 (jmp) | ctx: 0x004cf77f: push 1 ; 0x004cf781: mov dword ptr [ebp - 0x14], 0x7620f0 ; 0x004cf788: push dword ptr [eax + 0x2c] ; 0x004cf78b: jmp 0x4cf8c4

### 0x004cfa6f
- blocks=3, insns=15, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004cf6d6 at 0x004cfa72)
- branch points:
  - 0x004cfa7b: jne -> 0x004cfa84 (jcc_true) | ctx: 0x004cfa70: mov esi, ecx ; 0x004cfa72: call 0x4cf6c9 ; 0x004cfa77: cmp byte ptr [esi + 0x3d], 0 ; 0x004cfa7b: jne 0x4cfa84
  - 0x004cfa7b: jne -> 0x004cfa7d (jcc_false) | ctx: 0x004cfa70: mov esi, ecx ; 0x004cfa72: call 0x4cf6c9 ; 0x004cfa77: cmp byte ptr [esi + 0x3d], 0 ; 0x004cfa7b: jne 0x4cfa84

### 0x004cfacf
- blocks=7, insns=90, edges=15, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x004cfa6f at 0x004cfad2)
- branch points:
  - 0x004cfad9: jne -> 0x004cfb75 (jcc_true) | ctx: 0x004cfad0: mov esi, ecx ; 0x004cfad2: call 0x4cfa8b ; 0x004cfad7: test al, al ; 0x004cfad9: jne 0x4cfb75
  - 0x004cfad9: jne -> 0x004cfadf (jcc_false) | ctx: 0x004cfad0: mov esi, ecx ; 0x004cfad2: call 0x4cfa8b ; 0x004cfad7: test al, al ; 0x004cfad9: jne 0x4cfb75
  - 0x004cfb46: jne -> 0x004cfb73 (jcc_true) | ctx: 0x004cfb3b: fcomp dword ptr [0x763420] ; 0x004cfb41: fnstsw ax ; 0x004cfb43: test ah, 0x41 ; 0x004cfb46: jne 0x4cfb73
  - 0x004cfb46: jne -> 0x004cfb48 (jcc_false) | ctx: 0x004cfb3b: fcomp dword ptr [0x763420] ; 0x004cfb41: fnstsw ax ; 0x004cfb43: test ah, 0x41 ; 0x004cfb46: jne 0x4cfb73
  - 0x004cfb56: jnp -> 0x004cfb5b (jcc_true) | ctx: 0x004cfb4e: fnstsw ax ; 0x004cfb50: test ah, 5 ; 0x004cfb53: lea eax, [ebp - 8] ; 0x004cfb56: jnp 0x4cfb5b
  - 0x004cfb56: jnp -> 0x004cfb58 (jcc_false) | ctx: 0x004cfb4e: fnstsw ax ; 0x004cfb50: test ah, 5 ; 0x004cfb53: lea eax, [ebp - 8] ; 0x004cfb56: jnp 0x4cfb5b

### 0x004cfb89
- blocks=5, insns=43, edges=9, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x004cfa6f at 0x004cfb8c)
- branch points:
  - 0x004cfb93: jne -> 0x004cfbec (jcc_true) | ctx: 0x004cfb8a: mov esi, ecx ; 0x004cfb8c: call 0x4cfa8b ; 0x004cfb91: test al, al ; 0x004cfb93: jne 0x4cfbec
  - 0x004cfb93: jne -> 0x004cfb95 (jcc_false) | ctx: 0x004cfb8a: mov esi, ecx ; 0x004cfb8c: call 0x4cfa8b ; 0x004cfb91: test al, al ; 0x004cfb93: jne 0x4cfbec
  - 0x004cfba3: jne -> 0x004cfbec (jcc_true) | ctx: 0x004cfb98: fcomp dword ptr [0x763420] ; 0x004cfb9e: fnstsw ax ; 0x004cfba0: test ah, 0x41 ; 0x004cfba3: jne 0x4cfbec
  - 0x004cfba3: jne -> 0x004cfba5 (jcc_false) | ctx: 0x004cfb98: fcomp dword ptr [0x763420] ; 0x004cfb9e: fnstsw ax ; 0x004cfba0: test ah, 0x41 ; 0x004cfba3: jne 0x4cfbec
  - 0x004cfbac: je -> 0x004cfbec (jcc_true) | ctx: 0x004cfba5: mov eax, dword ptr [esi + 0x1c] ; 0x004cfba8: cmp dword ptr [eax + 0x64], 0 ; 0x004cfbac: je 0x4cfbec
  - 0x004cfbac: je -> 0x004cfbae (jcc_false) | ctx: 0x004cfba5: mov eax, dword ptr [esi + 0x1c] ; 0x004cfba8: cmp dword ptr [eax + 0x64], 0 ; 0x004cfbac: je 0x4cfbec

### 0x004cfc0a
- blocks=6, insns=71, edges=18, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x004cfa6f at 0x004cfc0d)
- branch points:
  - 0x004cfc14: jne -> 0x004cfc76 (jcc_true) | ctx: 0x004cfc0b: mov edi, ecx ; 0x004cfc0d: call 0x4cfa8b ; 0x004cfc12: test al, al ; 0x004cfc14: jne 0x4cfc76
  - 0x004cfc14: jne -> 0x004cfc16 (jcc_false) | ctx: 0x004cfc0b: mov edi, ecx ; 0x004cfc0d: call 0x4cfa8b ; 0x004cfc12: test al, al ; 0x004cfc14: jne 0x4cfc76
  - 0x004cfc1f: je -> 0x004cfc76 (jcc_true) | ctx: 0x004cfc16: mov ecx, edi ; 0x004cfc18: call 0x4cc751 ; 0x004cfc1d: test al, al ; 0x004cfc1f: je 0x4cfc76
  - 0x004cfc1f: je -> 0x004cfc21 (jcc_false) | ctx: 0x004cfc16: mov ecx, edi ; 0x004cfc18: call 0x4cc751 ; 0x004cfc1d: test al, al ; 0x004cfc1f: je 0x4cfc76
  - 0x004cfc3a: je -> 0x004cfc52 (jcc_true) | ctx: 0x004cfc31: call 0x44b115 ; 0x004cfc36: mov esi, eax ; 0x004cfc38: test esi, esi ; 0x004cfc3a: je 0x4cfc52
  - 0x004cfc3a: je -> 0x004cfc3c (jcc_false) | ctx: 0x004cfc31: call 0x44b115 ; 0x004cfc36: mov esi, eax ; 0x004cfc38: test esi, esi ; 0x004cfc3a: je 0x4cfc52

### 0x004cfc94
- blocks=7, insns=55, edges=16, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x004cfa6f at 0x004cfc97)
- branch points:
  - 0x004cfc9e: jne -> 0x004cfcfa (jcc_true) | ctx: 0x004cfc95: mov edi, ecx ; 0x004cfc97: call 0x4cfa8b ; 0x004cfc9c: test al, al ; 0x004cfc9e: jne 0x4cfcfa
  - 0x004cfc9e: jne -> 0x004cfca0 (jcc_false) | ctx: 0x004cfc95: mov edi, ecx ; 0x004cfc97: call 0x4cfa8b ; 0x004cfc9c: test al, al ; 0x004cfc9e: jne 0x4cfcfa
  - 0x004cfca9: je -> 0x004cfcfa (jcc_true) | ctx: 0x004cfca0: mov ecx, edi ; 0x004cfca2: call 0x4cc751 ; 0x004cfca7: test al, al ; 0x004cfca9: je 0x4cfcfa
  - 0x004cfca9: je -> 0x004cfcab (jcc_false) | ctx: 0x004cfca0: mov ecx, edi ; 0x004cfca2: call 0x4cc751 ; 0x004cfca7: test al, al ; 0x004cfca9: je 0x4cfcfa
  - 0x004cfcc1: je -> 0x004cfcfa (jcc_true) | ctx: 0x004cfcb7: lea ecx, [eax + 0x1c] ; 0x004cfcba: call 0x44b115 ; 0x004cfcbf: test eax, eax ; 0x004cfcc1: je 0x4cfcfa
  - 0x004cfcc1: je -> 0x004cfcc3 (jcc_false) | ctx: 0x004cfcb7: lea ecx, [eax + 0x1c] ; 0x004cfcba: call 0x44b115 ; 0x004cfcbf: test eax, eax ; 0x004cfcc1: je 0x4cfcfa
  - 0x004cfcd4: je -> 0x004cfcf9 (jcc_true) | ctx: 0x004cfccb: call 0x4faae3 ; 0x004cfcd0: mov esi, eax ; 0x004cfcd2: test esi, esi ; 0x004cfcd4: je 0x4cfcf9
  - 0x004cfcd4: je -> 0x004cfcd6 (jcc_false) | ctx: 0x004cfccb: call 0x4faae3 ; 0x004cfcd0: mov esi, eax ; 0x004cfcd2: test esi, esi ; 0x004cfcd4: je 0x4cfcf9

### 0x004d0062
- blocks=6, insns=46, edges=11, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x004cfa6f at 0x004d0065)
- branch points:
  - 0x004d006c: je -> 0x004d0072 (jcc_true) | ctx: 0x004d0063: mov esi, ecx ; 0x004d0065: call 0x4cfa8b ; 0x004d006a: test al, al ; 0x004d006c: je 0x4d0072
  - 0x004d006c: je -> 0x004d006e (jcc_false) | ctx: 0x004d0063: mov esi, ecx ; 0x004d0065: call 0x4cfa8b ; 0x004d006a: test al, al ; 0x004d006c: je 0x4d0072
  - 0x004d009e: jne -> 0x004d00b1 (jcc_true) | ctx: 0x004d0095: mov ecx, eax ; 0x004d0097: call dword ptr [edx + 0x40] ; 0x004d009a: cmp dword ptr [ebp - 0x10], 0 ; 0x004d009e: jne 0x4d00b1
  - 0x004d009e: jne -> 0x004d00a0 (jcc_false) | ctx: 0x004d0095: mov ecx, eax ; 0x004d0097: call dword ptr [edx + 0x40] ; 0x004d009a: cmp dword ptr [ebp - 0x10], 0 ; 0x004d009e: jne 0x4d00b1
  - 0x004d0070: jmp -> 0x004d00c7 (jmp) | ctx: 0x004d006e: xor eax, eax ; 0x004d0070: jmp 0x4d00c7
  - 0x004d00af: jmp -> 0x004d00c7 (jmp) | ctx: 0x004d00aa: setg al ; 0x004d00ad: dec eax ; 0x004d00ae: dec eax ; 0x004d00af: jmp 0x4d00c7

### 0x004d00e2
- blocks=3, insns=27, edges=5, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x004cfa6f at 0x004d00e5)
- branch points:
  - 0x004d00ec: jne -> 0x004d0112 (jcc_true) | ctx: 0x004d00e3: mov esi, ecx ; 0x004d00e5: call 0x4cfa8b ; 0x004d00ea: test al, al ; 0x004d00ec: jne 0x4d0112
  - 0x004d00ec: jne -> 0x004d00ee (jcc_false) | ctx: 0x004d00e3: mov esi, ecx ; 0x004d00e5: call 0x4cfa8b ; 0x004d00ea: test al, al ; 0x004d00ec: jne 0x4d0112

### 0x004d0130
- blocks=3, insns=30, edges=5, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x004cfa6f at 0x004d0133)
  - caller_of_anchor_path: depth 2 (calls 0x004cfa6f at 0x004d018a)
- branch points:
  - 0x004d013a: jne -> 0x004d0169 (jcc_true) | ctx: 0x004d0131: mov esi, ecx ; 0x004d0133: call 0x4cfa8b ; 0x004d0138: test al, al ; 0x004d013a: jne 0x4d0169
  - 0x004d013a: jne -> 0x004d013c (jcc_false) | ctx: 0x004d0131: mov esi, ecx ; 0x004d0133: call 0x4cfa8b ; 0x004d0138: test al, al ; 0x004d013a: jne 0x4d0169

### 0x004d02f3
- blocks=1, insns=11, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerBehavior@GGL@@ slot 3 (target 0x004d030d, vtable 0x00772b30)
- branch points:
  - none

### 0x004d2925
- blocks=7, insns=48, edges=15, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehavior@GGL@@ slot 1 (target 0x004d2c8b, vtable 0x007734dc)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehavior@GGL@@ slot 5 (target 0x004d2c93, vtable 0x007734dc)
- branch points:
  - 0x004d292c: jne -> 0x004d2995 (jcc_true) | ctx: 0x004d2925: push edi ; 0x004d2926: mov edi, ecx ; 0x004d2928: cmp dword ptr [edi + 0x44], 9 ; 0x004d292c: jne 0x4d2995
  - 0x004d292c: jne -> 0x004d292e (jcc_false) | ctx: 0x004d2925: push edi ; 0x004d2926: mov edi, ecx ; 0x004d2928: cmp dword ptr [edi + 0x44], 9 ; 0x004d292c: jne 0x4d2995
  - 0x004d2942: jne -> 0x004d2995 (jcc_true) | ctx: 0x004d2938: lea ecx, [eax + 0x1c] ; 0x004d293b: call 0x44b115 ; 0x004d2940: test eax, eax ; 0x004d2942: jne 0x4d2995
  - 0x004d2942: jne -> 0x004d2944 (jcc_false) | ctx: 0x004d2938: lea ecx, [eax + 0x1c] ; 0x004d293b: call 0x44b115 ; 0x004d2940: test eax, eax ; 0x004d2942: jne 0x4d2995
  - 0x004d2954: je -> 0x004d2994 (jcc_true) | ctx: 0x004d294e: call dword ptr [eax] ; 0x004d2950: mov ebx, eax ; 0x004d2952: test ebx, ebx ; 0x004d2954: je 0x4d2994
  - 0x004d2954: je -> 0x004d2956 (jcc_false) | ctx: 0x004d294e: call dword ptr [eax] ; 0x004d2950: mov ebx, eax ; 0x004d2952: test ebx, ebx ; 0x004d2954: je 0x4d2994
  - 0x004d2964: je -> 0x004d2994 (jcc_true) | ctx: 0x004d295c: push ebx ; 0x004d295d: call 0x4faabd ; 0x004d2962: test al, al ; 0x004d2964: je 0x4d2994
  - 0x004d2964: je -> 0x004d2966 (jcc_false) | ctx: 0x004d295c: push ebx ; 0x004d295d: call 0x4faabd ; 0x004d2962: test al, al ; 0x004d2964: je 0x4d2994

### 0x004d2e3f
- blocks=1, insns=9, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehaviorProps@GGL@@ slot 1 (target 0x004d2e5c, vtable 0x00773544)
- branch points:
  - none

### 0x004d34c9
- blocks=5, insns=53, edges=15, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehavior@GGL@@ slot 3 (target 0x004d352d, vtable 0x007734dc)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehavior@GGL@@ slot 4 (target 0x004d36eb, vtable 0x007734dc)
- branch points:
  - 0x004d34d8: jne -> 0x004d34e1 (jcc_true) | ctx: 0x004d34d1: mov esi, eax ; 0x004d34d3: mov al, byte ptr [esi + 0x6e] ; 0x004d34d6: test al, al ; 0x004d34d8: jne 0x4d34e1
  - 0x004d34d8: jne -> 0x004d34da (jcc_false) | ctx: 0x004d34d1: mov esi, eax ; 0x004d34d3: mov al, byte ptr [esi + 0x6e] ; 0x004d34d6: test al, al ; 0x004d34d8: jne 0x4d34e1
  - 0x004d34ff: jne -> 0x004d351d (jcc_true) | ctx: 0x004d34f5: lea ecx, [esi + 0x38] ; 0x004d34f8: call 0x44b115 ; 0x004d34fd: test eax, eax ; 0x004d34ff: jne 0x4d351d
  - 0x004d34ff: jne -> 0x004d3501 (jcc_false) | ctx: 0x004d34f5: lea ecx, [esi + 0x38] ; 0x004d34f8: call 0x44b115 ; 0x004d34fd: test eax, eax ; 0x004d34ff: jne 0x4d351d
  - 0x004d34ff: jne -> 0x004d351d (jcc_true) | ctx: 0x004d34f5: lea ecx, [esi + 0x38] ; 0x004d34f8: call 0x44b115 ; 0x004d34fd: test eax, eax ; 0x004d34ff: jne 0x4d351d
  - 0x004d34ff: jne -> 0x004d3501 (jcc_false) | ctx: 0x004d34f5: lea ecx, [esi + 0x38] ; 0x004d34f8: call 0x44b115 ; 0x004d34fd: test eax, eax ; 0x004d34ff: jne 0x4d351d

### 0x004d41db
- blocks=1, insns=9, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerFleeBehaviorProps@GGL@@ slot 0 (target 0x004d4200, vtable 0x00772a54)
  - rtti_vtable_method: .?AVCWorkerBehaviorProps@GGL@@ slot 0 (target 0x004d4200, vtable 0x00772b84)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehaviorProps@GGL@@ slot 0 (target 0x004d4200, vtable 0x00773538)
- branch points:
  - none

### 0x004d4208
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004d41db at 0x004d420b)
- branch points:
  - none

### 0x004d6b26
- blocks=1, insns=12, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004d41db at 0x004d6b29)
- branch points:
  - none

### 0x004da5e9
- blocks=1, insns=7, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00508a9b at 0x004da5ec)
  - caller_of_anchor_path: depth 2 (calls 0x004da5e9 at 0x004da64a)
- branch points:
  - none

### 0x004da815
- blocks=3, insns=219, edges=8, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: IsPathingUsed via `IsPathingUsed` (string 0x00774420, xref 0x004da9c1)
  - string_xref: NextWaypointOrientation via `NextWaypointOrientation` (string 0x00774450, xref 0x004da908)
  - string_xref: NextWayPoint via `NextWayPoint` (string 0x00774468, xref 0x004da8c9)
- branch points:
  - 0x004da822: jne -> 0x004dab1f (jcc_true) | ctx: 0x004da816: mov ebp, esp ; 0x004da818: sub esp, 0x24 ; 0x004da81b: test byte ptr [0x86e8a8], 1 ; 0x004da822: jne 0x4dab1f
  - 0x004da822: jne -> 0x004da828 (jcc_false) | ctx: 0x004da816: mov ebp, esp ; 0x004da818: sub esp, 0x24 ; 0x004da81b: test byte ptr [0x86e8a8], 1 ; 0x004da822: jne 0x4dab1f

### 0x004dab46
- blocks=3, insns=128, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: WaypointsCount via `WaypointsCount` (string 0x007744b4, xref 0x004dabe0)
  - string_xref: WayPoints via `WayPoints` (string 0x007744dc, xref 0x004dad33)
  - caller_of_anchor_path: depth 1 (calls 0x004dab46 at 0x004dac69)
  - caller_of_anchor_path: depth 1 (calls 0x004dab46 at 0x004dad26)
- branch points:
  - 0x004dab53: jne -> 0x004dad0a (jcc_true) | ctx: 0x004dab47: mov ebp, esp ; 0x004dab49: sub esp, 0x24 ; 0x004dab4c: test byte ptr [0x86e9f0], 1 ; 0x004dab53: jne 0x4dad0a
  - 0x004dab53: jne -> 0x004dab59 (jcc_false) | ctx: 0x004dab47: mov ebp, esp ; 0x004dab49: sub esp, 0x24 ; 0x004dab4c: test byte ptr [0x86e9f0], 1 ; 0x004dab53: jne 0x4dad0a

### 0x004dad86
- blocks=3, insns=92, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: CoarsePath via `CoarsePath` (string 0x00774510, xref 0x004dade6)
  - string_xref: FinePath via `FinePath` (string 0x0077451c, xref 0x004dadbd)
  - caller_of_anchor_path: depth 1 (calls 0x004da815 at 0x004dada3)
  - caller_of_anchor_path: depth 1 (calls 0x004dad86 at 0x004daebd)
- branch points:
  - 0x004dad93: jne -> 0x004daea1 (jcc_true) | ctx: 0x004dad87: mov ebp, esp ; 0x004dad89: sub esp, 0x24 ; 0x004dad8c: test byte ptr [0x86eb20], 1 ; 0x004dad93: jne 0x4daea1
  - 0x004dad93: jne -> 0x004dad99 (jcc_false) | ctx: 0x004dad87: mov ebp, esp ; 0x004dad89: sub esp, 0x24 ; 0x004dad8c: test byte ptr [0x86eb20], 1 ; 0x004dad93: jne 0x4daea1

### 0x004daf1d
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCPath@EGL@@ slot 1 (target 0x004daf6b, vtable 0x0077452c)
- branch points:
  - 0x004daf20: jne -> 0x004daf2c (jcc_true) | ctx: 0x004daf1d: push edi ; 0x004daf1e: mov edi, ecx ; 0x004daf20: jne 0x4daf2c
  - 0x004daf20: jne -> 0x004daf22 (jcc_false) | ctx: 0x004daf1d: push edi ; 0x004daf1e: mov edi, ecx ; 0x004daf20: jne 0x4daf2c

### 0x004daf73
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCPath@EGL@@ slot 0 (target 0x004daf73, vtable 0x0077452c)
  - rtti_vtable_method: .?AVCPath@GGL@@ slot 1 (target 0x004daf8f, vtable 0x00774540)
- branch points:
  - 0x004daf80: je -> 0x004daf89 (jcc_true) | ctx: 0x004daf74: mov esi, ecx ; 0x004daf76: call 0x58297d ; 0x004daf7b: test byte ptr [esp + 8], 1 ; 0x004daf80: je 0x4daf89
  - 0x004daf80: je -> 0x004daf82 (jcc_false) | ctx: 0x004daf74: mov esi, ecx ; 0x004daf76: call 0x58297d ; 0x004daf7b: test byte ptr [esp + 8], 1 ; 0x004daf80: je 0x4daf89

### 0x004daf9f
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCPath@GGL@@ slot 0 (target 0x004daf9f, vtable 0x00774540)
  - caller_of_anchor_path: depth 1 (calls 0x004daf9f at 0x004dafa2)
- branch points:
  - 0x004dafac: je -> 0x004dafb5 (jcc_true) | ctx: 0x004dafa0: mov esi, ecx ; 0x004dafa2: call 0x4dafbb ; 0x004dafa7: test byte ptr [esp + 8], 1 ; 0x004dafac: je 0x4dafb5
  - 0x004dafac: je -> 0x004dafae (jcc_false) | ctx: 0x004dafa0: mov esi, ecx ; 0x004dafa2: call 0x4dafbb ; 0x004dafa7: test byte ptr [esp + 8], 1 ; 0x004dafac: je 0x4dafb5

### 0x004db298
- blocks=1, insns=14, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004d41db at 0x004db29b)
- branch points:
  - none

### 0x004dbbb4
- blocks=1, insns=25, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004d41db at 0x004dbbb7)
- branch points:
  - none

### 0x004dc8d2
- blocks=1, insns=7, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00508a9b at 0x004dc8d5)
- branch points:
  - none

### 0x004dc8ec
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004dad86 at 0x004dc9a2)
  - caller_of_anchor_path: depth 2 (calls 0x004dc8ec at 0x004dc8ef)
  - caller_of_anchor_path: depth 2 (calls 0x004dc8ec at 0x004dc937)
  - caller_of_anchor_path: depth 2 (calls 0x004dc8d2 at 0x004dc937)
- branch points:
  - 0x004dc8f9: je -> 0x004dc902 (jcc_true) | ctx: 0x004dc8ed: mov esi, ecx ; 0x004dc8ef: call 0x4dc908 ; 0x004dc8f4: test byte ptr [esp + 8], 1 ; 0x004dc8f9: je 0x4dc902
  - 0x004dc8f9: je -> 0x004dc8fb (jcc_false) | ctx: 0x004dc8ed: mov esi, ecx ; 0x004dc8ef: call 0x4dc908 ; 0x004dc8f4: test byte ptr [esp + 8], 1 ; 0x004dc8f9: je 0x4dc902

### 0x004e3278
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCampWithFreeSlotPredicate@GGL@@ slot 0 (target 0x004e3278, vtable 0x007777ac)
- branch points:
  - 0x004e3285: je -> 0x004e328e (jcc_true) | ctx: 0x004e3279: mov esi, ecx ; 0x004e327b: call 0x4ffeb7 ; 0x004e3280: test byte ptr [esp + 8], 1 ; 0x004e3285: je 0x4e328e
  - 0x004e3285: je -> 0x004e3287 (jcc_false) | ctx: 0x004e3279: mov esi, ecx ; 0x004e327b: call 0x4ffeb7 ; 0x004e3280: test byte ptr [esp + 8], 1 ; 0x004e3285: je 0x4e328e

### 0x004e32d2
- blocks=1, insns=26, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004d41db at 0x004e32d5)
- branch points:
  - none

### 0x004e3324
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerFleeBehaviorProps@GGL@@ slot 0 (target 0x004e3324, vtable 0x00772a60)
  - rtti_vtable_method: .?AVCWorkerBehaviorProps@GGL@@ slot 0 (target 0x004e3324, vtable 0x00772b90)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehaviorProps@GGL@@ slot 0 (target 0x004e3324, vtable 0x00773544)
- branch points:
  - 0x004e3331: je -> 0x004e333a (jcc_true) | ctx: 0x004e3325: mov esi, ecx ; 0x004e3327: call 0x50fa20 ; 0x004e332c: test byte ptr [esp + 8], 1 ; 0x004e3331: je 0x4e333a
  - 0x004e3331: je -> 0x004e3333 (jcc_false) | ctx: 0x004e3325: mov esi, ecx ; 0x004e3327: call 0x50fa20 ; 0x004e332c: test byte ptr [esp + 8], 1 ; 0x004e3331: je 0x4e333a

### 0x004e3340
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerFleeBehavior@GGL@@ slot 0 (target 0x004e3340, vtable 0x007729fc)
  - rtti_vtable_method: .?AVCWorkerBehavior@GGL@@ slot 0 (target 0x004e3340, vtable 0x00772b30)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehavior@GGL@@ slot 0 (target 0x004e3340, vtable 0x007734dc)
  - rtti_vtable_method: .?AVCCamperBehavior@GGL@@ slot 0 (target 0x004e3340, vtable 0x0077777c)
  - caller_of_anchor_path: depth 1 (calls 0x004e3278 at 0x004e336e)
- branch points:
  - 0x004e334d: je -> 0x004e3356 (jcc_true) | ctx: 0x004e3341: mov esi, ecx ; 0x004e3343: call 0x4e2619 ; 0x004e3348: test byte ptr [esp + 8], 1 ; 0x004e334d: je 0x4e3356
  - 0x004e334d: je -> 0x004e334f (jcc_false) | ctx: 0x004e3341: mov esi, ecx ; 0x004e3343: call 0x4e2619 ; 0x004e3348: test byte ptr [esp + 8], 1 ; 0x004e334d: je 0x4e3356

### 0x004e3f31
- blocks=1, insns=9, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004d41db at 0x004e3f34)
- branch points:
  - none

### 0x004e5c2c
- blocks=3, insns=130, edges=2, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: MaximumDistanceWorkerToResidence via `MaximumDistanceWorkerToResidence` (string 0x0077569c, xref 0x004e5d96)
  - string_xref: MaximumDistanceWorkerToFarm via `MaximumDistanceWorkerToFarm` (string 0x007756c0, xref 0x004e5d57)
  - string_xref: ReAttachWorkerFrequency via `ReAttachWorkerFrequency` (string 0x007756f0, xref 0x004e5cf2)
- branch points:
  - 0x004e5c39: jne -> 0x004e5de9 (jcc_true) | ctx: 0x004e5c2d: mov ebp, esp ; 0x004e5c2f: sub esp, 0x24 ; 0x004e5c32: test byte ptr [0x871d88], 1 ; 0x004e5c39: jne 0x4e5de9
  - 0x004e5c39: jne -> 0x004e5c3f (jcc_false) | ctx: 0x004e5c2d: mov ebp, esp ; 0x004e5c2f: sub esp, 0x24 ; 0x004e5c32: test byte ptr [0x871d88], 1 ; 0x004e5c39: jne 0x4e5de9

### 0x004e5df7
- blocks=3, insns=19, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004e5c2c at 0x004e5e06)
- branch points:
  - 0x004e5dfa: jne -> 0x004e5e06 (jcc_true) | ctx: 0x004e5df7: push esi ; 0x004e5df8: mov esi, ecx ; 0x004e5dfa: jne 0x4e5e06
  - 0x004e5dfa: jne -> 0x004e5dfc (jcc_false) | ctx: 0x004e5df7: push esi ; 0x004e5df8: mov esi, ecx ; 0x004e5dfa: jne 0x4e5e06

### 0x004e5ee1
- blocks=1, insns=15, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004d41db at 0x004e5ee4)
- branch points:
  - none

### 0x004eaaf1
- blocks=1, insns=7, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00508a9b at 0x004eaaf4)
- branch points:
  - none

### 0x004eab0b
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004dad86 at 0x004eaba4)
  - caller_of_anchor_path: depth 2 (calls 0x004eab0b at 0x004eab0e)
  - caller_of_anchor_path: depth 2 (calls 0x004eab0b at 0x004eab56)
  - caller_of_anchor_path: depth 2 (calls 0x004eaaf1 at 0x004eab56)
- branch points:
  - 0x004eab18: je -> 0x004eab21 (jcc_true) | ctx: 0x004eab0c: mov esi, ecx ; 0x004eab0e: call 0x4eab27 ; 0x004eab13: test byte ptr [esp + 8], 1 ; 0x004eab18: je 0x4eab21
  - 0x004eab18: je -> 0x004eab1a (jcc_false) | ctx: 0x004eab0c: mov esi, ecx ; 0x004eab0e: call 0x4eab27 ; 0x004eab13: test byte ptr [esp + 8], 1 ; 0x004eab18: je 0x4eab21

### 0x004f0942
- blocks=1, insns=15, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004d41db at 0x004f0945)
- branch points:
  - none

### 0x004f2a63
- blocks=1, insns=17, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004d41db at 0x004f2a66)
- branch points:
  - none

### 0x004f32ef
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004d41db at 0x004f32f2)
- branch points:
  - none

### 0x004fa7ec
- blocks=3, insns=93, edges=10, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004a71d5 at 0x004fa809)
- branch points:
  - 0x004fa7f9: jne -> 0x004fa915 (jcc_true) | ctx: 0x004fa7ed: mov ebp, esp ; 0x004fa7ef: sub esp, 0x24 ; 0x004fa7f2: test byte ptr [0x875e80], 1 ; 0x004fa7f9: jne 0x4fa915
  - 0x004fa7f9: jne -> 0x004fa7ff (jcc_false) | ctx: 0x004fa7ed: mov ebp, esp ; 0x004fa7ef: sub esp, 0x24 ; 0x004fa7f2: test byte ptr [0x875e80], 1 ; 0x004fa7f9: jne 0x4fa915

### 0x004fa924
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x004fa7ec at 0x004fa935)
- branch points:
  - 0x004fa927: jne -> 0x004fa933 (jcc_true) | ctx: 0x004fa924: push edi ; 0x004fa925: mov edi, ecx ; 0x004fa927: jne 0x4fa933
  - 0x004fa927: jne -> 0x004fa929 (jcc_false) | ctx: 0x004fa924: push edi ; 0x004fa925: mov edi, ecx ; 0x004fa927: jne 0x4fa933

### 0x004fc624
- blocks=1, insns=15, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004d41db at 0x004fc627)
- branch points:
  - none

### 0x004fd227
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004d41db at 0x004fd22a)
- branch points:
  - none

### 0x004fe0eb
- blocks=1, insns=16, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004d41db at 0x004fe0ee)
- branch points:
  - none

### 0x004fe926
- blocks=1, insns=9, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004d41db at 0x004fe929)
- branch points:
  - none

### 0x004ffe1f
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCamperBehavior@GGL@@ slot 1 (target 0x004ffe42, vtable 0x0077777c)
  - rtti_vtable_method: .?AVCCamperBehavior@GGL@@ slot 4 (target 0x004ffe75, vtable 0x0077777c)
  - rtti_vtable_method: .?AVCCamperBehavior@GGL@@ slot 5 (target 0x004ffe99, vtable 0x0077777c)
  - rtti_vtable_method: .?AVCCampBehavior@GGL@@ slot 5 (target 0x004ffe4a, vtable 0x00777864)
- branch points:
  - 0x004ffe22: jne -> 0x004ffe2e (jcc_true) | ctx: 0x004ffe1f: push edi ; 0x004ffe20: mov edi, ecx ; 0x004ffe22: jne 0x4ffe2e
  - 0x004ffe22: jne -> 0x004ffe24 (jcc_false) | ctx: 0x004ffe1f: push edi ; 0x004ffe20: mov edi, ecx ; 0x004ffe22: jne 0x4ffe2e

### 0x004ffee5
- blocks=1, insns=9, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCamperBehaviorProperties@GGL@@ slot 1 (target 0x004fff05, vtable 0x007777d4)
- branch points:
  - none

### 0x004fff0d
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCPotentialCampSitePredicate@GGL@@ slot 1 (target 0x004fff46, vtable 0x007777a0)
  - rtti_vtable_method: .?AVCCamperBehaviorProperties@GGL@@ slot 0 (target 0x004fff3e, vtable 0x007777c8)
  - rtti_vtable_method: .?AVCCamperBehaviorProperties@GGL@@ slot 0 (target 0x004fff0d, vtable 0x007777d4)
  - caller_of_anchor_path: depth 1 (calls 0x004fff0d at 0x004fff10)
- branch points:
  - 0x004fff1a: je -> 0x004fff23 (jcc_true) | ctx: 0x004fff0e: mov esi, ecx ; 0x004fff10: call 0x4fff29 ; 0x004fff15: test byte ptr [esp + 8], 1 ; 0x004fff1a: je 0x4fff23
  - 0x004fff1a: je -> 0x004fff1c (jcc_false) | ctx: 0x004fff0e: mov esi, ecx ; 0x004fff10: call 0x4fff29 ; 0x004fff15: test byte ptr [esp + 8], 1 ; 0x004fff1a: je 0x4fff23

### 0x005000d8
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCampWithFreeSlotPredicate@GGL@@ slot 1 (target 0x005001fe, vtable 0x007777ac)
- branch points:
  - 0x005000e5: je -> 0x005000ee (jcc_true) | ctx: 0x005000d9: mov esi, ecx ; 0x005000db: call 0x50009d ; 0x005000e0: test byte ptr [esp + 8], 1 ; 0x005000e5: je 0x5000ee
  - 0x005000e5: je -> 0x005000e7 (jcc_false) | ctx: 0x005000d9: mov esi, ecx ; 0x005000db: call 0x50009d ; 0x005000e0: test byte ptr [esp + 8], 1 ; 0x005000e5: je 0x5000ee

### 0x00500212
- blocks=4, insns=36, edges=6, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x005000d8 at 0x005002eb)
- branch points:
  - 0x0050021f: jne -> 0x0050024f (jcc_true) | ctx: 0x00500217: xor bl, bl ; 0x00500219: call dword ptr [eax + 0x30] ; 0x0050021c: cmp eax, dword ptr [edi + 8] ; 0x0050021f: jne 0x50024f
  - 0x0050021f: jne -> 0x00500221 (jcc_false) | ctx: 0x00500217: xor bl, bl ; 0x00500219: call dword ptr [eax + 0x30] ; 0x0050021c: cmp eax, dword ptr [edi + 8] ; 0x0050021f: jne 0x50024f
  - 0x0050022a: jne -> 0x0050024f (jcc_true) | ctx: 0x00500221: mov eax, dword ptr [esi + 0x10] ; 0x00500224: cmp eax, dword ptr [0x877504] ; 0x0050022a: jne 0x50024f
  - 0x0050022a: jne -> 0x0050022c (jcc_false) | ctx: 0x00500221: mov eax, dword ptr [esi + 0x10] ; 0x00500224: cmp eax, dword ptr [0x877504] ; 0x0050022a: jne 0x50024f

### 0x00500a1d
- blocks=3, insns=44, edges=10, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCamperBehavior@GGL@@ slot 3 (target 0x00500b0d, vtable 0x0077777c)
  - rtti_vtable_method: .?AVCCampBehavior@GGL@@ slot 4 (target 0x00500ac6, vtable 0x00777864)
  - caller_of_anchor_path: depth 1 (calls 0x00500a1d at 0x00500ab1)
- branch points:
  - 0x00500a34: je -> 0x00500a80 (jcc_true) | ctx: 0x00500a2a: lea ecx, [eax + 4] ; 0x00500a2d: call 0x44b115 ; 0x00500a32: test eax, eax ; 0x00500a34: je 0x500a80
  - 0x00500a34: je -> 0x00500a36 (jcc_false) | ctx: 0x00500a2a: lea ecx, [eax + 4] ; 0x00500a2d: call 0x44b115 ; 0x00500a32: test eax, eax ; 0x00500a34: je 0x500a80

### 0x00500c1e
- blocks=1, insns=16, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCampBehaviorProperties@GGL@@ slot 0 (target 0x00500c5d, vtable 0x00777848)
  - rtti_vtable_method: .?AVCCampBehaviorProperties@GGL@@ slot 1 (target 0x00500c55, vtable 0x00777854)
- branch points:
  - none

### 0x00500c65
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCampBehaviorProperties@GGL@@ slot 0 (target 0x00500c65, vtable 0x00777854)
  - caller_of_anchor_path: depth 1 (calls 0x00500c65 at 0x00500c68)
  - caller_of_anchor_path: depth 1 (calls 0x00500c81 at 0x00500c68)
- branch points:
  - 0x00500c72: je -> 0x00500c7b (jcc_true) | ctx: 0x00500c66: mov esi, ecx ; 0x00500c68: call 0x500c81 ; 0x00500c6d: test byte ptr [esp + 8], 1 ; 0x00500c72: je 0x500c7b
  - 0x00500c72: je -> 0x00500c74 (jcc_false) | ctx: 0x00500c66: mov esi, ecx ; 0x00500c68: call 0x500c81 ; 0x00500c6d: test byte ptr [esp + 8], 1 ; 0x00500c72: je 0x500c7b

### 0x00500c81
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCampBehavior@GGL@@ slot 1 (target 0x00500ce2, vtable 0x00777864)
- branch points:
  - none

### 0x00500cea
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCampBehavior@GGL@@ slot 0 (target 0x00500cea, vtable 0x00777864)
  - caller_of_anchor_path: depth 1 (calls 0x00500cea at 0x00500ced)
  - caller_of_anchor_path: depth 1 (calls 0x00500d06 at 0x00500ced)
- branch points:
  - 0x00500cf7: je -> 0x00500d00 (jcc_true) | ctx: 0x00500ceb: mov esi, ecx ; 0x00500ced: call 0x500d06 ; 0x00500cf2: test byte ptr [esp + 8], 1 ; 0x00500cf7: je 0x500d00
  - 0x00500cf7: je -> 0x00500cf9 (jcc_false) | ctx: 0x00500ceb: mov esi, ecx ; 0x00500ced: call 0x500d06 ; 0x00500cf2: test byte ptr [esp + 8], 1 ; 0x00500cf7: je 0x500d00

### 0x00500d06
- blocks=1, insns=8, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCampBehavior@GGL@@ slot 3 (target 0x00500e12, vtable 0x00777864)
  - caller_of_anchor_path: depth 1 (calls 0x00500c1e at 0x00500d72)
- branch points:
  - none

### 0x0050122b
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004d41db at 0x0050122e)
- branch points:
  - none

### 0x0050256d
- blocks=4, insns=48, edges=12, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004aa09a at 0x005025ab)
- branch points:
  - 0x0050258d: je -> 0x005025c8 (jcc_true) | ctx: 0x00502588: test eax, eax ; 0x0050258a: push 0x64 ; 0x0050258c: pop esi ; 0x0050258d: je 0x5025c8
  - 0x0050258d: je -> 0x0050258f (jcc_false) | ctx: 0x00502588: test eax, eax ; 0x0050258a: push 0x64 ; 0x0050258c: pop esi ; 0x0050258d: je 0x5025c8
  - 0x00502598: je -> 0x005025c8 (jcc_true) | ctx: 0x00502590: call 0x449432 ; 0x00502595: test eax, eax ; 0x00502597: pop ecx ; 0x00502598: je 0x5025c8
  - 0x00502598: je -> 0x0050259a (jcc_false) | ctx: 0x00502590: call 0x449432 ; 0x00502595: test eax, eax ; 0x00502597: pop ecx ; 0x00502598: je 0x5025c8

### 0x0050443c
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004af71e at 0x00504474)
- branch points:
  - 0x0050443f: jne -> 0x0050444b (jcc_true) | ctx: 0x0050443c: push edi ; 0x0050443d: mov edi, ecx ; 0x0050443f: jne 0x50444b
  - 0x0050443f: jne -> 0x00504441 (jcc_false) | ctx: 0x0050443c: push edi ; 0x0050443d: mov edi, ecx ; 0x0050443f: jne 0x50444b

### 0x00508a9b
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCoarsePath@EGL@@ slot 0 (target 0x00508a9b, vtable 0x007786a4)
  - caller_of_anchor_path: depth 1 (calls 0x00508a9b at 0x00508a9e)
- branch points:
  - 0x00508aa8: je -> 0x00508ab1 (jcc_true) | ctx: 0x00508a9c: mov esi, ecx ; 0x00508a9e: call 0x508a94 ; 0x00508aa3: test byte ptr [esp + 8], 1 ; 0x00508aa8: je 0x508ab1
  - 0x00508aa8: je -> 0x00508aaa (jcc_false) | ctx: 0x00508a9c: mov esi, ecx ; 0x00508a9e: call 0x508a94 ; 0x00508aa3: test byte ptr [esp + 8], 1 ; 0x00508aa8: je 0x508ab1

### 0x00508b37
- blocks=12, insns=125, edges=34, jcc=8, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00508a9b at 0x00508d1d)
  - caller_of_anchor_path: depth 1 (calls 0x00582db4 at 0x00508c0f)
- branch points:
  - 0x00508ba9: je -> 0x00508bf1 (jcc_true) | ctx: 0x00508ba1: add esp, 0x24 ; 0x00508ba4: test eax, eax ; 0x00508ba6: mov dword ptr [ebp - 0x10], ecx ; 0x00508ba9: je 0x508bf1
  - 0x00508ba9: je -> 0x00508bab (jcc_false) | ctx: 0x00508ba1: add esp, 0x24 ; 0x00508ba4: test eax, eax ; 0x00508ba6: mov dword ptr [ebp - 0x10], ecx ; 0x00508ba9: je 0x508bf1
  - 0x00508c1f: jle -> 0x00508c62 (jcc_true) | ctx: 0x00508c14: mov ecx, dword ptr [esi + 0x4c] ; 0x00508c17: call 0x58270a ; 0x00508c1c: cmp eax, 1 ; 0x00508c1f: jle 0x508c62
  - 0x00508c1f: jle -> 0x00508c21 (jcc_false) | ctx: 0x00508c14: mov ecx, dword ptr [esi + 0x4c] ; 0x00508c17: call 0x58270a ; 0x00508c1c: cmp eax, 1 ; 0x00508c1f: jle 0x508c62
  - 0x00508bae: jne -> 0x00508bdf (jcc_true) | ctx: 0x00508bab: cmp eax, 1 ; 0x00508bae: jne 0x508bdf
  - 0x00508bae: jne -> 0x00508bb0 (jcc_false) | ctx: 0x00508bab: cmp eax, 1 ; 0x00508bae: jne 0x508bdf
  - 0x00508c34: jmp -> 0x00508c4b (jmp) | ctx: 0x00508c2b: lea eax, [ebp - 4] ; 0x00508c2e: push eax ; 0x00508c2f: call 0x40254d ; 0x00508c34: jmp 0x508c4b
  - 0x00508bef: jmp -> 0x00508c14 (jmp) | ctx: 0x00508be6: mov ecx, dword ptr [esi + 0x4c] ; 0x00508be9: push ebx ; 0x00508bea: call 0x582996 ; 0x00508bef: jmp 0x508c14
  - 0x00508bda: je -> 0x00508bf1 (jcc_true) | ctx: 0x00508bce: call 0x577805 ; 0x00508bd3: mov cx, word ptr [ebp - 2] ; 0x00508bd7: cmp ax, cx ; 0x00508bda: je 0x508bf1
  - 0x00508bda: je -> 0x00508bdc (jcc_false) | ctx: 0x00508bce: call 0x577805 ; 0x00508bd3: mov cx, word ptr [ebp - 2] ; 0x00508bd7: cmp ax, cx ; 0x00508bda: je 0x508bf1
  - 0x00508c60: jne -> 0x00508c36 (jcc_true) | ctx: 0x00508c56: call 0x582865 ; 0x00508c5b: mov ecx, dword ptr [ebp - 4] ; 0x00508c5e: cmp ecx, dword ptr [eax] ; 0x00508c60: jne 0x508c36
  - 0x00508c60: jne -> 0x00508c62 (jcc_false) | ctx: 0x00508c56: call 0x582865 ; 0x00508c5b: mov ecx, dword ptr [ebp - 4] ; 0x00508c5e: cmp ecx, dword ptr [eax] ; 0x00508c60: jne 0x508c36
  - 0x00508c1f: jle -> 0x00508c62 (jcc_true) | ctx: 0x00508c14: mov ecx, dword ptr [esi + 0x4c] ; 0x00508c17: call 0x58270a ; 0x00508c1c: cmp eax, 1 ; 0x00508c1f: jle 0x508c62
  - 0x00508c1f: jle -> 0x00508c21 (jcc_false) | ctx: 0x00508c14: mov ecx, dword ptr [esi + 0x4c] ; 0x00508c17: call 0x58270a ; 0x00508c1c: cmp eax, 1 ; 0x00508c1f: jle 0x508c62
  - 0x00508bef: jmp -> 0x00508c14 (jmp) | ctx: 0x00508be6: mov ecx, dword ptr [esi + 0x4c] ; 0x00508be9: push ebx ; 0x00508bea: call 0x582996 ; 0x00508bef: jmp 0x508c14
  - 0x00508c43: je -> 0x00508c62 (jcc_true) | ctx: 0x00508c3f: test al, al ; 0x00508c41: pop ecx ; 0x00508c42: pop ecx ; 0x00508c43: je 0x508c62
  - 0x00508c43: je -> 0x00508c45 (jcc_false) | ctx: 0x00508c3f: test al, al ; 0x00508c41: pop ecx ; 0x00508c42: pop ecx ; 0x00508c43: je 0x508c62
  - 0x00508c60: jne -> 0x00508c36 (jcc_true) | ctx: 0x00508c56: call 0x582865 ; 0x00508c5b: mov ecx, dword ptr [ebp - 4] ; 0x00508c5e: cmp ecx, dword ptr [eax] ; 0x00508c60: jne 0x508c36
  - 0x00508c60: jne -> 0x00508c62 (jcc_false) | ctx: 0x00508c56: call 0x582865 ; 0x00508c5b: mov ecx, dword ptr [ebp - 4] ; 0x00508c5e: cmp ecx, dword ptr [eax] ; 0x00508c60: jne 0x508c36

### 0x00508dbc
- blocks=4, insns=36, edges=6, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00508b37 at 0x00508dc8)
- branch points:
  - 0x00508dd3: jle -> 0x00508de1 (jcc_true) | ctx: 0x00508dcd: mov esi, dword ptr [esi] ; 0x00508dcf: test esi, esi ; 0x00508dd1: mov ecx, edi ; 0x00508dd3: jle 0x508de1
  - 0x00508dd3: jle -> 0x00508dd5 (jcc_false) | ctx: 0x00508dcd: mov esi, dword ptr [esi] ; 0x00508dcf: test esi, esi ; 0x00508dd1: mov ecx, edi ; 0x00508dd3: jle 0x508de1
  - 0x00508ddf: jmp -> 0x00508de9 (jmp) | ctx: 0x00508dd6: lea eax, [ebp - 8] ; 0x00508dd9: push eax ; 0x00508dda: call 0x508d4a ; 0x00508ddf: jmp 0x508de9

### 0x00508e84
- blocks=10, insns=96, edges=25, jcc=8, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 3 (calls 0x00508dbc at 0x00508f15)
- branch points:
  - 0x00508eba: je -> 0x00508ec5 (jcc_true) | ctx: 0x00508eb2: push eax ; 0x00508eb3: call 0x57772e ; 0x00508eb8: test al, al ; 0x00508eba: je 0x508ec5
  - 0x00508eba: je -> 0x00508ebc (jcc_false) | ctx: 0x00508eb2: push eax ; 0x00508eb3: call 0x57772e ; 0x00508eb8: test al, al ; 0x00508eba: je 0x508ec5
  - 0x00508ec9: jne -> 0x00508f3e (jcc_true) | ctx: 0x00508ec5: cmp byte ptr [edi + 0x6d], 0 ; 0x00508ec9: jne 0x508f3e
  - 0x00508ec9: jne -> 0x00508ecb (jcc_false) | ctx: 0x00508ec5: cmp byte ptr [edi + 0x6d], 0 ; 0x00508ec9: jne 0x508f3e
  - 0x00508ec9: jne -> 0x00508f3e (jcc_true) | ctx: 0x00508ebe: mov ecx, edi ; 0x00508ec0: call 0x57ab23 ; 0x00508ec5: cmp byte ptr [edi + 0x6d], 0 ; 0x00508ec9: jne 0x508f3e
  - 0x00508ec9: jne -> 0x00508ecb (jcc_false) | ctx: 0x00508ebe: mov ecx, edi ; 0x00508ec0: call 0x57ab23 ; 0x00508ec5: cmp byte ptr [edi + 0x6d], 0 ; 0x00508ec9: jne 0x508f3e
  - 0x00508ef5: jne -> 0x00508f02 (jcc_true) | ctx: 0x00508eeb: lea ecx, [edi + 0x58] ; 0x00508eee: call 0x498387 ; 0x00508ef3: test al, al ; 0x00508ef5: jne 0x508f02
  - 0x00508ef5: jne -> 0x00508ef7 (jcc_false) | ctx: 0x00508eeb: lea ecx, [edi + 0x58] ; 0x00508eee: call 0x498387 ; 0x00508ef3: test al, al ; 0x00508ef5: jne 0x508f02
  - 0x00508f06: jle -> 0x00508f0f (jcc_true) | ctx: 0x00508f02: cmp dword ptr [esi + 0x60], 0 ; 0x00508f06: jle 0x508f0f
  - 0x00508f06: jle -> 0x00508f08 (jcc_false) | ctx: 0x00508f02: cmp dword ptr [esi + 0x60], 0 ; 0x00508f06: jle 0x508f0f
  - 0x00508f00: je -> 0x00508f33 (jcc_true) | ctx: 0x00508ef7: mov ecx, esi ; 0x00508ef9: call 0x508865 ; 0x00508efe: test al, al ; 0x00508f00: je 0x508f33
  - 0x00508f00: je -> 0x00508f02 (jcc_false) | ctx: 0x00508ef7: mov ecx, esi ; 0x00508ef9: call 0x508865 ; 0x00508efe: test al, al ; 0x00508f00: je 0x508f33
  - 0x00508f31: jne -> 0x00508f3e (jcc_true) | ctx: 0x00508f29: setge al ; 0x00508f2c: test al, al ; 0x00508f2e: mov dword ptr [ebp - 0xc], ecx ; 0x00508f31: jne 0x508f3e
  - 0x00508f31: jne -> 0x00508f33 (jcc_false) | ctx: 0x00508f29: setge al ; 0x00508f2c: test al, al ; 0x00508f2e: mov dword ptr [ebp - 0xc], ecx ; 0x00508f31: jne 0x508f3e
  - 0x00508f31: jne -> 0x00508f3e (jcc_true) | ctx: 0x00508f29: setge al ; 0x00508f2c: test al, al ; 0x00508f2e: mov dword ptr [ebp - 0xc], ecx ; 0x00508f31: jne 0x508f3e
  - 0x00508f31: jne -> 0x00508f33 (jcc_false) | ctx: 0x00508f29: setge al ; 0x00508f2c: test al, al ; 0x00508f2e: mov dword ptr [ebp - 0xc], ecx ; 0x00508f31: jne 0x508f3e

### 0x00508f58
- blocks=13, insns=95, edges=25, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 3 (calls 0x00508dbc at 0x00508f9e)
- branch points:
  - 0x00508f75: jne -> 0x00508fcc (jcc_true) | ctx: 0x00508f70: dec eax ; 0x00508f71: cmp edi, eax ; 0x00508f73: mov ecx, esi ; 0x00508f75: jne 0x508fcc
  - 0x00508f75: jne -> 0x00508f77 (jcc_false) | ctx: 0x00508f70: dec eax ; 0x00508f71: cmp edi, eax ; 0x00508f73: mov ecx, esi ; 0x00508f75: jne 0x508fcc
  - 0x00508fd3: jle -> 0x00508fe7 (jcc_true) | ctx: 0x00508fcc: cmp dword ptr [esi + 0xf4], 0x10 ; 0x00508fd3: jle 0x508fe7
  - 0x00508fd3: jle -> 0x00508fd5 (jcc_false) | ctx: 0x00508fcc: cmp dword ptr [esi + 0xf4], 0x10 ; 0x00508fd3: jle 0x508fe7
  - 0x00508f7b: jg -> 0x00508f93 (jcc_true) | ctx: 0x00508f77: cmp dword ptr [esi + 0x60], 1 ; 0x00508f7b: jg 0x508f93
  - 0x00508f7b: jg -> 0x00508f7d (jcc_false) | ctx: 0x00508f77: cmp dword ptr [esi + 0x60], 1 ; 0x00508f7b: jg 0x508f93
  - 0x00508fe5: jmp -> 0x00508ffa (jmp) | ctx: 0x00508fdc: lea eax, [ebp - 8] ; 0x00508fdf: push eax ; 0x00508fe0: call 0x508e84 ; 0x00508fe5: jmp 0x508ffa
  - 0x00508faf: jge -> 0x00508fff (jcc_true) | ctx: 0x00508fa3: cmp dword ptr [esi + 0xf0], 0 ; 0x00508faa: mov edi, dword ptr [eax] ; 0x00508fac: mov ebx, dword ptr [eax + 4] ; 0x00508faf: jge 0x508fff
  - 0x00508faf: jge -> 0x00508fb1 (jcc_false) | ctx: 0x00508fa3: cmp dword ptr [esi + 0xf0], 0 ; 0x00508faa: mov edi, dword ptr [eax] ; 0x00508fac: mov ebx, dword ptr [eax + 4] ; 0x00508faf: jge 0x508fff
  - 0x00508f89: je -> 0x00508fdf (jcc_true) | ctx: 0x00508f82: test al, al ; 0x00508f84: mov ecx, esi ; 0x00508f86: lea eax, [ebp - 8] ; 0x00508f89: je 0x508fdf
  - 0x00508f89: je -> 0x00508f8b (jcc_false) | ctx: 0x00508f82: test al, al ; 0x00508f84: mov ecx, esi ; 0x00508f86: lea eax, [ebp - 8] ; 0x00508f89: je 0x508fdf
  - 0x00508fca: jmp -> 0x00508fff (jmp) | ctx: 0x00508fc2: push ecx ; 0x00508fc3: mov ecx, eax ; 0x00508fc5: call 0x57db6a ; 0x00508fca: jmp 0x508fff
  - 0x00508fe5: jmp -> 0x00508ffa (jmp) | ctx: 0x00508fdf: push eax ; 0x00508fe0: call 0x508e84 ; 0x00508fe5: jmp 0x508ffa
  - 0x00508f91: jmp -> 0x00508ff4 (jmp) | ctx: 0x00508f8b: push dword ptr [esi + 0xf0] ; 0x00508f91: jmp 0x508ff4

### 0x00509274
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004dad86 at 0x00509285)
- branch points:
  - 0x00509277: jne -> 0x00509283 (jcc_true) | ctx: 0x00509274: push edi ; 0x00509275: mov edi, ecx ; 0x00509277: jne 0x509283
  - 0x00509277: jne -> 0x00509279 (jcc_false) | ctx: 0x00509274: push edi ; 0x00509275: mov edi, ecx ; 0x00509277: jne 0x509283

### 0x00509d77
- blocks=1, insns=7, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00508a9b at 0x00509d7a)
- branch points:
  - none

### 0x00509d91
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004dad86 at 0x00509e2a)
  - caller_of_anchor_path: depth 2 (calls 0x00509d91 at 0x00509d94)
  - caller_of_anchor_path: depth 2 (calls 0x00509d91 at 0x00509ddc)
  - caller_of_anchor_path: depth 2 (calls 0x00509d77 at 0x00509ddc)
- branch points:
  - 0x00509d9e: je -> 0x00509da7 (jcc_true) | ctx: 0x00509d92: mov esi, ecx ; 0x00509d94: call 0x509dad ; 0x00509d99: test byte ptr [esp + 8], 1 ; 0x00509d9e: je 0x509da7
  - 0x00509d9e: je -> 0x00509da0 (jcc_false) | ctx: 0x00509d92: mov esi, ecx ; 0x00509d94: call 0x509dad ; 0x00509d99: test byte ptr [esp + 8], 1 ; 0x00509d9e: je 0x509da7

### 0x0050d7dc
- blocks=1, insns=18, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 3 (calls 0x00579a40 at 0x0050d8ea)
- branch points:
  - none

### 0x0051254c
- blocks=3, insns=142, edges=8, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004a71d5 at 0x00512569)
- branch points:
  - 0x00512559: jne -> 0x00512725 (jcc_true) | ctx: 0x0051254d: mov ebp, esp ; 0x0051254f: sub esp, 0x24 ; 0x00512552: test byte ptr [0x87c73c], 1 ; 0x00512559: jne 0x512725
  - 0x00512559: jne -> 0x0051255f (jcc_false) | ctx: 0x0051254d: mov ebp, esp ; 0x0051254f: sub esp, 0x24 ; 0x00512552: test byte ptr [0x87c73c], 1 ; 0x00512559: jne 0x512725

### 0x00512734
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0051254c at 0x00512745)
- branch points:
  - 0x00512737: jne -> 0x00512743 (jcc_true) | ctx: 0x00512734: push edi ; 0x00512735: mov edi, ecx ; 0x00512737: jne 0x512743
  - 0x00512737: jne -> 0x00512739 (jcc_false) | ctx: 0x00512734: push edi ; 0x00512735: mov edi, ecx ; 0x00512737: jne 0x512743

### 0x00513221
- blocks=1, insns=15, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004d41db at 0x00513224)
- branch points:
  - none

### 0x00516ab2
- blocks=3, insns=44, edges=5, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: WayPoints via `WayPoints` (string 0x007744dc, xref 0x00516ade)
- branch points:
  - 0x00516abf: jne -> 0x00516b33 (jcc_true) | ctx: 0x00516ab3: mov ebp, esp ; 0x00516ab5: sub esp, 0x24 ; 0x00516ab8: test byte ptr [0x87e1f8], 1 ; 0x00516abf: jne 0x516b33
  - 0x00516abf: jne -> 0x00516ac1 (jcc_false) | ctx: 0x00516ab3: mov ebp, esp ; 0x00516ab5: sub esp, 0x24 ; 0x00516ab8: test byte ptr [0x87e1f8], 1 ; 0x00516abf: jne 0x516b33

### 0x00516b3a
- blocks=3, insns=71, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00516ab2 at 0x00516b57)
  - caller_of_anchor_path: depth 2 (calls 0x00516b3a at 0x00516c32)
  - caller_of_anchor_path: depth 2 (calls 0x00516b3a at 0x00516c9f)
  - caller_of_anchor_path: depth 2 (calls 0x00516b3a at 0x00516d0c)
- branch points:
  - 0x00516b47: jne -> 0x00516c16 (jcc_true) | ctx: 0x00516b3b: mov ebp, esp ; 0x00516b3d: sub esp, 0x24 ; 0x00516b40: test byte ptr [0x87e290], 1 ; 0x00516b47: jne 0x516c16
  - 0x00516b47: jne -> 0x00516b4d (jcc_false) | ctx: 0x00516b3b: mov ebp, esp ; 0x00516b3d: sub esp, 0x24 ; 0x00516b40: test byte ptr [0x87e290], 1 ; 0x00516b47: jne 0x516c16

### 0x00516dab
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00516b3a at 0x00516dbc)
- branch points:
  - 0x00516dae: jne -> 0x00516dba (jcc_true) | ctx: 0x00516dab: push edi ; 0x00516dac: mov edi, ecx ; 0x00516dae: jne 0x516dba
  - 0x00516dae: jne -> 0x00516db0 (jcc_false) | ctx: 0x00516dab: push edi ; 0x00516dac: mov edi, ecx ; 0x00516dae: jne 0x516dba

### 0x0051a9c4
- blocks=4, insns=31, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 3 (calls 0x005516e5 at 0x0051abd9)
- branch points:
  - 0x0051a9e0: jae -> 0x0051a9f1 (jcc_true) | ctx: 0x0051a9d9: cmp edi, eax ; 0x0051a9db: push dword ptr [ebp + 8] ; 0x0051a9de: mov ecx, esi ; 0x0051a9e0: jae 0x51a9f1
  - 0x0051a9e0: jae -> 0x0051a9e2 (jcc_false) | ctx: 0x0051a9d9: cmp edi, eax ; 0x0051a9db: push dword ptr [ebp + 8] ; 0x0051a9de: mov ecx, esi ; 0x0051a9e0: jae 0x51a9f1
  - 0x0051a9ef: jmp -> 0x0051a9fe (jmp) | ctx: 0x0051a9e4: push dword ptr [esi + 8] ; 0x0051a9e7: call 0x51a71d ; 0x0051a9ec: mov dword ptr [esi + 8], eax ; 0x0051a9ef: jmp 0x51a9fe

### 0x005232f2
- blocks=8, insns=75, edges=13, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0052390a at 0x005233fa)
- branch points:
  - 0x005232fe: je -> 0x00523360 (jcc_true) | ctx: 0x005232f6: push edi ; 0x005232f7: mov edi, dword ptr [ebp + 8] ; 0x005232fa: cmp dword ptr [edi + 0x18], 0 ; 0x005232fe: je 0x523360
  - 0x005232fe: je -> 0x00523300 (jcc_false) | ctx: 0x005232f6: push edi ; 0x005232f7: mov edi, dword ptr [ebp + 8] ; 0x005232fa: cmp dword ptr [edi + 0x18], 0 ; 0x005232fe: je 0x523360
  - 0x0052331a: je -> 0x0052335f (jcc_true) | ctx: 0x00523310: call 0x70b520 ; 0x00523315: add esp, 0x10 ; 0x00523318: test eax, eax ; 0x0052331a: je 0x52335f
  - 0x0052331a: je -> 0x0052331c (jcc_false) | ctx: 0x00523310: call 0x70b520 ; 0x00523315: add esp, 0x10 ; 0x00523318: test eax, eax ; 0x0052331a: je 0x52335f
  - 0x00523321: je -> 0x0052334b (jcc_true) | ctx: 0x0052331c: mov eax, dword ptr [esi + 0x38] ; 0x0052331f: test eax, eax ; 0x00523321: je 0x52334b
  - 0x00523321: je -> 0x00523323 (jcc_false) | ctx: 0x0052331c: mov eax, dword ptr [esi + 0x38] ; 0x0052331f: test eax, eax ; 0x00523321: je 0x52334b
  - 0x0052333f: je -> 0x0052335f (jcc_true) | ctx: 0x00523338: call eax ; 0x0052333a: add esp, 0xc ; 0x0052333d: test al, al ; 0x0052333f: je 0x52335f
  - 0x0052333f: je -> 0x00523341 (jcc_false) | ctx: 0x00523338: call eax ; 0x0052333a: add esp, 0xc ; 0x0052333d: test al, al ; 0x0052333f: je 0x52335f

### 0x0052390a
- blocks=13, insns=127, edges=49, jcc=10, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0052b39d at 0x00523a76)
- branch points:
  - 0x00523911: je -> 0x0052399f (jcc_true) | ctx: 0x0052390a: push esi ; 0x0052390b: mov esi, ecx ; 0x0052390d: cmp dword ptr [esi + 0x5c], 0 ; 0x00523911: je 0x52399f
  - 0x00523911: je -> 0x00523917 (jcc_false) | ctx: 0x0052390a: push esi ; 0x0052390b: mov esi, ecx ; 0x0052390d: cmp dword ptr [esi + 0x5c], 0 ; 0x00523911: je 0x52399f
  - 0x005239a6: je -> 0x005239e7 (jcc_true) | ctx: 0x0052399f: call 0x45ea50 ; 0x005239a4: test eax, eax ; 0x005239a6: je 0x5239e7
  - 0x005239a6: je -> 0x005239a8 (jcc_false) | ctx: 0x0052399f: call 0x45ea50 ; 0x005239a4: test eax, eax ; 0x005239a6: je 0x5239e7
  - 0x00523922: jne -> 0x00523930 (jcc_true) | ctx: 0x0052391c: push edi ; 0x0052391d: call dword ptr [eax + 0x1c] ; 0x00523920: test eax, eax ; 0x00523922: jne 0x523930
  - 0x00523922: jne -> 0x00523924 (jcc_false) | ctx: 0x0052391c: push edi ; 0x0052391d: call dword ptr [eax + 0x1c] ; 0x00523920: test eax, eax ; 0x00523922: jne 0x523930
  - 0x005239ee: je -> 0x00523a03 (jcc_true) | ctx: 0x005239e7: cmp dword ptr [0x880ba4], 0 ; 0x005239ee: je 0x523a03
  - 0x005239ee: je -> 0x005239f0 (jcc_false) | ctx: 0x005239e7: cmp dword ptr [0x880ba4], 0 ; 0x005239ee: je 0x523a03
  - 0x005239ca: je -> 0x005239e7 (jcc_true) | ctx: 0x005239c1: mov ecx, eax ; 0x005239c3: call 0x5588a0 ; 0x005239c8: test eax, eax ; 0x005239ca: je 0x5239e7
  - 0x005239ca: je -> 0x005239cc (jcc_false) | ctx: 0x005239c1: mov ecx, eax ; 0x005239c3: call 0x5588a0 ; 0x005239c8: test eax, eax ; 0x005239ca: je 0x5239e7
  - 0x0052396a: je -> 0x0052397b (jcc_true) | ctx: 0x00523964: push edi ; 0x00523965: call dword ptr [eax + 0x14] ; 0x00523968: test al, al ; 0x0052396a: je 0x52397b
  - 0x0052396a: je -> 0x0052396c (jcc_false) | ctx: 0x00523964: push edi ; 0x00523965: call dword ptr [eax + 0x14] ; 0x00523968: test al, al ; 0x0052396a: je 0x52397b
  - 0x0052392e: jmp -> 0x0052397b (jmp) | ctx: 0x00523927: mov eax, dword ptr [ecx] ; 0x00523929: push 0 ; 0x0052392b: call dword ptr [eax + 0x10] ; 0x0052392e: jmp 0x52397b
  - 0x005239db: je -> 0x005239e7 (jcc_true) | ctx: 0x005239d2: mov ecx, eax ; 0x005239d4: call 0x558966 ; 0x005239d9: test eax, eax ; 0x005239db: je 0x5239e7
  - 0x005239db: je -> 0x005239dd (jcc_false) | ctx: 0x005239d2: mov ecx, eax ; 0x005239d4: call 0x558966 ; 0x005239d9: test eax, eax ; 0x005239db: je 0x5239e7
  - 0x005239a6: je -> 0x005239e7 (jcc_true) | ctx: 0x0052399e: pop edi ; 0x0052399f: call 0x45ea50 ; 0x005239a4: test eax, eax ; 0x005239a6: je 0x5239e7
  - 0x005239a6: je -> 0x005239a8 (jcc_false) | ctx: 0x0052399e: pop edi ; 0x0052399f: call 0x45ea50 ; 0x005239a4: test eax, eax ; 0x005239a6: je 0x5239e7
  - 0x005239a6: je -> 0x005239e7 (jcc_true) | ctx: 0x0052399e: pop edi ; 0x0052399f: call 0x45ea50 ; 0x005239a4: test eax, eax ; 0x005239a6: je 0x5239e7
  - 0x005239a6: je -> 0x005239a8 (jcc_false) | ctx: 0x0052399e: pop edi ; 0x0052399f: call 0x45ea50 ; 0x005239a4: test eax, eax ; 0x005239a6: je 0x5239e7
  - 0x005239ee: je -> 0x00523a03 (jcc_true) | ctx: 0x005239e2: mov ecx, eax ; 0x005239e4: call dword ptr [edx + 0x20] ; 0x005239e7: cmp dword ptr [0x880ba4], 0 ; 0x005239ee: je 0x523a03
  - 0x005239ee: je -> 0x005239f0 (jcc_false) | ctx: 0x005239e2: mov ecx, eax ; 0x005239e4: call dword ptr [edx + 0x20] ; 0x005239e7: cmp dword ptr [0x880ba4], 0 ; 0x005239ee: je 0x523a03

### 0x0052b39d
- blocks=7, insns=101, edges=23, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerFleeBehavior@GGL@@ slot 6 (target 0x0052b509, vtable 0x007729fc)
  - rtti_vtable_method: .?AVCWorkerFleeBehavior@GGL@@ slot 7 (target 0x0052b509, vtable 0x007729fc)
  - rtti_vtable_method: .?AVCWorkerBehavior@GGL@@ slot 6 (target 0x0052b509, vtable 0x00772b30)
  - rtti_vtable_method: .?AVCWorkerBehavior@GGL@@ slot 7 (target 0x0052b509, vtable 0x00772b30)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehavior@GGL@@ slot 6 (target 0x0052b509, vtable 0x007734dc)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehavior@GGL@@ slot 7 (target 0x0052b509, vtable 0x007734dc)
  - rtti_vtable_method: .?AVCCamperBehavior@GGL@@ slot 6 (target 0x0052b509, vtable 0x0077777c)
  - rtti_vtable_method: .?AVCCamperBehavior@GGL@@ slot 7 (target 0x0052b509, vtable 0x0077777c)
  - rtti_vtable_method: .?AVCCampBehavior@GGL@@ slot 6 (target 0x0052b509, vtable 0x00777864)
  - rtti_vtable_method: .?AVCCampBehavior@GGL@@ slot 7 (target 0x0052b509, vtable 0x00777864)
- branch points:
  - 0x0052b3ce: jle -> 0x0052b476 (jcc_true) | ctx: 0x0052b3c5: mov dword ptr [ebp + 8], ebx ; 0x0052b3c8: call dword ptr [eax + 0x4c] ; 0x0052b3cb: cmp dword ptr [ebp + 8], ebx ; 0x0052b3ce: jle 0x52b476
  - 0x0052b3ce: jle -> 0x0052b3d4 (jcc_false) | ctx: 0x0052b3c5: mov dword ptr [ebp + 8], ebx ; 0x0052b3c8: call dword ptr [eax + 0x4c] ; 0x0052b3cb: cmp dword ptr [ebp + 8], ebx ; 0x0052b3ce: jle 0x52b476
  - 0x0052b425: je -> 0x0052b44c (jcc_true) | ctx: 0x0052b41e: call dword ptr [eax + 0x4c] ; 0x0052b421: mov eax, dword ptr [ebp - 0x1c] ; 0x0052b424: dec eax ; 0x0052b425: je 0x52b44c
  - 0x0052b425: je -> 0x0052b427 (jcc_false) | ctx: 0x0052b41e: call dword ptr [eax + 0x4c] ; 0x0052b421: mov eax, dword ptr [ebp - 0x1c] ; 0x0052b424: dec eax ; 0x0052b425: je 0x52b44c
  - 0x0052b470: jl -> 0x0052b3d4 (jcc_true) | ctx: 0x0052b467: call 0x52afe5 ; 0x0052b46c: inc ebx ; 0x0052b46d: cmp ebx, dword ptr [ebp + 8] ; 0x0052b470: jl 0x52b3d4
  - 0x0052b470: jl -> 0x0052b476 (jcc_false) | ctx: 0x0052b467: call 0x52afe5 ; 0x0052b46c: inc ebx ; 0x0052b46d: cmp ebx, dword ptr [ebp + 8] ; 0x0052b470: jl 0x52b3d4
  - 0x0052b428: jne -> 0x0052b46c (jcc_true) | ctx: 0x0052b427: dec eax ; 0x0052b428: jne 0x52b46c
  - 0x0052b428: jne -> 0x0052b42a (jcc_false) | ctx: 0x0052b427: dec eax ; 0x0052b428: jne 0x52b46c
  - 0x0052b470: jl -> 0x0052b3d4 (jcc_true) | ctx: 0x0052b46c: inc ebx ; 0x0052b46d: cmp ebx, dword ptr [ebp + 8] ; 0x0052b470: jl 0x52b3d4
  - 0x0052b470: jl -> 0x0052b476 (jcc_false) | ctx: 0x0052b46c: inc ebx ; 0x0052b46d: cmp ebx, dword ptr [ebp + 8] ; 0x0052b470: jl 0x52b3d4
  - 0x0052b44a: jmp -> 0x0052b46c (jmp) | ctx: 0x0052b43f: fld dword ptr [ebp - 0x14] ; 0x0052b442: fstp dword ptr [esp] ; 0x0052b445: call 0x52b071 ; 0x0052b44a: jmp 0x52b46c

### 0x005463c3
- blocks=1, insns=21, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 3 (calls 0x005516e5 at 0x00546429)
- branch points:
  - none

### 0x0054de44
- blocks=3, insns=13, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 3 (calls 0x005516e5 at 0x0054de72)
- branch points:
  - 0x0054de4d: je -> 0x0054de56 (jcc_true) | ctx: 0x0054de44: push esi ; 0x0054de45: mov esi, ecx ; 0x0054de47: mov dword ptr [esi], 0x77f778 ; 0x0054de4d: je 0x54de56
  - 0x0054de4d: je -> 0x0054de4f (jcc_false) | ctx: 0x0054de44: push esi ; 0x0054de45: mov esi, ecx ; 0x0054de47: mov dword ptr [esi], 0x77f778 ; 0x0054de4d: je 0x54de56

### 0x0054e57d
- blocks=5, insns=34, edges=9, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 3 (calls 0x005516e5 at 0x0054e580)
- branch points:
  - 0x0054e589: je -> 0x0054e5c0 (jcc_true) | ctx: 0x0054e580: call 0x551701 ; 0x0054e585: mov esi, eax ; 0x0054e587: test esi, esi ; 0x0054e589: je 0x54e5c0
  - 0x0054e589: je -> 0x0054e58b (jcc_false) | ctx: 0x0054e580: call 0x551701 ; 0x0054e585: mov esi, eax ; 0x0054e587: test esi, esi ; 0x0054e589: je 0x54e5c0
  - 0x0054e59c: je -> 0x0054e5b4 (jcc_true) | ctx: 0x0054e592: call dword ptr [eax + 0x18] ; 0x0054e595: cmp byte ptr [ebp + 0xc], 0 ; 0x0054e599: mov dword ptr [ebp + 0xc], esi ; 0x0054e59c: je 0x54e5b4
  - 0x0054e59c: je -> 0x0054e59e (jcc_false) | ctx: 0x0054e592: call dword ptr [eax + 0x18] ; 0x0054e595: cmp byte ptr [ebp + 0xc], 0 ; 0x0054e599: mov dword ptr [ebp + 0xc], esi ; 0x0054e59c: je 0x54e5b4
  - 0x0054e5b2: jmp -> 0x0054e5c0 (jmp) | ctx: 0x0054e5a9: push eax ; 0x0054e5aa: lea ecx, [edi + 4] ; 0x0054e5ad: call 0x54e495 ; 0x0054e5b2: jmp 0x54e5c0

### 0x00550ff0
- blocks=1, insns=15, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerFleeBehaviorProps@GGL@@ slot 1 (target 0x0055101d, vtable 0x00772a54)
  - rtti_vtable_method: .?AVCWorkerBehaviorProps@GGL@@ slot 1 (target 0x0055101d, vtable 0x00772b84)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehaviorProps@GGL@@ slot 1 (target 0x0055101d, vtable 0x00773538)
  - rtti_vtable_method: .?AVCCampBehaviorProperties@GGL@@ slot 1 (target 0x0055101d, vtable 0x00777848)
  - rtti_vtable_method: .?AVCCamperBehaviorProperties@GGL@@ slot 1 (target 0x0055101d, vtable 0x007777c8)
- branch points:
  - none

### 0x0055128b
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00550ff0 at 0x0055128e)
- branch points:
  - 0x00551298: je -> 0x005512a1 (jcc_true) | ctx: 0x0055128c: mov esi, ecx ; 0x0055128e: call 0x550fe5 ; 0x00551293: test byte ptr [esp + 8], 1 ; 0x00551298: je 0x5512a1
  - 0x00551298: je -> 0x0055129a (jcc_false) | ctx: 0x0055128c: mov esi, ecx ; 0x0055128e: call 0x550fe5 ; 0x00551293: test byte ptr [esp + 8], 1 ; 0x00551298: je 0x5512a1

### 0x005516e5
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0055128b at 0x005516e8)
  - caller_of_anchor_path: depth 3 (calls 0x00551b7b at 0x005518e3)
  - caller_of_anchor_path: depth 3 (calls 0x00551b7b at 0x00551986)
- branch points:
  - 0x005516f2: je -> 0x005516fb (jcc_true) | ctx: 0x005516e6: mov esi, ecx ; 0x005516e8: call 0x5512a7 ; 0x005516ed: test byte ptr [esp + 8], 1 ; 0x005516f2: je 0x5516fb
  - 0x005516f2: je -> 0x005516f4 (jcc_false) | ctx: 0x005516e6: mov esi, ecx ; 0x005516e8: call 0x5512a7 ; 0x005516ed: test byte ptr [esp + 8], 1 ; 0x005516f2: je 0x5516fb

### 0x00551b7b
- blocks=4, insns=25, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00516b3a at 0x00551d97)
- branch points:
  - 0x00551b83: jne -> 0x00551b8b (jcc_true) | ctx: 0x00551b7c: mov ebp, esp ; 0x00551b7e: push ecx ; 0x00551b7f: cmp dword ptr [ebp + 0xc], 0 ; 0x00551b83: jne 0x551b8b
  - 0x00551b83: jne -> 0x00551b85 (jcc_false) | ctx: 0x00551b7c: mov ebp, esp ; 0x00551b7e: push ecx ; 0x00551b7f: cmp dword ptr [ebp + 0xc], 0 ; 0x00551b83: jne 0x551b8b
  - 0x00551b89: jbe -> 0x00551bb5 (jcc_true) | ctx: 0x00551b85: cmp dword ptr [ebp + 0x10], 0 ; 0x00551b89: jbe 0x551bb5
  - 0x00551b89: jbe -> 0x00551b8b (jcc_false) | ctx: 0x00551b85: cmp dword ptr [ebp + 0x10], 0 ; 0x00551b89: jbe 0x551bb5

### 0x00553339
- blocks=1, insns=16, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerFleeBehaviorProps@GGL@@ slot 2 (target 0x0055336a, vtable 0x00772a60)
  - rtti_vtable_method: .?AVCWorkerFleeBehavior@GGL@@ slot 2 (target 0x0055336a, vtable 0x007729fc)
  - rtti_vtable_method: .?AVCWorkerBehavior@GGL@@ slot 2 (target 0x0055336a, vtable 0x00772b30)
  - rtti_vtable_method: .?AVCWorkerBehaviorProps@GGL@@ slot 2 (target 0x0055336a, vtable 0x00772b90)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehaviorProps@GGL@@ slot 2 (target 0x0055336a, vtable 0x00773544)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehavior@GGL@@ slot 2 (target 0x0055336a, vtable 0x007734dc)
  - rtti_vtable_method: .?AVCPath@EGL@@ slot 2 (target 0x0055336a, vtable 0x0077452c)
  - rtti_vtable_method: .?AVCPath@GGL@@ slot 2 (target 0x0055336a, vtable 0x00774540)
  - rtti_vtable_method: .?AVCCamperBehavior@GGL@@ slot 2 (target 0x0055336a, vtable 0x0077777c)
  - rtti_vtable_method: .?AVCCampBehaviorProperties@GGL@@ slot 2 (target 0x0055336a, vtable 0x00777854)
  - rtti_vtable_method: .?AVCCamperBehaviorProperties@GGL@@ slot 2 (target 0x0055336a, vtable 0x007777d4)
  - rtti_vtable_method: .?AVCCampBehavior@GGL@@ slot 2 (target 0x0055336a, vtable 0x00777864)
- branch points:
  - none

### 0x00553468
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00553339 at 0x0055346b)
- branch points:
  - 0x00553475: je -> 0x0055347e (jcc_true) | ctx: 0x00553469: mov esi, ecx ; 0x0055346b: call 0x55332e ; 0x00553470: test byte ptr [esp + 8], 1 ; 0x00553475: je 0x55347e
  - 0x00553475: je -> 0x00553477 (jcc_false) | ctx: 0x00553469: mov esi, ecx ; 0x0055346b: call 0x55332e ; 0x00553470: test byte ptr [esp + 8], 1 ; 0x00553475: je 0x55347e

### 0x00570fd5
- blocks=3, insns=12, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00579631 at 0x0057108f)
- branch points:
  - 0x00570fdc: jne -> 0x00570fe6 (jcc_true) | ctx: 0x00570fd5: push esi ; 0x00570fd6: mov esi, ecx ; 0x00570fd8: cmp dword ptr [esi + 0x14], 0 ; 0x00570fdc: jne 0x570fe6
  - 0x00570fdc: jne -> 0x00570fde (jcc_false) | ctx: 0x00570fd5: push esi ; 0x00570fd6: mov esi, ecx ; 0x00570fd8: cmp dword ptr [esi + 0x14], 0 ; 0x00570fdc: jne 0x570fe6

### 0x00577a34
- blocks=3, insns=36, edges=8, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 3 (calls 0x00579a40 at 0x00577aa6)
  - caller_of_anchor_path: depth 3 (calls 0x00579a40 at 0x00577b65)
- branch points:
  - 0x00577a5c: je -> 0x00577a6c (jcc_true) | ctx: 0x00577a58: test edi, edi ; 0x00577a5a: pop ecx ; 0x00577a5b: pop ecx ; 0x00577a5c: je 0x577a6c
  - 0x00577a5c: je -> 0x00577a5e (jcc_false) | ctx: 0x00577a58: test edi, edi ; 0x00577a5a: pop ecx ; 0x00577a5b: pop ecx ; 0x00577a5c: je 0x577a6c

### 0x00577c12
- blocks=7, insns=47, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 3 (calls 0x00579a40 at 0x00577c97)
- branch points:
  - 0x00577c25: jmp -> 0x00577c44 (jmp) | ctx: 0x00577c1c: mov ebx, dword ptr [edi + 8] ; 0x00577c1f: mov esi, dword ptr [edi + 4] ; 0x00577c22: mov dword ptr [ebp - 4], ecx ; 0x00577c25: jmp 0x577c44
  - 0x00577c46: jne -> 0x00577c27 (jcc_true) | ctx: 0x00577c44: cmp esi, ebx ; 0x00577c46: jne 0x577c27
  - 0x00577c46: jne -> 0x00577c48 (jcc_false) | ctx: 0x00577c44: cmp esi, ebx ; 0x00577c46: jne 0x577c27
  - 0x00577c46: jne -> 0x00577c27 (jcc_true) | ctx: 0x00577c3c: call 0x577b41 ; 0x00577c41: add esi, 0x10 ; 0x00577c44: cmp esi, ebx ; 0x00577c46: jne 0x577c27
  - 0x00577c46: jne -> 0x00577c48 (jcc_false) | ctx: 0x00577c3c: call 0x577b41 ; 0x00577c41: add esi, 0x10 ; 0x00577c44: cmp esi, ebx ; 0x00577c46: jne 0x577c27
  - 0x00577c4e: je -> 0x00577c69 (jcc_true) | ctx: 0x00577c48: mov eax, dword ptr [ebp + 0x14] ; 0x00577c4b: test byte ptr [eax], 3 ; 0x00577c4e: je 0x577c69
  - 0x00577c4e: je -> 0x00577c50 (jcc_false) | ctx: 0x00577c48: mov eax, dword ptr [ebp + 0x14] ; 0x00577c4b: test byte ptr [eax], 3 ; 0x00577c4e: je 0x577c69
  - 0x00577c59: je -> 0x00577c69 (jcc_true) | ctx: 0x00577c50: mov ecx, edi ; 0x00577c52: call 0x4a2d04 ; 0x00577c57: test eax, eax ; 0x00577c59: je 0x577c69
  - 0x00577c59: je -> 0x00577c5b (jcc_false) | ctx: 0x00577c50: mov ecx, edi ; 0x00577c52: call 0x4a2d04 ; 0x00577c57: test eax, eax ; 0x00577c59: je 0x577c69

### 0x00577edf
- blocks=10, insns=76, edges=16, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00589a1d at 0x00577fc0)
- branch points:
  - 0x00577f15: jmp -> 0x00577f4e (jmp) | ctx: 0x00577f08: movzx esi, word ptr [esi + 4] ; 0x00577f0c: mov dword ptr [ebp - 4], 0x8000 ; 0x00577f13: mov eax, edi ; 0x00577f15: jmp 0x577f4e
  - 0x00577f54: jne -> 0x00577f17 (jcc_true) | ctx: 0x00577f4e: cmp esi, dword ptr [0x897620] ; 0x00577f54: jne 0x577f17
  - 0x00577f54: jne -> 0x00577f56 (jcc_false) | ctx: 0x00577f4e: cmp esi, dword ptr [0x897620] ; 0x00577f54: jne 0x577f17
  - 0x00577f31: jle -> 0x00577f3f (jcc_true) | ctx: 0x00577f2b: cmp dword ptr [ebp + 0xc], 0x1f ; 0x00577f2f: pop ecx ; 0x00577f30: pop ecx ; 0x00577f31: jle 0x577f3f
  - 0x00577f31: jle -> 0x00577f33 (jcc_false) | ctx: 0x00577f2b: cmp dword ptr [ebp + 0xc], 0x1f ; 0x00577f2f: pop ecx ; 0x00577f30: pop ecx ; 0x00577f31: jle 0x577f3f
  - 0x00577f5a: jle -> 0x00577f63 (jcc_true) | ctx: 0x00577f56: cmp dword ptr [ebx + 0xc], 2 ; 0x00577f5a: jle 0x577f63
  - 0x00577f5a: jle -> 0x00577f5c (jcc_false) | ctx: 0x00577f56: cmp dword ptr [ebx + 0xc], 2 ; 0x00577f5a: jle 0x577f63
  - 0x00577f4c: je -> 0x00577f6d (jcc_true) | ctx: 0x00577f42: mov ecx, dword ptr [ebp + 8] ; 0x00577f45: movzx esi, word ptr [ecx + esi*8 + 4] ; 0x00577f4a: mov eax, edi ; 0x00577f4c: je 0x577f6d
  - 0x00577f4c: je -> 0x00577f4e (jcc_false) | ctx: 0x00577f42: mov ecx, dword ptr [ebp + 8] ; 0x00577f45: movzx esi, word ptr [ecx + esi*8 + 4] ; 0x00577f4a: mov eax, edi ; 0x00577f4c: je 0x577f6d
  - 0x00577f4c: je -> 0x00577f6d (jcc_true) | ctx: 0x00577f42: mov ecx, dword ptr [ebp + 8] ; 0x00577f45: movzx esi, word ptr [ecx + esi*8 + 4] ; 0x00577f4a: mov eax, edi ; 0x00577f4c: je 0x577f6d
  - 0x00577f4c: je -> 0x00577f4e (jcc_false) | ctx: 0x00577f42: mov ecx, dword ptr [ebp + 8] ; 0x00577f45: movzx esi, word ptr [ecx + esi*8 + 4] ; 0x00577f4a: mov eax, edi ; 0x00577f4c: je 0x577f6d
  - 0x00577f88: jmp -> 0x00577f66 (jmp) | ctx: 0x00577f78: mov dword ptr [ebx + 0x10], 0x1f ; 0x00577f7f: mov byte ptr [ebx + 0x98], 0 ; 0x00577f86: xor eax, eax ; 0x00577f88: jmp 0x577f66

### 0x00579631
- blocks=4, insns=49, edges=10, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0057efde at 0x00579925)
  - caller_of_anchor_path: depth 1 (calls 0x0057efde at 0x00579935)
  - caller_of_anchor_path: depth 1 (calls 0x0057efde at 0x00579945)
  - caller_of_anchor_path: depth 1 (calls 0x0057efde at 0x00579955)
  - caller_of_anchor_path: depth 2 (calls 0x0058024d at 0x00579970)
  - caller_of_anchor_path: depth 3 (calls 0x0058bbce at 0x005799f9)
- branch points:
  - 0x00579643: je -> 0x0057969d (jcc_true) | ctx: 0x0057963a: mov esi, ecx ; 0x0057963c: call 0x5785bc ; 0x00579641: test al, al ; 0x00579643: je 0x57969d
  - 0x00579643: je -> 0x00579645 (jcc_false) | ctx: 0x0057963a: mov esi, ecx ; 0x0057963c: call 0x5785bc ; 0x00579641: test al, al ; 0x00579643: je 0x57969d
  - 0x0057966a: je -> 0x0057969d (jcc_true) | ctx: 0x00579660: push dword ptr [ebp - 8] ; 0x00579663: call 0x449d52 ; 0x00579668: test al, al ; 0x0057966a: je 0x57969d
  - 0x0057966a: je -> 0x0057966c (jcc_false) | ctx: 0x00579660: push dword ptr [ebp - 8] ; 0x00579663: call 0x449d52 ; 0x00579668: test al, al ; 0x0057966a: je 0x57969d

### 0x00579a40
- blocks=1, insns=64, edges=7, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00579631 at 0x00579af2)
  - caller_of_anchor_path: depth 2 (calls 0x0058024d at 0x00579ad9)
  - caller_of_anchor_path: depth 3 (calls 0x00579a40 at 0x00579b3e)
  - caller_of_anchor_path: depth 3 (calls 0x00579a40 at 0x00579c04)
  - caller_of_anchor_path: depth 3 (calls 0x00579a40 at 0x00579cc8)
- branch points:
  - none

### 0x0057efde
- blocks=20, insns=235, edges=45, jcc=15, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCBlockingStatusPredicate@EGL@@ slot 1 (target 0x0057f232, vtable 0x00783b90)
  - rtti_vtable_method: .?AVCUnblockedInSectorPredicate@EGL@@ slot 1 (target 0x0057f283, vtable 0x0078418c)
- branch points:
  - 0x0057efeb: jne -> 0x0057eff8 (jcc_true) | ctx: 0x0057efe4: mov eax, dword ptr [ebp + 8] ; 0x0057efe7: mov eax, dword ptr [eax] ; 0x0057efe9: test eax, eax ; 0x0057efeb: jne 0x57eff8
  - 0x0057efeb: jne -> 0x0057efed (jcc_false) | ctx: 0x0057efe4: mov eax, dword ptr [ebp + 8] ; 0x0057efe7: mov eax, dword ptr [eax] ; 0x0057efe9: test eax, eax ; 0x0057efeb: jne 0x57eff8
  - 0x0057effe: je -> 0x0057f1db (jcc_true) | ctx: 0x0057eff8: push esi ; 0x0057eff9: mov esi, dword ptr [ebp + 0x10] ; 0x0057effc: test esi, esi ; 0x0057effe: je 0x57f1db
  - 0x0057effe: je -> 0x0057f004 (jcc_false) | ctx: 0x0057eff8: push esi ; 0x0057eff9: mov esi, dword ptr [ebp + 0x10] ; 0x0057effc: test esi, esi ; 0x0057effe: je 0x57f1db
  - 0x0057eff2: je -> 0x0057f1dc (jcc_true) | ctx: 0x0057efed: mov ecx, dword ptr [ebp + 0xc] ; 0x0057eff0: cmp dword ptr [ecx], eax ; 0x0057eff2: je 0x57f1dc
  - 0x0057eff2: je -> 0x0057eff8 (jcc_false) | ctx: 0x0057efed: mov ecx, dword ptr [ebp + 0xc] ; 0x0057eff0: cmp dword ptr [ecx], eax ; 0x0057eff2: je 0x57f1dc
  - 0x0057f026: jge -> 0x0057f060 (jcc_true) | ctx: 0x0057f01b: cmp esi, 0xffa60000 ; 0x0057f021: mov ebx, eax ; 0x0057f023: mov dword ptr [ebp - 0x14], edx ; 0x0057f026: jge 0x57f060
  - 0x0057f026: jge -> 0x0057f028 (jcc_false) | ctx: 0x0057f01b: cmp esi, 0xffa60000 ; 0x0057f021: mov ebx, eax ; 0x0057f023: mov dword ptr [ebp - 0x14], edx ; 0x0057f026: jge 0x57f060
  - 0x0057f066: jle -> 0x0057f09f (jcc_true) | ctx: 0x0057f060: cmp esi, 0x5a0000 ; 0x0057f066: jle 0x57f09f
  - 0x0057f066: jle -> 0x0057f068 (jcc_false) | ctx: 0x0057f060: cmp esi, 0x5a0000 ; 0x0057f066: jle 0x57f09f
  - 0x0057f05e: jne -> 0x0057f043 (jcc_true) | ctx: 0x0057f058: neg ecx ; 0x0057f05a: dec eax ; 0x0057f05b: mov dword ptr [ebp - 0x14], ecx ; 0x0057f05e: jne 0x57f043
  - 0x0057f05e: jne -> 0x0057f060 (jcc_false) | ctx: 0x0057f058: neg ecx ; 0x0057f05a: dec eax ; 0x0057f05b: mov dword ptr [ebp - 0x14], ecx ; 0x0057f05e: jne 0x57f043
  - 0x0057f0a5: jge -> 0x0057f0d0 (jcc_true) | ctx: 0x0057f09f: test esi, esi ; 0x0057f0a1: push 0 ; 0x0057f0a3: push 2 ; 0x0057f0a5: jge 0x57f0d0
  - 0x0057f0a5: jge -> 0x0057f0a7 (jcc_false) | ctx: 0x0057f09f: test esi, esi ; 0x0057f0a1: push 0 ; 0x0057f0a3: push 2 ; 0x0057f0a5: jge 0x57f0d0
  - 0x0057f09d: jne -> 0x0057f082 (jcc_true) | ctx: 0x0057f097: neg ecx ; 0x0057f099: dec eax ; 0x0057f09a: mov dword ptr [ebp - 0x14], ecx ; 0x0057f09d: jne 0x57f082
  - 0x0057f09d: jne -> 0x0057f09f (jcc_false) | ctx: 0x0057f097: neg ecx ; 0x0057f099: dec eax ; 0x0057f09a: mov dword ptr [ebp - 0x14], ecx ; 0x0057f09d: jne 0x57f082
  - 0x0057f05e: jne -> 0x0057f043 (jcc_true) | ctx: 0x0057f058: neg ecx ; 0x0057f05a: dec eax ; 0x0057f05b: mov dword ptr [ebp - 0x14], ecx ; 0x0057f05e: jne 0x57f043
  - 0x0057f05e: jne -> 0x0057f060 (jcc_false) | ctx: 0x0057f058: neg ecx ; 0x0057f05a: dec eax ; 0x0057f05b: mov dword ptr [ebp - 0x14], ecx ; 0x0057f05e: jne 0x57f043
  - 0x0057f124: jge -> 0x0057f152 (jcc_true) | ctx: 0x0057f11b: mov eax, ebx ; 0x0057f11d: call 0x5c5cf0 ; 0x0057f122: test esi, esi ; 0x0057f124: jge 0x57f152
  - 0x0057f124: jge -> 0x0057f126 (jcc_false) | ctx: 0x0057f11b: mov eax, ebx ; 0x0057f11d: call 0x5c5cf0 ; 0x0057f122: test esi, esi ; 0x0057f124: jge 0x57f152
  - 0x0057f0ce: jmp -> 0x0057f10c (jmp) | ctx: 0x0057f0c2: add esi, dword ptr [0x836620] ; 0x0057f0c8: mov dword ptr [ebp - 0x10], eax ; 0x0057f0cb: mov dword ptr [ebp - 0xc], edx ; 0x0057f0ce: jmp 0x57f10c
  - 0x0057f09d: jne -> 0x0057f082 (jcc_true) | ctx: 0x0057f097: neg ecx ; 0x0057f099: dec eax ; 0x0057f09a: mov dword ptr [ebp - 0x14], ecx ; 0x0057f09d: jne 0x57f082
  - 0x0057f09d: jne -> 0x0057f09f (jcc_false) | ctx: 0x0057f097: neg ecx ; 0x0057f099: dec eax ; 0x0057f09a: mov dword ptr [ebp - 0x14], ecx ; 0x0057f09d: jne 0x57f082
  - 0x0057f18d: jle -> 0x0057f115 (jcc_true) | ctx: 0x0057f183: inc dword ptr [ebp - 4] ; 0x0057f186: cmp dword ptr [ebp - 4], 0x16 ; 0x0057f18a: mov dword ptr [ebp - 0xc], eax ; 0x0057f18d: jle 0x57f115
  - 0x0057f18d: jle -> 0x0057f18f (jcc_false) | ctx: 0x0057f183: inc dword ptr [ebp - 4] ; 0x0057f186: cmp dword ptr [ebp - 4], 0x16 ; 0x0057f18a: mov dword ptr [ebp - 0xc], eax ; 0x0057f18d: jle 0x57f115
  - 0x0057f150: jmp -> 0x0057f180 (jmp) | ctx: 0x0057f148: add esi, dword ptr [edi] ; 0x0057f14a: mov dword ptr [ebp - 0x10], eax ; 0x0057f14d: mov eax, dword ptr [ebp - 0x1c] ; 0x0057f150: jmp 0x57f180
  - 0x0057f124: jge -> 0x0057f152 (jcc_true) | ctx: 0x0057f11b: mov eax, ebx ; 0x0057f11d: call 0x5c5cf0 ; 0x0057f122: test esi, esi ; 0x0057f124: jge 0x57f152
  - 0x0057f124: jge -> 0x0057f126 (jcc_false) | ctx: 0x0057f11b: mov eax, ebx ; 0x0057f11d: call 0x5c5cf0 ; 0x0057f122: test esi, esi ; 0x0057f124: jge 0x57f152
  - 0x0057f124: jge -> 0x0057f152 (jcc_true) | ctx: 0x0057f11b: mov eax, ebx ; 0x0057f11d: call 0x5c5cf0 ; 0x0057f122: test esi, esi ; 0x0057f124: jge 0x57f152
  - 0x0057f124: jge -> 0x0057f126 (jcc_false) | ctx: 0x0057f11b: mov eax, ebx ; 0x0057f11d: call 0x5c5cf0 ; 0x0057f122: test esi, esi ; 0x0057f124: jge 0x57f152
  - 0x0057f18d: jle -> 0x0057f115 (jcc_true) | ctx: 0x0057f183: inc dword ptr [ebp - 4] ; 0x0057f186: cmp dword ptr [ebp - 4], 0x16 ; 0x0057f18a: mov dword ptr [ebp - 0xc], eax ; 0x0057f18d: jle 0x57f115
  - 0x0057f18d: jle -> 0x0057f18f (jcc_false) | ctx: 0x0057f183: inc dword ptr [ebp - 4] ; 0x0057f186: cmp dword ptr [ebp - 4], 0x16 ; 0x0057f18a: mov dword ptr [ebp - 0xc], eax ; 0x0057f18d: jle 0x57f115

### 0x0057f2e1
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCBuildBlockedOnlyPredicate@?A0xfc60cb98@GGL@@ slot 0 (target 0x0057f2e1, vtable 0x0076ea58)
  - rtti_vtable_method: .?AVCPotentialCampSitePredicate@GGL@@ slot 0 (target 0x0057f2e1, vtable 0x007777a0)
  - rtti_vtable_method: .?AVCBlockingStatusPredicate@EGL@@ slot 0 (target 0x0057f2e1, vtable 0x00783b90)
  - rtti_vtable_method: .?AVCUnblockedInSectorPredicate@EGL@@ slot 0 (target 0x0057f2e1, vtable 0x0078418c)
  - rtti_vtable_method: .?AVCUnblockedInLargeSectorPredicate@EGL@@ slot 0 (target 0x0057f2e1, vtable 0x00784198)
  - rtti_vtable_method: .?AVCUnblockedInLargeSectorPredicate@EGL@@ slot 1 (target 0x0057f2fd, vtable 0x00784198)
- branch points:
  - 0x0057f2ee: je -> 0x0057f2f7 (jcc_true) | ctx: 0x0057f2e2: mov esi, ecx ; 0x0057f2e4: call 0x4ffe6e ; 0x0057f2e9: test byte ptr [esp + 8], 1 ; 0x0057f2ee: je 0x57f2f7
  - 0x0057f2ee: je -> 0x0057f2f0 (jcc_false) | ctx: 0x0057f2e2: mov esi, ecx ; 0x0057f2e4: call 0x4ffe6e ; 0x0057f2e9: test byte ptr [esp + 8], 1 ; 0x0057f2ee: je 0x57f2f7

### 0x0057fa63
- blocks=1, insns=12, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCUnblockedAreasPredicate@EGL@@ slot 1 (target 0x0057fa80, vtable 0x007841a4)
- branch points:
  - none

### 0x0057fa9f
- blocks=1, insns=8, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0057fa63 at 0x0057fac3)
  - caller_of_anchor_path: depth 2 (calls 0x0057fa9f at 0x0057fc2a)
  - caller_of_anchor_path: depth 2 (calls 0x0057fa9f at 0x0057fcdb)
- branch points:
  - none

### 0x0057fe7c
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCUnblockedAreasPredicate@EGL@@ slot 0 (target 0x0057fe7c, vtable 0x007841a4)
  - caller_of_anchor_path: depth 1 (calls 0x0057fe7c at 0x0057fe7f)
- branch points:
  - 0x0057fe89: je -> 0x0057fe92 (jcc_true) | ctx: 0x0057fe7d: mov esi, ecx ; 0x0057fe7f: call 0x57fe63 ; 0x0057fe84: test byte ptr [esp + 8], 1 ; 0x0057fe89: je 0x57fe92
  - 0x0057fe89: je -> 0x0057fe8b (jcc_false) | ctx: 0x0057fe7d: mov esi, ecx ; 0x0057fe7f: call 0x57fe63 ; 0x0057fe84: test byte ptr [esp + 8], 1 ; 0x0057fe89: je 0x57fe92

### 0x0057fe98
- blocks=4, insns=31, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fa9f at 0x0057febb)
- branch points:
  - 0x0057feb4: jae -> 0x0057fec5 (jcc_true) | ctx: 0x0057fead: cmp edi, eax ; 0x0057feaf: push dword ptr [ebp + 8] ; 0x0057feb2: mov ecx, esi ; 0x0057feb4: jae 0x57fec5
  - 0x0057feb4: jae -> 0x0057feb6 (jcc_false) | ctx: 0x0057fead: cmp edi, eax ; 0x0057feaf: push dword ptr [ebp + 8] ; 0x0057feb2: mov ecx, esi ; 0x0057feb4: jae 0x57fec5
  - 0x0057fec3: jmp -> 0x0057fed2 (jmp) | ctx: 0x0057feb8: push dword ptr [esi + 8] ; 0x0057febb: call 0x57fab2 ; 0x0057fec0: mov dword ptr [esi + 8], eax ; 0x0057fec3: jmp 0x57fed2

### 0x0057fed8
- blocks=1, insns=5, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCUnblockedBuildingAreasPredicate@EGL@@ slot 1 (target 0x0057fed8, vtable 0x007841b0)
- branch points:
  - none

### 0x0057fee2
- blocks=11, insns=64, edges=21, jcc=8, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0057fa63 at 0x0057ff36)
  - caller_of_anchor_path: depth 1 (calls 0x0057fe7c at 0x0057ff47)
  - caller_of_anchor_path: depth 2 (calls 0x0057fa9f at 0x0057ff36)
  - caller_of_anchor_path: depth 3 (calls 0x0057fe98 at 0x0057ff47)
- branch points:
  - 0x0057fef8: jg -> 0x0057ff5a (jcc_true) | ctx: 0x0057feef: mov dword ptr [ebp + 0xc], eax ; 0x0057fef2: mov eax, dword ptr [ebp + 0xc] ; 0x0057fef5: cmp dword ptr [ebp - 0xb], eax ; 0x0057fef8: jg 0x57ff5a
  - 0x0057fef8: jg -> 0x0057fefa (jcc_false) | ctx: 0x0057feef: mov dword ptr [ebp + 0xc], eax ; 0x0057fef2: mov eax, dword ptr [ebp + 0xc] ; 0x0057fef5: cmp dword ptr [ebp - 0xb], eax ; 0x0057fef8: jg 0x57ff5a
  - 0x0057ff01: jmp -> 0x0057ff4f (jmp) | ctx: 0x0057fefa: mov eax, dword ptr [ebp + 8] ; 0x0057fefd: dec eax ; 0x0057fefe: mov dword ptr [ebp - 0xf], eax ; 0x0057ff01: jmp 0x57ff4f
  - 0x0057ff51: jne -> 0x0057ff03 (jcc_true) | ctx: 0x0057ff4f: test bl, bl ; 0x0057ff51: jne 0x57ff03
  - 0x0057ff51: jne -> 0x0057ff53 (jcc_false) | ctx: 0x0057ff4f: test bl, bl ; 0x0057ff51: jne 0x57ff03
  - 0x0057ff0a: jg -> 0x0057ff53 (jcc_true) | ctx: 0x0057ff03: mov eax, dword ptr [ebp + 8] ; 0x0057ff06: inc eax ; 0x0057ff07: cmp dword ptr [ebp - 0xf], eax ; 0x0057ff0a: jg 0x57ff53
  - 0x0057ff0a: jg -> 0x0057ff0c (jcc_false) | ctx: 0x0057ff03: mov eax, dword ptr [ebp + 8] ; 0x0057ff06: inc eax ; 0x0057ff07: cmp dword ptr [ebp - 0xf], eax ; 0x0057ff0a: jg 0x57ff53
  - 0x0057ff58: jne -> 0x0057fef2 (jcc_true) | ctx: 0x0057ff53: inc dword ptr [ebp - 0xb] ; 0x0057ff56: test bl, bl ; 0x0057ff58: jne 0x57fef2
  - 0x0057ff58: jne -> 0x0057ff5a (jcc_false) | ctx: 0x0057ff53: inc dword ptr [ebp - 0xb] ; 0x0057ff56: test bl, bl ; 0x0057ff58: jne 0x57fef2
  - 0x0057ff28: je -> 0x0057ff2e (jcc_true) | ctx: 0x0057ff21: mov eax, dword ptr [eax] ; 0x0057ff23: add esp, 0x10 ; 0x0057ff26: cmp eax, edi ; 0x0057ff28: je 0x57ff2e
  - 0x0057ff28: je -> 0x0057ff2a (jcc_false) | ctx: 0x0057ff21: mov eax, dword ptr [eax] ; 0x0057ff23: add esp, 0x10 ; 0x0057ff26: cmp eax, edi ; 0x0057ff28: je 0x57ff2e
  - 0x0057fef8: jg -> 0x0057ff5a (jcc_true) | ctx: 0x0057fef2: mov eax, dword ptr [ebp + 0xc] ; 0x0057fef5: cmp dword ptr [ebp - 0xb], eax ; 0x0057fef8: jg 0x57ff5a
  - 0x0057fef8: jg -> 0x0057fefa (jcc_false) | ctx: 0x0057fef2: mov eax, dword ptr [ebp + 0xc] ; 0x0057fef5: cmp dword ptr [ebp - 0xb], eax ; 0x0057fef8: jg 0x57ff5a
  - 0x0057ff51: jne -> 0x0057ff03 (jcc_true) | ctx: 0x0057ff47: call 0x57fe98 ; 0x0057ff4c: inc dword ptr [ebp - 0xf] ; 0x0057ff4f: test bl, bl ; 0x0057ff51: jne 0x57ff03
  - 0x0057ff51: jne -> 0x0057ff53 (jcc_false) | ctx: 0x0057ff47: call 0x57fe98 ; 0x0057ff4c: inc dword ptr [ebp - 0xf] ; 0x0057ff4f: test bl, bl ; 0x0057ff51: jne 0x57ff03
  - 0x0057ff2c: jmp -> 0x0057ff4c (jmp) | ctx: 0x0057ff2a: mov bl, byte ptr [eax] ; 0x0057ff2c: jmp 0x57ff4c
  - 0x0057ff51: jne -> 0x0057ff03 (jcc_true) | ctx: 0x0057ff4c: inc dword ptr [ebp - 0xf] ; 0x0057ff4f: test bl, bl ; 0x0057ff51: jne 0x57ff03
  - 0x0057ff51: jne -> 0x0057ff53 (jcc_false) | ctx: 0x0057ff4c: inc dword ptr [ebp - 0xf] ; 0x0057ff4f: test bl, bl ; 0x0057ff51: jne 0x57ff03

### 0x0058024d
- blocks=11, insns=206, edges=34, jcc=10, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0057efde at 0x005802b8)
  - caller_of_anchor_path: depth 1 (calls 0x0057efde at 0x005802c6)
  - caller_of_anchor_path: depth 1 (calls 0x0057efde at 0x005802d4)
  - caller_of_anchor_path: depth 1 (calls 0x0057efde at 0x005802e2)
  - caller_of_anchor_path: depth 2 (calls 0x0057fa9f at 0x00580254)
  - caller_of_anchor_path: depth 2 (calls 0x0057fa9f at 0x00580260)
- branch points:
  - 0x0058027d: jge -> 0x00580284 (jcc_true) | ctx: 0x00580273: mov eax, dword ptr [ebp + 0xc] ; 0x00580276: mov byte ptr [ebp - 4], 1 ; 0x0058027a: mov dword ptr [esi + 0x24], eax ; 0x0058027d: jge 0x580284
  - 0x0058027d: jge -> 0x0058027f (jcc_false) | ctx: 0x00580273: mov eax, dword ptr [ebp + 0xc] ; 0x00580276: mov byte ptr [ebp - 4], 1 ; 0x0058027a: mov dword ptr [esi + 0x24], eax ; 0x0058027d: jge 0x580284
  - 0x0058028e: jge -> 0x00580294 (jcc_true) | ctx: 0x00580287: mov ecx, dword ptr [ebp + 0x1c] ; 0x0058028a: cmp ecx, ebx ; 0x0058028c: mov eax, ebx ; 0x0058028e: jge 0x580294
  - 0x0058028e: jge -> 0x00580290 (jcc_false) | ctx: 0x00580287: mov ecx, dword ptr [ebp + 0x1c] ; 0x0058028a: cmp ecx, ebx ; 0x0058028c: mov eax, ebx ; 0x0058028e: jge 0x580294
  - 0x0058028e: jge -> 0x00580294 (jcc_true) | ctx: 0x00580287: mov ecx, dword ptr [ebp + 0x1c] ; 0x0058028a: cmp ecx, ebx ; 0x0058028c: mov eax, ebx ; 0x0058028e: jge 0x580294
  - 0x0058028e: jge -> 0x00580290 (jcc_false) | ctx: 0x00580287: mov ecx, dword ptr [ebp + 0x1c] ; 0x0058028a: cmp ecx, ebx ; 0x0058028c: mov eax, ebx ; 0x0058028e: jge 0x580294
  - 0x00580305: je -> 0x0058034c (jcc_true) | ctx: 0x005802fc: mov ebx, dword ptr [ebp + edx*4 - 0x20] ; 0x00580300: cmp edi, ebx ; 0x00580302: mov dword ptr [ebp + 0x10], edx ; 0x00580305: je 0x58034c
  - 0x00580305: je -> 0x00580307 (jcc_false) | ctx: 0x005802fc: mov ebx, dword ptr [ebp + edx*4 - 0x20] ; 0x00580300: cmp edi, ebx ; 0x00580302: mov dword ptr [ebp + 0x10], edx ; 0x00580305: je 0x58034c
  - 0x00580305: je -> 0x0058034c (jcc_true) | ctx: 0x005802fc: mov ebx, dword ptr [ebp + edx*4 - 0x20] ; 0x00580300: cmp edi, ebx ; 0x00580302: mov dword ptr [ebp + 0x10], edx ; 0x00580305: je 0x58034c
  - 0x00580305: je -> 0x00580307 (jcc_false) | ctx: 0x005802fc: mov ebx, dword ptr [ebp + edx*4 - 0x20] ; 0x00580300: cmp edi, ebx ; 0x00580302: mov dword ptr [ebp + 0x10], edx ; 0x00580305: je 0x58034c
  - 0x00580352: jl -> 0x005802ec (jcc_true) | ctx: 0x0058034c: mov ecx, dword ptr [ebp + 0x1c] ; 0x0058034f: cmp ecx, 4 ; 0x00580352: jl 0x5802ec
  - 0x00580352: jl -> 0x00580354 (jcc_false) | ctx: 0x0058034c: mov ecx, dword ptr [ebp + 0x1c] ; 0x0058034f: cmp ecx, 4 ; 0x00580352: jl 0x5802ec
  - 0x00580309: jle -> 0x0058030f (jcc_true) | ctx: 0x00580307: mov eax, ecx ; 0x00580309: jle 0x58030f
  - 0x00580309: jle -> 0x0058030b (jcc_false) | ctx: 0x00580307: mov eax, ecx ; 0x00580309: jle 0x58030f
  - 0x00580305: je -> 0x0058034c (jcc_true) | ctx: 0x005802fc: mov ebx, dword ptr [ebp + edx*4 - 0x20] ; 0x00580300: cmp edi, ebx ; 0x00580302: mov dword ptr [ebp + 0x10], edx ; 0x00580305: je 0x58034c
  - 0x00580305: je -> 0x00580307 (jcc_false) | ctx: 0x005802fc: mov ebx, dword ptr [ebp + edx*4 - 0x20] ; 0x00580300: cmp edi, ebx ; 0x00580302: mov dword ptr [ebp + 0x10], edx ; 0x00580305: je 0x58034c
  - 0x00580352: jl -> 0x005802ec (jcc_true) | ctx: 0x00580347: call 0x57fdf2 ; 0x0058034c: mov ecx, dword ptr [ebp + 0x1c] ; 0x0058034f: cmp ecx, 4 ; 0x00580352: jl 0x5802ec
  - 0x00580352: jl -> 0x00580354 (jcc_false) | ctx: 0x00580347: call 0x57fdf2 ; 0x0058034c: mov ecx, dword ptr [ebp + 0x1c] ; 0x0058034f: cmp ecx, 4 ; 0x00580352: jl 0x5802ec
  - 0x00580352: jl -> 0x005802ec (jcc_true) | ctx: 0x00580347: call 0x57fdf2 ; 0x0058034c: mov ecx, dword ptr [ebp + 0x1c] ; 0x0058034f: cmp ecx, 4 ; 0x00580352: jl 0x5802ec
  - 0x00580352: jl -> 0x00580354 (jcc_false) | ctx: 0x00580347: call 0x57fdf2 ; 0x0058034c: mov ecx, dword ptr [ebp + 0x1c] ; 0x0058034f: cmp ecx, 4 ; 0x00580352: jl 0x5802ec

### 0x005803cf
- blocks=4, insns=135, edges=24, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0058024d at 0x0058047d)
  - caller_of_anchor_path: depth 3 (calls 0x005803cf at 0x005804e7)
- branch points:
  - 0x0058041a: je -> 0x005804b6 (jcc_true) | ctx: 0x00580412: mov edi, dword ptr [eax + 4] ; 0x00580415: cmp edi, ecx ; 0x00580417: mov dword ptr [ebp - 0x1c], ecx ; 0x0058041a: je 0x5804b6
  - 0x0058041a: je -> 0x00580420 (jcc_false) | ctx: 0x00580412: mov edi, dword ptr [eax + 4] ; 0x00580415: cmp edi, ecx ; 0x00580417: mov dword ptr [ebp - 0x1c], ecx ; 0x0058041a: je 0x5804b6
  - 0x005804b0: jne -> 0x00580426 (jcc_true) | ctx: 0x005804a6: add dword ptr [ebp + 0x10], 0x10 ; 0x005804aa: add edi, 0x10 ; 0x005804ad: cmp edi, dword ptr [ebp - 0x1c] ; 0x005804b0: jne 0x580426
  - 0x005804b0: jne -> 0x005804b6 (jcc_false) | ctx: 0x005804a6: add dword ptr [ebp + 0x10], 0x10 ; 0x005804aa: add edi, 0x10 ; 0x005804ad: cmp edi, dword ptr [ebp - 0x1c] ; 0x005804b0: jne 0x580426
  - 0x005804b0: jne -> 0x00580426 (jcc_true) | ctx: 0x005804a6: add dword ptr [ebp + 0x10], 0x10 ; 0x005804aa: add edi, 0x10 ; 0x005804ad: cmp edi, dword ptr [ebp - 0x1c] ; 0x005804b0: jne 0x580426
  - 0x005804b0: jne -> 0x005804b6 (jcc_false) | ctx: 0x005804a6: add dword ptr [ebp + 0x10], 0x10 ; 0x005804aa: add edi, 0x10 ; 0x005804ad: cmp edi, dword ptr [ebp - 0x1c] ; 0x005804b0: jne 0x580426

### 0x0058051f
- blocks=3, insns=14, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCUnblockedBuildingAreasPredicate@EGL@@ slot 0 (target 0x0058051f, vtable 0x007841b0)
  - caller_of_anchor_path: depth 1 (calls 0x0058051f at 0x00580522)
- branch points:
  - 0x0058052c: je -> 0x00580535 (jcc_true) | ctx: 0x00580520: mov esi, ecx ; 0x00580522: call 0x58053b ; 0x00580527: test byte ptr [esp + 8], 1 ; 0x0058052c: je 0x580535
  - 0x0058052c: je -> 0x0058052e (jcc_false) | ctx: 0x00580520: mov esi, ecx ; 0x00580522: call 0x58053b ; 0x00580527: test byte ptr [esp + 8], 1 ; 0x0058052c: je 0x580535

### 0x00582db4
- blocks=12, insns=81, edges=31, jcc=8, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCPath@EGL@@ slot 3 (target 0x00582e72, vtable 0x0077452c)
  - rtti_vtable_method: .?AVCPath@GGL@@ slot 3 (target 0x00582e72, vtable 0x00774540)
- branch points:
  - 0x00582dd9: jne -> 0x00582de2 (jcc_true) | ctx: 0x00582dd3: push ebx ; 0x00582dd4: push dword ptr [ebp + 8] ; 0x00582dd7: mov ecx, esi ; 0x00582dd9: jne 0x582de2
  - 0x00582dd9: jne -> 0x00582ddb (jcc_false) | ctx: 0x00582dd3: push ebx ; 0x00582dd4: push dword ptr [ebp + 8] ; 0x00582dd7: mov ecx, esi ; 0x00582dd9: jne 0x582de2
  - 0x00582dfb: je -> 0x00582e6b (jcc_true) | ctx: 0x00582df1: mov dword ptr [ebp - 4], ebx ; 0x00582df4: call 0x5bc0d0 ; 0x00582df9: test eax, eax ; 0x00582dfb: je 0x582e6b
  - 0x00582dfb: je -> 0x00582dfd (jcc_false) | ctx: 0x00582df1: mov dword ptr [ebp - 4], ebx ; 0x00582df4: call 0x5bc0d0 ; 0x00582df9: test eax, eax ; 0x00582dfb: je 0x582e6b
  - 0x00582de0: jmp -> 0x00582de7 (jmp) | ctx: 0x00582ddb: call 0x582bba ; 0x00582de0: jmp 0x582de7
  - 0x00582e07: je -> 0x00582e3f (jcc_true) | ctx: 0x00582dfd: mov ecx, edi ; 0x00582dff: call 0x5bc0d0 ; 0x00582e04: cmp eax, 1 ; 0x00582e07: je 0x582e3f
  - 0x00582e07: je -> 0x00582e09 (jcc_false) | ctx: 0x00582dfd: mov ecx, edi ; 0x00582dff: call 0x5bc0d0 ; 0x00582e04: cmp eax, 1 ; 0x00582e07: je 0x582e3f
  - 0x00582dfb: je -> 0x00582e6b (jcc_true) | ctx: 0x00582df1: mov dword ptr [ebp - 4], ebx ; 0x00582df4: call 0x5bc0d0 ; 0x00582df9: test eax, eax ; 0x00582dfb: je 0x582e6b
  - 0x00582dfb: je -> 0x00582dfd (jcc_false) | ctx: 0x00582df1: mov dword ptr [ebp - 4], ebx ; 0x00582df4: call 0x5bc0d0 ; 0x00582df9: test eax, eax ; 0x00582dfb: je 0x582e6b
  - 0x00582e43: jne -> 0x00582e60 (jcc_true) | ctx: 0x00582e3f: cmp dword ptr [ebp + 0x10], 1 ; 0x00582e43: jne 0x582e60
  - 0x00582e43: jne -> 0x00582e45 (jcc_false) | ctx: 0x00582e3f: cmp dword ptr [ebp + 0x10], 1 ; 0x00582e43: jne 0x582e60
  - 0x00582e0d: je -> 0x00582e45 (jcc_true) | ctx: 0x00582e09: cmp dword ptr [ebp + 0x10], 1 ; 0x00582e0d: je 0x582e45
  - 0x00582e0d: je -> 0x00582e0f (jcc_false) | ctx: 0x00582e09: cmp dword ptr [ebp + 0x10], 1 ; 0x00582e0d: je 0x582e45
  - 0x00582e5e: jne -> 0x00582e6b (jcc_true) | ctx: 0x00582e54: lea ecx, [ebp - 8] ; 0x00582e57: call 0x4cb7b0 ; 0x00582e5c: test al, al ; 0x00582e5e: jne 0x582e6b
  - 0x00582e5e: jne -> 0x00582e60 (jcc_false) | ctx: 0x00582e54: lea ecx, [ebp - 8] ; 0x00582e57: call 0x4cb7b0 ; 0x00582e5c: test al, al ; 0x00582e5e: jne 0x582e6b
  - 0x00582e28: jne -> 0x00582e6b (jcc_true) | ctx: 0x00582e1e: lea ecx, [ebp - 8] ; 0x00582e21: call 0x4cb7b0 ; 0x00582e26: test al, al ; 0x00582e28: jne 0x582e6b
  - 0x00582e28: jne -> 0x00582e2a (jcc_false) | ctx: 0x00582e1e: lea ecx, [ebp - 8] ; 0x00582e21: call 0x4cb7b0 ; 0x00582e26: test al, al ; 0x00582e28: jne 0x582e6b
  - 0x00582e3d: jmp -> 0x00582e6b (jmp) | ctx: 0x00582e34: lea eax, [esi + eax*8 - 8] ; 0x00582e38: mov dword ptr [eax], ecx ; 0x00582e3a: mov dword ptr [eax + 4], ebx ; 0x00582e3d: jmp 0x582e6b

### 0x00582e8f
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00516ab2 at 0x00582ea0)
- branch points:
  - 0x00582e92: jne -> 0x00582e9e (jcc_true) | ctx: 0x00582e8f: push edi ; 0x00582e90: mov edi, ecx ; 0x00582e92: jne 0x582e9e
  - 0x00582e92: jne -> 0x00582e94 (jcc_false) | ctx: 0x00582e8f: push edi ; 0x00582e90: mov edi, ecx ; 0x00582e92: jne 0x582e9e

### 0x00589a1d
- blocks=9, insns=54, edges=14, jcc=7, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCAStar64Normal@EGL@@ slot 0 (target 0x00589ad3, vtable 0x00779bfc)
  - caller_of_anchor_path: depth 1 (calls 0x00589a1d at 0x00589b16)
- branch points:
  - 0x00589a3f: jg -> 0x00589a72 (jcc_true) | ctx: 0x00589a35: mov edi, dword ptr [ecx + eax*8 + 4] ; 0x00589a39: mov dword ptr [ebp - 8], esi ; 0x00589a3c: mov dword ptr [ebp - 4], edx ; 0x00589a3f: jg 0x589a72
  - 0x00589a3f: jg -> 0x00589a41 (jcc_false) | ctx: 0x00589a35: mov edi, dword ptr [ecx + eax*8 + 4] ; 0x00589a39: mov dword ptr [ebp - 8], esi ; 0x00589a3c: mov dword ptr [ebp - 4], edx ; 0x00589a3f: jg 0x589a72
  - 0x00589a48: jge -> 0x00589a55 (jcc_true) | ctx: 0x00589a41: push ebx ; 0x00589a42: lea esi, [eax + eax] ; 0x00589a45: cmp esi, dword ptr [ebp + 8] ; 0x00589a48: jge 0x589a55
  - 0x00589a48: jge -> 0x00589a4a (jcc_false) | ctx: 0x00589a41: push ebx ; 0x00589a42: lea esi, [eax + eax] ; 0x00589a45: cmp esi, dword ptr [ebp + 8] ; 0x00589a48: jge 0x589a55
  - 0x00589a5b: jbe -> 0x00589a71 (jcc_true) | ctx: 0x00589a55: lea edx, [ecx + esi*8 + 4] ; 0x00589a59: cmp edi, dword ptr [edx] ; 0x00589a5b: jbe 0x589a71
  - 0x00589a5b: jbe -> 0x00589a5d (jcc_false) | ctx: 0x00589a55: lea edx, [ecx + esi*8 + 4] ; 0x00589a59: cmp edi, dword ptr [edx] ; 0x00589a5b: jbe 0x589a71
  - 0x00589a52: jbe -> 0x00589a55 (jcc_true) | ctx: 0x00589a4a: mov edx, dword ptr [ecx + esi*8 + 4] ; 0x00589a4e: cmp edx, dword ptr [ecx + esi*8 + 0xc] ; 0x00589a52: jbe 0x589a55
  - 0x00589a52: jbe -> 0x00589a54 (jcc_false) | ctx: 0x00589a4a: mov edx, dword ptr [ecx + esi*8 + 4] ; 0x00589a4e: cmp edx, dword ptr [ecx + esi*8 + 0xc] ; 0x00589a52: jbe 0x589a55
  - 0x00589a6f: jle -> 0x00589a42 (jcc_true) | ctx: 0x00589a66: mov edx, dword ptr [edx + 4] ; 0x00589a69: mov dword ptr [ecx + eax*8 + 8], edx ; 0x00589a6d: mov eax, esi ; 0x00589a6f: jle 0x589a42
  - 0x00589a6f: jle -> 0x00589a71 (jcc_false) | ctx: 0x00589a66: mov edx, dword ptr [edx + 4] ; 0x00589a69: mov dword ptr [ecx + eax*8 + 8], edx ; 0x00589a6d: mov eax, esi ; 0x00589a6f: jle 0x589a42
  - 0x00589a5b: jbe -> 0x00589a71 (jcc_true) | ctx: 0x00589a54: inc esi ; 0x00589a55: lea edx, [ecx + esi*8 + 4] ; 0x00589a59: cmp edi, dword ptr [edx] ; 0x00589a5b: jbe 0x589a71
  - 0x00589a5b: jbe -> 0x00589a5d (jcc_false) | ctx: 0x00589a54: inc esi ; 0x00589a55: lea edx, [ecx + esi*8 + 4] ; 0x00589a59: cmp edi, dword ptr [edx] ; 0x00589a5b: jbe 0x589a71
  - 0x00589a48: jge -> 0x00589a55 (jcc_true) | ctx: 0x00589a42: lea esi, [eax + eax] ; 0x00589a45: cmp esi, dword ptr [ebp + 8] ; 0x00589a48: jge 0x589a55
  - 0x00589a48: jge -> 0x00589a4a (jcc_false) | ctx: 0x00589a42: lea esi, [eax + eax] ; 0x00589a45: cmp esi, dword ptr [ebp + 8] ; 0x00589a48: jge 0x589a55

### 0x0058bbce
- blocks=6, insns=93, edges=10, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00579631 at 0x0058bc63)
- branch points:
  - 0x0058bbf7: je -> 0x0058bc68 (jcc_true) | ctx: 0x0058bbed: mov esi, dword ptr [eax] ; 0x0058bbef: and esi, 0xff ; 0x0058bbf5: cmp esi, ebx ; 0x0058bbf7: je 0x58bc68
  - 0x0058bbf7: je -> 0x0058bbf9 (jcc_false) | ctx: 0x0058bbed: mov esi, dword ptr [eax] ; 0x0058bbef: and esi, 0xff ; 0x0058bbf5: cmp esi, ebx ; 0x0058bbf7: je 0x58bc68
  - 0x0058bc14: je -> 0x0058bc68 (jcc_true) | ctx: 0x0058bc0c: lea ecx, [eax + ebx*8] ; 0x0058bc0f: mov cl, byte ptr [ecx] ; 0x0058bc11: cmp byte ptr [eax + esi*8], cl ; 0x0058bc14: je 0x58bc68
  - 0x0058bc14: je -> 0x0058bc16 (jcc_false) | ctx: 0x0058bc0c: lea ecx, [eax + ebx*8] ; 0x0058bc0f: mov cl, byte ptr [ecx] ; 0x0058bc11: cmp byte ptr [eax + esi*8], cl ; 0x0058bc14: je 0x58bc68
  - 0x0058bc20: jne -> 0x0058bc2a (jcc_true) | ctx: 0x0058bc16: test cl, cl ; 0x0058bc18: mov eax, dword ptr [0x895dac] ; 0x0058bc1d: mov esi, dword ptr [eax + 0x24] ; 0x0058bc20: jne 0x58bc2a
  - 0x0058bc20: jne -> 0x0058bc22 (jcc_false) | ctx: 0x0058bc16: test cl, cl ; 0x0058bc18: mov eax, dword ptr [0x895dac] ; 0x0058bc1d: mov esi, dword ptr [eax + 0x24] ; 0x0058bc20: jne 0x58bc2a

### 0x00591a72
- blocks=15, insns=117, edges=31, jcc=11, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 3 (calls 0x0058bbce at 0x00591b35)
- branch points:
  - 0x00591a7d: je -> 0x00591b4e (jcc_true) | ctx: 0x00591a78: push edi ; 0x00591a79: mov edi, eax ; 0x00591a7b: test edi, edi ; 0x00591a7d: je 0x591b4e
  - 0x00591a7d: je -> 0x00591a83 (jcc_false) | ctx: 0x00591a78: push edi ; 0x00591a79: mov edi, eax ; 0x00591a7b: test edi, edi ; 0x00591a7d: je 0x591b4e
  - 0x00591a8c: je -> 0x00591b4d (jcc_true) | ctx: 0x00591a83: push esi ; 0x00591a84: mov esi, dword ptr [0x895dac] ; 0x00591a8a: test esi, esi ; 0x00591a8c: je 0x591b4d
  - 0x00591a8c: je -> 0x00591a92 (jcc_false) | ctx: 0x00591a83: push esi ; 0x00591a84: mov esi, dword ptr [0x895dac] ; 0x00591a8a: test esi, esi ; 0x00591a8c: je 0x591b4d
  - 0x00591adb: jmp -> 0x00591b44 (jmp) | ctx: 0x00591ad0: call 0x59bd81 ; 0x00591ad5: mov dword ptr [ebp - 0x1c], eax ; 0x00591ad8: mov eax, dword ptr [ebp - 0xc] ; 0x00591adb: jmp 0x591b44
  - 0x00591b4a: jle -> 0x00591add (jcc_true) | ctx: 0x00591b44: cmp eax, dword ptr [ebp - 0x10] ; 0x00591b47: mov dword ptr [ebp - 0xc], eax ; 0x00591b4a: jle 0x591add
  - 0x00591b4a: jle -> 0x00591b4c (jcc_false) | ctx: 0x00591b44: cmp eax, dword ptr [ebp - 0x10] ; 0x00591b47: mov dword ptr [ebp - 0xc], eax ; 0x00591b4a: jle 0x591add
  - 0x00591ae3: jg -> 0x00591b40 (jcc_true) | ctx: 0x00591add: mov ebx, dword ptr [ebp - 0x14] ; 0x00591ae0: cmp ebx, dword ptr [ebp - 8] ; 0x00591ae3: jg 0x591b40
  - 0x00591ae3: jg -> 0x00591ae5 (jcc_false) | ctx: 0x00591add: mov ebx, dword ptr [ebp - 0x14] ; 0x00591ae0: cmp ebx, dword ptr [ebp - 8] ; 0x00591ae3: jg 0x591b40
  - 0x00591b4a: jle -> 0x00591add (jcc_true) | ctx: 0x00591b43: inc eax ; 0x00591b44: cmp eax, dword ptr [ebp - 0x10] ; 0x00591b47: mov dword ptr [ebp - 0xc], eax ; 0x00591b4a: jle 0x591add
  - 0x00591b4a: jle -> 0x00591b4c (jcc_false) | ctx: 0x00591b43: inc eax ; 0x00591b44: cmp eax, dword ptr [ebp - 0x10] ; 0x00591b47: mov dword ptr [ebp - 0xc], eax ; 0x00591b4a: jle 0x591add
  - 0x00591b09: je -> 0x00591b3a (jcc_true) | ctx: 0x00591aff: mov dword ptr [ebp - 0x24], eax ; 0x00591b02: call 0x5917e5 ; 0x00591b07: test al, al ; 0x00591b09: je 0x591b3a
  - 0x00591b09: je -> 0x00591b0b (jcc_false) | ctx: 0x00591aff: mov dword ptr [ebp - 0x24], eax ; 0x00591b02: call 0x5917e5 ; 0x00591b07: test al, al ; 0x00591b09: je 0x591b3a
  - 0x00591b3e: jle -> 0x00591aee (jcc_true) | ctx: 0x00591b3a: inc ebx ; 0x00591b3b: cmp ebx, dword ptr [ebp - 8] ; 0x00591b3e: jle 0x591aee
  - 0x00591b3e: jle -> 0x00591b40 (jcc_false) | ctx: 0x00591b3a: inc ebx ; 0x00591b3b: cmp ebx, dword ptr [ebp - 8] ; 0x00591b3e: jle 0x591aee
  - 0x00591b0f: je -> 0x00591b2c (jcc_true) | ctx: 0x00591b0b: cmp dword ptr [ebp - 4], 0 ; 0x00591b0f: je 0x591b2c
  - 0x00591b0f: je -> 0x00591b11 (jcc_false) | ctx: 0x00591b0b: cmp dword ptr [ebp - 4], 0 ; 0x00591b0f: je 0x591b2c
  - 0x00591b09: je -> 0x00591b3a (jcc_true) | ctx: 0x00591aff: mov dword ptr [ebp - 0x24], eax ; 0x00591b02: call 0x5917e5 ; 0x00591b07: test al, al ; 0x00591b09: je 0x591b3a
  - 0x00591b09: je -> 0x00591b0b (jcc_false) | ctx: 0x00591aff: mov dword ptr [ebp - 0x24], eax ; 0x00591b02: call 0x5917e5 ; 0x00591b07: test al, al ; 0x00591b09: je 0x591b3a
  - 0x00591b3e: jle -> 0x00591aee (jcc_true) | ctx: 0x00591b35: call 0x58bbce ; 0x00591b3a: inc ebx ; 0x00591b3b: cmp ebx, dword ptr [ebp - 8] ; 0x00591b3e: jle 0x591aee
  - 0x00591b3e: jle -> 0x00591b40 (jcc_false) | ctx: 0x00591b35: call 0x58bbce ; 0x00591b3a: inc ebx ; 0x00591b3b: cmp ebx, dword ptr [ebp - 8] ; 0x00591b3e: jle 0x591aee
  - 0x00591b2a: jne -> 0x00591b3a (jcc_true) | ctx: 0x00591b20: mov eax, dword ptr [eax] ; 0x00591b22: and eax, 0xff ; 0x00591b27: cmp eax, dword ptr [ebp - 4] ; 0x00591b2a: jne 0x591b3a
  - 0x00591b2a: jne -> 0x00591b2c (jcc_false) | ctx: 0x00591b20: mov eax, dword ptr [eax] ; 0x00591b22: and eax, 0xff ; 0x00591b27: cmp eax, dword ptr [ebp - 4] ; 0x00591b2a: jne 0x591b3a

### 0x00591bf0
- blocks=1, insns=44, edges=6, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 3 (calls 0x0058bbce at 0x00591c48)
- branch points:
  - none

### 0x00594faf
- blocks=13, insns=83, edges=26, jcc=10, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 3 (calls 0x0058bbce at 0x0059506d)
- branch points:
  - 0x00594fde: jne -> 0x00594fe6 (jcc_true) | ctx: 0x00594fd4: lea eax, [eax + ecx*8] ; 0x00594fd7: cmp byte ptr [eax], 0 ; 0x00594fda: mov byte ptr [ebp + 0xb], 1 ; 0x00594fde: jne 0x594fe6
  - 0x00594fde: jne -> 0x00594fe0 (jcc_false) | ctx: 0x00594fd4: lea eax, [eax + ecx*8] ; 0x00594fd7: cmp byte ptr [eax], 0 ; 0x00594fda: mov byte ptr [ebp + 0xb], 1 ; 0x00594fde: jne 0x594fe6
  - 0x00595003: jge -> 0x0059505a (jcc_true) | ctx: 0x00594ffb: cmp eax, ebx ; 0x00594ffd: mov dword ptr [ebp - 0x10], ecx ; 0x00595000: mov dword ptr [ebp - 0xc], eax ; 0x00595003: jge 0x59505a
  - 0x00595003: jge -> 0x00595005 (jcc_false) | ctx: 0x00594ffb: cmp eax, ebx ; 0x00594ffd: mov dword ptr [ebp - 0x10], ecx ; 0x00595000: mov dword ptr [ebp - 0xc], eax ; 0x00595003: jge 0x59505a
  - 0x00594fe4: je -> 0x0059505a (jcc_true) | ctx: 0x00594fe0: cmp byte ptr [eax + 1], 0 ; 0x00594fe4: je 0x59505a
  - 0x00594fe4: je -> 0x00594fe6 (jcc_false) | ctx: 0x00594fe0: cmp byte ptr [eax + 1], 0 ; 0x00594fe4: je 0x59505a
  - 0x0059500d: jge -> 0x0059504c (jcc_true) | ctx: 0x00595005: lea eax, [esi + 4] ; 0x00595008: cmp esi, eax ; 0x0059500a: mov dword ptr [ebp - 8], esi ; 0x0059500d: jge 0x59504c
  - 0x0059500d: jge -> 0x0059500f (jcc_false) | ctx: 0x00595005: lea eax, [esi + 4] ; 0x00595008: cmp esi, eax ; 0x0059500a: mov dword ptr [ebp - 8], esi ; 0x0059500d: jge 0x59504c
  - 0x00595052: jl -> 0x00595005 (jcc_true) | ctx: 0x0059504c: inc dword ptr [ebp - 0xc] ; 0x0059504f: cmp dword ptr [ebp - 0xc], ebx ; 0x00595052: jl 0x595005
  - 0x00595052: jl -> 0x00595054 (jcc_false) | ctx: 0x0059504c: inc dword ptr [ebp - 0xc] ; 0x0059504f: cmp dword ptr [ebp - 0xc], ebx ; 0x00595052: jl 0x595005
  - 0x0059501f: je -> 0x0059503b (jcc_true) | ctx: 0x00595015: push dword ptr [ebp - 8] ; 0x00595018: call 0x449d52 ; 0x0059501d: test al, al ; 0x0059501f: je 0x59503b
  - 0x0059501f: je -> 0x00595021 (jcc_false) | ctx: 0x00595015: push dword ptr [ebp - 8] ; 0x00595018: call 0x449d52 ; 0x0059501d: test al, al ; 0x0059501f: je 0x59503b
  - 0x00595058: je -> 0x00595072 (jcc_true) | ctx: 0x00595054: cmp byte ptr [ebp + 0xb], 0 ; 0x00595058: je 0x595072
  - 0x00595058: je -> 0x0059505a (jcc_false) | ctx: 0x00595054: cmp byte ptr [ebp + 0xb], 0 ; 0x00595058: je 0x595072
  - 0x00595044: jl -> 0x0059500f (jcc_true) | ctx: 0x0059503b: inc dword ptr [ebp - 8] ; 0x0059503e: lea eax, [esi + 4] ; 0x00595041: cmp dword ptr [ebp - 8], eax ; 0x00595044: jl 0x59500f
  - 0x00595044: jl -> 0x00595046 (jcc_false) | ctx: 0x0059503b: inc dword ptr [ebp - 8] ; 0x0059503e: lea eax, [esi + 4] ; 0x00595041: cmp dword ptr [ebp - 8], eax ; 0x00595044: jl 0x59500f
  - 0x00595039: jne -> 0x00595048 (jcc_true) | ctx: 0x0059502f: push dword ptr [ebp - 8] ; 0x00595032: call 0x57ef15 ; 0x00595037: test al, al ; 0x00595039: jne 0x595048
  - 0x00595039: jne -> 0x0059503b (jcc_false) | ctx: 0x0059502f: push dword ptr [ebp - 8] ; 0x00595032: call 0x57ef15 ; 0x00595037: test al, al ; 0x00595039: jne 0x595048
  - 0x00595046: jmp -> 0x0059504c (jmp) | ctx: 0x00595046: jmp 0x59504c
  - 0x00595052: jl -> 0x00595005 (jcc_true) | ctx: 0x00595048: mov byte ptr [ebp + 0xb], 0 ; 0x0059504c: inc dword ptr [ebp - 0xc] ; 0x0059504f: cmp dword ptr [ebp - 0xc], ebx ; 0x00595052: jl 0x595005
  - 0x00595052: jl -> 0x00595054 (jcc_false) | ctx: 0x00595048: mov byte ptr [ebp + 0xb], 0 ; 0x0059504c: inc dword ptr [ebp - 0xc] ; 0x0059504f: cmp dword ptr [ebp - 0xc], ebx ; 0x00595052: jl 0x595005

### 0x005b9756
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004a71d5 at 0x005b9767)
- branch points:
  - 0x005b9759: jne -> 0x005b9765 (jcc_true) | ctx: 0x005b9756: push edi ; 0x005b9757: mov edi, ecx ; 0x005b9759: jne 0x5b9765
  - 0x005b9759: jne -> 0x005b975b (jcc_false) | ctx: 0x005b9756: push edi ; 0x005b9757: mov edi, ecx ; 0x005b9759: jne 0x5b9765

### 0x00749a38
- blocks=2, insns=5, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_GO_TO_BLOCKED_PILE via `TASK_GO_TO_BLOCKED_PILE` (string 0x0077163c, xref 0x00749a38)
- branch points:
  - 0x00749a3a: ja -> 0x00749a3c (jcc_true) | ctx: 0x00749a38: cmp al, 0x16 ; 0x00749a3a: ja 0x749a3c
  - 0x00749a3a: ja -> 0x00749a3c (jcc_false) | ctx: 0x00749a38: cmp al, 0x16 ; 0x00749a3a: ja 0x749a3c

### 0x00749ba8
- blocks=2, insns=5, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_GO_TO_CAMP via `TASK_GO_TO_CAMP` (string 0x00771788, xref 0x00749ba8)
- branch points:
  - 0x00749baa: ja -> 0x00749bac (jcc_true) | ctx: 0x00749ba8: mov byte ptr [edi], dl ; 0x00749baa: ja 0x749bac
  - 0x00749baa: ja -> 0x00749bac (jcc_false) | ctx: 0x00749ba8: mov byte ptr [edi], dl ; 0x00749baa: ja 0x749bac

### 0x00749bbf
- blocks=2, insns=6, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_LEAVE_CAMP via `TASK_LEAVE_CAMP` (string 0x00771798, xref 0x00749bbf)
- branch points:
  - 0x00749bc1: ja -> 0x00749bc3 (jcc_true) | ctx: 0x00749bbf: cwde ; 0x00749bc0: pop ss ; 0x00749bc1: ja 0x749bc3
  - 0x00749bc1: ja -> 0x00749bc3 (jcc_false) | ctx: 0x00749bbf: cwde ; 0x00749bc0: pop ss ; 0x00749bc1: ja 0x749bc3

### 0x00749e35
- blocks=2, insns=5, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_GO_TO_EAT_BUILDING via `TASK_GO_TO_EAT_BUILDING` (string 0x00771a88, xref 0x00749e35)
- branch points:
  - 0x00749e37: ja -> 0x00749e39 (jcc_true) | ctx: 0x00749e35: mov byte ptr [edx], bl ; 0x00749e37: ja 0x749e39
  - 0x00749e37: ja -> 0x00749e39 (jcc_false) | ctx: 0x00749e35: mov byte ptr [edx], bl ; 0x00749e37: ja 0x749e39

### 0x00749e4c
- blocks=3, insns=12, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_GO_TO_REST_BUILDING via `TASK_GO_TO_REST_BUILDING` (string 0x00771aa0, xref 0x00749e4c)
- branch points:
  - 0x00749e58: jecxz -> 0x00749e59 (jcc_true) | ctx: 0x00749e4c: mov al, byte ptr [0xb900771a] ; 0x00749e51: aaa ; 0x00749e52: xchg byte ptr [esi - 0x7e351800], al ; 0x00749e58: jecxz 0x749e59
  - 0x00749e58: jecxz -> 0x00749e5a (jcc_false) | ctx: 0x00749e4c: mov al, byte ptr [0xb900771a] ; 0x00749e51: aaa ; 0x00749e52: xchg byte ptr [esi - 0x7e351800], al ; 0x00749e58: jecxz 0x749e59

### 0x0074a0ac
- blocks=2, insns=5, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_CHANGE_WORK_TIME_CAMP via `TASK_CHANGE_WORK_TIME_CAMP` (string 0x00771d24, xref 0x0074a0ac)
- branch points:
  - 0x0074a0ae: ja -> 0x0074a0b0 (jcc_true) | ctx: 0x0074a0ac: and al, 0x1d ; 0x0074a0ae: ja 0x74a0b0
  - 0x0074a0ae: ja -> 0x0074a0b0 (jcc_false) | ctx: 0x0074a0ac: and al, 0x1d ; 0x0074a0ae: ja 0x74a0b0

### 0x0074a12e
- blocks=3, insns=12, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS via `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS` (string 0x00771d9c, xref 0x0074a12e)
- branch points:
  - 0x0074a13a: jecxz -> 0x0074a13b (jcc_true) | ctx: 0x0074a12e: pushfd ; 0x0074a12f: sbb eax, 0x55b90077 ; 0x0074a134: xchg byte ptr [esi + 0x7ee8e800], al ; 0x0074a13a: jecxz 0x74a13b
  - 0x0074a13a: jecxz -> 0x0074a13c (jcc_false) | ctx: 0x0074a12e: pushfd ; 0x0074a12f: sbb eax, 0x55b90077 ; 0x0074a134: xchg byte ptr [esi + 0x7ee8e800], al ; 0x0074a13a: jecxz 0x74a13b

### 0x0074a148
- blocks=3, insns=11, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS via `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS` (string 0x00771dc4, xref 0x0074a148)
- branch points:
  - 0x0074a154: jecxz -> 0x0074a155 (jcc_true) | ctx: 0x0074a148: les ebx, ptr [0x56b90077] ; 0x0074a14e: xchg byte ptr [esi + 0x7ecee800], al ; 0x0074a154: jecxz 0x74a155
  - 0x0074a154: jecxz -> 0x0074a156 (jcc_false) | ctx: 0x0074a148: les ebx, ptr [0x56b90077] ; 0x0074a14e: xchg byte ptr [esi + 0x7ecee800], al ; 0x0074a154: jecxz 0x74a155

### 0x0074a162
- blocks=3, insns=12, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS via `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS` (string 0x00771dec, xref 0x0074a162)
- branch points:
  - 0x0074a16e: jecxz -> 0x0074a16f (jcc_true) | ctx: 0x0074a162: in al, dx ; 0x0074a163: sbb eax, 0x57b90077 ; 0x0074a168: xchg byte ptr [esi + 0x7eb4e800], al ; 0x0074a16e: jecxz 0x74a16f
  - 0x0074a16e: jecxz -> 0x0074a170 (jcc_false) | ctx: 0x0074a162: in al, dx ; 0x0074a163: sbb eax, 0x57b90077 ; 0x0074a168: xchg byte ptr [esi + 0x7eb4e800], al ; 0x0074a16e: jecxz 0x74a16f

### 0x0074a17c
- blocks=2, insns=5, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS via `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS` (string 0x00771e14, xref 0x0074a17c)
- branch points:
  - 0x0074a17e: ja -> 0x0074a180 (jcc_true) | ctx: 0x0074a17c: adc al, 0x1e ; 0x0074a17e: ja 0x74a180
  - 0x0074a17e: ja -> 0x0074a180 (jcc_false) | ctx: 0x0074a17c: adc al, 0x1e ; 0x0074a17e: ja 0x74a180

### 0x0074a196
- blocks=2, insns=5, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS via `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS` (string 0x00771e3c, xref 0x0074a196)
- branch points:
  - 0x0074a198: ja -> 0x0074a19a (jcc_true) | ctx: 0x0074a196: cmp al, 0x1e ; 0x0074a198: ja 0x74a19a
  - 0x0074a198: ja -> 0x0074a19a (jcc_false) | ctx: 0x0074a196: cmp al, 0x1e ; 0x0074a198: ja 0x74a19a

## Limits

- Function starts are heuristic (prologue-based).
- Indirect control-flow targets are not fully resolved.
- This is static analysis without dynamic execution traces.
