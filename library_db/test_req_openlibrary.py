import requests
import json


name = "The Odyssey"
r = requests.get(f'https://openlibrary.org/search.json?q={name}')
json_str = json.dumps(r.json(), indent=2)
work = ""
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

