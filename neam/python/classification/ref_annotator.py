import re
from neam.python.classification.processing import NEAMProcessor

class RefAnnotator(NEAMProcessor):
    _DEFAULT_TAGS = ['persName', 'placeName', 'orgName']

    def __init__(self, tags=None):
        tags = tags or self._DEFAULT_TAGS
        tag_pattern = '|'.join(tags)
        self._pattern = re.compile('<({})>(.*?)</(?:{})>'.format(tag_pattern, tag_pattern))

    def run(self, text):
        return self._pattern.sub(self._make_ref, text)

    def _make_ref(self, match_object):
        tag = match_object.group(1)
        ne  = match_object.group(2)
        ref = ne.replace(' ', '_')

        return '<{} ref="#{}">{}</{}>'.format(tag, ref, ne, tag)

