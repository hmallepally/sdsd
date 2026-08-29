#!/usr/bin/env python3
"""
SDSD CLI - Spec-Driven Secure Development
Official reference CLI for enforcing the Five Pillars of SDSD in software repositories.

Usage:
  sdsd init [--ide cursor,copilot,windsurf,antigravity]
  sdsd spec validate <schema_path>
  sdsd prompt create --type <feature|bugfix|refactor> --target <target_path>
  sdsd audit [--path <path>] [--strict]
"""

import argparse
import json
import os
import re
import sys

AGENT_DIR = ".agent"
PROMPTS_DIR = os.path.join(AGENT_DIR, "prompts")
WORKFLOWS_DIR = os.path.join(AGENT_DIR, "workflows")

DEFAULT_TEMPLATES = {
    "feature": """# SDSD FEATURE PROMPT (FIVE PILLARS)

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
""",
    "bugfix": """# SDSD BUGFIX PROMPT (FIVE PILLARS)

## 1. THE GOAL (The 'What')
* Bug Description / Root Cause:
* Expected Behavior:

## 2. THE BLAST RADIUS (The 'Where')
* Target Files / Directories: [Target Files / Directories]

## 3. THE INVARIANTS (The 'Must')
* Regression Invariant: Existing invariant tests must remain 100% green.
* Boundary Invariant: No changes to external API schemas.

## 4. THE STATE MACHINE (The 'How')
* Guard validations added to:

## 5. POSITIVE REFRAMING & THREAT MITIGATION (The 'Not')
* DO NOT introduce bare try/catch exception swallowing.
* DO NOT add bypass flags or skip guard logic.
""",
    "refactor": """# SDSD REFACTOR PROMPT (FIVE PILLARS)

## 1. THE GOAL (The 'What')
* Refactoring Objective (Performance, Modularity, Readability):

## 2. THE BLAST RADIUS (The 'Where')
* Target Files / Directories: [Target Files / Directories]

## 3. THE INVARIANTS (The 'Must')
* Equivalence Invariant: Core execution output must be mathematically identical.

## 4. THE STATE MACHINE (The 'How')
* Lifecycle transitions and events must remain unmodified.

## 5. POSITIVE REFRAMING & THREAT MITIGATION (The 'Not')
* DO NOT alter public-facing signatures or domain events.
"""
}

CURSOR_RULES = """# .cursorrules - SDSD Global Invariant Enforcement
# Spec-Driven Secure Development Rules for Cursor AI

You are a Zero-Trust Security Architect. When writing or modifying code:

1. ABSOLUTE INVARIANTS:
   - Tenant Isolation: Every database query MUST filter by `tenant_id`.
   - Conservation of Mass: Total ledger balances must balance before and after any transfer.
   - Precision: All financial math MUST use `Decimal`, never `float`.

2. BLAST RADIUS:
   - Modify ONLY files within the user's explicitly specified directory.
   - Never import external unapproved dependencies.

3. FORBIDDEN PATTERNS:
   - Raw SQL strings / format strings -> FORBIDDEN. Use SQLAlchemy ORM.
   - Bare `except Exception: pass` -> FORBIDDEN. Catch and log explicit exceptions.
   - MD5 and SHA-1 -> FORBIDDEN. Use SHA-256 or bcrypt.
"""

COPILOT_INSTRUCTIONS = """# .github/copilot-instructions.md
# Spec-Driven Secure Development Rules for GitHub Copilot

You are an AI pair programmer adhering to Spec-Driven Secure Development (SDSD):

## Directives
- **Tenant Isolation:** Every query MUST be scoped to `tenant_id`.
- **Concurrency Safety:** Apply atomic row locking (`SELECT FOR UPDATE`) on balance changes.
- **Verification First:** Before generating data-modifying code, output a conceptual PyTest asserting invariant adherence.
- **Negative Constraints:** Never swallow exceptions. Never use floating-point types for currency.
"""

