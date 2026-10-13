# 履历索引（Credentials Index）— Jigao Yi

> 用途：NLnet CodeSupply 申请 "unique technical expertise" 论证的证据索引。
> 口径：只写本人实际贡献与验证范围，不冒领、不推广。AI 贡献单独说明。

## 本人贡献—技术判断—可核验证据

| 本人贡献 | 技术判断 | 可核验证据 |
|---|---|---|
| 设计 Market Evidence Check 规则体系（版本化规则、时效判断、结构化理由、固定快照） | 聚合类证据必须从固定输入复现，不能依赖实时页面 | https://github.com/yijigao/market-evidence-check-devday（代码、规则、测试记录） |
| 定位 dsh 适配器三处故障并编写修复（工具结果协议错配、429 重试策略、Claude thinking 签名回放） | endpoint 级联回退会掩盖真实错误；加逐 endpoint 状态/body 日志暴露之 | docs/evidence/dsh-patches.md＋4 diff（SHA-256＋回归记录）；dsh 本体为 DeepSeek 项目，fork 仅承载本人补丁 |
| 设定 PMV 验证原则与验收纪律（缺证据→undecidable；"现有测试零失败（56/56），PMV 为概念验证"公开口径；规则集冻结；同团队复跑如实披露） | 诚实收窄比过度宣称更符合例外口要求；规则细节由 AI 按原则起草 | PROMPT-LOG.md 条目 17、25（2026-10-13 决策记录）；明细规格 TASK-PMV-gemini.md 由 AI 编写，非本人手写 |

## AI 贡献说明
- PMV 实现代码由 AI（Gemini）按任务书编写；大纲修订用过 DeepSeek/GPT-6.1-Sol/Astra Max；本草稿为 AI 辅助起草。
- 申请人主张的专长在于**规格设计、故障定位、验证设计**，不是逐行手写代码。

## 其他
- terramike 外部验证：muse.md＋OpenAPI 路径，三项 smoke checks；不推广为 CLI/目录安装验证或生产成熟度。[报告](https://github.com/terramike/xrpl-muse-skill/issues/8#issuecomment-6109879435)
- PR #228：描述/评论/SKILL.md 已按终审更新。[PR](https://github.com/Anil-matcha/awesome-muse-connectors/pull/228)
- purl-validator#39：已发起技术对齐，不主张获认可。[issue](https://github.com/aboutcode-org/purl-validator/issues/39)
- ~~OKX 扫描器~~：无公开链接可提供，已从提案 §11 论证中删除，不作为证据引用。

---
*维护人：Jigao Yi ｜ 更新：2026-10-13*
