from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel
from .author import AuthorModel
from .book import BookModel


class BookAuthorModel(BaseModel):
    __tablename__ = "book_author"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    author: Mapped[AuthorModel] = relationship(lazy="joined")
    book: Mapped[BookModel] = relationship(lazy="joined")

    def __repr__(self):
        return f"Book_AuthorModel(Author={self.author}, Book={self.book})"
