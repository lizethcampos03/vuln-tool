# CWE Dataset Notes

This folder stores CWE-related security weakness data used to support the RAG layer.

For the current prototype, the tool uses a curated CWE subset focused on OWASP-relevant vulnerability categories. This keeps retrieval precise during calibration and avoids overwhelming the LLM with noisy or irrelevant context.

The architecture is designed so the curated CWE knowledge base can later be expanded with the full official CWE dataset.

Current focus areas:
- Injection
- Broken Access Control
- Identification and Authentication Failures
- Cryptographic Failures
- Security Misconfiguration
- Software and Data Integrity Failures
- Vulnerable and Outdated Components
- Security Logging and Monitoring Failures
- Insecure Design