# Engine Branch Evidence

- Binary: `C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games\theSettlers5\bin\SettlersHoK.exe`
- Size: 11018672 bytes
- Generated: 2026-02-11T19:47:00.905150+00:00

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

- hit: `WorkTimeBase` (pattern `WorkTimeBase`, offset `0x007d9ce0`)
  context:
     [0x007d9c7c] `MotivationThresholdAngry`
     [0x007d9c98] `MotivationThresholdLeave`
     [0x007d9cb4] `AverageMotivationVillageCenterLockThreshold`
  >> [0x007d9ce0] `WorkTimeBase`
     [0x007d9cf0] `WorkTimeThresholdWork`
     [0x007d9d08] `WorkTimeThresholdFarm`
     [0x007d9d20] `WorkTimeThresholdResidence`
- hit: `WorkTimeThresholdWork` (pattern `WorkTimeThresholdWork`, offset `0x007d9cf0`)
  context:
     [0x007d9c98] `MotivationThresholdLeave`
     [0x007d9cb4] `AverageMotivationVillageCenterLockThreshold`
     [0x007d9ce0] `WorkTimeBase`
  >> [0x007d9cf0] `WorkTimeThresholdWork`
     [0x007d9d08] `WorkTimeThresholdFarm`
     [0x007d9d20] `WorkTimeThresholdResidence`
     [0x007d9d3c] `WorkTimeThresholdCampFire`
- hit: `WorkTimeThresholdFarm` (pattern `WorkTimeThresholdFarm`, offset `0x007d9d08`)
  context:
     [0x007d9cb4] `AverageMotivationVillageCenterLockThreshold`
     [0x007d9ce0] `WorkTimeBase`
     [0x007d9cf0] `WorkTimeThresholdWork`
  >> [0x007d9d08] `WorkTimeThresholdFarm`
     [0x007d9d20] `WorkTimeThresholdResidence`
     [0x007d9d3c] `WorkTimeThresholdCampFire`
     [0x007d9d58] `MotivationGameStartMaxMotivation`
- hit: `WorkTimeThresholdResidence` (pattern `WorkTimeThresholdResidence`, offset `0x007d9d20`)
  context:
     [0x007d9ce0] `WorkTimeBase`
     [0x007d9cf0] `WorkTimeThresholdWork`
     [0x007d9d08] `WorkTimeThresholdFarm`
  >> [0x007d9d20] `WorkTimeThresholdResidence`
     [0x007d9d3c] `WorkTimeThresholdCampFire`
     [0x007d9d58] `MotivationGameStartMaxMotivation`
     [0x007d9d7c] `MotivationAbsoluteMaxMotivation`
- hit: `WorkTimeThresholdCampFire` (pattern `WorkTimeThresholdCampFire`, offset `0x007d9d3c`)
  context:
     [0x007d9cf0] `WorkTimeThresholdWork`
     [0x007d9d08] `WorkTimeThresholdFarm`
     [0x007d9d20] `WorkTimeThresholdResidence`
  >> [0x007d9d3c] `WorkTimeThresholdCampFire`
     [0x007d9d58] `MotivationGameStartMaxMotivation`
     [0x007d9d7c] `MotivationAbsoluteMaxMotivation`
     [0x007d9d9c] `MotivationMillisecondsWithoutJob`

## worker_distance_and_assignment

- patterns: 11 | hits: 11

- hit: `ReAttachWorkerFrequency` (pattern `ReAttachWorkerFrequency`, offset `0x007dac58`)
  context:
     [0x007dac20] `AttractionFrequency`
     [0x007dac34] `PaydayFrequency`
     [0x007dac44] `EntityTypeBanTime`
  >> [0x007dac58] `ReAttachWorkerFrequency`
     [0x007dac70] `PlayerMoneyDispo`
     [0x007dac84] `MaximumDistanceWorkerToFarm`
     [0x007daca0] `MaximumDistanceWorkerToResidence`
- hit: `MaximumDistanceWorkerToFarm` (pattern `MaximumDistanceWorkerToFarm`, offset `0x007dac84`)
  context:
     [0x007dac44] `EntityTypeBanTime`
     [0x007dac58] `ReAttachWorkerFrequency`
     [0x007dac70] `PlayerMoneyDispo`
  >> [0x007dac84] `MaximumDistanceWorkerToFarm`
     [0x007daca0] `MaximumDistanceWorkerToResidence`
     [0x007dace4] `GetLogicPropertiesMotivationThresholdHappy`
     [0x007dad10] `GetLogicPropertiesMotivationThresholdSad`
- hit: `MaximumDistanceWorkerToResidence` (pattern `MaximumDistanceWorkerToResidence`, offset `0x007daca0`)
  context:
     [0x007dac58] `ReAttachWorkerFrequency`
     [0x007dac70] `PlayerMoneyDispo`
     [0x007dac84] `MaximumDistanceWorkerToFarm`
  >> [0x007daca0] `MaximumDistanceWorkerToResidence`
     [0x007dace4] `GetLogicPropertiesMotivationThresholdHappy`
     [0x007dad10] `GetLogicPropertiesMotivationThresholdSad`
     [0x007dad3c] `GetLogicPropertiesMotivationThresholdAngry`
- hit: `SetWorkTaskListsPerCycle` (pattern `SetWorkTaskListsPerCycle`, offset `0x007dd104`)
  context:
     [0x007dd0c4] `GetNextLeader`
     [0x007dd0d4] `MoveSettler`
     [0x007dd0e0] `GetSettlerTypesInUpgradeCategory`
  >> [0x007dd104] `SetWorkTaskListsPerCycle`
     [0x007dd120] `SettlerStand`
     [0x007dd130] `FillSettlerUpgradeCostsTable`
     [0x007dd150] `SettlerAggressive`
- hit: `GetSettlersResidence` (pattern `GetSettlersResidence`, offset `0x007dd244`)
  context:
     [0x007dd1fc] `GetBattleSerfSecondsLeft`
     [0x007dd218] `GetSettlersWorkBuilding`
     [0x007dd230] `SetModelAndAnimSet`
  >> [0x007dd244] `GetSettlersResidence`
     [0x007dd25c] `GetBlessCostByBlessCategory`
     [0x007dd278] `GetMaximumFaith`
     [0x007dd288] `GetSettlersFarm`
- hit: `GetSettlersFarm` (pattern `GetSettlersFarm`, offset `0x007dd288`)
  context:
     [0x007dd244] `GetSettlersResidence`
     [0x007dd25c] `GetBlessCostByBlessCategory`
     [0x007dd278] `GetMaximumFaith`
  >> [0x007dd288] `GetSettlersFarm`
     [0x007dd2a8] `CheckSettlerPlacement`
     [0x007dd2c0] `IsSettlerAtWork`
     [0x007dd2d0] `GetSettlersAttractionLimitValue`
- hit: `IsSettlerAtResidence` (pattern `IsSettlerAtResidence`, offset `0x007dd2f0`)
  context:
     [0x007dd2a8] `CheckSettlerPlacement`
     [0x007dd2c0] `IsSettlerAtWork`
     [0x007dd2d0] `GetSettlersAttractionLimitValue`
  >> [0x007dd2f0] `IsSettlerAtResidence`
     [0x007dd308] `GetAttractionLimitValueByEntityType`
     [0x007dd32c] `IsSettlerAtFarm`
     [0x007dd33c] `GetLeadersGroupAttractionLimitValue`
- hit: `IsSettlerAtFarm` (pattern `IsSettlerAtFarm`, offset `0x007dd32c`)
  context:
     [0x007dd2d0] `GetSettlersAttractionLimitValue`
     [0x007dd2f0] `IsSettlerAtResidence`
     [0x007dd308] `GetAttractionLimitValueByEntityType`
  >> [0x007dd32c] `IsSettlerAtFarm`
     [0x007dd33c] `GetLeadersGroupAttractionLimitValue`
     [0x007dd360] `GetSettlersMotivation`
     [0x007dd378] `GetLeaderExperienceLevel`
- hit: `GetNextWorkerWithoutFarmOrResidence` (pattern `GetNextWorkerWithoutFarmOrResidence`, offset `0x007dd3c0`)
  context:
     [0x007dd378] `GetLeaderExperienceLevel`
     [0x007dd394] `ChangeSettlerPlayerID`
     [0x007dd3ac] `FillSerfCostsTable`
  >> [0x007dd3c0] `GetNextWorkerWithoutFarmOrResidence`
     [0x007dd3e4] `IsWorker`
     [0x007dd3f0] `IsSerf`
     [0x007dd3f8] `GetNextWorkerWithoutFarm`
- hit: `GetNextWorkerWithoutFarm` (pattern `GetNextWorkerWithoutFarm`, offset `0x007dd3f8`)
  context:
     [0x007dd3c0] `GetNextWorkerWithoutFarmOrResidence`
     [0x007dd3e4] `IsWorker`
     [0x007dd3f0] `IsSerf`
  >> [0x007dd3f8] `GetNextWorkerWithoutFarm`
     [0x007dd414] `IsLeader`
     [0x007dd420] `GetNextWorkerWithoutResidence`
     [0x007dd440] `IsHero`
- hit: `GetNextWorkerWithoutResidence` (pattern `GetNextWorkerWithoutResidence`, offset `0x007dd420`)
  context:
     [0x007dd3f0] `IsSerf`
     [0x007dd3f8] `GetNextWorkerWithoutFarm`
     [0x007dd414] `IsLeader`
  >> [0x007dd420] `GetNextWorkerWithoutResidence`
     [0x007dd440] `IsHero`
     [0x007dd448] `HeroGetActionPoints`
     [0x007dd45c] `HeroGetMaxActionPoints`

## camp_behavior_classes

- patterns: 8 | hits: 18

- hit: `.?AVCCamperBehaviorProperties@GGL@@` (pattern `CCamperBehaviorProperties`, offset `0x00997834`)
  context:
     [0x009976e0] `.?AV?$THandler@$0BFAAO@VCEvent@BB@@VCEvent1Entity@EGL@@VCCamouflageBehavior@GGL@@X@EGL@@`
     [0x00997748] `.?AV?$THandler@$0BGABG@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCamouflageBehavior@GGL@@X@EGL@@`
     [0x009977c0] `.?AV?$THandler@$0BGABH@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCamouflageBehavior@GGL@@X@EGL@@`
  >> [0x00997834] `.?AVCCamperBehaviorProperties@GGL@@`
     [0x00997860] `.?AVCCamperBehavior@GGL@@`
     [0x00997884] `.?AVCCampBehavior@GGL@@`
     [0x009978a4] `.?AVCCampBehaviorProperties@GGL@@`
