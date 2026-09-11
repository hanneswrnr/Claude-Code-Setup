---
name: devos-services
description: Implement service APIs, database changes or LLM integrations with explicit contracts, trust boundaries and failure handling.
---

# Service delivery

Identify the existing stack, versions, public contracts and data ownership. Read only the references needed:

- API/business logic or security-sensitive behavior: [API and security](references/api-security.md).
- Schema, migrations, SQL, storage policies or tenant isolation: [Data](references/data.md).
- Chatbots, retrieval, LLM/tool integration: [AI engineering](references/ai.md).

Use available framework, Supabase, Stripe, OpenAI or Anthropic specialist skills, plugins or agents where genuinely applicable, with current tool/docs interfaces (for example the `claude-api` skill, or installed agents such as `backend-architect`, `database-optimizer`, `ai-engineer`, `api-tester` or `application-security-engineer`, briefed with DevOS ownership and return contracts). If absent, the relevant reference remains usable. A provider name is not a reason to install another MCP server or access production data.

Define validation and error contracts before frontend/backend parallel work. Keep secrets server-side and local fixtures synthetic. Test both success and denial/failure. For consequential changes, use the D-class workflow in `devos-orchestrate` with independent scrutiny. Prefer existing architecture and small coherent modules; introduce dependencies only for a concrete need.

State what was implemented, the actual checks run and operational assumptions. No deployment, live data mutation or third-party message is implicitly authorized by this skill.
