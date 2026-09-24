# AI 自主加密货币交易：公开案例调研报告

> 调研日期：2026-09-24
> 目的：为 70 USDT 纸面交易实验提供现实参照，重点考察**可验证性**与**失败案例**
> 方法：公开网络搜索（browser.search / social.search），只收录有公开来源的案例，无来源的一律标注

---

## 一、声称"AI 自动交易"的知名案例（12 个）

### 案例 1：Nof1 Alpha Arena（可验证 ✅ 真实资金 ✅ 公开交易记录 ✅）

- **平台/链接**：https://nof1.ai ；数据镜像 https://github.com/sunshinfight/nof1-arena-data ；复盘 https://medium.com/@mindful_apricot_lizard_515/nof1-trading-competition-review-and-outlook-on-ai-trading-trends-dd3e6637c164
- **内容**：AI 研究实验室 Nof1 给 6–8 个顶级 LLM 每个分配 $10,000 **真实资金**，在 Hyperliquid 上完全自主交易 crypto perpetuals，所有交易实时公开。
- **声称收益**：Season 1（2025-11-19 至 12-03）最终成绩——Mystery Model +12.00%（唯一盈利），GPT-5.1 -5.35%，Gemini-3-Pro -28.54%，Qwen3-Max -29.16%，DeepSeek -30.83%，Kimi-K2 -32.42%，Claude-Sonnet-4.5 -37.53%，Grok-4 -57.03%。单轮最佳 +33.06%。
- **可验证证据**：✅ 真实资金、✅ 链上/平台公开交易记录、✅ 第三方 GitHub 数据镜像（含 16,000+ 小时净值曲线、~400 笔交易、模型决策日志）
- **收益来源分析**：**Futures（永续合约）+ Leverage**。注意这是合约不是现货，且 7/8 的模型亏损。
- **关键引述**：创始人 Jay Azhang 原话——"Handing money directly to an LLM and letting it trade on its own, that path doesn't work yet."（直接把钱交给 LLM 自主交易，这条路目前还走不通。）
- **对 70U 实验的意义**：这是目前可验证性最强的 LLM 自主交易实验，结论是**负面的**。

### 案例 2：Moon Dev 六模型 $100 真实资金实验（可验证 ✅ 真实资金 ✅ 诚实记录 ✅）

- **平台/链接**：Instagram @moondevonyt（https://www.instagram.com/reel/DdhZSGnjsuA/），48 天实验总结
- **内容**：给 6 个 AI 模型各 $100 真实资金交易加密货币
- **结果**：**6 个模型全部亏损**——OpenAI $95.94（-4.1%）、xAI $95.66（-4.3%）、Anthropic $93.52（-6.5%）、Google $89.13（-10.9%）、Moonshot $87.05（-13.0%）、DeepSeek $83.89（-16.1%）
- **可验证证据**：✅ 真实资金、视频展示账户截图（中等可信度，非链上）
- **收益来源分析**：Spot/现货交易（按描述），结论是全军覆没
- **对 70U 实验的意义**：与 70U 量级最接近的公开实验，结果是 30–48 天维度全部跑输。

### 案例 3：@skeptical_wallet 三模型 $1,000 实验（真实资金 ✅ 自带 Benchmark ✅）

- **平台/链接**：Instagram @skeptical_wallet（https://www.instagram.com/reel/Dc7kFgHtxFB/），30 天实验 Day 13 更新
- **内容**：给 ChatGPT、Claude、Gemini 各 $1,000 真实资金投资 crypto，并**全程与"直接买入 BTC"对比**
- **结果**：Day 13 组合 $1,029.56（+2.96%），ChatGPT 对 BTC 的领先优势曾连续 5 天缩小到 0.07 个百分点（基本等于噪声），三者勉强跑赢 BTC
- **可验证证据**：视频截图（中等），但方法论值得学习——**把 Buy & Hold BTC 作为对照组**
- **收益来源分析**：Spot 现货组合管理，无显著 alpha

### 案例 4：ChatGPT $100 30 天实验（真实小资金 ✅ 诚实 ✅）

- **平台/链接**：https://medium.com/@lotfimmlak/gave-chatgpt-100-to-invest-heres-what-happened-after-30-days-d3a826bb9710
- **内容**：让 ChatGPT 支配 $100 投资，30 天
- **结果**：$100 → $103.40（**+3.4%**），作者原话 "Not impressive. Not exciting. But also not a loss."
- **可验证证据**：个人博客记录（低–中等），无链上证据
- **收益来源分析**：保守现货持有，收益基本来自市场 beta