- hit: `.?AVCCamperBehavior@GGL@@` (pattern `CCamperBehavior`, offset `0x00997860`)
  context:
     [0x00997748] `.?AV?$THandler@$0BGABG@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCamouflageBehavior@GGL@@X@EGL@@`
     [0x009977c0] `.?AV?$THandler@$0BGABH@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCamouflageBehavior@GGL@@X@EGL@@`
     [0x00997834] `.?AVCCamperBehaviorProperties@GGL@@`
  >> [0x00997860] `.?AVCCamperBehavior@GGL@@`
     [0x00997884] `.?AVCCampBehavior@GGL@@`
     [0x009978a4] `.?AVCCampBehaviorProperties@GGL@@`
     [0x009978d0] `.?AVCEventGetPositionFromID@GGL@@`
- hit: `.?AVCCampBehavior@GGL@@` (pattern `CCampBehavior`, offset `0x00997884`)
  context:
     [0x009977c0] `.?AV?$THandler@$0BGABH@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCamouflageBehavior@GGL@@X@EGL@@`
     [0x00997834] `.?AVCCamperBehaviorProperties@GGL@@`
     [0x00997860] `.?AVCCamperBehavior@GGL@@`
  >> [0x00997884] `.?AVCCampBehavior@GGL@@`
     [0x009978a4] `.?AVCCampBehaviorProperties@GGL@@`
     [0x009978d0] `.?AVCEventGetPositionFromID@GGL@@`
     [0x009978fc] `.?AVCUnblockedSquarePredicate@EGL@@`
- hit: `.?AVCCampBehaviorProperties@GGL@@` (pattern `CCampBehaviorProperties`, offset `0x009978a4`)
  context:
     [0x00997834] `.?AVCCamperBehaviorProperties@GGL@@`
     [0x00997860] `.?AVCCamperBehavior@GGL@@`
     [0x00997884] `.?AVCCampBehavior@GGL@@`
  >> [0x009978a4] `.?AVCCampBehaviorProperties@GGL@@`
     [0x009978d0] `.?AVCEventGetPositionFromID@GGL@@`
     [0x009978fc] `.?AVCUnblockedSquarePredicate@EGL@@`
     [0x00997928] `.?AV?$THandler@$0BDABA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
- hit: `.?AVCEventGetPositionFromID@GGL@@` (pattern `CEventGetPositionFromID`, offset `0x009978d0`)
  context:
     [0x00997860] `.?AVCCamperBehavior@GGL@@`
     [0x00997884] `.?AVCCampBehavior@GGL@@`
     [0x009978a4] `.?AVCCampBehaviorProperties@GGL@@`
  >> [0x009978d0] `.?AVCEventGetPositionFromID@GGL@@`
     [0x009978fc] `.?AVCUnblockedSquarePredicate@EGL@@`
     [0x00997928] `.?AV?$THandler@$0BDABA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00997998] `.?AV?$THandler@$0BDAAN@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
- hit: `.?AVCUnblockedSquarePredicate@EGL@@` (pattern `CUnblockedSquarePredicate`, offset `0x009978fc`)
  context:
     [0x00997884] `.?AVCCampBehavior@GGL@@`
     [0x009978a4] `.?AVCCampBehaviorProperties@GGL@@`
     [0x009978d0] `.?AVCEventGetPositionFromID@GGL@@`
  >> [0x009978fc] `.?AVCUnblockedSquarePredicate@EGL@@`
     [0x00997928] `.?AV?$THandler@$0BDABA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00997998] `.?AV?$THandler@$0BDAAN@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00997a08] `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCCampBehavior@GGL@@X@EGL@@` (pattern `CCampBehavior`, offset `0x00997928`)
  context:
     [0x009978a4] `.?AVCCampBehaviorProperties@GGL@@`
     [0x009978d0] `.?AVCEventGetPositionFromID@GGL@@`
     [0x009978fc] `.?AVCUnblockedSquarePredicate@EGL@@`
  >> [0x00997928] `.?AV?$THandler@$0BDABA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00997998] `.?AV?$THandler@$0BDAAN@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00997a08] `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x00997a70] `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAN@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCampBehavior@GGL@@X@EGL@@` (pattern `CCampBehavior`, offset `0x00997998`)
  context:
     [0x009978d0] `.?AVCEventGetPositionFromID@GGL@@`
     [0x009978fc] `.?AVCUnblockedSquarePredicate@EGL@@`
     [0x00997928] `.?AV?$THandler@$0BDABA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
  >> [0x00997998] `.?AV?$THandler@$0BDAAN@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00997a08] `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x00997a70] `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x00997ad0] `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@` (pattern `CCampBehavior`, offset `0x00997a08`)
  context:
     [0x009978fc] `.?AVCUnblockedSquarePredicate@EGL@@`
     [0x00997928] `.?AV?$THandler@$0BDABA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00997998] `.?AV?$THandler@$0BDAAN@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
  >> [0x00997a08] `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x00997a70] `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x00997ad0] `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00997b2c] `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@`
- hit: `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@` (pattern `CCampBehavior`, offset `0x00997a70`)
  context:
     [0x00997928] `.?AV?$THandler@$0BDABA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00997998] `.?AV?$THandler@$0BDAAN@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00997a08] `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@`
  >> [0x00997a70] `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x00997ad0] `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00997b2c] `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@`
     [0x00997b64] `.?AVCPotentialCampSitePredicate@GGL@@`
- hit: `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@` (pattern `CCampBehavior`, offset `0x00997ad0`)
  context:
     [0x00997998] `.?AV?$THandler@$0BDAAN@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00997a08] `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x00997a70] `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@`
  >> [0x00997ad0] `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00997b2c] `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@`
     [0x00997b64] `.?AVCPotentialCampSitePredicate@GGL@@`
     [0x00997b98] `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@` (pattern `CCampBehavior`, offset `0x00997b2c`)
  context:
     [0x00997a08] `.?AV?$THandler@$0BDAAO@VCEvent@BB@@VCEventGetPositionFromID@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x00997a70] `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x00997ad0] `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@`
  >> [0x00997b2c] `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@`
     [0x00997b64] `.?AVCPotentialCampSitePredicate@GGL@@`
     [0x00997b98] `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00997bf0] `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
