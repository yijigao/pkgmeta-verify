# NLnet CodeSupply · rev3 大纲任务（Sol 6.1）：按 Astra rev2 终审 10 项 checklist

输入文件：
- rev2 大纲：~/workspace/nlnet-codesupply-council/outline-rev2-sol.txt
- rev2 终审全文：~/workspace/nlnet-codesupply-council/ASTRA-REV2-2026-10-13.md（第4节 10 项 checklist 为准）
- PMV 修复后证据：~/workspace/nlnet-codesupply-council/pmv/（新基线，rerun-report.md 已更新，0 错误）＋修复总结 ~/workspace/nlnet-codesupply-council/pmv-fix-gemini.txt
- PROMPT-LOG：~/workspace/nlnet-codesupply-council/PROMPT-LOG.md（已补 9 条）

## 10 项 checklist（逐项落实到大纲文字）

1. **真实错误证据**：typing-extensions 案例若 PMV 修复后仍不能证明原因，换案例或删除 DOWNSTREAM_PARSING_ERROR 责任断言；大纲只写已证明的结论。
2. **延迟时间链**：只写可证明的延迟范围；证据不足处写不可判定/疑似延迟。
3. **四类真实案例**：esprima 补字段和扫描范围；debug --cross-algo-test 明确标 synthetic；自然不可判定案例必须来自真实缺证。
4. **规则落实**：大纲中的判定规则必须与修复后的 verifier.py 一致（无发布时间→undecidable；空证据→undecidable；制品同一性需制品级证据；摘要比较仅同算法+记录归一化）。
5. **Schema 可用**：写明 Schema 已修正（小写类型、版本化 $id、全部实例校验通过）。
6. **独立复跑可归责**：大纲写明"提交前至少一名非实现者在干净环境复跑并记录身份/关系/commit/依赖/命令/原始日志"为提交前置动作；当前复跑记为自测。
7. **复跑程序**：rerun.sh 已改为实际检查、失败非零退出；大纲引用新基线。
8. **材料统一**：提案/README/结果/报告口径统一（案例分类、已完成状态）；快照附来源许可再分发说明。
9. **例外口论证完整**：分别写 exceptional quality（项目）、Jigao Yi 本人 unique technical expertise（履历三层：MEC 主证据＋dsh 补丁注明 fork＋OKX 辅助）、具体欧洲受益流程（CodeSupply 聚合管线哪段流程直接用）。
10. **提交口径收口**：明确已完成原型 vs 申请资助的后续工作；金额 €15,000、约 262h、9 个月交付、返修预留一致；申请人=负责人=MoU签署人=Jigao Yi；内部提交日 **11 月 2 日**（官方截止 11/3 12:00 CET＝北京时间 19:00）。

另：PR #228 已按终审更新（描述+评论+SKILL.md 同步）；大纲待拍板项更新为：对齐 issue 开启（目标 10/20 前，先 AboutCode 一个）、附件公开位置与维护人（PMV 公开仓库 docs/evidence/+evidence/，提交版本固定 commit+打 tag，维护人 Jigao Yi）、dsh 补丁具体 commit/diff/回归记录索引。

## 输出要求
中文输出 rev3 完整大纲（替代 rev2），只输出大纲不写提案正文。
技术负责人填 Joey（Jigao Yi）个人申请。末尾附"提交前 checklist 状态表"（10 项：已落实/待提交前完成）。
