#!/usr/bin/env python3
"""
check_manifest.py
Verify scaffolded files against burp_pro_spec.json and the canonical "251-file" baseline.

Usage:
  python scripts/check_manifest.py [--strict] [--list] [--json]

Behavior:
- Reads burp_pro_spec.json in repo root.
- Computes expected canonical file set (251-file baseline):
  * For each feature: impl/<CATEGORY>.<feature_id>/{README.md, main.py, tests/__init__.py}
  * Top-level: PLAN.md, HOWTO.md, mapping/coverage.json, tests/run_all.py, .gitignore
  * Test templates (3 features): scanner_full_crawl_audit, proxy, reporting_scan_results
    -> test_unit.py, test_integration.py, test_smoke.py under each feature's tests/
- Compares with actual file set (prefers `git ls-files`; falls back to fs walk).

Exit codes:
  0 = OK (parity)
  1 = Mismatch
"""

import os, sys, json, subprocess, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "burp_pro_spec.json"

CORE_TEST_FEATURES = [
    ("A_SCANNING", "scanner_full_crawl_audit"),
    ("B_MANUAL_TOOLS", "proxy"),
    ("G_REPORTING", "reporting_scan_results"),
]

def load_spec():
    if not SPEC.exists():
        print(f"[ERROR] Missing spec: {SPEC}", file=sys.stderr)
        sys.exit(1)
    return json.loads(SPEC.read_text(encoding="utf-8"))

def expected_paths(spec, strict=False):
    exp = set()
    for f in spec["features"]:
        cat = f["category"]
        fid = f["id"]
        base = Path("impl") / f"{cat}.{fid}"
        exp.add(str(base / "README.md"))
        exp.add(str(base / "main.py"))
        exp.add(str(base / "tests" / "__init__.py"))
    # Top-level
    exp.update(["PLAN.md", "HOWTO.md", "mapping/coverage.json", "tests/run_all.py", ".gitignore"])
    # 3 core features with test templates
    for cat, fid in CORE_TEST_FEATURES:
        base = Path("impl") / f"{cat}.{fid}" / "tests"
        for name in ("test_unit.py", "test_integration.py", "test_smoke.py"):
            exp.add(str(base / name))
    return exp

def actual_paths():
    files = set()
    git_dir = ROOT / ".git"
    if git_dir.exists():
        try:
            out = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
            for line in out.splitlines():
                p = line.strip()
                if p:
                    files.add(p)
            return files
        except Exception:
            pass
    # Fallback to filesystem walk
    for dp, dn, fn in os.walk(ROOT):
        if ".git" in dp.split(os.sep):
            continue
        for name in fn:
            rel = os.path.relpath(os.path.join(dp, name), ROOT)
            files.add(rel.replace("\\", "/"))
    return files

def main():
    strict = "--strict" in sys.argv
    json_out = "--json" in sys.argv
    list_out = "--list" in sys.argv
    spec = load_spec()
    exp = expected_paths(spec, strict=strict)
    act = actual_paths()

    missing = sorted(x for x in exp if x not in act)
    extra = sorted(x for x in act if x not in exp)

    result = {
        "expected_count": len(exp),
        "actual_count": len(act),
        "missing": missing,
        "extra": extra,
    }

    if json_out:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[SUMMARY] expected={len(exp)} actual={len(act)}  delta={len(act)-len(exp)}")
        if missing:
            print("\n[MISSING]")
            for x in missing:
                print("  -", x)
        if extra and list_out:
            print("\n[EXTRA]")
            for x in extra:
                print("  +", x)

    sys.exit(0 if not missing else 1)

if __name__ == "__main__":
    main()
