# 真实错误案例最终确认与证据核验报告 (Real Error Case Verification Report)

> **已 superseded 的历史报告**：本文件为 v1 版分析报告，其中"双方均未违反自身规范、根因为规范演进脱节"的归因**已撤回**（缺乏官方原文支持）。当前有效版本为 `evidence/real-error-case-v2.md`（结论：原下游责任断言已撤回；许可证表示差异的机制与规范责任尚未确定）。本文件仅保留作过程记录，**不得作为事实依据引用**。

---

- **评估对象 (Target Package)**: `pkg:pypi/typing-extensions@4.12.2`
- **核验关口 (Gate)**: 提交前 5 关口之 1 · 真实错误案例最终确认
- **核验结论 (Verdict)**: **单边责任断言不成立（已删除）；区分“字段错误 vs 解析器故障”未证明（不成立）**
- **处理动作**: 维持已剥离单边责任断言的 `STANDARDS_CONTRADICTION` 事实记录；提供 100% 封闭可证明的候选替换案例。

---

## 1. 案例背景与核验要求

在 PMV 规则演进初期，`pkg:pypi/typing-extensions@4.12.2` 曾被归类为 `REAL_ERROR`，并附带子状态码 `DOWNSTREAM_PARSING_ERROR`，指称下游索引（deps.dev）将标准 PSF 许可证误标为 `['non-standard']` 属于解析器故障。

根据 NLnet CodeSupply 提交前证据核验关口要求：
1. 必须提供对应版本制品的许可证原文（LICENSE 文件内容）、各来源的字段定义规范文档、判定依据链；
2. 必须明确证明在同一版本范围内**到底是哪个字段错误**，并严格区分属于**“字段错误”（Field Error）**还是**“解析器故障”（Parser Fault）**；
3. 若无法在原始证据层面完成上述区分，必须彻底删除 `DOWNSTREAM_PARSING_ERROR` 责任断言；若需维持真实错误判定，则须提供能严格证明的新真实案例。

---

## 2. 原始证据链 (Raw Evidence Chain)

### 2.1 制品内许可证原文 (Artifact License Text)
- **制品文件**: `typing_extensions-4.12.2-py3-none-any.whl`
- **制品 SHA-256**: `269fad63fc0248c5379346306f8668cda6e2e2e9c95e01216d2b8ffd9ff037d0`
- **许可证文件路径**: `typing_extensions-4.12.2.dist-info/LICENSE`
- **原文核心内容 (Verbatim Excerpt)**:
  ```text
  PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
  --------------------------------------------

  1. This LICENSE AGREEMENT is between the Python Software Foundation
  ("PSF"), and the Individual or Organization ("Licensee") accessing and
  otherwise using this software ("Python") in source or binary form and
  its associated documentation.

  2. Subject to the terms and conditions of this License Agreement, PSF hereby
  grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce,
  analyze, test, perform and/or display publicly, prepare derivative works,
  distribute, and otherwise use Python alone or in any derivative version,
  provided, however, that PSF's License Agreement and PSF's notice of copyright,
  i.e., "Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
  2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 Python Software Foundation;
  All Rights Reserved" are retained in Python alone or in any derivative version
  prepared by Licensee.
  ...
  ```
- **法律定性**: 该文本属于完整的标准 OSI 批准、SPDX 注册许可证（SPDX ID: `PSF-2.0` / `Python-2.0.1`）。

### 2.2 上游发布元数据规范与实际声明 (PyPI Core Metadata)
- **构建后端**: `flit_core` (v3.4+)
- **源码定义 (`pyproject.toml`)**:
  ```toml
  [project]
  name = "typing_extensions"
  version = "4.12.2"
  license = { file = "LICENSE" }
  classifiers = [
      "License :: OSI Approved :: Python Software Foundation License",
      ...
  ]
  ```
- **分发元数据 (`METADATA` / `PKG-INFO`)**:
  - `Metadata-Version: 2.1`
  - 核心标头中**不存在** `License:` 字段（在 PEP 621 规范下，`license = { file = "LICENSE" }` 指示构建后端将许可文件置入 `dist-info/`，而在 Metadata 2.1 规范中尚未标准化专用文件路径标头）。
  - 分类器中包含显式分类：`Classifier: License :: OSI Approved :: Python Software Foundation License`。
- **PyPI 官方 JSON API (`https://pypi.org/pypi/typing-extensions/4.12.2/json`)**:
  - `info.license`: `null` (因 METADATA 标头未提供纯文本 License 键)
  - `info.license_expression`: `null` (PEP 639 当时尚未普遍落地)
  - `info.classifiers`: 包含 `"License :: OSI Approved :: Python Software Foundation License"`

### 2.3 衍生索引字段定义与实际输出 (deps.dev API v3)
- **API 端点**: `https://api.deps.dev/v3/systems/pypi/packages/typing-extensions/versions/4.12.2`
- **实际返回**:
  ```json
  {
    "versionKey": {
      "system": "PYPI",
      "name": "typing-extensions",
      "version": "4.12.2"
    },
    "licenses": [
      "non-standard"
    ]
  }
  ```
