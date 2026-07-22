"""Validate repository competency and learning-sequence packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


class Code:
    SCHEMA_LOAD = "SCHEMA_LOAD"
    YAML_PARSE = "YAML_PARSE"
    SCHEMA = "SCHEMA"
    FIXTURE_EXPECTATION = "FIXTURE_EXPECTATION"
    MISSING_FILE = "MISSING_FILE"
    PACKAGE_ID_MISMATCH = "PACKAGE_ID_MISMATCH"
    SOURCE_ID_MISMATCH = "SOURCE_ID_MISMATCH"
    SOURCE_VERSION_MISMATCH = "SOURCE_VERSION_MISMATCH"
    DUPLICATE_SOURCE_ID = "DUPLICATE_SOURCE_ID"
    DUPLICATE_ITEM_ID = "DUPLICATE_ITEM_ID"
    DUPLICATE_ARTIFACT_PATH = "DUPLICATE_ARTIFACT_PATH"
    ARTIFACT_PATH = "ARTIFACT_PATH"
    ARTIFACT_MISSING = "ARTIFACT_MISSING"
    ARTIFACT_NOT_FILE = "ARTIFACT_NOT_FILE"
    ARTIFACT_HASH_MISMATCH = "ARTIFACT_HASH_MISMATCH"
    UNDECLARED_ARTIFACT = "UNDECLARED_ARTIFACT"
    CITATION_ONLY_ARTIFACT = "CITATION_ONLY_ARTIFACT"
    CANONICAL_PACKAGE_ID_MISMATCH = "CANONICAL_PACKAGE_ID_MISMATCH"
    DUPLICATE_COMPETENCY_SET_ID = "DUPLICATE_COMPETENCY_SET_ID"
    COMPETENCY_SET_ID_MISMATCH = "COMPETENCY_SET_ID_MISMATCH"
    COMPETENCY_SET_VERSION_MISMATCH = "COMPETENCY_SET_VERSION_MISMATCH"
    DUPLICATE_CANONICAL_ID = "DUPLICATE_CANONICAL_ID"
    EVIDENCE_SOURCE_MISSING = "EVIDENCE_SOURCE_MISSING"
    EVIDENCE_SOURCE_VERSION_MISMATCH = "EVIDENCE_SOURCE_VERSION_MISMATCH"
    EVIDENCE_ITEM_MISSING = "EVIDENCE_ITEM_MISSING"
    DUPLICATE_EVIDENCE_ITEM = "DUPLICATE_EVIDENCE_ITEM"
    DUPLICATE_EVIDENCE_ENTRY = "DUPLICATE_EVIDENCE_ENTRY"
    SEQUENCE_PACKAGE_ID_MISMATCH = "SEQUENCE_PACKAGE_ID_MISMATCH"
    DUPLICATE_SEQUENCE_VERSION = "DUPLICATE_SEQUENCE_VERSION"
    SEQUENCE_COMPETENCY_SET_MISSING = "SEQUENCE_COMPETENCY_SET_MISSING"
    SEQUENCE_COMPETENCY_SET_VERSION_MISMATCH = (
        "SEQUENCE_COMPETENCY_SET_VERSION_MISMATCH"
    )
    SEQUENCE_COMPETENCY_MISSING = "SEQUENCE_COMPETENCY_MISSING"
    DUPLICATE_STAGE_ID = "DUPLICATE_STAGE_ID"
    DUPLICATE_STAGE_COMPETENCY = "DUPLICATE_STAGE_COMPETENCY"
    DUPLICATE_SEQUENCE_COMPETENCY = "DUPLICATE_SEQUENCE_COMPETENCY"
    EMPTY_SEQUENCE_STAGES = "EMPTY_SEQUENCE_STAGES"
    EMPTY_STAGE_COMPETENCIES = "EMPTY_STAGE_COMPETENCIES"
    INTERNAL = "INTERNAL"


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
class SourcePackage:
    directory: Path
    source_path: Path
    items_path: Path
    source: dict[str, Any] | None = None
    items: dict[str, Any] | None = None


@dataclass
class CanonicalPackage:
    directory: Path
    set_path: Path
    competencies_path: Path
    competency_set: dict[str, Any] | None = None
    competencies: dict[str, Any] | None = None


@dataclass
class LearningSequencePackage:
    directory: Path
    sequence_path: Path
    sequence: Any | None = None


@dataclass(frozen=True)
class InvalidFixtureExpectation:
    schema_validator: str | None = None
    schema_path: tuple[Any, ...] = ()
    expected_instance: Any = None
    expected_validator_value: tuple[Any, ...] = ()
    required_property: str | None = None
    semantic_code: str | None = None
    semantic_value: str | None = None


@dataclass
class ValidationResult:
    diagnostics: list[Diagnostic] = field(default_factory=list)
    package_count: int = 0
    canonical_package_count: int = 0
    sequence_package_count: int = 0
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
    schema_names = {
        "source": "competency-source.schema.json",
        "items": "competency-items.schema.json",
        "canonical_set": "canonical-competency-set.schema.json",
        "canonical_competencies": "canonical-competencies.schema.json",
        "learning_sequence": "learning-sequence.schema.json",
    }
    for kind, filename in schema_names.items():
        path = root / "schemas" / filename
        try:
            with path.open(encoding="utf-8") as file:
                schema = json.load(file)
            Draft202012Validator.check_schema(schema)
            validators[kind] = Draft202012Validator(
                schema, format_checker=FormatChecker()
            )
        except (OSError, json.JSONDecodeError, SchemaError) as error:
            result.add(
                Code.SCHEMA_LOAD,
                _relative(root, path),
                str(error).splitlines()[0],
            )
            result.configuration_error = True
    return validators if len(validators) == len(schema_names) else None


def _load_yaml(root: Path, path: Path, result: ValidationResult) -> dict[str, Any] | None:
    try:
        with path.open(encoding="utf-8") as file:
            value = yaml.safe_load(file)
    except (OSError, yaml.YAMLError) as error:
        result.add(Code.YAML_PARSE, _relative(root, path), str(error).splitlines()[0])
        return None
    if not isinstance(value, dict):
        result.add(Code.YAML_PARSE, _relative(root, path), "YAML root must be a mapping")
        return None
    return value


def _load_sequence_yaml(root: Path, path: Path, result: ValidationResult) -> Any | None:
    try:
        with path.open(encoding="utf-8") as file:
            return yaml.safe_load(file)
    except (OSError, yaml.YAMLError) as error:
        result.add(Code.YAML_PARSE, _relative(root, path), str(error).splitlines()[0])
        return None


def _schema_errors(
    validator: Draft202012Validator, data: Any
) -> list[Any]:
    return sorted(
        validator.iter_errors(data),
        key=lambda error: (
            tuple(str(part) for part in error.absolute_path),
            error.message,
        ),
    )


def _validate_schema(
    root: Path,
    path: Path,
    validator: Draft202012Validator,
    data: Any,
    result: ValidationResult,
) -> bool:
    errors = _schema_errors(validator, data)
    for error in errors:
        result.add(
            Code.SCHEMA,
            _relative(root, path),
            error.message,
            _property_path(error.absolute_path),
        )
    return not errors


def _duplicates(values: Iterable[Any]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            continue
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def _duplicate_item_ids(items_data: Mapping[str, Any]) -> list[str]:
    items = items_data.get("items", [])
    if not isinstance(items, list):
        return []
    return _duplicates(
        item.get("id") for item in items if isinstance(item, Mapping)
    )


def _matches_invalid_fixture_expectation(
    data: Mapping[str, Any],
    errors: list[Any],
    expectation: InvalidFixtureExpectation,
) -> bool:
    if expectation.semantic_code == Code.DUPLICATE_ITEM_ID:
        return not errors and _duplicate_item_ids(data) == [expectation.semantic_value]

    if len(errors) != 1:
        return False
    error = errors[0]
    if error.validator != expectation.schema_validator:
        return False
    if tuple(error.absolute_path) != expectation.schema_path:
        return False
    if expectation.required_property is not None:
        return (
            isinstance(error.instance, Mapping)
            and expectation.required_property in error.validator_value
            and expectation.required_property not in error.instance
        )
    return (
        error.instance == expectation.expected_instance
        and tuple(error.validator_value) == expectation.expected_validator_value
    )


def _validate_support_files(
    root: Path,
    validators: Mapping[str, Draft202012Validator],
    result: ValidationResult,
) -> None:
    template_paths = {
        "source": root / "templates/competency-source/source.yaml",
        "items": root / "templates/competency-source/items.yaml",
    }
    result.template_count = len(template_paths)
    template_data: dict[str, dict[str, Any]] = {}
    for kind, path in template_paths.items():
        if not path.is_file():
            result.add(Code.SCHEMA, _relative(root, path), "required template is missing")
            continue
        data = _load_yaml(root, path, result)
        if data is not None:
            template_data[kind] = data
            _validate_schema(root, path, validators[kind], data, result)
    _validate_pair(
        root,
        template_paths["source"],
        template_paths["items"],
        template_data.get("source"),
        template_data.get("items"),
        result,
    )

    fixture_root = root / "schemas/fixtures/competencies"
    fixtures = (
        ("source", fixture_root / "valid/source.yaml", None),
        ("items", fixture_root / "valid/items.yaml", None),
        (
            "source",
            fixture_root / "invalid/source-invalid-usage.yaml",
            InvalidFixtureExpectation(
                schema_validator="enum",
                schema_path=("repository_usage",),
                expected_instance="unrestricted",
                expected_validator_value=(
                    "public",
                    "owned",
                    "permission-granted",
                    "citation-only",
                ),
            ),
        ),
        (
            "items",
            fixture_root / "invalid/items-duplicate-id.yaml",
            InvalidFixtureExpectation(
                semantic_code=Code.DUPLICATE_ITEM_ID,
                semantic_value="repeated-item",
            ),
        ),
        (
            "items",
            fixture_root / "invalid/items-missing-locator.yaml",
            InvalidFixtureExpectation(
                schema_validator="required",
                schema_path=("items", 0),
                required_property="locator",
            ),
        ),
    )
    result.fixture_count = len(fixtures)
    valid_data: dict[str, dict[str, Any]] = {}
    for kind, path, invalid_expectation in fixtures:
        if not path.is_file():
            result.add(Code.SCHEMA, _relative(root, path), "required competency fixture is missing")
            continue
        data = _load_yaml(root, path, result)
        if data is None:
            continue
        errors = _schema_errors(validators[kind], data)
        if invalid_expectation is None:
            valid_data[kind] = data
            _validate_schema(root, path, validators[kind], data, result)
        elif not _matches_invalid_fixture_expectation(
            data, errors, invalid_expectation
        ):
            result.add(
                Code.FIXTURE_EXPECTATION,
                _relative(root, path),
                "fixture did not fail exclusively for its intended reason",
            )
    _validate_pair(
        root,
        fixture_root / "valid/source.yaml",
        fixture_root / "valid/items.yaml",
        valid_data.get("source"),
        valid_data.get("items"),
        result,
    )
    _validate_canonical_fixtures(root, validators, result)
    _validate_learning_sequence_fixtures(root, validators, result)


def _validate_canonical_fixtures(
    root: Path,
    validators: Mapping[str, Draft202012Validator],
    result: ValidationResult,
) -> None:
    fixture_root = root / "schemas/fixtures/competencies/canonical"
    valid_paths = {
        "canonical_set": fixture_root / "valid/competency-set.yaml",
        "canonical_competencies": fixture_root / "valid/competencies.yaml",
    }
    invalid_expectations = {
        "competencies-missing-evidence.yaml": (
            ("required",),
            ("competencies", 0),
        ),
        "competencies-duplicate-item-id.yaml": (
            ("uniqueItems",),
            ("competencies", 0, "evidence", 0, "item_ids"),
        ),
        "competencies-duplicate-evidence.yaml": (
            ("uniqueItems",),
            ("competencies", 0, "evidence"),
        ),
        "competencies-unsupported-field.yaml": (
            ("additionalProperties",),
            ("competencies", 0),
        ),
        "competencies-empty-title.yaml": (
            ("minLength", "pattern"),
            ("competencies", 0, "title"),
        ),
        "competencies-empty-outcome.yaml": (
            ("minLength", "pattern"),
            ("competencies", 0, "outcome"),
        ),
    }
    result.fixture_count += len(valid_paths) + len(invalid_expectations)
    for kind, path in valid_paths.items():
        if not path.is_file():
            result.add(Code.SCHEMA, _relative(root, path), "required canonical fixture is missing")
            continue
        data = _load_yaml(root, path, result)
        if data is not None:
            _validate_schema(root, path, validators[kind], data, result)

    validator = validators["canonical_competencies"]
    for filename, (expected_validators, expected_path) in invalid_expectations.items():
        path = fixture_root / "invalid" / filename
        if not path.is_file():
            result.add(Code.SCHEMA, _relative(root, path), "required canonical fixture is missing")
            continue
        data = _load_yaml(root, path, result)
        if data is None:
            continue
        errors = _schema_errors(validator, data)
        if (
            sorted(error.validator for error in errors) != sorted(expected_validators)
            or any(tuple(error.absolute_path) != expected_path for error in errors)
        ):
            result.add(
                Code.FIXTURE_EXPECTATION,
                _relative(root, path),
                "fixture did not fail exclusively for its intended reason",
            )


def _validate_learning_sequence_fixtures(
    root: Path,
    validators: Mapping[str, Draft202012Validator],
    result: ValidationResult,
) -> None:
    fixture_root = root / "schemas/fixtures/learning-sequences"
    valid_filenames = ("minimal.yaml", "multi-stage.yaml")
    invalid_expectations = {
        "missing-required-field.yaml": (("required",), ()),
        "unsupported-schema-version.yaml": (("const",), ("schema_version",)),
        "empty-stages.yaml": (("minItems",), ("stages",)),
        "empty-stage-competencies.yaml": (
            ("minItems",),
            ("stages", 0, "competencies"),
        ),
        "duplicate-competency-within-stage.yaml": (
            ("uniqueItems",),
            ("stages", 0, "competencies"),
        ),
        "unexpected-property.yaml": (("additionalProperties",), ()),
    }
    semantic_expectations = {
        "duplicate-stage-id.yaml": Code.DUPLICATE_STAGE_ID,
        "duplicate-competency-across-stages.yaml": Code.DUPLICATE_SEQUENCE_COMPETENCY,
        "unknown-competency-set.yaml": Code.SEQUENCE_COMPETENCY_SET_MISSING,
        "wrong-competency-set-version.yaml": (
            Code.SEQUENCE_COMPETENCY_SET_VERSION_MISMATCH
        ),
        "unknown-competency.yaml": Code.SEQUENCE_COMPETENCY_MISSING,
    }
    result.fixture_count += (
        len(valid_filenames) + len(invalid_expectations) + len(semantic_expectations)
    )
    validator = validators["learning_sequence"]
    for filename in valid_filenames:
        path = fixture_root / "valid" / filename
        if not path.is_file():
            result.add(Code.SCHEMA, _relative(root, path), "required sequence fixture is missing")
            continue
        data = _load_yaml(root, path, result)
        if data is not None:
            _validate_schema(root, path, validator, data, result)

    for filename, (expected_validators, expected_path) in invalid_expectations.items():
        path = fixture_root / "invalid" / filename
        if not path.is_file():
            result.add(Code.SCHEMA, _relative(root, path), "required sequence fixture is missing")
            continue
        data = _load_yaml(root, path, result)
        if data is None:
            continue
        errors = _schema_errors(validator, data)
        if (
            sorted(error.validator for error in errors) != sorted(expected_validators)
            or any(tuple(error.absolute_path) != expected_path for error in errors)
        ):
            result.add(
                Code.FIXTURE_EXPECTATION,
                _relative(root, path),
                "fixture did not fail exclusively for its intended reason",
            )

    fixture_canonical = CanonicalPackage(
        directory=fixture_root / "fixture-competency-set",
        set_path=fixture_root / "fixture-competency-set/competency-set.yaml",
        competencies_path=fixture_root / "fixture-competency-set/competencies.yaml",
        competency_set={"id": "fixture-competency-set", "version": 1},
        competencies={
            "competencies": [
                {"id": "explain-fixture-boundary"},
                {"id": "apply-fixture-boundary"},
            ]
        },
    )
    for filename, expected_code in semantic_expectations.items():
        path = fixture_root / "invalid" / filename
        if not path.is_file():
            result.add(Code.SCHEMA, _relative(root, path), "required sequence fixture is missing")
            continue
        data = _load_yaml(root, path, result)
        if data is None:
            continue
        if _schema_errors(validator, data):
            result.add(
                Code.FIXTURE_EXPECTATION,
                _relative(root, path),
                "semantic fixture must satisfy the learning-sequence schema",
            )
            continue
        fixture_result = ValidationResult()
        fixture_package = LearningSequencePackage(
            directory=path.parent / str(data.get("sequence_id")),
            sequence_path=path,
            sequence=data,
        )
        _validate_learning_sequence(
            root,
            fixture_package,
            {"fixture-competency-set": fixture_canonical},
            fixture_result,
        )
        if {item.code for item in fixture_result.diagnostics} != {expected_code}:
            result.add(
                Code.FIXTURE_EXPECTATION,
                _relative(root, path),
                "fixture did not fail exclusively for its intended semantic reason",
            )


def _discover_packages(root: Path) -> list[SourcePackage]:
    sources_root = root / "competencies/sources"
    if not sources_root.is_dir():
        return []
    return [
        SourcePackage(
            directory=directory,
            source_path=directory / "source.yaml",
            items_path=directory / "items.yaml",
        )
        for directory in sorted(sources_root.iterdir(), key=lambda path: path.name)
        if directory.is_dir()
    ]


def _discover_canonical_packages(root: Path) -> list[CanonicalPackage]:
    normalized_root = root / "competencies/normalized"
    if not normalized_root.is_dir():
        return []
    return [
        CanonicalPackage(
            directory=directory,
            set_path=directory / "competency-set.yaml",
            competencies_path=directory / "competencies.yaml",
        )
        for directory in sorted(normalized_root.iterdir(), key=lambda path: path.name)
        if directory.is_dir()
    ]


def _discover_learning_sequence_packages(root: Path) -> list[LearningSequencePackage]:
    sequences_root = root / "learning-sequences"
    if not sequences_root.is_dir():
        return []
    return [
        LearningSequencePackage(
            directory=directory,
            sequence_path=directory / "sequence.yaml",
        )
        for directory in sorted(sequences_root.iterdir(), key=lambda path: path.name)
        if directory.is_dir() and directory.name != "reports"
    ]


def _validate_pair(
    root: Path,
    source_path: Path,
    items_path: Path,
    source: Mapping[str, Any] | None,
    items: Mapping[str, Any] | None,
    result: ValidationResult,
) -> None:
    if source is None or items is None:
        return
    if source.get("id") != items.get("source_id"):
        result.add(
            Code.SOURCE_ID_MISMATCH,
            _relative(root, items_path),
            f"source_id {items.get('source_id')!r} does not match source id {source.get('id')!r}",
            "source_id",
        )
    if source.get("source_version") != items.get("source_version"):
        result.add(
            Code.SOURCE_VERSION_MISMATCH,
            _relative(root, items_path),
            "items source_version does not match source metadata",
            "source_version",
        )
    for duplicate_id in _duplicate_item_ids(items):
        result.add(
            Code.DUPLICATE_ITEM_ID,
            _relative(root, items_path),
            f"item id {duplicate_id!r} appears more than once",
            "items",
        )


def _safe_artifact_path(package: Path, declared_path: str) -> tuple[Path, str] | None:
    if "\\" in declared_path:
        return None
    pure_path = PurePosixPath(declared_path)
    if pure_path.is_absolute() or not pure_path.parts or pure_path.parts[0] != "raw":
        return None
    if ".." in pure_path.parts or "." in pure_path.parts or len(pure_path.parts) < 2:
        return None
    target = package.joinpath(*pure_path.parts)
    raw_root = (package / "raw").resolve()
    try:
        if not target.resolve().is_relative_to(raw_root):
            return None
    except OSError:
        if not target.resolve(strict=False).is_relative_to(raw_root):
            return None
    return target, pure_path.as_posix()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_artifacts(
    root: Path,
    package: SourcePackage,
    source: Mapping[str, Any],
    result: ValidationResult,
) -> None:
    source_display = _relative(root, package.source_path)
    artifacts = source.get("artifacts", [])
    if not isinstance(artifacts, list):
        artifacts = []
    if source.get("repository_usage") == "citation-only" and artifacts:
        result.add(
            Code.CITATION_ONLY_ARTIFACT,
            source_display,
            "citation-only sources must not declare committed artifacts",
            "artifacts",
        )
    declared_values = [
        artifact.get("path") for artifact in artifacts if isinstance(artifact, Mapping)
    ]
    for duplicate_path in _duplicates(declared_values):
        result.add(
            Code.DUPLICATE_ARTIFACT_PATH,
            source_display,
            f"artifact path {duplicate_path!r} appears more than once",
            "artifacts",
        )

    declared_safe_paths: set[str] = set()
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, Mapping):
            continue
        declared_path = artifact.get("path")
        if not isinstance(declared_path, str):
            continue
        safe_path = _safe_artifact_path(package.directory, declared_path)
        location = f"artifacts[{index}].path"
        if safe_path is None:
            result.add(
                Code.ARTIFACT_PATH,
                source_display,
                f"artifact path {declared_path!r} must stay inside this package's raw directory",
                location,
            )
            continue
        target, normalized_path = safe_path
        declared_safe_paths.add(normalized_path)
        if not target.exists():
            result.add(
                Code.ARTIFACT_MISSING,
                source_display,
                f"declared artifact {declared_path!r} does not exist",
                location,
            )
            continue
        if target.is_symlink() or not target.is_file():
            result.add(
                Code.ARTIFACT_NOT_FILE,
                source_display,
                f"declared artifact {declared_path!r} is not a regular file",
                location,
            )
            continue
        expected_hash = artifact.get("sha256")
        if isinstance(expected_hash, str) and _sha256(target) != expected_hash:
            result.add(
                Code.ARTIFACT_HASH_MISMATCH,
                source_display,
                f"SHA-256 does not match for {declared_path!r}",
                f"artifacts[{index}].sha256",
            )

    raw_root = package.directory / "raw"
    if raw_root.is_dir():
        for path in sorted(raw_root.rglob("*")):
            if path.is_file():
                relative_path = path.relative_to(package.directory).as_posix()
                if relative_path not in declared_safe_paths:
                    result.add(
                        Code.UNDECLARED_ARTIFACT,
                        _relative(root, path),
                        "regular file under raw is not declared in source.yaml",
                    )


def _validate_repository_wide(
    root: Path, packages: list[SourcePackage], result: ValidationResult
) -> None:
    packages_by_id: dict[str, list[SourcePackage]] = {}
    for package in packages:
        if package.source is None:
            continue
        source_id = package.source.get("id")
        if isinstance(source_id, str):
            packages_by_id.setdefault(source_id, []).append(package)
    for source_id, matches in sorted(packages_by_id.items()):
        if len(matches) > 1:
            paths = sorted(_relative(root, package.source_path) for package in matches)
            result.add(
                Code.DUPLICATE_SOURCE_ID,
                paths[0],
                f"source id {source_id!r} appears in: {', '.join(paths)}",
            )


def _source_index(packages: list[SourcePackage]) -> dict[str, SourcePackage]:
    index: dict[str, SourcePackage] = {}
    for package in packages:
        if package.source is None or package.items is None:
            continue
        source_id = package.source.get("id")
        if isinstance(source_id, str) and source_id not in index:
            index[source_id] = package
    return index


def _evidence_key(entry: Mapping[str, Any]) -> tuple[str, int, tuple[str, ...]] | None:
    source_id = entry.get("source_id")
    source_version = entry.get("source_version")
    item_ids = entry.get("item_ids", [])
    if (
        not isinstance(source_id, str)
        or not isinstance(source_version, int)
        or isinstance(source_version, bool)
        or not isinstance(item_ids, list)
        or not all(isinstance(item_id, str) for item_id in item_ids)
    ):
        return None
    return (
        source_id,
        source_version,
        tuple(sorted(item_ids)),
    )


def _validate_canonical_pair(
    root: Path,
    package: CanonicalPackage,
    source_packages: Mapping[str, SourcePackage],
    result: ValidationResult,
) -> None:
    competency_set = package.competency_set
    document = package.competencies
    if competency_set is None or document is None:
        return
    set_id = competency_set.get("id")
    if set_id != package.directory.name:
        result.add(
            Code.CANONICAL_PACKAGE_ID_MISMATCH,
            _relative(root, package.set_path),
            f"competency set id {set_id!r} does not match package directory {package.directory.name!r}",
            "id",
        )
    if document.get("competency_set_id") != set_id:
        result.add(
            Code.COMPETENCY_SET_ID_MISMATCH,
            _relative(root, package.competencies_path),
            f"competency_set_id {document.get('competency_set_id')!r} does not match set id {set_id!r}",
            "competency_set_id",
        )
    if document.get("competency_set_version") != competency_set.get("version"):
        result.add(
            Code.COMPETENCY_SET_VERSION_MISMATCH,
            _relative(root, package.competencies_path),
            "competency_set_version does not match competency set metadata",
            "competency_set_version",
        )
    competencies = document.get("competencies", [])
    if not isinstance(competencies, list):
        return
    for competency_index, competency in enumerate(competencies):
        if not isinstance(competency, Mapping):
            continue
        competency_id = competency.get("id")
        evidence = competency.get("evidence", [])
        if not isinstance(evidence, list):
            continue
        seen_entries: set[tuple[str, int, tuple[str, ...]]] = set()
        duplicate_entries: set[tuple[str, int, tuple[str, ...]]] = set()
        for entry in evidence:
            if not isinstance(entry, Mapping):
                continue
            key = _evidence_key(entry)
            if key is None:
                continue
            if key in seen_entries:
                duplicate_entries.add(key)
            seen_entries.add(key)
        for source_id, source_version, item_ids in sorted(duplicate_entries):
            result.add(
                Code.DUPLICATE_EVIDENCE_ENTRY,
                _relative(root, package.competencies_path),
                f"competency {competency_id!r} repeats evidence for {source_id!r} version {source_version!r} and items {list(item_ids)!r}",
                f"competencies[{competency_index}] ({competency_id}).evidence",
            )
        for evidence_index, entry in enumerate(evidence):
            if not isinstance(entry, Mapping):
                continue
            location = f"competencies[{competency_index}] ({competency_id}).evidence[{evidence_index}]"
            source_id = entry.get("source_id")
            source_package = source_packages.get(source_id) if isinstance(source_id, str) else None
            if source_package is None:
                result.add(
                    Code.EVIDENCE_SOURCE_MISSING,
                    _relative(root, package.competencies_path),
                    f"competency {competency_id!r} references missing source {source_id!r}",
                    location,
                )
                continue
            actual_version = source_package.source.get("source_version") if source_package.source else None
            if entry.get("source_version") != actual_version:
                result.add(
                    Code.EVIDENCE_SOURCE_VERSION_MISMATCH,
                    _relative(root, package.competencies_path),
                    f"competency {competency_id!r} references source {source_id!r} version {entry.get('source_version')!r}, expected {actual_version!r}",
                    f"{location}.source_version",
                )
            item_ids = entry.get("item_ids", [])
            if not isinstance(item_ids, list):
                continue
            for duplicate_id in _duplicates(item_ids):
                result.add(
                    Code.DUPLICATE_EVIDENCE_ITEM,
                    _relative(root, package.competencies_path),
                    f"competency {competency_id!r} repeats item {duplicate_id!r} in evidence for source {source_id!r}",
                    f"{location}.item_ids",
                )
            available_items = {
                item.get("id")
                for item in (source_package.items or {}).get("items", [])
                if isinstance(item, Mapping) and isinstance(item.get("id"), str)
            }
            for item_id in item_ids:
                if isinstance(item_id, str) and item_id not in available_items:
                    result.add(
                        Code.EVIDENCE_ITEM_MISSING,
                        _relative(root, package.competencies_path),
                        f"competency {competency_id!r} references missing item {item_id!r} in source {source_id!r}",
                        f"{location}.item_ids",
                    )


def _validate_canonical_packages(
    root: Path,
    packages: list[CanonicalPackage],
    source_packages: Mapping[str, SourcePackage],
    validators: Mapping[str, Draft202012Validator],
    result: ValidationResult,
) -> None:
    for package in packages:
        for required_path in (package.set_path, package.competencies_path):
            if not required_path.is_file():
                result.add(
                    Code.MISSING_FILE,
                    _relative(root, package.directory),
                    f"missing required file {required_path.name!r}",
                )
        if package.set_path.is_file():
            package.competency_set = _load_yaml(root, package.set_path, result)
            if package.competency_set is not None:
                _validate_schema(
                    root,
                    package.set_path,
                    validators["canonical_set"],
                    package.competency_set,
                    result,
                )
        if package.competencies_path.is_file():
            package.competencies = _load_yaml(root, package.competencies_path, result)
            if package.competencies is not None:
                _validate_schema(
                    root,
                    package.competencies_path,
                    validators["canonical_competencies"],
                    package.competencies,
                    result,
                )
        _validate_canonical_pair(root, package, source_packages, result)

    competency_locations: dict[str, list[str]] = {}
    set_locations: dict[str, list[str]] = {}
    for package in packages:
        set_id = (package.competency_set or {}).get("id")
        if isinstance(set_id, str):
            set_locations.setdefault(set_id, []).append(
                _relative(root, package.set_path)
            )
        document = package.competencies or {}
        competencies = document.get("competencies", [])
        if not isinstance(competencies, list):
            continue
        for competency in competencies:
            if not isinstance(competency, Mapping):
                continue
            competency_id = competency.get("id")
            if isinstance(competency_id, str):
                competency_locations.setdefault(competency_id, []).append(
                    _relative(root, package.competencies_path)
                )
    for competency_id, paths in sorted(competency_locations.items()):
        if len(paths) > 1:
            result.add(
                Code.DUPLICATE_CANONICAL_ID,
                sorted(paths)[0],
                f"canonical competency id {competency_id!r} appears in: {', '.join(sorted(paths))}",
                "competencies",
            )
    for set_id, paths in sorted(set_locations.items()):
        if len(paths) > 1:
            result.add(
                Code.DUPLICATE_COMPETENCY_SET_ID,
                sorted(paths)[0],
                f"competency set id {set_id!r} appears in: {', '.join(sorted(paths))}",
                "id",
            )


def _canonical_set_index(
    packages: list[CanonicalPackage],
) -> dict[str, CanonicalPackage]:
    index: dict[str, CanonicalPackage] = {}
    for package in packages:
        set_id = (package.competency_set or {}).get("id")
        if isinstance(set_id, str) and set_id not in index:
            index[set_id] = package
    return index


def _canonical_competency_ids(package: CanonicalPackage) -> set[str]:
    document = package.competencies or {}
    competencies = document.get("competencies", [])
    if not isinstance(competencies, list):
        return set()
    return {
        competency["id"]
        for competency in competencies
        if isinstance(competency, Mapping) and isinstance(competency.get("id"), str)
    }


def _validate_learning_sequence(
    root: Path,
    package: LearningSequencePackage,
    canonical_sets: Mapping[str, CanonicalPackage],
    result: ValidationResult,
) -> None:
    sequence = package.sequence
    if not isinstance(sequence, Mapping):
        return
    display_path = _relative(root, package.sequence_path)
    sequence_id = sequence.get("sequence_id")
    if sequence_id != package.directory.name:
        result.add(
            Code.SEQUENCE_PACKAGE_ID_MISMATCH,
            display_path,
            f"sequence id {sequence_id!r} does not match package directory {package.directory.name!r}",
            "sequence_id",
        )

    stages = sequence.get("stages", [])
    if not isinstance(stages, list):
        return
    if not stages:
        result.add(
            Code.EMPTY_SEQUENCE_STAGES,
            display_path,
            "learning sequence must contain at least one stage",
            "stages",
        )
    stage_ids = [
        stage.get("id") for stage in stages if isinstance(stage, Mapping)
    ]
    for duplicate_id in _duplicates(stage_ids):
        result.add(
            Code.DUPLICATE_STAGE_ID,
            display_path,
            f"stage id {duplicate_id!r} appears more than once",
            "stages",
        )

    first_stage_by_competency: dict[str, tuple[int, str]] = {}
    referenced_competencies: list[tuple[int, str | None, str]] = []
    for stage_index, stage in enumerate(stages):
        if not isinstance(stage, Mapping):
            continue
        stage_id = stage.get("id")
        stage_label = stage_id if isinstance(stage_id, str) else f"index-{stage_index}"
        competencies = stage.get("competencies", [])
        if not isinstance(competencies, list):
            continue
        location = f"stages[{stage_index}] ({stage_label}).competencies"
        if not competencies:
            result.add(
                Code.EMPTY_STAGE_COMPETENCIES,
                display_path,
                f"stage {stage_label!r} must reference at least one competency",
                location,
            )
        for duplicate_id in _duplicates(competencies):
            result.add(
                Code.DUPLICATE_STAGE_COMPETENCY,
                display_path,
                f"stage {stage_label!r} repeats competency {duplicate_id!r}",
                location,
            )
        for competency_id in competencies:
            if not isinstance(competency_id, str):
                continue
            referenced_competencies.append((stage_index, stage_id, competency_id))
        for competency_id in sorted(set(value for value in competencies if isinstance(value, str))):
            previous_stage = first_stage_by_competency.get(competency_id)
            if previous_stage is not None and previous_stage[0] != stage_index:
                result.add(
                    Code.DUPLICATE_SEQUENCE_COMPETENCY,
                    display_path,
                    f"competency {competency_id!r} appears in stages {previous_stage[1]!r} and {stage_label!r}",
                    "stages",
                )
            else:
                first_stage_by_competency[competency_id] = (stage_index, stage_label)

    set_reference = sequence.get("competency_set", {})
    if not isinstance(set_reference, Mapping):
        return
    set_id = set_reference.get("id")
    canonical_package = canonical_sets.get(set_id) if isinstance(set_id, str) else None
    if canonical_package is None:
        result.add(
            Code.SEQUENCE_COMPETENCY_SET_MISSING,
            display_path,
            f"referenced competency set {set_id!r} does not exist",
            "competency_set.id",
        )
        return
    expected_version = (canonical_package.competency_set or {}).get("version")
    referenced_version = set_reference.get("version")
    if referenced_version != expected_version:
        result.add(
            Code.SEQUENCE_COMPETENCY_SET_VERSION_MISMATCH,
            display_path,
            f"competency set {set_id!r} version {referenced_version!r} does not match repository version {expected_version!r}",
            "competency_set.version",
        )
        return

    available_ids = _canonical_competency_ids(canonical_package)
    for stage_index, stage_id, competency_id in referenced_competencies:
        if competency_id not in available_ids:
            stage_label = stage_id if isinstance(stage_id, str) else f"index-{stage_index}"
            result.add(
                Code.SEQUENCE_COMPETENCY_MISSING,
                display_path,
                f"stage {stage_label!r} references missing competency {competency_id!r} in set {set_id!r} version {referenced_version!r}",
                f"stages[{stage_index}] ({stage_label}).competencies",
            )


def _validate_learning_sequence_packages(
    root: Path,
    packages: list[LearningSequencePackage],
    canonical_packages: list[CanonicalPackage],
    validator: Draft202012Validator,
    result: ValidationResult,
) -> None:
    canonical_sets = _canonical_set_index(canonical_packages)
    identities: dict[tuple[str, int], list[str]] = {}
    for package in packages:
        if not package.sequence_path.is_file():
            result.add(
                Code.MISSING_FILE,
                _relative(root, package.directory),
                "missing required file 'sequence.yaml'",
            )
            continue
        package.sequence = _load_sequence_yaml(root, package.sequence_path, result)
        if package.sequence is None:
            continue
        _validate_schema(root, package.sequence_path, validator, package.sequence, result)
        _validate_learning_sequence(root, package, canonical_sets, result)
        if not isinstance(package.sequence, Mapping):
            continue
        sequence_id = package.sequence.get("sequence_id")
        sequence_version = package.sequence.get("sequence_version")
        if (
            isinstance(sequence_id, str)
            and isinstance(sequence_version, int)
            and not isinstance(sequence_version, bool)
        ):
            identities.setdefault((sequence_id, sequence_version), []).append(
                _relative(root, package.sequence_path)
            )
    for (sequence_id, sequence_version), paths in sorted(identities.items()):
        if len(paths) > 1:
            ordered_paths = sorted(paths)
            result.add(
                Code.DUPLICATE_SEQUENCE_VERSION,
                ordered_paths[0],
                f"sequence {sequence_id!r} version {sequence_version!r} appears in: {', '.join(ordered_paths)}",
                "sequence_version",
            )


def validate_repository(root: Path, verbose: bool = False) -> ValidationResult:
    root = root.resolve()
    result = ValidationResult()
    validators = _load_schemas(root, result)
    if validators is None:
        return result
    if verbose:
        result.verbose_messages.append("Loaded and meta-validated competency schemas.")

    _validate_support_files(root, validators, result)
    packages = _discover_packages(root)
    result.package_count = len(packages)
    if verbose:
        result.verbose_messages.append(f"Discovered {len(packages)} competency source package(s).")

    for package in packages:
        for required_path in (package.source_path, package.items_path):
            if not required_path.is_file():
                result.add(
                    Code.MISSING_FILE,
                    _relative(root, package.directory),
                    f"missing required file {required_path.name!r}",
                )
        if package.source_path.is_file():
            package.source = _load_yaml(root, package.source_path, result)
            if package.source is not None:
                _validate_schema(
                    root, package.source_path, validators["source"], package.source, result
                )
                if package.source.get("id") != package.directory.name:
                    result.add(
                        Code.PACKAGE_ID_MISMATCH,
                        _relative(root, package.source_path),
                        f"source id {package.source.get('id')!r} does not match package directory {package.directory.name!r}",
                        "id",
                    )
                _validate_artifacts(root, package, package.source, result)
        if package.items_path.is_file():
            package.items = _load_yaml(root, package.items_path, result)
            if package.items is not None:
                _validate_schema(
                    root, package.items_path, validators["items"], package.items, result
                )
        _validate_pair(
            root,
            package.source_path,
            package.items_path,
            package.source,
            package.items,
            result,
        )

    _validate_repository_wide(root, packages, result)
    canonical_packages = _discover_canonical_packages(root)
    result.canonical_package_count = len(canonical_packages)
    if verbose:
        result.verbose_messages.append(
            f"Discovered {len(canonical_packages)} canonical competency package(s)."
        )
    _validate_canonical_packages(
        root,
        canonical_packages,
        _source_index(packages),
        validators,
        result,
    )
    sequence_packages = _discover_learning_sequence_packages(root)
    result.sequence_package_count = len(sequence_packages)
    if verbose:
        result.verbose_messages.append(
            f"Discovered {len(sequence_packages)} learning-sequence package(s)."
        )
    _validate_learning_sequence_packages(
        root,
        sequence_packages,
        canonical_packages,
        validators["learning_sequence"],
        result,
    )
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
    except Exception as error:  # Controlled boundary for unexpected failures.
        print(f"ERROR [{Code.INTERNAL}] {args.root}: {error}")
        return 2
    for message in result.verbose_messages:
        print(f"INFO {message}")
    diagnostics = result.sorted_diagnostics()
    for diagnostic in diagnostics:
        print(diagnostic.render())
    if result.passed:
        print(
            "Competency validation passed: "
            f"{result.package_count} source packages, "
            f"{result.canonical_package_count} canonical packages, "
            f"{result.sequence_package_count} learning-sequence packages, "
            f"{result.template_count} templates, {result.fixture_count} schema fixtures."
        )
    else:
        print(
            "Competency validation failed: "
            f"{len(diagnostics)} errors across {result.package_count} source packages "
            f"{result.canonical_package_count} canonical packages, and "
            f"{result.sequence_package_count} learning-sequence packages."
        )
    return result.exit_code


if __name__ == "__main__":
    sys.exit(main())
