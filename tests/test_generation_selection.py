from decimal import Decimal
from itertools import combinations

import pytest

from schema_coverage_lab.coverage import analyze, replay
from schema_coverage_lab.generate import generate
from schema_coverage_lab.jsonio import InputError, dumps, equal, loads
from schema_coverage_lab.select import EvidenceIndex, exact, greedy, reduce_report


def test_generation_determinism_literals_boundaries_and_exact_decimal():
    schema = loads('{"allOf":[{"minimum":0.10000000000000000000001},{"maximum":1},{"enum":[1.0,"x",true]}]}')
    first = generate(schema)
    assert dumps(first) == dumps(generate(schema))
    values = [v["value"] for v in first["instances"]]
    assert any(equal(v, Decimal('0.10000000000000000000001')) for v in values)
    assert any(equal(v, True) for v in values)
    assert any(equal(v, 1) for v in values)
    assert any(isinstance(v, Decimal) and v > 0 and v < Decimal('0.10000000000000000000001') for v in values)
    assert not first["generation"]["truncated"]


def test_generation_caps_are_visible_and_do_not_claim_completeness():
    result = generate({"minimum": 10}, max_candidates=3)
    assert len(result["instances"]) == 3
    assert result["generation"]["truncated"]
    assert "no all-JSON" in result["generation"]["completeness"]


@pytest.mark.parametrize("schema", [{"properties": {}}, {"format": "email"}, {"$ref": "#"}])
def test_generator_rejects_deferred_semantics(schema):
    with pytest.raises(InputError, match="pure-v1"):
        generate(schema)


def test_fresh_representatives_are_not_mistaken_for_literal_complements():
    data = generate({"enum": ["", "x", [], [None], {}, {"x": None}, "__fresh_0"]})
    reasons = data["generation"]["reasons"]
    assert sum("primitive:fresh-nonliteral" in r for r in reasons.values()) == 3


def small_report():
    return analyze({"allOf": [{"type": "integer"}, {"minimum": 18}]},
                   [{"id": "a", "value": 18}, {"id": "b", "value": 17},
                    {"id": "c", "value": "x"}, {"id": "d", "value": 20}])


@pytest.mark.parametrize("criterion", ["decision", "predicate", "independence"])
def test_greedy_preserves_full_pool_evidence_and_exact_is_minimum(criterion):
    index = EvidenceIndex(small_report())
    g, e = greedy(index, criterion), exact(index, criterion)
    assert index.covered(g, criterion) == index.universes[criterion]
    assert index.covered(e, criterion) == index.universes[criterion]
    assert len(e) <= len(g)
    for size in range(len(e)):
        assert all(index.covered(s, criterion) != index.universes[criterion]
                   for s in combinations(index.ids, size))


def test_pair_reduction_keeps_both_endpoints_and_replays():
    result = reduce_report(small_report())
    assert result["reduction"]["selected_count"] == 3
    assert result["report"]["counts"]["covered"] == 2
    assert replay(result["report"])["covered_pairs"] == 2
    assert result["reduction"]["optimality"] == "not claimed"


def test_budget_is_distinct_tests_and_exactly_filled_for_comparison():
    index = EvidenceIndex(small_report())
    for budget in range(5):
        for criterion in ("decision", "predicate", "independence"):
            selected = greedy(index, criterion, budget=budget, fill=True)
            assert len(selected) == budget
            assert len(set(selected)) == budget
    assert index.covered(greedy(index, budget=1), "independence") == set()


def test_no_witness_pool_reduces_to_empty_without_false_coverage():
    report = analyze({"anyOf": [True, True]}, [{"id": "a", "value": 1}])
    result = reduce_report(report)
    assert result["reduction"]["selected_count"] == 0
    assert result["report"]["counts"]["covered"] == 0
    assert result["report"]["counts"]["unknown"] == 2


def test_exact_limit_is_explicit():
    data = [{"id": str(i), "value": i} for i in range(17)]
    with pytest.raises(InputError, match="16 candidates"):
        exact(EvidenceIndex(analyze({"not": {"const": 1}}, data)))
