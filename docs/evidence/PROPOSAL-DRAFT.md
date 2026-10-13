# NLnet CodeSupply — Project Proposal (Draft for applicant review)

> **Status**: AI-assisted draft prepared 2026-10-13/14 for Jigao Yi's review and finalisation. No AI-generated text will be submitted unverified; the final proposal text will be written and verified by the applicant before submission.
> **Public claim standard (Joey, 2026-10-13)**: zero failures in the existing test suite (56/56); PMV is a proof of concept. Test passage means conformance with the current test set, not absolute correctness.

---

## 1. Project summary

**Project name**: Package Metadata Verifier (PMV) — a quality-inspection component for CodeSupply aggregation pipelines.

**Applicant**: Jigao Yi (individual application). The applicant is also the technical lead and the future MoU signatory, responsible for development, fact verification, delivery, maintenance, and upstream communication.

**Amount requested**: €15,000 (100% lump sum, milestone-based).

**Duration**: 9 months of planned delivery, with acceptance rework handled within 12 months (rework hours already budgeted).

**Technical scope**: npm + PyPI. Cross-source verdicts with provenance, timestamps, and offline-reproducible evidence; lifecycle tracking; a verifiable quality dataset.

**What this project delivers**: an independent package-metadata quality-inspection component that CodeSupply-style aggregation pipelines can plug in between data ingestion and aggregated-record publication. Its core increment is: cross-source discrepancy verdicts with source, time, and reproducible evidence; lifecycle event tracking; and a verifiable dataset of inspection results that can be re-run offline from fixed inputs.

**What this project is not**: it is not a new aggregator, and not a claim to a complete open dataset. The CodeSupply core consortium is itself building aggregation (AboutCode is a consortium member); this proposal positions PMV as an independent inspection component that fits into that pipeline, not a competing aggregator.

---

## 2. Problem, positioning, and expected value

### 2.1 Problem statement

When aggregators process license, publication-time, repository-link, artifact-digest, and lifecycle information for the same package version, they must distinguish field errors, sync delays, semantic differences, and insufficient evidence. Naive string diffing cannot explain source dependencies, field applicability, artifact identity, or observation time. Source agreement may merely reflect ingestion propagation; field disagreement may come from different analysis scopes.

PMV converts differences into structured, reasoned, evidence-referenced, re-computable quality verdicts, so aggregators can decide to re-check, send for review, or revise — instead of silently passing bad data through or raising false alarms.

### 2.2 Component positioning

- Consumes registry APIs, aggregator records, and fixed snapshots.
- Provides a CLI, a Python library, versioned rules, and a JSON Schema.
- Outputs field-level verdicts, source dependencies, observation times, and minimal evidence packages.
- Designed to plug into the quality-check step **after CodeSupply data ingestion and before aggregated-record publication**; also provides a batch-review entry for existing datasets.
- Integration interfaces are being aligned via an AboutCode issue; no claim of adoption is made at this stage.

---

## 3. Related projects and differentiation

| Project | What it does | What PMV adds |
|---|---|---|
| AboutCode / ScanCode | Coordinate parsing, normalisation, existence checks; license analysis | Reuses applicable capabilities; adds version-, field-, and artifact-level verdicts with evidence |
| ClearlyDefined | Curated license data | Used only to supplement license fields; actual coverage disclosed |
| deps.dev | Dependency metadata | One of the cross-sources; not treated as independent ground truth where fields derive from registries |
| OSV | Vulnerability data | Out of scope for this project |

PMV's increment: verdicts carry reasons and evidence citations, not just differences; source dependency, field scope, time chains, and artifact comparability conditions are part of the same output contract.

---

## 4. Dual-ecosystem sources and dependency relationships

- **npm**: npm registry + deps.dev.
- **PyPI**: PyPI + deps.dev.
- **ClearlyDefined**: supplements license fields only; actual coverage is disclosed per run.
- PyPI JSON and Simple are two interfaces of the same registry — not independent sources.
- Some deps.dev fields derive from registries; agreement there is not treated as independent corroboration.

---

## 5. Completed prototype and baseline evidence

