from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class BookModel(BaseModel):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    year_first_published: Mapped[int]

    def __repr__(self):
        return f"BookModel(id={self.id}, Title={self.title} , fist published: {self.year_first_published})"