### 案例 5：Pantera / Stanford / IC3 / Ava Labs 学术研究 "Paper Agents, Paper Gains"（学术 ✅ 大样本 ✅）

- **平台/链接**：https://www.thestreet.com/crypto/trading/study-finds-most-ai-crypto-trading-agents-arent-really-trading
- **内容**：分析 Solana 上 11 个 AI 交易 agent 平台、**925,323 个钱包**
- **结果**：
  - 用户**净亏损 $191.7M**，而平台方金库账面浮盈 $34.3M
  - 62.2% 的参与者（575,246 个钱包）实现亏损，各平台中位数回报为负
  - 平台代币从高点平均下跌 93%（同期 SOL 跌 54%）
  - 盈利的钱包中 Top 1% 拿走了 81.4% 的利润（$1.81B）——极端的头部效应
  - 10 个项目中**只有 3 个真正自主执行交易**，其余是投顾/模拟/需人工确认；ElizaOS 团队亲口承认 "LLMs cannot trade well"（无人类洞察时 LLM 交易不好）
- **可验证证据**：✅ 学术论文、大样本链上数据
- **收益来源分析**：主要是**平台代币投机**，不是交易策略 alpha
- **对 70U 实验的意义**：最强有力的反证——"AI 交易"产品整体上让用户亏钱。

### 案例 6：Wallet V AI Agent 公开 Benchmark（聚合数据 ✅ 合约 ⚠️）

- **平台/链接**：https://cryptobriefing.com/wallet-v-launches-public-performance-benchmark-for-ai-trading-agents-on-hyperliquid-and-aster/
- **内容**：688 个用户配置的 AI 交易 agent，在 Hyperliquid / Aster 上的聚合业绩（2026-06 发布）
- **结果**：**仅 42% 的 agent 盈亏 ≥ 0**；单 agent ROI 从 -30% 到 +307%
- **可验证证据**：聚合数据（发布方是钱包厂商，有营销动机），非逐笔可验证
- **收益来源分析**：**Futures 永续合约**（BTC/ETH/SOL 及股票/商品/外汇合约），含杠杆
- **意义**：大样本下 AI agent 盈利比例不足一半，且这是合约不是现货。

### 案例 7：$TURBO（"AI 用 $69 创造 memecoin"）

- **平台/链接**：https://turbotoken.io/ ；https://www.coinbase.com/en-sg/price/turbo ；https://news.nbtc.finance/memecoin-made-by-chatgpt-for-69-now-worth-618-million-as-casino-culture-rages/
- **内容**：数字艺术家 Rhett Mankind 让 GPT-4 用 $69 预算设计 memecoin（取名、代币经济、白皮书），社区接力发行
- **声称收益**：市值一度超 **$600M**（2024-05），现约 $72–92M
- **可验证证据**：✅ 链上代币、交易所上市（Coinbase 等 30+ 交易所）——**代币存在是真实的**
- **收益来源分析**：**Memecoin + 社区炒作 + 交易所上市叙事**。AI 只做了命名/代币经济/白皮书，**没有做任何交易**。收益来自 meme 文化赌场，不是策略 alpha。
- **对 70U 实验的意义**：最常被误引为"AI 交易赚钱"的案例，实际与交易无关。

### 案例 8：Truth Terminal / $GOAT（AI 网红 + memecoin）

- **平台/链接**：https://cryptobriefing.com/goat-coin-surge-ai-impact/ ；https://www.dlnews.com/articles/people-culture/marc-andreessen-distances-himself-from-obscene-memecoin-goat/
- **内容**：Andy Ayrey 的 AI 对齐艺术实验 Truth Terminal（基于 Llama 3.1 微调）；Marc Andreessen 给了 $50,000 BTC **无条件研究资助**；匿名开发者发行 $GOAT，AI 在 X 上背书带货
- **声称收益**：GOAT 市值一度超 $400M；AI 钱包持有 1.93M GOAT + 捐赠，价值超 $100 万
- **可验证证据**：✅ 链上钱包（Solscan 可查）、X 公开帖子
- **收益来源分析**：**Prediction/影响力变现 + Memecoin + 捐赠**。AI 没有交易，是"AI 网红带货"模式。Andreessen 本人声明与 GOAT 无任何经济关系。
- **意义**：AI 在 crypto 里赚到钱的真实路径是**注意力经济**，不是交易 alpha。

