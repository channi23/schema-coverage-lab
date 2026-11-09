"""Independent jsonschema oracle; no network resource retrieval."""

from decimal import Decimal
from importlib.metadata import version

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from referencing import Registry
from referencing.exceptions import NoSuchResource

from .jsonio import InputError, check_value

DIALECT = "https://json-schema.org/draft/2020-12/schema"


def _offline(uri):
    raise NoSuchResource(ref=uri)


REGISTRY = Registry(retrieve=_offline)


def _normalize(value):
    # jsonschema's stock integer checker recognizes ints, not Decimal. Convert
    # integral Decimal values exactly; nonintegral Decimals remain exact numbers.
    if isinstance(value, Decimal) and value == value.to_integral_value():
        return int(value)
    if isinstance(value, list):
        return [_normalize(v) for v in value]
    if isinstance(value, dict):
        return {k: _normalize(v) for k, v in value.items()}
    return value


def environment():
    return {name: version(name) for name in
            ("jsonschema", "jsonschema-specifications", "referencing", "rpds-py", "attrs")}


def check_schema(schema):
    check_value(schema)
    try:
        Draft202012Validator.check_schema(_normalize(schema))
    except SchemaError as exc:
        raise InputError("Invalid Draft 2020-12 schema: " + exc.message) from exc


class Oracle:
    def __init__(self, schema):
        self.validator = Draft202012Validator(_normalize(schema), registry=REGISTRY,
                                               format_checker=None)

    def valid(self, value):
        try:
            return self.validator.is_valid(_normalize(value))
        except Exception as exc:
            raise InputError("Oracle evaluation failed: " + str(exc)) from exc
