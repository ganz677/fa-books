from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .author_book_association import book_author_association_table
from .base import Base

if TYPE_CHECKING:
    from .author import Author


class Book(Base):
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text(),
    )
    num_pages: Mapped[int] = mapped_column(
        Integer(),
    )

    authors: Mapped[list["Author"]] = relationship(
        secondary=book_author_association_table,
        back_populates="books",
    )
