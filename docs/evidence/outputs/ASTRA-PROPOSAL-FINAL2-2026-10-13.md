**必须改的清单（审查 `565c70e`）：**

1. **hatch-vcs 的根因断言仍未撤回。** [附件](https://github.com/yijigao/pkgmeta-verify/blob/565c70e/evidence/real-error-case-v2.md#L139)仍写“官方确认”“贪婪或首个匹配”“解析器故障成立”。[官方回复](https://github.com/google/deps.dev/issues/220#issuecomment-2803737650)仅表示怀疑并调查。正文、附件必须统一为“链接错误成立，具体机制未确认”。

2. **validfilepath 的历史时间链仍缺同期原始记录。** 新 raw 能核实的是后来 HTTP 200；历史 404→200 仍靠报告摘录。[延迟报告](https://github.com/yijigao/pkgmeta-verify/blob/565c70e/evidence/delay-chain.md#L95)却继续声称“可证明区间”“100% 封闭完整”，并用两个样本推出“通常 7–12 分钟”。补同期记录；拿不到就撤回这些确定性声明，正文 §14 同步修改。

3. **django-flowcontrol 被过度定性为无许可证项目。** [raw](https://github.com/yijigao/pkgmeta-verify/blob/565c70e/evidence/supplementary/pkg-pypi-django-flowcontrol-0.0.21.raw.json)实际含 `license_files: ["LICENSE"]`。[报告](https://github.com/yijigao/pkgmeta-verify/blob/565c70e/evidence/natural-undecidable-case.md#L24)只能证明所采声明字段缺失，不能推出整包无许可、零授权。收窄表述并披露尚未核验 LICENSE 文件。

4. **§11 仍与 AI 归属披露冲突。** [贡献表及其后文](https://github.com/yijigao/pkgmeta-verify/blob/565c70e/docs/evidence/PROPOSAL-DRAFT.md#L205)把 PMV 规格列为申请人本人贡献、称“申请人的任务书”；§8/§13 却明确任务书由 AI 编写、没有人工原稿。必须区分 Joey 实际提出的技术判断与 AI 设计，并给对应记录。

5. **GenAI 日志仍未闭环。** [条目25](https://github.com/yijigao/pkgmeta-verify/blob/565c70e/PROMPT-LOG.md#L185)把已修改为 21,521 字节的正文称作“未编辑输出”；应固定指向 [19,346 字节初稿](https://github.com/yijigao/pkgmeta-verify/blob/82b1fbc/docs/evidence/PROPOSAL-DRAFT.md)。条目26还缺上一轮提案终审的 prompt，不能仅补输出文件就称日志完整。

6. **再分发索引包含明确事实错误。** [索引](https://github.com/yijigao/pkgmeta-verify/blob/565c70e/evidence/redistribution-index.md)把 ClearlyDefined 数据许可写成 CC-BY-4.0，[官方实际为 CC0](https://docs.clearlydefined.io/docs/resources/faq)。还将 typing-extensions 快照的 `info.license` 写成 `PSF-2.0`，实际为 `null`。按实际字段和官方条款修正；§12 同步披露尚未完成的事项。

7. **M3 费用来源仍重复占用。** [§10](https://github.com/yijigao/pkgmeta-verify/blob/565c70e/docs/evidence/PROPOSAL-DRAFT.md#L157)说第三方执行由 €2,500 覆盖，但该金额已全部分配为申请人 €2,400 工时及 €100 环境费。明确第三方无偿参与，或单列其劳务费并扣减申请人工时。

8. **接入示例重新引入过度保证和误报。** [代码](https://github.com/yijigao/pkgmeta-verify/blob/565c70e/examples/integration/pipeline_demo.py#L112)把元数据一致直接解释为生产部署安全；实跑又将已撤回错误归责的 typing-extensions 送入 `SECURITY_BLOCK`。删除安全保证，将 `STANDARDS_CONTRADICTION` 分流人工复核，并撤回 README“彻底避免误报”的声明。