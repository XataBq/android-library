from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from scripts.validate_competencies import Code, ValidationResult, validate_repository


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class LearningSequenceValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        shutil.copytree(PROJECT_ROOT / "schemas", self.root / "schemas")
        shutil.copytree(PROJECT_ROOT / "templates", self.root / "templates")
        for directory in ("sources", "normalized", "reports"):
            (self.root / "competencies" / directory).mkdir(parents=True)
        (self.root / "learning-sequences").mkdir()
        self.add_source_package()
        self.add_canonical_package()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    @staticmethod
    def write_yaml(path: Path, data: dict) -> None:
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
                        "statement": "An invented statement for sequence tests.",
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
                "description": "Canonical competencies for sequence tests.",
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

    def fixture_data(self, category: str, filename: str) -> dict:
        path = self.root / "schemas/fixtures/learning-sequences" / category / filename
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def add_sequence(self, data: dict, directory_name: str | None = None) -> Path:
        sequence_id = data.get("sequence_id", "missing-sequence-id")
        package = self.root / "learning-sequences" / (directory_name or sequence_id)
        package.mkdir(parents=True)
        self.write_yaml(package / "sequence.yaml", data)
        return package

    def codes(self) -> set[str]:
        return {item.code for item in validate_repository(self.root).diagnostics}

    def test_schema_is_valid_draft_2020_12(self) -> None:
        schema = json.loads(
            (self.root / "schemas/learning-sequence.schema.json").read_text(
                encoding="utf-8"
            )
        )
        Draft202012Validator.check_schema(schema)

    def test_minimal_fixture_is_valid(self) -> None:
        self.add_sequence(self.fixture_data("valid", "minimal.yaml"))
        result = validate_repository(self.root)
        self.assertEqual(0, result.exit_code, [item.render() for item in result.diagnostics])
        self.assertEqual(1, result.sequence_package_count)

    def test_optional_description_rationale_and_notes_are_valid(self) -> None:
        self.add_sequence(self.fixture_data("valid", "multi-stage.yaml"))
        self.assertEqual(0, validate_repository(self.root).exit_code)

    def test_schema_invalid_fixtures_are_rejected(self) -> None:
        filenames = (
            "missing-required-field.yaml",
            "unsupported-schema-version.yaml",
            "empty-stages.yaml",
            "empty-stage-competencies.yaml",
            "duplicate-competency-within-stage.yaml",
            "unexpected-property.yaml",
        )
        for filename in filenames:
            with self.subTest(filename=filename):
                sequences_root = self.root / "learning-sequences"
                for package in sequences_root.iterdir():
                    shutil.rmtree(package)
                self.add_sequence(self.fixture_data("invalid", filename))
                self.assertIn(Code.SCHEMA, self.codes())

    def test_empty_stages_have_semantic_diagnostic(self) -> None:
        self.add_sequence(self.fixture_data("invalid", "empty-stages.yaml"))
        self.assertIn(Code.EMPTY_SEQUENCE_STAGES, self.codes())

    def test_empty_stage_competencies_have_semantic_diagnostic(self) -> None:
        self.add_sequence(
            self.fixture_data("invalid", "empty-stage-competencies.yaml")
        )
        self.assertIn(Code.EMPTY_STAGE_COMPETENCIES, self.codes())

    def test_duplicate_stage_id_is_rejected(self) -> None:
        self.add_sequence(self.fixture_data("invalid", "duplicate-stage-id.yaml"))
        self.assertIn(Code.DUPLICATE_STAGE_ID, self.codes())

    def test_duplicate_competency_across_duplicate_stage_ids_is_rejected(self) -> None:
        data = self.fixture_data("invalid", "duplicate-stage-id.yaml")
        data["stages"][1]["competencies"] = ["explain-fixture-boundary"]
        self.add_sequence(data)
        codes = self.codes()
        self.assertIn(Code.DUPLICATE_STAGE_ID, codes)
        self.assertIn(Code.DUPLICATE_SEQUENCE_COMPETENCY, codes)

    def test_duplicate_competency_within_stage_is_rejected(self) -> None:
        self.add_sequence(
            self.fixture_data("invalid", "duplicate-competency-within-stage.yaml")
        )
        self.assertIn(Code.DUPLICATE_STAGE_COMPETENCY, self.codes())

    def test_duplicate_competency_across_stages_is_rejected(self) -> None:
        self.add_sequence(
            self.fixture_data("invalid", "duplicate-competency-across-stages.yaml")
        )
        self.assertIn(Code.DUPLICATE_SEQUENCE_COMPETENCY, self.codes())

    def test_unknown_competency_set_is_rejected(self) -> None:
        self.add_sequence(
            self.fixture_data("invalid", "unknown-competency-set.yaml")
        )
        self.assertIn(Code.SEQUENCE_COMPETENCY_SET_MISSING, self.codes())

    def test_wrong_competency_set_version_is_rejected(self) -> None:
        self.add_sequence(
            self.fixture_data("invalid", "wrong-competency-set-version.yaml")
        )
        self.assertIn(Code.SEQUENCE_COMPETENCY_SET_VERSION_MISMATCH, self.codes())

    def test_unknown_competency_is_rejected(self) -> None:
        self.add_sequence(self.fixture_data("invalid", "unknown-competency.yaml"))
        self.assertIn(Code.SEQUENCE_COMPETENCY_MISSING, self.codes())

    def test_semantic_fixture_wrong_reason_is_detected(self) -> None:
        path = (
            self.root
            / "schemas/fixtures/learning-sequences/invalid/unknown-competency.yaml"
        )
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["stages"][0]["competencies"] = ["explain-fixture-boundary"]
        self.write_yaml(path, data)
        self.assertIn(Code.FIXTURE_EXPECTATION, self.codes())

    def test_package_directory_must_match_sequence_id(self) -> None:
        self.add_sequence(
            self.fixture_data("valid", "minimal.yaml"),
            directory_name="different-directory",
        )
        self.assertIn(Code.SEQUENCE_PACKAGE_ID_MISMATCH, self.codes())

    def test_duplicate_sequence_id_and_version_are_rejected(self) -> None:
        data = self.fixture_data("valid", "minimal.yaml")
        self.add_sequence(data, "first-directory")
        self.add_sequence(data, "second-directory")
        self.assertIn(Code.DUPLICATE_SEQUENCE_VERSION, self.codes())

    def test_missing_sequence_file_is_rejected(self) -> None:
        (self.root / "learning-sequences/missing-package").mkdir()
        self.assertIn(Code.MISSING_FILE, self.codes())

    def test_malformed_sequence_yaml_is_rejected(self) -> None:
        package = self.root / "learning-sequences/malformed-sequence"
        package.mkdir()
        (package / "sequence.yaml").write_text(
            "stages: [unterminated\n", encoding="utf-8"
        )
        self.assertIn(Code.YAML_PARSE, self.codes())

    def test_sequence_with_list_root_returns_schema_diagnostic(self) -> None:
        package = self.root / "learning-sequences/list-root"
        package.mkdir()
        (package / "sequence.yaml").write_text("[]\n", encoding="utf-8")
        result = validate_repository(self.root)
        self.assertIsInstance(result, ValidationResult)
        self.assertIn(Code.SCHEMA, {item.code for item in result.diagnostics})

    def test_sequence_with_scalar_root_returns_schema_diagnostic(self) -> None:
        package = self.root / "learning-sequences/scalar-root"
        package.mkdir()
        (package / "sequence.yaml").write_text(
            "not-a-mapping\n", encoding="utf-8"
        )
        result = validate_repository(self.root)
        self.assertIsInstance(result, ValidationResult)
        self.assertIn(Code.SCHEMA, {item.code for item in result.diagnostics})

    def test_diagnostics_are_deterministic(self) -> None:
        self.add_sequence(self.fixture_data("invalid", "duplicate-stage-id.yaml"))
        first = validate_repository(self.root).sorted_diagnostics()
        second = validate_repository(self.root).sorted_diagnostics()
        self.assertEqual(first, second)

    def test_real_sequence_and_repository_validate(self) -> None:
        result = validate_repository(PROJECT_ROOT)
        self.assertEqual(0, result.exit_code, [item.render() for item in result.diagnostics])
        self.assertEqual(1, result.sequence_package_count)


if __name__ == "__main__":
    unittest.main()