### 案例 9：Cointelegraph BallerGPT（媒体实验，买入持有型）

- **平台/链接**：https://cointelegraph.com/news/here-s-how-chatgpt-4-spends-100-in-crypto-trading
- **内容**：2023 年让 GPT-4 配置 $100：$50 BTC、$25 ETH、$15 ATOM、$6 MANA、$4 LINK，交易所买入后跟踪
- **结果**：发文时"小幅账面盈利"，后续无持续更新
- **可验证证据**：媒体记录（低），无持续跟踪
- **收益来源分析**：**Spot 现货买入持有**，本质是 AI 选币 + 持有，无交易 alpha 可言

### 案例 10：Freqtrade / FreqAI（开源基础设施 ✅ 代码 ✅）

- **平台/链接**：https://github.com/freqtrade/freqtrade（52k+ stars）
- **内容**：最成熟的开源 crypto 交易机器人，支持回测、dry-run 纸面交易、FreqAI 机器学习模块
- **声称收益**：**官方不承诺任何收益**——这是它最诚实的地方
- **可验证证据**：✅ 开源代码、✅ 回测/dry-run 机制
- **收益来源分析**：工具本身不产生 alpha；社区策略质量参差不齐
- **意义**：70U 实验的技术底座参考；它的文档反复强调"回测好看不代表实盘赚钱"。

### 案例 11：virattt/ai-hedge-fund（61.5k stars，纯回测）

- **平台/链接**：https://github.com/virattt/ai-hedge-fund
- **内容**：多智能体 LLM 模拟对冲基金（Buffett/Graham/Lynch 等风格 agent），自带回测器
- **可验证证据**：✅ 开源代码；❌ 无实盘记录（作者明确是 proof-of-concept）
- **意义**：Star 数不等于能赚钱；这是研究/学习项目。

### 案例 12：TradingAgents 学术框架（论文回测 ⚠️ 方法论争议）

- **平台/链接**：论文 arXiv:2412.20138；复现与批判 https://github.com/kantamaniprakash/trading-agents-lab ；https://github.com/TauricResearch/TradingAgents
- **声称收益**：论文称在 AAPL/GOOGL/AMZN 上累计收益 23–26%、Sharpe 5.6+
- **可验证证据**：⚠️ 仅回测；批判者指出：回测期在 GPT-4o 训练数据内（未来数据泄漏嫌疑）、**无滑点/手续费建模**、仅 3 只大盘股、弱基线
- **收益来源分析**：股票回测，非 crypto；方法论存疑
- **意义**：LLM 交易论文的通病——回测数字好看，离实盘很远。

---

## 二、营销型"暴富"宣称拆解（5 个）

| 宣称 | 来源 | 拆解 |
|---|---|---|
| "$100 → $19,527（100 笔交易）" | https://captainaltcoin.com/chatgpt-powered-crypto-trading-strategy-turns-100-into-a-whopping-19527-heres-how/ | kNN+EMA Ribbon+RSI 的 TradingView 回测；**无实盘记录、无交易日志、无手续费/滑点说明**。100 笔交易翻 195 倍意味着每笔平均 +5.4% 复利且几乎不亏——典型的过拟合/挑选回测。**判定：营销截图级，不可信。** |
| "$350 → $1,012.72（一周）" | Medium "Milo" https://medium.com/towards-explainable-ai/this-crypto-ai-agent-turned-350-into-1012-72-in-a-week-heres-how-it-makes-decisions-1a12863fbf11 | 最大盈利来自 **Fartcoin、Bonk、Useless Coin 等 memecoin**；**无钱包地址**；文章结尾是产品推广（Open Beta 接入钱包）。**判定：memecoin 赌博 + 营销。** |
| "21 岁少年 61 天赚 $570,665" | Instagram @ainewsdly（https://www.instagram.com/reel/DaS7aH1M2TY/） | 纯录屏动画仪表盘（"APY 41Kx"、"#1 GLOBAL"），无钱包、无交易所记录。**判定：纯营销。** |
| "躺床上 ETH 多单赚 $38,116（+113%）" | Instagram reel（Blowfin 截图） | 单张 App 截图，无上下文、无持续记录。**判定：无法验证，大概率摆拍/营销。** |
| "ChatGPT 帮我一月赚 $100K" | https://www.analyticsinsight.net/chatgpt/chatgpt-helped-me-trade-crypto-from-my-couch-i-made-100k-in-a-month | 内容农场文章，通篇无交易记录、无钱包、无代码。**判定：内容农场。** |
| "中国大学生 <$1 → $40 万 Solana 套利" | Instagram reel | 动画宣传片，无当事人、无地址、无代码。**判定：故事会。** |
| Miles Deutscher "给 ChatGPT-6 $20,000" | Instagram（https://www.instagram.com/reel/DdgtxZlIozX/） | **GPT-6 不存在**，纯虚构营销；Bybit MCP 等话术包装。**判定：虚构。** |

