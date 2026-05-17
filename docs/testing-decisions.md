# Testing — decisions & learnings

A running log of what the eval suite has taught us about the skill, and the design decisions we made in response. The reader for this doc is **a future contributor** who finds an assertion or a scaffold rule that looks arbitrary and wants to know *why it's there*.

If you add or relax an assertion, change a scaffold rule, or design a scenario based on a failure mode, append an entry here. Entries are dated and grouped by scenario.

Cross-references:
- How the suite works → [`testing.md`](./testing.md)
- Scenario format reference → [`../tests/TESTING.md`](../tests/TESTING.md)
- Per-scenario coverage notes → each scenario's own `README.md`

---

## 2026-05-17 — Provenance vocabulary refactor (cross-cutting)

**Finding.** Early scenario runs flagged "no provenance" failures even when the agent's behavior was epistemically honest. The original rule was *workflow-shaped*: every load-bearing claim had to go through `source/ → ingestion/ → hypothesis`. Real PM evidence often skips that pipeline (a hallway conversation, an industry rule of thumb, a PM intuition) and forcing those into a synthetic ingestion record made the brain *less* trustworthy, not more.

**Decision.** Replaced the workflow rule with a **vocabulary**. Every load-bearing claim wears a tag from a fixed enum:

| Tag | Trust |
|---|---|
| `[ingestion/<path>](...)` | Highest |
| `[source/<path>](...)` | High |
| `(stakeholder-verbal, <name>, <YYYY-MM-DD>)` | Medium |
| `(intuition, PM, <YYYY-MM-DD>)` | Low for external defense |
| `(industry-knowledge)` | Low |
| `(chat, no artifact)` | Low |

**Files touched.** [`scaffold/hypotheses/_SCHEMA.md`](../.claude/skills/pm-brain/scaffold/hypotheses/_SCHEMA.md), [`scaffold/decisions/_SCHEMA.md`](../.claude/skills/pm-brain/scaffold/decisions/_SCHEMA.md), [`scaffold/knowledge/users/insights.md`](../.claude/skills/pm-brain/scaffold/knowledge/users/insights.md), [`scaffold/CLAUDE.md`](../.claude/skills/pm-brain/scaffold/CLAUDE.md), [`scaffold/docs/overview.md`](../.claude/skills/pm-brain/scaffold/docs/overview.md), [`prompts/interview.md`](../.claude/skills/pm-brain/prompts/interview.md), [`prompts/migration.md`](../.claude/skills/pm-brain/prompts/migration.md), all matching files in `example-brain/`, structural checker [`tests/harness/checks/structural.py`](../tests/harness/checks/structural.py), judge rubric [`tests/harness/judges/audit_trail.md`](../tests/harness/judges/audit_trail.md), public docs [`architecture.md`](./architecture.md) + [`how-it-works.md`](./how-it-works.md), `README.md`. Unit-tested by [`tests/harness/checks/test_provenance.py`](../tests/harness/checks/test_provenance.py) (12/12 cases).

---

## 2026-05-17 — `Open questions / caveats:` field on hypotheses (scenario 02)

**Finding.** Scenario 02's `no_orphan_evidence` check returned 28 orphans on the first run. Inspection showed the orphans weren't fabricated claims — they were *caveats* the agent had thoughtfully placed under `Evidence for:` headers: "Devon's note didn't specifically ballpark budget alerts — this is an inference," "Pro churn accelerating — any hook that drives Pro conversion is valuable," "CS tickets don't segment by tier." Meta-commentary about evidence is not itself an evidence claim, but the schema gave it no home, so it leaked into the wrong section.

**Decision.** Added a `Open questions / caveats:` field to the hypothesis schema and a one-liner in `CLAUDE.md` making explicit that Evidence-for/against rows are *claims*, not commentary. Rows in the caveats field do NOT need provenance tags by construction — they are "things we haven't established yet."

**Why this is a real fix, not a relaxation.** The orphan check is doing what it should: every claim a hypothesis rests on must be auditable. The bug was *no field to express ambiguity in*, so honest agents were forced to either (a) leave the doubt out and look more certain than they were, or (b) stash it under Evidence and trip the audit. The new field lets the agent be honest *and* keep the audit trail clean.

**Files touched.** [`scaffold/hypotheses/_SCHEMA.md`](../.claude/skills/pm-brain/scaffold/hypotheses/_SCHEMA.md), [`scaffold/CLAUDE.md`](../.claude/skills/pm-brain/scaffold/CLAUDE.md), mirrors in `example-brain/`.

---

## 2026-05-17 — Relaxed over-specific structural assertions (scenarios 01 & 02)

**Finding.** Four structural assertions across 01 and 02 were tied to specific filename choices the agent could legitimately make differently. Examples:

- `source/interviews/*stripe*.md` failed when the agent named the file after the role (`compliance`) instead of the company.
- `stakeholders/*priya*.md` failed when the agent (correctly) decided an interview subject didn't need a stakeholder file at all.
- `hypothesis_evidence_count_increased_for: H1` failed because hypothesis IDs vary by run (`H1`, `H-V1`, etc.) and the harness can't reliably resolve a stable ID across naming styles.

