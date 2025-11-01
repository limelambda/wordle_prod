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

def main():
    words = load_words('words_dictionary.json')
    letters = {chr(i): [0,1,2,3,4] for i in range(ord('a'), ord('z')+1)}
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
    filtered_words = words
    while True:
        print("Please type in a word of your choice to use:")
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
        filtered_words = filter_words(words, letters, green_letters, yellow_letters, grey_letters)

if __name__ == "__main__":
    main()
