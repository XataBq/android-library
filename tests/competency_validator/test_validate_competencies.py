from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.validate_competencies import Code, main, validate_repository


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def source_data(source_id: str) -> dict:
    return {
        "id": source_id,
        "title": f"Invented {source_id}",
        "source_type": "personal-analysis",
        "language": "en",
        "source_version": 1,
        "status": "draft",
        "repository_usage": "owned",
        "provenance": {"citation": "Invented test source"},
    }


def items_data(source_id: str) -> dict:
    return {
        "source_id": source_id,
        "source_version": 1,
        "items": [
            {
                "id": "invented-item",
                "statement": "An invented statement for validator tests.",
                "locator": {"type": "section", "value": "Test section"},
            }
        ],
    }


class CompetencyValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        shutil.copytree(PROJECT_ROOT / "schemas", self.root / "schemas")
        shutil.copytree(PROJECT_ROOT / "templates", self.root / "templates")
        for directory in ("sources", "normalized", "reports"):
            (self.root / "competencies" / directory).mkdir(parents=True)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def add_package(
        self,
        source_id: str = "invented-source",
        directory_name: str | None = None,
        source: dict | None = None,
        items: dict | None = None,
    ) -> Path:
        package = self.root / "competencies" / "sources" / (directory_name or source_id)
        package.mkdir(parents=True)
        source = copy.deepcopy(source if source is not None else source_data(source_id))
        items = copy.deepcopy(items if items is not None else items_data(source_id))
        self.write_yaml(package / "source.yaml", source)
        self.write_yaml(package / "items.yaml", items)
        return package

    @staticmethod
    def write_yaml(path: Path, data: dict) -> None:
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def result_codes(self) -> set[str]:
        return {item.code for item in validate_repository(self.root).diagnostics}

    def assert_code(self, code: str) -> None:
        result = validate_repository(self.root)
        self.assertEqual(1, result.exit_code, [item.render() for item in result.diagnostics])
        self.assertIn(code, {item.code for item in result.diagnostics})

    def test_valid_source_package(self) -> None:
        self.add_package()
        result = validate_repository(self.root)
        self.assertEqual(0, result.exit_code, [item.render() for item in result.diagnostics])

    def test_valid_declared_artifact(self) -> None:
        package = self.add_package()
        artifact = package / "raw" / "invented.txt"
        artifact.parent.mkdir()
        content = b"invented fixture artifact\n"
        artifact.write_bytes(content)
        source = source_data("invented-source")
        source["artifacts"] = [
            {
                "path": "raw/invented.txt",
                "media_type": "text/plain",
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        ]
        self.write_yaml(package / "source.yaml", source)
        self.assertEqual(0, validate_repository(self.root).exit_code)

    def test_missing_source_yaml(self) -> None:
        package = self.add_package()
        (package / "source.yaml").unlink()
        self.assert_code(Code.MISSING_FILE)

    def test_missing_items_yaml(self) -> None:
        package = self.add_package()
        (package / "items.yaml").unlink()
        self.assert_code(Code.MISSING_FILE)

    def test_source_package_id_mismatch(self) -> None:
        self.add_package(directory_name="different-directory")
        self.assert_code(Code.PACKAGE_ID_MISMATCH)

    def test_source_id_mismatch_between_files(self) -> None:
        self.add_package(items=items_data("different-source"))
        self.assert_code(Code.SOURCE_ID_MISMATCH)

    def test_source_version_mismatch(self) -> None:
        items = items_data("invented-source")
        items["source_version"] = 2
        self.add_package(items=items)
        self.assert_code(Code.SOURCE_VERSION_MISMATCH)

    def test_duplicate_source_ids(self) -> None:
        self.add_package("shared-id", "first-package")
        self.add_package("shared-id", "second-package")
        self.assert_code(Code.DUPLICATE_SOURCE_ID)

    def test_duplicate_item_ids(self) -> None:
        items = items_data("invented-source")
        duplicate = copy.deepcopy(items["items"][0])
        duplicate["statement"] = "A second invented statement."
        items["items"].append(duplicate)
        self.add_package(items=items)
        self.assert_code(Code.DUPLICATE_ITEM_ID)

    def test_missing_item_locator(self) -> None:
        items = items_data("invented-source")
        del items["items"][0]["locator"]
        self.add_package(items=items)
        self.assert_code(Code.SCHEMA)

    def test_invalid_repository_usage(self) -> None:
        source = source_data("invented-source")
        source["repository_usage"] = "unrestricted"
        self.add_package(source=source)
        self.assert_code(Code.SCHEMA)

    def test_invalid_usage_fixture_wrong_reason_is_detected(self) -> None:
        fixture_path = (
            self.root
            / "schemas/fixtures/competencies/invalid/source-invalid-usage.yaml"
        )
        fixture = yaml.safe_load(fixture_path.read_text(encoding="utf-8"))
        fixture["repository_usage"] = "owned"
        del fixture["title"]
        self.write_yaml(fixture_path, fixture)
        self.assert_code(Code.FIXTURE_EXPECTATION)

    def test_missing_locator_fixture_wrong_reason_is_detected(self) -> None:
        fixture_path = (
            self.root
            / "schemas/fixtures/competencies/invalid/items-missing-locator.yaml"
        )
        fixture = yaml.safe_load(fixture_path.read_text(encoding="utf-8"))
        fixture["items"][0]["locator"] = {"type": "item", "value": "Fixture item"}
        fixture["source_version"] = 0
        self.write_yaml(fixture_path, fixture)
        self.assert_code(Code.FIXTURE_EXPECTATION)

    def test_duplicate_id_fixture_wrong_reason_is_detected(self) -> None:
        fixture_path = (
            self.root
            / "schemas/fixtures/competencies/invalid/items-duplicate-id.yaml"
        )
        fixture = yaml.safe_load(fixture_path.read_text(encoding="utf-8"))
        fixture["items"][1]["id"] = "different-item"
        del fixture["items"][1]["locator"]
        self.write_yaml(fixture_path, fixture)
        self.assert_code(Code.FIXTURE_EXPECTATION)

    def test_artifact_path_escaping_package(self) -> None:
        source = source_data("invented-source")
        source["artifacts"] = [
            {
                "path": "../outside.txt",
                "media_type": "text/plain",
                "sha256": "0" * 64,
            }
        ]
        self.add_package(source=source)
        self.assert_code(Code.ARTIFACT_PATH)

    def test_missing_artifact(self) -> None:
        source = source_data("invented-source")
        source["artifacts"] = [
            {
                "path": "raw/missing.txt",
                "media_type": "text/plain",
                "sha256": "0" * 64,
            }
        ]
        self.add_package(source=source)
        self.assert_code(Code.ARTIFACT_MISSING)

    def test_artifact_must_be_a_regular_file(self) -> None:
        package = self.add_package()
        (package / "raw" / "directory.txt").mkdir(parents=True)
        source = source_data("invented-source")
        source["artifacts"] = [
            {
                "path": "raw/directory.txt",
                "media_type": "text/plain",
                "sha256": "0" * 64,
            }
        ]
        self.write_yaml(package / "source.yaml", source)
        self.assert_code(Code.ARTIFACT_NOT_FILE)

    def test_sha256_mismatch(self) -> None:
        package = self.add_package()
        raw_file = package / "raw" / "invented.txt"
        raw_file.parent.mkdir()
        raw_file.write_text("invented", encoding="utf-8")
        source = source_data("invented-source")
        source["artifacts"] = [
            {
                "path": "raw/invented.txt",
                "media_type": "text/plain",
                "sha256": "0" * 64,
            }
        ]
        self.write_yaml(package / "source.yaml", source)
        self.assert_code(Code.ARTIFACT_HASH_MISMATCH)

    def test_undeclared_file_under_raw(self) -> None:
        package = self.add_package()
        raw_file = package / "raw" / "undeclared.txt"
        raw_file.parent.mkdir()
        raw_file.write_text("invented", encoding="utf-8")
        self.assert_code(Code.UNDECLARED_ARTIFACT)

    def test_artifacts_forbidden_for_citation_only(self) -> None:
        package = self.add_package()
        raw_file = package / "raw" / "excerpt.txt"
        raw_file.parent.mkdir()
        content = b"short invented excerpt"
        raw_file.write_bytes(content)
        source = source_data("invented-source")
        source["repository_usage"] = "citation-only"
        source["artifacts"] = [
            {
                "path": "raw/excerpt.txt",
                "media_type": "text/plain",
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        ]
        self.write_yaml(package / "source.yaml", source)
        self.assert_code(Code.CITATION_ONLY_ARTIFACT)

    def test_diagnostics_are_deterministic(self) -> None:
        self.add_package(directory_name="wrong-directory", items=items_data("other-source"))
        first = validate_repository(self.root).sorted_diagnostics()
        second = validate_repository(self.root).sorted_diagnostics()
        self.assertEqual(first, second)

    def test_cli_exit_code_zero(self) -> None:
        self.add_package()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, main(["--root", str(self.root)]))

    def test_cli_exit_code_one(self) -> None:
        package = self.add_package()
        (package / "items.yaml").unlink()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(1, main(["--root", str(self.root)]))
        self.assertNotIn("Traceback", output.getvalue())

    def test_cli_exit_code_two_for_invalid_configuration(self) -> None:
        schema_path = self.root / "schemas" / "competency-source.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema["type"] = "invalid-schema-type"
        schema_path.write_text(json.dumps(schema), encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(2, main(["--root", str(self.root)]))
        self.assertIn(Code.SCHEMA_LOAD, output.getvalue())
        self.assertNotIn("Traceback", output.getvalue())


if __name__ == "__main__":
    unittest.main()