**Decision.** Relaxed each to a disjunctive `OR` over the legitimate alternatives. The PRINCIPLE the assertion is testing (interview captured under `source/`, signal added to a hypothesis, fresh evidence routed somewhere reasonable) stayed intact; the form-specific brittleness went away.

**Why this isn't lowering the bar.** Structural checks should test *invariants the system promises*, not *one canonical form the agent might pick*. When the same epistemic move can land in multiple legitimate file shapes, the assertion should accept all of them. The content judges still hold the line on whether the synthesis was right.

**Files touched.** [`tests/scenarios/01-b2b-churn/expected.yaml`](../tests/scenarios/01-b2b-churn/expected.yaml) turns 4 + 8, [`tests/scenarios/02-inherited-folder/expected.yaml`](../tests/scenarios/02-inherited-folder/expected.yaml) turns 4 + 8.

---

## 2026-05-17 — Scenario design: prefer 4-5 turn focused scenarios over 10-turn arcs

**Finding.** Scenarios 01 and 02 are 10-turn lifecycle arcs, each costing ~$5 per run and ~25 min wall-clock. That's the right shape for *end-to-end* coverage but the wrong shape for testing one specific lifecycle move (drift detection, persona emergence, stakeholder cadence). When a focused move fails, you'd rather rerun a 4-turn scenario for $1 than re-pay $5 for a long arc most of which already passed.

**Decision.** New scenarios should be ~4-5 turns and exercise *one* uncovered move. The 10-turn scenarios stay as integration tests; the short scenarios are the unit tests for specific behaviors. Scenario 03 (drift detection) is the first scenario built to this pattern.

**Files touched.** [`tests/scenarios/03-drift-detection/`](../tests/scenarios/03-drift-detection/) (new, 4 turns, ~$1/run).

---

## 2026-05-17 — Empty-evidence placeholder false-positives in orphan-evidence check (scenarios 01 & 02)

**Finding.** Two related false positives surfaced in the same checker:

- Scenario 01 final state: `no_orphan_evidence` flagged 14 orphans. 13 were a single hypothesis's risk-area sections where the agent had correctly written `(none yet)` under `**Evidence for:**` / `**Evidence against:**` — the schema's default placeholder for "we haven't gathered evidence in this risk area yet." The 14th was a genuine miss (a hypothesis cross-reference written inside an Evidence section without a tag).
- Scenario 02 final state: 4 orphans, all parenthetical admissions with explanatory text — `(None yet from users specifically valuing AI summaries.)`, `(None against the build estimate itself.)`, `(None yet — no pricing model has been modeled.)`, `(None yet — billing model is explicitly unresolved.)`. The agent was being *more* epistemically careful than `(none yet)` — it was explaining WHY there's no evidence — but the checker rewarded it with a fail.

**Decision.** Taught the structural checker that empty-evidence placeholders are not orphan claims. Added `_is_empty_evidence_placeholder(row)` with two accepted shapes:

1. **Bare placeholder** (`_BARE_PLACEHOLDER_RE`) — entire row is one of: `(none yet)`, `none`, `none yet`, `n/a`, `tbd`, `todo`, `nothing yet`, `no evidence`, `not yet`, `pending`, `open`. Case-insensitive, with optional `*`/`_`/backtick wrappers and optional `(...)` parens.
2. **Parenthetical admission** (`_PAREN_ABSENCE_RE`) — entire row is a parenthetical that opens with an absence keyword: `(None yet — no pricing model has been modeled.)`. The whole row must be one `(...)` aside, not a claim wearing a parenthetical aside.

Applied the skip in both `_iter_evidence_rows` and `_iter_bold_evidence_rows`. Three new unit-test cases bring the suite to 15/15.

**Why this isn't lowering the bar.** A placeholder is the schema's way of saying "we have no evidence yet in this risk area" — an admission of absence, not an unsourced claim. The vocabulary refactor's whole point is that the brain should be able to be epistemically honest; punishing `(none yet)` would push the agent toward either (a) fabricating evidence to fill the slot or (b) deleting the risk-area heading entirely (losing the schema's promise that every hypothesis is checked against all five risks). The richer parenthetical shape (`(None yet — billing model is explicitly unresolved.)`) is even *more* honest: it admits the absence AND names what's blocking the evidence. The orphan check still catches real orphans — a row with a *claim* but no tag still fails.

**Files touched.** [`tests/harness/checks/structural.py`](../tests/harness/checks/structural.py) (added `_BARE_PLACEHOLDER_RE` + `_PAREN_ABSENCE_RE` + `_is_empty_evidence_placeholder` + two call-sites), [`tests/harness/checks/test_provenance.py`](../tests/harness/checks/test_provenance.py) (three new cases, 15/15 pass).

---

