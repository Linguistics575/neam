#!/usr/bin/python3
import sys
from bs4 import BeautifulSoup
"""
Adds appropriate spacing to a TEI string

:author: Graham Still
"""

"""
The parser BeautifulSoup should use
"""
SOUP_PARSER = 'xml'

"""
The string to use for indentation
"""
TAB = '  '


IGNORE_TAGS = ['p']


def load_soup():
    """
    Loads the XML file into a BeautifulSoup object

    If a command line argument was passed, uses that as the name of the file to open. If
    not, reads from stdin.

    :rtype: BeautifulSoup
    """
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as soup_file:
            soup = BeautifulSoup(soup_file, SOUP_PARSER)
    else:
        soup = BeautifulSoup(sys.stdin, SOUP_PARSER)

    return soup.body


def recursive_print(soup, depth = 0):
    """
    Prints a BeautifulSoup tag recursively

    If the tag is in the IGNORE_TAGS list, it will be printed out without formatting.

    :param soup: A BeautifulSoup tag
    :param depth: The current indentation depth
    """
    indent = TAB * depth

    if soup.name in IGNORE_TAGS:
        print(indent + str(soup))
    else:
        print(indent + open_tag(soup))

        for child in soup.children:
            recursive_print(child, depth + 1)

        print(indent + close_tag(soup))


def open_tag(tag):
    """
    Generates an opening tag string for a given tag

    :param tag: A BeautifulSoup tag
    :return: The string that would open the tag, including any attributes
    :rtype: str
    """
    attrs = ' '.join(['{}="{}"'.format(id, value) for id, value in tag.attrs.items()])
    if attrs: attrs = ' ' + attrs

    return '<{}{}>'.format(tag.name, attrs)


def close_tag(tag):
    """
    Generates a closing tag string for a given tag
    :param tag: A BeautifulSoup tag
    :return: The string that would close the tag
    :rtype: str
    """
    return '</{}>'.format(tag.name)


if __name__ == '__main__':
    recursive_print(load_soup())
