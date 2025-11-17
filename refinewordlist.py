import json
from typing import List


def load_lines(path: str, encoding: str = 'utf-16') -> List[str]:
    with open(path, 'r', encoding=encoding) as fh:
        return [line.split(' ')[0] for line in fh.read().splitlines()]


def main() -> None:
    lines = load_lines('en_full.txt')
    with open('official_wordle_dict.json', 'r', encoding='utf-8') as json_file:
        words = json.load(json_file)  # Just to ensure it's valid JSON

    #words = [word for word in lines if word in words]
    # Above line is faster but still takes a while and if I'm waiting I might as well have progress output even at a performance cost.
    valid_words = []
    precompute = (len(lines) % 1000)
    for index, word in enumerate(lines):
        if (index + 1) % 1000 == precompute: # Guarantees my 100% progress output
            print(f'{index / len(lines):.2%} words processed', end='\r')
        if word in words:
            valid_words.append(word)

    with open('words_dictionary.json', 'w', encoding='utf-8') as json_file:
        json.dump(valid_words, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()