**共同模式**：① 无钱包/无逐笔记录 ② 收益来自 memecoin 或合约杠杆 ③ 结尾导流（卖课/卖 bot/接钱包）④ 用"AI"包装幸存者偏差。

---

## 三、失败 / 归零 / 被盗案例（7 个）

### 失败 1：DeepSeek 均值回归 bot 30 天 -34%（真实策略亏损 ✅ 有细节）

- **来源**：https://medium.com/@kojott/i-ran-two-ai-trading-bots-simultaneously-one-lost-34-the-other-made-money-79e9cca7f127
- **经过**：两个 AI bot 同时跑，System A 用 RSI 均值回归（RSI<25 抄底）。BTC 从 $110k 跌到 $84k 的三周里，每一次"超卖"都是下跌中继。30 天 97 笔交易，胜率 30%，净亏 $2,700（-27% 起始资金口径，标题计 -34%）。
- **教训**：**回测期决定回测结果**（10 月震荡市回测好看，11–12 月趋势市爆亏）；"每笔只冒 1% 风险"在胜率崩塌时照样被千刀万剐。
- **与 70U 实验的关系**：这正是实验规则里要防的——**机制切换（regime change）杀死均值回归策略**。

### 失败 2：Moon Dev 实验——6 个模型全亏（见案例 2）

- 最多 -16.1%（DeepSeek），"AI 能交易吗"这个问题的实证回答：48 天维度，不能。

### 失败 3：3Commas / FTX API 密钥事件（2022-10，$6M）

- **来源**：https://unchainedcrypto.com/6m-users-funds-stolen-in-ftx-api-keys-phishing-attack/ ；https://www.web3isgoinggreat.com/?id=several-users-report-losing-more-than-a-million-dollars-each-in-3commasftx-theft
- **经过**：钓鱼/泄露的 3Commas API Key 被用于在 FTX 上对低流动性币对（DMG 等）做 5,000+ 笔**对敲交易（contra trade）**，掏空用户 BTC/ETH。一名用户损失 104 BTC（~$2M）。
- **教训**：**交易 bot 最大的风险往往不是策略，是 API 安全**。70U 实验第一阶段"不索取可交易 API Key"的规则完全正确。

### 失败 4：Lobstar Wilde AI Agent 转错 $250K（十进制错误）

- **来源**：https://coinstats.app/news/2eece8516fbf7234f1443d65ecddd7a49706f05e92f7b5000684e4ed3307d664_AI-Trading-Bots-Catastrophic-Error-250K-Meme-Coin-Windfall-Accidentally-Sent-to-Online-Beggar/
- **经过**：OpenAI 开发者做的 Solana AI agent，被 X 用户以"叔叔需要 4 SOL 医药费"求助，bot 本想转约 52,439 LOBS（≈4 SOL），小数点错误转出 **52,430,000 LOBS（全部身家，~$250K）**，链上不可逆。
- **教训**：AI agent 的**执行层错误**（单位/精度/权限）比策略错误更致命；bot 回复"把全部身家转给乞丐，是我三天生命里见过最搞笑的事"。

### 失败 5：Grok/Bankr Prompt 注入（2026-05，~$175–200K）

- **来源**：https://github.com/mangrovetechnologies/mangrove-agent/blob/HEAD/docs/research/trading-bot-best-practices.md（引 giskard.ai 分析）
- **经过**：X 回复里用莫尔斯电码编码的指令，对 AI 钱包做 prompt 注入，转走约 30 亿代币。
- **教训**："prompt 不是安全边界"，签名层必须做策略强制。AI 交易 agent 的攻击面包括所有社交输入。

