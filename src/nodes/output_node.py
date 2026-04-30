"""
Output Node — Final Security Report Generation

Purpose:
This node compiles all results into a structured, human-readable
and experiment-ready security audit report.

Inputs:
- detection results
- validation results
- fix results
- retrieved sources

Outputs:
- final_report:
    {
        executive_summary,
        security_findings,
        fix_recommendation,
        validation_evidence,
        audit_trail,
        comparison_ready
    }

Role in Pipeline:
Presents the full analysis in a clear, trustworthy format suitable
for security experts, developers, and experimental evaluation.
"""
def output_node(state):
    new_state = dict(state)

    detection = state.get("detection_result", {})
    validation = state.get("validation_result", {})
    fix = state.get("fix_result", {})
    retrieved_sources = state.get("retrieved_sources", [])

    final_status = validation.get("final_decision", "uncertain")
    consistency_score = validation.get("consistency_score", 0.0)
    avg_conf = validation.get("average_confidence", 0.0)

    findings = detection.get("findings", [])

    if final_status == "vulnerable":
        risk_level = "high"
        summary_text = "A security vulnerability was detected and validated in the code."
        action = "Apply the recommended fix and perform a brief manual verification before deployment."
        confidence_reason = "The validator repeatedly confirmed the vulnerability across multiple runs."
    elif final_status == "safe":
        risk_level = "low"
        summary_text = "No security vulnerabilities were confirmed after analysis."
        action = "No immediate action required, but periodic security review is recommended."
        confidence_reason = "The validator did not confirm a vulnerability across the analysis runs."
    else:
        risk_level = "medium"
        summary_text = "The analysis was inconclusive."
        action = "Manual review is recommended before trusting the code in production."
        confidence_reason = "The validation results were not strong enough to make a confident final decision."

    key_findings = []
    for f in findings:
        key_findings.append({
            "vulnerability": f.get("vulnerability_name"),
            "severity": f.get("severity"),
            "owasp_category": f.get("owasp_category"),
            "cwe_id": f.get("cwe_id"),
            "confidence": f.get("confidence"),
            "evidence_from_code": f.get("evidence_from_code"),
            "why_it_matters": f.get("why_it_is_dangerous"),
            "business_impact": f.get("business_impact"),
            "recommended_fix": f.get("recommended_fix")
        })

    fix_section = {
        "fix_generated": fix.get("fix_generated", False),
        "summary": fix.get("fix_summary", ""),
        "fixed_code": fix.get("fixed_code", ""),
        "explanation": fix.get("fix_explanation", ""),
        "remaining_risks": fix.get("remaining_risks", [])
    }

    validation_section = {
        "method": validation.get("validation_method"),
        "runs": validation.get("number_of_runs"),
        "threshold": validation.get("threshold"),
        "vulnerable_votes": validation.get("vulnerable_votes"),
        "safe_votes": validation.get("safe_votes"),
        "uncertain_votes": validation.get("uncertain_votes"),
        "final_decision": final_status,
        "consistency_score": consistency_score,
        "average_confidence": avg_conf,
        "confidence_reason": confidence_reason
    }

    issue_label = "validated security issue" if len(findings) == 1 else "validated security issues"

    audit_trail = {
        "nodes_completed": [
            "rag_node",
            "detection_node",
            "validation_node",
            "fix_node",
            "output_node"
        ],
        "retrieved_sources": retrieved_sources,
        "decision_path": [
            f"RAG retrieved {len(retrieved_sources)} relevant security source(s).",
            f"Detection identified {len(findings)} {issue_label}.",
            f"Validation reached '{final_status}' with {validation.get('vulnerable_votes')} vulnerable vote(s), "
            f"{validation.get('safe_votes')} safe vote(s), and {validation.get('uncertain_votes')} uncertain vote(s).",
            f"Consistency score was {consistency_score}.",
            f"Fix generation executed: {fix.get('fix_generated', False)}."
        ],
        "trust_note": (
            "This report is intended to assist security review, not replace human judgment. "
            "Manual verification is recommended before production use."
        )
    }

    comparison_fields = {
        "owasp_category": findings[0].get("owasp_category") if findings else "",
        "cwe_id": findings[0].get("cwe_id") if findings else "",
        "predicted_label": final_status,
        "consistency_score": consistency_score,
        "average_confidence": avg_conf,
        "ready_for_codeql_comparison": True,
        "ready_for_bandit_comparison": True,
        "ready_for_paper_method_comparison": True
    }

    report = {
        "report_type": "security_audit_report",
        "executive_summary": {
            "final_status": final_status,
            "risk_level": risk_level,
            "confidence": avg_conf,
            "confidence_reason": confidence_reason,
            "plain_english_summary": summary_text,
            "recommended_next_action": action
        },
        "security_findings": key_findings,
        "fix_recommendation": fix_section,
        "validation_evidence": validation_section,
        "audit_trail": audit_trail,
        "comparison_ready": comparison_fields
    }

    new_state["final_report"] = report

    return new_state