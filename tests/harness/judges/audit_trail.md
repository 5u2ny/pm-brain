# Judge: audit_trail

## What we're checking

The entire architectural promise of PM Brain is that every durable claim traces back to a `source/` artifact through working markdown links. This is the auditability claim.

Starting from the decision file produced at turn 10, you should be able to navigate the chain:

```
decision → hypothesis → ingestion record → source artifact
```

Two clicks deep. Every step a working markdown link. If any link breaks, the audit chain is broken, and the system's load-bearing promise is broken.

This is the final-state assertion. Run it after all turns complete.

## You will be given

- The full work_dir (the brain after all 10 turns).
- The target file: the decision created at turn 10.

## Pass criteria

ALL of the following must be true:

- The decision file's evidence references include working markdown links to:
  - At least one hypothesis file under `hypotheses/`.
  - At least three ingestion records under `ingestion/interviews/` (Acme, Stripe, Notion at minimum).
  - At least one source artifact under `source/`.
- Following each link from the decision file resolves to a real file (no 404s on relative paths).
- Walking from the decision into the linked hypothesis, the hypothesis itself contains working links to ingestion records and source files.
- At least one full chain works end to end: `decision → hypothesis → ingestion → source/` with every step a valid relative markdown link.

## Fail criteria (must_not)

- Any link in the decision file is broken.
- The hypothesis the decision references doesn't itself link to its evidence sources.
- An ingestion record exists but no source artifact (broken at the bottom of the chain).
- The decision references evidence by name but doesn't link it (a claim without an audit anchor).

## Output format

```
VERDICT: PASS
VERDICT: FAIL — <one-line reason>
VERDICT: UNCERTAIN — <one-line reason>
```
