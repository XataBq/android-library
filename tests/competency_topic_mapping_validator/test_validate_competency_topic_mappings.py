from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from scripts.validate_competencies import Code, ValidationResult, validate_repository


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class CompetencyTopicMappingValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        shutil.copytree(PROJECT_ROOT / "schemas", self.root / "schemas")
        shutil.copytree(PROJECT_ROOT / "templates", self.root / "templates")
        for directory in ("sources", "normalized", "reports"):
            (self.root / "competencies" / directory).mkdir(parents=True)
        (self.root / "learning-sequences").mkdir()
        (self.root / "competency-topic-mappings").mkdir()
        self.add_source_package()
        self.add_canonical_package()
        self.add_topic("fixture-primary-topic", 1)
        self.add_topic("fixture-secondary-topic", 2)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    @staticmethod
    def write_yaml(path: Path, data: Any) -> None:
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def add_source_package(self) -> None:
        package = self.root / "competencies/sources/fixture-source"
        package.mkdir(parents=True)
        self.write_yaml(
            package / "source.yaml",
            {
                "id": "fixture-source",
                "title": "Fixture source",
                "source_type": "personal-analysis",
                "language": "en",
                "source_version": 1,
                "status": "draft",
                "repository_usage": "owned",
                "provenance": {"citation": "Invented fixture source"},
            },
        )
        self.write_yaml(
            package / "items.yaml",
            {
                "source_id": "fixture-source",
                "source_version": 1,
                "items": [
                    {
                        "id": "fixture-item",
                        "statement": "An invented statement for mapping tests.",
                        "locator": {"type": "section", "value": "Fixture"},
                    }
                ],
            },
        )

    def add_canonical_package(self) -> None:
        package = self.root / "competencies/normalized/fixture-competency-set"
        package.mkdir(parents=True)
        self.write_yaml(
            package / "competency-set.yaml",
            {
                "schema_version": 1,
                "id": "fixture-competency-set",
                "title": "Fixture competency set",
                "description": "Canonical competencies for mapping tests.",
                "language": "en",
                "version": 1,
                "status": "review",
            },
        )
        evidence = [
            {
                "source_id": "fixture-source",
                "source_version": 1,
                "item_ids": ["fixture-item"],
            }
        ]
        self.write_yaml(
            package / "competencies.yaml",
            {
                "schema_version": 1,
                "competency_set_id": "fixture-competency-set",
                "competency_set_version": 1,
                "competencies": [
                    {
                        "id": "explain-fixture-boundary",
                        "title": "Explain a fixture boundary",
                        "outcome": "Explain the invented fixture boundary.",
                        "evidence": evidence,
                    },
                    {
                        "id": "apply-fixture-boundary",
                        "title": "Apply a fixture boundary",
                        "outcome": "Apply the invented fixture boundary.",
                        "evidence": evidence,
                    },
                ],
            },
        )

    def add_topic(self, topic_id: str, content_version: int) -> None:
        package = self.root / "content/tools/fixtures" / topic_id
        package.mkdir(parents=True)
        self.write_yaml(
            package / "topic.yaml",
            {"id": topic_id, "content_version": content_version},
        )

    def fixture_data(self, category: str, filename: str) -> Any:
        path = (
            self.root
            / "schemas/fixtures/competency-topic-mappings"
            / category
            / filename
        )
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def add_mapping(self, data: dict[str, Any], directory_name: str | None = None) -> Path:
        mapping_id = data.get("mapping_id", "missing-mapping-id")
        package = self.root / "competency-topic-mappings" / (
            directory_name or mapping_id
        )
        package.mkdir(parents=True)
        self.write_yaml(package / "mapping.yaml", data)
        return package

    def codes(self) -> set[str]:
        return {item.code for item in validate_repository(self.root).diagnostics}

    def test_schema_is_valid_draft_2020_12(self) -> None:
        schema = json.loads(
            (self.root / "schemas/competency-topic-mapping.schema.json").read_text(
                encoding="utf-8"
            )
        )
        Draft202012Validator.check_schema(schema)

    def test_minimal_fixture_is_valid(self) -> None:
        self.add_mapping(self.fixture_data("valid", "minimal.yaml"))
        result = validate_repository(self.root)
        self.assertEqual(0, result.exit_code, [item.render() for item in result.diagnostics])
        self.assertEqual(1, result.mapping_package_count)

    def test_many_to_many_fixture_and_both_coverage_values_are_valid(self) -> None:
        self.add_mapping(self.fixture_data("valid", "many-to-many.yaml"))
        self.assertEqual(0, validate_repository(self.root).exit_code)

    def test_schema_invalid_fixtures_are_rejected(self) -> None:
        filenames = (
            "missing-required-field.yaml",
            "unsupported-schema-version.yaml",
            "invalid-coverage.yaml",
            "unexpected-property.yaml",
        )
        for filename in filenames:
            with self.subTest(filename=filename):
                for package in (self.root / "competency-topic-mappings").iterdir():
                    shutil.rmtree(package)
                self.add_mapping(self.fixture_data("invalid", filename))
                self.assertIn(Code.SCHEMA, self.codes())

    def test_duplicate_competency_entry_is_rejected(self) -> None:
        self.add_mapping(self.fixture_data("invalid", "duplicate-competency-entry.yaml"))
        self.assertIn(Code.DUPLICATE_MAPPING_COMPETENCY, self.codes())

    def test_duplicate_topic_reference_is_rejected(self) -> None:
        self.add_mapping(self.fixture_data("invalid", "duplicate-topic-reference.yaml"))
        codes = self.codes()
        self.assertIn(Code.DUPLICATE_MAPPING_TOPIC_REFERENCE, codes)
        self.assertIn(Code.DUPLICATE_COMPETENCY_TOPIC_PAIR, codes)

    def test_duplicate_competency_topic_pair_is_rejected(self) -> None:
        self.add_mapping(
            self.fixture_data("invalid", "duplicate-competency-topic-pair.yaml")
        )
        self.assertIn(Code.DUPLICATE_COMPETENCY_TOPIC_PAIR, self.codes())

    def test_unknown_competency_set_is_rejected(self) -> None:
        self.add_mapping(self.fixture_data("invalid", "unknown-competency-set.yaml"))
        self.assertIn(Code.MAPPING_COMPETENCY_SET_MISSING, self.codes())

    def test_wrong_competency_set_version_is_rejected(self) -> None:
        self.add_mapping(
            self.fixture_data("invalid", "wrong-competency-set-version.yaml")
        )
        self.assertIn(Code.MAPPING_COMPETENCY_SET_VERSION_MISMATCH, self.codes())

    def test_unknown_competency_is_rejected(self) -> None:
        self.add_mapping(self.fixture_data("invalid", "unknown-competency.yaml"))
        self.assertIn(Code.MAPPING_COMPETENCY_MISSING, self.codes())

    def test_unknown_topic_is_rejected(self) -> None:
        self.add_mapping(self.fixture_data("invalid", "unknown-topic.yaml"))
        self.assertIn(Code.MAPPING_TOPIC_MISSING, self.codes())

    def test_wrong_topic_content_version_is_rejected(self) -> None:
        self.add_mapping(
            self.fixture_data("invalid", "wrong-topic-content-version.yaml")
        )
        self.assertIn(Code.MAPPING_TOPIC_VERSION_MISMATCH, self.codes())

    def test_duplicate_mapping_identity_is_rejected(self) -> None:
        data = self.fixture_data("valid", "minimal.yaml")
        self.add_mapping(data, "first-package")
        self.add_mapping(data, "second-package")
        self.assertIn(Code.DUPLICATE_MAPPING_VERSION, self.codes())

    def test_missing_mapping_file_is_rejected(self) -> None:
        (self.root / "competency-topic-mappings/missing-package").mkdir()
        self.assertIn(Code.MISSING_FILE, self.codes())

    def test_malformed_yaml_is_rejected(self) -> None:
        package = self.root / "competency-topic-mappings/malformed-yaml"
        package.mkdir()
        (package / "mapping.yaml").write_text(
            "mappings: [unterminated\n", encoding="utf-8"
        )
        self.assertIn(Code.YAML_PARSE, self.codes())

    def test_list_root_returns_schema_diagnostic_without_crashing(self) -> None:
        package = self.root / "competency-topic-mappings/list-root"
        package.mkdir()
        (package / "mapping.yaml").write_text("[]\n", encoding="utf-8")
        result = validate_repository(self.root)
        self.assertIsInstance(result, ValidationResult)
        self.assertIn(Code.SCHEMA, {item.code for item in result.diagnostics})

    def test_scalar_root_returns_schema_diagnostic_without_crashing(self) -> None:
        package = self.root / "competency-topic-mappings/scalar-root"
        package.mkdir()
        (package / "mapping.yaml").write_text("not-a-mapping\n", encoding="utf-8")
        result = validate_repository(self.root)
        self.assertIsInstance(result, ValidationResult)
        self.assertIn(Code.SCHEMA, {item.code for item in result.diagnostics})

    def test_topic_with_list_root_returns_diagnostics_without_crashing(self) -> None:
        self.add_mapping(self.fixture_data("valid", "minimal.yaml"))
        topic_path = (
            self.root
            / "content/tools/fixtures/fixture-primary-topic/topic.yaml"
        )
        topic_path.write_text("[]\n", encoding="utf-8")
        result = validate_repository(self.root)
        self.assertIsInstance(result, ValidationResult)
        self.assertIn(Code.YAML_PARSE, {item.code for item in result.diagnostics})

    def test_topic_with_scalar_root_returns_diagnostics_without_crashing(self) -> None:
        self.add_mapping(self.fixture_data("valid", "minimal.yaml"))
        topic_path = (
            self.root
            / "content/tools/fixtures/fixture-primary-topic/topic.yaml"
        )
        topic_path.write_text("not-a-mapping\n", encoding="utf-8")
        result = validate_repository(self.root)
        self.assertIsInstance(result, ValidationResult)
        self.assertIn(Code.YAML_PARSE, {item.code for item in result.diagnostics})

    def test_diagnostics_are_deterministic(self) -> None:
        self.add_mapping(self.fixture_data("invalid", "duplicate-topic-reference.yaml"))
        first = validate_repository(self.root).sorted_diagnostics()
        second = validate_repository(self.root).sorted_diagnostics()
        self.assertEqual(first, second)

    def test_repository_without_production_mappings_remains_valid(self) -> None:
        result = validate_repository(PROJECT_ROOT)
        self.assertEqual(0, result.exit_code, [item.render() for item in result.diagnostics])
        self.assertEqual(0, result.mapping_package_count)


if __name__ == "__main__":
    unittest.main()
