from clearpath.demo import demo_opportunities, demo_person
from clearpath.models import OpportunitySpec, PersonProfile


def person():
    return PersonProfile.from_dict(demo_person())


def opportunities():
    return [OpportunitySpec.from_dict(item) for item in demo_opportunities()]
