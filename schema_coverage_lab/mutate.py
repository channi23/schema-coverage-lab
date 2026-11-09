"""Small declared schema mutation family; no global equivalence inference."""

from copy import deepcopy
from decimal import Decimal, localcontext

from .jsonio import InputError, digest
from .oracle import check_schema
from .semantics import LOGICAL, support_issues


def mutations(schema, *, limit=32):
    if type(limit) is not int or not 1 <= limit <= 128:
        raise InputError("Mutation limit must be 1..128")
    proposals = []

    def replace(path, replacement, operator):
        result = deepcopy(schema)
        if not path:
            result = replacement
        else:
            parent = result
            for step in path[:-1]:
                parent = parent[step]
            parent[path[-1]] = replacement
        proposals.append({"operator": operator, "path": list(path), "schema": result})

    def visit(node, path=()):
        if isinstance(node, bool):
            replace(path, not node, "flip-boolean-schema")
            return
        for key in ("minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum"):
            if key in node:
                with localcontext() as context:
                    context.prec = 5000
                    for shift in (-1, 1):
                        new = deepcopy(node)
                        new[key] = Decimal(node[key]) + shift
                        replace(path, new, "shift-" + key + ":" + str(shift))
        if "type" in node:
            new = deepcopy(node)
            new["type"] = "number" if node["type"] == "integer" else "boolean"
            replace(path, new, "replace-type")
        if "const" in node:
            new = deepcopy(node)
            new["const"] = "__mutated_const" if node["const"] is None else None
            replace(path, new, "replace-const")
        if "enum" in node and len(node["enum"]) > 1:
            new = deepcopy(node)
            new["enum"] = node["enum"][1:]
            replace(path, new, "remove-first-enum-member")
        for key in LOGICAL:
            if key not in node:
                continue
            if key != "not":
                new = deepcopy(node)
                target = {"allOf": "anyOf", "anyOf": "allOf", "oneOf": "anyOf"}[key]
                if target not in new:
                    new[target] = new.pop(key)
                    replace(path, new, "replace-" + key + "-with-" + target)
                if len(node[key]) > 1:
                    for i in range(len(node[key])):
                        new = deepcopy(node)
                        del new[key][i]
                        replace(path, new, "remove-" + key + "-child:" + str(i))
                for i, child in enumerate(node[key]):
                    visit(child, (*path, key, i))
            else:
                new = deepcopy(node)
                new[key] = {"not": new[key]}
                replace(path, new, "double-not")
                visit(node[key], (*path, key))

    visit(schema)
    unique, invalid = {}, []
    original = digest(schema)
    for p in proposals:
        key = digest(p["schema"])
        if key == original or key in unique:
            continue
        try:
            check_schema(p["schema"])
            if support_issues(p["schema"]):
                raise InputError("Mutation left admitted fragment")
        except InputError as exc:
            invalid.append({"operator": p["operator"], "reason": str(exc)})
            continue
        unique[key] = {"id": "m-" + key, **p}
    return {"mutants": list(unique.values())[:limit], "invalid_proposals": invalid,
            "distinct_admitted_proposals": len(unique), "truncated": len(unique) > limit,
            "family": "local-bound-type-const-enum-boolean-applicator-v1"}
