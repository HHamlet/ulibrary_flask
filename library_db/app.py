from flask import Flask, render_template, redirect
from library import Library
from models import BookModel


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/books")
def list_book():
    return render_template("book.html", books=Library.select_())


@app.route("/books/<book_id>")
def book_ditail(book_id):
    book_data = Library.select_( bookid=book_id)
    print(book_data)
    return render_template("book_ditail.html", book=book_data[0])


@app.route("/books/add_new", methods=["GET", "POST"])
def new_book():
    pass
    return render_template("new_book.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)

