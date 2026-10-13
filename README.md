# CodeSupply · Package Metadata Verifier (PMV)

**可运行的最小质检组件原型 (Minimum Viable Quality Inspection Component)**  
*技术负责人：Joey（Jigao Yi）个人申请 | 授权许可：Apache-2.0*

---

## 1. 组件背景与核心定位

在开源软件包供应链元数据聚合中，简单字段比对（Naive Field Diff）极易导致大量误判：例如将下游索引尚未同步的近期发布武断判定为“包丢失或镜像损坏”；将不同构建制品（Wheel vs Sdist）或不同算法（SHA-1 vs SHA-256）的哈希差异误判为“恶意篡改”；或将许可证复合表达式（AND / OR）强行单值化。

**PMV（Package Metadata Verifier）** 是为 NLnet CodeSupply 提案打造的可运行最小原型组件，旨在实现**“带来源（Provenance）、时间戳（Timestamps）与离线可复现证据的跨源差异判定与生命周期追踪”**。通过版本化质检规则（`rules v0.1`），PMV 提供了结构化仲裁证据链，彻底避免普通字段比对的误判。

---

## 2. 模块划分与工程架构

```
pmv/
├── LICENSE                 # Apache-2.0 许可声明
├── README.md               # 架构、实测案例与聚合方接入指南
├── rerun.sh                # 离线确定性复跑脚本（实际校验哈希清单、Schema、规则、代码并逐字节比对）
├── rerun-report.md         # 独立复跑审计报告（100% 字节级一致、Schema 校验通过、清单全匹配）
├── run_harvest.py          # 真实案例在线采集与基线生成脚本
├── bin/
│   └── pkgmeta-verify      # CLI 可执行入口脚本
├── pmv/
│   ├── __init__.py         # 包信息与 Apache-2.0 头
│   ├── collector.py        # 采集器：支持实时 HTTP 抓取与离线快照回放
│   ├── normalizer.py       # 归一器：制品归一化、许可证分类与来源依赖关系建模
│   ├── verifier.py         # 判定器：实现终审意见原文约束的核心决策引擎
│   ├── exporter.py         # 证据导出器：最小化脱敏快照与 SHA-256 清单计算
│   └── cli.py              # CLI 命令解析与人机交互展示
├── rules/
│   └── rules-v0.1.json     # 版本化质检规则集（v0.1）
├── schemas/
│   └── pmv-output.schema.json # 标准化输出 JSON Schema (Draft 2020-12, 项目版本化 $id)
├── tests/
│   ├── __init__.py         # 测试包声明
│   ├── test_verifier_rules.py # 判定规则与硬约束针对性回归测试
│   └── test_schema.py      # Schema 自检与实例校验测试
└── evidence/
    ├── MANIFEST.sha256     # 离线证据包与规则文件的 SHA-256 校验清单
    ├── snapshots/          # 最小可再分发原始响应脱敏快照（5个用例）
    └── results/            # 判定结果 JSON 文件（5个用例）
```

---

## 3. 双生态与对照源锁定

PMV 锁定 **npm** 与 **PyPI** 双生态，每个生态均包含权威注册表与第三方索引源，并补充 ClearlyDefined 作为许可证对照：

1. **npm 生态**：
   - 权威源：`registry.npmjs.org`（完整 packument 与 release tarball 元数据）
   - 对照源：`api.deps.dev v3`（Google Open Source Insights API）
   - 补充源：`api.clearlydefined.io`（深入源码扫描的许可证定义）
2. **PyPI 生态**：
   - 权威源：`pypi.org/pypi/<pkg>/<ver>/json`（PyPI JSON API，注：与 PEP 503/691 Simple 是同一 Warehouse 注册表的双接口）
   - 对照源：`api.deps.dev v3`（PyPI 镜像索引）
   - 补充源：`api.clearlydefined.io`（源码级许可证比对）

---

## 4. 终审硬约束在规则中的落实

根据终审意见原文（ASTRA-REV2 第 4 节 checklist），PMV 在 `rules/rules-v0.1.json` 与 `verifier.py` 中严格落实了各项判定硬约束：

1. **哈希比较硬约束**：
   - **严格限定**：哈希比对**只允许同一制品、同一算法**。
   - **制品同一性核验**：必须具备制品级证据（摘要 digest、下载 URL、包内文件清单其一），仅文件名相同不得认定为同一制品，直接输出 `undecidable`。
   - **摘要统一 `.lower()` 审计记录**：十六进制 hex digest 比较前统一大小写与去除首尾空格是允许的，但必须在 `decision_audit_trail` 中显式记录原始值与归一化动作，且仅限同一算法。
   - **跨输入统一为判定值**：若输入为跨算法（如 SHA-1 vs SHA-256）或跨制品（如 Wheel vs Sdist），输出统一判定值 `INDETERMINATE`（子状态码 `undecidable`），严禁抛出未捕获异常退出。
   - **仅证明摘要冲突**：对于同一制品、同一算法但哈希值不一致的情况，判定归类为 `DIGEST_CONFLICT`，结论严格限定为“摘要冲突”，**严禁断言镜像损坏或恶意篡改**。
