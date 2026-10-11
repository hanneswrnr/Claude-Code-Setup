---
name: aria-props-bausteine-pr-304
description: "PR #304 (03.10.2026) – Select/DatePicker/TimePicker nehmen ariaDescribedBy/ariaInvalid an; MusterEingaben ohne Gruppen-Umweg; GEMERGT 03.10.2026 (b5c3f16e5)"
metadata:
  node_type: memory
  type: project
  originSessionId: 02ffe839-9e30-40d1-a8a5-48229c9483f2
  modified: 2026-10-03T11:37:29.216Z
---

PR #304, Zweig `fix/shared-controls-aria-describedby` (Commit 4a70ecf9d, 03.10.2026): Die gemeinsamen Bausteine `Select`, `DatePicker`, `TimePicker` haben optionale Props `ariaDescribedBy` und `ariaInvalid` (Select: am Trigger-Knopf; Picker: am Eingabefeld, interne Kurzmeldung wird angehängt). `MusterEingaben.tsx` nutzt sie, die `role="group"` als Umweg ist weg. Keine Migration. Mit Freigabe von Hannes gemergt am 03.10.2026, Merge-Commit b5c3f16e5. Folgeaufgabe 3 aus [[rechtsdokument-mustervorlagen-pr-303]].

**Why:** Screenreader lasen Hilfe/Fehler am fokussierten Feld nicht vor (WCAG 1.3.1, 3.3.1).

**How to apply:** Neue Formulare mit Select/Date/TimePicker und eigenen Hilfe-/Fehlertexten diese Props nutzen statt einer umgebenden Gruppe; roter Rahmen braucht weiter eine bereichseigene CSS-Regel (Galerie färbt mit `.bs-invalid` nur `.bs-input`). Offen als mögliche Folge: Ja/Nein, Segmente und Mehrfachauswahl hängen den Fehler weiter am `fieldset`; weitere Kandidaten laut Durchsicht `VerbundBeitritt.tsx`, `ZeitBlockenMaske.tsx`.
