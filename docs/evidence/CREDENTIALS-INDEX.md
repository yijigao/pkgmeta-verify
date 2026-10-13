# 履历索引（Credentials Index）— Jigao Yi

> 用途：NLnet CodeSupply 申请 "unique technical expertise" 论证的证据索引。
> 口径：只写本人实际贡献与验证范围，不冒领、不推广。

## 1. dsh 定制补丁（LLM agent 协议层故障定位与修复）
- **主张**：独立定位并修复 DeepSeek 开源项目 dsh 的 out-of-tree LLM adapter 三处协议/重试缺陷。
- **证据**：`docs/evidence/dsh-patches.md` ＋ `docs/evidence/diffs/`（4 个 diff，SHA-256 见索引）。
- **验证范围**：补丁 diff＋回归记录（多步工具调用 9.7–11.3s PASS）。dsh 本体为 DeepSeek 官方项目、`dsh-llm-antigravity@0.1.0` 为第三方适配器——均非本人作品，只主张补丁本身。
- **fork**：https://github.com/yijigao/deepseek-harness

## 2. MEC（Market Evidence Check）公开项目
- **主张**：可运行的 AI 工具真实分发验证实验项目。
- **证据**：https://github.com/yijigao/market-evidence-check-devday（代码、规则、测试记录）。
- **验证范围**：见仓库内记录。

## 3. 外部独立安装验证（terramike）
- **主张**：陌生人独立安装并通过三项 smoke checks。
- **证据**：https://github.com/terramike/xrpl-muse-skill/issues/8#issuecomment-6109879435
- **验证范围**：验证的是 `muse.md＋OpenAPI` 生成可复用只读 skill 的路径；**不**证明 PR 内 catalog 安装路径或 CLI 已外部验证；只支持"一次外部安装及 smoke 验证"，不支持持续使用或生产成熟度。

## 4. awesome-muse-connectors PR #228
- **主张**：PR 描述、评论、`SKILL.md` 已按终审口径更新并推送。
- **证据**：https://github.com/Anil-matcha/awesome-muse-connectors/pull/228（含评论留痕 #issuecomment-6139970305）
- **验证范围**：PR 描述更新为事实口径；不主张合并或采用。

## 5. AboutCode 技术对齐（purl-validator#39）
- **主张**：已发起技术对齐（2026-10-13）。
- **证据**：https://github.com/aboutcode-org/purl-validator/issues/39
- **验证范围**：只写"已发起技术对齐"，不写获认可。archgraph-layout 案例已发纠正评论（#issuecomment-6140484558），降级为 suspect/retracted。

## 6. PMV 本题（概念验证）
- **主张**：可运行的包元数据质检组件原型。
- **证据**：本仓库（56/56 回归测试、5/5 基线复跑、证据包）。
- **验证范围**：现有测试零失败（56/56），PMV 为概念验证；不宣称覆盖全部误判或判定绝对正确。

---
*维护人：Jigao Yi ｜ 更新：2026-10-13*
