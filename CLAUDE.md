# CLAUDE.md — PM Brain repo

This is the canonical repo for the PM Brain Claude Code skill. It contains the skill itself, a pre-scaffolded example brain, an eval suite of synthetic scenarios, and architectural docs.

## What this repo is for

Three audiences, three uses:

1. **PMs installing the skill** — copy `.claude/skills/pm-brain/` into `~/.claude/skills/`, run `/pm-brain` in any working directory. Read `README.md` and `docs/how-it-works.md`.
2. **People evaluating whether PM Brain is right for them** — browse `example-brain/` to see what a populated PM Brain looks like. Read `docs/architecture.md`.
3. **Contributors and testers** — run the eval suite under `tests/`. Add scenarios. Tighten ground-truth assertions. Surface failure modes.

This `CLAUDE.md` is the **repo-level** operating manual. It tells Claude (or any agent working in this repo) how the pieces relate and what work patterns are valid here.

It is NOT the brain's own operating manual. The brain has its own `CLAUDE.md` inside `example-brain/CLAUDE.md` and inside any working directory the skill is invoked in.

## Repo structure

```
.claude/skills/pm-brain/    # Canonical skill (SKILL.md + scaffold/ + prompts/)
example-brain/              # Pre-scaffolded instance. Browseable, edit-safe.
tests/                      # Eval suite
├── scenarios/              # Synthetic PM scenarios with ground truth
└── harness/                # Runner + structural checks + LLM-judge rubrics
docs/                       # Architecture, how it works, testing, prior art
README.md                   # Public-facing
CLAUDE.md                   # This file
```

## Working in this repo

### When asked to modify the skill

The skill at `.claude/skills/pm-brain/` is the source of truth. Two layers:

- `scaffold/` — deterministic. Schemas, CLAUDE.md template, INDEX template, folder tree. Same every install.
- `prompts/` — adaptive. Mode detection, migration, interview, post-scaffold self-test. Loaded per phase.

When changing the skill:
1. If the change is structural (new file, new schema field) → edit `scaffold/`.
2. If the change is behavioral (better interview, sharper contradiction detection) → edit `prompts/` or `SKILL.md`.
3. Mirror structural scaffold changes into `example-brain/` if the example needs to stay current.
4. Run the eval suite (`tests/harness/run_all.py`) to confirm scenarios still pass at expected rates.

### When asked to add a test scenario

Each scenario under `tests/scenarios/<NN-slug>/` ships with:

- `inputs/` — ordered, cached, synthetic artifacts (`turn-NN-<kind>.md`). Generated once, committed, never regenerated on the fly.
- `expected.yaml` — ground-truth assertions per turn + final state.
- `README.md` — what this scenario covers, which lifecycle moves it exercises.

Add new scenarios for **uncovered lifecycle moves**, not for variations of moves the existing scenarios already test. The MVP scenario (`01-b2b-churn`) covers: hypothesis promotion, hypothesis demotion via contradicting evidence, contradiction surfacing, decision drafted from evidence trail, low-signal anecdote rejection.

Coverage gaps to fill before the eval suite is comprehensive:

- Drift detection (old hypothesis loses support over time)
- New persona emergence
- Stakeholder cadence flags
- Maintenance sweep behavior (compression, archival)
- Migration mode (bulk-ingest of pre-existing PM artifacts)

### When asked to run the eval suite

```bash
# Single scenario
python tests/harness/run_scenario.py tests/scenarios/01-b2b-churn

# All scenarios, N runs each
python tests/harness/run_all.py --runs 5
```

Outputs land in `tests/results/<date>-<scenario>-<run>.json`. Each run spins up a fresh scaffold in a temp dir, replays the scenario's inputs by calling `claude -p` with each, runs structural checks after every turn, and runs LLM-judge checks at scenario end.

**The eval suite uses real LLM calls.** Cost ballpark: ~$2-5 per scenario run. Don't loop the harness in a debug session without a kill switch.

### When asked to update docs

`docs/` is derivative: every claim in `docs/architecture.md`, `docs/how-it-works.md`, etc. should trace back to either the skill, the example brain, or a passing test scenario. When the skill changes, update the docs in the same commit.

`docs/prior-art.md` is the exception — it documents adjacent ideas and trade-offs. Update when adding a scenario that explicitly contrasts with an adjacent system (e.g., "RAG would have stored this differently").

## Off-limits

- **Don't push the skill scaffold's contents directly to user repos.** The skill orchestrates that copy through `SKILL.md` workflow steps 4-5. Bypassing skips placeholder population and the self-test.
- **Don't auto-regenerate scaffold content.** The whole architectural choice is that the scaffold is deterministic.
- **Don't add LLM-judge calls where a structural assertion would work.** Judges are non-deterministic and cost money. Use them only when no structural check can answer the question.
- **Don't commit `tests/results/` outputs** unless they're pinned snapshots for regression. By default it's gitignored.

## Operating preferences

Default autonomy mode for this repo: **propose and wait** for changes to the skill itself, **act and tell** for docs and tests.

The skill is the load-bearing artifact. Changes to it affect every install. Changes to a test scenario or a doc page don't.