2. **延迟时间链与不确定性保留（`SYNC_DELAY`）**：
   - **无发布时间仍判延迟之修正**：缺少上游发布时间字段时，不得输出 SYNC_DELAY，必须输出 `undecidable`（低置信度疑似延迟）。
   - **三段延迟时间链**：保存发布时间、下游缺失观察（404）、后续出现观察（200）三段证据，只报告可证明的延迟范围；单次 404 或缺少时间证据时输出不可判定／疑似延迟。
3. **真实错误责任断言剥离（`REAL_ERROR`）**：
   - 在无法区分字段缺失 vs 解析器故障的情况下，删除 `DOWNSTREAM_PARSING_ERROR` 及其单边责任断言。保存对应版本制品的许可证原文（如 wheel 包内 `dist-info/LICENSE`）与各源字段定义，客观判定为 `STANDARDS_CONTRADICTION`。
4. **语义差异多源与扫描范围补全（`SEMANTIC_DIVERGENCE`）**：
   - 当许可证出现逻辑运算符（`AND` / `OR`）或单值 vs 复合值差异时，判定为 `SEMANTIC_DIVERGENCE`，**严禁自动采信单方**。同时明确列出参与判定的全部来源、字段以及文件扫描范围（核心切面源码级扫描 vs 顶层声明）。
5. **空证据严禁默认一致**：
   - 当证据为空或不足（可用对照源少于 2 个）时，严禁默认返回 `CONSISTENT`，必须返回 `undecidable`。
6. **来源依赖关系明确记录（Source Provenance DAG）**：
   - `deps.dev` 的版本发布与哈希等字段本身衍生自权威注册表。PMV 在 `provenance_and_dependencies` 中强制记录 `[deps_dev -> registry]` 依赖链，显式标注“二者一致仅为摄取传播结果，不得作为独立真值证明”。
7. **synthetic 标记一致性**：
   - 跨算法比较模拟输入明确标记 `synthetic=true`，与构造基准 fixture 分开统计。

---

## 5. 四类案例与判定依据

| 判定类别 | 案例坐标 (PURL) | 对照源与状态 | 实测判定依据 | 相较普通 Diff 避免的误判 |
|---|---|---|---|---|
| **`REAL_ERROR`**<br>(真实错误) | `pkg:pypi/typing-extensions@4.12.2` | PyPI JSON (200)<br>deps.dev v3 (200)<br>ClearlyDefined (200) | 制品内 `dist-info/LICENSE` 与 PyPI 分类器明确为标准 PSF-2.0，ClearlyDefined 验证为 `Python-2.0.1`。但 deps.dev 标注为 `['non-standard']`。因核心元数据缺少显式 PEP 639 License-Expression，无法区分字段缺失还是解析故障，删除了单边责任归咎，判定为 `STANDARDS_CONTRADICTION`。 | 普通 Diff 仅报告字符串不一致或直接归咎某方。PMV 客观记录标准冲突，避免合规系统误拒合规核心库。 |
| **`SYNC_DELAY`**<br>(同步延迟) | `pkg:pypi/archgraph-layout@2.3.0` | PyPI JSON (200)<br>deps.dev v3 (404 & 200) | 基于上游发布时间 (06:16:05Z)、下游 404 缺失观察 (06:31:25Z) 及后续 200 出现观察 (07:15:00Z) 建立完整三段链，计算出可证明的延迟范围 `[920s, 3535s]`，处于 24h 容忍窗口内，判定为 `SYNC_DELAY`。 | 普通 Diff 会将 deps.dev 404 判定为“版本不存在/数据丢失”。PMV 识别时间链，保留不确定性并放行进入延迟重试队列。 |
| **`SEMANTIC_DIVERGENCE`**<br>(语义差异) | `pkg:npm/esprima@4.0.1` | npm packument (200)<br>ClearlyDefined (200) | 明确判定源（`npm_registry`, `clearlydefined`, `deps_dev`）与字段。ClearlyDefined 全仓库核心切面文件级扫描发现并声明 `BSD-2-Clause AND BSD-3-Clause`，与 npm 顶层声明 `BSD-2-Clause` 存在布尔与义务差异，禁止自动采信单方。 | 普通 Diff 会强行以顶层声明覆盖深度扫描，或机械合并导致许可冲突。PMV 标识复合布尔语义差异。 |
| **`INDETERMINATE`**<br>(无法判定) | `pkg:npm/debug@4.3.4`<br>*(synthetic=true)* | npm packument (200) | 跨算法比对测试：输入仅有 SHA-1 (`3d75be84...`) 与外部 SHA-256 请求。因缺乏共享算法，判定输出 `undecidable`。输入明确标为 `synthetic=true` 与真实案例分开统计。 | 普通 Diff 会因字符串不相等直接报警“哈希不匹配/被篡改”，或因算法键缺失触发 `KeyError` 崩溃。PMV 优雅降级为 `undecidable`。 |
| **`DIGEST_CONFLICT`**<br>(*构造用例, synthetic=true*) | `pkg:npm/synthetic-fixture@1.0.0` | npm registry (200)<br>synthetic mirror (200) | 同一制品 `synthetic-fixture-1.0.0.tgz`（包含 URL 及摘要证据）与同一算法 `SHA-256`，哈希值不同 (`aaa...` vs `bbb...`)。 | 普通 Diff 会断言“镜像遭黑客篡改/损坏”。PMV 恪守客观边界，仅认定“摘要冲突”，要求进一步核验镜像源证明。 |

