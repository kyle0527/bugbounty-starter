#!/usr/bin/env python3
"""
normalize_scaffold.py
Normalize scaffold to the canonical "251-file" baseline by:
- Ensuring every feature's tests/ has __init__.py
- Optionally seeding unit/integration/smoke templates for 3 core features (idempotent)

Usage:
  python scripts/normalize_scaffold.py [--seed-tests]

This script must be run at repo root (where burp_pro_spec.json is).
"""

import os, sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "burp_pro_spec.json"

CORE_TEST_FEATURES = [
    ("A_SCANNING", "scanner_full_crawl_audit"),
    ("B_MANUAL_TOOLS", "proxy"),
    ("G_REPORTING", "reporting_scan_results"),
]

UNIT_TMPL = """import unittest

class TestUnit(unittest.TestCase):
    def test_placeholder(self):
        self.assertTrue(True)
"""

INTEG_TMPL = """import unittest

class TestIntegration(unittest.TestCase):
    def test_placeholder(self):
        self.assertTrue(True)
"""

SMOKE_TMPL = """def test_smoke():
    assert True
"""

def load_spec():
    if not SPEC.exists():
        print(f"[ERROR] Missing spec: {SPEC}", file=sys.stderr)
        sys.exit(1)
    return json.loads(SPEC.read_text(encoding="utf-8"))

def ensure_file(p: Path, content=""):
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text(content, encoding="utf-8")
        return True
    return False

def main():
    seed = "--seed-tests" in sys.argv
    spec = load_spec()
    created = []
    for f in spec["features"]:
        cat = f["category"]
        fid = f["id"]
        base = ROOT / "impl" / f"{cat}.{fid}" / "tests"
        changed = ensure_file(base / "__init__.py", "")
        if changed:
            created.append(str((base / "__init__.py").relative_to(ROOT)))

    if seed:
        for cat, fid in CORE_TEST_FEATURES:
            base = ROOT / "impl" / f"{cat}.{fid}" / "tests"
            if ensure_file(base / "test_unit.py", UNIT_TMPL): created.append(str((base / "test_unit.py").relative_to(ROOT)))
            if ensure_file(base / "test_integration.py", INTEG_TMPL): created.append(str((base / "test_integration.py").relative_to(ROOT)))
            if ensure_file(base / "test_smoke.py", SMOKE_TMPL): created.append(str((base / "test_smoke.py").relative_to(ROOT)))

    print("[normalize] created files:")
    for c in created:
        print("  +", c)
    print(f"[normalize] total created = {len(created)}")

if __name__ == "__main__":
    main()
