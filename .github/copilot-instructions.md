# .github/copilot-instructions.md
# Spec-Driven Secure Development Rules for GitHub Copilot

You are an AI pair programmer adhering to Spec-Driven Secure Development (SDSD):

## Directives
- **Tenant Isolation:** Every query MUST be scoped to `tenant_id`.
- **Concurrency Safety:** Apply atomic row locking (`SELECT FOR UPDATE`) on balance changes.
- **Verification First:** Before generating data-modifying code, output a conceptual PyTest asserting invariant adherence.
- **Negative Constraints:** Never swallow exceptions. Never use floating-point types for currency.
