import json

def load_words(file_path):
    with open(file_path, 'r') as file:
        words = json.load(file)
    return words

def filter_words(words, letters, green_letters, yellow_letters, grey_letters):
    valid_words = []

    # Just doing this here to reduce redundant work
    green_indices = []
    for green_index in green_letters.values():
        green_indices.extend(green_index)
    
    for word in words:
        if check_word(word, letters, green_letters, yellow_letters, grey_letters, green_indices):
            valid_words.append(word)
    return valid_words

def check_word(word, letters, green_letters, yellow_letters, grey_letters, green_indices=[]):
    for letter in [word[letter_index] for letter_index in range(len(word)) if not letter_index in green_indices]: # Grey letters
        if letter in grey_letters:
            return False
    for letter, indices in green_letters.items(): # Green letters
        for index in indices:
            if word[index] != letter:
                return False
    for letter in yellow_letters: # Yellow letters pt1
        if not letter in word:
            return False
    for index, letter in enumerate(word): # Yellow letters pt2
        if not index in letters[letter]:
            return False
    return True

def postiton_proabilities(words):
    out = [{chr(i): 0 for i in range(ord('a'), ord('z')+1)} for i in range(5)] # 5 letter words
    for word in words:
        for index, letter in enumerate(word):
            out[index][letter] += 1
    # Normalize
    for position in out:
        total = sum(position.values())
        for letter in position:
            position[letter] /= total
    return out

def main():
    WORDS = load_words('words_dictionary.json')
    letters = {chr(i): [0,1,2,3,4] for i in range(ord('a'), ord('z')+1)} # 5 letter words
    green_letters = {chr(i): [] for i in range(ord('a'), ord('z')+1)}
    yellow_letters = []
    grey_letters = set()
    #
    #yellow_letters = ['t', 'e']
    #letters['t'] = [0,1,2,4]
    #letters['e'] = [0,1,2,3]
    #grey_letters.add('c')
    #grey_letters.add('r')
    #grey_letters.add('a')
    #print(check_word('motel', letters, green_letters, yellow_letters, grey_letters))
    #
    print("For your first guess, you can use any 5 letter word, crate is recommended!")
    filtered_words = WORDS.copy()
    while True:
        print("Please type in a word of your choice to use:")
        Position_probabilities = postiton_proabilities(filtered_words)
        # Reorder filtered words based on letter position probabilities, word commonness, and wether it has repeated letters
        # Propably should evetually adjust weights
        filtered_words = sorted(filtered_words[:1000], key=lambda word: ( # Limit to top 1000 to speed up sorting
            sum(Position_probabilities[index][letter] for index, letter in enumerate(word)) + # Letter position probabilities
            -(filtered_words.index(word) / len(filtered_words)) + # Word commonness (earlier in list is more common)
            len(set(word)) / 5 # Fewer repeated letters
        ), reverse=True)
        print(filtered_words[:75])  # Print only top 75 words
        user_word = input()
        if user_word == '':
            user_word = filtered_words[0]
        colors = input("After inputing your word, type the *last* letter of each resulting color from the guess below\nEX: \u001b[33mw\u001b[37myy\u001b[32mn\u001b[37my\n")
        for index, letter, color in zip(range(len(user_word)), user_word, colors):
            if color == 'y': # Grey letters
                grey_letters.add(letter)
            elif color == 'w': # Yellow letters
                letters[letter].remove(index)
                yellow_letters.append(letter)
            elif color == 'n':
                green_letters[letter].append(index)
        filtered_words = filter_words(WORDS, letters, green_letters, yellow_letters, grey_letters)

if __name__ == "__main__":
    main()
