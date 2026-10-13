# 独立复跑署名记录（Independent Rerun Attestation）

- **复跑人**：孔明（dsh 执行岗，Muse 代理）
- **与项目关系**：PMV 代码实现者为 Gemini（dsh --profile gemini-sub，按任务书执行）；复跑人未参与代码实现，仅负责任务下达、验收与证据核验。**独立性说明**：复跑人与实现者为不同执行主体；但同属申请人 AI 团队，评审方可视需要要求第三方复跑。
- **复跑 commit**：`d2f7995`（https://github.com/yijigao/pkgmeta-verify/commit/d2f7995）
- **干净环境**：全新 `git clone`，独立 Python venv，未复用实现环境的任何缓存/依赖。
- **依赖版本**：jsonschema==4.26.0、jsonschema-specifications==2025.9.1、requests==2.34.2、urllib3==2.8.0；Python 3.12.3；Linux 7.0.0-39-generic。

## 复跑尝试记录（两次都保留）

### 尝试 1（失败）— independent-tests-attempt1-failed.log
- 时间：2026-10-13 17:58–18:00 CST
- 命令：`./venv/bin/python -m unittest discover -s tests`
- 结果：Ran 53 tests，FAILED (errors=1) —— 原因：干净 venv 未安装 `jsonschema`，test_schema 模块导入失败。属环境缺件，非代码问题。
- 处置：安装 jsonschema==4.26.0 后重跑。

### 尝试 2（成功）— independent-tests-success.log
- 时间：2026-10-13 18:06:08Z–18:06:09Z（北京时间 18:06）
- 命令：
  1. `./venv/bin/python -m unittest discover -s tests` → Ran 56 tests, OK
  2. `PATH=.../venv/bin:$PATH bash rerun.sh` → RERUN_EXIT=0（日志见 independent-rerun.log）
- 复跑结果：56/56 测试通过；5/5 基线案例离线复跑字节级一致、Schema 校验通过。

## rerun 关键行
```
Rerunning pkg:pypi/typing-extensions@4.12.2 ... PASS (0 diff, Schema VALID)
Rerunning pkg:pypi/archgraph-layout@2.3.0 ... PASS (0 diff, Schema VALID)
Rerunning pkg:npm/esprima@4.0.1 ... PASS (0 diff, Schema VALID)
Rerunning pkg:npm/debug@4.3.4 ... PASS (0 diff, Schema VALID)
Rerunning pkg:npm/synthetic-fixture@1.0.0 ... PASS (0 diff, Schema VALID)
Test Result: 现有测试零失败 (0 failures)
Passed Cases: 5/5
RERUN_EXIT=0
```

- **结论口径**：现有测试零失败（56/56），PMV 为概念验证。
