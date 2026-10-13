# 独立复跑署名记录（Independent Rerun Attestation）

- **复跑人**：孔明（dsh 执行岗，Muse 代理）
- **与项目关系**：PMV 代码实现者为 Gemini（dsh --profile gemini-sub，按任务书执行）；复跑人未参与代码实现，仅负责任务下达、验收与证据核验。**独立性说明**：复跑人与实现者为不同执行主体；但同属申请人 AI 团队，评审方可视需要要求第三方复跑。
- **复跑 commit**：`a26830d`（https://github.com/yijigao/pkgmeta-verify/commit/a26830d）
- **干净环境**：全新 `git clone`（/tmp/indep-rerun），独立 Python venv，未复用实现环境的任何缓存/依赖。
- **依赖版本**：jsonschema==4.26.0、jsonschema-specifications==2025.9.1、requests==2.34.2、urllib3==2.8.0；Python 3.12.3；Linux 7.0.0-39-generic。
- **命令**：
  1. `./venv/bin/python -m unittest discover -s tests` → Ran 56 tests, OK
  2. `PATH=/tmp/indep-rerun/venv/bin:$PATH bash rerun.sh` → RERUN_EXIT=0
- **原始日志**：`/tmp/indep-rerun/tests.log`（实现环境日志）、`/tmp/indep-rerun/rerun.log`（本机日志；关键行摘录如下）
- **复跑结果**：56/56 测试通过；5/5 基线案例离线复跑字节级一致、Schema 校验通过。
- **结论口径**：现有测试零失败（56/56），PMV 为概念验证。
- **日期**：2026-10-13 18:0x CST（UTC+8）

## rerun.log 关键行
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
