**② 以下 4 项必须修，均为诚实／证据问题。**

已核查公开提交 [`d2f7995`](https://github.com/yijigao/pkgmeta-verify/commit/d2f7995d30b875a640887996c3a629aecbaa157b)，独立实跑 **56/56 测试通过、12/12 哈希匹配、5/5 基线复算一致**。技术路线和增量已有可执行证据，达到概念验证层级。13 prompt、20 output 均可访问且非空，条目 4 的重建标注合格。

1. **独立复跑证明与附件矛盾。** [署名记录](https://github.com/yijigao/pkgmeta-verify/blob/d2f7995/docs/evidence/INDEPENDENT-RERUN.md#L9)写“56 tests，OK”，对应[测试附件](https://github.com/yijigao/pkgmeta-verify/blob/d2f7995/docs/evidence/independent-tests.log)却是“53 tests，FAILED (errors=1)”。须区分失败尝试与成功复跑，补上对应成功记录和准确时间。我的复跑通过不能替代这份证据纠正。

2. **“覆盖全部误判”仍未删净。** [README 第 168 行](https://github.com/yijigao/pkgmeta-verify/blob/d2f7995/README.md#L168)仍写“覆盖全部误判缺陷的 25 个回归测试用例”。须改为实际的 **56 项现有测试**及其有限覆盖范围。

3. **归档数量正确，但申请过程记录仍缺件。** [日志条目 14](https://github.com/yijigao/pkgmeta-verify/blob/d2f7995/PROMPT-LOG.md#L112)明确缺五轮终审 prompt 和具体时间。标注缺失是诚实的，但尚不能验收为完整归档；须回收原记录补齐，重建部分明确来源和不确定性。[官方政策](https://nlnet.nl/foundation/policies/generativeAI/)要求记录模型、日期时间、prompt 和未编辑输出。

4. **人工贡献归属仍需纠正。** [日志条目 3、5、6](https://github.com/yijigao/pkgmeta-verify/blob/d2f7995/PROMPT-LOG.md#L24)把阿析代理的工作写成“人工编写／人工代填”。须改为真实的 AI 工作归属；[披露草稿](https://github.com/yijigao/pkgmeta-verify/blob/d2f7995/docs/evidence/GENAI-DISCLOSURE-DRAFT.md#L6)的“human-written technical specification”也须有对应人类原稿依据，否则据实改写。此前“所有输出已核验”“终稿已由申请人写成”两条旧声明，已确认删除。