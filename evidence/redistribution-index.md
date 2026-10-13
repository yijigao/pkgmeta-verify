# 证据快照再分发索引与合规授权说明 (Evidence Snapshots Redistribution Index)

**规范依据**：对应提案终审第 7 项（修正 §12 中关于“逐项再分发说明已完成”的过度声明，建立逐项真实索引；**拿不到的信息如实标记为“待办”，绝不虚报“已具备”**）。  
**适用范围**：`evidence/snapshots/` 下已纳入冻结基线的全部 5 个快照文件，以及 `evidence/supplementary/` 扩展快照。

---

## 1. 核心来源服务之条款与再分发通用基线

PMV 离线快照涉及四个主要外部数据提供方。在对具体快照逐项索引之前，先明确各数据源的公开条款、法理属性与当前授权状态：

| 数据源服务 | 典型端点 | 官方条款/许可 (Terms / License) | 署名要求 (Attribution) | 再分发法理依据 | 当前授权就绪状态 |
|---|---|---|---|---|---|
| **npm Registry** | `https://registry.npmjs.org/<pkg>/<ver>` | npm Terms of Use (GitHub Acceptable Use Policies) | 官方建议标明数据来源于 npm public registry；未要求特定法律格式 | 事实性技术元数据（不受独创性版权保护）；微量提取供安全验证之合理使用 (Fair Use) | **部分具备，核心待办**：缺少 GitHub/npm 官方书面数据再分发白名单确认 |
| **PyPI (Warehouse)** | `https://pypi.org/pypi/<pkg>/<ver>/json` | Python Software Foundation (PSF) Terms of Use / PyPI Acceptable Use Policy | 需注明来源于 Python Package Index (pypi.org) | 纯事实技术数据（文件名、哈希、上传时间、分类器），不含受独创性版权保护的表达 | **部分具备，核心待办**：PSF 尚未就 API 原始 JSON 数据发布显式 CC/开放数据许可，批量分发条款待办确认 |
| **Google deps.dev** | `https://api.deps.dev/v3/...` | Google APIs Terms of Service / Open Source Insights Terms | 页面要求注明 "Data from Open Source Insights (deps.dev)" | 极小片段的技术分析对照；转化性研究用途 (Transformative Fair Use) | **待办**：Google APIs ToS 对数据缓存与再分发有常规限制；未取得显式离线测试集再分发授权，**严禁写“已具备”** |
| **ClearlyDefined** | `https://api.clearlydefined.io/definitions/...` | **CC0** (Creative Commons Zero) | 建议保留 ClearlyDefined 来源链接（CC0 不强制署名） | CC0 公有领域奉献，自由复制与再分发 | **已具备（条款明确）** |
| **Synthetic Fixture** | `https://registry.npmjs.org/...` (桩) | Apache-2.0 / CC0 (CodeSupply PMV 原创构造) | 标注为 PMV 项目组合成桩，无第三方署名限制 | 自主版权直接开源分发 | **已具备** |

---

## 2. 冻结基线 5 个快照逐项再分发索引

### 2.1 `evidence/snapshots/pkg-npm-debug-4.3.4.json`

