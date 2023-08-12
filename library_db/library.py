from sqlalchemy.orm import Session
from sqlalchemy import select
from models import BookModel, AuthorModel, BookAuthorModel, Book_CopiesModel, BorrowsModel, StudentModel, BaseModel
from db import engine


class Library:
    @classmethod
    def search_by_title(cls, title):
        statement = select(BookModel).where(BookModel.title.like("%"+title+"%"))
        with Session(engine) as session:
            result = session.scalars(statement).fetchall()
        return result
    @classmethod
    def select_get(cls, bookid):
        statement = select(BookAuthorModel).where(BookAuthorModel.book_id == bookid)
        with Session(engine) as session:
            result = session.scalars(statement).fetchall()

        return result

    @classmethod
    def select_all(cls,):
        statement = select(BookAuthorModel)
        with Session(engine) as session:
            result = session.scalars(statement).fetchall()

        return result

    @classmethod
    def select_book(cls, title):
        statement = select(BookModel).where(BookModel.title == title)
        with Session(engine) as session:
            result = session.scalars(statement).first()
            # print(statement, result, type(result), result.title == title)
        return result

    @classmethod
    def select_author(cls, name, surname):
        statement = select(AuthorModel).where(AuthorModel.first_name == name, AuthorModel.last_name == surname)
        with Session(engine) as session:
            result = session.scalars(statement).first()
            print(statement, result, type(result))
        return result

    @classmethod
    def select_student(cls, name, surname):

        statement = select(StudentModel).where(StudentModel.first_name == name, StudentModel.last_name == surname)
        with Session(engine) as session:
            result = session.scalars(statement).first()
            print(statement, result, type(result))
        return result

    @classmethod
    def add_book(cls, title, author_name, author_surname, year, isbn="", p_year=0):

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
                statement_book_copies = Book_CopiesModel(book_id=statement_book.id, isbn=isbn, year=p_year)
                session.add(statement_book_copies)
                session.commit()

                print(statement_book, statement_author)

            elif (book_res is None) and (author_res is not None):
                statement_book = BookModel(title=title, year_first_published=year)
                session.add(statement_book)
                session.commit()
                statement_book_author = BookAuthorModel(author_id=author_res.id, book_id=statement_book.id)
                statement_book_copies = Book_CopiesModel(book_id=statement_book.id, isbn=isbn, year=p_year)
                session.add(statement_book_copies)
                session.add(statement_book_author)

                session.commit()

            elif (book_res is not None) and (author_res is None):
                statement_author = AuthorModel(first_name=author_name, last_name=author_surname)
                session.add(statement_author)
                session.commit()
                statement_book_author = BookAuthorModel(author_id=statement_author.id, book_id=book_res.id)
                statement_book_copies = Book_CopiesModel(book_id=book_res.id, isbn=isbn, year=p_year)
                session.add(statement_book_copies)
                session.add(statement_book_author)
                session.commit()

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

    @classmethod
    def student_reg(cls, stu_name, stu_surname, stu_email):
        student_res = Library.select_student(stu_name, stu_surname)
        if student_res is None or (student_res is not None and student_res.email != stu_email):
            with Session(engine, expire_on_commit=False) as session:
                statement_student = StudentModel(first_name=stu_name, last_name=stu_surname, email=stu_email)
                session.add(statement_student)
                session.commit()


# Library.student_reg("Adam", "Smith", "adam.smith@gimail.com")
# Library.student_reg("Eva", "Smith", "eva.smith@gimail.com")
# Library.student_reg("Markus", "Gregory", "markus.gregory@yahoo.com")
# Library.student_reg("Helga", "Peterson", "helga.peterson@outlook.com")
