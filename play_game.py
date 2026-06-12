# -*- coding: utf-8 -*-
"""
Siedler AI - Interaktiver Spielmodus

Steuere das Environment manuell wie der Agent.
Ausfuehren:  python play_game.py
GUI bewusst starten:  python play_game.py --gui
"""

import os
import sys
import queue as _q
import threading as _thr

# Vollstaendige Simulation (kein fast_train) fuer realistisches Spielgefuehl
os.environ.setdefault("SIEDLER_FAST_TRAIN", "0")
os.environ.setdefault("SIEDLER_DISABLE_RUNTIME_PATHING", "0")
os.environ.setdefault("SIEDLER_USE_SPATIAL", "0")
os.environ.setdefault("SIEDLER_TRAIN_PROFILE", "legacy")

# ANSI-Farben aktivieren (Windows braucht einmaligen os.system-Aufruf)
if os.name == "nt":
    os.system("")

# Farb-Konstanten
_R = "\033[0m"          # Reset
_BOLD = "\033[1m"
_DIM = "\033[2m"

# Karten-Farben
_C = {
    "t": "\033[32m",      # Holz/Baeume    = gruen
    "i": "\033[90m",      # Eisen-Stollen  (Minenbauslot, 4000cap) = grau
    "e": "\033[37m",      # Eisen-Vork.    (serf-only, kein Bau)  = silber
    "I": "\033[1;37m",    # Eisen-Mine     = hell-silber
    "s": "\033[97m",      # Stein-Stollen  (Minenbauslot)  = weiss
    "q": "\033[97m",      # Stein-Vork.    (serf-only)     = weiss
    "S": "\033[1;97m",    # Stein-Mine     = hell-weiss
    "l": "\033[33m",      # Lehm-Stollen   (Minenbauslot)  = braun
    "a": "\033[33m",      # Lehm-Vork.     (serf-only)     = braun
    "L": "\033[1;33m",    # Lehm-Mine      = hell-braun
    "f": "\033[93m",      # Schwefel-Stollen (Minenbauslot) = gelb
    "g": "\033[93m",      # Schwefel-Vork.   (serf-only)   = gelb
    "V": "\033[1;93m",    # Schwefel-Mine  = hell-gelb
    "H": "\033[1;91m",    # HQ             = rot+fett
    "D": "\033[1;96m",    # DZ             = hell-cyan
    "d": "\033[36m",      # freier DZ      = cyan
    "w": "\033[95m",      # Arbeiter       = magenta
    "p": "\033[1;95m",    # Leibeigener    = hell-magenta (fett)
    "b": "\033[1;33m",    # Baustelle      = gelb-fett (in Bau)
    ".": "\033[90m",      # Hintergrund    = dunkelgrau
}
_C_BLDG = "\033[94m"    # sonstige Gebaeude = blau

# UI-Farben
_HEAD  = "\033[1;33m"   # Header-Farbe     = gelb-fett
_KEY   = "\033[1;36m"   # Key-Labels       = cyan-fett
_OK    = "\033[32m"     # verfuegbar       = gruen
_GRAY  = "\033[90m"     # deaktiviert      = grau
_WARN  = "\033[91m"     # Warnung          = rot
_HL    = "\033[1;103m\033[30m"  # Highlight = gelber Hintergrund + schwarz


def _clear():
    os.system("cls" if os.name == "nt" else "clear")


