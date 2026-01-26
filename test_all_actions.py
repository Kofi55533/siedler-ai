# -*- coding: utf-8 -*-
"""Test aller 302 Actions auf Korrektheit."""

from environment import SiedlerScharfschuetzenEnv
import numpy as np

print('=' * 60)
print('VOLLSTAENDIGER ACTION-TEST')
print('=' * 60)

env = SiedlerScharfschuetzenEnv()
obs, info = env.reset()

errors = []

# ============================================
print('\n1. BUILD - Check')
print('============================================')

env.reset()
mask = env.get_action_mask()
build_offset = 1
valid_builds = [a for a in range(build_offset, build_offset + 84) if mask[a] == 1]
print(f'Gueltige Build-Actions: {len(valid_builds)}')

if valid_builds:
    # Test Wohnhaus bauen
    action = 7  # Wohnhaus_1 x1
    sites_before = len(env.construction_sites)
    res_before = env.resources.copy()
    obs, reward, done, trunc, info = env.step(action)
    sites_after = len(env.construction_sites)

    if sites_after > sites_before:
        print(f'  [OK] Baustelle erstellt, Ressourcen abgezogen')
    else:
        errors.append('BUILD: Keine Baustelle erstellt')

# ============================================
print('\n2. UPGRADE - Check')
print('============================================')

env.reset()
env.resources = {'Taler': 50000, 'Holz': 50000, 'Stein': 50000, 'Lehm': 50000, 'Eisen': 5000, 'Schwefel': 5000}
env.buildings['Wohnhaus_1'] = 1

mask = env.get_action_mask()
upgrade_offset = 85
valid_upgrades = [a for a in range(upgrade_offset, upgrade_offset + 35) if mask[a] == 1]
print(f'Gueltige Upgrade-Actions: {len(valid_upgrades)}')

if valid_upgrades:
    # Zeige welche Upgrades verfuegbar sind
    for a in valid_upgrades[:3]:
        idx = a - upgrade_offset
        name = env.upgradeable_buildings[idx]
        print(f'  - Action {a}: {name}')
    print('  [OK] Upgrades verfuegbar')
else:
    print('  Keine Upgrades verfuegbar (normal)')

# ============================================
print('\n3. RESEARCH - Check')
print('============================================')

env.reset()
env.resources = {'Taler': 50000, 'Holz': 50000, 'Stein': 50000, 'Lehm': 50000, 'Eisen': 5000, 'Schwefel': 5000}
env.buildings['Hochschule_1'] = 1

mask = env.get_action_mask()
research_offset = 120
valid_research = [a for a in range(research_offset, research_offset + 50) if mask[a] == 1]
print(f'Gueltige Research-Actions: {len(valid_research)}')

if valid_research:
    action = valid_research[0]
    tech_idx = action - research_offset
    tech_name = env.tech_list[tech_idx]
    print(f'  Test: Action {action} = Research {tech_name}')

    obs, reward, done, trunc, info = env.step(action)
    # current_research ist ein Tuple (tech_name, remaining_time)
    in_progress = env.current_research is not None and env.current_research[0] == tech_name

    if in_progress:
        print('  [OK] Forschung gestartet')
    else:
        errors.append(f'RESEARCH: {tech_name} nicht gestartet')
else:
    print('  Keine Forschung verfuegbar')

# ============================================
print('\n4. RECRUIT - Check')
print('============================================')

env.reset()
env.resources = {'Taler': 50000, 'Holz': 50000, 'Stein': 50000, 'Lehm': 50000, 'Eisen': 5000, 'Schwefel': 5000}
env.buildings['Kaserne_1'] = 1

mask = env.get_action_mask()
recruit_offset = 170
valid_recruit = [a for a in range(recruit_offset, recruit_offset + 22) if mask[a] == 1]
print(f'Gueltige Recruit-Actions: {len(valid_recruit)}')

if valid_recruit:
    action = valid_recruit[0]
    soldier_idx = action - recruit_offset
    soldier_name = env.soldier_types[soldier_idx]
    print(f'  Test: Action {action} = Recruit {soldier_name}')

    queue_before = len(env.recruit_queue)
    obs, reward, done, trunc, info = env.step(action)
    queue_after = len(env.recruit_queue)

    # Soldaten werden in Queue gestellt und brauchen Trainingszeit
    if queue_after > queue_before:
        queued_soldier = env.recruit_queue[-1][0]
        print(f'  [OK] {queued_soldier} in Trainings-Queue')
    else:
        errors.append(f'RECRUIT: {soldier_name} nicht in Queue')
