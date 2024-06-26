import datetime
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select
from models import BookModel, AuthorModel, BookAuthorModel, Book_CopiesModel, BorrowsModel, StudentModel
from db import engine


class Library:
    @classmethod
    def search_by_title(cls, title):
        statement = select(BookModel).where(BookModel.title.like("%"+title+"%"))
        with Session(engine) as session:
            result = session.scalars(statement).fetchall()
        return result

    @classmethod
    def select_get(cls, book_id):
        statement = select(BookAuthorModel).where(BookAuthorModel.book_id == book_id)
        with Session(engine) as session:
            result = session.scalars(statement).one()

        return result

    @classmethod
    def select_get_book_copies(cls, book_id):
        statement = select(Book_CopiesModel).where(Book_CopiesModel.book_id == book_id)
        with Session(engine) as session:
            result = session.scalars(statement).all()

        return result

    @classmethod
    def select_all(cls,):
        statement = select(BookAuthorModel)
        with Session(engine) as session:
            result = session.scalars(statement).all()

        return result

    @classmethod
    def select_book(cls, title):
        statement = select(BookModel).where(BookModel.title == title)
        with Session(engine) as session:
            result = session.scalars(statement).first()
        return result

    @classmethod
    def select_author(cls, name, surname):
        statement = select(AuthorModel).where(AuthorModel.first_name == name, AuthorModel.last_name == surname)
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

                print(statement_book, statement_author, "1")

            elif (book_res is None) and (author_res is not None):
                statement_book = BookModel(title=title, year_first_published=year)
                session.add(statement_book)
                session.commit()
                statement_book_author = BookAuthorModel(author_id=author_res.id, book_id=statement_book.id)
                statement_book_copies = Book_CopiesModel(book_id=statement_book.id, isbn=isbn, year=p_year)
                session.add(statement_book_copies)
                session.add(statement_book_author)
                print("2")
                session.commit()

            elif (book_res is not None) and (author_res is None):
                statement_author = AuthorModel(first_name=author_name, last_name=author_surname)
                session.add(statement_author)
                session.commit()
                statement_book_author = BookAuthorModel(author_id=statement_author.id, book_id=book_res.id)
                statement_book_copies = Book_CopiesModel(book_id=book_res.id, isbn=isbn, year=p_year)
                session.add(statement_book_copies)
                session.add(statement_book_author)
                print("3")
                session.commit()

            else:
                statement_book_copies = Book_CopiesModel(book_id=book_res.id, isbn=isbn, year=p_year)
                session.add(statement_book_copies)
                session.commit()
                print(statement_book_copies, "4")

    @classmethod
    def sign_to(cls, bookcopiesid, studentid):
        book = None
        student = None
        if Library.check_book_in_borrow_table(bookcopiesid) is not True:
            book = select(Book_CopiesModel).where(Book_CopiesModel.id == bookcopiesid)
        if len(Library.student_taken_book(studentid)) <= 5:
            student = select(StudentModel).where(StudentModel.id == studentid)

        if book is not None and student is not None:
            with Session(engine, expire_on_commit=False) as session:
                book_to_sign = session.scalars(book).first()
                sign_to_student = session.scalars(student).first()
                statement_borrow = BorrowsModel(book_copies_id=book_to_sign.id,
                                                student_id=sign_to_student.id,
                                                borrowed_data=datetime.date.today()
                                                )
                statement_borrow.return_data = statement_borrow.borrowed_data + datetime.timedelta(14)
                session.add(statement_borrow)
                session.commit()
                return True
        else:
            print("book or student are not available")
            return False

    @staticmethod
    def check_book_in_borrow_table(book_id):
        borrowed_book = select(BorrowsModel).where(BorrowsModel.book_copies_id == book_id)
        with Session(engine, expire_on_commit=False) as session:
            result = session.scalars(borrowed_book).first()
            print(result)
        if result is not None:
            return True
        return False

    @staticmethod
    def check_return_data(borrow_id):
        time_delta = datetime.timedelta(days=14)
        statement = select(BorrowsModel).where(BorrowsModel.id == borrow_id)
        with Session(engine, expire_on_commit=False) as session:
            result = session.scalars(statement).first()
        print(type(result.return_data), result.return_data)
        delta = datetime.date.today() - result.borrowed_data
        print(type(delta), delta)
        if delta < time_delta:
            print(time_delta - delta, "days remain...")
            return True
        else:
            print(abs(time_delta - delta), "days left...")
            return False

    @staticmethod
    def student_taken_book(student_id):
        taken_book = select(BorrowsModel).where(BorrowsModel.student_id == student_id)
        with Session(engine, expire_on_commit=False) as session:
            result = session.scalars(taken_book).fetchall()
        return result

    @classmethod
    def return_bookcopy(cls, book_copies_id, student_id):
        db_session = sessionmaker(bind=engine)
        borrow_sessions = db_session()
        entity_del = borrow_sessions.query(BorrowsModel).where(BorrowsModel.book_copies_id == book_copies_id and
                                                               BorrowsModel.student_id == student_id).first()
        borrow_sessions.delete(entity_del)
        borrow_sessions.commit()


class Students:
    @classmethod
    def select_student(cls, name, surname):
        statement = select(StudentModel).where(StudentModel.first_name == name, StudentModel.last_name == surname)
        with Session(engine) as session:
            result = session.scalars(statement).first()
            print(statement, result, type(result))
        return result

    @classmethod
    def student_reg(cls, stu_name, stu_surname, stu_email):
        student_res = Students.select_student(stu_name, stu_surname)
        if student_res is None or (student_res is not None and student_res.email != stu_email):
            with Session(engine, expire_on_commit=False) as session:
                statement_student = StudentModel(first_name=stu_name, last_name=stu_surname, email=stu_email)
                session.add(statement_student)
                session.commit()
                print(statement_student)

    @classmethod
    def select_all(cls):
        statement = select(StudentModel)
        with Session(engine) as session:
            result = session.scalars(statement).all()
        return result

    @classmethod
    def delete_student_entity(cls, student_id):
        db_session = sessionmaker(bind=engine)
        student_sessions = db_session()
        student_del = student_sessions.query(StudentModel).get(int(student_id))
        student_sessions.delete(student_del)
        student_sessions.commit()
