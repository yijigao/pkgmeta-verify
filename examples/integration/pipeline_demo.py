#!/usr/bin/env python3
# Copyright 2026 Joey (Jigao Yi)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
CodeSupply PMV - Minimal Executable Integration Example (接入示例)

Demonstrates the end-to-end integration workflow:
  Input Package Records -> PMV Formal Verification Output -> Triage / Re-check & Review Workflow

Uses existing PMV modules (Normalizer, Verifier, Collector) without reinventing wheels.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional

# Ensure pmv package can be imported from parent directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from pmv.collector import Collector
from pmv.normalizer import Normalizer
from pmv.verifier import Verifier


class ActionType(str, Enum):
    APPROVE = "APPROVE"                      # Direct release / cache pass
    SCHEDULE_RECHECK = "SCHEDULE_RECHECK"    # Put in delayed recheck queue (ingestion lag)
    COMPLIANCE_TRIAGE = "COMPLIANCE_TRIAGE"  # Legal / OSS compliance review
    SECURITY_BLOCK = "SECURITY_BLOCK"        # Immediate quarantine & alert
    MANUAL_REVIEW = "MANUAL_REVIEW"          # Missing evidence fallback review


@dataclass
class TriageDecision:
    purl: str
    category: str
    subcode: str
    confidence: float
    action: ActionType
    reason: str
    recheck_interval_seconds: Optional[int] = None
    quarantine_status: bool = False
    audit_notes: str = ""


