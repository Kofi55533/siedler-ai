-- =============================================================================
-- SIEDLER 5 - VOLLSTÄNDIGER GAME DATA EXPORT für RL Environment
-- =============================================================================
-- Exportiert via S5Hook.Log ins Spiel-Log:
-- 1. Terrain-Daten (Height, Blocking, Sector, TerrainType)
-- 2. Entity-Positionen (Bäume, Minen, Deposits, Gebäude)
-- 3. Spieler-Daten
-- =============================================================================

GameDataExport = {
    -- Export-Region (Player 1 Quadrant von Wintersturm)
    x_min = 25000,
    x_max = 51000,
    y_min = 0,
    y_max = 25500,
    step = 100,

    -- Flags
    export_terrain = true,
    export_entities = true,
    export_player_data = true,
}

-- =============================================================================
-- TERRAIN EXPORT (Height, Blocking, Sector, TerrainType)
-- =============================================================================
function GameDataExport_Terrain()
    if not S5Hook or not S5Hook.GetTerrainInfo then
        Message("FEHLER: S5Hook.GetTerrainInfo nicht verfuegbar!")
        return
    end

    local x_min = GameDataExport.x_min
    local x_max = GameDataExport.x_max
    local y_min = GameDataExport.y_min
    local y_max = GameDataExport.y_max
    local step = GameDataExport.step

    -- Header mit allen 4 Datentypen
    S5Hook.Log(string.format("TERRAIN_EXPORT_START,%d,%d,%d,%d,%d", x_min, x_max, y_min, y_max, step))

    for y = y_min, y_max, step do
        local heights = {}
        local blockings = {}
        local sectors = {}
        local terrains = {}

        for x = x_min, x_max, step do
            local height, blocking, sector, terrain = S5Hook.GetTerrainInfo(x, y)
            table.insert(heights, tostring(math.floor(height or 0)))
            table.insert(blockings, tostring(blocking or 0))
            table.insert(sectors, tostring(sector or 0))
            table.insert(terrains, tostring(terrain or 0))
        end

        S5Hook.Log("THEIGHT," .. tostring(y) .. "," .. table.concat(heights, ","))
        S5Hook.Log("TBLOCK," .. tostring(y) .. "," .. table.concat(blockings, ","))
        S5Hook.Log("TSECTOR," .. tostring(y) .. "," .. table.concat(sectors, ","))
        S5Hook.Log("TTERRAIN," .. tostring(y) .. "," .. table.concat(terrains, ","))
    end

    S5Hook.Log("TERRAIN_EXPORT_END")
end