---

## 6. 命令行使用说明 (CLI Usage)

```bash
# 1. 实时抓取并质检软件包
./bin/pkgmeta-verify check pkg:pypi/typing-extensions@4.12.2

# 2. 离线复现模式（完全基于 evidence/snapshots/ 快照，可断网运行）
./bin/pkgmeta-verify check pkg:npm/esprima@4.0.1 --offline

# 3. 指定输出 JSON 文件
./bin/pkgmeta-verify check pkg:pypi/archgraph-layout@2.3.0 --offline --output /tmp/result.json

# 4. 触发跨算法不可比性硬约束测试（输出 undecidable，synthetic=true）
./bin/pkgmeta-verify check pkg:npm/debug@4.3.4 --offline --cross-algo-test
```

### CLI 输出示例
```
========================================================================
PMV Quality Verification: pkg:pypi/typing-extensions@4.12.2
Ruleset: v0.1 | Mode: OFFLINE_REPLAY
Verdict Category: REAL_ERROR (Subcode: STANDARDS_CONTRADICTION)
Confidence:       1.0
Summary:          Downstream index license classification contradicts upstream and curated standards
------------------------------------------------------------------------
Avoided False Positive:
  Avoided discarding or flagging a legitimate package as license-incompatible while avoiding unverified attribution of parser fault.
------------------------------------------------------------------------
Source Dependencies:
  - [deps_dev -> pypi_json]: Downstream ingestion of upstream registry metadata; consistency represents ingestion propagation, NOT independent ground-truth verification.
========================================================================
```

---

## 7. 独立复跑、自动化测试与字节级复现 (Independent Rerun)

项目内置一键离线复跑脚本 `rerun.sh`：
- **密码学清单校验**：实际运行 `sha256sum -c evidence/MANIFEST.sha256` 校验全部 12 个规则、Schema、快照与基线文件；
- **Schema 严格校验**：执行 Draft 2020-12 Schema 自检及全部结果实例校验；
- **针对性回归测试**：执行 `tests/test_*.py` 中覆盖全部误判缺陷的 14 个回归测试用例；
- **确定性判定复跑**：对动态运行时时间戳 `evaluation_timestamp` 进行中立隔离后，与基线执行逐字节比对（`diff -u`）；
- **动态审计报告**：失败时非零退出，通过时生成 `rerun-report.md`。

```bash
# 执行完整独立复跑与检验
./rerun.sh

# 单独执行自动化回归测试集
python3 -m unittest discover -s tests -p "test_*.py"

# 手动校验所有离线证据包与规则文件的 SHA-256 清单
cd evidence && sha256sum -c MANIFEST.sha256
```

---

## 8. 规范与 Schema 说明

输出结果遵循严格的 JSON Schema 规范，定义文件位于 `schemas/pmv-output.schema.json`。
- **类型规范**：完全使用合法的 Draft 2020-12 小写类型（`object`, `string`, `array`, `boolean`, `number`, `integer` 等）。
- **$id 地址**：`https://pmv.codesupply.org/schemas/pmv-output/v0.1.json`（*注：项目上线并绑定生产域名之前，作为版本化规范占位地址*）。
- **核心字段**：
  - `purl`, `ecosystem`, `name`, `version`, `ruleset_version`, `synthetic`
  - `verdict`: `category`, `subcode`, `confidence`, `summary`, `details`, `avoided_false_positive`
  - `provenance_and_dependencies`: `sources_consulted`, `dependency_relations`
  - `normalized_evidence`: 各源规范化数据
  - `decision_audit_trail`: 规则审计判定轨迹（含大小写归一化动作与原始值记录）
