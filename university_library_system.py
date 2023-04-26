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
        book_copy = BookCopy(self)
        self.copies.append(book_copy)
        Library.book_object_list.append(book_copy)
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
    students_list = []
    book_object_list = []
    students_object_list = []

    @classmethod
    def add_to_storage(cls, *args):
        for element in args:
            found_in_storage = False
            for item in cls.storage:
                if (element.title == item["title"]) and \
                        (element.author.name == item["Author"]["name"] and
                         element.author.surname == item["Author"]["surname"]):
                    item["copies"] += 1
                    book_copy = cls.search_book(element.title, element.author.name, element.author.surname)
                    book_copy.book.add_copy()
                    found_in_storage = True
                    break

            if not found_in_storage:
                # cls.book_object_list.append(element)
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
    def write_to_db(book_list, filename="db.json"):
        json_str = json.dumps(book_list, indent=2)
        with open(filename, "w") as file:
            file.write(json_str)

    @staticmethod
    def read_from_db(filename="db.json"):
        with open(filename, "r") as file:
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
    def search_book(cls, title, name, surname):
        for items in cls.book_object_list:
            if title == items.book.title and (name == items.book.author.name and surname == items.book.author.surname):
                if len(items.book.copies) >= 1:
                    return items

    @classmethod
    def students_registration(cls, stud_name, stud_surname, email):
        student = Students(stud_name, stud_surname, email)
        if student not in cls.students_object_list:
            student_dict = {
                "student": {
                    "name": student.name,
                    "surname": student.surname,
                    "email": student.email,
                    "ID": student.id,
                    "books": student.book_current_taken,
                    "limit": student.book_limit
                    }
                }
            cls.students_object_list.append(student)
            cls.students_list.append(student_dict)
            print(f"{student} registered")
        else:
            return f"{student} is registered"

    @classmethod
    def sign_book(cls, title, author_name, author_surname, stud_name, stud_surname):
        if Library.request(title, author_name, author_surname):
            for student in cls.students_object_list:
                if stud_name == student.name and stud_surname == student.surname:
                    if student.book_limit > 0:
                        book_for_sign = cls.search_book(title, author_name, author_surname)
                        student.book_current_taken.add(book_for_sign)
                        book_for_sign.book.copies.remove(book_for_sign)
                        cls.book_object_list.remove(book_for_sign)
                        student.book_limit -= 1
                        print(student.book_limit)
                        print(f"{book_for_sign} signed to {student}")
                        return cls.students_list
                    else:
                        return print(f"Limit reach {student.book_limit}")

        else:
            return f"Book not available"


class Students:
    def __init__(self, name, surname, email):
        self.name = name
        self.surname = surname
        self.id = str(random.randint(1, 5000))
        self.email = email
        self.book_current_taken = set()
        self.book_limit = 5

    def __repr__(self):
        return f"Student ({self.name} {self.surname}, {self.email})"

    def __hash__(self):
        return hash((self.name, self.surname))

    def __eq__(self, other):
        return (self.name == other.name) and (self.surname == other.surname)


Library.storage_init()
print(Library.request("War of the Worlds", "Herbert", "Wells"))
Library.students_registration("Adam", "Smith", "adam.smith@domain.com")
Library.students_registration("Eva", "Schneider", "eva.schneider@domain.com")
Library.students_registration("Tom", "Sawyer", "tom.sawyer@domain.com")
b1 = Book("War of the Worlds", "Herbert", "Wells", 1898, "789456")
Library.add_to_storage(b1)
Library.sign_book("War of the Worlds", "Herbert", "Wells", "Eva", "Schneider")
print(Library.students_list)
