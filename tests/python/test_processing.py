import unittest

from neam.python.classification.processing import *


class TestPageReplacer(unittest.TestCase):
    def setUp(self):
        self.processor = PageReplacer()

    def test_it_replaces_single_digit_page_numbers(self):
        output = self.processor.run('page 5')
        self.assertEqual('<pb n="5"/>', output)

    def test_it_replaces_multi_digit_page_numbers(self):
        output = self.processor.run('page 20')
        self.assertEqual('<pb n="20"/>', output)

    def test_it_replaces_case_insensitively(self):
        output = self.processor.run('PagE 12')
        self.assertEqual('<pb n="12"/>', output)

    def test_it_replaces_all_page_numbers(self):
        output =self.processor.run('Page 3\nSome text\n\nPage 4')
        self.assertEqual('<pb n="3"/>\nSome text\n\n<pb n="4"/>', output)


class TestSicReplacer(unittest.TestCase):
    def setUp(self):
        self.processor = SicReplacer()

    def test_it_replaces_sics(self):
        output = self.processor.run('[sic; error]')
        self.assertEqual('<sic>error</sic>', output)

    def test_it_replaces_all_sics(self):
        output = self.processor.run('[sic; teh] big [sic; bal]')
        self.assertEqual('<sic>teh</sic> big <sic>bal</sic>', output)


class TestSpaceNormalizer(unittest.TestCase):
    def setUp(self):
        self.processor = SpaceNormalizer()

    def test_it_removes_repeated_spaces(self):
        output = self.processor.run('hello   there')
        self.assertEqual('hello there', output)

    def test_it_removes_newlines(self):
        output = self.processor.run('hello\n\n\nthere')
        self.assertEqual('hello there', output)

    def test_it_removes_space_after_an_opening_tag(self):
        output = self.processor.run('<p>    hello there</p>')
        self.assertEqual('<p>hello there</p>', output)

    def test_it_leaves_space_after_a_closing_tag(self):
        output = self.processor.run('<b>hello</b>   there')
        self.assertEqual('<b>hello</b> there', output)

    def test_it_removes_space_before_a_closing_tag(self):
        output = self.processor.run('<p>hello there   </p>')
        self.assertEqual('<p>hello there</p>', output)

    def test_it_leaves_space_before_an_opening_tag(self):
        output = self.processor.run('hello   <b>there</b>')
        self.assertEqual('hello <b>there</b>', output)


class TestPossessionFixer(unittest.TestCase):
    def setUp(self):
        self.processor = PossessionFixer()

    def test_it_moves_possessive_s_into_a_tag(self):
        output = self.processor.run('<persName>Bob</persName>\'s')
        self.assertEqual('<persName>Bob\'s</persName>', output)

    def test_it_moves_possessive_apostrophe_into_a_tag(self):
        output = self.processor.run('<persName>Bobs</persName>\'')
        self.assertEqual('<persName>Bobs\'</persName>', output)

    def test_it_only_moves_possessive_apostrophes_if_the_word_ends_in_s(self):
        output = self.processor.run("<persName>Bob</persName>'")
        self.assertEqual("<persName>Bob</persName>'", output)

    def test_it_doesnt_move_single_quotes(self):
        output = self.processor.run("'<persName>Bobs</persName>'")
        self.assertEqual("'<persName>Bobs</persName>'", output)

    def test_it_moves_possession_within_the_first_tag(self):
        output = self.processor.run("<persName>James</persName> and <persName>Bobs</persName>'")
        self.assertEqual("<persName>James</persName> and <persName>Bobs'</persName>", output)


class TestTagExpander(unittest.TestCase):
    def setUp(self):
        tags = ['persName', 'placeName']
        words = ['the', 'Mrs.', 'Dr.', 'SS']

        self.processor = TagExpander(tags=tags, words=words)

    def test_it_expands_single_words_to_the_left_of_tags(self):
        output = self.processor.run('the <placeName>Grand Canyon</placeName>')
        self.assertEqual('<placeName>the Grand Canyon</placeName>', output)

    def test_it_expands_multiple_words_to_the_left_of_tags(self):
        output = self.processor.run('Dr. Mrs. <persName>Jane Doe</persName>')
        self.assertEqual('<persName>Dr. Mrs. Jane Doe</persName>', output)

    def test_it_expands_case_insensitively(self):
        output = self.processor.run('The <placeName>Grand Canyon</placeName>')
        self.assertEqual('<placeName>The Grand Canyon</placeName>', output)

    def test_it_only_merges_full_words(self):
        output = self.processor.run('address <persName>John</persName>')
        self.assertEqual('address <persName>John</persName>', output)

    def test_it_expands_in_the_middle_of_a_line(self):
        output = self.processor.run('both stopping at the <placeName>Holland</placeName>')
        self.assertEqual('both stopping at <placeName>the Holland</placeName>', output)

