# 交付清单（Delivery Manifest）

- **交付版本**：`ab931da46a1c52af2e2b7849847e536b96767f24`（main 分支；tag `v0.1` 指向 Schema $id 版本）
- **交付目录**：https://github.com/yijigao/pkgmeta-verify（公开仓库，免登录可读）
- **清单生成时间**：2026-10-13（UTC+8）；共 120 个文件（含本清单与主张登记表自身）
- **修改规则**：每个文件同时只允许一个修改者；冻结文件（已冻结）不得修改，改则重新走验收
- **排除范围**：仓库内无重复目录；/tmp 中转目录不属于交付
- **哈希说明**：SHA-256 为完整 40 位 git blob hash，可用 `git hash-object <文件>` 独立校验；本清单自身为自指文件，以交付版本 commit 保证完整性

| # | 文件路径 | 用途 | 字节数 | SHA-256（git blob，完整 40 位） |
|---|---|---|---:|---|
| 1 | `LICENSE` | Apache-2.0 许可 | 10761 | `6840d8290540d54980b272b08dfbcd84d527677f` |
| 2 | `PROMPT-LOG.md` | Prompt provenance 总日志 | 27871 | `9e16410193deef87b042049b959a4c71abe6f404` |
| 3 | `README.md` | 说明文档 | 18039 | `d9a8f54ceb6b142f1c10c8455c57d26d3b4f36ff` |
| 4 | `bin/pkgmeta-verify` | 复跑程序与报告 | 869 | `898c267073d300b75e96f2a45ece6e39e9fe4980` |
| 5 | `docs/evidence/CLAIM-REGISTRY.md` | 主张登记表 | 5199 | `d3d63d0fca13f35b4a3177cb79abda5a72d7d588` |
| 6 | `docs/evidence/CREDENTIALS-INDEX.md` | 履历索引 | 2321 | `1b1b40b4b23997b89aca10ea6375a23b0a348b6f` |
| 7 | `docs/evidence/DELIVERY-MANIFEST.md` | 交付清单（本文件；自指，见注） | 14952 | `自指（本文件）；完整性由交付版本 commit 保证` |
| 8 | `docs/evidence/GENAI-DISCLOSURE-DRAFT.md` | GenAI 披露草稿（据实版） | 2482 | `8801c5a78000895a92cec381c59205591296d617` |
| 9 | `docs/evidence/INDEPENDENT-RERUN-AREN.md` | 独立复跑记录 | 2106 | `5a99a7a9177c3ed6c7a4f2064b68ff1e83eb2f88` |
| 10 | `docs/evidence/INDEPENDENT-RERUN.md` | 独立复跑记录 | 2202 | `a42b46d6f3046387f21b940df11a80885b5e232a` |
| 11 | `docs/evidence/PROPOSAL-DRAFT.md` | 提案正文草稿（待 Joey 定稿） | 22671 | `33e6b64b0025640aa98885fa648e7b500b6dc5c8` |
| 12 | `docs/evidence/README.md` | 说明文档 | 786 | `c67850846512f493515b01be00d873f166d08df5` |
| 13 | `docs/evidence/diffs/20261002-adapter.js.diff` | 申请人 dsh 补丁证据 | 8430 | `bcb9458ad1df6d376103cac51c786ebde8c0fe55` |
| 14 | `docs/evidence/diffs/20261002-index.js.diff` | 申请人 dsh 补丁证据 | 1392 | `5dda8996e1d3d41e8ca4f2c4064ea19e5eb1afd0` |
| 15 | `docs/evidence/diffs/20261002-wire.js.diff` | 申请人 dsh 补丁证据 | 1457 | `116b790ee2812bde360d1db5f5a30b40f68fc720` |
| 16 | `docs/evidence/diffs/20261006-claude-wire.diff` | 申请人 dsh 补丁证据 | 2659 | `180902e01ead4ca3248efeb9695dd636c69365c8` |
| 17 | `docs/evidence/dsh-patches.md` | 申请人 dsh 补丁证据 | 2701 | `ce2383dc5005887c98f05e4a96e0fe36fe1c3d3e` |
| 18 | `docs/evidence/independent-rerun.log` | 独立复跑记录 | 1269 | `b72837c44f6f7747f8a220b7e3ed7ea8e387d8e0` |
| 19 | `docs/evidence/independent-tests-attempt1-failed.log` | 独立复跑记录 | 1170 | `52b7051555ad3937872cf82313431cbff5d889c5` |
| 20 | `docs/evidence/independent-tests-success.log` | 独立复跑记录 | 374 | `28b7afb3a62d3ed5f9b346d8679e69f04a3a2ec1` |
| 21 | `docs/evidence/outputs/ASTRA-ADJUDICATION-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 3647 | `d8d0482105ac23062d96ea269ae7330d46feffdf` |
| 22 | `docs/evidence/outputs/ASTRA-FINAL-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 2194 | `de6cba0b675b7341cb376ae67aa8a46f49381f62` |
| 23 | `docs/evidence/outputs/ASTRA-PROPOSAL-FINAL-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 5285 | `6facc3f8f11b568786eddd651fca4fc83b7f03cf` |
| 24 | `docs/evidence/outputs/ASTRA-PROPOSAL-FINAL2-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 3393 | `2d80e6a943f26a08f07a6d535f0e899e97994b92` |
| 25 | `docs/evidence/outputs/ASTRA-REV1-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 5267 | `86fe1c0bdab302a640f9937040826f3dbd40696f` |
| 26 | `docs/evidence/outputs/ASTRA-REV2-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 6033 | `8cff4e79fab5dd6b499ff5569cdd321ce4642c36` |
| 27 | `docs/evidence/outputs/ASTRA-REV3-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 3639 | `84a30bcb6a3326bae3481cb02a3c19ce11e21e0a` |
| 28 | `docs/evidence/outputs/ASTRA-REV3FIX-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 4424 | `802fed14ce888a2eeed21ec65765016108738787` |
| 29 | `docs/evidence/outputs/ASTRA-REV3FIX2-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 4305 | `1feef60d4e675d54c7c6bdfb9847cb7dc57ae62a` |
| 30 | `docs/evidence/outputs/ASTRA-REV3FIX3-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 3342 | `82702195adc6f5891e7ce2b221e12c24ca0a151b` |
| 31 | `docs/evidence/outputs/ASTRA-ROOTCAUSE-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 5429 | `1d891b546519e1b8cadcc83c1a9cbe5e1bcc070e` |
| 32 | `docs/evidence/outputs/ASTRA-SWEEP1-2026-10-13.md` | GenAI 过程归档（prompt/未编辑输出） | 6124 | `91777c14f09a1a535079ae502af4b807218b3a48` |
| 33 | `docs/evidence/outputs/astra-draft.txt` | GenAI 过程归档（prompt/未编辑输出） | 5090 | `3c803ece522c1340e1f10510aee16ca257478947` |
| 34 | `docs/evidence/outputs/deepseek-draft.txt` | GenAI 过程归档（prompt/未编辑输出） | 7922 | `3f631eade0ff18fd04d01531f3264613e7fbab67` |
| 35 | `docs/evidence/outputs/demo-rev1-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 30903 | `8a4b726fb9eb07bb52253d031440a76400275d4f` |
| 36 | `docs/evidence/outputs/evidence-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 7912 | `8b28d5acaad8337b854f8b88e4d36d953d2d3641` |
| 37 | `docs/evidence/outputs/gates-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 10588 | `2b3072912f5889614d57934b4480d29e7376ee5c` |
| 38 | `docs/evidence/outputs/gemini-draft.txt` | GenAI 过程归档（prompt/未编辑输出） | 7022 | `caf59ea80c1c31316dadc0c9134847ae750ccf53` |
| 39 | `docs/evidence/outputs/outline-rev1-deepseek.txt` | GenAI 过程归档（prompt/未编辑输出） | 30113 | `a4b3c262a74bb870a15cd0d3795d6e583ec0a817` |
| 40 | `docs/evidence/outputs/outline-rev2-sol.txt` | GenAI 过程归档（prompt/未编辑输出） | 20941 | `5c2a3c3eb00727b1c10b9359f6c8d2e315f66b82` |
| 41 | `docs/evidence/outputs/outline-rev3-sol.txt` | GenAI 过程归档（prompt/未编辑输出） | 26537 | `2aaaf836ff5a9c38bc2d6a3fef0bd60d20700d25` |
| 42 | `docs/evidence/outputs/pmv-fix-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 9144 | `80c089c7e7556d552d0f0e6ae6be035a02d7ff9c` |
| 43 | `docs/evidence/outputs/pmv-fix2-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 18447 | `1d8426c74c488e38f160d42cd1559e5fd3641498` |
| 44 | `docs/evidence/outputs/pmv-fix3-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 8427 | `dd66c2cee12d6c10670a4ed43485a6b02178d345` |
| 45 | `docs/evidence/outputs/pmv-fix4-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 12498 | `adbb0c292805b537233c1f2d83bda69f0a12201c` |
| 46 | `docs/evidence/outputs/pmv-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 10258 | `81e6906f90279d6a369a8db0725a61cb42f69d1b` |
| 47 | `docs/evidence/outputs/realerror-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 4885 | `24e7a5f5f943878942c5a4c01c717b610cc91b8e` |
| 48 | `docs/evidence/outputs/taskA-deepseek.txt` | GenAI 过程归档（prompt/未编辑输出） | 27111 | `09f70e6034a92ba68854bb5a6b50aa2815c245c6` |
| 49 | `docs/evidence/outputs/taskB-gemini.txt` | GenAI 过程归档（prompt/未编辑输出） | 21033 | `1de9d26b2267e29abbd5db41935ecd20edbe7e4e` |
| 50 | `docs/evidence/prompts-reconstructed/00-README.md` | GenAI 过程归档（prompt/未编辑输出） | 612 | `46050056d79075e37c686ed38975c3955617b3e3` |
| 51 | `docs/evidence/prompts-reconstructed/01-adjudication-1346.md` | GenAI 过程归档（prompt/未编辑输出） | 2218 | `01d30335f46171490258b6de09e23d0cda61d1d6` |
| 52 | `docs/evidence/prompts-reconstructed/02-rev1-1404.md` | GenAI 过程归档（prompt/未编辑输出） | 2166 | `fa977fecaaf590166223d3b80aa9d34296fb99c3` |
| 53 | `docs/evidence/prompts-reconstructed/03-rev2-1440.md` | GenAI 过程归档（prompt/未编辑输出） | 2244 | `f6f237f81a72f3d1deaf5c074b27f1875f36cf0f` |
| 54 | `docs/evidence/prompts-reconstructed/04-rev3-1509.md` | GenAI 过程归档（prompt/未编辑输出） | 2288 | `e860957f04bd3dc54dfae31e7103218ab513d838` |
| 55 | `docs/evidence/prompts-reconstructed/05-rev3fix-1541.md` | GenAI 过程归档（prompt/未编辑输出） | 2025 | `566dcc740f30756fe8b04d54ba2f3ac42be08870` |
| 56 | `docs/evidence/prompts-reconstructed/06-rev3fix2-1610.md` | GenAI 过程归档（prompt/未编辑输出） | 2206 | `b39c12cd128b75a5a0f28c85f4e63d70c0b212b4` |
| 57 | `docs/evidence/prompts-reconstructed/07-rev3fix3-1733.md` | GenAI 过程归档（prompt/未编辑输出） | 2222 | `73e214784a4180f8ec75ec0eb3cec51297145a33` |
| 58 | `docs/evidence/prompts-reconstructed/08-final-1757.md` | GenAI 过程归档（prompt/未编辑输出） | 2082 | `962f7ec55feeaf86eba1d06646d3d191b2b16b4b` |
| 59 | `docs/evidence/prompts/PROMPT-ENTRY4-RECONSTRUCTED.md` | GenAI 过程归档（prompt/未编辑输出） | 1966 | `a4e282674e18346c42caf8e75ef73692dcd93e1a` |
| 60 | `docs/evidence/prompts/TASK-A-deepseek.md` | GenAI 过程归档（prompt/未编辑输出） | 2354 | `996b8e8f1909c505a21a82cfd54e47bcfb026f76` |
| 61 | `docs/evidence/prompts/TASK-A2-revise.md` | GenAI 过程归档（prompt/未编辑输出） | 2579 | `471a819c9ce61cecb2911045da85e3efcc1a573b` |
| 62 | `docs/evidence/prompts/TASK-B-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 1738 | `f86a0c00baa350012288f2c9a4a747cb1aff433d` |
| 63 | `docs/evidence/prompts/TASK-B2-revise.md` | GenAI 过程归档（prompt/未编辑输出） | 1984 | `ec512f644d86e9c8caf9cbe758dac4b910b07b95` |
| 64 | `docs/evidence/prompts/TASK-EVIDENCE-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 1726 | `05f2ab9afafaa922dd2911273b0712e378b05ddb` |
| 65 | `docs/evidence/prompts/TASK-GATES-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 1958 | `54375aaa64c735c3884252920008db5a3ae564c5` |
| 66 | `docs/evidence/prompts/TASK-PMV-FIX-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 3296 | `e8c9294e34ebdf0212deb61a40bf1432330fdbc3` |
| 67 | `docs/evidence/prompts/TASK-PMV-FIX2-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 3158 | `b725accfd86071a41831ba8ae276d6ca2974bc39` |
| 68 | `docs/evidence/prompts/TASK-PMV-FIX3-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 2927 | `f380a0d6fea435cc2d271537ec5c35abc6e4f37a` |
| 69 | `docs/evidence/prompts/TASK-PMV-FIX4-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 4314 | `907e55ddc0feac2bf3a7380c97f9a28b616fb8c3` |
| 70 | `docs/evidence/prompts/TASK-PMV-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 2956 | `9e3bc737d618908d174d3b62387e9b466ee7d8bf` |
| 71 | `docs/evidence/prompts/TASK-REALERROR-gemini.md` | GenAI 过程归档（prompt/未编辑输出） | 1451 | `72287958d303db9b6edc26456782d03b005abfcc` |
| 72 | `docs/evidence/prompts/TASK-REV2-deepseek.md` | GenAI 过程归档（prompt/未编辑输出） | 3570 | `b01f15a409799c50741da539c925e25be6d3e89f` |
| 73 | `docs/evidence/prompts/TASK-REV3-sol.md` | GenAI 过程归档（prompt/未编辑输出） | 3031 | `e2336ddda8e16f77a59c29b23195425b56d2df75` |
| 74 | `docs/evidence/prompts/TASK.md` | GenAI 过程归档（prompt/未编辑输出） | 1919 | `b1b7bece5cff6a658caec81f15ba2e593284591c` |
| 75 | `docs/evidence/pytest-full.log` | 独立复跑记录 | 8048 | `ee30eef3eaf58587ca582918a9496d03d8ec082d` |
| 76 | `docs/evidence/rerun-full.log` | 独立复跑记录 | 1866 | `2fc5840641b7eb5a23dea0bcafce6395c0b1614e` |
| 77 | `evidence/MANIFEST.sha256` | 冻结基线清单 | 1306 | `78b775f9160c5b0728149bb8bc57bd7443700407` |
| 78 | `evidence/cases.md` | 证据分析报告 | 3668 | `1abf1280b991131d3d4bb555deda21f0660f0221` |
| 79 | `evidence/delay-chain.md` | 证据分析报告 | 6452 | `eddd13c84d2ea675e0cc3a3a33e99f28bf16bb16` |
| 80 | `evidence/natural-undecidable-case.md` | 证据分析报告 | 5557 | `2c4d6ce4f29874ab652092269ccee23d82b5ee98` |
| 81 | `evidence/real-error-case-v2.md` | 证据分析报告 | 14347 | `95da9dfc2ea99ac37ebbc6ede4fe7732073c3283` |
| 82 | `evidence/real-error-case.md` | 证据分析报告 | 9226 | `ce97a533833eb2aeccd2fc0ce4918eeee2dfa307` |
| 83 | `evidence/redistribution-index.md` | 证据分析报告 | 14679 | `f67a6cf9f1b1c64de258f29767d609d240b0c0b8` |
| 84 | `evidence/results/pkg-npm-debug-4.3.4.result.json` | 冻结基线快照/结果（12 文件） | 4437 | `7a708de83716da13fc5db022d94d22d53b4ab9c6` |
| 85 | `evidence/results/pkg-npm-esprima-4.0.1.result.json` | 冻结基线快照/结果（12 文件） | 5209 | `f540f33688ddfdf0434651b1716aab00e83210ef` |
| 86 | `evidence/results/pkg-npm-synthetic-fixture-1.0.0.result.json` | 冻结基线快照/结果（12 文件） | 4694 | `67892ae11eca2c6fff047cb81e719cd5f6ed0497` |
| 87 | `evidence/results/pkg-pypi-archgraph-layout-2.3.0.result.json` | 冻结基线快照/结果（12 文件） | 4642 | `ae0fcdd809251f7206ec3d71d7ad8ab6dfc22b20` |
| 88 | `evidence/results/pkg-pypi-typing-extensions-4.12.2.result.json` | 冻结基线快照/结果（12 文件） | 6040 | `d153ef79ab2c579cf879b14728dedac8a59879be` |
| 89 | `evidence/snapshots/pkg-npm-debug-4.3.4.json` | 冻结基线快照/结果（12 文件） | 2363 | `e53c251e2e60746207dfa3cf09d67819696f4b27` |
| 90 | `evidence/snapshots/pkg-npm-esprima-4.0.1.json` | 冻结基线快照/结果（12 文件） | 2926 | `bc552deccdc0e6988e597e75f8a512b5e98edea4` |
| 91 | `evidence/snapshots/pkg-npm-synthetic-fixture-1.0.0.json` | 冻结基线快照/结果（12 文件） | 1861 | `b2a0340d52123d4b5d19b8b8d918add7efa6e26d` |
| 92 | `evidence/snapshots/pkg-pypi-archgraph-layout-2.3.0.json` | 冻结基线快照/结果（12 文件） | 2553 | `7c5d69cfab23f859b696555dc721c01a5d5ad855` |
| 93 | `evidence/snapshots/pkg-pypi-typing-extensions-4.12.2.json` | 冻结基线快照/结果（12 文件） | 5019 | `1e397340a9d9bc55db0fa237fee20eb7be18b71e` |
| 94 | `evidence/supplementary/README.md` | 补充证据（不在冻结基线内） | 8180 | `9ea7ea6c2e584c3db950d79589f736af527e9a00` |
| 95 | `evidence/supplementary/pkg-pypi-django-flowcontrol-0.0.21.raw.json` | 补充证据（不在冻结基线内） | 13691 | `3fe5079cae455ce1e7b75c994521f2ab68531335` |
| 96 | `evidence/supplementary/pkg-pypi-hatch-vcs-0.4.0.raw.json` | 补充证据（不在冻结基线内） | 31337 | `5667863ff1841909060b3ccf4800739cee8ea407` |
| 97 | `evidence/supplementary/pkg-pypi-validfilepath-0.1.raw.json` | 补充证据（不在冻结基线内） | 14278 | `398b45fcca2e8a2dae72c03db08d9dea41e70337` |
| 98 | `evidence/supplementary/result-pkg-pypi-django-flowcontrol-0.0.21.json` | 补充证据（不在冻结基线内） | 5351 | `76e869af5b18a4915f025f4a2767154b6ad61cf5` |
| 99 | `evidence/supplementary/result-pkg-pypi-hatch-vcs-0.4.0.json` | 补充证据（不在冻结基线内） | 5254 | `3f729d84e243081ae439241f50bbd99d3cf0f874` |
| 100 | `evidence/supplementary/result-pkg-pypi-validfilepath-0.1.json` | 补充证据（不在冻结基线内） | 5221 | `e4238b820d299049cbc6ebcb046a387ac4838327` |
| 101 | `evidence/supplementary/snapshot-pkg-pypi-django-flowcontrol-0.0.21.json` | 补充证据（不在冻结基线内） | 4706 | `9275d7ae8e8b8c3a4f6a7669aa37eec97ecdc6f6` |
| 102 | `evidence/supplementary/snapshot-pkg-pypi-hatch-vcs-0.4.0.json` | 补充证据（不在冻结基线内） | 5498 | `0f2d492c745819f5d512078b6c6bded9f92e32d3` |
| 103 | `evidence/supplementary/snapshot-pkg-pypi-validfilepath-0.1.json` | 补充证据（不在冻结基线内） | 4611 | `ab481a80af268b6849bb757522127653e8294b84` |
| 104 | `examples/integration/README.md` | 接入示例 | 9725 | `b0f09737f4d802abc7ab766ee51b02ce49f42861` |
| 105 | `examples/integration/audit_pipeline_run.json` | 接入示例 | 5801 | `e7742725b387dec5b82596f4a1da39fed312f267` |
| 106 | `examples/integration/pipeline_demo.py` | 接入示例 | 16078 | `d5e8f9df5d79002cfefbfa8ae3b9d66e359ec051` |
| 107 | `pmv/__init__.py` | PMV 实现代码（已冻结） | 803 | `02044242e589b788efea8744676bd98d3d0bae1a` |
| 108 | `pmv/cli.py` | PMV 实现代码（已冻结） | 5569 | `411a2a9f71ffaf8772394b09958e7ccdf8e584d6` |
| 109 | `pmv/collector.py` | PMV 实现代码（已冻结） | 8827 | `2e424f595189e9b7b96646a30265d46d5fffd3f5` |
| 110 | `pmv/exporter.py` | PMV 实现代码（已冻结） | 9721 | `5c6bbe7371c1cec95e5b827aa2916b4a5cd80c75` |
| 111 | `pmv/normalizer.py` | PMV 实现代码（已冻结） | 15952 | `c028fb3ab286c161cc14c40a6f89235613a3d065` |
| 112 | `pmv/verifier.py` | PMV 实现代码（已冻结） | 81246 | `a63cfe0bbf3d193822e3e763aec0f39e00f5c789` |
| 113 | `rerun-report.md` | 复跑程序与报告 | 6790 | `c6c186f7f712554810f493952671848f33f0f04f` |
| 114 | `rerun.sh` | 复跑程序与报告 | 14523 | `173b58b56bb97012cfc61075d14d590815c9be91` |
| 115 | `rules/rules-v0.1.json` | 判定规则 v0.1（已冻结） | 2492 | `c189774d2d417657f76fa502ed7671be4e47a9d6` |
| 116 | `run_harvest.py` | 复跑程序与报告 | 6340 | `9bfbbc61822e768388f686cd5cc9a26e66174b82` |
| 117 | `schemas/pmv-output.schema.json` | 输出 Schema（已冻结） | 4087 | `438cd44a6ba8a75190e2e9fc6bb21cad14776b28` |
| 118 | `tests/__init__.py` | 回归测试（已冻结） | 82 | `441f3e3837193c54637660a32210ab09620dd65f` |
| 119 | `tests/test_schema.py` | 回归测试（已冻结） | 3487 | `c79d03f2191c411e709fa043c67528b037f793e3` |
| 120 | `tests/test_verifier_rules.py` | 回归测试（已冻结） | 73197 | `11a22bfacccb94eaccb1bc1263f3c766bccdb18a` |
