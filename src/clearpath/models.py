from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .util import ClearPathError, clamp, nonnegative, positive, sha256_json

DIKWP_NODES = ("D", "I", "K", "W", "P")
DIKWP_TRANSITIONS = tuple(f"{a}->{b}" for a in DIKWP_NODES for b in DIKWP_NODES)
EVIDENCE_STAGES = (
    "EXPOSED",
    "RETRIEVED",
    "EXPLAINED",
    "DISCRIMINATED",
    "TRANSFERRED",
    "ACTED",
    "VERIFIED",
    "RETAINED",
)


@dataclass(frozen=True)
class CapabilityEvidence:
    score: float = 0.0
    stage: int = 0
    receipts: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "CapabilityEvidence":
        data = data or {}
        stage = int(data.get("stage", 0))
        if stage < 0 or stage >= len(EVIDENCE_STAGES):
            raise ClearPathError(f"stage must be 0..{len(EVIDENCE_STAGES)-1}")
        score = float(data.get("score", 0.0))
        if not 0 <= score <= 5:
            raise ClearPathError("capability score must be 0..5")
        return cls(score=score, stage=stage, receipts=tuple(str(x) for x in data.get("receipts", [])))

    def to_dict(self) -> dict[str, Any]:
        return {"score": self.score, "stage": self.stage, "stage_name": EVIDENCE_STAGES[self.stage], "receipts": list(self.receipts)}


@dataclass(frozen=True)
class PersonProfile:
    profile_id: str
    purpose: str
    weekly_hours: float
    runway_months: float
    experiment_budget: float
    risk_tolerance: float
    customer_access: float
    trust_access: float
    distribution_access: float
    local_execution: float
    regulated_access: float
    storage: dict[str, float]
    transformations: dict[str, CapabilityEvidence]
    private_constraints: dict[str, Any] = field(default_factory=dict)
    currency: str = "USD"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PersonProfile":
        missing = [k for k in ("profile_id", "purpose") if not data.get(k)]
        if missing:
            raise ClearPathError(f"Person profile missing: {', '.join(missing)}")
        storage_raw = dict(data.get("storage", {}))
        storage = {node: clamp(float(storage_raw.get(node, 0.5))) for node in DIKWP_NODES}
        trans_raw = dict(data.get("transformations", {}))
        transformations = {name: CapabilityEvidence.from_dict(trans_raw.get(name)) for name in DIKWP_TRANSITIONS}
        return cls(
            profile_id=str(data["profile_id"]),
            purpose=str(data["purpose"]),
            weekly_hours=nonnegative(data.get("weekly_hours", 5), "weekly_hours"),
            runway_months=nonnegative(data.get("runway_months", 3), "runway_months"),
            experiment_budget=nonnegative(data.get("experiment_budget", 0), "experiment_budget"),
            risk_tolerance=clamp(data.get("risk_tolerance", 0.4)),
            customer_access=clamp(data.get("customer_access", 0.2)),
            trust_access=clamp(data.get("trust_access", 0.2)),
            distribution_access=clamp(data.get("distribution_access", 0.2)),
            local_execution=clamp(data.get("local_execution", 0.4)),
            regulated_access=clamp(data.get("regulated_access", 0.1)),
            storage=storage,
            transformations=transformations,
            private_constraints=dict(data.get("private_constraints", {})),
            currency=str(data.get("currency", "USD")),
        )

    def to_dict(self, include_private: bool = True) -> dict[str, Any]:
        result = asdict(self)
        result["transformations"] = {k: v.to_dict() for k, v in self.transformations.items()}
        if not include_private:
            result.pop("private_constraints", None)
        return result

    @property
    def digest(self) -> str:
        return sha256_json(self.to_dict(include_private=True))


