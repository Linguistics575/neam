import re

from bs4 import BeautifulSoup

from neam.python.java import clms, java, boot_java
from neam.python.classification.processing import NEAMProcessor

CORE_NLP_DEFAULTS = {
  'annotators': 'tokenize,ssplit,pos,lemma,ner,entitymentions',
  'ner.applyNumericClassifiers': 'false',
  'tokenize.keepeol': 'true',
  'tokenize.options': 'asciiQuotes'
}

DEFAULT_TAGS = {
    'PERSON': 'persName',
    'LOCATION': 'placeName',
    'ORGANIZATION': 'orgName',
    'DATE': 'date',
    'MISC': 'miscName',
    'geo': 'placeName',
    'org': 'orgName',
    'per': 'persName',
    'gpe': 'orgName'
}


class Classifier(NEAMProcessor):
    def __init__(self, options = None, tags = None):
        boot_java()
        props = CORE_NLP_DEFAULTS.copy()
        if options:
            props.update(options)
        core_nlp_props = self._convert_props(props)

        tags = tags or DEFAULT_TAGS
        java_tags = self._convert_props(tags)

        self._target_tags = set(tags.values())
        self._classifier = clms.neam.classify.NEAMClassifier(core_nlp_props, java_tags)

        super().__init__(BeautifulSoup, str)

    def _convert_props(self, props):
        """
        Converts a Python dict to a Java Properties object

        :param props: The values to convert
        :type props: dict of str: str
        :return: A corresponding Java Properties object
        """
        java_props = java.util.Properties()

        for [key, value] in props.items():
            java_props.setProperty(key, value)

        return java_props

    def classify_file(self, file_name):
        with open(file_name) as input_file:
            text = ''.join(input_file.readlines())
        return self.classify(text)

    def classify(self, text):
        return self._classifier.classify(re.sub('\n', ' ', text))

    def run(self, soup):
        for tag in soup.find_all(['title', 'p']):
            text = self.classify(str(tag))
            tag.replace_with(BeautifulSoup(text, 'html.parser'))

        output = str(soup)
        for tag in self._target_tags:
            output = output.replace(tag.lower(), tag)

        return output
