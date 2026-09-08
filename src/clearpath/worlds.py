from __future__ import annotations

from .models import WorldSpec


def default_worlds() -> list[WorldSpec]:
    return [
        WorldSpec("governed_augmentation", "Governed augmentation", 0.24, 1.15, 1.15, 0.90, 1.00, 1.00),
        WorldSpec("rapid_commoditization", "Rapid capability commoditization", 0.24, 0.82, 1.75, 1.30, 0.66, 0.92),
        WorldSpec("platform_concentration", "Winner-take-most platform concentration", 0.18, 0.90, 1.40, 1.05, 0.80, 0.72),
        WorldSpec("local_trust_reopens", "Local trust and responsibility reopen niches", 0.20, 1.12, 0.88, 0.78, 1.08, 1.24),
        WorldSpec("agi_labor_compression", "AGI-scale labour-value compression", 0.14, 0.58, 2.20, 1.55, 0.48, 0.85),
    ]
