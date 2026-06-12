# Engine Branch Evidence

- Binary: `C:\Users\marku\OneDrive\Desktop\Gold edition\bin\SettlersHoK.exe`
- Size: 5038080 bytes
- Generated: 2026-06-10T22:45:23.522649+00:00

## Inferences

- [high] Engine contains distinct thresholds for Work/Farm/Residence/CampFire and shared WorkTimeBase.
  evidence: `worktime_thresholds`
- [high] Worker assignment/reassignment logic uses explicit max distance fields for Farm and Residence plus reattach frequency.
  evidence: `worker_distance_and_assignment`
- [medium] Camp placement/selection appears predicate-driven (potential site, free slot, unblocked square) under CCamp/CCamper behavior classes.
  evidence: `camp_behavior_classes`
- [high] Worker eat/rest/work transitions include explicit success-check task IDs for GO_TO_* branches.
  evidence: `task_ids_worker_camp`
- [high] Dedicated worker alarm/flee behavior classes and command names indicate separate alarm branch flow from regular worker cycle.
  evidence: `worker_alarm_and_flight`

## worktime_thresholds

- patterns: 5 | hits: 5

- hit: `WorkTimeThresholdCampFire` (pattern `WorkTimeThresholdCampFire`, offset `0x0036f384`)
  context:
     [0x0036f31c] `MotivationMillisecondsWithoutJob`
     [0x0036f340] `MotivationAbsoluteMaxMotivation`
     [0x0036f360] `MotivationGameStartMaxMotivation`
  >> [0x0036f384] `WorkTimeThresholdCampFire`
     [0x0036f3a0] `WorkTimeThresholdResidence`
     [0x0036f3bc] `WorkTimeThresholdFarm`
     [0x0036f3d4] `WorkTimeThresholdWork`
- hit: `WorkTimeThresholdResidence` (pattern `WorkTimeThresholdResidence`, offset `0x0036f3a0`)
  context:
     [0x0036f340] `MotivationAbsoluteMaxMotivation`
     [0x0036f360] `MotivationGameStartMaxMotivation`
     [0x0036f384] `WorkTimeThresholdCampFire`
  >> [0x0036f3a0] `WorkTimeThresholdResidence`
     [0x0036f3bc] `WorkTimeThresholdFarm`
     [0x0036f3d4] `WorkTimeThresholdWork`
     [0x0036f3ec] `WorkTimeBase`
- hit: `WorkTimeThresholdFarm` (pattern `WorkTimeThresholdFarm`, offset `0x0036f3bc`)
  context:
     [0x0036f360] `MotivationGameStartMaxMotivation`
     [0x0036f384] `WorkTimeThresholdCampFire`
     [0x0036f3a0] `WorkTimeThresholdResidence`
  >> [0x0036f3bc] `WorkTimeThresholdFarm`
     [0x0036f3d4] `WorkTimeThresholdWork`
     [0x0036f3ec] `WorkTimeBase`
     [0x0036f3fc] `AverageMotivationVillageCenterLockThreshold`
- hit: `WorkTimeThresholdWork` (pattern `WorkTimeThresholdWork`, offset `0x0036f3d4`)
  context:
     [0x0036f384] `WorkTimeThresholdCampFire`
     [0x0036f3a0] `WorkTimeThresholdResidence`
     [0x0036f3bc] `WorkTimeThresholdFarm`
  >> [0x0036f3d4] `WorkTimeThresholdWork`
     [0x0036f3ec] `WorkTimeBase`
     [0x0036f3fc] `AverageMotivationVillageCenterLockThreshold`
     [0x0036f428] `MotivationThresholdLeave`
- hit: `WorkTimeBase` (pattern `WorkTimeBase`, offset `0x0036f3ec`)
  context:
     [0x0036f3a0] `WorkTimeThresholdResidence`
     [0x0036f3bc] `WorkTimeThresholdFarm`
     [0x0036f3d4] `WorkTimeThresholdWork`
  >> [0x0036f3ec] `WorkTimeBase`
     [0x0036f3fc] `AverageMotivationVillageCenterLockThreshold`
     [0x0036f428] `MotivationThresholdLeave`
     [0x0036f444] `MotivationThresholdAngry`

## worker_distance_and_assignment

- patterns: 11 | hits: 11

- hit: `SetWorkTaskListsPerCycle` (pattern `SetWorkTaskListsPerCycle`, offset `0x00373e7c`)
  context:
     [0x00373e50] `GetEntityDamage`
     [0x00373e60] `GetEntityArmor`
     [0x00373e70] `MoveSettler`
  >> [0x00373e7c] `SetWorkTaskListsPerCycle`
     [0x00373e98] `FillSettlerUpgradeCostsTable`
     [0x00373eb8] `GetSettlerTypeByUpgradeCategory`
     [0x00373ed8] `DEBUG_UpgradeSettler`
- hit: `GetSettlersResidence` (pattern `GetSettlersResidence`, offset `0x00373f28`)
  context:
     [0x00373ef0] `UpgradeSettler`
     [0x00373f00] `SetSpeedFactor`
     [0x00373f10] `GetSettlersWorkBuilding`
  >> [0x00373f28] `GetSettlersResidence`
     [0x00373f40] `GetSettlersFarm`
     [0x00373f50] `IsSettlerAtWork`
     [0x00373f60] `IsSettlerAtResidence`
- hit: `GetSettlersFarm` (pattern `GetSettlersFarm`, offset `0x00373f40`)
  context:
     [0x00373f00] `SetSpeedFactor`
     [0x00373f10] `GetSettlersWorkBuilding`
     [0x00373f28] `GetSettlersResidence`
  >> [0x00373f40] `GetSettlersFarm`
     [0x00373f50] `IsSettlerAtWork`
     [0x00373f60] `IsSettlerAtResidence`
     [0x00373f78] `IsSettlerAtFarm`
- hit: `IsSettlerAtResidence` (pattern `IsSettlerAtResidence`, offset `0x00373f60`)
  context:
     [0x00373f28] `GetSettlersResidence`
     [0x00373f40] `GetSettlersFarm`
     [0x00373f50] `IsSettlerAtWork`
  >> [0x00373f60] `IsSettlerAtResidence`
     [0x00373f78] `IsSettlerAtFarm`
     [0x00373f88] `GetSettlersMotivation`
     [0x00373fa0] `FillSerfCostsTable`
- hit: `IsSettlerAtFarm` (pattern `IsSettlerAtFarm`, offset `0x00373f78`)
  context:
     [0x00373f40] `GetSettlersFarm`
     [0x00373f50] `IsSettlerAtWork`
     [0x00373f60] `IsSettlerAtResidence`
  >> [0x00373f78] `IsSettlerAtFarm`
     [0x00373f88] `GetSettlersMotivation`
     [0x00373fa0] `FillSerfCostsTable`
     [0x00373fb4] `IsWorker`
- hit: `GetNextWorkerWithoutFarmOrResidence` (pattern `GetNextWorkerWithoutFarmOrResidence`, offset `0x003742f4`)
  context:
     [0x0037429c] `GetLeadersGroupAttractionLimitValue`
     [0x003742c0] `GetLeaderExperienceLevel`
     [0x003742dc] `ChangeSettlerPlayerID`
  >> [0x003742f4] `GetNextWorkerWithoutFarmOrResidence`
     [0x00374318] `GetNextWorkerWithoutFarm`
     [0x00374334] `GetNextWorkerWithoutResidence`
     [0x00374354] `ChangeAllEntitiesPlayerID`
- hit: `GetNextWorkerWithoutFarm` (pattern `GetNextWorkerWithoutFarm`, offset `0x00374318`)
  context:
     [0x003742c0] `GetLeaderExperienceLevel`
     [0x003742dc] `ChangeSettlerPlayerID`
     [0x003742f4] `GetNextWorkerWithoutFarmOrResidence`
  >> [0x00374318] `GetNextWorkerWithoutFarm`
     [0x00374334] `GetNextWorkerWithoutResidence`
     [0x00374354] `ChangeAllEntitiesPlayerID`
     [0x00374370] `GetMerchantBuildingId`
- hit: `GetNextWorkerWithoutResidence` (pattern `GetNextWorkerWithoutResidence`, offset `0x00374334`)
  context:
     [0x003742dc] `ChangeSettlerPlayerID`
     [0x003742f4] `GetNextWorkerWithoutFarmOrResidence`
     [0x00374318] `GetNextWorkerWithoutFarm`
  >> [0x00374334] `GetNextWorkerWithoutResidence`
     [0x00374354] `ChangeAllEntitiesPlayerID`
     [0x00374370] `GetMerchantBuildingId`
     [0x003743d8] `IsObstructed`
- hit: `MaximumDistanceWorkerToResidence` (pattern `MaximumDistanceWorkerToResidence`, offset `0x0037569c`)
  context:
     [0x0037563c] `PlayerGetGameStateChangedTime`
     [0x0037565c] `PlayerSetIsHumanFlag`
     [0x00375674] `PlayerSetPlayerColor`
  >> [0x0037569c] `MaximumDistanceWorkerToResidence`
     [0x003756c0] `MaximumDistanceWorkerToFarm`
     [0x003756dc] `PlayerMoneyDispo`
     [0x003756f0] `ReAttachWorkerFrequency`
- hit: `MaximumDistanceWorkerToFarm` (pattern `MaximumDistanceWorkerToFarm`, offset `0x003756c0`)
  context:
     [0x0037565c] `PlayerSetIsHumanFlag`
     [0x00375674] `PlayerSetPlayerColor`
     [0x0037569c] `MaximumDistanceWorkerToResidence`
  >> [0x003756c0] `MaximumDistanceWorkerToFarm`
     [0x003756dc] `PlayerMoneyDispo`
     [0x003756f0] `ReAttachWorkerFrequency`
     [0x00375708] `EntityTypeBanTime`
