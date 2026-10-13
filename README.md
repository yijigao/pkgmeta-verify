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

根据终审意见原文（ASTRA-REV2 与 ASTRA-REV3 终审意见），PMV 在 `rules/rules-v0.1.json` 与 `verifier.py` 中严格落实了各项判定硬约束：

1. **制品身份关联核验 (同名文件不同摘要)**：
   - 摘要比对**必须验证制品身份关联**（证明 digest 绑定到同一下载 URL / 同一包内文件清单 / 同一制品发布记录之一）。
   - 仅“两边都有摘要”不足以证明同一制品，未证明身份关联时严格输出 `INDETERMINATE`（子状态码 `ARTIFACT_IDENTITY_UNPROVEN`），**严禁判定为 `DIGEST_CONFLICT`**。
   - 对于同一制品、同一算法且身份已证明的哈希冲突，判定为 `DIGEST_CONFLICT`，结论严格限定为“摘要冲突”，**严禁断言镜像损坏或恶意篡改**。
2. **编码感知字节级解码 (禁止静默 `.lower()` 判匹配)**：
   - 摘要比对统一按编码**解码为原始字节后比对**（十六进制 hex 经解码比对消除大小写差异；Base64 区分大小写比对）。
   - 禁止对 Base64 等区分大小写的编码静默 `.lower()` 判匹配。若编码未知或不支持，明确输出 `INDETERMINATE`（子状态码 `ENCODING_UNSUPPORTED`）。
3. **延迟时间链与观测有效性校验 (`SYNC_DELAY`)**：
   - 必须同时满足：**后续观察 HTTP 成功状态 (200)**、**有效发布时间**、**严格正向观察时间顺序**（`t_observed_after > t_observed_before > t_published`）。
   - 任一不满足均判定为 `INDETERMINATE`（子状态码 `undecidable`，疑似延迟，标注不确定性）。
   - 包含发布时间、下游缺失观察（404）、后续出现观察（200）的完整可信三段链，方可输出可证明的延迟范围。
4. **跨源许可证主动比对与可比性检查 (`SEMANTIC_DIVERGENCE`)**：
   - 实际进行字段比较；两源许可证为 MIT vs Apache-2.0 属于**明确不一致**，判定为 `SEMANTIC_DIVERGENCE`（子状态码 `LICENSE_DECLARATION_DISCREPANCY`）。
   - 当许可证出现逻辑运算符（`AND` / `OR`）时，判定为 `SEMANTIC_DIVERGENCE`（`LICENSE_EXPRESSION_CONJUNCTION_MISMATCH`），严禁自动采信单方。
   - 一源缺少可比字段时，严格判定为 `INDETERMINATE`（`undecidable`），**坚决禁止“无比较就判一致”**。
5. **真实错误经验证据要求 (`REAL_ERROR`)**：
   - 必须依赖制品内实际 LICENSE 原文等经验证据（如 wheel 包内 `dist-info/LICENSE`）。未提供对应证据时不得判定 `REAL_ERROR`（输出 `undecidable` 并注明缺证据）。
   - **删除一切硬编码事实断言**；在无法区分字段缺失 vs 解析器故障的情况下，删除 `DOWNSTREAM_PARSING_ERROR` 及其单边责任断言，客观判定为 `STANDARDS_CONTRADICTION`。
6. **archgraph-layout 延迟案例降级**：
   - 该公开案例降级为“**疑似延迟，时间链待核验**”，在证据与结果中标记 `verification_status: "suspect"` 与 `audit_status: "retracted"`，不再列为已证明的延迟。
7. **空证据严禁默认一致**：
   - 当证据为空或不足（可用对照源少于 2 个）时，严禁默认返回 `CONSISTENT`，必须返回 `undecidable`。
8. **来源依赖关系明确记录 (Source Provenance DAG)**：
   - PMV 在 `provenance_and_dependencies` 中强制记录 `[deps_dev -> registry]` 依赖链，显式标注“二者一致仅为摄取传播结果，不得作为独立真值证明”。
