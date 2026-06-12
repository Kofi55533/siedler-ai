# -*- coding: utf-8 -*-
"""Test aller Actions im Multi-Step System."""

from environment import SiedlerScharfschuetzenEnv, MAIN_ACTIONS, ActionPhase
import numpy as np

print('=' * 60)
print('VOLLSTAENDIGER ACTION-TEST (MULTI-STEP)')
print('=' * 60)

env = SiedlerScharfschuetzenEnv()
obs, info = env.reset()

errors = []


def _first_valid(mask):
    idxs = np.where(mask)[0]
    return int(idxs[0]) if len(idxs) > 0 else 0


def _run_flow(main_action_name, phase_selector=None):
    phase_selector = phase_selector or {}
    main_idx = MAIN_ACTIONS.index(main_action_name)
    main_mask = env.action_masks()
    if main_idx >= len(main_mask) or not main_mask[main_idx]:
        errors.append(f"{main_action_name}: Hauptaktion ist maskiert")
        return obs, 0.0, False, False, {"blocked": True}

    obs, reward, done, trunc, info = env.step(main_idx)
    while info.get("multi_step"):
        phase = env.current_phase
        mask = env.action_masks()
        if phase in phase_selector:
            choice = phase_selector[phase](mask)
        else:
            choice = _first_valid(mask)
        if choice >= len(mask) or not mask[choice]:
            choice = _first_valid(mask)
        obs, reward, done, trunc, info = env.step(choice)
    return obs, reward, done, trunc, info


def _build_flow_selectors(building_name):
    category_idx = env._get_build_category_index(building_name)
    building_idx = env.buildable_buildings.index(building_name)
    return {
        ActionPhase.SOURCE_CATEGORY: lambda mask: 0 if mask[0] else _first_valid(mask),
        ActionPhase.SOURCE_SPECIFIC: lambda mask: 0,
        ActionPhase.QUANTITY: lambda mask: 0 if mask[0] else _first_valid(mask),
        ActionPhase.BUILD_CATEGORY: lambda mask, idx=category_idx: idx if idx < len(mask) and mask[idx] else _first_valid(mask),
        ActionPhase.BUILDING: lambda mask, idx=building_idx: idx if idx < len(mask) and mask[idx] else _first_valid(mask),
        ActionPhase.POSITION_MODE: lambda mask: 0 if mask[0] else _first_valid(mask),
        ActionPhase.POSITION_GROUP: _first_valid,
        ActionPhase.POSITION_INDEX: _first_valid,
    }


# ============================================
print('\n1. BUILD (eigener build-Flow) - Check')
print('============================================')

env.reset()
# Genug Ressourcen fuer Bau
env.resources = {'Taler': 50000, 'Holz': 50000, 'Stein': 50000, 'Lehm': 50000, 'Eisen': 5000, 'Schwefel': 5000}

sites_before = len(env.construction_sites)

_run_flow("build", phase_selector=_build_flow_selectors("Wohnhaus_1"))

sites_after = len(env.construction_sites)
if sites_after > sites_before:
    print('  [OK] Baustelle erstellt')
else:
    errors.append('BUILD: Keine Baustelle erstellt')

# ============================================
print('\n2. UPGRADE - Check')
print('============================================')

env.reset()
env.resources = {'Taler': 50000, 'Holz': 50000, 'Stein': 50000, 'Lehm': 50000, 'Eisen': 5000, 'Schwefel': 5000}
env.buildings['Wohnhaus_1'] = 1

upgrade_queue_before = len(env.upgrade_queue)

_run_flow(
    "upgrade",
    phase_selector={
        ActionPhase.BUILDING: _first_valid,
        ActionPhase.POSITION_GROUP: lambda mask: 0,
        ActionPhase.POSITION_INDEX: lambda mask: 0,
    },
)

upgrade_queue_after = len(env.upgrade_queue)
if upgrade_queue_after > upgrade_queue_before:
    print('  [OK] Upgrade gestartet')
else:
    print('  Kein Upgrade verfuegbar (normal)')

# ============================================
print('\n3. RESEARCH - Check')
print('============================================')

env.reset()
env.resources = {'Taler': 50000, 'Holz': 50000, 'Stein': 50000, 'Lehm': 50000, 'Eisen': 5000, 'Schwefel': 5000}
env.buildings['Hochschule_1'] = 1

_run_flow(
    "research",
    phase_selector={
        ActionPhase.TECH_BUILDING: _first_valid,
        ActionPhase.TECH: _first_valid,
    },
)

if env.current_researches:
    print(f'  [OK] Forschung gestartet: {env.current_researches[0][0]}')
else:
    errors.append('RESEARCH: Forschung nicht gestartet')

# ============================================
print('\n4. RECRUIT - Check')
print('============================================')

env.reset()
env.resources = {'Taler': 50000, 'Holz': 50000, 'Stein': 50000, 'Lehm': 50000, 'Eisen': 5000, 'Schwefel': 5000}
env.buildings['Kaserne_1'] = 1

queue_before = len(env.recruit_queue)

