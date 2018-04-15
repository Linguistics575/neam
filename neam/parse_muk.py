#!/usr/bin/python3
"""
parse_muk.py

Takes a named entity-tagged MUK corpus and converts it to a format that can be used to
train the Stanford NER. Acceptable inputs are either the name of a file containing a MUK
corpus, or the name of a folder containing only MUK tagged corpus files.

:author: Graham Still
"""
import sys
import re
from os import listdir
from os.path import isfile, isdir, join
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize as _word_tokenize

""" The parser BeautifulSoup should use """
BS4_PARSER = 'html5lib'

""" Tags that are just for formatting, and can be safely unwrapped """
UNWRAPPABLE = ['p', 's']

""" Tags that occur in the body but don't contribute anything """
DECOMPOSABLE = ['trailer']

""" The possible tags that could hold the main body of an article """
TEXT_TAGS = ['text', 'txt']

""" The tag indicating a named entity """
NER_TAG = 'enamex'

""" The named entities we care about """
TAGS_OF_INTEREST = ['PERSON', 'ORGANIZATION', 'LOCATION']

""" The tag to assign to a non-named entity """
OUTSIDE_TAG = 'O'

""" The attribute that holds the type of NER """
TYPE_ATTR = 'type'


def main():
    name = sys.argv[1]

    if isfile(name):
        print(parse(name))
    elif isdir(name):
        listing = [join(name, f) for f in listdir(name)]
        parses = [parse(f) for f in listing if isfile(f)]
        for parse in parses:
            print(parse)
    else:
        print('Error: {} is not the name of a file or directory.'.format(name),
                file=sys.stderr)


def parse(file_name):
    """
    Parses a tagged XML file

    :type file_name: str
    :return: A string of tab-separated token/entity tag lines
    """
    with open(file_name) as muk_file:
        soup = BeautifulSoup(muk_file, BS4_PARSER)

    for el in soup.find_all(UNWRAPPABLE):
        el.unwrap()

    for el in soup.find_all(DECOMPOSABLE):
        el.decompose()

    return '\n'.join(tag_elements(soup.find_all(TEXT_TAGS)))


def tag_elements(els):
    """
    Tags all the words in a list of elements

    :param els: A list of BeautifulSoup tags
    :return: A list of strings, which are tab-separated words and NE tag pairs
    """
    tagged = []

    for el in els:
        for segment in el.contents:
            tag = OUTSIDE_TAG

            if not isinstance(segment, str):
                if segment[TYPE_ATTR] in TAGS_OF_INTEREST:
                    tag = segment[TYPE_ATTR]
                segment = segment.string

            tagged += tag_sequence(segment, tag)

    return tagged


def tag_sequence(sequence, tag):
    """
    Tags all of the words in a sequence with a given tag

    :type sequence: str
    :type tag: str
    :return: A list of strings, which are tab-separated words and NE tag pairs
    """
    tokens = word_tokenize(sequence, tag != OUTSIDE_TAG)
    return ["{}\t{}".format(token, tag) for token in tokens]


def word_tokenize(sequence, ne = False):
    """
    Tokenizes a sequence

    Wraps NLTK's word_tokenize. Since NLTK's version expects a sentence, it gets confused
    when a NE like "N.A.S.A." is passed in, and thinks that the last period is the end of
    the sentence. This wrapper glues the last period back onto the second last token if
    the sequence is identified as a named entity.

    :param sequence: A string of words to tokenize
    :param ne: Whether the sequence is a named entity or not
    :type ne: bool
    :return: A list of tokens
    """
    tokens = _word_tokenize(sequence)

    if ne and tokens[-1] == '.':
        tokens[-2] += '.'
        tokens = tokens[:-1]

    return tokens


if __name__ == '__main__':
    main()

