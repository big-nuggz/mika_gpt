import os
import json


def load_api_key(path: str) -> str:
    ''' loads api key from given path and returns it '''
    with open(path, 'r', encoding='utf8') as f:
        api_key = f.readline()

    return api_key

def load_json(path: str) -> dict:
    ''' self explanatory '''
    with open(path, 'r', encoding='utf8') as f:
        json_content = json.load(f)

    return json_content

def save_json(data: dict, path: str) -> None:
    ''' self explanatory '''
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f)

def delete_file(path: str) -> None:
    ''' self explanatory '''
    if os.path.exists(path):
        os.remove(path)