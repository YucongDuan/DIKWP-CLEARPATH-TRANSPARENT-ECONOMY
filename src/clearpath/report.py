from __future__ import annotations

from typing import Any


def render_markdown(person: dict[str, Any], opportunity: dict[str, Any], analysis: dict[str, Any]) -> str:
    market = analysis["base_market"]
    lines = [
        "# DIKWP ClearPath Opportunity Truth Report",
        "",
        f"- Decision: **{analysis['decision_status']}**",
        f"- Scope: `{analysis['decision_scope']}`",
        f"- Opportunity: **{opportunity['title']}**",
        f"- Declared purpose: {person['purpose']}",
        f"- Base viability: {analysis['base_viability']:.3f}",
        f"- Robust world floor: {analysis['robust_floor']:.3f}",
        f"- Saturation ratio: {market['saturation_ratio']:.2f}",
        f"- Remaining paid-slot coverage: {market['remaining_slot_coverage']:.2%}",
        f"- First-mover capture index: {market['first_mover_capture_index']:.3f}",
        f"- Opportunity-laundering risk: {market['opportunity_laundering_risk']:.3f}",
        "",
        "## Closure reasons",
    ]
    reasons = analysis["hard_closure_reasons"] or ["No hard closure reason under current declarations."]
    lines.extend(f"- {item}" for item in reasons)
    lines.extend(["", "## Conditions that could reopen or improve the route"])
    lines.extend(f"- {item}" for item in analysis["conditions_to_reopen"])
    lines.extend(["", "## DIKWP bottlenecks"])
    for item in analysis["capability"]["bottlenecks"]:
        lines.append(f"- {item['transition']}: requirement {item['requirement']:.2f}, available {item['available']:.2f}, gap {item['gap']:.2f}")
    lines.extend(["", "## Multi-world results", "", "| World | Viability | Saturation | Paid-slot coverage |", "|---|---:|---:|---:|"])
    for item in analysis["world_results"]:
        lines.append(f"| {item['world_name']} | {item['viability']:.3f} | {item['market']['saturation_ratio']:.2f} | {item['market']['remaining_slot_coverage']:.2%} |")
    lines.extend(["", "## 72-hour actions"])
    lines.extend(f"- {item}" for item in analysis["actions"]["next_72_hours"])
    lines.extend([
        "",
        "## Boundary",
        "This report evaluates one economic route under declared constraints. It is not a score of intelligence, dignity, moral worth, or permanent employability. A `NO_CURRENT_VIABLE_PATH` result means: stop spending on this route until named evidence changes one or more closure conditions.",
        "",
    ])
    return "\n".join(lines)