- hit: `ReAttachWorkerFrequency` (pattern `ReAttachWorkerFrequency`, offset `0x003756f0`)
  context:
     [0x0037569c] `MaximumDistanceWorkerToResidence`
     [0x003756c0] `MaximumDistanceWorkerToFarm`
     [0x003756dc] `PlayerMoneyDispo`
  >> [0x003756f0] `ReAttachWorkerFrequency`
     [0x00375708] `EntityTypeBanTime`
     [0x0037571c] `PaydayFrequency`
     [0x0037572c] `AttractionFrequency`

## camp_behavior_classes

- patterns: 8 | hits: 18

- hit: `.?AVCCamperBehavior@GGL@@` (pattern `CCamperBehavior`, offset `0x00423728`)
  context:
     [0x00423614] `.?AVCCannonBallEffectProps@GGL@@`
     [0x00423640] `.?AVCFlyingEffectSlot@EGL@@`
     [0x00423664] `.?AVCCannonBallEffect@GGL@@`
  >> [0x00423728] `.?AVCCamperBehavior@GGL@@`
     [0x0042374c] `.?AVCUnblockedSquarePredicate@EGL@@`
     [0x00423778] `.?AVCCampBehaviorProperties@GGL@@`
     [0x004237a4] `.?AVCPotentialCampSitePredicate@GGL@@`
- hit: `.?AVCUnblockedSquarePredicate@EGL@@` (pattern `CUnblockedSquarePredicate`, offset `0x0042374c`)
  context:
     [0x00423640] `.?AVCFlyingEffectSlot@EGL@@`
     [0x00423664] `.?AVCCannonBallEffect@GGL@@`
     [0x00423728] `.?AVCCamperBehavior@GGL@@`
  >> [0x0042374c] `.?AVCUnblockedSquarePredicate@EGL@@`
     [0x00423778] `.?AVCCampBehaviorProperties@GGL@@`
     [0x004237a4] `.?AVCPotentialCampSitePredicate@GGL@@`
     [0x004237d4] `.?AVCCamperBehaviorProperties@GGL@@`
- hit: `.?AVCCampBehaviorProperties@GGL@@` (pattern `CCampBehaviorProperties`, offset `0x00423778`)
  context:
     [0x00423664] `.?AVCCannonBallEffect@GGL@@`
     [0x00423728] `.?AVCCamperBehavior@GGL@@`
     [0x0042374c] `.?AVCUnblockedSquarePredicate@EGL@@`
  >> [0x00423778] `.?AVCCampBehaviorProperties@GGL@@`
     [0x004237a4] `.?AVCPotentialCampSitePredicate@GGL@@`
     [0x004237d4] `.?AVCCamperBehaviorProperties@GGL@@`
     [0x00423800] `.?AVCCampWithFreeSlotPredicate@GGL@@`
- hit: `.?AVCPotentialCampSitePredicate@GGL@@` (pattern `CPotentialCampSitePredicate`, offset `0x004237a4`)
  context:
     [0x00423728] `.?AVCCamperBehavior@GGL@@`
     [0x0042374c] `.?AVCUnblockedSquarePredicate@EGL@@`
     [0x00423778] `.?AVCCampBehaviorProperties@GGL@@`
  >> [0x004237a4] `.?AVCPotentialCampSitePredicate@GGL@@`
     [0x004237d4] `.?AVCCamperBehaviorProperties@GGL@@`
     [0x00423800] `.?AVCCampWithFreeSlotPredicate@GGL@@`
     [0x00423830] `.?AVCEventGetPositionFromID@GGL@@`
- hit: `.?AVCCamperBehaviorProperties@GGL@@` (pattern `CCamperBehaviorProperties`, offset `0x004237d4`)
  context:
     [0x0042374c] `.?AVCUnblockedSquarePredicate@EGL@@`
     [0x00423778] `.?AVCCampBehaviorProperties@GGL@@`
     [0x004237a4] `.?AVCPotentialCampSitePredicate@GGL@@`
  >> [0x004237d4] `.?AVCCamperBehaviorProperties@GGL@@`
     [0x00423800] `.?AVCCampWithFreeSlotPredicate@GGL@@`
     [0x00423830] `.?AVCEventGetPositionFromID@GGL@@`
     [0x0042385c] `.?AVCGLEEntityIterator@EGL@@`
- hit: `.?AVCCampWithFreeSlotPredicate@GGL@@` (pattern `CCampWithFreeSlotPredicate`, offset `0x00423800`)
  context:
     [0x00423778] `.?AVCCampBehaviorProperties@GGL@@`
     [0x004237a4] `.?AVCPotentialCampSitePredicate@GGL@@`
     [0x004237d4] `.?AVCCamperBehaviorProperties@GGL@@`
  >> [0x00423800] `.?AVCCampWithFreeSlotPredicate@GGL@@`
     [0x00423830] `.?AVCEventGetPositionFromID@GGL@@`
     [0x0042385c] `.?AVCGLEEntityIterator@EGL@@`
     [0x00423884] `.?AVCGLEEntityAreaIterator@EGL@@`
- hit: `.?AVCEventGetPositionFromID@GGL@@` (pattern `CEventGetPositionFromID`, offset `0x00423830`)
  context:
     [0x004237a4] `.?AVCPotentialCampSitePredicate@GGL@@`
     [0x004237d4] `.?AVCCamperBehaviorProperties@GGL@@`
     [0x00423800] `.?AVCCampWithFreeSlotPredicate@GGL@@`
  >> [0x00423830] `.?AVCEventGetPositionFromID@GGL@@`
     [0x0042385c] `.?AVCGLEEntityIterator@EGL@@`
     [0x00423884] `.?AVCGLEEntityAreaIterator@EGL@@`
     [0x004238b0] `.?AV?$THandler@$0BDABA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCCampBehavior@GGL@@X@EGL@@` (pattern `CCampBehavior`, offset `0x004238b0`)
  context:
     [0x00423830] `.?AVCEventGetPositionFromID@GGL@@`
     [0x0042385c] `.?AVCGLEEntityIterator@EGL@@`
     [0x00423884] `.?AVCGLEEntityAreaIterator@EGL@@`
  >> [0x004238b0] `.?AV?$THandler@$0BDABA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00423920] `.?AV?$THandler@$0BDAAN@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00423990] `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x004239f8] `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAN@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCampBehavior@GGL@@X@EGL@@` (pattern `CCampBehavior`, offset `0x00423920`)
  context:
     [0x0042385c] `.?AVCGLEEntityIterator@EGL@@`
     [0x00423884] `.?AVCGLEEntityAreaIterator@EGL@@`
     [0x004238b0] `.?AV?$THandler@$0BDABA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
  >> [0x00423920] `.?AV?$THandler@$0BDAAN@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00423990] `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x004239f8] `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x00423a58] `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@` (pattern `CCampBehavior`, offset `0x00423990`)
  context:
     [0x00423884] `.?AVCGLEEntityAreaIterator@EGL@@`
     [0x004238b0] `.?AV?$THandler@$0BDABA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00423920] `.?AV?$THandler@$0BDAAN@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
  >> [0x00423990] `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x004239f8] `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x00423a58] `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00423ab4] `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@`
