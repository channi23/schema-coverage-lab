"""Strict JSON and an exact, versioned project serialization (not RFC 8785)."""

import hashlib
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path


class InputError(ValueError):
    """Malformed input, invalid schema, or exceeded admitted resource limits."""


LIMITS = {"input_bytes": 16_777_216, "depth": 64, "nodes": 100_000,
          "numeric_digits": 1000, "numeric_exponent": 1000,
          "corpus_size": 10_000, "conditions_per_decision": 64,
          "schema_depth": 32, "value_depth": 32, "evaluation_cells": 100_000}


def is_number(value):
    return isinstance(value, (int, Decimal)) and not isinstance(value, bool)


def check_value(value, *, max_depth=None):
    """Admit JSON values only; floats must enter through exact JSON parsing."""
    count = 0

    def walk(v, depth):
        nonlocal count
        count += 1
        if depth > (LIMITS["depth"] if max_depth is None else max_depth) or count > LIMITS["nodes"]:
            raise InputError("JSON depth/node limit exceeded")
        if v is None or isinstance(v, (str, bool)):
            return
        if is_number(v):
            n = Decimal(v)
            if not n.is_finite():
                raise InputError("Nonfinite JSON number")
            t = n.as_tuple()
            if (len(t.digits) > LIMITS["numeric_digits"] or
                    abs(t.exponent) > LIMITS["numeric_exponent"] or
                    abs(n.adjusted()) > LIMITS["numeric_exponent"]):
                raise InputError("Numeric representation limit exceeded")
            return
        if isinstance(v, list):
            for item in v:
                walk(item, depth + 1)
            return
        if isinstance(v, dict) and all(isinstance(k, str) for k in v):
            for item in v.values():
                walk(item, depth + 1)
            return
        raise InputError("Expected JSON types; use Decimal rather than native float")

    walk(value, 0)


def loads(text):
    if len(text.encode("utf-8")) > LIMITS["input_bytes"]:
        raise InputError("JSON input byte limit exceeded")

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise InputError("Duplicate JSON key: " + key)
            result[key] = value
        return result

    def reject_constant(token):
        raise InputError("Nonfinite JSON token: " + token)

    try:
        value = json.loads(text, parse_float=Decimal, object_pairs_hook=pairs,
                           parse_constant=reject_constant)
        check_value(value)
        return value
    except (json.JSONDecodeError, InvalidOperation, RecursionError) as exc:
        raise InputError("Invalid JSON: " + str(exc)) from exc
    except ValueError as exc:
        if isinstance(exc, InputError):
            raise
        raise InputError("Invalid JSON number: " + str(exc)) from exc


def read(path):
    try:
        with Path(path).open("rb") as handle:
            data = handle.read(LIMITS["input_bytes"] + 1)
        if len(data) > LIMITS["input_bytes"]:
            raise InputError("JSON input byte limit exceeded")
        return loads(data.decode("utf-8"))
    except (OSError, UnicodeError) as exc:
        raise InputError(str(exc)) from exc


def number_text(value):
    n = Decimal(value)
    if n == 0:
        return "0"
    sign, digits, exponent = n.as_tuple()
    digits = list(digits)
    while digits[-1] == 0:
        digits.pop()
        exponent += 1
    coefficient = ("-" if sign else "") + "".join(map(str, digits))
    return coefficient + ("e" + str(exponent) if exponent else "")


def dumps(value):
    """Exact canonical JSON v1: sorted keys, ASCII strings, normalized decimals."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if is_number(value):
        return number_text(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=True)
    if isinstance(value, list):
        return "[" + ",".join(dumps(v) for v in value) + "]"
    if isinstance(value, dict):
        return "{" + ",".join(dumps(k) + ":" + dumps(value[k])
                                for k in sorted(value)) + "}"
    raise InputError("Cannot serialize non-JSON value")


def digest(value):
    return hashlib.sha256(dumps(value).encode("ascii")).hexdigest()


def equal(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if is_number(a) or is_number(b):
        return is_number(a) and is_number(b) and a == b
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(equal(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(equal(a[k], b[k]) for k in a)
    return type(a) is type(b) and a == b
