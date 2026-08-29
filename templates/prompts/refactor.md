# SDSD Refactoring Spec Template

## 1. GOAL & CONTEXT
- **Goal:** [Describe the exact feature capability to implement]
- **Target Domain:** [e.g., Transfers / Billing / Authentication]
- **User Role:** [e.g., Authenticated Account Holder]

## 2. BLAST RADIUS
- **Allowed Directory Scope:** `src/services/[feature]/` and `tests/[feature]/`
- **Allowed Dependencies:** [e.g., `redis.asyncio`, `sqlalchemy.ext.asyncio`]
- **Forbidden Files:** `src/core/auth/`, `src/db/migrations/`

## 3. INVARIANTS
- **INV-001:** [e.g., All cache keys must include tenant_id]
- **INV-002:** [e.g., Sum of transfer debit and credit must equal zero]

## 4. STATE MACHINE
- **Initial State:** `INITIATED`
- **Transitions:** `INITIATED` -> `LOCKED` -> `COMMITTED` | `REVERTED`
- **Guards:** Balance check must pass before moving from `INITIATED` to `LOCKED`.

## 5. POSITIVE REFRAMING (CONSTRAINTS)
- For database queries: Use ONLY `select(Model).where(...)` with `AsyncSession`.
- For currency amounts: Use ONLY `Decimal` arithmetic.