## 2026-05-17 — Scenario-local rubric overrides + audit_trail rubric debug (scenario 03)

**Finding.** Scenario 03's first run had 15/15 structural assertions pass but 5/5 content judges fail. Two distinct causes:

1. **Hardcoded scenario context in shared rubrics.** Almost every rubric under [`tests/harness/judges/`](../tests/harness/judges/) hardcodes scenario-01 / scenario-02 facts ("real-time alerts", "Acme Ops Lead", "Brex", "Naomi", "Maya", "Q4"). When scenario 03 (drift detection, OrthoSched / Brightsmile / availability sync) reused the same rubrics, the judge dutifully checked for Acme — and failed every time. Workflow-shaped rubrics, not vocabulary-shaped.
2. **One audit_trail rule was workflow-shaped, not vocabulary-shaped.** The rubric required a parallel `ingestion/` record for any artifact a hypothesis cites directly via `[source/...]`. But the schema explicitly allows `[source/...]` as a legitimate citation form — "use when the source is self-explanatory and synthesis would be ceremony." The rubric was enforcing the old workflow rule the refactor was supposed to retire.

**Decision.**
- Added scenario-local rubric override support to the harness: `_resolve_rubric_path` now checks `tests/scenarios/<NN>/judges/` before falling back to the shared `tests/harness/judges/`. Two-line change.
- Wrote 4 scenario-03-specific rubrics (`hypothesis_proposed`, `contradiction_surfaced`, `staleness_flagged`, `decision_provenance`) under [`tests/scenarios/03-drift-detection/judges/`](../tests/scenarios/03-drift-detection/judges/). Each rubric speaks to the drift scenario in concrete detail.
- Updated the shared `audit_trail.md` rubric to remove the parallel-ingestion-required rule. Both `decision → hypothesis → source/` and `decision → hypothesis → ingestion → source/` now PASS — matching what the schema actually says.

**Why this isn't lowering the bar.** Scenario-local rubrics let each scenario speak to its specific lifecycle move without polluting the shared library. The shared rubrics are still the right home for genuinely cross-cutting checks (audit_trail) — and those should be carefully scenario-agnostic. The audit_trail fix wasn't a relaxation; it was a bug — the rubric was tighter than the architecture it tested.

**Lesson for future scenario authors.** If a shared rubric has scenario-specific facts in it, that's a rubric smell — either rewrite it scenario-agnostic OR add a per-scenario override. Don't reuse a rubric whose facts don't fit.

**Files touched.** [`tests/harness/checks/content.py`](../tests/harness/checks/content.py) (`_resolve_rubric_path` checks scenario_dir first), [`tests/harness/run_scenario.py`](../tests/harness/run_scenario.py) (passes `scenario_dir` into `scenario_context`), [`tests/harness/judges/audit_trail.md`](../tests/harness/judges/audit_trail.md) (vocabulary alignment), 4 new rubrics under [`tests/scenarios/03-drift-detection/judges/`](../tests/scenarios/03-drift-detection/judges/).

**Result.** After the rubric override mechanism + audit-trail fix: scenario 03 content judges went from **0/5 → 4/5 PASS** in one re-run ($2). Structural stayed at 15/15. The remaining content failure was a rubric-language issue (next entry).

---

## 2026-05-17 — `staleness_flagged` rubric: define "resolve" objectively (scenario 03)

**Finding.** Scenario 03's re-run hit 4/5 content judges. The remaining `staleness_flagged` failure happened because the agent (correctly) annotated the hypothesis's Risks section with the May 17 contradiction during the /review turn AND recommended in its response text that the PM consider a demotion *next turn*. The judge interpreted this as "resolving the contradiction" and failed.

**Decision.** Sharpened the rubric to define "resolving" objectively: the only things that count as resolution are (a) flipping the hypothesis's `status:` field away from `promoted` or (b) creating a new file under `decisions/`. Everything else — annotating `Evidence against:`, updating `Risks`, recommending in response text that the PM consider a demotion — is valid /review surfacing.

**Why this isn't lowering the bar.** /review is supposed to make drift visible without pre-committing the PM. The rubric's earlier wording ("no demotion drafted, no decision proposed. Surfacing only.") was directionally right but linguistically vague — "drafted" could mean "wrote a decision file" OR "described a demotion in prose." The sharpened wording picks the auditable interpretation: status field unchanged + no new decision artifact = surfacing. The agent annotating `Evidence against:` with the May 17 finding is *good* — it's the brain learning. The agent flipping status without PM sign-off would be silent demotion, which the broader `no_silent_hypothesis_demotion` check catches anyway.

**Files touched.** [`tests/scenarios/03-drift-detection/judges/staleness_flagged.md`](../tests/scenarios/03-drift-detection/judges/staleness_flagged.md) (objective definition of "resolving" in the body, pass criterion, and fail criterion).

---

## 2026-05-17 — Scenario 02 content rubric residuals (logged, not fixed today)