- hit: `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@` (pattern `CCampBehavior`, offset `0x004239f8`)
  context:
     [0x004238b0] `.?AV?$THandler@$0BDABA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00423920] `.?AV?$THandler@$0BDAAN@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00423990] `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@`
  >> [0x004239f8] `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x00423a58] `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00423ab4] `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@`
     [0x00423af0] `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@` (pattern `CCampBehavior`, offset `0x00423a58`)
  context:
     [0x00423920] `.?AV?$THandler@$0BDAAN@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00423990] `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x004239f8] `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@`
  >> [0x00423a58] `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00423ab4] `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@`
     [0x00423af0] `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00423b48] `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@` (pattern `CCampBehavior`, offset `0x00423ab4`)
  context:
     [0x00423990] `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x004239f8] `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x00423a58] `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@`
  >> [0x00423ab4] `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@`
     [0x00423af0] `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00423b48] `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00423ba0] `.?AV?$THandler@$0BDABC@VCEvent@BB@@V12@VCCamperBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@` (pattern `CCamperBehavior`, offset `0x00423af0`)
  context:
     [0x004239f8] `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x00423a58] `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00423ab4] `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@`
  >> [0x00423af0] `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00423b48] `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00423ba0] `.?AV?$THandler@$0BDABC@VCEvent@BB@@V12@VCCamperBehavior@GGL@@X@EGL@@`
     [0x00423bf0] `.?AV?$THandler@$0BDABB@VCEvent@BB@@VCEvent1Entity@EGL@@VCCamperBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@` (pattern `CCamperBehavior`, offset `0x00423b48`)
  context:
     [0x00423a58] `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00423ab4] `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@`
     [0x00423af0] `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
  >> [0x00423b48] `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00423ba0] `.?AV?$THandler@$0BDABC@VCEvent@BB@@V12@VCCamperBehavior@GGL@@X@EGL@@`
     [0x00423bf0] `.?AV?$THandler@$0BDABB@VCEvent@BB@@VCEvent1Entity@EGL@@VCCamperBehavior@GGL@@X@EGL@@`
     [0x00423c50] `.?AVCCampBehavior@GGL@@`
- hit: `.?AV?$THandler@$0BDABC@VCEvent@BB@@V12@VCCamperBehavior@GGL@@X@EGL@@` (pattern `CCamperBehavior`, offset `0x00423ba0`)
  context:
     [0x00423ab4] `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@`
     [0x00423af0] `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00423b48] `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
  >> [0x00423ba0] `.?AV?$THandler@$0BDABC@VCEvent@BB@@V12@VCCamperBehavior@GGL@@X@EGL@@`
     [0x00423bf0] `.?AV?$THandler@$0BDABB@VCEvent@BB@@VCEvent1Entity@EGL@@VCCamperBehavior@GGL@@X@EGL@@`
     [0x00423c50] `.?AVCCampBehavior@GGL@@`
     [0x00423d30] `.?AVCCamouflageBehaviorProps@GGL@@`
- hit: `.?AV?$THandler@$0BDABB@VCEvent@BB@@VCEvent1Entity@EGL@@VCCamperBehavior@GGL@@X@EGL@@` (pattern `CCamperBehavior`, offset `0x00423bf0`)
  context:
     [0x00423af0] `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00423b48] `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00423ba0] `.?AV?$THandler@$0BDABC@VCEvent@BB@@V12@VCCamperBehavior@GGL@@X@EGL@@`
  >> [0x00423bf0] `.?AV?$THandler@$0BDABB@VCEvent@BB@@VCEvent1Entity@EGL@@VCCamperBehavior@GGL@@X@EGL@@`
     [0x00423c50] `.?AVCCampBehavior@GGL@@`
     [0x00423d30] `.?AVCCamouflageBehaviorProps@GGL@@`
     [0x00423d60] `.?AV?$THandler@$0BGABF@VCEvent@BB@@V12@VCCamouflageBehavior@GGL@@X@EGL@@`
- hit: `.?AVCCampBehavior@GGL@@` (pattern `CCampBehavior`, offset `0x00423c50`)
  context:
     [0x00423b48] `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00423ba0] `.?AV?$THandler@$0BDABC@VCEvent@BB@@V12@VCCamperBehavior@GGL@@X@EGL@@`
     [0x00423bf0] `.?AV?$THandler@$0BDABB@VCEvent@BB@@VCEvent1Entity@EGL@@VCCamperBehavior@GGL@@X@EGL@@`
  >> [0x00423c50] `.?AVCCampBehavior@GGL@@`
     [0x00423d30] `.?AVCCamouflageBehaviorProps@GGL@@`
     [0x00423d60] `.?AV?$THandler@$0BGABF@VCEvent@BB@@V12@VCCamouflageBehavior@GGL@@X@EGL@@`
     [0x00423db8] `.?AV?$THandler@$0CAAAF@VCEvent@BB@@V12@VCCamouflageBehavior@GGL@@X@EGL@@`

## worker_behavior_classes

- patterns: 8 | hits: 133

