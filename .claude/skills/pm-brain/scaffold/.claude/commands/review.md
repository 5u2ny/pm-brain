# /review

The weekly maintenance sweep. Six checks. Produces a dated report and edits files directly where confidence is high.

## Input

None, or an optional scope (`/review hypotheses`, `/review stakeholders`) to run a single check.

## Loads

- `CLAUDE.md` (operating principles, autonomy mode, memory promotion bar)
- `docs/system-evolution.md` (the 8 failure modes the sweep is designed to catch)
- All durable areas in scope: `knowledge/`, `hypotheses/`, `decisions/`, `stakeholders/`
- Recent `ingestion/` for promotion candidates
- The last 2 `maintenance/log/` entries to compare deltas

## Updates

- `maintenance/log/<date>-review.md` — the dated report
- Direct edits to durable files where confidence is high: promote / demote hypotheses, update stakeholder `Last touched`, archive shipped features past 90 days, compress duplicate insights
- Drafts (not committed) for items that need PM judgment: stale strategy assumptions, unresolved tensions, decision debt

## Surfaces

The six standard checks, with counts and the top item in each:

1. **Stale knowledge** — files not updated in 6+ weeks
2. **Stale evidence** — market past 30-60 days, interviews past 90, strategy assumptions past quarterly
3. **Hypothesis and decision hygiene** — active hypotheses with no evidence in 30+ days, promoted hypotheses without decisions, triggered "what would reverse this" conditions, decision debt
4. **Stakeholder cadence and strategy tensions** — high-influence stakeholders not touched in 3+ weeks, drift between recent decisions and strategy
5. **Knowledge synthesis (compression)** — recurring patterns, recurring contradictions, candidates for `strategy.md § Tensions`
6. **Archival sweep** — shipped features past 90 days, resolved hypotheses, old market intel

Compression is additive. Minority signals are preserved. Archive extracts durable lessons before removing.

## Cadence notes

- `/review` runs weekly. The biweekly / monthly / quarterly refinements live in `docs/system-evolution.md` and run separately.
