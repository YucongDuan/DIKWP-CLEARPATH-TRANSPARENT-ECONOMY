from clearpath.capability import capability_fit, evidence_strength
from clearpath.demo import demo_opportunities, demo_person
from clearpath.models import OpportunitySpec, PersonProfile


def test_higher_stage_increases_strength():
    assert evidence_strength(3, 6) > evidence_strength(3, 2)


def test_receipts_increase_strength():
    assert evidence_strength(3, 5, 3) > evidence_strength(3, 5, 0)


def test_fit_is_bounded():
    result = capability_fit(PersonProfile.from_dict(demo_person()), OpportunitySpec.from_dict(demo_opportunities()[1]))
    assert 0 <= result["fit"] <= 1
    assert result["bottlenecks"]
