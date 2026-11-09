"""Deterministic, incomplete candidate recipes for pure-v1 schemas."""

from decimal import Decimal, Inexact, ROUND_CEILING, ROUND_FLOOR, localcontext

from .jsonio import LIMITS, InputError, admit_output, check_value, digest, dumps
from .oracle import check_schema
from .semantics import LOGICAL, support_issues


def generate(schema, *, max_candidates=128):
    check_value(schema, max_depth=LIMITS["schema_depth"])
    check_schema(schema)
    issues = support_issues(schema)
    if issues:
        raise InputError("Generation requires pure-v1: " + str(issues))
    if type(max_candidates) is not int or not 1 <= max_candidates <= 128:
        raise InputError("max_candidates must be an integer from 1 to 128")
    proposed, rejected, bounds = {}, [], []

    def add(value, reason, priority):
        try:
            check_value(value)
        except InputError as exc:
            rejected.append({"reason": reason, "error": str(exc)})
            return
        key = digest(value)
        if key not in proposed:
            proposed[key] = {"value": value, "reasons": [], "priority": priority}
        proposed[key]["priority"] = min(proposed[key]["priority"], priority)
        if reason not in proposed[key]["reasons"]:
            proposed[key]["reasons"].append(reason)

    def visit(node, path=""):
        if isinstance(node, bool):
            return
        for key in ("const", "enum"):
            if key in node:
                values = node[key] if key == "enum" else [node[key]]
                for i, value in enumerate(values):
                    add(value, path + "/" + key + "/" + str(i), 0)
        for key in ("minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum"):
            if key in node:
                value = Decimal(node[key])
                bounds.append(value)
                add(value, path + "/" + key + ":boundary", 0)
        for key in LOGICAL:
            if key in node:
                children = [node[key]] if key == "not" else node[key]
                for i, child in enumerate(children):
                    visit(child, path + "/" + key + "/" + str(i))

    visit(schema)
    # 5000 digits exceed admitted input precision/exponent combinations; trap
    # any accidental inexact operation rather than silently rounding a witness.
    with localcontext() as context:
        context.prec = 5000
        context.traps[Inexact] = True
        unique_bounds = sorted(set(bounds))
        for bound in unique_bounds:
            epsilon = Decimal((0, (1,), min(bound.as_tuple().exponent, 0) - 1))
            for delta in (Decimal(1), Decimal("0.5"), epsilon):
                add(bound - delta, "numeric:below", 1)
                add(bound + delta, "numeric:above", 1)
            for rounded in (bound.to_integral_value(rounding=ROUND_FLOOR),
                            bound.to_integral_value(rounding=ROUND_CEILING)):
                for delta in (-1, 0, 1):
                    add(rounded + delta, "numeric:integer-neighbor", 1)
        for left, right in zip(unique_bounds, unique_bounds[1:]):
            add((left + right) / 2, "numeric:interval-midpoint", 1)
    for value in (None, False, True, -1, 0, 1, Decimal("0.5"), "", "x", [], [None], {}, {"x": None}):
        add(value, "primitive:representative", 2)
    # Fresh representatives outside a finite family of equality literals.
    for factory in (lambda n: "__fresh_" + str(n), lambda n: ["__fresh_" + str(n)],
                    lambda n: {"__fresh_" + str(n): None}):
        for n in range(len(proposed) + 1):
            value = factory(n)
            if digest(value) not in proposed:
                add(value, "primitive:fresh-nonliteral", 2)
                break
    ordered = sorted(proposed, key=lambda key: (proposed[key]["priority"], dumps(proposed[key]["value"])))
    chosen = ordered[:max_candidates]
    instances = sorted(({"id": "g-" + key, "value": proposed[key]["value"]} for key in chosen),
                       key=lambda entry: entry["id"])
    return admit_output({"instances": instances, "generation": {
        "recipe": "literal-boundary-v1", "schema_digest": digest(schema),
        "max_candidates": max_candidates, "proposed_distinct": len(proposed),
        "retained": len(instances), "truncated": len(ordered) > len(chosen),
        "priority_ids": ["g-" + key for key in chosen],
        "reasons": {"g-" + key: proposed[key]["reasons"] for key in chosen},
        "rejected_representations": rejected,
        "completeness": "heuristic candidate pool; no all-JSON completeness claim"}})