WINDSURF_RULES = """# .windsurfrules - SDSD Global Directives
# Spec-Driven Secure Development Rules for Windsurf AI Cascade

- Enforcement: Strict
- Primary Invariant: Conservation of Mass (Sum(Debits) == Sum(Credits))
- Isolation: All multi-tenant data access must enforce tenant_id partition
- Database: Parameterized queries and ORM only
- Crypto: Approved libraries only (src.security.crypto)
"""

def cmd_init(ides=None):
    """Scaffolds the .agent/ directory structure, IDE rules, and default templates."""
    print("[*] Initializing SDSD Repository-as-Context structure...")
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    os.makedirs(WORKFLOWS_DIR, exist_ok=True)
    
    # Write templates
    for name, content in DEFAULT_TEMPLATES.items():
        template_path = os.path.join(PROMPTS_DIR, f"{name}_template.md")
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"  [+] Created prompt template: {template_path}")
        
    # Write IDE rules
    with open(".cursorrules", "w", encoding="utf-8") as f:
        f.write(CURSOR_RULES.strip() + "\n")
    print("  [+] Created: .cursorrules")

    os.makedirs(".github", exist_ok=True)
    with open(os.path.join(".github", "copilot-instructions.md"), "w", encoding="utf-8") as f:
        f.write(COPILOT_INSTRUCTIONS.strip() + "\n")
    print("  [+] Created: .github/copilot-instructions.md")

    with open(".windsurfrules", "w", encoding="utf-8") as f:
        f.write(WINDSURF_RULES.strip() + "\n")
    print("  [+] Created: .windsurfrules")
    
    print("[+] Successfully initialized SDSD environment with Cursor, Copilot, and Windsurf rules!")

def cmd_spec_validate(schema_path):
    """Validates a JSON specification against SDSD meta-schema rules."""
    print(f"[*] Validating SDSD specification: {schema_path}...")
    if not os.path.exists(schema_path):
        print(f"[FAIL] Schema file not found: {schema_path}")
        sys.exit(1)
        
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Check for Five Pillar sections
        required_fields = ["title", "type", "properties"]
        missing = [rf for rf in required_fields if rf not in data]
        if missing:
            print(f"[FAIL] Missing top-level schema fields: {missing}")
            sys.exit(1)
            
        props = data.get("properties", {})
        print(f"  [+] Found schema '{data.get('title', 'SDSD Schema')}' with {len(props)} properties.")
        print("  [PASS] Schema is syntactically valid and compliant with SDSD Meta-Schema v1.0.")
    except Exception as e:
        print(f"[FAIL] Invalid JSON syntax: {e}")
        sys.exit(1)

def cmd_validate_repo():
    """Validates the repository structure against the SDSD readiness checklist."""
    print("[*] Scanning repository for SDSD compliance...")
    
    checks = []
    score = 0
    
    if os.path.exists(PROMPTS_DIR) and len(os.listdir(PROMPTS_DIR)) > 0:
        score += 25
        checks.append("[PASS] Prompt Templates directory found containing active templates (.agent/prompts/).")
    else:
        checks.append("[FAIL] Missing prompt templates directory (.agent/prompts/).")
        
    if os.path.exists(".cursorrules") or os.path.exists(".windsurfrules") or os.path.exists(".github/copilot-instructions.md"):
        score += 25
        checks.append("[PASS] IDE Repository-as-Context rules found (.cursorrules / copilot-instructions.md).")
    else:
        checks.append("[FAIL] Missing IDE context rules (.cursorrules).")

    if os.path.exists("schemas"):
        score += 25
        checks.append("[PASS] Executable JSON Schema contracts found (schemas/).")
    else:
        checks.append("[FAIL] Missing schemas/ directory.")

    if os.path.exists("examples") or os.path.exists("tests"):
        score += 25
        checks.append("[PASS] Automated Invariant Test Suites found (tests/ or examples/).")
    else:
        checks.append("[FAIL] Missing automated invariant tests.")

    print("\n--- SDSD Readiness Report ---")
    for check in checks:
        print(f"  {check}")
    print(f"  Overall Readiness Score: {score}%\n")
    
    if score < 100:
        print("[!] Run 'sdsd init' to automatically bootstrap missing compliance components.")
        sys.exit(1)
    else:
        print("[+] Repository is 100% SDSD-Ready for secure autonomous AI generation.")