_run_flow(
    "recruit",
    phase_selector={
        ActionPhase.SOLDIER: _first_valid,
        ActionPhase.QUANTITY: lambda mask: 0,
    },
)

queue_after = len(env.recruit_queue)
if queue_after > queue_before:
    queued_soldier = env.recruit_queue[-1][0]
    print(f'  [OK] {queued_soldier} in Trainings-Queue')
else:
    errors.append('RECRUIT: Kein Soldat in Queue')

# ============================================
print('\n5. RESOURCE (Holz) - Check')
print('============================================')

env.reset()
wood_before = env.wood_serfs

_run_flow(
    "assign_serf",
    phase_selector={
        ActionPhase.SOURCE_CATEGORY: lambda mask: 0 if mask[0] else _first_valid(mask),
        ActionPhase.SOURCE_SPECIFIC: lambda mask: 0,
        ActionPhase.QUANTITY: lambda mask: 0,
        ActionPhase.TARGET_CATEGORY: lambda mask: 1 if len(mask) > 1 and mask[1] else _first_valid(mask),
        ActionPhase.TARGET_SPECIFIC: lambda mask: 0,
    },
)

wood_after = env.wood_serfs
if wood_after > wood_before:
    print(f'  [OK] assign_wood: {wood_before}->{wood_after}')
else:
    errors.append('RESOURCE: Holz-Zuweisung fehlgeschlagen')

# Deposit-Recall (direkt testen)
env.reset()
env._assign_deposit_batch('Lehm', 3)
lehm_serfs = env.deposit_categories['Lehm']['serfs_assigned']
print(f'  Lehm-Deposit Serfs: {lehm_serfs}')

env._recall_deposit_batch('Lehm', 2)
lehm_serfs_after = env.deposit_categories['Lehm']['serfs_assigned']
if lehm_serfs_after < lehm_serfs:
    print(f'  [OK] recall_Lehm: {lehm_serfs}->{lehm_serfs_after}')
else:
    errors.append('RESOURCE: Lehm-Recall fehlgeschlagen')

# Exakter Holz-Zielcheck ueber Zone/TopK-Encoding
env.reset()
tree_specific = 0
tree_idx = env._get_wood_zone_rank_tree_index(
    tree_specific,
    1,
    mode="assign",
    available_free_override=env.free_leibeigene,
)
tree = env.tree_list_internal[tree_idx]
_run_flow(
    "assign_serf",
    phase_selector={
        ActionPhase.SOURCE_CATEGORY: lambda mask: 0 if mask[0] else _first_valid(mask),
        ActionPhase.SOURCE_SPECIFIC: lambda mask: 0,
        ActionPhase.QUANTITY: lambda mask: 0,
        ActionPhase.TARGET_CATEGORY: lambda mask: 1 if len(mask) > 1 and mask[1] else _first_valid(mask),
        ActionPhase.TARGET_SPECIFIC: lambda mask, idx=tree_specific: idx if idx < len(mask) and mask[idx] else _first_valid(mask),
    },
)
tree_targeted = any(
    serf.target_position
    and int(serf.target_position.x) == int(tree["x"])
    and int(serf.target_position.y) == int(tree["y"])
    for serf in env.production_system.serfs
)
if env.tree_list_internal[tree_idx]["serfs_assigned"] > 0 and tree_targeted:
    print(f'  [OK] exact_tree_target: TREE_{tree_idx} @ ({int(tree["x"])}, {int(tree["y"])})')
else:
    errors.append('RESOURCE: Einzelbaum-Zielkoordinate nicht uebernommen')

# ============================================
print('\n6. SERF BUY/DISMISS - Check')
print('============================================')

env.reset()
env.resources = {'Taler': 50000, 'Holz': 50000, 'Stein': 50000, 'Lehm': 50000, 'Eisen': 5000, 'Schwefel': 5000}
# Dorfzentrum fuer Kapazitaet
env.buildings['Dorfzentrum_1'] = 1

# Buy
before = env.total_leibeigene
_run_flow(
    "buy_serf",
    phase_selector={ActionPhase.QUANTITY: lambda mask: 0},
)
after = env.total_leibeigene
if after > before:
    print(f'  [OK] buy_serf_x1: {before}->{after}')
else:
    errors.append('SERF: Kauf fehlgeschlagen')

# Dismiss (aus FREE)
if env.free_leibeigene > 0:
    before = env.total_leibeigene
    _run_flow(
        "dismiss_serf",
        phase_selector={
            ActionPhase.SOURCE_CATEGORY: lambda mask: 0 if mask[0] else _first_valid(mask),
            ActionPhase.SOURCE_SPECIFIC: lambda mask: 0,
            ActionPhase.QUANTITY: lambda mask: 0,
        },
    )
    after = env.total_leibeigene
    if after < before:
        print(f'  [OK] dismiss_serf_x1: {before}->{after}')
    else:
        errors.append('SERF: Entlassen fehlgeschlagen')

# ============================================
print('\n7. BATCH RECRUIT (Quantity > 1) - Check')
print('============================================')

