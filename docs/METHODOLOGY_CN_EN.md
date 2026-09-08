# ClearPath Methodology / ClearPath 数学与判定方法

## 1. Scope / 范围

ClearPath evaluates a **specific opportunity route under declared constraints**. It does not estimate intelligence, human worth, morality, or permanent employability.

ClearPath 评价的是“具体机会路径 × 声明约束”，不评价智力、人的价值、善恶或永久就业能力。

## 2. Capability evidence / 能力证据

Each DIKWP transformation has:

```text
score: 0..5
evidence stage: 0..7
receipts: zero or more identifiers
```

Evidence stages:

```text
EXPOSED → RETRIEVED → EXPLAINED → DISCRIMINATED
→ TRANSFERRED → ACTED → VERIFIED → RETAINED
```

Strength:

\[
E_t=0.52\frac{s_t}{5}+0.36\frac{g_t}{7}+0.12\min(1,\frac{n_t}{3})
\]

Available capability:

\[
A_t=0.78E_t+0.22S_{src(t)}
\]

## 3. Market denominator / 市场分母

\[
\sigma_w=\frac{(S_0+S_1)s_w}{\max(Qd_w,1)}
\]

where \(Q\) is funded capacity, \(S_0\) is current qualified supply, \(S_1\) is expected new supply, and \(d_w,s_w\) are world multipliers.

## 4. Opportunity half-life / 机会半衰期

\[
c=\max(0,g_s-g_d+0.55a_w)
\]

\[
T_{1/2}=\frac{\ln2}{c}\cdot12
\]

This is an analytical indicator, not a forecast of a literal market expiry date.

## 5. Residual non-commoditized need / 剩余不可商品化需求

\[
R=clip[(1-a)+0.42r+0.32p+0.26l]
\]

where \(a\) is automation, \(r\) accountability, \(p\) physical-world share, and \(l\) local-context share.

## 6. First-mover capture / 先发者占位

\[
F=clip[0.35c_{10}+0.30f(\sigma)+0.20f(T)+0.15d]
\]

This combines supplier concentration, saturation, short remaining lifetime, and distribution requirements.

## 7. Route viability / 路径可行度

The engine preserves ten factors:

```text
capability
access
budget
runway
time
remaining paid slots
residual need
margin
concentration
risk fit
```

It uses a geometric mean:

\[
V_w=\left(\prod_{k=1}^{10}x_{kw}\right)^{1/10}
\]

A geometric mean prevents one severe bottleneck from being hidden by unrelated strengths.

## 8. Plural worlds / 多世界

Default worlds:

1. Governed augmentation / 受治理增强
2. Rapid commoditization / 快速商品化
3. Platform concentration / 平台集中
4. Local trust reopens niches / 本地信任重新打开机会
5. AGI-scale labour compression / AGI 级劳动压缩

\[
V_{floor}=\min_wV_w
\]

\[
\bar V=\frac{\sum_w\omega_wV_w}{\sum_w\omega_w}
\]

Weights are decision-importance weights, not objective probabilities.

## 9. Route decisions / 路径结论

Hard closure occurs for declared conditions including:

- no funded opportunity;
- non-positive unit margin;
- entry cost and runway both fail;
- extreme saturation without differentiation.

The thresholds are transparent policy parameters and may be calibrated with real outcome data.

## 10. Training integrity / 培训诚信

\[
Coverage=\frac{Q}{Seats}
\]

\[
DownstreamValue=Q\max(Price-Cost,0)
\]

\[
TrainingRevenue=Seats\cdot TrainingPrice
\]

A high risk result is a request for disclosure and review, not an automatic accusation of fraud.

## 11. Contribution allocation / 贡献分配

\[
Score_i=0.30O_i+0.24E_i+0.20R_i+0.16S_i+0.10B_i
\]

The reference core produces a proposal only. It does not transfer money.

## 12. Recalibration / 重新校准

Every real deployment should compare predictions with:

- paid test acceptance;
- time to first paid receipt;
- actual margin;
- rework;
- buyer repetition;
- opportunity expiry;
- appeal and correction outcomes.

Parameters that repeatedly fail should be revised or retired.
