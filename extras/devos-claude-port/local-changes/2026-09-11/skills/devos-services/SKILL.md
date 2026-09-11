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

Define validation and error contracts before frontend/backend parallel work. Keep secrets server-side and local fixtures synthetic. Test both success and denial/failure. For consequential changes, use the D-class workflow in `devos-orchestrate` with independent scrutiny. Prefer existing architecture and small coherent modules; introduce dependencies only for a concrete need — before adding one, check whether the stack already covers it, whether it is mature and maintained, whether it materially simplifies the solution, its bundle, runtime and security cost, and whether an equivalent is already in use. Security is a default, not a final check. For every relevant service change evaluate authentication, authorization, input validation, API boundaries, secrets and environment variables, data exposure, database permissions and row-level security, session handling, CSRF, XSS, injection, SSRF, insecure direct object references, file uploads, dependency risks, rate limiting, webhook validation, privilege boundaries, error leakage and logging of sensitive data (section 15 of the user's orchestration contract, `devos-orchestrate` → `references/autonomous-software-engineering.md`; the controls are in the API and security and Data references above). Never weaken security to make tests pass.

State what was implemented, the actual checks run and operational assumptions. No deployment, live data mutation or third-party message is implicitly authorized by this skill.
