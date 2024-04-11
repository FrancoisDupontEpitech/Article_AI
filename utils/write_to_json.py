import os
import json

def write_to_json(articles, json_path):
    directory = os.path.dirname(json_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(json_path, 'w', encoding='utf8') as file:
        json.dump(articles, file, ensure_ascii=False, indent=4)