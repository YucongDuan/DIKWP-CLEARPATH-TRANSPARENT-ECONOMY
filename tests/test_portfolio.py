from clearpath.demo import demo_opportunities, demo_person
from clearpath.models import OpportunitySpec, PersonProfile
from clearpath.portfolio import analyze_portfolio


def test_portfolio_finds_diversified_routes():
    person = PersonProfile.from_dict(demo_person())
    opportunities = [OpportunitySpec.from_dict(x) for x in demo_opportunities()]
    result = analyze_portfolio(person, opportunities)
    assert result["portfolio_status"] == "FUNDED_ROUTE_FOUND"
    assert result["safe_actionable_opportunity_count"] >= 2
    assert result["person_level_worth_score"] is None
    assert result["automatic_external_action_authority"] == 0


def test_portfolio_closed_set_does_not_score_person():
    person = PersonProfile.from_dict(demo_person())
    generic = OpportunitySpec.from_dict(demo_opportunities()[0])
    result = analyze_portfolio(person, [generic])
    assert result["portfolio_status"] == "NO_CURRENT_VIABLE_PATH_IN_TESTED_SET"
    assert result["decision_scope"].endswith("NOT_HUMAN_WORTH")
