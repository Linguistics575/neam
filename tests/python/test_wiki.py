from unittest import TestCase
from neam.python.query.wiki import Entity
from neam.python.classification import WikiRetagger


class EntityTest(TestCase):
    def test_it_looks_up_entities_by_label(self):
        queen_elizabeth = Entity('Queen Elizabeth')
        self.assertEqual('Elizabeth II', queen_elizabeth.label)

    def test_it_has_a_qid_of_none_if_the_label_cannot_be_found(self):
        unknown = Entity('jkal;sdfjkls;df')
        self.assertEqual(None, unknown.qid)

    def test_entities_are_falsy_if_they_have_no_qid(self):
        unknown = Entity('jkal;sdfjkls;df')
        self.assertFalse(unknown)

    def test_entities_are_truthy_if_they_have_a_qid(self):
        queen_elizabeth = Entity('Queen Elizabeth')
        self.assertTrue(queen_elizabeth)

    def test_it_can_be_initialized_with_a_qid(self):
        queen_elizabeth = Entity('Q9682')
        self.assertEqual('Q9682', queen_elizabeth.qid)

    def test_entities_initialized_with_qids_dont_have_labels(self):
        queen_elizabeth = Entity('Q9682')
        self.assertEqual(None, queen_elizabeth.label)

    def test_entities_can_be_checked_for_true_relations(self):
        queen_elizabeth = Entity('Queen Elizabeth')
        human = Entity('human')
        self.assertTrue(queen_elizabeth.is_a(human))

    def test_entities_can_be_checked_for_false_relations(self):
        queen_elizabeth = Entity('Queen Elizabeth')
        lizard = Entity('lizard')
        self.assertFalse(queen_elizabeth.is_a(lizard))

    def test_entities_can_be_checked_for_relations_using_a_string(self):
        queen_elizabeth = Entity('Queen Elizabeth')
        self.assertTrue(queen_elizabeth.is_a('human'))

    def test_entities_can_be_checked_for_relations_using_a_qid(self):
        queen_elizabeth = Entity('Queen Elizabeth')
        self.assertTrue(queen_elizabeth.is_a('Q5'))

    def test_entities_with_no_qid_always_return_false_for_relations(self):
        unknown = Entity('jkal;sdfjkls;df')
        self.assertFalse(unknown.is_a('human'))

    def test_multiple_relations_can_be_checked(self):
        queen_elizabeth = Entity('Queen Elizabeth')
        options = ['person', 'place', 'thing']
        self.assertEqual(['person', 'thing'], queen_elizabeth.which(options))

    def test_multiple_relations_can_be_checked_using_qids(self):
        queen_elizabeth = Entity('Queen Elizabeth')
        options = ['Q5', 'Q82794', 'Q35120']
        self.assertEqual(['Q5', 'Q35120'], queen_elizabeth.which(options))

    def test_multiple_relations_can_be_checked_using_mixed_options(self):
        queen_elizabeth = Entity('Queen Elizabeth')
        options = ['Q5', 'place', 'thing']
        self.assertEqual(['Q5', 'thing'], queen_elizabeth.which(options))

    def test_entities_with_no_qid_always_return_false_for_multiple_relations(self):
        unknown = Entity('jkal;sdfjkls;df')
        options = ['Person', 'Place', 'thing']
        self.assertEqual([], unknown.which(options))


class WikiRetaggerTest(TestCase):
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

