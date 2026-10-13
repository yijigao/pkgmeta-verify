# GenAI 使用日志（Prompt Provenance Log）— NLnet CodeSupply 提案准备

按官方 GenAI Policy（https://nlnet.nl/foundation/policies/generativeAI/）要求：任何 GenAI 使用（含 drafting/translation/summarisation）须声明并保留 prompt provenance log（model、日期、prompt、未编辑输出）。

## 条目 1 — 差异点分析＋提案大纲
- 日期：2026-10-13 13:31 CST
- 模型：DeepSeek（经 ~/workspace/tools/dsh-deepseek-valley.sh 调 dsh --profile headless）
- Prompt：~/workspace/nlnet-codesupply-council/TASK-A-deepseek.md（原文存档）
- 未编辑输出：~/workspace/nlnet-codesupply-council/taskA-deepseek.txt（DSH_EXIT=0，27,111 字节）
- 用途：资料整理与摘要（summarisation）+ 提案大纲结构建议。提案正文将人工主笔。

## 条目 2 — 最小样例 demo 设计方案
- 日期：2026-10-13 13:32 CST
- 模型：Gemini（dsh --profile gemini-sub，订阅版）
- Prompt：~/workspace/nlnet-codesupply-council/TASK-B-gemini.md（原文存档）
- 未编辑输出：~/workspace/nlnet-codesupply-council/taskB-gemini.txt（DSH_EXIT=0，21,033 字节）
- 用途：demo 技术设计建议。后续 PMV 原型代码实际由 Gemini（agent）按 TASK-PMV-gemini.md 实现（见条目 7），此处"人工/工程师实现"的原描述不准确，特此纠正。

## 条目 3 — 三席初审独立投票（专家会）
- 日期：2026-10-13 09:00–12:07 CST
- 模型：DeepSeek（谷时席 12:05 经 gate 调 dsh --profile headless；输出 deepseek-draft.txt，DSH_EXIT=0）、Gemini（dsh --profile gemini-sub；输出 gemini-draft.txt，DSH_EXIT=0）、Astra Max（gpt-6-astra，effort max，本机 codex；输出 astra-draft.txt，CODEX_EXIT=0）
- Prompt：~/workspace/nlnet-codesupply-council/TASK.md（原文存档）
- 未编辑输出：~/workspace/nlnet-codesupply-council/{deepseek,gemini,astra}-draft.txt
- 用途：选题评估（条件投/不投独立意见）。合成稿 ~/workspace/nlnet-codesupply-council/SYNTHESIS.md 由阿析（AI 代理，主聊侧）编写。

## 条目 4 — Astra 终审建议
- 日期：2026-10-13（主聊发起，本机读取）
- 模型：Astra Max（gpt-6-astra，reasoning effort max；主聊发起的终审咨询）
- Prompt：**重建件，非逐字节原件**——原文件（/tmp）已被清理，主聊 2026-10-13 从执行记录重建，内容与当时发给 Astra 的一致。重建原文：~/workspace/nlnet-codesupply-council/PROMPT-LOG-ENTRY4-RECONSTRUCTED.md（公开副本：docs/evidence/prompts/PROMPT-ENTRY4-RECONSTRUCTED.md）。
- 未编辑输出：~/workspace/nlnet-codesupply-council/ASTRA-ADJUDICATION-2026-10-13.md（全文存档，未编辑；公开副本：docs/evidence/outputs/ASTRA-ADJUDICATION-2026-10-13.md）
- 用途：终审建议（选题/金额/AI 合规三项"修改后通过"）。本轮大纲与 demo 修改即按此执行。

## 后续要求
- 提案正文须人工主笔；任何后续 AI 辅助（翻译、校对、摘要）继续追加本日志。
- 政策正在修订：建议等待新版发布后再投（公告不是强制停投令；"取消例外"指 GenAI 政策例外、非地域资格例外）。2026-11-03 提交前须复查政策页最新版并存档版本。
- 提交时打包：本日志＋所有引用的 prompt 原文＋未编辑输出（含评审可访问的副本，不能只给本机路径）。

