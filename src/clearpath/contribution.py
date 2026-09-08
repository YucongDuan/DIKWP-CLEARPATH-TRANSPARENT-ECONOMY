from __future__ import annotations

from typing import Any

from .util import ClearPathError, clamp


def allocate_contribution_budget(
    budget: float,
    contributions: list[dict[str, Any]],
    platform_rate: float = 0.08,
    commons_rate: float = 0.03,
    correction_reserve_rate: float = 0.03,
) -> dict[str, Any]:
    if budget <= 0:
        raise ClearPathError("budget must be positive")
    platform_rate = clamp(platform_rate, 0, 0.12)
    commons_rate = clamp(commons_rate, 0, 0.10)
    correction_reserve_rate = clamp(correction_reserve_rate, 0, 0.10)
    fixed = budget * (platform_rate + commons_rate + correction_reserve_rate)
    distributable = max(0.0, budget - fixed)
    scored = []
    for item in contributions:
        actor = str(item.get("actor_id", "unknown"))
        transition = str(item.get("transition", "D->I"))
        evidence = clamp(item.get("evidence_quality", 0.5))
        scarcity = clamp(item.get("scarcity", 0.5))
        responsibility = clamp(item.get("responsibility", 0.5))
        outcome = clamp(item.get("verified_outcome_share", 0.5))
        risk = clamp(item.get("risk_burden", 0.0))
        score = max(1e-9, 0.30 * outcome + 0.24 * evidence + 0.20 * responsibility + 0.16 * scarcity + 0.10 * risk)
        scored.append({"actor_id": actor, "transition": transition, "score": score})
    total = sum(item["score"] for item in scored) or 1.0
    allocations = [
        {
            "actor_id": item["actor_id"],
            "transition": item["transition"],
            "share": round(item["score"] / total, 6),
            "proposed_amount": round(distributable * item["score"] / total, 2),
        }
        for item in scored
    ]
    return {
        "budget": round(budget, 2),
        "participant_pool": round(distributable, 2),
        "platform_fee": round(budget * platform_rate, 2),
        "commons_return": round(budget * commons_rate, 2),
        "correction_reserve": round(budget * correction_reserve_rate, 2),
        "allocations": allocations,
        "settlement_status": "PROPOSAL_ONLY_NO_AUTOMATIC_PAYMENT",
        "automatic_payment_authority": 0,
    }
