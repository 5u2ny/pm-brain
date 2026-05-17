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

## Decision-scoped /review — relevance filter on cadence flags

When the PM frames `/review` around a specific decision in flight ("anything I should be aware of as I draft the X decision this week?"), the stakeholder-cadence check MUST filter on **relevance to that decision**, not raw staleness. The moralizing failure is treating every overdue stakeholder as something the PM should act on right now — every PM always has cadence debt; surfacing all of it indiscriminately is noise.

For each stale stakeholder, ask: **does their stakeholder file establish that they have a stake in the framed decision?** Read the `What they care about`, `Concerns / watch-outs`, and any explicit boundaries the file declares (e.g., "doesn't weigh in on feature-level deprecations unless X").

- **Stale AND relevant** → name them in the should-contact-before-the-decision-lands section, with a one-line tie to *why* this decision touches their stake. **Always include their staleness as a specific reference** alongside the name — ISO date ("last touched 2026-04-12"), week-count ("5 weeks stale"), or day-count ("36 days"). Naming the stakeholder without the number leaves the PM with no urgency signal.
- **Stale BUT not relevant to the framed decision** → either omit, or put them in a clearly-separate "other cadence notes — not blocking this decision" section. NEVER mix the two lists.

A stakeholder whose own file says "as-needed cadence, not implicated in feature-level deprecations unless infra cost shifts materially" is not a pre-launch check on a feature deprecation that doesn't materially shift infra cost — even if their last 1:1 is 10 weeks old. Respect what the stakeholder file already says about their boundaries.

## Cadence notes

- `/review` runs weekly. The biweekly / monthly / quarterly refinements live in `docs/system-evolution.md` and run separately.
