# Tech Effects Coverage Report

Vergleich: Technologien aus Original (config/game_data.json) vs. implementierte Effekte in environment.py (TECHNOLOGY_EFFECTS).

## Zusammenfassung
- Originale T_ Technologien (Effects): 80
- Implementiert (T_ in TECHNOLOGY_EFFECTS): 31
- Fehlend (T_ gesamt): 49
  - Davon als Kampf-relevant erkannt: 17
  - Davon nicht-Kampf (Wirtschaft/Gebaeude/Utility): 32

## Implementierte T_-Effekte (mit Environment-Name)
- T_BETTERTRAININGBARRACKS -> Kasernentraining
- T_BETTERTRAININGARCHERY -> Schießtraining
- T_SHOEING -> Hufbeschlag
- T_BETTERCHASSIS -> Verbessertes Fahrgestell
- T_TOWNGUARD -> Stadtwache
- T_LOOM -> Webstuhl
- T_SHOES -> Schuhe
- T_LIGHTBRICKS -> Leichte Ziegel
- T_MASONRY -> Maurerarbeit
- T_LEATHERMAILARMOR -> Lederrüstung
- T_CHAINMAILARMOR -> Kettenrüstung
- T_PLATEMAILARMOR -> Plattenrüstung
- T_SOFTARCHERARMOR -> Schützenrüstung
- T_PADDEDARCHERARMOR -> Gepolsterte Schützenrüstung
- T_LEATHERARCHERARMOR -> Lederne Schützenrüstung
- T_MASTEROFSMITHERY -> Schwertschmied
- T_IRONCASTING -> Waffenmeister
- T_FLETCHING -> Pfeilherstellung
- T_BODKINARROW -> Panzerbrechende Pfeile
- T_WOODAGING -> Holzalterung
- T_TURNERY -> Drechselei
- T_ENHANCEDGUNPOWDER -> Verbessertes Schießpulver
- T_BLISTERINGCANNONBALLS -> Sprenggeschosse
- T_DEBENTURE -> Schuldschein
- T_BOOKKEEPING -> Buchführung
- T_SCALE -> Waage
- T_COINAGE -> Münzprägung
- T_FLEECEARMOR -> Vliesrüstung
- T_FLEECELINEDLEATHERARMOR -> Vliesgefütterte Lederrüstung
- T_LEADSHOT -> Bleikugeln
- T_SIGHTS -> Zielfernrohr

## Fehlende T_-Effekte (Nicht-Kampf)
- T_ADJUSTTAXES
- T_BLESSSETTLERS1
- T_BLESSSETTLERS2
- T_BLESSSETTLERS3
- T_BLESSSETTLERS4
- T_BLESSSETTLERS5
- T_CHANGEWEATHER
- T_CITYGUARD
- T_CROPCYCLE
- T_MAKERAIN
- T_MAKESNOW
- T_MAKESUMMER
- T_MARKETCLAY
- T_MARKETGOLD
- T_MARKETIRON
- T_MARKETSTONE
- T_MARKETSULFUR
- T_MARKETWOOD
- T_MINIMAPNORMALVIEW
- T_MINIMAPRESOUCEVIEW
- T_MINIMAPTACTICVIEW
- T_ONLINEHELP
- T_PICKAXE
- T_SCOUTFINDRESOURCES
- T_SCOUTTORCHES
- T_SPINNINGWHEEL
- T_SUPERTECHNOLOGY
- T_TEST
- T_TEST2
- T_THIEFSABOTAGE
- T_TRACKING
- T_WEATHERFORECAST

## Fehlende T_-Effekte (Kampf-relevant, heuristisch)
- T_CHAINBARDINGARMOR
- T_ENABLEMILITIA
- T_LEATHERBARINGARMOR
- T_PADDEDBARDINGARMOR
- T_PLATEBARDINGARMOR
- T_UPGRADEBOW1
- T_UPGRADEBOW2
- T_UPGRADEBOW3
- T_UPGRADEHEAVYCAVALRY1
- T_UPGRADELIGHTCAVALRY1
- T_UPGRADERIFLE1
- T_UPGRADESPEAR1
- T_UPGRADESPEAR2
- T_UPGRADESPEAR3
- T_UPGRADESWORD1
- T_UPGRADESWORD2
- T_UPGRADESWORD3

## Hinweis
- Technologie-XMLs enthalten in der Regel keine konkreten Effektwerte; viele Effekte sind hardcoded im Spiel.
- Diese Analyse basiert auf den in environment.py dokumentierten Zuordnungen (Kommentare).
- Falls du eine andere Mapping-Quelle hast (z.B. C++/Lua), kann ich den Abgleich verfeinern.