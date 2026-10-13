# NLnet CodeSupply · PMV 第四轮 bug 修复（Gemini）：Astra 第二轮实核的 5 组新反例＋系统性边界扫荡

工作目录：~/workspace/nlnet-codesupply-council/pmv/
实核意见全文：~/workspace/nlnet-codesupply-council/ASTRA-REV3FIX2-2026-10-13.md（第1节表格为准）
当前公开实现：https://github.com/yijigao/pkgmeta-verify/blob/c821170/pmv/verifier.py

**核心要求（主聊原话）**：这是连续第二轮"修完旧的、找出新的"——**把同类边界一次性想全，别一轮一补**。每修一组反例，必须同时枚举该判定维度所有相邻的边界情况并一并处理，加进回归测试。

**口径**：只报告"现有测试零失败"，不得宣称判定正确。

## 5 组新反例（逐项修复＋同类边界扫荡）

### 1. 制品身份（verifier.py L182）
反例：相同清单 `{"LICENSE":{"sha256":""}}`（空 hash）仍被认作身份证据，判 DIGEST_CONFLICT；只检查键名/前缀不校验内容。
修复：身份证据必须含**有效内容**——非空 hash 且格式合法；空字符串、占位符、明显无效值一律不算证据。**同类扫荡**：枚举所有"有键无实值"的变体（null、""、"unknown"、"n/a"、全零 hash），全部 → `undecidable`（ARTIFACT_IDENTITY_UNPROVEN）。

### 2. 摘要长度（L545）
反例：算法键写成 "SHA-256"（大写）就绕过长度校验，hex:00/hex:01 又判 DIGEST_CONFLICT；未识别算法直接跳过长度约束。
修复：**算法名先规范化**（大小写/别名映射表：sha256/SHA-256/SHA256→同一算法；未知算法 → `undecidable` ENCODING_UNSUPPORTED，**不得跳过约束**）。长度校验对规范化后的算法强制执行。**同类扫荡**：所有算法别名写法、未知算法名、缺算法字段，全部有明确分支。

### 3. 延迟时间链（L728、L692）
反例：evaluation_timestamp 设 2100 年，2099 年观察就通过未来时间检查；HTTP 204 被接受还硬写成"200 已出现"。
修复：未来时间检查必须对照**真实当前时钟**（不得信任输入自带的 evaluation_timestamp）；HTTP 状态必须精确报告实际值（204 就是 204，不得改写为 200）；只有 2xx 且时间链完整才判延迟。**同类扫荡**：所有时间字段缺失/倒序/未来、所有非 200 的 2xx/3xx/4xx/5xx 状态码，逐类明确输出。

### 4. 许可证／一致性（L1042）
反例：两源许可证都是 `[" "]`（空白），normalizer 后仍判 CONSISTENT；三源发布时间差六年判一致置信度 0.96。
修复：空白/空值 normalize 后视同**无可比证据** → `undecidable`；CONSISTENT 仅在实际比较且一致时输出；**置信度必须按证据强度计算**，公式写进文档（证据项数、来源独立性、时间跨度惩罚），不得恒为 1.0 或拍脑袋。**同类扫荡**：空数组、null、空白字符串、"unknown"、"see license file" 等无信息值的全部情形。

### 5. 标准文本与硬编码（L210）
反例："This is not an MIT license. All rights reserved." 触发 REAL_ERROR 置信度 1.0；任意文本加 matches_standard=True 同样通过；缺 ClearlyDefined 还输出"确认了 None"。
修复：**关键词命中、自报标记不能作为核验证据**——标准文本判定必须有原文与标准文本的实质比对证据；matches_standard=True 这类自报字段只能作为输入声明，不得作为判定依据；缺数据源时不得输出"确认了 None"（改为"未覆盖"）。**同类扫荡**：所有"自证式输入"（self-attested flags）一律降权处理。

## 公开口径收窄
- README §4"严格落实各项硬约束"：改为与实际测试覆盖一致的表述（列出已覆盖的规则＋已知未覆盖项）。
- rerun-report.md 末句"100% 确定性与可复现性"：删除；改为"本次固定输入基线的复跑结果"，并注明改运行时钟判定可能变化。

## 回归与基线
- 每组至少 2 个回归测试（含原反例＋同类边界变体）。
- 修完后重新冻结基线（MANIFEST.sha256），修正后的 rerun.sh 完整重跑。
- 中文总结：每处修了什么、同类边界扫荡清单、测试结果；只报"现有测试零失败"。

不要写提案正文。技术负责人栏保持 Joey（Jigao Yi）个人申请。
