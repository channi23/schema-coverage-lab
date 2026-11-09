"""Independent evaluator for the explicitly admitted pure fragment."""

from decimal import Decimal

from .jsonio import LIMITS, InputError, equal, is_number
from .oracle import DIALECT

LOGICAL = ("allOf", "anyOf", "oneOf", "not")
ALLOWED = {"$schema", "title", "description", "$comment", "type", "const", "enum",
           "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", *LOGICAL}


def support_issues(schema, path=""):
    issues = []
    if isinstance(schema, bool):
        return issues
    for key in sorted(schema):
        pointer = path + "/" + key.replace("~", "~0").replace("/", "~1")
        if key not in ALLOWED:
            issues.append({"path": pointer, "reason": "Keyword outside pure-v1 fragment"})
        elif key == "$schema" and schema[key] != DIALECT:
            issues.append({"path": pointer, "reason": "Unsupported dialect declaration"})
    for key in LOGICAL:
        if key not in schema:
            continue
        children = [schema[key]] if key == "not" else schema[key]
        if len(children) > LIMITS["conditions_per_decision"]:
            raise InputError("Condition count exceeds limit at " + path + "/" + key)
        for i, child in enumerate(children):
            child_path = path + "/" + key + ("" if key == "not" else "/" + str(i))
            issues.extend(support_issues(child, child_path))
    return issues


def catalog(schema, path=""):
    if isinstance(schema, bool):
        return []
    result = []
    for key in LOGICAL:
        if key not in schema:
            continue
        children = [schema[key]] if key == "not" else schema[key]
        pointer = path + "/" + key
        result.append({"pointer": pointer, "function": key, "children": children})
        for i, child in enumerate(children):
            result.extend(catalog(child, pointer + ("" if key == "not" else "/" + str(i))))
    return result


def matches_type(value, name):
    return {
        "null": lambda: value is None,
        "boolean": lambda: isinstance(value, bool),
        "number": lambda: is_number(value),
        "integer": lambda: is_number(value) and Decimal(value) == Decimal(value).to_integral_value(),
        "string": lambda: isinstance(value, str),
        "array": lambda: isinstance(value, list),
        "object": lambda: isinstance(value, dict),
    }[name]()


def logical(function, vector):
    if function == "allOf":
        return all(vector)
    if function == "anyOf":
        return any(vector)
    if function == "oneOf":
        return sum(vector) == 1
    if function == "not":
        return not vector[0]
    raise InputError("Unknown local decision function")


def evaluate(schema, value, path="", observations=None):
    if isinstance(schema, bool):
        return schema
    results = []
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        results.append(any(matches_type(value, t) for t in types))
    if "const" in schema:
        results.append(equal(value, schema["const"]))
    if "enum" in schema:
        results.append(any(equal(value, v) for v in schema["enum"]))
    if is_number(value):
        for key, compare in (("minimum", lambda a, b: a >= b),
                             ("maximum", lambda a, b: a <= b),
                             ("exclusiveMinimum", lambda a, b: a > b),
                             ("exclusiveMaximum", lambda a, b: a < b)):
            if key in schema:
                results.append(compare(value, schema[key]))
    for key in LOGICAL:
        if key not in schema:
            continue
        pointer = path + "/" + key
        children = [schema[key]] if key == "not" else schema[key]
        vector = [evaluate(child, value,
                           pointer + ("" if key == "not" else "/" + str(i)), observations)
                  for i, child in enumerate(children)]
        local = logical(key, vector)
        results.append(local)
        if observations is not None:
            observations[pointer] = {"vector": vector, "local_result": local}
    return all(results)
