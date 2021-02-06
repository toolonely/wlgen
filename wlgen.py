#!/usr/bin/env python3

"""wlgen - a wordlist generator"""

import os
import time

APP_NAME = "wlgen"
STATE_DIR = "~/.local/share/{}".format(APP_NAME)
ABS_STATE_DIR = os.path.expanduser(STATE_DIR)
STATE_FILE = "state"
ABS_STATE_FILE = os.path.join(ABS_STATE_DIR, STATE_FILE)
FILE_SIZE = 1024 * 1024 * 20  # 25MB
WORDLIST_FILE = "/dev/shm/words"
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.!?,-_ "


class WlgenException(Exception):
    pass


class LastCharException(WlgenException):
    """
    Raised when a char is last char in the alphabet
    """
    def __init__(self, char, alphabet):
        """
        Args:
            char (chr): char

            alphabet (str): alphabet
        """
        self.char = char
        self.alphabet = alphabet

    def __str__(self):
        ret = (
            "Char '{}' is the last char "
            "in alphabet '{}'"
        ).format(self.char, self.alphabet)


def next_char(char, alphabet):
    """
    Return next char from alphabet

    Args:
        char (chr): char

        alphabet (str): alphabet
    """
    index = alphabet.index(char)
    if index == len(alphabet) - 1:
        raise LastCharException(char, alphabet)
    return alphabet[index + 1]


def next(password, alphabet):
    """
    Return next password
    
    Args:
        password (str): password
        
        alphabet (str): alphabet
    """
    if password == "":
        return alphabet[0]
    chars = list(password)
    first_char = alphabet[0]
    last_char = alphabet[-1]
    i = len(chars) - 1
    while chars[i] == last_char:
        chars[i] = first_char
        i -= 1
    if i == -1:
        chars.insert(0, first_char)
    else:
        chars[i] = next_char(chars[i], alphabet)
    return "".join(chars)


def generate_words(first_password, alphabet, words_file, max_words_file_size):
    """
    Generate words and write them to a file

    Args:
        first_password (str): first password

        alphabet (str): alphabet

        words_file (str): words file name

        max_words_file_size (int): max words file size in bytes
    """
    size = 0
    current_password = first_password
    passwords = []
    list_append = passwords.append
    start_time = time.time()
    while size < max_words_file_size:
        next_password = next(current_password, alphabet)
        size += len(next_password)
        list_append(next_password)
        current_password = next_password
    end_time = time.time()
    total_time = end_time - start_time
    print("Generated {} passwords in {:.2f} seconds".format(len(passwords), total_time))
    with open(words_file, "w") as f:
        f.write("\n".join(passwords))


def save_state(state_file, words_file):
    """
    Save last password in the state file

    Args:
        state_file (str): state file name

        words_file (str): words file name
    """
    with open(words_file, "rb") as f:
        f.seek(-80, 2)  # read a few bytes from the end
        lines = f.readlines()
        last_password = lines[-1].decode()
        print("Last password is '{}'".format(last_password))
        with open(state_file, "w") as f1:
            f1.write(last_password)


def main():
    """main"""
    if not os.path.isdir(ABS_STATE_DIR):
        os.mkdir(ABS_STATE_DIR, mode=0o700)
    if os.path.isfile(ABS_STATE_FILE):
        with open(ABS_STATE_FILE) as f:
            line = f.readline()
            first_password = line
    else:
        first_password = ""
    print("Previous last password is '{}'".format(first_password))
    generate_words(first_password, ALPHABET, WORDLIST_FILE, FILE_SIZE)
    save_state(ABS_STATE_FILE, WORDLIST_FILE)


if __name__ == "__main__":
    main()
