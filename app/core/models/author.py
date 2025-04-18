from typing import TYPE_CHECKING

from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .author_book_association import book_author_association_table
from .base import Base

if TYPE_CHECKING:
    from .book import Book


class Author(Base):
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    biography: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )
    birthdate: Mapped[Date] = mapped_column(
        Date(),
        nullable=False,
    )

    books: Mapped[list["Book"]] = relationship(
        secondary=book_author_association_table,
        back_populates="authors",
    )
