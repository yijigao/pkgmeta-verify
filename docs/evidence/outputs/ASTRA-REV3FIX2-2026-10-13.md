**未全部通过，暂不能进入“提交前 5 项关口”。**

**1. 未通过——原反例已修，仍有同类误判。**

按公开提交 `c821170` 核对文件哈希后独立运行：**36/36 测试通过、12/12 清单匹配、5/5 基线复算一致**。当前测试用于修复前 `27edf1f` 时有 **10 项失败**，说明回归测试有效，但遗漏以下反例：

| 修复组 | 实际复现的剩余问题 |
|---|---|
| 制品身份 | 相同清单 `{"LICENSE":{"sha256":""}}` 没有有效 hash，仍被认作身份证据，两个不同摘要被判 `DIGEST_CONFLICT`。只检查键名或前缀，不校验内容。[代码](https://github.com/yijigao/pkgmeta-verify/blob/c821170/pmv/verifier.py#L182) |
| 摘要长度 | `sha256` 已拦住短摘要；但算法键改为 `SHA-256`，`hex:00`／`hex:01` 又被判 `DIGEST_CONFLICT`。未识别算法直接跳过长度约束。[代码](https://github.com/yijigao/pkgmeta-verify/blob/c821170/pmv/verifier.py#L545) |
| 延迟时间链 | 输入增加 `evaluation_timestamp=2100年`，即可让 **2099 年观察**通过未来时间检查。另，HTTP **204** 也被接受，并在结论中硬写成 **200 已出现**。[时间检查](https://github.com/yijigao/pkgmeta-verify/blob/c821170/pmv/verifier.py#L728)、[状态检查](https://github.com/yijigao/pkgmeta-verify/blob/c821170/pmv/verifier.py#L692) |
| 许可证／一致性 | 两源许可证均为 `[" "]`，经过 normalizer 后仍判 `CONSISTENT`。三个源前两者发布时间一致、第三者相差六年，也判一致，置信度 **0.96**。[代码](https://github.com/yijigao/pkgmeta-verify/blob/c821170/pmv/verifier.py#L1042) |
| 标准文本与硬编码 | 文本 **“This is not an MIT license. All rights reserved.”** 仍触发 `REAL_ERROR`、置信度 **1.0**；任意文本加 `matches_standard=True` 同样通过。缺少 ClearlyDefined 时还输出其“确认了 None”。关键词命中、自报标记不能作为标准文本已核验证据。[代码](https://github.com/yijigao/pkgmeta-verify/blob/c821170/pmv/verifier.py#L210) |

上述反例必须补入回归并修复。

公开口径仍须修：README L12 已收窄，但[§4“严格落实各项硬约束”](https://github.com/yijigao/pkgmeta-verify/blob/c821170/README.md#L67)与上述结果矛盾；[复跑报告末句](https://github.com/yijigao/pkgmeta-verify/blob/c821170/rerun-report.md#L95)仍宣称“100% 确定性与可复现性”。实测固定输入、仅改变运行时钟，判定会从 `INDETERMINATE` 变成 `SYNC_DELAY`，不能由五个基线推广此结论。

**2. 通过——延迟案例纠正保持落实。**

[公开纠正评论](https://github.com/aboutcode-org/purl-validator/issues/39#issuecomment-6140484558)可访问；快照保留 `suspect/retracted`，本次复算仍为 `INDETERMINATE`。

**3. 未通过——旧缺件补了，本轮归档仍不完整。**

原四个缺件及 REV1–REV3FIX 输出均实际可访问；条目 4 已明确标注“重建件，非逐字节原件”，这一点通过。但必须补齐、纠正：

- **FIX3 prompt 未公开；`pmv-fix3-gemini.txt` 是 0 字节空文件**，条目 13 却写完成并归档。[归档目录](https://github.com/yijigao/pkgmeta-verify/tree/c821170/docs/evidence)
- REV1–REV3FIX 只有评审输出，缺对应 prompt 和日志条目。
- 索引仍同时写 `41d6a55`、`f25484f`；“14 prompt、13 output”也不符实际：**11 个 prompt、18 个 output，其中一个为空**。[索引及条目13](https://github.com/yijigao/pkgmeta-verify/blob/c821170/PROMPT-LOG.md#L80)

官方申请阶段要求保留模型、日期时间、prompt、未经编辑输出；空文件和仅有评审结论不能补足这些记录。[GenAI 政策](https://nlnet.nl/foundation/policies/generativeAI/)

**4. 未通过——两条不成立的完成声明根本没删。**

[披露正文 L9](https://github.com/yijigao/pkgmeta-verify/blob/c821170/docs/evidence/GENAI-DISCLOSURE-DRAFT.md#L9)仍声称：

- 每个 AI 输出使用前都已对照一手来源检查；
- 最终提案已由申请人写成并核验。

现有证据不能支持，且与 L15“成立前不要如此声称”的备注直接冲突，必须据实改写。使用原因已并入英文正文、**262h 已明确为未来人类工作预算**，这两处通过。