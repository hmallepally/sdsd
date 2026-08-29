# SDSD FEATURE PROMPT (FIVE PILLARS)

## 1. THE GOAL (The 'What')
* Target feature functionality: 
* Business acceptance criteria:

## 2. THE BLAST RADIUS (The 'Where')
* Target Files / Directories: [Target Files / Directories]
* Forbidden Modules / Paths: ["infrastructure/*", "migrations/*", "*.env"]

## 3. THE INVARIANTS (The 'Must')
* Invariant 1 (Conservation): Total balances must remain equal across transactions.
* Invariant 2 (Isolation): All queries MUST include tenant_id filter.
* Invariant 3 (Precision): All monetary amounts must use Decimal with 4 decimal places.

## 4. THE STATE MACHINE (The 'How')
* Allowed states: DRAFT -> PENDING_APPROVAL -> SETTLED -> ARCHIVED
* Forbidden transitions: DRAFT -> SETTLED (Direct bypass)

## 5. POSITIVE REFRAMING & THREAT MITIGATION (The 'Not')
* Cryptography: Use src.security.crypto with bcrypt / AES-256-GCM.
* Database: Parameterized SQLAlchemy ORM models exclusively. No raw string SQL.
* Concurrency: Atomic SELECT FOR UPDATE with bounded asyncio.gather pool.
