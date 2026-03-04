# -*- coding: utf-8 -*-
"""
Siedler AI - Interaktiver Spielmodus

Steuere das Environment manuell wie der Agent.
Ausfuehren:  python play_game.py
"""

import os
import sys

# Vollstaendige Simulation (kein fast_train) fuer realistisches Spielgefuehl
os.environ.setdefault("SIEDLER_FAST_TRAIN", "0")
os.environ.setdefault("SIEDLER_DISABLE_RUNTIME_PATHING", "0")
os.environ.setdefault("SIEDLER_USE_SPATIAL", "0")
os.environ.setdefault("SIEDLER_TRAIN_PROFILE", "legacy")


def _clear():
    os.system("cls" if os.name == "nt" else "clear")


def _format_res(resources: dict) -> str:
    important = ["Holz", "Stein", "Lehm", "Eisen", "Schwefel", "Taler"]
    parts = []
    for k in important:
        v = resources.get(k, 0)
        if v > 0:
            parts.append(f"{k}:{int(v)}")
    return "  ".join(parts) if parts else "(keine)"


def _format_buildings(buildings: dict) -> str:
    active = {k: v for k, v in buildings.items() if v > 0}
    if not active:
        return "(keine)"
    # Sortiert nach Anzahl (haeufigstes zuerst)
    parts = []
    for k, v in sorted(active.items(), key=lambda x: -x[1]):
        parts.append(f"{k}({v}x)" if v > 1 else k)
    # Max 8 anzeigen
    if len(parts) > 8:
        return "  ".join(parts[:8]) + f"  ... +{len(parts)-8} weitere"
    return "  ".join(parts)


def _format_soldiers(soldiers: dict, scharfschuetzen: int) -> str:
    parts = [f"Scharfschuetzen:{scharfschuetzen}"]
    for k, v in soldiers.items():
        if v > 0:
            parts.append(f"{k}:{v}")
    return "  ".join(parts)


def _format_research(current_researches: list, researched_techs: set) -> str:
    if current_researches:
        active = ", ".join(f"{r[0]}({r[1]:.0f}s)" for r in current_researches[:3])
        return f"Aktiv: {active}"
    return f"Fertig: {len(researched_techs)} Techs"


def show_state(env):
    """Zeigt aktuellen Game-State."""
    width = 62
    bar = "=" * width

    print(bar)
    print(f"  SIEDLER AI | Zeit: {int(env.current_time)}s/{env.max_time}s"
          f" | Motivation: {getattr(env, 'base_motivation', 0)*100:.0f}%"
          f" | Steuer: {getattr(env, 'current_tax_level', 2)}")
    print(bar)

    # Ressourcen
    print(f"RESSOURCEN:  {_format_res(env.resources)}")

    # Leibeigene
    total = getattr(env, "total_leibeigene", 0)
    free = getattr(env, "free_leibeigene", 0)
    print(f"LEIBEIGENE:  {total} gesamt, {free} frei"
          f"  |  Glaube: {int(getattr(env, 'faith', 0))}")

    # Gebaeude
    print(f"GEBAEUDE:    {_format_buildings(env.buildings)}")

    # Forschung
    cr = getattr(env, "current_researches", [])
    rt = getattr(env, "researched_techs", set())
    print(f"FORSCHUNG:   {_format_research(cr, rt)}")

    # Baustellen
    sites = getattr(env, "construction_sites", [])
    if sites:
        site_str = ", ".join(
            f"{s.get('building', '?')}({s.get('remaining_work', 0):.0f}h)"
            for s in sites[:4]
        )
        if len(sites) > 4:
            site_str += f" +{len(sites)-4}"
        print(f"BAUSTELLEN:  {site_str}")

    # Militaer
    soldiers = getattr(env, "soldiers", {})
    scharf = getattr(env, "scharfschuetzen", 0)
    print(f"MILITAER:    {_format_soldiers(soldiers, scharf)}")

    # Alarm
    alarm = getattr(env, "alarm_active", False)
    if alarm:
        print(f"  !!! ALARM AKTIV !!!")