## 条目 5 — 大纲修改（按 Astra 终审意见）
- 日期：2026-10-13 13:51 CST
- 模型：DeepSeek（谷时经 ~/workspace/tools/dsh-deepseek-valley.sh 调 dsh --profile headless）
- Prompt：~/workspace/nlnet-codesupply-council/TASK-A2-revise.md（原文存档）
- 未编辑输出：~/workspace/nlnet-codesupply-council/outline-rev1-deepseek.txt（DSH_EXIT=0）
- 用途：大纲修改（选题收窄为独立质检组件、竞品差异表、真实冲突样例设计、里程碑 M1–M4 新验收表、预算 €55/h≈273h 或 €60/h≈250h 二选一）。后续由阿析（AI 代理，主聊侧）代填负责人（Joey/Jigao Yi 个人申请，按主聊 13:53 指令）。

## 条目 6 — demo 设计修改（按 Astra 终审意见）
- 日期：2026-10-13 13:54 CST
- 模型：Gemini（dsh --profile gemini-sub，订阅版）
- Prompt：~/workspace/nlnet-codesupply-council/TASK-B2-revise.md（原文存档）
- 未编辑输出：~/workspace/nlnet-codesupply-council/demo-rev1-gemini.txt（DSH_EXIT=0）
- 用途：demo 设计修改（输入/输出/接入示例、四类冲突样例、同一制品同一算法哈希硬约束、npm+PyPI 双生态锁定）。后续由阿析（AI 代理，主聊侧）代填负责人（Joey/Jigao Yi 个人申请，按主聊 13:53 指令）。

## 条目 7 — PMV 原型实现（按 Astra rev1 终审 item 8）
- 日期：2026-10-13 14:12 CST（启动）
- 模型：Gemini（dsh --profile gemini-sub，订阅版）
- Prompt：~/workspace/nlnet-codesupply-council/TASK-PMV-gemini.md（原文存档）
- 未编辑输出：~/workspace/nlnet-codesupply-council/pmv-gemini.txt（DSH_EXIT=0，已完成）；代码落盘 ~/workspace/nlnet-codesupply-council/pmv/（含 evidence/、rerun-report.md）
- 用途：技术设计＋代码实现（小型 PMV 原型、四类实测证据包、一次独立复跑）。提案正文人工主笔。

## 条目 8 — rev2 大纲改由 Sol 6.1 执行（替代 DeepSeek 席）
- 日期：2026-10-13 14:28 CST（Joey 指令）；原排期 18:05，14:33 Joey 改为直接跑
- 模型：Sol 6.1（gpt-6.1-sol；本机 codex exec，--sandbox read-only；stdin 关闭）
- Prompt：~/workspace/nlnet-codesupply-council/TASK-REV2-deepseek.md（原文存档，复用）
- 未编辑输出：~/workspace/nlnet-codesupply-council/outline-rev2-sol.txt（直接跑，待完成）
- 用途：rev2 大纲（按 Astra rev1 终审 8 项清单）。原 DeepSeek 谷时跑席已按指令取消。提案正文人工主笔。

## 条目 9 — PMV bug 修复（按 Astra rev2 终审第4节）
- 日期：2026-10-13 14:47 CST（启动）
- 模型：Gemini（dsh --profile gemini-sub，订阅版）
- Prompt：~/workspace/nlnet-codesupply-council/TASK-PMV-FIX-gemini.md（原文存档）
- 未编辑输出：~/workspace/nlnet-codesupply-council/pmv-fix-gemini.txt（DSH_EXIT=0，已完成；"0 错误"口径后收窄为"现有测试零失败"，见条目 12）
- 用途：修复 verifier.py 判定规则、Schema 小写类型、synthetic 标注、typing-extensions 证据、延迟时间链、rerun.sh 实际检查、新基线冻结复跑。提案正文人工主笔。

## 条目 10 — rev3 大纲（按 Astra rev2 终审 10 项 checklist）
- 日期：2026-10-13 15:04 CST（启动）
- 模型：Sol 6.1（gpt-6.1-sol；本机 codex exec，--sandbox read-only；stdin 关闭）
- Prompt：~/workspace/nlnet-codesupply-council/TASK-REV3-sol.md（原文存档）
- 未编辑输出：~/workspace/nlnet-codesupply-council/outline-rev3-sol.txt（CODEX_EXIT=0，已完成）
- 用途：rev3 大纲（10 项 checklist 逐项落实）。提案正文人工主笔。