- hit: `.?AVCWorkerFleeBehaviorProps@GGL@@` (pattern `CWorkerFleeBehaviorProps`, offset `0x00413754`)
  context:
     [0x004135e8] `.?AVCPositionAtCircularResourceFinder@GGL@@`
     [0x0041361c] `.?AVCPositionAtLinearResourceFinder@GGL@@`
     [0x00413730] `.?AVCGLEBehaviorProps@EGL@@`
  >> [0x00413754] `.?AVCWorkerFleeBehaviorProps@GGL@@`
     [0x00413780] `.?AVCGLEBehavior@EGL@@`
     [0x004137a0] `.?AVCWorkerFleeBehavior@GGL@@`
     [0x004137c8] `.?AV?$THandler@$0BFAAO@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
- hit: `.?AVCWorkerFleeBehavior@GGL@@` (pattern `CWorkerFleeBehavior`, offset `0x004137a0`)
  context:
     [0x00413730] `.?AVCGLEBehaviorProps@EGL@@`
     [0x00413754] `.?AVCWorkerFleeBehaviorProps@GGL@@`
     [0x00413780] `.?AVCGLEBehavior@EGL@@`
  >> [0x004137a0] `.?AVCWorkerFleeBehavior@GGL@@`
     [0x004137c8] `.?AV?$THandler@$0BFAAO@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
     [0x00413830] `.?AV?$THandler@$0BDABP@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
     [0x004138a8] `.?AV?$THandler@$0IN@VCGLETaskArgs@EGL@@V12@VCWorkerFleeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BFAAO@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@` (pattern `CWorkerFleeBehavior`, offset `0x004137c8`)
  context:
     [0x00413754] `.?AVCWorkerFleeBehaviorProps@GGL@@`
     [0x00413780] `.?AVCGLEBehavior@EGL@@`
     [0x004137a0] `.?AVCWorkerFleeBehavior@GGL@@`
  >> [0x004137c8] `.?AV?$THandler@$0BFAAO@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
     [0x00413830] `.?AV?$THandler@$0BDABP@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
     [0x004138a8] `.?AV?$THandler@$0IN@VCGLETaskArgs@EGL@@V12@VCWorkerFleeBehavior@GGL@@H@EGL@@`
     [0x004139a0] `.?AVCEvadeBehaviorBase@GGL@@`
- hit: `.?AV?$THandler@$0BDABP@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@` (pattern `CWorkerFleeBehavior`, offset `0x00413830`)
  context:
     [0x00413780] `.?AVCGLEBehavior@EGL@@`
     [0x004137a0] `.?AVCWorkerFleeBehavior@GGL@@`
     [0x004137c8] `.?AV?$THandler@$0BFAAO@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
  >> [0x00413830] `.?AV?$THandler@$0BDABP@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
     [0x004138a8] `.?AV?$THandler@$0IN@VCGLETaskArgs@EGL@@V12@VCWorkerFleeBehavior@GGL@@H@EGL@@`
     [0x004139a0] `.?AVCEvadeBehaviorBase@GGL@@`
     [0x004139c8] `.?AVCWorkerEvadeBehavior@GGL@@`
- hit: `.?AV?$THandler@$0IN@VCGLETaskArgs@EGL@@V12@VCWorkerFleeBehavior@GGL@@H@EGL@@` (pattern `CWorkerFleeBehavior`, offset `0x004138a8`)
  context:
     [0x004137a0] `.?AVCWorkerFleeBehavior@GGL@@`
     [0x004137c8] `.?AV?$THandler@$0BFAAO@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
     [0x00413830] `.?AV?$THandler@$0BDABP@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
  >> [0x004138a8] `.?AV?$THandler@$0IN@VCGLETaskArgs@EGL@@V12@VCWorkerFleeBehavior@GGL@@H@EGL@@`
     [0x004139a0] `.?AVCEvadeBehaviorBase@GGL@@`
     [0x004139c8] `.?AVCWorkerEvadeBehavior@GGL@@`
     [0x00413a90] `.?AVCGLETaskArgsAnimation@EGL@@`
- hit: `.?AVCWorkerBehavior@GGL@@` (pattern `CWorkerBehavior`, offset `0x00413b24`)
  context:
     [0x00413ab8] `.?AVCTaskArgsInteger@EGL@@`
     [0x00413adc] `.?AVCTaskArgsFloat@EGL@@`
     [0x00413b00] `.?AVCSectorPredicate@EGL@@`
  >> [0x00413b24] `.?AVCWorkerBehavior@GGL@@`
     [0x00413b48] `.?AVCWorkerBehaviorProps@GGL@@`
     [0x00413b70] `.?AVCEventUVAnim@EGL@@`
     [0x00413b90] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AVCWorkerBehaviorProps@GGL@@` (pattern `CWorkerBehaviorProps`, offset `0x00413b48`)
  context:
     [0x00413adc] `.?AVCTaskArgsFloat@EGL@@`
     [0x00413b00] `.?AVCSectorPredicate@EGL@@`
     [0x00413b24] `.?AVCWorkerBehavior@GGL@@`
  >> [0x00413b48] `.?AVCWorkerBehaviorProps@GGL@@`
     [0x00413b70] `.?AVCEventUVAnim@EGL@@`
     [0x00413b90] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413be8] `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00413b90`)
  context:
     [0x00413b24] `.?AVCWorkerBehavior@GGL@@`
     [0x00413b48] `.?AVCWorkerBehaviorProps@GGL@@`
     [0x00413b70] `.?AVCEventUVAnim@EGL@@`
  >> [0x00413b90] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413be8] `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413c50] `.?AV?$THandler@$0DO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413ca8] `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00413be8`)
  context:
     [0x00413b48] `.?AVCWorkerBehaviorProps@GGL@@`
     [0x00413b70] `.?AVCEventUVAnim@EGL@@`
     [0x00413b90] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00413be8] `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413c50] `.?AV?$THandler@$0DO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413ca8] `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413d10] `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0DO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00413c50`)
  context:
     [0x00413b70] `.?AVCEventUVAnim@EGL@@`
     [0x00413b90] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413be8] `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00413c50] `.?AV?$THandler@$0DO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413ca8] `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413d10] `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413d78] `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00413ca8`)
  context:
     [0x00413b90] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413be8] `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413c50] `.?AV?$THandler@$0DO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00413ca8] `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413d10] `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413d78] `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413de0] `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00413d10`)
  context:
     [0x00413be8] `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413c50] `.?AV?$THandler@$0DO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413ca8] `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00413d10] `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413d78] `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413de0] `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413e48] `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00413d78`)
  context:
     [0x00413c50] `.?AV?$THandler@$0DO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413ca8] `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413d10] `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00413d78] `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413de0] `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413e48] `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413eb0] `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00413de0`)
  context:
     [0x00413ca8] `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413d10] `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413d78] `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00413de0] `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413e48] `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413eb0] `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413f18] `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00413e48`)
  context:
     [0x00413d10] `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413d78] `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413de0] `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00413e48] `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413eb0] `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413f18] `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413f80] `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00413eb0`)
  context:
     [0x00413d78] `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413de0] `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413e48] `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00413eb0] `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413f18] `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413f80] `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413fe8] `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00413f18`)
  context:
     [0x00413de0] `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413e48] `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413eb0] `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00413f18] `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413f80] `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413fe8] `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414050] `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00413f80`)
  context:
     [0x00413e48] `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413eb0] `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413f18] `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00413f80] `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413fe8] `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414050] `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004140b8] `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00413fe8`)
  context:
     [0x00413eb0] `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413f18] `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413f80] `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00413fe8] `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414050] `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004140b8] `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414120] `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414050`)
  context:
     [0x00413f18] `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413f80] `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413fe8] `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414050] `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004140b8] `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414120] `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414188] `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x004140b8`)
  context:
     [0x00413f80] `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00413fe8] `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414050] `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x004140b8] `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414120] `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414188] `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004141f0] `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414120`)
  context:
     [0x00413fe8] `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414050] `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004140b8] `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414120] `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414188] `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004141f0] `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414258] `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414188`)
  context:
     [0x00414050] `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004140b8] `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414120] `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414188] `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004141f0] `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414258] `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004142c0] `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x004141f0`)
  context:
     [0x004140b8] `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414120] `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414188] `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x004141f0] `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414258] `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004142c0] `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414328] `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414258`)
  context:
     [0x00414120] `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414188] `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004141f0] `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414258] `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004142c0] `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414328] `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414390] `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x004142c0`)
  context:
     [0x00414188] `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004141f0] `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414258] `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x004142c0] `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414328] `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414390] `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004143f8] `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414328`)
  context:
     [0x004141f0] `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414258] `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004142c0] `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414328] `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414390] `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004143f8] `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414458] `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414390`)
  context:
     [0x00414258] `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004142c0] `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414328] `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414390] `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004143f8] `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414458] `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004144b0] `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x004143f8`)
  context:
     [0x004142c0] `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414328] `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414390] `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x004143f8] `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414458] `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004144b0] `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414508] `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414458`)
  context:
     [0x00414328] `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414390] `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004143f8] `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414458] `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004144b0] `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414508] `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414560] `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x004144b0`)
  context:
     [0x00414390] `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004143f8] `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414458] `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x004144b0] `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414508] `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414560] `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004145b8] `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414508`)
  context:
     [0x004143f8] `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414458] `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004144b0] `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414508] `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414560] `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004145b8] `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414610] `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414560`)
  context:
     [0x00414458] `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004144b0] `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414508] `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414560] `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004145b8] `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414610] `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414668] `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x004145b8`)
  context:
     [0x004144b0] `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414508] `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414560] `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x004145b8] `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414610] `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414668] `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004146c0] `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414610`)
  context:
     [0x00414508] `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414560] `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004145b8] `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414610] `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414668] `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004146c0] `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414718] `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414668`)
  context:
     [0x00414560] `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004145b8] `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414610] `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414668] `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004146c0] `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414718] `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414770] `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x004146c0`)
  context:
     [0x004145b8] `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414610] `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414668] `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x004146c0] `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414718] `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414770] `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004147c8] `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414718`)
  context:
     [0x00414610] `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414668] `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004146c0] `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414718] `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414770] `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004147c8] `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414820] `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414770`)
  context:
     [0x00414668] `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004146c0] `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414718] `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414770] `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004147c8] `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414820] `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414878] `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x004147c8`)
  context:
     [0x004146c0] `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414718] `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414770] `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x004147c8] `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414820] `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414878] `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004148d0] `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414820`)
  context:
     [0x00414718] `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414770] `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004147c8] `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414820] `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414878] `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004148d0] `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414928] `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414878`)
  context:
     [0x00414770] `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004147c8] `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414820] `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414878] `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004148d0] `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414928] `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414980] `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x004148d0`)
  context:
     [0x004147c8] `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414820] `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414878] `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x004148d0] `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414928] `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414980] `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004149e8] `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414928`)
  context:
     [0x00414820] `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414878] `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004148d0] `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414928] `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414980] `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004149e8] `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414a50] `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414980`)
  context:
     [0x00414878] `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004148d0] `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414928] `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414980] `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004149e8] `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414a50] `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414ab8] `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x004149e8`)
  context:
     [0x004148d0] `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414928] `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414980] `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x004149e8] `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414a50] `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414ab8] `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414b20] `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414a50`)
  context:
     [0x00414928] `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414980] `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004149e8] `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414a50] `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414ab8] `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414b20] `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414b78] `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414ab8`)
  context:
     [0x00414980] `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004149e8] `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414a50] `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414ab8] `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414b20] `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414b78] `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414bd0] `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414b20`)
  context:
     [0x004149e8] `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414a50] `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414ab8] `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414b20] `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414b78] `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414bd0] `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414c28] `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414b78`)
  context:
     [0x00414a50] `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414ab8] `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414b20] `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414b78] `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414bd0] `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414c28] `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414c80] `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414bd0`)
  context:
     [0x00414ab8] `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414b20] `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414b78] `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414bd0] `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414c28] `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414c80] `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414cd8] `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414c28`)
  context:
     [0x00414b20] `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414b78] `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414bd0] `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414c28] `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414c80] `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414cd8] `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414d30] `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414c80`)
  context:
     [0x00414b78] `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414bd0] `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414c28] `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414c80] `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414cd8] `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414d30] `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414d88] `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414cd8`)
  context:
     [0x00414bd0] `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414c28] `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414c80] `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414cd8] `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414d30] `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414d88] `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414df0] `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414d30`)
  context:
     [0x00414c28] `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414c80] `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414cd8] `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414d30] `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414d88] `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414df0] `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414e48] `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414d88`)
  context:
     [0x00414c80] `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414cd8] `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414d30] `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414d88] `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414df0] `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414e48] `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414ea0] `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414df0`)
  context:
     [0x00414cd8] `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414d30] `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414d88] `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414df0] `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414e48] `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414ea0] `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414ef8] `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414e48`)
  context:
     [0x00414d30] `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414d88] `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414df0] `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414e48] `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414ea0] `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414ef8] `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414f50] `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414ea0`)
  context:
     [0x00414d88] `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414df0] `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414e48] `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414ea0] `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414ef8] `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414f50] `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414fa8] `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414ef8`)
  context:
     [0x00414df0] `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414e48] `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414ea0] `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414ef8] `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414f50] `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414fa8] `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415008] `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414f50`)
  context:
     [0x00414e48] `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414ea0] `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414ef8] `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414f50] `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414fa8] `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415008] `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415070] `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00414fa8`)
  context:
     [0x00414ea0] `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414ef8] `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414f50] `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00414fa8] `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415008] `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415070] `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004150e0] `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415008`)
  context:
     [0x00414ef8] `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414f50] `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414fa8] `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00415008] `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415070] `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004150e0] `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415150] `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415070`)
  context:
     [0x00414f50] `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00414fa8] `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415008] `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00415070] `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004150e0] `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415150] `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004151a8] `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x004150e0`)
  context:
     [0x00414fa8] `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415008] `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415070] `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x004150e0] `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415150] `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004151a8] `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415200] `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415150`)
  context:
     [0x00415008] `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415070] `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004150e0] `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00415150] `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004151a8] `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415200] `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415258] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x004151a8`)
  context:
     [0x00415070] `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004150e0] `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415150] `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x004151a8] `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415200] `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415258] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004152b8] `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415200`)
  context:
     [0x004150e0] `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415150] `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004151a8] `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00415200] `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415258] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004152b8] `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415318] `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415258`)
  context:
     [0x00415150] `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x004151a8] `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415200] `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x00415258] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004152b8] `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415318] `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415378] `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x004152b8`)
  context:
     [0x004151a8] `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415200] `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415258] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x004152b8] `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415318] `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415378] `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004153e8] `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415318`)
  context:
     [0x00415200] `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x00415258] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004152b8] `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415318] `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415378] `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004153e8] `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@`
     [0x00415450] `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415378`)
  context:
     [0x00415258] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004152b8] `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415318] `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415378] `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004153e8] `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@`
     [0x00415450] `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004154c0] `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x004153e8`)
  context:
     [0x004152b8] `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415318] `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415378] `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x004153e8] `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@`
     [0x00415450] `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004154c0] `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415530] `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415450`)
  context:
     [0x00415318] `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415378] `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004153e8] `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@`
  >> [0x00415450] `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004154c0] `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415530] `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004155a0] `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x004154c0`)
  context:
     [0x00415378] `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004153e8] `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@`
     [0x00415450] `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x004154c0] `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415530] `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004155a0] `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004155f0] `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415530`)
  context:
     [0x004153e8] `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@`
     [0x00415450] `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004154c0] `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415530] `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004155a0] `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004155f0] `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415640] `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x004155a0`)
  context:
     [0x00415450] `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004154c0] `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415530] `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x004155a0] `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004155f0] `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415640] `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415690] `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x004155f0`)
  context:
     [0x004154c0] `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415530] `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004155a0] `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x004155f0] `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415640] `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415690] `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004156e0] `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415640`)
  context:
     [0x00415530] `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004155a0] `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004155f0] `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415640] `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415690] `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004156e0] `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415750] `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415690`)
  context:
     [0x004155a0] `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004155f0] `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415640] `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415690] `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004156e0] `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415750] `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004157c0] `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x004156e0`)
  context:
     [0x004155f0] `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415640] `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415690] `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x004156e0] `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415750] `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004157c0] `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415810] `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415750`)
  context:
     [0x00415640] `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415690] `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004156e0] `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415750] `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004157c0] `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415810] `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415860] `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x004157c0`)
  context:
     [0x00415690] `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004156e0] `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415750] `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x004157c0] `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415810] `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415860] `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004158d0] `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415810`)
  context:
     [0x004156e0] `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415750] `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004157c0] `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415810] `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415860] `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004158d0] `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415940] `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415860`)
  context:
     [0x00415750] `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004157c0] `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415810] `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415860] `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004158d0] `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415940] `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004159b0] `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x004158d0`)
  context:
     [0x004157c0] `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415810] `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415860] `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x004158d0] `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415940] `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004159b0] `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415a20] `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415940`)
  context:
     [0x00415810] `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415860] `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004158d0] `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415940] `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004159b0] `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415a20] `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415a80] `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x004159b0`)
  context:
     [0x00415860] `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004158d0] `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415940] `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x004159b0] `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415a20] `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415a80] `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415ae0] `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415a20`)
  context:
     [0x004158d0] `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415940] `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004159b0] `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415a20] `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415a80] `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415ae0] `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415b50] `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415a80`)
  context:
     [0x00415940] `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x004159b0] `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415a20] `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415a80] `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415ae0] `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415b50] `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415bc0] `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415ae0`)
  context:
     [0x004159b0] `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415a20] `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415a80] `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415ae0] `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415b50] `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415bc0] `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415c20] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415b50`)
  context:
     [0x00415a20] `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415a80] `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415ae0] `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415b50] `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415bc0] `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415c20] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415c90] `.?AV?$THandler@$0BDACC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415bc0`)
  context:
     [0x00415a80] `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415ae0] `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415b50] `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415bc0] `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415c20] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415c90] `.?AV?$THandler@$0BDACC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415d00] `.?AV?$THandler@$0BDACF@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415c20`)
  context:
     [0x00415ae0] `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415b50] `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415bc0] `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415c20] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415c90] `.?AV?$THandler@$0BDACC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415d00] `.?AV?$THandler@$0BDACF@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415d60] `.?AV?$TStateHandler@VCWorkerBehavior@GGL@@@EGL@@`
- hit: `.?AV?$THandler@$0BDACC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415c90`)
  context:
     [0x00415b50] `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415bc0] `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415c20] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415c90] `.?AV?$THandler@$0BDACC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415d00] `.?AV?$THandler@$0BDACF@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415d60] `.?AV?$TStateHandler@VCWorkerBehavior@GGL@@@EGL@@`
     [0x00415da0] `.?AV?$CEventGetValue@PAVCNeutralBridgeBehavior@GGL@@$0EEJAALPH@@EGL@@`
- hit: `.?AV?$THandler@$0BDACF@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415d00`)
  context:
     [0x00415bc0] `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415c20] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415c90] `.?AV?$THandler@$0BDACC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415d00] `.?AV?$THandler@$0BDACF@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415d60] `.?AV?$TStateHandler@VCWorkerBehavior@GGL@@@EGL@@`
     [0x00415da0] `.?AV?$CEventGetValue@PAVCNeutralBridgeBehavior@GGL@@$0EEJAALPH@@EGL@@`
     [0x00415ed0] `.?AVCBehaviorFollow@GGL@@`
