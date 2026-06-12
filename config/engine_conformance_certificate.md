# Engine Conformance Certificate

- Generated: `2026-06-11T10:42:43.350740+00:00`
- Source binary: `C:\Users\marku\OneDrive\Desktop\Gold edition\bin\SettlersHoK.exe`
- Source binary SHA256: `414593764e96ca36c56acc27251f7aef61b28d2e0ee1b15fcbb4c73d0fce9f33`

## Coverage

- Worker XML/TaskLists: 361 TaskLists, 21 worker/serf entities, 48 worker buildings, 231 reachable TaskLists, 0 unresolved refs
- Static CFG: 153 functions, 591 blocks, 8761 instructions, 275 conditional branches
- Worker/Camp/Path matrix: 130 selected functions, 52 anchors, 215 selected conditional branches
- Simulation contract: 18 worker profiles, 32 branch anchors
- Ghidra decompiler: 105/130 target addresses matched, 104 functions matched, 104 decompiled OK, full code stored=False
- Engine-vs-env diff: critical=0, warnings=0

## Proof Status

- `xml_tasklist_extraction`: `machine_checked_exact_extract`
- `runtime_worker_values`: `machine_checked_against_extract`
- `static_binary_cfg`: `heuristic_static_disassembly`
- `ghidra_decompiler_evidence`: `available_hashes_and_pcode_histograms`
- `full_runtime_equivalence`: `not_formally_proven`
- `pathfinding_equivalence`: `not_formally_proven`

## Formal Equivalence Requirements

- A compiler/CPU semantic model for the exact x86 binary.
- Verified function boundaries and typed memory layout for all relevant engine objects.
- A decompiled or lifted IR for every task/path/worker function used by the simulation.
- A formal relation between engine state and simulation state.
- Exhaustive or theorem-proved transition equivalence for every reachable state.
- Runtime trace validation for nondeterministic choices, timing, floating point, and OS-dependent pathing.

## Limits

- Static CFG extraction is evidence, not a mathematical proof of semantic equivalence.
- TaskList/XML extraction is exact for the parsed files, but task execution semantics live in the binary.
- The local simulation pathfinder is not proven equivalent to the engine path solver.
- No complete proprietary high-level decompiler output is stored in this repository.

## Artifact Hashes

- `full_worker_engine_behavior`: sha256 `c0a372e3db3b9c00848ae7421982c7ff369a30533c0772feeb4bcf671a5b826a`, size 4004444 bytes
- `engine_instruction_cfg`: sha256 `fa470db9c4c786e72f11c0a3d4e3b8167f276c48fcb19f2045704ee5dc5c44ec`, size 2576189 bytes
- `worker_camp_path_branch_matrix`: sha256 `51302c8760df6ab2ad3815a9b511e3945ab09a3d86acec8012584072f11de896`, size 238046 bytes
- `worker_sim_contract`: sha256 `2de47dc8a6c8917675b341cc41c73645782c1c11a9c3951d1251babc59853b17`, size 84886 bytes
- `ghidra_worker_decompile_evidence`: sha256 `5639b809b745d1cdb868d86c7bcaad62c9d08962080957a01160004550205f4c`, size 60034 bytes
- `engine_env_diff_report`: sha256 `3501611cd6c80edc0aa214f7cfd5292dd97a8bcc90964706c740d7e1922a22ec`, size 2466 bytes
