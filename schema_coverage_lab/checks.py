"""Research-fixture and pinned official-subset verification."""

from pathlib import Path

from .coverage import analyze
from .jsonio import InputError, digest, read
from .oracle import Oracle, check_schema, environment
from .semantics import evaluate, support_issues


def check_fixtures(data):
    results = []
    for case in data["cases"]:
        schema = case["schema"]
        check_schema(schema)
        oracle = Oracle(schema)
        diagnostics = support_issues(schema)
        for i, test in enumerate(case["tests"]):
            actual = oracle.valid(test["instance"])
            if type(test["valid"]) is not bool or actual != test["valid"]:
                raise InputError("Research fixture disagreement: " + str(case.get("id", case.get("name"))))
            if diagnostics:
                result = analyze(schema, [{"id": "fixture", "value": test["instance"]}])
                if result["analysis_status"] != "unsupported":
                    raise InputError("Unsupported fixture was silently admitted")
            elif evaluate(schema, test["instance"]) != actual:
                raise InputError("Analyzer disagrees on research fixture")
            results.append({"case": case.get("id", case.get("name")), "test": i,
                            "valid": actual, "analyzer": "unsupported" if diagnostics else "supported"})
    return {"status": "passed", "catalog_digest": digest(data), "oracle": environment(),
            "tests": len(results), "results": results}


def check_official(directory):
    directory = Path(directory)
    manifest = read(directory / "manifest.json")
    selected, skipped = [], []
    for entry in manifest["files"]:
        import hashlib
        source = directory / entry["path"]
        if hashlib.sha256(source.read_bytes()).hexdigest() != entry["sha256"]:
            raise InputError("Official fixture file digest mismatch: " + entry["path"])
        groups = read(source)
        for group in groups:
            schema = group["schema"]
            check_schema(schema)
            diagnostics = support_issues(schema)
            if diagnostics:
                skipped.append({"file": entry["path"], "description": group["description"],
                                "tests": len(group["tests"]), "diagnostics": diagnostics})
                continue
            oracle = Oracle(schema)
            for test in group["tests"]:
                actual = evaluate(schema, test["data"])
                oracle_actual = oracle.valid(test["data"])
                if actual != test["valid"] or actual != oracle_actual:
                    raise InputError("Official suite disagreement: " + group["description"] + ": " + test["description"])
                selected.append({"file": entry["path"], "group": group["description"],
                                 "test": test["description"], "valid": actual})
    return {"status": "passed", "suite_commit": manifest["commit"], "oracle": environment(),
            "selected_tests": len(selected), "skipped_tests": sum(s["tests"] for s in skipped),
            "selected": selected, "skipped": skipped}
