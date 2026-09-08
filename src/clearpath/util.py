from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ClearPathError(ValueError):
    """Raised when an input violates an explicit ClearPath contract."""


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ClearPathError("A finite numeric value is required")
    return max(low, min(high, value))


def nonnegative(value: Any, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise ClearPathError(f"{name} must be finite and nonnegative")
    return number


def positive(value: Any, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise ClearPathError(f"{name} must be finite and positive")
    return number


def sha256_json(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ClearPathError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ClearPathError(f"Invalid JSON in {path}: {exc}") from exc


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def geometric_mean(values: list[float], floor: float = 1e-6) -> float:
    if not values:
        return 0.0
    return math.exp(sum(math.log(max(floor, clamp(v))) for v in values) / len(values))
