# Domain Model

## User

- id
- username
- display_name
- role
- password_hash
- is_active
- created_at
- updated_at

Roles: CHAIRMAN, SECRETARY, TREASURER, MANAGER.

## Task

- id
- title
- description
- priority
- status
- due_date
- created_by
- assigned_to
- completion_remarks
- review_remarks
- created_at
- updated_at
- completed_at
- reviewed_at

Priorities: LOW, MEDIUM, HIGH, URGENT.

Statuses: ASSIGNED, IN_PROGRESS, COMPLETED, REVIEWED.

## AuditEvent

- id
- task_id
- actor_id
- event_type
- old_value
- new_value
- created_at

Every meaningful workflow transition should generate an audit event.
