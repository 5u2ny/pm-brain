"""
structural.py — deterministic assertion helpers used by run_scenario.py.

Each helper takes the work_dir (Path) and the assertion args from expected.yaml,
returns {"name": str, "passed": bool, "detail": str}.

Conventions:
  - All paths in expected.yaml are RELATIVE to work_dir.
  - Glob patterns use ** for recursive match.
  - Returns must always have all three keys, even on failure.

STATUS
    Skeleton. A Claude session working in this repo should implement the TODOs.
"""

from pathlib import Path
import re


# ============================================================
# File presence
# ============================================================

def file_exists(work_dir: Path, path: str) -> dict:
    p = work_dir / path
    return {
        "name": f"file_exists:{path}",
        "passed": p.is_file(),
        "detail": "" if p.is_file() else f"not found: {p}",
    }


def file_exists_glob(work_dir: Path, pattern: str) -> dict:
    matches = list(work_dir.glob(pattern))
    return {
        "name": f"file_exists_glob:{pattern}",
        "passed": len(matches) > 0,
        "detail": "" if matches else f"no matches for {pattern}",
    }


def file_modified_or_created(work_dir: Path, path: str) -> dict:
    """Either the file exists (created) OR was modified after scenario start."""
    p = work_dir / path
    return {
        "name": f"file_modified_or_created:{path}",
        "passed": p.is_file(),
        "detail": "" if p.is_file() else f"not present: {p}",
    }


# ============================================================
# Hypothesis lifecycle
# ============================================================

def hypothesis_count_at_least(work_dir: Path, n: int) -> dict:
    """
    Count hypothesis files under hypotheses/ (excluding INDEX, _SCHEMA, .gitkeep).

    TODO: tighten — should probably look INSIDE each file for at least one risk-area
    section with content, since an empty stub doesn't count as a real hypothesis.
    """
    h_dir = work_dir / "hypotheses"
    if not h_dir.is_dir():
        return {"name": f"hypothesis_count_at_least:{n}", "passed": False,
                "detail": "hypotheses/ dir missing"}
    files = [p for p in h_dir.glob("*.md")
             if p.name not in {"INDEX.md", "_SCHEMA.md"} and not p.name.startswith(".")]
    return {
        "name": f"hypothesis_count_at_least:{n}",
        "passed": len(files) >= n,
        "detail": f"found {len(files)} hypothesis files",
    }


def hypothesis_evidence_count_increased_for(work_dir: Path, hypothesis_id: str) -> dict:
    """
    Was at least one evidence row added to <hypothesis_id> since the previous turn?

    TODO: requires diffing against a snapshot taken before the turn ran.
    run_scenario.py should pass before/after snapshots into this helper.
    """
    return {
        "name": f"hypothesis_evidence_count_increased_for:{hypothesis_id}",
        "passed": False,
        "detail": "not_implemented — requires before/after snapshot",
    }


def hypothesis_evidence_count_unchanged_for(work_dir: Path, hypothesis_id: str) -> dict:
    """
    Negative assertion: agent should NOT have added evidence to <hypothesis_id> this turn.
    Used to verify low-signal rejection (turn 5 in 01-b2b-churn).
    """
    return {
        "name": f"hypothesis_evidence_count_unchanged_for:{hypothesis_id}",
        "passed": False,
        "detail": "not_implemented — requires before/after snapshot",
    }


# ============================================================
# Decisions
# ============================================================

def all_decisions_have_reversal_condition(work_dir: Path) -> dict:
    """
    Every file under decisions/ (excluding INDEX, _SCHEMA) must contain a
    'what would reverse this' field. The presence test is structural;
    the *quality* of the reversal condition is a content (LLM-judge) check.
    """
    d_dir = work_dir / "decisions"
    if not d_dir.is_dir():
        return {"name": "all_decisions_have_reversal_condition", "passed": True,
                "detail": "decisions/ dir absent (vacuous pass)"}
    decision_files = [p for p in d_dir.glob("*.md")
                      if p.name not in {"INDEX.md", "_SCHEMA.md"}]
    missing = []
    for f in decision_files:
        text = f.read_text().lower()
        if "what would reverse" not in text and "reversal condition" not in text:
            missing.append(f.name)
    return {
        "name": "all_decisions_have_reversal_condition",
        "passed": len(missing) == 0,
        "detail": "" if not missing else f"missing in: {missing}",
    }


