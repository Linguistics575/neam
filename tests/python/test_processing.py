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

