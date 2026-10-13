# 主张—证据—出现位置登记表（Claim Registry）

> 每条事实主张一个稳定 ID。结论强度分级：**已证明**（原始证据＋可复核）/ **已记录**（有来源，待补强）/ **候选**（单次观察）/ **未知**（缺证据）/ **已撤回**。
> 同一事实在摘要/正文/附件中的所有表述都受本表约束；修改一处必须核对所有出现位置。

## 测试与基线

| ID | 主张 | 原始来源 | 观察值/定位 | 适用范围 | 结论强度 | 出现位置 |
|---|---|---|---|---|---|---|
| CLM-001 | 现有测试零失败（56/56） | `tests/` 实跑 | 56 passed | 当前测试集 | 已证明 | README L6/L170/L172；PROPOSAL §5/§7/§14；rerun-report |
| CLM-002 | PMV 为概念验证 | Joey 2026-10-13 决策 | PROMPT-LOG 条目 17 | 全部公开口径 | 已证明（决策） | README L6；PROPOSAL §1/§5/§14 |
| CLM-021 | 冻结基线 12/12 哈希通过 | `evidence/MANIFEST.sha256` | sha256sum -c 12/12 | 5 个基线案例 | 已证明 | rerun-report；README；PROPOSAL §7 |

## 案例证据

| ID | 主张 | 原始来源 | 观察值/定位 | 适用范围 | 结论强度 | 出现位置 |
|---|---|---|---|---|---|---|
| CLM-003 | hatch-vcs SOURCE_REPO 链接字段错误 | PyPI METADATA（Funding vs Source）＋`git ls-remote` | sponsors/ofek 非 Git 仓库；真实仓库 github.com/ofek/hatch-vcs | hatch-vcs@0.4.0 | 已证明（字段错误） | real-error-case-v2.md；PROPOSAL §5/§14 |
| CLM-004 | deps.dev #220 官方回复内容 | https://github.com/google/deps.dev/issues/220#issuecomment-2803737650 | "怀疑与 PEP 753 规范变化有关，会调查" | 该 issue | 已证明 | real-error-case-v2.md L143 |
| CLM-005 | ofek 的跟进 | 同上 issue #220 | 询问处理进展 | 该 issue | 已记录 | real-error-case-v2.md |
| CLM-006 | hatch-vcs@0.4.0 上传时间 | PyPI JSON API | 2023-11-06T06:24:55Z | 该版本 | 已证明 | real-error-case-v2.md |
| CLM-007 | validfilepath 延迟观察 | 单次网络采集 2026-10-13 | 404→200，两次观察 | 该版本单次 | **候选**（历史同期原始记录缺失） | delay-chain.md；PROPOSAL §5/§14；evidence/cases.md L14/L29；README L121；evidence/supplementary/README.md L14 |
| CLM-008 | archgraph-layout 延迟 | 早期复跑报告 | 07:03 报告引用 07:15 观察（倒序） | 该版本 | **已撤回**（suspect/retracted） | delay-chain.md；PROPOSAL §5 |
| CLM-009 | django-flowcontrol 声明字段缺失 | PyPI JSON＋deps.dev API 实测 | info.license=null，licenses=[] | 声明字段 | 已记录（LICENSE 文件未核验） | natural-undecidable-case.md；PROPOSAL §5 |
| CLM-010 | typing-extensions 下游责任断言 | — | — | — | **已撤回** | real-error-case-v2.md（撤回记录）；PROPOSAL §5 |
| CLM-026 | typing-extensions FAQ 政策归因（已撤回） | — | "下游 FAQ 明确声明仅提取 License: 标头""双方均未违反自身规范" | — | **已撤回**（无官方原文支持） | real-error-case-v2.md L17–19（撤回记录） |
| CLM-027 | "老版本＋HTTP 200 排除延迟"规则（已撤回） | — | 四维表排除条件 | — | **已撤回** | real-error-case-v2.md（四维表，已删除） |

## 许可与数据事实

