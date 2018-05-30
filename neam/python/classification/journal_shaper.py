import re
from neam.python.classification.processing import NEAMProcessor
from bs4 import BeautifulSoup, NavigableString, Tag


class JournalShaper(NEAMProcessor):
    """
    Shapes journal text into TEI format by finding titles and paragraphs
    """
    _MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'oct', 'nov', 'dec']
    _ORDINALS = ['st', 'd', 'nd', 'rd', 'th']

    def __init__(self, author, year = 0, month = 1, day = 1):
        """
        Initializes the processor

        :param author: An ID for the author, to use in title tags
        :type author: str
        :param year: The year of the first entry
        :type year: int
        :param month: The 1-based integer corresponding to the month of the
                      first entry
        :type month: int
        :param day: The day of the first entry
        :type day: int
        """
        self._author = author
        self._year = year
        self._month = month
        self._day = day
        super().__init__(BeautifulSoup, BeautifulSoup)

    @property
    def formatted_year(self):
        """
        :return: The current year, as far as journal parsing is concerned
        :rtype: str
        """
        return str(self._year)

    @property
    def formatted_month(self):
        """
        :return: The current month, as far as journal parsing is concerned
        :rtype: str
        """
        return self._pad(self._month, 2)

    @property
    def formatted_day(self):
        """
        :return: The current day, as far as journal parsing is concerned
        :rtype: str
        """
        return self._pad(self._day, 2)

    def run(self, soup):
        title = None
        body = soup.new_tag('body')
        for child in soup.body.contents[:]:
            if isinstance(child, Tag):
                title = child.extract()
            else:
                text = NavigableString(str(child))

                if title:
                    div = soup.new_tag('div')
                    div['type'] = 'Entry'
                    div['xml:id'] = self.extract_code(title)

                    p_text = soup.new_tag('p')
                    p_text.append(text)
                    p_title = soup.new_tag('p')
                    p_title.append(title)

                    div.append(p_title)
                    div.append(p_text)
                    body.append(div)
                else:
                    body.append(text)

        soup.body.replace_with(body)
        return soup

    def extract_code(self, title):
        if title.string:
            return self._make_code(re.search('({})(?:\.|[a-z]+)? +(\d+)(?:{})?\.?(?: +(\d+)\.?)?'.format('|'.join(self._MONTHS), '|'.join(self._ORDINALS)), title.string.lower()))
        return self._author + '???'

    def _make_code(self, match_data):
        """
        Translates match data into a TEI title

        :param match_data: The result from a regular expression search
        """
        month = day = year = None

        if match_data:
            month = match_data.group(1)
            day   = match_data.group(2)
            year  = match_data.group(3)

        if day:
            day = int(day)
            if day < self._day:
                self._month += 1
            self._day = int(day)

        if month:
            month = self._MONTHS.index(month.lower()) + 1
            if month < self._month:
                self._year += 1
            self._month = month

        if year:
            self._year = int(year)

        return self._author + self.formatted_year + self.formatted_month + self.formatted_day

    def _tag_bodies(self, text):
        """
        Fills in the paragraphs based on the position of the titles

        :param text: The partially processed text
        :return: The text with bodies filled in
        """
        return re.sub('(</p><p>[\S\s]*?)(<div)', '\g<1></p></div>\g<2>', text)

    def _pad(self, n, size):
        """
        Adds 0s to the beginning of a number until the number is *size*
        characters long.

        :param n: The number to pad
        :param size: The size to pad until
        :return: The padded number
        :rtype: str
        """
        return '0' * (size - len(str(n))) + str(n)

