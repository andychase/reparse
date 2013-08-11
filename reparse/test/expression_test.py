import unittest
from reparse.expression import Expression, AlternatesGroup


class expression_test(unittest.TestCase):

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