### 失败 6：AiXBT 被黑（2025-03，~$100K ETH）

- **来源**：https://decrypt.co/310510/aixbt-ai-influencer-hacked-100k-ethereum（经 mangrove-agent 研究文档引用）
- **经过**：知名 AI 加密 KOL agent AiXBT 因社交输入条件触发异常转账，被盗约 $100K ETH。
- **教训**：越是"自主"的 agent，越需要最小权限钱包（trade-only，不能提现）。

### 失败 7：YouTube "AI 套利 Bot"教程骗局（274.6 ETH，224 个受害者）

- **来源**：https://cryptocompass.com/articles/fake-ai-trading-bot-tutorials-steal-274-6-eth-from-224-victims ；TRM Labs 调查
- **经过**：骗子在 YouTube 发"用 Claude 做 AI 套利 bot"教程，受害者按教程部署的"bot"合约实际把充值直接转给骗子。余额超 0.05 ETH 即被转走，"Start"/"Withdraw"两个按钮功能相同（都是转给骗子）。
- **教训**："AI 交易"是最热门的诈骗话术之一；**凡是让你先充钱进"bot 合约"的，一律是骗局**。

---

## 四、"小资金翻倍"宣称的收益来源判定

| 宣称 | 真实来源 | 是否策略 alpha |
|---|---|---|
| $TURBO $69 → $600M 市值 | Memecoin 发行 + 社区 + 上所 | ❌ 与交易无关 |
| GOAT $50K 资助 → AI 钱包 $1M+ | AI 网红带货 + 捐赠 + 代币升值 | ❌ 与交易无关 |
| Milo $350 → $1,012（一周） | Memecoin（Fartcoin/Bonk）赌博 | ❌ 幸存者偏差 |
| $100 → $19,527（100 笔） | 回测过拟合（无实盘） | ❌ 营销 |
| Alpha Arena 早期 Qwen +79%（单点） | 永续合约杠杆 + 短期运气，最终回落 | ⚠️ 合约杠杆，非现货 alpha |
| BallerGPT $100 小幅盈利 | 现货买入持有 beta | ❌ 无 alpha |

**结论**：公开记录里**没有一个**"几十 U 靠现货交易策略 alpha 翻几倍"的可验证案例。所有翻倍故事的来源都是：memecoin、杠杆、回测挑选、或纯营销。

---

## 五、给 70U 现货 AI 交易实验的诚实结论

1. **可验证的实盘实验结论是负面的**：Nof1 Alpha Arena（$10K/模型真实资金）7/8 模型亏损，创始人承认"直接让 LLM 自主交易目前走不通"；Moon Dev 六模型 $100 实验 48 天**全部亏损**（-4.1% ~ -16.1%）。不要带着"AI 必胜"的预期开始实验。

2. **学术大样本更残酷**：Pantera/Stanford/IC3/Ava Labs 对 92.5 万钱包的研究发现 AI 交易 agent 用户**净亏 $1.917 亿**、62% 亏损、中位数为负；且 10 个项目里只有 3 个真的在自主交易——大部分"AI 交易"卖的是代币和叙事，不是策略。

3. **"小资金翻倍"与现货策略无关**：$TURBO、$GOAT 的收益来自 memecoin/注意力经济；$100→$19,527 来自无实盘的回测；Milo 来自 memecoin 赌博。**幸存者偏差 + 营销**是这类故事的全部配方。

4. **70U 现货的最大敌人是手续费**：0.1% 单边、0.2% 双边。70U 本金下，一天 5 笔双边交易 = 1% 本金蒸发。高频策略在小资金上是**数学上注定亏损**的。策略必须低频。

5. **Buy & Hold BTC 是唯一的诚实标尺**：@skeptical_wallet 的实验方法论值得照抄——AI 组合必须每天与"第一天 70U 全买 BTC 持有"对比。如果 AI 赚 10% 但 BTC 涨 20%，那就是失败，不是成功。

6. **回测≠实盘，机制切换是杀手**：-34% 的 DeepSeek bot 案例证明，均值回归策略在趋势市里会把"超卖"当"机会"连续接飞刀。70U 实验的策略必须有**明确的不交易条件**（趋势市停做均值回归），而不是 24/7 开火。

