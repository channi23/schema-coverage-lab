"""Run the bounded milestone checks and save auditable, offline artifacts."""

import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from schema_coverage_lab.jsonio import dumps, read


def main():
    out = ROOT / "results/milestone-1"
    out.mkdir(parents=True, exist_ok=True)
    commands = [
        (["-m", "pytest", "-q"], "pytest.txt"),
        (["research-checks/check_semantic_model.py"], "finite-identities.txt"),
        (["-m", "schema_coverage_lab", "check-fixtures", "--input", "research-fixtures/schema-semantics.json"], "schema-fixtures.json"),
        (["-m", "schema_coverage_lab", "check-fixtures", "--input", "research-fixtures/semantic-counterexamples.json"], "counterexamples.json"),
        (["-m", "schema_coverage_lab", "check-official"], "official-subset.json"),
        (["-m", "schema_coverage_lab", "analyze", "--schema", "examples/conjunction.schema.json",
          "--corpus", "examples/conjunction.instances.json"], "example-report.json"),
        (["-m", "schema_coverage_lab", "replay", "--report", "results/milestone-1/example-report.json"], "replay.json"),
    ]
    # A failed rerun must not leave an earlier passing manifest/artifact set.
    for filename in [name for _, name in commands] + [name + ".stderr.txt" for _, name in commands] + ["manifest.json"]:
        (out / filename).unlink(missing_ok=True)
    executions = []
    failed = 0
    for args, filename in commands:
        result = subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)
        (out / filename).write_text(result.stdout, encoding="utf-8")
        if result.stderr:
            (out / (filename + ".stderr.txt")).write_text(result.stderr, encoding="utf-8")
        executions.append({"command": ["python", *args], "artifact": filename,
                           "exit_status": result.returncode,
                           "stderr": result.stderr})
        if result.returncode:
            print(result.stderr or result.stdout, file=sys.stderr)
            failed = result.returncode
            break
    inputs = [ROOT / "requirements.lock", ROOT / "pyproject.toml", ROOT / "tools/verify.py"]
    for folder in ("schema_coverage_lab", "tests", "research-checks", "research-fixtures", "vendor", "examples"):
        inputs.extend(p for p in (ROOT / folder).rglob("*")
                      if p.is_file() and "__pycache__" not in p.parts)
    source_hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in sorted(inputs)}
    manifest = {
        "evidence_id": "E-0002", "milestone": "bounded corpus analysis and independent replay",
        "status": "failed" if failed else "passed",
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "base_commit": "0d3411da47df952bbc1bd678db25cf658343c7a4",
        "source_sha256": source_hashes, "source_set_digest": hashlib.sha256(dumps(source_hashes).encode()).hexdigest(),
        "environment": {"python": platform.python_version(), "system": platform.system(),
                        "machine": platform.machine(), "packages": {name: importlib.metadata.version(name)
                        for name in ("attrs", "iniconfig", "jsonschema", "jsonschema-specifications", "packaging",
                                     "pluggy", "pygments", "pytest", "referencing", "rpds-py")}},
        "suite_commit": read(ROOT / "vendor/json-schema-test-suite/manifest.json")["commit"],
        "executions": executions,
        "artifact_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in sorted(out.iterdir()) if p.name != "manifest.json" and p.is_file()},
        "limitations": ["No generated corpus or suite optimizer", "No all-JSON feasibility solver",
                        "Pure-fragment subset only", "No comparative utility or mutation experiment",
                        "Tested runtime is Python 3.14.2 macOS arm64 only"],
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("Milestone checks " + ("failed" if failed else "passed") + "; artifacts in results/milestone-1")
    return failed


if __name__ == "__main__":
    raise SystemExit(main())
