from sqlalchemy.orm import Session
from sqlalchemy import select
from db import engine
from flask import Flask, render_template, redirect, request, url_for, session
from library import Library, Students
from models import BookModel, BookAuthorModel, UserModel, StudentModel
from forms import CreateBookForm, LoginForm, AdminRegisterForm, StudentRegisterForm
from login import login_required
import requests
import math

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
    r = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={book_copy_data.isbn}'
                     f'&key=AIzaSyDHSdWAbF5rMzG4LhNnDwmhvET1dtRXDYo')
    description_by_api = r.json()["items"][0]
    img_url = url_for('static', filename=f'/picture/id_{book_id}.jpeg')
    return render_template("book_ditail.html", book=book_data, img_url=img_url, book_copy_data=book_copy_data,
                           description=description_by_api)


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


@login_required
@app.route("/students")
def list_students():
    item_per_page = 10

    page_number = int(request.args.get("page", 1))
    offset = (page_number - 1) * item_per_page
    total_pages = math.ceil(len(Session(engine).scalars(select(StudentModel)).all()) / item_per_page)
    students = Session(engine).scalars(select(StudentModel).limit(item_per_page).offset(offset)).fetchall()

    return render_template("students.html", students=students, total_pages=total_pages)


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


if __name__ == "__main__":
    app.run(port=5000, debug=True)