| ID | 主张 | 原始来源 | 观察值/定位 | 适用范围 | 结论强度 | 出现位置 |
|---|---|---|---|---|---|---|
| CLM-011 | ClearlyDefined 数据许可 | https://docs.clearlydefined.io/docs/resources/faq | "all the data is distributed under CC0" | ClearlyDefined 数据 | 已证明 | redistribution-index.md |
| CLM-012 | typing-extensions 三源 info.license | 快照文件实测 | 均为 null | 该快照 | 已证明 | redistribution-index.md；快照 JSON |

## 申请口径

| ID | 主张 | 原始来源 | 观察值/定位 | 适用范围 | 结论强度 | 出现位置 |
|---|---|---|---|---|---|---|
| CLM-013 | 预算 €15,000 / 约 262h | 大纲算术 | €14,400÷€55=261.82h | 本申请 | 已证明（算术） | PROPOSAL §10/§14 |
| CLM-014 | 里程碑 M1–M4 金额 | 同上 | 6000/5000/2500/1500 | 本申请 | 已证明（算术） | PROPOSAL §10 |
| CLM-015 | 申请人＝Jigao Yi，个人申请 | Joey 决策 | PROMPT-LOG | 本申请 | 已证明（决策） | PROPOSAL §1/§14 |
| CLM-016 | terramike 验证范围 | issue #8 评论 | muse.md＋OpenAPI，三项 smoke | 该验证 | 已记录 | CREDENTIALS-INDEX；PROPOSAL §11 |
| CLM-017 | dsh 补丁为申请人本人贡献 | diff＋回归记录 | 4 个 diff，SHA-256 | 补丁本身 | 已证明 | dsh-patches.md；CREDENTIALS-INDEX；PROPOSAL §11 |
| CLM-018 | purl-validator#39 已发起对齐 | GitHub issue | #39＋纠正评论 | 该 issue | 已记录 | PROPOSAL §12 |
| CLM-019 | 独立复跑（同团队非实现者） | 复跑记录 | 阿仁 56/56，署名记录 | 本次复跑 | 已记录 | INDEPENDENT-RERUN-AREN.md；PROPOSAL §8 |
| CLM-020 | Schema $id 版本化地址 | curl 验证 | HTTP 200 | v0.1 tag | 已证明 | schemas/；PROPOSAL §7 |
| CLM-022 | M3 第三方无偿参与 | 提案声明 | voluntary | M3 | 已记录（声明） | PROPOSAL §10 |
| CLM-023 | GenAI 政策 v1.1 | https://nlnet.nl/foundation/policies/generativeAI/ | 2026-01-26 生效 | 政策版本 | 已证明 | PROMPT-LOG 条目 25 |
| CLM-024 | 截止 2026-11-03 12:00 CET | https://nlnet.nl/codesupply/ | 北京时间 19:00 | 本申请 | 已证明 | PROPOSAL §1 |
| CLM-025 | 生态范围 npm＋PyPI | Joey 决策 | 大纲 | 本申请 | 已证明（决策） | PROPOSAL §4 |

| CLM-028 | PSF 分支标题触发局限 | `verifier.py` L346 实测 | 标题＋"version 2"即触发 | PMV 概念验证 | 已记录（已知局限） | README；rerun-report.md；PROPOSAL §6 |
| CLM-029 | 接入示例为重建演示 | pipeline_demo.py／audit_pipeline_run.json 标注 | 手工填写时间戳 | 演示，非实测证明 | 已记录（演示） | examples/integration/ |
| CLM-030 | real-error-case.md v1 已 superseded | 文件顶部标注 | "双方均未违反规范"归因已撤回 | 历史过程记录 | **已撤回**（被 v2 替代） | evidence/real-error-case.md；引用已改指 v2 |

## 状态机

`待修改 → 已修改待验收 → 已验收 → 已封版`

"已封版"条件：阻断问题全关；主张都有证据或明确未知状态；跨文件口径一致；提交包与验收版本相同。
