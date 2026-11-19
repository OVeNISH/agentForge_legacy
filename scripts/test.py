"""One command: run unit tests, then integration tests; fail on empty suites."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main():
    for group in ("unit", "integration"):
        directory = ROOT / "tests" / group
        if not directory.is_dir():
            print(f"Missing {group} suite: {directory}", file=sys.stderr)
            return 2
        suite = unittest.TestLoader().discover(str(directory), pattern="test_*.py")
        if not suite.countTestCases():
            print(f"No {group} tests discovered", file=sys.stderr)
            return 2
        print(f"Running {group} tests", flush=True)
        if not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful():
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
