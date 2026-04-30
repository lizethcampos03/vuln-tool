# Node Contracts — Vulnerability Detection Tool

## Global State

This defines the data shared across all nodes.

- code: string
- context: string
- cleaned_code: string
- retrieved_knowledge: list
- detection_results: list
- validation_result: dict
- fix_suggestions: list
- final_report: dict

---

## 1. Input Node

Purpose:
Receives initial input.

Input:
- raw code
- context

Output:
- code
- context

---

## 2. Preprocessing Node

Purpose:
Cleans and prepares code.

Input:
- code
- context

Output:
- cleaned_code

---

## 3. RAG Node

Purpose:
Retrieve vulnerability knowledge.

Input:
- cleaned_code
- context

Output:
- retrieved_knowledge

---

## 4. Detection Node (Multi-run)

Purpose:
Detect vulnerabilities using LLM.

Input:
- cleaned_code
- retrieved_knowledge
- context

Output:
- detection_results
  - list of:
    - vulnerability
    - reasoning
    - confidence

---

## 5. Validation Node (Aggregation + Threshold)

Purpose:
Combine results and decide final outcome.

Input:
- detection_results

Output:
- validation_result
  - vulnerability_detected (true/false)
  - confidence_score
  - explanation

---

## 6. Fix Generation Node

Purpose:
Generate fixes.

Input:
- validation_result
- cleaned_code

Output:
- fix_suggestions

---

## 7. Output Node

Purpose:
Generate final report.

Input:
- validation_result
- fix_suggestions

Output:
- final_report


---

## Output Format Standards

### Detection Result Format (per run)

Each detection run should output:

{
  "vulnerability": "string",
  "reasoning": "string",
  "confidence": float
}

---

### Detection Results (all runs)

{
  "runs": [
    { detection_result },
    { detection_result },
    ...
  ]
}

---

### Validation Result Format

{
  "vulnerability_detected": true/false,
  "confidence_score": float,
  "agreement_ratio": float,
  "explanation": "string"
}

---

### Fix Suggestion Format

{
  "issue": "string",
  "fix": "string",
  "improved_code": "string"
}

---

### Final Report Format

{
  "summary": "string",
  "vulnerabilities": [],
  "confidence": float,
  "fixes": []
}