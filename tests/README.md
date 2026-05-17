# tests/

Eval suite for the PM Brain skill. Runs synthetic scenarios through `claude -p` and asserts the brain's state after each turn.

See [`docs/testing.md`](../docs/testing.md) for the full philosophy and architecture. This file is the operator-level quickstart.

## Quickstart

```bash
# Single scenario, single run (cheap, fast)
python tests/harness/run_scenario.py tests/scenarios/01-b2b-churn

# Single scenario, N runs (for convergence pass rate)
python tests/harness/run_scenario.py tests/scenarios/01-b2b-churn --runs 5

# All scenarios, N runs each
python tests/harness/run_all.py --runs 5
```

Results land in `tests/results/<date>-<scenario>-<run>.json`. The folder is gitignored by default.

## Layout

```
tests/
├── README.md                  # This file
├── scenarios/                 # Synthetic scenarios with ground truth
│   └── 01-b2b-churn/
│       ├── README.md          # What this scenario covers
│       ├── inputs/            # Cached synthetic artifacts, ordered
│       └── expected.yaml      # Ground-truth assertions
└── harness/
    ├── run_scenario.py        # Per-scenario runner
    ├── run_all.py             # Batch runner
    ├── checks/                # Structural assertion helpers
    │   └── structural.py
    └── judges/                # LLM-judge rubrics
        ├── hypothesis_promoted.md
        ├── contradiction_surfaced.md
        └── decision_quality.md
```

## What a scenario looks like

A scenario is an ordered stream of synthetic PM artifacts (turns) with ground-truth assertions about what the brain's state should look like after each turn.

Each turn under `inputs/` is a single file: an interview transcript, a meeting note, an analytics screenshot description, a Slack thread, a competitor changelog. The harness replays them in filename order.

`expected.yaml` declares per-turn and final-state assertions. Two kinds:

- **Structural** — Python asserts on the file system. Deterministic, fast, free.
- **Content** — LLM-judge calls with a tight rubric. Non-deterministic, costs money. Use sparingly.

See [`docs/testing.md § Scenario format`](../docs/testing.md#scenario-format) for the full ground-truth schema.

## Adding a scenario

1. Pick a lifecycle move not covered by existing scenarios (see the coverage gaps in `docs/testing.md`).
2. Create `tests/scenarios/<NN-slug>/`.
3. Write `README.md` declaring what the scenario covers and which lifecycle moves it exercises.
4. Generate cached synthetic inputs under `inputs/`. Name them `turn-NN-<kind>.md`. **Commit them.** Don't regenerate on the fly.
5. Write `expected.yaml` with per-turn structural + content assertions and a `final_state` block.
6. Run the harness against the scenario. Iterate on `expected.yaml` until the scenario passes at the threshold you set.

## Cost guard

The harness uses real LLM calls. Cost ballpark:

- Per turn: ~$0.05-0.20
- Per content (judge) assertion: ~$0.02-0.05
- Per full scenario run (10 turns + 8 judges): ~$2-5

Don't loop the harness in a debug session without a kill switch. The runner has a `--max-cost` flag for safety.
