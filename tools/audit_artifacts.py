"""Audit hashes, budgets, raw metric numerators, and reduction replay."""

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from schema_coverage_lab.jsonio import read
from schema_coverage_lab.select import CRITERIA, EvidenceIndex, replay_reduction


def main():
    out = ROOT / "results/milestone-2"
    for location in (out, out / "verification"):
        manifest = json.loads((location / "manifest.json").read_text())
        assert manifest["status"] == "passed"
        for path, value in manifest["source_sha256"].items():
            assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == value, path
        for path, value in manifest["artifact_sha256"].items():
            assert hashlib.sha256((location / path).read_bytes()).hexdigest() == value, str(location / path)
    rows = json.loads((out / "observations.json").read_text())
    subjects = json.loads((out / "subjects.json").read_text())
    checked = 0
    for subject in subjects:
        case = out / "cases" / subject["subject"]
        index = EvidenceIndex(read(case / "pool-report.json"))
        mutants = read(case / "mutants.json")["mutants"]
        detectable = [m for m in mutants if m["killing_ids"]]
        replay_reduction(read(case / "reduced.json"))
        for row in [r for r in rows if r["subject"] == subject["subject"]]:
            ids = set(row["selected_ids"])
            assert len(ids) == len(row["selected_ids"]) == row["effective_budget"]
            assert len(ids) == min(row["budget"], len(index.ids))
            assert ids <= set(index.ids)
            for criterion in CRITERIA:
                recorded = row[criterion]
                numerator = len(index.covered(ids, criterion))
                denominator = len(index.universes[criterion])
                assert recorded == ({"numerator": numerator, "denominator": denominator} if denominator else None)
            killed = sum(bool(ids.intersection(m["killing_ids"])) for m in mutants)
            for name, denominator in (("mutant_all", len(mutants)), ("mutant_detectable", len(detectable))):
                assert row[name] == ({"numerator": killed, "denominator": denominator} if denominator else None)
            checked += 1
    result = {"status": "passed", "source_and_artifact_hashes": "matched",
              "subjects": len(subjects), "equal_budget_rows_audited": checked,
              "reductions_replayed": len(subjects),
              "limits": "Consistency audit of recorded finite-pool evidence; not a new global correctness proof"}
    destination = ROOT / "results/audits/milestone-2.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
