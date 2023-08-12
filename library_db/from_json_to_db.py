import json
from library import Library

with open("book_list1.json", "r") as file:
    json_list = json.load(file)


for book in json_list:
    Library.add_book(book["title"],
                     book["autor_first_name"],
                     book["autor_last_name"],
                     book["first_published_year"],
                     book["isbn"],
                     book["publishedDate"])

