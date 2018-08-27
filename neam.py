#!/usr/bin/python3
from neam.python.neam import main as run_neam
from neam.python.util import unverified_https_context

import nltk

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
    ensure_nltk_collections_exist(NEEDED_COLLECTIONS)
    run_neam()


def ensure_nltk_collections_exist(collections):
    """
    Ensures that all required NLTK collections exist on the system, and
    downloads them if they are not present

    :param collections: The collections that must be present - a dict of
                        folder/name pairs, corresponding to where the
                        collections should exist in the filesystem
    :see: http://www.nltk.org/_modules/nltk/downloader.html
    """
    missing_collections = find_missing_nltk_collections(collections)

    if missing_collections:
        print("Downloading NLTK models...", file=sys.stderr)
        with unverified_https_context():
            for collection in missing_collections:
                print("Downloading {}...".format(collection), file=sys.stderr)
                nltk.download(collection)


def find_missing_nltk_collections(collections):
    """
    Checks if a dict of NLTK collections exist on the system and returns a
    list of collections that are missing

    :param collections: The collections that must be present - a dict of
                        folder/name pairs, corresponding to where the
                        collections should exist in the filesystem
    :return: A list of collections not present on the system
    """
    missing_collections = []

    for collection_type, collection_names in collections.items():
        for collection in collection_names:
            try:
                nltk.data.find(f"{collection_type}/{collection}")
            except LookupError:
                missing_collections.append(collection)

    return missing_collections


if __name__ == '__main__':
    main()