- **软件包坐标**: `pkg:npm/debug@4.3.4` (Ecosystem: npm)
- **采集时间戳 (`fetch_timestamp`)**: `2026-10-13T06:31:27Z`
- **人工/合成属性**: `synthetic: false` (真实网络采集，包含跨算法对比合成插桩)
- **逐项来源明细**:
  1. **Source: `registry`**
     - **端点**: `https://registry.npmjs.org/debug/4.3.4`
     - **HTTP 状态**: `200 OK`
     - **来源许可/条款**: npm Terms of Use (GitHub)。
     - **署名要求**: 标明源自 npm registry。
     - **裁剪说明**: 剔除了 42KB README 正文、所有维护者邮箱与个人信息、非目标版本信息。仅保留 `name`, `version`, `license`, `dist.tarball`, `dist.shasum`, `publish_time`。
     - **再分发依据**: 事实性元数据极小片段，用于技术可重现验证之合理使用。
     - **授权状态**: **待办**（需确认 GitHub/npm 对脱机包元数据的再分发细则）。
  2. **Source: `deps_dev`**
     - **端点**: `https://api.deps.dev/v3/systems/npm/packages/debug/versions/4.3.4`
     - **HTTP 状态**: `200 OK`
     - **来源许可/条款**: Google APIs Terms of Service / deps.dev Terms。
     - **署名要求**: 署名 "Open Source Insights (deps.dev)"。
     - **裁剪说明**: 剔除了数百个传递依赖节点、完整 SLSA 溯源图与安全公告大列表，仅保留 `versionKey`, `publishedAt`, `licenses`, `links` 4 个核心字段。
     - **再分发依据**: 转化性合理使用（Transformative Fair Use）。
     - **授权状态**: **待办**（尚未获得 Google 官方对离线数据再分发的书面豁免或许可）。
  3. **Source: `clearlydefined`**
     - **端点**: `https://api.clearlydefined.io/definitions/npm/npmjs/-/debug/4.3.4`
     - **HTTP 状态**: `0` (采集时发生超时网络异常 `Read timed out`)
     - **来源许可/条款**: CC0（若成功响应）。
     - **署名要求**: 署名 ClearlyDefined (OSI/LF)。
     - **裁剪说明**: 仅记录网络错误体，未载入外部版权数据。
     - **再分发依据**: 错误日志不构成第三方版权客体。
     - **授权状态**: **已具备**（无第三方受保护内容）。

---

### 2.2 `evidence/snapshots/pkg-npm-esprima-4.0.1.json`

- **软件包坐标**: `pkg:npm/esprima@4.0.1` (Ecosystem: npm)
- **采集时间戳 (`fetch_timestamp`)**: `2026-10-13T06:31:25Z`
- **人工/合成属性**: `synthetic: false` (真实案例，语义差异 `SEMANTIC_DIVERGENCE`)
- **逐项来源明细**:
  1. **Source: `registry`**
     - **端点**: `https://registry.npmjs.org/esprima/4.0.1`
     - **HTTP 状态**: `200 OK`
     - **来源许可/条款**: npm Terms of Use (GitHub)。
     - **署名要求**: 标明源自 npm registry。
     - **裁剪说明**: 剥离了 README 全文、历史版本树与个人邮箱，仅保留 `name`, `version`, `license: "BSD-2-Clause"`, `dist`, `publish_time`。
     - **再分发依据**: 事实性元数据微量提取（Fair Use）。
     - **授权状态**: **待办**（正式分发资质待办审查）。
  2. **Source: `deps_dev`**
     - **端点**: `https://api.deps.dev/v3/systems/npm/packages/esprima/versions/4.0.1`
     - **HTTP 状态**: `200 OK`
     - **来源许可/条款**: Google APIs Terms of Service。
     - **署名要求**: 署名 "Open Source Insights (deps.dev)"。
     - **裁剪说明**: 剥离全量依赖拓扑与 SLSA 证据链，仅保留 `versionKey`, `publishedAt`, `licenses: ["BSD-2-Clause"]`。
     - **再分发依据**: 极小测试集转化性引用。
     - **授权状态**: **待办**（Google 官方再分发许可未封闭）。
  3. **Source: `clearlydefined`**
     - **端点**: `https://api.clearlydefined.io/definitions/npm/npmjs/-/esprima/4.0.1`
     - **HTTP 状态**: `200 OK`
     - **来源许可/条款**: **CC0**。
     - **署名要求**: 建议署名 ClearlyDefined（CC0 不强制要求署名，但保留来源链接）。
     - **裁剪说明**: 剥离了庞大的 ScanCode 原始逐行扫描 AST、50+ 文件级切面细节与内部评分，仅保留核心许可声明 `declared: "BSD-2-Clause AND BSD-3-Clause"` 与 `facets.core.discovered.expressions`。
     - **再分发依据**: CC0 公有领域奉献允许自由复制与再分发。
     - **授权状态**: **已具备**（条款明确许可，需执行署名归档）。

---

### 2.3 `evidence/snapshots/pkg-npm-synthetic-fixture-1.0.0.json`

