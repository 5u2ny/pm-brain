# /risk

Run the 5-area risk scan on a feature or plan. Surface which risks have no hypothesis, draft stubs for the gaps.

## Input

A feature slug (`/risk weekly-digest`), a plan name, or a draft PRD pasted into the call.

## Loads

- `knowledge/product/features/<slug>.md` if the feature exists
- All `hypotheses/<slug>.md` files linked to it
- `knowledge/users/insights.md` (value and usability evidence)
- `knowledge/strategy.md § Non-goals` (does this violate one?)
- `decisions/` filtered to ones that constrain this feature
- `rules/discovery.md` for any risk-area discovery rules

## Updates

`/risk` is not read-only. For any of the 5 risk areas with no hypothesis, it drafts a stub (status: `candidate`) with the open question and the suggested first test. Behavior depends on autonomy mode (`CLAUDE.md § Operating preferences § Autonomy mode`):

- **Act and tell (default).** Stubs are saved to `hypotheses/<slug>.md` and the feature file's `## Linked § Hypotheses` is updated to reference them. The operator triages on next `/review` or earlier.
- **Propose and wait.** Stubs are presented as drafts. Nothing saved until the operator confirms.

Risks with active hypotheses and fresh evidence are not touched.

## Surfaces

The five risk areas, each with status and the top item:

1. **Value** — will it solve a real, frequent, valuable problem? Evidence for / against / gap
2. **Usability** — can the target user complete the core flow? Evidence for / against / gap
3. **Feasibility** — can the team build it given current capability? Evidence for / against / gap
4. **Viability** — does it work for the business (revenue, ops, legal, regulatory)? Evidence for / against / gap
5. **Other** — anything not in the canonical four (partnership, ecosystem, timing)

Format per area: `[have hypothesis | stub drafted | confirmed | demoted]` + one line on what's missing.

- 1-3 highest-leverage tests across all five areas
- Any non-goal this feature might violate
