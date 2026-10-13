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
Regression tests capturing all Astra rev2 and rev3 bug findings:
Rev2:
1. Missing upstream publication time MUST NOT output SYNC_DELAY -> outputs undecidable.
2. Single 404 observation without subsequent appearance observation -> outputs undecidable.
3. Complete temporal observation chain -> outputs SYNC_DELAY with provable delay range.
4. Empty or missing evidence MUST NOT return CONSISTENT -> outputs undecidable.
5. Empty metadata fields yield undecidable.
6. Cross-algorithm comparison yields undecidable.
7. Synthetic flag in output strictly matches input.

Rev3 fixes:
1. Same filename, different digests, unproven artifact identity -> outputs ARTIFACT_IDENTITY_UNPROVEN, NOT DIGEST_CONFLICT.
2. Base64 digests differing only in case are compared by decoded bytes (do NOT match); unsupported encodings yield ENCODING_UNSUPPORTED.
3. Subsequent observation HTTP 404, missing time, or time inversion MUST NOT output SYNC_DELAY -> outputs undecidable.
4. MIT vs Apache-2.0 yields SEMANTIC_DIVERGENCE, missing comparable fields yields undecidable, prohibited from judging CONSISTENT without comparison.
5. Missing artifact LICENSE text evidence MUST NOT output REAL_ERROR -> outputs undecidable without hardcoded assertions.
6. Demoted suspect/retracted delay cases yield undecidable (suspected delay).
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

    # =========================================================================
    # Rev2 Baselines
    # =========================================================================

    def test_missing_published_at_yields_undecidable_not_sync_delay(self):
        """Bug 1: Lacking upstream publication timestamp must yield undecidable, NEVER SYNC_DELAY."""
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "test_registry",
                "role": "upstream_registry",
                "status": 200,
                "available": True,
                "published_at": None,
                "artifacts": [],
                "licenses": ["MIT"],
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "role": "derived_indexer",
                "status": 404,
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
        norm_data["fetch_timestamp"] = "2026-10-12T12:00:00Z"
        norm_data["evaluation_timestamp"] = "2026-10-12T13:00:00Z"
        norm_data["sources"] = {
            "registry": {
                "source_id": "test_registry",
                "role": "upstream_registry",
                "status": 200,
                "available": True,
                "published_at": "2026-10-12T11:45:00Z",
                "artifacts": [],
                "licenses": ["MIT"],
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "role": "derived_indexer",
                "status": 404,
                "available": False,
                "subsequent_observation": {
                    "observed_at": "2026-10-12T12:30:00Z",
                    "status": 200,
                    "published_at": "2026-10-12T11:45:00Z",
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
        norm_data_a = self._base_norm_data()
        norm_data_a["sources"] = {}
        res_a = self.verifier.verify(norm_data_a)
        self.assertNotEqual(res_a["verdict"]["category"], "CONSISTENT")
        self.assertEqual(res_a["verdict"]["category"], "INDETERMINATE")
        self.assertEqual(res_a["verdict"]["subcode"], "undecidable")

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

    def test_synthetic_flag_strictly_preserved(self):
        """Bug 3: Synthetic input flag must be preserved identically in output."""
        norm_true = self._base_norm_data()
        norm_true["synthetic"] = True
        res_true = self.verifier.verify(norm_true)
        self.assertTrue(res_true["synthetic"])

        norm_false = self._base_norm_data()
        norm_false["synthetic"] = False
        res_false = self.verifier.verify(norm_false)
        self.assertFalse(res_false["synthetic"])

    # =========================================================================
    # Rev3 Fix 1: Artifact Identity Provenance (DIGEST_CONFLICT vs ARTIFACT_IDENTITY_UNPROVEN)
    # =========================================================================

    def test_rev3_fix1_unproven_identity_different_digests_yields_artifact_identity_unproven(self):
        """
        Fix 1: Same filename, different digests, but no evidence binding to same artifact
        MUST NOT return DIGEST_CONFLICT; MUST output INDETERMINATE with subcode ARTIFACT_IDENTITY_UNPROVEN.
        """
        norm_data = self._base_norm_data()
        # Same filename, different hashes, NO url, NO file list, NO release record
        art_a = {
            "artifact_id": "sample-1.0.0.tgz",
            "digests": {"sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
        }
        art_b = {
            "artifact_id": "sample-1.0.0.tgz",
            "digests": {"sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},
        }
        res = self.verifier.verify(norm_data, compare_artifacts=(art_a, art_b))
        verdict = res["verdict"]

        self.assertNotEqual(verdict["category"], "DIGEST_CONFLICT")
        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "ARTIFACT_IDENTITY_UNPROVEN")
        self.assertIn("unproven", verdict["summary"].lower())

    def test_rev3_fix1_proven_identity_different_digests_yields_digest_conflict(self):
        """
        Fix 1 (Positive): When artifact identity IS bound (e.g. shared release record or download URL),
        different digests correctly prove DIGEST_CONFLICT.
        """
        norm_data = self._base_norm_data()
        art_a = {
            "artifact_id": "sample-1.0.0.tgz",
            "digests": {"sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
            "release_record": "pkg:npm/sample@1.0.0",
            "url": "https://registry.npmjs.org/sample/-/sample-1.0.0.tgz",
        }
        art_b = {
            "artifact_id": "sample-1.0.0.tgz",
            "digests": {"sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},
            "release_record": "pkg:npm/sample@1.0.0",
            "url": "https://mirror.example.org/sample-1.0.0.tgz",
        }
        res = self.verifier.verify(norm_data, compare_artifacts=(art_a, art_b))
        verdict = res["verdict"]

        self.assertEqual(verdict["category"], "DIGEST_CONFLICT")
        self.assertEqual(verdict["subcode"], "ARTIFACT_DIGEST_MISMATCH")

    # =========================================================================
    # Rev3 Fix 2: Base64 Byte Decoding & Case Sensitivity (No silent .lower())
    # =========================================================================

    def test_rev3_fix2_base64_case_difference_does_not_silently_match(self):
        """
        Fix 2: Two genuine 32-byte base64 digests differing only in case must be decoded to bytes and NOT silently match via .lower().
        """
        norm_data = self._base_norm_data()
        # Genuine 32-byte SHA-256 base64 vectors where .lower() matches but decoded bytes differ
        art_a = {
            "artifact_id": "sample-1.0.0.tgz",
            "digests": {"sha256": "base64:LPJNul+wow4m6DsqxbninhsWHlwfp0JecwQzYpOLmCQ="},
            "release_record": "pkg:npm/sample@1.0.0",
        }
        art_b = {
            "artifact_id": "sample-1.0.0.tgz",
            "digests": {"sha256": "base64:LPJNuL+wow4m6DsqxbninhsWHlwfp0JecwQzYpOLmCQ="},
            "release_record": "pkg:npm/sample@1.0.0",
        }
        res = self.verifier.verify(norm_data, compare_artifacts=(art_a, art_b))
        verdict = res["verdict"]

        # Must NOT pass or judge matching!
        self.assertEqual(verdict["category"], "DIGEST_CONFLICT")
        self.assertEqual(verdict["subcode"], "ARTIFACT_DIGEST_MISMATCH")

    def test_rev3_fix2_unsupported_encoding_yields_encoding_unsupported(self):
        """
        Fix 2: When digest encoding is unknown/unsupported, strictly outputs INDETERMINATE with subcode ENCODING_UNSUPPORTED.
        """
        norm_data = self._base_norm_data()
        art_a = {
            "artifact_id": "sample-1.0.0.tgz",
            "digests": {"sha256": {"encoding": "base58", "value": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"}},
            "release_record": "pkg:npm/sample@1.0.0",
        }
        art_b = {
            "artifact_id": "sample-1.0.0.tgz",
            "digests": {"sha256": {"encoding": "base58", "value": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"}},
            "release_record": "pkg:npm/sample@1.0.0",
        }
        res = self.verifier.verify(norm_data, compare_artifacts=(art_a, art_b))
        verdict = res["verdict"]

        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "ENCODING_UNSUPPORTED")
        self.assertIn("unsupported", verdict["summary"].lower() + verdict["details"].lower())

    def test_rev3_fix2_hex_case_difference_matches_at_byte_level(self):
        """
        Fix 2 (Hex): Hex digests differing only in case decode to identical bytes and match cleanly.
        """
        norm_data = self._base_norm_data()
        art_a = {
            "artifact_id": "sample-1.0.0.tgz",
            "digests": {"sha1": "3D75BE84557F600AA38DD222580F0BB17947C6B6"},
            "release_record": "pkg:npm/sample@1.0.0",
        }
        art_b = {
            "artifact_id": "sample-1.0.0.tgz",
            "digests": {"sha1": "3d75be84557f600aa38dd222580f0bb17947c6b6"},
            "release_record": "pkg:npm/sample@1.0.0",
        }
        res = self.verifier.verify(norm_data, compare_artifacts=(art_a, art_b))
        # No conflict flagged
        self.assertNotEqual(res["verdict"]["category"], "DIGEST_CONFLICT")
        audit_trail = res["decision_audit_trail"]
        decode_entries = [e for e in audit_trail if e.get("rule_id") == "DIGEST_03_BYTE_DECODING"]
        self.assertTrue(len(decode_entries) > 0)
        self.assertEqual(decode_entries[0]["outcome"], "DECODED")

    # =========================================================================
    # Rev3 Fix 3: Sync Delay Validation (HTTP 200, valid time, forward order)
    # =========================================================================

    def test_rev3_fix3_subsequent_observation_404_yields_undecidable(self):
        """
        Fix 3: Subsequent observation remaining 404 (non-success) MUST NOT output SYNC_DELAY.
        """
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "registry",
                "status": 200,
                "available": True,
                "published_at": "2026-10-13T11:00:00Z",
                "licenses": ["MIT"],
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "status": 404,
                "available": False,
                "subsequent_observation": {
                    "observed_at": "2026-10-13T12:00:00Z",
                    "status": 404,  # Still 404!
                },
            },
        }
        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]

        self.assertNotEqual(verdict["category"], "SYNC_DELAY")
        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "undecidable")
        self.assertIn("non-success", verdict["summary"].lower() + verdict["details"].lower())

    def test_rev3_fix3_subsequent_observation_missing_time_yields_undecidable(self):
        """
        Fix 3: Subsequent observation missing timestamp MUST NOT output SYNC_DELAY.
        """
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "registry",
                "status": 200,
                "available": True,
                "published_at": "2026-10-13T11:00:00Z",
                "licenses": ["MIT"],
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "status": 404,
                "available": False,
                "subsequent_observation": {
                    "status": 200,
                    "observed_at": None,  # Missing timestamp!
                },
            },
        }
        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]

        self.assertNotEqual(verdict["category"], "SYNC_DELAY")
        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "undecidable")

    def test_rev3_fix3_time_inversion_yields_undecidable(self):
        """
        Fix 3: Inverted observation order (t_observed_after <= t_observed_before) MUST NOT output SYNC_DELAY.
        """
        norm_data = self._base_norm_data()
        norm_data["fetch_timestamp"] = "2026-10-13T12:00:00Z"
        norm_data["sources"] = {
            "registry": {
                "source_id": "registry",
                "status": 200,
                "available": True,
                "published_at": "2026-10-13T11:00:00Z",
                "licenses": ["MIT"],
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "status": 404,
                "available": False,
                "subsequent_observation": {
                    "status": 200,
                    "observed_at": "2026-10-13T11:30:00Z",  # Before fetch_timestamp (12:00)!
                },
            },
        }
        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]

        self.assertNotEqual(verdict["category"], "SYNC_DELAY")
        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "undecidable")
        self.assertIn("inversion", verdict["summary"].lower() + verdict["details"].lower())

    # =========================================================================
    # Rev3 Fix 4: License Comparison (MIT vs Apache-2.0 & Incomparable Fields)
    # =========================================================================

    def test_rev3_fix4_mit_vs_apache_yields_semantic_divergence_not_consistent(self):
        """
        Fix 4: Two sources declaring MIT vs Apache-2.0 is a definite contradiction;
        MUST output SEMANTIC_DIVERGENCE, strictly prohibited from judging CONSISTENT.
        """
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "registry",
                "status": 200,
                "available": True,
                "licenses": ["MIT"],
            },
            "clearlydefined": {
                "source_id": "clearlydefined",
                "status": 200,
                "available": True,
                "declared_license": "Apache-2.0",
                "discovered_licenses": ["Apache-2.0"],
            },
        }
        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]

        self.assertNotEqual(verdict["category"], "CONSISTENT")
        self.assertEqual(verdict["category"], "SEMANTIC_DIVERGENCE")
        self.assertEqual(verdict["subcode"], "LICENSE_DECLARATION_DISCREPANCY")

    def test_rev3_fix4_missing_comparable_license_field_yields_undecidable(self):
        """
        Fix 4: When one source declares a license and another source lacks comparable fields,
        MUST output INDETERMINATE with subcode undecidable; prohibited from 'no comparison, judge consistent'.
        """
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "registry",
                "status": 200,
                "available": True,
                "licenses": ["MIT"],
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "status": 200,
                "available": True,
                "licenses": [],  # Lacks comparable license field
            },
        }
        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]

        self.assertNotEqual(verdict["category"], "CONSISTENT")
        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "undecidable")
        self.assertIn("comparable", verdict["summary"].lower() + verdict["details"].lower())

    def test_rev3_fix4_matching_licenses_across_sources_yields_consistent(self):
        """
        Fix 4 (Positive): When all available sources provide comparable license fields and they match,
        outputs CONSISTENT.
        """
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "registry",
                "status": 200,
                "available": True,
                "licenses": ["MIT"],
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "status": 200,
                "available": True,
                "licenses": ["MIT"],
            },
        }
        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]

        self.assertEqual(verdict["category"], "CONSISTENT")
        self.assertEqual(verdict["subcode"], "MUTUALLY_CONSISTENT")

    # =========================================================================
    # Rev3 Fix 5: Real Error Requires Empirical License Text Evidence
    # =========================================================================

    def test_rev3_fix5_missing_artifact_license_text_yields_undecidable_not_real_error(self):
        """
        Fix 5: Downstream reports 'non-standard' vs classifiers, but no artifact LICENSE text
        evidence is provided. MUST NOT output REAL_ERROR, and MUST NOT assert hardcoded PSF claims.
        """
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "pypi_json",
                "available": True,
                "status": 200,
                "license_classifiers": ["License :: OSI Approved :: Python Software Foundation License"],
                "licenses": [],
                # license_text_evidence is MISSING!
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

        self.assertNotEqual(verdict["category"], "REAL_ERROR")
        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "undecidable")
        # Ensure no hardcoded PSF assertions
        self.assertNotIn("the artifact dist-info/license contains", verdict["details"].lower())

    def test_rev3_fix5_provided_artifact_license_text_yields_real_error_dynamically(self):
        """
        Fix 5 (Positive): When artifact LICENSE text evidence IS provided, outputs REAL_ERROR
        and dynamically references the provided artifact evidence without hardcoded assertions.
        """
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "pypi_json",
                "available": True,
                "status": 200,
                "license_classifiers": ["License :: OSI Approved :: Python Software Foundation License"],
                "licenses": [],
                "license_text_evidence": {
                    "file": "custom_pkg.dist-info/LICENSE",
                    "spdx_identifier": "PSF-2.0",
                    "text_snippet": "PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2",
                },
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
        self.assertEqual(verdict["subcode"], "STANDARDS_CONTRADICTION")
        self.assertIn("custom_pkg.dist-info/license", verdict["details"].lower())
        self.assertNotIn("parsing failure", verdict["details"].lower())

    # =========================================================================
    # archgraph-layout Suspect / Retracted Demotion
    # =========================================================================

    def test_rev3_archgraph_suspect_status_yields_undecidable(self):
        """
        Demotion: When verification_status is 'suspect' or audit_status is 'retracted',
        MUST output INDETERMINATE (subcode undecidable) with suspect delay notice.
        """
        norm_data = self._base_norm_data()
        norm_data["verification_status"] = "suspect"
        norm_data["audit_status"] = "retracted"
        norm_data["sources"] = {
            "registry": {
                "source_id": "pypi_json",
                "status": 200,
                "available": True,
                "published_at": "2026-10-13T06:16:05Z",
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "status": 404,
                "available": False,
                "subsequent_observation": {
                    "status": 200,
                    "observed_at": "2026-10-13T07:15:00Z",
                },
            },
        }
        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]

        self.assertNotEqual(verdict["category"], "SYNC_DELAY")
        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "undecidable")
        self.assertIn("疑似延迟", verdict["summary"])
        self.assertEqual(res.get("verification_status"), "suspect")

    # =========================================================================
    # Astra 2026-10-13 Counterexample Regression Suite (Rev3 Bug Fixes)
    # =========================================================================

    def test_astra_counterexample_1_bare_file_list_does_not_prove_identity(self):
        """
        Astra 1: Bare filename list ['README', 'LICENSE'] must NOT prove artifact identity.
        Different digests with only bare filename list MUST return INDETERMINATE (ARTIFACT_IDENTITY_UNPROVEN),
        strictly prohibited from returning DIGEST_CONFLICT.
        """
        norm_data = self._base_norm_data()
        art_a = {
            "artifact_id": "sample-1.0.0.tgz",
            "digests": {"sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
            "files": ["README", "LICENSE"],
        }
        art_b = {
            "artifact_id": "sample-1.0.0.tgz",
            "digests": {"sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},
            "files": ["README", "LICENSE"],
        }
        res = self.verifier.verify(norm_data, compare_artifacts=(art_a, art_b))
        verdict = res["verdict"]

        self.assertNotEqual(verdict["category"], "DIGEST_CONFLICT")
        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "ARTIFACT_IDENTITY_UNPROVEN")
        self.assertIn("unproven", verdict["summary"].lower())

    def test_astra_counterexample_1_hashed_file_list_proves_identity(self):
        """
        Astra 1 (Positive): Package file list containing cryptographic hashes DOES prove artifact identity.
        Different digests correctly return DIGEST_CONFLICT.
        """
        norm_data = self._base_norm_data()
        hashed_files = {
            "README.md": "sha256:1111111111111111111111111111111111111111111111111111111111111111",
            "LICENSE": "sha256:2222222222222222222222222222222222222222222222222222222222222222",
        }
        art_a = {
            "artifact_id": "sample-1.0.0.tgz",
            "digests": {"sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
            "files": hashed_files,
        }
        art_b = {
            "artifact_id": "sample-1.0.0.tgz",
            "digests": {"sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},
            "files": hashed_files,
        }
        res = self.verifier.verify(norm_data, compare_artifacts=(art_a, art_b))
        verdict = res["verdict"]

        self.assertEqual(verdict["category"], "DIGEST_CONFLICT")
        self.assertEqual(verdict["subcode"], "ARTIFACT_DIGEST_MISMATCH")

    def test_astra_counterexample_2_sha256_short_hex_yields_length_mismatch(self):
        """
        Astra 2: SHA-256 inputs 'hex:00' and 'hex:01' (1 byte) must fail length validation (expected 32 bytes).
        MUST return INDETERMINATE with subcode DIGEST_LENGTH_MISMATCH, NOT DIGEST_CONFLICT.
        """
        norm_data = self._base_norm_data()
        art_a = {
            "artifact_id": "sample-1.0.0.tgz",
            "digests": {"sha256": "hex:00"},
            "release_record": "pkg:npm/sample@1.0.0",
        }
        art_b = {
            "artifact_id": "sample-1.0.0.tgz",
            "digests": {"sha256": "hex:01"},
            "release_record": "pkg:npm/sample@1.0.0",
        }
        res = self.verifier.verify(norm_data, compare_artifacts=(art_a, art_b))
        verdict = res["verdict"]

        self.assertNotEqual(verdict["category"], "DIGEST_CONFLICT")
        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "DIGEST_LENGTH_MISMATCH")
        self.assertIn("length mismatch", verdict["summary"].lower())

    def test_astra_counterexample_3_future_observation_year_2099_rejected(self):
        """
        Astra 3: Subsequent observation with future timestamp (e.g. 2099) MUST be rejected.
        MUST return INDETERMINATE (subcode undecidable) and NOT assert proven SYNC_DELAY.
        """
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "upstream",
                "status": 200,
                "available": True,
                "published_at": "2026-10-13T06:00:00Z",
                "licenses": ["MIT"],
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "status": 404,
                "available": False,
                "subsequent_observation": {
                    "observed_at": "2099-01-01T00:00:00Z",  # Year 2099 future observation!
                    "status": 200,
                },
            },
        }
        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]

        self.assertNotEqual(verdict["category"], "SYNC_DELAY")
        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "undecidable")
        self.assertIn("future", verdict["summary"].lower() + verdict["details"].lower())

    def test_astra_counterexample_3_42_day_delay_truthfully_reported_exceeding_tolerance(self):
        """
        Astra 3: 42-day delay must be truthfully reported as 42 days and explicitly note that it
        exceeds the sync tolerance window (86400s). Strictly prohibited from claiming 'within tolerance'.
        """
        norm_data = self._base_norm_data()
        # 42 days = 3628800 seconds
        norm_data["fetch_timestamp"] = "2024-01-01T01:00:00Z"
        norm_data["evaluation_timestamp"] = "2024-02-15T00:00:00Z"
        norm_data["sources"] = {
            "registry": {
                "source_id": "upstream",
                "status": 200,
                "available": True,
                "published_at": "2024-01-01T00:00:00Z",
                "licenses": ["MIT"],
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "status": 404,
                "available": False,
                "subsequent_observation": {
                    "observed_at": "2024-02-12T00:00:00Z",  # Exactly 42 days after published_at
                    "status": 200,
                },
            },
        }
        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]

        self.assertEqual(verdict["category"], "SYNC_DELAY")
        self.assertEqual(verdict["subcode"], "DOWNSTREAM_INGESTION_LAG")
        self.assertIn("42 days", verdict["details"])
        self.assertIn("exceeds", verdict["details"].lower())
        self.assertNotIn("within sync tolerance window", verdict["details"].lower())

    def test_astra_counterexample_4_mit_vs_non_standard_yields_divergence(self):
        """
        Astra 4: MIT vs non-standard must yield SEMANTIC_DIVERGENCE, strictly prohibited from judging CONSISTENT.
        """
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "registry",
                "status": 200,
                "available": True,
                "licenses": ["MIT"],
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "status": 200,
                "available": True,
                "licenses": ["non-standard"],
            },
        }
        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]

        self.assertNotEqual(verdict["category"], "CONSISTENT")
        self.assertEqual(verdict["category"], "SEMANTIC_DIVERGENCE")
        self.assertEqual(verdict["subcode"], "LICENSE_DECLARATION_DISCREPANCY")

    def test_astra_counterexample_4_no_license_differing_publication_time_yields_undecidable(self):
        """
        Astra 4: Neither source has a license, differing only in publication timestamps.
        MUST yield INDETERMINATE (subcode undecidable) due to lack of comparable license evidence;
        strictly prohibited from judging CONSISTENT with 1.0 confidence.
        """
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "source_a": {
                "source_id": "source_a",
                "status": 200,
                "available": True,
                "published_at": "2024-01-01T00:00:00Z",
                "licenses": [],
            },
            "source_b": {
                "source_id": "source_b",
                "status": 200,
                "available": True,
                "published_at": "2024-02-01T00:00:00Z",
                "licenses": [],
            },
        }
        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]

        self.assertNotEqual(verdict["category"], "CONSISTENT")
        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "undecidable")

    def test_astra_counterexample_4_consistent_confidence_strictly_less_than_one(self):
        """
        Astra 4: CONSISTENT is only output when actively compared and matching.
        Confidence is calculated based on evidence strength and MUST NOT be constantly 1.0.
        """
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "source_a": {
                "source_id": "source_a",
                "status": 200,
                "available": True,
                "licenses": ["MIT"],
            },
            "source_b": {
                "source_id": "source_b",
                "status": 200,
                "available": True,
                "licenses": ["MIT"],
            },
        }
        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]

        self.assertEqual(verdict["category"], "CONSISTENT")
        self.assertEqual(verdict["subcode"], "MUTUALLY_CONSISTENT")
        self.assertLess(verdict["confidence"], 1.0)
        self.assertGreaterEqual(verdict["confidence"], 0.80)

    def test_astra_counterexample_5_arbitrary_snippet_without_standard_match_yields_undecidable(self):
        """
        Astra 5: Arbitrary non-empty text snippet lacking evidence of matching standard text
        MUST NOT trigger REAL_ERROR. MUST return INDETERMINATE with subcode undecidable.
        """
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "pypi_json",
                "available": True,
                "status": 200,
                "license_classifiers": ["License :: OSI Approved :: Python Software Foundation License"],
                "licenses": [],
                "license_text_evidence": {
                    "file": "custom.dist-info/LICENSE",
                    "spdx_identifier": "PSF-2.0",
                    "text_snippet": "This is completely arbitrary custom text that does not follow any standard license at all.",
                },
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

        self.assertNotEqual(verdict["category"], "REAL_ERROR")
        self.assertEqual(verdict["category"], "INDETERMINATE")
        self.assertEqual(verdict["subcode"], "undecidable")
        self.assertIn("lacks standard text match", verdict["summary"].lower() + verdict["details"].lower())

    def test_astra_counterexample_5_pep_639_assertion_removed_from_real_error(self):
        """
        Astra 5: Verifiable real error must NOT contain hardcoded 'PEP 639' assertions.
        """
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "pypi_json",
                "available": True,
                "status": 200,
                "license_classifiers": ["License :: OSI Approved :: Python Software Foundation License"],
                "licenses": [],
                "license_text_evidence": {
                    "file": "typing_extensions.dist-info/LICENSE",
                    "spdx_identifier": "PSF-2.0",
                    "text_snippet": "PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2\n\n1. This LICENSE AGREEMENT...",
                },
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
        self.assertEqual(verdict["subcode"], "STANDARDS_CONTRADICTION")
        self.assertNotIn("pep 639", verdict["details"].lower())

    def test_astra_counterexample_5_or_expression_described_as_spdx_disjunction_not_and_obligation(self):
        """
        Astra 5: OR compound expression must be described as disjunctive alternative licensing choice
        under SPDX semantics, NOT as AND dual obligations.
        """
        norm_data = self._base_norm_data()
        norm_data["sources"] = {
            "registry": {
                "source_id": "npm_registry",
                "status": 200,
                "available": True,
                "licenses": ["MIT"],
            },
            "clearlydefined": {
                "source_id": "clearlydefined",
                "status": 200,
                "available": True,
                "declared_license": "MIT OR Apache-2.0",
                "discovered_licenses": ["MIT", "Apache-2.0"],
            },
            "deps_dev": {
                "source_id": "deps_dev",
                "status": 200,
                "available": True,
                "licenses": ["MIT"],
            },
        }
        res = self.verifier.verify(norm_data)
        verdict = res["verdict"]

        self.assertEqual(verdict["category"], "SEMANTIC_DIVERGENCE")
        self.assertEqual(verdict["subcode"], "LICENSE_EXPRESSION_DISJUNCTION_MISMATCH")
        self.assertIn("or disjunction", verdict["summary"].lower() + verdict["details"].lower())
        self.assertNotIn("dual compliance obligations", verdict["details"].lower())


if __name__ == "__main__":
    unittest.main()
