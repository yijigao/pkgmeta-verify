**修改后通过：当前不可提交。必须修改以下 8 项。**

已完整读取全部 14 节、19,346 字节，审查版本为 [`ef1b3a7`](https://github.com/yijigao/pkgmeta-verify/blob/ef1b3a7/docs/evidence/PROPOSAL-DRAFT.md)。

1. **§7：“12/12 哈希通过”不符合当前提交。**  
   我对公开 Schema 原文计算的 SHA-256 为 `b5996ac4…924fceb`，清单仍是 `7a72b4df…4530b9`。必须更新清单，对最终提交重新复跑并归档结果；保留旧失败记录。复跑报告和生成脚本中残留的 `pmv.codesupply.org` 地址也须同步纠正。[清单](https://github.com/yijigao/pkgmeta-verify/blob/ef1b3a7/evidence/MANIFEST.sha256)、[现有失败日志](https://github.com/yijigao/pkgmeta-verify/blob/ef1b3a7/docs/evidence/rerun-full.log)

2. **§5、§14：hatch-vcs 的“官方确认解析器故障”必须撤回。**  
   官方回复仅表示怀疑与规范变化有关、会调查；ofek 只是追问进展。可写“仓库链接错误已有公开报告，具体解析机制尚未确认”，不能写官方已确认根因。附件还把 `0.4.0` 发布时间写成 **2023-12-11**，PyPI 实际是 **2023-11-06**；正文坐标应补全 `@0.4.0`。[官方回复](https://github.com/google/deps.dev/issues/220#issuecomment-2803737650)、[PyPI](https://pypi.org/project/hatch-vcs/0.4.0/)

3. **§5：“每个案例都有快照、结果和清单”不成立。**  
   冻结包只有原来的五组输入／输出，新增 hatch-vcs、validfilepath、django-flowcontrol 目前只有说明文档，未进入对应快照、结果和哈希清单。必须补原始采集记录与可复跑材料；拿不到就撤回相应的 **Proven** 和完整证据声明。validfilepath 历史 HTTP 响应不能靠 AI 报告中的摘录证明。另外，“字节一致”必须注明先隔离了 `evaluation_timestamp`。[证据目录](https://github.com/yijigao/pkgmeta-verify/tree/ef1b3a7/evidence)、[复跑方法](https://github.com/yijigao/pkgmeta-verify/blob/ef1b3a7/rerun-report.md)

4. **§6：把绝对实现保证改为概念验证的实际覆盖范围。**  
   草稿说置信度不会硬编码为 `1.0`、不会凭关键词断言，但当前代码仍有 `confidence: 1.0`，PSF 分支也可凭许可证标题及 “version 2” 通过。必须纠正文案并披露已知局限；顶端写“概念验证”不能抵消后文的具体错误声明。[相关代码](https://github.com/yijigao/pkgmeta-verify/blob/ef1b3a7/pmv/verifier.py#L346)、[硬编码置信度](https://github.com/yijigao/pkgmeta-verify/blob/ef1b3a7/pmv/verifier.py#L1097)

5. **§8、§13：纠正人工归属，并补齐 GenAI 日志。**  
   §8 的 `human-authored task specification` 与 §13“规格由 AI 编写、没有人工原稿”直接矛盾，必须改成真实归属。复跑应明确为“同一申请人 AI 团队内的非实现者复跑”。日志条目 14 所列 `ASTRA-REV3FIX3-2026-10-13.md`、`ASTRA-FINAL-2026-10-13.md` 未在公开输出目录中；条目 25 缺正文生成 prompt。须补齐这些材料、实际模型标识及本轮审稿记录，保留重建件标注。申请人尚未完成的核验／定稿不能写成已完成。[日志](https://github.com/yijigao/pkgmeta-verify/blob/ef1b3a7/PROMPT-LOG.md)、[v1.1 要求](https://nlnet.nl/foundation/policies/generativeAI/)

6. **§11：独特专长的证据链尚未成立。**  
   MEC、dsh 补丁支持相关工程能力，但当前材料没有清楚证明 **Jigao Yi 本人的具体技术贡献，以及这些贡献如何构成本题所需的独特专长**。必须补“本人贡献—具体技术判断—可核验证据”的对应关系，并明确 AI 的贡献；OKX 行所称脱敏代码、日志和复盘须给链接，否则删除。exceptional quality 的证据须随前四项纠正；欧洲受益方向成立，但“提交时提供”的接入示例必须实际补上。[履历索引](https://github.com/yijigao/pkgmeta-verify/blob/ef1b3a7/docs/evidence/CREDENTIALS-INDEX.md)、[例外条件](https://nlnet.nl/codesupply/eligibility/)

7. **§12：逐项再分发说明的完成声明不成立。**  
   现有快照有端点和时间，但未见所宣称的逐项来源条款、署名要求、裁剪说明及再分发依据。须补对应索引；未完成部分改为明确的待办，不能写成已经具备。[现有快照示例](https://github.com/yijigao/pkgmeta-verify/blob/ef1b3a7/evidence/snapshots/pkg-npm-esprima-4.0.1.json)

8. **§10：厘清 M3 的独立复跑与人工预算归属。**  
   M3 要求两名独立复跑者，但后文把独立验证也列为申请人自己的工时。必须说明复跑者与实现者的关系、参与安排及费用来源；申请人的预算工时应准确区分准备、协调、分析与第三方执行，避免把自测算作独立验收。

**金额和工时算术通过**：€6,000＋€5,000＋€2,500＋€1,500＝€15,000；€14,400÷€55＝261.82h；235.82h＋26h 储备一致。9 个月交付、12 个月内处理范围内返工没有直接矛盾。AboutCode 仅称“已发起沟通”的口径成立；截止时间也正确：**2026-11-03 12:00 CET／北京时间 19:00**。[沟通记录](https://github.com/aboutcode-org/purl-validator/issues/39)、[官方截止](https://nlnet.nl/codesupply/)