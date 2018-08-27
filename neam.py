#!/usr/bin/python3
from neam.python.neam import main as run_neam

import nltk

from contextlib import contextmanager
import ssl
import sys

NEEDED_COLLECTIONS = {
    'tokenizers': ['punkt'],
    'taggers': ['averaged_perceptron_tagger', 'universal_tagset']
}


def main():
    """
    Makes sure the NLTK dependencies have been downloaded, then passes off to
    the real NEAM script
    """
    ensure_collections_exist(NEEDED_COLLECTIONS)
    run_neam()


def ensure_collections_exist(collections):
    """
    Ensures that all required collections exist on the system, and downloads
    them if they are not present

    :param collections: The collections that must be present - a dict of
                        folder/name pairs, corresponding to where the
                        collections should exist in the filesystem
    :see: http://www.nltk.org/_modules/nltk/downloader.html
    """
    missing_collections = []

    for collection_type, collection_names in collections.items():
        for collection in collection_names:
            try:
                nltk.data.find(f"{collection_type}/{collection}")
            except LookupError:
                missing_collections.append(collection)

    if missing_collections:
        print("Downloading NLTK models...", file=sys.stderr)
        with unverified_https_context():
            for collection in missing_collections:
                print("Downloading {}...".format(collection), file=sys.stderr)
                nltk.download(collection)


@contextmanager
def unverified_https_context():
    """
    Turns off the SSL check for the duration of the function
    """
    try:
        create_unverified_https_context = ssl._create_unverified_context
        create_default_https_context = ssl.create_default_https_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = create_unverified_https_context

    try:
        yield
    finally:
        ssl._create_default_https_context = create_default_https_context


main()
