import csv
import random


class Author:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.book = set()

    def __repr__(self):
        return f"{self.name},{self.surname}"

    def __hash__(self):
        return hash((self.name, self.surname))

    def __eq__(self, other):
        return (self.name == other.name) and (self.surname == other.surname)

    def new_book(self, title, year=None, isbn=None):
        new_book = Book(title, year, isbn)
        self.book.add(new_book)
        return new_book


class Book:
    def __init__(self, title, author, year=None, isbn=None):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.copies = []

    def __repr__(self):
        return f"{self.title} {self.author.name} {self.author.surname}, {self.year}, {self.isbn}"

    def add_copy(self):
        book_copy = BookCopy(self)
        self.copies.append(book_copy)
        return self.copies

    def __hash__(self):
        return hash((self.title, self.author))

    def __eq__(self, other):
        return (self.title == other.title) and (self.author == other.author)


class BookCopy:
    def __init__(self, book):
        self.book = book
        self.year = book.year
        self.isbn = book.isbn

    def __repr__(self):
        return f"copy: {self.book.title} {self.year},ISBN :{self.isbn}"


class Library:
    storage = {}
    students_list = {}

    @classmethod
    def add_to_storage(cls, title, name, surname, year=None, isbn=None):
        author = Author(name, surname)

        if author not in cls.storage:
            cls.storage[author] = {}

        book = Book(title, author, year, isbn)

        if book not in cls.storage[author]:
            cls.storage[author][book] = book.copies
        else:
            cls.storage[author][book] = book.add_copy()

    @classmethod
    def storage_init(cls):
        with open("db.csv", "r") as f:
            fieldnames = ["name", "surname", "title", "copy"]
            csv_read = csv.DictReader(f, fieldnames=fieldnames)
            for row in csv_read:
                author = Author(row["name"], row["surname"])
                cls.storage[author] = {}
                book = Book(row["title"], author)
                cls.storage[author][book] = row["copy"]
        return cls.storage

    @staticmethod
    def add_to_db(book_list):
        with open("db.csv", "w") as f:
            fieldnames = ["name", "surname", "title", "copy"]
            csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
            for key, value in book_list.items():
                dict_1 = {"name": key.name,
                          "surname": key.surname
                          }
                for el in value:
                    dict_2 = {"title": el,
                              "copy": value[el]
                              }
                    csv_writer.writerow({"name": dict_1["name"], "surname": dict_1["surname"],
                                         "title": dict_2["title"], "copy": dict_2["copy"]})

    @classmethod
    def request(cls, title, name, surname):
        request_flag = False
        for items in cls.storage:
            if surname == items.surname and name == items.name:
                for el in cls.storage[items]:
                    if title == el.title:
                        if len(el.copies) >= 1:
                            request_flag = True
        return request_flag

    @classmethod
    def students_registration(cls, name, email):
        student = Students(name, email)
        if student not in cls.students_list:
            cls.students_list[student] = [student.id, student.book_current_taken]
        else:
            return f"{student} is registered"
        return cls.students_list

    @classmethod
    def sign_book(cls):
        pass


class Students:
    def __init__(self, name, email):
        self.name = name
        self.id = str(random.getrandbits(30))
        self.email = email
        self.book_current_taken = ()
        self.book_limit = 5

    def __repr__(self):
        return f"Student ({self.name}, {self.email})"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


Library.add_to_storage("War of the Worlds", "Herbert", "Wells", 1898, "789456")
Library.add_to_storage("War of the Worlds", "Herbert", "Wells", 1898, "789456")
Library.add_to_storage("War of the Worlds", "Herbert", "Wells", 1898, "789456")
Library.add_to_storage("The White Man's Burden", "Rudyard", "Kipling", 1899, "7894887")
Library.add_to_storage("The Jungle Book", "Rudyard", "Kipling", 1894, "7894127")
Library.add_to_storage("The Jungle Book", "Rudyard", "Kipling", 1894, "7894127")
Library.add_to_storage("Dune", "Frank", "Herbert", 1965, "7895129")
Library.add_to_db(Library.storage)
# Library.storage_init()
print(Library.storage)
print(Library.request("War of the Worlds", "Herbert", "Wells"))
