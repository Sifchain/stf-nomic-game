from contextlib import contextmanager
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from nomic.database import SessionLocal, engine
from nomic.database.models.user import User


class DatabaseHandler:
    def __init__(self):
        self.engine = engine

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def transform_created_at(self, created_at: Optional[datetime] = None) -> str:
        if not created_at:
            created_at = datetime.utcnow()

        return created_at.strftime("%Y-%m-%d %H:%M:%S")


# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: str) -> User | None:
    return db.query(User).get({"id": user_id})


def create_user(db: Session, username: str, hashed_password: str) -> User:
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
