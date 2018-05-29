#!/usr/bin/python3
"""
evaluate.py

Evaluates a set of tagged data against a gold standard. Provides both MUC and CoNLL-style
calculates of precision, recall, and f-measure.

:author: Sunny Woldenga-Racine
"""
from bs4 import BeautifulSoup
import re
import sys


# the tags we want to keep in the gold standard
KEEP_TAGS = ['persname', 'placename', 'orgname']


# the tags we want to see accuracy for
EVAL_TAGS = ['persname', 'placename', 'orgname']


def clean_gold(soup):
    """
    Tidies up the gold standard for evaluation. Removes tags that aren't being evaluated,
    removes any material inside a desired tag after the tag name, strips punctuation.
    :param soup: the tagged gold standard
    :type soup: BeautifulSoup
    :return: a string representation of the gold standard
    """
    spaced = space_punct(soup)
    # convert to string
    str_soup = str(spaced)
    # remove tag attributes
    str_soup = re.sub(r'<persname.+?>', '<persname>', str_soup)
    str_soup = re.sub(r'<placename.+?>', '<placename>', str_soup)
    str_soup = re.sub(r'<orgname.+?>', '<orgname>', str_soup)
    # remove any whitespace before a closing tag or after opening tag
    str_soup = strip_inner_tag(str_soup)
    # turn page breaks into line breaks
    str_soup = re.sub(r'<pb.+?>', '\n', str_soup)
    # get the tags present in the text
    tags = set(re.findall(r'</?.+?>', str_soup))
    # remove tags which we do not want to keep
    for tag in tags:
        tag_name = re.search(r'\w+', tag)
        if tag_name.group(0) not in KEEP_TAGS:
            str_soup = re.sub(re.escape(tag), '', str_soup)
    return str_soup


def clean_test(soup):
    """
    Tidies up the gold standard for evaluation. Removes content referring to page
    number and strips punctuation.
    :param soup: the tagged data to be tested
    :type soup: BeautifulSoup
    :return: a string representation of the data to be tested
    """
    spaced = space_punct(soup)
    # get a string representation
    str_soup = ''.join([str(x) for x in spaced.contents])
    # remove any whitespace before a closing tag or after opening tag
    str_soup = strip_inner_tag(str_soup)
    # remove the BOM char which literally no one likes
    str_soup = str_soup.replace('\ufeff', '')
    # get the tags present in the text
    tags = set(re.findall(r'</?.+?>', str_soup))
    # remove tags which we do not want to keep
    for tag in tags:
        tag_name = re.search(r'\w+', tag)
        if tag_name.group(0) not in EVAL_TAGS:
            str_soup = re.sub(tag, '', str_soup)
    # remove page information
    str_soup = re.sub(r'PAGE \d+', '', str_soup)
    return str_soup


def space_punct(soup):
    """
    Puts whitespace around word-external punctuation and word-internal
    apostrophes.
    :param soup: xml data to be modified
    :type soup: BeautifulSoup object
    :return: soup object with external punctuation surrounded with whitespace
    """
    punct = re.escape('!"#$%&\'()*+,-.:;=?@[\\]^_`{|}~’‘')
    for node in soup.find_all(string=lambda x: x.strip()):
        spaced = re.sub(r'([%s])(\W|$)' % re.escape(punct), r' \1 ', str(node))
        spaced = re.sub(r'(\W|^)([%s])' % re.escape(punct), r' \2 ', spaced)
        spaced = re.sub(r'(\w)(\')(\w)', r'\1 \2 \3', spaced)
        node.replace_with(spaced)
    return soup


def strip_inner_tag(text):
    """
    Strips leading and trailing whitespace within a tag. This prevents an
    opening tag from being followed by whitespace and a closing tag from
    being preceded by whitespace.
    :param text: text to be stripped
    :return: stripped text
    """
    stripped_text = re.sub(r'<persname>\s+', '<persname>', text)
    stripped_text = re.sub(r'\s+</persname>', '</persname>', stripped_text)
    stripped_text = re.sub(r'<placename>\s+', '<placename>', stripped_text)
    stripped_text = re.sub(r'\s+</placename>', '</placename>', stripped_text)
    stripped_text = re.sub(r'<orgname>\s+', '<orgname>', stripped_text)
    stripped_text = re.sub(r'\s+</orgname>', '</orgname>', stripped_text)
    return stripped_text


