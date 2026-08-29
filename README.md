# Spec-Driven Secure Development (SDSD)

[![SDSD Invariant Verification](https://github.com/hmallepally/sdsd/actions/workflows/sdsd-verify.yml/badge.svg)](https://github.com/hmallepally/sdsd/actions/workflows/sdsd-verify.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

Official companion repository for the book:
**Spec-Driven Secure Development: Architecting Resilient Systems in the Age of Autonomous AI Agents**  
by **Harinath Mallepally** (2026).

---

## 🎯 What is SDSD?

**Spec-Driven Secure Development (SDSD)** is an enterprise architectural framework designed to eliminate the risks of autonomous AI code generation (hallucinated packages, cross-tenant cache confusion, subtle race conditions, and silent invariant drift). 

SDSD replaces fuzzy natural-language user stories with **executable mathematical specifications** enforced through the **Five Pillars of SDSD**:

1. **Goal & Domain Context:** Unambiguous business intent with quantitative acceptance criteria.
2. **Blast Radius Definition:** Strict file, folder, and dependency firewalls.
3. **Invariants (The Invariant Wall):** Non-negotiable mathematical and architectural truths.
4. **State Machine Boundaries:** Guarded lifecycle transitions preventing unauthorized state jumps.
5. **Adversarial Threat Blueprints (Positive Reframing):** Negative constraint enforcement declaring approved secure pathways.

---

## 📂 Repository Structure

| Directory | Content Description | Relevant Book Chapters |
|:----------|:--------------------|:-----------------------|
| [`schemas/`](schemas/) | Master Five-Pillar JSON Schema & Domain contracts | Ch. 2, Ch. 14 (Appendix A) |
| [`templates/`](templates/) | `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md`, Prompt templates | Ch. 4, Ch. 7, Ch. 14 (Appendix B) |
| [`examples/python/`](examples/python/) | Python test suites (Hypothesis, FastAPI, AsyncIO, PyTest, Z3 SMT) | Ch. 1, 2, 3, 10, 11 (Python Edition) |
| [`examples/java/`](examples/java/) | Java test suites (Spring Boot, JUnit 5, Concurrent Ledgers) | Ch. 1, 2, 3, 10, 11 (Java Edition) |
| [`examples/csharp/`](examples/csharp/) | C# test suites (ASP.NET Core, xUnit, Concurrent Ledgers) | Ch. 1, 2, 3, 10, 11 (C# Edition) |
| [`sdsd.py`](sdsd.py) | CLI tool for prompt synthesis, AST auditing, and spec validation | Ch. 14 (Appendix C) |

---

## 🚀 Quickstart

### 1. Installation

Install the SDSD CLI directly via `pip` or `pipx`:

```bash
# Direct installation from GitHub
pip install git+https://github.com/hmallepally/sdsd.git

# Or clone and install in editable mode
git clone https://github.com/hmallepally/sdsd.git
cd sdsd
pip install -e .
```

### 2. Using the SDSD CLI Tool

```bash
# Initialize SDSD rules in your local repository for Cursor, Windsurf, Copilot
sdsd init --ide cursor,copilot,windsurf

# Generate a structured feature prompt with Blast Radius & Invariants
sdsd prompt create --type feature --target src/services/transfers/

# Validate an SDSD JSON specification against the meta-schema
sdsd spec validate schemas/aetherfi_transfer.schema.json

# Audit codebase for invariant violations (raw SQL, missing tenant_id)
sdsd audit --path src/
```

### 3. Running the Invariant Test Suites (Python)

```bash
# Install test dependencies
pip install pytest pytest-asyncio hypothesis pydantic z3-solver

# 1. Conservation of Mass invariant tests under high concurrency (asyncio.gather)
pytest examples/python/ch02_bulletproof_spec/test_concurrent_transfers.py -v

# 2. Cross-Tenant Cache Isolation tests (Preventing Cache Confusion)
pytest examples/python/ch01_caching_confusion/test_cache.py -v

# 3. SQL Injection & Tenant Isolation tests (Threat Blueprint)
pytest examples/python/ch03_threat_modeling/test_threat_mitigation.py -v

# 4. Property-Based Fuzzing with Hypothesis
pytest examples/python/ch10_testing_methodology/test_property_based.py -v

# 5. Formal Mathematical Invariant Proof with Microsoft Z3 SMT Solver
pytest examples/python/ch10_testing_methodology/test_z3_invariants.py -v
```

---

## 🛡️ The SDSD Fortress: Four Layers of Defense-in-Depth

```
+-----------------------------------------------------------------------------------+
| 1. Threat Blueprint & Blast Radius Filter (Scopes directory access & imports)     |
+-----------------------------------------------------------------------------------+
  |
  v
+-----------------------------------------------------------------------------------+
| 2. Strict Input Whitelisting & Pydantic Schema Validation                         |
+-----------------------------------------------------------------------------------+
  |
  v
+-----------------------------------------------------------------------------------+
| 3. Finite State Machine Transition Guards (Guarded lifecycle state transitions)   |
+-----------------------------------------------------------------------------------+
  |
  v
+-----------------------------------------------------------------------------------+
| 4. Mathematical Invariant Enforcement (Conservation of Mass, Zero-Trust Audit)    |
+-----------------------------------------------------------------------------------+
  |
  v
+===================================================================================+
|                        CORE PROTECTED FINANCIAL LEDGER                            |
+===================================================================================+
```

---

## 📖 Book Editions

* **Python Edition:** FastAPI, Pydantic v2, PyTest, Hypothesis, Redis AsyncIO, SQLAlchemy ORM.
* **Java Edition:** Spring Boot 3, Hibernate/JPA, JUnit 5, jqwik, Lettuce Reactive Cache.
* **C# Edition:** ASP.NET Core 9, Entity Framework Core, xUnit, FsCheck, StackExchange.Redis.

---

## 📄 License

This repository and all code samples are licensed under the [MIT License](LICENSE).
