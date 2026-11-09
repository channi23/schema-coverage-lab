import subprocess
import sys
from pathlib import Path

import pytest

from schema_coverage_lab.checks import check_fixtures, check_official
from schema_coverage_lab.jsonio import read


@pytest.mark.parametrize("path,count", [
    ("research-fixtures/schema-semantics.json", 23),
    ("research-fixtures/semantic-counterexamples.json", 20),
])
def test_original_research_fixtures_against_independent_oracle(path, count):
    report = check_fixtures(read(path))
    assert report["tests"] == count
    assert report["status"] == "passed"
    assert any(row["analyzer"] == "unsupported" for row in report["results"])


def test_pinned_official_subset_and_explicit_exclusions():
    report = check_official("vendor/json-schema-test-suite")
    assert report["selected_tests"] == 295
    assert report["skipped_tests"] == 52
    assert report["suite_commit"] == "245a45abc90190c0bff04d97e6d2b541b4bb9f12"


def run(*args):
    return subprocess.run([sys.executable, "-m", "schema_coverage_lab", *map(str, args)],
                          text=True, capture_output=True)


def test_cli_round_trip_and_invalid_input(tmp_path):
    result = tmp_path / "report.json"
    first = run("analyze", "--schema", "examples/conjunction.schema.json", "--corpus",
                "examples/conjunction.instances.json", "--output", result)
    assert first.returncode == 0, first.stderr
    assert run("replay", "--report", result).returncode == 0
    before = result.read_bytes()
    assert run("analyze", "--schema", "examples/conjunction.schema.json", "--corpus",
               "examples/conjunction.instances.json", "--output", result).returncode == 0
    assert result.read_bytes() == before
    bad = tmp_path / "bad.json"
    bad.write_text('{"type":"integer","type":"number"}')
    assert run("analyze", "--schema", bad, "--corpus", "examples/conjunction.instances.json").returncode == 2


def test_cli_unsupported_has_distinct_exit(tmp_path):
    schema = tmp_path / "schema.json"
    schema.write_text('{"properties":{}}')
    result = run("analyze", "--schema", schema, "--corpus", "examples/conjunction.instances.json")
    assert result.returncode == 3
    assert '"analysis_status":"unsupported"' in result.stdout


def test_fixture_cli(tmp_path):
    output = tmp_path / "checked.json"
    result = run("check-fixtures", "--input", "research-fixtures/schema-semantics.json", "--output", output)
    assert result.returncode == 0, result.stderr
    assert read(output)["tests"] == 23
