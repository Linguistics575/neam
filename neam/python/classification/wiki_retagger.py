"""
Processor for retagging named entities using Wikidata
"""
from bs4 import BeautifulSoup
from neam.python.classification.processing import NEAMProcessor
from neam.python.query import wiki

class WikiRetagger(NEAMProcessor):
    _DEFAULT_TAGS = ['persName', 'placeName', 'orgName']
    _DEFAULT_TAGMAP = {'Person': 'persName', 'Location': 'placeName', 'Organization': 'orgName'}

    def __init__(self, tags=None, tagmap=None):
        """
        Initializes the processor

        :param tags: The tags the processor should check with Wikipedia on
        :type tags: list of str
        :param tagmap: A mapping from Wikipedia tags to TEI tags
        :type tagmap: dict of str: str
        """
        self._tags = [tag.lower() for tag in tags or self._DEFAULT_TAGS]
        self._tagmap = tagmap or self._DEFAULT_TAGMAP

    def run(self, text):
        """
        Runs a block of text through the retagger.

        The text must be valid XML.

        :param text: The text to run through the tagger
        :type text: str
        :return: The retagged text
        :rtype: str
        """
        # Parse the text to get the XML structure
        soup = BeautifulSoup(text, 'lxml')

        # Run through each NE tag and evaluate it
        for element in soup.find_all(self._tags):
            named_entity = ' '.join(element.stripped_strings)
            retag = self.retag(named_entity)

            if retag:
                tag = self._tagmap[retag]
                element.name = tag

        return str(soup.body)

    def retag(self, tag):
        entity = wiki.Entity(tag)
        matches = entity.which(self._tagmap.keys())

        if matches:
            return matches[0]

