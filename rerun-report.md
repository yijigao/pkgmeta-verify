# CodeSupply PMV 独立复跑审计报告 (Independent Rerun Audit Report)

- **执行时间 (Run Timestamp)**: 2026-10-13T07:03:12Z
- **执行环境 (Environment)**: Linux 7.0.0-39-generic / Python 3.12.3
- **技术负责人 (Technical Lead)**: Joey (Jigao Yi) 个人申请
- **规则集版本 (Ruleset Version)**: `rules v0.1` (`rules/rules-v0.1.json`)
- **输出规范 (Output Schema)**: `schemas/pmv-output.schema.json` (Draft 2020-12, $id: `https://pmv.codesupply.org/schemas/pmv-output/v0.1.json`)
- **复跑模式 (Mode)**: 完全脱网离线快照复跑 (`--offline`)，固定输入源于 `evidence/snapshots/`
- **时间戳隔离策略 (Timestamp Isolation)**: 仅对运行时字段 `evaluation_timestamp` 进行中立隔离，其余全部结构、证据字段与推导理由执行逐字节比对

---

## 1. 密码学与规范性校验 (Integrity & Schema Verification)

### 1.1 MANIFEST.sha256 离线哈希清单校验结果
**状态: 全部 12/12 文件哈希比对一致 (VERIFIED)**

```
../rules/rules-v0.1.json: OK
../schemas/pmv-output.schema.json: OK
results/pkg-npm-debug-4.3.4.result.json: OK
results/pkg-npm-esprima-4.0.1.result.json: OK
results/pkg-npm-synthetic-fixture-1.0.0.result.json: OK
results/pkg-pypi-archgraph-layout-2.3.0.result.json: OK
results/pkg-pypi-typing-extensions-4.12.2.result.json: OK
snapshots/pkg-npm-debug-4.3.4.json: OK
snapshots/pkg-npm-esprima-4.0.1.json: OK
snapshots/pkg-npm-synthetic-fixture-1.0.0.json: OK
snapshots/pkg-pypi-archgraph-layout-2.3.0.json: OK
snapshots/pkg-pypi-typing-extensions-4.12.2.json: OK
```

### 1.2 JSON Schema 规范性校验结果
**状态: Schema 自检及全部结果实例校验 100% 通过 (VALID Draft 2020-12)**

```
SCHEMA_SELF_CHECK: PASS (Valid Draft 2020-12)
BASELINE_VALIDATE [pkg-npm-debug-4.3.4.result.json]: PASS
BASELINE_VALIDATE [pkg-npm-esprima-4.0.1.result.json]: PASS
BASELINE_VALIDATE [pkg-npm-synthetic-fixture-1.0.0.result.json]: PASS
BASELINE_VALIDATE [pkg-pypi-archgraph-layout-2.3.0.result.json]: PASS
BASELINE_VALIDATE [pkg-pypi-typing-extensions-4.12.2.result.json]: PASS
```

### 1.3 规则回归测试用例 (Targeted Regression Test Suite)
**状态: 规则测试用例全部通过 (ALL PASS)**

```
..............
----------------------------------------------------------------------
Ran 14 tests in 0.058s

OK
```

---

## 2. 案例执行与逐字节比对明细 (Case Execution & Deterministic Diff)

| 案例 PURL | 判定类别 | 子状态码 | 置信度 | synthetic 标记 | 原始快照校验 | 逐字节比对状态 |
|---|---|---|---|---|---|---|
| `pkg:pypi/typing-extensions@4.12.2` | `REAL_ERROR` | `STANDARDS_CONTRADICTION` | 1.0 | `False` | SHA-256 VERIFIED | **PASS** (0 diff) |
| `pkg:pypi/archgraph-layout@2.3.0` | `SYNC_DELAY` | `DOWNSTREAM_INGESTION_LAG` | 0.978 | `False` | SHA-256 VERIFIED | **PASS** (0 diff) |
| `pkg:npm/esprima@4.0.1` | `SEMANTIC_DIVERGENCE` | `LICENSE_EXPRESSION_CONJUNCTION_MISMATCH` | 0.95 | `False` | SHA-256 VERIFIED | **PASS** (0 diff) |
| `pkg:npm/debug@4.3.4` | `INDETERMINATE` | `undecidable` | 1.0 | `True` | SHA-256 VERIFIED | **PASS** (0 diff) |
| `pkg:npm/synthetic-fixture@1.0.0` | `DIGEST_CONFLICT` | `ARTIFACT_DIGEST_MISMATCH` | 1.0 | `True` | SHA-256 VERIFIED | **PASS** (0 diff) |

---

## 3. 统计与审计结论 (Audit Statistics & Summary)

- **总案例数**: 5
- **通过案例数**: 5
- **失败案例数**: 0
- **分类统计**:
  - **真实软件包案例 (3个)**: `typing-extensions@4.12.2` (`REAL_ERROR`), `archgraph-layout@2.3.0` (`SYNC_DELAY`), `esprima@4.0.1` (`SEMANTIC_DIVERGENCE`)
  - **真实包跨算法构造测试 (1个, synthetic=true)**: `debug@4.3.4` (`INDETERMINATE`, subcode: `undecidable`)
  - **构造基准用例 (1个, synthetic=true)**: `synthetic-fixture@1.0.0` (`DIGEST_CONFLICT`, subcode: `ARTIFACT_DIGEST_MISMATCH`)
- **复跑综合结论**: **ALL PASSED (100% 字节级一致、Schema 校验通过、清单哈希全匹配)**

### 终审修复规则落实情况
1. **真实错误责任断言剥离**: 在 `pkg:pypi/typing-extensions@4.12.2` 中，记录了制品内标准 PSF 许可证原文及 PyPI 分类器事实，删除了未证明原因的 `DOWNSTREAM_PARSING_ERROR` 及其单边责任归咎，客观判定为 `STANDARDS_CONTRADICTION`。
2. **完整延迟时间链与范围计算**: 在 `pkg:pypi/archgraph-layout@2.3.0` 中，基于上游发布时间、下游 404 缺失观察及后续 200 出现观察建立完整三段链，输出可证明的延迟范围，避免了单次 404 或无发布时间时的误判。
3. **语义差异多源与扫描范围补全**: 在 `pkg:npm/esprima@4.0.1` 中，完整补清了 npm registry 顶层声明与 ClearlyDefined 仓库核心切面文件级扫描的字段差异与扫描范围。
4. **哈希比较硬约束与归一化审计**: 跨算法输入严格判定为 `undecidable`；hex digest 比较在同一算法下记录大小写/空格归一化动作与原始值；制品同一性强制核验制品级证据（摘要、URL、文件清单），杜绝仅凭文件名武断认定。
5. **空证据严禁默认一致**: 证据为空或不足时严格输出 `undecidable`，杜绝空数据误判为 `CONSISTENT`。

## 4. Diff 详细说明
所有案例在离线快照复跑中与基线输出逐字节比对完全一致（0 diff，动态 `evaluation_timestamp` 字段中立隔离），证明 PMV 判定逻辑具备 100% 确定性与可复现性。
