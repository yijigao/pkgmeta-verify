# NLnet CodeSupply · PMV 第二轮 bug 修复（Gemini）：Astra rev3 终审复现的 5 个误判

工作目录：~/workspace/nlnet-codesupply-council/pmv/
终审意见全文：~/workspace/nlnet-codesupply-council/ASTRA-REV3-2026-10-13.md（第1节表格为准）
当前公开实现：https://github.com/yijigao/pkgmeta-verify/blob/f387dd1/pmv/verifier.py

**重要口径**：本轮起，"0 错误"收窄为"现有测试零失败"——测试通过≠判定正确。不要再宣称判定正确性，只报告测试结果。

## 5 个必须修复的误判（逐项，补回归测试）

1. **同名文件、不同摘要、无证据绑定到同一制品 → 现在判 DIGEST_CONFLICT**
   改为：必须验证制品身份关联（digest 绑定到同一下载 URL / 同一包内文件清单 / 同一制品发布记录其一）；仅"两边都有摘要"不足 → 输出 `undecidable`（子码 `ARTIFACT_IDENTITY_UNPROVEN`），不得判 DIGEST_CONFLICT。

2. **两个 base64 摘要仅大小写不同 → 现在转小写判匹配**
   改为：按编码**解码后比较字节**；若编码未知/不支持，明确输出 `undecidable`（子码 `ENCODING_UNSUPPORTED`）并记录原因。禁止静默 `.lower()` 后判匹配。

3. **后续观察仍 404、缺时间、时间倒序 → 现在判 SYNC_DELAY**
   改为：必须同时满足——后续观察 HTTP 成功状态、发布时间字段有效、观察时间顺序正确（t_observed_after > t_observed_before > t_published）；任一不满足 → `undecidable`（疑似延迟，标注不确定性）。

4. **两源许可证 MIT vs Apache-2.0，或一源无可比字段 → 现在判 CONSISTENT**
   改为：实际进行字段比较；MIT vs Apache-2.0 是**明确不一致**（判 SEMANTIC_DIVERGENCE 或 REAL_ERROR，按规则）；一源缺少可比字段 → `undecidable`。禁止"无比较就判一致"。

5. **未提供制品 LICENSE 原文 → 现在判 REAL_ERROR 且硬编码"制品包含 PSF 许可证"**
   改为：删除一切硬编码事实断言；无对应证据 → 不得判 REAL_ERROR（输出 `undecidable` 并注明缺证据）。

## archgraph-layout 延迟案例降级
- 该案例公开口径已降级为"**疑似延迟，时间链待核验**"（issue #39 已发纠正评论）。
- 在证据中给该案例加 `verification_status: "suspect"` 标记；rerun-report 和结果中不再将其列为"已证明的延迟"。
- 若原始 HTTP 响应/采集日志无法解释 07:03:12Z 报告引用 07:15:00Z 观察的时间倒序，则从"已证明案例"中撤下（保留原快照做审计记录，标注 retracted）。

## 回归与基线
- 为以上 5 项各加至少一个回归测试（tests/），用例必须能复现原误判输入。
- 修完后重新冻结基线（更新 MANIFEST.sha256），用修正后的 rerun.sh 完整重跑并生成新 rerun-report.md。
- 报告措辞统一用"现有测试零失败"，不得写"判定正确/0 错误"。

## 输出要求
- 全部落盘、可运行；最后中文总结：每处修了什么、回归测试结果、新基线复跑结果。
- 不要写提案正文。技术负责人栏保持 Joey（Jigao Yi）个人申请。
