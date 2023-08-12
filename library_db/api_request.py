import requests
name = "Dune"
# r = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={name}'
#                      f'&key=AIzaSyDHSdWAbF5rMzG4LhNnDwmhvET1dtRXDYo')
#
# for el in r.json()["items"]:
#     print(el["volumeInfo"]["title"])
#     print(el["volumeInfo"]["publishedDate"])
#     print(el["volumeInfo"]["industryIdentifiers"][0]["identifier"])
#     print(el["volumeInfo"]["authors"])
#     print("============================================")
#
# name = "The Odyssey"
# author_name = "Mikhail Bulgakov"
r = requests.get(f'https://openlibrary.org/search.json?q={name}')
count = 0
for el in r.json()["docs"]:
    # if el["title"] == name:
    print(el["title"])
    print(el["first_publish_year"])
    print(el["isbn"])
    print(el["author_name"])
    print("============================================")
    count += 1
    if count == 5:
        break
