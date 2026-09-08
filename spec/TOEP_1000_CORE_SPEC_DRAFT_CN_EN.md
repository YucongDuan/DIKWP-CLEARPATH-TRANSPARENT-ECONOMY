# TOEP-1000:2026-DRAFT

## Transparent Opportunity Economy Protocol / 透明机会经济协议

### Status

Author-side pre-standard draft. It is not an ISO, ILO, OECD, W3C, 1EdTech, government, or labour-regulator standard.

作者侧预标准草案，不代表任何国际组织或政府已采纳。

## 1. Scope / 范围

TOEP defines machine-readable requirements for publishing, evaluating, closing, reopening, and correcting economic opportunity routes in a model-native economy.

TOEP 规定模型原生经济中机会路径的发布、评估、关闭、重新打开和纠错要求。

## 2. Normative language / 规范用语

`MUST`, `MUST NOT`, `SHOULD`, and `MAY` are normative.

## 3. Core objects / 核心对象

- `PersonPurposeProfile`
- `DIKWPCapabilityEvidence`
- `OpportunityTruthRecord`
- `PluralWorldSet`
- `RouteAnalysis`
- `TrainingIntegrityRecord`
- `ContributionProposal`
- `RealityReceipt`
- `AppealAndCorrectionRecord`

## 4. Normative requirements / 规范要求

### 4.1 Route identity and scope / 路径身份与范围

- R-001: An opportunity record MUST identify one concrete route, customer segment, and time period.
- R-002: A route decision MUST NOT be represented as a judgment of human worth, general intelligence, morality, or permanent employability.
- R-003: Every record MUST include a capture time, effective time, and expiry or review time in a production deployment.
- R-004: A route MUST identify the expected accepted outcome rather than only a course or tool name.

### 4.2 Funded demand and supply denominator / 付费需求与供给分母

- R-010: The publisher MUST distinguish funded demand from views, interest, downloads, waitlists, and verbal enthusiasm.
- R-011: The record MUST disclose funded paid capacity or declare it unknown.
- R-012: The record MUST disclose current qualified supply and its counting method or declare it unknown.
- R-013: The record SHOULD disclose expected new supply over the same time period.
- R-014: Demand and supply estimates MUST carry a source and uncertainty class in production.
- R-015: Supplier concentration and first-mover capture SHOULD be disclosed when material.
- R-016: A route with unknown funded demand MUST NOT be marketed as a generally available economic outcome.

### 4.3 Costs and timing / 成本与时间

- R-020: Price, variable cost, entry cost, time to first paid receipt, and required weekly time MUST be separated.
- R-021: Debt-financed entry risk SHOULD be disclosed.
- R-022: A route SHOULD publish a maximum loss and stop condition for experiments.
- R-023: An estimate of opportunity lifetime SHOULD be versioned and reviewable.

### 4.4 DIKWP evidence / DIKWP证据

- R-030: Storage capability D/I/K/W/P MUST remain distinct.
- R-031: The system MUST support directed transformation requirements among D/I/K/W/P.
- R-032: Capability claims MUST include an evidence stage.
- R-033: Exposure to content MUST NOT be equated with demonstrated transfer or verified action.
- R-034: A public capability card MUST exclude private constraints by default.
- R-035: Capability evidence MUST be Purpose-bounded and expiring in production.

### 4.5 Plural worlds / 多世界

- R-040: A consequential route analysis MUST retain at least two non-identical worlds.
- R-041: World weights MUST NOT be misrepresented as objective probabilities unless independently estimated.
- R-042: The analysis MUST report a robust floor or equivalent adverse-world result.
- R-043: A favored world MUST NOT silently erase material adverse worlds.

### 4.6 Decisions / 判定

- R-050: The system MUST distinguish `GO_NOW`, `TEST_CHEAPLY`, `PIVOT_TO_COMPLEMENT`, and `NO_CURRENT_VIABLE_PATH`, or document equivalent semantics.
- R-051: Every adverse or closing decision MUST publish reason codes.
- R-052: Every closing decision MUST publish conditions that could reopen the route.
- R-053: `NO_CURRENT_VIABLE_PATH` MUST apply only to the declared route and constraints.
- R-054: A multi-route system MUST be able to state that no route was found in the tested set without making a global claim about the person.

### 4.7 Training integrity / 培训诚信

- R-060: A training offer SHOULD disclose marketed seats and downstream paid capacity for the claimed route.
- R-061: Success cases SHOULD be accompanied by a complete or clearly bounded entrant denominator.
- R-062: Training value and downstream employment or business value MUST be distinguished.
- R-063: High-certainty outcome claims in highly saturated routes MUST trigger review.
- R-064: A provider MUST NOT suppress evidence that the claimed opportunity has expired or contracted.

### 4.8 Contribution and settlement / 贡献与结算

- R-070: Contribution records SHOULD identify the DIKWP transformation performed.
- R-071: Evidence, verified outcome share, responsibility, scarcity, and risk burden MAY inform an allocation proposal.
- R-072: The platform fee MUST be separately disclosed.
- R-073: Correction and commons reserves SHOULD be separately disclosed.
- R-074: A reference analysis engine MUST NOT execute payment without external lawful authorization.

### 4.9 Rights, privacy, and worker protection / 权利、隐私与劳动保护

- R-080: Private financial, health, family, political, religious, and location information MUST be excluded from public cards by default.
- R-081: Private vulnerability MAY increase support but MUST NOT reduce rights.
- R-082: TOEP data MUST NOT be converted into a secret social-credit or general human-value score.
- R-083: Collective labour standards MUST NOT be silently replaced by individualized scoring.
- R-084: Regulated and safety-critical work MUST preserve professional and legal requirements.

### 4.10 Appeal, correction, and retirement / 申诉、纠错与退役

- R-090: Consequential records MUST support appeal.
- R-091: A confirmed error MUST support record correction and downstream notice.
- R-092: Verified loss SHOULD support appropriate restoration or compensation by the responsible institution.
- R-093: A repeatedly contradicted model or parameter MUST be revised or retired.
- R-094: Appealing MUST NOT itself reduce a person's route access or reputation.

### 4.11 Agent authority / Agent权限

- R-100: Agents MAY analyze, compare, draft, and prepare proposals.
- R-101: Agents MUST NOT self-grant employment, payment, credit, benefit, legal, or publication authority.
- R-102: Successor agents MUST re-authorize inherited private data, credentials, and mandates.
- R-103: External action authority MUST be explicit and auditable; the reference profile sets it to zero.

## 5. Conformance levels / 符合等级

- L0: identity, buyer, purpose, time.
- L1: demand, supply, price, cost, evidence.
- L2: DIKWP requirements, capability evidence, privacy.
- L3: plural worlds, decisions, closure, reopening.
- L4: training integrity, contribution, reality receipts.
- L5: signatures, revocation, cross-institution correction, independent audit.

A higher level includes all lower levels.

## 6. Reference profile / 参考实现

The ClearPath v1.0.0 reference profile has:

```text
automatic_external_action_authority = 0
automatic_employment_decision_authority = 0
automatic_payment_authority = 0
person_level_worth_score = null
```
