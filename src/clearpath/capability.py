from __future__ import annotations

from collections import defaultdict
from typing import Any

from .models import DIKWP_NODES, DIKWP_TRANSITIONS, PersonProfile, OpportunitySpec
from .util import clamp


def evidence_strength(score: float, stage: int, receipt_count: int = 0) -> float:
    score_factor = clamp(score / 5.0)
    stage_factor = clamp(stage / 7.0)
    receipt_factor = min(1.0, receipt_count / 3.0)
    return clamp(0.52 * score_factor + 0.36 * stage_factor + 0.12 * receipt_factor)


def capability_fit(person: PersonProfile, opportunity: OpportunitySpec) -> dict[str, Any]:
    numerator = 0.0
    denominator = 0.0
    details: list[dict[str, Any]] = []
    source_storage = defaultdict(float)
    destination_value = defaultdict(float)
    for name in DIKWP_TRANSITIONS:
        requirement = opportunity.required_transformations.get(name, 0.0)
        if requirement <= 0:
            continue
        evidence = person.transformations[name]
        strength = evidence_strength(evidence.score, evidence.stage, len(evidence.receipts))
        src, dst = name.split("->")
        storage_support = person.storage.get(src, 0.0)
        available = clamp(0.78 * strength + 0.22 * storage_support)
        match = min(available, requirement) / max(requirement, 1e-9)
        numerator += requirement * match
        denominator += requirement
        gap = max(0.0, requirement - available)
        source_storage[src] += requirement * storage_support
        destination_value[dst] += requirement * available
        details.append({
            "transition": name,
            "requirement": round(requirement, 6),
            "available": round(available, 6),
            "fit": round(clamp(match), 6),
            "gap": round(gap, 6),
            "evidence_stage": evidence.stage,
        })
    details.sort(key=lambda item: (-item["gap"], item["transition"]))
    fit = numerator / denominator if denominator else 0.0
    return {
        "fit": round(clamp(fit), 6),
        "bottlenecks": details[:5],
        "transition_details": details,
        "storage_by_source": {k: round(v, 6) for k, v in source_storage.items()},
        "value_by_destination": {k: round(v, 6) for k, v in destination_value.items()},
    }


def compact_dikwp_summary(person: PersonProfile) -> dict[str, float]:
    totals = {node: [] for node in DIKWP_NODES}
    for name, evidence in person.transformations.items():
        _, dst = name.split("->")
        totals[dst].append(evidence_strength(evidence.score, evidence.stage, len(evidence.receipts)))
    return {node: round(sum(values) / len(values), 6) if values else 0.0 for node, values in totals.items()}
