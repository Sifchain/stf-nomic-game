from sqlalchemy import (JSON, BigInteger, Column, DateTime, ForeignKey,
                        Integer, String)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from nomic.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
