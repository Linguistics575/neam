from neam.python.java import clms, java
from neam.python.classification.processing import NEAMProcessor

NEAMClassifier = clms.neam.classify.NEAMClassifier

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
        props = CORE_NLP_DEFAULTS.copy()
        if options:
            props.update(options)
        core_nlp_props = self._convert_props(props)

        tags = tags or DEFAULT_TAGS
        tags = self._convert_props(tags)

        self._classifier = NEAMClassifier(core_nlp_props, tags)
        self._preprocesses = []
        self._postprocesses = []

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
        for preprocess in self._preprocesses:
            text = preprocess(text)

        text = self._classifier.classify(text)

        for postprocess in self._postprocesses:
            text = postprocess(text)

        return text

    def run(self, text):
        return self.classify(text)

