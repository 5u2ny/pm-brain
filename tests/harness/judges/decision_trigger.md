# Judge: decision_trigger

## What we're checking

At turn 7, the PM asks the agent to synthesize the case without drafting a decision yet. This is the "load and reason" step that should precede the actual decision write.

The agent's response (visible in stdout from the `claude -p` invocation, or in any artifact it writes) should:

- Reference every ingested artifact by slug (Acme, Stripe, Brex, eng sync, churn snapshot, pricing thread).
- Explicitly address the Brex contradiction as a contradiction, not as a footnote.
- Name what's still ambiguous (the third compliance-ops interview hasn't happened yet, no segmentation data, no quantitative churn-cause test).
- NOT draft a decision file.

## You will be given

- The agent's response (stdout) from turn 7.
- All markdown files under the brain (for verifying no decision was prematurely written).
- The turn context: turn 7, decision trigger.

## Pass criteria

ALL of the following must be true:

- The agent's response references every prior ingestion artifact by slug or by clear identifier.
- The Brex interview is explicitly named as a contradiction (not buried in a "diverse customer feedback" framing).
- The persona-split insight from Brex (mid-market ops splitting into compliance-ops and operational-risk-ops) is named in the synthesis.
- The synthesis names at least one specific ambiguity or missing piece.
- No new file under `decisions/` was created on this turn.

## Fail criteria (must_not)

- A decision file was drafted on this turn (the PM explicitly said don't).
- The Brex contradiction was flattened ("most customers want weekly, one wanted real-time").
- The agent claims higher certainty than the evidence supports ("we now know that mid-market wants weekly").
- The synthesis is vague — no specific artifact references, just generalities.

## Output format

```
VERDICT: PASS
VERDICT: FAIL — <one-line reason>
VERDICT: UNCERTAIN — <one-line reason>
```
