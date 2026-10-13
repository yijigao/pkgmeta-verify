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
Harvest script to fetch live snapshots for all 4 real cases + 1 synthetic case,
sanitize them into evidence/snapshots/, execute verification, save results,
and generate SHA-256 manifest.
"""

import os
import sys
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from pmv.collector import Collector
from pmv.normalizer import Normalizer
from pmv.verifier import Verifier
from pmv.exporter import Exporter

def harvest():
    ev_dir = os.path.join(base_dir, "evidence")
    rules_path = os.path.join(base_dir, "rules", "rules-v0.1.json")
    collector = Collector()
    normalizer = Normalizer()
    verifier = Verifier(rules_path=rules_path)
    exporter = Exporter(base_evidence_dir=ev_dir)

    real_cases = [
        ("pkg:pypi/typing-extensions@4.12.2", "REAL_ERROR", False),
        ("pkg:pypi/archgraph-layout@2.3.0", "SYNC_DELAY", False),
        ("pkg:npm/esprima@4.0.1", "SEMANTIC_DIVERGENCE", False),
        ("pkg:npm/debug@4.3.4", "INDETERMINATE", True),  # with cross-algo check
    ]

    print("=== Harvesting Real Cases ===")
    for purl, expected_cat, cross_algo in real_cases:
        print(f"\nProcessing {purl} (Expected: {expected_cat})...")
        raw = collector.collect(purl)
        sanitized = exporter.sanitize_raw_bundle(raw)
        snap_path = exporter.save_snapshot(sanitized)
        print(f"  Saved snapshot: {snap_path}")

        norm = normalizer.normalize(sanitized)
        compare_pair = None
        if cross_algo:
            # Cross-algorithm test on debug@4.3.4 artifact
            norm["synthetic"] = True
            art = norm["sources"]["registry"]["artifacts"][0]
            art_sha1 = {"artifact_id": art["artifact_id"], "digests": {"sha1": "3d75be84557f600aa38dd222580f0bb17947c6b6"}, "url": art.get("url")}
            art_sha256 = {"artifact_id": art["artifact_id"], "digests": {"sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}, "url": art.get("url")}
            compare_pair = (art_sha1, art_sha256)

        res = verifier.verify(norm, compare_artifacts=compare_pair)
        res_path = exporter.save_result(res)
        print(f"  Verdict: {res['verdict']['category']} ({res['verdict']['subcode']})")
        print(f"  Confidence: {res['verdict']['confidence']}")
        print(f"  Saved result: {res_path}")
        assert res["verdict"]["category"] == expected_cat, f"Mismatch: expected {expected_cat}, got {res['verdict']['category']}"

    # Synthetic Case: DIGEST_CONFLICT (synthetic=true)
    print("\n=== Generating Synthetic Case (synthetic=true, DIGEST_CONFLICT) ===")
    syn_purl = "pkg:npm/synthetic-fixture@1.0.0"
    syn_raw = {
        "purl": syn_purl,
        "ecosystem": "npm",
        "name": "synthetic-fixture",
        "version": "1.0.0",
        "fetch_timestamp": "2026-10-13T06:00:00Z",
        "synthetic": True,
        "sources": {
            "registry": {
                "source_id": "npm_registry",
                "role": "upstream_registry",
                "endpoint": "https://registry.npmjs.org/synthetic-fixture/1.0.0",
                "status": 200,
                "data": {
                    "name": "synthetic-fixture",
                    "version": "1.0.0",
                    "license": "Apache-2.0",
                    "dist": {
                        "tarball": "https://registry.npmjs.org/synthetic-fixture/-/synthetic-fixture-1.0.0.tgz",
                        "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                    }
                },
                "artifacts": [
                    {
                        "artifact_id": "synthetic-fixture-1.0.0.tgz",
                        "artifact_type": "npm_tarball",
                        "digests": {
                            "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                        }
                    }
                ]
            },
            "synthetic": {
                "source_id": "mirror_b",
                "role": "synthetic_mirror",
                "endpoint": "https://mirror.example.org/synthetic-fixture-1.0.0.tgz",
                "status": 200,
                "artifacts": [
                    {
                        "artifact_id": "synthetic-fixture-1.0.0.tgz",
                        "artifact_type": "npm_tarball",
                        "digests": {
                            "sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
                        }
                    }
                ]
            }
        }
    }
    syn_snap_path = os.path.join(ev_dir, "snapshots", "pkg-npm-synthetic-fixture-1.0.0.json")
    with open(syn_snap_path, "w", encoding="utf-8") as f:
        json.dump(syn_raw, f, indent=2, sort_keys=True)
    print(f"  Saved synthetic snapshot: {syn_snap_path}")

    syn_norm = normalizer.normalize(syn_raw)
    syn_res = verifier.verify(syn_norm)
    syn_res_path = exporter.save_result(syn_res)
    print(f"  Verdict: {syn_res['verdict']['category']} ({syn_res['verdict']['subcode']})")
    print(f"  Saved synthetic result: {syn_res_path}")
    assert syn_res["verdict"]["category"] == "DIGEST_CONFLICT"

    # Generate MANIFEST.sha256
    print("\n=== Generating MANIFEST.sha256 ===")
    rules_file = os.path.join(base_dir, "rules", "rules-v0.1.json")
    schema_file = os.path.join(base_dir, "schemas", "pmv-output.schema.json")
    manifest_path = exporter.generate_manifest(additional_files=[rules_file, schema_file])
    print(f"Manifest written to: {manifest_path}")
    with open(manifest_path, "r", encoding="utf-8") as f:
        print(f.read())

if __name__ == "__main__":
    harvest()