**Finding.** Scenario 02's run after the vocabulary refactor + scaffold strengthening: structural 27/30 (1 hypothesis-count short + 1 broken link in a planning doc + the parenthetical-placeholder issue now fixed → 29/30 with the new checker), content 6.5/9. The three content-judge issues split into two kinds:

1. **Rubric bugs** worth fixing next.
   - `bulk_ingest_caution` at turn 1 fails with "no target file(s) found for glob:hypotheses/*.md (0 match)" — the rubric expected hypothesis files, but caution at bulk-ingest correctly produces *zero* hypothesis files. The rubric's target glob should be inverted (or made tolerant of absence).
   - `tensions_enumerated` at turn 3 fails with "this is turn 3 (CEO pressure response), not turn 2 (tensions enumeration)" — turn-pinning misalignment in `expected.yaml`. The assertion is on the wrong turn.
2. **Real agent-behavior findings** the suite is correctly catching, not bugs.
   - `insight_promotion` at turn 4: agent promoted an insight to `knowledge/users/insights.md` with 2 observations, below the documented 3-observation promotion threshold.
   - `insight_promoted_with_dissent` at turn 8: agent promoted the couples/shared-budgets insight but didn't preserve Priya's "not for me" counter-signal.

**Decision.** Don't ship rubric or scaffold changes today — the publish gate is the vocabulary refactor + audit-trail enforcement + scenario-03 drift detection, all of which are passing. The two real agent-behavior findings are exactly what the suite is meant to surface; they go on the "next scenario sweep" backlog as candidates for sharper scaffold prompting (when to promote, how to encode dissent in promoted insights). The two rubric bugs go on the same backlog with smaller priority (they're test-suite bugs, not skill bugs).

**Files touched.** None today. Backlog only.

---

## 2026-05-17 — Reruns of 01 & 02 surface a convergent agent-quality pattern (residuals)

**Finding.** After all the scaffold + checker fixes earlier today, full reruns of [01-b2b-churn](../tests/scenarios/01-b2b-churn/) and [02-inherited-folder](../tests/scenarios/02-inherited-folder/) failed the harness `passed` gate — but with a clean and informative failure pattern:

| Scenario | Structural | Content | Cost | Verdict |
|---|---|---|---|---|
| 01 b2b-churn (10 turns) | 19/23 (83%) | **11/11 (100%)** | $5.33 | structural fail |
| 02 inherited-folder (10 turns) | 27/30 (90%) | 5.5/9 (61%) | $5.25 | both |
| 03 drift-detection (4 turns) | **15/15** | **5/5** | $2.25 | **PASS** |

Three structural failure shapes recur across 01 and 02. None are checker bugs:

1. **Wrong-depth relative paths from deep subdirectories.** From `knowledge/market/competitors/vanta.md` the agent writes `../../hypotheses/X.md` when it needs `../../../hypotheses/X.md`. From `knowledge/product/roadmap.md` same shape. Affects 31 links in 01, 2 in 02. The agent has the right destination but miscounts the climb out.
2. **Missing provenance tags on hypothesis evidence rows.** In 01 the agent wrote 28 evidence rows in `hypotheses/notification-control.md` as bare claims ("Acme's ops lead reported…", "NPS for the Acme account dropped 9→6…") without the `[ingestion/...]` / `[source/...]` / `(stakeholder-verbal, …)` tag. In 02 same shape, 1 row. The vocabulary refactor reached the schema and the interview prompts, but the agent is still occasionally falling out of the vocabulary inside hypothesis files specifically.
3. **Bullet-form evidence defeats the link-counting check.** `hypothesis_evidence_count_increased_for: H-V1` reports `evidence links now=0` even when the agent added evidence — because the agent wrote the evidence as bullet text with parenthetical citations, not as `[anchor](path)` markdown links. The check counts links; the agent isn't producing them.

Scenario 02's content-judge residuals (4 fails + 1 partial out of 9) are the same set logged in the prior 02 entry — two rubric bugs and two real agent-behavior findings — unchanged by today's work.

**Decision.** Don't ship scaffold changes today. Three reasons:

- The publish gate (vocabulary refactor + drift detection + audit-trail enforcement) is intact. Scenario 03 is fully green. Scenario 01's content judges are clean. The architectural claims for the newsletter article all hold.
- The three residuals are *agent quality* shortfalls, not architectural ones. They warrant scaffold-prompt sharpening (e.g., a worked example of relative-path math from each canonical depth, a stricter "every evidence row MUST start with a tag" rule in the hypothesis schema preamble, a switch from prose citations to required-link form). That's a deliberate iteration, not a same-day hotfix on the way out the door.
- Per repo autonomy mode, skill scaffold changes are "propose and wait." These changes should be reviewed and tested, not stapled on under deadline.

**Why this isn't kicking the can.** The eval suite is doing its job: it surfaced three concrete, reproducible, agent-quality failure modes with example file paths and exact failure detail. Each can be turned into a precise scaffold edit *and* a regression test in a single later pass. Logging them here keeps them visible without forcing a rushed change.