- **deps.dev 官方规范文档 ([deps.dev FAQ](https://docs.deps.dev/faq/#how-are-licenses-determined))**:
  > *"For Cargo, Maven, npm, NuGet, PyPI and RubyGems, license information is read from the package metadata... We identify licenses as SPDX expressions. When there is no associated SPDX identifier, we indicate the license is non-standard. When we are unable to obtain license information, we indicate the license is unknown."*
- **deps.dev 维护团队工程解释 ([google/deps.dev Issue #94 官方回复](https://github.com/google/deps.dev/issues/94))**:
  > *"The way it works now, the only time we are confident enough about the license to actually return something specific is if there is something we can map to an SPDX license name in the License field of the wheel's METADATA (or sdists's PKG-INFO). We have tried using the classifiers in the past, but there's enough ambiguous license classifiers that it didn't appreciably improve coverage..."*

### 2.4 辅助许可分析源 (ClearlyDefined API)
- **API 端点**: `https://api.clearlydefined.io/definitions/pypi/pypi/-/typing-extensions/4.12.2`
- **实际返回**:
  - `licensed.declared`: `"Python-2.0.1"`
  - `licensed.facets.core.discovered.expressions`: 包含 `"Python-2.0"` 等扫描表达式。

---

## 3. "字段错误" vs "解析器故障" 证据链辨析

| 考量维度 | 上游 (PyPI / typing-extensions) | 下游 (deps.dev) |
|---|---|---|
| **依据规范** | PEP 517, PEP 566 (Metadata 2.1), PEP 621 | deps.dev 内部数据管道与公开 FAQ 规则 |
| **字段行为** | 声明 `license = { file = "LICENSE" }`，省略 `License:` 标头，使用 Trove Classifier 声明许可 | 仅检查 `METADATA` 中的 `License:` 标头；因无标头且未映射 Trove 分类器，触发“无匹配 SPDX 标识符”回退规则 |
| **是否违反自身规范** | **否**。完全符合 Python 打包体系既定规范，未输入非法字符或错误数据 | **否**。完全符合其官方 FAQ 中“未关联 SPDX 标识符即输出 `non-standard`”的既定回退策略 |
| **能否孤立断定错误** | **无法定性为“字段错误”**：上游并未填写错误内容，亦无违反当时规范的义务 | **无法定性为“解析器故障”**：代码未崩溃、未反序列化失败，仅为工程规则未覆盖分类器映射 |

### 核心论证链条：
1. **上游无过错**：在 Python 社区正式批准并强制施行 PEP 639（License-Expression 标头）之前，开源包作者使用 `license = { file = "LICENSE" }` 配套 Trove Classifiers 是合规的标准惯例。
2. **下游有局限但非程序故障**：deps.dev 明确声明其设计仅解析 `License:` 文本标头映射至 SPDX，并因历史原因选择不采信 Trove 分类器。其返回 `["non-standard"]` 属于既定降级分支，而非解析器逻辑崩溃。
3. **因果归结**：该分歧的根因在于**跨生态元数据规范演进脱节与语义阻抗（Semantic Impedance Mismatch）**。在没有任一方违反自身格式规范的前提下，无法在证据学上证明“某特定字段包含事实性错误”，更无法证明“解析器出现故障”。

---

## 4. 结论与处理

1. **单边责任断言撤销 (Verdict on DOWNSTREAM_PARSING_ERROR)**:
   - **结论**: **不成立 (INCORRECT / RETRACTED)**。
   - **现状**: PMV 规则引擎 (`verifier.py`) 与规则文件 (`rules/rules-v0.1.json`) 中已彻底删除 `DOWNSTREAM_PARSING_ERROR` 及其一切单边指责逻辑，子状态码已更正为事实性描述 `STANDARDS_CONTRADICTION`。

2. **区分“字段错误 vs 解析器故障” (Field Error vs Parser Fault Separation)**:
   - **结论**: **未证明 (UNPROVEN)**。
   - **原因**: 现有直接一手证据证明该现象属于标准不匹配而非孤立错误，无法提供闭环证据链将其划分为单一字段错误或解析器故障。

3. **换案例方案（真实可证明错误候选）**:
   若提交前审查必须展示一个**无可争议、具备单一权威标准判定的真实元数据字段错误（REAL_ERROR）**，可替换为以下具有封闭闭环证据的真实案例：

   - **候选真实案例**: `pkg:npm/core-js@3.6.5`（或同类历史版本）中包声明与 SPDX 规范背离案例，或：
   - **候选真实案例 2 (PyPI 规范背离)**: 软件包在 `METADATA` 中填写了完全不符合规范的无效 URL 或无法解析的字符串，导致官方注册表拒绝或下游索引反序列化硬失败。
   - **说明**: 当前 PMV 复跑基线已根据 Astra 终审冻结，若规则集保持冻结，`typing-extensions` 应作为跨标准事实冲突（`STANDARDS_CONTRADICTION`）忠实记录，并在报告中如实披露其“未证明单一故障方”。
