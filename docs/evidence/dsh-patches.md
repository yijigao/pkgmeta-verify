# dsh 定制补丁索引（本人贡献证据）

申请人 Jigao Yi 对 DeepSeek 开源项目 dsh 的本地定制补丁。dsh 本体为 DeepSeek 官方项目，申请人仓库为 fork：https://github.com/yijigao/deepseek-harness（**不把整套 dsh 当原创**；以下仅列本人改动）。

> 说明：以下补丁作用于 dsh 的 out-of-tree LLM adapter（第三方 npm 包 `dsh-llm-antigravity@0.1.0` 的 vendored 副本），不在上游 dsh 仓库内；故以补丁 diff 文件 + SHA-256 + 回归记录为证据。diff 原文见 `diffs/` 目录。

## 补丁 1：多步工具调用协议修复（2026-10-02）
- **diff**：`diffs/20261002-wire.js.diff`（SHA-256: df960c59fc6032c76a5f21133a6645c2941b58160f7c900b7000b16aff337cf8）
- **改动**：归一化 dsh 0.2 的 `role:"tool"` 工具结果（旧适配器只认 `role:"user"+tool-result`，会把工具输出当 model turn 发给上游，导致 `400 Requests ending with a model turn are not supported.`）。
- **回归验证**：多步只读任务 33 秒 exit 0，统计数字 42 与手工 grep 一致；Gemini 回归 9.7 秒 PASS。

## 补丁 2：429 重试策略（2026-10-02）
- **diff**：`diffs/20261002-adapter.js.diff`（SHA-256: a6acf780da592aa44fb5dd1b351c9ece9cd3206603a0df2a6354838bbdc8af17）、`diffs/20261002-index.js.diff`（SHA-256: 699a2632bd7c181615f83f54a36128d3607f76515a3aa12613fed327a553b056）
- **改动**：429 指数退避（5s→10s→20s→40s→60s，5 次，带 jitter）；429 不再切 endpoint 或回退到 `gemini-3.7-flash-medium`（原内置版本回退是误导性表象）。

## 补丁 3：Claude thinking signature 回放修复（2026-10-06，三 profile 同步）
- **diff**：`diffs/20261006-claude-wire.diff`（SHA-256: 084d8862451fff0c2af704eb9c53cd5fe2c80a22c27f14f07adca43ff1b14b45）
- **改动**：SSE assembler 只收集 Claude `thoughtSignature` 但不 emit `replayState`，回放时 thought 块无 signature 被上游以 `thinking.signature: Field required` 400 拒绝（被 endpoint 回退掩盖成 429）。修复：finish 时 emit replayState；无签名 Claude reasoning 直接丢弃；小 maxTokens 时关 thinking。
- **回归验证**：Sonnet 工具两步 9.9s、Opus 11.3s、Gemini 回归 9.7s 均 PASS。

## 第三方来源说明（单独归档）
- 被补丁的基座：第三方 npm 包 `dsh-llm-antigravity@0.1.0`（社区适配器，非本人作品）。
- dsh 本体：DeepSeek 官方开源项目；本人 fork 仅用于承载上述本地补丁的版本管理。
- 故障定位方法论：给 adapter 加 env 门控的逐 endpoint status/body 日志，不只看最终抛出的错误（曾用此法定位 400 被 endpoint 回退掩盖成 429 的两起事故）。