def tokenize(text):
    """
    Tokenizes text by splitting on whitespace. Made as function in case more
    complicated tokenization is needed in the future.
    :param text: text to be tokenized
    :return: tokenized text
    """
    tokens = text.split()
    return tokens


def check(test, gold):
    """
    Checks whether all tokens (once tags have been removed) are identical
    and whether each set has the same number of tokens. If tokens are
    different, it prints the first pair of tokens which do not match. If
    one of the lists is longer, it prints the extra tokens. If either of
    these things happens it means there is likely a bug in how I am
    cleaning or tokenizing the data.
    it.
    :param test: list of tokens in the test data
    :param gold: list of tokens in the gold standard data
    :return: whether the lists are the same length
    """
    for i, t in enumerate(test):
        # avoid IndexError when indexing gold
        if i < len(gold):
            t1 = re.sub(r'</?\w+>', '', t)
            t2 = re.sub(r'</?\w+>', '', gold[i])
            # if the tokens are different
            if t1 != t2:
                print('Difference: \'{}\' vs \'{}\''.format(t1, t2))
                print('Context test = {} {} {} {} {}'.format(test[i-2], test[i-1], test[i], test[i+1], test[i+2]))
                print('Context gold = {} {} {} {} {}'.format(gold[i-2], gold[i-1], gold[i], gold[i+1], gold[i+2]))
                return False
    if len(test) > len(gold):
        print('Test has more tokens than gold. Extra:')
        for i in range(len(gold), len(test)):
            print(test[i])
        return False
    elif len(gold) > len(test):
        print('Gold has more tokens than test. Extra:')
        for i in range(len(test), len(gold)):
            print(gold[i])
        return False
    else:
        return True


def conll_eval(test, gold):
    """
    Evaluates the test data against the gold data following the CoNLL style
    of evaluation, then prints the results. CoNLL uses exact-match evaluation,
    meaning a tag is only considered correct if both its type and span match
    the gold standard.
    :param test: the data to be tested
    :type test: list of strings
    :param gold: the gold standard data
    :type test: list of strings
    """
    counts = {}
    for tag in EVAL_TAGS:
        counts[tag] = {'cor': 0,  # number of correct guesses made
                       'gue': 0,  # total number of guesses made
                       'pos': 0}  # number of possible correct tags
    # whether an opening tag in test has been found and matches the gold
    correct_open = False
    for i, t1 in enumerate(test):
        t2 = gold[i]
        # an opening tag found in test
        t1_has_left = re.search(r'<(\w+)>', t1)
        # its closing tag
        t1_has_right = re.search(r'</\w+>', t1)
        # an opening tag found in gold
        if re.search(r'<(\w+)>', t2):
            gold_tag = re.search(r'<(\w+)>', t2).group(1)
            if gold_tag in EVAL_TAGS:
                # increment number of possible correct tags
                counts[gold_tag]['pos'] = counts[gold_tag]['pos'] + 1
        # an opening tag found in test
        if t1_has_left:
            test_tag = t1_has_left.group(1)
            # increment number of guesses
            counts[test_tag]['gue'] = counts[test_tag]['gue'] + 1
            # if the tag matches the gold at this point
            if t1 == t2:
                correct_open = True  # a correct opening tag was found
        # if a correct opening tag has already been found
        if correct_open:
            # if the test's tag has been closed, and that tag matches the gold at this point
            if t1_has_right and t1 == t2:
                # exact match found
                counts[test_tag]['cor'] = counts[test_tag]['cor'] + 1
                correct_open = False  # reset the opening tag tracker
    # write the results to stdout
    print_eval('CoNLL', counts)


