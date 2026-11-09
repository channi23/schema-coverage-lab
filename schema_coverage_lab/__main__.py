"""Offline command-line entry point. Exit 0 success, 2 error, 3 unsupported."""

import argparse
import sys
from pathlib import Path

from .checks import check_fixtures, check_official
from .coverage import analyze, replay
from .jsonio import LIMITS, InputError, dumps, read


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m schema_coverage_lab")
    commands = parser.add_subparsers(dest="command", required=True)
    a = commands.add_parser("analyze")
    a.add_argument("--schema", required=True)
    a.add_argument("--corpus", required=True)
    a.add_argument("--domain", choices=["all_json", "candidate_pool"], default="all_json")
    a.add_argument("--output")
    r = commands.add_parser("replay")
    r.add_argument("--report", required=True)
    r.add_argument("--output")
    f = commands.add_parser("check-fixtures")
    f.add_argument("--input", required=True)
    f.add_argument("--output")
    o = commands.add_parser("check-official")
    o.add_argument("--directory", default="vendor/json-schema-test-suite")
    o.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        if args.command == "analyze":
            corpus = read(args.corpus)
            if (not isinstance(corpus, dict) or "instances" not in corpus or
                    set(corpus) - {"instances", "suite_ids"}):
                raise InputError("Corpus must contain instances and optional suite_ids")
            result = analyze(read(args.schema), corpus["instances"],
                             suite_ids=corpus.get("suite_ids"), domain=args.domain)
        elif args.command == "replay":
            result = replay(read(args.report))
        elif args.command == "check-fixtures":
            result = check_fixtures(read(args.input))
        else:
            result = check_official(args.directory)
        serialized = dumps(result) + "\n"
        if len(serialized.encode("ascii")) > LIMITS["input_bytes"]:
            raise InputError("Report exceeds replayable input byte limit")
        if args.output:
            Path(args.output).write_text(serialized, encoding="ascii")
        else:
            print(serialized, end="")
        return 3 if result.get("analysis_status") == "unsupported" else 0
    except (InputError, OSError, RecursionError, KeyError, TypeError) as exc:
        print(dumps({"analysis_status": "error", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
