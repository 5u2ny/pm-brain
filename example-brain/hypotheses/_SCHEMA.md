# Hypothesis File Schema

Hypotheses are **feature-scoped**. One file per feature, named `<feature-slug>.md`.

A feature can have hypotheses in two modes:
- **Pre-ship:** generated proactively, organized by the 5 risk areas (value, usability, feasibility, viability, **other**), tested via experiments.
- **Post-ship:** generated from observed product/analytics/interview data after launch — "why is retention dropping in week 2?" Same schema, the `Origin` field marks them as data-derived.

The `other` bucket exists because real risks don't always fit the canonical four — regulatory, ethical, partnership-dependency, brand, security, internal-political risks all show up and should be hypothesized about explicitly rather than buried.

## File structure

```markdown
# Hypotheses — <feature-name>

<!-- Paths in this file are relative to THIS file's location (hypotheses/<slug>.md). -->

## Meta
- Feature: `../knowledge/product/features/<slug>.md`
- Status: one of `active`, `partially-validated`, `promoted`, `demoted`, `archived`. Pick exactly one. If individual hypotheses inside the file have mixed states, the file-level `Status` reflects the dominant state; per-hypothesis status (under each H-Vn / H-Un / etc.) carries the detail. Do not invent compound file-level statuses like `active (1 partially-validated)`.
- Created: YYYY-MM-DD
- Last updated: YYYY-MM-DD

## Value risk
### H-V1: <one-sentence belief>
- **Origin:** proactive | data-derived (from <source>)
- **Confidence:** low | medium | high
- **Evidence for:**
- **Evidence against:**
- **Test:** <experiment, interview, analysis>
- **Decision trigger:** <what result would promote? what would demote?>
- **Status:** active | promoted | demoted | killed
- **Resolution:** <if resolved, what happened — links to decision>

## Usability risk
### H-U1: …
<same fields>

## Feasibility risk
### H-F1: …

## Viability risk
### H-B1: …

## Other risk
### H-O1: <one-sentence belief>
<!-- For risks that don't fit the canonical four: regulatory, ethical, partnership-dependency, brand, security, internal-political, etc. Name the risk type in the heading. -->
<same fields>
```

## Lifecycle

- **active** — being tested, evidence accumulating
- **promoted** — confirmed; spawn a decision in `decisions/`
- **demoted** — contradicted but kept for context; document why
- **killed** — no longer relevant (feature reshaped, market shifted)
- **archived** — feature shipped and measured; move file to `hypotheses/archive/`

## Promotion rule

When evidence is sufficient to promote a hypothesis, the system MUST:
1. Mark the hypothesis `promoted` with the resolution note.
2. Create a corresponding decision file in `decisions/` referencing the hypothesis.
3. Surface the promotion to the PM in the task summary.
