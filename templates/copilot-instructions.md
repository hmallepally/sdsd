# GitHub Copilot Repository Instructions (.github/copilot-instructions.md)

## Spec-Driven Secure Development Guidelines

When generating code for this repository:
1. **Always adhere to the Five Pillars of SDSD**:
   - Goal & Domain Context
   - Blast Radius Isolation
   - Invariants
   - State Machine Constraints
   - Negative Constraints (via Positive Reframing)

2. **Security Baselines**:
   - All REST endpoints must require authenticated tenant contexts via dependency injection.
   - Cache keys must use format: `f"cache:{tenant_id}:{resource_type}:{sha256_hash}"`.
   - Never write single-threaded unit tests when concurrent race conditions are possible. Always use `asyncio.gather`.
