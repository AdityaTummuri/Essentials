---
name: security-audit
description: "Audit codebases for OWASP Top 10 vulnerabilities, supply-chain risks, insecure deserialization, secret leakage, and permission flaws."
---

# Static Security Audit & Threat Modeling Protocol

Use this skill when auditing source code, reviewing third-party dependencies, or conducting pre-deployment security reviews.

## High-Risk Vulnerability Checklist

### 1. Injection & Deserialization
- **SQL/NoSQL Injection**: Verify all database queries use parameterized prepared statements or safe ORM filters. Prohibit string formatting (`f"SELECT ... {user_input}"`).
- **Command Injection**: Prohibit raw `shell=True` in Python `subprocess` or `child_process.exec` in Node. Ensure argument lists are passed with validated binary paths.
- **Insecure Deserialization**: Prohibit unpickling untrusted inputs (`pickle.loads`). Use strict JSON or Protocol Buffers.

### 2. Authentication & Session Security
- Enforce constant-time string comparisons (`hmac.compare_digest` / `timingSafeEqual`) on tokens and webhook signatures to thwart timing attacks.
- Ensure JWT tokens explicitly validate the signature algorithm (`alg != "none"`) and check `exp` and `iss` claims.
- Mark session cookies: `HttpOnly`, `Secure`, `SameSite=Strict` or `Lax`.

### 3. Supply-Chain & Dependency Hygiene
- Run automated vulnerability scans: `pip-audit`, `npm audit`, `cargo audit`.
- Verify lockfiles (`package-lock.json`, `poetry.lock`, `uv.lock`) are committed and integrity hashes match.
- Block untrusted post-install build scripts (`npm config set ignore-scripts true` where appropriate).

### 4. Secret Leakage & Hardening
- Audit repositories for hardcoded API keys, private keys, and passwords using tools like `trufflehog` or `gitleaks`.
- Verify all public endpoints enforce rate limiting to mitigate denial-of-service and brute-force credential stuffing.
