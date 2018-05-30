"""
processing.py

Defines processes that NEAM data can be run through, and a Pipeline class to
run them with. A processor should inherit from NEAMProcessor and adhere to its
contract. Once defined, add an instance of the processor to the a pipeline and
call the pipeline's *run* method. The pipeline will pipe the data given to
*run* through each process defined in the pipeline, in order.
"""
import re
from abc import ABC
from bs4 import BeautifulSoup, NavigableString
from neam.python.util import multi_sub

class NEAMProcessor(ABC):
    """
    Defines the interface for neam processes.

    A NEAMProcessor should implement a method called "run", which accepts an
    str and returns an str.
    """
    def __init__(self, from_type, to_type):
        self._from = from_type
        self._to = to_type

    def run(self, text):
        raise NotImplemented


class Pipeline:
    """
    Stores a list of NEAMProcessor objects and passes data through them
    """
    def __init__(self, processes = None):
        """
        Initializes the Pipeline

        :param processes: The processes to use in the pipeline
        :type processes: list of NEAMProcessor or callable
        """
        self._processes = processes or []

    def run(self, data):
        """
        Consumes some data and passes it sequentially through each processor
        in the pipeline.

        Each processor receives as input the output of the previous processor.

        :param data: The data to pass into the first processor
        :return: The output from the final processor
        """
        for process in self._processes:
            try:
                data = process.run(data)
            except AttributeError:
                data = process(data)
        return data

    def add(self, process):
        """
        Adds a processor to the end of the pipeline

        :param process: The process to add
        :type process: NEAMProcessor or callable
        """
        self._processes.append(process)


class ASCIIifier(NEAMProcessor):
    """
    Replaces non-ascii characters with ascii equivalents
    """
    _CHARMAP = {
        "\u2018": "'",
        "\u2019": "'",
        "\ufeff": ""
    }

    def __init__(self, map = None):
        """
        Initializes the processor

        :param map: Correspondances between UTF-8 characters and ASCII
                    characters
        :type map: dict of str: str
        """
        self._map = map or self._CHARMAP
        super().__init__(str, str)

    def run(self, text):
        return multi_sub(self._map, text)


class PageReplacer(NEAMProcessor):
    def __init__(self):
        super().__init__(BeautifulSoup, BeautifulSoup)

    """
    Replaces page numbers with the corresponding TEI tag
    """
    def run(self, soup):
        for string in soup.body.children:
            if isinstance(string, str):
                string.replace_with(
                    BeautifulSoup(
                        re.sub('page (\d+):?', '<pb n="\g<1>"/>', '<foo>' + str(string) + '</foo>', flags=re.I),
                        'html.parser'
                    ).foo
                )

        for p in soup.body.find_all('p'):
            p.replace_with(
                BeautifulSoup(
                    re.sub('page (\d+):?', '<pb n="\g<1>"/>', str(p), flags=re.I),
                    'html.parser'
                ).p
            )
        return soup


class SicReplacer(NEAMProcessor):
    def __init__(self):
        super().__init__(BeautifulSoup, BeautifulSoup)

    """
    Replaces [sic] items with the corresponding TEI tag
    """
    def run(self, soup):
        for p in soup.body.find_all('p'):
            p.replace_with(
                BeautifulSoup(
                    re.sub('\[sic; (\S+)\]', '<sic>\g<1></sic>', str(p)),
                    'html.parser'
                ).p
            )
        return soup


class SpaceNormalizer(NEAMProcessor):
    """
    Normalizes spaces in XML text
    """
    def __init__(self):
        super().__init__(str, str)

    def run(self, text):
        text = re.sub('\n', ' ', text)
        text = re.sub('(<[^/>]*>) +', '\g<1>', text)
        text = re.sub(' +(?=</)', '', text)
        return re.sub('(?<= ) ', '', text)


class PossessionFixer(NEAMProcessor):
    """
    Moves possession markers inside tags
    """
    def __init__(self):
        super().__init__(str, str)

    def run(self, text):
        text =re.sub("(<[^/>]+>[^<]+)(<[^>]+>)'s", "\g<1>'s\g<2>", text)
        return re.sub("(?<!')(<[^/>]+>[^<]*s)(<[^>]+>)'", "\g<1>'\g<2>", text)


class TagExpander(NEAMProcessor):
    _SPACE_PATTERN = re.compile(' +')

    def __init__(self, tags, words):
        self._tags = tags
        self._words = words
        self._pattern = re.compile('(^|\s)((?:(?:{})\s+)+)<({}[^>]*)>'.format('|'.join(words), '|'.join(tags)), flags=re.I)
        super().__init__(str, str)

    def run(self, text):
        return self._pattern.sub(self._format, text)

    def _format(self, match_object):
        prefix = match_object.group(1)
        words = match_object.group(2).strip()
        tag = match_object.group(3)

        words = self._SPACE_PATTERN.sub(' ', words)

        return '{}<{}>{} '.format(prefix, tag, words)


__all__ = ['ASCIIifier', 'PageReplacer', 'SicReplacer', 'SpaceNormalizer', 'Pipeline', 'PossessionFixer', 'TagExpander']

