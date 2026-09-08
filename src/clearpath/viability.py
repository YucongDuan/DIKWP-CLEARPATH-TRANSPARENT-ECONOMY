from __future__ import annotations

from typing import Any

from .capability import capability_fit, compact_dikwp_summary
from .market import market_metrics
from .models import OpportunitySpec, PersonProfile, WorldSpec
from .util import clamp, geometric_mean
from .worlds import default_worlds


def _ratio(current: float, requirement: float) -> float:
    if requirement <= 1e-9:
        return 1.0
    return clamp(current / requirement)


def _access_factor(person: PersonProfile, opportunity: OpportunitySpec, multiplier: float) -> tuple[float, list[dict[str, float]]]:
    factors = [
        ("customer_access", _ratio(clamp(person.customer_access * multiplier), opportunity.customer_access_requirement)),
        ("trust_access", _ratio(clamp(person.trust_access * multiplier), opportunity.trust_requirement)),
        ("distribution_access", _ratio(clamp(person.distribution_access * multiplier), opportunity.distribution_requirement)),
        ("regulated_access", _ratio(clamp(person.regulated_access * multiplier), opportunity.regulatory_requirement)),
        ("local_execution", _ratio(clamp(person.local_execution * multiplier), opportunity.local_execution_requirement)),
    ]
    return geometric_mean([value for _, value in factors]), [{"name": name, "factor": round(value, 6)} for name, value in factors]


def evaluate_world(person: PersonProfile, opportunity: OpportunitySpec, world: WorldSpec) -> dict[str, Any]:
    cap = capability_fit(person, opportunity)
    market = market_metrics(opportunity, world)
    access, access_details = _access_factor(person, opportunity, world.access_multiplier)
    budget = 1.0 if opportunity.entry_cost <= 0 else clamp(person.experiment_budget / opportunity.entry_cost)
    runway = clamp(person.runway_months / opportunity.time_to_first_revenue_months)
    time = 1.0 if opportunity.required_weekly_hours <= 0 else clamp(person.weekly_hours / opportunity.required_weekly_hours)
    slot = market["remaining_slot_coverage"]
    residual = market["residual_noncommoditized_need"]
    margin = market["gross_margin_factor"]
    concentration_penalty = clamp(1.0 - 0.55 * market["first_mover_capture_index"])
    risk_fit = clamp(1.0 - max(0.0, market["first_mover_capture_index"] - person.risk_tolerance) * 0.65)
    factors = {
        "capability_fit": cap["fit"],
        "access_fit": access,
        "budget_fit": budget,
        "runway_fit": runway,
        "time_fit": time,
        "remaining_slot_factor": slot,
        "residual_need": residual,
        "margin_factor": margin,
        "concentration_factor": concentration_penalty,
        "risk_fit": risk_fit,
    }
    viability = geometric_mean(list(factors.values()))
    return {
        "world_id": world.world_id,
        "world_name": world.name,
        "weight": world.weight,
        "viability": round(viability, 6),
        "factors": {k: round(v, 6) for k, v in factors.items()},
        "access_details": access_details,
        "market": market,
    }


def _conditions_to_reopen(person: PersonProfile, opportunity: OpportunitySpec, base: dict[str, Any]) -> list[str]:
    conditions: list[str] = []
    f = base["factors"]
    m = base["market"]
    if f["capability_fit"] < 0.60:
        conditions.append("BUILD_TASK_SPECIFIC_DIKWP_EVIDENCE")
    if f["access_fit"] < 0.60:
        conditions.append("OBTAIN_A_NAMED_CUSTOMER_TRUST_OR_DISTRIBUTION_BRIDGE")
    if f["budget_fit"] < 0.75:
        conditions.append("REDUCE_ENTRY_COST_OR_SECURE_NON_DEBT_EXPERIMENT_SUPPORT")
    if f["runway_fit"] < 0.75:
        conditions.append("SHORTEN_TIME_TO_FIRST_PAID_RECEIPT_OR_EXTEND_RUNWAY")
    if f["time_fit"] < 0.75:
        conditions.append("REDESIGN_THE_ROUTE_TO_FIT_AVAILABLE_WEEKLY_TIME")
    if m["saturation_ratio"] > 1.5:
        conditions.append("MOVE_FROM_GENERIC_SUPPLY_TO_A_LOCAL_DOMAIN_OR_RESPONSIBILITY_BEARING_NICHE")
    if m["residual_noncommoditized_need"] < 0.35:
        conditions.append("SHIFT_FROM_EXECUTION_TO_PURPOSE_CONTEXT_VALIDATION_OR_ACCOUNTABILITY")
    if m["funded_slots_12m"] <= 0:
        conditions.append("REQUIRE_EVIDENCE_OF_REAL_FUNDED_DEMAND_BEFORE_MORE_TRAINING")
    if not conditions:
        conditions.append("RUN_A_SMALL_PAID_REALITY_TEST_AND_RECALIBRATE")
    return conditions


