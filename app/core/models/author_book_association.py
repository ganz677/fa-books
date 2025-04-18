from sqlalchemy import Column, ForeignKey, Integer, Table

from .base import Base

book_author_association_table = Table(
    "book_author_association",
    Base.metadata,
    Column(
        "book_id", Integer, ForeignKey("books.id"), nullable=False, primary_key=True
    ),
    Column(
        "author_id", Integer, ForeignKey("authors.id"), nullable=False, primary_key=True
    ),
)