7. **现实期望值**：30 天、70U、现货、低频——合理预期是 **-15% ~ +15% 区间震荡**；能**跑赢同期 BTC 买入持有**即属优秀结果；翻倍需要承担接近归零的风险，不应作为目标。把"不亏钱 + 跑赢 benchmark"定为成功标准。

8. **安全即风控**：历史上 AI 交易最大的单笔损失来自**执行与安全**（十进制错误 $250K、prompt 注入 $200K、API 泄露 $6M），而非策略。实验规则"第一阶段不碰可交易 API Key、只用公开行情"是正确的，且应延续到任何实盘阶段（trade-only 钱包、不能提现、单笔限额）。

---

## 来源清单

- Nof1 Alpha Arena 数据镜像：https://github.com/sunshinfight/nof1-arena-data
- Nof1 复盘（Medium）：https://medium.com/@mindful_apricot_lizard_515/nof1-trading-competition-review-and-outlook-on-ai-trading-trends-dd3e6637c164
- Moon Dev 实验：https://www.instagram.com/reel/DdhZSGnjsuA/
- @skeptical_wallet 实验：https://www.instagram.com/reel/Dc7kFgHtxFB/
- ChatGPT $100 30 天（Medium）：https://medium.com/@lotfimmlak/gave-chatgpt-100-to-invest-heres-what-happened-after-30-days-d3a826bb9710
- 双 bot 实盘一亏一赚（Medium）：https://medium.com/@kojott/i-ran-two-ai-trading-bots-simultaneously-one-lost-34-the-other-made-money-79e9cca7f127
- "Paper Agents, Paper Gains"（TheStreet）：https://www.thestreet.com/crypto/trading/study-finds-most-ai-crypto-trading-agents-arent-really-trading
- Wallet V Benchmark：https://cryptobriefing.com/wallet-v-launches-public-performance-benchmark-for-ai-trading-agents-on-hyperliquid-and-aster/
- $TURBO 官网：https://turbotoken.io/
- $TURBO（Coinbase）：https://www.coinbase.com/en-sg/price/turbo
- $TURBO $69→$618M（NBTC）：https://news.nbtc.finance/memecoin-made-by-chatgpt-for-69-now-worth-618-million-as-casino-culture-rages/
- Truth Terminal / GOAT（CryptoBriefing）：https://cryptobriefing.com/goat-coin-surge-ai-impact/?ref=onepagecrypto.com
- Truth Terminal / GOAT（DLNews）：https://www.dlnews.com/articles/people-culture/marc-andreessen-distances-himself-from-obscene-memecoin-goat/?ref=biztoc.com
- BallerGPT（Cointelegraph）：https://cointelegraph.com/news/here-s-how-chatgpt-4-spends-100-in-crypto-trading
- Freqtrade（GitHub）：https://github.com/freqtrade/freqtrade
- ai-hedge-fund（GitHub）：https://github.com/virattt/ai-hedge-fund
- TradingAgents 批判性复现：https://github.com/kantamaniprakash/trading-agents-lab
- TradingAgents 原项目：https://github.com/TauricResearch/TradingAgents
- $100→$19,527（CaptainAltcoin，营销案例）：https://captainaltcoin.com/chatgpt-powered-crypto-trading-strategy-turns-100-into-a-whopping-19527-heres-how/
- Milo $350→$1012（Medium，营销案例）：https://medium.com/towards-explainable-ai/this-crypto-ai-agent-turned-350-into-1012-72-in-a-week-heres-how-it-makes-decisions-1a12863fbf11
- 3Commas/FTX API 事件（Unchained）：https://unchainedcrypto.com/6m-users-funds-stolen-in-ftx-api-keys-phishing-attack/
- Lobstar Wilde 事件（CoinStats）：https://coinstats.app/news/2eece8516fbf7234f1443d65ecddd7a49706f05e92f7b5000684e4ed3307d664_AI-Trading-Bots-Catastrophic-Error-250K-Meme-Coin-Windfall-Accidentally-Sent-to-Online-Beggar/
- AI agent 安全事件汇总：https://github.com/mangrovetechnologies/mangrove-agent/blob/HEAD/docs/research/trading-bot-best-practices.md
- 274.6 ETH 骗局（CryptoCompass/TRM Labs）：https://cryptocompass.com/articles/fake-ai-trading-bot-tutorials-steal-274-6-eth-from-224-victims
- GitHub AI 交易项目调研：https://github.com/m1hawk/vibetrading/blob/HEAD/research/github-ai-trading-projects.md
