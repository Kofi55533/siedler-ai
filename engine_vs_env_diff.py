# -*- coding: utf-8 -*-
"""
Engine vs Environment Diff Report

Vergleicht config/engine_decoded.json (Original-Engine) gegen die
aktuelle Python-Implementierung und schreibt einen Markdown-Report.

Wichtig:
- Env-Werte werden zur Laufzeit aus den aktuellen Modulen geladen
  (kein veraltetes Hardcoding).
- Dadurch bleibt der Report auch nach Code-Aenderungen korrekt.
"""

import json
import os
from dataclasses import asdict
from typing import Any, Dict, List


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_DATA = os.path.join(SCRIPT_DIR, "config", "engine_decoded.json")
FULL_WORKER_ENGINE_DATA = os.path.join(SCRIPT_DIR, "config", "full_worker_engine_behavior.json")
REPORT_FILE = os.path.join(SCRIPT_DIR, "config", "engine_env_diff_report.md")


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalize_worker_name(name: str) -> str:
    if not name:
        return ""
    n = str(name).strip().lower()
    alias = {
        "sawmillworker": "sawmill_worker",
        "masterbuilder": "master_builder",
        "tavernbarkeeper": "barkeeper",
    }
    return alias.get(n, n)


def load_engine_data() -> Dict[str, Any]:
    with open(ENGINE_DATA, "r", encoding="utf-8") as f:
        return json.load(f)


def load_full_worker_engine_data() -> Dict[str, Any]:
    if not os.path.exists(FULL_WORKER_ENGINE_DATA):
        return {}
    with open(FULL_WORKER_ENGINE_DATA, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}


