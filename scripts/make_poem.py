import word_count as wc
import sys
import os
import random


def main(path, num_stanzas, lines_per_stanza, words_per_line):
    book = wc.read_file(path)
    word_count = wc.count_words(book)
    word_frequency = wc.get_word_frequency(len(book), word_count)
    follow_word_count = wc.get_follow_word_count(book, word_count)
    follow_word_frequency = wc.get_follow_frequency(follow_word_count, word_count)

    poem = make_poem(word_frequency, follow_word_frequency, num_stanzas, lines_per_stanza, words_per_line)
    return poem
    #print(poem)




def make_poem(word_frequency, follow_word_frequency, num_stanzas, lines_per_stanza, words_per_line):
    current_word = get_first_word(word_frequency)
    poem = current_word + " "
    next_word = ""

    for i in range(1, num_stanzas * lines_per_stanza * words_per_line):
        if i % words_per_line is 0:
            poem = poem + "\n"
            
            if i % (lines_per_stanza * words_per_line) is 0:
                poem = poem + "\n"

        next_word = get_next_word(follow_word_frequency[current_word])
        poem = poem + next_word + " "
        current_word = next_word
    return poem




def get_first_word(word_frequency):
    first_word_probability = random.random()
    high = 0
    low = 0

    for word in word_frequency:
        low = high
        high += word_frequency[word]
        if first_word_probability >= low and first_word_probability <= high:
            return word




def get_next_word(follow_word_frequency):
    current_word_probability = random.random()
    high = 0
    low = 0

    for word in follow_word_frequency:
        low = high
        high += follow_word_frequency[word]
        if current_word_probability >= low and current_word_probability <= high:
            return word




if __name__ == "__main__":
    if len(sys.argv) is not 5:
        print("USAGE")
        exit(1)
    path = os.path.join("./input_files/", sys.argv[1])
    num_stanzas = eval(sys.argv[2])
    lines_per_stanza = eval(sys.argv[3])
    words_per_line = eval(sys.argv[4])

    main(path, num_stanzas, lines_per_stanza, words_per_line)
