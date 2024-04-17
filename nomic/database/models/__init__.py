from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from nomic.database import Base

# Define the association table for the many-to-many relationship between Games and Users
game_players = Table(
    "game_players",
    Base.metadata,
    Column("game_id", UUID(as_uuid=True), ForeignKey("games.id"), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
)
