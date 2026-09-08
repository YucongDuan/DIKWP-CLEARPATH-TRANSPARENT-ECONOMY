#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
required = [
    "README.md", "README_CN.md", "LICENSE", "SECURITY.md", "GOVERNANCE.md",
    "DIKWP_CLEARPATH_TRANSPARENT_ECONOMY_OS_v1.0.0.html",
    "spec/TOEP_1000_CORE_SPEC_DRAFT_CN_EN.md",
    "schemas/person.schema.json", "schemas/opportunity.schema.json",
]
missing = [p for p in required if not (ROOT / p).exists()]
text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in (ROOT / "src/clearpath").glob("*.py"))
forbidden = {
    "automatic external authority > 0": "automatic_external_action_authority\": 1",
    "automatic employment authority > 0": "automatic_employment_decision_authority\": 1",
}
findings = [name for name, token in forbidden.items() if token in text]
result = {"missing_required_files": missing, "forbidden_findings": findings, "passed": not missing and not findings}
(ROOT / "validation/RELEASE_AUDIT_RECEIPT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["passed"] else 1)
