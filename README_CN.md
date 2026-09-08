[English](README.md) · [项目选择](ECOSYSTEM.md) · [本次验证](publication/VALIDATION_2026-09-08.md)

# DIKWP ClearPath 透明机会经济系统

**先公开真实付费需求，再售卖技能。**

ClearPath 是一个离线优先、可直接运行的开源系统，用来判断：在当前供需、自动化、首发者占位、本人时间、资金、客户入口和 DIKWP 能力证据条件下，一条具体经济路径究竟仍有付费空间，还是应当停止投入。

系统包括：

- 机会容量真相表；
- D/I/K/W/P 五类存储能力与 25 条转换能力；
- 五个相互冲突的未来世界；
- 供给饱和和先发者占位审计；
- 培训席位与真实付费机会的诚信审计；
- `立即进入 / 低成本验证 / 转向互补位置 / 当前无可行路径` 四种结论；
- 多路径机会组合判定；
- 透明贡献分配提案；
- 可验证的追加式责任账本。

系统评价的是“具体路径 × 当前约束”，不是人的智力、尊严、善恶或永久就业价值。

## 直接运行

双击打开：

```text
DIKWP_CLEARPATH_TRANSPARENT_ECONOMY_OS_v1.0.0.html
```

无需账户、服务器、模型 API 或网络连接。

## 命令行

```bash
python -m pip install .
clearpath demo --workspace .clearpath-demo --reset

clearpath portfolio \
  examples/person-profile.json \
  examples/generic-ai-microsaas.json \
  examples/local-sme-workflow-builder.json \
  examples/local-care-navigation.json
```

## 结论语义

- `GO_NOW`：可以进入一个范围窄、可退出、有真实付费承诺的试验。
- `TEST_CHEAPLY`：只支持低成本、可逆、预先限定损失的验证。
- `PIVOT_TO_COMPLEMENT`：应从通用执行转向行业语境、信任、责任、本地执行或 Purpose 承担。
- `NO_CURRENT_VIABLE_PATH`：在具名证据改变关闭条件前，停止继续购买课程、开发或投入。

最后一种结论不等于“这个人没有出路”，只表示当前被测试的路径没有足够依据。

## 硬边界

```text
自动外部行动权限 = 0
自动就业决定权限 = 0
自动付款权限 = 0
人的价值总分 = 不存在
```
