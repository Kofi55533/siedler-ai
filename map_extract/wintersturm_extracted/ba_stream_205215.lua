-- Global table to hold all player chunk informations
PLAYER_CHUNK_INFO = {
	--[[
	[playerID] : {
		chunk : ChunkWrapper;
		diplomacyState : {
			[pID] : state;
		};
	};
	]]
};

function PlayerChunk_IsEnemy(_id, _playerID)
	local player = Logic.EntityGetPlayer(_id);
	if player == 0 or player == _playerID then
		return false;
	end;
	
    return
    (
    Logic.IsWorker(_id) == 1
    or Logic.IsLeader(_id) == 1
    or (Logic.IsBuilding(_id) == 1 and Logic.IsEntityInCategory(_id,EntityCategories.Wall) == 0)
    or Logic.IsSerf(_id) == 1
    --or Logic.IsSettler(_id) == 1
    )
    and Logic.GetDiplomacyState(_playerID, player) == Diplomacy.Hostile;
end;

-- do initial setup of all 8 (sp) or 16 (mp) chunks
do
	local nplayers = XNetwork.Manager_DoesExist() == 1 and 16 or 8;
	for i = 1, nplayers do
		local filter = ChunkFilter.new();
		ChunkFilter.AddFunctionFilter(filter, PlayerChunk_IsEnemy, i);
		PLAYER_CHUNK_INFO[i] = {
			chunk = ChunkWrapper.new(filter);
			diplomacyState = {};
		};
		
		for j = 1, nplayers do
			PLAYER_CHUNK_INFO[i].diplomacyState[j] = Logic.GetDiplomacyState(i, j);
		end;
		
		do
			ChunkWrapper.InitAllExistingEntities(PLAYER_CHUNK_INFO[i].chunk);
		end;
	end;
end;


function PlayerChunk_DiplomacyChanged()
	local p = Event.GetSourcePlayerID();
	local p2 = Event.GetTargetPlayerID();
	local state = Event.GetDiplomacyState();
	
	local chunk_info = PLAYER_CHUNK_INFO[p];
	
	local old_state = chunk_info.diplomacyState[p2];
	
	local was_hostile = Diplomacy.Hostile == old_state;
	local is_hostile = Diplomacy.Hostile == state;
	
	chunk_info.diplomacyState[p2] = state;
	
	if was_hostile ~= is_hostile then
		local chunk = chunk_info.chunk;
		
		if is_hostile then -- add
			--LuaDebugger.Log("Add: " .. p .. " " .. p2);
			for id in CEntityIterator.Iterator(CEntityIterator.OfPlayerFilter(p2)) do
				ChunkWrapper.AddEntityApplyFilter(chunk, id);
			end;
		else -- remove
			--LuaDebugger.Log("Remove: " .. p .. " " .. p2);
			for id in CEntityIterator.Iterator(CEntityIterator.OfPlayerFilter(p2)) do
				ChunkWrapper.RemoveEntity(chunk, id);
			end;
		end;
	end;
end;

-- setup trigger
Trigger.RequestTrigger(Events.LOGIC_EVENT_DIPLOMACY_CHANGED, "", "PlayerChunk_DiplomacyChanged", 1);

function PlayerChunk_GetPlayerEnemyChunk(_playerID)
	return PLAYER_CHUNK_INFO[_playerID].chunk;
end;