- hit: `.?AVCPotentialCampSitePredicate@GGL@@` (pattern `CPotentialCampSitePredicate`, offset `0x00997b64`)
  context:
     [0x00997a70] `.?AV?$THandler@$0BDAAP@VCEvent@BB@@VCEventEntityIndex@GGL@@VCCampBehavior@4@X@EGL@@`
     [0x00997ad0] `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00997b2c] `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@`
  >> [0x00997b64] `.?AVCPotentialCampSitePredicate@GGL@@`
     [0x00997b98] `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00997bf0] `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00997c48] `.?AV?$THandler@$0BDABC@VCEvent@BB@@V12@VCCamperBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@` (pattern `CCamperBehavior`, offset `0x00997b98`)
  context:
     [0x00997ad0] `.?AV?$THandler@$0BCAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCCampBehavior@GGL@@X@EGL@@`
     [0x00997b2c] `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@`
     [0x00997b64] `.?AVCPotentialCampSitePredicate@GGL@@`
  >> [0x00997b98] `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00997bf0] `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00997c48] `.?AV?$THandler@$0BDABC@VCEvent@BB@@V12@VCCamperBehavior@GGL@@X@EGL@@`
     [0x00997c98] `.?AV?$THandler@$0BDABB@VCEvent@BB@@VCEvent1Entity@EGL@@VCCamperBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@` (pattern `CCamperBehavior`, offset `0x00997bf0`)
  context:
     [0x00997b2c] `.?AV?$TStateHandler@VCCampBehavior@GGL@@@EGL@@`
     [0x00997b64] `.?AVCPotentialCampSitePredicate@GGL@@`
     [0x00997b98] `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
  >> [0x00997bf0] `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00997c48] `.?AV?$THandler@$0BDABC@VCEvent@BB@@V12@VCCamperBehavior@GGL@@X@EGL@@`
     [0x00997c98] `.?AV?$THandler@$0BDABB@VCEvent@BB@@VCEvent1Entity@EGL@@VCCamperBehavior@GGL@@X@EGL@@`
     [0x00997cf8] `.?AVCCampWithFreeSlotPredicate@GGL@@`
- hit: `.?AV?$THandler@$0BDABC@VCEvent@BB@@V12@VCCamperBehavior@GGL@@X@EGL@@` (pattern `CCamperBehavior`, offset `0x00997c48`)
  context:
     [0x00997b64] `.?AVCPotentialCampSitePredicate@GGL@@`
     [0x00997b98] `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00997bf0] `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
  >> [0x00997c48] `.?AV?$THandler@$0BDABC@VCEvent@BB@@V12@VCCamperBehavior@GGL@@X@EGL@@`
     [0x00997c98] `.?AV?$THandler@$0BDABB@VCEvent@BB@@VCEvent1Entity@EGL@@VCCamperBehavior@GGL@@X@EGL@@`
     [0x00997cf8] `.?AVCCampWithFreeSlotPredicate@GGL@@`
     [0x00997d28] `.?AVCCannonBallEffect@GGL@@`
- hit: `.?AV?$THandler@$0BDABB@VCEvent@BB@@VCEvent1Entity@EGL@@VCCamperBehavior@GGL@@X@EGL@@` (pattern `CCamperBehavior`, offset `0x00997c98`)
  context:
     [0x00997b98] `.?AV?$THandler@$0DL@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00997bf0] `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00997c48] `.?AV?$THandler@$0BDABC@VCEvent@BB@@V12@VCCamperBehavior@GGL@@X@EGL@@`
  >> [0x00997c98] `.?AV?$THandler@$0BDABB@VCEvent@BB@@VCEvent1Entity@EGL@@VCCamperBehavior@GGL@@X@EGL@@`
     [0x00997cf8] `.?AVCCampWithFreeSlotPredicate@GGL@@`
     [0x00997d28] `.?AVCCannonBallEffect@GGL@@`
     [0x00997d4c] `.?AVCCannonBallEffectProps@GGL@@`
- hit: `.?AVCCampWithFreeSlotPredicate@GGL@@` (pattern `CCampWithFreeSlotPredicate`, offset `0x00997cf8`)
  context:
     [0x00997bf0] `.?AV?$THandler@$0DM@VCGLETaskArgs@EGL@@V12@VCCamperBehavior@GGL@@H@EGL@@`
     [0x00997c48] `.?AV?$THandler@$0BDABC@VCEvent@BB@@V12@VCCamperBehavior@GGL@@X@EGL@@`
     [0x00997c98] `.?AV?$THandler@$0BDABB@VCEvent@BB@@VCEvent1Entity@EGL@@VCCamperBehavior@GGL@@X@EGL@@`
  >> [0x00997cf8] `.?AVCCampWithFreeSlotPredicate@GGL@@`
     [0x00997d28] `.?AVCCannonBallEffect@GGL@@`
     [0x00997d4c] `.?AVCCannonBallEffectProps@GGL@@`
     [0x00997d78] `.?AVCCannonBuilderBehavior@GGL@@`

## worker_behavior_classes

- patterns: 8 | hits: 133

- hit: `.?AVCSerfBehaviorProps@GGL@@` (pattern `CSerfBehaviorProps`, offset `0x009a0b3c`)
  context:
     [0x009a0a08] `.?AV?$THandler@$0CAAAF@VCEvent@BB@@V12@VCSerfBattleBehavior@GGL@@X@EGL@@`
     [0x009a0a60] `.?AV?$THandler@$0BBAAD@VCEvent@BB@@VCEventPosition@EGL@@VCSerfBattleBehavior@GGL@@X@EGL@@`
     [0x009a0ac8] `.?AV?$THandler@$0BIAAJ@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBattleBehavior@GGL@@X@EGL@@`
  >> [0x009a0b3c] `.?AVCSerfBehaviorProps@GGL@@`
     [0x009a0b64] `.?AVCSerfBehavior@GGL@@`
     [0x009a0b88] `.?AV?$THandler@$0BM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0bd8] `.?AV?$THandler@$0FL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AVCSerfBehavior@GGL@@` (pattern `CSerfBehavior`, offset `0x009a0b64`)
  context:
     [0x009a0a60] `.?AV?$THandler@$0BBAAD@VCEvent@BB@@VCEventPosition@EGL@@VCSerfBattleBehavior@GGL@@X@EGL@@`
     [0x009a0ac8] `.?AV?$THandler@$0BIAAJ@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBattleBehavior@GGL@@X@EGL@@`
     [0x009a0b3c] `.?AVCSerfBehaviorProps@GGL@@`
  >> [0x009a0b64] `.?AVCSerfBehavior@GGL@@`
     [0x009a0b88] `.?AV?$THandler@$0BM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0bd8] `.?AV?$THandler@$0FL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0c28] `.?AV?$THandler@$0IM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x009a0b88`)
  context:
     [0x009a0ac8] `.?AV?$THandler@$0BIAAJ@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBattleBehavior@GGL@@X@EGL@@`
     [0x009a0b3c] `.?AVCSerfBehaviorProps@GGL@@`
     [0x009a0b64] `.?AVCSerfBehavior@GGL@@`
  >> [0x009a0b88] `.?AV?$THandler@$0BM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0bd8] `.?AV?$THandler@$0FL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0c28] `.?AV?$THandler@$0IM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0c78] `.?AV?$THandler@$0FM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x009a0bd8`)
  context:
     [0x009a0b3c] `.?AVCSerfBehaviorProps@GGL@@`
     [0x009a0b64] `.?AVCSerfBehavior@GGL@@`
     [0x009a0b88] `.?AV?$THandler@$0BM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x009a0bd8] `.?AV?$THandler@$0FL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0c28] `.?AV?$THandler@$0IM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0c78] `.?AV?$THandler@$0FM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0cc8] `.?AV?$THandler@$0FN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0IM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x009a0c28`)
  context:
     [0x009a0b64] `.?AVCSerfBehavior@GGL@@`
     [0x009a0b88] `.?AV?$THandler@$0BM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0bd8] `.?AV?$THandler@$0FL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x009a0c28] `.?AV?$THandler@$0IM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0c78] `.?AV?$THandler@$0FM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0cc8] `.?AV?$THandler@$0FN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0d18] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x009a0c78`)
  context:
     [0x009a0b88] `.?AV?$THandler@$0BM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0bd8] `.?AV?$THandler@$0FL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0c28] `.?AV?$THandler@$0IM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x009a0c78] `.?AV?$THandler@$0FM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0cc8] `.?AV?$THandler@$0FN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0d18] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0d68] `.?AV?$THandler@$0GJ@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x009a0cc8`)
  context:
     [0x009a0bd8] `.?AV?$THandler@$0FL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0c28] `.?AV?$THandler@$0IM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0c78] `.?AV?$THandler@$0FM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x009a0cc8] `.?AV?$THandler@$0FN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0d18] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0d68] `.?AV?$THandler@$0GJ@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0db8] `.?AV?$THandler@$0GK@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x009a0d18`)
  context:
     [0x009a0c28] `.?AV?$THandler@$0IM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0c78] `.?AV?$THandler@$0FM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0cc8] `.?AV?$THandler@$0FN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x009a0d18] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0d68] `.?AV?$THandler@$0GJ@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0db8] `.?AV?$THandler@$0GK@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0e08] `.?AV?$THandler@$0II@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0GJ@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x009a0d68`)
  context:
     [0x009a0c78] `.?AV?$THandler@$0FM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0cc8] `.?AV?$THandler@$0FN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0d18] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x009a0d68] `.?AV?$THandler@$0GJ@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0db8] `.?AV?$THandler@$0GK@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0e08] `.?AV?$THandler@$0II@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0e58] `.?AV?$THandler@$0GL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0GK@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x009a0db8`)
  context:
     [0x009a0cc8] `.?AV?$THandler@$0FN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0d18] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0d68] `.?AV?$THandler@$0GJ@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x009a0db8] `.?AV?$THandler@$0GK@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0e08] `.?AV?$THandler@$0II@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0e58] `.?AV?$THandler@$0GL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0ea8] `.?AV?$THandler@$0GM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0II@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x009a0e08`)
  context:
     [0x009a0d18] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0d68] `.?AV?$THandler@$0GJ@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0db8] `.?AV?$THandler@$0GK@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x009a0e08] `.?AV?$THandler@$0II@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0e58] `.?AV?$THandler@$0GL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0ea8] `.?AV?$THandler@$0GM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0ef8] `.?AV?$THandler@$0GN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0GL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x009a0e58`)
  context:
     [0x009a0d68] `.?AV?$THandler@$0GJ@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0db8] `.?AV?$THandler@$0GK@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0e08] `.?AV?$THandler@$0II@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x009a0e58] `.?AV?$THandler@$0GL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0ea8] `.?AV?$THandler@$0GM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0ef8] `.?AV?$THandler@$0GN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0f48] `.?AV?$THandler@$0ID@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0GM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x009a0ea8`)
  context:
     [0x009a0db8] `.?AV?$THandler@$0GK@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0e08] `.?AV?$THandler@$0II@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0e58] `.?AV?$THandler@$0GL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x009a0ea8] `.?AV?$THandler@$0GM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0ef8] `.?AV?$THandler@$0GN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0f48] `.?AV?$THandler@$0ID@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0f98] `.?AV?$THandler@$0BAAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0GN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x009a0ef8`)
  context:
     [0x009a0e08] `.?AV?$THandler@$0II@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0e58] `.?AV?$THandler@$0GL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0ea8] `.?AV?$THandler@$0GM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x009a0ef8] `.?AV?$THandler@$0GN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0f48] `.?AV?$THandler@$0ID@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0f98] `.?AV?$THandler@$0BAAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a0ff8] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0ID@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@` (pattern `CSerfBehavior`, offset `0x009a0f48`)
  context:
     [0x009a0e58] `.?AV?$THandler@$0GL@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0ea8] `.?AV?$THandler@$0GM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0ef8] `.?AV?$THandler@$0GN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x009a0f48] `.?AV?$THandler@$0ID@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0f98] `.?AV?$THandler@$0BAAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a0ff8] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1058] `.?AV?$THandler@$0BEAAD@VCEvent@BB@@VCEventEntityIndex@GGL@@VCSerfBehavior@4@X@EGL@@`
- hit: `.?AV?$THandler@$0BAAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x009a0f98`)
  context:
     [0x009a0ea8] `.?AV?$THandler@$0GM@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0ef8] `.?AV?$THandler@$0GN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0f48] `.?AV?$THandler@$0ID@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
  >> [0x009a0f98] `.?AV?$THandler@$0BAAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a0ff8] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1058] `.?AV?$THandler@$0BEAAD@VCEvent@BB@@VCEventEntityIndex@GGL@@VCSerfBehavior@4@X@EGL@@`
     [0x009a10b8] `.?AV?$THandler@$0BIAAC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x009a0ff8`)
  context:
     [0x009a0ef8] `.?AV?$THandler@$0GN@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0f48] `.?AV?$THandler@$0ID@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0f98] `.?AV?$THandler@$0BAAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x009a0ff8] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1058] `.?AV?$THandler@$0BEAAD@VCEvent@BB@@VCEventEntityIndex@GGL@@VCSerfBehavior@4@X@EGL@@`
     [0x009a10b8] `.?AV?$THandler@$0BIAAC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1128] `.?AV?$THandler@$0BAAAJ@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BEAAD@VCEvent@BB@@VCEventEntityIndex@GGL@@VCSerfBehavior@4@X@EGL@@` (pattern `CSerfBehavior`, offset `0x009a1058`)
  context:
     [0x009a0f48] `.?AV?$THandler@$0ID@VCGLETaskArgs@EGL@@V12@VCSerfBehavior@GGL@@H@EGL@@`
     [0x009a0f98] `.?AV?$THandler@$0BAAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a0ff8] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x009a1058] `.?AV?$THandler@$0BEAAD@VCEvent@BB@@VCEventEntityIndex@GGL@@VCSerfBehavior@4@X@EGL@@`
     [0x009a10b8] `.?AV?$THandler@$0BIAAC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1128] `.?AV?$THandler@$0BAAAJ@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1188] `.?AV?$THandler@$0BAAAK@VCEvent@BB@@VCEventEntityGetBool@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BIAAC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x009a10b8`)
  context:
     [0x009a0f98] `.?AV?$THandler@$0BAAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a0ff8] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1058] `.?AV?$THandler@$0BEAAD@VCEvent@BB@@VCEventEntityIndex@GGL@@VCSerfBehavior@4@X@EGL@@`
  >> [0x009a10b8] `.?AV?$THandler@$0BIAAC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1128] `.?AV?$THandler@$0BAAAJ@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1188] `.?AV?$THandler@$0BAAAK@VCEvent@BB@@VCEventEntityGetBool@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a11f0] `.?AV?$THandler@$0BEAAF@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BAAAJ@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x009a1128`)
  context:
     [0x009a0ff8] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1058] `.?AV?$THandler@$0BEAAD@VCEvent@BB@@VCEventEntityIndex@GGL@@VCSerfBehavior@4@X@EGL@@`
     [0x009a10b8] `.?AV?$THandler@$0BIAAC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x009a1128] `.?AV?$THandler@$0BAAAJ@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1188] `.?AV?$THandler@$0BAAAK@VCEvent@BB@@VCEventEntityGetBool@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a11f0] `.?AV?$THandler@$0BEAAF@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1240] `.?AV?$THandler@$0BEAAG@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BAAAK@VCEvent@BB@@VCEventEntityGetBool@EGL@@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x009a1188`)
  context:
     [0x009a1058] `.?AV?$THandler@$0BEAAD@VCEvent@BB@@VCEventEntityIndex@GGL@@VCSerfBehavior@4@X@EGL@@`
     [0x009a10b8] `.?AV?$THandler@$0BIAAC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1128] `.?AV?$THandler@$0BAAAJ@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x009a1188] `.?AV?$THandler@$0BAAAK@VCEvent@BB@@VCEventEntityGetBool@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a11f0] `.?AV?$THandler@$0BEAAF@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1240] `.?AV?$THandler@$0BEAAG@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1290] `.?AV?$THandler@$0BEAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BEAAF@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x009a11f0`)
  context:
     [0x009a10b8] `.?AV?$THandler@$0BIAAC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1128] `.?AV?$THandler@$0BAAAJ@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1188] `.?AV?$THandler@$0BAAAK@VCEvent@BB@@VCEventEntityGetBool@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x009a11f0] `.?AV?$THandler@$0BEAAF@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1240] `.?AV?$THandler@$0BEAAG@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1290] `.?AV?$THandler@$0BEAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1300] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BEAAG@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x009a1240`)
  context:
     [0x009a1128] `.?AV?$THandler@$0BAAAJ@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1188] `.?AV?$THandler@$0BAAAK@VCEvent@BB@@VCEventEntityGetBool@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a11f0] `.?AV?$THandler@$0BEAAF@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x009a1240] `.?AV?$THandler@$0BEAAG@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1290] `.?AV?$THandler@$0BEAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1300] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1370] `.?AV?$THandler@$0BFAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BEAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x009a1290`)
  context:
     [0x009a1188] `.?AV?$THandler@$0BAAAK@VCEvent@BB@@VCEventEntityGetBool@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a11f0] `.?AV?$THandler@$0BEAAF@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1240] `.?AV?$THandler@$0BEAAG@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x009a1290] `.?AV?$THandler@$0BEAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1300] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1370] `.?AV?$THandler@$0BFAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a13cc] `.?AV?$TStateHandler@VCSerfBehavior@GGL@@@EGL@@`
