# GenAI Disclosure (draft for the application text — applicant to adopt/edit)

> **Use of generative AI in preparing this application.** We used generative AI tools for the following, because the applicant was travelling and needed to complete cross-project differentiation research and a runnable prototype verification within three weeks:
> - *Research summarisation:* DeepSeek (via API) for literature/differentiation analysis across AboutCode/ScanCode, ClearlyDefined, deps.dev, and OSV.
> - *Outline and design drafts:* DeepSeek for the proposal outline structure; Gemini for the demo technical design.
> - *Prototype implementation:* Gemini for the PMV prototype code (package metadata verifier), per a detailed human-written technical specification.
> - *Outline revisions:* GPT-6.1-Sol and Astra Max for revising the outline against independent reviewer feedback.
>
> Every AI output was checked against primary sources (official NLnet pages, upstream project documentation, live API responses, and re-runnable code) before use; claims that could not be evidenced were removed or downgraded. The final proposal text is written and verified by the applicant (Jigao Yi). A prompt provenance log — model, date/time, full prompts, and unedited outputs archived to date — is available at https://github.com/yijigao/pkgmeta-verify/blob/main/PROMPT-LOG.md, with prompts under `docs/evidence/prompts/` and outputs under `docs/evidence/outputs/`. The log is updated as work continues; entries not yet independently verified are marked as such.
>
> The ~262h labour budget is a **forward-looking budget for human work**: software development, code review, dataset integration, independent verification runs, documentation, and upstream coordination by the applicant. AI-assisted artefacts do not substitute for this human contribution and are not claimed as completed human work.

Notes for the applicant (not part of the submission text):
- Per the GenAI policy, the "why necessary" reason is now inside the English text above (was previously only in Chinese notes).
- Do NOT claim "all outputs independently verified" or "final application written by applicant" until each is actually true at submission time.
- Before submission, re-check whether the GenAI policy has been revised; archive the version in force.
