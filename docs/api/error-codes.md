# Geetorus — API Error Codes & Handling

## 1. Error Response Format

All error responses from the Geetorus API adhere to a uniform JSON error payload format:

```json
{
  "error": "Descriptive error summary",
  "code": "ERROR_CODE_CONSTANT",
  "statusCode": 400,
  "details": {
    "field": "budgetLimitDaily",
    "reason": "Must be greater than 0"
  },
  "traceId": "req_8f19a0e2_39df"
}
```

---

## 2. Standardized Error Codes

| HTTP Status | Error Code | Description & Trigger Condition | Suggested Operator Action |
| :--- | :--- | :--- | :--- |
| **400** | `INVALID_PAYLOAD` | Request body failed validation against schema. | Verify required JSON fields and types. |
| **401** | `UNAUTHORIZED` | Missing or invalid Bearer authentication token. | Refresh user session or check API key validity. |
| **403** | `COMPANY_FORBIDDEN` | Authenticated principal is not a member of the requested company. | Request an invite from the company admin. |
| **403** | `APPROVAL_REQUIRED` | Tool execution blocked pending human sign-off. | Review and approve the request in UI. |
| **404** | `RESOURCE_NOT_FOUND` | Task, agent, secret, or company ID does not exist. | Confirm UUID validity in route path. |
| **409** | `CONCURRENCY_CONFLICT` | Task or turn modified by another process. | Reload latest task state before re-submitting. |
| **422** | `BUDGET_EXCEEDED` | Daily spend cap or per-task limit reached. | Increase company budget cap in settings. |
| **429** | `RATE_LIMITED` | Upstream AI provider rate limit encountered. | Watchdog will automatically retry with exponential backoff. |
| **500** | `INTERNAL_ERROR` | Uncaught exception in server runtime. | Inspect server stdout/stderr logs and activity ledger. |
