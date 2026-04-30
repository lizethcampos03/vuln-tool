# Testing Strategy

## Purpose
This document defines how the vulnerability detection pipeline is tested to ensure correctness, consistency, and reliability across all components.

The goal is to validate that each node performs its intended function and that the full pipeline produces trustworthy security analysis outputs.

---

## Testing Approach

The system is tested at two levels:

### 1. Unit Testing (Node-Level)
Each node in the pipeline is tested independently to verify its functionality in isolation.

### 2. Integration Testing (Pipeline-Level)
The full pipeline is executed end-to-end to ensure proper interaction between nodes and correct final outputs.

---

## Node-Level Testing

Each node has a corresponding test file located in the `/tests` directory.

### Input Node
**Test File:** `test_input_node.py`  
**Purpose:**
- Ensures raw input is correctly structured
- Verifies default values (e.g., `file_name = unknown.py`)
- Confirms required fields (`code`, `context`) are preserved

---

### Preprocess Node
**Test File:** `test_preprocess_node.py`  
**Purpose:**
- Validates code cleaning (whitespace removal)
- Ensures `cleaned_code` is correctly generated
- Confirms no unintended modification of logic

---

### RAG Node
**Test File:** `test_rag_node.py`  
**Purpose:**
- Verifies retrieval of relevant CWE/CVE context
- Confirms proper formatting of retrieved data
- Ensures fallback behavior when no relevant context is found

---

### Detection Node
**Test File:** `test_detection_node.py`  
**Purpose:**
- Validates vulnerability detection logic
- Ensures structured output (JSON format)
- Confirms inclusion of:
  - vulnerability type
  - reasoning
  - confidence score

---

### Validation Node
**Test File:** `test_validation_node.py`  
**Purpose:**
- Tests multi-run majority voting mechanism
- Verifies:
  - vote aggregation
  - threshold logic (e.g., 50%)
  - consistency scoring
- Ensures reduction of false positives

---

### Fix Node
**Test File:** `test_fix_node.py`  
**Purpose:**
- Confirms secure code generation
- Ensures fixes align with detected vulnerabilities
- Verifies explanation and summary clarity

---

### Output Node
**Test File:** `test_output_node.py`  
**Purpose:**
- Validates final report structure
- Ensures all sections are present:
  - executive summary
  - findings
  - validation evidence
  - fix recommendation
  - audit trail
- Confirms consistency for comparison with external tools (CodeQL, Bandit)

---

## Integration Testing

The full pipeline is tested via:
python -m src.main


### Validation Criteria:
- All nodes execute in correct sequence
- State is correctly passed between nodes
- Final report is complete and structured
- Outputs are logically consistent

---

## Test Scenarios

### Vulnerable Code
- SQL Injection (primary test case)
- Hardcoded credentials (planned)
- Weak cryptography (planned)

### Safe Code
- Clean, parameterized queries
- Proper validation and sanitization

---

## Evaluation Goals

The testing strategy ensures the system:

- Detects real vulnerabilities accurately
- Minimizes false positives
- Provides clear explanations
- Generates actionable fixes
- Produces consistent results across runs

---

## Future Testing Improvements

- Expand dataset coverage (CWE/CVE)
- Automate benchmark comparisons (CodeQL, Bandit)
- Introduce edge-case testing
- Add performance evaluation metrics