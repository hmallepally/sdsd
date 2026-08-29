"""
Demonstration harness showing prompt formatting differences
for Claude (XML), GPT-5 (System Messages), and Gemini (Structured JSON).
"""

def format_claude_prompt(task: str, invariants: list) -> str:
    xml_invariants = "\n".join(f"  <invariant>{inv}</invariant>" for inv in invariants)
    return f"""
<task_specification>
<instructions>{task}</instructions>
<invariant_wall>
{xml_invariants}
</invariant_wall>
</task_specification>
"""

def format_gpt5_payload(system_invariants: list, user_task: str) -> dict:
    formatted_invariants = "\n".join(f"- {inv}" for inv in system_invariants)
    return {
        "messages": [
            {
                "role": "system",
                "content": f"You are a secure code generator. ABSOLUTE INVARIANTS:\n{formatted_invariants}"
            },
            {"role": "user", "content": user_task}
        ]
    }

def format_gemini_schema() -> dict:
    return {
        "type": "object",
        "properties": {
            "code": {"type": "string"},
            "invariants_satisfied": {"type": "array", "items": {"type": "string"}},
            "blast_radius_verified": {"type": "boolean"}
        },
        "required": ["code", "invariants_satisfied", "blast_radius_verified"]
    }