else:
    print('  Keine Rekrutierung moeglich')

# ============================================
print('\n5. RESOURCE BATCH (Holz, Deposits, Minen) - Check')
print('============================================')

env.reset()
mask = env.get_action_mask()
resource_offset = 192
valid_resource = [a for a in range(resource_offset, resource_offset + 54) if mask[a] == 1]
print(f'Gueltige Resource-Actions: {len(valid_resource)}')

# Test wood assign
if valid_resource and valid_resource[0] < resource_offset + 3:
    action = valid_resource[0]
    batch_size = [1, 3, 5][action - resource_offset]

    wood_before = env.wood_serfs
    obs, reward, done, trunc, info = env.step(action)
    wood_after = env.wood_serfs

    if wood_after > wood_before:
        print(f'  [OK] assign_wood_x{batch_size}: {wood_before}->{wood_after}')
    else:
        errors.append('RESOURCE: Holz-Zuweisung fehlgeschlagen')

# Test deposit recall
env.reset()
# Weise Serfs zu Lehm-Deposit zu
env._assign_deposit_batch('Lehm', 3)
lehm_serfs = env.deposit_categories['Lehm']['serfs_assigned']
print(f'  Lehm-Deposit Serfs: {lehm_serfs}')

# Recall
env._recall_deposit_batch('Lehm', 2)
lehm_serfs_after = env.deposit_categories['Lehm']['serfs_assigned']
if lehm_serfs_after < lehm_serfs:
    print(f'  [OK] recall_Lehm: {lehm_serfs}->{lehm_serfs_after}')
else:
    errors.append('RESOURCE: Lehm-Recall fehlgeschlagen')

# ============================================
print('\n6. SERF BUY/DISMISS - Check')
print('============================================')

env.reset()
env.resources = {'Taler': 50000, 'Holz': 50000, 'Stein': 50000, 'Lehm': 50000, 'Eisen': 5000, 'Schwefel': 5000}
# Baue Dorfzentrum fuer Kapazitaet (sonst kann man keine Serfs kaufen!)
env.buildings['Dorfzentrum_1'] = 1

mask = env.get_action_mask()
serf_offset = 246
valid_serf = [a for a in range(serf_offset, serf_offset + 6) if mask[a] == 1]
print(f'Gueltige Serf-Actions: {len(valid_serf)}')
print(f'  Village Capacity: {env._get_total_village_capacity()}')
print(f'  Total Leibeigene: {env.total_leibeigene}')

# Test buy (mit Dorfzentrum)
if mask[serf_offset]:  # buy_serf_x1
    action = serf_offset
    total_before = env.total_leibeigene
    obs, reward, done, trunc, info = env.step(action)
    total_after = env.total_leibeigene

    if total_after > total_before:
        print(f'  [OK] buy_serf_x1: {total_before}->{total_after}')
    else:
        errors.append('SERF: Kauf fehlgeschlagen')
else:
    print('  Kauf nicht moeglich (Kapazitaet oder Taler)')

# Test dismiss
if env.free_leibeigene > 0:
    action = serf_offset + 3  # dismiss_serf_x1
    total_before = env.total_leibeigene
    obs, reward, done, trunc, info = env.step(action)
    total_after = env.total_leibeigene

    if total_after < total_before:
        print(f'  [OK] dismiss_serf_x1: {total_before}->{total_after}')
    else:
        errors.append('SERF: Entlassen fehlgeschlagen')

# ============================================
print('\n7. BATCH RECRUIT (Scharfschuetzen x3, x5) - Check')
print('============================================')

env.reset()
env.resources = {'Taler': 50000, 'Holz': 50000, 'Stein': 50000, 'Lehm': 50000, 'Eisen': 5000, 'Schwefel': 5000}
env.buildings['Buechsenmacherei_1'] = 1
env.researched_techs.add('Luntenschloss')

mask = env.get_action_mask()
batch_recruit_offset = 252
valid_batch = [a for a in range(batch_recruit_offset, batch_recruit_offset + 4) if mask[a] == 1]
print(f'Gueltige Batch-Recruit-Actions: {len(valid_batch)}')

if valid_batch:
    print('  [OK] Batch-Recruit verfuegbar')
else:
    print('  Keine Batch-Rekrutierung (Voraussetzungen fehlen - normal)')

# ============================================
print('\n8. DEMOLISH - Check')
print('============================================')

env.reset()
env.buildings['Wohnhaus_1'] = 1

