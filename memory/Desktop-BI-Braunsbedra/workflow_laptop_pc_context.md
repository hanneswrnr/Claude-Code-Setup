---
name: Laptop/PC-Wechsel ueber Repo-.md-Dateien
description: User wechselt zwischen Laptop und PC; .md-Dateien im Repo sind sein Kanal fuer Kontext-Transfer zwischen den Geraeten und Sessions.
type: feedback
originSessionId: 8cc1199a-c1ea-4215-9c86-63177e973403
---
User arbeitet abwechselnd an Laptop und PC und nutzt die `.md`-Dateien im Repo (CLAUDE.md, PLAN.md, FOLLOWUPS.md, docs/**/*.md) bewusst als Kontext-Transfer-Mechanismus zwischen den Geraeten.

**Why:** Auto-Memory liegt pro Maschine lokal unter `C:\Users\hanne\.claude\...` und synchronisiert NICHT zwischen Laptop und PC. Nur was im Git-Repo landet, ist auf beiden Geraeten verfuegbar. Der User hat das explizit so festgelegt.

**How to apply:**
- Nicht-trivialer Session-Stand (Entscheidungen, geparkte Ideen, Blocker, naechste Schritte) gehoert in eine `.md`-Datei im Repo, nicht nur in Memory.
- **ALLE `.md`-Dateien im Hauptordner bleiben liegen.** Keine loeschen, verschieben oder in externe Systeme (GitHub-Issues, Notion, etc.) auslagern — auch nicht, wenn sie kurz oder redundant wirken. Der User hat das explizit geklaert.
- Vor Session-Uebergabe proaktiv daran erinnern: lokale Commits `git push`en. Der User schliesst aus "noch nicht beim anderen Geraet sichtbar" gelegentlich auf ".gitignore blockiert das" — kurz pruefen, ob Pull/Push fehlt statt Ignore-Regeln umzuschichten.
- Aktuelle .md-Landschaft im Repo-Root (Stand 2026-04-22): A11Y-AUDIT, BUGS, CLAUDE, DSGVO-AUDIT, FOLLOWUPS, Optimierung, PLAN, README, SECURITY-AUDIT, SECURITY-FOLLOWUPS, SUPABASE_SETUP.
