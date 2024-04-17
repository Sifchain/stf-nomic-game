"""Create tables

Revision ID: 50ec82c4ef4d
Revises: 
Create Date: 2024-04-15 12:56:58.540035

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "50ec82c4ef4d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            primary_key=True,
            default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("username", sa.String(), nullable=False, unique=True, index=True),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False, default=0),
    )
    op.create_table(
        "games",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            primary_key=True,
            default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("CREATED", "STARTED", "ENDED", name="game_statuses"),
            nullable=False,
            default="CREATED",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            default=sa.text("CURRENT_TIMESTAMP"),
            onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.create_table(
        "rules",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            primary_key=True,
            default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "game_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("games.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, default=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            default=sa.text("CURRENT_TIMESTAMP"),
            onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.create_table(
        "game_players",
        sa.Column(
            "game_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("games.id"),
            primary_key=True,
        ),
        sa.Column("user_id", sa.UUID(), sa.ForeignKey("users.id"), primary_key=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    op.drop_table("rules")
    op.drop_table("games")
    op.drop_table("game_players")
    # ### end Alembic commands ###
