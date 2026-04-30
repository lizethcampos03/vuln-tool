"""
Fix Node — Secure Code Generation

Purpose:
This node generates a secure version of the vulnerable code using
LLM guidance based on validated findings.

Inputs:
- cleaned_code
- validated findings

Outputs:
- fix_result:
    {
        fixed_code,
        fix_summary,
        explanation,
        remaining_risks
    }

Role in Pipeline:
Transforms detection into action by providing practical, secure
code fixes grounded in identified vulnerabilities.
"""
from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def fix_node(state):
    new_state = dict(state)

    validation_result = state.get("validation_result", {})
    detection_result = state.get("detection_result", {})
    code = state.get("cleaned_code", state.get("code", ""))
    rag_context = state.get("retrieved_context", "")

    final_decision = validation_result.get("final_decision", "uncertain")

    # 🚨 SAFETY: Do NOT generate fix if not vulnerable
    if final_decision != "vulnerable":
        new_state["fix_result"] = {
            "fix_generated": False,
            "fix_summary": "No fix generated because the validator did not confirm a vulnerability.",
            "fixed_code": code,
            "fix_explanation": "",
            "remaining_risks": []
        }
        return new_state

    # Extract first finding (we keep it simple for now)
    findings = detection_result.get("findings", [])
    finding_text = json.dumps(findings, indent=2)

    prompt = f"""
You are a secure code repair assistant.

Your job is to fix the vulnerability in the code based on validated findings.

IMPORTANT:
- Do NOT change the functionality of the code
- Only fix the security issue
- Keep the fix minimal and precise
- Do NOT introduce new libraries unless necessary

Original Code:
{code}

Validated Findings:
{finding_text}

Security Context:
{rag_context}

Return ONLY valid JSON in this format:

{{
  "fix_summary": "short description of what was fixed",
  "fixed_code": "the corrected code",
  "fix_explanation": "why this fix works",
  "remaining_risks": []
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        output_text = response.choices[0].message.content.strip()

        try:
            parsed = json.loads(output_text)
        except Exception:
            parsed = {
                "fix_summary": "Failed to parse fix output",
                "fixed_code": code,
                "fix_explanation": output_text,
                "remaining_risks": ["Parsing error"]
            }

        new_state["fix_result"] = {
            "fix_generated": True,
            **parsed
        }

    except Exception as e:
        new_state["fix_result"] = {
            "fix_generated": False,
            "fix_summary": "Fix generation failed",
            "fixed_code": code,
            "fix_explanation": str(e),
            "remaining_risks": ["LLM call failed"]
        }

    return new_state