from fastapi import Depends, HTTPException, Request, status
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Role, User

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy-password-for-timing")


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def authenticate(db: Session, username: str, password: str) -> User | None:
    user = db.scalar(select(User).where(User.username == username))
    if not user or not user.is_active:
        password_hash.verify(password, DUMMY_HASH)
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def require_user(request: Request, db: Session = Depends(get_db)) -> User:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    user = db.get(User, int(user_id))
    if not user or not user.is_active:
        request.session.clear()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    return user


def require_committee(user: User = Depends(require_user)) -> User:
    if user.role not in {Role.CHAIRMAN, Role.SECRETARY, Role.TREASURER}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Committee role required")
    return user


def require_manager(user: User = Depends(require_user)) -> User:
    if user.role != Role.MANAGER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manager role required")
    return user