- **软件包坐标**: `pkg:npm/synthetic-fixture@1.0.0` (Ecosystem: npm)
- **采集时间戳 (`fetch_timestamp`)**: `2026-10-13T06:00:00Z`
- **人工/合成属性**: `synthetic: true` (合成插桩案例，摘要冲突 `DIGEST_CONFLICT`)
- **逐项来源明细**:
  1. **Source: `registry`**
     - **端点**: `https://registry.npmjs.org/synthetic-fixture/1.0.0` (模拟端点)
     - **HTTP 状态**: `200 OK`
     - **来源许可/条款**: Apache-2.0 (项目自主构造)。
     - **署名要求**: CodeSupply PMV 原创。
     - **裁剪说明**: 无裁剪，直接生成结构化最小测试数据（sha256 `aaa...`）。
     - **再分发依据**: 项目自主知识产权。
     - **授权状态**: **已具备**。
  2. **Source: `synthetic`**
     - **端点**: `https://mirror.example.org/synthetic-fixture-1.0.0.tgz` (模拟镜像)
     - **HTTP 状态**: `200 OK`
     - **来源许可/条款**: Apache-2.0 (项目自主构造)。
     - **署名要求**: 无。
     - **裁剪说明**: 纯测试桩，包含冲突摘要（sha256 `bbb...`）。
     - **再分发依据**: 项目自主知识产权。
     - **授权状态**: **已具备**。

---

### 2.4 `evidence/snapshots/pkg-pypi-archgraph-layout-2.3.0.json`

- **软件包坐标**: `pkg:pypi/archgraph-layout@2.3.0` (Ecosystem: PyPI)
- **采集时间戳 (`fetch_timestamp`)**: `2026-10-13T06:31:25Z`
- **人工/合成属性**: `synthetic: false` (真实案例，维持 `suspect`/`retracted` 撤回状态，判定 `INDETERMINATE`)
- **逐项来源明细**:
  1. **Source: `registry`**
     - **端点**: `https://pypi.org/pypi/archgraph-layout/2.3.0/json`
     - **HTTP 状态**: `200 OK`
     - **来源许可/条款**: PSF Terms of Use。
     - **署名要求**: 标注源自 Python Package Index。
     - **裁剪说明**: 剔除了作者邮箱、README 文本、其他历史版本列表；仅保留 `info.name`, `info.version`, `releases["2.3.0"]`。
     - **再分发依据**: 纯技术元数据事实。
     - **授权状态**: **待办**（需核实 PSF 官方公开元数据镜像政策）。
  2. **Source: `deps_dev`**
     - **端点**: `https://api.deps.dev/v3/systems/pypi/packages/archgraph-layout/versions/2.3.0`
     - **HTTP 状态**: `404 Not Found`
     - **来源许可/条款**: Google APIs Terms of Service。
     - **署名要求**: 署名 "Open Source Insights (deps.dev)"。
     - **裁剪说明**: 仅记录 404 错误主体 `body: "version not found"`。
     - **再分发依据**: 错误报文技术事实。
     - **授权状态**: **待办**（Google ToS 离线数据再分发正式确认待办）。
  3. **Source: `clearlydefined`**
     - **端点**: `https://api.clearlydefined.io/definitions/pypi/pypi/-/archgraph-layout/2.3.0`
     - **HTTP 状态**: `200 OK`
     - **来源许可/条款**: **CC0**。
     - **署名要求**: 署名 ClearlyDefined。
     - **裁剪说明**: 剥离非核心扫描树，仅保留 `licensed.declared: null`。
     - **再分发依据**: CC0。
     - **授权状态**: **已具备**。

---

### 2.5 `evidence/snapshots/pkg-pypi-typing-extensions-4.12.2.json`

