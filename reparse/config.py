"""
This module defines some variables you can
set for how RE|PARSE operates.
"""

# This number should be bigger than the longest
# chain of patterns-inside-patterns
pattern_max_recursion_depth = 10

# The regex engine and settings
import regex
flags = regex.VERBOSE | regex.IGNORECASE
expression_compiler = lambda expression: regex.compile(expression, flags=flags)
expression_sub = lambda expression, sub, string: regex.sub(expression, sub, string, flags=flags)
