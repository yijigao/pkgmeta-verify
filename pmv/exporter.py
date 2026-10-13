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
Evidence Exporter module.
Produces minimal redistributable snapshots, saves verification results,
and generates cryptographic SHA-256 manifests for offline reproducibility.
"""

import hashlib
import json
import os
from typing import Any, Dict, List, Optional
from .collector import purl_to_snapshot_filename


class Exporter:
    """Exports sanitized minimal snapshots, verification results, and SHA-256 manifests."""

    def __init__(self, base_evidence_dir: str):
        self.base_dir = base_evidence_dir
        self.snapshots_dir = os.path.join(self.base_dir, "snapshots")
        self.results_dir = os.path.join(self.base_dir, "results")
        os.makedirs(self.snapshots_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)

    def sanitize_raw_bundle(self, raw_bundle: Dict[str, Any]) -> Dict[str, Any]:
        """
        Produce a minimal redistributable snapshot by trimming bulky, non-essential data
        (such as huge readme texts, user email addresses, or unneeded historic versions).
        """
        sanitized = {
            "purl": raw_bundle["purl"],
            "ecosystem": raw_bundle["ecosystem"],
            "name": raw_bundle["name"],
            "version": raw_bundle["version"],
            "fetch_timestamp": raw_bundle.get("fetch_timestamp"),
            "synthetic": raw_bundle.get("synthetic", False),
            "sources": {},
        }

        for s_key, s_val in raw_bundle.get("sources", {}).items():
            status = s_val.get("status")
            data = s_val.get("data")
            clean_data = None

            if status == 200 and isinstance(data, dict):
                clean_data = self._sanitize_source_data(s_key, raw_bundle["ecosystem"], raw_bundle["version"], data)
            else:
                clean_data = data

            sanitized["sources"][s_key] = {
                "source_id": s_val.get("source_id", s_key),
                "role": s_val.get("role"),
                "endpoint": s_val.get("endpoint"),
                "status": status,
                "data": clean_data,
                "derived_from": s_val.get("derived_from"),
            }
            if "registry_interface_note" in s_val:
                sanitized["sources"][s_key]["registry_interface_note"] = s_val["registry_interface_note"]
            if "license_text_evidence" in s_val:
                sanitized["sources"][s_key]["license_text_evidence"] = s_val["license_text_evidence"]
            if "subsequent_observation" in s_val:
                sanitized["sources"][s_key]["subsequent_observation"] = s_val["subsequent_observation"]

        return sanitized

    def _sanitize_source_data(
        self, s_key: str, ecosystem: str, version: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Keep essential verification fields and strip noisy/bloated attributes."""
        if s_key == "registry":
            if ecosystem == "npm":
                # Keep version metadata, dist hashes, license, repository
                return {
                    "name": data.get("name"),
                    "version": data.get("version"),
                    "license": data.get("license"),
                    "licenses": data.get("licenses"),
                    "repository": data.get("repository"),
                    "dist": {
                        "tarball": data.get("dist", {}).get("tarball"),
                        "shasum": data.get("dist", {}).get("shasum"),
                        "integrity": data.get("dist", {}).get("integrity"),
                    },
                    "publish_time": data.get("publish_time") or (data.get("time", {}).get(version) if isinstance(data.get("time"), dict) else None),
                }
            elif ecosystem == "pypi":
                # Keep info (license, classifiers, project_urls) and target version releases
                releases = data.get("releases", {}).get(version, []) or data.get("urls", [])
                clean_releases = []
                for r in releases:
                    clean_releases.append({
                        "filename": r.get("filename"),
                        "packagetype": r.get("packagetype"),
                        "upload_time_iso_8601": r.get("upload_time_iso_8601") or r.get("upload_time"),
                        "digests": r.get("digests", {}),
                        "md5_digest": r.get("md5_digest"),
                        "url": r.get("url"),
                    })
                info = data.get("info", {})
                res = {
                    "info": {
                        "name": info.get("name"),
                        "version": info.get("version"),
                        "license": info.get("license"),
                        "classifiers": [c for c in info.get("classifiers", []) if c.startswith("License ::") or c.startswith("Development Status ::")],
                        "project_urls": info.get("project_urls"),
                        "home_page": info.get("home_page"),
                    },
                    "releases": {version: clean_releases},
                }
                if "urls" in data:
                    res["urls"] = clean_releases
                if "license_text_evidence" in data:
                    res["license_text_evidence"] = data["license_text_evidence"]
                return res

        elif s_key == "deps_dev":
            res = {
                "versionKey": data.get("versionKey"),
                "publishedAt": data.get("publishedAt"),
                "licenses": data.get("licenses"),
                "links": data.get("links"),
                "isDefault": data.get("isDefault"),
            }
            if "subsequent_observation" in data:
                res["subsequent_observation"] = data["subsequent_observation"]
            if "error" in data:
                res["error"] = data["error"]
            if "body" in data:
                res["body"] = data["body"]
            return res

        elif s_key == "clearlydefined":
            licensed = data.get("licensed", {})
            return {
                "licensed": {
                    "declared": licensed.get("declared"),
                    "facets": {
                        "core": {
                            "discovered": licensed.get("facets", {}).get("core", {}).get("discovered", {})
                        }
                    },
                },
                "described": {
                    "urls": data.get("described", {}).get("urls"),
                    "releaseDate": data.get("described", {}).get("releaseDate"),
                },
            }

        return data

    def save_snapshot(self, sanitized_bundle: Dict[str, Any]) -> str:
        """Write sanitized snapshot to evidence/snapshots/."""
        filename = purl_to_snapshot_filename(sanitized_bundle["purl"])
        path = os.path.join(self.snapshots_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sanitized_bundle, f, indent=2, sort_keys=True)
        return path

    def save_result(self, result: Dict[str, Any]) -> str:
        """Write verification result to evidence/results/."""
        base_name = purl_to_snapshot_filename(result["purl"])
        res_name = base_name.replace(".json", ".result.json")
        path = os.path.join(self.results_dir, res_name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, sort_keys=True)
        return path

    def generate_manifest(self, additional_files: Optional[List[str]] = None) -> str:
        """Compute SHA-256 for all snapshots, results, rules, and additional files."""
        manifest_path = os.path.join(self.base_dir, "MANIFEST.sha256")
        entries = []

        # Snapshots
        for fname in sorted(os.listdir(self.snapshots_dir)):
            if fname.endswith(".json"):
                fpath = os.path.join(self.snapshots_dir, fname)
                rel_path = os.path.relpath(fpath, self.base_dir)
                entries.append((self._sha256_file(fpath), rel_path))

        # Results
        for fname in sorted(os.listdir(self.results_dir)):
            if fname.endswith(".json"):
                fpath = os.path.join(self.results_dir, fname)
                rel_path = os.path.relpath(fpath, self.base_dir)
                entries.append((self._sha256_file(fpath), rel_path))

        # Additional files (e.g. rules, schemas)
        if additional_files:
            for fpath in additional_files:
                if os.path.exists(fpath):
                    rel_path = os.path.relpath(fpath, self.base_dir)
                    entries.append((self._sha256_file(fpath), rel_path))

        with open(manifest_path, "w", encoding="utf-8") as f:
            for sha, rel in sorted(entries, key=lambda x: x[1]):
                f.write(f"{sha}  {rel}\n")

        return manifest_path

    @staticmethod
    def _sha256_file(filepath: str) -> str:
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
