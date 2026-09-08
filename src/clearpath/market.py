from __future__ import annotations

import math
from typing import Any

from .models import OpportunitySpec, WorldSpec
from .util import clamp


def market_metrics(opportunity: OpportunitySpec, world: WorldSpec | None = None) -> dict[str, Any]:
    demand_multiplier = world.demand_multiplier if world else 1.0
    supply_multiplier = world.supply_multiplier if world else 1.0
    automation_multiplier = world.automation_multiplier if world else 1.0
    price_multiplier = world.price_multiplier if world else 1.0

    funded_slots = max(0.0, opportunity.funded_slots_12m * demand_multiplier)
    projected_supply = max(0.0, (opportunity.qualified_supply_now + opportunity.new_supply_12m) * supply_multiplier)
    saturation = projected_supply / max(funded_slots, 1.0)
    remaining_slot_coverage = min(1.0, funded_slots / max(projected_supply, 1.0))
    net_commoditization = max(
        0.0,
        opportunity.supply_growth_rate - opportunity.demand_growth_rate + 0.55 * opportunity.automation_rate * automation_multiplier,
    )
    half_life = math.inf if net_commoditization <= 1e-9 else math.log(2.0) / net_commoditization * 12.0
    adjusted_price = opportunity.price_per_outcome * price_multiplier
    margin = (adjusted_price - opportunity.variable_cost_per_outcome) / max(adjusted_price, 1.0)
    residual_need = clamp(
        (1.0 - clamp(opportunity.automation_rate * automation_multiplier))
        + 0.42 * opportunity.accountability_share
        + 0.32 * opportunity.physical_world_share
        + 0.26 * opportunity.local_context_share
    )
    first_mover_capture = clamp(
        0.35 * opportunity.top10_supplier_share
        + 0.30 * clamp((saturation - 0.6) / 2.4)
        + 0.20 * clamp(1.0 - opportunity.remaining_lifetime_months / 48.0)
        + 0.15 * opportunity.distribution_requirement
    )
    marketed = opportunity.training_seats_marketed
    opportunity_coverage = funded_slots / max(marketed, 1.0) if marketed > 0 else 1.0
    downstream_value = funded_slots * max(adjusted_price - opportunity.variable_cost_per_outcome, 0.0)
    training_revenue = marketed * opportunity.training_price
    laundering_risk = 0.0
    reasons: list[str] = []
    if marketed > 0:
        laundering_risk = clamp(
            0.46 * (1.0 - min(1.0, opportunity_coverage))
            + 0.34 * opportunity.marketing_certainty
            + 0.20 * min(1.0, training_revenue / max(downstream_value, 1.0))
        )
        if opportunity_coverage < 0.10:
            reasons.append("FEWER_THAN_ONE_REMAINING_PAID_SLOT_PER_TEN_MARKETED_SEATS")
        if training_revenue > downstream_value:
            reasons.append("TRAINING_REVENUE_EXCEEDS_DECLARED_DOWNSTREAM_OPPORTUNITY_VALUE")
        if opportunity.marketing_certainty > 0.75 and saturation > 1.5:
            reasons.append("HIGH_CERTAINTY_MARKETING_IN_A_SATURATED_PATH")
    return {
        "funded_slots_12m": round(funded_slots, 6),
        "projected_qualified_supply_12m": round(projected_supply, 6),
        "saturation_ratio": round(saturation, 6),
        "remaining_slot_coverage": round(remaining_slot_coverage, 6),
        "opportunity_half_life_months": None if math.isinf(half_life) else round(half_life, 3),
        "adjusted_price_per_outcome": round(adjusted_price, 6),
        "gross_margin_factor": round(clamp(margin), 6),
        "residual_noncommoditized_need": round(residual_need, 6),
        "first_mover_capture_index": round(first_mover_capture, 6),
        "training_paid_slot_coverage": round(opportunity_coverage, 6),
        "training_revenue": round(training_revenue, 6),
        "declared_downstream_opportunity_value": round(downstream_value, 6),
        "opportunity_laundering_risk": round(laundering_risk, 6),
        "training_integrity_reasons": reasons,
    }
