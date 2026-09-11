# Purposeful motion and 3D

Select the smallest technique that achieves the visual goal: CSS for simple transitions, the project's motion library for coordinated states, GSAP/scroll tooling for justified storytelling, Three.js/R3F for genuine spatial content. Check the installed version and primary API documentation before adding or changing libraries.

Define motion roles: orientation, feedback, state continuity and optional delight. Reuse durations/easing; let important content remain readable without animations. Honor `prefers-reduced-motion`: remove large movement, parallax and scroll-linked effects while preserving state information. Avoid scroll hijacking and pointer-only interactions. Provide keyboard/touch equivalents.

For scroll stories, verify sticky boundaries, browser resize, refresh mid-page, anchor navigation and mobile viewport changes. Prefer transform/opacity where suitable; avoid layout read/write loops. Pause work when offscreen or the tab is hidden. Limit simultaneous animation and test on constrained hardware where possible.

For 3D, define a visual budget before building: geometry, textures, lights, postprocessing and frame cost. Lazy-load heavy scenes, cap device-pixel ratio on mobile, dispose geometries/materials/textures/listeners, and handle context loss. Provide a static fallback for unsupported/reduced-motion contexts. Keep critical copy, links and controls in accessible DOM. Test loading/failure, touch, memory cleanup and resized layouts. Report which real device/browser conditions were exercised rather than promising universal frame rates.
