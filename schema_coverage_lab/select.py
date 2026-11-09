"""Pair-aware reduction and budgeted offline selection over frozen evidence."""

from itertools import combinations

from .coverage import analyze, replay
from .jsonio import InputError, admit_output, digest, equal

CRITERIA = ("decision", "predicate", "independence")


class EvidenceIndex:
    def __init__(self, report):
        if report["analysis_status"] != "supported":
            raise InputError("Selection requires supported analysis")
        if len(report["candidate_ids"]) > 128:
            raise InputError("Selection limited to 128 candidates")
        self.report = report
        self.ids = tuple(report["candidate_ids"])
        self.rows = {d["decision_id"]: {} for d in report["decisions"]}
        for row in report["observations"]:
            self.rows[row["decision_id"]][row["input_id"]] = row
        self.edges = {}
        edge_count = 0
        for decision in report["decisions"]:
            did = decision["decision_id"]
            for i in range(decision["condition_count"]):
                pairs = []
                for a, b in combinations(self.ids, 2):
                    x, y = self.rows[did][a], self.rows[did][b]
                    if (x["local_result"] != y["local_result"] and
                            [j for j, (u, v) in enumerate(zip(x["vector"], y["vector"])) if u != v] == [i]):
                        pairs.append(frozenset((a, b)))
                edge_count += len(pairs)
                if edge_count > 200_000:
                    raise InputError("Selection eligible-pair limit exceeded")
                self.edges[did + ":" + str(i)] = pairs
        self.universes = {criterion: self.covered(self.ids, criterion) for criterion in CRITERIA}

    def covered(self, suite, criterion):
        if criterion not in CRITERIA:
            raise InputError("Unknown selection criterion")
        chosen = set(suite)
        if not chosen <= set(self.ids):
            raise InputError("Selected ids are not in candidate pool")
        if criterion == "independence":
            return {condition for condition, pairs in self.edges.items() if any(p <= chosen for p in pairs)}
        result = set()
        for did, rows in self.rows.items():
            for input_id in chosen:
                row = rows[input_id]
                if criterion == "decision":
                    result.add((did, row["local_result"]))
                else:
                    result.update((did, i, value) for i, value in enumerate(row["vector"]))
        return result


def greedy(index, criterion="independence", *, budget=None, fill=False):
    if criterion not in CRITERIA:
        raise InputError("Unknown selection criterion")
    if budget is None:
        budget = len(index.ids)
    if type(budget) is not int or not 0 <= budget <= len(index.ids):
        raise InputError("Budget must be within candidate pool size")
    target = index.universes[criterion]
    chosen, current = set(), set()
    actions = ({tuple(sorted(pair)) for pairs in index.edges.values() for pair in pairs}
               if criterion == "independence" else {(i,) for i in index.ids})
    while current != target:
        best = None
        for action in sorted(actions):
            addition = set(action) - chosen
            if not addition or len(chosen | addition) > budget:
                continue
            covered = index.covered(chosen | addition, criterion)
            gain = len(covered - current)
            if not gain:
                continue
            # Compare integer cross-products rather than floating gain/cost.
            if (best is None or gain * best[1] > best[0] * len(addition) or
                    (gain * best[1] == best[0] * len(addition) and action < best[2])):
                best = (gain, len(addition), action, covered)
        if best is None:
            break
        chosen.update(best[2])
        current = best[3]
    if fill:
        for input_id in index.ids:
            if len(chosen) == budget:
                break
            chosen.add(input_id)
    else:
        for input_id in sorted(chosen, reverse=True):
            if index.covered(chosen - {input_id}, criterion) == current:
                chosen.remove(input_id)
    return sorted(chosen)


def exact(index, criterion="independence"):
    if len(index.ids) > 16:
        raise InputError("Exact reduction limited to 16 candidates (65536 subsets)")
    target = index.universes[criterion]
    for size in range(len(index.ids) + 1):
        for suite in combinations(index.ids, size):
            if index.covered(suite, criterion) == target:
                return list(suite)
    raise InputError("Internal error: full pool did not preserve its own evidence")


def reduce_report(report, *, criterion="independence", method="greedy"):
    replay(report)
    index = EvidenceIndex(report)
    if method == "greedy":
        suite = greedy(index, criterion)
    elif method == "exact":
        suite = exact(index, criterion)
    else:
        raise InputError("Reduction method must be greedy or exact")
    if index.covered(suite, criterion) != index.universes[criterion]:
        raise InputError("Reduction failed to preserve finite-pool evidence")
    result = analyze(report["schema"], report["corpus"], suite_ids=suite,
                     domain=report["domain"]["kind"])
    replay(result)
    return admit_output({"source_report": report, "reduction": {"criterion": criterion, "method": method,
                          "scope": "supplied finite candidate pool", "candidate_count": len(index.ids),
                          "selected_count": len(suite), "selected_ids": suite,
                          "preserved_features": len(index.universes[criterion]),
                          "optimality": "minimum distinct tests within pool" if method == "exact" else "not claimed",
                          "source_report_digest": digest(report)}, "report": result})


def replay_reduction(bundle):
    try:
        expected = reduce_report(bundle["source_report"], criterion=bundle["reduction"]["criterion"],
                                 method=bundle["reduction"]["method"])
    except (KeyError, TypeError) as exc:
        raise InputError("Incomplete reduction bundle") from exc
    if not equal(bundle, expected):
        raise InputError("Reduction replay mismatch")
    return {"replay_status": "verified", "selected_count": expected["reduction"]["selected_count"],
            "preserved_features": expected["reduction"]["preserved_features"],
            "scope": "supplied finite candidate pool"}
