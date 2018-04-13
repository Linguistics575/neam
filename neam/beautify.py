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


def main():
    body = load_soup()
    builder = []

    builder.append(open_tag(body))

    for div in body.find_all('div'):
        print(TAB + open_tag(div))

        # The <P> tags should not receive any special formatting; just print them directly
        for p in div.find_all('p'):
            builder.append(TAB*2 + str(p))

        builder.append(TAB + close_tag(div))

    builder.append(close_tag(body))

    print('\n'.join(builder))


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


def open_tag(tag):
    """
    Generates an opening tag string for a given tag

    :param tag: A BeautifulSoup tag
    :return: The string that would open the tag, including any attributes
    :rtype: str
    """
    attrs = ['{}="{}"'.format(id, value) for id, value in tag.attrs.items()]
    return '<{} {}>'.format(tag.name, ' '.join(attrs))


def close_tag(tag):
    """
    Generates a closing tag string for a given tag
    :param tag: A BeautifulSoup tag
    :return: The string that would close the tag
    :rtype: str
    """
    return '</{}>'.format(tag.name)


main()