def get_action_names(env) -> list:
    """
    Gibt Liste von (index, name, enabled) fuer die aktuelle Phase zurueck.
    """
    from environment import (
        ActionPhase, MAIN_ACTIONS, QUANTITY_VALUES, RESEARCH_BUILDINGS,
        SOURCE_CATEGORIES, TARGET_CATEGORIES, TAX_LEVELS, BLESS_CATEGORIES,
    )

    phase = env.current_phase
    mask = env.action_masks()

    # Maske ist auf max_action_size gepadded — wir nehmen nur die relevante Laenge
    n = env.action_spaces[phase].n
    phase_mask = mask[:n]

    options = []

    if phase == ActionPhase.MAIN:
        for i, name in enumerate(MAIN_ACTIONS):
            enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
            options.append((i, name, enabled))

    elif phase == ActionPhase.BUILDING:
        flow = getattr(env, "current_flow", None)
        if flow == "upgrade":
            blist = env.upgradeable_buildings
        else:
            blist = env.demolishable_buildings
        for i in range(n):
            name = blist[i] if i < len(blist) else f"Gebaeude_{i}"
            enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
            options.append((i, name, enabled))

    elif phase == ActionPhase.TECH_BUILDING:
        for i, bname in enumerate(RESEARCH_BUILDINGS):
            if i >= n:
                break
            enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
            options.append((i, bname, enabled))

    elif phase == ActionPhase.TECH:
        # Welches Forschungsgebaeude wurde gewaehlt?
        from environment import ActionPhase as AP
        tb_idx = env.pending_selections.get(AP.TECH_BUILDING, 0)
        tb_name = RESEARCH_BUILDINGS[tb_idx] if tb_idx < len(RESEARCH_BUILDINGS) else "Hochschule"
        techs = env.tech_by_building.get(tb_name, [])
        for i in range(n):
            name = techs[i] if i < len(techs) else f"Tech_{i}"
            enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
            options.append((i, name, enabled))

    elif phase == ActionPhase.SOLDIER:
        for i, sname in enumerate(env.soldier_types):
            if i >= n:
                break
            enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
            options.append((i, sname, enabled))

    elif phase == ActionPhase.QUANTITY:
        for i, qty in enumerate(QUANTITY_VALUES):
            if i >= n:
                break
            enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
            options.append((i, str(qty), enabled))

    elif phase == ActionPhase.SOURCE_CATEGORY:
        for i, name in SOURCE_CATEGORIES.items():
            if i >= n:
                break
            enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
            options.append((i, name, enabled))

    elif phase == ActionPhase.TARGET_CATEGORY:
        for i, name in TARGET_CATEGORIES.items():
            if i >= n:
                break
            enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
            options.append((i, name, enabled))

    elif phase in (ActionPhase.SOURCE_SPECIFIC, ActionPhase.TARGET_SPECIFIC):
        # Zeige einfach Indizes der aktiven Optionen
        for i in range(n):
            enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
            options.append((i, f"Option {i}", enabled))

    elif phase in (ActionPhase.POSITION_GROUP, ActionPhase.POSITION_INDEX):
        label = "Gruppe" if phase == ActionPhase.POSITION_GROUP else "Position"
        for i in range(n):
            enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
            options.append((i, f"{label} {i}", enabled))

    elif phase == ActionPhase.CATEGORY:
        for i, cat in BLESS_CATEGORIES.items():
            if i >= n:
                break
            enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
            options.append((i, cat.get("name", f"Segen_{i}"), enabled))

    elif phase == ActionPhase.TAX_LEVEL:
        for i, lvl in TAX_LEVELS.items():
            if i >= n:
                break
            enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
            options.append((i, lvl.get("name", f"Stufe_{i}"), enabled))

    elif phase == ActionPhase.ON_OFF:
        for i, name in enumerate(["Aus", "Ein"]):
            if i >= n:
                break
            enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
            options.append((i, name, enabled))

    else:
        for i in range(n):
            enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
            options.append((i, f"Option {i}", enabled))

    return options


