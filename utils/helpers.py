from typing import List

import uuid
import json
import pickle

def load_category_sets(file_path: str):
    with open(file_path, "rb") as file:
        return pickle.load(file)
    

def load_tile_set_distribution(file_path: str):
    with open(file_path, "r") as file:
        return json.load(file)


def save_scramble(scramble: List[str], file_path: str):
    with open(file_path, "w") as file:
        file.write(str(scramble))
