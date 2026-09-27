---
name: devos-verify
description: Diagnose nontrivial bugs and verify behavior changes with reproduction, risk-based tests and concrete completion evidence.
---

# Evidence before claims

For a bug, reproduce the reported trigger before patching when feasible. Trace the narrow code path, collect relevant logs/state without secrets, state a falsifiable cause and test it. If reproduction is blocked, distinguish inference from confirmed cause. Avoid stacking unrelated speculative fixes. Prefer the smallest coherent correction, then re-run the original trigger and relevant regression checks. For difficult bugs, research competing hypotheses in parallel read-only agents and edit only after choosing the strongest; never let several debugging agents make speculative edits at once (user contract, section 17 of `devos-orchestrate` → `references/autonomous-software-engineering.md`).

Tests verify the implementation; they do not define reality. Never hardcode test-specific values, special-case fixtures, disable meaningful tests, silently weaken assertions, mock away the actual problem or bypass type or security checks without strong justification. If a test is genuinely wrong, fix the test (section 16).

For a feature, derive checks from user-observable requirements and risks, not implementation wording. Use existing tools/commands from package manifests and CI. Select useful unit, contract, integration or E2E tests; add a regression test when it would catch recurrence. Do not write mirror tests for a reversible copy/padding change or insist on arbitrary coverage percentages.

Exercise meaningful negative paths: malformed/empty input, failures and retries, unauthorized/cross-user access, cancellation, concurrency or stale state when applicable. Substantial UI or interaction changes require actual browser interaction and visual inspection at relevant widths via `devos-experience`, not only build output. For an isolated copy/style correction use a proportional local or visual check without loading the full experience workflow. Use the browser tools actually available in the session (see `devos-experience`) rather than remembered APIs. Use synthetic data for destructive paths.

A useful completion record is compact:

| Requirement/risk | Check actually executed | Observed result | Gap |
| --- | --- | --- | --- |
| Specific behavior | Command or interaction and environment | Pass/fail with evidence location | Concrete untested condition |

Inspect the final diff and working-tree status for unintended changes. For complex/high-risk work, ask an independent reviewer (`devos-reviewer`, plus `devos-security` for risk-bearing changes, briefed through `devos-orchestrate`) to examine the requirements, actual patch and relevant surrounding code; triage findings and rerun affected checks after fixes. Review commands or plugins available in the session (for example `/security-review` or a code-review plugin) can add a pass but do not replace a reviewer briefed with the requirements. Installed QA specialist agents (for example `api-tester`, `performance-benchmarker` or `accessibility-auditor`) may run a bounded check when briefed with this evidence contract. Keep tests tied to the final integrated version. Do not repeat a whole suite without a new reason.

Checks that were planned, skipped, mocked or only inspected must be labeled accordingly. Never claim a live provider, real device, independent review, performance score or production deployment was tested unless it was. Test execution can write artifacts even in a verification role: scope permitted directories and avoid destructive scripts or unauthorized services.
