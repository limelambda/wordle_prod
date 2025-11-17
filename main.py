import json
import string
from typing import Dict, List, Optional


def load_words(file_path: str) -> List[str]:
    """Load a JSON list of words from ``file_path``."""
    with open(file_path, 'r') as file:
        words = json.load(file)

    return words


def filter_words(words: List[str], letters: Dict[str, List[int]],
                 green_letters: Dict[str, List[int]],
                 yellow_letters: List[str], grey_letters: set) -> List[str]:
    """Return words that satisfy the given positional and color constraints."""
    green_indices = [i for indices in green_letters.values() for i in indices]

    valid_words: List[str] = []
    for word in words:
        if check_word(word, letters, green_letters, yellow_letters,
                      grey_letters, green_indices):
            valid_words.append(word)

    return valid_words


def check_word(word: str, letters: Dict[str, List[int]],
               green_letters: Dict[str, List[int]],
               yellow_letters: List[str], grey_letters: set,
               green_indices: Optional[List[int]] = None) -> bool:
    """Return True if ``word`` matches the provided constraints.

    ``green_indices`` should be a list of indices that are already
    confirmed (green) and therefore excluded from grey-letter checks.
    """
    if green_indices is None:
        green_indices = []

    # Grey letters: none of the non-green positions may be in grey set
    for letter in (word[i] for i in range(len(word)) if i not in green_indices):
        if letter in grey_letters:
            return False

    # Green letters: confirmed positions must match
    for letter, indices in green_letters.items():
        for index in indices:
            if word[index] != letter:
                return False

    # Yellow letters: must appear somewhere in the word
    for letter in yellow_letters:
        if letter not in word:
            return False

    # Position constraints per letter
    for index, letter in enumerate(word):
        if index not in letters[letter]:
            return False

    return True


def position_probabilities(words: List[str]) -> List[Dict[str, float]]:
    """Compute letter frequency per position for 5-letter words.

    Returns a list of 5 dicts mapping letter -> probability.
    """
    positions = [{chr(i): 0.0 for i in range(ord('a'), ord('z') + 1)} for _ in range(5)]

    for word in words:
        for index, letter in enumerate(word):
            positions[index][letter] += 1

    # Normalize to probabilities (guard divide-by-zero)
    for position in positions:
        total = sum(position.values())
        if total:
            for letter in position:
                position[letter] /= total

    return positions


def main() -> None:
    words = load_words('words_dictionary.json')

    letters = {chr(i): [0, 1, 2, 3, 4] for i in range(ord('a'), ord('z') + 1)}
    green_letters = {chr(i): [] for i in range(ord('a'), ord('z') + 1)}
    yellow_letters: List[str] = []
    grey_letters = set()

    filtered_words = words.copy()

    while True:
        print('Please type in a word of your choice to use:', end=' ')
        pos_probs = position_probabilities(filtered_words)

        # Reorder filtered words based on letter-position probabilities,
        # word commonness (earlier in list is more common), and fewer
        # repeated letters. Limit to top 1000 to speed up sorting.

        def score(word: str) -> float:
            return (
                sum(pos_probs[i][ch] for i, ch in enumerate(word))
                - (filtered_words.index(word) / len(filtered_words))
                + (len(set(word)) / 5)
            )

        filtered_words = sorted(filtered_words[:1000], key=score, reverse=True)

        print(filtered_words[:75])

        user_word = input().strip()
        if not user_word:
            user_word = filtered_words[0]

        colors = input(
            'After inputing your word, type the *last* letter of each '
            'resulting color from the guess below\nEX: \u001b[33mw\u001b[37myy\u001b[32mn\u001b[37my\n'
        )

        # We do yellow -> green -> grey to solve double-letter issues
        for index, letter, color in zip(range(len(user_word)), user_word, colors):
            if color == 'w':  # Yellow letters
                letters[letter].remove(index)
                yellow_letters.append(letter)
        for index, letter, color in zip(range(len(user_word)), user_word, colors):
            if color == 'n':
                green_letters[letter].append(index)
        for index, letter, color in zip(range(len(user_word)), user_word, colors):
            if color == 'y':  # Grey letters
                letters[letter].remove(index)
                if letter in yellow_letters or green_letters[letter] != []:
                    continue # Could do some stuff to limit to 1 instance of a letter but~
                grey_letters.add(letter)

        filtered_words = filter_words(words, letters, green_letters, yellow_letters, grey_letters)


if __name__ == '__main__':
    main()
