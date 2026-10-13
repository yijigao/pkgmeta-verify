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
Metadata Collector module.
Fetches package metadata across npm, PyPI, deps.dev, and ClearlyDefined.
Supports both live HTTP retrieval and offline reproducible snapshot loading.
"""

from datetime import datetime, timezone
import json
import os
import re
from typing import Any, Dict, Optional
import urllib.parse

import requests

USER_AGENT = "CodeSupply-PMV/0.1.0 (Joey Jigao Yi; NLnet Application)"
REQUEST_TIMEOUT = 10


def parse_purl(purl: str) -> Dict[str, str]:
    """Parse a package URL (PURL) into ecosystem, name, and version."""
    match = re.match(r"^pkg:(npm|pypi)/([^@]+)@([^?#]+)$", purl.strip())
    if not match:
        raise ValueError(f"Unsupported or malformed PURL format: {purl}")
    ecosystem, raw_name, version = match.groups()
    name = urllib.parse.unquote(raw_name)
    return {
        "purl": purl.strip(),
        "ecosystem": ecosystem,
        "name": name,
        "version": version.strip(),
    }


def purl_to_snapshot_filename(purl: str) -> str:
    """Derive deterministic filename for snapshot persistence."""
    parsed = parse_purl(purl)
    safe_name = parsed["name"].replace("/", "-").replace("@", "")
    return f"pkg-{parsed['ecosystem']}-{safe_name}-{parsed['version']}.json"


class Collector:
    """Collects raw package metadata from registries and indexers."""

    def __init__(self, offline_dir: Optional[str] = None):
        self.offline_dir = offline_dir
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    def collect(self, purl: str) -> Dict[str, Any]:
        """Collect raw metadata for a package from multiple comparison sources."""
        parsed = parse_purl(purl)
        ecosystem = parsed["ecosystem"]
        name = parsed["name"]
        version = parsed["version"]

        if self.offline_dir:
            return self._load_offline_snapshot(purl)

        fetch_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        if ecosystem == "npm":
            return self._collect_npm(name, version, purl, fetch_ts)
        elif ecosystem == "pypi":
            return self._collect_pypi(name, version, purl, fetch_ts)
        else:
            raise ValueError(f"Unsupported ecosystem: {ecosystem}")

    def _collect_npm(
        self, name: str, version: str, purl: str, fetch_ts: str
    ) -> Dict[str, Any]:
        """Fetch npm packument, deps.dev API v3, and ClearlyDefined API."""
        encoded_name = urllib.parse.quote(name, safe="")
        # npm registry packument
        reg_url = f"https://registry.npmjs.org/{encoded_name}/{version}"
        reg_resp = self._http_get(reg_url, timeout=6, retries=2)

        # deps.dev API v3
        deps_url = f"https://api.deps.dev/v3/systems/npm/packages/{encoded_name}/versions/{version}"
        deps_resp = self._http_get(deps_url, timeout=6, retries=2)

        # ClearlyDefined API (supplemental for license)
        if "/" in name:
            namespace, pkg_name = name.split("/", 1)
            namespace = namespace.lstrip("@")
        else:
            namespace = "-"
            pkg_name = name
        cd_url = f"https://api.clearlydefined.io/definitions/npm/npmjs/{namespace}/{pkg_name}/{version}"
        # ClearlyDefined is supplemental; short timeout, no retry
        cd_resp = self._http_get(cd_url, timeout=4, retries=1)

        return {
            "purl": purl,
            "ecosystem": "npm",
            "name": name,
            "version": version,
            "fetch_timestamp": fetch_ts,
            "synthetic": False,
            "sources": {
                "registry": {
                    "source_id": "npm_registry",
                    "role": "upstream_registry",
                    "endpoint": reg_url,
                    "status": reg_resp["status"],
                    "data": reg_resp["data"],
                    "derived_from": None,
                },
                "deps_dev": {
                    "source_id": "deps_dev",
                    "role": "derived_indexer",
                    "endpoint": deps_url,
                    "status": deps_resp["status"],
                    "data": deps_resp["data"],
                    "derived_from": "npm_registry",
                },
                "clearlydefined": {
                    "source_id": "clearlydefined",
                    "role": "supplemental_license_analyzer",
                    "endpoint": cd_url,
                    "status": cd_resp["status"],
                    "data": cd_resp["data"],
                    "derived_from": None,
                },
            },
        }

    def _collect_pypi(
        self, name: str, version: str, purl: str, fetch_ts: str
    ) -> Dict[str, Any]:
        """Fetch PyPI JSON API, deps.dev API v3, and ClearlyDefined API."""
        encoded_name = urllib.parse.quote(name, safe="")
        # PyPI JSON API (Note: PyPI JSON API and Simple Repository PEP 503/691 are dual interfaces of the same warehouse registry)
        reg_url = f"https://pypi.org/pypi/{encoded_name}/{version}/json"
        reg_resp = self._http_get(reg_url, timeout=6, retries=2)

        # deps.dev API v3
        deps_url = f"https://api.deps.dev/v3/systems/pypi/packages/{encoded_name}/versions/{version}"
        deps_resp = self._http_get(deps_url, timeout=6, retries=2)

        # ClearlyDefined API (supplemental for license)
        cd_url = f"https://api.clearlydefined.io/definitions/pypi/pypi/-/{encoded_name}/{version}"
        cd_resp = self._http_get(cd_url, timeout=4, retries=1)

        return {
            "purl": purl,
            "ecosystem": "pypi",
            "name": name,
            "version": version,
            "fetch_timestamp": fetch_ts,
            "synthetic": False,
            "sources": {
                "registry": {
                    "source_id": "pypi_json",
                    "role": "upstream_registry",
                    "endpoint": reg_url,
                    "status": reg_resp["status"],
                    "data": reg_resp["data"],
                    "derived_from": None,
                    "registry_interface_note": "PyPI JSON API shares warehouse backend with PEP 503/691 Simple repository",
                },
                "deps_dev": {
                    "source_id": "deps_dev",
                    "role": "derived_indexer",
                    "endpoint": deps_url,
                    "status": deps_resp["status"],
                    "data": deps_resp["data"],
                    "derived_from": "pypi_json",
                },
                "clearlydefined": {
                    "source_id": "clearlydefined",
                    "role": "supplemental_license_analyzer",
                    "endpoint": cd_url,
                    "status": cd_resp["status"],
                    "data": cd_resp["data"],
                    "derived_from": None,
                },
            },
        }

    def _http_get(
        self, url: str, timeout: int = 6, retries: int = 2
    ) -> Dict[str, Any]:
        """Execute HTTP GET with graceful retry and error encapsulation."""
        last_exc = None
        for attempt in range(retries):
            try:
                resp = self.session.get(url, timeout=timeout)
                status = resp.status_code
                if status == 200:
                    try:
                        data = resp.json()
                    except Exception:
                        data = {"raw_text": resp.text[:2000]}
                else:
                    data = {"error": f"HTTP status {status}", "body": resp.text[:500]}
                return {"status": status, "data": data}
            except Exception as exc:
                last_exc = exc
        return {"status": 0, "data": {"error": f"Network exception: {str(last_exc)}"}}

    def _load_offline_snapshot(self, purl: str) -> Dict[str, Any]:
        """Load deterministic raw metadata snapshot from offline directory."""
        filename = purl_to_snapshot_filename(purl)
        path = os.path.join(self.offline_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Offline snapshot not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