@dataclass(frozen=True)
class OpportunitySpec:
    opportunity_id: str
    title: str
    customer_segment: str
    funded_slots_12m: float
    qualified_supply_now: float
    new_supply_12m: float
    demand_growth_rate: float
    supply_growth_rate: float
    automation_rate: float
    price_per_outcome: float
    variable_cost_per_outcome: float
    entry_cost: float
    time_to_first_revenue_months: float
    required_weekly_hours: float
    remaining_lifetime_months: float
    customer_access_requirement: float
    trust_requirement: float
    distribution_requirement: float
    regulatory_requirement: float
    local_execution_requirement: float
    accountability_share: float
    physical_world_share: float
    local_context_share: float
    top10_supplier_share: float
    training_seats_marketed: float
    training_price: float
    marketing_certainty: float
    required_transformations: dict[str, float]
    evidence_notes: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OpportunitySpec":
        required = ["opportunity_id", "title", "customer_segment"]
        missing = [k for k in required if not data.get(k)]
        if missing:
            raise ClearPathError(f"Opportunity missing: {', '.join(missing)}")
        req_raw = dict(data.get("required_transformations", {}))
        required_transformations = {name: clamp(req_raw.get(name, 0.0)) for name in DIKWP_TRANSITIONS}
        if sum(required_transformations.values()) <= 0:
            for name in ("D->I", "I->K", "K->W", "W->P", "P->P"):
                required_transformations[name] = 0.6
        return cls(
            opportunity_id=str(data["opportunity_id"]),
            title=str(data["title"]),
            customer_segment=str(data["customer_segment"]),
            funded_slots_12m=nonnegative(data.get("funded_slots_12m", 0), "funded_slots_12m"),
            qualified_supply_now=nonnegative(data.get("qualified_supply_now", 0), "qualified_supply_now"),
            new_supply_12m=nonnegative(data.get("new_supply_12m", 0), "new_supply_12m"),
            demand_growth_rate=float(data.get("demand_growth_rate", 0.0)),
            supply_growth_rate=float(data.get("supply_growth_rate", 0.0)),
            automation_rate=clamp(data.get("automation_rate", 0.5)),
            price_per_outcome=nonnegative(data.get("price_per_outcome", 0), "price_per_outcome"),
            variable_cost_per_outcome=nonnegative(data.get("variable_cost_per_outcome", 0), "variable_cost_per_outcome"),
            entry_cost=nonnegative(data.get("entry_cost", 0), "entry_cost"),
            time_to_first_revenue_months=positive(data.get("time_to_first_revenue_months", 1), "time_to_first_revenue_months"),
            required_weekly_hours=nonnegative(data.get("required_weekly_hours", 5), "required_weekly_hours"),
            remaining_lifetime_months=positive(data.get("remaining_lifetime_months", 12), "remaining_lifetime_months"),
            customer_access_requirement=clamp(data.get("customer_access_requirement", 0.5)),
            trust_requirement=clamp(data.get("trust_requirement", 0.5)),
            distribution_requirement=clamp(data.get("distribution_requirement", 0.5)),
            regulatory_requirement=clamp(data.get("regulatory_requirement", 0.0)),
            local_execution_requirement=clamp(data.get("local_execution_requirement", 0.0)),
            accountability_share=clamp(data.get("accountability_share", 0.2)),
            physical_world_share=clamp(data.get("physical_world_share", 0.0)),
            local_context_share=clamp(data.get("local_context_share", 0.2)),
            top10_supplier_share=clamp(data.get("top10_supplier_share", 0.5)),
            training_seats_marketed=nonnegative(data.get("training_seats_marketed", 0), "training_seats_marketed"),
            training_price=nonnegative(data.get("training_price", 0), "training_price"),
            marketing_certainty=clamp(data.get("marketing_certainty", 0.5)),
            required_transformations=required_transformations,
            evidence_notes=tuple(str(x) for x in data.get("evidence_notes", [])),
        )

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["evidence_notes"] = list(self.evidence_notes)
        return result

    @property
    def digest(self) -> str:
        return sha256_json(self.to_dict())


@dataclass(frozen=True)
class WorldSpec:
    world_id: str
    name: str
    weight: float
    demand_multiplier: float
    supply_multiplier: float
    automation_multiplier: float
    price_multiplier: float
    access_multiplier: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WorldSpec":
        return cls(
            world_id=str(data["world_id"]),
            name=str(data["name"]),
            weight=nonnegative(data.get("weight", 1), "world.weight"),
            demand_multiplier=nonnegative(data.get("demand_multiplier", 1), "world.demand_multiplier"),
            supply_multiplier=nonnegative(data.get("supply_multiplier", 1), "world.supply_multiplier"),
            automation_multiplier=nonnegative(data.get("automation_multiplier", 1), "world.automation_multiplier"),
            price_multiplier=nonnegative(data.get("price_multiplier", 1), "world.price_multiplier"),
            access_multiplier=nonnegative(data.get("access_multiplier", 1), "world.access_multiplier"),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
