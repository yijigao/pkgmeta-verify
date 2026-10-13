# NLnet CodeSupply · PMV bug 修复任务（Gemini）：Astra rev2 终审发现的真 bug

工作目录：~/workspace/nlnet-codesupply-council/pmv/
终审意见全文：~/workspace/nlnet-codesupply-council/ASTRA-REV2-2026-10-13.md（第4节 checklist 为准）

背景：Astra 同机只读复算确认 5/5 规范化一致、12/12 哈希匹配，但发现以下必须修的 bug。修完后**重新冻结基线并完整复跑**。

## 必须修复的 bug（逐项）

### 1. verifier.py 判定规则（当前问题见 pmv/pmv/verifier.py:184 附近）
- **无发布时间仍判延迟**：缺少上游发布时间字段时，不得输出 SYNC_DELAY，必须输出 `undecidable`（或带低置信度的疑似延迟，明确标注不确定性）。
- **空证据默认一致**：证据为空/缺失时不得返回 `CONSISTENT`，必须返回 `undecidable`。
- **仅凭文件名认定同一制品**：制品同一性必须有制品级证据（digest、下载 URL、包内文件清单其一），仅文件名相同不得认定为同一制品。
- **摘要统一 .lower()**：hex digest 比较前统一大小写是允许的，但必须**记录原始值与归一化动作**，且仅限同一算法；跨算法输入输出 `undecidable`（已实现则保留并加测试）。
- 为以上每项加**针对性回归测试**（能捕获该误判的用例）。

### 2. Schema 真正可用（pmv/schemas/pmv-output.schema.json）
- `OBJECT/STRING/ARRAY` 等改为合法小写类型（object/string/array）。
- `$id` 改为项目控制的版本化地址（形如 https://<项目域名>/schemas/pmv-output/v0.1.json；域名未定先用占位并在 README 注明待定）。
- Schema 自检通过，且**全部结果实例**用修正后的 Schema 校验通过。

### 3. synthetic 标注
- `debug --cross-algo-test` 的比较输入明确标 `synthetic=true`，与另一构造 fixture 分开统计；检查所有输出中 synthetic 标记与输入一致。

### 4. 真实错误证据（typing-extensions 案例）
- 若不能证明同一范围内哪个字段错误、且不能区分字段错误 vs 解析器故障原因，则**删除 `DOWNSTREAM_PARSING_ERROR` 及其责任断言**，或换一个能证明的案例。证据要求：对应版本制品的许可证原文、来源字段定义。

### 5. 延迟时间链（archgraph-layout 案例）
- 保存发布时间、下游缺失观察、后续出现观察三段证据；只报告**可证明的延迟范围**；只有一次 404 或缺少时间证据时输出不可判定/疑似延迟。

### 6. rerun.sh 实际检查
- 当前 rerun.sh 直接写死 `SHA-256 MATCH` 且含固定归因文字。改为：**实际校验**快照、规则、Schema、代码版本及结果，逐项检查生成报告；**失败时非零退出**。
- 修完后**冻结新基线**（更新 MANIFEST.sha256），用新 rerun.sh 完整重跑并生成新 rerun-report.md。

### 7. esprima 案例补字段
- 补清判定所用字段和扫描范围（哪些源、哪些字段参与了判定）。

## 输出要求
- 所有修复落盘、可运行；新基线冻结后完整复跑通过。
- 最后输出中文总结：修了哪几处、每处改了什么、回归测试结果、新基线复跑结果。
- 不要写提案正文。技术负责人栏保持 Joey（Jigao Yi）个人申请。