- hit: `.?AV?$TStateHandler@VCWorkerBehavior@GGL@@@EGL@@` (pattern `CWorkerBehavior`, offset `0x00415d60`)
  context:
     [0x00415c20] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415c90] `.?AV?$THandler@$0BDACC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x00415d00] `.?AV?$THandler@$0BDACF@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x00415d60] `.?AV?$TStateHandler@VCWorkerBehavior@GGL@@@EGL@@`
     [0x00415da0] `.?AV?$CEventGetValue@PAVCNeutralBridgeBehavior@GGL@@$0EEJAALPH@@EGL@@`
     [0x00415ed0] `.?AVCBehaviorFollow@GGL@@`
     [0x00415ef4] `.?AVCBattleBehavior@GGL@@`
- hit: `.?AVCWorkerAlarmModeBehaviorProps@GGL@@` (pattern `CWorkerAlarmModeBehaviorProps`, offset `0x004164bc`)
  context:
     [0x004162c8] `.?AV?$THandler@$0CAAAF@VCEvent@BB@@V12@VCWorkerBattleBehavior@GGL@@X@EGL@@`
     [0x00416320] `.?AV?$THandler@$0BBAAD@VCEvent@BB@@VCEventPosition@EGL@@VCWorkerBattleBehavior@GGL@@X@EGL@@`
     [0x00416388] `.?AV?$THandler@$0BIAAJ@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBattleBehavior@GGL@@X@EGL@@`
  >> [0x004164bc] `.?AVCWorkerAlarmModeBehaviorProps@GGL@@`
     [0x004164ec] `.?AVCWorkerAlarmModeBehavior@GGL@@`
     [0x00416518] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416570] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
- hit: `.?AVCWorkerAlarmModeBehavior@GGL@@` (pattern `CWorkerAlarmModeBehavior`, offset `0x004164ec`)
  context:
     [0x00416320] `.?AV?$THandler@$0BBAAD@VCEvent@BB@@VCEventPosition@EGL@@VCWorkerBattleBehavior@GGL@@X@EGL@@`
     [0x00416388] `.?AV?$THandler@$0BIAAJ@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBattleBehavior@GGL@@X@EGL@@`
     [0x004164bc] `.?AVCWorkerAlarmModeBehaviorProps@GGL@@`
  >> [0x004164ec] `.?AVCWorkerAlarmModeBehavior@GGL@@`
     [0x00416518] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416570] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x004165c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `CWorkerAlarmModeBehavior`, offset `0x00416518`)
  context:
     [0x00416388] `.?AV?$THandler@$0BIAAJ@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBattleBehavior@GGL@@X@EGL@@`
     [0x004164bc] `.?AVCWorkerAlarmModeBehaviorProps@GGL@@`
     [0x004164ec] `.?AVCWorkerAlarmModeBehavior@GGL@@`
  >> [0x00416518] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416570] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x004165c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416630] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `CWorkerAlarmModeBehavior`, offset `0x00416570`)
  context:
     [0x004164bc] `.?AVCWorkerAlarmModeBehaviorProps@GGL@@`
     [0x004164ec] `.?AVCWorkerAlarmModeBehavior@GGL@@`
     [0x00416518] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
  >> [0x00416570] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x004165c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416630] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x00416690] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `CWorkerAlarmModeBehavior`, offset `0x004165c8`)
  context:
     [0x004164ec] `.?AVCWorkerAlarmModeBehavior@GGL@@`
     [0x00416518] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416570] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
  >> [0x004165c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416630] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x00416690] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x004166f0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `CWorkerAlarmModeBehavior`, offset `0x00416630`)
  context:
     [0x00416518] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416570] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x004165c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
  >> [0x00416630] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x00416690] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x004166f0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x00416750] `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `CWorkerAlarmModeBehavior`, offset `0x00416690`)
  context:
     [0x00416570] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x004165c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416630] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
  >> [0x00416690] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x004166f0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x00416750] `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x0041688c] `.?AVCEventStartAlphaBlending@GGL@@`
- hit: `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `CWorkerAlarmModeBehavior`, offset `0x004166f0`)
  context:
     [0x004165c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416630] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x00416690] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
  >> [0x004166f0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x00416750] `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x0041688c] `.?AVCEventStartAlphaBlending@GGL@@`
     [0x00416a80] `.?AVCBehaviorWalkCommand@GGL@@`
- hit: `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `CWorkerAlarmModeBehavior`, offset `0x00416750`)
  context:
     [0x00416630] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x00416690] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x004166f0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
  >> [0x00416750] `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x0041688c] `.?AVCEventStartAlphaBlending@GGL@@`
     [0x00416a80] `.?AVCBehaviorWalkCommand@GGL@@`
     [0x00416aa8] `.?AV?$THandler@$0CM@VCGLETaskArgs@EGL@@V12@VCBehaviorWalkCommand@GGL@@H@EGL@@`
