import json
import string
from typing import List


ALLOWED_CHARS = set(string.ascii_lowercase)


def load_lines(path: str, encoding: str = 'utf-16') -> List[str]:
    with open(path, 'r', encoding=encoding) as fh:
        return fh.read().splitlines()


def extract_valid_words(lines: List[str]) -> List[str]:
    """Return 5-letter ASCII-only words from the provided lines."""
    valid = []
    for line in lines:
        word = line.split(' ')[0].lower()
        if len(word) != 5:
            continue
        if all(char in ALLOWED_CHARS for char in word):
            valid.append(word)

    return valid


def main() -> None:
    lines = load_lines('en_full.txt')
    words = extract_valid_words(lines)

    print(f'Total 5-letter words found (STRICT ASCII): {len(words)}')

    with open('words_dictionary.json', 'w', encoding='utf-8') as json_file:
        json.dump(words, json_file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()