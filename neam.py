#!/usr/bin/python3
import sys
import nltk

try:
    nltk.tokenize.word_tokenize('Good to go?')
except LookupError:
    print("Downloading NLTK models...", file=sys.stderr)
    for data in ['punkt', 'averaged_perceptron_tagger', 'universal_tagset']:
        print("Downloading {}...".format(data), file=sys.stderr)
        nltk.download(data)

from neam.python.neam import main

main()

