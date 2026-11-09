from decimal import Decimal

import pytest

from schema_coverage_lab.coverage import analyze
from schema_coverage_lab.jsonio import InputError, digest, dumps, equal, loads
from schema_coverage_lab.oracle import Oracle


@pytest.mark.parametrize("text", [
    '{"a":1,"a":2}', '{"x":{"a":1,"a":2}}', 'NaN', 'Infinity', '-Infinity',
    '1e9999', '1e-9999', '1' * 1001, '{', '01', '\ufeff{}',
])
def test_rejects_noncontract_json(text):
    with pytest.raises(InputError):
        loads(text)


@pytest.mark.parametrize("left,right,same", [
    ('1', '1.0', True), ('true', '1', False), ('false', '0', False),
    ('[1,{"a":2}]', '[1.00,{"a":2.0}]', True),
    ('{"a":1,"b":2}', '{"b":2,"a":1}', True), ('[1,2]', '[2,1]', False),
    ('0.10000000000000000000001', '0.1', False), ('null', 'false', False),
])
def test_structural_numeric_equality(left, right, same):
    a, b = loads(left), loads(right)
    assert equal(a, b) is same
    assert (digest(a) == digest(b)) is same
    assert equal(loads(dumps(a)), a)


@pytest.mark.parametrize("text", ['0', '-0.0', '1e1000', '1e-1000',
                                  '0.123456789012345678901234567890123456789'])
def test_serialization_never_rounds_decimal_context(text):
    value = loads(text)
    assert equal(loads(dumps(value)), value)


def test_decimal_bounds_and_integer_oracle_normalization():
    schema = loads('{"allOf":[{"type":"number"},{"exclusiveMinimum":0.10000000000000000000001}]}')
    result = analyze(schema, [{"id": "equal", "value": loads('0.10000000000000000000001')},
                              {"id": "higher", "value": loads('0.10000000000000000000002')}])
    assert [r["valid"] for r in result["root_results"]] == [False, True]
    assert Oracle({"type": "integer"}).valid(Decimal("1.000"))
    assert not Oracle({"type": "integer"}).valid(Decimal("1.001"))


def test_bool_is_not_number_or_numeric_const():
    for schema in [{"type": "integer"}, {"type": "number"}, {"const": 1}, {"enum": [1]}]:
        result = analyze(schema, [{"id": "bool", "value": True}])
        assert not result["root_results"][0]["valid"]


def test_api_rejects_native_float_instead_of_rounding():
    with pytest.raises(InputError, match="Decimal"):
        analyze({}, [{"id": "float", "value": 0.1}])


def test_offline_unknown_reference_fails_as_error():
    with pytest.raises(InputError, match="Oracle evaluation failed"):
        Oracle({"$ref": "https://invalid.example/must-not-fetch"}).valid(1)
