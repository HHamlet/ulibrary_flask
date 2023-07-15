from sqlalchemy.orm import Session
from sqlalchemy import select
from models import BookModel, AuthorModel, BookAuthorModel, Book_CopiesModel, BorrowsModel, StudentModel, BaseModel
from db import engine


class Library:

    @classmethod
    def select_book(cls, title):
        statement = select(BookModel).where(BookModel.title == title)
        with Session(engine) as session:
            result = session.scalars(statement).first()
            print(statement, result, type(result), result.title == title)
        return result

    @classmethod
    def select_author(cls, name, surname):
        statement = select(AuthorModel).where(AuthorModel.first_name == name, AuthorModel.last_name == surname)
        with Session(engine) as session:
            result = session.scalars(statement).first()
            print(statement, result, type(result))
        return result

    @classmethod
    def add_book(cls, title, author_name, author_surname, year):

        author_res = Library.select_author(author_name, author_surname)
        book_res = Library.select_book(title)

        with Session(engine, expire_on_commit=False) as session:

            if (book_res is None) and (author_res is None):

                statement_book = BookModel(title=title, year_first_published=year)
                statement_author = AuthorModel(first_name=author_name, last_name=author_surname)
                session.add(statement_book)
                session.add(statement_author)
                session.commit()
                statement_book_author = BookAuthorModel(author_id=statement_author.id, book_id=statement_book.id)
                session.add(statement_book_author)
                session.commit()

                print(statement_book, statement_author)
            else:
                statement_book_copies = Book_CopiesModel(book_id=book_res.id)
                session.add(statement_book_copies)
                session.commit()
                print(statement_book_copies)

    @classmethod
    def del_db(cls):
        pass

    @classmethod
    def sign_to(cls):
        pass


# book1 = Library.select_book("The Master and Margarita")
# book2 = Library.select_author("Herbert", "Wells")
# print(book1)
# print(book2)
Library.add_book("War of the Worlds", "Herbert", "Wells", 1898)
# Library.add_book("The White Man's Burden", "Rudyard", "Kipling", 1899)
# Library.add_book("Dune", "Frank", "Herbert", 1965)
# Library.add_book("Foundation", "Isaac", "Asimov", 1951)
# Library.add_book("The Master and Margarita", "Mikhail", "Bulgakov", 1967)

