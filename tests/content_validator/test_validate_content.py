from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.validate_content import Code, validate_repository


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def topic_data(topic_id: str, section: str = "basics") -> dict:
    return {
        "id": topic_id,
        "title": f"Synthetic {topic_id}",
        "track": "tools",
        "section": section,
        "difficulty": "foundation",
        "status": "draft",
        "estimated_minutes": 5,
        "content_version": 1,
        "prerequisites": [],
        "learning_outcomes": ["Validate synthetic content."],
        "tags": [],
        "references": [
            {
                "title": "JSON Schema",
                "url": "https://json-schema.org/",
                "type": "official-docs",
            }
        ],
    }


def test_data(topic_id: str) -> dict:
    return {
        "topic_id": topic_id,
        "content_version": 1,
        "passing_score_percent": 70,
        "questions": [
            {
                "id": "synthetic-question",
                "type": "single-choice",
                "prompt": "Choose the expected option.",
                "difficulty": "foundation",
                "points": 1,
                "explanation": "The expected option is declared.",
                "options": [
                    {"id": "expected", "text": "Expected"},
                    {"id": "alternate", "text": "Alternate"},
                ],
                "correct_option_id": "expected",
            }
        ],
    }


class ContentValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        shutil.copytree(PROJECT_ROOT / "schemas", self.root / "schemas")
        shutil.copytree(PROJECT_ROOT / "templates", self.root / "templates")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def add_package(
        self,
        topic_id: str = "synthetic-topic",
        section: str = "basics",
        topic: dict | None = None,
        test: dict | None = None,
    ) -> Path:
        package = self.root / "content" / "tools" / section / topic_id
        package.mkdir(parents=True)
        topic = copy.deepcopy(topic if topic is not None else topic_data(topic_id, section))
        test = copy.deepcopy(test if test is not None else test_data(topic_id))
        (package / "topic.yaml").write_text(yaml.safe_dump(topic, sort_keys=False), encoding="utf-8")
        (package / "test.yaml").write_text(yaml.safe_dump(test, sort_keys=False), encoding="utf-8")
        for filename in ("theory.md", "cheat-sheet.md", "practice.md", "interview.md"):
            (package / filename).write_text("# Synthetic\n", encoding="utf-8")
        return package

    def assert_code(self, code: str) -> None:
        result = validate_repository(self.root)
        self.assertNotEqual(0, result.exit_code)
        self.assertIn(code, {diagnostic.code for diagnostic in result.diagnostics})

    def test_valid_repository_passes(self) -> None:
        self.add_package()
        result = validate_repository(self.root)
        self.assertEqual(0, result.exit_code, [item.render() for item in result.diagnostics])

    def test_duplicate_topic_ids_fail(self) -> None:
        self.add_package("duplicate-topic", "first")
        self.add_package("duplicate-topic", "second")
        self.assert_code(Code.DUPLICATE_TOPIC_ID)

    def test_missing_canonical_package_file_fails(self) -> None:
        package = self.add_package()
        (package / "theory.md").unlink()
        self.assert_code(Code.MISSING_FILE)

    def test_topic_test_id_mismatch_fails(self) -> None:
        test = test_data("different-topic")
        self.add_package(test=test)
        self.assert_code(Code.TOPIC_TEST_ID_MISMATCH)

    def test_content_version_mismatch_fails(self) -> None:
        test = test_data("synthetic-topic")
        test["content_version"] = 2
        self.add_package(test=test)
        self.assert_code(Code.CONTENT_VERSION_MISMATCH)

    def test_duplicate_question_ids_fail(self) -> None:
        test = test_data("synthetic-topic")
        test["questions"].append(copy.deepcopy(test["questions"][0]))
        self.add_package(test=test)
        self.assert_code(Code.DUPLICATE_QUESTION_ID)

    def test_duplicate_option_ids_fail(self) -> None:
        test = test_data("synthetic-topic")
        test["questions"][0]["options"][1]["id"] = "expected"
        self.add_package(test=test)
        self.assert_code(Code.DUPLICATE_OPTION_ID)

    def test_unknown_correct_option_fails(self) -> None:
        test = test_data("synthetic-topic")
        test["questions"][0]["correct_option_id"] = "unknown"
        self.add_package(test=test)
        self.assert_code(Code.UNKNOWN_CORRECT_OPTION)

    def test_rubric_point_mismatch_fails(self) -> None:
        test = test_data("synthetic-topic")
        test["questions"] = [
            {
                "id": "written-answer",
                "type": "free-text",
                "prompt": "Explain the synthetic case.",
                "difficulty": "foundation",
                "points": 2,
                "explanation": "The rubric defines the score.",
                "rubric": [{"criterion": "Explains it.", "points": 1}],
            }
        ]
        self.add_package(test=test)
        self.assert_code(Code.RUBRIC_POINTS_MISMATCH)

    def test_unknown_prerequisite_fails(self) -> None:
        topic = topic_data("synthetic-topic")
        topic["prerequisites"] = ["missing-topic"]
        self.add_package(topic=topic)
        self.assert_code(Code.UNKNOWN_TOPIC_REFERENCE)

    def test_self_prerequisite_fails(self) -> None:
        topic = topic_data("synthetic-topic")
        topic["prerequisites"] = ["synthetic-topic"]
        self.add_package(topic=topic)
        self.assert_code(Code.SELF_REFERENCE)

    def test_prerequisite_cycle_fails_deterministically(self) -> None:
        first = topic_data("first-topic")
        first["prerequisites"] = ["second-topic"]
        second = topic_data("second-topic")
        second["prerequisites"] = ["first-topic"]
        self.add_package("first-topic", topic=first, test=test_data("first-topic"))
        self.add_package("second-topic", topic=second, test=test_data("second-topic"))
        first_result = validate_repository(self.root)
        second_result = validate_repository(self.root)
        self.assertIn(Code.DEPENDENCY_CYCLE, {item.code for item in first_result.diagnostics})
        self.assertEqual(first_result.sorted_diagnostics(), second_result.sorted_diagnostics())

    def test_path_metadata_mismatch_fails(self) -> None:
        topic = topic_data("synthetic-topic")
        topic["track"] = "java"
        self.add_package(topic=topic)
        self.assert_code(Code.PATH_METADATA_MISMATCH)

    def test_malformed_yaml_fails_without_crashing(self) -> None:
        package = self.add_package()
        (package / "topic.yaml").write_text("id: [unterminated\n", encoding="utf-8")
        self.assert_code(Code.YAML_PARSE)

    def test_invalid_schema_content_is_controlled_configuration_failure(self) -> None:
        schema_path = self.root / "schemas" / "topic.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema["type"] = "not-a-json-schema-type"
        schema_path.write_text(json.dumps(schema), encoding="utf-8")
        result = validate_repository(self.root)
        self.assertEqual(2, result.exit_code)
        self.assertIn(Code.SCHEMA_LOAD, {item.code for item in result.diagnostics})


if __name__ == "__main__":
    unittest.main()
