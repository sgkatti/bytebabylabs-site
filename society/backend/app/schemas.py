from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import Priority, TaskStatus


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=200)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    display_name: str
    role: str


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=10000)
    priority: Priority = Priority.MEDIUM
    due_date: datetime | None = None


class TaskComplete(BaseModel):
    completion_remarks: str = Field(min_length=1, max_length=10000)


class TaskReview(BaseModel):
    approved: bool
    review_remarks: str = Field(default="", max_length=10000)


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    priority: str
    status: str
    due_date: datetime | None
    created_by_id: int
    assigned_to_id: int
    completion_remarks: str | None
    review_remarks: str | None
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None
    reviewed_at: datetime | None
