"""add is_superuser value in users table

Revision ID: 5f922e50e2e3
Revises: e45b6d54f61c
Create Date: 2025-05-05 18:36:17.317297

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "5f922e50e2e3"
down_revision: Union[str, None] = "e45b6d54f61c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "is_superuser",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "is_superuser")

