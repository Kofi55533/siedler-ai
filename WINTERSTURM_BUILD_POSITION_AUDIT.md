# Wintersturm Build Position Audit

Diese Tabelle zeigt, wie viele konkrete Baupositionen der Agent pro baubarem Gebaeudetyp aktuell waehlen kann.

## Summary

| field | value | note |
| --- | --- | --- |
| buildable_building_types | 40 | alle `target_specific`-Eintraege fuer Neubau |
| currently_buildable_types | 17 | nach Wintersturm-Regeln und Positionslogik |
| position_cap_per_building | 2200 | 44 * 50 |
| buildings_hitting_cap | 11 | wenn > 0, dann ist der Positionsraum fuer diese Typen abgeschnitten |
| full_map_search | ja | normale Gebaeude kommen aus `find_valid_building_positions(...)` ueber ganz P1 |

## Position Counts

| build_idx | building | class | buildable_now | candidate_count | hits_cap | sample_positions |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | Hauptquartier_1 | Kartenposition | nein | 0 | nein | - |
| 1 | Dorfzentrum_1 | Dorfzentrum-Slot | ja | 2 | nein | (34500, 23700); (43500, 9400) |
| 2 | Wohnhaus_1 | Kartenposition | ja | 376 | nein | (40100, 22900); (41088, 24266); (39914, 23480) |
| 3 | Bauernhof_1 | Kartenposition | ja | 149 | nein | (40100, 22900); (41088, 24266); (39327, 23087) |
| 4 | Hochschule_1 | Kartenposition | ja | 21 | nein | (38545, 21810); (44904, 21810); (42360, 19255) |
| 5 | Steinmine_1 | Mine-Slot | ja | 1 | nein | (42800, 15100) |
| 6 | Lehmmine_1 | Mine-Slot | ja | 1 | nein | (31125, 18750) |
| 7 | Eisenmine_1 | Mine-Slot | ja | 2 | nein | (34325, 7950); (36325, 6750) |
| 8 | Schwefelmine_1 | Mine-Slot | ja | 2 | nein | (48125, 20950); (47725, 18550) |
| 9 | SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle_1 | Kartenposition | nein | 0 | nein | - |
| 10 | LehmhÃƒÆ’Ã‚Â¼tte_1 | Kartenposition | nein | 0 | nein | - |
| 11 | Schmiede_1 | Kartenposition | nein | 0 | nein | - |
| 12 | AlchimistenhÃƒÆ’Ã‚Â¼tte_1 | Kartenposition | nein | 0 | nein | - |
| 13 | SteinmetzhÃƒÆ’Ã‚Â¼tte_1 | Kartenposition | nein | 0 | nein | - |
| 14 | Bank_1 | Kartenposition | nein | 0 | nein | - |
| 15 | Kloster_1 | Kartenposition | nein | 0 | nein | - |
| 16 | Markt_1 | Kartenposition | nein | 0 | nein | - |
| 17 | Kaserne_1 | Kartenposition | nein | 0 | nein | - |
| 18 | SchieÃƒÆ’Ã…Â¸platz_1 | Kartenposition | nein | 0 | nein | - |
| 19 | Stall_1 | Kartenposition | nein | 0 | nein | - |
| 20 | KanongieÃƒÆ’Ã…Â¸erei_1 | Kartenposition | nein | 0 | nein | - |
| 21 | Turm_1 | Kartenposition | nein | 0 | nein | - |
| 22 | Wetterturm | Kartenposition | nein | 0 | nein | - |
| 23 | Wetterkraftwerk | Kartenposition | nein | 0 | nein | - |
| 24 | Taverne_1 | Kartenposition | nein | 0 | nein | - |
| 25 | BÃƒÆ’Ã‚Â¼chsenmacherei_1 | Kartenposition | nein | 0 | nein | - |
| 26 | Architektenstube | Kartenposition | nein | 0 | nein | - |
| 27 | BrÃƒÆ’Ã‚Â¼cke | Kartenposition | nein | 0 | nein | - |
| 28 | PB_Beautification01 | Kartenposition | ja | 2200 | ja | (40100, 22900); (40100, 23300); (40900, 22100) |
| 29 | PB_Beautification02 | Kartenposition | ja | 811 | nein | (40100, 22900); (40100, 23300); (41088, 23971) |
| 30 | PB_Beautification03 | Kartenposition | ja | 2200 | ja | (40100, 22900); (40100, 23300); (40900, 22100) |
| 31 | PB_Beautification04 | Kartenposition | ja | 2200 | ja | (40100, 22900); (40100, 23300); (40900, 22100) |
| 32 | PB_Beautification05 | Kartenposition | ja | 2200 | ja | (40100, 22900); (40100, 23300); (40900, 22100) |
| 33 | PB_Beautification06 | Kartenposition | nein | 0 | ja | - |
| 34 | PB_Beautification07 | Kartenposition | ja | 2200 | ja | (40100, 22900); (40100, 23300); (40900, 22100) |
| 35 | PB_Beautification08 | Kartenposition | ja | 2200 | ja | (40100, 22900); (40100, 23300); (40900, 22100) |
| 36 | PB_Beautification09 | Kartenposition | ja | 2200 | ja | (40100, 22900); (40100, 23300); (40900, 22100) |
| 37 | PB_Beautification10 | Kartenposition | nein | 0 | ja | - |
| 38 | PB_Beautification11 | Kartenposition | ja | 2200 | ja | (40100, 22900); (40100, 23300); (40900, 22100) |
| 39 | PB_Beautification12 | Kartenposition | nein | 0 | ja | - |
