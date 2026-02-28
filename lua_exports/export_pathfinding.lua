-- =============================================================================
-- PATHFINDING EXPORT
-- Testet Erreichbarkeit zwischen wichtigen Punkten (HQ, Ressourcen, Bauplätze)
-- =============================================================================
-- Verwendung: In EMS Config Callback_OnGameStart einfügen
-- Output: Documents\Siedler5\Logs\Game.log
-- =============================================================================

function ExportPathfindingData()
    S5Hook.Log("=== PATHFINDING_EXPORT_START ===")

    -- Player 1 HQ Position
    local hqX, hqY = 41100, 23100

    -- Wichtige Zielpunkte zum Testen
    local testPoints = {
        -- Nächste Bäume
        {name="Tree1", x=42330, y=24030},
        {name="Tree2", x=41745, y=21626},
        {name="Tree3", x=42424, y=22173},

        -- Minen-Schächte (Eisen)
        {name="IronShaft1", x=36276, y=8927},
        {name="IronShaft2", x=37495, y=7801},
        {name="IronShaft3", x=37784, y=7266},

        -- Minen-Schächte (Stein)
        {name="StoneShaft1", x=40056, y=14891},
        {name="StoneShaft2", x=39321, y=14716},
        {name="StoneShaft3", x=38633, y=14720},

        -- Minen-Schächte (Lehm)
        {name="ClayShaft1", x=35181, y=19553},
        {name="ClayShaft2", x=35106, y=18872},
        {name="ClayShaft3", x=34991, y=17997},

        -- Minen-Schächte (Schwefel)
        {name="SulfurShaft1", x=44304, y=21484},
        {name="SulfurShaft2", x=44006, y=20978},
        {name="SulfurShaft3", x=44576, y=22120},

        -- Kleine Vorkommen
        {name="IronDeposit1", x=34325, y=7950},
        {name="IronDeposit2", x=36325, y=6750},
        {name="StoneDeposit1", x=42800, y=15100},
        {name="ClayDeposit1", x=31125, y=18750},
        {name="SulfurDeposit1", x=48125, y=20950},
        {name="SulfurDeposit2", x=47725, y=18550},

        -- Dorfzentrum-Slots
        {name="VCSlot1", x=39400, y=24300},
        {name="VCSlot2", x=34500, y=23700},
        {name="VCSlot3", x=43500, y=9400},
    }

    -- Erstelle temporären Serf für Pathfinding-Test
    local testSerf = nil
    local serfs = S5Hook.EntityIteratorTableize(
        Predicate.OfType(Entities.PU_Serf),
        Predicate.OfPlayer(1)
    )

    if #serfs > 0 then
        testSerf = serfs[1]
        S5Hook.Log("PATH_TEST_SERF|" .. testSerf)
    else
        S5Hook.Log("PATH_ERROR|No serf found for player 1")
        S5Hook.Log("=== PATHFINDING_EXPORT_END ===")
        return
    end

    -- Teste Pfade von HQ zu allen Zielpunkten
    for _, point in ipairs(testPoints) do
        -- Methode 1: Sektor-Vergleich (schnell)
        local _, _, hqSector = S5Hook.GetTerrainInfo(hqX, hqY)
        local _, _, targetSector = S5Hook.GetTerrainInfo(point.x, point.y)
        local sameSector = (hqSector == targetSector) and 1 or 0

        -- Methode 2: Distanz berechnen
        local dx = point.x - hqX
        local dy = point.y - hqY
        local distance = math.sqrt(dx*dx + dy*dy)

        -- Methode 3: Blocking am Zielpunkt
        local _, blocking = S5Hook.GetTerrainInfo(point.x, point.y)
        local walkable = (blocking == 0) and 1 or 0

        S5Hook.Log(string.format("PATH|%s|%d|%d|%d|%d|%.0f|%d|%d",
            point.name,
            point.x,
            point.y,
            hqSector,
            targetSector,
            distance,
            sameSector,
            walkable
        ))
    end

    S5Hook.Log("=== PATHFINDING_EXPORT_END ===")
end

-- Starte Export nach 2 Sekunden (wenn alles geladen ist)
function StartPathfindingExport()
    ExportPathfindingData()
end

StartSimpleJob("StartPathfindingExport")