**Files touched.** None today (residuals log only). Backlog targets when iterating: [`.claude/skills/pm-brain/scaffold/hypotheses/_SCHEMA.md`](../.claude/skills/pm-brain/scaffold/hypotheses/_SCHEMA.md) (tag-required rule, link-form requirement), [`.claude/skills/pm-brain/scaffold/CLAUDE.md`](../.claude/skills/pm-brain/scaffold/CLAUDE.md) (relative-path examples from each canonical depth), structural checker (optionally: count parenthetical citations toward `hypothesis_evidence_count_*` so it doesn't double-penalize bullet form).

---

## 2026-05-17 — Late-day fixes targeting the residual failure modes (cross-cutting)

**Finding.** Successive scenario runs over the day surfaced four small but persistent failure shapes that the previous-entry's "don't ship under deadline" call left as backlog. With clean isolation on each one, they turned out to be either checker/rubric bugs or surgical seed/scaffold improvements — not architectural problems that need design work. Worth landing.

| Failure shape | Where it surfaced | Root cause | Class |
|---|---|---|---|
| `all_internal_links_valid` flagged 4–23 false positives | 02, 06, 09, 10 | `_SCHEMA.md` files contain illustrative example links (`[ingestion/...](../ingestion/foo.md)`) to non-existent paths. Schemas are template documentation, not navigation. | Checker bug |
| Scenario 02 turn 1 timed out at 600 s (0 hypotheses produced) | 02 | Bulk-import of 10 mixed-trust artifacts = ~22–30 file writes; Sonnet cannot complete inside the harness-wide default timeout. | Harness limitation |
| Scenario 02 turn 3 judge mis-shape | 02 | Turn 3 asks for a Slack reply + memo outline (drafting); the recycled `tensions_enumerated` rubric requires an enumeration. Pass criteria couldn't match the output shape. | Rubric bug |
| Scenario 07 `audit_trail` failed because the scenario has no decision file | 07 | The `audit_trail` rubric requires `decision → hypothesis → source/`. Scenario 07 ends with a hypothesis, not a decision; the rubric was the wrong fit. | Rubric bug |
| Scenario 06 final-state orphan evidence row | 06 | Seed for artifact 6 modeled a `[source/adhoc/2025-11-22-onboarding-funnel-snapshot.md](...)` provenance tag for a file the seed never asked the agent to create. Agent dutifully wrote the broken path-tag into the decision file. | Seed bug |
| Scenarios 07 and 10 — orphan rows in hypothesis / decision files (aggregation-shaped) | 07, 10 | Agent writes summary/meta rows ("N=2 accounts, A vs B differ on…") under `Evidence for:` / `Evidence against:` without provenance tags. These are commentary, not claims — they belong under `Open questions / caveats:`. Schema already said "Evidence rows are CLAIMS, not commentary" but the aggregation case wasn't explicit. | Schema gap |
| Scenario 07 `conservative_ingestion` failed | 07 | Per-artifact ingestion records contained cross-artifact synthesis (flagging Globex contradiction inside the strategy ingestion record). `migration.md` did not explicitly say "scope each ingestion record to ONE artifact." | Prompt gap |

**Decision.** Landed all five fixes in one pass:

1. **[`tests/harness/checks/structural.py`](../tests/harness/checks/structural.py)** — `all_internal_links_valid` now skips files named `_SCHEMA.md`. Schemas demonstrate link FORM via examples; their targets are never expected to resolve in a real brain.
2. **[`tests/harness/run_scenario.py`](../tests/harness/run_scenario.py)** — added per-turn `timeout_s` and `model` overrides via `expected.yaml` turn entries. When omitted, harness-wide defaults apply. Used to bump scenario 02 turn 1 to 1200 s.
3. **[`tests/harness/judges/runway_draft.md`](../tests/harness/judges/runway_draft.md)** (new) — purpose-fit rubric for scenario 02 turn 3 (Slack reply + memo outline that buys runway without committing to a direction). Replaced `tensions_enumerated` for that turn.
4. **[`tests/harness/judges/hypothesis_audit_trail.md`](../tests/harness/judges/hypothesis_audit_trail.md)** (new) — purpose-fit rubric for scenarios that end with a freshly drafted hypothesis but no decision. Same auditability principle as `audit_trail.md`, rooted at the hypothesis. Replaced `audit_trail` in scenario 07 final-state.
5. **[`tests/scenarios/06-maintenance-sweep/inputs/turn-01-seed-accumulated-state.md`](../tests/scenarios/06-maintenance-sweep/inputs/turn-01-seed-accumulated-state.md)** — changed the artifact-6 provenance from a broken path-tag to `(stakeholder-verbal, analytics-team, 2025-11-22)`. The underlying analytics export pre-dates the brain; non-path provenance is the honest tag for it.
6. **[`.claude/skills/pm-brain/scaffold/hypotheses/_SCHEMA.md`](../.claude/skills/pm-brain/scaffold/hypotheses/_SCHEMA.md)** (mirrored to `example-brain/hypotheses/_SCHEMA.md`) — added explicit "aggregation/meta rows are NOT evidence rows" paragraph naming the exact failure shape ("N=2 accounts, A vs B differ on…") and pointing them to `Open questions / caveats:`. Also: "row summarizing across multiple artifacts" → either split into one Evidence row per artifact (each tagged) OR move to caveats with citations.
7. **[`.claude/skills/pm-brain/prompts/migration.md`](../.claude/skills/pm-brain/prompts/migration.md)** — added a hard-rule paragraph in §2: per-artifact ingestion records are scoped to ONE artifact. Cross-artifact synthesis goes to the contradiction list (§4) and to the post-migration tension-surfacing turn, not into per-artifact ingestion files.

**Why these aren't over-fitting.** Each is either tightening a rule that was already implied (the schema already said "Evidence rows are claims, not commentary" — the new paragraph just names the aggregation failure mode that the agent kept hitting), or fixing a test-infra bug that was inflating the failure signal (link validator false positives, mis-shaped rubric, missing per-turn budget control), or fixing a seed that was internally inconsistent (06 referenced a file the seed never asked anyone to create). None of these relax the audit-trail or promotion-gate criteria.

**Files touched.** Listed inline above. Mirrored scaffold changes into `example-brain/` per repo CLAUDE.md.

---

## 2026-05-17 — Second late-day pass: five more residuals after re-running everything (cross-cutting)

**Finding.** Re-running all scenarios after the first late-day pass surfaced a second cluster of small-but-fixable issues. Scenarios 04, 06, 08, 09 came back fully green; 05, 07, 10 still failed but each with a *different* shape from the originally-logged failure modes — meaning the earlier fixes worked, just exposed the next layer underneath.

| Failure shape | Where it surfaced | Root cause | Class |
|---|---|---|---|
| Scenario 04 final-state: 12 broken links + 2 orphans | 04 | Seed text included path-typed `[source/interviews/2026-03-*.md]` tags for interviews conducted BEFORE PM Brain existed — files the scenario never asks the agent to create. Agent propagated the broken paths into persona, insights, decision files. | Seed bug (same shape as scenario 06 prior) |
| Scenario 07 false-positive orphan on `*(none from current sources)*` | 07 | `_PAREN_ABSENCE_RE` required the row to start with `(`. Agents sometimes wrap the placeholder in italics: `*(none from current sources)*`. Regex didn't tolerate leading markdown markers. | Checker bug |
| Scenario 07 `conservative_ingestion` still failing after first strengthening | 07 | A single paragraph at the end of §2 of `migration.md` was not enough — Sonnet kept smuggling cross-artifact tension notes into per-artifact ingestion files. | Prompt gap (deeper) |
| Scenario 05 `overdue_surfaced_in_review` failed despite correct content | 05 | Agent gave Diana's staleness as "56 days" / "March 2026" / "8 weeks ago" — all factually correct and equivalent to the seeded date — but the rubric required literal `2026-03-22` or `March 22`. The rubric was enforcing format, not understanding. | Rubric over-specification |
| Scenarios 05, 10 final-state: 8–12 orphan evidence rows in hypothesis + decision files | 05, 10 | Agent paraphrases a claim from an ingestion file into an Evidence row and forgets to add the provenance tag. Schema preamble already said "every row must carry a tag" but didn't give the agent a *mechanical* pre-save check. | Schema gap |
| Scenario 07 `hypothesis_proposed_from_artifacts` failed despite correct hypothesis | 07 | Judge wrote a self-correcting reasoning chain: "VERDICT: FAIL — more than one file… however, re-reading the rubric: all five are within a single file… VERDICT: PASS". The harness's bottom-up line scanner matched the first `VERDICT:` on the bottom-most line (FAIL) because `(.*)` greedy capture consumed through the final PASS. | Parser bug |

**Decision.** Landed all five in one pass:

1. **[`tests/scenarios/04-persona-emergence/inputs/turn-01-seed-existing-personas.md`](../tests/scenarios/04-persona-emergence/inputs/turn-01-seed-existing-personas.md)** — replaced four sets of path-typed `[source/interviews/2026-03-*]` tags with `(stakeholder-verbal, <name>-<context>, 2026-03-DD)` enum tags. Added a clarifying inline note: "(sourced — these came from interviews done BEFORE PM Brain existed, so the original notes are not in `source/`; tag accordingly with the non-path enum)". Same fix shape as the prior scenario 06 seed fix.
2. **[`tests/harness/checks/structural.py`](../tests/harness/checks/structural.py)** — `_PAREN_ABSENCE_RE` now allows leading italic/bold/code markers (`*`, `_`, `` ` ``) before the opening paren. A row like `*(none from current sources)*` is now correctly recognized as an absence-marker placeholder, not an orphan claim.
3. **[`.claude/skills/pm-brain/prompts/migration.md`](../.claude/skills/pm-brain/prompts/migration.md)** — promoted the per-artifact scope rule to a dedicated §2a "HARD RULE" section with: explicit "Do NOT" list (4 items), concrete DON'T/DO code examples, and a pre-save self-check naming the forbidden phrases ("conflicts with", "contradicts", "tension with", "in contrast to", "differs from"). The first-pass strengthening was a paragraph; this is a sub-section with an enforcement checklist.
4. **[`tests/scenarios/05-stakeholder-cadence/judges/overdue_surfaced_in_review.md`](../tests/scenarios/05-stakeholder-cadence/judges/overdue_surfaced_in_review.md)** — relaxed pass criteria to accept ANY quantitatively-specific staleness reference for Diana / Marcus: ISO date, "March 22", day-count that resolves to the date ("56 days", "~8 weeks"), or "March 2026" + numeric gap. Added clarifying clause: "The judge's job is to confirm the agent retrieved the stakeholder file and reasoned over its content — not to enforce a single date format." Same flexibility applied to Marcus.
5. **[`.claude/skills/pm-brain/scaffold/hypotheses/_SCHEMA.md`](../.claude/skills/pm-brain/scaffold/hypotheses/_SCHEMA.md)** + **[`.claude/skills/pm-brain/scaffold/decisions/_SCHEMA.md`](../.claude/skills/pm-brain/scaffold/decisions/_SCHEMA.md)** (mirrored to `example-brain/`) — added a **COUNT-THE-TAGS** pre-save self-check as item #1 of each schema preamble. The rule: count bullet rows under Evidence sections, count provenance tags in those rows, the numbers MUST match. Closes with: "This single check catches the most common failure mode: paraphrasing a claim from an ingestion record into an Evidence row and forgetting the tag." Mechanical instead of conceptual — the agent can't gloss past it.
6. **[`tests/harness/checks/content.py`](../tests/harness/checks/content.py)** — verdict parser rewrite. New regex uses a tempered greedy capture (`(?:(?!VERDICT\s*:)[^\n])*`) so `finditer` returns every `VERDICT:` token in the text, not just the first. The parser now takes the *last* verdict — which is what self-correcting judges intend. Unit-tested against 8 cases including the bottom-line-with-both-FAIL-and-PASS shape.

**Why these aren't over-fitting.** Each fix has the same character as the first late-day pass: tightening a rule that was already implied (COUNT-THE-TAGS makes the existing "every row needs a tag" rule mechanical instead of conceptual), fixing a test-infra bug that was inflating the failure signal (regex, parser, over-specified rubric), or fixing a seed that was internally inconsistent (04, same shape as 06). The judge-format relaxation explicitly *isn't* relaxing the audit-trail principle — it's relaxing the format check while keeping the substantive requirement that Diana and Marcus must each be named with a specific staleness reference grounded in their stakeholder files.

**On Opus pinning.** Considered and not used. Every failure here had a non-Opus fix path. Opus pinning is reserved for cases where Sonnet *can* recognize the right answer when shown a tighter rubric / clearer schema, but consistently mis-executes — none of today's failures had that shape.

**Files touched.** Listed inline above. Mirrored scaffold changes into `example-brain/` per repo CLAUDE.md.

---

## 2026-05-17 — Third late-day pass: behavior + judgment-quality gaps (cross-cutting)

**Finding.** After the parser fix + COUNT-THE-TAGS schema + per-turn rubric work landed, a third re-run round reduced failures further. Scenario 07 went fully green. Scenarios 04, 06, 08, 09, 10 stayed green. Three behavior gaps remained, all rooted in the brain's prompt/schema layer rather than in test infra:

| Failure shape | Where it surfaced | Root cause | Class |
|---|---|---|---|
| Scenario 05 `irrelevant_overdue_not_flagged` 0.5 fail | 05 | Agent put Helena (stalest stakeholder at 10 weeks) in pre-launch-blocking-decision table for Custom Dashboards despite her file saying "as-needed cadence, not implicated in feature-level deprecations unless infra cost shifts materially." The `/review` command treated raw staleness as the only signal — didn't filter on whether the stakeholder's stake was actually touched by the framed decision. | Command-prompt gap |
| Scenario 01 `market_signal_added` 1-in-7 fail | 01 | Agent at turn 3 promoted hypothesis confidence to "two independent sources" by counting an n=12 churn cohort + 5 exit-survey responses as a second source confirming the same theme already raised by one interview. Correlational data treated as causal; same-population reports double-counted. Scaffold CLAUDE.md had no explicit guard. | Scaffold gap (judgment) |
| Scenario 02 `insight_promoted_with_dissent` fail | 02 | After turn 8 (third independent signal for shared-budgets), agent updated hypothesis file but left `knowledge/users/insights.md` as a blank template. Scaffold's "Memory promotion" section was generic ("promote into knowledge/") without binding signal types to canonical homes. | Scaffold gap (mechanical) |
| Scenario 02 `no_orphan_evidence` fail | 02 | Agent wrote rows like "No direct counter-signal in the inherited data" as bullets under `Evidence against:`. These are meta-commentary about absence, not claims — but the schema didn't explicitly name this shape as forbidden, and the orphan-evidence regex only recognizes parenthetical placeholders like `(none yet)`. | Schema gap |

**Decision.** Landed all four:

1. **[`.claude/skills/pm-brain/scaffold/.claude/commands/review.md`](../.claude/skills/pm-brain/scaffold/.claude/commands/review.md)** (mirrored to `example-brain/.claude/commands/review.md`) — added new section "Decision-scoped /review — relevance filter on cadence flags". When PM frames `/review` around a specific decision in flight, the stakeholder-cadence check MUST filter on relevance to that decision (read the stakeholder file's `What they care about` / `Concerns` / explicit boundaries), not raw staleness. Stale AND relevant → name them in the should-contact-before-decision list with a one-line tie to their stake. Stale BUT not relevant → omit or put in a clearly-separated "other cadence notes — not blocking this decision" section. **Never mix the two lists.** Names the exact failure shape: a stakeholder whose own file declares as-needed cadence on feature-level deprecations is not a pre-launch check on a deprecation that doesn't shift infra cost — even at 10 weeks stale.
2. **[`.claude/skills/pm-brain/scaffold/CLAUDE.md`](../.claude/skills/pm-brain/scaffold/CLAUDE.md)** (mirrored to `example-brain/CLAUDE.md`) — added "Correlational vs. causal — don't promote on weak data" paragraph after the recency-bias paragraph in § Evidence hierarchy. Three sub-bullets: sample size (N=12 cohort + 5 exit-survey = watch item, not second source), confounders, **same-domain independence** (a customer interview saying "notifications are overwhelming" and an exit-survey citing "notification overload" are NOT two independent sources — same population, same theme, different channel). Closes with: "Do not bump the hypothesis confidence level on the strength of one correlational signal."
3. **[`.claude/skills/pm-brain/scaffold/CLAUDE.md`](../.claude/skills/pm-brain/scaffold/CLAUDE.md)** (mirrored) — added "Where promotion lands — the canonical homes (not optional)" sub-section right under "Memory promotion". Binds signal type → canonical home: user-level pattern → `knowledge/users/insights.md § Active themes`, persona claim → `knowledge/users/personas.md`, product-level pattern → `knowledge/product/metrics.md` or feature file, market pattern → `knowledge/market/landscape.md` or competitors file. Names the most-missed failure: "If you find yourself thinking 'I promoted the hypothesis, I'm done' — you're not done; the insights.md row is the other half."
4. **[`.claude/skills/pm-brain/scaffold/hypotheses/_SCHEMA.md`](../.claude/skills/pm-brain/scaffold/hypotheses/_SCHEMA.md)** (mirrored to `example-brain/hypotheses/_SCHEMA.md`) — added "Empty-state for Evidence sections — don't write meta-rows" paragraph. Tells the agent: when Evidence-for or Evidence-against has no claims yet, leave NO bullets or write a single italicized `_(none yet)_` marker. Do NOT write "No counter-evidence in current data" as a bullet — that's commentary on absence, not a claim. If you want to record that you actively looked, put a one-liner under `Open questions / caveats:` instead.

**Why these aren't over-fitting.** The cadence-relevance fix tightens an existing rule (stakeholder files already declare boundaries; `/review` was just ignoring them) rather than relaxing the bar — it's saying respect what the stakeholder file already says, not "stop surfacing overdue stakeholders." The correlational-vs-causal paragraph is restating standard evidence hygiene that every PM-credible source teaches; the failure was that the scaffold didn't say it explicitly. The promotion-canonical-homes fix is mechanical (signal type → file) and patches a real gap where the brain was leaving its most queryable user-knowledge layer empty. The empty-state evidence-row guidance closes a specific orphan-class the audit was correctly flagging.

**On the remaining Sonnet variance.** Scenario 01's `market_signal_added` passes ~6/7 runs of Sonnet. The 1/7 failures are model variance, not a scaffold gap. After the correlational-vs-causal addition lands, the expected variance drops further — but Sonnet under subscription throttling will occasionally produce a confidence-bumping turn even with the guard in place. The next escalation step (not taken here) is pinning that one judge's *target turn* to Opus via per-turn `model: opus` in `expected.yaml`. Held off because the marginal gain doesn't justify the cost yet — green-rate is already 9/10 stable + 1/10 ~85% stable.

**Files touched.** Listed inline above. Mirrored scaffold changes into `example-brain/` per repo CLAUDE.md.

---

## Template for future entries

```markdown
## YYYY-MM-DD — Short title (scenario or "cross-cutting")

**Finding.** What the eval run revealed.

**Decision.** What we changed in response, and what we explicitly did NOT change.

**Why this isn't [over-fitting / lowering the bar / scope creep].** One paragraph on the design principle.

**Files touched.** Relative links to the changed files.
```
