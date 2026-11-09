"""Deterministic finite-corpus evidence and strict pair detection."""

import platform

from . import __version__
from .jsonio import LIMITS, InputError, check_value, digest, dumps, equal
from .oracle import DIALECT, Oracle, check_schema, environment
from .semantics import catalog, evaluate, support_issues

STATUSES = ("covered", "feasible_uncovered", "proven_infeasible", "unknown", "unsupported")


def _report(value):
    # Observations expand a corpus. Do not emit a report the strict loader
    # cannot subsequently read for replay, even when each input was admissible.
    check_value(value)
    if len(dumps(value).encode("ascii")) + 1 > LIMITS["input_bytes"]:
        raise InputError("Report exceeds replayable input byte limit")
    return value


def _pair(observations, index, allowed):
    by_vector = {}
    for row in observations:
        if row["input_id"] in allowed:
            key = tuple(row["vector"])
            by_vector.setdefault(key, row)
    choices = []
    for vector, row in by_vector.items():
        flipped = list(vector)
        flipped[index] = not flipped[index]
        other = by_vector.get(tuple(flipped))
        if other and row["local_result"] != other["local_result"]:
            endpoints = sorted([row, other], key=lambda r: r["input_id"])
            choices.append(endpoints)
    return min(choices, key=lambda rows: [r["input_id"] for r in rows]) if choices else None


