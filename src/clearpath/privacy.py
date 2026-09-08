from __future__ import annotations

from typing import Any

from .capability import compact_dikwp_summary
from .models import PersonProfile


def public_capability_card(person: PersonProfile) -> dict[str, Any]:
    stages = [value.stage for value in person.transformations.values()]
    verified = sum(1 for value in person.transformations.values() if value.stage >= 6)
    return {
        "type": "ClearPathPublicCapabilityCard",
        "profile_id": person.profile_id,
        "purpose_category": "OWNER_DECLARED",
        "dikwp_destination_summary": compact_dikwp_summary(person),
        "verified_transition_count": verified,
        "median_evidence_stage": sorted(stages)[len(stages) // 2],
        "excluded_fields": [
            "private_constraints",
            "runway_months",
            "experiment_budget",
            "financial_state",
            "health_state",
            "family_state",
            "political_or_religious_views",
        ],
        "not_a_human_worth_score": True,
    }
