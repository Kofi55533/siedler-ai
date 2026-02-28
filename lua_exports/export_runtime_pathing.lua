-- =============================================================================
-- RUNTIME PATHING EXPORT (REAL ENGINE)
-- Sends a real serf to target points and logs the traveled path over time.
-- =============================================================================
-- Output: Documents\...\Logs\Game.log
-- =============================================================================

RuntimePathingExport = {
    sample_interval = 0.25,   -- seconds between PATHPOS logs
    arrive_distance = 150,    -- cm
    max_time_per_target = 120.0,
    stall_timeout = 10.0,     -- no progress for this long -> fail
    progress_epsilon = 20.0,
    running = false,
    finished = false,
    serf_id = nil,
    current_idx = 0,
    start_time = 0.0,
    last_sample_time = 0.0,
    last_progress_time = 0.0,
    min_dist = 0.0,
    target = nil,
    targets = {
        {name="Tree1", x=42330, y=24030},
        {name="Tree2", x=41745, y=21626},
        {name="Tree3", x=42424, y=22173},
        {name="IronShaft1", x=36276, y=8927},
        {name="IronShaft2", x=37495, y=7801},
        {name="IronShaft3", x=37784, y=7266},
        {name="StoneShaft1", x=40056, y=14891},
        {name="StoneShaft2", x=39321, y=14716},
        {name="StoneShaft3", x=38633, y=14720},
        {name="ClayShaft1", x=35181, y=19553},
        {name="ClayShaft2", x=35106, y=18872},
        {name="ClayShaft3", x=34991, y=17997},
        {name="SulfurShaft1", x=44304, y=21484},
        {name="SulfurShaft2", x=44006, y=20978},
        {name="SulfurShaft3", x=44576, y=22120},
        {name="VCSlot1", x=39400, y=24300},
        {name="VCSlot2", x=34500, y=23700},
        {name="VCSlot3", x=43500, y=9400},
    },
}

local function dist(ax, ay, bx, by)
    local dx = ax - bx
    local dy = ay - by
    return math.sqrt(dx * dx + dy * dy)
end

local function logf(fmt, ...)
    S5Hook.Log(string.format(fmt, ...))
end

function RuntimePathingExport_SelectSerf()
    local serfs = S5Hook.EntityIteratorTableize(
        Predicate.OfType(Entities.PU_Serf),
        Predicate.OfPlayer(1)
    )
    if #serfs == 0 then
        return nil
    end
    return serfs[1]
end

function RuntimePathingExport_StartNextTarget()
    RuntimePathingExport.current_idx = RuntimePathingExport.current_idx + 1
    if RuntimePathingExport.current_idx > #RuntimePathingExport.targets then
        logf("RPATH|END|all_targets_done")
        RuntimePathingExport.finished = true
        RuntimePathingExport.running = false
        return
    end

    local idx = RuntimePathingExport.current_idx
    local target = RuntimePathingExport.targets[idx]
    RuntimePathingExport.target = target

    local sx, sy = Logic.GetEntityPosition(RuntimePathingExport.serf_id)
    local t = Logic.GetTime()
    RuntimePathingExport.start_time = t
    RuntimePathingExport.last_sample_time = t
    RuntimePathingExport.min_dist = dist(sx, sy, target.x, target.y)
    RuntimePathingExport.last_progress_time = t

    local cmd_ok = Logic.MoveSettler(RuntimePathingExport.serf_id, target.x, target.y)
    logf(
        "RPATH|CMD|%d|%s|%d|%d|%d|%d|%s",
        idx, target.name, sx, sy, target.x, target.y, tostring(cmd_ok)
    )
end

function RuntimePathingExport_Tick()
    if RuntimePathingExport.finished then
        return true
    end
    if not RuntimePathingExport.running then
        return nil
    end

    local idx = RuntimePathingExport.current_idx
    local target = RuntimePathingExport.target
    if target == nil then
        return nil
    end

    local x, y = Logic.GetEntityPosition(RuntimePathingExport.serf_id)
    local now = Logic.GetTime()
    local elapsed = now - RuntimePathingExport.start_time
    local d = dist(x, y, target.x, target.y)

    if d + RuntimePathingExport.progress_epsilon < RuntimePathingExport.min_dist then
        RuntimePathingExport.min_dist = d
        RuntimePathingExport.last_progress_time = now
    end

    if now - RuntimePathingExport.last_sample_time >= RuntimePathingExport.sample_interval then
        RuntimePathingExport.last_sample_time = now
        logf(
            "RPATH|POS|%d|%s|%.2f|%d|%d|%.1f",
            idx, target.name, elapsed, x, y, d
        )
    end

    if d <= RuntimePathingExport.arrive_distance then
        logf(
            "RPATH|DONE|%d|%s|%.2f|%.1f",
            idx, target.name, elapsed, RuntimePathingExport.min_dist
        )
        RuntimePathingExport_StartNextTarget()
        return nil
    end

    if elapsed > RuntimePathingExport.max_time_per_target then
        logf(
            "RPATH|FAIL|%d|%s|timeout|%.2f|%.1f",
            idx, target.name, elapsed, RuntimePathingExport.min_dist
        )
        RuntimePathingExport_StartNextTarget()
        return nil
    end

    if now - RuntimePathingExport.last_progress_time > RuntimePathingExport.stall_timeout then
        logf(
            "RPATH|FAIL|%d|%s|stalled|%.2f|%.1f",
            idx, target.name, elapsed, RuntimePathingExport.min_dist
        )
        RuntimePathingExport_StartNextTarget()
        return nil
    end

    return nil
end

function RuntimePathingExport_Start()
    if not S5Hook then
        Message("RPATH: S5Hook missing")
        return
    end
    RuntimePathingExport.serf_id = RuntimePathingExport_SelectSerf()
    if RuntimePathingExport.serf_id == nil then
        logf("RPATH|ERROR|no_serf_found")
        return
    end

    RuntimePathingExport.running = true
    RuntimePathingExport.finished = false
    RuntimePathingExport.current_idx = 0

    local sx, sy = Logic.GetEntityPosition(RuntimePathingExport.serf_id)
    logf("RPATH|START|serf=%d|x=%d|y=%d|targets=%d",
        RuntimePathingExport.serf_id, sx, sy, #RuntimePathingExport.targets)

    RuntimePathingExport_StartNextTarget()
    StartSimpleHiResJob("RuntimePathingExport_Tick")
end

RuntimePathingExport_Start()
