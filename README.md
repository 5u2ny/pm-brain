# PM Brain

**A second brain for product managers.** Your PM context — interviews, decisions, hypotheses, stakeholder claims, strategy — lives as plain markdown files in a folder on your laptop. Claude reads them before answering, writes to them after, and runs a weekly sweep that flags what's drifting.

You manage one product. Your context is scattered across Notion, Linear, Slack, your dashboards, and your head. You ship a feature. Six weeks later, nobody remembers why you killed the other option. PM Brain fixes that.

> **See it in action:** [A week with PM Brain — Lena's first five days](./docs/walkthrough.md) is a short story of one PM using it on a real team. New here? Start there.

## What it is

A folder of markdown files in a git repo, plus one short operating manual (`CLAUDE.md`) that tells Claude how to use them. The agent loads the right files before a task, updates the right files after, and surfaces contradictions you'd otherwise miss.

The folder is organized around how PM work actually flows:

- **`knowledge/`** — your stable picture of strategy, product, users, market, and org
- **`hypotheses/`** — things you're tracking the evidence for
- **`decisions/`** — calls you've made, with the evidence trail and what would reopen them
- **`stakeholders/`** — one file per person, with their asks and concerns
- **`ingestion/`** — synthesis of every interview, meeting, doc, or message the brain has read
- **`source/`** — the untouched originals, so the audit trail stays intact

Every claim wears a small tag — a **provenance** marker — that says where it came from: a documented interview, a verbal stakeholder comment, your own hunch, or general industry knowledge. The brain treats them with appropriate weight. (Full list in the [glossary](./docs/glossary.md).)

No vector database. No embeddings. No auto-tagging. The whole brain is human-readable; you can open it in any editor.

## What it isn't

- Not a notes app — it's an opinionated structure with maintenance built in
- Not a chatbot with memory — the memory lives in your repo, not in Claude
- Not a vector database — every file is plain markdown, grep-able by you
- Not autonomous product management — judgment stays with you; the brain makes the boring cross-referencing easier

## Install

```bash
# Drop the skill into your Claude Code skills directory
cp -R .claude/skills/pm-brain ~/.claude/skills/

# Open Claude Code in the directory where you want the brain
cd ~/projects/my-product-brain

# Invoke
/pm-brain
```

The skill detects what's already in the directory. An empty folder gets a fresh start (**greenfield**). A folder with existing PM artifacts — Notion exports, a Jira CSV, meeting notes — gets read and absorbed (**migration**). Either way, a short 5-batch interview captures company, role, and current priorities. The scaffold drops in, the brain commits locally. Never pushes.

## The six commands

| Command | What it does |
|---|---|
| `/ingest <thing>` | Feed an artifact into the brain — a file, a paste, a quick note in chat. The skill figures out the shape (interview, meeting, market signal, ad-hoc) and routes it. |
| `/prep <stakeholder>` | One-page brief before a meeting: their open asks, last unresolved concern, suggested questions. |
| `/review` | Weekly sweep. Six checks across the brain. Fixes small things directly, drafts the bigger ones for your call. |
| `/ideate <problem>` | Synthesis, not brainstorm. Loads strategy, insights, and hypotheses. Surfaces 3–7 directions, each tagged with the evidence behind it. |
| `/risk <feature>` | Five-area risk scan. Drafts hypothesis stubs for any area with no coverage. |
| `/plan <objective>` | Six-block draft plan: what we know, assumption vs evidence, who to interview, hypotheses to open, experiments to run, decision points. |

## Repo layout

```
.claude/skills/pm-brain/    # The canonical skill — install this
example-brain/              # Pre-scaffolded instance (browseable demo)
tests/                      # Eval suite — synthetic scenarios + harness
docs/                       # Architecture, how it works, testing, prior art
```

## Tests

Synthetic scenarios + a harness that runs them through the skill via `claude -p` and asserts the brain's state after each turn. Three eval layers — **structural** (deterministic Python asserts), **content** (LLM-as-judge with tight rubrics), **convergence** (per-assertion pass rate across N runs).

```bash
python tests/harness/run_scenario.py tests/scenarios/01-b2b-churn
```

Full reference — scenario format, ground-truth schema, harness internals, assumptions, cost model, current coverage, gaps, and how to add a scenario — lives in [`tests/TESTING.md`](./tests/TESTING.md). The 90-second operator quickstart is in [`tests/README.md`](./tests/README.md). Design rationale (why scenarios over per-turn unit tests, why LLM-as-judge is reserved) is in [`docs/testing.md`](./docs/testing.md).

## Docs

- [`docs/walkthrough.md`](./docs/walkthrough.md) — *Start here.* A week with PM Brain, told as a story
- [`docs/glossary.md`](./docs/glossary.md) — every term used in PM Brain, defined in plain English
- [`docs/how-it-works.md`](./docs/how-it-works.md) — the technical version of the walkthrough, with files and folders
- [`docs/architecture.md`](./docs/architecture.md) — the design choices (deterministic scaffold + adaptive prompts) and why
- [`docs/testing.md`](./docs/testing.md) — how the eval suite works, scenario format, ground-truth schema
- [`docs/testing-decisions.md`](./docs/testing-decisions.md) — running log of what eval runs taught us and the design calls that came out of them. Read when an assertion or scaffold rule looks arbitrary and you want to know *why it's there*.
- [`docs/prior-art.md`](./docs/prior-art.md) — Zettelkasten, RAG memory, agent OS patterns: what's borrowed and what's new

## Composing with PM Skills

PM Brain is the memory layer. [PM Skills](https://github.com/phuryn/pm-skills) are the workflow modules — how to run a JTBD interview, how to score with RICE, how to design an experiment. They compose: the skill is how to do the work once, the brain is what you know across all the times you did it.

## License

MIT.

## Credits

Designed and maintained by [Paweł Huryn](https://www.productcompass.pm). Full long-form on Product Compass: [PM Brain OS](https://www.productcompass.pm/p/pm-brain-os).
