---
name: devos-experience
description: Build or substantially redesign interfaces with deliberate visual direction, responsive interaction, motion and browser quality checks.
---

# Experience quality

Use for material UI creation/redesign, not every CSS or copy edit. Reuse the project's design system and available frontend/product-design skills or specialist agents when relevant (for example a `frontend-design` skill, or installed agents such as `ui-designer`, `ux-architect`, `frontend-developer` or `accessibility-auditor`, using the exact agent names the session lists); this workflow supplies the acceptance loop, not a competing UI framework. Respect an explicit visual reference and existing product identity.

## Web implementation preference

For websites and web apps, implement structure with semantic HTML and the visual design with CSS: layout, typography, colors, responsive rules and suitable animation. Implement interaction, state, validation and other application logic in TypeScript. HTML-producing framework templates and JSX/TSX are allowed; use CSS files, CSS Modules or an existing CSS design system for styling. Specialized SVG/WebGL content may complement the HTML/CSS interface when the product requires it; control its behavior with TypeScript. Apply this to new work without rewriting an existing application merely to change its language. Native apps and games follow their platform-appropriate stack.

## Establish direction before components

From the brief and available product context determine audience, key journey, content hierarchy, brand character and primary action. Choose a coherent typography scale, spacing/grid, color roles, surfaces, icon language and interaction hierarchy. State a short art-direction decision. When unspecified, make a reasoned reversible choice; do not invent a mandatory design approval meeting.

Compose around real content and product purpose. Avoid placeholder card grids, arbitrary gradients and component-library defaults when they weaken hierarchy. A dashboard should support decisions; a landing page should tell a concrete story. Empty/loading/error/success/disabled states are part of the design. Use real images or generated assets only when they help; preserve asset provenance and licensing. Claude Code has no built-in image generator (the Codex image generation plugin has no equivalent here): prefer supplied or licensed assets and SVG/CSS artwork, or a generation tool the user explicitly provides and authorizes.

## Implement behavior and responsive intent

Design for narrow screens explicitly: navigation, forms, charts/tables, sidebars, dialogs, safe areas and virtual keyboard. Keep content reachable at zoom and long translations. Prefer semantic HTML, labels, visible focus, keyboard operation and accessible dialog focus management. Announce asynchronous errors where necessary. Check contrast and touch targets using current WCAG guidance; automated checks alone cannot certify accessibility.

Use [motion and 3D](references/motion-3d.md) only when animation or a scene materially contributes to the requested experience. Do not add WebGL to ordinary CRUD as decoration.

## Render, inspect, improve

Choose the browser surface actually available in this session and load deferred tool schemas (ToolSearch) before the first call; do not assume a tool from another client or an old API exists. Typical surfaces: the desktop app's Browser pane (`mcp__Claude_Browser__*`: `preview_start` or `navigate`, screenshots, `read_page`, `resize_window` for viewport widths, console and network logs), Playwright MCP (`mcp__playwright__*`), Chrome DevTools MCP (performance traces), or Claude in Chrome (`mcp__claude-in-chrome__*`, which drives the user's own Chrome profile). The CLI usually has no Browser pane. Start the actual application with its documented command; run long-lived dev servers as background commands and stop them afterwards. Use mock/local data for unauthorized external actions.

Check representative narrow/mobile, tablet and desktop widths; a useful starting set is 390, 768 and 1440 CSS pixels, adapted to actual breakpoints. Inspect screenshots, not only DOM text. Exercise the main journey, navigation, forms, validation, overlays, empty/loading/error states, keyboard/focus and scroll. Check clipping, horizontal overflow, stacking and content density. Capture concrete defects, fix them, then repeat only affected checks. Reset temporary viewport overrides (Browser pane: `resize_window` preset `desktop`).

Measure performance proportional to the experience: image/font loading, layout shifts, largest content, interaction latency, bundle changes and mobile animation cost. Distinguish lab evidence from field Core Web Vitals. Do not fabricate Lighthouse scores or claim cross-browser coverage from one Chromium session.

Completion evidence identifies the route, tested widths, interactions, screenshot observations and remaining gaps. If the browser or runtime cannot start, diagnose it and report the blocker; build/typecheck passing does not establish visual quality.

For maintained web UI, use the available browser tools for real inspection and project-local Playwright for repeatable regression checks. Locate the source bundle web-kit through `<codex-home>/.devos/state.json` (`source_bundle`, subfolder `web-kit`) for a tested HTML/CSS/TypeScript gallery and QA example; adapt it to the product. Preserve reviewed screenshot baselines; do not regenerate them to hide regressions. Keep fonts and browser/OS stable for comparisons. Add axe checks for important states plus explicit keyboard/focus checks. Set performance budgets from measured evidence for heavy imagery/motion; no automatic analytics installation.
