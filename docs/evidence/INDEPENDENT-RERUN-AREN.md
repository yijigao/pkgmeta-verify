# 独立复跑记录（阿仁执行）

- **执行人**：阿仁（主聊侧 AI 代理）
- **与项目关系**：未参与实现。代码由 Gemini 实现、孔明（dsh 执行岗）组织；本人仅做独立复跑与记录。
- **同属关系声明**：本人与实现者同属申请人 Jigao Yi 的 AI 团队，非外部第三方。评审方可要求外部第三方复跑。
- **复跑时间**：2026-10-13 约 18:10–18:15（北京时间）
- **仓库**：https://github.com/yijigao/pkgmeta-verify
- **commit**：c5fe6f62b667bb1bf4a270bfd499616d611fd9e5（main 分支最新）
- **环境**：全新 git clone（/tmp/pmv-independent-rerun-aren/repo），新建独立 venv
- **依赖版本**：
  - jsonschema==4.26.0
  - jsonschema-specifications==2025.9.1
  - pytest==9.1.1
  - requests==2.34.2
  - urllib3==2.8.0

## 执行命令

```
git clone https://github.com/yijigao/pkgmeta-verify.git repo
python3 -m venv venv
./venv/bin/pip install requests urllib3 jsonschema pytest
./venv/bin/python -m pytest tests/ -v
bash rerun.sh
```

## 结果

1. **回归测试**：56/56 通过（0.28s），原始日志见 pytest-full.log。
2. **基线复跑**：5/5 案例字节级一致、Schema VALID，原始日志见 rerun-full.log。
3. **发现的问题（诚实记录）**：
   - `rerun.sh` Phase 1 报告 `schemas/pmv-output.schema.json: FAILED`——MANIFEST.sha256 中的哈希（b7d647ea…）与当前文件实际哈希（7a72b4df…）不符。
   - 原因：6545bc4 提交把 Schema `$id` 改成了版本化 raw URL，但 MANIFEST.sha256 未同步更新，为过期值。
   - 其余 11 个文件哈希全部匹配；Phase 2–4 全部通过。
   - 该问题不影响判定正确性，但 manifest 已过期，须重新生成 MANIFEST.sha256 后再冻结基线。

## 结论

- 现有测试零失败（56/56），基线复跑 5/5 字节一致——与团队自报一致。
- 但 MANIFEST.sha256 已过期（schema $id 变更未同步），须修复后重新冻结基线。本次复跑不能作为"全部检查通过"的证据，只能作为"测试与复跑通过、manifest 待更新"的记录。
