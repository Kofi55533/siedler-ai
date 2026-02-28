# Engine Instruction CFG Reconstruction

- Binary: `C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games\theSettlers5\bin\SettlersHoK.exe`
- Arch: `x86` (`machine=0x14c`)
- ImageBase: `0x400000`
- .text: `0x401000` -> `0xbb7a00`
- Target patterns: 65
- Matched strings: 177
- Direct call sites in .text: 197253
- RTTI vtable method anchors: 91 (classes: 22)
- Caller expansion: depth=3, window=0x20, max_callers/entry=120, max_functions=500
- Candidate functions: 500
- Total basic blocks: 3421
- Total instructions: 40006
- Conditional branches: 2018
- Switch candidates (indirect jmp): 1

## Matched Strings

- `WayPoints` (pattern `WayPoints`, va `0x00bc9228`, xrefs 2)
- `UpdateBlocking` (pattern `UpdateBlocking`, va `0x00bca3dc`, xrefs 1)
- `BlockingArea` (pattern `BlockingArea`, va `0x00bd5d1c`, xrefs 1)
- `NumBlockedPoints` (pattern `NumBlockedPoints`, va `0x00bd5d2c`, xrefs 1)
- `WaypointsCount` (pattern `WaypointsCount`, va `0x00bd753c`, xrefs 1)
- `NextWayPoint` (pattern `NextWayPoint`, va `0x00bd757c`, xrefs 1)
- `NextWaypointOrientation` (pattern `NextWaypointOrientation`, va `0x00bd758c`, xrefs 1)
- `IsPathingUsed` (pattern `IsPathingUsed`, va `0x00bd75b0`, xrefs 1)
- `FinePath` (pattern `FinePath`, va `0x00bd7608`, xrefs 1)
- `CoarsePath` (pattern `CoarsePath`, va `0x00bd7614`, xrefs 1)
- `WorkerAlarmModeActive` (pattern `WorkerAlarmMode`, va `0x00bd7d88`, xrefs 1)
- `WorkTimeBase` (pattern `WorkTimeBase`, va `0x00bdb8e0`, xrefs 1)
- `WorkTimeThresholdWork` (pattern `WorkTimeThresholdWork`, va `0x00bdb8f0`, xrefs 1)
- `WorkTimeThresholdFarm` (pattern `WorkTimeThresholdFarm`, va `0x00bdb908`, xrefs 1)
- `WorkTimeThresholdResidence` (pattern `WorkTimeThresholdResidence`, va `0x00bdb920`, xrefs 1)
- `WorkTimeThresholdCampFire` (pattern `WorkTimeThresholdCampFire`, va `0x00bdb93c`, xrefs 1)
- `WorkerFlightDistance` (pattern `WorkerFlightDistance`, va `0x00bdbb28`, xrefs 1)
- `ReAttachWorkerFrequency` (pattern `ReAttachWorkerFrequency`, va `0x00bdc858`, xrefs 1)
- `MaximumDistanceWorkerToFarm` (pattern `MaximumDistanceWorkerToFarm`, va `0x00bdc884`, xrefs 1)
- `MaximumDistanceWorkerToResidence` (pattern `MaximumDistanceWorkerToResidence`, va `0x00bdc8a0`, xrefs 1)
- `WorkerAlarmMode` (pattern `WorkerAlarmMode`, va `0x00bdd39c`, xrefs 1)
- `SetWorkTaskListsPerCycle` (pattern `SetWorkTaskListsPerCycle`, va `0x00bded04`, xrefs 1)
- `GetSettlersResidence` (pattern `GetSettlersResidence`, va `0x00bdee44`, xrefs 1)
- `GetSettlersFarm` (pattern `GetSettlersFarm`, va `0x00bdee88`, xrefs 1)
- `CheckSettlerPlacement` (pattern `CheckSettlerPlacement`, va `0x00bdeea8`, xrefs 1)
- `IsSettlerAtResidence` (pattern `IsSettlerAtResidence`, va `0x00bdeef0`, xrefs 1)
- `IsSettlerAtFarm` (pattern `IsSettlerAtFarm`, va `0x00bdef2c`, xrefs 1)
- `GetNextWorkerWithoutFarmOrResidence` (pattern `GetNextWorkerWithoutFarmOrResidence`, va `0x00bdefc0`, xrefs 1)
- `GetNextWorkerWithoutFarm` (pattern `GetNextWorkerWithoutFarm`, va `0x00bdeff8`, xrefs 1)
- `GetNextWorkerWithoutResidence` (pattern `GetNextWorkerWithoutResidence`, va `0x00bdf020`, xrefs 1)
- `TASK_GO_TO_BLOCKED_PILE` (pattern `TASK_GO_TO_BLOCKED_PILE`, va `0x00bdf804`, xrefs 1)
- `TASK_GO_TO_CAMP` (pattern `TASK_GO_TO_CAMP`, va `0x00bdfb04`, xrefs 1)
- `TASK_LEAVE_CAMP` (pattern `TASK_LEAVE_CAMP`, va `0x00bdfb28`, xrefs 1)
- `TASK_GO_TO_EAT_BUILDING` (pattern `TASK_GO_TO_EAT_BUILDING`, va `0x00be0108`, xrefs 1)
- `TASK_GO_TO_REST_BUILDING` (pattern `TASK_GO_TO_REST_BUILDING`, va `0x00be0140`, xrefs 1)
- `TASK_CHANGE_WORK_TIME_CAMP` (pattern `TASK_CHANGE_WORK_TIME_CAMP`, va `0x00be04a8`, xrefs 1)
- `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS` (pattern `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS`, va `0x00be0520`, xrefs 1)
- `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS` (pattern `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS`, va `0x00be0548`, xrefs 1)
- `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS` (pattern `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS`, va `0x00be0570`, xrefs 1)
- `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS` (pattern `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS`, va `0x00be0598`, xrefs 1)
- `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS` (pattern `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS`, va `0x00be05c0`, xrefs 1)
- `EnterWorkerAlarmMode` (pattern `WorkerAlarmMode`, va `0x00be4794`, xrefs 1)
- `QuitWorkerAlarmMode` (pattern `WorkerAlarmMode`, va `0x00be47c8`, xrefs 1)
- `.?AVCBlockingStatusPredicate@EGL@@` (pattern `CBlockingStatusPredicate`, va `0x00d8c30c`, xrefs 0)
- `.?AVCUnblockedInSectorPredicate@EGL@@` (pattern `CUnblockedInSectorPredicate`, va `0x00d8db60`, xrefs 0)
- `.?AVCUnblockedInLargeSectorPredicate@EGL@@` (pattern `CUnblockedInLargeSectorPredicate`, va `0x00d8db90`, xrefs 0)
- `.?AVCUnblockedAreasPredicate@EGL@@` (pattern `CUnblockedAreasPredicate`, va `0x00d8dbc4`, xrefs 0)
- `.?AVCUnblockedBuildingAreasPredicate@EGL@@` (pattern `CUnblockedBuildingAreasPredicate`, va `0x00d8dbf0`, xrefs 0)
- `.?AVCAStar64@EGL@@` (pattern `CAStar64`, va `0x00d8e8e8`, xrefs 0)
- `.?AVCPath@EGL@@` (pattern `CPath`, va `0x00d8e904`, xrefs 0)
- `.?AVCAStar64Normal@EGL@@` (pattern `CAStar64`, va `0x00d8e91c`, xrefs 0)
- `.?AVCCoarsePath@EGL@@` (pattern `CoarsePath`, va `0x00d8e940`, xrefs 0)
- `.?AVCBuildBlockedOnlyPredicate@?A0xe5557549@GGL@@` (pattern `CBuildBlockedOnlyPredicate`, va `0x00d982d8`, xrefs 0)
- `.?AVCCamperBehaviorProperties@GGL@@` (pattern `CCamperBehaviorProperties`, va `0x00d99634`, xrefs 0)
- `.?AVCCamperBehavior@GGL@@` (pattern `CCamperBehavior`, va `0x00d99660`, xrefs 0)
- `.?AVCCampBehavior@GGL@@` (pattern `CCampBehavior`, va `0x00d99684`, xrefs 0)
- `.?AVCCampBehaviorProperties@GGL@@` (pattern `CCampBehavior`, va `0x00d996a4`, xrefs 0)
- `.?AVCUnblockedSquarePredicate@EGL@@` (pattern `CUnblockedSquarePredicate`, va `0x00d996fc`, xrefs 0)
- `.?AV?$THandler@$0BDABA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCCampBehavior@GGL@@X@EGL@@` (pattern `CCampBehavior`, va `0x00d99728`, xrefs 0)
- `.?AV?$THandler@$0BDAAN@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCampBehavior@GGL@@X@EGL@@` (pattern `CCampBehavior`, va `0x00d99798`, xrefs 0)
- `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@` (pattern `CCampBehavior`, va `0x00d99808`, xrefs 0)
- `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@` (pattern `CCampBehavior`, va `0x00d99870`, xrefs 0)
- `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@` (pattern `CCampBehavior`, va `0x00d998d0`, xrefs 0)
- `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@` (pattern `CCampBehavior`, va `0x00d9992c`, xrefs 0)
- `.?AVCPotentialCampSitePredicate@GGL@@` (pattern `CPotentialCampSitePredicate`, va `0x00d99964`, xrefs 0)
- `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@` (pattern `CCamperBehavior`, va `0x00d99998`, xrefs 0)
- `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@` (pattern `CCamperBehavior`, va `0x00d999f0`, xrefs 0)
- `.?AV?$THandler@$0BDABC@VCEvent@BB@@V12@VCCamperBehavior@GGL@@X@EGL@@` (pattern `CCamperBehavior`, va `0x00d99a48`, xrefs 0)
- `.?AV?$THandler@$0BDABB@VCEvent@BB@@VCEvent1Entity@EGL@@VCCamperBehavior@GGL@@X@EGL@@` (pattern `CCamperBehavior`, va `0x00d99a98`, xrefs 0)
- `.?AVCCampWithFreeSlotPredicate@GGL@@` (pattern `CCampWithFreeSlotPredicate`, va `0x00d99af8`, xrefs 0)
- `.?AVCPath@GGL@@` (pattern `CPath`, va `0x00d9ffa8`, xrefs 0)
- `.?AVCWorkerAlarmModeBehaviorProps@GGL@@` (pattern `CWorkerAlarmModeBehaviorProps`, va `0x00da56b8`, xrefs 0)
- `.?AVCWorkerAlarmModeBehavior@GGL@@` (pattern `CWorkerAlarmModeBehavior`, va `0x00da56e8`, xrefs 0)
- `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `CWorkerAlarmModeBehavior`, va `0x00da5718`, xrefs 0)
- `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `CWorkerAlarmModeBehavior`, va `0x00da5770`, xrefs 0)
- `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `CWorkerAlarmModeBehavior`, va `0x00da57c8`, xrefs 0)
- `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `CWorkerAlarmModeBehavior`, va `0x00da5830`, xrefs 0)
- `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `CWorkerAlarmModeBehavior`, va `0x00da5890`, xrefs 0)
- `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `CWorkerAlarmModeBehavior`, va `0x00da58f0`, xrefs 0)
- `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `CWorkerAlarmModeBehavior`, va `0x00da5950`, xrefs 0)
- `.?AVCWorkerBehaviorProps@GGL@@` (pattern `CWorkerBehaviorProps`, va `0x00da5e6c`, xrefs 0)
- `.?AVCWorkerBehavior@GGL@@` (pattern `CWorkerBehavior`, va `0x00da5e94`, xrefs 0)
- `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da5f08`, xrefs 0)
- `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da5f60`, xrefs 0)
- `.?AV?$THandler@$0DO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da5fc8`, xrefs 0)
- `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6020`, xrefs 0)
- `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6088`, xrefs 0)
- `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da60f0`, xrefs 0)
- `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6158`, xrefs 0)
- `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da61c0`, xrefs 0)
- `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6228`, xrefs 0)
- `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6290`, xrefs 0)
- `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da62f8`, xrefs 0)
- `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6360`, xrefs 0)
- `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da63c8`, xrefs 0)
- `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6430`, xrefs 0)
- `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6498`, xrefs 0)
- `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6500`, xrefs 0)
- `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6568`, xrefs 0)
- `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da65d0`, xrefs 0)
- `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6638`, xrefs 0)
- `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da66a0`, xrefs 0)
- `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6708`, xrefs 0)
- `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6770`, xrefs 0)
- `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da67d0`, xrefs 0)
- `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6828`, xrefs 0)
- `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6880`, xrefs 0)
- `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da68d8`, xrefs 0)
- `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6930`, xrefs 0)
- `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6988`, xrefs 0)
- `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da69e0`, xrefs 0)
- `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6a38`, xrefs 0)
- `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6a90`, xrefs 0)
- `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6ae8`, xrefs 0)
- `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6b40`, xrefs 0)
- `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6b98`, xrefs 0)
- `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6bf0`, xrefs 0)
- `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6c48`, xrefs 0)
- `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6ca0`, xrefs 0)
- `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6cf8`, xrefs 0)
- `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6d60`, xrefs 0)
- `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6dc8`, xrefs 0)
- `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6e30`, xrefs 0)
- `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6e98`, xrefs 0)
- `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6ef0`, xrefs 0)
- `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6f48`, xrefs 0)
- `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6fa0`, xrefs 0)
- `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da6ff8`, xrefs 0)
- `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7050`, xrefs 0)
- `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da70a8`, xrefs 0)
- `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7100`, xrefs 0)
- `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7168`, xrefs 0)
- `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da71c0`, xrefs 0)
- `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7218`, xrefs 0)
- `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7270`, xrefs 0)
- `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da72c8`, xrefs 0)
- `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7320`, xrefs 0)
- `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7380`, xrefs 0)
- `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da73e8`, xrefs 0)
- `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7458`, xrefs 0)
- `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da74c8`, xrefs 0)
- `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7520`, xrefs 0)
- `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7578`, xrefs 0)
- `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da75d0`, xrefs 0)
- `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7630`, xrefs 0)
- `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7690`, xrefs 0)
- `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da76f0`, xrefs 0)
- `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7760`, xrefs 0)
- `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da77c8`, xrefs 0)
- `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7838`, xrefs 0)
- `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da78a8`, xrefs 0)
- `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7918`, xrefs 0)
- `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7968`, xrefs 0)
- `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da79b8`, xrefs 0)
- `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7a08`, xrefs 0)
- `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7a58`, xrefs 0)
- `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7ac8`, xrefs 0)
- `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7b38`, xrefs 0)
- `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7b88`, xrefs 0)
- `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7bd8`, xrefs 0)
- `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7c48`, xrefs 0)
- `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7cb8`, xrefs 0)
- `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7d28`, xrefs 0)
- `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7d98`, xrefs 0)
- `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7df8`, xrefs 0)
- `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7e58`, xrefs 0)
- `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7ec8`, xrefs 0)
- `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7f38`, xrefs 0)
- `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da7f98`, xrefs 0)
- `.?AV?$THandler@$0BDACC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da8008`, xrefs 0)
- `.?AV?$THandler@$0BDACF@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, va `0x00da8078`, xrefs 0)
- `.?AV?$TStateHandler@VCWorkerBehavior@GGL@@@EGL@@` (pattern `CWorkerBehavior`, va `0x00da80d8`, xrefs 0)
- `.?AVCWorkerFleeBehaviorProps@GGL@@` (pattern `CWorkerFleeBehaviorProps`, va `0x00da813c`, xrefs 0)
- `.?AVCWorkerFleeBehavior@GGL@@` (pattern `CWorkerFleeBehavior`, va `0x00da8168`, xrefs 0)
- `.?AV?$THandler@$0BFAAO@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@` (pattern `CWorkerFleeBehavior`, va `0x00da8190`, xrefs 0)
- `.?AV?$THandler@$0BDABP@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@` (pattern `CWorkerFleeBehavior`, va `0x00da81f8`, xrefs 0)
- `.?AV?$THandler@$0IN@VCGLETaskArgs@EGL@@V12@VCWorkerFleeBehavior@GGL@@H@EGL@@` (pattern `CWorkerFleeBehavior`, va `0x00da8270`, xrefs 0)

## Functions

### 0x004d5c45
- blocks=1, insns=14, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x004d5c52)
- branch points:
  - none

### 0x004d5c6b
- blocks=1, insns=14, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x004d5c78)
- branch points:
  - none

### 0x004d634a
- blocks=1, insns=14, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: UpdateBlocking via `UpdateBlocking` (string 0x00bca3dc, xref 0x004d65f6)
- branch points:
  - none

### 0x004ebfbf
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: CheckSettlerPlacement via `CheckSettlerPlacement` (string 0x00bdeea8, xref 0x004ebfbf)
- branch points:
  - none

### 0x004ec436
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: GetNextWorkerWithoutFarm via `GetNextWorkerWithoutFarm` (string 0x00bdeff8, xref 0x004ec436)
- branch points:
  - none

### 0x004ec46f
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: GetNextWorkerWithoutFarmOrResidence via `GetNextWorkerWithoutFarmOrResidence` (string 0x00bdefc0, xref 0x004ec46f)
- branch points:
  - none

### 0x004ec4a8
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: GetNextWorkerWithoutResidence via `GetNextWorkerWithoutResidence` (string 0x00bdf020, xref 0x004ec4a8)
- branch points:
  - none

### 0x004ec5fe
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: GetSettlersFarm via `GetSettlersFarm` (string 0x00bdee88, xref 0x004ec5fe)
- branch points:
  - none

### 0x004ec670
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: GetSettlersResidence via `GetSettlersResidence` (string 0x00bdee44, xref 0x004ec670)
- branch points:
  - none

### 0x004ec9c7
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: IsSettlerAtFarm via `IsSettlerAtFarm` (string 0x00bdef2c, xref 0x004ec9c7)
- branch points:
  - none

### 0x004eca00
- blocks=1, insns=0, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: IsSettlerAtResidence via `IsSettlerAtResidence` (string 0x00bdeef0, xref 0x004eca00)
- branch points:
  - none

### 0x004ecbc8
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: SetWorkTaskListsPerCycle via `SetWorkTaskListsPerCycle` (string 0x00bded04, xref 0x004ecbc8)
- branch points:
  - none

### 0x004ed50a
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_CHANGE_WORK_TIME_CAMP via `TASK_CHANGE_WORK_TIME_CAMP` (string 0x00be04a8, xref 0x004ed50a)
- branch points:
  - none

### 0x004ed5bd
- blocks=1, insns=9, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS via `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS` (string 0x00be05c0, xref 0x004ed5bd)
- branch points:
  - none

### 0x004ed5d7
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS via `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS` (string 0x00be0548, xref 0x004ed5d7)
- branch points:
  - none

### 0x004ed60b
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS via `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS` (string 0x00be0520, xref 0x004ed60b)
- branch points:
  - none

### 0x004ed673
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS via `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS` (string 0x00be0598, xref 0x004ed673)
- branch points:
  - none

### 0x004ed68d
- blocks=3, insns=18, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS via `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS` (string 0x00be0570, xref 0x004ed68d)
- branch points:
  - 0x004ed68d: jo -> 0x004ed694 (jcc_true) | ctx: 0x004ed68d: jo 0x4ed694
  - 0x004ed68d: jo -> 0x004ed68f (jcc_false) | ctx: 0x004ed68d: jo 0x4ed694

### 0x004ed9b9
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_GO_TO_BLOCKED_PILE via `TASK_GO_TO_BLOCKED_PILE` (string 0x00bdf804, xref 0x004ed9b9)
- branch points:
  - none

### 0x004ed9e7
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_GO_TO_CAMP via `TASK_GO_TO_CAMP` (string 0x00bdfb04, xref 0x004ed9e7)
- branch points:
  - none

### 0x004eda49
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_GO_TO_EAT_BUILDING via `TASK_GO_TO_EAT_BUILDING` (string 0x00be0108, xref 0x004eda49)
- branch points:
  - none

### 0x004edbb4
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_GO_TO_REST_BUILDING via `TASK_GO_TO_REST_BUILDING` (string 0x00be0140, xref 0x004edbb4)
- branch points:
  - none

### 0x004ede78
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: TASK_LEAVE_CAMP via `TASK_LEAVE_CAMP` (string 0x00bdfb28, xref 0x004ede78)
- branch points:
  - none

### 0x004f0b10
- blocks=1, insns=6, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: WorkerAlarmMode via `EnterWorkerAlarmMode` (string 0x00be4794, xref 0x004f0b10)
- branch points:
  - none

### 0x004f0ee0
- blocks=1, insns=4, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: WorkerAlarmMode via `QuitWorkerAlarmMode` (string 0x00be47c8, xref 0x004f0ee0)
- branch points:
  - none

### 0x004f74f0
- blocks=1, insns=8, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCamperBehavior@GGL@@ slot 6 (target 0x004f7500, vtable 0x00bd8eb0)
  - rtti_vtable_method: .?AVCCamperBehavior@GGL@@ slot 7 (target 0x004f7500, vtable 0x00bd8eb0)
  - rtti_vtable_method: .?AVCCampBehavior@GGL@@ slot 6 (target 0x004f7500, vtable 0x00bd8f10)
  - rtti_vtable_method: .?AVCCampBehavior@GGL@@ slot 7 (target 0x004f7500, vtable 0x00bd8f10)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehavior@GGL@@ slot 6 (target 0x004f7500, vtable 0x00be1058)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehavior@GGL@@ slot 7 (target 0x004f7500, vtable 0x00be1058)
  - rtti_vtable_method: .?AVCWorkerBehavior@GGL@@ slot 6 (target 0x004f7500, vtable 0x00be1450)
  - rtti_vtable_method: .?AVCWorkerBehavior@GGL@@ slot 7 (target 0x004f7500, vtable 0x00be1450)
  - rtti_vtable_method: .?AVCWorkerFleeBehavior@GGL@@ slot 6 (target 0x004f7500, vtable 0x00be17a8)
  - rtti_vtable_method: .?AVCWorkerFleeBehavior@GGL@@ slot 7 (target 0x004f7500, vtable 0x00be17a8)
- branch points:
  - none

### 0x005131e7
- blocks=3, insns=82, edges=26, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00547cad at 0x0051328d)
- branch points:
  - 0x00513277: je -> 0x00513283 (jcc_true) | ctx: 0x0051326d: call 0x5b14c0 ; 0x00513272: mov ecx, dword ptr [esi + 0xc] ; 0x00513275: test ecx, ecx ; 0x00513277: je 0x513283
  - 0x00513277: je -> 0x00513279 (jcc_false) | ctx: 0x0051326d: call 0x5b14c0 ; 0x00513272: mov ecx, dword ptr [esi + 0xc] ; 0x00513275: test ecx, ecx ; 0x00513277: je 0x513283

### 0x005138db
- blocks=1, insns=19, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00607853 at 0x0051396e)
- branch points:
  - none

### 0x0051b423
- blocks=3, insns=61, edges=5, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0051b435)
- branch points:
  - 0x0051b45b: je -> 0x0051b471 (jcc_true) | ctx: 0x0051b453: idiv ecx ; 0x0051b455: cmp dword ptr [esi], 0 ; 0x0051b458: mov dword ptr [ebp + 8], eax ; 0x0051b45b: je 0x51b471
  - 0x0051b45b: je -> 0x0051b45d (jcc_false) | ctx: 0x0051b453: idiv ecx ; 0x0051b455: cmp dword ptr [esi], 0 ; 0x0051b458: mov dword ptr [ebp + 8], eax ; 0x0051b45b: je 0x51b471

### 0x0051b48f
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0051b423 at 0x0051b4c7)
- branch points:
  - 0x0051b4a6: jae -> 0x0051b4cc (jcc_true) | ctx: 0x0051b49f: idiv ebx ; 0x0051b4a1: mov edi, dword ptr [ebp + 8] ; 0x0051b4a4: cmp eax, edi ; 0x0051b4a6: jae 0x51b4cc
  - 0x0051b4a6: jae -> 0x0051b4a8 (jcc_false) | ctx: 0x0051b49f: idiv ebx ; 0x0051b4a1: mov edi, dword ptr [ebp + 8] ; 0x0051b4a4: cmp eax, edi ; 0x0051b4a6: jae 0x51b4cc
  - 0x0051b4b8: jb -> 0x0051b4d3 (jcc_true) | ctx: 0x0051b4b2: idiv ebx ; 0x0051b4b4: sub ecx, eax ; 0x0051b4b6: cmp ecx, edi ; 0x0051b4b8: jb 0x51b4d3
  - 0x0051b4b8: jb -> 0x0051b4ba (jcc_false) | ctx: 0x0051b4b2: idiv ebx ; 0x0051b4b4: sub ecx, eax ; 0x0051b4b6: cmp ecx, edi ; 0x0051b4b8: jb 0x51b4d3

### 0x0052cf4b
- blocks=1, insns=12, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0052cf7e)
- branch points:
  - none

### 0x0053095d
- blocks=3, insns=25, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00607853 at 0x00530962)
- branch points:
  - 0x00530974: je -> 0x00530986 (jcc_true) | ctx: 0x00530969: lea edi, [esi + 0x10] ; 0x0053096c: mov word ptr [esi + 0xc], 0 ; 0x00530972: test edi, edi ; 0x00530974: je 0x530986
  - 0x00530974: je -> 0x00530976 (jcc_false) | ctx: 0x00530969: lea edi, [esi + 0x10] ; 0x0053096c: mov word ptr [esi + 0xc], 0 ; 0x00530972: test edi, edi ; 0x00530974: je 0x530986

### 0x00531750
- blocks=10, insns=49, edges=18, jcc=7, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005317b6)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005317e3)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00531813)
- branch points:
  - 0x00531758: je -> 0x005317ac (jcc_true) | ctx: 0x00531751: mov ebp, esp ; 0x00531753: mov ecx, dword ptr [ebp + 0xc] ; 0x00531756: test ecx, ecx ; 0x00531758: je 0x5317ac
  - 0x00531758: je -> 0x0053175a (jcc_false) | ctx: 0x00531751: mov ebp, esp ; 0x00531753: mov ecx, dword ptr [ebp + 0xc] ; 0x00531756: test ecx, ecx ; 0x00531758: je 0x5317ac
  - 0x00531767: je -> 0x005317ac (jcc_true) | ctx: 0x00531761: push ecx ; 0x00531762: call dword ptr [eax + 8] ; 0x00531765: test eax, eax ; 0x00531767: je 0x5317ac
  - 0x00531767: je -> 0x00531769 (jcc_false) | ctx: 0x00531761: push ecx ; 0x00531762: call dword ptr [eax + 8] ; 0x00531765: test eax, eax ; 0x00531767: je 0x5317ac
  - 0x00531788: je -> 0x0053178f (jcc_true) | ctx: 0x0053177d: lea ecx, [esi + 4] ; 0x00531780: call 0x69570e ; 0x00531785: cmp eax, dword ptr [esi + 4] ; 0x00531788: je 0x53178f
  - 0x00531788: je -> 0x0053178a (jcc_false) | ctx: 0x0053177d: lea ecx, [esi + 4] ; 0x00531780: call 0x69570e ; 0x00531785: cmp eax, dword ptr [esi + 4] ; 0x00531788: je 0x53178f
  - 0x00531795: je -> 0x005317aa (jcc_true) | ctx: 0x0053178f: mov eax, dword ptr [esi + 4] ; 0x00531792: cmp eax, dword ptr [esi + 4] ; 0x00531795: je 0x5317aa
  - 0x00531795: je -> 0x00531797 (jcc_false) | ctx: 0x0053178f: mov eax, dword ptr [esi + 4] ; 0x00531792: cmp eax, dword ptr [esi + 4] ; 0x00531795: je 0x5317aa
  - 0x0053178d: jge -> 0x00531792 (jcc_true) | ctx: 0x0053178a: cmp edi, dword ptr [eax + 0x10] ; 0x0053178d: jge 0x531792
  - 0x0053178d: jge -> 0x0053178f (jcc_false) | ctx: 0x0053178a: cmp edi, dword ptr [eax + 0x10] ; 0x0053178d: jge 0x531792
  - 0x0053179b: jne -> 0x005317aa (jcc_true) | ctx: 0x00531797: cmp byte ptr [eax + 0x18], 0 ; 0x0053179b: jne 0x5317aa
  - 0x0053179b: jne -> 0x0053179d (jcc_false) | ctx: 0x00531797: cmp byte ptr [eax + 0x18], 0 ; 0x0053179b: jne 0x5317aa
  - 0x00531795: je -> 0x005317aa (jcc_true) | ctx: 0x00531792: cmp eax, dword ptr [esi + 4] ; 0x00531795: je 0x5317aa
  - 0x00531795: je -> 0x00531797 (jcc_false) | ctx: 0x00531792: cmp eax, dword ptr [esi + 4] ; 0x00531795: je 0x5317aa

### 0x00532259
- blocks=3, insns=18, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fd2e1 at 0x00532262)
- branch points:
  - 0x0053226c: je -> 0x0053227d (jcc_true) | ctx: 0x00532262: call 0x5fd2e1 ; 0x00532267: lea edx, [eax + 8] ; 0x0053226a: test edx, edx ; 0x0053226c: je 0x53227d
  - 0x0053226c: je -> 0x0053226e (jcc_false) | ctx: 0x00532262: call 0x5fd2e1 ; 0x00532267: lea edx, [eax + 8] ; 0x0053226a: test edx, edx ; 0x0053226c: je 0x53227d

### 0x00532281
- blocks=3, insns=17, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fd2e1 at 0x0053228a)
- branch points:
  - 0x00532294: je -> 0x005322a3 (jcc_true) | ctx: 0x0053228a: call 0x5fd2e1 ; 0x0053228f: lea edx, [eax + 8] ; 0x00532292: test edx, edx ; 0x00532294: je 0x5322a3
  - 0x00532294: je -> 0x00532296 (jcc_false) | ctx: 0x0053228a: call 0x5fd2e1 ; 0x0053228f: lea edx, [eax + 8] ; 0x00532292: test edx, edx ; 0x00532294: je 0x5322a3

### 0x00532ba1
- blocks=1, insns=37, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x00532bb0)
  - caller_of_anchor_path: depth 2 (calls 0x005fd2e1 at 0x00532bc9)
- branch points:
  - none

### 0x00532c26
- blocks=1, insns=29, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x00532c43)
- branch points:
  - none

### 0x00532c7d
- blocks=1, insns=27, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x00532c9a)
- branch points:
  - none

### 0x00532cd6
- blocks=1, insns=35, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fd2e1 at 0x00532cf7)
- branch points:
  - none

### 0x00532d62
- blocks=1, insns=20, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x00532d7f)
- branch points:
  - none

### 0x00532fea
- blocks=2, insns=10, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0053304b)
- branch points:
  - 0x00532fff: jmp -> 0x00532fa0 (jmp) | ctx: 0x00532ffb: pop ecx ; 0x00532ffc: mov ecx, esi ; 0x00532ffe: pop esi ; 0x00532fff: jmp 0x532fa0

### 0x005333fb
- blocks=6, insns=43, edges=13, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0053356a)
- branch points:
  - 0x00533404: je -> 0x0053343c (jcc_true) | ctx: 0x005333fe: push esi ; 0x005333ff: mov esi, dword ptr [ebp + 0x10] ; 0x00533402: test esi, esi ; 0x00533404: je 0x53343c
  - 0x00533404: je -> 0x00533406 (jcc_false) | ctx: 0x005333fe: push esi ; 0x005333ff: mov esi, dword ptr [ebp + 0x10] ; 0x00533402: test esi, esi ; 0x00533404: je 0x53343c
  - 0x00533416: jne -> 0x00533422 (jcc_true) | ctx: 0x0053340d: mov edi, eax ; 0x0053340f: mov eax, dword ptr [0xdd1e00] ; 0x00533414: test eax, eax ; 0x00533416: jne 0x533422
  - 0x00533416: jne -> 0x00533418 (jcc_false) | ctx: 0x0053340d: mov edi, eax ; 0x0053340f: mov eax, dword ptr [0xdd1e00] ; 0x00533414: test eax, eax ; 0x00533416: jne 0x533422
  - 0x0053342c: je -> 0x0053343c (jcc_true) | ctx: 0x00533426: call dword ptr [ecx + 0x1c] ; 0x00533429: pop edi ; 0x0053342a: test eax, eax ; 0x0053342c: je 0x53343c
  - 0x0053342c: je -> 0x0053342e (jcc_false) | ctx: 0x00533426: call dword ptr [ecx + 0x1c] ; 0x00533429: pop edi ; 0x0053342a: test eax, eax ; 0x0053342c: je 0x53343c
  - 0x0053342c: je -> 0x0053343c (jcc_true) | ctx: 0x00533426: call dword ptr [ecx + 0x1c] ; 0x00533429: pop edi ; 0x0053342a: test eax, eax ; 0x0053342c: je 0x53343c
  - 0x0053342c: je -> 0x0053342e (jcc_false) | ctx: 0x00533426: call dword ptr [ecx + 0x1c] ; 0x00533429: pop edi ; 0x0053342a: test eax, eax ; 0x0053342c: je 0x53343c

### 0x0053416f
- blocks=13, insns=146, edges=35, jcc=10, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x00534366)
- branch points:
  - 0x00534188: je -> 0x0053423b (jcc_true) | ctx: 0x00534182: call dword ptr [eax] ; 0x00534184: mov edi, eax ; 0x00534186: test edi, edi ; 0x00534188: je 0x53423b
  - 0x00534188: je -> 0x0053418e (jcc_false) | ctx: 0x00534182: call dword ptr [eax] ; 0x00534184: mov edi, eax ; 0x00534186: test edi, edi ; 0x00534188: je 0x53423b
  - 0x005341c9: jbe -> 0x0053421e (jcc_true) | ctx: 0x005341c1: sar eax, 3 ; 0x005341c4: mov dword ptr [ebp + 8], ecx ; 0x005341c7: cmp eax, ecx ; 0x005341c9: jbe 0x53421e
  - 0x005341c9: jbe -> 0x005341cb (jcc_false) | ctx: 0x005341c1: sar eax, 3 ; 0x005341c4: mov dword ptr [ebp + 8], ecx ; 0x005341c7: cmp eax, ecx ; 0x005341c9: jbe 0x53421e
  - 0x00534234: jne -> 0x00534192 (jcc_true) | ctx: 0x0053422e: call dword ptr [eax] ; 0x00534230: mov edi, eax ; 0x00534232: test edi, edi ; 0x00534234: jne 0x534192
  - 0x00534234: jne -> 0x0053423a (jcc_false) | ctx: 0x0053422e: call dword ptr [eax] ; 0x00534230: mov edi, eax ; 0x00534232: test edi, edi ; 0x00534234: jne 0x534192
  - 0x005341d6: jae -> 0x005341e0 (jcc_true) | ctx: 0x005341ce: sub eax, dword ptr [edi + 8] ; 0x005341d1: sar eax, 3 ; 0x005341d4: cmp ecx, eax ; 0x005341d6: jae 0x5341e0
  - 0x005341d6: jae -> 0x005341d8 (jcc_false) | ctx: 0x005341ce: sub eax, dword ptr [edi + 8] ; 0x005341d1: sar eax, 3 ; 0x005341d4: cmp ecx, eax ; 0x005341d6: jae 0x5341e0
  - 0x005341c9: jbe -> 0x0053421e (jcc_true) | ctx: 0x005341c1: sar eax, 3 ; 0x005341c4: mov dword ptr [ebp + 8], ecx ; 0x005341c7: cmp eax, ecx ; 0x005341c9: jbe 0x53421e
  - 0x005341c9: jbe -> 0x005341cb (jcc_false) | ctx: 0x005341c1: sar eax, 3 ; 0x005341c4: mov dword ptr [ebp + 8], ecx ; 0x005341c7: cmp eax, ecx ; 0x005341c9: jbe 0x53421e
  - 0x005341e7: je -> 0x0053420a (jcc_true) | ctx: 0x005341e0: xor eax, eax ; 0x005341e2: mov dword ptr [ebp + 0xc], eax ; 0x005341e5: test eax, eax ; 0x005341e7: je 0x53420a
  - 0x005341e7: je -> 0x005341e9 (jcc_false) | ctx: 0x005341e0: xor eax, eax ; 0x005341e2: mov dword ptr [ebp + 0xc], eax ; 0x005341e5: test eax, eax ; 0x005341e7: je 0x53420a
  - 0x005341de: jmp -> 0x005341e2 (jmp) | ctx: 0x005341d8: mov eax, dword ptr [edi + 8] ; 0x005341db: mov eax, dword ptr [eax + ecx*8] ; 0x005341de: jmp 0x5341e2
  - 0x00534219: jb -> 0x005341cb (jcc_true) | ctx: 0x00534211: sar eax, 3 ; 0x00534214: mov dword ptr [ebp + 8], ecx ; 0x00534217: cmp ecx, eax ; 0x00534219: jb 0x5341cb
  - 0x00534219: jb -> 0x0053421b (jcc_false) | ctx: 0x00534211: sar eax, 3 ; 0x00534214: mov dword ptr [ebp + 8], ecx ; 0x00534217: cmp ecx, eax ; 0x00534219: jb 0x5341cb
  - 0x00534219: jb -> 0x005341cb (jcc_true) | ctx: 0x00534211: sar eax, 3 ; 0x00534214: mov dword ptr [ebp + 8], ecx ; 0x00534217: cmp ecx, eax ; 0x00534219: jb 0x5341cb
  - 0x00534219: jb -> 0x0053421b (jcc_false) | ctx: 0x00534211: sar eax, 3 ; 0x00534214: mov dword ptr [ebp + 8], ecx ; 0x00534217: cmp ecx, eax ; 0x00534219: jb 0x5341cb
  - 0x005341e7: je -> 0x0053420a (jcc_true) | ctx: 0x005341e2: mov dword ptr [ebp + 0xc], eax ; 0x005341e5: test eax, eax ; 0x005341e7: je 0x53420a
  - 0x005341e7: je -> 0x005341e9 (jcc_false) | ctx: 0x005341e2: mov dword ptr [ebp + 0xc], eax ; 0x005341e5: test eax, eax ; 0x005341e7: je 0x53420a
  - 0x00534234: jne -> 0x00534192 (jcc_true) | ctx: 0x0053422e: call dword ptr [eax] ; 0x00534230: mov edi, eax ; 0x00534232: test edi, edi ; 0x00534234: jne 0x534192
  - 0x00534234: jne -> 0x0053423a (jcc_false) | ctx: 0x0053422e: call dword ptr [eax] ; 0x00534230: mov edi, eax ; 0x00534232: test edi, edi ; 0x00534234: jne 0x534192

### 0x00534739
- blocks=4, insns=31, edges=6, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00534773)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005347a3)
- branch points:
  - 0x00534740: je -> 0x00534756 (jcc_true) | ctx: 0x00534739: push ebp ; 0x0053473a: mov ebp, esp ; 0x0053473c: cmp dword ptr [ebp + 0x10], 0 ; 0x00534740: je 0x534756
  - 0x00534740: je -> 0x00534742 (jcc_false) | ctx: 0x00534739: push ebp ; 0x0053473a: mov ebp, esp ; 0x0053473c: cmp dword ptr [ebp + 0x10], 0 ; 0x00534740: je 0x534756
  - 0x00534754: jmp -> 0x0053475a (jmp) | ctx: 0x0053474c: mov ecx, dword ptr [eax] ; 0x0053474e: call dword ptr [ecx + 4] ; 0x00534751: mov dword ptr [ebp + 0x10], eax ; 0x00534754: jmp 0x53475a

### 0x005364d4
- blocks=3, insns=86, edges=12, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005369a7 at 0x0053651e)
- branch points:
  - 0x00536519: jae -> 0x00536523 (jcc_true) | ctx: 0x00536510: mov ecx, 0x400 ; 0x00536515: sub eax, dword ptr [edi] ; 0x00536517: cmp eax, ecx ; 0x00536519: jae 0x536523
  - 0x00536519: jae -> 0x0053651b (jcc_false) | ctx: 0x00536510: mov ecx, 0x400 ; 0x00536515: sub eax, dword ptr [edi] ; 0x00536517: cmp eax, ecx ; 0x00536519: jae 0x536523

### 0x005369a7
- blocks=3, insns=49, edges=5, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005369b6)
- branch points:
  - 0x005369d3: je -> 0x005369e7 (jcc_true) | ctx: 0x005369cb: add esp, 0x18 ; 0x005369ce: sub ebx, dword ptr [esi] ; 0x005369d0: cmp dword ptr [esi], 0 ; 0x005369d3: je 0x5369e7
  - 0x005369d3: je -> 0x005369d5 (jcc_false) | ctx: 0x005369cb: add esp, 0x18 ; 0x005369ce: sub ebx, dword ptr [esi] ; 0x005369d0: cmp dword ptr [esi], 0 ; 0x005369d3: je 0x5369e7

### 0x00536a01
- blocks=5, insns=28, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005369a7 at 0x00536a29)
- branch points:
  - 0x00536a0f: jae -> 0x00536a2e (jcc_true) | ctx: 0x00536a07: mov edx, dword ptr [esi + 4] ; 0x00536a0a: sub eax, edx ; 0x00536a0c: cmp eax, dword ptr [ebp + 8] ; 0x00536a0f: jae 0x536a2e
  - 0x00536a0f: jae -> 0x00536a11 (jcc_false) | ctx: 0x00536a07: mov edx, dword ptr [esi + 4] ; 0x00536a0a: sub eax, edx ; 0x00536a0c: cmp eax, dword ptr [ebp + 8] ; 0x00536a0f: jae 0x536a2e
  - 0x00536a19: jb -> 0x00536a33 (jcc_true) | ctx: 0x00536a13: sub eax, edx ; 0x00536a15: dec eax ; 0x00536a16: cmp eax, dword ptr [ebp + 8] ; 0x00536a19: jb 0x536a33
  - 0x00536a19: jb -> 0x00536a1b (jcc_false) | ctx: 0x00536a13: sub eax, edx ; 0x00536a15: dec eax ; 0x00536a16: cmp eax, dword ptr [ebp + 8] ; 0x00536a19: jb 0x536a33

### 0x0053e7e1
- blocks=16, insns=121, edges=40, jcc=13, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0053e8ed)
- branch points:
  - 0x0053e7e9: je -> 0x0053e8ce (jcc_true) | ctx: 0x0053e7e2: mov esi, ecx ; 0x0053e7e4: xor ebx, ebx ; 0x0053e7e6: cmp dword ptr [esi + 0x30], ebx ; 0x0053e7e9: je 0x53e8ce
  - 0x0053e7e9: je -> 0x0053e7ef (jcc_false) | ctx: 0x0053e7e2: mov esi, ecx ; 0x0053e7e4: xor ebx, ebx ; 0x0053e7e6: cmp dword ptr [esi + 0x30], ebx ; 0x0053e7e9: je 0x53e8ce
  - 0x0053e808: je -> 0x0053e85a (jcc_true) | ctx: 0x0053e7fe: call 0xacf6cc ; 0x0053e803: add esp, 0xc ; 0x0053e806: test eax, eax ; 0x0053e808: je 0x53e85a
  - 0x0053e808: je -> 0x0053e80a (jcc_false) | ctx: 0x0053e7fe: call 0xacf6cc ; 0x0053e803: add esp, 0xc ; 0x0053e806: test eax, eax ; 0x0053e808: je 0x53e85a
  - 0x0053e872: je -> 0x0053e89c (jcc_true) | ctx: 0x0053e868: call 0xacf6cc ; 0x0053e86d: add esp, 0xc ; 0x0053e870: test eax, eax ; 0x0053e872: je 0x53e89c
  - 0x0053e872: je -> 0x0053e874 (jcc_false) | ctx: 0x0053e868: call 0xacf6cc ; 0x0053e86d: add esp, 0xc ; 0x0053e870: test eax, eax ; 0x0053e872: je 0x53e89c
  - 0x0053e81d: je -> 0x0053e82f (jcc_true) | ctx: 0x0053e812: call 0xace3b0 ; 0x0053e817: add esp, 0xc ; 0x0053e81a: cmp dword ptr [esi + 0x3c], ebx ; 0x0053e81d: je 0x53e82f
  - 0x0053e81d: je -> 0x0053e81f (jcc_false) | ctx: 0x0053e812: call 0xace3b0 ; 0x0053e817: add esp, 0xc ; 0x0053e81a: cmp dword ptr [esi + 0x3c], ebx ; 0x0053e81d: je 0x53e82f
  - 0x0053e89e: je -> 0x0053e8cd (jcc_true) | ctx: 0x0053e89c: test bl, bl ; 0x0053e89e: je 0x53e8cd
  - 0x0053e89e: je -> 0x0053e8a0 (jcc_false) | ctx: 0x0053e89c: test bl, bl ; 0x0053e89e: je 0x53e8cd
  - 0x0053e888: je -> 0x0053e89a (jcc_true) | ctx: 0x0053e87c: call 0xace3b0 ; 0x0053e881: add esp, 0xc ; 0x0053e884: cmp dword ptr [esi + 0x44], 0 ; 0x0053e888: je 0x53e89a
  - 0x0053e888: je -> 0x0053e88a (jcc_false) | ctx: 0x0053e87c: call 0xace3b0 ; 0x0053e881: add esp, 0xc ; 0x0053e884: cmp dword ptr [esi + 0x44], 0 ; 0x0053e888: je 0x53e89a
  - 0x0053e840: je -> 0x0053e858 (jcc_true) | ctx: 0x0053e837: push eax ; 0x0053e838: call 0x6c9192 ; 0x0053e83d: cmp dword ptr [esi + 0x40], ebx ; 0x0053e840: je 0x53e858
  - 0x0053e840: je -> 0x0053e842 (jcc_false) | ctx: 0x0053e837: push eax ; 0x0053e838: call 0x6c9192 ; 0x0053e83d: cmp dword ptr [esi + 0x40], ebx ; 0x0053e840: je 0x53e858
  - 0x0053e840: je -> 0x0053e858 (jcc_true) | ctx: 0x0053e837: push eax ; 0x0053e838: call 0x6c9192 ; 0x0053e83d: cmp dword ptr [esi + 0x40], ebx ; 0x0053e840: je 0x53e858
  - 0x0053e840: je -> 0x0053e842 (jcc_false) | ctx: 0x0053e837: push eax ; 0x0053e838: call 0x6c9192 ; 0x0053e83d: cmp dword ptr [esi + 0x40], ebx ; 0x0053e840: je 0x53e858
  - 0x0053e8bb: je -> 0x0053e8cd (jcc_true) | ctx: 0x0053e8af: call 0xace3b0 ; 0x0053e8b4: add esp, 0xc ; 0x0053e8b7: cmp dword ptr [esi + 0x48], 0 ; 0x0053e8bb: je 0x53e8cd
  - 0x0053e8bb: je -> 0x0053e8bd (jcc_false) | ctx: 0x0053e8af: call 0xace3b0 ; 0x0053e8b4: add esp, 0xc ; 0x0053e8b7: cmp dword ptr [esi + 0x48], 0 ; 0x0053e8bb: je 0x53e8cd
  - 0x0053e89e: je -> 0x0053e8cd (jcc_true) | ctx: 0x0053e89a: mov bl, 1 ; 0x0053e89c: test bl, bl ; 0x0053e89e: je 0x53e8cd
  - 0x0053e89e: je -> 0x0053e8a0 (jcc_false) | ctx: 0x0053e89a: mov bl, 1 ; 0x0053e89c: test bl, bl ; 0x0053e89e: je 0x53e8cd
  - 0x0053e89e: je -> 0x0053e8cd (jcc_true) | ctx: 0x0053e894: call dword ptr [ecx + 0x98] ; 0x0053e89a: mov bl, 1 ; 0x0053e89c: test bl, bl ; 0x0053e89e: je 0x53e8cd
  - 0x0053e89e: je -> 0x0053e8a0 (jcc_false) | ctx: 0x0053e894: call dword ptr [ecx + 0x98] ; 0x0053e89a: mov bl, 1 ; 0x0053e89c: test bl, bl ; 0x0053e89e: je 0x53e8cd
  - 0x0053e872: je -> 0x0053e89c (jcc_true) | ctx: 0x0053e868: call 0xacf6cc ; 0x0053e86d: add esp, 0xc ; 0x0053e870: test eax, eax ; 0x0053e872: je 0x53e89c
  - 0x0053e872: je -> 0x0053e874 (jcc_false) | ctx: 0x0053e868: call 0xacf6cc ; 0x0053e86d: add esp, 0xc ; 0x0053e870: test eax, eax ; 0x0053e872: je 0x53e89c
  - 0x0053e872: je -> 0x0053e89c (jcc_true) | ctx: 0x0053e868: call 0xacf6cc ; 0x0053e86d: add esp, 0xc ; 0x0053e870: test eax, eax ; 0x0053e872: je 0x53e89c
  - 0x0053e872: je -> 0x0053e874 (jcc_false) | ctx: 0x0053e868: call 0xacf6cc ; 0x0053e86d: add esp, 0xc ; 0x0053e870: test eax, eax ; 0x0053e872: je 0x53e89c

### 0x0053f45f
- blocks=1, insns=38, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0053f489)
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0053f4a2)
- branch points:
  - none

### 0x0054540e
- blocks=4, insns=24, edges=5, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00545442)
- branch points:
  - 0x00545422: je -> 0x0054542c (jcc_true) | ctx: 0x0054541a: push eax ; 0x0054541b: call 0x69570e ; 0x00545420: cmp eax, dword ptr [esi] ; 0x00545422: je 0x54542c
  - 0x00545422: je -> 0x00545424 (jcc_false) | ctx: 0x0054541a: push eax ; 0x0054541b: call 0x69570e ; 0x00545420: cmp eax, dword ptr [esi] ; 0x00545422: je 0x54542c
  - 0x0054542a: jge -> 0x0054542e (jcc_true) | ctx: 0x00545424: mov ecx, dword ptr [ebp + 8] ; 0x00545427: cmp ecx, dword ptr [eax + 0x10] ; 0x0054542a: jge 0x54542e
  - 0x0054542a: jge -> 0x0054542c (jcc_false) | ctx: 0x00545424: mov ecx, dword ptr [ebp + 8] ; 0x00545427: cmp ecx, dword ptr [eax + 0x10] ; 0x0054542a: jge 0x54542e

### 0x00546f67
- blocks=1, insns=24, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00607853 at 0x00546fd8)
- branch points:
  - none

### 0x00547cad
- blocks=1, insns=17, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00547cd9)
- branch points:
  - none

### 0x0054a55f
- blocks=3, insns=21, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0054a914)
- branch points:
  - 0x0054a577: je -> 0x0054a586 (jcc_true) | ctx: 0x0054a56a: mov dword ptr [0xdd8478], eax ; 0x0054a56f: imul eax, eax, 0x64 ; 0x0054a572: add eax, 0xdd8480 ; 0x0054a577: je 0x54a586
  - 0x0054a577: je -> 0x0054a579 (jcc_false) | ctx: 0x0054a56a: mov dword ptr [0xdd8478], eax ; 0x0054a56f: imul eax, eax, 0x64 ; 0x0054a572: add eax, 0xdd8480 ; 0x0054a577: je 0x54a586

### 0x0054b4bd
- blocks=3, insns=29, edges=5, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0054b517)
- branch points:
  - 0x0054b4da: je -> 0x0054b4eb (jcc_true) | ctx: 0x0054b4d4: sub edi, eax ; 0x0054b4d6: mov esi, edi ; 0x0054b4d8: cmp edi, ebx ; 0x0054b4da: je 0x54b4eb
  - 0x0054b4da: je -> 0x0054b4dc (jcc_false) | ctx: 0x0054b4d4: sub edi, eax ; 0x0054b4d6: mov esi, edi ; 0x0054b4d8: cmp edi, ebx ; 0x0054b4da: je 0x54b4eb
  - 0x0054b4e9: jne -> 0x0054b4dc (jcc_true) | ctx: 0x0054b4df: call 0x628420 ; 0x0054b4e4: add esi, 0x10 ; 0x0054b4e7: cmp esi, ebx ; 0x0054b4e9: jne 0x54b4dc
  - 0x0054b4e9: jne -> 0x0054b4eb (jcc_false) | ctx: 0x0054b4df: call 0x628420 ; 0x0054b4e4: add esi, 0x10 ; 0x0054b4e7: cmp esi, ebx ; 0x0054b4e9: jne 0x54b4dc

### 0x0054b69b
- blocks=5, insns=56, edges=8, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0054b4bd at 0x0054b6b9)
- branch points:
  - 0x0054b6b2: jbe -> 0x0054b6d1 (jcc_true) | ctx: 0x0054b6aa: sar ecx, 4 ; 0x0054b6ad: mov dword ptr [ebp - 0x14], esi ; 0x0054b6b0: cmp ecx, edi ; 0x0054b6b2: jbe 0x54b6d1
  - 0x0054b6b2: jbe -> 0x0054b6b4 (jcc_false) | ctx: 0x0054b6aa: sar ecx, 4 ; 0x0054b6ad: mov dword ptr [ebp - 0x14], esi ; 0x0054b6b0: cmp ecx, edi ; 0x0054b6b2: jbe 0x54b6d1
  - 0x0054b6d1: jae -> 0x0054b6be (jcc_true) | ctx: 0x0054b6d1: jae 0x54b6be
  - 0x0054b6d1: jae -> 0x0054b6d3 (jcc_false) | ctx: 0x0054b6d1: jae 0x54b6be
  - 0x0054b70f: jmp -> 0x0054b6be (jmp) | ctx: 0x0054b707: sub edi, eax ; 0x0054b709: shl edi, 4 ; 0x0054b70c: add dword ptr [esi + 4], edi ; 0x0054b70f: jmp 0x54b6be

### 0x0054c2a6
- blocks=3, insns=28, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005761c7 at 0x0054c2e5)
- branch points:
  - 0x0054c2b0: je -> 0x0054c2ea (jcc_true) | ctx: 0x0054c2a7: mov esi, ecx ; 0x0054c2a9: mov eax, dword ptr [eax + 0x14] ; 0x0054c2ac: cmp dword ptr [eax + 0x5c], 0 ; 0x0054c2b0: je 0x54c2ea
  - 0x0054c2b0: je -> 0x0054c2b2 (jcc_false) | ctx: 0x0054c2a7: mov esi, ecx ; 0x0054c2a9: mov eax, dword ptr [eax + 0x14] ; 0x0054c2ac: cmp dword ptr [eax + 0x5c], 0 ; 0x0054c2b0: je 0x54c2ea

### 0x0054c358
- blocks=4, insns=72, edges=15, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0054c429)
- branch points:
  - 0x0054c39e: je -> 0x0054c417 (jcc_true) | ctx: 0x0054c393: call 0x54c470 ; 0x0054c398: mov ecx, dword ptr [ebp - 0x10] ; 0x0054c39b: cmp ecx, dword ptr [eax + 8] ; 0x0054c39e: je 0x54c417
  - 0x0054c39e: je -> 0x0054c3a0 (jcc_false) | ctx: 0x0054c393: call 0x54c470 ; 0x0054c398: mov ecx, dword ptr [ebp - 0x10] ; 0x0054c39b: cmp ecx, dword ptr [eax + 8] ; 0x0054c39e: je 0x54c417
  - 0x0054c3b9: jb -> 0x0054c417 (jcc_true) | ctx: 0x0054c3af: mov eax, dword ptr [eax + 4] ; 0x0054c3b2: mov dword ptr [ebp - 8], eax ; 0x0054c3b5: comiss xmm0, dword ptr [ebp - 8] ; 0x0054c3b9: jb 0x54c417
  - 0x0054c3b9: jb -> 0x0054c3bb (jcc_false) | ctx: 0x0054c3af: mov eax, dword ptr [eax + 4] ; 0x0054c3b2: mov dword ptr [ebp - 8], eax ; 0x0054c3b5: comiss xmm0, dword ptr [ebp - 8] ; 0x0054c3b9: jb 0x54c417
  - 0x0054c415: jne -> 0x0054c3a0 (jcc_true) | ctx: 0x0054c40a: mov dword ptr [ebp - 0x10], esi ; 0x0054c40d: call 0x54c470 ; 0x0054c412: cmp esi, dword ptr [eax + 8] ; 0x0054c415: jne 0x54c3a0
  - 0x0054c415: jne -> 0x0054c417 (jcc_false) | ctx: 0x0054c40a: mov dword ptr [ebp - 0x10], esi ; 0x0054c40d: call 0x54c470 ; 0x0054c412: cmp esi, dword ptr [eax + 8] ; 0x0054c415: jne 0x54c3a0

### 0x0054e9fb
- blocks=1, insns=14, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0053e7e1 at 0x0054ec93)
  - caller_of_anchor_path: depth 2 (calls 0x0053e7e1 at 0x0054f5d5)
  - caller_of_anchor_path: depth 2 (calls 0x0053e7e1 at 0x0054f686)
- branch points:
  - none

### 0x0054fa98
- blocks=8, insns=171, edges=29, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0053e7e1 at 0x0054fbd3)
- branch points:
  - 0x0054faaf: jne -> 0x0054fab8 (jcc_true) | ctx: 0x0054faa8: call dword ptr [eax + 0x14] ; 0x0054faab: mov edx, eax ; 0x0054faad: test edx, edx ; 0x0054faaf: jne 0x54fab8
  - 0x0054faaf: jne -> 0x0054fab1 (jcc_false) | ctx: 0x0054faa8: call dword ptr [eax + 0x14] ; 0x0054faab: mov edx, eax ; 0x0054faad: test edx, edx ; 0x0054faaf: jne 0x54fab8
  - 0x0054fac8: je -> 0x0054fab1 (jcc_true) | ctx: 0x0054fac1: mov eax, dword ptr [ecx] ; 0x0054fac3: call dword ptr [eax + 0x1c] ; 0x0054fac6: test eax, eax ; 0x0054fac8: je 0x54fab1
  - 0x0054fac8: je -> 0x0054faca (jcc_false) | ctx: 0x0054fac1: mov eax, dword ptr [ecx] ; 0x0054fac3: call dword ptr [eax + 0x1c] ; 0x0054fac6: test eax, eax ; 0x0054fac8: je 0x54fab1
  - 0x0054fab3: jmp -> 0x0054fc82 (jmp) | ctx: 0x0054fab1: mov al, 1 ; 0x0054fab3: jmp 0x54fc82
  - 0x0054fad1: je -> 0x0054fab1 (jcc_true) | ctx: 0x0054faca: mov edx, dword ptr [eax] ; 0x0054facc: mov dword ptr [ebp - 0xc], edx ; 0x0054facf: test edx, edx ; 0x0054fad1: je 0x54fab1
  - 0x0054fad1: je -> 0x0054fad3 (jcc_false) | ctx: 0x0054faca: mov edx, dword ptr [eax] ; 0x0054facc: mov dword ptr [ebp - 0xc], edx ; 0x0054facf: test edx, edx ; 0x0054fad1: je 0x54fab1
  - 0x0054fbc2: je -> 0x0054fc58 (jcc_true) | ctx: 0x0054fbb8: call 0x4161c0 ; 0x0054fbbd: add esp, 0xc ; 0x0054fbc0: test eax, eax ; 0x0054fbc2: je 0x54fc58
  - 0x0054fbc2: je -> 0x0054fbc8 (jcc_false) | ctx: 0x0054fbb8: call 0x4161c0 ; 0x0054fbbd: add esp, 0xc ; 0x0054fbc0: test eax, eax ; 0x0054fbc2: je 0x54fc58

### 0x00552615
- blocks=22, insns=328, edges=88, jcc=13, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x005526a4)
- branch points:
  - 0x00552697: je -> 0x005526ad (jcc_true) | ctx: 0x0055268e: mov dword ptr [ebp - 0x20], edi ; 0x00552691: mov byte ptr [ebp - 4], 1 ; 0x00552695: test edi, edi ; 0x00552697: je 0x5526ad
  - 0x00552697: je -> 0x00552699 (jcc_false) | ctx: 0x0055268e: mov dword ptr [ebp - 0x20], edi ; 0x00552691: mov byte ptr [ebp - 4], 1 ; 0x00552695: test edi, edi ; 0x00552697: je 0x5526ad
  - 0x005526f1: je -> 0x005526ff (jcc_true) | ctx: 0x005526e8: mov dword ptr [ebp - 0x24], eax ; 0x005526eb: mov byte ptr [ebp - 4], 2 ; 0x005526ef: test eax, eax ; 0x005526f1: je 0x5526ff
  - 0x005526f1: je -> 0x005526f3 (jcc_false) | ctx: 0x005526e8: mov dword ptr [ebp - 0x24], eax ; 0x005526eb: mov byte ptr [ebp - 4], 2 ; 0x005526ef: test eax, eax ; 0x005526f1: je 0x5526ff
  - 0x005526ab: jmp -> 0x005526af (jmp) | ctx: 0x005526a1: mov dword ptr [edi + 4], eax ; 0x005526a4: call 0x57fd44 ; 0x005526a9: mov dword ptr [edi], eax ; 0x005526ab: jmp 0x5526af
  - 0x00552719: je -> 0x00552736 (jcc_true) | ctx: 0x00552710: mov dword ptr [ebp - 0x24], eax ; 0x00552713: mov byte ptr [ebp - 4], 3 ; 0x00552717: test eax, eax ; 0x00552719: je 0x552736
  - 0x00552719: je -> 0x0055271b (jcc_false) | ctx: 0x00552710: mov dword ptr [ebp - 0x24], eax ; 0x00552713: mov byte ptr [ebp - 4], 3 ; 0x00552717: test eax, eax ; 0x00552719: je 0x552736
  - 0x005526fd: jmp -> 0x00552701 (jmp) | ctx: 0x005526f3: push dword ptr [esi + 0x1c] ; 0x005526f6: mov ecx, eax ; 0x005526f8: call 0x55180c ; 0x005526fd: jmp 0x552701
  - 0x005526f1: je -> 0x005526ff (jcc_true) | ctx: 0x005526e8: mov dword ptr [ebp - 0x24], eax ; 0x005526eb: mov byte ptr [ebp - 4], 2 ; 0x005526ef: test eax, eax ; 0x005526f1: je 0x5526ff
  - 0x005526f1: je -> 0x005526f3 (jcc_false) | ctx: 0x005526e8: mov dword ptr [ebp - 0x24], eax ; 0x005526eb: mov byte ptr [ebp - 4], 2 ; 0x005526ef: test eax, eax ; 0x005526f1: je 0x5526ff
  - 0x0055276e: je -> 0x00552779 (jcc_true) | ctx: 0x00552765: mov dword ptr [ebp - 0x24], eax ; 0x00552768: mov byte ptr [ebp - 4], 4 ; 0x0055276c: test eax, eax ; 0x0055276e: je 0x552779
  - 0x0055276e: je -> 0x00552770 (jcc_false) | ctx: 0x00552765: mov dword ptr [ebp - 0x24], eax ; 0x00552768: mov byte ptr [ebp - 4], 4 ; 0x0055276c: test eax, eax ; 0x0055276e: je 0x552779
  - 0x00552734: jmp -> 0x00552738 (jmp) | ctx: 0x00552729: push dword ptr [ebp - 0x10] ; 0x0055272c: push dword ptr [ebp - 0x14] ; 0x0055272f: call 0x54bd6a ; 0x00552734: jmp 0x552738
  - 0x00552719: je -> 0x00552736 (jcc_true) | ctx: 0x00552710: mov dword ptr [ebp - 0x24], eax ; 0x00552713: mov byte ptr [ebp - 4], 3 ; 0x00552717: test eax, eax ; 0x00552719: je 0x552736
  - 0x00552719: je -> 0x0055271b (jcc_false) | ctx: 0x00552710: mov dword ptr [ebp - 0x24], eax ; 0x00552713: mov byte ptr [ebp - 4], 3 ; 0x00552717: test eax, eax ; 0x00552719: je 0x552736
  - 0x005527a0: je -> 0x005527af (jcc_true) | ctx: 0x00552797: mov dword ptr [ebp - 0x24], eax ; 0x0055279a: mov byte ptr [ebp - 4], 5 ; 0x0055279e: test eax, eax ; 0x005527a0: je 0x5527af
  - 0x005527a0: je -> 0x005527a2 (jcc_false) | ctx: 0x00552797: mov dword ptr [ebp - 0x24], eax ; 0x0055279a: mov byte ptr [ebp - 4], 5 ; 0x0055279e: test eax, eax ; 0x005527a0: je 0x5527af
  - 0x00552777: jmp -> 0x0055277b (jmp) | ctx: 0x00552770: mov ecx, eax ; 0x00552772: call 0x55c473 ; 0x00552777: jmp 0x55277b
  - 0x0055276e: je -> 0x00552779 (jcc_true) | ctx: 0x00552765: mov dword ptr [ebp - 0x24], eax ; 0x00552768: mov byte ptr [ebp - 4], 4 ; 0x0055276c: test eax, eax ; 0x0055276e: je 0x552779
  - 0x0055276e: je -> 0x00552770 (jcc_false) | ctx: 0x00552765: mov dword ptr [ebp - 0x24], eax ; 0x00552768: mov byte ptr [ebp - 4], 4 ; 0x0055276c: test eax, eax ; 0x0055276e: je 0x552779
  - 0x005527dd: je -> 0x005527ec (jcc_true) | ctx: 0x005527d4: mov dword ptr [ebp - 0x24], eax ; 0x005527d7: mov byte ptr [ebp - 4], 6 ; 0x005527db: test eax, eax ; 0x005527dd: je 0x5527ec
  - 0x005527dd: je -> 0x005527df (jcc_false) | ctx: 0x005527d4: mov dword ptr [ebp - 0x24], eax ; 0x005527d7: mov byte ptr [ebp - 4], 6 ; 0x005527db: test eax, eax ; 0x005527dd: je 0x5527ec
  - 0x005527ad: jmp -> 0x005527b1 (jmp) | ctx: 0x005527a5: push ecx ; 0x005527a6: mov ecx, eax ; 0x005527a8: call 0x555c69 ; 0x005527ad: jmp 0x5527b1
  - 0x005527a0: je -> 0x005527af (jcc_true) | ctx: 0x00552797: mov dword ptr [ebp - 0x24], eax ; 0x0055279a: mov byte ptr [ebp - 4], 5 ; 0x0055279e: test eax, eax ; 0x005527a0: je 0x5527af
  - 0x005527a0: je -> 0x005527a2 (jcc_false) | ctx: 0x00552797: mov dword ptr [ebp - 0x24], eax ; 0x0055279a: mov byte ptr [ebp - 4], 5 ; 0x0055279e: test eax, eax ; 0x005527a0: je 0x5527af
  - 0x00552806: je -> 0x00552811 (jcc_true) | ctx: 0x005527fd: mov dword ptr [ebp - 0x24], eax ; 0x00552800: mov byte ptr [ebp - 4], 7 ; 0x00552804: test eax, eax ; 0x00552806: je 0x552811
  - 0x00552806: je -> 0x00552808 (jcc_false) | ctx: 0x005527fd: mov dword ptr [ebp - 0x24], eax ; 0x00552800: mov byte ptr [ebp - 4], 7 ; 0x00552804: test eax, eax ; 0x00552806: je 0x552811
  - 0x005527ea: jmp -> 0x005527ee (jmp) | ctx: 0x005527e2: push ecx ; 0x005527e3: mov ecx, eax ; 0x005527e5: call 0x564a79 ; 0x005527ea: jmp 0x5527ee
  - 0x005527dd: je -> 0x005527ec (jcc_true) | ctx: 0x005527d4: mov dword ptr [ebp - 0x24], eax ; 0x005527d7: mov byte ptr [ebp - 4], 6 ; 0x005527db: test eax, eax ; 0x005527dd: je 0x5527ec
  - 0x005527dd: je -> 0x005527df (jcc_false) | ctx: 0x005527d4: mov dword ptr [ebp - 0x24], eax ; 0x005527d7: mov byte ptr [ebp - 4], 6 ; 0x005527db: test eax, eax ; 0x005527dd: je 0x5527ec
  - 0x0055280f: jmp -> 0x00552813 (jmp) | ctx: 0x00552808: mov ecx, eax ; 0x0055280a: call 0x569894 ; 0x0055280f: jmp 0x552813
  - 0x00552806: je -> 0x00552811 (jcc_true) | ctx: 0x005527fd: mov dword ptr [ebp - 0x24], eax ; 0x00552800: mov byte ptr [ebp - 4], 7 ; 0x00552804: test eax, eax ; 0x00552806: je 0x552811
  - 0x00552806: je -> 0x00552808 (jcc_false) | ctx: 0x005527fd: mov dword ptr [ebp - 0x24], eax ; 0x00552800: mov byte ptr [ebp - 4], 7 ; 0x00552804: test eax, eax ; 0x00552806: je 0x552811

### 0x00554f4d
- blocks=3, insns=46, edges=8, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x00554fa8)
- branch points:
  - 0x00554f92: jne -> 0x00554f85 (jcc_true) | ctx: 0x00554f87: call 0x554e34 ; 0x00554f8c: add ebx, 0x18 ; 0x00554f8f: sub esi, 1 ; 0x00554f92: jne 0x554f85
  - 0x00554f92: jne -> 0x00554f94 (jcc_false) | ctx: 0x00554f87: call 0x554e34 ; 0x00554f8c: add ebx, 0x18 ; 0x00554f8f: sub esi, 1 ; 0x00554f92: jne 0x554f85
  - 0x00554f92: jne -> 0x00554f85 (jcc_true) | ctx: 0x00554f87: call 0x554e34 ; 0x00554f8c: add ebx, 0x18 ; 0x00554f8f: sub esi, 1 ; 0x00554f92: jne 0x554f85
  - 0x00554f92: jne -> 0x00554f94 (jcc_false) | ctx: 0x00554f87: call 0x554e34 ; 0x00554f8c: add ebx, 0x18 ; 0x00554f8f: sub esi, 1 ; 0x00554f92: jne 0x554f85

### 0x005558d0
- blocks=10, insns=61, edges=18, jcc=7, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0056815d at 0x005558d7)
- branch points:
  - 0x005558de: je -> 0x00555934 (jcc_true) | ctx: 0x005558d4: mov dword ptr [ebp - 4], ecx ; 0x005558d7: call 0x56815d ; 0x005558dc: test al, al ; 0x005558de: je 0x555934
  - 0x005558de: je -> 0x005558e0 (jcc_false) | ctx: 0x005558d4: mov dword ptr [ebp - 4], ecx ; 0x005558d7: call 0x56815d ; 0x005558dc: test al, al ; 0x005558de: je 0x555934
  - 0x005558fb: je -> 0x0055592d (jcc_true) | ctx: 0x005558f5: idiv ecx ; 0x005558f7: mov edi, eax ; 0x005558f9: test edi, edi ; 0x005558fb: je 0x55592d
  - 0x005558fb: je -> 0x005558fd (jcc_false) | ctx: 0x005558f5: idiv ecx ; 0x005558f7: mov edi, eax ; 0x005558f9: test edi, edi ; 0x005558fb: je 0x55592d
  - 0x00555917: je -> 0x00555924 (jcc_true) | ctx: 0x0055590e: mov ecx, dword ptr [ebp - 4] ; 0x00555911: mov ecx, dword ptr [ecx + eax*8 + 0x10] ; 0x00555915: test ecx, ecx ; 0x00555917: je 0x555924
  - 0x00555917: je -> 0x00555919 (jcc_false) | ctx: 0x0055590e: mov ecx, dword ptr [ebp - 4] ; 0x00555911: mov ecx, dword ptr [ecx + eax*8 + 0x10] ; 0x00555915: test ecx, ecx ; 0x00555917: je 0x555924
  - 0x0055592a: jne -> 0x00555900 (jcc_true) | ctx: 0x00555924: add esi, 0xc ; 0x00555927: sub edi, 1 ; 0x0055592a: jne 0x555900
  - 0x0055592a: jne -> 0x0055592c (jcc_false) | ctx: 0x00555924: add esi, 0xc ; 0x00555927: sub edi, 1 ; 0x0055592a: jne 0x555900
  - 0x0055591d: je -> 0x00555924 (jcc_true) | ctx: 0x00555919: cmp byte ptr [ecx + 5], 0 ; 0x0055591d: je 0x555924
  - 0x0055591d: je -> 0x0055591f (jcc_false) | ctx: 0x00555919: cmp byte ptr [ecx + 5], 0 ; 0x0055591d: je 0x555924
  - 0x00555917: je -> 0x00555924 (jcc_true) | ctx: 0x0055590e: mov ecx, dword ptr [ebp - 4] ; 0x00555911: mov ecx, dword ptr [ecx + eax*8 + 0x10] ; 0x00555915: test ecx, ecx ; 0x00555917: je 0x555924
  - 0x00555917: je -> 0x00555919 (jcc_false) | ctx: 0x0055590e: mov ecx, dword ptr [ebp - 4] ; 0x00555911: mov ecx, dword ptr [ecx + eax*8 + 0x10] ; 0x00555915: test ecx, ecx ; 0x00555917: je 0x555924
  - 0x0055592a: jne -> 0x00555900 (jcc_true) | ctx: 0x00555921: call dword ptr [eax + 0x10] ; 0x00555924: add esi, 0xc ; 0x00555927: sub edi, 1 ; 0x0055592a: jne 0x555900
  - 0x0055592a: jne -> 0x0055592c (jcc_false) | ctx: 0x00555921: call dword ptr [eax + 0x10] ; 0x00555924: add esi, 0xc ; 0x00555927: sub edi, 1 ; 0x0055592a: jne 0x555900

### 0x0055833e
- blocks=3, insns=28, edges=5, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00558399)
- branch points:
  - 0x00558359: je -> 0x00558369 (jcc_true) | ctx: 0x00558353: sub edi, eax ; 0x00558355: mov esi, edi ; 0x00558357: cmp edi, ebx ; 0x00558359: je 0x558369
  - 0x00558359: je -> 0x0055835b (jcc_false) | ctx: 0x00558353: sub edi, eax ; 0x00558355: mov esi, edi ; 0x00558357: cmp edi, ebx ; 0x00558359: je 0x558369
  - 0x00558367: jne -> 0x0055835b (jcc_true) | ctx: 0x0055835d: call 0x54ca58 ; 0x00558362: add esi, 0x34 ; 0x00558365: cmp esi, ebx ; 0x00558367: jne 0x55835b
  - 0x00558367: jne -> 0x00558369 (jcc_false) | ctx: 0x0055835d: call 0x54ca58 ; 0x00558362: add esi, 0x34 ; 0x00558365: cmp esi, ebx ; 0x00558367: jne 0x55835b

### 0x005584cf
- blocks=5, insns=62, edges=8, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0055833e at 0x005584f2)
- branch points:
  - 0x005584eb: jbe -> 0x0055850a (jcc_true) | ctx: 0x005584e4: mov ecx, eax ; 0x005584e6: mov dword ptr [ebp - 0x14], esi ; 0x005584e9: cmp ecx, edi ; 0x005584eb: jbe 0x55850a
  - 0x005584eb: jbe -> 0x005584ed (jcc_false) | ctx: 0x005584e4: mov ecx, eax ; 0x005584e6: mov dword ptr [ebp - 0x14], esi ; 0x005584e9: cmp ecx, edi ; 0x005584eb: jbe 0x55850a
  - 0x0055850a: jae -> 0x005584f7 (jcc_true) | ctx: 0x0055850a: jae 0x5584f7
  - 0x0055850a: jae -> 0x0055850c (jcc_false) | ctx: 0x0055850a: jae 0x5584f7
  - 0x00558548: jmp -> 0x005584f7 (jmp) | ctx: 0x00558540: sub edi, eax ; 0x00558542: imul eax, edi, 0x34 ; 0x00558545: add dword ptr [esi + 4], eax ; 0x00558548: jmp 0x5584f7

### 0x00559507
- blocks=3, insns=28, edges=5, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00559562)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00559626)
- branch points:
  - 0x00559522: je -> 0x00559532 (jcc_true) | ctx: 0x0055951c: sub edi, eax ; 0x0055951e: mov esi, edi ; 0x00559520: cmp edi, ebx ; 0x00559522: je 0x559532
  - 0x00559522: je -> 0x00559524 (jcc_false) | ctx: 0x0055951c: sub edi, eax ; 0x0055951e: mov esi, edi ; 0x00559520: cmp edi, ebx ; 0x00559522: je 0x559532
  - 0x00559530: jne -> 0x00559524 (jcc_true) | ctx: 0x00559526: call 0x55937a ; 0x0055952b: add esi, 0xc ; 0x0055952e: cmp esi, ebx ; 0x00559530: jne 0x559524
  - 0x00559530: jne -> 0x00559532 (jcc_false) | ctx: 0x00559526: call 0x55937a ; 0x0055952b: add esi, 0xc ; 0x0055952e: cmp esi, ebx ; 0x00559530: jne 0x559524

### 0x0055977c
- blocks=5, insns=62, edges=8, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00564601 at 0x0055979f)
- branch points:
  - 0x00559798: jbe -> 0x005597b7 (jcc_true) | ctx: 0x00559791: mov ecx, eax ; 0x00559793: mov dword ptr [ebp - 0x14], esi ; 0x00559796: cmp ecx, edi ; 0x00559798: jbe 0x5597b7
  - 0x00559798: jbe -> 0x0055979a (jcc_false) | ctx: 0x00559791: mov ecx, eax ; 0x00559793: mov dword ptr [ebp - 0x14], esi ; 0x00559796: cmp ecx, edi ; 0x00559798: jbe 0x5597b7
  - 0x005597b7: jae -> 0x005597a4 (jcc_true) | ctx: 0x005597b7: jae 0x5597a4
  - 0x005597b7: jae -> 0x005597b9 (jcc_false) | ctx: 0x005597b7: jae 0x5597a4
  - 0x005597f5: jmp -> 0x005597a4 (jmp) | ctx: 0x005597ed: sub edi, eax ; 0x005597ef: imul eax, edi, 0xc ; 0x005597f2: add dword ptr [esi + 4], eax ; 0x005597f5: jmp 0x5597a4

### 0x00559816
- blocks=5, insns=62, edges=8, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00559507 at 0x00559839)
- branch points:
  - 0x00559832: jbe -> 0x00559851 (jcc_true) | ctx: 0x0055982b: mov ecx, eax ; 0x0055982d: mov dword ptr [ebp - 0x14], esi ; 0x00559830: cmp ecx, edi ; 0x00559832: jbe 0x559851
  - 0x00559832: jbe -> 0x00559834 (jcc_false) | ctx: 0x0055982b: mov ecx, eax ; 0x0055982d: mov dword ptr [ebp - 0x14], esi ; 0x00559830: cmp ecx, edi ; 0x00559832: jbe 0x559851
  - 0x00559851: jae -> 0x0055983e (jcc_true) | ctx: 0x00559851: jae 0x55983e
  - 0x00559851: jae -> 0x00559853 (jcc_false) | ctx: 0x00559851: jae 0x55983e
  - 0x0055988f: jmp -> 0x0055983e (jmp) | ctx: 0x00559887: sub edi, eax ; 0x00559889: imul eax, edi, 0xc ; 0x0055988c: add dword ptr [esi + 4], eax ; 0x0055988f: jmp 0x55983e

### 0x00559d42
- blocks=9, insns=69, edges=20, jcc=7, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0055a673 at 0x00559e27)
  - caller_of_anchor_path: depth 2 (calls 0x005696ac at 0x00559e11)
- branch points:
  - 0x00559d60: je -> 0x00559d7d (jcc_true) | ctx: 0x00559d58: sar ebx, 2 ; 0x00559d5b: mov dword ptr [ebp - 4], ecx ; 0x00559d5e: test ebx, ebx ; 0x00559d60: je 0x559d7d
  - 0x00559d60: je -> 0x00559d62 (jcc_false) | ctx: 0x00559d58: sar ebx, 2 ; 0x00559d5b: mov dword ptr [ebp - 4], ecx ; 0x00559d5e: test ebx, ebx ; 0x00559d60: je 0x559d7d
  - 0x00559d82: je -> 0x00559d8e (jcc_true) | ctx: 0x00559d7d: mov ecx, dword ptr [esi + 0xc] ; 0x00559d80: test ecx, ecx ; 0x00559d82: je 0x559d8e
  - 0x00559d82: je -> 0x00559d84 (jcc_false) | ctx: 0x00559d7d: mov ecx, dword ptr [esi + 0xc] ; 0x00559d80: test ecx, ecx ; 0x00559d82: je 0x559d8e
  - 0x00559d6f: je -> 0x00559d75 (jcc_true) | ctx: 0x00559d65: push dword ptr [eax + edi*4] ; 0x00559d68: call 0x65f1be ; 0x00559d6d: test eax, eax ; 0x00559d6f: je 0x559d75
  - 0x00559d6f: je -> 0x00559d71 (jcc_false) | ctx: 0x00559d65: push dword ptr [eax + edi*4] ; 0x00559d68: call 0x65f1be ; 0x00559d6d: test eax, eax ; 0x00559d6f: je 0x559d75
  - 0x00559d93: je -> 0x00559d9f (jcc_true) | ctx: 0x00559d8e: mov ecx, dword ptr [esi + 0x10] ; 0x00559d91: test ecx, ecx ; 0x00559d93: je 0x559d9f
  - 0x00559d93: je -> 0x00559d95 (jcc_false) | ctx: 0x00559d8e: mov ecx, dword ptr [esi + 0x10] ; 0x00559d91: test ecx, ecx ; 0x00559d93: je 0x559d9f
  - 0x00559d93: je -> 0x00559d9f (jcc_true) | ctx: 0x00559d8b: call dword ptr [eax + 8] ; 0x00559d8e: mov ecx, dword ptr [esi + 0x10] ; 0x00559d91: test ecx, ecx ; 0x00559d93: je 0x559d9f
  - 0x00559d93: je -> 0x00559d95 (jcc_false) | ctx: 0x00559d8b: call dword ptr [eax + 8] ; 0x00559d8e: mov ecx, dword ptr [esi + 0x10] ; 0x00559d91: test ecx, ecx ; 0x00559d93: je 0x559d9f
  - 0x00559d7b: jb -> 0x00559d62 (jcc_true) | ctx: 0x00559d75: mov ecx, dword ptr [ebp - 4] ; 0x00559d78: inc edi ; 0x00559d79: cmp edi, ebx ; 0x00559d7b: jb 0x559d62
  - 0x00559d7b: jb -> 0x00559d7d (jcc_false) | ctx: 0x00559d75: mov ecx, dword ptr [ebp - 4] ; 0x00559d78: inc edi ; 0x00559d79: cmp edi, ebx ; 0x00559d7b: jb 0x559d62
  - 0x00559d7b: jb -> 0x00559d62 (jcc_true) | ctx: 0x00559d75: mov ecx, dword ptr [ebp - 4] ; 0x00559d78: inc edi ; 0x00559d79: cmp edi, ebx ; 0x00559d7b: jb 0x559d62
  - 0x00559d7b: jb -> 0x00559d7d (jcc_false) | ctx: 0x00559d75: mov ecx, dword ptr [ebp - 4] ; 0x00559d78: inc edi ; 0x00559d79: cmp edi, ebx ; 0x00559d7b: jb 0x559d62

### 0x0055a673
- blocks=3, insns=51, edges=5, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0055a682)
- branch points:
  - 0x0055a6a1: je -> 0x0055a6b7 (jcc_true) | ctx: 0x0055a69a: sub ebx, dword ptr [esi] ; 0x0055a69c: sar ebx, 1 ; 0x0055a69e: cmp dword ptr [esi], 0 ; 0x0055a6a1: je 0x55a6b7
  - 0x0055a6a1: je -> 0x0055a6a3 (jcc_false) | ctx: 0x0055a69a: sub ebx, dword ptr [esi] ; 0x0055a69c: sar ebx, 1 ; 0x0055a69e: cmp dword ptr [esi], 0 ; 0x0055a6a1: je 0x55a6b7

### 0x0055a6d2
- blocks=5, insns=31, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0055a673 at 0x0055a703)
- branch points:
  - 0x0055a6e4: jae -> 0x0055a708 (jcc_true) | ctx: 0x0055a6de: sub eax, edx ; 0x0055a6e0: sar eax, 1 ; 0x0055a6e2: cmp eax, ecx ; 0x0055a6e4: jae 0x55a708
  - 0x0055a6e4: jae -> 0x0055a6e6 (jcc_false) | ctx: 0x0055a6de: sub eax, edx ; 0x0055a6e0: sar eax, 1 ; 0x0055a6e2: cmp eax, ecx ; 0x0055a6e4: jae 0x55a708
  - 0x0055a6f3: jb -> 0x0055a70d (jcc_true) | ctx: 0x0055a6ed: sar edx, 1 ; 0x0055a6ef: sub eax, edx ; 0x0055a6f1: cmp eax, ecx ; 0x0055a6f3: jb 0x55a70d
  - 0x0055a6f3: jb -> 0x0055a6f5 (jcc_false) | ctx: 0x0055a6ed: sar edx, 1 ; 0x0055a6ef: sub eax, edx ; 0x0055a6f1: cmp eax, ecx ; 0x0055a6f3: jb 0x55a70d

### 0x0055b125
- blocks=1, insns=23, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0055b175)
- branch points:
  - none

### 0x0055b203
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0055b125 at 0x0055b233)
- branch points:
  - 0x0055b21a: jae -> 0x0055b240 (jcc_true) | ctx: 0x0055b213: idiv ebx ; 0x0055b215: mov edi, dword ptr [ebp + 8] ; 0x0055b218: cmp eax, edi ; 0x0055b21a: jae 0x55b240
  - 0x0055b21a: jae -> 0x0055b21c (jcc_false) | ctx: 0x0055b213: idiv ebx ; 0x0055b215: mov edi, dword ptr [ebp + 8] ; 0x0055b218: cmp eax, edi ; 0x0055b21a: jae 0x55b240
  - 0x0055b22c: jb -> 0x0055b247 (jcc_true) | ctx: 0x0055b226: idiv ebx ; 0x0055b228: sub ecx, eax ; 0x0055b22a: cmp ecx, edi ; 0x0055b22c: jb 0x55b247
  - 0x0055b22c: jb -> 0x0055b22e (jcc_false) | ctx: 0x0055b226: idiv ebx ; 0x0055b228: sub ecx, eax ; 0x0055b22a: cmp ecx, edi ; 0x0055b22c: jb 0x55b247

### 0x0055c446
- blocks=4, insns=21, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0055c51f)
- branch points:
  - 0x0055c456: je -> 0x0055c45f (jcc_true) | ctx: 0x0055c44e: call 0x55c368 ; 0x0055c453: pop ecx ; 0x0055c454: test al, al ; 0x0055c456: je 0x55c45f
  - 0x0055c456: je -> 0x0055c458 (jcc_false) | ctx: 0x0055c44e: call 0x55c368 ; 0x0055c453: pop ecx ; 0x0055c454: test al, al ; 0x0055c456: je 0x55c45f
  - 0x0055c45d: jmp -> 0x0055c470 (jmp) | ctx: 0x0055c458: mov eax, 0x55c387 ; 0x0055c45d: jmp 0x55c470

### 0x0055cafd
- blocks=1, insns=65, edges=4, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0055cb28)
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0055cb7d)
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0055cb97)
- branch points:
  - none

### 0x0055dd7c
- blocks=12, insns=136, edges=29, jcc=6, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0055deb2)
- branch points:
  - 0x0055dd8c: jne -> 0x0055de8c (jcc_true) | ctx: 0x0055dd82: push ebx ; 0x0055dd83: mov ebx, ecx ; 0x0055dd85: test dword ptr [ebx + 4], 0x8000000 ; 0x0055dd8c: jne 0x55de8c
  - 0x0055dd8c: jne -> 0x0055dd92 (jcc_false) | ctx: 0x0055dd82: push ebx ; 0x0055dd83: mov ebx, ecx ; 0x0055dd85: test dword ptr [ebx + 4], 0x8000000 ; 0x0055dd8c: jne 0x55de8c
  - 0x0055ddad: je -> 0x0055ddfc (jcc_true) | ctx: 0x0055dda9: pop edi ; 0x0055ddaa: pop esi ; 0x0055ddab: cmp ecx, eax ; 0x0055ddad: je 0x55ddfc
  - 0x0055ddad: je -> 0x0055ddaf (jcc_false) | ctx: 0x0055dda9: pop edi ; 0x0055ddaa: pop esi ; 0x0055ddab: cmp ecx, eax ; 0x0055ddad: je 0x55ddfc
  - 0x0055de4a: je -> 0x0055de55 (jcc_true) | ctx: 0x0055de3e: lea ecx, [ebp - 0x2c] ; 0x0055de41: call 0x55a913 ; 0x0055de46: cmp byte ptr [ebp - 0x30], 0 ; 0x0055de4a: je 0x55de55
  - 0x0055de4a: je -> 0x0055de4c (jcc_false) | ctx: 0x0055de3e: lea ecx, [ebp - 0x2c] ; 0x0055de41: call 0x55a913 ; 0x0055de46: cmp byte ptr [ebp - 0x30], 0 ; 0x0055de4a: je 0x55de55
  - 0x0055ddd7: jb -> 0x0055ddde (jcc_true) | ctx: 0x0055ddc4: mulss xmm2, dword ptr [0xd46128] ; 0x0055ddcc: mulss xmm3, dword ptr [0xd46128] ; 0x0055ddd4: comiss xmm2, xmm1 ; 0x0055ddd7: jb 0x55ddde
  - 0x0055ddd7: jb -> 0x0055ddd9 (jcc_false) | ctx: 0x0055ddc4: mulss xmm2, dword ptr [0xd46128] ; 0x0055ddcc: mulss xmm3, dword ptr [0xd46128] ; 0x0055ddd4: comiss xmm2, xmm1 ; 0x0055ddd7: jb 0x55ddde
  - 0x0055de53: jmp -> 0x0055de5c (jmp) | ctx: 0x0055de4c: or dword ptr [ebx + 4], 0x1000000 ; 0x0055de53: jmp 0x55de5c
  - 0x0055dde8: jb -> 0x0055ddef (jcc_true) | ctx: 0x0055ddde: movaps xmm0, xmm3 ; 0x0055dde1: addss xmm0, xmm2 ; 0x0055dde5: comiss xmm1, xmm0 ; 0x0055dde8: jb 0x55ddef
  - 0x0055dde8: jb -> 0x0055ddea (jcc_false) | ctx: 0x0055ddde: movaps xmm0, xmm3 ; 0x0055dde1: addss xmm0, xmm2 ; 0x0055dde5: comiss xmm1, xmm0 ; 0x0055dde8: jb 0x55ddef
  - 0x0055dddc: jmp -> 0x0055ddfc (jmp) | ctx: 0x0055ddd9: mov dword ptr [ebp - 0x14], eax ; 0x0055dddc: jmp 0x55ddfc
  - 0x0055de4a: je -> 0x0055de55 (jcc_true) | ctx: 0x0055de3e: lea ecx, [ebp - 0x2c] ; 0x0055de41: call 0x55a913 ; 0x0055de46: cmp byte ptr [ebp - 0x30], 0 ; 0x0055de4a: je 0x55de55
  - 0x0055de4a: je -> 0x0055de4c (jcc_false) | ctx: 0x0055de3e: lea ecx, [ebp - 0x2c] ; 0x0055de41: call 0x55a913 ; 0x0055de46: cmp byte ptr [ebp - 0x30], 0 ; 0x0055de4a: je 0x55de55
  - 0x0055dded: jmp -> 0x0055ddfc (jmp) | ctx: 0x0055ddea: mov dword ptr [ebp - 0x10], ecx ; 0x0055dded: jmp 0x55ddfc

### 0x0055fc14
- blocks=3, insns=15, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0055fc1d)
- branch points:
  - 0x0055fc27: je -> 0x0055fc30 (jcc_true) | ctx: 0x0055fc1d: call 0x57fd44 ; 0x0055fc22: lea edx, [eax + 8] ; 0x0055fc25: test edx, edx ; 0x0055fc27: je 0x55fc30
  - 0x0055fc27: je -> 0x0055fc29 (jcc_false) | ctx: 0x0055fc1d: call 0x57fd44 ; 0x0055fc22: lea edx, [eax + 8] ; 0x0055fc25: test edx, edx ; 0x0055fc27: je 0x55fc30

### 0x005643c1
- blocks=1, insns=14, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00569602 at 0x0056440f)
- branch points:
  - none

### 0x00564601
- blocks=3, insns=28, edges=5, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0056465a)
- branch points:
  - 0x0056461c: je -> 0x0056462c (jcc_true) | ctx: 0x00564616: sub edi, eax ; 0x00564618: mov esi, edi ; 0x0056461a: cmp edi, ebx ; 0x0056461c: je 0x56462c
  - 0x0056461c: je -> 0x0056461e (jcc_false) | ctx: 0x00564616: sub edi, eax ; 0x00564618: mov esi, edi ; 0x0056461a: cmp edi, ebx ; 0x0056461c: je 0x56462c
  - 0x0056462a: jne -> 0x0056461e (jcc_true) | ctx: 0x00564620: call 0x628420 ; 0x00564625: add esi, 0xc ; 0x00564628: cmp esi, ebx ; 0x0056462a: jne 0x56461e
  - 0x0056462a: jne -> 0x0056462c (jcc_false) | ctx: 0x00564620: call 0x628420 ; 0x00564625: add esi, 0xc ; 0x00564628: cmp esi, ebx ; 0x0056462a: jne 0x56461e

### 0x00564ee7
- blocks=1, insns=19, edges=7, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005652c9 at 0x00564fcc)
- branch points:
  - 0x00564f24: jmp -> 0x006a5c79 (jmp) | ctx: 0x00564f1b: call 0x6a5c79 ; 0x00564f20: lea ecx, [esi + 4] ; 0x00564f23: pop esi ; 0x00564f24: jmp 0x6a5c79

### 0x005652c9
- blocks=6, insns=33, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005652e9)
- branch points:
  - 0x005652d6: jne -> 0x005652dc (jcc_true) | ctx: 0x005652ce: mov dword ptr [edi + 4], eax ; 0x005652d1: mov dword ptr [edi + 8], eax ; 0x005652d4: test esi, esi ; 0x005652d6: jne 0x5652dc
  - 0x005652d6: jne -> 0x005652d8 (jcc_false) | ctx: 0x005652ce: mov dword ptr [edi + 4], eax ; 0x005652d1: mov dword ptr [edi + 8], eax ; 0x005652d4: test esi, esi ; 0x005652d6: jne 0x5652dc
  - 0x005652e2: ja -> 0x00565306 (jcc_true) | ctx: 0x005652dc: cmp esi, 0x7ffffff ; 0x005652e2: ja 0x565306
  - 0x005652e2: ja -> 0x005652e4 (jcc_false) | ctx: 0x005652dc: cmp esi, 0x7ffffff ; 0x005652e2: ja 0x565306
  - 0x005652da: jmp -> 0x00565300 (jmp) | ctx: 0x005652d8: xor al, al ; 0x005652da: jmp 0x565300

### 0x0056559d
- blocks=1, insns=19, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00588b31 at 0x005655aa)
- branch points:
  - none

### 0x00565732
- blocks=1, insns=33, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00588b31 at 0x0056574d)
  - caller_of_anchor_path: depth 2 (calls 0x005fd315 at 0x0056576e)
- branch points:
  - none

### 0x00565c1b
- blocks=7, insns=37, edges=12, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fd315 at 0x00565c4b)
- branch points:
  - 0x00565c2e: jbe -> 0x00565c57 (jcc_true) | ctx: 0x00565c23: fstp dword ptr [ebp - 4] ; 0x00565c26: movss xmm0, dword ptr [ebp - 4] ; 0x00565c2b: comiss xmm0, dword ptr [esi] ; 0x00565c2e: jbe 0x565c57
  - 0x00565c2e: jbe -> 0x00565c30 (jcc_false) | ctx: 0x00565c23: fstp dword ptr [ebp - 4] ; 0x00565c26: movss xmm0, dword ptr [ebp - 4] ; 0x00565c2b: comiss xmm0, dword ptr [esi] ; 0x00565c2e: jbe 0x565c57
  - 0x00565c38: jae -> 0x00565c3f (jcc_true) | ctx: 0x00565c30: mov eax, dword ptr [esi + 0x1c] ; 0x00565c33: cmp eax, 0x200 ; 0x00565c38: jae 0x565c3f
  - 0x00565c38: jae -> 0x00565c3a (jcc_false) | ctx: 0x00565c30: mov eax, dword ptr [esi + 0x1c] ; 0x00565c33: cmp eax, 0x200 ; 0x00565c38: jae 0x565c3f
  - 0x00565c44: jae -> 0x00565c48 (jcc_true) | ctx: 0x00565c3f: cmp eax, 0x1fffffff ; 0x00565c44: jae 0x565c48
  - 0x00565c44: jae -> 0x00565c46 (jcc_false) | ctx: 0x00565c3f: cmp eax, 0x1fffffff ; 0x00565c44: jae 0x565c48
  - 0x00565c3d: jmp -> 0x00565c48 (jmp) | ctx: 0x00565c3a: shl eax, 3 ; 0x00565c3d: jmp 0x565c48

### 0x00566eb3
- blocks=3, insns=28, edges=5, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00566f0e)
  - caller_of_anchor_path: depth 2 (calls 0x00566eb3 at 0x00566ed2)
  - caller_of_anchor_path: depth 2 (calls 0x00566eb3 at 0x00566f48)
- branch points:
  - 0x00566ece: je -> 0x00566ede (jcc_true) | ctx: 0x00566ec8: sub edi, eax ; 0x00566eca: mov esi, edi ; 0x00566ecc: cmp edi, ebx ; 0x00566ece: je 0x566ede
  - 0x00566ece: je -> 0x00566ed0 (jcc_false) | ctx: 0x00566ec8: sub edi, eax ; 0x00566eca: mov esi, edi ; 0x00566ecc: cmp edi, ebx ; 0x00566ece: je 0x566ede
  - 0x00566edc: jne -> 0x00566ed0 (jcc_true) | ctx: 0x00566ed2: call 0x566e9b ; 0x00566ed7: add esi, 0x28 ; 0x00566eda: cmp esi, ebx ; 0x00566edc: jne 0x566ed0
  - 0x00566edc: jne -> 0x00566ede (jcc_false) | ctx: 0x00566ed2: call 0x566e9b ; 0x00566ed7: add esi, 0x28 ; 0x00566eda: cmp esi, ebx ; 0x00566edc: jne 0x566ed0

### 0x00566fb5
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0060ad20 at 0x00566fe5)
- branch points:
  - 0x00566fcc: jae -> 0x00566ff2 (jcc_true) | ctx: 0x00566fc5: idiv ebx ; 0x00566fc7: mov edi, dword ptr [ebp + 8] ; 0x00566fca: cmp eax, edi ; 0x00566fcc: jae 0x566ff2
  - 0x00566fcc: jae -> 0x00566fce (jcc_false) | ctx: 0x00566fc5: idiv ebx ; 0x00566fc7: mov edi, dword ptr [ebp + 8] ; 0x00566fca: cmp eax, edi ; 0x00566fcc: jae 0x566ff2
  - 0x00566fde: jb -> 0x00566ff9 (jcc_true) | ctx: 0x00566fd8: idiv ebx ; 0x00566fda: sub ecx, eax ; 0x00566fdc: cmp ecx, edi ; 0x00566fde: jb 0x566ff9
  - 0x00566fde: jb -> 0x00566fe0 (jcc_false) | ctx: 0x00566fd8: idiv ebx ; 0x00566fda: sub ecx, eax ; 0x00566fdc: cmp ecx, edi ; 0x00566fde: jb 0x566ff9

### 0x00567009
- blocks=7, insns=70, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00566eb3 at 0x00567024)
- branch points:
  - 0x00567013: je -> 0x00567054 (jcc_true) | ctx: 0x0056700c: mov dword ptr [ebp - 4], edi ; 0x0056700f: mov esi, dword ptr [edi] ; 0x00567011: test esi, esi ; 0x00567013: je 0x567054
  - 0x00567013: je -> 0x00567015 (jcc_false) | ctx: 0x0056700c: mov dword ptr [ebp - 4], edi ; 0x0056700f: mov esi, dword ptr [edi] ; 0x00567011: test esi, esi ; 0x00567013: je 0x567054
  - 0x0056701e: je -> 0x00567035 (jcc_true) | ctx: 0x00567019: push 0x28 ; 0x0056701b: pop ecx ; 0x0056701c: cmp esi, ebx ; 0x0056701e: je 0x567035
  - 0x0056701e: je -> 0x00567020 (jcc_false) | ctx: 0x00567019: push 0x28 ; 0x0056701b: pop ecx ; 0x0056701c: cmp esi, ebx ; 0x0056701e: je 0x567035
  - 0x0056702d: jne -> 0x00567022 (jcc_true) | ctx: 0x00567024: call 0x566e9b ; 0x00567029: add esi, edi ; 0x0056702b: cmp esi, ebx ; 0x0056702d: jne 0x567022
  - 0x0056702d: jne -> 0x0056702f (jcc_false) | ctx: 0x00567024: call 0x566e9b ; 0x00567029: add esi, edi ; 0x0056702b: cmp esi, ebx ; 0x0056702d: jne 0x567022
  - 0x0056702d: jne -> 0x00567022 (jcc_true) | ctx: 0x00567024: call 0x566e9b ; 0x00567029: add esi, edi ; 0x0056702b: cmp esi, ebx ; 0x0056702d: jne 0x567022
  - 0x0056702d: jne -> 0x0056702f (jcc_false) | ctx: 0x00567024: call 0x566e9b ; 0x00567029: add esi, edi ; 0x0056702b: cmp esi, ebx ; 0x0056702d: jne 0x567022

### 0x00567092
- blocks=5, insns=62, edges=8, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00566eb3 at 0x005670b5)
- branch points:
  - 0x005670ae: jbe -> 0x005670cd (jcc_true) | ctx: 0x005670a7: mov ecx, eax ; 0x005670a9: mov dword ptr [ebp - 0x14], esi ; 0x005670ac: cmp ecx, edi ; 0x005670ae: jbe 0x5670cd
  - 0x005670ae: jbe -> 0x005670b0 (jcc_false) | ctx: 0x005670a7: mov ecx, eax ; 0x005670a9: mov dword ptr [ebp - 0x14], esi ; 0x005670ac: cmp ecx, edi ; 0x005670ae: jbe 0x5670cd
  - 0x005670cd: jae -> 0x005670ba (jcc_true) | ctx: 0x005670cd: jae 0x5670ba
  - 0x005670cd: jae -> 0x005670cf (jcc_false) | ctx: 0x005670cd: jae 0x5670ba
  - 0x0056710b: jmp -> 0x005670ba (jmp) | ctx: 0x00567103: sub edi, eax ; 0x00567105: imul eax, edi, 0x28 ; 0x00567108: add dword ptr [esi + 4], eax ; 0x0056710b: jmp 0x5670ba

### 0x0056815d
- blocks=8, insns=87, edges=20, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00568292)
- branch points:
  - 0x00568180: je -> 0x00568239 (jcc_true) | ctx: 0x00568177: call 0x55ec57 ; 0x0056817c: mov edi, eax ; 0x0056817e: test edi, edi ; 0x00568180: je 0x568239
  - 0x00568180: je -> 0x00568186 (jcc_false) | ctx: 0x00568177: call 0x55ec57 ; 0x0056817c: mov edi, eax ; 0x0056817e: test edi, edi ; 0x00568180: je 0x568239
  - 0x0056818a: je -> 0x00568239 (jcc_true) | ctx: 0x00568186: test byte ptr [edi + 0x50], 8 ; 0x0056818a: je 0x568239
  - 0x0056818a: je -> 0x00568190 (jcc_false) | ctx: 0x00568186: test byte ptr [edi + 0x50], 8 ; 0x0056818a: je 0x568239
  - 0x00568210: je -> 0x0056821a (jcc_true) | ctx: 0x0056820b: xor eax, eax ; 0x0056820d: pop esi ; 0x0056820e: test ecx, ecx ; 0x00568210: je 0x56821a
  - 0x00568210: je -> 0x00568212 (jcc_false) | ctx: 0x0056820b: xor eax, eax ; 0x0056820d: pop esi ; 0x0056820e: test ecx, ecx ; 0x00568210: je 0x56821a
  - 0x00568233: je -> 0x00568239 (jcc_true) | ctx: 0x0056822a: mov ecx, edi ; 0x0056822c: call 0x53a11d ; 0x00568231: test al, al ; 0x00568233: je 0x568239
  - 0x00568233: je -> 0x00568235 (jcc_false) | ctx: 0x0056822a: mov ecx, edi ; 0x0056822c: call 0x53a11d ; 0x00568231: test al, al ; 0x00568233: je 0x568239
  - 0x00568233: je -> 0x00568239 (jcc_true) | ctx: 0x0056822a: mov ecx, edi ; 0x0056822c: call 0x53a11d ; 0x00568231: test al, al ; 0x00568233: je 0x568239
  - 0x00568233: je -> 0x00568235 (jcc_false) | ctx: 0x0056822a: mov ecx, edi ; 0x0056822c: call 0x53a11d ; 0x00568231: test al, al ; 0x00568233: je 0x568239
  - 0x00568237: jmp -> 0x0056823b (jmp) | ctx: 0x00568235: mov al, 1 ; 0x00568237: jmp 0x56823b

### 0x0056833a
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00611570 at 0x0056836a)
- branch points:
  - 0x00568351: jae -> 0x00568377 (jcc_true) | ctx: 0x0056834a: idiv ebx ; 0x0056834c: mov edi, dword ptr [ebp + 8] ; 0x0056834f: cmp eax, edi ; 0x00568351: jae 0x568377
  - 0x00568351: jae -> 0x00568353 (jcc_false) | ctx: 0x0056834a: idiv ebx ; 0x0056834c: mov edi, dword ptr [ebp + 8] ; 0x0056834f: cmp eax, edi ; 0x00568351: jae 0x568377
  - 0x00568363: jb -> 0x0056837e (jcc_true) | ctx: 0x0056835d: idiv ebx ; 0x0056835f: sub ecx, eax ; 0x00568361: cmp ecx, edi ; 0x00568363: jb 0x56837e
  - 0x00568363: jb -> 0x00568365 (jcc_false) | ctx: 0x0056835d: idiv ebx ; 0x0056835f: sub ecx, eax ; 0x00568361: cmp ecx, edi ; 0x00568363: jb 0x56837e

### 0x005684d7
- blocks=3, insns=28, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00569602 at 0x005684e3)
  - caller_of_anchor_path: depth 2 (calls 0x00677fd2 at 0x0056872b)
- branch points:
  - 0x005684ea: je -> 0x005684fe (jcc_true) | ctx: 0x005684e0: mov dword ptr [edi + 8], ebx ; 0x005684e3: call 0x5695ff ; 0x005684e8: test al, al ; 0x005684ea: je 0x5684fe
  - 0x005684ea: je -> 0x005684ec (jcc_false) | ctx: 0x005684e0: mov dword ptr [edi + 8], ebx ; 0x005684e3: call 0x5695ff ; 0x005684e8: test al, al ; 0x005684ea: je 0x5684fe

### 0x00569602
- blocks=6, insns=36, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00569628)
- branch points:
  - 0x00569615: jne -> 0x0056961b (jcc_true) | ctx: 0x0056960d: mov dword ptr [esi + 4], eax ; 0x00569610: mov dword ptr [esi + 8], eax ; 0x00569613: test edi, edi ; 0x00569615: jne 0x56961b
  - 0x00569615: jne -> 0x00569617 (jcc_false) | ctx: 0x0056960d: mov dword ptr [esi + 4], eax ; 0x00569610: mov dword ptr [esi + 8], eax ; 0x00569613: test edi, edi ; 0x00569615: jne 0x56961b
  - 0x00569621: ja -> 0x00569645 (jcc_true) | ctx: 0x0056961b: cmp edi, 0x3fffffff ; 0x00569621: ja 0x569645
  - 0x00569621: ja -> 0x00569623 (jcc_false) | ctx: 0x0056961b: cmp edi, 0x3fffffff ; 0x00569621: ja 0x569645
  - 0x00569619: jmp -> 0x0056963f (jmp) | ctx: 0x00569617: xor al, al ; 0x00569619: jmp 0x56963f

### 0x005696ac
- blocks=3, insns=61, edges=5, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005696be)
- branch points:
  - 0x005696e4: je -> 0x005696fa (jcc_true) | ctx: 0x005696dc: idiv ecx ; 0x005696de: cmp dword ptr [esi], 0 ; 0x005696e1: mov dword ptr [ebp + 8], eax ; 0x005696e4: je 0x5696fa
  - 0x005696e4: je -> 0x005696e6 (jcc_false) | ctx: 0x005696dc: idiv ecx ; 0x005696de: cmp dword ptr [esi], 0 ; 0x005696e1: mov dword ptr [ebp + 8], eax ; 0x005696e4: je 0x5696fa

### 0x00569763
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005696ac at 0x0056979b)
- branch points:
  - 0x0056977a: jae -> 0x005697a0 (jcc_true) | ctx: 0x00569773: idiv ebx ; 0x00569775: mov edi, dword ptr [ebp + 8] ; 0x00569778: cmp eax, edi ; 0x0056977a: jae 0x5697a0
  - 0x0056977a: jae -> 0x0056977c (jcc_false) | ctx: 0x00569773: idiv ebx ; 0x00569775: mov edi, dword ptr [ebp + 8] ; 0x00569778: cmp eax, edi ; 0x0056977a: jae 0x5697a0
  - 0x0056978c: jb -> 0x005697a7 (jcc_true) | ctx: 0x00569786: idiv ebx ; 0x00569788: sub ecx, eax ; 0x0056978a: cmp ecx, edi ; 0x0056978c: jb 0x5697a7
  - 0x0056978c: jb -> 0x0056978e (jcc_false) | ctx: 0x00569786: idiv ebx ; 0x00569788: sub ecx, eax ; 0x0056978a: cmp ecx, edi ; 0x0056978c: jb 0x5697a7

### 0x0056a378
- blocks=1, insns=23, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0056a39e)
- branch points:
  - none

### 0x0056a408
- blocks=2, insns=17, edges=4, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x005804ab at 0x0056a434)
- branch points:
  - 0x0056a416: jmp -> 0x0056a3ad (jmp) | ctx: 0x0056a40e: call 0x56a3ad ; 0x0056a413: mov ecx, esi ; 0x0056a415: pop esi ; 0x0056a416: jmp 0x56a3ad

### 0x0056a50a
- blocks=1, insns=3, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCBlockingStatusPredicate@EGL@@ slot 0 (target 0x0056a50a, vtable 0x00bc72e0)
- branch points:
  - none

### 0x0056af26
- blocks=8, insns=60, edges=13, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00580fd5 at 0x0056b005)
- branch points:
  - 0x0056af37: jne -> 0x0056af53 (jcc_true) | ctx: 0x0056af2f: mov edi, dword ptr [eax] ; 0x0056af31: imul edi, edi ; 0x0056af34: cmp dword ptr [esi + 8], ebx ; 0x0056af37: jne 0x56af53
  - 0x0056af37: jne -> 0x0056af39 (jcc_false) | ctx: 0x0056af2f: mov edi, dword ptr [eax] ; 0x0056af31: imul edi, edi ; 0x0056af34: cmp dword ptr [esi + 8], ebx ; 0x0056af37: jne 0x56af53
  - 0x0056af66: jne -> 0x0056af84 (jcc_true) | ctx: 0x0056af5b: call 0xacf2c0 ; 0x0056af60: add esp, 0xc ; 0x0056af63: cmp dword ptr [esi + 0xc], ebx ; 0x0056af66: jne 0x56af84
  - 0x0056af66: jne -> 0x0056af68 (jcc_false) | ctx: 0x0056af5b: call 0xacf2c0 ; 0x0056af60: add esp, 0xc ; 0x0056af63: cmp dword ptr [esi + 0xc], ebx ; 0x0056af66: jne 0x56af84
  - 0x0056af66: jne -> 0x0056af84 (jcc_true) | ctx: 0x0056af5b: call 0xacf2c0 ; 0x0056af60: add esp, 0xc ; 0x0056af63: cmp dword ptr [esi + 0xc], ebx ; 0x0056af66: jne 0x56af84
  - 0x0056af66: jne -> 0x0056af68 (jcc_false) | ctx: 0x0056af5b: call 0xacf2c0 ; 0x0056af60: add esp, 0xc ; 0x0056af63: cmp dword ptr [esi + 0xc], ebx ; 0x0056af66: jne 0x56af84
  - 0x0056af72: je -> 0x0056af7f (jcc_true) | ctx: 0x0056af6a: call 0xab67aa ; 0x0056af6f: pop ecx ; 0x0056af70: test eax, eax ; 0x0056af72: je 0x56af7f
  - 0x0056af72: je -> 0x0056af74 (jcc_false) | ctx: 0x0056af6a: call 0xab67aa ; 0x0056af6f: pop ecx ; 0x0056af70: test eax, eax ; 0x0056af72: je 0x56af7f
  - 0x0056af7d: jmp -> 0x0056af81 (jmp) | ctx: 0x0056af74: mov dword ptr [eax + 4], ebx ; 0x0056af77: mov dword ptr [eax], 0xbc72f8 ; 0x0056af7d: jmp 0x56af81

### 0x0056b0c1
- blocks=7, insns=60, edges=17, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00580fd5 at 0x0056b10b)
- branch points:
  - 0x0056b0e5: je -> 0x0056b101 (jcc_true) | ctx: 0x0056b0dc: mov edi, dword ptr [ebp + 0xc] ; 0x0056b0df: add esp, 0x10 ; 0x0056b0e2: test byte ptr [edi], 1 ; 0x0056b0e5: je 0x56b101
  - 0x0056b0e5: je -> 0x0056b0e7 (jcc_false) | ctx: 0x0056b0dc: mov edi, dword ptr [ebp + 0xc] ; 0x0056b0df: add esp, 0x10 ; 0x0056b0e2: test byte ptr [edi], 1 ; 0x0056b0e5: je 0x56b101
  - 0x0056b113: je -> 0x0056b12c (jcc_true) | ctx: 0x0056b108: push dword ptr [ebp - 8] ; 0x0056b10b: call 0x580fb5 ; 0x0056b110: test byte ptr [edi], 1 ; 0x0056b113: je 0x56b12c
  - 0x0056b113: je -> 0x0056b115 (jcc_false) | ctx: 0x0056b108: push dword ptr [ebp - 8] ; 0x0056b10b: call 0x580fb5 ; 0x0056b110: test byte ptr [edi], 1 ; 0x0056b113: je 0x56b12c
  - 0x0056b0f1: je -> 0x0056b101 (jcc_true) | ctx: 0x0056b0ea: mov eax, dword ptr [ecx] ; 0x0056b0ec: call dword ptr [eax + 0x38] ; 0x0056b0ef: test al, al ; 0x0056b0f1: je 0x56b101
  - 0x0056b0f1: je -> 0x0056b0f3 (jcc_false) | ctx: 0x0056b0ea: mov eax, dword ptr [ecx] ; 0x0056b0ec: call dword ptr [eax + 0x38] ; 0x0056b0ef: test al, al ; 0x0056b0f1: je 0x56b101
  - 0x0056b11f: je -> 0x0056b12c (jcc_true) | ctx: 0x0056b118: mov eax, dword ptr [ecx] ; 0x0056b11a: call dword ptr [eax + 0x38] ; 0x0056b11d: test al, al ; 0x0056b11f: je 0x56b12c
  - 0x0056b11f: je -> 0x0056b121 (jcc_false) | ctx: 0x0056b118: mov eax, dword ptr [ecx] ; 0x0056b11a: call dword ptr [eax + 0x38] ; 0x0056b11d: test al, al ; 0x0056b11f: je 0x56b12c
  - 0x0056b113: je -> 0x0056b12c (jcc_true) | ctx: 0x0056b108: push dword ptr [ebp - 8] ; 0x0056b10b: call 0x580fb5 ; 0x0056b110: test byte ptr [edi], 1 ; 0x0056b113: je 0x56b12c
  - 0x0056b113: je -> 0x0056b115 (jcc_false) | ctx: 0x0056b108: push dword ptr [ebp - 8] ; 0x0056b10b: call 0x580fb5 ; 0x0056b110: test byte ptr [edi], 1 ; 0x0056b113: je 0x56b12c

### 0x0056cf36
- blocks=1, insns=13, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCAStar64Normal@EGL@@ slot 0 (target 0x0056cf36, vtable 0x00bc9238)
- branch points:
  - none

### 0x0056eb15
- blocks=3, insns=61, edges=5, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0056eb27)
- branch points:
  - 0x0056eb4d: je -> 0x0056eb63 (jcc_true) | ctx: 0x0056eb45: idiv ecx ; 0x0056eb47: cmp dword ptr [esi], 0 ; 0x0056eb4a: mov dword ptr [ebp + 8], eax ; 0x0056eb4d: je 0x56eb63
  - 0x0056eb4d: je -> 0x0056eb4f (jcc_false) | ctx: 0x0056eb45: idiv ecx ; 0x0056eb47: cmp dword ptr [esi], 0 ; 0x0056eb4a: mov dword ptr [ebp + 8], eax ; 0x0056eb4d: je 0x56eb63

### 0x0056eb81
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0056eb15 at 0x0056ebb9)
- branch points:
  - 0x0056eb98: jae -> 0x0056ebbe (jcc_true) | ctx: 0x0056eb91: idiv ebx ; 0x0056eb93: mov edi, dword ptr [ebp + 8] ; 0x0056eb96: cmp eax, edi ; 0x0056eb98: jae 0x56ebbe
  - 0x0056eb98: jae -> 0x0056eb9a (jcc_false) | ctx: 0x0056eb91: idiv ebx ; 0x0056eb93: mov edi, dword ptr [ebp + 8] ; 0x0056eb96: cmp eax, edi ; 0x0056eb98: jae 0x56ebbe
  - 0x0056ebaa: jb -> 0x0056ebc5 (jcc_true) | ctx: 0x0056eba4: idiv ebx ; 0x0056eba6: sub ecx, eax ; 0x0056eba8: cmp ecx, edi ; 0x0056ebaa: jb 0x56ebc5
  - 0x0056ebaa: jb -> 0x0056ebac (jcc_false) | ctx: 0x0056eba4: idiv ebx ; 0x0056eba6: sub ecx, eax ; 0x0056eba8: cmp ecx, edi ; 0x0056ebaa: jb 0x56ebc5

### 0x005706d2
- blocks=1, insns=11, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00570fb3 at 0x005706df)
- branch points:
  - none

### 0x00570fb3
- blocks=5, insns=40, edges=6, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00571019)
- branch points:
  - 0x00570fc3: je -> 0x00570ff1 (jcc_true) | ctx: 0x00570fbe: cdq ; 0x00570fbf: idiv ecx ; 0x00570fc1: test eax, eax ; 0x00570fc3: je 0x570ff1
  - 0x00570fc3: je -> 0x00570fc5 (jcc_false) | ctx: 0x00570fbe: cdq ; 0x00570fbf: idiv ecx ; 0x00570fc1: test eax, eax ; 0x00570fc3: je 0x570ff1
  - 0x00570fe3: je -> 0x00570ff0 (jcc_true) | ctx: 0x00570fda: push eax ; 0x00570fdb: call 0x570e9d ; 0x00570fe0: cmp eax, -1 ; 0x00570fe3: je 0x570ff0
  - 0x00570fe3: je -> 0x00570fe5 (jcc_false) | ctx: 0x00570fda: push eax ; 0x00570fdb: call 0x570e9d ; 0x00570fe0: cmp eax, -1 ; 0x00570fe3: je 0x570ff0

### 0x0057113f
- blocks=5, insns=62, edges=8, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00564601 at 0x00571162)
- branch points:
  - 0x0057115b: jbe -> 0x0057117a (jcc_true) | ctx: 0x00571154: mov ecx, eax ; 0x00571156: mov dword ptr [ebp - 0x14], esi ; 0x00571159: cmp ecx, edi ; 0x0057115b: jbe 0x57117a
  - 0x0057115b: jbe -> 0x0057115d (jcc_false) | ctx: 0x00571154: mov ecx, eax ; 0x00571156: mov dword ptr [ebp - 0x14], esi ; 0x00571159: cmp ecx, edi ; 0x0057115b: jbe 0x57117a
  - 0x0057117a: jae -> 0x00571167 (jcc_true) | ctx: 0x0057117a: jae 0x571167
  - 0x0057117a: jae -> 0x0057117c (jcc_false) | ctx: 0x0057117a: jae 0x571167
  - 0x005711b8: jmp -> 0x00571167 (jmp) | ctx: 0x005711b0: sub edi, eax ; 0x005711b2: imul eax, edi, 0xc ; 0x005711b5: add dword ptr [esi + 4], eax ; 0x005711b8: jmp 0x571167

### 0x005727d7
- blocks=3, insns=22, edges=5, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005761c7 at 0x00572928)
  - caller_of_anchor_path: depth 2 (calls 0x0057624f at 0x0057285c)
- branch points:
  - 0x005727ea: je -> 0x005727fa (jcc_true) | ctx: 0x005727e3: xor edi, edi ; 0x005727e5: mov dword ptr [ebp - 4], eax ; 0x005727e8: cmp eax, esi ; 0x005727ea: je 0x5727fa
  - 0x005727ea: je -> 0x005727ec (jcc_false) | ctx: 0x005727e3: xor edi, edi ; 0x005727e5: mov dword ptr [ebp - 4], eax ; 0x005727e8: cmp eax, esi ; 0x005727ea: je 0x5727fa
  - 0x005727f8: jne -> 0x005727ec (jcc_true) | ctx: 0x005727ef: inc edi ; 0x005727f0: call 0x577cf5 ; 0x005727f5: cmp dword ptr [ebp - 4], esi ; 0x005727f8: jne 0x5727ec
  - 0x005727f8: jne -> 0x005727fa (jcc_false) | ctx: 0x005727ef: inc edi ; 0x005727f0: call 0x577cf5 ; 0x005727f5: cmp dword ptr [ebp - 4], esi ; 0x005727f8: jne 0x5727ec

### 0x00574ef4
- blocks=10, insns=178, edges=26, jcc=6, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00576019 at 0x00574f05)
- branch points:
  - 0x00574f03: je -> 0x00574f0c (jcc_true) | ctx: 0x00574efc: mov ebx, ecx ; 0x00574efe: push edi ; 0x00574eff: cmp byte ptr [esi + 0x5e], 0 ; 0x00574f03: je 0x574f0c
  - 0x00574f03: je -> 0x00574f05 (jcc_false) | ctx: 0x00574efc: mov ebx, ecx ; 0x00574efe: push edi ; 0x00574eff: cmp byte ptr [esi + 0x5e], 0 ; 0x00574f03: je 0x574f0c
  - 0x00574ff1: je -> 0x0057500e (jcc_true) | ctx: 0x00574fe4: call 0x575e73 ; 0x00574fe9: mov eax, dword ptr [ebx + 0xac] ; 0x00574fef: test eax, eax ; 0x00574ff1: je 0x57500e
  - 0x00574ff1: je -> 0x00574ff3 (jcc_false) | ctx: 0x00574fe4: call 0x575e73 ; 0x00574fe9: mov eax, dword ptr [ebx + 0xac] ; 0x00574fef: test eax, eax ; 0x00574ff1: je 0x57500e
  - 0x00574f0a: jmp -> 0x00574f11 (jmp) | ctx: 0x00574f05: call 0x575ff9 ; 0x00574f0a: jmp 0x574f11
  - 0x00575052: jmp -> 0x0057505f (jmp) | ctx: 0x00575045: cvttss2si eax, xmm1 ; 0x00575049: mov dword ptr [ebx + 0xa8], eax ; 0x0057504f: mov esi, dword ptr [ebx + 0x68] ; 0x00575052: jmp 0x57505f
  - 0x00574ffc: je -> 0x0057500e (jcc_true) | ctx: 0x00574ff4: call 0xadde70 ; 0x00574ff9: pop ecx ; 0x00574ffa: test eax, eax ; 0x00574ffc: je 0x57500e
  - 0x00574ffc: je -> 0x00574ffe (jcc_false) | ctx: 0x00574ff4: call 0xadde70 ; 0x00574ff9: pop ecx ; 0x00574ffa: test eax, eax ; 0x00574ffc: je 0x57500e
  - 0x00574ff1: je -> 0x0057500e (jcc_true) | ctx: 0x00574fe4: call 0x575e73 ; 0x00574fe9: mov eax, dword ptr [ebx + 0xac] ; 0x00574fef: test eax, eax ; 0x00574ff1: je 0x57500e
  - 0x00574ff1: je -> 0x00574ff3 (jcc_false) | ctx: 0x00574fe4: call 0x575e73 ; 0x00574fe9: mov eax, dword ptr [ebx + 0xac] ; 0x00574fef: test eax, eax ; 0x00574ff1: je 0x57500e
  - 0x00575062: jne -> 0x00575054 (jcc_true) | ctx: 0x0057505f: cmp esi, dword ptr [ebx + 0x6c] ; 0x00575062: jne 0x575054
  - 0x00575062: jne -> 0x00575064 (jcc_false) | ctx: 0x0057505f: cmp esi, dword ptr [ebx + 0x6c] ; 0x00575062: jne 0x575054
  - 0x00575052: jmp -> 0x0057505f (jmp) | ctx: 0x00575045: cvttss2si eax, xmm1 ; 0x00575049: mov dword ptr [ebx + 0xa8], eax ; 0x0057504f: mov esi, dword ptr [ebx + 0x68] ; 0x00575052: jmp 0x57505f
  - 0x00575062: jne -> 0x00575054 (jcc_true) | ctx: 0x00575059: call dword ptr [eax + 0x18] ; 0x0057505c: add esi, 4 ; 0x0057505f: cmp esi, dword ptr [ebx + 0x6c] ; 0x00575062: jne 0x575054
  - 0x00575062: jne -> 0x00575064 (jcc_false) | ctx: 0x00575059: call dword ptr [eax + 0x18] ; 0x0057505c: add esi, 4 ; 0x0057505f: cmp esi, dword ptr [ebx + 0x6c] ; 0x00575062: jne 0x575054

### 0x005751ed
- blocks=1, insns=14, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005761c7 at 0x00575202)
- branch points:
  - none

### 0x00575fc7
- blocks=3, insns=19, edges=5, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057b4ed at 0x00575ff2)
- branch points:
  - 0x00575fdd: je -> 0x00575ff7 (jcc_true) | ctx: 0x00575fd1: lea ecx, [ecx + 0x28] ; 0x00575fd4: call 0x578dc8 ; 0x00575fd9: cmp dword ptr [esi + 0x18], 0 ; 0x00575fdd: je 0x575ff7
  - 0x00575fdd: je -> 0x00575fdf (jcc_false) | ctx: 0x00575fd1: lea ecx, [ecx + 0x28] ; 0x00575fd4: call 0x578dc8 ; 0x00575fd9: cmp dword ptr [esi + 0x18], 0 ; 0x00575fdd: je 0x575ff7

### 0x00576019
- blocks=12, insns=128, edges=26, jcc=7, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00576061)
- branch points:
  - 0x00576035: jb -> 0x0057603c (jcc_true) | ctx: 0x0057602e: mov eax, edi ; 0x00576030: sub eax, ecx ; 0x00576032: cmp eax, dword ptr [ebp + 8] ; 0x00576035: jb 0x57603c
  - 0x00576035: jb -> 0x00576037 (jcc_false) | ctx: 0x0057602e: mov eax, edi ; 0x00576030: sub eax, ecx ; 0x00576032: cmp eax, dword ptr [ebp + 8] ; 0x00576035: jb 0x57603c
  - 0x00576045: jb -> 0x00576123 (jcc_true) | ctx: 0x0057603c: mov eax, 0xfffffff ; 0x00576041: sub eax, edi ; 0x00576043: cmp eax, edi ; 0x00576045: jb 0x576123
  - 0x00576045: jb -> 0x0057604b (jcc_false) | ctx: 0x0057603c: mov eax, 0xfffffff ; 0x00576041: sub eax, edi ; 0x00576043: cmp eax, edi ; 0x00576045: jb 0x576123
  - 0x0057603a: jae -> 0x0057604f (jcc_true) | ctx: 0x00576037: cmp edi, 8 ; 0x0057603a: jae 0x57604f
  - 0x0057603a: jae -> 0x0057603c (jcc_false) | ctx: 0x00576037: cmp edi, 8 ; 0x0057603a: jae 0x57604f
  - 0x0057604d: jmp -> 0x0057602e (jmp) | ctx: 0x0057604b: add edi, edi ; 0x0057604d: jmp 0x57602e
  - 0x00576091: ja -> 0x005760c7 (jcc_true) | ctx: 0x00576089: mov eax, dword ptr [ebp + 8] ; 0x0057608c: mov dword ptr [ebp - 8], edx ; 0x0057608f: cmp eax, edi ; 0x00576091: ja 0x5760c7
  - 0x00576091: ja -> 0x00576093 (jcc_false) | ctx: 0x00576089: mov eax, dword ptr [ebp + 8] ; 0x0057608c: mov dword ptr [ebp - 8], edx ; 0x0057608f: cmp eax, edi ; 0x00576091: ja 0x5760c7
  - 0x00576035: jb -> 0x0057603c (jcc_true) | ctx: 0x0057602e: mov eax, edi ; 0x00576030: sub eax, ecx ; 0x00576032: cmp eax, dword ptr [ebp + 8] ; 0x00576035: jb 0x57603c
  - 0x00576035: jb -> 0x00576037 (jcc_false) | ctx: 0x0057602e: mov eax, edi ; 0x00576030: sub eax, ecx ; 0x00576032: cmp eax, dword ptr [ebp + 8] ; 0x00576035: jb 0x57603c
  - 0x00576102: je -> 0x00576114 (jcc_true) | ctx: 0x005760f8: mov esi, dword ptr [ebp - 4] ; 0x005760fb: add esp, 0x24 ; 0x005760fe: cmp dword ptr [ebx + 4], 0 ; 0x00576102: je 0x576114
  - 0x00576102: je -> 0x00576104 (jcc_false) | ctx: 0x005760f8: mov esi, dword ptr [ebp - 4] ; 0x005760fb: add esp, 0x24 ; 0x005760fe: cmp dword ptr [ebx + 4], 0 ; 0x00576102: je 0x576114
  - 0x005760c5: jmp -> 0x005760fb (jmp) | ctx: 0x005760bd: push 0 ; 0x005760bf: push esi ; 0x005760c0: call 0xacf2c0 ; 0x005760c5: jmp 0x5760fb
  - 0x00576102: je -> 0x00576114 (jcc_true) | ctx: 0x005760fb: add esp, 0x24 ; 0x005760fe: cmp dword ptr [ebx + 4], 0 ; 0x00576102: je 0x576114
  - 0x00576102: je -> 0x00576104 (jcc_false) | ctx: 0x005760fb: add esp, 0x24 ; 0x005760fe: cmp dword ptr [ebx + 4], 0 ; 0x00576102: je 0x576114

### 0x005761c7
- blocks=8, insns=80, edges=14, jcc=6, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00576217)
  - caller_of_anchor_path: depth 2 (calls 0x00576019 at 0x005761e4)
- branch points:
  - 0x005761d4: jne -> 0x005761e9 (jcc_true) | ctx: 0x005761cd: mov ecx, dword ptr [esi + 0x10] ; 0x005761d0: add eax, ecx ; 0x005761d2: test al, 1 ; 0x005761d4: jne 0x5761e9
  - 0x005761d4: jne -> 0x005761d6 (jcc_false) | ctx: 0x005761cd: mov ecx, dword ptr [esi + 0x10] ; 0x005761d0: add eax, ecx ; 0x005761d2: test al, 1 ; 0x005761d4: jne 0x5761e9
  - 0x0057620f: jne -> 0x00576225 (jcc_true) | ctx: 0x00576206: and edi, eax ; 0x00576208: mov eax, dword ptr [esi + 4] ; 0x0057620b: cmp dword ptr [eax + edi*4], 0 ; 0x0057620f: jne 0x576225
  - 0x0057620f: jne -> 0x00576211 (jcc_false) | ctx: 0x00576206: and edi, eax ; 0x00576208: mov eax, dword ptr [esi + 4] ; 0x0057620b: cmp dword ptr [eax + edi*4], 0 ; 0x0057620f: jne 0x576225
  - 0x005761de: ja -> 0x005761e9 (jcc_true) | ctx: 0x005761d6: lea eax, [ecx + 2] ; 0x005761d9: shr eax, 1 ; 0x005761db: cmp dword ptr [esi + 8], eax ; 0x005761de: ja 0x5761e9
  - 0x005761de: ja -> 0x005761e0 (jcc_false) | ctx: 0x005761d6: lea eax, [ecx + 2] ; 0x005761d9: shr eax, 1 ; 0x005761db: cmp dword ptr [esi + 8], eax ; 0x005761de: ja 0x5761e9
  - 0x00576235: je -> 0x00576244 (jcc_true) | ctx: 0x0057622f: lea edx, [eax + ebx*8] ; 0x00576232: pop ebx ; 0x00576233: test edx, edx ; 0x00576235: je 0x576244
  - 0x00576235: je -> 0x00576237 (jcc_false) | ctx: 0x0057622f: lea edx, [eax + ebx*8] ; 0x00576232: pop ebx ; 0x00576233: test edx, edx ; 0x00576235: je 0x576244
  - 0x00576235: je -> 0x00576244 (jcc_true) | ctx: 0x0057622f: lea edx, [eax + ebx*8] ; 0x00576232: pop ebx ; 0x00576233: test edx, edx ; 0x00576235: je 0x576244
  - 0x00576235: je -> 0x00576237 (jcc_false) | ctx: 0x0057622f: lea edx, [eax + ebx*8] ; 0x00576232: pop ebx ; 0x00576233: test edx, edx ; 0x00576235: je 0x576244
  - 0x0057620f: jne -> 0x00576225 (jcc_true) | ctx: 0x00576206: and edi, eax ; 0x00576208: mov eax, dword ptr [esi + 4] ; 0x0057620b: cmp dword ptr [eax + edi*4], 0 ; 0x0057620f: jne 0x576225
  - 0x0057620f: jne -> 0x00576211 (jcc_false) | ctx: 0x00576206: and edi, eax ; 0x00576208: mov eax, dword ptr [esi + 4] ; 0x0057620b: cmp dword ptr [eax + edi*4], 0 ; 0x0057620f: jne 0x576225

### 0x0057624f
- blocks=10, insns=84, edges=18, jcc=8, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0057629f)
  - caller_of_anchor_path: depth 2 (calls 0x00576019 at 0x00576268)
- branch points:
  - 0x00576257: jne -> 0x0057626d (jcc_true) | ctx: 0x00576250: mov esi, ecx ; 0x00576252: push edi ; 0x00576253: test byte ptr [esi + 0xc], 1 ; 0x00576257: jne 0x57626d
  - 0x00576257: jne -> 0x00576259 (jcc_false) | ctx: 0x00576250: mov esi, ecx ; 0x00576252: push edi ; 0x00576253: test byte ptr [esi + 0xc], 1 ; 0x00576257: jne 0x57626d
  - 0x0057627d: jne -> 0x00576284 (jcc_true) | ctx: 0x00576270: lea eax, [eax*2 - 1] ; 0x00576277: and dword ptr [esi + 0xc], eax ; 0x0057627a: mov edi, dword ptr [esi + 0xc] ; 0x0057627d: jne 0x576284
  - 0x0057627d: jne -> 0x0057627f (jcc_false) | ctx: 0x00576270: lea eax, [eax*2 - 1] ; 0x00576277: and dword ptr [esi + 0xc], eax ; 0x0057627a: mov edi, dword ptr [esi + 0xc] ; 0x0057627d: jne 0x576284
  - 0x00576264: ja -> 0x0057626d (jcc_true) | ctx: 0x0057625c: add eax, 2 ; 0x0057625f: shr eax, 1 ; 0x00576261: cmp dword ptr [esi + 8], eax ; 0x00576264: ja 0x57626d
  - 0x00576264: ja -> 0x00576266 (jcc_false) | ctx: 0x0057625c: add eax, 2 ; 0x0057625f: shr eax, 1 ; 0x00576261: cmp dword ptr [esi + 8], eax ; 0x00576264: ja 0x57626d
  - 0x00576297: jne -> 0x005762ad (jcc_true) | ctx: 0x0057628e: and ebx, eax ; 0x00576290: mov eax, dword ptr [esi + 4] ; 0x00576293: cmp dword ptr [eax + ebx*4], 0 ; 0x00576297: jne 0x5762ad
  - 0x00576297: jne -> 0x00576299 (jcc_false) | ctx: 0x0057628e: and ebx, eax ; 0x00576290: mov eax, dword ptr [esi + 4] ; 0x00576293: cmp dword ptr [eax + ebx*4], 0 ; 0x00576297: jne 0x5762ad
  - 0x00576297: jne -> 0x005762ad (jcc_true) | ctx: 0x0057628e: and ebx, eax ; 0x00576290: mov eax, dword ptr [esi + 4] ; 0x00576293: cmp dword ptr [eax + ebx*4], 0 ; 0x00576297: jne 0x5762ad
  - 0x00576297: jne -> 0x00576299 (jcc_false) | ctx: 0x0057628e: and ebx, eax ; 0x00576290: mov eax, dword ptr [esi + 4] ; 0x00576293: cmp dword ptr [eax + ebx*4], 0 ; 0x00576297: jne 0x5762ad
  - 0x0057627d: jne -> 0x00576284 (jcc_true) | ctx: 0x00576270: lea eax, [eax*2 - 1] ; 0x00576277: and dword ptr [esi + 0xc], eax ; 0x0057627a: mov edi, dword ptr [esi + 0xc] ; 0x0057627d: jne 0x576284
  - 0x0057627d: jne -> 0x0057627f (jcc_false) | ctx: 0x00576270: lea eax, [eax*2 - 1] ; 0x00576277: and dword ptr [esi + 0xc], eax ; 0x0057627a: mov edi, dword ptr [esi + 0xc] ; 0x0057627d: jne 0x576284
  - 0x005762be: je -> 0x005762cd (jcc_true) | ctx: 0x005762b8: pop ebx ; 0x005762b9: lea edx, [eax + ecx*8] ; 0x005762bc: test edx, edx ; 0x005762be: je 0x5762cd
  - 0x005762be: je -> 0x005762c0 (jcc_false) | ctx: 0x005762b8: pop ebx ; 0x005762b9: lea edx, [eax + ecx*8] ; 0x005762bc: test edx, edx ; 0x005762be: je 0x5762cd
  - 0x005762be: je -> 0x005762cd (jcc_true) | ctx: 0x005762b8: pop ebx ; 0x005762b9: lea edx, [eax + ecx*8] ; 0x005762bc: test edx, edx ; 0x005762be: je 0x5762cd
  - 0x005762be: je -> 0x005762c0 (jcc_false) | ctx: 0x005762b8: pop ebx ; 0x005762b9: lea edx, [eax + ecx*8] ; 0x005762bc: test edx, edx ; 0x005762be: je 0x5762cd

### 0x00576996
- blocks=6, insns=24, edges=9, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005769c6)
- branch points:
  - 0x005769a7: je -> 0x005769b1 (jcc_true) | ctx: 0x0057699f: push eax ; 0x005769a0: call 0x69570e ; 0x005769a5: cmp eax, dword ptr [esi] ; 0x005769a7: je 0x5769b1
  - 0x005769a7: je -> 0x005769a9 (jcc_false) | ctx: 0x0057699f: push eax ; 0x005769a0: call 0x69570e ; 0x005769a5: cmp eax, dword ptr [esi] ; 0x005769a7: je 0x5769b1
  - 0x005769b6: je -> 0x005769bc (jcc_true) | ctx: 0x005769b1: mov eax, dword ptr [esi] ; 0x005769b3: cmp eax, dword ptr [esi] ; 0x005769b5: pop esi ; 0x005769b6: je 0x5769bc
  - 0x005769b6: je -> 0x005769b8 (jcc_false) | ctx: 0x005769b1: mov eax, dword ptr [esi] ; 0x005769b3: cmp eax, dword ptr [esi] ; 0x005769b5: pop esi ; 0x005769b6: je 0x5769bc
  - 0x005769af: jge -> 0x005769b3 (jcc_true) | ctx: 0x005769a9: mov ecx, dword ptr [ebp + 8] ; 0x005769ac: cmp ecx, dword ptr [eax + 0x10] ; 0x005769af: jge 0x5769b3
  - 0x005769af: jge -> 0x005769b1 (jcc_false) | ctx: 0x005769a9: mov ecx, dword ptr [ebp + 8] ; 0x005769ac: cmp ecx, dword ptr [eax + 0x10] ; 0x005769af: jge 0x5769b3
  - 0x005769b6: je -> 0x005769bc (jcc_true) | ctx: 0x005769b3: cmp eax, dword ptr [esi] ; 0x005769b5: pop esi ; 0x005769b6: je 0x5769bc
  - 0x005769b6: je -> 0x005769b8 (jcc_false) | ctx: 0x005769b3: cmp eax, dword ptr [esi] ; 0x005769b5: pop esi ; 0x005769b6: je 0x5769bc

### 0x005769ed
- blocks=3, insns=29, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00576a4f)
  - caller_of_anchor_path: depth 2 (calls 0x005769ed at 0x00576a05)
- branch points:
  - 0x005769fe: jne -> 0x00576a29 (jcc_true) | ctx: 0x005769f7: push edi ; 0x005769f8: mov edi, esi ; 0x005769fa: cmp byte ptr [esi + 0xd], 0 ; 0x005769fe: jne 0x576a29
  - 0x005769fe: jne -> 0x00576a00 (jcc_false) | ctx: 0x005769f7: push edi ; 0x005769f8: mov edi, esi ; 0x005769fa: cmp byte ptr [esi + 0xd], 0 ; 0x005769fe: jne 0x576a29
  - 0x00576a27: je -> 0x00576a00 (jcc_true) | ctx: 0x00576a1e: add esp, 0xc ; 0x00576a21: mov esi, edi ; 0x00576a23: cmp byte ptr [edi + 0xd], 0 ; 0x00576a27: je 0x576a00
  - 0x00576a27: je -> 0x00576a29 (jcc_false) | ctx: 0x00576a1e: add esp, 0xc ; 0x00576a21: mov esi, edi ; 0x00576a23: cmp byte ptr [edi + 0xd], 0 ; 0x00576a27: je 0x576a00

### 0x00576df0
- blocks=3, insns=31, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00569602 at 0x00576e0a)
- branch points:
  - 0x00576e11: je -> 0x00576e25 (jcc_true) | ctx: 0x00576e09: push eax ; 0x00576e0a: call 0x5695ff ; 0x00576e0f: test al, al ; 0x00576e11: je 0x576e25
  - 0x00576e11: je -> 0x00576e13 (jcc_false) | ctx: 0x00576e09: push eax ; 0x00576e0a: call 0x5695ff ; 0x00576e0f: test al, al ; 0x00576e11: je 0x576e25

### 0x00577c3d
- blocks=14, insns=99, edges=24, jcc=7, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00569602 at 0x00577cd1)
- branch points:
  - 0x00577c42: je -> 0x00577ced (jcc_true) | ctx: 0x00577c3d: push edi ; 0x00577c3e: mov edi, ecx ; 0x00577c40: cmp edi, ebx ; 0x00577c42: je 0x577ced
  - 0x00577c42: je -> 0x00577c48 (jcc_false) | ctx: 0x00577c3d: push edi ; 0x00577c3e: mov edi, ecx ; 0x00577c40: cmp edi, ebx ; 0x00577c42: je 0x577ced
  - 0x00577c4d: jne -> 0x00577c59 (jcc_true) | ctx: 0x00577c48: mov ecx, dword ptr [ebx] ; 0x00577c4a: cmp ecx, dword ptr [ebx + 4] ; 0x00577c4d: jne 0x577c59
  - 0x00577c4d: jne -> 0x00577c4f (jcc_false) | ctx: 0x00577c48: mov ecx, dword ptr [ebx] ; 0x00577c4a: cmp ecx, dword ptr [ebx + 4] ; 0x00577c4d: jne 0x577c59
  - 0x00577c6c: ja -> 0x00577c8b (jcc_true) | ctx: 0x00577c64: sar edx, 2 ; 0x00577c67: sar esi, 2 ; 0x00577c6a: cmp edx, esi ; 0x00577c6c: ja 0x577c8b
  - 0x00577c6c: ja -> 0x00577c6e (jcc_false) | ctx: 0x00577c64: sar edx, 2 ; 0x00577c67: sar esi, 2 ; 0x00577c6a: cmp edx, esi ; 0x00577c6c: ja 0x577c8b
  - 0x00577c54: jmp -> 0x00577ced (jmp) | ctx: 0x00577c4f: mov eax, dword ptr [edi] ; 0x00577c51: mov dword ptr [edi + 4], eax ; 0x00577c54: jmp 0x577ced
  - 0x00577c95: ja -> 0x00577cb4 (jcc_true) | ctx: 0x00577c8e: sub eax, dword ptr [edi] ; 0x00577c90: sar eax, 2 ; 0x00577c93: cmp edx, eax ; 0x00577c95: ja 0x577cb4
  - 0x00577c95: ja -> 0x00577c97 (jcc_false) | ctx: 0x00577c8e: sub eax, dword ptr [edi] ; 0x00577c90: sar eax, 2 ; 0x00577c93: cmp edx, eax ; 0x00577c95: ja 0x577cb4
  - 0x00577c89: jmp -> 0x00577ce9 (jmp) | ctx: 0x00577c81: mov eax, dword ptr [edi] ; 0x00577c83: sar ecx, 2 ; 0x00577c86: lea eax, [eax + ecx*4] ; 0x00577c89: jmp 0x577ce9
  - 0x00577cb7: je -> 0x00577cc6 (jcc_true) | ctx: 0x00577cb4: cmp dword ptr [edi], 0 ; 0x00577cb7: je 0x577cc6
  - 0x00577cb7: je -> 0x00577cb9 (jcc_false) | ctx: 0x00577cb4: cmp dword ptr [edi], 0 ; 0x00577cb7: je 0x577cc6
  - 0x00577cb2: jmp -> 0x00577ce9 (jmp) | ctx: 0x00577ca9: push esi ; 0x00577caa: call 0x570cbe ; 0x00577caf: add esp, 0x18 ; 0x00577cb2: jmp 0x577ce9
  - 0x00577cd8: je -> 0x00577cec (jcc_true) | ctx: 0x00577cd0: push eax ; 0x00577cd1: call 0x5695ff ; 0x00577cd6: test al, al ; 0x00577cd8: je 0x577cec
  - 0x00577cd8: je -> 0x00577cda (jcc_false) | ctx: 0x00577cd0: push eax ; 0x00577cd1: call 0x5695ff ; 0x00577cd6: test al, al ; 0x00577cd8: je 0x577cec
  - 0x00577cd8: je -> 0x00577cec (jcc_true) | ctx: 0x00577cd0: push eax ; 0x00577cd1: call 0x5695ff ; 0x00577cd6: test al, al ; 0x00577cd8: je 0x577cec
  - 0x00577cd8: je -> 0x00577cda (jcc_false) | ctx: 0x00577cd0: push eax ; 0x00577cd1: call 0x5695ff ; 0x00577cd6: test al, al ; 0x00577cd8: je 0x577cec

### 0x005781c1
- blocks=7, insns=83, edges=18, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00578543)
- branch points:
  - 0x005781e4: je -> 0x005781fc (jcc_true) | ctx: 0x005781db: mov dword ptr [ebp + 0x14], eax ; 0x005781de: mov byte ptr [ebp - 4], 1 ; 0x005781e2: test eax, eax ; 0x005781e4: je 0x5781fc
  - 0x005781e4: je -> 0x005781e6 (jcc_false) | ctx: 0x005781db: mov dword ptr [ebp + 0x14], eax ; 0x005781de: mov byte ptr [ebp - 4], 1 ; 0x005781e2: test eax, eax ; 0x005781e4: je 0x5781fc
  - 0x0057820c: je -> 0x0057824f (jcc_true) | ctx: 0x00578204: mov dword ptr [ebp + 0x14], ebx ; 0x00578207: call dword ptr [eax + 4] ; 0x0057820a: test al, al ; 0x0057820c: je 0x57824f
  - 0x0057820c: je -> 0x0057820e (jcc_false) | ctx: 0x00578204: mov dword ptr [ebp + 0x14], ebx ; 0x00578207: call dword ptr [eax + 4] ; 0x0057820a: test al, al ; 0x0057820c: je 0x57824f
  - 0x005781fa: jmp -> 0x005781fe (jmp) | ctx: 0x005781f1: mov ecx, eax ; 0x005781f3: call 0x576fd1 ; 0x005781f8: mov esi, eax ; 0x005781fa: jmp 0x5781fe
  - 0x0057824a: jne -> 0x0057820e (jcc_true) | ctx: 0x00578244: push esi ; 0x00578245: call dword ptr [eax + 4] ; 0x00578248: test al, al ; 0x0057824a: jne 0x57820e
  - 0x0057824a: jne -> 0x0057824c (jcc_false) | ctx: 0x00578244: push esi ; 0x00578245: call dword ptr [eax + 4] ; 0x00578248: test al, al ; 0x0057824a: jne 0x57820e
  - 0x0057820c: je -> 0x0057824f (jcc_true) | ctx: 0x00578204: mov dword ptr [ebp + 0x14], ebx ; 0x00578207: call dword ptr [eax + 4] ; 0x0057820a: test al, al ; 0x0057820c: je 0x57824f
  - 0x0057820c: je -> 0x0057820e (jcc_false) | ctx: 0x00578204: mov dword ptr [ebp + 0x14], ebx ; 0x00578207: call dword ptr [eax + 4] ; 0x0057820a: test al, al ; 0x0057820c: je 0x57824f

### 0x00578e2e
- blocks=3, insns=28, edges=5, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00578e89)
- branch points:
  - 0x00578e49: je -> 0x00578e59 (jcc_true) | ctx: 0x00578e43: sub edi, eax ; 0x00578e45: mov esi, edi ; 0x00578e47: cmp edi, ebx ; 0x00578e49: je 0x578e59
  - 0x00578e49: je -> 0x00578e4b (jcc_false) | ctx: 0x00578e43: sub edi, eax ; 0x00578e45: mov esi, edi ; 0x00578e47: cmp edi, ebx ; 0x00578e49: je 0x578e59
  - 0x00578e57: jne -> 0x00578e4b (jcc_true) | ctx: 0x00578e4d: call 0x578790 ; 0x00578e52: add esi, 0x5c ; 0x00578e55: cmp esi, ebx ; 0x00578e57: jne 0x578e4b
  - 0x00578e57: jne -> 0x00578e59 (jcc_false) | ctx: 0x00578e4d: call 0x578790 ; 0x00578e52: add esi, 0x5c ; 0x00578e55: cmp esi, ebx ; 0x00578e57: jne 0x578e4b

### 0x00579005
- blocks=5, insns=62, edges=8, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00578e2e at 0x00579028)
- branch points:
  - 0x00579021: jbe -> 0x00579040 (jcc_true) | ctx: 0x0057901a: mov ecx, eax ; 0x0057901c: mov dword ptr [ebp - 0x14], esi ; 0x0057901f: cmp ecx, edi ; 0x00579021: jbe 0x579040
  - 0x00579021: jbe -> 0x00579023 (jcc_false) | ctx: 0x0057901a: mov ecx, eax ; 0x0057901c: mov dword ptr [ebp - 0x14], esi ; 0x0057901f: cmp ecx, edi ; 0x00579021: jbe 0x579040
  - 0x00579040: jae -> 0x0057902d (jcc_true) | ctx: 0x00579040: jae 0x57902d
  - 0x00579040: jae -> 0x00579042 (jcc_false) | ctx: 0x00579040: jae 0x57902d
  - 0x0057907e: jmp -> 0x0057902d (jmp) | ctx: 0x00579076: sub edi, eax ; 0x00579078: imul eax, edi, 0x5c ; 0x0057907b: add dword ptr [esi + 4], eax ; 0x0057907e: jmp 0x57902d

### 0x00579280
- blocks=7, insns=68, edges=17, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005781c1 at 0x005797ea)
- branch points:
  - 0x005792b6: je -> 0x005792fa (jcc_true) | ctx: 0x005792af: xor edi, edi ; 0x005792b1: fstp dword ptr [ebp - 8] ; 0x005792b4: test eax, eax ; 0x005792b6: je 0x5792fa
  - 0x005792b6: je -> 0x005792b8 (jcc_false) | ctx: 0x005792af: xor edi, edi ; 0x005792b1: fstp dword ptr [ebp - 8] ; 0x005792b4: test eax, eax ; 0x005792b6: je 0x5792fa
  - 0x005792ba: je -> 0x005792fa (jcc_true) | ctx: 0x005792b8: test ebx, ebx ; 0x005792ba: je 0x5792fa
  - 0x005792ba: je -> 0x005792bc (jcc_false) | ctx: 0x005792b8: test ebx, ebx ; 0x005792ba: je 0x5792fa
  - 0x005792d0: je -> 0x005792fa (jcc_true) | ctx: 0x005792c6: call 0x589b34 ; 0x005792cb: mov ecx, dword ptr [ebp - 4] ; 0x005792ce: test ecx, ecx ; 0x005792d0: je 0x5792fa
  - 0x005792d0: je -> 0x005792d2 (jcc_false) | ctx: 0x005792c6: call 0x589b34 ; 0x005792cb: mov ecx, dword ptr [ebp - 4] ; 0x005792ce: test ecx, ecx ; 0x005792d0: je 0x5792fa
  - 0x005792d4: je -> 0x005792fa (jcc_true) | ctx: 0x005792d2: test eax, eax ; 0x005792d4: je 0x5792fa
  - 0x005792d4: je -> 0x005792d6 (jcc_false) | ctx: 0x005792d2: test eax, eax ; 0x005792d4: je 0x5792fa
  - 0x005792f8: jmp -> 0x005792fd (jmp) | ctx: 0x005792f0: pop ebx ; 0x005792f1: comiss xmm0, dword ptr [ebp - 4] ; 0x005792f5: cmovae edi, ebx ; 0x005792f8: jmp 0x5792fd

### 0x0057a79e
- blocks=1, insns=13, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00576996 at 0x0057a7ba)
- branch points:
  - none

### 0x0057b4ed
- blocks=6, insns=35, edges=10, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0057b52f)
- branch points:
  - 0x0057b50c: je -> 0x0057b513 (jcc_true) | ctx: 0x0057b502: mov dword ptr [ebp + 8], edi ; 0x0057b505: call 0x69570e ; 0x0057b50a: cmp eax, dword ptr [esi] ; 0x0057b50c: je 0x57b513
  - 0x0057b50c: je -> 0x0057b50e (jcc_false) | ctx: 0x0057b502: mov dword ptr [ebp + 8], edi ; 0x0057b505: call 0x69570e ; 0x0057b50a: cmp eax, dword ptr [esi] ; 0x0057b50c: je 0x57b513
  - 0x0057b517: je -> 0x0057b522 (jcc_true) | ctx: 0x0057b513: mov eax, dword ptr [esi] ; 0x0057b515: cmp eax, dword ptr [esi] ; 0x0057b517: je 0x57b522
  - 0x0057b517: je -> 0x0057b519 (jcc_false) | ctx: 0x0057b513: mov eax, dword ptr [esi] ; 0x0057b515: cmp eax, dword ptr [esi] ; 0x0057b517: je 0x57b522
  - 0x0057b511: jge -> 0x0057b515 (jcc_true) | ctx: 0x0057b50e: cmp edi, dword ptr [eax + 0x10] ; 0x0057b511: jge 0x57b515
  - 0x0057b511: jge -> 0x0057b513 (jcc_false) | ctx: 0x0057b50e: cmp edi, dword ptr [eax + 0x10] ; 0x0057b511: jge 0x57b515
  - 0x0057b517: je -> 0x0057b522 (jcc_true) | ctx: 0x0057b515: cmp eax, dword ptr [esi] ; 0x0057b517: je 0x57b522
  - 0x0057b517: je -> 0x0057b519 (jcc_false) | ctx: 0x0057b515: cmp eax, dword ptr [esi] ; 0x0057b517: je 0x57b522

### 0x0057b556
- blocks=1, insns=19, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0057b569)
- branch points:
  - none

### 0x0057fd44
- blocks=8, insns=30, edges=12, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0057fd4d)
- branch points:
  - 0x0057fd5a: jne -> 0x0057fd62 (jcc_true) | ctx: 0x0057fd52: mov ecx, dword ptr [ebp + 8] ; 0x0057fd55: add esp, 0xc ; 0x0057fd58: test ecx, ecx ; 0x0057fd5a: jne 0x57fd62
  - 0x0057fd5a: jne -> 0x0057fd5c (jcc_false) | ctx: 0x0057fd52: mov ecx, dword ptr [ebp + 8] ; 0x0057fd55: add esp, 0xc ; 0x0057fd58: test ecx, ecx ; 0x0057fd5a: jne 0x57fd62
  - 0x0057fd67: je -> 0x0057fd6b (jcc_true) | ctx: 0x0057fd62: mov edx, dword ptr [ebp + 0xc] ; 0x0057fd65: test eax, eax ; 0x0057fd67: je 0x57fd6b
  - 0x0057fd67: je -> 0x0057fd69 (jcc_false) | ctx: 0x0057fd62: mov edx, dword ptr [ebp + 0xc] ; 0x0057fd65: test eax, eax ; 0x0057fd67: je 0x57fd6b
  - 0x0057fd60: jmp -> 0x0057fd65 (jmp) | ctx: 0x0057fd5c: mov ecx, eax ; 0x0057fd5e: mov edx, eax ; 0x0057fd60: jmp 0x57fd65
  - 0x0057fd70: je -> 0x0057fd74 (jcc_true) | ctx: 0x0057fd6b: lea ecx, [eax + 4] ; 0x0057fd6e: test ecx, ecx ; 0x0057fd70: je 0x57fd74
  - 0x0057fd70: je -> 0x0057fd72 (jcc_false) | ctx: 0x0057fd6b: lea ecx, [eax + 4] ; 0x0057fd6e: test ecx, ecx ; 0x0057fd70: je 0x57fd74
  - 0x0057fd70: je -> 0x0057fd74 (jcc_true) | ctx: 0x0057fd69: mov dword ptr [eax], ecx ; 0x0057fd6b: lea ecx, [eax + 4] ; 0x0057fd6e: test ecx, ecx ; 0x0057fd70: je 0x57fd74
  - 0x0057fd70: je -> 0x0057fd72 (jcc_false) | ctx: 0x0057fd69: mov dword ptr [eax], ecx ; 0x0057fd6b: lea ecx, [eax + 4] ; 0x0057fd6e: test ecx, ecx ; 0x0057fd70: je 0x57fd74
  - 0x0057fd67: je -> 0x0057fd6b (jcc_true) | ctx: 0x0057fd65: test eax, eax ; 0x0057fd67: je 0x57fd6b
  - 0x0057fd67: je -> 0x0057fd69 (jcc_false) | ctx: 0x0057fd65: test eax, eax ; 0x0057fd67: je 0x57fd6b

### 0x0057fd87
- blocks=7, insns=50, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005769ed at 0x0057fd9c)
- branch points:
  - 0x0057fd8e: jne -> 0x0057fdd5 (jcc_true) | ctx: 0x0057fd88: mov edi, ecx ; 0x0057fd8a: mov eax, dword ptr [edi] ; 0x0057fd8c: cmp esi, dword ptr [eax] ; 0x0057fd8e: jne 0x57fdd5
  - 0x0057fd8e: jne -> 0x0057fd90 (jcc_false) | ctx: 0x0057fd88: mov edi, ecx ; 0x0057fd8a: mov eax, dword ptr [edi] ; 0x0057fd8c: cmp esi, dword ptr [eax] ; 0x0057fd8e: jne 0x57fdd5
  - 0x0057fdd8: jne -> 0x0057fdbe (jcc_true) | ctx: 0x0057fdd5: cmp esi, dword ptr [ebp + 0x10] ; 0x0057fdd8: jne 0x57fdbe
  - 0x0057fdd8: jne -> 0x0057fdda (jcc_false) | ctx: 0x0057fdd5: cmp esi, dword ptr [ebp + 0x10] ; 0x0057fdd8: jne 0x57fdbe
  - 0x0057fd93: jne -> 0x0057fdd5 (jcc_true) | ctx: 0x0057fd90: cmp dword ptr [ebp + 0x10], eax ; 0x0057fd93: jne 0x57fdd5
  - 0x0057fd93: jne -> 0x0057fd95 (jcc_false) | ctx: 0x0057fd90: cmp dword ptr [ebp + 0x10], eax ; 0x0057fd93: jne 0x57fdd5
  - 0x0057fdd8: jne -> 0x0057fdbe (jcc_true) | ctx: 0x0057fdcd: call 0x576b04 ; 0x0057fdd2: mov esi, dword ptr [ebp + 0xc] ; 0x0057fdd5: cmp esi, dword ptr [ebp + 0x10] ; 0x0057fdd8: jne 0x57fdbe
  - 0x0057fdd8: jne -> 0x0057fdda (jcc_false) | ctx: 0x0057fdcd: call 0x576b04 ; 0x0057fdd2: mov esi, dword ptr [ebp + 0xc] ; 0x0057fdd5: cmp esi, dword ptr [ebp + 0x10] ; 0x0057fdd8: jne 0x57fdbe
  - 0x0057fdbc: jmp -> 0x0057fddf (jmp) | ctx: 0x0057fdb5: mov ecx, dword ptr [eax] ; 0x0057fdb7: mov eax, dword ptr [ebp + 8] ; 0x0057fdba: mov dword ptr [eax], ecx ; 0x0057fdbc: jmp 0x57fddf

### 0x0057ff1d
- blocks=3, insns=21, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00580fd5 at 0x0057ff27)
- branch points:
  - 0x0057ff31: je -> 0x0057ff3d (jcc_true) | ctx: 0x0057ff27: call 0x580fd5 ; 0x0057ff2c: lea edi, [eax + 8] ; 0x0057ff2f: test edi, edi ; 0x0057ff31: je 0x57ff3d
  - 0x0057ff31: je -> 0x0057ff33 (jcc_false) | ctx: 0x0057ff27: call 0x580fd5 ; 0x0057ff2c: lea edi, [eax + 8] ; 0x0057ff2f: test edi, edi ; 0x0057ff31: je 0x57ff3d

### 0x0058012c
- blocks=9, insns=155, edges=24, jcc=7, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00580fd5 at 0x0058013b)
  - caller_of_anchor_path: depth 2 (calls 0x00580fd5 at 0x00580154)
- branch points:
  - 0x005801ef: jns -> 0x005801f6 (jcc_true) | ctx: 0x005801e4: mov ebx, ecx ; 0x005801e6: mov dword ptr [ebp + 0x10], ecx ; 0x005801e9: and ebx, 0x80000003 ; 0x005801ef: jns 0x5801f6
  - 0x005801ef: jns -> 0x005801f1 (jcc_false) | ctx: 0x005801e4: mov ebx, ecx ; 0x005801e6: mov dword ptr [ebp + 0x10], ecx ; 0x005801e9: and ebx, 0x80000003 ; 0x005801ef: jns 0x5801f6
  - 0x005801fe: je -> 0x0058023e (jcc_true) | ctx: 0x005801f6: mov edx, dword ptr [ebp + ebx*4 - 0x24] ; 0x005801fa: cmp dword ptr [ebp + eax*4 - 0x24], edx ; 0x005801fe: je 0x58023e
  - 0x005801fe: je -> 0x00580200 (jcc_false) | ctx: 0x005801f6: mov edx, dword ptr [ebp + ebx*4 - 0x24] ; 0x005801fa: cmp dword ptr [ebp + eax*4 - 0x24], edx ; 0x005801fe: je 0x58023e
  - 0x005801fe: je -> 0x0058023e (jcc_true) | ctx: 0x005801f5: inc ebx ; 0x005801f6: mov edx, dword ptr [ebp + ebx*4 - 0x24] ; 0x005801fa: cmp dword ptr [ebp + eax*4 - 0x24], edx ; 0x005801fe: je 0x58023e
  - 0x005801fe: je -> 0x00580200 (jcc_false) | ctx: 0x005801f5: inc ebx ; 0x005801f6: mov edx, dword ptr [ebp + ebx*4 - 0x24] ; 0x005801fa: cmp dword ptr [ebp + eax*4 - 0x24], edx ; 0x005801fe: je 0x58023e
  - 0x00580243: jl -> 0x005801e1 (jcc_true) | ctx: 0x0058023e: mov eax, ecx ; 0x00580240: cmp eax, 4 ; 0x00580243: jl 0x5801e1
  - 0x00580243: jl -> 0x00580245 (jcc_false) | ctx: 0x0058023e: mov eax, ecx ; 0x00580240: cmp eax, 4 ; 0x00580243: jl 0x5801e1
  - 0x00580243: jl -> 0x005801e1 (jcc_true) | ctx: 0x0058023b: mov ecx, dword ptr [ebp + 0x10] ; 0x0058023e: mov eax, ecx ; 0x00580240: cmp eax, 4 ; 0x00580243: jl 0x5801e1
  - 0x00580243: jl -> 0x00580245 (jcc_false) | ctx: 0x0058023b: mov ecx, dword ptr [ebp + 0x10] ; 0x0058023e: mov eax, ecx ; 0x00580240: cmp eax, 4 ; 0x00580243: jl 0x5801e1
  - 0x005801ef: jns -> 0x005801f6 (jcc_true) | ctx: 0x005801e4: mov ebx, ecx ; 0x005801e6: mov dword ptr [ebp + 0x10], ecx ; 0x005801e9: and ebx, 0x80000003 ; 0x005801ef: jns 0x5801f6
  - 0x005801ef: jns -> 0x005801f1 (jcc_false) | ctx: 0x005801e4: mov ebx, ecx ; 0x005801e6: mov dword ptr [ebp + 0x10], ecx ; 0x005801e9: and ebx, 0x80000003 ; 0x005801ef: jns 0x5801f6
  - 0x00580267: je -> 0x00580273 (jcc_true) | ctx: 0x0058025d: push eax ; 0x0058025e: call 0x580010 ; 0x00580263: cmp dword ptr [edi + 4], 0 ; 0x00580267: je 0x580273
  - 0x00580267: je -> 0x00580269 (jcc_false) | ctx: 0x0058025d: push eax ; 0x0058025e: call 0x580010 ; 0x00580263: cmp dword ptr [edi + 4], 0 ; 0x00580267: je 0x580273

### 0x005804ab
- blocks=1, insns=14, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCBlockingStatusPredicate@EGL@@ slot 1 (target 0x005804ab, vtable 0x00bc72e0)
- branch points:
  - none

### 0x005804d4
- blocks=1, insns=13, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCUnblockedAreasPredicate@EGL@@ slot 1 (target 0x005804d4, vtable 0x00bc8db4)
- branch points:
  - none

### 0x005804f4
- blocks=11, insns=76, edges=22, jcc=9, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCUnblockedBuildingAreasPredicate@EGL@@ slot 1 (target 0x005804f4, vtable 0x00bc8dc0)
  - caller_of_anchor_path: depth 1 (calls 0x005804d4 at 0x00580550)
  - caller_of_anchor_path: depth 1 (calls 0x005804f4 at 0x00580550)
- branch points:
  - 0x00580511: jg -> 0x00580585 (jcc_true) | ctx: 0x0058050a: mov bl, 1 ; 0x0058050c: mov dword ptr [ebp - 0xc], eax ; 0x0058050f: cmp esi, eax ; 0x00580511: jg 0x580585
  - 0x00580511: jg -> 0x00580513 (jcc_false) | ctx: 0x0058050a: mov bl, 1 ; 0x0058050c: mov dword ptr [ebp - 0xc], eax ; 0x0058050f: cmp esi, eax ; 0x00580511: jg 0x580585
  - 0x0058051e: je -> 0x0058057a (jcc_true) | ctx: 0x00580516: lea edi, [eax - 1] ; 0x00580519: mov dword ptr [ebp - 0x17], edi ; 0x0058051c: test bl, bl ; 0x0058051e: je 0x58057a
  - 0x0058051e: je -> 0x00580520 (jcc_false) | ctx: 0x00580516: lea edi, [eax - 1] ; 0x00580519: mov dword ptr [ebp - 0x17], edi ; 0x0058051c: test bl, bl ; 0x0058051e: je 0x58057a
  - 0x00580583: jne -> 0x0058050f (jcc_true) | ctx: 0x0058057d: inc esi ; 0x0058057e: mov dword ptr [ebp - 0x13], esi ; 0x00580581: test bl, bl ; 0x00580583: jne 0x58050f
  - 0x00580583: jne -> 0x00580585 (jcc_false) | ctx: 0x0058057d: inc esi ; 0x0058057e: mov dword ptr [ebp - 0x13], esi ; 0x00580581: test bl, bl ; 0x00580583: jne 0x58050f
  - 0x00580526: jg -> 0x0058057a (jcc_true) | ctx: 0x00580520: inc eax ; 0x00580521: mov dword ptr [ebp - 8], eax ; 0x00580524: cmp edi, eax ; 0x00580526: jg 0x58057a
  - 0x00580526: jg -> 0x00580528 (jcc_false) | ctx: 0x00580520: inc eax ; 0x00580521: mov dword ptr [ebp - 8], eax ; 0x00580524: cmp edi, eax ; 0x00580526: jg 0x58057a
  - 0x00580511: jg -> 0x00580585 (jcc_true) | ctx: 0x0058050f: cmp esi, eax ; 0x00580511: jg 0x580585
  - 0x00580511: jg -> 0x00580513 (jcc_false) | ctx: 0x0058050f: cmp esi, eax ; 0x00580511: jg 0x580585
  - 0x00580548: je -> 0x0058054e (jcc_true) | ctx: 0x0058053f: mov ecx, dword ptr [ebp - 4] ; 0x00580542: add esp, 0x10 ; 0x00580545: cmp eax, dword ptr [ecx + 0x28] ; 0x00580548: je 0x58054e
  - 0x00580548: je -> 0x0058054a (jcc_false) | ctx: 0x0058053f: mov ecx, dword ptr [ebp - 4] ; 0x00580542: add esp, 0x10 ; 0x00580545: cmp eax, dword ptr [ecx + 0x28] ; 0x00580548: je 0x58054e
  - 0x00580578: jne -> 0x00580524 (jcc_true) | ctx: 0x00580572: inc edi ; 0x00580573: mov dword ptr [ebp - 0x17], edi ; 0x00580576: test bl, bl ; 0x00580578: jne 0x580524
  - 0x00580578: jne -> 0x0058057a (jcc_false) | ctx: 0x00580572: inc edi ; 0x00580573: mov dword ptr [ebp - 0x17], edi ; 0x00580576: test bl, bl ; 0x00580578: jne 0x580524
  - 0x0058054c: jmp -> 0x0058056f (jmp) | ctx: 0x0058054a: mov bl, byte ptr [eax] ; 0x0058054c: jmp 0x58056f
  - 0x00580526: jg -> 0x0058057a (jcc_true) | ctx: 0x00580524: cmp edi, eax ; 0x00580526: jg 0x58057a
  - 0x00580526: jg -> 0x00580528 (jcc_false) | ctx: 0x00580524: cmp edi, eax ; 0x00580526: jg 0x58057a
  - 0x00580578: jne -> 0x00580524 (jcc_true) | ctx: 0x00580572: inc edi ; 0x00580573: mov dword ptr [ebp - 0x17], edi ; 0x00580576: test bl, bl ; 0x00580578: jne 0x580524
  - 0x00580578: jne -> 0x0058057a (jcc_false) | ctx: 0x00580572: inc edi ; 0x00580573: mov dword ptr [ebp - 0x17], edi ; 0x00580576: test bl, bl ; 0x00580578: jne 0x580524

### 0x00580590
- blocks=4, insns=32, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCUnblockedInLargeSectorPredicate@EGL@@ slot 1 (target 0x00580590, vtable 0x00bc8da8)
  - caller_of_anchor_path: depth 1 (calls 0x005804ab at 0x0058059f)
- branch points:
  - 0x005805a6: je -> 0x005805c9 (jcc_true) | ctx: 0x0058059c: push dword ptr [ebp + 8] ; 0x0058059f: call 0x5804ab ; 0x005805a4: test al, al ; 0x005805a6: je 0x5805c9
  - 0x005805a6: je -> 0x005805a8 (jcc_false) | ctx: 0x0058059c: push dword ptr [ebp + 8] ; 0x0058059f: call 0x5804ab ; 0x005805a4: test al, al ; 0x005805a6: je 0x5805c9
  - 0x005805b8: je -> 0x005805c9 (jcc_true) | ctx: 0x005805ae: push dword ptr [ebp + 8] ; 0x005805b1: call 0x56ab1c ; 0x005805b6: test eax, eax ; 0x005805b8: je 0x5805c9
  - 0x005805b8: je -> 0x005805ba (jcc_false) | ctx: 0x005805ae: push dword ptr [ebp + 8] ; 0x005805b1: call 0x56ab1c ; 0x005805b6: test eax, eax ; 0x005805b8: je 0x5805c9

### 0x005805d1
- blocks=5, insns=25, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCUnblockedInSectorPredicate@EGL@@ slot 1 (target 0x005805d1, vtable 0x00bc8d9c)
  - caller_of_anchor_path: depth 1 (calls 0x005804ab at 0x005805dd)
- branch points:
  - 0x005805e4: je -> 0x005805fe (jcc_true) | ctx: 0x005805da: push dword ptr [ebp + 8] ; 0x005805dd: call 0x5804ab ; 0x005805e2: test al, al ; 0x005805e4: je 0x5805fe
  - 0x005805e4: je -> 0x005805e6 (jcc_false) | ctx: 0x005805da: push dword ptr [ebp + 8] ; 0x005805dd: call 0x5804ab ; 0x005805e2: test al, al ; 0x005805e4: je 0x5805fe
  - 0x005805f7: jne -> 0x005805fe (jcc_true) | ctx: 0x005805ec: push dword ptr [ebp + 8] ; 0x005805ef: call 0x56ab1c ; 0x005805f4: cmp eax, dword ptr [esi + 0xc] ; 0x005805f7: jne 0x5805fe
  - 0x005805f7: jne -> 0x005805f9 (jcc_false) | ctx: 0x005805ec: push dword ptr [ebp + 8] ; 0x005805ef: call 0x56ab1c ; 0x005805f4: cmp eax, dword ptr [esi + 0xc] ; 0x005805f7: jne 0x5805fe
  - 0x005805fc: jmp -> 0x00580600 (jmp) | ctx: 0x005805f9: xor eax, eax ; 0x005805fb: inc eax ; 0x005805fc: jmp 0x580600

### 0x00580627
- blocks=1, insns=2, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCUnblockedAreasPredicate@EGL@@ slot 0 (target 0x00580627, vtable 0x00bc8db4)
- branch points:
  - none

### 0x0058062a
- blocks=3, insns=18, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x005804ab at 0x0058062d)
- branch points:
  - 0x00580636: je -> 0x00580642 (jcc_true) | ctx: 0x0058062b: mov esi, ecx ; 0x0058062d: call 0x580492 ; 0x00580632: test byte ptr [ebp + 8], 1 ; 0x00580636: je 0x580642
  - 0x00580636: je -> 0x00580638 (jcc_false) | ctx: 0x0058062b: mov esi, ecx ; 0x0058062d: call 0x580492 ; 0x00580632: test byte ptr [ebp + 8], 1 ; 0x00580636: je 0x580642

### 0x00580649
- blocks=1, insns=2, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCUnblockedBuildingAreasPredicate@EGL@@ slot 0 (target 0x00580649, vtable 0x00bc8dc0)
- branch points:
  - none

### 0x0058064c
- blocks=3, insns=21, edges=5, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x005804ab at 0x00580659)
- branch points:
  - 0x00580662: je -> 0x0058066e (jcc_true) | ctx: 0x00580657: mov ecx, esi ; 0x00580659: call 0x580492 ; 0x0058065e: test byte ptr [ebp + 8], 1 ; 0x00580662: je 0x58066e
  - 0x00580662: je -> 0x00580664 (jcc_false) | ctx: 0x00580657: mov ecx, esi ; 0x00580659: call 0x580492 ; 0x0058065e: test byte ptr [ebp + 8], 1 ; 0x00580662: je 0x58066e

### 0x00580675
- blocks=1, insns=3, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCUnblockedInSectorPredicate@EGL@@ slot 0 (target 0x00580675, vtable 0x00bc8d9c)
  - rtti_vtable_method: .?AVCUnblockedInLargeSectorPredicate@EGL@@ slot 0 (target 0x00580675, vtable 0x00bc8da8)
  - rtti_vtable_method: .?AVCPotentialCampSitePredicate@GGL@@ slot 0 (target 0x00580675, vtable 0x00bd8fac)
- branch points:
  - none

### 0x00580fd5
- blocks=8, insns=30, edges=12, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00580fde)
- branch points:
  - 0x00580feb: jne -> 0x00580ff3 (jcc_true) | ctx: 0x00580fe3: mov ecx, dword ptr [ebp + 8] ; 0x00580fe6: add esp, 0xc ; 0x00580fe9: test ecx, ecx ; 0x00580feb: jne 0x580ff3
  - 0x00580feb: jne -> 0x00580fed (jcc_false) | ctx: 0x00580fe3: mov ecx, dword ptr [ebp + 8] ; 0x00580fe6: add esp, 0xc ; 0x00580fe9: test ecx, ecx ; 0x00580feb: jne 0x580ff3
  - 0x00580ff8: je -> 0x00580ffc (jcc_true) | ctx: 0x00580ff3: mov edx, dword ptr [ebp + 0xc] ; 0x00580ff6: test eax, eax ; 0x00580ff8: je 0x580ffc
  - 0x00580ff8: je -> 0x00580ffa (jcc_false) | ctx: 0x00580ff3: mov edx, dword ptr [ebp + 0xc] ; 0x00580ff6: test eax, eax ; 0x00580ff8: je 0x580ffc
  - 0x00580ff1: jmp -> 0x00580ff6 (jmp) | ctx: 0x00580fed: mov ecx, eax ; 0x00580fef: mov edx, eax ; 0x00580ff1: jmp 0x580ff6
  - 0x00581001: je -> 0x00581005 (jcc_true) | ctx: 0x00580ffc: lea ecx, [eax + 4] ; 0x00580fff: test ecx, ecx ; 0x00581001: je 0x581005
  - 0x00581001: je -> 0x00581003 (jcc_false) | ctx: 0x00580ffc: lea ecx, [eax + 4] ; 0x00580fff: test ecx, ecx ; 0x00581001: je 0x581005
  - 0x00581001: je -> 0x00581005 (jcc_true) | ctx: 0x00580ffa: mov dword ptr [eax], ecx ; 0x00580ffc: lea ecx, [eax + 4] ; 0x00580fff: test ecx, ecx ; 0x00581001: je 0x581005
  - 0x00581001: je -> 0x00581003 (jcc_false) | ctx: 0x00580ffa: mov dword ptr [eax], ecx ; 0x00580ffc: lea ecx, [eax + 4] ; 0x00580fff: test ecx, ecx ; 0x00581001: je 0x581005
  - 0x00580ff8: je -> 0x00580ffc (jcc_true) | ctx: 0x00580ff6: test eax, eax ; 0x00580ff8: je 0x580ffc
  - 0x00580ff8: je -> 0x00580ffa (jcc_false) | ctx: 0x00580ff6: test eax, eax ; 0x00580ff8: je 0x580ffc

### 0x00581065
- blocks=3, insns=61, edges=5, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00581077)
- branch points:
  - 0x0058109d: je -> 0x005810b3 (jcc_true) | ctx: 0x00581095: idiv ecx ; 0x00581097: cmp dword ptr [esi], 0 ; 0x0058109a: mov dword ptr [ebp + 8], eax ; 0x0058109d: je 0x5810b3
  - 0x0058109d: je -> 0x0058109f (jcc_false) | ctx: 0x00581095: idiv ecx ; 0x00581097: cmp dword ptr [esi], 0 ; 0x0058109a: mov dword ptr [ebp + 8], eax ; 0x0058109d: je 0x5810b3

### 0x005810d1
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00581065 at 0x00581109)
- branch points:
  - 0x005810e8: jae -> 0x0058110e (jcc_true) | ctx: 0x005810e1: idiv ebx ; 0x005810e3: mov edi, dword ptr [ebp + 8] ; 0x005810e6: cmp eax, edi ; 0x005810e8: jae 0x58110e
  - 0x005810e8: jae -> 0x005810ea (jcc_false) | ctx: 0x005810e1: idiv ebx ; 0x005810e3: mov edi, dword ptr [ebp + 8] ; 0x005810e6: cmp eax, edi ; 0x005810e8: jae 0x58110e
  - 0x005810fa: jb -> 0x00581115 (jcc_true) | ctx: 0x005810f4: idiv ebx ; 0x005810f6: sub ecx, eax ; 0x005810f8: cmp ecx, edi ; 0x005810fa: jb 0x581115
  - 0x005810fa: jb -> 0x005810fc (jcc_false) | ctx: 0x005810f4: idiv ebx ; 0x005810f6: sub ecx, eax ; 0x005810f8: cmp ecx, edi ; 0x005810fa: jb 0x581115

### 0x00581d66
- blocks=9, insns=88, edges=20, jcc=6, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00580fd5 at 0x00581da1)
- branch points:
  - 0x00581d74: je -> 0x00581d80 (jcc_true) | ctx: 0x00581d70: push esi ; 0x00581d71: push edi ; 0x00581d72: mov esi, ecx ; 0x00581d74: je 0x581d80
  - 0x00581d74: je -> 0x00581d76 (jcc_false) | ctx: 0x00581d70: push esi ; 0x00581d71: push edi ; 0x00581d72: mov esi, ecx ; 0x00581d74: je 0x581d80
  - 0x00581d8d: jle -> 0x00581db6 (jcc_true) | ctx: 0x00581d85: mov ebx, dword ptr [eax] ; 0x00581d87: mov byte ptr [ebp - 1], 7 ; 0x00581d8b: test ebx, ebx ; 0x00581d8d: jle 0x581db6
  - 0x00581d8d: jle -> 0x00581d8f (jcc_false) | ctx: 0x00581d85: mov ebx, dword ptr [eax] ; 0x00581d87: mov byte ptr [ebp - 1], 7 ; 0x00581d8b: test ebx, ebx ; 0x00581d8d: jle 0x581db6
  - 0x00581d7e: jmp -> 0x00581db6 (jmp) | ctx: 0x00581d76: mov ecx, dword ptr [esi + 4] ; 0x00581d79: call 0x580fa1 ; 0x00581d7e: jmp 0x581db6
  - 0x00581de5: je -> 0x00581df4 (jcc_true) | ctx: 0x00581dda: push 0 ; 0x00581ddc: call 0x58196e ; 0x00581de1: cmp byte ptr [ebp + 8], 0 ; 0x00581de5: je 0x581df4
  - 0x00581de5: je -> 0x00581de7 (jcc_false) | ctx: 0x00581dda: push 0 ; 0x00581ddc: call 0x58196e ; 0x00581de1: cmp byte ptr [ebp + 8], 0 ; 0x00581de5: je 0x581df4
  - 0x00581d96: jle -> 0x00581db1 (jcc_true) | ctx: 0x00581d8f: xor eax, eax ; 0x00581d91: mov dword ptr [ebp - 8], eax ; 0x00581d94: test ebx, ebx ; 0x00581d96: jle 0x581db1
  - 0x00581d96: jle -> 0x00581d98 (jcc_false) | ctx: 0x00581d8f: xor eax, eax ; 0x00581d91: mov dword ptr [ebp - 8], eax ; 0x00581d94: test ebx, ebx ; 0x00581d96: jle 0x581db1
  - 0x00581db4: jl -> 0x00581d8f (jcc_true) | ctx: 0x00581db1: inc edi ; 0x00581db2: cmp edi, ebx ; 0x00581db4: jl 0x581d8f
  - 0x00581db4: jl -> 0x00581db6 (jcc_false) | ctx: 0x00581db1: inc edi ; 0x00581db2: cmp edi, ebx ; 0x00581db4: jl 0x581d8f
  - 0x00581daf: jl -> 0x00581d98 (jcc_true) | ctx: 0x00581da9: inc eax ; 0x00581daa: mov dword ptr [ebp - 8], eax ; 0x00581dad: cmp eax, ebx ; 0x00581daf: jl 0x581d98
  - 0x00581daf: jl -> 0x00581db1 (jcc_false) | ctx: 0x00581da9: inc eax ; 0x00581daa: mov dword ptr [ebp - 8], eax ; 0x00581dad: cmp eax, ebx ; 0x00581daf: jl 0x581d98

### 0x0058288e
- blocks=16, insns=106, edges=34, jcc=14, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00580fd5 at 0x005828fd)
  - caller_of_anchor_path: depth 2 (calls 0x00580fd5 at 0x0058290f)
- branch points:
  - 0x005828b8: jge -> 0x00582928 (jcc_true) | ctx: 0x005828b0: mov dword ptr [ebp - 8], ecx ; 0x005828b3: mov dword ptr [ebp - 0x10], eax ; 0x005828b6: cmp esi, eax ; 0x005828b8: jge 0x582928
  - 0x005828b8: jge -> 0x005828ba (jcc_false) | ctx: 0x005828b0: mov dword ptr [ebp - 8], ecx ; 0x005828b3: mov dword ptr [ebp - 0x10], eax ; 0x005828b6: cmp esi, eax ; 0x005828b8: jge 0x582928
  - 0x005828bf: jge -> 0x00582922 (jcc_true) | ctx: 0x005828ba: push edi ; 0x005828bb: mov edi, ebx ; 0x005828bd: cmp ebx, ecx ; 0x005828bf: jge 0x582922
  - 0x005828bf: jge -> 0x005828c1 (jcc_false) | ctx: 0x005828ba: push edi ; 0x005828bb: mov edi, ebx ; 0x005828bd: cmp ebx, ecx ; 0x005828bf: jge 0x582922
  - 0x00582925: jl -> 0x005828bb (jcc_true) | ctx: 0x00582922: inc esi ; 0x00582923: cmp esi, eax ; 0x00582925: jl 0x5828bb
  - 0x00582925: jl -> 0x00582927 (jcc_false) | ctx: 0x00582922: inc esi ; 0x00582923: cmp esi, eax ; 0x00582925: jl 0x5828bb
  - 0x005828c6: jle -> 0x00582917 (jcc_true) | ctx: 0x005828c1: mov ebx, dword ptr [ebp - 4] ; 0x005828c4: test edi, edi ; 0x005828c6: jle 0x582917
  - 0x005828c6: jle -> 0x005828c8 (jcc_false) | ctx: 0x005828c1: mov ebx, dword ptr [ebp - 4] ; 0x005828c4: test edi, edi ; 0x005828c6: jle 0x582917
  - 0x005828bf: jge -> 0x00582922 (jcc_true) | ctx: 0x005828bb: mov edi, ebx ; 0x005828bd: cmp ebx, ecx ; 0x005828bf: jge 0x582922
  - 0x005828bf: jge -> 0x005828c1 (jcc_false) | ctx: 0x005828bb: mov edi, ebx ; 0x005828bd: cmp ebx, ecx ; 0x005828bf: jge 0x582922
  - 0x0058291a: jl -> 0x005828c4 (jcc_true) | ctx: 0x00582917: inc edi ; 0x00582918: cmp edi, ecx ; 0x0058291a: jl 0x5828c4
  - 0x0058291a: jl -> 0x0058291c (jcc_false) | ctx: 0x00582917: inc edi ; 0x00582918: cmp edi, ecx ; 0x0058291a: jl 0x5828c4
  - 0x005828ca: jle -> 0x00582917 (jcc_true) | ctx: 0x005828c8: test esi, esi ; 0x005828ca: jle 0x582917
  - 0x005828ca: jle -> 0x005828cc (jcc_false) | ctx: 0x005828c8: test esi, esi ; 0x005828ca: jle 0x582917
  - 0x005828c6: jle -> 0x00582917 (jcc_true) | ctx: 0x005828c4: test edi, edi ; 0x005828c6: jle 0x582917
  - 0x005828c6: jle -> 0x005828c8 (jcc_false) | ctx: 0x005828c4: test edi, edi ; 0x005828c6: jle 0x582917
  - 0x00582925: jl -> 0x005828bb (jcc_true) | ctx: 0x0058291f: mov eax, dword ptr [ebp - 0x10] ; 0x00582922: inc esi ; 0x00582923: cmp esi, eax ; 0x00582925: jl 0x5828bb
  - 0x00582925: jl -> 0x00582927 (jcc_false) | ctx: 0x0058291f: mov eax, dword ptr [ebp - 0x10] ; 0x00582922: inc esi ; 0x00582923: cmp esi, eax ; 0x00582925: jl 0x5828bb
  - 0x005828d4: jge -> 0x00582917 (jcc_true) | ctx: 0x005828cc: mov eax, dword ptr [0xf4955c] ; 0x005828d1: dec eax ; 0x005828d2: cmp edi, eax ; 0x005828d4: jge 0x582917
  - 0x005828d4: jge -> 0x005828d6 (jcc_false) | ctx: 0x005828cc: mov eax, dword ptr [0xf4955c] ; 0x005828d1: dec eax ; 0x005828d2: cmp edi, eax ; 0x005828d4: jge 0x582917
  - 0x005828d8: jge -> 0x00582917 (jcc_true) | ctx: 0x005828d6: cmp esi, eax ; 0x005828d8: jge 0x582917
  - 0x005828d8: jge -> 0x005828da (jcc_false) | ctx: 0x005828d6: cmp esi, eax ; 0x005828d8: jge 0x582917
  - 0x005828e4: je -> 0x005828f0 (jcc_true) | ctx: 0x005828dd: mov eax, dword ptr [ecx] ; 0x005828df: call dword ptr [eax + 0x38] ; 0x005828e2: test al, al ; 0x005828e4: je 0x5828f0
  - 0x005828e4: je -> 0x005828e6 (jcc_false) | ctx: 0x005828dd: mov eax, dword ptr [ecx] ; 0x005828df: call dword ptr [eax + 0x38] ; 0x005828e2: test al, al ; 0x005828e4: je 0x5828f0
  - 0x0058291a: jl -> 0x005828c4 (jcc_true) | ctx: 0x00582914: mov ecx, dword ptr [ebp - 8] ; 0x00582917: inc edi ; 0x00582918: cmp edi, ecx ; 0x0058291a: jl 0x5828c4
  - 0x0058291a: jl -> 0x0058291c (jcc_false) | ctx: 0x00582914: mov ecx, dword ptr [ebp - 8] ; 0x00582917: inc edi ; 0x00582918: cmp edi, ecx ; 0x0058291a: jl 0x5828c4
  - 0x0058291a: jl -> 0x005828c4 (jcc_true) | ctx: 0x00582914: mov ecx, dword ptr [ebp - 8] ; 0x00582917: inc edi ; 0x00582918: cmp edi, ecx ; 0x0058291a: jl 0x5828c4
  - 0x0058291a: jl -> 0x0058291c (jcc_false) | ctx: 0x00582914: mov ecx, dword ptr [ebp - 8] ; 0x00582917: inc edi ; 0x00582918: cmp edi, ecx ; 0x0058291a: jl 0x5828c4

### 0x00582930
- blocks=4, insns=51, edges=10, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00580fd5 at 0x00582a1c)
  - caller_of_anchor_path: depth 2 (calls 0x00580fd5 at 0x00582a2e)
  - caller_of_anchor_path: depth 2 (calls 0x00580fd5 at 0x00582a40)
- branch points:
  - 0x00582942: je -> 0x005829a4 (jcc_true) | ctx: 0x00582939: mov esi, ecx ; 0x0058293b: call 0x58203e ; 0x00582940: test al, al ; 0x00582942: je 0x5829a4
  - 0x00582942: je -> 0x00582944 (jcc_false) | ctx: 0x00582939: mov esi, ecx ; 0x0058293b: call 0x58203e ; 0x00582940: test al, al ; 0x00582942: je 0x5829a4
  - 0x00582969: je -> 0x005829a4 (jcc_true) | ctx: 0x0058295f: push dword ptr [ebp - 8] ; 0x00582962: call 0x553c72 ; 0x00582967: test al, al ; 0x00582969: je 0x5829a4
  - 0x00582969: je -> 0x0058296b (jcc_false) | ctx: 0x0058295f: push dword ptr [ebp - 8] ; 0x00582962: call 0x553c72 ; 0x00582967: test al, al ; 0x00582969: je 0x5829a4

### 0x00585f60
- blocks=1, insns=8, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCPath@EGL@@ slot 3 (target 0x00585f60, vtable 0x00bc9218)
  - rtti_vtable_method: .?AVCPath@GGL@@ slot 3 (target 0x00585f60, vtable 0x00bdb29c)
- branch points:
  - none

### 0x00585f77
- blocks=1, insns=2, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCPath@EGL@@ slot 0 (target 0x00585f77, vtable 0x00bc9218)
- branch points:
  - none

### 0x00585f7a
- blocks=3, insns=18, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCPath@EGL@@ slot 1 (target 0x00585f99, vtable 0x00bc9218)
- branch points:
  - 0x00585f86: je -> 0x00585f92 (jcc_true) | ctx: 0x00585f7b: mov esi, ecx ; 0x00585f7d: call 0x5861f2 ; 0x00585f82: test byte ptr [ebp + 8], 1 ; 0x00585f86: je 0x585f92
  - 0x00585f86: je -> 0x00585f88 (jcc_false) | ctx: 0x00585f7b: mov esi, ecx ; 0x00585f7d: call 0x5861f2 ; 0x00585f82: test byte ptr [ebp + 8], 1 ; 0x00585f86: je 0x585f92

### 0x00586054
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0058680d at 0x00586068)
- branch points:
  - 0x00586059: jne -> 0x00586068 (jcc_true) | ctx: 0x00586054: push edi ; 0x00586055: mov edi, ecx ; 0x00586057: test esi, esi ; 0x00586059: jne 0x586068
  - 0x00586059: jne -> 0x0058605b (jcc_false) | ctx: 0x00586054: push edi ; 0x00586055: mov edi, ecx ; 0x00586057: test esi, esi ; 0x00586059: jne 0x586068

### 0x00586227
- blocks=1, insns=3, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCoarsePath@EGL@@ slot 0 (target 0x00586227, vtable 0x00bc9240)
- branch points:
  - none

### 0x0058680d
- blocks=4, insns=52, edges=9, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: WayPoints via `WayPoints` (string 0x00bc9228, xref 0x0058685b)
- branch points:
  - 0x0058682d: jg -> 0x00586838 (jcc_true) | ctx: 0x0058681f: mov ecx, dword ptr [eax + ecx*4] ; 0x00586822: mov eax, dword ptr [0xdf7b00] ; 0x00586827: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0058682d: jg 0x586838
  - 0x0058682d: jg -> 0x0058682f (jcc_false) | ctx: 0x0058681f: mov ecx, dword ptr [eax + ecx*4] ; 0x00586822: mov eax, dword ptr [0xdf7b00] ; 0x00586827: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0058682d: jg 0x586838
  - 0x0058684a: jne -> 0x0058682f (jcc_true) | ctx: 0x0058683d: call 0xab6ba9 ; 0x00586842: cmp dword ptr [0xdf7b00], -1 ; 0x00586849: pop ecx ; 0x0058684a: jne 0x58682f
  - 0x0058684a: jne -> 0x0058684c (jcc_false) | ctx: 0x0058683d: call 0xab6ba9 ; 0x00586842: cmp dword ptr [0xdf7b00], -1 ; 0x00586849: pop ecx ; 0x0058684a: jne 0x58682f
  - 0x005868c9: jmp -> 0x0058682f (jmp) | ctx: 0x005868c6: pop edi ; 0x005868c7: pop esi ; 0x005868c8: pop ebx ; 0x005868c9: jmp 0x58682f

### 0x00587cd5
- blocks=3, insns=22, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00588b31 at 0x00587cdf)
- branch points:
  - 0x00587ce9: je -> 0x00587cf4 (jcc_true) | ctx: 0x00587cdf: call 0x588b31 ; 0x00587ce4: lea edi, [eax + 8] ; 0x00587ce7: test edi, edi ; 0x00587ce9: je 0x587cf4
  - 0x00587ce9: je -> 0x00587ceb (jcc_false) | ctx: 0x00587cdf: call 0x588b31 ; 0x00587ce4: lea edi, [eax + 8] ; 0x00587ce7: test edi, edi ; 0x00587ce9: je 0x587cf4

### 0x00587eb7
- blocks=1, insns=18, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00588b31 at 0x00587eca)
- branch points:
  - none

### 0x00588b31
- blocks=8, insns=30, edges=12, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00588b3a)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00588b82)
- branch points:
  - 0x00588b47: jne -> 0x00588b4f (jcc_true) | ctx: 0x00588b3f: mov ecx, dword ptr [ebp + 8] ; 0x00588b42: add esp, 0xc ; 0x00588b45: test ecx, ecx ; 0x00588b47: jne 0x588b4f
  - 0x00588b47: jne -> 0x00588b49 (jcc_false) | ctx: 0x00588b3f: mov ecx, dword ptr [ebp + 8] ; 0x00588b42: add esp, 0xc ; 0x00588b45: test ecx, ecx ; 0x00588b47: jne 0x588b4f
  - 0x00588b54: je -> 0x00588b58 (jcc_true) | ctx: 0x00588b4f: mov edx, dword ptr [ebp + 0xc] ; 0x00588b52: test eax, eax ; 0x00588b54: je 0x588b58
  - 0x00588b54: je -> 0x00588b56 (jcc_false) | ctx: 0x00588b4f: mov edx, dword ptr [ebp + 0xc] ; 0x00588b52: test eax, eax ; 0x00588b54: je 0x588b58
  - 0x00588b4d: jmp -> 0x00588b52 (jmp) | ctx: 0x00588b49: mov ecx, eax ; 0x00588b4b: mov edx, eax ; 0x00588b4d: jmp 0x588b52
  - 0x00588b5d: je -> 0x00588b61 (jcc_true) | ctx: 0x00588b58: lea ecx, [eax + 4] ; 0x00588b5b: test ecx, ecx ; 0x00588b5d: je 0x588b61
  - 0x00588b5d: je -> 0x00588b5f (jcc_false) | ctx: 0x00588b58: lea ecx, [eax + 4] ; 0x00588b5b: test ecx, ecx ; 0x00588b5d: je 0x588b61
  - 0x00588b5d: je -> 0x00588b61 (jcc_true) | ctx: 0x00588b56: mov dword ptr [eax], ecx ; 0x00588b58: lea ecx, [eax + 4] ; 0x00588b5b: test ecx, ecx ; 0x00588b5d: je 0x588b61
  - 0x00588b5d: je -> 0x00588b5f (jcc_false) | ctx: 0x00588b56: mov dword ptr [eax], ecx ; 0x00588b58: lea ecx, [eax + 4] ; 0x00588b5b: test ecx, ecx ; 0x00588b5d: je 0x588b61
  - 0x00588b54: je -> 0x00588b58 (jcc_true) | ctx: 0x00588b52: test eax, eax ; 0x00588b54: je 0x588b58
  - 0x00588b54: je -> 0x00588b56 (jcc_false) | ctx: 0x00588b52: test eax, eax ; 0x00588b54: je 0x588b58

### 0x0058b20e
- blocks=1, insns=3, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehavior@GGL@@ slot 0 (target 0x0058b20e, vtable 0x00be1058)
- branch points:
  - none

### 0x0058e49d
- blocks=1, insns=23, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0058e4f0)
- branch points:
  - none

### 0x0059f799
- blocks=1, insns=20, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0059f7b6)
- branch points:
  - none

### 0x0059f950
- blocks=4, insns=55, edges=6, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0059f975)
- branch points:
  - 0x0059f999: je -> 0x0059f9aa (jcc_true) | ctx: 0x0059f990: mov dword ptr [ebp - 0x14], esi ; 0x0059f993: mov byte ptr [ebp - 4], 2 ; 0x0059f997: test esi, esi ; 0x0059f999: je 0x59f9aa
  - 0x0059f999: je -> 0x0059f99b (jcc_false) | ctx: 0x0059f990: mov dword ptr [ebp - 0x14], esi ; 0x0059f993: mov byte ptr [ebp - 4], 2 ; 0x0059f997: test esi, esi ; 0x0059f999: je 0x59f9aa
  - 0x0059f9a8: jmp -> 0x0059f9ac (jmp) | ctx: 0x0059f99b: mov ecx, esi ; 0x0059f99d: call 0x52f85a ; 0x0059f9a2: mov dword ptr [esi], 0xbc3144 ; 0x0059f9a8: jmp 0x59f9ac

### 0x0059ffc0
- blocks=7, insns=44, edges=8, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00564601 at 0x005a0019)
- branch points:
  - 0x0059ffe2: je -> 0x0059ffe6 (jcc_true) | ctx: 0x0059ffd1: mov dword ptr fs:[0], esp ; 0x0059ffd8: sub esp, 0xc ; 0x0059ffdb: cmp dword ptr [0xf4ace4], 0 ; 0x0059ffe2: je 0x59ffe6
  - 0x0059ffe2: je -> 0x0059ffe4 (jcc_false) | ctx: 0x0059ffd1: mov dword ptr fs:[0], esp ; 0x0059ffd8: sub esp, 0xc ; 0x0059ffdb: cmp dword ptr [0xf4ace4], 0 ; 0x0059ffe2: je 0x59ffe6
  - 0x0059fffe: je -> 0x005a000d (jcc_true) | ctx: 0x0059fff0: mov dword ptr [ebp - 0x10], eax ; 0x0059fff3: mov dword ptr [ebp - 4], 0 ; 0x0059fffa: cmp dword ptr [ebp - 0x10], 0 ; 0x0059fffe: je 0x5a000d
  - 0x0059fffe: je -> 0x005a0000 (jcc_false) | ctx: 0x0059fff0: mov dword ptr [ebp - 0x10], eax ; 0x0059fff3: mov dword ptr [ebp - 4], 0 ; 0x0059fffa: cmp dword ptr [ebp - 0x10], 0 ; 0x0059fffe: je 0x5a000d
  - 0x0059ffe4: jmp -> 0x005a0021 (jmp) | ctx: 0x0059ffe4: jmp 0x5a0021
  - 0x005a000b: jmp -> 0x005a0014 (jmp) | ctx: 0x005a0000: mov ecx, dword ptr [ebp - 0x10] ; 0x005a0003: call 0x59ff70 ; 0x005a0008: mov dword ptr [ebp - 0x14], eax ; 0x005a000b: jmp 0x5a0014

### 0x005a0570
- blocks=1, insns=30, edges=5, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005a05b9)
- branch points:
  - none

### 0x005a05e0
- blocks=1, insns=32, edges=5, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005a062f)
- branch points:
  - none

### 0x005a16e0
- blocks=1, insns=14, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005a16f2)
- branch points:
  - none

### 0x005a1700
- blocks=1, insns=15, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005a1716)
- branch points:
  - none

### 0x005a1df0
- blocks=3, insns=91, edges=18, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a2a60 at 0x005a1e21)
- branch points:
  - 0x005a1ebd: jmp -> 0x005a1ee3 (jmp) | ctx: 0x005a1eb1: call 0x5a2670 ; 0x005a1eb6: mov ecx, eax ; 0x005a1eb8: call 0x5c89a0 ; 0x005a1ebd: jmp 0x5a1ee3
  - 0x005a1eea: jmp -> 0x005a1ef3 (jmp) | ctx: 0x005a1ee3: mov dword ptr [ebp - 4], 0xffffffff ; 0x005a1eea: jmp 0x5a1ef3

### 0x005a2a00
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a2a60 at 0x005a2a0e)
  - caller_of_anchor_path: depth 2 (calls 0x005a2a80 at 0x005a2a0e)
- branch points:
  - none

### 0x005a2a20
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a2a60 at 0x005a2a2e)
  - caller_of_anchor_path: depth 2 (calls 0x005a2a80 at 0x005a2a2e)
  - caller_of_anchor_path: depth 2 (calls 0x005a2aa0 at 0x005a2a2e)
- branch points:
  - none

### 0x005a2a40
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a2a80 at 0x005a2a4e)
  - caller_of_anchor_path: depth 2 (calls 0x005a2aa0 at 0x005a2a4e)
- branch points:
  - none

### 0x005a2a60
- blocks=1, insns=13, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005a2a6f)
- branch points:
  - none

### 0x005a2a80
- blocks=1, insns=13, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005a2a92)
- branch points:
  - none

### 0x005a2aa0
- blocks=1, insns=13, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005a2aaf)
- branch points:
  - none

### 0x005a2fb0
- blocks=7, insns=65, edges=19, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a2aa0 at 0x005a2ff4)
- branch points:
  - 0x005a2fd3: je -> 0x005a300c (jcc_true) | ctx: 0x005a2fc9: call 0x5f1d80 ; 0x005a2fce: movzx ecx, al ; 0x005a2fd1: test ecx, ecx ; 0x005a2fd3: je 0x5a300c
  - 0x005a2fd3: je -> 0x005a2fd5 (jcc_false) | ctx: 0x005a2fc9: call 0x5f1d80 ; 0x005a2fce: movzx ecx, al ; 0x005a2fd1: test ecx, ecx ; 0x005a2fd3: je 0x5a300c
  - 0x005a301d: je -> 0x005a303e (jcc_true) | ctx: 0x005a3013: call 0x5f1de0 ; 0x005a3018: movzx eax, al ; 0x005a301b: test eax, eax ; 0x005a301d: je 0x5a303e
  - 0x005a301d: je -> 0x005a301f (jcc_false) | ctx: 0x005a3013: call 0x5f1de0 ; 0x005a3018: movzx eax, al ; 0x005a301b: test eax, eax ; 0x005a301d: je 0x5a303e
  - 0x005a2fef: je -> 0x005a300c (jcc_true) | ctx: 0x005a2fe5: call 0x5f1d80 ; 0x005a2fea: movzx eax, al ; 0x005a2fed: test eax, eax ; 0x005a2fef: je 0x5a300c
  - 0x005a2fef: je -> 0x005a2ff1 (jcc_false) | ctx: 0x005a2fe5: call 0x5f1d80 ; 0x005a2fea: movzx eax, al ; 0x005a2fed: test eax, eax ; 0x005a2fef: je 0x5a300c
  - 0x005a303c: jmp -> 0x005a300c (jmp) | ctx: 0x005a3033: push eax ; 0x005a3034: mov ecx, dword ptr [ebp - 4] ; 0x005a3037: call 0x5a3060 ; 0x005a303c: jmp 0x5a300c
  - 0x005a3008: jmp -> 0x005a3056 (jmp) | ctx: 0x005a2ffd: mov ecx, dword ptr [ebp - 4] ; 0x005a3000: call 0x5facb0 ; 0x005a3005: mov eax, dword ptr [ebp + 8] ; 0x005a3008: jmp 0x5a3056

### 0x005a4bf0
- blocks=15, insns=70, edges=27, jcc=8, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a2aa0 at 0x005a4c86)
- branch points:
  - 0x005a4bfe: jne -> 0x005a4c05 (jcc_true) | ctx: 0x005a4bf4: mov dword ptr [ebp - 4], ecx ; 0x005a4bf7: mov eax, dword ptr [ebp - 4] ; 0x005a4bfa: cmp dword ptr [eax + 0x18], 5 ; 0x005a4bfe: jne 0x5a4c05
  - 0x005a4bfe: jne -> 0x005a4c00 (jcc_false) | ctx: 0x005a4bf4: mov dword ptr [ebp - 4], ecx ; 0x005a4bf7: mov eax, dword ptr [ebp - 4] ; 0x005a4bfa: cmp dword ptr [eax + 0x18], 5 ; 0x005a4bfe: jne 0x5a4c05
  - 0x005a4c0c: jne -> 0x005a4c20 (jcc_true) | ctx: 0x005a4c05: mov ecx, dword ptr [ebp - 4] ; 0x005a4c08: cmp dword ptr [ecx + 0x14], 0xc ; 0x005a4c0c: jne 0x5a4c20
  - 0x005a4c0c: jne -> 0x005a4c0e (jcc_false) | ctx: 0x005a4c05: mov ecx, dword ptr [ebp - 4] ; 0x005a4c08: cmp dword ptr [ecx + 0x14], 0xc ; 0x005a4c0c: jne 0x5a4c20
  - 0x005a4c00: jmp -> 0x005a4cb3 (jmp) | ctx: 0x005a4c00: jmp 0x5a4cb3
  - 0x005a4c2d: jmp -> 0x005a4cb3 (jmp) | ctx: 0x005a4c22: mov ecx, dword ptr [ebp - 4] ; 0x005a4c25: sub ecx, 8 ; 0x005a4c28: call 0x5ac380 ; 0x005a4c2d: jmp 0x5a4cb3
  - 0x005a4c15: je -> 0x005a4c32 (jcc_true) | ctx: 0x005a4c0e: mov edx, dword ptr [ebp - 4] ; 0x005a4c11: cmp dword ptr [edx + 0x18], 3 ; 0x005a4c15: je 0x5a4c32
  - 0x005a4c15: je -> 0x005a4c17 (jcc_false) | ctx: 0x005a4c0e: mov edx, dword ptr [ebp - 4] ; 0x005a4c11: cmp dword ptr [edx + 0x18], 3 ; 0x005a4c15: je 0x5a4c32
  - 0x005a4c4a: jne -> 0x005a4c5b (jcc_true) | ctx: 0x005a4c40: call 0x492080 ; 0x005a4c45: movzx eax, al ; 0x005a4c48: test eax, eax ; 0x005a4c4a: jne 0x5a4c5b
  - 0x005a4c4a: jne -> 0x005a4c4c (jcc_false) | ctx: 0x005a4c40: call 0x492080 ; 0x005a4c45: movzx eax, al ; 0x005a4c48: test eax, eax ; 0x005a4c4a: jne 0x5a4c5b
  - 0x005a4c1e: je -> 0x005a4c32 (jcc_true) | ctx: 0x005a4c17: mov eax, dword ptr [ebp - 4] ; 0x005a4c1a: cmp dword ptr [eax + 0x18], 2 ; 0x005a4c1e: je 0x5a4c32
  - 0x005a4c1e: je -> 0x005a4c20 (jcc_false) | ctx: 0x005a4c17: mov eax, dword ptr [ebp - 4] ; 0x005a4c1a: cmp dword ptr [eax + 0x18], 2 ; 0x005a4c1e: je 0x5a4c32
  - 0x005a4c6f: jne -> 0x005a4c80 (jcc_true) | ctx: 0x005a4c65: call 0x492040 ; 0x005a4c6a: movzx edx, al ; 0x005a4c6d: test edx, edx ; 0x005a4c6f: jne 0x5a4c80
  - 0x005a4c6f: jne -> 0x005a4c71 (jcc_false) | ctx: 0x005a4c65: call 0x492040 ; 0x005a4c6a: movzx edx, al ; 0x005a4c6d: test edx, edx ; 0x005a4c6f: jne 0x5a4c80
  - 0x005a4c59: jmp -> 0x005a4cb3 (jmp) | ctx: 0x005a4c4e: mov ecx, dword ptr [ebp - 4] ; 0x005a4c51: sub ecx, 8 ; 0x005a4c54: call 0x5ac380 ; 0x005a4c59: jmp 0x5a4cb3
  - 0x005a4c92: jne -> 0x005a4ca0 (jcc_true) | ctx: 0x005a4c86: call 0x5a2ac0 ; 0x005a4c8b: mov eax, dword ptr [ebp - 4] ; 0x005a4c8e: cmp dword ptr [eax + 0x18], 3 ; 0x005a4c92: jne 0x5a4ca0
  - 0x005a4c92: jne -> 0x005a4c94 (jcc_false) | ctx: 0x005a4c86: call 0x5a2ac0 ; 0x005a4c8b: mov eax, dword ptr [ebp - 4] ; 0x005a4c8e: cmp dword ptr [eax + 0x18], 3 ; 0x005a4c92: jne 0x5a4ca0
  - 0x005a4c7e: jmp -> 0x005a4cb3 (jmp) | ctx: 0x005a4c73: mov ecx, dword ptr [ebp - 4] ; 0x005a4c76: sub ecx, 8 ; 0x005a4c79: call 0x5ac380 ; 0x005a4c7e: jmp 0x5a4cb3
  - 0x005a4ca7: jne -> 0x005a4cb3 (jcc_true) | ctx: 0x005a4ca0: mov edx, dword ptr [ebp - 4] ; 0x005a4ca3: cmp dword ptr [edx + 0x18], 2 ; 0x005a4ca7: jne 0x5a4cb3
  - 0x005a4ca7: jne -> 0x005a4ca9 (jcc_false) | ctx: 0x005a4ca0: mov edx, dword ptr [ebp - 4] ; 0x005a4ca3: cmp dword ptr [edx + 0x18], 2 ; 0x005a4ca7: jne 0x5a4cb3
  - 0x005a4c9e: jmp -> 0x005a4cb3 (jmp) | ctx: 0x005a4c94: mov ecx, dword ptr [ebp - 4] ; 0x005a4c97: mov dword ptr [ecx + 0x18], 4 ; 0x005a4c9e: jmp 0x5a4cb3

### 0x005a7070
- blocks=1, insns=18, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005a7090)
- branch points:
  - none

### 0x005a94e0
- blocks=3, insns=84, edges=19, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a2a60 at 0x005a9511)
- branch points:
  - 0x005a95bc: jmp -> 0x005a95e2 (jmp) | ctx: 0x005a95b0: call 0x5a2670 ; 0x005a95b5: mov ecx, eax ; 0x005a95b7: call 0x5c89a0 ; 0x005a95bc: jmp 0x5a95e2
  - 0x005a95e9: jmp -> 0x005a95f2 (jmp) | ctx: 0x005a95e2: mov dword ptr [ebp - 4], 0xffffffff ; 0x005a95e9: jmp 0x5a95f2

### 0x005aad70
- blocks=1, insns=17, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005aad8e)
- branch points:
  - none

### 0x005ac180
- blocks=15, insns=185, edges=64, jcc=7, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a2aa0 at 0x005ac345)
- branch points:
  - 0x005ac1bd: jbe -> 0x005ac1db (jcc_true) | ctx: 0x005ac1b3: add ecx, 0x40 ; 0x005ac1b6: call 0x501b00 ; 0x005ac1bb: test eax, eax ; 0x005ac1bd: jbe 0x5ac1db
  - 0x005ac1bd: jbe -> 0x005ac1bf (jcc_false) | ctx: 0x005ac1b3: add ecx, 0x40 ; 0x005ac1b6: call 0x501b00 ; 0x005ac1bb: test eax, eax ; 0x005ac1bd: jbe 0x5ac1db
  - 0x005ac1ea: jmp -> 0x005ac1f4 (jmp) | ctx: 0x005ac1df: mov ecx, dword ptr [ebp - 0x14] ; 0x005ac1e2: add ecx, 0x38 ; 0x005ac1e5: call 0x5facb0 ; 0x005ac1ea: jmp 0x5ac1f4
  - 0x005ac1ea: jmp -> 0x005ac1f4 (jmp) | ctx: 0x005ac1df: mov ecx, dword ptr [ebp - 0x14] ; 0x005ac1e2: add ecx, 0x38 ; 0x005ac1e5: call 0x5facb0 ; 0x005ac1ea: jmp 0x5ac1f4
  - 0x005ac211: je -> 0x005ac300 (jcc_true) | ctx: 0x005ac207: call 0x5f1de0 ; 0x005ac20c: movzx eax, al ; 0x005ac20f: test eax, eax ; 0x005ac211: je 0x5ac300
  - 0x005ac211: je -> 0x005ac217 (jcc_false) | ctx: 0x005ac207: call 0x5f1de0 ; 0x005ac20c: movzx eax, al ; 0x005ac20f: test eax, eax ; 0x005ac211: je 0x5ac300
  - 0x005ac30a: jbe -> 0x005ac33f (jcc_true) | ctx: 0x005ac300: lea ecx, [ebp - 0x2c] ; 0x005ac303: call 0x501b00 ; 0x005ac308: test eax, eax ; 0x005ac30a: jbe 0x5ac33f
  - 0x005ac30a: jbe -> 0x005ac30c (jcc_false) | ctx: 0x005ac300: lea ecx, [ebp - 0x2c] ; 0x005ac303: call 0x501b00 ; 0x005ac308: test eax, eax ; 0x005ac30a: jbe 0x5ac33f
  - 0x005ac223: jne -> 0x005ac260 (jcc_true) | ctx: 0x005ac217: lea ecx, [ebp - 0x10] ; 0x005ac21a: call 0x5a6b20 ; 0x005ac21f: cmp dword ptr [eax + 0x1c], 1 ; 0x005ac223: jne 0x5ac260
  - 0x005ac223: jne -> 0x005ac225 (jcc_false) | ctx: 0x005ac217: lea ecx, [ebp - 0x10] ; 0x005ac21a: call 0x5a6b20 ; 0x005ac21f: cmp dword ptr [eax + 0x1c], 1 ; 0x005ac223: jne 0x5ac260
  - 0x005ac31f: je -> 0x005ac33f (jcc_true) | ctx: 0x005ac315: call 0x5aacf0 ; 0x005ac31a: movzx ecx, al ; 0x005ac31d: test ecx, ecx ; 0x005ac31f: je 0x5ac33f
  - 0x005ac31f: je -> 0x005ac321 (jcc_false) | ctx: 0x005ac315: call 0x5aacf0 ; 0x005ac31a: movzx ecx, al ; 0x005ac31d: test ecx, ecx ; 0x005ac31f: je 0x5ac33f
  - 0x005ac26c: jne -> 0x005ac2b2 (jcc_true) | ctx: 0x005ac260: lea ecx, [ebp - 0x10] ; 0x005ac263: call 0x5a6b20 ; 0x005ac268: cmp dword ptr [eax + 0x20], 1 ; 0x005ac26c: jne 0x5ac2b2
  - 0x005ac26c: jne -> 0x005ac26e (jcc_false) | ctx: 0x005ac260: lea ecx, [ebp - 0x10] ; 0x005ac263: call 0x5a6b20 ; 0x005ac268: cmp dword ptr [eax + 0x20], 1 ; 0x005ac26c: jne 0x5ac2b2
  - 0x005ac25e: jmp -> 0x005ac2df (jmp) | ctx: 0x005ac255: push edx ; 0x005ac256: call 0x51374e ; 0x005ac25b: add esp, 0x10 ; 0x005ac25e: jmp 0x5ac2df
  - 0x005ac2fb: jmp -> 0x005ac1ec (jmp) | ctx: 0x005ac2ee: push 0xbbf63c ; 0x005ac2f3: lea ecx, [ebp - 0x2c] ; 0x005ac2f6: call 0x5113d0 ; 0x005ac2fb: jmp 0x5ac1ec
  - 0x005ac2b0: jmp -> 0x005ac2df (jmp) | ctx: 0x005ac2a7: push ecx ; 0x005ac2a8: call 0x51374e ; 0x005ac2ad: add esp, 0x10 ; 0x005ac2b0: jmp 0x5ac2df
  - 0x005ac2fb: jmp -> 0x005ac1ec (jmp) | ctx: 0x005ac2ee: push 0xbbf63c ; 0x005ac2f3: lea ecx, [ebp - 0x2c] ; 0x005ac2f6: call 0x5113d0 ; 0x005ac2fb: jmp 0x5ac1ec
  - 0x005ac211: je -> 0x005ac300 (jcc_true) | ctx: 0x005ac207: call 0x5f1de0 ; 0x005ac20c: movzx eax, al ; 0x005ac20f: test eax, eax ; 0x005ac211: je 0x5ac300
  - 0x005ac211: je -> 0x005ac217 (jcc_false) | ctx: 0x005ac207: call 0x5f1de0 ; 0x005ac20c: movzx eax, al ; 0x005ac20f: test eax, eax ; 0x005ac211: je 0x5ac300

### 0x005ad530
- blocks=26, insns=497, edges=138, jcc=14, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005ad960)
- branch points:
  - 0x005ad551: ja -> 0x005ad56a (jcc_true) | ctx: 0x005ad547: mov ecx, dword ptr [ebp - 8] ; 0x005ad54a: call 0x5a2880 ; 0x005ad54f: cmp esi, dword ptr [eax] ; 0x005ad551: ja 0x5ad56a
  - 0x005ad551: ja -> 0x005ad553 (jcc_false) | ctx: 0x005ad547: mov ecx, dword ptr [ebp - 8] ; 0x005ad54a: call 0x5a2880 ; 0x005ad54f: cmp esi, dword ptr [eax] ; 0x005ad551: ja 0x5ad56a
  - 0x005ad5b5: jne -> 0x005ad5e0 (jcc_true) | ctx: 0x005ad5ab: call 0x5d84b0 ; 0x005ad5b0: mov edx, dword ptr [ebp + 0x10] ; 0x005ad5b3: cmp edx, dword ptr [eax] ; 0x005ad5b5: jne 0x5ad5e0
  - 0x005ad5b5: jne -> 0x005ad5b7 (jcc_false) | ctx: 0x005ad5ab: call 0x5d84b0 ; 0x005ad5b0: mov edx, dword ptr [ebp + 0x10] ; 0x005ad5b3: cmp edx, dword ptr [eax] ; 0x005ad5b5: jne 0x5ad5e0
  - 0x005ad5b5: jne -> 0x005ad5e0 (jcc_true) | ctx: 0x005ad5ab: call 0x5d84b0 ; 0x005ad5b0: mov edx, dword ptr [ebp + 0x10] ; 0x005ad5b3: cmp edx, dword ptr [eax] ; 0x005ad5b5: jne 0x5ad5e0
  - 0x005ad5b5: jne -> 0x005ad5b7 (jcc_false) | ctx: 0x005ad5ab: call 0x5d84b0 ; 0x005ad5b0: mov edx, dword ptr [ebp + 0x10] ; 0x005ad5b3: cmp edx, dword ptr [eax] ; 0x005ad5b5: jne 0x5ad5e0
  - 0x005ad5e6: je -> 0x005ad617 (jcc_true) | ctx: 0x005ad5e0: movzx edx, byte ptr [ebp + 0xc] ; 0x005ad5e4: test edx, edx ; 0x005ad5e6: je 0x5ad617
  - 0x005ad5e6: je -> 0x005ad5e8 (jcc_false) | ctx: 0x005ad5e0: movzx edx, byte ptr [ebp + 0xc] ; 0x005ad5e4: test edx, edx ; 0x005ad5e6: je 0x5ad617
  - 0x005ad5de: jmp -> 0x005ad644 (jmp) | ctx: 0x005ad5d4: call 0x5a28e0 ; 0x005ad5d9: mov ecx, dword ptr [ebp - 0xc] ; 0x005ad5dc: mov dword ptr [eax], ecx ; 0x005ad5de: jmp 0x5ad644
  - 0x005ad635: jne -> 0x005ad644 (jcc_true) | ctx: 0x005ad62b: call 0x5a28e0 ; 0x005ad630: mov edx, dword ptr [ebp + 0x10] ; 0x005ad633: cmp edx, dword ptr [eax] ; 0x005ad635: jne 0x5ad644
  - 0x005ad635: jne -> 0x005ad637 (jcc_false) | ctx: 0x005ad62b: call 0x5a28e0 ; 0x005ad630: mov edx, dword ptr [ebp + 0x10] ; 0x005ad633: cmp edx, dword ptr [eax] ; 0x005ad635: jne 0x5ad644
  - 0x005ad606: jne -> 0x005ad615 (jcc_true) | ctx: 0x005ad5fc: call 0x5d83e0 ; 0x005ad601: mov edx, dword ptr [ebp + 0x10] ; 0x005ad604: cmp edx, dword ptr [eax] ; 0x005ad606: jne 0x5ad615
  - 0x005ad606: jne -> 0x005ad608 (jcc_false) | ctx: 0x005ad5fc: call 0x5d83e0 ; 0x005ad601: mov edx, dword ptr [ebp + 0x10] ; 0x005ad604: cmp edx, dword ptr [eax] ; 0x005ad606: jne 0x5ad615
  - 0x005ad666: jne -> 0x005ad93a (jcc_true) | ctx: 0x005ad65e: add esp, 4 ; 0x005ad661: movsx edx, byte ptr [eax] ; 0x005ad664: test edx, edx ; 0x005ad666: jne 0x5ad93a
  - 0x005ad666: jne -> 0x005ad66c (jcc_false) | ctx: 0x005ad65e: add esp, 4 ; 0x005ad661: movsx edx, byte ptr [eax] ; 0x005ad664: test edx, edx ; 0x005ad666: jne 0x5ad93a
  - 0x005ad666: jne -> 0x005ad93a (jcc_true) | ctx: 0x005ad65e: add esp, 4 ; 0x005ad661: movsx edx, byte ptr [eax] ; 0x005ad664: test edx, edx ; 0x005ad666: jne 0x5ad93a
  - 0x005ad666: jne -> 0x005ad66c (jcc_false) | ctx: 0x005ad65e: add esp, 4 ; 0x005ad661: movsx edx, byte ptr [eax] ; 0x005ad664: test edx, edx ; 0x005ad666: jne 0x5ad93a
  - 0x005ad615: jmp -> 0x005ad644 (jmp) | ctx: 0x005ad615: jmp 0x5ad644
  - 0x005ad615: jmp -> 0x005ad644 (jmp) | ctx: 0x005ad60b: call 0x5d83e0 ; 0x005ad610: mov ecx, dword ptr [ebp - 0xc] ; 0x005ad613: mov dword ptr [eax], ecx ; 0x005ad615: jmp 0x5ad644
  - 0x005ad6a0: jne -> 0x005ad7f0 (jcc_true) | ctx: 0x005ad699: add esp, 4 ; 0x005ad69c: mov ecx, dword ptr [esi] ; 0x005ad69e: cmp ecx, dword ptr [eax] ; 0x005ad6a0: jne 0x5ad7f0
  - 0x005ad6a0: jne -> 0x005ad6a6 (jcc_false) | ctx: 0x005ad699: add esp, 4 ; 0x005ad69c: mov ecx, dword ptr [esi] ; 0x005ad69e: cmp ecx, dword ptr [eax] ; 0x005ad6a0: jne 0x5ad7f0
  - 0x005ad828: jne -> 0x005ad899 (jcc_true) | ctx: 0x005ad820: add esp, 4 ; 0x005ad823: movsx eax, byte ptr [eax] ; 0x005ad826: test eax, eax ; 0x005ad828: jne 0x5ad899
  - 0x005ad828: jne -> 0x005ad82a (jcc_false) | ctx: 0x005ad820: add esp, 4 ; 0x005ad823: movsx eax, byte ptr [eax] ; 0x005ad826: test eax, eax ; 0x005ad828: jne 0x5ad899
  - 0x005ad6de: jne -> 0x005ad74f (jcc_true) | ctx: 0x005ad6d6: add esp, 4 ; 0x005ad6d9: movsx ecx, byte ptr [eax] ; 0x005ad6dc: test ecx, ecx ; 0x005ad6de: jne 0x5ad74f
  - 0x005ad6de: jne -> 0x005ad6e0 (jcc_false) | ctx: 0x005ad6d6: add esp, 4 ; 0x005ad6d9: movsx ecx, byte ptr [eax] ; 0x005ad6dc: test ecx, ecx ; 0x005ad6de: jne 0x5ad74f
  - 0x005ad8b5: jne -> 0x005ad8d4 (jcc_true) | ctx: 0x005ad8ad: add esp, 4 ; 0x005ad8b0: mov ecx, dword ptr [ebp - 4] ; 0x005ad8b3: cmp ecx, dword ptr [eax] ; 0x005ad8b5: jne 0x5ad8d4
  - 0x005ad8b5: jne -> 0x005ad8b7 (jcc_false) | ctx: 0x005ad8ad: add esp, 4 ; 0x005ad8b0: mov ecx, dword ptr [ebp - 4] ; 0x005ad8b3: cmp ecx, dword ptr [eax] ; 0x005ad8b5: jne 0x5ad8d4
  - 0x005ad894: jmp -> 0x005ad935 (jmp) | ctx: 0x005ad88c: add esp, 4 ; 0x005ad88f: mov eax, dword ptr [eax] ; 0x005ad891: mov dword ptr [ebp - 4], eax ; 0x005ad894: jmp 0x5ad935
  - 0x005ad76b: jne -> 0x005ad78a (jcc_true) | ctx: 0x005ad763: add esp, 4 ; 0x005ad766: mov ecx, dword ptr [ebp - 4] ; 0x005ad769: cmp ecx, dword ptr [eax] ; 0x005ad76b: jne 0x5ad78a
  - 0x005ad76b: jne -> 0x005ad76d (jcc_false) | ctx: 0x005ad763: add esp, 4 ; 0x005ad766: mov ecx, dword ptr [ebp - 4] ; 0x005ad769: cmp ecx, dword ptr [eax] ; 0x005ad76b: jne 0x5ad78a
  - 0x005ad74a: jmp -> 0x005ad7eb (jmp) | ctx: 0x005ad742: add esp, 4 ; 0x005ad745: mov ecx, dword ptr [eax] ; 0x005ad747: mov dword ptr [ebp - 4], ecx ; 0x005ad74a: jmp 0x5ad7eb
  - 0x005ad935: jmp -> 0x005ad64a (jmp) | ctx: 0x005ad92c: push eax ; 0x005ad92d: mov ecx, dword ptr [ebp - 8] ; 0x005ad930: call 0x546a08 ; 0x005ad935: jmp 0x5ad64a
  - 0x005ad935: jmp -> 0x005ad64a (jmp) | ctx: 0x005ad92c: push eax ; 0x005ad92d: mov ecx, dword ptr [ebp - 8] ; 0x005ad930: call 0x546a08 ; 0x005ad935: jmp 0x5ad64a
  - 0x005ad935: jmp -> 0x005ad64a (jmp) | ctx: 0x005ad935: jmp 0x5ad64a
  - 0x005ad7eb: jmp -> 0x005ad935 (jmp) | ctx: 0x005ad7e2: push eax ; 0x005ad7e3: mov ecx, dword ptr [ebp - 8] ; 0x005ad7e6: call 0x516f83 ; 0x005ad7eb: jmp 0x5ad935
  - 0x005ad7eb: jmp -> 0x005ad935 (jmp) | ctx: 0x005ad7e2: push eax ; 0x005ad7e3: mov ecx, dword ptr [ebp - 8] ; 0x005ad7e6: call 0x516f83 ; 0x005ad7eb: jmp 0x5ad935
  - 0x005ad7eb: jmp -> 0x005ad935 (jmp) | ctx: 0x005ad7eb: jmp 0x5ad935
  - 0x005ad666: jne -> 0x005ad93a (jcc_true) | ctx: 0x005ad65e: add esp, 4 ; 0x005ad661: movsx edx, byte ptr [eax] ; 0x005ad664: test edx, edx ; 0x005ad666: jne 0x5ad93a
  - 0x005ad666: jne -> 0x005ad66c (jcc_false) | ctx: 0x005ad65e: add esp, 4 ; 0x005ad661: movsx edx, byte ptr [eax] ; 0x005ad664: test edx, edx ; 0x005ad666: jne 0x5ad93a

### 0x005ad970
- blocks=23, insns=301, edges=73, jcc=11, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005adb23)
- branch points:
  - 0x005ad9d7: jne -> 0x005adac4 (jcc_true) | ctx: 0x005ad9cf: mov ecx, dword ptr [ebp - 0x3c] ; 0x005ad9d2: movsx edx, byte ptr [ecx] ; 0x005ad9d5: test edx, edx ; 0x005ad9d7: jne 0x5adac4
  - 0x005ad9d7: jne -> 0x005ad9dd (jcc_false) | ctx: 0x005ad9cf: mov ecx, dword ptr [ebp - 0x3c] ; 0x005ad9d2: movsx edx, byte ptr [ecx] ; 0x005ad9d5: test edx, edx ; 0x005ad9d7: jne 0x5adac4
  - 0x005adac6: je -> 0x005adb13 (jcc_true) | ctx: 0x005adac4: xor eax, eax ; 0x005adac6: je 0x5adb13
  - 0x005adac6: je -> 0x005adac8 (jcc_false) | ctx: 0x005adac4: xor eax, eax ; 0x005adac6: je 0x5adb13
  - 0x005ad9e9: je -> 0x005ada43 (jcc_true) | ctx: 0x005ad9e0: mov dword ptr [ebp - 0x28], eax ; 0x005ad9e3: movzx ecx, byte ptr [ebp + 0xc] ; 0x005ad9e7: test ecx, ecx ; 0x005ad9e9: je 0x5ada43
  - 0x005ad9e9: je -> 0x005ad9eb (jcc_false) | ctx: 0x005ad9e0: mov dword ptr [ebp - 0x28], eax ; 0x005ad9e3: movzx ecx, byte ptr [ebp + 0xc] ; 0x005ad9e7: test ecx, ecx ; 0x005ad9e9: je 0x5ada43
  - 0x005adb2e: jne -> 0x005adb32 (jcc_true) | ctx: 0x005adb23: call 0x5a16e0 ; 0x005adb28: movzx eax, byte ptr [ebp - 0x11] ; 0x005adb2c: test eax, eax ; 0x005adb2e: jne 0x5adb32
  - 0x005adb2e: jne -> 0x005adb30 (jcc_false) | ctx: 0x005adb23: call 0x5a16e0 ; 0x005adb28: movzx eax, byte ptr [ebp - 0x11] ; 0x005adb2c: test eax, eax ; 0x005adb2e: jne 0x5adb32
  - 0x005adb09: jmp -> 0x005adc83 (jmp) | ctx: 0x005adafe: mov ecx, dword ptr [ebp + 8] ; 0x005adb01: call 0x5a5360 ; 0x005adb06: mov eax, dword ptr [ebp + 8] ; 0x005adb09: jmp 0x5adc83
  - 0x005ada87: je -> 0x005adaa2 (jcc_true) | ctx: 0x005ada7e: mov byte ptr [ebp - 0x11], al ; 0x005ada81: movzx ecx, byte ptr [ebp - 0x11] ; 0x005ada85: test ecx, ecx ; 0x005ada87: je 0x5adaa2
  - 0x005ada87: je -> 0x005ada89 (jcc_false) | ctx: 0x005ada7e: mov byte ptr [ebp - 0x11], al ; 0x005ada81: movzx ecx, byte ptr [ebp - 0x11] ; 0x005ada85: test ecx, ecx ; 0x005ada87: je 0x5adaa2
  - 0x005ada29: jne -> 0x005ada34 (jcc_true) | ctx: 0x005ada20: mov byte ptr [ebp - 0x19], al ; 0x005ada23: movzx eax, byte ptr [ebp - 0x19] ; 0x005ada27: test eax, eax ; 0x005ada29: jne 0x5ada34
  - 0x005ada29: jne -> 0x005ada2b (jcc_false) | ctx: 0x005ada20: mov byte ptr [ebp - 0x19], al ; 0x005ada23: movzx eax, byte ptr [ebp - 0x19] ; 0x005ada27: test eax, eax ; 0x005ada29: jne 0x5ada34
  - 0x005adb50: je -> 0x005adb97 (jcc_true) | ctx: 0x005adb47: mov byte ptr [ebp - 0x1c], al ; 0x005adb4a: movzx edx, byte ptr [ebp - 0x1c] ; 0x005adb4e: test edx, edx ; 0x005adb50: je 0x5adb97
  - 0x005adb50: je -> 0x005adb52 (jcc_false) | ctx: 0x005adb47: mov byte ptr [ebp - 0x1c], al ; 0x005adb4a: movzx edx, byte ptr [ebp - 0x1c] ; 0x005adb4e: test edx, edx ; 0x005adb50: je 0x5adb97
  - 0x005adb30: jmp -> 0x005adb9f (jmp) | ctx: 0x005adb30: jmp 0x5adb9f
  - 0x005adabf: jmp -> 0x005ad9c0 (jmp) | ctx: 0x005adab6: mov dword ptr [ebp - 0x34], ecx ; 0x005adab9: mov edx, dword ptr [ebp - 0x34] ; 0x005adabc: mov dword ptr [ebp - 0x24], edx ; 0x005adabf: jmp 0x5ad9c0
  - 0x005adaa0: jmp -> 0x005adab9 (jmp) | ctx: 0x005ada98: mov eax, dword ptr [ebp - 0x50] ; 0x005ada9b: mov ecx, dword ptr [eax] ; 0x005ada9d: mov dword ptr [ebp - 0x34], ecx ; 0x005adaa0: jmp 0x5adab9
  - 0x005ada41: jmp -> 0x005ada81 (jmp) | ctx: 0x005ada34: mov dword ptr [ebp - 0x30], 0 ; 0x005ada3b: mov cl, byte ptr [ebp - 0x30] ; 0x005ada3e: mov byte ptr [ebp - 0x11], cl ; 0x005ada41: jmp 0x5ada81
  - 0x005ada32: jmp -> 0x005ada3b (jmp) | ctx: 0x005ada2b: mov dword ptr [ebp - 0x30], 1 ; 0x005ada32: jmp 0x5ada3b
  - 0x005adbe8: je -> 0x005adc2f (jcc_true) | ctx: 0x005adbdf: mov byte ptr [ebp - 0x1e], al ; 0x005adbe2: movzx ecx, byte ptr [ebp - 0x1e] ; 0x005adbe6: test ecx, ecx ; 0x005adbe8: je 0x5adc2f
  - 0x005adbe8: je -> 0x005adbea (jcc_false) | ctx: 0x005adbdf: mov byte ptr [ebp - 0x1e], al ; 0x005adbe2: movzx ecx, byte ptr [ebp - 0x1e] ; 0x005adbe6: test ecx, ecx ; 0x005adbe8: je 0x5adc2f
  - 0x005adb90: jmp -> 0x005adc83 (jmp) | ctx: 0x005adb85: mov ecx, dword ptr [ebp + 8] ; 0x005adb88: call 0x5a5360 ; 0x005adb8d: mov eax, dword ptr [ebp + 8] ; 0x005adb90: jmp 0x5adc83
  - 0x005adbe8: je -> 0x005adc2f (jcc_true) | ctx: 0x005adbdf: mov byte ptr [ebp - 0x1e], al ; 0x005adbe2: movzx ecx, byte ptr [ebp - 0x1e] ; 0x005adbe6: test ecx, ecx ; 0x005adbe8: je 0x5adc2f
  - 0x005adbe8: je -> 0x005adbea (jcc_false) | ctx: 0x005adbdf: mov byte ptr [ebp - 0x1e], al ; 0x005adbe2: movzx ecx, byte ptr [ebp - 0x1e] ; 0x005adbe6: test ecx, ecx ; 0x005adbe8: je 0x5adc2f
  - 0x005ad9d7: jne -> 0x005adac4 (jcc_true) | ctx: 0x005ad9cf: mov ecx, dword ptr [ebp - 0x3c] ; 0x005ad9d2: movsx edx, byte ptr [ecx] ; 0x005ad9d5: test edx, edx ; 0x005ad9d7: jne 0x5adac4
  - 0x005ad9d7: jne -> 0x005ad9dd (jcc_false) | ctx: 0x005ad9cf: mov ecx, dword ptr [ebp - 0x3c] ; 0x005ad9d2: movsx edx, byte ptr [ecx] ; 0x005ad9d5: test edx, edx ; 0x005ad9d7: jne 0x5adac4
  - 0x005adabf: jmp -> 0x005ad9c0 (jmp) | ctx: 0x005adab9: mov edx, dword ptr [ebp - 0x34] ; 0x005adabc: mov dword ptr [ebp - 0x24], edx ; 0x005adabf: jmp 0x5ad9c0
  - 0x005ada87: je -> 0x005adaa2 (jcc_true) | ctx: 0x005ada81: movzx ecx, byte ptr [ebp - 0x11] ; 0x005ada85: test ecx, ecx ; 0x005ada87: je 0x5adaa2
  - 0x005ada87: je -> 0x005ada89 (jcc_false) | ctx: 0x005ada81: movzx ecx, byte ptr [ebp - 0x11] ; 0x005ada85: test ecx, ecx ; 0x005ada87: je 0x5adaa2
  - 0x005ada41: jmp -> 0x005ada81 (jmp) | ctx: 0x005ada3b: mov cl, byte ptr [ebp - 0x30] ; 0x005ada3e: mov byte ptr [ebp - 0x11], cl ; 0x005ada41: jmp 0x5ada81
  - 0x005adc53: jmp -> 0x005adc83 (jmp) | ctx: 0x005adc48: mov ecx, dword ptr [ebp + 8] ; 0x005adc4b: call 0x5a5360 ; 0x005adc50: mov eax, dword ptr [ebp + 8] ; 0x005adc53: jmp 0x5adc83
  - 0x005adc2b: jmp -> 0x005adc83 (jmp) | ctx: 0x005adc20: mov ecx, dword ptr [ebp + 8] ; 0x005adc23: call 0x5a5360 ; 0x005adc28: mov eax, dword ptr [ebp + 8] ; 0x005adc2b: jmp 0x5adc83

### 0x005ae8f0
- blocks=1, insns=28, edges=4, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005ae92e)
- branch points:
  - none

### 0x005ae9c0
- blocks=1, insns=24, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005ae9f3)
- branch points:
  - none

### 0x005b7f90
- blocks=7, insns=45, edges=15, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005b8940 at 0x005b7fcf)
- branch points:
  - 0x005b7fa3: je -> 0x005b7ffe (jcc_true) | ctx: 0x005b7f99: mov ecx, dword ptr [ebp - 4] ; 0x005b7f9c: call 0x5b4860 ; 0x005b7fa1: test eax, eax ; 0x005b7fa3: je 0x5b7ffe
  - 0x005b7fa3: je -> 0x005b7fa5 (jcc_false) | ctx: 0x005b7f99: mov ecx, dword ptr [ebp - 4] ; 0x005b7f9c: call 0x5b4860 ; 0x005b7fa1: test eax, eax ; 0x005b7fa3: je 0x5b7ffe
  - 0x005b7fe4: je -> 0x005b7ff5 (jcc_true) | ctx: 0x005b7fda: mov eax, dword ptr [ebp - 0x18] ; 0x005b7fdd: mov dword ptr [ebp - 0xc], eax ; 0x005b7fe0: cmp dword ptr [ebp - 0xc], 0 ; 0x005b7fe4: je 0x5b7ff5
  - 0x005b7fe4: je -> 0x005b7fe6 (jcc_false) | ctx: 0x005b7fda: mov eax, dword ptr [ebp - 0x18] ; 0x005b7fdd: mov dword ptr [ebp - 0xc], eax ; 0x005b7fe0: cmp dword ptr [ebp - 0xc], 0 ; 0x005b7fe4: je 0x5b7ff5
  - 0x005b7ffc: jmp -> 0x005b7f99 (jmp) | ctx: 0x005b7ff5: mov dword ptr [ebp - 0x1c], 0 ; 0x005b7ffc: jmp 0x5b7f99
  - 0x005b7ff3: jmp -> 0x005b7ffc (jmp) | ctx: 0x005b7fe8: mov ecx, dword ptr [ebp - 0xc] ; 0x005b7feb: call 0x5b86d0 ; 0x005b7ff0: mov dword ptr [ebp - 0x1c], eax ; 0x005b7ff3: jmp 0x5b7ffc
  - 0x005b7fa3: je -> 0x005b7ffe (jcc_true) | ctx: 0x005b7f99: mov ecx, dword ptr [ebp - 4] ; 0x005b7f9c: call 0x5b4860 ; 0x005b7fa1: test eax, eax ; 0x005b7fa3: je 0x5b7ffe
  - 0x005b7fa3: je -> 0x005b7fa5 (jcc_false) | ctx: 0x005b7f99: mov ecx, dword ptr [ebp - 4] ; 0x005b7f9c: call 0x5b4860 ; 0x005b7fa1: test eax, eax ; 0x005b7fa3: je 0x5b7ffe
  - 0x005b7ffc: jmp -> 0x005b7f99 (jmp) | ctx: 0x005b7ffc: jmp 0x5b7f99

### 0x005b8190
- blocks=15, insns=144, edges=46, jcc=7, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005b8940 at 0x005b82bb)
- branch points:
  - 0x005b81c9: jmp -> 0x005b81d3 (jmp) | ctx: 0x005b81c0: push eax ; 0x005b81c1: mov ecx, dword ptr [ebp - 0x10] ; 0x005b81c4: call 0x5ae890 ; 0x005b81c9: jmp 0x5b81d3
  - 0x005b81ed: je -> 0x005b821d (jcc_true) | ctx: 0x005b81e3: call 0x5f1de0 ; 0x005b81e8: movzx edx, al ; 0x005b81eb: test edx, edx ; 0x005b81ed: je 0x5b821d
  - 0x005b81ed: je -> 0x005b81ef (jcc_false) | ctx: 0x005b81e3: call 0x5f1de0 ; 0x005b81e8: movzx edx, al ; 0x005b81eb: test edx, edx ; 0x005b81ed: je 0x5b821d
  - 0x005b8229: jmp -> 0x005b8233 (jmp) | ctx: 0x005b8220: push eax ; 0x005b8221: lea ecx, [ebp - 0x58] ; 0x005b8224: call 0x5ae890 ; 0x005b8229: jmp 0x5b8233
  - 0x005b820d: jge -> 0x005b821b (jcc_true) | ctx: 0x005b8204: mov dword ptr [ebp - 0x2c], eax ; 0x005b8207: mov ecx, dword ptr [ebp - 0x2c] ; 0x005b820a: cmp ecx, dword ptr [ebp + 8] ; 0x005b820d: jge 0x5b821b
  - 0x005b820d: jge -> 0x005b820f (jcc_false) | ctx: 0x005b8204: mov dword ptr [ebp - 0x2c], eax ; 0x005b8207: mov ecx, dword ptr [ebp - 0x2c] ; 0x005b820a: cmp ecx, dword ptr [ebp + 8] ; 0x005b820d: jge 0x5b821b
  - 0x005b824d: je -> 0x005b82ed (jcc_true) | ctx: 0x005b8243: call 0x5f1de0 ; 0x005b8248: movzx edx, al ; 0x005b824b: test edx, edx ; 0x005b824d: je 0x5b82ed
  - 0x005b824d: je -> 0x005b8253 (jcc_false) | ctx: 0x005b8243: call 0x5f1de0 ; 0x005b8248: movzx edx, al ; 0x005b824b: test edx, edx ; 0x005b824d: je 0x5b82ed
  - 0x005b821b: jmp -> 0x005b81cb (jmp) | ctx: 0x005b821b: jmp 0x5b81cb
  - 0x005b821b: jmp -> 0x005b81cb (jmp) | ctx: 0x005b8212: push edx ; 0x005b8213: lea ecx, [ebp - 0x58] ; 0x005b8216: call 0x5b89d0 ; 0x005b821b: jmp 0x5b81cb
  - 0x005b82a8: je -> 0x005b82e8 (jcc_true) | ctx: 0x005b829e: call 0x5f1de0 ; 0x005b82a3: movzx edx, al ; 0x005b82a6: test edx, edx ; 0x005b82a8: je 0x5b82e8
  - 0x005b82a8: je -> 0x005b82aa (jcc_false) | ctx: 0x005b829e: call 0x5f1de0 ; 0x005b82a3: movzx edx, al ; 0x005b82a6: test edx, edx ; 0x005b82a8: je 0x5b82e8
  - 0x005b81ed: je -> 0x005b821d (jcc_true) | ctx: 0x005b81e3: call 0x5f1de0 ; 0x005b81e8: movzx edx, al ; 0x005b81eb: test edx, edx ; 0x005b81ed: je 0x5b821d
  - 0x005b81ed: je -> 0x005b81ef (jcc_false) | ctx: 0x005b81e3: call 0x5f1de0 ; 0x005b81e8: movzx edx, al ; 0x005b81eb: test edx, edx ; 0x005b81ed: je 0x5b821d
  - 0x005b82e8: jmp -> 0x005b822b (jmp) | ctx: 0x005b82e8: jmp 0x5b822b
  - 0x005b82d0: je -> 0x005b82e1 (jcc_true) | ctx: 0x005b82c6: mov ecx, dword ptr [ebp - 0x34] ; 0x005b82c9: mov dword ptr [ebp - 0x28], ecx ; 0x005b82cc: cmp dword ptr [ebp - 0x28], 0 ; 0x005b82d0: je 0x5b82e1
  - 0x005b82d0: je -> 0x005b82d2 (jcc_false) | ctx: 0x005b82c6: mov ecx, dword ptr [ebp - 0x34] ; 0x005b82c9: mov dword ptr [ebp - 0x28], ecx ; 0x005b82cc: cmp dword ptr [ebp - 0x28], 0 ; 0x005b82d0: je 0x5b82e1
  - 0x005b824d: je -> 0x005b82ed (jcc_true) | ctx: 0x005b8243: call 0x5f1de0 ; 0x005b8248: movzx edx, al ; 0x005b824b: test edx, edx ; 0x005b824d: je 0x5b82ed
  - 0x005b824d: je -> 0x005b8253 (jcc_false) | ctx: 0x005b8243: call 0x5f1de0 ; 0x005b8248: movzx edx, al ; 0x005b824b: test edx, edx ; 0x005b824d: je 0x5b82ed
  - 0x005b82e8: jmp -> 0x005b822b (jmp) | ctx: 0x005b82e1: mov dword ptr [ebp - 0x38], 0 ; 0x005b82e8: jmp 0x5b822b
  - 0x005b82df: jmp -> 0x005b82e8 (jmp) | ctx: 0x005b82d4: mov ecx, dword ptr [ebp - 0x28] ; 0x005b82d7: call 0x5b86d0 ; 0x005b82dc: mov dword ptr [ebp - 0x38], eax ; 0x005b82df: jmp 0x5b82e8

### 0x005b8720
- blocks=5, insns=105, edges=23, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005b8940 at 0x005b8751)
- branch points:
  - 0x005b875d: jne -> 0x005b876b (jcc_true) | ctx: 0x005b8751: call 0x5b8920 ; 0x005b8756: mov dword ptr [ebp - 0x14], eax ; 0x005b8759: cmp dword ptr [ebp + 8], 0 ; 0x005b875d: jne 0x5b876b
  - 0x005b875d: jne -> 0x005b875f (jcc_false) | ctx: 0x005b8751: call 0x5b8920 ; 0x005b8756: mov dword ptr [ebp - 0x14], eax ; 0x005b8759: cmp dword ptr [ebp + 8], 0 ; 0x005b875d: jne 0x5b876b
  - 0x005b87d0: jmp -> 0x005b87f6 (jmp) | ctx: 0x005b87c4: call 0x5d8290 ; 0x005b87c9: mov ecx, eax ; 0x005b87cb: call 0x5c89a0 ; 0x005b87d0: jmp 0x5b87f6
  - 0x005b87d0: jmp -> 0x005b87f6 (jmp) | ctx: 0x005b87c4: call 0x5d8290 ; 0x005b87c9: mov ecx, eax ; 0x005b87cb: call 0x5c89a0 ; 0x005b87d0: jmp 0x5b87f6
  - 0x005b87fd: jmp -> 0x005b8806 (jmp) | ctx: 0x005b87f6: mov dword ptr [ebp - 4], 0xffffffff ; 0x005b87fd: jmp 0x5b8806

### 0x005b88f0
- blocks=1, insns=16, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005b8909)
- branch points:
  - none

### 0x005b8920
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005b8940 at 0x005b892e)
- branch points:
  - none

### 0x005b8940
- blocks=1, insns=13, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005b894f)
- branch points:
  - none

### 0x005c4af0
- blocks=12, insns=164, edges=43, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c4cf0 at 0x005c4ca1)
- branch points:
  - 0x005c4b29: jae -> 0x005c4b33 (jcc_true) | ctx: 0x005c4b1e: mov ecx, dword ptr [ebp - 0x14] ; 0x005c4b21: call 0x5c5940 ; 0x005c4b26: cmp eax, dword ptr [ebp - 0x18] ; 0x005c4b29: jae 0x5c4b33
  - 0x005c4b29: jae -> 0x005c4b2b (jcc_false) | ctx: 0x005c4b1e: mov ecx, dword ptr [ebp - 0x14] ; 0x005c4b21: call 0x5c5940 ; 0x005c4b26: cmp eax, dword ptr [ebp - 0x18] ; 0x005c4b29: jae 0x5c4b33
  - 0x005c4b4f: ja -> 0x005c4b53 (jcc_true) | ctx: 0x005c4b49: mov edx, dword ptr [eax] ; 0x005c4b4b: shr edx, 1 ; 0x005c4b4d: cmp edx, esi ; 0x005c4b4f: ja 0x5c4b53
  - 0x005c4b4f: ja -> 0x005c4b51 (jcc_false) | ctx: 0x005c4b49: mov edx, dword ptr [eax] ; 0x005c4b4b: shr edx, 1 ; 0x005c4b4d: cmp edx, esi ; 0x005c4b4f: ja 0x5c4b53
  - 0x005c4b31: jmp -> 0x005c4b9d (jmp) | ctx: 0x005c4b2b: mov ecx, dword ptr [ebp + 8] ; 0x005c4b2e: mov dword ptr [ebp - 0x18], ecx ; 0x005c4b31: jmp 0x5c4b9d
  - 0x005c4b75: ja -> 0x005c4b92 (jcc_true) | ctx: 0x005c4b6b: mov ecx, dword ptr [ebp - 0x14] ; 0x005c4b6e: call 0x5d84f0 ; 0x005c4b73: cmp dword ptr [eax], edi ; 0x005c4b75: ja 0x5c4b92
  - 0x005c4b75: ja -> 0x005c4b77 (jcc_false) | ctx: 0x005c4b6b: mov ecx, dword ptr [ebp - 0x14] ; 0x005c4b6e: call 0x5d84f0 ; 0x005c4b73: cmp dword ptr [eax], edi ; 0x005c4b75: ja 0x5c4b92
  - 0x005c4b51: jmp -> 0x005c4b9d (jmp) | ctx: 0x005c4b51: jmp 0x5c4b9d
  - 0x005c4bc3: jmp -> 0x005c4c24 (jmp) | ctx: 0x005c4bba: mov dword ptr [ebp - 0x20], eax ; 0x005c4bbd: mov ecx, dword ptr [ebp - 0x20] ; 0x005c4bc0: mov dword ptr [ebp - 0x1c], ecx ; 0x005c4bc3: jmp 0x5c4c24
  - 0x005c4bc3: jmp -> 0x005c4c24 (jmp) | ctx: 0x005c4bba: mov dword ptr [ebp - 0x20], eax ; 0x005c4bbd: mov ecx, dword ptr [ebp - 0x20] ; 0x005c4bc0: mov dword ptr [ebp - 0x1c], ecx ; 0x005c4bc3: jmp 0x5c4c24
  - 0x005c4b90: jmp -> 0x005c4b9d (jmp) | ctx: 0x005c4b86: call 0x5d84f0 ; 0x005c4b8b: add esi, dword ptr [eax] ; 0x005c4b8d: mov dword ptr [ebp - 0x18], esi ; 0x005c4b90: jmp 0x5c4b9d
  - 0x005c4c2b: jmp -> 0x005c4c34 (jmp) | ctx: 0x005c4c24: mov dword ptr [ebp - 4], 0xffffffff ; 0x005c4c2b: jmp 0x5c4c34
  - 0x005c4c38: jbe -> 0x005c4c5c (jcc_true) | ctx: 0x005c4c34: cmp dword ptr [ebp + 0xc], 0 ; 0x005c4c38: jbe 0x5c4c5c
  - 0x005c4c38: jbe -> 0x005c4c3a (jcc_false) | ctx: 0x005c4c34: cmp dword ptr [ebp + 0xc], 0 ; 0x005c4c38: jbe 0x5c4c5c

### 0x005c4cf0
- blocks=1, insns=22, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005c4d21)
- branch points:
  - none

### 0x005c4dd0
- blocks=16, insns=78, edges=34, jcc=9, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c4cf0 at 0x005c4e63)
- branch points:
  - 0x005c4de4: jae -> 0x005c4dee (jcc_true) | ctx: 0x005c4dd9: mov ecx, dword ptr [ebp - 4] ; 0x005c4ddc: call 0x5c5940 ; 0x005c4de1: cmp eax, dword ptr [ebp + 8] ; 0x005c4de4: jae 0x5c4dee
  - 0x005c4de4: jae -> 0x005c4de6 (jcc_false) | ctx: 0x005c4dd9: mov ecx, dword ptr [ebp - 4] ; 0x005c4ddc: call 0x5c5940 ; 0x005c4de1: cmp eax, dword ptr [ebp + 8] ; 0x005c4de4: jae 0x5c4dee
  - 0x005c4dfb: jae -> 0x005c4e16 (jcc_true) | ctx: 0x005c4df1: call 0x5d84f0 ; 0x005c4df6: mov eax, dword ptr [eax] ; 0x005c4df8: cmp eax, dword ptr [ebp + 8] ; 0x005c4dfb: jae 0x5c4e16
  - 0x005c4dfb: jae -> 0x005c4dfd (jcc_false) | ctx: 0x005c4df1: call 0x5d84f0 ; 0x005c4df6: mov eax, dword ptr [eax] ; 0x005c4df8: cmp eax, dword ptr [ebp + 8] ; 0x005c4dfb: jae 0x5c4e16
  - 0x005c4dfb: jae -> 0x005c4e16 (jcc_true) | ctx: 0x005c4df1: call 0x5d84f0 ; 0x005c4df6: mov eax, dword ptr [eax] ; 0x005c4df8: cmp eax, dword ptr [ebp + 8] ; 0x005c4dfb: jae 0x5c4e16
  - 0x005c4dfb: jae -> 0x005c4dfd (jcc_false) | ctx: 0x005c4df1: call 0x5d84f0 ; 0x005c4df6: mov eax, dword ptr [eax] ; 0x005c4df8: cmp eax, dword ptr [ebp + 8] ; 0x005c4dfb: jae 0x5c4e16
  - 0x005c4e1c: je -> 0x005c4e58 (jcc_true) | ctx: 0x005c4e16: movzx eax, byte ptr [ebp + 0xc] ; 0x005c4e1a: test eax, eax ; 0x005c4e1c: je 0x5c4e58
  - 0x005c4e1c: je -> 0x005c4e1e (jcc_false) | ctx: 0x005c4e16: movzx eax, byte ptr [ebp + 0xc] ; 0x005c4e1a: test eax, eax ; 0x005c4e1c: je 0x5c4e58
  - 0x005c4e14: jmp -> 0x005c4e68 (jmp) | ctx: 0x005c4e0b: push edx ; 0x005c4e0c: mov ecx, dword ptr [ebp - 4] ; 0x005c4e0f: call 0x5c4af0 ; 0x005c4e14: jmp 0x5c4e68
  - 0x005c4e5c: jne -> 0x005c4e68 (jcc_true) | ctx: 0x005c4e58: cmp dword ptr [ebp + 8], 0 ; 0x005c4e5c: jne 0x5c4e68
  - 0x005c4e5c: jne -> 0x005c4e5e (jcc_false) | ctx: 0x005c4e58: cmp dword ptr [ebp + 8], 0 ; 0x005c4e5c: jne 0x5c4e68
  - 0x005c4e22: jae -> 0x005c4e58 (jcc_true) | ctx: 0x005c4e1e: cmp dword ptr [ebp + 8], 0x10 ; 0x005c4e22: jae 0x5c4e58
  - 0x005c4e22: jae -> 0x005c4e24 (jcc_false) | ctx: 0x005c4e1e: cmp dword ptr [ebp + 8], 0x10 ; 0x005c4e22: jae 0x5c4e58
  - 0x005c4e6c: jbe -> 0x005c4e77 (jcc_true) | ctx: 0x005c4e68: cmp dword ptr [ebp + 8], 0 ; 0x005c4e6c: jbe 0x5c4e77
  - 0x005c4e6c: jbe -> 0x005c4e6e (jcc_false) | ctx: 0x005c4e68: cmp dword ptr [ebp + 8], 0 ; 0x005c4e6c: jbe 0x5c4e77
  - 0x005c4e6c: jbe -> 0x005c4e77 (jcc_true) | ctx: 0x005c4e60: mov ecx, dword ptr [ebp - 4] ; 0x005c4e63: call 0x5c4cf0 ; 0x005c4e68: cmp dword ptr [ebp + 8], 0 ; 0x005c4e6c: jbe 0x5c4e77
  - 0x005c4e6c: jbe -> 0x005c4e6e (jcc_false) | ctx: 0x005c4e60: mov ecx, dword ptr [ebp - 4] ; 0x005c4e63: call 0x5c4cf0 ; 0x005c4e68: cmp dword ptr [ebp + 8], 0 ; 0x005c4e6c: jbe 0x5c4e77
  - 0x005c4e31: jae -> 0x005c4e3b (jcc_true) | ctx: 0x005c4e27: call 0x5c4f40 ; 0x005c4e2c: mov ecx, dword ptr [ebp + 8] ; 0x005c4e2f: cmp ecx, dword ptr [eax] ; 0x005c4e31: jae 0x5c4e3b
  - 0x005c4e31: jae -> 0x005c4e33 (jcc_false) | ctx: 0x005c4e27: call 0x5c4f40 ; 0x005c4e2c: mov ecx, dword ptr [ebp + 8] ; 0x005c4e2f: cmp ecx, dword ptr [eax] ; 0x005c4e31: jae 0x5c4e3b
  - 0x005c4e75: jmp -> 0x005c4e7e (jmp) | ctx: 0x005c4e6e: mov dword ptr [ebp - 0xc], 1 ; 0x005c4e75: jmp 0x5c4e7e
  - 0x005c4e56: jmp -> 0x005c4e68 (jmp) | ctx: 0x005c4e4c: push 1 ; 0x005c4e4e: mov ecx, dword ptr [ebp - 4] ; 0x005c4e51: call 0x5c5130 ; 0x005c4e56: jmp 0x5c4e68
  - 0x005c4e39: jmp -> 0x005c4e48 (jmp) | ctx: 0x005c4e33: mov edx, dword ptr [ebp + 8] ; 0x005c4e36: mov dword ptr [ebp - 8], edx ; 0x005c4e39: jmp 0x5c4e48
  - 0x005c4e56: jmp -> 0x005c4e68 (jmp) | ctx: 0x005c4e4c: push 1 ; 0x005c4e4e: mov ecx, dword ptr [ebp - 4] ; 0x005c4e51: call 0x5c5130 ; 0x005c4e56: jmp 0x5c4e68

### 0x005c4f70
- blocks=5, insns=121, edges=27, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c53e0 at 0x005c4fa3)
- branch points:
  - 0x005c4fd4: jmp -> 0x005c4ffc (jmp) | ctx: 0x005c4fcb: push eax ; 0x005c4fcc: mov ecx, dword ptr [ebp - 0x14] ; 0x005c4fcf: call 0x5c1ed0 ; 0x005c4fd4: jmp 0x5c4ffc
  - 0x005c5003: jmp -> 0x005c500c (jmp) | ctx: 0x005c4ffc: mov dword ptr [ebp - 4], 0xffffffff ; 0x005c5003: jmp 0x5c500c
  - 0x005c5022: je -> 0x005c507b (jcc_true) | ctx: 0x005c5017: mov ecx, dword ptr [ebp - 0x14] ; 0x005c501a: call 0x5fa1a0 ; 0x005c501f: cmp dword ptr [eax], 0 ; 0x005c5022: je 0x5c507b
  - 0x005c5022: je -> 0x005c5024 (jcc_false) | ctx: 0x005c5017: mov ecx, dword ptr [ebp - 0x14] ; 0x005c501a: call 0x5fa1a0 ; 0x005c501f: cmp dword ptr [eax], 0 ; 0x005c5022: je 0x5c507b

### 0x005c5130
- blocks=7, insns=92, edges=28, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c4cf0 at 0x005c51df)
- branch points:
  - 0x005c513f: jne -> 0x005c5146 (jcc_true) | ctx: 0x005c5136: mov dword ptr [ebp - 4], ecx ; 0x005c5139: movzx eax, byte ptr [ebp + 8] ; 0x005c513d: test eax, eax ; 0x005c513f: jne 0x5c5146
  - 0x005c513f: jne -> 0x005c5141 (jcc_false) | ctx: 0x005c5136: mov dword ptr [ebp - 4], ecx ; 0x005c5139: movzx eax, byte ptr [ebp + 8] ; 0x005c513d: test eax, eax ; 0x005c513f: jne 0x5c5146
  - 0x005c5151: jb -> 0x005c51ca (jcc_true) | ctx: 0x005c5146: mov ecx, dword ptr [ebp - 4] ; 0x005c5149: call 0x5d84f0 ; 0x005c514e: cmp dword ptr [eax], 0x10 ; 0x005c5151: jb 0x5c51ca
  - 0x005c5151: jb -> 0x005c5153 (jcc_false) | ctx: 0x005c5146: mov ecx, dword ptr [ebp - 4] ; 0x005c5149: call 0x5d84f0 ; 0x005c514e: cmp dword ptr [eax], 0x10 ; 0x005c5151: jb 0x5c51ca
  - 0x005c5141: jmp -> 0x005c51ca (jmp) | ctx: 0x005c5141: jmp 0x5c51ca
  - 0x005c5185: jbe -> 0x005c51a9 (jcc_true) | ctx: 0x005c517a: mov ecx, eax ; 0x005c517c: call 0x5ed150 ; 0x005c5181: cmp dword ptr [ebp + 0xc], 0 ; 0x005c5185: jbe 0x5c51a9
  - 0x005c5185: jbe -> 0x005c5187 (jcc_false) | ctx: 0x005c517a: mov ecx, eax ; 0x005c517c: call 0x5ed150 ; 0x005c5181: cmp dword ptr [ebp + 0xc], 0 ; 0x005c5185: jbe 0x5c51a9

### 0x005c53a0
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c53e0 at 0x005c53ae)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x005c53ae)
- branch points:
  - none

### 0x005c53c0
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c53e0 at 0x005c53ce)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x005c53ce)
- branch points:
  - none

### 0x005c53e0
- blocks=1, insns=13, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005c53ef)
- branch points:
  - none

### 0x005c5400
- blocks=1, insns=13, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005c540f)
- branch points:
  - none

### 0x005c5420
- blocks=5, insns=60, edges=14, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c4cf0 at 0x005c54aa)
- branch points:
  - 0x005c544c: jne -> 0x005c546d (jcc_true) | ctx: 0x005c5443: mov dword ptr [ebp + 0x10], eax ; 0x005c5446: mov eax, dword ptr [ebp - 4] ; 0x005c5449: cmp eax, dword ptr [ebp + 8] ; 0x005c544c: jne 0x5c546d
  - 0x005c544c: jne -> 0x005c544e (jcc_false) | ctx: 0x005c5443: mov dword ptr [ebp + 0x10], eax ; 0x005c5446: mov eax, dword ptr [ebp - 4] ; 0x005c5449: cmp eax, dword ptr [ebp + 8] ; 0x005c544c: jne 0x5c546d
  - 0x005c5480: je -> 0x005c54af (jcc_true) | ctx: 0x005c5476: call 0x5c4dd0 ; 0x005c547b: movzx ecx, al ; 0x005c547e: test ecx, ecx ; 0x005c5480: je 0x5c54af
  - 0x005c5480: je -> 0x005c5482 (jcc_false) | ctx: 0x005c5476: call 0x5c4dd0 ; 0x005c547b: movzx ecx, al ; 0x005c547e: test ecx, ecx ; 0x005c5480: je 0x5c54af
  - 0x005c546b: jmp -> 0x005c54af (jmp) | ctx: 0x005c5461: push 0 ; 0x005c5463: mov ecx, dword ptr [ebp - 4] ; 0x005c5466: call 0x5c57f0 ; 0x005c546b: jmp 0x5c54af

### 0x005c54f0
- blocks=6, insns=55, edges=12, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c4cf0 at 0x005c555f)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x005c5523)
- branch points:
  - 0x005c5508: je -> 0x005c552a (jcc_true) | ctx: 0x005c54fe: call 0x5c4ef0 ; 0x005c5503: movzx ecx, al ; 0x005c5506: test ecx, ecx ; 0x005c5508: je 0x5c552a
  - 0x005c5508: je -> 0x005c550a (jcc_false) | ctx: 0x005c54fe: call 0x5c4ef0 ; 0x005c5503: movzx ecx, al ; 0x005c5506: test ecx, ecx ; 0x005c5508: je 0x5c552a
  - 0x005c553d: je -> 0x005c5564 (jcc_true) | ctx: 0x005c5533: call 0x5c4dd0 ; 0x005c5538: movzx ecx, al ; 0x005c553b: test ecx, ecx ; 0x005c553d: je 0x5c5564
  - 0x005c553d: je -> 0x005c553f (jcc_false) | ctx: 0x005c5533: call 0x5c4dd0 ; 0x005c5538: movzx ecx, al ; 0x005c553b: test ecx, ecx ; 0x005c553d: je 0x5c5564
  - 0x005c5528: jmp -> 0x005c5567 (jmp) | ctx: 0x005c551f: push edx ; 0x005c5520: mov ecx, dword ptr [ebp - 4] ; 0x005c5523: call 0x5c5420 ; 0x005c5528: jmp 0x5c5567

### 0x005c5570
- blocks=1, insns=24, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005c55a3)
- branch points:
  - none

### 0x005c57c0
- blocks=1, insns=16, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c4cf0 at 0x005c57da)
- branch points:
  - none

### 0x005c57f0
- blocks=5, insns=52, edges=12, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c4cf0 at 0x005c581e)
  - caller_of_anchor_path: depth 2 (calls 0x005c4cf0 at 0x005c586a)
- branch points:
  - 0x005c5815: ja -> 0x005c5825 (jcc_true) | ctx: 0x005c580d: mov ecx, dword ptr [eax] ; 0x005c580f: sub ecx, dword ptr [ebp + 8] ; 0x005c5812: cmp ecx, dword ptr [ebp + 0xc] ; 0x005c5815: ja 0x5c5825
  - 0x005c5815: ja -> 0x005c5817 (jcc_false) | ctx: 0x005c580d: mov ecx, dword ptr [eax] ; 0x005c580f: sub ecx, dword ptr [ebp + 8] ; 0x005c5812: cmp ecx, dword ptr [ebp + 0xc] ; 0x005c5815: ja 0x5c5825
  - 0x005c5829: jbe -> 0x005c586f (jcc_true) | ctx: 0x005c5825: cmp dword ptr [ebp + 0xc], 0 ; 0x005c5829: jbe 0x5c586f
  - 0x005c5829: jbe -> 0x005c582b (jcc_false) | ctx: 0x005c5825: cmp dword ptr [ebp + 0xc], 0 ; 0x005c5829: jbe 0x5c586f
  - 0x005c5823: jmp -> 0x005c586f (jmp) | ctx: 0x005c581a: push edx ; 0x005c581b: mov ecx, dword ptr [ebp - 4] ; 0x005c581e: call 0x5c4cf0 ; 0x005c5823: jmp 0x5c586f

### 0x005c7b80
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c9fe0 at 0x005c7b8d)
- branch points:
  - none

### 0x005c9800
- blocks=5, insns=105, edges=23, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c9fa0 at 0x005c9831)
- branch points:
  - 0x005c983d: jne -> 0x005c984b (jcc_true) | ctx: 0x005c9831: call 0x5c9f80 ; 0x005c9836: mov dword ptr [ebp - 0x14], eax ; 0x005c9839: cmp dword ptr [ebp + 8], 0 ; 0x005c983d: jne 0x5c984b
  - 0x005c983d: jne -> 0x005c983f (jcc_false) | ctx: 0x005c9831: call 0x5c9f80 ; 0x005c9836: mov dword ptr [ebp - 0x14], eax ; 0x005c9839: cmp dword ptr [ebp + 8], 0 ; 0x005c983d: jne 0x5c984b
  - 0x005c98b0: jmp -> 0x005c98d6 (jmp) | ctx: 0x005c98a4: call 0x5d8290 ; 0x005c98a9: mov ecx, eax ; 0x005c98ab: call 0x5c89a0 ; 0x005c98b0: jmp 0x5c98d6
  - 0x005c98b0: jmp -> 0x005c98d6 (jmp) | ctx: 0x005c98a4: call 0x5d8290 ; 0x005c98a9: mov ecx, eax ; 0x005c98ab: call 0x5c89a0 ; 0x005c98b0: jmp 0x5c98d6
  - 0x005c98dd: jmp -> 0x005c98e6 (jmp) | ctx: 0x005c98d6: mov dword ptr [ebp - 4], 0xffffffff ; 0x005c98dd: jmp 0x5c98e6

### 0x005c9e30
- blocks=1, insns=9, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c9fe0 at 0x005c9e3a)
- branch points:
  - none

### 0x005c9f40
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c9fa0 at 0x005c9f4e)
  - caller_of_anchor_path: depth 2 (calls 0x005c9fc0 at 0x005c9f4e)
- branch points:
  - none

### 0x005c9f60
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c9fa0 at 0x005c9f6e)
  - caller_of_anchor_path: depth 2 (calls 0x005c9fc0 at 0x005c9f6e)
  - caller_of_anchor_path: depth 2 (calls 0x005c9fe0 at 0x005c9f6e)
- branch points:
  - none

### 0x005c9f80
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c9fc0 at 0x005c9f8e)
  - caller_of_anchor_path: depth 2 (calls 0x005c9fe0 at 0x005c9f8e)
- branch points:
  - none

### 0x005c9fa0
- blocks=1, insns=13, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005c9faf)
- branch points:
  - none

### 0x005c9fc0
- blocks=1, insns=13, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005c9fcf)
- branch points:
  - none

### 0x005c9fe0
- blocks=1, insns=13, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005c9fef)
- branch points:
  - none

### 0x005cc4a0
- blocks=4, insns=31, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005cc4bd)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005cc4dc)
- branch points:
  - 0x005cc4ab: jne -> 0x005cc4c7 (jcc_true) | ctx: 0x005cc4a3: push ecx ; 0x005cc4a4: mov dword ptr [ebp - 4], ecx ; 0x005cc4a7: cmp dword ptr [ebp + 0xc], 1 ; 0x005cc4ab: jne 0x5cc4c7
  - 0x005cc4ab: jne -> 0x005cc4ad (jcc_false) | ctx: 0x005cc4a3: push ecx ; 0x005cc4a4: mov dword ptr [ebp - 4], ecx ; 0x005cc4a7: cmp dword ptr [ebp + 0xc], 1 ; 0x005cc4ab: jne 0x5cc4c7
  - 0x005cc4c5: jmp -> 0x005cc4e4 (jmp) | ctx: 0x005cc4bc: push eax ; 0x005cc4bd: call 0x4f74f0 ; 0x005cc4c2: add esp, 8 ; 0x005cc4c5: jmp 0x5cc4e4

### 0x005cc700
- blocks=6, insns=56, edges=16, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c4cf0 at 0x005cc774)
  - caller_of_anchor_path: depth 2 (calls 0x005cc4a0 at 0x005cc768)
- branch points:
  - 0x005cc71c: ja -> 0x005cc726 (jcc_true) | ctx: 0x005cc711: mov ecx, dword ptr [0xbcf8d0] ; 0x005cc717: sub ecx, dword ptr [eax] ; 0x005cc719: cmp ecx, dword ptr [ebp + 8] ; 0x005cc71c: ja 0x5cc726
  - 0x005cc71c: ja -> 0x005cc71e (jcc_false) | ctx: 0x005cc711: mov ecx, dword ptr [0xbcf8d0] ; 0x005cc717: sub ecx, dword ptr [eax] ; 0x005cc719: cmp ecx, dword ptr [ebp + 8] ; 0x005cc71c: ja 0x5cc726
  - 0x005cc73a: jbe -> 0x005cc779 (jcc_true) | ctx: 0x005cc730: add edx, dword ptr [ebp + 8] ; 0x005cc733: mov dword ptr [ebp - 8], edx ; 0x005cc736: cmp dword ptr [ebp + 8], 0 ; 0x005cc73a: jbe 0x5cc779
  - 0x005cc73a: jbe -> 0x005cc73c (jcc_false) | ctx: 0x005cc730: add edx, dword ptr [ebp + 8] ; 0x005cc733: mov dword ptr [ebp - 8], edx ; 0x005cc736: cmp dword ptr [ebp + 8], 0 ; 0x005cc73a: jbe 0x5cc779
  - 0x005cc73a: jbe -> 0x005cc779 (jcc_true) | ctx: 0x005cc730: add edx, dword ptr [ebp + 8] ; 0x005cc733: mov dword ptr [ebp - 8], edx ; 0x005cc736: cmp dword ptr [ebp + 8], 0 ; 0x005cc73a: jbe 0x5cc779
  - 0x005cc73a: jbe -> 0x005cc73c (jcc_false) | ctx: 0x005cc730: add edx, dword ptr [ebp + 8] ; 0x005cc733: mov dword ptr [ebp - 8], edx ; 0x005cc736: cmp dword ptr [ebp + 8], 0 ; 0x005cc73a: jbe 0x5cc779
  - 0x005cc74f: je -> 0x005cc779 (jcc_true) | ctx: 0x005cc745: call 0x5c4dd0 ; 0x005cc74a: movzx ecx, al ; 0x005cc74d: test ecx, ecx ; 0x005cc74f: je 0x5cc779
  - 0x005cc74f: je -> 0x005cc751 (jcc_false) | ctx: 0x005cc745: call 0x5c4dd0 ; 0x005cc74a: movzx ecx, al ; 0x005cc74d: test ecx, ecx ; 0x005cc74f: je 0x5cc779

### 0x005cc790
- blocks=1, insns=14, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x005cc7a6)
- branch points:
  - none

### 0x005cc7c0
- blocks=1, insns=17, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c4cf0 at 0x005cc7e1)
- branch points:
  - none

### 0x005cc910
- blocks=4, insns=29, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c4cf0 at 0x005cc92d)
- branch points:
  - 0x005cc924: ja -> 0x005cc934 (jcc_true) | ctx: 0x005cc91a: call 0x5c4f40 ; 0x005cc91f: mov ecx, dword ptr [ebp + 8] ; 0x005cc922: cmp ecx, dword ptr [eax] ; 0x005cc924: ja 0x5cc934
  - 0x005cc924: ja -> 0x005cc926 (jcc_false) | ctx: 0x005cc91a: call 0x5c4f40 ; 0x005cc91f: mov ecx, dword ptr [ebp + 8] ; 0x005cc922: cmp ecx, dword ptr [eax] ; 0x005cc924: ja 0x5cc934
  - 0x005cc932: jmp -> 0x005cc94f (jmp) | ctx: 0x005cc929: push edx ; 0x005cc92a: mov ecx, dword ptr [ebp - 4] ; 0x005cc92d: call 0x5c4cf0 ; 0x005cc932: jmp 0x5cc94f

### 0x005cc960
- blocks=3, insns=54, edges=13, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fa320 at 0x005cc9a5)
- branch points:
  - 0x005cc982: je -> 0x005cc9ea (jcc_true) | ctx: 0x005cc979: mov dword ptr [ebp - 0x10], ecx ; 0x005cc97c: mov eax, dword ptr [ebp - 0x10] ; 0x005cc97f: cmp eax, dword ptr [ebp + 8] ; 0x005cc982: je 0x5cc9ea
  - 0x005cc982: je -> 0x005cc984 (jcc_false) | ctx: 0x005cc979: mov dword ptr [ebp - 0x10], ecx ; 0x005cc97c: mov eax, dword ptr [ebp - 0x10] ; 0x005cc97f: cmp eax, dword ptr [ebp + 8] ; 0x005cc982: je 0x5cc9ea

### 0x005cdc30
- blocks=1, insns=24, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005cdc63)
- branch points:
  - none

### 0x005cf520
- blocks=1, insns=14, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005cf532)
- branch points:
  - none

### 0x005d1470
- blocks=1, insns=21, edges=4, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005d1499)
- branch points:
  - none

### 0x005d8440
- blocks=1, insns=15, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005d8457)
- branch points:
  - none

### 0x005d8a20
- blocks=7, insns=92, edges=28, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c4cf0 at 0x005d8acf)
- branch points:
  - 0x005d8a2f: jne -> 0x005d8a36 (jcc_true) | ctx: 0x005d8a26: mov dword ptr [ebp - 4], ecx ; 0x005d8a29: movzx eax, byte ptr [ebp + 8] ; 0x005d8a2d: test eax, eax ; 0x005d8a2f: jne 0x5d8a36
  - 0x005d8a2f: jne -> 0x005d8a31 (jcc_false) | ctx: 0x005d8a26: mov dword ptr [ebp - 4], ecx ; 0x005d8a29: movzx eax, byte ptr [ebp + 8] ; 0x005d8a2d: test eax, eax ; 0x005d8a2f: jne 0x5d8a36
  - 0x005d8a41: jb -> 0x005d8aba (jcc_true) | ctx: 0x005d8a36: mov ecx, dword ptr [ebp - 4] ; 0x005d8a39: call 0x5d84f0 ; 0x005d8a3e: cmp dword ptr [eax], 0x10 ; 0x005d8a41: jb 0x5d8aba
  - 0x005d8a41: jb -> 0x005d8a43 (jcc_false) | ctx: 0x005d8a36: mov ecx, dword ptr [ebp - 4] ; 0x005d8a39: call 0x5d84f0 ; 0x005d8a3e: cmp dword ptr [eax], 0x10 ; 0x005d8a41: jb 0x5d8aba
  - 0x005d8a31: jmp -> 0x005d8aba (jmp) | ctx: 0x005d8a31: jmp 0x5d8aba
  - 0x005d8a75: jbe -> 0x005d8a99 (jcc_true) | ctx: 0x005d8a6a: mov ecx, eax ; 0x005d8a6c: call 0x5d5500 ; 0x005d8a71: cmp dword ptr [ebp + 0xc], 0 ; 0x005d8a75: jbe 0x5d8a99
  - 0x005d8a75: jbe -> 0x005d8a77 (jcc_false) | ctx: 0x005d8a6a: mov ecx, eax ; 0x005d8a6c: call 0x5d5500 ; 0x005d8a71: cmp dword ptr [ebp + 0xc], 0 ; 0x005d8a75: jbe 0x5d8a99

### 0x005d9450
- blocks=1, insns=24, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005d9483)
- branch points:
  - none

### 0x005d9940
- blocks=1, insns=24, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005d9973)
- branch points:
  - none

### 0x005db460
- blocks=1, insns=18, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005db480)
- branch points:
  - none

### 0x005e45d0
- blocks=3, insns=46, edges=8, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fac10 at 0x005e460b)
- branch points:
  - 0x005e4638: jmp -> 0x005e4657 (jmp) | ctx: 0x005e462f: push eax ; 0x005e4630: lea ecx, [ebp - 0x11] ; 0x005e4633: call 0x5eb8a0 ; 0x005e4638: jmp 0x5e4657
  - 0x005e465e: jmp -> 0x005e4667 (jmp) | ctx: 0x005e4657: mov dword ptr [ebp - 4], 0xffffffff ; 0x005e465e: jmp 0x5e4667

### 0x005e8560
- blocks=3, insns=45, edges=6, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fac10 at 0x005e858a)
- branch points:
  - 0x005e85b6: jmp -> 0x005e85d5 (jmp) | ctx: 0x005e85ad: push edx ; 0x005e85ae: mov ecx, dword ptr [ebp + 0x14] ; 0x005e85b1: call 0x5eba60 ; 0x005e85b6: jmp 0x5e85d5
  - 0x005e85dc: jmp -> 0x005e85e5 (jmp) | ctx: 0x005e85d5: mov dword ptr [ebp - 4], 0xffffffff ; 0x005e85dc: jmp 0x5e85e5

### 0x005efbf0
- blocks=1, insns=46, edges=6, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x005efc6a)
- branch points:
  - none

### 0x005f4990
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fac30 at 0x005f499d)
- branch points:
  - none

### 0x005f5830
- blocks=1, insns=43, edges=10, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fa320 at 0x005f583f)
- branch points:
  - none

### 0x005fa320
- blocks=1, insns=14, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005fa33a)
- branch points:
  - none

### 0x005fabd0
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fac10 at 0x005fabde)
  - caller_of_anchor_path: depth 2 (calls 0x005fac30 at 0x005fabde)
- branch points:
  - none

### 0x005fabf0
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fac10 at 0x005fabfe)
  - caller_of_anchor_path: depth 2 (calls 0x005fac30 at 0x005fabfe)
- branch points:
  - none

### 0x005fac10
- blocks=1, insns=13, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005fac22)
- branch points:
  - none

### 0x005fac30
- blocks=1, insns=13, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005fac3f)
- branch points:
  - none

### 0x005fb1b0
- blocks=1, insns=24, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005a1700 at 0x005fb1e3)
- branch points:
  - none

### 0x005fd2e1
- blocks=8, insns=30, edges=12, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005fd2ea)
- branch points:
  - 0x005fd2f7: jne -> 0x005fd2ff (jcc_true) | ctx: 0x005fd2ef: mov ecx, dword ptr [ebp + 8] ; 0x005fd2f2: add esp, 0xc ; 0x005fd2f5: test ecx, ecx ; 0x005fd2f7: jne 0x5fd2ff
  - 0x005fd2f7: jne -> 0x005fd2f9 (jcc_false) | ctx: 0x005fd2ef: mov ecx, dword ptr [ebp + 8] ; 0x005fd2f2: add esp, 0xc ; 0x005fd2f5: test ecx, ecx ; 0x005fd2f7: jne 0x5fd2ff
  - 0x005fd304: je -> 0x005fd308 (jcc_true) | ctx: 0x005fd2ff: mov edx, dword ptr [ebp + 0xc] ; 0x005fd302: test eax, eax ; 0x005fd304: je 0x5fd308
  - 0x005fd304: je -> 0x005fd306 (jcc_false) | ctx: 0x005fd2ff: mov edx, dword ptr [ebp + 0xc] ; 0x005fd302: test eax, eax ; 0x005fd304: je 0x5fd308
  - 0x005fd2fd: jmp -> 0x005fd302 (jmp) | ctx: 0x005fd2f9: mov ecx, eax ; 0x005fd2fb: mov edx, eax ; 0x005fd2fd: jmp 0x5fd302
  - 0x005fd30d: je -> 0x005fd311 (jcc_true) | ctx: 0x005fd308: lea ecx, [eax + 4] ; 0x005fd30b: test ecx, ecx ; 0x005fd30d: je 0x5fd311
  - 0x005fd30d: je -> 0x005fd30f (jcc_false) | ctx: 0x005fd308: lea ecx, [eax + 4] ; 0x005fd30b: test ecx, ecx ; 0x005fd30d: je 0x5fd311
  - 0x005fd30d: je -> 0x005fd311 (jcc_true) | ctx: 0x005fd306: mov dword ptr [eax], ecx ; 0x005fd308: lea ecx, [eax + 4] ; 0x005fd30b: test ecx, ecx ; 0x005fd30d: je 0x5fd311
  - 0x005fd30d: je -> 0x005fd30f (jcc_false) | ctx: 0x005fd306: mov dword ptr [eax], ecx ; 0x005fd308: lea ecx, [eax + 4] ; 0x005fd30b: test ecx, ecx ; 0x005fd30d: je 0x5fd311
  - 0x005fd304: je -> 0x005fd308 (jcc_true) | ctx: 0x005fd302: test eax, eax ; 0x005fd304: je 0x5fd308
  - 0x005fd304: je -> 0x005fd306 (jcc_false) | ctx: 0x005fd302: test eax, eax ; 0x005fd304: je 0x5fd308

### 0x005fd315
- blocks=1, insns=38, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x005fd3d8)
- branch points:
  - none

### 0x005fd587
- blocks=3, insns=20, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fd2e1 at 0x005fd591)
- branch points:
  - 0x005fd59b: je -> 0x005fd5aa (jcc_true) | ctx: 0x005fd591: call 0x5fd2e1 ; 0x005fd596: lea esi, [eax + 8] ; 0x005fd599: test esi, esi ; 0x005fd59b: je 0x5fd5aa
  - 0x005fd59b: je -> 0x005fd59d (jcc_false) | ctx: 0x005fd591: call 0x5fd2e1 ; 0x005fd596: lea esi, [eax + 8] ; 0x005fd599: test esi, esi ; 0x005fd59b: je 0x5fd5aa

### 0x005fd6e4
- blocks=1, insns=33, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fd2e1 at 0x005fd6ff)
  - caller_of_anchor_path: depth 2 (calls 0x005fd315 at 0x005fd720)
- branch points:
  - none

### 0x005fdc00
- blocks=7, insns=37, edges=12, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fd315 at 0x005fdc30)
- branch points:
  - 0x005fdc13: jbe -> 0x005fdc3c (jcc_true) | ctx: 0x005fdc08: fstp dword ptr [ebp - 4] ; 0x005fdc0b: movss xmm0, dword ptr [ebp - 4] ; 0x005fdc10: comiss xmm0, dword ptr [esi] ; 0x005fdc13: jbe 0x5fdc3c
  - 0x005fdc13: jbe -> 0x005fdc15 (jcc_false) | ctx: 0x005fdc08: fstp dword ptr [ebp - 4] ; 0x005fdc0b: movss xmm0, dword ptr [ebp - 4] ; 0x005fdc10: comiss xmm0, dword ptr [esi] ; 0x005fdc13: jbe 0x5fdc3c
  - 0x005fdc1d: jae -> 0x005fdc24 (jcc_true) | ctx: 0x005fdc15: mov eax, dword ptr [esi + 0x1c] ; 0x005fdc18: cmp eax, 0x200 ; 0x005fdc1d: jae 0x5fdc24
  - 0x005fdc1d: jae -> 0x005fdc1f (jcc_false) | ctx: 0x005fdc15: mov eax, dword ptr [esi + 0x1c] ; 0x005fdc18: cmp eax, 0x200 ; 0x005fdc1d: jae 0x5fdc24
  - 0x005fdc29: jae -> 0x005fdc2d (jcc_true) | ctx: 0x005fdc24: cmp eax, 0x1fffffff ; 0x005fdc29: jae 0x5fdc2d
  - 0x005fdc29: jae -> 0x005fdc2b (jcc_false) | ctx: 0x005fdc24: cmp eax, 0x1fffffff ; 0x005fdc29: jae 0x5fdc2d
  - 0x005fdc22: jmp -> 0x005fdc2d (jmp) | ctx: 0x005fdc1f: shl eax, 3 ; 0x005fdc22: jmp 0x5fdc2d

### 0x005fdcf8
- blocks=7, insns=49, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fd315 at 0x005fdd1a)
- branch points:
  - 0x005fdd05: jne -> 0x005fdd2a (jcc_true) | ctx: 0x005fdcfe: mov edx, dword ptr [esi] ; 0x005fdd00: cmp eax, dword ptr [edx] ; 0x005fdd02: mov edx, dword ptr [ebp + 0x10] ; 0x005fdd05: jne 0x5fdd2a
  - 0x005fdd05: jne -> 0x005fdd07 (jcc_false) | ctx: 0x005fdcfe: mov edx, dword ptr [esi] ; 0x005fdd00: cmp eax, dword ptr [edx] ; 0x005fdd02: mov edx, dword ptr [ebp + 0x10] ; 0x005fdd05: jne 0x5fdd2a
  - 0x005fdd2c: je -> 0x005fdd47 (jcc_true) | ctx: 0x005fdd2a: cmp eax, edx ; 0x005fdd2c: je 0x5fdd47
  - 0x005fdd2c: je -> 0x005fdd2e (jcc_false) | ctx: 0x005fdd2a: cmp eax, edx ; 0x005fdd2c: je 0x5fdd47
  - 0x005fdd09: jne -> 0x005fdd2a (jcc_true) | ctx: 0x005fdd07: cmp edx, dword ptr [esi] ; 0x005fdd09: jne 0x5fdd2a
  - 0x005fdd09: jne -> 0x005fdd0b (jcc_false) | ctx: 0x005fdd07: cmp edx, dword ptr [esi] ; 0x005fdd09: jne 0x5fdd2a
  - 0x005fdd45: jne -> 0x005fdd2e (jcc_true) | ctx: 0x005fdd3a: call 0x5fdd60 ; 0x005fdd3f: mov eax, dword ptr [ebp + 0xc] ; 0x005fdd42: cmp eax, dword ptr [ebp + 0x10] ; 0x005fdd45: jne 0x5fdd2e
  - 0x005fdd45: jne -> 0x005fdd47 (jcc_false) | ctx: 0x005fdd3a: call 0x5fdd60 ; 0x005fdd3f: mov eax, dword ptr [ebp + 0xc] ; 0x005fdd42: cmp eax, dword ptr [ebp + 0x10] ; 0x005fdd45: jne 0x5fdd2e
  - 0x005fdd28: jmp -> 0x005fdd4e (jmp) | ctx: 0x005fdd21: mov ecx, dword ptr [eax] ; 0x005fdd23: mov eax, dword ptr [ebp + 8] ; 0x005fdd26: mov dword ptr [eax], ecx ; 0x005fdd28: jmp 0x5fdd4e

### 0x005fe82a
- blocks=1, insns=106, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x005fe95a)
- branch points:
  - none

### 0x00604488
- blocks=1, insns=18, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0060449b)
- branch points:
  - none

### 0x00605cc4
- blocks=7, insns=65, edges=19, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00607853 at 0x00605db4)
- branch points:
  - 0x00605cf3: je -> 0x00605d10 (jcc_true) | ctx: 0x00605ce7: call dword ptr [0xbb93a0] ; 0x00605ced: add esp, 0x18 ; 0x00605cf0: cmp eax, 5 ; 0x00605cf3: je 0x605d10
  - 0x00605cf3: je -> 0x00605cf5 (jcc_false) | ctx: 0x00605ce7: call dword ptr [0xbb93a0] ; 0x00605ced: add esp, 0x18 ; 0x00605cf0: cmp eax, 5 ; 0x00605cf3: je 0x605d10
  - 0x00605d2e: je -> 0x00605d41 (jcc_true) | ctx: 0x00605d22: call dword ptr [0xbb93a0] ; 0x00605d28: add esp, 0x18 ; 0x00605d2b: cmp eax, 6 ; 0x00605d2e: je 0x605d41
  - 0x00605d2e: je -> 0x00605d30 (jcc_false) | ctx: 0x00605d22: call dword ptr [0xbb93a0] ; 0x00605d28: add esp, 0x18 ; 0x00605d2b: cmp eax, 6 ; 0x00605d2e: je 0x605d41
  - 0x00605d0e: jmp -> 0x00605d5c (jmp) | ctx: 0x00605d01: push 0xbd3094 ; 0x00605d06: call 0x4f7350 ; 0x00605d0b: add esp, 0x10 ; 0x00605d0e: jmp 0x605d5c
  - 0x00605d52: je -> 0x00605d5c (jcc_true) | ctx: 0x00605d47: call dword ptr [0xbb93bc] ; 0x00605d4d: add esp, 0x10 ; 0x00605d50: test eax, eax ; 0x00605d52: je 0x605d5c
  - 0x00605d52: je -> 0x00605d54 (jcc_false) | ctx: 0x00605d47: call dword ptr [0xbb93bc] ; 0x00605d4d: add esp, 0x10 ; 0x00605d50: test eax, eax ; 0x00605d52: je 0x605d5c
  - 0x00605d3f: jmp -> 0x00605d5c (jmp) | ctx: 0x00605d38: call 0x4f7350 ; 0x00605d3d: pop ecx ; 0x00605d3e: pop ecx ; 0x00605d3f: jmp 0x605d5c

### 0x00606b46
- blocks=5, insns=48, edges=14, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00607853 at 0x00606b76)
- branch points:
  - 0x00606b56: je -> 0x00606b71 (jcc_true) | ctx: 0x00606b4d: call 0x604916 ; 0x00606b52: mov edi, eax ; 0x00606b54: test edi, edi ; 0x00606b56: je 0x606b71
  - 0x00606b56: je -> 0x00606b58 (jcc_false) | ctx: 0x00606b4d: call 0x604916 ; 0x00606b52: mov edi, eax ; 0x00606b54: test edi, edi ; 0x00606b56: je 0x606b71
  - 0x00606b5d: je -> 0x00606b68 (jcc_true) | ctx: 0x00606b58: mov eax, dword ptr [edi + 8] ; 0x00606b5b: test eax, eax ; 0x00606b5d: je 0x606b68
  - 0x00606b5d: je -> 0x00606b5f (jcc_false) | ctx: 0x00606b58: mov eax, dword ptr [edi + 8] ; 0x00606b5b: test eax, eax ; 0x00606b5d: je 0x606b68

### 0x00607853
- blocks=3, insns=13, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00607876)
- branch points:
  - 0x00607862: je -> 0x00607869 (jcc_true) | ctx: 0x00607859: call dword ptr [0xbb9448] ; 0x0060785f: pop ecx ; 0x00607860: test eax, eax ; 0x00607862: je 0x607869
  - 0x00607862: je -> 0x00607864 (jcc_false) | ctx: 0x00607859: call dword ptr [0xbb9448] ; 0x0060785f: pop ecx ; 0x00607860: test eax, eax ; 0x00607862: je 0x607869

### 0x0060ad20
- blocks=1, insns=23, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0060ad6f)
- branch points:
  - none

### 0x0060ae05
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0060ad20 at 0x0060ae35)
- branch points:
  - 0x0060ae1c: jae -> 0x0060ae42 (jcc_true) | ctx: 0x0060ae15: idiv ebx ; 0x0060ae17: mov edi, dword ptr [ebp + 8] ; 0x0060ae1a: cmp eax, edi ; 0x0060ae1c: jae 0x60ae42
  - 0x0060ae1c: jae -> 0x0060ae1e (jcc_false) | ctx: 0x0060ae15: idiv ebx ; 0x0060ae17: mov edi, dword ptr [ebp + 8] ; 0x0060ae1a: cmp eax, edi ; 0x0060ae1c: jae 0x60ae42
  - 0x0060ae2e: jb -> 0x0060ae49 (jcc_true) | ctx: 0x0060ae28: idiv ebx ; 0x0060ae2a: sub ecx, eax ; 0x0060ae2c: cmp ecx, edi ; 0x0060ae2e: jb 0x60ae49
  - 0x0060ae2e: jb -> 0x0060ae30 (jcc_false) | ctx: 0x0060ae28: idiv ebx ; 0x0060ae2a: sub ecx, eax ; 0x0060ae2c: cmp ecx, edi ; 0x0060ae2e: jb 0x60ae49

### 0x0060b776
- blocks=4, insns=52, edges=9, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0060b8f9)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0060b99a)
  - caller_of_anchor_path: depth 2 (calls 0x0060b776 at 0x0060b87f)
- branch points:
  - 0x0060b796: jg -> 0x0060b7a1 (jcc_true) | ctx: 0x0060b788: mov ecx, dword ptr [eax + ecx*4] ; 0x0060b78b: mov eax, dword ptr [0xf54ef8] ; 0x0060b790: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0060b796: jg 0x60b7a1
  - 0x0060b796: jg -> 0x0060b798 (jcc_false) | ctx: 0x0060b788: mov ecx, dword ptr [eax + ecx*4] ; 0x0060b78b: mov eax, dword ptr [0xf54ef8] ; 0x0060b790: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0060b796: jg 0x60b7a1
  - 0x0060b7b3: jne -> 0x0060b798 (jcc_true) | ctx: 0x0060b7a6: call 0xab6ba9 ; 0x0060b7ab: cmp dword ptr [0xf54ef8], -1 ; 0x0060b7b2: pop ecx ; 0x0060b7b3: jne 0x60b798
  - 0x0060b7b3: jne -> 0x0060b7b5 (jcc_false) | ctx: 0x0060b7a6: call 0xab6ba9 ; 0x0060b7ab: cmp dword ptr [0xf54ef8], -1 ; 0x0060b7b2: pop ecx ; 0x0060b7b3: jne 0x60b798
  - 0x0060b82e: jmp -> 0x0060b798 (jmp) | ctx: 0x0060b82b: pop edi ; 0x0060b82c: pop esi ; 0x0060b82d: pop ebx ; 0x0060b82e: jmp 0x60b798

### 0x0060ba28
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0061e633 at 0x0060ba58)
- branch points:
  - 0x0060ba3f: jae -> 0x0060ba65 (jcc_true) | ctx: 0x0060ba38: idiv ebx ; 0x0060ba3a: mov edi, dword ptr [ebp + 8] ; 0x0060ba3d: cmp eax, edi ; 0x0060ba3f: jae 0x60ba65
  - 0x0060ba3f: jae -> 0x0060ba41 (jcc_false) | ctx: 0x0060ba38: idiv ebx ; 0x0060ba3a: mov edi, dword ptr [ebp + 8] ; 0x0060ba3d: cmp eax, edi ; 0x0060ba3f: jae 0x60ba65
  - 0x0060ba51: jb -> 0x0060ba6c (jcc_true) | ctx: 0x0060ba4b: idiv ebx ; 0x0060ba4d: sub ecx, eax ; 0x0060ba4f: cmp ecx, edi ; 0x0060ba51: jb 0x60ba6c
  - 0x0060ba51: jb -> 0x0060ba53 (jcc_false) | ctx: 0x0060ba4b: idiv ebx ; 0x0060ba4d: sub ecx, eax ; 0x0060ba4f: cmp ecx, edi ; 0x0060ba51: jb 0x60ba6c

### 0x0060cf7e
- blocks=1, insns=21, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0060d112 at 0x0060cfb8)
- branch points:
  - none

### 0x0060d008
- blocks=12, insns=123, edges=26, jcc=7, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0060d04d)
- branch points:
  - 0x0060d023: jb -> 0x0060d02a (jcc_true) | ctx: 0x0060d01c: mov eax, edi ; 0x0060d01e: sub eax, ecx ; 0x0060d020: cmp eax, dword ptr [ebp + 8] ; 0x0060d023: jb 0x60d02a
  - 0x0060d023: jb -> 0x0060d025 (jcc_false) | ctx: 0x0060d01c: mov eax, edi ; 0x0060d01e: sub eax, ecx ; 0x0060d020: cmp eax, dword ptr [ebp + 8] ; 0x0060d023: jb 0x60d02a
  - 0x0060d033: jb -> 0x0060d107 (jcc_true) | ctx: 0x0060d02a: mov eax, 0xaaaaaaa ; 0x0060d02f: sub eax, edi ; 0x0060d031: cmp eax, edi ; 0x0060d033: jb 0x60d107
  - 0x0060d033: jb -> 0x0060d039 (jcc_false) | ctx: 0x0060d02a: mov eax, 0xaaaaaaa ; 0x0060d02f: sub eax, edi ; 0x0060d031: cmp eax, edi ; 0x0060d033: jb 0x60d107
  - 0x0060d028: jae -> 0x0060d03d (jcc_true) | ctx: 0x0060d025: cmp edi, 8 ; 0x0060d028: jae 0x60d03d
  - 0x0060d028: jae -> 0x0060d02a (jcc_false) | ctx: 0x0060d025: cmp edi, 8 ; 0x0060d028: jae 0x60d03d
  - 0x0060d03b: jmp -> 0x0060d01c (jmp) | ctx: 0x0060d039: add edi, edi ; 0x0060d03b: jmp 0x60d01c
  - 0x0060d079: ja -> 0x0060d0ac (jcc_true) | ctx: 0x0060d073: add esp, 0x18 ; 0x0060d076: push eax ; 0x0060d077: cmp ecx, edi ; 0x0060d079: ja 0x60d0ac
  - 0x0060d079: ja -> 0x0060d07b (jcc_false) | ctx: 0x0060d073: add esp, 0x18 ; 0x0060d076: push eax ; 0x0060d077: cmp ecx, edi ; 0x0060d079: ja 0x60d0ac
  - 0x0060d023: jb -> 0x0060d02a (jcc_true) | ctx: 0x0060d01c: mov eax, edi ; 0x0060d01e: sub eax, ecx ; 0x0060d020: cmp eax, dword ptr [ebp + 8] ; 0x0060d023: jb 0x60d02a
  - 0x0060d023: jb -> 0x0060d025 (jcc_false) | ctx: 0x0060d01c: mov eax, edi ; 0x0060d01e: sub eax, ecx ; 0x0060d020: cmp eax, dword ptr [ebp + 8] ; 0x0060d023: jb 0x60d02a
  - 0x0060d0e6: je -> 0x0060d0f8 (jcc_true) | ctx: 0x0060d0dc: mov esi, dword ptr [ebp - 4] ; 0x0060d0df: add esp, 0x24 ; 0x0060d0e2: cmp dword ptr [ebx + 4], 0 ; 0x0060d0e6: je 0x60d0f8
  - 0x0060d0e6: je -> 0x0060d0e8 (jcc_false) | ctx: 0x0060d0dc: mov esi, dword ptr [ebp - 4] ; 0x0060d0df: add esp, 0x24 ; 0x0060d0e2: cmp dword ptr [ebx + 4], 0 ; 0x0060d0e6: je 0x60d0f8
  - 0x0060d0aa: jmp -> 0x0060d0df (jmp) | ctx: 0x0060d0a2: push 0 ; 0x0060d0a4: push esi ; 0x0060d0a5: call 0xacf2c0 ; 0x0060d0aa: jmp 0x60d0df
  - 0x0060d0e6: je -> 0x0060d0f8 (jcc_true) | ctx: 0x0060d0df: add esp, 0x24 ; 0x0060d0e2: cmp dword ptr [ebx + 4], 0 ; 0x0060d0e6: je 0x60d0f8
  - 0x0060d0e6: je -> 0x0060d0e8 (jcc_false) | ctx: 0x0060d0df: add esp, 0x24 ; 0x0060d0e2: cmp dword ptr [ebx + 4], 0 ; 0x0060d0e6: je 0x60d0f8

### 0x0060d112
- blocks=7, insns=65, edges=12, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0060d14c)
  - caller_of_anchor_path: depth 2 (calls 0x0060d008 at 0x0060d125)
- branch points:
  - 0x0060d121: ja -> 0x0060d12a (jcc_true) | ctx: 0x0060d11a: mov eax, dword ptr [ebx + 0x10] ; 0x0060d11d: inc eax ; 0x0060d11e: cmp dword ptr [ebx + 8], eax ; 0x0060d121: ja 0x60d12a
  - 0x0060d121: ja -> 0x0060d123 (jcc_false) | ctx: 0x0060d11a: mov eax, dword ptr [ebx + 0x10] ; 0x0060d11d: inc eax ; 0x0060d11e: cmp dword ptr [ebx + 8], eax ; 0x0060d121: ja 0x60d12a
  - 0x0060d144: jne -> 0x0060d15a (jcc_true) | ctx: 0x0060d13b: and esi, eax ; 0x0060d13d: mov eax, dword ptr [ebx + 4] ; 0x0060d140: cmp dword ptr [eax + esi*4], 0 ; 0x0060d144: jne 0x60d15a
  - 0x0060d144: jne -> 0x0060d146 (jcc_false) | ctx: 0x0060d13b: and esi, eax ; 0x0060d13d: mov eax, dword ptr [ebx + 4] ; 0x0060d140: cmp dword ptr [eax + esi*4], 0 ; 0x0060d144: jne 0x60d15a
  - 0x0060d144: jne -> 0x0060d15a (jcc_true) | ctx: 0x0060d13b: and esi, eax ; 0x0060d13d: mov eax, dword ptr [ebx + 4] ; 0x0060d140: cmp dword ptr [eax + esi*4], 0 ; 0x0060d144: jne 0x60d15a
  - 0x0060d144: jne -> 0x0060d146 (jcc_false) | ctx: 0x0060d13b: and esi, eax ; 0x0060d13d: mov eax, dword ptr [ebx + 4] ; 0x0060d140: cmp dword ptr [eax + esi*4], 0 ; 0x0060d144: jne 0x60d15a
  - 0x0060d162: je -> 0x0060d16c (jcc_true) | ctx: 0x0060d15a: mov eax, dword ptr [ebx + 4] ; 0x0060d15d: mov edi, dword ptr [eax + esi*4] ; 0x0060d160: test edi, edi ; 0x0060d162: je 0x60d16c
  - 0x0060d162: je -> 0x0060d164 (jcc_false) | ctx: 0x0060d15a: mov eax, dword ptr [ebx + 4] ; 0x0060d15d: mov edi, dword ptr [eax + esi*4] ; 0x0060d160: test edi, edi ; 0x0060d162: je 0x60d16c
  - 0x0060d162: je -> 0x0060d16c (jcc_true) | ctx: 0x0060d15a: mov eax, dword ptr [ebx + 4] ; 0x0060d15d: mov edi, dword ptr [eax + esi*4] ; 0x0060d160: test edi, edi ; 0x0060d162: je 0x60d16c
  - 0x0060d162: je -> 0x0060d164 (jcc_false) | ctx: 0x0060d15a: mov eax, dword ptr [ebx + 4] ; 0x0060d15d: mov edi, dword ptr [eax + esi*4] ; 0x0060d160: test edi, edi ; 0x0060d162: je 0x60d16c

### 0x0060f9df
- blocks=7, insns=37, edges=12, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fd315 at 0x0060fa0f)
- branch points:
  - 0x0060f9f2: jbe -> 0x0060fa1b (jcc_true) | ctx: 0x0060f9e7: fstp dword ptr [ebp - 4] ; 0x0060f9ea: movss xmm0, dword ptr [ebp - 4] ; 0x0060f9ef: comiss xmm0, dword ptr [esi] ; 0x0060f9f2: jbe 0x60fa1b
  - 0x0060f9f2: jbe -> 0x0060f9f4 (jcc_false) | ctx: 0x0060f9e7: fstp dword ptr [ebp - 4] ; 0x0060f9ea: movss xmm0, dword ptr [ebp - 4] ; 0x0060f9ef: comiss xmm0, dword ptr [esi] ; 0x0060f9f2: jbe 0x60fa1b
  - 0x0060f9fc: jae -> 0x0060fa03 (jcc_true) | ctx: 0x0060f9f4: mov eax, dword ptr [esi + 0x1c] ; 0x0060f9f7: cmp eax, 0x200 ; 0x0060f9fc: jae 0x60fa03
  - 0x0060f9fc: jae -> 0x0060f9fe (jcc_false) | ctx: 0x0060f9f4: mov eax, dword ptr [esi + 0x1c] ; 0x0060f9f7: cmp eax, 0x200 ; 0x0060f9fc: jae 0x60fa03
  - 0x0060fa08: jae -> 0x0060fa0c (jcc_true) | ctx: 0x0060fa03: cmp eax, 0x1fffffff ; 0x0060fa08: jae 0x60fa0c
  - 0x0060fa08: jae -> 0x0060fa0a (jcc_false) | ctx: 0x0060fa03: cmp eax, 0x1fffffff ; 0x0060fa08: jae 0x60fa0c
  - 0x0060fa01: jmp -> 0x0060fa0c (jmp) | ctx: 0x0060f9fe: shl eax, 3 ; 0x0060fa01: jmp 0x60fa0c

### 0x0060faf6
- blocks=7, insns=49, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fd315 at 0x0060fb18)
- branch points:
  - 0x0060fb03: jne -> 0x0060fb28 (jcc_true) | ctx: 0x0060fafc: mov edx, dword ptr [esi] ; 0x0060fafe: cmp eax, dword ptr [edx] ; 0x0060fb00: mov edx, dword ptr [ebp + 0x10] ; 0x0060fb03: jne 0x60fb28
  - 0x0060fb03: jne -> 0x0060fb05 (jcc_false) | ctx: 0x0060fafc: mov edx, dword ptr [esi] ; 0x0060fafe: cmp eax, dword ptr [edx] ; 0x0060fb00: mov edx, dword ptr [ebp + 0x10] ; 0x0060fb03: jne 0x60fb28
  - 0x0060fb2a: je -> 0x0060fb45 (jcc_true) | ctx: 0x0060fb28: cmp eax, edx ; 0x0060fb2a: je 0x60fb45
  - 0x0060fb2a: je -> 0x0060fb2c (jcc_false) | ctx: 0x0060fb28: cmp eax, edx ; 0x0060fb2a: je 0x60fb45
  - 0x0060fb07: jne -> 0x0060fb28 (jcc_true) | ctx: 0x0060fb05: cmp edx, dword ptr [esi] ; 0x0060fb07: jne 0x60fb28
  - 0x0060fb07: jne -> 0x0060fb09 (jcc_false) | ctx: 0x0060fb05: cmp edx, dword ptr [esi] ; 0x0060fb07: jne 0x60fb28
  - 0x0060fb43: jne -> 0x0060fb2c (jcc_true) | ctx: 0x0060fb38: call 0x60fb5e ; 0x0060fb3d: mov eax, dword ptr [ebp + 0xc] ; 0x0060fb40: cmp eax, dword ptr [ebp + 0x10] ; 0x0060fb43: jne 0x60fb2c
  - 0x0060fb43: jne -> 0x0060fb45 (jcc_false) | ctx: 0x0060fb38: call 0x60fb5e ; 0x0060fb3d: mov eax, dword ptr [ebp + 0xc] ; 0x0060fb40: cmp eax, dword ptr [ebp + 0x10] ; 0x0060fb43: jne 0x60fb2c
  - 0x0060fb26: jmp -> 0x0060fb4c (jmp) | ctx: 0x0060fb1f: mov ecx, dword ptr [eax] ; 0x0060fb21: mov eax, dword ptr [ebp + 8] ; 0x0060fb24: mov dword ptr [eax], ecx ; 0x0060fb26: jmp 0x60fb4c

### 0x0060fe9c
- blocks=1, insns=33, edges=2, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0060feb7)
  - caller_of_anchor_path: depth 2 (calls 0x005fd315 at 0x0060fed8)
- branch points:
  - none

### 0x00611570
- blocks=1, insns=23, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006115c2)
- branch points:
  - none

### 0x00611669
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00611570 at 0x00611699)
- branch points:
  - 0x00611680: jae -> 0x006116a6 (jcc_true) | ctx: 0x00611679: idiv ebx ; 0x0061167b: mov edi, dword ptr [ebp + 8] ; 0x0061167e: cmp eax, edi ; 0x00611680: jae 0x6116a6
  - 0x00611680: jae -> 0x00611682 (jcc_false) | ctx: 0x00611679: idiv ebx ; 0x0061167b: mov edi, dword ptr [ebp + 8] ; 0x0061167e: cmp eax, edi ; 0x00611680: jae 0x6116a6
  - 0x00611692: jb -> 0x006116ad (jcc_true) | ctx: 0x0061168c: idiv ebx ; 0x0061168e: sub ecx, eax ; 0x00611690: cmp ecx, edi ; 0x00611692: jb 0x6116ad
  - 0x00611692: jb -> 0x00611694 (jcc_false) | ctx: 0x0061168c: idiv ebx ; 0x0061168e: sub ecx, eax ; 0x00611690: cmp ecx, edi ; 0x00611692: jb 0x6116ad

### 0x00611e48
- blocks=1, insns=19, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00611e92)
- branch points:
  - none

### 0x00611f33
- blocks=5, insns=31, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00611e48 at 0x00611f5e)
- branch points:
  - 0x00611f46: jae -> 0x00611f6b (jcc_true) | ctx: 0x00611f3f: sub eax, edx ; 0x00611f41: sar eax, 6 ; 0x00611f44: cmp eax, ecx ; 0x00611f46: jae 0x611f6b
  - 0x00611f46: jae -> 0x00611f48 (jcc_false) | ctx: 0x00611f3f: sub eax, edx ; 0x00611f41: sar eax, 6 ; 0x00611f44: cmp eax, ecx ; 0x00611f46: jae 0x611f6b
  - 0x00611f56: jb -> 0x00611f70 (jcc_true) | ctx: 0x00611f4f: sar edx, 6 ; 0x00611f52: sub eax, edx ; 0x00611f54: cmp eax, ecx ; 0x00611f56: jb 0x611f70
  - 0x00611f56: jb -> 0x00611f58 (jcc_false) | ctx: 0x00611f4f: sar edx, 6 ; 0x00611f52: sub eax, edx ; 0x00611f54: cmp eax, ecx ; 0x00611f56: jb 0x611f70

### 0x00613d09
- blocks=6, insns=53, edges=12, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0061c64c at 0x00613d41)
- branch points:
  - 0x00613d1a: je -> 0x00613d62 (jcc_true) | ctx: 0x00613d13: mov eax, dword ptr [ebx] ; 0x00613d15: mov ecx, dword ptr [eax + 0x64] ; 0x00613d18: test ecx, ecx ; 0x00613d1a: je 0x613d62
  - 0x00613d1a: je -> 0x00613d1c (jcc_false) | ctx: 0x00613d13: mov eax, dword ptr [ebx] ; 0x00613d15: mov ecx, dword ptr [eax + 0x64] ; 0x00613d18: test ecx, ecx ; 0x00613d1a: je 0x613d62
  - 0x00613d2e: je -> 0x00613d61 (jcc_true) | ctx: 0x00613d25: mov ecx, esi ; 0x00613d27: call 0x6160ce ; 0x00613d2c: test al, al ; 0x00613d2e: je 0x613d61
  - 0x00613d2e: je -> 0x00613d30 (jcc_false) | ctx: 0x00613d25: mov ecx, esi ; 0x00613d27: call 0x6160ce ; 0x00613d2c: test al, al ; 0x00613d2e: je 0x613d61
  - 0x00613d56: jbe -> 0x00613d61 (jcc_true) | ctx: 0x00613d4b: mulss xmm0, xmm0 ; 0x00613d4f: fstp dword ptr [ebp - 4] ; 0x00613d52: comiss xmm0, dword ptr [ebp - 4] ; 0x00613d56: jbe 0x613d61
  - 0x00613d56: jbe -> 0x00613d58 (jcc_false) | ctx: 0x00613d4b: mulss xmm0, xmm0 ; 0x00613d4f: fstp dword ptr [ebp - 4] ; 0x00613d52: comiss xmm0, dword ptr [ebp - 4] ; 0x00613d56: jbe 0x613d61

### 0x006164a9
- blocks=11, insns=54, edges=19, jcc=8, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00616535)
- branch points:
  - 0x006164b2: je -> 0x00616512 (jcc_true) | ctx: 0x006164aa: mov esi, ecx ; 0x006164ac: mov eax, dword ptr [esi + 0x24] ; 0x006164af: cmp eax, dword ptr [esi + 0x28] ; 0x006164b2: je 0x616512
  - 0x006164b2: je -> 0x006164b4 (jcc_false) | ctx: 0x006164aa: mov esi, ecx ; 0x006164ac: mov eax, dword ptr [esi + 0x24] ; 0x006164af: cmp eax, dword ptr [esi + 0x28] ; 0x006164b2: je 0x616512
  - 0x006164b8: je -> 0x006164ca (jcc_true) | ctx: 0x006164b4: cmp dword ptr [esi + 4], -1 ; 0x006164b8: je 0x6164ca
  - 0x006164b8: je -> 0x006164ba (jcc_false) | ctx: 0x006164b4: cmp dword ptr [esi + 4], -1 ; 0x006164b8: je 0x6164ca
  - 0x006164dc: je -> 0x006164f6 (jcc_true) | ctx: 0x006164d3: mov ecx, edi ; 0x006164d5: call 0x501a10 ; 0x006164da: test eax, eax ; 0x006164dc: je 0x6164f6
  - 0x006164dc: je -> 0x006164de (jcc_false) | ctx: 0x006164d3: mov ecx, edi ; 0x006164d5: call 0x501a10 ; 0x006164da: test eax, eax ; 0x006164dc: je 0x6164f6
  - 0x006164c8: jbe -> 0x00616512 (jcc_true) | ctx: 0x006164ba: mov eax, dword ptr [esi] ; 0x006164bc: movss xmm0, dword ptr [eax + 0x2c] ; 0x006164c1: comiss xmm0, dword ptr [0xbbf608] ; 0x006164c8: jbe 0x616512
  - 0x006164c8: jbe -> 0x006164ca (jcc_false) | ctx: 0x006164ba: mov eax, dword ptr [esi] ; 0x006164bc: movss xmm0, dword ptr [eax + 0x2c] ; 0x006164c1: comiss xmm0, dword ptr [0xbbf608] ; 0x006164c8: jbe 0x616512
  - 0x00616508: jl -> 0x00616511 (jcc_true) | ctx: 0x00616502: pop ecx ; 0x00616503: idiv ecx ; 0x00616505: cmp dword ptr [esi + 4], eax ; 0x00616508: jl 0x616511
  - 0x00616508: jl -> 0x0061650a (jcc_false) | ctx: 0x00616502: pop ecx ; 0x00616503: idiv ecx ; 0x00616505: cmp dword ptr [esi + 4], eax ; 0x00616508: jl 0x616511
  - 0x006164e2: jb -> 0x006164e6 (jcc_true) | ctx: 0x006164de: cmp dword ptr [edi + 0x14], 0x10 ; 0x006164e2: jb 0x6164e6
  - 0x006164e2: jb -> 0x006164e4 (jcc_false) | ctx: 0x006164de: cmp dword ptr [edi + 0x14], 0x10 ; 0x006164e2: jb 0x6164e6
  - 0x006164f4: jne -> 0x00616511 (jcc_true) | ctx: 0x006164ef: pop ecx ; 0x006164f0: pop ecx ; 0x006164f1: cmp eax, 1 ; 0x006164f4: jne 0x616511
  - 0x006164f4: jne -> 0x006164f6 (jcc_false) | ctx: 0x006164ef: pop ecx ; 0x006164f0: pop ecx ; 0x006164f1: cmp eax, 1 ; 0x006164f4: jne 0x616511
  - 0x006164f4: jne -> 0x00616511 (jcc_true) | ctx: 0x006164ef: pop ecx ; 0x006164f0: pop ecx ; 0x006164f1: cmp eax, 1 ; 0x006164f4: jne 0x616511
  - 0x006164f4: jne -> 0x006164f6 (jcc_false) | ctx: 0x006164ef: pop ecx ; 0x006164f0: pop ecx ; 0x006164f1: cmp eax, 1 ; 0x006164f4: jne 0x616511

### 0x00619e3e
- blocks=1, insns=30, edges=7, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x006164a9 at 0x00619e85)
- branch points:
  - none

### 0x0061a1a3
- blocks=1, insns=17, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0061d303 at 0x0061a1c5)
- branch points:
  - none

### 0x0061c64c
- blocks=1, insns=31, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0061c712)
- branch points:
  - none

### 0x0061d303
- blocks=7, insns=41, edges=17, jcc=6, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0061d34e)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0061d37e)
- branch points:
  - 0x0061d30f: je -> 0x0061d341 (jcc_true) | ctx: 0x0061d308: mov edx, dword ptr [eax] ; 0x0061d30a: mov dword ptr [ebp - 4], edx ; 0x0061d30d: cmp edx, eax ; 0x0061d30f: je 0x61d341
  - 0x0061d30f: je -> 0x0061d311 (jcc_false) | ctx: 0x0061d308: mov edx, dword ptr [eax] ; 0x0061d30a: mov dword ptr [ebp - 4], edx ; 0x0061d30d: cmp edx, eax ; 0x0061d30f: je 0x61d341
  - 0x0061d321: jp -> 0x0061d332 (jcc_true) | ctx: 0x0061d319: ucomiss xmm0, dword ptr [edx + 0x18] ; 0x0061d31d: lahf ; 0x0061d31e: test ah, 0x44 ; 0x0061d321: jp 0x61d332
  - 0x0061d321: jp -> 0x0061d323 (jcc_false) | ctx: 0x0061d319: ucomiss xmm0, dword ptr [edx + 0x18] ; 0x0061d31d: lahf ; 0x0061d31e: test ah, 0x44 ; 0x0061d321: jp 0x61d332
  - 0x0061d33f: jne -> 0x0061d311 (jcc_true) | ctx: 0x0061d335: call 0x577cf5 ; 0x0061d33a: mov edx, dword ptr [ebp - 4] ; 0x0061d33d: cmp edx, dword ptr [esi] ; 0x0061d33f: jne 0x61d311
  - 0x0061d33f: jne -> 0x0061d341 (jcc_false) | ctx: 0x0061d335: call 0x577cf5 ; 0x0061d33a: mov edx, dword ptr [ebp - 4] ; 0x0061d33d: cmp edx, dword ptr [esi] ; 0x0061d33f: jne 0x61d311
  - 0x0061d327: jb -> 0x0061d32b (jcc_true) | ctx: 0x0061d323: cmp dword ptr [edx + 0x14], 0x10 ; 0x0061d327: jb 0x61d32b
  - 0x0061d327: jb -> 0x0061d329 (jcc_false) | ctx: 0x0061d323: cmp dword ptr [edx + 0x14], 0x10 ; 0x0061d327: jb 0x61d32b
  - 0x0061d33f: jne -> 0x0061d311 (jcc_true) | ctx: 0x0061d335: call 0x577cf5 ; 0x0061d33a: mov edx, dword ptr [ebp - 4] ; 0x0061d33d: cmp edx, dword ptr [esi] ; 0x0061d33f: jne 0x61d311
  - 0x0061d33f: jne -> 0x0061d341 (jcc_false) | ctx: 0x0061d335: call 0x577cf5 ; 0x0061d33a: mov edx, dword ptr [ebp - 4] ; 0x0061d33d: cmp edx, dword ptr [esi] ; 0x0061d33f: jne 0x61d311
  - 0x0061d33f: jne -> 0x0061d311 (jcc_true) | ctx: 0x0061d335: call 0x577cf5 ; 0x0061d33a: mov edx, dword ptr [ebp - 4] ; 0x0061d33d: cmp edx, dword ptr [esi] ; 0x0061d33f: jne 0x61d311
  - 0x0061d33f: jne -> 0x0061d341 (jcc_false) | ctx: 0x0061d335: call 0x577cf5 ; 0x0061d33a: mov edx, dword ptr [ebp - 4] ; 0x0061d33d: cmp edx, dword ptr [esi] ; 0x0061d33f: jne 0x61d311

### 0x0061e633
- blocks=1, insns=23, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0061e682)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0061e730)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0061e7d5)
- branch points:
  - none

### 0x0061e8bd
- blocks=5, insns=31, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00611e48 at 0x0061e8e8)
- branch points:
  - 0x0061e8d0: jae -> 0x0061e8f5 (jcc_true) | ctx: 0x0061e8c9: sub eax, edx ; 0x0061e8cb: sar eax, 6 ; 0x0061e8ce: cmp eax, ecx ; 0x0061e8d0: jae 0x61e8f5
  - 0x0061e8d0: jae -> 0x0061e8d2 (jcc_false) | ctx: 0x0061e8c9: sub eax, edx ; 0x0061e8cb: sar eax, 6 ; 0x0061e8ce: cmp eax, ecx ; 0x0061e8d0: jae 0x61e8f5
  - 0x0061e8e0: jb -> 0x0061e8fa (jcc_true) | ctx: 0x0061e8d9: sar edx, 6 ; 0x0061e8dc: sub eax, edx ; 0x0061e8de: cmp eax, ecx ; 0x0061e8e0: jb 0x61e8fa
  - 0x0061e8e0: jb -> 0x0061e8e2 (jcc_false) | ctx: 0x0061e8d9: sar edx, 6 ; 0x0061e8dc: sub eax, edx ; 0x0061e8de: cmp eax, ecx ; 0x0061e8e0: jb 0x61e8fa

### 0x0061e909
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0061e633 at 0x0061e939)
- branch points:
  - 0x0061e920: jae -> 0x0061e946 (jcc_true) | ctx: 0x0061e919: idiv ebx ; 0x0061e91b: mov edi, dword ptr [ebp + 8] ; 0x0061e91e: cmp eax, edi ; 0x0061e920: jae 0x61e946
  - 0x0061e920: jae -> 0x0061e922 (jcc_false) | ctx: 0x0061e919: idiv ebx ; 0x0061e91b: mov edi, dword ptr [ebp + 8] ; 0x0061e91e: cmp eax, edi ; 0x0061e920: jae 0x61e946
  - 0x0061e932: jb -> 0x0061e94d (jcc_true) | ctx: 0x0061e92c: idiv ebx ; 0x0061e92e: sub ecx, eax ; 0x0061e930: cmp ecx, edi ; 0x0061e932: jb 0x61e94d
  - 0x0061e932: jb -> 0x0061e934 (jcc_false) | ctx: 0x0061e92c: idiv ebx ; 0x0061e92e: sub ecx, eax ; 0x0061e930: cmp ecx, edi ; 0x0061e932: jb 0x61e94d

### 0x00622a98
- blocks=43, insns=843, edges=98, jcc=34, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00623295)
- branch points:
  - 0x00622b6d: jb -> 0x00622b82 (jcc_true) | ctx: 0x00622b62: mulss xmm1, xmm2 ; 0x00622b66: addss xmm1, xmm0 ; 0x00622b6a: comiss xmm1, xmm4 ; 0x00622b6d: jb 0x622b82
  - 0x00622b6d: jb -> 0x00622b6f (jcc_false) | ctx: 0x00622b62: mulss xmm1, xmm2 ; 0x00622b66: addss xmm1, xmm0 ; 0x00622b6a: comiss xmm1, xmm4 ; 0x00622b6d: jb 0x622b82
  - 0x00622bad: jb -> 0x00622bd0 (jcc_true) | ctx: 0x00622ba1: cvtps2pd xmm0, xmm0 ; 0x00622ba4: pop ecx ; 0x00622ba5: comisd xmm0, xmmword ptr [0xbd56e0] ; 0x00622bad: jb 0x622bd0
  - 0x00622bad: jb -> 0x00622baf (jcc_false) | ctx: 0x00622ba1: cvtps2pd xmm0, xmm0 ; 0x00622ba4: pop ecx ; 0x00622ba5: comisd xmm0, xmmword ptr [0xbd56e0] ; 0x00622bad: jb 0x622bd0
  - 0x00622bad: jb -> 0x00622bd0 (jcc_true) | ctx: 0x00622ba1: cvtps2pd xmm0, xmm0 ; 0x00622ba4: pop ecx ; 0x00622ba5: comisd xmm0, xmmword ptr [0xbd56e0] ; 0x00622bad: jb 0x622bd0
  - 0x00622bad: jb -> 0x00622baf (jcc_false) | ctx: 0x00622ba1: cvtps2pd xmm0, xmm0 ; 0x00622ba4: pop ecx ; 0x00622ba5: comisd xmm0, xmmword ptr [0xbd56e0] ; 0x00622bad: jb 0x622bd0
  - 0x00622c0a: jp -> 0x00622c1b (jcc_true) | ctx: 0x00622bff: ucomiss xmm0, dword ptr [0xbc35d0] ; 0x00622c06: lahf ; 0x00622c07: test ah, 0x44 ; 0x00622c0a: jp 0x622c1b
  - 0x00622c0a: jp -> 0x00622c0c (jcc_false) | ctx: 0x00622bff: ucomiss xmm0, dword ptr [0xbc35d0] ; 0x00622c06: lahf ; 0x00622c07: test ah, 0x44 ; 0x00622c0a: jp 0x622c1b
  - 0x00622bce: jmp -> 0x00622bd8 (jmp) | ctx: 0x00622bbf: mulss xmm0, dword ptr [ebp - 0x64] ; 0x00622bc4: mulss xmm1, dword ptr [ebp - 0x68] ; 0x00622bc9: movss dword ptr [ebp - 0x1c], xmm1 ; 0x00622bce: jmp 0x622bd8
  - 0x00622c4f: jl -> 0x00622c61 (jcc_true) | ctx: 0x00622c44: mulss xmm0, xmm3 ; 0x00622c48: subss xmm1, xmm0 ; 0x00622c4c: movaps xmm2, xmm1 ; 0x00622c4f: jl 0x622c61
  - 0x00622c4f: jl -> 0x00622c51 (jcc_false) | ctx: 0x00622c44: mulss xmm0, xmm3 ; 0x00622c48: subss xmm1, xmm0 ; 0x00622c4c: movaps xmm2, xmm1 ; 0x00622c4f: jl 0x622c61
  - 0x00622c16: jmp -> 0x0062326e (jmp) | ctx: 0x00622c0c: movss xmm0, dword ptr [ebp + 0xc] ; 0x00622c11: movss dword ptr [edi + 0x14], xmm0 ; 0x00622c16: jmp 0x62326e
  - 0x00622c0a: jp -> 0x00622c1b (jcc_true) | ctx: 0x00622bff: ucomiss xmm0, dword ptr [0xbc35d0] ; 0x00622c06: lahf ; 0x00622c07: test ah, 0x44 ; 0x00622c0a: jp 0x622c1b
  - 0x00622c0a: jp -> 0x00622c0c (jcc_false) | ctx: 0x00622bff: ucomiss xmm0, dword ptr [0xbc35d0] ; 0x00622c06: lahf ; 0x00622c07: test ah, 0x44 ; 0x00622c0a: jp 0x622c1b
  - 0x00622d65: jae -> 0x00622d79 (jcc_true) | ctx: 0x00622d5e: mov edx, eax ; 0x00622d60: mov dword ptr [ebp - 0xc], edx ; 0x00622d63: cmp edx, edi ; 0x00622d65: jae 0x622d79
  - 0x00622d65: jae -> 0x00622d67 (jcc_false) | ctx: 0x00622d5e: mov edx, eax ; 0x00622d60: mov dword ptr [ebp - 0xc], edx ; 0x00622d63: cmp edx, edi ; 0x00622d65: jae 0x622d79
  - 0x00622d65: jae -> 0x00622d79 (jcc_true) | ctx: 0x00622d5e: mov edx, eax ; 0x00622d60: mov dword ptr [ebp - 0xc], edx ; 0x00622d63: cmp edx, edi ; 0x00622d65: jae 0x622d79
  - 0x00622d65: jae -> 0x00622d67 (jcc_false) | ctx: 0x00622d5e: mov edx, eax ; 0x00622d60: mov dword ptr [ebp - 0xc], edx ; 0x00622d63: cmp edx, edi ; 0x00622d65: jae 0x622d79
  - 0x00622d79: jbe -> 0x00622d8d (jcc_true) | ctx: 0x00622d79: jbe 0x622d8d
  - 0x00622d79: jbe -> 0x00622d7b (jcc_false) | ctx: 0x00622d79: jbe 0x622d8d
  - 0x00622d70: jbe -> 0x00622d77 (jcc_true) | ctx: 0x00622d6a: mov ecx, edi ; 0x00622d6c: sub ecx, edx ; 0x00622d6e: cmp ecx, eax ; 0x00622d70: jbe 0x622d77
  - 0x00622d70: jbe -> 0x00622d72 (jcc_false) | ctx: 0x00622d6a: mov ecx, edi ; 0x00622d6c: sub ecx, edx ; 0x00622d6e: cmp ecx, eax ; 0x00622d70: jbe 0x622d77
  - 0x00622d9b: jae -> 0x00622dca (jcc_true) | ctx: 0x00622d91: call 0x623352 ; 0x00622d96: mov eax, dword ptr [ebp - 0xc] ; 0x00622d99: cmp eax, edi ; 0x00622d9b: jae 0x622dca
  - 0x00622d9b: jae -> 0x00622d9d (jcc_false) | ctx: 0x00622d91: call 0x623352 ; 0x00622d96: mov eax, dword ptr [ebp - 0xc] ; 0x00622d99: cmp eax, edi ; 0x00622d9b: jae 0x622dca
  - 0x00622d84: jbe -> 0x00622d8d (jcc_true) | ctx: 0x00622d7e: mov eax, edx ; 0x00622d80: sub eax, edi ; 0x00622d82: cmp eax, ecx ; 0x00622d84: jbe 0x622d8d
  - 0x00622d84: jbe -> 0x00622d86 (jcc_false) | ctx: 0x00622d7e: mov eax, edx ; 0x00622d80: sub eax, edi ; 0x00622d82: cmp eax, ecx ; 0x00622d84: jbe 0x622d8d
  - 0x00622d79: jbe -> 0x00622d8d (jcc_true) | ctx: 0x00622d77: cmp edx, edi ; 0x00622d79: jbe 0x622d8d
  - 0x00622d79: jbe -> 0x00622d7b (jcc_false) | ctx: 0x00622d77: cmp edx, edi ; 0x00622d79: jbe 0x622d8d
  - 0x00622d75: jmp -> 0x00622d8a (jmp) | ctx: 0x00622d72: lea edi, [edx + eax] ; 0x00622d75: jmp 0x622d8a
  - 0x00622de4: jbe -> 0x00623085 (jcc_true) | ctx: 0x00622dd7: addss xmm0, xmm1 ; 0x00622ddb: movss dword ptr [esi + 0x50], xmm0 ; 0x00622de0: comiss xmm0, dword ptr [eax + 0x38] ; 0x00622de4: jbe 0x623085
  - 0x00622de4: jbe -> 0x00622dea (jcc_false) | ctx: 0x00622dd7: addss xmm0, xmm1 ; 0x00622ddb: movss dword ptr [esi + 0x50], xmm0 ; 0x00622de0: comiss xmm0, dword ptr [eax + 0x38] ; 0x00622de4: jbe 0x623085
  - 0x00622dc5: jne -> 0x00622dac (jcc_true) | ctx: 0x00622dbc: add edx, 0x14 ; 0x00622dbf: mov dword ptr [ebp - 0xc], edx ; 0x00622dc2: sub edi, 1 ; 0x00622dc5: jne 0x622dac
  - 0x00622dc5: jne -> 0x00622dc7 (jcc_false) | ctx: 0x00622dbc: add edx, 0x14 ; 0x00622dbf: mov dword ptr [ebp - 0xc], edx ; 0x00622dc2: sub edi, 1 ; 0x00622dc5: jne 0x622dac
  - 0x00622d9b: jae -> 0x00622dca (jcc_true) | ctx: 0x00622d91: call 0x623352 ; 0x00622d96: mov eax, dword ptr [ebp - 0xc] ; 0x00622d99: cmp eax, edi ; 0x00622d9b: jae 0x622dca
  - 0x00622d9b: jae -> 0x00622d9d (jcc_false) | ctx: 0x00622d91: call 0x623352 ; 0x00622d96: mov eax, dword ptr [ebp - 0xc] ; 0x00622d99: cmp eax, edi ; 0x00622d9b: jae 0x622dca
  - 0x00622d9b: jae -> 0x00622dca (jcc_true) | ctx: 0x00622d91: call 0x623352 ; 0x00622d96: mov eax, dword ptr [ebp - 0xc] ; 0x00622d99: cmp eax, edi ; 0x00622d9b: jae 0x622dca
  - 0x00622d9b: jae -> 0x00622d9d (jcc_false) | ctx: 0x00622d91: call 0x623352 ; 0x00622d96: mov eax, dword ptr [ebp - 0xc] ; 0x00622d99: cmp eax, edi ; 0x00622d9b: jae 0x622dca
  - 0x006230a2: je -> 0x006231ea (jcc_true) | ctx: 0x00623096: movss dword ptr [ebp - 0x3c], xmm2 ; 0x0062309b: movss dword ptr [ebp - 0x30], xmm6 ; 0x006230a0: test edi, edi ; 0x006230a2: je 0x6231ea
  - 0x006230a2: je -> 0x006230a8 (jcc_false) | ctx: 0x00623096: movss dword ptr [ebp - 0x3c], xmm2 ; 0x0062309b: movss dword ptr [ebp - 0x30], xmm6 ; 0x006230a0: test edi, edi ; 0x006230a2: je 0x6231ea
  - 0x00622df2: jbe -> 0x00622e02 (jcc_true) | ctx: 0x00622dea: movss xmm1, dword ptr [esi + 0x4c] ; 0x00622def: comiss xmm1, xmm0 ; 0x00622df2: jbe 0x622e02
  - 0x00622df2: jbe -> 0x00622df4 (jcc_false) | ctx: 0x00622dea: movss xmm1, dword ptr [esi + 0x4c] ; 0x00622def: comiss xmm1, xmm0 ; 0x00622df2: jbe 0x622e02
  - 0x00622dc5: jne -> 0x00622dac (jcc_true) | ctx: 0x00622dbc: add edx, 0x14 ; 0x00622dbf: mov dword ptr [ebp - 0xc], edx ; 0x00622dc2: sub edi, 1 ; 0x00622dc5: jne 0x622dac
  - 0x00622dc5: jne -> 0x00622dc7 (jcc_false) | ctx: 0x00622dbc: add edx, 0x14 ; 0x00622dbf: mov dword ptr [ebp - 0xc], edx ; 0x00622dc2: sub edi, 1 ; 0x00622dc5: jne 0x622dac
  - 0x00622de4: jbe -> 0x00623085 (jcc_true) | ctx: 0x00622dd7: addss xmm0, xmm1 ; 0x00622ddb: movss dword ptr [esi + 0x50], xmm0 ; 0x00622de0: comiss xmm0, dword ptr [eax + 0x38] ; 0x00622de4: jbe 0x623085
  - 0x00622de4: jbe -> 0x00622dea (jcc_false) | ctx: 0x00622dd7: addss xmm0, xmm1 ; 0x00622ddb: movss dword ptr [esi + 0x50], xmm0 ; 0x00622de0: comiss xmm0, dword ptr [eax + 0x38] ; 0x00622de4: jbe 0x623085
  - 0x00623205: je -> 0x00623245 (jcc_true) | ctx: 0x006231fd: mov ecx, dword ptr [ebp - 0x40] ; 0x00623200: add esp, 0x10 ; 0x00623203: test edi, edi ; 0x00623205: je 0x623245
  - 0x00623205: je -> 0x00623207 (jcc_false) | ctx: 0x006231fd: mov ecx, dword ptr [ebp - 0x40] ; 0x00623200: add esp, 0x10 ; 0x00623203: test edi, edi ; 0x00623205: je 0x623245
  - 0x006230cb: jb -> 0x006231c8 (jcc_true) | ctx: 0x006230be: addss xmm0, dword ptr [eax + 8] ; 0x006230c3: comiss xmm0, xmm2 ; 0x006230c6: movss dword ptr [ebp - 0x38], xmm0 ; 0x006230cb: jb 0x6231c8
  - 0x006230cb: jb -> 0x006230d1 (jcc_false) | ctx: 0x006230be: addss xmm0, dword ptr [eax + 8] ; 0x006230c3: comiss xmm0, xmm2 ; 0x006230c6: movss dword ptr [ebp - 0x38], xmm0 ; 0x006230cb: jb 0x6231c8
  - 0x006230a2: je -> 0x006231ea (jcc_true) | ctx: 0x00623096: movss dword ptr [ebp - 0x3c], xmm2 ; 0x0062309b: movss dword ptr [ebp - 0x30], xmm6 ; 0x006230a0: test edi, edi ; 0x006230a2: je 0x6231ea
  - 0x006230a2: je -> 0x006230a8 (jcc_false) | ctx: 0x00623096: movss dword ptr [ebp - 0x3c], xmm2 ; 0x0062309b: movss dword ptr [ebp - 0x30], xmm6 ; 0x006230a0: test edi, edi ; 0x006230a2: je 0x6231ea
  - 0x00622dfd: jmp -> 0x00622f18 (jmp) | ctx: 0x00622df4: subss xmm1, xmm0 ; 0x00622df8: movss dword ptr [esi + 0x4c], xmm1 ; 0x00622dfd: jmp 0x622f18
  - 0x00623243: jne -> 0x0062320f (jcc_true) | ctx: 0x00623238: movss dword ptr [ecx + 8], xmm0 ; 0x0062323d: add ecx, dword ptr [ebp - 0x3c] ; 0x00623240: sub edx, 1 ; 0x00623243: jne 0x62320f
  - 0x00623243: jne -> 0x00623245 (jcc_false) | ctx: 0x00623238: movss dword ptr [ecx + 8], xmm0 ; 0x0062323d: add ecx, dword ptr [ebp - 0x3c] ; 0x00623240: sub edx, 1 ; 0x00623243: jne 0x62320f
  - 0x006231e1: jne -> 0x006230ad (jcc_true) | ctx: 0x006231d5: add edi, 0x14 ; 0x006231d8: sub dword ptr [ebp - 0x28], 1 ; 0x006231dc: movss xmm2, dword ptr [ebp - 0x3c] ; 0x006231e1: jne 0x6230ad
  - 0x006231e1: jne -> 0x006231e7 (jcc_false) | ctx: 0x006231d5: add edi, 0x14 ; 0x006231d8: sub dword ptr [ebp - 0x28], 1 ; 0x006231dc: movss xmm2, dword ptr [ebp - 0x3c] ; 0x006231e1: jne 0x6230ad
  - 0x00623104: jb -> 0x00623145 (jcc_true) | ctx: 0x006230f8: mulss xmm0, xmm2 ; 0x006230fc: addss xmm1, xmm0 ; 0x00623100: comiss xmm1, dword ptr [ebp - 0x20] ; 0x00623104: jb 0x623145
  - 0x00623104: jb -> 0x00623106 (jcc_false) | ctx: 0x006230f8: mulss xmm0, xmm2 ; 0x006230fc: addss xmm1, xmm0 ; 0x00623100: comiss xmm1, dword ptr [ebp - 0x20] ; 0x00623104: jb 0x623145
  - 0x006230a2: je -> 0x006231ea (jcc_true) | ctx: 0x00623096: movss dword ptr [ebp - 0x3c], xmm2 ; 0x0062309b: movss dword ptr [ebp - 0x30], xmm6 ; 0x006230a0: test edi, edi ; 0x006230a2: je 0x6231ea
  - 0x006230a2: je -> 0x006230a8 (jcc_false) | ctx: 0x00623096: movss dword ptr [ebp - 0x3c], xmm2 ; 0x0062309b: movss dword ptr [ebp - 0x30], xmm6 ; 0x006230a0: test edi, edi ; 0x006230a2: je 0x6231ea
  - 0x00623243: jne -> 0x0062320f (jcc_true) | ctx: 0x00623238: movss dword ptr [ecx + 8], xmm0 ; 0x0062323d: add ecx, dword ptr [ebp - 0x3c] ; 0x00623240: sub edx, 1 ; 0x00623243: jne 0x62320f
  - 0x00623243: jne -> 0x00623245 (jcc_false) | ctx: 0x00623238: movss dword ptr [ecx + 8], xmm0 ; 0x0062323d: add ecx, dword ptr [ebp - 0x3c] ; 0x00623240: sub edx, 1 ; 0x00623243: jne 0x62320f
  - 0x006230cb: jb -> 0x006231c8 (jcc_true) | ctx: 0x006230be: addss xmm0, dword ptr [eax + 8] ; 0x006230c3: comiss xmm0, xmm2 ; 0x006230c6: movss dword ptr [ebp - 0x38], xmm0 ; 0x006230cb: jb 0x6231c8
  - 0x006230cb: jb -> 0x006230d1 (jcc_false) | ctx: 0x006230be: addss xmm0, dword ptr [eax + 8] ; 0x006230c3: comiss xmm0, xmm2 ; 0x006230c6: movss dword ptr [ebp - 0x38], xmm0 ; 0x006230cb: jb 0x6231c8
  - 0x00623205: je -> 0x00623245 (jcc_true) | ctx: 0x006231fd: mov ecx, dword ptr [ebp - 0x40] ; 0x00623200: add esp, 0x10 ; 0x00623203: test edi, edi ; 0x00623205: je 0x623245
  - 0x00623205: je -> 0x00623207 (jcc_false) | ctx: 0x006231fd: mov ecx, dword ptr [ebp - 0x40] ; 0x00623200: add esp, 0x10 ; 0x00623203: test edi, edi ; 0x00623205: je 0x623245
  - 0x00623198: jbe -> 0x006231a5 (jcc_true) | ctx: 0x0062318c: addss xmm1, xmm0 ; 0x00623190: movss xmm0, dword ptr [ebp - 0x20] ; 0x00623195: comiss xmm0, xmm1 ; 0x00623198: jbe 0x6231a5
  - 0x00623198: jbe -> 0x0062319a (jcc_false) | ctx: 0x0062318c: addss xmm1, xmm0 ; 0x00623190: movss xmm0, dword ptr [ebp - 0x20] ; 0x00623195: comiss xmm0, xmm1 ; 0x00623198: jbe 0x6231a5
  - 0x00623198: jbe -> 0x006231a5 (jcc_true) | ctx: 0x0062318c: addss xmm1, xmm0 ; 0x00623190: movss xmm0, dword ptr [ebp - 0x20] ; 0x00623195: comiss xmm0, xmm1 ; 0x00623198: jbe 0x6231a5
  - 0x00623198: jbe -> 0x0062319a (jcc_false) | ctx: 0x0062318c: addss xmm1, xmm0 ; 0x00623190: movss xmm0, dword ptr [ebp - 0x20] ; 0x00623195: comiss xmm0, xmm1 ; 0x00623198: jbe 0x6231a5
  - 0x006231c6: jmp -> 0x006231d0 (jmp) | ctx: 0x006231b7: movss dword ptr [eax + 4], xmm2 ; 0x006231bc: movss xmm0, dword ptr [ebp - 0x38] ; 0x006231c1: movss dword ptr [eax + 8], xmm0 ; 0x006231c6: jmp 0x6231d0
  - 0x006231a3: jmp -> 0x006231bc (jmp) | ctx: 0x0062319a: movss dword ptr [eax], xmm4 ; 0x0062319e: movss dword ptr [eax + 4], xmm5 ; 0x006231a3: jmp 0x6231bc
  - 0x006231e1: jne -> 0x006230ad (jcc_true) | ctx: 0x006231d5: add edi, 0x14 ; 0x006231d8: sub dword ptr [ebp - 0x28], 1 ; 0x006231dc: movss xmm2, dword ptr [ebp - 0x3c] ; 0x006231e1: jne 0x6230ad
  - 0x006231e1: jne -> 0x006231e7 (jcc_false) | ctx: 0x006231d5: add edi, 0x14 ; 0x006231d8: sub dword ptr [ebp - 0x28], 1 ; 0x006231dc: movss xmm2, dword ptr [ebp - 0x3c] ; 0x006231e1: jne 0x6230ad
  - 0x006231c6: jmp -> 0x006231d0 (jmp) | ctx: 0x006231bc: movss xmm0, dword ptr [ebp - 0x38] ; 0x006231c1: movss dword ptr [eax + 8], xmm0 ; 0x006231c6: jmp 0x6231d0

### 0x0062484b
- blocks=8, insns=91, edges=11, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00588b31 at 0x00624916)
- branch points:
  - 0x006248a8: je -> 0x006248de (jcc_true) | ctx: 0x006248a0: comiss xmm0, xmm1 ; 0x006248a3: seta al ; 0x006248a6: test cl, cl ; 0x006248a8: je 0x6248de
  - 0x006248a8: je -> 0x006248aa (jcc_false) | ctx: 0x006248a0: comiss xmm0, xmm1 ; 0x006248a3: seta al ; 0x006248a6: test cl, cl ; 0x006248a8: je 0x6248de
  - 0x006248e0: jne -> 0x006248e8 (jcc_true) | ctx: 0x006248de: test al, al ; 0x006248e0: jne 0x6248e8
  - 0x006248e0: jne -> 0x006248e2 (jcc_false) | ctx: 0x006248de: test al, al ; 0x006248e0: jne 0x6248e8
  - 0x006248ae: je -> 0x006248b4 (jcc_true) | ctx: 0x006248aa: push -1 ; 0x006248ac: test al, al ; 0x006248ae: je 0x6248b4
  - 0x006248ae: je -> 0x006248b0 (jcc_false) | ctx: 0x006248aa: push -1 ; 0x006248ac: test al, al ; 0x006248ae: je 0x6248b4
  - 0x006248e6: jmp -> 0x00624913 (jmp) | ctx: 0x006248e2: push 0 ; 0x006248e4: push 0 ; 0x006248e6: jmp 0x624913
  - 0x006248dc: jmp -> 0x00624913 (jmp) | ctx: 0x006248d6: cmp eax, ecx ; 0x006248d8: cmovl eax, ecx ; 0x006248db: push eax ; 0x006248dc: jmp 0x624913
  - 0x006248b2: jmp -> 0x00624913 (jmp) | ctx: 0x006248b0: push 1 ; 0x006248b2: jmp 0x624913

### 0x00627469
- blocks=4, insns=160, edges=11, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0062767a at 0x006274ab)
- branch points:
  - 0x00627489: jg -> 0x00627494 (jcc_true) | ctx: 0x0062747b: mov ecx, dword ptr [eax + ecx*4] ; 0x0062747e: mov eax, dword ptr [0xf583ec] ; 0x00627483: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00627489: jg 0x627494
  - 0x00627489: jg -> 0x0062748b (jcc_false) | ctx: 0x0062747b: mov ecx, dword ptr [eax + ecx*4] ; 0x0062747e: mov eax, dword ptr [0xf583ec] ; 0x00627483: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00627489: jg 0x627494
  - 0x006274a6: jne -> 0x0062748b (jcc_true) | ctx: 0x00627499: call 0xab6ba9 ; 0x0062749e: cmp dword ptr [0xf583ec], -1 ; 0x006274a5: pop ecx ; 0x006274a6: jne 0x62748b
  - 0x006274a6: jne -> 0x006274a8 (jcc_false) | ctx: 0x00627499: call 0xab6ba9 ; 0x0062749e: cmp dword ptr [0xf583ec], -1 ; 0x006274a5: pop ecx ; 0x006274a6: jne 0x62748b
  - 0x00627675: jmp -> 0x0062748b (jmp) | ctx: 0x00627672: pop edi ; 0x00627673: pop esi ; 0x00627674: pop ebx ; 0x00627675: jmp 0x62748b

### 0x0062767a
- blocks=4, insns=417, edges=20, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: BlockingArea via `BlockingArea` (string 0x00bd5d1c, xref 0x006277e4)
  - string_xref: NumBlockedPoints via `NumBlockedPoints` (string 0x00bd5d2c, xref 0x00627845)
- branch points:
  - 0x0062769a: jg -> 0x006276a5 (jcc_true) | ctx: 0x0062768c: mov ecx, dword ptr [eax + ecx*4] ; 0x0062768f: mov eax, dword ptr [0xf583c4] ; 0x00627694: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0062769a: jg 0x6276a5
  - 0x0062769a: jg -> 0x0062769c (jcc_false) | ctx: 0x0062768c: mov ecx, dword ptr [eax + ecx*4] ; 0x0062768f: mov eax, dword ptr [0xf583c4] ; 0x00627694: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0062769a: jg 0x6276a5
  - 0x006276b7: jne -> 0x0062769c (jcc_true) | ctx: 0x006276aa: call 0xab6ba9 ; 0x006276af: cmp dword ptr [0xf583c4], -1 ; 0x006276b6: pop ecx ; 0x006276b7: jne 0x62769c
  - 0x006276b7: jne -> 0x006276b9 (jcc_false) | ctx: 0x006276aa: call 0xab6ba9 ; 0x006276af: cmp dword ptr [0xf583c4], -1 ; 0x006276b6: pop ecx ; 0x006276b7: jne 0x62769c
  - 0x00627c3b: jmp -> 0x0062769c (jmp) | ctx: 0x00627c38: pop edi ; 0x00627c39: pop esi ; 0x00627c3a: pop ebx ; 0x00627c3b: jmp 0x62769c

### 0x0062876f
- blocks=4, insns=64, edges=11, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00628848 at 0x006287cd)
- branch points:
  - 0x0062878f: jg -> 0x0062879a (jcc_true) | ctx: 0x00628781: mov ecx, dword ptr [eax + ecx*4] ; 0x00628784: mov eax, dword ptr [0xf59344] ; 0x00628789: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0062878f: jg 0x62879a
  - 0x0062878f: jg -> 0x00628791 (jcc_false) | ctx: 0x00628781: mov ecx, dword ptr [eax + ecx*4] ; 0x00628784: mov eax, dword ptr [0xf59344] ; 0x00628789: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0062878f: jg 0x62879a
  - 0x006287ac: jne -> 0x00628791 (jcc_true) | ctx: 0x0062879f: call 0xab6ba9 ; 0x006287a4: cmp dword ptr [0xf59344], -1 ; 0x006287ab: pop ecx ; 0x006287ac: jne 0x628791
  - 0x006287ac: jne -> 0x006287ae (jcc_false) | ctx: 0x0062879f: call 0xab6ba9 ; 0x006287a4: cmp dword ptr [0xf59344], -1 ; 0x006287ab: pop ecx ; 0x006287ac: jne 0x628791
  - 0x00628843: jmp -> 0x00628791 (jmp) | ctx: 0x00628840: pop edi ; 0x00628841: pop esi ; 0x00628842: pop ebx ; 0x00628843: jmp 0x628791

### 0x00628848
- blocks=4, insns=71, edges=9, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00628979)
- branch points:
  - 0x00628868: jg -> 0x00628873 (jcc_true) | ctx: 0x0062885a: mov ecx, dword ptr [eax + ecx*4] ; 0x0062885d: mov eax, dword ptr [0xf59350] ; 0x00628862: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00628868: jg 0x628873
  - 0x00628868: jg -> 0x0062886a (jcc_false) | ctx: 0x0062885a: mov ecx, dword ptr [eax + ecx*4] ; 0x0062885d: mov eax, dword ptr [0xf59350] ; 0x00628862: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00628868: jg 0x628873
  - 0x00628885: jne -> 0x0062886a (jcc_true) | ctx: 0x00628878: call 0xab6ba9 ; 0x0062887d: cmp dword ptr [0xf59350], -1 ; 0x00628884: pop ecx ; 0x00628885: jne 0x62886a
  - 0x00628885: jne -> 0x00628887 (jcc_false) | ctx: 0x00628878: call 0xab6ba9 ; 0x0062887d: cmp dword ptr [0xf59350], -1 ; 0x00628884: pop ecx ; 0x00628885: jne 0x62886a
  - 0x0062892f: jmp -> 0x0062886a (jmp) | ctx: 0x0062892c: pop edi ; 0x0062892d: pop esi ; 0x0062892e: pop ebx ; 0x0062892f: jmp 0x62886a

### 0x0062e056
- blocks=1, insns=3, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCamperBehavior@GGL@@ slot 0 (target 0x0062e056, vtable 0x00bd8eb0)
- branch points:
  - none

### 0x00631daa
- blocks=6, insns=52, edges=10, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00631e3d at 0x00631df0)
- branch points:
  - 0x00631dca: jle -> 0x00631dcf (jcc_true) | ctx: 0x00631dbc: mov ecx, dword ptr [eax + ecx*4] ; 0x00631dbf: mov eax, dword ptr [0xf5cc80] ; 0x00631dc4: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00631dca: jle 0x631dcf
  - 0x00631dca: jle -> 0x00631dcc (jcc_false) | ctx: 0x00631dbc: mov ecx, dword ptr [eax + ecx*4] ; 0x00631dbf: mov eax, dword ptr [0xf5cc80] ; 0x00631dc4: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00631dca: jle 0x631dcf
  - 0x00631dcc: jmp -> 0x00631dd8 (jmp) | ctx: 0x00631dcc: jmp 0x631dd8
  - 0x00631dec: jne -> 0x00631dce (jcc_true) | ctx: 0x00631ddf: call 0xab6ba9 ; 0x00631de4: cmp dword ptr [0xf5cc80], -1 ; 0x00631deb: pop ecx ; 0x00631dec: jne 0x631dce
  - 0x00631dec: jne -> 0x00631dee (jcc_false) | ctx: 0x00631ddf: call 0xab6ba9 ; 0x00631de4: cmp dword ptr [0xf5cc80], -1 ; 0x00631deb: pop ecx ; 0x00631dec: jne 0x631dce
  - 0x00631e3b: jmp -> 0x00631dce (jmp) | ctx: 0x00631e36: add esp, 0xc ; 0x00631e39: pop edi ; 0x00631e3a: pop esi ; 0x00631e3b: jmp 0x631dce

### 0x00631e3d
- blocks=4, insns=102, edges=12, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: FinePath via `FinePath` (string 0x00bd7608, xref 0x00631e9e)
  - string_xref: CoarsePath via `CoarsePath` (string 0x00bd7614, xref 0x00631ec2)
  - caller_of_anchor_path: depth 1 (calls 0x00631f80 at 0x00631eb6)
  - caller_of_anchor_path: depth 1 (calls 0x0063201a at 0x00631e7f)
- branch points:
  - 0x00631e5d: jg -> 0x00631e68 (jcc_true) | ctx: 0x00631e4f: mov ecx, dword ptr [eax + ecx*4] ; 0x00631e52: mov eax, dword ptr [0xf5cc34] ; 0x00631e57: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00631e5d: jg 0x631e68
  - 0x00631e5d: jg -> 0x00631e5f (jcc_false) | ctx: 0x00631e4f: mov ecx, dword ptr [eax + ecx*4] ; 0x00631e52: mov eax, dword ptr [0xf5cc34] ; 0x00631e57: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00631e5d: jg 0x631e68
  - 0x00631e7a: jne -> 0x00631e5f (jcc_true) | ctx: 0x00631e6d: call 0xab6ba9 ; 0x00631e72: cmp dword ptr [0xf5cc34], -1 ; 0x00631e79: pop ecx ; 0x00631e7a: jne 0x631e5f
  - 0x00631e7a: jne -> 0x00631e7c (jcc_false) | ctx: 0x00631e6d: call 0xab6ba9 ; 0x00631e72: cmp dword ptr [0xf5cc34], -1 ; 0x00631e79: pop ecx ; 0x00631e7a: jne 0x631e5f
  - 0x00631f7a: jmp -> 0x00631e5f (jmp) | ctx: 0x00631f77: pop edi ; 0x00631f78: pop esi ; 0x00631f79: pop ebx ; 0x00631f7a: jmp 0x631e5f

### 0x00631f80
- blocks=6, insns=54, edges=10, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: WayPoints via `WayPoints` (string 0x00bc9228, xref 0x00631fd2)
  - caller_of_anchor_path: depth 1 (calls 0x0063231d at 0x00631fc6)
- branch points:
  - 0x00631fa0: jle -> 0x00631fa5 (jcc_true) | ctx: 0x00631f92: mov ecx, dword ptr [eax + ecx*4] ; 0x00631f95: mov eax, dword ptr [0xf5cb50] ; 0x00631f9a: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00631fa0: jle 0x631fa5
  - 0x00631fa0: jle -> 0x00631fa2 (jcc_false) | ctx: 0x00631f92: mov ecx, dword ptr [eax + ecx*4] ; 0x00631f95: mov eax, dword ptr [0xf5cb50] ; 0x00631f9a: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00631fa0: jle 0x631fa5
  - 0x00631fa2: jmp -> 0x00631fae (jmp) | ctx: 0x00631fa2: jmp 0x631fae
  - 0x00631fc2: jne -> 0x00631fa4 (jcc_true) | ctx: 0x00631fb5: call 0xab6ba9 ; 0x00631fba: cmp dword ptr [0xf5cb50], -1 ; 0x00631fc1: pop ecx ; 0x00631fc2: jne 0x631fa4
  - 0x00631fc2: jne -> 0x00631fc4 (jcc_false) | ctx: 0x00631fb5: call 0xab6ba9 ; 0x00631fba: cmp dword ptr [0xf5cb50], -1 ; 0x00631fc1: pop ecx ; 0x00631fc2: jne 0x631fa4
  - 0x00632018: jmp -> 0x00631fa4 (jmp) | ctx: 0x00632013: add esp, 0x14 ; 0x00632016: pop edi ; 0x00632017: pop esi ; 0x00632018: jmp 0x631fa4

### 0x0063201a
- blocks=4, insns=235, edges=14, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: NextWayPoint via `NextWayPoint` (string 0x00bd757c, xref 0x006320f6)
  - string_xref: NextWaypointOrientation via `NextWaypointOrientation` (string 0x00bd758c, xref 0x0063211b)
  - string_xref: IsPathingUsed via `IsPathingUsed` (string 0x00bd75b0, xref 0x006321ca)
- branch points:
  - 0x0063203a: jg -> 0x00632045 (jcc_true) | ctx: 0x0063202c: mov ecx, dword ptr [eax + ecx*4] ; 0x0063202f: mov eax, dword ptr [0xf5cc30] ; 0x00632034: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0063203a: jg 0x632045
  - 0x0063203a: jg -> 0x0063203c (jcc_false) | ctx: 0x0063202c: mov ecx, dword ptr [eax + ecx*4] ; 0x0063202f: mov eax, dword ptr [0xf5cc30] ; 0x00632034: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0063203a: jg 0x632045
  - 0x00632057: jne -> 0x0063203c (jcc_true) | ctx: 0x0063204a: call 0xab6ba9 ; 0x0063204f: cmp dword ptr [0xf5cc30], -1 ; 0x00632056: pop ecx ; 0x00632057: jne 0x63203c
  - 0x00632057: jne -> 0x00632059 (jcc_false) | ctx: 0x0063204a: call 0xab6ba9 ; 0x0063204f: cmp dword ptr [0xf5cc30], -1 ; 0x00632056: pop ecx ; 0x00632057: jne 0x63203c
  - 0x00632318: jmp -> 0x0063203c (jmp) | ctx: 0x00632315: pop edi ; 0x00632316: pop esi ; 0x00632317: pop ebx ; 0x00632318: jmp 0x63203c

### 0x0063231d
- blocks=4, insns=138, edges=8, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: WaypointsCount via `WaypointsCount` (string 0x00bd753c, xref 0x006323f1)
- branch points:
  - 0x0063233d: jg -> 0x00632348 (jcc_true) | ctx: 0x0063232f: mov ecx, dword ptr [eax + ecx*4] ; 0x00632332: mov eax, dword ptr [0xf5c8e4] ; 0x00632337: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0063233d: jg 0x632348
  - 0x0063233d: jg -> 0x0063233f (jcc_false) | ctx: 0x0063232f: mov ecx, dword ptr [eax + ecx*4] ; 0x00632332: mov eax, dword ptr [0xf5c8e4] ; 0x00632337: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0063233d: jg 0x632348
  - 0x0063235a: jne -> 0x0063233f (jcc_true) | ctx: 0x0063234d: call 0xab6ba9 ; 0x00632352: cmp dword ptr [0xf5c8e4], -1 ; 0x00632359: pop ecx ; 0x0063235a: jne 0x63233f
  - 0x0063235a: jne -> 0x0063235c (jcc_false) | ctx: 0x0063234d: call 0xab6ba9 ; 0x00632352: cmp dword ptr [0xf5c8e4], -1 ; 0x00632359: pop ecx ; 0x0063235a: jne 0x63233f
  - 0x00632515: jmp -> 0x0063233f (jmp) | ctx: 0x00632512: pop edi ; 0x00632513: pop esi ; 0x00632514: pop ebx ; 0x00632515: jmp 0x63233f

### 0x00633f1a
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00631e3d at 0x00633f2e)
- branch points:
  - 0x00633f1f: jne -> 0x00633f2e (jcc_true) | ctx: 0x00633f1a: push edi ; 0x00633f1b: mov edi, ecx ; 0x00633f1d: test esi, esi ; 0x00633f1f: jne 0x633f2e
  - 0x00633f1f: jne -> 0x00633f21 (jcc_false) | ctx: 0x00633f1a: push edi ; 0x00633f1b: mov edi, ecx ; 0x00633f1d: test esi, esi ; 0x00633f1f: jne 0x633f2e

### 0x0063423e
- blocks=1, insns=19, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0058680d at 0x00634249)
- branch points:
  - none

### 0x006342eb
- blocks=12, insns=134, edges=36, jcc=9, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0058680d at 0x006343e4)
  - caller_of_anchor_path: depth 1 (calls 0x0058680d at 0x00634409)
- branch points:
  - 0x0063435f: je -> 0x006343a8 (jcc_true) | ctx: 0x00634355: cmp dword ptr [ebx + 0x60], 0 ; 0x00634359: mov ecx, dword ptr [eax + 0x24] ; 0x0063435c: mov dword ptr [ebp - 0x10], ecx ; 0x0063435f: je 0x6343a8
  - 0x0063435f: je -> 0x00634361 (jcc_false) | ctx: 0x00634355: cmp dword ptr [ebx + 0x60], 0 ; 0x00634359: mov ecx, dword ptr [eax + 0x24] ; 0x0063435c: mov dword ptr [ebp - 0x10], ecx ; 0x0063435f: je 0x6343a8
  - 0x006343d4: jle -> 0x00634415 (jcc_true) | ctx: 0x006343c9: mov ecx, dword ptr [ebx + 0x4c] ; 0x006343cc: call 0x5868ce ; 0x006343d1: cmp eax, 1 ; 0x006343d4: jle 0x634415
  - 0x006343d4: jle -> 0x006343d6 (jcc_false) | ctx: 0x006343c9: mov ecx, dword ptr [ebx + 0x4c] ; 0x006343cc: call 0x5868ce ; 0x006343d1: cmp eax, 1 ; 0x006343d4: jle 0x634415
  - 0x00634365: jne -> 0x00634391 (jcc_true) | ctx: 0x00634361: cmp dword ptr [ebx + 0x60], 1 ; 0x00634365: jne 0x634391
  - 0x00634365: jne -> 0x00634367 (jcc_false) | ctx: 0x00634361: cmp dword ptr [ebx + 0x60], 1 ; 0x00634365: jne 0x634391
  - 0x006343e9: jmp -> 0x006343fe (jmp) | ctx: 0x006343dc: and dword ptr [ebx + 0xf0], 0 ; 0x006343e3: push eax ; 0x006343e4: call 0x5867fe ; 0x006343e9: jmp 0x6343fe
  - 0x006343a3: jmp -> 0x006343c9 (jmp) | ctx: 0x00634397: push dword ptr [ebx + eax*4 + 0x68] ; 0x0063439b: push dword ptr [ebp - 0x18] ; 0x0063439e: call 0x5863c9 ; 0x006343a3: jmp 0x6343c9
  - 0x0063438f: je -> 0x006343a5 (jcc_true) | ctx: 0x00634384: call 0x56ac30 ; 0x00634389: mov edi, dword ptr [ebp - 4] ; 0x0063438c: cmp ax, si ; 0x0063438f: je 0x6343a5
  - 0x0063438f: je -> 0x00634391 (jcc_false) | ctx: 0x00634384: call 0x56ac30 ; 0x00634389: mov edi, dword ptr [ebp - 4] ; 0x0063438c: cmp ax, si ; 0x0063438f: je 0x6343a5
  - 0x00634413: jne -> 0x006343eb (jcc_true) | ctx: 0x00634409: call 0x5867ef ; 0x0063440e: mov ecx, dword ptr [ebp - 4] ; 0x00634411: cmp ecx, dword ptr [eax] ; 0x00634413: jne 0x6343eb
  - 0x00634413: jne -> 0x00634415 (jcc_false) | ctx: 0x00634409: call 0x5867ef ; 0x0063440e: mov ecx, dword ptr [ebp - 4] ; 0x00634411: cmp ecx, dword ptr [eax] ; 0x00634413: jne 0x6343eb
  - 0x006343d4: jle -> 0x00634415 (jcc_true) | ctx: 0x006343c9: mov ecx, dword ptr [ebx + 0x4c] ; 0x006343cc: call 0x5868ce ; 0x006343d1: cmp eax, 1 ; 0x006343d4: jle 0x634415
  - 0x006343d4: jle -> 0x006343d6 (jcc_false) | ctx: 0x006343c9: mov ecx, dword ptr [ebx + 0x4c] ; 0x006343cc: call 0x5868ce ; 0x006343d1: cmp eax, 1 ; 0x006343d4: jle 0x634415
  - 0x006343d4: jle -> 0x00634415 (jcc_true) | ctx: 0x006343c9: mov ecx, dword ptr [ebx + 0x4c] ; 0x006343cc: call 0x5868ce ; 0x006343d1: cmp eax, 1 ; 0x006343d4: jle 0x634415
  - 0x006343d4: jle -> 0x006343d6 (jcc_false) | ctx: 0x006343c9: mov ecx, dword ptr [ebx + 0x4c] ; 0x006343cc: call 0x5868ce ; 0x006343d1: cmp eax, 1 ; 0x006343d4: jle 0x634415
  - 0x006343f6: je -> 0x00634415 (jcc_true) | ctx: 0x006343f2: pop ecx ; 0x006343f3: pop ecx ; 0x006343f4: test al, al ; 0x006343f6: je 0x634415
  - 0x006343f6: je -> 0x006343f8 (jcc_false) | ctx: 0x006343f2: pop ecx ; 0x006343f3: pop ecx ; 0x006343f4: test al, al ; 0x006343f6: je 0x634415
  - 0x00634413: jne -> 0x006343eb (jcc_true) | ctx: 0x00634409: call 0x5867ef ; 0x0063440e: mov ecx, dword ptr [ebp - 4] ; 0x00634411: cmp ecx, dword ptr [eax] ; 0x00634413: jne 0x6343eb
  - 0x00634413: jne -> 0x00634415 (jcc_false) | ctx: 0x00634409: call 0x5867ef ; 0x0063440e: mov ecx, dword ptr [ebp - 4] ; 0x00634411: cmp ecx, dword ptr [eax] ; 0x00634413: jne 0x6343eb

### 0x0063499c
- blocks=1, insns=7, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00586227 at 0x00634a12)
- branch points:
  - none

### 0x00634fdd
- blocks=1, insns=5, edges=1, jcc=0, indirect_jmp=1, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCamperBehavior@GGL@@ slot 5 (target 0x00634fdd, vtable 0x00bd8eb0)
- branch points:
  - 0x00634fe3: jmp dword ptr [eax + 0x10] -> <indirect> | ctx: 0x00634fde: mov ebp, esp ; 0x00634fe0: mov eax, dword ptr [ecx] ; 0x00634fe2: pop ebp ; 0x00634fe3: jmp dword ptr [eax + 0x10]

### 0x006373f4
- blocks=11, insns=93, edges=30, jcc=10, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005781c1 at 0x00637480)
- branch points:
  - 0x00637452: je -> 0x006374cd (jcc_true) | ctx: 0x0063744a: mov eax, dword ptr [eax + 0x18] ; 0x0063744d: mov dword ptr [ebp - 0x10], eax ; 0x00637450: test ebx, ebx ; 0x00637452: je 0x6374cd
  - 0x00637452: je -> 0x00637454 (jcc_false) | ctx: 0x0063744a: mov eax, dword ptr [eax + 0x18] ; 0x0063744d: mov dword ptr [ebp - 0x10], eax ; 0x00637450: test ebx, ebx ; 0x00637452: je 0x6374cd
  - 0x0063748b: jle -> 0x006374c1 (jcc_true) | ctx: 0x00637485: mov ebx, eax ; 0x00637487: xor esi, esi ; 0x00637489: test ebx, ebx ; 0x0063748b: jle 0x6374c1
  - 0x0063748b: jle -> 0x0063748d (jcc_false) | ctx: 0x00637485: mov ebx, eax ; 0x00637487: xor esi, esi ; 0x00637489: test ebx, ebx ; 0x0063748b: jle 0x6374c1
  - 0x006374cb: jb -> 0x00637454 (jcc_true) | ctx: 0x006374c4: inc edi ; 0x006374c5: mov dword ptr [ebp - 4], edi ; 0x006374c8: cmp edi, dword ptr [ebp - 0x14] ; 0x006374cb: jb 0x637454
  - 0x006374cb: jb -> 0x006374cd (jcc_false) | ctx: 0x006374c4: inc edi ; 0x006374c5: mov dword ptr [ebp - 4], edi ; 0x006374c8: cmp edi, dword ptr [ebp - 0x14] ; 0x006374cb: jb 0x637454
  - 0x006374a1: je -> 0x006374b9 (jcc_true) | ctx: 0x00637494: mov ecx, dword ptr [0xdf4df0] ; 0x0063749a: call 0x56d756 ; 0x0063749f: test eax, eax ; 0x006374a1: je 0x6374b9
  - 0x006374a1: je -> 0x006374a3 (jcc_false) | ctx: 0x00637494: mov ecx, dword ptr [0xdf4df0] ; 0x0063749a: call 0x56d756 ; 0x0063749f: test eax, eax ; 0x006374a1: je 0x6374b9
  - 0x006374bc: jl -> 0x00637490 (jcc_true) | ctx: 0x006374b9: inc esi ; 0x006374ba: cmp esi, ebx ; 0x006374bc: jl 0x637490
  - 0x006374bc: jl -> 0x006374be (jcc_false) | ctx: 0x006374b9: inc esi ; 0x006374ba: cmp esi, ebx ; 0x006374bc: jl 0x637490
  - 0x006374a8: je -> 0x006374af (jcc_true) | ctx: 0x006374a3: mov ecx, dword ptr [edi + 0x18] ; 0x006374a6: test ecx, ecx ; 0x006374a8: je 0x6374af
  - 0x006374a8: je -> 0x006374aa (jcc_false) | ctx: 0x006374a3: mov ecx, dword ptr [edi + 0x18] ; 0x006374a6: test ecx, ecx ; 0x006374a8: je 0x6374af
  - 0x006374a1: je -> 0x006374b9 (jcc_true) | ctx: 0x00637494: mov ecx, dword ptr [0xdf4df0] ; 0x0063749a: call 0x56d756 ; 0x0063749f: test eax, eax ; 0x006374a1: je 0x6374b9
  - 0x006374a1: je -> 0x006374a3 (jcc_false) | ctx: 0x00637494: mov ecx, dword ptr [0xdf4df0] ; 0x0063749a: call 0x56d756 ; 0x0063749f: test eax, eax ; 0x006374a1: je 0x6374b9
  - 0x006374cb: jb -> 0x00637454 (jcc_true) | ctx: 0x006374c4: inc edi ; 0x006374c5: mov dword ptr [ebp - 4], edi ; 0x006374c8: cmp edi, dword ptr [ebp - 0x14] ; 0x006374cb: jb 0x637454
  - 0x006374cb: jb -> 0x006374cd (jcc_false) | ctx: 0x006374c4: inc edi ; 0x006374c5: mov dword ptr [ebp - 4], edi ; 0x006374c8: cmp edi, dword ptr [ebp - 0x14] ; 0x006374cb: jb 0x637454
  - 0x006374bc: jl -> 0x00637490 (jcc_true) | ctx: 0x006374b4: call 0x574650 ; 0x006374b9: inc esi ; 0x006374ba: cmp esi, ebx ; 0x006374bc: jl 0x637490
  - 0x006374bc: jl -> 0x006374be (jcc_false) | ctx: 0x006374b4: call 0x574650 ; 0x006374b9: inc esi ; 0x006374ba: cmp esi, ebx ; 0x006374bc: jl 0x637490
  - 0x006374ad: je -> 0x006374b9 (jcc_true) | ctx: 0x006374aa: cmp ecx, dword ptr [eax + 0x18] ; 0x006374ad: je 0x6374b9
  - 0x006374ad: je -> 0x006374af (jcc_false) | ctx: 0x006374aa: cmp ecx, dword ptr [eax + 0x18] ; 0x006374ad: je 0x6374b9

### 0x00638923
- blocks=6, insns=52, edges=10, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00638c75 at 0x00638969)
- branch points:
  - 0x00638943: jle -> 0x00638948 (jcc_true) | ctx: 0x00638935: mov ecx, dword ptr [eax + ecx*4] ; 0x00638938: mov eax, dword ptr [0xf5e7c4] ; 0x0063893d: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00638943: jle 0x638948
  - 0x00638943: jle -> 0x00638945 (jcc_false) | ctx: 0x00638935: mov ecx, dword ptr [eax + ecx*4] ; 0x00638938: mov eax, dword ptr [0xf5e7c4] ; 0x0063893d: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00638943: jle 0x638948
  - 0x00638945: jmp -> 0x00638951 (jmp) | ctx: 0x00638945: jmp 0x638951
  - 0x00638965: jne -> 0x00638947 (jcc_true) | ctx: 0x00638958: call 0xab6ba9 ; 0x0063895d: cmp dword ptr [0xf5e7c4], -1 ; 0x00638964: pop ecx ; 0x00638965: jne 0x638947
  - 0x00638965: jne -> 0x00638967 (jcc_false) | ctx: 0x00638958: call 0xab6ba9 ; 0x0063895d: cmp dword ptr [0xf5e7c4], -1 ; 0x00638964: pop ecx ; 0x00638965: jne 0x638947
  - 0x006389b4: jmp -> 0x00638947 (jmp) | ctx: 0x006389af: add esp, 0xc ; 0x006389b2: pop edi ; 0x006389b3: pop esi ; 0x006389b4: jmp 0x638947

### 0x00638b95
- blocks=6, insns=76, edges=14, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0062767a at 0x00638bdb)
- branch points:
  - 0x00638bb5: jle -> 0x00638bba (jcc_true) | ctx: 0x00638ba7: mov ecx, dword ptr [eax + ecx*4] ; 0x00638baa: mov eax, dword ptr [0xf5eb40] ; 0x00638baf: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00638bb5: jle 0x638bba
  - 0x00638bb5: jle -> 0x00638bb7 (jcc_false) | ctx: 0x00638ba7: mov ecx, dword ptr [eax + ecx*4] ; 0x00638baa: mov eax, dword ptr [0xf5eb40] ; 0x00638baf: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00638bb5: jle 0x638bba
  - 0x00638bb7: jmp -> 0x00638bc3 (jmp) | ctx: 0x00638bb7: jmp 0x638bc3
  - 0x00638bd7: jne -> 0x00638bb9 (jcc_true) | ctx: 0x00638bca: call 0xab6ba9 ; 0x00638bcf: cmp dword ptr [0xf5eb40], -1 ; 0x00638bd6: pop ecx ; 0x00638bd7: jne 0x638bb9
  - 0x00638bd7: jne -> 0x00638bd9 (jcc_false) | ctx: 0x00638bca: call 0xab6ba9 ; 0x00638bcf: cmp dword ptr [0xf5eb40], -1 ; 0x00638bd6: pop ecx ; 0x00638bd7: jne 0x638bb9
  - 0x00638c70: jmp -> 0x00638bb9 (jmp) | ctx: 0x00638c6b: add esp, 0x2c ; 0x00638c6e: pop edi ; 0x00638c6f: pop esi ; 0x00638c70: jmp 0x638bb9

### 0x00638c75
- blocks=4, insns=292, edges=15, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: WorkerAlarmMode via `WorkerAlarmModeActive` (string 0x00bd7d88, xref 0x00638f53)
- branch points:
  - 0x00638c95: jg -> 0x00638ca0 (jcc_true) | ctx: 0x00638c87: mov ecx, dword ptr [eax + ecx*4] ; 0x00638c8a: mov eax, dword ptr [0xf5e454] ; 0x00638c8f: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00638c95: jg 0x638ca0
  - 0x00638c95: jg -> 0x00638c97 (jcc_false) | ctx: 0x00638c87: mov ecx, dword ptr [eax + ecx*4] ; 0x00638c8a: mov eax, dword ptr [0xf5e454] ; 0x00638c8f: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00638c95: jg 0x638ca0
  - 0x00638cb2: jne -> 0x00638c97 (jcc_true) | ctx: 0x00638ca5: call 0xab6ba9 ; 0x00638caa: cmp dword ptr [0xf5e454], -1 ; 0x00638cb1: pop ecx ; 0x00638cb2: jne 0x638c97
  - 0x00638cb2: jne -> 0x00638cb4 (jcc_false) | ctx: 0x00638ca5: call 0xab6ba9 ; 0x00638caa: cmp dword ptr [0xf5e454], -1 ; 0x00638cb1: pop ecx ; 0x00638cb2: jne 0x638c97
  - 0x0063904c: jmp -> 0x00638c97 (jmp) | ctx: 0x00639049: pop edi ; 0x0063904a: pop esi ; 0x0063904b: pop ebx ; 0x0063904c: jmp 0x638c97

### 0x0063ade6
- blocks=3, insns=52, edges=5, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0066a5b2 at 0x0063ae5e)
- branch points:
  - 0x0063adf6: jne -> 0x0063ae43 (jcc_true) | ctx: 0x0063adee: mov dword ptr [ebp - 0x10], esp ; 0x0063adf1: mov ebx, dword ptr [esi] ; 0x0063adf3: mov dword ptr [ebp - 0x14], esi ; 0x0063adf6: jne 0x63ae43
  - 0x0063adf6: jne -> 0x0063adf8 (jcc_false) | ctx: 0x0063adee: mov dword ptr [ebp - 0x10], esp ; 0x0063adf1: mov ebx, dword ptr [esi] ; 0x0063adf3: mov dword ptr [ebp - 0x14], esi ; 0x0063adf6: jne 0x63ae43

### 0x0063afc4
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00638c75 at 0x0063afd8)
- branch points:
  - 0x0063afc9: jne -> 0x0063afd8 (jcc_true) | ctx: 0x0063afc4: push edi ; 0x0063afc5: mov edi, ecx ; 0x0063afc7: test esi, esi ; 0x0063afc9: jne 0x63afd8
  - 0x0063afc9: jne -> 0x0063afcb (jcc_false) | ctx: 0x0063afc4: push edi ; 0x0063afc5: mov edi, ecx ; 0x0063afc7: test esi, esi ; 0x0063afc9: jne 0x63afd8

### 0x0063b393
- blocks=3, insns=34, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0066a5b2 at 0x0063b3a4)
- branch points:
  - 0x0063b399: je -> 0x0063b3cc (jcc_true) | ctx: 0x0063b393: push esi ; 0x0063b394: mov esi, ecx ; 0x0063b396: cmp esi, dword ptr [ebp + 8] ; 0x0063b399: je 0x63b3cc
  - 0x0063b399: je -> 0x0063b39b (jcc_false) | ctx: 0x0063b393: push esi ; 0x0063b394: mov esi, ecx ; 0x0063b396: cmp esi, dword ptr [ebp + 8] ; 0x0063b399: je 0x63b3cc

### 0x0063b448
- blocks=6, insns=52, edges=10, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCBuildBlockedOnlyPredicate@?A0xe5557549@GGL@@ slot 1 (target 0x0063b448, vtable 0x00bd8280)
- branch points:
  - 0x0063b49e: jne -> 0x0063b4a4 (jcc_true) | ctx: 0x0063b498: sbb al, al ; 0x0063b49a: inc al ; 0x0063b49c: test bl, bl ; 0x0063b49e: jne 0x63b4a4
  - 0x0063b49e: jne -> 0x0063b4a0 (jcc_false) | ctx: 0x0063b498: sbb al, al ; 0x0063b49a: inc al ; 0x0063b49c: test bl, bl ; 0x0063b49e: jne 0x63b4a4
  - 0x0063b4a6: je -> 0x0063b4ad (jcc_true) | ctx: 0x0063b4a4: test al, al ; 0x0063b4a6: je 0x63b4ad
  - 0x0063b4a6: je -> 0x0063b4a8 (jcc_false) | ctx: 0x0063b4a4: test al, al ; 0x0063b4a6: je 0x63b4ad
  - 0x0063b4a2: je -> 0x0063b4ad (jcc_true) | ctx: 0x0063b4a0: test bh, bh ; 0x0063b4a2: je 0x63b4ad
  - 0x0063b4a2: je -> 0x0063b4a4 (jcc_false) | ctx: 0x0063b4a0: test bh, bh ; 0x0063b4a2: je 0x63b4ad
  - 0x0063b4ab: jmp -> 0x0063b4af (jmp) | ctx: 0x0063b4a8: xor eax, eax ; 0x0063b4aa: inc eax ; 0x0063b4ab: jmp 0x63b4af

### 0x0063b4c7
- blocks=1, insns=3, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCBuildBlockedOnlyPredicate@?A0xe5557549@GGL@@ slot 0 (target 0x0063b4c7, vtable 0x00bd8280)
- branch points:
  - none

### 0x0063b62a
- blocks=8, insns=93, edges=25, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005781c1 at 0x0063b680)
- branch points:
  - 0x0063b639: jne -> 0x0063b6f4 (jcc_true) | ctx: 0x0063b62f: lea ecx, [edi + 0x30] ; 0x0063b632: call 0x6179ea ; 0x0063b637: test eax, eax ; 0x0063b639: jne 0x63b6f4
  - 0x0063b639: jne -> 0x0063b63f (jcc_false) | ctx: 0x0063b62f: lea ecx, [edi + 0x30] ; 0x0063b632: call 0x6179ea ; 0x0063b637: test eax, eax ; 0x0063b639: jne 0x63b6f4
  - 0x0063b6ac: je -> 0x0063b6c7 (jcc_true) | ctx: 0x0063b6a3: pop esi ; 0x0063b6a4: pop ebx ; 0x0063b6a5: cmp byte ptr [eax + 0x124], 0 ; 0x0063b6ac: je 0x63b6c7
  - 0x0063b6ac: je -> 0x0063b6ae (jcc_false) | ctx: 0x0063b6a3: pop esi ; 0x0063b6a4: pop ebx ; 0x0063b6a5: cmp byte ptr [eax + 0x124], 0 ; 0x0063b6ac: je 0x63b6c7
  - 0x0063b6d5: je -> 0x0063b6e5 (jcc_true) | ctx: 0x0063b6c9: mov ecx, edi ; 0x0063b6cb: call dword ptr [eax + 0x84] ; 0x0063b6d1: cmp byte ptr [ebp + 8], 0 ; 0x0063b6d5: je 0x63b6e5
  - 0x0063b6d5: je -> 0x0063b6d7 (jcc_false) | ctx: 0x0063b6c9: mov ecx, edi ; 0x0063b6cb: call dword ptr [eax + 0x84] ; 0x0063b6d1: cmp byte ptr [ebp + 8], 0 ; 0x0063b6d5: je 0x63b6e5
  - 0x0063b6be: je -> 0x0063b6c7 (jcc_true) | ctx: 0x0063b6b1: mov ecx, dword ptr [0xdf4df0] ; 0x0063b6b7: call 0x56d756 ; 0x0063b6bc: test eax, eax ; 0x0063b6be: je 0x63b6c7
  - 0x0063b6be: je -> 0x0063b6c0 (jcc_false) | ctx: 0x0063b6b1: mov ecx, dword ptr [0xdf4df0] ; 0x0063b6b7: call 0x56d756 ; 0x0063b6bc: test eax, eax ; 0x0063b6be: je 0x63b6c7
  - 0x0063b6d5: je -> 0x0063b6e5 (jcc_true) | ctx: 0x0063b6c9: mov ecx, edi ; 0x0063b6cb: call dword ptr [eax + 0x84] ; 0x0063b6d1: cmp byte ptr [ebp + 8], 0 ; 0x0063b6d5: je 0x63b6e5
  - 0x0063b6d5: je -> 0x0063b6d7 (jcc_false) | ctx: 0x0063b6c9: mov ecx, edi ; 0x0063b6cb: call dword ptr [eax + 0x84] ; 0x0063b6d1: cmp byte ptr [ebp + 8], 0 ; 0x0063b6d5: je 0x63b6e5

### 0x0063be80
- blocks=5, insns=59, edges=14, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00576019 at 0x0063bece)
- branch points:
  - 0x0063be91: je -> 0x0063bed3 (jcc_true) | ctx: 0x0063be88: call 0x6179ea ; 0x0063be8d: mov ebx, eax ; 0x0063be8f: test ebx, ebx ; 0x0063be91: je 0x63bed3
  - 0x0063be91: je -> 0x0063be93 (jcc_false) | ctx: 0x0063be88: call 0x6179ea ; 0x0063be8d: mov ebx, eax ; 0x0063be8f: test ebx, ebx ; 0x0063be91: je 0x63bed3
  - 0x0063beba: je -> 0x0063bed3 (jcc_true) | ctx: 0x0063beb1: pop ecx ; 0x0063beb2: pop esi ; 0x0063beb3: cmp byte ptr [eax + 0x124], 0 ; 0x0063beba: je 0x63bed3
  - 0x0063beba: je -> 0x0063bebc (jcc_false) | ctx: 0x0063beb1: pop ecx ; 0x0063beb2: pop esi ; 0x0063beb3: cmp byte ptr [eax + 0x124], 0 ; 0x0063beba: je 0x63bed3
  - 0x0063beca: je -> 0x0063bed3 (jcc_true) | ctx: 0x0063bec2: push ebx ; 0x0063bec3: call 0x56d756 ; 0x0063bec8: test eax, eax ; 0x0063beca: je 0x63bed3
  - 0x0063beca: je -> 0x0063becc (jcc_false) | ctx: 0x0063bec2: push ebx ; 0x0063bec3: call 0x56d756 ; 0x0063bec8: test eax, eax ; 0x0063beca: je 0x63bed3

### 0x00641654
- blocks=5, insns=37, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005781c1 at 0x006417ec)
- branch points:
  - 0x00641689: je -> 0x00641693 (jcc_true) | ctx: 0x0064167f: call 0x641632 ; 0x00641684: add esp, 0x14 ; 0x00641687: test al, al ; 0x00641689: je 0x641693
  - 0x00641689: je -> 0x0064168b (jcc_false) | ctx: 0x0064167f: call 0x641632 ; 0x00641684: add esp, 0x14 ; 0x00641687: test al, al ; 0x00641689: je 0x641693
  - 0x0064168d: jne -> 0x00641693 (jcc_true) | ctx: 0x0064168b: cmp edi, esi ; 0x0064168d: jne 0x641693
  - 0x0064168d: jne -> 0x0064168f (jcc_false) | ctx: 0x0064168b: cmp edi, esi ; 0x0064168d: jne 0x641693
  - 0x00641691: jmp -> 0x00641696 (jmp) | ctx: 0x0064168f: xor eax, eax ; 0x00641691: jmp 0x641696

### 0x00644b9e
- blocks=3, insns=21, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00644bd1)
- branch points:
  - 0x00644bb6: je -> 0x00644bc5 (jcc_true) | ctx: 0x00644ba9: mov dword ptr [0xf616fc], eax ; 0x00644bae: imul eax, eax, 0x64 ; 0x00644bb1: add eax, 0xf61700 ; 0x00644bb6: je 0x644bc5
  - 0x00644bb6: je -> 0x00644bb8 (jcc_false) | ctx: 0x00644ba9: mov dword ptr [0xf616fc], eax ; 0x00644bae: imul eax, eax, 0x64 ; 0x00644bb1: add eax, 0xf61700 ; 0x00644bb6: je 0x644bc5

### 0x00644c42
- blocks=7, insns=50, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0066a5b2 at 0x00644c57)
- branch points:
  - 0x00644c49: jne -> 0x00644c90 (jcc_true) | ctx: 0x00644c43: mov edi, ecx ; 0x00644c45: mov eax, dword ptr [edi] ; 0x00644c47: cmp esi, dword ptr [eax] ; 0x00644c49: jne 0x644c90
  - 0x00644c49: jne -> 0x00644c4b (jcc_false) | ctx: 0x00644c43: mov edi, ecx ; 0x00644c45: mov eax, dword ptr [edi] ; 0x00644c47: cmp esi, dword ptr [eax] ; 0x00644c49: jne 0x644c90
  - 0x00644c93: jne -> 0x00644c79 (jcc_true) | ctx: 0x00644c90: cmp esi, dword ptr [ebp + 0x10] ; 0x00644c93: jne 0x644c79
  - 0x00644c93: jne -> 0x00644c95 (jcc_false) | ctx: 0x00644c90: cmp esi, dword ptr [ebp + 0x10] ; 0x00644c93: jne 0x644c79
  - 0x00644c4e: jne -> 0x00644c90 (jcc_true) | ctx: 0x00644c4b: cmp dword ptr [ebp + 0x10], eax ; 0x00644c4e: jne 0x644c90
  - 0x00644c4e: jne -> 0x00644c50 (jcc_false) | ctx: 0x00644c4b: cmp dword ptr [ebp + 0x10], eax ; 0x00644c4e: jne 0x644c90
  - 0x00644c93: jne -> 0x00644c79 (jcc_true) | ctx: 0x00644c88: call 0x644cac ; 0x00644c8d: mov esi, dword ptr [ebp + 0xc] ; 0x00644c90: cmp esi, dword ptr [ebp + 0x10] ; 0x00644c93: jne 0x644c79
  - 0x00644c93: jne -> 0x00644c95 (jcc_false) | ctx: 0x00644c88: call 0x644cac ; 0x00644c8d: mov esi, dword ptr [ebp + 0xc] ; 0x00644c90: cmp esi, dword ptr [ebp + 0x10] ; 0x00644c93: jne 0x644c79
  - 0x00644c77: jmp -> 0x00644c9a (jmp) | ctx: 0x00644c70: mov ecx, dword ptr [eax] ; 0x00644c72: mov eax, dword ptr [ebp + 8] ; 0x00644c75: mov dword ptr [eax], ecx ; 0x00644c77: jmp 0x644c9a

### 0x00645be5
- blocks=1, insns=7, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCamperBehaviorProperties@GGL@@ slot 0 (target 0x00645c09, vtable 0x00bd8f58)
  - rtti_vtable_method: .?AVCCampBehaviorProperties@GGL@@ slot 1 (target 0x00645c11, vtable 0x00bd8ed4)
  - rtti_vtable_method: .?AVCCampBehaviorProperties@GGL@@ slot 0 (target 0x00645c01, vtable 0x00bd8ee4)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehaviorProps@GGL@@ slot 0 (target 0x00645c09, vtable 0x00be102c)
  - rtti_vtable_method: .?AVCWorkerFleeBehaviorProps@GGL@@ slot 0 (target 0x00645c09, vtable 0x00be178c)
- branch points:
  - none

### 0x00645c19
- blocks=1, insns=2, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCampBehaviorProperties@GGL@@ slot 0 (target 0x00645c19, vtable 0x00bd8ed4)
- branch points:
  - none

### 0x00645c1c
- blocks=3, insns=18, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCampBehavior@GGL@@ slot 1 (target 0x00645c3b, vtable 0x00bd8f10)
  - rtti_vtable_method: .?AVCCampBehavior@GGL@@ slot 3 (target 0x00645c43, vtable 0x00bd8f10)
  - caller_of_anchor_path: depth 1 (calls 0x0064629f at 0x00645c1f)
- branch points:
  - 0x00645c28: je -> 0x00645c34 (jcc_true) | ctx: 0x00645c1d: mov esi, ecx ; 0x00645c1f: call 0x64629f ; 0x00645c24: test byte ptr [ebp + 8], 1 ; 0x00645c28: je 0x645c34
  - 0x00645c28: je -> 0x00645c2a (jcc_false) | ctx: 0x00645c1d: mov esi, ecx ; 0x00645c1f: call 0x64629f ; 0x00645c24: test byte ptr [ebp + 8], 1 ; 0x00645c28: je 0x645c34

### 0x00645def
- blocks=1, insns=33, edges=4, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCampBehavior@GGL@@ slot 4 (target 0x00645def, vtable 0x00bd8f10)
- branch points:
  - none

### 0x00645e40
- blocks=1, insns=15, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCampBehavior@GGL@@ slot 5 (target 0x00645e40, vtable 0x00bd8f10)
- branch points:
  - none

### 0x00645e67
- blocks=1, insns=2, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCampBehavior@GGL@@ slot 0 (target 0x00645e67, vtable 0x00bd8f10)
- branch points:
  - none

### 0x00645e6a
- blocks=3, insns=18, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCamperBehaviorProperties@GGL@@ slot 1 (target 0x00645e89, vtable 0x00bd8f48)
  - caller_of_anchor_path: depth 1 (calls 0x0064629f at 0x00645e6d)
- branch points:
  - 0x00645e76: je -> 0x00645e82 (jcc_true) | ctx: 0x00645e6b: mov esi, ecx ; 0x00645e6d: call 0x646286 ; 0x00645e72: test byte ptr [ebp + 8], 1 ; 0x00645e76: je 0x645e82
  - 0x00645e76: je -> 0x00645e78 (jcc_false) | ctx: 0x00645e6b: mov esi, ecx ; 0x00645e6d: call 0x646286 ; 0x00645e72: test byte ptr [ebp + 8], 1 ; 0x00645e76: je 0x645e82

### 0x00645e91
- blocks=1, insns=3, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCamperBehaviorProperties@GGL@@ slot 0 (target 0x00645e91, vtable 0x00bd8f48)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehaviorProps@GGL@@ slot 0 (target 0x00645e91, vtable 0x00be101c)
  - rtti_vtable_method: .?AVCWorkerFleeBehaviorProps@GGL@@ slot 0 (target 0x00645e91, vtable 0x00be177c)
- branch points:
  - none

### 0x00645e98
- blocks=3, insns=18, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCamperBehavior@GGL@@ slot 1 (target 0x00645ebb, vtable 0x00bd8eb0)
  - rtti_vtable_method: .?AVCCamperBehavior@GGL@@ slot 3 (target 0x00645ec3, vtable 0x00bd8eb0)
- branch points:
  - 0x00645ea8: je -> 0x00645eb4 (jcc_true) | ctx: 0x00645e99: mov esi, ecx ; 0x00645e9b: mov dword ptr [esi + 4], 0xbc75c0 ; 0x00645ea2: mov dword ptr [esi], 0xbbe3c8 ; 0x00645ea8: je 0x645eb4
  - 0x00645ea8: je -> 0x00645eaa (jcc_false) | ctx: 0x00645e99: mov esi, ecx ; 0x00645e9b: mov dword ptr [esi + 4], 0xbc75c0 ; 0x00645ea2: mov dword ptr [esi], 0xbbe3c8 ; 0x00645ea8: je 0x645eb4

### 0x00645ff9
- blocks=1, insns=15, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCamperBehavior@GGL@@ slot 4 (target 0x00645ff9, vtable 0x00bd8eb0)
- branch points:
  - none

### 0x0064629f
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCPotentialCampSitePredicate@GGL@@ slot 1 (target 0x00646332, vtable 0x00bd8fac)
  - rtti_vtable_method: .?AVCCampWithFreeSlotPredicate@GGL@@ slot 1 (target 0x006462cd, vtable 0x00bd8fd8)
- branch points:
  - none

### 0x006464b5
- blocks=1, insns=3, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCampWithFreeSlotPredicate@GGL@@ slot 0 (target 0x006464b5, vtable 0x00bd8fd8)
- branch points:
  - none

### 0x00648cb5
- blocks=6, insns=67, edges=11, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00638c75 at 0x00648cfb)
- branch points:
  - 0x00648cd5: jle -> 0x00648cda (jcc_true) | ctx: 0x00648cc7: mov ecx, dword ptr [eax + ecx*4] ; 0x00648cca: mov eax, dword ptr [0xf62d54] ; 0x00648ccf: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00648cd5: jle 0x648cda
  - 0x00648cd5: jle -> 0x00648cd7 (jcc_false) | ctx: 0x00648cc7: mov ecx, dword ptr [eax + ecx*4] ; 0x00648cca: mov eax, dword ptr [0xf62d54] ; 0x00648ccf: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00648cd5: jle 0x648cda
  - 0x00648cd7: jmp -> 0x00648ce3 (jmp) | ctx: 0x00648cd7: jmp 0x648ce3
  - 0x00648cf7: jne -> 0x00648cd9 (jcc_true) | ctx: 0x00648cea: call 0xab6ba9 ; 0x00648cef: cmp dword ptr [0xf62d54], -1 ; 0x00648cf6: pop ecx ; 0x00648cf7: jne 0x648cd9
  - 0x00648cf7: jne -> 0x00648cf9 (jcc_false) | ctx: 0x00648cea: call 0xab6ba9 ; 0x00648cef: cmp dword ptr [0xf62d54], -1 ; 0x00648cf6: pop ecx ; 0x00648cf7: jne 0x648cd9
  - 0x00648d83: jmp -> 0x00648cd9 (jmp) | ctx: 0x00648d7e: add esp, 0xc ; 0x00648d81: pop edi ; 0x00648d82: pop esi ; 0x00648d83: jmp 0x648cd9

### 0x0064d55d
- blocks=4, insns=111, edges=12, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0062767a at 0x0064d59f)
- branch points:
  - 0x0064d57d: jg -> 0x0064d588 (jcc_true) | ctx: 0x0064d56f: mov ecx, dword ptr [eax + ecx*4] ; 0x0064d572: mov eax, dword ptr [0xf64478] ; 0x0064d577: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0064d57d: jg 0x64d588
  - 0x0064d57d: jg -> 0x0064d57f (jcc_false) | ctx: 0x0064d56f: mov ecx, dword ptr [eax + ecx*4] ; 0x0064d572: mov eax, dword ptr [0xf64478] ; 0x0064d577: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0064d57d: jg 0x64d588
  - 0x0064d59a: jne -> 0x0064d57f (jcc_true) | ctx: 0x0064d58d: call 0xab6ba9 ; 0x0064d592: cmp dword ptr [0xf64478], -1 ; 0x0064d599: pop ecx ; 0x0064d59a: jne 0x64d57f
  - 0x0064d59a: jne -> 0x0064d59c (jcc_false) | ctx: 0x0064d58d: call 0xab6ba9 ; 0x0064d592: cmp dword ptr [0xf64478], -1 ; 0x0064d599: pop ecx ; 0x0064d59a: jne 0x64d57f
  - 0x0064d6d4: jmp -> 0x0064d57f (jmp) | ctx: 0x0064d6d1: pop edi ; 0x0064d6d2: pop esi ; 0x0064d6d3: pop ebx ; 0x0064d6d4: jmp 0x64d57f

### 0x0064ec2c
- blocks=1, insns=26, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0064ed43)
- branch points:
  - none

### 0x00651640
- blocks=3, insns=51, edges=5, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0065164f)
- branch points:
  - 0x0065166f: je -> 0x00651686 (jcc_true) | ctx: 0x00651667: sub ebx, dword ptr [esi] ; 0x00651669: sar ebx, 3 ; 0x0065166c: cmp dword ptr [esi], 0 ; 0x0065166f: je 0x651686
  - 0x0065166f: je -> 0x00651671 (jcc_false) | ctx: 0x00651667: sub ebx, dword ptr [esi] ; 0x00651669: sar ebx, 3 ; 0x0065166c: cmp dword ptr [esi], 0 ; 0x0065166f: je 0x651686

### 0x006516a1
- blocks=5, insns=31, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00651640 at 0x006516d4)
- branch points:
  - 0x006516b4: jae -> 0x006516d9 (jcc_true) | ctx: 0x006516ad: sub eax, edx ; 0x006516af: sar eax, 3 ; 0x006516b2: cmp eax, ecx ; 0x006516b4: jae 0x6516d9
  - 0x006516b4: jae -> 0x006516b6 (jcc_false) | ctx: 0x006516ad: sub eax, edx ; 0x006516af: sar eax, 3 ; 0x006516b2: cmp eax, ecx ; 0x006516b4: jae 0x6516d9
  - 0x006516c4: jb -> 0x006516de (jcc_true) | ctx: 0x006516bd: sar edx, 3 ; 0x006516c0: sub eax, edx ; 0x006516c2: cmp eax, ecx ; 0x006516c4: jb 0x6516de
  - 0x006516c4: jb -> 0x006516c6 (jcc_false) | ctx: 0x006516bd: sar edx, 3 ; 0x006516c0: sub eax, edx ; 0x006516c2: cmp eax, ecx ; 0x006516c4: jb 0x6516de

### 0x0065b35b
- blocks=1, insns=19, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005652c9 at 0x0065b48f)
- branch points:
  - none

### 0x0065b4db
- blocks=14, insns=121, edges=24, jcc=7, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0065bd8c at 0x0065b56f)
- branch points:
  - 0x0065b4e6: je -> 0x0065b593 (jcc_true) | ctx: 0x0065b4de: mov dword ptr [ebp - 0x10], esp ; 0x0065b4e1: mov dword ptr [ebp - 0x14], edi ; 0x0065b4e4: cmp edi, ebx ; 0x0065b4e6: je 0x65b593
  - 0x0065b4e6: je -> 0x0065b4ec (jcc_false) | ctx: 0x0065b4de: mov dword ptr [ebp - 0x10], esp ; 0x0065b4e1: mov dword ptr [ebp - 0x14], edi ; 0x0065b4e4: cmp edi, ebx ; 0x0065b4e6: je 0x65b593
  - 0x0065b4f1: jne -> 0x0065b4fa (jcc_true) | ctx: 0x0065b4ec: mov eax, dword ptr [ebx] ; 0x0065b4ee: cmp eax, dword ptr [ebx + 4] ; 0x0065b4f1: jne 0x65b4fa
  - 0x0065b4f1: jne -> 0x0065b4f3 (jcc_false) | ctx: 0x0065b4ec: mov eax, dword ptr [ebx] ; 0x0065b4ee: cmp eax, dword ptr [ebx + 4] ; 0x0065b4f1: jne 0x65b4fa
  - 0x0065b50c: ja -> 0x0065b52b (jcc_true) | ctx: 0x0065b504: sar edx, 3 ; 0x0065b507: sar esi, 3 ; 0x0065b50a: cmp edx, esi ; 0x0065b50c: ja 0x65b52b
  - 0x0065b50c: ja -> 0x0065b50e (jcc_false) | ctx: 0x0065b504: sar edx, 3 ; 0x0065b507: sar esi, 3 ; 0x0065b50a: cmp edx, esi ; 0x0065b50c: ja 0x65b52b
  - 0x0065b4f5: jmp -> 0x0065b590 (jmp) | ctx: 0x0065b4f3: mov eax, dword ptr [edi] ; 0x0065b4f5: jmp 0x65b590
  - 0x0065b535: ja -> 0x0065b552 (jcc_true) | ctx: 0x0065b52e: sub ecx, dword ptr [edi] ; 0x0065b530: sar ecx, 3 ; 0x0065b533: cmp edx, ecx ; 0x0065b535: ja 0x65b552
  - 0x0065b535: ja -> 0x0065b537 (jcc_false) | ctx: 0x0065b52e: sub ecx, dword ptr [edi] ; 0x0065b530: sar ecx, 3 ; 0x0065b533: cmp edx, ecx ; 0x0065b535: ja 0x65b552
  - 0x0065b529: jmp -> 0x0065b590 (jmp) | ctx: 0x0065b521: mov eax, dword ptr [edi] ; 0x0065b523: sar ecx, 3 ; 0x0065b526: lea eax, [eax + ecx*8] ; 0x0065b529: jmp 0x65b590
  - 0x0065b555: je -> 0x0065b564 (jcc_true) | ctx: 0x0065b552: cmp dword ptr [edi], 0 ; 0x0065b555: je 0x65b564
  - 0x0065b555: je -> 0x0065b557 (jcc_false) | ctx: 0x0065b552: cmp dword ptr [edi], 0 ; 0x0065b555: je 0x65b564
  - 0x0065b550: jmp -> 0x0065b588 (jmp) | ctx: 0x0065b549: push dword ptr [edi + 4] ; 0x0065b54c: push dword ptr [ebx + 4] ; 0x0065b54f: push esi ; 0x0065b550: jmp 0x65b588
  - 0x0065b576: je -> 0x0065b593 (jcc_true) | ctx: 0x0065b56e: push eax ; 0x0065b56f: call 0x65bd89 ; 0x0065b574: test al, al ; 0x0065b576: je 0x65b593
  - 0x0065b576: je -> 0x0065b578 (jcc_false) | ctx: 0x0065b56e: push eax ; 0x0065b56f: call 0x65bd89 ; 0x0065b574: test al, al ; 0x0065b576: je 0x65b593
  - 0x0065b576: je -> 0x0065b593 (jcc_true) | ctx: 0x0065b56e: push eax ; 0x0065b56f: call 0x65bd89 ; 0x0065b574: test al, al ; 0x0065b576: je 0x65b593
  - 0x0065b576: je -> 0x0065b578 (jcc_false) | ctx: 0x0065b56e: push eax ; 0x0065b56f: call 0x65bd89 ; 0x0065b574: test al, al ; 0x0065b576: je 0x65b593

### 0x0065bd8c
- blocks=6, insns=36, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0065bdb2)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0065bdf7)
- branch points:
  - 0x0065bd9f: jne -> 0x0065bda5 (jcc_true) | ctx: 0x0065bd97: mov dword ptr [esi + 4], eax ; 0x0065bd9a: mov dword ptr [esi + 8], eax ; 0x0065bd9d: test edi, edi ; 0x0065bd9f: jne 0x65bda5
  - 0x0065bd9f: jne -> 0x0065bda1 (jcc_false) | ctx: 0x0065bd97: mov dword ptr [esi + 4], eax ; 0x0065bd9a: mov dword ptr [esi + 8], eax ; 0x0065bd9d: test edi, edi ; 0x0065bd9f: jne 0x65bda5
  - 0x0065bdab: ja -> 0x0065bdcf (jcc_true) | ctx: 0x0065bda5: cmp edi, 0x1fffffff ; 0x0065bdab: ja 0x65bdcf
  - 0x0065bdab: ja -> 0x0065bdad (jcc_false) | ctx: 0x0065bda5: cmp edi, 0x1fffffff ; 0x0065bdab: ja 0x65bdcf
  - 0x0065bda3: jmp -> 0x0065bdc9 (jmp) | ctx: 0x0065bda1: xor al, al ; 0x0065bda3: jmp 0x65bdc9

### 0x0065e2e1
- blocks=3, insns=31, edges=5, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005781c1 at 0x0065e3c6)
- branch points:
  - 0x0065e2fd: je -> 0x0065e31f (jcc_true) | ctx: 0x0065e2f8: xor eax, eax ; 0x0065e2fa: pop esi ; 0x0065e2fb: test ecx, ecx ; 0x0065e2fd: je 0x65e31f
  - 0x0065e2fd: je -> 0x0065e2ff (jcc_false) | ctx: 0x0065e2f8: xor eax, eax ; 0x0065e2fa: pop esi ; 0x0065e2fb: test ecx, ecx ; 0x0065e2fd: je 0x65e31f

### 0x0065f312
- blocks=3, insns=28, edges=5, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0065f36d)
- branch points:
  - 0x0065f32d: je -> 0x0065f33d (jcc_true) | ctx: 0x0065f327: sub edi, eax ; 0x0065f329: mov esi, edi ; 0x0065f32b: cmp edi, ebx ; 0x0065f32d: je 0x65f33d
  - 0x0065f32d: je -> 0x0065f32f (jcc_false) | ctx: 0x0065f327: sub edi, eax ; 0x0065f329: mov esi, edi ; 0x0065f32b: cmp edi, ebx ; 0x0065f32d: je 0x65f33d
  - 0x0065f33b: jne -> 0x0065f32f (jcc_true) | ctx: 0x0065f331: call 0x61b1c3 ; 0x0065f336: add esi, 0x24 ; 0x0065f339: cmp esi, ebx ; 0x0065f33b: jne 0x65f32f
  - 0x0065f33b: jne -> 0x0065f33d (jcc_false) | ctx: 0x0065f331: call 0x61b1c3 ; 0x0065f336: add esi, 0x24 ; 0x0065f339: cmp esi, ebx ; 0x0065f33b: jne 0x65f32f

### 0x0065f4c6
- blocks=5, insns=62, edges=8, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0065f312 at 0x0065f4e9)
- branch points:
  - 0x0065f4e2: jbe -> 0x0065f501 (jcc_true) | ctx: 0x0065f4db: mov ecx, eax ; 0x0065f4dd: mov dword ptr [ebp - 0x14], esi ; 0x0065f4e0: cmp ecx, edi ; 0x0065f4e2: jbe 0x65f501
  - 0x0065f4e2: jbe -> 0x0065f4e4 (jcc_false) | ctx: 0x0065f4db: mov ecx, eax ; 0x0065f4dd: mov dword ptr [ebp - 0x14], esi ; 0x0065f4e0: cmp ecx, edi ; 0x0065f4e2: jbe 0x65f501
  - 0x0065f501: jae -> 0x0065f4ee (jcc_true) | ctx: 0x0065f501: jae 0x65f4ee
  - 0x0065f501: jae -> 0x0065f503 (jcc_false) | ctx: 0x0065f501: jae 0x65f4ee
  - 0x0065f53f: jmp -> 0x0065f4ee (jmp) | ctx: 0x0065f537: sub edi, eax ; 0x0065f539: imul eax, edi, 0x24 ; 0x0065f53c: add dword ptr [esi + 4], eax ; 0x0065f53f: jmp 0x65f4ee

### 0x00660af3
- blocks=1, insns=3, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerFleeBehavior@GGL@@ slot 0 (target 0x00660af3, vtable 0x00be17a8)
- branch points:
  - none

### 0x00668ba1
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00668ca6 at 0x00668bb5)
- branch points:
  - 0x00668ba6: jne -> 0x00668bb5 (jcc_true) | ctx: 0x00668ba1: push edi ; 0x00668ba2: mov edi, ecx ; 0x00668ba4: test esi, esi ; 0x00668ba6: jne 0x668bb5
  - 0x00668ba6: jne -> 0x00668ba8 (jcc_false) | ctx: 0x00668ba1: push edi ; 0x00668ba2: mov edi, ecx ; 0x00668ba4: test esi, esi ; 0x00668ba6: jne 0x668bb5

### 0x00668ca6
- blocks=6, insns=52, edges=10, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00668d3f)
- branch points:
  - 0x00668cc6: jle -> 0x00668ccb (jcc_true) | ctx: 0x00668cb8: mov ecx, dword ptr [eax + ecx*4] ; 0x00668cbb: mov eax, dword ptr [0xf69270] ; 0x00668cc0: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00668cc6: jle 0x668ccb
  - 0x00668cc6: jle -> 0x00668cc8 (jcc_false) | ctx: 0x00668cb8: mov ecx, dword ptr [eax + ecx*4] ; 0x00668cbb: mov eax, dword ptr [0xf69270] ; 0x00668cc0: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00668cc6: jle 0x668ccb
  - 0x00668cc8: jmp -> 0x00668cd4 (jmp) | ctx: 0x00668cc8: jmp 0x668cd4
  - 0x00668ce8: jne -> 0x00668cca (jcc_true) | ctx: 0x00668cdb: call 0xab6ba9 ; 0x00668ce0: cmp dword ptr [0xf69270], -1 ; 0x00668ce7: pop ecx ; 0x00668ce8: jne 0x668cca
  - 0x00668ce8: jne -> 0x00668cea (jcc_false) | ctx: 0x00668cdb: call 0xab6ba9 ; 0x00668ce0: cmp dword ptr [0xf69270], -1 ; 0x00668ce7: pop ecx ; 0x00668ce8: jne 0x668cca
  - 0x00668d37: jmp -> 0x00668cca (jmp) | ctx: 0x00668d32: add esp, 0xc ; 0x00668d35: pop edi ; 0x00668d36: pop esi ; 0x00668d37: jmp 0x668cca

### 0x00668e1a
- blocks=64, insns=319, edges=120, jcc=46, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0066912f at 0x006690a0)
- branch points:
  - 0x00668e37: je -> 0x00668e3e (jcc_true) | ctx: 0x00668e2c: call 0x577cf5 ; 0x00668e31: mov ecx, dword ptr [ebx] ; 0x00668e33: cmp byte ptr [ecx + 0xd], 0 ; 0x00668e37: je 0x668e3e
  - 0x00668e37: je -> 0x00668e39 (jcc_false) | ctx: 0x00668e2c: call 0x577cf5 ; 0x00668e31: mov ecx, dword ptr [ebx] ; 0x00668e33: cmp byte ptr [ecx + 0xd], 0 ; 0x00668e37: je 0x668e3e
  - 0x00668e45: je -> 0x00668e4b (jcc_true) | ctx: 0x00668e3e: mov eax, dword ptr [ebx + 8] ; 0x00668e41: cmp byte ptr [eax + 0xd], 0 ; 0x00668e45: je 0x668e4b
  - 0x00668e45: je -> 0x00668e47 (jcc_false) | ctx: 0x00668e3e: mov eax, dword ptr [ebx + 8] ; 0x00668e41: cmp byte ptr [eax + 0xd], 0 ; 0x00668e45: je 0x668e4b
  - 0x00668e3c: jmp -> 0x00668e55 (jmp) | ctx: 0x00668e39: mov edi, dword ptr [ebx + 8] ; 0x00668e3c: jmp 0x668e55
  - 0x00668e53: jne -> 0x00668ec9 (jcc_true) | ctx: 0x00668e4b: mov edx, dword ptr [ebp + 0xc] ; 0x00668e4e: mov edi, dword ptr [edx + 8] ; 0x00668e51: cmp edx, ebx ; 0x00668e53: jne 0x668ec9
  - 0x00668e53: jne -> 0x00668e55 (jcc_false) | ctx: 0x00668e4b: mov edx, dword ptr [ebp + 0xc] ; 0x00668e4e: mov edi, dword ptr [edx + 8] ; 0x00668e51: cmp edx, ebx ; 0x00668e53: jne 0x668ec9
  - 0x00668e49: jmp -> 0x00668e55 (jmp) | ctx: 0x00668e47: mov edi, ecx ; 0x00668e49: jmp 0x668e55
  - 0x00668e5c: jne -> 0x00668e61 (jcc_true) | ctx: 0x00668e55: cmp byte ptr [edi + 0xd], 0 ; 0x00668e59: mov esi, dword ptr [ebx + 4] ; 0x00668e5c: jne 0x668e61
  - 0x00668e5c: jne -> 0x00668e5e (jcc_false) | ctx: 0x00668e55: cmp byte ptr [edi + 0xd], 0 ; 0x00668e59: mov esi, dword ptr [ebx + 4] ; 0x00668e5c: jne 0x668e61
  - 0x00668ed3: jne -> 0x00668ed9 (jcc_true) | ctx: 0x00668ecc: mov eax, dword ptr [ebx] ; 0x00668ece: mov dword ptr [edx], eax ; 0x00668ed0: cmp edx, dword ptr [ebx + 8] ; 0x00668ed3: jne 0x668ed9
  - 0x00668ed3: jne -> 0x00668ed5 (jcc_false) | ctx: 0x00668ecc: mov eax, dword ptr [ebx] ; 0x00668ece: mov dword ptr [edx], eax ; 0x00668ed0: cmp edx, dword ptr [ebx + 8] ; 0x00668ed3: jne 0x668ed9
  - 0x00668e69: jne -> 0x00668e70 (jcc_true) | ctx: 0x00668e61: mov edx, dword ptr [ebp - 4] ; 0x00668e64: mov eax, dword ptr [edx] ; 0x00668e66: cmp dword ptr [eax + 4], ebx ; 0x00668e69: jne 0x668e70
  - 0x00668e69: jne -> 0x00668e6b (jcc_false) | ctx: 0x00668e61: mov edx, dword ptr [ebp - 4] ; 0x00668e64: mov eax, dword ptr [edx] ; 0x00668e66: cmp dword ptr [eax + 4], ebx ; 0x00668e69: jne 0x668e70
  - 0x00668e69: jne -> 0x00668e70 (jcc_true) | ctx: 0x00668e61: mov edx, dword ptr [ebp - 4] ; 0x00668e64: mov eax, dword ptr [edx] ; 0x00668e66: cmp dword ptr [eax + 4], ebx ; 0x00668e69: jne 0x668e70
  - 0x00668e69: jne -> 0x00668e6b (jcc_false) | ctx: 0x00668e61: mov edx, dword ptr [ebp - 4] ; 0x00668e64: mov eax, dword ptr [edx] ; 0x00668e66: cmp dword ptr [eax + 4], ebx ; 0x00668e69: jne 0x668e70
  - 0x00668ee0: jne -> 0x00668ee5 (jcc_true) | ctx: 0x00668ed9: cmp byte ptr [edi + 0xd], 0 ; 0x00668edd: mov esi, dword ptr [edx + 4] ; 0x00668ee0: jne 0x668ee5
  - 0x00668ee0: jne -> 0x00668ee2 (jcc_false) | ctx: 0x00668ed9: cmp byte ptr [edi + 0xd], 0 ; 0x00668edd: mov esi, dword ptr [edx + 4] ; 0x00668ee0: jne 0x668ee5
  - 0x00668ed7: jmp -> 0x00668ef3 (jmp) | ctx: 0x00668ed5: mov esi, edx ; 0x00668ed7: jmp 0x668ef3
  - 0x00668e72: jne -> 0x00668e78 (jcc_true) | ctx: 0x00668e70: cmp dword ptr [esi], ebx ; 0x00668e72: jne 0x668e78
  - 0x00668e72: jne -> 0x00668e74 (jcc_false) | ctx: 0x00668e70: cmp dword ptr [esi], ebx ; 0x00668e72: jne 0x668e78
  - 0x00668e6e: jmp -> 0x00668e7b (jmp) | ctx: 0x00668e6b: mov dword ptr [eax + 4], edi ; 0x00668e6e: jmp 0x668e7b
  - 0x00668efb: jne -> 0x00668f02 (jcc_true) | ctx: 0x00668ef3: mov ecx, dword ptr [ebp - 4] ; 0x00668ef6: mov eax, dword ptr [ecx] ; 0x00668ef8: cmp dword ptr [eax + 4], ebx ; 0x00668efb: jne 0x668f02
  - 0x00668efb: jne -> 0x00668efd (jcc_false) | ctx: 0x00668ef3: mov ecx, dword ptr [ebp - 4] ; 0x00668ef6: mov eax, dword ptr [ecx] ; 0x00668ef8: cmp dword ptr [eax + 4], ebx ; 0x00668efb: jne 0x668f02
  - 0x00668efb: jne -> 0x00668f02 (jcc_true) | ctx: 0x00668ef3: mov ecx, dword ptr [ebp - 4] ; 0x00668ef6: mov eax, dword ptr [ecx] ; 0x00668ef8: cmp dword ptr [eax + 4], ebx ; 0x00668efb: jne 0x668f02
  - 0x00668efb: jne -> 0x00668efd (jcc_false) | ctx: 0x00668ef3: mov ecx, dword ptr [ebp - 4] ; 0x00668ef6: mov eax, dword ptr [ecx] ; 0x00668ef8: cmp dword ptr [eax + 4], ebx ; 0x00668efb: jne 0x668f02
  - 0x00668efb: jne -> 0x00668f02 (jcc_true) | ctx: 0x00668ef3: mov ecx, dword ptr [ebp - 4] ; 0x00668ef6: mov eax, dword ptr [ecx] ; 0x00668ef8: cmp dword ptr [eax + 4], ebx ; 0x00668efb: jne 0x668f02
  - 0x00668efb: jne -> 0x00668efd (jcc_false) | ctx: 0x00668ef3: mov ecx, dword ptr [ebp - 4] ; 0x00668ef6: mov eax, dword ptr [ecx] ; 0x00668ef8: cmp dword ptr [eax + 4], ebx ; 0x00668efb: jne 0x668f02
  - 0x00668e7f: jne -> 0x00668e9f (jcc_true) | ctx: 0x00668e78: mov dword ptr [esi + 8], edi ; 0x00668e7b: mov eax, dword ptr [edx] ; 0x00668e7d: cmp dword ptr [eax], ebx ; 0x00668e7f: jne 0x668e9f
  - 0x00668e7f: jne -> 0x00668e81 (jcc_false) | ctx: 0x00668e78: mov dword ptr [esi + 8], edi ; 0x00668e7b: mov eax, dword ptr [edx] ; 0x00668e7d: cmp dword ptr [eax], ebx ; 0x00668e7f: jne 0x668e9f
  - 0x00668e76: jmp -> 0x00668e7b (jmp) | ctx: 0x00668e74: mov dword ptr [esi], edi ; 0x00668e76: jmp 0x668e7b
  - 0x00668e7f: jne -> 0x00668e9f (jcc_true) | ctx: 0x00668e7b: mov eax, dword ptr [edx] ; 0x00668e7d: cmp dword ptr [eax], ebx ; 0x00668e7f: jne 0x668e9f
  - 0x00668e7f: jne -> 0x00668e81 (jcc_false) | ctx: 0x00668e7b: mov eax, dword ptr [edx] ; 0x00668e7d: cmp dword ptr [eax], ebx ; 0x00668e7f: jne 0x668e9f
  - 0x00668f07: jne -> 0x00668f0d (jcc_true) | ctx: 0x00668f02: mov eax, dword ptr [ebx + 4] ; 0x00668f05: cmp dword ptr [eax], ebx ; 0x00668f07: jne 0x668f0d
  - 0x00668f07: jne -> 0x00668f09 (jcc_false) | ctx: 0x00668f02: mov eax, dword ptr [ebx + 4] ; 0x00668f05: cmp dword ptr [eax], ebx ; 0x00668f07: jne 0x668f0d
  - 0x00668f00: jmp -> 0x00668f10 (jmp) | ctx: 0x00668efd: mov dword ptr [eax + 4], edx ; 0x00668f00: jmp 0x668f10
  - 0x00668ea4: jne -> 0x00668f25 (jcc_true) | ctx: 0x00668e9f: mov eax, dword ptr [edx] ; 0x00668ea1: cmp dword ptr [eax + 8], ebx ; 0x00668ea4: jne 0x668f25
  - 0x00668ea4: jne -> 0x00668ea6 (jcc_false) | ctx: 0x00668e9f: mov eax, dword ptr [edx] ; 0x00668ea1: cmp dword ptr [eax + 8], ebx ; 0x00668ea4: jne 0x668f25
  - 0x00668e85: je -> 0x00668e8b (jcc_true) | ctx: 0x00668e81: cmp byte ptr [edi + 0xd], 0 ; 0x00668e85: je 0x668e8b
  - 0x00668e85: je -> 0x00668e87 (jcc_false) | ctx: 0x00668e81: cmp byte ptr [edi + 0xd], 0 ; 0x00668e85: je 0x668e8b
  - 0x00668f29: jne -> 0x00669018 (jcc_true) | ctx: 0x00668f1f: mov edx, dword ptr [ebp - 4] ; 0x00668f22: mov byte ptr [ebx + 0xc], cl ; 0x00668f25: cmp byte ptr [ebx + 0xc], 1 ; 0x00668f29: jne 0x669018
  - 0x00668f29: jne -> 0x00668f2f (jcc_false) | ctx: 0x00668f1f: mov edx, dword ptr [ebp - 4] ; 0x00668f22: mov byte ptr [ebx + 0xc], cl ; 0x00668f25: cmp byte ptr [ebx + 0xc], 1 ; 0x00668f29: jne 0x669018
  - 0x00668f0b: jmp -> 0x00668f10 (jmp) | ctx: 0x00668f09: mov dword ptr [eax], edx ; 0x00668f0b: jmp 0x668f10
  - 0x00668f29: jne -> 0x00669018 (jcc_true) | ctx: 0x00668f1f: mov edx, dword ptr [ebp - 4] ; 0x00668f22: mov byte ptr [ebx + 0xc], cl ; 0x00668f25: cmp byte ptr [ebx + 0xc], 1 ; 0x00668f29: jne 0x669018
  - 0x00668f29: jne -> 0x00668f2f (jcc_false) | ctx: 0x00668f1f: mov edx, dword ptr [ebp - 4] ; 0x00668f22: mov byte ptr [ebx + 0xc], cl ; 0x00668f25: cmp byte ptr [ebx + 0xc], 1 ; 0x00668f29: jne 0x669018
  - 0x00668f29: jne -> 0x00669018 (jcc_true) | ctx: 0x00668f25: cmp byte ptr [ebx + 0xc], 1 ; 0x00668f29: jne 0x669018
  - 0x00668f29: jne -> 0x00668f2f (jcc_false) | ctx: 0x00668f25: cmp byte ptr [ebx + 0xc], 1 ; 0x00668f29: jne 0x669018
  - 0x00668eaa: je -> 0x00668eb0 (jcc_true) | ctx: 0x00668ea6: cmp byte ptr [edi + 0xd], 0 ; 0x00668eaa: je 0x668eb0
  - 0x00668eaa: je -> 0x00668eac (jcc_false) | ctx: 0x00668ea6: cmp byte ptr [edi + 0xd], 0 ; 0x00668eaa: je 0x668eb0
  - 0x00668e8f: jmp -> 0x00668e95 (jmp) | ctx: 0x00668e8b: mov ecx, dword ptr [edi] ; 0x00668e8d: mov eax, edi ; 0x00668e8f: jmp 0x668e95
  - 0x00668e89: jmp -> 0x00668e9b (jmp) | ctx: 0x00668e87: mov eax, esi ; 0x00668e89: jmp 0x668e9b
  - 0x00669030: je -> 0x00669036 (jcc_true) | ctx: 0x0066902c: pop esi ; 0x0066902d: pop ebx ; 0x0066902e: test eax, eax ; 0x00669030: je 0x669036
  - 0x00669030: je -> 0x00669032 (jcc_false) | ctx: 0x0066902c: pop esi ; 0x0066902d: pop ebx ; 0x0066902e: test eax, eax ; 0x00669030: je 0x669036
  - 0x00668f34: je -> 0x00669014 (jcc_true) | ctx: 0x00668f2f: mov eax, dword ptr [edx] ; 0x00668f31: cmp edi, dword ptr [eax + 4] ; 0x00668f34: je 0x669014
  - 0x00668f34: je -> 0x00668f3a (jcc_false) | ctx: 0x00668f2f: mov eax, dword ptr [edx] ; 0x00668f31: cmp edi, dword ptr [eax + 4] ; 0x00668f34: je 0x669014
  - 0x00668eb5: jmp -> 0x00668ebc (jmp) | ctx: 0x00668eb0: mov ecx, dword ptr [edi + 8] ; 0x00668eb3: mov eax, edi ; 0x00668eb5: jmp 0x668ebc
  - 0x00668eae: jmp -> 0x00668ec2 (jmp) | ctx: 0x00668eac: mov eax, esi ; 0x00668eae: jmp 0x668ec2
  - 0x00668e99: je -> 0x00668e91 (jcc_true) | ctx: 0x00668e95: cmp byte ptr [ecx + 0xd], 0 ; 0x00668e99: je 0x668e91
  - 0x00668e99: je -> 0x00668e9b (jcc_false) | ctx: 0x00668e95: cmp byte ptr [ecx + 0xd], 0 ; 0x00668e99: je 0x668e91
  - 0x00668ea4: jne -> 0x00668f25 (jcc_true) | ctx: 0x00668e9d: mov dword ptr [ecx], eax ; 0x00668e9f: mov eax, dword ptr [edx] ; 0x00668ea1: cmp dword ptr [eax + 8], ebx ; 0x00668ea4: jne 0x668f25
  - 0x00668ea4: jne -> 0x00668ea6 (jcc_false) | ctx: 0x00668e9d: mov dword ptr [ecx], eax ; 0x00668e9f: mov eax, dword ptr [edx] ; 0x00668ea1: cmp dword ptr [eax + 8], ebx ; 0x00668ea4: jne 0x668f25
  - 0x00669030: je -> 0x00669036 (jcc_true) | ctx: 0x0066902c: pop esi ; 0x0066902d: pop ebx ; 0x0066902e: test eax, eax ; 0x00669030: je 0x669036
  - 0x00669030: je -> 0x00669032 (jcc_false) | ctx: 0x0066902c: pop esi ; 0x0066902d: pop ebx ; 0x0066902e: test eax, eax ; 0x00669030: je 0x669036
  - 0x00668f47: jne -> 0x00669014 (jcc_true) | ctx: 0x00668f3e: mov dword ptr [ebp - 0xc], esi ; 0x00668f41: mov dword ptr [ebp - 8], esi ; 0x00668f44: mov dword ptr [ebp - 0x10], esi ; 0x00668f47: jne 0x669014
  - 0x00668f47: jne -> 0x00668f4d (jcc_false) | ctx: 0x00668f3e: mov dword ptr [ebp - 0xc], esi ; 0x00668f41: mov dword ptr [ebp - 8], esi ; 0x00668f44: mov dword ptr [ebp - 0x10], esi ; 0x00668f47: jne 0x669014
  - 0x00668ec0: je -> 0x00668eb7 (jcc_true) | ctx: 0x00668ebc: cmp byte ptr [ecx + 0xd], 0 ; 0x00668ec0: je 0x668eb7
  - 0x00668ec0: je -> 0x00668ec2 (jcc_false) | ctx: 0x00668ebc: cmp byte ptr [ecx + 0xd], 0 ; 0x00668ec0: je 0x668eb7
  - 0x00668ec7: jmp -> 0x00668f25 (jmp) | ctx: 0x00668ec2: mov ecx, dword ptr [edx] ; 0x00668ec4: mov dword ptr [ecx + 8], eax ; 0x00668ec7: jmp 0x668f25
  - 0x00668e99: je -> 0x00668e91 (jcc_true) | ctx: 0x00668e91: mov eax, ecx ; 0x00668e93: mov ecx, dword ptr [eax] ; 0x00668e95: cmp byte ptr [ecx + 0xd], 0 ; 0x00668e99: je 0x668e91
  - 0x00668e99: je -> 0x00668e9b (jcc_false) | ctx: 0x00668e91: mov eax, ecx ; 0x00668e93: mov ecx, dword ptr [eax] ; 0x00668e95: cmp byte ptr [ecx + 0xd], 0 ; 0x00668e99: je 0x668e91
  - 0x00668f51: jne -> 0x00668fc7 (jcc_true) | ctx: 0x00668f4d: mov ecx, dword ptr [esi] ; 0x00668f4f: cmp edi, ecx ; 0x00668f51: jne 0x668fc7
  - 0x00668f51: jne -> 0x00668f53 (jcc_false) | ctx: 0x00668f4d: mov ecx, dword ptr [esi] ; 0x00668f4f: cmp edi, ecx ; 0x00668f51: jne 0x668fc7
  - 0x00668ec0: je -> 0x00668eb7 (jcc_true) | ctx: 0x00668eb7: mov eax, ecx ; 0x00668eb9: mov ecx, dword ptr [eax + 8] ; 0x00668ebc: cmp byte ptr [ecx + 0xd], 0 ; 0x00668ec0: je 0x668eb7
  - 0x00668ec0: je -> 0x00668ec2 (jcc_false) | ctx: 0x00668eb7: mov eax, ecx ; 0x00668eb9: mov ecx, dword ptr [eax + 8] ; 0x00668ebc: cmp byte ptr [ecx + 0xd], 0 ; 0x00668ec0: je 0x668eb7
  - 0x00668fcb: jne -> 0x00668fe2 (jcc_true) | ctx: 0x00668fc7: cmp byte ptr [ecx + 0xc], 0 ; 0x00668fcb: jne 0x668fe2
  - 0x00668fcb: jne -> 0x00668fcd (jcc_false) | ctx: 0x00668fc7: cmp byte ptr [ecx + 0xc], 0 ; 0x00668fcb: jne 0x668fe2
  - 0x00668f5a: jne -> 0x00668f72 (jcc_true) | ctx: 0x00668f53: mov ecx, dword ptr [esi + 8] ; 0x00668f56: cmp byte ptr [ecx + 0xc], 0 ; 0x00668f5a: jne 0x668f72
  - 0x00668f5a: jne -> 0x00668f5c (jcc_false) | ctx: 0x00668f53: mov ecx, dword ptr [esi + 8] ; 0x00668f56: cmp byte ptr [ecx + 0xc], 0 ; 0x00668f5a: jne 0x668f72
  - 0x00668fe6: jne -> 0x00668ffd (jcc_true) | ctx: 0x00668fe2: cmp byte ptr [ecx + 0xd], 0 ; 0x00668fe6: jne 0x668ffd
  - 0x00668fe6: jne -> 0x00668fe8 (jcc_false) | ctx: 0x00668fe2: cmp byte ptr [ecx + 0xd], 0 ; 0x00668fe6: jne 0x668ffd
  - ... 28 more

### 0x0066912f
- blocks=3, insns=19, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCPath@GGL@@ slot 1 (target 0x00669167, vtable 0x00bdb29c)
- branch points:
  - 0x00669141: je -> 0x00669150 (jcc_true) | ctx: 0x00669132: mov dword ptr [esi], 0xbdb25c ; 0x00669138: call 0x633f76 ; 0x0066913d: test byte ptr [ebp + 8], 1 ; 0x00669141: je 0x669150
  - 0x00669141: je -> 0x00669143 (jcc_false) | ctx: 0x00669132: mov dword ptr [esi], 0xbdb25c ; 0x00669138: call 0x633f76 ; 0x0066913d: test byte ptr [ebp + 8], 1 ; 0x00669141: je 0x669150

### 0x0066916f
- blocks=6, insns=52, edges=10, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00631e3d at 0x006691b5)
- branch points:
  - 0x0066918f: jle -> 0x00669194 (jcc_true) | ctx: 0x00669181: mov ecx, dword ptr [eax + ecx*4] ; 0x00669184: mov eax, dword ptr [0xf692d0] ; 0x00669189: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0066918f: jle 0x669194
  - 0x0066918f: jle -> 0x00669191 (jcc_false) | ctx: 0x00669181: mov ecx, dword ptr [eax + ecx*4] ; 0x00669184: mov eax, dword ptr [0xf692d0] ; 0x00669189: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0066918f: jle 0x669194
  - 0x00669191: jmp -> 0x0066919d (jmp) | ctx: 0x00669191: jmp 0x66919d
  - 0x006691b1: jne -> 0x00669193 (jcc_true) | ctx: 0x006691a4: call 0xab6ba9 ; 0x006691a9: cmp dword ptr [0xf692d0], -1 ; 0x006691b0: pop ecx ; 0x006691b1: jne 0x669193
  - 0x006691b1: jne -> 0x006691b3 (jcc_false) | ctx: 0x006691a4: call 0xab6ba9 ; 0x006691a9: cmp dword ptr [0xf692d0], -1 ; 0x006691b0: pop ecx ; 0x006691b1: jne 0x669193
  - 0x00669200: jmp -> 0x00669193 (jmp) | ctx: 0x006691fb: add esp, 0xc ; 0x006691fe: pop edi ; 0x006691ff: pop esi ; 0x00669200: jmp 0x669193

### 0x0066a5b2
- blocks=3, insns=27, edges=6, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0066a609)
  - caller_of_anchor_path: depth 2 (calls 0x0066a5b2 at 0x0066a5ca)
- branch points:
  - 0x0066a5c3: jne -> 0x0066a5e6 (jcc_true) | ctx: 0x0066a5bb: mov ebx, ecx ; 0x0066a5bd: mov esi, edi ; 0x0066a5bf: cmp byte ptr [edi + 0xd], 0 ; 0x0066a5c3: jne 0x66a5e6
  - 0x0066a5c3: jne -> 0x0066a5c5 (jcc_false) | ctx: 0x0066a5bb: mov ebx, ecx ; 0x0066a5bd: mov esi, edi ; 0x0066a5bf: cmp byte ptr [edi + 0xd], 0 ; 0x0066a5c3: jne 0x66a5e6
  - 0x0066a5e4: je -> 0x0066a5c5 (jcc_true) | ctx: 0x0066a5db: add esp, 0xc ; 0x0066a5de: mov edi, esi ; 0x0066a5e0: cmp byte ptr [esi + 0xd], 0 ; 0x0066a5e4: je 0x66a5c5
  - 0x0066a5e4: je -> 0x0066a5e6 (jcc_false) | ctx: 0x0066a5db: add esp, 0xc ; 0x0066a5de: mov edi, esi ; 0x0066a5e0: cmp byte ptr [esi + 0xd], 0 ; 0x0066a5e4: je 0x66a5c5

### 0x0066b228
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0066b910 at 0x0066b23c)
- branch points:
  - 0x0066b22d: jne -> 0x0066b23c (jcc_true) | ctx: 0x0066b228: push edi ; 0x0066b229: mov edi, ecx ; 0x0066b22b: test esi, esi ; 0x0066b22d: jne 0x66b23c
  - 0x0066b22d: jne -> 0x0066b22f (jcc_false) | ctx: 0x0066b228: push edi ; 0x0066b229: mov edi, ecx ; 0x0066b22b: test esi, esi ; 0x0066b22d: jne 0x66b23c

### 0x0066b910
- blocks=4, insns=1194, edges=23, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: WorkTimeBase via `WorkTimeBase` (string 0x00bdb8e0, xref 0x0066c21e)
  - string_xref: WorkTimeThresholdWork via `WorkTimeThresholdWork` (string 0x00bdb8f0, xref 0x0066c257)
  - string_xref: WorkTimeThresholdFarm via `WorkTimeThresholdFarm` (string 0x00bdb908, xref 0x0066c290)
  - string_xref: WorkTimeThresholdResidence via `WorkTimeThresholdResidence` (string 0x00bdb920, xref 0x0066c2c9)
  - string_xref: WorkTimeThresholdCampFire via `WorkTimeThresholdCampFire` (string 0x00bdb93c, xref 0x0066c302)
  - string_xref: WorkerFlightDistance via `WorkerFlightDistance` (string 0x00bdbb28, xref 0x0066c70c)
- branch points:
  - 0x0066b930: jg -> 0x0066b93b (jcc_true) | ctx: 0x0066b922: mov ecx, dword ptr [eax + ecx*4] ; 0x0066b925: mov eax, dword ptr [0xf69ee8] ; 0x0066b92a: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0066b930: jg 0x66b93b
  - 0x0066b930: jg -> 0x0066b932 (jcc_false) | ctx: 0x0066b922: mov ecx, dword ptr [eax + ecx*4] ; 0x0066b925: mov eax, dword ptr [0xf69ee8] ; 0x0066b92a: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0066b930: jg 0x66b93b
  - 0x0066b94d: jne -> 0x0066b932 (jcc_true) | ctx: 0x0066b940: call 0xab6ba9 ; 0x0066b945: cmp dword ptr [0xf69ee8], -1 ; 0x0066b94c: pop ecx ; 0x0066b94d: jne 0x66b932
  - 0x0066b94d: jne -> 0x0066b94f (jcc_false) | ctx: 0x0066b940: call 0xab6ba9 ; 0x0066b945: cmp dword ptr [0xf69ee8], -1 ; 0x0066b94c: pop ecx ; 0x0066b94d: jne 0x66b932
  - 0x0066cb03: jmp -> 0x0066b932 (jmp) | ctx: 0x0066cb00: pop edi ; 0x0066cb01: pop esi ; 0x0066cb02: pop ebx ; 0x0066cb03: jmp 0x66b932

### 0x0066d329
- blocks=1, insns=9, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0066d35d)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0066d41d)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0066d4b7)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0066d559)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0066d5f9)
- branch points:
  - none

### 0x0066d679
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0066d329 at 0x0066d6b1)
- branch points:
  - 0x0066d690: jae -> 0x0066d6b6 (jcc_true) | ctx: 0x0066d689: idiv ebx ; 0x0066d68b: mov edi, dword ptr [ebp + 8] ; 0x0066d68e: cmp eax, edi ; 0x0066d690: jae 0x66d6b6
  - 0x0066d690: jae -> 0x0066d692 (jcc_false) | ctx: 0x0066d689: idiv ebx ; 0x0066d68b: mov edi, dword ptr [ebp + 8] ; 0x0066d68e: cmp eax, edi ; 0x0066d690: jae 0x66d6b6
  - 0x0066d6a2: jb -> 0x0066d6bd (jcc_true) | ctx: 0x0066d69c: idiv ebx ; 0x0066d69e: sub ecx, eax ; 0x0066d6a0: cmp ecx, edi ; 0x0066d6a2: jb 0x66d6bd
  - 0x0066d6a2: jb -> 0x0066d6a4 (jcc_false) | ctx: 0x0066d69c: idiv ebx ; 0x0066d69e: sub ecx, eax ; 0x0066d6a0: cmp ecx, edi ; 0x0066d6a2: jb 0x66d6bd

### 0x0066fe2f
- blocks=1, insns=10, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005781c1 at 0x0066ffc1)
- branch points:
  - none

### 0x0067403a
- blocks=3, insns=36, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005781c1 at 0x006740ba)
- branch points:
  - 0x00674067: je -> 0x00674075 (jcc_true) | ctx: 0x0067405f: cmove eax, ecx ; 0x00674062: lea ecx, [eax + esi] ; 0x00674065: cmp edx, dword ptr [ecx] ; 0x00674067: je 0x674075
  - 0x00674067: je -> 0x00674069 (jcc_false) | ctx: 0x0067405f: cmove eax, ecx ; 0x00674062: lea ecx, [eax + esi] ; 0x00674065: cmp edx, dword ptr [ecx] ; 0x00674067: je 0x674075

### 0x006745c7
- blocks=1, insns=2, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCPath@GGL@@ slot 0 (target 0x006745c7, vtable 0x00bdb29c)
- branch points:
  - none

### 0x006748a0
- blocks=4, insns=80, edges=9, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0058680d at 0x006748e2)
- branch points:
  - 0x006748c0: jg -> 0x006748cb (jcc_true) | ctx: 0x006748b2: mov ecx, dword ptr [eax + ecx*4] ; 0x006748b5: mov eax, dword ptr [0xf6dd20] ; 0x006748ba: cmp eax, dword ptr [ecx + 0x3adc] ; 0x006748c0: jg 0x6748cb
  - 0x006748c0: jg -> 0x006748c2 (jcc_false) | ctx: 0x006748b2: mov ecx, dword ptr [eax + ecx*4] ; 0x006748b5: mov eax, dword ptr [0xf6dd20] ; 0x006748ba: cmp eax, dword ptr [ecx + 0x3adc] ; 0x006748c0: jg 0x6748cb
  - 0x006748dd: jne -> 0x006748c2 (jcc_true) | ctx: 0x006748d0: call 0xab6ba9 ; 0x006748d5: cmp dword ptr [0xf6dd20], -1 ; 0x006748dc: pop ecx ; 0x006748dd: jne 0x6748c2
  - 0x006748dd: jne -> 0x006748df (jcc_false) | ctx: 0x006748d0: call 0xab6ba9 ; 0x006748d5: cmp dword ptr [0xf6dd20], -1 ; 0x006748dc: pop ecx ; 0x006748dd: jne 0x6748c2
  - 0x0067499f: jmp -> 0x006748c2 (jmp) | ctx: 0x0067499c: pop edi ; 0x0067499d: pop esi ; 0x0067499e: pop ebx ; 0x0067499f: jmp 0x6748c2

### 0x00674b83
- blocks=1, insns=16, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0056cf36 at 0x00674b90)
- branch points:
  - none

### 0x00674ba9
- blocks=1, insns=12, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0056cf36 at 0x00674bb4)
- branch points:
  - none

### 0x00674bc6
- blocks=1, insns=16, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0056cf36 at 0x00674bd3)
- branch points:
  - none

### 0x006754b8
- blocks=3, insns=21, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00677fd2 at 0x006754c2)
- branch points:
  - 0x006754cc: je -> 0x006754d6 (jcc_true) | ctx: 0x006754c2: call 0x677fd2 ; 0x006754c7: lea edi, [eax + 8] ; 0x006754ca: test edi, edi ; 0x006754cc: je 0x6754d6
  - 0x006754cc: je -> 0x006754ce (jcc_false) | ctx: 0x006754c2: call 0x677fd2 ; 0x006754c7: lea edi, [eax + 8] ; 0x006754ca: test edi, edi ; 0x006754cc: je 0x6754d6

### 0x0067576e
- blocks=1, insns=81, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fd2e1 at 0x0067584f)
- branch points:
  - none

### 0x00675d4e
- blocks=26, insns=218, edges=64, jcc=16, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00677fd2 at 0x00675dce)
- branch points:
  - 0x00675d58: jne -> 0x00675f74 (jcc_true) | ctx: 0x00675d4f: mov edi, ecx ; 0x00675d51: call 0x677195 ; 0x00675d56: test al, al ; 0x00675d58: jne 0x675f74
  - 0x00675d58: jne -> 0x00675d5e (jcc_false) | ctx: 0x00675d4f: mov edi, ecx ; 0x00675d51: call 0x677195 ; 0x00675d56: test al, al ; 0x00675d58: jne 0x675f74
  - 0x00675d79: jne -> 0x00675f73 (jcc_true) | ctx: 0x00675d74: cdq ; 0x00675d75: idiv ecx ; 0x00675d77: test edx, edx ; 0x00675d79: jne 0x675f73
  - 0x00675d79: jne -> 0x00675d7f (jcc_false) | ctx: 0x00675d74: cdq ; 0x00675d75: idiv ecx ; 0x00675d77: test edx, edx ; 0x00675d79: jne 0x675f73
  - 0x00675d82: jne -> 0x00675dac (jcc_true) | ctx: 0x00675d7f: cmp byte ptr [edi + 0x10], dl ; 0x00675d82: jne 0x675dac
  - 0x00675d82: jne -> 0x00675d84 (jcc_false) | ctx: 0x00675d7f: cmp byte ptr [edi + 0x10], dl ; 0x00675d82: jne 0x675dac
  - 0x00675db2: jne -> 0x00675dc0 (jcc_true) | ctx: 0x00675dac: mov eax, dword ptr [edi + 0x28] ; 0x00675daf: cmp eax, dword ptr [edi + 0x2c] ; 0x00675db2: jne 0x675dc0
  - 0x00675db2: jne -> 0x00675db4 (jcc_false) | ctx: 0x00675dac: mov eax, dword ptr [edi + 0x28] ; 0x00675daf: cmp eax, dword ptr [edi + 0x2c] ; 0x00675db2: jne 0x675dc0
  - 0x00675d8a: je -> 0x00675f73 (jcc_true) | ctx: 0x00675d84: mov eax, dword ptr [edi + 0x34] ; 0x00675d87: cmp eax, dword ptr [edi + 0x38] ; 0x00675d8a: je 0x675f73
  - 0x00675d8a: je -> 0x00675d90 (jcc_false) | ctx: 0x00675d84: mov eax, dword ptr [edi + 0x34] ; 0x00675d87: cmp eax, dword ptr [edi + 0x38] ; 0x00675d8a: je 0x675f73
  - 0x00675de7: je -> 0x00675f5b (jcc_true) | ctx: 0x00675ddd: mov ecx, edi ; 0x00675ddf: call 0x677065 ; 0x00675de4: cmp dword ptr [ebp - 0x18], ebx ; 0x00675de7: je 0x675f5b
  - 0x00675de7: je -> 0x00675ded (jcc_false) | ctx: 0x00675ddd: mov ecx, edi ; 0x00675ddf: call 0x677065 ; 0x00675de4: cmp dword ptr [ebp - 0x18], ebx ; 0x00675de7: je 0x675f5b
  - 0x00675dba: je -> 0x00675f73 (jcc_true) | ctx: 0x00675db4: mov eax, dword ptr [edi + 0x34] ; 0x00675db7: cmp eax, dword ptr [edi + 0x38] ; 0x00675dba: je 0x675f73
  - 0x00675dba: je -> 0x00675dc0 (jcc_false) | ctx: 0x00675db4: mov eax, dword ptr [edi + 0x34] ; 0x00675db7: cmp eax, dword ptr [edi + 0x38] ; 0x00675dba: je 0x675f73
  - 0x00675da4: jle -> 0x00675f73 (jcc_true) | ctx: 0x00675d9b: call 0x6761ef ; 0x00675da0: sub esi, eax ; 0x00675da2: test esi, esi ; 0x00675da4: jle 0x675f73
  - 0x00675da4: jle -> 0x00675daa (jcc_false) | ctx: 0x00675d9b: call 0x6761ef ; 0x00675da0: sub esi, eax ; 0x00675da2: test esi, esi ; 0x00675da4: jle 0x675f73
  - 0x00675df4: je -> 0x00675f5b (jcc_true) | ctx: 0x00675ded: mov eax, dword ptr [ebp - 0x1c] ; 0x00675df0: mov esi, dword ptr [eax] ; 0x00675df2: cmp esi, eax ; 0x00675df4: je 0x675f5b
  - 0x00675df4: je -> 0x00675dfa (jcc_false) | ctx: 0x00675ded: mov eax, dword ptr [ebp - 0x1c] ; 0x00675df0: mov esi, dword ptr [eax] ; 0x00675df2: cmp esi, eax ; 0x00675df4: je 0x675f5b
  - 0x00675daa: jmp -> 0x00675dc0 (jmp) | ctx: 0x00675daa: jmp 0x675dc0
  - 0x00675e33: jne -> 0x00675e4e (jcc_true) | ctx: 0x00675e2a: call 0x677aeb ; 0x00675e2f: mov ebx, eax ; 0x00675e31: test ebx, ebx ; 0x00675e33: jne 0x675e4e
  - 0x00675e33: jne -> 0x00675e35 (jcc_false) | ctx: 0x00675e2a: call 0x677aeb ; 0x00675e2f: mov ebx, eax ; 0x00675e31: test ebx, ebx ; 0x00675e33: jne 0x675e4e
  - 0x00675e6b: jne -> 0x00675f3e (jcc_true) | ctx: 0x00675e62: pop ecx ; 0x00675e63: mov cl, byte ptr [edx + 0xfc] ; 0x00675e69: test cl, cl ; 0x00675e6b: jne 0x675f3e
  - 0x00675e6b: jne -> 0x00675e71 (jcc_false) | ctx: 0x00675e62: pop ecx ; 0x00675e63: mov cl, byte ptr [edx + 0xfc] ; 0x00675e69: test cl, cl ; 0x00675e6b: jne 0x675f3e
  - 0x00675e48: je -> 0x00675f3e (jcc_true) | ctx: 0x00675e3f: call 0x677aeb ; 0x00675e44: mov ebx, eax ; 0x00675e46: test ebx, ebx ; 0x00675e48: je 0x675f3e
  - 0x00675e48: je -> 0x00675e4e (jcc_false) | ctx: 0x00675e3f: call 0x677aeb ; 0x00675e44: mov ebx, eax ; 0x00675e46: test ebx, ebx ; 0x00675e48: je 0x675f3e
  - 0x00675f43: jmp -> 0x00675df4 (jmp) | ctx: 0x00675f3e: mov esi, dword ptr [esi] ; 0x00675f40: cmp esi, dword ptr [ebp - 0x1c] ; 0x00675f43: jmp 0x675df4
  - 0x00675ede: jne -> 0x00675ee6 (jcc_true) | ctx: 0x00675ed6: call dword ptr [eax + 0x58] ; 0x00675ed9: mov dword ptr [ebp - 0x14], eax ; 0x00675edc: test eax, eax ; 0x00675ede: jne 0x675ee6
  - 0x00675ede: jne -> 0x00675ee0 (jcc_false) | ctx: 0x00675ed6: call dword ptr [eax + 0x58] ; 0x00675ed9: mov dword ptr [ebp - 0x14], eax ; 0x00675edc: test eax, eax ; 0x00675ede: jne 0x675ee6
  - 0x00675df4: je -> 0x00675f5b (jcc_true) | ctx: 0x00675df4: je 0x675f5b
  - 0x00675df4: je -> 0x00675dfa (jcc_false) | ctx: 0x00675df4: je 0x675f5b
  - 0x00675ef7: jne -> 0x00675eff (jcc_true) | ctx: 0x00675eed: call 0x56d756 ; 0x00675ef2: mov dword ptr [ebp - 0x10], eax ; 0x00675ef5: test eax, eax ; 0x00675ef7: jne 0x675eff
  - 0x00675ef7: jne -> 0x00675ef9 (jcc_false) | ctx: 0x00675eed: call 0x56d756 ; 0x00675ef2: mov dword ptr [ebp - 0x10], eax ; 0x00675ef5: test eax, eax ; 0x00675ef7: jne 0x675eff
  - 0x00675ee4: jmp -> 0x00675f2b (jmp) | ctx: 0x00675ee0: mov byte ptr [ebp - 4], 2 ; 0x00675ee4: jmp 0x675f2b
  - 0x00675f25: jne -> 0x00675f48 (jcc_true) | ctx: 0x00675f1b: push dword ptr [ebp - 0x14] ; 0x00675f1e: call 0x6759c9 ; 0x00675f23: test al, al ; 0x00675f25: jne 0x675f48
  - 0x00675f25: jne -> 0x00675f27 (jcc_false) | ctx: 0x00675f1b: push dword ptr [ebp - 0x14] ; 0x00675f1e: call 0x6759c9 ; 0x00675f23: test al, al ; 0x00675f25: jne 0x675f48
  - 0x00675efd: jmp -> 0x00675f2b (jmp) | ctx: 0x00675ef9: mov byte ptr [ebp - 4], 3 ; 0x00675efd: jmp 0x675f2b
  - 0x00675f43: jmp -> 0x00675df4 (jmp) | ctx: 0x00675f3a: mov byte ptr [ebp - 4], 0 ; 0x00675f3e: mov esi, dword ptr [esi] ; 0x00675f40: cmp esi, dword ptr [ebp - 0x1c] ; 0x00675f43: jmp 0x675df4
  - 0x00675f43: jmp -> 0x00675df4 (jmp) | ctx: 0x00675f3a: mov byte ptr [ebp - 4], 0 ; 0x00675f3e: mov esi, dword ptr [esi] ; 0x00675f40: cmp esi, dword ptr [ebp - 0x1c] ; 0x00675f43: jmp 0x675df4

### 0x00677fd2
- blocks=8, insns=30, edges=12, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00677fdb)
- branch points:
  - 0x00677fe8: jne -> 0x00677ff0 (jcc_true) | ctx: 0x00677fe0: mov ecx, dword ptr [ebp + 8] ; 0x00677fe3: add esp, 0xc ; 0x00677fe6: test ecx, ecx ; 0x00677fe8: jne 0x677ff0
  - 0x00677fe8: jne -> 0x00677fea (jcc_false) | ctx: 0x00677fe0: mov ecx, dword ptr [ebp + 8] ; 0x00677fe3: add esp, 0xc ; 0x00677fe6: test ecx, ecx ; 0x00677fe8: jne 0x677ff0
  - 0x00677ff5: je -> 0x00677ff9 (jcc_true) | ctx: 0x00677ff0: mov edx, dword ptr [ebp + 0xc] ; 0x00677ff3: test eax, eax ; 0x00677ff5: je 0x677ff9
  - 0x00677ff5: je -> 0x00677ff7 (jcc_false) | ctx: 0x00677ff0: mov edx, dword ptr [ebp + 0xc] ; 0x00677ff3: test eax, eax ; 0x00677ff5: je 0x677ff9
  - 0x00677fee: jmp -> 0x00677ff3 (jmp) | ctx: 0x00677fea: mov ecx, eax ; 0x00677fec: mov edx, eax ; 0x00677fee: jmp 0x677ff3
  - 0x00677ffe: je -> 0x00678002 (jcc_true) | ctx: 0x00677ff9: lea ecx, [eax + 4] ; 0x00677ffc: test ecx, ecx ; 0x00677ffe: je 0x678002
  - 0x00677ffe: je -> 0x00678000 (jcc_false) | ctx: 0x00677ff9: lea ecx, [eax + 4] ; 0x00677ffc: test ecx, ecx ; 0x00677ffe: je 0x678002
  - 0x00677ffe: je -> 0x00678002 (jcc_true) | ctx: 0x00677ff7: mov dword ptr [eax], ecx ; 0x00677ff9: lea ecx, [eax + 4] ; 0x00677ffc: test ecx, ecx ; 0x00677ffe: je 0x678002
  - 0x00677ffe: je -> 0x00678000 (jcc_false) | ctx: 0x00677ff7: mov dword ptr [eax], ecx ; 0x00677ff9: lea ecx, [eax + 4] ; 0x00677ffc: test ecx, ecx ; 0x00677ffe: je 0x678002
  - 0x00677ff5: je -> 0x00677ff9 (jcc_true) | ctx: 0x00677ff3: test eax, eax ; 0x00677ff5: je 0x677ff9
  - 0x00677ff5: je -> 0x00677ff7 (jcc_false) | ctx: 0x00677ff3: test eax, eax ; 0x00677ff5: je 0x677ff9

### 0x00678182
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x006781a8 at 0x00678196)
- branch points:
  - 0x00678187: jne -> 0x00678196 (jcc_true) | ctx: 0x00678182: push edi ; 0x00678183: mov edi, ecx ; 0x00678185: test esi, esi ; 0x00678187: jne 0x678196
  - 0x00678187: jne -> 0x00678189 (jcc_false) | ctx: 0x00678182: push edi ; 0x00678183: mov edi, ecx ; 0x00678185: test esi, esi ; 0x00678187: jne 0x678196

### 0x006781a8
- blocks=4, insns=141, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: ReAttachWorkerFrequency via `ReAttachWorkerFrequency` (string 0x00bdc858, xref 0x006782b0)
  - string_xref: MaximumDistanceWorkerToFarm via `MaximumDistanceWorkerToFarm` (string 0x00bdc884, xref 0x00678301)
  - string_xref: MaximumDistanceWorkerToResidence via `MaximumDistanceWorkerToResidence` (string 0x00bdc8a0, xref 0x00678357)
- branch points:
  - 0x006781c8: jg -> 0x006781d3 (jcc_true) | ctx: 0x006781ba: mov ecx, dword ptr [eax + ecx*4] ; 0x006781bd: mov eax, dword ptr [0xf6eaf8] ; 0x006781c2: cmp eax, dword ptr [ecx + 0x3adc] ; 0x006781c8: jg 0x6781d3
  - 0x006781c8: jg -> 0x006781ca (jcc_false) | ctx: 0x006781ba: mov ecx, dword ptr [eax + ecx*4] ; 0x006781bd: mov eax, dword ptr [0xf6eaf8] ; 0x006781c2: cmp eax, dword ptr [ecx + 0x3adc] ; 0x006781c8: jg 0x6781d3
  - 0x006781e5: jne -> 0x006781ca (jcc_true) | ctx: 0x006781d8: call 0xab6ba9 ; 0x006781dd: cmp dword ptr [0xf6eaf8], -1 ; 0x006781e4: pop ecx ; 0x006781e5: jne 0x6781ca
  - 0x006781e5: jne -> 0x006781e7 (jcc_false) | ctx: 0x006781d8: call 0xab6ba9 ; 0x006781dd: cmp dword ptr [0xf6eaf8], -1 ; 0x006781e4: pop ecx ; 0x006781e5: jne 0x6781ca
  - 0x00678399: jmp -> 0x006781ca (jmp) | ctx: 0x00678396: pop edi ; 0x00678397: pop esi ; 0x00678398: pop ebx ; 0x00678399: jmp 0x6781ca

### 0x0067840d
- blocks=1, insns=17, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00588b31 at 0x00678427)
- branch points:
  - none

### 0x006785a8
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00678bd6 at 0x0067864f)
- branch points:
  - 0x006785ad: jne -> 0x006785bc (jcc_true) | ctx: 0x006785a8: push edi ; 0x006785a9: mov edi, ecx ; 0x006785ab: test esi, esi ; 0x006785ad: jne 0x6785bc
  - 0x006785ad: jne -> 0x006785af (jcc_false) | ctx: 0x006785a8: push edi ; 0x006785a9: mov edi, ecx ; 0x006785ab: test esi, esi ; 0x006785ad: jne 0x6785bc

### 0x00678bd6
- blocks=8, insns=30, edges=12, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x00678bdf)
- branch points:
  - 0x00678bec: jne -> 0x00678bf4 (jcc_true) | ctx: 0x00678be4: mov ecx, dword ptr [ebp + 8] ; 0x00678be7: add esp, 0xc ; 0x00678bea: test ecx, ecx ; 0x00678bec: jne 0x678bf4
  - 0x00678bec: jne -> 0x00678bee (jcc_false) | ctx: 0x00678be4: mov ecx, dword ptr [ebp + 8] ; 0x00678be7: add esp, 0xc ; 0x00678bea: test ecx, ecx ; 0x00678bec: jne 0x678bf4
  - 0x00678bf9: je -> 0x00678bfd (jcc_true) | ctx: 0x00678bf4: mov edx, dword ptr [ebp + 0xc] ; 0x00678bf7: test eax, eax ; 0x00678bf9: je 0x678bfd
  - 0x00678bf9: je -> 0x00678bfb (jcc_false) | ctx: 0x00678bf4: mov edx, dword ptr [ebp + 0xc] ; 0x00678bf7: test eax, eax ; 0x00678bf9: je 0x678bfd
  - 0x00678bf2: jmp -> 0x00678bf7 (jmp) | ctx: 0x00678bee: mov ecx, eax ; 0x00678bf0: mov edx, eax ; 0x00678bf2: jmp 0x678bf7
  - 0x00678c02: je -> 0x00678c06 (jcc_true) | ctx: 0x00678bfd: lea ecx, [eax + 4] ; 0x00678c00: test ecx, ecx ; 0x00678c02: je 0x678c06
  - 0x00678c02: je -> 0x00678c04 (jcc_false) | ctx: 0x00678bfd: lea ecx, [eax + 4] ; 0x00678c00: test ecx, ecx ; 0x00678c02: je 0x678c06
  - 0x00678c02: je -> 0x00678c06 (jcc_true) | ctx: 0x00678bfb: mov dword ptr [eax], ecx ; 0x00678bfd: lea ecx, [eax + 4] ; 0x00678c00: test ecx, ecx ; 0x00678c02: je 0x678c06
  - 0x00678c02: je -> 0x00678c04 (jcc_false) | ctx: 0x00678bfb: mov dword ptr [eax], ecx ; 0x00678bfd: lea ecx, [eax + 4] ; 0x00678c00: test ecx, ecx ; 0x00678c02: je 0x678c06
  - 0x00678bf9: je -> 0x00678bfd (jcc_true) | ctx: 0x00678bf7: test eax, eax ; 0x00678bf9: je 0x678bfd
  - 0x00678bf9: je -> 0x00678bfb (jcc_false) | ctx: 0x00678bf7: test eax, eax ; 0x00678bf9: je 0x678bfd

### 0x0067a91d
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0067bb8a at 0x0067a931)
- branch points:
  - 0x0067a922: jne -> 0x0067a931 (jcc_true) | ctx: 0x0067a91d: push edi ; 0x0067a91e: mov edi, ecx ; 0x0067a920: test esi, esi ; 0x0067a922: jne 0x67a931
  - 0x0067a922: jne -> 0x0067a924 (jcc_false) | ctx: 0x0067a91d: push edi ; 0x0067a91e: mov edi, ecx ; 0x0067a920: test esi, esi ; 0x0067a922: jne 0x67a931

### 0x0067adb4
- blocks=1, insns=30, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0067ade6)
- branch points:
  - none

### 0x0067bb8a
- blocks=4, insns=424, edges=24, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - string_xref: WorkerAlarmMode via `WorkerAlarmMode` (string 0x00bdd39c, xref 0x0067bdde)
- branch points:
  - 0x0067bbaa: jg -> 0x0067bbb5 (jcc_true) | ctx: 0x0067bb9c: mov ecx, dword ptr [eax + ecx*4] ; 0x0067bb9f: mov eax, dword ptr [0xf705a4] ; 0x0067bba4: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0067bbaa: jg 0x67bbb5
  - 0x0067bbaa: jg -> 0x0067bbac (jcc_false) | ctx: 0x0067bb9c: mov ecx, dword ptr [eax + ecx*4] ; 0x0067bb9f: mov eax, dword ptr [0xf705a4] ; 0x0067bba4: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0067bbaa: jg 0x67bbb5
  - 0x0067bbc7: jne -> 0x0067bbac (jcc_true) | ctx: 0x0067bbba: call 0xab6ba9 ; 0x0067bbbf: cmp dword ptr [0xf705a4], -1 ; 0x0067bbc6: pop ecx ; 0x0067bbc7: jne 0x67bbac
  - 0x0067bbc7: jne -> 0x0067bbc9 (jcc_false) | ctx: 0x0067bbba: call 0xab6ba9 ; 0x0067bbbf: cmp dword ptr [0xf705a4], -1 ; 0x0067bbc6: pop ecx ; 0x0067bbc7: jne 0x67bbac
  - 0x0067c144: jmp -> 0x0067bbac (jmp) | ctx: 0x0067c141: pop edi ; 0x0067c142: pop esi ; 0x0067c143: pop ebx ; 0x0067c144: jmp 0x67bbac

### 0x0067cfe0
- blocks=1, insns=23, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0067d02f)
- branch points:
  - none

### 0x00680907
- blocks=4, insns=69, edges=9, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005781c1 at 0x00680a2e)
- branch points:
  - 0x00680927: jg -> 0x00680932 (jcc_true) | ctx: 0x00680919: mov ecx, dword ptr [eax + ecx*4] ; 0x0068091c: mov eax, dword ptr [0xf71ae4] ; 0x00680921: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00680927: jg 0x680932
  - 0x00680927: jg -> 0x00680929 (jcc_false) | ctx: 0x00680919: mov ecx, dword ptr [eax + ecx*4] ; 0x0068091c: mov eax, dword ptr [0xf71ae4] ; 0x00680921: cmp eax, dword ptr [ecx + 0x3adc] ; 0x00680927: jg 0x680932
  - 0x00680944: jne -> 0x00680929 (jcc_true) | ctx: 0x00680937: call 0xab6ba9 ; 0x0068093c: cmp dword ptr [0xf71ae4], -1 ; 0x00680943: pop ecx ; 0x00680944: jne 0x680929
  - 0x00680944: jne -> 0x00680946 (jcc_false) | ctx: 0x00680937: call 0xab6ba9 ; 0x0068093c: cmp dword ptr [0xf71ae4], -1 ; 0x00680943: pop ecx ; 0x00680944: jne 0x680929
  - 0x006809eb: jmp -> 0x00680929 (jmp) | ctx: 0x006809e8: pop edi ; 0x006809e9: pop esi ; 0x006809ea: pop ebx ; 0x006809eb: jmp 0x680929

### 0x006880a6
- blocks=4, insns=373, edges=37, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0062767a at 0x006880e8)
- branch points:
  - 0x006880c6: jg -> 0x006880d1 (jcc_true) | ctx: 0x006880b8: mov ecx, dword ptr [eax + ecx*4] ; 0x006880bb: mov eax, dword ptr [0xf73ad8] ; 0x006880c0: cmp eax, dword ptr [ecx + 0x3adc] ; 0x006880c6: jg 0x6880d1
  - 0x006880c6: jg -> 0x006880c8 (jcc_false) | ctx: 0x006880b8: mov ecx, dword ptr [eax + ecx*4] ; 0x006880bb: mov eax, dword ptr [0xf73ad8] ; 0x006880c0: cmp eax, dword ptr [ecx + 0x3adc] ; 0x006880c6: jg 0x6880d1
  - 0x006880e3: jne -> 0x006880c8 (jcc_true) | ctx: 0x006880d6: call 0xab6ba9 ; 0x006880db: cmp dword ptr [0xf73ad8], -1 ; 0x006880e2: pop ecx ; 0x006880e3: jne 0x6880c8
  - 0x006880e3: jne -> 0x006880e5 (jcc_false) | ctx: 0x006880d6: call 0xab6ba9 ; 0x006880db: cmp dword ptr [0xf73ad8], -1 ; 0x006880e2: pop ecx ; 0x006880e3: jne 0x6880c8
  - 0x00688563: jmp -> 0x006880c8 (jmp) | ctx: 0x00688560: pop edi ; 0x00688561: pop esi ; 0x00688562: pop ebx ; 0x00688563: jmp 0x6880c8

### 0x00688cd7
- blocks=11, insns=102, edges=25, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00576019 at 0x00688d67)
  - caller_of_anchor_path: depth 2 (calls 0x00576019 at 0x00688dcf)
- branch points:
  - 0x00688ceb: jl -> 0x00688da7 (jcc_true) | ctx: 0x00688ce0: mov eax, dword ptr [ecx] ; 0x00688ce2: call dword ptr [eax + 0x38] ; 0x00688ce5: cmp eax, dword ptr [edi + 0x1f4] ; 0x00688ceb: jl 0x688da7
  - 0x00688ceb: jl -> 0x00688cf1 (jcc_false) | ctx: 0x00688ce0: mov eax, dword ptr [ecx] ; 0x00688ce2: call dword ptr [eax + 0x38] ; 0x00688ce5: cmp eax, dword ptr [edi + 0x1f4] ; 0x00688ceb: jl 0x688da7
  - 0x00688d00: je -> 0x00688dca (jcc_true) | ctx: 0x00688cf6: call 0x6179ea ; 0x00688cfb: mov dword ptr [ebp - 0x10], eax ; 0x00688cfe: test eax, eax ; 0x00688d00: je 0x688dca
  - 0x00688d00: je -> 0x00688d06 (jcc_false) | ctx: 0x00688cf6: call 0x6179ea ; 0x00688cfb: mov dword ptr [ebp - 0x10], eax ; 0x00688cfe: test eax, eax ; 0x00688d00: je 0x688dca
  - 0x00688dcd: jmp -> 0x00688daa (jmp) | ctx: 0x00688dca: push -2 ; 0x00688dcc: pop eax ; 0x00688dcd: jmp 0x688daa
  - 0x00688d14: je -> 0x00688da7 (jcc_true) | ctx: 0x00688d0c: push eax ; 0x00688d0d: call 0x56d756 ; 0x00688d12: test eax, eax ; 0x00688d14: je 0x688da7
  - 0x00688d14: je -> 0x00688d1a (jcc_false) | ctx: 0x00688d0c: push eax ; 0x00688d0d: call 0x56d756 ; 0x00688d12: test eax, eax ; 0x00688d14: je 0x688da7
  - 0x00688d26: je -> 0x00688da6 (jcc_true) | ctx: 0x00688d21: mov ebx, eax ; 0x00688d23: pop ecx ; 0x00688d24: test ebx, ebx ; 0x00688d26: je 0x688da6
  - 0x00688d26: je -> 0x00688d28 (jcc_false) | ctx: 0x00688d21: mov ebx, eax ; 0x00688d23: pop ecx ; 0x00688d24: test ebx, ebx ; 0x00688d26: je 0x688da6
  - 0x00688d31: je -> 0x00688dbb (jcc_true) | ctx: 0x00688d28: mov ecx, ebx ; 0x00688d2a: call 0x63dcab ; 0x00688d2f: test al, al ; 0x00688d31: je 0x688dbb
  - 0x00688d31: je -> 0x00688d37 (jcc_false) | ctx: 0x00688d28: mov ecx, ebx ; 0x00688d2a: call 0x63dcab ; 0x00688d2f: test al, al ; 0x00688d31: je 0x688dbb
  - 0x00688dc8: jmp -> 0x00688da6 (jmp) | ctx: 0x00688dbb: mov ecx, ebx ; 0x00688dbd: call 0x63bade ; 0x00688dc2: mov dword ptr [edi + 0x1f4], eax ; 0x00688dc8: jmp 0x688da6

### 0x00688ed1
- blocks=9, insns=126, edges=26, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00576019 at 0x00688fba)
- branch points:
  - 0x00688ee7: jne -> 0x00688f01 (jcc_true) | ctx: 0x00688ede: call 0x6179ea ; 0x00688ee3: mov esi, eax ; 0x00688ee5: test esi, esi ; 0x00688ee7: jne 0x688f01
  - 0x00688ee7: jne -> 0x00688ee9 (jcc_false) | ctx: 0x00688ede: call 0x6179ea ; 0x00688ee3: mov esi, eax ; 0x00688ee5: test esi, esi ; 0x00688ee7: jne 0x688f01
  - 0x00688f0f: je -> 0x00688ffa (jcc_true) | ctx: 0x00688f07: push esi ; 0x00688f08: call 0x56d756 ; 0x00688f0d: test eax, eax ; 0x00688f0f: je 0x688ffa
  - 0x00688f0f: je -> 0x00688f15 (jcc_false) | ctx: 0x00688f07: push esi ; 0x00688f08: call 0x56d756 ; 0x00688f0d: test eax, eax ; 0x00688f0f: je 0x688ffa
  - 0x00688efb: je -> 0x00688ffa (jcc_true) | ctx: 0x00688ef2: call 0x6179ea ; 0x00688ef7: mov esi, eax ; 0x00688ef9: test esi, esi ; 0x00688efb: je 0x688ffa
  - 0x00688efb: je -> 0x00688f01 (jcc_false) | ctx: 0x00688ef2: call 0x6179ea ; 0x00688ef7: mov esi, eax ; 0x00688ef9: test esi, esi ; 0x00688efb: je 0x688ffa
  - 0x00688f21: je -> 0x00688ffa (jcc_true) | ctx: 0x00688f1b: mov dword ptr [ebp - 0x14], eax ; 0x00688f1e: pop ecx ; 0x00688f1f: test eax, eax ; 0x00688f21: je 0x688ffa
  - 0x00688f21: je -> 0x00688f27 (jcc_false) | ctx: 0x00688f1b: mov dword ptr [ebp - 0x14], eax ; 0x00688f1e: pop ecx ; 0x00688f1f: test eax, eax ; 0x00688f21: je 0x688ffa
  - 0x00688f2a: jne -> 0x00688fb8 (jcc_true) | ctx: 0x00688f27: cmp byte ptr [ebp - 0xd], bl ; 0x00688f2a: jne 0x688fb8
  - 0x00688f2a: jne -> 0x00688f30 (jcc_false) | ctx: 0x00688f27: cmp byte ptr [ebp - 0xd], bl ; 0x00688f2a: jne 0x688fb8
  - 0x00688fb6: jmp -> 0x00688ff7 (jmp) | ctx: 0x00688faf: mov eax, dword ptr [edi] ; 0x00688fb1: push 0x1b ; 0x00688fb3: call dword ptr [eax + 0x60] ; 0x00688fb6: jmp 0x688ff7

### 0x0068a16f
- blocks=6, insns=52, edges=10, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00631e3d at 0x0068a1b5)
- branch points:
  - 0x0068a18f: jle -> 0x0068a194 (jcc_true) | ctx: 0x0068a181: mov ecx, dword ptr [eax + ecx*4] ; 0x0068a184: mov eax, dword ptr [0xf73cf0] ; 0x0068a189: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0068a18f: jle 0x68a194
  - 0x0068a18f: jle -> 0x0068a191 (jcc_false) | ctx: 0x0068a181: mov ecx, dword ptr [eax + ecx*4] ; 0x0068a184: mov eax, dword ptr [0xf73cf0] ; 0x0068a189: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0068a18f: jle 0x68a194
  - 0x0068a191: jmp -> 0x0068a19d (jmp) | ctx: 0x0068a191: jmp 0x68a19d
  - 0x0068a1b1: jne -> 0x0068a193 (jcc_true) | ctx: 0x0068a1a4: call 0xab6ba9 ; 0x0068a1a9: cmp dword ptr [0xf73cf0], -1 ; 0x0068a1b0: pop ecx ; 0x0068a1b1: jne 0x68a193
  - 0x0068a1b1: jne -> 0x0068a1b3 (jcc_false) | ctx: 0x0068a1a4: call 0xab6ba9 ; 0x0068a1a9: cmp dword ptr [0xf73cf0], -1 ; 0x0068a1b0: pop ecx ; 0x0068a1b1: jne 0x68a193
  - 0x0068a200: jmp -> 0x0068a193 (jmp) | ctx: 0x0068a1fb: add esp, 0xc ; 0x0068a1fe: pop edi ; 0x0068a1ff: pop esi ; 0x0068a200: jmp 0x68a193

### 0x0068a306
- blocks=3, insns=13, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0068a30f)
- branch points:
  - 0x0068a319: je -> 0x0068a31e (jcc_true) | ctx: 0x0068a30f: call 0x57fd44 ; 0x0068a314: lea ecx, [eax + 8] ; 0x0068a317: test ecx, ecx ; 0x0068a319: je 0x68a31e
  - 0x0068a319: je -> 0x0068a31b (jcc_false) | ctx: 0x0068a30f: call 0x57fd44 ; 0x0068a314: lea ecx, [eax + 8] ; 0x0068a317: test ecx, ecx ; 0x0068a319: je 0x68a31e

### 0x0068a624
- blocks=5, insns=76, edges=17, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x0068a700)
- branch points:
  - 0x0068a648: je -> 0x0068a65c (jcc_true) | ctx: 0x0068a640: call 0x68883d ; 0x0068a645: pop ecx ; 0x0068a646: test eax, eax ; 0x0068a648: je 0x68a65c
  - 0x0068a648: je -> 0x0068a64a (jcc_false) | ctx: 0x0068a640: call 0x68883d ; 0x0068a645: pop ecx ; 0x0068a646: test eax, eax ; 0x0068a648: je 0x68a65c
  - 0x0068a690: jle -> 0x0068a674 (jcc_true) | ctx: 0x0068a687: call 0x60b242 ; 0x0068a68c: inc ebx ; 0x0068a68d: cmp ebx, 0x11 ; 0x0068a690: jle 0x68a674
  - 0x0068a690: jle -> 0x0068a692 (jcc_false) | ctx: 0x0068a687: call 0x60b242 ; 0x0068a68c: inc ebx ; 0x0068a68d: cmp ebx, 0x11 ; 0x0068a690: jle 0x68a674
  - 0x0068a690: jle -> 0x0068a674 (jcc_true) | ctx: 0x0068a687: call 0x60b242 ; 0x0068a68c: inc ebx ; 0x0068a68d: cmp ebx, 0x11 ; 0x0068a690: jle 0x68a674
  - 0x0068a690: jle -> 0x0068a692 (jcc_false) | ctx: 0x0068a687: call 0x60b242 ; 0x0068a68c: inc ebx ; 0x0068a68d: cmp ebx, 0x11 ; 0x0068a690: jle 0x68a674
  - 0x0068a690: jle -> 0x0068a674 (jcc_true) | ctx: 0x0068a687: call 0x60b242 ; 0x0068a68c: inc ebx ; 0x0068a68d: cmp ebx, 0x11 ; 0x0068a690: jle 0x68a674
  - 0x0068a690: jle -> 0x0068a692 (jcc_false) | ctx: 0x0068a687: call 0x60b242 ; 0x0068a68c: inc ebx ; 0x0068a68d: cmp ebx, 0x11 ; 0x0068a690: jle 0x68a674

### 0x0068f264
- blocks=6, insns=52, edges=10, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00631e3d at 0x0068f2aa)
- branch points:
  - 0x0068f284: jle -> 0x0068f289 (jcc_true) | ctx: 0x0068f276: mov ecx, dword ptr [eax + ecx*4] ; 0x0068f279: mov eax, dword ptr [0xf755a0] ; 0x0068f27e: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0068f284: jle 0x68f289
  - 0x0068f284: jle -> 0x0068f286 (jcc_false) | ctx: 0x0068f276: mov ecx, dword ptr [eax + ecx*4] ; 0x0068f279: mov eax, dword ptr [0xf755a0] ; 0x0068f27e: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0068f284: jle 0x68f289
  - 0x0068f286: jmp -> 0x0068f292 (jmp) | ctx: 0x0068f286: jmp 0x68f292
  - 0x0068f2a6: jne -> 0x0068f288 (jcc_true) | ctx: 0x0068f299: call 0xab6ba9 ; 0x0068f29e: cmp dword ptr [0xf755a0], -1 ; 0x0068f2a5: pop ecx ; 0x0068f2a6: jne 0x68f288
  - 0x0068f2a6: jne -> 0x0068f2a8 (jcc_false) | ctx: 0x0068f299: call 0xab6ba9 ; 0x0068f29e: cmp dword ptr [0xf755a0], -1 ; 0x0068f2a5: pop ecx ; 0x0068f2a6: jne 0x68f288
  - 0x0068f2f5: jmp -> 0x0068f288 (jmp) | ctx: 0x0068f2f0: add esp, 0xc ; 0x0068f2f3: pop edi ; 0x0068f2f4: pop esi ; 0x0068f2f5: jmp 0x68f288

### 0x006933a1
- blocks=1, insns=9, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00576019 at 0x006933ab)
- branch points:
  - none

### 0x00693aa7
- blocks=15, insns=100, edges=34, jcc=10, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x00645be5 at 0x00693b66)
- branch points:
  - 0x00693aca: je -> 0x00693add (jcc_true) | ctx: 0x00693ac2: mov edx, dword ptr [eax] ; 0x00693ac4: call dword ptr [edx + 0x40] ; 0x00693ac7: cmp byte ptr [ebp - 0x10], bl ; 0x00693aca: je 0x693add
  - 0x00693aca: je -> 0x00693acc (jcc_false) | ctx: 0x00693ac2: mov edx, dword ptr [eax] ; 0x00693ac4: call dword ptr [edx + 0x40] ; 0x00693ac7: cmp byte ptr [ebp - 0x10], bl ; 0x00693aca: je 0x693add
  - 0x00693ae1: jle -> 0x00693b5f (jcc_true) | ctx: 0x00693add: push edi ; 0x00693ade: cmp dword ptr [esi + 0x20], ebx ; 0x00693ae1: jle 0x693b5f
  - 0x00693ae1: jle -> 0x00693ae3 (jcc_false) | ctx: 0x00693add: push edi ; 0x00693ade: cmp dword ptr [esi + 0x20], ebx ; 0x00693ae1: jle 0x693b5f
  - 0x00693ad8: jmp -> 0x00693ba1 (jmp) | ctx: 0x00693acf: mov dword ptr [esi + 0x20], ebx ; 0x00693ad2: mov eax, dword ptr [eax + 0x14] ; 0x00693ad5: mov dword ptr [esi + 0x24], eax ; 0x00693ad8: jmp 0x693ba1
  - 0x00693b62: je -> 0x00693b6f (jcc_true) | ctx: 0x00693b5f: cmp dword ptr [esi + 0x24], ebx ; 0x00693b62: je 0x693b6f
  - 0x00693b62: je -> 0x00693b64 (jcc_false) | ctx: 0x00693b5f: cmp dword ptr [esi + 0x24], ebx ; 0x00693b62: je 0x693b6f
  - 0x00693aee: je -> 0x00693b78 (jcc_true) | ctx: 0x00693ae5: call 0x645839 ; 0x00693aea: mov edi, eax ; 0x00693aec: test edi, edi ; 0x00693aee: je 0x693b78
  - 0x00693aee: je -> 0x00693af4 (jcc_false) | ctx: 0x00693ae5: call 0x645839 ; 0x00693aea: mov edi, eax ; 0x00693aec: test edi, edi ; 0x00693aee: je 0x693b78
  - 0x00693b7e: je -> 0x00693ba1 (jcc_true) | ctx: 0x00693b78: mov eax, dword ptr [esi + 0x24] ; 0x00693b7b: pop edi ; 0x00693b7c: test eax, eax ; 0x00693b7e: je 0x693ba1
  - 0x00693b7e: je -> 0x00693b80 (jcc_false) | ctx: 0x00693b78: mov eax, dword ptr [esi + 0x24] ; 0x00693b7b: pop edi ; 0x00693b7c: test eax, eax ; 0x00693b7e: je 0x693ba1
  - 0x00693b6d: je -> 0x00693b78 (jcc_true) | ctx: 0x00693b64: mov ecx, esi ; 0x00693b66: call 0x645bf5 ; 0x00693b6b: test al, al ; 0x00693b6d: je 0x693b78
  - 0x00693b6d: je -> 0x00693b6f (jcc_false) | ctx: 0x00693b64: mov ecx, esi ; 0x00693b66: call 0x645bf5 ; 0x00693b6b: test al, al ; 0x00693b6d: je 0x693b78
  - 0x00693b7e: je -> 0x00693ba1 (jcc_true) | ctx: 0x00693b78: mov eax, dword ptr [esi + 0x24] ; 0x00693b7b: pop edi ; 0x00693b7c: test eax, eax ; 0x00693b7e: je 0x693ba1
  - 0x00693b7e: je -> 0x00693b80 (jcc_false) | ctx: 0x00693b78: mov eax, dword ptr [esi + 0x24] ; 0x00693b7b: pop edi ; 0x00693b7c: test eax, eax ; 0x00693b7e: je 0x693ba1
  - 0x00693b0b: je -> 0x00693b59 (jcc_true) | ctx: 0x00693b03: push edi ; 0x00693b04: call 0x56d756 ; 0x00693b09: test eax, eax ; 0x00693b0b: je 0x693b59
  - 0x00693b0b: je -> 0x00693b0d (jcc_false) | ctx: 0x00693b03: push edi ; 0x00693b04: call 0x56d756 ; 0x00693b09: test eax, eax ; 0x00693b0b: je 0x693b59
  - 0x00693b86: jne -> 0x00693ba1 (jcc_true) | ctx: 0x00693b80: sub eax, 1 ; 0x00693b83: mov dword ptr [esi + 0x24], eax ; 0x00693b86: jne 0x693ba1
  - 0x00693b86: jne -> 0x00693b88 (jcc_false) | ctx: 0x00693b80: sub eax, 1 ; 0x00693b83: mov dword ptr [esi + 0x24], eax ; 0x00693b86: jne 0x693ba1
  - 0x00693b5d: jmp -> 0x00693b6f (jmp) | ctx: 0x00693b59: and dword ptr [esi + 0x20], 0 ; 0x00693b5d: jmp 0x693b6f
  - 0x00693b5d: jmp -> 0x00693b6f (jmp) | ctx: 0x00693b50: call 0x57b60f ; 0x00693b55: mov byte ptr [ebp - 4], 0 ; 0x00693b59: and dword ptr [esi + 0x20], 0 ; 0x00693b5d: jmp 0x693b6f
  - 0x00693b98: je -> 0x00693ba1 (jcc_true) | ctx: 0x00693b91: mov ecx, esi ; 0x00693b93: call dword ptr [eax + 0x28] ; 0x00693b96: test al, al ; 0x00693b98: je 0x693ba1
  - 0x00693b98: je -> 0x00693b9a (jcc_false) | ctx: 0x00693b91: mov ecx, esi ; 0x00693b93: call dword ptr [eax + 0x28] ; 0x00693b96: test al, al ; 0x00693b98: je 0x693ba1

### 0x00696a75
- blocks=1, insns=18, edges=3, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehavior@GGL@@ slot 1 (target 0x00696aab, vtable 0x00be1058)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehavior@GGL@@ slot 3 (target 0x00696ab3, vtable 0x00be1058)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehavior@GGL@@ slot 4 (target 0x00696cb4, vtable 0x00be1058)
- branch points:
  - none

### 0x00696d33
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehaviorProps@GGL@@ slot 1 (target 0x00696d4a, vtable 0x00be101c)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehavior@GGL@@ slot 5 (target 0x00696d33, vtable 0x00be1058)
- branch points:
  - none

### 0x006972af
- blocks=5, insns=55, edges=15, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00576019 at 0x006972c2)
- branch points:
  - 0x006972be: jne -> 0x006972c7 (jcc_true) | ctx: 0x006972b7: mov esi, eax ; 0x006972b9: mov dl, byte ptr [esi + 0x5e] ; 0x006972bc: test dl, dl ; 0x006972be: jne 0x6972c7
  - 0x006972be: jne -> 0x006972c0 (jcc_false) | ctx: 0x006972b7: mov esi, eax ; 0x006972b9: mov dl, byte ptr [esi + 0x5e] ; 0x006972bc: test dl, dl ; 0x006972be: jne 0x6972c7
  - 0x006972e5: jne -> 0x00697303 (jcc_true) | ctx: 0x006972db: lea ecx, [esi + 0x30] ; 0x006972de: call 0x6179ea ; 0x006972e3: test eax, eax ; 0x006972e5: jne 0x697303
  - 0x006972e5: jne -> 0x006972e7 (jcc_false) | ctx: 0x006972db: lea ecx, [esi + 0x30] ; 0x006972de: call 0x6179ea ; 0x006972e3: test eax, eax ; 0x006972e5: jne 0x697303
  - 0x006972e5: jne -> 0x00697303 (jcc_true) | ctx: 0x006972db: lea ecx, [esi + 0x30] ; 0x006972de: call 0x6179ea ; 0x006972e3: test eax, eax ; 0x006972e5: jne 0x697303
  - 0x006972e5: jne -> 0x006972e7 (jcc_false) | ctx: 0x006972db: lea ecx, [esi + 0x30] ; 0x006972de: call 0x6179ea ; 0x006972e3: test eax, eax ; 0x006972e5: jne 0x697303

### 0x00697f7b
- blocks=1, insns=9, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerBehaviorProps@GGL@@ slot 1 (target 0x0069805a, vtable 0x00be1178)
  - rtti_vtable_method: .?AVCWorkerBehaviorProps@GGL@@ slot 0 (target 0x00698052, vtable 0x00be1188)
- branch points:
  - none

### 0x00698062
- blocks=1, insns=3, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerBehaviorProps@GGL@@ slot 0 (target 0x00698062, vtable 0x00be1178)
- branch points:
  - none

### 0x00698266
- blocks=1, insns=3, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerBehavior@GGL@@ slot 0 (target 0x00698266, vtable 0x00be1450)
- branch points:
  - none

### 0x0069826d
- blocks=3, insns=17, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerBehavior@GGL@@ slot 3 (target 0x00698379, vtable 0x00be1450)
- branch points:
  - 0x00698276: je -> 0x00698282 (jcc_true) | ctx: 0x0069826d: push esi ; 0x0069826e: mov esi, ecx ; 0x00698270: mov dword ptr [esi], 0xbbe3c8 ; 0x00698276: je 0x698282
  - 0x00698276: je -> 0x00698278 (jcc_false) | ctx: 0x0069826d: push esi ; 0x0069826e: mov esi, ecx ; 0x00698270: mov dword ptr [esi], 0xbbe3c8 ; 0x00698276: je 0x698282

### 0x00699bad
- blocks=11, insns=118, edges=34, jcc=9, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0069826d at 0x00699c9b)
- branch points:
  - 0x00699bcd: jne -> 0x00699c00 (jcc_true) | ctx: 0x00699bc3: call 0x687dae ; 0x00699bc8: mov ebx, dword ptr [ebp + 8] ; 0x00699bcb: cmp eax, ebx ; 0x00699bcd: jne 0x699c00
  - 0x00699bcd: jne -> 0x00699bcf (jcc_false) | ctx: 0x00699bc3: call 0x687dae ; 0x00699bc8: mov ebx, dword ptr [ebp + 8] ; 0x00699bcb: cmp eax, ebx ; 0x00699bcd: jne 0x699c00
  - 0x00699c0f: je -> 0x00699c3c (jcc_true) | ctx: 0x00699c08: mov eax, dword ptr [esi] ; 0x00699c0a: call dword ptr [eax + 0x1c] ; 0x00699c0d: test al, al ; 0x00699c0f: je 0x699c3c
  - 0x00699c0f: je -> 0x00699c11 (jcc_false) | ctx: 0x00699c08: mov eax, dword ptr [esi] ; 0x00699c0a: call dword ptr [eax + 0x1c] ; 0x00699c0d: test al, al ; 0x00699c0f: je 0x699c3c
  - 0x00699be4: je -> 0x00699c00 (jcc_true) | ctx: 0x00699bdc: call 0x629f68 ; 0x00699be1: pop ecx ; 0x00699be2: test eax, eax ; 0x00699be4: je 0x699c00
  - 0x00699be4: je -> 0x00699be6 (jcc_false) | ctx: 0x00699bdc: call 0x629f68 ; 0x00699be1: pop ecx ; 0x00699be2: test eax, eax ; 0x00699be4: je 0x699c00
  - 0x00699c48: je -> 0x00699c78 (jcc_true) | ctx: 0x00699c41: push 0x15 ; 0x00699c43: call dword ptr [eax + 0x1c] ; 0x00699c46: test al, al ; 0x00699c48: je 0x699c78
  - 0x00699c48: je -> 0x00699c4a (jcc_false) | ctx: 0x00699c41: push 0x15 ; 0x00699c43: call dword ptr [eax + 0x1c] ; 0x00699c46: test al, al ; 0x00699c48: je 0x699c78
  - 0x00699c48: je -> 0x00699c78 (jcc_true) | ctx: 0x00699c41: push 0x15 ; 0x00699c43: call dword ptr [eax + 0x1c] ; 0x00699c46: test al, al ; 0x00699c48: je 0x699c78
  - 0x00699c48: je -> 0x00699c4a (jcc_false) | ctx: 0x00699c41: push 0x15 ; 0x00699c43: call dword ptr [eax + 0x1c] ; 0x00699c46: test al, al ; 0x00699c48: je 0x699c78
  - 0x00699c0f: je -> 0x00699c3c (jcc_true) | ctx: 0x00699c08: mov eax, dword ptr [esi] ; 0x00699c0a: call dword ptr [eax + 0x1c] ; 0x00699c0d: test al, al ; 0x00699c0f: je 0x699c3c
  - 0x00699c0f: je -> 0x00699c11 (jcc_false) | ctx: 0x00699c08: mov eax, dword ptr [esi] ; 0x00699c0a: call dword ptr [eax + 0x1c] ; 0x00699c0d: test al, al ; 0x00699c0f: je 0x699c3c
  - 0x00699c84: je -> 0x00699ca0 (jcc_true) | ctx: 0x00699c7d: push 0x17 ; 0x00699c7f: call dword ptr [eax + 0x1c] ; 0x00699c82: test al, al ; 0x00699c84: je 0x699ca0
  - 0x00699c84: je -> 0x00699c86 (jcc_false) | ctx: 0x00699c7d: push 0x17 ; 0x00699c7f: call dword ptr [eax + 0x1c] ; 0x00699c82: test al, al ; 0x00699c84: je 0x699ca0
  - 0x00699c84: je -> 0x00699ca0 (jcc_true) | ctx: 0x00699c7d: push 0x17 ; 0x00699c7f: call dword ptr [eax + 0x1c] ; 0x00699c82: test al, al ; 0x00699c84: je 0x699ca0
  - 0x00699c84: je -> 0x00699c86 (jcc_false) | ctx: 0x00699c7d: push 0x17 ; 0x00699c7f: call dword ptr [eax + 0x1c] ; 0x00699c82: test al, al ; 0x00699c84: je 0x699ca0
  - 0x00699c91: jne -> 0x00699ca0 (jcc_true) | ctx: 0x00699c86: mov eax, dword ptr [edi + 0x20] ; 0x00699c89: cmp dword ptr [eax*4 + 0xbe1434], 1 ; 0x00699c91: jne 0x699ca0
  - 0x00699c91: jne -> 0x00699c93 (jcc_false) | ctx: 0x00699c86: mov eax, dword ptr [edi + 0x20] ; 0x00699c89: cmp dword ptr [eax*4 + 0xbe1434], 1 ; 0x00699c91: jne 0x699ca0

### 0x00699e58
- blocks=5, insns=33, edges=10, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005781c1 at 0x0069a00f)
- branch points:
  - 0x00699e71: jne -> 0x00699e9a (jcc_true) | ctx: 0x00699e6a: test eax, eax ; 0x00699e6c: setne bl ; 0x00699e6f: test eax, eax ; 0x00699e71: jne 0x699e9a
  - 0x00699e71: jne -> 0x00699e73 (jcc_false) | ctx: 0x00699e6a: test eax, eax ; 0x00699e6c: setne bl ; 0x00699e6f: test eax, eax ; 0x00699e71: jne 0x699e9a
  - 0x00699e8f: jle -> 0x00699ea4 (jcc_true) | ctx: 0x00699e81: imul ecx, eax, 0x64 ; 0x00699e84: mov eax, dword ptr [0xf64d54] ; 0x00699e89: cmp ecx, dword ptr [eax + 0x130] ; 0x00699e8f: jle 0x699ea4
  - 0x00699e8f: jle -> 0x00699e91 (jcc_false) | ctx: 0x00699e81: imul ecx, eax, 0x64 ; 0x00699e84: mov eax, dword ptr [0xf64d54] ; 0x00699e89: cmp ecx, dword ptr [eax + 0x130] ; 0x00699e8f: jle 0x699ea4
  - 0x00699e98: jmp -> 0x00699ea4 (jmp) | ctx: 0x00699e91: mov ecx, esi ; 0x00699e93: call 0x69c80d ; 0x00699e98: jmp 0x699ea4

### 0x0069a053
- blocks=4, insns=27, edges=8, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerBehavior@GGL@@ slot 1 (target 0x0069a095, vtable 0x00be1450)
  - caller_of_anchor_path: depth 1 (calls 0x0069a053 at 0x0069a0df)
- branch points:
  - 0x0069a06b: je -> 0x0069a086 (jcc_true) | ctx: 0x0069a061: lea ecx, [eax + 0x30] ; 0x0069a064: call 0x6179ea ; 0x0069a069: test eax, eax ; 0x0069a06b: je 0x69a086
  - 0x0069a06b: je -> 0x0069a06d (jcc_false) | ctx: 0x0069a061: lea ecx, [eax + 0x30] ; 0x0069a064: call 0x6179ea ; 0x0069a069: test eax, eax ; 0x0069a06b: je 0x69a086
  - 0x0069a07b: je -> 0x0069a086 (jcc_true) | ctx: 0x0069a073: push eax ; 0x0069a074: call 0x56d756 ; 0x0069a079: test eax, eax ; 0x0069a07b: je 0x69a086
  - 0x0069a07b: je -> 0x0069a07d (jcc_false) | ctx: 0x0069a073: push eax ; 0x0069a074: call 0x56d756 ; 0x0069a079: test eax, eax ; 0x0069a07b: je 0x69a086

### 0x0069a48a
- blocks=4, insns=465, edges=21, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0069a053 at 0x0069ac14)
- branch points:
  - 0x0069a4aa: jg -> 0x0069a4b5 (jcc_true) | ctx: 0x0069a49c: mov ecx, dword ptr [eax + ecx*4] ; 0x0069a49f: mov eax, dword ptr [0xf77db0] ; 0x0069a4a4: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0069a4aa: jg 0x69a4b5
  - 0x0069a4aa: jg -> 0x0069a4ac (jcc_false) | ctx: 0x0069a49c: mov ecx, dword ptr [eax + ecx*4] ; 0x0069a49f: mov eax, dword ptr [0xf77db0] ; 0x0069a4a4: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0069a4aa: jg 0x69a4b5
  - 0x0069a4c7: jne -> 0x0069a4ac (jcc_true) | ctx: 0x0069a4ba: call 0xab6ba9 ; 0x0069a4bf: cmp dword ptr [0xf77db0], -1 ; 0x0069a4c6: pop ecx ; 0x0069a4c7: jne 0x69a4ac
  - 0x0069a4c7: jne -> 0x0069a4c9 (jcc_false) | ctx: 0x0069a4ba: call 0xab6ba9 ; 0x0069a4bf: cmp dword ptr [0xf77db0], -1 ; 0x0069a4c6: pop ecx ; 0x0069a4c7: jne 0x69a4ac
  - 0x0069aaf2: jmp -> 0x0069a4ac (jmp) | ctx: 0x0069aaef: pop edi ; 0x0069aaf0: pop esi ; 0x0069aaf1: pop ebx ; 0x0069aaf2: jmp 0x69a4ac

### 0x0069aca4
- blocks=5, insns=41, edges=10, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0069a053 at 0x0069ad08)
- branch points:
  - 0x0069acc6: je -> 0x0069acce (jcc_true) | ctx: 0x0069acbd: mov ecx, ebx ; 0x0069acbf: call 0x6179ea ; 0x0069acc4: test eax, eax ; 0x0069acc6: je 0x69acce
  - 0x0069acc6: je -> 0x0069acc8 (jcc_false) | ctx: 0x0069acbd: mov ecx, ebx ; 0x0069acbf: call 0x6179ea ; 0x0069acc4: test eax, eax ; 0x0069acc6: je 0x69acce
  - 0x0069acd9: je -> 0x0069ace1 (jcc_true) | ctx: 0x0069acd0: mov ecx, ebx ; 0x0069acd2: call 0x6179ea ; 0x0069acd7: test eax, eax ; 0x0069acd9: je 0x69ace1
  - 0x0069acd9: je -> 0x0069acdb (jcc_false) | ctx: 0x0069acd0: mov ecx, ebx ; 0x0069acd2: call 0x6179ea ; 0x0069acd7: test eax, eax ; 0x0069acd9: je 0x69ace1
  - 0x0069acd9: je -> 0x0069ace1 (jcc_true) | ctx: 0x0069acd0: mov ecx, ebx ; 0x0069acd2: call 0x6179ea ; 0x0069acd7: test eax, eax ; 0x0069acd9: je 0x69ace1
  - 0x0069acd9: je -> 0x0069acdb (jcc_false) | ctx: 0x0069acd0: mov ecx, ebx ; 0x0069acd2: call 0x6179ea ; 0x0069acd7: test eax, eax ; 0x0069acd9: je 0x69ace1

### 0x0069ae66
- blocks=4, insns=20, edges=8, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0069826d at 0x0069ae95)
  - caller_of_anchor_path: depth 2 (calls 0x00576019 at 0x0069ae8e)
- branch points:
  - 0x0069ae74: jne -> 0x0069ae9a (jcc_true) | ctx: 0x0069ae67: mov esi, ecx ; 0x0069ae69: mov eax, dword ptr [esi + 0x20] ; 0x0069ae6c: cmp dword ptr [eax*4 + 0xbe1434], 2 ; 0x0069ae74: jne 0x69ae9a
  - 0x0069ae74: jne -> 0x0069ae76 (jcc_false) | ctx: 0x0069ae67: mov esi, ecx ; 0x0069ae69: mov eax, dword ptr [esi + 0x20] ; 0x0069ae6c: cmp dword ptr [eax*4 + 0xbe1434], 2 ; 0x0069ae74: jne 0x69ae9a
  - 0x0069ae7d: jne -> 0x0069ae9a (jcc_true) | ctx: 0x0069ae76: call 0x69c6e4 ; 0x0069ae7b: test al, al ; 0x0069ae7d: jne 0x69ae9a
  - 0x0069ae7d: jne -> 0x0069ae7f (jcc_false) | ctx: 0x0069ae76: call 0x69c6e4 ; 0x0069ae7b: test al, al ; 0x0069ae7d: jne 0x69ae9a

### 0x0069ae9e
- blocks=12, insns=63, edges=26, jcc=9, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0069826d at 0x0069af40)
- branch points:
  - 0x0069aea5: jne -> 0x0069af46 (jcc_true) | ctx: 0x0069ae9e: push edi ; 0x0069ae9f: mov edi, ecx ; 0x0069aea1: cmp byte ptr [edi + 0x3d], 0 ; 0x0069aea5: jne 0x69af46
  - 0x0069aea5: jne -> 0x0069aeab (jcc_false) | ctx: 0x0069ae9e: push edi ; 0x0069ae9f: mov edi, ecx ; 0x0069aea1: cmp byte ptr [edi + 0x3d], 0 ; 0x0069aea5: jne 0x69af46
  - 0x0069aebb: je -> 0x0069aef8 (jcc_true) | ctx: 0x0069aeac: mov ebx, dword ptr [0xdf5ee4] ; 0x0069aeb2: call 0x56d8a7 ; 0x0069aeb7: cmp dword ptr [eax + 0x7c], 0 ; 0x0069aebb: je 0x69aef8
  - 0x0069aebb: je -> 0x0069aebd (jcc_false) | ctx: 0x0069aeac: mov ebx, dword ptr [0xdf5ee4] ; 0x0069aeb2: call 0x56d8a7 ; 0x0069aeb7: cmp dword ptr [eax + 0x7c], 0 ; 0x0069aebb: je 0x69aef8
  - 0x0069af29: jne -> 0x0069af3e (jcc_true) | ctx: 0x0069af1f: or dword ptr [edi + 0x20], 0xffffffff ; 0x0069af23: xor eax, eax ; 0x0069af25: cmp dword ptr [edi + 0x20], -1 ; 0x0069af29: jne 0x69af3e
  - 0x0069af29: jne -> 0x0069af2b (jcc_false) | ctx: 0x0069af1f: or dword ptr [edi + 0x20], 0xffffffff ; 0x0069af23: xor eax, eax ; 0x0069af25: cmp dword ptr [edi + 0x20], -1 ; 0x0069af29: jne 0x69af3e
  - 0x0069aed0: je -> 0x0069aef8 (jcc_true) | ctx: 0x0069aec6: push dword ptr [eax + 0x7c] ; 0x0069aec9: call 0x58ae50 ; 0x0069aece: test eax, eax ; 0x0069aed0: je 0x69aef8
  - 0x0069aed0: je -> 0x0069aed2 (jcc_false) | ctx: 0x0069aec6: push dword ptr [eax + 0x7c] ; 0x0069aec9: call 0x58ae50 ; 0x0069aece: test eax, eax ; 0x0069aed0: je 0x69aef8
  - 0x0069af33: jne -> 0x0069af38 (jcc_true) | ctx: 0x0069af2b: cmp dword ptr [eax*4 + 0xbe1434], 0 ; 0x0069af33: jne 0x69af38
  - 0x0069af33: jne -> 0x0069af35 (jcc_false) | ctx: 0x0069af2b: cmp dword ptr [eax*4 + 0xbe1434], 0 ; 0x0069af33: jne 0x69af38
  - 0x0069aef6: je -> 0x0069af45 (jcc_true) | ctx: 0x0069aeee: call 0x58ad88 ; 0x0069aef3: cmp esi, eax ; 0x0069aef5: pop esi ; 0x0069aef6: je 0x69af45
  - 0x0069aef6: je -> 0x0069aef8 (jcc_false) | ctx: 0x0069aeee: call 0x58ad88 ; 0x0069aef3: cmp esi, eax ; 0x0069aef5: pop esi ; 0x0069aef6: je 0x69af45
  - 0x0069af3c: jl -> 0x0069af25 (jcc_true) | ctx: 0x0069af38: inc eax ; 0x0069af39: cmp eax, 6 ; 0x0069af3c: jl 0x69af25
  - 0x0069af3c: jl -> 0x0069af3e (jcc_false) | ctx: 0x0069af38: inc eax ; 0x0069af39: cmp eax, 6 ; 0x0069af3c: jl 0x69af25
  - 0x0069af3c: jl -> 0x0069af25 (jcc_true) | ctx: 0x0069af35: mov dword ptr [edi + 0x20], eax ; 0x0069af38: inc eax ; 0x0069af39: cmp eax, 6 ; 0x0069af3c: jl 0x69af25
  - 0x0069af3c: jl -> 0x0069af3e (jcc_false) | ctx: 0x0069af35: mov dword ptr [edi + 0x20], eax ; 0x0069af38: inc eax ; 0x0069af39: cmp eax, 6 ; 0x0069af3c: jl 0x69af25
  - 0x0069af29: jne -> 0x0069af3e (jcc_true) | ctx: 0x0069af25: cmp dword ptr [edi + 0x20], -1 ; 0x0069af29: jne 0x69af3e
  - 0x0069af29: jne -> 0x0069af2b (jcc_false) | ctx: 0x0069af25: cmp dword ptr [edi + 0x20], -1 ; 0x0069af29: jne 0x69af3e

### 0x0069b0ab
- blocks=4, insns=20, edges=8, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0069826d at 0x0069b0da)
  - caller_of_anchor_path: depth 2 (calls 0x00576019 at 0x0069b0d3)
- branch points:
  - 0x0069b0b9: jne -> 0x0069b0df (jcc_true) | ctx: 0x0069b0ac: mov esi, ecx ; 0x0069b0ae: mov eax, dword ptr [esi + 0x20] ; 0x0069b0b1: cmp dword ptr [eax*4 + 0xbe1434], 3 ; 0x0069b0b9: jne 0x69b0df
  - 0x0069b0b9: jne -> 0x0069b0bb (jcc_false) | ctx: 0x0069b0ac: mov esi, ecx ; 0x0069b0ae: mov eax, dword ptr [esi + 0x20] ; 0x0069b0b1: cmp dword ptr [eax*4 + 0xbe1434], 3 ; 0x0069b0b9: jne 0x69b0df
  - 0x0069b0c2: jne -> 0x0069b0df (jcc_true) | ctx: 0x0069b0bb: call 0x69c6e4 ; 0x0069b0c0: test al, al ; 0x0069b0c2: jne 0x69b0df
  - 0x0069b0c2: jne -> 0x0069b0c4 (jcc_false) | ctx: 0x0069b0bb: call 0x69c6e4 ; 0x0069b0c0: test al, al ; 0x0069b0c2: jne 0x69b0df

### 0x0069b103
- blocks=4, insns=25, edges=9, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0069826d at 0x0069b142)
  - caller_of_anchor_path: depth 2 (calls 0x00576019 at 0x0069b13b)
- branch points:
  - 0x0069b11f: jne -> 0x0069b147 (jcc_true) | ctx: 0x0069b111: mov dword ptr [esi + 0x38], eax ; 0x0069b114: mov eax, dword ptr [esi + 0x20] ; 0x0069b117: cmp dword ptr [eax*4 + 0xbe1434], 1 ; 0x0069b11f: jne 0x69b147
  - 0x0069b11f: jne -> 0x0069b121 (jcc_false) | ctx: 0x0069b111: mov dword ptr [esi + 0x38], eax ; 0x0069b114: mov eax, dword ptr [esi + 0x20] ; 0x0069b117: cmp dword ptr [eax*4 + 0xbe1434], 1 ; 0x0069b11f: jne 0x69b147
  - 0x0069b12a: jne -> 0x0069b147 (jcc_true) | ctx: 0x0069b121: mov ecx, esi ; 0x0069b123: call 0x69c6e4 ; 0x0069b128: test al, al ; 0x0069b12a: jne 0x69b147
  - 0x0069b12a: jne -> 0x0069b12c (jcc_false) | ctx: 0x0069b121: mov ecx, esi ; 0x0069b123: call 0x69c6e4 ; 0x0069b128: test al, al ; 0x0069b12a: jne 0x69b147

### 0x0069b176
- blocks=8, insns=53, edges=13, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0069826d at 0x0069b293)
  - caller_of_anchor_path: depth 1 (calls 0x0069a053 at 0x0069b249)
- branch points:
  - 0x0069b180: je -> 0x0069b186 (jcc_true) | ctx: 0x0069b177: mov esi, ecx ; 0x0069b179: call 0x69c7d1 ; 0x0069b17e: test al, al ; 0x0069b180: je 0x69b186
  - 0x0069b180: je -> 0x0069b182 (jcc_false) | ctx: 0x0069b177: mov esi, ecx ; 0x0069b179: call 0x69c7d1 ; 0x0069b17e: test al, al ; 0x0069b180: je 0x69b186
  - 0x0069b1b2: jne -> 0x0069b1c2 (jcc_true) | ctx: 0x0069b1a9: mov ecx, eax ; 0x0069b1ab: call dword ptr [edx + 0x40] ; 0x0069b1ae: cmp dword ptr [ebp - 0x10], 0 ; 0x0069b1b2: jne 0x69b1c2
  - 0x0069b1b2: jne -> 0x0069b1b4 (jcc_false) | ctx: 0x0069b1a9: mov ecx, eax ; 0x0069b1ab: call dword ptr [edx + 0x40] ; 0x0069b1ae: cmp dword ptr [ebp - 0x10], 0 ; 0x0069b1b2: jne 0x69b1c2
  - 0x0069b184: jmp -> 0x0069b1d8 (jmp) | ctx: 0x0069b182: xor eax, eax ; 0x0069b184: jmp 0x69b1d8
  - 0x0069b1bb: jle -> 0x0069b1d5 (jcc_true) | ctx: 0x0069b1b4: dec dword ptr [esi + 0x40] ; 0x0069b1b7: cmp dword ptr [esi + 0x40], 0 ; 0x0069b1bb: jle 0x69b1d5
  - 0x0069b1bb: jle -> 0x0069b1bd (jcc_false) | ctx: 0x0069b1b4: dec dword ptr [esi + 0x40] ; 0x0069b1b7: cmp dword ptr [esi + 0x40], 0 ; 0x0069b1bb: jle 0x69b1d5
  - 0x0069b1c0: jmp -> 0x0069b1d8 (jmp) | ctx: 0x0069b1bd: or eax, 0xffffffff ; 0x0069b1c0: jmp 0x69b1d8

### 0x0069b4d7
- blocks=3, insns=15, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0069826d at 0x0069b4eb)
- branch points:
  - 0x0069b4e1: je -> 0x0069b4f0 (jcc_true) | ctx: 0x0069b4d8: mov esi, ecx ; 0x0069b4da: call 0x69c5a1 ; 0x0069b4df: test al, al ; 0x0069b4e1: je 0x69b4f0
  - 0x0069b4e1: je -> 0x0069b4e3 (jcc_false) | ctx: 0x0069b4d8: mov esi, ecx ; 0x0069b4da: call 0x69c5a1 ; 0x0069b4df: test al, al ; 0x0069b4e1: je 0x69b4f0

### 0x0069c12e
- blocks=3, insns=15, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0069826d at 0x0069c13e)
  - caller_of_anchor_path: depth 1 (calls 0x0069a053 at 0x0069c226)
  - caller_of_anchor_path: depth 1 (calls 0x0069a053 at 0x0069c28e)
- branch points:
  - 0x0069c13a: jne -> 0x0069c143 (jcc_true) | ctx: 0x0069c12f: mov esi, ecx ; 0x0069c131: call 0x69c9c7 ; 0x0069c136: cmp byte ptr [esi + 0x3d], 0 ; 0x0069c13a: jne 0x69c143
  - 0x0069c13a: jne -> 0x0069c13c (jcc_false) | ctx: 0x0069c12f: mov esi, ecx ; 0x0069c131: call 0x69c9c7 ; 0x0069c136: cmp byte ptr [esi + 0x3d], 0 ; 0x0069c13a: jne 0x69c143

### 0x0069c3d0
- blocks=8, insns=82, edges=20, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0069826d at 0x0069c3e6)
- branch points:
  - 0x0069c3de: jne -> 0x0069c3f3 (jcc_true) | ctx: 0x0069c3d8: mov ebx, eax ; 0x0069c3da: mov ecx, esi ; 0x0069c3dc: test ebx, ebx ; 0x0069c3de: jne 0x69c3f3
  - 0x0069c3de: jne -> 0x0069c3e0 (jcc_false) | ctx: 0x0069c3d8: mov ebx, eax ; 0x0069c3da: mov ecx, esi ; 0x0069c3dc: test ebx, ebx ; 0x0069c3de: jne 0x69c3f3
  - 0x0069c404: je -> 0x0069c476 (jcc_true) | ctx: 0x0069c3ff: mov edi, eax ; 0x0069c401: pop ecx ; 0x0069c402: test edi, edi ; 0x0069c404: je 0x69c476
  - 0x0069c404: je -> 0x0069c406 (jcc_false) | ctx: 0x0069c3ff: mov edi, eax ; 0x0069c401: pop ecx ; 0x0069c402: test edi, edi ; 0x0069c404: je 0x69c476
  - 0x0069c3ee: jmp -> 0x0069c479 (jmp) | ctx: 0x0069c3e6: call 0x698289 ; 0x0069c3eb: push 2 ; 0x0069c3ed: pop eax ; 0x0069c3ee: jmp 0x69c479
  - 0x0069c412: je -> 0x0069c476 (jcc_true) | ctx: 0x0069c409: mov ecx, edi ; 0x0069c40b: call 0x689351 ; 0x0069c410: test al, al ; 0x0069c412: je 0x69c476
  - 0x0069c412: je -> 0x0069c414 (jcc_false) | ctx: 0x0069c409: mov ecx, edi ; 0x0069c40b: call 0x689351 ; 0x0069c410: test al, al ; 0x0069c412: je 0x69c476
  - 0x0069c420: jne -> 0x0069c476 (jcc_true) | ctx: 0x0069c416: lea ecx, [edi + 0x30] ; 0x0069c419: call 0x6179ea ; 0x0069c41e: test eax, eax ; 0x0069c420: jne 0x69c476
  - 0x0069c420: jne -> 0x0069c422 (jcc_false) | ctx: 0x0069c416: lea ecx, [edi + 0x30] ; 0x0069c419: call 0x6179ea ; 0x0069c41e: test eax, eax ; 0x0069c420: jne 0x69c476

### 0x0069c627
- blocks=3, insns=20, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerBehavior@GGL@@ slot 5 (target 0x0069c627, vtable 0x00be1450)
- branch points:
  - 0x0069c648: je -> 0x0069c64d (jcc_true) | ctx: 0x0069c63e: call 0xad21fe ; 0x0069c643: add esp, 0x14 ; 0x0069c646: test eax, eax ; 0x0069c648: je 0x69c64d
  - 0x0069c648: je -> 0x0069c64a (jcc_false) | ctx: 0x0069c63e: call 0xad21fe ; 0x0069c643: add esp, 0x14 ; 0x0069c646: test eax, eax ; 0x0069c648: je 0x69c64d

### 0x0069c652
- blocks=8, insns=63, edges=22, jcc=7, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerBehavior@GGL@@ slot 4 (target 0x0069c652, vtable 0x00be1450)
  - caller_of_anchor_path: depth 1 (calls 0x0069826d at 0x0069c6d8)
- branch points:
  - 0x0069c677: je -> 0x0069c6ab (jcc_true) | ctx: 0x0069c670: mov ebx, eax ; 0x0069c672: add esp, 0x14 ; 0x0069c675: test ebx, ebx ; 0x0069c677: je 0x69c6ab
  - 0x0069c677: je -> 0x0069c679 (jcc_false) | ctx: 0x0069c670: mov ebx, eax ; 0x0069c672: add esp, 0x14 ; 0x0069c675: test ebx, ebx ; 0x0069c677: je 0x69c6ab
  - 0x0069c6c1: jne -> 0x0069c6d6 (jcc_true) | ctx: 0x0069c6b6: or dword ptr [edi + 0x20], 0xffffffff ; 0x0069c6ba: mov dword ptr [edi + 0x38], eax ; 0x0069c6bd: cmp dword ptr [edi + 0x20], -1 ; 0x0069c6c1: jne 0x69c6d6
  - 0x0069c6c1: jne -> 0x0069c6c3 (jcc_false) | ctx: 0x0069c6b6: or dword ptr [edi + 0x20], 0xffffffff ; 0x0069c6ba: mov dword ptr [edi + 0x38], eax ; 0x0069c6bd: cmp dword ptr [edi + 0x20], -1 ; 0x0069c6c1: jne 0x69c6d6
  - 0x0069c6c1: jne -> 0x0069c6d6 (jcc_true) | ctx: 0x0069c6b6: or dword ptr [edi + 0x20], 0xffffffff ; 0x0069c6ba: mov dword ptr [edi + 0x38], eax ; 0x0069c6bd: cmp dword ptr [edi + 0x20], -1 ; 0x0069c6c1: jne 0x69c6d6
  - 0x0069c6c1: jne -> 0x0069c6c3 (jcc_false) | ctx: 0x0069c6b6: or dword ptr [edi + 0x20], 0xffffffff ; 0x0069c6ba: mov dword ptr [edi + 0x38], eax ; 0x0069c6bd: cmp dword ptr [edi + 0x20], -1 ; 0x0069c6c1: jne 0x69c6d6
  - 0x0069c6cb: jne -> 0x0069c6d0 (jcc_true) | ctx: 0x0069c6c3: cmp dword ptr [esi*4 + 0xbe1434], -1 ; 0x0069c6cb: jne 0x69c6d0
  - 0x0069c6cb: jne -> 0x0069c6cd (jcc_false) | ctx: 0x0069c6c3: cmp dword ptr [esi*4 + 0xbe1434], -1 ; 0x0069c6cb: jne 0x69c6d0
  - 0x0069c6d4: jl -> 0x0069c6bd (jcc_true) | ctx: 0x0069c6d0: inc esi ; 0x0069c6d1: cmp esi, 6 ; 0x0069c6d4: jl 0x69c6bd
  - 0x0069c6d4: jl -> 0x0069c6d6 (jcc_false) | ctx: 0x0069c6d0: inc esi ; 0x0069c6d1: cmp esi, 6 ; 0x0069c6d4: jl 0x69c6bd
  - 0x0069c6d4: jl -> 0x0069c6bd (jcc_true) | ctx: 0x0069c6cd: mov dword ptr [edi + 0x20], esi ; 0x0069c6d0: inc esi ; 0x0069c6d1: cmp esi, 6 ; 0x0069c6d4: jl 0x69c6bd
  - 0x0069c6d4: jl -> 0x0069c6d6 (jcc_false) | ctx: 0x0069c6cd: mov dword ptr [edi + 0x20], esi ; 0x0069c6d0: inc esi ; 0x0069c6d1: cmp esi, 6 ; 0x0069c6d4: jl 0x69c6bd
  - 0x0069c6c1: jne -> 0x0069c6d6 (jcc_true) | ctx: 0x0069c6bd: cmp dword ptr [edi + 0x20], -1 ; 0x0069c6c1: jne 0x69c6d6
  - 0x0069c6c1: jne -> 0x0069c6c3 (jcc_false) | ctx: 0x0069c6bd: cmp dword ptr [edi + 0x20], -1 ; 0x0069c6c1: jne 0x69c6d6

### 0x0069c7d1
- blocks=5, insns=24, edges=10, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0069826d at 0x0069c7e9)
- branch points:
  - 0x0069c7e7: jne -> 0x0069c7f2 (jcc_true) | ctx: 0x0069c7de: call 0x6179ea ; 0x0069c7e3: mov ecx, esi ; 0x0069c7e5: test eax, eax ; 0x0069c7e7: jne 0x69c7f2
  - 0x0069c7e7: jne -> 0x0069c7e9 (jcc_false) | ctx: 0x0069c7de: call 0x6179ea ; 0x0069c7e3: mov ecx, esi ; 0x0069c7e5: test eax, eax ; 0x0069c7e7: jne 0x69c7f2
  - 0x0069c7f9: jne -> 0x0069c7ff (jcc_true) | ctx: 0x0069c7f2: call 0x69acf5 ; 0x0069c7f7: test eax, eax ; 0x0069c7f9: jne 0x69c7ff
  - 0x0069c7f9: jne -> 0x0069c7fb (jcc_false) | ctx: 0x0069c7f2: call 0x69acf5 ; 0x0069c7f7: test eax, eax ; 0x0069c7f9: jne 0x69c7ff
  - 0x0069c7fd: jmp -> 0x0069c7e9 (jmp) | ctx: 0x0069c7fb: mov ecx, esi ; 0x0069c7fd: jmp 0x69c7e9

### 0x0069c99d
- blocks=3, insns=18, edges=6, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00576019 at 0x0069c9b4)
- branch points:
  - 0x0069c9a7: jne -> 0x0069c9c5 (jcc_true) | ctx: 0x0069c99e: mov esi, ecx ; 0x0069c9a0: call 0x69c6e4 ; 0x0069c9a5: test al, al ; 0x0069c9a7: jne 0x69c9c5
  - 0x0069c9a7: jne -> 0x0069c9a9 (jcc_false) | ctx: 0x0069c99e: mov esi, ecx ; 0x0069c9a0: call 0x69c6e4 ; 0x0069c9a5: test al, al ; 0x0069c9a7: jne 0x69c9c5

### 0x0069c9d5
- blocks=32, insns=237, edges=72, jcc=16, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0069826d at 0x0069ca02)
- branch points:
  - 0x0069c9e5: je -> 0x0069cbf3 (jcc_true) | ctx: 0x0069c9d8: mov eax, dword ptr [edi + 0x20] ; 0x0069c9db: mov eax, dword ptr [eax*4 + 0xbe1434] ; 0x0069c9e2: sub eax, 0 ; 0x0069c9e5: je 0x69cbf3
  - 0x0069c9e5: je -> 0x0069c9eb (jcc_false) | ctx: 0x0069c9d8: mov eax, dword ptr [edi + 0x20] ; 0x0069c9db: mov eax, dword ptr [eax*4 + 0xbe1434] ; 0x0069c9e2: sub eax, 0 ; 0x0069c9e5: je 0x69cbf3
  - 0x0069c9ee: je -> 0x0069cb80 (jcc_true) | ctx: 0x0069c9eb: sub eax, 1 ; 0x0069c9ee: je 0x69cb80
  - 0x0069c9ee: je -> 0x0069c9f4 (jcc_false) | ctx: 0x0069c9eb: sub eax, 1 ; 0x0069c9ee: je 0x69cb80
  - 0x0069cb87: je -> 0x0069cbd0 (jcc_true) | ctx: 0x0069cb80: call 0x699e57 ; 0x0069cb85: test al, al ; 0x0069cb87: je 0x69cbd0
  - 0x0069cb87: je -> 0x0069cb89 (jcc_false) | ctx: 0x0069cb80: call 0x699e57 ; 0x0069cb85: test al, al ; 0x0069cb87: je 0x69cbd0
  - 0x0069c9f7: je -> 0x0069cae1 (jcc_true) | ctx: 0x0069c9f4: sub eax, 1 ; 0x0069c9f7: je 0x69cae1
  - 0x0069c9f7: je -> 0x0069c9fd (jcc_false) | ctx: 0x0069c9f4: sub eax, 1 ; 0x0069c9f7: je 0x69cae1
  - 0x0069cbd4: jne -> 0x0069cbf3 (jcc_true) | ctx: 0x0069cbd0: cmp byte ptr [edi + 0x3d], 0 ; 0x0069cbd4: jne 0x69cbf3
  - 0x0069cbd4: jne -> 0x0069cbd6 (jcc_false) | ctx: 0x0069cbd0: cmp byte ptr [edi + 0x3d], 0 ; 0x0069cbd4: jne 0x69cbf3
  - 0x0069cbcb: jmp -> 0x0069ca93 (jmp) | ctx: 0x0069cbc3: push 1 ; 0x0069cbc5: call 0x69ac5e ; 0x0069cbca: push eax ; 0x0069cbcb: jmp 0x69ca93
  - 0x0069caf0: je -> 0x0069cb4f (jcc_true) | ctx: 0x0069cae7: test al, al ; 0x0069cae9: mov ecx, edi ; 0x0069caeb: mov eax, dword ptr [0xf64d54] ; 0x0069caf0: je 0x69cb4f
  - 0x0069caf0: je -> 0x0069caf2 (jcc_false) | ctx: 0x0069cae7: test al, al ; 0x0069cae9: mov ecx, edi ; 0x0069caeb: mov eax, dword ptr [0xf64d54] ; 0x0069caf0: je 0x69cb4f
  - 0x0069ca00: je -> 0x0069ca0c (jcc_true) | ctx: 0x0069c9fd: sub eax, 1 ; 0x0069ca00: je 0x69ca0c
  - 0x0069ca00: je -> 0x0069ca02 (jcc_false) | ctx: 0x0069c9fd: sub eax, 1 ; 0x0069ca00: je 0x69ca0c
  - 0x0069ca95: jmp -> 0x0069cbee (jmp) | ctx: 0x0069ca93: mov ecx, esi ; 0x0069ca95: jmp 0x69cbee
  - 0x0069cb71: jle -> 0x0069cb76 (jcc_true) | ctx: 0x0069cb66: mov dword ptr [edi + 0x14], eax ; 0x0069cb69: call 0x69aca2 ; 0x0069cb6e: cmp dword ptr [edi + 0x14], eax ; 0x0069cb71: jle 0x69cb76
  - 0x0069cb71: jle -> 0x0069cb73 (jcc_false) | ctx: 0x0069cb66: mov dword ptr [edi + 0x14], eax ; 0x0069cb69: call 0x69aca2 ; 0x0069cb6e: cmp dword ptr [edi + 0x14], eax ; 0x0069cb71: jle 0x69cb76
  - 0x0069cb14: jle -> 0x0069cb19 (jcc_true) | ctx: 0x0069cb09: mov dword ptr [edi + 0x14], eax ; 0x0069cb0c: call 0x69aca2 ; 0x0069cb11: cmp dword ptr [edi + 0x14], eax ; 0x0069cb14: jle 0x69cb19
  - 0x0069cb14: jle -> 0x0069cb16 (jcc_false) | ctx: 0x0069cb09: mov dword ptr [edi + 0x14], eax ; 0x0069cb0c: call 0x69aca2 ; 0x0069cb11: cmp dword ptr [edi + 0x14], eax ; 0x0069cb14: jle 0x69cb19
  - 0x0069ca1b: je -> 0x0069ca9a (jcc_true) | ctx: 0x0069ca12: test al, al ; 0x0069ca14: mov ecx, edi ; 0x0069ca16: mov eax, dword ptr [0xf64d54] ; 0x0069ca1b: je 0x69ca9a
  - 0x0069ca1b: je -> 0x0069ca1d (jcc_false) | ctx: 0x0069ca12: test al, al ; 0x0069ca14: mov ecx, edi ; 0x0069ca16: mov eax, dword ptr [0xf64d54] ; 0x0069ca1b: je 0x69ca9a
  - 0x0069ca07: jmp -> 0x0069cbf3 (jmp) | ctx: 0x0069ca02: call 0x698289 ; 0x0069ca07: jmp 0x69cbf3
  - 0x0069cb7e: jmp -> 0x0069cbe5 (jmp) | ctx: 0x0069cb76: mov eax, dword ptr [edi + 0x1c] ; 0x0069cb79: push 1 ; 0x0069cb7b: push dword ptr [eax + 0x24] ; 0x0069cb7e: jmp 0x69cbe5
  - 0x0069cb7e: jmp -> 0x0069cbe5 (jmp) | ctx: 0x0069cb76: mov eax, dword ptr [edi + 0x1c] ; 0x0069cb79: push 1 ; 0x0069cb7b: push dword ptr [eax + 0x24] ; 0x0069cb7e: jmp 0x69cbe5
  - 0x0069cb4a: jmp -> 0x0069ca8f (jmp) | ctx: 0x0069cb42: mov eax, dword ptr [edi + 0x1c] ; 0x0069cb45: push 1 ; 0x0069cb47: push dword ptr [eax + 0x20] ; 0x0069cb4a: jmp 0x69ca8f
  - 0x0069cb4a: jmp -> 0x0069ca8f (jmp) | ctx: 0x0069cb42: mov eax, dword ptr [edi + 0x1c] ; 0x0069cb45: push 1 ; 0x0069cb47: push dword ptr [eax + 0x20] ; 0x0069cb4a: jmp 0x69ca8f
  - 0x0069cabc: jle -> 0x0069cac1 (jcc_true) | ctx: 0x0069cab1: mov dword ptr [edi + 0x14], eax ; 0x0069cab4: call 0x69aca2 ; 0x0069cab9: cmp dword ptr [edi + 0x14], eax ; 0x0069cabc: jle 0x69cac1
  - 0x0069cabc: jle -> 0x0069cabe (jcc_false) | ctx: 0x0069cab1: mov dword ptr [edi + 0x14], eax ; 0x0069cab4: call 0x69aca2 ; 0x0069cab9: cmp dword ptr [edi + 0x14], eax ; 0x0069cabc: jle 0x69cac1
  - 0x0069ca3f: jle -> 0x0069ca44 (jcc_true) | ctx: 0x0069ca34: mov dword ptr [edi + 0x14], eax ; 0x0069ca37: call 0x69aca2 ; 0x0069ca3c: cmp dword ptr [edi + 0x14], eax ; 0x0069ca3f: jle 0x69ca44
  - 0x0069ca3f: jle -> 0x0069ca41 (jcc_false) | ctx: 0x0069ca34: mov dword ptr [edi + 0x14], eax ; 0x0069ca37: call 0x69aca2 ; 0x0069ca3c: cmp dword ptr [edi + 0x14], eax ; 0x0069ca3f: jle 0x69ca44
  - 0x0069ca95: jmp -> 0x0069cbee (jmp) | ctx: 0x0069ca8f: or dword ptr [ebp - 4], 0xffffffff ; 0x0069ca93: mov ecx, esi ; 0x0069ca95: jmp 0x69cbee
  - 0x0069cacf: jge -> 0x0069cad4 (jcc_true) | ctx: 0x0069cac1: mov eax, dword ptr [0xf64d54] ; 0x0069cac6: mov eax, dword ptr [eax + 0x118] ; 0x0069cacc: cmp dword ptr [edi + 0x14], eax ; 0x0069cacf: jge 0x69cad4
  - 0x0069cacf: jge -> 0x0069cad1 (jcc_false) | ctx: 0x0069cac1: mov eax, dword ptr [0xf64d54] ; 0x0069cac6: mov eax, dword ptr [eax + 0x118] ; 0x0069cacc: cmp dword ptr [edi + 0x14], eax ; 0x0069cacf: jge 0x69cad4
  - 0x0069cacf: jge -> 0x0069cad4 (jcc_true) | ctx: 0x0069cac1: mov eax, dword ptr [0xf64d54] ; 0x0069cac6: mov eax, dword ptr [eax + 0x118] ; 0x0069cacc: cmp dword ptr [edi + 0x14], eax ; 0x0069cacf: jge 0x69cad4
  - 0x0069cacf: jge -> 0x0069cad1 (jcc_false) | ctx: 0x0069cac1: mov eax, dword ptr [0xf64d54] ; 0x0069cac6: mov eax, dword ptr [eax + 0x118] ; 0x0069cacc: cmp dword ptr [edi + 0x14], eax ; 0x0069cacf: jge 0x69cad4
  - 0x0069ca52: jge -> 0x0069ca57 (jcc_true) | ctx: 0x0069ca44: mov eax, dword ptr [0xf64d54] ; 0x0069ca49: mov eax, dword ptr [eax + 0x118] ; 0x0069ca4f: cmp dword ptr [edi + 0x14], eax ; 0x0069ca52: jge 0x69ca57
  - 0x0069ca52: jge -> 0x0069ca54 (jcc_false) | ctx: 0x0069ca44: mov eax, dword ptr [0xf64d54] ; 0x0069ca49: mov eax, dword ptr [eax + 0x118] ; 0x0069ca4f: cmp dword ptr [edi + 0x14], eax ; 0x0069ca52: jge 0x69ca57
  - 0x0069ca52: jge -> 0x0069ca57 (jcc_true) | ctx: 0x0069ca44: mov eax, dword ptr [0xf64d54] ; 0x0069ca49: mov eax, dword ptr [eax + 0x118] ; 0x0069ca4f: cmp dword ptr [edi + 0x14], eax ; 0x0069ca52: jge 0x69ca57
  - 0x0069ca52: jge -> 0x0069ca54 (jcc_false) | ctx: 0x0069ca44: mov eax, dword ptr [0xf64d54] ; 0x0069ca49: mov eax, dword ptr [eax + 0x118] ; 0x0069ca4f: cmp dword ptr [edi + 0x14], eax ; 0x0069ca52: jge 0x69ca57
  - 0x0069cadc: jmp -> 0x0069cbe5 (jmp) | ctx: 0x0069cad4: mov eax, dword ptr [edi + 0x1c] ; 0x0069cad7: push 1 ; 0x0069cad9: push dword ptr [eax + 0x30] ; 0x0069cadc: jmp 0x69cbe5
  - 0x0069cadc: jmp -> 0x0069cbe5 (jmp) | ctx: 0x0069cad4: mov eax, dword ptr [edi + 0x1c] ; 0x0069cad7: push 1 ; 0x0069cad9: push dword ptr [eax + 0x30] ; 0x0069cadc: jmp 0x69cbe5
  - 0x0069ca95: jmp -> 0x0069cbee (jmp) | ctx: 0x0069ca8c: push dword ptr [eax + 0x2c] ; 0x0069ca8f: or dword ptr [ebp - 4], 0xffffffff ; 0x0069ca93: mov ecx, esi ; 0x0069ca95: jmp 0x69cbee
  - 0x0069ca95: jmp -> 0x0069cbee (jmp) | ctx: 0x0069ca8c: push dword ptr [eax + 0x2c] ; 0x0069ca8f: or dword ptr [ebp - 4], 0xffffffff ; 0x0069ca93: mov ecx, esi ; 0x0069ca95: jmp 0x69cbee

### 0x0069ce69
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0069ce8f at 0x0069ce7d)
- branch points:
  - 0x0069ce6e: jne -> 0x0069ce7d (jcc_true) | ctx: 0x0069ce69: push edi ; 0x0069ce6a: mov edi, ecx ; 0x0069ce6c: test esi, esi ; 0x0069ce6e: jne 0x69ce7d
  - 0x0069ce6e: jne -> 0x0069ce70 (jcc_false) | ctx: 0x0069ce69: push edi ; 0x0069ce6a: mov edi, ecx ; 0x0069ce6c: test esi, esi ; 0x0069ce6e: jne 0x69ce7d

### 0x0069ce8f
- blocks=6, insns=52, edges=10, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerFleeBehavior@GGL@@ slot 1 (target 0x0069cf22, vtable 0x00be17a8)
  - rtti_vtable_method: .?AVCWorkerFleeBehavior@GGL@@ slot 3 (target 0x0069cf2a, vtable 0x00be17a8)
- branch points:
  - 0x0069ceaf: jle -> 0x0069ceb4 (jcc_true) | ctx: 0x0069cea1: mov ecx, dword ptr [eax + ecx*4] ; 0x0069cea4: mov eax, dword ptr [0xf78020] ; 0x0069cea9: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0069ceaf: jle 0x69ceb4
  - 0x0069ceaf: jle -> 0x0069ceb1 (jcc_false) | ctx: 0x0069cea1: mov ecx, dword ptr [eax + ecx*4] ; 0x0069cea4: mov eax, dword ptr [0xf78020] ; 0x0069cea9: cmp eax, dword ptr [ecx + 0x3adc] ; 0x0069ceaf: jle 0x69ceb4
  - 0x0069ceb1: jmp -> 0x0069cebd (jmp) | ctx: 0x0069ceb1: jmp 0x69cebd
  - 0x0069ced1: jne -> 0x0069ceb3 (jcc_true) | ctx: 0x0069cec4: call 0xab6ba9 ; 0x0069cec9: cmp dword ptr [0xf78020], -1 ; 0x0069ced0: pop ecx ; 0x0069ced1: jne 0x69ceb3
  - 0x0069ced1: jne -> 0x0069ced3 (jcc_false) | ctx: 0x0069cec4: call 0xab6ba9 ; 0x0069cec9: cmp dword ptr [0xf78020], -1 ; 0x0069ced0: pop ecx ; 0x0069ced1: jne 0x69ceb3
  - 0x0069cf20: jmp -> 0x0069ceb3 (jmp) | ctx: 0x0069cf1b: add esp, 0xc ; 0x0069cf1e: pop edi ; 0x0069cf1f: pop esi ; 0x0069cf20: jmp 0x69ceb3

### 0x0069d023
- blocks=1, insns=11, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCWorkerFleeBehaviorProps@GGL@@ slot 1 (target 0x0069d03a, vtable 0x00be177c)
  - rtti_vtable_method: .?AVCWorkerFleeBehavior@GGL@@ slot 4 (target 0x0069d023, vtable 0x00be17a8)
  - rtti_vtable_method: .?AVCWorkerFleeBehavior@GGL@@ slot 5 (target 0x0069d023, vtable 0x00be17a8)
- branch points:
  - none

### 0x0069ec2d
- blocks=3, insns=23, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x0062767a at 0x0069ec41)
- branch points:
  - 0x0069ec32: jne -> 0x0069ec41 (jcc_true) | ctx: 0x0069ec2d: push edi ; 0x0069ec2e: mov edi, ecx ; 0x0069ec30: test esi, esi ; 0x0069ec32: jne 0x69ec41
  - 0x0069ec32: jne -> 0x0069ec34 (jcc_false) | ctx: 0x0069ec2d: push edi ; 0x0069ec2e: mov edi, ecx ; 0x0069ec30: test esi, esi ; 0x0069ec32: jne 0x69ec41

### 0x0069fe5d
- blocks=3, insns=30, edges=5, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x0069feb9)
- branch points:
  - 0x0069fe78: je -> 0x0069fe89 (jcc_true) | ctx: 0x0069fe72: sub edi, eax ; 0x0069fe74: mov esi, edi ; 0x0069fe76: cmp edi, ebx ; 0x0069fe78: je 0x69fe89
  - 0x0069fe78: je -> 0x0069fe7a (jcc_false) | ctx: 0x0069fe72: sub edi, eax ; 0x0069fe74: mov esi, edi ; 0x0069fe76: cmp edi, ebx ; 0x0069fe78: je 0x69fe89
  - 0x0069fe87: jne -> 0x0069fe7a (jcc_true) | ctx: 0x0069fe80: call dword ptr [eax] ; 0x0069fe82: add esi, 0x1c ; 0x0069fe85: cmp esi, ebx ; 0x0069fe87: jne 0x69fe7a
  - 0x0069fe87: jne -> 0x0069fe89 (jcc_false) | ctx: 0x0069fe80: call dword ptr [eax] ; 0x0069fe82: add esi, 0x1c ; 0x0069fe85: cmp esi, ebx ; 0x0069fe87: jne 0x69fe7a

### 0x0069ff61
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0061e633 at 0x0069ff91)
- branch points:
  - 0x0069ff78: jae -> 0x0069ff9e (jcc_true) | ctx: 0x0069ff71: idiv ebx ; 0x0069ff73: mov edi, dword ptr [ebp + 8] ; 0x0069ff76: cmp eax, edi ; 0x0069ff78: jae 0x69ff9e
  - 0x0069ff78: jae -> 0x0069ff7a (jcc_false) | ctx: 0x0069ff71: idiv ebx ; 0x0069ff73: mov edi, dword ptr [ebp + 8] ; 0x0069ff76: cmp eax, edi ; 0x0069ff78: jae 0x69ff9e
  - 0x0069ff8a: jb -> 0x0069ffa5 (jcc_true) | ctx: 0x0069ff84: idiv ebx ; 0x0069ff86: sub ecx, eax ; 0x0069ff88: cmp ecx, edi ; 0x0069ff8a: jb 0x69ffa5
  - 0x0069ff8a: jb -> 0x0069ff8c (jcc_false) | ctx: 0x0069ff84: idiv ebx ; 0x0069ff86: sub ecx, eax ; 0x0069ff88: cmp ecx, edi ; 0x0069ff8a: jb 0x69ffa5

### 0x006a236e
- blocks=1, insns=14, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006a23aa)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006a245a)
- branch points:
  - none

### 0x006a36ec
- blocks=1, insns=6, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006a37a5)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006a3840)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006a38e9)
- branch points:
  - none

### 0x006a3a0a
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00611570 at 0x006a3a3a)
- branch points:
  - 0x006a3a21: jae -> 0x006a3a47 (jcc_true) | ctx: 0x006a3a1a: idiv ebx ; 0x006a3a1c: mov edi, dword ptr [ebp + 8] ; 0x006a3a1f: cmp eax, edi ; 0x006a3a21: jae 0x6a3a47
  - 0x006a3a21: jae -> 0x006a3a23 (jcc_false) | ctx: 0x006a3a1a: idiv ebx ; 0x006a3a1c: mov edi, dword ptr [ebp + 8] ; 0x006a3a1f: cmp eax, edi ; 0x006a3a21: jae 0x6a3a47
  - 0x006a3a33: jb -> 0x006a3a4e (jcc_true) | ctx: 0x006a3a2d: idiv ebx ; 0x006a3a2f: sub ecx, eax ; 0x006a3a31: cmp ecx, edi ; 0x006a3a33: jb 0x6a3a4e
  - 0x006a3a33: jb -> 0x006a3a35 (jcc_false) | ctx: 0x006a3a2d: idiv ebx ; 0x006a3a2f: sub ecx, eax ; 0x006a3a31: cmp ecx, edi ; 0x006a3a33: jb 0x6a3a4e

### 0x006a7435
- blocks=8, insns=30, edges=12, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006a743e)
- branch points:
  - 0x006a744b: jne -> 0x006a7453 (jcc_true) | ctx: 0x006a7443: mov ecx, dword ptr [ebp + 8] ; 0x006a7446: add esp, 0xc ; 0x006a7449: test ecx, ecx ; 0x006a744b: jne 0x6a7453
  - 0x006a744b: jne -> 0x006a744d (jcc_false) | ctx: 0x006a7443: mov ecx, dword ptr [ebp + 8] ; 0x006a7446: add esp, 0xc ; 0x006a7449: test ecx, ecx ; 0x006a744b: jne 0x6a7453
  - 0x006a7458: je -> 0x006a745c (jcc_true) | ctx: 0x006a7453: mov edx, dword ptr [ebp + 0xc] ; 0x006a7456: test eax, eax ; 0x006a7458: je 0x6a745c
  - 0x006a7458: je -> 0x006a745a (jcc_false) | ctx: 0x006a7453: mov edx, dword ptr [ebp + 0xc] ; 0x006a7456: test eax, eax ; 0x006a7458: je 0x6a745c
  - 0x006a7451: jmp -> 0x006a7456 (jmp) | ctx: 0x006a744d: mov ecx, eax ; 0x006a744f: mov edx, eax ; 0x006a7451: jmp 0x6a7456
  - 0x006a7461: je -> 0x006a7465 (jcc_true) | ctx: 0x006a745c: lea ecx, [eax + 4] ; 0x006a745f: test ecx, ecx ; 0x006a7461: je 0x6a7465
  - 0x006a7461: je -> 0x006a7463 (jcc_false) | ctx: 0x006a745c: lea ecx, [eax + 4] ; 0x006a745f: test ecx, ecx ; 0x006a7461: je 0x6a7465
  - 0x006a7461: je -> 0x006a7465 (jcc_true) | ctx: 0x006a745a: mov dword ptr [eax], ecx ; 0x006a745c: lea ecx, [eax + 4] ; 0x006a745f: test ecx, ecx ; 0x006a7461: je 0x6a7465
  - 0x006a7461: je -> 0x006a7463 (jcc_false) | ctx: 0x006a745a: mov dword ptr [eax], ecx ; 0x006a745c: lea ecx, [eax + 4] ; 0x006a745f: test ecx, ecx ; 0x006a7461: je 0x6a7465
  - 0x006a7458: je -> 0x006a745c (jcc_true) | ctx: 0x006a7456: test eax, eax ; 0x006a7458: je 0x6a745c
  - 0x006a7458: je -> 0x006a745a (jcc_false) | ctx: 0x006a7456: test eax, eax ; 0x006a7458: je 0x6a745c

### 0x006a76ec
- blocks=8, insns=30, edges=12, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006a76f5)
- branch points:
  - 0x006a7702: jne -> 0x006a770a (jcc_true) | ctx: 0x006a76fa: mov ecx, dword ptr [ebp + 8] ; 0x006a76fd: add esp, 0xc ; 0x006a7700: test ecx, ecx ; 0x006a7702: jne 0x6a770a
  - 0x006a7702: jne -> 0x006a7704 (jcc_false) | ctx: 0x006a76fa: mov ecx, dword ptr [ebp + 8] ; 0x006a76fd: add esp, 0xc ; 0x006a7700: test ecx, ecx ; 0x006a7702: jne 0x6a770a
  - 0x006a770f: je -> 0x006a7713 (jcc_true) | ctx: 0x006a770a: mov edx, dword ptr [ebp + 0xc] ; 0x006a770d: test eax, eax ; 0x006a770f: je 0x6a7713
  - 0x006a770f: je -> 0x006a7711 (jcc_false) | ctx: 0x006a770a: mov edx, dword ptr [ebp + 0xc] ; 0x006a770d: test eax, eax ; 0x006a770f: je 0x6a7713
  - 0x006a7708: jmp -> 0x006a770d (jmp) | ctx: 0x006a7704: mov ecx, eax ; 0x006a7706: mov edx, eax ; 0x006a7708: jmp 0x6a770d
  - 0x006a7718: je -> 0x006a771c (jcc_true) | ctx: 0x006a7713: lea ecx, [eax + 4] ; 0x006a7716: test ecx, ecx ; 0x006a7718: je 0x6a771c
  - 0x006a7718: je -> 0x006a771a (jcc_false) | ctx: 0x006a7713: lea ecx, [eax + 4] ; 0x006a7716: test ecx, ecx ; 0x006a7718: je 0x6a771c
  - 0x006a7718: je -> 0x006a771c (jcc_true) | ctx: 0x006a7711: mov dword ptr [eax], ecx ; 0x006a7713: lea ecx, [eax + 4] ; 0x006a7716: test ecx, ecx ; 0x006a7718: je 0x6a771c
  - 0x006a7718: je -> 0x006a771a (jcc_false) | ctx: 0x006a7711: mov dword ptr [eax], ecx ; 0x006a7713: lea ecx, [eax + 4] ; 0x006a7716: test ecx, ecx ; 0x006a7718: je 0x6a771c
  - 0x006a770f: je -> 0x006a7713 (jcc_true) | ctx: 0x006a770d: test eax, eax ; 0x006a770f: je 0x6a7713
  - 0x006a770f: je -> 0x006a7711 (jcc_false) | ctx: 0x006a770d: test eax, eax ; 0x006a770f: je 0x6a7713

### 0x006a930f
- blocks=6, insns=36, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006a9335)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006a9363)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006a9393)
- branch points:
  - 0x006a9322: jne -> 0x006a9328 (jcc_true) | ctx: 0x006a931a: mov dword ptr [esi + 4], eax ; 0x006a931d: mov dword ptr [esi + 8], eax ; 0x006a9320: test edi, edi ; 0x006a9322: jne 0x6a9328
  - 0x006a9322: jne -> 0x006a9324 (jcc_false) | ctx: 0x006a931a: mov dword ptr [esi + 4], eax ; 0x006a931d: mov dword ptr [esi + 8], eax ; 0x006a9320: test edi, edi ; 0x006a9322: jne 0x6a9328
  - 0x006a932e: ja -> 0x006a9352 (jcc_true) | ctx: 0x006a9328: cmp edi, 0xaaaaaaa ; 0x006a932e: ja 0x6a9352
  - 0x006a932e: ja -> 0x006a9330 (jcc_false) | ctx: 0x006a9328: cmp edi, 0xaaaaaaa ; 0x006a932e: ja 0x6a9352
  - 0x006a9326: jmp -> 0x006a934c (jmp) | ctx: 0x006a9324: xor al, al ; 0x006a9326: jmp 0x6a934c

### 0x006a9423
- blocks=1, insns=23, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006a9472)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006a9517)
- branch points:
  - none

### 0x006ad089
- blocks=3, insns=51, edges=5, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006ad098)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006ad103)
- branch points:
  - 0x006ad0b8: je -> 0x006ad0cf (jcc_true) | ctx: 0x006ad0b0: sub ebx, dword ptr [esi] ; 0x006ad0b2: sar ebx, 2 ; 0x006ad0b5: cmp dword ptr [esi], 0 ; 0x006ad0b8: je 0x6ad0cf
  - 0x006ad0b8: je -> 0x006ad0ba (jcc_false) | ctx: 0x006ad0b0: sub ebx, dword ptr [esi] ; 0x006ad0b2: sar ebx, 2 ; 0x006ad0b5: cmp dword ptr [esi], 0 ; 0x006ad0b8: je 0x6ad0cf

### 0x006b07f3
- blocks=1, insns=23, edges=0, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006b0845)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006b090a)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006b09cf)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006b0a94)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006b0b59)
- branch points:
  - none

### 0x006b0c01
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00611570 at 0x006b0c31)
- branch points:
  - 0x006b0c18: jae -> 0x006b0c3e (jcc_true) | ctx: 0x006b0c11: idiv ebx ; 0x006b0c13: mov edi, dword ptr [ebp + 8] ; 0x006b0c16: cmp eax, edi ; 0x006b0c18: jae 0x6b0c3e
  - 0x006b0c18: jae -> 0x006b0c1a (jcc_false) | ctx: 0x006b0c11: idiv ebx ; 0x006b0c13: mov edi, dword ptr [ebp + 8] ; 0x006b0c16: cmp eax, edi ; 0x006b0c18: jae 0x6b0c3e
  - 0x006b0c2a: jb -> 0x006b0c45 (jcc_true) | ctx: 0x006b0c24: idiv ebx ; 0x006b0c26: sub ecx, eax ; 0x006b0c28: cmp ecx, edi ; 0x006b0c2a: jb 0x6b0c45
  - 0x006b0c2a: jb -> 0x006b0c2c (jcc_false) | ctx: 0x006b0c24: idiv ebx ; 0x006b0c26: sub ecx, eax ; 0x006b0c28: cmp ecx, edi ; 0x006b0c2a: jb 0x6b0c45

### 0x006b0c54
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00611570 at 0x006b0c84)
- branch points:
  - 0x006b0c6b: jae -> 0x006b0c91 (jcc_true) | ctx: 0x006b0c64: idiv ebx ; 0x006b0c66: mov edi, dword ptr [ebp + 8] ; 0x006b0c69: cmp eax, edi ; 0x006b0c6b: jae 0x6b0c91
  - 0x006b0c6b: jae -> 0x006b0c6d (jcc_false) | ctx: 0x006b0c64: idiv ebx ; 0x006b0c66: mov edi, dword ptr [ebp + 8] ; 0x006b0c69: cmp eax, edi ; 0x006b0c6b: jae 0x6b0c91
  - 0x006b0c7d: jb -> 0x006b0c98 (jcc_true) | ctx: 0x006b0c77: idiv ebx ; 0x006b0c79: sub ecx, eax ; 0x006b0c7b: cmp ecx, edi ; 0x006b0c7d: jb 0x6b0c98
  - 0x006b0c7d: jb -> 0x006b0c7f (jcc_false) | ctx: 0x006b0c77: idiv ebx ; 0x006b0c79: sub ecx, eax ; 0x006b0c7b: cmp ecx, edi ; 0x006b0c7d: jb 0x6b0c98

### 0x006b0cfa
- blocks=5, insns=41, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00611570 at 0x006b0d2a)
- branch points:
  - 0x006b0d11: jae -> 0x006b0d37 (jcc_true) | ctx: 0x006b0d0a: idiv ebx ; 0x006b0d0c: mov edi, dword ptr [ebp + 8] ; 0x006b0d0f: cmp eax, edi ; 0x006b0d11: jae 0x6b0d37
  - 0x006b0d11: jae -> 0x006b0d13 (jcc_false) | ctx: 0x006b0d0a: idiv ebx ; 0x006b0d0c: mov edi, dword ptr [ebp + 8] ; 0x006b0d0f: cmp eax, edi ; 0x006b0d11: jae 0x6b0d37
  - 0x006b0d23: jb -> 0x006b0d3e (jcc_true) | ctx: 0x006b0d1d: idiv ebx ; 0x006b0d1f: sub ecx, eax ; 0x006b0d21: cmp ecx, edi ; 0x006b0d23: jb 0x6b0d3e
  - 0x006b0d23: jb -> 0x006b0d25 (jcc_false) | ctx: 0x006b0d1d: idiv ebx ; 0x006b0d1f: sub ecx, eax ; 0x006b0d21: cmp ecx, edi ; 0x006b0d23: jb 0x6b0d3e

### 0x006b7e86
- blocks=4, insns=44, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x00607853 at 0x006b7f14)
- branch points:
  - 0x006b7e99: jnp -> 0x006b7ef8 (jcc_true) | ctx: 0x006b7e8e: ucomiss xmm0, dword ptr [0xbc35d0] ; 0x006b7e95: lahf ; 0x006b7e96: test ah, 0x44 ; 0x006b7e99: jnp 0x6b7ef8
  - 0x006b7e99: jnp -> 0x006b7e9b (jcc_false) | ctx: 0x006b7e8e: ucomiss xmm0, dword ptr [0xbc35d0] ; 0x006b7e95: lahf ; 0x006b7e96: test ah, 0x44 ; 0x006b7e99: jnp 0x6b7ef8
  - 0x006b7ec6: jbe -> 0x006b7ef8 (jcc_true) | ctx: 0x006b7eba: call dword ptr [eax + 0x38] ; 0x006b7ebd: movss xmm0, dword ptr [ebp - 0x14] ; 0x006b7ec2: comiss xmm0, dword ptr [esi + 0x48] ; 0x006b7ec6: jbe 0x6b7ef8
  - 0x006b7ec6: jbe -> 0x006b7ec8 (jcc_false) | ctx: 0x006b7eba: call dword ptr [eax + 0x38] ; 0x006b7ebd: movss xmm0, dword ptr [ebp - 0x14] ; 0x006b7ec2: comiss xmm0, dword ptr [esi + 0x48] ; 0x006b7ec6: jbe 0x6b7ef8

### 0x006b9462
- blocks=3, insns=43, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0065bd8c at 0x006b947e)
- branch points:
  - 0x006b9485: je -> 0x006b94a1 (jcc_true) | ctx: 0x006b947d: push eax ; 0x006b947e: call 0x65bd89 ; 0x006b9483: test al, al ; 0x006b9485: je 0x6b94a1
  - 0x006b9485: je -> 0x006b9487 (jcc_false) | ctx: 0x006b947d: push eax ; 0x006b947e: call 0x65bd89 ; 0x006b9483: test al, al ; 0x006b9485: je 0x6b94a1

### 0x006baed6
- blocks=8, insns=30, edges=12, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006baedf)
- branch points:
  - 0x006baeec: jne -> 0x006baef4 (jcc_true) | ctx: 0x006baee4: mov ecx, dword ptr [ebp + 8] ; 0x006baee7: add esp, 0xc ; 0x006baeea: test ecx, ecx ; 0x006baeec: jne 0x6baef4
  - 0x006baeec: jne -> 0x006baeee (jcc_false) | ctx: 0x006baee4: mov ecx, dword ptr [ebp + 8] ; 0x006baee7: add esp, 0xc ; 0x006baeea: test ecx, ecx ; 0x006baeec: jne 0x6baef4
  - 0x006baef9: je -> 0x006baefd (jcc_true) | ctx: 0x006baef4: mov edx, dword ptr [ebp + 0xc] ; 0x006baef7: test eax, eax ; 0x006baef9: je 0x6baefd
  - 0x006baef9: je -> 0x006baefb (jcc_false) | ctx: 0x006baef4: mov edx, dword ptr [ebp + 0xc] ; 0x006baef7: test eax, eax ; 0x006baef9: je 0x6baefd
  - 0x006baef2: jmp -> 0x006baef7 (jmp) | ctx: 0x006baeee: mov ecx, eax ; 0x006baef0: mov edx, eax ; 0x006baef2: jmp 0x6baef7
  - 0x006baf02: je -> 0x006baf06 (jcc_true) | ctx: 0x006baefd: lea ecx, [eax + 4] ; 0x006baf00: test ecx, ecx ; 0x006baf02: je 0x6baf06
  - 0x006baf02: je -> 0x006baf04 (jcc_false) | ctx: 0x006baefd: lea ecx, [eax + 4] ; 0x006baf00: test ecx, ecx ; 0x006baf02: je 0x6baf06
  - 0x006baf02: je -> 0x006baf06 (jcc_true) | ctx: 0x006baefb: mov dword ptr [eax], ecx ; 0x006baefd: lea ecx, [eax + 4] ; 0x006baf00: test ecx, ecx ; 0x006baf02: je 0x6baf06
  - 0x006baf02: je -> 0x006baf04 (jcc_false) | ctx: 0x006baefb: mov dword ptr [eax], ecx ; 0x006baefd: lea ecx, [eax + 4] ; 0x006baf00: test ecx, ecx ; 0x006baf02: je 0x6baf06
  - 0x006baef9: je -> 0x006baefd (jcc_true) | ctx: 0x006baef7: test eax, eax ; 0x006baef9: je 0x6baefd
  - 0x006baef9: je -> 0x006baefb (jcc_false) | ctx: 0x006baef7: test eax, eax ; 0x006baef9: je 0x6baefd

### 0x006be0ac
- blocks=1, insns=20, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0057fd44 at 0x006be0bf)
- branch points:
  - none

### 0x006c11e4
- blocks=1, insns=69, edges=11, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005fd2e1 at 0x006c1204)
- branch points:
  - none

### 0x006c528d
- blocks=4, insns=84, edges=7, jcc=2, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006c54b7)
- branch points:
  - 0x006c52ad: jg -> 0x006c52b8 (jcc_true) | ctx: 0x006c529f: mov ecx, dword ptr [eax + ecx*4] ; 0x006c52a2: mov eax, dword ptr [0xf810f8] ; 0x006c52a7: cmp eax, dword ptr [ecx + 0x3adc] ; 0x006c52ad: jg 0x6c52b8
  - 0x006c52ad: jg -> 0x006c52af (jcc_false) | ctx: 0x006c529f: mov ecx, dword ptr [eax + ecx*4] ; 0x006c52a2: mov eax, dword ptr [0xf810f8] ; 0x006c52a7: cmp eax, dword ptr [ecx + 0x3adc] ; 0x006c52ad: jg 0x6c52b8
  - 0x006c52ca: jne -> 0x006c52af (jcc_true) | ctx: 0x006c52bd: call 0xab6ba9 ; 0x006c52c2: cmp dword ptr [0xf810f8], -1 ; 0x006c52c9: pop ecx ; 0x006c52ca: jne 0x6c52af
  - 0x006c52ca: jne -> 0x006c52cc (jcc_false) | ctx: 0x006c52bd: call 0xab6ba9 ; 0x006c52c2: cmp dword ptr [0xf810f8], -1 ; 0x006c52c9: pop ecx ; 0x006c52ca: jne 0x6c52af
  - 0x006c539f: jmp -> 0x006c52af (jmp) | ctx: 0x006c539c: pop edi ; 0x006c539d: pop esi ; 0x006c539e: pop ebx ; 0x006c539f: jmp 0x6c52af

### 0x006c5a1f
- blocks=8, insns=128, edges=35, jcc=6, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006c5b7f)
- branch points:
  - 0x006c5a63: jmp -> 0x006c5b32 (jmp) | ctx: 0x006c5a5a: mov byte ptr [ebp - 4], 1 ; 0x006c5a5e: mov edi, dword ptr [ebx] ; 0x006c5a60: mov dword ptr [ebp - 0x14], edi ; 0x006c5a63: jmp 0x6c5b32
  - 0x006c5b34: jne -> 0x006c5a68 (jcc_true) | ctx: 0x006c5b32: cmp edi, ebx ; 0x006c5b34: jne 0x6c5a68
  - 0x006c5b34: jne -> 0x006c5b3a (jcc_false) | ctx: 0x006c5b32: cmp edi, ebx ; 0x006c5b34: jne 0x6c5a68
  - 0x006c5ae9: jb -> 0x006c5aed (jcc_true) | ctx: 0x006c5add: call 0x505960 ; 0x006c5ae2: add edi, 0x10 ; 0x006c5ae5: cmp dword ptr [edi + 0x14], 0x10 ; 0x006c5ae9: jb 0x6c5aed
  - 0x006c5ae9: jb -> 0x006c5aeb (jcc_false) | ctx: 0x006c5add: call 0x505960 ; 0x006c5ae2: add edi, 0x10 ; 0x006c5ae5: cmp dword ptr [edi + 0x14], 0x10 ; 0x006c5ae9: jb 0x6c5aed
  - 0x006c5b17: jne -> 0x006c5b27 (jcc_true) | ctx: 0x006c5b0f: push eax ; 0x006c5b10: call 0x6c53a4 ; 0x006c5b15: test al, al ; 0x006c5b17: jne 0x6c5b27
  - 0x006c5b17: jne -> 0x006c5b19 (jcc_false) | ctx: 0x006c5b0f: push eax ; 0x006c5b10: call 0x6c53a4 ; 0x006c5b15: test al, al ; 0x006c5b17: jne 0x6c5b27
  - 0x006c5b17: jne -> 0x006c5b27 (jcc_true) | ctx: 0x006c5b0f: push eax ; 0x006c5b10: call 0x6c53a4 ; 0x006c5b15: test al, al ; 0x006c5b17: jne 0x6c5b27
  - 0x006c5b17: jne -> 0x006c5b19 (jcc_false) | ctx: 0x006c5b0f: push eax ; 0x006c5b10: call 0x6c53a4 ; 0x006c5b15: test al, al ; 0x006c5b17: jne 0x6c5b27
  - 0x006c5b34: jne -> 0x006c5a68 (jcc_true) | ctx: 0x006c5b2a: call 0x577cf5 ; 0x006c5b2f: mov edi, dword ptr [ebp - 0x14] ; 0x006c5b32: cmp edi, ebx ; 0x006c5b34: jne 0x6c5a68
  - 0x006c5b34: jne -> 0x006c5b3a (jcc_false) | ctx: 0x006c5b2a: call 0x577cf5 ; 0x006c5b2f: mov edi, dword ptr [ebp - 0x14] ; 0x006c5b32: cmp edi, ebx ; 0x006c5b34: jne 0x6c5a68
  - 0x006c5b34: jne -> 0x006c5a68 (jcc_true) | ctx: 0x006c5b2a: call 0x577cf5 ; 0x006c5b2f: mov edi, dword ptr [ebp - 0x14] ; 0x006c5b32: cmp edi, ebx ; 0x006c5b34: jne 0x6c5a68
  - 0x006c5b34: jne -> 0x006c5b3a (jcc_false) | ctx: 0x006c5b2a: call 0x577cf5 ; 0x006c5b2f: mov edi, dword ptr [ebp - 0x14] ; 0x006c5b32: cmp edi, ebx ; 0x006c5b34: jne 0x6c5a68

### 0x006c698f
- blocks=6, insns=127, edges=28, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006c6c9b)
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006c6ccb)
- branch points:
  - 0x006c69d2: jb -> 0x006c69d8 (jcc_true) | ctx: 0x006c69c6: call 0x505960 ; 0x006c69cb: add edi, 0x30 ; 0x006c69ce: cmp dword ptr [edi + 0x14], 0x10 ; 0x006c69d2: jb 0x6c69d8
  - 0x006c69d2: jb -> 0x006c69d4 (jcc_false) | ctx: 0x006c69c6: call 0x505960 ; 0x006c69cb: add edi, 0x30 ; 0x006c69ce: cmp dword ptr [edi + 0x14], 0x10 ; 0x006c69d2: jb 0x6c69d8
  - 0x006c6a25: jb -> 0x006c6a29 (jcc_true) | ctx: 0x006c6a19: lea ecx, [ebp - 0x24] ; 0x006c6a1c: call 0x505960 ; 0x006c6a21: cmp dword ptr [edi + 0x14], 0x10 ; 0x006c6a25: jb 0x6c6a29
  - 0x006c6a25: jb -> 0x006c6a27 (jcc_false) | ctx: 0x006c6a19: lea ecx, [ebp - 0x24] ; 0x006c6a1c: call 0x505960 ; 0x006c6a21: cmp dword ptr [edi + 0x14], 0x10 ; 0x006c6a25: jb 0x6c6a29
  - 0x006c69d6: jmp -> 0x006c69da (jmp) | ctx: 0x006c69d4: mov ecx, dword ptr [edi] ; 0x006c69d6: jmp 0x6c69da
  - 0x006c6a25: jb -> 0x006c6a29 (jcc_true) | ctx: 0x006c6a19: lea ecx, [ebp - 0x24] ; 0x006c6a1c: call 0x505960 ; 0x006c6a21: cmp dword ptr [edi + 0x14], 0x10 ; 0x006c6a25: jb 0x6c6a29
  - 0x006c6a25: jb -> 0x006c6a27 (jcc_false) | ctx: 0x006c6a19: lea ecx, [ebp - 0x24] ; 0x006c6a1c: call 0x505960 ; 0x006c6a21: cmp dword ptr [edi + 0x14], 0x10 ; 0x006c6a25: jb 0x6c6a29

### 0x006c7bef
- blocks=9, insns=61, edges=15, jcc=6, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x006c8050)
- branch points:
  - 0x006c7c0c: je -> 0x006c7c3c (jcc_true) | ctx: 0x006c7c05: idiv ecx ; 0x006c7c07: mov dword ptr [ebp - 4], eax ; 0x006c7c0a: test eax, eax ; 0x006c7c0c: je 0x6c7c3c
  - 0x006c7c0c: je -> 0x006c7c0e (jcc_false) | ctx: 0x006c7c05: idiv ecx ; 0x006c7c07: mov dword ptr [ebp - 4], eax ; 0x006c7c0a: test eax, eax ; 0x006c7c0c: je 0x6c7c3c
  - 0x006c7c1d: jb -> 0x006c7c21 (jcc_true) | ctx: 0x006c7c12: add eax, 0xb4 ; 0x006c7c17: add eax, edi ; 0x006c7c19: cmp dword ptr [eax + 0x14], 0x10 ; 0x006c7c1d: jb 0x6c7c21
  - 0x006c7c1d: jb -> 0x006c7c1f (jcc_false) | ctx: 0x006c7c12: add eax, 0xb4 ; 0x006c7c17: add eax, edi ; 0x006c7c19: cmp dword ptr [eax + 0x14], 0x10 ; 0x006c7c1d: jb 0x6c7c21
  - 0x006c7c2e: je -> 0x006c7c48 (jcc_true) | ctx: 0x006c7c2a: pop ecx ; 0x006c7c2b: pop ecx ; 0x006c7c2c: test eax, eax ; 0x006c7c2e: je 0x6c7c48
  - 0x006c7c2e: je -> 0x006c7c30 (jcc_false) | ctx: 0x006c7c2a: pop ecx ; 0x006c7c2b: pop ecx ; 0x006c7c2c: test eax, eax ; 0x006c7c2e: je 0x6c7c48
  - 0x006c7c2e: je -> 0x006c7c48 (jcc_true) | ctx: 0x006c7c2a: pop ecx ; 0x006c7c2b: pop ecx ; 0x006c7c2c: test eax, eax ; 0x006c7c2e: je 0x6c7c48
  - 0x006c7c2e: je -> 0x006c7c30 (jcc_false) | ctx: 0x006c7c2a: pop ecx ; 0x006c7c2b: pop ecx ; 0x006c7c2c: test eax, eax ; 0x006c7c2e: je 0x6c7c48
  - 0x006c7c4a: jmp -> 0x006c7c3f (jmp) | ctx: 0x006c7c48: mov eax, esi ; 0x006c7c4a: jmp 0x6c7c3f
  - 0x006c7c3a: jb -> 0x006c7c10 (jcc_true) | ctx: 0x006c7c30: inc esi ; 0x006c7c31: add edi, 0xe4 ; 0x006c7c37: cmp esi, dword ptr [ebp - 4] ; 0x006c7c3a: jb 0x6c7c10
  - 0x006c7c3a: jb -> 0x006c7c3c (jcc_false) | ctx: 0x006c7c30: inc esi ; 0x006c7c31: add edi, 0xe4 ; 0x006c7c37: cmp esi, dword ptr [ebp - 4] ; 0x006c7c3a: jb 0x6c7c10
  - 0x006c7c1d: jb -> 0x006c7c21 (jcc_true) | ctx: 0x006c7c12: add eax, 0xb4 ; 0x006c7c17: add eax, edi ; 0x006c7c19: cmp dword ptr [eax + 0x14], 0x10 ; 0x006c7c1d: jb 0x6c7c21
  - 0x006c7c1d: jb -> 0x006c7c1f (jcc_false) | ctx: 0x006c7c12: add eax, 0xb4 ; 0x006c7c17: add eax, edi ; 0x006c7c19: cmp dword ptr [eax + 0x14], 0x10 ; 0x006c7c1d: jb 0x6c7c21

### 0x007dcf10
- blocks=11, insns=177, edges=26, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x007dd033)
- branch points:
  - 0x007dcf4f: jne -> 0x007dcfc4 (jcc_true) | ctx: 0x007dcf44: mov dword ptr [ebp - 0x10], 0 ; 0x007dcf4b: push eax ; 0x007dcf4c: lea ecx, [ecx + 0x40] ; 0x007dcf4f: jne 0x7dcfc4
  - 0x007dcf4f: jne -> 0x007dcf51 (jcc_false) | ctx: 0x007dcf44: mov dword ptr [ebp - 0x10], 0 ; 0x007dcf4b: push eax ; 0x007dcf4c: lea ecx, [ecx + 0x40] ; 0x007dcf4f: jne 0x7dcfc4
  - 0x007dcfdb: je -> 0x007dcfe4 (jcc_true) | ctx: 0x007dcfcf: mov dword ptr [ebp - 0x10], ecx ; 0x007dcfd2: mov dword ptr [ebp - 4], 1 ; 0x007dcfd9: test ecx, ecx ; 0x007dcfdb: je 0x7dcfe4
  - 0x007dcfdb: je -> 0x007dcfdd (jcc_false) | ctx: 0x007dcfcf: mov dword ptr [ebp - 0x10], ecx ; 0x007dcfd2: mov dword ptr [ebp - 4], 1 ; 0x007dcfd9: test ecx, ecx ; 0x007dcfdb: je 0x7dcfe4
  - 0x007dcf68: je -> 0x007dcf71 (jcc_true) | ctx: 0x007dcf5c: mov dword ptr [ebp - 0x14], ecx ; 0x007dcf5f: mov dword ptr [ebp - 4], 0 ; 0x007dcf66: test ecx, ecx ; 0x007dcf68: je 0x7dcf71
  - 0x007dcf68: je -> 0x007dcf6a (jcc_false) | ctx: 0x007dcf5c: mov dword ptr [ebp - 0x14], ecx ; 0x007dcf5f: mov dword ptr [ebp - 4], 0 ; 0x007dcf66: test ecx, ecx ; 0x007dcf68: je 0x7dcf71
  - 0x007dd02c: je -> 0x007dd038 (jcc_true) | ctx: 0x007dd024: lea ecx, [esi + 0x34] ; 0x007dd027: lea eax, [ebx + 0x34] ; 0x007dd02a: cmp ecx, eax ; 0x007dd02c: je 0x7dd038
  - 0x007dd02c: je -> 0x007dd02e (jcc_false) | ctx: 0x007dd024: lea ecx, [esi + 0x34] ; 0x007dd027: lea eax, [ebx + 0x34] ; 0x007dd02a: cmp ecx, eax ; 0x007dd02c: je 0x7dd038
  - 0x007dcfe2: jmp -> 0x007dcfe6 (jmp) | ctx: 0x007dcfdd: call 0x7d4ca0 ; 0x007dcfe2: jmp 0x7dcfe6
  - 0x007dcf6f: jmp -> 0x007dcf73 (jmp) | ctx: 0x007dcf6a: call 0x7d4ca0 ; 0x007dcf6f: jmp 0x7dcf73
  - 0x007dd02c: je -> 0x007dd038 (jcc_true) | ctx: 0x007dd024: lea ecx, [esi + 0x34] ; 0x007dd027: lea eax, [ebx + 0x34] ; 0x007dd02a: cmp ecx, eax ; 0x007dd02c: je 0x7dd038
  - 0x007dd02c: je -> 0x007dd02e (jcc_false) | ctx: 0x007dd024: lea ecx, [esi + 0x34] ; 0x007dd027: lea eax, [ebx + 0x34] ; 0x007dd02a: cmp ecx, eax ; 0x007dd02c: je 0x7dd038

### 0x007de650
- blocks=15, insns=178, edges=34, jcc=10, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x007de7a2)
- branch points:
  - 0x007de694: je -> 0x007de71e (jcc_true) | ctx: 0x007de68c: mov dword ptr [ebp - 0x10], esi ; 0x007de68f: mov dword ptr [ebp - 0x10], esi ; 0x007de692: test esi, esi ; 0x007de694: je 0x7de71e
  - 0x007de694: je -> 0x007de69a (jcc_false) | ctx: 0x007de68c: mov dword ptr [ebp - 0x10], esi ; 0x007de68f: mov dword ptr [ebp - 0x10], esi ; 0x007de692: test esi, esi ; 0x007de694: je 0x7de71e
  - 0x007de749: jne -> 0x007de74f (jcc_true) | ctx: 0x007de73b: mov dword ptr [ebp - 0x18], 0 ; 0x007de742: mov byte ptr [ebp - 0x28], 0 ; 0x007de746: cmp byte ptr [edx], 0 ; 0x007de749: jne 0x7de74f
  - 0x007de749: jne -> 0x007de74b (jcc_false) | ctx: 0x007de73b: mov dword ptr [ebp - 0x18], 0 ; 0x007de742: mov byte ptr [ebp - 0x28], 0 ; 0x007de746: cmp byte ptr [edx], 0 ; 0x007de749: jne 0x7de74f
  - 0x007de6e4: jb -> 0x007de6e8 (jcc_true) | ctx: 0x007de6d2: mov dword ptr [eax + 0x14], 0xf ; 0x007de6d9: mov dword ptr [eax + 0x10], 0 ; 0x007de6e0: cmp dword ptr [eax + 0x14], 0x10 ; 0x007de6e4: jb 0x7de6e8
  - 0x007de6e4: jb -> 0x007de6e6 (jcc_false) | ctx: 0x007de6d2: mov dword ptr [eax + 0x14], 0xf ; 0x007de6d9: mov dword ptr [eax + 0x10], 0 ; 0x007de6e0: cmp dword ptr [eax + 0x14], 0x10 ; 0x007de6e4: jb 0x7de6e8
  - 0x007de759: jne -> 0x007de754 (jcc_true) | ctx: 0x007de754: mov al, byte ptr [ecx] ; 0x007de756: inc ecx ; 0x007de757: test al, al ; 0x007de759: jne 0x7de754
  - 0x007de759: jne -> 0x007de75b (jcc_false) | ctx: 0x007de754: mov al, byte ptr [ecx] ; 0x007de756: inc ecx ; 0x007de757: test al, al ; 0x007de759: jne 0x7de754
  - 0x007de74d: jmp -> 0x007de75d (jmp) | ctx: 0x007de74b: xor ecx, ecx ; 0x007de74d: jmp 0x7de75d
  - 0x007de71c: jmp -> 0x007de720 (jmp) | ctx: 0x007de707: mov dword ptr [esi + 0x50], 0 ; 0x007de70e: mov dword ptr [esi + 0x54], 0 ; 0x007de715: mov dword ptr [esi + 0x58], 0 ; 0x007de71c: jmp 0x7de720
  - 0x007de71c: jmp -> 0x007de720 (jmp) | ctx: 0x007de707: mov dword ptr [esi + 0x50], 0 ; 0x007de70e: mov dword ptr [esi + 0x54], 0 ; 0x007de715: mov dword ptr [esi + 0x58], 0 ; 0x007de71c: jmp 0x7de720
  - 0x007de759: jne -> 0x007de754 (jcc_true) | ctx: 0x007de754: mov al, byte ptr [ecx] ; 0x007de756: inc ecx ; 0x007de757: test al, al ; 0x007de759: jne 0x7de754
  - 0x007de759: jne -> 0x007de75b (jcc_false) | ctx: 0x007de754: mov al, byte ptr [ecx] ; 0x007de756: inc ecx ; 0x007de757: test al, al ; 0x007de759: jne 0x7de754
  - 0x007de79b: je -> 0x007de7a7 (jcc_true) | ctx: 0x007de78f: mov dword ptr [ebp - 4], 2 ; 0x007de796: mov dword ptr [esi + 0x20], edi ; 0x007de799: cmp ecx, eax ; 0x007de79b: je 0x7de7a7
  - 0x007de79b: je -> 0x007de79d (jcc_false) | ctx: 0x007de78f: mov dword ptr [ebp - 4], 2 ; 0x007de796: mov dword ptr [esi + 0x20], edi ; 0x007de799: cmp ecx, eax ; 0x007de79b: je 0x7de7a7
  - 0x007de79b: je -> 0x007de7a7 (jcc_true) | ctx: 0x007de78f: mov dword ptr [ebp - 4], 2 ; 0x007de796: mov dword ptr [esi + 0x20], edi ; 0x007de799: cmp ecx, eax ; 0x007de79b: je 0x7de7a7
  - 0x007de79b: je -> 0x007de79d (jcc_false) | ctx: 0x007de78f: mov dword ptr [ebp - 4], 2 ; 0x007de796: mov dword ptr [esi + 0x20], edi ; 0x007de799: cmp ecx, eax ; 0x007de79b: je 0x7de7a7
  - 0x007de749: jne -> 0x007de74f (jcc_true) | ctx: 0x007de73b: mov dword ptr [ebp - 0x18], 0 ; 0x007de742: mov byte ptr [ebp - 0x28], 0 ; 0x007de746: cmp byte ptr [edx], 0 ; 0x007de749: jne 0x7de74f
  - 0x007de749: jne -> 0x007de74b (jcc_false) | ctx: 0x007de73b: mov dword ptr [ebp - 0x18], 0 ; 0x007de742: mov byte ptr [ebp - 0x28], 0 ; 0x007de746: cmp byte ptr [edx], 0 ; 0x007de749: jne 0x7de74f
  - 0x007de7d0: jb -> 0x007de7dd (jcc_true) | ctx: 0x007de7c0: call 0x7d8450 ; 0x007de7c5: cmp dword ptr [ebp - 0x14], 0x10 ; 0x007de7c9: mov dword ptr [ebp - 4], 3 ; 0x007de7d0: jb 0x7de7dd
  - 0x007de7d0: jb -> 0x007de7d2 (jcc_false) | ctx: 0x007de7c0: call 0x7d8450 ; 0x007de7c5: cmp dword ptr [ebp - 0x14], 0x10 ; 0x007de7c9: mov dword ptr [ebp - 4], 3 ; 0x007de7d0: jb 0x7de7dd
  - 0x007de7d0: jb -> 0x007de7dd (jcc_true) | ctx: 0x007de7c0: call 0x7d8450 ; 0x007de7c5: cmp dword ptr [ebp - 0x14], 0x10 ; 0x007de7c9: mov dword ptr [ebp - 4], 3 ; 0x007de7d0: jb 0x7de7dd
  - 0x007de7d0: jb -> 0x007de7d2 (jcc_false) | ctx: 0x007de7c0: call 0x7d8450 ; 0x007de7c5: cmp dword ptr [ebp - 0x14], 0x10 ; 0x007de7c9: mov dword ptr [ebp - 4], 3 ; 0x007de7d0: jb 0x7de7dd

### 0x007e03bc
- blocks=11, insns=318, edges=34, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x007e0679)
- branch points:
  - 0x007e03ea: jne -> 0x007e056b (jcc_true) | ctx: 0x007e03dc: mov dword ptr [ebp - 0x14], 0 ; 0x007e03e3: push eax ; 0x007e03e4: lea ecx, [ecx + 0x80] ; 0x007e03ea: jne 0x7e056b
  - 0x007e03ea: jne -> 0x007e03f0 (jcc_false) | ctx: 0x007e03dc: mov dword ptr [ebp - 0x14], 0 ; 0x007e03e3: push eax ; 0x007e03e4: lea ecx, [ecx + 0x80] ; 0x007e03ea: jne 0x7e056b
  - 0x007e0582: je -> 0x007e0618 (jcc_true) | ctx: 0x007e0576: mov dword ptr [ebp - 0x24], ebx ; 0x007e0579: mov dword ptr [ebp - 4], 2 ; 0x007e0580: test ebx, ebx ; 0x007e0582: je 0x7e0618
  - 0x007e0582: je -> 0x007e0588 (jcc_false) | ctx: 0x007e0576: mov dword ptr [ebp - 0x24], ebx ; 0x007e0579: mov dword ptr [ebp - 4], 2 ; 0x007e0580: test ebx, ebx ; 0x007e0582: je 0x7e0618
  - 0x007e040a: je -> 0x007e049d (jcc_true) | ctx: 0x007e03fe: mov dword ptr [ebp - 0x24], ebx ; 0x007e0401: mov dword ptr [ebp - 4], 0 ; 0x007e0408: test ebx, ebx ; 0x007e040a: je 0x7e049d
  - 0x007e040a: je -> 0x007e0410 (jcc_false) | ctx: 0x007e03fe: mov dword ptr [ebp - 0x24], ebx ; 0x007e0401: mov dword ptr [ebp - 4], 0 ; 0x007e0408: test ebx, ebx ; 0x007e040a: je 0x7e049d
  - 0x007e0672: je -> 0x007e067e (jcc_true) | ctx: 0x007e0667: lea ecx, [ebx + 0x98] ; 0x007e066d: mov dword ptr [ebx + 0x30], edi ; 0x007e0670: cmp ecx, eax ; 0x007e0672: je 0x7e067e
  - 0x007e0672: je -> 0x007e0674 (jcc_false) | ctx: 0x007e0667: lea ecx, [ebx + 0x98] ; 0x007e066d: mov dword ptr [ebx + 0x30], edi ; 0x007e0670: cmp ecx, eax ; 0x007e0672: je 0x7e067e
  - 0x007e0616: jmp -> 0x007e061a (jmp) | ctx: 0x007e05fe: mov dword ptr [ebx + 0x3c], 0 ; 0x007e0605: mov dword ptr [ebx + 0x44], 0 ; 0x007e060c: mov dword ptr [ebx + 0x88], 0 ; 0x007e0616: jmp 0x7e061a
  - 0x007e049b: jmp -> 0x007e04a2 (jmp) | ctx: 0x007e0483: mov dword ptr [ebx + 0x3c], 0 ; 0x007e048a: mov dword ptr [ebx + 0x44], 0 ; 0x007e0491: mov dword ptr [ebx + 0x88], 0 ; 0x007e049b: jmp 0x7e04a2
  - 0x007e0672: je -> 0x007e067e (jcc_true) | ctx: 0x007e0667: lea ecx, [ebx + 0x98] ; 0x007e066d: mov dword ptr [ebx + 0x30], edi ; 0x007e0670: cmp ecx, eax ; 0x007e0672: je 0x7e067e
  - 0x007e0672: je -> 0x007e0674 (jcc_false) | ctx: 0x007e0667: lea ecx, [ebx + 0x98] ; 0x007e066d: mov dword ptr [ebx + 0x30], edi ; 0x007e0670: cmp ecx, eax ; 0x007e0672: je 0x7e067e

### 0x007e1f00
- blocks=15, insns=167, edges=30, jcc=10, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x007e203d)
- branch points:
  - 0x007e1f47: je -> 0x007e1fae (jcc_true) | ctx: 0x007e1f3f: mov dword ptr [ebp - 0x10], esi ; 0x007e1f42: mov dword ptr [ebp - 0x10], esi ; 0x007e1f45: test esi, esi ; 0x007e1f47: je 0x7e1fae
  - 0x007e1f47: je -> 0x007e1f49 (jcc_false) | ctx: 0x007e1f3f: mov dword ptr [ebp - 0x10], esi ; 0x007e1f42: mov dword ptr [ebp - 0x10], esi ; 0x007e1f45: test esi, esi ; 0x007e1f47: je 0x7e1fae
  - 0x007e1fd9: jne -> 0x007e1fdf (jcc_true) | ctx: 0x007e1fcb: mov dword ptr [ebp - 0x1c], 0 ; 0x007e1fd2: mov byte ptr [ebp - 0x2c], 0 ; 0x007e1fd6: cmp byte ptr [edx], 0 ; 0x007e1fd9: jne 0x7e1fdf
  - 0x007e1fd9: jne -> 0x007e1fdb (jcc_false) | ctx: 0x007e1fcb: mov dword ptr [ebp - 0x1c], 0 ; 0x007e1fd2: mov byte ptr [ebp - 0x2c], 0 ; 0x007e1fd6: cmp byte ptr [edx], 0 ; 0x007e1fd9: jne 0x7e1fdf
  - 0x007e1f9e: jb -> 0x007e1fa2 (jcc_true) | ctx: 0x007e1f8c: mov dword ptr [eax + 0x14], 0xf ; 0x007e1f93: mov dword ptr [eax + 0x10], 0 ; 0x007e1f9a: cmp dword ptr [eax + 0x14], 0x10 ; 0x007e1f9e: jb 0x7e1fa2
  - 0x007e1f9e: jb -> 0x007e1fa0 (jcc_false) | ctx: 0x007e1f8c: mov dword ptr [eax + 0x14], 0xf ; 0x007e1f93: mov dword ptr [eax + 0x10], 0 ; 0x007e1f9a: cmp dword ptr [eax + 0x14], 0x10 ; 0x007e1f9e: jb 0x7e1fa2
  - 0x007e1fe9: jne -> 0x007e1fe4 (jcc_true) | ctx: 0x007e1fe4: mov al, byte ptr [ecx] ; 0x007e1fe6: inc ecx ; 0x007e1fe7: test al, al ; 0x007e1fe9: jne 0x7e1fe4
  - 0x007e1fe9: jne -> 0x007e1feb (jcc_false) | ctx: 0x007e1fe4: mov al, byte ptr [ecx] ; 0x007e1fe6: inc ecx ; 0x007e1fe7: test al, al ; 0x007e1fe9: jne 0x7e1fe4
  - 0x007e1fdd: jmp -> 0x007e1fed (jmp) | ctx: 0x007e1fdb: xor ecx, ecx ; 0x007e1fdd: jmp 0x7e1fed
  - 0x007e1fac: jmp -> 0x007e1fb0 (jmp) | ctx: 0x007e1fa2: mov byte ptr [eax], 0 ; 0x007e1fa5: mov dword ptr [esi + 0x48], 0xffffffff ; 0x007e1fac: jmp 0x7e1fb0
  - 0x007e1fac: jmp -> 0x007e1fb0 (jmp) | ctx: 0x007e1fa0: mov eax, dword ptr [eax] ; 0x007e1fa2: mov byte ptr [eax], 0 ; 0x007e1fa5: mov dword ptr [esi + 0x48], 0xffffffff ; 0x007e1fac: jmp 0x7e1fb0
  - 0x007e1fe9: jne -> 0x007e1fe4 (jcc_true) | ctx: 0x007e1fe4: mov al, byte ptr [ecx] ; 0x007e1fe6: inc ecx ; 0x007e1fe7: test al, al ; 0x007e1fe9: jne 0x7e1fe4
  - 0x007e1fe9: jne -> 0x007e1feb (jcc_false) | ctx: 0x007e1fe4: mov al, byte ptr [ecx] ; 0x007e1fe6: inc ecx ; 0x007e1fe7: test al, al ; 0x007e1fe9: jne 0x7e1fe4
  - 0x007e2036: je -> 0x007e2042 (jcc_true) | ctx: 0x007e202e: lea eax, [ebp - 0x2c] ; 0x007e2031: mov byte ptr [esi + 0x2c], bl ; 0x007e2034: cmp ecx, eax ; 0x007e2036: je 0x7e2042
  - 0x007e2036: je -> 0x007e2038 (jcc_false) | ctx: 0x007e202e: lea eax, [ebp - 0x2c] ; 0x007e2031: mov byte ptr [esi + 0x2c], bl ; 0x007e2034: cmp ecx, eax ; 0x007e2036: je 0x7e2042
  - 0x007e2036: je -> 0x007e2042 (jcc_true) | ctx: 0x007e202e: lea eax, [ebp - 0x2c] ; 0x007e2031: mov byte ptr [esi + 0x2c], bl ; 0x007e2034: cmp ecx, eax ; 0x007e2036: je 0x7e2042
  - 0x007e2036: je -> 0x007e2038 (jcc_false) | ctx: 0x007e202e: lea eax, [ebp - 0x2c] ; 0x007e2031: mov byte ptr [esi + 0x2c], bl ; 0x007e2034: cmp ecx, eax ; 0x007e2036: je 0x7e2042
  - 0x007e1fd9: jne -> 0x007e1fdf (jcc_true) | ctx: 0x007e1fcb: mov dword ptr [ebp - 0x1c], 0 ; 0x007e1fd2: mov byte ptr [ebp - 0x2c], 0 ; 0x007e1fd6: cmp byte ptr [edx], 0 ; 0x007e1fd9: jne 0x7e1fdf
  - 0x007e1fd9: jne -> 0x007e1fdb (jcc_false) | ctx: 0x007e1fcb: mov dword ptr [ebp - 0x1c], 0 ; 0x007e1fd2: mov byte ptr [ebp - 0x2c], 0 ; 0x007e1fd6: cmp byte ptr [edx], 0 ; 0x007e1fd9: jne 0x7e1fdf
  - 0x007e2053: jb -> 0x007e2060 (jcc_true) | ctx: 0x007e2045: mov dword ptr [esi + 0x48], eax ; 0x007e2048: cmp dword ptr [ebp - 0x18], 0x10 ; 0x007e204c: mov dword ptr [ebp - 4], 3 ; 0x007e2053: jb 0x7e2060
  - 0x007e2053: jb -> 0x007e2055 (jcc_false) | ctx: 0x007e2045: mov dword ptr [esi + 0x48], eax ; 0x007e2048: cmp dword ptr [ebp - 0x18], 0x10 ; 0x007e204c: mov dword ptr [ebp - 4], 3 ; 0x007e2053: jb 0x7e2060
  - 0x007e2053: jb -> 0x007e2060 (jcc_true) | ctx: 0x007e2045: mov dword ptr [esi + 0x48], eax ; 0x007e2048: cmp dword ptr [ebp - 0x18], 0x10 ; 0x007e204c: mov dword ptr [ebp - 4], 3 ; 0x007e2053: jb 0x7e2060
  - 0x007e2053: jb -> 0x007e2055 (jcc_false) | ctx: 0x007e2045: mov dword ptr [esi + 0x48], eax ; 0x007e2048: cmp dword ptr [ebp - 0x18], 0x10 ; 0x007e204c: mov dword ptr [ebp - 4], 3 ; 0x007e2053: jb 0x7e2060

### 0x007eb060
- blocks=3, insns=37, edges=5, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x007eb09d)
- branch points:
  - 0x007eb096: je -> 0x007eb0a2 (jcc_true) | ctx: 0x007eb08e: lea ecx, [esi + 0x34] ; 0x007eb091: mov eax, dword ptr [ebp + 0x1c] ; 0x007eb094: cmp ecx, eax ; 0x007eb096: je 0x7eb0a2
  - 0x007eb096: je -> 0x007eb098 (jcc_false) | ctx: 0x007eb08e: lea ecx, [esi + 0x34] ; 0x007eb091: mov eax, dword ptr [ebp + 0x1c] ; 0x007eb094: cmp ecx, eax ; 0x007eb096: je 0x7eb0a2

### 0x007eb5e3
- blocks=3, insns=42, edges=7, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x007eb60b)
- branch points:
  - 0x007eb604: je -> 0x007eb610 (jcc_true) | ctx: 0x007eb5fc: mov dword ptr [edi + 0x20], eax ; 0x007eb5ff: mov eax, dword ptr [ebp + 0x10] ; 0x007eb602: cmp ecx, eax ; 0x007eb604: je 0x7eb610
  - 0x007eb604: je -> 0x007eb606 (jcc_false) | ctx: 0x007eb5fc: mov dword ptr [edi + 0x20], eax ; 0x007eb5ff: mov eax, dword ptr [ebp + 0x10] ; 0x007eb602: cmp ecx, eax ; 0x007eb604: je 0x7eb610

### 0x007ebdd0
- blocks=3, insns=49, edges=8, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x007ebe09)
- branch points:
  - 0x007ebe02: je -> 0x007ebe0e (jcc_true) | ctx: 0x007ebdfa: mov dword ptr [esi + 0x30], eax ; 0x007ebdfd: mov eax, dword ptr [ebp + 0x24] ; 0x007ebe00: cmp ecx, eax ; 0x007ebe02: je 0x7ebe0e
  - 0x007ebe02: je -> 0x007ebe04 (jcc_false) | ctx: 0x007ebdfa: mov dword ptr [esi + 0x30], eax ; 0x007ebdfd: mov eax, dword ptr [ebp + 0x24] ; 0x007ebe00: cmp ecx, eax ; 0x007ebe02: je 0x7ebe0e

### 0x007ec3d6
- blocks=3, insns=37, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x007ec413)
- branch points:
  - 0x007ec40c: je -> 0x007ec418 (jcc_true) | ctx: 0x007ec404: mov byte ptr [esi + 0x2c], al ; 0x007ec407: mov eax, dword ptr [ebp + 0x18] ; 0x007ec40a: cmp ecx, eax ; 0x007ec40c: je 0x7ec418
  - 0x007ec40c: je -> 0x007ec40e (jcc_false) | ctx: 0x007ec404: mov byte ptr [esi + 0x2c], al ; 0x007ec407: mov eax, dword ptr [ebp + 0x18] ; 0x007ec40a: cmp ecx, eax ; 0x007ec40c: je 0x7ec418

### 0x007f6bd0
- blocks=14, insns=113, edges=27, jcc=9, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x007f6c6a)
- branch points:
  - 0x007f6be9: jb -> 0x007f6bf2 (jcc_true) | ctx: 0x007f6bdc: mov dword ptr [ebp - 0xc], 0 ; 0x007f6be3: mov ecx, dword ptr [edi + 0x14] ; 0x007f6be6: cmp ecx, 0x10 ; 0x007f6be9: jb 0x7f6bf2
  - 0x007f6be9: jb -> 0x007f6beb (jcc_false) | ctx: 0x007f6bdc: mov dword ptr [ebp - 0xc], 0 ; 0x007f6be3: mov ecx, dword ptr [edi + 0x14] ; 0x007f6be6: cmp ecx, 0x10 ; 0x007f6be9: jb 0x7f6bf2
  - 0x007f6bf8: jb -> 0x007f6bfe (jcc_true) | ctx: 0x007f6bf2: mov dword ptr [ebp - 4], edi ; 0x007f6bf5: cmp ecx, 0x10 ; 0x007f6bf8: jb 0x7f6bfe
  - 0x007f6bf8: jb -> 0x007f6bfa (jcc_false) | ctx: 0x007f6bf2: mov dword ptr [ebp - 4], edi ; 0x007f6bf5: cmp ecx, 0x10 ; 0x007f6bf8: jb 0x7f6bfe
  - 0x007f6bf0: jmp -> 0x007f6bf5 (jmp) | ctx: 0x007f6beb: mov eax, dword ptr [edi] ; 0x007f6bed: mov dword ptr [ebp - 4], eax ; 0x007f6bf0: jmp 0x7f6bf5
  - 0x007f6c08: jb -> 0x007f6c0e (jcc_true) | ctx: 0x007f6c00: mov eax, dword ptr [edi + 0x10] ; 0x007f6c03: add eax, edx ; 0x007f6c05: cmp ecx, 0x10 ; 0x007f6c08: jb 0x7f6c0e
  - 0x007f6c08: jb -> 0x007f6c0a (jcc_false) | ctx: 0x007f6c00: mov eax, dword ptr [edi + 0x10] ; 0x007f6c03: add eax, edx ; 0x007f6c05: cmp ecx, 0x10 ; 0x007f6c08: jb 0x7f6c0e
  - 0x007f6bfc: jmp -> 0x007f6c00 (jmp) | ctx: 0x007f6bfa: mov edx, dword ptr [edi] ; 0x007f6bfc: jmp 0x7f6c00
  - 0x007f6bf8: jb -> 0x007f6bfe (jcc_true) | ctx: 0x007f6bf5: cmp ecx, 0x10 ; 0x007f6bf8: jb 0x7f6bfe
  - 0x007f6bf8: jb -> 0x007f6bfa (jcc_false) | ctx: 0x007f6bf5: cmp ecx, 0x10 ; 0x007f6bf8: jb 0x7f6bfe
  - 0x007f6c22: je -> 0x007f6c41 (jcc_true) | ctx: 0x007f6c1a: cmova ecx, edx ; 0x007f6c1d: mov dword ptr [ebp - 8], ecx ; 0x007f6c20: test ecx, ecx ; 0x007f6c22: je 0x7f6c41
  - 0x007f6c22: je -> 0x007f6c24 (jcc_false) | ctx: 0x007f6c1a: cmova ecx, edx ; 0x007f6c1d: mov dword ptr [ebp - 8], ecx ; 0x007f6c20: test ecx, ecx ; 0x007f6c22: je 0x7f6c41
  - 0x007f6c0c: jmp -> 0x007f6c10 (jmp) | ctx: 0x007f6c0a: mov ebx, dword ptr [edi] ; 0x007f6c0c: jmp 0x7f6c10
  - 0x007f6c08: jb -> 0x007f6c0e (jcc_true) | ctx: 0x007f6c00: mov eax, dword ptr [edi + 0x10] ; 0x007f6c03: add eax, edx ; 0x007f6c05: cmp ecx, 0x10 ; 0x007f6c08: jb 0x7f6c0e
  - 0x007f6c08: jb -> 0x007f6c0a (jcc_false) | ctx: 0x007f6c00: mov eax, dword ptr [edi + 0x10] ; 0x007f6c03: add eax, edx ; 0x007f6c05: cmp ecx, 0x10 ; 0x007f6c08: jb 0x7f6c0e
  - 0x007f6c3c: jne -> 0x007f6c26 (jcc_true) | ctx: 0x007f6c36: mov byte ptr [esi + ecx], al ; 0x007f6c39: inc esi ; 0x007f6c3a: cmp esi, edi ; 0x007f6c3c: jne 0x7f6c26
  - 0x007f6c3c: jne -> 0x007f6c3e (jcc_false) | ctx: 0x007f6c36: mov byte ptr [esi + ecx], al ; 0x007f6c39: inc esi ; 0x007f6c3a: cmp esi, edi ; 0x007f6c3c: jne 0x7f6c26
  - 0x007f6c22: je -> 0x007f6c41 (jcc_true) | ctx: 0x007f6c1a: cmova ecx, edx ; 0x007f6c1d: mov dword ptr [ebp - 8], ecx ; 0x007f6c20: test ecx, ecx ; 0x007f6c22: je 0x7f6c41
  - 0x007f6c22: je -> 0x007f6c24 (jcc_false) | ctx: 0x007f6c1a: cmova ecx, edx ; 0x007f6c1d: mov dword ptr [ebp - 8], ecx ; 0x007f6c20: test ecx, ecx ; 0x007f6c22: je 0x7f6c41
  - 0x007f6c3c: jne -> 0x007f6c26 (jcc_true) | ctx: 0x007f6c36: mov byte ptr [esi + ecx], al ; 0x007f6c39: inc esi ; 0x007f6c3a: cmp esi, edi ; 0x007f6c3c: jne 0x7f6c26
  - 0x007f6c3c: jne -> 0x007f6c3e (jcc_false) | ctx: 0x007f6c36: mov byte ptr [esi + ecx], al ; 0x007f6c39: inc esi ; 0x007f6c3a: cmp esi, edi ; 0x007f6c3c: jne 0x7f6c26

### 0x00807360
- blocks=15, insns=163, edges=33, jcc=10, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x008074aa)
- branch points:
  - 0x008073ab: je -> 0x00807413 (jcc_true) | ctx: 0x0080739f: mov dword ptr [ebp - 0x14], esi ; 0x008073a2: mov dword ptr [ebp - 4], 0 ; 0x008073a9: test esi, esi ; 0x008073ab: je 0x807413
  - 0x008073ab: je -> 0x008073ad (jcc_false) | ctx: 0x0080739f: mov dword ptr [ebp - 0x14], esi ; 0x008073a2: mov dword ptr [ebp - 4], 0 ; 0x008073a9: test esi, esi ; 0x008073ab: je 0x807413
  - 0x0080743e: jne -> 0x00807444 (jcc_true) | ctx: 0x00807430: mov dword ptr [ebp - 0x1c], 0 ; 0x00807437: mov byte ptr [ebp - 0x2c], 0 ; 0x0080743b: cmp byte ptr [edx], 0 ; 0x0080743e: jne 0x807444
  - 0x0080743e: jne -> 0x00807440 (jcc_false) | ctx: 0x00807430: mov dword ptr [ebp - 0x1c], 0 ; 0x00807437: mov byte ptr [ebp - 0x2c], 0 ; 0x0080743b: cmp byte ptr [edx], 0 ; 0x0080743e: jne 0x807444
  - 0x00807403: jb -> 0x00807407 (jcc_true) | ctx: 0x008073f1: mov dword ptr [eax + 0x14], 0xf ; 0x008073f8: mov dword ptr [eax + 0x10], 0 ; 0x008073ff: cmp dword ptr [eax + 0x14], 0x10 ; 0x00807403: jb 0x807407
  - 0x00807403: jb -> 0x00807405 (jcc_false) | ctx: 0x008073f1: mov dword ptr [eax + 0x14], 0xf ; 0x008073f8: mov dword ptr [eax + 0x10], 0 ; 0x008073ff: cmp dword ptr [eax + 0x14], 0x10 ; 0x00807403: jb 0x807407
  - 0x00807455: jne -> 0x00807450 (jcc_true) | ctx: 0x00807450: mov al, byte ptr [ecx] ; 0x00807452: inc ecx ; 0x00807453: test al, al ; 0x00807455: jne 0x807450
  - 0x00807455: jne -> 0x00807457 (jcc_false) | ctx: 0x00807450: mov al, byte ptr [ecx] ; 0x00807452: inc ecx ; 0x00807453: test al, al ; 0x00807455: jne 0x807450
  - 0x00807442: jmp -> 0x00807459 (jmp) | ctx: 0x00807440: xor ecx, ecx ; 0x00807442: jmp 0x807459
  - 0x00807411: jmp -> 0x00807415 (jmp) | ctx: 0x00807407: mov byte ptr [eax], 0 ; 0x0080740a: mov dword ptr [esi + 0x4c], 0xffffffff ; 0x00807411: jmp 0x807415
  - 0x00807411: jmp -> 0x00807415 (jmp) | ctx: 0x00807405: mov eax, dword ptr [eax] ; 0x00807407: mov byte ptr [eax], 0 ; 0x0080740a: mov dword ptr [esi + 0x4c], 0xffffffff ; 0x00807411: jmp 0x807415
  - 0x00807455: jne -> 0x00807450 (jcc_true) | ctx: 0x00807450: mov al, byte ptr [ecx] ; 0x00807452: inc ecx ; 0x00807453: test al, al ; 0x00807455: jne 0x807450
  - 0x00807455: jne -> 0x00807457 (jcc_false) | ctx: 0x00807450: mov al, byte ptr [ecx] ; 0x00807452: inc ecx ; 0x00807453: test al, al ; 0x00807455: jne 0x807450
  - 0x008074a3: je -> 0x008074af (jcc_true) | ctx: 0x0080749b: lea ecx, [esi + 0x34] ; 0x0080749e: lea eax, [ebp - 0x2c] ; 0x008074a1: cmp ecx, eax ; 0x008074a3: je 0x8074af
  - 0x008074a3: je -> 0x008074a5 (jcc_false) | ctx: 0x0080749b: lea ecx, [esi + 0x34] ; 0x0080749e: lea eax, [ebp - 0x2c] ; 0x008074a1: cmp ecx, eax ; 0x008074a3: je 0x8074af
  - 0x008074a3: je -> 0x008074af (jcc_true) | ctx: 0x0080749b: lea ecx, [esi + 0x34] ; 0x0080749e: lea eax, [ebp - 0x2c] ; 0x008074a1: cmp ecx, eax ; 0x008074a3: je 0x8074af
  - 0x008074a3: je -> 0x008074a5 (jcc_false) | ctx: 0x0080749b: lea ecx, [esi + 0x34] ; 0x0080749e: lea eax, [ebp - 0x2c] ; 0x008074a1: cmp ecx, eax ; 0x008074a3: je 0x8074af
  - 0x0080743e: jne -> 0x00807444 (jcc_true) | ctx: 0x00807430: mov dword ptr [ebp - 0x1c], 0 ; 0x00807437: mov byte ptr [ebp - 0x2c], 0 ; 0x0080743b: cmp byte ptr [edx], 0 ; 0x0080743e: jne 0x807444
  - 0x0080743e: jne -> 0x00807440 (jcc_false) | ctx: 0x00807430: mov dword ptr [ebp - 0x1c], 0 ; 0x00807437: mov byte ptr [ebp - 0x2c], 0 ; 0x0080743b: cmp byte ptr [edx], 0 ; 0x0080743e: jne 0x807444
  - 0x008074c0: jb -> 0x008074cd (jcc_true) | ctx: 0x008074b2: mov dword ptr [esi + 0x4c], eax ; 0x008074b5: cmp dword ptr [ebp - 0x18], 0x10 ; 0x008074b9: mov dword ptr [ebp - 4], 4 ; 0x008074c0: jb 0x8074cd
  - 0x008074c0: jb -> 0x008074c2 (jcc_false) | ctx: 0x008074b2: mov dword ptr [esi + 0x4c], eax ; 0x008074b5: cmp dword ptr [ebp - 0x18], 0x10 ; 0x008074b9: mov dword ptr [ebp - 4], 4 ; 0x008074c0: jb 0x8074cd
  - 0x008074c0: jb -> 0x008074cd (jcc_true) | ctx: 0x008074b2: mov dword ptr [esi + 0x4c], eax ; 0x008074b5: cmp dword ptr [ebp - 0x18], 0x10 ; 0x008074b9: mov dword ptr [ebp - 4], 4 ; 0x008074c0: jb 0x8074cd
  - 0x008074c0: jb -> 0x008074c2 (jcc_false) | ctx: 0x008074b2: mov dword ptr [esi + 0x4c], eax ; 0x008074b5: cmp dword ptr [ebp - 0x18], 0x10 ; 0x008074b9: mov dword ptr [ebp - 4], 4 ; 0x008074c0: jb 0x8074cd

### 0x00814070
- blocks=17, insns=202, edges=38, jcc=11, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x008141c5)
- branch points:
  - 0x0081409d: je -> 0x00814207 (jcc_true) | ctx: 0x00814094: call 0x84a150 ; 0x00814099: mov ebx, eax ; 0x0081409b: test ebx, ebx ; 0x0081409d: je 0x814207
  - 0x0081409d: je -> 0x008140a3 (jcc_false) | ctx: 0x00814094: call 0x84a150 ; 0x00814099: mov ebx, eax ; 0x0081409b: test ebx, ebx ; 0x0081409d: je 0x814207
  - 0x008140ce: je -> 0x00814136 (jcc_true) | ctx: 0x008140c2: mov dword ptr [ebp - 0x14], esi ; 0x008140c5: mov dword ptr [ebp - 4], 0 ; 0x008140cc: test esi, esi ; 0x008140ce: je 0x814136
  - 0x008140ce: je -> 0x008140d0 (jcc_false) | ctx: 0x008140c2: mov dword ptr [ebp - 0x14], esi ; 0x008140c5: mov dword ptr [ebp - 4], 0 ; 0x008140cc: test esi, esi ; 0x008140ce: je 0x814136
  - 0x0081415b: jne -> 0x00814161 (jcc_true) | ctx: 0x0081414d: cmp byte ptr [edx], 0 ; 0x00814150: mov dword ptr [ebp - 0x20], 0 ; 0x00814157: mov byte ptr [ebp - 0x30], 0 ; 0x0081415b: jne 0x814161
  - 0x0081415b: jne -> 0x0081415d (jcc_false) | ctx: 0x0081414d: cmp byte ptr [edx], 0 ; 0x00814150: mov dword ptr [ebp - 0x20], 0 ; 0x00814157: mov byte ptr [ebp - 0x30], 0 ; 0x0081415b: jne 0x814161
  - 0x00814126: jb -> 0x0081412a (jcc_true) | ctx: 0x00814114: mov dword ptr [eax + 0x14], 0xf ; 0x0081411b: mov dword ptr [eax + 0x10], 0 ; 0x00814122: cmp dword ptr [eax + 0x14], 0x10 ; 0x00814126: jb 0x81412a
  - 0x00814126: jb -> 0x00814128 (jcc_false) | ctx: 0x00814114: mov dword ptr [eax + 0x14], 0xf ; 0x0081411b: mov dword ptr [eax + 0x10], 0 ; 0x00814122: cmp dword ptr [eax + 0x14], 0x10 ; 0x00814126: jb 0x81412a
  - 0x0081416b: jne -> 0x00814166 (jcc_true) | ctx: 0x00814166: mov al, byte ptr [ecx] ; 0x00814168: inc ecx ; 0x00814169: test al, al ; 0x0081416b: jne 0x814166
  - 0x0081416b: jne -> 0x0081416d (jcc_false) | ctx: 0x00814166: mov al, byte ptr [ecx] ; 0x00814168: inc ecx ; 0x00814169: test al, al ; 0x0081416b: jne 0x814166
  - 0x0081415f: jmp -> 0x0081416f (jmp) | ctx: 0x0081415d: xor ecx, ecx ; 0x0081415f: jmp 0x81416f
  - 0x00814134: jmp -> 0x00814138 (jmp) | ctx: 0x0081412a: mov byte ptr [eax], 0 ; 0x0081412d: mov dword ptr [esi + 0x4c], 0xffffffff ; 0x00814134: jmp 0x814138
  - 0x00814134: jmp -> 0x00814138 (jmp) | ctx: 0x00814128: mov eax, dword ptr [eax] ; 0x0081412a: mov byte ptr [eax], 0 ; 0x0081412d: mov dword ptr [esi + 0x4c], 0xffffffff ; 0x00814134: jmp 0x814138
  - 0x0081416b: jne -> 0x00814166 (jcc_true) | ctx: 0x00814166: mov al, byte ptr [ecx] ; 0x00814168: inc ecx ; 0x00814169: test al, al ; 0x0081416b: jne 0x814166
  - 0x0081416b: jne -> 0x0081416d (jcc_false) | ctx: 0x00814166: mov al, byte ptr [ecx] ; 0x00814168: inc ecx ; 0x00814169: test al, al ; 0x0081416b: jne 0x814166
  - 0x008141be: je -> 0x008141ca (jcc_true) | ctx: 0x008141b6: lea ecx, [esi + 0x34] ; 0x008141b9: lea eax, [ebp - 0x30] ; 0x008141bc: cmp ecx, eax ; 0x008141be: je 0x8141ca
  - 0x008141be: je -> 0x008141c0 (jcc_false) | ctx: 0x008141b6: lea ecx, [esi + 0x34] ; 0x008141b9: lea eax, [ebp - 0x30] ; 0x008141bc: cmp ecx, eax ; 0x008141be: je 0x8141ca
  - 0x008141be: je -> 0x008141ca (jcc_true) | ctx: 0x008141b6: lea ecx, [esi + 0x34] ; 0x008141b9: lea eax, [ebp - 0x30] ; 0x008141bc: cmp ecx, eax ; 0x008141be: je 0x8141ca
  - 0x008141be: je -> 0x008141c0 (jcc_false) | ctx: 0x008141b6: lea ecx, [esi + 0x34] ; 0x008141b9: lea eax, [ebp - 0x30] ; 0x008141bc: cmp ecx, eax ; 0x008141be: je 0x8141ca
  - 0x0081415b: jne -> 0x00814161 (jcc_true) | ctx: 0x0081414d: cmp byte ptr [edx], 0 ; 0x00814150: mov dword ptr [ebp - 0x20], 0 ; 0x00814157: mov byte ptr [ebp - 0x30], 0 ; 0x0081415b: jne 0x814161
  - 0x0081415b: jne -> 0x0081415d (jcc_false) | ctx: 0x0081414d: cmp byte ptr [edx], 0 ; 0x00814150: mov dword ptr [ebp - 0x20], 0 ; 0x00814157: mov byte ptr [ebp - 0x30], 0 ; 0x0081415b: jne 0x814161
  - 0x008141dd: jb -> 0x008141ea (jcc_true) | ctx: 0x008141cf: mov dword ptr [esi + 0x4c], eax ; 0x008141d2: cmp dword ptr [ebp - 0x1c], 0x10 ; 0x008141d6: mov dword ptr [ebp - 4], 4 ; 0x008141dd: jb 0x8141ea
  - 0x008141dd: jb -> 0x008141df (jcc_false) | ctx: 0x008141cf: mov dword ptr [esi + 0x4c], eax ; 0x008141d2: cmp dword ptr [ebp - 0x1c], 0x10 ; 0x008141d6: mov dword ptr [ebp - 4], 4 ; 0x008141dd: jb 0x8141ea
  - 0x008141dd: jb -> 0x008141ea (jcc_true) | ctx: 0x008141cf: mov dword ptr [esi + 0x4c], eax ; 0x008141d2: cmp dword ptr [ebp - 0x1c], 0x10 ; 0x008141d6: mov dword ptr [ebp - 4], 4 ; 0x008141dd: jb 0x8141ea
  - 0x008141dd: jb -> 0x008141df (jcc_false) | ctx: 0x008141cf: mov dword ptr [esi + 0x4c], eax ; 0x008141d2: cmp dword ptr [ebp - 0x1c], 0x10 ; 0x008141d6: mov dword ptr [ebp - 4], 4 ; 0x008141dd: jb 0x8141ea

### 0x008224f0
- blocks=16, insns=568, edges=37, jcc=13, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0082294e)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00822968)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00822982)
- branch points:
  - 0x00822658: jne -> 0x00822662 (jcc_true) | ctx: 0x0082264a: mov eax, dword ptr [esi + 0x468] ; 0x00822650: mov dword ptr [ebx + 0x468], eax ; 0x00822656: test dl, dl ; 0x00822658: jne 0x822662
  - 0x00822658: jne -> 0x0082265a (jcc_false) | ctx: 0x0082264a: mov eax, dword ptr [esi + 0x468] ; 0x00822650: mov dword ptr [ebx + 0x468], eax ; 0x00822656: test dl, dl ; 0x00822658: jne 0x822662
  - 0x008226f2: je -> 0x008226fe (jcc_true) | ctx: 0x008226e4: mov byte ptr [ebx + 0x2e8], al ; 0x008226ea: lea eax, [esi + 0x2ec] ; 0x008226f0: cmp ecx, eax ; 0x008226f2: je 0x8226fe
  - 0x008226f2: je -> 0x008226f4 (jcc_false) | ctx: 0x008226e4: mov byte ptr [ebx + 0x2e8], al ; 0x008226ea: lea eax, [esi + 0x2ec] ; 0x008226f0: cmp ecx, eax ; 0x008226f2: je 0x8226fe
  - 0x00822660: jmp -> 0x0082267c (jmp) | ctx: 0x0082265a: mov byte ptr [ebx + 0x2ce], dl ; 0x00822660: jmp 0x82267c
  - 0x0082270c: je -> 0x00822718 (jcc_true) | ctx: 0x008226fe: lea eax, [esi + 0x304] ; 0x00822704: lea ecx, [ebx + 0x304] ; 0x0082270a: cmp ecx, eax ; 0x0082270c: je 0x822718
  - 0x0082270c: je -> 0x0082270e (jcc_false) | ctx: 0x008226fe: lea eax, [esi + 0x304] ; 0x00822704: lea ecx, [ebx + 0x304] ; 0x0082270a: cmp ecx, eax ; 0x0082270c: je 0x822718
  - 0x0082270c: je -> 0x00822718 (jcc_true) | ctx: 0x008226fe: lea eax, [esi + 0x304] ; 0x00822704: lea ecx, [ebx + 0x304] ; 0x0082270a: cmp ecx, eax ; 0x0082270c: je 0x822718
  - 0x0082270c: je -> 0x0082270e (jcc_false) | ctx: 0x008226fe: lea eax, [esi + 0x304] ; 0x00822704: lea ecx, [ebx + 0x304] ; 0x0082270a: cmp ecx, eax ; 0x0082270c: je 0x822718
  - 0x008226f2: je -> 0x008226fe (jcc_true) | ctx: 0x008226e4: mov byte ptr [ebx + 0x2e8], al ; 0x008226ea: lea eax, [esi + 0x2ec] ; 0x008226f0: cmp ecx, eax ; 0x008226f2: je 0x8226fe
  - 0x008226f2: je -> 0x008226f4 (jcc_false) | ctx: 0x008226e4: mov byte ptr [ebx + 0x2e8], al ; 0x008226ea: lea eax, [esi + 0x2ec] ; 0x008226f0: cmp ecx, eax ; 0x008226f2: je 0x8226fe
  - 0x00822726: je -> 0x00822732 (jcc_true) | ctx: 0x00822718: lea eax, [esi + 0x31c] ; 0x0082271e: lea ecx, [ebx + 0x31c] ; 0x00822724: cmp ecx, eax ; 0x00822726: je 0x822732
  - 0x00822726: je -> 0x00822728 (jcc_false) | ctx: 0x00822718: lea eax, [esi + 0x31c] ; 0x0082271e: lea ecx, [ebx + 0x31c] ; 0x00822724: cmp ecx, eax ; 0x00822726: je 0x822732
  - 0x00822726: je -> 0x00822732 (jcc_true) | ctx: 0x00822718: lea eax, [esi + 0x31c] ; 0x0082271e: lea ecx, [ebx + 0x31c] ; 0x00822724: cmp ecx, eax ; 0x00822726: je 0x822732
  - 0x00822726: je -> 0x00822728 (jcc_false) | ctx: 0x00822718: lea eax, [esi + 0x31c] ; 0x0082271e: lea ecx, [ebx + 0x31c] ; 0x00822724: cmp ecx, eax ; 0x00822726: je 0x822732
  - 0x00822947: je -> 0x00822953 (jcc_true) | ctx: 0x00822939: mov dword ptr [ebx + 0x39c], eax ; 0x0082293f: lea eax, [esi + 0x334] ; 0x00822945: cmp ecx, eax ; 0x00822947: je 0x822953
  - 0x00822947: je -> 0x00822949 (jcc_false) | ctx: 0x00822939: mov dword ptr [ebx + 0x39c], eax ; 0x0082293f: lea eax, [esi + 0x334] ; 0x00822945: cmp ecx, eax ; 0x00822947: je 0x822953
  - 0x00822947: je -> 0x00822953 (jcc_true) | ctx: 0x00822939: mov dword ptr [ebx + 0x39c], eax ; 0x0082293f: lea eax, [esi + 0x334] ; 0x00822945: cmp ecx, eax ; 0x00822947: je 0x822953
  - 0x00822947: je -> 0x00822949 (jcc_false) | ctx: 0x00822939: mov dword ptr [ebx + 0x39c], eax ; 0x0082293f: lea eax, [esi + 0x334] ; 0x00822945: cmp ecx, eax ; 0x00822947: je 0x822953
  - 0x00822961: je -> 0x0082296d (jcc_true) | ctx: 0x00822953: lea eax, [esi + 0x364] ; 0x00822959: lea ecx, [ebx + 0x364] ; 0x0082295f: cmp ecx, eax ; 0x00822961: je 0x82296d
  - 0x00822961: je -> 0x00822963 (jcc_false) | ctx: 0x00822953: lea eax, [esi + 0x364] ; 0x00822959: lea ecx, [ebx + 0x364] ; 0x0082295f: cmp ecx, eax ; 0x00822961: je 0x82296d
  - 0x00822961: je -> 0x0082296d (jcc_true) | ctx: 0x00822953: lea eax, [esi + 0x364] ; 0x00822959: lea ecx, [ebx + 0x364] ; 0x0082295f: cmp ecx, eax ; 0x00822961: je 0x82296d
  - 0x00822961: je -> 0x00822963 (jcc_false) | ctx: 0x00822953: lea eax, [esi + 0x364] ; 0x00822959: lea ecx, [ebx + 0x364] ; 0x0082295f: cmp ecx, eax ; 0x00822961: je 0x82296d
  - 0x0082297b: je -> 0x00822987 (jcc_true) | ctx: 0x0082296d: lea eax, [esi + 0x34c] ; 0x00822973: lea ecx, [ebx + 0x34c] ; 0x00822979: cmp ecx, eax ; 0x0082297b: je 0x822987
  - 0x0082297b: je -> 0x0082297d (jcc_false) | ctx: 0x0082296d: lea eax, [esi + 0x34c] ; 0x00822973: lea ecx, [ebx + 0x34c] ; 0x00822979: cmp ecx, eax ; 0x0082297b: je 0x822987
  - 0x0082297b: je -> 0x00822987 (jcc_true) | ctx: 0x0082296d: lea eax, [esi + 0x34c] ; 0x00822973: lea ecx, [ebx + 0x34c] ; 0x00822979: cmp ecx, eax ; 0x0082297b: je 0x822987
  - 0x0082297b: je -> 0x0082297d (jcc_false) | ctx: 0x0082296d: lea eax, [esi + 0x34c] ; 0x00822973: lea ecx, [ebx + 0x34c] ; 0x00822979: cmp ecx, eax ; 0x0082297b: je 0x822987

### 0x00822f67
- blocks=103, insns=577, edges=252, jcc=84, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x0066a5b2 at 0x00822f93)
- branch points:
  - 0x00822f72: jne -> 0x00823500 (jcc_true) | ctx: 0x00822f6a: push edi ; 0x00822f6b: mov dword ptr [ebp - 0xc], esi ; 0x00822f6e: cmp dword ptr [esi + 0x54], 1 ; 0x00822f72: jne 0x823500
  - 0x00822f72: jne -> 0x00822f78 (jcc_false) | ctx: 0x00822f6a: push edi ; 0x00822f6b: mov dword ptr [ebp - 0xc], esi ; 0x00822f6e: cmp dword ptr [esi + 0x54], 1 ; 0x00822f72: jne 0x823500
  - 0x00822fc0: je -> 0x00822fc7 (jcc_true) | ctx: 0x00822fb7: mov ecx, dword ptr [ebp - 0x18] ; 0x00822fba: mov dword ptr [ebp - 0x10], eax ; 0x00822fbd: mov dword ptr [esi + 0x5c], ecx ; 0x00822fc0: je 0x822fc7
  - 0x00822fc0: je -> 0x00822fc2 (jcc_false) | ctx: 0x00822fb7: mov ecx, dword ptr [ebp - 0x18] ; 0x00822fba: mov dword ptr [ebp - 0x10], eax ; 0x00822fbd: mov dword ptr [esi + 0x5c], ecx ; 0x00822fc0: je 0x822fc7
  - 0x00822fcb: je -> 0x00822fd5 (jcc_true) | ctx: 0x00822fc7: cmp dword ptr [esi + 0x7c], 0 ; 0x00822fcb: je 0x822fd5
  - 0x00822fcb: je -> 0x00822fcd (jcc_false) | ctx: 0x00822fc7: cmp dword ptr [esi + 0x7c], 0 ; 0x00822fcb: je 0x822fd5
  - 0x00822fc5: jmp -> 0x00822fd5 (jmp) | ctx: 0x00822fc2: xorps xmm1, xmm1 ; 0x00822fc5: jmp 0x822fd5
  - 0x00822ffa: jne -> 0x00823021 (jcc_true) | ctx: 0x00822ff3: mov eax, dword ptr [ecx] ; 0x00822ff5: call dword ptr [eax] ; 0x00822ff7: cmp eax, 2 ; 0x00822ffa: jne 0x823021
  - 0x00822ffa: jne -> 0x00822ffc (jcc_false) | ctx: 0x00822ff3: mov eax, dword ptr [ecx] ; 0x00822ff5: call dword ptr [eax] ; 0x00822ff7: cmp eax, 2 ; 0x00822ffa: jne 0x823021
  - 0x00822ffa: jne -> 0x00823021 (jcc_true) | ctx: 0x00822ff3: mov eax, dword ptr [ecx] ; 0x00822ff5: call dword ptr [eax] ; 0x00822ff7: cmp eax, 2 ; 0x00822ffa: jne 0x823021
  - 0x00822ffa: jne -> 0x00822ffc (jcc_false) | ctx: 0x00822ff3: mov eax, dword ptr [ecx] ; 0x00822ff5: call dword ptr [eax] ; 0x00822ff7: cmp eax, 2 ; 0x00822ffa: jne 0x823021
  - 0x0082303b: je -> 0x008234a8 (jcc_true) | ctx: 0x00823033: mov byte ptr [ebp - 1], al ; 0x00823036: mov edi, dword ptr [edi] ; 0x00823038: cmp edi, dword ptr [esi + 0x78] ; 0x0082303b: je 0x8234a8
  - 0x0082303b: je -> 0x00823041 (jcc_false) | ctx: 0x00823033: mov byte ptr [ebp - 1], al ; 0x00823036: mov edi, dword ptr [edi] ; 0x00823038: cmp edi, dword ptr [esi + 0x78] ; 0x0082303b: je 0x8234a8
  - 0x00823000: jne -> 0x00823021 (jcc_true) | ctx: 0x00822ffc: cmp dword ptr [esi + 0x7c], 0 ; 0x00823000: jne 0x823021
  - 0x00823000: jne -> 0x00823002 (jcc_false) | ctx: 0x00822ffc: cmp dword ptr [esi + 0x7c], 0 ; 0x00823000: jne 0x823021
  - 0x008234ac: jne -> 0x008234b2 (jcc_true) | ctx: 0x008234a8: cmp byte ptr [ebp - 3], 0 ; 0x008234ac: jne 0x8234b2
  - 0x008234ac: jne -> 0x008234ae (jcc_false) | ctx: 0x008234a8: cmp byte ptr [ebp - 3], 0 ; 0x008234ac: jne 0x8234b2
  - 0x0082305e: jne -> 0x00823067 (jcc_true) | ctx: 0x00823050: movups xmmword ptr [ebp - 0x3c], xmm0 ; 0x00823054: movq xmm0, qword ptr [edi + 0x18] ; 0x00823059: movq qword ptr [ebp - 0x2c], xmm0 ; 0x0082305e: jne 0x823067
  - 0x0082305e: jne -> 0x00823060 (jcc_false) | ctx: 0x00823050: movups xmmword ptr [ebp - 0x3c], xmm0 ; 0x00823054: movq xmm0, qword ptr [edi + 0x18] ; 0x00823059: movq qword ptr [ebp - 0x2c], xmm0 ; 0x0082305e: jne 0x823067
  - 0x00823006: jne -> 0x00823021 (jcc_true) | ctx: 0x00823002: cmp dword ptr [esi + 0x10], 0 ; 0x00823006: jne 0x823021
  - 0x00823006: jne -> 0x00823008 (jcc_false) | ctx: 0x00823002: cmp dword ptr [esi + 0x10], 0 ; 0x00823006: jne 0x823021
  - 0x008234b9: jmp -> 0x00823021 (jmp) | ctx: 0x008234b2: mov dword ptr [esi + 0x70], 0 ; 0x008234b9: jmp 0x823021
  - 0x008234b0: je -> 0x008234be (jcc_true) | ctx: 0x008234ae: test al, al ; 0x008234b0: je 0x8234be
  - 0x008234b0: je -> 0x008234b2 (jcc_false) | ctx: 0x008234ae: test al, al ; 0x008234b0: je 0x8234be
  - 0x00823075: jb -> 0x0082316b (jcc_true) | ctx: 0x0082306c: mov eax, dword ptr [ebx] ; 0x0082306e: call dword ptr [eax + 4] ; 0x00823071: cmp dword ptr [eax + 8], 2 ; 0x00823075: jb 0x82316b
  - 0x00823075: jb -> 0x0082307b (jcc_false) | ctx: 0x0082306c: mov eax, dword ptr [ebx] ; 0x0082306e: call dword ptr [eax + 4] ; 0x00823071: cmp dword ptr [eax + 8], 2 ; 0x00823075: jb 0x82316b
  - 0x00823075: jb -> 0x0082316b (jcc_true) | ctx: 0x0082306c: mov eax, dword ptr [ebx] ; 0x0082306e: call dword ptr [eax + 4] ; 0x00823071: cmp dword ptr [eax + 8], 2 ; 0x00823075: jb 0x82316b
  - 0x00823075: jb -> 0x0082307b (jcc_false) | ctx: 0x0082306c: mov eax, dword ptr [ebx] ; 0x0082306e: call dword ptr [eax + 4] ; 0x00823071: cmp dword ptr [eax + 8], 2 ; 0x00823075: jb 0x82316b
  - 0x008234c6: je -> 0x008234f9 (jcc_true) | ctx: 0x008234be: mov byte ptr [esi + 0x6d], 0 ; 0x008234c2: cmp dword ptr [esi + 0x7c], 0 ; 0x008234c6: je 0x8234f9
  - 0x008234c6: je -> 0x008234c8 (jcc_false) | ctx: 0x008234be: mov byte ptr [esi + 0x6d], 0 ; 0x008234c2: cmp dword ptr [esi + 0x7c], 0 ; 0x008234c6: je 0x8234f9
  - 0x00823172: jne -> 0x0082317b (jcc_true) | ctx: 0x0082316b: cmp dword ptr [0xf8bc28], 0 ; 0x00823172: jne 0x82317b
  - 0x00823172: jne -> 0x00823174 (jcc_false) | ctx: 0x0082316b: cmp dword ptr [0xf8bc28], 0 ; 0x00823172: jne 0x82317b
  - 0x00823084: jne -> 0x0082316b (jcc_true) | ctx: 0x0082307b: mov eax, dword ptr [eax + 0x10] ; 0x0082307e: cmp eax, dword ptr [0xf8b764] ; 0x00823084: jne 0x82316b
  - 0x00823084: jne -> 0x0082308a (jcc_false) | ctx: 0x0082307b: mov eax, dword ptr [eax + 0x10] ; 0x0082307e: cmp eax, dword ptr [0xf8b764] ; 0x00823084: jne 0x82316b
  - 0x008234cc: je -> 0x008234f9 (jcc_true) | ctx: 0x008234c8: cmp byte ptr [esi + 0x75], 0 ; 0x008234cc: je 0x8234f9
  - 0x008234cc: je -> 0x008234ce (jcc_false) | ctx: 0x008234c8: cmp byte ptr [esi + 0x75], 0 ; 0x008234cc: je 0x8234f9
  - 0x00823186: jb -> 0x008232a4 (jcc_true) | ctx: 0x0082317d: mov ecx, ebx ; 0x0082317f: call dword ptr [eax + 4] ; 0x00823182: cmp dword ptr [eax + 8], 2 ; 0x00823186: jb 0x8232a4
  - 0x00823186: jb -> 0x0082318c (jcc_false) | ctx: 0x0082317d: mov ecx, ebx ; 0x0082317f: call dword ptr [eax + 4] ; 0x00823182: cmp dword ptr [eax + 8], 2 ; 0x00823186: jb 0x8232a4
  - 0x00823186: jb -> 0x008232a4 (jcc_true) | ctx: 0x0082317d: mov ecx, ebx ; 0x0082317f: call dword ptr [eax + 4] ; 0x00823182: cmp dword ptr [eax + 8], 2 ; 0x00823186: jb 0x8232a4
  - 0x00823186: jb -> 0x0082318c (jcc_false) | ctx: 0x0082317d: mov ecx, ebx ; 0x0082317f: call dword ptr [eax + 4] ; 0x00823182: cmp dword ptr [eax + 8], 2 ; 0x00823186: jb 0x8232a4
  - 0x008230ac: je -> 0x00823457 (jcc_true) | ctx: 0x008230a4: not esi ; 0x008230a6: call dword ptr [eax + 0x24] ; 0x008230a9: cmp dword ptr [eax + 0x38], esi ; 0x008230ac: je 0x823457
  - 0x008230ac: je -> 0x008230b2 (jcc_false) | ctx: 0x008230a4: not esi ; 0x008230a6: call dword ptr [eax + 0x24] ; 0x008230a9: cmp dword ptr [eax + 0x38], esi ; 0x008230ac: je 0x823457
  - 0x008234db: jbe -> 0x00823500 (jcc_true) | ctx: 0x008234ce: mov eax, dword ptr [ebp - 0x10] ; 0x008234d1: add dword ptr [esi + 0x70], eax ; 0x008234d4: cmp dword ptr [esi + 0x70], 0x7d0 ; 0x008234db: jbe 0x823500
  - 0x008234db: jbe -> 0x008234dd (jcc_false) | ctx: 0x008234ce: mov eax, dword ptr [ebp - 0x10] ; 0x008234d1: add dword ptr [esi + 0x70], eax ; 0x008234d4: cmp dword ptr [esi + 0x70], 0x7d0 ; 0x008234db: jbe 0x823500
  - 0x008232ab: jne -> 0x008232b4 (jcc_true) | ctx: 0x008232a4: cmp dword ptr [0xf8c928], 0 ; 0x008232ab: jne 0x8232b4
  - 0x008232ab: jne -> 0x008232ad (jcc_false) | ctx: 0x008232a4: cmp dword ptr [0xf8c928], 0 ; 0x008232ab: jne 0x8232b4
  - 0x00823195: jne -> 0x008232a4 (jcc_true) | ctx: 0x0082318c: mov eax, dword ptr [eax + 0x10] ; 0x0082318f: cmp eax, dword ptr [0xf8bc38] ; 0x00823195: jne 0x8232a4
  - 0x00823195: jne -> 0x0082319b (jcc_false) | ctx: 0x0082318c: mov eax, dword ptr [eax + 0x10] ; 0x0082318f: cmp eax, dword ptr [0xf8bc38] ; 0x00823195: jne 0x8232a4
  - 0x0082348c: jmp -> 0x0082349f (jmp) | ctx: 0x00823484: mov edi, esi ; 0x00823486: mov esi, dword ptr [ebp - 0xc] ; 0x00823489: add esp, 4 ; 0x0082348c: jmp 0x82349f
  - 0x008230e6: jne -> 0x008230ef (jcc_true) | ctx: 0x008230d7: call 0x80e9b0 ; 0x008230dc: mov dword ptr [ebx + 0x20], eax ; 0x008230df: cmp dword ptr [0xf8b774], 0 ; 0x008230e6: jne 0x8230ef
  - 0x008230e6: jne -> 0x008230e8 (jcc_false) | ctx: 0x008230d7: call 0x80e9b0 ; 0x008230dc: mov dword ptr [ebx + 0x20], eax ; 0x008230df: cmp dword ptr [0xf8b774], 0 ; 0x008230e6: jne 0x8230ef
  - 0x008234e6: jb -> 0x008234f5 (jcc_true) | ctx: 0x008234dd: mov eax, dword ptr [esi + 0x7c] ; 0x008234e0: cmp eax, dword ptr [esi + 0x80] ; 0x008234e6: jb 0x8234f5
  - 0x008234e6: jb -> 0x008234e8 (jcc_false) | ctx: 0x008234dd: mov eax, dword ptr [esi + 0x7c] ; 0x008234e0: cmp eax, dword ptr [esi + 0x80] ; 0x008234e6: jb 0x8234f5
  - 0x008232bf: jb -> 0x008232e9 (jcc_true) | ctx: 0x008232b6: mov ecx, ebx ; 0x008232b8: call dword ptr [eax + 4] ; 0x008232bb: cmp dword ptr [eax + 8], 3 ; 0x008232bf: jb 0x8232e9
  - 0x008232bf: jb -> 0x008232c1 (jcc_false) | ctx: 0x008232b6: mov ecx, ebx ; 0x008232b8: call dword ptr [eax + 4] ; 0x008232bb: cmp dword ptr [eax + 8], 3 ; 0x008232bf: jb 0x8232e9
  - 0x008232bf: jb -> 0x008232e9 (jcc_true) | ctx: 0x008232b6: mov ecx, ebx ; 0x008232b8: call dword ptr [eax + 4] ; 0x008232bb: cmp dword ptr [eax + 8], 3 ; 0x008232bf: jb 0x8232e9
  - 0x008232bf: jb -> 0x008232c1 (jcc_false) | ctx: 0x008232b6: mov ecx, ebx ; 0x008232b8: call dword ptr [eax + 4] ; 0x008232bb: cmp dword ptr [eax + 8], 3 ; 0x008232bf: jb 0x8232e9
  - 0x008231bd: je -> 0x00823457 (jcc_true) | ctx: 0x008231b5: not esi ; 0x008231b7: call dword ptr [eax + 0x20] ; 0x008231ba: cmp dword ptr [eax + 0x38], esi ; 0x008231bd: je 0x823457
  - 0x008231bd: je -> 0x008231c3 (jcc_false) | ctx: 0x008231b5: not esi ; 0x008231b7: call dword ptr [eax + 0x20] ; 0x008231ba: cmp dword ptr [eax + 0x38], esi ; 0x008231bd: je 0x823457
  - 0x008234a2: jne -> 0x00823041 (jcc_true) | ctx: 0x0082349f: cmp edi, dword ptr [esi + 0x78] ; 0x008234a2: jne 0x823041
  - 0x008234a2: jne -> 0x008234a8 (jcc_false) | ctx: 0x0082349f: cmp edi, dword ptr [esi + 0x78] ; 0x008234a2: jne 0x823041
  - 0x008230fa: jb -> 0x0082344a (jcc_true) | ctx: 0x008230f1: mov ecx, ebx ; 0x008230f3: call dword ptr [eax + 4] ; 0x008230f6: cmp dword ptr [eax + 8], 3 ; 0x008230fa: jb 0x82344a
  - 0x008230fa: jb -> 0x00823100 (jcc_false) | ctx: 0x008230f1: mov ecx, ebx ; 0x008230f3: call dword ptr [eax + 4] ; 0x008230f6: cmp dword ptr [eax + 8], 3 ; 0x008230fa: jb 0x82344a
  - 0x008230fa: jb -> 0x0082344a (jcc_true) | ctx: 0x008230f1: mov ecx, ebx ; 0x008230f3: call dword ptr [eax + 4] ; 0x008230f6: cmp dword ptr [eax + 8], 3 ; 0x008230fa: jb 0x82344a
  - 0x008230fa: jb -> 0x00823100 (jcc_false) | ctx: 0x008230f1: mov ecx, ebx ; 0x008230f3: call dword ptr [eax + 4] ; 0x008230f6: cmp dword ptr [eax + 8], 3 ; 0x008230fa: jb 0x82344a
  - 0x008232f0: jne -> 0x008232f9 (jcc_true) | ctx: 0x008232e9: cmp dword ptr [0xf8c904], 0 ; 0x008232f0: jne 0x8232f9
  - 0x008232f0: jne -> 0x008232f2 (jcc_false) | ctx: 0x008232e9: cmp dword ptr [0xf8c904], 0 ; 0x008232f0: jne 0x8232f9
  - 0x008232ca: jne -> 0x008232e9 (jcc_true) | ctx: 0x008232c1: mov eax, dword ptr [eax + 0x14] ; 0x008232c4: cmp eax, dword ptr [0xf8c93c] ; 0x008232ca: jne 0x8232e9
  - 0x008232ca: jne -> 0x008232cc (jcc_false) | ctx: 0x008232c1: mov eax, dword ptr [eax + 0x14] ; 0x008232c4: cmp eax, dword ptr [0xf8c93c] ; 0x008232ca: jne 0x8232e9
  - 0x008231f5: jne -> 0x00823212 (jcc_true) | ctx: 0x008231ec: mov ebx, dword ptr [ebp - 0x3c] ; 0x008231ef: mov dword ptr [ebp - 8], eax ; 0x008231f2: cmp eax, -1 ; 0x008231f5: jne 0x823212
  - 0x008231f5: jne -> 0x008231f7 (jcc_false) | ctx: 0x008231ec: mov ebx, dword ptr [ebp - 0x3c] ; 0x008231ef: mov dword ptr [ebp - 8], eax ; 0x008231f2: cmp eax, -1 ; 0x008231f5: jne 0x823212
  - 0x0082344f: je -> 0x00823251 (jcc_true) | ctx: 0x0082344a: xor al, al ; 0x0082344c: cmp byte ptr [ebp - 2], al ; 0x0082344f: je 0x823251
  - 0x0082344f: je -> 0x00823455 (jcc_false) | ctx: 0x0082344a: xor al, al ; 0x0082344c: cmp byte ptr [ebp - 2], al ; 0x0082344f: je 0x823251
  - 0x00823109: jne -> 0x0082344a (jcc_true) | ctx: 0x00823100: mov eax, dword ptr [eax + 0x14] ; 0x00823103: cmp eax, dword ptr [0xf8b788] ; 0x00823109: jne 0x82344a
  - 0x00823109: jne -> 0x0082310f (jcc_false) | ctx: 0x00823100: mov eax, dword ptr [eax + 0x14] ; 0x00823103: cmp eax, dword ptr [0xf8b788] ; 0x00823109: jne 0x82344a
  - 0x00823304: jb -> 0x00823311 (jcc_true) | ctx: 0x008232fb: mov ecx, ebx ; 0x008232fd: call dword ptr [eax + 4] ; 0x00823300: cmp dword ptr [eax + 8], 3 ; 0x00823304: jb 0x823311
  - 0x00823304: jb -> 0x00823306 (jcc_false) | ctx: 0x008232fb: mov ecx, ebx ; 0x008232fd: call dword ptr [eax + 4] ; 0x00823300: cmp dword ptr [eax + 8], 3 ; 0x00823304: jb 0x823311
  - 0x00823304: jb -> 0x00823311 (jcc_true) | ctx: 0x008232fb: mov ecx, ebx ; 0x008232fd: call dword ptr [eax + 4] ; 0x00823300: cmp dword ptr [eax + 8], 3 ; 0x00823304: jb 0x823311
  - 0x00823304: jb -> 0x00823306 (jcc_false) | ctx: 0x008232fb: mov ecx, ebx ; 0x008232fd: call dword ptr [eax + 4] ; 0x00823300: cmp dword ptr [eax + 8], 3 ; 0x00823304: jb 0x823311
  - 0x008232e4: jmp -> 0x0082324f (jmp) | ctx: 0x008232da: mov ecx, esi ; 0x008232dc: call 0x80edd0 ; 0x008232e1: mov dword ptr [ebp - 8], eax ; 0x008232e4: jmp 0x82324f
  - ... 102 more

### 0x008395da
- blocks=26, insns=307, edges=64, jcc=21, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x008396eb)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00839736)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00839784)
- branch points:
  - 0x0083961c: je -> 0x00839622 (jcc_true) | ctx: 0x00839614: mov dword ptr [ebp + 8], ebx ; 0x00839617: mov dword ptr [ebp + 0xc], eax ; 0x0083961a: test ebx, ebx ; 0x0083961c: je 0x839622
  - 0x0083961c: je -> 0x0083961e (jcc_false) | ctx: 0x00839614: mov dword ptr [ebp + 8], ebx ; 0x00839617: mov dword ptr [ebp + 0xc], eax ; 0x0083961a: test ebx, ebx ; 0x0083961c: je 0x839622
  - 0x0083962a: je -> 0x0083964b (jcc_true) | ctx: 0x00839622: mov edi, dword ptr [esi + 0x14] ; 0x00839625: or ebx, 0xffffffff ; 0x00839628: test edi, edi ; 0x0083962a: je 0x83964b
  - 0x0083962a: je -> 0x0083962c (jcc_false) | ctx: 0x00839622: mov edi, dword ptr [esi + 0x14] ; 0x00839625: or ebx, 0xffffffff ; 0x00839628: test edi, edi ; 0x0083962a: je 0x83964b
  - 0x0083962a: je -> 0x0083964b (jcc_true) | ctx: 0x00839622: mov edi, dword ptr [esi + 0x14] ; 0x00839625: or ebx, 0xffffffff ; 0x00839628: test edi, edi ; 0x0083962a: je 0x83964b
  - 0x0083962a: je -> 0x0083962c (jcc_false) | ctx: 0x00839622: mov edi, dword ptr [esi + 0x14] ; 0x00839625: or ebx, 0xffffffff ; 0x00839628: test edi, edi ; 0x0083962a: je 0x83964b
  - 0x008396d3: jb -> 0x008396da (jcc_true) | ctx: 0x008396c1: mov dword ptr [esi + 0x68], 0xf ; 0x008396c8: mov dword ptr [esi + 0x64], 0 ; 0x008396cf: cmp dword ptr [esi + 0x68], 0x10 ; 0x008396d3: jb 0x8396da
  - 0x008396d3: jb -> 0x008396d5 (jcc_false) | ctx: 0x008396c1: mov dword ptr [esi + 0x68], 0xf ; 0x008396c8: mov dword ptr [esi + 0x64], 0 ; 0x008396cf: cmp dword ptr [esi + 0x68], 0x10 ; 0x008396d3: jb 0x8396da
  - 0x00839633: jne -> 0x0083964b (jcc_true) | ctx: 0x0083962c: mov eax, ebx ; 0x0083962e: lock xadd dword ptr [edi + 4], eax ; 0x00839633: jne 0x83964b
  - 0x00839633: jne -> 0x00839635 (jcc_false) | ctx: 0x0083962c: mov eax, ebx ; 0x0083962e: lock xadd dword ptr [edi + 4], eax ; 0x00839633: jne 0x83964b
  - 0x0083971e: jb -> 0x00839725 (jcc_true) | ctx: 0x00839706: mov dword ptr [esi + 0x80], 0xf ; 0x00839710: mov dword ptr [esi + 0x7c], 0 ; 0x00839717: cmp dword ptr [esi + 0x80], 0x10 ; 0x0083971e: jb 0x839725
  - 0x0083971e: jb -> 0x00839720 (jcc_false) | ctx: 0x00839706: mov dword ptr [esi + 0x80], 0xf ; 0x00839710: mov dword ptr [esi + 0x7c], 0 ; 0x00839717: cmp dword ptr [esi + 0x80], 0x10 ; 0x0083971e: jb 0x839725
  - 0x008396d8: jmp -> 0x008396dd (jmp) | ctx: 0x008396d5: mov eax, dword ptr [esi + 0x54] ; 0x008396d8: jmp 0x8396dd
  - 0x00839642: jne -> 0x0083964b (jcc_true) | ctx: 0x00839639: call dword ptr [eax] ; 0x0083963b: mov eax, ebx ; 0x0083963d: lock xadd dword ptr [edi + 8], eax ; 0x00839642: jne 0x83964b
  - 0x00839642: jne -> 0x00839644 (jcc_false) | ctx: 0x00839639: call dword ptr [eax] ; 0x0083963b: mov eax, ebx ; 0x0083963d: lock xadd dword ptr [edi + 8], eax ; 0x00839642: jne 0x83964b
  - 0x0083976c: jb -> 0x00839772 (jcc_true) | ctx: 0x0083975a: mov dword ptr [edi + 0x14], 0xf ; 0x00839761: mov dword ptr [edi + 0x10], 0 ; 0x00839768: cmp dword ptr [edi + 0x14], 0x10 ; 0x0083976c: jb 0x839772
  - 0x0083976c: jb -> 0x0083976e (jcc_false) | ctx: 0x0083975a: mov dword ptr [edi + 0x14], 0xf ; 0x00839761: mov dword ptr [edi + 0x10], 0 ; 0x00839768: cmp dword ptr [edi + 0x14], 0x10 ; 0x0083976c: jb 0x839772
  - 0x00839723: jmp -> 0x00839728 (jmp) | ctx: 0x00839720: mov eax, dword ptr [esi + 0x6c] ; 0x00839723: jmp 0x839728
  - 0x0083971e: jb -> 0x00839725 (jcc_true) | ctx: 0x00839706: mov dword ptr [esi + 0x80], 0xf ; 0x00839710: mov dword ptr [esi + 0x7c], 0 ; 0x00839717: cmp dword ptr [esi + 0x80], 0x10 ; 0x0083971e: jb 0x839725
  - 0x0083971e: jb -> 0x00839720 (jcc_false) | ctx: 0x00839706: mov dword ptr [esi + 0x80], 0xf ; 0x00839710: mov dword ptr [esi + 0x7c], 0 ; 0x00839717: cmp dword ptr [esi + 0x80], 0x10 ; 0x0083971e: jb 0x839725
  - 0x008396d3: jb -> 0x008396da (jcc_true) | ctx: 0x008396c1: mov dword ptr [esi + 0x68], 0xf ; 0x008396c8: mov dword ptr [esi + 0x64], 0 ; 0x008396cf: cmp dword ptr [esi + 0x68], 0x10 ; 0x008396d3: jb 0x8396da
  - 0x008396d3: jb -> 0x008396d5 (jcc_false) | ctx: 0x008396c1: mov dword ptr [esi + 0x68], 0xf ; 0x008396c8: mov dword ptr [esi + 0x64], 0 ; 0x008396cf: cmp dword ptr [esi + 0x68], 0x10 ; 0x008396d3: jb 0x8396da
  - 0x008397b9: je -> 0x008397d9 (jcc_true) | ctx: 0x008397aa: mov byte ptr [esi + 0xa4], al ; 0x008397b0: mov dword ptr [esi + 0x48], 0x1f4 ; 0x008397b7: test edi, edi ; 0x008397b9: je 0x8397d9
  - 0x008397b9: je -> 0x008397bb (jcc_false) | ctx: 0x008397aa: mov byte ptr [esi + 0xa4], al ; 0x008397b0: mov dword ptr [esi + 0x48], 0x1f4 ; 0x008397b7: test edi, edi ; 0x008397b9: je 0x8397d9
  - 0x00839770: jmp -> 0x00839774 (jmp) | ctx: 0x0083976e: mov eax, dword ptr [edi] ; 0x00839770: jmp 0x839774
  - 0x0083976c: jb -> 0x00839772 (jcc_true) | ctx: 0x0083975a: mov dword ptr [edi + 0x14], 0xf ; 0x00839761: mov dword ptr [edi + 0x10], 0 ; 0x00839768: cmp dword ptr [edi + 0x14], 0x10 ; 0x0083976c: jb 0x839772
  - 0x0083976c: jb -> 0x0083976e (jcc_false) | ctx: 0x0083975a: mov dword ptr [edi + 0x14], 0xf ; 0x00839761: mov dword ptr [edi + 0x10], 0 ; 0x00839768: cmp dword ptr [edi + 0x14], 0x10 ; 0x0083976c: jb 0x839772
  - 0x008397e1: jb -> 0x008397ee (jcc_true) | ctx: 0x008397d9: cmp dword ptr [ebp + 0x68], 0x10 ; 0x008397dd: mov byte ptr [ebp - 4], 8 ; 0x008397e1: jb 0x8397ee
  - 0x008397e1: jb -> 0x008397e3 (jcc_false) | ctx: 0x008397d9: cmp dword ptr [ebp + 0x68], 0x10 ; 0x008397dd: mov byte ptr [ebp - 4], 8 ; 0x008397e1: jb 0x8397ee
  - 0x008397c2: jne -> 0x008397d9 (jcc_true) | ctx: 0x008397bb: mov eax, ebx ; 0x008397bd: lock xadd dword ptr [edi + 4], eax ; 0x008397c2: jne 0x8397d9
  - 0x008397c2: jne -> 0x008397c4 (jcc_false) | ctx: 0x008397bb: mov eax, ebx ; 0x008397bd: lock xadd dword ptr [edi + 4], eax ; 0x008397c2: jne 0x8397d9
  - 0x008397b9: je -> 0x008397d9 (jcc_true) | ctx: 0x008397aa: mov byte ptr [esi + 0xa4], al ; 0x008397b0: mov dword ptr [esi + 0x48], 0x1f4 ; 0x008397b7: test edi, edi ; 0x008397b9: je 0x8397d9
  - 0x008397b9: je -> 0x008397bb (jcc_false) | ctx: 0x008397aa: mov byte ptr [esi + 0xa4], al ; 0x008397b0: mov dword ptr [esi + 0x48], 0x1f4 ; 0x008397b7: test edi, edi ; 0x008397b9: je 0x8397d9
  - 0x0083980b: jb -> 0x00839818 (jcc_true) | ctx: 0x008397fc: mov byte ptr [ebp + 0x54], 0 ; 0x00839800: cmp dword ptr [ebp + 0x80], 0x10 ; 0x00839807: mov byte ptr [ebp - 4], 9 ; 0x0083980b: jb 0x839818
  - 0x0083980b: jb -> 0x0083980d (jcc_false) | ctx: 0x008397fc: mov byte ptr [ebp + 0x54], 0 ; 0x00839800: cmp dword ptr [ebp + 0x80], 0x10 ; 0x00839807: mov byte ptr [ebp - 4], 9 ; 0x0083980b: jb 0x839818
  - 0x0083980b: jb -> 0x00839818 (jcc_true) | ctx: 0x008397fc: mov byte ptr [ebp + 0x54], 0 ; 0x00839800: cmp dword ptr [ebp + 0x80], 0x10 ; 0x00839807: mov byte ptr [ebp - 4], 9 ; 0x0083980b: jb 0x839818
  - 0x0083980b: jb -> 0x0083980d (jcc_false) | ctx: 0x008397fc: mov byte ptr [ebp + 0x54], 0 ; 0x00839800: cmp dword ptr [ebp + 0x80], 0x10 ; 0x00839807: mov byte ptr [ebp - 4], 9 ; 0x0083980b: jb 0x839818
  - 0x008397d0: jne -> 0x008397d9 (jcc_true) | ctx: 0x008397c8: call dword ptr [eax] ; 0x008397ca: lock xadd dword ptr [edi + 8], ebx ; 0x008397cf: dec ebx ; 0x008397d0: jne 0x8397d9
  - 0x008397d0: jne -> 0x008397d2 (jcc_false) | ctx: 0x008397c8: call dword ptr [eax] ; 0x008397ca: lock xadd dword ptr [edi + 8], ebx ; 0x008397cf: dec ebx ; 0x008397d0: jne 0x8397d9
  - 0x0083983b: jb -> 0x0083984b (jcc_true) | ctx: 0x00839829: mov byte ptr [ebp + 0x6c], 0 ; 0x0083982d: cmp dword ptr [ebp + 0x98], 0x10 ; 0x00839834: mov dword ptr [ebp - 4], 0xa ; 0x0083983b: jb 0x83984b
  - 0x0083983b: jb -> 0x0083983d (jcc_false) | ctx: 0x00839829: mov byte ptr [ebp + 0x6c], 0 ; 0x0083982d: cmp dword ptr [ebp + 0x98], 0x10 ; 0x00839834: mov dword ptr [ebp - 4], 0xa ; 0x0083983b: jb 0x83984b
  - 0x0083983b: jb -> 0x0083984b (jcc_true) | ctx: 0x00839829: mov byte ptr [ebp + 0x6c], 0 ; 0x0083982d: cmp dword ptr [ebp + 0x98], 0x10 ; 0x00839834: mov dword ptr [ebp - 4], 0xa ; 0x0083983b: jb 0x83984b
  - 0x0083983b: jb -> 0x0083983d (jcc_false) | ctx: 0x00839829: mov byte ptr [ebp + 0x6c], 0 ; 0x0083982d: cmp dword ptr [ebp + 0x98], 0x10 ; 0x00839834: mov dword ptr [ebp - 4], 0xa ; 0x0083983b: jb 0x83984b
  - 0x008397e1: jb -> 0x008397ee (jcc_true) | ctx: 0x008397d6: call dword ptr [eax + 4] ; 0x008397d9: cmp dword ptr [ebp + 0x68], 0x10 ; 0x008397dd: mov byte ptr [ebp - 4], 8 ; 0x008397e1: jb 0x8397ee
  - 0x008397e1: jb -> 0x008397e3 (jcc_false) | ctx: 0x008397d6: call dword ptr [eax + 4] ; 0x008397d9: cmp dword ptr [ebp + 0x68], 0x10 ; 0x008397dd: mov byte ptr [ebp - 4], 8 ; 0x008397e1: jb 0x8397ee

### 0x0083c324
- blocks=27, insns=484, edges=56, jcc=25, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0083c5dd)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0083c5f7)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0083c611)
- branch points:
  - 0x0083c353: jne -> 0x0083c347 (jcc_true) | ctx: 0x0083c34a: lea edx, [edx + 1] ; 0x0083c34d: mov byte ptr [edx - 1], al ; 0x0083c350: sub ebx, 1 ; 0x0083c353: jne 0x83c347
  - 0x0083c353: jne -> 0x0083c355 (jcc_false) | ctx: 0x0083c34a: lea edx, [edx + 1] ; 0x0083c34d: mov byte ptr [edx - 1], al ; 0x0083c350: sub ebx, 1 ; 0x0083c353: jne 0x83c347
  - 0x0083c353: jne -> 0x0083c347 (jcc_true) | ctx: 0x0083c34a: lea edx, [edx + 1] ; 0x0083c34d: mov byte ptr [edx - 1], al ; 0x0083c350: sub ebx, 1 ; 0x0083c353: jne 0x83c347
  - 0x0083c353: jne -> 0x0083c355 (jcc_false) | ctx: 0x0083c34a: lea edx, [edx + 1] ; 0x0083c34d: mov byte ptr [edx - 1], al ; 0x0083c350: sub ebx, 1 ; 0x0083c353: jne 0x83c347
  - 0x0083c371: jne -> 0x0083c365 (jcc_true) | ctx: 0x0083c368: lea edx, [edx + 1] ; 0x0083c36b: mov byte ptr [edx - 1], al ; 0x0083c36e: sub ebx, 1 ; 0x0083c371: jne 0x83c365
  - 0x0083c371: jne -> 0x0083c373 (jcc_false) | ctx: 0x0083c368: lea edx, [edx + 1] ; 0x0083c36b: mov byte ptr [edx - 1], al ; 0x0083c36e: sub ebx, 1 ; 0x0083c371: jne 0x83c365
  - 0x0083c371: jne -> 0x0083c365 (jcc_true) | ctx: 0x0083c368: lea edx, [edx + 1] ; 0x0083c36b: mov byte ptr [edx - 1], al ; 0x0083c36e: sub ebx, 1 ; 0x0083c371: jne 0x83c365
  - 0x0083c371: jne -> 0x0083c373 (jcc_false) | ctx: 0x0083c368: lea edx, [edx + 1] ; 0x0083c36b: mov byte ptr [edx - 1], al ; 0x0083c36e: sub ebx, 1 ; 0x0083c371: jne 0x83c365
  - 0x0083c39c: jne -> 0x0083c390 (jcc_true) | ctx: 0x0083c393: lea edx, [edx + 1] ; 0x0083c396: mov byte ptr [edx - 1], al ; 0x0083c399: sub ebx, 1 ; 0x0083c39c: jne 0x83c390
  - 0x0083c39c: jne -> 0x0083c39e (jcc_false) | ctx: 0x0083c393: lea edx, [edx + 1] ; 0x0083c396: mov byte ptr [edx - 1], al ; 0x0083c399: sub ebx, 1 ; 0x0083c39c: jne 0x83c390
  - 0x0083c39c: jne -> 0x0083c390 (jcc_true) | ctx: 0x0083c393: lea edx, [edx + 1] ; 0x0083c396: mov byte ptr [edx - 1], al ; 0x0083c399: sub ebx, 1 ; 0x0083c39c: jne 0x83c390
  - 0x0083c39c: jne -> 0x0083c39e (jcc_false) | ctx: 0x0083c393: lea edx, [edx + 1] ; 0x0083c396: mov byte ptr [edx - 1], al ; 0x0083c399: sub ebx, 1 ; 0x0083c39c: jne 0x83c390
  - 0x0083c3dc: jne -> 0x0083c3d0 (jcc_true) | ctx: 0x0083c3d3: lea edx, [edx + 1] ; 0x0083c3d6: mov byte ptr [edx - 1], al ; 0x0083c3d9: sub ebx, 1 ; 0x0083c3dc: jne 0x83c3d0
  - 0x0083c3dc: jne -> 0x0083c3de (jcc_false) | ctx: 0x0083c3d3: lea edx, [edx + 1] ; 0x0083c3d6: mov byte ptr [edx - 1], al ; 0x0083c3d9: sub ebx, 1 ; 0x0083c3dc: jne 0x83c3d0
  - 0x0083c3dc: jne -> 0x0083c3d0 (jcc_true) | ctx: 0x0083c3d3: lea edx, [edx + 1] ; 0x0083c3d6: mov byte ptr [edx - 1], al ; 0x0083c3d9: sub ebx, 1 ; 0x0083c3dc: jne 0x83c3d0
  - 0x0083c3dc: jne -> 0x0083c3de (jcc_false) | ctx: 0x0083c3d3: lea edx, [edx + 1] ; 0x0083c3d6: mov byte ptr [edx - 1], al ; 0x0083c3d9: sub ebx, 1 ; 0x0083c3dc: jne 0x83c3d0
  - 0x0083c48c: jne -> 0x0083c480 (jcc_true) | ctx: 0x0083c483: lea edx, [edx + 1] ; 0x0083c486: mov byte ptr [edx - 1], al ; 0x0083c489: sub ebx, 1 ; 0x0083c48c: jne 0x83c480
  - 0x0083c48c: jne -> 0x0083c48e (jcc_false) | ctx: 0x0083c483: lea edx, [edx + 1] ; 0x0083c486: mov byte ptr [edx - 1], al ; 0x0083c489: sub ebx, 1 ; 0x0083c48c: jne 0x83c480
  - 0x0083c48c: jne -> 0x0083c480 (jcc_true) | ctx: 0x0083c483: lea edx, [edx + 1] ; 0x0083c486: mov byte ptr [edx - 1], al ; 0x0083c489: sub ebx, 1 ; 0x0083c48c: jne 0x83c480
  - 0x0083c48c: jne -> 0x0083c48e (jcc_false) | ctx: 0x0083c483: lea edx, [edx + 1] ; 0x0083c486: mov byte ptr [edx - 1], al ; 0x0083c489: sub ebx, 1 ; 0x0083c48c: jne 0x83c480
  - 0x0083c4ac: jne -> 0x0083c4a0 (jcc_true) | ctx: 0x0083c4a3: lea edx, [edx + 1] ; 0x0083c4a6: mov byte ptr [edx - 1], al ; 0x0083c4a9: sub ebx, 1 ; 0x0083c4ac: jne 0x83c4a0
  - 0x0083c4ac: jne -> 0x0083c4ae (jcc_false) | ctx: 0x0083c4a3: lea edx, [edx + 1] ; 0x0083c4a6: mov byte ptr [edx - 1], al ; 0x0083c4a9: sub ebx, 1 ; 0x0083c4ac: jne 0x83c4a0
  - 0x0083c4ac: jne -> 0x0083c4a0 (jcc_true) | ctx: 0x0083c4a3: lea edx, [edx + 1] ; 0x0083c4a6: mov byte ptr [edx - 1], al ; 0x0083c4a9: sub ebx, 1 ; 0x0083c4ac: jne 0x83c4a0
  - 0x0083c4ac: jne -> 0x0083c4ae (jcc_false) | ctx: 0x0083c4a3: lea edx, [edx + 1] ; 0x0083c4a6: mov byte ptr [edx - 1], al ; 0x0083c4a9: sub ebx, 1 ; 0x0083c4ac: jne 0x83c4a0
  - 0x0083c4cc: jne -> 0x0083c4c0 (jcc_true) | ctx: 0x0083c4c3: lea edx, [edx + 1] ; 0x0083c4c6: mov byte ptr [edx - 1], al ; 0x0083c4c9: sub ebx, 1 ; 0x0083c4cc: jne 0x83c4c0
  - 0x0083c4cc: jne -> 0x0083c4ce (jcc_false) | ctx: 0x0083c4c3: lea edx, [edx + 1] ; 0x0083c4c6: mov byte ptr [edx - 1], al ; 0x0083c4c9: sub ebx, 1 ; 0x0083c4cc: jne 0x83c4c0
  - 0x0083c4cc: jne -> 0x0083c4c0 (jcc_true) | ctx: 0x0083c4c3: lea edx, [edx + 1] ; 0x0083c4c6: mov byte ptr [edx - 1], al ; 0x0083c4c9: sub ebx, 1 ; 0x0083c4cc: jne 0x83c4c0
  - 0x0083c4cc: jne -> 0x0083c4ce (jcc_false) | ctx: 0x0083c4c3: lea edx, [edx + 1] ; 0x0083c4c6: mov byte ptr [edx - 1], al ; 0x0083c4c9: sub ebx, 1 ; 0x0083c4cc: jne 0x83c4c0
  - 0x0083c589: je -> 0x0083c594 (jcc_true) | ctx: 0x0083c57b: mov byte ptr [esi + 0x2e8], al ; 0x0083c581: lea eax, [edi + 0x2ec] ; 0x0083c587: cmp ecx, eax ; 0x0083c589: je 0x83c594
  - 0x0083c589: je -> 0x0083c58b (jcc_false) | ctx: 0x0083c57b: mov byte ptr [esi + 0x2e8], al ; 0x0083c581: lea eax, [edi + 0x2ec] ; 0x0083c587: cmp ecx, eax ; 0x0083c589: je 0x83c594
  - 0x0083c5a2: je -> 0x0083c5ae (jcc_true) | ctx: 0x0083c594: lea eax, [edi + 0x304] ; 0x0083c59a: lea ecx, [esi + 0x304] ; 0x0083c5a0: cmp ecx, eax ; 0x0083c5a2: je 0x83c5ae
  - 0x0083c5a2: je -> 0x0083c5a4 (jcc_false) | ctx: 0x0083c594: lea eax, [edi + 0x304] ; 0x0083c59a: lea ecx, [esi + 0x304] ; 0x0083c5a0: cmp ecx, eax ; 0x0083c5a2: je 0x83c5ae
  - 0x0083c5a2: je -> 0x0083c5ae (jcc_true) | ctx: 0x0083c594: lea eax, [edi + 0x304] ; 0x0083c59a: lea ecx, [esi + 0x304] ; 0x0083c5a0: cmp ecx, eax ; 0x0083c5a2: je 0x83c5ae
  - 0x0083c5a2: je -> 0x0083c5a4 (jcc_false) | ctx: 0x0083c594: lea eax, [edi + 0x304] ; 0x0083c59a: lea ecx, [esi + 0x304] ; 0x0083c5a0: cmp ecx, eax ; 0x0083c5a2: je 0x83c5ae
  - 0x0083c5bc: je -> 0x0083c5c8 (jcc_true) | ctx: 0x0083c5ae: lea eax, [edi + 0x31c] ; 0x0083c5b4: lea ecx, [esi + 0x31c] ; 0x0083c5ba: cmp ecx, eax ; 0x0083c5bc: je 0x83c5c8
  - 0x0083c5bc: je -> 0x0083c5be (jcc_false) | ctx: 0x0083c5ae: lea eax, [edi + 0x31c] ; 0x0083c5b4: lea ecx, [esi + 0x31c] ; 0x0083c5ba: cmp ecx, eax ; 0x0083c5bc: je 0x83c5c8
  - 0x0083c5bc: je -> 0x0083c5c8 (jcc_true) | ctx: 0x0083c5ae: lea eax, [edi + 0x31c] ; 0x0083c5b4: lea ecx, [esi + 0x31c] ; 0x0083c5ba: cmp ecx, eax ; 0x0083c5bc: je 0x83c5c8
  - 0x0083c5bc: je -> 0x0083c5be (jcc_false) | ctx: 0x0083c5ae: lea eax, [edi + 0x31c] ; 0x0083c5b4: lea ecx, [esi + 0x31c] ; 0x0083c5ba: cmp ecx, eax ; 0x0083c5bc: je 0x83c5c8
  - 0x0083c5d6: je -> 0x0083c5e2 (jcc_true) | ctx: 0x0083c5c8: lea eax, [edi + 0x334] ; 0x0083c5ce: lea ecx, [esi + 0x334] ; 0x0083c5d4: cmp ecx, eax ; 0x0083c5d6: je 0x83c5e2
  - 0x0083c5d6: je -> 0x0083c5d8 (jcc_false) | ctx: 0x0083c5c8: lea eax, [edi + 0x334] ; 0x0083c5ce: lea ecx, [esi + 0x334] ; 0x0083c5d4: cmp ecx, eax ; 0x0083c5d6: je 0x83c5e2
  - 0x0083c5d6: je -> 0x0083c5e2 (jcc_true) | ctx: 0x0083c5c8: lea eax, [edi + 0x334] ; 0x0083c5ce: lea ecx, [esi + 0x334] ; 0x0083c5d4: cmp ecx, eax ; 0x0083c5d6: je 0x83c5e2
  - 0x0083c5d6: je -> 0x0083c5d8 (jcc_false) | ctx: 0x0083c5c8: lea eax, [edi + 0x334] ; 0x0083c5ce: lea ecx, [esi + 0x334] ; 0x0083c5d4: cmp ecx, eax ; 0x0083c5d6: je 0x83c5e2
  - 0x0083c5f0: je -> 0x0083c5fc (jcc_true) | ctx: 0x0083c5e2: lea eax, [edi + 0x34c] ; 0x0083c5e8: lea ecx, [esi + 0x34c] ; 0x0083c5ee: cmp ecx, eax ; 0x0083c5f0: je 0x83c5fc
  - 0x0083c5f0: je -> 0x0083c5f2 (jcc_false) | ctx: 0x0083c5e2: lea eax, [edi + 0x34c] ; 0x0083c5e8: lea ecx, [esi + 0x34c] ; 0x0083c5ee: cmp ecx, eax ; 0x0083c5f0: je 0x83c5fc
  - 0x0083c5f0: je -> 0x0083c5fc (jcc_true) | ctx: 0x0083c5e2: lea eax, [edi + 0x34c] ; 0x0083c5e8: lea ecx, [esi + 0x34c] ; 0x0083c5ee: cmp ecx, eax ; 0x0083c5f0: je 0x83c5fc
  - 0x0083c5f0: je -> 0x0083c5f2 (jcc_false) | ctx: 0x0083c5e2: lea eax, [edi + 0x34c] ; 0x0083c5e8: lea ecx, [esi + 0x34c] ; 0x0083c5ee: cmp ecx, eax ; 0x0083c5f0: je 0x83c5fc
  - 0x0083c60a: je -> 0x0083c616 (jcc_true) | ctx: 0x0083c5fc: lea eax, [edi + 0x364] ; 0x0083c602: lea ecx, [esi + 0x364] ; 0x0083c608: cmp ecx, eax ; 0x0083c60a: je 0x83c616
  - 0x0083c60a: je -> 0x0083c60c (jcc_false) | ctx: 0x0083c5fc: lea eax, [edi + 0x364] ; 0x0083c602: lea ecx, [esi + 0x364] ; 0x0083c608: cmp ecx, eax ; 0x0083c60a: je 0x83c616
  - 0x0083c60a: je -> 0x0083c616 (jcc_true) | ctx: 0x0083c5fc: lea eax, [edi + 0x364] ; 0x0083c602: lea ecx, [esi + 0x364] ; 0x0083c608: cmp ecx, eax ; 0x0083c60a: je 0x83c616
  - 0x0083c60a: je -> 0x0083c60c (jcc_false) | ctx: 0x0083c5fc: lea eax, [edi + 0x364] ; 0x0083c602: lea ecx, [esi + 0x364] ; 0x0083c608: cmp ecx, eax ; 0x0083c60a: je 0x83c616

### 0x008425db
- blocks=8, insns=101, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x008426b1)
- branch points:
  - 0x00842602: je -> 0x00842664 (jcc_true) | ctx: 0x008425fa: mov dword ptr [ebp - 0x10], esi ; 0x008425fd: mov dword ptr [ebp - 0x10], esi ; 0x00842600: test esi, esi ; 0x00842602: je 0x842664
  - 0x00842602: je -> 0x00842604 (jcc_false) | ctx: 0x008425fa: mov dword ptr [ebp - 0x10], esi ; 0x008425fd: mov dword ptr [ebp - 0x10], esi ; 0x00842600: test esi, esi ; 0x00842602: je 0x842664
  - 0x008426aa: je -> 0x008426b6 (jcc_true) | ctx: 0x008426a2: mov byte ptr [esi + 0x28], bl ; 0x008426a5: mov byte ptr [esi + 0x29], bh ; 0x008426a8: cmp ecx, eax ; 0x008426aa: je 0x8426b6
  - 0x008426aa: je -> 0x008426ac (jcc_false) | ctx: 0x008426a2: mov byte ptr [esi + 0x28], bl ; 0x008426a5: mov byte ptr [esi + 0x29], bh ; 0x008426a8: cmp ecx, eax ; 0x008426aa: je 0x8426b6
  - 0x00842654: jb -> 0x00842658 (jcc_true) | ctx: 0x00842642: mov dword ptr [eax + 0x14], 0xf ; 0x00842649: mov dword ptr [eax + 0x10], 0 ; 0x00842650: cmp dword ptr [eax + 0x14], 0x10 ; 0x00842654: jb 0x842658
  - 0x00842654: jb -> 0x00842656 (jcc_false) | ctx: 0x00842642: mov dword ptr [eax + 0x14], 0xf ; 0x00842649: mov dword ptr [eax + 0x10], 0 ; 0x00842650: cmp dword ptr [eax + 0x14], 0x10 ; 0x00842654: jb 0x842658
  - 0x00842662: jmp -> 0x00842666 (jmp) | ctx: 0x00842658: mov byte ptr [eax], 0 ; 0x0084265b: mov dword ptr [esi + 0x44], 0xffffffff ; 0x00842662: jmp 0x842666
  - 0x00842662: jmp -> 0x00842666 (jmp) | ctx: 0x00842656: mov eax, dword ptr [eax] ; 0x00842658: mov byte ptr [eax], 0 ; 0x0084265b: mov dword ptr [esi + 0x44], 0xffffffff ; 0x00842662: jmp 0x842666
  - 0x008426aa: je -> 0x008426b6 (jcc_true) | ctx: 0x008426a2: mov byte ptr [esi + 0x28], bl ; 0x008426a5: mov byte ptr [esi + 0x29], bh ; 0x008426a8: cmp ecx, eax ; 0x008426aa: je 0x8426b6
  - 0x008426aa: je -> 0x008426ac (jcc_false) | ctx: 0x008426a2: mov byte ptr [esi + 0x28], bl ; 0x008426a5: mov byte ptr [esi + 0x29], bh ; 0x008426a8: cmp ecx, eax ; 0x008426aa: je 0x8426b6

### 0x00842ab0
- blocks=8, insns=102, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00842b8f)
- branch points:
  - 0x00842af2: je -> 0x00842b4e (jcc_true) | ctx: 0x00842aea: mov dword ptr [ebp - 0x10], edi ; 0x00842aed: mov dword ptr [ebp - 0x10], edi ; 0x00842af0: test edi, edi ; 0x00842af2: je 0x842b4e
  - 0x00842af2: je -> 0x00842af4 (jcc_false) | ctx: 0x00842aea: mov dword ptr [ebp - 0x10], edi ; 0x00842aed: mov dword ptr [ebp - 0x10], edi ; 0x00842af0: test edi, edi ; 0x00842af2: je 0x842b4e
  - 0x00842b88: je -> 0x00842b94 (jcc_true) | ctx: 0x00842b7c: mov dword ptr [ebp - 4], 0xffffffff ; 0x00842b83: mov dword ptr [edi + 0x20], esi ; 0x00842b86: cmp ecx, eax ; 0x00842b88: je 0x842b94
  - 0x00842b88: je -> 0x00842b8a (jcc_false) | ctx: 0x00842b7c: mov dword ptr [ebp - 4], 0xffffffff ; 0x00842b83: mov dword ptr [edi + 0x20], esi ; 0x00842b86: cmp ecx, eax ; 0x00842b88: je 0x842b94
  - 0x00842b3e: jb -> 0x00842b42 (jcc_true) | ctx: 0x00842b2c: mov dword ptr [eax + 0x14], 0xf ; 0x00842b33: mov dword ptr [eax + 0x10], 0 ; 0x00842b3a: cmp dword ptr [eax + 0x14], 0x10 ; 0x00842b3e: jb 0x842b42
  - 0x00842b3e: jb -> 0x00842b40 (jcc_false) | ctx: 0x00842b2c: mov dword ptr [eax + 0x14], 0xf ; 0x00842b33: mov dword ptr [eax + 0x10], 0 ; 0x00842b3a: cmp dword ptr [eax + 0x14], 0x10 ; 0x00842b3e: jb 0x842b42
  - 0x00842b4c: jmp -> 0x00842b50 (jmp) | ctx: 0x00842b42: mov byte ptr [eax], 0 ; 0x00842b45: mov dword ptr [edi + 0x40], 0xffffffff ; 0x00842b4c: jmp 0x842b50
  - 0x00842b4c: jmp -> 0x00842b50 (jmp) | ctx: 0x00842b40: mov eax, dword ptr [eax] ; 0x00842b42: mov byte ptr [eax], 0 ; 0x00842b45: mov dword ptr [edi + 0x40], 0xffffffff ; 0x00842b4c: jmp 0x842b50
  - 0x00842b88: je -> 0x00842b94 (jcc_true) | ctx: 0x00842b7c: mov dword ptr [ebp - 4], 0xffffffff ; 0x00842b83: mov dword ptr [edi + 0x20], esi ; 0x00842b86: cmp ecx, eax ; 0x00842b88: je 0x842b94
  - 0x00842b88: je -> 0x00842b8a (jcc_false) | ctx: 0x00842b7c: mov dword ptr [ebp - 4], 0xffffffff ; 0x00842b83: mov dword ptr [edi + 0x20], esi ; 0x00842b86: cmp ecx, eax ; 0x00842b88: je 0x842b94

### 0x00842bb0
- blocks=8, insns=102, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00842c8f)
- branch points:
  - 0x00842bf2: je -> 0x00842c4e (jcc_true) | ctx: 0x00842bea: mov dword ptr [ebp - 0x10], edi ; 0x00842bed: mov dword ptr [ebp - 0x10], edi ; 0x00842bf0: test edi, edi ; 0x00842bf2: je 0x842c4e
  - 0x00842bf2: je -> 0x00842bf4 (jcc_false) | ctx: 0x00842bea: mov dword ptr [ebp - 0x10], edi ; 0x00842bed: mov dword ptr [ebp - 0x10], edi ; 0x00842bf0: test edi, edi ; 0x00842bf2: je 0x842c4e
  - 0x00842c88: je -> 0x00842c94 (jcc_true) | ctx: 0x00842c7c: mov dword ptr [ebp - 4], 0xffffffff ; 0x00842c83: mov dword ptr [edi + 0x20], esi ; 0x00842c86: cmp ecx, eax ; 0x00842c88: je 0x842c94
  - 0x00842c88: je -> 0x00842c8a (jcc_false) | ctx: 0x00842c7c: mov dword ptr [ebp - 4], 0xffffffff ; 0x00842c83: mov dword ptr [edi + 0x20], esi ; 0x00842c86: cmp ecx, eax ; 0x00842c88: je 0x842c94
  - 0x00842c3e: jb -> 0x00842c42 (jcc_true) | ctx: 0x00842c2c: mov dword ptr [eax + 0x14], 0xf ; 0x00842c33: mov dword ptr [eax + 0x10], 0 ; 0x00842c3a: cmp dword ptr [eax + 0x14], 0x10 ; 0x00842c3e: jb 0x842c42
  - 0x00842c3e: jb -> 0x00842c40 (jcc_false) | ctx: 0x00842c2c: mov dword ptr [eax + 0x14], 0xf ; 0x00842c33: mov dword ptr [eax + 0x10], 0 ; 0x00842c3a: cmp dword ptr [eax + 0x14], 0x10 ; 0x00842c3e: jb 0x842c42
  - 0x00842c4c: jmp -> 0x00842c50 (jmp) | ctx: 0x00842c42: mov byte ptr [eax], 0 ; 0x00842c45: mov dword ptr [edi + 0x40], 0xffffffff ; 0x00842c4c: jmp 0x842c50
  - 0x00842c4c: jmp -> 0x00842c50 (jmp) | ctx: 0x00842c40: mov eax, dword ptr [eax] ; 0x00842c42: mov byte ptr [eax], 0 ; 0x00842c45: mov dword ptr [edi + 0x40], 0xffffffff ; 0x00842c4c: jmp 0x842c50
  - 0x00842c88: je -> 0x00842c94 (jcc_true) | ctx: 0x00842c7c: mov dword ptr [ebp - 4], 0xffffffff ; 0x00842c83: mov dword ptr [edi + 0x20], esi ; 0x00842c86: cmp ecx, eax ; 0x00842c88: je 0x842c94
  - 0x00842c88: je -> 0x00842c8a (jcc_false) | ctx: 0x00842c7c: mov dword ptr [ebp - 4], 0xffffffff ; 0x00842c83: mov dword ptr [edi + 0x20], esi ; 0x00842c86: cmp ecx, eax ; 0x00842c88: je 0x842c94

### 0x00843800
- blocks=8, insns=119, edges=15, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0084390d)
- branch points:
  - 0x0084384b: je -> 0x008438ba (jcc_true) | ctx: 0x0084383f: mov dword ptr [ebp - 0x14], edi ; 0x00843842: mov dword ptr [ebp - 4], 0 ; 0x00843849: test edi, edi ; 0x0084384b: je 0x8438ba
  - 0x0084384b: je -> 0x0084384d (jcc_false) | ctx: 0x0084383f: mov dword ptr [ebp - 0x14], edi ; 0x00843842: mov dword ptr [ebp - 4], 0 ; 0x00843849: test edi, edi ; 0x0084384b: je 0x8438ba
  - 0x00843906: je -> 0x00843912 (jcc_true) | ctx: 0x008438fe: lea ecx, [edi + 0x38] ; 0x00843901: lea eax, [ebx + 0x38] ; 0x00843904: cmp ecx, eax ; 0x00843906: je 0x843912
  - 0x00843906: je -> 0x00843908 (jcc_false) | ctx: 0x008438fe: lea ecx, [edi + 0x38] ; 0x00843901: lea eax, [ebx + 0x38] ; 0x00843904: cmp ecx, eax ; 0x00843906: je 0x843912
  - 0x008438aa: jb -> 0x008438ae (jcc_true) | ctx: 0x00843898: mov dword ptr [eax + 0x14], 0xf ; 0x0084389f: mov dword ptr [eax + 0x10], 0 ; 0x008438a6: cmp dword ptr [eax + 0x14], 0x10 ; 0x008438aa: jb 0x8438ae
  - 0x008438aa: jb -> 0x008438ac (jcc_false) | ctx: 0x00843898: mov dword ptr [eax + 0x14], 0xf ; 0x0084389f: mov dword ptr [eax + 0x10], 0 ; 0x008438a6: cmp dword ptr [eax + 0x14], 0x10 ; 0x008438aa: jb 0x8438ae
  - 0x008438b8: jmp -> 0x008438bc (jmp) | ctx: 0x008438ae: mov byte ptr [eax], 0 ; 0x008438b1: mov dword ptr [edi + 0x50], 0xffffffff ; 0x008438b8: jmp 0x8438bc
  - 0x008438b8: jmp -> 0x008438bc (jmp) | ctx: 0x008438ac: mov eax, dword ptr [eax] ; 0x008438ae: mov byte ptr [eax], 0 ; 0x008438b1: mov dword ptr [edi + 0x50], 0xffffffff ; 0x008438b8: jmp 0x8438bc
  - 0x00843906: je -> 0x00843912 (jcc_true) | ctx: 0x008438fe: lea ecx, [edi + 0x38] ; 0x00843901: lea eax, [ebx + 0x38] ; 0x00843904: cmp ecx, eax ; 0x00843906: je 0x843912
  - 0x00843906: je -> 0x00843908 (jcc_false) | ctx: 0x008438fe: lea ecx, [edi + 0x38] ; 0x00843901: lea eax, [ebx + 0x38] ; 0x00843904: cmp ecx, eax ; 0x00843906: je 0x843912

### 0x00843ec0
- blocks=18, insns=324, edges=46, jcc=9, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00844046)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0084410f)
- branch points:
  - 0x00843f01: jne -> 0x00843fa0 (jcc_true) | ctx: 0x00843ef7: push 1 ; 0x00843ef9: push 0x140 ; 0x00843efe: cmp eax, 1 ; 0x00843f01: jne 0x843fa0
  - 0x00843f01: jne -> 0x00843f07 (jcc_false) | ctx: 0x00843ef7: push 1 ; 0x00843ef9: push 0x140 ; 0x00843efe: cmp eax, 1 ; 0x00843f01: jne 0x843fa0
  - 0x00843fa7: jne -> 0x00844064 (jcc_true) | ctx: 0x00843fa0: cmp dword ptr [ebx + 0x108], -1 ; 0x00843fa7: jne 0x844064
  - 0x00843fa7: jne -> 0x00843fad (jcc_false) | ctx: 0x00843fa0: cmp dword ptr [ebx + 0x108], -1 ; 0x00843fa7: jne 0x844064
  - 0x00843f1e: je -> 0x00843f29 (jcc_true) | ctx: 0x00843f12: mov dword ptr [ebp - 0x18], eax ; 0x00843f15: mov dword ptr [ebp - 4], 0 ; 0x00843f1c: test eax, eax ; 0x00843f1e: je 0x843f29
  - 0x00843f1e: je -> 0x00843f20 (jcc_false) | ctx: 0x00843f12: mov dword ptr [ebp - 0x18], eax ; 0x00843f15: mov dword ptr [ebp - 4], 0 ; 0x00843f1c: test eax, eax ; 0x00843f1e: je 0x843f29
  - 0x0084407b: je -> 0x00844086 (jcc_true) | ctx: 0x0084406f: mov dword ptr [ebp - 0x10], eax ; 0x00844072: mov dword ptr [ebp - 4], 2 ; 0x00844079: test eax, eax ; 0x0084407b: je 0x844086
  - 0x0084407b: je -> 0x0084407d (jcc_false) | ctx: 0x0084406f: mov dword ptr [ebp - 0x10], eax ; 0x00844072: mov dword ptr [ebp - 4], 2 ; 0x00844079: test eax, eax ; 0x0084407b: je 0x844086
  - 0x00843fc4: je -> 0x00843fcf (jcc_true) | ctx: 0x00843fb8: mov dword ptr [ebp - 0x18], eax ; 0x00843fbb: mov dword ptr [ebp - 4], 1 ; 0x00843fc2: test eax, eax ; 0x00843fc4: je 0x843fcf
  - 0x00843fc4: je -> 0x00843fc6 (jcc_false) | ctx: 0x00843fb8: mov dword ptr [ebp - 0x18], eax ; 0x00843fbb: mov dword ptr [ebp - 4], 1 ; 0x00843fc2: test eax, eax ; 0x00843fc4: je 0x843fcf
  - 0x00843f27: jmp -> 0x00843f2b (jmp) | ctx: 0x00843f20: mov ecx, eax ; 0x00843f22: call 0x836ae0 ; 0x00843f27: jmp 0x843f2b
  - 0x00844108: je -> 0x00844114 (jcc_true) | ctx: 0x008440fa: lea ecx, [ebx + 0x124] ; 0x00844100: lea eax, [edi + 0x124] ; 0x00844106: cmp ecx, eax ; 0x00844108: je 0x844114
  - 0x00844108: je -> 0x0084410a (jcc_false) | ctx: 0x008440fa: lea ecx, [ebx + 0x124] ; 0x00844100: lea eax, [edi + 0x124] ; 0x00844106: cmp ecx, eax ; 0x00844108: je 0x844114
  - 0x00844084: jmp -> 0x00844088 (jmp) | ctx: 0x0084407d: mov ecx, eax ; 0x0084407f: call 0x836ae0 ; 0x00844084: jmp 0x844088
  - 0x0084403f: je -> 0x0084404b (jcc_true) | ctx: 0x00844034: mov eax, dword ptr [ebp - 0x1c] ; 0x00844037: mov dword ptr [edi + 0x108], ebx ; 0x0084403d: cmp ecx, eax ; 0x0084403f: je 0x84404b
  - 0x0084403f: je -> 0x00844041 (jcc_false) | ctx: 0x00844034: mov eax, dword ptr [ebp - 0x1c] ; 0x00844037: mov dword ptr [edi + 0x108], ebx ; 0x0084403d: cmp ecx, eax ; 0x0084403f: je 0x84404b
  - 0x00843fcd: jmp -> 0x00843fd1 (jmp) | ctx: 0x00843fc6: mov ecx, eax ; 0x00843fc8: call 0x836ae0 ; 0x00843fcd: jmp 0x843fd1
  - 0x00844108: je -> 0x00844114 (jcc_true) | ctx: 0x008440fa: lea ecx, [ebx + 0x124] ; 0x00844100: lea eax, [edi + 0x124] ; 0x00844106: cmp ecx, eax ; 0x00844108: je 0x844114
  - 0x00844108: je -> 0x0084410a (jcc_false) | ctx: 0x008440fa: lea ecx, [ebx + 0x124] ; 0x00844100: lea eax, [edi + 0x124] ; 0x00844106: cmp ecx, eax ; 0x00844108: je 0x844114
  - 0x0084403f: je -> 0x0084404b (jcc_true) | ctx: 0x00844034: mov eax, dword ptr [ebp - 0x1c] ; 0x00844037: mov dword ptr [edi + 0x108], ebx ; 0x0084403d: cmp ecx, eax ; 0x0084403f: je 0x84404b
  - 0x0084403f: je -> 0x00844041 (jcc_false) | ctx: 0x00844034: mov eax, dword ptr [ebp - 0x1c] ; 0x00844037: mov dword ptr [edi + 0x108], ebx ; 0x0084403d: cmp ecx, eax ; 0x0084403f: je 0x84404b

### 0x00845c30
- blocks=25, insns=347, edges=64, jcc=17, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00845d7b)
- branch points:
  - 0x00845c57: je -> 0x00845f73 (jcc_true) | ctx: 0x00845c4e: push esi ; 0x00845c4f: push edi ; 0x00845c50: cmp dword ptr [ebx + 0x1e8], 0 ; 0x00845c57: je 0x845f73
  - 0x00845c57: je -> 0x00845c5d (jcc_false) | ctx: 0x00845c4e: push esi ; 0x00845c4f: push edi ; 0x00845c50: cmp dword ptr [ebx + 0x1e8], 0 ; 0x00845c57: je 0x845f73
  - 0x00845c72: jne -> 0x00845df2 (jcc_true) | ctx: 0x00845c68: mov edi, dword ptr [eax + 8] ; 0x00845c6b: mov dword ptr [ebp - 0x10], edi ; 0x00845c6e: cmp dword ptr [edi + 0x1c], 1 ; 0x00845c72: jne 0x845df2
  - 0x00845c72: jne -> 0x00845c78 (jcc_false) | ctx: 0x00845c68: mov edi, dword ptr [eax + 8] ; 0x00845c6b: mov dword ptr [ebp - 0x10], edi ; 0x00845c6e: cmp dword ptr [edi + 0x1c], 1 ; 0x00845c72: jne 0x845df2
  - 0x00845df8: je -> 0x00845f31 (jcc_true) | ctx: 0x00845df2: mov eax, dword ptr [edi + 0x1c] ; 0x00845df5: cmp eax, 6 ; 0x00845df8: je 0x845f31
  - 0x00845df8: je -> 0x00845dfe (jcc_false) | ctx: 0x00845df2: mov eax, dword ptr [edi + 0x1c] ; 0x00845df5: cmp eax, 6 ; 0x00845df8: je 0x845f31
  - 0x00845c7c: je -> 0x00845da6 (jcc_true) | ctx: 0x00845c78: cmp byte ptr [edi + 0x40], 0 ; 0x00845c7c: je 0x845da6
  - 0x00845c7c: je -> 0x00845c82 (jcc_false) | ctx: 0x00845c78: cmp byte ptr [edi + 0x40], 0 ; 0x00845c7c: je 0x845da6
  - 0x00845f6d: jne -> 0x00845c60 (jcc_true) | ctx: 0x00845f60: push eax ; 0x00845f61: call 0x845ad0 ; 0x00845f66: cmp dword ptr [ebx + 0x1e8], 0 ; 0x00845f6d: jne 0x845c60
  - 0x00845f6d: jne -> 0x00845f73 (jcc_false) | ctx: 0x00845f60: push eax ; 0x00845f61: call 0x845ad0 ; 0x00845f66: cmp dword ptr [ebx + 0x1e8], 0 ; 0x00845f6d: jne 0x845c60
  - 0x00845e00: je -> 0x00845f31 (jcc_true) | ctx: 0x00845dfe: test eax, eax ; 0x00845e00: je 0x845f31
  - 0x00845e00: je -> 0x00845e06 (jcc_false) | ctx: 0x00845dfe: test eax, eax ; 0x00845e00: je 0x845f31
  - 0x00845dc9: je -> 0x00845df2 (jcc_true) | ctx: 0x00845dc3: push eax ; 0x00845dc4: call dword ptr [esi + 0x5c] ; 0x00845dc7: test eax, eax ; 0x00845dc9: je 0x845df2
  - 0x00845dc9: je -> 0x00845dcb (jcc_false) | ctx: 0x00845dc3: push eax ; 0x00845dc4: call dword ptr [esi + 0x5c] ; 0x00845dc7: test eax, eax ; 0x00845dc9: je 0x845df2
  - 0x00845cad: je -> 0x00845d1c (jcc_true) | ctx: 0x00845ca1: mov dword ptr [ebp - 0x18], edi ; 0x00845ca4: mov dword ptr [ebp - 4], 0 ; 0x00845cab: test edi, edi ; 0x00845cad: je 0x845d1c
  - 0x00845cad: je -> 0x00845caf (jcc_false) | ctx: 0x00845ca1: mov dword ptr [ebp - 0x18], edi ; 0x00845ca4: mov dword ptr [ebp - 4], 0 ; 0x00845cab: test edi, edi ; 0x00845cad: je 0x845d1c
  - 0x00845c72: jne -> 0x00845df2 (jcc_true) | ctx: 0x00845c68: mov edi, dword ptr [eax + 8] ; 0x00845c6b: mov dword ptr [ebp - 0x10], edi ; 0x00845c6e: cmp dword ptr [edi + 0x1c], 1 ; 0x00845c72: jne 0x845df2
  - 0x00845c72: jne -> 0x00845c78 (jcc_false) | ctx: 0x00845c68: mov edi, dword ptr [eax + 8] ; 0x00845c6b: mov dword ptr [ebp - 0x10], edi ; 0x00845c6e: cmp dword ptr [edi + 0x1c], 1 ; 0x00845c72: jne 0x845df2
  - 0x00845e0a: je -> 0x00845eec (jcc_true) | ctx: 0x00845e06: cmp byte ptr [edi + 0x40], 0 ; 0x00845e0a: je 0x845eec
  - 0x00845e0a: je -> 0x00845e10 (jcc_false) | ctx: 0x00845e06: cmp byte ptr [edi + 0x40], 0 ; 0x00845e0a: je 0x845eec
  - 0x00845df8: je -> 0x00845f31 (jcc_true) | ctx: 0x00845ded: call 0x870eb0 ; 0x00845df2: mov eax, dword ptr [edi + 0x1c] ; 0x00845df5: cmp eax, 6 ; 0x00845df8: je 0x845f31
  - 0x00845df8: je -> 0x00845dfe (jcc_false) | ctx: 0x00845ded: call 0x870eb0 ; 0x00845df2: mov eax, dword ptr [edi + 0x1c] ; 0x00845df5: cmp eax, 6 ; 0x00845df8: je 0x845f31
  - 0x00845d74: je -> 0x00845d80 (jcc_true) | ctx: 0x00845d6c: mov esi, dword ptr [ebp + 0x10] ; 0x00845d6f: lea ecx, [edi + 0x38] ; 0x00845d72: cmp ecx, esi ; 0x00845d74: je 0x845d80
  - 0x00845d74: je -> 0x00845d76 (jcc_false) | ctx: 0x00845d6c: mov esi, dword ptr [ebp + 0x10] ; 0x00845d6f: lea ecx, [edi + 0x38] ; 0x00845d72: cmp ecx, esi ; 0x00845d74: je 0x845d80
  - 0x00845d0c: jb -> 0x00845d10 (jcc_true) | ctx: 0x00845cfa: mov dword ptr [eax + 0x14], 0xf ; 0x00845d01: mov dword ptr [eax + 0x10], 0 ; 0x00845d08: cmp dword ptr [eax + 0x14], 0x10 ; 0x00845d0c: jb 0x845d10
  - 0x00845d0c: jb -> 0x00845d0e (jcc_false) | ctx: 0x00845cfa: mov dword ptr [eax + 0x14], 0xf ; 0x00845d01: mov dword ptr [eax + 0x10], 0 ; 0x00845d08: cmp dword ptr [eax + 0x14], 0x10 ; 0x00845d0c: jb 0x845d10
  - 0x00845f0f: je -> 0x00845f31 (jcc_true) | ctx: 0x00845f09: push eax ; 0x00845f0a: call dword ptr [esi + 0x5c] ; 0x00845f0d: test eax, eax ; 0x00845f0f: je 0x845f31
  - 0x00845f0f: je -> 0x00845f11 (jcc_false) | ctx: 0x00845f09: push eax ; 0x00845f0a: call dword ptr [esi + 0x5c] ; 0x00845f0d: test eax, eax ; 0x00845f0f: je 0x845f31
  - 0x00845e38: je -> 0x00845e84 (jcc_true) | ctx: 0x00845e2c: mov dword ptr [ebp - 0x14], esi ; 0x00845e2f: mov dword ptr [ebp - 4], 3 ; 0x00845e36: test esi, esi ; 0x00845e38: je 0x845e84
  - 0x00845e38: je -> 0x00845e3a (jcc_false) | ctx: 0x00845e2c: mov dword ptr [ebp - 0x14], esi ; 0x00845e2f: mov dword ptr [ebp - 4], 3 ; 0x00845e36: test esi, esi ; 0x00845e38: je 0x845e84
  - 0x00845da4: jmp -> 0x00845df2 (jmp) | ctx: 0x00845d9d: push eax ; 0x00845d9e: call dword ptr [edx + 0x1c] ; 0x00845da1: mov edi, dword ptr [ebp - 0x10] ; 0x00845da4: jmp 0x845df2
  - 0x00845da4: jmp -> 0x00845df2 (jmp) | ctx: 0x00845d9d: push eax ; 0x00845d9e: call dword ptr [edx + 0x1c] ; 0x00845da1: mov edi, dword ptr [ebp - 0x10] ; 0x00845da4: jmp 0x845df2
  - 0x00845d1a: jmp -> 0x00845d1e (jmp) | ctx: 0x00845d10: mov byte ptr [eax], 0 ; 0x00845d13: mov dword ptr [edi + 0x50], 0xffffffff ; 0x00845d1a: jmp 0x845d1e
  - 0x00845d1a: jmp -> 0x00845d1e (jmp) | ctx: 0x00845d0e: mov eax, dword ptr [eax] ; 0x00845d10: mov byte ptr [eax], 0 ; 0x00845d13: mov dword ptr [edi + 0x50], 0xffffffff ; 0x00845d1a: jmp 0x845d1e
  - 0x00845f6d: jne -> 0x00845c60 (jcc_true) | ctx: 0x00845f60: push eax ; 0x00845f61: call 0x845ad0 ; 0x00845f66: cmp dword ptr [ebx + 0x1e8], 0 ; 0x00845f6d: jne 0x845c60
  - 0x00845f6d: jne -> 0x00845f73 (jcc_false) | ctx: 0x00845f60: push eax ; 0x00845f61: call 0x845ad0 ; 0x00845f66: cmp dword ptr [ebx + 0x1e8], 0 ; 0x00845f6d: jne 0x845c60
  - 0x00845eea: jmp -> 0x00845f31 (jmp) | ctx: 0x00845ee5: push ecx ; 0x00845ee6: push eax ; 0x00845ee7: call dword ptr [edx + 0x1c] ; 0x00845eea: jmp 0x845f31
  - 0x00845e82: jmp -> 0x00845e86 (jmp) | ctx: 0x00845e72: mov byte ptr [ebp - 4], 4 ; 0x00845e76: mov dword ptr [esi + 0x28], 0xffffffff ; 0x00845e7d: call 0x9289a0 ; 0x00845e82: jmp 0x845e86
  - 0x00845d74: je -> 0x00845d80 (jcc_true) | ctx: 0x00845d6c: mov esi, dword ptr [ebp + 0x10] ; 0x00845d6f: lea ecx, [edi + 0x38] ; 0x00845d72: cmp ecx, esi ; 0x00845d74: je 0x845d80
  - 0x00845d74: je -> 0x00845d76 (jcc_false) | ctx: 0x00845d6c: mov esi, dword ptr [ebp + 0x10] ; 0x00845d6f: lea ecx, [edi + 0x38] ; 0x00845d72: cmp ecx, esi ; 0x00845d74: je 0x845d80
  - 0x00845eea: jmp -> 0x00845f31 (jmp) | ctx: 0x00845ee5: push ecx ; 0x00845ee6: push eax ; 0x00845ee7: call dword ptr [edx + 0x1c] ; 0x00845eea: jmp 0x845f31

### 0x00846130
- blocks=44, insns=247, edges=86, jcc=35, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x008462b1)
- branch points:
  - 0x00846146: je -> 0x00846187 (jcc_true) | ctx: 0x0084613c: mov ebx, ecx ; 0x0084613e: push edi ; 0x0084613f: cmp si, word ptr [0xd6b9ec] ; 0x00846146: je 0x846187
  - 0x00846146: je -> 0x00846148 (jcc_false) | ctx: 0x0084613c: mov ebx, ecx ; 0x0084613e: push edi ; 0x0084613f: cmp si, word ptr [0xd6b9ec] ; 0x00846146: je 0x846187
  - 0x00846191: je -> 0x008461ae (jcc_true) | ctx: 0x0084618a: mov edi, dword ptr [ebp + 0x14] ; 0x0084618d: mov eax, dword ptr [ecx] ; 0x0084618f: cmp eax, ecx ; 0x00846191: je 0x8461ae
  - 0x00846191: je -> 0x00846193 (jcc_false) | ctx: 0x0084618a: mov edi, dword ptr [ebp + 0x14] ; 0x0084618d: mov eax, dword ptr [ecx] ; 0x0084618f: cmp eax, ecx ; 0x00846191: je 0x8461ae
  - 0x0084614f: je -> 0x00846160 (jcc_true) | ctx: 0x00846148: mov edx, dword ptr [ebx + 0x34] ; 0x0084614b: mov eax, dword ptr [edx] ; 0x0084614d: cmp eax, edx ; 0x0084614f: je 0x846160
  - 0x0084614f: je -> 0x00846151 (jcc_false) | ctx: 0x00846148: mov edx, dword ptr [ebx + 0x34] ; 0x0084614b: mov eax, dword ptr [edx] ; 0x0084614d: cmp eax, edx ; 0x0084614f: je 0x846160
  - 0x008461b5: je -> 0x008461ce (jcc_true) | ctx: 0x008461ae: mov ecx, dword ptr [ebx + 0x3c] ; 0x008461b1: mov eax, dword ptr [ecx] ; 0x008461b3: cmp eax, ecx ; 0x008461b5: je 0x8461ce
  - 0x008461b5: je -> 0x008461b7 (jcc_false) | ctx: 0x008461ae: mov ecx, dword ptr [ebx + 0x3c] ; 0x008461b1: mov eax, dword ptr [ecx] ; 0x008461b3: cmp eax, ecx ; 0x008461b5: je 0x8461ce
  - 0x0084619b: je -> 0x008461a5 (jcc_true) | ctx: 0x00846193: mov edx, dword ptr [edi] ; 0x00846195: mov esi, dword ptr [eax + 8] ; 0x00846198: cmp dword ptr [esi + 0xc], edx ; 0x0084619b: je 0x8461a5
  - 0x0084619b: je -> 0x0084619d (jcc_false) | ctx: 0x00846193: mov edx, dword ptr [edi] ; 0x00846195: mov esi, dword ptr [eax + 8] ; 0x00846198: cmp dword ptr [esi + 0xc], edx ; 0x0084619b: je 0x8461a5
  - 0x00846164: jne -> 0x00846217 (jcc_true) | ctx: 0x00846160: xor edi, edi ; 0x00846162: test edi, edi ; 0x00846164: jne 0x846217
  - 0x00846164: jne -> 0x0084616a (jcc_false) | ctx: 0x00846160: xor edi, edi ; 0x00846162: test edi, edi ; 0x00846164: jne 0x846217
  - 0x00846158: je -> 0x00846183 (jcc_true) | ctx: 0x00846151: mov ecx, dword ptr [eax + 8] ; 0x00846154: cmp si, word ptr [ecx + 0x30] ; 0x00846158: je 0x846183
  - 0x00846158: je -> 0x0084615a (jcc_false) | ctx: 0x00846151: mov ecx, dword ptr [eax + 8] ; 0x00846154: cmp si, word ptr [ecx + 0x30] ; 0x00846158: je 0x846183
  - 0x008461eb: je -> 0x008462d4 (jcc_true) | ctx: 0x008461e5: push edx ; 0x008461e6: call dword ptr [eax + 0x50] ; 0x008461e9: test edi, edi ; 0x008461eb: je 0x8462d4
  - 0x008461eb: je -> 0x008461f1 (jcc_false) | ctx: 0x008461e5: push edx ; 0x008461e6: call dword ptr [eax + 0x50] ; 0x008461e9: test edi, edi ; 0x008461eb: je 0x8462d4
  - 0x008461c6: je -> 0x00846211 (jcc_true) | ctx: 0x008461b9: nop dword ptr [eax] ; 0x008461c0: mov esi, dword ptr [eax + 8] ; 0x008461c3: cmp dword ptr [esi + 0xc], edx ; 0x008461c6: je 0x846211
  - 0x008461c6: je -> 0x008461c8 (jcc_false) | ctx: 0x008461b9: nop dword ptr [eax] ; 0x008461c0: mov esi, dword ptr [eax + 8] ; 0x008461c3: cmp dword ptr [esi + 0xc], edx ; 0x008461c6: je 0x846211
  - 0x008461a9: jne -> 0x00846217 (jcc_true) | ctx: 0x008461a5: mov edi, esi ; 0x008461a7: test edi, edi ; 0x008461a9: jne 0x846217
  - 0x008461a9: jne -> 0x008461ab (jcc_false) | ctx: 0x008461a5: mov edi, esi ; 0x008461a7: test edi, edi ; 0x008461a9: jne 0x846217
  - 0x008461a1: jne -> 0x00846195 (jcc_true) | ctx: 0x0084619d: mov eax, dword ptr [eax] ; 0x0084619f: cmp eax, ecx ; 0x008461a1: jne 0x846195
  - 0x008461a1: jne -> 0x008461a3 (jcc_false) | ctx: 0x0084619d: mov eax, dword ptr [eax] ; 0x0084619f: cmp eax, ecx ; 0x008461a1: jne 0x846195
  - 0x0084621c: je -> 0x00846222 (jcc_true) | ctx: 0x00846217: mov eax, dword ptr [edi + 0x1c] ; 0x0084621a: test eax, eax ; 0x0084621c: je 0x846222
  - 0x0084621c: je -> 0x0084621e (jcc_false) | ctx: 0x00846217: mov eax, dword ptr [edi + 0x1c] ; 0x0084621a: test eax, eax ; 0x0084621c: je 0x846222
  - 0x0084617e: jmp -> 0x00846213 (jmp) | ctx: 0x00846176: push eax ; 0x00846177: call 0x849f40 ; 0x0084617c: mov edi, eax ; 0x0084617e: jmp 0x846213
  - 0x00846185: jmp -> 0x00846162 (jmp) | ctx: 0x00846183: mov edi, ecx ; 0x00846185: jmp 0x846162
  - 0x0084615e: jne -> 0x00846151 (jcc_true) | ctx: 0x0084615a: mov eax, dword ptr [eax] ; 0x0084615c: cmp eax, edx ; 0x0084615e: jne 0x846151
  - 0x0084615e: jne -> 0x00846160 (jcc_false) | ctx: 0x0084615a: mov eax, dword ptr [eax] ; 0x0084615c: cmp eax, edx ; 0x0084615e: jne 0x846151
  - 0x008461f5: jne -> 0x008462d4 (jcc_true) | ctx: 0x008461f1: cmp dword ptr [edi + 0x1c], 0 ; 0x008461f5: jne 0x8462d4
  - 0x008461f5: jne -> 0x008461fb (jcc_false) | ctx: 0x008461f1: cmp dword ptr [edi + 0x1c], 0 ; 0x008461f5: jne 0x8462d4
  - 0x00846215: je -> 0x008461d0 (jcc_true) | ctx: 0x00846211: mov edi, esi ; 0x00846213: test edi, edi ; 0x00846215: je 0x8461d0
  - 0x00846215: je -> 0x00846217 (jcc_false) | ctx: 0x00846211: mov edi, esi ; 0x00846213: test edi, edi ; 0x00846215: je 0x8461d0
  - 0x008461cc: jne -> 0x008461c0 (jcc_true) | ctx: 0x008461c8: mov eax, dword ptr [eax] ; 0x008461ca: cmp eax, ecx ; 0x008461cc: jne 0x8461c0
  - 0x008461cc: jne -> 0x008461ce (jcc_false) | ctx: 0x008461c8: mov eax, dword ptr [eax] ; 0x008461ca: cmp eax, ecx ; 0x008461cc: jne 0x8461c0
  - 0x008461b5: je -> 0x008461ce (jcc_true) | ctx: 0x008461ae: mov ecx, dword ptr [ebx + 0x3c] ; 0x008461b1: mov eax, dword ptr [ecx] ; 0x008461b3: cmp eax, ecx ; 0x008461b5: je 0x8461ce
  - 0x008461b5: je -> 0x008461b7 (jcc_false) | ctx: 0x008461ae: mov ecx, dword ptr [ebx + 0x3c] ; 0x008461b1: mov eax, dword ptr [ecx] ; 0x008461b3: cmp eax, ecx ; 0x008461b5: je 0x8461ce
  - 0x0084619b: je -> 0x008461a5 (jcc_true) | ctx: 0x00846195: mov esi, dword ptr [eax + 8] ; 0x00846198: cmp dword ptr [esi + 0xc], edx ; 0x0084619b: je 0x8461a5
  - 0x0084619b: je -> 0x0084619d (jcc_false) | ctx: 0x00846195: mov esi, dword ptr [eax + 8] ; 0x00846198: cmp dword ptr [esi + 0xc], edx ; 0x0084619b: je 0x8461a5
  - 0x008461a3: jmp -> 0x008461ae (jmp) | ctx: 0x008461a3: jmp 0x8461ae
  - 0x0084622f: je -> 0x008461d0 (jcc_true) | ctx: 0x00846227: push esi ; 0x00846228: call 0x84a1d0 ; 0x0084622d: test eax, eax ; 0x0084622f: je 0x8461d0
  - 0x0084622f: je -> 0x00846231 (jcc_false) | ctx: 0x00846227: push esi ; 0x00846228: call 0x84a1d0 ; 0x0084622d: test eax, eax ; 0x0084622f: je 0x8461d0
  - 0x0084622f: je -> 0x008461d0 (jcc_true) | ctx: 0x00846227: push esi ; 0x00846228: call 0x84a1d0 ; 0x0084622d: test eax, eax ; 0x0084622f: je 0x8461d0
  - 0x0084622f: je -> 0x00846231 (jcc_false) | ctx: 0x00846227: push esi ; 0x00846228: call 0x84a1d0 ; 0x0084622d: test eax, eax ; 0x0084622f: je 0x8461d0
  - 0x00846215: je -> 0x008461d0 (jcc_true) | ctx: 0x00846213: test edi, edi ; 0x00846215: je 0x8461d0
  - 0x00846215: je -> 0x00846217 (jcc_false) | ctx: 0x00846213: test edi, edi ; 0x00846215: je 0x8461d0
  - 0x00846164: jne -> 0x00846217 (jcc_true) | ctx: 0x00846162: test edi, edi ; 0x00846164: jne 0x846217
  - 0x00846164: jne -> 0x0084616a (jcc_false) | ctx: 0x00846162: test edi, edi ; 0x00846164: jne 0x846217
  - 0x00846202: je -> 0x00846270 (jcc_true) | ctx: 0x008461fb: mov ecx, dword ptr [ebx + 0x34] ; 0x008461fe: mov eax, dword ptr [ecx] ; 0x00846200: cmp eax, ecx ; 0x00846202: je 0x846270
  - 0x00846202: je -> 0x00846204 (jcc_false) | ctx: 0x008461fb: mov ecx, dword ptr [ebx + 0x34] ; 0x008461fe: mov eax, dword ptr [ecx] ; 0x00846200: cmp eax, ecx ; 0x00846202: je 0x846270
  - 0x008461eb: je -> 0x008462d4 (jcc_true) | ctx: 0x008461e5: push edx ; 0x008461e6: call dword ptr [eax + 0x50] ; 0x008461e9: test edi, edi ; 0x008461eb: je 0x8462d4
  - 0x008461eb: je -> 0x008461f1 (jcc_false) | ctx: 0x008461e5: push edx ; 0x008461e6: call dword ptr [eax + 0x50] ; 0x008461e9: test edi, edi ; 0x008461eb: je 0x8462d4
  - 0x008461c6: je -> 0x00846211 (jcc_true) | ctx: 0x008461c0: mov esi, dword ptr [eax + 8] ; 0x008461c3: cmp dword ptr [esi + 0xc], edx ; 0x008461c6: je 0x846211
  - 0x008461c6: je -> 0x008461c8 (jcc_false) | ctx: 0x008461c0: mov esi, dword ptr [eax + 8] ; 0x008461c3: cmp dword ptr [esi + 0xc], edx ; 0x008461c6: je 0x846211
  - 0x00846238: je -> 0x008461d0 (jcc_true) | ctx: 0x00846231: dec eax ; 0x00846232: cmp dword ptr [esi], -1 ; 0x00846235: mov dword ptr [ebp + 0xc], eax ; 0x00846238: je 0x8461d0
  - 0x00846238: je -> 0x0084623a (jcc_false) | ctx: 0x00846231: dec eax ; 0x00846232: cmp dword ptr [esi], -1 ; 0x00846235: mov dword ptr [ebp + 0xc], eax ; 0x00846238: je 0x8461d0
  - 0x0084627a: je -> 0x0084628b (jcc_true) | ctx: 0x00846273: lea esi, [ebx + 0x3c] ; 0x00846276: mov eax, dword ptr [ecx] ; 0x00846278: cmp eax, ecx ; 0x0084627a: je 0x84628b
  - 0x0084627a: je -> 0x0084627c (jcc_false) | ctx: 0x00846273: lea esi, [ebx + 0x3c] ; 0x00846276: mov eax, dword ptr [ecx] ; 0x00846278: cmp eax, ecx ; 0x0084627a: je 0x84628b
  - 0x00846207: je -> 0x00846255 (jcc_true) | ctx: 0x00846204: cmp dword ptr [eax + 8], edi ; 0x00846207: je 0x846255
  - 0x00846207: je -> 0x00846209 (jcc_false) | ctx: 0x00846204: cmp dword ptr [eax + 8], edi ; 0x00846207: je 0x846255
  - 0x00846250: jmp -> 0x008461d0 (jmp) | ctx: 0x00846247: mov eax, dword ptr [ebp - 8] ; 0x0084624a: mov ecx, dword ptr [ebp + 0xc] ; 0x0084624d: mov dword ptr [eax + 0x14], ecx ; 0x00846250: jmp 0x8461d0
  - 0x008462aa: je -> 0x008462b6 (jcc_true) | ctx: 0x008462a2: mov eax, dword ptr [ebp + 0x20] ; 0x008462a5: mov dword ptr [edi + 0x2c], edx ; 0x008462a8: cmp ecx, eax ; 0x008462aa: je 0x8462b6
  - 0x008462aa: je -> 0x008462ac (jcc_false) | ctx: 0x008462a2: mov eax, dword ptr [ebp + 0x20] ; 0x008462a5: mov dword ptr [edi + 0x2c], edx ; 0x008462a8: cmp ecx, eax ; 0x008462aa: je 0x8462b6
  - 0x00846283: je -> 0x008462ed (jcc_true) | ctx: 0x0084627c: nop dword ptr [eax] ; 0x00846280: cmp edi, dword ptr [eax + 8] ; 0x00846283: je 0x8462ed
  - 0x00846283: je -> 0x00846285 (jcc_false) | ctx: 0x0084627c: nop dword ptr [eax] ; 0x00846280: cmp edi, dword ptr [eax + 8] ; 0x00846283: je 0x8462ed
  - 0x0084627a: je -> 0x0084628b (jcc_true) | ctx: 0x00846273: lea esi, [ebx + 0x3c] ; 0x00846276: mov eax, dword ptr [ecx] ; 0x00846278: cmp eax, ecx ; 0x0084627a: je 0x84628b
  - 0x0084627a: je -> 0x0084627c (jcc_false) | ctx: 0x00846273: lea esi, [ebx + 0x3c] ; 0x00846276: mov eax, dword ptr [ecx] ; 0x00846278: cmp eax, ecx ; 0x0084627a: je 0x84628b
  - 0x0084620d: jne -> 0x00846204 (jcc_true) | ctx: 0x00846209: mov eax, dword ptr [eax] ; 0x0084620b: cmp eax, ecx ; 0x0084620d: jne 0x846204
  - 0x0084620d: jne -> 0x0084620f (jcc_false) | ctx: 0x00846209: mov eax, dword ptr [eax] ; 0x0084620b: cmp eax, ecx ; 0x0084620d: jne 0x846204
  - 0x008462f1: je -> 0x0084628b (jcc_true) | ctx: 0x008462ed: cmp dword ptr [eax + 8], 0 ; 0x008462f1: je 0x84628b
  - 0x008462f1: je -> 0x008462f3 (jcc_false) | ctx: 0x008462ed: cmp dword ptr [eax + 8], 0 ; 0x008462f1: je 0x84628b
  - 0x00846289: jne -> 0x00846280 (jcc_true) | ctx: 0x00846285: mov eax, dword ptr [eax] ; 0x00846287: cmp eax, ecx ; 0x00846289: jne 0x846280
  - 0x00846289: jne -> 0x0084628b (jcc_false) | ctx: 0x00846285: mov eax, dword ptr [eax] ; 0x00846287: cmp eax, ecx ; 0x00846289: jne 0x846280
  - 0x0084620f: jmp -> 0x00846270 (jmp) | ctx: 0x0084620f: jmp 0x846270
  - 0x00846283: je -> 0x008462ed (jcc_true) | ctx: 0x00846280: cmp edi, dword ptr [eax + 8] ; 0x00846283: je 0x8462ed
  - 0x00846283: je -> 0x00846285 (jcc_false) | ctx: 0x00846280: cmp edi, dword ptr [eax + 8] ; 0x00846283: je 0x8462ed

### 0x00846363
- blocks=7, insns=58, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00846390)
- branch points:
  - 0x0084636b: jne -> 0x008463cb (jcc_true) | ctx: 0x00846364: mov esi, ecx ; 0x00846366: mov al, byte ptr [esi + 6] ; 0x00846369: test al, 1 ; 0x0084636b: jne 0x8463cb
  - 0x0084636b: jne -> 0x0084636d (jcc_false) | ctx: 0x00846364: mov esi, ecx ; 0x00846366: mov al, byte ptr [esi + 6] ; 0x00846369: test al, 1 ; 0x0084636b: jne 0x8463cb
  - 0x00846389: je -> 0x00846395 (jcc_true) | ctx: 0x0084637a: mov dword ptr [esi + 0x1e0], 3 ; 0x00846384: mov byte ptr [esi + 6], al ; 0x00846387: cmp ecx, edi ; 0x00846389: je 0x846395
  - 0x00846389: je -> 0x0084638b (jcc_false) | ctx: 0x0084637a: mov dword ptr [esi + 0x1e0], 3 ; 0x00846384: mov byte ptr [esi + 6], al ; 0x00846387: cmp ecx, edi ; 0x00846389: je 0x846395
  - 0x008463a8: je -> 0x008463b3 (jcc_true) | ctx: 0x0084639a: mov dword ptr [esi + 0xd8], eax ; 0x008463a0: mov eax, dword ptr [esi + 0x1f4] ; 0x008463a6: test eax, eax ; 0x008463a8: je 0x8463b3
  - 0x008463a8: je -> 0x008463aa (jcc_false) | ctx: 0x0084639a: mov dword ptr [esi + 0xd8], eax ; 0x008463a0: mov eax, dword ptr [esi + 0x1f4] ; 0x008463a6: test eax, eax ; 0x008463a8: je 0x8463b3
  - 0x008463a8: je -> 0x008463b3 (jcc_true) | ctx: 0x0084639a: mov dword ptr [esi + 0xd8], eax ; 0x008463a0: mov eax, dword ptr [esi + 0x1f4] ; 0x008463a6: test eax, eax ; 0x008463a8: je 0x8463b3
  - 0x008463a8: je -> 0x008463aa (jcc_false) | ctx: 0x0084639a: mov dword ptr [esi + 0xd8], eax ; 0x008463a0: mov eax, dword ptr [esi + 0x1f4] ; 0x008463a6: test eax, eax ; 0x008463a8: je 0x8463b3

### 0x0084ae63
- blocks=3, insns=35, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0084ae99)
- branch points:
  - 0x0084ae92: je -> 0x0084ae9e (jcc_true) | ctx: 0x0084ae8a: mov byte ptr [edi + 0x29], al ; 0x0084ae8d: mov eax, dword ptr [ebp + 0x18] ; 0x0084ae90: cmp ecx, eax ; 0x0084ae92: je 0x84ae9e
  - 0x0084ae92: je -> 0x0084ae94 (jcc_false) | ctx: 0x0084ae8a: mov byte ptr [edi + 0x29], al ; 0x0084ae8d: mov eax, dword ptr [ebp + 0x18] ; 0x0084ae90: cmp ecx, eax ; 0x0084ae92: je 0x84ae9e

### 0x0084b9d0
- blocks=10, insns=67, edges=17, jcc=6, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0084ba46)
- branch points:
  - 0x0084b9f8: je -> 0x0084ba08 (jcc_true) | ctx: 0x0084b9ef: mov esi, dword ptr [eax + 4] ; 0x0084b9f2: mov eax, dword ptr [esi + 0x3c] ; 0x0084b9f5: cmp eax, 3 ; 0x0084b9f8: je 0x84ba08
  - 0x0084b9f8: je -> 0x0084b9fa (jcc_false) | ctx: 0x0084b9ef: mov esi, dword ptr [eax + 4] ; 0x0084b9f2: mov eax, dword ptr [esi + 0x3c] ; 0x0084b9f5: cmp eax, 3 ; 0x0084b9f8: je 0x84ba08
  - 0x0084ba1b: jne -> 0x0084ba5b (jcc_true) | ctx: 0x0084ba0f: and byte ptr [esi + 0x4a], 0xfe ; 0x0084ba13: and byte ptr [esi + 0x49], 0x17 ; 0x0084ba17: test byte ptr [esi + 0x4a], 6 ; 0x0084ba1b: jne 0x84ba5b
  - 0x0084ba1b: jne -> 0x0084ba1d (jcc_false) | ctx: 0x0084ba0f: and byte ptr [esi + 0x4a], 0xfe ; 0x0084ba13: and byte ptr [esi + 0x49], 0x17 ; 0x0084ba17: test byte ptr [esi + 0x4a], 6 ; 0x0084ba1b: jne 0x84ba5b
  - 0x0084b9fd: je -> 0x0084ba08 (jcc_true) | ctx: 0x0084b9fa: cmp eax, 6 ; 0x0084b9fd: je 0x84ba08
  - 0x0084b9fd: je -> 0x0084b9ff (jcc_false) | ctx: 0x0084b9fa: cmp eax, 6 ; 0x0084b9fd: je 0x84ba08
  - 0x0084ba21: jne -> 0x0084ba5b (jcc_true) | ctx: 0x0084ba1d: test byte ptr [esi + 0x48], 4 ; 0x0084ba21: jne 0x84ba5b
  - 0x0084ba21: jne -> 0x0084ba23 (jcc_false) | ctx: 0x0084ba1d: test byte ptr [esi + 0x48], 4 ; 0x0084ba21: jne 0x84ba5b
  - 0x0084ba06: jmp -> 0x0084ba0f (jmp) | ctx: 0x0084b9ff: mov dword ptr [esi + 0x3c], 4 ; 0x0084ba06: jmp 0x84ba0f
  - 0x0084ba3f: je -> 0x0084ba4b (jcc_true) | ctx: 0x0084ba33: mov dword ptr [ebp - 4], 0 ; 0x0084ba3a: lea eax, [ebp - 0x24] ; 0x0084ba3d: cmp ecx, eax ; 0x0084ba3f: je 0x84ba4b
  - 0x0084ba3f: je -> 0x0084ba41 (jcc_false) | ctx: 0x0084ba33: mov dword ptr [ebp - 4], 0 ; 0x0084ba3a: lea eax, [ebp - 0x24] ; 0x0084ba3d: cmp ecx, eax ; 0x0084ba3f: je 0x84ba4b
  - 0x0084ba1b: jne -> 0x0084ba5b (jcc_true) | ctx: 0x0084ba0f: and byte ptr [esi + 0x4a], 0xfe ; 0x0084ba13: and byte ptr [esi + 0x49], 0x17 ; 0x0084ba17: test byte ptr [esi + 0x4a], 6 ; 0x0084ba1b: jne 0x84ba5b
  - 0x0084ba1b: jne -> 0x0084ba1d (jcc_false) | ctx: 0x0084ba0f: and byte ptr [esi + 0x4a], 0xfe ; 0x0084ba13: and byte ptr [esi + 0x49], 0x17 ; 0x0084ba17: test byte ptr [esi + 0x4a], 6 ; 0x0084ba1b: jne 0x84ba5b

### 0x00852c50
- blocks=47, insns=564, edges=96, jcc=30, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00852d59)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00852e55)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00852f4a)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0085303a)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00853121)
- branch points:
  - 0x00852c75: jne -> 0x00853141 (jcc_true) | ctx: 0x00852c6f: push edi ; 0x00852c70: mov al, byte ptr [ebx + 5] ; 0x00852c73: test al, 0x10 ; 0x00852c75: jne 0x853141
  - 0x00852c75: jne -> 0x00852c7b (jcc_false) | ctx: 0x00852c6f: push edi ; 0x00852c70: mov al, byte ptr [ebx + 5] ; 0x00852c73: test al, 0x10 ; 0x00852c75: jne 0x853141
  - 0x00852c8c: jne -> 0x00852d84 (jcc_true) | ctx: 0x00852c7d: mov dword ptr [ebx + 0x1e0], 3 ; 0x00852c87: mov byte ptr [ebx + 5], al ; 0x00852c8a: test al, 1 ; 0x00852c8c: jne 0x852d84
  - 0x00852c8c: jne -> 0x00852c92 (jcc_false) | ctx: 0x00852c7d: mov dword ptr [ebx + 0x1e0], 3 ; 0x00852c87: mov byte ptr [ebx + 5], al ; 0x00852c8a: test al, 1 ; 0x00852c8c: jne 0x852d84
  - 0x00852d88: je -> 0x00852e79 (jcc_true) | ctx: 0x00852d84: cmp dword ptr [ebx + 0x48], -1 ; 0x00852d88: je 0x852e79
  - 0x00852d88: je -> 0x00852d8e (jcc_false) | ctx: 0x00852d84: cmp dword ptr [ebx + 0x48], -1 ; 0x00852d88: je 0x852e79
  - 0x00852cb6: je -> 0x00852d12 (jcc_true) | ctx: 0x00852cae: mov dword ptr [ebp - 0x10], edi ; 0x00852cb1: mov dword ptr [ebp - 0x10], edi ; 0x00852cb4: test edi, edi ; 0x00852cb6: je 0x852d12
  - 0x00852cb6: je -> 0x00852cb8 (jcc_false) | ctx: 0x00852cae: mov dword ptr [ebp - 0x10], edi ; 0x00852cb1: mov dword ptr [ebp - 0x10], edi ; 0x00852cb4: test edi, edi ; 0x00852cb6: je 0x852d12
  - 0x00852e80: je -> 0x00852f6c (jcc_true) | ctx: 0x00852e79: mov esi, dword ptr [ebp + 0xc] ; 0x00852e7c: cmp dword ptr [ebx + 0x4c], -1 ; 0x00852e80: je 0x852f6c
  - 0x00852e80: je -> 0x00852e86 (jcc_false) | ctx: 0x00852e79: mov esi, dword ptr [ebp + 0xc] ; 0x00852e7c: cmp dword ptr [ebx + 0x4c], -1 ; 0x00852e80: je 0x852f6c
  - 0x00852db2: je -> 0x00852e0e (jcc_true) | ctx: 0x00852daa: mov dword ptr [ebp - 0x10], edi ; 0x00852dad: mov dword ptr [ebp - 0x10], edi ; 0x00852db0: test edi, edi ; 0x00852db2: je 0x852e0e
  - 0x00852db2: je -> 0x00852db4 (jcc_false) | ctx: 0x00852daa: mov dword ptr [ebp - 0x10], edi ; 0x00852dad: mov dword ptr [ebp - 0x10], edi ; 0x00852db0: test edi, edi ; 0x00852db2: je 0x852e0e
  - 0x00852d52: je -> 0x00852d5e (jcc_true) | ctx: 0x00852d46: mov dword ptr [ebp - 4], 0xffffffff ; 0x00852d4d: mov dword ptr [edi + 0x20], esi ; 0x00852d50: cmp ecx, eax ; 0x00852d52: je 0x852d5e
  - 0x00852d52: je -> 0x00852d54 (jcc_false) | ctx: 0x00852d46: mov dword ptr [ebp - 4], 0xffffffff ; 0x00852d4d: mov dword ptr [edi + 0x20], esi ; 0x00852d50: cmp ecx, eax ; 0x00852d52: je 0x852d5e
  - 0x00852d02: jb -> 0x00852d06 (jcc_true) | ctx: 0x00852cf0: mov dword ptr [eax + 0x14], 0xf ; 0x00852cf7: mov dword ptr [eax + 0x10], 0 ; 0x00852cfe: cmp dword ptr [eax + 0x14], 0x10 ; 0x00852d02: jb 0x852d06
  - 0x00852d02: jb -> 0x00852d04 (jcc_false) | ctx: 0x00852cf0: mov dword ptr [eax + 0x14], 0xf ; 0x00852cf7: mov dword ptr [eax + 0x10], 0 ; 0x00852cfe: cmp dword ptr [eax + 0x14], 0x10 ; 0x00852d02: jb 0x852d06
  - 0x00852f70: je -> 0x0085305a (jcc_true) | ctx: 0x00852f6c: cmp dword ptr [ebx + 0x50], -1 ; 0x00852f70: je 0x85305a
  - 0x00852f70: je -> 0x00852f76 (jcc_false) | ctx: 0x00852f6c: cmp dword ptr [ebx + 0x50], -1 ; 0x00852f70: je 0x85305a
  - 0x00852eaa: je -> 0x00852f06 (jcc_true) | ctx: 0x00852ea2: mov dword ptr [ebp - 0x10], edi ; 0x00852ea5: mov dword ptr [ebp - 0x10], edi ; 0x00852ea8: test edi, edi ; 0x00852eaa: je 0x852f06
  - 0x00852eaa: je -> 0x00852eac (jcc_false) | ctx: 0x00852ea2: mov dword ptr [ebp - 0x10], edi ; 0x00852ea5: mov dword ptr [ebp - 0x10], edi ; 0x00852ea8: test edi, edi ; 0x00852eaa: je 0x852f06
  - 0x00852e4e: je -> 0x00852e5a (jcc_true) | ctx: 0x00852e42: mov dword ptr [ebp - 4], 0xffffffff ; 0x00852e49: mov dword ptr [edi + 0x20], esi ; 0x00852e4c: cmp ecx, eax ; 0x00852e4e: je 0x852e5a
  - 0x00852e4e: je -> 0x00852e50 (jcc_false) | ctx: 0x00852e42: mov dword ptr [ebp - 4], 0xffffffff ; 0x00852e49: mov dword ptr [edi + 0x20], esi ; 0x00852e4c: cmp ecx, eax ; 0x00852e4e: je 0x852e5a
  - 0x00852dfe: jb -> 0x00852e02 (jcc_true) | ctx: 0x00852dec: mov dword ptr [eax + 0x14], 0xf ; 0x00852df3: mov dword ptr [eax + 0x10], 0 ; 0x00852dfa: cmp dword ptr [eax + 0x14], 0x10 ; 0x00852dfe: jb 0x852e02
  - 0x00852dfe: jb -> 0x00852e00 (jcc_false) | ctx: 0x00852dec: mov dword ptr [eax + 0x14], 0xf ; 0x00852df3: mov dword ptr [eax + 0x10], 0 ; 0x00852dfa: cmp dword ptr [eax + 0x14], 0x10 ; 0x00852dfe: jb 0x852e02
  - 0x00852d7f: jmp -> 0x00853141 (jmp) | ctx: 0x00852d7a: push ecx ; 0x00852d7b: push eax ; 0x00852d7c: call dword ptr [edx + 0x1c] ; 0x00852d7f: jmp 0x853141
  - 0x00852d7f: jmp -> 0x00853141 (jmp) | ctx: 0x00852d7a: push ecx ; 0x00852d7b: push eax ; 0x00852d7c: call dword ptr [edx + 0x1c] ; 0x00852d7f: jmp 0x853141
  - 0x00852d10: jmp -> 0x00852d14 (jmp) | ctx: 0x00852d06: mov byte ptr [eax], 0 ; 0x00852d09: mov dword ptr [edi + 0x40], 0xffffffff ; 0x00852d10: jmp 0x852d14
  - 0x00852d10: jmp -> 0x00852d14 (jmp) | ctx: 0x00852d04: mov eax, dword ptr [eax] ; 0x00852d06: mov byte ptr [eax], 0 ; 0x00852d09: mov dword ptr [edi + 0x40], 0xffffffff ; 0x00852d10: jmp 0x852d14
  - 0x0085307e: je -> 0x008530da (jcc_true) | ctx: 0x00853076: mov dword ptr [ebp - 0x10], edi ; 0x00853079: mov dword ptr [ebp - 0x10], edi ; 0x0085307c: test edi, edi ; 0x0085307e: je 0x8530da
  - 0x0085307e: je -> 0x00853080 (jcc_false) | ctx: 0x00853076: mov dword ptr [ebp - 0x10], edi ; 0x00853079: mov dword ptr [ebp - 0x10], edi ; 0x0085307c: test edi, edi ; 0x0085307e: je 0x8530da
  - 0x00852f9a: je -> 0x00852ff6 (jcc_true) | ctx: 0x00852f92: mov dword ptr [ebp - 0x10], edi ; 0x00852f95: mov dword ptr [ebp - 0x10], edi ; 0x00852f98: test edi, edi ; 0x00852f9a: je 0x852ff6
  - 0x00852f9a: je -> 0x00852f9c (jcc_false) | ctx: 0x00852f92: mov dword ptr [ebp - 0x10], edi ; 0x00852f95: mov dword ptr [ebp - 0x10], edi ; 0x00852f98: test edi, edi ; 0x00852f9a: je 0x852ff6
  - 0x00852f43: je -> 0x00852f4f (jcc_true) | ctx: 0x00852f37: mov dword ptr [ebp - 4], 0xffffffff ; 0x00852f3e: mov dword ptr [edi + 0x20], esi ; 0x00852f41: cmp ecx, eax ; 0x00852f43: je 0x852f4f
  - 0x00852f43: je -> 0x00852f45 (jcc_false) | ctx: 0x00852f37: mov dword ptr [ebp - 4], 0xffffffff ; 0x00852f3e: mov dword ptr [edi + 0x20], esi ; 0x00852f41: cmp ecx, eax ; 0x00852f43: je 0x852f4f
  - 0x00852ef6: jb -> 0x00852efa (jcc_true) | ctx: 0x00852ee4: mov dword ptr [eax + 0x14], 0xf ; 0x00852eeb: mov dword ptr [eax + 0x10], 0 ; 0x00852ef2: cmp dword ptr [eax + 0x14], 0x10 ; 0x00852ef6: jb 0x852efa
  - 0x00852ef6: jb -> 0x00852ef8 (jcc_false) | ctx: 0x00852ee4: mov dword ptr [eax + 0x14], 0xf ; 0x00852eeb: mov dword ptr [eax + 0x10], 0 ; 0x00852ef2: cmp dword ptr [eax + 0x14], 0x10 ; 0x00852ef6: jb 0x852efa
  - 0x00852e77: jmp -> 0x00852e7c (jmp) | ctx: 0x00852e71: push ecx ; 0x00852e72: mov ecx, esi ; 0x00852e74: call dword ptr [eax + 0x1c] ; 0x00852e77: jmp 0x852e7c
  - 0x00852e77: jmp -> 0x00852e7c (jmp) | ctx: 0x00852e71: push ecx ; 0x00852e72: mov ecx, esi ; 0x00852e74: call dword ptr [eax + 0x1c] ; 0x00852e77: jmp 0x852e7c
  - 0x00852e0c: jmp -> 0x00852e10 (jmp) | ctx: 0x00852e02: mov byte ptr [eax], 0 ; 0x00852e05: mov dword ptr [edi + 0x40], 0xffffffff ; 0x00852e0c: jmp 0x852e10
  - 0x00852e0c: jmp -> 0x00852e10 (jmp) | ctx: 0x00852e00: mov eax, dword ptr [eax] ; 0x00852e02: mov byte ptr [eax], 0 ; 0x00852e05: mov dword ptr [edi + 0x40], 0xffffffff ; 0x00852e0c: jmp 0x852e10
  - 0x00852d52: je -> 0x00852d5e (jcc_true) | ctx: 0x00852d46: mov dword ptr [ebp - 4], 0xffffffff ; 0x00852d4d: mov dword ptr [edi + 0x20], esi ; 0x00852d50: cmp ecx, eax ; 0x00852d52: je 0x852d5e
  - 0x00852d52: je -> 0x00852d54 (jcc_false) | ctx: 0x00852d46: mov dword ptr [ebp - 4], 0xffffffff ; 0x00852d4d: mov dword ptr [edi + 0x20], esi ; 0x00852d50: cmp ecx, eax ; 0x00852d52: je 0x852d5e
  - 0x0085311a: je -> 0x00853126 (jcc_true) | ctx: 0x0085310e: mov dword ptr [ebp - 4], 0xffffffff ; 0x00853115: mov dword ptr [edi + 0x20], esi ; 0x00853118: cmp ecx, eax ; 0x0085311a: je 0x853126
  - 0x0085311a: je -> 0x0085311c (jcc_false) | ctx: 0x0085310e: mov dword ptr [ebp - 4], 0xffffffff ; 0x00853115: mov dword ptr [edi + 0x20], esi ; 0x00853118: cmp ecx, eax ; 0x0085311a: je 0x853126
  - 0x008530ca: jb -> 0x008530ce (jcc_true) | ctx: 0x008530b8: mov dword ptr [eax + 0x14], 0xf ; 0x008530bf: mov dword ptr [eax + 0x10], 0 ; 0x008530c6: cmp dword ptr [eax + 0x14], 0x10 ; 0x008530ca: jb 0x8530ce
  - 0x008530ca: jb -> 0x008530cc (jcc_false) | ctx: 0x008530b8: mov dword ptr [eax + 0x14], 0xf ; 0x008530bf: mov dword ptr [eax + 0x10], 0 ; 0x008530c6: cmp dword ptr [eax + 0x14], 0x10 ; 0x008530ca: jb 0x8530ce
  - 0x00853033: je -> 0x0085303f (jcc_true) | ctx: 0x00853027: mov dword ptr [ebp - 4], 0xffffffff ; 0x0085302e: mov dword ptr [edi + 0x20], esi ; 0x00853031: cmp ecx, eax ; 0x00853033: je 0x85303f
  - 0x00853033: je -> 0x00853035 (jcc_false) | ctx: 0x00853027: mov dword ptr [ebp - 4], 0xffffffff ; 0x0085302e: mov dword ptr [edi + 0x20], esi ; 0x00853031: cmp ecx, eax ; 0x00853033: je 0x85303f
  - 0x00852fe6: jb -> 0x00852fea (jcc_true) | ctx: 0x00852fd4: mov dword ptr [eax + 0x14], 0xf ; 0x00852fdb: mov dword ptr [eax + 0x10], 0 ; 0x00852fe2: cmp dword ptr [eax + 0x14], 0x10 ; 0x00852fe6: jb 0x852fea
  - 0x00852fe6: jb -> 0x00852fe8 (jcc_false) | ctx: 0x00852fd4: mov dword ptr [eax + 0x14], 0xf ; 0x00852fdb: mov dword ptr [eax + 0x10], 0 ; 0x00852fe2: cmp dword ptr [eax + 0x14], 0x10 ; 0x00852fe6: jb 0x852fea
  - 0x00852f70: je -> 0x0085305a (jcc_true) | ctx: 0x00852f67: mov ecx, esi ; 0x00852f69: call dword ptr [eax + 0x1c] ; 0x00852f6c: cmp dword ptr [ebx + 0x50], -1 ; 0x00852f70: je 0x85305a
  - 0x00852f70: je -> 0x00852f76 (jcc_false) | ctx: 0x00852f67: mov ecx, esi ; 0x00852f69: call dword ptr [eax + 0x1c] ; 0x00852f6c: cmp dword ptr [ebx + 0x50], -1 ; 0x00852f70: je 0x85305a
  - 0x00852f70: je -> 0x0085305a (jcc_true) | ctx: 0x00852f67: mov ecx, esi ; 0x00852f69: call dword ptr [eax + 0x1c] ; 0x00852f6c: cmp dword ptr [ebx + 0x50], -1 ; 0x00852f70: je 0x85305a
  - 0x00852f70: je -> 0x00852f76 (jcc_false) | ctx: 0x00852f67: mov ecx, esi ; 0x00852f69: call dword ptr [eax + 0x1c] ; 0x00852f6c: cmp dword ptr [ebx + 0x50], -1 ; 0x00852f70: je 0x85305a
  - 0x00852f04: jmp -> 0x00852f08 (jmp) | ctx: 0x00852efa: mov byte ptr [eax], 0 ; 0x00852efd: mov dword ptr [edi + 0x40], 0xffffffff ; 0x00852f04: jmp 0x852f08
  - 0x00852f04: jmp -> 0x00852f08 (jmp) | ctx: 0x00852ef8: mov eax, dword ptr [eax] ; 0x00852efa: mov byte ptr [eax], 0 ; 0x00852efd: mov dword ptr [edi + 0x40], 0xffffffff ; 0x00852f04: jmp 0x852f08
  - 0x00852e80: je -> 0x00852f6c (jcc_true) | ctx: 0x00852e7c: cmp dword ptr [ebx + 0x4c], -1 ; 0x00852e80: je 0x852f6c
  - 0x00852e80: je -> 0x00852e86 (jcc_false) | ctx: 0x00852e7c: cmp dword ptr [ebx + 0x4c], -1 ; 0x00852e80: je 0x852f6c
  - 0x00852e4e: je -> 0x00852e5a (jcc_true) | ctx: 0x00852e42: mov dword ptr [ebp - 4], 0xffffffff ; 0x00852e49: mov dword ptr [edi + 0x20], esi ; 0x00852e4c: cmp ecx, eax ; 0x00852e4e: je 0x852e5a
  - 0x00852e4e: je -> 0x00852e50 (jcc_false) | ctx: 0x00852e42: mov dword ptr [ebp - 4], 0xffffffff ; 0x00852e49: mov dword ptr [edi + 0x20], esi ; 0x00852e4c: cmp ecx, eax ; 0x00852e4e: je 0x852e5a
  - 0x008530d8: jmp -> 0x008530dc (jmp) | ctx: 0x008530ce: mov byte ptr [eax], 0 ; 0x008530d1: mov dword ptr [edi + 0x40], 0xffffffff ; 0x008530d8: jmp 0x8530dc
  - 0x008530d8: jmp -> 0x008530dc (jmp) | ctx: 0x008530cc: mov eax, dword ptr [eax] ; 0x008530ce: mov byte ptr [eax], 0 ; 0x008530d1: mov dword ptr [edi + 0x40], 0xffffffff ; 0x008530d8: jmp 0x8530dc
  - 0x0085307e: je -> 0x008530da (jcc_true) | ctx: 0x00853076: mov dword ptr [ebp - 0x10], edi ; 0x00853079: mov dword ptr [ebp - 0x10], edi ; 0x0085307c: test edi, edi ; 0x0085307e: je 0x8530da
  - 0x0085307e: je -> 0x00853080 (jcc_false) | ctx: 0x00853076: mov dword ptr [ebp - 0x10], edi ; 0x00853079: mov dword ptr [ebp - 0x10], edi ; 0x0085307c: test edi, edi ; 0x0085307e: je 0x8530da
  - 0x0085307e: je -> 0x008530da (jcc_true) | ctx: 0x00853076: mov dword ptr [ebp - 0x10], edi ; 0x00853079: mov dword ptr [ebp - 0x10], edi ; 0x0085307c: test edi, edi ; 0x0085307e: je 0x8530da
  - 0x0085307e: je -> 0x00853080 (jcc_false) | ctx: 0x00853076: mov dword ptr [ebp - 0x10], edi ; 0x00853079: mov dword ptr [ebp - 0x10], edi ; 0x0085307c: test edi, edi ; 0x0085307e: je 0x8530da
  - 0x00852ff4: jmp -> 0x00852ff8 (jmp) | ctx: 0x00852fea: mov byte ptr [eax], 0 ; 0x00852fed: mov dword ptr [edi + 0x40], 0xffffffff ; 0x00852ff4: jmp 0x852ff8
  - 0x00852ff4: jmp -> 0x00852ff8 (jmp) | ctx: 0x00852fe8: mov eax, dword ptr [eax] ; 0x00852fea: mov byte ptr [eax], 0 ; 0x00852fed: mov dword ptr [edi + 0x40], 0xffffffff ; 0x00852ff4: jmp 0x852ff8
  - 0x00852f43: je -> 0x00852f4f (jcc_true) | ctx: 0x00852f37: mov dword ptr [ebp - 4], 0xffffffff ; 0x00852f3e: mov dword ptr [edi + 0x20], esi ; 0x00852f41: cmp ecx, eax ; 0x00852f43: je 0x852f4f
  - 0x00852f43: je -> 0x00852f45 (jcc_false) | ctx: 0x00852f37: mov dword ptr [ebp - 4], 0xffffffff ; 0x00852f3e: mov dword ptr [edi + 0x20], esi ; 0x00852f41: cmp ecx, eax ; 0x00852f43: je 0x852f4f
  - 0x0085311a: je -> 0x00853126 (jcc_true) | ctx: 0x0085310e: mov dword ptr [ebp - 4], 0xffffffff ; 0x00853115: mov dword ptr [edi + 0x20], esi ; 0x00853118: cmp ecx, eax ; 0x0085311a: je 0x853126
  - 0x0085311a: je -> 0x0085311c (jcc_false) | ctx: 0x0085310e: mov dword ptr [ebp - 4], 0xffffffff ; 0x00853115: mov dword ptr [edi + 0x20], esi ; 0x00853118: cmp ecx, eax ; 0x0085311a: je 0x853126
  - 0x00853033: je -> 0x0085303f (jcc_true) | ctx: 0x00853027: mov dword ptr [ebp - 4], 0xffffffff ; 0x0085302e: mov dword ptr [edi + 0x20], esi ; 0x00853031: cmp ecx, eax ; 0x00853033: je 0x85303f
  - 0x00853033: je -> 0x00853035 (jcc_false) | ctx: 0x00853027: mov dword ptr [ebp - 4], 0xffffffff ; 0x0085302e: mov dword ptr [edi + 0x20], esi ; 0x00853031: cmp ecx, eax ; 0x00853033: je 0x85303f

### 0x00854ca0
- blocks=8, insns=138, edges=20, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00854d6b)
- branch points:
  - 0x00854cc1: je -> 0x00854d89 (jcc_true) | ctx: 0x00854cbb: cmp dword ptr [ebp + 0x28], -1 ; 0x00854cbf: push esi ; 0x00854cc0: push edi ; 0x00854cc1: je 0x854d89
  - 0x00854cc1: je -> 0x00854cc7 (jcc_false) | ctx: 0x00854cbb: cmp dword ptr [ebp + 0x28], -1 ; 0x00854cbf: push esi ; 0x00854cc0: push edi ; 0x00854cc1: je 0x854d89
  - 0x00854cec: je -> 0x00854cf9 (jcc_true) | ctx: 0x00854ce0: mov dword ptr [ebp - 0x14], eax ; 0x00854ce3: mov dword ptr [ebp - 4], 0 ; 0x00854cea: test eax, eax ; 0x00854cec: je 0x854cf9
  - 0x00854cec: je -> 0x00854cee (jcc_false) | ctx: 0x00854ce0: mov dword ptr [ebp - 0x14], eax ; 0x00854ce3: mov dword ptr [ebp - 4], 0 ; 0x00854cea: test eax, eax ; 0x00854cec: je 0x854cf9
  - 0x00854d64: je -> 0x00854d70 (jcc_true) | ctx: 0x00854d59: mov eax, dword ptr [ebp + 0x20] ; 0x00854d5c: lea ecx, [edi + 0x124] ; 0x00854d62: cmp ecx, eax ; 0x00854d64: je 0x854d70
  - 0x00854d64: je -> 0x00854d66 (jcc_false) | ctx: 0x00854d59: mov eax, dword ptr [ebp + 0x20] ; 0x00854d5c: lea ecx, [edi + 0x124] ; 0x00854d62: cmp ecx, eax ; 0x00854d64: je 0x854d70
  - 0x00854cf7: jmp -> 0x00854cfb (jmp) | ctx: 0x00854cee: mov ecx, eax ; 0x00854cf0: call 0x836ae0 ; 0x00854cf5: mov edi, eax ; 0x00854cf7: jmp 0x854cfb
  - 0x00854d64: je -> 0x00854d70 (jcc_true) | ctx: 0x00854d59: mov eax, dword ptr [ebp + 0x20] ; 0x00854d5c: lea ecx, [edi + 0x124] ; 0x00854d62: cmp ecx, eax ; 0x00854d64: je 0x854d70
  - 0x00854d64: je -> 0x00854d66 (jcc_false) | ctx: 0x00854d59: mov eax, dword ptr [ebp + 0x20] ; 0x00854d5c: lea ecx, [edi + 0x124] ; 0x00854d62: cmp ecx, eax ; 0x00854d64: je 0x854d70

### 0x00854db0
- blocks=8, insns=132, edges=16, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00854e6a)
- branch points:
  - 0x00854dd1: je -> 0x00854e88 (jcc_true) | ctx: 0x00854dcb: cmp dword ptr [ebp + 0x24], -1 ; 0x00854dcf: push esi ; 0x00854dd0: push edi ; 0x00854dd1: je 0x854e88
  - 0x00854dd1: je -> 0x00854dd7 (jcc_false) | ctx: 0x00854dcb: cmp dword ptr [ebp + 0x24], -1 ; 0x00854dcf: push esi ; 0x00854dd0: push edi ; 0x00854dd1: je 0x854e88
  - 0x00854dfc: je -> 0x00854e09 (jcc_true) | ctx: 0x00854df0: mov dword ptr [ebp - 0x14], eax ; 0x00854df3: mov dword ptr [ebp - 4], 0 ; 0x00854dfa: test eax, eax ; 0x00854dfc: je 0x854e09
  - 0x00854dfc: je -> 0x00854dfe (jcc_false) | ctx: 0x00854df0: mov dword ptr [ebp - 0x14], eax ; 0x00854df3: mov dword ptr [ebp - 4], 0 ; 0x00854dfa: test eax, eax ; 0x00854dfc: je 0x854e09
  - 0x00854e63: je -> 0x00854e6f (jcc_true) | ctx: 0x00854e58: mov dword ptr [edi + 0x108], eax ; 0x00854e5e: mov eax, dword ptr [ebp + 0x1c] ; 0x00854e61: cmp ecx, eax ; 0x00854e63: je 0x854e6f
  - 0x00854e63: je -> 0x00854e65 (jcc_false) | ctx: 0x00854e58: mov dword ptr [edi + 0x108], eax ; 0x00854e5e: mov eax, dword ptr [ebp + 0x1c] ; 0x00854e61: cmp ecx, eax ; 0x00854e63: je 0x854e6f
  - 0x00854e07: jmp -> 0x00854e0b (jmp) | ctx: 0x00854dfe: mov ecx, eax ; 0x00854e00: call 0x836ae0 ; 0x00854e05: mov edi, eax ; 0x00854e07: jmp 0x854e0b
  - 0x00854e63: je -> 0x00854e6f (jcc_true) | ctx: 0x00854e58: mov dword ptr [edi + 0x108], eax ; 0x00854e5e: mov eax, dword ptr [ebp + 0x1c] ; 0x00854e61: cmp ecx, eax ; 0x00854e63: je 0x854e6f
  - 0x00854e63: je -> 0x00854e65 (jcc_false) | ctx: 0x00854e58: mov dword ptr [edi + 0x108], eax ; 0x00854e5e: mov eax, dword ptr [ebp + 0x1c] ; 0x00854e61: cmp ecx, eax ; 0x00854e63: je 0x854e6f

### 0x00856eb6
- blocks=26, insns=241, edges=62, jcc=16, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00856f8e)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00857055)
- branch points:
  - 0x00856ec0: je -> 0x00856ee9 (jcc_true) | ctx: 0x00856eb6: push esi ; 0x00856eb7: mov esi, ecx ; 0x00856eb9: cmp byte ptr [esi + 0x140], 0 ; 0x00856ec0: je 0x856ee9
  - 0x00856ec0: je -> 0x00856ec2 (jcc_false) | ctx: 0x00856eb6: push esi ; 0x00856eb7: mov esi, ecx ; 0x00856eb9: cmp byte ptr [esi + 0x140], 0 ; 0x00856ec0: je 0x856ee9
  - 0x00856f0e: jns -> 0x00856fc9 (jcc_true) | ctx: 0x00856f04: lea ecx, [edi + 0x20] ; 0x00856f07: call 0x61d7f0 ; 0x00856f0c: test eax, eax ; 0x00856f0e: jns 0x856fc9
  - 0x00856f0e: jns -> 0x00856f14 (jcc_false) | ctx: 0x00856f04: lea ecx, [edi + 0x20] ; 0x00856f07: call 0x61d7f0 ; 0x00856f0c: test eax, eax ; 0x00856f0e: jns 0x856fc9
  - 0x00856ee4: jmp -> 0x008570be (jmp) | ctx: 0x00856ed4: mov eax, dword ptr [0xd6b9d4] ; 0x00856ed9: mov dword ptr [esi + 0x14c], eax ; 0x00856edf: call 0x846060 ; 0x00856ee4: jmp 0x8570be
  - 0x00857002: jne -> 0x008570b5 (jcc_true) | ctx: 0x00856ff2: mov byte ptr [ebp + 0xf], 0 ; 0x00856ff6: call 0x99a080 ; 0x00856ffb: cmp ax, word ptr [esi + 0x136] ; 0x00857002: jne 0x8570b5
  - 0x00857002: jne -> 0x00857008 (jcc_false) | ctx: 0x00856ff2: mov byte ptr [ebp + 0xf], 0 ; 0x00856ff6: call 0x99a080 ; 0x00856ffb: cmp ax, word ptr [esi + 0x136] ; 0x00857002: jne 0x8570b5
  - 0x00856f21: jne -> 0x00856f2c (jcc_true) | ctx: 0x00856f14: lea ecx, [edi + 0x20] ; 0x00856f17: call 0x61d7f0 ; 0x00856f1c: cmp eax, 0xfff0be33 ; 0x00856f21: jne 0x856f2c
  - 0x00856f21: jne -> 0x00856f23 (jcc_false) | ctx: 0x00856f14: lea ecx, [edi + 0x20] ; 0x00856f17: call 0x61d7f0 ; 0x00856f1c: cmp eax, 0xfff0be33 ; 0x00856f21: jne 0x856f2c
  - 0x00857015: je -> 0x00857028 (jcc_true) | ctx: 0x00857008: mov ecx, edi ; 0x0085700a: call 0xacbf60 ; 0x0085700f: cmp dword ptr [esi + 0x13c], eax ; 0x00857015: je 0x857028
  - 0x00857015: je -> 0x00857017 (jcc_false) | ctx: 0x00857008: mov ecx, edi ; 0x0085700a: call 0xacbf60 ; 0x0085700f: cmp dword ptr [esi + 0x13c], eax ; 0x00857015: je 0x857028
  - 0x00856f59: jne -> 0x008570bc (jcc_true) | ctx: 0x00856f4c: push eax ; 0x00856f4d: call 0x963d00 ; 0x00856f52: cmp dword ptr [esi + 0x160], 2 ; 0x00856f59: jne 0x8570bc
  - 0x00856f59: jne -> 0x00856f5f (jcc_false) | ctx: 0x00856f4c: push eax ; 0x00856f4d: call 0x963d00 ; 0x00856f52: cmp dword ptr [esi + 0x160], 2 ; 0x00856f59: jne 0x8570bc
  - 0x00856f2a: jmp -> 0x00856f3a (jmp) | ctx: 0x00856f23: mov byte ptr [esi + 0x140], 1 ; 0x00856f2a: jmp 0x856f3a
  - 0x00857041: je -> 0x0085708d (jcc_true) | ctx: 0x00857037: call 0x5cb3d0 ; 0x0085703c: add esp, 8 ; 0x0085703f: test al, al ; 0x00857041: je 0x85708d
  - 0x00857041: je -> 0x00857043 (jcc_false) | ctx: 0x00857037: call 0x5cb3d0 ; 0x0085703c: add esp, 8 ; 0x0085703f: test al, al ; 0x00857041: je 0x85708d
  - 0x00857041: je -> 0x0085708d (jcc_true) | ctx: 0x00857037: call 0x5cb3d0 ; 0x0085703c: add esp, 8 ; 0x0085703f: test al, al ; 0x00857041: je 0x85708d
  - 0x00857041: je -> 0x00857043 (jcc_false) | ctx: 0x00857037: call 0x5cb3d0 ; 0x0085703c: add esp, 8 ; 0x0085703f: test al, al ; 0x00857041: je 0x85708d
  - 0x00856f66: jne -> 0x008570bc (jcc_true) | ctx: 0x00856f5f: cmp dword ptr [esi + 0x164], 0 ; 0x00856f66: jne 0x8570bc
  - 0x00856f66: jne -> 0x00856f6c (jcc_false) | ctx: 0x00856f5f: cmp dword ptr [esi + 0x164], 0 ; 0x00856f66: jne 0x8570bc
  - 0x00856f59: jne -> 0x008570bc (jcc_true) | ctx: 0x00856f4c: push eax ; 0x00856f4d: call 0x963d00 ; 0x00856f52: cmp dword ptr [esi + 0x160], 2 ; 0x00856f59: jne 0x8570bc
  - 0x00856f59: jne -> 0x00856f5f (jcc_false) | ctx: 0x00856f4c: push eax ; 0x00856f4d: call 0x963d00 ; 0x00856f52: cmp dword ptr [esi + 0x160], 2 ; 0x00856f59: jne 0x8570bc
  - 0x00857091: je -> 0x008570b5 (jcc_true) | ctx: 0x0085708d: cmp byte ptr [ebp + 0xf], 0 ; 0x00857091: je 0x8570b5
  - 0x00857091: je -> 0x00857093 (jcc_false) | ctx: 0x0085708d: cmp byte ptr [ebp + 0xf], 0 ; 0x00857091: je 0x8570b5
  - 0x0085704c: je -> 0x0085705a (jcc_true) | ctx: 0x00857043: mov ecx, edi ; 0x00857045: call 0xb3bc00 ; 0x0085704a: cmp ebx, eax ; 0x0085704c: je 0x85705a
  - 0x0085704c: je -> 0x0085704e (jcc_false) | ctx: 0x00857043: mov ecx, edi ; 0x00857045: call 0xb3bc00 ; 0x0085704a: cmp ebx, eax ; 0x0085704c: je 0x85705a
  - 0x00856f85: je -> 0x00856f93 (jcc_true) | ctx: 0x00856f78: call 0xb3bc00 ; 0x00856f7d: lea edi, [esi + 0xa4] ; 0x00856f83: cmp edi, eax ; 0x00856f85: je 0x856f93
  - 0x00856f85: je -> 0x00856f87 (jcc_false) | ctx: 0x00856f78: call 0xb3bc00 ; 0x00856f7d: lea edi, [esi + 0xa4] ; 0x00856f83: cmp edi, eax ; 0x00856f85: je 0x856f93
  - 0x0085709b: je -> 0x008570b5 (jcc_true) | ctx: 0x00857093: mov ecx, dword ptr [esi + 0x13c] ; 0x00857099: test ecx, ecx ; 0x0085709b: je 0x8570b5
  - 0x0085709b: je -> 0x0085709d (jcc_false) | ctx: 0x00857093: mov ecx, dword ptr [esi + 0x13c] ; 0x00857099: test ecx, ecx ; 0x0085709b: je 0x8570b5
  - 0x0085708b: jmp -> 0x00857093 (jmp) | ctx: 0x00857082: add ecx, 0xc ; 0x00857085: push eax ; 0x00857086: call 0x9a9d60 ; 0x0085708b: jmp 0x857093
  - 0x0085708b: jmp -> 0x00857093 (jmp) | ctx: 0x00857082: add ecx, 0xc ; 0x00857085: push eax ; 0x00857086: call 0x9a9d60 ; 0x0085708b: jmp 0x857093
  - 0x00856fc4: jmp -> 0x008570b5 (jmp) | ctx: 0x00856fbb: add ecx, 0xc ; 0x00856fbe: push eax ; 0x00856fbf: call 0x9a9d60 ; 0x00856fc4: jmp 0x8570b5
  - 0x00856fc4: jmp -> 0x008570b5 (jmp) | ctx: 0x00856fbb: add ecx, 0xc ; 0x00856fbe: push eax ; 0x00856fbf: call 0x9a9d60 ; 0x00856fc4: jmp 0x8570b5
  - 0x008570a5: je -> 0x008570b5 (jcc_true) | ctx: 0x0085709d: mov eax, dword ptr [esi + 0x138] ; 0x008570a3: test eax, eax ; 0x008570a5: je 0x8570b5
  - 0x008570a5: je -> 0x008570a7 (jcc_false) | ctx: 0x0085709d: mov eax, dword ptr [esi + 0x138] ; 0x008570a3: test eax, eax ; 0x008570a5: je 0x8570b5
  - 0x008570a9: jge -> 0x008570b5 (jcc_true) | ctx: 0x008570a7: cmp ecx, eax ; 0x008570a9: jge 0x8570b5
  - 0x008570a9: jge -> 0x008570ab (jcc_false) | ctx: 0x008570a7: cmp ecx, eax ; 0x008570a9: jge 0x8570b5

### 0x008570e0
- blocks=10, insns=66, edges=22, jcc=7, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00857127)
- branch points:
  - 0x008570f3: jne -> 0x00857155 (jcc_true) | ctx: 0x008570ea: mov ecx, edi ; 0x008570ec: call 0x92ffd0 ; 0x008570f1: test eax, eax ; 0x008570f3: jne 0x857155
  - 0x008570f3: jne -> 0x008570f5 (jcc_false) | ctx: 0x008570ea: mov ecx, edi ; 0x008570ec: call 0x92ffd0 ; 0x008570f1: test eax, eax ; 0x008570f3: jne 0x857155
  - 0x00857102: je -> 0x00857155 (jcc_true) | ctx: 0x008570f5: mov ecx, edi ; 0x008570f7: call 0x99a090 ; 0x008570fc: cmp dword ptr [esi + 0x138], eax ; 0x00857102: je 0x857155
  - 0x00857102: je -> 0x00857104 (jcc_false) | ctx: 0x008570f5: mov ecx, edi ; 0x008570f7: call 0x99a090 ; 0x008570fc: cmp dword ptr [esi + 0x138], eax ; 0x00857102: je 0x857155
  - 0x00857120: je -> 0x0085712c (jcc_true) | ctx: 0x00857113: call 0x997de0 ; 0x00857118: lea ecx, [esi + 0x8c] ; 0x0085711e: cmp ecx, eax ; 0x00857120: je 0x85712c
  - 0x00857120: je -> 0x00857122 (jcc_false) | ctx: 0x00857113: call 0x997de0 ; 0x00857118: lea ecx, [esi + 0x8c] ; 0x0085711e: cmp ecx, eax ; 0x00857120: je 0x85712c
  - 0x00857134: je -> 0x0085714e (jcc_true) | ctx: 0x0085712c: mov eax, dword ptr [esi + 0x13c] ; 0x00857132: test eax, eax ; 0x00857134: je 0x85714e
  - 0x00857134: je -> 0x00857136 (jcc_false) | ctx: 0x0085712c: mov eax, dword ptr [esi + 0x13c] ; 0x00857132: test eax, eax ; 0x00857134: je 0x85714e
  - 0x00857134: je -> 0x0085714e (jcc_true) | ctx: 0x00857127: call 0x5c5420 ; 0x0085712c: mov eax, dword ptr [esi + 0x13c] ; 0x00857132: test eax, eax ; 0x00857134: je 0x85714e
  - 0x00857134: je -> 0x00857136 (jcc_false) | ctx: 0x00857127: call 0x5c5420 ; 0x0085712c: mov eax, dword ptr [esi + 0x13c] ; 0x00857132: test eax, eax ; 0x00857134: je 0x85714e
  - 0x0085713e: je -> 0x0085714e (jcc_true) | ctx: 0x00857136: mov ecx, dword ptr [esi + 0x138] ; 0x0085713c: test ecx, ecx ; 0x0085713e: je 0x85714e
  - 0x0085713e: je -> 0x00857140 (jcc_false) | ctx: 0x00857136: mov ecx, dword ptr [esi + 0x138] ; 0x0085713c: test ecx, ecx ; 0x0085713e: je 0x85714e
  - 0x00857142: jge -> 0x0085714e (jcc_true) | ctx: 0x00857140: cmp eax, ecx ; 0x00857142: jge 0x85714e
  - 0x00857142: jge -> 0x00857144 (jcc_false) | ctx: 0x00857140: cmp eax, ecx ; 0x00857142: jge 0x85714e

### 0x0085e137
- blocks=8, insns=92, edges=15, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0085e179)
- branch points:
  - 0x0085e154: je -> 0x0085e186 (jcc_true) | ctx: 0x0085e14d: mov edx, eax ; 0x0085e14f: add esp, 8 ; 0x0085e152: test edx, edx ; 0x0085e154: je 0x85e186
  - 0x0085e154: je -> 0x0085e156 (jcc_false) | ctx: 0x0085e14d: mov edx, eax ; 0x0085e14f: add esp, 8 ; 0x0085e152: test edx, edx ; 0x0085e154: je 0x85e186
  - 0x0085e1a1: jne -> 0x0085e1a9 (jcc_true) | ctx: 0x0085e199: mov edx, dword ptr [ebp + 0x10] ; 0x0085e19c: mov eax, dword ptr [eax + esi] ; 0x0085e19f: cmp dword ptr [edx], eax ; 0x0085e1a1: jne 0x85e1a9
  - 0x0085e1a1: jne -> 0x0085e1a3 (jcc_false) | ctx: 0x0085e199: mov edx, dword ptr [ebp + 0x10] ; 0x0085e19c: mov eax, dword ptr [eax + esi] ; 0x0085e19f: cmp dword ptr [edx], eax ; 0x0085e1a1: jne 0x85e1a9
  - 0x0085e166: jne -> 0x0085e180 (jcc_true) | ctx: 0x0085e15c: or cl, 2 ; 0x0085e15f: test byte ptr [edx + 0x4a], 0xe ; 0x0085e163: mov byte ptr [edx + 0x48], cl ; 0x0085e166: jne 0x85e180
  - 0x0085e166: jne -> 0x0085e168 (jcc_false) | ctx: 0x0085e15c: or cl, 2 ; 0x0085e15f: test byte ptr [edx + 0x4a], 0xe ; 0x0085e163: mov byte ptr [edx + 0x48], cl ; 0x0085e166: jne 0x85e180
  - 0x0085e1a1: jne -> 0x0085e1a9 (jcc_true) | ctx: 0x0085e199: mov edx, dword ptr [ebp + 0x10] ; 0x0085e19c: mov eax, dword ptr [eax + esi] ; 0x0085e19f: cmp dword ptr [edx], eax ; 0x0085e1a1: jne 0x85e1a9
  - 0x0085e1a1: jne -> 0x0085e1a3 (jcc_false) | ctx: 0x0085e199: mov edx, dword ptr [ebp + 0x10] ; 0x0085e19c: mov eax, dword ptr [eax + esi] ; 0x0085e19f: cmp dword ptr [edx], eax ; 0x0085e1a1: jne 0x85e1a9
  - 0x0085e172: je -> 0x0085e186 (jcc_true) | ctx: 0x0085e16a: lea ecx, [edx + 0x4c] ; 0x0085e16d: mov dword ptr [edx + 0x64], eax ; 0x0085e170: cmp ecx, edi ; 0x0085e172: je 0x85e186
  - 0x0085e172: je -> 0x0085e174 (jcc_false) | ctx: 0x0085e16a: lea ecx, [edx + 0x4c] ; 0x0085e16d: mov dword ptr [edx + 0x64], eax ; 0x0085e170: cmp ecx, edi ; 0x0085e172: je 0x85e186
  - 0x0085e17e: jmp -> 0x0085e186 (jmp) | ctx: 0x0085e176: push 0 ; 0x0085e178: push edi ; 0x0085e179: call 0x5c5420 ; 0x0085e17e: jmp 0x85e186

### 0x0085ed08
- blocks=11, insns=114, edges=19, jcc=7, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0085ed81)
- branch points:
  - 0x0085ed12: je -> 0x0085ede9 (jcc_true) | ctx: 0x0085ed08: push edi ; 0x0085ed09: mov edi, ecx ; 0x0085ed0b: cmp dword ptr [edi + 0x1e0], 3 ; 0x0085ed12: je 0x85ede9
  - 0x0085ed12: je -> 0x0085ed18 (jcc_false) | ctx: 0x0085ed08: push edi ; 0x0085ed09: mov edi, ecx ; 0x0085ed0b: cmp dword ptr [edi + 0x1e0], 3 ; 0x0085ed12: je 0x85ede9
  - 0x0085ed31: jne -> 0x0085ede9 (jcc_true) | ctx: 0x0085ed29: cmovne eax, ecx ; 0x0085ed2c: mov eax, dword ptr [eax + edi] ; 0x0085ed2f: cmp dword ptr [ebx], eax ; 0x0085ed31: jne 0x85ede9
  - 0x0085ed31: jne -> 0x0085ed37 (jcc_false) | ctx: 0x0085ed29: cmovne eax, ecx ; 0x0085ed2c: mov eax, dword ptr [eax + edi] ; 0x0085ed2f: cmp dword ptr [ebx], eax ; 0x0085ed31: jne 0x85ede9
  - 0x0085ed3b: jne -> 0x0085ede9 (jcc_true) | ctx: 0x0085ed37: test byte ptr [edi + 6], 2 ; 0x0085ed3b: jne 0x85ede9
  - 0x0085ed3b: jne -> 0x0085ed41 (jcc_false) | ctx: 0x0085ed37: test byte ptr [edi + 6], 2 ; 0x0085ed3b: jne 0x85ede9
  - 0x0085ed55: je -> 0x0085ede9 (jcc_true) | ctx: 0x0085ed4e: mov esi, eax ; 0x0085ed50: add esp, 8 ; 0x0085ed53: test esi, esi ; 0x0085ed55: je 0x85ede9
  - 0x0085ed55: je -> 0x0085ed5b (jcc_false) | ctx: 0x0085ed4e: mov esi, eax ; 0x0085ed50: add esp, 8 ; 0x0085ed53: test esi, esi ; 0x0085ed55: je 0x85ede9
  - 0x0085ed78: je -> 0x0085ed8c (jcc_true) | ctx: 0x0085ed70: mov dword ptr [ebp + 0x14], edx ; 0x0085ed73: mov dword ptr [ebp + 0x10], ecx ; 0x0085ed76: cmp eax, ecx ; 0x0085ed78: je 0x85ed8c
  - 0x0085ed78: je -> 0x0085ed7a (jcc_false) | ctx: 0x0085ed70: mov dword ptr [ebp + 0x14], edx ; 0x0085ed73: mov dword ptr [ebp + 0x10], ecx ; 0x0085ed76: cmp eax, ecx ; 0x0085ed78: je 0x85ed8c
  - 0x0085ed9f: je -> 0x0085eda7 (jcc_true) | ctx: 0x0085ed8f: mov dword ptr [ebp - 8], 0xfff0be04 ; 0x0085ed96: mov dword ptr [ebp - 4], 0 ; 0x0085ed9d: test eax, eax ; 0x0085ed9f: je 0x85eda7
  - 0x0085ed9f: je -> 0x0085eda1 (jcc_false) | ctx: 0x0085ed8f: mov dword ptr [ebp - 8], 0xfff0be04 ; 0x0085ed96: mov dword ptr [ebp - 4], 0 ; 0x0085ed9d: test eax, eax ; 0x0085ed9f: je 0x85eda7
  - 0x0085ed9f: je -> 0x0085eda7 (jcc_true) | ctx: 0x0085ed8f: mov dword ptr [ebp - 8], 0xfff0be04 ; 0x0085ed96: mov dword ptr [ebp - 4], 0 ; 0x0085ed9d: test eax, eax ; 0x0085ed9f: je 0x85eda7
  - 0x0085ed9f: je -> 0x0085eda1 (jcc_false) | ctx: 0x0085ed8f: mov dword ptr [ebp - 8], 0xfff0be04 ; 0x0085ed96: mov dword ptr [ebp - 4], 0 ; 0x0085ed9d: test eax, eax ; 0x0085ed9f: je 0x85eda7
  - 0x0085eda5: jmp -> 0x0085edad (jmp) | ctx: 0x0085eda1: mov ax, word ptr [eax + 0x30] ; 0x0085eda5: jmp 0x85edad

### 0x008600e6
- blocks=14, insns=118, edges=25, jcc=10, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00860158)
- branch points:
  - 0x008600f0: je -> 0x008601f2 (jcc_true) | ctx: 0x008600e6: push edi ; 0x008600e7: mov edi, ecx ; 0x008600e9: cmp dword ptr [edi + 0x1e0], 3 ; 0x008600f0: je 0x8601f2
  - 0x008600f0: je -> 0x008600f6 (jcc_false) | ctx: 0x008600e6: push edi ; 0x008600e7: mov edi, ecx ; 0x008600e9: cmp dword ptr [edi + 0x1e0], 3 ; 0x008600f0: je 0x8601f2
  - 0x008600fa: jne -> 0x008601f2 (jcc_true) | ctx: 0x008600f6: test byte ptr [edi + 6], 2 ; 0x008600fa: jne 0x8601f2
  - 0x008600fa: jne -> 0x00860100 (jcc_false) | ctx: 0x008600f6: test byte ptr [edi + 6], 2 ; 0x008600fa: jne 0x8601f2
  - 0x00860106: je -> 0x0086010f (jcc_true) | ctx: 0x00860100: push esi ; 0x00860101: mov esi, dword ptr [ebp + 0x14] ; 0x00860104: test esi, esi ; 0x00860106: je 0x86010f
  - 0x00860106: je -> 0x00860108 (jcc_false) | ctx: 0x00860100: push esi ; 0x00860101: mov esi, dword ptr [ebp + 0x14] ; 0x00860104: test esi, esi ; 0x00860106: je 0x86010f
  - 0x0086010d: je -> 0x00860127 (jcc_true) | ctx: 0x00860108: mov al, byte ptr [esi + 0x4a] ; 0x0086010b: test al, 4 ; 0x0086010d: je 0x860127
  - 0x0086010d: je -> 0x0086010f (jcc_false) | ctx: 0x00860108: mov al, byte ptr [esi + 0x4a] ; 0x0086010b: test al, 4 ; 0x0086010d: je 0x860127
  - 0x00860134: je -> 0x0086013c (jcc_true) | ctx: 0x00860129: mov byte ptr [ebp + 0x14], 0 ; 0x0086012d: mov byte ptr [esi + 0x4a], al ; 0x00860130: test byte ptr [edi + 4], 2 ; 0x00860134: je 0x86013c
  - 0x00860134: je -> 0x00860136 (jcc_false) | ctx: 0x00860129: mov byte ptr [ebp + 0x14], 0 ; 0x0086012d: mov byte ptr [esi + 0x4a], al ; 0x00860130: test byte ptr [edi + 4], 2 ; 0x00860134: je 0x86013c
  - 0x00860151: je -> 0x0086015d (jcc_true) | ctx: 0x0086014a: mov eax, dword ptr [eax] ; 0x0086014c: mov dword ptr [esi + 0x64], eax ; 0x0086014f: cmp ecx, ebx ; 0x00860151: je 0x86015d
  - 0x00860151: je -> 0x00860153 (jcc_false) | ctx: 0x0086014a: mov eax, dword ptr [eax] ; 0x0086014c: mov dword ptr [esi + 0x64], eax ; 0x0086014f: cmp ecx, ebx ; 0x00860151: je 0x86015d
  - 0x0086013a: je -> 0x00860140 (jcc_true) | ctx: 0x00860136: test byte ptr [edi + 5], 0x40 ; 0x0086013a: je 0x860140
  - 0x0086013a: je -> 0x0086013c (jcc_false) | ctx: 0x00860136: test byte ptr [edi + 5], 0x40 ; 0x0086013a: je 0x860140
  - 0x0086017a: je -> 0x00860195 (jcc_true) | ctx: 0x0086016e: mov eax, 0xfff0be08 ; 0x00860173: cmovne eax, ecx ; 0x00860176: test byte ptr [esi + 0x4a], 2 ; 0x0086017a: je 0x860195
  - 0x0086017a: je -> 0x0086017c (jcc_false) | ctx: 0x0086016e: mov eax, 0xfff0be08 ; 0x00860173: cmovne eax, ecx ; 0x00860176: test byte ptr [esi + 0x4a], 2 ; 0x0086017a: je 0x860195
  - 0x0086017a: je -> 0x00860195 (jcc_true) | ctx: 0x0086016e: mov eax, 0xfff0be08 ; 0x00860173: cmovne eax, ecx ; 0x00860176: test byte ptr [esi + 0x4a], 2 ; 0x0086017a: je 0x860195
  - 0x0086017a: je -> 0x0086017c (jcc_false) | ctx: 0x0086016e: mov eax, 0xfff0be08 ; 0x00860173: cmovne eax, ecx ; 0x00860176: test byte ptr [esi + 0x4a], 2 ; 0x0086017a: je 0x860195
  - 0x00860151: je -> 0x0086015d (jcc_true) | ctx: 0x0086014a: mov eax, dword ptr [eax] ; 0x0086014c: mov dword ptr [esi + 0x64], eax ; 0x0086014f: cmp ecx, ebx ; 0x00860151: je 0x86015d
  - 0x00860151: je -> 0x00860153 (jcc_false) | ctx: 0x0086014a: mov eax, dword ptr [eax] ; 0x0086014c: mov dword ptr [esi + 0x64], eax ; 0x0086014f: cmp ecx, ebx ; 0x00860151: je 0x86015d

### 0x008604d7
- blocks=34, insns=350, edges=74, jcc=24, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00860546)
- branch points:
  - 0x008604e9: jne -> 0x00860504 (jcc_true) | ctx: 0x008604da: mov dword ptr [ebp - 4], 0 ; 0x008604e1: push edi ; 0x008604e2: cmp dword ptr [esi + 0x1e0], 3 ; 0x008604e9: jne 0x860504
  - 0x008604e9: jne -> 0x008604eb (jcc_false) | ctx: 0x008604da: mov dword ptr [ebp - 4], 0 ; 0x008604e1: push edi ; 0x008604e2: cmp dword ptr [esi + 0x1e0], 3 ; 0x008604e9: jne 0x860504
  - 0x00860509: je -> 0x008604eb (jcc_true) | ctx: 0x00860504: mov edi, dword ptr [ebp + 0x14] ; 0x00860507: test edi, edi ; 0x00860509: je 0x8604eb
  - 0x00860509: je -> 0x0086050b (jcc_false) | ctx: 0x00860504: mov edi, dword ptr [ebp + 0x14] ; 0x00860507: test edi, edi ; 0x00860509: je 0x8604eb
  - 0x0086050f: je -> 0x00860519 (jcc_true) | ctx: 0x0086050b: test byte ptr [esi + 4], 2 ; 0x0086050f: je 0x860519
  - 0x0086050f: je -> 0x00860511 (jcc_false) | ctx: 0x0086050b: test byte ptr [esi + 4], 2 ; 0x0086050f: je 0x860519
  - 0x00860521: jne -> 0x008604eb (jcc_true) | ctx: 0x00860519: mov ecx, dword ptr [esi + 0x5c] ; 0x0086051c: mov eax, dword ptr [ebp + 0x18] ; 0x0086051f: cmp ecx, dword ptr [eax] ; 0x00860521: jne 0x8604eb
  - 0x00860521: jne -> 0x00860523 (jcc_false) | ctx: 0x00860519: mov ecx, dword ptr [esi + 0x5c] ; 0x0086051c: mov eax, dword ptr [ebp + 0x18] ; 0x0086051f: cmp ecx, dword ptr [eax] ; 0x00860521: jne 0x8604eb
  - 0x00860517: jmp -> 0x0086051c (jmp) | ctx: 0x00860511: mov ecx, dword ptr [esi + 0x1a0] ; 0x00860517: jmp 0x86051c
  - 0x00860531: jne -> 0x0086054e (jcc_true) | ctx: 0x00860527: test byte ptr [edi + 0x4a], 4 ; 0x0086052b: mov ebx, dword ptr [ebp + 0x20] ; 0x0086052e: mov ecx, dword ptr [ebp + 0x24] ; 0x00860531: jne 0x86054e
  - 0x00860531: jne -> 0x00860533 (jcc_false) | ctx: 0x00860527: test byte ptr [edi + 0x4a], 4 ; 0x0086052b: mov ebx, dword ptr [ebp + 0x20] ; 0x0086052e: mov ecx, dword ptr [ebp + 0x24] ; 0x00860531: jne 0x86054e
  - 0x00860521: jne -> 0x008604eb (jcc_true) | ctx: 0x0086051c: mov eax, dword ptr [ebp + 0x18] ; 0x0086051f: cmp ecx, dword ptr [eax] ; 0x00860521: jne 0x8604eb
  - 0x00860521: jne -> 0x00860523 (jcc_false) | ctx: 0x0086051c: mov eax, dword ptr [ebp + 0x18] ; 0x0086051f: cmp ecx, dword ptr [eax] ; 0x00860521: jne 0x8604eb
  - 0x00860554: jne -> 0x00860719 (jcc_true) | ctx: 0x0086054e: mov eax, dword ptr [edi + 0x44] ; 0x00860551: cmp eax, dword ptr [esi + 0x60] ; 0x00860554: jne 0x860719
  - 0x00860554: jne -> 0x0086055a (jcc_false) | ctx: 0x0086054e: mov eax, dword ptr [edi + 0x44] ; 0x00860551: cmp eax, dword ptr [esi + 0x60] ; 0x00860554: jne 0x860719
  - 0x0086053d: je -> 0x0086054e (jcc_true) | ctx: 0x00860535: mov dword ptr [edi + 0x64], eax ; 0x00860538: lea eax, [edi + 0x4c] ; 0x0086053b: cmp eax, ebx ; 0x0086053d: je 0x86054e
  - 0x0086053d: je -> 0x0086053f (jcc_false) | ctx: 0x00860535: mov dword ptr [edi + 0x64], eax ; 0x00860538: lea eax, [edi + 0x4c] ; 0x0086053b: cmp eax, ebx ; 0x0086053d: je 0x86054e
  - 0x0086071d: jne -> 0x0086075d (jcc_true) | ctx: 0x00860719: cmp byte ptr [ebp + 0x28], 1 ; 0x0086071d: jne 0x86075d
  - 0x0086071d: jne -> 0x0086071f (jcc_false) | ctx: 0x00860719: cmp byte ptr [ebp + 0x28], 1 ; 0x0086071d: jne 0x86075d
  - 0x0086055f: jne -> 0x008604eb (jcc_true) | ctx: 0x0086055a: mov al, byte ptr [esi + 7] ; 0x0086055d: test al, 4 ; 0x0086055f: jne 0x8604eb
  - 0x0086055f: jne -> 0x00860561 (jcc_false) | ctx: 0x0086055a: mov al, byte ptr [esi + 7] ; 0x0086055d: test al, 4 ; 0x0086055f: jne 0x8604eb
  - 0x00860554: jne -> 0x00860719 (jcc_true) | ctx: 0x0086054b: mov ecx, dword ptr [ebp + 0x24] ; 0x0086054e: mov eax, dword ptr [edi + 0x44] ; 0x00860551: cmp eax, dword ptr [esi + 0x60] ; 0x00860554: jne 0x860719
  - 0x00860554: jne -> 0x0086055a (jcc_false) | ctx: 0x0086054b: mov ecx, dword ptr [ebp + 0x24] ; 0x0086054e: mov eax, dword ptr [edi + 0x44] ; 0x00860551: cmp eax, dword ptr [esi + 0x60] ; 0x00860554: jne 0x860719
  - 0x00860761: jne -> 0x008604eb (jcc_true) | ctx: 0x0086075d: test byte ptr [edi + 0x4a], 4 ; 0x00860761: jne 0x8604eb
  - 0x00860761: jne -> 0x00860767 (jcc_false) | ctx: 0x0086075d: test byte ptr [edi + 0x4a], 4 ; 0x00860761: jne 0x8604eb
  - 0x00860723: jne -> 0x0086075d (jcc_true) | ctx: 0x0086071f: cmp dword ptr [edi + 0x3c], 3 ; 0x00860723: jne 0x86075d
  - 0x00860723: jne -> 0x00860725 (jcc_false) | ctx: 0x0086071f: cmp dword ptr [edi + 0x3c], 3 ; 0x00860723: jne 0x86075d
  - 0x0086058e: jne -> 0x008606c8 (jcc_true) | ctx: 0x00860581: push eax ; 0x00860582: call 0x841a60 ; 0x00860587: cmp dword ptr [esi + 0x1e0], 1 ; 0x0086058e: jne 0x8606c8
  - 0x0086058e: jne -> 0x00860594 (jcc_false) | ctx: 0x00860581: push eax ; 0x00860582: call 0x841a60 ; 0x00860587: cmp dword ptr [esi + 0x1e0], 1 ; 0x0086058e: jne 0x8606c8
  - 0x0086076b: je -> 0x00860777 (jcc_true) | ctx: 0x00860767: test byte ptr [esi + 4], 2 ; 0x0086076b: je 0x860777
  - 0x0086076b: je -> 0x0086076d (jcc_false) | ctx: 0x00860767: test byte ptr [esi + 4], 2 ; 0x0086076b: je 0x860777
  - 0x00860761: jne -> 0x008604eb (jcc_true) | ctx: 0x00860757: push eax ; 0x00860758: call 0x86fb50 ; 0x0086075d: test byte ptr [edi + 0x4a], 4 ; 0x00860761: jne 0x8604eb
  - 0x00860761: jne -> 0x00860767 (jcc_false) | ctx: 0x00860757: push eax ; 0x00860758: call 0x86fb50 ; 0x0086075d: test byte ptr [edi + 0x4a], 4 ; 0x00860761: jne 0x8604eb
  - 0x008606cc: jne -> 0x008605c9 (jcc_true) | ctx: 0x008606c8: test byte ptr [esi + 6], 2 ; 0x008606cc: jne 0x8605c9
  - 0x008606cc: jne -> 0x008606d2 (jcc_false) | ctx: 0x008606c8: test byte ptr [esi + 6], 2 ; 0x008606cc: jne 0x8605c9
  - 0x00860598: jne -> 0x008606c8 (jcc_true) | ctx: 0x00860594: test byte ptr [esi + 4], 2 ; 0x00860598: jne 0x8606c8
  - 0x00860598: jne -> 0x0086059e (jcc_false) | ctx: 0x00860594: test byte ptr [esi + 4], 2 ; 0x00860598: jne 0x8606c8
  - 0x00860771: je -> 0x008605c9 (jcc_true) | ctx: 0x0086076d: test byte ptr [esi + 5], 0x40 ; 0x00860771: je 0x8605c9
  - 0x00860771: je -> 0x00860777 (jcc_false) | ctx: 0x0086076d: test byte ptr [esi + 5], 0x40 ; 0x00860771: je 0x8605c9
  - 0x008606d6: jb -> 0x008606f7 (jcc_true) | ctx: 0x008606d2: cmp byte ptr [esi + 5], 0x80 ; 0x008606d6: jb 0x8606f7
  - 0x008606d6: jb -> 0x008606d8 (jcc_false) | ctx: 0x008606d2: cmp byte ptr [esi + 5], 0x80 ; 0x008606d6: jb 0x8606f7
  - 0x008605a2: je -> 0x008605e2 (jcc_true) | ctx: 0x0086059e: test byte ptr [esi + 5], 0x20 ; 0x008605a2: je 0x8605e2
  - 0x008605a2: je -> 0x008605a4 (jcc_false) | ctx: 0x0086059e: test byte ptr [esi + 5], 0x20 ; 0x008605a2: je 0x8605e2
  - 0x00860714: jmp -> 0x008605c1 (jmp) | ctx: 0x0086070d: push ebx ; 0x0086070e: push dword ptr [ebp + 0xc] ; 0x00860711: lea eax, [ebp - 0x14] ; 0x00860714: jmp 0x8605c1
  - 0x008606f2: jmp -> 0x008605c9 (jmp) | ctx: 0x008606e9: lea eax, [ebp - 0x14] ; 0x008606ec: push eax ; 0x008606ed: call 0x858610 ; 0x008606f2: jmp 0x8605c9
  - 0x008605f4: je -> 0x008606a7 (jcc_true) | ctx: 0x008605e8: sar eax, 2 ; 0x008605eb: mov dword ptr [ebp + 0x28], 0 ; 0x008605f2: test eax, eax ; 0x008605f4: je 0x8606a7
  - 0x008605f4: je -> 0x008605fa (jcc_false) | ctx: 0x008605e8: sar eax, 2 ; 0x008605eb: mov dword ptr [ebp + 0x28], 0 ; 0x008605f2: test eax, eax ; 0x008605f4: je 0x8606a7
  - 0x008606c3: jmp -> 0x008605c9 (jmp) | ctx: 0x008606ba: lea eax, [ebp - 0x14] ; 0x008606bd: push eax ; 0x008606be: call 0x852c50 ; 0x008606c3: jmp 0x8605c9
  - 0x0086069b: jb -> 0x00860600 (jcc_true) | ctx: 0x00860693: sar eax, 2 ; 0x00860696: mov dword ptr [ebp + 0x28], ebx ; 0x00860699: cmp ebx, eax ; 0x0086069b: jb 0x860600
  - 0x0086069b: jb -> 0x008606a1 (jcc_false) | ctx: 0x00860693: sar eax, 2 ; 0x00860696: mov dword ptr [ebp + 0x28], ebx ; 0x00860699: cmp ebx, eax ; 0x0086069b: jb 0x860600
  - 0x0086069b: jb -> 0x00860600 (jcc_true) | ctx: 0x00860693: sar eax, 2 ; 0x00860696: mov dword ptr [ebp + 0x28], ebx ; 0x00860699: cmp ebx, eax ; 0x0086069b: jb 0x860600
  - 0x0086069b: jb -> 0x008606a1 (jcc_false) | ctx: 0x00860693: sar eax, 2 ; 0x00860696: mov dword ptr [ebp + 0x28], ebx ; 0x00860699: cmp ebx, eax ; 0x0086069b: jb 0x860600
  - 0x008606c3: jmp -> 0x008605c9 (jmp) | ctx: 0x008606ba: lea eax, [ebp - 0x14] ; 0x008606bd: push eax ; 0x008606be: call 0x852c50 ; 0x008606c3: jmp 0x8605c9

### 0x00862c30
- blocks=28, insns=463, edges=65, jcc=17, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00862daa)
- branch points:
  - 0x00862c6d: jne -> 0x00862ca5 (jcc_true) | ctx: 0x00862c65: mov edi, eax ; 0x00862c67: mov dword ptr [ebp + 0x14], edi ; 0x00862c6a: cmp esi, -1 ; 0x00862c6d: jne 0x862ca5
  - 0x00862c6d: jne -> 0x00862c6f (jcc_false) | ctx: 0x00862c65: mov edi, eax ; 0x00862c67: mov dword ptr [ebp + 0x14], edi ; 0x00862c6a: cmp esi, -1 ; 0x00862c6d: jne 0x862ca5
  - 0x00862ca9: je -> 0x00862ed7 (jcc_true) | ctx: 0x00862ca5: cmp byte ptr [ebp + 0x1c], 0 ; 0x00862ca9: je 0x862ed7
  - 0x00862ca9: je -> 0x00862caf (jcc_false) | ctx: 0x00862ca5: cmp byte ptr [ebp + 0x1c], 0 ; 0x00862ca9: je 0x862ed7
  - 0x00862c71: jne -> 0x00862c9f (jcc_true) | ctx: 0x00862c6f: test edi, edi ; 0x00862c71: jne 0x862c9f
  - 0x00862c71: jne -> 0x00862c73 (jcc_false) | ctx: 0x00862c6f: test edi, edi ; 0x00862c71: jne 0x862c9f
  - 0x00862eec: jne -> 0x00862f4f (jcc_true) | ctx: 0x00862ee5: mov ecx, eax ; 0x00862ee7: mov dword ptr [ebp + 0x1c], ecx ; 0x00862eea: test ecx, ecx ; 0x00862eec: jne 0x862f4f
  - 0x00862eec: jne -> 0x00862eee (jcc_false) | ctx: 0x00862ee5: mov ecx, eax ; 0x00862ee7: mov dword ptr [ebp + 0x1c], ecx ; 0x00862eea: test ecx, ecx ; 0x00862eec: jne 0x862f4f
  - 0x00862cda: je -> 0x00862d49 (jcc_true) | ctx: 0x00862cce: mov dword ptr [ebp - 0x10], edi ; 0x00862cd1: mov dword ptr [ebp - 4], 0 ; 0x00862cd8: test edi, edi ; 0x00862cda: je 0x862d49
  - 0x00862cda: je -> 0x00862cdc (jcc_false) | ctx: 0x00862cce: mov dword ptr [ebp - 0x10], edi ; 0x00862cd1: mov dword ptr [ebp - 4], 0 ; 0x00862cd8: test edi, edi ; 0x00862cda: je 0x862d49
  - 0x00862ca9: je -> 0x00862ed7 (jcc_true) | ctx: 0x00862c9f: mov esi, dword ptr [edi + 0x48] ; 0x00862ca2: mov dword ptr [ebp + 0x18], esi ; 0x00862ca5: cmp byte ptr [ebp + 0x1c], 0 ; 0x00862ca9: je 0x862ed7
  - 0x00862ca9: je -> 0x00862caf (jcc_false) | ctx: 0x00862c9f: mov esi, dword ptr [edi + 0x48] ; 0x00862ca2: mov dword ptr [ebp + 0x18], esi ; 0x00862ca5: cmp byte ptr [ebp + 0x1c], 0 ; 0x00862ca9: je 0x862ed7
  - 0x00862c9a: jmp -> 0x00862fde (jmp) | ctx: 0x00862c8d: mov dword ptr [ebp - 0x14], 0xfff0bdc0 ; 0x00862c94: push dword ptr [ebp + 0xc] ; 0x00862c97: mov dword ptr [ebp - 0x10], edi ; 0x00862c9a: jmp 0x862fde
  - 0x00862f78: je -> 0x00862fb5 (jcc_true) | ctx: 0x00862f6d: mov ecx, ebx ; 0x00862f6f: call 0x870eb0 ; 0x00862f74: cmp byte ptr [ebp + 0x28], 0 ; 0x00862f78: je 0x862fb5
  - 0x00862f78: je -> 0x00862f7a (jcc_false) | ctx: 0x00862f6d: mov ecx, ebx ; 0x00862f6f: call 0x870eb0 ; 0x00862f74: cmp byte ptr [ebp + 0x28], 0 ; 0x00862f78: je 0x862fb5
  - 0x00862f2e: je -> 0x00862ff0 (jcc_true) | ctx: 0x00862f24: mov ecx, dword ptr [eax + 0x64] ; 0x00862f27: call 0x854fd0 ; 0x00862f2c: test edi, edi ; 0x00862f2e: je 0x862ff0
  - 0x00862f2e: je -> 0x00862f34 (jcc_false) | ctx: 0x00862f24: mov ecx, dword ptr [eax + 0x64] ; 0x00862f27: call 0x854fd0 ; 0x00862f2c: test edi, edi ; 0x00862f2e: je 0x862ff0
  - 0x00862da3: je -> 0x00862daf (jcc_true) | ctx: 0x00862d9b: mov eax, dword ptr [ebp + 0x20] ; 0x00862d9e: lea ecx, [edi + 0x38] ; 0x00862da1: cmp ecx, eax ; 0x00862da3: je 0x862daf
  - 0x00862da3: je -> 0x00862da5 (jcc_false) | ctx: 0x00862d9b: mov eax, dword ptr [ebp + 0x20] ; 0x00862d9e: lea ecx, [edi + 0x38] ; 0x00862da1: cmp ecx, eax ; 0x00862da3: je 0x862daf
  - 0x00862d39: jb -> 0x00862d3d (jcc_true) | ctx: 0x00862d27: mov dword ptr [eax + 0x14], 0xf ; 0x00862d2e: mov dword ptr [eax + 0x10], 0 ; 0x00862d35: cmp dword ptr [eax + 0x14], 0x10 ; 0x00862d39: jb 0x862d3d
  - 0x00862d39: jb -> 0x00862d3b (jcc_false) | ctx: 0x00862d27: mov dword ptr [eax + 0x14], 0xf ; 0x00862d2e: mov dword ptr [eax + 0x10], 0 ; 0x00862d35: cmp dword ptr [eax + 0x14], 0x10 ; 0x00862d39: jb 0x862d3d
  - 0x00862f9d: je -> 0x00862fb5 (jcc_true) | ctx: 0x00862f95: push eax ; 0x00862f96: call 0x870de0 ; 0x00862f9b: test edi, edi ; 0x00862f9d: je 0x862fb5
  - 0x00862f9d: je -> 0x00862f9f (jcc_false) | ctx: 0x00862f95: push eax ; 0x00862f96: call 0x870de0 ; 0x00862f9b: test edi, edi ; 0x00862f9d: je 0x862fb5
  - 0x00862f4a: jmp -> 0x00862ff0 (jmp) | ctx: 0x00862f43: push esi ; 0x00862f44: push eax ; 0x00862f45: call 0x86d060 ; 0x00862f4a: jmp 0x862ff0
  - 0x00862dd6: je -> 0x00862fb5 (jcc_true) | ctx: 0x00862dce: push eax ; 0x00862dcf: call dword ptr [edx + 0x1c] ; 0x00862dd2: cmp byte ptr [ebp + 0x28], 0 ; 0x00862dd6: je 0x862fb5
  - 0x00862dd6: je -> 0x00862ddc (jcc_false) | ctx: 0x00862dce: push eax ; 0x00862dcf: call dword ptr [edx + 0x1c] ; 0x00862dd2: cmp byte ptr [ebp + 0x28], 0 ; 0x00862dd6: je 0x862fb5
  - 0x00862dd6: je -> 0x00862fb5 (jcc_true) | ctx: 0x00862dce: push eax ; 0x00862dcf: call dword ptr [edx + 0x1c] ; 0x00862dd2: cmp byte ptr [ebp + 0x28], 0 ; 0x00862dd6: je 0x862fb5
  - 0x00862dd6: je -> 0x00862ddc (jcc_false) | ctx: 0x00862dce: push eax ; 0x00862dcf: call dword ptr [edx + 0x1c] ; 0x00862dd2: cmp byte ptr [ebp + 0x28], 0 ; 0x00862dd6: je 0x862fb5
  - 0x00862d47: jmp -> 0x00862d4b (jmp) | ctx: 0x00862d3d: mov byte ptr [eax], 0 ; 0x00862d40: mov dword ptr [edi + 0x50], 0xffffffff ; 0x00862d47: jmp 0x862d4b
  - 0x00862d47: jmp -> 0x00862d4b (jmp) | ctx: 0x00862d3b: mov eax, dword ptr [eax] ; 0x00862d3d: mov byte ptr [eax], 0 ; 0x00862d40: mov dword ptr [edi + 0x50], 0xffffffff ; 0x00862d47: jmp 0x862d4b
  - 0x00862e04: je -> 0x00862e50 (jcc_true) | ctx: 0x00862df8: mov dword ptr [ebp + 0x1c], edi ; 0x00862dfb: mov dword ptr [ebp - 4], 3 ; 0x00862e02: test edi, edi ; 0x00862e04: je 0x862e50
  - 0x00862e04: je -> 0x00862e06 (jcc_false) | ctx: 0x00862df8: mov dword ptr [ebp + 0x1c], edi ; 0x00862dfb: mov dword ptr [ebp - 4], 3 ; 0x00862e02: test edi, edi ; 0x00862e04: je 0x862e50
  - 0x00862da3: je -> 0x00862daf (jcc_true) | ctx: 0x00862d9b: mov eax, dword ptr [ebp + 0x20] ; 0x00862d9e: lea ecx, [edi + 0x38] ; 0x00862da1: cmp ecx, eax ; 0x00862da3: je 0x862daf
  - 0x00862da3: je -> 0x00862da5 (jcc_false) | ctx: 0x00862d9b: mov eax, dword ptr [ebp + 0x20] ; 0x00862d9e: lea ecx, [edi + 0x38] ; 0x00862da1: cmp ecx, eax ; 0x00862da3: je 0x862daf
  - 0x00862ec2: je -> 0x00862fb5 (jcc_true) | ctx: 0x00862eba: call dword ptr [edx + 0x1c] ; 0x00862ebd: mov eax, dword ptr [ebp + 0x14] ; 0x00862ec0: test eax, eax ; 0x00862ec2: je 0x862fb5
  - 0x00862ec2: je -> 0x00862ec8 (jcc_false) | ctx: 0x00862eba: call dword ptr [edx + 0x1c] ; 0x00862ebd: mov eax, dword ptr [ebp + 0x14] ; 0x00862ec0: test eax, eax ; 0x00862ec2: je 0x862fb5
  - 0x00862e4e: jmp -> 0x00862e52 (jmp) | ctx: 0x00862e3e: mov byte ptr [ebp - 4], 4 ; 0x00862e42: mov dword ptr [edi + 0x28], 0xffffffff ; 0x00862e49: call 0x9289a0 ; 0x00862e4e: jmp 0x862e52
  - 0x00862ed2: jmp -> 0x00862fa9 (jmp) | ctx: 0x00862ec8: lea ecx, [ebx + 0x1e4] ; 0x00862ece: push ecx ; 0x00862ecf: push dword ptr [eax + 0x20] ; 0x00862ed2: jmp 0x862fa9
  - 0x00862ec2: je -> 0x00862fb5 (jcc_true) | ctx: 0x00862eba: call dword ptr [edx + 0x1c] ; 0x00862ebd: mov eax, dword ptr [ebp + 0x14] ; 0x00862ec0: test eax, eax ; 0x00862ec2: je 0x862fb5
  - 0x00862ec2: je -> 0x00862ec8 (jcc_false) | ctx: 0x00862eba: call dword ptr [edx + 0x1c] ; 0x00862ebd: mov eax, dword ptr [ebp + 0x14] ; 0x00862ec0: test eax, eax ; 0x00862ec2: je 0x862fb5

### 0x00865fc0
- blocks=31, insns=385, edges=73, jcc=23, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00866128)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x008662a8)
- branch points:
  - 0x00865fef: jae -> 0x00866003 (jcc_true) | ctx: 0x00865fe5: push edi ; 0x00865fe6: mov edx, dword ptr [esi + 0x20] ; 0x00865fe9: cmp edx, 0x80 ; 0x00865fef: jae 0x866003
  - 0x00865fef: jae -> 0x00865ff1 (jcc_false) | ctx: 0x00865fe5: push edi ; 0x00865fe6: mov edx, dword ptr [esi + 0x20] ; 0x00865fe9: cmp edx, 0x80 ; 0x00865fef: jae 0x866003
  - 0x00866050: jne -> 0x00866192 (jcc_true) | ctx: 0x00866048: shr eax, 0x1c ; 0x0086604b: and eax, 3 ; 0x0086604e: cmp ecx, eax ; 0x00866050: jne 0x866192
  - 0x00866050: jne -> 0x00866056 (jcc_false) | ctx: 0x00866048: shr eax, 0x1c ; 0x0086604b: and eax, 3 ; 0x0086604e: cmp ecx, eax ; 0x00866050: jne 0x866192
  - 0x00865ff7: je -> 0x00866003 (jcc_true) | ctx: 0x00865ff1: mov ecx, dword ptr [ebx + edx*4 + 0x4c] ; 0x00865ff5: test ecx, ecx ; 0x00865ff7: je 0x866003
  - 0x00865ff7: je -> 0x00865ff9 (jcc_false) | ctx: 0x00865ff1: mov ecx, dword ptr [ebx + edx*4 + 0x4c] ; 0x00865ff5: test ecx, ecx ; 0x00865ff7: je 0x866003
  - 0x008661b6: je -> 0x00866212 (jcc_true) | ctx: 0x008661ae: mov dword ptr [ebp - 0x10], edi ; 0x008661b1: mov dword ptr [ebp - 0x10], edi ; 0x008661b4: test edi, edi ; 0x008661b6: je 0x866212
  - 0x008661b6: je -> 0x008661b8 (jcc_false) | ctx: 0x008661ae: mov dword ptr [ebp - 0x10], edi ; 0x008661b1: mov dword ptr [ebp - 0x10], edi ; 0x008661b4: test edi, edi ; 0x008661b6: je 0x866212
  - 0x008660ad: jb -> 0x008660b1 (jcc_true) | ctx: 0x0086609f: lea edx, [esi + 0x28] ; 0x008660a2: mov dword ptr [ebp - 4], 1 ; 0x008660a9: mov byte ptr [ebp - 0x5c], 1 ; 0x008660ad: jb 0x8660b1
  - 0x008660ad: jb -> 0x008660af (jcc_false) | ctx: 0x0086609f: lea edx, [esi + 0x28] ; 0x008660a2: mov dword ptr [ebp - 4], 1 ; 0x008660a9: mov byte ptr [ebp - 0x5c], 1 ; 0x008660ad: jb 0x8660b1
  - 0x00866050: jne -> 0x00866192 (jcc_true) | ctx: 0x00866048: shr eax, 0x1c ; 0x0086604b: and eax, 3 ; 0x0086604e: cmp ecx, eax ; 0x00866050: jne 0x866192
  - 0x00866050: jne -> 0x00866056 (jcc_false) | ctx: 0x00866048: shr eax, 0x1c ; 0x0086604b: and eax, 3 ; 0x0086604e: cmp ecx, eax ; 0x00866050: jne 0x866192
  - 0x0086623d: jne -> 0x00866243 (jcc_true) | ctx: 0x0086622f: mov dword ptr [ebp - 0x1c], 0 ; 0x00866236: mov byte ptr [ebp - 0x2c], 0 ; 0x0086623a: cmp byte ptr [edx], 0 ; 0x0086623d: jne 0x866243
  - 0x0086623d: jne -> 0x0086623f (jcc_false) | ctx: 0x0086622f: mov dword ptr [ebp - 0x1c], 0 ; 0x00866236: mov byte ptr [ebp - 0x2c], 0 ; 0x0086623a: cmp byte ptr [edx], 0 ; 0x0086623d: jne 0x866243
  - 0x00866202: jb -> 0x00866206 (jcc_true) | ctx: 0x008661f0: mov dword ptr [eax + 0x14], 0xf ; 0x008661f7: mov dword ptr [eax + 0x10], 0 ; 0x008661fe: cmp dword ptr [eax + 0x14], 0x10 ; 0x00866202: jb 0x866206
  - 0x00866202: jb -> 0x00866204 (jcc_false) | ctx: 0x008661f0: mov dword ptr [eax + 0x14], 0xf ; 0x008661f7: mov dword ptr [eax + 0x10], 0 ; 0x008661fe: cmp dword ptr [eax + 0x14], 0x10 ; 0x00866202: jb 0x866206
  - 0x008660c9: jne -> 0x008660cf (jcc_true) | ctx: 0x008660b8: mov dword ptr [ebp - 0x7c], 0 ; 0x008660bf: mov byte ptr [ebp - 0x8c], 0 ; 0x008660c6: cmp byte ptr [edx], 0 ; 0x008660c9: jne 0x8660cf
  - 0x008660c9: jne -> 0x008660cb (jcc_false) | ctx: 0x008660b8: mov dword ptr [ebp - 0x7c], 0 ; 0x008660bf: mov byte ptr [ebp - 0x8c], 0 ; 0x008660c6: cmp byte ptr [edx], 0 ; 0x008660c9: jne 0x8660cf
  - 0x008660c9: jne -> 0x008660cf (jcc_true) | ctx: 0x008660b8: mov dword ptr [ebp - 0x7c], 0 ; 0x008660bf: mov byte ptr [ebp - 0x8c], 0 ; 0x008660c6: cmp byte ptr [edx], 0 ; 0x008660c9: jne 0x8660cf
  - 0x008660c9: jne -> 0x008660cb (jcc_false) | ctx: 0x008660b8: mov dword ptr [ebp - 0x7c], 0 ; 0x008660bf: mov byte ptr [ebp - 0x8c], 0 ; 0x008660c6: cmp byte ptr [edx], 0 ; 0x008660c9: jne 0x8660cf
  - 0x00866255: jne -> 0x00866250 (jcc_true) | ctx: 0x00866250: mov al, byte ptr [ecx] ; 0x00866252: inc ecx ; 0x00866253: test al, al ; 0x00866255: jne 0x866250
  - 0x00866255: jne -> 0x00866257 (jcc_false) | ctx: 0x00866250: mov al, byte ptr [ecx] ; 0x00866252: inc ecx ; 0x00866253: test al, al ; 0x00866255: jne 0x866250
  - 0x00866241: jmp -> 0x0086625a (jmp) | ctx: 0x0086623f: xor ecx, ecx ; 0x00866241: jmp 0x86625a
  - 0x00866210: jmp -> 0x00866214 (jmp) | ctx: 0x00866206: mov byte ptr [eax], 0 ; 0x00866209: mov dword ptr [edi + 0x40], 0xffffffff ; 0x00866210: jmp 0x866214
  - 0x00866210: jmp -> 0x00866214 (jmp) | ctx: 0x00866204: mov eax, dword ptr [eax] ; 0x00866206: mov byte ptr [eax], 0 ; 0x00866209: mov dword ptr [edi + 0x40], 0xffffffff ; 0x00866210: jmp 0x866214
  - 0x008660d9: jne -> 0x008660d4 (jcc_true) | ctx: 0x008660d4: mov al, byte ptr [ecx] ; 0x008660d6: inc ecx ; 0x008660d7: test al, al ; 0x008660d9: jne 0x8660d4
  - 0x008660d9: jne -> 0x008660db (jcc_false) | ctx: 0x008660d4: mov al, byte ptr [ecx] ; 0x008660d6: inc ecx ; 0x008660d7: test al, al ; 0x008660d9: jne 0x8660d4
  - 0x008660cd: jmp -> 0x008660dd (jmp) | ctx: 0x008660cb: xor ecx, ecx ; 0x008660cd: jmp 0x8660dd
  - 0x00866255: jne -> 0x00866250 (jcc_true) | ctx: 0x00866250: mov al, byte ptr [ecx] ; 0x00866252: inc ecx ; 0x00866253: test al, al ; 0x00866255: jne 0x866250
  - 0x00866255: jne -> 0x00866257 (jcc_false) | ctx: 0x00866250: mov al, byte ptr [ecx] ; 0x00866252: inc ecx ; 0x00866253: test al, al ; 0x00866255: jne 0x866250
  - 0x008662a1: je -> 0x008662ad (jcc_true) | ctx: 0x00866299: mov dword ptr [edi + 0x14], edx ; 0x0086629c: mov dword ptr [edi + 0x20], esi ; 0x0086629f: cmp ecx, eax ; 0x008662a1: je 0x8662ad
  - 0x008662a1: je -> 0x008662a3 (jcc_false) | ctx: 0x00866299: mov dword ptr [edi + 0x14], edx ; 0x0086629c: mov dword ptr [edi + 0x20], esi ; 0x0086629f: cmp ecx, eax ; 0x008662a1: je 0x8662ad
  - 0x008662a1: je -> 0x008662ad (jcc_true) | ctx: 0x00866299: mov dword ptr [edi + 0x14], edx ; 0x0086629c: mov dword ptr [edi + 0x20], esi ; 0x0086629f: cmp ecx, eax ; 0x008662a1: je 0x8662ad
  - 0x008662a1: je -> 0x008662a3 (jcc_false) | ctx: 0x00866299: mov dword ptr [edi + 0x14], edx ; 0x0086629c: mov dword ptr [edi + 0x20], esi ; 0x0086629f: cmp ecx, eax ; 0x008662a1: je 0x8662ad
  - 0x0086623d: jne -> 0x00866243 (jcc_true) | ctx: 0x0086622f: mov dword ptr [ebp - 0x1c], 0 ; 0x00866236: mov byte ptr [ebp - 0x2c], 0 ; 0x0086623a: cmp byte ptr [edx], 0 ; 0x0086623d: jne 0x866243
  - 0x0086623d: jne -> 0x0086623f (jcc_false) | ctx: 0x0086622f: mov dword ptr [ebp - 0x1c], 0 ; 0x00866236: mov byte ptr [ebp - 0x2c], 0 ; 0x0086623a: cmp byte ptr [edx], 0 ; 0x0086623d: jne 0x866243
  - 0x008660d9: jne -> 0x008660d4 (jcc_true) | ctx: 0x008660d4: mov al, byte ptr [ecx] ; 0x008660d6: inc ecx ; 0x008660d7: test al, al ; 0x008660d9: jne 0x8660d4
  - 0x008660d9: jne -> 0x008660db (jcc_false) | ctx: 0x008660d4: mov al, byte ptr [ecx] ; 0x008660d6: inc ecx ; 0x008660d7: test al, al ; 0x008660d9: jne 0x8660d4
  - 0x0086613b: jb -> 0x0086614b (jcc_true) | ctx: 0x00866130: mov dword ptr [ebp - 0x34], eax ; 0x00866133: cmp dword ptr [ebp - 0x78], 0x10 ; 0x00866137: mov byte ptr [ebp - 4], 3 ; 0x0086613b: jb 0x86614b
  - 0x0086613b: jb -> 0x0086613d (jcc_false) | ctx: 0x00866130: mov dword ptr [ebp - 0x34], eax ; 0x00866133: cmp dword ptr [ebp - 0x78], 0x10 ; 0x00866137: mov byte ptr [ebp - 4], 3 ; 0x0086613b: jb 0x86614b
  - 0x0086613b: jb -> 0x0086614b (jcc_true) | ctx: 0x00866130: mov dword ptr [ebp - 0x34], eax ; 0x00866133: cmp dword ptr [ebp - 0x78], 0x10 ; 0x00866137: mov byte ptr [ebp - 4], 3 ; 0x0086613b: jb 0x86614b
  - 0x0086613b: jb -> 0x0086613d (jcc_false) | ctx: 0x00866130: mov dword ptr [ebp - 0x34], eax ; 0x00866133: cmp dword ptr [ebp - 0x78], 0x10 ; 0x00866137: mov byte ptr [ebp - 4], 3 ; 0x0086613b: jb 0x86614b
  - 0x008662c1: jb -> 0x008662ce (jcc_true) | ctx: 0x008662b3: mov dword ptr [edi + 0x40], eax ; 0x008662b6: cmp dword ptr [ebp - 0x18], 0x10 ; 0x008662ba: mov dword ptr [ebp - 4], 8 ; 0x008662c1: jb 0x8662ce
  - 0x008662c1: jb -> 0x008662c3 (jcc_false) | ctx: 0x008662b3: mov dword ptr [edi + 0x40], eax ; 0x008662b6: cmp dword ptr [ebp - 0x18], 0x10 ; 0x008662ba: mov dword ptr [ebp - 4], 8 ; 0x008662c1: jb 0x8662ce
  - 0x008662c1: jb -> 0x008662ce (jcc_true) | ctx: 0x008662b3: mov dword ptr [edi + 0x40], eax ; 0x008662b6: cmp dword ptr [ebp - 0x18], 0x10 ; 0x008662ba: mov dword ptr [ebp - 4], 8 ; 0x008662c1: jb 0x8662ce
  - 0x008662c1: jb -> 0x008662c3 (jcc_false) | ctx: 0x008662b3: mov dword ptr [edi + 0x40], eax ; 0x008662b6: cmp dword ptr [ebp - 0x18], 0x10 ; 0x008662ba: mov dword ptr [ebp - 4], 8 ; 0x008662c1: jb 0x8662ce
  - 0x0086617c: jb -> 0x008662f0 (jcc_true) | ctx: 0x0086616a: mov dword ptr [ebp - 0x74], 0xc1ab90 ; 0x00866171: cmp dword ptr [ebp - 0x38], 0x10 ; 0x00866175: mov dword ptr [ebp - 4], 4 ; 0x0086617c: jb 0x8662f0
  - 0x0086617c: jb -> 0x00866182 (jcc_false) | ctx: 0x0086616a: mov dword ptr [ebp - 0x74], 0xc1ab90 ; 0x00866171: cmp dword ptr [ebp - 0x38], 0x10 ; 0x00866175: mov dword ptr [ebp - 4], 4 ; 0x0086617c: jb 0x8662f0
  - 0x0086617c: jb -> 0x008662f0 (jcc_true) | ctx: 0x0086616a: mov dword ptr [ebp - 0x74], 0xc1ab90 ; 0x00866171: cmp dword ptr [ebp - 0x38], 0x10 ; 0x00866175: mov dword ptr [ebp - 4], 4 ; 0x0086617c: jb 0x8662f0
  - 0x0086617c: jb -> 0x00866182 (jcc_false) | ctx: 0x0086616a: mov dword ptr [ebp - 0x74], 0xc1ab90 ; 0x00866171: cmp dword ptr [ebp - 0x38], 0x10 ; 0x00866175: mov dword ptr [ebp - 4], 4 ; 0x0086617c: jb 0x8662f0
  - 0x0086618d: jmp -> 0x008662f0 (jmp) | ctx: 0x00866182: push dword ptr [ebp - 0x4c] ; 0x00866185: call 0x9afbf0 ; 0x0086618a: add esp, 4 ; 0x0086618d: jmp 0x8662f0

### 0x0086a6e0
- blocks=14, insns=84, edges=26, jcc=10, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0086a740)
- branch points:
  - 0x0086a6f7: jb -> 0x0086a700 (jcc_true) | ctx: 0x0086a6ed: add edi, 0x20 ; 0x0086a6f0: mov dword ptr [ebp - 4], ecx ; 0x0086a6f3: cmp dword ptr [edi + 0x14], 0x10 ; 0x0086a6f7: jb 0x86a700
  - 0x0086a6f7: jb -> 0x0086a6f9 (jcc_false) | ctx: 0x0086a6ed: add edi, 0x20 ; 0x0086a6f0: mov dword ptr [ebp - 4], ecx ; 0x0086a6f3: cmp dword ptr [edi + 0x14], 0x10 ; 0x0086a6f7: jb 0x86a700
  - 0x0086a707: jb -> 0x0086a70d (jcc_true) | ctx: 0x0086a700: mov dword ptr [ebp + 0xc], edi ; 0x0086a703: cmp dword ptr [esi + 0x14], 0x10 ; 0x0086a707: jb 0x86a70d
  - 0x0086a707: jb -> 0x0086a709 (jcc_false) | ctx: 0x0086a700: mov dword ptr [ebp + 0xc], edi ; 0x0086a703: cmp dword ptr [esi + 0x14], 0x10 ; 0x0086a707: jb 0x86a70d
  - 0x0086a6fe: jmp -> 0x0086a703 (jmp) | ctx: 0x0086a6f9: mov eax, dword ptr [edi] ; 0x0086a6fb: mov dword ptr [ebp + 0xc], eax ; 0x0086a6fe: jmp 0x86a703
  - 0x0086a72a: jne -> 0x0086a735 (jcc_true) | ctx: 0x0086a720: call 0x4f7400 ; 0x0086a725: add esp, 0xc ; 0x0086a728: test eax, eax ; 0x0086a72a: jne 0x86a735
  - 0x0086a72a: jne -> 0x0086a72c (jcc_false) | ctx: 0x0086a720: call 0x4f7400 ; 0x0086a725: add esp, 0xc ; 0x0086a728: test eax, eax ; 0x0086a72a: jne 0x86a735
  - 0x0086a70b: jmp -> 0x0086a70f (jmp) | ctx: 0x0086a709: mov edx, dword ptr [esi] ; 0x0086a70b: jmp 0x86a70f
  - 0x0086a707: jb -> 0x0086a70d (jcc_true) | ctx: 0x0086a703: cmp dword ptr [esi + 0x14], 0x10 ; 0x0086a707: jb 0x86a70d
  - 0x0086a707: jb -> 0x0086a709 (jcc_false) | ctx: 0x0086a703: cmp dword ptr [esi + 0x14], 0x10 ; 0x0086a707: jb 0x86a70d
  - 0x0086a737: je -> 0x0086a745 (jcc_true) | ctx: 0x0086a735: cmp esi, edi ; 0x0086a737: je 0x86a745
  - 0x0086a737: je -> 0x0086a739 (jcc_false) | ctx: 0x0086a735: cmp esi, edi ; 0x0086a737: je 0x86a745
  - 0x0086a731: jb -> 0x0086a735 (jcc_true) | ctx: 0x0086a72c: mov eax, dword ptr [esi + 0x10] ; 0x0086a72f: cmp eax, ebx ; 0x0086a731: jb 0x86a735
  - 0x0086a731: jb -> 0x0086a733 (jcc_false) | ctx: 0x0086a72c: mov eax, dword ptr [esi + 0x10] ; 0x0086a72f: cmp eax, ebx ; 0x0086a731: jb 0x86a735
  - 0x0086a72a: jne -> 0x0086a735 (jcc_true) | ctx: 0x0086a720: call 0x4f7400 ; 0x0086a725: add esp, 0xc ; 0x0086a728: test eax, eax ; 0x0086a72a: jne 0x86a735
  - 0x0086a72a: jne -> 0x0086a72c (jcc_false) | ctx: 0x0086a720: call 0x4f7400 ; 0x0086a725: add esp, 0xc ; 0x0086a728: test eax, eax ; 0x0086a72a: jne 0x86a735
  - 0x0086a74c: je -> 0x0086a757 (jcc_true) | ctx: 0x0086a745: mov ecx, dword ptr [ebp - 4] ; 0x0086a748: cmp byte ptr [ecx + 0x15], 0 ; 0x0086a74c: je 0x86a757
  - 0x0086a74c: je -> 0x0086a74e (jcc_false) | ctx: 0x0086a745: mov ecx, dword ptr [ebp - 4] ; 0x0086a748: cmp byte ptr [ecx + 0x15], 0 ; 0x0086a74c: je 0x86a757
  - 0x0086a74c: je -> 0x0086a757 (jcc_true) | ctx: 0x0086a740: call 0x5c5420 ; 0x0086a745: mov ecx, dword ptr [ebp - 4] ; 0x0086a748: cmp byte ptr [ecx + 0x15], 0 ; 0x0086a74c: je 0x86a757
  - 0x0086a74c: je -> 0x0086a74e (jcc_false) | ctx: 0x0086a740: call 0x5c5420 ; 0x0086a745: mov ecx, dword ptr [ebp - 4] ; 0x0086a748: cmp byte ptr [ecx + 0x15], 0 ; 0x0086a74c: je 0x86a757
  - 0x0086a733: jbe -> 0x0086a757 (jcc_true) | ctx: 0x0086a733: jbe 0x86a757
  - 0x0086a733: jbe -> 0x0086a735 (jcc_false) | ctx: 0x0086a733: jbe 0x86a757

### 0x0086b64c
- blocks=40, insns=246, edges=91, jcc=32, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0086b7fd)
- branch points:
  - 0x0086b675: jne -> 0x0086b6aa (jcc_true) | ctx: 0x0086b661: cmp dword ptr [edi + 0x9c], 0 ; 0x0086b668: lea eax, [edi + 0x8c] ; 0x0086b66e: mov dword ptr [ebp - 4], 0 ; 0x0086b675: jne 0x86b6aa
  - 0x0086b675: jne -> 0x0086b677 (jcc_false) | ctx: 0x0086b661: cmp dword ptr [edi + 0x9c], 0 ; 0x0086b668: lea eax, [edi + 0x8c] ; 0x0086b66e: mov dword ptr [ebp - 4], 0 ; 0x0086b675: jne 0x86b6aa
  - 0x0086b6c1: jb -> 0x0086b707 (jcc_true) | ctx: 0x0086b6b2: call 0x7f3d30 ; 0x0086b6b7: cmp dword ptr [edi + 0xb4], 5 ; 0x0086b6be: lea ecx, [ebp - 0x28] ; 0x0086b6c1: jb 0x86b707
  - 0x0086b6c1: jb -> 0x0086b6c3 (jcc_false) | ctx: 0x0086b6b2: call 0x7f3d30 ; 0x0086b6b7: cmp dword ptr [edi + 0xb4], 5 ; 0x0086b6be: lea ecx, [ebp - 0x28] ; 0x0086b6c1: jb 0x86b707
  - 0x0086b680: jne -> 0x0086b690 (jcc_true) | ctx: 0x0086b677: mov edx, dword ptr [0xd6bf58] ; 0x0086b67d: cmp byte ptr [edx], 0 ; 0x0086b680: jne 0x86b690
  - 0x0086b680: jne -> 0x0086b682 (jcc_false) | ctx: 0x0086b677: mov edx, dword ptr [0xd6bf58] ; 0x0086b67d: cmp byte ptr [edx], 0 ; 0x0086b680: jne 0x86b690
  - 0x0086b721: je -> 0x0086b7ab (jcc_true) | ctx: 0x0086b713: lea ecx, [edi + 0xfc] ; 0x0086b719: call 0x9311c0 ; 0x0086b71e: test ax, ax ; 0x0086b721: je 0x86b7ab
  - 0x0086b721: je -> 0x0086b727 (jcc_false) | ctx: 0x0086b713: lea ecx, [edi + 0xfc] ; 0x0086b719: call 0x9311c0 ; 0x0086b71e: test ax, ax ; 0x0086b721: je 0x86b7ab
  - 0x0086b6dc: jb -> 0x0086b6e0 (jcc_true) | ctx: 0x0086b6ca: call 0x7f3e30 ; 0x0086b6cf: cmp dword ptr [edi + 0xb8], 0x10 ; 0x0086b6d6: lea eax, [edi + 0xa4] ; 0x0086b6dc: jb 0x86b6e0
  - 0x0086b6dc: jb -> 0x0086b6de (jcc_false) | ctx: 0x0086b6ca: call 0x7f3e30 ; 0x0086b6cf: cmp dword ptr [edi + 0xb8], 0x10 ; 0x0086b6d6: lea eax, [edi + 0xa4] ; 0x0086b6dc: jb 0x86b6e0
  - 0x0086b69a: jne -> 0x0086b695 (jcc_true) | ctx: 0x0086b695: mov al, byte ptr [ecx] ; 0x0086b697: inc ecx ; 0x0086b698: test al, al ; 0x0086b69a: jne 0x86b695
  - 0x0086b69a: jne -> 0x0086b69c (jcc_false) | ctx: 0x0086b695: mov al, byte ptr [ecx] ; 0x0086b697: inc ecx ; 0x0086b698: test al, al ; 0x0086b69a: jne 0x86b695
  - 0x0086b68e: jmp -> 0x0086b6b7 (jmp) | ctx: 0x0086b685: push edx ; 0x0086b686: lea ecx, [ebp - 0x28] ; 0x0086b689: call 0x7f3e30 ; 0x0086b68e: jmp 0x86b6b7
  - 0x0086b7bd: jb -> 0x0086b7c6 (jcc_true) | ctx: 0x0086b7b2: lea esi, [edi + 0x74] ; 0x0086b7b5: cmovae edx, dword ptr [ebp - 0x28] ; 0x0086b7b9: cmp dword ptr [esi + 0x14], 0x10 ; 0x0086b7bd: jb 0x86b7c6
  - 0x0086b7bd: jb -> 0x0086b7bf (jcc_false) | ctx: 0x0086b7b2: lea esi, [edi + 0x74] ; 0x0086b7b5: cmovae edx, dword ptr [ebp - 0x28] ; 0x0086b7b9: cmp dword ptr [esi + 0x14], 0x10 ; 0x0086b7bd: jb 0x86b7c6
  - 0x0086b75b: jb -> 0x0086b75f (jcc_true) | ctx: 0x0086b751: mov edx, eax ; 0x0086b753: cmp dword ptr [edx + 0x14], 0x10 ; 0x0086b757: mov byte ptr [ebp - 4], 1 ; 0x0086b75b: jb 0x86b75f
  - 0x0086b75b: jb -> 0x0086b75d (jcc_false) | ctx: 0x0086b751: mov edx, eax ; 0x0086b753: cmp dword ptr [edx + 0x14], 0x10 ; 0x0086b757: mov byte ptr [ebp - 4], 1 ; 0x0086b75b: jb 0x86b75f
  - 0x0086b6e7: jne -> 0x0086b6f2 (jcc_true) | ctx: 0x0086b6e0: cmp byte ptr [eax + 5], 0 ; 0x0086b6e4: lea edx, [eax + 5] ; 0x0086b6e7: jne 0x86b6f2
  - 0x0086b6e7: jne -> 0x0086b6e9 (jcc_false) | ctx: 0x0086b6e0: cmp byte ptr [eax + 5], 0 ; 0x0086b6e4: lea edx, [eax + 5] ; 0x0086b6e7: jne 0x86b6f2
  - 0x0086b6e7: jne -> 0x0086b6f2 (jcc_true) | ctx: 0x0086b6de: mov eax, dword ptr [eax] ; 0x0086b6e0: cmp byte ptr [eax + 5], 0 ; 0x0086b6e4: lea edx, [eax + 5] ; 0x0086b6e7: jne 0x86b6f2
  - 0x0086b6e7: jne -> 0x0086b6e9 (jcc_false) | ctx: 0x0086b6de: mov eax, dword ptr [eax] ; 0x0086b6e0: cmp byte ptr [eax + 5], 0 ; 0x0086b6e4: lea edx, [eax + 5] ; 0x0086b6e7: jne 0x86b6f2
  - 0x0086b69a: jne -> 0x0086b695 (jcc_true) | ctx: 0x0086b695: mov al, byte ptr [ecx] ; 0x0086b697: inc ecx ; 0x0086b698: test al, al ; 0x0086b69a: jne 0x86b695
  - 0x0086b69a: jne -> 0x0086b69c (jcc_false) | ctx: 0x0086b695: mov al, byte ptr [ecx] ; 0x0086b697: inc ecx ; 0x0086b698: test al, al ; 0x0086b69a: jne 0x86b695
  - 0x0086b6a8: jmp -> 0x0086b6b7 (jmp) | ctx: 0x0086b69f: push edx ; 0x0086b6a0: lea ecx, [ebp - 0x28] ; 0x0086b6a3: call 0x7f3e30 ; 0x0086b6a8: jmp 0x86b6b7
  - 0x0086b6c1: jb -> 0x0086b707 (jcc_true) | ctx: 0x0086b6b7: cmp dword ptr [edi + 0xb4], 5 ; 0x0086b6be: lea ecx, [ebp - 0x28] ; 0x0086b6c1: jb 0x86b707
  - 0x0086b6c1: jb -> 0x0086b6c3 (jcc_false) | ctx: 0x0086b6b7: cmp dword ptr [edi + 0xb4], 5 ; 0x0086b6be: lea ecx, [ebp - 0x28] ; 0x0086b6c1: jb 0x86b707
  - 0x0086b7e4: jne -> 0x0086b7ef (jcc_true) | ctx: 0x0086b7da: call 0x4f7400 ; 0x0086b7df: add esp, 0xc ; 0x0086b7e2: test eax, eax ; 0x0086b7e4: jne 0x86b7ef
  - 0x0086b7e4: jne -> 0x0086b7e6 (jcc_false) | ctx: 0x0086b7da: call 0x4f7400 ; 0x0086b7df: add esp, 0xc ; 0x0086b7e2: test eax, eax ; 0x0086b7e4: jne 0x86b7ef
  - 0x0086b7c4: jmp -> 0x0086b7c9 (jmp) | ctx: 0x0086b7bf: mov eax, dword ptr [esi] ; 0x0086b7c1: mov dword ptr [ebp - 0x10], eax ; 0x0086b7c4: jmp 0x86b7c9
  - 0x0086b762: jne -> 0x0086b768 (jcc_true) | ctx: 0x0086b75f: cmp byte ptr [edx], 0 ; 0x0086b762: jne 0x86b768
  - 0x0086b762: jne -> 0x0086b764 (jcc_false) | ctx: 0x0086b75f: cmp byte ptr [edx], 0 ; 0x0086b762: jne 0x86b768
  - 0x0086b762: jne -> 0x0086b768 (jcc_true) | ctx: 0x0086b75d: mov edx, dword ptr [edx] ; 0x0086b75f: cmp byte ptr [edx], 0 ; 0x0086b762: jne 0x86b768
  - 0x0086b762: jne -> 0x0086b764 (jcc_false) | ctx: 0x0086b75d: mov edx, dword ptr [edx] ; 0x0086b75f: cmp byte ptr [edx], 0 ; 0x0086b762: jne 0x86b768
  - 0x0086b6fc: jne -> 0x0086b6f7 (jcc_true) | ctx: 0x0086b6f7: mov al, byte ptr [ecx] ; 0x0086b6f9: inc ecx ; 0x0086b6fa: test al, al ; 0x0086b6fc: jne 0x86b6f7
  - 0x0086b6fc: jne -> 0x0086b6fe (jcc_false) | ctx: 0x0086b6f7: mov al, byte ptr [ecx] ; 0x0086b6f9: inc ecx ; 0x0086b6fa: test al, al ; 0x0086b6fc: jne 0x86b6f7
  - 0x0086b6f0: jmp -> 0x0086b70e (jmp) | ctx: 0x0086b6eb: push ecx ; 0x0086b6ec: push edx ; 0x0086b6ed: lea ecx, [ebp - 0x28] ; 0x0086b6f0: jmp 0x86b70e
  - 0x0086b7f4: je -> 0x0086b802 (jcc_true) | ctx: 0x0086b7ef: lea eax, [ebp - 0x28] ; 0x0086b7f2: cmp esi, eax ; 0x0086b7f4: je 0x86b802
  - 0x0086b7f4: je -> 0x0086b7f6 (jcc_false) | ctx: 0x0086b7ef: lea eax, [ebp - 0x28] ; 0x0086b7f2: cmp esi, eax ; 0x0086b7f4: je 0x86b802
  - 0x0086b7eb: jb -> 0x0086b7ef (jcc_true) | ctx: 0x0086b7e6: mov eax, dword ptr [ebp - 0x18] ; 0x0086b7e9: cmp ebx, eax ; 0x0086b7eb: jb 0x86b7ef
  - 0x0086b7eb: jb -> 0x0086b7ed (jcc_false) | ctx: 0x0086b7e6: mov eax, dword ptr [ebp - 0x18] ; 0x0086b7e9: cmp ebx, eax ; 0x0086b7eb: jb 0x86b7ef
  - 0x0086b7e4: jne -> 0x0086b7ef (jcc_true) | ctx: 0x0086b7da: call 0x4f7400 ; 0x0086b7df: add esp, 0xc ; 0x0086b7e2: test eax, eax ; 0x0086b7e4: jne 0x86b7ef
  - 0x0086b7e4: jne -> 0x0086b7e6 (jcc_false) | ctx: 0x0086b7da: call 0x4f7400 ; 0x0086b7df: add esp, 0xc ; 0x0086b7e2: test eax, eax ; 0x0086b7e4: jne 0x86b7ef
  - 0x0086b775: jne -> 0x0086b770 (jcc_true) | ctx: 0x0086b770: mov al, byte ptr [ecx] ; 0x0086b772: inc ecx ; 0x0086b773: test al, al ; 0x0086b775: jne 0x86b770
  - 0x0086b775: jne -> 0x0086b777 (jcc_false) | ctx: 0x0086b770: mov al, byte ptr [ecx] ; 0x0086b772: inc ecx ; 0x0086b773: test al, al ; 0x0086b775: jne 0x86b770
  - 0x0086b766: jmp -> 0x0086b779 (jmp) | ctx: 0x0086b764: xor ecx, ecx ; 0x0086b766: jmp 0x86b779
  - 0x0086b6fc: jne -> 0x0086b6f7 (jcc_true) | ctx: 0x0086b6f7: mov al, byte ptr [ecx] ; 0x0086b6f9: inc ecx ; 0x0086b6fa: test al, al ; 0x0086b6fc: jne 0x86b6f7
  - 0x0086b6fc: jne -> 0x0086b6fe (jcc_false) | ctx: 0x0086b6f7: mov al, byte ptr [ecx] ; 0x0086b6f9: inc ecx ; 0x0086b6fa: test al, al ; 0x0086b6fc: jne 0x86b6f7
  - 0x0086b705: jmp -> 0x0086b70e (jmp) | ctx: 0x0086b700: push ecx ; 0x0086b701: push edx ; 0x0086b702: lea ecx, [ebp - 0x28] ; 0x0086b705: jmp 0x86b70e
  - 0x0086b721: je -> 0x0086b7ab (jcc_true) | ctx: 0x0086b713: lea ecx, [edi + 0xfc] ; 0x0086b719: call 0x9311c0 ; 0x0086b71e: test ax, ax ; 0x0086b721: je 0x86b7ab
  - 0x0086b721: je -> 0x0086b727 (jcc_false) | ctx: 0x0086b713: lea ecx, [edi + 0xfc] ; 0x0086b719: call 0x9311c0 ; 0x0086b71e: test ax, ax ; 0x0086b721: je 0x86b7ab
  - 0x0086b807: je -> 0x0086b818 (jcc_true) | ctx: 0x0086b802: cmp byte ptr [edi + 0x1d], 0 ; 0x0086b806: pop ebx ; 0x0086b807: je 0x86b818
  - 0x0086b807: je -> 0x0086b809 (jcc_false) | ctx: 0x0086b802: cmp byte ptr [edi + 0x1d], 0 ; 0x0086b806: pop ebx ; 0x0086b807: je 0x86b818
  - 0x0086b807: je -> 0x0086b818 (jcc_true) | ctx: 0x0086b7fd: call 0x5c5420 ; 0x0086b802: cmp byte ptr [edi + 0x1d], 0 ; 0x0086b806: pop ebx ; 0x0086b807: je 0x86b818
  - 0x0086b807: je -> 0x0086b809 (jcc_false) | ctx: 0x0086b7fd: call 0x5c5420 ; 0x0086b802: cmp byte ptr [edi + 0x1d], 0 ; 0x0086b806: pop ebx ; 0x0086b807: je 0x86b818
  - 0x0086b7ed: jbe -> 0x0086b802 (jcc_true) | ctx: 0x0086b7ed: jbe 0x86b802
  - 0x0086b7ed: jbe -> 0x0086b7ef (jcc_false) | ctx: 0x0086b7ed: jbe 0x86b802
  - 0x0086b775: jne -> 0x0086b770 (jcc_true) | ctx: 0x0086b770: mov al, byte ptr [ecx] ; 0x0086b772: inc ecx ; 0x0086b773: test al, al ; 0x0086b775: jne 0x86b770
  - 0x0086b775: jne -> 0x0086b777 (jcc_false) | ctx: 0x0086b770: mov al, byte ptr [ecx] ; 0x0086b772: inc ecx ; 0x0086b773: test al, al ; 0x0086b775: jne 0x86b770
  - 0x0086b78d: jb -> 0x0086b79c (jcc_true) | ctx: 0x0086b783: mov eax, dword ptr [ebp - 0x2c] ; 0x0086b786: mov byte ptr [ebp - 4], 0 ; 0x0086b78a: cmp eax, 0x10 ; 0x0086b78d: jb 0x86b79c
  - 0x0086b78d: jb -> 0x0086b78f (jcc_false) | ctx: 0x0086b783: mov eax, dword ptr [ebp - 0x2c] ; 0x0086b786: mov byte ptr [ebp - 4], 0 ; 0x0086b78a: cmp eax, 0x10 ; 0x0086b78d: jb 0x86b79c
  - 0x0086b78d: jb -> 0x0086b79c (jcc_true) | ctx: 0x0086b783: mov eax, dword ptr [ebp - 0x2c] ; 0x0086b786: mov byte ptr [ebp - 4], 0 ; 0x0086b78a: cmp eax, 0x10 ; 0x0086b78d: jb 0x86b79c
  - 0x0086b78d: jb -> 0x0086b78f (jcc_false) | ctx: 0x0086b783: mov eax, dword ptr [ebp - 0x2c] ; 0x0086b786: mov byte ptr [ebp - 4], 0 ; 0x0086b78a: cmp eax, 0x10 ; 0x0086b78d: jb 0x86b79c
  - 0x0086b825: jb -> 0x0086b832 (jcc_true) | ctx: 0x0086b81c: pop edi ; 0x0086b81d: mov dword ptr [ebp - 4], 2 ; 0x0086b824: pop esi ; 0x0086b825: jb 0x86b832
  - 0x0086b825: jb -> 0x0086b827 (jcc_false) | ctx: 0x0086b81c: pop edi ; 0x0086b81d: mov dword ptr [ebp - 4], 2 ; 0x0086b824: pop esi ; 0x0086b825: jb 0x86b832
  - 0x0086b825: jb -> 0x0086b832 (jcc_true) | ctx: 0x0086b81c: pop edi ; 0x0086b81d: mov dword ptr [ebp - 4], 2 ; 0x0086b824: pop esi ; 0x0086b825: jb 0x86b832
  - 0x0086b825: jb -> 0x0086b827 (jcc_false) | ctx: 0x0086b81c: pop edi ; 0x0086b81d: mov dword ptr [ebp - 4], 2 ; 0x0086b824: pop esi ; 0x0086b825: jb 0x86b832
  - 0x0086b7bd: jb -> 0x0086b7c6 (jcc_true) | ctx: 0x0086b7b2: lea esi, [edi + 0x74] ; 0x0086b7b5: cmovae edx, dword ptr [ebp - 0x28] ; 0x0086b7b9: cmp dword ptr [esi + 0x14], 0x10 ; 0x0086b7bd: jb 0x86b7c6
  - 0x0086b7bd: jb -> 0x0086b7bf (jcc_false) | ctx: 0x0086b7b2: lea esi, [edi + 0x74] ; 0x0086b7b5: cmovae edx, dword ptr [ebp - 0x28] ; 0x0086b7b9: cmp dword ptr [esi + 0x14], 0x10 ; 0x0086b7bd: jb 0x86b7c6
  - 0x0086b7bd: jb -> 0x0086b7c6 (jcc_true) | ctx: 0x0086b7b2: lea esi, [edi + 0x74] ; 0x0086b7b5: cmovae edx, dword ptr [ebp - 0x28] ; 0x0086b7b9: cmp dword ptr [esi + 0x14], 0x10 ; 0x0086b7bd: jb 0x86b7c6
  - 0x0086b7bd: jb -> 0x0086b7bf (jcc_false) | ctx: 0x0086b7b2: lea esi, [edi + 0x74] ; 0x0086b7b5: cmovae edx, dword ptr [ebp - 0x28] ; 0x0086b7b9: cmp dword ptr [esi + 0x14], 0x10 ; 0x0086b7bd: jb 0x86b7c6

### 0x0086da60
- blocks=161, insns=1851, edges=402, jcc=121, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0086e3ee)
- branch points:
  - 0x0086da9e: je -> 0x0086dae6 (jcc_true) | ctx: 0x0086da94: test byte ptr [ebx + 6], 1 ; 0x0086da98: mov dword ptr [ebp - 0x50], eax ; 0x0086da9b: mov dword ptr [ebp - 0x2c], edx ; 0x0086da9e: je 0x86dae6
  - 0x0086da9e: je -> 0x0086daa0 (jcc_false) | ctx: 0x0086da94: test byte ptr [ebx + 6], 1 ; 0x0086da98: mov dword ptr [ebp - 0x50], eax ; 0x0086da9b: mov dword ptr [ebp - 0x2c], edx ; 0x0086da9e: je 0x86dae6
  - 0x0086dafe: jne -> 0x0086de9e (jcc_true) | ctx: 0x0086daf8: mov al, cl ; 0x0086dafa: and al, 0xa ; 0x0086dafc: cmp al, 0xa ; 0x0086dafe: jne 0x86de9e
  - 0x0086dafe: jne -> 0x0086db04 (jcc_false) | ctx: 0x0086daf8: mov al, cl ; 0x0086dafa: and al, 0xa ; 0x0086dafc: cmp al, 0xa ; 0x0086dafe: jne 0x86de9e
  - 0x0086daa4: je -> 0x0086dac9 (jcc_true) | ctx: 0x0086daa0: test byte ptr [ebx + 5], 1 ; 0x0086daa4: je 0x86dac9
  - 0x0086daa4: je -> 0x0086daa6 (jcc_false) | ctx: 0x0086daa0: test byte ptr [ebx + 5], 1 ; 0x0086daa4: je 0x86dac9
  - 0x0086dea8: jne -> 0x0086deb8 (jcc_true) | ctx: 0x0086de9e: mov edi, dword ptr [ebp - 0x2c] ; 0x0086dea1: cmp dword ptr [ebx + 0x1e0], 1 ; 0x0086dea8: jne 0x86deb8
  - 0x0086dea8: jne -> 0x0086deaa (jcc_false) | ctx: 0x0086de9e: mov edi, dword ptr [ebp - 0x2c] ; 0x0086dea1: cmp dword ptr [ebx + 0x1e0], 1 ; 0x0086dea8: jne 0x86deb8
  - 0x0086db0a: je -> 0x0086dc77 (jcc_true) | ctx: 0x0086db04: mov edx, dword ptr [ebx + 0x60] ; 0x0086db07: cmp edx, -1 ; 0x0086db0a: je 0x86dc77
  - 0x0086db0a: je -> 0x0086db10 (jcc_false) | ctx: 0x0086db04: mov edx, dword ptr [ebx + 0x60] ; 0x0086db07: cmp edx, -1 ; 0x0086db0a: je 0x86dc77
  - 0x0086debd: je -> 0x0086e142 (jcc_true) | ctx: 0x0086deb8: mov al, byte ptr [ebx + 4] ; 0x0086debb: test al, 2 ; 0x0086debd: je 0x86e142
  - 0x0086debd: je -> 0x0086dec3 (jcc_false) | ctx: 0x0086deb8: mov al, byte ptr [ebx + 4] ; 0x0086debb: test al, 2 ; 0x0086debd: je 0x86e142
  - 0x0086debd: je -> 0x0086e142 (jcc_true) | ctx: 0x0086deb3: call 0x8420d0 ; 0x0086deb8: mov al, byte ptr [ebx + 4] ; 0x0086debb: test al, 2 ; 0x0086debd: je 0x86e142
  - 0x0086debd: je -> 0x0086dec3 (jcc_false) | ctx: 0x0086deb3: call 0x8420d0 ; 0x0086deb8: mov al, byte ptr [ebx + 4] ; 0x0086debb: test al, 2 ; 0x0086debd: je 0x86e142
  - 0x0086dc88: je -> 0x0086dd02 (jcc_true) | ctx: 0x0086dc80: push esi ; 0x0086dc81: call 0x84bb80 ; 0x0086dc86: test al, al ; 0x0086dc88: je 0x86dd02
  - 0x0086dc88: je -> 0x0086dc8a (jcc_false) | ctx: 0x0086dc80: push esi ; 0x0086dc81: call 0x84bb80 ; 0x0086dc86: test al, al ; 0x0086dc88: je 0x86dd02
  - 0x0086db13: je -> 0x0086db1d (jcc_true) | ctx: 0x0086db10: test cl, 2 ; 0x0086db13: je 0x86db1d
  - 0x0086db13: je -> 0x0086db15 (jcc_false) | ctx: 0x0086db10: test cl, 2 ; 0x0086db13: je 0x86db1d
  - 0x0086e149: jne -> 0x0086e2b7 (jcc_true) | ctx: 0x0086e142: cmp dword ptr [ebx + 0x1e0], 1 ; 0x0086e149: jne 0x86e2b7
  - 0x0086e149: jne -> 0x0086e14f (jcc_false) | ctx: 0x0086e142: cmp dword ptr [ebx + 0x1e0], 1 ; 0x0086e149: jne 0x86e2b7
  - 0x0086dec9: jb -> 0x0086eb0a (jcc_true) | ctx: 0x0086dec3: cmp edi, dword ptr [ebx + 0x1dc] ; 0x0086dec9: jb 0x86eb0a
  - 0x0086dec9: jb -> 0x0086decf (jcc_false) | ctx: 0x0086dec3: cmp edi, dword ptr [ebx + 0x1dc] ; 0x0086dec9: jb 0x86eb0a
  - 0x0086dd08: je -> 0x0086dd23 (jcc_true) | ctx: 0x0086dd02: mov ecx, dword ptr [ebx + 0x60] ; 0x0086dd05: cmp ecx, -1 ; 0x0086dd08: je 0x86dd23
  - 0x0086dd08: je -> 0x0086dd0a (jcc_false) | ctx: 0x0086dd02: mov ecx, dword ptr [ebx + 0x60] ; 0x0086dd05: cmp ecx, -1 ; 0x0086dd08: je 0x86dd23
  - 0x0086dc95: je -> 0x0086dd02 (jcc_true) | ctx: 0x0086dc8c: mov ecx, ebx ; 0x0086dc8e: call 0x84bb10 ; 0x0086dc93: test al, al ; 0x0086dc95: je 0x86dd02
  - 0x0086dc95: je -> 0x0086dc97 (jcc_false) | ctx: 0x0086dc8c: mov ecx, ebx ; 0x0086dc8e: call 0x84bb10 ; 0x0086dc93: test al, al ; 0x0086dc95: je 0x86dd02
  - 0x0086db22: jne -> 0x0086dc77 (jcc_true) | ctx: 0x0086db1d: mov eax, dword ptr [ebx + 0x5c] ; 0x0086db20: cmp edx, eax ; 0x0086db22: jne 0x86dc77
  - 0x0086db22: jne -> 0x0086db28 (jcc_false) | ctx: 0x0086db1d: mov eax, dword ptr [ebx + 0x5c] ; 0x0086db20: cmp edx, eax ; 0x0086db22: jne 0x86dc77
  - 0x0086db1b: jmp -> 0x0086db20 (jmp) | ctx: 0x0086db15: mov eax, dword ptr [ebx + 0x1a0] ; 0x0086db1b: jmp 0x86db20
  - 0x0086e2c3: je -> 0x0086eb0a (jcc_true) | ctx: 0x0086e2ba: mov ecx, ebx ; 0x0086e2bc: call 0x84bcf0 ; 0x0086e2c1: test al, al ; 0x0086e2c3: je 0x86eb0a
  - 0x0086e2c3: je -> 0x0086e2c9 (jcc_false) | ctx: 0x0086e2ba: mov ecx, ebx ; 0x0086e2bc: call 0x84bcf0 ; 0x0086e2c1: test al, al ; 0x0086e2c3: je 0x86eb0a
  - 0x0086e155: jb -> 0x0086eb0a (jcc_true) | ctx: 0x0086e14f: cmp edi, dword ptr [ebx + 0x194] ; 0x0086e155: jb 0x86eb0a
  - 0x0086e155: jb -> 0x0086e15b (jcc_false) | ctx: 0x0086e14f: cmp edi, dword ptr [ebx + 0x194] ; 0x0086e155: jb 0x86eb0a
  - 0x0086decf: ja -> 0x0086dee0 (jcc_true) | ctx: 0x0086decf: ja 0x86dee0
  - 0x0086decf: ja -> 0x0086ded1 (jcc_false) | ctx: 0x0086decf: ja 0x86dee0
  - 0x0086dd34: jb -> 0x0086dea1 (jcc_true) | ctx: 0x0086dd29: mov edi, dword ptr [ebp - 0x2c] ; 0x0086dd2c: mov eax, dword ptr [ebx + 0x1d0] ; 0x0086dd32: cmp edi, ecx ; 0x0086dd34: jb 0x86dea1
  - 0x0086dd34: jb -> 0x0086dd3a (jcc_false) | ctx: 0x0086dd29: mov edi, dword ptr [ebp - 0x2c] ; 0x0086dd2c: mov eax, dword ptr [ebx + 0x1d0] ; 0x0086dd32: cmp edi, ecx ; 0x0086dd34: jb 0x86dea1
  - 0x0086dd0e: je -> 0x0086dd18 (jcc_true) | ctx: 0x0086dd0a: test byte ptr [ebx + 4], 2 ; 0x0086dd0e: je 0x86dd18
  - 0x0086dd0e: je -> 0x0086dd10 (jcc_false) | ctx: 0x0086dd0a: test byte ptr [ebx + 4], 2 ; 0x0086dd0e: je 0x86dd18
  - 0x0086dc9c: jae -> 0x0086dcf6 (jcc_true) | ctx: 0x0086dc97: mov al, byte ptr [ebx + 4] ; 0x0086dc9a: cmp al, 0x80 ; 0x0086dc9c: jae 0x86dcf6
  - 0x0086dc9c: jae -> 0x0086dc9e (jcc_false) | ctx: 0x0086dc97: mov al, byte ptr [ebx + 4] ; 0x0086dc9a: cmp al, 0x80 ; 0x0086dc9c: jae 0x86dcf6
  - 0x0086db39: je -> 0x0086dd02 (jcc_true) | ctx: 0x0086db31: push esi ; 0x0086db32: call 0x84bb80 ; 0x0086db37: test al, al ; 0x0086db39: je 0x86dd02
  - 0x0086db39: je -> 0x0086db3f (jcc_false) | ctx: 0x0086db31: push esi ; 0x0086db32: call 0x84bb80 ; 0x0086db37: test al, al ; 0x0086db39: je 0x86dd02
  - 0x0086db22: jne -> 0x0086dc77 (jcc_true) | ctx: 0x0086db20: cmp edx, eax ; 0x0086db22: jne 0x86dc77
  - 0x0086db22: jne -> 0x0086db28 (jcc_false) | ctx: 0x0086db20: cmp edx, eax ; 0x0086db22: jne 0x86dc77
  - 0x0086e2d7: je -> 0x0086e8cc (jcc_true) | ctx: 0x0086e2c9: mov eax, dword ptr [ebx + 0x1e4] ; 0x0086e2cf: mov eax, dword ptr [eax] ; 0x0086e2d1: cmp eax, dword ptr [ebx + 0x1e4] ; 0x0086e2d7: je 0x86e8cc
  - 0x0086e2d7: je -> 0x0086e2dd (jcc_false) | ctx: 0x0086e2c9: mov eax, dword ptr [ebx + 0x1e4] ; 0x0086e2cf: mov eax, dword ptr [eax] ; 0x0086e2d1: cmp eax, dword ptr [ebx + 0x1e4] ; 0x0086e2d7: je 0x86e8cc
  - 0x0086e15b: ja -> 0x0086e16c (jcc_true) | ctx: 0x0086e15b: ja 0x86e16c
  - 0x0086e15b: ja -> 0x0086e15d (jcc_false) | ctx: 0x0086e15b: ja 0x86e16c
  - 0x0086dee2: jne -> 0x0086eb0a (jcc_true) | ctx: 0x0086dee0: test al, 0x40 ; 0x0086dee2: jne 0x86eb0a
  - 0x0086dee2: jne -> 0x0086dee8 (jcc_false) | ctx: 0x0086dee0: test al, 0x40 ; 0x0086dee2: jne 0x86eb0a
  - 0x0086deda: jbe -> 0x0086eb0a (jcc_true) | ctx: 0x0086ded1: mov ecx, dword ptr [ebp - 0x50] ; 0x0086ded4: cmp ecx, dword ptr [ebx + 0x1d8] ; 0x0086deda: jbe 0x86eb0a
  - 0x0086deda: jbe -> 0x0086dee0 (jcc_false) | ctx: 0x0086ded1: mov ecx, dword ptr [ebp - 0x50] ; 0x0086ded4: cmp ecx, dword ptr [ebx + 0x1d8] ; 0x0086deda: jbe 0x86eb0a
  - 0x0086dea8: jne -> 0x0086deb8 (jcc_true) | ctx: 0x0086dea1: cmp dword ptr [ebx + 0x1e0], 1 ; 0x0086dea8: jne 0x86deb8
  - 0x0086dea8: jne -> 0x0086deaa (jcc_false) | ctx: 0x0086dea1: cmp dword ptr [ebx + 0x1e0], 1 ; 0x0086dea8: jne 0x86deb8
  - 0x0086dd3d: ja -> 0x0086dd47 (jcc_true) | ctx: 0x0086dd3a: mov edi, dword ptr [ebp - 0x50] ; 0x0086dd3d: ja 0x86dd47
  - 0x0086dd3d: ja -> 0x0086dd3f (jcc_false) | ctx: 0x0086dd3a: mov edi, dword ptr [ebp - 0x50] ; 0x0086dd3d: ja 0x86dd47
  - 0x0086dd1d: je -> 0x0086de9e (jcc_true) | ctx: 0x0086dd18: mov eax, dword ptr [ebx + 0x5c] ; 0x0086dd1b: cmp ecx, eax ; 0x0086dd1d: je 0x86de9e
  - 0x0086dd1d: je -> 0x0086dd23 (jcc_false) | ctx: 0x0086dd18: mov eax, dword ptr [ebx + 0x5c] ; 0x0086dd1b: cmp ecx, eax ; 0x0086dd1d: je 0x86de9e
  - 0x0086dd16: jmp -> 0x0086dd1b (jmp) | ctx: 0x0086dd10: mov eax, dword ptr [ebx + 0x1a0] ; 0x0086dd16: jmp 0x86dd1b
  - 0x0086dd08: je -> 0x0086dd23 (jcc_true) | ctx: 0x0086dcfd: call 0x8580e0 ; 0x0086dd02: mov ecx, dword ptr [ebx + 0x60] ; 0x0086dd05: cmp ecx, -1 ; 0x0086dd08: je 0x86dd23
  - 0x0086dd08: je -> 0x0086dd0a (jcc_false) | ctx: 0x0086dcfd: call 0x8580e0 ; 0x0086dd02: mov ecx, dword ptr [ebx + 0x60] ; 0x0086dd05: cmp ecx, -1 ; 0x0086dd08: je 0x86dd23
  - 0x0086dca4: je -> 0x0086dd02 (jcc_true) | ctx: 0x0086dc9e: mov cl, byte ptr [ebx + 6] ; 0x0086dca1: test cl, 8 ; 0x0086dca4: je 0x86dd02
  - 0x0086dca4: je -> 0x0086dca6 (jcc_false) | ctx: 0x0086dc9e: mov cl, byte ptr [ebx + 6] ; 0x0086dca1: test cl, 8 ; 0x0086dca4: je 0x86dd02
  - 0x0086db44: jne -> 0x0086dba6 (jcc_true) | ctx: 0x0086db3f: mov al, byte ptr [ebx + 4] ; 0x0086db42: test al, 0x40 ; 0x0086db44: jne 0x86dba6
  - 0x0086db44: jne -> 0x0086db46 (jcc_false) | ctx: 0x0086db3f: mov al, byte ptr [ebx + 4] ; 0x0086db42: test al, 0x40 ; 0x0086db44: jne 0x86dba6
  - 0x0086e8da: je -> 0x0086eb0a (jcc_true) | ctx: 0x0086e8cc: mov eax, dword ptr [ebx + 0x1ec] ; 0x0086e8d2: mov eax, dword ptr [eax] ; 0x0086e8d4: cmp eax, dword ptr [ebx + 0x1ec] ; 0x0086e8da: je 0x86eb0a
  - 0x0086e8da: je -> 0x0086e8e0 (jcc_false) | ctx: 0x0086e8cc: mov eax, dword ptr [ebx + 0x1ec] ; 0x0086e8d2: mov eax, dword ptr [eax] ; 0x0086e8d4: cmp eax, dword ptr [ebx + 0x1ec] ; 0x0086e8da: je 0x86eb0a
  - 0x0086e2f1: jb -> 0x0086e8bf (jcc_true) | ctx: 0x0086e2e8: mov eax, dword ptr [ebp - 0x2c] ; 0x0086e2eb: mov dword ptr [ebp - 0x14], esi ; 0x0086e2ee: cmp eax, dword ptr [edi + 0x2c] ; 0x0086e2f1: jb 0x86e8bf
  - 0x0086e2f1: jb -> 0x0086e2f7 (jcc_false) | ctx: 0x0086e2e8: mov eax, dword ptr [ebp - 0x2c] ; 0x0086e2eb: mov dword ptr [ebp - 0x14], esi ; 0x0086e2ee: cmp eax, dword ptr [edi + 0x2c] ; 0x0086e2f1: jb 0x86e8bf
  - 0x0086e17c: je -> 0x0086e267 (jcc_true) | ctx: 0x0086e174: sar eax, 2 ; 0x0086e177: mov dword ptr [ebp - 0x14], edi ; 0x0086e17a: test eax, eax ; 0x0086e17c: je 0x86e267
  - 0x0086e17c: je -> 0x0086e182 (jcc_false) | ctx: 0x0086e174: sar eax, 2 ; 0x0086e177: mov dword ptr [ebp - 0x14], edi ; 0x0086e17a: test eax, eax ; 0x0086e17c: je 0x86e267
  - 0x0086e166: jbe -> 0x0086eb0a (jcc_true) | ctx: 0x0086e15d: mov eax, dword ptr [ebp - 0x50] ; 0x0086e160: cmp eax, dword ptr [ebx + 0x190] ; 0x0086e166: jbe 0x86eb0a
  - 0x0086e166: jbe -> 0x0086e16c (jcc_false) | ctx: 0x0086e15d: mov eax, dword ptr [ebp - 0x50] ; 0x0086e160: cmp eax, dword ptr [ebx + 0x190] ; 0x0086e166: jbe 0x86eb0a
  - 0x0086deea: jne -> 0x0086dfb0 (jcc_true) | ctx: 0x0086dee8: test al, 8 ; 0x0086deea: jne 0x86dfb0
  - 0x0086deea: jne -> 0x0086def0 (jcc_false) | ctx: 0x0086dee8: test al, 8 ; 0x0086deea: jne 0x86dfb0
  - 0x0086dd49: jne -> 0x0086dd53 (jcc_true) | ctx: 0x0086dd47: test ecx, ecx ; 0x0086dd49: jne 0x86dd53
  - 0x0086dd49: jne -> 0x0086dd4b (jcc_false) | ctx: 0x0086dd47: test ecx, ecx ; 0x0086dd49: jne 0x86dd53
  - 0x0086dd41: jbe -> 0x0086de9e (jcc_true) | ctx: 0x0086dd3f: cmp edi, eax ; 0x0086dd41: jbe 0x86de9e
  - 0x0086dd41: jbe -> 0x0086dd47 (jcc_false) | ctx: 0x0086dd3f: cmp edi, eax ; 0x0086dd41: jbe 0x86de9e
  - ... 192 more

### 0x00871230
- blocks=3, insns=14, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00871242)
- branch points:
  - 0x0087123b: je -> 0x00871247 (jcc_true) | ctx: 0x00871233: mov eax, dword ptr [ebp + 8] ; 0x00871236: add ecx, 0x4c ; 0x00871239: cmp ecx, eax ; 0x0087123b: je 0x871247
  - 0x0087123b: je -> 0x0087123d (jcc_false) | ctx: 0x00871233: mov eax, dword ptr [ebp + 8] ; 0x00871236: add ecx, 0x4c ; 0x00871239: cmp ecx, eax ; 0x0087123b: je 0x871247

### 0x0087f0a9
- blocks=6, insns=99, edges=14, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0087f108)
- branch points:
  - 0x0087f0f1: jb -> 0x0087f0f8 (jcc_true) | ctx: 0x0087f0df: mov dword ptr [esi + 0x24], 0xf ; 0x0087f0e6: mov dword ptr [esi + 0x20], 0 ; 0x0087f0ed: cmp dword ptr [esi + 0x24], 0x10 ; 0x0087f0f1: jb 0x87f0f8
  - 0x0087f0f1: jb -> 0x0087f0f3 (jcc_false) | ctx: 0x0087f0df: mov dword ptr [esi + 0x24], 0xf ; 0x0087f0e6: mov dword ptr [esi + 0x20], 0 ; 0x0087f0ed: cmp dword ptr [esi + 0x24], 0x10 ; 0x0087f0f1: jb 0x87f0f8
  - 0x0087f122: jb -> 0x0087f126 (jcc_true) | ctx: 0x0087f110: mov dword ptr [eax + 0x14], 0xf ; 0x0087f117: mov dword ptr [eax + 0x10], 0 ; 0x0087f11e: cmp dword ptr [eax + 0x14], 0x10 ; 0x0087f122: jb 0x87f126
  - 0x0087f122: jb -> 0x0087f124 (jcc_false) | ctx: 0x0087f110: mov dword ptr [eax + 0x14], 0xf ; 0x0087f117: mov dword ptr [eax + 0x10], 0 ; 0x0087f11e: cmp dword ptr [eax + 0x14], 0x10 ; 0x0087f122: jb 0x87f126
  - 0x0087f0f6: jmp -> 0x0087f0fb (jmp) | ctx: 0x0087f0f3: mov eax, dword ptr [esi + 0x10] ; 0x0087f0f6: jmp 0x87f0fb
  - 0x0087f122: jb -> 0x0087f126 (jcc_true) | ctx: 0x0087f110: mov dword ptr [eax + 0x14], 0xf ; 0x0087f117: mov dword ptr [eax + 0x10], 0 ; 0x0087f11e: cmp dword ptr [eax + 0x14], 0x10 ; 0x0087f122: jb 0x87f126
  - 0x0087f122: jb -> 0x0087f124 (jcc_false) | ctx: 0x0087f110: mov dword ptr [eax + 0x14], 0xf ; 0x0087f117: mov dword ptr [eax + 0x10], 0 ; 0x0087f11e: cmp dword ptr [eax + 0x14], 0x10 ; 0x0087f122: jb 0x87f126

### 0x00882ccc
- blocks=8, insns=75, edges=18, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00882d3f)
- branch points:
  - 0x00882cf7: jb -> 0x00882cfd (jcc_true) | ctx: 0x00882ce5: mov dword ptr [esi + 0x14], 0xf ; 0x00882cec: mov dword ptr [esi + 0x10], 0 ; 0x00882cf3: cmp dword ptr [esi + 0x14], 0x10 ; 0x00882cf7: jb 0x882cfd
  - 0x00882cf7: jb -> 0x00882cf9 (jcc_false) | ctx: 0x00882ce5: mov dword ptr [esi + 0x14], 0xf ; 0x00882cec: mov dword ptr [esi + 0x10], 0 ; 0x00882cf3: cmp dword ptr [esi + 0x14], 0x10 ; 0x00882cf7: jb 0x882cfd
  - 0x00882d36: je -> 0x00882d44 (jcc_true) | ctx: 0x00882d2c: call 0x8857d0 ; 0x00882d31: lea eax, [ebp - 0x28] ; 0x00882d34: cmp esi, eax ; 0x00882d36: je 0x882d44
  - 0x00882d36: je -> 0x00882d38 (jcc_false) | ctx: 0x00882d2c: call 0x8857d0 ; 0x00882d31: lea eax, [ebp - 0x28] ; 0x00882d34: cmp esi, eax ; 0x00882d36: je 0x882d44
  - 0x00882cfb: jmp -> 0x00882cff (jmp) | ctx: 0x00882cf9: mov eax, dword ptr [esi] ; 0x00882cfb: jmp 0x882cff
  - 0x00882d4c: jb -> 0x00882d59 (jcc_true) | ctx: 0x00882d44: cmp dword ptr [ebp - 0x14], 0x10 ; 0x00882d48: mov byte ptr [ebp - 4], 3 ; 0x00882d4c: jb 0x882d59
  - 0x00882d4c: jb -> 0x00882d4e (jcc_false) | ctx: 0x00882d44: cmp dword ptr [ebp - 0x14], 0x10 ; 0x00882d48: mov byte ptr [ebp - 4], 3 ; 0x00882d4c: jb 0x882d59
  - 0x00882d4c: jb -> 0x00882d59 (jcc_true) | ctx: 0x00882d3f: call 0x5c5420 ; 0x00882d44: cmp dword ptr [ebp - 0x14], 0x10 ; 0x00882d48: mov byte ptr [ebp - 4], 3 ; 0x00882d4c: jb 0x882d59
  - 0x00882d4c: jb -> 0x00882d4e (jcc_false) | ctx: 0x00882d3f: call 0x5c5420 ; 0x00882d44: cmp dword ptr [ebp - 0x14], 0x10 ; 0x00882d48: mov byte ptr [ebp - 4], 3 ; 0x00882d4c: jb 0x882d59
  - 0x00882d36: je -> 0x00882d44 (jcc_true) | ctx: 0x00882d2c: call 0x8857d0 ; 0x00882d31: lea eax, [ebp - 0x28] ; 0x00882d34: cmp esi, eax ; 0x00882d36: je 0x882d44
  - 0x00882d36: je -> 0x00882d38 (jcc_false) | ctx: 0x00882d2c: call 0x8857d0 ; 0x00882d31: lea eax, [ebp - 0x28] ; 0x00882d34: cmp esi, eax ; 0x00882d36: je 0x882d44

### 0x00885423
- blocks=13, insns=127, edges=29, jcc=11, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x008854a1)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x008854b5)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x008854c9)
- branch points:
  - 0x00885450: je -> 0x00885456 (jcc_true) | ctx: 0x00885448: mov eax, dword ptr [edi + 0x1c] ; 0x0088544b: mov ecx, dword ptr [edi + 0x18] ; 0x0088544e: test eax, eax ; 0x00885450: je 0x885456
  - 0x00885450: je -> 0x00885452 (jcc_false) | ctx: 0x00885448: mov eax, dword ptr [edi + 0x1c] ; 0x0088544b: mov ecx, dword ptr [edi + 0x18] ; 0x0088544e: test eax, eax ; 0x00885450: je 0x885456
  - 0x00885462: je -> 0x00885485 (jcc_true) | ctx: 0x0088545a: mov dword ptr [esi + 0x1c], eax ; 0x0088545d: mov dword ptr [esi + 0x18], ecx ; 0x00885460: test ebx, ebx ; 0x00885462: je 0x885485
  - 0x00885462: je -> 0x00885464 (jcc_false) | ctx: 0x0088545a: mov dword ptr [esi + 0x1c], eax ; 0x0088545d: mov dword ptr [esi + 0x18], ecx ; 0x00885460: test ebx, ebx ; 0x00885462: je 0x885485
  - 0x00885462: je -> 0x00885485 (jcc_true) | ctx: 0x0088545a: mov dword ptr [esi + 0x1c], eax ; 0x0088545d: mov dword ptr [esi + 0x18], ecx ; 0x00885460: test ebx, ebx ; 0x00885462: je 0x885485
  - 0x00885462: je -> 0x00885464 (jcc_false) | ctx: 0x0088545a: mov dword ptr [esi + 0x1c], eax ; 0x0088545d: mov dword ptr [esi + 0x18], ecx ; 0x00885460: test ebx, ebx ; 0x00885462: je 0x885485
  - 0x0088549a: je -> 0x008854a6 (jcc_true) | ctx: 0x00885494: lea eax, [edi + 0x28] ; 0x00885497: pop ebx ; 0x00885498: cmp ecx, eax ; 0x0088549a: je 0x8854a6
  - 0x0088549a: je -> 0x0088549c (jcc_false) | ctx: 0x00885494: lea eax, [edi + 0x28] ; 0x00885497: pop ebx ; 0x00885498: cmp ecx, eax ; 0x0088549a: je 0x8854a6
  - 0x0088546c: jne -> 0x00885485 (jcc_true) | ctx: 0x00885464: or eax, 0xffffffff ; 0x00885467: lock xadd dword ptr [ebx + 4], eax ; 0x0088546c: jne 0x885485
  - 0x0088546c: jne -> 0x0088546e (jcc_false) | ctx: 0x00885464: or eax, 0xffffffff ; 0x00885467: lock xadd dword ptr [ebx + 4], eax ; 0x0088546c: jne 0x885485
  - 0x008854ae: je -> 0x008854ba (jcc_true) | ctx: 0x008854a6: lea eax, [edi + 0x40] ; 0x008854a9: lea ecx, [esi + 0x40] ; 0x008854ac: cmp ecx, eax ; 0x008854ae: je 0x8854ba
  - 0x008854ae: je -> 0x008854b0 (jcc_false) | ctx: 0x008854a6: lea eax, [edi + 0x40] ; 0x008854a9: lea ecx, [esi + 0x40] ; 0x008854ac: cmp ecx, eax ; 0x008854ae: je 0x8854ba
  - 0x008854ae: je -> 0x008854ba (jcc_true) | ctx: 0x008854a6: lea eax, [edi + 0x40] ; 0x008854a9: lea ecx, [esi + 0x40] ; 0x008854ac: cmp ecx, eax ; 0x008854ae: je 0x8854ba
  - 0x008854ae: je -> 0x008854b0 (jcc_false) | ctx: 0x008854a6: lea eax, [edi + 0x40] ; 0x008854a9: lea ecx, [esi + 0x40] ; 0x008854ac: cmp ecx, eax ; 0x008854ae: je 0x8854ba
  - 0x0088547c: jne -> 0x00885485 (jcc_true) | ctx: 0x00885472: call dword ptr [eax] ; 0x00885474: or eax, 0xffffffff ; 0x00885477: lock xadd dword ptr [ebx + 8], eax ; 0x0088547c: jne 0x885485
  - 0x0088547c: jne -> 0x0088547e (jcc_false) | ctx: 0x00885472: call dword ptr [eax] ; 0x00885474: or eax, 0xffffffff ; 0x00885477: lock xadd dword ptr [ebx + 8], eax ; 0x0088547c: jne 0x885485
  - 0x008854c2: je -> 0x008854ce (jcc_true) | ctx: 0x008854ba: lea eax, [edi + 0x58] ; 0x008854bd: lea ecx, [esi + 0x58] ; 0x008854c0: cmp ecx, eax ; 0x008854c2: je 0x8854ce
  - 0x008854c2: je -> 0x008854c4 (jcc_false) | ctx: 0x008854ba: lea eax, [edi + 0x58] ; 0x008854bd: lea ecx, [esi + 0x58] ; 0x008854c0: cmp ecx, eax ; 0x008854c2: je 0x8854ce
  - 0x008854c2: je -> 0x008854ce (jcc_true) | ctx: 0x008854ba: lea eax, [edi + 0x58] ; 0x008854bd: lea ecx, [esi + 0x58] ; 0x008854c0: cmp ecx, eax ; 0x008854c2: je 0x8854ce
  - 0x008854c2: je -> 0x008854c4 (jcc_false) | ctx: 0x008854ba: lea eax, [edi + 0x58] ; 0x008854bd: lea ecx, [esi + 0x58] ; 0x008854c0: cmp ecx, eax ; 0x008854c2: je 0x8854ce
  - 0x0088549a: je -> 0x008854a6 (jcc_true) | ctx: 0x00885494: lea eax, [edi + 0x28] ; 0x00885497: pop ebx ; 0x00885498: cmp ecx, eax ; 0x0088549a: je 0x8854a6
  - 0x0088549a: je -> 0x0088549c (jcc_false) | ctx: 0x00885494: lea eax, [edi + 0x28] ; 0x00885497: pop ebx ; 0x00885498: cmp ecx, eax ; 0x0088549a: je 0x8854a6

### 0x008856a3
- blocks=13, insns=159, edges=27, jcc=11, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00885763)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00885777)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00885791)
- branch points:
  - 0x008856c4: je -> 0x008856ca (jcc_true) | ctx: 0x008856bc: mov eax, dword ptr [edi + 0x14] ; 0x008856bf: mov ecx, dword ptr [edi + 0x10] ; 0x008856c2: test eax, eax ; 0x008856c4: je 0x8856ca
  - 0x008856c4: je -> 0x008856c6 (jcc_false) | ctx: 0x008856bc: mov eax, dword ptr [edi + 0x14] ; 0x008856bf: mov ecx, dword ptr [edi + 0x10] ; 0x008856c2: test eax, eax ; 0x008856c4: je 0x8856ca
  - 0x008856d6: je -> 0x008856f9 (jcc_true) | ctx: 0x008856ce: mov dword ptr [esi + 0x14], eax ; 0x008856d1: mov dword ptr [esi + 0x10], ecx ; 0x008856d4: test ebx, ebx ; 0x008856d6: je 0x8856f9
  - 0x008856d6: je -> 0x008856d8 (jcc_false) | ctx: 0x008856ce: mov dword ptr [esi + 0x14], eax ; 0x008856d1: mov dword ptr [esi + 0x10], ecx ; 0x008856d4: test ebx, ebx ; 0x008856d6: je 0x8856f9
  - 0x008856d6: je -> 0x008856f9 (jcc_true) | ctx: 0x008856ce: mov dword ptr [esi + 0x14], eax ; 0x008856d1: mov dword ptr [esi + 0x10], ecx ; 0x008856d4: test ebx, ebx ; 0x008856d6: je 0x8856f9
  - 0x008856d6: je -> 0x008856d8 (jcc_false) | ctx: 0x008856ce: mov dword ptr [esi + 0x14], eax ; 0x008856d1: mov dword ptr [esi + 0x10], ecx ; 0x008856d4: test ebx, ebx ; 0x008856d6: je 0x8856f9
  - 0x0088575c: je -> 0x00885768 (jcc_true) | ctx: 0x00885756: lea eax, [edi + 0x54] ; 0x00885759: pop ebx ; 0x0088575a: cmp ecx, eax ; 0x0088575c: je 0x885768
  - 0x0088575c: je -> 0x0088575e (jcc_false) | ctx: 0x00885756: lea eax, [edi + 0x54] ; 0x00885759: pop ebx ; 0x0088575a: cmp ecx, eax ; 0x0088575c: je 0x885768
  - 0x008856e0: jne -> 0x008856f9 (jcc_true) | ctx: 0x008856d8: or eax, 0xffffffff ; 0x008856db: lock xadd dword ptr [ebx + 4], eax ; 0x008856e0: jne 0x8856f9
  - 0x008856e0: jne -> 0x008856e2 (jcc_false) | ctx: 0x008856d8: or eax, 0xffffffff ; 0x008856db: lock xadd dword ptr [ebx + 4], eax ; 0x008856e0: jne 0x8856f9
  - 0x00885770: je -> 0x0088577c (jcc_true) | ctx: 0x00885768: lea eax, [edi + 0x6c] ; 0x0088576b: lea ecx, [esi + 0x6c] ; 0x0088576e: cmp ecx, eax ; 0x00885770: je 0x88577c
  - 0x00885770: je -> 0x00885772 (jcc_false) | ctx: 0x00885768: lea eax, [edi + 0x6c] ; 0x0088576b: lea ecx, [esi + 0x6c] ; 0x0088576e: cmp ecx, eax ; 0x00885770: je 0x88577c
  - 0x00885770: je -> 0x0088577c (jcc_true) | ctx: 0x00885768: lea eax, [edi + 0x6c] ; 0x0088576b: lea ecx, [esi + 0x6c] ; 0x0088576e: cmp ecx, eax ; 0x00885770: je 0x88577c
  - 0x00885770: je -> 0x00885772 (jcc_false) | ctx: 0x00885768: lea eax, [edi + 0x6c] ; 0x0088576b: lea ecx, [esi + 0x6c] ; 0x0088576e: cmp ecx, eax ; 0x00885770: je 0x88577c
  - 0x008856f0: jne -> 0x008856f9 (jcc_true) | ctx: 0x008856e6: call dword ptr [eax] ; 0x008856e8: or eax, 0xffffffff ; 0x008856eb: lock xadd dword ptr [ebx + 8], eax ; 0x008856f0: jne 0x8856f9
  - 0x008856f0: jne -> 0x008856f2 (jcc_false) | ctx: 0x008856e6: call dword ptr [eax] ; 0x008856e8: or eax, 0xffffffff ; 0x008856eb: lock xadd dword ptr [ebx + 8], eax ; 0x008856f0: jne 0x8856f9
  - 0x0088578a: je -> 0x00885796 (jcc_true) | ctx: 0x0088577c: lea eax, [edi + 0x84] ; 0x00885782: lea ecx, [esi + 0x84] ; 0x00885788: cmp ecx, eax ; 0x0088578a: je 0x885796
  - 0x0088578a: je -> 0x0088578c (jcc_false) | ctx: 0x0088577c: lea eax, [edi + 0x84] ; 0x00885782: lea ecx, [esi + 0x84] ; 0x00885788: cmp ecx, eax ; 0x0088578a: je 0x885796
  - 0x0088578a: je -> 0x00885796 (jcc_true) | ctx: 0x0088577c: lea eax, [edi + 0x84] ; 0x00885782: lea ecx, [esi + 0x84] ; 0x00885788: cmp ecx, eax ; 0x0088578a: je 0x885796
  - 0x0088578a: je -> 0x0088578c (jcc_false) | ctx: 0x0088577c: lea eax, [edi + 0x84] ; 0x00885782: lea ecx, [esi + 0x84] ; 0x00885788: cmp ecx, eax ; 0x0088578a: je 0x885796
  - 0x0088575c: je -> 0x00885768 (jcc_true) | ctx: 0x00885756: lea eax, [edi + 0x54] ; 0x00885759: pop ebx ; 0x0088575a: cmp ecx, eax ; 0x0088575c: je 0x885768
  - 0x0088575c: je -> 0x0088575e (jcc_false) | ctx: 0x00885756: lea eax, [edi + 0x54] ; 0x00885759: pop ebx ; 0x0088575a: cmp ecx, eax ; 0x0088575c: je 0x885768

### 0x00887c20
- blocks=14, insns=166, edges=40, jcc=9, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00887c8c)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00887d27)
- branch points:
  - 0x00887c45: je -> 0x00887d76 (jcc_true) | ctx: 0x00887c40: mov ebx, ecx ; 0x00887c42: push edi ; 0x00887c43: test esi, esi ; 0x00887c45: je 0x887d76
  - 0x00887c45: je -> 0x00887c4b (jcc_false) | ctx: 0x00887c40: mov ebx, ecx ; 0x00887c42: push edi ; 0x00887c43: test esi, esi ; 0x00887c45: je 0x887d76
  - 0x00887c52: jne -> 0x00887c5b (jcc_true) | ctx: 0x00887c4b: cmp dword ptr [0xf8fd24], 0 ; 0x00887c52: jne 0x887c5b
  - 0x00887c52: jne -> 0x00887c54 (jcc_false) | ctx: 0x00887c4b: cmp dword ptr [0xf8fd24], 0 ; 0x00887c52: jne 0x887c5b
  - 0x00887c66: jb -> 0x00887d76 (jcc_true) | ctx: 0x00887c5d: mov ecx, esi ; 0x00887c5f: call dword ptr [eax + 4] ; 0x00887c62: cmp dword ptr [eax + 8], 3 ; 0x00887c66: jb 0x887d76
  - 0x00887c66: jb -> 0x00887c6c (jcc_false) | ctx: 0x00887c5d: mov ecx, esi ; 0x00887c5f: call dword ptr [eax + 4] ; 0x00887c62: cmp dword ptr [eax + 8], 3 ; 0x00887c66: jb 0x887d76
  - 0x00887c66: jb -> 0x00887d76 (jcc_true) | ctx: 0x00887c5d: mov ecx, esi ; 0x00887c5f: call dword ptr [eax + 4] ; 0x00887c62: cmp dword ptr [eax + 8], 3 ; 0x00887c66: jb 0x887d76
  - 0x00887c66: jb -> 0x00887c6c (jcc_false) | ctx: 0x00887c5d: mov ecx, esi ; 0x00887c5f: call dword ptr [eax + 4] ; 0x00887c62: cmp dword ptr [eax + 8], 3 ; 0x00887c66: jb 0x887d76
  - 0x00887c75: jne -> 0x00887d76 (jcc_true) | ctx: 0x00887c6c: mov eax, dword ptr [eax + 0x14] ; 0x00887c6f: cmp eax, dword ptr [0xf8fd38] ; 0x00887c75: jne 0x887d76
  - 0x00887c75: jne -> 0x00887c7b (jcc_false) | ctx: 0x00887c6c: mov eax, dword ptr [eax + 0x14] ; 0x00887c6f: cmp eax, dword ptr [0xf8fd38] ; 0x00887c75: jne 0x887d76
  - 0x00887c83: je -> 0x00887c91 (jcc_true) | ctx: 0x00887c7b: lea ecx, [esi + 0x28] ; 0x00887c7e: lea eax, [ebx + 0x54] ; 0x00887c81: cmp eax, ecx ; 0x00887c83: je 0x887c91
  - 0x00887c83: je -> 0x00887c85 (jcc_false) | ctx: 0x00887c7b: lea ecx, [esi + 0x28] ; 0x00887c7e: lea eax, [ebx + 0x54] ; 0x00887c81: cmp eax, ecx ; 0x00887c83: je 0x887c91
  - 0x00887caa: jne -> 0x00887d64 (jcc_true) | ctx: 0x00887c9d: call 0x931340 ; 0x00887ca2: mov eax, dword ptr [eax] ; 0x00887ca4: cmp eax, dword ptr [0xd6ba18] ; 0x00887caa: jne 0x887d64
  - 0x00887caa: jne -> 0x00887cb0 (jcc_false) | ctx: 0x00887c9d: call 0x931340 ; 0x00887ca2: mov eax, dword ptr [eax] ; 0x00887ca4: cmp eax, dword ptr [0xd6ba18] ; 0x00887caa: jne 0x887d64
  - 0x00887caa: jne -> 0x00887d64 (jcc_true) | ctx: 0x00887c9d: call 0x931340 ; 0x00887ca2: mov eax, dword ptr [eax] ; 0x00887ca4: cmp eax, dword ptr [0xd6ba18] ; 0x00887caa: jne 0x887d64
  - 0x00887caa: jne -> 0x00887cb0 (jcc_false) | ctx: 0x00887c9d: call 0x931340 ; 0x00887ca2: mov eax, dword ptr [eax] ; 0x00887ca4: cmp eax, dword ptr [0xd6ba18] ; 0x00887caa: jne 0x887d64
  - 0x00887d74: jmp -> 0x00887d7f (jmp) | ctx: 0x00887d66: call 0x8aa560 ; 0x00887d6b: mov eax, dword ptr [ebp + 8] ; 0x00887d6e: mov dword ptr [eax], 1 ; 0x00887d74: jmp 0x887d7f
  - 0x00887d20: je -> 0x00887d2c (jcc_true) | ctx: 0x00887d18: mov dword ptr [ebp - 0x4c], esi ; 0x00887d1b: lea eax, [ebx + 0x54] ; 0x00887d1e: cmp ecx, eax ; 0x00887d20: je 0x887d2c
  - 0x00887d20: je -> 0x00887d22 (jcc_false) | ctx: 0x00887d18: mov dword ptr [ebp - 0x4c], esi ; 0x00887d1b: lea eax, [ebx + 0x54] ; 0x00887d1e: cmp ecx, eax ; 0x00887d20: je 0x887d2c
  - 0x00887d74: jmp -> 0x00887d7f (jmp) | ctx: 0x00887d66: call 0x8aa560 ; 0x00887d6b: mov eax, dword ptr [ebp + 8] ; 0x00887d6e: mov dword ptr [eax], 1 ; 0x00887d74: jmp 0x887d7f
  - 0x00887d74: jmp -> 0x00887d7f (jmp) | ctx: 0x00887d66: call 0x8aa560 ; 0x00887d6b: mov eax, dword ptr [ebp + 8] ; 0x00887d6e: mov dword ptr [eax], 1 ; 0x00887d74: jmp 0x887d7f

### 0x00887e70
- blocks=14, insns=158, edges=37, jcc=9, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00887edc)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00887f77)
- branch points:
  - 0x00887e95: je -> 0x00887fb8 (jcc_true) | ctx: 0x00887e90: mov ebx, ecx ; 0x00887e92: push edi ; 0x00887e93: test esi, esi ; 0x00887e95: je 0x887fb8
  - 0x00887e95: je -> 0x00887e9b (jcc_false) | ctx: 0x00887e90: mov ebx, ecx ; 0x00887e92: push edi ; 0x00887e93: test esi, esi ; 0x00887e95: je 0x887fb8
  - 0x00887ea2: jne -> 0x00887eab (jcc_true) | ctx: 0x00887e9b: cmp dword ptr [0xf8fd48], 0 ; 0x00887ea2: jne 0x887eab
  - 0x00887ea2: jne -> 0x00887ea4 (jcc_false) | ctx: 0x00887e9b: cmp dword ptr [0xf8fd48], 0 ; 0x00887ea2: jne 0x887eab
  - 0x00887eb6: jb -> 0x00887fb8 (jcc_true) | ctx: 0x00887ead: mov ecx, esi ; 0x00887eaf: call dword ptr [eax + 4] ; 0x00887eb2: cmp dword ptr [eax + 8], 3 ; 0x00887eb6: jb 0x887fb8
  - 0x00887eb6: jb -> 0x00887ebc (jcc_false) | ctx: 0x00887ead: mov ecx, esi ; 0x00887eaf: call dword ptr [eax + 4] ; 0x00887eb2: cmp dword ptr [eax + 8], 3 ; 0x00887eb6: jb 0x887fb8
  - 0x00887eb6: jb -> 0x00887fb8 (jcc_true) | ctx: 0x00887ead: mov ecx, esi ; 0x00887eaf: call dword ptr [eax + 4] ; 0x00887eb2: cmp dword ptr [eax + 8], 3 ; 0x00887eb6: jb 0x887fb8
  - 0x00887eb6: jb -> 0x00887ebc (jcc_false) | ctx: 0x00887ead: mov ecx, esi ; 0x00887eaf: call dword ptr [eax + 4] ; 0x00887eb2: cmp dword ptr [eax + 8], 3 ; 0x00887eb6: jb 0x887fb8
  - 0x00887ec5: jne -> 0x00887fb8 (jcc_true) | ctx: 0x00887ebc: mov eax, dword ptr [eax + 0x14] ; 0x00887ebf: cmp eax, dword ptr [0xf8fd5c] ; 0x00887ec5: jne 0x887fb8
  - 0x00887ec5: jne -> 0x00887ecb (jcc_false) | ctx: 0x00887ebc: mov eax, dword ptr [eax + 0x14] ; 0x00887ebf: cmp eax, dword ptr [0xf8fd5c] ; 0x00887ec5: jne 0x887fb8
  - 0x00887ed3: je -> 0x00887ee1 (jcc_true) | ctx: 0x00887ecb: lea ecx, [esi + 0x28] ; 0x00887ece: lea eax, [ebx + 0x54] ; 0x00887ed1: cmp eax, ecx ; 0x00887ed3: je 0x887ee1
  - 0x00887ed3: je -> 0x00887ed5 (jcc_false) | ctx: 0x00887ecb: lea ecx, [esi + 0x28] ; 0x00887ece: lea eax, [ebx + 0x54] ; 0x00887ed1: cmp eax, ecx ; 0x00887ed3: je 0x887ee1
  - 0x00887efa: jne -> 0x00887fad (jcc_true) | ctx: 0x00887eed: call 0x931340 ; 0x00887ef2: mov eax, dword ptr [eax] ; 0x00887ef4: cmp eax, dword ptr [0xd6ba18] ; 0x00887efa: jne 0x887fad
  - 0x00887efa: jne -> 0x00887f00 (jcc_false) | ctx: 0x00887eed: call 0x931340 ; 0x00887ef2: mov eax, dword ptr [eax] ; 0x00887ef4: cmp eax, dword ptr [0xd6ba18] ; 0x00887efa: jne 0x887fad
  - 0x00887efa: jne -> 0x00887fad (jcc_true) | ctx: 0x00887eed: call 0x931340 ; 0x00887ef2: mov eax, dword ptr [eax] ; 0x00887ef4: cmp eax, dword ptr [0xd6ba18] ; 0x00887efa: jne 0x887fad
  - 0x00887efa: jne -> 0x00887f00 (jcc_false) | ctx: 0x00887eed: call 0x931340 ; 0x00887ef2: mov eax, dword ptr [eax] ; 0x00887ef4: cmp eax, dword ptr [0xd6ba18] ; 0x00887efa: jne 0x887fad
  - 0x00887fb6: jmp -> 0x00887fc1 (jmp) | ctx: 0x00887fad: mov eax, dword ptr [ebp + 8] ; 0x00887fb0: mov dword ptr [eax], 1 ; 0x00887fb6: jmp 0x887fc1
  - 0x00887f70: je -> 0x00887f7c (jcc_true) | ctx: 0x00887f68: mov dword ptr [ebp - 0x4c], esi ; 0x00887f6b: lea eax, [ebx + 0x54] ; 0x00887f6e: cmp ecx, eax ; 0x00887f70: je 0x887f7c
  - 0x00887f70: je -> 0x00887f72 (jcc_false) | ctx: 0x00887f68: mov dword ptr [ebp - 0x4c], esi ; 0x00887f6b: lea eax, [ebx + 0x54] ; 0x00887f6e: cmp ecx, eax ; 0x00887f70: je 0x887f7c
  - 0x00887fb6: jmp -> 0x00887fc1 (jmp) | ctx: 0x00887fa8: call 0x884870 ; 0x00887fad: mov eax, dword ptr [ebp + 8] ; 0x00887fb0: mov dword ptr [eax], 1 ; 0x00887fb6: jmp 0x887fc1
  - 0x00887fb6: jmp -> 0x00887fc1 (jmp) | ctx: 0x00887fa8: call 0x884870 ; 0x00887fad: mov eax, dword ptr [ebp + 8] ; 0x00887fb0: mov dword ptr [eax], 1 ; 0x00887fb6: jmp 0x887fc1

### 0x00887fe0
- blocks=93, insns=676, edges=230, jcc=83, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00888174)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00888250)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00888284)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088848c)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x008884a3)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x008884ba)
- branch points:
  - 0x0088801d: je -> 0x0088804a (jcc_true) | ctx: 0x00888015: push edi ; 0x00888016: mov edi, 0xfff0be1c ; 0x0088801b: test esi, esi ; 0x0088801d: je 0x88804a
  - 0x0088801d: je -> 0x0088801f (jcc_false) | ctx: 0x00888015: push edi ; 0x00888016: mov edi, 0xfff0be1c ; 0x0088801b: test esi, esi ; 0x0088801d: je 0x88804a
  - 0x00888053: je -> 0x00888080 (jcc_true) | ctx: 0x0088804a: mov dword ptr [ebp + 0xc], 0 ; 0x00888051: test esi, esi ; 0x00888053: je 0x888080
  - 0x00888053: je -> 0x00888055 (jcc_false) | ctx: 0x0088804a: mov dword ptr [ebp + 0xc], 0 ; 0x00888051: test esi, esi ; 0x00888053: je 0x888080
  - 0x00888026: jne -> 0x0088802f (jcc_true) | ctx: 0x0088801f: cmp dword ptr [0xf8f4e0], 0 ; 0x00888026: jne 0x88802f
  - 0x00888026: jne -> 0x00888028 (jcc_false) | ctx: 0x0088801f: cmp dword ptr [0xf8f4e0], 0 ; 0x00888026: jne 0x88802f
  - 0x00888089: je -> 0x008880b6 (jcc_true) | ctx: 0x00888080: mov dword ptr [ebp - 0x10], 0 ; 0x00888087: test esi, esi ; 0x00888089: je 0x8880b6
  - 0x00888089: je -> 0x0088808b (jcc_false) | ctx: 0x00888080: mov dword ptr [ebp - 0x10], 0 ; 0x00888087: test esi, esi ; 0x00888089: je 0x8880b6
  - 0x0088805c: jne -> 0x00888065 (jcc_true) | ctx: 0x00888055: cmp dword ptr [0xf8f528], 0 ; 0x0088805c: jne 0x888065
  - 0x0088805c: jne -> 0x0088805e (jcc_false) | ctx: 0x00888055: cmp dword ptr [0xf8f528], 0 ; 0x0088805c: jne 0x888065
  - 0x0088803a: jb -> 0x0088804a (jcc_true) | ctx: 0x00888031: mov ecx, esi ; 0x00888033: call dword ptr [eax + 4] ; 0x00888036: cmp dword ptr [eax + 8], 3 ; 0x0088803a: jb 0x88804a
  - 0x0088803a: jb -> 0x0088803c (jcc_false) | ctx: 0x00888031: mov ecx, esi ; 0x00888033: call dword ptr [eax + 4] ; 0x00888036: cmp dword ptr [eax + 8], 3 ; 0x0088803a: jb 0x88804a
  - 0x0088803a: jb -> 0x0088804a (jcc_true) | ctx: 0x00888031: mov ecx, esi ; 0x00888033: call dword ptr [eax + 4] ; 0x00888036: cmp dword ptr [eax + 8], 3 ; 0x0088803a: jb 0x88804a
  - 0x0088803a: jb -> 0x0088803c (jcc_false) | ctx: 0x00888031: mov ecx, esi ; 0x00888033: call dword ptr [eax + 4] ; 0x00888036: cmp dword ptr [eax + 8], 3 ; 0x0088803a: jb 0x88804a
  - 0x008880bf: je -> 0x008880ec (jcc_true) | ctx: 0x008880b6: mov dword ptr [ebp - 0x14], 0 ; 0x008880bd: test esi, esi ; 0x008880bf: je 0x8880ec
  - 0x008880bf: je -> 0x008880c1 (jcc_false) | ctx: 0x008880b6: mov dword ptr [ebp - 0x14], 0 ; 0x008880bd: test esi, esi ; 0x008880bf: je 0x8880ec
  - 0x00888092: jne -> 0x0088809b (jcc_true) | ctx: 0x0088808b: cmp dword ptr [0xf8f378], 0 ; 0x00888092: jne 0x88809b
  - 0x00888092: jne -> 0x00888094 (jcc_false) | ctx: 0x0088808b: cmp dword ptr [0xf8f378], 0 ; 0x00888092: jne 0x88809b
  - 0x00888070: jb -> 0x00888080 (jcc_true) | ctx: 0x00888067: mov ecx, esi ; 0x00888069: call dword ptr [eax + 4] ; 0x0088806c: cmp dword ptr [eax + 8], 3 ; 0x00888070: jb 0x888080
  - 0x00888070: jb -> 0x00888072 (jcc_false) | ctx: 0x00888067: mov ecx, esi ; 0x00888069: call dword ptr [eax + 4] ; 0x0088806c: cmp dword ptr [eax + 8], 3 ; 0x00888070: jb 0x888080
  - 0x00888070: jb -> 0x00888080 (jcc_true) | ctx: 0x00888067: mov ecx, esi ; 0x00888069: call dword ptr [eax + 4] ; 0x0088806c: cmp dword ptr [eax + 8], 3 ; 0x00888070: jb 0x888080
  - 0x00888070: jb -> 0x00888072 (jcc_false) | ctx: 0x00888067: mov ecx, esi ; 0x00888069: call dword ptr [eax + 4] ; 0x0088806c: cmp dword ptr [eax + 8], 3 ; 0x00888070: jb 0x888080
  - 0x00888048: je -> 0x00888051 (jcc_true) | ctx: 0x0088803c: mov eax, dword ptr [eax + 0x14] ; 0x0088803f: mov dword ptr [ebp + 0xc], esi ; 0x00888042: cmp eax, dword ptr [0xf8f4f4] ; 0x00888048: je 0x888051
  - 0x00888048: je -> 0x0088804a (jcc_false) | ctx: 0x0088803c: mov eax, dword ptr [eax + 0x14] ; 0x0088803f: mov dword ptr [ebp + 0xc], esi ; 0x00888042: cmp eax, dword ptr [0xf8f4f4] ; 0x00888048: je 0x888051
  - 0x008880f5: je -> 0x00888122 (jcc_true) | ctx: 0x008880ec: mov dword ptr [ebp - 0x1c], 0 ; 0x008880f3: test esi, esi ; 0x008880f5: je 0x888122
  - 0x008880f5: je -> 0x008880f7 (jcc_false) | ctx: 0x008880ec: mov dword ptr [ebp - 0x1c], 0 ; 0x008880f3: test esi, esi ; 0x008880f5: je 0x888122
  - 0x008880c8: jne -> 0x008880d1 (jcc_true) | ctx: 0x008880c1: cmp dword ptr [0xf8f39c], 0 ; 0x008880c8: jne 0x8880d1
  - 0x008880c8: jne -> 0x008880ca (jcc_false) | ctx: 0x008880c1: cmp dword ptr [0xf8f39c], 0 ; 0x008880c8: jne 0x8880d1
  - 0x008880a6: jb -> 0x008880b6 (jcc_true) | ctx: 0x0088809d: mov ecx, esi ; 0x0088809f: call dword ptr [eax + 4] ; 0x008880a2: cmp dword ptr [eax + 8], 3 ; 0x008880a6: jb 0x8880b6
  - 0x008880a6: jb -> 0x008880a8 (jcc_false) | ctx: 0x0088809d: mov ecx, esi ; 0x0088809f: call dword ptr [eax + 4] ; 0x008880a2: cmp dword ptr [eax + 8], 3 ; 0x008880a6: jb 0x8880b6
  - 0x008880a6: jb -> 0x008880b6 (jcc_true) | ctx: 0x0088809d: mov ecx, esi ; 0x0088809f: call dword ptr [eax + 4] ; 0x008880a2: cmp dword ptr [eax + 8], 3 ; 0x008880a6: jb 0x8880b6
  - 0x008880a6: jb -> 0x008880a8 (jcc_false) | ctx: 0x0088809d: mov ecx, esi ; 0x0088809f: call dword ptr [eax + 4] ; 0x008880a2: cmp dword ptr [eax + 8], 3 ; 0x008880a6: jb 0x8880b6
  - 0x0088807e: je -> 0x00888087 (jcc_true) | ctx: 0x00888072: mov eax, dword ptr [eax + 0x14] ; 0x00888075: mov dword ptr [ebp - 0x10], esi ; 0x00888078: cmp eax, dword ptr [0xf8f53c] ; 0x0088807e: je 0x888087
  - 0x0088807e: je -> 0x00888080 (jcc_false) | ctx: 0x00888072: mov eax, dword ptr [eax + 0x14] ; 0x00888075: mov dword ptr [ebp - 0x10], esi ; 0x00888078: cmp eax, dword ptr [0xf8f53c] ; 0x0088807e: je 0x888087
  - 0x00888053: je -> 0x00888080 (jcc_true) | ctx: 0x00888051: test esi, esi ; 0x00888053: je 0x888080
  - 0x00888053: je -> 0x00888055 (jcc_false) | ctx: 0x00888051: test esi, esi ; 0x00888053: je 0x888080
  - 0x0088812b: je -> 0x00888155 (jcc_true) | ctx: 0x00888122: mov dword ptr [ebp - 0x24], 0 ; 0x00888129: test esi, esi ; 0x0088812b: je 0x888155
  - 0x0088812b: je -> 0x0088812d (jcc_false) | ctx: 0x00888122: mov dword ptr [ebp - 0x24], 0 ; 0x00888129: test esi, esi ; 0x0088812b: je 0x888155
  - 0x008880fe: jne -> 0x00888107 (jcc_true) | ctx: 0x008880f7: cmp dword ptr [0xf8f3c0], 0 ; 0x008880fe: jne 0x888107
  - 0x008880fe: jne -> 0x00888100 (jcc_false) | ctx: 0x008880f7: cmp dword ptr [0xf8f3c0], 0 ; 0x008880fe: jne 0x888107
  - 0x008880dc: jb -> 0x008880ec (jcc_true) | ctx: 0x008880d3: mov ecx, esi ; 0x008880d5: call dword ptr [eax + 4] ; 0x008880d8: cmp dword ptr [eax + 8], 3 ; 0x008880dc: jb 0x8880ec
  - 0x008880dc: jb -> 0x008880de (jcc_false) | ctx: 0x008880d3: mov ecx, esi ; 0x008880d5: call dword ptr [eax + 4] ; 0x008880d8: cmp dword ptr [eax + 8], 3 ; 0x008880dc: jb 0x8880ec
  - 0x008880dc: jb -> 0x008880ec (jcc_true) | ctx: 0x008880d3: mov ecx, esi ; 0x008880d5: call dword ptr [eax + 4] ; 0x008880d8: cmp dword ptr [eax + 8], 3 ; 0x008880dc: jb 0x8880ec
  - 0x008880dc: jb -> 0x008880de (jcc_false) | ctx: 0x008880d3: mov ecx, esi ; 0x008880d5: call dword ptr [eax + 4] ; 0x008880d8: cmp dword ptr [eax + 8], 3 ; 0x008880dc: jb 0x8880ec
  - 0x008880b4: je -> 0x008880bd (jcc_true) | ctx: 0x008880a8: mov eax, dword ptr [eax + 0x14] ; 0x008880ab: mov dword ptr [ebp - 0x14], esi ; 0x008880ae: cmp eax, dword ptr [0xf8f38c] ; 0x008880b4: je 0x8880bd
  - 0x008880b4: je -> 0x008880b6 (jcc_false) | ctx: 0x008880a8: mov eax, dword ptr [eax + 0x14] ; 0x008880ab: mov dword ptr [ebp - 0x14], esi ; 0x008880ae: cmp eax, dword ptr [0xf8f38c] ; 0x008880b4: je 0x8880bd
  - 0x00888089: je -> 0x008880b6 (jcc_true) | ctx: 0x00888087: test esi, esi ; 0x00888089: je 0x8880b6
  - 0x00888089: je -> 0x0088808b (jcc_false) | ctx: 0x00888087: test esi, esi ; 0x00888089: je 0x8880b6
  - 0x0088815c: je -> 0x00888231 (jcc_true) | ctx: 0x00888155: xor esi, esi ; 0x00888157: mov eax, dword ptr [ebp + 0xc] ; 0x0088815a: test eax, eax ; 0x0088815c: je 0x888231
  - 0x0088815c: je -> 0x00888162 (jcc_false) | ctx: 0x00888155: xor esi, esi ; 0x00888157: mov eax, dword ptr [ebp + 0xc] ; 0x0088815a: test eax, eax ; 0x0088815c: je 0x888231
  - 0x00888134: jne -> 0x0088813d (jcc_true) | ctx: 0x0088812d: cmp dword ptr [0xf8f3e4], 0 ; 0x00888134: jne 0x88813d
  - 0x00888134: jne -> 0x00888136 (jcc_false) | ctx: 0x0088812d: cmp dword ptr [0xf8f3e4], 0 ; 0x00888134: jne 0x88813d
  - 0x00888112: jb -> 0x00888122 (jcc_true) | ctx: 0x00888109: mov ecx, esi ; 0x0088810b: call dword ptr [eax + 4] ; 0x0088810e: cmp dword ptr [eax + 8], 3 ; 0x00888112: jb 0x888122
  - 0x00888112: jb -> 0x00888114 (jcc_false) | ctx: 0x00888109: mov ecx, esi ; 0x0088810b: call dword ptr [eax + 4] ; 0x0088810e: cmp dword ptr [eax + 8], 3 ; 0x00888112: jb 0x888122
  - 0x00888112: jb -> 0x00888122 (jcc_true) | ctx: 0x00888109: mov ecx, esi ; 0x0088810b: call dword ptr [eax + 4] ; 0x0088810e: cmp dword ptr [eax + 8], 3 ; 0x00888112: jb 0x888122
  - 0x00888112: jb -> 0x00888114 (jcc_false) | ctx: 0x00888109: mov ecx, esi ; 0x0088810b: call dword ptr [eax + 4] ; 0x0088810e: cmp dword ptr [eax + 8], 3 ; 0x00888112: jb 0x888122
  - 0x008880ea: je -> 0x008880f3 (jcc_true) | ctx: 0x008880de: mov eax, dword ptr [eax + 0x14] ; 0x008880e1: mov dword ptr [ebp - 0x1c], esi ; 0x008880e4: cmp eax, dword ptr [0xf8f3b0] ; 0x008880ea: je 0x8880f3
  - 0x008880ea: je -> 0x008880ec (jcc_false) | ctx: 0x008880de: mov eax, dword ptr [eax + 0x14] ; 0x008880e1: mov dword ptr [ebp - 0x1c], esi ; 0x008880e4: cmp eax, dword ptr [0xf8f3b0] ; 0x008880ea: je 0x8880f3
  - 0x008880bf: je -> 0x008880ec (jcc_true) | ctx: 0x008880bd: test esi, esi ; 0x008880bf: je 0x8880ec
  - 0x008880bf: je -> 0x008880c1 (jcc_false) | ctx: 0x008880bd: test esi, esi ; 0x008880bf: je 0x8880ec
  - 0x00888236: je -> 0x0088826b (jcc_true) | ctx: 0x00888231: mov eax, dword ptr [ebp - 0x10] ; 0x00888234: test eax, eax ; 0x00888236: je 0x88826b
  - 0x00888236: je -> 0x00888238 (jcc_false) | ctx: 0x00888231: mov eax, dword ptr [ebp - 0x10] ; 0x00888234: test eax, eax ; 0x00888236: je 0x88826b
  - 0x0088816d: je -> 0x0088817c (jcc_true) | ctx: 0x00888162: lea edx, [eax + 0x28] ; 0x00888165: lea ecx, [ebx + 0x80] ; 0x0088816b: cmp ecx, edx ; 0x0088816d: je 0x88817c
  - 0x0088816d: je -> 0x0088816f (jcc_false) | ctx: 0x00888162: lea edx, [eax + 0x28] ; 0x00888165: lea ecx, [ebx + 0x80] ; 0x0088816b: cmp ecx, edx ; 0x0088816d: je 0x88817c
  - 0x00888148: jb -> 0x00888155 (jcc_true) | ctx: 0x0088813f: mov ecx, esi ; 0x00888141: call dword ptr [eax + 4] ; 0x00888144: cmp dword ptr [eax + 8], 3 ; 0x00888148: jb 0x888155
  - 0x00888148: jb -> 0x0088814a (jcc_false) | ctx: 0x0088813f: mov ecx, esi ; 0x00888141: call dword ptr [eax + 4] ; 0x00888144: cmp dword ptr [eax + 8], 3 ; 0x00888148: jb 0x888155
  - 0x00888148: jb -> 0x00888155 (jcc_true) | ctx: 0x0088813f: mov ecx, esi ; 0x00888141: call dword ptr [eax + 4] ; 0x00888144: cmp dword ptr [eax + 8], 3 ; 0x00888148: jb 0x888155
  - 0x00888148: jb -> 0x0088814a (jcc_false) | ctx: 0x0088813f: mov ecx, esi ; 0x00888141: call dword ptr [eax + 4] ; 0x00888144: cmp dword ptr [eax + 8], 3 ; 0x00888148: jb 0x888155
  - 0x00888120: je -> 0x00888129 (jcc_true) | ctx: 0x00888114: mov eax, dword ptr [eax + 0x14] ; 0x00888117: mov dword ptr [ebp - 0x24], esi ; 0x0088811a: cmp eax, dword ptr [0xf8f3d4] ; 0x00888120: je 0x888129
  - 0x00888120: je -> 0x00888122 (jcc_false) | ctx: 0x00888114: mov eax, dword ptr [eax + 0x14] ; 0x00888117: mov dword ptr [ebp - 0x24], esi ; 0x0088811a: cmp eax, dword ptr [0xf8f3d4] ; 0x00888120: je 0x888129
  - 0x008880f5: je -> 0x00888122 (jcc_true) | ctx: 0x008880f3: test esi, esi ; 0x008880f5: je 0x888122
  - 0x008880f5: je -> 0x008880f7 (jcc_false) | ctx: 0x008880f3: test esi, esi ; 0x008880f5: je 0x888122
  - 0x00888270: je -> 0x0088829f (jcc_true) | ctx: 0x0088826b: mov eax, dword ptr [ebp - 0x14] ; 0x0088826e: test eax, eax ; 0x00888270: je 0x88829f
  - 0x00888270: je -> 0x00888272 (jcc_false) | ctx: 0x0088826b: mov eax, dword ptr [ebp - 0x14] ; 0x0088826e: test eax, eax ; 0x00888270: je 0x88829f
  - 0x00888249: je -> 0x00888258 (jcc_true) | ctx: 0x0088823e: lea edx, [eax + 0x28] ; 0x00888241: lea ecx, [ebx + 0x80] ; 0x00888247: cmp ecx, edx ; 0x00888249: je 0x888258
  - 0x00888249: je -> 0x0088824b (jcc_false) | ctx: 0x0088823e: lea edx, [eax + 0x28] ; 0x00888241: lea ecx, [ebx + 0x80] ; 0x00888247: cmp ecx, edx ; 0x00888249: je 0x888258
  - 0x008881a5: je -> 0x0088831e (jcc_true) | ctx: 0x0088819e: mov dword ptr [ebp - 0x24], eax ; 0x008881a1: mov esi, dword ptr [edi] ; 0x008881a3: cmp esi, edi ; 0x008881a5: je 0x88831e
  - 0x008881a5: je -> 0x008881ab (jcc_false) | ctx: 0x0088819e: mov dword ptr [ebp - 0x24], eax ; 0x008881a1: mov esi, dword ptr [edi] ; 0x008881a3: cmp esi, edi ; 0x008881a5: je 0x88831e
  - 0x008881a5: je -> 0x0088831e (jcc_true) | ctx: 0x0088819e: mov dword ptr [ebp - 0x24], eax ; 0x008881a1: mov esi, dword ptr [edi] ; 0x008881a3: cmp esi, edi ; 0x008881a5: je 0x88831e
  - 0x008881a5: je -> 0x008881ab (jcc_false) | ctx: 0x0088819e: mov dword ptr [ebp - 0x24], eax ; 0x008881a1: mov esi, dword ptr [edi] ; 0x008881a3: cmp esi, edi ; 0x008881a5: je 0x88831e
  - ... 94 more

### 0x00888610
- blocks=83, insns=384, edges=177, jcc=69, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x008887e6)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088880c)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00888837)
- branch points:
  - 0x00888635: je -> 0x00888662 (jcc_true) | ctx: 0x0088862d: push edi ; 0x0088862e: mov edi, 0xfff0be1c ; 0x00888633: test esi, esi ; 0x00888635: je 0x888662
  - 0x00888635: je -> 0x00888637 (jcc_false) | ctx: 0x0088862d: push edi ; 0x0088862e: mov edi, 0xfff0be1c ; 0x00888633: test esi, esi ; 0x00888635: je 0x888662
  - 0x0088866b: je -> 0x00888698 (jcc_true) | ctx: 0x00888662: mov dword ptr [ebp - 0xc], 0 ; 0x00888669: test esi, esi ; 0x0088866b: je 0x888698
  - 0x0088866b: je -> 0x0088866d (jcc_false) | ctx: 0x00888662: mov dword ptr [ebp - 0xc], 0 ; 0x00888669: test esi, esi ; 0x0088866b: je 0x888698
  - 0x0088863e: jne -> 0x00888647 (jcc_true) | ctx: 0x00888637: cmp dword ptr [0xf8f2e8], 0 ; 0x0088863e: jne 0x888647
  - 0x0088863e: jne -> 0x00888640 (jcc_false) | ctx: 0x00888637: cmp dword ptr [0xf8f2e8], 0 ; 0x0088863e: jne 0x888647
  - 0x008886a1: je -> 0x008886ce (jcc_true) | ctx: 0x00888698: mov dword ptr [ebp - 0x10], 0 ; 0x0088869f: test esi, esi ; 0x008886a1: je 0x8886ce
  - 0x008886a1: je -> 0x008886a3 (jcc_false) | ctx: 0x00888698: mov dword ptr [ebp - 0x10], 0 ; 0x0088869f: test esi, esi ; 0x008886a1: je 0x8886ce
  - 0x00888674: jne -> 0x0088867d (jcc_true) | ctx: 0x0088866d: cmp dword ptr [0xf8f3e4], 0 ; 0x00888674: jne 0x88867d
  - 0x00888674: jne -> 0x00888676 (jcc_false) | ctx: 0x0088866d: cmp dword ptr [0xf8f3e4], 0 ; 0x00888674: jne 0x88867d
  - 0x00888652: jb -> 0x00888662 (jcc_true) | ctx: 0x00888649: mov ecx, esi ; 0x0088864b: call dword ptr [eax + 4] ; 0x0088864e: cmp dword ptr [eax + 8], 3 ; 0x00888652: jb 0x888662
  - 0x00888652: jb -> 0x00888654 (jcc_false) | ctx: 0x00888649: mov ecx, esi ; 0x0088864b: call dword ptr [eax + 4] ; 0x0088864e: cmp dword ptr [eax + 8], 3 ; 0x00888652: jb 0x888662
  - 0x00888652: jb -> 0x00888662 (jcc_true) | ctx: 0x00888649: mov ecx, esi ; 0x0088864b: call dword ptr [eax + 4] ; 0x0088864e: cmp dword ptr [eax + 8], 3 ; 0x00888652: jb 0x888662
  - 0x00888652: jb -> 0x00888654 (jcc_false) | ctx: 0x00888649: mov ecx, esi ; 0x0088864b: call dword ptr [eax + 4] ; 0x0088864e: cmp dword ptr [eax + 8], 3 ; 0x00888652: jb 0x888662
  - 0x008886d7: je -> 0x00888704 (jcc_true) | ctx: 0x008886ce: mov dword ptr [ebp - 4], 0 ; 0x008886d5: test esi, esi ; 0x008886d7: je 0x888704
  - 0x008886d7: je -> 0x008886d9 (jcc_false) | ctx: 0x008886ce: mov dword ptr [ebp - 4], 0 ; 0x008886d5: test esi, esi ; 0x008886d7: je 0x888704
  - 0x008886aa: jne -> 0x008886b3 (jcc_true) | ctx: 0x008886a3: cmp dword ptr [0xf8f4e0], 0 ; 0x008886aa: jne 0x8886b3
  - 0x008886aa: jne -> 0x008886ac (jcc_false) | ctx: 0x008886a3: cmp dword ptr [0xf8f4e0], 0 ; 0x008886aa: jne 0x8886b3
  - 0x00888688: jb -> 0x00888698 (jcc_true) | ctx: 0x0088867f: mov ecx, esi ; 0x00888681: call dword ptr [eax + 4] ; 0x00888684: cmp dword ptr [eax + 8], 3 ; 0x00888688: jb 0x888698
  - 0x00888688: jb -> 0x0088868a (jcc_false) | ctx: 0x0088867f: mov ecx, esi ; 0x00888681: call dword ptr [eax + 4] ; 0x00888684: cmp dword ptr [eax + 8], 3 ; 0x00888688: jb 0x888698
  - 0x00888688: jb -> 0x00888698 (jcc_true) | ctx: 0x0088867f: mov ecx, esi ; 0x00888681: call dword ptr [eax + 4] ; 0x00888684: cmp dword ptr [eax + 8], 3 ; 0x00888688: jb 0x888698
  - 0x00888688: jb -> 0x0088868a (jcc_false) | ctx: 0x0088867f: mov ecx, esi ; 0x00888681: call dword ptr [eax + 4] ; 0x00888684: cmp dword ptr [eax + 8], 3 ; 0x00888688: jb 0x888698
  - 0x00888660: je -> 0x00888669 (jcc_true) | ctx: 0x00888654: mov eax, dword ptr [eax + 0x14] ; 0x00888657: mov dword ptr [ebp - 0xc], esi ; 0x0088865a: cmp eax, dword ptr [0xf8f2fc] ; 0x00888660: je 0x888669
  - 0x00888660: je -> 0x00888662 (jcc_false) | ctx: 0x00888654: mov eax, dword ptr [eax + 0x14] ; 0x00888657: mov dword ptr [ebp - 0xc], esi ; 0x0088865a: cmp eax, dword ptr [0xf8f2fc] ; 0x00888660: je 0x888669
  - 0x0088870d: je -> 0x0088873a (jcc_true) | ctx: 0x00888704: mov dword ptr [ebp + 0xc], 0 ; 0x0088870b: test esi, esi ; 0x0088870d: je 0x88873a
  - 0x0088870d: je -> 0x0088870f (jcc_false) | ctx: 0x00888704: mov dword ptr [ebp + 0xc], 0 ; 0x0088870b: test esi, esi ; 0x0088870d: je 0x88873a
  - 0x008886e0: jne -> 0x008886e9 (jcc_true) | ctx: 0x008886d9: cmp dword ptr [0xf8f528], 0 ; 0x008886e0: jne 0x8886e9
  - 0x008886e0: jne -> 0x008886e2 (jcc_false) | ctx: 0x008886d9: cmp dword ptr [0xf8f528], 0 ; 0x008886e0: jne 0x8886e9
  - 0x008886be: jb -> 0x008886ce (jcc_true) | ctx: 0x008886b5: mov ecx, esi ; 0x008886b7: call dword ptr [eax + 4] ; 0x008886ba: cmp dword ptr [eax + 8], 3 ; 0x008886be: jb 0x8886ce
  - 0x008886be: jb -> 0x008886c0 (jcc_false) | ctx: 0x008886b5: mov ecx, esi ; 0x008886b7: call dword ptr [eax + 4] ; 0x008886ba: cmp dword ptr [eax + 8], 3 ; 0x008886be: jb 0x8886ce
  - 0x008886be: jb -> 0x008886ce (jcc_true) | ctx: 0x008886b5: mov ecx, esi ; 0x008886b7: call dword ptr [eax + 4] ; 0x008886ba: cmp dword ptr [eax + 8], 3 ; 0x008886be: jb 0x8886ce
  - 0x008886be: jb -> 0x008886c0 (jcc_false) | ctx: 0x008886b5: mov ecx, esi ; 0x008886b7: call dword ptr [eax + 4] ; 0x008886ba: cmp dword ptr [eax + 8], 3 ; 0x008886be: jb 0x8886ce
  - 0x00888696: je -> 0x0088869f (jcc_true) | ctx: 0x0088868a: mov eax, dword ptr [eax + 0x14] ; 0x0088868d: mov dword ptr [ebp - 0x10], esi ; 0x00888690: cmp eax, dword ptr [0xf8f3f8] ; 0x00888696: je 0x88869f
  - 0x00888696: je -> 0x00888698 (jcc_false) | ctx: 0x0088868a: mov eax, dword ptr [eax + 0x14] ; 0x0088868d: mov dword ptr [ebp - 0x10], esi ; 0x00888690: cmp eax, dword ptr [0xf8f3f8] ; 0x00888696: je 0x88869f
  - 0x0088866b: je -> 0x00888698 (jcc_true) | ctx: 0x00888669: test esi, esi ; 0x0088866b: je 0x888698
  - 0x0088866b: je -> 0x0088866d (jcc_false) | ctx: 0x00888669: test esi, esi ; 0x0088866b: je 0x888698
  - 0x00888743: je -> 0x00888770 (jcc_true) | ctx: 0x0088873a: mov dword ptr [ebp - 8], 0 ; 0x00888741: test esi, esi ; 0x00888743: je 0x888770
  - 0x00888743: je -> 0x00888745 (jcc_false) | ctx: 0x0088873a: mov dword ptr [ebp - 8], 0 ; 0x00888741: test esi, esi ; 0x00888743: je 0x888770
  - 0x00888716: jne -> 0x0088871f (jcc_true) | ctx: 0x0088870f: cmp dword ptr [0xf8f378], 0 ; 0x00888716: jne 0x88871f
  - 0x00888716: jne -> 0x00888718 (jcc_false) | ctx: 0x0088870f: cmp dword ptr [0xf8f378], 0 ; 0x00888716: jne 0x88871f
  - 0x008886f4: jb -> 0x00888704 (jcc_true) | ctx: 0x008886eb: mov ecx, esi ; 0x008886ed: call dword ptr [eax + 4] ; 0x008886f0: cmp dword ptr [eax + 8], 3 ; 0x008886f4: jb 0x888704
  - 0x008886f4: jb -> 0x008886f6 (jcc_false) | ctx: 0x008886eb: mov ecx, esi ; 0x008886ed: call dword ptr [eax + 4] ; 0x008886f0: cmp dword ptr [eax + 8], 3 ; 0x008886f4: jb 0x888704
  - 0x008886f4: jb -> 0x00888704 (jcc_true) | ctx: 0x008886eb: mov ecx, esi ; 0x008886ed: call dword ptr [eax + 4] ; 0x008886f0: cmp dword ptr [eax + 8], 3 ; 0x008886f4: jb 0x888704
  - 0x008886f4: jb -> 0x008886f6 (jcc_false) | ctx: 0x008886eb: mov ecx, esi ; 0x008886ed: call dword ptr [eax + 4] ; 0x008886f0: cmp dword ptr [eax + 8], 3 ; 0x008886f4: jb 0x888704
  - 0x008886cc: je -> 0x008886d5 (jcc_true) | ctx: 0x008886c0: mov eax, dword ptr [eax + 0x14] ; 0x008886c3: mov dword ptr [ebp - 4], esi ; 0x008886c6: cmp eax, dword ptr [0xf8f4f4] ; 0x008886cc: je 0x8886d5
  - 0x008886cc: je -> 0x008886ce (jcc_false) | ctx: 0x008886c0: mov eax, dword ptr [eax + 0x14] ; 0x008886c3: mov dword ptr [ebp - 4], esi ; 0x008886c6: cmp eax, dword ptr [0xf8f4f4] ; 0x008886cc: je 0x8886d5
  - 0x008886a1: je -> 0x008886ce (jcc_true) | ctx: 0x0088869f: test esi, esi ; 0x008886a1: je 0x8886ce
  - 0x008886a1: je -> 0x008886a3 (jcc_false) | ctx: 0x0088869f: test esi, esi ; 0x008886a1: je 0x8886ce
  - 0x00888779: je -> 0x008887a3 (jcc_true) | ctx: 0x00888770: mov dword ptr [ebp - 0x14], 0 ; 0x00888777: test esi, esi ; 0x00888779: je 0x8887a3
  - 0x00888779: je -> 0x0088877b (jcc_false) | ctx: 0x00888770: mov dword ptr [ebp - 0x14], 0 ; 0x00888777: test esi, esi ; 0x00888779: je 0x8887a3
  - 0x0088874c: jne -> 0x00888755 (jcc_true) | ctx: 0x00888745: cmp dword ptr [0xf8f39c], 0 ; 0x0088874c: jne 0x888755
  - 0x0088874c: jne -> 0x0088874e (jcc_false) | ctx: 0x00888745: cmp dword ptr [0xf8f39c], 0 ; 0x0088874c: jne 0x888755
  - 0x0088872a: jb -> 0x0088873a (jcc_true) | ctx: 0x00888721: mov ecx, esi ; 0x00888723: call dword ptr [eax + 4] ; 0x00888726: cmp dword ptr [eax + 8], 3 ; 0x0088872a: jb 0x88873a
  - 0x0088872a: jb -> 0x0088872c (jcc_false) | ctx: 0x00888721: mov ecx, esi ; 0x00888723: call dword ptr [eax + 4] ; 0x00888726: cmp dword ptr [eax + 8], 3 ; 0x0088872a: jb 0x88873a
  - 0x0088872a: jb -> 0x0088873a (jcc_true) | ctx: 0x00888721: mov ecx, esi ; 0x00888723: call dword ptr [eax + 4] ; 0x00888726: cmp dword ptr [eax + 8], 3 ; 0x0088872a: jb 0x88873a
  - 0x0088872a: jb -> 0x0088872c (jcc_false) | ctx: 0x00888721: mov ecx, esi ; 0x00888723: call dword ptr [eax + 4] ; 0x00888726: cmp dword ptr [eax + 8], 3 ; 0x0088872a: jb 0x88873a
  - 0x00888702: je -> 0x0088870b (jcc_true) | ctx: 0x008886f6: mov eax, dword ptr [eax + 0x14] ; 0x008886f9: mov dword ptr [ebp + 0xc], esi ; 0x008886fc: cmp eax, dword ptr [0xf8f53c] ; 0x00888702: je 0x88870b
  - 0x00888702: je -> 0x00888704 (jcc_false) | ctx: 0x008886f6: mov eax, dword ptr [eax + 0x14] ; 0x008886f9: mov dword ptr [ebp + 0xc], esi ; 0x008886fc: cmp eax, dword ptr [0xf8f53c] ; 0x00888702: je 0x88870b
  - 0x008886d7: je -> 0x00888704 (jcc_true) | ctx: 0x008886d5: test esi, esi ; 0x008886d7: je 0x888704
  - 0x008886d7: je -> 0x008886d9 (jcc_false) | ctx: 0x008886d5: test esi, esi ; 0x008886d7: je 0x888704
  - 0x008887a9: je -> 0x008887b5 (jcc_true) | ctx: 0x008887a3: xor esi, esi ; 0x008887a5: cmp dword ptr [ebp - 0xc], 0 ; 0x008887a9: je 0x8887b5
  - 0x008887a9: je -> 0x008887ab (jcc_false) | ctx: 0x008887a3: xor esi, esi ; 0x008887a5: cmp dword ptr [ebp - 0xc], 0 ; 0x008887a9: je 0x8887b5
  - 0x00888782: jne -> 0x0088878b (jcc_true) | ctx: 0x0088877b: cmp dword ptr [0xf8f3c0], 0 ; 0x00888782: jne 0x88878b
  - 0x00888782: jne -> 0x00888784 (jcc_false) | ctx: 0x0088877b: cmp dword ptr [0xf8f3c0], 0 ; 0x00888782: jne 0x88878b
  - 0x00888760: jb -> 0x00888770 (jcc_true) | ctx: 0x00888757: mov ecx, esi ; 0x00888759: call dword ptr [eax + 4] ; 0x0088875c: cmp dword ptr [eax + 8], 3 ; 0x00888760: jb 0x888770
  - 0x00888760: jb -> 0x00888762 (jcc_false) | ctx: 0x00888757: mov ecx, esi ; 0x00888759: call dword ptr [eax + 4] ; 0x0088875c: cmp dword ptr [eax + 8], 3 ; 0x00888760: jb 0x888770
  - 0x00888760: jb -> 0x00888770 (jcc_true) | ctx: 0x00888757: mov ecx, esi ; 0x00888759: call dword ptr [eax + 4] ; 0x0088875c: cmp dword ptr [eax + 8], 3 ; 0x00888760: jb 0x888770
  - 0x00888760: jb -> 0x00888762 (jcc_false) | ctx: 0x00888757: mov ecx, esi ; 0x00888759: call dword ptr [eax + 4] ; 0x0088875c: cmp dword ptr [eax + 8], 3 ; 0x00888760: jb 0x888770
  - 0x00888738: je -> 0x00888741 (jcc_true) | ctx: 0x0088872c: mov eax, dword ptr [eax + 0x14] ; 0x0088872f: mov dword ptr [ebp - 8], esi ; 0x00888732: cmp eax, dword ptr [0xf8f38c] ; 0x00888738: je 0x888741
  - 0x00888738: je -> 0x0088873a (jcc_false) | ctx: 0x0088872c: mov eax, dword ptr [eax + 0x14] ; 0x0088872f: mov dword ptr [ebp - 8], esi ; 0x00888732: cmp eax, dword ptr [0xf8f38c] ; 0x00888738: je 0x888741
  - 0x0088870d: je -> 0x0088873a (jcc_true) | ctx: 0x0088870b: test esi, esi ; 0x0088870d: je 0x88873a
  - 0x0088870d: je -> 0x0088870f (jcc_false) | ctx: 0x0088870b: test esi, esi ; 0x0088870d: je 0x88873a
  - 0x008887ba: je -> 0x008887cd (jcc_true) | ctx: 0x008887b5: mov ecx, dword ptr [ebp - 0x10] ; 0x008887b8: test ecx, ecx ; 0x008887ba: je 0x8887cd
  - 0x008887ba: je -> 0x008887bc (jcc_false) | ctx: 0x008887b5: mov ecx, dword ptr [ebp - 0x10] ; 0x008887b8: test ecx, ecx ; 0x008887ba: je 0x8887cd
  - 0x008887b0: jmp -> 0x00888867 (jmp) | ctx: 0x008887ab: mov eax, dword ptr [0xc18520] ; 0x008887b0: jmp 0x888867
  - 0x00888796: jb -> 0x008887a3 (jcc_true) | ctx: 0x0088878d: mov ecx, esi ; 0x0088878f: call dword ptr [eax + 4] ; 0x00888792: cmp dword ptr [eax + 8], 3 ; 0x00888796: jb 0x8887a3
  - 0x00888796: jb -> 0x00888798 (jcc_false) | ctx: 0x0088878d: mov ecx, esi ; 0x0088878f: call dword ptr [eax + 4] ; 0x00888792: cmp dword ptr [eax + 8], 3 ; 0x00888796: jb 0x8887a3
  - 0x00888796: jb -> 0x008887a3 (jcc_true) | ctx: 0x0088878d: mov ecx, esi ; 0x0088878f: call dword ptr [eax + 4] ; 0x00888792: cmp dword ptr [eax + 8], 3 ; 0x00888796: jb 0x8887a3
  - 0x00888796: jb -> 0x00888798 (jcc_false) | ctx: 0x0088878d: mov ecx, esi ; 0x0088878f: call dword ptr [eax + 4] ; 0x00888792: cmp dword ptr [eax + 8], 3 ; 0x00888796: jb 0x8887a3
  - 0x0088876e: je -> 0x00888777 (jcc_true) | ctx: 0x00888762: mov eax, dword ptr [eax + 0x14] ; 0x00888765: mov dword ptr [ebp - 0x14], esi ; 0x00888768: cmp eax, dword ptr [0xf8f3b0] ; 0x0088876e: je 0x888777
  - ... 69 more

### 0x00888ef0
- blocks=13, insns=87, edges=28, jcc=9, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00888f82)
- branch points:
  - 0x00888efe: jne -> 0x00888f07 (jcc_true) | ctx: 0x00888efa: push esi ; 0x00888efb: push edi ; 0x00888efc: mov esi, ecx ; 0x00888efe: jne 0x888f07
  - 0x00888efe: jne -> 0x00888f00 (jcc_false) | ctx: 0x00888efa: push esi ; 0x00888efb: push edi ; 0x00888efc: mov esi, ecx ; 0x00888efe: jne 0x888f07
  - 0x00888f15: jb -> 0x00888f45 (jcc_true) | ctx: 0x00888f0c: mov eax, dword ptr [edi] ; 0x00888f0e: call dword ptr [eax + 4] ; 0x00888f11: cmp dword ptr [eax + 8], 3 ; 0x00888f15: jb 0x888f45
  - 0x00888f15: jb -> 0x00888f17 (jcc_false) | ctx: 0x00888f0c: mov eax, dword ptr [edi] ; 0x00888f0e: call dword ptr [eax + 4] ; 0x00888f11: cmp dword ptr [eax + 8], 3 ; 0x00888f15: jb 0x888f45
  - 0x00888f15: jb -> 0x00888f45 (jcc_true) | ctx: 0x00888f0c: mov eax, dword ptr [edi] ; 0x00888f0e: call dword ptr [eax + 4] ; 0x00888f11: cmp dword ptr [eax + 8], 3 ; 0x00888f15: jb 0x888f45
  - 0x00888f15: jb -> 0x00888f17 (jcc_false) | ctx: 0x00888f0c: mov eax, dword ptr [edi] ; 0x00888f0e: call dword ptr [eax + 4] ; 0x00888f11: cmp dword ptr [eax + 8], 3 ; 0x00888f15: jb 0x888f45
  - 0x00888f4c: jne -> 0x00888f55 (jcc_true) | ctx: 0x00888f45: cmp dword ptr [0xf8fc94], 0 ; 0x00888f4c: jne 0x888f55
  - 0x00888f4c: jne -> 0x00888f4e (jcc_false) | ctx: 0x00888f45: cmp dword ptr [0xf8fc94], 0 ; 0x00888f4c: jne 0x888f55
  - 0x00888f20: jne -> 0x00888f45 (jcc_true) | ctx: 0x00888f17: mov eax, dword ptr [eax + 0x14] ; 0x00888f1a: cmp eax, dword ptr [0xf8fc84] ; 0x00888f20: jne 0x888f45
  - 0x00888f20: jne -> 0x00888f22 (jcc_false) | ctx: 0x00888f17: mov eax, dword ptr [eax + 0x14] ; 0x00888f1a: cmp eax, dword ptr [0xf8fc84] ; 0x00888f20: jne 0x888f45
  - 0x00888f60: jb -> 0x00888fa4 (jcc_true) | ctx: 0x00888f57: mov ecx, edi ; 0x00888f59: call dword ptr [eax + 4] ; 0x00888f5c: cmp dword ptr [eax + 8], 3 ; 0x00888f60: jb 0x888fa4
  - 0x00888f60: jb -> 0x00888f62 (jcc_false) | ctx: 0x00888f57: mov ecx, edi ; 0x00888f59: call dword ptr [eax + 4] ; 0x00888f5c: cmp dword ptr [eax + 8], 3 ; 0x00888f60: jb 0x888fa4
  - 0x00888f60: jb -> 0x00888fa4 (jcc_true) | ctx: 0x00888f57: mov ecx, edi ; 0x00888f59: call dword ptr [eax + 4] ; 0x00888f5c: cmp dword ptr [eax + 8], 3 ; 0x00888f60: jb 0x888fa4
  - 0x00888f60: jb -> 0x00888f62 (jcc_false) | ctx: 0x00888f57: mov ecx, edi ; 0x00888f59: call dword ptr [eax + 4] ; 0x00888f5c: cmp dword ptr [eax + 8], 3 ; 0x00888f60: jb 0x888fa4
  - 0x00888f6b: jne -> 0x00888fa4 (jcc_true) | ctx: 0x00888f62: mov eax, dword ptr [eax + 0x14] ; 0x00888f65: cmp eax, dword ptr [0xf8fca8] ; 0x00888f6b: jne 0x888fa4
  - 0x00888f6b: jne -> 0x00888f6d (jcc_false) | ctx: 0x00888f62: mov eax, dword ptr [eax + 0x14] ; 0x00888f65: cmp eax, dword ptr [0xf8fca8] ; 0x00888f6b: jne 0x888fa4
  - 0x00888f7b: je -> 0x00888f87 (jcc_true) | ctx: 0x00888f73: add edi, 0x28 ; 0x00888f76: mov dword ptr [esi + 0x6c], eax ; 0x00888f79: cmp ecx, edi ; 0x00888f7b: je 0x888f87
  - 0x00888f7b: je -> 0x00888f7d (jcc_false) | ctx: 0x00888f73: add edi, 0x28 ; 0x00888f76: mov dword ptr [esi + 0x6c], eax ; 0x00888f79: cmp ecx, edi ; 0x00888f7b: je 0x888f87

### 0x0088adb0
- blocks=41, insns=350, edges=107, jcc=34, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088af1c)
- branch points:
  - 0x0088ade8: je -> 0x0088aff8 (jcc_true) | ctx: 0x0088add9: mov dword ptr [ebp - 0x14], ebx ; 0x0088addc: mov esi, dword ptr [ebx + 0xa4] ; 0x0088ade2: cmp esi, dword ptr [ebx + 0xa8] ; 0x0088ade8: je 0x88aff8
  - 0x0088ade8: je -> 0x0088adee (jcc_false) | ctx: 0x0088add9: mov dword ptr [ebp - 0x14], ebx ; 0x0088addc: mov esi, dword ptr [ebx + 0xa4] ; 0x0088ade2: cmp esi, dword ptr [ebx + 0xa8] ; 0x0088ade8: je 0x88aff8
  - 0x0088afff: je -> 0x0088b0a9 (jcc_true) | ctx: 0x0088aff8: mov eax, dword ptr [ebx + 0x48] ; 0x0088affb: mov esi, dword ptr [eax] ; 0x0088affd: cmp esi, eax ; 0x0088afff: je 0x88b0a9
  - 0x0088afff: je -> 0x0088b005 (jcc_false) | ctx: 0x0088aff8: mov eax, dword ptr [ebx + 0x48] ; 0x0088affb: mov esi, dword ptr [eax] ; 0x0088affd: cmp esi, eax ; 0x0088afff: je 0x88b0a9
  - 0x0088ae1e: jb -> 0x0088afe3 (jcc_true) | ctx: 0x0088ae15: push eax ; 0x0088ae16: call 0xab6ea0 ; 0x0088ae1b: cmp edx, dword ptr [esi + 0x24] ; 0x0088ae1e: jb 0x88afe3
  - 0x0088ae1e: jb -> 0x0088ae24 (jcc_false) | ctx: 0x0088ae15: push eax ; 0x0088ae16: call 0xab6ea0 ; 0x0088ae1b: cmp edx, dword ptr [esi + 0x24] ; 0x0088ae1e: jb 0x88afe3
  - 0x0088b036: jb -> 0x0088b05a (jcc_true) | ctx: 0x0088b02d: push eax ; 0x0088b02e: call 0xab6ea0 ; 0x0088b033: cmp edx, dword ptr [edi + 4] ; 0x0088b036: jb 0x88b05a
  - 0x0088b036: jb -> 0x0088b038 (jcc_false) | ctx: 0x0088b02d: push eax ; 0x0088b02e: call 0xab6ea0 ; 0x0088b033: cmp edx, dword ptr [edi + 4] ; 0x0088b036: jb 0x88b05a
  - 0x0088aff2: jne -> 0x0088adf0 (jcc_true) | ctx: 0x0088afe3: add esi, 0x40 ; 0x0088afe6: mov ecx, dword ptr [0xbb92fc] ; 0x0088afec: cmp esi, dword ptr [ebx + 0xa8] ; 0x0088aff2: jne 0x88adf0
  - 0x0088aff2: jne -> 0x0088aff8 (jcc_false) | ctx: 0x0088afe3: add esi, 0x40 ; 0x0088afe6: mov ecx, dword ptr [0xbb92fc] ; 0x0088afec: cmp esi, dword ptr [ebx + 0xa8] ; 0x0088aff2: jne 0x88adf0
  - 0x0088ae24: ja -> 0x0088ae2f (jcc_true) | ctx: 0x0088ae24: ja 0x88ae2f
  - 0x0088ae24: ja -> 0x0088ae26 (jcc_false) | ctx: 0x0088ae24: ja 0x88ae2f
  - 0x0088b05e: jne -> 0x0088b09a (jcc_true) | ctx: 0x0088b05a: cmp byte ptr [esi + 0xd], 0 ; 0x0088b05e: jne 0x88b09a
  - 0x0088b05e: jne -> 0x0088b060 (jcc_false) | ctx: 0x0088b05a: cmp byte ptr [esi + 0xd], 0 ; 0x0088b05e: jne 0x88b09a
  - 0x0088b038: ja -> 0x0088b03e (jcc_true) | ctx: 0x0088b038: ja 0x88b03e
  - 0x0088b038: ja -> 0x0088b03a (jcc_false) | ctx: 0x0088b038: ja 0x88b03e
  - 0x0088ae1e: jb -> 0x0088afe3 (jcc_true) | ctx: 0x0088ae15: push eax ; 0x0088ae16: call 0xab6ea0 ; 0x0088ae1b: cmp edx, dword ptr [esi + 0x24] ; 0x0088ae1e: jb 0x88afe3
  - 0x0088ae1e: jb -> 0x0088ae24 (jcc_false) | ctx: 0x0088ae15: push eax ; 0x0088ae16: call 0xab6ea0 ; 0x0088ae1b: cmp edx, dword ptr [esi + 0x24] ; 0x0088ae1e: jb 0x88afe3
  - 0x0088ae34: je -> 0x0088ae79 (jcc_true) | ctx: 0x0088ae2f: mov al, byte ptr [esi + 0x28] ; 0x0088ae32: test al, al ; 0x0088ae34: je 0x88ae79
  - 0x0088ae34: je -> 0x0088ae36 (jcc_false) | ctx: 0x0088ae2f: mov al, byte ptr [esi + 0x28] ; 0x0088ae32: test al, al ; 0x0088ae34: je 0x88ae79
  - 0x0088ae29: jbe -> 0x0088afe3 (jcc_true) | ctx: 0x0088ae26: cmp eax, dword ptr [esi + 0x20] ; 0x0088ae29: jbe 0x88afe3
  - 0x0088ae29: jbe -> 0x0088ae2f (jcc_false) | ctx: 0x0088ae26: cmp eax, dword ptr [esi + 0x20] ; 0x0088ae29: jbe 0x88afe3
  - 0x0088b0a3: jne -> 0x0088b005 (jcc_true) | ctx: 0x0088b09a: mov ecx, dword ptr [0xbb92fc] ; 0x0088b0a0: cmp esi, dword ptr [ebx + 0x48] ; 0x0088b0a3: jne 0x88b005
  - 0x0088b0a3: jne -> 0x0088b0a9 (jcc_false) | ctx: 0x0088b09a: mov ecx, dword ptr [0xbb92fc] ; 0x0088b0a0: cmp esi, dword ptr [ebx + 0x48] ; 0x0088b0a3: jne 0x88b005
  - 0x0088b067: jne -> 0x0088b07f (jcc_true) | ctx: 0x0088b060: mov eax, dword ptr [esi + 8] ; 0x0088b063: cmp byte ptr [eax + 0xd], 0 ; 0x0088b067: jne 0x88b07f
  - 0x0088b067: jne -> 0x0088b069 (jcc_false) | ctx: 0x0088b060: mov eax, dword ptr [esi + 8] ; 0x0088b063: cmp byte ptr [eax + 0xd], 0 ; 0x0088b067: jne 0x88b07f
  - 0x0088b058: jmp -> 0x0088b09a (jmp) | ctx: 0x0088b04e: lea ecx, [ebx + 0x48] ; 0x0088b051: call 0x8af310 ; 0x0088b056: mov esi, dword ptr [eax] ; 0x0088b058: jmp 0x88b09a
  - 0x0088b03c: jbe -> 0x0088b05a (jcc_true) | ctx: 0x0088b03a: cmp eax, dword ptr [edi] ; 0x0088b03c: jbe 0x88b05a
  - 0x0088b03c: jbe -> 0x0088b03e (jcc_false) | ctx: 0x0088b03a: cmp eax, dword ptr [edi] ; 0x0088b03c: jbe 0x88b05a
  - 0x0088af42: jb -> 0x0088af4f (jcc_true) | ctx: 0x0088af37: mov dword ptr [ebp - 0x44], eax ; 0x0088af3a: cmp dword ptr [ebp - 0x2c], 0x10 ; 0x0088af3e: mov byte ptr [ebp - 4], 2 ; 0x0088af42: jb 0x88af4f
  - 0x0088af42: jb -> 0x0088af44 (jcc_false) | ctx: 0x0088af37: mov dword ptr [ebp - 0x44], eax ; 0x0088af3a: cmp dword ptr [ebp - 0x2c], 0x10 ; 0x0088af3e: mov byte ptr [ebp - 4], 2 ; 0x0088af42: jb 0x88af4f
  - 0x0088ae45: jne -> 0x0088ae5b (jcc_true) | ctx: 0x0088ae3b: mov edi, dword ptr [esi + 0xc] ; 0x0088ae3e: mov edx, dword ptr [ecx + 4] ; 0x0088ae41: cmp byte ptr [edx + 0xd], 0 ; 0x0088ae45: jne 0x88ae5b
  - 0x0088ae45: jne -> 0x0088ae47 (jcc_false) | ctx: 0x0088ae3b: mov edi, dword ptr [esi + 0xc] ; 0x0088ae3e: mov edx, dword ptr [ecx + 4] ; 0x0088ae41: cmp byte ptr [edx + 0xd], 0 ; 0x0088ae45: jne 0x88ae5b
  - 0x0088b086: jne -> 0x0088b098 (jcc_true) | ctx: 0x0088b07f: mov eax, dword ptr [esi + 4] ; 0x0088b082: cmp byte ptr [eax + 0xd], 0 ; 0x0088b086: jne 0x88b098
  - 0x0088b086: jne -> 0x0088b088 (jcc_false) | ctx: 0x0088b07f: mov eax, dword ptr [esi + 4] ; 0x0088b082: cmp byte ptr [eax + 0xd], 0 ; 0x0088b086: jne 0x88b098
  - 0x0088b071: jne -> 0x0088b09a (jcc_true) | ctx: 0x0088b069: mov esi, eax ; 0x0088b06b: mov eax, dword ptr [esi] ; 0x0088b06d: cmp byte ptr [eax + 0xd], 0 ; 0x0088b071: jne 0x88b09a
  - 0x0088b071: jne -> 0x0088b073 (jcc_false) | ctx: 0x0088b069: mov esi, eax ; 0x0088b06b: mov eax, dword ptr [esi] ; 0x0088b06d: cmp byte ptr [eax + 0xd], 0 ; 0x0088b071: jne 0x88b09a
  - 0x0088afcd: jb -> 0x0088afda (jcc_true) | ctx: 0x0088afc0: call 0x973a50 ; 0x0088afc5: cmp dword ptr [ebp - 0x4c], 0x10 ; 0x0088afc9: mov byte ptr [ebp - 4], 4 ; 0x0088afcd: jb 0x88afda
  - 0x0088afcd: jb -> 0x0088afcf (jcc_false) | ctx: 0x0088afc0: call 0x973a50 ; 0x0088afc5: cmp dword ptr [ebp - 0x4c], 0x10 ; 0x0088afc9: mov byte ptr [ebp - 4], 4 ; 0x0088afcd: jb 0x88afda
  - 0x0088afcd: jb -> 0x0088afda (jcc_true) | ctx: 0x0088afc0: call 0x973a50 ; 0x0088afc5: cmp dword ptr [ebp - 0x4c], 0x10 ; 0x0088afc9: mov byte ptr [ebp - 4], 4 ; 0x0088afcd: jb 0x88afda
  - 0x0088afcd: jb -> 0x0088afcf (jcc_false) | ctx: 0x0088afc0: call 0x973a50 ; 0x0088afc5: cmp dword ptr [ebp - 0x4c], 0x10 ; 0x0088afc9: mov byte ptr [ebp - 4], 4 ; 0x0088afcd: jb 0x88afda
  - 0x0088ae5d: je -> 0x0088ae64 (jcc_true) | ctx: 0x0088ae5b: cmp eax, ecx ; 0x0088ae5d: je 0x88ae64
  - 0x0088ae5d: je -> 0x0088ae5f (jcc_false) | ctx: 0x0088ae5b: cmp eax, ecx ; 0x0088ae5d: je 0x88ae64
  - 0x0088ae4a: jae -> 0x0088ae51 (jcc_true) | ctx: 0x0088ae47: cmp dword ptr [edx + 0x10], edi ; 0x0088ae4a: jae 0x88ae51
  - 0x0088ae4a: jae -> 0x0088ae4c (jcc_false) | ctx: 0x0088ae47: cmp dword ptr [edx + 0x10], edi ; 0x0088ae4a: jae 0x88ae51
  - 0x0088b0a3: jne -> 0x0088b005 (jcc_true) | ctx: 0x0088b098: mov esi, eax ; 0x0088b09a: mov ecx, dword ptr [0xbb92fc] ; 0x0088b0a0: cmp esi, dword ptr [ebx + 0x48] ; 0x0088b0a3: jne 0x88b005
  - 0x0088b0a3: jne -> 0x0088b0a9 (jcc_false) | ctx: 0x0088b098: mov esi, eax ; 0x0088b09a: mov ecx, dword ptr [0xbb92fc] ; 0x0088b0a0: cmp esi, dword ptr [ebx + 0x48] ; 0x0088b0a3: jne 0x88b005
  - 0x0088b08b: jne -> 0x0088b098 (jcc_true) | ctx: 0x0088b088: cmp esi, dword ptr [eax + 8] ; 0x0088b08b: jne 0x88b098
  - 0x0088b08b: jne -> 0x0088b08d (jcc_false) | ctx: 0x0088b088: cmp esi, dword ptr [eax + 8] ; 0x0088b08b: jne 0x88b098
  - 0x0088b07b: je -> 0x0088b073 (jcc_true) | ctx: 0x0088b073: mov esi, eax ; 0x0088b075: mov eax, dword ptr [esi] ; 0x0088b077: cmp byte ptr [eax + 0xd], 0 ; 0x0088b07b: je 0x88b073
  - 0x0088b07b: je -> 0x0088b07d (jcc_false) | ctx: 0x0088b073: mov esi, eax ; 0x0088b075: mov eax, dword ptr [esi] ; 0x0088b077: cmp byte ptr [eax + 0xd], 0 ; 0x0088b07b: je 0x88b073
  - 0x0088afe1: jmp -> 0x0088afe6 (jmp) | ctx: 0x0088afda: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088afe1: jmp 0x88afe6
  - 0x0088afe1: jmp -> 0x0088afe6 (jmp) | ctx: 0x0088afd2: call 0x9afbf0 ; 0x0088afd7: add esp, 4 ; 0x0088afda: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088afe1: jmp 0x88afe6
  - 0x0088ae68: je -> 0x0088ae84 (jcc_true) | ctx: 0x0088ae64: mov eax, ecx ; 0x0088ae66: cmp eax, ecx ; 0x0088ae68: je 0x88ae84
  - 0x0088ae68: je -> 0x0088ae6a (jcc_false) | ctx: 0x0088ae64: mov eax, ecx ; 0x0088ae66: cmp eax, ecx ; 0x0088ae68: je 0x88ae84
  - 0x0088ae62: jae -> 0x0088ae66 (jcc_true) | ctx: 0x0088ae5f: cmp edi, dword ptr [eax + 0x10] ; 0x0088ae62: jae 0x88ae66
  - 0x0088ae62: jae -> 0x0088ae64 (jcc_false) | ctx: 0x0088ae5f: cmp edi, dword ptr [eax + 0x10] ; 0x0088ae62: jae 0x88ae66
  - 0x0088ae59: je -> 0x0088ae47 (jcc_true) | ctx: 0x0088ae51: mov eax, edx ; 0x0088ae53: mov edx, dword ptr [edx] ; 0x0088ae55: cmp byte ptr [edx + 0xd], 0 ; 0x0088ae59: je 0x88ae47
  - 0x0088ae59: je -> 0x0088ae5b (jcc_false) | ctx: 0x0088ae51: mov eax, edx ; 0x0088ae53: mov edx, dword ptr [edx] ; 0x0088ae55: cmp byte ptr [edx + 0xd], 0 ; 0x0088ae59: je 0x88ae47
  - 0x0088ae4f: jmp -> 0x0088ae55 (jmp) | ctx: 0x0088ae4c: mov edx, dword ptr [edx + 8] ; 0x0088ae4f: jmp 0x88ae55
  - 0x0088b096: je -> 0x0088b088 (jcc_true) | ctx: 0x0088b08d: mov esi, eax ; 0x0088b08f: mov eax, dword ptr [eax + 4] ; 0x0088b092: cmp byte ptr [eax + 0xd], 0 ; 0x0088b096: je 0x88b088
  - 0x0088b096: je -> 0x0088b098 (jcc_false) | ctx: 0x0088b08d: mov esi, eax ; 0x0088b08f: mov eax, dword ptr [eax + 4] ; 0x0088b092: cmp byte ptr [eax + 0xd], 0 ; 0x0088b096: je 0x88b088
  - 0x0088b07d: jmp -> 0x0088b09a (jmp) | ctx: 0x0088b07d: jmp 0x88b09a
  - 0x0088aff2: jne -> 0x0088adf0 (jcc_true) | ctx: 0x0088afe6: mov ecx, dword ptr [0xbb92fc] ; 0x0088afec: cmp esi, dword ptr [ebx + 0xa8] ; 0x0088aff2: jne 0x88adf0
  - 0x0088aff2: jne -> 0x0088aff8 (jcc_false) | ctx: 0x0088afe6: mov ecx, dword ptr [0xbb92fc] ; 0x0088afec: cmp esi, dword ptr [ebx + 0xa8] ; 0x0088aff2: jne 0x88adf0
  - 0x0088af42: jb -> 0x0088af4f (jcc_true) | ctx: 0x0088af37: mov dword ptr [ebp - 0x44], eax ; 0x0088af3a: cmp dword ptr [ebp - 0x2c], 0x10 ; 0x0088af3e: mov byte ptr [ebp - 4], 2 ; 0x0088af42: jb 0x88af4f
  - 0x0088af42: jb -> 0x0088af44 (jcc_false) | ctx: 0x0088af37: mov dword ptr [ebp - 0x44], eax ; 0x0088af3a: cmp dword ptr [ebp - 0x2c], 0x10 ; 0x0088af3e: mov byte ptr [ebp - 4], 2 ; 0x0088af42: jb 0x88af4f
  - 0x0088ae6f: je -> 0x0088ae84 (jcc_true) | ctx: 0x0088ae6a: mov ecx, dword ptr [eax + 0x14] ; 0x0088ae6d: test ecx, ecx ; 0x0088ae6f: je 0x88ae84
  - 0x0088ae6f: je -> 0x0088ae71 (jcc_false) | ctx: 0x0088ae6a: mov ecx, dword ptr [eax + 0x14] ; 0x0088ae6d: test ecx, ecx ; 0x0088ae6f: je 0x88ae84
  - 0x0088ae68: je -> 0x0088ae84 (jcc_true) | ctx: 0x0088ae66: cmp eax, ecx ; 0x0088ae68: je 0x88ae84
  - 0x0088ae68: je -> 0x0088ae6a (jcc_false) | ctx: 0x0088ae66: cmp eax, ecx ; 0x0088ae68: je 0x88ae84
  - 0x0088ae59: je -> 0x0088ae47 (jcc_true) | ctx: 0x0088ae55: cmp byte ptr [edx + 0xd], 0 ; 0x0088ae59: je 0x88ae47
  - 0x0088ae59: je -> 0x0088ae5b (jcc_false) | ctx: 0x0088ae55: cmp byte ptr [edx + 0xd], 0 ; 0x0088ae59: je 0x88ae47
  - 0x0088ae77: jmp -> 0x0088ae84 (jmp) | ctx: 0x0088ae71: push esi ; 0x0088ae72: call 0x8a9fb0 ; 0x0088ae77: jmp 0x88ae84

### 0x0088b460
- blocks=11, insns=177, edges=26, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088b583)
- branch points:
  - 0x0088b49f: jne -> 0x0088b514 (jcc_true) | ctx: 0x0088b494: mov dword ptr [ebp - 0x10], 0 ; 0x0088b49b: push eax ; 0x0088b49c: lea ecx, [ecx + 0x40] ; 0x0088b49f: jne 0x88b514
  - 0x0088b49f: jne -> 0x0088b4a1 (jcc_false) | ctx: 0x0088b494: mov dword ptr [ebp - 0x10], 0 ; 0x0088b49b: push eax ; 0x0088b49c: lea ecx, [ecx + 0x40] ; 0x0088b49f: jne 0x88b514
  - 0x0088b52b: je -> 0x0088b534 (jcc_true) | ctx: 0x0088b51f: mov dword ptr [ebp - 0x10], ecx ; 0x0088b522: mov dword ptr [ebp - 4], 1 ; 0x0088b529: test ecx, ecx ; 0x0088b52b: je 0x88b534
  - 0x0088b52b: je -> 0x0088b52d (jcc_false) | ctx: 0x0088b51f: mov dword ptr [ebp - 0x10], ecx ; 0x0088b522: mov dword ptr [ebp - 4], 1 ; 0x0088b529: test ecx, ecx ; 0x0088b52b: je 0x88b534
  - 0x0088b4b8: je -> 0x0088b4c1 (jcc_true) | ctx: 0x0088b4ac: mov dword ptr [ebp - 0x14], ecx ; 0x0088b4af: mov dword ptr [ebp - 4], 0 ; 0x0088b4b6: test ecx, ecx ; 0x0088b4b8: je 0x88b4c1
  - 0x0088b4b8: je -> 0x0088b4ba (jcc_false) | ctx: 0x0088b4ac: mov dword ptr [ebp - 0x14], ecx ; 0x0088b4af: mov dword ptr [ebp - 4], 0 ; 0x0088b4b6: test ecx, ecx ; 0x0088b4b8: je 0x88b4c1
  - 0x0088b57c: je -> 0x0088b588 (jcc_true) | ctx: 0x0088b574: lea ecx, [esi + 0x34] ; 0x0088b577: lea eax, [ebx + 0x34] ; 0x0088b57a: cmp ecx, eax ; 0x0088b57c: je 0x88b588
  - 0x0088b57c: je -> 0x0088b57e (jcc_false) | ctx: 0x0088b574: lea ecx, [esi + 0x34] ; 0x0088b577: lea eax, [ebx + 0x34] ; 0x0088b57a: cmp ecx, eax ; 0x0088b57c: je 0x88b588
  - 0x0088b532: jmp -> 0x0088b536 (jmp) | ctx: 0x0088b52d: call 0x87efa0 ; 0x0088b532: jmp 0x88b536
  - 0x0088b4bf: jmp -> 0x0088b4c3 (jmp) | ctx: 0x0088b4ba: call 0x87efa0 ; 0x0088b4bf: jmp 0x88b4c3
  - 0x0088b57c: je -> 0x0088b588 (jcc_true) | ctx: 0x0088b574: lea ecx, [esi + 0x34] ; 0x0088b577: lea eax, [ebx + 0x34] ; 0x0088b57a: cmp ecx, eax ; 0x0088b57c: je 0x88b588
  - 0x0088b57c: je -> 0x0088b57e (jcc_false) | ctx: 0x0088b574: lea ecx, [esi + 0x34] ; 0x0088b577: lea eax, [ebx + 0x34] ; 0x0088b57a: cmp ecx, eax ; 0x0088b57c: je 0x88b588

### 0x0088b74d
- blocks=8, insns=133, edges=15, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088b873)
- branch points:
  - 0x0088b77b: je -> 0x0088b812 (jcc_true) | ctx: 0x0088b76f: mov dword ptr [ebp - 0x14], esi ; 0x0088b772: mov dword ptr [ebp - 4], 0 ; 0x0088b779: test esi, esi ; 0x0088b77b: je 0x88b812
  - 0x0088b77b: je -> 0x0088b781 (jcc_false) | ctx: 0x0088b76f: mov dword ptr [ebp - 0x14], esi ; 0x0088b772: mov dword ptr [ebp - 4], 0 ; 0x0088b779: test esi, esi ; 0x0088b77b: je 0x88b812
  - 0x0088b86c: je -> 0x0088b878 (jcc_true) | ctx: 0x0088b864: mov eax, dword ptr [edi + 0x3c] ; 0x0088b867: mov dword ptr [esi + 0x3c], eax ; 0x0088b86a: cmp ecx, ebx ; 0x0088b86c: je 0x88b878
  - 0x0088b86c: je -> 0x0088b86e (jcc_false) | ctx: 0x0088b864: mov eax, dword ptr [edi + 0x3c] ; 0x0088b867: mov dword ptr [esi + 0x3c], eax ; 0x0088b86a: cmp ecx, ebx ; 0x0088b86c: je 0x88b878
  - 0x0088b7f4: jb -> 0x0088b7f8 (jcc_true) | ctx: 0x0088b7e2: mov dword ptr [eax + 0x14], 0xf ; 0x0088b7e9: mov dword ptr [eax + 0x10], 0 ; 0x0088b7f0: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088b7f4: jb 0x88b7f8
  - 0x0088b7f4: jb -> 0x0088b7f6 (jcc_false) | ctx: 0x0088b7e2: mov dword ptr [eax + 0x14], 0xf ; 0x0088b7e9: mov dword ptr [eax + 0x10], 0 ; 0x0088b7f0: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088b7f4: jb 0x88b7f8
  - 0x0088b810: jmp -> 0x0088b814 (jmp) | ctx: 0x0088b7fb: mov dword ptr [esi + 0x58], 0xffffffff ; 0x0088b802: mov dword ptr [esi + 0x5c], 0 ; 0x0088b809: mov dword ptr [esi + 0x60], 0 ; 0x0088b810: jmp 0x88b814
  - 0x0088b810: jmp -> 0x0088b814 (jmp) | ctx: 0x0088b7fb: mov dword ptr [esi + 0x58], 0xffffffff ; 0x0088b802: mov dword ptr [esi + 0x5c], 0 ; 0x0088b809: mov dword ptr [esi + 0x60], 0 ; 0x0088b810: jmp 0x88b814
  - 0x0088b86c: je -> 0x0088b878 (jcc_true) | ctx: 0x0088b864: mov eax, dword ptr [edi + 0x3c] ; 0x0088b867: mov dword ptr [esi + 0x3c], eax ; 0x0088b86a: cmp ecx, ebx ; 0x0088b86c: je 0x88b878
  - 0x0088b86c: je -> 0x0088b86e (jcc_false) | ctx: 0x0088b864: mov eax, dword ptr [edi + 0x3c] ; 0x0088b867: mov dword ptr [esi + 0x3c], eax ; 0x0088b86a: cmp ecx, ebx ; 0x0088b86c: je 0x88b878

### 0x0088babd
- blocks=8, insns=111, edges=15, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088bbb7)
- branch points:
  - 0x0088baeb: je -> 0x0088bb62 (jcc_true) | ctx: 0x0088badf: mov dword ptr [ebp - 0x14], esi ; 0x0088bae2: mov dword ptr [ebp - 4], 0 ; 0x0088bae9: test esi, esi ; 0x0088baeb: je 0x88bb62
  - 0x0088baeb: je -> 0x0088baed (jcc_false) | ctx: 0x0088badf: mov dword ptr [ebp - 0x14], esi ; 0x0088bae2: mov dword ptr [ebp - 4], 0 ; 0x0088bae9: test esi, esi ; 0x0088baeb: je 0x88bb62
  - 0x0088bbb0: je -> 0x0088bbbc (jcc_true) | ctx: 0x0088bba6: call 0x7d81a0 ; 0x0088bbab: lea ecx, [esi + 0x38] ; 0x0088bbae: cmp ecx, ebx ; 0x0088bbb0: je 0x88bbbc
  - 0x0088bbb0: je -> 0x0088bbb2 (jcc_false) | ctx: 0x0088bba6: call 0x7d81a0 ; 0x0088bbab: lea ecx, [esi + 0x38] ; 0x0088bbae: cmp ecx, ebx ; 0x0088bbb0: je 0x88bbbc
  - 0x0088bb52: jb -> 0x0088bb56 (jcc_true) | ctx: 0x0088bb40: mov dword ptr [eax + 0x14], 0xf ; 0x0088bb47: mov dword ptr [eax + 0x10], 0 ; 0x0088bb4e: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088bb52: jb 0x88bb56
  - 0x0088bb52: jb -> 0x0088bb54 (jcc_false) | ctx: 0x0088bb40: mov dword ptr [eax + 0x14], 0xf ; 0x0088bb47: mov dword ptr [eax + 0x10], 0 ; 0x0088bb4e: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088bb52: jb 0x88bb56
  - 0x0088bb60: jmp -> 0x0088bb64 (jmp) | ctx: 0x0088bb56: mov byte ptr [eax], 0 ; 0x0088bb59: mov dword ptr [esi + 0x50], 0xffffffff ; 0x0088bb60: jmp 0x88bb64
  - 0x0088bb60: jmp -> 0x0088bb64 (jmp) | ctx: 0x0088bb54: mov eax, dword ptr [eax] ; 0x0088bb56: mov byte ptr [eax], 0 ; 0x0088bb59: mov dword ptr [esi + 0x50], 0xffffffff ; 0x0088bb60: jmp 0x88bb64
  - 0x0088bbb0: je -> 0x0088bbbc (jcc_true) | ctx: 0x0088bba6: call 0x7d81a0 ; 0x0088bbab: lea ecx, [esi + 0x38] ; 0x0088bbae: cmp ecx, ebx ; 0x0088bbb0: je 0x88bbbc
  - 0x0088bbb0: je -> 0x0088bbb2 (jcc_false) | ctx: 0x0088bba6: call 0x7d81a0 ; 0x0088bbab: lea ecx, [esi + 0x38] ; 0x0088bbae: cmp ecx, ebx ; 0x0088bbb0: je 0x88bbbc

### 0x0088bf0d
- blocks=8, insns=121, edges=15, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088c025)
- branch points:
  - 0x0088bf3b: je -> 0x0088bfc4 (jcc_true) | ctx: 0x0088bf2f: mov dword ptr [ebp - 0x14], esi ; 0x0088bf32: mov dword ptr [ebp - 4], 0 ; 0x0088bf39: test esi, esi ; 0x0088bf3b: je 0x88bfc4
  - 0x0088bf3b: je -> 0x0088bf41 (jcc_false) | ctx: 0x0088bf2f: mov dword ptr [ebp - 0x14], esi ; 0x0088bf32: mov dword ptr [ebp - 4], 0 ; 0x0088bf39: test esi, esi ; 0x0088bf3b: je 0x88bfc4
  - 0x0088c01e: je -> 0x0088c02a (jcc_true) | ctx: 0x0088c016: mov eax, dword ptr [edi + 0x3c] ; 0x0088c019: mov dword ptr [esi + 0x3c], eax ; 0x0088c01c: cmp ecx, ebx ; 0x0088c01e: je 0x88c02a
  - 0x0088c01e: je -> 0x0088c020 (jcc_false) | ctx: 0x0088c016: mov eax, dword ptr [edi + 0x3c] ; 0x0088c019: mov dword ptr [esi + 0x3c], eax ; 0x0088c01c: cmp ecx, ebx ; 0x0088c01e: je 0x88c02a
  - 0x0088bfb4: jb -> 0x0088bfb8 (jcc_true) | ctx: 0x0088bfa2: mov dword ptr [eax + 0x14], 0xf ; 0x0088bfa9: mov dword ptr [eax + 0x10], 0 ; 0x0088bfb0: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088bfb4: jb 0x88bfb8
  - 0x0088bfb4: jb -> 0x0088bfb6 (jcc_false) | ctx: 0x0088bfa2: mov dword ptr [eax + 0x14], 0xf ; 0x0088bfa9: mov dword ptr [eax + 0x10], 0 ; 0x0088bfb0: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088bfb4: jb 0x88bfb8
  - 0x0088bfc2: jmp -> 0x0088bfc6 (jmp) | ctx: 0x0088bfb8: mov byte ptr [eax], 0 ; 0x0088bfbb: mov dword ptr [esi + 0x58], 0xffffffff ; 0x0088bfc2: jmp 0x88bfc6
  - 0x0088bfc2: jmp -> 0x0088bfc6 (jmp) | ctx: 0x0088bfb6: mov eax, dword ptr [eax] ; 0x0088bfb8: mov byte ptr [eax], 0 ; 0x0088bfbb: mov dword ptr [esi + 0x58], 0xffffffff ; 0x0088bfc2: jmp 0x88bfc6
  - 0x0088c01e: je -> 0x0088c02a (jcc_true) | ctx: 0x0088c016: mov eax, dword ptr [edi + 0x3c] ; 0x0088c019: mov dword ptr [esi + 0x3c], eax ; 0x0088c01c: cmp ecx, ebx ; 0x0088c01e: je 0x88c02a
  - 0x0088c01e: je -> 0x0088c020 (jcc_false) | ctx: 0x0088c016: mov eax, dword ptr [edi + 0x3c] ; 0x0088c019: mov dword ptr [esi + 0x3c], eax ; 0x0088c01c: cmp ecx, ebx ; 0x0088c01e: je 0x88c02a

### 0x0088c360
- blocks=8, insns=104, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088c44a)
- branch points:
  - 0x0088c3a2: je -> 0x0088c407 (jcc_true) | ctx: 0x0088c39a: mov dword ptr [ebp - 0x10], edi ; 0x0088c39d: mov dword ptr [ebp - 0x10], edi ; 0x0088c3a0: test edi, edi ; 0x0088c3a2: je 0x88c407
  - 0x0088c3a2: je -> 0x0088c3a4 (jcc_false) | ctx: 0x0088c39a: mov dword ptr [ebp - 0x10], edi ; 0x0088c39d: mov dword ptr [ebp - 0x10], edi ; 0x0088c3a0: test edi, edi ; 0x0088c3a2: je 0x88c407
  - 0x0088c443: je -> 0x0088c44f (jcc_true) | ctx: 0x0088c437: lea eax, [ebx + 0x28] ; 0x0088c43a: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088c441: cmp ecx, eax ; 0x0088c443: je 0x88c44f
  - 0x0088c443: je -> 0x0088c445 (jcc_false) | ctx: 0x0088c437: lea eax, [ebx + 0x28] ; 0x0088c43a: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088c441: cmp ecx, eax ; 0x0088c443: je 0x88c44f
  - 0x0088c3f7: jb -> 0x0088c3fb (jcc_true) | ctx: 0x0088c3e5: mov dword ptr [eax + 0x14], 0xf ; 0x0088c3ec: mov dword ptr [eax + 0x10], 0 ; 0x0088c3f3: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088c3f7: jb 0x88c3fb
  - 0x0088c3f7: jb -> 0x0088c3f9 (jcc_false) | ctx: 0x0088c3e5: mov dword ptr [eax + 0x14], 0xf ; 0x0088c3ec: mov dword ptr [eax + 0x10], 0 ; 0x0088c3f3: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088c3f7: jb 0x88c3fb
  - 0x0088c405: jmp -> 0x0088c409 (jmp) | ctx: 0x0088c3fb: mov byte ptr [eax], 0 ; 0x0088c3fe: mov dword ptr [edi + 0x40], 0xffffffff ; 0x0088c405: jmp 0x88c409
  - 0x0088c405: jmp -> 0x0088c409 (jmp) | ctx: 0x0088c3f9: mov eax, dword ptr [eax] ; 0x0088c3fb: mov byte ptr [eax], 0 ; 0x0088c3fe: mov dword ptr [edi + 0x40], 0xffffffff ; 0x0088c405: jmp 0x88c409
  - 0x0088c443: je -> 0x0088c44f (jcc_true) | ctx: 0x0088c437: lea eax, [ebx + 0x28] ; 0x0088c43a: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088c441: cmp ecx, eax ; 0x0088c443: je 0x88c44f
  - 0x0088c443: je -> 0x0088c445 (jcc_false) | ctx: 0x0088c437: lea eax, [ebx + 0x28] ; 0x0088c43a: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088c441: cmp ecx, eax ; 0x0088c443: je 0x88c44f

### 0x0088c470
- blocks=11, insns=184, edges=22, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088c5a4)
- branch points:
  - 0x0088c4b7: jne -> 0x0088c52f (jcc_true) | ctx: 0x0088c4ac: mov dword ptr [ebp - 0x10], 0 ; 0x0088c4b3: push eax ; 0x0088c4b4: lea ecx, [ecx + 0x40] ; 0x0088c4b7: jne 0x88c52f
  - 0x0088c4b7: jne -> 0x0088c4b9 (jcc_false) | ctx: 0x0088c4ac: mov dword ptr [ebp - 0x10], 0 ; 0x0088c4b3: push eax ; 0x0088c4b4: lea ecx, [ecx + 0x40] ; 0x0088c4b7: jne 0x88c52f
  - 0x0088c546: je -> 0x0088c54f (jcc_true) | ctx: 0x0088c53a: mov dword ptr [ebp - 0x10], ecx ; 0x0088c53d: mov dword ptr [ebp - 4], 1 ; 0x0088c544: test ecx, ecx ; 0x0088c546: je 0x88c54f
  - 0x0088c546: je -> 0x0088c548 (jcc_false) | ctx: 0x0088c53a: mov dword ptr [ebp - 0x10], ecx ; 0x0088c53d: mov dword ptr [ebp - 4], 1 ; 0x0088c544: test ecx, ecx ; 0x0088c546: je 0x88c54f
  - 0x0088c4d0: je -> 0x0088c4d9 (jcc_true) | ctx: 0x0088c4c4: mov dword ptr [ebp - 0x18], ecx ; 0x0088c4c7: mov dword ptr [ebp - 4], 0 ; 0x0088c4ce: test ecx, ecx ; 0x0088c4d0: je 0x88c4d9
  - 0x0088c4d0: je -> 0x0088c4d2 (jcc_false) | ctx: 0x0088c4c4: mov dword ptr [ebp - 0x18], ecx ; 0x0088c4c7: mov dword ptr [ebp - 4], 0 ; 0x0088c4ce: test ecx, ecx ; 0x0088c4d0: je 0x88c4d9
  - 0x0088c59d: je -> 0x0088c5a9 (jcc_true) | ctx: 0x0088c595: mov dword ptr [esi + 0x30], ebx ; 0x0088c598: mov dword ptr [esi + 0x58], edi ; 0x0088c59b: cmp ecx, eax ; 0x0088c59d: je 0x88c5a9
  - 0x0088c59d: je -> 0x0088c59f (jcc_false) | ctx: 0x0088c595: mov dword ptr [esi + 0x30], ebx ; 0x0088c598: mov dword ptr [esi + 0x58], edi ; 0x0088c59b: cmp ecx, eax ; 0x0088c59d: je 0x88c5a9
  - 0x0088c54d: jmp -> 0x0088c551 (jmp) | ctx: 0x0088c548: call 0x87fc60 ; 0x0088c54d: jmp 0x88c551
  - 0x0088c4d7: jmp -> 0x0088c4db (jmp) | ctx: 0x0088c4d2: call 0x87fc60 ; 0x0088c4d7: jmp 0x88c4db
  - 0x0088c59d: je -> 0x0088c5a9 (jcc_true) | ctx: 0x0088c595: mov dword ptr [esi + 0x30], ebx ; 0x0088c598: mov dword ptr [esi + 0x58], edi ; 0x0088c59b: cmp ecx, eax ; 0x0088c59d: je 0x88c5a9
  - 0x0088c59d: je -> 0x0088c59f (jcc_false) | ctx: 0x0088c595: mov dword ptr [esi + 0x30], ebx ; 0x0088c598: mov dword ptr [esi + 0x58], edi ; 0x0088c59b: cmp ecx, eax ; 0x0088c59d: je 0x88c5a9

### 0x0088c71b
- blocks=8, insns=106, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088c7f8)
- branch points:
  - 0x0088c742: je -> 0x0088c7b5 (jcc_true) | ctx: 0x0088c73a: mov dword ptr [ebp - 0x10], esi ; 0x0088c73d: mov dword ptr [ebp - 0x10], esi ; 0x0088c740: test esi, esi ; 0x0088c742: je 0x88c7b5
  - 0x0088c742: je -> 0x0088c744 (jcc_false) | ctx: 0x0088c73a: mov dword ptr [ebp - 0x10], esi ; 0x0088c73d: mov dword ptr [ebp - 0x10], esi ; 0x0088c740: test esi, esi ; 0x0088c742: je 0x88c7b5
  - 0x0088c7f1: je -> 0x0088c7fd (jcc_true) | ctx: 0x0088c7e4: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088c7eb: mov word ptr [esi + 0x20], ax ; 0x0088c7ef: cmp ecx, ebx ; 0x0088c7f1: je 0x88c7fd
  - 0x0088c7f1: je -> 0x0088c7f3 (jcc_false) | ctx: 0x0088c7e4: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088c7eb: mov word ptr [esi + 0x20], ax ; 0x0088c7ef: cmp ecx, ebx ; 0x0088c7f1: je 0x88c7fd
  - 0x0088c797: jb -> 0x0088c79b (jcc_true) | ctx: 0x0088c785: mov dword ptr [eax + 0x14], 0xf ; 0x0088c78c: mov dword ptr [eax + 0x10], 0 ; 0x0088c793: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088c797: jb 0x88c79b
  - 0x0088c797: jb -> 0x0088c799 (jcc_false) | ctx: 0x0088c785: mov dword ptr [eax + 0x14], 0xf ; 0x0088c78c: mov dword ptr [eax + 0x10], 0 ; 0x0088c793: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088c797: jb 0x88c79b
  - 0x0088c7b3: jmp -> 0x0088c7b7 (jmp) | ctx: 0x0088c79e: mov dword ptr [esi + 0x40], 0xffffffff ; 0x0088c7a5: mov dword ptr [esi + 0x48], 0xffffffff ; 0x0088c7ac: mov dword ptr [esi + 0x4c], 0xffffffff ; 0x0088c7b3: jmp 0x88c7b7
  - 0x0088c7b3: jmp -> 0x0088c7b7 (jmp) | ctx: 0x0088c79e: mov dword ptr [esi + 0x40], 0xffffffff ; 0x0088c7a5: mov dword ptr [esi + 0x48], 0xffffffff ; 0x0088c7ac: mov dword ptr [esi + 0x4c], 0xffffffff ; 0x0088c7b3: jmp 0x88c7b7
  - 0x0088c7f1: je -> 0x0088c7fd (jcc_true) | ctx: 0x0088c7e4: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088c7eb: mov word ptr [esi + 0x20], ax ; 0x0088c7ef: cmp ecx, ebx ; 0x0088c7f1: je 0x88c7fd
  - 0x0088c7f1: je -> 0x0088c7f3 (jcc_false) | ctx: 0x0088c7e4: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088c7eb: mov word ptr [esi + 0x20], ax ; 0x0088c7ef: cmp ecx, ebx ; 0x0088c7f1: je 0x88c7fd

### 0x0088c830
- blocks=8, insns=134, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088c95d)
- branch points:
  - 0x0088c87a: je -> 0x0088c8f4 (jcc_true) | ctx: 0x0088c872: mov dword ptr [ebp - 0x10], ecx ; 0x0088c875: mov dword ptr [ebp - 0x18], ecx ; 0x0088c878: test ecx, ecx ; 0x0088c87a: je 0x88c8f4
  - 0x0088c87a: je -> 0x0088c87c (jcc_false) | ctx: 0x0088c872: mov dword ptr [ebp - 0x10], ecx ; 0x0088c875: mov dword ptr [ebp - 0x18], ecx ; 0x0088c878: test ecx, ecx ; 0x0088c87a: je 0x88c8f4
  - 0x0088c956: je -> 0x0088c962 (jcc_true) | ctx: 0x0088c94e: add ecx, 0x30 ; 0x0088c951: lea eax, [ebx + 0x30] ; 0x0088c954: cmp ecx, eax ; 0x0088c956: je 0x88c962
  - 0x0088c956: je -> 0x0088c958 (jcc_false) | ctx: 0x0088c94e: add ecx, 0x30 ; 0x0088c951: lea eax, [ebx + 0x30] ; 0x0088c954: cmp ecx, eax ; 0x0088c956: je 0x88c962
  - 0x0088c8e4: jb -> 0x0088c8e8 (jcc_true) | ctx: 0x0088c8d2: mov dword ptr [eax + 0x14], 0xf ; 0x0088c8d9: mov dword ptr [eax + 0x10], 0 ; 0x0088c8e0: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088c8e4: jb 0x88c8e8
  - 0x0088c8e4: jb -> 0x0088c8e6 (jcc_false) | ctx: 0x0088c8d2: mov dword ptr [eax + 0x14], 0xf ; 0x0088c8d9: mov dword ptr [eax + 0x10], 0 ; 0x0088c8e0: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088c8e4: jb 0x88c8e8
  - 0x0088c8f2: jmp -> 0x0088c8f9 (jmp) | ctx: 0x0088c8e8: mov byte ptr [eax], 0 ; 0x0088c8eb: mov dword ptr [ecx + 0x48], 0xffffffff ; 0x0088c8f2: jmp 0x88c8f9
  - 0x0088c8f2: jmp -> 0x0088c8f9 (jmp) | ctx: 0x0088c8e6: mov eax, dword ptr [eax] ; 0x0088c8e8: mov byte ptr [eax], 0 ; 0x0088c8eb: mov dword ptr [ecx + 0x48], 0xffffffff ; 0x0088c8f2: jmp 0x88c8f9
  - 0x0088c956: je -> 0x0088c962 (jcc_true) | ctx: 0x0088c94e: add ecx, 0x30 ; 0x0088c951: lea eax, [ebx + 0x30] ; 0x0088c954: cmp ecx, eax ; 0x0088c956: je 0x88c962
  - 0x0088c956: je -> 0x0088c958 (jcc_false) | ctx: 0x0088c94e: add ecx, 0x30 ; 0x0088c951: lea eax, [ebx + 0x30] ; 0x0088c954: cmp ecx, eax ; 0x0088c956: je 0x88c962

### 0x0088c980
- blocks=8, insns=104, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088ca6a)
- branch points:
  - 0x0088c9c2: je -> 0x0088ca27 (jcc_true) | ctx: 0x0088c9ba: mov dword ptr [ebp - 0x10], edi ; 0x0088c9bd: mov dword ptr [ebp - 0x10], edi ; 0x0088c9c0: test edi, edi ; 0x0088c9c2: je 0x88ca27
  - 0x0088c9c2: je -> 0x0088c9c4 (jcc_false) | ctx: 0x0088c9ba: mov dword ptr [ebp - 0x10], edi ; 0x0088c9bd: mov dword ptr [ebp - 0x10], edi ; 0x0088c9c0: test edi, edi ; 0x0088c9c2: je 0x88ca27
  - 0x0088ca63: je -> 0x0088ca6f (jcc_true) | ctx: 0x0088ca57: lea eax, [ebx + 0x28] ; 0x0088ca5a: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088ca61: cmp ecx, eax ; 0x0088ca63: je 0x88ca6f
  - 0x0088ca63: je -> 0x0088ca65 (jcc_false) | ctx: 0x0088ca57: lea eax, [ebx + 0x28] ; 0x0088ca5a: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088ca61: cmp ecx, eax ; 0x0088ca63: je 0x88ca6f
  - 0x0088ca17: jb -> 0x0088ca1b (jcc_true) | ctx: 0x0088ca05: mov dword ptr [eax + 0x14], 0xf ; 0x0088ca0c: mov dword ptr [eax + 0x10], 0 ; 0x0088ca13: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088ca17: jb 0x88ca1b
  - 0x0088ca17: jb -> 0x0088ca19 (jcc_false) | ctx: 0x0088ca05: mov dword ptr [eax + 0x14], 0xf ; 0x0088ca0c: mov dword ptr [eax + 0x10], 0 ; 0x0088ca13: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088ca17: jb 0x88ca1b
  - 0x0088ca25: jmp -> 0x0088ca29 (jmp) | ctx: 0x0088ca1b: mov byte ptr [eax], 0 ; 0x0088ca1e: mov dword ptr [edi + 0x40], 0xffffffff ; 0x0088ca25: jmp 0x88ca29
  - 0x0088ca25: jmp -> 0x0088ca29 (jmp) | ctx: 0x0088ca19: mov eax, dword ptr [eax] ; 0x0088ca1b: mov byte ptr [eax], 0 ; 0x0088ca1e: mov dword ptr [edi + 0x40], 0xffffffff ; 0x0088ca25: jmp 0x88ca29
  - 0x0088ca63: je -> 0x0088ca6f (jcc_true) | ctx: 0x0088ca57: lea eax, [ebx + 0x28] ; 0x0088ca5a: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088ca61: cmp ecx, eax ; 0x0088ca63: je 0x88ca6f
  - 0x0088ca63: je -> 0x0088ca65 (jcc_false) | ctx: 0x0088ca57: lea eax, [ebx + 0x28] ; 0x0088ca5a: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088ca61: cmp ecx, eax ; 0x0088ca63: je 0x88ca6f

### 0x0088ccf0
- blocks=8, insns=134, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088ce1d)
- branch points:
  - 0x0088cd3a: je -> 0x0088cdb4 (jcc_true) | ctx: 0x0088cd32: mov dword ptr [ebp - 0x10], ecx ; 0x0088cd35: mov dword ptr [ebp - 0x18], ecx ; 0x0088cd38: test ecx, ecx ; 0x0088cd3a: je 0x88cdb4
  - 0x0088cd3a: je -> 0x0088cd3c (jcc_false) | ctx: 0x0088cd32: mov dword ptr [ebp - 0x10], ecx ; 0x0088cd35: mov dword ptr [ebp - 0x18], ecx ; 0x0088cd38: test ecx, ecx ; 0x0088cd3a: je 0x88cdb4
  - 0x0088ce16: je -> 0x0088ce22 (jcc_true) | ctx: 0x0088ce0e: add ecx, 0x30 ; 0x0088ce11: lea eax, [ebx + 0x30] ; 0x0088ce14: cmp ecx, eax ; 0x0088ce16: je 0x88ce22
  - 0x0088ce16: je -> 0x0088ce18 (jcc_false) | ctx: 0x0088ce0e: add ecx, 0x30 ; 0x0088ce11: lea eax, [ebx + 0x30] ; 0x0088ce14: cmp ecx, eax ; 0x0088ce16: je 0x88ce22
  - 0x0088cda4: jb -> 0x0088cda8 (jcc_true) | ctx: 0x0088cd92: mov dword ptr [eax + 0x14], 0xf ; 0x0088cd99: mov dword ptr [eax + 0x10], 0 ; 0x0088cda0: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088cda4: jb 0x88cda8
  - 0x0088cda4: jb -> 0x0088cda6 (jcc_false) | ctx: 0x0088cd92: mov dword ptr [eax + 0x14], 0xf ; 0x0088cd99: mov dword ptr [eax + 0x10], 0 ; 0x0088cda0: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088cda4: jb 0x88cda8
  - 0x0088cdb2: jmp -> 0x0088cdb9 (jmp) | ctx: 0x0088cda8: mov byte ptr [eax], 0 ; 0x0088cdab: mov dword ptr [ecx + 0x48], 0xffffffff ; 0x0088cdb2: jmp 0x88cdb9
  - 0x0088cdb2: jmp -> 0x0088cdb9 (jmp) | ctx: 0x0088cda6: mov eax, dword ptr [eax] ; 0x0088cda8: mov byte ptr [eax], 0 ; 0x0088cdab: mov dword ptr [ecx + 0x48], 0xffffffff ; 0x0088cdb2: jmp 0x88cdb9
  - 0x0088ce16: je -> 0x0088ce22 (jcc_true) | ctx: 0x0088ce0e: add ecx, 0x30 ; 0x0088ce11: lea eax, [ebx + 0x30] ; 0x0088ce14: cmp ecx, eax ; 0x0088ce16: je 0x88ce22
  - 0x0088ce16: je -> 0x0088ce18 (jcc_false) | ctx: 0x0088ce0e: add ecx, 0x30 ; 0x0088ce11: lea eax, [ebx + 0x30] ; 0x0088ce14: cmp ecx, eax ; 0x0088ce16: je 0x88ce22

### 0x0088d7c0
- blocks=15, insns=168, edges=33, jcc=10, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088d913)
- branch points:
  - 0x0088d80e: je -> 0x0088d876 (jcc_true) | ctx: 0x0088d802: mov dword ptr [ebp - 0x18], edi ; 0x0088d805: mov dword ptr [ebp - 4], 0 ; 0x0088d80c: test edi, edi ; 0x0088d80e: je 0x88d876
  - 0x0088d80e: je -> 0x0088d810 (jcc_false) | ctx: 0x0088d802: mov dword ptr [ebp - 0x18], edi ; 0x0088d805: mov dword ptr [ebp - 4], 0 ; 0x0088d80c: test edi, edi ; 0x0088d80e: je 0x88d876
  - 0x0088d8a1: jne -> 0x0088d8a7 (jcc_true) | ctx: 0x0088d893: mov dword ptr [ebp - 0x20], 0 ; 0x0088d89a: mov byte ptr [ebp - 0x30], 0 ; 0x0088d89e: cmp byte ptr [edx], 0 ; 0x0088d8a1: jne 0x88d8a7
  - 0x0088d8a1: jne -> 0x0088d8a3 (jcc_false) | ctx: 0x0088d893: mov dword ptr [ebp - 0x20], 0 ; 0x0088d89a: mov byte ptr [ebp - 0x30], 0 ; 0x0088d89e: cmp byte ptr [edx], 0 ; 0x0088d8a1: jne 0x88d8a7
  - 0x0088d866: jb -> 0x0088d86a (jcc_true) | ctx: 0x0088d854: mov dword ptr [eax + 0x14], 0xf ; 0x0088d85b: mov dword ptr [eax + 0x10], 0 ; 0x0088d862: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088d866: jb 0x88d86a
  - 0x0088d866: jb -> 0x0088d868 (jcc_false) | ctx: 0x0088d854: mov dword ptr [eax + 0x14], 0xf ; 0x0088d85b: mov dword ptr [eax + 0x10], 0 ; 0x0088d862: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088d866: jb 0x88d86a
  - 0x0088d8b5: jne -> 0x0088d8b0 (jcc_true) | ctx: 0x0088d8b0: mov al, byte ptr [ecx] ; 0x0088d8b2: inc ecx ; 0x0088d8b3: test al, al ; 0x0088d8b5: jne 0x88d8b0
  - 0x0088d8b5: jne -> 0x0088d8b7 (jcc_false) | ctx: 0x0088d8b0: mov al, byte ptr [ecx] ; 0x0088d8b2: inc ecx ; 0x0088d8b3: test al, al ; 0x0088d8b5: jne 0x88d8b0
  - 0x0088d8a5: jmp -> 0x0088d8b9 (jmp) | ctx: 0x0088d8a3: xor ecx, ecx ; 0x0088d8a5: jmp 0x88d8b9
  - 0x0088d874: jmp -> 0x0088d878 (jmp) | ctx: 0x0088d86a: mov byte ptr [eax], 0 ; 0x0088d86d: mov dword ptr [edi + 0x4c], 0xffffffff ; 0x0088d874: jmp 0x88d878
  - 0x0088d874: jmp -> 0x0088d878 (jmp) | ctx: 0x0088d868: mov eax, dword ptr [eax] ; 0x0088d86a: mov byte ptr [eax], 0 ; 0x0088d86d: mov dword ptr [edi + 0x4c], 0xffffffff ; 0x0088d874: jmp 0x88d878
  - 0x0088d8b5: jne -> 0x0088d8b0 (jcc_true) | ctx: 0x0088d8b0: mov al, byte ptr [ecx] ; 0x0088d8b2: inc ecx ; 0x0088d8b3: test al, al ; 0x0088d8b5: jne 0x88d8b0
  - 0x0088d8b5: jne -> 0x0088d8b7 (jcc_false) | ctx: 0x0088d8b0: mov al, byte ptr [ecx] ; 0x0088d8b2: inc ecx ; 0x0088d8b3: test al, al ; 0x0088d8b5: jne 0x88d8b0
  - 0x0088d90c: je -> 0x0088d918 (jcc_true) | ctx: 0x0088d904: lea ecx, [edi + 0x34] ; 0x0088d907: lea eax, [ebp - 0x30] ; 0x0088d90a: cmp ecx, eax ; 0x0088d90c: je 0x88d918
  - 0x0088d90c: je -> 0x0088d90e (jcc_false) | ctx: 0x0088d904: lea ecx, [edi + 0x34] ; 0x0088d907: lea eax, [ebp - 0x30] ; 0x0088d90a: cmp ecx, eax ; 0x0088d90c: je 0x88d918
  - 0x0088d90c: je -> 0x0088d918 (jcc_true) | ctx: 0x0088d904: lea ecx, [edi + 0x34] ; 0x0088d907: lea eax, [ebp - 0x30] ; 0x0088d90a: cmp ecx, eax ; 0x0088d90c: je 0x88d918
  - 0x0088d90c: je -> 0x0088d90e (jcc_false) | ctx: 0x0088d904: lea ecx, [edi + 0x34] ; 0x0088d907: lea eax, [ebp - 0x30] ; 0x0088d90a: cmp ecx, eax ; 0x0088d90c: je 0x88d918
  - 0x0088d8a1: jne -> 0x0088d8a7 (jcc_true) | ctx: 0x0088d893: mov dword ptr [ebp - 0x20], 0 ; 0x0088d89a: mov byte ptr [ebp - 0x30], 0 ; 0x0088d89e: cmp byte ptr [edx], 0 ; 0x0088d8a1: jne 0x88d8a7
  - 0x0088d8a1: jne -> 0x0088d8a3 (jcc_false) | ctx: 0x0088d893: mov dword ptr [ebp - 0x20], 0 ; 0x0088d89a: mov byte ptr [ebp - 0x30], 0 ; 0x0088d89e: cmp byte ptr [edx], 0 ; 0x0088d8a1: jne 0x88d8a7
  - 0x0088d926: jb -> 0x0088d933 (jcc_true) | ctx: 0x0088d918: mov dword ptr [edi + 0x4c], esi ; 0x0088d91b: cmp dword ptr [ebp - 0x1c], 0x10 ; 0x0088d91f: mov dword ptr [ebp - 4], 4 ; 0x0088d926: jb 0x88d933
  - 0x0088d926: jb -> 0x0088d928 (jcc_false) | ctx: 0x0088d918: mov dword ptr [edi + 0x4c], esi ; 0x0088d91b: cmp dword ptr [ebp - 0x1c], 0x10 ; 0x0088d91f: mov dword ptr [ebp - 4], 4 ; 0x0088d926: jb 0x88d933
  - 0x0088d926: jb -> 0x0088d933 (jcc_true) | ctx: 0x0088d918: mov dword ptr [edi + 0x4c], esi ; 0x0088d91b: cmp dword ptr [ebp - 0x1c], 0x10 ; 0x0088d91f: mov dword ptr [ebp - 4], 4 ; 0x0088d926: jb 0x88d933
  - 0x0088d926: jb -> 0x0088d928 (jcc_false) | ctx: 0x0088d918: mov dword ptr [edi + 0x4c], esi ; 0x0088d91b: cmp dword ptr [ebp - 0x1c], 0x10 ; 0x0088d91f: mov dword ptr [ebp - 4], 4 ; 0x0088d926: jb 0x88d933

### 0x0088e28b
- blocks=8, insns=94, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088e35a)
- branch points:
  - 0x0088e2b2: je -> 0x0088e317 (jcc_true) | ctx: 0x0088e2aa: mov dword ptr [ebp - 0x10], esi ; 0x0088e2ad: mov dword ptr [ebp - 0x10], esi ; 0x0088e2b0: test esi, esi ; 0x0088e2b2: je 0x88e317
  - 0x0088e2b2: je -> 0x0088e2b4 (jcc_false) | ctx: 0x0088e2aa: mov dword ptr [ebp - 0x10], esi ; 0x0088e2ad: mov dword ptr [ebp - 0x10], esi ; 0x0088e2b0: test esi, esi ; 0x0088e2b2: je 0x88e317
  - 0x0088e353: je -> 0x0088e35f (jcc_true) | ctx: 0x0088e346: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088e34d: mov word ptr [esi + 0x20], ax ; 0x0088e351: cmp ecx, ebx ; 0x0088e353: je 0x88e35f
  - 0x0088e353: je -> 0x0088e355 (jcc_false) | ctx: 0x0088e346: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088e34d: mov word ptr [esi + 0x20], ax ; 0x0088e351: cmp ecx, ebx ; 0x0088e353: je 0x88e35f
  - 0x0088e307: jb -> 0x0088e30b (jcc_true) | ctx: 0x0088e2f5: mov dword ptr [eax + 0x14], 0xf ; 0x0088e2fc: mov dword ptr [eax + 0x10], 0 ; 0x0088e303: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088e307: jb 0x88e30b
  - 0x0088e307: jb -> 0x0088e309 (jcc_false) | ctx: 0x0088e2f5: mov dword ptr [eax + 0x14], 0xf ; 0x0088e2fc: mov dword ptr [eax + 0x10], 0 ; 0x0088e303: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088e307: jb 0x88e30b
  - 0x0088e315: jmp -> 0x0088e319 (jmp) | ctx: 0x0088e30b: mov byte ptr [eax], 0 ; 0x0088e30e: mov dword ptr [esi + 0x40], 0xffffffff ; 0x0088e315: jmp 0x88e319
  - 0x0088e315: jmp -> 0x0088e319 (jmp) | ctx: 0x0088e309: mov eax, dword ptr [eax] ; 0x0088e30b: mov byte ptr [eax], 0 ; 0x0088e30e: mov dword ptr [esi + 0x40], 0xffffffff ; 0x0088e315: jmp 0x88e319
  - 0x0088e353: je -> 0x0088e35f (jcc_true) | ctx: 0x0088e346: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088e34d: mov word ptr [esi + 0x20], ax ; 0x0088e351: cmp ecx, ebx ; 0x0088e353: je 0x88e35f
  - 0x0088e353: je -> 0x0088e355 (jcc_false) | ctx: 0x0088e346: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088e34d: mov word ptr [esi + 0x20], ax ; 0x0088e351: cmp ecx, ebx ; 0x0088e353: je 0x88e35f

### 0x0088e7cd
- blocks=11, insns=193, edges=26, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088e8f8)
- branch points:
  - 0x0088e7f7: jne -> 0x0088e887 (jcc_true) | ctx: 0x0088e7ec: mov dword ptr [ebp - 0x14], 0 ; 0x0088e7f3: push eax ; 0x0088e7f4: lea ecx, [ecx + 0x40] ; 0x0088e7f7: jne 0x88e887
  - 0x0088e7f7: jne -> 0x0088e7fd (jcc_false) | ctx: 0x0088e7ec: mov dword ptr [ebp - 0x14], 0 ; 0x0088e7f3: push eax ; 0x0088e7f4: lea ecx, [ecx + 0x40] ; 0x0088e7f7: jne 0x88e887
  - 0x0088e89e: je -> 0x0088e8a9 (jcc_true) | ctx: 0x0088e892: mov dword ptr [ebp - 0x14], ecx ; 0x0088e895: mov dword ptr [ebp - 4], 1 ; 0x0088e89c: test ecx, ecx ; 0x0088e89e: je 0x88e8a9
  - 0x0088e89e: je -> 0x0088e8a0 (jcc_false) | ctx: 0x0088e892: mov dword ptr [ebp - 0x14], ecx ; 0x0088e895: mov dword ptr [ebp - 4], 1 ; 0x0088e89c: test ecx, ecx ; 0x0088e89e: je 0x88e8a9
  - 0x0088e814: je -> 0x0088e81d (jcc_true) | ctx: 0x0088e808: mov dword ptr [ebp - 0x14], ecx ; 0x0088e80b: mov dword ptr [ebp - 4], 0 ; 0x0088e812: test ecx, ecx ; 0x0088e814: je 0x88e81d
  - 0x0088e814: je -> 0x0088e816 (jcc_false) | ctx: 0x0088e808: mov dword ptr [ebp - 0x14], ecx ; 0x0088e80b: mov dword ptr [ebp - 4], 0 ; 0x0088e812: test ecx, ecx ; 0x0088e814: je 0x88e81d
  - 0x0088e8f1: je -> 0x0088e8fd (jcc_true) | ctx: 0x0088e8e9: lea ecx, [ebx + 0x40] ; 0x0088e8ec: mov dword ptr [ebx + 0x30], edi ; 0x0088e8ef: cmp ecx, eax ; 0x0088e8f1: je 0x88e8fd
  - 0x0088e8f1: je -> 0x0088e8f3 (jcc_false) | ctx: 0x0088e8e9: lea ecx, [ebx + 0x40] ; 0x0088e8ec: mov dword ptr [ebx + 0x30], edi ; 0x0088e8ef: cmp ecx, eax ; 0x0088e8f1: je 0x88e8fd
  - 0x0088e8a7: jmp -> 0x0088e8ab (jmp) | ctx: 0x0088e8a0: call 0x881fd0 ; 0x0088e8a5: mov ebx, eax ; 0x0088e8a7: jmp 0x88e8ab
  - 0x0088e81b: jmp -> 0x0088e81f (jmp) | ctx: 0x0088e816: call 0x881fd0 ; 0x0088e81b: jmp 0x88e81f
  - 0x0088e8f1: je -> 0x0088e8fd (jcc_true) | ctx: 0x0088e8e9: lea ecx, [ebx + 0x40] ; 0x0088e8ec: mov dword ptr [ebx + 0x30], edi ; 0x0088e8ef: cmp ecx, eax ; 0x0088e8f1: je 0x88e8fd
  - 0x0088e8f1: je -> 0x0088e8f3 (jcc_false) | ctx: 0x0088e8e9: lea ecx, [ebx + 0x40] ; 0x0088e8ec: mov dword ptr [ebx + 0x30], edi ; 0x0088e8ef: cmp ecx, eax ; 0x0088e8f1: je 0x88e8fd

### 0x0088e94d
- blocks=8, insns=103, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088ea2c)
- branch points:
  - 0x0088e977: je -> 0x0088e9dd (jcc_true) | ctx: 0x0088e96f: mov dword ptr [ebp - 0x10], ebx ; 0x0088e972: mov dword ptr [ebp - 0x10], ebx ; 0x0088e975: test ebx, ebx ; 0x0088e977: je 0x88e9dd
  - 0x0088e977: je -> 0x0088e979 (jcc_false) | ctx: 0x0088e96f: mov dword ptr [ebp - 0x10], ebx ; 0x0088e972: mov dword ptr [ebp - 0x10], ebx ; 0x0088e975: test ebx, ebx ; 0x0088e977: je 0x88e9dd
  - 0x0088ea25: je -> 0x0088ea31 (jcc_true) | ctx: 0x0088ea19: mov eax, dword ptr [ebp - 0x10] ; 0x0088ea1c: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088ea23: cmp ecx, eax ; 0x0088ea25: je 0x88ea31
  - 0x0088ea25: je -> 0x0088ea27 (jcc_false) | ctx: 0x0088ea19: mov eax, dword ptr [ebp - 0x10] ; 0x0088ea1c: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088ea23: cmp ecx, eax ; 0x0088ea25: je 0x88ea31
  - 0x0088e9cc: jb -> 0x0088e9d0 (jcc_true) | ctx: 0x0088e9ba: mov dword ptr [eax + 0x14], 0xf ; 0x0088e9c1: mov dword ptr [eax + 0x10], 0 ; 0x0088e9c8: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088e9cc: jb 0x88e9d0
  - 0x0088e9cc: jb -> 0x0088e9ce (jcc_false) | ctx: 0x0088e9ba: mov dword ptr [eax + 0x14], 0xf ; 0x0088e9c1: mov dword ptr [eax + 0x10], 0 ; 0x0088e9c8: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088e9cc: jb 0x88e9d0
  - 0x0088e9db: jmp -> 0x0088e9df (jmp) | ctx: 0x0088e9d0: mov byte ptr [eax], 0 ; 0x0088e9d3: mov eax, dword ptr [0xc18510] ; 0x0088e9d8: mov dword ptr [ebx + 0x40], eax ; 0x0088e9db: jmp 0x88e9df
  - 0x0088e9db: jmp -> 0x0088e9df (jmp) | ctx: 0x0088e9d0: mov byte ptr [eax], 0 ; 0x0088e9d3: mov eax, dword ptr [0xc18510] ; 0x0088e9d8: mov dword ptr [ebx + 0x40], eax ; 0x0088e9db: jmp 0x88e9df
  - 0x0088ea25: je -> 0x0088ea31 (jcc_true) | ctx: 0x0088ea19: mov eax, dword ptr [ebp - 0x10] ; 0x0088ea1c: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088ea23: cmp ecx, eax ; 0x0088ea25: je 0x88ea31
  - 0x0088ea25: je -> 0x0088ea27 (jcc_false) | ctx: 0x0088ea19: mov eax, dword ptr [ebp - 0x10] ; 0x0088ea1c: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088ea23: cmp ecx, eax ; 0x0088ea25: je 0x88ea31

### 0x0088ed70
- blocks=8, insns=104, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088ee5a)
- branch points:
  - 0x0088edb2: je -> 0x0088ee17 (jcc_true) | ctx: 0x0088edaa: mov dword ptr [ebp - 0x10], edi ; 0x0088edad: mov dword ptr [ebp - 0x10], edi ; 0x0088edb0: test edi, edi ; 0x0088edb2: je 0x88ee17
  - 0x0088edb2: je -> 0x0088edb4 (jcc_false) | ctx: 0x0088edaa: mov dword ptr [ebp - 0x10], edi ; 0x0088edad: mov dword ptr [ebp - 0x10], edi ; 0x0088edb0: test edi, edi ; 0x0088edb2: je 0x88ee17
  - 0x0088ee53: je -> 0x0088ee5f (jcc_true) | ctx: 0x0088ee47: lea eax, [ebx + 0x28] ; 0x0088ee4a: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088ee51: cmp ecx, eax ; 0x0088ee53: je 0x88ee5f
  - 0x0088ee53: je -> 0x0088ee55 (jcc_false) | ctx: 0x0088ee47: lea eax, [ebx + 0x28] ; 0x0088ee4a: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088ee51: cmp ecx, eax ; 0x0088ee53: je 0x88ee5f
  - 0x0088ee07: jb -> 0x0088ee0b (jcc_true) | ctx: 0x0088edf5: mov dword ptr [eax + 0x14], 0xf ; 0x0088edfc: mov dword ptr [eax + 0x10], 0 ; 0x0088ee03: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088ee07: jb 0x88ee0b
  - 0x0088ee07: jb -> 0x0088ee09 (jcc_false) | ctx: 0x0088edf5: mov dword ptr [eax + 0x14], 0xf ; 0x0088edfc: mov dword ptr [eax + 0x10], 0 ; 0x0088ee03: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088ee07: jb 0x88ee0b
  - 0x0088ee15: jmp -> 0x0088ee19 (jmp) | ctx: 0x0088ee0b: mov byte ptr [eax], 0 ; 0x0088ee0e: mov dword ptr [edi + 0x40], 0xffffffff ; 0x0088ee15: jmp 0x88ee19
  - 0x0088ee15: jmp -> 0x0088ee19 (jmp) | ctx: 0x0088ee09: mov eax, dword ptr [eax] ; 0x0088ee0b: mov byte ptr [eax], 0 ; 0x0088ee0e: mov dword ptr [edi + 0x40], 0xffffffff ; 0x0088ee15: jmp 0x88ee19
  - 0x0088ee53: je -> 0x0088ee5f (jcc_true) | ctx: 0x0088ee47: lea eax, [ebx + 0x28] ; 0x0088ee4a: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088ee51: cmp ecx, eax ; 0x0088ee53: je 0x88ee5f
  - 0x0088ee53: je -> 0x0088ee55 (jcc_false) | ctx: 0x0088ee47: lea eax, [ebx + 0x28] ; 0x0088ee4a: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088ee51: cmp ecx, eax ; 0x0088ee53: je 0x88ee5f

### 0x0088ef5b
- blocks=8, insns=94, edges=12, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088f02a)
- branch points:
  - 0x0088ef82: je -> 0x0088efe7 (jcc_true) | ctx: 0x0088ef7a: mov dword ptr [ebp - 0x10], esi ; 0x0088ef7d: mov dword ptr [ebp - 0x10], esi ; 0x0088ef80: test esi, esi ; 0x0088ef82: je 0x88efe7
  - 0x0088ef82: je -> 0x0088ef84 (jcc_false) | ctx: 0x0088ef7a: mov dword ptr [ebp - 0x10], esi ; 0x0088ef7d: mov dword ptr [ebp - 0x10], esi ; 0x0088ef80: test esi, esi ; 0x0088ef82: je 0x88efe7
  - 0x0088f023: je -> 0x0088f02f (jcc_true) | ctx: 0x0088f016: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088f01d: mov word ptr [esi + 0x20], ax ; 0x0088f021: cmp ecx, ebx ; 0x0088f023: je 0x88f02f
  - 0x0088f023: je -> 0x0088f025 (jcc_false) | ctx: 0x0088f016: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088f01d: mov word ptr [esi + 0x20], ax ; 0x0088f021: cmp ecx, ebx ; 0x0088f023: je 0x88f02f
  - 0x0088efd7: jb -> 0x0088efdb (jcc_true) | ctx: 0x0088efc5: mov dword ptr [eax + 0x14], 0xf ; 0x0088efcc: mov dword ptr [eax + 0x10], 0 ; 0x0088efd3: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088efd7: jb 0x88efdb
  - 0x0088efd7: jb -> 0x0088efd9 (jcc_false) | ctx: 0x0088efc5: mov dword ptr [eax + 0x14], 0xf ; 0x0088efcc: mov dword ptr [eax + 0x10], 0 ; 0x0088efd3: cmp dword ptr [eax + 0x14], 0x10 ; 0x0088efd7: jb 0x88efdb
  - 0x0088efe5: jmp -> 0x0088efe9 (jmp) | ctx: 0x0088efdb: mov byte ptr [eax], 0 ; 0x0088efde: mov dword ptr [esi + 0x40], 0xffffffff ; 0x0088efe5: jmp 0x88efe9
  - 0x0088efe5: jmp -> 0x0088efe9 (jmp) | ctx: 0x0088efd9: mov eax, dword ptr [eax] ; 0x0088efdb: mov byte ptr [eax], 0 ; 0x0088efde: mov dword ptr [esi + 0x40], 0xffffffff ; 0x0088efe5: jmp 0x88efe9
  - 0x0088f023: je -> 0x0088f02f (jcc_true) | ctx: 0x0088f016: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088f01d: mov word ptr [esi + 0x20], ax ; 0x0088f021: cmp ecx, ebx ; 0x0088f023: je 0x88f02f
  - 0x0088f023: je -> 0x0088f025 (jcc_false) | ctx: 0x0088f016: mov dword ptr [ebp - 4], 0xffffffff ; 0x0088f01d: mov word ptr [esi + 0x20], ax ; 0x0088f021: cmp ecx, ebx ; 0x0088f023: je 0x88f02f

### 0x0088f9cf
- blocks=25, insns=297, edges=74, jcc=22, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088fb3b)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088fb52)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0088fb69)
- branch points:
  - 0x0088f9e3: je -> 0x0088fc60 (jcc_true) | ctx: 0x0088f9d9: call 0x956530 ; 0x0088f9de: mov dword ptr [ebp - 0x24], eax ; 0x0088f9e1: test eax, eax ; 0x0088f9e3: je 0x88fc60
  - 0x0088f9e3: je -> 0x0088f9e9 (jcc_false) | ctx: 0x0088f9d9: call 0x956530 ; 0x0088f9de: mov dword ptr [ebp - 0x24], eax ; 0x0088f9e1: test eax, eax ; 0x0088f9e3: je 0x88fc60
  - 0x0088fa04: je -> 0x0088fc60 (jcc_true) | ctx: 0x0088f9fa: call 0x826c00 ; 0x0088f9ff: mov ecx, dword ptr [ebp - 0x18] ; 0x0088fa02: test ecx, ecx ; 0x0088fa04: je 0x88fc60
  - 0x0088fa04: je -> 0x0088fa0a (jcc_false) | ctx: 0x0088f9fa: call 0x826c00 ; 0x0088f9ff: mov ecx, dword ptr [ebp - 0x18] ; 0x0088fa02: test ecx, ecx ; 0x0088fa04: je 0x88fc60
  - 0x0088fa39: je -> 0x0088fa57 (jcc_true) | ctx: 0x0088fa2a: mov di, word ptr [ebp - 0x14] ; 0x0088fa2e: mov word ptr [ebp - 0x20], di ; 0x0088fa32: cmp di, word ptr [0xd6ba64] ; 0x0088fa39: je 0x88fa57
  - 0x0088fa39: je -> 0x0088fa3b (jcc_false) | ctx: 0x0088fa2a: mov di, word ptr [ebp - 0x14] ; 0x0088fa2e: mov word ptr [ebp - 0x20], di ; 0x0088fa32: cmp di, word ptr [0xd6ba64] ; 0x0088fa39: je 0x88fa57
  - 0x0088fa60: jb -> 0x0088fa20 (jcc_true) | ctx: 0x0088fa57: inc ebx ; 0x0088fa58: mov eax, 0xff ; 0x0088fa5d: cmp bx, ax ; 0x0088fa60: jb 0x88fa20
  - 0x0088fa60: jb -> 0x0088fa62 (jcc_false) | ctx: 0x0088fa57: inc ebx ; 0x0088fa58: mov eax, 0xff ; 0x0088fa5d: cmp bx, ax ; 0x0088fa60: jb 0x88fa20
  - 0x0088fa42: je -> 0x0088fa57 (jcc_true) | ctx: 0x0088fa3b: cmp di, word ptr [0xd6ba68] ; 0x0088fa42: je 0x88fa57
  - 0x0088fa42: je -> 0x0088fa44 (jcc_false) | ctx: 0x0088fa3b: cmp di, word ptr [0xd6ba68] ; 0x0088fa42: je 0x88fa57
  - 0x0088fa39: je -> 0x0088fa57 (jcc_true) | ctx: 0x0088fa2a: mov di, word ptr [ebp - 0x14] ; 0x0088fa2e: mov word ptr [ebp - 0x20], di ; 0x0088fa32: cmp di, word ptr [0xd6ba64] ; 0x0088fa39: je 0x88fa57
  - 0x0088fa39: je -> 0x0088fa3b (jcc_false) | ctx: 0x0088fa2a: mov di, word ptr [ebp - 0x14] ; 0x0088fa2e: mov word ptr [ebp - 0x20], di ; 0x0088fa32: cmp di, word ptr [0xd6ba64] ; 0x0088fa39: je 0x88fa57
  - 0x0088fad5: je -> 0x0088fadb (jcc_true) | ctx: 0x0088fac9: mov byte ptr [ebp - 4], 2 ; 0x0088facd: mov dword ptr [ebp - 0xb4], esi ; 0x0088fad3: test eax, eax ; 0x0088fad5: je 0x88fadb
  - 0x0088fad5: je -> 0x0088fad7 (jcc_false) | ctx: 0x0088fac9: mov byte ptr [ebp - 4], 2 ; 0x0088facd: mov dword ptr [ebp - 0xb4], esi ; 0x0088fad3: test eax, eax ; 0x0088fad5: je 0x88fadb
  - 0x0088fa55: je -> 0x0088fa62 (jcc_true) | ctx: 0x0088fa48: lea ecx, [esi + 0xe4] ; 0x0088fa4e: call 0x890ee0 ; 0x0088fa53: test eax, eax ; 0x0088fa55: je 0x88fa62
  - 0x0088fa55: je -> 0x0088fa57 (jcc_false) | ctx: 0x0088fa48: lea ecx, [esi + 0xe4] ; 0x0088fa4e: call 0x890ee0 ; 0x0088fa53: test eax, eax ; 0x0088fa55: je 0x88fa62
  - 0x0088faf2: je -> 0x0088fb14 (jcc_true) | ctx: 0x0088fae4: mov dword ptr [ebp - 0x9c], eax ; 0x0088faea: mov dword ptr [ebp - 0xa0], edx ; 0x0088faf0: test ecx, ecx ; 0x0088faf2: je 0x88fb14
  - 0x0088faf2: je -> 0x0088faf4 (jcc_false) | ctx: 0x0088fae4: mov dword ptr [ebp - 0x9c], eax ; 0x0088faea: mov dword ptr [ebp - 0xa0], edx ; 0x0088faf0: test ecx, ecx ; 0x0088faf2: je 0x88fb14
  - 0x0088faf2: je -> 0x0088fb14 (jcc_true) | ctx: 0x0088fae4: mov dword ptr [ebp - 0x9c], eax ; 0x0088faea: mov dword ptr [ebp - 0xa0], edx ; 0x0088faf0: test ecx, ecx ; 0x0088faf2: je 0x88fb14
  - 0x0088faf2: je -> 0x0088faf4 (jcc_false) | ctx: 0x0088fae4: mov dword ptr [ebp - 0x9c], eax ; 0x0088faea: mov dword ptr [ebp - 0xa0], edx ; 0x0088faf0: test ecx, ecx ; 0x0088faf2: je 0x88fb14
  - 0x0088fb34: je -> 0x0088fb40 (jcc_true) | ctx: 0x0088fb26: mov dword ptr [ebp - 0x94], eax ; 0x0088fb2c: lea eax, [esi + 0x90] ; 0x0088fb32: cmp ecx, eax ; 0x0088fb34: je 0x88fb40
  - 0x0088fb34: je -> 0x0088fb36 (jcc_false) | ctx: 0x0088fb26: mov dword ptr [ebp - 0x94], eax ; 0x0088fb2c: lea eax, [esi + 0x90] ; 0x0088fb32: cmp ecx, eax ; 0x0088fb34: je 0x88fb40
  - 0x0088fafc: jne -> 0x0088fb14 (jcc_true) | ctx: 0x0088faf4: or eax, 0xffffffff ; 0x0088faf7: lock xadd dword ptr [ecx + 4], eax ; 0x0088fafc: jne 0x88fb14
  - 0x0088fafc: jne -> 0x0088fafe (jcc_false) | ctx: 0x0088faf4: or eax, 0xffffffff ; 0x0088faf7: lock xadd dword ptr [ecx + 4], eax ; 0x0088fafc: jne 0x88fb14
  - 0x0088fb4b: je -> 0x0088fb57 (jcc_true) | ctx: 0x0088fb40: lea eax, [esi + 0xa8] ; 0x0088fb46: lea ecx, [ebp - 0x78] ; 0x0088fb49: cmp ecx, eax ; 0x0088fb4b: je 0x88fb57
  - 0x0088fb4b: je -> 0x0088fb4d (jcc_false) | ctx: 0x0088fb40: lea eax, [esi + 0xa8] ; 0x0088fb46: lea ecx, [ebp - 0x78] ; 0x0088fb49: cmp ecx, eax ; 0x0088fb4b: je 0x88fb57
  - 0x0088fb4b: je -> 0x0088fb57 (jcc_true) | ctx: 0x0088fb40: lea eax, [esi + 0xa8] ; 0x0088fb46: lea ecx, [ebp - 0x78] ; 0x0088fb49: cmp ecx, eax ; 0x0088fb4b: je 0x88fb57
  - 0x0088fb4b: je -> 0x0088fb4d (jcc_false) | ctx: 0x0088fb40: lea eax, [esi + 0xa8] ; 0x0088fb46: lea ecx, [ebp - 0x78] ; 0x0088fb49: cmp ecx, eax ; 0x0088fb4b: je 0x88fb57
  - 0x0088fb0d: jne -> 0x0088fb14 (jcc_true) | ctx: 0x0088fb02: mov ecx, dword ptr [ebp - 0x18] ; 0x0088fb05: or eax, 0xffffffff ; 0x0088fb08: lock xadd dword ptr [ecx + 8], eax ; 0x0088fb0d: jne 0x88fb14
  - 0x0088fb0d: jne -> 0x0088fb0f (jcc_false) | ctx: 0x0088fb02: mov ecx, dword ptr [ebp - 0x18] ; 0x0088fb05: or eax, 0xffffffff ; 0x0088fb08: lock xadd dword ptr [ecx + 8], eax ; 0x0088fb0d: jne 0x88fb14
  - 0x0088fb62: je -> 0x0088fb6e (jcc_true) | ctx: 0x0088fb57: lea eax, [esi + 0xc0] ; 0x0088fb5d: lea ecx, [ebp - 0x60] ; 0x0088fb60: cmp ecx, eax ; 0x0088fb62: je 0x88fb6e
  - 0x0088fb62: je -> 0x0088fb64 (jcc_false) | ctx: 0x0088fb57: lea eax, [esi + 0xc0] ; 0x0088fb5d: lea ecx, [ebp - 0x60] ; 0x0088fb60: cmp ecx, eax ; 0x0088fb62: je 0x88fb6e
  - 0x0088fb62: je -> 0x0088fb6e (jcc_true) | ctx: 0x0088fb57: lea eax, [esi + 0xc0] ; 0x0088fb5d: lea ecx, [ebp - 0x60] ; 0x0088fb60: cmp ecx, eax ; 0x0088fb62: je 0x88fb6e
  - 0x0088fb62: je -> 0x0088fb64 (jcc_false) | ctx: 0x0088fb57: lea eax, [esi + 0xc0] ; 0x0088fb5d: lea ecx, [ebp - 0x60] ; 0x0088fb60: cmp ecx, eax ; 0x0088fb62: je 0x88fb6e
  - 0x0088fb34: je -> 0x0088fb40 (jcc_true) | ctx: 0x0088fb26: mov dword ptr [ebp - 0x94], eax ; 0x0088fb2c: lea eax, [esi + 0x90] ; 0x0088fb32: cmp ecx, eax ; 0x0088fb34: je 0x88fb40
  - 0x0088fb34: je -> 0x0088fb36 (jcc_false) | ctx: 0x0088fb26: mov dword ptr [ebp - 0x94], eax ; 0x0088fb2c: lea eax, [esi + 0x90] ; 0x0088fb32: cmp ecx, eax ; 0x0088fb34: je 0x88fb40
  - 0x0088fbe8: je -> 0x0088fc08 (jcc_true) | ctx: 0x0088fbdd: mov ecx, dword ptr [ebp + 8] ; 0x0088fbe0: mov eax, dword ptr [ecx] ; 0x0088fbe2: cmp eax, dword ptr [0xd6ba60] ; 0x0088fbe8: je 0x88fc08
  - 0x0088fbe8: je -> 0x0088fbea (jcc_false) | ctx: 0x0088fbdd: mov ecx, dword ptr [ebp + 8] ; 0x0088fbe0: mov eax, dword ptr [ecx] ; 0x0088fbe2: cmp eax, dword ptr [0xd6ba60] ; 0x0088fbe8: je 0x88fc08
  - 0x0088fbe8: je -> 0x0088fc08 (jcc_true) | ctx: 0x0088fbdd: mov ecx, dword ptr [ebp + 8] ; 0x0088fbe0: mov eax, dword ptr [ecx] ; 0x0088fbe2: cmp eax, dword ptr [0xd6ba60] ; 0x0088fbe8: je 0x88fc08
  - 0x0088fbe8: je -> 0x0088fbea (jcc_false) | ctx: 0x0088fbdd: mov ecx, dword ptr [ebp + 8] ; 0x0088fbe0: mov eax, dword ptr [ecx] ; 0x0088fbe2: cmp eax, dword ptr [0xd6ba60] ; 0x0088fbe8: je 0x88fc08
  - 0x0088fc17: je -> 0x0088fc31 (jcc_true) | ctx: 0x0088fc0d: call 0x956c80 ; 0x0088fc12: mov ecx, dword ptr [eax] ; 0x0088fc14: cmp ecx, dword ptr [eax + 4] ; 0x0088fc17: je 0x88fc31
  - 0x0088fc17: je -> 0x0088fc19 (jcc_false) | ctx: 0x0088fc0d: call 0x956c80 ; 0x0088fc12: mov ecx, dword ptr [eax] ; 0x0088fc14: cmp ecx, dword ptr [eax + 4] ; 0x0088fc17: je 0x88fc31
  - 0x0088fc17: je -> 0x0088fc31 (jcc_true) | ctx: 0x0088fc0d: call 0x956c80 ; 0x0088fc12: mov ecx, dword ptr [eax] ; 0x0088fc14: cmp ecx, dword ptr [eax + 4] ; 0x0088fc17: je 0x88fc31
  - 0x0088fc17: je -> 0x0088fc19 (jcc_false) | ctx: 0x0088fc0d: call 0x956c80 ; 0x0088fc12: mov ecx, dword ptr [eax] ; 0x0088fc14: cmp ecx, dword ptr [eax + 4] ; 0x0088fc17: je 0x88fc31

### 0x00890620
- blocks=15, insns=123, edges=28, jcc=11, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x008906f2)
- branch points:
  - 0x0089064f: jne -> 0x00890665 (jcc_true) | ctx: 0x00890646: mov eax, edx ; 0x00890648: mov esi, dword ptr [edx + 4] ; 0x0089064b: cmp byte ptr [esi + 0xd], 0 ; 0x0089064f: jne 0x890665
  - 0x0089064f: jne -> 0x00890651 (jcc_false) | ctx: 0x00890646: mov eax, edx ; 0x00890648: mov esi, dword ptr [edx + 4] ; 0x0089064b: cmp byte ptr [esi + 0xd], 0 ; 0x0089064f: jne 0x890665
  - 0x00890667: je -> 0x0089066e (jcc_true) | ctx: 0x00890665: cmp eax, edx ; 0x00890667: je 0x89066e
  - 0x00890667: je -> 0x00890669 (jcc_false) | ctx: 0x00890665: cmp eax, edx ; 0x00890667: je 0x89066e
  - 0x00890654: jae -> 0x0089065b (jcc_true) | ctx: 0x00890651: cmp dword ptr [esi + 0x10], edi ; 0x00890654: jae 0x89065b
  - 0x00890654: jae -> 0x00890656 (jcc_false) | ctx: 0x00890651: cmp dword ptr [esi + 0x10], edi ; 0x00890654: jae 0x89065b
  - 0x00890672: jne -> 0x00890697 (jcc_true) | ctx: 0x0089066e: mov eax, edx ; 0x00890670: cmp eax, edx ; 0x00890672: jne 0x890697
  - 0x00890672: jne -> 0x00890674 (jcc_false) | ctx: 0x0089066e: mov eax, edx ; 0x00890670: cmp eax, edx ; 0x00890672: jne 0x890697
  - 0x0089066c: jae -> 0x00890670 (jcc_true) | ctx: 0x00890669: cmp edi, dword ptr [eax + 0x10] ; 0x0089066c: jae 0x890670
  - 0x0089066c: jae -> 0x0089066e (jcc_false) | ctx: 0x00890669: cmp edi, dword ptr [eax + 0x10] ; 0x0089066c: jae 0x890670
  - 0x00890663: je -> 0x00890651 (jcc_true) | ctx: 0x0089065b: mov eax, esi ; 0x0089065d: mov esi, dword ptr [esi] ; 0x0089065f: cmp byte ptr [esi + 0xd], 0 ; 0x00890663: je 0x890651
  - 0x00890663: je -> 0x00890665 (jcc_false) | ctx: 0x0089065b: mov eax, esi ; 0x0089065d: mov esi, dword ptr [esi] ; 0x0089065f: cmp byte ptr [esi + 0xd], 0 ; 0x00890663: je 0x890651
  - 0x00890659: jmp -> 0x0089065f (jmp) | ctx: 0x00890656: mov esi, dword ptr [esi + 8] ; 0x00890659: jmp 0x89065f
  - 0x008906eb: je -> 0x008906f7 (jcc_true) | ctx: 0x008906df: mov eax, dword ptr [ebp + 0x10] ; 0x008906e2: mov dword ptr [ebp - 0x54], 0xffffffff ; 0x008906e9: cmp ecx, eax ; 0x008906eb: je 0x8906f7
  - 0x008906eb: je -> 0x008906ed (jcc_false) | ctx: 0x008906df: mov eax, dword ptr [ebp + 0x10] ; 0x008906e2: mov dword ptr [ebp - 0x54], 0xffffffff ; 0x008906e9: cmp ecx, eax ; 0x008906eb: je 0x8906f7
  - 0x00890672: jne -> 0x00890697 (jcc_true) | ctx: 0x00890670: cmp eax, edx ; 0x00890672: jne 0x890697
  - 0x00890672: jne -> 0x00890674 (jcc_false) | ctx: 0x00890670: cmp eax, edx ; 0x00890672: jne 0x890697
  - 0x00890663: je -> 0x00890651 (jcc_true) | ctx: 0x0089065f: cmp byte ptr [esi + 0xd], 0 ; 0x00890663: je 0x890651
  - 0x00890663: je -> 0x00890665 (jcc_false) | ctx: 0x0089065f: cmp byte ptr [esi + 0xd], 0 ; 0x00890663: je 0x890651
  - 0x00890727: jb -> 0x00890734 (jcc_true) | ctx: 0x00890715: mov dword ptr [esi + 4], 0 ; 0x0089071c: cmp dword ptr [ebp - 0x20], 0x10 ; 0x00890720: mov dword ptr [ebp - 4], 1 ; 0x00890727: jb 0x890734
  - 0x00890727: jb -> 0x00890729 (jcc_false) | ctx: 0x00890715: mov dword ptr [esi + 4], 0 ; 0x0089071c: cmp dword ptr [ebp - 0x20], 0x10 ; 0x00890720: mov dword ptr [ebp - 4], 1 ; 0x00890727: jb 0x890734
  - 0x00890727: jb -> 0x00890734 (jcc_true) | ctx: 0x00890715: mov dword ptr [esi + 4], 0 ; 0x0089071c: cmp dword ptr [ebp - 0x20], 0x10 ; 0x00890720: mov dword ptr [ebp - 4], 1 ; 0x00890727: jb 0x890734
  - 0x00890727: jb -> 0x00890729 (jcc_false) | ctx: 0x00890715: mov dword ptr [esi + 4], 0 ; 0x0089071c: cmp dword ptr [ebp - 0x20], 0x10 ; 0x00890720: mov dword ptr [ebp - 4], 1 ; 0x00890727: jb 0x890734

### 0x00890750
- blocks=18, insns=156, edges=37, jcc=16, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00890812)
- branch points:
  - 0x00890779: je -> 0x0089089e (jcc_true) | ctx: 0x00890771: mov dword ptr [ebp - 0x10], ecx ; 0x00890774: mov esi, dword ptr [esi] ; 0x00890776: cmp esi, dword ptr [ecx + 4] ; 0x00890779: je 0x89089e
  - 0x00890779: je -> 0x0089077f (jcc_false) | ctx: 0x00890771: mov dword ptr [ebp - 0x10], ecx ; 0x00890774: mov esi, dword ptr [esi] ; 0x00890776: cmp esi, dword ptr [ecx + 4] ; 0x00890779: je 0x89089e
  - 0x0089080b: je -> 0x00890817 (jcc_true) | ctx: 0x00890803: mov dword ptr [ebp - 0x50], edi ; 0x00890806: mov dword ptr [ebp - 0x4c], edx ; 0x00890809: cmp ecx, eax ; 0x0089080b: je 0x890817
  - 0x0089080b: je -> 0x0089080d (jcc_false) | ctx: 0x00890803: mov dword ptr [ebp - 0x50], edi ; 0x00890806: mov dword ptr [ebp - 0x4c], edx ; 0x00890809: cmp ecx, eax ; 0x0089080b: je 0x890817
  - 0x00890837: jb -> 0x00890844 (jcc_true) | ctx: 0x00890827: call 0x9343a0 ; 0x0089082c: cmp dword ptr [ebp - 0x24], 0x10 ; 0x00890830: mov dword ptr [ebp - 4], 2 ; 0x00890837: jb 0x890844
  - 0x00890837: jb -> 0x00890839 (jcc_false) | ctx: 0x00890827: call 0x9343a0 ; 0x0089082c: cmp dword ptr [ebp - 0x24], 0x10 ; 0x00890830: mov dword ptr [ebp - 4], 2 ; 0x00890837: jb 0x890844
  - 0x00890837: jb -> 0x00890844 (jcc_true) | ctx: 0x00890827: call 0x9343a0 ; 0x0089082c: cmp dword ptr [ebp - 0x24], 0x10 ; 0x00890830: mov dword ptr [ebp - 4], 2 ; 0x00890837: jb 0x890844
  - 0x00890837: jb -> 0x00890839 (jcc_false) | ctx: 0x00890827: call 0x9343a0 ; 0x0089082c: cmp dword ptr [ebp - 0x24], 0x10 ; 0x00890830: mov dword ptr [ebp - 4], 2 ; 0x00890837: jb 0x890844
  - 0x0089084f: jne -> 0x00890892 (jcc_true) | ctx: 0x00890844: cmp byte ptr [esi + 0xd], 0 ; 0x00890848: mov dword ptr [ebp - 4], 0xffffffff ; 0x0089084f: jne 0x890892
  - 0x0089084f: jne -> 0x00890851 (jcc_false) | ctx: 0x00890844: cmp byte ptr [esi + 0xd], 0 ; 0x00890848: mov dword ptr [ebp - 4], 0xffffffff ; 0x0089084f: jne 0x890892
  - 0x0089084f: jne -> 0x00890892 (jcc_true) | ctx: 0x00890841: add esp, 4 ; 0x00890844: cmp byte ptr [esi + 0xd], 0 ; 0x00890848: mov dword ptr [ebp - 4], 0xffffffff ; 0x0089084f: jne 0x890892
  - 0x0089084f: jne -> 0x00890851 (jcc_false) | ctx: 0x00890841: add esp, 4 ; 0x00890844: cmp byte ptr [esi + 0xd], 0 ; 0x00890848: mov dword ptr [ebp - 4], 0xffffffff ; 0x0089084f: jne 0x890892
  - 0x00890898: jne -> 0x00890780 (jcc_true) | ctx: 0x00890892: mov ecx, dword ptr [ebp - 0x10] ; 0x00890895: cmp esi, dword ptr [ecx + 4] ; 0x00890898: jne 0x890780
  - 0x00890898: jne -> 0x0089089e (jcc_false) | ctx: 0x00890892: mov ecx, dword ptr [ebp - 0x10] ; 0x00890895: cmp esi, dword ptr [ecx + 4] ; 0x00890898: jne 0x890780
  - 0x00890858: jne -> 0x00890870 (jcc_true) | ctx: 0x00890851: mov eax, dword ptr [esi + 8] ; 0x00890854: cmp byte ptr [eax + 0xd], 0 ; 0x00890858: jne 0x890870
  - 0x00890858: jne -> 0x0089085a (jcc_false) | ctx: 0x00890851: mov eax, dword ptr [esi + 8] ; 0x00890854: cmp byte ptr [eax + 0xd], 0 ; 0x00890858: jne 0x890870
  - 0x0089080b: je -> 0x00890817 (jcc_true) | ctx: 0x00890803: mov dword ptr [ebp - 0x50], edi ; 0x00890806: mov dword ptr [ebp - 0x4c], edx ; 0x00890809: cmp ecx, eax ; 0x0089080b: je 0x890817
  - 0x0089080b: je -> 0x0089080d (jcc_false) | ctx: 0x00890803: mov dword ptr [ebp - 0x50], edi ; 0x00890806: mov dword ptr [ebp - 0x4c], edx ; 0x00890809: cmp ecx, eax ; 0x0089080b: je 0x890817
  - 0x00890877: jne -> 0x00890890 (jcc_true) | ctx: 0x00890870: mov eax, dword ptr [esi + 4] ; 0x00890873: cmp byte ptr [eax + 0xd], 0 ; 0x00890877: jne 0x890890
  - 0x00890877: jne -> 0x00890879 (jcc_false) | ctx: 0x00890870: mov eax, dword ptr [esi + 4] ; 0x00890873: cmp byte ptr [eax + 0xd], 0 ; 0x00890877: jne 0x890890
  - 0x00890862: jne -> 0x00890892 (jcc_true) | ctx: 0x0089085a: mov esi, eax ; 0x0089085c: mov eax, dword ptr [esi] ; 0x0089085e: cmp byte ptr [eax + 0xd], 0 ; 0x00890862: jne 0x890892
  - 0x00890862: jne -> 0x00890864 (jcc_false) | ctx: 0x0089085a: mov esi, eax ; 0x0089085c: mov eax, dword ptr [esi] ; 0x0089085e: cmp byte ptr [eax + 0xd], 0 ; 0x00890862: jne 0x890892
  - 0x00890898: jne -> 0x00890780 (jcc_true) | ctx: 0x00890890: mov esi, eax ; 0x00890892: mov ecx, dword ptr [ebp - 0x10] ; 0x00890895: cmp esi, dword ptr [ecx + 4] ; 0x00890898: jne 0x890780
  - 0x00890898: jne -> 0x0089089e (jcc_false) | ctx: 0x00890890: mov esi, eax ; 0x00890892: mov ecx, dword ptr [ebp - 0x10] ; 0x00890895: cmp esi, dword ptr [ecx + 4] ; 0x00890898: jne 0x890780
  - 0x00890883: jne -> 0x00890890 (jcc_true) | ctx: 0x00890879: nop dword ptr [eax] ; 0x00890880: cmp esi, dword ptr [eax + 8] ; 0x00890883: jne 0x890890
  - 0x00890883: jne -> 0x00890885 (jcc_false) | ctx: 0x00890879: nop dword ptr [eax] ; 0x00890880: cmp esi, dword ptr [eax + 8] ; 0x00890883: jne 0x890890
  - 0x0089086c: je -> 0x00890864 (jcc_true) | ctx: 0x00890864: mov esi, eax ; 0x00890866: mov eax, dword ptr [esi] ; 0x00890868: cmp byte ptr [eax + 0xd], 0 ; 0x0089086c: je 0x890864
  - 0x0089086c: je -> 0x0089086e (jcc_false) | ctx: 0x00890864: mov esi, eax ; 0x00890866: mov eax, dword ptr [esi] ; 0x00890868: cmp byte ptr [eax + 0xd], 0 ; 0x0089086c: je 0x890864
  - 0x0089088e: je -> 0x00890880 (jcc_true) | ctx: 0x00890885: mov esi, eax ; 0x00890887: mov eax, dword ptr [eax + 4] ; 0x0089088a: cmp byte ptr [eax + 0xd], 0 ; 0x0089088e: je 0x890880
  - 0x0089088e: je -> 0x00890890 (jcc_false) | ctx: 0x00890885: mov esi, eax ; 0x00890887: mov eax, dword ptr [eax + 4] ; 0x0089088a: cmp byte ptr [eax + 0xd], 0 ; 0x0089088e: je 0x890880
  - 0x0089086e: jmp -> 0x00890892 (jmp) | ctx: 0x0089086e: jmp 0x890892
  - 0x00890883: jne -> 0x00890890 (jcc_true) | ctx: 0x00890880: cmp esi, dword ptr [eax + 8] ; 0x00890883: jne 0x890890
  - 0x00890883: jne -> 0x00890885 (jcc_false) | ctx: 0x00890880: cmp esi, dword ptr [eax + 8] ; 0x00890883: jne 0x890890

### 0x008908ec
- blocks=20, insns=166, edges=44, jcc=16, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00890986)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x008909ed)
- branch points:
  - 0x00890910: je -> 0x00890950 (jcc_true) | ctx: 0x00890908: mov eax, dword ptr [ebp - 0x14] ; 0x0089090b: mov edi, dword ptr [ebp + 0xc] ; 0x0089090e: cmp eax, dword ptr [ebx] ; 0x00890910: je 0x890950
  - 0x00890910: je -> 0x00890912 (jcc_false) | ctx: 0x00890908: mov eax, dword ptr [ebp - 0x14] ; 0x0089090b: mov edi, dword ptr [ebp + 0xc] ; 0x0089090e: cmp eax, dword ptr [ebx] ; 0x00890910: je 0x890950
  - 0x0089095a: je -> 0x00890975 (jcc_true) | ctx: 0x00890950: mov eax, dword ptr [esi + 0x178] ; 0x00890956: xor bl, bl ; 0x00890958: test eax, eax ; 0x0089095a: je 0x890975
  - 0x0089095a: je -> 0x0089095c (jcc_false) | ctx: 0x00890950: mov eax, dword ptr [esi + 0x178] ; 0x00890956: xor bl, bl ; 0x00890958: test eax, eax ; 0x0089095a: je 0x890975
  - 0x00890934: je -> 0x00890950 (jcc_true) | ctx: 0x00890929: shr bl, 3 ; 0x0089092c: call 0x8c9100 ; 0x00890931: and bl, 1 ; 0x00890934: je 0x890950
  - 0x00890934: je -> 0x00890936 (jcc_false) | ctx: 0x00890929: shr bl, 3 ; 0x0089092c: call 0x8c9100 ; 0x00890931: and bl, 1 ; 0x00890934: je 0x890950
  - 0x0089097f: je -> 0x0089098b (jcc_true) | ctx: 0x00890975: mov bl, 1 ; 0x00890977: lea ecx, [esi + 0x80] ; 0x0089097d: cmp ecx, edi ; 0x0089097f: je 0x89098b
  - 0x0089097f: je -> 0x00890981 (jcc_false) | ctx: 0x00890975: mov bl, 1 ; 0x00890977: lea ecx, [esi + 0x80] ; 0x0089097d: cmp ecx, edi ; 0x0089097f: je 0x89098b
  - 0x0089095f: jne -> 0x00890977 (jcc_true) | ctx: 0x0089095c: cmp eax, 1 ; 0x0089095f: jne 0x890977
  - 0x0089095f: jne -> 0x00890961 (jcc_false) | ctx: 0x0089095c: cmp eax, 1 ; 0x0089095f: jne 0x890977
  - 0x0089095a: je -> 0x00890975 (jcc_true) | ctx: 0x00890950: mov eax, dword ptr [esi + 0x178] ; 0x00890956: xor bl, bl ; 0x00890958: test eax, eax ; 0x0089095a: je 0x890975
  - 0x0089095a: je -> 0x0089095c (jcc_false) | ctx: 0x00890950: mov eax, dword ptr [esi + 0x178] ; 0x00890956: xor bl, bl ; 0x00890958: test eax, eax ; 0x0089095a: je 0x890975
  - 0x00890998: je -> 0x00890a39 (jcc_true) | ctx: 0x0089098e: mov eax, dword ptr [eax] ; 0x00890990: mov dword ptr [esi + 0x98], eax ; 0x00890996: test bl, bl ; 0x00890998: je 0x890a39
  - 0x00890998: je -> 0x0089099e (jcc_false) | ctx: 0x0089098e: mov eax, dword ptr [eax] ; 0x00890990: mov dword ptr [esi + 0x98], eax ; 0x00890996: test bl, bl ; 0x00890998: je 0x890a39
  - 0x00890998: je -> 0x00890a39 (jcc_true) | ctx: 0x0089098e: mov eax, dword ptr [eax] ; 0x00890990: mov dword ptr [esi + 0x98], eax ; 0x00890996: test bl, bl ; 0x00890998: je 0x890a39
  - 0x00890998: je -> 0x0089099e (jcc_false) | ctx: 0x0089098e: mov eax, dword ptr [eax] ; 0x00890990: mov dword ptr [esi + 0x98], eax ; 0x00890996: test bl, bl ; 0x00890998: je 0x890a39
  - 0x0089097f: je -> 0x0089098b (jcc_true) | ctx: 0x00890977: lea ecx, [esi + 0x80] ; 0x0089097d: cmp ecx, edi ; 0x0089097f: je 0x89098b
  - 0x0089097f: je -> 0x00890981 (jcc_false) | ctx: 0x00890977: lea ecx, [esi + 0x80] ; 0x0089097d: cmp ecx, edi ; 0x0089097f: je 0x89098b
  - 0x0089096d: jne -> 0x00890977 (jcc_true) | ctx: 0x00890961: mov eax, dword ptr [esi + 0x174] ; 0x00890967: mov eax, dword ptr [eax] ; 0x00890969: cmp dword ptr [eax + 0x10], 0x75 ; 0x0089096d: jne 0x890977
  - 0x0089096d: jne -> 0x0089096f (jcc_false) | ctx: 0x00890961: mov eax, dword ptr [esi + 0x174] ; 0x00890967: mov eax, dword ptr [eax] ; 0x00890969: cmp dword ptr [eax + 0x10], 0x75 ; 0x0089096d: jne 0x890977
  - 0x00890a40: je -> 0x00890a5d (jcc_true) | ctx: 0x00890a39: mov ebx, dword ptr [ebp + 8] ; 0x00890a3c: cmp byte ptr [ebp - 0xd], 0 ; 0x00890a40: je 0x890a5d
  - 0x00890a40: je -> 0x00890a42 (jcc_false) | ctx: 0x00890a39: mov ebx, dword ptr [ebp + 8] ; 0x00890a3c: cmp byte ptr [ebp - 0xd], 0 ; 0x00890a40: je 0x890a5d
  - 0x008909e4: je -> 0x008909f2 (jcc_true) | ctx: 0x008909d8: lea eax, [ebp - 0x48] ; 0x008909db: mov dword ptr [ebp - 0x68], 0xffffffff ; 0x008909e2: cmp eax, edi ; 0x008909e4: je 0x8909f2
  - 0x008909e4: je -> 0x008909e6 (jcc_false) | ctx: 0x008909d8: lea eax, [ebp - 0x48] ; 0x008909db: mov dword ptr [ebp - 0x68], 0xffffffff ; 0x008909e2: cmp eax, edi ; 0x008909e4: je 0x8909f2
  - 0x00890973: jne -> 0x00890977 (jcc_true) | ctx: 0x0089096f: cmp dword ptr [eax + 0x14], 0 ; 0x00890973: jne 0x890977
  - 0x00890973: jne -> 0x00890975 (jcc_false) | ctx: 0x0089096f: cmp dword ptr [eax + 0x14], 0 ; 0x00890973: jne 0x890977
  - 0x00890a23: jb -> 0x00890a30 (jcc_true) | ctx: 0x00890a13: call 0x9343a0 ; 0x00890a18: cmp dword ptr [ebp - 0x34], 0x10 ; 0x00890a1c: mov dword ptr [ebp - 4], 1 ; 0x00890a23: jb 0x890a30
  - 0x00890a23: jb -> 0x00890a25 (jcc_false) | ctx: 0x00890a13: call 0x9343a0 ; 0x00890a18: cmp dword ptr [ebp - 0x34], 0x10 ; 0x00890a1c: mov dword ptr [ebp - 4], 1 ; 0x00890a23: jb 0x890a30
  - 0x00890a23: jb -> 0x00890a30 (jcc_true) | ctx: 0x00890a13: call 0x9343a0 ; 0x00890a18: cmp dword ptr [ebp - 0x34], 0x10 ; 0x00890a1c: mov dword ptr [ebp - 4], 1 ; 0x00890a23: jb 0x890a30
  - 0x00890a23: jb -> 0x00890a25 (jcc_false) | ctx: 0x00890a13: call 0x9343a0 ; 0x00890a18: cmp dword ptr [ebp - 0x34], 0x10 ; 0x00890a1c: mov dword ptr [ebp - 4], 1 ; 0x00890a23: jb 0x890a30
  - 0x00890a37: jmp -> 0x00890a3c (jmp) | ctx: 0x00890a30: mov dword ptr [ebp - 4], 0xffffffff ; 0x00890a37: jmp 0x890a3c
  - 0x00890a37: jmp -> 0x00890a3c (jmp) | ctx: 0x00890a28: call 0x9afbf0 ; 0x00890a2d: add esp, 4 ; 0x00890a30: mov dword ptr [ebp - 4], 0xffffffff ; 0x00890a37: jmp 0x890a3c
  - 0x00890a40: je -> 0x00890a5d (jcc_true) | ctx: 0x00890a3c: cmp byte ptr [ebp - 0xd], 0 ; 0x00890a40: je 0x890a5d
  - 0x00890a40: je -> 0x00890a42 (jcc_false) | ctx: 0x00890a3c: cmp byte ptr [ebp - 0xd], 0 ; 0x00890a40: je 0x890a5d

### 0x00893fa0
- blocks=3, insns=58, edges=4, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00894000)
- branch points:
  - 0x00893ff9: je -> 0x00894005 (jcc_true) | ctx: 0x00893ff1: mov dword ptr [edi + 0x3c], eax ; 0x00893ff4: mov eax, dword ptr [ebp + 0x20] ; 0x00893ff7: cmp ecx, eax ; 0x00893ff9: je 0x894005
  - 0x00893ff9: je -> 0x00893ffb (jcc_false) | ctx: 0x00893ff1: mov dword ptr [edi + 0x3c], eax ; 0x00893ff4: mov eax, dword ptr [ebp + 0x20] ; 0x00893ff7: cmp ecx, eax ; 0x00893ff9: je 0x894005

### 0x00894120
- blocks=3, insns=43, edges=6, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00894156)
- branch points:
  - 0x0089414f: je -> 0x0089415b (jcc_true) | ctx: 0x00894147: mov dword ptr [esi + 0x30], eax ; 0x0089414a: mov eax, dword ptr [ebp + 0x20] ; 0x0089414d: cmp ecx, eax ; 0x0089414f: je 0x89415b
  - 0x0089414f: je -> 0x00894151 (jcc_false) | ctx: 0x00894147: mov dword ptr [esi + 0x30], eax ; 0x0089414a: mov eax, dword ptr [ebp + 0x20] ; 0x0089414d: cmp ecx, eax ; 0x0089414f: je 0x89415b

### 0x00894213
- blocks=3, insns=30, edges=3, jcc=1, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0089423d)
- branch points:
  - 0x00894236: je -> 0x00894242 (jcc_true) | ctx: 0x0089422d: mov word ptr [edi + 0x20], ax ; 0x00894231: mov eax, dword ptr [ebp + 0x10] ; 0x00894234: cmp ecx, eax ; 0x00894236: je 0x894242
  - 0x00894236: je -> 0x00894238 (jcc_false) | ctx: 0x0089422d: mov word ptr [edi + 0x20], ax ; 0x00894231: mov eax, dword ptr [ebp + 0x10] ; 0x00894234: cmp ecx, eax ; 0x00894236: je 0x894242

### 0x00894396
- blocks=15, insns=111, edges=30, jcc=10, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00894419)
- branch points:
  - 0x008943a0: jne -> 0x00894481 (jcc_true) | ctx: 0x00894396: push esi ; 0x00894397: mov esi, ecx ; 0x00894399: cmp dword ptr [esi + 0x838], 0 ; 0x008943a0: jne 0x894481
  - 0x008943a0: jne -> 0x008943a6 (jcc_false) | ctx: 0x00894396: push esi ; 0x00894397: mov esi, ecx ; 0x00894399: cmp dword ptr [esi + 0x838], 0 ; 0x008943a0: jne 0x894481
  - 0x008943b5: jne -> 0x008943ca (jcc_true) | ctx: 0x008943ab: mov ecx, eax ; 0x008943ad: mov dword ptr [esi + 0x838], ecx ; 0x008943b3: test ecx, ecx ; 0x008943b5: jne 0x8943ca
  - 0x008943b5: jne -> 0x008943b7 (jcc_false) | ctx: 0x008943ab: mov ecx, eax ; 0x008943ad: mov dword ptr [esi + 0x838], ecx ; 0x008943b3: test ecx, ecx ; 0x008943b5: jne 0x8943ca
  - 0x008943e7: js -> 0x0089449e (jcc_true) | ctx: 0x008943da: call 0x61d7f0 ; 0x008943df: mov ecx, dword ptr [esi + 0x838] ; 0x008943e5: test eax, eax ; 0x008943e7: js 0x89449e
  - 0x008943e7: js -> 0x008943ed (jcc_false) | ctx: 0x008943da: call 0x61d7f0 ; 0x008943df: mov ecx, dword ptr [esi + 0x838] ; 0x008943e5: test eax, eax ; 0x008943e7: js 0x89449e
  - 0x008943f4: je -> 0x00894498 (jcc_true) | ctx: 0x008943ed: call 0x8e4360 ; 0x008943f2: test al, al ; 0x008943f4: je 0x894498
  - 0x008943f4: je -> 0x008943fa (jcc_false) | ctx: 0x008943ed: call 0x8e4360 ; 0x008943f2: test al, al ; 0x008943f4: je 0x894498
  - 0x00894404: je -> 0x00894498 (jcc_true) | ctx: 0x008943fa: mov eax, dword ptr [esi + 0x838] ; 0x00894400: cmp dword ptr [eax + 0x4c], 0 ; 0x00894404: je 0x894498
  - 0x00894404: je -> 0x0089440a (jcc_false) | ctx: 0x008943fa: mov eax, dword ptr [esi + 0x838] ; 0x00894400: cmp dword ptr [eax + 0x4c], 0 ; 0x00894404: je 0x894498
  - 0x00894412: je -> 0x0089441e (jcc_true) | ctx: 0x0089440a: add eax, 0x3c ; 0x0089440d: lea ecx, [esi + 0x28] ; 0x00894410: cmp ecx, eax ; 0x00894412: je 0x89441e
  - 0x00894412: je -> 0x00894414 (jcc_false) | ctx: 0x0089440a: add eax, 0x3c ; 0x0089440d: lea ecx, [esi + 0x28] ; 0x00894410: cmp ecx, eax ; 0x00894412: je 0x89441e
  - 0x0089442c: je -> 0x00894438 (jcc_true) | ctx: 0x00894424: lea ecx, [esi + 0x40] ; 0x00894427: add eax, 0x54 ; 0x0089442a: cmp ecx, eax ; 0x0089442c: je 0x894438
  - 0x0089442c: je -> 0x0089442e (jcc_false) | ctx: 0x00894424: lea ecx, [esi + 0x40] ; 0x00894427: add eax, 0x54 ; 0x0089442a: cmp ecx, eax ; 0x0089442c: je 0x894438
  - 0x0089442c: je -> 0x00894438 (jcc_true) | ctx: 0x00894424: lea ecx, [esi + 0x40] ; 0x00894427: add eax, 0x54 ; 0x0089442a: cmp ecx, eax ; 0x0089442c: je 0x894438
  - 0x0089442c: je -> 0x0089442e (jcc_false) | ctx: 0x00894424: lea ecx, [esi + 0x40] ; 0x00894427: add eax, 0x54 ; 0x0089442a: cmp ecx, eax ; 0x0089442c: je 0x894438
  - 0x0089443f: je -> 0x00894481 (jcc_true) | ctx: 0x00894438: cmp dword ptr [esi + 0x864], 0 ; 0x0089443f: je 0x894481
  - 0x0089443f: je -> 0x00894441 (jcc_false) | ctx: 0x00894438: cmp dword ptr [esi + 0x864], 0 ; 0x0089443f: je 0x894481
  - 0x0089443f: je -> 0x00894481 (jcc_true) | ctx: 0x00894432: push eax ; 0x00894433: call 0x826ef0 ; 0x00894438: cmp dword ptr [esi + 0x864], 0 ; 0x0089443f: je 0x894481
  - 0x0089443f: je -> 0x00894441 (jcc_false) | ctx: 0x00894432: push eax ; 0x00894433: call 0x826ef0 ; 0x00894438: cmp dword ptr [esi + 0x864], 0 ; 0x0089443f: je 0x894481

### 0x0089530b
- blocks=6, insns=60, edges=13, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00895368)
- branch points:
  - 0x00895353: jb -> 0x00895359 (jcc_true) | ctx: 0x00895341: mov dword ptr [esi + 0x14], 0xf ; 0x00895348: mov dword ptr [esi + 0x10], 0 ; 0x0089534f: cmp dword ptr [esi + 0x14], 0x10 ; 0x00895353: jb 0x895359
  - 0x00895353: jb -> 0x00895355 (jcc_false) | ctx: 0x00895341: mov dword ptr [esi + 0x14], 0xf ; 0x00895348: mov dword ptr [esi + 0x10], 0 ; 0x0089534f: cmp dword ptr [esi + 0x14], 0x10 ; 0x00895353: jb 0x895359
  - 0x00895378: jb -> 0x00895385 (jcc_true) | ctx: 0x00895368: call 0x5c5420 ; 0x0089536d: cmp dword ptr [ebp - 0x18], 0x10 ; 0x00895371: mov dword ptr [ebp - 4], 1 ; 0x00895378: jb 0x895385
  - 0x00895378: jb -> 0x0089537a (jcc_false) | ctx: 0x00895368: call 0x5c5420 ; 0x0089536d: cmp dword ptr [ebp - 0x18], 0x10 ; 0x00895371: mov dword ptr [ebp - 4], 1 ; 0x00895378: jb 0x895385
  - 0x00895357: jmp -> 0x0089535b (jmp) | ctx: 0x00895355: mov eax, dword ptr [esi] ; 0x00895357: jmp 0x89535b
  - 0x00895378: jb -> 0x00895385 (jcc_true) | ctx: 0x00895368: call 0x5c5420 ; 0x0089536d: cmp dword ptr [ebp - 0x18], 0x10 ; 0x00895371: mov dword ptr [ebp - 4], 1 ; 0x00895378: jb 0x895385
  - 0x00895378: jb -> 0x0089537a (jcc_false) | ctx: 0x00895368: call 0x5c5420 ; 0x0089536d: cmp dword ptr [ebp - 0x18], 0x10 ; 0x00895371: mov dword ptr [ebp - 4], 1 ; 0x00895378: jb 0x895385

### 0x00896d80
- blocks=17, insns=273, edges=53, jcc=14, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00896fbd)
- branch points:
  - 0x00896db7: je -> 0x00896ed9 (jcc_true) | ctx: 0x00896da6: cmp dword ptr [esi + 0x4c], 0 ; 0x00896daa: mov dword ptr [edi], 1 ; 0x00896db0: mov dword ptr [edi + 4], 0 ; 0x00896db7: je 0x896ed9
  - 0x00896db7: je -> 0x00896dbd (jcc_false) | ctx: 0x00896da6: cmp dword ptr [esi + 0x4c], 0 ; 0x00896daa: mov dword ptr [edi], 1 ; 0x00896db0: mov dword ptr [edi + 4], 0 ; 0x00896db7: je 0x896ed9
  - 0x00896ee5: je -> 0x00897027 (jcc_true) | ctx: 0x00896ed9: mov eax, dword ptr [esi + 0x10c] ; 0x00896edf: cmp eax, dword ptr [esi + 0x110] ; 0x00896ee5: je 0x897027
  - 0x00896ee5: je -> 0x00896eeb (jcc_false) | ctx: 0x00896ed9: mov eax, dword ptr [esi + 0x10c] ; 0x00896edf: cmp eax, dword ptr [esi + 0x110] ; 0x00896ee5: je 0x897027
  - 0x00896dfd: jne -> 0x00896e0c (jcc_true) | ctx: 0x00896df3: mov eax, dword ptr [ebp - 0x14] ; 0x00896df6: mov byte ptr [ebp - 4], 1 ; 0x00896dfa: cmp eax, dword ptr [ebp - 0x10] ; 0x00896dfd: jne 0x896e0c
  - 0x00896dfd: jne -> 0x00896dff (jcc_false) | ctx: 0x00896df3: mov eax, dword ptr [ebp - 0x14] ; 0x00896df6: mov byte ptr [ebp - 4], 1 ; 0x00896dfa: cmp eax, dword ptr [ebp - 0x10] ; 0x00896dfd: jne 0x896e0c
  - 0x00896fb4: je -> 0x00896fc2 (jcc_true) | ctx: 0x00896faa: call 0x7d81a0 ; 0x00896faf: lea eax, [ebp - 0x50] ; 0x00896fb2: cmp eax, ebx ; 0x00896fb4: je 0x896fc2
  - 0x00896fb4: je -> 0x00896fb6 (jcc_false) | ctx: 0x00896faa: call 0x7d81a0 ; 0x00896faf: lea eax, [ebp - 0x50] ; 0x00896fb2: cmp eax, ebx ; 0x00896fb4: je 0x896fc2
  - 0x00896e2e: jb -> 0x00896e3e (jcc_true) | ctx: 0x00896e23: mov dword ptr [ebp - 0x14], eax ; 0x00896e26: cmp dword ptr [ebp - 0x1c], 0x10 ; 0x00896e2a: mov byte ptr [ebp - 4], 2 ; 0x00896e2e: jb 0x896e3e
  - 0x00896e2e: jb -> 0x00896e30 (jcc_false) | ctx: 0x00896e23: mov dword ptr [ebp - 0x14], eax ; 0x00896e26: cmp dword ptr [ebp - 0x1c], 0x10 ; 0x00896e2a: mov byte ptr [ebp - 4], 2 ; 0x00896e2e: jb 0x896e3e
  - 0x00896e2e: jb -> 0x00896e3e (jcc_true) | ctx: 0x00896e23: mov dword ptr [ebp - 0x14], eax ; 0x00896e26: cmp dword ptr [ebp - 0x1c], 0x10 ; 0x00896e2a: mov byte ptr [ebp - 4], 2 ; 0x00896e2e: jb 0x896e3e
  - 0x00896e2e: jb -> 0x00896e30 (jcc_false) | ctx: 0x00896e23: mov dword ptr [ebp - 0x14], eax ; 0x00896e26: cmp dword ptr [ebp - 0x1c], 0x10 ; 0x00896e2a: mov byte ptr [ebp - 4], 2 ; 0x00896e2e: jb 0x896e3e
  - 0x00896ff6: jb -> 0x00897003 (jcc_true) | ctx: 0x00896fe1: mov dword ptr [ebp - 0x88], 0xc1ce54 ; 0x00896feb: cmp dword ptr [ebp - 0x3c], 0x10 ; 0x00896fef: mov dword ptr [ebp - 4], 8 ; 0x00896ff6: jb 0x897003
  - 0x00896ff6: jb -> 0x00896ff8 (jcc_false) | ctx: 0x00896fe1: mov dword ptr [ebp - 0x88], 0xc1ce54 ; 0x00896feb: cmp dword ptr [ebp - 0x3c], 0x10 ; 0x00896fef: mov dword ptr [ebp - 4], 8 ; 0x00896ff6: jb 0x897003
  - 0x00896ff6: jb -> 0x00897003 (jcc_true) | ctx: 0x00896fe1: mov dword ptr [ebp - 0x88], 0xc1ce54 ; 0x00896feb: cmp dword ptr [ebp - 0x3c], 0x10 ; 0x00896fef: mov dword ptr [ebp - 4], 8 ; 0x00896ff6: jb 0x897003
  - 0x00896ff6: jb -> 0x00896ff8 (jcc_false) | ctx: 0x00896fe1: mov dword ptr [ebp - 0x88], 0xc1ce54 ; 0x00896feb: cmp dword ptr [ebp - 0x3c], 0x10 ; 0x00896fef: mov dword ptr [ebp - 4], 8 ; 0x00896ff6: jb 0x897003
  - 0x00896e45: jne -> 0x00896e54 (jcc_true) | ctx: 0x00896e3e: mov byte ptr [ebp - 4], 0 ; 0x00896e42: cmp eax, dword ptr [ebp - 0x10] ; 0x00896e45: jne 0x896e54
  - 0x00896e45: jne -> 0x00896e47 (jcc_false) | ctx: 0x00896e3e: mov byte ptr [ebp - 4], 0 ; 0x00896e42: cmp eax, dword ptr [ebp - 0x10] ; 0x00896e45: jne 0x896e54
  - 0x00896e45: jne -> 0x00896e54 (jcc_true) | ctx: 0x00896e3b: add esp, 4 ; 0x00896e3e: mov byte ptr [ebp - 4], 0 ; 0x00896e42: cmp eax, dword ptr [ebp - 0x10] ; 0x00896e45: jne 0x896e54
  - 0x00896e45: jne -> 0x00896e47 (jcc_false) | ctx: 0x00896e3b: add esp, 4 ; 0x00896e3e: mov byte ptr [ebp - 4], 0 ; 0x00896e42: cmp eax, dword ptr [ebp - 0x10] ; 0x00896e45: jne 0x896e54
  - 0x00896ebd: jb -> 0x00896eca (jcc_true) | ctx: 0x00896eb0: call 0x965c60 ; 0x00896eb5: cmp dword ptr [ebp - 0x1c], 0x10 ; 0x00896eb9: mov byte ptr [ebp - 4], 4 ; 0x00896ebd: jb 0x896eca
  - 0x00896ebd: jb -> 0x00896ebf (jcc_false) | ctx: 0x00896eb0: call 0x965c60 ; 0x00896eb5: cmp dword ptr [ebp - 0x1c], 0x10 ; 0x00896eb9: mov byte ptr [ebp - 4], 4 ; 0x00896ebd: jb 0x896eca
  - 0x00896ebd: jb -> 0x00896eca (jcc_true) | ctx: 0x00896eb0: call 0x965c60 ; 0x00896eb5: cmp dword ptr [ebp - 0x1c], 0x10 ; 0x00896eb9: mov byte ptr [ebp - 4], 4 ; 0x00896ebd: jb 0x896eca
  - 0x00896ebd: jb -> 0x00896ebf (jcc_false) | ctx: 0x00896eb0: call 0x965c60 ; 0x00896eb5: cmp dword ptr [ebp - 0x1c], 0x10 ; 0x00896eb9: mov byte ptr [ebp - 4], 4 ; 0x00896ebd: jb 0x896eca
  - 0x00896ee5: je -> 0x00897027 (jcc_true) | ctx: 0x00896ed4: call 0x8835f0 ; 0x00896ed9: mov eax, dword ptr [esi + 0x10c] ; 0x00896edf: cmp eax, dword ptr [esi + 0x110] ; 0x00896ee5: je 0x897027
  - 0x00896ee5: je -> 0x00896eeb (jcc_false) | ctx: 0x00896ed4: call 0x8835f0 ; 0x00896ed9: mov eax, dword ptr [esi + 0x10c] ; 0x00896edf: cmp eax, dword ptr [esi + 0x110] ; 0x00896ee5: je 0x897027
  - 0x00896ee5: je -> 0x00897027 (jcc_true) | ctx: 0x00896ed4: call 0x8835f0 ; 0x00896ed9: mov eax, dword ptr [esi + 0x10c] ; 0x00896edf: cmp eax, dword ptr [esi + 0x110] ; 0x00896ee5: je 0x897027
  - 0x00896ee5: je -> 0x00896eeb (jcc_false) | ctx: 0x00896ed4: call 0x8835f0 ; 0x00896ed9: mov eax, dword ptr [esi + 0x10c] ; 0x00896edf: cmp eax, dword ptr [esi + 0x110] ; 0x00896ee5: je 0x897027

### 0x0089746f
- blocks=7, insns=110, edges=16, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00897506)
- branch points:
  - 0x0089748b: je -> 0x00897567 (jcc_true) | ctx: 0x00897478: mov dword ptr [esi + 4], 0 ; 0x0089747f: mov eax, dword ptr [edi + 0x10c] ; 0x00897485: cmp eax, dword ptr [edi + 0x110] ; 0x0089748b: je 0x897567
  - 0x0089748b: je -> 0x00897491 (jcc_false) | ctx: 0x00897478: mov dword ptr [esi + 4], 0 ; 0x0089747f: mov eax, dword ptr [edi + 0x10c] ; 0x00897485: cmp eax, dword ptr [edi + 0x110] ; 0x0089748b: je 0x897567
  - 0x008974ff: je -> 0x0089750b (jcc_true) | ctx: 0x008974f7: mov dword ptr [ebp - 0x38], eax ; 0x008974fa: mov eax, dword ptr [ebp + 0x14] ; 0x008974fd: cmp ecx, eax ; 0x008974ff: je 0x89750b
  - 0x008974ff: je -> 0x00897501 (jcc_false) | ctx: 0x008974f7: mov dword ptr [ebp - 0x38], eax ; 0x008974fa: mov eax, dword ptr [ebp + 0x14] ; 0x008974fd: cmp ecx, eax ; 0x008974ff: je 0x89750b
  - 0x00897539: jb -> 0x00897546 (jcc_true) | ctx: 0x00897527: mov dword ptr [ebp - 0x74], 0xc1ce94 ; 0x0089752e: cmp dword ptr [ebp - 0x20], 0x10 ; 0x00897532: mov dword ptr [ebp - 4], 1 ; 0x00897539: jb 0x897546
  - 0x00897539: jb -> 0x0089753b (jcc_false) | ctx: 0x00897527: mov dword ptr [ebp - 0x74], 0xc1ce94 ; 0x0089752e: cmp dword ptr [ebp - 0x20], 0x10 ; 0x00897532: mov dword ptr [ebp - 4], 1 ; 0x00897539: jb 0x897546
  - 0x00897539: jb -> 0x00897546 (jcc_true) | ctx: 0x00897527: mov dword ptr [ebp - 0x74], 0xc1ce94 ; 0x0089752e: cmp dword ptr [ebp - 0x20], 0x10 ; 0x00897532: mov dword ptr [ebp - 4], 1 ; 0x00897539: jb 0x897546
  - 0x00897539: jb -> 0x0089753b (jcc_false) | ctx: 0x00897527: mov dword ptr [ebp - 0x74], 0xc1ce94 ; 0x0089752e: cmp dword ptr [ebp - 0x20], 0x10 ; 0x00897532: mov dword ptr [ebp - 4], 1 ; 0x00897539: jb 0x897546

### 0x008987ad
- blocks=8, insns=125, edges=17, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x008988a1)
- branch points:
  - 0x008987de: je -> 0x00898846 (jcc_true) | ctx: 0x008987d2: mov dword ptr [ebp - 0x18], ebx ; 0x008987d5: mov dword ptr [ebp - 4], 0 ; 0x008987dc: test ebx, ebx ; 0x008987de: je 0x898846
  - 0x008987de: je -> 0x008987e0 (jcc_false) | ctx: 0x008987d2: mov dword ptr [ebp - 0x18], ebx ; 0x008987d5: mov dword ptr [ebp - 4], 0 ; 0x008987dc: test ebx, ebx ; 0x008987de: je 0x898846
  - 0x0089889a: je -> 0x008988a6 (jcc_true) | ctx: 0x00898892: mov eax, dword ptr [ebp + 0xc] ; 0x00898895: lea ecx, [ebx + 0x34] ; 0x00898898: cmp ecx, eax ; 0x0089889a: je 0x8988a6
  - 0x0089889a: je -> 0x0089889c (jcc_false) | ctx: 0x00898892: mov eax, dword ptr [ebp + 0xc] ; 0x00898895: lea ecx, [ebx + 0x34] ; 0x00898898: cmp ecx, eax ; 0x0089889a: je 0x8988a6
  - 0x00898836: jb -> 0x0089883a (jcc_true) | ctx: 0x00898824: mov dword ptr [eax + 0x14], 0xf ; 0x0089882b: mov dword ptr [eax + 0x10], 0 ; 0x00898832: cmp dword ptr [eax + 0x14], 0x10 ; 0x00898836: jb 0x89883a
  - 0x00898836: jb -> 0x00898838 (jcc_false) | ctx: 0x00898824: mov dword ptr [eax + 0x14], 0xf ; 0x0089882b: mov dword ptr [eax + 0x10], 0 ; 0x00898832: cmp dword ptr [eax + 0x14], 0x10 ; 0x00898836: jb 0x89883a
  - 0x00898844: jmp -> 0x00898848 (jmp) | ctx: 0x0089883a: mov byte ptr [eax], 0 ; 0x0089883d: mov dword ptr [ebx + 0x4c], 0xffffffff ; 0x00898844: jmp 0x898848
  - 0x00898844: jmp -> 0x00898848 (jmp) | ctx: 0x00898838: mov eax, dword ptr [eax] ; 0x0089883a: mov byte ptr [eax], 0 ; 0x0089883d: mov dword ptr [ebx + 0x4c], 0xffffffff ; 0x00898844: jmp 0x898848
  - 0x0089889a: je -> 0x008988a6 (jcc_true) | ctx: 0x00898892: mov eax, dword ptr [ebp + 0xc] ; 0x00898895: lea ecx, [ebx + 0x34] ; 0x00898898: cmp ecx, eax ; 0x0089889a: je 0x8988a6
  - 0x0089889a: je -> 0x0089889c (jcc_false) | ctx: 0x00898892: mov eax, dword ptr [ebp + 0xc] ; 0x00898895: lea ecx, [ebx + 0x34] ; 0x00898898: cmp ecx, eax ; 0x0089889a: je 0x8988a6

### 0x008989b0
- blocks=5, insns=113, edges=17, jcc=3, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00898a47)
- branch points:
  - 0x00898a40: je -> 0x00898a4c (jcc_true) | ctx: 0x00898a38: mov dword ptr [ebp - 0x48], esi ; 0x00898a3b: lea eax, [ebx + 0x54] ; 0x00898a3e: cmp ecx, eax ; 0x00898a40: je 0x898a4c
  - 0x00898a40: je -> 0x00898a42 (jcc_false) | ctx: 0x00898a38: mov dword ptr [ebp - 0x48], esi ; 0x00898a3b: lea eax, [ebx + 0x54] ; 0x00898a3e: cmp ecx, eax ; 0x00898a40: je 0x898a4c
  - 0x00898a96: jb -> 0x00898aa3 (jcc_true) | ctx: 0x00898a89: call 0x973a50 ; 0x00898a8e: cmp dword ptr [ebp - 0x24], 0x10 ; 0x00898a92: mov byte ptr [ebp - 4], 2 ; 0x00898a96: jb 0x898aa3
  - 0x00898a96: jb -> 0x00898a98 (jcc_false) | ctx: 0x00898a89: call 0x973a50 ; 0x00898a8e: cmp dword ptr [ebp - 0x24], 0x10 ; 0x00898a92: mov byte ptr [ebp - 4], 2 ; 0x00898a96: jb 0x898aa3
  - 0x00898a96: jb -> 0x00898aa3 (jcc_true) | ctx: 0x00898a89: call 0x973a50 ; 0x00898a8e: cmp dword ptr [ebp - 0x24], 0x10 ; 0x00898a92: mov byte ptr [ebp - 4], 2 ; 0x00898a96: jb 0x898aa3
  - 0x00898a96: jb -> 0x00898a98 (jcc_false) | ctx: 0x00898a89: call 0x973a50 ; 0x00898a8e: cmp dword ptr [ebp - 0x24], 0x10 ; 0x00898a92: mov byte ptr [ebp - 4], 2 ; 0x00898a96: jb 0x898aa3

### 0x00898c43
- blocks=21, insns=308, edges=66, jcc=14, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00898d6a)
- branch points:
  - 0x00898c55: jne -> 0x00898c6b (jcc_true) | ctx: 0x00898c4c: mov eax, edx ; 0x00898c4e: mov esi, dword ptr [edx + 4] ; 0x00898c51: cmp byte ptr [esi + 0xd], 0 ; 0x00898c55: jne 0x898c6b
  - 0x00898c55: jne -> 0x00898c57 (jcc_false) | ctx: 0x00898c4c: mov eax, edx ; 0x00898c4e: mov esi, dword ptr [edx + 4] ; 0x00898c51: cmp byte ptr [esi + 0xd], 0 ; 0x00898c55: jne 0x898c6b
  - 0x00898c6d: je -> 0x00898c74 (jcc_true) | ctx: 0x00898c6b: cmp eax, edx ; 0x00898c6d: je 0x898c74
  - 0x00898c6d: je -> 0x00898c6f (jcc_false) | ctx: 0x00898c6b: cmp eax, edx ; 0x00898c6d: je 0x898c74
  - 0x00898c5a: jae -> 0x00898c61 (jcc_true) | ctx: 0x00898c57: cmp dword ptr [esi + 0x10], ecx ; 0x00898c5a: jae 0x898c61
  - 0x00898c5a: jae -> 0x00898c5c (jcc_false) | ctx: 0x00898c57: cmp dword ptr [esi + 0x10], ecx ; 0x00898c5a: jae 0x898c61
  - 0x00898c78: je -> 0x00899002 (jcc_true) | ctx: 0x00898c74: mov eax, edx ; 0x00898c76: cmp eax, edx ; 0x00898c78: je 0x899002
  - 0x00898c78: je -> 0x00898c7e (jcc_false) | ctx: 0x00898c74: mov eax, edx ; 0x00898c76: cmp eax, edx ; 0x00898c78: je 0x899002
  - 0x00898c72: jae -> 0x00898c76 (jcc_true) | ctx: 0x00898c6f: cmp ecx, dword ptr [eax + 0x10] ; 0x00898c72: jae 0x898c76
  - 0x00898c72: jae -> 0x00898c74 (jcc_false) | ctx: 0x00898c6f: cmp ecx, dword ptr [eax + 0x10] ; 0x00898c72: jae 0x898c76
  - 0x00898c69: je -> 0x00898c57 (jcc_true) | ctx: 0x00898c61: mov eax, esi ; 0x00898c63: mov esi, dword ptr [esi] ; 0x00898c65: cmp byte ptr [esi + 0xd], 0 ; 0x00898c69: je 0x898c57
  - 0x00898c69: je -> 0x00898c6b (jcc_false) | ctx: 0x00898c61: mov eax, esi ; 0x00898c63: mov esi, dword ptr [esi] ; 0x00898c65: cmp byte ptr [esi + 0xd], 0 ; 0x00898c69: je 0x898c57
  - 0x00898c5f: jmp -> 0x00898c65 (jmp) | ctx: 0x00898c5c: mov esi, dword ptr [esi + 8] ; 0x00898c5f: jmp 0x898c65
  - 0x00898c83: je -> 0x00899002 (jcc_true) | ctx: 0x00898c7e: mov ebx, dword ptr [eax + 0x14] ; 0x00898c81: test ebx, ebx ; 0x00898c83: je 0x899002
  - 0x00898c83: je -> 0x00898c89 (jcc_false) | ctx: 0x00898c7e: mov ebx, dword ptr [eax + 0x14] ; 0x00898c81: test ebx, ebx ; 0x00898c83: je 0x899002
  - 0x00898c78: je -> 0x00899002 (jcc_true) | ctx: 0x00898c76: cmp eax, edx ; 0x00898c78: je 0x899002
  - 0x00898c78: je -> 0x00898c7e (jcc_false) | ctx: 0x00898c76: cmp eax, edx ; 0x00898c78: je 0x899002
  - 0x00898c69: je -> 0x00898c57 (jcc_true) | ctx: 0x00898c65: cmp byte ptr [esi + 0xd], 0 ; 0x00898c69: je 0x898c57
  - 0x00898c69: je -> 0x00898c6b (jcc_false) | ctx: 0x00898c65: cmp byte ptr [esi + 0xd], 0 ; 0x00898c69: je 0x898c57
  - 0x00898ca9: je -> 0x00899002 (jcc_true) | ctx: 0x00898c9e: call 0x8b0910 ; 0x00898ca3: mov esi, dword ptr [ebp - 0x14] ; 0x00898ca6: cmp esi, dword ptr [edi + 0x48] ; 0x00898ca9: je 0x899002
  - 0x00898ca9: je -> 0x00898caf (jcc_false) | ctx: 0x00898c9e: call 0x8b0910 ; 0x00898ca3: mov esi, dword ptr [ebp - 0x14] ; 0x00898ca6: cmp esi, dword ptr [edi + 0x48] ; 0x00898ca9: je 0x899002
  - 0x00898cf7: je -> 0x00898de5 (jcc_true) | ctx: 0x00898cee: mov ecx, ebx ; 0x00898cf0: call 0x891110 ; 0x00898cf5: test eax, eax ; 0x00898cf7: je 0x898de5
  - 0x00898cf7: je -> 0x00898cfd (jcc_false) | ctx: 0x00898cee: mov ecx, ebx ; 0x00898cf0: call 0x891110 ; 0x00898cf5: test eax, eax ; 0x00898cf7: je 0x898de5
  - 0x00898e1d: js -> 0x00898f43 (jcc_true) | ctx: 0x00898e14: mov ecx, eax ; 0x00898e16: call 0x61d7f0 ; 0x00898e1b: test eax, eax ; 0x00898e1d: js 0x898f43
  - 0x00898e1d: js -> 0x00898e23 (jcc_false) | ctx: 0x00898e14: mov ecx, eax ; 0x00898e16: call 0x61d7f0 ; 0x00898e1b: test eax, eax ; 0x00898e1d: js 0x898f43
  - 0x00898e2c: jne -> 0x00898f43 (jcc_true) | ctx: 0x00898e23: mov eax, dword ptr [esi + 0x90] ; 0x00898e29: cmp dword ptr [ebp - 0x10], eax ; 0x00898e2c: jne 0x898f43
  - 0x00898e2c: jne -> 0x00898e32 (jcc_false) | ctx: 0x00898e23: mov eax, dword ptr [esi + 0x90] ; 0x00898e29: cmp dword ptr [ebp - 0x10], eax ; 0x00898e2c: jne 0x898f43
  - 0x00898e66: je -> 0x00898f1b (jcc_true) | ctx: 0x00898e5d: push eax ; 0x00898e5e: call 0x889bd0 ; 0x00898e63: cmp dword ptr [eax], 1 ; 0x00898e66: je 0x898f1b
  - 0x00898e66: je -> 0x00898e6c (jcc_false) | ctx: 0x00898e5d: push eax ; 0x00898e5e: call 0x889bd0 ; 0x00898e63: cmp dword ptr [eax], 1 ; 0x00898e66: je 0x898f1b
  - 0x00898f3e: jmp -> 0x0089900b (jmp) | ctx: 0x00898f30: call 0x905e20 ; 0x00898f35: mov eax, dword ptr [ebp + 8] ; 0x00898f38: mov dword ptr [eax], 1 ; 0x00898f3e: jmp 0x89900b

### 0x008992b0
- blocks=38, insns=504, edges=103, jcc=31, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00899427)
- branch points:
  - 0x008992eb: je -> 0x00899506 (jcc_true) | ctx: 0x008992df: mov eax, dword ptr [edi + 0x20] ; 0x008992e2: mov dword ptr [ebp - 0x10], eax ; 0x008992e5: cmp esi, dword ptr [ebx + 0xa8] ; 0x008992eb: je 0x899506
  - 0x008992eb: je -> 0x008992f1 (jcc_false) | ctx: 0x008992df: mov eax, dword ptr [edi + 0x20] ; 0x008992e2: mov dword ptr [ebp - 0x10], eax ; 0x008992e5: cmp esi, dword ptr [ebx + 0xa8] ; 0x008992eb: je 0x899506
  - 0x00899515: jne -> 0x0089952b (jcc_true) | ctx: 0x0089950b: mov esi, dword ptr [ebp - 0x10] ; 0x0089950e: mov edx, dword ptr [ecx + 4] ; 0x00899511: cmp byte ptr [edx + 0xd], 0 ; 0x00899515: jne 0x89952b
  - 0x00899515: jne -> 0x00899517 (jcc_false) | ctx: 0x0089950b: mov esi, dword ptr [ebp - 0x10] ; 0x0089950e: mov edx, dword ptr [ecx + 4] ; 0x00899511: cmp byte ptr [edx + 0xd], 0 ; 0x00899515: jne 0x89952b
  - 0x0089930b: jne -> 0x008994f1 (jcc_true) | ctx: 0x00899304: mov eax, dword ptr [eax + 4] ; 0x00899307: sub eax, ecx ; 0x00899309: cmp edi, eax ; 0x0089930b: jne 0x8994f1
  - 0x0089930b: jne -> 0x00899311 (jcc_false) | ctx: 0x00899304: mov eax, dword ptr [eax + 4] ; 0x00899307: sub eax, ecx ; 0x00899309: cmp edi, eax ; 0x0089930b: jne 0x8994f1
  - 0x0089952d: je -> 0x00899534 (jcc_true) | ctx: 0x0089952b: cmp eax, ecx ; 0x0089952d: je 0x899534
  - 0x0089952d: je -> 0x0089952f (jcc_false) | ctx: 0x0089952b: cmp eax, ecx ; 0x0089952d: je 0x899534
  - 0x0089951a: jae -> 0x00899521 (jcc_true) | ctx: 0x00899517: cmp dword ptr [edx + 0x10], esi ; 0x0089951a: jae 0x899521
  - 0x0089951a: jae -> 0x0089951c (jcc_false) | ctx: 0x00899517: cmp dword ptr [edx + 0x10], esi ; 0x0089951a: jae 0x899521
  - 0x00899500: jne -> 0x008992f1 (jcc_true) | ctx: 0x008994f4: add esi, 0x40 ; 0x008994f7: mov edi, dword ptr [ebp + 0xc] ; 0x008994fa: cmp esi, dword ptr [ebx + 0xa8] ; 0x00899500: jne 0x8992f1
  - 0x00899500: jne -> 0x00899506 (jcc_false) | ctx: 0x008994f4: add esi, 0x40 ; 0x008994f7: mov edi, dword ptr [ebp + 0xc] ; 0x008994fa: cmp esi, dword ptr [ebx + 0xa8] ; 0x00899500: jne 0x8992f1
  - 0x00899316: jb -> 0x00899329 (jcc_true) | ctx: 0x00899311: sub ebx, edx ; 0x00899313: sub ebx, 4 ; 0x00899316: jb 0x899329
  - 0x00899316: jb -> 0x00899318 (jcc_false) | ctx: 0x00899311: sub ebx, edx ; 0x00899313: sub ebx, 4 ; 0x00899316: jb 0x899329
  - 0x00899538: je -> 0x008996df (jcc_true) | ctx: 0x00899534: mov eax, ecx ; 0x00899536: cmp eax, ecx ; 0x00899538: je 0x8996df
  - 0x00899538: je -> 0x0089953e (jcc_false) | ctx: 0x00899534: mov eax, ecx ; 0x00899536: cmp eax, ecx ; 0x00899538: je 0x8996df
  - 0x00899532: jae -> 0x00899536 (jcc_true) | ctx: 0x0089952f: cmp esi, dword ptr [eax + 0x10] ; 0x00899532: jae 0x899536
  - 0x00899532: jae -> 0x00899534 (jcc_false) | ctx: 0x0089952f: cmp esi, dword ptr [eax + 0x10] ; 0x00899532: jae 0x899536
  - 0x00899529: je -> 0x00899517 (jcc_true) | ctx: 0x00899521: mov eax, edx ; 0x00899523: mov edx, dword ptr [edx] ; 0x00899525: cmp byte ptr [edx + 0xd], 0 ; 0x00899529: je 0x899517
  - 0x00899529: je -> 0x0089952b (jcc_false) | ctx: 0x00899521: mov eax, edx ; 0x00899523: mov edx, dword ptr [edx] ; 0x00899525: cmp byte ptr [edx + 0xd], 0 ; 0x00899529: je 0x899517
  - 0x0089951f: jmp -> 0x00899525 (jmp) | ctx: 0x0089951c: mov edx, dword ptr [edx + 8] ; 0x0089951f: jmp 0x899525
  - 0x0089932c: je -> 0x0089936b (jcc_true) | ctx: 0x00899329: cmp ebx, -4 ; 0x0089932c: je 0x89936b
  - 0x0089932c: je -> 0x0089932e (jcc_false) | ctx: 0x00899329: cmp ebx, -4 ; 0x0089932c: je 0x89936b
  - 0x0089931c: jne -> 0x0089932e (jcc_true) | ctx: 0x00899318: mov eax, dword ptr [edx] ; 0x0089931a: cmp eax, dword ptr [ecx] ; 0x0089931c: jne 0x89932e
  - 0x0089931c: jne -> 0x0089931e (jcc_false) | ctx: 0x00899318: mov eax, dword ptr [edx] ; 0x0089931a: cmp eax, dword ptr [ecx] ; 0x0089931c: jne 0x89932e
  - 0x00899543: je -> 0x008996df (jcc_true) | ctx: 0x0089953e: mov esi, dword ptr [eax + 0x14] ; 0x00899541: test esi, esi ; 0x00899543: je 0x8996df
  - 0x00899543: je -> 0x00899549 (jcc_false) | ctx: 0x0089953e: mov esi, dword ptr [eax + 0x14] ; 0x00899541: test esi, esi ; 0x00899543: je 0x8996df
  - 0x00899538: je -> 0x008996df (jcc_true) | ctx: 0x00899536: cmp eax, ecx ; 0x00899538: je 0x8996df
  - 0x00899538: je -> 0x0089953e (jcc_false) | ctx: 0x00899536: cmp eax, ecx ; 0x00899538: je 0x8996df
  - 0x00899529: je -> 0x00899517 (jcc_true) | ctx: 0x00899525: cmp byte ptr [edx + 0xd], 0 ; 0x00899529: je 0x899517
  - 0x00899529: je -> 0x0089952b (jcc_false) | ctx: 0x00899525: cmp byte ptr [edx + 0xd], 0 ; 0x00899529: je 0x899517
  - 0x00899374: jne -> 0x008994f1 (jcc_true) | ctx: 0x0089936b: mov ebx, dword ptr [ebp + 0xc] ; 0x0089936e: mov eax, dword ptr [esi + 0xc] ; 0x00899371: cmp eax, dword ptr [ebx + 0x20] ; 0x00899374: jne 0x8994f1
  - 0x00899374: jne -> 0x0089937a (jcc_false) | ctx: 0x0089936b: mov ebx, dword ptr [ebp + 0xc] ; 0x0089936e: mov eax, dword ptr [esi + 0xc] ; 0x00899371: cmp eax, dword ptr [ebx + 0x20] ; 0x00899374: jne 0x8994f1
  - 0x00899332: jne -> 0x008994f1 (jcc_true) | ctx: 0x0089932e: mov al, byte ptr [edx] ; 0x00899330: cmp al, byte ptr [ecx] ; 0x00899332: jne 0x8994f1
  - 0x00899332: jne -> 0x00899338 (jcc_false) | ctx: 0x0089932e: mov al, byte ptr [edx] ; 0x00899330: cmp al, byte ptr [ecx] ; 0x00899332: jne 0x8994f1
  - 0x00899327: jae -> 0x00899318 (jcc_true) | ctx: 0x0089931e: add edx, 4 ; 0x00899321: add ecx, 4 ; 0x00899324: sub ebx, 4 ; 0x00899327: jae 0x899318
  - 0x00899327: jae -> 0x00899329 (jcc_false) | ctx: 0x0089931e: add edx, 4 ; 0x00899321: add ecx, 4 ; 0x00899324: sub ebx, 4 ; 0x00899327: jae 0x899318
  - 0x008995b0: jb -> 0x008995c0 (jcc_true) | ctx: 0x0089959d: call 0x8904f0 ; 0x008995a2: cmp dword ptr [ebp - 0xec], 0x10 ; 0x008995a9: mov dword ptr [ebp - 4], 8 ; 0x008995b0: jb 0x8995c0
  - 0x008995b0: jb -> 0x008995b2 (jcc_false) | ctx: 0x0089959d: call 0x8904f0 ; 0x008995a2: cmp dword ptr [ebp - 0xec], 0x10 ; 0x008995a9: mov dword ptr [ebp - 4], 8 ; 0x008995b0: jb 0x8995c0
  - 0x0089937f: je -> 0x00899389 (jcc_true) | ctx: 0x0089937a: mov ecx, dword ptr [esi + 0x38] ; 0x0089937d: test ecx, ecx ; 0x0089937f: je 0x899389
  - 0x0089937f: je -> 0x00899381 (jcc_false) | ctx: 0x0089937a: mov ecx, dword ptr [esi + 0x38] ; 0x0089937d: test ecx, ecx ; 0x0089937f: je 0x899389
  - 0x0089933b: je -> 0x0089936b (jcc_true) | ctx: 0x00899338: cmp ebx, -3 ; 0x0089933b: je 0x89936b
  - 0x0089933b: je -> 0x0089933d (jcc_false) | ctx: 0x00899338: cmp ebx, -3 ; 0x0089933b: je 0x89936b
  - 0x008996da: jmp -> 0x008997bb (jmp) | ctx: 0x008996c3: mov dword ptr [ebp - 4], 0xa ; 0x008996ca: lea ecx, [ebp - 0xd0] ; 0x008996d0: mov dword ptr [ebp - 0xd0], 0xc1d670 ; 0x008996da: jmp 0x8997bb
  - 0x008996da: jmp -> 0x008997bb (jmp) | ctx: 0x008996c3: mov dword ptr [ebp - 4], 0xa ; 0x008996ca: lea ecx, [ebp - 0xd0] ; 0x008996d0: mov dword ptr [ebp - 0xd0], 0xc1d670 ; 0x008996da: jmp 0x8997bb
  - 0x00899450: jb -> 0x00899460 (jcc_true) | ctx: 0x00899442: mov dword ptr [ebp - 0x34], eax ; 0x00899445: cmp dword ptr [ebp - 0xd4], 0x10 ; 0x0089944c: mov byte ptr [ebp - 4], 2 ; 0x00899450: jb 0x899460
  - 0x00899450: jb -> 0x00899452 (jcc_false) | ctx: 0x00899442: mov dword ptr [ebp - 0x34], eax ; 0x00899445: cmp dword ptr [ebp - 0xd4], 0x10 ; 0x0089944c: mov byte ptr [ebp - 4], 2 ; 0x00899450: jb 0x899460
  - 0x00899450: jb -> 0x00899460 (jcc_true) | ctx: 0x00899442: mov dword ptr [ebp - 0x34], eax ; 0x00899445: cmp dword ptr [ebp - 0xd4], 0x10 ; 0x0089944c: mov byte ptr [ebp - 4], 2 ; 0x00899450: jb 0x899460
  - 0x00899450: jb -> 0x00899452 (jcc_false) | ctx: 0x00899442: mov dword ptr [ebp - 0x34], eax ; 0x00899445: cmp dword ptr [ebp - 0xd4], 0x10 ; 0x0089944c: mov byte ptr [ebp - 4], 2 ; 0x00899450: jb 0x899460
  - 0x00899343: jne -> 0x008994f1 (jcc_true) | ctx: 0x0089933d: mov al, byte ptr [edx + 1] ; 0x00899340: cmp al, byte ptr [ecx + 1] ; 0x00899343: jne 0x8994f1
  - 0x00899343: jne -> 0x00899349 (jcc_false) | ctx: 0x0089933d: mov al, byte ptr [edx + 1] ; 0x00899340: cmp al, byte ptr [ecx + 1] ; 0x00899343: jne 0x8994f1
  - 0x008994db: jb -> 0x008994e8 (jcc_true) | ctx: 0x008994ce: call 0x973a50 ; 0x008994d3: cmp dword ptr [ebp - 0x3c], 0x10 ; 0x008994d7: mov byte ptr [ebp - 4], 4 ; 0x008994db: jb 0x8994e8
  - 0x008994db: jb -> 0x008994dd (jcc_false) | ctx: 0x008994ce: call 0x973a50 ; 0x008994d3: cmp dword ptr [ebp - 0x3c], 0x10 ; 0x008994d7: mov byte ptr [ebp - 4], 4 ; 0x008994db: jb 0x8994e8
  - 0x008994db: jb -> 0x008994e8 (jcc_true) | ctx: 0x008994ce: call 0x973a50 ; 0x008994d3: cmp dword ptr [ebp - 0x3c], 0x10 ; 0x008994d7: mov byte ptr [ebp - 4], 4 ; 0x008994db: jb 0x8994e8
  - 0x008994db: jb -> 0x008994dd (jcc_false) | ctx: 0x008994ce: call 0x973a50 ; 0x008994d3: cmp dword ptr [ebp - 0x3c], 0x10 ; 0x008994d7: mov byte ptr [ebp - 4], 4 ; 0x008994db: jb 0x8994e8
  - 0x0089934c: je -> 0x0089936b (jcc_true) | ctx: 0x00899349: cmp ebx, -2 ; 0x0089934c: je 0x89936b
  - 0x0089934c: je -> 0x0089934e (jcc_false) | ctx: 0x00899349: cmp ebx, -2 ; 0x0089934c: je 0x89936b
  - 0x008994ef: jmp -> 0x008994f7 (jmp) | ctx: 0x008994e8: mov dword ptr [ebp - 4], 0xffffffff ; 0x008994ef: jmp 0x8994f7
  - 0x008994ef: jmp -> 0x008994f7 (jmp) | ctx: 0x008994e0: call 0x9afbf0 ; 0x008994e5: add esp, 4 ; 0x008994e8: mov dword ptr [ebp - 4], 0xffffffff ; 0x008994ef: jmp 0x8994f7
  - 0x00899354: jne -> 0x008994f1 (jcc_true) | ctx: 0x0089934e: mov al, byte ptr [edx + 2] ; 0x00899351: cmp al, byte ptr [ecx + 2] ; 0x00899354: jne 0x8994f1
  - 0x00899354: jne -> 0x0089935a (jcc_false) | ctx: 0x0089934e: mov al, byte ptr [edx + 2] ; 0x00899351: cmp al, byte ptr [ecx + 2] ; 0x00899354: jne 0x8994f1
  - 0x00899500: jne -> 0x008992f1 (jcc_true) | ctx: 0x008994f7: mov edi, dword ptr [ebp + 0xc] ; 0x008994fa: cmp esi, dword ptr [ebx + 0xa8] ; 0x00899500: jne 0x8992f1
  - 0x00899500: jne -> 0x00899506 (jcc_false) | ctx: 0x008994f7: mov edi, dword ptr [ebp + 0xc] ; 0x008994fa: cmp esi, dword ptr [ebx + 0xa8] ; 0x00899500: jne 0x8992f1
  - 0x0089935d: je -> 0x0089936b (jcc_true) | ctx: 0x0089935a: cmp ebx, -1 ; 0x0089935d: je 0x89936b
  - 0x0089935d: je -> 0x0089935f (jcc_false) | ctx: 0x0089935a: cmp ebx, -1 ; 0x0089935d: je 0x89936b
  - 0x00899365: jne -> 0x008994f1 (jcc_true) | ctx: 0x0089935f: mov al, byte ptr [edx + 3] ; 0x00899362: cmp al, byte ptr [ecx + 3] ; 0x00899365: jne 0x8994f1
  - 0x00899365: jne -> 0x0089936b (jcc_false) | ctx: 0x0089935f: mov al, byte ptr [edx + 3] ; 0x00899362: cmp al, byte ptr [ecx + 3] ; 0x00899365: jne 0x8994f1

### 0x00899970
- blocks=12, insns=174, edges=26, jcc=8, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x00899ac5)
- branch points:
  - 0x008999c2: je -> 0x00899a3c (jcc_true) | ctx: 0x008999ba: mov dword ptr [ebp - 0x10], edi ; 0x008999bd: mov dword ptr [ebp - 0x10], edi ; 0x008999c0: test edi, edi ; 0x008999c2: je 0x899a3c
  - 0x008999c2: je -> 0x008999c4 (jcc_false) | ctx: 0x008999ba: mov dword ptr [ebp - 0x10], edi ; 0x008999bd: mov dword ptr [ebp - 0x10], edi ; 0x008999c0: test edi, edi ; 0x008999c2: je 0x899a3c
  - 0x00899abe: je -> 0x00899aca (jcc_true) | ctx: 0x00899ab6: mov dword ptr [edi + 0x20], eax ; 0x00899ab9: lea eax, [ebp - 0x2c] ; 0x00899abc: cmp ecx, eax ; 0x00899abe: je 0x899aca
  - 0x00899abe: je -> 0x00899ac0 (jcc_false) | ctx: 0x00899ab6: mov dword ptr [edi + 0x20], eax ; 0x00899ab9: lea eax, [ebp - 0x2c] ; 0x00899abc: cmp ecx, eax ; 0x00899abe: je 0x899aca
  - 0x00899a2c: jb -> 0x00899a30 (jcc_true) | ctx: 0x00899a1a: mov dword ptr [eax + 0x14], 0xf ; 0x00899a21: mov dword ptr [eax + 0x10], 0 ; 0x00899a28: cmp dword ptr [eax + 0x14], 0x10 ; 0x00899a2c: jb 0x899a30
  - 0x00899a2c: jb -> 0x00899a2e (jcc_false) | ctx: 0x00899a1a: mov dword ptr [eax + 0x14], 0xf ; 0x00899a21: mov dword ptr [eax + 0x10], 0 ; 0x00899a28: cmp dword ptr [eax + 0x14], 0x10 ; 0x00899a2c: jb 0x899a30
  - 0x00899ada: jb -> 0x00899ae7 (jcc_true) | ctx: 0x00899acf: mov dword ptr [edi + 0x48], eax ; 0x00899ad2: cmp dword ptr [ebp - 0x18], 0x10 ; 0x00899ad6: mov byte ptr [ebp - 4], 6 ; 0x00899ada: jb 0x899ae7
  - 0x00899ada: jb -> 0x00899adc (jcc_false) | ctx: 0x00899acf: mov dword ptr [edi + 0x48], eax ; 0x00899ad2: cmp dword ptr [ebp - 0x18], 0x10 ; 0x00899ad6: mov byte ptr [ebp - 4], 6 ; 0x00899ada: jb 0x899ae7
  - 0x00899ada: jb -> 0x00899ae7 (jcc_true) | ctx: 0x00899acf: mov dword ptr [edi + 0x48], eax ; 0x00899ad2: cmp dword ptr [ebp - 0x18], 0x10 ; 0x00899ad6: mov byte ptr [ebp - 4], 6 ; 0x00899ada: jb 0x899ae7
  - 0x00899ada: jb -> 0x00899adc (jcc_false) | ctx: 0x00899acf: mov dword ptr [edi + 0x48], eax ; 0x00899ad2: cmp dword ptr [ebp - 0x18], 0x10 ; 0x00899ad6: mov byte ptr [ebp - 4], 6 ; 0x00899ada: jb 0x899ae7
  - 0x00899a3a: jmp -> 0x00899a3e (jmp) | ctx: 0x00899a30: mov byte ptr [eax], 0 ; 0x00899a33: mov dword ptr [edi + 0x48], 0xffffffff ; 0x00899a3a: jmp 0x899a3e
  - 0x00899a3a: jmp -> 0x00899a3e (jmp) | ctx: 0x00899a2e: mov eax, dword ptr [eax] ; 0x00899a30: mov byte ptr [eax], 0 ; 0x00899a33: mov dword ptr [edi + 0x48], 0xffffffff ; 0x00899a3a: jmp 0x899a3e
  - 0x00899b0a: je -> 0x00899b24 (jcc_true) | ctx: 0x00899b01: mov ecx, dword ptr [ebp + 8] ; 0x00899b04: mov byte ptr [ebp - 4], 8 ; 0x00899b08: test ecx, ecx ; 0x00899b0a: je 0x899b24
  - 0x00899b0a: je -> 0x00899b0c (jcc_false) | ctx: 0x00899b01: mov ecx, dword ptr [ebp + 8] ; 0x00899b04: mov byte ptr [ebp - 4], 8 ; 0x00899b08: test ecx, ecx ; 0x00899b0a: je 0x899b24
  - 0x00899b0a: je -> 0x00899b24 (jcc_true) | ctx: 0x00899b01: mov ecx, dword ptr [ebp + 8] ; 0x00899b04: mov byte ptr [ebp - 4], 8 ; 0x00899b08: test ecx, ecx ; 0x00899b0a: je 0x899b24
  - 0x00899b0a: je -> 0x00899b0c (jcc_false) | ctx: 0x00899b01: mov ecx, dword ptr [ebp + 8] ; 0x00899b04: mov byte ptr [ebp - 4], 8 ; 0x00899b08: test ecx, ecx ; 0x00899b0a: je 0x899b24
  - 0x00899abe: je -> 0x00899aca (jcc_true) | ctx: 0x00899ab6: mov dword ptr [edi + 0x20], eax ; 0x00899ab9: lea eax, [ebp - 0x2c] ; 0x00899abc: cmp ecx, eax ; 0x00899abe: je 0x899aca
  - 0x00899abe: je -> 0x00899ac0 (jcc_false) | ctx: 0x00899ab6: mov dword ptr [edi + 0x20], eax ; 0x00899ab9: lea eax, [ebp - 0x2c] ; 0x00899abc: cmp ecx, eax ; 0x00899abe: je 0x899aca

### 0x0089a3c0
- blocks=71, insns=855, edges=166, jcc=52, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0089a678)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0089a888)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0089aa38)
- branch points:
  - 0x0089a3f5: jne -> 0x0089a40b (jcc_true) | ctx: 0x0089a3eb: mov esi, dword ptr [edx + 4] ; 0x0089a3ee: mov dword ptr [ebp - 0x10], ecx ; 0x0089a3f1: cmp byte ptr [esi + 0xd], 0 ; 0x0089a3f5: jne 0x89a40b
  - 0x0089a3f5: jne -> 0x0089a3f7 (jcc_false) | ctx: 0x0089a3eb: mov esi, dword ptr [edx + 4] ; 0x0089a3ee: mov dword ptr [ebp - 0x10], ecx ; 0x0089a3f1: cmp byte ptr [esi + 0xd], 0 ; 0x0089a3f5: jne 0x89a40b
  - 0x0089a40d: je -> 0x0089a414 (jcc_true) | ctx: 0x0089a40b: cmp eax, edx ; 0x0089a40d: je 0x89a414
  - 0x0089a40d: je -> 0x0089a40f (jcc_false) | ctx: 0x0089a40b: cmp eax, edx ; 0x0089a40d: je 0x89a414
  - 0x0089a3fa: jae -> 0x0089a401 (jcc_true) | ctx: 0x0089a3f7: cmp dword ptr [esi + 0x10], ecx ; 0x0089a3fa: jae 0x89a401
  - 0x0089a3fa: jae -> 0x0089a3fc (jcc_false) | ctx: 0x0089a3f7: cmp dword ptr [esi + 0x10], ecx ; 0x0089a3fa: jae 0x89a401
  - 0x0089a418: je -> 0x0089ab25 (jcc_true) | ctx: 0x0089a414: mov eax, edx ; 0x0089a416: cmp eax, edx ; 0x0089a418: je 0x89ab25
  - 0x0089a418: je -> 0x0089a41e (jcc_false) | ctx: 0x0089a414: mov eax, edx ; 0x0089a416: cmp eax, edx ; 0x0089a418: je 0x89ab25
  - 0x0089a412: jae -> 0x0089a416 (jcc_true) | ctx: 0x0089a40f: cmp ecx, dword ptr [eax + 0x10] ; 0x0089a412: jae 0x89a416
  - 0x0089a412: jae -> 0x0089a414 (jcc_false) | ctx: 0x0089a40f: cmp ecx, dword ptr [eax + 0x10] ; 0x0089a412: jae 0x89a416
  - 0x0089a409: je -> 0x0089a3f7 (jcc_true) | ctx: 0x0089a401: mov eax, esi ; 0x0089a403: mov esi, dword ptr [esi] ; 0x0089a405: cmp byte ptr [esi + 0xd], 0 ; 0x0089a409: je 0x89a3f7
  - 0x0089a409: je -> 0x0089a40b (jcc_false) | ctx: 0x0089a401: mov eax, esi ; 0x0089a403: mov esi, dword ptr [esi] ; 0x0089a405: cmp byte ptr [esi + 0xd], 0 ; 0x0089a409: je 0x89a3f7
  - 0x0089a3ff: jmp -> 0x0089a405 (jmp) | ctx: 0x0089a3fc: mov esi, dword ptr [esi + 8] ; 0x0089a3ff: jmp 0x89a405
  - 0x0089a423: je -> 0x0089ab25 (jcc_true) | ctx: 0x0089a41e: mov edx, dword ptr [eax + 0x14] ; 0x0089a421: test edx, edx ; 0x0089a423: je 0x89ab25
  - 0x0089a423: je -> 0x0089a429 (jcc_false) | ctx: 0x0089a41e: mov edx, dword ptr [eax + 0x14] ; 0x0089a421: test edx, edx ; 0x0089a423: je 0x89ab25
  - 0x0089a418: je -> 0x0089ab25 (jcc_true) | ctx: 0x0089a416: cmp eax, edx ; 0x0089a418: je 0x89ab25
  - 0x0089a418: je -> 0x0089a41e (jcc_false) | ctx: 0x0089a416: cmp eax, edx ; 0x0089a418: je 0x89ab25
  - 0x0089a409: je -> 0x0089a3f7 (jcc_true) | ctx: 0x0089a405: cmp byte ptr [esi + 0xd], 0 ; 0x0089a409: je 0x89a3f7
  - 0x0089a409: je -> 0x0089a40b (jcc_false) | ctx: 0x0089a405: cmp byte ptr [esi + 0xd], 0 ; 0x0089a409: je 0x89a3f7
  - 0x0089a430: je -> 0x0089a52d (jcc_true) | ctx: 0x0089a429: cmp dword ptr [edx + 0x208], -1 ; 0x0089a430: je 0x89a52d
  - 0x0089a430: je -> 0x0089a436 (jcc_false) | ctx: 0x0089a429: cmp dword ptr [edx + 0x208], -1 ; 0x0089a430: je 0x89a52d
  - 0x0089a54f: je -> 0x0089a75a (jcc_true) | ctx: 0x0089a53c: mov dword ptr [edx + 0x210], eax ; 0x0089a542: mov dword ptr [edx + 0x214], ecx ; 0x0089a548: cmp dword ptr [ebx + 0x9c], -1 ; 0x0089a54f: je 0x89a75a
  - 0x0089a54f: je -> 0x0089a555 (jcc_false) | ctx: 0x0089a53c: mov dword ptr [edx + 0x210], eax ; 0x0089a542: mov dword ptr [edx + 0x214], ecx ; 0x0089a548: cmp dword ptr [ebx + 0x9c], -1 ; 0x0089a54f: je 0x89a75a
  - 0x0089a45f: je -> 0x0089a4bc (jcc_true) | ctx: 0x0089a455: call 0x7f3b40 ; 0x0089a45a: mov edi, dword ptr [ebp - 0x18] ; 0x0089a45d: test edi, edi ; 0x0089a45f: je 0x89a4bc
  - 0x0089a45f: je -> 0x0089a461 (jcc_false) | ctx: 0x0089a455: call 0x7f3b40 ; 0x0089a45a: mov edi, dword ptr [ebp - 0x18] ; 0x0089a45d: test edi, edi ; 0x0089a45f: je 0x89a4bc
  - 0x0089a761: je -> 0x0089a96a (jcc_true) | ctx: 0x0089a75a: cmp dword ptr [ebx + 0x98], -1 ; 0x0089a761: je 0x89a96a
  - 0x0089a761: je -> 0x0089a767 (jcc_false) | ctx: 0x0089a75a: cmp dword ptr [ebx + 0x98], -1 ; 0x0089a761: je 0x89a96a
  - 0x0089a579: je -> 0x0089a5e3 (jcc_true) | ctx: 0x0089a571: mov dword ptr [ebp + 0xc], esi ; 0x0089a574: mov dword ptr [ebp + 0xc], esi ; 0x0089a577: test esi, esi ; 0x0089a579: je 0x89a5e3
  - 0x0089a579: je -> 0x0089a57b (jcc_false) | ctx: 0x0089a571: mov dword ptr [ebp + 0xc], esi ; 0x0089a574: mov dword ptr [ebp + 0xc], esi ; 0x0089a577: test esi, esi ; 0x0089a579: je 0x89a5e3
  - 0x0089a4ba: jmp -> 0x0089a4be (jmp) | ctx: 0x0089a4aa: mov dword ptr [edi + 0x2c], eax ; 0x0089a4ad: mov dword ptr [edi], 0xc1d610 ; 0x0089a4b3: mov dword ptr [edi + 0x30], 0xffffffff ; 0x0089a4ba: jmp 0x89a4be
  - 0x0089a995: je -> 0x0089a9a0 (jcc_true) | ctx: 0x0089a989: mov dword ptr [ebp - 0x18], ecx ; 0x0089a98c: mov dword ptr [ebp - 4], 8 ; 0x0089a993: test ecx, ecx ; 0x0089a995: je 0x89a9a0
  - 0x0089a995: je -> 0x0089a997 (jcc_false) | ctx: 0x0089a989: mov dword ptr [ebp - 0x18], ecx ; 0x0089a98c: mov dword ptr [ebp - 4], 8 ; 0x0089a993: test ecx, ecx ; 0x0089a995: je 0x89a9a0
  - 0x0089a78b: je -> 0x0089a7f5 (jcc_true) | ctx: 0x0089a783: mov dword ptr [ebp + 0xc], esi ; 0x0089a786: mov dword ptr [ebp + 0xc], esi ; 0x0089a789: test esi, esi ; 0x0089a78b: je 0x89a7f5
  - 0x0089a78b: je -> 0x0089a78d (jcc_false) | ctx: 0x0089a783: mov dword ptr [ebp + 0xc], esi ; 0x0089a786: mov dword ptr [ebp + 0xc], esi ; 0x0089a789: test esi, esi ; 0x0089a78b: je 0x89a7f5
  - 0x0089a60e: jne -> 0x0089a614 (jcc_true) | ctx: 0x0089a600: mov dword ptr [ebp - 0x2c], 0 ; 0x0089a607: mov byte ptr [ebp - 0x3c], 0 ; 0x0089a60b: cmp byte ptr [edx], 0 ; 0x0089a60e: jne 0x89a614
  - 0x0089a60e: jne -> 0x0089a610 (jcc_false) | ctx: 0x0089a600: mov dword ptr [ebp - 0x2c], 0 ; 0x0089a607: mov byte ptr [ebp - 0x3c], 0 ; 0x0089a60b: cmp byte ptr [edx], 0 ; 0x0089a60e: jne 0x89a614
  - 0x0089a5d3: jb -> 0x0089a5d7 (jcc_true) | ctx: 0x0089a5c1: mov dword ptr [eax + 0x14], 0xf ; 0x0089a5c8: cmp dword ptr [eax + 0x14], 0x10 ; 0x0089a5cc: mov dword ptr [eax + 0x10], 0 ; 0x0089a5d3: jb 0x89a5d7
  - 0x0089a5d3: jb -> 0x0089a5d5 (jcc_false) | ctx: 0x0089a5c1: mov dword ptr [eax + 0x14], 0xf ; 0x0089a5c8: cmp dword ptr [eax + 0x14], 0x10 ; 0x0089a5cc: mov dword ptr [eax + 0x10], 0 ; 0x0089a5d3: jb 0x89a5d7
  - 0x0089a9cb: jne -> 0x0089a9d1 (jcc_true) | ctx: 0x0089a9bd: mov dword ptr [ebp - 0x5c], 0 ; 0x0089a9c4: mov byte ptr [ebp - 0x6c], 0 ; 0x0089a9c8: cmp byte ptr [edx], 0 ; 0x0089a9cb: jne 0x89a9d1
  - 0x0089a9cb: jne -> 0x0089a9cd (jcc_false) | ctx: 0x0089a9bd: mov dword ptr [ebp - 0x5c], 0 ; 0x0089a9c4: mov byte ptr [ebp - 0x6c], 0 ; 0x0089a9c8: cmp byte ptr [edx], 0 ; 0x0089a9cb: jne 0x89a9d1
  - 0x0089a99e: jmp -> 0x0089a9a2 (jmp) | ctx: 0x0089a997: call 0x881220 ; 0x0089a99c: mov esi, eax ; 0x0089a99e: jmp 0x89a9a2
  - 0x0089a820: jne -> 0x0089a826 (jcc_true) | ctx: 0x0089a812: mov dword ptr [ebp - 0x44], 0 ; 0x0089a819: mov byte ptr [ebp - 0x54], 0 ; 0x0089a81d: cmp byte ptr [edx], 0 ; 0x0089a820: jne 0x89a826
  - 0x0089a820: jne -> 0x0089a822 (jcc_false) | ctx: 0x0089a812: mov dword ptr [ebp - 0x44], 0 ; 0x0089a819: mov byte ptr [ebp - 0x54], 0 ; 0x0089a81d: cmp byte ptr [edx], 0 ; 0x0089a820: jne 0x89a826
  - 0x0089a7e5: jb -> 0x0089a7e9 (jcc_true) | ctx: 0x0089a7d3: mov dword ptr [eax + 0x14], 0xf ; 0x0089a7da: cmp dword ptr [eax + 0x14], 0x10 ; 0x0089a7de: mov dword ptr [eax + 0x10], 0 ; 0x0089a7e5: jb 0x89a7e9
  - 0x0089a7e5: jb -> 0x0089a7e7 (jcc_false) | ctx: 0x0089a7d3: mov dword ptr [eax + 0x14], 0xf ; 0x0089a7da: cmp dword ptr [eax + 0x14], 0x10 ; 0x0089a7de: mov dword ptr [eax + 0x10], 0 ; 0x0089a7e5: jb 0x89a7e9
  - 0x0089a625: jne -> 0x0089a620 (jcc_true) | ctx: 0x0089a620: mov al, byte ptr [ecx] ; 0x0089a622: inc ecx ; 0x0089a623: test al, al ; 0x0089a625: jne 0x89a620
  - 0x0089a625: jne -> 0x0089a627 (jcc_false) | ctx: 0x0089a620: mov al, byte ptr [ecx] ; 0x0089a622: inc ecx ; 0x0089a623: test al, al ; 0x0089a625: jne 0x89a620
  - 0x0089a612: jmp -> 0x0089a62a (jmp) | ctx: 0x0089a610: xor ecx, ecx ; 0x0089a612: jmp 0x89a62a
  - 0x0089a5e1: jmp -> 0x0089a5e5 (jmp) | ctx: 0x0089a5d7: mov byte ptr [eax], 0 ; 0x0089a5da: mov dword ptr [esi + 0x40], 0xffffffff ; 0x0089a5e1: jmp 0x89a5e5
  - 0x0089a5e1: jmp -> 0x0089a5e5 (jmp) | ctx: 0x0089a5d5: mov eax, dword ptr [eax] ; 0x0089a5d7: mov byte ptr [eax], 0 ; 0x0089a5da: mov dword ptr [esi + 0x40], 0xffffffff ; 0x0089a5e1: jmp 0x89a5e5
  - 0x0089a9e5: jne -> 0x0089a9e0 (jcc_true) | ctx: 0x0089a9e0: mov al, byte ptr [ecx] ; 0x0089a9e2: inc ecx ; 0x0089a9e3: test al, al ; 0x0089a9e5: jne 0x89a9e0
  - 0x0089a9e5: jne -> 0x0089a9e7 (jcc_false) | ctx: 0x0089a9e0: mov al, byte ptr [ecx] ; 0x0089a9e2: inc ecx ; 0x0089a9e3: test al, al ; 0x0089a9e5: jne 0x89a9e0
  - 0x0089a9cf: jmp -> 0x0089a9ea (jmp) | ctx: 0x0089a9cd: xor ecx, ecx ; 0x0089a9cf: jmp 0x89a9ea
  - 0x0089a9cb: jne -> 0x0089a9d1 (jcc_true) | ctx: 0x0089a9bd: mov dword ptr [ebp - 0x5c], 0 ; 0x0089a9c4: mov byte ptr [ebp - 0x6c], 0 ; 0x0089a9c8: cmp byte ptr [edx], 0 ; 0x0089a9cb: jne 0x89a9d1
  - 0x0089a9cb: jne -> 0x0089a9cd (jcc_false) | ctx: 0x0089a9bd: mov dword ptr [ebp - 0x5c], 0 ; 0x0089a9c4: mov byte ptr [ebp - 0x6c], 0 ; 0x0089a9c8: cmp byte ptr [edx], 0 ; 0x0089a9cb: jne 0x89a9d1
  - 0x0089a835: jne -> 0x0089a830 (jcc_true) | ctx: 0x0089a830: mov al, byte ptr [ecx] ; 0x0089a832: inc ecx ; 0x0089a833: test al, al ; 0x0089a835: jne 0x89a830
  - 0x0089a835: jne -> 0x0089a837 (jcc_false) | ctx: 0x0089a830: mov al, byte ptr [ecx] ; 0x0089a832: inc ecx ; 0x0089a833: test al, al ; 0x0089a835: jne 0x89a830
  - 0x0089a824: jmp -> 0x0089a83a (jmp) | ctx: 0x0089a822: xor ecx, ecx ; 0x0089a824: jmp 0x89a83a
  - 0x0089a7f3: jmp -> 0x0089a7f7 (jmp) | ctx: 0x0089a7e9: mov byte ptr [eax], 0 ; 0x0089a7ec: mov dword ptr [esi + 0x40], 0xffffffff ; 0x0089a7f3: jmp 0x89a7f7
  - 0x0089a7f3: jmp -> 0x0089a7f7 (jmp) | ctx: 0x0089a7e7: mov eax, dword ptr [eax] ; 0x0089a7e9: mov byte ptr [eax], 0 ; 0x0089a7ec: mov dword ptr [esi + 0x40], 0xffffffff ; 0x0089a7f3: jmp 0x89a7f7
  - 0x0089a625: jne -> 0x0089a620 (jcc_true) | ctx: 0x0089a620: mov al, byte ptr [ecx] ; 0x0089a622: inc ecx ; 0x0089a623: test al, al ; 0x0089a625: jne 0x89a620
  - 0x0089a625: jne -> 0x0089a627 (jcc_false) | ctx: 0x0089a620: mov al, byte ptr [ecx] ; 0x0089a622: inc ecx ; 0x0089a623: test al, al ; 0x0089a625: jne 0x89a620
  - 0x0089a671: je -> 0x0089a67d (jcc_true) | ctx: 0x0089a669: mov dword ptr [esi + 0x20], eax ; 0x0089a66c: lea eax, [ebp - 0x3c] ; 0x0089a66f: cmp ecx, eax ; 0x0089a671: je 0x89a67d
  - 0x0089a671: je -> 0x0089a673 (jcc_false) | ctx: 0x0089a669: mov dword ptr [esi + 0x20], eax ; 0x0089a66c: lea eax, [ebp - 0x3c] ; 0x0089a66f: cmp ecx, eax ; 0x0089a671: je 0x89a67d
  - 0x0089a671: je -> 0x0089a67d (jcc_true) | ctx: 0x0089a669: mov dword ptr [esi + 0x20], eax ; 0x0089a66c: lea eax, [ebp - 0x3c] ; 0x0089a66f: cmp ecx, eax ; 0x0089a671: je 0x89a67d
  - 0x0089a671: je -> 0x0089a673 (jcc_false) | ctx: 0x0089a669: mov dword ptr [esi + 0x20], eax ; 0x0089a66c: lea eax, [ebp - 0x3c] ; 0x0089a66f: cmp ecx, eax ; 0x0089a671: je 0x89a67d
  - 0x0089a60e: jne -> 0x0089a614 (jcc_true) | ctx: 0x0089a600: mov dword ptr [ebp - 0x2c], 0 ; 0x0089a607: mov byte ptr [ebp - 0x3c], 0 ; 0x0089a60b: cmp byte ptr [edx], 0 ; 0x0089a60e: jne 0x89a614
  - 0x0089a60e: jne -> 0x0089a610 (jcc_false) | ctx: 0x0089a600: mov dword ptr [ebp - 0x2c], 0 ; 0x0089a607: mov byte ptr [ebp - 0x3c], 0 ; 0x0089a60b: cmp byte ptr [edx], 0 ; 0x0089a60e: jne 0x89a614
  - 0x0089a9e5: jne -> 0x0089a9e0 (jcc_true) | ctx: 0x0089a9e0: mov al, byte ptr [ecx] ; 0x0089a9e2: inc ecx ; 0x0089a9e3: test al, al ; 0x0089a9e5: jne 0x89a9e0
  - 0x0089a9e5: jne -> 0x0089a9e7 (jcc_false) | ctx: 0x0089a9e0: mov al, byte ptr [ecx] ; 0x0089a9e2: inc ecx ; 0x0089a9e3: test al, al ; 0x0089a9e5: jne 0x89a9e0
  - 0x0089aa31: je -> 0x0089aa3d (jcc_true) | ctx: 0x0089aa29: mov dword ptr [esi + 0x20], eax ; 0x0089aa2c: lea eax, [ebp - 0x6c] ; 0x0089aa2f: cmp ecx, eax ; 0x0089aa31: je 0x89aa3d
  - 0x0089aa31: je -> 0x0089aa33 (jcc_false) | ctx: 0x0089aa29: mov dword ptr [esi + 0x20], eax ; 0x0089aa2c: lea eax, [ebp - 0x6c] ; 0x0089aa2f: cmp ecx, eax ; 0x0089aa31: je 0x89aa3d
  - 0x0089aa31: je -> 0x0089aa3d (jcc_true) | ctx: 0x0089aa29: mov dword ptr [esi + 0x20], eax ; 0x0089aa2c: lea eax, [ebp - 0x6c] ; 0x0089aa2f: cmp ecx, eax ; 0x0089aa31: je 0x89aa3d
  - 0x0089aa31: je -> 0x0089aa33 (jcc_false) | ctx: 0x0089aa29: mov dword ptr [esi + 0x20], eax ; 0x0089aa2c: lea eax, [ebp - 0x6c] ; 0x0089aa2f: cmp ecx, eax ; 0x0089aa31: je 0x89aa3d
  - 0x0089a835: jne -> 0x0089a830 (jcc_true) | ctx: 0x0089a830: mov al, byte ptr [ecx] ; 0x0089a832: inc ecx ; 0x0089a833: test al, al ; 0x0089a835: jne 0x89a830
  - 0x0089a835: jne -> 0x0089a837 (jcc_false) | ctx: 0x0089a830: mov al, byte ptr [ecx] ; 0x0089a832: inc ecx ; 0x0089a833: test al, al ; 0x0089a835: jne 0x89a830
  - 0x0089a881: je -> 0x0089a88d (jcc_true) | ctx: 0x0089a879: mov dword ptr [esi + 0x20], eax ; 0x0089a87c: lea eax, [ebp - 0x54] ; 0x0089a87f: cmp ecx, eax ; 0x0089a881: je 0x89a88d
  - 0x0089a881: je -> 0x0089a883 (jcc_false) | ctx: 0x0089a879: mov dword ptr [esi + 0x20], eax ; 0x0089a87c: lea eax, [ebp - 0x54] ; 0x0089a87f: cmp ecx, eax ; 0x0089a881: je 0x89a88d
  - 0x0089a881: je -> 0x0089a88d (jcc_true) | ctx: 0x0089a879: mov dword ptr [esi + 0x20], eax ; 0x0089a87c: lea eax, [ebp - 0x54] ; 0x0089a87f: cmp ecx, eax ; 0x0089a881: je 0x89a88d
  - 0x0089a881: je -> 0x0089a883 (jcc_false) | ctx: 0x0089a879: mov dword ptr [esi + 0x20], eax ; 0x0089a87c: lea eax, [ebp - 0x54] ; 0x0089a87f: cmp ecx, eax ; 0x0089a881: je 0x89a88d
  - ... 39 more

### 0x0089ab50
- blocks=31, insns=368, edges=80, jcc=24, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0089acdc)
  - caller_of_anchor_path: depth 2 (calls 0x005c5400 at 0x0089ae7d)
- branch points:
  - 0x0089ab89: jne -> 0x0089aba4 (jcc_true) | ctx: 0x0089ab7f: mov dword ptr [ebp - 0x10], edi ; 0x0089ab82: mov esi, dword ptr [edx + 4] ; 0x0089ab85: cmp byte ptr [esi + 0xd], 0 ; 0x0089ab89: jne 0x89aba4
  - 0x0089ab89: jne -> 0x0089ab8b (jcc_false) | ctx: 0x0089ab7f: mov dword ptr [ebp - 0x10], edi ; 0x0089ab82: mov esi, dword ptr [edx + 4] ; 0x0089ab85: cmp byte ptr [esi + 0xd], 0 ; 0x0089ab89: jne 0x89aba4
  - 0x0089aba6: je -> 0x0089abad (jcc_true) | ctx: 0x0089aba4: cmp eax, edx ; 0x0089aba6: je 0x89abad
  - 0x0089aba6: je -> 0x0089aba8 (jcc_false) | ctx: 0x0089aba4: cmp eax, edx ; 0x0089aba6: je 0x89abad
  - 0x0089ab93: jae -> 0x0089ab9a (jcc_true) | ctx: 0x0089ab8b: nop dword ptr [eax + eax] ; 0x0089ab90: cmp dword ptr [esi + 0x10], edi ; 0x0089ab93: jae 0x89ab9a
  - 0x0089ab93: jae -> 0x0089ab95 (jcc_false) | ctx: 0x0089ab8b: nop dword ptr [eax + eax] ; 0x0089ab90: cmp dword ptr [esi + 0x10], edi ; 0x0089ab93: jae 0x89ab9a
  - 0x0089abb1: je -> 0x0089ade8 (jcc_true) | ctx: 0x0089abad: mov eax, edx ; 0x0089abaf: cmp eax, edx ; 0x0089abb1: je 0x89ade8
  - 0x0089abb1: je -> 0x0089abb7 (jcc_false) | ctx: 0x0089abad: mov eax, edx ; 0x0089abaf: cmp eax, edx ; 0x0089abb1: je 0x89ade8
  - 0x0089abab: jae -> 0x0089abaf (jcc_true) | ctx: 0x0089aba8: cmp edi, dword ptr [eax + 0x10] ; 0x0089abab: jae 0x89abaf
  - 0x0089abab: jae -> 0x0089abad (jcc_false) | ctx: 0x0089aba8: cmp edi, dword ptr [eax + 0x10] ; 0x0089abab: jae 0x89abaf
  - 0x0089aba2: je -> 0x0089ab90 (jcc_true) | ctx: 0x0089ab9a: mov eax, esi ; 0x0089ab9c: mov esi, dword ptr [esi] ; 0x0089ab9e: cmp byte ptr [esi + 0xd], 0 ; 0x0089aba2: je 0x89ab90
  - 0x0089aba2: je -> 0x0089aba4 (jcc_false) | ctx: 0x0089ab9a: mov eax, esi ; 0x0089ab9c: mov esi, dword ptr [esi] ; 0x0089ab9e: cmp byte ptr [esi + 0xd], 0 ; 0x0089aba2: je 0x89ab90
  - 0x0089ab98: jmp -> 0x0089ab9e (jmp) | ctx: 0x0089ab95: mov esi, dword ptr [esi + 8] ; 0x0089ab98: jmp 0x89ab9e
  - 0x0089ae92: jb -> 0x0089ae9f (jcc_true) | ctx: 0x0089ae87: mov dword ptr [ebp - 0x64], eax ; 0x0089ae8a: cmp dword ptr [ebp - 0x44], 0x10 ; 0x0089ae8e: mov byte ptr [ebp - 4], 2 ; 0x0089ae92: jb 0x89ae9f
  - 0x0089ae92: jb -> 0x0089ae94 (jcc_false) | ctx: 0x0089ae87: mov dword ptr [ebp - 0x64], eax ; 0x0089ae8a: cmp dword ptr [ebp - 0x44], 0x10 ; 0x0089ae8e: mov byte ptr [ebp - 4], 2 ; 0x0089ae92: jb 0x89ae9f
  - 0x0089abbc: je -> 0x0089ade8 (jcc_true) | ctx: 0x0089abb7: mov esi, dword ptr [eax + 0x14] ; 0x0089abba: test esi, esi ; 0x0089abbc: je 0x89ade8
  - 0x0089abbc: je -> 0x0089abc2 (jcc_false) | ctx: 0x0089abb7: mov esi, dword ptr [eax + 0x14] ; 0x0089abba: test esi, esi ; 0x0089abbc: je 0x89ade8
  - 0x0089abb1: je -> 0x0089ade8 (jcc_true) | ctx: 0x0089abaf: cmp eax, edx ; 0x0089abb1: je 0x89ade8
  - 0x0089abb1: je -> 0x0089abb7 (jcc_false) | ctx: 0x0089abaf: cmp eax, edx ; 0x0089abb1: je 0x89ade8
  - 0x0089ab93: jae -> 0x0089ab9a (jcc_true) | ctx: 0x0089ab90: cmp dword ptr [esi + 0x10], edi ; 0x0089ab93: jae 0x89ab9a
  - 0x0089ab93: jae -> 0x0089ab95 (jcc_false) | ctx: 0x0089ab90: cmp dword ptr [esi + 0x10], edi ; 0x0089ab93: jae 0x89ab9a
  - 0x0089aba2: je -> 0x0089ab90 (jcc_true) | ctx: 0x0089ab9e: cmp byte ptr [esi + 0xd], 0 ; 0x0089aba2: je 0x89ab90
  - 0x0089aba2: je -> 0x0089aba4 (jcc_false) | ctx: 0x0089ab9e: cmp byte ptr [esi + 0xd], 0 ; 0x0089aba2: je 0x89ab90
  - 0x0089aee7: jb -> 0x0089aef4 (jcc_true) | ctx: 0x0089aed9: mov dword ptr [esi + 4], eax ; 0x0089aedc: mov dword ptr [ebp - 4], 3 ; 0x0089aee3: cmp dword ptr [ebp - 0x68], 0x10 ; 0x0089aee7: jb 0x89aef4
  - 0x0089aee7: jb -> 0x0089aee9 (jcc_false) | ctx: 0x0089aed9: mov dword ptr [esi + 4], eax ; 0x0089aedc: mov dword ptr [ebp - 4], 3 ; 0x0089aee3: cmp dword ptr [ebp - 0x68], 0x10 ; 0x0089aee7: jb 0x89aef4
  - 0x0089aee7: jb -> 0x0089aef4 (jcc_true) | ctx: 0x0089aed9: mov dword ptr [esi + 4], eax ; 0x0089aedc: mov dword ptr [ebp - 4], 3 ; 0x0089aee3: cmp dword ptr [ebp - 0x68], 0x10 ; 0x0089aee7: jb 0x89aef4
  - 0x0089aee7: jb -> 0x0089aee9 (jcc_false) | ctx: 0x0089aed9: mov dword ptr [esi + 4], eax ; 0x0089aedc: mov dword ptr [ebp - 4], 3 ; 0x0089aee3: cmp dword ptr [ebp - 0x68], 0x10 ; 0x0089aee7: jb 0x89aef4
  - 0x0089abdc: jb -> 0x0089abe0 (jcc_true) | ctx: 0x0089abd0: call 0x86cbb0 ; 0x0089abd5: cmp dword ptr [ebx + 0x40], 0x10 ; 0x0089abd9: lea edx, [ebx + 0x2c] ; 0x0089abdc: jb 0x89abe0
  - 0x0089abdc: jb -> 0x0089abde (jcc_false) | ctx: 0x0089abd0: call 0x86cbb0 ; 0x0089abd5: cmp dword ptr [ebx + 0x40], 0x10 ; 0x0089abd9: lea edx, [ebx + 0x2c] ; 0x0089abdc: jb 0x89abe0
  - 0x0089abf5: jne -> 0x0089abfb (jcc_true) | ctx: 0x0089abe7: mov dword ptr [ebp - 0x30], 0 ; 0x0089abee: mov byte ptr [ebp - 0x40], 0 ; 0x0089abf2: cmp byte ptr [edx], 0 ; 0x0089abf5: jne 0x89abfb
  - 0x0089abf5: jne -> 0x0089abf7 (jcc_false) | ctx: 0x0089abe7: mov dword ptr [ebp - 0x30], 0 ; 0x0089abee: mov byte ptr [ebp - 0x40], 0 ; 0x0089abf2: cmp byte ptr [edx], 0 ; 0x0089abf5: jne 0x89abfb
  - 0x0089abf5: jne -> 0x0089abfb (jcc_true) | ctx: 0x0089abe7: mov dword ptr [ebp - 0x30], 0 ; 0x0089abee: mov byte ptr [ebp - 0x40], 0 ; 0x0089abf2: cmp byte ptr [edx], 0 ; 0x0089abf5: jne 0x89abfb
  - 0x0089abf5: jne -> 0x0089abf7 (jcc_false) | ctx: 0x0089abe7: mov dword ptr [ebp - 0x30], 0 ; 0x0089abee: mov byte ptr [ebp - 0x40], 0 ; 0x0089abf2: cmp byte ptr [edx], 0 ; 0x0089abf5: jne 0x89abfb
  - 0x0089ac05: jne -> 0x0089ac00 (jcc_true) | ctx: 0x0089ac00: mov al, byte ptr [ecx] ; 0x0089ac02: inc ecx ; 0x0089ac03: test al, al ; 0x0089ac05: jne 0x89ac00
  - 0x0089ac05: jne -> 0x0089ac07 (jcc_false) | ctx: 0x0089ac00: mov al, byte ptr [ecx] ; 0x0089ac02: inc ecx ; 0x0089ac03: test al, al ; 0x0089ac05: jne 0x89ac00
  - 0x0089abf9: jmp -> 0x0089ac09 (jmp) | ctx: 0x0089abf7: xor ecx, ecx ; 0x0089abf9: jmp 0x89ac09
  - 0x0089ac05: jne -> 0x0089ac00 (jcc_true) | ctx: 0x0089ac00: mov al, byte ptr [ecx] ; 0x0089ac02: inc ecx ; 0x0089ac03: test al, al ; 0x0089ac05: jne 0x89ac00
  - 0x0089ac05: jne -> 0x0089ac07 (jcc_false) | ctx: 0x0089ac00: mov al, byte ptr [ecx] ; 0x0089ac02: inc ecx ; 0x0089ac03: test al, al ; 0x0089ac05: jne 0x89ac00
  - 0x0089ac3f: jb -> 0x0089ac4c (jcc_true) | ctx: 0x0089ac2f: call 0x890620 ; 0x0089ac34: cmp dword ptr [ebp - 0x2c], 0x10 ; 0x0089ac38: mov dword ptr [ebp - 4], 5 ; 0x0089ac3f: jb 0x89ac4c
  - 0x0089ac3f: jb -> 0x0089ac41 (jcc_false) | ctx: 0x0089ac2f: call 0x890620 ; 0x0089ac34: cmp dword ptr [ebp - 0x2c], 0x10 ; 0x0089ac38: mov dword ptr [ebp - 4], 5 ; 0x0089ac3f: jb 0x89ac4c
  - 0x0089ac3f: jb -> 0x0089ac4c (jcc_true) | ctx: 0x0089ac2f: call 0x890620 ; 0x0089ac34: cmp dword ptr [ebp - 0x2c], 0x10 ; 0x0089ac38: mov dword ptr [ebp - 4], 5 ; 0x0089ac3f: jb 0x89ac4c
  - 0x0089ac3f: jb -> 0x0089ac41 (jcc_false) | ctx: 0x0089ac2f: call 0x890620 ; 0x0089ac34: cmp dword ptr [ebp - 0x2c], 0x10 ; 0x0089ac38: mov dword ptr [ebp - 4], 5 ; 0x0089ac3f: jb 0x89ac4c
  - 0x0089ac5d: jns -> 0x0089ad4d (jcc_true) | ctx: 0x0089ac4f: mov dword ptr [ebp - 4], 0xffffffff ; 0x0089ac56: call 0x61d7f0 ; 0x0089ac5b: test eax, eax ; 0x0089ac5d: jns 0x89ad4d
  - 0x0089ac5d: jns -> 0x0089ac63 (jcc_false) | ctx: 0x0089ac4f: mov dword ptr [ebp - 4], 0xffffffff ; 0x0089ac56: call 0x61d7f0 ; 0x0089ac5b: test eax, eax ; 0x0089ac5d: jns 0x89ad4d
  - 0x0089ac5d: jns -> 0x0089ad4d (jcc_true) | ctx: 0x0089ac4f: mov dword ptr [ebp - 4], 0xffffffff ; 0x0089ac56: call 0x61d7f0 ; 0x0089ac5b: test eax, eax ; 0x0089ac5d: jns 0x89ad4d
  - 0x0089ac5d: jns -> 0x0089ac63 (jcc_false) | ctx: 0x0089ac4f: mov dword ptr [ebp - 4], 0xffffffff ; 0x0089ac56: call 0x61d7f0 ; 0x0089ac5b: test eax, eax ; 0x0089ac5d: jns 0x89ad4d
  - 0x0089ade3: jmp -> 0x0089aef4 (jmp) | ctx: 0x0089add1: mov dword ptr [esi], 2 ; 0x0089add7: mov dword ptr [esi + 4], 0 ; 0x0089adde: call 0x883d80 ; 0x0089ade3: jmp 0x89aef4
  - 0x0089acf4: jb -> 0x0089ad04 (jcc_true) | ctx: 0x0089ace6: mov dword ptr [ebp - 0x64], eax ; 0x0089ace9: cmp dword ptr [ebp - 0xbc], 0x10 ; 0x0089acf0: mov byte ptr [ebp - 4], 8 ; 0x0089acf4: jb 0x89ad04
  - 0x0089acf4: jb -> 0x0089acf6 (jcc_false) | ctx: 0x0089ace6: mov dword ptr [ebp - 0x64], eax ; 0x0089ace9: cmp dword ptr [ebp - 0xbc], 0x10 ; 0x0089acf0: mov byte ptr [ebp - 4], 8 ; 0x0089acf4: jb 0x89ad04
  - 0x0089ad48: jmp -> 0x0089aee3 (jmp) | ctx: 0x0089ad3b: mov eax, dword ptr [ebp - 0x24] ; 0x0089ad3e: mov dword ptr [esi + 4], eax ; 0x0089ad41: mov dword ptr [ebp - 4], 9 ; 0x0089ad48: jmp 0x89aee3
  - 0x0089ad48: jmp -> 0x0089aee3 (jmp) | ctx: 0x0089ad3b: mov eax, dword ptr [ebp - 0x24] ; 0x0089ad3e: mov dword ptr [esi + 4], eax ; 0x0089ad41: mov dword ptr [ebp - 4], 9 ; 0x0089ad48: jmp 0x89aee3
  - 0x0089aee7: jb -> 0x0089aef4 (jcc_true) | ctx: 0x0089aee3: cmp dword ptr [ebp - 0x68], 0x10 ; 0x0089aee7: jb 0x89aef4
  - 0x0089aee7: jb -> 0x0089aee9 (jcc_false) | ctx: 0x0089aee3: cmp dword ptr [ebp - 0x68], 0x10 ; 0x0089aee7: jb 0x89aef4

### 0x008e46d0
- blocks=8, insns=52, edges=13, jcc=4, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x004f74f0 at 0x008e472f)
- branch points:
  - 0x008e46ee: jae -> 0x008e46f5 (jcc_true) | ctx: 0x008e46e3: mov ecx, eax ; 0x008e46e5: mov eax, dword ptr [edi + 0x554] ; 0x008e46eb: cmp esi, dword ptr [eax + 0xc] ; 0x008e46ee: jae 0x8e46f5
  - 0x008e46ee: jae -> 0x008e46f0 (jcc_false) | ctx: 0x008e46e3: mov ecx, eax ; 0x008e46e5: mov eax, dword ptr [edi + 0x554] ; 0x008e46eb: cmp esi, dword ptr [eax + 0xc] ; 0x008e46ee: jae 0x8e46f5
  - 0x008e46f7: jne -> 0x008e4736 (jcc_true) | ctx: 0x008e46f5: test ecx, ecx ; 0x008e46f7: jne 0x8e4736
  - 0x008e46f7: jne -> 0x008e46f9 (jcc_false) | ctx: 0x008e46f5: test ecx, ecx ; 0x008e46f7: jne 0x8e4736
  - 0x008e46f7: jne -> 0x008e4736 (jcc_true) | ctx: 0x008e46f0: mov byte ptr [eax + esi + 0x10], 0 ; 0x008e46f5: test ecx, ecx ; 0x008e46f7: jne 0x8e4736
  - 0x008e46f7: jne -> 0x008e46f9 (jcc_false) | ctx: 0x008e46f0: mov byte ptr [eax + esi + 0x10], 0 ; 0x008e46f5: test ecx, ecx ; 0x008e46f7: jne 0x8e4736
  - 0x008e4718: je -> 0x008e4722 (jcc_true) | ctx: 0x008e4711: test eax, eax ; 0x008e4713: mov dword ptr [ecx], eax ; 0x008e4715: mov eax, dword ptr [ebp + 0x20] ; 0x008e4718: je 0x8e4722
  - 0x008e4718: je -> 0x008e471a (jcc_false) | ctx: 0x008e4711: test eax, eax ; 0x008e4713: mov dword ptr [ecx], eax ; 0x008e4715: mov eax, dword ptr [ebp + 0x20] ; 0x008e4718: je 0x8e4722
  - 0x008e4734: jmp -> 0x008e473b (jmp) | ctx: 0x008e4723: lea ecx, [edi + 0x108] ; 0x008e4729: mov dword ptr [eax], 1 ; 0x008e472f: call 0x4f7500 ; 0x008e4734: jmp 0x8e473b
  - 0x008e4720: jmp -> 0x008e473b (jmp) | ctx: 0x008e471a: mov dword ptr [eax], 0 ; 0x008e4720: jmp 0x8e473b

### 0x008e6903
- blocks=28, insns=176, edges=56, jcc=18, indirect_jmp=0, truncated=False
- reasons:
  - caller_of_anchor_path: depth 1 (calls 0x008ecf90 at 0x008e6a3a)
- branch points:
  - 0x008e690d: je -> 0x008e6924 (jcc_true) | ctx: 0x008e6904: mov edi, ecx ; 0x008e6906: mov eax, dword ptr [edi + 0x20] ; 0x008e6909: cmp dword ptr [eax + 4], 3 ; 0x008e690d: je 0x8e6924
  - 0x008e690d: je -> 0x008e690f (jcc_false) | ctx: 0x008e6904: mov edi, ecx ; 0x008e6906: mov eax, dword ptr [edi + 0x20] ; 0x008e6909: cmp dword ptr [eax + 4], 3 ; 0x008e690d: je 0x8e6924
  - 0x008e692b: jne -> 0x008e6934 (jcc_true) | ctx: 0x008e6924: cmp dword ptr [0xf8bc48], 0 ; 0x008e692b: jne 0x8e6934
  - 0x008e692b: jne -> 0x008e692d (jcc_false) | ctx: 0x008e6924: cmp dword ptr [0xf8bc48], 0 ; 0x008e692b: jne 0x8e6934
  - 0x008e6943: jb -> 0x008e6964 (jcc_true) | ctx: 0x008e693a: mov eax, dword ptr [esi] ; 0x008e693c: call dword ptr [eax + 4] ; 0x008e693f: cmp dword ptr [eax + 8], 3 ; 0x008e6943: jb 0x8e6964
  - 0x008e6943: jb -> 0x008e6945 (jcc_false) | ctx: 0x008e693a: mov eax, dword ptr [esi] ; 0x008e693c: call dword ptr [eax + 4] ; 0x008e693f: cmp dword ptr [eax + 8], 3 ; 0x008e6943: jb 0x8e6964
  - 0x008e6943: jb -> 0x008e6964 (jcc_true) | ctx: 0x008e693a: mov eax, dword ptr [esi] ; 0x008e693c: call dword ptr [eax + 4] ; 0x008e693f: cmp dword ptr [eax + 8], 3 ; 0x008e6943: jb 0x8e6964
  - 0x008e6943: jb -> 0x008e6945 (jcc_false) | ctx: 0x008e693a: mov eax, dword ptr [esi] ; 0x008e693c: call dword ptr [eax + 4] ; 0x008e693f: cmp dword ptr [eax + 8], 3 ; 0x008e6943: jb 0x8e6964
  - 0x008e696b: jne -> 0x008e6974 (jcc_true) | ctx: 0x008e6964: cmp dword ptr [0xf8bc6c], 0 ; 0x008e696b: jne 0x8e6974
  - 0x008e696b: jne -> 0x008e696d (jcc_false) | ctx: 0x008e6964: cmp dword ptr [0xf8bc6c], 0 ; 0x008e696b: jne 0x8e6974
  - 0x008e694e: jne -> 0x008e6964 (jcc_true) | ctx: 0x008e6945: mov eax, dword ptr [eax + 0x14] ; 0x008e6948: cmp eax, dword ptr [0xf8bc5c] ; 0x008e694e: jne 0x8e6964
  - 0x008e694e: jne -> 0x008e6950 (jcc_false) | ctx: 0x008e6945: mov eax, dword ptr [eax + 0x14] ; 0x008e6948: cmp eax, dword ptr [0xf8bc5c] ; 0x008e694e: jne 0x8e6964
  - 0x008e697f: jb -> 0x008e69a0 (jcc_true) | ctx: 0x008e6976: mov ecx, esi ; 0x008e6978: call dword ptr [eax + 4] ; 0x008e697b: cmp dword ptr [eax + 8], 3 ; 0x008e697f: jb 0x8e69a0
  - 0x008e697f: jb -> 0x008e6981 (jcc_false) | ctx: 0x008e6976: mov ecx, esi ; 0x008e6978: call dword ptr [eax + 4] ; 0x008e697b: cmp dword ptr [eax + 8], 3 ; 0x008e697f: jb 0x8e69a0
  - 0x008e697f: jb -> 0x008e69a0 (jcc_true) | ctx: 0x008e6976: mov ecx, esi ; 0x008e6978: call dword ptr [eax + 4] ; 0x008e697b: cmp dword ptr [eax + 8], 3 ; 0x008e697f: jb 0x8e69a0
  - 0x008e697f: jb -> 0x008e6981 (jcc_false) | ctx: 0x008e6976: mov ecx, esi ; 0x008e6978: call dword ptr [eax + 4] ; 0x008e697b: cmp dword ptr [eax + 8], 3 ; 0x008e697f: jb 0x8e69a0
  - 0x008e69a7: jne -> 0x008e69b0 (jcc_true) | ctx: 0x008e69a0: cmp dword ptr [0xf8d824], 0 ; 0x008e69a7: jne 0x8e69b0
  - 0x008e69a7: jne -> 0x008e69a9 (jcc_false) | ctx: 0x008e69a0: cmp dword ptr [0xf8d824], 0 ; 0x008e69a7: jne 0x8e69b0
  - 0x008e698a: jne -> 0x008e69a0 (jcc_true) | ctx: 0x008e6981: mov eax, dword ptr [eax + 0x14] ; 0x008e6984: cmp eax, dword ptr [0xf8bc80] ; 0x008e698a: jne 0x8e69a0
  - 0x008e698a: jne -> 0x008e698c (jcc_false) | ctx: 0x008e6981: mov eax, dword ptr [eax + 0x14] ; 0x008e6984: cmp eax, dword ptr [0xf8bc80] ; 0x008e698a: jne 0x8e69a0
  - 0x008e69bb: jb -> 0x008e69dc (jcc_true) | ctx: 0x008e69b2: mov ecx, esi ; 0x008e69b4: call dword ptr [eax + 4] ; 0x008e69b7: cmp dword ptr [eax + 8], 3 ; 0x008e69bb: jb 0x8e69dc
  - 0x008e69bb: jb -> 0x008e69bd (jcc_false) | ctx: 0x008e69b2: mov ecx, esi ; 0x008e69b4: call dword ptr [eax + 4] ; 0x008e69b7: cmp dword ptr [eax + 8], 3 ; 0x008e69bb: jb 0x8e69dc
  - 0x008e69bb: jb -> 0x008e69dc (jcc_true) | ctx: 0x008e69b2: mov ecx, esi ; 0x008e69b4: call dword ptr [eax + 4] ; 0x008e69b7: cmp dword ptr [eax + 8], 3 ; 0x008e69bb: jb 0x8e69dc
  - 0x008e69bb: jb -> 0x008e69bd (jcc_false) | ctx: 0x008e69b2: mov ecx, esi ; 0x008e69b4: call dword ptr [eax + 4] ; 0x008e69b7: cmp dword ptr [eax + 8], 3 ; 0x008e69bb: jb 0x8e69dc
  - 0x008e69e9: je -> 0x008e6a01 (jcc_true) | ctx: 0x008e69e0: mov ecx, esi ; 0x008e69e2: call 0x7f69c0 ; 0x008e69e7: test al, al ; 0x008e69e9: je 0x8e6a01
  - 0x008e69e9: je -> 0x008e69eb (jcc_false) | ctx: 0x008e69e0: mov ecx, esi ; 0x008e69e2: call 0x7f69c0 ; 0x008e69e7: test al, al ; 0x008e69e9: je 0x8e6a01
  - 0x008e69c6: jne -> 0x008e69dc (jcc_true) | ctx: 0x008e69bd: mov eax, dword ptr [eax + 0x14] ; 0x008e69c0: cmp eax, dword ptr [0xf8d838] ; 0x008e69c6: jne 0x8e69dc
  - 0x008e69c6: jne -> 0x008e69c8 (jcc_false) | ctx: 0x008e69bd: mov eax, dword ptr [eax + 0x14] ; 0x008e69c0: cmp eax, dword ptr [0xf8d838] ; 0x008e69c6: jne 0x8e69dc
  - 0x008e6a0e: je -> 0x008e6a24 (jcc_true) | ctx: 0x008e6a05: mov ecx, esi ; 0x008e6a07: call 0x7f5d50 ; 0x008e6a0c: test al, al ; 0x008e6a0e: je 0x8e6a24
  - 0x008e6a0e: je -> 0x008e6a10 (jcc_false) | ctx: 0x008e6a05: mov ecx, esi ; 0x008e6a07: call 0x7f5d50 ; 0x008e6a0c: test al, al ; 0x008e6a0e: je 0x8e6a24
  - 0x008e6a31: je -> 0x008e6a47 (jcc_true) | ctx: 0x008e6a28: mov ecx, esi ; 0x008e6a2a: call 0x7f6a00 ; 0x008e6a2f: test al, al ; 0x008e6a31: je 0x8e6a47
  - 0x008e6a31: je -> 0x008e6a33 (jcc_false) | ctx: 0x008e6a28: mov ecx, esi ; 0x008e6a2a: call 0x7f6a00 ; 0x008e6a2f: test al, al ; 0x008e6a31: je 0x8e6a47
  - 0x008e6a54: je -> 0x008e6a6a (jcc_true) | ctx: 0x008e6a4b: mov ecx, esi ; 0x008e6a4d: call 0x8cbaa0 ; 0x008e6a52: test al, al ; 0x008e6a54: je 0x8e6a6a
  - 0x008e6a54: je -> 0x008e6a56 (jcc_false) | ctx: 0x008e6a4b: mov ecx, esi ; 0x008e6a4d: call 0x8cbaa0 ; 0x008e6a52: test al, al ; 0x008e6a54: je 0x8e6a6a
  - 0x008e6a7a: jne -> 0x008e69ee (jcc_true) | ctx: 0x008e6a70: call 0x7f6740 ; 0x008e6a75: test al, al ; 0x008e6a77: mov eax, dword ptr [ebp + 8] ; 0x008e6a7a: jne 0x8e69ee
  - 0x008e6a7a: jne -> 0x008e6a80 (jcc_false) | ctx: 0x008e6a70: call 0x7f6740 ; 0x008e6a75: test al, al ; 0x008e6a77: mov eax, dword ptr [ebp + 8] ; 0x008e6a7a: jne 0x8e69ee

### 0x008ecf90
- blocks=1, insns=17, edges=1, jcc=0, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCPath@EGL@@ slot 2 (target 0x008ecfd0, vtable 0x00bc9218)
  - rtti_vtable_method: .?AVCCamperBehaviorProperties@GGL@@ slot 2 (target 0x008ecfd0, vtable 0x00bd8f48)
  - rtti_vtable_method: .?AVCCamperBehavior@GGL@@ slot 2 (target 0x008ecfd0, vtable 0x00bd8eb0)
  - rtti_vtable_method: .?AVCCampBehavior@GGL@@ slot 2 (target 0x008ecfd0, vtable 0x00bd8f10)
  - rtti_vtable_method: .?AVCCampBehaviorProperties@GGL@@ slot 2 (target 0x008ecfd0, vtable 0x00bd8ed4)
  - rtti_vtable_method: .?AVCPath@GGL@@ slot 2 (target 0x008ecfd0, vtable 0x00bdb29c)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehaviorProps@GGL@@ slot 2 (target 0x008ecfd0, vtable 0x00be101c)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehavior@GGL@@ slot 2 (target 0x008ecfd0, vtable 0x00be1058)
  - rtti_vtable_method: .?AVCWorkerBehaviorProps@GGL@@ slot 2 (target 0x008ecfd0, vtable 0x00be1178)
  - rtti_vtable_method: .?AVCWorkerBehavior@GGL@@ slot 2 (target 0x008ecfd0, vtable 0x00be1450)
  - rtti_vtable_method: .?AVCWorkerFleeBehaviorProps@GGL@@ slot 2 (target 0x008ecfd0, vtable 0x00be177c)
  - rtti_vtable_method: .?AVCWorkerFleeBehavior@GGL@@ slot 2 (target 0x008ecfd0, vtable 0x00be17a8)
- branch points:
  - none

### 0x00b4b114
- blocks=8, insns=66, edges=20, jcc=5, indirect_jmp=0, truncated=False
- reasons:
  - rtti_vtable_method: .?AVCCamperBehaviorProperties@GGL@@ slot 1 (target 0x00b4b190, vtable 0x00bd8f58)
  - rtti_vtable_method: .?AVCCampBehaviorProperties@GGL@@ slot 1 (target 0x00b4b190, vtable 0x00bd8ee4)
  - rtti_vtable_method: .?AVCWorkerAlarmModeBehaviorProps@GGL@@ slot 1 (target 0x00b4b190, vtable 0x00be102c)
  - rtti_vtable_method: .?AVCWorkerBehaviorProps@GGL@@ slot 1 (target 0x00b4b190, vtable 0x00be1188)
  - rtti_vtable_method: .?AVCWorkerFleeBehaviorProps@GGL@@ slot 1 (target 0x00b4b190, vtable 0x00be178c)
- branch points:
  - 0x00b4b121: jne -> 0x00b4b12a (jcc_true) | ctx: 0x00b4b117: mov byte ptr [ebp - 0x14], 1 ; 0x00b4b11b: lea esi, [edi + 8] ; 0x00b4b11e: mov dword ptr [ebp - 0x10], esi ; 0x00b4b121: jne 0xb4b12a
  - 0x00b4b121: jne -> 0x00b4b123 (jcc_false) | ctx: 0x00b4b117: mov byte ptr [ebp - 0x14], 1 ; 0x00b4b11b: lea esi, [edi + 8] ; 0x00b4b11e: mov dword ptr [ebp - 0x10], esi ; 0x00b4b121: jne 0xb4b12a
  - 0x00b4b14d: je -> 0x00b4b158 (jcc_true) | ctx: 0x00b4b142: push dword ptr [edi + 4] ; 0x00b4b145: call dword ptr [0xbb9594] ; 0x00b4b14b: test eax, eax ; 0x00b4b14d: je 0xb4b158
  - 0x00b4b14d: je -> 0x00b4b14f (jcc_false) | ctx: 0x00b4b142: push dword ptr [edi + 4] ; 0x00b4b145: call dword ptr [0xbb9594] ; 0x00b4b14b: test eax, eax ; 0x00b4b14d: je 0xb4b158
  - 0x00b4b14d: je -> 0x00b4b158 (jcc_true) | ctx: 0x00b4b142: push dword ptr [edi + 4] ; 0x00b4b145: call dword ptr [0xbb9594] ; 0x00b4b14b: test eax, eax ; 0x00b4b14d: je 0xb4b158
  - 0x00b4b14d: je -> 0x00b4b14f (jcc_false) | ctx: 0x00b4b142: push dword ptr [edi + 4] ; 0x00b4b145: call dword ptr [0xbb9594] ; 0x00b4b14b: test eax, eax ; 0x00b4b14d: je 0xb4b158
  - 0x00b4b16f: jne -> 0x00b4b178 (jcc_true) | ctx: 0x00b4b15c: mov dword ptr [ebp - 4], 2 ; 0x00b4b163: call 0xb1d310 ; 0x00b4b168: cmp byte ptr [0xfb036c], 0 ; 0x00b4b16f: jne 0xb4b178
  - 0x00b4b16f: jne -> 0x00b4b171 (jcc_false) | ctx: 0x00b4b15c: mov dword ptr [ebp - 4], 2 ; 0x00b4b163: call 0xb1d310 ; 0x00b4b168: cmp byte ptr [0xfb036c], 0 ; 0x00b4b16f: jne 0xb4b178
  - 0x00b4b156: jmp -> 0x00b4b15a (jmp) | ctx: 0x00b4b14f: call 0xb1d280 ; 0x00b4b154: xor bl, bl ; 0x00b4b156: jmp 0xb4b15a
  - 0x00b4b16f: jne -> 0x00b4b178 (jcc_true) | ctx: 0x00b4b15c: mov dword ptr [ebp - 4], 2 ; 0x00b4b163: call 0xb1d310 ; 0x00b4b168: cmp byte ptr [0xfb036c], 0 ; 0x00b4b16f: jne 0xb4b178
  - 0x00b4b16f: jne -> 0x00b4b171 (jcc_false) | ctx: 0x00b4b15c: mov dword ptr [ebp - 4], 2 ; 0x00b4b163: call 0xb1d310 ; 0x00b4b168: cmp byte ptr [0xfb036c], 0 ; 0x00b4b16f: jne 0xb4b178

## Limits

- Function starts are heuristic (prologue-based).
- Indirect control-flow targets are not fully resolved.
- This is static analysis without dynamic execution traces.
