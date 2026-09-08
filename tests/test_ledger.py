import json

from clearpath.ledger import append_event, verify_ledger


def test_ledger_roundtrip(tmp_path):
    path = tmp_path / "ledger.jsonl"
    append_event(path, "A", {"x":1})
    append_event(path, "B", {"x":2})
    assert verify_ledger(path)["valid"] is True


def test_ledger_tamper_detected(tmp_path):
    path = tmp_path / "ledger.jsonl"
    append_event(path, "A", {"x":1})
    row = json.loads(path.read_text())
    row["payload"]["x"] = 9
    path.write_text(json.dumps(row)+"\n")
    assert verify_ledger(path)["valid"] is False
