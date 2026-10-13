# GenAI Disclosure (draft for the application text — applicant to adopt/edit)

> **Use of generative AI in preparing this application.** We used generative AI tools for the following, because the applicant was travelling and needed to complete cross-project differentiation research and a runnable prototype verification within three weeks:
> - *Research summarisation:* DeepSeek (via API) for literature/differentiation analysis across AboutCode/ScanCode, ClearlyDefined, deps.dev, and OSV.
> - *Outline and design drafts:* DeepSeek for the proposal outline structure; Gemini for the demo technical design.
> - *Prototype implementation:* Gemini for the PMV prototype code (package metadata verifier), per a detailed technical specification authored by the main-chat AI agent (TASK-PMV-gemini.md). No human-written specification original exists for this prototype; the specification itself is AI-authored.
> - *Outline revisions:* GPT-6.1-Sol and Astra Max for revising the outline against independent reviewer feedback.
>
> AI outputs were checked against primary sources (official NLnet pages, upstream project documentation, live API responses, re-runnable code) **where feasible; items not yet independently verified are marked as such in the log** — the log is a working record, not a certificate of verification. The final proposal text **will be written and verified by the applicant (Jigao Yi) before submission**; no AI-generated text will be submitted unverified. A prompt provenance log — model, date/time, full prompts, and unedited outputs archived to date — is available at https://github.com/yijigao/pkgmeta-verify/blob/main/PROMPT-LOG.md, with prompts under `docs/evidence/prompts/` and outputs under `docs/evidence/outputs/`.
>
> The ~262h labour budget is a **forward-looking budget for human work**: software development, code review, dataset integration, independent verification runs, documentation, and upstream coordination by the applicant. AI-assisted artefacts do not substitute for this human contribution and are not claimed as completed human work.

Notes for the applicant (not part of the submission text):
- Per the GenAI policy, the "why necessary" reason is inside the English text above.
- Do NOT claim "all outputs independently verified" or "final application already written by applicant" — both are unconfirmed as of this draft.
- Before submission, re-check whether the GenAI policy has been revised; archive the version in force.