## 公开归档索引（提交材料用，评审可访问）
- 提交历史：f25484f（初版）→ 41d6a55 → c821170 → 27edf1f → 本轮推送后更新。索引以最新推送为准，旧提交号仅作历史记录。
- PMV 公开仓库：https://github.com/yijigao/pkgmeta-verify（commit f25484f，main 分支；含代码、evidence/ 快照与 MANIFEST.sha256、rerun-report.md、schemas/、docs/evidence/dsh-patches.md、PROMPT-LOG.md 本日志副本）
- AboutCode 对齐 issue：https://github.com/aboutcode-org/purl-validator/issues/39（2026-10-13 发起，只写"已发起技术对齐"，不写获认可）；archgraph-layout 案例纠正评论 https://github.com/aboutcode-org/purl-validator/issues/39#issuecomment-6140484558（降级为疑似延迟）
- PR #228（MEC 履历证据）：https://github.com/Anil-matcha/awesome-muse-connectors/pull/228（描述已按终审更新成熟度措辞＋评论留痕；SKILL.md 同步）
- 维护人：Jigao Yi（@yijigao）。提交版本固定 commit＋打 tag（提交前执行）。

## 条目 11 — PMV 第二轮 bug 修复（按 Astra rev3 终审第1节）
- 日期：2026-10-13 15:41 CST（完成）
- 模型：Gemini（dsh --profile gemini-sub，订阅版）
- Prompt：~/workspace/nlnet-codesupply-council/TASK-PMV-FIX2-gemini.md（原文存档）
- 未编辑输出：~/workspace/nlnet-codesupply-council/pmv-fix2-gemini.txt（DSH_EXIT=0）
- 用途：修复 5 个误判（制品身份关联、base64 解码比较、延迟三条件、许可证实际比较、删硬编码断言）＋25 项回归测试；archgraph-layout 降级 suspect/retracted；新基线冻结。口径统一为"现有测试零失败"。

## 条目 12 — PMV 第三轮 bug 修复（按 Astra rev3fix 第1节）
- 日期：2026-10-13 15:52 CST（启动）
- 模型：Gemini（dsh --profile gemini-sub，订阅版）
- Prompt：~/workspace/nlnet-codesupply-council/TASK-PMV-FIX3-gemini.md（原文存档）
- 未编辑输出：~/workspace/nlnet-codesupply-council/pmv-fix3-gemini.txt（待完成）
- 用途：修复 5 组新反例（制品身份文件名清单、摘要长度校验、延迟未来时间/容差表述、许可证实际比较、硬编码断言）＋README 口径收窄＋回归测试＋新基线冻结。口径统一为"现有测试零失败"。

## 条目 4 补记（已补入重建件）
- 2026-10-13 主聊提供重建件（非逐字节原件，已如实标注）。"完整日志"一项待本轮所有附件推送公开后关闭。

## 条目 13 — PMV 第三轮 bug 修复完成＋归档补齐（按 Astra rev3fix）
- 日期：2026-10-13 16:10 CST（完成）
- 模型：Gemini（dsh --profile gemini-sub，订阅版）
- Prompt：~/workspace/nlnet-codesupply-council/TASK-PMV-FIX3-gemini.md（原文存档）
- 未编辑输出：~/workspace/nlnet-codesupply-council/pmv-fix3-gemini.txt（DSH_EXIT=0；现有测试零失败）
- 用途：修复 5 组新反例（制品身份文件名清单排除、摘要长度校验、延迟未来时间拒绝＋容差阈值文档化、许可证实际比较＋置信度按证据、硬编码断言删除）＋README 口径收窄＋回归测试＋新基线冻结。
- 公开提交：https://github.com/yijigao/pkgmeta-verify @41d6a55（含附件：dsh-patches.md＋4 diff、披露草稿、条目4重建件）。**计数纠正**：此前写的"14 prompt、13 output"不符实际，且 pmv-fix3-gemini.txt（8,427 字节）当时未拷贝公开。实际应为 13 prompt、19 output，pmv-fix3-gemini.txt 已在本轮补入。

