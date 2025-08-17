# Acceptance Checklist – Burp Pro Spec (A–G)

This checklist is intended for QA and automated gatekeeping.

## Global Gates
- [ ] Uses only feature IDs from `burp_pro_spec.json`.
- [ ] All implemented features include unit/integration/smoke tests.
- [ ] Reverse verification report present and complete.

## Category A – Scanning
- [ ] scanner_full_crawl_audit: given start_urls and scan_configuration_id, then issues[] and logs are produced.
- [ ] scanner_targeted: given selected messages, then issues[] for those requests are produced.
- [ ] scanner_api_only: given api_endpoints[], produces issues[] without crawling pages.
- [ ] scanner_authenticated: recorded_login_sequence used; session maintained across scans.
- [ ] scanner_resource_pools: effective throttling seen in logs/metrics.
- [ ] scanner_live_tasks: continuous runs with adjustable params.
- [ ] scanner_results_views: all tabs render data.
- [ ] scanner_browser_powered: SPA navigation executed; client-side issues observable.
- [ ] scanner_bchecks: custom_issues produced from .bcheck files.

## Category B – Manual Tools
- [ ] proxy: intercept/modify works; history populated; WebSockets supported; Match & Replace applies.
- [ ] repeater: resend/edit requests; custom actions attach; AI suggestions consumable.
- [ ] intruder: all attack types run; payload processing; results filterable.
- [ ] target: site map populates; scope enforced; issue definitions visible.
- [ ] logger: filters apply; custom columns visible; extension requests visible.
- [ ] sequencer: tokens captured and analyzed; report generated.
- [ ] dom_invader: DOM tests produce signals; settings applied.
- [ ] clickbandit: PoC generated successfully.
- [ ] comparer/decoder: transformations and diffs accurate.
- [ ] engagement_tools: analyzer/content discovery/CSRF PoC/simulator run.
- [ ] infiltrator: probes reach sinks; collaborator signals correlate.
- [ ] organizer: items archived and tagged.
- [ ] search: workspace search returns expected results.
- [ ] context_menu/filter_settings: actions/filters reusable across tools.
- [ ] protocol_http2: HTTP/2 messages editable and sent.

## Category C – Burp AI (Pro)
- [ ] burp_ai_issues: AI explanations and test suggestions produced for a known issue.
- [ ] burp_ai_repeater: AI suggestions within Repeater tab appear and are actionable.
- [ ] burp_ai_recorded_logins: AI-assisted login sequence produced and reusable.
- [ ] burp_ai_extensions: at least one AI-enabled custom action/extension demo works.
- [ ] burp_ai_settings: privacy/credits policy toggles reflected in state.

## Category D – Extensibility
- [ ] bapp_store: install and remove an extension.
- [ ] montoya_api/extender_api_legacy: compile and load a simple extension.
- [ ] bambdas: create and invoke a custom action.
- [ ] rest_api: start a scan and query issues over REST.
- [ ] extensions_requests_logger: extension-originated requests visible.
- [ ] bchecks_ext: author/import bcheck and integrate with scan config.

## Category E – Projects & Files
- [ ] project_files: can create/open disk-based project; safety wizard behaves as expected.
- [ ] configuration_library: config items saved and referenced by ID.

## Category F – Settings
- [ ] Verify each listed Settings subpage is accessible and saves/restores options.

## Category G – Reporting
- [ ] reporting_scan_results: report generated with selected scope and filters; file present.
