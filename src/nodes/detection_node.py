"""
Detection Node — Vulnerability Analysis (LLM-Based)

Purpose:
This node analyzes input code to detect potential security vulnerabilities
using an LLM, guided by retrieved security knowledge (RAG).

Inputs:
- cleaned_code: Preprocessed source code
- retrieved_context: Relevant CWE/CVE knowledge

Outputs:
- detection_result:
    {
        overall_security_status,
        findings[],
        summary,
        false_positive_considerations
    }

Role in Pipeline:
This is the core intelligence layer where semantic understanding
is applied to identify vulnerabilities beyond simple pattern matching.
"""
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def detection_node(state):
    new_state = dict(state)

    code = state.get("cleaned_code", state.get("code", ""))
    application_context = state.get("application_context", "")
    rag_context = state.get("retrieved_context", state.get("rag_context", ""))

    prompt = f"""
You are a security vulnerability detection agent inside a LangGraph-based secure code analysis tool.

Your task is to analyze the provided code using:
1. The code itself
2. The application/business context
3. The retrieved CWE/CVE/security knowledge
4. The OWASP Top 10 categories

Focus especially on OWASP Top 10 vulnerabilities, including:
- Broken Access Control
- Cryptographic Failures
- Injection
- Insecure Design
- Security Misconfiguration
- Vulnerable and Outdated Components
- Identification and Authentication Failures
- Software and Data Integrity Failures
- Security Logging and Monitoring Failures
- Server-Side Request Forgery

Application Context:
{application_context}

Retrieved Security Knowledge:
{rag_context}

Code to Analyze:
{code}

Return your answer ONLY in valid JSON using this exact structure:

{{
  "overall_security_status": "vulnerable | safe | uncertain",
  "findings": [
    {{
      "finding_id": "FINDING-001",
      "owasp_category": "OWASP category name",
      "cwe_id": "CWE ID if known, otherwise unknown",
      "severity": "low | medium | high | critical",
      "confidence": 0.0,
      "vulnerability_name": "short name of the issue",
      "evidence_from_code": "specific code behavior or line/pattern that supports the finding",
      "why_it_is_dangerous": "clear explanation of the security risk",
      "business_impact": "explain the risk in the context of the application",
      "recommended_fix": "specific fix recommendation",
      "safe_alternative": "brief example or description of safer approach"
    }}
  ],
  "false_positive_considerations": [
    "explain any reasons this might not be exploitable"
  ],
  "summary": "short plain-English summary of the result"
}}

CRITICAL INSTRUCTION:

The retrieved security knowledge (CWE/CVE) is only contextual guidance.

You MUST base your final decision primarily on the actual code.

Do NOT label code as vulnerable just because a relevant CWE is retrieved.

Only mark "vulnerable" if the code itself clearly contains the vulnerability.

If the code demonstrates safe practices (e.g., parameterized queries), you must mark it as "safe" even if CWE-89 (SQL Injection) is present in the context.

Rules:
- If no vulnerability is found, return an empty findings list.
- Do not invent CWE IDs.
- Do not claim a vulnerability exists unless the code itself clearly supports it.
- Retrieved context is NOT proof of a vulnerability.
- The code behavior is the primary source of truth.
- If the code uses safe practices, mark it as "safe".
- Confidence should be between 0.0 and 1.0.
- Output valid JSON only."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        output_text = response.choices[0].message.content.strip()

        try:
            parsed_output = json.loads(output_text)
        except Exception:
            parsed_output = {
                "overall_security_status": "uncertain",
                "findings": [],
                "false_positive_considerations": [],
                "summary": "The model response could not be parsed as valid JSON.",
                "error": "Failed to parse LLM output",
                "raw_output": output_text
            }

        new_state["detection_result"] = parsed_output

    except Exception as e:
        new_state["detection_result"] = {
            "overall_security_status": "uncertain",
            "findings": [],
            "false_positive_considerations": [],
            "summary": "The detection node failed while calling the LLM.",
            "error": str(e)
        }

    return new_state