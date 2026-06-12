# Adaptive Reward Update 2026-03-14

## Goal

The experiment loop should not only compare fixed reward presets. It should propose new reward families, test them, rank them on measured progress, and use the results to decide what to mutate next.

## Added Reward Hooks

- `terminal_path_ready_bonus`
- `step_unlock_milestone_bonus`
- `step_unlock_milestone_count`
- `step_path_ready_bonus`
- `step_required_building_complete_bonus`
- `step_required_tech_complete_bonus`
- `step_delta_taler_income_bonus`

These hooks are intended to break the flat "all zero terminal potential" regime by rewarding path unlocking and economy buildup before the final Scharfschuetzen stock objective becomes reachable.

## Added Evaluation Metrics

Adaptive runs now track:

- unlock progress
- completed required buildings
- completed required techs
- taler income per cycle

This avoids ranking all early-stage candidates as identical when terminal potential is still zero.

## New Adaptive Families

- `custom_path_ready_bounty`
- `custom_requirement_milestones`
- `custom_income_bridge`
- `custom_short_unlock_curriculum`
- `custom_short_requirement_sprint`
- `custom_dual_phase_stock_after_path`

These sit alongside the earlier families (`custom_unlock_*`, `custom_dependency_heavy`, `custom_economy_bootstrap`, `custom_hybrid_*`, `custom_force_progress`).

## Mutation Directions

Adaptive round-2 mutations now include:

- `*_path_ready_focus`
- `*_milestone_focus`
- `*_income_focus`
- `*_short_horizon`

## Smoke Result

A small adaptive smoke run completed far enough to verify:

- live per-round logs are written under `adaptive_sessions/.../logs`
- partial `detail.json` and `summary.json` are written during the round
- the new metrics appear in summaries and rankings

Current smoke ranking still shows zero terminal potential, but the framework now distinguishes candidates on unlock-oriented signals instead of collapsing everything to the same score.
