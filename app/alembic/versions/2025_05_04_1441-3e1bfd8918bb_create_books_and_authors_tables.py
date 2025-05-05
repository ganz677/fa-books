"""create books and authors tables

Revision ID: 3e1bfd8918bb
Revises:
Create Date: 2025-05-04 14:41:49.674312

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "3e1bfd8918bb"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("full_name", sa.String(length=100), nullable=False),
        sa.Column("biography", sa.Text(), nullable=False),
        sa.Column("birthdate", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_authors")),
    )
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("num_pages", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_books")),
    )
    op.create_table(
        "book_author_association",
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["authors.id"],
            name=op.f("fk_book_author_association_author_id_authors"),
        ),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["books.id"],
            name=op.f("fk_book_author_association_book_id_books"),
        ),
        sa.PrimaryKeyConstraint(
            "book_id", "author_id", name=op.f("pk_book_author_association")
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("book_author_association")
    op.drop_table("books")
    op.drop_table("authors")
