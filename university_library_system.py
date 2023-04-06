import csv


class Book:
    def __init__(self, title, author_name, author_surname, year=None):
        self.title = title
        self.author_name = author_name
        self.author_surname = author_surname
        self.isbn = f"{hash(self.title)}"
        self.year = None

    def __str__(self):
        return f"{self.title}, Author: {self.author_name} {self.author_surname}"


class Library:
    @classmethod
    def display(cls):
        with open("db.csv", "r") as f:
            csv_read = csv.DictReader(f)
            for row in csv_read:
                print(row["Title"], row["Name"], row["Surname"], row["ISBN"], row["Year"])

    @classmethod
    def storage_init(cls):
        storage = []
        with open("db.csv", "r") as f:
            csv_read = csv.DictReader(f)
            for row in csv_read:
                storage.append(row)
        return storage

    def add_to_db(*args):
        with open("db.csv", "a") as f:
            fieldnames = ["Title", "Name", "Surname", "ISBN", "Year"]
            csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
            csv_writer.writeheader()
            for item in args:
                item_dict = {"Title": item.title,
                             "Name": item.author_name,
                             "Surname": item.author_surname,
                             "ISBN": item.isbn,
                             "Year": item.year}
                csv_writer.writerow(item_dict)


class Students:
    pass


book1 = Book("book1", "name1", "surname1")
book2 = Book("book2", "name2", "surname2")
book3 = Book("book3", "name3", "surname3")
print(book3)
# Library.add_to_db(book1, book2, book3)
book4 = Book("book4", "name4", "surname4")
# Library.add_to_db(book4)
lib = Library()
print(Library.storage_init())
lib.display()
