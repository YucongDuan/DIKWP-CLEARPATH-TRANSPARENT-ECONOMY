from clearpath.demo import demo_opportunities
from clearpath.market import market_metrics
from clearpath.models import OpportunitySpec


def test_generic_market_is_saturated():
    result = market_metrics(OpportunitySpec.from_dict(demo_opportunities()[0]))
    assert result["saturation_ratio"] > 10
    assert result["opportunity_laundering_risk"] > 0.7


def test_local_market_has_more_slot_coverage():
    generic = market_metrics(OpportunitySpec.from_dict(demo_opportunities()[0]))
    local = market_metrics(OpportunitySpec.from_dict(demo_opportunities()[1]))
    assert local["remaining_slot_coverage"] > generic["remaining_slot_coverage"]


def test_no_training_seats_no_laundering_flag():
    raw = demo_opportunities()[1]
    raw["training_seats_marketed"] = 0
    result = market_metrics(OpportunitySpec.from_dict(raw))
    assert result["opportunity_laundering_risk"] == 0
