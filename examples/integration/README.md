# CodeSupply PMV 最小可运行接入示例 (Minimal Executable Integration Guide)

**对应终审要求**：对应提案终审第 6 项（实现最小可运行的接入示例：输入记录 → PMV 输出 → 重查/复核处理流程，复用仓库内现有 PMV 代码，不新造轮子）。

---

## 1. 架构概览与工作流

本示例演示了企业级软件供应链关口（如 CI/CD 准入门禁、企业私有仓库代理 Nexus/Artifactory 插件、或 SCA 安全扫描前置钩子）如何接入 CodeSupply PMV 验证引擎：

```
                    ┌────────────────────────────┐
                    │ 1. 输入记录 (Input Records)  │
                    │   - PURL 坐标 / 跨源元数据包   │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │ 2. PMV 核心验证 (Engine)    │
                    │   - pmv.normalizer         │
                    │   - pmv.verifier (规则集)   │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │ 3. 结构化判定 (PMV Output)  │
                    │   - 6 类判定类别 + 置信度    │
                    │   - 形式化审计链路 / 证据追踪│
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │ 4. 重查 / 复核分流处理流水线 │
                    └──────┬──────────┬──────────┘
                           │          │
        ┌──────────────────┼──────────┼───────────────────┐
        ▼                  ▼          ▼                   ▼
  [APPROVE]        [SCHEDULE_RECHECK] [COMPLIANCE_TRIAGE] [SECURITY_BLOCK]
  直接放行缓存     延迟重查队列       法务合规介入        立即隔离熔断
  (CONSISTENT)     (SYNC_DELAY)       (SEMANTIC_DIVERGENCE)(REAL_ERROR /
                                                           DIGEST_CONFLICT)
```

---

## 2. 判定类别与处置策略映射表

下游系统接入 PMV 时，依据 PMV 严格区分的 6 种状态码采取差异化处置，彻底避免传统工具将“延迟”或“语义差异”误判为“被投毒/被篡改”的报假警现象：

| PMV 判定类别 (`category`) | 语义解释与证据属性 | 下游门禁处置动作 (`Action`) | 处置说明与策略依据 |
|---|---|---|---|
| **`CONSISTENT`** | 跨数据源证据相互印证且一致 | **`APPROVE`** (直接放行) | 经形式化比对无冲突，放行进入生产构建通道或私服缓存。 |
| **`SYNC_DELAY`** | 证据链证明下游索引处于正常摄取时滞窗口内（<24h） | **`SCHEDULE_RECHECK`** (排期重查) | **核心价值：避免安全误报**。不发出篡改告警，而是将包压入延迟重试队列（指数退避：5m、15m、30m），待下游同步完成后自动复验放行。 |
| **`SEMANTIC_DIVERGENCE`** | 各来源表达存在合法维度视角差异（如顶层简写 vs 深入切面合取式） | **`COMPLIANCE_TRIAGE`** (法务分流) | 代码本身未被损坏，但存在许可范围差异。自动生成合规工单，附带 PMV 审计链，交由开源法务专员判定条款兼容性。 |
| **`REAL_ERROR`** | 客观事实冲突或下游解析机制错误（如非代码库被错误绑为源码仓库） | **`SECURITY_BLOCK`** (安全阻断) | 阻断构建流水线，隔离制品，向上游/下游生态提报事实性元数据缺陷。 |
| **`DIGEST_CONFLICT`** | 同一算法与同一制品坐标下哈希摘要直接冲突 | **`SECURITY_BLOCK`** (安全阻断+隔离) | 严重完整性告警：镜像或注册表存在篡改或供应链劫持风险，立即隔离制品并通知安全响应小组 (SecOps)。 |
| **`INDETERMINATE`** | 证据真空（如三方均无许可证）或跨算法不可比 | **`MANUAL_REVIEW`** (人工兜底) | 拒绝盲目判通过或不通过；挂起构建，提示审计员补充第三方源码深层扫描证据。 |

---

## 3. 代码实现与模块复用说明

示例脚本位于 [`pipeline_demo.py`](./pipeline_demo.py)，**完全复用仓库内既有 PMV 模块，未重复造轮子**：

- **`pmv.normalizer.Normalizer`**：复用既有清洗管道，将各数据源异构字段归一化为标准的中间数据表示；
- **`pmv.verifier.Verifier`**：复用既有验证器引擎，加载 `rules/rules-v0.1.json` 规则集执行可证明判定；
- **`pmv.collector.Collector`**：支持离线快照回放或实时抓取；
- **`IngestionGatePipeline`**：示例门禁类，展示输入接收、PMV 调用、分流决策、以及针对 `SYNC_DELAY` 的下游重查轮询循环（Re-check Loop）。

