"""create users table

Revision ID: e45b6d54f61c
Revises: 3e1bfd8918bb
Create Date: 2025-05-05 16:22:09.230219

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "e45b6d54f61c"
down_revision: Union[str, None] = "3e1bfd8918bb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column(
            "active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")

