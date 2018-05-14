from bs4 import BeautifulSoup
from neam.python.classification.processing import NEAMProcessor

class Beautifier(NEAMProcessor):
    """
    Adds indentation to XML text
    """
    def __init__(self, tab = '  ', parser = 'xml', ignore = None):
        """
        Initializes the processor

        :param tab: The string to use as a tab. Defaults to two spaces.
        :type tab: str
        :param parser: The parser BeautifulSoup should use to load the soup
        :type parser: str
        :ignore: The tags that should not be formatted. Defaults to P tags.
        :type ignore: list of str
        """
        self._tab = tab
        self._parser = parser
        self._ignore_tags = ignore or ['p', 'pb']

    def run(self, text):
        soup = BeautifulSoup(text, self._parser).contents[0]
        return '\n'.join(self._beautify(soup, 0, []))

    def _beautify(self, soup, depth, builder):
        """
        Adds a BeautifulSoup tag to the builder recursively

        If the tag is in the IGNORE_TAGS list, it will be printed out without formatting.

        :param soup: A BeautifulSoup tag
        :param depth: The current indentation depth
        """
        indent = self._tab * depth

        if isinstance(soup, str) or soup.name in self._ignore_tags:
            builder.append(indent + str(soup))
        else:
            builder.append(indent + self._open_tag(soup))

            for child in soup.children:
                self._beautify(child, depth + 1, builder)

            builder.append(indent + self._close_tag(soup))

        return builder

    def _open_tag(self, tag):
        """
        Generates an opening tag string for a given tag

        :param tag: A BeautifulSoup tag
        :return: The string that would open the tag, including any attributes
        :rtype: str
        """
        attrs = ' '.join(['{}="{}"'.format(id, value) for id, value in tag.attrs.items()])
        if attrs:
            attrs = ' ' + attrs
        return '<{}{}>'.format(tag.name, attrs)

    def _close_tag(self, tag):
        """
        Generates a closing tag string for a given tag
        :param tag: A BeautifulSoup tag
        :return: The string that would close the tag
        :rtype: str
        """
        return '</{}>'.format(tag.name)

