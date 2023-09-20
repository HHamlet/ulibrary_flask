from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select
from db import engine
from flask import Flask, render_template, redirect, request, url_for, session
from library import Library, Students
from models import BookAuthorModel, UserModel, StudentModel, Book_CopiesModel, BorrowsModel
from forms import CreateBookForm, LoginForm, AdminRegisterForm, StudentRegisterForm
from login import login_required
import requests
import math
import wikipedia

app = Flask(__name__, static_folder="static")
app.config.from_object("config.AppConfig")


@app.context_processor
def inject_data() -> dict:
    user_id = session.get("user")
    user = None
    if user_id:
        user = Session(engine).scalars(select(UserModel).where(UserModel.id == user_id)).first()
    return {
        "user": user,
    }


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/books")
def list_book():
    item_per_page = 10
    page_number = int(request.args.get("page", 1))
    offset = (page_number - 1) * item_per_page
    total_pages = math.ceil(len(Session(engine).scalars(select(BookAuthorModel)).all()) / item_per_page)
    book = Session(engine).scalars(select(BookAuthorModel).limit(item_per_page).offset(offset)).fetchall()

    return render_template("book.html", books=book, total_pages=total_pages)


@app.route("/books/<book_id>")
def book_ditail(book_id):
    book_data = Library.select_get(book_id)
    book_copy_data = Library.select_get_book_copies(book_id)
    copies_count = Session(engine).query(Book_CopiesModel).where(Book_CopiesModel.book_id == book_id).count()
    name = book_data.author.first_name + " " + book_data.author.last_name
    # r1 = requests.get(f'https://openlibrary.org/search/authors.json?q={name}')
    # key = r1.json()["docs"][0]["key"]
    # author_bio = ""
    # r2 = requests.get(f'https://openlibrary.org/authors/{key}.json')
    # if r2.json().get("bio"):
    #     if isinstance(r2.json().get("bio"), dict):
    #         if r2.json()["bio"].get("value"):
    #             author_bio = r2.json()["bio"].get("value")
    #     else:
    #         author_bio = r2.json().get("bio")
    try:
        wiki_author_data = wikipedia.summary(name)
        author_url = wikipedia.page(name).url
    except KeyError:
        wiki_author_data = ""
        author_url = ""
    except wikipedia.exceptions.PageError:
        try:
            name = book_data.author.last_name + " " + book_data.author.first_name
            wiki_author_data = wikipedia.summary(name)
            author_url = wikipedia.page(name).url
        except wikipedia.exceptions.PageError:
            wiki_author_data = ""
            author_url = ""

    for el in book_copy_data:
        r = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={[el.isbn]}'
                         f'&key=AIzaSyDHSdWAbF5rMzG4LhNnDwmhvET1dtRXDYo')
        description_by_api = r.json()["items"][0]
        img_url = url_for('static', filename=f'/picture/id_{book_id}.jpeg')

        return render_template("book_ditail.html",
                               book=book_data,
                               img_url=img_url,
                               book_copy_data=book_copy_data,
                               description=description_by_api,
                               copies_count=copies_count,
                               author_bio=wiki_author_data,
                               author_url=author_url
                               )


@app.route("/books/add_new", methods=["GET", "POST"])
@login_required
def new_book():
    create_book_form = CreateBookForm()
    if create_book_form.validate_on_submit():
        Library.add_book(title=create_book_form.book_title.data,
                         author_name=create_book_form.author_first_name.data,
                         author_surname=create_book_form.author_last_name.data,
                         year=create_book_form.first_published_year.data,
                         isbn=create_book_form.isbn.data,
                         p_year=create_book_form.published_year.data,
                         )
        return redirect("/books")

    return render_template("new_book.html", form=create_book_form)


@app.route("/registration", methods=["GET", "POST"])
@login_required
def registration():
    form = AdminRegisterForm()
    return render_template("reg.html", form=form)


@app.route("/registration/students", methods=["GET", "POST"])
@login_required
def registration_students():
    form = StudentRegisterForm()
    if form.validate_on_submit():
        Students.student_reg(
            stu_name=form.first_name.data,
            stu_surname=form.last_name.data,
            stu_email=form.email.data,
        )
        return redirect("/")
    return render_template("reg_students.html", form=form)


