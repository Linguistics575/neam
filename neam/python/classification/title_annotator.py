import os
import re
from neam.python.classification.processing import NEAMProcessor
from neam.python.classification.title_classifier import TitleClassifier
from bs4 import BeautifulSoup, NavigableString


class TitleAnnotator(NEAMProcessor):
    _DEFAULT_MODEL = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'title_tag_model.pickle')
    _TAG_PATTERN = re.compile('<[^>]+>')

    def __init__(self, model=_DEFAULT_MODEL, inside='I', outside='O'):
        self._classifier = TitleClassifier(model)
        self._inside = inside
        self._outside = outside
        super().__init__(BeautifulSoup, BeautifulSoup)

    def run(self, soup):
        builder = []
        last_tag = self._outside
        text = str(soup.body.string)
        soup.body.clear()
        #soup.body.new_tag('a')

        for line in text.split('\n'):
            curr_tag = self._classifier.classify(self._remove_tags(line))
            if last_tag == self._outside and curr_tag == self._inside:
                soup.body.append(NavigableString('\n'.join(builder)))
                builder = []
            elif last_tag == self._inside and curr_tag == self._outside:
                tag = soup.new_tag('title')
                soup.body.append(tag)
                tag.string = '\n'.join(builder)
                builder = []
            builder.append(line)
            last_tag = curr_tag

        if last_tag == self._inside:
            tag = soup.new_tag('title')
            soup.body.append(tag)
            tag.string = '\n'.join(builder)
        else:
            soup.body.append(NavigableString('\n'.join(builder)))

        return soup

    def _remove_tags(self, line):
        return self._TAG_PATTERN.sub('', line)

