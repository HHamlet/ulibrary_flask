import requests
import json
import csv

names = []

books = []
i = 0
with open("./tgb_3.csv", 'r') as file:

    csv_reader = csv.reader(file)
    for row in csv_reader:
        names.append(row[1])

t = 0
for name in names:
    r = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={name}'
                     f'&key=AIzaSyDHSdWAbF5rMzG4LhNnDwmhvET1dtRXDYo')
    count = 0
    for el in r.json()["items"]:
        print(el["volumeInfo"]["title"])
        print(el["volumeInfo"]["publishedDate"])
        print(el["volumeInfo"]["industryIdentifiers"][0]["identifier"])
        print(el["volumeInfo"]["authors"])
        print("============================================")
        book = {}
        count += 1
        book["title"] = el["volumeInfo"]["title"]
        book["publishedDate"] = el["volumeInfo"]["publishedDate"]
        book["isbn"] = el["volumeInfo"]["industryIdentifiers"][0]["identifier"]
        book["author"] = el["volumeInfo"]["authors"]
        books.append(book)
        if count == 1:
            break

print(books)
json_data = json.dumps(books, indent=2)
print(json_data)
with open("book_list.json", "w") as book_list:
    book_list.write(json_data)

