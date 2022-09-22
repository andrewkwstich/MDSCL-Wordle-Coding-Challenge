# Imports
from collections import defaultdict
import string

file_path = ""

# Task 1

# Creating list of English words

with open(file_path + "English6.txt") as f1:
    english_list = [line.strip() for line in f1.readlines()]
    

# Solution to Task 1


def make_guess(file, guess_count=4):
    """
    Given a text file and the number of previous attempts, outputs a guess.

    Parameters:
        file (txt file): a text file assumed to contain one word per line.
        guess_count (int): the number of guesses already made for a particular word.

    Returns:
        guess (str): the most likely word according to the algorithm.
    """

    with open(file_path + file) as f:
        word_list = [line.strip() for line in f.readlines()]

    letters = []  # List of characters in word list

    eng_dictionary = defaultdict(list)  # Dictionary mapping letters to frequency in each word position

    for word in word_list:  # Populating `letters`
        for letter in word:
            if letter not in letters:
                letters.append(letter)

    for i in range(6):  # Populating dictionary
        for letter in letters:
            counter = 0
            for word in word_list:
                if word[i] == letter:
                    counter += 1
            eng_dictionary[letter].append(counter)

    best_sum = -1

    for word in word_list:
        used_letters = set()
        current_sum = 0
        for i, char in enumerate(word):
            letr_pos_val = eng_dictionary[char][i]
            if char not in used_letters:
                current_sum += letr_pos_val
            else:  # Penalize letters already included in guess
                mult = 0.25 * max(guess_count, 1)
                current_sum += letr_pos_val * min(mult, 1)  # Reduce penalty as guesses increase
            used_letters.add(char)
        if current_sum > best_sum:
            best_sum = current_sum
            guess = word

    return guess

# Task 2

# Creating list of Gitksan words

with open(file_path + "Gitksan5.txt") as f1:
    gitksan_list = [line.split("\t")[0] for line in f1.readlines()]


# Defining a dictionary to use in grapheme conversion

polygraphs = ["kw",
              "k_",
              "gy",
              "gw",
              "ts",
              "p'",
              "t'",
              "ky'",
              "kw'",
              "k_'",
              "ts'",
              "tl'",
              "xw",
              "x_",
              "hl",
              "'m",
              "'l",
              "'n",
              "'y",
              "'w",
              "ii",
              "ee",
              "aa",
              "oo",
              "uu",
              "k'",
              "g_",
              "a'a",
              "e'e",
              "i'i",
              "o'o",
              "u'u"]

subs = {}

alphabet = list(string.ascii_uppercase)  # For single-character ciphers; Gitksan words do not use uppercase

for i, graph in enumerate(polygraphs):
    if i < len(alphabet):
        subs[graph] = alphabet[i]
    else:
        subs[graph] = str(i-len(alphabet))
        
# Defining relevant character classes for encoding
        
velars = ["k", "g", "x"]

vowels = ["a", "e", "i", "o", "u"]

resonants = ["m", "n", "l", "y", "w"]

glides = ["y", "w", "_"]

voiceless_stops = ["p", "t", "k"]

triggers = velars + vowels + ["h", "p", "t", "'"]

# Defining rules to use in encoding words

def velar_rule(char1, char2, char3):

    seq = char1
    if char2 in glides:
        seq += char2
        if char3 == "'":
            seq += char3
    elif char1 == "k" and char2 == "'":
        seq += char2

    return seq

def vowel_rule(char1, char2, char3, char4):
    
    seq = char1
    if char2 == "'":
        if char3 == char1:
            seq += char2+char3
    elif char2 == char1:
        if char3 != "'" or (char3 == "'" and char4 in resonants):
            seq += char2

    return seq

def resonant_rule(char1, char2):
    
    return char1 + char2

def voiceless_rule(char1, char2, char3):
    
    seq = char1
    if char2 == "'" or (char1 == "t" and char2 == "s"):
        seq += char2
        if char3 == "'":
            seq += char3
    elif char2 == "l" and char3 == "'":
        seq += char2+char3
            
    return seq
            
def hl_rule(char1, char2):
    
    return char1 + char2

# Defining rule that uses the above rules to encode words


def encode_word(word, mode="encode"):
    """
    Encodes a Gitksan word for stats collection and analysis to aid in guessing.
    Can also be used to decode words so that the appropriate items from the active list
    can be removed.

    Parameters:
        word (str): a list of lowercase characters spelling a Gitksan word.
        mode (str): "encode" or "decode"

    Returns:
        enc (str): a word encoding digraphs and trigraphs as single arbitrary letters.
    """

    if mode == "decode":
        subs_rev = {v: k for k, v in subs.items()}
        dec = ""
        for char in word:
            if char in subs_rev:
                dec += subs_rev[char]
            else:
                dec += char
        return dec

    enc = ""

    i = 0

    while i < len(word):
        char1 = word[i]
        seq = char1
        if i < len(word)-1:
            char2 = word[i+1]
        else:
            char2 = ""
            break
        if i < len(word)-2:
            char3 = word[i+2]
        else:
            char3 = ""
        if i < len(word)-3:
            char4 = word[i+3]
        else:
            char4 = ""
        if char1 in triggers:
            if char1 in velars:
                seq = velar_rule(char1, char2, char3)
            elif char1 in vowels:
                seq = vowel_rule(char1, char2, char3, char4)
            elif char1 == "'" and char2 in resonants:
                seq = resonant_rule(char1, char2)
            elif char1 in voiceless_stops:
                seq = voiceless_rule(char1, char2, char3)
            elif char1 == "h" and char2 == "l":
                seq = hl_rule(char1, char2)
        if len(seq) == 1:
            enc += seq
        else:
            enc += subs[seq]
        i += len(seq)

    if not char2:
        enc += word[-1]

    return enc

# Testing the above function

for word in gitksan_list:
    assert len(encode_word(word)) == 5
    
for word in gitksan_list:
    assert word == encode_word(encode_word(word), "decode")


# Solution to Task 2


def make_guess_gitksan(file, guess_count=3):
    """
    Given a text file and the number of previous attempts, outputs a wordle guess.

    Assumes the words are in Gitksan and transcribed as in the instructions.

    Parameters:
        file (txt file): a text file assumed to contain one word per line.
        guess_count (int): the number of guesses already made for a particular word.

    Returns:
        guess (str): the most likely word according to the algorithm.
    """

    with open(file_path + file) as f:
        word_list = [line.split("\t")[0].strip() for line in f.readlines()]

    enc_word_list = [encode_word(word) for word in word_list]

    letters = []  # List of characters in word list

    git_dictionary = defaultdict(list)  # Dictionary mapping letters to frequency in each word position

    for word in enc_word_list:  # Populating `letters`
        for letter in word:
            if letter not in letters:
                letters.append(letter)

    for i in range(5):  # Populating dictionary
        for letter in letters:
            counter = 0
            for word in enc_word_list:
                if word[i] == letter:
                    counter += 1
            git_dictionary[letter].append(counter)

    best_sum = -1

    for word in enc_word_list:
        used_letters = set()
        current_sum = 0
        for i, char in enumerate(word):
            letr_pos_val = git_dictionary[char][i]
            if char not in used_letters:
                current_sum += letr_pos_val
            else:  # Penalize letters already included in guess
                mult = 0.25 * max(guess_count, 1)
                current_sum += letr_pos_val * min(mult, 1)  # Reduce penalty as guesses increase
            used_letters.add(char)
        if current_sum > best_sum:
            best_sum = current_sum
            guess = word

    return guess