def muc_eval(test, gold):
    """
    Evaluates the test data against the gold data following the MUC style of
    evaluation, then prints the results. MUC gives points separately for the
    correct tag type and tag span, for a maximum of two points per tag.
    :param test: the data to be tested
    :type test: list of strings
    :param gold: the gold standard data
    :type test: list of strings
    """
    counts = {}
    for tag in EVAL_TAGS:
        counts[tag] = {'text_cor': 0,  # number of correct spans
                       'text_gue': 0,  # total span guesses
                       'text_pos': 0,  # number of possible correct spans
                       'type_cor': 0,  # number of correct tag types
                       'type_gue': 0,  # total tag type guesses
                       'type_pos': 0}  # number of possible correct tag types
    test_tag = ""  # type of tag found in test, empty if uninitialized
    test_span = [-1, -1]  # span of tag found in test, -1 if uninitialized
    gold_tag = ""  # type of tag found in gold, empty if uninitialized
    gold_span = [-1, -1]  # span of tag found in gold, -1 if uninitialized
    for i, t1 in enumerate(test):
        t2 = gold[i]
        # if the test token has an opening tag
        if re.search(r'<(\w+)>', t1):
            test_tag = re.search(r'<(\w+)>', t1).group(1)  # get tag type
            test_span[0] = i  # get start index of span
            # increment total guesses
            counts[test_tag]['text_gue'] = counts[test_tag]['text_gue'] + 1
            counts[test_tag]['type_gue'] = counts[test_tag]['type_gue'] + 1
        # if the test token has a closing tag
        if re.search(r'</(\w+)>', t1):
            # if the start index of span is initialized (if it's not, it
            # has been reset and we should do nothing)
            if test_span[0] != -1:
                test_span[1] = i  # get end index of span
        # if the test token has an opening tag
        if re.search(r'<(\w+)>', t2):
            gold_tag = re.search(r'<(\w+)>', t2).group(1)  # get tag type
            gold_span[0] = i  # get start index of span
            if gold_tag in EVAL_TAGS:
                # increment total possible correct
                counts[gold_tag]['text_pos'] = counts[gold_tag]['text_pos'] + 1
                counts[gold_tag]['type_pos'] = counts[gold_tag]['type_pos'] + 1
        # if the test token has a closing tag
        if re.search(r'</(\w+)>', t2):
            # if the start index of span is initialized (if it's not, it
            # has been reset and we should do nothing)
            if gold_span[0] != -1:
                gold_span[1] = i  # get end index of span
        # if an open tag has been closed
        if test_span[1] > -1 or gold_span[1] > -1:
            incorrect = False  # whether the tag is wrong in some way
            # if tag types match
            if test_tag == gold_tag:
                # increment correct tag type
                counts[test_tag]['type_cor'] = counts[test_tag]['type_cor'] + 1
            else:
                incorrect = True
            # if tag spans match
            if test_span == gold_span:
                # increment correct span
                counts[test_tag]['text_cor'] = counts[test_tag]['text_cor'] + 1
            else:
                incorrect = True
            # dump incorrect tags to stderr
            if incorrect:
                print2err(test_span, gold_span, test, gold)
            # reset tag variables
            test_tag = ""
            test_span = [-1, -1]
            gold_tag = ""
            gold_span = [-1, -1]
    totals = {}
    for tag in EVAL_TAGS:
        totals[tag] = {'cor': counts[tag]['text_cor'] + counts[tag]['type_cor'],
                       'gue': counts[tag]['text_gue'] + counts[tag]['type_gue'],
                       'pos': counts[tag]['text_pos'] + counts[tag]['type_pos']}
    # write the results to stdout
    print_eval('MUC', totals)


