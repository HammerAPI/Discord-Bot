import sys
import time
import os
import asyncio

# Global variables used by all methods to hold words
source_file = "words_alpha.txt"
path = os.path.join("./input_files/", source_file)
# Checks that both words are the same length and found in the dictionary


def check_words(dictionary, start_word, end_word):
    if start_word not in dictionary:
        return start_word + " is not in the dictionary", None

    if end_word not in dictionary:
        return end_word + " is not in the dictionary", None

    if len(start_word) != len(end_word):
        return "Provided words are not the same length", None

    return "Attempting to find ladder between " + start_word + " and " + end_word, ""


# Creates a list of all words found in the provided text file
def build_dictionary():
    dictionary = []
    with open(path) as f:
        for line in f:
            dictionary.append(line.strip().replace("\n", ""))
    return dictionary


# Builds a list of all words with the same length as the starting word
def build_word_list(dictionary, length):
    word_list = []
    for word in dictionary:
        if len(word) == length:
            word_list.append(word)
    return word_list


# Returns a list of words one letter different than the passed word
def get_words_one_letter_away(word_list, base_word):
    one_letter_away = []

    for word in word_list:
        letters_different = 0
        for i in range(0, len(word)):
            if word[i] != base_word[i]:
                letters_different += 1
        if letters_different == 1:
            one_letter_away.append(word)
    return one_letter_away


# Returns a list of words one letter away from their neighors that link the
# starting word and the ending word
def build_ladder(word_list, start, end):
    ladder = []
    list_of_ladders = []
    used_words = []
    one_away = get_words_one_letter_away(word_list, start)

    ladder.append(start)
    used_words.append(start)
    list_of_ladders.append(ladder)

    start_time = time.time()
    while list_of_ladders and (time.time() - start_time) < 120:

        # Retrieve the top ladder on the list
        ladder = list_of_ladders.pop(0)
        one_away = get_words_one_letter_away(word_list, ladder[-1])

        # For every word one letter away from the ladder's top,
        # Clone the ladder and append the new word onto it
        for word in one_away:
            if time.time() - start_time > 120:
                return None
            if word not in ladder and word not in used_words:
                ladder.append(word)

                # If the top of the ladder is the start word, return it
                if ladder[-1] == end:
                    return ladder

                used_words.extend(ladder)

                new_ladder = []
                new_ladder.extend(ladder)

                list_of_ladders.append(new_ladder)
                ladder.remove(word)