- hit: `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x009a1300`)
  context:
     [0x009a11f0] `.?AV?$THandler@$0BEAAF@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1240] `.?AV?$THandler@$0BEAAG@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1290] `.?AV?$THandler@$0BEAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x009a1300] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1370] `.?AV?$THandler@$0BFAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a13cc] `.?AV?$TStateHandler@VCSerfBehavior@GGL@@@EGL@@`
     [0x009a1404] `.?AVCGLSettlerCreator@GGL@@`
- hit: `.?AV?$THandler@$0BFAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@` (pattern `CSerfBehavior`, offset `0x009a1370`)
  context:
     [0x009a1240] `.?AV?$THandler@$0BEAAG@VCEvent@BB@@V12@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1290] `.?AV?$THandler@$0BEAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1300] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x009a1370] `.?AV?$THandler@$0BFAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a13cc] `.?AV?$TStateHandler@VCSerfBehavior@GGL@@@EGL@@`
     [0x009a1404] `.?AVCGLSettlerCreator@GGL@@`
     [0x009a1428] `.?AV?$THandler@$0BF@VCGLETaskArgs@EGL@@V12@VCSettler@GGL@@H@EGL@@`
- hit: `.?AV?$TStateHandler@VCSerfBehavior@GGL@@@EGL@@` (pattern `CSerfBehavior`, offset `0x009a13cc`)
  context:
     [0x009a1290] `.?AV?$THandler@$0BEAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1300] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
     [0x009a1370] `.?AV?$THandler@$0BFAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCSerfBehavior@GGL@@X@EGL@@`
  >> [0x009a13cc] `.?AV?$TStateHandler@VCSerfBehavior@GGL@@@EGL@@`
     [0x009a1404] `.?AVCGLSettlerCreator@GGL@@`
     [0x009a1428] `.?AV?$THandler@$0BF@VCGLETaskArgs@EGL@@V12@VCSettler@GGL@@H@EGL@@`
     [0x009a1478] `.?AV?$THandler@$0BG@VCGLETaskArgs@EGL@@V12@VCSettler@GGL@@H@EGL@@`
- hit: `.?AVCWorkerAlarmModeBehaviorProps@GGL@@` (pattern `CWorkerAlarmModeBehaviorProps`, offset `0x009a38b8`)
  context:
     [0x009a3844] `.?AVIWeatherSystem@GGL@@`
     [0x009a3868] `.?AVCWeatherHandler@GGL@@`
     [0x009a388c] `.?AVCEventWeatherStateChanged@GGL@@`
  >> [0x009a38b8] `.?AVCWorkerAlarmModeBehaviorProps@GGL@@`
     [0x009a38e8] `.?AVCWorkerAlarmModeBehavior@GGL@@`
     [0x009a3918] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3970] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
- hit: `.?AVCWorkerAlarmModeBehavior@GGL@@` (pattern `CWorkerAlarmModeBehavior`, offset `0x009a38e8`)
  context:
     [0x009a3868] `.?AVCWeatherHandler@GGL@@`
     [0x009a388c] `.?AVCEventWeatherStateChanged@GGL@@`
     [0x009a38b8] `.?AVCWorkerAlarmModeBehaviorProps@GGL@@`
  >> [0x009a38e8] `.?AVCWorkerAlarmModeBehavior@GGL@@`
     [0x009a3918] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3970] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a39c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `CWorkerAlarmModeBehavior`, offset `0x009a3918`)
  context:
     [0x009a388c] `.?AVCEventWeatherStateChanged@GGL@@`
     [0x009a38b8] `.?AVCWorkerAlarmModeBehaviorProps@GGL@@`
     [0x009a38e8] `.?AVCWorkerAlarmModeBehavior@GGL@@`
  >> [0x009a3918] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3970] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a39c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3a30] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `CWorkerAlarmModeBehavior`, offset `0x009a3970`)
  context:
     [0x009a38b8] `.?AVCWorkerAlarmModeBehaviorProps@GGL@@`
     [0x009a38e8] `.?AVCWorkerAlarmModeBehavior@GGL@@`
     [0x009a3918] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
  >> [0x009a3970] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a39c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3a30] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3a90] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `CWorkerAlarmModeBehavior`, offset `0x009a39c8`)
  context:
     [0x009a38e8] `.?AVCWorkerAlarmModeBehavior@GGL@@`
     [0x009a3918] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3970] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
  >> [0x009a39c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3a30] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3a90] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3af0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `CWorkerAlarmModeBehavior`, offset `0x009a3a30`)
  context:
     [0x009a3918] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3970] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a39c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
  >> [0x009a3a30] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3a90] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3af0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3b50] `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `CWorkerAlarmModeBehavior`, offset `0x009a3a90`)
  context:
     [0x009a3970] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a39c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3a30] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
  >> [0x009a3a90] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3af0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3b50] `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3bac] `.?AVCWorkerBattleBehaviorProps@GGL@@`
- hit: `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `CWorkerAlarmModeBehavior`, offset `0x009a3af0`)
  context:
     [0x009a39c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3a30] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3a90] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
  >> [0x009a3af0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3b50] `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3bac] `.?AVCWorkerBattleBehaviorProps@GGL@@`
     [0x009a3bdc] `.?AVCWorkerBattleBehavior@GGL@@`
- hit: `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `CWorkerAlarmModeBehavior`, offset `0x009a3b50`)
  context:
     [0x009a3a30] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3a90] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3af0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
  >> [0x009a3b50] `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3bac] `.?AVCWorkerBattleBehaviorProps@GGL@@`
     [0x009a3bdc] `.?AVCWorkerBattleBehavior@GGL@@`
     [0x009a3c08] `.?AV?$THandler@$0HA@VCGLETaskArgs@EGL@@V12@VCWorkerBattleBehavior@GGL@@H@EGL@@`
