#!/usr/bin/env python3
"""Repository smoke checks for local runs, Colab bootstrap, and CI."""

from __future__ import annotations

import argparse
import importlib
import traceback


DEPENDENCY_IMPORTS = [
    ("gymnasium", "gymnasium"),
    ("stable-baselines3", "stable_baselines3"),
    ("sb3-contrib", "sb3_contrib"),
    ("tensorboard", "tensorboard"),
]


def _import_module(module_name: str):
    module = importlib.import_module(module_name)
    print(f"SMOKE_IMPORT_OK module={module_name}")
    return module


def _check_dependency_imports() -> None:
    for package_name, module_name in DEPENDENCY_IMPORTS:
        _import_module(module_name)
        print(f"SMOKE_DEP_OK package={package_name}")


def _check_project_imports() -> None:
    production_system = _import_module("production_system")
    worker_simulation = _import_module("worker_simulation")

    if not hasattr(production_system, "get_refiner_resource_ops_per_cycle"):
        raise AttributeError(
            "production_system is missing get_refiner_resource_ops_per_cycle"
        )
    print("SMOKE_ATTR_OK module=production_system attr=get_refiner_resource_ops_per_cycle")

    if not hasattr(worker_simulation, "FORCE_TO_WORK_PENALTY"):
        raise AttributeError(
            "worker_simulation is missing FORCE_TO_WORK_PENALTY"
        )
    print("SMOKE_ATTR_OK module=worker_simulation attr=FORCE_TO_WORK_PENALTY")

    _import_module("colab_training")
    print("SMOKE_PROJECT_IMPORTS_OK")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run smoke checks for training bootstrap imports.")
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Also validate dependency imports used by Colab training.",
    )
    args = parser.parse_args()

    try:
        if args.check_deps:
            _check_dependency_imports()
        _check_project_imports()
    except Exception:
        print("SMOKE_FAILED")
        traceback.print_exc()
        return 1

    print("SMOKE_IMPORT_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
