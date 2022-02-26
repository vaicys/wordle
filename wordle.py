import re


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


def sort_words_by_letter_frequency(words):
    word_scores = []
    letter_frequencies = calculate_letter_frequencies(words)

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


def sort_words_by_deviation_from_mean(words):
    word_scores = []
    letter_frequencies = calculate_letter_frequencies(words)
    dict_values = letter_frequencies.values()
    average_frequency = sum(dict_values) / len(dict_values)

    for word in words:
        score = 0
        for letter in word:
            score += abs(letter_frequencies[letter] - average_frequency)
        word_scores.append((word, score))
    word_scores.sort(key=lambda x: x[1])
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
    return [x for x in words if x[pos] != letter and x.find(letter) != -1]


def letters_dont_exist(words, cmd):
    pattern = f".*[{cmd[1:]}].*"
    return [x for x in words if not re.match(pattern, x)]


def process_command(words, cmd):
    if cmd.find("!") != -1:
        return negative_match(words, cmd)
    elif cmd.startswith("-"):
        return letters_dont_exist(words, cmd)
    return positive_match(words, cmd)


def main():
    words = read_words()

    print("Commands: [pos][letter] [pos]![letter] -[letter1]..[letterN]")
    print("Multiple commands allowed, separate by space.")
    print("Example: -adiu 5!e 1r")

    starting_words = sort_words_by_letter_frequency(words)
    print_top_words(starting_words)

    while True:
        print("Command(s): ", end="")
        commands = input()
        for cmd in commands.split(" "):
            words = process_command(words, cmd)

        words = sort_words_by_deviation_from_mean(words)
        print_top_words(words)


main()
