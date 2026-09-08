"""DIKWP ClearPath Transparent Economy OS."""

__version__ = "1.0.0"

from .contribution import allocate_contribution_budget
from .market import market_metrics
from .portfolio import analyze_portfolio
from .models import OpportunitySpec, PersonProfile
from .viability import analyze_opportunity

__all__ = ["OpportunitySpec", "PersonProfile", "analyze_opportunity", "analyze_portfolio", "market_metrics", "allocate_contribution_budget"]
