# 补充案例原始采集记录与复核说明文档 (Supplementary Evidence Catalog & Acquisition Records)

**明确状态标注**：  
**本目录内所有文件均为补充证据材料（Supplementary Evidence），严格独立于已冻结的 12 文件 `evidence/MANIFEST.sha256` 基线之外。**  
冻结基线仅包含 5 个原始案例（`typing-extensions@4.12.2`、`archgraph-layout@2.3.0`、`esprima@4.0.1`、`debug@4.3.4`、`synthetic-fixture@1.0.0`），本目录材料供终审第 3 项扩展审查与独立重查使用，不修改原有 MANIFEST 与基线测试。

---

## 1. 补充案例清单与文件索引

| 软件包坐标 (PURL) | 原始抓取记录 (Raw JSON) | 快照文件 (Snapshot) | 验证输出 (Result) | 案例性质 |
|---|---|---|---|---|
| `pkg:pypi/hatch-vcs@0.4.0` | `pkg-pypi-hatch-vcs-0.4.0.raw.json` | `snapshot-pkg-pypi-hatch-vcs-0.4.0.json` | `result-pkg-pypi-hatch-vcs-0.4.0.json` | 仓库链接错误（Issue #220 已公开报告，机制调查中） |
| `pkg:pypi/validfilepath@0.1` | `pkg-pypi-validfilepath-0.1.raw.json` | `snapshot-pkg-pypi-validfilepath-0.1.json` | `result-pkg-pypi-validfilepath-0.1.json` | 下游索引同步延迟（瞬态 404 → 稳态 200） |
| `pkg:pypi/django-flowcontrol@0.0.21` | `pkg-pypi-django-flowcontrol-0.0.21.raw.json` | `snapshot-pkg-pypi-django-flowcontrol-0.0.21.json` | `result-pkg-pypi-django-flowcontrol-0.0.21.json` | 真实自然不可判定（多源许可证事实证据真空） |

---

## 2. 案例逐项详细说明

### 2.1 案例一：`pkg:pypi/hatch-vcs@0.4.0`

