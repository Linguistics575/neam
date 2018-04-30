import unittest
from neam.python.classification import WikiRetagger

class WikiRetaggerTest(unittest.TestCase):
    def setUp(self):
        tags = ['persName', 'placeName', 'orgName']
        tagmap = {'Person': 'persName', 'Location': 'placeName', 'Organization': 'orgName' }
        self.retagger = WikiRetagger(tags, tagmap)

    def test_it_relabels_people(self):
        output = self.retagger.run('<body><placeName>Queen Elizabeth</placeName></body>')
        self.assertEqual('<body><persName>Queen Elizabeth</persName></body>', output)

    def test_it_relabels_places(self):
        output = self.retagger.run('<body><persName>The Grand Canyon</persName></body>')
        self.assertEqual('<body><placeName>The Grand Canyon</placeName></body>', output)

    def test_it_relabels_when_there_are_intervening_tags(self):
        output = self.retagger.run('<body><placeName><sic>Queen</sic> Elizabeth</placeName></body>')
        self.assertEqual('<body><persName><sic>Queen</sic> Elizabeth</persName></body>', output)

    def test_it_caches_mappings(self):
        self.retagger.run('<body><placeName>Queen Elizabeth</placeName></body>')
        self.assertEqual('persName', self.retagger._cache['Queen Elizabeth'])


