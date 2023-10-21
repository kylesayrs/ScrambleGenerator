from typing import Dict, List

import numpy
import matplotlib.pyplot as plt


def multiply_distribution(distribution: Dict[str, int], scalar: int) -> Dict[str, int]:
    return {
        key: value * scalar
        for key, value in distribution.items()
    }


def gini(distribution: Dict[str, int]) -> float:
    values = list(distribution.values())

    mean_absolute_differences = numpy.mean(
        numpy.abs(numpy.subtract.outer(values, values))
    )
    return 0.5 * mean_absolute_differences / numpy.mean(values)


def get_character_frequency(words: List[str]) -> Dict[str, int]:
    characters = numpy.array([c for c in "".join(words)])
    all_characters = [chr(i) for i in range(97, 123)]

    return {
        character: int(numpy.sum(characters == character))
        for character in all_characters
    }


def plot_scramble_char_freq(scramble: List[str]):
    plt.bar([chr(i) for i in range(97, 123)], list(get_character_frequency(scramble).values()))
    plt.show()
