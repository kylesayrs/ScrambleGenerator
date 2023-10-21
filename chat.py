from typing import List, Dict, Set

import os
import tqdm
import openai
import argparse
openai.api_key = os.getenv("OPENAI_API_KEY")

from utils import (
    print_category_sets,
    write_category_sets,
    load_category_sets,
    parse_word_list
)

parser = argparse.ArgumentParser()
parser.add_argument("--category", type=str, default=None, help="Category to add words to. Not specifying this will print the current sets")
parser.add_argument("--num_iterations", type=int, default=5, help="Number of prompt iterations")
parser.add_argument("--temperature", type=int, default=1.1, help="Model temperature. Higher values yield more creative responses")
parser.add_argument("--category_sets_path", type=str, default="category_sets.pkl")


def get_category_response(category: str, temperature: float) -> str:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who lists words separated by commas"},
            {"role": "user", "content": f"List at least ten words belonging to the category '{category}' separated by commas"}
        ],
        temperature=temperature
    )

    return ",".join([
        choice["message"]["content"]
        for choice in completion["choices"]
        if choice["finish_reason"] == "stop"
    ])
    


def grow_category_list(category_sets: Dict[str, Set[str]], category: str, temperature: float):
    category = category.lower()
    if not category in category_sets:
        category_sets[category] = set()

    response = get_category_response(category, temperature)
    new_words = parse_word_list(response)
    category_sets[category].update(new_words)


if __name__ == "__main__":
    args = parser.parse_args()

    category_sets = load_category_sets(args.category_sets_path)
    print_category_sets(category_sets)
    if args.category is None:
        exit(0)

    for _ in tqdm.tqdm(range(args.num_iterations)):
        grow_category_list(category_sets, args.category, args.temperature)

    print_category_sets(category_sets)
    write_category_sets(args.category_sets_path, category_sets)
