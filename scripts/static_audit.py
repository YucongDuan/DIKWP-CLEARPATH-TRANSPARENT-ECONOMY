#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

BANNED_CALLS = {
    ("os", "system"), ("subprocess", "run"), ("subprocess", "Popen"),
    ("subprocess", "call"), ("socket", "socket"), ("urllib.request", "urlopen"),
    ("requests", "get"), ("requests", "post"), ("builtins", "eval"), ("builtins", "exec"),
}


def dotted_name(node):
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))


def audit(root: Path):
    findings = []
    files = sorted(root.rglob("*.py"))
    for path in files:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = dotted_name(node.func)
                normalized = tuple(name.rsplit(".", 1)) if "." in name else ("builtins", name)
                if normalized in BANNED_CALLS:
                    findings.append({"file": str(path), "line": node.lineno, "call": name})
    return {
        "audited_python_files": len(files),
        "findings": findings,
        "passed": not findings,
        "note": "Static pattern audit is not a security certification."
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="src/clearpath")
    parser.add_argument("--output", default="validation/STATIC_AUDIT_RECEIPT.json")
    args = parser.parse_args()
    result = audit(Path(args.root))
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
