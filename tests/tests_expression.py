from unittest import TestCase
from reparse.expression import AlternatesGroup, Expression

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
