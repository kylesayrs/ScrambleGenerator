from typing import List, Set

import re


def parse_word_list(response: str) -> Set[str]:
    response = response.lower()
    response_letters = "".join(re.findall("[a-z,]+", response))
    return set([
        word
        for word in response_letters.split(",")
        if word != ""
    ])
