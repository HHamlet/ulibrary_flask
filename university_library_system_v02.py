import json
import random
from datetime import datetime


class BaseModel:
    def to_dict(self):
        obj_dict = {}
        for key, value in vars(self).items():
            obj_dict[key] = self.__serialize(value)
        return obj_dict

    @classmethod
    def __serialize(cls, value):
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        elif hasattr(value, "to_dict"):
            return value.to_dict()
        elif isinstance(value, (list, set, tuple)):
            new_value = []
            for element in value:
                new_value.append(cls.__serialize(element))
            return new_value
        elif isinstance(value, dict):
            new_value = {}
            for key, element in value.items():
                new_value[key] = cls.__serialize(element)
            return new_value
        else:
            raise TypeError("Not serializable")


class JSONSerializer:
    @staticmethod
    def to_json(obj_lis):
        list_json = []
        for obj in obj_lis:
            str_json = Library.to_dict(obj)
            list_json.append(str_json)
        return list_json


class Author(BaseModel):
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def __repr__(self):
        return f"{self.name},{self.surname}"

    def __hash__(self):
        return hash((self.name, self.surname))

    def __eq__(self, other):
        return (self.name == other.name) and (self.surname == other.surname)


class Book(BaseModel):
    def __init__(self, title, author_name, author_surname, year, isbn):
        self.title = title
        self.author = Author(author_name, author_surname)
        self.year = year
        self.isbn = isbn
        self.copies = []

    def __repr__(self):
        return f"{self.title} , {self.author}, {self.year}, {self.isbn}"

    def add_copy(self, book):
        book_copy = BookCopy(book.title, book.author.name, book.author.surname, book.year, book.isbn)
        self.copies.append(book_copy)
        return self.copies

    def __hash__(self):
        return hash((self.title, self.author))

    def __eq__(self, other):
        return (self.title == other.title) and (self.author == other.author)


class BookCopy(BaseModel):
    def __init__(self, title, author_name, author_surname, year, isbn):
        self.title = title
        self.author = (author_name, author_surname)
        self.year = year
        self.isbn = isbn
        self.status = "Available"
        self.borrow_data = None
        self.borrow_student = None

    def __repr__(self):
        return f"copy: {self.title} , {self.author}, {self.year}, {self.isbn}"


class Library(BaseModel):
    book_object_list = []
    students_object_list = []

    @classmethod
    def add_to_storage(cls, *args):
        for element in args:
            if element not in cls.book_object_list:
                cls.book_object_list.append(element)
            else:
                fined_book = cls.search_book(element)
                fined_book.add_copy(element)

    @classmethod
    def storage_init(cls):
        data = Library.read_from_db("new.json")
        for items in data:
            book = Book(items["title"], items["author"]["name"], items["author"]["surname"],
                        items["year"], items["isbn"])
            if len(items["copies"]) != 0:
                for element in items["copies"]:
                    book_copy = BookCopy(element["title"], element["author"][0], element["author"][1],
                                         element["year"], element["isbn"])
                    book_copy.status = element["status"]
                    book_copy.borrow_data = element["borrow_data"]
                    book_copy.borrow_student = element["borrow_student"]
                    book.copies.append(book_copy)
            cls.book_object_list.append(book)

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
    def search_book(cls, book):
        for items in cls.book_object_list:
            if book.title == items.title and book.author == items.author:
                return items

    @classmethod
    def request(cls, title, name, surname):
        request_flag = False
        for items in cls.book_object_list:
            if title == items.title and (name == items.author.name and surname == items.author.surname):
                for book_copy in items.copies:
                    if book_copy.status == "Available":
                        request_flag = True
                        print(request_flag)
                        return book_copy
        return request_flag

    @classmethod
    def students_registration(cls, stud_name, stud_surname, email):
        student = Students(stud_name, stud_surname, email)
        if student not in cls.students_object_list:
            cls.students_object_list.append(student)
            print(f"{student} registered")
        else:
            return f"{student} is registered"

    @classmethod
    def sign_book(cls, title, author_name, author_surname, stud_name, stud_surname):
        if isinstance(Library.request(title, author_name, author_surname), BookCopy):
            book_for_sign = Library.request(title, author_name, author_surname)
            for student in cls.students_object_list:
                if stud_name == student.name and stud_surname == student.surname:
                    if len(student.book_current_taken) < student.book_limit:
                        if len(student.book_current_taken) >= 1:
                            for cb in student.book_current_taken:
                                delta = datetime.now() - cb.borrow_data
                                if delta.days > 14:
                                    return f"{student} not returned book in 14 days!!!"
                        student.book_current_taken.add(book_for_sign)
                        book_for_sign.status = "Not available"
                        book_for_sign.borrow_student = (student.name, student.surname, student.email)
                        book_for_sign.borrow_data = str(datetime.today())
                        print(f"{book_for_sign} signed to {student}")
                        return cls.students_object_list
                    else:
                        return print(f"Limit reach {student.book_limit}")
        else:
            return f"Book not available"

    @classmethod
    def student_list_init(cls):
        data = Library.read_from_db("student.json")
        for items in data:
            student = Students(items["name"], items["surname"], items["email"])
            student.id = items["id"]
            student.book_limit = items["book_limit"]
            if len(items["book_current_taken"]) != 0:
                for element in items["book_current_taken"]:
                    book_copy = BookCopy(element["title"], element["author"][0],
                                         element["author"][1], element["year"], element["isbn"])
                    book_copy.status = element["status"]
                    book_copy.borrow_data = datetime.strptime(element["borrow_data"], "%Y-%m-%d %H:%M:%S.%f")
                    book_copy.borrow_student = element["borrow_student"]
                    for some_book in Library.book_object_list:
                        if book_copy.title == some_book.title and book_copy.author[0] == some_book.author.name and \
                                book_copy.author[1] == some_book.author.surname:
                            for books in some_book.copies:
                                if books.borrow_student == book_copy.borrow_student:
                                    student.book_current_taken.add(books)
            Library.students_object_list.append(student)

    @classmethod
    def search_student(cls, student_name, student_surname):
        for student in cls.students_object_list:
            if student_name == student.name and student_surname == student.surname:
                print("student find!")
                return student

    @classmethod
    def book_return(cls, title, author_name, author_surname, student_name, student_surname):
        student = cls.search_student(student_name, student_surname)
        print("current taken ", student.book_current_taken)
        for book_copy in student.book_current_taken:
            if title == book_copy.title and author_name == book_copy.author[0] and author_surname == book_copy.author[1]:
                book_copy.status = "Available"
                book_copy.borrow_data = None
                book_copy.borrow_student = None
                student.book_current_taken.remove(book_copy)
                break


class Students(BaseModel):
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

