# Wintersturm Specific Index Table

Diese Tabelle zeigt die aktuelle, tatsaechlich maskierte Bedeutung von `source_specific` und `target_specific` auf Wintersturm.

## Summary

| field | value | note |
| --- | --- | --- |
| source_specific_size | 202 | gepolsterter Head; Masken schalten pro Kategorie frei |
| target_specific_size | 202 | Head-Groesse fuer exakte Holz-Baeume und Neubau-Ziele |
| currently_masked_neubau_types | 17 | auf Wintersturm im Reset wirklich waehlbar |
| wood_tree_count | 202 | Holz ist jetzt einzelbaum-genau maskiert |
| wood_zone_count | 11 | nach Split grosser Holzgebiete |
| position_group_count | 44 | 44 Gruppen |
| position_index_size | 50 | 50 Indizes je Gruppe |
| max_position_slots | 2200 | harte Obergrenze pro Gebaeudetyp |

## Source Specific

| source_category | category_name | specific_index | entry | coords | note |
| --- | --- | --- | --- | --- | --- |
| 0 | Frei | 0 | FREE | - | Specific wird uebersprungen; 0 ist Fallback |
| 1 | Holz | 0 | TREE_0 | 41780, 21532 | zone=HQ_Bereich; einzelner Baum |
| 1 | Holz | 1 | TREE_1 | 42920, 23420 | zone=HQ_Bereich; einzelner Baum |
| 1 | Holz | 2 | TREE_2 | 41169, 21057 | zone=HQ_Bereich; einzelner Baum |
| 1 | Holz | 3 | TREE_3 | 43470, 23820 | zone=HQ_Bereich; einzelner Baum |
| 1 | Holz | 4 | TREE_4 | 41380, 20561 | zone=HQ_Bereich; einzelner Baum |
| 1 | Holz | 5 | TREE_5 | 43520, 24178 | zone=HQ_Bereich; einzelner Baum |
| 1 | Holz | 6 | TREE_6 | 41820, 20546 | zone=HQ_Bereich; einzelner Baum |
| 1 | Holz | 7 | TREE_7 | 40873, 20042 | zone=HQ_Bereich; einzelner Baum |
| 1 | Holz | 8 | TREE_8 | 43220, 21657 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 9 | TREE_9 | 42780, 21380 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 10 | TREE_10 | 42776, 20721 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 11 | TREE_11 | 45580, 19980 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 12 | TREE_12 | 46280, 22046 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 13 | TREE_13 | 44880, 23534 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 14 | TREE_14 | 44680, 23624 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 15 | TREE_15 | 45720, 23333 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 16 | TREE_16 | 44979, 24146 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 17 | TREE_17 | 43926, 24351 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 18 | TREE_18 | 44520, 18478 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 19 | TREE_19 | 44180, 18341 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 20 | TREE_20 | 45466, 24433 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 21 | TREE_21 | 44540, 18230 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 22 | TREE_22 | 45739, 24842 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 23 | TREE_23 | 48080, 22120 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 24 | TREE_24 | 47977, 23377 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 25 | TREE_25 | 49424, 21380 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 26 | TREE_26 | 49379, 22320 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 27 | TREE_27 | 49638, 20632 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 28 | TREE_28 | 49543, 23327 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 29 | TREE_29 | 50120, 22344 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 30 | TREE_30 | 49580, 24220 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 31 | TREE_31 | 49441, 18080 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 32 | TREE_32 | 50020, 23920 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 33 | TREE_33 | 49520, 24980 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 34 | TREE_34 | 50643, 20848 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 35 | TREE_35 | 48220, 16380 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 36 | TREE_36 | 49151, 17180 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 37 | TREE_37 | 50580, 24720 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 38 | TREE_38 | 48323, 15554 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 39 | TREE_39 | 35820, 19820 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 40 | TREE_40 | 35657, 18879 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 41 | TREE_41 | 35920, 18880 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 42 | TREE_42 | 35020, 20634 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 43 | TREE_43 | 33939, 19844 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 44 | TREE_44 | 35238, 20961 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 45 | TREE_45 | 35264, 21160 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 46 | TREE_46 | 35480, 17861 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 47 | TREE_47 | 33957, 17580 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 48 | TREE_48 | 35359, 22320 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 49 | TREE_49 | 32580, 16620 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 50 | TREE_50 | 32641, 15355 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 51 | TREE_51 | 31574, 24475 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 52 | TREE_52 | 28820, 20368 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 53 | TREE_53 | 28420, 18080 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 54 | TREE_54 | 28580, 22020 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 55 | TREE_55 | 28456, 15545 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 56 | TREE_56 | 27328, 19456 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 57 | TREE_57 | 27074, 18420 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 58 | TREE_58 | 26468, 18773 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 59 | TREE_59 | 26562, 21739 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 60 | TREE_60 | 26660, 22676 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 61 | TREE_61 | 26780, 15959 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 62 | TREE_62 | 26748, 15673 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 63 | TREE_63 | 27380, 14520 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 64 | TREE_64 | 25920, 20854 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 65 | TREE_65 | 25380, 20854 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 66 | TREE_66 | 25734, 13722 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 67 | TREE_67 | 25566, 13722 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 68 | TREE_68 | 39653, 15533 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 69 | TREE_69 | 40520, 14127 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 70 | TREE_70 | 40262, 15977 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 71 | TREE_71 | 40720, 15880 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 72 | TREE_72 | 41256, 15558 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 73 | TREE_73 | 40666, 13220 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 74 | TREE_74 | 41720, 13867 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 75 | TREE_75 | 38620, 13272 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 76 | TREE_76 | 41978, 13267 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 77 | TREE_77 | 41380, 12540 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 78 | TREE_78 | 41337, 17320 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 79 | TREE_79 | 41779, 17120 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 80 | TREE_80 | 43459, 16843 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 81 | TREE_81 | 40920, 11057 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 82 | TREE_82 | 43622, 16726 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 83 | TREE_83 | 44820, 15738 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 84 | TREE_84 | 43680, 11280 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 85 | TREE_85 | 45220, 15365 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 86 | TREE_86 | 44431, 10280 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 87 | TREE_87 | 45565, 11458 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 88 | TREE_88 | 45561, 11180 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 89 | TREE_89 | 44657, 9820 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 90 | TREE_90 | 47441, 14471 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 91 | TREE_91 | 37920, 25156 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 92 | TREE_92 | 37663, 24652 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 93 | TREE_93 | 37920, 25340 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 94 | TREE_94 | 37531, 24776 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 95 | TREE_95 | 37463, 23420 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 96 | TREE_96 | 37320, 23380 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 97 | TREE_97 | 37680, 22340 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 98 | TREE_98 | 37551, 22456 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 99 | TREE_99 | 37430, 22549 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 100 | TREE_100 | 37420, 22476 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 101 | TREE_101 | 37380, 22159 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 102 | TREE_102 | 35820, 23780 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 103 | TREE_103 | 36659, 8420 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 104 | TREE_104 | 35580, 9278 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 105 | TREE_105 | 37058, 8527 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 106 | TREE_106 | 38346, 9233 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 107 | TREE_107 | 37530, 10767 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 108 | TREE_108 | 37420, 11070 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 109 | TREE_109 | 35742, 11320 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 110 | TREE_110 | 37575, 11025 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 111 | TREE_111 | 35750, 11380 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 112 | TREE_112 | 34220, 10372 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 113 | TREE_113 | 37354, 11247 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 114 | TREE_114 | 37868, 6638 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 115 | TREE_115 | 38642, 7380 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 116 | TREE_116 | 38880, 7820 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 117 | TREE_117 | 38744, 10372 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 118 | TREE_118 | 38347, 11336 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 119 | TREE_119 | 38240, 6420 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 120 | TREE_120 | 34120, 11320 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 121 | TREE_121 | 33322, 10320 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 122 | TREE_122 | 39172, 7048 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 123 | TREE_123 | 32780, 8563 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 124 | TREE_124 | 33745, 11380 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 125 | TREE_125 | 38473, 6120 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 126 | TREE_126 | 38149, 5820 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 127 | TREE_127 | 38627, 5931 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 128 | TREE_128 | 38680, 5961 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 129 | TREE_129 | 38620, 5748 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 130 | TREE_130 | 38740, 5620 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 131 | TREE_131 | 40324, 7541 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 132 | TREE_132 | 40520, 9522 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 133 | TREE_133 | 38748, 5380 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 134 | TREE_134 | 39844, 6234 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 135 | TREE_135 | 31880, 9858 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 136 | TREE_136 | 40322, 6680 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 137 | TREE_137 | 39470, 5560 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 138 | TREE_138 | 40964, 8521 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 139 | TREE_139 | 34655, 4420 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 140 | TREE_140 | 39620, 5420 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 141 | TREE_141 | 32875, 5280 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 142 | TREE_142 | 36439, 3851 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 143 | TREE_143 | 32320, 5670 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 144 | TREE_144 | 34066, 4180 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 145 | TREE_145 | 31955, 5962 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 146 | TREE_146 | 41420, 7827 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 147 | TREE_147 | 33967, 4120 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 148 | TREE_148 | 33226, 4320 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 149 | TREE_149 | 35080, 3320 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 150 | TREE_150 | 34947, 3220 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 151 | TREE_151 | 41958, 7380 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 152 | TREE_152 | 30820, 11353 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 153 | TREE_153 | 34431, 3225 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 154 | TREE_154 | 30820, 11543 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 155 | TREE_155 | 30641, 11520 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 156 | TREE_156 | 35574, 2742 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 157 | TREE_157 | 31820, 4580 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 158 | TREE_158 | 31637, 4646 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 159 | TREE_159 | 31646, 4520 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 160 | TREE_160 | 29680, 8464 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 161 | TREE_161 | 29742, 7580 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 162 | TREE_162 | 29551, 9180 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 163 | TREE_163 | 29461, 8165 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 164 | TREE_164 | 32673, 3064 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 165 | TREE_165 | 33580, 2422 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 166 | TREE_166 | 32577, 2820 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 167 | TREE_167 | 32934, 2565 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 168 | TREE_168 | 29042, 9138 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 169 | TREE_169 | 32733, 2580 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 170 | TREE_170 | 31966, 2723 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 171 | TREE_171 | 28874, 7032 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 172 | TREE_172 | 30564, 3534 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 173 | TREE_173 | 29042, 5120 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 174 | TREE_174 | 30080, 3420 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 175 | TREE_175 | 30151, 3321 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 176 | TREE_176 | 28228, 11065 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 177 | TREE_177 | 28727, 4552 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 178 | TREE_178 | 31257, 1756 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 179 | TREE_179 | 28465, 4880 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 180 | TREE_180 | 28720, 4380 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 181 | TREE_181 | 28665, 4453 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 182 | TREE_182 | 28469, 4780 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 183 | TREE_183 | 28329, 4880 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 184 | TREE_184 | 27720, 11480 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 185 | TREE_185 | 30770, 1820 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 186 | TREE_186 | 27261, 9764 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 187 | TREE_187 | 27032, 8680 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 188 | TREE_188 | 27980, 4720 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 189 | TREE_189 | 28046, 13421 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 190 | TREE_190 | 27930, 4549 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 191 | TREE_191 | 30080, 1820 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 192 | TREE_192 | 27234, 11631 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 193 | TREE_193 | 26820, 10544 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 194 | TREE_194 | 30053, 1380 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 195 | TREE_195 | 29669, 1625 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 196 | TREE_196 | 29720, 1464 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 197 | TREE_197 | 27225, 4338 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 198 | TREE_198 | 29520, 1320 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 199 | TREE_199 | 26573, 12536 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 200 | TREE_200 | 25820, 5543 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 201 | TREE_201 | 25480, 5543 | zone=Eisenmine_3; einzelner Baum |
| 2 | Eisen | 0 | SHAFT_IRON_1 | 36275.84, 8927.04 | Stollen; Sammelpunkt |
| 2 | Eisen | 1 | SHAFT_IRON_2 | 37495.02, 7801.38 | Stollen; Sammelpunkt |
| 2 | Eisen | 2 | SHAFT_IRON_3 | 37784.37, 7265.83 | Stollen; Sammelpunkt |
| 2 | Eisen | 3 | DEPOSIT_IRON_1 | 34325.00, 7950.00 | Vorkommen; Mine-Bauplatz + Sammelpunkt bis Mine steht |
| 2 | Eisen | 4 | DEPOSIT_IRON_2 | 36325.00, 6750.00 | Vorkommen; Mine-Bauplatz + Sammelpunkt bis Mine steht |
| 3 | Stein | 0 | SHAFT_STONE_1 | 40056.03, 14890.56 | Stollen; Sammelpunkt |
| 3 | Stein | 1 | SHAFT_STONE_2 | 39320.85, 14715.73 | Stollen; Sammelpunkt |
| 3 | Stein | 2 | SHAFT_STONE_3 | 38633.13, 14720.38 | Stollen; Sammelpunkt |
| 3 | Stein | 3 | DEPOSIT_STONE_1 | 42800.00, 15100.00 | Vorkommen; Mine-Bauplatz + Sammelpunkt bis Mine steht |
| 3 | Stein | 4 | DEPOSIT_STONE_2 | - | Vorkommen; unbenutzt auf Wintersturm |
| 4 | Lehm | 0 | SHAFT_CLAY_1 | 35180.72, 19552.98 | Stollen; Sammelpunkt |
| 4 | Lehm | 1 | SHAFT_CLAY_2 | 35106.41, 18871.68 | Stollen; Sammelpunkt |
| 4 | Lehm | 2 | SHAFT_CLAY_3 | 34991.41, 17996.99 | Stollen; Sammelpunkt |
| 4 | Lehm | 3 | DEPOSIT_CLAY_1 | 31125.00, 18750.00 | Vorkommen; Mine-Bauplatz + Sammelpunkt bis Mine steht |
| 5 | Schwefel | 0 | SHAFT_SULFUR_1 | 44304.14, 21484.33 | Stollen; Sammelpunkt |
| 5 | Schwefel | 1 | SHAFT_SULFUR_2 | 44005.73, 20978.49 | Stollen; Sammelpunkt |
| 5 | Schwefel | 2 | SHAFT_SULFUR_3 | 44576.42, 22119.58 | Stollen; Sammelpunkt |
| 5 | Schwefel | 3 | DEPOSIT_SULFUR_1 | 48125.00, 20950.00 | Vorkommen; Mine-Bauplatz + Sammelpunkt bis Mine steht |
| 5 | Schwefel | 4 | DEPOSIT_SULFUR_2 | 47725.00, 18550.00 | Vorkommen; Mine-Bauplatz + Sammelpunkt bis Mine steht |
| 6 | Baustelle | 0..N-1 | construction_sites[i] | - | dynamisch zur Laufzeit |

