# PM Brain

A markdown-native second brain for product managers, built as a Claude Code skill.

You manage one product. Your context lives in five places: Notion, Linear, Slack, your dashboards, and your head. You ship a feature. Six weeks later, nobody remembers why you killed the other option.

PM Brain fixes that. It runs as markdown files in a git repo with a single `CLAUDE.md` operating manual. No vector database. No embeddings. No auto-tagging. The agent loads relevant context before a task, updates the right files after, and runs a weekly maintenance sweep that compresses what's worth keeping and flags what's drifting.

## What it is

- Markdown files in a git repo
- One `CLAUDE.md` operating manual the agent reads at the start of every session
- Five knowledge areas (strategy, product, users, market, org)
- Three lifecycle areas (hypotheses, decisions, stakeholders)
- Four ingestion modes (interviews, meetings, market, ad-hoc)
- One maintenance loop that runs weekly

## What it isn't

- Not a notes app
- Not a chatbot with memory
- Not a vector database
- Not autonomous product management

## Install

```bash
# Drop the skill into your Claude Code skills directory
cp -R .claude/skills/pm-brain ~/.claude/skills/

# Open Claude Code in the directory where you want the brain
cd ~/projects/my-product-brain

# Invoke
/pm-brain
```

The skill detects mode (greenfield, migration, or active repo), runs a focused 5-batch interview, copies a deterministic scaffold into the directory, and commits locally. Never pushes.

## The six verbs

| Command | What it does |
|---|---|
| `/ingest <source>` | Route an artifact into the brain. Auto-detects shape (interview, meeting, market, ad-hoc). Updates `ingestion/` plus whichever durable areas apply. |
| `/prep <stakeholder>` | Read-only at call time. Surfaces open asks, last unresolved concern, suggested questions. |
| `/review` | Weekly sweep. Six checks. Edits directly where confidence is high, drafts where not. |
| `/ideate <problem>` | Synthesis, not brainstorm. Loads strategy + insights + hypotheses. Surfaces 3-7 directions tagged with evidence. |
| `/risk <feature>` | 5-area risk scan. Drafts hypothesis stubs for any area with no coverage. |
| `/plan <objective>` | Drafts a six-block plan: what we know, assumption vs evidence, who to interview, hypotheses to open, experiments, decision points. |

## Repo layout

```
.claude/skills/pm-brain/    # The canonical skill — install this
example-brain/              # Pre-scaffolded instance (browseable demo)
tests/                      # Eval suite — synthetic scenarios + harness
docs/                       # Architecture, how it works, testing, prior art
```

## What's in `tests/`

Synthetic scenarios + a harness that runs them through the skill via `claude -p` and asserts the brain's state after each turn. Tests verify three layers:

- **Structural** — file presence, schema validity, INDEX integrity (deterministic)
- **Content** — did the right hypothesis get promoted? was the contradiction surfaced? (LLM-as-judge with rubrics)
- **Convergence** — across N runs of the same scenario, what's the pass rate per assertion? (statistical)

See [`tests/README.md`](./tests/README.md) and [`docs/testing.md`](./docs/testing.md).

## Docs

- [`docs/architecture.md`](./docs/architecture.md) — the layered split (deterministic scaffold + adaptive prompts) and why
- [`docs/how-it-works.md`](./docs/how-it-works.md) — ingestion → knowledge / hypotheses / decisions lifecycle, with a worked example
- [`docs/testing.md`](./docs/testing.md) — how the eval suite works, scenario format, ground-truth schema
- [`docs/prior-art.md`](./docs/prior-art.md) — Zettelkasten, RAG memory, agent OS patterns, what's borrowed and what's new

## Composing with PM Skills

PM Brain is the memory layer. [PM Skills](https://github.com/phuryn/pm-skills) are the workflow modules — how to run a JTBD interview, how to score with RICE, how to design an experiment. They compose: the skill is how to do the work once, the brain is what you know across all the times you did it.

## License

MIT.

## Credits

Designed and maintained by [Paweł Huryn](https://www.productcompass.pm). Full long-form on Product Compass: [PM Brain OS](https://www.productcompass.pm/p/pm-brain-os).
