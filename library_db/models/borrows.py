import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel
from .student import StudentModel
from .book_copies import Book_CopiesModel


class BorrowsModel(BaseModel):
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    borrowed_data: Mapped[datetime.date]
    return_data: Mapped[datetime.date]
    book_copies_id: Mapped[int] = mapped_column(ForeignKey("book_copies.id"))
    book_copies: Mapped[Book_CopiesModel] = relationship(lazy="joined")
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    student: Mapped[StudentModel] = relationship(lazy="joined")

    def __repr__(self):
        return f"BorrowsModel(id={self.id},Student={self.student} Book={self.book_copies}, " \
               f"Borrowed={self.borrowed_data}, return={self.return_data})"
