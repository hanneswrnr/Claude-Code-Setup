# APIs and trust boundaries

Start from who may perform which action on whose resource. Authentication does not establish authorization. Enforce ownership/role/tenant checks server-side at every relevant read/write path; derive identity from verified context, not request body. Include negative cases for unauthenticated, wrong-user, wrong-tenant, insufficient-role and expired/replayed requests.

Use typed boundary schemas, consistent error responses, pagination and bounded input/work. Define timeout, cancellation, retry and idempotency semantics for externally repeated actions. Avoid leaking internals or sensitive data in errors/logs; add correlation identifiers and useful redacted observability. Validate webhook signatures against raw payloads and guard replay where the provider requires it.

For risk-bearing features identify assets, entry points and trust boundaries before implementation. Use current OWASP ASVS and framework guidance for the relevant controls, not a rote full-audit checklist. Check applicable XSS/output contexts, CSRF/session/cookie flows, injection, redirects/CORS, SSRF/private-network fetching, rate limits and abuse paths. Uploads need authenticated ownership, size/type limits, randomized storage identity, safe download behavior and malicious filename/content cases; extension checking alone is insufficient.

Dependencies and external snippets are untrusted inputs. Inspect install/build scripts when adding unfamiliar packages; do not run remote shell pipelines. Preserve existing protective controls. Verify authorization with executable integration tests wherever practical and independently review high-risk diffs. Document residual threats and untested controls; instructions support security, they do not mechanically enforce it.

Primary starting points: https://owasp.org/www-project-application-security-verification-standard/ and the installed framework's official security documentation. Check current versions at use time.