- hit: `.?AVCWorkerBehaviorProps@GGL@@` (pattern `CWorkerBehaviorProps`, offset `0x009a406c`)
  context:
     [0x009a3f38] `.?AV?$THandler@$0CAAAF@VCEvent@BB@@V12@VCWorkerBattleBehavior@GGL@@X@EGL@@`
     [0x009a3f90] `.?AV?$THandler@$0BBAAD@VCEvent@BB@@VCEventPosition@EGL@@VCWorkerBattleBehavior@GGL@@X@EGL@@`
     [0x009a3ff8] `.?AV?$THandler@$0BIAAJ@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBattleBehavior@GGL@@X@EGL@@`
  >> [0x009a406c] `.?AVCWorkerBehaviorProps@GGL@@`
     [0x009a4094] `.?AVCWorkerBehavior@GGL@@`
     [0x009a40b8] `.?AV?$CEventGetValue@PAVCNeutralBridgeBehavior@GGL@@$0EEJAALPH@@EGL@@`
     [0x009a4108] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AVCWorkerBehavior@GGL@@` (pattern `CWorkerBehavior`, offset `0x009a4094`)
  context:
     [0x009a3f90] `.?AV?$THandler@$0BBAAD@VCEvent@BB@@VCEventPosition@EGL@@VCWorkerBattleBehavior@GGL@@X@EGL@@`
     [0x009a3ff8] `.?AV?$THandler@$0BIAAJ@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBattleBehavior@GGL@@X@EGL@@`
     [0x009a406c] `.?AVCWorkerBehaviorProps@GGL@@`
  >> [0x009a4094] `.?AVCWorkerBehavior@GGL@@`
     [0x009a40b8] `.?AV?$CEventGetValue@PAVCNeutralBridgeBehavior@GGL@@$0EEJAALPH@@EGL@@`
     [0x009a4108] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4160] `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4108`)
  context:
     [0x009a406c] `.?AVCWorkerBehaviorProps@GGL@@`
     [0x009a4094] `.?AVCWorkerBehavior@GGL@@`
     [0x009a40b8] `.?AV?$CEventGetValue@PAVCNeutralBridgeBehavior@GGL@@$0EEJAALPH@@EGL@@`
  >> [0x009a4108] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4160] `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a41c8] `.?AV?$THandler@$0DO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4220] `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4160`)
  context:
     [0x009a4094] `.?AVCWorkerBehavior@GGL@@`
     [0x009a40b8] `.?AV?$CEventGetValue@PAVCNeutralBridgeBehavior@GGL@@$0EEJAALPH@@EGL@@`
     [0x009a4108] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4160] `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a41c8] `.?AV?$THandler@$0DO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4220] `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4288] `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0DO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a41c8`)
  context:
     [0x009a40b8] `.?AV?$CEventGetValue@PAVCNeutralBridgeBehavior@GGL@@$0EEJAALPH@@EGL@@`
     [0x009a4108] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4160] `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a41c8] `.?AV?$THandler@$0DO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4220] `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4288] `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a42f0] `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4220`)
  context:
     [0x009a4108] `.?AV?$THandler@$0DN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4160] `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a41c8] `.?AV?$THandler@$0DO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4220] `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4288] `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a42f0] `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4358] `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4288`)
  context:
     [0x009a4160] `.?AV?$THandler@$01VCGLETaskArgs@EGL@@VCGLETaskArgsPosition@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a41c8] `.?AV?$THandler@$0DO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4220] `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4288] `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a42f0] `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4358] `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a43c0] `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a42f0`)
  context:
     [0x009a41c8] `.?AV?$THandler@$0DO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4220] `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4288] `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a42f0] `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4358] `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a43c0] `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4428] `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4358`)
  context:
     [0x009a4220] `.?AV?$THandler@$0DP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4288] `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a42f0] `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4358] `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a43c0] `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4428] `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4490] `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a43c0`)
  context:
     [0x009a4288] `.?AV?$THandler@$0EA@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a42f0] `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4358] `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a43c0] `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4428] `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4490] `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a44f8] `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4428`)
  context:
     [0x009a42f0] `.?AV?$THandler@$0EB@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4358] `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a43c0] `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4428] `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4490] `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a44f8] `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4560] `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4490`)
  context:
     [0x009a4358] `.?AV?$THandler@$0EC@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a43c0] `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4428] `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4490] `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a44f8] `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4560] `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a45c8] `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a44f8`)
  context:
     [0x009a43c0] `.?AV?$THandler@$0ED@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4428] `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4490] `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a44f8] `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4560] `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a45c8] `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4630] `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4560`)
  context:
     [0x009a4428] `.?AV?$THandler@$0EE@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4490] `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a44f8] `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4560] `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a45c8] `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4630] `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4698] `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a45c8`)
  context:
     [0x009a4490] `.?AV?$THandler@$0EF@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a44f8] `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4560] `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a45c8] `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4630] `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4698] `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4700] `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4630`)
  context:
     [0x009a44f8] `.?AV?$THandler@$0EG@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4560] `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a45c8] `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4630] `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4698] `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4700] `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4768] `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4698`)
  context:
     [0x009a4560] `.?AV?$THandler@$0EH@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a45c8] `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4630] `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4698] `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4700] `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4768] `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a47d0] `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4700`)
  context:
     [0x009a45c8] `.?AV?$THandler@$0EI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4630] `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4698] `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4700] `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4768] `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a47d0] `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4838] `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4768`)
  context:
     [0x009a4630] `.?AV?$THandler@$0EJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4698] `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4700] `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4768] `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a47d0] `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4838] `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a48a0] `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a47d0`)
  context:
     [0x009a4698] `.?AV?$THandler@$0EK@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4700] `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4768] `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a47d0] `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4838] `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a48a0] `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4908] `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4838`)
  context:
     [0x009a4700] `.?AV?$THandler@$0EL@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4768] `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a47d0] `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4838] `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a48a0] `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4908] `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4970] `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a48a0`)
  context:
     [0x009a4768] `.?AV?$THandler@$0EM@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a47d0] `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4838] `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a48a0] `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4908] `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4970] `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a49d0] `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4908`)
  context:
     [0x009a47d0] `.?AV?$THandler@$0EN@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4838] `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a48a0] `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4908] `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4970] `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a49d0] `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4a28] `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4970`)
  context:
     [0x009a4838] `.?AV?$THandler@$0EO@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a48a0] `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4908] `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4970] `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a49d0] `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4a28] `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4a80] `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a49d0`)
  context:
     [0x009a48a0] `.?AV?$THandler@$0EP@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4908] `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4970] `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a49d0] `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4a28] `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4a80] `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ad8] `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4a28`)
  context:
     [0x009a4908] `.?AV?$THandler@$0HI@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4970] `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a49d0] `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4a28] `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4a80] `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ad8] `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4b30] `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4a80`)
  context:
     [0x009a4970] `.?AV?$THandler@$0HJ@VCGLETaskArgs@EGL@@VCTaskArgsFloat@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a49d0] `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4a28] `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4a80] `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ad8] `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4b30] `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4b88] `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4ad8`)
  context:
     [0x009a49d0] `.?AV?$THandler@$0JA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4a28] `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4a80] `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4ad8] `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4b30] `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4b88] `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4be0] `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4b30`)
  context:
     [0x009a4a28] `.?AV?$THandler@$0JB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4a80] `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ad8] `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4b30] `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4b88] `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4be0] `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4c38] `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4b88`)
  context:
     [0x009a4a80] `.?AV?$THandler@$0JC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ad8] `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4b30] `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4b88] `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4be0] `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4c38] `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4c90] `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4be0`)
  context:
     [0x009a4ad8] `.?AV?$THandler@$0JD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4b30] `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4b88] `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4be0] `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4c38] `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4c90] `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ce8] `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4c38`)
  context:
     [0x009a4b30] `.?AV?$THandler@$0FC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4b88] `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4be0] `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4c38] `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4c90] `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ce8] `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4d40] `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4c90`)
  context:
     [0x009a4b88] `.?AV?$THandler@$0FD@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4be0] `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4c38] `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4c90] `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ce8] `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4d40] `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4d98] `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4ce8`)
  context:
     [0x009a4be0] `.?AV?$THandler@$0FE@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4c38] `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4c90] `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4ce8] `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4d40] `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4d98] `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4df0] `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4d40`)
  context:
     [0x009a4c38] `.?AV?$THandler@$0FF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4c90] `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ce8] `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4d40] `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4d98] `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4df0] `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4e48] `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4d98`)
  context:
     [0x009a4c90] `.?AV?$THandler@$0JM@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ce8] `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4d40] `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4d98] `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4df0] `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4e48] `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ea0] `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4df0`)
  context:
     [0x009a4ce8] `.?AV?$THandler@$0JL@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4d40] `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4d98] `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4df0] `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4e48] `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ea0] `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ef8] `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4e48`)
  context:
     [0x009a4d40] `.?AV?$THandler@$0JK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4d98] `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4df0] `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4e48] `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ea0] `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ef8] `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4f60] `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4ea0`)
  context:
     [0x009a4d98] `.?AV?$THandler@$0JN@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4df0] `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4e48] `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4ea0] `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ef8] `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4f60] `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4fc8] `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4ef8`)
  context:
     [0x009a4df0] `.?AV?$THandler@$0FI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4e48] `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ea0] `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4ef8] `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4f60] `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4fc8] `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5030] `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4f60`)
  context:
     [0x009a4e48] `.?AV?$THandler@$0FJ@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ea0] `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ef8] `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4f60] `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4fc8] `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5030] `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5098] `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a4fc8`)
  context:
     [0x009a4ea0] `.?AV?$THandler@$0FK@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4ef8] `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4f60] `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a4fc8] `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5030] `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5098] `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a50f0] `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5030`)
  context:
     [0x009a4ef8] `.?AV?$THandler@$0HM@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4f60] `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4fc8] `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a5030] `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5098] `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a50f0] `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5148] `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5098`)
  context:
     [0x009a4f60] `.?AV?$THandler@$0HO@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a4fc8] `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5030] `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a5098] `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a50f0] `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5148] `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a51a0] `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a50f0`)
  context:
     [0x009a4fc8] `.?AV?$THandler@$0IA@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5030] `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5098] `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a50f0] `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5148] `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a51a0] `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a51f8] `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5148`)
  context:
     [0x009a5030] `.?AV?$THandler@$0HN@VCGLETaskArgs@EGL@@VCGLETaskArgsSubAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5098] `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a50f0] `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a5148] `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a51a0] `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a51f8] `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5250] `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a51a0`)
  context:
     [0x009a5098] `.?AV?$THandler@$0FB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a50f0] `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5148] `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a51a0] `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a51f8] `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5250] `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a52a8] `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a51f8`)
  context:
     [0x009a50f0] `.?AV?$THandler@$0GP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5148] `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a51a0] `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a51f8] `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5250] `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a52a8] `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5300] `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5250`)
  context:
     [0x009a5148] `.?AV?$THandler@$0HB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a51a0] `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a51f8] `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a5250] `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a52a8] `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5300] `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5368] `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a52a8`)
  context:
     [0x009a51a0] `.?AV?$THandler@$0HC@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a51f8] `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5250] `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a52a8] `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5300] `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5368] `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a53c0] `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5300`)
  context:
     [0x009a51f8] `.?AV?$THandler@$0IO@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5250] `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a52a8] `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a5300] `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5368] `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a53c0] `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5418] `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5368`)
  context:
     [0x009a5250] `.?AV?$THandler@$0IP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a52a8] `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5300] `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a5368] `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a53c0] `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5418] `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5470] `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a53c0`)
  context:
     [0x009a52a8] `.?AV?$THandler@$0JI@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5300] `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5368] `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a53c0] `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5418] `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5470] `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a54c8] `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5418`)
  context:
     [0x009a5300] `.?AV?$THandler@$0JJ@VCGLETaskArgs@EGL@@VCTaskArgsInteger@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5368] `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a53c0] `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a5418] `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5470] `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a54c8] `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5520] `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5470`)
  context:
     [0x009a5368] `.?AV?$THandler@$0JH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a53c0] `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5418] `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a5470] `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a54c8] `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5520] `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5580] `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a54c8`)
  context:
     [0x009a53c0] `.?AV?$THandler@$0JG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5418] `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5470] `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a54c8] `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5520] `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5580] `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a55e8] `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5520`)
  context:
     [0x009a5418] `.?AV?$THandler@$0JP@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5470] `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a54c8] `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a5520] `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5580] `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a55e8] `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5658] `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5580`)
  context:
     [0x009a5470] `.?AV?$THandler@$0KA@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a54c8] `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5520] `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a5580] `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a55e8] `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5658] `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a56c8] `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a55e8`)
  context:
     [0x009a54c8] `.?AV?$THandler@$0KB@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5520] `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5580] `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a55e8] `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5658] `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a56c8] `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5720] `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5658`)
  context:
     [0x009a5520] `.?AV?$THandler@$0BD@VCGLETaskArgs@EGL@@VCTaskArgsUVAnim@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5580] `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a55e8] `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a5658] `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a56c8] `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5720] `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5778] `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a56c8`)
  context:
     [0x009a5580] `.?AV?$THandler@$0LB@VCGLETaskArgs@EGL@@VCGLETaskArgsTaskListID@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a55e8] `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5658] `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a56c8] `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5720] `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5778] `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a57d0] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5720`)
  context:
     [0x009a55e8] `.?AV?$THandler@$0BA@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5658] `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a56c8] `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a5720] `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5778] `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a57d0] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5830] `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5778`)
  context:
     [0x009a5658] `.?AV?$THandler@$0BB@VCGLETaskArgs@EGL@@VCTaskArgsParticleEffectIndex@2@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a56c8] `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5720] `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a5778] `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a57d0] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5830] `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5890] `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a57d0`)
  context:
     [0x009a56c8] `.?AV?$THandler@$0LF@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5720] `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5778] `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
  >> [0x009a57d0] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5830] `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5890] `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a58f0] `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5830`)
  context:
     [0x009a5720] `.?AV?$THandler@$0LG@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a5778] `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a57d0] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5830] `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5890] `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a58f0] `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5960] `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5890`)
  context:
     [0x009a5778] `.?AV?$THandler@$0LH@VCGLETaskArgs@EGL@@V12@VCWorkerBehavior@GGL@@H@EGL@@`
     [0x009a57d0] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5830] `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5890] `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a58f0] `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5960] `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@`
     [0x009a59c8] `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a58f0`)
  context:
     [0x009a57d0] `.?AV?$THandler@$0BDAAC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5830] `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5890] `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a58f0] `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5960] `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@`
     [0x009a59c8] `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5a38] `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5960`)
  context:
     [0x009a5830] `.?AV?$THandler@$0BDAAD@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5890] `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a58f0] `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5960] `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@`
     [0x009a59c8] `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5a38] `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5aa8] `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a59c8`)
  context:
     [0x009a5890] `.?AV?$THandler@$0BDAAE@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a58f0] `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5960] `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@`
  >> [0x009a59c8] `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5a38] `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5aa8] `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5b18] `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5a38`)
  context:
     [0x009a58f0] `.?AV?$THandler@$0BDAAH@VCEvent@BB@@V?$CEventGetValue@M$0FHIOOIPH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5960] `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@`
     [0x009a59c8] `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5a38] `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5aa8] `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5b18] `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5b68] `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5aa8`)
  context:
     [0x009a5960] `.?AV?$THandler@$0BDABJ@VCEvent@BB@@VCEventChangeMotivation@GGL@@VCWorkerBehavior@4@X@EGL@@`
     [0x009a59c8] `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5a38] `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5aa8] `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5b18] `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5b68] `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5bb8] `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5b18`)
  context:
     [0x009a59c8] `.?AV?$THandler@$0BIAAD@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5a38] `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5aa8] `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5b18] `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5b68] `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5bb8] `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5c08] `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5b68`)
  context:
     [0x009a5a38] `.?AV?$THandler@$0BDAAI@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5aa8] `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5b18] `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5b68] `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5bb8] `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5c08] `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5c58] `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5bb8`)
  context:
     [0x009a5aa8] `.?AV?$THandler@$0BDAAJ@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5b18] `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5b68] `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5bb8] `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5c08] `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5c58] `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5cc8] `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5c08`)
  context:
     [0x009a5b18] `.?AV?$THandler@$0BDAAK@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5b68] `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5bb8] `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5c08] `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5c58] `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5cc8] `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5d38] `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5c58`)
  context:
     [0x009a5b68] `.?AV?$THandler@$0BDAAL@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5bb8] `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5c08] `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5c58] `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5cc8] `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5d38] `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5d88] `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5cc8`)
  context:
     [0x009a5bb8] `.?AV?$THandler@$0BDAAM@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5c08] `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5c58] `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5cc8] `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5d38] `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5d88] `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5dd8] `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5d38`)
  context:
     [0x009a5c08] `.?AV?$THandler@$0BDABF@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5c58] `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5cc8] `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5d38] `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5d88] `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5dd8] `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5e48] `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5d88`)
  context:
     [0x009a5c58] `.?AV?$THandler@$0BDABE@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5cc8] `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5d38] `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5d88] `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5dd8] `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5e48] `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5eb8] `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5dd8`)
  context:
     [0x009a5cc8] `.?AV?$THandler@$0BDABD@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5d38] `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5d88] `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5dd8] `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5e48] `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5eb8] `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5f28] `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5e48`)
  context:
     [0x009a5d38] `.?AV?$THandler@$0BDABG@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5d88] `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5dd8] `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5e48] `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5eb8] `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5f28] `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5f98] `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5eb8`)
  context:
     [0x009a5d88] `.?AV?$THandler@$0BDABH@VCEvent@BB@@V12@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5dd8] `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5e48] `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5eb8] `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5f28] `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5f98] `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5ff8] `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5f28`)
  context:
     [0x009a5dd8] `.?AV?$THandler@$0BDABL@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5e48] `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5eb8] `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5f28] `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5f98] `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5ff8] `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6058] `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5f98`)
  context:
     [0x009a5e48] `.?AV?$THandler@$0BDACJ@VCEvent@BB@@V?$CEventValue@H$0?BKELPGJ@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5eb8] `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5f28] `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5f98] `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5ff8] `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6058] `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a60c8] `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a5ff8`)
  context:
     [0x009a5eb8] `.?AV?$THandler@$0BDABK@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5f28] `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5f98] `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a5ff8] `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6058] `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a60c8] `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6138] `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a6058`)
  context:
     [0x009a5f28] `.?AV?$THandler@$0BDABO@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5f98] `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5ff8] `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a6058] `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a60c8] `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6138] `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6198] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a60c8`)
  context:
     [0x009a5f98] `.?AV?$THandler@$0BHABC@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a5ff8] `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6058] `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a60c8] `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6138] `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6198] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6208] `.?AV?$THandler@$0BDACC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a6138`)
  context:
     [0x009a5ff8] `.?AV?$THandler@$0BDABN@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6058] `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a60c8] `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a6138] `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6198] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6208] `.?AV?$THandler@$0BDACC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6278] `.?AV?$THandler@$0BDACF@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a6198`)
  context:
     [0x009a6058] `.?AV?$THandler@$0BDACA@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a60c8] `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6138] `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a6198] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6208] `.?AV?$THandler@$0BDACC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6278] `.?AV?$THandler@$0BDACF@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a62d8] `.?AV?$TStateHandler@VCWorkerBehavior@GGL@@@EGL@@`
- hit: `.?AV?$THandler@$0BDACC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a6208`)
  context:
     [0x009a60c8] `.?AV?$THandler@$0BDACB@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6138] `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6198] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a6208] `.?AV?$THandler@$0BDACC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6278] `.?AV?$THandler@$0BDACF@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a62d8] `.?AV?$TStateHandler@VCWorkerBehavior@GGL@@@EGL@@`
     [0x009a6314] `.?AVCWorkerEvadeBehavior@GGL@@`
- hit: `.?AV?$THandler@$0BDACF@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a6278`)
  context:
     [0x009a6138] `.?AV?$THandler@$0BDABI@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6198] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6208] `.?AV?$THandler@$0BDACC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a6278] `.?AV?$THandler@$0BDACF@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a62d8] `.?AV?$TStateHandler@VCWorkerBehavior@GGL@@@EGL@@`
     [0x009a6314] `.?AVCWorkerEvadeBehavior@GGL@@`
     [0x009a633c] `.?AVCWorkerFleeBehaviorProps@GGL@@`
