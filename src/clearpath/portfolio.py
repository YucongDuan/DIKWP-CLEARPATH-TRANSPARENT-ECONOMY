from __future__ import annotations

from collections import Counter
from typing import Any, Iterable

from .models import OpportunitySpec, PersonProfile, WorldSpec
from .viability import analyze_opportunity


_ACTIONABLE = {"GO_NOW", "TEST_CHEAPLY"}


def _diversification_signature(opportunity: OpportunitySpec) -> tuple[int, int, int, int]:
    """Return a coarse, non-identifying route signature used only for portfolio diversity."""
    return (
        int(opportunity.local_context_share >= 0.50),
        int(opportunity.physical_world_share >= 0.35),
        int(opportunity.accountability_share >= 0.50),
        int(opportunity.regulatory_requirement >= 0.35),
    )


def analyze_portfolio(
    person: PersonProfile,
    opportunities: Iterable[OpportunitySpec],
    worlds: list[WorldSpec] | None = None,
) -> dict[str, Any]:
    opportunities = list(opportunities)
    if not opportunities:
        raise ValueError("At least one opportunity is required")

    analyses = [analyze_opportunity(person, opportunity, worlds) for opportunity in opportunities]
    paired = list(zip(opportunities, analyses))
    ranked = sorted(
        paired,
        key=lambda pair: (
            pair[1]["decision_status"] == "GO_NOW",
            pair[1]["decision_status"] == "TEST_CHEAPLY",
            pair[1]["weighted_mean"],
            pair[1]["robust_floor"],
        ),
        reverse=True,
    )

    go_now = [pair for pair in ranked if pair[1]["decision_status"] == "GO_NOW"]
    testable = [pair for pair in ranked if pair[1]["decision_status"] == "TEST_CHEAPLY"]
    pivots = [pair for pair in ranked if pair[1]["decision_status"] == "PIVOT_TO_COMPLEMENT"]
    closed = [pair for pair in ranked if pair[1]["decision_status"] == "NO_CURRENT_VIABLE_PATH"]

    if go_now:
        portfolio_status = "FUNDED_ROUTE_FOUND"
    elif testable:
        portfolio_status = "LOW_COST_TEST_ROUTE_FOUND"
    elif pivots:
        portfolio_status = "ONLY_COMPLEMENTARY_PIVOTS_FOUND"
    else:
        portfolio_status = "NO_CURRENT_VIABLE_PATH_IN_TESTED_SET"

    selected: list[dict[str, Any]] = []
    signatures: set[tuple[int, int, int, int]] = set()
    for opportunity, analysis in ranked:
        if analysis["decision_status"] not in _ACTIONABLE:
            continue
        signature = _diversification_signature(opportunity)
        if not selected or signature not in signatures:
            selected.append({
                "opportunity_id": opportunity.opportunity_id,
                "title": opportunity.title,
                "decision_status": analysis["decision_status"],
                "weighted_mean": analysis["weighted_mean"],
                "robust_floor": analysis["robust_floor"],
                "saturation_ratio": analysis["base_market"]["saturation_ratio"],
                "signature": list(signature),
            })
            signatures.add(signature)
        if len(selected) >= 3:
            break

    first_mover_only = bool(paired) and all(
        analysis["base_market"]["first_mover_capture_index"] >= 0.72
        and analysis["base_market"]["remaining_slot_coverage"] <= 0.10
        for _, analysis in paired
    )
    status_counts = Counter(analysis["decision_status"] for _, analysis in paired)
    opportunity_floor = len(go_now) + len(testable)

    return {
        "system": "DIKWP_CLEARPATH_TRANSPARENT_ECONOMY_OS",
        "version": "1.0.0",
        "portfolio_status": portfolio_status,
        "decision_scope": "TESTED_OPPORTUNITY_SET_UNDER_DECLARED_CONSTRAINTS_NOT_HUMAN_WORTH",
        "tested_opportunity_count": len(opportunities),
        "safe_actionable_opportunity_count": opportunity_floor,
        "first_mover_only_pattern": first_mover_only,
        "status_counts": dict(sorted(status_counts.items())),
        "selected_diversified_routes": selected,
        "ranked_routes": [
            {
                "opportunity_id": opportunity.opportunity_id,
                "title": opportunity.title,
                "decision_status": analysis["decision_status"],
                "weighted_mean": analysis["weighted_mean"],
                "robust_floor": analysis["robust_floor"],
                "saturation_ratio": analysis["base_market"]["saturation_ratio"],
                "remaining_paid_slot_coverage": analysis["base_market"]["remaining_slot_coverage"],
                "opportunity_laundering_risk": analysis["base_market"]["opportunity_laundering_risk"],
                "hard_closure_reasons": analysis["hard_closure_reasons"],
                "conditions_to_reopen": analysis["conditions_to_reopen"],
            }
            for opportunity, analysis in ranked
        ],
        "next_decision": (
            "RUN_SMALLEST_PAID_TEST_ON_TOP_DIVERSIFIED_ROUTE"
            if portfolio_status in {"FUNDED_ROUTE_FOUND", "LOW_COST_TEST_ROUTE_FOUND"}
            else "STOP_GENERIC_TRAINING_SPEND_AND_ADD_NEW_FUNDED_OPPORTUNITY_CANDIDATES"
        ),
        "person_level_worth_score": None,
        "automatic_employment_decision_authority": 0,
        "automatic_external_action_authority": 0,
    }