A runnable minimum prototype exists at https://github.com/yijigao/pkgmeta-verify (Apache-2.0). Current state: **zero failures in the existing test suite (56/56); PMV is a proof of concept.**

**Frozen baseline** (5 cases, each with snapshots, results, and SHA-256 manifest — 12/12 hash-verified):

| Case | Verdict | Status |
|---|---|---|
| `pkg:pypi/typing-extensions@4.12.2` | Earlier downstream fault attribution falsified and removed; license-representation difference mechanism and specification responsibility undetermined | Documented |
| `pkg:pypi/archgraph-layout@2.3.0` | Suspected delay | **suspect/retracted** — time-order contradiction unresolved |
| `pkg:npm/esprima@4.0.1` | License semantic difference | Documented with field/facet scope |
| `pkg:npm/debug@4.3.4` | INDETERMINATE | Synthetic cross-algorithm test, `synthetic=true` |
| `pkg:npm/synthetic-fixture@1.0.0` | DIGEST_CONFLICT | Constructed fixture, `synthetic=true` |

**Supplementary documented cases** (reports only; raw collection records being added as supplementary evidence, not part of the frozen 5-case baseline):

| Case | Verdict | Status |
|---|---|---|
| `pkg:pypi/hatch-vcs@0.4.0` | Real repository-link error (deps.dev listed the funding URL as SOURCE_REPO) | **Documented** — link error publicly reported in deps.dev issue #220; the specific parsing mechanism is unconfirmed (the deps.dev team suspects a spec-change-related cause and is investigating); `git ls-remote` shows the funding URL is not a Git repository |
| `pkg:pypi/validfilepath@0.1` | Candidate delay observation | **Documented** — single observation; historical 404→200 lacks contemporaneous raw records; not a proven sync delay or delay interval |
| `pkg:pypi/django-flowcontrol@0.0.21` | INDETERMINATE | **Documented** — genuine missing evidence, naturally undecidable, not constructed |

Byte-identical replay results are reported after isolating `evaluation_timestamp` (clock-dependent fields are normalised before comparison; this is documented in `rerun-report.md`).

---

## 6. Verdict rules and output contract

Versioned inspection rules (`rules v0.1`) with:
- Missing upstream publication time → `undecidable`, never `SYNC_DELAY`.
- Empty evidence → `undecidable`, never "consistent".
- Artifact identity requires valid digest content, not just key names.
- Algorithm names normalised before length checks; unknown algorithms → `undecidable`.
- Future times rejected against the real clock; HTTP statuses reported exactly.
- Blank/unknown license values → `undecidable`; confidence is scored by evidence strength in the general case.
- No hardcoded assertions from keyword hits or self-attested flags as a design goal.

**Known limitations of the proof of concept** (disclosed): some verdict paths still carry hardcoded `confidence: 1.0` (e.g. `verifier.py` L1097), and the PSF-license branch can trigger on license title text plus "version 2" alone (L346) without authorisation/conditions/disclaimer text. These are documented limitations, not claimed-away. The "concept validation" standard at the top of this proposal does not cancel these specific limitations.

The output contract (JSON Schema, Draft 2020-12) carries field-level verdicts, provenance, observation times, and minimal evidence packages.

---

## 7. Schema, baseline, and rerun procedure

- Schema `$id`: versioned address under the project's control (GitHub raw, tagged at submission snapshot).
- Evidence manifest (`evidence/MANIFEST.sha256`): 12/12 files hash-verified.
- `rerun.sh`: real checks (not stubbed), non-zero exit on failure, regenerates the audit report.
- Fixed-input offline replay: 5/5 baseline cases byte-identical, Schema VALID.

---

## 8. Independent rerun

An independent rerun (non-implementer, clean environment) is a pre-submission requirement. The implementer was an AI agent working to an AI-agent-authored task specification (TASK-PMV-gemini.md); the rerun must be performed by a different party with full attribution (identity, relationship to the project, commit, dependency versions, commands, raw logs). The rerun performed to date was done by a non-implementer **within the same applicant AI team** — this is documented as such and is not presented as external third-party verification. The rerun record is archived in `docs/evidence/`; the rerun's own honest conclusions are preserved verbatim, including any findings against the project.

---

## 9. Funded future work (not yet done)

