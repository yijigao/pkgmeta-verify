# CodeSupply PMV 案例清单与证据状态总表 (Comprehensive Case Catalog & Verification Status)

最后更新时间: 2026-10-13  
版本规范: rules v0.1 / Draft 2020-12 Schema

---

## 1. 案例总览表 (Case Catalog)

| 案例 PURL | 判定类别 | 子状态码 | synthetic 属性 | 证据核验状态 | 核心依据与核验结论 |
|---|---|---|---|---|---|
| `pkg:pypi/typing-extensions@4.12.2` | `REAL_ERROR` | `STANDARDS_CONTRADICTION` | `false` (真实) | **部分成立** (责任已剥离，归因未证明) | 制品内为 PSF-2.0，PyPI 为分类器声明，ClearlyDefined 为 `Python-2.0.1`，deps.dev 标为 `non-standard`。已彻底删除 `DOWNSTREAM_PARSING_ERROR` 单边责任归咎，定性为跨标准语义脱节；未能封闭隔离单一字段错误与解析器故障。详见 `evidence/real-error-case.md`。 |
| `pkg:pypi/archgraph-layout@2.3.0` | `INDETERMINATE` | `undecidable` | `false` (真实) | **不成立** (维持 suspect / retracted) | 07:03:12Z 报告与 07:15:00Z 观察存在倒序矛盾，且缺少 07:15:00Z 原始 HTTP 抓包记录。按证据准则维持撤回与降级状态，严禁列为已证明延迟案例。详见 `evidence/delay-chain.md`。 |
| `pkg:pypi/validfilepath@0.1` | `SYNC_DELAY` | `DOWNSTREAM_INGESTION_LAG` | `false` (真实) | **成立** (全新重采干净案例) | 实时捕获 PyPI 09:59:55Z 发布、deps.dev 10:07:26Z (404 Not Found) 与 10:11:15Z (200 OK)。时间链严格单调向前递增，具备服务器原生 Date 标头与完整响应体。可证明延迟范围 `[450.1s, 679.1s]`。详见 `evidence/delay-chain.md`。 |
| `pkg:pypi/django-flowcontrol@0.0.21` | `INDETERMINATE` | `undecidable` | `false` (真实) | **成立** (真实自然不可判定案例) | 上游 PyPI `license: null`, `classifiers: []`；下游 deps.dev `licenses: []`；ClearlyDefined 无覆盖。多源许可证事实证据真空，触发 `CONSISTENCY_01_COMPARABLE_LICENSE`，输出置信度 0.0。证明“双源皆空”属于自然不可判定，非人工构造。详见 `evidence/natural-undecidable-case.md`。 |
| `pkg:npm/esprima@4.0.1` | `SEMANTIC_DIVERGENCE` | `LICENSE_EXPRESSION_CONJUNCTION_MISMATCH` | `false` (真实) | **成立** (已冻结基线) | npm 顶层声明 `BSD-2-Clause` vs ClearlyDefined 源码切面扫描确认为 `BSD-2-Clause AND BSD-3-Clause`，标识复合布尔语义差异。 |
| `pkg:npm/debug@4.3.4` | `INDETERMINATE` | `undecidable` | `true` (构造) | **成立** (已冻结基线) | 跨算法不可比性硬约束测试（SHA-1 vs SHA-256），避免普通 Diff 因算法不同产生报假警或崩溃。 |
| `pkg:npm/synthetic-fixture@1.0.0` | `DIGEST_CONFLICT` | `ARTIFACT_DIGEST_MISMATCH` | `true` (构造) | **成立** (已冻结基线) | 同一制品身份与同一算法下解码摘要冲突（`aaa...` vs `bbb...`），避免武断指控镜像被黑。 |

---

## 2. 提交前 5 关口之证据核验专项结论

1. **关口 1：真实错误案例最终确认 (`typing-extensions`)**
   - **结论**: **单边责任不成立（已撤销），区分“字段错误 vs 解析器故障”未证明**。
   - **产出证据**: `evidence/real-error-case.md`。

2. **关口 2：延迟时间链核验 (`archgraph-layout` / `validfilepath`)**
   - **结论**: `archgraph-layout` **不成立**（保持 suspect/retracted）；新采集 `validfilepath` **成立**（证明延迟区间 `[450.1s, 679.1s]`）。
   - **产出证据**: `evidence/delay-chain.md`。

3. **关口 3：自然不可判定案例 (`django-flowcontrol`)**
   - **结论**: **成立**（真实缺证、自然不可比，非构造）。
   - **产出证据**: `evidence/natural-undecidable-case.md`。
