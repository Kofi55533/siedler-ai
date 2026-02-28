--##############################################################################--
--##                                                                          ##--
--##  Spawn Army Controller (flexibel ausbaufähig mit AttackPrio/Attackrange) ##--
--##                           by Maxi & McB                                  ##--
--##                       modifiziert by Kimichura                           ##--
--##																		  ##--
--## 				Benötigt: kimichurasdefarmy.lua + filter.lua			  ##--
--##																		  ##--
--##					Nur im SP(Ext) | MP Server nutzbar!				      ##--
--##																		  ##--
--##############################################################################--

--[[Anmerkung: Die neue mod. army ist mittlerweile die 
	stärkste s5 army, vlt sogar zu stark, evtl nerfen..]]

-- In FMA aufrufen: StartSimpleJob("WaypointsFunc")
Waypoints = {}
function AddWaypoints(name, points)
    Waypoints[name] = points
    points.i = 1
	points.additionalData = { -- added this table here
		lastAttack = 0;
		
		lastAttackMinDelta = 5000; -- min time between attack commands (in ms)
	};
end

Waypoints_AttackedBy = {}; -- TODO theoretisch unendlich wachsender table

function WaypointsFunc()
	local time = Logic.GetTimeMs();
	
	if Counter.Tick2("Waypoints", 1) then -- every sec
		for name, points in pairs(Waypoints) do
			if IsAlive(name) then
                if IsValid(points[points.i]) and IsNear(name, points[points.i], 1000) then
					points.i = points.i + 1
                    if IsDestroyed(points[points.i]) and points.loop then
                        points.i = 1
                    end
				end
				if IsValid(points[points.i]) then
					-- changed section
					local id = GetEntityId(name);
					local data = points.additionalData;
					local lastAttackDelta = time - data.lastAttack;
					local newAttackAllowed = lastAttackDelta >= data.lastAttackMinDelta;
					
					local current_command = Logic.LeaderGetCurrentCommand(id);
					
					local attack = false;
					
					if current_command == 0 then -- (entity is chasing or attacking something)
						if newAttackAllowed then
							attack = true;
						else
							-- do nothing (keep attacking)
						end;
					else
						attack = true;
					end;
					
					if attack then
						
						local player = Logic.EntityGetPlayer(id);
						local enemy_chunk = PlayerChunk_GetPlayerEnemyChunk(player);
						
						ChunkWrapper.UpdatePositions(enemy_chunk);
						
						local x, y = Logic.EntityGetPos(id);
						local enemies = ChunkWrapper.GetEntitiesWithHealthAndNotCamouflagedAndNotConstructionSiteInAreaInCMSorted(enemy_chunk, x, y, 3300);
						local current_command = Logic.LeaderGetCurrentCommand(id);
						
                        local is_cannon = Logic.IsEntityInCategory(id, EntityCategories.Cannon) == 1;
                        
                        -- reorder
                        local t = {};
                        for i = 1, table.getn(enemies) do
                            local enemy = enemies[i];
                            
                            if (Logic.IsWorker(enemy) == 1
                            and (
                               is_cannon
                            or Logic.IsSettlerAtWork(enemy) == 1
                            or Logic.IsSettlerAtFarm(enemy) == 1
                            or Logic.IsSettlerAtResidence(enemy) == 1)
                            ) then
                                -- entity is not attackable
                            else
							
								Waypoints_AttackedBy[enemy] = Waypoints_AttackedBy[enemy] or {n = 0; t = time};
								if time - Waypoints_AttackedBy[enemy].t > 12000 then
									Waypoints_AttackedBy[enemy].n = 0;
									Waypoints_AttackedBy[enemy].t = time;
								end;
								
								local x2, y2 = Logic.EntityGetPos(enemy);
								local d = math.sqrt((x-x2)^2 + (y-y2)^2);
								
								d = d + Waypoints_AttackedBy[enemy].n * 50;
								
								table.insert(t, {enemy, d});
								
							end;
						end;
						
							-- TODO min range for cannons!
						table.sort(t, function(a,b) return a[2] < b[2] end);
						
						enemies = {};
						for i = 1, table.getn(t) do
							table.insert(enemies, t[i][1]);
						end;
						--
						for i = 1, table.getn(enemies) do
							Logic.GroupAttack(id, enemies[i]);
							local current_command = Logic.LeaderGetCurrentCommand(id);
							if current_command == 3 then -- TODO maybe check something else? or check for anti event ( == 0)
								-- can't attack (so what, nothing to do here... target not reachable)
							else
								-- attack started... entity will move to target or long range it when possible
								data.lastAttack = time;
								
								Waypoints_AttackedBy[enemies[i]].n = Waypoints_AttackedBy[enemies[i]].n + 1;
								
								break;
							end;
						end;
					end;
					
					current_command = Logic.LeaderGetCurrentCommand(id);
					
					if current_command == 3 then
						local tX, tY = Logic.EntityGetPos(GetEntityId(points[points.i]));
						Logic.MoveSettler(id, tX, tY);
						data.lastAttack = 0;
					end;
					-- end of changed section
				end
			end
		end
	end
end

-- Beispiel:
--[[ 
StartSimpleJob("NameDerArmee")

function NameDerArmee()
    if IsExisting("Spawnername") then
    local SpawnPos = GetPosition("Spawnpoint")
	    if IsDestroyed("Truppname0") and IsDestroyed("Truppname1")  and IsDestroyed("Truppname2") and IsDestroyed("Truppname3")  and IsDestroyed("Truppname4") then
			if Counter.Tick2("NameDerArmee1", RespawnTime) then
				for i = 0, 4 do
					SetEntityName(AI.Entity_CreateFormation(3, Entities.PU_LeaderSword4, nil, 8, SpawnPos.X, SpawnPos.Y, 0, 1, 3, 0),"Truppname"..i)
					AddWaypoints("Truppname"..i, {"Waypoint1", "Waypoint2", "Waypoint3", "Waypoint4", loop=true})
					Logic.LeaderChangeFormationType(GetEntityId("Truppname"..i), math.random(1, 4))
				end
			end
        end
		--
        if IsDestroyed("Truppname5") and IsDestroyed("Truppname6") and IsDestroyed("Truppname7") and IsDestroyed("Truppname8") and IsDestroyed("Truppname9") then
			if Counter.Tick2("NameDerArmee2", RespawnTime) then
				for i = 5, 9 do
					SetEntityName(AI.Entity_CreateFormation(3, Entities.PU_LeaderBow4, nil, 8, SpawnPos.X, SpawnPos.Y, 0, 1, 3, 0),"Truppname"..i)
					AddWaypoints("Truppname"..i, {"Waypoint1", "Waypoint2", "Waypoint3", "Waypoint4", loop=true})
					Logic.LeaderChangeFormationType(GetEntityId("Truppname"..i), math.random(1, 4))
				end
			end
        end
    end
	if IsDead("Spawnername") then
		return true
	end
end 

-- Zusatzinfos:

- loop=true bedeutet, dass die Truppen vom letztem Waypoint zum erstem Waypoint zurücklaufen und ihren Weg "wiederholen". 
- Counter.Tick2("NameDerArmee1", RespawnTime) ist ein eingebauter Spawndelayer, wichtig ist IMMER ein neuer Name des Counter.Tick2! Hier im Beispiel "NameDerArmee1" und "NameDerArmee2"

]]

