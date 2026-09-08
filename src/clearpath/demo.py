from __future__ import annotations

import shutil
from pathlib import Path

from .dashboard import generate_dashboard
from .ledger import append_event, verify_ledger
from .models import DIKWP_TRANSITIONS, OpportunitySpec, PersonProfile
from .portfolio import analyze_portfolio
from .report import render_markdown
from .util import write_json
from .viability import analyze_opportunity


def _transitions(default_score: float = 2.6, default_stage: int = 3, boosts: dict[str, tuple[float, int]] | None = None) -> dict:
    result = {name: {"score": default_score, "stage": default_stage, "receipts": []} for name in DIKWP_TRANSITIONS}
    for name, (score, stage) in (boosts or {}).items():
        result[name] = {"score": score, "stage": stage, "receipts": [f"synthetic-{name.lower().replace('->','-')}"] if stage >= 6 else []}
    return result


def demo_person() -> dict:
    return {
        "profile_id": "synthetic-person-001",
        "purpose": "Find a paid transition path without spending more on a saturated generic skill.",
        "weekly_hours": 12,
        "runway_months": 6,
        "experiment_budget": 2500,
        "risk_tolerance": 0.38,
        "customer_access": 0.42,
        "trust_access": 0.55,
        "distribution_access": 0.25,
        "local_execution": 0.70,
        "regulated_access": 0.20,
        "currency": "USD",
        "storage": {"D": 0.75, "I": 0.70, "K": 0.62, "W": 0.58, "P": 0.66},
        "transformations": _transitions(2.5, 3, {
            "D->I": (4.0, 6), "I->K": (3.8, 6), "K->W": (3.2, 5), "W->P": (3.5, 5), "P->P": (3.8, 6),
            "P->D": (3.4, 5), "I->P": (3.4, 5), "K->P": (3.2, 5),
        }),
        "private_constraints": {"family_obligations": "synthetic", "minimum_income_floor": 1800},
    }


