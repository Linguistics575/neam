#!/usr/bin/python3
import re
import sys

correspondences = {
    '': re.compile('\ufeff'),
    "'": re.compile('[\u2018\u2019]')
}


def main():
    file_name = sys.argv[1]

    with open(file_name, encoding='utf-8') as input_file:
        for line in input_file:
            print(asciify(line), end='')


def asciify(text):
    for replacement, pattern in correspondences.items():
        text = pattern.sub(replacement, text)

    return text


if __name__ == '__main__':
    main()