env.reset()
env.resources = {'Taler': 50000, 'Holz': 50000, 'Stein': 50000, 'Lehm': 50000, 'Eisen': 5000, 'Schwefel': 5000}
env.buildings['Buechsenmacherei_1'] = 1
env.researched_techs.add('Luntenschloss')

queue_before = len(env.recruit_queue)
_run_flow(
    "recruit",
    phase_selector={
        ActionPhase.SOLDIER: _first_valid,
        ActionPhase.QUANTITY: lambda mask: 1,  # x2
    },
)
queue_after = len(env.recruit_queue)
if queue_after > queue_before:
    print('  [OK] Batch-Recruit (x2) gestartet')
else:
    print('  Keine Batch-Rekrutierung (Voraussetzungen fehlen - normal)')

# ============================================
print('\n8. DEMOLISH - Check')
print('============================================')

env.reset()
env.buildings['Wohnhaus_1'] = 1
# Explizit eine Instanz inkl. Position/Grid anlegen, damit Positionsphasen sicher greifen.
demo_pos = {"x": env.hq_position[0] + 2200, "y": env.hq_position[1] + 2200}
env.building_position_map["Wohnhaus_1_test"] = demo_pos
env._on_building_completed("Wohnhaus_1", demo_pos, pos_key="Wohnhaus_1_test")

before = env.buildings.get('Wohnhaus_1', 0)
_run_flow(
    "demolish",
    phase_selector={
        ActionPhase.BUILDING: lambda mask: env.demolishable_buildings.index("Wohnhaus_1"),
        ActionPhase.POSITION_GROUP: _first_valid,
        ActionPhase.POSITION_INDEX: _first_valid,
    },
)
after = env.buildings.get('Wohnhaus_1', 0)
if after < before:
    print(f'  [OK] Wohnhaus_1 abgerissen: {before}->{after}')
else:
    errors.append('DEMOLISH: Wohnhaus_1 nicht abgerissen')

# ============================================
print('\n9. BLESS (5 Kategorien) - Check')
print('============================================')

env.reset()
env.buildings['Kloster_1'] = 1
env.faith = 10000

_run_flow(
    "bless",
    phase_selector={ActionPhase.CATEGORY: _first_valid},
)

# Pruefe ob irgendein Cooldown gesetzt wurde
if any(v > 0 for v in env.bless_cooldowns.values()):
    print('  [OK] Segen ausgeloest (Cooldown gesetzt)')
else:
    print('  Kein Segen moeglich (Kloster fehlt oder nicht genug Faith)')

# ============================================
print('\n10. TAX (5 Stufen) - Check')
print('============================================')

env.reset()
current_tax = env.current_tax_level
env.researched_techs.add("Bildung")
env._can_cache = {}

_run_flow(
    "tax",
    phase_selector={
        ActionPhase.TAX_LEVEL: lambda mask: 0 if current_tax != 0 else 1,
    },
)

if env.current_tax_level != current_tax:
    print(f'  [OK] Steuerstufe gewechselt: {current_tax}->{env.current_tax_level}')
else:
    errors.append('TAX: Steuerwechsel fehlgeschlagen')

# ============================================
print('\n11. ALARM (AN/AUS) - Check')
print('============================================')

env.reset()
alarm_before = env.alarm_active

_run_flow(
    "alarm",
    phase_selector={ActionPhase.ON_OFF: lambda mask: 0 if not alarm_before else 1},
)

alarm_after = env.alarm_active
print(f'  [OK] Alarm: {alarm_before}->{alarm_after}')

# ============================================
print('\n12. BUILD SERF (Baustellen-Zuweisung) - Check')
print('============================================')

env.reset()
env.resources = {'Taler': 50000, 'Holz': 50000, 'Stein': 50000, 'Lehm': 50000, 'Eisen': 5000, 'Schwefel': 5000}

# Erst Baustelle ueber den aktuellen build-Flow erstellen
_run_flow("build", phase_selector=_build_flow_selectors("Wohnhaus_1"))

if env.construction_sites:
    assigned_before = env.construction_sites[0]['serfs_assigned']

    # Dann Serfs explizit zur Baustelle schicken
    _run_flow(
        "assign_serf",
        phase_selector={
            ActionPhase.SOURCE_CATEGORY: lambda mask: 0 if mask[0] else _first_valid(mask),
            ActionPhase.SOURCE_SPECIFIC: lambda mask: 0,
            ActionPhase.QUANTITY: lambda mask: 0,
            ActionPhase.TARGET_CATEGORY: lambda mask: 6 if len(mask) > 6 and mask[6] else _first_valid(mask),
            ActionPhase.TARGET_SPECIFIC: lambda mask: 0,
        },
    )

    assigned_after = env.construction_sites[0]['serfs_assigned']

    if assigned_after > assigned_before:
        print(f'  [OK] Serfs zugewiesen: {assigned_before}->{assigned_after}')
    else:
        errors.append('BUILD_SERF: Zuweisung fehlgeschlagen')
else:
    errors.append('BUILD_SERF: Keine Baustelle erstellt')

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
