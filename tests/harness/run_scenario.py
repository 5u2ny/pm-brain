#!/usr/bin/env python3
"""
run_scenario.py — execute a single PM Brain test scenario.

USAGE
    python tests/harness/run_scenario.py tests/scenarios/01-b2b-churn
    python tests/harness/run_scenario.py tests/scenarios/01-b2b-churn --runs 5
    python tests/harness/run_scenario.py tests/scenarios/01-b2b-churn --runs 5 --max-cost 25

WHAT IT DOES
    For each run:
      1. Creates a fresh temp dir.
      2. Bootstraps the PM Brain scaffold into the temp dir via the canonical skill.
      3. Iterates through scenario inputs/ in filename order. For each turn:
         - Invokes `claude -p <prompt>` in the temp dir, feeding the turn's input.
         - Runs the turn's structural assertions from expected.yaml.
         - Runs the turn's content (LLM-judge) assertions.
      4. At scenario end, runs final_state assertions.
      5. Writes results to tests/results/<date>-<scenario>-<run>.json.

    Across N runs, computes pass rates per assertion and compares to pass_threshold.

STATUS
    Skeleton. The hard work is in:
      - actually shelling out to `claude -p` and feeding it inputs
      - parsing the agent's tool calls / file writes to know what happened
      - running judge calls cleanly
      - aggregating results

    A Claude session working in this repo should implement the TODOs below.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("ERROR: PyYAML required. pip install pyyaml\n")
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SKILL_PATH = REPO_ROOT / ".claude" / "skills" / "pm-brain"
RESULTS_DIR = REPO_ROOT / "tests" / "results"


# ============================================================
# Scenario loading
# ============================================================

def load_scenario(scenario_dir: Path) -> dict:
    """Load expected.yaml + sorted list of input files."""
    expected = yaml.safe_load((scenario_dir / "expected.yaml").read_text())
    inputs = sorted((scenario_dir / "inputs").glob("turn-*.md"))
    return {"expected": expected, "inputs": inputs}


# ============================================================
# Brain bootstrap
# ============================================================

def bootstrap_brain(work_dir: Path) -> None:
    """
    Bootstrap a fresh PM Brain in work_dir via the canonical skill.

    TODO: decide whether to:
      (a) call `claude -p "/pm-brain"` and let the skill handle init through its full interview flow
          (slower, exercises the real skill path, harder to seed with scenario-consistent answers)
      (b) bypass the interview and `cp -R` the scaffold directly into work_dir
          (faster, deterministic, but skips the interview/self-test step the real install runs)

    Recommendation: (b) for scenario testing — the scenarios test the *post-init* brain behavior,
    not the init workflow. Init has its own tests (TBD: scenario 04-greenfield-init).
    """
    scaffold_src = SKILL_PATH / "scaffold"
    if not scaffold_src.exists():
        raise RuntimeError(f"Skill scaffold not found at {scaffold_src}")
    for item in scaffold_src.iterdir():
        dest = work_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)


# ============================================================
# Turn execution
# ============================================================

def run_turn(work_dir: Path, input_file: Path, turn_index: int) -> dict:
    """
    Run a single turn through `claude -p`.

    The prompt instructs the agent to ingest the input file using PM Brain's
    operating manual, which it reads from CLAUDE.md in work_dir.

    TODO: actual implementation. Sketch:
      cmd = [
          "claude", "-p",
          f"Ingest this artifact into the PM Brain in your current working directory. "
          f"Follow CLAUDE.md. Treat this as turn {turn_index} in the scenario.\\n\\n"
          f"Artifact: {input_file.read_text()}"
      ]
      result = subprocess.run(cmd, cwd=work_dir, capture_output=True, text=True, timeout=300)
      return {
          "turn": turn_index,
          "input": input_file.name,
          "stdout": result.stdout,
          "stderr": result.stderr,
          "returncode": result.returncode,
          "files_after": snapshot_files(work_dir),
      }

    Returning a stub for now so callers can wire up.
    """
    return {
        "turn": turn_index,
        "input": input_file.name,
        "status": "not_implemented",
    }


def snapshot_files(work_dir: Path) -> dict:
    """Return a dict of {relpath: mtime} for everything under work_dir, ignoring .git."""
    snap = {}
    for path in work_dir.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_file():
            rel = str(path.relative_to(work_dir))
            snap[rel] = path.stat().st_mtime
    return snap


# ============================================================
# Assertions
# ============================================================

def run_structural_assertions(work_dir: Path, assertions: list) -> list:
    """
    Run the deterministic assertions defined in expected.yaml.

    See tests/harness/checks/structural.py for the assertion implementations.
    Each assertion returns {"name": ..., "passed": bool, "detail": str}.

    TODO: dispatch table keyed on assertion type (file_exists, file_modified, etc.)
    """
    return [{"name": str(a), "passed": False, "detail": "not_implemented"} for a in (assertions or [])]


def run_content_assertions(work_dir: Path, assertions: list) -> list:
    """
    Run LLM-judge assertions. Each calls `claude -p` with the rubric file and the target.

    TODO: load rubric from judges/, format the judge prompt, call claude -p, parse the
    verdict (one of: PASS, FAIL, UNCERTAIN). UNCERTAIN counts as FAIL for this run;
    aggregate pass-rate across N runs handles the noise.
    """
    return [{"name": str(a), "passed": False, "detail": "not_implemented"} for a in (assertions or [])]


# ============================================================
# Main runner
# ============================================================

def run_once(scenario_dir: Path, run_index: int, max_cost: float | None) -> dict:
    scenario = load_scenario(scenario_dir)
    expected = scenario["expected"]
    inputs = scenario["inputs"]

    with tempfile.TemporaryDirectory(prefix="pm-brain-test-") as tmp:
        work_dir = Path(tmp)
        bootstrap_brain(work_dir)

        run_log = {
            "scenario": scenario_dir.name,
            "run": run_index,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "turns": [],
            "final_state": {},
        }

        # Map turn-NN.md -> turn config from expected.yaml.
        turn_configs = {t["input"]: t for t in expected.get("turns", [])}

        for i, input_file in enumerate(inputs, start=1):
            turn_result = run_turn(work_dir, input_file, i)
            tcfg = turn_configs.get(input_file.name, {})
            turn_result["structural"] = run_structural_assertions(
                work_dir, tcfg.get("structural", [])
            )
            turn_result["content"] = run_content_assertions(
                work_dir, tcfg.get("content", [])
            )
            run_log["turns"].append(turn_result)

        final_cfg = expected.get("final_state", {})
        run_log["final_state"] = {
            "structural": run_structural_assertions(work_dir, final_cfg.get("structural", [])),
            "content": run_content_assertions(work_dir, final_cfg.get("content", [])),
        }
        run_log["finished_at"] = datetime.now(timezone.utc).isoformat()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out = RESULTS_DIR / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{scenario_dir.name}-run{run_index}.json"
    out.write_text(json.dumps(run_log, indent=2))
    return run_log


def aggregate(run_logs: list, threshold: dict) -> dict:
    """
    Compute pass rates per assertion across runs.

    TODO: per-assertion rollup, compare to threshold, return summary.
    """
    return {
        "runs": len(run_logs),
        "threshold": threshold,
        "summary": "not_implemented",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenario", type=Path, help="Path to scenario dir, e.g. tests/scenarios/01-b2b-churn")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--max-cost", type=float, default=None, help="Abort if estimated cost exceeds this (USD)")
    args = ap.parse_args()

    scenario_dir = args.scenario.resolve()
    if not scenario_dir.is_dir():
        sys.exit(f"Scenario dir not found: {scenario_dir}")
    if not (scenario_dir / "expected.yaml").exists():
        sys.exit(f"expected.yaml not found in {scenario_dir}")

    expected = yaml.safe_load((scenario_dir / "expected.yaml").read_text())
    threshold = expected.get("pass_threshold", {"structural": 1.0, "content": 0.8})

    logs = []
    for i in range(1, args.runs + 1):
        print(f"--- run {i}/{args.runs} ---", file=sys.stderr)
        log = run_once(scenario_dir, i, args.max_cost)
        logs.append(log)

    summary = aggregate(logs, threshold)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
