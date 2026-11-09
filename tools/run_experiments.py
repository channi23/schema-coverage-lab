"""Execute the frozen 32-subject offline selection study, with raw evidence."""

import hashlib
import json
import platform
import random
import statistics
import sys
import time
import tracemalloc
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from schema_coverage_lab.coverage import analyze, replay
from schema_coverage_lab.generate import generate
from schema_coverage_lab.jsonio import digest, dumps, read
from schema_coverage_lab.mutate import mutations
from schema_coverage_lab.oracle import Oracle, environment
from schema_coverage_lab.select import CRITERIA, EvidenceIndex, greedy, reduce_report, replay_reduction


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dumps(data) + "\n", encoding="ascii")


def score(numerator, denominator):
    return {"numerator": numerator, "denominator": denominator} if denominator else None


def ratio(record):
    return None if record is None else record["numerator"] / record["denominator"]


def aggregate(rows, subjects):
    summaries = []
    methods = ("decision", "predicate", "independence", "boundary", "random")
    budgets = sorted({r["budget"] for r in rows})
    for budget in budgets:
        for method in methods:
            group = [r for r in rows if r["budget"] == budget and r["method"] == method]
            summary = {"budget": budget, "method": method, "schemas": len({r["subject"] for r in group}),
                       "rows": len(group), "unit": "macro mean of per-schema means; random seeds nested"}
            for metric in ("decision", "predicate", "independence", "mutant_detectable", "mutant_all"):
                schema_means, within_sd = [], []
                for subject in sorted({r["subject"] for r in group}):
                    values = [ratio(r[metric]) for r in group if r["subject"] == subject and r[metric] is not None]
                    if values:
                        schema_means.append(statistics.mean(values))
                        within_sd.append(statistics.stdev(values) if len(values) > 1 else 0)
                summary[metric] = {"eligible_schemas": len(schema_means),
                                   "mean": format(statistics.mean(schema_means), ".6f") if schema_means else None,
                                   "median": format(statistics.median(schema_means), ".6f") if schema_means else None,
                                   "mean_within_schema_seed_sd": format(statistics.mean(within_sd), ".6f") if within_sd else None}
            summaries.append(summary)
    return {"subjects": len(subjects), "authored": 20, "official_derived": 12,
            "schema_units_with_feasible_independence_obligations": sum(s["feasible_independence_obligations"] > 0 for s in subjects),
            "pool_size": {"min": min(s["pool_size"] for s in subjects),
                          "max": max(s["pool_size"] for s in subjects),
                          "sum": sum(s["pool_size"] for s in subjects)},
            "truncated_pools": sum(s["generation_truncated"] for s in subjects),
            "mutants": sum(s["mutants"] for s in subjects),
            "pool_indistinguishable_mutants": sum(s["pool_indistinguishable"] for s in subjects),
            "invalid_mutation_proposals": sum(s["invalid_mutation_proposals"] for s in subjects),
            "reduction": {"subjects_with_targets": sum(s["feasible_independence_obligations"] > 0 for s in subjects),
                          "candidate_tests_total": sum(s["pool_size"] for s in subjects if s["feasible_independence_obligations"] > 0),
                          "selected_tests_total": sum(s["reduced_size"] for s in subjects if s["feasible_independence_obligations"] > 0),
                          "all_preserved_and_replayed": all(s["reduction_replayed"] for s in subjects)},
            "rows": len(rows), "random_seed_count": 20, "comparisons": summaries,
            "interpretation": "Descriptive selected-corpus offline comparison; no population significance, global equivalence or end-to-end superiority claim"}


