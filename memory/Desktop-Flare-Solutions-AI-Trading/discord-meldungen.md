---
name: discord-meldungen
description: "Discord-Server fuer die Trading-Agent-Meldungen, Versandweg ueber GitHub Actions, Geheimnisse und Sicherheitsentscheidungen"
metadata:
  node_type: memory
  type: project
  originSessionId: 04ac9823-fc1f-4a44-8f84-afe678386fd9
  modified: 2026-10-16T18:17:22.573Z
---

Discord-Server "Trading-Agent" (16.10.2026 per eingebautem Browser angelegt) mit Kanaelen #trades, #tagesbericht, #warnungen, #wochenbericht; je ein Webhook. Adressen liegen in den Windows-Benutzer-Umgebungsvariablen DISCORD_WEBHOOK_TRADES / _TAGESBERICHT / _WARNUNGEN / _WOCHENBERICHT und als GitHub-Geheimnisse im privaten Repo hanneswrnr/trading-agent-spielgeld (zusammen mit ANTHROPIC_API_KEY, KONTO_STORE_ID, AUSWERTUNG_STORE_ID). Nie im Chat ausgeben, nie in die Agenten-Cloud.

**Versandweg:** GitHub-Workflow `.github/workflows/meldungen.yml` stuendlich :38 -> src/relay.ts -> engine/melden.py (Nutzer bestaetigte "rund um die Uhr, auch bei PC aus"). Die lokale Windows-Aufgabe wurde danach entfernt. Der Haendler/Agenten senden nichts (Sicherheitspruefung H1: Versand aus der Sandbox waere per Prompt-Injection auslesbar gewesen).

**Why:** Anthropic-Tresor nimmt nur MCP-Zugaenge, daher kein Bot-Token; Webhook = geringstes Risiko. Texte deterministisch (kein freier KI-Text, Ausnahme bereinigte Pruefer-Kurzfassung woche_kurz.md).

**How to apply:** `gh secret set NAME --repo ... --body <Wert>` (NICHT per Pipe: ein angehaengter Zeilenumbruch machte den Wert ungueltig). Wird der API-Schluessel erneuert, auch das GitHub-Geheimnis neu setzen. Bei Webhook-Leck: Webhook in Discord loeschen/neu anlegen, lokale Variablen und GitHub-Geheimnisse neu setzen. Computer-Use-Freigabe fuer die Discord-App kam beim Nutzer nicht an; der eingebaute Browser funktionierte (Webhook-Adresse per Hook auf navigator.clipboard.writeText abgegriffen).

Siehe auch [[trading-agent-system]].