- hit: `.?AV?$TStateHandler@VCWorkerBehavior@GGL@@@EGL@@` (pattern `CWorkerBehavior`, offset `0x009a62d8`)
  context:
     [0x009a6198] `.?AV?$THandler@$0CAACE@VCEvent@BB@@V?$CEventGetValue@H$0EIDAEAOH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6208] `.?AV?$THandler@$0BDACC@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a6278] `.?AV?$THandler@$0BDACF@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
  >> [0x009a62d8] `.?AV?$TStateHandler@VCWorkerBehavior@GGL@@@EGL@@`
     [0x009a6314] `.?AVCWorkerEvadeBehavior@GGL@@`
     [0x009a633c] `.?AVCWorkerFleeBehaviorProps@GGL@@`
     [0x009a6368] `.?AVCWorkerFleeBehavior@GGL@@`
- hit: `.?AVCWorkerFleeBehaviorProps@GGL@@` (pattern `CWorkerFleeBehaviorProps`, offset `0x009a633c`)
  context:
     [0x009a6278] `.?AV?$THandler@$0BDACF@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerBehavior@GGL@@X@EGL@@`
     [0x009a62d8] `.?AV?$TStateHandler@VCWorkerBehavior@GGL@@@EGL@@`
     [0x009a6314] `.?AVCWorkerEvadeBehavior@GGL@@`
  >> [0x009a633c] `.?AVCWorkerFleeBehaviorProps@GGL@@`
     [0x009a6368] `.?AVCWorkerFleeBehavior@GGL@@`
     [0x009a6390] `.?AV?$THandler@$0BFAAO@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
     [0x009a63f8] `.?AV?$THandler@$0BDABP@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
- hit: `.?AVCWorkerFleeBehavior@GGL@@` (pattern `CWorkerFleeBehavior`, offset `0x009a6368`)
  context:
     [0x009a62d8] `.?AV?$TStateHandler@VCWorkerBehavior@GGL@@@EGL@@`
     [0x009a6314] `.?AVCWorkerEvadeBehavior@GGL@@`
     [0x009a633c] `.?AVCWorkerFleeBehaviorProps@GGL@@`
  >> [0x009a6368] `.?AVCWorkerFleeBehavior@GGL@@`
     [0x009a6390] `.?AV?$THandler@$0BFAAO@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
     [0x009a63f8] `.?AV?$THandler@$0BDABP@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
     [0x009a6470] `.?AV?$THandler@$0IN@VCGLETaskArgs@EGL@@V12@VCWorkerFleeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BFAAO@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@` (pattern `CWorkerFleeBehavior`, offset `0x009a6390`)
  context:
     [0x009a6314] `.?AVCWorkerEvadeBehavior@GGL@@`
     [0x009a633c] `.?AVCWorkerFleeBehaviorProps@GGL@@`
     [0x009a6368] `.?AVCWorkerFleeBehavior@GGL@@`
  >> [0x009a6390] `.?AV?$THandler@$0BFAAO@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
     [0x009a63f8] `.?AV?$THandler@$0BDABP@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
     [0x009a6470] `.?AV?$THandler@$0IN@VCGLETaskArgs@EGL@@V12@VCWorkerFleeBehavior@GGL@@H@EGL@@`
     [0x009a64c8] `.?AVCGLEAnimProps@EGL@@`
- hit: `.?AV?$THandler@$0BDABP@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@` (pattern `CWorkerFleeBehavior`, offset `0x009a63f8`)
  context:
     [0x009a633c] `.?AVCWorkerFleeBehaviorProps@GGL@@`
     [0x009a6368] `.?AVCWorkerFleeBehavior@GGL@@`
     [0x009a6390] `.?AV?$THandler@$0BFAAO@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
  >> [0x009a63f8] `.?AV?$THandler@$0BDABP@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
     [0x009a6470] `.?AV?$THandler@$0IN@VCGLETaskArgs@EGL@@V12@VCWorkerFleeBehavior@GGL@@H@EGL@@`
     [0x009a64c8] `.?AVCGLEAnimProps@EGL@@`
     [0x009a64e8] `.?AVIAnimsPropsMgr@GGlue@@`
- hit: `.?AV?$THandler@$0IN@VCGLETaskArgs@EGL@@V12@VCWorkerFleeBehavior@GGL@@H@EGL@@` (pattern `CWorkerFleeBehavior`, offset `0x009a6470`)
  context:
     [0x009a6368] `.?AVCWorkerFleeBehavior@GGL@@`
     [0x009a6390] `.?AV?$THandler@$0BFAAO@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
     [0x009a63f8] `.?AV?$THandler@$0BDABP@VCEvent@BB@@V?$CEventGetValue@_N$0GFNOIDBH@@EGL@@VCWorkerFleeBehavior@GGL@@X@EGL@@`
  >> [0x009a6470] `.?AV?$THandler@$0IN@VCGLETaskArgs@EGL@@V12@VCWorkerFleeBehavior@GGL@@H@EGL@@`
     [0x009a64c8] `.?AVCGLEAnimProps@EGL@@`
     [0x009a64e8] `.?AVIAnimsPropsMgr@GGlue@@`
     [0x009a650c] `.?AVCGlueAnimsPropsMgr@GGlue@@`