#### (1) 背景与定性说明
- **生态与坐标**：PyPI, `pkg:pypi/hatch-vcs@0.4.0`。
- **发布时间**：`2023-11-06T06:24:55Z`（注意：纠正此前草稿中的 2023-12-11 笔误，PyPI 实际发布时间为 2023-11-06）。
- **审查与定性纠正（对应终审第 2 项）**：
  - 严谨定性：**“仓库链接错误已有公开报告，具体解析机制尚未确认”**；
  - 撤回“官方已确认解析器故障”之断言。在 [google/deps.dev Issue #220](https://github.com/google/deps.dev/issues/220) 中，官方回复仅表示怀疑与 PEP 规范演进有关、会进行调查；维护者 ofek 亦在跟进。因此属于“已公开报告的仓库链接分歧”，官方尚未下达终局根因定论。

#### (2) 采集端点与原始响应信息
- **上游 PyPI JSON API**：
  - 端点：`https://pypi.org/pypi/hatch-vcs/0.4.0/json`
  - HTTP 状态：`200 OK`
  - 标头包含：`Date`, `Content-Type: application/json`, `ETag`, `Server`, 等；
  - 核心内容：`info.project_urls` 清晰将 `Funding` 标为 `https://github.com/sponsors/ofek`，将 `Source` 标为 `https://github.com/ofek/hatch-vcs`。
- **衍生索引 deps.dev API v3**：
  - 端点：`https://api.deps.dev/v3/systems/pypi/packages/hatch-vcs/versions/0.4.0`
  - HTTP 状态：`200 OK`
  - 核心内容：`links` 中将 `label: "SOURCE_REPO"` 指向了 `"https://github.com/sponsors/ofek"`；`relatedProjects` 亦绑定该 sponsors 页面。
- **补充许可源 ClearlyDefined API**：
  - 端点：`https://api.clearlydefined.io/definitions/pypi/pypi/-/hatch-vcs/0.4.0`
  - HTTP 状态：`200 OK`
  - 核心内容：收录基本坐标与描述信息，但许可证 declared 为 null。
- **物理协议层探测 (Git Protocol Probes)**：
  - `git ls-remote https://github.com/sponsors/ofek`：返回 `exit code 128`，`fatal: repository 'https://github.com/sponsors/ofek/' not found`，实测证明该地址在物理上非 Git 代码库；
  - `git ls-remote https://github.com/ofek/hatch-vcs`：返回 `exit code 0`，成功解析 HEAD (`dfec2c06defdb4648eb66f6aadf7b57453d732cd`)，证明为真实源码版本库。

---

### 2.2 案例二：`pkg:pypi/validfilepath@0.1`

#### (1) 背景与定性说明
- **生态与坐标**：PyPI, `pkg:pypi/validfilepath@0.1`。
- **发布时间**：`2026-10-13T09:59:55.901785Z`。
- **案例性质**：下游索引同步摄取滞后（`SYNC_DELAY` / `DOWNSTREAM_INGESTION_LAG`）。

#### (2) 采集端点与时间链凭据
- **节点 T1（上游发布）**：
  - 端点：`https://pypi.org/pypi/validfilepath/0.1/json`
  - HTTP 状态：`200 OK`
  - PyPI 记录上传时间：`2026-10-13T09:59:55.901785Z`。
- **节点 T2（下游瞬态 404）**：
  - 端点：`https://api.deps.dev/v3/systems/pypi/packages/validfilepath/versions/0.1`
  - HTTP 状态：`404 Not Found`
  - 服务端响应时间：`Tue, 13 Oct 2026 10:07:26 GMT`（时延 +450.1s）
  - 响应文本：`version not found\n`
- **节点 T3（下游同步完成 200）**：
  - 端点：`https://api.deps.dev/v3/systems/pypi/packages/validfilepath/versions/0.1`
  - HTTP 状态：`200 OK`
  - 服务端响应时间：`Tue, 13 Oct 2026 10:11:15 GMT`（时延 +679.1s）
  - 响应文本：包含完整 `versionKey`、`publishedAt: 2026-10-13T09:59:55Z`、`licenses: ["MIT"]`。

#### (3) 当前实时状态与证据局限性如实说明（对应终审第 3 项）
- **当前实时采集状态**：
  - 实时执行采集时，PyPI (`200 OK`)、deps.dev (`200 OK`)、ClearlyDefined (`200 OK`) 均已就绪，当前 API 响应原文与完整 HTTP 标头已完整保存在 `pkg-pypi-validfilepath-0.1.raw.json` 中。
- **历史瞬态 404 局限性说明**：
  - 由于 deps.dev 的索引摄取滞后是**瞬态事件**（摄取窗口约在 7.5 至 11.3 分钟内收敛），在下游摄取完毕后，远程端点已持久化为 HTTP 200。
  - **无法在当前网络环境下对远程端点发起请求重新产生历史的 404 响应包**。历史 404 仅具备当时抓取所记录的时间标头与报文摘录。按终审审查要求，不将该瞬态 404 夸大为拥有全量可复现抓包，特此如实记录该时序证据的自然局限。

---

### 2.3 案例三：`pkg:pypi/django-flowcontrol@0.0.21`

#### (1) 背景与定性说明
- **生态与坐标**：PyPI, `pkg:pypi/django-flowcontrol@0.0.21`。
- **发布时间**：`2026-10-13T09:57:53Z`。
- **案例性质**：真实自然不可判定（`INDETERMINATE` / `undecidable`，置信度 `0.0`）。

#### (2) 采集端点与原始响应信息
- **上游 PyPI JSON API**：
  - 端点：`https://pypi.org/pypi/django-flowcontrol/0.0.21/json`
  - HTTP 状态：`200 OK`
  - 核心字段：`info.license: null`，`info.license_expression: null`，`info.classifiers: []`（无任何 License 分类器）。
- **衍生索引 deps.dev API v3**：
  - 端点：`https://api.deps.dev/v3/systems/pypi/packages/django-flowcontrol/versions/0.0.21`
  - HTTP 状态：`200 OK`
  - 核心字段：`licenses: []`（下游未提取到任何许可证）。
- **补充许可源 ClearlyDefined API**：
  - 端点：`https://api.clearlydefined.io/definitions/pypi/pypi/-/django-flowcontrol/0.0.21`
  - HTTP 状态：`200 OK`
  - 核心字段：`licensed.score.total: 0`，`declared: null`，`discovered: {}`。
- **验证机制**：
  - 触发 PMV 核心硬约束规则 `CONSISTENCY_01_COMPARABLE_LICENSE`。
  - 证明“双源皆空”属于事实证据真空（Evidence Vacuum），而非“空与空相等”，拒绝武断输出 `CONSISTENT`，严格判定为不可判定（`undecidable`，置信度 `0.0`）。

---

## 3. 文件格式与复跑指引

每个案例均配对提供三类文件：
1. **`*.raw.json`**：包含真实 API 调用的未修改原始响应数据、HTTP 状态码、全量响应标头（Headers）、SHA-256 校验和以及补充法证信息；
2. **`snapshot-*.json`**：符合 PMV 采集清洗规范的快照格式，可直接供 PMV 加载器重放；
3. **`result-*.json`**：PMV 验证引擎对该快照运行规则集 `rules-v0.1.json` 得出的结构化判定结果。

可以通过 PMV 引擎对上述快照进行独立检验：
```bash
# 示例：复核 django-flowcontrol 自然不可判定快照
python3 -c "
import json
from pmv.normalizer import Normalizer
from pmv.verifier import Verifier

snapshot = json.load(open('evidence/supplementary/snapshot-pkg-pypi-django-flowcontrol-0.0.21.json'))
norm = Normalizer().normalize(snapshot)
verdict = Verifier('rules/rules-v0.1.json').verify(norm)['verdict']
print('Verdict:', verdict['category'], verdict['subcode'], 'Confidence:', verdict['confidence'])
"
```
