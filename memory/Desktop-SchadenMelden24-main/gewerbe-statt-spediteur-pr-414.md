---
name: gewerbe-statt-spediteur-pr-414
description: "Spediteur heißt sichtbar Gewerbe/Gewerbekunde; PR #414 am 17.10.2026 in sammel/verbesserungen gemergt; Datenschutzerklärung am selben Tag nachgezogen"
metadata:
  node_type: memory
  type: project
  originSessionId: 0fc11645-2017-4545-b96e-4f3501826b78
  modified: 2026-10-17T12:07:11.748Z
---

Chat 4 des Verbesserungspakets: Am 17.10.2026 hat Hannes entschieden, dass die Rolle „Gewerbe“ heißt, eine einzelne Firma „Gewerbekunde“ und die Liste „Gewerbekunden“. Die Adressen sind jetzt /gewerbe, /register/gewerbe und /werkstatt/gewerbekunden; die alten leiten mit 308 weiter. Intern bleibt `flottenkunde`, auch die API-Pfade unter spediteure. ADR 0041.
PR #414 ist am 17.10.2026 in `sammel/verbesserungen` gemergt (b214ce45f). Keine Migration.

**Why:** Im Werkstatt-Call fiel auf, dass „Spedition“ irreführend war ([[version-4-0-sammelzweig]]).

**How to apply:**
- Neue Texte sagen „Gewerbe“ bzw. „Gewerbekunde“ (schwach gebeugt: „den Gewerbekunden“).
- Rechtstexte: Hannes 17.10.2026 „überall wo Spediteur stand muss jetzt Gewerbe/Gewerbekunde stehen“. Datenschutzerklärung umgestellt (PR #415, am 17.10.2026 in sammel/verbesserungen gemergt, 5cd8d1c63; Stand 17. Oktober 2026; Einwilligungsversion bewusst gleich); ein Wächter in `lib/legal/rechtsseiten-ohne-platzhalter.test.ts` hält die Rechtsseiten frei von Spedit…/Flottenkund…. Die verschickte AGB-Mitteilung bleibt als Nachweis.
- „Gewerbekunde“ (Abzeichen in der Werkstatt) und „Firma“ (Kundenkartei) sind laut Hannes verschiedene Dinge: nicht angleichen.
- Die Rundgang-Texte ändert Chat 5.
- Ältere Zweige, die den alten Ordner `app/(dashboard)/spediteur/` ändern, holen den Stand mit `merge.directoryRenames=true` herein.