@app.route("/students")
@login_required
def list_students():
    item_per_page = 10

    page_number = int(request.args.get("page", 1))
    offset = (page_number - 1) * item_per_page
    total_pages = math.ceil(len(Session(engine).scalars(select(StudentModel)).all()) / item_per_page)
    students = Session(engine).scalars(select(StudentModel).limit(item_per_page).offset(offset)).fetchall()

    return render_template("students.html", students=students, total_pages=total_pages)


@app.route("/students/<student_id>", methods=["GET", "POST"])
@login_required
def student_ditail(student_id):
    not_return_intime = []
    student = Session(engine).query(StudentModel).get(int(student_id))
    borrow_ditail = Session(engine).scalars(
        select(BorrowsModel).where(BorrowsModel.student_id == student_id)).fetchall()
    for data in borrow_ditail:
        if Library.check_return_data(data.id) is False:
            not_return_intime.append(data)

    if request.method == "POST":
        if request.form.get("change"):
            return redirect(url_for(".update_form", student_id=student.id))
        elif request.form.get("del"):
            Students.delete_student_entity(student_id)
            return redirect("/students")

    return render_template("student_ditail.html",
                           student=student,
                           borrow_ditail=borrow_ditail,
                           not_return_intime=not_return_intime)


@app.route('/update-form')
def update_form():
    student_id = request.args.get("student_id")
    student = Session(engine).query(StudentModel).get(int(student_id))
    print("REQUEST: ", request.args.get("student_id"))
    return render_template('update_form.html', student=student)


@app.route('/update', methods=['POST'])
def update_info():
    student_id = request.form['ID']
    new_firs_name = request.form['new_first_name']
    new_last_name = request.form['new_last_name']
    new_email = request.form['new_email']

    session_db = sessionmaker(bind=engine)()
    student = session_db.query(StudentModel).filter_by(id=student_id).first()
    student.first_name = new_firs_name
    student.last_name = new_last_name
    student.email = new_email
    session_db.commit()

    return redirect("/students")


@app.route("/search_result")
def search_result():
    search_title = request.args.get("title")
    print(search_title)
    books = Library.search_by_title(search_title)
    return render_template("search_result.html", search_title=search_title, books=books)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Session(engine).scalars(select(UserModel).where(UserModel.username == form.username.data)).first()
        hashed_password = UserModel.hash_password(form.username.data, form.password.data)
        if not user or user.password != hashed_password:
            form.username.errors.append("Invalid credentials")
            return render_template("login.html", form=form)
        session["user"] = user.id
        return_url = request.args.get("next")
        print(return_url)
        return redirect(return_url if return_url else "/")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session["user"] = None
    return redirect("/login")


@app.route("/borrow", methods=["GET", "POST"])
@login_required
def borrow():
    student = ""
    book_copies = ""
    books_taken = []
    if request.method == "GET" and "title" in request.args:
        title = request.args.get("title")
        book = Library.select_book(title)
        if book:
            book_copies = Library.select_get_book_copies(book.id)
            print("Book Copies : ", book_copies)
            for data in book_copies:
                if Library.check_book_in_borrow_table(data.id):
                    books_taken.append(data)

    if request.method == "GET" and ("student_fname" and "student_lname" in request.args):
        student_first_name = request.args.get("student_fname")
        student_last_name = request.args.get("student_lname")
        student = Students.select_student(student_first_name, student_last_name)

    if request.method == "POST" and ("bookcopies_id" and "student_id" in request.form):
        bookcopies_id = request.form["bookcopies_id"]
        student_id = request.form["student_id"]
        Library.sign_to(bookcopies_id, student_id)

    if request.method == "POST" and ("return_bookcopies_id" and "return_student_id" in request.form):
        return_book_id = request.form["return_bookcopies_id"]
        return_student_id = request.form["return_student_id"]
        print(return_book_id, return_student_id)
        Library.return_bookcopy(return_book_id, return_student_id)

    return render_template("borrow.html",
                           student=student,
                           book_copies=book_copies,
                           books_taken=books_taken
                           )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
