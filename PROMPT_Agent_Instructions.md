# Build Agent Prompt – Burp Suite Professional Spec (A–G)

**Spec file**: `burp_pro_spec.json` (version_tag: v2025-08-17, generated: 2025-08-17T18:45:42Z)

## Your Objective
Given the machine-readable spec, generate code, configuration, or artifacts that implement the requested subset of features.
Follow the evaluation rules and produce reverse-verification artifacts.

## Constraints
- Do not invent features that are not present in `burp_pro_spec.json`.
- Only treat `pro_only=true` where specified.
- Keep deliverables modular: one module per `feature.id` wherever practical.
- Provide test scaffolding for each module (unit, integration, smoke).

## Required Outputs
1. **Implementation plan**: ordered list of features to implement; include dependencies.
2. **Code skeletons**: one folder per feature_id; include README.md with usage.
3. **Tests**: per-feature tests; integrate a top-level test runner.
4. **Reverse verification**: CSV/JSON mapping feature_id -> implemented -> tests -> status.
5. **Docs**: SHORT USAGE for each feature (what, inputs, outputs, how to extend).

## Planning Heuristics
- Build from foundations: `E_PROJECTS_FILES.project_files` -> `B_MANUAL_TOOLS.proxy` -> `B_MANUAL_TOOLS.target` -> scanners -> reports.
- When a module depends on another (see `dependencies`), stub the dependency first.
- Reuse the `configuration_library` for any reusable settings.
- For AI features, ensure `settings_ai` baseline exists before invoking AI assistants.

## Acceptance Template (per feature)
- Unit: Validate function signatures and basic behaviors per `capabilities`.
- Integration: Validate data contracts with dependencies (e.g., `scanner_results_views` produces issues for `reporting_scan_results`).
- Smoke: End-to-end run using minimal config (see `inputs` -> `outputs`).

## Deliverable Structure Example
```
/impl
  /B_MANUAL_TOOLS.proxy
    proxy.py
    README.md
    tests/
  /A_SCANNING.scanner_full_crawl_audit
    crawl_audit.py
    README.md
    tests/
/tests
  run_all.py
/mapping
  coverage.json
/docs
  HOWTO.md
```
