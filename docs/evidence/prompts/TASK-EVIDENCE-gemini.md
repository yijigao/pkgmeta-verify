# NLnet CodeSupply · 提案终审 8 项修正之证据采集（Gemini）

工作目录：~/workspace/nlnet-codesupply-council/pmv/
背景：Astra 对提案正文终审提出 8 项必须修改（ASTRA-PROPOSAL-FINAL-2026-10-13.md）。以下三项需要实际证据采集工作，verifier.py 保持冻结不改。

## 任务 A：三个补充案例的原始采集记录（对应终审第 3 项）
hatch-vcs@0.4.0、validfilepath@0.1、django-flowcontrol@0.0.21 目前只有说明文档。
要求：为每个案例保存**原始采集记录**（实际 API 响应原文、HTTP 状态/头、采集时间、endpoint），存为 `evidence/supplementary/` 下的 JSON 文件，附采集说明 `evidence/supplementary/README.md`（每个文件的来源、时间、内容说明）。
明确标注：补充证据，不在冻结的 12 文件 MANIFEST 基线内（基线为 5 个原始案例）。

## 任务 B：快照再分发索引（对应终审第 7 项）
检查 `evidence/snapshots/` 下每个快照文件，为每个写明：来源 endpoint、采集时间、来源许可/条款、署名要求、裁剪说明、再分发依据。
输出：`evidence/redistribution-index.md`。**拿不到的信息如实写"待办"**，不写"已具备"。

## 任务 C：接入示例（对应终审第 6 项）
写一个最小可运行的接入示例：输入记录 → PMV 输出 → 重查/复核处理流程。
输出：`examples/integration/`（代码＋README），用仓库内现有 PMV 代码演示，不要新造轮子。

## 输出要求
- 只做证据采集和示例，不改 verifier.py、不改测试、不改 MANIFEST（补充文件不进冻结清单）。
- 中文总结：每个任务完成情况、拿不到的部分如实说明。
