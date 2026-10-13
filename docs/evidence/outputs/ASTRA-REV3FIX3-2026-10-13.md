**1. 未通过——修复有效，但仍有新误判。**

按 `d5b5d5a` 校验源码后实跑：**56/56 测试通过、5/5 基线一致**；当前规则测试用于旧版 verifier 时 **18 项失败**。仍须修复并补回归：

| 必须修复 | 实际复现 |
|---|---|
| 制品身份证据仍接受无效内容 | 相同清单 `{"LICENSE":{"sha256":"a"*32}}` 中 SHA-256 长度错误，仍能证明身份并触发 `DIGEST_CONFLICT`；将 64 位十六进制**文件名**放入 `filename`、摘要留空也能通过。[代码](https://github.com/yijigao/pkgmeta-verify/blob/d5b5d5a/pmv/verifier.py#L267) |
| 算法别名覆盖冲突值 | A 同时提供 `sha256=a×64`、`SHA-256=b×64`，B 提供 `sha256=b×64`。仅交换 A 的键顺序，结果就在 `CONSISTENT` 与 `DIGEST_CONFLICT` 间变化。必须检测规范化后的键冲突。[代码](https://github.com/yijigao/pkgmeta-verify/blob/d5b5d5a/pmv/verifier.py#L643) |
| 无信息许可证仍判一致 | 三源均为 `NOASSERTION`，经过 normalizer 后仍判 `CONSISTENT`、置信度 **0.84**；该值明确表示未提供判断，不能算许可证证据。[代码](https://github.com/yijigao/pkgmeta-verify/blob/d5b5d5a/pmv/verifier.py#L80)、[SPDX 定义](https://spdx.github.io/spdx-spec/v2.3/package-information/#715-declared-license-field) |
| 无效时间被跳过后宣称已核验 | 两源许可证均 MIT，发布时间分别为 `"invalid"` 与合法时间，仍判 `CONSISTENT`，声称发布时间匹配，并获得时间证据加分。[代码](https://github.com/yijigao/pkgmeta-verify/blob/d5b5d5a/pmv/verifier.py#L1315) |
| 标题仍冒充标准许可证正文 | `text_snippet` 仅为 `PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2`，配合 PSF 分类器与下游 `non-standard`，即判 `REAL_ERROR`、置信度 **1.0**。没有授权、条件或免责正文。[代码](https://github.com/yijigao/pkgmeta-verify/blob/d5b5d5a/pmv/verifier.py#L346) |

另须删除缺少 ClearlyDefined 时审计轨迹仍称其“确认标准许可证”的[硬编码断言](https://github.com/yijigao/pkgmeta-verify/blob/d5b5d5a/pmv/verifier.py#L1092)，并纠正 README §7“[覆盖全部误判缺陷的 25 个测试](https://github.com/yijigao/pkgmeta-verify/blob/d5b5d5a/README.md#L166)”的过度承诺和旧计数。

**2. 通过。**

**3. 未通过——文件数量对，内容仍未补齐。**

- 实查 **13 个 prompt、20 个 output 均可访问**，但 [`pmv-fix3-gemini.txt`](https://github.com/yijigao/pkgmeta-verify/blob/d5b5d5a/docs/evidence/outputs/pmv-fix3-gemini.txt) **仍为 0 字节**，只有 19 个非空输出；与日志声称已补入 8,427 字节原文矛盾。
- [条目 14](https://github.com/yijigao/pkgmeta-verify/blob/d5b5d5a/PROMPT-LOG.md#L112)确实标了“主聊下达、无副本”，但五轮评审的 prompt 和具体时间仍缺失。标注缺失不能代替[官方要求的申请过程记录](https://nlnet.nl/foundation/policies/generativeAI/#application)。

**4. 未通过——公开披露草稿仍是旧稿。**

[公开正文 L9](https://github.com/yijigao/pkgmeta-verify/blob/d5b5d5a/docs/evidence/GENAI-DISCLOSURE-DRAFT.md#L9)仍声称“每个 AI 输出使用前均已核验”“最终提案由申请人写成并核验”。必须将本地已经改好的据实表述真正发布到仓库；目前两条声明均未删除。