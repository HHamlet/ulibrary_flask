from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel
from .book import BookModel


class Book_CopiesModel(BaseModel):
    __tablename__ = "book_copies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isbn: Mapped[str] = mapped_column(String(50), nullable=True)
    year: Mapped[int] = mapped_column(nullable=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    book: Mapped[BookModel] = relationship(lazy="joined")

    def __repr__(self):
        return f"Book_CopiesModel(id={self.id},Book={self.book} ISBN={self.isbn}, Year={self.year})"
