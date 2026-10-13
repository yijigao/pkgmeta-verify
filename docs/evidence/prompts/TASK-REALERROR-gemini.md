# NLnet CodeSupply · 关口 1 补救：找一个新的真实错误案例（Gemini）

工作目录：~/workspace/nlnet-codesupply-council/pmv/

背景：typing-extensions@4.12.2 的单边责任断言（DOWNSTREAM_PARSING_ERROR）已被证伪并删除。需要一个新的**真实错误案例**，要求：

1. **真实**：真实包、真实版本、真实来源数据，非构造。
2. **可证明**：能明确指出同一版本范围内**哪个字段错误**，并区分"字段错误"（Field Error）vs"解析器故障"（Parser Fault）vs"同步延迟"（Sync Delay）vs"语义差异"（Semantic Difference）。
3. **证据链完整**：对应版本制品的原始文件（如 LICENSE/sdist/wheel 元数据）、各来源的字段值、字段定义文档、判定依据链。每个主张都要有可引用的原始证据。
4. **生态**：npm 或 PyPI（项目锁定范围）。

方法建议：扫描 evidence/snapshots/ 中的现有快照，或用 PyPI JSON API / npm registry API 拉取真实数据，找许可证字段、发布时间、仓库链接、摘要等存在明确错误的案例。重点找"同一版本、跨源字段值冲突且其中一方可被原始制品证伪"的情形。

输出：`evidence/real-error-case-v2.md`（案例坐标＋证据链＋明确结论：成立/不成立）。不成立就继续找，最多尝试 3 个候选，每个都写清为什么不成立。

不改 verifier.py（已冻结）。中文总结。