## Target Specific

| target_category | category_name | specific_index | entry | coords | note |
| --- | --- | --- | --- | --- | --- |
| 0 | Frei (deaktiviert) | 0 | FREE | - | Specific wird uebersprungen; 0 ist Fallback |
| 1 | Holz | 0 | TREE_0 | 41780, 21532 | zone=HQ_Bereich; einzelner Baum |
| 1 | Holz | 1 | TREE_1 | 42920, 23420 | zone=HQ_Bereich; einzelner Baum |
| 1 | Holz | 2 | TREE_2 | 41169, 21057 | zone=HQ_Bereich; einzelner Baum |
| 1 | Holz | 3 | TREE_3 | 43470, 23820 | zone=HQ_Bereich; einzelner Baum |
| 1 | Holz | 4 | TREE_4 | 41380, 20561 | zone=HQ_Bereich; einzelner Baum |
| 1 | Holz | 5 | TREE_5 | 43520, 24178 | zone=HQ_Bereich; einzelner Baum |
| 1 | Holz | 6 | TREE_6 | 41820, 20546 | zone=HQ_Bereich; einzelner Baum |
| 1 | Holz | 7 | TREE_7 | 40873, 20042 | zone=HQ_Bereich; einzelner Baum |
| 1 | Holz | 8 | TREE_8 | 43220, 21657 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 9 | TREE_9 | 42780, 21380 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 10 | TREE_10 | 42776, 20721 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 11 | TREE_11 | 45580, 19980 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 12 | TREE_12 | 46280, 22046 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 13 | TREE_13 | 44880, 23534 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 14 | TREE_14 | 44680, 23624 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 15 | TREE_15 | 45720, 23333 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 16 | TREE_16 | 44979, 24146 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 17 | TREE_17 | 43926, 24351 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 18 | TREE_18 | 44520, 18478 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 19 | TREE_19 | 44180, 18341 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 20 | TREE_20 | 45466, 24433 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 21 | TREE_21 | 44540, 18230 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 22 | TREE_22 | 45739, 24842 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 23 | TREE_23 | 48080, 22120 | zone=Schwefelmine_1; einzelner Baum |
| 1 | Holz | 24 | TREE_24 | 47977, 23377 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 25 | TREE_25 | 49424, 21380 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 26 | TREE_26 | 49379, 22320 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 27 | TREE_27 | 49638, 20632 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 28 | TREE_28 | 49543, 23327 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 29 | TREE_29 | 50120, 22344 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 30 | TREE_30 | 49580, 24220 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 31 | TREE_31 | 49441, 18080 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 32 | TREE_32 | 50020, 23920 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 33 | TREE_33 | 49520, 24980 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 34 | TREE_34 | 50643, 20848 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 35 | TREE_35 | 48220, 16380 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 36 | TREE_36 | 49151, 17180 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 37 | TREE_37 | 50580, 24720 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 38 | TREE_38 | 48323, 15554 | zone=Schwefelmine_2; einzelner Baum |
| 1 | Holz | 39 | TREE_39 | 35820, 19820 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 40 | TREE_40 | 35657, 18879 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 41 | TREE_41 | 35920, 18880 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 42 | TREE_42 | 35020, 20634 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 43 | TREE_43 | 33939, 19844 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 44 | TREE_44 | 35238, 20961 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 45 | TREE_45 | 35264, 21160 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 46 | TREE_46 | 35480, 17861 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 47 | TREE_47 | 33957, 17580 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 48 | TREE_48 | 35359, 22320 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 49 | TREE_49 | 32580, 16620 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 50 | TREE_50 | 32641, 15355 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 51 | TREE_51 | 31574, 24475 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 52 | TREE_52 | 28820, 20368 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 53 | TREE_53 | 28420, 18080 | zone=Lehmmine_1; einzelner Baum |
| 1 | Holz | 54 | TREE_54 | 28580, 22020 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 55 | TREE_55 | 28456, 15545 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 56 | TREE_56 | 27328, 19456 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 57 | TREE_57 | 27074, 18420 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 58 | TREE_58 | 26468, 18773 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 59 | TREE_59 | 26562, 21739 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 60 | TREE_60 | 26660, 22676 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 61 | TREE_61 | 26780, 15959 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 62 | TREE_62 | 26748, 15673 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 63 | TREE_63 | 27380, 14520 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 64 | TREE_64 | 25920, 20854 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 65 | TREE_65 | 25380, 20854 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 66 | TREE_66 | 25734, 13722 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 67 | TREE_67 | 25566, 13722 | zone=Lehmmine_2; einzelner Baum |
| 1 | Holz | 68 | TREE_68 | 39653, 15533 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 69 | TREE_69 | 40520, 14127 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 70 | TREE_70 | 40262, 15977 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 71 | TREE_71 | 40720, 15880 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 72 | TREE_72 | 41256, 15558 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 73 | TREE_73 | 40666, 13220 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 74 | TREE_74 | 41720, 13867 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 75 | TREE_75 | 38620, 13272 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 76 | TREE_76 | 41978, 13267 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 77 | TREE_77 | 41380, 12540 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 78 | TREE_78 | 41337, 17320 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 79 | TREE_79 | 41779, 17120 | zone=Steinmine_1; einzelner Baum |
| 1 | Holz | 80 | TREE_80 | 43459, 16843 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 81 | TREE_81 | 40920, 11057 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 82 | TREE_82 | 43622, 16726 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 83 | TREE_83 | 44820, 15738 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 84 | TREE_84 | 43680, 11280 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 85 | TREE_85 | 45220, 15365 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 86 | TREE_86 | 44431, 10280 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 87 | TREE_87 | 45565, 11458 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 88 | TREE_88 | 45561, 11180 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 89 | TREE_89 | 44657, 9820 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 90 | TREE_90 | 47441, 14471 | zone=Steinmine_2; einzelner Baum |
| 1 | Holz | 91 | TREE_91 | 37920, 25156 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 92 | TREE_92 | 37663, 24652 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 93 | TREE_93 | 37920, 25340 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 94 | TREE_94 | 37531, 24776 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 95 | TREE_95 | 37463, 23420 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 96 | TREE_96 | 37320, 23380 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 97 | TREE_97 | 37680, 22340 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 98 | TREE_98 | 37551, 22456 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 99 | TREE_99 | 37430, 22549 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 100 | TREE_100 | 37420, 22476 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 101 | TREE_101 | 37380, 22159 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 102 | TREE_102 | 35820, 23780 | zone=Dorfzentrum; einzelner Baum |
| 1 | Holz | 103 | TREE_103 | 36659, 8420 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 104 | TREE_104 | 35580, 9278 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 105 | TREE_105 | 37058, 8527 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 106 | TREE_106 | 38346, 9233 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 107 | TREE_107 | 37530, 10767 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 108 | TREE_108 | 37420, 11070 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 109 | TREE_109 | 35742, 11320 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 110 | TREE_110 | 37575, 11025 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 111 | TREE_111 | 35750, 11380 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 112 | TREE_112 | 34220, 10372 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 113 | TREE_113 | 37354, 11247 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 114 | TREE_114 | 37868, 6638 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 115 | TREE_115 | 38642, 7380 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 116 | TREE_116 | 38880, 7820 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 117 | TREE_117 | 38744, 10372 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 118 | TREE_118 | 38347, 11336 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 119 | TREE_119 | 38240, 6420 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 120 | TREE_120 | 34120, 11320 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 121 | TREE_121 | 33322, 10320 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 122 | TREE_122 | 39172, 7048 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 123 | TREE_123 | 32780, 8563 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 124 | TREE_124 | 33745, 11380 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 125 | TREE_125 | 38473, 6120 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 126 | TREE_126 | 38149, 5820 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 127 | TREE_127 | 38627, 5931 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 128 | TREE_128 | 38680, 5961 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 129 | TREE_129 | 38620, 5748 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 130 | TREE_130 | 38740, 5620 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 131 | TREE_131 | 40324, 7541 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 132 | TREE_132 | 40520, 9522 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 133 | TREE_133 | 38748, 5380 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 134 | TREE_134 | 39844, 6234 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 135 | TREE_135 | 31880, 9858 | zone=Eisenmine_1; einzelner Baum |
| 1 | Holz | 136 | TREE_136 | 40322, 6680 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 137 | TREE_137 | 39470, 5560 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 138 | TREE_138 | 40964, 8521 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 139 | TREE_139 | 34655, 4420 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 140 | TREE_140 | 39620, 5420 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 141 | TREE_141 | 32875, 5280 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 142 | TREE_142 | 36439, 3851 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 143 | TREE_143 | 32320, 5670 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 144 | TREE_144 | 34066, 4180 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 145 | TREE_145 | 31955, 5962 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 146 | TREE_146 | 41420, 7827 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 147 | TREE_147 | 33967, 4120 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 148 | TREE_148 | 33226, 4320 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 149 | TREE_149 | 35080, 3320 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 150 | TREE_150 | 34947, 3220 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 151 | TREE_151 | 41958, 7380 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 152 | TREE_152 | 30820, 11353 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 153 | TREE_153 | 34431, 3225 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 154 | TREE_154 | 30820, 11543 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 155 | TREE_155 | 30641, 11520 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 156 | TREE_156 | 35574, 2742 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 157 | TREE_157 | 31820, 4580 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 158 | TREE_158 | 31637, 4646 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 159 | TREE_159 | 31646, 4520 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 160 | TREE_160 | 29680, 8464 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 161 | TREE_161 | 29742, 7580 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 162 | TREE_162 | 29551, 9180 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 163 | TREE_163 | 29461, 8165 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 164 | TREE_164 | 32673, 3064 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 165 | TREE_165 | 33580, 2422 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 166 | TREE_166 | 32577, 2820 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 167 | TREE_167 | 32934, 2565 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 168 | TREE_168 | 29042, 9138 | zone=Eisenmine_2; einzelner Baum |
| 1 | Holz | 169 | TREE_169 | 32733, 2580 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 170 | TREE_170 | 31966, 2723 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 171 | TREE_171 | 28874, 7032 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 172 | TREE_172 | 30564, 3534 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 173 | TREE_173 | 29042, 5120 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 174 | TREE_174 | 30080, 3420 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 175 | TREE_175 | 30151, 3321 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 176 | TREE_176 | 28228, 11065 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 177 | TREE_177 | 28727, 4552 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 178 | TREE_178 | 31257, 1756 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 179 | TREE_179 | 28465, 4880 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 180 | TREE_180 | 28720, 4380 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 181 | TREE_181 | 28665, 4453 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 182 | TREE_182 | 28469, 4780 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 183 | TREE_183 | 28329, 4880 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 184 | TREE_184 | 27720, 11480 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 185 | TREE_185 | 30770, 1820 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 186 | TREE_186 | 27261, 9764 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 187 | TREE_187 | 27032, 8680 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 188 | TREE_188 | 27980, 4720 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 189 | TREE_189 | 28046, 13421 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 190 | TREE_190 | 27930, 4549 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 191 | TREE_191 | 30080, 1820 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 192 | TREE_192 | 27234, 11631 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 193 | TREE_193 | 26820, 10544 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 194 | TREE_194 | 30053, 1380 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 195 | TREE_195 | 29669, 1625 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 196 | TREE_196 | 29720, 1464 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 197 | TREE_197 | 27225, 4338 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 198 | TREE_198 | 29520, 1320 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 199 | TREE_199 | 26573, 12536 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 200 | TREE_200 | 25820, 5543 | zone=Eisenmine_3; einzelner Baum |
| 1 | Holz | 201 | TREE_201 | 25480, 5543 | zone=Eisenmine_3; einzelner Baum |
| 2 | Eisen | 0 | SHAFT_IRON_1 | 36275.84, 8927.04 | Stollen; Sammelpunkt |
| 2 | Eisen | 1 | SHAFT_IRON_2 | 37495.02, 7801.38 | Stollen; Sammelpunkt |
| 2 | Eisen | 2 | SHAFT_IRON_3 | 37784.37, 7265.83 | Stollen; Sammelpunkt |
| 2 | Eisen | 3 | DEPOSIT_IRON_1 | 34325.00, 7950.00 | Vorkommen; Mine-Bauplatz + Sammelpunkt bis Mine steht |
| 2 | Eisen | 4 | DEPOSIT_IRON_2 | 36325.00, 6750.00 | Vorkommen; Mine-Bauplatz + Sammelpunkt bis Mine steht |
| 3 | Stein | 0 | SHAFT_STONE_1 | 40056.03, 14890.56 | Stollen; Sammelpunkt |
| 3 | Stein | 1 | SHAFT_STONE_2 | 39320.85, 14715.73 | Stollen; Sammelpunkt |
| 3 | Stein | 2 | SHAFT_STONE_3 | 38633.13, 14720.38 | Stollen; Sammelpunkt |
| 3 | Stein | 3 | DEPOSIT_STONE_1 | 42800.00, 15100.00 | Vorkommen; Mine-Bauplatz + Sammelpunkt bis Mine steht |
| 3 | Stein | 4 | DEPOSIT_STONE_2 | - | Vorkommen; unbenutzt auf Wintersturm |
| 4 | Lehm | 0 | SHAFT_CLAY_1 | 35180.72, 19552.98 | Stollen; Sammelpunkt |
| 4 | Lehm | 1 | SHAFT_CLAY_2 | 35106.41, 18871.68 | Stollen; Sammelpunkt |
| 4 | Lehm | 2 | SHAFT_CLAY_3 | 34991.41, 17996.99 | Stollen; Sammelpunkt |
| 4 | Lehm | 3 | DEPOSIT_CLAY_1 | 31125.00, 18750.00 | Vorkommen; Mine-Bauplatz + Sammelpunkt bis Mine steht |
| 5 | Schwefel | 0 | SHAFT_SULFUR_1 | 44304.14, 21484.33 | Stollen; Sammelpunkt |
| 5 | Schwefel | 1 | SHAFT_SULFUR_2 | 44005.73, 20978.49 | Stollen; Sammelpunkt |
| 5 | Schwefel | 2 | SHAFT_SULFUR_3 | 44576.42, 22119.58 | Stollen; Sammelpunkt |
| 5 | Schwefel | 3 | DEPOSIT_SULFUR_1 | 48125.00, 20950.00 | Vorkommen; Mine-Bauplatz + Sammelpunkt bis Mine steht |
| 5 | Schwefel | 4 | DEPOSIT_SULFUR_2 | 47725.00, 18550.00 | Vorkommen; Mine-Bauplatz + Sammelpunkt bis Mine steht |
| 6 | Baustelle | 0..N-1 | construction_sites[i] | - | dynamisch zur Laufzeit |
| 7 | Neubau | 0 | Hauptquartier_1 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 1 | Dorfzentrum_1 | - | 2 Baupositionen; maskiert=ja |
| 7 | Neubau | 2 | Wohnhaus_1 | - | 376 Baupositionen; maskiert=ja |
| 7 | Neubau | 3 | Bauernhof_1 | - | 149 Baupositionen; maskiert=ja |
| 7 | Neubau | 4 | Hochschule_1 | - | 21 Baupositionen; maskiert=ja |
| 7 | Neubau | 5 | Steinmine_1 | - | 1 Baupositionen; maskiert=ja |
| 7 | Neubau | 6 | Lehmmine_1 | - | 1 Baupositionen; maskiert=ja |
| 7 | Neubau | 7 | Eisenmine_1 | - | 2 Baupositionen; maskiert=ja |
| 7 | Neubau | 8 | Schwefelmine_1 | - | 2 Baupositionen; maskiert=ja |
| 7 | Neubau | 9 | SÃƒÆ’Ã‚Â¤gemÃƒÆ’Ã‚Â¼hle_1 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 10 | LehmhÃƒÆ’Ã‚Â¼tte_1 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 11 | Schmiede_1 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 12 | AlchimistenhÃƒÆ’Ã‚Â¼tte_1 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 13 | SteinmetzhÃƒÆ’Ã‚Â¼tte_1 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 14 | Bank_1 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 15 | Kloster_1 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 16 | Markt_1 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 17 | Kaserne_1 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 18 | SchieÃƒÆ’Ã…Â¸platz_1 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 19 | Stall_1 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 20 | KanongieÃƒÆ’Ã…Â¸erei_1 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 21 | Turm_1 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 22 | Wetterturm | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 23 | Wetterkraftwerk | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 24 | Taverne_1 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 25 | BÃƒÆ’Ã‚Â¼chsenmacherei_1 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 26 | Architektenstube | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 27 | BrÃƒÆ’Ã‚Â¼cke | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 28 | PB_Beautification01 | - | 2200 Baupositionen; maskiert=ja |
| 7 | Neubau | 29 | PB_Beautification02 | - | 811 Baupositionen; maskiert=ja |
| 7 | Neubau | 30 | PB_Beautification03 | - | 2200 Baupositionen; maskiert=ja |
| 7 | Neubau | 31 | PB_Beautification04 | - | 2200 Baupositionen; maskiert=ja |
| 7 | Neubau | 32 | PB_Beautification05 | - | 2200 Baupositionen; maskiert=ja |
| 7 | Neubau | 33 | PB_Beautification06 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 34 | PB_Beautification07 | - | 2200 Baupositionen; maskiert=ja |
| 7 | Neubau | 35 | PB_Beautification08 | - | 2200 Baupositionen; maskiert=ja |
| 7 | Neubau | 36 | PB_Beautification09 | - | 2200 Baupositionen; maskiert=ja |
| 7 | Neubau | 37 | PB_Beautification10 | - | 0 Baupositionen; maskiert=nein |
| 7 | Neubau | 38 | PB_Beautification11 | - | 2200 Baupositionen; maskiert=ja |
| 7 | Neubau | 39 | PB_Beautification12 | - | 0 Baupositionen; maskiert=nein |
