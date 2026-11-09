import copy
import subprocess
import sys

import pytest

from schema_coverage_lab.coverage import analyze
from schema_coverage_lab.generate import generate
from schema_coverage_lab.jsonio import LIMITS, InputError, dumps, loads, read
from schema_coverage_lab.mutate import mutations
from schema_coverage_lab.oracle import Oracle, check_schema
from schema_coverage_lab.select import reduce_report, replay_reduction


def test_mutants_are_deduplicated_well_formed_and_controlled():
    schema = {"allOf": [{"minimum": 0}, {"type": "integer"}]}
    result = mutations(schema)
    assert len({m["id"] for m in result["mutants"]}) == len(result["mutants"])
    assert not result["invalid_proposals"]
    for m in result["mutants"]:
        check_schema(m["schema"])
        assert m["schema"] != schema


def test_pool_indistinguishable_is_not_global_equivalence():
    original = {"minimum": 0}
    shifted = {"minimum": 1}
    assert Oracle(original).valid(2) == Oracle(shifted).valid(2)
    assert Oracle(original).valid(0) != Oracle(shifted).valid(0)


def test_reduction_bundle_replay_recomputes_selection_and_rejects_tampering():
    bundle = reduce_report(analyze({"not": {"const": 1}}, [{"id": "a", "value": 1}, {"id": "b", "value": 2}]))
    assert replay_reduction(loads(dumps(bundle)))["selected_count"] == 2
    changed = copy.deepcopy(bundle)
    changed["reduction"]["selected_count"] = 1
    with pytest.raises(InputError, match="Reduction replay mismatch"):
        replay_reduction(changed)


def test_generated_cli_path_reduce_and_replay(tmp_path):
    def run(*args):
        return subprocess.run([sys.executable, "-m", "schema_coverage_lab", *map(str, args)],
                              capture_output=True, text=True)
    corpus, report, reduced = [tmp_path / name for name in ("corpus.json", "report.json", "reduced.json")]
    assert run("generate", "--schema", "examples/conjunction.schema.json", "--output", corpus).returncode == 0
    assert run("analyze", "--schema", "examples/conjunction.schema.json", "--corpus", corpus, "--output", report).returncode == 0
    assert run("reduce", "--report", report, "--output", reduced).returncode == 0
    result = run("replay", "--report", reduced)
    assert result.returncode == 0, result.stderr
    assert read(reduced)["reduction"]["selected_count"] == 3


def test_frozen_protocol_is_32_subjects_and_20_integral_seeds():
    data = read("benchmarks/study.json")
    assert len(data["subjects"]) == 32
    assert [int(s) for s in data["design"]["random_seeds"]] == list(range(20))


def test_reduction_bundle_must_fit_strict_replay_limits(monkeypatch):
    schema = {"not": {"const": 1}}
    corpus = [{"id": "a", "value": 1}, {"id": "b", "value": 2}]
    report = analyze(schema, corpus)
    def nodes(value):
        return 1 + (sum(nodes(v) for v in value.values()) if isinstance(value, dict) else
                    sum(nodes(v) for v in value) if isinstance(value, list) else 0)
    monkeypatch.setitem(LIMITS, "nodes", nodes(report) + 50)
    report = analyze(schema, corpus)
    with pytest.raises(InputError, match="node limit"):
        reduce_report(report)
