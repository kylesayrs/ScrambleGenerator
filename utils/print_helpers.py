from typing import Dict, Set

import os
import json


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


class Node:
    def __init__(self, data) -> None:
        self.data = data
        self.left = None
        self.right = None


def print_in_box(message: str):
    terminal_size = os.get_terminal_size().columns

    root_node = Node(message)

    def split_node(node):
        split_index = None

        try:
            split_index = node.data.index("\n")
            node.data = node.data[:split_index] + node.data[split_index + 1:]
        except:
            if len(node.data) > terminal_size - 4:
                split_index = terminal_size - 4

        if split_index is not None:
            if node.data[:split_index] != "":
                node.left = Node(node.data[:split_index])
                split_node(node.left)

            if node.data[split_index:] != "":
                node.right = Node(node.data[split_index:])
                split_node(node.right)
    
    def get_lines(node):
        if node.left is not None and node.right is None:
            return get_lines(node.left)
        
        if node.left is None and node.right is not None:
            return get_lines(node.right)
        
        if node.left is not None and node.right is not None:
            return get_lines(node.left) + get_lines(node.right)
        
        return [node.data]

    split_node(root_node)
    lines = get_lines(root_node)

    max_line_length = max([len(line) for line in lines])

    print("".join(["-"] * (max_line_length + 4)))
    for line in lines:
        print("| ", end="")
        print(line, end="")
        padding = max_line_length - len(line)
        print("".join([" "] * padding), end="")
        print(" |")
    print("".join(["-"] * (max_line_length + 4)))