def demo_opportunities() -> list[dict]:
    common_req = {name: 0.0 for name in DIKWP_TRANSITIONS}
    def req(**kwargs):
        value = dict(common_req)
        value.update({k.replace("_", "->"): v for k, v in kwargs.items()})
        return value
    return [
        {
            "opportunity_id": "generic-ai-microsaas",
            "title": "Generic AI micro-SaaS builder",
            "customer_segment": "global self-serve users",
            "funded_slots_12m": 180,
            "qualified_supply_now": 1500,
            "new_supply_12m": 5000,
            "demand_growth_rate": 0.12,
            "supply_growth_rate": 1.20,
            "automation_rate": 0.88,
            "price_per_outcome": 300,
            "variable_cost_per_outcome": 120,
            "entry_cost": 4000,
            "time_to_first_revenue_months": 7,
            "required_weekly_hours": 18,
            "remaining_lifetime_months": 12,
            "customer_access_requirement": 0.70,
            "trust_requirement": 0.35,
            "distribution_requirement": 0.85,
            "regulatory_requirement": 0.0,
            "local_execution_requirement": 0.0,
            "accountability_share": 0.10,
            "physical_world_share": 0.0,
            "local_context_share": 0.12,
            "top10_supplier_share": 0.78,
            "training_seats_marketed": 12000,
            "training_price": 800,
            "marketing_certainty": 0.88,
            "required_transformations": req(D_I=0.72, I_K=0.70, K_W=0.42, W_P=0.40, P_P=0.48),
            "evidence_notes": ["Synthetic opportunity used for mechanism testing."],
        },
        {
            "opportunity_id": "local-sme-workflow-builder",
            "title": "Local SME workflow and agent integration builder",
            "customer_segment": "owner-managed local businesses",
            "funded_slots_12m": 55,
            "qualified_supply_now": 32,
            "new_supply_12m": 40,
            "demand_growth_rate": 0.35,
            "supply_growth_rate": 0.28,
            "automation_rate": 0.58,
            "price_per_outcome": 8500,
            "variable_cost_per_outcome": 2500,
            "entry_cost": 1800,
            "time_to_first_revenue_months": 2,
            "required_weekly_hours": 10,
            "remaining_lifetime_months": 30,
            "customer_access_requirement": 0.45,
            "trust_requirement": 0.55,
            "distribution_requirement": 0.25,
            "regulatory_requirement": 0.10,
            "local_execution_requirement": 0.55,
            "accountability_share": 0.62,
            "physical_world_share": 0.18,
            "local_context_share": 0.72,
            "top10_supplier_share": 0.30,
            "training_seats_marketed": 70,
            "training_price": 600,
            "marketing_certainty": 0.45,
            "required_transformations": req(D_I=0.62, I_K=0.66, K_W=0.75, W_P=0.82, P_P=0.78, P_D=0.65),
            "evidence_notes": ["Synthetic opportunity used for mechanism testing."],
        },
        {
            "opportunity_id": "local-care-navigation",
            "title": "Local care and public-service navigation",
            "customer_segment": "families, community organizations, public programmes",
            "funded_slots_12m": 80,
            "qualified_supply_now": 50,
            "new_supply_12m": 25,
            "demand_growth_rate": 0.25,
            "supply_growth_rate": 0.10,
            "automation_rate": 0.32,
            "price_per_outcome": 2200,
            "variable_cost_per_outcome": 900,
            "entry_cost": 700,
            "time_to_first_revenue_months": 2,
            "required_weekly_hours": 12,
            "remaining_lifetime_months": 48,
            "customer_access_requirement": 0.35,
            "trust_requirement": 0.75,
            "distribution_requirement": 0.20,
            "regulatory_requirement": 0.35,
            "local_execution_requirement": 0.75,
            "accountability_share": 0.70,
            "physical_world_share": 0.55,
            "local_context_share": 0.85,
            "top10_supplier_share": 0.18,
            "training_seats_marketed": 90,
            "training_price": 350,
            "marketing_certainty": 0.30,
            "required_transformations": req(D_I=0.55, I_K=0.60, K_W=0.72, W_P=0.78, P_P=0.82, P_I=0.60),
            "evidence_notes": ["Synthetic opportunity used for mechanism testing."],
        },
    ]


def run_demo(workspace: Path, reset: bool = False) -> dict:
    if reset and workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    person_dict = demo_person()
    person = PersonProfile.from_dict(person_dict)
    results = []
    ledger = workspace / "responsibility-ledger.jsonl"
    opportunity_objects = [OpportunitySpec.from_dict(raw) for raw in demo_opportunities()]
    for opportunity in opportunity_objects:
        analysis = analyze_opportunity(person, opportunity)
        out = workspace / opportunity.opportunity_id
        out.mkdir(parents=True, exist_ok=True)
        write_json(out / "person-public.json", person.to_dict(include_private=False))
        write_json(out / "opportunity.json", opportunity.to_dict())
        write_json(out / "analysis.json", analysis)
        (out / "report.md").write_text(render_markdown(person.to_dict(), opportunity.to_dict(), analysis), encoding="utf-8")
        generate_dashboard(analysis, out / "dashboard.html")
        append_event(ledger, "OPPORTUNITY_ANALYSIS", {"opportunity_id": opportunity.opportunity_id, "decision_status": analysis["decision_status"], "analysis_digest": analysis["opportunity_digest"]})
        results.append({"opportunity_id": opportunity.opportunity_id, "decision_status": analysis["decision_status"], "base_viability": analysis["base_viability"], "robust_floor": analysis["robust_floor"]})
    portfolio = analyze_portfolio(person, opportunity_objects)
    write_json(workspace / "portfolio-analysis.json", portfolio)
    return {"workspace": str(workspace), "results": results, "portfolio": portfolio, "ledger": verify_ledger(ledger), "automatic_external_action_authority": 0}