def main():
    out = ROOT / "results/milestone-2"
    out.mkdir(parents=True, exist_ok=True)
    (out / "manifest.json").unlink(missing_ok=True)
    specification = read(ROOT / "benchmarks/study.json")
    design = specification["design"]
    rows, subjects = [], []
    for subject in specification["subjects"]:
        sid, schema = subject["id"], subject["schema"]
        tracemalloc.start()
        start = time.perf_counter_ns()
        generated = generate(schema, max_candidates=design["pool_cap"])
        generation_ns = time.perf_counter_ns() - start
        start = time.perf_counter_ns()
        report = analyze(schema, generated["instances"], domain="candidate_pool")
        replay(report)
        analysis_ns = time.perf_counter_ns() - start
        start = time.perf_counter_ns()
        index = EvidenceIndex(report)
        index_ns = time.perf_counter_ns() - start
        values = {r["id"]: r["value"] for r in generated["instances"]}
        original = {r["input_id"]: r["valid"] for r in report["root_results"]}
        start = time.perf_counter_ns()
        mutation_data = mutations(schema, limit=design["mutant_cap"])
        classified = []
        for mutant in mutation_data["mutants"]:
            oracle = Oracle(mutant["schema"])
            killing = [i for i in index.ids if oracle.valid(values[i]) != original[i]]
            classified.append({**mutant, "killing_ids": killing,
                               "classification": "pool_detectable" if killing else "pool_indistinguishable"})
        mutation_ns = time.perf_counter_ns() - start
        peak_memory = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        start = time.perf_counter_ns()
        reduced = reduce_report(report)
        replay_result = replay_reduction(reduced)
        reduction_ns = time.perf_counter_ns() - start
        case = out / "cases" / sid
        write(case / "corpus.json", generated)
        write(case / "pool-report.json", report)
        write(case / "reduced.json", reduced)
        write(case / "replay.json", replay_result)
        write(case / "mutants.json", {**mutation_data, "mutants": classified})
        detectable = [m for m in classified if m["killing_ids"]]
        subjects.append({"subject": sid, "provenance": subject["provenance"],
                         "schema_digest": digest(schema), "pool_size": len(index.ids),
                         "corpus_digest": report["corpus_digest"],
                         "generation_truncated": generated["generation"]["truncated"],
                         "rejected_numeric_representations": len(generated["generation"]["rejected_representations"]),
                         "feasible_independence_obligations": len(index.universes["independence"]),
                         "catalogued_obligations": len(report["obligations"]),
                         "reduced_size": reduced["reduction"]["selected_count"],
                         "reduction_replayed": replay_result["replay_status"] == "verified",
                         "mutants": len(classified), "pool_indistinguishable": len(classified) - len(detectable),
                         "invalid_mutation_proposals": len(mutation_data["invalid_proposals"]),
                         "mutation_truncated": mutation_data["truncated"],
                         "generation_ns": generation_ns, "analysis_and_replay_ns": analysis_ns,
                         "index_ns": index_ns, "mutation_classification_ns": mutation_ns,
                         "reduction_and_replay_ns": reduction_ns, "traced_preprocessing_peak_bytes": peak_memory})
        for declared_budget in design["budgets"]:
            budget = min(declared_budget, len(index.ids))
            selectors = [(criterion, None) for criterion in CRITERIA] + [("boundary", None)] + [("random", seed) for seed in design["random_seeds"]]
            for method, seed in selectors:
                # Exact JSON canonicalization may encode 10 as 1e1, parsed as
                # an integral Decimal. RNG controls require Python int values.
                seed = None if seed is None else int(seed)
                start = time.perf_counter_ns()
                if method in CRITERIA:
                    selected = greedy(index, method, budget=budget, fill=True)
                elif method == "boundary":
                    selected = generated["generation"]["priority_ids"][:budget]
                else:
                    selected = sorted(random.Random(seed).sample(list(index.ids), budget))
                selection_ns = time.perf_counter_ns() - start
                assert len(set(selected)) == budget
                selected_set = set(selected)
                killed = sum(bool(selected_set.intersection(m["killing_ids"])) for m in classified)
                row = {"subject": sid, "budget": declared_budget, "effective_budget": budget,
                       "method": method, "seed": seed, "selected_ids": sorted(selected),
                       "selection_ns": selection_ns,
                       "mutant_detectable": score(killed, len(detectable)),
                       "mutant_all": score(killed, len(classified))}
                for criterion in CRITERIA:
                    row[criterion] = score(len(index.covered(selected, criterion)), len(index.universes[criterion]))
                rows.append(row)
        print(sid, "pool", len(index.ids), "pairs", len(index.universes["independence"]),
              "reduced", reduced["reduction"]["selected_count"], flush=True)
    write(out / "subjects.json", subjects)
    write(out / "observations.json", rows)
    write(out / "summary.json", aggregate(rows, subjects))
    inputs = [ROOT / "requirements.lock", ROOT / "pyproject.toml", ROOT / "tools/run_experiments.py",
              ROOT / "tools/audit_artifacts.py"]
    for folder in ("schema_coverage_lab", "tests", "benchmarks", "vendor"):
        inputs.extend(p for p in (ROOT / folder).rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    source_hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)}
    artifacts = {str(p.relative_to(out)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in sorted(out.rglob("*")) if p.is_file() and p.name != "manifest.json"
                 and p.relative_to(out).parts[0] != "verification"}
    manifest = {"evidence_id": "E-0003", "status": "passed", "recorded_utc": datetime.now(timezone.utc).isoformat(),
                "command": "python tools/run_experiments.py", "base_commit": "c48fbe4ec1aa49f0b4bd2b8eb0797944981034fa",
                "environment": {"python": platform.python_version(), "system": platform.system(), "machine": platform.machine(), "oracle": environment()},
                "study_digest": digest(specification), "protocol_sha256": hashlib.sha256((ROOT / "benchmarks/README.md").read_bytes()).hexdigest(),
                "suite_commit": specification["suite_commit"], "source_sha256": source_hashes,
                "source_set_digest": hashlib.sha256(dumps(source_hashes).encode()).hexdigest(), "artifact_sha256": artifacts,
                "limitations": ["Selected synthetic/official-derived subjects", "Offline full-pool preprocessing",
                                "Pool-indistinguishable is not globally equivalent", "Greedy optimality not claimed",
                                "One tested platform; local observations differ from root mutation outcomes"]}
    write(out / "manifest.json", manifest)
    print("Completed", len(subjects), "subjects and", len(rows), "equal-budget rows")


if __name__ == "__main__":
    main()
