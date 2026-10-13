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
Schema regression tests:
1. Validates that pmv-output.schema.json passes Draft 2020-12 self-check.
2. Validates that all evidence results pass schema validation.
3. Validates that invalid outputs (e.g. invalid category, missing required fields) are rejected.
"""

import glob
import json
import os
import unittest
import jsonschema
from jsonschema.validators import Draft202012Validator


class TestOutputSchema(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.schema_path = os.path.join(self.base_dir, "schemas", "pmv-output.schema.json")
        with open(self.schema_path, "r", encoding="utf-8") as f:
            self.schema = json.load(f)

    def test_schema_itself_is_valid_draft202012(self):
        """Schema itself must be valid standard JSON Schema Draft 2020-12 without exception."""
        Draft202012Validator.check_schema(self.schema)
        # Confirm lowercase types
        self.assertEqual(self.schema.get("type"), "object")
        # Confirm versioned project $id
        self.assertTrue(self.schema.get("$id", "").startswith("https://"))
        self.assertIn("/schemas/pmv-output.schema.json", self.schema.get("$id", ""))

    def test_all_baseline_results_validate_against_schema(self):
        """All result instances in evidence/results/ must validate cleanly against schema."""
        result_files = glob.glob(os.path.join(self.base_dir, "evidence", "results", "*.json"))
        self.assertGreaterEqual(len(result_files), 5, "Must have at least 5 baseline result files")
        for fpath in result_files:
            with open(fpath, "r", encoding="utf-8") as f:
                instance = json.load(f)
            jsonschema.validate(instance=instance, schema=self.schema)

    def test_schema_rejects_invalid_verdict_category(self):
        """Schema must reject an invalid verdict category."""
        sample_file = glob.glob(os.path.join(self.base_dir, "evidence", "results", "*.json"))[0]
        with open(sample_file, "r", encoding="utf-8") as f:
            invalid_instance = json.load(f)
        invalid_instance["verdict"]["category"] = "INVALID_CATEGORY_NAME"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_instance, schema=self.schema)

    def test_schema_rejects_missing_required_field(self):
        """Schema must reject output missing a required top-level field (e.g. purl)."""
        sample_file = glob.glob(os.path.join(self.base_dir, "evidence", "results", "*.json"))[0]
        with open(sample_file, "r", encoding="utf-8") as f:
            invalid_instance = json.load(f)
        del invalid_instance["purl"]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_instance, schema=self.schema)


if __name__ == "__main__":
    unittest.main()
