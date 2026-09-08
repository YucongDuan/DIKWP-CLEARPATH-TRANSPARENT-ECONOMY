# DIKWP ClearPath Transparent Opportunity Economy OS

**Show the paid demand before selling the skill.**

ClearPath is an offline-first, open-source system for deciding whether a specific economic route still has funded room for a specific person under declared constraints. It combines:

- an opportunity-capacity truth sheet;
- a 5 x 5 DIKWP storage-and-transformation capability map;
- five incompatible labour-market worlds;
- a first-mover and saturation audit;
- a training-opportunity integrity audit;
- route-level `GO_NOW`, `TEST_CHEAPLY`, `PIVOT_TO_COMPLEMENT`, or `NO_CURRENT_VIABLE_PATH` decisions;
- a multi-route portfolio decision;
- transparent contribution-allocation proposals;
- append-only responsibility receipts.

ClearPath never converts a route decision into a score of human intelligence, dignity, morality, or permanent employability.

## Direct use

Open `DIKWP_CLEARPATH_TRANSPARENT_ECONOMY_OS_v1.0.0.html` in a modern browser. No account, server, model API, or network connection is required.

## CLI

```bash
python -m pip install .
clearpath demo --workspace .clearpath-demo --reset

clearpath analyze \
  examples/person-profile.json \
  examples/local-sme-workflow-builder.json \
  --output-dir .clearpath-analysis \
  --reset

clearpath portfolio \
  examples/person-profile.json \
  examples/generic-ai-microsaas.json \
  examples/local-sme-workflow-builder.json \
  examples/local-care-navigation.json
```

## Core result semantics

- `GO_NOW`: a narrow paid test is supported by the declared demand, capability, access, time, and risk conditions.
- `TEST_CHEAPLY`: only a small reversible test is justified.
- `PIVOT_TO_COMPLEMENT`: generic execution is weak; move toward domain context, trust, accountability, local execution, or Purpose-bearing work.
- `NO_CURRENT_VIABLE_PATH`: stop spending on this route until named evidence changes a closure condition.

The last status never means that the person has no value or no future.

## Why it exists

Model-native software makes code, interfaces, and tool use easier to reproduce. This lowers the price of generic execution but does not automatically create customers, funded demand, trusted access, legal authority, local context, accountability, or distribution. ClearPath makes that denominator visible before a person buys another course or spends months building an undifferentiated product.

## Runtime boundary

```text
automatic_external_action_authority = 0
automatic_employment_decision_authority = 0
automatic_payment_authority = 0
person_level_worth_score = null
```

## License

Apache License 2.0. See `LICENSE`.
