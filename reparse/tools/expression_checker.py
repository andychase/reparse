"""
This module contains a useful function that aids in validating
expression files by making sure each expression in a group
are valid against the 'Expression', 'Matches', & 'Non-Matches' fields.

It is intended to be used against a ``testing_framework`` that
contains assertIn, assertTrue, assertFalse (such as unittest).

Example Usage::

    from reparse.tools.expression_checker import check_expression
    import unittest

    class cool_test(unittest.TestCase):
        def test_coolness(self):
            check_expression(self, load_yaml("parse/cool/expressions.yaml"))
"""
from __future__ import unicode_literals
from reparse.config import get_expression_sub
base_error_msg = "Expression Type [{}], Group [{}], "
match_error_msg = base_error_msg + "Could not match [{}]"
non_match_error_msg = base_error_msg + "Should not match [{}]"


def check_expression(testing_framework, expression_dict):
    """
    >>> class mock_framework:
    ...   def assertIn(self, item, list, msg="Failed asserting item is in list"):
    ...     if item not in list: raise Exception(msg)
    ...   def assertTrue(self, value, msg="Failed asserting true"):
    ...     if not value: raise Exception(msg)
    ...   def assertFalse(self, value, msg): self.assertTrue(not value, msg)
    >>> check_expression(mock_framework(),
    ...   {'class': {'group' :{'Matches': " 0 | 1", 'Non-Matches': "2 | 0 2", 'Expression': "[0-1]"}}})
    """
    expression_sub = get_expression_sub()
    
    for expression_type_name, expression_type in expression_dict.items():
        for name, expression_object in expression_type.items():
            if 'Matches' in expression_object.keys():
                for test in expression_object['Matches'].split('|'):
                    # Substitute and check to make sure that the entire string matches
                    result = expression_sub(expression_object['Expression'], '', test.strip()) == ''
                    testing_framework.assertTrue(result, match_error_msg.format(expression_type_name, name, test))
            if 'Non-Matches' in expression_object.keys():
                for test in expression_object['Non-Matches'].split('|'):
                    result = expression_sub(expression_object['Expression'], '', test.strip()) == ''
                    testing_framework.assertFalse(result, non_match_error_msg.format(expression_type_name, name, test))
