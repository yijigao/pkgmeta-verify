# NLnet CodeSupply · PMV 第三轮 bug 修复（Gemini）：Astra 实核复现的新反例

工作目录：~/workspace/nlnet-codesupply-council/pmv/
实核意见全文：~/workspace/nlnet-codesupply-council/ASTRA-REV3FIX-2026-10-13.md（第1节表格为准）
当前公开实现：https://github.com/yijigao/pkgmeta-verify/blob/27edf1f/pmv/verifier.py

**口径**：只报告"现有测试零失败"，不得宣称判定正确。

## 5 组新反例（逐项修复＋回归测试）

1. **制品身份关联（verifier.py L128）**：两个不同来源仅提供相同的 `["README","LICENSE"]` 文件名清单，仍被认作身份已证明判 DIGEST_CONFLICT。
   改为：文件名清单**不得**作为制品身份证据；身份关联必须有 digest→同一制品发布记录、或同一下载 URL、或包内文件清单含 hash 其一；否则 `undecidable`（`ARTIFACT_IDENTITY_UNPROVEN`）。

2. **摘要长度校验（L159，测试 L266）**：SHA-256 输入 `hex:00`、`hex:01` 仍判摘要冲突；现有 Base64 测试用 5 字节数据冒充 SHA-256。
   改为：增加摘要长度校验——声明算法 SHA-256 则解码后必须为 32 字节，否则 `undecidable`（`DIGEST_LENGTH_MISMATCH`）；修正冒充测试用例为真实长度向量。

3. **延迟三条件（L537）**：后续观察写 2099 年仍判已证明延迟；42 天延迟声称"在 86400 秒容差内"。
   改为：后续观察时间必须 ≤ 当前时间（拒绝未来时间）；延迟容差必须有明确定义的阈值常量并在文档中说明，超出容差不得称"在容差内"；42 天延迟如实报告为 42 天，不得压缩表述。

4. **许可证比较（L694）**：MIT／non-standard、双方均无许可证仅发布时间不同，仍判 CONSISTENT 置信度 1.0。
   改为：MIT vs non-standard → 不一致（SEMANTIC_DIVERGENCE 或 REAL_ERROR）；双方均无许可证 → 无可比证据 → `undecidable`；CONSISTENT 仅在实际比较且一致时输出，置信度按证据强度计算，不得恒为 1.0。

5. **硬编码事实断言（L607，未完成）**：
   - 任意非空 `text_snippet` 触发"已验证标准许可证" → 改为：必须有许可证原文与标准文本的匹配证据，否则不得断言。
   - 删除"缺少 PEP 639 License-Expression"硬编码表述。
   - OR 表达式不得描述成 AND 双重义务；按 SPDX 语义如实描述。

## 公开口径收窄
- README L12"彻底避免普通字段比对的误判"：删除或收窄为"减少特定类别的误判（以回归测试为准）"。

## 回归与基线
- 每项至少一个回归测试（能复现上述反例输入）。
- 修完后重新冻结基线（MANIFEST.sha256），修正后的 rerun.sh 完整重跑。
- 总结用中文：每处修了什么、测试结果、基线复跑结果；只报"现有测试零失败"。

不要写提案正文。技术负责人栏保持 Joey（Jigao Yi）个人申请。
