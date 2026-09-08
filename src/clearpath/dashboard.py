from __future__ import annotations

if __package__:
    from ._ui_presentation import localize_html as _ui_localize_html
else:
    from _ui_presentation import localize_html as _ui_localize_html


import html
import json
from pathlib import Path
from typing import Any


def generate_dashboard(analysis: dict[str, Any], output: Path) -> str:
    rows = "".join(
        f"<tr><td>{html.escape(item['world_name'])}</td><td>{item['viability']:.3f}</td><td>{item['market']['saturation_ratio']:.2f}</td><td>{item['market']['remaining_slot_coverage']:.1%}</td></tr>"
        for item in analysis["world_results"]
    )
    reasons = "".join(f"<li>{html.escape(x)}</li>" for x in (analysis["hard_closure_reasons"] or ["No hard closure reason."]))
    conditions = "".join(f"<li>{html.escape(x)}</li>" for x in analysis["conditions_to_reopen"])
    data = json.dumps(analysis, ensure_ascii=False).replace("</", "<\\/")
    document = f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>ClearPath Report</title><style>
    body{{font-family:system-ui,sans-serif;background:#f5f7fb;color:#172033;margin:0}}main{{max-width:1100px;margin:auto;padding:28px}}.hero{{background:#17324d;color:white;padding:24px;border-radius:18px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:18px 0}}.card{{background:white;border:1px solid #dbe3ec;border-radius:14px;padding:16px}}table{{width:100%;border-collapse:collapse;background:white}}th,td{{padding:10px;border-bottom:1px solid #e5eaf0;text-align:left}}code{{background:#eef2f6;padding:2px 5px;border-radius:5px}}</style></head><body><main><section class='hero'><h1>DIKWP ClearPath Opportunity Truth Report</h1><p>{html.escape(analysis['decision_status'])}</p><p>This is a route decision, not a human-worth judgment.</p></section><section class='grid'><div class='card'><b>Base viability</b><div>{analysis['base_viability']:.3f}</div></div><div class='card'><b>Robust floor</b><div>{analysis['robust_floor']:.3f}</div></div><div class='card'><b>Saturation</b><div>{analysis['base_market']['saturation_ratio']:.2f}</div></div><div class='card'><b>Paid-slot coverage</b><div>{analysis['base_market']['remaining_slot_coverage']:.1%}</div></div></section><div class='card'><h2>Closure reasons</h2><ul>{reasons}</ul><h2>Conditions to reopen</h2><ul>{conditions}</ul></div><h2>Plural worlds</h2><table><thead><tr><th>World</th><th>Viability</th><th>Saturation</th><th>Slot coverage</th></tr></thead><tbody>{rows}</tbody></table><script type='application/json' id='analysis-data'>{data}</script></main></body></html>"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(_ui_localize_html(document), encoding="utf-8")
    return _ui_localize_html(str(output))
