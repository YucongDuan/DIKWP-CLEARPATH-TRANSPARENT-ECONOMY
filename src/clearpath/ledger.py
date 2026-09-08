from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .util import sha256_json, utc_now


def append_event(path: Path, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    previous = "0" * 64
    if path.exists():
        lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if lines:
            previous = json.loads(lines[-1])["event_digest"]
    record = {
        "timestamp": utc_now(),
        "event_type": event_type,
        "previous_digest": previous,
        "payload": payload,
    }
    record["event_digest"] = sha256_json(record)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return record


def verify_ledger(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"valid": False, "events": 0, "reason": "LEDGER_NOT_FOUND"}
    previous = "0" * 64
    count = 0
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        record = json.loads(raw)
        digest = record.get("event_digest")
        check = dict(record)
        check.pop("event_digest", None)
        if record.get("previous_digest") != previous:
            return {"valid": False, "events": count, "reason": "BROKEN_PREVIOUS_DIGEST"}
        if sha256_json(check) != digest:
            return {"valid": False, "events": count, "reason": "EVENT_DIGEST_MISMATCH"}
        previous = digest
        count += 1
    return {"valid": True, "events": count, "head": previous}
