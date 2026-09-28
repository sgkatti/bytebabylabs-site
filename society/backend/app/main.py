from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import authenticate, require_committee, require_manager, require_user
from app.config import get_settings
from app.database import get_db
from app.models import AuditEvent, Role, Task, TaskStatus, User
from app.schemas import LoginRequest, TaskComplete, TaskCreate, TaskOut, TaskReview, UserOut

settings = get_settings()

app = FastAPI(title="Society Task Platform API", version="0.2.0")

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret,
    session_cookie=settings.session_cookie_name,
    max_age=settings.session_max_age,
    https_only=settings.secure_cookies,
    same_site="lax",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "society-task-platform"}


@app.post("/auth/login", response_model=UserOut)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)) -> User:
    user = authenticate(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    request.session.clear()
    request.session["user_id"] = user.id
    return user


@app.get("/users/manager", response_model=list[UserOut])
def list_managers(user: User = Depends(require_committee), db: Session = Depends(get_db)) -> list[User]:
    return list(db.scalars(select(User).where(User.role == Role.MANAGER, User.is_active.is_(True))).all())


@app.post("/auth/logout")
def logout(request: Request) -> dict[str, str]:
    request.session.clear()
    return {"status": "ok"}


@app.get("/auth/me", response_model=UserOut)
def me(user: User = Depends(require_user)) -> User:
    return user


@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(user: User = Depends(require_user), db: Session = Depends(get_db)) -> list[Task]:
    statement = select(Task).order_by(Task.created_at.desc())
    if user.role == Role.MANAGER:
        statement = statement.where(Task.assigned_to_id == user.id)
    return list(db.scalars(statement).all())


@app.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, user: User = Depends(require_committee), db: Session = Depends(get_db)) -> Task:
    manager = db.scalar(select(User).where(User.role == Role.MANAGER, User.is_active.is_(True)))
    if not manager:
        raise HTTPException(status_code=409, detail="No active manager is configured")

    task = Task(
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        status=TaskStatus.ASSIGNED,
        due_date=payload.due_date,
        created_by_id=user.id,
        assigned_to_id=manager.id,
    )
    db.add(task)
    db.flush()
    db.add(AuditEvent(task_id=task.id, actor_id=user.id, event_type="TASK_CREATED", new_value=task.status.value))
    db.commit()
    db.refresh(task)
    return task


@app.post("/tasks/{task_id}/start", response_model=TaskOut)
def start_task(task_id: int, user: User = Depends(require_manager), db: Session = Depends(get_db)) -> Task:
    task = db.get(Task, task_id)
    if not task or task.assigned_to_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != TaskStatus.ASSIGNED:
        raise HTTPException(status_code=409, detail="Task is not assigned")
    old = task.status.value
    task.status = TaskStatus.IN_PROGRESS
    db.add(AuditEvent(task_id=task.id, actor_id=user.id, event_type="TASK_STARTED", old_value=old, new_value=task.status.value))
    db.commit()
    db.refresh(task)
    return task


@app.post("/tasks/{task_id}/complete", response_model=TaskOut)
def complete_task(task_id: int, payload: TaskComplete, user: User = Depends(require_manager), db: Session = Depends(get_db)) -> Task:
    from datetime import datetime
    task = db.get(Task, task_id)
    if not task or task.assigned_to_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != TaskStatus.IN_PROGRESS:
        raise HTTPException(status_code=409, detail="Task must be in progress")
    old = task.status.value
    task.status = TaskStatus.COMPLETED
    task.completion_remarks = payload.completion_remarks
    task.completed_at = datetime.utcnow()
    db.add(AuditEvent(task_id=task.id, actor_id=user.id, event_type="TASK_COMPLETED", old_value=old, new_value=task.status.value))
    db.commit()
    db.refresh(task)
    return task


@app.post("/tasks/{task_id}/review", response_model=TaskOut)
def review_task(task_id: int, payload: TaskReview, user: User = Depends(require_committee), db: Session = Depends(get_db)) -> Task:
    from datetime import datetime
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != TaskStatus.COMPLETED:
        raise HTTPException(status_code=409, detail="Task must be completed before review")
    old = task.status.value
    if payload.approved:
        task.status = TaskStatus.REVIEWED
        task.reviewed_at = datetime.utcnow()
        event_type = "TASK_REVIEWED"
    else:
        task.status = TaskStatus.IN_PROGRESS
        task.reviewed_at = None
        event_type = "TASK_RETURNED"
    task.review_remarks = payload.review_remarks
    db.add(AuditEvent(task_id=task.id, actor_id=user.id, event_type=event_type, old_value=old, new_value=task.status.value))
    db.commit()
    db.refresh(task)
    return task

@app.get("/tasks/{task_id}/audit")
def task_audit(task_id: int, user: User = Depends(require_committee), db: Session = Depends(get_db)) -> list[dict]:
    if not db.get(Task, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    events = db.scalars(
        select(AuditEvent).where(AuditEvent.task_id == task_id).order_by(AuditEvent.created_at.asc())
    ).all()
    return [
        {
            "id": event.id,
            "task_id": event.task_id,
            "actor_id": event.actor_id,
            "event_type": event.event_type,
            "old_value": event.old_value,
            "new_value": event.new_value,
            "created_at": event.created_at,
        }
        for event in events
    ]