## 条目 14 — Astra 八轮终审（主聊侧发起；重建件已补入）
- 轮次：adjudication（13:46）、rev1（14:04）、rev2（14:40）、rev3（15:09）、rev3fix（15:41）、rev3fix2（16:10；首轮下达丢失，17:03 重派）、rev3fix3（17:33）、final（17:57），均为 2026-10-13 北京时间（时间精确到 5 分钟）
- 模型：Astra Max（gpt-6-astra，reasoning effort max；本机 codex 直连，主聊侧下达）
- Prompt：**重建件**——原件为 /tmp 下 heredoc 文件，已被系统清理；主聊侧（阿仁）根据执行记录重建，文字与下达时一致，但**非逐字节原件**。重建件：~/workspace/nlnet-codesupply-council/prompts-reconstructed/（00-README 说明＋01～08 八个文件，含时间、模型、输出文件对应关系）；公开副本：docs/evidence/prompts-reconstructed/。
- 未编辑输出：ASTRA-ADJUDICATION-2026-10-13.md、ASTRA-REV1-2026-10-13.md、ASTRA-REV2-2026-10-13.md、ASTRA-REV3-2026-10-13.md、ASTRA-REV3FIX-2026-10-13.md、ASTRA-REV3FIX2-2026-10-13.md、ASTRA-REV3FIX3-2026-10-13.md、ASTRA-FINAL-2026-10-13.md（全文存档，未编辑；公开副本：docs/evidence/outputs/）
- 用途：各轮终审结论与复核意见。
- **诚实声明**：prompt 为重建件已如实标注；输出为未编辑原件。

## 条目 15 — PMV 第四轮 bug 修复（按 Astra rev3fix2 第1节）
- 日期：2026-10-13 17:12 CST（启动）
- 模型：Gemini（dsh --profile gemini-sub，订阅版）
- Prompt：~/workspace/nlnet-codesupply-council/TASK-PMV-FIX4-gemini.md（原文存档）
- 未编辑输出：~/workspace/nlnet-codesupply-council/pmv-fix4-gemini.txt（待完成）
- 用途：修复 5 组新反例＋同类边界一次性扫荡（算法名规范化、摘要内容校验、真实时钟、HTTP 精确状态、许可证无信息值、自证输入降权）＋README/报告口径收窄＋回归测试＋新基线冻结。口径统一为"现有测试零失败"。

## 条目 16 — PMV 第四轮 bug 修复完成＋归档补齐（按 Astra rev3fix2）
- 日期：2026-10-13 17:33 CST（完成）
- 模型：Gemini（dsh --profile gemini-sub，订阅版）
- Prompt：~/workspace/nlnet-codesupply-council/TASK-PMV-FIX4-gemini.md（原文存档）
- 未编辑输出：~/workspace/nlnet-codesupply-council/pmv-fix4-gemini.txt（DSH_EXIT=0；现有测试零失败）
- 用途：修复 5 组新反例＋同类边界一次性扫荡＋README/报告口径收窄＋回归测试＋新基线冻结。
- 公开提交：https://github.com/yijigao/pkgmeta-verify @7fc8757（13 prompt、20 output，全部可访问；此前漏拷的 pmv-fix3-gemini.txt、TASK-PMV-FIX3-gemini.md、ASTRA-REV3FIX2-2026-10-13.md 已补齐）。

## 条目 17 — Joey 战略拍板（2026-10-13 17:57，主聊）
- 冻结规则集：verifier.py 当前版本冻结，不再追 Astra 新反例；5 组新误判不动。
- 公开口径统一收窄为"现有测试零失败（56/56），PMV 为概念验证"（README、rerun-report、提案大纲同步）。
- 火力转 5 项提交前关口：真实错误案例最终确认、延迟时间链核验、自然不可判定案例、Schema $id 落实、独立复跑＋材料统一＋履历索引；11/2 内部提交日前关闭。
- 提案正文（人工主笔）可开始，大纲 rev3 已过。

## 条目 18 — Astra 最终验收 4 项诚实修正（2026-10-13 18:05，主聊）
- 模型：孔明（dsh 执行岗）直接执行
- 修正 1：独立复跑记录拆分——尝试 1（53 tests FAILED，缺 jsonschema 依赖，环境问题）如实保留为 independent-tests-attempt1-failed.log；尝试 2（56/56 OK，2026-10-13T10:06:08Z–10:06:09Z）完整记录为 independent-tests-success.log。署名记录 INDEPENDENT-RERUN.md 重写，两次都保留。
- 修正 2：README L168"覆盖全部误判缺陷的 25 个回归测试用例"改为"56 项回归测试（现有测试零失败）；仅覆盖已发现的误判类别，PMV 为概念验证"。
- 修正 3：条目 14 五轮终审 prompt 缺件——待主聊重建件，收到后标注来源和不确定性补入。
- 修正 4：条目 3/5/6"阿析人工编写/代填"改为"阿析（AI 代理，主聊侧）"；披露草稿 L6"human-written technical specification"据实改写（TASK-PMV-gemini.md 为 AI 代理编写，无人类原稿）。

