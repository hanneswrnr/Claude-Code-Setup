---
name: Lucide 0.563 Icon-Namen (PascalCase-Umbenennung)
description: Fallstricke bei dynamischen Lucide-Icon-Lookups via `icons[name]` in DynamicLucideIcon
type: project
originSessionId: 1a61b6b4-b24f-40bf-a3c7-35043a547ad4
---
lucide-react 0.563 hat viele Icon-Namen umbenannt. Nur die **neuen** PascalCase-Namen liegen im `icons`-Registry (`Object.keys(L.icons)`). Die alten Namen existieren zwar noch als direkte Named Exports (`import { HelpCircle }`), sind aber **nicht** in `L.icons` auffindbar.

**Why:** `src/components/content/DynamicLucideIcon.tsx` macht `icons[name]`-Lookup. Ein in der DB gespeicherter Key wie `Home` oder `CheckCircle` rendert dort die HelpCircle-Fallback-Icon, nicht das eigentliche Icon.

**How to apply:** Für `iconCatalog.ts` und jeden anderen Code-Pfad, der einen Icon-String persistiert, nur Namen aus `Object.keys(L.icons)` verwenden. Mapping wichtiger Umbenennungen:

- `Home` → `House`
- `HelpCircle` → `CircleQuestionMark` (nicht `CircleHelp`)
- `CheckCircle` → `CircleCheck`
- `CheckCircle2` → `CircleCheckBig`
- `AlertCircle` → `CircleAlert`
- `AlertTriangle` → `TriangleAlert`
- `FileSignature` → `Signature`

Der iconCatalog-Test (`iconCatalog.test.ts`) validiert alle Keys per Runtime-Check gegen `L.icons` und fängt zukünftige Regressions.
