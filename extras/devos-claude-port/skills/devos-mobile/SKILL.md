---
name: devos-mobile
description: Implement native or cross-platform mobile features with platform navigation, lifecycle, storage and device QA.
---

# Mobile delivery

Detect Expo/React Native, Flutter, Swift/iOS or Kotlin/Android from actual manifests; do not apply web layout rules blindly. Read installed version-specific primary docs and use available platform skills, plugins or specialist agents (for example an installed `mobile-app-builder` agent, briefed with DevOS ownership and return contracts). Preserve the app's navigation and state architecture.

Design around safe areas, virtual keyboard, touch targets, gestures, back behavior, focus and screen-reader semantics. Test form dismissal, navigation restoration, deep links and permission-denied paths. Consider foreground/background transitions, cancellation, offline/reconnect, stale data and low-memory cleanup where the feature depends on them.

Put credentials in platform secure storage, keep server secrets off devices and enforce authorization remotely. For push/deep-link flows validate identity and routing inputs. Use platform permission requests only for relevant capabilities with meaningful user context. AI, database and backend components follow the appropriate `devos-services` reference.

Run the project's lint/type/unit/integration/build checks. Exercise the affected journey in a real device or supported emulator/simulator, including orientation/font scaling when relevant; inspect rendered screens (for example capture emulator screenshots to files with the platform CLI and open them with Read). iOS simulator and Xcode builds require a compatible macOS host. On Windows, never claim native iOS verification from a browser preview; state the exact untested platform and provide the reproducible downstream check. Use Android tooling only when already available or justified by the project.

For high-risk or cross-system behavior request bounded independent review via `devos-orchestrate` (`devos-platform` for stack contracts, `devos-reviewer`/`devos-security` for review). Report tested platform/runtime/device, real interactions and remaining limitations.
