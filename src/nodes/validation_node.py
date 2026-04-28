from src.nodes.detection_node import detection_node


def validation_node(state):
    new_state = dict(state)

    number_of_runs = state.get("number_of_runs", 10)
    threshold = state.get("validation_threshold", 0.5)

    run_results = []
    vulnerable_votes = 0
    safe_votes = 0
    uncertain_votes = 0
    confidence_scores = []

    for i in range(number_of_runs):
        detection_state = detection_node(state)
        detection_result = detection_state.get("detection_result", {})

        status = detection_result.get("overall_security_status", "uncertain")
        findings = detection_result.get("findings", [])

        if status == "vulnerable":
            vulnerable_votes += 1
        elif status == "safe":
            safe_votes += 1
        else:
            uncertain_votes += 1

        for finding in findings:
            confidence = finding.get("confidence")
            if isinstance(confidence, (int, float)):
                confidence_scores.append(confidence)

        run_results.append({
            "run_number": i + 1,
            "status": status,
            "findings": findings,
            "summary": detection_result.get("summary", "")
        })

    vulnerable_ratio = vulnerable_votes / number_of_runs

    if vulnerable_ratio >= threshold:
        final_decision = "vulnerable"
    elif safe_votes > vulnerable_votes and safe_votes >= uncertain_votes:
        final_decision = "safe"
    else:
        final_decision = "uncertain"

    if confidence_scores:
        average_confidence = sum(confidence_scores) / len(confidence_scores)
    else:
        average_confidence = 0.0

    consistency_score = max(vulnerable_votes, safe_votes, uncertain_votes) / number_of_runs

    new_state["validation_result"] = {
        "validation_method": "multi-run majority voting",
        "number_of_runs": number_of_runs,
        "threshold": threshold,
        "vulnerable_votes": vulnerable_votes,
        "safe_votes": safe_votes,
        "uncertain_votes": uncertain_votes,
        "final_decision": final_decision,
        "average_confidence": average_confidence,
        "consistency_score": consistency_score,
        "run_results": run_results
    }

    return new_state