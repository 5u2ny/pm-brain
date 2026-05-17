# Ingestion Modes

Every mode follows the same shape: **load → process → route updates → surface what changed.**

All modes feed back into strategy when relevant — opportunities, user needs, and market signals can inform `knowledge/strategy.md` just as much as strategy informs which signals matter. When an ingested signal conflicts with strategy, append to `strategy.md § Tensions`. Do not reject the signal automatically.

## 1. Customer interview (`/ingest interview <file>` or paste transcript)

Input: transcript (raw or lightly cleaned).
Process:
1. Extract: pains, JTBDs, current alternatives, surprising quotes, contradictions with prior insights.
2. Map to existing personas / segments (`knowledge/users/`).
3. Compare against active hypotheses — does anything confirm or contradict?
4. Generate up to 3 new hypothesis candidates if signal warrants.

Updates:
- `knowledge/users/insights.md` — themes
- `knowledge/users/personas.md` / `segments.md` — only if a persona meaningfully shifts
- `hypotheses/<feature>.md` — evidence-for / evidence-against entries
- `ingestion/interviews/YYYY-MM-DD-<participant>.md` — synthesized record

Surface: "Affected hypotheses: …. New candidates: …. Persona drift detected: yes/no."

## 2. Meeting / 1:1 notes (`/ingest meeting <file>`)

Input: notes from a 1:1, review, or cross-functional sync.
Process:
1. Extract: decisions made, action items (mine vs theirs), stakeholder-specific signals, open questions.
2. If stakeholder(s) identifiable, update their `stakeholders/<slug>.md` (touchpoint log, open asks, concerns).
3. If a decision was made, draft a record in `decisions/` for PM confirmation.

Updates:
- `stakeholders/<slug>.md`
- `decisions/YYYY-MM-DD-<slug>.md` (draft)
- `ingestion/meetings/YYYY-MM-DD-<topic>.md`

## 3. Market / competitor intel (`/ingest market <url-or-file>`)

Input: article, screenshot, tweet, competitor changelog, analyst note.
Process:
1. Identify which competitor / trend it touches.
2. Update the relevant file in `knowledge/market/competitors/` or `trends.md`.
3. Flag any active hypothesis or strategy element it contradicts or supports.

Updates:
- `knowledge/market/competitors/<slug>.md` or `trends.md`
- `hypotheses/*` if directly relevant
- `knowledge/strategy.md § Tensions` if the signal conflicts with strategy

## 4. Ad-hoc (`/ingest adhoc` or any unstructured dump)

Input: anything the PM thinks is worth capturing but isn't an interview / meeting / market signal.
Process:
1. Read it. Decide where it belongs.
2. If unclear, ask **one** question to disambiguate.
3. Route to the right area file. Never park indefinitely in `ingestion/adhoc/` — that folder is a sorting bench, not a graveyard.

Rule: every adhoc item is resolved (routed or discarded) within the same session.