def _actions(status: str, conditions: list[str], opportunity: OpportunitySpec) -> dict[str, list[str]]:
    if status == "GO_NOW":
        return {
            "next_72_hours": [
                "IDENTIFY_THREE_NAMED_BUYERS_WITH_THE_DECLARED_PROBLEM",
                "OFFER_ONE_NARROW_PAID_OUTCOME_NOT_A_GENERIC_SOFTWARE_PRODUCT",
                "DEFINE_A_RECEIPT_THAT_PROVES_THE_RESULT_AND_THE_DIKWP_TRANSFORMATION",
            ],
            "next_30_days": ["DELIVER_ONE_PAID_PILOT", "MEASURE_REWORK_AND_BUYER_VALUE", "PUBLISH_ONLY_CONSENTED_EVIDENCE"],
            "next_90_days": ["REPEAT_WITH_THREE_BUYERS", "DISTILL_THE_VERIFIED_WORKFLOW", "RECHECK_SATURATION_AND_MARGIN"],
        }
    if status == "TEST_CHEAPLY":
        return {
            "next_72_hours": ["DO_NOT_BUILD_A_FULL_PRODUCT", "ASK_FIVE_BUYERS_FOR_A_PAID_OR_SIGNED_TEST", "SET_A_LOSS_CAP"],
            "next_30_days": ["RUN_ONE_SMALL_REVERSIBLE_TEST", "STOP_IF_NO_BUYER_COMMITS_VALUE", "RECORD_WHICH_CONDITION_FAILED"],
            "next_90_days": ["SCALE_ONLY_AFTER_REPEATABLE_PAYMENT", "COMPARE_A_LOCAL_NICHE_WITH_THE_GENERIC_ROUTE"],
        }
    if status == "PIVOT_TO_COMPLEMENT":
        return {
            "next_72_hours": ["STOP_GENERIC_SKILL_ACCUMULATION", "SELECT_ONE_UNMET_DOMAIN_PROBLEM", "MAP_THE_MISSING_W_OR_P_RESPONSIBILITY"],
            "next_30_days": ["PARTNER_WITH_A_CUSTOMER_OR_DOMAIN_HOLDER", "BUILD_A_RESULT_RECEIPT_INSTEAD_OF_A_DEMO", "TEST_A_PHYSICAL_LOCAL_OR_REGULATED_COMPLEMENT"],
            "next_90_days": ["REASSESS_TWO_ALTERNATIVE_PATHS", "ABANDON_THE_ORIGINAL_ROUTE_IF_PAID_DEMAND_REMAINS_UNPROVEN"],
        }
    return {
        "next_72_hours": ["STOP_SPENDING_ON_THIS_ROUTE", "PRESERVE_CASH_AND_TIME", "DOCUMENT_THE_EXACT_CLOSURE_REASONS"],
        "next_30_days": ["TEST_ONLY_CONDITIONS_THAT_COULD_REOPEN_THE_ROUTE", "SEARCH_FOR_ADJACENT_FUNDED_PROBLEMS_NOT_MORE_GENERIC_TRAINING"],
        "next_90_days": ["KEEP_THE_ROUTE_CLOSED_UNLESS_A_NAMED_BUYER_OR_NEW_EVIDENCE_CHANGES_THE_MODEL", "BUILD_A_DIFFERENT_OPPORTUNITY_PORTFOLIO"],
    }


def analyze_opportunity(
    person: PersonProfile,
    opportunity: OpportunitySpec,
    worlds: list[WorldSpec] | None = None,
) -> dict[str, Any]:
    worlds = worlds or default_worlds()
    if len(worlds) < 2:
        raise ValueError("At least two non-identical worlds are required")
    world_results = [evaluate_world(person, opportunity, world) for world in worlds]
    weight_sum = sum(item["weight"] for item in world_results) or 1.0
    weighted_mean = sum(item["viability"] * item["weight"] for item in world_results) / weight_sum
    robust_floor = min(item["viability"] for item in world_results)
    base_world = WorldSpec("declared_base", "Declared base", 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    base = evaluate_world(person, opportunity, base_world)
    hard_reasons: list[str] = []
    if base["market"]["funded_slots_12m"] <= 0:
        hard_reasons.append("NO_DECLARED_FUNDED_OPPORTUNITY")
    if opportunity.price_per_outcome <= opportunity.variable_cost_per_outcome:
        hard_reasons.append("NONPOSITIVE_DECLARED_UNIT_MARGIN")
    if opportunity.entry_cost > person.experiment_budget and person.runway_months < opportunity.time_to_first_revenue_months:
        hard_reasons.append("ENTRY_COST_AND_RUNWAY_BOTH_FAIL")
    if base["market"]["saturation_ratio"] >= 5 and base["factors"]["capability_fit"] < 0.80:
        hard_reasons.append("EXTREME_SATURATION_WITHOUT_DIFFERENTIATION")

    if hard_reasons or weighted_mean < 0.27:
        status = "NO_CURRENT_VIABLE_PATH"
    elif weighted_mean >= 0.60 and robust_floor >= 0.38 and base["market"]["saturation_ratio"] < 1.6:
        status = "GO_NOW"
    elif weighted_mean >= 0.44 and base["market"]["funded_slots_12m"] > 0:
        status = "TEST_CHEAPLY"
    else:
        status = "PIVOT_TO_COMPLEMENT"

    conditions = _conditions_to_reopen(person, opportunity, base)
    result = {
        "system": "DIKWP_CLEARPATH_TRANSPARENT_ECONOMY_OS",
        "version": "1.0.0",
        "decision_status": status,
        "decision_scope": "THIS_OPPORTUNITY_UNDER_DECLARED_CONSTRAINTS_NOT_HUMAN_WORTH",
        "base_viability": base["viability"],
        "robust_floor": round(robust_floor, 6),
        "weighted_mean": round(weighted_mean, 6),
        "hard_closure_reasons": hard_reasons,
        "conditions_to_reopen": conditions,
        "actions": _actions(status, conditions, opportunity),
        "person_digest": person.digest,
        "opportunity_digest": opportunity.digest,
        "capability": capability_fit(person, opportunity),
        "dikwp_summary": compact_dikwp_summary(person),
        "base_market": base["market"],
        "base_factors": base["factors"],
        "world_results": world_results,
        "automatic_external_action_authority": 0,
        "automatic_employment_decision_authority": 0,
        "person_level_worth_score": None,
    }
    return result
