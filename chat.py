from typing import List, Dict, Set

import re
import os
import json
import pickle
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_category_response(category: str) -> str:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who lists words separated by commas"},
            {"role": "user", "content": f"List at least ten words belonging to the category '{category}' separated by commas"}
        ]
    )

    return ",".join([
        choice["message"]["content"]
        for choice in completion["choices"]
        if choice["finish_reason"] == "stop"
    ])


def parse_word_list(response: str) -> List[str]:
    response = response.lower()
    response_letters = "".join(re.findall("[a-z,]+", response))
    return set([
        word
        for word in response_letters.split(",")
        if word != ""
    ])


def load_category_sets(file_path: str):
    with open(file_path, "rb") as file:
        return pickle.load(file)
    

def write_category_sets(file_path: str, category_sets: Dict[str, Set[str]]):
    with open(file_path, "wb") as file:
        pickle.dump(category_sets, file)


def grow_category_list(category_sets: Dict[str, Set[str]], category: str):
    if not category in category_sets:
        category_sets[category] = set()

    response = get_category_response(category)

    new_words = parse_word_list(response)

    category_sets[category].update(new_words)


def print_category_sets(category_sets: Dict[str, Set[str]]):
    data = {
        category: {
            "num_words": len(words),
            "min_length": min([len(word) for word in words]),
            "max_length": max([len(word) for word in words]),
        }
        for category, words in category_sets.items()
    }

    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    all_categories = ["Seasame Street Characters"]

    category_sets = load_category_sets("category_sets.pkl")
    print_category_sets(category_sets)

    for category in all_categories:
        grow_category_list(category_sets, category)

    print_category_sets(category_sets)
    write_category_sets("category_sets.pkl", category_sets)
