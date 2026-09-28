import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.auth import hash_password
from app.database import Base, SessionLocal, engine
from app.main import app
from app.models import AuditEvent, Role, User


@pytest.fixture(autouse=True)
def database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.execute(delete(AuditEvent))
    db.execute(delete(User))
    db.add_all([
        User(username="chair", display_name="Chairman", role=Role.CHAIRMAN, password_hash=hash_password("chair-pass")),
        User(username="manager", display_name="Manager", role=Role.MANAGER, password_hash=hash_password("manager-pass")),
    ])
    db.commit()
    db.close()
    yield
    db = SessionLocal()
    db.execute(delete(AuditEvent))
    db.execute(delete(User))
    db.commit()
    db.close()


def test_task_lifecycle_and_rbac():
    with TestClient(app) as committee, TestClient(app) as manager:
        assert committee.post("/auth/login", json={"username":"chair","password":"chair-pass"}).status_code == 200

        created = committee.post("/tasks", json={
            "title":"Repair lobby light",
            "description":"Replace failed fixture",
            "priority":"HIGH"
        })
        assert created.status_code == 201
        task_id = created.json()["id"]

        assert manager.post("/tasks/"+str(task_id)+"/start").status_code == 401
        assert manager.post("/auth/login", json={"username":"manager","password":"manager-pass"}).status_code == 200
        assert manager.post("/tasks/"+str(task_id)+"/start").status_code == 200

        completed = manager.post("/tasks/"+str(task_id)+"/complete", json={"completion_remarks":"Fixture replaced"})
        assert completed.status_code == 200
        assert completed.json()["status"] == "COMPLETED"

        reviewed = committee.post("/tasks/"+str(task_id)+"/review", json={"approved":True,"review_remarks":"Verified"})
        assert reviewed.status_code == 200
        assert reviewed.json()["status"] == "REVIEWED"

        audit = committee.get("/tasks/"+str(task_id)+"/audit")
        assert audit.status_code == 200
        assert [x["event_type"] for x in audit.json()] == [
            "TASK_CREATED", "TASK_STARTED", "TASK_COMPLETED", "TASK_REVIEWED"
        ]


def test_foreign_origin_is_rejected():
    with TestClient(app) as client:
        response = client.post("/auth/login", headers={"Origin":"https://evil.example"}, json={
            "username":"chair","password":"chair-pass"
        })
        assert response.status_code == 403
