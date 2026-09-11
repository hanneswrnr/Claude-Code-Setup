# Project web quality

Use HTML/CSS for design and TypeScript for application behavior including new web backend code. Start new projects with strict TypeScript; evaluate noUncheckedIndexedAccess. External data requires runtime validation, not a type assertion. Keep checks project-local and pin dependencies with the existing lockfile.

Interactive browser tools (the Claude desktop Browser pane, Playwright MCP, Chrome DevTools MCP or Claude in Chrome, whichever the session actually has) serve exploration, interactive diagnosis and visual judgment. Project-local Playwright tests provide stored repeatable E2E, accessibility and visual regression checks, including in CI. Use both when useful, and reuse existing project tooling. Do not install another browser MCP merely for Playwright.

Adopt from the DevOS source bundle web-kit (`source_bundle` in `<codex-home>/.devos/state.json`, subfolder `web-kit`) after reading its README: typecheck/build/unit+API checks, Playwright critical journeys and axe scans, responsive CSS examples, CI. New projects can use the example; existing projects merge only relevant configuration. Review install scripts before execution. Run the actual commands before documenting success.

Reference screenshots depend on OS/browser/fonts; create and compare in a consistent environment and inspect every baseline update. Test that a deliberate layout defect fails the affected check. Never auto-accept new screenshots to clear a failure. Keyboard/focus and actual visual inspection remain necessary; axe does not certify accessibility. Budget performance from measurements, and distinguish Lighthouse laboratory evidence from field metrics. No unrequested visitor telemetry.

CI should run required checks at the current commit, have bounded timeouts and preserve diagnostics on failure. Do not skip mandatory jobs based on changed paths or treat missing commands as pass. Configure remote branch rules only within repository authorization. No deployment credentials or automatic release are part of this kit.

Browsers execute JavaScript, not TypeScript source syntax. Keep authored functionality in .ts/.tsx and compile it to browser JavaScript, or use a development server that performs that transformation. Do not link a raw .ts file as a portable production script. Verify the served MIME type and actual browser behavior; JavaScript-compatible text inside .ts does not remove the build/runtime contract.
