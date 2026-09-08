from clearpath.contribution import allocate_contribution_budget
from clearpath.demo import demo_person
from clearpath.models import PersonProfile
from clearpath.privacy import public_capability_card


def test_allocation_sums_to_budget():
    result = allocate_contribution_budget(10000, [
        {"actor_id":"a","transition":"D->I","verified_outcome_share":0.5},
        {"actor_id":"b","transition":"W->P","verified_outcome_share":0.8},
    ])
    total = result["participant_pool"] + result["platform_fee"] + result["commons_return"] + result["correction_reserve"]
    assert round(total, 2) == 10000


def test_platform_fee_is_capped():
    result = allocate_contribution_budget(10000, [{"actor_id":"a"}], platform_rate=0.8)
    assert result["platform_fee"] == 1200


def test_payment_is_proposal_only():
    result = allocate_contribution_budget(10000, [{"actor_id":"a"}])
    assert result["automatic_payment_authority"] == 0


def test_public_card_excludes_financial_constraints():
    card = public_capability_card(PersonProfile.from_dict(demo_person()))
    text = str(card)
    assert "runway_months" in card["excluded_fields"]
    assert "minimum_income_floor" not in text
    assert card["not_a_human_worth_score"] is True
