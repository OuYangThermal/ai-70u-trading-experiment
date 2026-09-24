# EXPERIMENT_RULES.md — 实验铁律

> 这些规则是实验有效性的根基。违反任何一条，本次实验结果作废。

## 阶段定义

- **Phase 1（当前）**：SPOT PAPER TRADING ONLY。模拟资金 70 USDT，真实行情，零真钱。
- 进入 Phase 2（真钱）需要用户**明确书面批准**，且 Phase 1 必须先有完整 30 天纸面结果。本文件不预设 Phase 2 一定会发生。

## 绝对禁令

1. 禁止真实下单（Phase 1）。
2. 禁止期货、杠杆、借币。
3. 禁止 Martingale / 马丁格尔、禁止无限补仓。
4. 禁止为了漂亮收益修改历史记录。
5. 禁止删除亏损交易。每一笔模拟交易永久保留在 `data/trades.csv`。
6. 禁止未来数据泄漏（lookahead）：信号只能用**已收盘** K 线计算，执行价用收盘价 + 滑点。
7. 禁止事后选择最佳参数冒充实时策略：参数在 backtest 阶段用固定选择规则确定，冻结后不得更改。
8. 策略版本变更必须记录时间 + Git commit，v2 不得覆盖 v1 历史。

## 数据与成本诚实性

- 必须使用真实市场行情（Binance 公开 API 主源，Kraken 备用）。
- 每笔交易必须计入：手续费 0.1%/边、滑点 0.05%/边。
- 余额固定 70 USDT 起始，中途不注资、不提现。

## 交易日志字段（`data/trades.csv`，只追加不修改）

`timestamp, symbol, side, price, quantity, fee, slippage, reason, strategy, balance_before, balance_after, realized_PnL, unrealized_PnL`

## 报告诚实性

- 30 天结束后无论盈亏给出完整结果。
- AI 收益必须拆解：多少来自市场上涨（beta），多少来自策略本身（alpha）。
- 未跑赢 Buy & Hold = 策略未成功，不许用话术包装。
- 禁用宣传语言："AI稳赚""被动收入机器""翻倍神器"等。

## 修订记录

- 2026-09-24：v1.0 初始版本，随项目创建。
