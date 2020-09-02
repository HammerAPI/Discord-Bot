import sys
import os
import re



def main(path):
    book = read_file(path)
    word_count = count_words(book)
    word_frequency = get_word_frequency(len(book), word_count)
    follow_word_count = get_follow_word_count(book, word_count)
    follow_word_frequency = get_follow_frequency(follow_word_count, word_count)


    """
    print("Word Count is:")
    print(word_count)
    print()

    print("Word Frequency is:")
    print(word_frequency)
    print()

    print("Follow Word Count is:")
    for key in follow_word_count:
        print(str(key) + " : " + str(follow_word_count[key]))
    print()

    print("Follow Word Frequency is:")
    for key in follow_word_frequency:
        print(str(key) + " : " + str(follow_word_frequency[key]))
    print()
    """
    print("Top 10 words:")
    display_first_items(word_count, 10)
    print()

    print("Top 10 word frequencies:")
    display_first_items(word_frequency, 10)
    print()

    print("Top 10 word followings:")
    display_first_items(follow_word_count, 10)
    print()

    print("Top 10 word following frequencies:")
    display_first_items(follow_word_frequency, 10)
    print()




def read_file(path):
    try:
        source_file = open(path, "r")
    except:
        print("\nError: '" + str(path) + "' not found on system.\n")
        exit(1)

    book = []
    for line in source_file:
        for word in line.split():
            book.append(re.sub('[^a-zA-Z]', '', word).lower())

    if len(book) is 0:
        print("\nError: Input file contains no valid words.\n")
    
    return book




def count_words(book):
    word_count = {}
    for word in book:
        if word in word_count.keys():
            word_count[word] += 1
        else:
            word_count[word] = 1

    return sort_dictionary(word_count, False)




def get_word_frequency(book_length, word_count):
    word_frequency = {}

    for word in word_count:
        word_frequency[word] = word_count[word] / book_length

    return sort_dictionary(word_frequency, False)




def get_follow_word_count(book, word_count):
    follow_word_count = {}

    for word in word_count:
        if word not in follow_word_count.keys():
            follow_word_count[word] = {}

    for i in range(len(book)):
        #if book[i] not in follow_word_count.keys():
        #    follow_word_count[book[i]] = {}

        if i < len(book) - 1:
            if book[i + 1] not in follow_word_count[book[i]].keys():
                follow_word_count[book[i]][book[i + 1]] = 1
            else:
                follow_word_count[book[i]][book[i + 1]] += 1
        else: 
            if book[0] not in follow_word_count[book[i]].keys():
                follow_word_count[book[i]][book[0]] = 1
            else:
                follow_word_count[book[i]][book[0]] += 1

    return sort_dictionary(follow_word_count, True)





def get_follow_frequency(follow_word_count, word_count):
    follow_word_frequency = {}

    for word in word_count.keys():
        follow_word_frequency[word] = {}

        for val in follow_word_count[word]:
            follow_word_frequency[word][val] = follow_word_count[word][val] / word_count[word]

    return sort_dictionary(follow_word_frequency, True)




# TODO: This isn't sorting follow_word_count properly
def sort_dictionary(dictionary, nested):
    sorted_dictionary = {}

    if not nested:
        #sorted_dictionary = {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}
        for word in sorted(dictionary, key = dictionary.get, reverse = True):
            sorted_dictionary[word] = dictionary[word]
    else:
         # Recursively sort all of the dictionary's contents
        for word in dictionary:
            sorted_dictionary[word] = sort_dictionary(dictionary[word], False)

    return sorted_dictionary


def display_first_items(dictionary, num_to_display):
    items = list(dictionary.keys())
    if num_to_display > len(items):
        num_to_display = len(items)
    
    #for i in range(0, len(items)):
    for i in range(0, num_to_display):
        if type(dictionary[items[i]]) is type(dict()):
            print("\n" + str(items[i]))
            #for val in dictionary[items[i]]:
            #    print("   " + str(val) + " : " + str(dictionary[items[i]][val]))
            display_first_items(dictionary[items[i]], num_to_display)
        else:
            print(str(items[i]) + " : " + str(dictionary[items[i]]))




if __name__ == "__main__":
    if len(sys.argv) is not 2:
        print("\nUsage: python3 word_count.py <path to input file>\n")
        exit(1)
    path = os.path.join("./input_files/", sys.argv[1])
    main(path)
