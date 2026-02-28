GFXSetHandler = {}


function Mission_InitWeatherGfxSetsForAllMaps()
	Display.SetRenderUseGfxSets(1)
	GFXSetHandler.InitSummerSet()
	GFXSetHandler.InitRainSet()
	GFXSetHandler.InitWinterSet()

	--Sommertage
	AddPeriodicSummer(15*60);
	AddPeriodicRain(3*60);
	AddPeriodicSummer(12*60);
	AddPeriodicRain(2*60);
	AddPeriodicSummer(8*60);
end

function SetupHighlandWeatherGfxSet()
	Mission_InitWeatherGfxSetsForAllMaps()
end

---------------------------------------------------------Sommer------------------------------------------------------------
function GFXSetHandler.InitSummerSet()
	Display.GfxSetSetSkyBox(1, 0.0, 1.0, "YSkyBox07")
	Display.GfxSetSetRainEffectStatus(1, 0.0, 1.0, 0)
	Display.GfxSetSetSnowStatus(1, 0, 1.0, 0)
	Display.GfxSetSetSnowEffectStatus(1, 0.0, 0.8, 0)
	Display.GfxSetSetFogParams(1, 0.0, 1.0, 1, 130 , 150 , 170 , 6000, 23000)
	Display.GfxSetSetLightParams(1, 0.0, 1.0, 40, -15, -50, 145, 155, 165, 240, 220, 100) 
end
-- Display.GfxSetSetFogParams(1, 0.0, 1.0, 1, 120 , 140 , 160 , 3000, 23000) --bei Zoomstufe 1

---------------------------------------------------------Regen-------------------------------------------------------------
function GFXSetHandler.InitRainSet()
	Display.GfxSetSetSkyBox(2, 0.0, 1.0, "YSkyBox04")
	Display.GfxSetSetRainEffectStatus(2, 0.0, 1.0, 1)
	Display.GfxSetSetSnowStatus(2, 0, 1.0, 0)
	Display.GfxSetSetSnowEffectStatus(2, 0.0, 0.8, 0)
	Display.GfxSetSetFogParams(2, 0.0, 1.0, 1, 120, 140, 160, 5000, 20000) --ChatGpt-Vorschlag
	Display.GfxSetSetLightParams(2, 0.0, 1.0, 40, -15, -50, 70, 80, 90, 150, 160, 170) --ChatGpt-Vorschlag
end
-- Display.GfxSetSetFogParams(2, 0.0, 1.0, 1, 120, 140, 160, 0, 20000) --bei Zoomstufe 1

---------------------------------------------------------Winter------------------------------------------------------------
function GFXSetHandler.InitWinterSet()
	Display.GfxSetSetSkyBox(3, 0.0, 1.0, "YSkyBox01")
	Display.GfxSetSetRainEffectStatus(3, 0.0, 1.0, 0)
	Display.GfxSetSetSnowStatus(3, 0, 1.0, 1)
	Display.GfxSetSetSnowEffectStatus(3, 0.0, 0.8, 1)
	Display.GfxSetSetFogParams(3, 0.0, 1.0, 1, 200, 220, 230,  7000 , 22000) --ChatGpt-Vorschlag
	Display.GfxSetSetLightParams(3, 0.0, 1.0, 40, -15, -50, 100, 110 , 120, 200 , 190, 180) --ChatGpt-Vorschlag
end
-- Display.GfxSetSetFogParams(3, 0.0, 1.0, 1, 200, 220, 230,  0 , 22000) --bei Zoomstufe 1

function GFXSetHandler.InitWeather()
	GFXSetHandler.InitSummerSet()
	GFXSetHandler.InitRainSet()
	GFXSetHandler.InitWinterSet()
end
----------------------------------------------------------------------------------------------------------------------------
function GFXSetHandler.UpdateFog()
	
	local currentZoom = Camera.GetZoomFactor()
	
	--SummerFog
	local GFXFogSummer = 3000 * currentZoom
	Display.GfxSetSetFogParams(1, 0.0, 1.0, 1, 120 , 140 , 160 , GFXFogSummer , 23000)
	
	--RainFog
	local GFXFogRain = 5000 * currentZoom - 5000
	Display.GfxSetSetFogParams(2, 0.0, 1.0, 1, 120, 140, 160, GFXFogRain, 20000)
	
	--WinterFog
	local GFXFogWinter = 7000 * currentZoom - 7000
	Display.GfxSetSetFogParams(3, 0.0, 1.0, 1, 200, 220, 230,  GFXFogWinter , 22000)
end
----------------------------------------------------------------------------------------------------------------------------

InputCallback_MouseWheelNew = InputCallback_MouseWheelNew or InputCallback_MouseWheel
function InputCallback_MouseWheel( _Forward )
	InputCallback_MouseWheelNew( _Forward )
	GFXSetHandler.UpdateFog()
end



    