-- =============================================================================
-- ENTITY EXPORT (Bäume, Ressourcen, Minen, Gebäude)
-- =============================================================================
function GameDataExport_Entities()
    if not S5Hook or not S5Hook.EntityIteratorTableize then
        Message("FEHLER: S5Hook.EntityIterator nicht verfuegbar!")
        return
    end

    S5Hook.Log("ENTITY_EXPORT_START")

    -- Bäume (XD_Tree*, XD_Fir*, XD_Pine*, etc.)
    local tree_types = {
        Entities.XD_Fir1, Entities.XD_Fir2, Entities.XD_Fir3,
        Entities.XD_Pine1, Entities.XD_Pine2, Entities.XD_Pine3,
        Entities.XD_Tree1, Entities.XD_Tree2, Entities.XD_Tree3,
        Entities.XD_Cypress1, Entities.XD_Cypress2,
        Entities.XD_Willow1, Entities.XD_Willow2,
    }

    for _, tree_type in ipairs(tree_types) do
        if tree_type then
            local trees = S5Hook.EntityIteratorTableize(Predicate.OfType(tree_type))
            for _, eID in ipairs(trees) do
                local x, y = Logic.GetEntityPosition(eID)
                local res = Logic.GetResourceDoodadGoodAmount(eID)
                local name = Logic.GetEntityTypeName(Logic.GetEntityType(eID))
                S5Hook.Log(string.format("TREE,%d,%.0f,%.0f,%d,%s", eID, x, y, res or 0, name or ""))
            end
        end
    end

    -- Stollen (XD_Iron1, XD_Stone1, XD_Clay1, XD_Sulfur1) - kleine Ressourcen-Punkte
    local shaft_types = {
        {Entities.XD_Iron1, "Iron"},
        {Entities.XD_Stone1, "Stone"},
        {Entities.XD_Clay1, "Clay"},
        {Entities.XD_Sulfur1, "Sulfur"},
    }

    for _, shaft_info in ipairs(shaft_types) do
        local shaft_type, res_name = shaft_info[1], shaft_info[2]
        if shaft_type then
            local shafts = S5Hook.EntityIteratorTableize(Predicate.OfType(shaft_type))
            for _, eID in ipairs(shafts) do
                local x, y = Logic.GetEntityPosition(eID)
                local res = Logic.GetResourceDoodadGoodAmount(eID)
                S5Hook.Log(string.format("SHAFT,%d,%.0f,%.0f,%d,%s", eID, x, y, res or 0, res_name))
            end
        end
    end

    -- Vorkommen/Deposits (XD_IronPit1, XD_StonePit1, etc.) - wo Minen gebaut werden
    local pit_types = {
        {Entities.XD_IronPit1, "Iron"},
        {Entities.XD_StonePit1, "Stone"},
        {Entities.XD_ClayPit1, "Clay"},
        {Entities.XD_SulfurPit1, "Sulfur"},
    }

    for _, pit_info in ipairs(pit_types) do
        local pit_type, res_name = pit_info[1], pit_info[2]
        if pit_type then
            local pits = S5Hook.EntityIteratorTableize(Predicate.OfType(pit_type))
            for _, eID in ipairs(pits) do
                local x, y = Logic.GetEntityPosition(eID)
                local res = Logic.GetResourceDoodadGoodAmount(eID)
                S5Hook.Log(string.format("DEPOSIT,%d,%.0f,%.0f,%d,%s", eID, x, y, res or 0, res_name))
            end
        end
    end

    -- Gebäude aller Spieler
    local buildings = S5Hook.EntityIteratorTableize(Predicate.IsBuilding())
    for _, eID in ipairs(buildings) do
        local x, y = Logic.GetEntityPosition(eID)
        local player = Logic.EntityGetPlayer(eID)
        local etype = Logic.GetEntityType(eID)
        local name = Logic.GetEntityTypeName(etype)
        local hp = Logic.GetEntityHealth(eID)
        local max_hp = Logic.GetEntityMaxHealth(eID)
        S5Hook.Log(string.format("BUILDING,%d,%.0f,%.0f,%d,%s,%d,%d", eID, x, y, player, name or "", hp or 0, max_hp or 0))
    end

    -- Siedler/Units aller Spieler
    local settlers = S5Hook.EntityIteratorTableize(Predicate.IsSettler())
    for _, eID in ipairs(settlers) do
        local x, y = Logic.GetEntityPosition(eID)
        local player = Logic.EntityGetPlayer(eID)
        local etype = Logic.GetEntityType(eID)
        local name = Logic.GetEntityTypeName(etype)
        S5Hook.Log(string.format("SETTLER,%d,%.0f,%.0f,%d,%s", eID, x, y, player, name or ""))
    end

    S5Hook.Log("ENTITY_EXPORT_END")
end

-- =============================================================================
-- PLAYER DATA EXPORT (Ressourcen, Technologien, etc.)
-- =============================================================================
function GameDataExport_PlayerData()
    S5Hook.Log("PLAYER_DATA_START")

    for player = 1, 4 do
        -- Ressourcen
        local gold = Logic.GetPlayersGlobalResource(player, ResourceType.Gold) or 0
        local clay = Logic.GetPlayersGlobalResource(player, ResourceType.Clay) or 0
        local wood = Logic.GetPlayersGlobalResource(player, ResourceType.Wood) or 0
        local stone = Logic.GetPlayersGlobalResource(player, ResourceType.Stone) or 0
        local iron = Logic.GetPlayersGlobalResource(player, ResourceType.Iron) or 0
        local sulfur = Logic.GetPlayersGlobalResource(player, ResourceType.Sulfur) or 0

        S5Hook.Log(string.format("PLAYER_RES,%d,%d,%d,%d,%d,%d,%d", player, gold, clay, wood, stone, iron, sulfur))

        -- HQ Position
        local hq = Logic.GetHeadquarters(player)
        if hq and hq > 0 then
            local hx, hy = Logic.GetEntityPosition(hq)
            S5Hook.Log(string.format("PLAYER_HQ,%d,%.0f,%.0f", player, hx, hy))
        end
    end

    S5Hook.Log("PLAYER_DATA_END")
end

-- =============================================================================
-- MAIN EXPORT FUNCTION
-- =============================================================================
function GameDataExport_Run()
    if not S5Hook then
        Message("FEHLER: S5Hook nicht verfuegbar!")
        return false
    end

    Message("GAME DATA EXPORT gestartet...")
    S5Hook.Log("=== SIEDLER 5 GAME DATA EXPORT ===")
    S5Hook.Log("MAP_NAME," .. (Framework.GetCurrentMapName and Framework.GetCurrentMapName() or "unknown"))

    if GameDataExport.export_terrain then
        Message("Exportiere Terrain-Daten...")
        GameDataExport_Terrain()
    end

    if GameDataExport.export_entities then
        Message("Exportiere Entity-Daten...")
        GameDataExport_Entities()
    end

    if GameDataExport.export_player_data then
        Message("Exportiere Spieler-Daten...")
        GameDataExport_PlayerData()
    end

    S5Hook.Log("=== EXPORT COMPLETE ===")
    Message("GAME DATA EXPORT abgeschlossen!")
    return true
end
