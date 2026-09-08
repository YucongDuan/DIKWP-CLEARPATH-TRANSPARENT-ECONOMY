import pytest

from clearpath.demo import demo_person, demo_opportunities
from clearpath.models import DIKWP_TRANSITIONS, OpportunitySpec, PersonProfile


def test_person_has_25_transformations():
    value = PersonProfile.from_dict(demo_person())
    assert len(value.transformations) == 25
    assert set(value.transformations) == set(DIKWP_TRANSITIONS)


def test_invalid_stage_rejected():
    raw = demo_person()
    raw["transformations"]["D->I"]["stage"] = 99
    with pytest.raises(ValueError):
        PersonProfile.from_dict(raw)


def test_opportunity_requires_positive_lifetime():
    raw = demo_opportunities()[0]
    raw["remaining_lifetime_months"] = 0
    with pytest.raises(ValueError):
        OpportunitySpec.from_dict(raw)


def test_private_fields_can_be_removed():
    person = PersonProfile.from_dict(demo_person())
    assert "private_constraints" not in person.to_dict(include_private=False)