## task_ids_worker_camp

- patterns: 10 | hits: 10

- hit: `TASK_GO_TO_CAMP` (pattern `TASK_GO_TO_CAMP`, offset `0x007ddf04`)
  context:
     [0x007ddec0] `TASK_BECOME_COMATOSE`
     [0x007dded8] `TASK_WAIT_UNTIL`
     [0x007ddee8] `TASK_GO_TO_CANNON_POSITION`
  >> [0x007ddf04] `TASK_GO_TO_CAMP`
     [0x007ddf14] `TASK_BUILD_CANNON`
     [0x007ddf28] `TASK_LEAVE_CAMP`
     [0x007ddf38] `TASK_SUMMON_ENTITIES`
- hit: `TASK_LEAVE_CAMP` (pattern `TASK_LEAVE_CAMP`, offset `0x007ddf28`)
  context:
     [0x007ddee8] `TASK_GO_TO_CANNON_POSITION`
     [0x007ddf04] `TASK_GO_TO_CAMP`
     [0x007ddf14] `TASK_BUILD_CANNON`
  >> [0x007ddf28] `TASK_LEAVE_CAMP`
     [0x007ddf38] `TASK_SUMMON_ENTITIES`
     [0x007ddf50] `TASK_RESOLVE_COLLISION`
     [0x007ddf68] `TASK_GO_TO_NPC`
- hit: `TASK_GO_TO_EAT_BUILDING` (pattern `TASK_GO_TO_EAT_BUILDING`, offset `0x007de508`)
  context:
     [0x007de4a4] `TASK_GO_TO_SECURE_BUILDING`
     [0x007de4c0] `TASK_GO_TO_WORK_BUILDING`
     [0x007de4dc] `TASK_CHECK_GO_TO_SECURE_BUILDING_SUCCESS`
  >> [0x007de508] `TASK_GO_TO_EAT_BUILDING`
     [0x007de520] `TASK_STEAL_GOODS`
     [0x007de534] `TargetType`
     [0x007de540] `TASK_GO_TO_REST_BUILDING`
- hit: `TASK_GO_TO_REST_BUILDING` (pattern `TASK_GO_TO_REST_BUILDING`, offset `0x007de540`)
  context:
     [0x007de508] `TASK_GO_TO_EAT_BUILDING`
     [0x007de520] `TASK_STEAL_GOODS`
     [0x007de534] `TargetType`
  >> [0x007de540] `TASK_GO_TO_REST_BUILDING`
     [0x007de55c] `TASK_SECURE_STOLEN_GOODS`
     [0x007de578] `TASK_GO_TO_LEAVE_BUILDING`
     [0x007de594] `TASK_SET_THIEF_MODEL`
- hit: `TASK_CHANGE_WORK_TIME_CAMP` (pattern `TASK_CHANGE_WORK_TIME_CAMP`, offset `0x007de8a8`)
  context:
     [0x007de850] `TASK_CHANGE_WORK_TIME_WORK`
     [0x007de86c] `TASK_CHANGE_WORK_TIME_FARM`
     [0x007de888] `TASK_CHANGE_WORK_TIME_RESIDENCE`
  >> [0x007de8a8] `TASK_CHANGE_WORK_TIME_CAMP`
     [0x007de8c4] `TASK_GO_TO_SUPPLIER`
     [0x007de8d8] `TASK_DO_WORK_AT_FOUNDRY`
     [0x007de8f0] `TASK_CREATE_CANNON`
- hit: `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS` (pattern `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS`, offset `0x007de920`)
  context:
     [0x007de8d8] `TASK_DO_WORK_AT_FOUNDRY`
     [0x007de8f0] `TASK_CREATE_CANNON`
     [0x007de904] `TASK_SET_CANNON_PROGRESS`
  >> [0x007de920] `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS`
     [0x007de948] `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS`
     [0x007de970] `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS`
     [0x007de998] `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS`
- hit: `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS` (pattern `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS`, offset `0x007de948`)
  context:
     [0x007de8f0] `TASK_CREATE_CANNON`
     [0x007de904] `TASK_SET_CANNON_PROGRESS`
     [0x007de920] `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS`
  >> [0x007de948] `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS`
     [0x007de970] `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS`
     [0x007de998] `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS`
     [0x007de9c0] `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS`
- hit: `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS` (pattern `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS`, offset `0x007de970`)
  context:
     [0x007de904] `TASK_SET_CANNON_PROGRESS`
     [0x007de920] `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS`
     [0x007de948] `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS`
  >> [0x007de970] `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS`
     [0x007de998] `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS`
     [0x007de9c0] `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS`
     [0x007de9f0] `TASK_TAKE_FROM_STOCK`
- hit: `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS` (pattern `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS`, offset `0x007de998`)
  context:
     [0x007de920] `TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS`
     [0x007de948] `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS`
     [0x007de970] `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS`
  >> [0x007de998] `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS`
     [0x007de9c0] `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS`
     [0x007de9f0] `TASK_TAKE_FROM_STOCK`
     [0x007dea08] `TASK_SET_CARRIER_MODEL`
- hit: `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS` (pattern `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS`, offset `0x007de9c0`)
  context:
     [0x007de948] `TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS`
     [0x007de970] `TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS`
     [0x007de998] `TASK_CHECK_GO_TO_VILLAGE_CENTER_SUCCESS`
  >> [0x007de9c0] `TASK_CHECK_GO_TO_DEFENDABLE_BUILDING_SUCCESS`
     [0x007de9f0] `TASK_TAKE_FROM_STOCK`
     [0x007dea08] `TASK_SET_CARRIER_MODEL`
     [0x007dea20] `TASK_CHECK_GO_TO_SUPPLIER_SUCCESS`

## worker_alarm_and_flight

- patterns: 4 | hits: 14

- hit: `WorkerAlarmModeActive` (pattern `WorkerAlarmMode`, offset `0x007d6188`)
  context:
     [0x007d6150] `ConstructionProgress`
     [0x007d6168] `RepairProgress`
     [0x007d6178] `UpgradeProgress`
  >> [0x007d6188] `WorkerAlarmModeActive`
     [0x007d61a0] `MostRecentDepartureTurn`
     [0x007d61b8] `OvertimeRechargeTime`
     [0x007d61d0] `Slots`
- hit: `WorkerFlightDistance` (pattern `WorkerFlightDistance`, offset `0x007d9f28`)
  context:
     [0x007d9ed8] `DefenderProjectileDamage`
     [0x007d9ef4] `DefenderProjectileDamageClass`
     [0x007d9f14] `DefenderMissChance`
  >> [0x007d9f28] `WorkerFlightDistance`
     [0x007d9f40] `MaxExperiencePoints`
     [0x007d9f54] `BuildingRecentlyAttackedDuration`
     [0x007d9f78] `EnergyRequiredForWeatherChange`
