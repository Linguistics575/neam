import re
from neam.python.classification.processing import NEAMProcessor

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

    def run(self, text):
        text = re.sub('(<title>)(.*?)(</title>)(.*?)(?=<title>)', self._format, text, flags=re.S)
        text = re.sub('(?<!<p>)(<title>)(.*?)(</title>)(.*?)$', self._format, text, flags=re.S)
        return '<body>' + text + '</body>'

    def _format(self, match_data):
        open_tag  = match_data.group(1)
        title     = match_data.group(2)
        close_tag = match_data.group(3)
        body      = match_data.group(4)

        code = self._make_code(re.search('({})(?:\.|[a-z]+)? +(\d+)(?:{})?\.?(?: +(\d+)\.?)?'.format('|'.join(self._MONTHS), '|'.join(self._ORDINALS)), title.lower()))

        return '<div xml:id="' + code + '" type="Entry"><p>' + open_tag + title + close_tag + '</p><p>' + body + '</p></div>'

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

