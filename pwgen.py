#!/usr/bin/env python3
import math
from argparse import ArgumentParser
import secrets

WORDLIST_FILENAME = "wordlist"
DEFAULT_NUM_WORDS = 5
DEFAULT_NUM_CHARS = 4
# charset that results in a password with the lowest possible number of keystrokes on my keyboard:
CHARSET = "1234567890qwertyuiopasdfghjklzxcvbnm[];'\\,./`"


def read_wordlist():
    with open(WORDLIST_FILENAME, 'r') as f:
        return f.read().splitlines()


def new_password(num_words=DEFAULT_NUM_WORDS, num_chars=DEFAULT_NUM_CHARS):
    words = ' '.join(secrets.choice(WORDLIST) for x in range(num_words))
    chars = ''.join(secrets.choice(CHARSET) for x in range(num_chars))

    return "{} {}".format(words, chars)


def get_entropy(num_words, num_chars):
    return int(math.log(len(WORDLIST)**num_words, 2) +
               math.log(len(CHARSET)**num_chars, 2))


def get_cracktime(entropy):
    hashrate = 1600000 * 1000000000000 * 86400 / 1000
    return round((2**entropy) / hashrate)


def cli_args():
    parser = ArgumentParser(description='''Passphrase generator.\n
    Time to crack is how long it would take all Bitcoin mining power to crack the password when
    it is hashed with 2 iterations of sha256.''')
    parser.add_argument("-w", "--num-words", nargs='?', default=DEFAULT_NUM_WORDS, type=int,
                        help='Number of random words to generate (default: %d)' % DEFAULT_NUM_WORDS)
    parser.add_argument("-c", "--num-chars", nargs='?', default=DEFAULT_NUM_CHARS, type=int,
                        help='Number of random characters to generate (default: %d)' % DEFAULT_NUM_CHARS)
    return parser.parse_args()


WORDLIST = read_wordlist()


def main():
    args = cli_args()
    password = new_password(args.num_words, args.num_chars)
    ent = get_entropy(args.num_words, args.num_chars)

    print('Password:', password)
    print('Strength:', ent, 'bits')
    cracktime = get_cracktime(ent)
    print("Time to Crack:", cracktime, 'days')


if __name__ == '__main__':
    main()
