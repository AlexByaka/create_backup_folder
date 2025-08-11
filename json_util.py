import json


def load_json(filename) -> dict:
    with open(filename, "r", encoding="UTF-8") as json_file:
        return json.load(json_file)


def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=3)
