from unittest import TestCase
from reparse.expression import Expression

class TestExpression(TestCase):

    def test_raises_useful_exception(self):
        """Expression has to raise readable error message."""
        exp = Expression('inalid (\d]', {}, [], lambda x: x)
        with self.assertRaises(exp.InvalidPattern):
            exp.pattern
