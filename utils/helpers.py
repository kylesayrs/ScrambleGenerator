from typing import List, Dict, Set

import os
import json
import pickle

def load_category_sets(file_path: str) -> Dict[str, Set[str]]:
    if not os.path.exists(file_path):
        return {}

    with open(file_path, "rb") as file:
        return pickle.load(file)
    

def write_category_sets(file_path: str, category_sets: Dict[str, Set[str]]):
    with open(file_path, "wb") as file:
        pickle.dump(category_sets, file)
    

def load_tile_set_distribution(file_path: str):
    with open(file_path, "r") as file:
        return json.load(file)


def save_scramble(scramble: List[str], file_path: str):
    with open(file_path, "w") as file:
        file.write(str(scramble))