def analyze(schema, corpus, *, suite_ids=None, domain="all_json"):
    """Analyze supplied candidates; all_json not-found stays unknown."""
    check_value(schema, max_depth=LIMITS["schema_depth"])
    check_schema(schema)
    if domain not in ("all_json", "candidate_pool"):
        raise InputError("domain must be all_json or candidate_pool")
    if not isinstance(corpus, list) or len(corpus) > LIMITS["corpus_size"]:
        raise InputError("Expected a bounded corpus list")
    check_value(corpus)
    candidates = {}
    for entry in corpus:
        if (not isinstance(entry, dict) or set(entry) != {"id", "value"} or
                not isinstance(entry["id"], str) or not entry["id"] or
                len(entry["id"]) > 200 or entry["id"] in candidates):
            raise InputError("Corpus entries need unique nonempty string ids and value")
        candidates[entry["id"]] = entry["value"]
        check_value(entry["value"], max_depth=LIMITS["value_depth"])
    ids = sorted(candidates)
    if suite_ids is None:
        suite_ids = ids
    if (not isinstance(suite_ids, list) or
            not all(isinstance(i, str) for i in suite_ids) or
            len(set(suite_ids)) != len(suite_ids) or
            not set(suite_ids) <= candidates.keys()):
        raise InputError("suite_ids must be a unique subset of candidate ids")
    suite_ids = sorted(suite_ids)
    corpus = [{"id": i, "value": candidates[i]} for i in ids]
    schema_digest = digest(schema)
    resource = "urn:sha256:" + schema_digest
    report = {
        "report_version": 1, "engine_version": __version__,
        "criterion": "semantic_unique_cause_v1", "fragment": "pure-v1",
        "decomposition": "immediate children of each local logical applicator",
        "context": "root instance; no references; semantic evaluation, not execution",
        "dialect": DIALECT, "schema_digest": schema_digest, "schema_resource": resource,
        "schema": schema, "corpus_digest": digest(corpus), "corpus": corpus,
        "candidate_ids": ids, "suite_ids": suite_ids,
        "instance_digests": {i: digest(candidates[i]) for i in ids},
        "domain": {"kind": domain, "description": (
            "Exactly the supplied candidate pool" if domain == "candidate_pool" else
            "All JSON; corpus search is incomplete for this universe")},
        "configuration": {"serialization": "project-exact-json-v1",
                          "numbers": "exact decimal; oracle integral normalization",
                          "format_assertion": False, "remote_retrieval": False,
                          "generation": "none; supplied corpus only", "limits": LIMITS},
        "environment": {"python": platform.python_version(),
                        "system": platform.system(), "machine": platform.machine(),
                        "oracle": environment()},
    }
    unsupported = support_issues(schema)
    if unsupported:
        return _report({**report, "analysis_status": "unsupported", "diagnostics": unsupported,
                "catalog_complete": False, "counts": None, "scores": None,
                "decisions": [], "observations": [], "root_results": [], "obligations": []})
    decisions = catalog(schema)
    work = (1 + sum(len(d["children"]) for d in decisions)) * len(corpus)
    if work > LIMITS["evaluation_cells"]:
        raise InputError("Schema occurrences times corpus size exceeds 100000 evaluation cells")
    root_oracle = Oracle(schema)
    oracle_children = {d["pointer"]: [Oracle(s) for s in d["children"]] for d in decisions}
    rows = {d["pointer"]: [] for d in decisions}
    root_results = []
    for input_id in ids:
        value = candidates[input_id]
        local = {}
        root = evaluate(schema, value, observations=local)
        if root != root_oracle.valid(value):
            raise InputError("Oracle disagreement at root for " + input_id)
        root_results.append({"input_id": input_id, "valid": root, "oracle_replayed": True})
        for decision in decisions:
            pointer = decision["pointer"]
            row = local[pointer]
            oracle_vector = [o.valid(value) for o in oracle_children[pointer]]
            # Validate the applicator itself, not just a shared Boolean function.
            local_schema = {decision["function"]: (
                decision["children"][0] if decision["function"] == "not" else decision["children"])}
            oracle_local = Oracle(local_schema).valid(value)
            if row["vector"] != oracle_vector or row["local_result"] != oracle_local:
                raise InputError("Oracle disagreement at " + pointer + " for " + input_id)
            rows[pointer].append({"input_id": input_id, **row, "root_result": root,
                                  "evaluation_status": "complete", "oracle_replayed": True})
    obligations, decision_records, observations = [], [], []
    for d in decisions:
        pointer = d["pointer"]
        decision_id = resource + "#" + pointer + "@semantic_unique_cause_v1"
        selected_rows = [r for r in rows[pointer] if r["input_id"] in suite_ids]
        decision_records.append({"decision_id": decision_id, "pointer": pointer,
                                 "function": d["function"], "condition_count": len(d["children"]),
                                 "observed_local_outcomes": sorted({r["local_result"] for r in selected_rows}),
                                 "observed_condition_outcomes": [sorted({r["vector"][i] for r in selected_rows})
                                                                 for i in range(len(d["children"]))]})
        observations.extend({"decision_id": decision_id, **r} for r in rows[pointer])
        for i in range(len(d["children"])):
            pair = _pair(rows[pointer], i, set(suite_ids))
            status = "covered" if pair else "feasible_uncovered"
            if pair is None:
                pair = _pair(rows[pointer], i, set(ids))
            if pair is None:
                status = "proven_infeasible" if domain == "candidate_pool" else "unknown"
            witness = None if pair is None else {
                "endpoint_ids": [r["input_id"] for r in pair],
                "vectors": [r["vector"] for r in pair],
                "local_results": [r["local_result"] for r in pair],
                "target_index": i, "oracle_replayed": True}
            obligations.append({"condition_id": decision_id + ":" + str(i),
                                "decision_id": decision_id, "target_index": i,
                                "status": status, "scope": domain, "witness": witness,
                                "evidence": ("complete finite candidate enumeration" if status == "proven_infeasible"
                                             else "incomplete all-JSON search" if status == "unknown"
                                             else "independently replayed concrete pair")})
    counts = {s: sum(o["status"] == s for o in obligations) for s in STATUSES}
    total = len(obligations)
    adjusted = total - counts["proven_infeasible"]
    return _report({**report, "analysis_status": "supported", "diagnostics": [],
            "catalog_complete": True, "counts": counts,
            "scores": {"scope": domain,
                       "raw": {"numerator": counts["covered"], "denominator": total} if total else None,
                       "feasibility_adjusted": {"numerator": counts["covered"], "denominator": adjusted} if adjusted else None},
            "decisions": decision_records, "observations": observations,
            "root_results": root_results, "obligations": obligations})


def replay(report):
    """Recompute the complete report, including oracle evidence; reject tampering."""
    if not isinstance(report, dict):
        raise InputError("Expected a coverage report object")
    try:
        expected = analyze(report["schema"], report["corpus"], suite_ids=report["suite_ids"],
                           domain=report["domain"]["kind"])
    except (KeyError, TypeError) as exc:
        raise InputError("Incomplete report envelope") from exc
    if not equal(expected, report):
        raise InputError("Report replay mismatch: evidence, configuration or environment changed")
    return {"replay_status": "verified", "analysis_status": report["analysis_status"],
            "schema_digest": report["schema_digest"],
            "covered_pairs": 0 if report["counts"] is None else report["counts"]["covered"],
            "observations_checked": len(report["observations"])}
