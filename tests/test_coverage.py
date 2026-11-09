import copy

import pytest

from schema_coverage_lab.coverage import analyze, replay
from schema_coverage_lab.jsonio import LIMITS, InputError, dumps, equal, loads


def corpus(*values):
    return [{"id": str(i), "value": v} for i, v in enumerate(values)]


def conjunction():
    return {"allOf": [{"type": "integer"}, {"minimum": 18}]}


def test_conjunction_pairs_replay_and_order_independence():
    data = corpus(18, 17, "x")
    result = analyze(conjunction(), data)
    assert result["counts"]["covered"] == 2
    assert [o["witness"]["endpoint_ids"] for o in result["obligations"]] == [["0", "2"], ["0", "1"]]
    assert replay(loads(dumps(result)))["covered_pairs"] == 2
    assert equal(result, analyze(conjunction(), list(reversed(data))))


@pytest.mark.parametrize("schema,data,covered,unknown", [
    ({"anyOf": [{"type": "integer"}, {"type": "integer"}]}, corpus(1, "x"), 0, 2),
    ({"allOf": [{"minimum": 0}, {"minimum": 10}]}, corpus(-1, 5, 10, "x"), 1, 1),
    ({"allOf": [{"const": 0}, {"const": 1}]}, corpus(0, 1, 2), 0, 2),
    ({"anyOf": [True, {"type": "integer"}]}, corpus(1, "x"), 0, 2),
    ({"oneOf": [True, True, True]}, corpus(None, 1), 0, 3),
    ({"not": {"type": "integer"}}, corpus(1, "x"), 1, 0),
    ({"oneOf": [{"minimum": 0}, {"maximum": 10}]}, corpus(-1, 5, 11), 2, 0),
])
def test_semantic_counterexamples(schema, data, covered, unknown):
    result = analyze(schema, data)
    assert result["counts"]["covered"] == covered
    assert result["counts"]["unknown"] == unknown
    replay(result)


def test_global_not_found_is_unknown_finite_absence_is_scoped():
    schema = {"anyOf": [{"const": 1}, {"const": 1}]}
    global_report = analyze(schema, corpus(1, 2))
    finite_report = analyze(schema, corpus(1, 2), domain="candidate_pool")
    assert global_report["counts"]["unknown"] == 2
    assert global_report["scores"]["feasibility_adjusted"]["denominator"] == 2
    assert finite_report["counts"]["proven_infeasible"] == 2
    assert finite_report["scores"]["feasibility_adjusted"] is None
    assert all(o["scope"] == "candidate_pool" for o in finite_report["obligations"])


@pytest.mark.parametrize("schema", [True, False, {}, {"type": "integer"}])
def test_atomic_and_constant_schemas_have_no_invented_obligations(schema):
    result = analyze(schema, corpus(1, "x"))
    assert result["obligations"] == []
    assert result["scores"]["raw"] is None
    assert replay(result)["covered_pairs"] == 0


def test_outcome_coverage_does_not_make_an_independence_pair():
    # 17 gives 01; "x" gives 10 for these selected predicates. Both change,
    # the OR result remains true, so condition outcomes alone are insufficient.
    result = analyze({"anyOf": [{"type": "integer"}, {"minimum": 18}]}, corpus(17, "x"))
    assert result["decisions"][0]["observed_condition_outcomes"] == [[False, True], [False, True]]
    assert result["counts"]["covered"] == 0


def test_conjunction_00_11_outcomes_without_independence():
    schema = {"allOf": [{"minimum": 0}, {"minimum": 10}]}
    result = analyze(schema, corpus(-1, 10))
    assert result["decisions"][0]["observed_local_outcomes"] == [False, True]
    assert result["counts"]["covered"] == 0


def test_pair_can_cross_two_suites_and_uncovered_feasibility_is_retained():
    schema = {"not": {"const": 1}}
    data = corpus(1, 2)
    left = analyze(schema, data, suite_ids=["0"])
    right = analyze(schema, data, suite_ids=["1"])
    both = analyze(schema, data)
    assert left["counts"]["feasible_uncovered"] == right["counts"]["feasible_uncovered"] == 1
    assert both["counts"]["covered"] == 1
    assert analyze(schema, data, suite_ids=[])["counts"]["feasible_uncovered"] == 1


def test_local_influence_does_not_require_or_claim_root_influence():
    schema = {"allOf": [False, {"anyOf": [{"const": 0}, {"const": 1}]}]}
    result = analyze(schema, corpus(0, 1, 2))
    assert all(r["valid"] is False for r in result["root_results"])
    assert result["counts"]["covered"] == 2
    assert len({o["decision_id"] for o in result["obligations"]}) == 2
    assert "local" in result["decomposition"]


@pytest.mark.parametrize("schema", [
    {"properties": {"a": True}}, {"$ref": "#"}, {"$defs": {}},
    {"if": True, "then": False}, {"format": "email"}, {"multipleOf": 2},
    {"allOf": [{"unevaluatedProperties": False}]}, {"unknown": True},
    {"$schema": "http://json-schema.org/draft-07/schema#"},
])
def test_unsupported_has_no_partial_catalog_or_percentage(schema):
    result = analyze(schema, corpus(1))
    assert result["analysis_status"] == "unsupported"
    assert not result["catalog_complete"]
    assert result["scores"] is None and result["counts"] is None
    assert result["diagnostics"][0]["path"].startswith("/")


@pytest.mark.parametrize("schema", [{"allOf": []}, {"type": "bogus"}, {"minimum": "x"}, []])
def test_invalid_schema_is_not_ordinary_invalidity_or_unsupported(schema):
    with pytest.raises(InputError, match="Invalid Draft"):
        analyze(schema, corpus(1))


@pytest.mark.parametrize("data,suite", [
    ([{"id": "a", "value": 1}, {"id": "a", "value": 2}], None),
    ([{"id": "", "value": 1}], None), ([{"id": "a"}], None),
    (corpus(1), ["missing"]), (corpus(1), ["0", "0"]), (corpus(1), "0"),
])
def test_invalid_corpus_and_suite_are_errors(data, suite):
    with pytest.raises(InputError):
        analyze({}, data, suite_ids=suite)


def test_empty_corpus_retains_unknown_obligations():
    result = analyze(conjunction(), [])
    assert result["counts"]["unknown"] == 2
    assert result["scores"]["raw"] == {"numerator": 0, "denominator": 2}


@pytest.mark.parametrize("field", ["schema_digest", "schema_resource", "criterion", "report_version",
                                   "counts", "observations", "root_results", "decisions", "environment",
                                   "suite_ids", "obligations", "configuration", "catalog_complete"])
def test_replay_rejects_altered_evidence_or_contract(field):
    result = copy.deepcopy(analyze(conjunction(), corpus(18, 17, "x")))
    result[field] = None
    with pytest.raises(InputError):
        replay(result)


def test_limits_are_errors_not_coverage_results():
    schema = True
    for _ in range(34):
        schema = {"not": schema}
    with pytest.raises(InputError):
        analyze(schema, corpus(1))
    with pytest.raises(InputError, match="Condition count"):
        analyze({"anyOf": [True] * 65}, corpus(1))


def test_expanded_report_must_fit_strict_replay_loader(monkeypatch):
    monkeypatch.setitem(LIMITS, "nodes", 1000)
    # Each input separately fits, but expanded observation evidence does not.
    with pytest.raises(InputError, match="node limit"):
        analyze({"anyOf": [{"const": i} for i in range(5)]}, corpus(*range(80)))
