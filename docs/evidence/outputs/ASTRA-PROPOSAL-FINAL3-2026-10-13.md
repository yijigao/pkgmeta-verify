**必须改的清单（仅实质性；审查公开提交 `7187ef7`）。**

本轮已复核：56/56 测试通过，manifest 12/12 通过。但以下问题仍未修完：

1. **hatch-vcs 仍冒称官方确认根因。** [附件最终结论](https://github.com/yijigao/pkgmeta-verify/blob/7187ef7/evidence/real-error-case-v2.md#L204)仍写“官方承认为解析器提取缺陷”“Parser Fault: YES”；[官方回复](https://github.com/google/deps.dev/issues/220#issuecomment-2803737650)只有怀疑和调查承诺。必须同步撤回总结段的根因断言。

2. **延迟证据仍被写成已经证明。** [报告](https://github.com/yijigao/pkgmeta-verify/blob/7187ef7/evidence/delay-chain.md#L102)仍用两个样本宣称“通常 7–12 分钟”；[正文 §14](https://github.com/yijigao/pkgmeta-verify/blob/7187ef7/docs/evidence/PROPOSAL-DRAFT.md#L266)仍写完整时间链及原始 HTTP headers。必须与“同期原始记录缺失”的披露一致，撤回这些确定性结论。

3. **django-flowcontrol 仍被定性为无许可项目。** [附件结尾](https://github.com/yijigao/pkgmeta-verify/blob/7187ef7/evidence/natural-undecidable-case.md#L94)仍写“真实发布的无许可项目”。既然 LICENSE 尚未核验，只能认定所采声明字段缺失；必须删除整包无许可的结论。

4. **本人贡献归属仍有冲突。** [履历索引](https://github.com/yijigao/pkgmeta-verify/blob/7187ef7/docs/evidence/CREDENTIALS-INDEX.md#L12)仍把“编写 PMV 判定规则与证据契约”列为本人贡献，与正文披露的 AI 编写规格不一致。必须同步区分 Joey 的实际决策与 AI 起草成果。

5. **条目 26 补错了 prompt。** [日志](https://github.com/yijigao/pkgmeta-verify/blob/7187ef7/PROMPT-LOG.md#L194)记录的是“验收回来了”之后派给孔明的整改 handoff，且含省略占位，并非送入 Astra 的终审 prompt。必须补真实审查输入，并正确标注整改指令的归属；[官方政策](https://nlnet.nl/foundation/policies/generativeAI/)要求记录实际 prompts。

6. **接入示例修正没有生效。** [正式入口](https://github.com/yijigao/pkgmeta-verify/blob/7187ef7/examples/integration/pipeline_demo.py#L112)仍保留生产安全保证；修改落在重复目录，而且[新增分支](https://github.com/yijigao/pkgmeta-verify/blob/7187ef7/examples/integration/integration/pipeline_demo.py#L162)把 `STANDARDS_CONTRADICTION` 当成 `category`，实际它是 `subcode`。我实测两个版本都仍将 typing-extensions 送入 `SECURITY_BLOCK`。必须修正式入口，在通用 `REAL_ERROR` 分支前按 `subcode` 分流，并同步 README 和运行记录。