- hit: `.?AVCSerfBehavior@GGL@@` (pattern `CSerfBehavior`, offset `0x00419b04`)
  context:
     [0x00419870] `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCSettlerMerchantBehavior@GGL@@H@EGL@@`
     [0x004198e0] `.?AV?$THandler@$0LE@VCGLETaskArgs@EGL@@V12@VCSettlerMerchantBehavior@GGL@@H@EGL@@`
     [0x00419940] `.?AV?$TStateHandler@VCSettlerMerchantBehavior@GGL@@@EGL@@`
  >> [0x00419b04] `.?AVCSerfBehavior@GGL@@`
     [0x00419b24] `.?AVCSerfBehaviorProps@GGL@@`
     [0x00419b50] `.?AV?$THandler@$0BM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419ba0] `.?AV?$THandler@$0FL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AVCSerfBehaviorProps@GGL@@` (pattern `CSerfBehaviorProps`, offset `0x00419b24`)
  context:
     [0x004198e0] `.?AV?$THandler@$0LE@VCGLETaskArgs@EGL@@V12@VCSettlerMerchantBehavior@GGL@@H@EGL@@`
     [0x00419940] `.?AV?$TStateHandler@VCSettlerMerchantBehavior@GGL@@@EGL@@`
     [0x00419b04] `.?AVCSerfBehavior@GGL@@`
  >> [0x00419b24] `.?AVCSerfBehaviorProps@GGL@@`
     [0x00419b50] `.?AV?$THandler@$0BM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419ba0] `.?AV?$THandler@$0FL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419bf0] `.?AV?$THandler@$0IM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x00419b50`)
  context:
     [0x00419940] `.?AV?$TStateHandler@VCSettlerMerchantBehavior@GGL@@@EGL@@`
     [0x00419b04] `.?AVCSerfBehavior@GGL@@`
     [0x00419b24] `.?AVCSerfBehaviorProps@GGL@@`
  >> [0x00419b50] `.?AV?$THandler@$0BM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419ba0] `.?AV?$THandler@$0FL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419bf0] `.?AV?$THandler@$0IM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419c40] `.?AV?$THandler@$0FM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x00419ba0`)
  context:
     [0x00419b04] `.?AVCSerfBehavior@GGL@@`
     [0x00419b24] `.?AVCSerfBehaviorProps@GGL@@`
     [0x00419b50] `.?AV?$THandler@$0BM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x00419ba0] `.?AV?$THandler@$0FL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419bf0] `.?AV?$THandler@$0IM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419c40] `.?AV?$THandler@$0FM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419c90] `.?AV?$THandler@$0FN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0IM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x00419bf0`)
  context:
     [0x00419b24] `.?AVCSerfBehaviorProps@GGL@@`
     [0x00419b50] `.?AV?$THandler@$0BM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419ba0] `.?AV?$THandler@$0FL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x00419bf0] `.?AV?$THandler@$0IM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419c40] `.?AV?$THandler@$0FM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419c90] `.?AV?$THandler@$0FN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419ce0] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x00419c40`)
  context:
     [0x00419b50] `.?AV?$THandler@$0BM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419ba0] `.?AV?$THandler@$0FL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419bf0] `.?AV?$THandler@$0IM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x00419c40] `.?AV?$THandler@$0FM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419c90] `.?AV?$THandler@$0FN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419ce0] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419d30] `.?AV?$THandler@$0GJ@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x00419c90`)
  context:
     [0x00419ba0] `.?AV?$THandler@$0FL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419bf0] `.?AV?$THandler@$0IM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419c40] `.?AV?$THandler@$0FM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x00419c90] `.?AV?$THandler@$0FN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419ce0] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419d30] `.?AV?$THandler@$0GJ@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419d80] `.?AV?$THandler@$0GK@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x00419ce0`)
  context:
     [0x00419bf0] `.?AV?$THandler@$0IM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419c40] `.?AV?$THandler@$0FM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419c90] `.?AV?$THandler@$0FN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x00419ce0] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419d30] `.?AV?$THandler@$0GJ@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419d80] `.?AV?$THandler@$0GK@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419dd0] `.?AV?$THandler@$0II@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0GJ@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x00419d30`)
  context:
     [0x00419c40] `.?AV?$THandler@$0FM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419c90] `.?AV?$THandler@$0FN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419ce0] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x00419d30] `.?AV?$THandler@$0GJ@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419d80] `.?AV?$THandler@$0GK@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419dd0] `.?AV?$THandler@$0II@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419e20] `.?AV?$THandler@$0GL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0GK@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x00419d80`)
  context:
     [0x00419c90] `.?AV?$THandler@$0FN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419ce0] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419d30] `.?AV?$THandler@$0GJ@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x00419d80] `.?AV?$THandler@$0GK@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419dd0] `.?AV?$THandler@$0II@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419e20] `.?AV?$THandler@$0GL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419e70] `.?AV?$THandler@$0GM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0II@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x00419dd0`)
  context:
     [0x00419ce0] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419d30] `.?AV?$THandler@$0GJ@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419d80] `.?AV?$THandler@$0GK@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x00419dd0] `.?AV?$THandler@$0II@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419e20] `.?AV?$THandler@$0GL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419e70] `.?AV?$THandler@$0GM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419ec0] `.?AV?$THandler@$0GN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0GL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x00419e20`)
  context:
     [0x00419d30] `.?AV?$THandler@$0GJ@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419d80] `.?AV?$THandler@$0GK@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419dd0] `.?AV?$THandler@$0II@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x00419e20] `.?AV?$THandler@$0GL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419e70] `.?AV?$THandler@$0GM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419ec0] `.?AV?$THandler@$0GN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419f10] `.?AV?$THandler@$0ID@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0GM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x00419e70`)
  context:
     [0x00419d80] `.?AV?$THandler@$0GK@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419dd0] `.?AV?$THandler@$0II@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419e20] `.?AV?$THandler@$0GL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x00419e70] `.?AV?$THandler@$0GM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419ec0] `.?AV?$THandler@$0GN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419f10] `.?AV?$THandler@$0ID@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419f60] `.?AV?$THandler@$0BAAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0GN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x00419ec0`)
  context:
     [0x00419dd0] `.?AV?$THandler@$0II@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419e20] `.?AV?$THandler@$0GL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419e70] `.?AV?$THandler@$0GM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x00419ec0] `.?AV?$THandler@$0GN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419f10] `.?AV?$THandler@$0ID@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419f60] `.?AV?$THandler@$0BAAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x00419fc0] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0ID@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x00419f10`)
  context:
     [0x00419e20] `.?AV?$THandler@$0GL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419e70] `.?AV?$THandler@$0GM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419ec0] `.?AV?$THandler@$0GN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x00419f10] `.?AV?$THandler@$0ID@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419f60] `.?AV?$THandler@$0BAAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x00419fc0] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a020] `.?AV?$THandler@$0BEAAD@VCEvent@BB@@VCEventEntityIndex@GGL@@VCSerfBehavior@4@X@EGL@@`
- hit: `.?AV?$THandler@$0BAAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x00419f60`)
  context:
     [0x00419e70] `.?AV?$THandler@$0GM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419ec0] `.?AV?$THandler@$0GN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419f10] `.?AV?$THandler@$0ID@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x00419f60] `.?AV?$THandler@$0BAAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x00419fc0] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a020] `.?AV?$THandler@$0BEAAD@VCEvent@BB@@VCEventEntityIndex@GGL@@VCSerfBehavior@4@X@EGL@@`
     [0x0041a080] `.?AV?$THandler@$0BIAAC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x00419fc0`)
  context:
     [0x00419ec0] `.?AV?$THandler@$0GN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419f10] `.?AV?$THandler@$0ID@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419f60] `.?AV?$THandler@$0BAAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x00419fc0] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a020] `.?AV?$THandler@$0BEAAD@VCEvent@BB@@VCEventEntityIndex@GGL@@VCSerfBehavior@4@X@EGL@@`
     [0x0041a080] `.?AV?$THandler@$0BIAAC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a0f0] `.?AV?$THandler@$0BAAAJ@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BEAAD@VCEvent@BB@@VCEventEntityIndex@GGL@@VCSerfBehavior@4@X@EGL@@` (pattern `CSerfBehavior`, offset `0x0041a020`)
  context:
     [0x00419f10] `.?AV?$THandler@$0ID@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x00419f60] `.?AV?$THandler@$0BAAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x00419fc0] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x0041a020] `.?AV?$THandler@$0BEAAD@VCEvent@BB@@VCEventEntityIndex@GGL@@VCSerfBehavior@4@X@EGL@@`
     [0x0041a080] `.?AV?$THandler@$0BIAAC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a0f0] `.?AV?$THandler@$0BAAAJ@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a150] `.?AV?$THandler@$0BAAAK@VCEvent@BB@@VCEventEntityGetBool@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BIAAC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x0041a080`)
  context:
     [0x00419f60] `.?AV?$THandler@$0BAAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x00419fc0] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a020] `.?AV?$THandler@$0BEAAD@VCEvent@BB@@VCEventEntityIndex@GGL@@VCSerfBehavior@4@X@EGL@@`
  >> [0x0041a080] `.?AV?$THandler@$0BIAAC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a0f0] `.?AV?$THandler@$0BAAAJ@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a150] `.?AV?$THandler@$0BAAAK@VCEvent@BB@@VCEventEntityGetBool@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a1b8] `.?AV?$THandler@$0BEAAF@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BAAAJ@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x0041a0f0`)
  context:
     [0x00419fc0] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a020] `.?AV?$THandler@$0BEAAD@VCEvent@BB@@VCEventEntityIndex@GGL@@VCSerfBehavior@4@X@EGL@@`
     [0x0041a080] `.?AV?$THandler@$0BIAAC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x0041a0f0] `.?AV?$THandler@$0BAAAJ@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a150] `.?AV?$THandler@$0BAAAK@VCEvent@BB@@VCEventEntityGetBool@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a1b8] `.?AV?$THandler@$0BEAAF@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a208] `.?AV?$THandler@$0BEAAG@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BAAAK@VCEvent@BB@@VCEventEntityGetBool@EGL@@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x0041a150`)
  context:
     [0x0041a020] `.?AV?$THandler@$0BEAAD@VCEvent@BB@@VCEventEntityIndex@GGL@@VCSerfBehavior@4@X@EGL@@`
     [0x0041a080] `.?AV?$THandler@$0BIAAC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a0f0] `.?AV?$THandler@$0BAAAJ@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x0041a150] `.?AV?$THandler@$0BAAAK@VCEvent@BB@@VCEventEntityGetBool@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a1b8] `.?AV?$THandler@$0BEAAF@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a208] `.?AV?$THandler@$0BEAAG@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a258] `.?AV?$THandler@$0BEAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BEAAF@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x0041a1b8`)
  context:
     [0x0041a080] `.?AV?$THandler@$0BIAAC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a0f0] `.?AV?$THandler@$0BAAAJ@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a150] `.?AV?$THandler@$0BAAAK@VCEvent@BB@@VCEventEntityGetBool@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x0041a1b8] `.?AV?$THandler@$0BEAAF@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a208] `.?AV?$THandler@$0BEAAG@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a258] `.?AV?$THandler@$0BEAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a2c8] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BEAAG@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x0041a208`)
  context:
     [0x0041a0f0] `.?AV?$THandler@$0BAAAJ@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a150] `.?AV?$THandler@$0BAAAK@VCEvent@BB@@VCEventEntityGetBool@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a1b8] `.?AV?$THandler@$0BEAAF@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x0041a208] `.?AV?$THandler@$0BEAAG@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a258] `.?AV?$THandler@$0BEAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a2c8] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a338] `.?AV?$THandler@$0BFAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BEAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x0041a258`)
  context:
     [0x0041a150] `.?AV?$THandler@$0BAAAK@VCEvent@BB@@VCEventEntityGetBool@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a1b8] `.?AV?$THandler@$0BEAAF@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a208] `.?AV?$THandler@$0BEAAG@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x0041a258] `.?AV?$THandler@$0BEAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a2c8] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a338] `.?AV?$THandler@$0BFAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a394] `.?AV?$TStateHandler@VCSerfBehavior@GGL@@@EGL@@`
