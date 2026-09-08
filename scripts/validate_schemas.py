#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CASES = [
    ("schemas/person.schema.json", "examples/person-profile.json"),
    ("schemas/opportunity.schema.json", "examples/generic-ai-microsaas.json"),
    ("schemas/opportunity.schema.json", "examples/local-sme-workflow-builder.json"),
    ("schemas/opportunity.schema.json", "examples/local-care-navigation.json"),
]

results = []
for schema_path, instance_path in CASES:
    schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
    instance = json.loads((ROOT / instance_path).read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e: list(e.path))
    results.append({"schema": schema_path, "instance": instance_path, "valid": not errors, "errors": [e.message for e in errors]})

receipt = {"checks": results, "passed": all(item["valid"] for item in results)}
output = ROOT / "validation/SCHEMA_VALIDATION_RECEIPT.json"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=2, sort_keys=True))
raise SystemExit(0 if receipt["passed"] else 1)
