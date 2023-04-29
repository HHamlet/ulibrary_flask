import json
import random


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
    # @staticmethod
    # def to_json(obj):
    #     if not hasattr(obj, "to_dict"):
    #         raise TypeError("Not serializable")
    #     return json.dumps(obj.to_dict())
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
        # self.book = set()

    def __repr__(self):
        return f"{self.name},{self.surname}"

    def __hash__(self):
        return hash((self.name, self.surname))

    def __eq__(self, other):
        return (self.name == other.name) and (self.surname == other.surname)

    # @classmethod
    # def from_dict(cls, author_data):
    #     return cls(
    #         name=author_data["name"],
    #         surname=author_data["surname"]
    #     )


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
        self.copies.append(book)
        return self.copies

    def __hash__(self):
        return hash((self.title, self.author))

    def __eq__(self, other):
        return (self.title == other.title) and (self.author == other.author)

    # @classmethod
    # def from_dict(cls, book_data):
    #     return cls(
    #         title=book_data["title"],
    #         author_name=Author.from_dict(book_data["author"]["name"]),
    #         author_surname=Author.from_dict(book_data["author"]["surname"]),
    #         year=book_data["year"],
    #         isbn=book_data["isbn"]
    #         # copies=book_data["copies"]
    #     )


class BookCopy(BaseModel):
    def __init__(self, book):
        self.book = book
        # self.year = book.year
        # self.isbn = book.isbn

    def __repr__(self):
        return f"copy: {self.book.title}"


class Library(BaseModel):
    # storage = []
    # students_list = []
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
                for i in range(len(items["copies"])):
                    book.add_copy(book)
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
                request_flag = True
                print(request_flag)
                return items
        return request_flag

    @classmethod
    def students_registration(cls, stud_name, stud_surname, email):
        student = Students(stud_name, stud_surname, email)
        if student not in cls.students_object_list:
            # student_dict = {
            #     "student": {
            #         "name": student.name,
            #         "surname": student.surname,
            #         "email": student.email,
            #         "ID": student.id,
            #         "books": student.book_current_taken,
            #         "limit": student.book_limit
            #         }
            #     }
            cls.students_object_list.append(student)
            # cls.students_list.append(student_dict)
            print(f"{student} registered")
        else:
            return f"{student} is registered"

    @classmethod
    def sign_book(cls, title, author_name, author_surname, stud_name, stud_surname):
        if isinstance(Library.request(title, author_name, author_surname), Book):
            book_for_sign = Library.request(title, author_name, author_surname)
            for student in cls.students_object_list:
                if stud_name == student.name and stud_surname == student.surname:
                    if student.book_limit > 0:

                        student.book_current_taken.add(book_for_sign)
                        book_for_sign.copies.remove(book_for_sign)
                        student.book_limit -= 1
                        print(student.book_limit)
                        print(f"{book_for_sign} signed to {student}")
                        return cls.students_object_list
                    else:
                        return print(f"Limit reach {student.book_limit}")

        else:
            return f"Book not available"


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


# b1 = Book("War of the Worlds", "Herbert", "Wells", 1898, "9781595400307")
# b2 = Book("War of the Worlds", "Herbert", "Wells", 1898, "9781595400307")
# b3 = Book("War of the Worlds", "Herbert", "Wells", 1898, "9781595400307")
# b4 = Book("War of the Worlds", "Herbert", "Wells", 1898, "9781595400307")
# b5 = Book("The White Man's Burden", "Rudyard", "Kipling", 1899, "9780199210824")
# b6 = Book("The White Man's Burden", "Rudyard", "Kipling", 1899, "9780199210824")
# b7 = Book("Dune", "Frank", "Herbert", 1965, "9780441013593")
# Library.add_to_storage(b1, b2, b3, b4, b5, b6, b7)

# Library.write_to_db(JSONSerializer.to_json(Library.book_object_list), "new.json")
Library.storage_init()
# for el in Library.book_object_list:
#     print("1", type(el))
#     print(el.copies)
b8 = Book("Dune", "Frank", "Herbert", 1965, "9780441013593")
Library.add_to_storage(b8)
# print(Library.book_object_list)

for el in Library.book_object_list:
    # print("2", type(el))
    print(el.copies, len(el.copies))
# ddd = JSONSerializer.to_json(Library.book_object_list)
# Library.write_to_db(JSONSerializer.to_json(Library.book_object_list), "new.json")
print(Library.request("The White Man's Burden", "Rudyard", "Kipling"))
Library.students_registration("Adam", "Smith", "adam.smith@domain.com")
Library.students_registration("Eva", "Schneider", "eva.schneider@domain.com")
Library.students_registration("Tom", "Sawyer", "tom.sawyer@domain.com")
print(Library.students_object_list)
sdata = JSONSerializer.to_json(Library.students_object_list)

Library.sign_book("War of the Worlds", "Herbert", "Wells", "Eva", "Schneider")

for el in Library.students_object_list:
    print(el)
    print(el.book_current_taken, el.book_limit)
for el in Library.book_object_list:
    print(el.copies, len(el.copies))
    sdata = Library.to_dict(el)
    print(type(sdata), sdata)