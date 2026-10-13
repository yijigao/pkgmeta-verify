# NLnet CodeSupply · PMV 原型任务（Gemini）：可运行的最小质检组件

## 背景
为 NLnet CodeSupply 提案提供**最关键的实测证据**：证明"带来源、时间和可复现证据的跨源差异判定与生命周期追踪"真实可行，且相较普通字段 diff 能避免误判。工作目录：~/workspace/nlnet-codesupply-council/pmv/（新建）。

## 交付清单（全部必须可运行、可复现）
1. **代码**：Python 3（只用标准库 + requests），模块划分：采集器 / 归一器 / 判定器 / 证据导出。Apache-2.0 许可头。
2. **双生态锁定**：npm + PyPI；每生态至少两个对照源：
   - npm：registry.npmjs.org（packument）+ deps.dev API v3
   - PyPI：PyPI JSON API（注明与 Simple 是同一注册表两个接口）+ deps.dev API v3
   - ClearlyDefined API 仅作许可证字段补充对照
3. **四类实测案例**：四类判定各至少一个**真实**案例（包名、版本、PURL 坐标、来源、抓取时间、快照、判定依据全部落盘）：
   - `REAL_ERROR`（真实错误：跨源字段矛盾且有证据指向一方错误）
   - `SYNC_DELAY`（同步延迟：抓取时间≠上游更新时间，保留不确定性，不得武断判错）
   - `SEMANTIC_DIVERGENCE`（语义差异：如许可证 AND/OR 表达不同，不得自动认定双方都对）
   - `INDETERMINATE`（无法判定：不可比输入输出 `undecidable`）
   构造测试单独标注 `synthetic=true`。
4. **判定规则硬约束**（终审意见原文落实）：
   - 哈希比较**只允许同一制品、同一算法**；跨算法/跨制品输入输出 `undecidable`（不报错退出，统一为判定值）。
   - 哈希不同只能先证"摘要冲突"，**不得断言镜像损坏/篡改**。
   - 抓取时间≠上游更新时间：疑似延迟保留不确定性（`SYNC_DELAY` 带置信度）。
   - 记录**来源依赖关系**：deps.dev 部分字段本身来自注册表，一致结果不得当作独立真值证明。
5. **证据包**：`evidence/` 目录含最小可再分发快照（原始 API 响应的脱敏子集）+ 规则版本文件（rules v0.1，版本化）+ SHA-256 清单。
6. **一次独立复跑**：提供 `rerun.sh`，按固定输入快照复跑并与首次结果逐字节比对（时间戳字段隔离），输出复跑报告 `rerun-report.md`（通过/失败 + diff 说明）。
7. **接入示例**：CLI 示例（`pkgmeta-verify check <purl>`）+ 输出 Schema（JSON Schema 文件）+ 聚合方接入说明（一段 README）。

## 输出要求
- 代码全部写进 pmv/ 目录并实际跑通；把运行日志、证据包、复跑报告全部落盘。
- 最后输出一份中文总结：跑了哪几个真实案例、每类判定的输入输出、相较普通字段 diff 避免了哪些误判、CodeSupply 聚合管线哪段流程能直接用这个组件。
- 不要写提案正文。技术负责人栏填 Joey（Jigao Yi）个人申请。
