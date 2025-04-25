from .base import Base


from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean



class User(Base):
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
    )
    full_name: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )
    hashed_password: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    disabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
    
    def __repr__(self):
        return f'<User id = {self.id}, username = {self.username}>'