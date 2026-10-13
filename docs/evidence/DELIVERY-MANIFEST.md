# 交付清单（Delivery Manifest）

- **交付版本**：`956cec4`（main 分支）＋ tag `v0.1`（Schema $id 指向版本）
- **交付目录**：https://github.com/yijigao/pkgmeta-verify（公开仓库，免登录可读）
- **清单生成时间**：2026-10-13（UTC+8）；共 117 个文件
- **修改规则**：每个文件同时只允许一个修改者；冻结文件（已冻结）不得修改，改则重新走验收
- **排除范围**：仓库内无重复目录（examples/integration/integration/ 已删除）；/tmp 中转目录不属于交付

| # | 文件路径 | 用途 | 字节数 | SHA-256（git blob） |
|---|---|---|---:|---|
| 1 | `docs/evidence/prompts-reconstructed/01-adjudication-1346.md` | GenAI 过程归档（prompt/未编辑输出） | 2218 | `01d30335f4617149…` |
| 2 | `pmv/__init__.py` | PMV 实现代码（已冻结） | 803 | `02044242e589b788…` |
| 3 | `docs/evidence/prompts/TASK-EVIDENCE-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 1726 | `05f2ab9afafaa922…` |
| 4 | `docs/evidence/outputs/taskA-deepseek.txt` | GenAI 过程归档（prompt/未编辑输出） | 27111 | `09f70e6034a92ba6…` |
| 5 | `evidence/supplementary/snapshot-pkg-pypi-hatch-vcs-0.4.0.json` | 补充证据（不在冻结基线内） | 5498 | `0f2d492c745819f5…` |
| 6 | `docs/evidence/diffs/20261002-wire.js.diff` | 申请人 dsh 补丁证据 | 1457 | `116b790ee2812bde…` |
| 7 | `tests/test_verifier_rules.py` | 回归测试（已冻结） | 73197 | `11a22bfacccb94ea…` |
| 8 | `rerun.sh` | 复跑程序与报告 | 14523 | `173b58b56bb97012…` |
| 9 | `docs/evidence/diffs/20261006-claude-wire.diff` | 申请人 dsh 补丁证据 | 2659 | `180902e01ead4ca3…` |
| 10 | `evidence/cases.md` | 证据分析报告 | 3668 | `1abf1280b991131d…` |
| 11 | `docs/evidence/CREDENTIALS-INDEX.md` | 履历索引 | 2321 | `1b1b40b4b23997b8…` |
| 12 | `docs/evidence/outputs/pmv-fix2-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 18447 | `1d8426c74c488e38…` |
| 13 | `docs/evidence/outputs/taskB-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 21033 | `1de9d26b2267e29a…` |
| 14 | `evidence/snapshots/pkg-pypi-typing-extensions-4.12.2.json` | 冻结基线快照/结果（12 文件） | 5019 | `1e397340a9d9bc55…` |
| 15 | `docs/evidence/outputs/ASTRA-REV3FIX2-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 4305 | `1feef60d4e675d54…` |
| 16 | `docs/evidence/outputs/realerror-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 4885 | `24e7a5f5f9438789…` |
| 17 | `docs/evidence/independent-tests-success.log` | 独立复跑记录 | 374 | `28b7afb3a62d3ed5…` |
| 18 | `docs/evidence/outputs/outline-rev3-sol.txt` | GenAI 过程归档（prompt/未编辑输出） | 26537 | `2aaaf836ff5a9c38…` |
| 19 | `docs/evidence/outputs/gates-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 10588 | `2b3072912f588961…` |
| 20 | `evidence/natural-undecidable-case.md` | 证据分析报告 | 5557 | `2c4d6ce4f29874ab…` |
| 21 | `docs/evidence/outputs/ASTRA-PROPOSAL-FINAL2-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 3393 | `2d80e6a943f26a08…` |
| 22 | `pmv/collector.py` | PMV 实现代码（已冻结） | 8827 | `2e424f595189e9b7…` |
| 23 | `docs/evidence/rerun-full.log` | 独立复跑记录 | 1866 | `2fc5840641b7eb5a…` |
| 24 | `docs/evidence/PROPOSAL-DRAFT.md` | 提案正文草稿（待 Joey 定稿） | 22671 | `33e6b64b0025640a…` |
| 25 | `evidence/supplementary/pkg-pypi-validfilepath-0.1.raw.json` | 补充证据（不在冻结基线内） | 14278 | `398b45fcca2e8a2d…` |
| 26 | `docs/evidence/outputs/astra-draft.txt` | GenAI 过程归档（prompt/未编辑输出） | 5090 | `3c803ece522c1340…` |
| 27 | `docs/evidence/outputs/deepseek-draft.txt` | GenAI 过程归档（prompt/未编辑输出） | 7922 | `3f631eade0ff18fd…` |
| 28 | `evidence/supplementary/result-pkg-pypi-hatch-vcs-0.4.0.json` | 补充证据（不在冻结基线内） | 5254 | `3f729d84e243081a…` |
| 29 | `evidence/supplementary/pkg-pypi-django-flowcontrol-0.0.21.raw.json` | 补充证据（不在冻结基线内） | 13691 | `3fe5079cae455ce1…` |
| 30 | `pmv/cli.py` | PMV 实现代码（已冻结） | 5569 | `411a2a9f71ffaf87…` |
| 31 | `schemas/pmv-output.schema.json` | 输出 Schema（已冻结） | 4087 | `438cd44a6ba8a751…` |
| 32 | `tests/__init__.py` | 回归测试（已冻结） | 82 | `441f3e3837193c54…` |
| 33 | `docs/evidence/prompts-reconstructed/00-README.md` | GenAI 过程归档（prompt/未编辑输出） | 612 | `46050056d79075e3…` |
| 34 | `docs/evidence/prompts/TASK-A2-revise.md` | GenAI 过程归档（prompt/未编辑输出） | 2579 | `471a819c9ce61cec…` |
| 35 | `docs/evidence/independent-tests-attempt1-failed.log` | 独立复跑记录 | 1170 | `52b7051555ad3937…` |
| 36 | `docs/evidence/prompts/TASK-GATES-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 1958 | `54375aaa64c735c3…` |
| 37 | `evidence/supplementary/pkg-pypi-hatch-vcs-0.4.0.raw.json` | 补充证据（不在冻结基线内） | 31337 | `5667863ff1841909…` |
| 38 | `docs/evidence/prompts-reconstructed/05-rev3fix-1541.md` | GenAI 过程归档（prompt/未编辑输出） | 2025 | `566dcc740f30756f…` |
| 39 | `docs/evidence/INDEPENDENT-RERUN-AREN.md` | 独立复跑记录 | 2106 | `5a99a7a9177c3ed6…` |
| 40 | `docs/evidence/outputs/outline-rev2-sol.txt` | GenAI 过程归档（prompt/未编辑输出） | 20941 | `5c2a3c3eb00727b1…` |
| 41 | `pmv/exporter.py` | PMV 实现代码（已冻结） | 9721 | `5c6bbe7371c1cec9…` |
| 42 | `docs/evidence/diffs/20261002-index.js.diff` | 申请人 dsh 补丁证据 | 1392 | `5dda8996e1d3d41e…` |
| 43 | `evidence/results/pkg-npm-synthetic-fixture-1.0.0.result.json` | 冻结基线快照/结果（12 文件） | 4694 | `67892ae11eca2c6f…` |
| 44 | `LICENSE` | Apache-2.0 许可 | 10761 | `6840d8290540d549…` |
| 45 | `docs/evidence/outputs/ASTRA-PROPOSAL-FINAL-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 5285 | `6facc3f8f11b5687…` |
| 46 | `docs/evidence/prompts/TASK-REALERROR-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 1451 | `72287958d303db9b…` |
| 47 | `docs/evidence/prompts-reconstructed/07-rev3fix3-1733.md` | GenAI 过程归档（prompt/未编辑输出） | 2222 | `73e214784a4180f8…` |
| 48 | `evidence/supplementary/result-pkg-pypi-django-flowcontrol-0.0.21.json` | 补充证据（不在冻结基线内） | 5351 | `76e869af5b18a491…` |
| 49 | `evidence/MANIFEST.sha256` | 冻结基线清单 | 1306 | `78b775f9160c5b07…` |
| 50 | `evidence/results/pkg-npm-debug-4.3.4.result.json` | 冻结基线快照/结果（12 文件） | 4437 | `7a708de83716da13…` |
| 51 | `evidence/snapshots/pkg-pypi-archgraph-layout-2.3.0.json` | 冻结基线快照/结果（12 文件） | 2553 | `7c5d69cfab23f859…` |
| 52 | `docs/evidence/outputs/ASTRA-REV3FIX-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 4424 | `802fed14ce888a2e…` |
| 53 | `docs/evidence/outputs/pmv-fix-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 9144 | `80c089c7e7556d55…` |
| 54 | `docs/evidence/outputs/pmv-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 10258 | `81e6906f90279d6a…` |
| 55 | `docs/evidence/outputs/ASTRA-REV3FIX3-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 3342 | `82702195adc6f589…` |
| 56 | `docs/evidence/outputs/ASTRA-REV3-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 3639 | `84a30bcb6a3326ba…` |
| 57 | `docs/evidence/outputs/ASTRA-REV1-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 5267 | `86fe1c0bdab302a6…` |
| 58 | `docs/evidence/GENAI-DISCLOSURE-DRAFT.md` | GenAI 披露草稿（据实版） | 2482 | `8801c5a78000895a…` |
| 59 | `bin/pkgmeta-verify` | 复跑程序与报告 | 869 | `898c267073d300b7…` |
| 60 | `docs/evidence/outputs/demo-rev1-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 30903 | `8a4b726fb9eb07bb…` |
| 61 | `docs/evidence/outputs/evidence-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 7912 | `8b28d5acaad8337b…` |
| 62 | `docs/evidence/outputs/ASTRA-REV2-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 6033 | `8cff4e79fab5dd6b…` |
| 63 | `docs/evidence/prompts/TASK-PMV-FIX4-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 4314 | `907e55ddc0feac2b…` |
| 64 | `docs/evidence/outputs/ASTRA-SWEEP1-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 6124 | `91777c14f09a1a53…` |
| 65 | `evidence/supplementary/snapshot-pkg-pypi-django-flowcontrol-0.0.21.json` | 补充证据（不在冻结基线内） | 4706 | `9275d7ae8e8b8c3a…` |
| 66 | `evidence/real-error-case-v2.md` | 证据分析报告 | 14347 | `95da9dfc2ea99ac3…` |
| 67 | `docs/evidence/prompts-reconstructed/08-final-1757.md` | GenAI 过程归档（prompt/未编辑输出） | 2082 | `962f7ec55feeaf86…` |
| 68 | `docs/evidence/prompts/TASK-A-deepseek.md` | GenAI 过程归档（prompt/未编辑输出） | 2354 | `996b8e8f1909c505…` |
| 69 | `run_harvest.py` | 复跑程序与报告 | 6340 | `9bfbbc61822e7683…` |
| 70 | `docs/evidence/prompts/TASK-PMV-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 2956 | `9e3bc737d618908d…` |
| 71 | `evidence/supplementary/README.md` | 补充证据（不在冻结基线内） | 8180 | `9ea7ea6c2e584c3d…` |
| 72 | `docs/evidence/INDEPENDENT-RERUN.md` | 独立复跑记录 | 2202 | `a42b46d6f3046387…` |
| 73 | `docs/evidence/outputs/outline-rev1-deepseek.txt` | GenAI 过程归档（prompt/未编辑输出） | 30113 | `a4b3c262a74bb870…` |
| 74 | `docs/evidence/prompts/PROMPT-ENTRY4-RECONSTRUCTED.md` | GenAI 过程归档（prompt/未编辑输出） | 1966 | `a4e282674e18346c…` |
| 75 | `pmv/verifier.py` | PMV 实现代码（已冻结） | 81246 | `a63cfe0bbf3d1938…` |
| 76 | `evidence/supplementary/snapshot-pkg-pypi-validfilepath-0.1.json` | 补充证据（不在冻结基线内） | 4611 | `ab481a80af268b68…` |
| 77 | `docs/evidence/outputs/pmv-fix4-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 12498 | `adbb0c292805b537…` |
| 78 | `evidence/results/pkg-pypi-archgraph-layout-2.3.0.result.json` | 冻结基线快照/结果（12 文件） | 4642 | `ae0fcdd809251f72…` |
| 79 | `docs/evidence/prompts/TASK-REV2-deepseek.md` | GenAI 过程归档（prompt/未编辑输出） | 3570 | `b01f15a409799c50…` |
| 80 | `examples/integration/README.md` | 接入示例 | 9725 | `b0f09737f4d802ab…` |
| 81 | `docs/evidence/prompts/TASK.md` | GenAI 过程归档（prompt/未编辑输出） | 1919 | `b1b7bece5cff6a65…` |
| 82 | `evidence/snapshots/pkg-npm-synthetic-fixture-1.0.0.json` | 冻结基线快照/结果（12 文件） | 1861 | `b2a0340d52123d4b…` |
| 83 | `docs/evidence/prompts-reconstructed/06-rev3fix2-1610.md` | GenAI 过程归档（prompt/未编辑输出） | 2206 | `b39c12cd128b75a5…` |
| 84 | `docs/evidence/prompts/TASK-PMV-FIX2-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 3158 | `b725accfd86071a4…` |
| 85 | `docs/evidence/independent-rerun.log` | 独立复跑记录 | 1269 | `b72837c44f6f7747…` |
| 86 | `evidence/snapshots/pkg-npm-esprima-4.0.1.json` | 冻结基线快照/结果（12 文件） | 2926 | `bc552deccdc0e698…` |
| 87 | `docs/evidence/diffs/20261002-adapter.js.diff` | 申请人 dsh 补丁证据 | 8430 | `bcb9458ad1df6d37…` |
| 88 | `PROMPT-LOG.md` | Prompt  provenance 总日志 | 27127 | `bec4853dbd3d8110…` |
| 89 | `pmv/normalizer.py` | PMV 实现代码（已冻结） | 15952 | `c028fb3ab286c161…` |
| 90 | `rules/rules-v0.1.json` | 判定规则 v0.1（已冻结） | 2492 | `c189774d2d417657…` |
| 91 | `docs/evidence/README.md` | 说明文档 | 786 | `c67850846512f493…` |
| 92 | `rerun-report.md` | 复跑程序与报告 | 6790 | `c6c186f7f7125548…` |
| 93 | `tests/test_schema.py` | 回归测试（已冻结） | 3487 | `c79d03f2191c411e…` |
| 94 | `docs/evidence/outputs/gemini-draft.txt` | GenAI 过程归档（prompt/未编辑输出） | 7022 | `caf59ea80c1c3131…` |
| 95 | `docs/evidence/dsh-patches.md` | 申请人 dsh 补丁证据 | 2701 | `ce2383dc5005887c…` |
| 96 | `evidence/real-error-case.md` | 证据分析报告 | 9226 | `ce97a533833eb2ae…` |
| 97 | `evidence/results/pkg-pypi-typing-extensions-4.12.2.result.json` | 冻结基线快照/结果（12 文件） | 6040 | `d153ef79ab2c579c…` |
| 98 | `examples/integration/pipeline_demo.py` | 接入示例 | 16078 | `d5e8f9df5d79002c…` |
| 99 | `docs/evidence/outputs/ASTRA-ADJUDICATION-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 3647 | `d8d0482105ac2306…` |
| 100 | `README.md` | 说明文档 | 18039 | `d9a8f54ceb6b142f…` |
| 101 | `docs/evidence/outputs/pmv-fix3-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 8427 | `dd66c2cee12d6c10…` |
| 102 | `docs/evidence/outputs/ASTRA-FINAL-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 2194 | `de6cba0b675b7341…` |
| 103 | `docs/evidence/prompts/TASK-REV3-sol.md` | GenAI 过程归档（prompt/未编辑输出） | 3031 | `e2336ddda8e16f77…` |
| 104 | `evidence/supplementary/result-pkg-pypi-validfilepath-0.1.json` | 补充证据（不在冻结基线内） | 5221 | `e4238b820d299049…` |
| 105 | `evidence/snapshots/pkg-npm-debug-4.3.4.json` | 冻结基线快照/结果（12 文件） | 2363 | `e53c251e2e607462…` |
| 106 | `examples/integration/audit_pipeline_run.json` | 接入示例 | 5801 | `e7742725b387dec5…` |
| 107 | `docs/evidence/prompts-reconstructed/04-rev3-1509.md` | GenAI 过程归档（prompt/未编辑输出） | 2288 | `e860957f04bd3dc5…` |
| 108 | `docs/evidence/prompts/TASK-PMV-FIX-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 3296 | `e8c9294e34ebdf02…` |
| 109 | `docs/evidence/prompts/TASK-B2-revise.md` | GenAI 过程归档（prompt/未编辑输出） | 1984 | `ec512f644d86e9c8…` |
| 110 | `evidence/delay-chain.md` | 证据分析报告 | 6452 | `eddd13c84d2ea675…` |
| 111 | `docs/evidence/pytest-full.log` | 独立复跑记录 | 8048 | `ee30eef3eaf58587…` |
| 112 | `docs/evidence/prompts/TASK-PMV-FIX3-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 2927 | `f380a0d6fea435cc…` |
| 113 | `evidence/results/pkg-npm-esprima-4.0.1.result.json` | 冻结基线快照/结果（12 文件） | 5209 | `f540f33688ddfdf0…` |
| 114 | `evidence/redistribution-index.md` | 证据分析报告 | 14679 | `f67a6cf9f1b1c64d…` |
| 115 | `docs/evidence/prompts-reconstructed/03-rev2-1440.md` | GenAI 过程归档（prompt/未编辑输出） | 2244 | `f6f237f81a72f3d1…` |
| 116 | `docs/evidence/prompts/TASK-B-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 1738 | `f86a0c00baa35001…` |
| 117 | `docs/evidence/prompts-reconstructed/02-rev1-1404.md` | GenAI 过程归档（prompt/未编辑输出） | 2166 | `fa977fecaaf59016…` |