- **软件包坐标**: `pkg:pypi/typing-extensions@4.12.2` (Ecosystem: PyPI)
- **采集时间戳 (`fetch_timestamp`)**: `2026-10-13T06:31:23Z`
- **人工/合成属性**: `synthetic: false` (真实案例，标准脱节 `STANDARDS_CONTRADICTION`)
- **逐项来源明细**:
  1. **Source: `registry`**
     - **端点**: `https://pypi.org/pypi/typing-extensions/4.12.2/json`
     - **HTTP 状态**: `200 OK`
     - **来源许可/条款**: PSF Terms of Use。
     - **署名要求**: 标注源自 Python Package Index。
     - **裁剪说明**: 剥离长描述文本、邮箱；仅保留 `info.license: null`（实测三源均为 null，非 PSF-2.0）, `info.classifiers` (License 条目), `releases["4.12.2"]` 的制品摘要与上传时间。
     - **再分发依据**: 事实性技术元数据。
     - **授权状态**: **待办**（PSF 离线元数据再分发条款待办确认）。
  2. **Source: `deps_dev`**
     - **端点**: `https://api.deps.dev/v3/systems/pypi/packages/typing-extensions/versions/4.12.2`
     - **HTTP 状态**: `200 OK`
     - **来源许可/条款**: Google APIs Terms of Service。
     - **署名要求**: 署名 "Open Source Insights (deps.dev)"。
     - **裁剪说明**: 剥离依赖网络，保留 `licenses: ["non-standard"]`, `links`, `publishedAt`。
     - **再分发依据**: 转化性技术引用。
     - **授权状态**: **待办**（需向 deps.dev 沟通离线基准测试集再分发白名单）。
  3. **Source: `clearlydefined`**
     - **端点**: `https://api.clearlydefined.io/definitions/pypi/pypi/-/typing-extensions/4.12.2`
     - **HTTP 状态**: `200 OK`
     - **来源许可/条款**: **CC0**。
     - **署名要求**: 署名 ClearlyDefined (OSI/LF)。
     - **裁剪说明**: 裁剪数百个代码扫描切面，保留顶层 `declared: "Python-2.0.1"` 与核心切面汇总表达式。
     - **再分发依据**: CC0。
     - **授权状态**: **已具备**。

---

## 3. 补充案例 (`evidence/supplementary/`) 再分发属性说明

| 补充快照文件 | 包含端点 | 裁剪说明 | 当前再分发依据与待办状态 |
|---|---|---|---|
| `snapshot-pkg-pypi-hatch-vcs-0.4.0.json` | PyPI JSON, deps.dev v3, ClearlyDefined | 剔除 README、作者信息与依赖树，仅保留 URL/Links/License 核心对比字段 | **待办**：PyPI/deps.dev 官方离线再分发条款待办核实；ClearlyDefined 为 CC0 已具备。 |
| `snapshot-pkg-pypi-validfilepath-0.1.json` | PyPI JSON, deps.dev v3, ClearlyDefined | 同上，剔除长文本与非目标版本 | **待办**：同上；且历史 404 瞬态数据受限于当时记录，非全量抓包。 |
| `snapshot-pkg-pypi-django-flowcontrol-0.0.21.json` | PyPI JSON, deps.dev v3, ClearlyDefined | 同上，三方皆空字段极小保留 | **待办**：同上；纯事实空值数据不具独创性版权。 |

---

## 4. 全局合规审查待办事项清单 (Consolidated To-Do List)

按照 Astra 终审意见第 7 项，**拿不到的信息必须如实列入待办，绝不写成“已具备”**：

1. **[待办 1 · deps.dev] Google API 离线基准数据集再分发许可确认**：
   - 现状：现有快照依据 Fair Use 裁剪为极小片段，但 Google APIs ToS 缺少针对第三方开源项目长期离线打包再分发的明文许可。
   - 动作：在里程碑 M1 阶段，向 deps.dev 官方团队正式发函/开 Issue 咨询并确认其公开 API 导出用于开源基准测试套件（Benchmark Suite）的再分发授权政策。
2. **[待办 2 · PyPI] PSF Warehouse 纯元数据离线分发政策核定**：
   - 现状：PyPI 网页与 API 依赖 PSF 服务条款，缺少类似 CC0 的显式数据版权标识。
   - 动作：核查 Python 官方 PSF 法律委员会关于 PyPI 镜像及元数据存档公开分发的官方立场文件。
3. **[待办 3 · npm] GitHub/npm Terms of Service 外部镜像与脱机数据集条款**：
   - 现状：npm 仅提供公共 API 访问权限，未对第三方仓库内打包 registry packuments 片段提供格式化再分发授权声明。
   - 动作：核对 GitHub Acceptable Use Policies 与 npm Open Source Terms 中的非商业性技术验证豁免范围。
4. **[待办 4 · ClearlyDefined] 统一法律署名规范落地**：
   - 现状：CC0 公有领域奉献，再分发无署名强制要求。
   - 动作：保留 ClearlyDefined 来源链接（建议性署名）。
