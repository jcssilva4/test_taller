# Synthetic Sensitive-Data Test Set

All files in this directory are **entirely fictional** and generated for testing
purposes (e.g., role-based access control, document classification, redaction
pipelines). No real people, companies, financial accounts, or legal cases are
represented.

## Structure
- `contracts/` — sample service and employment contracts
- `financial/` — sample financial reports and payroll summaries
- `legal/` — sample NDAs and litigation notes
- `policies/` — sample internal company policies

## Access Control Convention
Each `.txt` file begins with a header specifying:
```
Document Type: ...
Document ID: ...
Authorized Roles: role1, role2, ...
```
Use the `Authorized Roles` field to test access-control logic (e.g., only
allow a simulated user to view the document if their role is in this list).