def show_actions(env):
    """Zeigt verfuegbare Aktionen fuer die aktuelle Phase."""
    from environment import ActionPhase

    phase = env.current_phase
    flow = getattr(env, "current_flow", None)

    width = 62
    print("-" * width)

    phase_label = phase.value.upper()
    flow_label = f"  (Aktion: {flow})" if flow and phase != ActionPhase.MAIN else ""
    print(f"PHASE: {phase_label}{flow_label}")
    print("-" * width)

    options = get_action_names(env)
    enabled_options = [(i, name) for i, name, ok in options if ok]
    disabled_options = [(i, name) for i, name, ok in options if not ok]

    if not enabled_options:
        print("  (keine Aktionen verfuegbar — environment-Fehler?)")
        return

    # Verfuegbare Aktionen in 2 Spalten
    print("  Verfuegbar:")
    col_w = 28
    for j in range(0, len(enabled_options), 2):
        left_i, left_n = enabled_options[j]
        left_str = f"  [{left_i:>2}] {left_n}"
        if j + 1 < len(enabled_options):
            right_i, right_n = enabled_options[j + 1]
            right_str = f"[{right_i:>2}] {right_n}"
            print(f"{left_str:<{col_w+4}}  {right_str}")
        else:
            print(left_str)

    # Deaktivierte Aktionen kompakt
    if disabled_options and len(disabled_options) <= 15:
        disabled_str = "  ".join(f"[{i}]" for i, _ in disabled_options[:10])
        print(f"\n  Gesperrt: {disabled_str}")

    print("-" * width)


def play():
    """Hauptloop des interaktiven Spielmodus."""
    print("Lade Environment...")
    from environment import SiedlerScharfschuetzenEnv

    env = SiedlerScharfschuetzenEnv(player_id=1, use_spatial_obs=False)
    obs, _ = env.reset(seed=0)

    total_reward = 0.0
    step_count = 0
    last_info = {}
    last_action_name = "—"

    print("Environment geladen. Starte Spiel...\n")

    while True:
        _clear()
        show_state(env)

        # Letztes Ergebnis anzeigen
        if step_count > 0:
            print(f"\n  Letzter Step #{step_count}: [{last_action_name}]"
                  f"  Reward: {last_info.get('step_reward', 0):.4f}"
                  f"  Gesamt: {total_reward:.3f}")
            if last_info.get("blocked_invalid_action"):
                print("  !!! Ungueltige Aktion — wurde ignoriert !!!")

        show_actions(env)

        # Eingabe
        try:
            raw = input("Aktion (Nummer oder 'q'=Beenden 'r'=Reset 'w'=Warten): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBeendet.")
            break

        if raw.lower() == "q":
            print(f"\nSpiel beendet nach {step_count} Steps. Gesamt-Reward: {total_reward:.3f}")
            break

        if raw.lower() == "r":
            obs, _ = env.reset()
            total_reward = 0.0
            step_count = 0
            last_info = {}
            last_action_name = "—"
            print("Reset!")
            continue

        if raw.lower() == "w":
            action = 0  # wait
        else:
            try:
                action = int(raw)
            except ValueError:
                print("Ungueltige Eingabe. Bitte Zahl eingeben.")
                input("Enter druecken...")
                continue

        # Maske pruefen
        import numpy as np
        mask = env.action_masks()
        n = env.action_spaces[env.current_phase].n
        if action < 0 or action >= n or not mask[action]:
            print(f"Aktion {action} ist nicht verfuegbar!")
            input("Enter druecken...")
            continue

        # Schritt ausfuehren
        from environment import MAIN_ACTIONS
        options = get_action_names(env)
        action_name = next((name for i, name, _ in options if i == action), str(action))
        if env.current_phase.value == "main":
            last_action_name = action_name
        else:
            last_action_name = f"{env.current_flow} > {action_name}"

        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        step_count += 1
        last_info = info

        # Multi-Step: weiter ohne _clear wenn noch in Sub-Phase
        if info.get("multi_step"):
            continue

        # Episode-Ende
        if terminated or truncated:
            _clear()
            show_state(env)
            print(f"\n{'='*62}")
            print(f"EPISODE BEENDET nach {step_count} Steps")
            print(f"Gesamt-Reward: {total_reward:.3f}")
            print(f"Scharfschuetzen: {env.scharfschuetzen}")
            print(f"{'='*62}")
            again = input("\nNeue Episode? (j/n): ").strip().lower()
            if again != "j":
                break
            obs, _ = env.reset()
            total_reward = 0.0
            step_count = 0
            last_info = {}
            last_action_name = "—"


if __name__ == "__main__":
    play()
