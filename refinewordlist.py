import json
import string

ALLOWED_CHARS = set(string.ascii_letters)

with open('en_full.txt', 'r', encoding='utf-16') as file:
    lines = file.read().splitlines()

print(lines[:10])

# Filter for 5-letter, ASCII-only words
valid_words = []
for line in lines:
    word = line.split(' ')[0]
    if len(word) != 5:
        continue
    if all(char in ALLOWED_CHARS for char in word):
        valid_words.append(word)

print(f"Total 5-letter words found (STRICT ASCII): {len(valid_words)}")

with open('words_dictionary.json', 'w', encoding='utf-8') as json_file:
    json.dump(valid_words, json_file)