# AI 70U Trading Experiment

> 给 AI 70 USDT，让它完全自动交易，30 天后真实结果会怎样？
> 目的不是证明 AI 一定赚钱，而是用真实数据客观验证。

**Phase 1: SPOT PAPER TRADING ONLY — 严格禁止真钱、期货、杠杆。**

## 实验设计

| 项目 | 值 |
|---|---|
| 初始模拟资金 | 70 USDT（固定，不可更改） |
| 实验周期 | 30 天 |
| 市场 | BTC/USDT 现货（流动性最高） |
| 时间框架 | 1h K 线 |
| 数据源 | Binance 公开行情 API（`data-api.binance.vision`，无需 Key）备用 Kraken |
| 交易成本 | 手续费 0.1%/边 + 滑点 0.05%/边，全部计入 |

## 两个环境

- **BACKTEST**：历史回测，用于研究策略。随便折腾。
- **PAPER LIVE**：真正的 70U 实验。开始前冻结 Strategy v1，之后任何修改记为 v2，不覆盖 v1 历史。

## Benchmark（非常重要）

AI 策略必须和 **Buy & Hold** 对比：
第一天用 70 USDT 全仓买入 BTC 并持有 30 天，现在价值多少？

如果 AI 赚 10% 但 BTC 同期涨 20%，**不能宣传 AI 策略成功**。

## 仓库文件

| 文件 | 说明 |
|---|---|
| `EXPERIMENT_RULES.md` | 实验铁律（禁令清单） |
| `RISK_RULES.md` | 风控规则 |
| `STRATEGY.md` | 策略说明（v1 已冻结） |
| `CHANGELOG.md` | 所有策略版本变更记录 |
| `data/trades.csv` | 不可修改的交易日志 |
| `data/daily_equity.csv` | 每日权益曲线 |
| `dashboard.html` | 实时 Dashboard |
| `research/AI_TRADING_CASES.md` | 公开 AI 交易案例调研 |

## 快速开始

```bash
pip install -r requirements.txt
# 回测
python -m src.backtest --strategy ma_trend --days 730
# Paper Live 单步执行（由 cron 每小时调用）
python -m src.paper --step
# 生成 Dashboard
python -m src.dashboard
```

## 安全声明

- 本实验**不索取、不存储**任何交易所密码、Seed Phrase、私钥。
- 第一阶段**不使用**任何有交易/提现权限的 API Key。
- 行情全部来自公开 API，只读，无需账户。

## 30 天结束后的交付

无论盈亏，如实报告：70 USDT → 最终多少、收益率、最大回撤、手续费、交易次数、Buy & Hold 收益、是否跑赢 Benchmark、多少利润来自市场上涨、多少来自策略本身。

**禁止使用"AI稳赚""被动收入机器"等宣传语言。**
