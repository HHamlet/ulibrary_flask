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

    # def __eq__(self, other):
    #     return (self.title == other.title) and (self.author_name == other.author_name) and (self.author_surname == other.author_surname)


class Library:
    storage = []

    @classmethod
    def display(cls):
        with open("db.csv", "r") as f:
            csv_read = csv.DictReader(f)
            for row in csv_read:
                print(row["Title"], row["Name"], row["Surname"], row["ISBN"], row["Year"])

    @classmethod
    def storage_init(cls):
        with open("db.csv", "r") as f:
            csv_read = csv.DictReader(f)
            for row in csv_read:
                cls.storage.append(row)
        return cls.storage

    @classmethod
    def add_to_storage(cls, *args):
        for item in args:
            item_dict = {"Title": item.title,
                         "Name": item.author_name,
                         "Surname": item.author_surname,
                         "ISBN": item.isbn,
                         "Year": item.year}
            cls.storage.append(item_dict)
        return cls.storage

    @staticmethod
    def add_to_db(book_list):
        with open("db.csv", "w") as f:
            fieldnames = ["Title", "Name", "Surname", "ISBN", "Year"]
            csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
            # csv_writer.writeheader()
            for item in book_list:
                csv_writer.writerow(item)


class Students:
    def __init__(self, name, id, email):
        self.name = name
        self.id = id
        self.email = email
        self.book_current_taken = ()
        self.book_limit = 5


book1 = Book("book1", "name1", "surname1")
book2 = Book("book2", "name2", "surname2")
book3 = Book("book3", "name3", "surname3")
print(book3)
Library.add_to_storage(book1, book2, book3)
Library.add_to_db(Library.storage)
book4 = Book("book4", "name4", "surname4")
book5 = Book("book5", "name5", "surname5")
Library.add_to_storage(book4)
Library.add_to_storage(book5)
book6 = Book("book1", "name1", "surname1")
Library.add_to_storage(book6)
lib = Library()
# print(Library.storage_init())
# lib.display()
Library.add_to_db(Library.storage)
print(book1.title == book6.title)
