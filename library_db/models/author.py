from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class AuthorModel(BaseModel):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    UniqueConstraint(first_name, last_name)
    def __repr__(self):
        return f"AuthorModel(id={self.id}, Author={self.first_name} {self.last_name})"
