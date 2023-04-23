import json
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

    def new_book(self, title, year, isbn):
        new_book = Book(title, year, isbn)
        if new_book in self.book:
            new_book.add_copy()
        self.book.add(new_book)
        return new_book


class Book:
    def __init__(self, title, author_name, author_surname, year, isbn):
        self.title = title
        self.author = Author(author_name, author_surname)
        self.year = year
        self.isbn = isbn
        self.copies = []

    def __repr__(self):
        return f"{self.title} , {self.year}, {self.isbn}"

    def add_copy(self):
        self.copies.append(BookCopy(self))
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
    storage = []
    students_list = {}

    @classmethod
    def add_to_storage(cls, *args):
        for element in args:
            found_in_storage = False
            for item in cls.storage:
                if (element.title == item["title"]) and \
                        (element.author.name == item["Author"]["name"] and
                         element.author.surname == item["Author"]["surname"]):
                    item["copies"] += 1
                    found_in_storage = True
                    break

            if not found_in_storage:
                book_dict = {
                    "title": element.title,
                    "Author": {
                        "name": element.author.name,
                        "surname": element.author.surname,
                    },
                    "year": element.year,
                    "ISBN": element.isbn,
                    "copies": len(element.copies)
                }
                cls.storage.append(book_dict)

    @classmethod
    def storage_init(cls):
        data = Library.read_from_db()
        for items in data:
            book = Book(items["title"], items["Author"]["name"], items["Author"]["surname"],
                        items["year"], items["ISBN"])
            if items["copies"] != 0:
                for i in range(items["copies"]):
                    book.add_copy()
            cls.add_to_storage(book)
        return cls.storage

    @staticmethod
    def write_to_db(book_list):
        json_str = json.dumps(book_list, indent=2)
        with open("db.json", "w") as file:
            file.write(json_str)

    @staticmethod
    def read_from_db():
        with open("db.json", "r") as file:
            data = json.load(file)
        return data

    @classmethod
    def request(cls, title, name, surname):
        request_flag = False
        for items in cls.storage:
            if title == items["title"] and (name == items["Author"]["name"] and surname == items["Author"]["surname"]):
                if items["copies"] >= 1:
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


# Library.add_to_storage("War of the Worlds", "Herbert", "Wells", 1898, "789456")
# Library.add_to_storage("War of the Worlds", "Herbert", "Wells", 1898, "789456")
# Library.add_to_storage("War of the Worlds", "Herbert", "Wells", 1898, "789456")
# Library.add_to_storage("The White Man's Burden", "Rudyard", "Kipling", 1899, "7894887")
# Library.add_to_storage("The Jungle Book", "Rudyard", "Kipling", 1894, "7894127")
# Library.add_to_storage("The Jungle Book", "Rudyard", "Kipling", 1894, "7894127")
# Library.add_to_storage("Dune", "Frank", "Herbert", 1965, "7895129")
# Library.add_to_db(Library.storage)
Library.storage_init()
print(Library.storage)
print(Library.request("War of the Worlds", "Herbert", "Wells"))
