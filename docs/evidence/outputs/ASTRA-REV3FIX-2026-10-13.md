**1. 未通过——旧反例已修，但仍有误判和硬编码断言。**

按 `27edf1f` 校验源码后独立运行：**25/25 测试通过、12/12 清单匹配、5/5 基线复算一致**。将当前规则测试用于修复前的 verifier，有 **12 项失败**，说明回归测试确实有效，但覆盖不足。

| 修复点 | 实核结果与剩余问题 |
|---|---|
| 制品身份关联 | 已增加门槛，能拦住原反例；但两个不同来源仅提供相同的 `["README","LICENSE"]` 文件名清单，仍被认作身份已证明，判 `DIGEST_CONFLICT`。[代码](https://github.com/yijigao/pkgmeta-verify/blob/27edf1f/pmv/verifier.py#L128) |
| Base64 解码 | 按字节比较、不支持编码拒绝均落实；但缺少摘要长度校验，SHA-256 输入 `hex:00`、`hex:01` 仍判摘要冲突。现有 Base64 测试甚至用 **5 字节数据冒充 SHA-256**。[代码](https://github.com/yijigao/pkgmeta-verify/blob/27edf1f/pmv/verifier.py#L159)、[测试](https://github.com/yijigao/pkgmeta-verify/blob/27edf1f/tests/test_verifier_rules.py#L266) |
| 延迟三条件 | 原来的 404、缺时间、倒序反例已拦住；但将后续观察写成 **2099 年**仍判已证明延迟；42 天延迟也会声称“在 86400 秒容差内”。[代码](https://github.com/yijigao/pkgmeta-verify/blob/27edf1f/pmv/verifier.py#L537) |
| 许可证比较 | MIT／Apache-2.0 已正确识别；但 **MIT／non-standard**，以及双方均无许可证、仅有不同发布时间，仍判 `CONSISTENT`、置信度 1.0。[代码](https://github.com/yijigao/pkgmeta-verify/blob/27edf1f/pmv/verifier.py#L694) |
| 删除硬编码事实 | **未完成。** 任意非空 `text_snippet` 即可触发“已验证标准许可证”；仍硬写“缺少 PEP 639 License-Expression”。输入 OR 表达式也被描述成 AND 双重义务。[代码](https://github.com/yijigao/pkgmeta-verify/blob/27edf1f/pmv/verifier.py#L607) |

公开口径也未完全收窄：[README](https://github.com/yijigao/pkgmeta-verify/blob/27edf1f/README.md#L12) 仍写“彻底避免普通字段比对的误判”。

**2. 通过——延迟案例纠正确实落实。**

[纠正评论](https://github.com/aboutcode-org/purl-validator/issues/39#issuecomment-6140484558)存在，明确指出 **07:03:12 报告引用 07:15 后续观察**的矛盾，降级为疑似延迟，没有编造解释。公开快照已加 `suspect/retracted`，结果为 `INDETERMINATE`；与旧版比较，原快照字段保持不变，仅新增两个状态标记。[快照](https://github.com/yijigao/pkgmeta-verify/blob/27edf1f/evidence/snapshots/pkg-pypi-archgraph-layout-2.3.0.json)

**3. 未通过——文件已公开，但归档没有补齐。**

`dsh-patches.md`、4 个 diff、10 个 prompt、9 个 output、披露草稿均可访问；**4 个补丁 SHA-256 全部匹配，改动内容与索引相符**。[归档目录](https://github.com/yijigao/pkgmeta-verify/tree/27edf1f/docs/evidence)

但 [PROMPT-LOG.md](https://github.com/yijigao/pkgmeta-verify/blob/27edf1f/PROMPT-LOG.md) 引用的下列输出仍未公开：`taskA-deepseek.txt`、`taskB-gemini.txt`、`pmv-fix2-gemini.txt`、`ASTRA-ADJUDICATION-2026-10-13.md`；条目 4 的 prompt 原文也明确缺失。索引还指向旧提交 `f25484f`。因此“完整公开归档”不能验收。

**4. 未通过——披露草稿存在，但有不成立的完成声明。**

[草稿](https://github.com/yijigao/pkgmeta-verify/blob/27edf1f/docs/evidence/GENAI-DISCLOSURE-DRAFT.md)包含模型用途、原因、日志链接及 262h 人类工作说明；但“完整日志已归档”与上述缺件直接矛盾，“全部输出已独立核验”“最终申请已由申请人写成”也不能由现有证据确认。应据实改写；使用原因目前仅在中文备注，需并入英文申请正文。

262h 可保留为**未来人类工作预算**，不能用代理评审或自动复跑代替人类贡献证明。官方要求披露使用及原因、保存模型／时间／prompt／未编辑输出，并排除纯 AI 生成成果直接请款。[申请 FAQ](https://nlnet.nl/codesupply/faq/)、[GenAI 政策](https://nlnet.nl/foundation/policies/generativeAI/)

**当前不能终审放行。** 11/2 内部提交前应关闭上述缺口；官方截止确为 **2026-11-03 12:00 CET／北京时间 19:00**，提交前还须复查正在修订的 GenAI 政策。[官方公告](https://nlnet.nl/news/2026/20260903-call.html)