- hit: `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x0041a2c8`)
  context:
     [0x0041a1b8] `.?AV?$THandler@$0BEAAF@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a208] `.?AV?$THandler@$0BEAAG@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a258] `.?AV?$THandler@$0BEAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x0041a2c8] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a338] `.?AV?$THandler@$0BFAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a394] `.?AV?$TStateHandler@VCSerfBehavior@GGL@@@EGL@@`
     [0x0041a3cc] `.?AVCFeedbackEventResource@GGL@@`
- hit: `.?AV?$THandler@$0BFAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x0041a338`)
  context:
     [0x0041a208] `.?AV?$THandler@$0BEAAG@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a258] `.?AV?$THandler@$0BEAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a2c8] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x0041a338] `.?AV?$THandler@$0BFAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a394] `.?AV?$TStateHandler@VCSerfBehavior@GGL@@@EGL@@`
     [0x0041a3cc] `.?AVCFeedbackEventResource@GGL@@`
     [0x0041a4d8] `.?AVCSerfBattleBehaviorProps@GGL@@`
- hit: `.?AV?$TStateHandler@VCSerfBehavior@GGL@@@EGL@@` (pattern `CSerfBehavior`, offset `0x0041a394`)
  context:
     [0x0041a258] `.?AV?$THandler@$0BEAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a2c8] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x0041a338] `.?AV?$THandler@$0BFAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x0041a394] `.?AV?$TStateHandler@VCSerfBehavior@GGL@@@EGL@@`
     [0x0041a3cc] `.?AVCFeedbackEventResource@GGL@@`
     [0x0041a4d8] `.?AVCSerfBattleBehaviorProps@GGL@@`
     [0x0041a504] `.?AVCSerfBattleBehavior@GGL@@`

## task_ids_worker_camp

- patterns: 10 | hits: 10

- hit: `TASK_GO_TO_CAMP` (pattern `TASK_GO_TO_CAMP`, offset `0x00371788`)
  context:
     [0x0037174c] `TASK_WANDER`
     [0x00371758] `TASK_BACK_TO_DEFAULT_TASKLIST`
     [0x00371778] `TASK_WAIT_UNTIL`
  >> [0x00371788] `TASK_GO_TO_CAMP`
     [0x00371798] `TASK_LEAVE_CAMP`
     [0x003717a8] `TASK_RESOLVE_COLLISION`
     [0x003717c0] `TASK_LEFT_BUILDING`
- hit: `TASK_LEAVE_CAMP` (pattern `TASK_LEAVE_CAMP`, offset `0x00371798`)
  context:
     [0x00371758] `TASK_BACK_TO_DEFAULT_TASKLIST`
     [0x00371778] `TASK_WAIT_UNTIL`
     [0x00371788] `TASK_GO_TO_CAMP`
  >> [0x00371798] `TASK_LEAVE_CAMP`
     [0x003717a8] `TASK_RESOLVE_COLLISION`
     [0x003717c0] `TASK_LEFT_BUILDING`
     [0x003717d4] `TASK_GO_TO_FREE_POSITION`
- hit: `TASK_GO_TO_EAT_BUILDING` (pattern `TASK_GO_TO_EAT_BUILDING`, offset `0x00371a88`)
  context:
     [0x00371a40] `TASK_CONSUME_RESOURCE`
     [0x00371a58] `TASK_MINED_RESOURCE`
     [0x00371a6c] `TASK_GO_TO_WORK_BUILDING`
  >> [0x00371a88] `TASK_GO_TO_EAT_BUILDING`
     [0x00371aa0] `TASK_GO_TO_REST_BUILDING`
     [0x00371abc] `TASK_GO_TO_LEAVE_BUILDING`
     [0x00371ad8] `TASK_NEW_MOTIVATION_MODIFIER`
- hit: `TASK_GO_TO_REST_BUILDING` (pattern `TASK_GO_TO_REST_BUILDING`, offset `0x00371aa0`)
  context:
     [0x00371a58] `TASK_MINED_RESOURCE`
     [0x00371a6c] `TASK_GO_TO_WORK_BUILDING`
     [0x00371a88] `TASK_GO_TO_EAT_BUILDING`
  >> [0x00371aa0] `TASK_GO_TO_REST_BUILDING`
     [0x00371abc] `TASK_GO_TO_LEAVE_BUILDING`
     [0x00371ad8] `TASK_NEW_MOTIVATION_MODIFIER`
     [0x00371af8] `TASK_CHECK_MOTIVATION`
- hit: `TASK_CHANGE_WORK_TIME_CAMP` (pattern `TASK_CHANGE_WORK_TIME_CAMP`, offset `0x00371d24`)
  context:
     [0x00371ccc] `TASK_CHANGE_WORK_TIME_WORK`
     [0x00371ce8] `TASK_CHANGE_WORK_TIME_FARM`
     [0x00371d04] `TASK_CHANGE_WORK_TIME_RESIDENCE`
  >> [0x00371d24] `TASK_CHANGE_WORK_TIME_CAMP`
     [0x00371d40] `TASK_GO_TO_SUPPLIER`
     [0x00371d54] `TASK_DO_WORK_AT_FOUNDRY`
     [0x00371d6c] `TASK_CREATE_CANNON`
- hit: `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS` (pattern `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS`, offset `0x00371d9c`)
  context:
     [0x00371d54] `TASK_DO_WORK_AT_FOUNDRY`
     [0x00371d6c] `TASK_CREATE_CANNON`
     [0x00371d80] `TASK_SET_CANNON_PROGRESS`
  >> [0x00371d9c] `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS`
     [0x00371dc4] `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS`
     [0x00371dec] `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS`
     [0x00371e14] `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS`
- hit: `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS` (pattern `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS`, offset `0x00371dc4`)
  context:
     [0x00371d6c] `TASK_CREATE_CANNON`
     [0x00371d80] `TASK_SET_CANNON_PROGRESS`
     [0x00371d9c] `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS`
  >> [0x00371dc4] `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS`
     [0x00371dec] `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS`
     [0x00371e14] `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS`
     [0x00371e3c] `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS`
- hit: `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS` (pattern `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS`, offset `0x00371dec`)
  context:
     [0x00371d80] `TASK_SET_CANNON_PROGRESS`
     [0x00371d9c] `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS`
     [0x00371dc4] `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS`
  >> [0x00371dec] `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS`
     [0x00371e14] `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS`
     [0x00371e3c] `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS`
     [0x00371e6c] `TASK_TAKE_FROM_STOCK`
- hit: `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS` (pattern `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS`, offset `0x00371e14`)
  context:
     [0x00371d9c] `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS`
     [0x00371dc4] `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS`
     [0x00371dec] `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS`
  >> [0x00371e14] `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS`
     [0x00371e3c] `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS`
     [0x00371e6c] `TASK_TAKE_FROM_STOCK`
     [0x00371e84] `TASK_SET_CARRIER_MODEL`
- hit: `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS` (pattern `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS`, offset `0x00371e3c`)
  context:
     [0x00371dc4] `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS`
     [0x00371dec] `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS`
     [0x00371e14] `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS`
  >> [0x00371e3c] `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS`
     [0x00371e6c] `TASK_TAKE_FROM_STOCK`
     [0x00371e84] `TASK_SET_CARRIER_MODEL`
     [0x00371e9c] `TASK_CHECK_GO_TO_SUPPLIER_SUCCESS`

## worker_alarm_and_flight

- patterns: 4 | hits: 14

- hit: `WorkerAlarmModeActive` (pattern `WorkerAlarmMode`, offset `0x0036ee00`)
  context:
     [0x0036edc8] `Slots`
     [0x0036edd0] `OvertimeRechargeTime`
     [0x0036ede8] `MostRecentDepartureTurn`
  >> [0x0036ee00] `WorkerAlarmModeActive`
     [0x0036ee18] `UpgradeProgress`
     [0x0036ee28] `RepairProgress`
     [0x0036ee38] `ConstructionProgress`
- hit: `WorkerFlightDistance` (pattern `WorkerFlightDistance`, offset `0x0036f19c`)
  context:
     [0x0036f144] `EnergyRequiredForWeatherChange`
     [0x0036f164] `BuildingRecentlyAttackedDuration`
     [0x0036f188] `MaxExperiencePoints`
  >> [0x0036f19c] `WorkerFlightDistance`
     [0x0036f1b4] `DefenderMissChance`
     [0x0036f1c8] `DefenderProjectileDamageClass`
     [0x0036f1e8] `DefenderProjectileDamage`
- hit: `WorkerAlarmMode` (pattern `WorkerAlarmMode`, offset `0x0036fda0`)
  context:
     [0x0036fd58] `PlayerGameStateChangeGameTurn`
     [0x0036fd78] `PlayerHasLeftGameFlag`
     [0x0036fd90] `PlayerGameState`
  >> [0x0036fda0] `WorkerAlarmMode`
     [0x0036fdb0] `NumberOfBuyableHeros`
     [0x0036fdc8] `DurationOfWeatherChange`
     [0x0036fde0] `CurrentMaxMotivation`
- hit: `EnterWorkerAlarmMode` (pattern `WorkerAlarmMode`, offset `0x0037de6c`)
  context:
     [0x0037de30] `ChangeToBattleSerf`
     [0x0037de44] `EnterSerfAlarmMode`
     [0x0037de58] `QuitSerfAlarmMode`
  >> [0x0037de6c] `EnterWorkerAlarmMode`
     [0x0037de84] `QuitWorkerAlarmMode`
     [0x0037de98] `CancelState`
     [0x0037dea4] `State_SetExclusiveMessageRecipient`
- hit: `QuitWorkerAlarmMode` (pattern `WorkerAlarmMode`, offset `0x0037de84`)
  context:
     [0x0037de44] `EnterSerfAlarmMode`
     [0x0037de58] `QuitSerfAlarmMode`
     [0x0037de6c] `EnterWorkerAlarmMode`
  >> [0x0037de84] `QuitWorkerAlarmMode`
     [0x0037de98] `CancelState`
     [0x0037dea4] `State_SetExclusiveMessageRecipient`
     [0x0037dec8] `GetCurrentStateName`
- hit: `.?AVCWorkerAlarmModeBehaviorProps@GGL@@` (pattern `WorkerAlarmMode`, offset `0x004164bc`)
  context:
     [0x004162c8] `.?AV?$THandler@$0CAAAF@VCEvent@BB@@V12@VCWorkerBattleBehavior@GGL@@X@EGL@@`
     [0x00416320] `.?AV?$THandler@$0BBAAD@VCEvent@BB@@VCEventPosition@EGL@@VCWorkerBattleBehavior@GGL@@X@EGL@@`
     [0x00416388] `.?AV?$THandler@$0BIAAJ@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBattleBehavior@GGL@@X@EGL@@`
  >> [0x004164bc] `.?AVCWorkerAlarmModeBehaviorProps@GGL@@`
     [0x004164ec] `.?AVCWorkerAlarmModeBehavior@GGL@@`
     [0x00416518] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416570] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
- hit: `.?AVCWorkerAlarmModeBehavior@GGL@@` (pattern `WorkerAlarmMode`, offset `0x004164ec`)
  context:
     [0x00416320] `.?AV?$THandler@$0BBAAD@VCEvent@BB@@VCEventPosition@EGL@@VCWorkerBattleBehavior@GGL@@X@EGL@@`
     [0x00416388] `.?AV?$THandler@$0BIAAJ@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBattleBehavior@GGL@@X@EGL@@`
     [0x004164bc] `.?AVCWorkerAlarmModeBehaviorProps@GGL@@`
  >> [0x004164ec] `.?AVCWorkerAlarmModeBehavior@GGL@@`
     [0x00416518] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416570] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x004165c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `WorkerAlarmMode`, offset `0x00416518`)
  context:
     [0x00416388] `.?AV?$THandler@$0BIAAJ@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBattleBehavior@GGL@@X@EGL@@`
     [0x004164bc] `.?AVCWorkerAlarmModeBehaviorProps@GGL@@`
     [0x004164ec] `.?AVCWorkerAlarmModeBehavior@GGL@@`
  >> [0x00416518] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416570] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x004165c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416630] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `WorkerAlarmMode`, offset `0x00416570`)
  context:
     [0x004164bc] `.?AVCWorkerAlarmModeBehaviorProps@GGL@@`
     [0x004164ec] `.?AVCWorkerAlarmModeBehavior@GGL@@`
     [0x00416518] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
  >> [0x00416570] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x004165c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416630] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x00416690] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `WorkerAlarmMode`, offset `0x004165c8`)
  context:
     [0x004164ec] `.?AVCWorkerAlarmModeBehavior@GGL@@`
     [0x00416518] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416570] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
  >> [0x004165c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416630] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x00416690] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x004166f0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `WorkerAlarmMode`, offset `0x00416630`)
  context:
     [0x00416518] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416570] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x004165c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
  >> [0x00416630] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x00416690] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x004166f0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x00416750] `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `WorkerAlarmMode`, offset `0x00416690`)
  context:
     [0x00416570] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x004165c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416630] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
  >> [0x00416690] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x004166f0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x00416750] `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x0041688c] `.?AVCEventStartAlphaBlending@GGL@@`
- hit: `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `WorkerAlarmMode`, offset `0x004166f0`)
  context:
     [0x004165c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x00416630] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x00416690] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
  >> [0x004166f0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x00416750] `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x0041688c] `.?AVCEventStartAlphaBlending@GGL@@`
     [0x00416a80] `.?AVCBehaviorWalkCommand@GGL@@`
- hit: `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `WorkerAlarmMode`, offset `0x00416750`)
  context:
     [0x00416630] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x00416690] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x004166f0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
  >> [0x00416750] `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x0041688c] `.?AVCEventStartAlphaBlending@GGL@@`
     [0x00416a80] `.?AVCBehaviorWalkCommand@GGL@@`
     [0x00416aa8] `.?AV?$THandler@$0CM@VCGLETaskArgs@EGL@@V12@VCBehaviorWalkCommand@GGL@@H@EGL@@`

## attachments_and_entities

- patterns: 5 | hits: 7

- hit: `ATTACHMENT_WORKER_FARM` (pattern `ATTACHMENT_WORKER_FARM`, offset `0x00370db4`)
  context:
     [0x00370d38] `ATTACHMENT_APPROACHING_SERF_CONSTRUCTION_SITE`
     [0x00370d68] `ATTACHMENT_SERF_CONSTRUCTION_SITE`
     [0x00370d8c] `ATTACHMENT_CONSTRUCTION_SITE_BUILDING`
  >> [0x00370db4] `ATTACHMENT_WORKER_FARM`
     [0x00370dcc] `ATTACHMENT_WORKER_RESIDENCE`
     [0x00370de8] `ATTACHMENT_WORKER_WORKPLACE`
     [0x00370e04] `ATTACHMENT_MINE_RESOURCE`
- hit: `ATTACHMENT_WORKER_RESIDENCE` (pattern `ATTACHMENT_WORKER_RESIDENCE`, offset `0x00370dcc`)
  context:
     [0x00370d68] `ATTACHMENT_SERF_CONSTRUCTION_SITE`
     [0x00370d8c] `ATTACHMENT_CONSTRUCTION_SITE_BUILDING`
     [0x00370db4] `ATTACHMENT_WORKER_FARM`
  >> [0x00370dcc] `ATTACHMENT_WORKER_RESIDENCE`
     [0x00370de8] `ATTACHMENT_WORKER_WORKPLACE`
     [0x00370e04] `ATTACHMENT_MINE_RESOURCE`
     [0x00370e20] `ATTACHMENT_MINE_LORRY`
- hit: `ATTACHMENT_CAMP_SETTLER` (pattern `ATTACHMENT_CAMP_SETTLER`, offset `0x00370f18`)
  context:
     [0x00370ec4] `ATTACHMENT_LEADER_SOLDIER`
     [0x00370ee0] `ATTACHMENT_ATTACKER_TARGET`
     [0x00370efc] `ATTACHMENT_ATTACKED_DEAD`
  >> [0x00370f18] `ATTACHMENT_CAMP_SETTLER`
     [0x00370f30] `ATTACHMENT_ATTACKER_COMMAND_TARGET`
     [0x00370f54] `ATTACHMENT_BUILDING_BASE`
     [0x00370f70] `ATTACHMENT_FOLLOWER_FOLLOWED`
- hit: `SetWorkTaskListsPerCycle` (pattern `TaskLists`, offset `0x00373e7c`)
  context:
     [0x00373e50] `GetEntityDamage`
     [0x00373e60] `GetEntityArmor`
     [0x00373e70] `MoveSettler`
  >> [0x00373e7c] `SetWorkTaskListsPerCycle`
     [0x00373e98] `FillSettlerUpgradeCostsTable`
     [0x00373eb8] `GetSettlerTypeByUpgradeCategory`
     [0x00373ed8] `DEBUG_UpgradeSettler`
- hit: `XD_Camp_Internal` (pattern `XD_Camp_Internal`, offset `0x003778ac`)
  context:
     [0x00377884] `RemoveDelay`
     [0x00377890] `Slot`
     [0x00377898] `NumTurnsToDeletion`
  >> [0x003778ac] `XD_Camp_Internal`
     [0x00377924] `DiscoveryRange`
     [0x00377934] `DurationSeconds`
     [0x003779bc] `GetBuildingsByUpgradeCategory`
- hit: `TaskLists` (pattern `TaskLists`, offset `0x00384584`)
  context:
     [0x003844e4] `TASK_SPAWN_PARTICLE_EFFECT`
     [0x00384500] `TASK_ACTIVATE_UVANIM`
     [0x00384578] `Map Script`
  >> [0x00384584] `TaskLists`
     [0x00384590] `AnimSets`
     [0x0038459c] `GGL_Effects`
     [0x003845a8] `GameCallback_SetDefaultValues`
- hit: `Data\Config\TaskLists\` (pattern `TaskLists`, offset `0x00384610`)
  context:
     [0x003845a8] `GameCallback_SetDefaultValues`
     [0x003845c8] `GameCallback_NewGame`
     [0x00384608] `  ID:`
  >> [0x00384610] `Data\Config\TaskLists\`
     [0x00384628] `Task`
     [0x00384630] `PrincipalTask`
     [0x0038465e] `Y@MessageAttacked`

## Limits

- Static string/RTTI evidence only, no instruction-level control-flow graph.
- Mangled handler names expose event/task wiring but not exact branch predicates.
