基于 main **`22435cb5`**，四份文件仍有以下实质性问题：

1. **[evidence/delay-chain.md:8、39、48、78、93](https://github.com/yijigao/pkgmeta-verify/blob/22435cb5e63ae668605666fc337042e81b85a35a/evidence/delay-chain.md#L8)；[docs/evidence/PROPOSAL-DRAFT.md:86、266](https://github.com/yijigao/pkgmeta-verify/blob/22435cb5e63ae668605666fc337042e81b85a35a/docs/evidence/PROPOSAL-DRAFT.md#L86)**  
   **问题：**第97行已承认同期原始记录缺失，但摘要、节点结论和提案仍宣称延迟成立、时间链完整、有原始 HTTP 证据。  
   **应改：**统一为“候选延迟观察；历史 404→200 尚未获得同期原始记录验证，不能作为已证明的同步延迟或延迟区间”。

2. **[evidence/real-error-case-v2.md:151](https://github.com/yijigao/pkgmeta-verify/blob/22435cb5e63ae668605666fc337042e81b85a35a/evidence/real-error-case-v2.md#L151)**  
   **问题：**仍断言“100%……下游解析器故障”，直接违背第147行“具体机制未确认”。  
   **应改：**“仓库链接字段错误成立；具体解析机制和故障环节未确认。”

3. **[evidence/real-error-case-v2.md:17–19](https://github.com/yijigao/pkgmeta-verify/blob/22435cb5e63ae668605666fc337042e81b85a35a/evidence/real-error-case-v2.md#L17)；[docs/evidence/PROPOSAL-DRAFT.md:75](https://github.com/yijigao/pkgmeta-verify/blob/22435cb5e63ae668605666fc337042e81b85a35a/docs/evidence/PROPOSAL-DRAFT.md#L75)**  
   **问题：**[deps.dev 官方 FAQ](https://docs.deps.dev/faq/#how-are-licenses-determined)没有报告所称“仅提取 `License:`、因历史歧义不映射 Trove”的明确政策，不能据此证明“双方均合规、属于规范矛盾”。  
   **应改：**删除无原文支持的政策归因，保留“原下游责任断言已撤回；许可证表示差异的机制与规范责任尚未确定”，提案同步修改。

4. **[evidence/real-error-case-v2.md:27、148、215](https://github.com/yijigao/pkgmeta-verify/blob/22435cb5e63ae668605666fc337042e81b85a35a/evidence/real-error-case-v2.md#L27)**  
   **问题：**“老版本＋HTTP 200”不能证明记录已稳定，更不能作为排除同步或更新延迟的通用规则；[官方 FAQ](https://docs.deps.dev/faq/#how-fresh-is-the-information)明确说明不活跃包可能呈现较旧数据。  
   **应改：**删除这条排除规则；本例只确认链接字段错误，是否存在更新传播滞后须另有更新时间或连续观测证据。

5. **[evidence/real-error-case-v2.md:143](https://github.com/yijigao/pkgmeta-verify/blob/22435cb5e63ae668605666fc337042e81b85a35a/evidence/real-error-case-v2.md#L143)**  
   **问题：**把 `ofek` 的“询问是否有进展”扩大成维护者“确认该错误”，超过[原评论](https://github.com/google/deps.dev/issues/220#issuecomment-3478074544)所能支持的范围。  
   **应改：**“维护者 `ofek` 曾跟进询问处理进展。”

6. **[evidence/real-error-case-v2.md:197–198](https://github.com/yijigao/pkgmeta-verify/blob/22435cb5e63ae668605666fc337042e81b85a35a/evidence/real-error-case-v2.md#L197)**  
   **问题：**将 PyPI 版本补零描述成跨生态统一采用“三段式 SemVer”，混淆了键规范化和版本语义；[上游解释](https://github.com/google/deps.dev/issues/89#issuecomment-2111642552)只是为内部一致键至少补足三段。  
   **应改：**“deps.dev 对 PEP 440 等价版本进行内部键规范化，本例补零不改变版本等价关系”，删除统一 SemVer 的归因。

7. **[evidence/delay-chain.md:26、29](https://github.com/yijigao/pkgmeta-verify/blob/22435cb5e63ae668605666fc337042e81b85a35a/evidence/delay-chain.md#L26)**  
   **问题：**一边承认无法解释倒序，一边断言观察“已被预填或来自未校准时钟”，仍在无证据地指定原因。  
   **应改：**“报告时间与观察时间矛盾，原因未知；现有记录不足以验证该观察”，保留撤回状态。

8. **[evidence/natural-undecidable-case.md:47、56](https://github.com/yijigao/pkgmeta-verify/blob/22435cb5e63ae668605666fc337042e81b85a35a/evidence/natural-undecidable-case.md#L47)**  
   **问题：**以“404 / Empty”代替确定的请求结果，却把 ClearlyDefined 纳入已核验的第三源缺证结论，无法区分未收录与已有记录但许可字段为空。  
   **应改：**给出具体查询坐标、实际状态码、响应及时间；无法提供时标为“未核实，不参与本例判断”。

9. **[evidence/natural-undecidable-case.md:97](https://github.com/yijigao/pkgmeta-verify/blob/22435cb5e63ae668605666fc337042e81b85a35a/evidence/natural-undecidable-case.md#L97)**  
   **问题：**从空字段比较直接推导“企业系统放行没有任何授权的闭源或侵权风险代码”，既无系统行为证据，也超出了第29、99行限定的许可证核验范围。  
   **应改：**“将空字段相等当成许可证已核验一致，会产生错误的一致性结论；本例不能判断整包授权状态或企业放行行为。”

10. **[docs/evidence/PROPOSAL-DRAFT.md:216](https://github.com/yijigao/pkgmeta-verify/blob/22435cb5e63ae668605666fc337042e81b85a35a/docs/evidence/PROPOSAL-DRAFT.md#L216)**  
    **问题：**个人专长段仍把实现依据写成“申请人的任务规格”，与第213、250行明确披露详细规格由 AI 撰写、无人类原稿的归属口径冲突。  
    **应改：**“Gemini 按 AI 起草、依据申请人所定原则的详细规格实现；申请人贡献为原则制定和验收决策。”

11. **[docs/evidence/PROPOSAL-DRAFT.md:184、189](https://github.com/yijigao/pkgmeta-verify/blob/22435cb5e63ae668605666fc337042e81b85a35a/docs/evidence/PROPOSAL-DRAFT.md#L184)**  
    **问题：**预算总结仍将独立复跑执行列入申请人的约262小时，与第157行“第三方执行不计入申请人工时”的明确安排矛盾。  
    **应改：**申请人工时统一列为“复现包准备、复跑协调和结果分析”；第三方执行另列为预算外无偿投入，内部自测不得算独立验收。