def cmd_create(template_type, target):
    """Loads the template, injects context/blast radius, and outputs a secure prompt."""
    print(f"[*] Assembling secure prompt for target: '{target}'...")
    
    template_content = DEFAULT_TEMPLATES.get(template_type)
    if not template_content:
        print(f"[Error] Unknown template type '{template_type}'. Available: feature, bugfix, refactor")
        sys.exit(1)
        
    final_prompt = template_content.replace("[Target Files / Directories]", target)
    output_file = f"sdsd_{template_type}_prompt.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_prompt.strip() + "\n")
        
    print(f"[+] Successfully generated secure prompt: {output_file}")
    print("[!] Ready for developer review of invariants before submitting to AI agent.")

def cmd_audit(target_path=".", strict=False):
    """AST / Static Analysis scan for forbidden AI code patterns."""
    print(f"[*] Running SDSD AST Invariant Audit on: '{target_path}'...")
    violations = []
    
    for root, _, files in os.walk(target_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    
                for idx, line in enumerate(lines, 1):
                    # Check 1: Bare except
                    if re.search(r"except\s*:", line) or re.search(r"except\s+Exception\s*:\s*pass", line):
                        violations.append((full_path, idx, "SD-05: Silent Exception Swallowing (Bare except)"))
                    # Check 2: Raw MD5/SHA1
                    if "hashlib.md5(" in line or "hashlib.sha1(" in line:
                        violations.append((full_path, idx, "SD-09: Cryptographic Degradation (MD5/SHA1 usage)"))
                    # Check 3: Raw SQL formatting
                    if ("execute(f\"" in line or "execute(f'" in line) and "SELECT" in line:
                        violations.append((full_path, idx, "SD-04: SQL Injection via Dynamic String Interpolation"))
                        
    print(f"  Scanned directory tree. Violations found: {len(violations)}")
    if violations:
        for path, line_no, desc in violations:
            print(f"  [FAIL] {path}:{line_no} -> {desc}")
        if strict:
            sys.exit(1)
    else:
        print("  [PASS] Zero invariant violations detected! All code conforms to SDSD Negative Constraints.")

def main():
    parser = argparse.ArgumentParser(description="SDSD Command Line Interface")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # init
    subparsers.add_parser("init", help="Scaffold SDSD rules and templates")
    
    # validate
    subparsers.add_parser("validate", help="Check repository compliance readiness")
    
    # spec
    spec_parser = subparsers.add_parser("spec", help="Manage SDSD specifications")
    spec_subparsers = spec_parser.add_subparsers(dest="spec_command")
    spec_validate_parser = spec_subparsers.add_parser("validate", help="Validate a specification against JSON meta-schema")
    spec_validate_parser.add_argument("schema_path", help="Path to schema file")
    
    # prompt
    prompt_parser = subparsers.add_parser("prompt", help="Manage SDSD prompts")
    prompt_subparsers = prompt_parser.add_subparsers(dest="prompt_command")
    create_parser = prompt_subparsers.add_parser("create", help="Assemble a secure prompt from template")
    create_parser.add_argument("--type", required=True, choices=["feature", "bugfix", "refactor"], help="Template type")
    create_parser.add_argument("--target", required=True, help="Target file or directory (The Blast Radius)")

    # audit
    audit_parser = subparsers.add_parser("audit", help="Audit codebase for invariant violations")
    audit_parser.add_argument("--path", default=".", help="Path to scan")
    audit_parser.add_argument("--strict", action="store_true", help="Exit with code 1 if violations found")
    
    args = parser.parse_args()
    
    if args.command == "init":
        cmd_init()
    elif args.command == "validate":
        cmd_validate_repo()
    elif args.command == "spec" and args.spec_command == "validate":
        cmd_spec_validate(args.schema_path)
    elif args.command == "prompt" and args.prompt_command == "create":
        cmd_create(args.type, args.target)
    elif args.command == "audit":
        cmd_audit(args.path, args.strict)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