class IngestionGatePipeline:
    """
    Downstream Ingestion Gate demonstrating how a software repository,
    SCA scanner, or enterprise registry proxy integrates PMV.
    """

    def __init__(self, rules_path: Optional[str] = None):
        self.rules_path = rules_path or os.path.join(BASE_DIR, "rules", "rules-v0.1.json")
        self.verifier = Verifier(rules_path=self.rules_path)
        self.normalizer = Normalizer()
        self.recheck_queue: List[Dict[str, Any]] = []

    def evaluate_record(self, raw_bundle: Dict[str, Any]) -> Dict[str, Any]:
        """Step 1 & 2: Normalize input record and invoke PMV engine."""
        norm_data = self.normalizer.normalize(raw_bundle)

        # Cross-algorithm fixture handling for demonstration
        compare_pair = None
        if raw_bundle.get("name") == "debug" and raw_bundle.get("synthetic"):
            norm_data["synthetic"] = True
            art = norm_data["sources"]["registry"]["artifacts"][0]
            art_sha1 = {
                "artifact_id": art["artifact_id"],
                "digests": {"sha1": "3d75be84557f600aa38dd222580f0bb17947c6b6"},
                "url": art.get("url"),
            }
            art_sha256 = {
                "artifact_id": art["artifact_id"],
                "digests": {"sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},
                "url": art.get("url"),
            }
            compare_pair = (art_sha1, art_sha256)

        pmv_output = self.verifier.verify(norm_data, compare_artifacts=compare_pair)
        return pmv_output

    def triage_verdict(self, pmv_output: Dict[str, Any]) -> TriageDecision:
        """
        Step 3: Downstream Re-check & Review Triage Decision Flow.
        Maps PMV 6-category verdicts to operational actions.
        """
        verdict = pmv_output["verdict"]
        cat = verdict["category"]
        subcode = verdict["subcode"]
        conf = verdict["confidence"]
        purl = pmv_output["purl"]

        # Retracted fault attribution: STANDARDS_CONTRADICTION carries no
        # unilateral fault claim (typing-extensions case). Route to human review,
        # never to SECURITY_BLOCK, regardless of the top-level category.
        if subcode == "STANDARDS_CONTRADICTION":
            return TriageDecision(
                purl=purl,
                category=cat,
                subcode=subcode,
                confidence=conf,
                action=ActionType.MANUAL_REVIEW,
                reason="Standards contradiction: sources comply with different specs. No fault attributed.",
                audit_notes="Route to human analyst; do NOT treat as security incident.",
            )

        if cat == "CONSISTENT":
            return TriageDecision(
                purl=purl,
                category=cat,
                subcode=subcode,
                confidence=conf,
                action=ActionType.APPROVE,
                reason="Cross-source metadata consistent within the checked fields. NOT a safety guarantee for production deployment.",
                audit_notes="Consistency verdict only; deployment decisions require separate review.",
            )

        elif cat == "SYNC_DELAY":
            # Downstream ingestion lag within 24h tolerance.
            # Crucial: Avoid false-positive tampering alarms! Schedule delayed re-check.
            return TriageDecision(
                purl=purl,
                category=cat,
                subcode=subcode,
                confidence=conf,
                action=ActionType.SCHEDULE_RECHECK,
                reason="Downstream indexer ingestion lag detected within 24h normal window. Scheduled for re-check.",
                recheck_interval_seconds=300,  # e.g. re-check in 5 minutes
                audit_notes="Avoided false positive: Do not alarm security on transient sync delays.",
            )

        elif cat == "SEMANTIC_DIVERGENCE":
            # Legitimate differing perspectives (e.g., license conjunction mismatch).
            return TriageDecision(
                purl=purl,
                category=cat,
                subcode=subcode,
                confidence=conf,
                action=ActionType.COMPLIANCE_TRIAGE,
                reason="Semantic divergence in metadata representation. Route to Legal/Compliance for review.",
                audit_notes=f"Audit details: {verdict.get('summary')}",
            )

        elif cat in ("REAL_ERROR", "DIGEST_CONFLICT"):
            # Conflicting checksums or contradictory metadata.
            return TriageDecision(
                purl=purl,
                category=cat,
                subcode=subcode,
                confidence=conf,
                action=ActionType.SECURITY_BLOCK,
                reason="Metadata conflict or digest mismatch. Ingestion blocked pending review.",
                quarantine_status=True,
                audit_notes="Quarantine artifact and notify reviewers; block is precautionary, not proof of malice.",
            )

        elif cat == "INDETERMINATE":
            # Evidence vacuum or incomparable cross-algorithm hashing.
            return TriageDecision(
                purl=purl,
                category=cat,
                subcode=subcode,
                confidence=conf,
                action=ActionType.MANUAL_REVIEW,
                reason="Metadata consistency is undecidable (missing evidence or incomparable data).",
                audit_notes="Do NOT guess default PASS/FAIL; route to secondary human analyst.",
            )

        else:
            raise ValueError(f"Unknown PMV category: {cat}")

    def execute_recheck_cycle(self, scheduled_item: Dict[str, Any]) -> TriageDecision:
        """
        Demonstrates the Re-check Execution Workflow:
        Simulates polling downstream indexer when initial status was 404.
        """
        print(f"  [RE-CHECK WORKFLOW] Polling downstream indexer for {scheduled_item['purl']}...")
        # Simulate time passing and downstream indexer synchronizing to 200 OK:
        resolved_bundle = json.loads(json.dumps(scheduled_item["raw_bundle"]))
        deps_data = resolved_bundle["sources"]["deps_dev"]
        deps_data["status"] = 200
        deps_data["data"] = {
            "versionKey": {"system": "PYPI", "name": "validfilepath", "version": "0.1"},
            "publishedAt": "2026-10-13T09:59:55Z",
            "licenses": ["MIT"],
            "links": [],
        }
        resolved_bundle["fetch_timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Re-run PMV verification
        recheck_pmv_output = self.evaluate_record(resolved_bundle)
        recheck_decision = self.triage_verdict(recheck_pmv_output)
        return recheck_decision


def load_sample_records() -> List[Dict[str, Any]]:
    """Constructs a representative batch of input records across all PMV categories."""
    snapshots_dir = os.path.join(BASE_DIR, "evidence", "snapshots")
    supplementary_dir = os.path.join(BASE_DIR, "evidence", "supplementary")

    records = []

    # 1. Clean Consistent Case (Synthetic baseline)
    records.append({
        "purl": "pkg:npm/example-clean@1.0.0",
        "ecosystem": "npm",
        "name": "example-clean",
        "version": "1.0.0",
        "fetch_timestamp": "2026-10-13T12:00:00Z",
        "synthetic": True,
        "sources": {
            "registry": {
                "source_id": "npm_registry",
                "role": "upstream_registry",
                "endpoint": "https://registry.npmjs.org/example-clean/1.0.0",
                "status": 200,
                "data": {
                    "name": "example-clean",
                    "version": "1.0.0",
                    "license": "MIT",
                    "dist": {
                        "tarball": "https://registry.npmjs.org/example-clean/-/example-clean-1.0.0.tgz",
                        "shasum": "0123456789abcdef0123456789abcdef01234567",
                    },
                },
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "role": "derived_indexer",
                "endpoint": "https://api.deps.dev/v3/systems/npm/packages/example-clean/versions/1.0.0",
                "status": 200,
                "data": {
                    "versionKey": {"system": "NPM", "name": "example-clean", "version": "1.0.0"},
                    "publishedAt": "2026-10-13T12:00:00Z",
                    "licenses": ["MIT"],
                    "links": [],
                },
            },
        },
    })

    # 2. Semantic Divergence: pkg:npm/esprima@4.0.1
    esprima_path = os.path.join(snapshots_dir, "pkg-npm-esprima-4.0.1.json")
    if os.path.exists(esprima_path):
        records.append(json.load(open(esprima_path, encoding="utf-8")))

    # 3. Standards Contradiction (Real Error): pkg:pypi/typing-extensions@4.12.2
    typing_path = os.path.join(snapshots_dir, "pkg-pypi-typing-extensions-4.12.2.json")
    if os.path.exists(typing_path):
        records.append(json.load(open(typing_path, encoding="utf-8")))

    # 4. Digest Conflict: pkg:npm/synthetic-fixture@1.0.0
    synth_path = os.path.join(snapshots_dir, "pkg-npm-synthetic-fixture-1.0.0.json")
    if os.path.exists(synth_path):
        records.append(json.load(open(synth_path, encoding="utf-8")))

    # 5. Natural Undecidable: pkg:pypi/django-flowcontrol@0.0.21
    df_path = os.path.join(supplementary_dir, "snapshot-pkg-pypi-django-flowcontrol-0.0.21.json")
    if os.path.exists(df_path):
        records.append(json.load(open(df_path, encoding="utf-8")))

    # 6. Ingestion Sync Delay: pkg:pypi/validfilepath@0.1
    # DEMO NOTE: the timestamps below are hand-filled from a single observation
    # session for pipeline demonstration; this is a RECONSTRUCTED DEMO RECORD,
    # not a measured proof. Do not cite as primary evidence.
    sync_record = {
        "purl": "pkg:pypi/validfilepath@0.1",
        "ecosystem": "pypi",
        "name": "validfilepath",
        "version": "0.1",
        "fetch_timestamp": "2026-10-13T10:07:26Z",
        "evaluation_timestamp": "2026-10-13T10:15:00Z",
        "synthetic": True,  # reconstructed demo record; not measured proof,
        "sources": {
            "registry": {
                "source_id": "pypi_json",
                "role": "upstream_registry",
                "status": 200,
                "data": {
                    "info": {"name": "validfilepath", "version": "0.1", "license": "MIT"},
                    "releases": {
                        "0.1": [
                            {
                                "filename": "validfilepath-0.1.tar.gz",
                                "upload_time_iso_8601": "2026-10-13T09:59:55Z",
                            }
                        ]
                    },
                },
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "role": "derived_indexer",
                "status": 404,
                "data": {
                    "body": "version not found",
                },
                "subsequent_observation": {
                    "status": 200,
                    "observed_at": "2026-10-13T10:11:15Z",
                    "published_at": "2026-10-13T09:59:55Z",
                },
            },
        },
    }
    records.append(sync_record)

    return records


def run_pipeline():
    """Main execution entrypoint for integration demonstration."""
    print("=" * 80)
    print("CodeSupply PMV Integration Pipeline Example (Minimal Executable)")
    print(f"Started at: {datetime.now(timezone.utc).isoformat()} (UTC)")
    print("=" * 80)

    pipeline = IngestionGatePipeline()
    batch = load_sample_records()
    print(f"Loaded {len(batch)} input package records for quality verification.\n")
    print("NOTE: records flagged synthetic=True are RECONSTRUCTED DEMO inputs;")
    print("their timestamps are illustrative, not measured proof.\n")

    audit_log = []

    for idx, raw_record in enumerate(batch, 1):
        purl = raw_record.get("purl")
        print(f"[{idx}/{len(batch)}] Processing Ingestion: {purl}")

        # Step 1 & 2: PMV Evaluation
        pmv_output = pipeline.evaluate_record(raw_record)
        verdict = pmv_output["verdict"]

        print(f"  PMV Verdict:    {verdict['category']} ({verdict['subcode']})")
        print(f"  Confidence:     {verdict['confidence']:.2f}")
        print(f"  Summary:        {verdict['summary']}")

        # Demo provenance stamping (survives re-runs: applied at generation time).
        # Records flagged synthetic=True are reconstructed demo inputs, not measured proof.
        is_demo = bool(raw_record.get("synthetic"))
        if is_demo:
            verdict = dict(verdict)
            verdict["summary"] = "[DEMO RECONSTRUCTION — not measured proof] " + str(verdict.get("summary", ""))
            details = verdict.get("details")
            if isinstance(details, str):
                verdict["details"] = "[DEMO RECONSTRUCTION — not measured proof] " + details

        # Step 3: Triage Decision
        decision = pipeline.triage_verdict(pmv_output)
        print(f"  --> Action:     [{decision.action.value}]")
        print(f"  --> Policy:     {decision.reason}")
        if decision.quarantine_status:
            print(f"  [QUARANTINE]    Artifact quarantined from build pipeline.")

        # Special Step: Re-check flow demonstration for SYNC_DELAY
        if decision.action == ActionType.SCHEDULE_RECHECK:
            print(f"  [SCHEDULER]     Queued for retry in {decision.recheck_interval_seconds}s...")
            # Execute simulated re-check step
            recheck_decision = pipeline.execute_recheck_cycle({"purl": purl, "raw_bundle": raw_record})
            print(f"  [RE-CHECK PASS] Post-delay outcome: [{recheck_decision.action.value}] - {recheck_decision.reason}")
            audit_log.append({
                "purl": purl,
                "record_provenance": "DEMO_RECONSTRUCTION" if is_demo else "measured",
                "initial_verdict": verdict,
                "initial_action": decision.action.value,
                "recheck_executed": True,
                "final_action": recheck_decision.action.value,
            })
        else:
            audit_log.append({
                "purl": purl,
                "record_provenance": "DEMO_RECONSTRUCTION" if is_demo else "measured",
                "initial_verdict": verdict,
                "initial_action": decision.action.value,
                "recheck_executed": False,
                "final_action": decision.action.value,
            })

        print("-" * 80)

    # Save integration audit log
    out_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_pipeline_run.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(audit_log, f, indent=2, sort_keys=True)

    print("\nPipeline execution completed successfully.")
    print(f"Saved integration audit log to: {out_file}")
    print("=" * 80)


if __name__ == "__main__":
    run_pipeline()
