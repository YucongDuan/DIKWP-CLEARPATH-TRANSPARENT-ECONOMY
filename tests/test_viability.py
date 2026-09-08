from clearpath.demo import demo_opportunities, demo_person
from clearpath.models import OpportunitySpec, PersonProfile
from clearpath.viability import analyze_opportunity


def test_generic_route_is_not_go_now():
    result = analyze_opportunity(PersonProfile.from_dict(demo_person()), OpportunitySpec.from_dict(demo_opportunities()[0]))
    assert result["decision_status"] in {"PIVOT_TO_COMPLEMENT", "NO_CURRENT_VIABLE_PATH"}


def test_local_sme_route_has_higher_viability():
    person = PersonProfile.from_dict(demo_person())
    generic = analyze_opportunity(person, OpportunitySpec.from_dict(demo_opportunities()[0]))
    local = analyze_opportunity(person, OpportunitySpec.from_dict(demo_opportunities()[1]))
    assert local["weighted_mean"] > generic["weighted_mean"]


def test_no_funded_slots_closes_route():
    raw = demo_opportunities()[1]
    raw["funded_slots_12m"] = 0
    result = analyze_opportunity(PersonProfile.from_dict(demo_person()), OpportunitySpec.from_dict(raw))
    assert result["decision_status"] == "NO_CURRENT_VIABLE_PATH"
    assert "NO_DECLARED_FUNDED_OPPORTUNITY" in result["hard_closure_reasons"]


def test_result_has_no_human_worth_score():
    result = analyze_opportunity(PersonProfile.from_dict(demo_person()), OpportunitySpec.from_dict(demo_opportunities()[1]))
    assert result["person_level_worth_score"] is None
    assert "NOT_HUMAN_WORTH" in result["decision_scope"]


def test_plural_worlds_are_retained():
    result = analyze_opportunity(PersonProfile.from_dict(demo_person()), OpportunitySpec.from_dict(demo_opportunities()[1]))
    assert len(result["world_results"]) >= 4
    assert result["robust_floor"] == min(item["viability"] for item in result["world_results"])


def test_external_authority_is_zero():
    result = analyze_opportunity(PersonProfile.from_dict(demo_person()), OpportunitySpec.from_dict(demo_opportunities()[1]))
    assert result["automatic_external_action_authority"] == 0
    assert result["automatic_employment_decision_authority"] == 0