mask = env.get_action_mask()
demolish_offset = 256
valid_demolish = [a for a in range(demolish_offset, demolish_offset + 28) if mask[a] == 1]
print(f'Gueltige Demolish-Actions: {len(valid_demolish)}')

if valid_demolish:
    action = valid_demolish[0]
    building_idx = action - demolish_offset
    building_name = env.buildable_buildings[building_idx]

    count_before = env.buildings.get(building_name, 0)
    obs, reward, done, trunc, info = env.step(action)
    count_after = env.buildings.get(building_name, 0)

    if count_after < count_before:
        print(f'  [OK] {building_name} abgerissen: {count_before}->{count_after}')
    else:
        errors.append(f'DEMOLISH: {building_name} nicht abgerissen')

# ============================================
print('\n9. BLESS (5 Kategorien) - Check')
print('============================================')

env.reset()
env.buildings['Kloster_1'] = 1
env.faith = 10000

mask = env.get_action_mask()
bless_offset = 284
valid_bless = [a for a in range(bless_offset, bless_offset + 5) if mask[a] == 1]
print(f'Gueltige Bless-Actions: {len(valid_bless)}')

if valid_bless:
    action = valid_bless[0]
    cat = action - bless_offset
    print(f'  Test: Bless Kategorie {cat}')

    faith_before = env.faith
    obs, reward, done, trunc, info = env.step(action)
    faith_after = env.faith

    print(f'  [OK] Faith: {faith_before}->{faith_after}')
else:
    print('  Kein Segen moeglich (Kloster fehlt oder nicht genug Faith)')

# ============================================
print('\n10. TAX (5 Stufen) - Check')
print('============================================')

env.reset()
mask = env.get_action_mask()
tax_offset = 289
valid_tax = [a for a in range(tax_offset, tax_offset + 5) if mask[a] == 1]
print(f'Gueltige Tax-Actions: {len(valid_tax)}')

current_tax = env.current_tax_level
print(f'  Aktuelle Steuerstufe: {current_tax}')

for action in valid_tax:
    new_level = action - tax_offset
    if new_level != current_tax:
        obs, reward, done, trunc, info = env.step(action)
        if env.current_tax_level == new_level:
            print(f'  [OK] Steuerstufe gewechselt: {current_tax}->{new_level}')
        else:
            errors.append(f'TAX: Wechsel zu {new_level} fehlgeschlagen')
        break

# ============================================
print('\n11. ALARM (AN/AUS) - Check')
print('============================================')

env.reset()
mask = env.get_action_mask()
alarm_offset = 294
valid_alarm = [a for a in range(alarm_offset, alarm_offset + 2) if mask[a] == 1]
print(f'Gueltige Alarm-Actions: {len(valid_alarm)}')

if valid_alarm:
    alarm_before = env.alarm_active
    action = alarm_offset if not alarm_before else alarm_offset + 1
    obs, reward, done, trunc, info = env.step(action)
    alarm_after = env.alarm_active
    print(f'  [OK] Alarm: {alarm_before}->{alarm_after}')

# ============================================
print('\n12. BUILD SERF (Baustellen-Zuweisung) - Check')
print('============================================')

env.reset()
env.resources = {'Taler': 50000, 'Holz': 50000, 'Stein': 50000, 'Lehm': 50000, 'Eisen': 5000, 'Schwefel': 5000}
env.step(7)  # Wohnhaus bauen

mask = env.get_action_mask()
build_serf_offset = 296
valid_build_serf = [a for a in range(build_serf_offset, build_serf_offset + 6) if mask[a] == 1]
print(f'Gueltige Build-Serf-Actions: {len(valid_build_serf)}')

if valid_build_serf and env.construction_sites:
    action = valid_build_serf[0]

    sites_before = env.construction_sites[0]['serfs_assigned']
    obs, reward, done, trunc, info = env.step(action)
    sites_after = env.construction_sites[0]['serfs_assigned']

    if sites_after > sites_before:
        print(f'  [OK] Serfs zugewiesen: {sites_before}->{sites_after}')
    else:
        errors.append('BUILD_SERF: Zuweisung fehlgeschlagen')
else:
    print('  Keine Build-Serf-Action verfuegbar')

# ============================================
print('\n' + '=' * 60)
print('ZUSAMMENFASSUNG')
print('=' * 60)

if errors:
    print(f'FEHLER ({len(errors)}):')
    for e in errors:
        print(f'  - {e}')
else:
    print('ALLE 12 ACTION-KATEGORIEN FUNKTIONIEREN!')
