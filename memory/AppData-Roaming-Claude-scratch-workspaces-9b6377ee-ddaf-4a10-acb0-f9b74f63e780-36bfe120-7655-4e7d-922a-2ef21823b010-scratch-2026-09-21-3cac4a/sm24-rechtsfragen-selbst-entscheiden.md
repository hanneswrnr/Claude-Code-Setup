---
name: sm24-rechtsfragen-selbst-entscheiden
description: "SchadenMelden24 — Datenschutz-/Steuerrechtsfragen zu Daten und Löschung entscheidet Claude selbst, begründet mit Primärquellen, dokumentiert im Wiki"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 47f0339f-0e3c-46ed-848a-f0ec414fa721
  modified: 2026-09-22T23:15:18.049Z
---

Bei SchadenMelden24 hat der Product Owner am 22.09.2026 ausdrücklich gesagt: Was datenschutz- und steuerrechtlich (und an sonstigen Rechten Dritter) relevant ist, soll Claude selbst entscheiden — nicht zurückfragen.

**Why:** Der Nutzer ist kein Jurist und kein Entwickler; eine Rückfrage "a oder b?" bei Rechtsfragen blockiert ihn. Er will eine begründete Entscheidung, die umgesetzt ist.

**How to apply:** Rechtslage an Primärquellen prüfen (gesetze-im-internet.de; Fristen ändern sich, z. B. Buchungsbelege seit 2025 8 statt 10 Jahre), Entscheidung mit Paragrafen im Wiki festhalten (Muster: Abschnitt "Löschkonzept" in wiki/09-Operations/Security-Audits/2026-09-19-email-wechsel-passwortregeln.md), umsetzen, und im Bericht knapp den Hinweis geben, dass es keine Rechtsberatung ist. Weiterhin fragen bei Aktionen mit Außenwirkung, die nicht freigegeben sind. Siehe auch [[sm24-loeschkonzept]].