## 条目 19 — Schema $id 落实＋条目 14 重建件补入（2026-10-13 18:07，主聊）
- Schema $id：由占位 `https://pmv.codesupply.org/...` 改为版本化地址 `https://raw.githubusercontent.com/yijigao/pkgmeta-verify/<tag>/schemas/pmv-output/v0.1.json`（主聊 18:07 指令；Joey 未定域名前的推荐方案）。**注意**：`<tag>` 为占位符，提交前打 tag 时必须替换为实际 tag 名；替换后重跑 56 测试确认。
- $id 变更后本地 56/56 测试通过（test_schema 断言 `/schemas/pmv-output/` 子串，地址已按此调整）。
- 条目 14：主聊提供八轮终审 prompt 重建件（~/workspace/nlnet-codesupply-council/prompts-reconstructed/，01～08），如实标注"重建件、非逐字节原件"，公开副本已推送。
- 独立复跑：主聊已派烛龙（非实现者、干净环境）执行，结果回主聊侧统一归档；孔明此前的自跑仅作自检。

## 条目 20 — 阿仁独立复跑发现 MANIFEST 过期＋修复（2026-10-13 18:10，主聊）
- 阿仁（主聊侧，非实现者）干净环境复跑抓到真问题：6545bc4 改了 Schema $id，但 evidence/MANIFEST.sha256 未同步，rerun.sh Phase 1 报 `schemas/pmv-output.schema.json: FAILED`。
- 修复：已按当前 12 个文件重新生成 MANIFEST.sha256，`sha256sum -c` 12/12 OK；基线重新冻结。
- 阿仁的复跑记录原文归档：docs/evidence/INDEPENDENT-RERUN-AREN.md（**逐字归档，未改写其结论**，含"本次复跑不能作为全部检查通过的证据"）。
- **缺件**：记录中引用的 pytest-full.log、rerun-full.log 原始日志尚未收到，已向主聊索取；收到后补入归档。

## 条目 21 — 阿仁复跑原始日志补入（2026-10-13 18:11，主聊）
- pytest-full.log（8,048 字节：56 passed）、rerun-full.log（1,866 字节）已归档到 docs/evidence/。
- 4 项诚实问题全部闭环。

## 条目 22 — 提交前关口 1–3 证据核验完成（Gemini，2026-10-13 18:17）
- 模型：Gemini（dsh --profile gemini-sub）；Prompt：TASK-GATES-gemini.md；输出：gates-gemini.txt（DSH_EXIT=0）
- 关口 1（真实错误案例）：typing-extensions 单边责任断言**不成立**（已删除）；"字段错误 vs 解析器故障"区分未证明。需替换新案例。
- 关口 2（延迟时间链）：archgraph-layout 倒序矛盾无法消除，维持 suspect/retracted；**新采 validfilepath@0.1 成立**（完整时间链＋原始 HTTP 响应头＋可证明延迟范围）。
- 关口 3（自然不可判定）：**django-flowcontrol@0.0.21 成立**（真实缺证、INDETERMINATE、非构造）。
- 证据文件：evidence/real-error-case.md、delay-chain.md、natural-undecidable-case.md、cases.md；README §5 索引已更新。
- verifier.py 保持冻结未改；MANIFEST 12/12 仍有效。

## 条目 23 — 剩余三项开工（2026-10-13 19:30，主聊催进度）
- 新真实错误案例：Gemini 已派工（TASK-REALERROR-gemini.md），最多试 3 个候选。
- 材料统一：已核查——README/大纲/日志/披露草稿口径一致（56/56、PMV 概念验证、262h 未来人类预算）；大纲 L336 为历史修正记录，非过度承诺。
- 履历索引：新建 CREDENTIALS-INDEX.md（6 项：dsh 补丁、MEC、terramike、PR #228、purl#39、PMV），每项写明主张/证据/验证范围。
