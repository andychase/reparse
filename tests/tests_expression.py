from __future__ import unicode_literals
import regex
from unittest import TestCase
from reparse.expression import AlternatesGroup, Expression
from reparse import config


class TestExpression(TestCase):

    def test_raises_useful_exception(self):
        """Expression has to raise readable error message."""
        exp = Expression(r'inalid (\d]', {}, [], lambda x: x)
        with self.assertRaises(exp.InvalidPattern):
            assert not exp.pattern

    def test_expressions(self):
        def greeting(input):
            def func(greeting):
                return greeting
            return func(*input)

        def final(input):
            for i in input:
                if i is not None:
                    return i

        regex = "(hi)|(hi)"

        exp = Expression(regex, [greeting, greeting], [1, 1], final)

        self.assertIsInstance(exp, Expression)
        self.assertEquals(exp.findall("hi"), ["hi"])

    def test_groups(self):
        def greeting(input):
            def func(greeting):
                return greeting
            return func(*input)

        def final(input):
            for i in input:
                if i is not None:
                    return i
        regex = "(hi)"
        exp = Expression(regex, [greeting], [1], final)

        regex = "(ho)"
        exp2 = Expression(regex, [greeting], [1], final)

        grouped_expressions = AlternatesGroup([exp, exp2], final)
        self.assertEquals(grouped_expressions.findall("hi"), ["hi"])
        
        
class TestCustomFlags(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._regex_flags = config.regex_flags
        
    @classmethod
    def tearDownClass(cls):
        config.regex_flags = cls._regex_flags
        
    def test_unicode_flag(self):
        def uni_match(input):
            def func(uni_match):
                return uni_match
            return func(*input)

        def final(input):
            return input

        config.regex_flags = config.regex_flags | regex.UNICODE
        
        imp_regex = "(\w+)"
        implicit_u = Expression(imp_regex, [uni_match], [1], final)
        self.assertEquals(implicit_u.findall("b\xebs"), ["b\xebs"])
        
        exp_regex = "([\u00c0-\ud7ff]+)"
        explicit_u = Expression(exp_regex, [uni_match], [1], final)
        self.assertEquals(explicit_u.findall("b\u00eb\u2013s"), ["\u00eb\u2013"])
        
    def test_case_sensitivity(self):
        def uni_match(input):
            def func(uni_match):
                return uni_match
            return func(*input)

        def final(input):
            return input

        config.regex_flags = regex.VERBOSE
        
        lower_regex = "([a-z]+)"
        lower_exp = Expression(lower_regex, [uni_match], [1], final)
        self.assertEquals(lower_exp.findall("aAbcBC"), ["a", "bc"])
        
        upper_regex = "([A-Z]+)"
        upper_exp = Expression(upper_regex, [uni_match], [1], final)
        self.assertEquals(upper_exp.findall("aAbcBC"), ["A", "BC"])