9. **synthetic 标记一致性**：
   - 跨算法比较模拟输入明确标记 `synthetic=true`，与构造基准 fixture 分开统计。

---

## 5. 案例与判定依据

| 判定类别 | 案例坐标 (PURL) | 对照源与状态 | 实测判定依据 | 相较普通 Diff 避免的误判 |
|---|---|---|---|---|
| **`REAL_ERROR`**<br>(真实错误) | `pkg:pypi/typing-extensions@4.12.2` | PyPI JSON (200)<br>deps.dev v3 (200)<br>ClearlyDefined (200) | 基于制品内 `typing_extensions-4.12.2.dist-info/LICENSE` 经验证据与 PyPI 分类器明确为标准 PSF-2.0，ClearlyDefined 验证为 `Python-2.0.1`。但 deps.dev 标注为 `['non-standard']`。动态引用经验证据，客观判定为 `STANDARDS_CONTRADICTION`，删除单边归因。 | 普通 Diff 仅报告字符串不一致或直接归咎某方。PMV 客观记录标准冲突，避免合规系统误拒合规核心库。 |
| **`INDETERMINATE`**<br>(疑似延迟，时间链待核验) | `pkg:pypi/archgraph-layout@2.3.0` | PyPI JSON (200)<br>deps.dev v3 (404 & 200) | 按照 Astra rev3 审查要求，该案例降级为“疑似延迟，时间链待核验”，标记 `verification_status: suspect` 与 `audit_status: retracted`。从已证明延迟案例撤下，判定为 `INDETERMINATE` (`undecidable`)。 | 避免在缺乏原始日志核验时武断宣称延迟已获确凿证明。保留快照审计记录并保留不确定性。 |
| **`SEMANTIC_DIVERGENCE`**<br>(语义差异) | `pkg:npm/esprima@4.0.1` | npm packument (200)<br>ClearlyDefined (200) | 明确判定源（`npm_registry`, `clearlydefined`, `deps_dev`）与字段。ClearlyDefined 全仓库核心切面文件级扫描发现并声明 `BSD-2-Clause AND BSD-3-Clause`，与 npm 顶层声明 `BSD-2-Clause` 存在布尔与义务差异，禁止自动采信单方。 | 普通 Diff 会强行以顶层声明覆盖深度扫描，或机械合并导致许可冲突。PMV 标识复合布尔语义差异。 |
| **`INDETERMINATE`**<br>(无法判定) | `pkg:npm/debug@4.3.4`<br>*(synthetic=true)* | npm packument (200) | 跨算法比对测试：输入仅有 SHA-1 (`3d75be84...`) 与外部 SHA-256 请求。因缺乏共享算法，判定输出 `undecidable`。输入明确标为 `synthetic=true` 与真实案例分开统计。 | 普通 Diff 会因字符串不相等直接报警“哈希不匹配/被篡改”，或因算法键缺失触发 `KeyError` 崩溃。PMV 优雅降级为 `undecidable`。 |
| **`DIGEST_CONFLICT`**<br>(*构造用例, synthetic=true*) | `pkg:npm/synthetic-fixture@1.0.0` | npm registry (200)<br>synthetic mirror (200) | 同一制品 `synthetic-fixture-1.0.0.tgz`（具备版本发布记录与 origin_url 身份绑定证据）与同一算法 `SHA-256`，解码字节不同 (`aaa...` vs `bbb...`)。 | 普通 Diff 会断言“镜像遭黑客篡改/损坏”。PMV 恪守客观边界，仅认定“摘要冲突”，要求进一步核验镜像源证明。 |

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
- **针对性回归测试**：执行 `tests/test_*.py` 中覆盖全部误判缺陷的 25 个回归测试用例；
- **确定性判定复跑**：对动态运行时时间戳 `evaluation_timestamp` 进行中立隔离后，与基线执行逐字节比对（`diff -u`）；
- **动态审计报告**：失败时非零退出，通过时生成 `rerun-report.md`，口径严格遵循“现有测试零失败”。

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
