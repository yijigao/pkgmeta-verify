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
Decision Verifier module.
Implements the core decision rules and hard constraints mandated by the CodeSupply council:
- REAL_ERROR: Proven contradictory metadata with empirical evidence of error (requires artifact license evidence; no hardcoded assertions).
- SYNC_DELAY: Upstream vs downstream time skew preserving uncertainty; requires complete temporal chain, HTTP success, forward chronological order.
- SEMANTIC_DIVERGENCE: License differences across sources (conjunction/disjunction or MIT vs Apache-2.0); disallows auto-acceptance.
- INDETERMINATE: Incomparable inputs, unproven artifact identity, unsupported encodings, or missing comparable fields strictly output 'undecidable'.
- DIGEST_CONFLICT: Identical artifact & algorithm hash mismatch proves only digest conflict, MUST NOT assert tampering/corruption.
- Source Dependency: deps.dev dependency on registry is tracked; agreement is not independent proof.
"""

import base64
from datetime import datetime, timezone
import json
import os
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from .normalizer import Normalizer


class Verifier:
    """Evaluates normalized package metadata against versioned verification rules."""

    # Constant threshold: 24 hours (86400 seconds) sync delay tolerance window
    DEFAULT_SYNC_DELAY_TOLERANCE_SECONDS: int = 86400

    # Normalization map for supported cryptographic hash algorithms (case-insensitive & aliases)
    ALGO_ALIAS_MAP: Dict[str, str] = {
        "sha256": "sha256",
        "sha-256": "sha256",
        "sha_256": "sha256",
        "sha512": "sha512",
        "sha-512": "sha512",
        "sha_512": "sha512",
        "sha384": "sha384",
        "sha-384": "sha384",
        "sha_384": "sha384",
        "sha1": "sha1",
        "sha-1": "sha1",
        "sha_1": "sha1",
        "md5": "md5",
        "blake2b_256": "blake2b_256",
        "blake2b-256": "blake2b_256",
        "blake2b256": "blake2b_256",
        "blake2b_512": "blake2b_512",
        "blake2b-512": "blake2b_512",
        "blake2b512": "blake2b_512",
        "blake2s_256": "blake2s_256",
        "blake2s-256": "blake2s_256",
        "blake2s256": "blake2s_256",
    }

    # Expected raw decoded byte length for supported hash algorithms
    EXPECTED_DIGEST_LENGTHS: Dict[str, int] = {
        "sha256": 32,
        "sha512": 64,
        "sha384": 48,
        "sha1": 20,
        "md5": 16,
        "blake2b_256": 32,
        "blake2b_512": 64,
        "blake2s_256": 32,
    }

    # Vacuous / placeholder / uninformative license declarations
    UNINFORMATIVE_LICENSES: Set[str] = {
        "", "none", "null", "unknown", "n/a", "na", "undefined",
        "see license file", "see license", "see-license-file",
        "custom", "unspecified", "other", "placeholder"
    }

    def __init__(self, rules_path: Optional[str] = None):
        self.rules_path = rules_path or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "rules", "rules-v0.1.json"
        )
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict[str, Any]:
        if os.path.exists(self.rules_path):
            with open(self.rules_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"ruleset_version": "v0.1"}

    def verify(
        self,
        norm_data: Dict[str, Any],
        compare_artifacts: Optional[Tuple[Dict[str, Any], Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Execute full verification pipeline and return structured PMV result."""
        purl = norm_data["purl"]
        ecosystem = norm_data["ecosystem"]
        name = norm_data["name"]
        version = norm_data["version"]
        synthetic = norm_data.get("synthetic", False)
        eval_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        sources = norm_data.get("sources", {})
        audit_trail: List[Dict[str, Any]] = []

        # 1. Check Digest Hard Constraints if artifacts comparison requested or present
        digest_verdict = self._evaluate_digest_constraints(norm_data, compare_artifacts, audit_trail)
        if digest_verdict:
            verdict = digest_verdict
        else:
            # 2. Check Sync Delay Constraint
            sync_verdict = self._evaluate_sync_delay(norm_data, audit_trail)
            if sync_verdict:
                verdict = sync_verdict
            else:
                # 3. Check Real Error Constraint
                error_verdict = self._evaluate_real_error(norm_data, audit_trail)
                if error_verdict:
                    verdict = error_verdict
                else:
                    # 4. Check Semantic Divergence Constraint
                    sem_verdict = self._evaluate_semantic_divergence(norm_data, audit_trail)
                    if sem_verdict:
                        verdict = sem_verdict
                    else:
                        # 5. Default Consistent
                        verdict = self._evaluate_consistent(norm_data, audit_trail)

        # Assemble sources consulted for provenance output in deterministic sorted order
        sources_consulted = []
        for s_key in sorted(sources.keys()):
            s_val = sources[s_key]
            sources_consulted.append({
                "source_id": s_val.get("source_id", s_key),
                "role": s_val.get("role", "unknown"),
                "endpoint": s_val.get("endpoint", ""),
                "fetch_timestamp": norm_data.get("fetch_timestamp", eval_ts),
                "status": s_val.get("status", 200),
                "derived_from": s_val.get("derived_from"),
            })

        res: Dict[str, Any] = {
            "purl": purl,
            "ecosystem": ecosystem,
            "name": name,
            "version": version,
            "evaluation_timestamp": eval_ts,
            "ruleset_version": self.rules.get("ruleset_version", "v0.1"),
            "synthetic": synthetic,
            "verdict": verdict,
            "provenance_and_dependencies": {
                "sources_consulted": sources_consulted,
                "dependency_relations": norm_data.get("dependency_relations", []),
            },
            "normalized_evidence": sources,
            "decision_audit_trail": audit_trail,
        }

        if norm_data.get("verification_status"):
            res["verification_status"] = norm_data["verification_status"]
        if norm_data.get("audit_status"):
            res["audit_status"] = norm_data["audit_status"]

        return res

    @staticmethod
    def _parse_iso_ts(ts_str: Optional[str]) -> Optional[datetime]:
        """Safely parse an ISO-8601 timestamp string into a timezone-aware datetime."""
        if not ts_str or not isinstance(ts_str, str):
            return None
        try:
            clean = ts_str.replace("Z", "+00:00")
            dt = datetime.fromisoformat(clean)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            return None

    @staticmethod
    def _format_delay_duration(seconds: float) -> str:
        """Format duration in seconds to human-readable duration without obscuring long delays."""
        s = int(seconds)
        days = s // 86400
        rem_s = s % 86400
        if days > 0:
            if rem_s == 0:
                return f"{days} days ({s}s)"
            hours = rem_s // 3600
            if hours > 0:
                return f"{days} days {hours} hours ({s}s)"
            return f"{days} days ({s}s)"
        elif s >= 3600:
            hours = s // 3600
            return f"{hours} hours ({s}s)"
        elif s >= 60:
            mins = s // 60
            return f"{mins} minutes ({s}s)"
        return f"{s}s"

    @staticmethod
    def _is_valid_hash_string(val: Any) -> bool:
        """
        Validate whether a candidate string is a substantive cryptographic hash.
        Rejects empty strings, placeholders ('none', 'null', 'unknown', 'n/a'),
        all-zero dummy hashes ('0'*32, '0'*64), and malformed structures.
        """
        if not isinstance(val, str):
            return False
        s = val.strip()
        if not s:
            return False
        lower = s.lower()
        if lower in (
            "none", "null", "unknown", "n/a", "na", "undefined",
            "placeholder", "tbd", "missing", "void", "empty", "0"
        ):
            return False

        # Strip standard algorithm / encoding prefixes
        for prefix in (
            "sha256:", "sha512:", "sha384:", "sha1:", "md5:",
            "hex:", "base64:", "sha256-", "sha512-", "sha384-", "sha1-"
        ):
            if lower.startswith(prefix):
                s = s[len(prefix):].strip()
                lower = s.lower()
                break

        if not s or lower in (
            "none", "null", "unknown", "n/a", "na", "undefined",
            "placeholder", "tbd", "missing", "void", "empty"
        ):
            return False

        # Reject all-zero dummy / tombstone hashes (e.g. '0'*32, '0'*40, '0'*64, '0'*128)
        if set(lower) == {"0"}:
            return False

        # Check hexadecimal
        if re.fullmatch(r"[0-9a-fA-F]+", s):
            # Supported standard byte lengths: md5=32 hex, sha1=40 hex, sha256/blake2b=64 hex, sha384=96 hex, sha512=128 hex
            if len(s) in (32, 40, 64, 96, 128):
                return True
            return False

        # Check base64
        try:
            b = base64.b64decode(s, validate=True)
            if len(b) in (16, 20, 32, 48, 64) and any(x != 0 for x in b):
                return True
        except Exception:
            pass

        return False

    @staticmethod
    def _manifest_has_hashes(manifest: Any) -> bool:
        """
        Check if a package file list / manifest contains valid cryptographic hashes
        with verifiable content, rather than bare filenames, empty values, placeholders,
        or all-zero dummy hashes.
        """
        if not manifest:
            return False
        if isinstance(manifest, dict):
            for k, v in manifest.items():
                if isinstance(v, str):
                    if Verifier._is_valid_hash_string(v):
                        return True
                elif isinstance(v, dict):
                    for sub_k, sub_v in v.items():
                        if Verifier._is_valid_hash_string(sub_v):
                            return True
                elif isinstance(v, list):
                    for item in v:
                        if Verifier._is_valid_hash_string(item):
                            return True
            return False
        elif isinstance(manifest, list):
            for item in manifest:
                if isinstance(item, dict):
                    for sub_k, sub_v in item.items():
                        if Verifier._is_valid_hash_string(sub_v):
                            return True
                elif isinstance(item, str):
                    if Verifier._is_valid_hash_string(item):
                        return True
                    parts = item.strip().split()
                    if any(Verifier._is_valid_hash_string(p) for p in parts):
                        return True
            return False
        return False

    @staticmethod
    def _is_valid_provenance_scalar(val: Any) -> bool:
        """Verify that a provenance identifier (URL, release record) is non-empty and non-placeholder."""
        if not isinstance(val, str):
            return False
        s = val.strip()
        if not s or s.lower() in ("none", "null", "unknown", "n/a", "na", "undefined", "placeholder"):
            return False
        return True

    @staticmethod
    def _has_standard_license_match_evidence(lic_ev: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Verify that the artifact license text evidence contains substantive proof
        matching standard license canonical text rather than arbitrary unverified text.
        Self-attested flags (e.g. matches_standard=True) are treated strictly as declarations,
        NEVER as verification proof.
        """
        if not lic_ev:
            return False, "missing license_text_evidence"
        snippet = str(lic_ev.get("text_snippet", "")).strip()
        if not snippet:
            return False, "empty text_snippet"

        snippet_lower = snippet.lower()

        # 1. Reject explicit negation and disclaimer phrases (e.g. "This is not an MIT license")
        negation_patterns = [
            r"\b(?:this\s+is\s+)?not\s+(?:an?\s+)?(?:mit|apache|bsd|gpl|lgpl|mpl|psf|python|osi)\b",
            r"\bnon-(?:mit|apache|bsd|gpl|standard)\b",
            r"\bneither\s+(?:an?\s+)?(?:mit|apache|bsd|gpl)\b",
            r"\bnot\s+licensed\s+under\b",
        ]
        for pat in negation_patterns:
            if re.search(pat, snippet_lower):
                return False, f"text snippet explicitly disclaims standard license: matches negation pattern '{pat}'"

        spdx_id = str(lic_ev.get("spdx_identifier", "")).strip()

        # 2. Substantive core legal clauses required for standard licenses
        # Each standard license requires BOTH primary grant and core condition/disclaimer clauses.
        # Merely mentioning the license name is strictly prohibited from passing.
        if spdx_id in ("PSF-2.0", "Python-2.0", "Python-2.0.1"):
            has_psf_header = any(
                p in snippet_lower for p in (
                    "python software foundation license",
                    "license agreement for python",
                    "cnri license agreement",
                )
            )
            has_psf_body = any(
                p in snippet_lower for p in (
                    "license agreement",
                    "hereby grants",
                    "in source or binary form",
                    "psf",
                    "version 2",
                    "version 1",
                )
            )
            if has_psf_header and has_psf_body:
                return True, f"text snippet contains substantive canonical clauses for '{spdx_id}'"
            return False, f"text snippet lacks substantive canonical agreement clauses for '{spdx_id}'"

        elif spdx_id == "MIT":
            has_grant = (
                "permission is hereby granted, free of charge" in snippet_lower
                or "to deal in the software without restriction" in snippet_lower
            )
            has_condition_or_disclaimer = (
                "the above copyright notice and this permission notice shall be included" in snippet_lower
                or "the software is provided \"as is\", without warranty of any kind" in snippet_lower
                or "in no event shall the authors or copyright holders be liable" in snippet_lower
            )
            if has_grant and has_condition_or_disclaimer:
                return True, "text snippet contains substantive canonical grant and disclaimer clauses for 'MIT'"
            return False, "text snippet lacks substantive canonical permission grant or conditions for 'MIT' (keyword presence alone is strictly insufficient)"

        elif spdx_id in ("Apache-2.0", "Apache-1.1"):
            has_apache_header = (
                "apache license" in snippet_lower
                and ("version 2.0" in snippet_lower or "http://www.apache.org/licenses/license-2.0" in snippet_lower)
            )
            has_apache_body = any(
                p in snippet_lower for p in (
                    "terms and conditions for use, reproduction, and distribution",
                    "licensed under the apache license, version 2.0",
                    "subject to the terms and conditions of this license",
                )
            )
            if has_apache_header and has_apache_body:
                return True, f"text snippet contains substantive canonical clauses for '{spdx_id}'"
            return False, f"text snippet lacks substantive canonical clauses for '{spdx_id}'"

        elif spdx_id in ("BSD-2-Clause", "BSD-3-Clause", "0BSD", "ISC"):
            has_redist = (
                "redistribution and use in source and binary forms" in snippet_lower
                or "permission to use, copy, modify, and/or distribute this software" in snippet_lower
            )
            has_disclaimer = (
                "neither the name of" in snippet_lower
                or "reproduce the above copyright notice" in snippet_lower
                or "as is" in snippet_lower
            )
            if has_redist and has_disclaimer:
                return True, f"text snippet contains substantive canonical clauses for '{spdx_id}'"
            return False, f"text snippet lacks substantive canonical clauses for '{spdx_id}'"

        elif spdx_id in ("GPL-2.0-only", "GPL-3.0-only", "GPL-2.0-or-later", "GPL-3.0-or-later", "LGPL-2.1-only", "LGPL-3.0-only"):
            has_gpl = "gnu general public license" in snippet_lower or "gnu lesser general public license" in snippet_lower
            has_fsf = "free software foundation" in snippet_lower or "terms and conditions for copying" in snippet_lower
            if has_gpl and has_fsf:
                return True, f"text snippet contains substantive canonical clauses for '{spdx_id}'"
            return False, f"text snippet lacks substantive canonical clauses for '{spdx_id}'"

        return False, f"text snippet does not match recognized substantive standard clauses for '{spdx_id}'"

    @staticmethod
    def _check_artifact_identity_provenance(art_a: Dict[str, Any], art_b: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Verify artifact identity association:
        Must prove digest is bound to:
        1. Identical download URL; OR
        2. Package file list containing valid cryptographic hashes (bare filename lists, empty hashes,
           or placeholders are strictly forbidden); OR
        3. Identical release record / publication record.
        Bare filename lists (e.g. ['README', 'LICENSE']), empty hashes (e.g. {'LICENSE': {'sha256': ''}}),
        or merely having digests on both sides is strictly insufficient.
        """
        url_a = art_a.get("url") or art_a.get("download_url")
        url_b = art_b.get("url") or art_b.get("download_url")
        if (
            Verifier._is_valid_provenance_scalar(url_a)
            and Verifier._is_valid_provenance_scalar(url_b)
            and url_a == url_b
        ):
            return True, f"identical download URL: '{url_a}'"

        orig_b = art_b.get("origin_url")
        if (
            Verifier._is_valid_provenance_scalar(orig_b)
            and Verifier._is_valid_provenance_scalar(url_a)
            and orig_b == url_a
        ):
            return True, f"artifact B origin URL binds to artifact A download URL: '{url_a}'"

        orig_a = art_a.get("origin_url")
        if (
            Verifier._is_valid_provenance_scalar(orig_a)
            and Verifier._is_valid_provenance_scalar(url_b)
            and orig_a == url_b
        ):
            return True, f"artifact A origin URL binds to artifact B download URL: '{url_b}'"

        rel_a = art_a.get("release_record") or art_a.get("release_id") or art_a.get("package_release")
        rel_b = art_b.get("release_record") or art_b.get("release_id") or art_b.get("package_release")
        if (
            Verifier._is_valid_provenance_scalar(rel_a)
            and Verifier._is_valid_provenance_scalar(rel_b)
            and rel_a == rel_b
        ):
            return True, f"identical artifact release record: '{rel_a}'"

        files_a = art_a.get("file_list") or art_a.get("files") or art_a.get("manifest")
        files_b = art_b.get("file_list") or art_b.get("files") or art_b.get("manifest")
        if files_a and files_b and files_a == files_b:
            if Verifier._manifest_has_hashes(files_a):
                return True, "identical package file list with valid cryptographic hashes"
            else:
                return False, "package file list lacks valid cryptographic hashes (bare filename lists, empty hashes, placeholders, or all-zero hashes are strictly insufficient to prove artifact identity)"

        return False, "no shared release record, download URL, or file list with valid cryptographic hashes"

    @staticmethod
    def _decode_digest_bytes(raw_val: Any, algo: str) -> Tuple[Optional[bytes], str, Optional[str]]:
        """
        Decodes a digest representation to raw bytes without case corruption.
        Supported encodings:
        - hex: valid hexadecimal string
        - base64: valid base64 string (including SRI prefixes like sha256-, sha512-)
        Returns (decoded_bytes, encoding_name, error_reason).
        """
        if raw_val is None:
            return None, "empty", "Digest value is null or empty"

        # Structured dictionary input
        if isinstance(raw_val, dict):
            enc = raw_val.get("encoding", "").lower()
            val = str(raw_val.get("value", "")).strip()
            if enc == "base64":
                try:
                    return base64.b64decode(val, validate=True), "base64", None
                except Exception as exc:
                    return None, "base64", f"Invalid base64 payload: {exc}"
            elif enc in ("hex", "base16"):
                try:
                    return bytes.fromhex(val), "hex", None
                except Exception as exc:
                    return None, "hex", f"Invalid hex payload: {exc}"
            else:
                return None, enc or "unknown", f"Unsupported explicit digest encoding '{enc}'"

        s = str(raw_val).strip()

        # Explicit prefixes
        if s.startswith("base64:"):
            payload = s[7:].strip()
            try:
                return base64.b64decode(payload, validate=True), "base64", None
            except Exception as exc:
                return None, "base64", f"Invalid base64 payload: {exc}"

        if s.startswith("hex:"):
            payload = s[4:].strip()
            try:
                return bytes.fromhex(payload), "hex", None
            except Exception as exc:
                return None, "hex", f"Invalid hex payload: {exc}"

        # SRI format (e.g. sha512-..., sha256-...)
        canon_algo = Verifier.ALGO_ALIAS_MAP.get(algo.lower(), algo.lower()) if hasattr(Verifier, "ALGO_ALIAS_MAP") else algo.lower()
        sri_prefix = f"{canon_algo}-"
        if s.startswith(sri_prefix) or s.startswith(f"{algo}-") or (canon_algo == "sha512" and s.startswith("sha512-")) or (canon_algo == "sha256" and s.startswith("sha256-")):
            payload = s.split("-", 1)[1].strip()
            try:
                return base64.b64decode(payload, validate=True), "base64", None
            except Exception as exc:
                return None, "base64", f"Invalid SRI base64 payload: {exc}"

        expected_bytes = Verifier.EXPECTED_DIGEST_LENGTHS.get(canon_algo)

        # Check explicit base64 characteristics
        has_b64_chars = "+" in s or "/" in s or s.endswith("=")
        if has_b64_chars:
            try:
                b = base64.b64decode(s, validate=True)
                if expected_bytes is None or len(b) == expected_bytes:
                    return b, "base64", None
            except Exception as exc:
                return None, "base64", f"Invalid base64 characters or padding: {exc}"

        # Check if valid hex string
        is_all_hex = bool(re.fullmatch(r"[0-9a-fA-F]+", s))
        if is_all_hex and len(s) % 2 == 0:
            if expected_bytes is None or len(s) == expected_bytes * 2:
                try:
                    return bytes.fromhex(s), "hex", None
                except Exception as exc:
                    return None, "hex", f"Hex decode error: {exc}"

        # Fallback base64 attempt
        try:
            b = base64.b64decode(s, validate=True)
            if expected_bytes is None or len(b) == expected_bytes:
                return b, "base64", None
        except Exception:
            pass

        # Fallback hex attempt
        if is_all_hex and len(s) % 2 == 0:
            try:
                return bytes.fromhex(s), "hex", None
            except Exception:
                pass

        return None, "unknown", f"Unsupported or unrecognizable digest encoding for value '{s}'"

    def _evaluate_digest_constraints(
        self,
        norm_data: Dict[str, Any],
        compare_artifacts: Optional[Tuple[Dict[str, Any], Dict[str, Any]]],
        audit_trail: List[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:
        """
        Enforce hard constraints:
        - Hash comparison ONLY allowed for identical artifact + identical algorithm.
        - Cross-algorithm / cross-artifact inputs output 'undecidable' under INDETERMINATE (never crash).
        - Artifact identity association requires proven binding (same URL, file list, or release record).
        - Hash comparison decodes bytes strictly according to encoding; silent .lower() matching prohibited.
        - Hash divergence only proves 'digest conflict', MUST NOT assert mirror corruption or tampering.
        """
        pair = compare_artifacts
        if not pair:
            syn = norm_data["sources"].get("synthetic")
            reg = norm_data["sources"].get("registry")
            if syn and reg and syn.get("artifacts") and reg.get("artifacts"):
                pair = (reg["artifacts"][0], syn["artifacts"][0])

        if not pair:
            return None

        art_a, art_b = pair
        id_a = art_a.get("artifact_id")
        id_b = art_b.get("artifact_id")
        digs_a = art_a.get("digests", {})
        digs_b = art_b.get("digests", {})

        # Rule 1: Identical artifact ID check
        if not id_a or not id_b or id_a != id_b:
            audit_trail.append({
                "rule_id": "DIGEST_01_ARTIFACT_IDENTITY",
                "condition_evaluated": f"artifact_id_a ('{id_a}') == artifact_id_b ('{id_b}')",
                "outcome": "FAIL_CROSS_ARTIFACT",
                "rationale": "Different artifact formats/names (e.g. sdist vs wheel, or tarball vs repo tree) cannot have hashes directly compared.",
            })
            return {
                "category": "INDETERMINATE",
                "subcode": "undecidable",
                "confidence": 1.0,
                "summary": "Hash comparison between different artifacts is undecidable",
                "details": f"Attempted to compare hashes across incomparable artifacts '{id_a}' and '{id_b}'. Enforcing hard constraint: cross-artifact hash comparison yields 'undecidable'.",
                "avoided_false_positive": "Avoided false-positive 'hash corruption/tampering' alert caused by comparing different build artifact targets (e.g. wheel vs sdist tarball).",
            }

        # Rule 1b: Artifact identity association check
        is_prov_bound, prov_reason = self._check_artifact_identity_provenance(art_a, art_b)
        if not is_prov_bound:
            audit_trail.append({
                "rule_id": "DIGEST_01_ARTIFACT_IDENTITY_PROVENANCE",
                "condition_evaluated": "has_artifact_identity_provenance(same_url, same_file_list, same_release_record)",
                "outcome": "FAIL_IDENTITY_UNPROVEN",
                "rationale": f"Artifact identity association unproven: {prov_reason}. Merely sharing filename '{id_a}' and both providing digests is insufficient to assert identical artifact.",
            })
            return {
                "category": "INDETERMINATE",
                "subcode": "ARTIFACT_IDENTITY_UNPROVEN",
                "confidence": 1.0,
                "summary": "Artifact identity association unproven for digest comparison",
                "details": f"Artifacts share filename '{id_a}', but lack verified artifact identity association (digest must bind to identical download URL, identical package file list containing cryptographic hashes, or identical release record; bare filename lists are strictly forbidden). Merely having digests on both sides is insufficient. Enforcing hard constraint: outputs undecidable (subcode ARTIFACT_IDENTITY_UNPROVEN), strictly prohibited from asserting DIGEST_CONFLICT.",
                "avoided_false_positive": "Avoided false-positive DIGEST_CONFLICT between unlinked files sharing only a common filename or bare filename list.",
            }

        audit_trail.append({
            "rule_id": "DIGEST_01_ARTIFACT_IDENTITY_PROVENANCE",
            "condition_evaluated": "has_artifact_identity_provenance(same_url, same_file_list, same_release_record)",
            "outcome": "PASS_IDENTITY_PROVEN",
            "rationale": f"Artifact identity verified via {prov_reason}.",
        })

        # Rule 2: Algorithm normalization and mapping
        # Maps raw algorithm names (case-insensitive & aliases) to canonical algorithm names.
        norm_digs_a: Dict[str, Tuple[str, Any]] = {}
        unknown_algos_a: List[str] = []
        for k, v in digs_a.items():
            if not isinstance(k, str) or not k.strip():
                continue
            canon = self.ALGO_ALIAS_MAP.get(k.strip().lower())
            if canon:
                norm_digs_a[canon] = (k, v)
            else:
                unknown_algos_a.append(k)

        norm_digs_b: Dict[str, Tuple[str, Any]] = {}
        unknown_algos_b: List[str] = []
        for k, v in digs_b.items():
            if not isinstance(k, str) or not k.strip():
                continue
            canon = self.ALGO_ALIAS_MAP.get(k.strip().lower())
            if canon:
                norm_digs_b[canon] = (k, v)
            else:
                unknown_algos_b.append(k)

        shared_algos = sorted(list(set(norm_digs_a.keys()).intersection(set(norm_digs_b.keys()))))
        shared_unknown = sorted(list(set(unknown_algos_a).intersection(set(unknown_algos_b))))

        # If algorithms are unknown/unrecognized:
        # Enforce hard constraint: unknown algorithms MUST NOT bypass length constraints;
        # output undecidable (subcode ENCODING_UNSUPPORTED).
        if not shared_algos and (shared_unknown or unknown_algos_a or unknown_algos_b):
            target_unknown = shared_unknown or unknown_algos_a or unknown_algos_b
            audit_trail.append({
                "rule_id": "DIGEST_02_ALGORITHM_IDENTITY",
                "condition_evaluated": f"shared_unknown_algorithms({target_unknown})",
                "outcome": "ENCODING_UNSUPPORTED",
                "rationale": f"Digest algorithm(s) {target_unknown} are unknown or unsupported. Unknown algorithms cannot bypass length constraints; outputs undecidable.",
            })
            return {
                "category": "INDETERMINATE",
                "subcode": "ENCODING_UNSUPPORTED",
                "confidence": 1.0,
                "summary": f"Digest algorithm {target_unknown} is unknown or unsupported",
                "details": f"Attempted to compare digests with unknown algorithm(s) {target_unknown}. Enforcing hard constraint: unknown algorithms must NOT skip length constraints; outputs undecidable (subcode ENCODING_UNSUPPORTED).",
                "avoided_false_positive": "Avoided skipping length constraints or asserting false DIGEST_CONFLICT on unrecognized hash algorithms.",
            }

        if not shared_algos:
            audit_trail.append({
                "rule_id": "DIGEST_02_ALGORITHM_IDENTITY",
                "condition_evaluated": f"shared_algorithms({list(digs_a.keys())}, {list(digs_b.keys())})",
                "outcome": "FAIL_CROSS_ALGORITHM",
                "rationale": "Cross-algorithm hash comparison (e.g. sha1 vs sha256 or sha512) is mathematically incomparable.",
            })
            return {
                "category": "INDETERMINATE",
                "subcode": "undecidable",
                "confidence": 1.0,
                "summary": "Hash comparison across different algorithms is undecidable",
                "details": f"Artifact '{id_a}' has algorithms {list(digs_a.keys())} vs {list(digs_b.keys())}. No shared algorithm available. Enforcing hard constraint: cross-algorithm input yields 'undecidable' without unhandled exception.",
                "avoided_false_positive": "Avoided crash/exception or false mismatch alert when one source only provides sha1/md5 and another provides sha256/sha512.",
            }

        # Rule 3: Hash value check across shared algorithms via byte-level decoding & length validation
        conflict_algos = []
        for algo in shared_algos:
            raw_a = norm_digs_a[algo][1]
            raw_b = norm_digs_b[algo][1]
            orig_k_a = norm_digs_a[algo][0]
            orig_k_b = norm_digs_b[algo][0]

            bytes_a, enc_a, err_a = self._decode_digest_bytes(raw_a, algo)
            bytes_b, enc_b, err_b = self._decode_digest_bytes(raw_b, algo)

            if bytes_a is None or bytes_b is None:
                fail_reason = err_a or err_b or "Unknown or unsupported encoding"
                audit_trail.append({
                    "rule_id": "DIGEST_03_BYTE_DECODING",
                    "condition_evaluated": f"decode_digest_bytes(algo='{algo}', raw_a={raw_a}, raw_b={raw_b})",
                    "outcome": "ENCODING_UNSUPPORTED",
                    "rationale": f"Digest decoding failed for algorithm '{algo}': {fail_reason}. Silent .lower() string matching prohibited; unsupported encoding outputs undecidable.",
                })
                return {
                    "category": "INDETERMINATE",
                    "subcode": "ENCODING_UNSUPPORTED",
                    "confidence": 1.0,
                    "summary": f"Digest encoding unknown or unsupported for algorithm '{algo}'",
                    "details": f"Digest value could not be decoded to raw bytes using supported encodings (hex, base64). Reason: {fail_reason}. Enforcing hard constraint: outputs undecidable (subcode ENCODING_UNSUPPORTED), silent .lower() matching strictly prohibited.",
                    "avoided_false_positive": "Avoided corrupting case-sensitive digest encodings (such as base64) through naive lowercase string comparison.",
                }

            # Rule 3b: Digest length validation (normalized algorithm requires exact decoded byte length)
            expected_len = self.EXPECTED_DIGEST_LENGTHS.get(algo)
            if expected_len is not None and (len(bytes_a) != expected_len or len(bytes_b) != expected_len):
                audit_trail.append({
                    "rule_id": "DIGEST_03_LENGTH_VALIDATION",
                    "condition_evaluated": f"len(digest_bytes) == {expected_len} for algo '{algo}' (source_a={len(bytes_a)}, source_b={len(bytes_b)})",
                    "outcome": "DIGEST_LENGTH_MISMATCH",
                    "rationale": f"Decoded digest byte length mismatch for algorithm '{algo}' (keys '{orig_k_a}', '{orig_k_b}'): expected {expected_len} bytes, got source_a={len(bytes_a)} bytes, source_b={len(bytes_b)} bytes. Enforcing hard constraint: length mismatch outputs undecidable (subcode DIGEST_LENGTH_MISMATCH).",
                })
                return {
                    "category": "INDETERMINATE",
                    "subcode": "DIGEST_LENGTH_MISMATCH",
                    "confidence": 1.0,
                    "summary": f"Digest length mismatch for algorithm '{algo}'",
                    "details": f"Declared algorithm '{algo}' (keys: '{orig_k_a}', '{orig_k_b}') requires {expected_len} bytes, but decoded digest length does not match (source_a has {len(bytes_a)} bytes, source_b has {len(bytes_b)} bytes). Enforcing hard constraint: length mismatch outputs undecidable (subcode DIGEST_LENGTH_MISMATCH), strictly prohibited from asserting DIGEST_CONFLICT.",
                    "avoided_false_positive": f"Avoided false-positive DIGEST_CONFLICT on malformed or truncated {algo} digest vectors.",
                }

            audit_trail.append({
                "rule_id": "DIGEST_03_BYTE_DECODING",
                "condition_evaluated": f"decode_digest_bytes(algo='{algo}')",
                "outcome": "DECODED",
                "rationale": f"Decoded digests to raw bytes for algorithm '{algo}' (encodings: source_a={enc_a}, source_b={enc_b}). Byte-level comparison executed; silent .lower() string matching prohibited.",
                "original_values": {"source_a": str(raw_a), "source_b": str(raw_b)},
                "encodings": {"source_a": enc_a, "source_b": enc_b},
            })

            if bytes_a != bytes_b:
                conflict_algos.append((algo, str(raw_a), str(raw_b), enc_a, enc_b))

        if conflict_algos:
            audit_trail.append({
                "rule_id": "DIGEST_03_VALUE_COMPARISON",
                "condition_evaluated": f"bytes_match({[(c[0], c[3], c[4]) for c in conflict_algos]})",
                "outcome": "DIGEST_CONFLICT",
                "rationale": "Different decoded byte values for identical artifact & algorithm prove digest conflict. Strictly prohibited from asserting mirror tampering or corruption.",
            })
            return {
                "category": "DIGEST_CONFLICT",
                "subcode": "ARTIFACT_DIGEST_MISMATCH",
                "confidence": 1.0,
                "summary": "Digest conflict observed between sources for identical artifact and algorithm",
                "details": f"Digest discrepancy on artifact '{id_a}' for algorithm(s): {', '.join([c[0] for c in conflict_algos])}. Evidence proves conflicting digests across sources. Enforcing hard constraint: strictly prohibited from asserting mirror corruption or malicious tampering.",
                "avoided_false_positive": "Avoided defamatory or premature assertion of 'mirror tampered / compromised'; accurately scoped factual claim to verifiable 'digest conflict'.",
            }

        audit_trail.append({
            "rule_id": "DIGEST_03_VALUE_COMPARISON",
            "condition_evaluated": f"bytes_match(shared={shared_algos})",
            "outcome": "PASS",
            "rationale": "Identical artifact and identical algorithm hashes match perfectly at byte level.",
        })
        return None

    def _evaluate_sync_delay(
        self, norm_data: Dict[str, Any], audit_trail: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Evaluate synchronization delay between upstream registry and downstream indexer (deps.dev).
        Requires temporal evidence:
        - HTTP success on subsequent appearance observation (status 200).
        - Valid publication timestamp.
        - Forward chronological order: t_observed_after > t_observed_before > t_published.
        - Demoted suspect / retracted cases output undecidable preserving uncertainty.
        """
        reg = norm_data["sources"].get("registry", {})
        deps = norm_data["sources"].get("deps_dev", {})

        # If downstream returned 404 while upstream is 200 available
        if reg.get("available") and not deps.get("available") and deps.get("status") == 404:
            # Check 0: Suspect or retracted status check (archgraph-layout demotion)
            if norm_data.get("verification_status") == "suspect" or norm_data.get("audit_status") == "retracted":
                audit_trail.append({
                    "rule_id": "SYNC_00_VERIFICATION_STATUS",
                    "condition_evaluated": "verification_status == 'suspect' or audit_status == 'retracted'",
                    "outcome": "UNDECIDABLE_SUSPECT",
                    "rationale": "Observation temporal chain is marked verification_status: suspect / retracted due to temporal inconsistency or lack of raw audit corroboration. Demoted to suspect pending reverification.",
                })
                return {
                    "category": "INDETERMINATE",
                    "subcode": "undecidable",
                    "confidence": 0.4,
                    "summary": "疑似延迟，时间链待核验 (Suspected sync delay, temporal chain unproven)",
                    "details": "Downstream deps.dev returned HTTP 404 while upstream registry was available, but observation is marked verification_status: 'suspect' / retracted due to temporal chain inconsistency against audit environment. Demoted to suspect; delay is undecidable pending reverification.",
                    "avoided_false_positive": "Avoided prematurely asserting proven sync delay when observation temporal chain contains unverified or inverted timestamps.",
                }

            up_time_str = reg.get("published_at")
            fetch_time_str = norm_data.get("fetch_timestamp")
            tolerance_seconds = self.rules.get("hard_constraints", {}).get("sync_delay", {}).get(
                "tolerance_window_seconds", self.DEFAULT_SYNC_DELAY_TOLERANCE_SECONDS
            )

            # Check 1: Missing upstream publication time -> undecidable
            if not up_time_str:
                audit_trail.append({
                    "rule_id": "SYNC_01_TEMPORAL_WINDOW",
                    "condition_evaluated": "upstream_available=True, downstream_status=404, upstream_published_at=None",
                    "outcome": "UNDECIDABLE",
                    "rationale": "Downstream indexer returned 404, but upstream registry does not provide a release publication timestamp. Lacking temporal evidence, sync delay cannot be determined.",
                })
                return {
                    "category": "INDETERMINATE",
                    "subcode": "undecidable",
                    "confidence": 0.3,
                    "summary": "Synchronization delay cannot be verified due to missing upstream publication timestamp",
                    "details": "Downstream deps.dev returned HTTP 404, but upstream registry does not provide a release publication timestamp. Enforcing hard constraint: without temporal evidence, sync delay is undecidable (suspected delay with low confidence 0.3).",
                    "avoided_false_positive": "Avoided misclassifying missing package or dead link as normal sync latency when publication time is unknown.",
                }

            time_diff_seconds = None
            if fetch_time_str:
                time_diff_seconds = self._calc_time_diff_seconds(up_time_str, fetch_time_str)

            if time_diff_seconds is None or time_diff_seconds <= 0:
                audit_trail.append({
                    "rule_id": "SYNC_01_TEMPORAL_WINDOW",
                    "condition_evaluated": f"upstream_published_at='{up_time_str}', fetch_time='{fetch_time_str}', delta={time_diff_seconds}",
                    "outcome": "UNDECIDABLE",
                    "rationale": "Invalid or unparseable temporal window between release and observation. Outputting undecidable.",
                })
                return {
                    "category": "INDETERMINATE",
                    "subcode": "undecidable",
                    "confidence": 0.3,
                    "summary": "Synchronization delay cannot be verified due to unparseable temporal delta or time inversion",
                    "details": f"Upstream published_at '{up_time_str}' and fetch_timestamp '{fetch_time_str}' could not yield a valid forward time delta (delta={time_diff_seconds}). Delay is undecidable.",
                    "avoided_false_positive": "Avoided temporal calculation error false positive.",
                }

            # Check 2: Subsequent observation must exist
            subsequent_obs = deps.get("subsequent_observation")
            if not subsequent_obs:
                audit_trail.append({
                    "rule_id": "SYNC_02_OBSERVATION_CHAIN",
                    "condition_evaluated": "single_404_observation_without_subsequent_appearance",
                    "outcome": "UNDECIDABLE",
                    "rationale": "Only a single 404 observation exists without subsequent appearance observation to establish proven delay range. Preserving uncertainty as undecidable / suspected delay.",
                })
                return {
                    "category": "INDETERMINATE",
                    "subcode": "undecidable",
                    "confidence": 0.5,
                    "summary": "Suspected synchronization delay undecidable without subsequent appearance observation",
                    "details": f"Upstream registry reports release at '{up_time_str}'. Only a single 404 observation at '{fetch_time_str}' exists (+{int(time_diff_seconds)}s). Without a subsequent appearance observation to prove resolution, ingestion delay range cannot be proven. Enforcing hard constraint: outputs undecidable / suspected delay with low confidence 0.5.",
                    "avoided_false_positive": "Avoided asserting sync delay without multi-point temporal evidence chain.",
                }

            # Check 3: Subsequent observation HTTP status must be success (2xx)
            sub_status = subsequent_obs.get("status")
            if not isinstance(sub_status, int):
                audit_trail.append({
                    "rule_id": "SYNC_02_SUBSEQUENT_STATUS",
                    "condition_evaluated": f"subsequent_status={sub_status} (is integer)",
                    "outcome": "UNDECIDABLE_INVALID_STATUS",
                    "rationale": f"Subsequent observation returned invalid non-integer HTTP status '{sub_status}'.",
                })
                return {
                    "category": "INDETERMINATE",
                    "subcode": "undecidable",
                    "confidence": 0.3,
                    "summary": f"Subsequent observation invalid status ({sub_status}); sync delay cannot be verified",
                    "details": f"Subsequent observation HTTP status is invalid or missing ({sub_status}). Ingestion success is not established; delay is undecidable.",
                    "avoided_false_positive": "Avoided computing delay without valid HTTP status.",
                }

            if not (200 <= sub_status < 300):
                if 300 <= sub_status < 400:
                    status_desc = f"non-success redirect HTTP {sub_status}"
                    rat_desc = f"Subsequent observation returned redirect HTTP {sub_status}. Redirection does not prove final ingestion success."
                elif 400 <= sub_status < 500:
                    status_desc = f"non-success client error HTTP {sub_status}"
                    rat_desc = f"Subsequent observation returned client error HTTP {sub_status}. Package remains uningested or missing downstream."
                elif 500 <= sub_status < 600:
                    status_desc = f"non-success server error HTTP {sub_status}"
                    rat_desc = f"Subsequent observation returned server error HTTP {sub_status}. Indexer server failure prevents delay verification."
                else:
                    status_desc = f"non-success HTTP {sub_status}"
                    rat_desc = f"Subsequent observation returned non-success HTTP {sub_status}."

                audit_trail.append({
                    "rule_id": "SYNC_02_SUBSEQUENT_STATUS",
                    "condition_evaluated": f"subsequent_status={sub_status} (expected HTTP 2xx)",
                    "outcome": f"UNDECIDABLE_HTTP_{sub_status}",
                    "rationale": rat_desc,
                })
                return {
                    "category": "INDETERMINATE",
                    "subcode": "undecidable",
                    "confidence": 0.4,
                    "summary": f"Subsequent observation {status_desc}; sync delay cannot be verified",
                    "details": f"Upstream registry reports release at '{up_time_str}'. Initial 404 observed at '{fetch_time_str}'. However, subsequent observation returned {status_desc} instead of successful 2xx. Ingestion success is not established; delay is undecidable (suspected delay with uncertainty preserved).",
                    "avoided_false_positive": "Avoided asserting resolved synchronization delay when downstream indexer returned error or redirect.",
                }

            # Check 4: Subsequent observation timestamp valid
            sub_ts = subsequent_obs.get("observed_at") or subsequent_obs.get("fetch_timestamp")
            if not sub_ts:
                audit_trail.append({
                    "rule_id": "SYNC_02_SUBSEQUENT_TIMESTAMP",
                    "condition_evaluated": "subsequent_observation.observed_at is None",
                    "outcome": "UNDECIDABLE_MISSING_TIME",
                    "rationale": "Subsequent observation lacks a valid timestamp. Ingestion delay range cannot be computed.",
                })
                return {
                    "category": "INDETERMINATE",
                    "subcode": "undecidable",
                    "confidence": 0.4,
                    "summary": "Subsequent observation missing timestamp; sync delay cannot be verified",
                    "details": "Subsequent observation lacks a valid timestamp. Ingestion delay range cannot be computed; outputting undecidable (suspected delay).",
                    "avoided_false_positive": "Avoided computing delay without valid subsequent observation timestamp.",
                }

            # Check 4b: Temporal order check: t_observed_after > t_observed_before
            delta_after = self._calc_time_diff_seconds(fetch_time_str, sub_ts)
            if delta_after is None or delta_after <= 0:
                audit_trail.append({
                    "rule_id": "SYNC_02_TEMPORAL_ORDER",
                    "condition_evaluated": f"t_observed_after ('{sub_ts}') > t_observed_before ('{fetch_time_str}')",
                    "outcome": "UNDECIDABLE_TIME_INVERSION",
                    "rationale": f"Temporal order invalid: subsequent observation '{sub_ts}' is not strictly greater than initial observation '{fetch_time_str}'. Outputting undecidable.",
                })
                return {
                    "category": "INDETERMINATE",
                    "subcode": "undecidable",
                    "confidence": 0.4,
                    "summary": "Temporal order invalid (time inversion); sync delay cannot be verified",
                    "details": f"Subsequent observation timestamp '{sub_ts}' does not strictly succeed initial observation '{fetch_time_str}' (delta: {delta_after}s). Lacking valid forward temporal order, delay cannot be proven; outputting undecidable (suspected delay).",
                    "avoided_false_positive": "Avoided asserting sync delay when observation order is inverted or concurrent.",
                }

            # Check 5: Subsequent observation must not be in the future (t_observed_after <= real current_time)
            # Must check against real wall clock: input evaluation_timestamp MUST NOT be trusted.
            sub_dt = self._parse_iso_ts(sub_ts)
            now_dt = datetime.now(timezone.utc)
            if sub_dt and sub_dt > now_dt:
                audit_trail.append({
                    "rule_id": "SYNC_02_FUTURE_TIMESTAMP",
                    "condition_evaluated": f"t_observed_after ('{sub_ts}') <= current_time ('{now_dt.isoformat()}')",
                    "outcome": "UNDECIDABLE_FUTURE_TIME",
                    "rationale": f"Subsequent observation timestamp '{sub_ts}' is in the future relative to real system clock ({now_dt.isoformat()}). Input evaluation_timestamp cannot override real current time.",
                })
                return {
                    "category": "INDETERMINATE",
                    "subcode": "undecidable",
                    "confidence": 0.4,
                    "summary": "Subsequent observation timestamp is in the future; sync delay cannot be verified",
                    "details": f"Subsequent observation timestamp '{sub_ts}' exceeds real current time ({now_dt.isoformat()}). Enforcing hard constraint: future timestamps are strictly rejected against real system clock (input evaluation_timestamp is not trusted); delay is undecidable.",
                    "avoided_false_positive": "Avoided prematurely asserting resolved sync delay based on unreached future observation timestamps.",
                }

            # If all checks passed, calculate provable range
            sub_diff = self._calc_time_diff_seconds(up_time_str, sub_ts)
            max_delay = sub_diff if sub_diff is not None else time_diff_seconds
            is_within_tolerance = (max_delay <= tolerance_seconds)

            delay_before_str = self._format_delay_duration(time_diff_seconds)
            delay_after_str = self._format_delay_duration(sub_diff) if sub_diff else delay_before_str
            provable_range_str = f"[{delay_before_str}, {delay_after_str}]"

            if is_within_tolerance:
                tolerance_str = f"within sync tolerance window ({tolerance_seconds}s)"
                summary_text = "Downstream index ingested release with verified temporal delay chain"
                decay = (time_diff_seconds / tolerance_seconds) * 0.15
                confidence = round(max(0.70, 0.98 - decay), 3)
            else:
                tolerance_str = f"exceeds sync tolerance window ({tolerance_seconds}s; observed delay: {self._format_delay_duration(max_delay)})"
                summary_text = f"Downstream index ingested release with verified temporal delay chain (delay: {self._format_delay_duration(max_delay)}, exceeds tolerance {tolerance_seconds}s)"
                confidence = 0.65

            audit_trail.append({
                "rule_id": "SYNC_02_OBSERVATION_CHAIN",
                "condition_evaluated": f"temporal_chain_complete(upstream='{up_time_str}', 404_observed='{fetch_time_str}', HTTP_{sub_status}_observed='{sub_ts}')",
                "outcome": "SYNC_DELAY",
                "rationale": f"Three-stage temporal observation chain confirmed (published -> 404 missing -> HTTP {sub_status} resolved). Provable delay range {provable_range_str} is {tolerance_str}.",
            })
            return {
                "category": "SYNC_DELAY",
                "subcode": "DOWNSTREAM_INGESTION_LAG",
                "confidence": confidence,
                "summary": summary_text,
                "details": f"Upstream registry reports release published at '{up_time_str}'. Temporal observation chain verified: downstream missing (404) observed at '{fetch_time_str}' (delta {delay_before_str}), subsequent appearance (HTTP {sub_status}) observed at '{sub_ts}'. Provable delay range is {provable_range_str}, which {tolerance_str}. Preserving uncertainty; not judged as missing package or mirror defect.",
                "avoided_false_positive": "Avoided misclassifying normal downstream indexing latency as upstream publication failure or missing package integrity fault.",
            }

        return None

    def _evaluate_real_error(
        self, norm_data: Dict[str, Any], audit_trail: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Evaluate real error: cross-source field contradiction where empirical evidence points to one side being wrong.
        E.g. deps.dev labels standard PSF-2.0 as 'non-standard', while PyPI classifiers explicitly record OSI approved status
        and ClearlyDefined confirms standard Python-2.0.1.
        Hard constraint: requires empirical artifact license text evidence; prohibits hardcoded factual claims without evidence.
        """
        reg = norm_data["sources"].get("registry", {})
        deps = norm_data["sources"].get("deps_dev", {})
        cd = norm_data["sources"].get("clearlydefined", {})

        deps_licenses = deps.get("licenses", [])
        reg_classifiers = reg.get("license_classifiers", [])
        cd_declared = cd.get("declared_license")

        # Specific check: deps.dev labels standard OSI/SPDX license as 'non-standard'
        if "non-standard" in deps_licenses:
            has_osi_classifier = any("OSI Approved" in c for c in reg_classifiers)
            is_cd_standard = cd_declared in Normalizer.KNOWN_STANDARD_LICENSES

            if has_osi_classifier or is_cd_standard:
                # Require empirical artifact LICENSE text evidence
                lic_ev = (
                    reg.get("license_text_evidence")
                    or norm_data.get("sources", {}).get("registry", {}).get("license_text_evidence")
                    or norm_data.get("license_text_evidence")
                )
                cd_desc = f"ClearlyDefined confirms '{cd_declared}'" if cd_declared else "ClearlyDefined: 未覆盖"
                if not lic_ev or not lic_ev.get("text_snippet"):
                    audit_trail.append({
                        "rule_id": "ERROR_01_ARTIFACT_LICENSE_EVIDENCE",
                        "condition_evaluated": "has_artifact_license_text_evidence=False",
                        "outcome": "UNDECIDABLE_NO_LICENSE_EVIDENCE",
                        "rationale": "Downstream reports 'non-standard' vs classifiers/ClearlyDefined, but no empirical artifact LICENSE text evidence is provided. Without direct artifact evidence, REAL_ERROR cannot be proven.",
                    })
                    return {
                        "category": "INDETERMINATE",
                        "subcode": "undecidable",
                        "confidence": 0.5,
                        "summary": "Cannot verify real error due to missing artifact LICENSE text evidence",
                        "details": f"deps.dev reports licenses: {deps_licenses}. While registry classifiers contain {[c for c in reg_classifiers if 'OSI Approved' in c]} and {cd_desc}, no artifact LICENSE text evidence was provided. Without empirical artifact license text, REAL_ERROR cannot be asserted. Enforcing hard constraint: missing evidence strictly outputs 'undecidable'.",
                        "avoided_false_positive": "Avoided uncorroborated REAL_ERROR assertion without empirical artifact license text proof.",
                    }

                # Verify that license text snippet contains proof matching standard license text
                has_match, match_reason = self._has_standard_license_match_evidence(lic_ev)
                file_name = lic_ev.get("file", "dist-info/LICENSE")
                spdx_id = lic_ev.get("spdx_identifier", "standard license")

                if not has_match:
                    audit_trail.append({
                        "rule_id": "ERROR_01_ARTIFACT_LICENSE_EVIDENCE",
                        "condition_evaluated": f"has_standard_license_match_evidence=False ({match_reason})",
                        "outcome": "UNDECIDABLE_NO_MATCHING_LICENSE_TEXT",
                        "rationale": f"Artifact license text snippet provided, but lacks evidence matching standard text: {match_reason}. Without verified match to standard text, REAL_ERROR cannot be proven.",
                    })
                    return {
                        "category": "INDETERMINATE",
                        "subcode": "undecidable",
                        "confidence": 0.5,
                        "summary": "Cannot verify real error: artifact license text lacks standard text match evidence",
                        "details": f"deps.dev reports licenses: {deps_licenses}. While registry classifiers contain {[c for c in reg_classifiers if 'OSI Approved' in c]} and {cd_desc}, artifact license text snippet lacks verified match evidence against standard license text ({match_reason}). Without empirical evidence demonstrating equivalence to standard text, REAL_ERROR cannot be asserted. Enforcing hard constraint: outputs undecidable.",
                        "avoided_false_positive": "Avoided asserting REAL_ERROR on arbitrary text snippet without verified match to standard license text.",
                    }

                audit_trail.append({
                    "rule_id": "ERROR_01_STANDARDS_CONTRADICTION",
                    "condition_evaluated": f"deps.dev reported 'non-standard' vs (osi_classifier={has_osi_classifier}, cd_standard={is_cd_standard}, artifact_evidence='{file_name}')",
                    "outcome": "REAL_ERROR",
                    "rationale": f"Cross-source license classification contradiction: PyPI classifiers, ClearlyDefined, and artifact license text ({file_name}, {spdx_id}) confirm standard license, while downstream indexer classifies it as non-standard. Because authoring field omission vs parser fault cannot be definitively proven, unilateral parser blame assertion is removed.",
                })
                return {
                    "category": "REAL_ERROR",
                    "subcode": "STANDARDS_CONTRADICTION",
                    "confidence": 1.0,
                    "summary": "Downstream index license classification contradicts upstream and curated standards",
                    "details": f"deps.dev reports licenses: {deps_licenses}. In contrast, PyPI registry classifiers contain '{[c for c in reg_classifiers if 'OSI Approved' in c]}' and {cd_desc}. The artifact {file_name} contains verified license text ({spdx_id}). Because authoring field omission versus downstream classifier parsing fault cannot be separated, unilateral parser responsibility assertion is removed; recorded verifiable metadata contradiction.",
                    "avoided_false_positive": "Avoided discarding or flagging a legitimate package as license-incompatible while avoiding unverified attribution of parser fault.",
                }

        return None

    def _evaluate_semantic_divergence(
        self, norm_data: Dict[str, Any], audit_trail: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Evaluate semantic divergence: e.g. license AND/OR compound expressions or conflicting license declarations (MIT vs Apache-2.0).
        Hard constraint: Cannot automatically assume both sides are right or pick one without actual field comparison.
        """
        reg = norm_data["sources"].get("registry", {})
        cd = norm_data["sources"].get("clearlydefined", {})
        deps = norm_data["sources"].get("deps_dev", {})

        reg_lics = reg.get("licenses", [])
        reg_str = reg_lics[0] if reg_lics else None
        cd_declared = cd.get("declared_license")
        cd_discovered = cd.get("discovered_licenses", [])
        deps_lics = deps.get("licenses", [])

        # 1. Compound boolean operator disparity (e.g. esprima)
        if reg_str and cd_declared and reg_str != cd_declared:
            has_and = (" AND " in cd_declared or " AND " in reg_str)
            has_or = (" OR " in cd_declared or " OR " in reg_str)
            if has_and or has_or:
                if has_or and not has_and:
                    subcode = "LICENSE_EXPRESSION_DISJUNCTION_MISMATCH"
                    summary = "Declared package license diverges from discovered multi-license OR disjunction"
                    op_desc = "compound OR disjunction grants licensee choice among alternative licenses under SPDX semantics"
                    avoided_fp = "Avoided naive diff failure that blindly accepts the single declaration while ignoring disjunctive alternative licensing choices under SPDX semantics."
                    rationale_desc = "scanned deep license disjunction (choice under SPDX semantics)"
                elif has_and and not has_or:
                    subcode = "LICENSE_EXPRESSION_CONJUNCTION_MISMATCH"
                    summary = "Declared package license diverges from deeply discovered multi-license AND conjunction"
                    op_desc = "compound AND conjunction imposes distinct dual compliance obligations"
                    avoided_fp = "Avoided naive diff failure that blindly accepts the simple top-level declaration while ignoring dual-clause compliance obligations discovered in repository files."
                    rationale_desc = "scanned deep license conjunction"
                else:
                    subcode = "LICENSE_EXPRESSION_COMPOUND_OPERATOR_MISMATCH"
                    summary = "Declared package license diverges from discovered compound boolean license expression (AND/OR)"
                    op_desc = "compound boolean operators (AND conjunction and OR disjunction) define concurrent obligations and alternative choices under SPDX semantics"
                    avoided_fp = "Avoided naive diff failure by accounting for compound boolean licensing operators under SPDX semantics."
                    rationale_desc = "scanned compound boolean license expression (AND/OR under SPDX semantics)"

                audit_trail.append({
                    "rule_id": "SEMANTIC_01_BOOLEAN_OPERATOR_DISPARITY",
                    "condition_evaluated": f"registry.license='{reg_str}' != clearlydefined.licensed.declared='{cd_declared}'",
                    "outcome": "SEMANTIC_DIVERGENCE",
                    "rationale": f"Declared package license differs from {rationale_desc}. Sources consulted: npm_registry (field: license), clearlydefined (fields: licensed.declared, licensed.facets.core.discovered.expressions), deps_dev (field: licenses). Scan scope: ClearlyDefined full-repo core facet file scan vs npm top-level packument declaration. Hard constraint strictly disallows automatic acceptance of either side.",
                })
                return {
                    "category": "SEMANTIC_DIVERGENCE",
                    "subcode": subcode,
                    "confidence": 0.95,
                    "summary": summary,
                    "details": (
                        f"Evaluated sources and fields: "
                        f"(1) npm_registry (field: 'license' -> '{reg_str}'), "
                        f"(2) clearlydefined (field: 'licensed.declared' -> '{cd_declared}', "
                        f"field: 'licensed.facets.core.discovered.expressions' -> {cd_discovered}), "
                        f"(3) deps_dev (field: 'licenses' -> {deps_lics}). "
                        f"Scan scope: ClearlyDefined core facet file-level source tree scan discovered dual licenses, "
                        f"whereas npm registry and deps.dev reflect top-level package.json declaration. "
                        f"The presence of {op_desc} that cannot "
                        f"be reconciled by simple equality. Enforcing hard constraint: neither side is automatically assumed as the sole truth."
                    ),
                    "avoided_false_positive": avoided_fp,
                }

        # 2. General cross-source license divergence check (e.g. MIT vs Apache-2.0, MIT vs non-standard)
        sources = norm_data.get("sources", {})
        source_license_map: Dict[str, List[str]] = {}
        for s_key, s_val in sources.items():
            if not (s_val.get("available") and s_val.get("status") == 200):
                continue
            lics = s_val.get("licenses") or []
            if not lics and s_val.get("declared_license"):
                lics = [s_val["declared_license"]]
            if lics:
                source_license_map[s_key] = [str(x).strip() for x in lics if str(x).strip()]

        s_keys = sorted(list(source_license_map.keys()))
        for i in range(len(s_keys)):
            for j in range(i + 1, len(s_keys)):
                k1, k2 = s_keys[i], s_keys[j]
                lics1 = set(source_license_map[k1])
                lics2 = set(source_license_map[k2])
                if lics1 != lics2:
                    audit_trail.append({
                        "rule_id": "SEMANTIC_02_LICENSE_DISCREPANCY",
                        "condition_evaluated": f"{k1}.licenses ({sorted(lics1)}) != {k2}.licenses ({sorted(lics2)})",
                        "outcome": "SEMANTIC_DIVERGENCE",
                        "rationale": f"Explicit cross-source license divergence: source '{k1}' declares {sorted(lics1)} while source '{k2}' declares {sorted(lics2)}. Enforcing hard constraint: prohibited from judging consistent without comparison.",
                    })
                    return {
                        "category": "SEMANTIC_DIVERGENCE",
                        "subcode": "LICENSE_DECLARATION_DISCREPANCY",
                        "confidence": 0.95,
                        "summary": f"Cross-source license declarations diverge ({', '.join(sorted(lics1))} vs {', '.join(sorted(lics2))})",
                        "details": f"Cross-source metadata comparison detected license divergence: source '{k1}' reports {sorted(lics1)} while source '{k2}' reports {sorted(lics2)}. Enforcing hard constraint: prohibited from judging consistent without comparison.",
                        "avoided_false_positive": "Avoided false-positive CONSISTENT verdict by actively comparing license fields across sources.",
                    }

        return None

    def _evaluate_consistent(
        self, norm_data: Dict[str, Any], audit_trail: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluate consistency when no prior rules triggered divergence or delay.
        Hard constraints:
        - Empty or missing evidence MUST NOT return CONSISTENT, must return undecidable.
        - If any source lacks comparable fields, MUST NOT return CONSISTENT, must return undecidable.
        - Strict prohibition: 'no comparison, no consistency'.
        - Consistent confidence is calculated dynamically based on evidence strength, strictly < 1.0.
        """
        sources = norm_data.get("sources", {})
        avail_sources = [s for s in sources.values() if s.get("available") and s.get("status") == 200]

        # Check 1: Evidence sufficiency (< 2 sources)
        if len(avail_sources) < 2:
            audit_trail.append({
                "rule_id": "CONSISTENCY_01_EVIDENCE_SUFFICIENCY",
                "condition_evaluated": f"available_sources_count={len(avail_sources)} >= 2",
                "outcome": "INSUFFICIENT_EVIDENCE",
                "rationale": "Evidence is empty or insufficient. At least two available comparison sources are required to verify consistency across sources.",
            })
            return {
                "category": "INDETERMINATE",
                "subcode": "undecidable",
                "confidence": 0.0,
                "summary": "Cannot determine consistency due to empty or missing comparison evidence",
                "details": f"Fewer than two available sources were present for comparison (found {len(avail_sources)}). Enforcing hard constraint: empty or missing evidence strictly outputs 'undecidable', NEVER defaults to CONSISTENT.",
                "avoided_false_positive": "Avoided false-positive 'CONSISTENT' verdict when verification evidence is absent or uncorroborated.",
            }

        # Check 2: Sources must provide substantive metadata
        has_substantive = any(
            bool(s.get("licenses") or s.get("artifacts") or s.get("declared_license") or s.get("published_at"))
            for s in avail_sources
        )
        if not has_substantive:
            audit_trail.append({
                "rule_id": "CONSISTENCY_01_EVIDENCE_SUBSTANCE",
                "condition_evaluated": "has_substantive_metadata=False",
                "outcome": "EMPTY_EVIDENCE",
                "rationale": "Available sources contain empty metadata fields. Empty evidence strictly outputs undecidable.",
            })
            return {
                "category": "INDETERMINATE",
                "subcode": "undecidable",
                "confidence": 0.0,
                "summary": "Cannot determine consistency due to empty metadata fields across sources",
                "details": "Available sources lack substantive metadata fields (no licenses, artifacts, or timestamps). Enforcing hard constraint: empty evidence cannot be judged CONSISTENT.",
                "avoided_false_positive": "Avoided asserting consistency on empty or vacuous metadata.",
            }

        # Check 3: Comparable license declarations check across sources
        def _get_substantive_licenses(s: Dict[str, Any]) -> List[str]:
            raw_lics = s.get("licenses") or []
            if not raw_lics and s.get("declared_license"):
                raw_lics = [s["declared_license"]]
            clean_list = []
            for item in raw_lics:
                if not isinstance(item, str):
                    continue
                s_item = item.strip()
                if not s_item or s_item.lower() in self.UNINFORMATIVE_LICENSES:
                    continue
                clean_list.append(s_item)
            return clean_list

        sources_with_license = [
            s.get("source_id", "unknown") for s in avail_sources
            if bool(_get_substantive_licenses(s))
        ]
        sources_without_license = [
            s.get("source_id", "unknown") for s in avail_sources
            if not bool(_get_substantive_licenses(s))
        ]

        if not sources_with_license:
            audit_trail.append({
                "rule_id": "CONSISTENCY_01_COMPARABLE_LICENSE",
                "condition_evaluated": "has_comparable_license_declarations(sources)",
                "outcome": "NO_COMPARABLE_LICENSE_EVIDENCE",
                "rationale": "Neither source provides a substantive license declaration (all empty, missing, or placeholder values). Without comparable license evidence, metadata consistency cannot be determined.",
            })
            return {
                "category": "INDETERMINATE",
                "subcode": "undecidable",
                "confidence": 0.0,
                "summary": "Cannot determine consistency: no comparable license evidence across sources",
                "details": "None of the available sources provide verifiable license declarations (found only empty arrays, whitespace, or placeholder values such as 'unknown' or 'see license file'). Lacking comparable license evidence, metadata consistency is undecidable. Enforcing hard constraint: absent license evidence strictly yields 'undecidable', NEVER defaults to CONSISTENT.",
                "avoided_false_positive": "Avoided false-positive CONSISTENT verdict when sources lack substantive license declarations entirely.",
            }

        if sources_with_license and sources_without_license:
            audit_trail.append({
                "rule_id": "CONSISTENCY_01_COMPARABLE_FIELDS",
                "condition_evaluated": f"all_sources_have_comparable_licenses(with={sources_with_license}, without={sources_without_license})",
                "outcome": "INCOMPARABLE_FIELDS",
                "rationale": f"One source provides license fields ({sources_with_license}) while another lacks comparable fields ({sources_without_license}). Lacking comparable fields, consistency cannot be determined.",
            })
            return {
                "category": "INDETERMINATE",
                "subcode": "undecidable",
                "confidence": 0.0,
                "summary": "Cannot determine consistency due to missing comparable license fields across sources",
                "details": f"Source(s) {sources_with_license} provide license declarations, but source(s) {sources_without_license} lack comparable license metadata. Enforcing hard constraint: missing comparable fields strictly outputs 'undecidable', NEVER defaults to CONSISTENT.",
                "avoided_false_positive": "Avoided false-positive 'CONSISTENT' verdict when one source lacks comparable fields to verify against.",
            }

        # Check 4: Check release timestamps consistency across ALL sources providing published_at
        ts_map: Dict[str, str] = {}
        for s in avail_sources:
            pub = s.get("published_at")
            if pub and str(pub).strip():
                ts_map[s.get("source_id", "src")] = str(pub).strip()

        if len(ts_map) >= 2:
            ts_keys = list(ts_map.keys())
            for i in range(len(ts_keys)):
                for j in range(i + 1, len(ts_keys)):
                    k1, k2 = ts_keys[i], ts_keys[j]
                    t1, t2 = ts_map[k1], ts_map[k2]
                    diff_sec = self._calc_time_diff_seconds(t1, t2)
                    if diff_sec is not None and abs(diff_sec) > 86400:
                        audit_trail.append({
                            "rule_id": "CONSISTENCY_01_TIMESTAMP_DISCREPANCY",
                            "condition_evaluated": f"release_timestamp_match({k1}='{t1}', {k2}='{t2}', delta={diff_sec}s)",
                            "outcome": "TIMESTAMP_DIVERGENCE",
                            "rationale": f"Cross-source release publication timestamp discrepancy: {k1} reports '{t1}' vs {k2} reports '{t2}' (delta {int(abs(diff_sec))}s exceeds 86400s). Cannot determine consistency.",
                        })
                        return {
                            "category": "INDETERMINATE",
                            "subcode": "undecidable",
                            "confidence": 0.2,
                            "summary": "Cannot determine consistency due to contradictory release publication timestamps",
                            "details": f"Available sources report conflicting release publication timestamps ({k1}: '{t1}' vs {k2}: '{t2}', delta: {int(abs(diff_sec))}s). Pairwise timestamp discrepancy exceeds tolerance window (86400s). Metadata consistency is undecidable.",
                            "avoided_false_positive": "Avoided false-positive CONSISTENT verdict when publication timestamps disagree across sources.",
                        }

        # Actual comparison passed! Compute confidence dynamically based on evidence strength (strictly < 1.0)
        # Formula:
        # Base: 0.70
        # + Corroborated dimensions: license (+0.06), artifacts (+0.06), repository (+0.03), timestamps (+0.03)
        # + Source independence: independent sources >= 2 (+0.08), single independent + derived mirror (+0.02)
        # - Temporal span penalty: max |t1 - t2| / 86400 * 0.08
        dim_bonus = 0.0
        if len(sources_with_license) >= 2:
            dim_bonus += 0.06
        art_sources = [s for s in avail_sources if s.get("artifacts")]
        if len(art_sources) >= 2:
            dim_bonus += 0.06
        repo_sources = [s for s in avail_sources if s.get("repository")]
        if len(repo_sources) >= 2:
            dim_bonus += 0.03
        if len(ts_map) >= 2:
            dim_bonus += 0.03

        independent_sources = [s for s in avail_sources if not s.get("derived_from")]
        if len(independent_sources) >= 2 or any(s.get("source_id") == "clearlydefined" for s in avail_sources):
            indep_bonus = 0.08
        else:
            indep_bonus = 0.02

        time_penalty = 0.0
        if len(ts_map) >= 2:
            ts_keys = list(ts_map.keys())
            max_delta = max(
                abs(self._calc_time_diff_seconds(ts_map[ts_keys[i]], ts_map[ts_keys[j]]) or 0)
                for i in range(len(ts_keys))
                for j in range(i + 1, len(ts_keys))
            )
            time_penalty = min(0.08, (max_delta / 86400.0) * 0.08)

        confidence = 0.70 + dim_bonus + indep_bonus - time_penalty
        confidence = min(0.95, max(0.60, round(confidence, 3)))

        audit_trail.append({
            "rule_id": "CONSISTENCY_02_CORROBORATION",
            "condition_evaluated": f"all_sources_match(sources_count={len(avail_sources)})",
            "outcome": "CONSISTENT",
            "rationale": f"Metadata fields are mutually consistent across available corroborating sources with verified comparable fields. Confidence calculated at {confidence} based on evidence strength (strictly < 1.0).",
        })
        return {
            "category": "CONSISTENT",
            "subcode": "MUTUALLY_CONSISTENT",
            "confidence": confidence,
            "summary": "Package metadata is consistent across consulted sources",
            "details": f"All verified coordinates, release timestamps, and license declarations match across {len(avail_sources)} available sources (evaluated confidence: {confidence} based on evidence strength).",
            "avoided_false_positive": "Verified consistent metadata across sources without false alarm.",
        }

    def _calc_time_diff_seconds(self, t1_str: str, t2_str: str) -> Optional[float]:
        """Calculate signed delta (t2 - t1) in seconds between two ISO-8601 timestamps."""
        try:
            dt1 = self._parse_iso_ts(t1_str)
            dt2 = self._parse_iso_ts(t2_str)
            if dt1 is None or dt2 is None:
                return None
            return (dt2 - dt1).total_seconds()
        except Exception:
            return None