Clear boundary: the prototype, baseline cases, rules, Schema, and self-test procedures completed before application are the starting point — they are not listed again as future deliverables or hours.

### 9.1 Dataset and observation plan

- M1: 200 unique version coordinates (100 npm / 100 PyPI); synthetic samples excluded from real counts.
- dataset v1: 1,000 unique version coordinates (500 per ecosystem); public sampling list and stratification rationale.
- ≥3 observations per coordinate across ≥30 days; target ≥3,000 coordinate-observation records.
- 100 coordinates observed daily for 30 consecutive days.
- Each round covers registry + deps.dev; failure states preserved as-is; ClearlyDefined coverage disclosed.
- Automated waits and scheduled runs are not counted as human labour.

### 9.2 Fields and scorecard

- Name/version/PURL, version visibility, license, repository link, publication time, artifact URL/type/size/digest, and available yank/deprecated information.
- Lifecycle events require explicit status, announcement, redirect, or maintainer statement.
- Report field availability rate, comparability rate, conflict rate, undecidable rate, difference duration, and evidence-backed delay ranges.
- No "staleness rate" computed for data without update timestamps.

---

## 10. Milestones, budget, and acceptance

### 10.1 Milestones

| Milestone | Time | Amount | Acceptance |
|---|---|---:|---|
| M1: Alignment + core verification | Month 3 | €6,000 | CLI/library completion; dual-ecosystem adapters; 200 coordinates; four categories of real evidence plus separately-marked constructed tests; rules, Schema, evidence package, CI |
| M2: Lifecycle + dataset | Month 5 | €5,000 | 1,000 coordinates × 3 observation rounds; 100 coordinates daily; ≥100 boundary tests; evidence-backed lifecycle records; dataset v1 |
| M3: Independent reproduction + scorecard | Month 7 | €2,500 | Complete records from two independent rerunners; fixed-input result comparison; scorecard and time series |

**M3 rerunner arrangements**: the two independent rerunners are third parties external to the applicant's AI team (not the implementer, not the applicant), participating on a **voluntary unpaid basis** — a clean-environment rerun of the frozen package takes approximately 2–4 hours each, and no labour fees are budgeted for them. The €100 M3 non-labour covers any environment costs they incur (e.g. compute); if a rerunner required payment, it would be deducted from the applicant's €2,400 coordination allocation with hours reduced accordingly. The applicant's 43.64h are for preparation of the reproduction package, coordination, and analysis of results only — **not** for the third-party execution itself. Self-tests and the applicant-team rerun are documented separately and are **not** counted as independent acceptance.
| M4: Release + upstream adaptation | Month 9 | €1,500 | v1.0, install/reproduction manual, integration examples, upstream submissions with feedback-handling records, SBOM, release checksums |

- Third-party replies, adoption, or merges are **not** acceptance criteria.
- Months 9–12 handle agreed-scope rework.

### 10.2 Budget (€15,000 total)

| Item | Amount |
|---|---:|
| Evidence archiving, CI, release verification expenses | €600 |
| Labour at €55/h | €14,400 |
| **Total** | **€15,000** |

Labour: €14,400 ÷ €55/h = **261.82h ≈ 262h**, of which 235.82h planned work + 26h rework reserve.

| Milestone | Non-labour | Labour € | Planned h | Rework reserve | Total h |
|---|---:|---:|---:|---:|---:|
| M1 | €240 | €5,760 | 96.73 | 8 | 104.73 |
| M2 | €200 | €4,800 | 79.27 | 8 | 87.27 |
| M3 | €100 | €2,400 | 38.64 | 5 | 43.64 |
| M4 | €60 | €1,440 | 21.18 | 5 | 26.18 |
| **Total** | **€600** | **€14,400** | **235.82** | **26** | **261.82** |

Hour breakdown:
- M1: interfaces/Schema 14h; adapters + snapshots 24h; general rules + boundary completion 26h; CLI/library/CI/samples 32.73h.
- M2: lifecycle 18h; observation + sampling 22h; boundary corpus 18h; data packaging + docs 21.27h.
- M3: reproduction package preparation + rerun coordination + result analysis 20.64h (applicant); scorecard 18h. Third-party rerun execution is off-budget voluntary input, not applicant hours.
- M4: release/SBOM/docs 10h; upstream adaptation + feedback 11.18h.
- 26h rework listed separately, not double-counted.
- 9 months at 160h/month ≈ 0.182 FTE; budget includes no long-term hosting commitment.

