# -*- coding: utf-8 -*-
"""
Test-Skript für Siedler AI Mechaniken
Verifiziert: Segen, Forschung, Motivation, WorkTime, Scholar
"""

from environment import SiedlerScharfschuetzenEnv, BLESS_COOLDOWN, BLESS_DURATION


def test_bless_cooldown():
    """Test: Segen-Cooldown ist 180s (3 Minuten wie im Original)"""
    print("\n=== Test: Segen-Cooldown ===")

    env = SiedlerScharfschuetzenEnv()
    env.reset()

    # Simuliere Kloster und Faith
    env.buildings["Kloster_1"] = 1
    env.faith = 6000

    # Segen ausführen (Kategorie 0)
    env._bless(0)

    cooldown = env.bless_cooldowns[0]
    duration = env.bless_active_times[0]

    print(f"  Cooldown nach Segen: {cooldown}s (erwartet: 180s)")
    print(f"  Aktive Dauer: {duration}s (erwartet: 180s)")

    assert cooldown == 180, f"Cooldown sollte 180s sein, ist {cooldown}"
    assert duration == 180, f"Dauer sollte 180s sein, ist {duration}"
    print("  [OK] Segen-Cooldown korrekt (180s wie im Original)")


def test_monastery_motivation():
    """Test: Kloster erhöht Motivation"""
    print("\n=== Test: Kloster-Motivation ===")

    env = SiedlerScharfschuetzenEnv()
    env.reset()

    base = env._get_total_motivation()
    print(f"  Basis-Motivation: {base}")

    # Kloster bauen
    env.buildings["Kloster_1"] = 1
    with_monastery = env._get_total_motivation()
    print(f"  Mit Kloster_1: {with_monastery} (erwartet: {base + 0.08})")

    assert abs(with_monastery - (base + 0.08)) < 0.01, f"Kloster sollte +0.08 geben"

    # Kloster Level 2 testen
    env.buildings["Kloster_1"] = 0
    env.buildings["Kloster_2"] = 1
    with_monastery2 = env._get_total_motivation()
    print(f"  Mit Kloster_2: {with_monastery2} (erwartet: {base + 0.10})")

    assert abs(with_monastery2 - (base + 0.10)) < 0.01, f"Kloster_2 sollte +0.10 geben"
    print("  [OK] Kloster-Motivation-Effekt funktioniert")


def test_motivation_modifier():
    """Test: Motivation-Modifier wird an WorkforceManager übergeben"""
    print("\n=== Test: Motivation-Modifier ===")

    env = SiedlerScharfschuetzenEnv()
    env.reset()

    # Initial sollte Modifier 1.0 sein
    initial_mod = env.workforce_manager.motivation_modifier
    print(f"  Initial Modifier: {initial_mod}")

    # Segen aktivieren für höhere Motivation
    env.buildings["Kloster_1"] = 1
    env.faith = 6000
    env._bless(0)

    # Ein Step ausführen damit Modifier aktualisiert wird
    env.step(0)

    new_mod = env.workforce_manager.motivation_modifier
    print(f"  Nach Segen: {new_mod}")

    assert new_mod > initial_mod, f"Modifier sollte gestiegen sein"
    print("  [OK] Motivation-Modifier wird korrekt übergeben")


def test_scholar_creation():
    """Test: Scholar wird bei Hochschule-Bau erstellt"""
    print("\n=== Test: Scholar-Erstellung ===")

    env = SiedlerScharfschuetzenEnv()
    env.reset()

    # Village-Kapazität setzen damit Worker hinzugefügt werden können
    env.workforce_manager.set_village_capacity(100)

    # Zähle initiale Scholars
    initial_scholars = len([w for w in env.workforce_manager.workers
                           if w.worker_type == "scholar"])
    print(f"  Initiale Scholars: {initial_scholars}")

    # Simuliere Hochschule-Fertigstellung
    from worker_simulation import Position
    pos = Position(x=40000, y=23000)
    env._on_building_completed("Hochschule_1", pos)

    # Zähle neue Scholars
    new_scholars = len([w for w in env.workforce_manager.workers
                       if w.worker_type == "scholar"])
    print(f"  Nach Hochschule_1: {new_scholars}")

    assert new_scholars == initial_scholars + 1, f"Sollte 1 Scholar mehr sein"
    print("  [OK] Scholar wird bei Hochschule-Bau erstellt")


def test_scholar_efficiency():
    """Test: Forschung hängt von Gelehrten ab"""
    print("\n=== Test: Scholar-Effizienz ===")

    env = SiedlerScharfschuetzenEnv()
    env.reset()

    # Ohne Scholars sollte Effizienz 1.0 sein (Fallback)
    eff_no_scholars = env._get_scholar_efficiency()
    print(f"  Effizienz ohne Scholars: {eff_no_scholars}")
    assert eff_no_scholars == 1.0, "Ohne Scholars sollte Effizienz 1.0 sein"

    # Scholar hinzufügen
    from worker_simulation import Position
    pos = Position(x=40000, y=23000)
    env.workforce_manager.add_worker("scholar", pos, pos)

    # Effizienz mit Scholar
    eff_with_scholar = env._get_scholar_efficiency()
    print(f"  Effizienz mit Scholar: {eff_with_scholar}")

    # Neuer Scholar sollte 100% Effizienz haben (volle WorkTime)
    assert eff_with_scholar > 0.9, f"Neuer Scholar sollte hohe Effizienz haben"
    print("  [OK] Scholar-Effizienz wird berechnet")


def test_tax_motivation():
    """Test: Steuern beeinflussen Motivation"""
    print("\n=== Test: Steuern-Motivation ===")

    env = SiedlerScharfschuetzenEnv()
    env.reset()

    start_motivation = env.base_motivation
    print(f"  Start-Motivation: {start_motivation}")

    # Hohe Steuern setzen (Level 4 = -0.12/Tick)
    env.current_tax_level = 4

    # Simuliere mehrere Income-Cycles (INCOME_CYCLE = 60)
    for _ in range(1200):  # 2 Minuten
        env.step(0)

    end_motivation = env.base_motivation
    print(f"  Nach hohen Steuern: {end_motivation}")

    assert end_motivation < start_motivation, "Motivation sollte gesunken sein"
    print(f"  [OK] Steuern-Effekt funktioniert: {start_motivation} -> {end_motivation}")


def test_worker_types():
    """Test: Alle neuen Worker-Typen sind definiert"""
    print("\n=== Test: Worker-Typen ===")

    from worker_simulation import WORKER_PARAMS, WORKER_SPEEDS

    required_types = ["scholar", "engineer", "master_builder", "gunsmith"]

    for worker_type in required_types:
        assert worker_type in WORKER_PARAMS, f"{worker_type} fehlt in WORKER_PARAMS"
        assert worker_type in WORKER_SPEEDS, f"{worker_type} fehlt in WORKER_SPEEDS"
        print(f"  [OK] {worker_type} ist definiert")

    print("  [OK] Alle neuen Worker-Typen vorhanden")


if __name__ == "__main__":
    print("=" * 50)
    print("SIEDLER AI - MECHANIK-TESTS")
    print("=" * 50)

    try:
        test_worker_types()
        test_bless_cooldown()
        test_monastery_motivation()
        test_motivation_modifier()
        test_scholar_creation()
        test_scholar_efficiency()
        test_tax_motivation()

        print("\n" + "=" * 50)
        print("=== ALLE TESTS BESTANDEN ===")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n[FEHLER] TEST FEHLGESCHLAGEN: {e}")
    except Exception as e:
        print(f"\n[FEHLER] FEHLER: {e}")
        import traceback
        traceback.print_exc()
