# 真实自然不可判定案例证据报告 (Naturally Undecidable Real Case Verification Report)

- **评估对象 (Target Package)**: `pkg:pypi/django-flowcontrol@0.0.21`
- **属性 (Attributes)**: `synthetic: false`（真实软件包、真实网络抓取、非人工构造）
- **核验关口**: 提交前 5 关口之 3 · 自然不可判定案例
- **判定结果 (Verdict)**: **`INDETERMINATE`** (Subcode: `undecidable`, Confidence: `0.0`)
- **核验结论**: **成立（完全符合真实缺证与自然不可比标准，非构造）**

---

## 1. 案例坐标与基本信息

- **包名 (Package Name)**: `django-flowcontrol`
- **版本 (Version)**: `0.0.21`
- **Ecosystem**: `pypi`
- **PURL**: `pkg:pypi/django-flowcontrol@0.0.21`
- **上游端点**: `https://pypi.org/pypi/django-flowcontrol/0.0.21/json`
- **下游索引**: `https://api.deps.dev/v3/systems/pypi/packages/django-flowcontrol/versions/0.0.21`

---

## 2. 原始证据与缺失证据核验 (Raw Evidence & Missing Evidence)

### 2.1 上游 PyPI 注册表核心元数据
调用 `https://pypi.org/pypi/django-flowcontrol/0.0.21/json` 实测返回：
- `info.license`: `null` (None)
- `info.license_expression`: `null`
- `info.classifiers`: 包含编程语言与框架，但**完全不包含**任何 License 相关的 Trove Classifiers（`[]`）。
- **缺失证据**: 上游发布者在打包清单（`pyproject.toml` / `setup.py` / `PKG-INFO`）中完全未声明开源许可证。

### 2.2 衍生索引 deps.dev API v3
调用 `https://api.deps.dev/v3/systems/pypi/packages/django-flowcontrol/versions/0.0.21` 实测返回：
```json
{
  "versionKey": {
    "system": "PYPI",
    "name": "django-flowcontrol",
    "version": "0.0.21"
  },
  "publishedAt": "2026-10-13T09:57:53Z",
  "licenses": []
}
```
- **缺失证据**: `licenses` 字段为空数组 `[]`，下游解析引擎在摄取时未发现任何可提取的许可证标识。

### 2.3 辅助分析源 ClearlyDefined
- 该包该版本在 ClearlyDefined 中无收录记录或无有效许可切面（Status 404 / Empty）。

---

## 3. 为什么不可比 (Why Undecidable / Incomparable)

在元数据验证的形式化规则体系中，本案例触发 PMV 硬约束规则 **`CONSISTENCY_01_COMPARABLE_LICENSE`**：

1. **证据真空（Evidence Vacuum）**:
   各对照源均未提供任何实质性的许可证声明（全部表现为空值 `null`、空数组 `[]` 或缺失标头）。
2. **逻辑非等价（Null Is Not Equality）**:
   在传统的非类型化比较中，工具可能会因 `upstream.license == downstream.license == null` 计算出 `True`，进而得出“双源一致（CONSISTENT）”的荒谬结论。但在安全与合规审计的形式化定义中：
   $$\text{Evidence}(\text{Source}_A) = \emptyset \land \text{Evidence}(\text{Source}_B) = \emptyset \implies \text{Consistency is Undecidable}$$
   “双源皆空”代表的是**证据的完全缺失（Missing Evidence）**，绝不等于**元数据已被核验一致（Verified Consistency）**。
3. **不可判定裁决**:
   当没有任何实质性事实可供交叉对比时，该案例在法律属性上属于典型的**自然不可判定（Naturally Undecidable）**。系统拒绝盲目采信或输出高置信度，严格输出 `category: INDETERMINATE`，子码为 `undecidable`，置信度强制赋 `0.0`。

---

## 4. 实际审计追踪 (Decision Audit Trail)

通过 PMV 验证引擎对该真实快照执行质检，完整输出如下：

```json
{
  "category": "INDETERMINATE",
  "subcode": "undecidable",
  "confidence": 0.0,
  "summary": "Cannot determine consistency: no comparable license evidence across sources",
  "details": "None of the available sources provide verifiable license declarations (found only empty arrays, whitespace, or placeholder values such as 'unknown' or 'see license file'). Lacking comparable license evidence, metadata consistency is undecidable. Enforcing hard constraint: absent license evidence strictly yields 'undecidable', NEVER defaults to CONSISTENT.",
  "avoided_false_positive": "Avoided false-positive CONSISTENT verdict when sources lack substantive license declarations entirely."
}
```

```json
[
  {
    "condition_evaluated": "has_comparable_license_declarations(sources)",
    "outcome": "NO_COMPARABLE_LICENSE_EVIDENCE",
    "rationale": "Neither source provides a substantive license declaration (all empty, missing, or placeholder values). Without comparable license evidence, metadata consistency cannot be determined.",
    "rule_id": "CONSISTENCY_01_COMPARABLE_LICENSE"
  }
]
```

---

## 5. 相较普通 Diff 避免的误判 (Avoided False Positive)

- **避免传统比较工具的虚假安全感**:
  传统 Diff 比较 `null == null` 判定一致并给出绿灯，导致企业合规系统放行没有任何授权保护的闭源或侵权风险代码；
- **真实性保障**:
  该案例为 PyPI 真实发布的无许可项目（非人工构造的 cross-algorithm 桩），直接证明了 PMV 针对真实生态“证据真空”现象具备严密的不确定性捕捉能力。
