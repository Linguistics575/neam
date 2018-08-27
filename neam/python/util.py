"""
Miscellaneous helper methods - should be refactored should this file get too
large.
"""
from contextlib import contextmanager
import re
import ssl


def multi_sub(correspondences, text):
    """
    Substitutes multiple keys from a dict with their values within a string

    :param correspondences: A dict where the key is the string to look up and
                            the value is the string to replace it with
    :param text: The string on which to conduct the replacements
    :return: The substituted string
    """
    options = '|'.join(re.escape(key) for key in correspondences.keys())
    pattern = '(' + options + ')'
    return re.sub(pattern, lambda match: correspondences[match.group(0)], text)


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