---

## 4. 快速运行与重现方法

在 `pmv/` 根目录下执行以下命令即可直接运行示例：

```bash
# 执行最小可运行接入示例
python3 examples/integration/pipeline_demo.py
```

### 运行输出预览
```text
================================================================================
CodeSupply PMV Integration Pipeline Example (Minimal Executable)
Started at: 2026-10-13T12:49:23.503239+00:00 (UTC)
================================================================================
Loaded 6 input package records for quality verification.

[1/6] Processing Ingestion: pkg:npm/example-clean@1.0.0
  PMV Verdict:    CONSISTENT (MUTUALLY_CONSISTENT)
  Confidence:     0.78
  Summary:        Package metadata is consistent across consulted sources
  --> Action:     [APPROVE]
  --> Policy:     Cross-source metadata strictly consistent. Fast-track approval for production deployment.
--------------------------------------------------------------------------------
[2/6] Processing Ingestion: pkg:npm/esprima@4.0.1
  PMV Verdict:    SEMANTIC_DIVERGENCE (LICENSE_EXPRESSION_CONJUNCTION_MISMATCH)
  Confidence:     0.95
  Summary:        Declared package license diverges from deeply discovered multi-license AND conjunction
  --> Action:     [COMPLIANCE_TRIAGE]
  --> Policy:     Semantic divergence in metadata representation. Route to Legal/Compliance for review.
--------------------------------------------------------------------------------
[3/6] Processing Ingestion: pkg:pypi/typing-extensions@4.12.2
  PMV Verdict:    REAL_ERROR (STANDARDS_CONTRADICTION)
  Confidence:     1.00
  Summary:        Downstream index license classification contradicts upstream and curated standards
  --> Action:     [SECURITY_BLOCK]
  --> Policy:     High-severity metadata conflict or digest mismatch. Ingestion blocked immediately.
  [QUARANTINE]    Artifact quarantined from build pipeline.
--------------------------------------------------------------------------------
[4/6] Processing Ingestion: pkg:npm/synthetic-fixture@1.0.0
  PMV Verdict:    DIGEST_CONFLICT (ARTIFACT_DIGEST_MISMATCH)
  Confidence:     1.00
  Summary:        Digest conflict observed between sources for identical artifact and algorithm
  --> Action:     [SECURITY_BLOCK]
  --> Policy:     High-severity metadata conflict or digest mismatch. Ingestion blocked immediately.
  [QUARANTINE]    Artifact quarantined from build pipeline.
--------------------------------------------------------------------------------
[5/6] Processing Ingestion: pkg:pypi/django-flowcontrol@0.0.21
  PMV Verdict:    INDETERMINATE (undecidable)
  Confidence:     0.00
  Summary:        Cannot determine consistency: no comparable license evidence across sources
  --> Action:     [MANUAL_REVIEW]
  --> Policy:     Metadata consistency is undecidable (missing evidence or incomparable data).
--------------------------------------------------------------------------------
[6/6] Processing Ingestion: pkg:pypi/validfilepath@0.1
  PMV Verdict:    SYNC_DELAY (DOWNSTREAM_INGESTION_LAG)
  Confidence:     0.98
  Summary:        Downstream index ingested release with verified temporal delay chain
  --> Action:     [SCHEDULE_RECHECK]
  --> Policy:     Downstream indexer ingestion lag detected within 24h normal window. Scheduled for re-check.
  [SCHEDULER]     Queued for retry in 300s...
  [RE-CHECK WORKFLOW] Polling downstream indexer for pkg:pypi/validfilepath@0.1...
  [RE-CHECK PASS] Post-delay outcome: [APPROVE] - Cross-source metadata strictly consistent. Fast-track approval for production deployment.
--------------------------------------------------------------------------------

Pipeline execution completed successfully.
Saved integration audit log to: examples/integration/audit_pipeline_run.json
================================================================================
```

---

## 5. 产出物说明

- **`pipeline_demo.py`**：最小可运行接入示例核心源代码；
- **`audit_pipeline_run.json`**：每次流水线执行后生成的结构化审计日志，包含输入 PURL、初始判定、处置动作、重查跟踪结果等，满足企业可追溯性合规要求。
