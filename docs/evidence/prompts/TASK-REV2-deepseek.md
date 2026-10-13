# NLnet CodeSupply · rev2 大纲任务（DeepSeek）：按 Astra rev1 终审 8 项修改清单

输入文件：
- rev1 大纲：~/workspace/nlnet-codesupply-council/outline-rev1-deepseek.txt
- rev1 终审全文：~/workspace/nlnet-codesupply-council/ASTRA-REV1-2026-10-13.md
- PMV 证据：~/workspace/nlnet-codesupply-council/pmv/（代码+evidence/+rerun-report.md+Gemini 总结 pmv-gemini.txt）——**先读 PMV 实测结果，再写 rev2**；大纲中引用的每个实测案例必须与 pmv/evidence 落盘文件一致。

## 8 项修改清单（逐项落实，不得遗漏）

1. **四类真实样例**：提交前四类各至少一个实测案例（包名、版本、坐标、来源、时间、快照、判定依据），直接引用 PMV 证据包；构造测试单独标注 `synthetic=true`。
2. **竞品表去过度断言**：删除"CodeSupply 输出无 provenance""deps.dev 不接受外部校验""评分低说明数据陈旧"；承认 deps.dev 已有证明验证信息和问题反馈入口、ClearlyDefined 有原始采集记录及修订机制；差异精确限定为**跨源判定、时间追踪、离线复现能力**三项。
3. **判定规则修正**：哈希不同只能先证摘要冲突，不得断言镜像损坏/篡改；抓取时间≠上游更新时间，疑似延迟保留不确定性；许可证 AND/OR 不同不自动认定双方都对；不可比输出 `undecidable`，与跨算法规则统一。
4. **交付可计量**：正式数据集写明样本规模、覆盖字段、观察周期；离线复现包须含可再分发的最小证据快照+规则版本（不只是结果+SHA-256）；改名迁移只处理有明确证据的事件。
5. **预算口径修正**：€600 非人工费用先扣除，档 A 实为 **€14,400≈262h**（不是273h）；删除"按实际工时结算"，改为"**完成约定里程碑后申请付款**"；里程碑工时/FTE/返修预留全部按净额重算。
6. **双生态来源依赖**：npm registry＋deps.dev；PyPI＋deps.dev；ClearlyDefined 补许可证字段。注明 PyPI JSON 与 Simple 是同一注册表两个接口；deps.dev 部分字段也来自注册表，记录来源依赖关系；**删除"OSV 用于撤包/改名生命周期交叉核对"**（其 withdrawn 指漏洞记录撤回）。
7. **对齐 issue**：计划先向 AboutCode 最相关仓库开一个 issue（附 1–2 个 PMV 实测冲突、输出 Schema、具体接入问题）；ClearlyDefined 有独立问题再开。只写"已发起沟通"，不写"获认可"除非对方明确回复。
8. **履历（终审否决项，重点补）**：按以下顺序呈现——① Market Evidence Check 主证据（版本化规则、数据时效检查、结构化判定理由、固定快照测试、实际集成；陌生人安装验证附原始记录及验证范围；注明公开 PR（Anil-matcha/awesome-muse-connectors #228）描述需同步更新"尚未外部安装"为最新事实）；② dsh 定制补丁列第二（协议适配/工具消息归一/故障定位/回归验证，链接具体提交，注明仓库是 DeepSeek 项目 fork，不把整套 dsh 当原创）；③ OKX 扫描器作辅助证据（持续采集、故障恢复、日志追溯）。**明确写出：提交前优先补小型 PMV 原型＋四类实测证据包＋一次独立复跑**（本轮 PMV 即为此）。

## 输出要求
中文输出 rev2 完整大纲（替代 rev1），只输出大纲不写提案正文。
技术负责人填 Joey（Jigao Yi）个人申请。待拍板项单独成段（含：PR #228 描述同步更新、提交前对齐 issue 开启时机）。
