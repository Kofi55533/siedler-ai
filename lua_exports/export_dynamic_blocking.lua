-- =============================================================================
-- DYNAMIC BLOCKING EXPORT
-- Loggt Blocking-Änderungen über Zeit während des Spielens
-- =============================================================================
-- Verwendung: In EMS Config Callback_OnGameStart einfügen
-- Output: Documents\Siedler5\Logs\Game.log
-- =============================================================================

-- Konfiguration
local SNAPSHOT_INTERVAL = 30  -- Sekunden zwischen Snapshots
local GRID_STEP = 200         -- Auflösung (kleiner = mehr Daten)
local PLAYER_1_AREA = {
    x_min = 34000,
    x_max = 50000,
    y_min = 6000,
    y_max = 26000
}

-- State
local snapshotCount = 0
local lastSnapshot = {}
local gameStartTime = 0

function InitDynamicBlockingExport()
    gameStartTime = Logic.GetTime()
    S5Hook.Log("=== DYNAMIC_BLOCKING_INIT ===")
    S5Hook.Log("GRID_STEP|" .. GRID_STEP)
    S5Hook.Log("INTERVAL|" .. SNAPSHOT_INTERVAL)

    -- Erster Snapshot sofort
    TakeBlockingSnapshot()

    -- Starte periodischen Job
    StartSimpleHiResJob("CheckSnapshotTime")
end

function CheckSnapshotTime()
    local currentTime = Logic.GetTime()
    local elapsed = currentTime - gameStartTime
    local expectedSnapshots = math.floor(elapsed / SNAPSHOT_INTERVAL)

    if expectedSnapshots > snapshotCount then
        TakeBlockingSnapshot()
    end

    -- Job läuft weiter (return nil = weiterlaufen)
    return nil
end

function TakeBlockingSnapshot()
    snapshotCount = snapshotCount + 1
    local timestamp = Logic.GetTime() - gameStartTime

    S5Hook.Log(string.format("=== SNAPSHOT_%d_START|%.1f ===", snapshotCount, timestamp))

    -- Zähle Änderungen
    local changes = 0
    local newSnapshot = {}

    -- Scanne das Grid
    for x = PLAYER_1_AREA.x_min, PLAYER_1_AREA.x_max, GRID_STEP do
        for y = PLAYER_1_AREA.y_min, PLAYER_1_AREA.y_max, GRID_STEP do
            local _, blocking, sector = S5Hook.GetTerrainInfo(x, y)
            local key = x .. "_" .. y
            local value = blocking .. "_" .. sector

            newSnapshot[key] = value

            -- Vergleiche mit letztem Snapshot
            if lastSnapshot[key] then
                if lastSnapshot[key] ~= value then
                    -- Änderung gefunden!
                    local oldBlocking, oldSector = string.match(lastSnapshot[key], "(%d+)_(%d+)")
                    changes = changes + 1

                    -- Log nur die Änderungen (nicht alles)
                    S5Hook.Log(string.format("CHANGE|%d|%d|%s|%s",
                        x, y,
                        lastSnapshot[key],
                        value
                    ))
                end
            else
                -- Erster Snapshot - log nur blockierte Punkte
                if blocking > 0 and snapshotCount == 1 then
                    S5Hook.Log(string.format("INITIAL_BLOCKED|%d|%d|%d|%d",
                        x, y, blocking, sector
                    ))
                end
            end
        end
    end

    lastSnapshot = newSnapshot

    -- Log Zusammenfassung
    S5Hook.Log(string.format("SNAPSHOT_SUMMARY|%d|%.1f|%d",
        snapshotCount, timestamp, changes
    ))

    -- Log auch aktuelle Gebäude/Bäume Anzahl
    local buildings = #S5Hook.EntityIteratorTableize(
        Predicate.IsBuilding(),
        Predicate.OfPlayer(1)
    )
    local trees = #S5Hook.EntityIteratorTableize(
        Predicate.OfCategory(EntityCategories.ResourceDoodad)
    )

    S5Hook.Log(string.format("ENTITY_COUNT|%d|%d|%d",
        snapshotCount, buildings, trees
    ))

    S5Hook.Log(string.format("=== SNAPSHOT_%d_END ===", snapshotCount))
end

-- Event-basiertes Logging (zusätzlich zu Snapshots)
function OnBuildingConstructed(entityId)
    local entityType = Logic.GetEntityType(entityId)
    local typeName = Logic.GetEntityTypeName(entityType)
    local x, y = Logic.GetEntityPosition(entityId)
    local timestamp = Logic.GetTime() - gameStartTime

    S5Hook.Log(string.format("EVENT_BUILD|%.1f|%d|%s|%.0f|%.0f",
        timestamp, entityId, typeName, x, y
    ))
end

function OnEntityDestroyed(entityId)
    local timestamp = Logic.GetTime() - gameStartTime
    S5Hook.Log(string.format("EVENT_DESTROY|%.1f|%d",
        timestamp, entityId
    ))
end

-- Starte Export
InitDynamicBlockingExport()
