# Security Baseline

## Identity

Exactly four society identities are expected in the initial production deployment. There is no self-service registration.

## Authorization

### Committee roles

Chairman, Secretary and Treasurer may:
- create tasks
- assign tasks to the Manager
- change task priority/due date where authorized
- review completed work
- close or return tasks
- view audit history

### Manager

The Manager may:
- view assigned tasks
- mark a task in progress
- mark work completed
- provide completion remarks/evidence
- view relevant task history

The Manager cannot create committee users or bypass review controls.

## Credential handling

Passwords must be hashed using a modern password hashing scheme. Initial credentials are supplied through secure deployment configuration and are never committed to source control.

## Session handling

Production should use secure, HttpOnly, SameSite cookies over HTTPS. Authentication state must not be stored in browser localStorage.

## Data protection

- TLS for all production traffic.
- Database credentials stored as deployment secrets.
- No database credentials in source code.
- Audit records are append-oriented and attributable to a user.
- Sensitive error details are not returned to clients.

Free-tier infrastructure is a cost constraint, not a reason to weaken application security.
