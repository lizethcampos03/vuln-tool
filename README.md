# LLM-Based Security Vulnerability Detection & Repair Tool

A LangGraph-powered system for detecting, validating, and fixing security vulnerabilities in code using LLMs and structured security knowledge (CWE/CVE).

---

## Overview

This project introduces a structured pipeline for secure code auditing using large language models.

The system:
- Detects vulnerabilities in source code
- Uses contextual information and security knowledge (RAG)
- Validates results through multi-run consistency checks
- Generates secure fixes using LLMs
- Produces a structured, human-readable security report

---

## Motivation

Traditional static analysis tools (e.g., CodeQL, Bandit) rely heavily on pattern matching and predefined rules.

This project explores a different approach:

Can LLMs, when properly structured and grounded, act as reliable security auditors?

Key goals:
- Improve detection of complex vulnerabilities
- Reduce false positives
- Provide actionable fixes
- Increase trust through validation and transparency

---

## System Architecture

The system is built as a modular pipeline using LangGraph:


Input → Preprocess → RAG → Detection → Validation → Fix → Output


Each stage is implemented as a node with a specific responsibility.

---

### Pipeline Overview

[ Input ]
↓
[ Preprocess ]
↓
[ RAG (CWE/CVE Knowledge) ]
↓
[ Detection (LLM) ]
↓
[ Validation (Multi-run Voting) ]
↓
[ Fix Generation (LLM) ]
↓
[ Output Report ]

---

## Pipeline Breakdown

| Stage        | Purpose                                       |
|--------------|-----------------------------------------------|
| Input        | Receives raw code and contextual information  |
| Preprocess   | Cleans and standardizes code                  |
| RAG          | Retrieves relevant CWE/CVE security knowledge |
| Detection    | LLM identifies potential vulnerabilities      |
| Validation   | Multi-run majority voting for consistency     |
| Fix          | LLM generates secure version of the code      |
| Output       | Builds final structured security report       |

---

## Project Structure


vuln-tool/
├── src/
│ ├── nodes/ # Core pipeline logic
│ ├── rag/ # Security knowledge retrieval
│ ├── graph.py # LangGraph workflow
│ └── main.py # Entry point
│
├── tests/ # Node-level testing
├── experiments/ # Evaluation (Phase 2)
├── docs/ # Architecture and methodology
│
├── README.md
├── requirements.txt
├── langgraph.json
└── .gitignore


---

## How to Run

1. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
2. Install dependencies
pip install -r requirements.txt

3. Add API keys
Create a .env file:
OPENAI_API_KEY=your_key_here
LANGSMITH_API_KEY=your_key_here
LANGSMITH_TRACING=true

4. Run the pipeline
python -m src.main

Example Output:
The system generates a structured security report including:
Executive summary
Vulnerability findings
CWE mapping
Secure fix recommendations
Validation evidence
Audit trail

Experiments (Phase 2)
Planned experiments:
Comparison vs CodeQL
Comparison vs Bandit
Comparison vs end-to-end LLM pipeline 
OWASP Top 10 evaluation

Future Work:
Expand CWE/CVE coverage
Improve RAG retrieval quality
Add iterative fix-validation loop
Optimize performance
Improve LangSmith-based workflow visualization


Author

Lizeth Campos
Fresno State — Computer Science


---

