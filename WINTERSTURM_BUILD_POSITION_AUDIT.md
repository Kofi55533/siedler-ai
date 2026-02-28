# Wintersturm Build Position Audit

Diese Tabelle zeigt, wie viele konkrete Baupositionen der Agent pro baubarem Gebaeudetyp aktuell waehlen kann.

## Summary

| field | value | note |
| --- | --- | --- |
| buildable_building_types | 40 | alle `target_specific`-Eintraege fuer Neubau |
| currently_buildable_types | 17 | nach Wintersturm-Regeln und Positionslogik |
| position_cap_per_building | 2200 | 44 * 50 |
| buildings_hitting_cap | 0 | wenn > 0, dann ist der Positionsraum fuer diese Typen abgeschnitten |
| full_map_search | ja | normale Gebaeude kommen aus `find_valid_building_positions(...)` ueber ganz P1 |

## Position Counts

| build_idx | building | class | buildable_now | candidate_count | hits_cap | sample_positions |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | Hauptquartier_1 | Kartenposition | nein | 0 | nein | - |
| 1 | Dorfzentrum_1 | Dorfzentrum-Slot | ja | 2 | nein | (34500, 23700); (43500, 9400) |
| 2 | Wohnhaus_1 | Kartenposition | ja | 407 | nein | (41074, 24200); (41810, 24200); (40337, 24200) |
| 3 | Bauernhof_1 | Kartenposition | ja | 115 | nein | (41074, 24234); (42212, 24234); (40505, 21361) |
| 4 | Hochschule_1 | Kartenposition | ja | 8 | nein | (38529, 21800); (42346, 19232); (47434, 24369) |
| 5 | Steinmine_1 | Mine-Slot | ja | 1 | nein | (42800, 15100) |
| 6 | Lehmmine_1 | Mine-Slot | ja | 1 | nein | (31125, 18750) |
| 7 | Eisenmine_1 | Mine-Slot | ja | 2 | nein | (34325, 7950); (36325, 6750) |
| 8 | Schwefelmine_1 | Mine-Slot | ja | 2 | nein | (48125, 20950); (47725, 18550) |
| 9 | SÃƒÂ¤gemÃƒÂ¼hle_1 | Kartenposition | nein | 0 | nein | - |
| 10 | LehmhÃƒÂ¼tte_1 | Kartenposition | nein | 0 | nein | - |
| 11 | Schmiede_1 | Kartenposition | nein | 0 | nein | - |
| 12 | AlchimistenhÃƒÂ¼tte_1 | Kartenposition | nein | 0 | nein | - |
| 13 | SteinmetzhÃƒÂ¼tte_1 | Kartenposition | nein | 0 | nein | - |
| 14 | Bank_1 | Kartenposition | nein | 0 | nein | - |
| 15 | Kloster_1 | Kartenposition | nein | 0 | nein | - |
| 16 | Markt_1 | Kartenposition | nein | 0 | nein | - |
| 17 | Kaserne_1 | Kartenposition | nein | 0 | nein | - |
| 18 | SchieÃƒÅ¸platz_1 | Kartenposition | nein | 0 | nein | - |
| 19 | Stall_1 | Kartenposition | nein | 0 | nein | - |
| 20 | KanongieÃƒÅ¸erei_1 | Kartenposition | nein | 0 | nein | - |
| 21 | Turm_1 | Kartenposition | nein | 0 | nein | - |
| 22 | Wetterturm | Kartenposition | nein | 0 | nein | - |
| 23 | Wetterkraftwerk | Kartenposition | nein | 0 | nein | - |
| 24 | Taverne_1 | Kartenposition | nein | 0 | nein | - |
| 25 | BÃƒÂ¼chsenmacherei_1 | Kartenposition | nein | 0 | nein | - |
| 26 | Architektenstube | Kartenposition | nein | 0 | nein | - |
| 27 | BrÃƒÂ¼cke | Kartenposition | nein | 0 | nein | - |
| 28 | PB_Beautification01 | Kartenposition | ja | 897 | nein | (42100, 23300); (41074, 23896); (41877, 22814) |
| 29 | PB_Beautification02 | Kartenposition | ja | 251 | nein | (41074, 24031); (42011, 23558); (41074, 21665) |
| 30 | PB_Beautification03 | Kartenposition | ja | 897 | nein | (42100, 23300); (41074, 23896); (41877, 22814) |
| 31 | PB_Beautification04 | Kartenposition | ja | 897 | nein | (42100, 23300); (41074, 23896); (41877, 22814) |
| 32 | PB_Beautification05 | Kartenposition | ja | 897 | nein | (42100, 23300); (41074, 23896); (41877, 22814) |
| 33 | PB_Beautification06 | Kartenposition | nein | 0 | nein | - |
| 34 | PB_Beautification07 | Kartenposition | ja | 897 | nein | (42100, 23300); (41074, 23896); (41877, 22814) |
| 35 | PB_Beautification08 | Kartenposition | ja | 897 | nein | (42100, 23300); (41074, 23896); (41877, 22814) |
| 36 | PB_Beautification09 | Kartenposition | ja | 897 | nein | (42100, 23300); (41074, 23896); (41877, 22814) |
| 37 | PB_Beautification10 | Kartenposition | nein | 0 | nein | - |
| 38 | PB_Beautification11 | Kartenposition | ja | 897 | nein | (42100, 23300); (41074, 23896); (41877, 22814) |
| 39 | PB_Beautification12 | Kartenposition | nein | 0 | nein | - |
