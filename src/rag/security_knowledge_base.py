OWASP_CWE_KNOWLEDGE = [
    {
        "source_type": "CWE",
        "source_id": "CWE-89",
        "owasp_category": "Injection",
        "title": "SQL Injection",
        "keywords": ["sql", "query", "execute", "database", "injection", "sqlite", "mysql"],
        "summary": "SQL Injection happens when untrusted input is included directly in SQL queries without safe parameterization.",
        "safe_fix": "Use parameterized queries or prepared statements instead of string concatenation."
    },
    {
        "source_type": "CWE",
        "source_id": "CWE-79",
        "owasp_category": "Cross-Site Scripting",
        "title": "Cross-Site Scripting",
        "keywords": ["html", "script", "xss", "render", "template", "user input"],
        "summary": "XSS happens when untrusted user input is rendered into a web page without proper escaping or sanitization.",
        "safe_fix": "Escape output, sanitize input, and use safe templating practices."
    },
    {
        "source_type": "CWE",
        "source_id": "CWE-798",
        "owasp_category": "Identification and Authentication Failures",
        "title": "Use of Hard-coded Credentials",
        "keywords": ["password", "secret", "api_key", "token", "credential", "hardcoded"],
        "summary": "Hard-coded credentials expose secrets directly in source code and can allow unauthorized access.",
        "safe_fix": "Store secrets in environment variables or a secure secret manager."
    },
    {
        "source_type": "CWE",
        "source_id": "CWE-327",
        "owasp_category": "Cryptographic Failures",
        "title": "Use of a Broken or Risky Cryptographic Algorithm",
        "keywords": ["md5", "sha1", "hash", "crypto", "encrypt", "password"],
        "summary": "Weak cryptographic algorithms can expose sensitive data or make passwords easier to crack.",
        "safe_fix": "Use modern hashing algorithms like bcrypt, scrypt, or Argon2."
    },
    {
        "source_type": "CWE",
        "source_id": "CWE-306",
        "owasp_category": "Broken Access Control",
        "title": "Missing Authentication for Critical Function",
        "keywords": ["admin", "role", "permission", "authorization", "access", "delete", "update"],
        "summary": "Missing authentication or authorization checks can allow users to access privileged functions.",
        "safe_fix": "Add authentication and authorization checks before sensitive operations."
    },
    {
        "source_type": "CWE",
        "source_id": "CWE-200",
        "owasp_category": "Security Misconfiguration",
        "title": "Exposure of Sensitive Information",
        "keywords": ["debug", "error", "traceback", "secret", "config", "expose"],
        "summary": "Sensitive information exposure can happen when debug mode or verbose errors reveal internal details.",
        "safe_fix": "Disable debug mode in production and avoid exposing sensitive data."
    }
    {
    "source_type": "CWE",
    "source_id": "CWE-284",
    "owasp_category": "Broken Access Control",
    "title": "Improper Access Control",
    "keywords": ["access", "authorization", "permission", "role", "admin", "privilege", "allow_access"],
    "summary": "Improper access control happens when users can access functionality or resources without proper authorization checks.",
    "safe_fix": "Enforce authentication and authorization checks before allowing access to sensitive operations."
},
{
    "source_type": "CWE",
    "source_id": "CWE-489",
    "owasp_category": "Security Misconfiguration",
    "title": "Active Debug Code",
    "keywords": ["debug", "debug=true", "development", "production", "traceback", "app.run"],
    "summary": "Active debug code in production can expose sensitive information, stack traces, or internal application behavior.",
    "safe_fix": "Disable debug mode in production and remove development-only behavior from deployed systems."
},
]


def retrieve_security_context(code, application_context=""):
    combined_text = f"{code} {application_context}".lower()
    matched_results = []

    for item in OWASP_CWE_KNOWLEDGE:
        score = 0

        for keyword in item["keywords"]:
            if keyword in combined_text:
                score += 1

        if score > 0:
            result = dict(item)
            result["relevance_score"] = score
            matched_results.append(result)

    matched_results.sort(key=lambda x: x["relevance_score"], reverse=True)

    return matched_results[:5]


def format_retrieved_context(results):
    if not results:
        return "No directly relevant CWE/CVE context was retrieved."

    formatted_blocks = []

    for item in results:
        block = (
            f"{item['source_id']} — {item['title']} "
            f"({item['owasp_category']}): {item['summary']} "
            f"Recommended fix: {item['safe_fix']}"
        )
        formatted_blocks.append(block)

    return "\n".join(formatted_blocks)