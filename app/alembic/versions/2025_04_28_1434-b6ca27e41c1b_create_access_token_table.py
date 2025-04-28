"""create access token table

Revision ID: b6ca27e41c1b
Revises: bedb21a5d3ec
Create Date: 2025-04-28 14:34:14.818580

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import fastapi_users_db_sqlalchemy

revision: str = "b6ca27e41c1b"
down_revision: Union[str, None] = "bedb21a5d3ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "access_tokens",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("token", sa.String(length=43), nullable=False),
        sa.Column(
            "created_at",
            fastapi_users_db_sqlalchemy.generics.TIMESTAMPAware(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_access_tokens_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("token", name=op.f("pk_access_tokens")),
    )
    op.create_index(
        op.f("ix_access_tokens_created_at"),
        "access_tokens",
        ["created_at"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_access_tokens_created_at"), table_name="access_tokens"
    )
    op.drop_table("access_tokens")