# ============================================================
# Link integrity
# ============================================================

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def all_internal_links_valid(work_dir: Path) -> dict:
    """
    Walk every .md file under work_dir. For every relative markdown link
    that doesn't start with http(s)://, mailto:, or #, verify the target file exists.
    """
    broken = []
    for md_file in work_dir.rglob("*.md"):
        for m in LINK_RE.finditer(md_file.read_text()):
            target = m.group(2).split("#", 1)[0].strip()
            if not target:
                continue
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (md_file.parent / target).resolve()
            if not resolved.exists():
                broken.append(f"{md_file.relative_to(work_dir)} -> {target}")
    return {
        "name": "all_internal_links_valid",
        "passed": len(broken) == 0,
        "detail": "" if not broken else f"broken: {broken[:10]}",
    }


def no_orphan_evidence(work_dir: Path) -> dict:
    """
    Every evidence row in hypotheses/ should link to a source/ or ingestion/ file
    that actually exists. Orphan evidence = a claim with no audit anchor.

    TODO: parse hypothesis evidence sections, extract links, verify resolved paths
    under source/ or ingestion/.
    """
    return {
        "name": "no_orphan_evidence",
        "passed": False,
        "detail": "not_implemented",
    }


def no_silent_hypothesis_demotion(work_dir: Path) -> dict:
    """
    Any hypothesis whose status was lowered (active → deprecated, promoted → demoted)
    must have a corresponding evidence-against row added in the same turn.

    TODO: needs turn-level diff. run_scenario.py should track status transitions.
    """
    return {
        "name": "no_silent_hypothesis_demotion",
        "passed": False,
        "detail": "not_implemented",
    }


# ============================================================
# Dispatch
# ============================================================

DISPATCH = {
    "file_exists": file_exists,
    "file_exists_glob": file_exists_glob,
    "file_modified_or_created": file_modified_or_created,
    "hypothesis_count_at_least": hypothesis_count_at_least,
    "hypothesis_evidence_count_increased_for": hypothesis_evidence_count_increased_for,
    "hypothesis_evidence_count_unchanged_for": hypothesis_evidence_count_unchanged_for,
    "all_decisions_have_reversal_condition": all_decisions_have_reversal_condition,
    "all_internal_links_valid": all_internal_links_valid,
    "no_orphan_evidence": no_orphan_evidence,
    "no_silent_hypothesis_demotion": no_silent_hypothesis_demotion,
}


def run_assertion(work_dir: Path, assertion: dict | str) -> dict:
    """
    assertion can be either:
      - "name: value"   (string form for single-arg assertions)
      - {key: value}    (dict form, key is the assertion name)
    """
    if isinstance(assertion, str):
        if ":" in assertion:
            name, _, arg = assertion.partition(":")
            return DISPATCH.get(name.strip(),
                                lambda *_: {"name": assertion, "passed": False, "detail": "unknown assertion"}
                                )(work_dir, arg.strip())
        return DISPATCH.get(assertion.strip(),
                            lambda *_: {"name": assertion, "passed": False, "detail": "unknown assertion"}
                            )(work_dir)
    if isinstance(assertion, dict):
        # Expect single key
        (name, arg), = assertion.items()
        fn = DISPATCH.get(name)
        if not fn:
            return {"name": name, "passed": False, "detail": "unknown assertion"}
        return fn(work_dir, arg)
    return {"name": str(assertion), "passed": False, "detail": "malformed assertion"}
