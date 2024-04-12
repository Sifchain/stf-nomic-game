from contextlib import contextmanager
from datetime import datetime
from typing import Optional

import httpx
from sqlalchemy import create_engine

from nomic import config
from nomic.database.database import SessionLocal
from nomic.database.url import get_url


class DatabaseHandler:
    def __init__(self):
        self.db_url = get_url()
        if not self.db_url:
            raise ValueError("DB_URL not found in environment variables")

        self.engine = create_engine(self.db_url)

    @contextmanager
    def session_scope(self):
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