The ~262h is a **forward-looking budget for human work**: software development, code review, dataset integration, reproduction-package preparation, rerun coordination and result analysis, documentation, and upstream coordination by the applicant. Third-party independent rerun execution is separate voluntary input, not counted in the 262h. AI-assisted artefacts do not substitute for this human contribution.

---

## 11. Non-EU exception route: three arguments

Per the eligibility terms, non-qualifying-region applicants must separately support the project's exceptional quality, the applicant's unique technical expertise, and a strong European dimension.

### 11.1 Project's exceptional quality

- Addresses concretely reviewable misjudgment problems in aggregation workflows, providing verdict reasons and evidence rather than bare diffs.
- Source dependency, field scope, time chains, and artifact comparability conditions are part of one output contract.
- Quality is supported by real cases, targeted tests, a valid Schema, a frozen evidence package, and a non-implementer rerun.
- The completed prototype reduces implementation uncertainty; future delivery has defined sample sizes, observation periods, and acceptance boundaries.
- Remaining evidence gaps are explicitly reserved; no claim is made that the exception has been granted.

### 11.2 Applicant's unique technical expertise (Jigao Yi)

Contribution — technical judgment — verifiable evidence mapping (applicant's own work only; AI assistance disclosed per §13):

| Applicant's contribution | Technical judgment demonstrated | Verifiable evidence |
|---|---|---|
| Designed the Market Evidence Check rule system: versioned rules, timeliness judgments, structured reasons, fixed snapshots | Judged that aggregator-style evidence must be reproducible from fixed inputs, not live pages | [MEC project](https://github.com/yijigao/market-evidence-check-devday) — code, rules, test records |
| Diagnosed three dsh adapter faults (tool-result protocol mismatch, 429 retry policy, Claude thinking-signature replay) and wrote the fixes | Judged that cascading endpoint fallbacks mask the real error; added per-endpoint status/body logging to expose it | `docs/evidence/dsh-patches.md` + 4 diffs with SHA-256 and regression records; dsh is DeepSeek's project, the [fork](https://github.com/yijigao/deepseek-harness) carries only the applicant's patches |
| Set PMV's verification principles and acceptance discipline: missing evidence → `undecidable` (never false "consistent"); "zero failures in existing tests (56/56), PMV is a proof of concept" as the public claim standard; ruleset freeze; same-team rerun disclosed as such | Judged that honest scoping beats overclaiming for the exception route | PROMPT-LOG.md entries 17, 25 (2026-10-13 decisions); the detailed rule specification (TASK-PMV-gemini.md) was drafted by an AI agent **to these principles** — the applicant's contribution is the principles and the acceptance discipline, not the line-by-line spec |

- terramike's external verification covered the `muse.md` + OpenAPI path for generating a reusable read-only skill, passing three smoke checks; it is **not** generalised to CLI/directory install-path verification or production maturity. [External report](https://github.com/terramike/xrpl-muse-skill/issues/8#issuecomment-6109879435)
- AI contributions: the PMV implementation was written by an AI agent (Gemini) to an AI-drafted detailed specification (TASK-PMV-gemini.md) based on principles set by the applicant; outline revisions used DeepSeek/GPT-6.1-Sol/Astra Max; this draft was AI-assisted. All are logged in PROMPT-LOG.md. The applicant's claimed expertise is in the **principles, fault diagnosis, and acceptance decisions** — not in hand-writing the detailed spec or every line of code.
- PMV's own evidence and the above credentials jointly support the application; general engineering credentials are not presented as a substitute for domain-specific expertise argumentation.

### 11.3 Concrete European benefit

CodeSupply organises distributed-source metadata into reference datasets distributed through a unified catalogue. The proposed direct service to that process:

1. CodeSupply/AboutCode ingests registry and license-analysis records.
2. PMV checks comparable fields, source dependencies, time chains, and artifact digests before publication.
3. Suspected delays go to a re-check queue; semantic differences and conflicts go to maintainer review; missing-evidence states are preserved.
4. Verdict reasons and evidence citations ship with aggregated records, supporting license review and supply-chain metadata verification by European public bodies, companies, and open-source maintainers.
5. Fixed evidence packages allow offline re-computation, supporting local deployment and audit without depending on applicant-hosted services.

An adaptation example (input records → PMV output → re-check/review handling) will be provided at submission; this is a proposed delivery, not a claim of adoption.

---

## 12. Upstream alignment and public attachments

- AboutCode alignment issue opened: aboutcode-org/purl-validator#39 (2026-10-13, "technical alignment initiated" only; no endorsement claimed).
- Attachments live in the public PMV repository (`docs/evidence/` + `evidence/`); attachment entry requires no login.
- Code: Apache-2.0. Project-owned result data: intended CC-BY-4.0.
- Snapshots carry endpoint, capture time, source license/terms, attribution requirements, trimming notes, and redistribution basis per item. PMV's code license does not cover third-party responses or license texts.
- Materials that cannot be publicly redistributed are represented by publishable minimal excerpts, summaries, and re-fetch instructions — not as the sole offline-acceptance input.
- The submission version is pinned to a fixed commit and snapshot tag; later revisions preserve the submission snapshot.

---

## 13. Use of generative AI in preparing this application

We used generative AI tools for the following, because the applicant was travelling and needed to complete cross-project differentiation research and a runnable prototype verification within three weeks:

- *Research summarisation:* DeepSeek (via API) for literature/differentiation analysis across AboutCode/ScanCode, ClearlyDefined, deps.dev, and OSV.
- *Outline and design drafts:* DeepSeek for the proposal outline structure; Gemini for the demo technical design.
- *Prototype implementation:* Gemini for the PMV prototype code (package metadata verifier), per a detailed technical specification authored by an AI agent (TASK-PMV-gemini.md). No human-written specification original exists for this prototype.
- *Outline revisions:* GPT-6.1-Sol and Astra Max for revising the outline against independent reviewer feedback.
- *This proposal draft:* drafted with AI assistance (Muse) from the reviewed outline; the final text will be written and verified by the applicant (Jigao Yi) before submission.

AI outputs were checked against primary sources (official NLnet pages, upstream project documentation, live API responses, re-runnable code) where feasible; items not yet independently verified are marked as such in the log — the log is a working record, not a certificate of verification. No AI-generated text will be submitted unverified.

A prompt provenance log — model, date/time, prompts, and unedited outputs — is available at https://github.com/yijigao/pkgmeta-verify/blob/main/PROMPT-LOG.md, with prompts under `docs/evidence/prompts/` and outputs under `docs/evidence/outputs/`.

---

## 14. Appendix: claim → evidence → verification-scope index

| Claim in this proposal | Evidence | Verification scope / limits |
|---|---|---|
| 56/56 regression tests, zero failures | `tests/`, `rerun-report.md`, independent rerun logs | Existing test set only; PMV is a proof of concept |
| hatch-vcs real link error | `evidence/real-error-case-v2.md` | Link error publicly reported (deps.dev #220); root-cause mechanism unconfirmed — **not** claimed as officially confirmed |
| validfilepath candidate delay | `evidence/delay-chain.md` | Single observation; historical records unverified — **not** claimed as proven |
| django-flowcontrol INDETERMINATE | `evidence/natural-undecidable-case.md` | Genuine missing evidence, not constructed |
| archgraph-layout suspected delay | `evidence/delay-chain.md` + issue #39 comment | suspect/retracted; contradiction unresolved |
| Independent rerun | `docs/evidence/INDEPENDENT-RERUN-AREN.md` + raw logs | Non-implementer, clean env; same AI team, external rerun may be requested |
| Budget €15,000 / ~262h | §10 tables | Forward-looking human-work budget |
| Applicant credentials | `docs/evidence/CREDENTIALS-INDEX.md` | Per-item claim/evidence/scope; no overclaim |

---

*Draft prepared 2026-10-13/14 for Jigao Yi's review. Applicant = technical lead = future MoU signatory: Jigao Yi (individual application).*
