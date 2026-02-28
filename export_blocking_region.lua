-- Export blocking values for a specific region (Wintersturm)
-- Logs to Settlers5 logfile via S5Hook.Log
--
-- Usage:
-- 1) Open map in Map Editor -> Map/Script Wizard -> Edit Script
-- 2) Paste this file content into the map script (or load it via Script.Load)
-- 3) Start the map once in-game. The export runs on GameCallback_OnGameStart.
--
-- Output in log:
--   BLOCKING_EXPORT_START,x_min,x_max,y_min,y_max,step
--   BROW,y,val1,val2,...
--   BLOCKING_EXPORT_END

if not S5Hook or not S5Hook.Log then
    -- Try to load S5Hook if available (EMS tools)
    if Script and Script.Load then
        -- Common EMS tool path inside extra2
        Script.Load("maps\\user\\EMS\\tools\\S5Hook.lua")
    end
end

BlockingExport = {
    x_min = 25500,
    x_max = 28200,
    y_min = 4500,
    y_max = 11800,
    step = 100
}

function BlockingExport_Dump()
    if not S5Hook or not S5Hook.Log then
        if Logic and Logic.DebugLog then
            Logic.DebugLog("BlockingExport: S5Hook.Log not available")
        end
        return
    end

    local x_min = BlockingExport.x_min
    local x_max = BlockingExport.x_max
    local y_min = BlockingExport.y_min
    local y_max = BlockingExport.y_max
    local step = BlockingExport.step

    S5Hook.Log(string.format("BLOCKING_EXPORT_START,%d,%d,%d,%d,%d", x_min, x_max, y_min, y_max, step))

    for y = y_min, y_max, step do
        local row = {}
        for x = x_min, x_max, step do
            local v = CUtil.GetBlocking100(x, y)
            row[#row + 1] = tostring(v)
        end
        S5Hook.Log("BROW," .. tostring(y) .. "," .. table.concat(row, ","))
    end

    S5Hook.Log("BLOCKING_EXPORT_END")
end

if not _G.__BLOCKING_EXPORT_HOOKED then
    _G.__BLOCKING_EXPORT_HOOKED = true
    local _orig = GameCallback_OnGameStart
    function GameCallback_OnGameStart()
        if _orig then
            _orig()
        end
        BlockingExport_Dump()
    end
end
