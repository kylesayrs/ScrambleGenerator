from typing import Dict, List, Tuple, Union

import os
import re
import uuid
import json
import numpy
import argparse

from utils import (
    load_tile_set_distribution,
    get_character_frequency,
    plot_scramble_char_freq,
    multiply_distribution,
    load_category_sets,
    save_scramble,
    print_in_box,
    gini,
)


parser = argparse.ArgumentParser()
parser.add_argument("--category", type=str, default=None, help="Category to create scramble for. Defaults to random category")
parser.add_argument("--num_words", type=int, default=5, help="Number of words in scramble")
parser.add_argument("--min_word_length", type=int, default=5, help="Minimum word length of words appearing in scramble")
parser.add_argument("--max_word_length", type=int, default=10, help="Minimum word length of words appearing in scramble")

parser.add_argument("--num_tile_sets", type=int, default=2, help="Multiplier factor for tile set distribution")

parser.add_argument("--category_sets_path", type=str, default="category_sets.pkl")
parser.add_argument("--tile_set_path", type=str, default="tile_set_distribution.json")
parser.add_argument("--scramble_dir", type=str, default="scrambles")


def get_score(word: str, scramble: List[str], tile_set_distribution: Dict[str, int]) -> Union[float, None]:
    new_scramble = scramble + [word]

    # calculate character frequency
    char_freq = get_character_frequency(new_scramble)

    # check for overflow
    for char, freq in char_freq.items():
        if freq > tile_set_distribution[char.upper()]:
            return None

    # score is negative gini coeficient
    gini_score = (1 - gini(char_freq)) ** 10

    return gini_score


def get_scores(
    words: List[str],
    scramble: List[str],
    tile_set_distribution: Dict[str, int]
) -> Tuple[List[str]]:
    _words = []
    scores = []
    for word in words:
        score = get_score(word, scramble, tile_set_distribution)
        if score is not None:
            _words.append(word)
            scores.append(score)

    return _words, scores


def get_scramble(words_set: set, num_words: int, tile_set_distribution: Dict[str, int]) -> List[str]:
    words = list(words_set)
    scramble = []

    for i in range(num_words):
        words, scores = get_scores(words, scramble, tile_set_distribution)
        if len(words) <= 0:
            print("Ran out of viable words")
            return scramble

        scores_normed = numpy.array(scores) / sum(scores)

        new_word = numpy.random.choice(words, p=scores_normed)
        #new_word = words[numpy.argmax(scores_normed)]
        #new_word = numpy.random.choice(words)

        scramble.append(new_word)
        words.remove(new_word)

    return scramble


if __name__ == "__main__":
    args = parser.parse_args()

    # load data and tile distribution
    category_sets = load_category_sets(args.category_sets_path)
    """ Used for testing
    my_text = "Call me Ishmael Some years ago--never mind how long precisely having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. It is a way I have of driving off the spleen and regulating the circulation. Whenever I find myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; whenever I find myself involuntarily pausing before coffin warehouses, and bringing up the rear of every funeral I meet; and especially whenever my hypos get such an upper hand of me, that it requires a strong moral principle to prevent me from deliberately stepping into the street, and methodically knocking people's hats off--then, I account it high time to get to sea as soon as I can. This is my substitute for pistol and ball. With a philosophical flourish Cato throws himself upon his sword; I quietly take to the ship. There is nothing surprising in this. If they but knew it, almost all men in their degree, some time or other, cherish very nearly the same feelings towards the ocean with me. There now is your insular city of the Manhattoes, belted round by wharves as Indian isles by coral reefs--commerce surrounds it with her surf. Right and left, the streets take you waterward. Its extreme downtown is the battery, where that noble mole is washed by waves, and cooled by breezes, which a few hours previous were out of sight of land Look at the crowds of water-gazers there. Circumambulate the city of a dreamy Sabbath afternoon. Go from Corlears Hook to Coenties Slip, and from thence, by Whitehall, northward. What do you see?--Posted like silent sentinels all around the town, stand thousands upon thousands of mortal men fixed in ocean reveries. Some leaning against the spiles; some seated upon the pier-heads; some looking over the bulwarks of ships from China; some high aloft in the rigging, as if striving to get a still better seaward peep. But these are all landsmen; of week days pent up in lath and plaster--tied to counters, nailed to benches, clinched to desks. How then is this? Are the green fields gone? What do they here?"
    my_text = my_text.lower()
    my_text = " ".join(re.findall("[a-z]+", my_text))
    category_sets = {
        "my_cat": set(my_text.split(" "))
    }
    """

    # load tile set distribution
    tile_set_distribution = load_tile_set_distribution(args.tile_set_path)
    tile_set_distribution = multiply_distribution(tile_set_distribution, args.num_tile_sets)

    # get a random category
    if len(category_sets.keys()) <= 0:
        raise ValueError("Category sets cannot be empty")
    
    category = (
        numpy.random.choice(list(category_sets.keys()))
        if args.category is None
        else args.category
    )

    # create the scramble
    words = [
        word
        for word in category_sets[category]
        if len(word) >= args.min_word_length and len(word) <= args.max_word_length
    ]
    scramble = get_scramble(words, args.num_words, tile_set_distribution)

    # print results
    scramble_name = f"{category}_{str(uuid.uuid4())[:8]}"
    scramble_path = os.path.join(args.scramble_dir, f"{scramble_name}.txt")
    scramble_char_freq = get_character_frequency(scramble)
    print_in_box(
        f"Category: {category}\n"
        f"Answer path: {scramble_path}\n"
        f"Gini Coeficient: {gini(scramble_char_freq):.3f}\n"
        f"Characters: {json.dumps(scramble_char_freq, indent=4)}"
    )
    plot_scramble_char_freq(scramble)

    # save results
    save_scramble(scramble, scramble_path)
