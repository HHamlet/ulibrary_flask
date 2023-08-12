from flask import Flask, render_template, redirect, request, url_for
from library import Library
from models import BookModel
from forms import CreateBookForm


app = Flask(__name__, static_folder="static")
app.config.from_object("config.AppConfig")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/books")
def list_book():
    return render_template("book.html", books=Library.select_all())


@app.route("/books/<book_id>")
def book_ditail(book_id):
    book_data = Library.select_get(book_id)
    print(book_data)
    img_url = url_for('static', filename=f'id_{book_id}.jpeg')
    print(img_url)
    return render_template("book_ditail.html", book=book_data[0], img_url=img_url)


@app.route("/books/add_new", methods=["GET", "POST"])
def new_book():
    create_book_form = CreateBookForm()
    if create_book_form.validate_on_submit():
        Library.add_book(title=create_book_form.book_title.data,
                         author_name=create_book_form.author_first_name.data,
                         author_surname=create_book_form.author_last_name.data,
                         year=create_book_form.first_published_year.data,
                         isbn=create_book_form.isbn.data,
                         p_year=create_book_form.published_year.data
                         )
        return redirect("/books")

    return render_template("new_book.html", form=create_book_form)


@app.route("/search_result")
def search_result():
    search_title = request.args.get("title")
    print(search_title)
    books = Library.search_by_title(search_title)
    return render_template("search_result.html", search_title=search_title, books=books)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
