"""Validate repository educational content packages."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


class Code:
    SCHEMA_LOAD = "SCHEMA_LOAD"
    YAML_PARSE = "YAML_PARSE"
    SCHEMA = "SCHEMA"
    MISSING_FILE = "MISSING_FILE"
    TOPIC_TEST_ID_MISMATCH = "TOPIC_TEST_ID_MISMATCH"
    CONTENT_VERSION_MISMATCH = "CONTENT_VERSION_MISMATCH"
    DUPLICATE_TOPIC_ID = "DUPLICATE_TOPIC_ID"
    DUPLICATE_QUESTION_ID = "DUPLICATE_QUESTION_ID"
    DUPLICATE_OPTION_ID = "DUPLICATE_OPTION_ID"
    UNKNOWN_CORRECT_OPTION = "UNKNOWN_CORRECT_OPTION"
    RUBRIC_POINTS_MISMATCH = "RUBRIC_POINTS_MISMATCH"
    SELF_REFERENCE = "SELF_REFERENCE"
    UNKNOWN_TOPIC_REFERENCE = "UNKNOWN_TOPIC_REFERENCE"
    PATH_METADATA_MISMATCH = "PATH_METADATA_MISMATCH"
    DEPENDENCY_CYCLE = "DEPENDENCY_CYCLE"
    INTERNAL = "INTERNAL"


CANONICAL_FILES = (
    "topic.yaml",
    "theory.md",
    "cheat-sheet.md",
    "practice.md",
    "interview.md",
    "test.yaml",
)


@dataclass(frozen=True, order=True)
class Diagnostic:
    path: str
    code: str
    location: str
    message: str

    def render(self) -> str:
        location = f": {self.location}" if self.location else ""
        return f"ERROR [{self.code}] {self.path}{location}: {self.message}"


@dataclass
class Package:
    directory: Path
    relative_directory: str
    topic_path: Path
    test_path: Path
    topic: dict[str, Any] | None = None
    test: dict[str, Any] | None = None
    topic_schema_valid: bool = False
    test_schema_valid: bool = False


@dataclass
class ValidationResult:
    diagnostics: list[Diagnostic] = field(default_factory=list)
    package_count: int = 0
    template_count: int = 0
    fixture_count: int = 0
    configuration_error: bool = False
    verbose_messages: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.diagnostics

    @property
    def exit_code(self) -> int:
        if self.configuration_error:
            return 2
        return 0 if self.passed else 1

    def add(self, code: str, path: str, message: str, location: str = "") -> None:
        self.diagnostics.append(Diagnostic(path, code, location, message))

    def sorted_diagnostics(self) -> list[Diagnostic]:
        return sorted(set(self.diagnostics))


def _relative(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _property_path(parts: Iterable[Any]) -> str:
    result = ""
    for part in parts:
        if isinstance(part, int):
            result += f"[{part}]"
        else:
            result += ("." if result else "") + str(part)
    return result


def _load_schemas(
    root: Path, result: ValidationResult
) -> dict[str, Draft202012Validator] | None:
    validators: dict[str, Draft202012Validator] = {}
    for name in ("topic", "test"):
        path = root / "schemas" / f"{name}.schema.json"
        display_path = _relative(root, path)
        try:
            with path.open(encoding="utf-8") as file:
                schema = json.load(file)
            Draft202012Validator.check_schema(schema)
            validators[name] = Draft202012Validator(
                schema, format_checker=FormatChecker()
            )
        except (OSError, json.JSONDecodeError, SchemaError) as error:
            result.add(Code.SCHEMA_LOAD, display_path, str(error).splitlines()[0])
            result.configuration_error = True
    return validators if len(validators) == 2 else None


def _discover_packages(root: Path) -> list[Package]:
    content = root / "content"
    if not content.is_dir():
        return []
    packages: list[Package] = []
    for directory in sorted(path for path in content.rglob("*") if path.is_dir()):
        relative_parts = directory.relative_to(content).parts
        if len(relative_parts) != 3:
            continue
        if not ((directory / "topic.yaml").exists() or (directory / "test.yaml").exists()):
            continue
        packages.append(
            Package(
                directory=directory,
                relative_directory=_relative(root, directory),
                topic_path=directory / "topic.yaml",
                test_path=directory / "test.yaml",
            )
        )
    return packages


def _load_yaml(root: Path, path: Path, result: ValidationResult) -> dict[str, Any] | None:
    display_path = _relative(root, path)
    try:
        with path.open(encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except (OSError, yaml.YAMLError) as error:
        result.add(Code.YAML_PARSE, display_path, str(error).splitlines()[0])
        return None
    if not isinstance(data, dict):
        result.add(Code.YAML_PARSE, display_path, "YAML root must be a mapping")
        return None
    return data


def _schema_errors(
    validator: Draft202012Validator, data: Mapping[str, Any]
) -> list[Any]:
    return sorted(
        validator.iter_errors(data),
        key=lambda error: (
            tuple(str(part) for part in error.absolute_path),
            error.message,
        ),
    )


def _validate_schema_document(
    root: Path,
    path: Path,
    validator: Draft202012Validator,
    data: Mapping[str, Any],
    result: ValidationResult,
) -> bool:
    errors = _schema_errors(validator, data)
    display_path = _relative(root, path)
    for error in errors:
        result.add(
            Code.SCHEMA,
            display_path,
            error.message,
            _property_path(error.absolute_path),
        )
    return not errors


def _validate_support_files(
    root: Path,
    validators: Mapping[str, Draft202012Validator],
    result: ValidationResult,
) -> None:
    templates = (
        (root / "templates/topic/topic.yaml", validators["topic"]),
        (root / "templates/topic/test.yaml", validators["test"]),
    )
    result.template_count = len(templates)
    for path, validator in templates:
        if not path.is_file():
            result.add(Code.SCHEMA, _relative(root, path), "required template is missing")
            continue
        data = _load_yaml(root, path, result)
        if data is not None:
            _validate_schema_document(root, path, validator, data, result)

    fixtures = (
        (root / "schemas/fixtures/valid/topic.yaml", validators["topic"], True),
        (root / "schemas/fixtures/valid/test.yaml", validators["test"], True),
        (root / "schemas/fixtures/invalid/topic-invalid-id.yaml", validators["topic"], False),
        (root / "schemas/fixtures/invalid/test-missing-answer.yaml", validators["test"], False),
    )
    result.fixture_count = len(fixtures)
    for path, validator, expected_valid in fixtures:
        if not path.is_file():
            result.add(Code.SCHEMA, _relative(root, path), "required schema fixture is missing")
            continue
        data = _load_yaml(root, path, result)
        if data is None:
            continue
        errors = _schema_errors(validator, data)
        if expected_valid:
            _validate_schema_document(root, path, validator, data, result)
        elif not errors:
            result.add(
                Code.SCHEMA,
                _relative(root, path),
                "fixture expected to fail schema validation but passed",
            )


def _duplicates(values: Iterable[Any]) -> list[Any]:
    seen: set[Any] = set()
    duplicate_values: set[Any] = set()
    for value in values:
        try:
            if value in seen:
                duplicate_values.add(value)
            seen.add(value)
        except TypeError:
            continue
    return sorted(duplicate_values, key=str)


def _validate_package_local(root: Path, package: Package, result: ValidationResult) -> None:
    topic = package.topic
    test = package.test
    topic_path = _relative(root, package.topic_path)
    test_path = _relative(root, package.test_path)

    if topic is not None and test is not None:
        if topic.get("id") != test.get("topic_id"):
            result.add(
                Code.TOPIC_TEST_ID_MISMATCH,
                test_path,
                f"topic_id {test.get('topic_id')!r} does not match topic id {topic.get('id')!r}",
                "topic_id",
            )
        if topic.get("content_version") != test.get("content_version"):
            result.add(
                Code.CONTENT_VERSION_MISMATCH,
                test_path,
                "test content_version does not match topic content_version",
                "content_version",
            )

    if topic is not None:
        topic_id = topic.get("id")
        for field_name in ("prerequisites", "related_topics"):
            references = topic.get(field_name, [])
            if isinstance(references, list) and topic_id in references:
                result.add(
                    Code.SELF_REFERENCE,
                    topic_path,
                    f"topic {topic_id!r} must not reference itself",
                    field_name,
                )
        relative_parts = package.directory.relative_to(root / "content").parts
        expected = {
            "track": relative_parts[0],
            "section": relative_parts[1],
            "id": relative_parts[2],
        }
        for field_name, path_value in expected.items():
            if topic.get(field_name) != path_value:
                result.add(
                    Code.PATH_METADATA_MISMATCH,
                    topic_path,
                    f"metadata value {topic.get(field_name)!r} does not match path value {path_value!r}",
                    field_name,
                )

    if test is None:
        return
    questions = test.get("questions")
    if not isinstance(questions, list):
        return
    question_ids = [question.get("id") for question in questions if isinstance(question, dict)]
    for duplicate_id in _duplicates(question_ids):
        result.add(
            Code.DUPLICATE_QUESTION_ID,
            test_path,
            f"question id {duplicate_id!r} appears more than once",
            "questions",
        )
    for index, question in enumerate(questions):
        if not isinstance(question, dict):
            continue
        question_location = f"questions[{index}]"
        question_type = question.get("type")
        options = question.get("options")
        if question_type in ("single-choice", "multiple-choice") and isinstance(options, list):
            option_ids = [option.get("id") for option in options if isinstance(option, dict)]
            for duplicate_id in _duplicates(option_ids):
                result.add(
                    Code.DUPLICATE_OPTION_ID,
                    test_path,
                    f"option id {duplicate_id!r} appears more than once",
                    f"{question_location}.options",
                )
            available_ids = set(value for value in option_ids if isinstance(value, str))
            correct_ids: list[Any]
            if question_type == "single-choice":
                correct_ids = [question.get("correct_option_id")]
            else:
                raw_correct_ids = question.get("correct_option_ids", [])
                correct_ids = raw_correct_ids if isinstance(raw_correct_ids, list) else []
                for duplicate_id in _duplicates(correct_ids):
                    result.add(
                        Code.UNKNOWN_CORRECT_OPTION,
                        test_path,
                        f"correct option id {duplicate_id!r} is duplicated",
                        f"{question_location}.correct_option_ids",
                    )
            for correct_id in sorted(
                set(value for value in correct_ids if isinstance(value, str))
            ):
                if correct_id not in available_ids:
                    result.add(
                        Code.UNKNOWN_CORRECT_OPTION,
                        test_path,
                        f"correct option id {correct_id!r} does not reference a declared option",
                        question_location,
                    )
        if question_type in ("free-text", "code-analysis"):
            rubric = question.get("rubric")
            points = question.get("points")
            if isinstance(rubric, list) and isinstance(points, int):
                rubric_points = [
                    item.get("points") for item in rubric if isinstance(item, dict)
                ]
                if all(isinstance(value, int) for value in rubric_points):
                    total = sum(rubric_points)
                    if total != points:
                        result.add(
                            Code.RUBRIC_POINTS_MISMATCH,
                            test_path,
                            f"rubric points sum to {total}, expected {points}",
                            f"{question_location}.rubric",
                        )


def _validate_repository_wide(root: Path, packages: list[Package], result: ValidationResult) -> None:
    topics_by_id: dict[str, list[Package]] = {}
    for package in packages:
        if package.topic is None:
            continue
        topic_id = package.topic.get("id")
        if isinstance(topic_id, str):
            topics_by_id.setdefault(topic_id, []).append(package)

    for topic_id, matching_packages in sorted(topics_by_id.items()):
        if len(matching_packages) < 2:
            continue
        paths = sorted(_relative(root, package.topic_path) for package in matching_packages)
        result.add(
            Code.DUPLICATE_TOPIC_ID,
            paths[0],
            f"topic id {topic_id!r} appears in: {', '.join(paths)}",
        )

    known_ids = set(topics_by_id)
    for package in packages:
        if package.topic is None:
            continue
        topic_path = _relative(root, package.topic_path)
        for field_name in ("prerequisites", "related_topics"):
            references = package.topic.get(field_name, [])
            if not isinstance(references, list):
                continue
            for referenced_id in sorted(
                set(value for value in references if isinstance(value, str))
            ):
                if referenced_id not in known_ids:
                    result.add(
                        Code.UNKNOWN_TOPIC_REFERENCE,
                        topic_path,
                        f"topic id {referenced_id!r} does not exist",
                        field_name,
                    )

    graph: dict[str, list[str]] = {}
    for topic_id, matching_packages in sorted(topics_by_id.items()):
        topic = matching_packages[0].topic or {}
        prerequisites = topic.get("prerequisites", [])
        graph[topic_id] = sorted(
            value
            for value in prerequisites
            if isinstance(value, str) and value in known_ids
        ) if isinstance(prerequisites, list) else []
    _validate_cycles(graph, result)


def _validate_cycles(graph: Mapping[str, list[str]], result: ValidationResult) -> None:
    state: dict[str, int] = {node: 0 for node in graph}
    stack: list[str] = []
    reported: set[tuple[str, ...]] = set()

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for prerequisite in graph[node]:
            if state[prerequisite] == 0:
                visit(prerequisite)
            elif state[prerequisite] == 1:
                start = stack.index(prerequisite)
                cycle = tuple(stack[start:] + [prerequisite])
                core = cycle[:-1]
                rotations = [core[index:] + core[:index] for index in range(len(core))]
                canonical_core = min(rotations)
                canonical = canonical_core + (canonical_core[0],)
                if canonical not in reported:
                    reported.add(canonical)
                    result.add(
                        Code.DEPENDENCY_CYCLE,
                        "content",
                        " -> ".join(canonical),
                    )
        stack.pop()
        state[node] = 2

    for node in sorted(graph):
        if state[node] == 0:
            visit(node)


def validate_repository(root: Path, verbose: bool = False) -> ValidationResult:
    root = root.resolve()
    result = ValidationResult()
    validators = _load_schemas(root, result)
    if validators is None:
        return result

    if verbose:
        result.verbose_messages.append("Loaded and meta-validated Draft 2020-12 schemas.")
    _validate_support_files(root, validators, result)
    packages = _discover_packages(root)
    result.package_count = len(packages)
    if verbose:
        result.verbose_messages.append(f"Discovered {len(packages)} topic package(s).")

    for package in packages:
        for filename in CANONICAL_FILES:
            path = package.directory / filename
            if not path.is_file():
                result.add(
                    Code.MISSING_FILE,
                    package.relative_directory,
                    f"missing canonical file {filename!r}",
                )
        if package.topic_path.is_file():
            package.topic = _load_yaml(root, package.topic_path, result)
            if package.topic is not None:
                package.topic_schema_valid = _validate_schema_document(
                    root, package.topic_path, validators["topic"], package.topic, result
                )
        if package.test_path.is_file():
            package.test = _load_yaml(root, package.test_path, result)
            if package.test is not None:
                package.test_schema_valid = _validate_schema_document(
                    root, package.test_path, validators["test"], package.test, result
                )
        _validate_package_local(root, package, result)

    _validate_repository_wide(root, packages, result)
    return result


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the root containing this script)",
    )
    parser.add_argument("--verbose", action="store_true", help="print validation phases")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        result = validate_repository(args.root, verbose=args.verbose)
    except Exception as error:  # Controlled CLI boundary for unexpected failures.
        print(f"ERROR [{Code.INTERNAL}] {args.root}: {error}")
        return 2
    for message in result.verbose_messages:
        print(f"INFO {message}")
    diagnostics = result.sorted_diagnostics()
    for diagnostic in diagnostics:
        print(diagnostic.render())
    if result.passed:
        print(
            "Content validation passed: "
            f"{result.package_count} topic packages, "
            f"{result.template_count} templates, {result.fixture_count} schema fixtures."
        )
    else:
        print(
            "Content validation failed: "
            f"{len(diagnostics)} errors across {result.package_count} topic packages."
        )
    return result.exit_code


if __name__ == "__main__":
    sys.exit(main())
