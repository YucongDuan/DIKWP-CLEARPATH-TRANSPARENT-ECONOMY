#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import deque
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass(frozen=True)
class State:
    phase: str
    reasons: int
    appeal_open: bool
    corrected: bool
    external_authority: int
    worth_score: bool


def successors(s: State):
    if s.phase == "DRAFT":
        yield State("EVIDENCED", s.reasons, s.appeal_open, s.corrected, 0, False)
    if s.phase == "EVIDENCED":
        yield State("ANALYZED", s.reasons, s.appeal_open, s.corrected, 0, False)
    if s.phase == "ANALYZED":
        for phase in ("GO", "TEST", "PIVOT", "CLOSED"):
            yield State(phase, 1 if phase == "CLOSED" else s.reasons, False, False, 0, False)
    if s.phase in {"GO", "TEST", "PIVOT", "CLOSED"} and not s.appeal_open:
        yield State(s.phase, s.reasons, True, s.corrected, 0, False)
    if s.appeal_open:
        yield State("CORRECTED", s.reasons, False, True, 0, False)


def invariants(s: State):
    return {
        "no_external_authority": s.external_authority == 0,
        "no_person_worth_score": not s.worth_score,
        "closed_has_reason": s.phase != "CLOSED" or s.reasons > 0,
        "corrected_is_marked": s.phase != "CORRECTED" or s.corrected,
        "appeal_not_open_after_correction": s.phase != "CORRECTED" or not s.appeal_open,
    }


def run(output: Path):
    initial = State("DRAFT", 0, False, False, 0, False)
    queue = deque([(initial, 0)])
    seen = {initial}
    transitions = 0
    violations = []
    max_depth = 0
    phases = set()
    while queue:
        state, depth = queue.popleft()
        max_depth = max(max_depth, depth)
        phases.add(state.phase)
        for name, ok in invariants(state).items():
            if not ok:
                violations.append({"invariant": name, "state": asdict(state)})
        for nxt in successors(state):
            transitions += 1
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, depth + 1))
    receipt = {
        "model": "TOEP-1000 bounded reference workflow",
        "reachable_states": len(seen),
        "checked_transitions": transitions,
        "max_shortest_path_depth": max_depth,
        "reachable_phases": sorted(phases),
        "invariant_violations": violations,
        "passed": not violations,
        "scope": "FINITE_REFERENCE_ABSTRACTION_NOT_UNIVERSAL_PROOF"
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="validation/TOEP_1000_BOUNDED_MODEL_CHECK_RECEIPT.json")
    args = parser.parse_args()
    print(json.dumps(run(Path(args.output)), indent=2, sort_keys=True))
