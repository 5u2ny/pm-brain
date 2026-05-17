# Decision Record Schema

Filename: `YYYY-MM-DD-<slug>.md`

```markdown
# Decision: <one-line statement>

## Status
pending | decided | superseded

## Date
YYYY-MM-DD <!-- decided date, or date opened if pending -->

## Context
<!-- 2–4 sentences. What problem / fork in the road. -->

## Options considered
1.
2.
3.

## Decision
<!-- What we picked. Empty for pending. -->

## Why
<!-- The actual reasoning. Be specific. Empty for pending. -->

## What would reverse this
<!-- The most valuable field. The condition under which we'd revisit. -->

## For pending decisions only
- **Blocker impact:** <what work this is currently blocking>
- **Deadline:** <when it needs to be resolved, or "no hard deadline">
- **Owner:** <who's driving the resolution>
- **Missing evidence:** <what we'd need to learn to decide>

## Linked
<!-- Paths are relative to THIS file's location (decisions/YYYY-MM-DD-<slug>.md). -->
- Hypotheses: `../hypotheses/<slug>.md`
- Strategy: `../knowledge/strategy.md` § <section>
- Stakeholders informed: `../stakeholders/<slug>.md`, …
```

## Rules

- Every shipped feature should have at least one decision record.
- When a hypothesis is `promoted`, a decision is auto-drafted (PM confirms).
- Decisions are append-only. To reverse, write a new decision that references and supersedes the old one (set the old one's status to `superseded`).
- **Decision debt:** decisions with `status: pending` are unresolved forks. Maintenance surfaces them — especially when their blocker impact is high or deadline is approaching.
