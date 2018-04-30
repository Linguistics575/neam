import os
import pickle
import random
import re
from neam.python.classification.processing import NEAMProcessor
from nltk import MaxentClassifier, word_tokenize, pos_tag
from nltk.classify import accuracy

class TitleAnnotator(NEAMProcessor):
    _DEFAULT_MODEL = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'title_tag_model.pickle')
    _TAG_PATTERN = re.compile('<[^>]+>')

    def __init__(self, model=_DEFAULT_MODEL, inside='I', outside='O'):
        self._classifier = TitleClassifier(model)
        self._inside = inside
        self._outside = outside

    def run(self, text):
        builder = []
        last_tag = self._outside

        for line in text.split('\n'):
            curr_tag = self._classifier.classify(self._remove_tags(line))
            if last_tag == self._outside and curr_tag == self._inside:
                builder.append('<title>')
            elif last_tag == self._inside and curr_tag == self._outside:
                builder.append('</title>')
            builder.append(line)
            last_tag = curr_tag

        if last_tag == self._inside:
            builder.append('</title>')

        return '\n'.join(builder)

    def _remove_tags(self, line):
        return self._TAG_PATTERN.sub('', line)


class TitleClassifier:
    def __init__(self, model):
        if isinstance(model, MaxentClassifier):
            self._classifier = model
        else:
            with open(model, 'rb') as pickle_file:
                self._classifier = pickle.load(pickle_file)

        self.clear()

    def clear(self):
        self._prevTag = 'O'
        self._prev2Tag = 'O'

    def classify(self, line, clear=False):
        if clear:
            self.clear()

        features = extract(line)
        features['prevTag'] = self._prevTag
        features['prev2Tag'] = self._prev2Tag

        tag = self._classifier.classify(features)
        self._prev2Tag = self._prevTag
        self._prevTag = tag

        return tag

    @staticmethod
    def train(file_name, max_iter=20, train_ratio=1.0, dump=None):
        data = []
        with open(file_name) as input_file:
            for item in input_file:
                label, line = item.split('%%%')
                features = extract(line)

                features['prevTag'] = data[-1][1] if len(data) > 0 else 'O'
                features['prev2Tag'] = data[-2][1] if len(data) > 1 else 'O'

                data.append((features, label))

        random.shuffle(data)
        threshold = int(len(data) * train_ratio)
        train, text = [data[:threshold], data[threshold:]]

        classifier = MaxentClassifier.train(train, max_iter=max_iter)

        if train_ratio < 1:
            print(accuracy(classifier, test))

        if dump:
            with open(dump, 'wb') as model_file:
                pickle.dump(classifier, model_file)

        return TitleClassifier(classifier)


def extract(line):
    tokens = word_tokenize(line)
    tags = []

    if tokens:
        tagged = pos_tag(tokens)
        tokens, tags = zip(*tagged)

    features = {'numTokens': len(tokens)}

    for token in set(tokens):
        features["token({})".format(token)] = 1

    for tag in set(tags):
        features["tags({})".format(tag)] = 1

    return features

