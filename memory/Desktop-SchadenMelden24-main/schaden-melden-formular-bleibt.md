---
name: schaden-melden-formular-bleibt
description: "Entscheidung 2026-09-16 — das Schadenmelde-Formular der Versicherung/Vermittler bleibt wie es ist, kein neuer geführter Ablauf dort"
metadata: 
  node_type: memory
  type: project
  originSessionId: 10a4f912-c6fb-4fc9-863d-dda4ecf791af
  modified: 2026-09-16T12:47:32.644Z
---

Am 2026-09-16 hat der Nutzer im Brainstorm zu Auftragserstellung/-detail entschieden: Versicherungen und Vermittler brauchen keinen eigenen neuen Erstellungsablauf. Das Formular unter `app/(dashboard)/versicherung/schaden-melden/page.tsx` ist aus seiner Sicht sehr gut und bleibt so (kein Akkordeon-Stepper, keine Umstrukturierung).

**Why:** Das Formular funktioniert für die Zielgruppe; Umbau wäre Risiko ohne Nutzen.

**How to apply:** Vorschläge zur geführten Erstellung nur auf Werkstatt-Eigenauftrag (Modal in der Auftragsliste) und ggf. Spediteur beziehen. Kleine Konsistenz-Fixes am Versicherungsformular (z. B. Rollenfarbe statt fester Farbverläufe) nur nach ausdrücklicher Freigabe. Siehe [[abgabe-pruefliste-knoepfe-redirects]].
