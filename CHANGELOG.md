# CHANGELOG.md

所有策略版本变更、规则变更、重要事件的时间线。只追加，不修改历史条目。

## 2026-09-24
- 项目创建。Phase 1: SPOT PAPER TRADING ONLY。
- 初始规则文档：README / EXPERIMENT_RULES / RISK_RULES / STRATEGY / CHANGELOG。
- 三个候选策略定义：ma_trend / rsi_reversion / donchian_breakout。
- v1 选择规则确定（回测前）：score = (strategy_return - buyhold_return) / (1 + max_drawdown)，门槛 ≥30 笔交易。
- **v1 冻结：hold_cash**。730 天回测三候选全部跑输 Buy&Hold（+48.85%）：ma_trend -31.73% / rsi_reversion -26.05% / donchian_breakout -44.78%，score 全 < 0。按预定规则 v1 = 空仓观望。报告：research/BACKTEST_V1.md。
- Paper Live 30 天实验启动（每小时 1 步）。
- **目标定位修正（用户裁定）**：30 天目标是"检验能不能跑赢 BTC Buy&Hold"，不是"跑赢"这个 KPI。Buy&Hold 是对照组和标尺。详见 EXPERIMENT_RULES.md v1.1。
- **结算四件事（用户裁定）**：到期只看——最终净值、同期 Buy&Hold、最大回撤、扣手续费/滑点后的超额收益。冻结期内不再干预、不再加策略任务。实验转长期观察线，主力精力回 Spin & Learn + Roblox AI 自动化开发底座。
- 公开案例调研完成：research/AI_TRADING_CASES.md（12 可验证案例 / 7 营销拆解 / 7 失败安全案例）；原始证据索引：research/EVIDENCE_INDEX.md（关键数字逐项挂原始来源 + 采集日期 2026-09-24）。
