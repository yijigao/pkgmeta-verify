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
CLI entry point for pkgmeta-verify.
Usage:
    pkgmeta-verify check <purl> [--offline] [--evidence-dir <dir>] [--output <file>]
"""

import argparse
import json
import os
import sys
from typing import Optional

from .collector import Collector, parse_purl
from .exporter import Exporter
from .normalizer import Normalizer
from .verifier import Verifier


def run_check(
    purl: str,
    offline: bool = False,
    evidence_dir: Optional[str] = None,
    rules_path: Optional[str] = None,
    output_path: Optional[str] = None,
    export_evidence: bool = False,
    simulate_cross_algo: bool = False,
) -> int:
    """Run full check for a package coordinate."""
    # Resolve directory paths
    base_pmv_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ev_dir = evidence_dir or os.path.join(base_pmv_dir, "evidence")
    rl_path = rules_path or os.path.join(base_pmv_dir, "rules", "rules-v0.1.json")

    collector = Collector(offline_dir=os.path.join(ev_dir, "snapshots") if offline else None)
    normalizer = Normalizer()
    verifier = Verifier(rules_path=rl_path)
    exporter = Exporter(base_evidence_dir=ev_dir)

    try:
        raw_bundle = collector.collect(purl)
    except Exception as exc:
        print(f"Error collecting metadata for {purl}: {exc}", file=sys.stderr)
        return 1

    norm_data = normalizer.normalize(raw_bundle)

    # Optional cross-algorithm simulation flag for INDETERMINATE demonstration
    compare_pair = None
    if simulate_cross_algo:
        # Construct cross-algorithm pair: sha1 vs sha256 for the same artifact
        norm_data["synthetic"] = True
        artifacts = norm_data["sources"].get("registry", {}).get("artifacts", [])
        if artifacts:
            target_art = artifacts[0]
            art_sha1 = {
                "artifact_id": target_art["artifact_id"],
                "digests": {"sha1": "3d75be84557f600aa38dd222580f0bb17947c6b6"},
                "url": target_art.get("url"),
            }
            art_sha256 = {
                "artifact_id": target_art["artifact_id"],
                "digests": {"sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},
                "url": target_art.get("url"),
            }
            compare_pair = (art_sha1, art_sha256)

    result = verifier.verify(norm_data, compare_artifacts=compare_pair)

    if export_evidence:
        sanitized = exporter.sanitize_raw_bundle(raw_bundle)
        exporter.save_snapshot(sanitized)
        exporter.save_result(result)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, sort_keys=True)

    # Human readable output
    print("=" * 72)
    print(f"PMV Quality Verification: {result['purl']}")
    print(f"Ruleset: {result['ruleset_version']} | Mode: {'OFFLINE_REPLAY' if offline else 'LIVE_FETCH'}")
    print(f"Verdict Category: {result['verdict']['category']} (Subcode: {result['verdict']['subcode']})")
    print(f"Confidence:       {result['verdict']['confidence']}")
    print(f"Summary:          {result['verdict']['summary']}")
    print("-" * 72)
    print(f"Avoided False Positive:")
    print(f"  {result['verdict'].get('avoided_false_positive')}")
    print("-" * 72)
    print("Source Dependencies:")
    for dep in result["provenance_and_dependencies"]["dependency_relations"]:
        print(f"  - [{dep['subject']} -> {dep['upstream']}]: {dep['nature']}")
    print("=" * 72)

    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="pkgmeta-verify",
        description="CodeSupply Package Metadata Verifier (PMV) prototype CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="Verify package metadata against rules")
    check_parser.add_argument("purl", help="Package URL coordinate (e.g. pkg:npm/esprima@4.0.1)")
    check_parser.add_argument("--offline", action="store_true", help="Replay from local evidence snapshot")
    check_parser.add_argument("--evidence-dir", help="Path to evidence storage directory")
    check_parser.add_argument("--rules", help="Path to ruleset JSON")
    check_parser.add_argument("--output", help="Write result JSON to specified file")
    check_parser.add_argument("--export", action="store_true", help="Save minimal snapshot and result to evidence/")
    check_parser.add_argument("--cross-algo-test", action="store_true", help="Trigger cross-algorithm indeterminate check")

    args = parser.parse_args()
    if args.command == "check":
        sys.exit(
            run_check(
                purl=args.purl,
                offline=args.offline,
                evidence_dir=args.evidence_dir,
                rules_path=args.rules,
                output_path=args.output,
                export_evidence=args.export,
                simulate_cross_algo=args.cross_algo_test,
            )
        )


if __name__ == "__main__":
    main()