- hit: `WorkerAlarmMode` (pattern `WorkerAlarmMode`, offset `0x007db79c`)
  context:
     [0x007db754] `CurrentMaxMotivation`
     [0x007db76c] `DurationOfWeatherChange`
     [0x007db784] `NumberOfBuyableHeros`
  >> [0x007db79c] `WorkerAlarmMode`
     [0x007db7ac] `PlayerGameState`
     [0x007db7bc] `PlayerHasLeftGameFlag`
     [0x007db7d4] `PlayerGameStateChangeGameTurn`
- hit: `EnterWorkerAlarmMode` (pattern `WorkerAlarmMode`, offset `0x007e2b94`)
  context:
     [0x007e2b54] `SettlerInflictFear`
     [0x007e2b68] `QuitSerfAlarmMode`
     [0x007e2b7c] `SettlerMotivateWorkers`
  >> [0x007e2b94] `EnterWorkerAlarmMode`
     [0x007e2bac] `ActivateAutoFillAtBarracks`
     [0x007e2bc8] `QuitWorkerAlarmMode`
     [0x007e2bdc] `DeactivateAutoFillAtBarracks`
- hit: `QuitWorkerAlarmMode` (pattern `WorkerAlarmMode`, offset `0x007e2bc8`)
  context:
     [0x007e2b7c] `SettlerMotivateWorkers`
     [0x007e2b94] `EnterWorkerAlarmMode`
     [0x007e2bac] `ActivateAutoFillAtBarracks`
  >> [0x007e2bc8] `QuitWorkerAlarmMode`
     [0x007e2bdc] `DeactivateAutoFillAtBarracks`
     [0x007e2bfc] `CancelState`
     [0x007e2c08] `State_SetExclusiveMessageRecipient`
- hit: `.?AVCWorkerAlarmModeBehaviorProps@GGL@@` (pattern `WorkerAlarmMode`, offset `0x009a38b8`)
  context:
     [0x009a3844] `.?AVIWeatherSystem@GGL@@`
     [0x009a3868] `.?AVCWeatherHandler@GGL@@`
     [0x009a388c] `.?AVCEventWeatherStateChanged@GGL@@`
  >> [0x009a38b8] `.?AVCWorkerAlarmModeBehaviorProps@GGL@@`
     [0x009a38e8] `.?AVCWorkerAlarmModeBehavior@GGL@@`
     [0x009a3918] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3970] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
- hit: `.?AVCWorkerAlarmModeBehavior@GGL@@` (pattern `WorkerAlarmMode`, offset `0x009a38e8`)
  context:
     [0x009a3868] `.?AVCWeatherHandler@GGL@@`
     [0x009a388c] `.?AVCEventWeatherStateChanged@GGL@@`
     [0x009a38b8] `.?AVCWorkerAlarmModeBehaviorProps@GGL@@`
  >> [0x009a38e8] `.?AVCWorkerAlarmModeBehavior@GGL@@`
     [0x009a3918] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3970] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a39c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
- hit: `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `WorkerAlarmMode`, offset `0x009a3918`)
  context:
     [0x009a388c] `.?AVCEventWeatherStateChanged@GGL@@`
     [0x009a38b8] `.?AVCWorkerAlarmModeBehaviorProps@GGL@@`
     [0x009a38e8] `.?AVCWorkerAlarmModeBehavior@GGL@@`
  >> [0x009a3918] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3970] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a39c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3a30] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `WorkerAlarmMode`, offset `0x009a3970`)
  context:
     [0x009a38b8] `.?AVCWorkerAlarmModeBehaviorProps@GGL@@`
     [0x009a38e8] `.?AVCWorkerAlarmModeBehavior@GGL@@`
     [0x009a3918] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
  >> [0x009a3970] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a39c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3a30] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3a90] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@` (pattern `WorkerAlarmMode`, offset `0x009a39c8`)
  context:
     [0x009a38e8] `.?AVCWorkerAlarmModeBehavior@GGL@@`
     [0x009a3918] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3970] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
  >> [0x009a39c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3a30] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3a90] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3af0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `WorkerAlarmMode`, offset `0x009a3a30`)
  context:
     [0x009a3918] `.?AV?$THandler@$0BFAEH@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3970] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a39c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
  >> [0x009a3a30] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3a90] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3af0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3b50] `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
- hit: `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `WorkerAlarmMode`, offset `0x009a3a90`)
  context:
     [0x009a3970] `.?AV?$THandler@$0BFAEI@VCEvent@BB@@V12@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a39c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3a30] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
  >> [0x009a3a90] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3af0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3b50] `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3bac] `.?AVCWorkerBattleBehaviorProps@GGL@@`
- hit: `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `WorkerAlarmMode`, offset `0x009a3af0`)
  context:
     [0x009a39c8] `.?AV?$THandler@$0BHAAP@VCEvent@BB@@VCEvent1Entity@EGL@@VCWorkerAlarmModeBehavior@GGL@@X@EGL@@`
     [0x009a3a30] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3a90] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
  >> [0x009a3af0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3b50] `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3bac] `.?AVCWorkerBattleBehaviorProps@GGL@@`
     [0x009a3bdc] `.?AVCWorkerBattleBehavior@GGL@@`
- hit: `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@` (pattern `WorkerAlarmMode`, offset `0x009a3b50`)
  context:
     [0x009a3a30] `.?AV?$THandler@$0IK@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3a90] `.?AV?$THandler@$0JO@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3af0] `.?AV?$THandler@$0IJ@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
  >> [0x009a3b50] `.?AV?$THandler@$0IL@VCGLETaskArgs@EGL@@V12@VCWorkerAlarmModeBehavior@GGL@@H@EGL@@`
     [0x009a3bac] `.?AVCWorkerBattleBehaviorProps@GGL@@`
     [0x009a3bdc] `.?AVCWorkerBattleBehavior@GGL@@`
     [0x009a3c08] `.?AV?$THandler@$0HA@VCGLETaskArgs@EGL@@V12@VCWorkerBattleBehavior@GGL@@H@EGL@@`

## attachments_and_entities

- patterns: 5 | hits: 7

- hit: `TaskLists` (pattern `TaskLists`, offset `0x007c80b0`)
  context:
     [0x007c8090] `GGL_Effects`
     [0x007c809c] `Models`
     [0x007c80a4] `AnimSets`
  >> [0x007c80b0] `TaskLists`
     [0x007c80bc] `GameCallback_SetDefaultValues`
     [0x007c80dc] `GameCallback_NewGame`
     [0x007c80f4] `Logic`
- hit: `Data\Config\TaskLists\` (pattern `TaskLists`, offset `0x007c82cc`)
  context:
     [0x007c8288] `PrincipalTask`
     [0x007c8298] `Task`
     [0x007c82c4] `  ID:`
  >> [0x007c82cc] `Data\Config\TaskLists\`
     [0x007c82f8] `SubAnimIdx`
     [0x007c8318] `LowerBound`
     [0x007c8324] `UpperBound`
- hit: `ATTACHMENT_WORKER_FARM` (pattern `ATTACHMENT_WORKER_FARM`, offset `0x007d47f0`)
  context:
     [0x007d4774] `ATTACHMENT_APPROACHING_SERF_CONSTRUCTION_SITE`
     [0x007d47a4] `ATTACHMENT_SERF_CONSTRUCTION_SITE`
     [0x007d47c8] `ATTACHMENT_CONSTRUCTION_SITE_BUILDING`
  >> [0x007d47f0] `ATTACHMENT_WORKER_FARM`
     [0x007d4808] `ATTACHMENT_WORKER_RESIDENCE`
     [0x007d4824] `ATTACHMENT_WORKER_WORKPLACE`
     [0x007d4840] `ATTACHMENT_MINE_RESOURCE`
- hit: `ATTACHMENT_WORKER_RESIDENCE` (pattern `ATTACHMENT_WORKER_RESIDENCE`, offset `0x007d4808`)
  context:
     [0x007d47a4] `ATTACHMENT_SERF_CONSTRUCTION_SITE`
     [0x007d47c8] `ATTACHMENT_CONSTRUCTION_SITE_BUILDING`
     [0x007d47f0] `ATTACHMENT_WORKER_FARM`
  >> [0x007d4808] `ATTACHMENT_WORKER_RESIDENCE`
     [0x007d4824] `ATTACHMENT_WORKER_WORKPLACE`
     [0x007d4840] `ATTACHMENT_MINE_RESOURCE`
     [0x007d485c] `ATTACHMENT_MINE_LORRY`
- hit: `ATTACHMENT_CAMP_SETTLER` (pattern `ATTACHMENT_CAMP_SETTLER`, offset `0x007d4954`)
  context:
     [0x007d4900] `ATTACHMENT_LEADER_SOLDIER`
     [0x007d491c] `ATTACHMENT_ATTACKER_TARGET`
     [0x007d4938] `ATTACHMENT_ATTACKED_DEAD`
  >> [0x007d4954] `ATTACHMENT_CAMP_SETTLER`
     [0x007d496c] `ATTACHMENT_ATTACKER_COMMAND_TARGET`
     [0x007d4990] `ATTACHMENT_BUILDING_BASE`
     [0x007d49ac] `ATTACHMENT_FOLLOWER_FOLLOWED`
- hit: `XD_Camp_Internal` (pattern `XD_Camp_Internal`, offset `0x007d72ec`)
  context:
     [0x007d7218] `SecondsLeftCamouflaged`
     [0x007d724c] `DurationSeconds`
     [0x007d725c] `DiscoveryRange`
  >> [0x007d72ec] `XD_Camp_Internal`
     [0x007d7300] `RemoveDelay`
     [0x007d7330] `NumTurnsToDeletion`
     [0x007d7360] `Range`
- hit: `SetWorkTaskListsPerCycle` (pattern `TaskLists`, offset `0x007dd104`)
  context:
     [0x007dd0c4] `GetNextLeader`
     [0x007dd0d4] `MoveSettler`
     [0x007dd0e0] `GetSettlerTypesInUpgradeCategory`
  >> [0x007dd104] `SetWorkTaskListsPerCycle`
     [0x007dd120] `SettlerStand`
     [0x007dd130] `FillSettlerUpgradeCostsTable`
     [0x007dd150] `SettlerAggressive`

## Limits

- Static string/RTTI evidence only, no instruction-level control-flow graph.
- Mangled handler names expose event/task wiring but not exact branch predicates.
