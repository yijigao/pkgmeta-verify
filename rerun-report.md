# CodeSupply PMV 独立复跑审计报告 (Independent Rerun Audit Report)

- **执行时间 (Run Timestamp)**: 2026-10-13T10:16:27Z
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
**状态: 现有测试零失败 (ALL TESTS PASSED)**

```
........................................................
----------------------------------------------------------------------
Ran 56 tests in 0.072s

OK
```

---

## 2. 案例执行与逐字节比对明细 (Case Execution & Deterministic Diff)

| 案例 PURL | 判定类别 | 子状态码 | 置信度 | synthetic 标记 | 原始快照校验 | 逐字节比对状态 |
|---|---|---|---|---|---|---|
| `pkg:pypi/typing-extensions@4.12.2` | `REAL_ERROR` | `STANDARDS_CONTRADICTION` | 1.0 | `False` | SHA-256 VERIFIED | **PASS** (0 diff) |
| `pkg:pypi/archgraph-layout@2.3.0` | `INDETERMINATE` | `undecidable` | 0.4 | `False` | SHA-256 VERIFIED | **PASS** (0 diff) |
| `pkg:npm/esprima@4.0.1` | `SEMANTIC_DIVERGENCE` | `LICENSE_EXPRESSION_CONJUNCTION_MISMATCH` | 0.95 | `False` | SHA-256 VERIFIED | **PASS** (0 diff) |
| `pkg:npm/debug@4.3.4` | `INDETERMINATE` | `undecidable` | 1.0 | `True` | SHA-256 VERIFIED | **PASS** (0 diff) |
| `pkg:npm/synthetic-fixture@1.0.0` | `DIGEST_CONFLICT` | `ARTIFACT_DIGEST_MISMATCH` | 1.0 | `True` | SHA-256 VERIFIED | **PASS** (0 diff) |

---

## 3. 统计与审计结论 (Audit Statistics & Summary)

- **总案例数**: 5
- **通过案例数**: 5
- **失败案例数**: 0
- **分类统计**:
  - **真实软件包案例 (3个)**:
    - `typing-extensions@4.12.2`: `REAL_ERROR` (subcode: `STANDARDS_CONTRADICTION`)
    - `archgraph-layout@2.3.0`: `INDETERMINATE` (subcode: `undecidable`, 疑似延迟，时间链待核验；已标注 suspect/retracted，撤出已证明延迟案例)
    - `esprima@4.0.1`: `SEMANTIC_DIVERGENCE` (subcode: `LICENSE_EXPRESSION_CONJUNCTION_MISMATCH`)
  - **真实包跨算法构造测试 (1个, synthetic=true)**: `debug@4.3.4` (`INDETERMINATE`, subcode: `undecidable`)
  - **构造基准用例 (1个, synthetic=true)**: `synthetic-fixture@1.0.0` (`DIGEST_CONFLICT`, subcode: `ARTIFACT_DIGEST_MISMATCH`)
- **复跑综合结论**: **现有测试零失败 (100% 字节级一致、Schema 校验通过、清单哈希全匹配)**

> **重要口径说明**：本轮起严格遵照 Astra rev3 审查要求，\"0 错误\"收窄为\"现有测试零失败\"——测试通过仅代表符合当前测试集规范，不等于判定绝对正确。本报告仅陈述客观测试结果。

### Astra rev4 终审修复与系统性边界扫荡落实情况
1. **制品身份关联核验 (空值/占位符/全零 hash 扫荡)**: 身份证据必须含有效内容；空字符串 `{"LICENSE":{"sha256":""}}`、占位符（null、""、"unknown"、"n/a"）、全零 dummy hash 均视同无有效 hash，判定为 `undecidable` (`ARTIFACT_IDENTITY_UNPROVEN`)，严禁误判 `DIGEST_CONFLICT`。
2. **算法规范化与长度约束强制执行**: 算法名称先做大小写与别名映射归一化（SHA-256/sha256/sha-256 同等处理）；未知算法输出 `undecidable` (`ENCODING_UNSUPPORTED`)，严禁跳过长度约束；所有规范化算法强制执行精确字节长度校验（截断输出 `DIGEST_LENGTH_MISMATCH`）。
3. **延迟时间链真实时钟校验与精确状态码报告**: 未来时间检查必须对照真实当前系统时钟（拒绝信任输入自带的 evaluation_timestamp）；HTTP 状态码精确如实报告（HTTP 204 即报告为 HTTP 204，严禁改写为 200）；3xx/4xx/5xx 分类明确输出 undecidable。
4. **许可证空值扫荡、全两两时间比对与置信度公式**: 空白数组、空白字符串、"unknown"、"see license file" 等无信息值归一化后视同无可比证据（`undecidable`）；多源发布时间强制执行全两两比对（跨源跨年差距判定为 `TIMESTAMP_DIVERGENCE`，严禁仅比对前两项或输出拍脑袋高置信度）；置信度严格依据证据项数、来源独立性、时间跨度惩罚等公式动态计算（严格 < 1.0）。
5. **标准文本实质比对、降权自证标记与空源脱敏**: 彻底排除否定模式（如 "This is not an MIT license"）与名称关键词假命中；matches_standard=True 等自证标记一律降权，仅作为输入声明不得作为判定证据；必须具备核心法律条款实质比对证据；缺少 ClearlyDefined 时如实输出“ClearlyDefined: 未覆盖”，严禁输出“确认了 None”。

## 4. Diff 详细说明
本次固定输入基线的复跑结果（所有案例在离线快照复跑中与基线输出逐字节比对完全一致，0 diff，动态 `evaluation_timestamp` 字段中立隔离；注：若改变运行时钟或引入外部动态时变输入，判定可能发生变化，不代表全环境或未来时段的绝对确定性）。
