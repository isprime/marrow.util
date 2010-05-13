# encoding: utf-8

from unittest import TestCase

from pulp.util import convert as conv



def assert_boolean(boolean, expected):
    assert conv.boolean(boolean) is expected

def test_truths():
    for truth in [True, 1, ['foo'], 'yes', 'y', 'on', 'true', 't', '1', 'Y', 'True']:
        yield assert_boolean, truth, True

def test_falsehoods():
    for falsehood in [False, 0, [], 'no', 'n', 'off', 'false', 'f', '0', 'N', 'False']:
        yield assert_boolean, falsehood, False


class TestConverters(TestCase):
    def test_boolean_exceptions(self):
        self.assertRaises(ValueError, lambda: conv.boolean('oui'))
        
    def test_array(self):
        self.assertEqual(conv.array(None), [])
        
        self.assertEqual(conv.array([]), [])
        self.assertEqual(conv.array([1, '', 2, 3]), [1, 2, 3])
        self.assertEqual(conv.array([1, '', 3], empty=True), [1, '', 3])
        self.assertEqual(conv.array((4, '', 5)), [4, 5])
        self.assertEqual(conv.array((4, '', 5), empty=True), [4, '', 5])
        
        self.assertEqual(conv.array("foo,bar"), ["foo", "bar"])
        self.assertEqual(conv.array("foo,,bar", empty=True), ["foo", '', "bar"])
        self.assertEqual(conv.array(u"baz, diz"), [u"baz", u"diz"])
        
        self.assertEqual(conv.array("foo|bar", '|'), ["foo", "bar"])
        self.assertEqual(conv.array("baz |diz", '|', False), ["baz ", "diz"])
        self.assertEqual(conv.array("baz||diz", '|', False, True), ["baz", '', "diz"])
        
        self.assertEqual(conv.array("baz  diz", None), ["baz", "diz"])
        self.assertEqual(conv.array("baz   diz", None, False, False), ["baz", "diz"])
    
    def test_keyword_parser_regex(self):
        self.assertEqual(conv.tags.pattern, '[\\s \t,]*("[^"]+"|\'[^\']+\'|[^ \t,]+)[ \t,]*')
        self.assertEqual(conv.terms.pattern, '[\\s \t]*([+-]?"[^"]+"|\'[^\']+\'|[^ \t]+)[ \t]*')
    
    def test_tags(self):
        self.assertEqual(
                conv.tags('"high altitude" "melting panda" panda bends'),
                set(('bends', 'high altitude', 'melting panda', 'panda'))
            )
    
    def test_terms(self):
        self.assertEqual(
                conv.terms('animals +cat -dog +"medical treatment"'),
                (['animals'], ['cat', '"medical treatment"'], ['dog'])
            )
        
        self.assertEqual(
                conv.terms('animal medicine +cat +"kitty death"'),
                (['animal', 'medicine'], ['cat', '"kitty death"'], [])
            )
        
        conv.terms.group = dict
        self.assertEqual(
                conv.terms(' foo  bar "baz"diz       '),
                {None: ['foo', 'bar', '"baz"', 'diz'], '+': [], '-': []}
            )
        
        conv.terms.group = False 
        self.assertEqual(
                conv.terms('cat dog -leather'),
                [(None, 'cat'), (None, 'dog'), ('-', 'leather')]
            )