def _apply_window_geometry(root, width: int, height: int, anchor: str = "center", margin: int = 24):
    """Positioniert Fenster sichtbar auf dem Desktop statt den Bildschirm zu ueberfahren."""
    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    width = max(720, min(width, sw - (margin * 2)))
    height = max(480, min(height, sh - (margin * 2)))
    if anchor == "top-right":
        x = max(margin, sw - width - margin)
        y = margin
    else:
        x = max(margin, (sw - width) // 2)
        y = max(margin, (sh - height) // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")


# --- Graphischer Live-View (Tkinter, Background-Thread, auto-refresh) ----

_render_module = None   # Gecachter Render-Modul-Import
_lv_base       = None   # Gecachtes Terrain-Bild (aendert sich nie)
_lv_queue: "_q.Queue | None" = None
_lv_thread: "_thr.Thread | None" = None
_lv_enabled    = False  # Ob das Live-View-Fenster aktiv ist


def _get_render_module():
    """Laedt render_replay_mp4 ueber sys.path — zuverlaessiger als spec-Import."""
    global _render_module
    if _render_module is not None:
        return _render_module
    archive_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "tools", "archive",
    )
    orig = sys.path[:]
    try:
        sys.path.insert(0, archive_dir)
        import render_replay_mp4 as _m
        _render_module = _m
        return _m
    finally:
        sys.path[:] = orig


def _live_view_thread_func(q: "_q.Queue"):
    """Tkinter-Fenster im Daemon-Thread: pollt Queue und zeigt neuste Frames."""
    try:
        import tkinter as tk
        from PIL import Image as _PIL, ImageTk
    except ImportError:
        return

    root = tk.Tk()
    root.title("Siedler AI — Live View")
    root.configure(bg="#111")
    root.minsize(520, 360)
    _apply_window_geometry(root, 900, 620, anchor="top-right", margin=28)
    lbl = tk.Label(root, bg="#111")
    lbl.pack(fill=tk.BOTH, expand=True)
    _ref = [None]

    def _close_live_view():
        global _lv_enabled, _lv_queue, _lv_thread
        _lv_enabled = False
        _lv_queue = None
        _lv_thread = None
        try:
            root.destroy()
        except tk.TclError:
            pass

    root.protocol("WM_DELETE_WINDOW", _close_live_view)
    root.bind("<Escape>", lambda _event: _close_live_view())

    def poll():
        if not root.winfo_exists():
            return
        latest = None
        try:
            while True:
                latest = q.get_nowait()
        except _q.Empty:
            pass
        if latest is not None:
            img = _PIL.fromarray(latest)
            img.thumbnail((1400, 900))
            photo = ImageTk.PhotoImage(img)
            lbl.config(image=photo)
            _ref[0] = photo  # GC-Schutz
        try:
            root.after(250, poll)
        except tk.TclError:
            pass

    root.after(150, poll)
    try:
        root.mainloop()
    except Exception:
        pass


def _ensure_live_view():
    """Startet Live-View-Thread falls nicht aktiv, gibt Queue zurueck."""
    global _lv_queue, _lv_thread
    if _lv_thread and _lv_thread.is_alive():
        return _lv_queue
    _lv_queue = _q.Queue(maxsize=2)
    t = _thr.Thread(target=_live_view_thread_func, args=(_lv_queue,), daemon=True)
    t.start()
    _lv_thread = t
    return _lv_queue


def update_live_view(env, label: str = ""):
    """
    Rendert aktuellen State und schickt Frame an Live-View-Fenster.
    Wird nach jedem Step automatisch aufgerufen wenn _lv_enabled=True.
    """
    global _lv_base
    if not _lv_enabled:
        return
    if not hasattr(env, "map_manager"):
        return
    try:
        m = _get_render_module()
        if _lv_base is None:
            _lv_base = m._make_base_image(env, None)  # Terrain wird gecacht
        frame = m._draw_frame(
            env, _lv_base,
            step_idx=0, total_steps=1,
            draw_paths=True, max_paths=800,
            action_label=label or f"t={int(env.current_time)}s",
            label_entities=True,
            show_worker_states=True,
            show_worker_targets=True,
            show_refiner_trips=True,
        )
        q = _ensure_live_view()
        try:
            q.put_nowait(frame)
        except _q.Full:
            pass  # langsamer Viewer → Frame droppen
    except Exception:
        pass  # Live-View-Fehler sollen Spiel nie unterbrechen


def toggle_live_view(env):
    """Schaltet Live-View ein/aus. Gibt neue Status-Nachricht zurueck."""
    global _lv_enabled, _lv_base
    _lv_enabled = not _lv_enabled
    if _lv_enabled:
        _lv_base = None  # Terrain bei Neustart neu generieren
        update_live_view(env, "Live-View gestartet")
        return f"{_OK}Live-View aktiviert{_R} (aktualisiert nach jedem Step)"
    else:
        return f"{_GRAY}Live-View deaktiviert{_R}"


def _format_res(resources: dict) -> str:
    # Roh- UND verarbeitete Ressourcen anzeigen
    pairs = [
        ("Holz", "HolzRoh"), ("Stein", "SteinRoh"),
        ("Lehm", "LehmRoh"), ("Eisen", "EisenRoh"),
        ("Schwefel", "SchwefelRoh"), ("Taler", "GoldRoh"),
    ]
    parts = []
    for refined, raw in pairs:
        v = resources.get(refined, 0) + resources.get(raw, 0)
        if v > 0:
            label = refined if refined != "Taler" else "Taler"
            parts.append(f"{label}:{int(v)}")
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
    parts = []
    if current_researches:
        parts.append("Aktiv: " + ", ".join(f"{r[0]}({r[1]:.0f}s)" for r in current_researches[:3]))
    if researched_techs:
        parts.append("Fertig: " + ", ".join(sorted(researched_techs)))
    return "  |  ".join(parts) if parts else "(keine)"


def show_state(env):
    """Zeigt aktuellen Game-State kompakt (4-7 Zeilen)."""
    W = 68
    bar = f"{_HEAD}{'=' * W}{_R}"
    sep = f"{_GRAY}{'-' * W}{_R}"

    # Zeile 1: Zeitstempel + Kennzahlen
    zeit  = int(env.current_time)
    mot   = getattr(env, "base_motivation", 0) * 100
    tax   = getattr(env, "current_tax_level", 2)
    faith = int(getattr(env, "faith", 0))
    alarm = getattr(env, "alarm_active", False)
    alarm_str = f"  {_WARN}[ALARM]{_R}" if alarm else ""

    # Zahltag-Countdown (startet erst nach erstem Workergebaeude)
    try:
        from environment import INCOME_CYCLE as _IC
        _fwt = getattr(env, "_first_worker_building_time", None)
        if _fwt is None:
            zahltag_str = f"  {_GRAY}Zahltag:--{_R}"
        else:
            _elapsed = env.current_time - _fwt
            _ctdwn = int(_IC - (_elapsed % _IC))
            if _ctdwn == _IC:
                _ctdwn = 0
            zahltag_str = f"  {_KEY}Zahltag{_R}:{_ctdwn}s"
    except Exception:
        zahltag_str = ""

    print(bar)
    print(f" {_BOLD}SIEDLER AI{_R}  "
          f"{_KEY}t{_R}:{zeit}/{env.max_time}s  "
          f"{_KEY}Mot{_R}:{mot:.0f}%  "
          f"{_KEY}Steu{_R}:{tax}  "
          f"{_KEY}Glb{_R}:{faith}"
          f"{zahltag_str}"
          f"{alarm_str}")
    print(bar)

    # Zeile 2: Ressourcen + Leibeigene in einer Zeile
    res_str = _format_res(env.resources)
    total   = getattr(env, "total_leibeigene", 0)
    free    = getattr(env, "free_leibeigene", 0)
    assigned = total - free
    rw = getattr(env, "resource_workers", {})
    rw_str = " ".join(
        f"{k.replace('Roh','').replace('RohRoh','Roh')}:{int(v)}"
        for k, v in rw.items() if v > 0
    )
    lei_detail = f" {_GRAY}[{rw_str}]{_R}" if rw_str else ""
    # Freie Leibeigene nach Herkunft aufschlüsseln
    n_neu  = max(0, int(getattr(env, "_pending_spawned_unassigned_serfs", 0)))
    n_bau  = max(0, int(getattr(env, "_construction_freed_serfs", 0)))
    n_idle = max(0, free - n_neu - n_bau)
    parts = []
    if n_neu  > 0: parts.append(f"{_OK}{n_neu} neu{_R}")
    if n_bau  > 0: parts.append(f"\033[36m{n_bau} von Bau{_R}")
    if n_idle > 0: parts.append(f"{_GRAY}{n_idle} idle{_R}")
    free_detail = f" ({', '.join(parts)})" if parts else ""
    # Dorfzentrum-Kapazitaet und buy_serf Diagnose
    try:
        vc_cap = env._get_total_village_capacity()
        taler  = int(env._get_total_resource("Taler") + env._get_total_resource("GoldRoh"))
        mot    = env._get_total_motivation()
        from environment import SERF_BUY_COST, soldiers_db
        # DZ-Kap zaehlt ALLE Bewohner: Leibeigene + Worker + Soldaten (mit population_cost)
        n_workers_dz = len(getattr(env, "workforce_manager", None).workers) if hasattr(env, "workforce_manager") else 0
        n_soldiers_dz = sum(
            cnt * soldiers_db.get(stype, {}).get("population_cost", 1)
            for stype, cnt in getattr(env, "soldiers", {}).items()
        ) + getattr(env, "scharfschuetzen", 0)
        dz_used = total + n_workers_dz + n_soldiers_dz
        cap_str = f"  {_KEY}DZ-Kap{_R}:{dz_used}/{vc_cap}"
        # Blockade-Hinweis
        if dz_used >= vc_cap:
            cap_str += f" {_WARN}[VOLL]{_R}"
        elif taler < SERF_BUY_COST:
            cap_str += f" {_WARN}[Taler<{SERF_BUY_COST}]{_R}"
    except Exception:
        cap_str = ""
    print(f" {_KEY}RES{_R} {res_str}   "
          f"{_KEY}LEI{_R} {_OK}{free}{_R}/{total} frei{free_detail}{lei_detail}{cap_str}")

    # Zeile 3: Gebaeude
    print(f" {_KEY}GEB{_R} {_format_buildings(env.buildings)}")

    # Zeile 4: Militaer
    soldiers = getattr(env, "soldiers", {})
    scharf   = getattr(env, "scharfschuetzen", 0)
    print(f" {_KEY}MIL{_R} {_format_soldiers(soldiers, scharf)}")

    # Optional: Baustellen / Upgrades / Forschung (nur wenn aktiv)
    sites = getattr(env, "construction_sites", [])
    uq    = getattr(env, "upgrade_queue", [])
    cr    = getattr(env, "current_researches", [])
    rt    = getattr(env, "researched_techs", set())
    if sites:
        site_str = "  ".join(
            f"{s.get('building','?')}({s.get('remaining_work',0):.0f}s)"
            for s in sites[:4]
        ) + (f" +{len(sites)-4}" if len(sites) > 4 else "")
        print(f" {_KEY}BAU{_R} {site_str}")
    if uq:
        print(f" {_KEY}UPG{_R} " + "  ".join(f"{item[1]}({item[2]:.0f}s)" for item in uq[:4]))
    if cr:
        active_str = "  ".join(f"{r[0]}({r[1]:.0f}s)" for r in cr[:3])
        done_str   = (f"  Fertig:{','.join(sorted(rt))}") if rt else ""
        print(f" {_KEY}FOR{_R} {active_str}{done_str}")

    print(sep)


def get_action_names(env) -> list:
    """
    Gibt Liste von (index, name, enabled) fuer die aktuelle Phase zurueck.
    """
    from environment import (
        ActionPhase, MAIN_ACTIONS, QUANTITY_VALUES, RESEARCH_BUILDINGS,
        SOURCE_CATEGORIES, TARGET_CATEGORIES, TAX_LEVELS, BLESS_CATEGORIES,
    )

    MAIN_NAMES_DE = {
        "wait": "Warten", "upgrade": "Upgraden", "research": "Forschen",
        "recruit": "Rekrutieren", "buy_serf": "Leibeig. kaufen",
        "dismiss_serf": "Leibeig. entlassen", "assign_serf": "Leibeig. zuweisen",
        "demolish": "Abreissen", "bless": "Segnen", "tax": "Steuer", "alarm": "Alarm",
    }

    phase = env.current_phase
    mask = env.action_masks()

    # Maske ist auf max_action_size gepadded — wir nehmen nur die relevante Laenge
    n = env.action_spaces[phase].n
    phase_mask = mask[:n]

    options = []

    if phase == ActionPhase.MAIN:
        for i, name in enumerate(MAIN_ACTIONS):
            enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
            options.append((i, MAIN_NAMES_DE.get(name, name), enabled))

    elif phase == ActionPhase.BUILDING:
        from environment import buildings_db
        flow = getattr(env, "current_flow", None)
        if flow == "upgrade":
            blist = env.upgradeable_buildings
        else:
            blist = env.demolishable_buildings
        bpm = getattr(env, "building_position_map", {})
        for i in range(n):
            bname = blist[i] if i < len(blist) else f"Gebaeude_{i}"
            enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
            # Kosten anzeigen
            binfo = buildings_db.get(bname, {})
            if flow == "upgrade":
                cost = binfo.get("upgrade_cost", {})
                t = binfo.get("upgrade_time", 0)
            else:
                cost = binfo.get("cost", {})
                t = binfo.get("build_time", 0)
            cost_str = " ".join(f"{k}:{int(v)}" for k, v in cost.items()) if cost else ""
            # Position(en) aus building_position_map
            matching = [(k, v) for k, v in bpm.items()
                        if k == bname or k.startswith(bname + "_")]
            if matching:
                pos_parts = [f"({int(v['x'])},{int(v['y'])})" for _, v in matching[:3]]
                pos_str = " " + " ".join(pos_parts)
            else:
                pos_str = ""
            if cost_str:
                label = f"{bname}{pos_str}  [{cost_str} {t:.0f}s]"
            else:
                label = f"{bname}{pos_str}"
            options.append((i, label, enabled))

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
        tgt_cat = env.pending_selections.get(ActionPhase.TARGET_CATEGORY, -1)

        # Aktive Kategorie bestimmen
        if phase == ActionPhase.SOURCE_SPECIFIC:
            sel_cat = env.pending_selections.get(ActionPhase.SOURCE_CATEGORY, -1)
        else:
            sel_cat = tgt_cat

        if phase == ActionPhase.TARGET_SPECIFIC and sel_cat == 7:
            # Neubau: TARGET_SPECIFIC = Gebaeude auswaehlen (index → buildable_buildings)
            from environment import buildings_db
            blist = env.buildable_buildings
            for i in range(n):
                enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
                bname = blist[i] if i < len(blist) else f"Gebaeude_{i}"
                binfo = buildings_db.get(bname, {})
                cost = binfo.get("cost", {})
                t = binfo.get("build_time", 0)
                cost_str = " ".join(f"{k}:{int(v)}" for k, v in cost.items()) if cost else ""
                label = f"{bname}  [{cost_str} {t:.0f}s]" if cost_str else bname
                options.append((i, label, enabled))

        elif sel_cat == 0:
            # Frei-Pool: nur Index 0 — free_leibeigene ist immer aktuell (serf_areas kann veraltet sein)
            enabled = bool(phase_mask[0]) if len(phase_mask) > 0 else False
            free_count = getattr(env, "free_leibeigene", 0)
            n_neu  = max(0, int(getattr(env, "_pending_spawned_unassigned_serfs", 0)))
            n_bau  = max(0, int(getattr(env, "_construction_freed_serfs", 0)))
            n_idle = max(0, free_count - n_neu - n_bau)
            detail_parts = []
            if n_neu  > 0: detail_parts.append(f"{n_neu} neu")
            if n_bau  > 0: detail_parts.append(f"{n_bau} von Bau")
            if n_idle > 0: detail_parts.append(f"{n_idle} idle")
            detail = f" [{', '.join(detail_parts)}]" if detail_parts else ""
            options.append((0, f"Frei-Pool ({free_count} verfuegbar{detail})", enabled))

        elif sel_cat == 1:
            # Holz: index → tree_list_internal[i]
            trees = getattr(env, "tree_list_internal", [])
            for i in range(min(n, len(trees))):
                enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
                if not enabled:
                    continue  # nur verfuegbare Baeume zeigen
                t = trees[i]
                rem = int(t.get("resource_remaining", t.get("remaining_wood", 0)))
                assigned = int(t.get("serfs_assigned", 0))
                tx, ty = int(t.get("x", 0)), int(t.get("y", 0))
                options.append((i, f"Baum{i} @({tx},{ty}) [{rem}Holz {assigned}L]", enabled))

        elif sel_cat == 6:
            # Baustelle: index → construction_sites[i]
            sites = getattr(env, "construction_sites", [])
            for i, site in enumerate(sites[:n]):
                enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
                bname = site.get("building", f"Baustelle_{i}")
                rem = site.get("remaining_work", 0)
                s_assigned = site.get("serfs_assigned", 0)
                options.append((i, f"{bname} ({rem:.0f}s verbl., {s_assigned}L)", enabled))
            if not sites:
                options.append((0, "(keine Baustellen)", False))

        elif sel_cat in (2, 3, 4, 5):
            # Mineralien: index = Position in CATEGORY_AREA_MAP[cat] — NICHT in serf_areas!
            from environment import CATEGORY_AREA_MAP
            SERF_AREA_DE = {
                "SHAFT_IRON_1":   "Eisen-Vork.1",   "SHAFT_IRON_2":   "Eisen-Vork.2",
                "SHAFT_IRON_3":   "Eisen-Vork.3",   "SHAFT_STONE_1":  "Stein-Vork.1",
                "SHAFT_STONE_2":  "Stein-Vork.2",   "SHAFT_STONE_3":  "Stein-Vork.3",
                "SHAFT_CLAY_1":   "Lehm-Vork.1",    "SHAFT_CLAY_2":   "Lehm-Vork.2",
                "SHAFT_CLAY_3":   "Lehm-Vork.3",    "SHAFT_SULFUR_1": "Schwefel-Vork.1",
                "SHAFT_SULFUR_2": "Schwefel-Vork.2", "SHAFT_SULFUR_3": "Schwefel-Vork.3",
                "DEPOSIT_IRON_1":   "Eisen-Mine.1",   "DEPOSIT_IRON_2":   "Eisen-Mine.2",
                "DEPOSIT_STONE_1":  "Stein-Mine.1",   "DEPOSIT_STONE_2":  "Stein-Mine.2",
                "DEPOSIT_CLAY_1":   "Lehm-Mine.1",
                "DEPOSIT_SULFUR_1": "Schwefel-Mine.1", "DEPOSIT_SULFUR_2": "Schwefel-Mine.2",
            }
            _DE_EN = {"Eisen": "IRON", "Stein": "STONE", "Lehm": "CLAY", "Schwefel": "SULFUR"}
            # Koordinaten aufbauen
            _coords: dict = {}
            for _cat, _cd in getattr(env, "shaft_categories", {}).items():
                _en = _DE_EN.get(_cat, _cat.upper())
                for _idx, _sh in enumerate(_cd.get("shafts", []), start=1):
                    _coords[f"SHAFT_{_en}_{_idx}"] = (int(_sh.get("x", 0)), int(_sh.get("y", 0)))
                    _coords[f"SHAFT_{_en}_{_idx}_rem"] = int(_sh.get("remaining", 0))
            for _cat, _cd in getattr(env, "deposit_categories", {}).items():
                _en = _DE_EN.get(_cat, _cat.upper())
                for _idx, _dp in enumerate(_cd.get("deposits", []), start=1):
                    _coords[f"DEPOSIT_{_en}_{_idx}"] = (int(_dp.get("x", 0)), int(_dp.get("y", 0)))
                    _coords[f"DEPOSIT_{_en}_{_idx}_rem"] = int(_dp.get("remaining", 0))
            # Serf-counts aus serf_areas
            serf_areas = getattr(env, "serf_areas", {})
            serf_count = {area.name: data.get("count", 0) for area, data in serf_areas.items()}

            cat_areas = CATEGORY_AREA_MAP.get(sel_cat, [])
            for i, area in enumerate(cat_areas):
                enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
                akey  = area.name
                aname = SERF_AREA_DE.get(akey, akey)
                cnt   = serf_count.get(akey, 0)
                coord = _coords.get(akey)
                rem   = _coords.get(akey + "_rem", "?")
                pos_str = f" @({coord[0]},{coord[1]})" if coord else ""
                options.append((i, f"{aname} ({cnt}L, {rem} verbl.){pos_str}", enabled))

        else:
            # Unbekannte Kategorie: alle Optionen zeigen
            for i in range(n):
                enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
                options.append((i, f"Option {i}", enabled))

    elif phase in (ActionPhase.POSITION_GROUP, ActionPhase.POSITION_INDEX):
        # Versuche echte Positions-Namen zu zeigen
        from environment import POSITION_GROUP_SIZE
        try:
            building_idx = env.pending_selections.get(ActionPhase.BUILDING, 0)
            building = env._get_position_phase_building(building_idx)
            if building and env.current_flow == "assign_serf":
                candidates = env._get_build_position_candidates(building)
            elif building:
                keys = env._get_building_instance_keys(building)
                candidates = [{"x": 0, "y": 0, "_key": k} for k in keys]
            else:
                candidates = []
        except Exception:
            candidates = []

        if phase == ActionPhase.POSITION_GROUP:
            for i in range(n):
                enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
                start = i * POSITION_GROUP_SIZE
                end = min(start + POSITION_GROUP_SIZE, len(candidates))
                if candidates and start < len(candidates):
                    c = candidates[start]
                    if "_key" in c:
                        label = c["_key"]
                    else:
                        label = f"({int(c['x'])},{int(c['y'])})"
                    if end - start > 1:
                        label += f" ..+{end-start-1}"
                else:
                    label = f"Gruppe {i}"
                options.append((i, label, enabled))
        else:  # POSITION_INDEX
            group_idx = env.pending_selections.get(ActionPhase.POSITION_GROUP, 0)
            for i in range(n):
                enabled = bool(phase_mask[i]) if i < len(phase_mask) else False
                global_idx = group_idx * POSITION_GROUP_SIZE + i
                if candidates and global_idx < len(candidates):
                    c = candidates[global_idx]
                    if "_key" in c:
                        label = c["_key"]
                    else:
                        label = f"Pos {i}: ({int(c['x'])},{int(c['y'])})"
                else:
                    label = f"Position {i}"
                options.append((i, label, enabled))

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
    flow  = getattr(env, "current_flow", None)

    W = 64
    phase_label = phase.value.upper()
    flow_label  = f"  {_GRAY}({flow}){_R}" if flow and phase != ActionPhase.MAIN else ""
    print(f"  {_KEY}PHASE:{_R} {_BOLD}{phase_label}{_R}{flow_label}")
    print(f"{_GRAY}{'-' * W}{_R}")

    options = get_action_names(env)
    enabled_options  = [(i, name) for i, name, ok in options if ok]
    disabled_options = [(i, name) for i, name, ok in options if not ok]

    if not enabled_options:
        print(f"  {_WARN}(keine Aktionen verfuegbar){_R}")
        return

    # Verfuegbare Aktionen in 2 Spalten (farbig gruen)
    col_w = 30
    for j in range(0, len(enabled_options), 2):
        li, ln = enabled_options[j]
        left_str = f"  {_OK}[{li:>2}]{_R} {ln}"
        # Sichtbare Laenge ohne ANSI-Codes fuer Ausrichtung berechnen
        visible_left = f"  [{li:>2}] {ln}"
        pad = col_w - len(visible_left)
        if j + 1 < len(enabled_options):
            ri, rn = enabled_options[j + 1]
            right_str = f"{_OK}[{ri:>2}]{_R} {rn}"
            print(f"{left_str}{' ' * max(1, pad)}  {right_str}")
        else:
            print(left_str)

    # Deaktivierte Aktionen kompakt grau
    if disabled_options and len(disabled_options) <= 20:
        dis_str = "  ".join(f"{_GRAY}[{i}]{_R}" for i, _ in disabled_options[:12])
        print(f"\n  Gesperrt: {dis_str}")

    print(f"{_GRAY}{'-' * W}{_R}")


def get_map_highlights(env) -> list:
    """
    Gibt Liste von (x, y, label) World-Koordinaten zurueck, die auf der Karte
    hervorgehoben werden sollen — je nach aktueller Aktions-Phase.
    label ist 1 Zeichen (Aktions-Index 0-9 = '0'-'9', 10+ = 'A','B',...).
    """
    from environment import ActionPhase, CATEGORY_AREA_MAP

    def _lbl(i):
        return str(i) if i < 10 else chr(ord('A') + i - 10)

    def _mask_ok(phase_mask, i):
        return bool(phase_mask[i]) if i < len(phase_mask) else False

    highlights = []
    phase = env.current_phase

    try:
        n = env.action_spaces[phase].n
        mask = env.action_masks()
        phase_mask = mask[:n]
    except Exception:
        return []

    # ── POSITION_GROUP / POSITION_INDEX: Baupositionen mit Aktionsnummer ────
    if phase in (ActionPhase.POSITION_GROUP, ActionPhase.POSITION_INDEX):
        from environment import POSITION_GROUP_SIZE
        try:
            building_idx = env.pending_selections.get(ActionPhase.BUILDING, 0)
            building = env._get_position_phase_building(building_idx)
            if building:
                candidates = env._get_build_position_candidates(building)
                if phase == ActionPhase.POSITION_GROUP:
                    for i in range(n):
                        if not _mask_ok(phase_mask, i):
                            continue
                        start = i * POSITION_GROUP_SIZE
                        if start < len(candidates):
                            c = candidates[start]
                            highlights.append((float(c["x"]), float(c["y"]), _lbl(i)))
                else:  # POSITION_INDEX
                    group_idx = env.pending_selections.get(ActionPhase.POSITION_GROUP, 0)
                    start = group_idx * POSITION_GROUP_SIZE
                    for i in range(n):
                        if not _mask_ok(phase_mask, i):
                            continue
                        ci = start + i
                        if ci < len(candidates):
                            c = candidates[ci]
                            highlights.append((float(c["x"]), float(c["y"]), _lbl(i)))
        except Exception:
            pass

    # ── BUILDING: Upgrade/Abreissen → vorhandene Gebaeude mit Aktionsnummer ─
    elif phase == ActionPhase.BUILDING:
        flow = getattr(env, "current_flow", None)
        if flow in ("upgrade", "demolish"):
            blist = getattr(env, "upgradeable_buildings" if flow == "upgrade"
                            else "demolishable_buildings", [])
            bpm = getattr(env, "building_position_map", {})
            for i in range(n):
                if not _mask_ok(phase_mask, i):
                    continue
                bname = blist[i] if i < len(blist) else None
                if not bname:
                    continue
                for k, pos in bpm.items():
                    if k == bname or k.startswith(bname + "_"):
                        highlights.append((float(pos["x"]), float(pos["y"]), _lbl(i)))
                        break

    # ── TECH_BUILDING: Forschungsgebaeude auf Karte zeigen ───────────────────
    elif phase == ActionPhase.TECH_BUILDING:
        from environment import RESEARCH_BUILDINGS
        bpm = getattr(env, "building_position_map", {})
        for i, bname in enumerate(RESEARCH_BUILDINGS):
            if i >= n or not _mask_ok(phase_mask, i):
                continue
            base = bname.split("_")[0]
            for k, pos in bpm.items():
                if k.startswith(base):
                    highlights.append((float(pos["x"]), float(pos["y"]), _lbl(i)))
                    break

    # ── SOURCE_SPECIFIC / TARGET_SPECIFIC ────────────────────────────────────
    elif phase in (ActionPhase.SOURCE_SPECIFIC, ActionPhase.TARGET_SPECIFIC):
        sel_cat = env.pending_selections.get(
            ActionPhase.SOURCE_CATEGORY if phase == ActionPhase.SOURCE_SPECIFIC
            else ActionPhase.TARGET_CATEGORY, -1)

        if phase == ActionPhase.TARGET_SPECIFIC and sel_cat == 7:
            # Neubau Schritt 2: Gebaeude gewaehlt → Baupositionen zeigen
            tgt_spec = env.pending_selections.get(ActionPhase.TARGET_SPECIFIC, -1)
            if tgt_spec >= 0:
                try:
                    blist = env.buildable_buildings
                    if tgt_spec < len(blist):
                        for c in env._get_build_position_candidates(blist[tgt_spec]):
                            highlights.append((float(c["x"]), float(c["y"]), "!"))
                except Exception:
                    pass
            else:
                # Gebaeude-Auswahl: Baupositionen aller verfuegbaren Gebaeude
                blist = getattr(env, "buildable_buildings", [])
                for i in range(min(n, len(blist))):
                    if not _mask_ok(phase_mask, i):
                        continue
                    try:
                        cands = env._get_build_position_candidates(blist[i])
                        for c in cands[:1]:
                            highlights.append((float(c["x"]), float(c["y"]), _lbl(i)))
                    except Exception:
                        pass

        elif sel_cat == 1:
            # Holz: Baum-Positionen
            trees = getattr(env, "tree_list_internal", [])
            for i in range(min(n, len(trees))):
                if not _mask_ok(phase_mask, i):
                    continue
                t = trees[i]
                highlights.append((float(t.get("x", 0)), float(t.get("y", 0)), _lbl(i)))

        elif sel_cat == 6:
            # Baustellen
            sites = getattr(env, "construction_sites", [])
            for i, site in enumerate(sites[:n]):
                if not _mask_ok(phase_mask, i):
                    continue
                sx = site.get("x") or site.get("pos_x")
                sy = site.get("y") or site.get("pos_y")
                if sx is None:
                    bpos = env.building_position_map.get(site.get("building", ""))
                    if bpos:
                        sx, sy = bpos["x"], bpos["y"]
                if sx is not None:
                    highlights.append((float(sx), float(sy), _lbl(i)))

        elif sel_cat in (2, 3, 4, 5):
            # Mineralien: Stollen + Minen mit Aktionsnummer
            _DE_EN = {"Eisen": "IRON", "Stein": "STONE", "Lehm": "CLAY", "Schwefel": "SULFUR"}
            _coords: dict = {}
            for _cat, _cd in getattr(env, "shaft_categories", {}).items():
                _en = _DE_EN.get(_cat, _cat.upper())
                for _idx, _sh in enumerate(_cd.get("shafts", []), start=1):
                    _coords[f"SHAFT_{_en}_{_idx}"] = (float(_sh.get("x", 0)), float(_sh.get("y", 0)))
            for _cat, _cd in getattr(env, "deposit_categories", {}).items():
                _en = _DE_EN.get(_cat, _cat.upper())
                for _idx, _dp in enumerate(_cd.get("deposits", []), start=1):
                    _coords[f"DEPOSIT_{_en}_{_idx}"] = (float(_dp.get("x", 0)), float(_dp.get("y", 0)))
            cat_areas = CATEGORY_AREA_MAP.get(sel_cat, [])
            for i, area in enumerate(cat_areas):
                if not _mask_ok(phase_mask, i):
                    continue
                coord = _coords.get(area.name)
                if coord:
                    highlights.append((coord[0], coord[1], _lbl(i)))

    return highlights


def show_map(env, compact=False, highlights=None):
    """Zeigt ASCII-Karte mit Gebaeuden, Baeumen und Arbeitern."""
    # Feste Weltgrenzen aus dem Walkable-Grid (754×747 Pixel, Scale 33.5/33.8, Offset 25240/0)
    # → Welt ist exakt quadratisch (25259 × 25249 World-Units)
    WORLD_MIN_X, WORLD_MAX_X = 25240.0, 25240.0 + 754 * 33.5   # ≈ 50499
    WORLD_MIN_Y, WORLD_MAX_Y = 0.0,     747 * 33.8               # ≈ 25249
    range_x = WORLD_MAX_X - WORLD_MIN_X
    range_y = WORLD_MAX_Y - WORLD_MIN_Y

    # Groesse: Welt ist quadratisch → MAP_W = MAP_H * 2.0 (Terminal-Chars 2:1)
    MAP_H = 20 if compact else 50
    MAP_W = int(MAP_H * (range_x / range_y) * 2.0)  # ≈ 40 kompakt / 100 voll

    # Zeichen-Prioritaet: hoehere Zahl ueberschreibt niedrigere
    points = []  # (x, y, char, priority)

    # Baeume (noch vorhanden)
    for tree in env.tree_list_internal:
        if tree.get("remaining_wood", 1) > 0:
            points.append((float(tree["x"]), float(tree["y"]), "t", 1))

    # Arbeiter (workforce_manager: Holzfaeller, Minenarbeiter etc.)
    wm = getattr(env, "workforce_manager", None)
    if wm:
        for w in getattr(wm, "workers", []):
            pos = getattr(w, "position", None)
            if pos is not None:
                points.append((float(pos.x), float(pos.y), "w", 2))

    # Leibeigene (production_system.serfs: laufen zu Ressourcen/Baustellen)
    ps = getattr(env, "production_system", None)
    if ps:
        for serf in getattr(ps, "serfs", []):
            pos = getattr(serf, "position", None)
            if pos is not None:
                points.append((float(pos.x), float(pos.y), "p", 2))

    # Unbebaute DZ-Slots ('d')
    for slot in getattr(env, "dz_slots", []):
        if slot.get("status") != "built":
            points.append((float(slot["x"]), float(slot["y"]), "d", 2))

    # Vorkommen / Mine-Bauplätze (kleine Buchstaben = noch nicht gebaut)
    mine_positions = getattr(env, "mine_positions", {})
    vork_chars = {"Eisenmine": "i", "Steinmine": "s", "Lehmmine": "l", "Schwefelmine": "f"}
    for mtype, slot_list in mine_positions.items():
        ch = vork_chars.get(mtype, "v")
        for mpos in slot_list:
            points.append((float(mpos["x"]), float(mpos["y"]), ch, 2))

    # Stollen (Schaechte) aus map_config
    try:
        from map_config_wintersturm import PLAYER_1_MINE_SHAFTS
        shaft_chars = {"Eisenmine": "e", "Steinmine": "q", "Lehmmine": "a", "Schwefelmine": "g"}
        for mtype, shafts in PLAYER_1_MINE_SHAFTS.items():
            ch = shaft_chars.get(mtype, "x")
            for shaft in shafts:
                points.append((float(shaft["x"]), float(shaft["y"]), ch, 2))
    except Exception:
        pass

    # Gebaute Minen (Grossbuchstaben = fertig gebaut)
    mine_chars = {"Steinmine": "S", "Eisenmine": "I", "Lehmmine": "L", "Schwefelmine": "V"}
    for mine_type, mine_list in env.built_mines.items():
        ch = mine_chars.get(mine_type, "M")
        for mpos in mine_list:
            points.append((float(mpos["x"]), float(mpos["y"]), ch, 4))

    # Baustellen ('b' = in Bau, noch nicht fertig)
    for site in getattr(env, "construction_sites", []):
        sx = site.get("x") or site.get("pos_x")
        sy = site.get("y") or site.get("pos_y")
        if sx is None:
            # Versuche Position aus building_position_map
            bname = site.get("building", "")
            bpos = env.building_position_map.get(bname)
            if bpos:
                sx, sy = bpos["x"], bpos["y"]
        if sx is not None and sy is not None:
            points.append((float(sx), float(sy), "b", 3))

    # Gebaeude aus building_position_map (fertig gebaut)
    bldg_chars = {
        "Hauptquartier": "H", "Dorfzentrum": "D", "Wohnhaus": "W",
        "Holzfaeller": "F", "Saegewerk": "Z", "Hochschule": "O",
        "Schmiede": "C", "Kloster": "K", "Waffenschmiede": "A",
        "Steinbruch": "B", "Lehmgrube": "G", "Eisenhuette": "E",
        "Schwefelhuette": "X", "Kaserne": "R", "Schiesstand": "U",
        "Speicher": "P", "Dorfschule": "Y", "Muehle": "N",
        "Taverne": "T", "Krankenhaus": "J", "Markt": "Q",
    }
    for key, pos in env.building_position_map.items():
        btype = key.split("_")[0]
        ch = bldg_chars.get(btype, btype[0].upper())
        priority = 6 if btype in ("Hauptquartier", "Dorfzentrum") else 5
        points.append((float(pos["x"]), float(pos["y"]), ch, priority))

    # Feste Bounds — kein auto-detect, damit Karte immer gleich aussieht
    min_x, max_x = WORLD_MIN_X, WORLD_MAX_X
    min_y, max_y = WORLD_MIN_Y, WORLD_MAX_Y

    # Grid befuellen
    grid = [["." for _ in range(MAP_W)] for _ in range(MAP_H)]

    # Sortiert nach Prioritaet (niedrig zuerst, hoch ueberschreibt)
    points.sort(key=lambda p: p[3])
    for x, y, ch, _pri in points:
        col = int((x - min_x) / range_x * (MAP_W - 1))
        row = int((y - min_y) / range_y * (MAP_H - 1))
        col = max(0, min(MAP_W - 1, col))
        row = max(0, min(MAP_H - 1, row))
        grid[row][col] = ch

    # Highlight-Zellen berechnen: dict (row,col) → label-char
    hl_cells: dict = {}
    if highlights:
        for hl in highlights:
            hx, hy, lbl = hl if len(hl) == 3 else (*hl, "!")
            col = int((hx - min_x) / range_x * (MAP_W - 1))
            row = int((hy - min_y) / range_y * (MAP_H - 1))
            col = max(0, min(MAP_W - 1, col))
            row = max(0, min(MAP_H - 1, row))
            if (row, col) not in hl_cells:  # erstes Label gewinnt
                hl_cells[(row, col)] = lbl

    # Ausgabe mit Farben
    border_color = _GRAY
    print(f"{border_color}+{'-' * MAP_W}+{_R}")
    for r_idx, row in enumerate(grid):
        colored = ""
        for c_idx, ch in enumerate(row):
            if (r_idx, c_idx) in hl_cells:
                # Hervorgehobene Zelle: Aktionsnummer auf gelbem Hintergrund
                colored += _HL + hl_cells[(r_idx, c_idx)] + _R
            else:
                color = _C.get(ch, _C_BLDG)
                colored += color + ch + _R
        print(f"{border_color}|{_R}{colored}{border_color}|{_R}")
    print(f"{border_color}+{'-' * MAP_W}+{_R}")

    # Legende kompakt
    trees_alive = sum(1 for t in env.tree_list_internal if t.get("remaining_wood", 1) > 0)
    n_workers   = len(getattr(wm, "workers", [])) if wm else 0
    n_serfs     = len(getattr(ps, "serfs", [])) if ps else 0
    mines_built = sum(len(v) for v in env.built_mines.values())
    n_bldg      = len(env.building_position_map)
    n_sites     = len(getattr(env, "construction_sites", []))
    hl_hint     = f"  {_HL}0{_R}=Aktionsnr." if hl_cells else ""
    leg_parts = [
        f"{_C['H']}H{_R}=HQ", f"{_C['D']}D{_R}=DZ",
        f"{_C_BLDG}*{_R}=Geb", f"{_C['b']}b{_R}=Bau",
        f"{_C['t']}t{_R}=Holz", f"{_C['w']}w{_R}=Arb", f"{_C['p']}p{_R}=Lei",
        f"{_C['i']}i{_R}=Ei-Stln", f"{_C['e']}e{_R}=Ei-Vork",
        f"{_C['s']}s{_R}=St-Stln", f"{_C['q']}q{_R}=St-Vork",
        f"{_C['l']}l{_R}=Le-Stln", f"{_C['f']}f{_R}=Sw-Stln",
        f"{_GRAY}[{trees_alive}B {n_workers}A {n_serfs}L {mines_built}M {n_bldg}G]{_R}",
    ]
    print("  " + "  ".join(leg_parts) + hl_hint)


def _wintersturm_start(env):
    """Spielmodus startet mit 0 Leibeigenen — muessen erst gekauft werden."""
    env.total_leibeigene = 0
    env.free_leibeigene = 0
    for area in env.serf_areas:
        env.serf_areas[area]["count"] = 0
    env.production_system.serfs.clear()


def play():
    """Hauptloop des interaktiven Spielmodus."""
    print("Lade Environment...")
    from environment import SiedlerScharfschuetzenEnv

    env = SiedlerScharfschuetzenEnv(player_id=1, use_spatial_obs=False)
    obs, _ = env.reset(seed=0)
    _wintersturm_start(env)

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
            rw_val = last_info.get("step_reward", 0)
            rw_color = _OK if rw_val >= 0 else _WARN
            print(f"  {_GRAY}Step #{step_count}:{_R} {_KEY}{last_action_name}{_R}"
                  f"  {rw_color}{rw_val:+.4f}{_R}  Gesamt:{total_reward:.3f}")
            if last_info.get("blocked_invalid_action"):
                print(f"  {_WARN}!!! Ungueltige Aktion — ignoriert !!!{_R}")

        show_map(env, compact=True, highlights=get_map_highlights(env))
        show_actions(env)

        # Eingabe
        try:
            lv_hint = f"{_OK}v=Bild[AN]{_R}" if _lv_enabled else f"{_GRAY}v=Bild[aus]{_R}"
            raw = input(
                f"\n  {_BOLD}Aktion{_R} (Nr  {_GRAY}q=Ende  r=Reset  w=Warten  m=Karte{_R}  {lv_hint}): "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBeendet.")
            break

        if raw.lower() == "q":
            print(f"\nSpiel beendet nach {step_count} Steps. Gesamt-Reward: {total_reward:.3f}")
            break

        if raw.lower() == "m":
            show_map(env, compact=False, highlights=get_map_highlights(env))
            input("Enter druecken...")
            continue

        if raw.lower() == "v":
            msg = toggle_live_view(env)
            print(f"  {msg}")
            continue

        if raw.lower() == "r":
            obs, _ = env.reset()
            _wintersturm_start(env)
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
        from environment import MAIN_ACTIONS, ActionPhase
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

        # Auto-Skip: Wenn naechste Phase nur 1 Option hat, automatisch waehlen
        while info.get("multi_step") and env.current_phase in (
            ActionPhase.POSITION_GROUP, ActionPhase.POSITION_INDEX
        ):
            auto_mask = env.action_masks()
            auto_n = env.action_spaces[env.current_phase].n
            enabled = [i for i in range(auto_n) if auto_mask[i]]
            if len(enabled) == 1:
                auto_a = enabled[0]
                print(f"  [Auto] {env.current_phase.value}: nur Option {auto_a} verfuegbar — automatisch gewaehlt")
                obs, reward, terminated, truncated, info = env.step(auto_a)
                total_reward += reward
                step_count += 1
                last_info = info
            else:
                break  # Mehrere Optionen -> User muss waehlen

        # Live-View nach jedem abgeschlossenen Schritt aktualisieren
        update_live_view(env, last_action_name)

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
            _wintersturm_start(env)
            total_reward = 0.0
            step_count = 0
            last_info = {}
            last_action_name = "—"



# ---------------------------------------------------------------------------
# ANSI-Code-Stripper fuer Tkinter-Textwidget
# ---------------------------------------------------------------------------
import re as _re
_ANSI_RE = _re.compile(r"\033\[[0-9;]*m")

def _strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


# ---------------------------------------------------------------------------
# Vollstaendige Tkinter-UI: Karte links, State+Aktionen rechts, Input unten
# ---------------------------------------------------------------------------
def play_ui():
    """Spiel mit integrierter Tkinter-GUI (Karte + Befehle in einem Fenster)."""
    import io
    import tkinter as tk
    from tkinter import font as tkfont
    try:
        from PIL import Image as _PIL, ImageTk
    except ImportError:
        print("Pillow nicht installiert — fallback auf Terminal-Modus.")
        play()
        return

    # --- Queues fuer Thread-Kommunikation ---
    _map_q   = _q.Queue(maxsize=2)   # map-frames (numpy) vom Game-Thread → UI
    _text_q  = _q.Queue(maxsize=4)   # state-text vom Game-Thread → UI
    _input_q = _q.Queue(maxsize=1)   # Eingabe vom UI → Game-Thread

    _shutdown = _thr.Event()

    # --- Tkinter-Fenster aufbauen ---
    root = tk.Tk()
    root.title("Siedler AI — Interaktiv")
    root.configure(bg="#111")
    root.minsize(1024, 640)
    _apply_window_geometry(root, 1280, 760, anchor="center", margin=28)
    root.resizable(True, True)

    # Linke Haelfte: Karte
    map_frame = tk.Frame(root, bg="#111")
    map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    map_lbl = tk.Label(map_frame, bg="#111")
    map_lbl.pack(fill=tk.BOTH, expand=True)
    _map_ref = [None]

    # Rechte Haelfte: State + Aktionen + Input
    right_frame = tk.Frame(root, bg="#1a1a1a", width=480)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
    right_frame.pack_propagate(False)

    mono = tkfont.Font(family="Consolas", size=9)

    text_box = tk.Text(
        right_frame, bg="#1a1a1a", fg="#d4d4d4",
        font=mono, wrap=tk.WORD, state=tk.DISABLED,
        borderwidth=0, highlightthickness=0,
        selectbackground="#333",
    )
    scroll = tk.Scrollbar(right_frame, command=text_box.yview, bg="#333")
    text_box.configure(yscrollcommand=scroll.set)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    text_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Eingabe-Zeile
    input_frame = tk.Frame(right_frame, bg="#222")
    input_frame.pack(side=tk.BOTTOM, fill=tk.X)
    tk.Label(input_frame, text=">", bg="#222", fg="#0f0",
             font=mono).pack(side=tk.LEFT, padx=4)
    entry = tk.Entry(input_frame, bg="#111", fg="#0f0", font=mono,
                     insertbackground="#0f0", borderwidth=0)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=4)
    entry.focus_set()

    hint_lbl = tk.Label(input_frame, text="Nr | q=Ende | r=Reset | w=Wait | Esc=Schliessen",
                        bg="#222", fg="#555", font=("Consolas", 8))
    hint_lbl.pack(side=tk.RIGHT, padx=6)

    def _submit(_event=None):
        cmd = entry.get().strip()
        entry.delete(0, tk.END)
        if cmd:
            try:
                _input_q.put_nowait(cmd)
            except _q.Full:
                pass

    def _request_close():
        if _shutdown.is_set():
            return
        _shutdown.set()
        try:
            while True:
                _input_q.get_nowait()
        except _q.Empty:
            pass
        try:
            _input_q.put_nowait("q")
        except _q.Full:
            pass
        try:
            root.destroy()
        except tk.TclError:
            pass

    root.protocol("WM_DELETE_WINDOW", _request_close)
    root.bind("<Escape>", lambda _event: _request_close())
    entry.bind("<Return>", _submit)

    # --- Farb-Tags fuer Tkinter-Text ---
    text_box.tag_configure("green",  foreground="#4ec94e")
    text_box.tag_configure("red",    foreground="#f55")
    text_box.tag_configure("yellow", foreground="#e8c43a")
    text_box.tag_configure("cyan",   foreground="#5dd")
    text_box.tag_configure("gray",   foreground="#666")
    text_box.tag_configure("bold",   font=tkfont.Font(family="Consolas", size=9, weight="bold"))
    text_box.tag_configure("head",   foreground="#e8c43a",
                           font=tkfont.Font(family="Consolas", size=9, weight="bold"))

    def _update_text(raw: str):
        """Setzt Text im State-Panel (ANSI-Codes werden entfernt)."""
        plain = _strip_ansi(raw)
        text_box.configure(state=tk.NORMAL)
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, plain)
        text_box.configure(state=tk.DISABLED)
        text_box.see(tk.END)

    def _update_map(frame):
        """Zeigt neuen Karten-Frame im linken Panel."""
        img = _PIL.fromarray(frame)
        w = map_frame.winfo_width() or 900
        h = map_frame.winfo_height() or 720
        img.thumbnail((w, h), _PIL.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        map_lbl.config(image=photo)
        _map_ref[0] = photo

    def _poll():
        """Pollt beide Queues und aktualisiert UI (laeuft im Tkinter-Thread)."""
        if _shutdown.is_set() or not root.winfo_exists():
            return
        try:
            while True:
                frame = _map_q.get_nowait()
                _update_map(frame)
        except _q.Empty:
            pass
        try:
            while True:
                txt = _text_q.get_nowait()
                _update_text(txt)
        except _q.Empty:
            pass
        try:
            root.after(120, _poll)
        except tk.TclError:
            pass

    root.after(120, _poll)

    # --- Game-Thread ---
    def _game_loop():
        from environment import SiedlerScharfschuetzenEnv, MAIN_ACTIONS, ActionPhase
        import io as _io

        env = SiedlerScharfschuetzenEnv(player_id=1, use_spatial_obs=False)
        env.reset(seed=0)
        _wintersturm_start(env)

        total_reward = 0.0
        step_count   = 0
        last_info    = {}
        last_action_name = "—"

        def _render_state() -> str:
            """Faengt show_state + show_actions als String ab."""
            buf = _io.StringIO()
            old = sys.stdout
            sys.stdout = buf
            try:
                show_state(env)
                if step_count > 0:
                    rw = last_info.get("step_reward", 0)
                    sign = "+" if rw >= 0 else ""
                    print(f"\nStep #{step_count}: {last_action_name}  {sign}{rw:.4f}  "
                          f"Gesamt:{total_reward:.3f}")
                    if last_info.get("blocked_invalid_action"):
                        print("!!! Ungueltige Aktion — ignoriert !!!")
                print("")
                show_actions(env)
                print("\nEingabe: Nr | q=Ende | r=Reset | w=Warten")
            finally:
                sys.stdout = old
            return buf.getvalue()

        def _render_map_frame():
            """Rendert Karten-Frame mit Phase-Highlights und schickt ihn an Map-Queue."""
            try:
                from PIL import Image as _PILI, ImageDraw as _PILID, ImageFont as _PILIF
                import pathfinding as _pf
                m = _get_render_module()
                global _lv_base
                if _lv_base is None:
                    _lv_base = m._make_base_image(env, None)
                frame = m._draw_frame(
                    env, _lv_base, step_idx=0, total_steps=1,
                    draw_paths=True, max_paths=800,
                    action_label=f"t={int(env.current_time)}s",
                    label_entities=True,
                    show_worker_states=True,
                    show_worker_targets=True,
                    show_refiner_trips=True,
                )
                # Phase-Highlights einzeichnen
                highlights = get_map_highlights(env)
                if highlights:
                    img = _PILI.fromarray(frame, mode="RGB")
                    draw = _PILID.Draw(img, mode="RGBA")
                    font = _PILIF.load_default()
                    grid_h = env.map_manager.grid.height
                    grid_w = env.map_manager.grid.width
                    for hx, hy, lbl in highlights:
                        lx, ly = env.map_manager.to_local_coords(hx, hy)
                        px = int(round(lx / _pf.SCALE_X))
                        py = int(round(ly / _pf.SCALE_Y))
                        px = max(0, min(grid_w - 1, px))
                        py = max(0, min(grid_h - 1, py))
                        r = 5
                        draw.ellipse((px - r, py - r, px + r, py + r),
                                     fill=(255, 220, 0, 200), outline=(0, 0, 0, 180))
                        draw.text((px - 3, py - 4), lbl,
                                  fill=(0, 0, 0, 255), font=font)
                    import numpy as _np
                    frame = _np.array(img)
                try:
                    _map_q.put_nowait(frame)
                except _q.Full:
                    pass
            except Exception:
                pass

        # Initialen State + Karte zeigen
        try:
            _text_q.put_nowait(_render_state())
        except _q.Full:
            pass
        _render_map_frame()

        while not _shutdown.is_set():
            # Auf Eingabe warten
            try:
                raw = _input_q.get(timeout=0.1)
            except _q.Empty:
                continue

            if raw.lower() == "q":
                _shutdown.set()
                try:
                    root.after(0, root.destroy)
                except tk.TclError:
                    pass
                break

            if raw.lower() == "r":
                env.reset()
                _wintersturm_start(env)
                total_reward = 0.0
                step_count = 0
                last_info = {}
                last_action_name = "—"
                _lv_base = None
                _render_map_frame()
                try:
                    _text_q.put_nowait(_render_state())
                except _q.Full:
                    pass
                continue

            if raw.lower() == "w":
                action = 0
            else:
                try:
                    action = int(raw)
                except ValueError:
                    try:
                        _text_q.put_nowait(_render_state() + "\n!!! Ungueltige Eingabe !!!")
                    except _q.Full:
                        pass
                    continue

            import numpy as np
            mask = env.action_masks()
            n = env.action_spaces[env.current_phase].n
            if action < 0 or action >= n or not mask[action]:
                try:
                    _text_q.put_nowait(_render_state() + f"\n!!! Aktion {action} nicht verfuegbar !!!")
                except _q.Full:
                    pass
                continue

            # Aktionsname bestimmen
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

            # Auto-Skip
            while info.get("multi_step") and env.current_phase in (
                ActionPhase.POSITION_GROUP, ActionPhase.POSITION_INDEX
            ):
                auto_mask = env.action_masks()
                auto_n = env.action_spaces[env.current_phase].n
                enabled = [i for i in range(auto_n) if auto_mask[i]]
                if len(enabled) == 1:
                    obs, reward, terminated, truncated, info = env.step(enabled[0])
                    total_reward += reward
                    step_count += 1
                    last_info = info
                else:
                    break

            _render_map_frame()

            if terminated or truncated:
                end_txt = (f"\n{'='*50}\nEPISODE BEENDET nach {step_count} Steps\n"
                           f"Gesamt-Reward: {total_reward:.3f}\n"
                           f"Scharfschuetzen: {env.scharfschuetzen}\n{'='*50}\n"
                           f"Eingabe 'r' fuer neue Episode, 'q' zum Beenden.")
                try:
                    _text_q.put_nowait(end_txt)
                except _q.Full:
                    pass
                continue

            try:
                _text_q.put_nowait(_render_state())
            except _q.Full:
                pass

    game_thr = _thr.Thread(target=_game_loop, daemon=True)
    game_thr.start()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        _request_close()
        game_thr.join(timeout=1.0)


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if "--gui" in args or os.environ.get("SIEDLER_PLAY_UI") == "1":
        play_ui()
        return
    play()


if __name__ == "__main__":
    main()
