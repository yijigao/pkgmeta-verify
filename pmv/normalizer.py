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
Metadata Normalizer module.
Transforms heterogeneous ecosystem metadata (npm packument, PyPI JSON API, deps.dev v3, ClearlyDefined)
into a canonical normalized representation with strict artifact, digest, and provenance tracking.
"""

from typing import Any, Dict, List, Optional
import urllib.parse


class Normalizer:
    """Normalizes raw package metadata across registries and indexes."""

    # Well-known OSI approved and SPDX identifier lookup
    KNOWN_STANDARD_LICENSES = {
        "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC",
        "GPL-2.0-only", "GPL-3.0-only", "GPL-2.0-or-later", "GPL-3.0-or-later",
        "LGPL-2.1-only", "LGPL-3.0-only", "MPL-2.0", "Python-2.0", "Python-2.0.1",
        "PSF-2.0", "0BSD", "Unlicense", "CC0-1.0", "Zlib"
    }

    def normalize(self, raw_bundle: Dict[str, Any]) -> Dict[str, Any]:
        """Produce canonical normalized evidence and provenance records."""
        ecosystem = raw_bundle["ecosystem"]
        purl = raw_bundle["purl"]
        name = raw_bundle["name"]
        version = raw_bundle["version"]
        fetch_ts = raw_bundle.get("fetch_timestamp")
        synthetic = raw_bundle.get("synthetic", False)

        sources = raw_bundle.get("sources", {})
        norm_sources: Dict[str, Any] = {}

        for src_key, src_val in sources.items():
            if src_key == "registry":
                norm_sources[src_key] = self._normalize_registry(ecosystem, name, version, src_val)
            elif src_key == "deps_dev":
                norm_sources[src_key] = self._normalize_deps_dev(ecosystem, name, version, src_val)
            elif src_key == "clearlydefined":
                norm_sources[src_key] = self._normalize_clearlydefined(name, version, src_val)
            elif src_key.startswith("synthetic"):
                norm_sources[src_key] = self._normalize_synthetic(src_val)

        # Provenance DAG and dependency tracking
        dependency_relations = self._build_dependency_relations(ecosystem, sources)

        return {
            "purl": purl,
            "ecosystem": ecosystem,
            "name": name,
            "version": version,
            "fetch_timestamp": fetch_ts,
            "synthetic": synthetic,
            "sources": norm_sources,
            "dependency_relations": dependency_relations,
        }

    def _normalize_registry(
        self, ecosystem: str, name: str, version: str, src: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Normalize primary registry response (npm packument or PyPI JSON)."""
        status = src.get("status", 0)
        data = src.get("data", {})
        endpoint = src.get("endpoint", "")
        role = src.get("role", "upstream_registry")

        if status != 200 or not isinstance(data, dict):
            return {
                "source_id": src.get("source_id", "registry"),
                "role": role,
                "status": status,
                "endpoint": endpoint,
                "available": False,
                "published_at": None,
                "artifacts": [],
                "licenses": [],
                "repository": None,
                "derived_from": None,
            }

        published_at = None
        artifacts: List[Dict[str, Any]] = []
        licenses: List[str] = []
        license_classifiers: List[str] = []
        repository = None

        if ecosystem == "npm":
            # npm packument
            published_at = data.get("publish_time") or (data.get("time", {}).get(version) if isinstance(data.get("time"), dict) else None)
            lic = data.get("license")
            if isinstance(lic, str):
                licenses.append(lic)
            elif isinstance(lic, dict) and "type" in lic:
                licenses.append(lic["type"])
            elif isinstance(data.get("licenses"), list):
                for l_item in data["licenses"]:
                    if isinstance(l_item, dict) and "type" in l_item:
                        licenses.append(l_item["type"])
                    elif isinstance(l_item, str):
                        licenses.append(l_item)

            repo_field = data.get("repository")
            if isinstance(repo_field, dict):
                repository = repo_field.get("url")
            elif isinstance(repo_field, str):
                repository = repo_field

            # npm artifact
            dist = data.get("dist", {})
            tarball_url = dist.get("tarball")
            filename = tarball_url.split("/")[-1] if tarball_url else f"{name}-{version}.tgz"
            digests: Dict[str, str] = {}
            if "shasum" in dist:
                digests["sha1"] = dist["shasum"].lower()
            if "sha256" in dist:
                digests["sha256"] = dist["sha256"].lower()
            if "integrity" in dist:
                integrity_str = dist["integrity"]
                if integrity_str.startswith("sha512-"):
                    # We preserve the standard hex/base64 representation
                    digests["sha512"] = integrity_str
                elif integrity_str.startswith("sha256-"):
                    digests["sha256"] = integrity_str

            artifacts.append({
                "artifact_id": filename,
                "artifact_type": "npm_tarball",
                "digests": digests,
                "url": tarball_url,
            })

        elif ecosystem == "pypi":
            # PyPI JSON API
            info = data.get("info", {})
            raw_lic = info.get("license")
            if raw_lic and raw_lic.strip():
                licenses.append(raw_lic.strip())
            classifiers = info.get("classifiers", [])
            for c in classifiers:
                if c.startswith("License ::"):
                    license_classifiers.append(c)

            proj_urls = info.get("project_urls") or {}
            repository = (
                proj_urls.get("Source")
                or proj_urls.get("Source Code")
                or proj_urls.get("Repository")
                or proj_urls.get("Code")
                or proj_urls.get("Homepage")
                or info.get("home_page")
            )

            releases = data.get("releases", {}).get(version, []) or data.get("urls", [])
            for rel in releases:
                fn = rel.get("filename")
                pkg_type = rel.get("packagetype", "unknown")
                upload_time = rel.get("upload_time_iso_8601") or rel.get("upload_time")
                if upload_time and not published_at:
                    published_at = upload_time

                digs: Dict[str, str] = {}
                d_obj = rel.get("digests", {})
                for algo in ["sha256", "md5", "blake2b_256"]:
                    if algo in d_obj and d_obj[algo]:
                        digs[algo] = d_obj[algo].lower()
                if "md5_digest" in rel and "md5" not in digs:
                    digs["md5"] = rel["md5_digest"].lower()

                artifacts.append({
                    "artifact_id": fn,
                    "artifact_type": pkg_type,
                    "digests": digs,
                    "url": rel.get("url"),
                    "upload_time": upload_time,
                })

        return {
            "source_id": src.get("source_id", "registry"),
            "role": role,
            "status": status,
            "endpoint": endpoint,
            "available": True,
            "published_at": published_at,
            "artifacts": artifacts,
            "licenses": licenses,
            "license_classifiers": license_classifiers,
            "repository": repository,
            "license_text_evidence": src.get("license_text_evidence") or data.get("license_text_evidence"),
            "derived_from": None,
        }

    def _normalize_deps_dev(
        self, ecosystem: str, name: str, version: str, src: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Normalize deps.dev API v3 response."""
        status = src.get("status", 0)
        data = src.get("data", {})
        endpoint = src.get("endpoint", "")
        derived_from = src.get("derived_from", "registry")
        subsequent_observation = src.get("subsequent_observation") or (data.get("subsequent_observation") if isinstance(data, dict) else None)

        if status != 200 or not isinstance(data, dict):
            return {
                "source_id": "deps_dev",
                "role": "derived_indexer",
                "status": status,
                "endpoint": endpoint,
                "available": False,
                "published_at": None,
                "licenses": [],
                "repository": None,
                "derived_from": derived_from,
                "subsequent_observation": subsequent_observation,
            }

        published_at = data.get("publishedAt")
        licenses = data.get("licenses", [])
        repository = None
        for link in data.get("links", []):
            if link.get("label") == "SOURCE_REPO":
                repository = link.get("url")
                break

        return {
            "source_id": "deps_dev",
            "role": "derived_indexer",
            "status": status,
            "endpoint": endpoint,
            "available": True,
            "published_at": published_at,
            "licenses": licenses,
            "repository": repository,
            "derived_from": derived_from,
            "subsequent_observation": subsequent_observation,
        }

    def _normalize_clearlydefined(
        self, name: str, version: str, src: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Normalize ClearlyDefined API response for supplemental license analysis."""
        status = src.get("status", 0)
        data = src.get("data", {})
        endpoint = src.get("endpoint", "")

        if status != 200 or not isinstance(data, dict):
            return {
                "source_id": "clearlydefined",
                "role": "supplemental_license_analyzer",
                "status": status,
                "endpoint": endpoint,
                "available": False,
                "declared_license": None,
                "discovered_licenses": [],
                "derived_from": None,
            }

        licensed_info = data.get("licensed", {})
        declared = licensed_info.get("declared")
        facets = licensed_info.get("facets", {}).get("core", {})
        discovered = facets.get("discovered", {}).get("expressions", [])

        return {
            "source_id": "clearlydefined",
            "role": "supplemental_license_analyzer",
            "status": status,
            "endpoint": endpoint,
            "available": True,
            "declared_license": declared,
            "discovered_licenses": discovered,
            "derived_from": None,
        }

    def _normalize_synthetic(self, src: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize synthetic fixture source."""
        artifacts = []
        for art in src.get("artifacts", []):
            artifacts.append({
                "artifact_id": art.get("artifact_id"),
                "artifact_type": art.get("artifact_type", "npm_tarball"),
                "digests": art.get("digests", {}),
                "url": art.get("url", src.get("endpoint")),
            })
        return {
            "source_id": src.get("source_id", "synthetic"),
            "role": "synthetic_mirror",
            "status": src.get("status", 200),
            "endpoint": src.get("endpoint", "synthetic://fixture"),
            "available": True,
            "published_at": src.get("published_at"),
            "artifacts": artifacts,
            "licenses": src.get("licenses", []),
            "derived_from": None,
        }

    def _build_dependency_relations(
        self, ecosystem: str, sources: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Record the provenance derivation DAG.
        deps.dev derives its package registry listings directly from upstream registry.
        Consistency between deps.dev and registry cannot be counted as independent truth validation.
        """
        relations = []
        if "deps_dev" in sources and "registry" in sources:
            upstream_id = "npm_registry" if ecosystem == "npm" else "pypi_json"
            relations.append({
                "subject": "deps_dev",
                "upstream": upstream_id,
                "nature": "Downstream ingestion of upstream registry metadata; consistency represents ingestion propagation, NOT independent ground-truth verification.",
                "independent_truth_valid": False,
            })
        return relations
