def read_words():
    word_file = open("wordlist.txt", "r")
    words = word_file.read().splitlines()
    word_file.close()
    return words

def calculate_letter_frequencies(words):
    letter_frequencies = {}
    for word in words:
        for letter in word:
            if letter not in letter_frequencies:
                letter_frequencies[letter] = 1
            else:
                letter_frequencies[letter] += 1
    return letter_frequencies

def sort_words_by_score(words, letter_frequencies):
    word_scores = []
    for word in words:
        current_word = []
        score = 0
        for letter in word:
            if letter in current_word:
                # ignore words with duplicate letters
                score = 0
                break
            current_word.append(letter)
            score += letter_frequencies[letter]
        if score > 0:
            word_scores.append((word, score))
    word_scores.sort(reverse=True, key=lambda x: x[1])
    return [x[0] for x in word_scores]

def print_top_words(words):
    print()
    print(f"Current best words ({len(words)}):")
    for i in range(min(10, len(words))):
        print(words[i])
    print()

def positive_match(words, cmd):
    pos = int(cmd[0]) - 1
    letter = cmd[1]
    return [x for x in words if x[pos] == letter]

def negative_match(words, cmd):
    pos = int(cmd[0]) - 1
    letter = cmd[2]
    result = []
    for word in words:
        if word[pos] == letter:
            continue
        letter_pos = word.find(letter)
        if letter_pos == -1:
            continue
        if letter_pos == pos:
            letter_pos = word.find(letter, pos + 1)
            if letter_pos == -1:
                continue
        result.append(word)
        1
    return result

def letters_dont_exist(words, cmd):
    letters = [x for x in cmd if x != "-"]
    result = []
    for word in words:
        found = False
        for letter in letters:
            if letter in word:
                found = True
                break;
        if found: continue
        result.append(word)
    return result

def process_command(words, cmd):
    if cmd.find("!") != -1:
        return negative_match(words, cmd)
    elif cmd.startswith("-"):
        return letters_dont_exist(words, cmd)
    return positive_match(words, cmd)

def main():
    words = read_words()
    letter_frequencies = calculate_letter_frequencies(words)
    sorted_words = sort_words_by_score(words, letter_frequencies)

    print("Commands: [pos][letter] [pos]![letter] -[letter1]..[letterN]")
    print("Multiple commands allowed, separate by space.")
    print("Example: -adiu 5!e 1r")

    while True:
        print_top_words(sorted_words)
        print("Command(s): ", end="")
        commands = input()
        for cmd in commands.split(" "):
            sorted_words = process_command(sorted_words, cmd)

main()