def load_env_runtime() -> Dict[str, Any]:
    # Laufzeitwerte aus aktuellem Code.
    from map_config_wintersturm import PLAYER_1_SMALL_DEPOSITS
    from production_system import (
        DEFAULT_REFINER_RESOURCE_OPS_PER_CYCLE,
        Mine,
        REFINER_RESOURCE_OPS_PER_CYCLE,
        SERF_EXTRACTION,
        SERF_RESOURCE_SEARCH_RADIUS,
    )
    from worker_simulation import (
        FORCE_TO_WORK_PENALTY,
        WORKER_PARAMS,
        WORKTIME_BASE,
        WORKTIME_THRESHOLD_WORK,
    )
    from environment import (
        BLESS_CATEGORIES,
        BLESS_DURATION,
        BLESS_MOTIVATION_BONUS,
        BLESS_REQUIRED_FAITH,
        INITIAL_TAX_LEVEL,
        MAXIMUM_FAITH,
        SNOW_MOVE_SPEED_FACTOR,
        TAX_AMOUNT_PER_WORKER,
        TAX_PENALTY,
    )

    mine_defaults = Mine.__dataclass_fields__
    mine_production = {
        "mines_per_cycle": _safe_int(mine_defaults["mines_per_cycle"].default, 1),
        "amount_by_level": {1: 4, 2: 5, 3: 6},
        "workers_by_level": {1: 5, 2: 6, 3: 7},
    }

    worker_params = {
        name: asdict(params)
        for name, params in WORKER_PARAMS.items()
    }

    env_refiner_ops = dict(DEFAULT_REFINER_RESOURCE_OPS_PER_CYCLE)
    env_refiner_ops.update(REFINER_RESOURCE_OPS_PER_CYCLE)

    def _pit_amount(category: str, fallback: int) -> int:
        deps = PLAYER_1_SMALL_DEPOSITS.get(category, [])
        if not deps:
            return fallback
        return _safe_int(deps[0].get("amount"), fallback)

    env_deposit_amounts = {
        "xd_ironpit1": _pit_amount("Eisen", 12000),
        "xd_stonepit1": _pit_amount("Stein", 14000),
        "xd_claypit1": _pit_amount("Lehm", 12000),
        "xd_sulfurpit1": _pit_amount("Schwefel", 8000),
        "xd_iron1": 400,
        "xd_stone1": 400,
        "xd_clay1": 400,
        "xd_sulfur1": 400,
    }

    runtime_map_deposit_amounts: Dict[str, int] = {}
    resources_path = os.path.join(SCRIPT_DIR, "player1_resources.json")
    if os.path.exists(resources_path):
        try:
            with open(resources_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            runtime_deps = (
                data.get("mine_pits", data.get("deposits", {}))
                if isinstance(data, dict)
                else {}
            )
            runtime_map_deposit_amounts = {
                "xd_ironpit1": _safe_int((runtime_deps.get("Eisen") or [{}])[0].get("amount"), 0),
                "xd_stonepit1": _safe_int((runtime_deps.get("Stein") or [{}])[0].get("amount"), 0),
                "xd_claypit1": _safe_int((runtime_deps.get("Lehm") or [{}])[0].get("amount"), 0),
                "xd_sulfurpit1": _safe_int((runtime_deps.get("Schwefel") or [{}])[0].get("amount"), 0),
            }
        except Exception:
            runtime_map_deposit_amounts = {}

    specific_bless_filters_modeled = any(
        any(str(w).upper() != "ALL" for w in cfg.get("worker_types", []))
        for cfg in BLESS_CATEGORIES.values()
    )

    env_logic = {
        "worktime_base": WORKTIME_BASE,
        "worktime_threshold_work": WORKTIME_THRESHOLD_WORK,
        "force_to_work_penalty": FORCE_TO_WORK_PENALTY,
        "tax_amount": TAX_AMOUNT_PER_WORKER,
        "tax_penalty": TAX_PENALTY,
        "initial_tax_level": INITIAL_TAX_LEVEL,
        "blessing_bonus": BLESS_MOTIVATION_BONUS,
        "blessing_bonus_time": BLESS_DURATION,
        "maximum_faith": MAXIMUM_FAITH,
        "blessing_worker_filter_modeled": specific_bless_filters_modeled,
        "snow_speed_factor": SNOW_MOVE_SPEED_FACTOR,
    }

    # Enum-Keys auf stabile String-Keys abbilden.
    extraction_key_map = {
        "IRON_RAW": "iron",
        "STONE_RAW": "stone",
        "CLAY_RAW": "clay",
        "SULFUR_RAW": "sulfur",
        "WOOD_RAW": "wood",
    }
    env_serf_extraction: Dict[str, Dict[str, float]] = {}
    for res_type, cfg in SERF_EXTRACTION.items():
        key = extraction_key_map.get(getattr(res_type, "name", ""))
        if not key:
            continue
        env_serf_extraction[key] = {
            "delay": _safe_float(cfg.get("delay"), 0.0),
            "animation": _safe_float(cfg.get("animation"), 0.0),
            "amount": _safe_int(cfg.get("amount"), 0),
        }

    return {
        "serf_extraction": env_serf_extraction,
        "serf_search_radius": SERF_RESOURCE_SEARCH_RADIUS,
        "mine_production": mine_production,
        "worker_params": worker_params,
        "refiner_ops": env_refiner_ops,
        "deposit_amounts": env_deposit_amounts,
        "runtime_map_deposit_amounts": runtime_map_deposit_amounts,
        "logic": env_logic,
    }


def generate_report(
    engine: Dict[str, Any],
    env: Dict[str, Any],
    full_worker_engine: Dict[str, Any] | None = None,
) -> str:
    lines: List[str] = []
    critical: List[str] = []
    warnings: List[str] = []

    has_mine_mismatch = False
    has_refiner_mismatch = False
    has_deposit_mismatch = False
    has_worktime_logic_mismatch = False
    has_bless_filter_mismatch = False
    has_snow_factor_mismatch = False

    lines.append("# Engine vs Environment Diff Report")
    lines.append("")
    lines.append("Automatisch generiert von engine_vs_env_diff.py")
    if full_worker_engine:
        lines.append("")
        lines.append(
            "Worker-Parameter werden gegen `config/full_worker_engine_behavior.json` "
            "verglichen, weil dieser Extract alle Arbeitsplatz-TaskLists rekursiv einbezieht."
        )
    lines.append("")

    # ---------------------------------------------------------------------
    # 1) Minen
    # ---------------------------------------------------------------------
    lines.append("## 1. Minen-Produktion")
    lines.append("")
    mine_tls = engine.get("mine_tasklists", {}) or {}
    env_mines_per_cycle = _safe_int(env["mine_production"].get("mines_per_cycle"), 1)
    for mine_name, tl in sorted(mine_tls.items()):
        engine_mine_ops = _safe_int(tl.get("task_mined_resource_count"), 0)
        engine_wt_ops = _safe_int(tl.get("task_change_work_time_work_count"), 0)
        if engine_mine_ops != env_mines_per_cycle:
            has_mine_mismatch = True
            msg = (
                f"{mine_name}: Engine mine_ops={engine_mine_ops} "
                f"vs Env mine_ops={env_mines_per_cycle}"
            )
            critical.append(msg)
            lines.append(f"- KRITISCH: {msg}")
        else:
            lines.append(
                f"- OK: {mine_name}: mine_ops={engine_mine_ops}, "
                f"worktime_ops={engine_wt_ops}"
            )
    lines.append("")

    # ---------------------------------------------------------------------
    # 2) Refiner-Operationen
    # ---------------------------------------------------------------------
    lines.append("## 2. Refiner/Verarbeiter")
    lines.append("")
    tasklists = engine.get("tasklists", {}) or {}
    for engine_worker, tl in sorted(tasklists.items()):
        mine_count = _safe_int(tl.get("task_mined_resource_count"), 0)
        refine_count = _safe_int(tl.get("task_refine_resource_count"), 0)
        total_ops = mine_count + refine_count
        if total_ops <= 0:
            continue

        env_worker = _normalize_worker_name(engine_worker)
        env_ops = _safe_int(env["refiner_ops"].get(env_worker), 1)
        if total_ops != env_ops:
            has_refiner_mismatch = True
            msg = (
                f"{engine_worker}: Engine resource_ops={total_ops} "
                f"vs Env resource_ops={env_ops}"
            )
            critical.append(msg)
            lines.append(f"- KRITISCH: {msg}")
        else:
            lines.append(f"- OK: {engine_worker}: resource_ops={total_ops}")
    lines.append("")

    # ---------------------------------------------------------------------
    # 3) Deposit-Mengen
    # ---------------------------------------------------------------------
    lines.append("## 3. Deposit-Mengen")
    lines.append("")
    deposits = engine.get("deposits", {}) or {}
    runtime_map_amounts = env.get("runtime_map_deposit_amounts", {}) or {}
    for name, dep in sorted(deposits.items()):
        engine_amount = _safe_int(dep.get("resource_amount"), 0)
        env_amount = env["deposit_amounts"].get(name)
        if env_amount is None:
            lines.append(f"- INFO: {name}: Engine={engine_amount}, Env=nicht definiert")
            continue
        if engine_amount != env_amount:
            msg = f"{name}: Engine={engine_amount} vs Env={env_amount}"
            runtime_override = _safe_int(runtime_map_amounts.get(name), 0)
            if runtime_override > 0 and runtime_override == env_amount:
                lines.append(
                    f"- INFO: {msg} (Map-Override plausibel: runtime_export={runtime_override})"
                )
                continue
            has_deposit_mismatch = True
            if abs(engine_amount - env_amount) > 1000:
                critical.append(msg)
                lines.append(f"- KRITISCH: {msg}")
            else:
                warnings.append(msg)
                lines.append(f"- WARNUNG: {msg}")
        else:
            lines.append(f"- OK: {name}: {engine_amount}")
    lines.append("")

    # ---------------------------------------------------------------------
    # 4) Worker-Parameter
    # ---------------------------------------------------------------------
    lines.append("## 4. Worker-Parameter")
    lines.append("")
    workers = engine.get("workers", {}) or {}
    full_runtime_workers = {}
    if full_worker_engine:
        full_runtime_workers = (full_worker_engine.get("runtime") or {}).get("workers") or {}
    for engine_name, data in sorted(workers.items()):
        if engine_name == "serf":
            continue
        env_name = _normalize_worker_name(engine_name)
        env_cfg = env["worker_params"].get(env_name)
        if env_cfg is None:
            warnings.append(f"{engine_name}: fehlt in Env-WORKER_PARAMS")
            lines.append(f"- WARNUNG: {engine_name}: fehlt in Env-WORKER_PARAMS")
            continue

        diffs = []
        full_runtime = full_runtime_workers.get(env_name, {}) if isinstance(full_runtime_workers, dict) else {}
        full_worktime = full_runtime.get("worktime") if isinstance(full_runtime, dict) else None
        worker_truth = full_worktime if isinstance(full_worktime, dict) and full_worktime else data
        checks = [
            ("work_wait_until", _safe_int(worker_truth.get("work_wait_until")), _safe_int(env_cfg.get("work_wait_until"))),
            ("eat_wait", _safe_int(worker_truth.get("eat_wait")), _safe_int(env_cfg.get("eat_wait"))),
            ("rest_wait", _safe_int(worker_truth.get("rest_wait")), _safe_int(env_cfg.get("rest_wait"))),
            ("work_time_change_work", _safe_int(worker_truth.get("work_time_change_work")), _safe_int(env_cfg.get("work_time_change_work"))),
            ("exhausted_malus", _safe_float(worker_truth.get("exhausted_malus")), _safe_float(env_cfg.get("exhausted_malus"))),
        ]
        for key, engine_val, env_val in checks:
            if engine_val != env_val:
                diffs.append(f"{key}: Engine={engine_val} vs Env={env_val}")

        if full_runtime:
            engine_wt_ops = _safe_int(full_runtime.get("worktime_changes_per_cycle"), 1)
        else:
            tl = tasklists.get(engine_name, {}) or {}
            engine_wt_ops = _safe_int(tl.get("task_change_work_time_work_count"), 1)
            if engine_name == "miner":
                mine_tls = engine.get("mine_tasklists", {}) or {}
                mine_counts = [
                    _safe_int(entry.get("task_change_work_time_work_count"), 1)
                    for entry in mine_tls.values()
                ]
                if mine_counts:
                    engine_wt_ops = max(engine_wt_ops, max(mine_counts))
        env_wt_ops = _safe_int(env_cfg.get("worktime_changes_per_cycle"), 1)
        if engine_wt_ops != env_wt_ops:
            diffs.append(f"worktime_changes_per_cycle: Engine={engine_wt_ops} vs Env={env_wt_ops}")

        if diffs:
            for diff in diffs:
                warnings.append(f"{engine_name}.{diff}")
            lines.append(f"- WARNUNG: {engine_name}")
            for diff in diffs:
                lines.append(f"  - {diff}")
        else:
            lines.append(f"- OK: {engine_name}")
    lines.append("")

    # ---------------------------------------------------------------------
    # 5) Serf / Logic
    # ---------------------------------------------------------------------
    lines.append("## 5. Serf und Logik")
    lines.append("")

    serf = workers.get("serf", {}) or {}
    engine_search = _safe_int(serf.get("resource_search_radius"), -1)
    env_search = _safe_int(env.get("serf_search_radius"), -1)
    lines.append(
        f"- Serf ResourceSearchRadius: Engine={engine_search}, Env={env_search} "
        f"[{'OK' if engine_search == env_search else 'DIFF'}]"
    )

    logic = engine.get("logic", {}) or {}
    wt = logic.get("worktime", {}) or {}
    taxes = logic.get("taxes", {}) or {}
    blessing = logic.get("blessing", {}) or {}
    weather = logic.get("weather", {}) or {}
    env_logic = env["logic"]

    worktime_checks = [
        ("worktime_base", _safe_int(wt.get("base")), _safe_int(env_logic.get("worktime_base"))),
        ("worktime_threshold_work", _safe_int(wt.get("threshold_work")), _safe_int(env_logic.get("worktime_threshold_work"))),
        ("force_to_work_penalty", _safe_float(wt.get("force_to_work_penalty")), _safe_float(env_logic.get("force_to_work_penalty"))),
    ]
    for key, engine_val, env_val in worktime_checks:
        if engine_val != env_val:
            has_worktime_logic_mismatch = True
            msg = f"{key}: Engine={engine_val} vs Env={env_val}"
            critical.append(msg)
            lines.append(f"- KRITISCH: {msg}")
        else:
            lines.append(f"- OK: {key}: {engine_val}")

    tax_amount_engine = _safe_int(taxes.get("tax_amount"), 0)
    tax_amount_env = _safe_int(env_logic.get("tax_amount"), 0)
    lines.append(
        f"- TaxAmount: Engine={tax_amount_engine}, Env={tax_amount_env} "
        f"[{'OK' if tax_amount_engine == tax_amount_env else 'DIFF'}]"
    )
    tax_penalty_engine = _safe_float(taxes.get("tax_penalty"), 0.0)
    tax_penalty_env = _safe_float(env_logic.get("tax_penalty"), 0.0)
    lines.append(
        f"- TaxPenalty: Engine={tax_penalty_engine}, Env={tax_penalty_env} "
        f"[{'OK' if tax_penalty_engine == tax_penalty_env else 'DIFF'}]"
    )
    init_tax_engine = _safe_int(taxes.get("initial_tax_level"), 0)
    init_tax_env = _safe_int(env_logic.get("initial_tax_level"), 0)
    lines.append(
        f"- InitialTaxLevel: Engine={init_tax_engine}, Env={init_tax_env} "
        f"[{'OK' if init_tax_engine == init_tax_env else 'DIFF'}]"
    )

    bless_bonus_engine = _safe_float(blessing.get("bonus"), 0.0)
    bless_bonus_env = _safe_float(env_logic.get("blessing_bonus"), 0.0)
    lines.append(
        f"- BlessingBonus: Engine={bless_bonus_engine}, Env={bless_bonus_env} "
        f"[{'OK' if bless_bonus_engine == bless_bonus_env else 'DIFF'}]"
    )
    bless_time_engine = _safe_int(blessing.get("bonus_time"), 0)
    bless_time_env = _safe_int(env_logic.get("blessing_bonus_time"), 0)
    lines.append(
        f"- BlessingBonusTime: Engine={bless_time_engine}, Env={bless_time_env} "
        f"[{'OK' if bless_time_engine == bless_time_env else 'DIFF'}]"
    )
    max_faith_engine = _safe_int(blessing.get("maximum_faith"), 0)
    max_faith_env = _safe_int(env_logic.get("maximum_faith"), 0)
    lines.append(
        f"- MaximumFaith: Engine={max_faith_engine}, Env={max_faith_env} "
        f"[{'OK' if max_faith_engine == max_faith_env else 'DIFF'}]"
    )

    if not env_logic.get("blessing_worker_filter_modeled", False):
        has_bless_filter_mismatch = True
        msg = "Blessing worker filter nicht modelliert"
        critical.append(msg)
        lines.append(f"- KRITISCH: {msg}")
    else:
        lines.append("- OK: Blessing worker filter ist modelliert")

    engine_snow = weather.get("snow_move_speed_factor")
    env_snow = env_logic.get("snow_speed_factor")
    if env_snow is None:
        has_snow_factor_mismatch = True
        msg = f"SnowMoveSpeedFactor: Engine={engine_snow}, Env=nicht modelliert"
        critical.append(msg)
        lines.append(f"- KRITISCH: {msg}")
    else:
        lines.append(
            f"- SnowMoveSpeedFactor: Engine={engine_snow}, Env={env_snow} "
            f"[{'OK' if _safe_float(engine_snow) == _safe_float(env_snow) else 'DIFF'}]"
        )
    lines.append("")

    # ---------------------------------------------------------------------
    # Zusammenfassung
    # ---------------------------------------------------------------------
    lines.append("---")
    lines.append("")
    lines.append("## Zusammenfassung")
    lines.append("")
    lines.append(f"- Kritische Punkte: {len(critical)}")
    lines.append(f"- Warnungen: {len(warnings)}")
    lines.append("")

    if critical:
        lines.append("### Kritisch")
        for i, item in enumerate(critical, 1):
            lines.append(f"{i}. {item}")
        lines.append("")

    if warnings:
        lines.append("### Warnungen")
        for i, item in enumerate(warnings, 1):
            lines.append(f"{i}. {item}")
        lines.append("")

    recommendations: List[str] = []
    if has_mine_mismatch:
        recommendations.append("Mine-Multiplikatoren (TASK_MINED_RESOURCE pro Zyklus) angleichen.")
    if has_refiner_mismatch:
        recommendations.append("Refiner-ResourceOps pro Worker (refine+mine pro Zyklus) angleichen.")
    if has_deposit_mismatch:
        recommendations.append("Deposit-Mengen in map_config_wintersturm.py an Engine-Werte angleichen.")
    if has_worktime_logic_mismatch:
        recommendations.append("WorkTime-Globalwerte (base/threshold/force penalty) angleichen.")
    if has_bless_filter_mismatch:
        recommendations.append("Segen nur fuer die korrekten Worker-Kategorien anwenden.")
    if has_snow_factor_mismatch:
        recommendations.append("SnowMoveSpeedFactor fuer Wintersturm modellieren (wenn gewuenscht).")

    if recommendations:
        lines.append("### Empfohlene Aenderungen")
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"{i}. {rec}")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    print("Engine vs Environment Diff Report")
    print("=" * 40)
    engine = load_engine_data()
    full_worker_engine = load_full_worker_engine_data()
    env = load_env_runtime()
    report = generate_report(engine, env, full_worker_engine)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report geschrieben: {REPORT_FILE}")
    print()
    print(report)


if __name__ == "__main__":
    main()
