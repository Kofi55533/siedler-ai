-- =============================================================================
-- BUILDING BLOCKING EXPORT
-- Exportiert welche Terrain-Punkte durch Gebäude blockiert werden
-- =============================================================================
-- Verwendung: In EMS Config Callback_OnGameStart einfügen
-- Output: Documents\Siedler5\Logs\Game.log
-- =============================================================================

function ExportBuildingBlocking()
    S5Hook.Log("=== BUILDING_BLOCKING_EXPORT_START ===")

    -- Alle Gebäude auf der Karte finden
    local buildings = S5Hook.EntityIteratorTableize(
        Predicate.IsBuilding()
    )

    S5Hook.Log("BUILDING_COUNT|" .. #buildings)

    for _, buildingId in ipairs(buildings) do
        local entityType = Logic.GetEntityType(buildingId)
        local typeName = Logic.GetEntityTypeName(entityType)
        local player = Logic.GetEntityPlayerID(buildingId)
        local x, y = Logic.GetEntityPosition(buildingId)

        -- Gebäude-Größe über Blocked-Bereich ermitteln
        -- Teste Grid um das Gebäude herum
        local blockSize = 0
        local blockedPoints = {}

        -- Scanne 20x20 Grid um Gebäude (in 100er Schritten)
        for dx = -1000, 1000, 100 do
            for dy = -1000, 1000, 100 do
                local testX = x + dx
                local testY = y + dy

                -- Prüfe ob dieser Punkt durch das Gebäude blockiert wird
                local _, blocking = S5Hook.GetTerrainInfo(testX, testY)

                if blocking > 0 then
                    -- Ist es wegen diesem Gebäude blockiert?
                    -- Heuristik: Punkte nahe am Gebäudezentrum
                    local dist = math.sqrt(dx*dx + dy*dy)
                    if dist < 600 then  -- Innerhalb 600 units = wahrscheinlich dieses Gebäude
                        table.insert(blockedPoints, {dx=dx, dy=dy})
                        blockSize = blockSize + 1
                    end
                end
            end
        end

        -- Log building info
        S5Hook.Log(string.format("BUILDING|%d|%s|%d|%.0f|%.0f|%d",
            buildingId,
            typeName,
            player,
            x,
            y,
            blockSize
        ))

        -- Log blocked points (first 20 max to avoid spam)
        local maxPoints = math.min(#blockedPoints, 20)
        for i = 1, maxPoints do
            local p = blockedPoints[i]
            S5Hook.Log(string.format("BLOCKED|%d|%d|%d",
                buildingId,
                p.dx,
                p.dy
            ))
        end
    end

    S5Hook.Log("=== BUILDING_BLOCKING_EXPORT_END ===")
end

-- Alternative: Teste Baubarkeit an verschiedenen Positionen
function ExportBuildabilityGrid()
    S5Hook.Log("=== BUILDABILITY_EXPORT_START ===")

    -- Player 1 HQ Bereich
    local startX = 38000
    local startY = 20000
    local endX = 45000
    local endY = 26000
    local step = 400  -- Grid-Auflösung

    -- Gebäudetypen zum Testen
    local buildingTypes = {
        {name="Wohnhaus", type=Entities.PB_Residence1},
        {name="Bauernhof", type=Entities.PB_Farm1},
        {name="Hochschule", type=Entities.PB_University1},
    }

    for _, building in ipairs(buildingTypes) do
        S5Hook.Log("BUILDTYPE|" .. building.name)

        local buildableCount = 0
        for x = startX, endX, step do
            for y = startY, endY, step do
                -- Prüfe ob hier gebaut werden kann
                local canBuild = Logic.CanBuildingBeBuiltOnPosition(
                    1,  -- Player 1
                    building.type,
                    x, y,
                    0   -- Rotation
                )

                if canBuild == 1 then
                    buildableCount = buildableCount + 1
                    -- Nur die ersten 50 loggen
                    if buildableCount <= 50 then
                        S5Hook.Log(string.format("CANBUILD|%s|%d|%d",
                            building.name, x, y
                        ))
                    end
                end
            end
        end

        S5Hook.Log(string.format("BUILDABLE_TOTAL|%s|%d",
            building.name, buildableCount
        ))
    end

    S5Hook.Log("=== BUILDABILITY_EXPORT_END ===")
end

-- Starte beide Exports
function StartBuildingExports()
    ExportBuildingBlocking()
    -- ExportBuildabilityGrid()  -- Auskommentiert wegen Länge
end

StartSimpleJob("StartBuildingExports")
