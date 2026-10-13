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
Regression tests capturing all Astra rev2 bug findings:
1. Missing upstream publication time MUST NOT output SYNC_DELAY -> outputs undecidable.
2. Single 404 observation without subsequent appearance observation -> outputs undecidable.
3. Complete temporal observation chain -> outputs SYNC_DELAY with provable delay range.
4. Empty or missing evidence MUST NOT return CONSISTENT -> outputs undecidable.
5. Matching filename alone without artifact-level evidence -> outputs undecidable.
6. Digest case normalization is logged with raw/normalized values in audit trail.
7. Cross-algorithm comparison yields undecidable.
8. Real error removes DOWNSTREAM_PARSING_ERROR and parser blame assertion.
9. Synthetic flag in output strictly matches input.
"""

import unittest
from pmv.verifier import Verifier


class TestVerifierRulesRegression(unittest.TestCase):
    def setUp(self):
        self.verifier = Verifier()

    def _base_norm_data(self):
        return {
            "purl": "pkg:test/sample@1.0.0",
            "ecosystem": "npm",
            "name": "sample",
            "version": "1.0.0",
            "fetch_timestamp": "2026-10-13T12:00:00Z",
            "synthetic": False,
            "sources": {},
            "dependency_relations": [],
        }

    def test_missing_published_at_yields_undecidable_not_sync_delay(self):
        """Bug 1: Lacking upstream publication timestamp must yield undecidable, NEVER SYNC_DELAY."""
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "test_registry",
                "role": "upstream_registry",
                "status": 200,
                "available": True,
                "published_at": None,  # Missing publication time!
                "artifacts": [],
                "licenses": ["MIT"],
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "role": "derived_indexer",
                "status": 404,  # Downstream missing
                "available": False,
            },
        }
        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]
        self.assertNotEqual(verdict["category"], "SYNC_DELAY")
        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "undecidable")
        self.assertLessEqual(verdict["confidence"], 0.5)
        self.assertIn("missing upstream publication timestamp", verdict["summary"].lower())

    def test_single_404_observation_yields_undecidable_not_proven_delay(self):
        """Bug 1 & 5: Single 404 observation without subsequent appearance observation yields undecidable."""
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "test_registry",
                "role": "upstream_registry",
                "status": 200,
                "available": True,
                "published_at": "2026-10-13T11:45:00Z",
                "artifacts": [],
                "licenses": ["MIT"],
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "role": "derived_indexer",
                "status": 404,
                "available": False,
                # No subsequent_observation!
            },
        }
        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]
        self.assertNotEqual(verdict["category"], "SYNC_DELAY")
        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "undecidable")
        self.assertIn("suspected", verdict["summary"].lower())

    def test_complete_temporal_chain_yields_proven_sync_delay(self):
        """Bug 5: Three-stage temporal observation chain proves delay range within window."""
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "test_registry",
                "role": "upstream_registry",
                "status": 200,
                "available": True,
                "published_at": "2026-10-13T11:45:00Z",
                "artifacts": [],
                "licenses": ["MIT"],
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "role": "derived_indexer",
                "status": 404,
                "available": False,
                "subsequent_observation": {
                    "observed_at": "2026-10-13T12:30:00Z",
                    "status": 200,
                    "published_at": "2026-10-13T11:45:00Z",
                },
            },
        }
        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]
        self.assertEqual(verdict["category"], "SYNC_DELAY")
        self.assertEqual(verdict["subcode"], "DOWNSTREAM_INGESTION_LAG")
        self.assertIn("provable delay range", verdict["details"].lower())

    def test_empty_evidence_yields_undecidable_not_consistent(self):
        """Bug 1: Empty or missing evidence must NEVER default to CONSISTENT."""
        # Scenario A: empty sources
        norm_data_a = self._base_norm_data()
        norm_data_a["sources"] = {}
        res_a = self.verifier.verify(norm_data_a)
        self.assertNotEqual(res_a["verdict"]["category"], "CONSISTENT")
        self.assertEqual(res_a["verdict"]["category"], "INDETERMINATE")
        self.assertEqual(res_a["verdict"]["subcode"], "undecidable")

        # Scenario B: only 1 available source
        norm_data_b = self._base_norm_data()
        norm_data_b["sources"] = {
            "registry": {
                "source_id": "registry",
                "status": 200,
                "available": True,
                "licenses": ["MIT"],
            }
        }
        res_b = self.verifier.verify(norm_data_b)
        self.assertNotEqual(res_b["verdict"]["category"], "CONSISTENT")
        self.assertEqual(res_b["verdict"]["category"], "INDETERMINATE")
        self.assertEqual(res_b["verdict"]["subcode"], "undecidable")

    def test_empty_metadata_fields_yield_undecidable(self):
        """Bug 1: Two available sources but empty metadata fields must not yield CONSISTENT."""
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "src_a": {"source_id": "src_a", "status": 200, "available": True, "licenses": [], "artifacts": []},
            "src_b": {"source_id": "src_b", "status": 200, "available": True, "licenses": [], "artifacts": []},
        }
        res = self.verifier.verify(norm_data)
        self.assertNotEqual(res["verdict"]["category"], "CONSISTENT")
        self.assertEqual(res["verdict"]["category"], "INDETERMINATE")
        self.assertEqual(res["verdict"]["subcode"], "undecidable")

    def test_filename_only_matching_yields_undecidable(self):
        """Bug 1: Artifact identity cannot be asserted solely on matching filenames without artifact-level evidence."""
        norm_data = self._base_norm_data()
        art_a = {"artifact_id": "foo-1.0.0.tgz"}  # No digest, no url, no file list
        art_b = {"artifact_id": "foo-1.0.0.tgz"}  # No digest, no url, no file list

        res = self.verifier.verify(norm_data, compare_artifacts=(art_a, art_b))
        verdict = res["verdict"]
        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "undecidable")
        self.assertIn("filename alone", verdict["summary"].lower() + verdict["details"].lower())

    def test_digest_case_normalization_logged_in_audit_trail(self):
        """Bug 1: Hex digest case differences are normalized and explicitly logged with raw/norm values."""
        norm_data = self._base_norm_data()
        raw_hash_upper = "3D75BE84557F600AA38DD222580F0BB17947C6B6"
        raw_hash_lower = "3d75be84557f600aa38dd222580f0bb17947c6b6"

        art_a = {
            "artifact_id": "pkg-1.0.0.tgz",
            "digests": {"sha1": raw_hash_upper},
            "url": "https://example.org/pkg-1.0.0.tgz",
        }
        art_b = {
            "artifact_id": "pkg-1.0.0.tgz",
            "digests": {"sha1": raw_hash_lower},
            "url": "https://example.org/pkg-1.0.0.tgz",
        }

        res = self.verifier.verify(norm_data, compare_artifacts=(art_a, art_b))
        # After normalization they match, so verify doesn't flag DIGEST_CONFLICT
        audit_trail = res["decision_audit_trail"]
        norm_entries = [e for e in audit_trail if e.get("rule_id") == "DIGEST_03_NORMALIZATION"]
        self.assertTrue(len(norm_entries) > 0, "Must record DIGEST_03_NORMALIZATION in audit trail")
        entry = norm_entries[0]
        self.assertEqual(entry["original_values"]["source_a"], raw_hash_upper)
        self.assertEqual(entry["normalized_values"]["source_a"], raw_hash_lower)

    def test_cross_algorithm_comparison_yields_undecidable(self):
        """Bug 1: Comparing sha1 against sha256 outputs undecidable without exception."""
        norm_data = self._base_norm_data()
        art_a = {
            "artifact_id": "pkg-1.0.0.tgz",
            "digests": {"sha1": "3d75be84557f600aa38dd222580f0bb17947c6b6"},
            "url": "https://example.org/pkg-1.0.0.tgz",
        }
        art_b = {
            "artifact_id": "pkg-1.0.0.tgz",
            "digests": {"sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},
            "url": "https://example.org/pkg-1.0.0.tgz",
        }

        res = self.verifier.verify(norm_data, compare_artifacts=(art_a, art_b))
        verdict = res["verdict"]
        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "undecidable")
        self.assertIn("different algorithms", verdict["summary"].lower())

    def test_real_error_no_downstream_parser_blame(self):
        """Bug 4: Real error must NOT assert DOWNSTREAM_PARSING_ERROR or unilateral parser blame."""
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "pypi_json",
                "available": True,
                "status": 200,
                "license_classifiers": ["License :: OSI Approved :: Python Software Foundation License"],
                "licenses": [],
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "available": True,
                "status": 200,
                "licenses": ["non-standard"],
            },
            "clearlydefined": {
                "source_id": "clearlydefined",
                "available": True,
                "status": 200,
                "declared_license": "Python-2.0.1",
            },
        }

        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]
        self.assertEqual(verdict["category"], "REAL_ERROR")
        self.assertNotEqual(verdict["subcode"], "DOWNSTREAM_PARSING_ERROR")
        self.assertEqual(verdict["subcode"], "STANDARDS_CONTRADICTION")
        self.assertNotIn("parsing failure", verdict["details"].lower())
        self.assertIn("cannot be separated", verdict["details"].lower())

    def test_synthetic_flag_strictly_preserved(self):
        """Bug 3: Synthetic input flag must be preserved identically in output."""
        # True input
        norm_true = self._base_norm_data()
        norm_true["synthetic"] = True
        res_true = self.verifier.verify(norm_true)
        self.assertTrue(res_true["synthetic"])

        # False input
        norm_false = self._base_norm_data()
        norm_false["synthetic"] = False
        res_false = self.verifier.verify(norm_false)
        self.assertFalse(res_false["synthetic"])


if __name__ == "__main__":
    unittest.main()
