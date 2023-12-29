import json


def get_data():
    with open('levels.json') as fp:
        return json.load(fp)


data = get_data()
print(data["levels"][0]["objects"]["pigs"])
