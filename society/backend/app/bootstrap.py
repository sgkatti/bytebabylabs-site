import os
import sys

from sqlalchemy import select

from app.auth import hash_password
from app.database import SessionLocal
from app.models import Role, User

ROLE_ENV = {
    Role.CHAIRMAN: "SOCIETY_USER_1",
    Role.SECRETARY: "SOCIETY_USER_2",
    Role.TREASURER: "SOCIETY_USER_3",
    Role.MANAGER: "SOCIETY_USER_4",
}

def required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

def main() -> None:
    db = SessionLocal()
    try:
        for role, prefix in ROLE_ENV.items():
            username = required(f"{prefix}_USERNAME")
            display_name = required(f"{prefix}_DISPLAY_NAME")
            password = required(f"{prefix}_PASSWORD")
            user = db.scalar(select(User).where(User.username == username))
            if user:
                user.display_name = display_name
                user.role = role
                user.password_hash = hash_password(password)
                user.is_active = True
            else:
                db.add(User(username=username, display_name=display_name, role=role,
                            password_hash=hash_password(password), is_active=True))
        db.commit()
        print("Society users provisioned successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Bootstrap failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