def print2err(test_span, gold_span, test_tokens, gold_tokens):
    """
    Prints the span containing the proposed tag and its corresponding span in the
    gold standard, and vice versa, to stderr.
    :param test_span: the span of the proposed tag
    :param gold_span: the span of the gold tag
    :param test_tokens: tokens in test data
    :param gold_tokens: tokens in gold standard
    """
    # if both test and gold have a tag open in the span
    if test_span[0] > -1 and gold_span[0] > -1:
        start = min(test_span[0], gold_span[0])
    else:
        # max can be used because if the start is uninitialized, it is -1
        start = max(test_span[0], gold_span[0])
    end = max(test_span[1], gold_span[1])
    # get the test text contained in full span
    test_text = " ".join(test_tokens[start:end+1])
    # get the gold text contained in full span
    gold_text = " ".join(gold_tokens[start:end+1])
    print("[{}] VS [{}]".format(test_text, gold_text), file=sys.stderr)


def print_eval(name, totals):
    """
    Writes the precision, recall, and f-measure of the input counts to stdout, with
    the name of the evaluation style used.
    :param name: name of evaluation style used
    :param totals: the counts for correct, guesses, and possible tags
    """
    cols = ['Precision', 'Recall', 'F-measure']  # columns out output table
    rows = []  # rows of output table
    total_cor = 0  # total correct guesses for all tags
    total_gue = 0  # total guesses for all tags
    total_pos = 0  # total possible correct guesses for all tags
    accuracy = []  # precision, recall, and f-measure for every tag
    # for every tag
    for tag in EVAL_TAGS:
        rows.append(tag)  # make a row for it
        # increment total counts
        total_cor += totals[tag]['cor']
        total_gue += totals[tag]['gue']
        total_pos += totals[tag]['pos']
        # get precision, recall, and f-measure for tag
        precision = safe_divide(totals[tag]['cor'], totals[tag]['gue'])
        recall = safe_divide(totals[tag]['cor'], totals[tag]['pos'])
        fmeasure = 2 * safe_divide(precision * recall, precision + recall)
        # add figures to master list
        accuracy.append([precision, recall, fmeasure])
    # make a row for the total accuracy of all tags
    rows.append('Total')
    # get total precision, recall, and f-measure
    total_precision = safe_divide(total_cor, total_gue)
    total_recall = safe_divide(total_cor, total_pos)
    total_fmeasure = 2 * safe_divide(total_precision * total_recall, total_precision + total_recall)
    # add figures to master list
    accuracy.append([total_precision, total_recall, total_fmeasure])
    # get the column width
    max_width = max(len(x) for x in cols + rows) + 2
    # create the format for text cells
    text_align = '{:>%d}' % max_width
    # create the format for numerical cells
    num_align = '{:>%d.6}' % max_width
    num_align = num_align * 3
    # create format for the first row
    first_row = text_align * 4
    # print the table
    print('\n%s-Style Evaluation Results:' % name)
    print(first_row.format("", *cols))
    for i, tag in enumerate(rows):
        vals = accuracy[i]
        print(text_align.format(tag), end="")
        print(num_align.format(*vals))


def safe_divide(x, y):
    """
    Divides two numbers, or returns NaN if the denominator is 0.
    :param x: the numerator
    :param y: the denominator
    :return: the ratio of x to y
    """
    try:
        return x / y
    except ZeroDivisionError:
        return float('nan')


def main():
    # get the command line arguments
    try:
        testfile = sys.argv[1]
        goldfile = sys.argv[2]
    except IndexError:
        print('Command line arguments needed: file to be tested, gold standard file')
        sys.exit(1)
    if len(sys.argv) > 3:
        global EVAL_TAGS
        EVAL_TAGS = [x.lower() for x in sys.argv[3:]]
    EVAL_TAGS.sort()
    # make soup for test
    with open(testfile, 'r', encoding='utf-8', errors="surrogateescape") as tf:
        test = BeautifulSoup(tf, 'html.parser')
    # make soup for gold
    with open(goldfile, 'r', encoding='utf-8', errors="surrogateescape") as gf:
        gold = BeautifulSoup(gf, 'html.parser')
    # clean and tokenize the data
    test = tokenize(clean_gold(test.body))
    gold = tokenize(clean_gold(gold.body))
    # ensure the data are formatted for evaluation
    if check(test, gold):
        # evaluate using CoNLL and MUC style evaluation
        muc_eval(test, gold)
        conll_eval(test, gold)


if __name__ == '__main__':
    main()
