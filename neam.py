#!/usr/bin/python3
import nltk

import ssl
import sys

try:
    nltk.tokenize.word_tokenize('Good to go?')
except LookupError:
    """
    From https://stackoverflow.com/a/41351871 - potentially unsafe, but should
    work as a workaround for now where SSL checking is failing.

    Also see https://www.python.org/dev/peps/pep-0476/
    """
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    print("Downloading NLTK models...", file=sys.stderr)
    for data in ['punkt', 'averaged_perceptron_tagger', 'universal_tagset']:
        print("Downloading {}...".format(data), file=sys.stderr)
        nltk.download(data)

from neam.python.neam import main

main()
