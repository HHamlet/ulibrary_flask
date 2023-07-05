from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class StudentModel(BaseModel):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))

    def __repr__(self):
        return f"StudentModel(id={self.id}, Student={self.first_name} {self.last_name}, email: {self.email})"
