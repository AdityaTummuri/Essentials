---
name: api-design
description: "Design clean, scalable, backward-compatible APIs following RESTful/RPC standards, idempotency keys, pagination, and error schemas."
---

# API Design & Architecture Protocol

Use this skill when designing HTTP REST endpoints, GraphQL schemas, or internal RPC interfaces.

## Core Design Principles

### 1. Resource Modeling & URI Structure
- Use nouns, not verbs: `GET /v1/orders`, `POST /v1/orders`, `DELETE /v1/orders/123`.
- Sub-resources for ownership: `GET /v1/users/42/tokens`.
- Pluralize collection names consistently.

### 2. Idempotency & Safe Mutation
- Ensure `GET`, `HEAD`, `OPTIONS`, `PUT`, and `DELETE` are idempotent by HTTP specification.
- For unsafe mutations (`POST`), support an `Idempotency-Key` header:
  - Cache the response against the idempotency key in Redis/database with a TTL (e.g. 24 hours).
  - If a duplicate request arrives, return the cached response without re-executing state changes.

### 3. Pagination & Filtering
- Prefer **Cursor-Based Pagination** over offset-based pagination for high-cardinality tables:
  ```json
  {
    "data": [...],
    "pagination": {
      "has_more": true,
      "next_cursor": "eyJpZCI6MTQyOCwidGltZSI6MTcyOTQ..."
    }
  }
  ```
- Offset pagination (`LIMIT ... OFFSET ...`) causes severe database degradation on deep pages and misses records when items are inserted mid-page.

### 4. Standardized Error Payloads (RFC 7807)
- Return structured error objects with HTTP status codes (400, 401, 403, 404, 409, 422, 429, 500):
  ```json
  {
    "type": "https://api.example.com/errors/validation-error",
    "title": "Invalid Request Parameters",
    "status": 422,
    "detail": "Field 'email' must be a valid email address.",
    "invalid_params": [
      { "name": "email", "reason": "Missing @ domain symbol" }
    ]
  }
  ```

