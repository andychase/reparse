from __future__ import unicode_literals
import regex
from reparse.config import get_expression_compiler


class Expression(object):
    """ Expressions are the building blocks of parsers.

    Each contains:

    - A regex pattern (lazily compiled on first usage)
    - Group lengths, functions and names
    - a ``final_function``

    When an expression runs with ``findall`` or ``scan``,
    it matches a string using its regex, and returns the
    results from the parsing functions.
    """

    class InvalidPattern(Exception):
        def __init__(self, pattern, regex_error):
            super(Expression.InvalidPattern, self).__init__()
            self.pattern = pattern
            self.regex_error = regex_error

        def __str__(self):
            return '%{0.regex_error} in "{0.pattern}" pattern'.format(self)

    def __init__(self, regex, functions, group_lengths, final_function, name=""):
        self.regex = regex
        self.group_functions = functions
        self.group_lengths = group_lengths
        self.final_function = final_function
        self.name = name
        self.compiled = False
        self.expression_compiler = get_expression_compiler()

    @property
    def pattern(self):
        if not self.compiled:
            try:
                self.compiled = self.expression_compiler(self.regex)
            except regex.error as e:
                raise self.InvalidPattern(self.regex, e)
        return self.compiled

    def findall(self, string):
        """ Parse string, returning all outputs as parsed by functions
        """
        output = []
        for match in self.pattern.findall(string):
            if hasattr(match, 'strip'):
                match = [match]
            self._list_add(output, self.run(match))
        return output

    def scan(self, string):
        """ Like findall, but also returning matching start and end string locations
        """
        return list(self._scanner_to_matches(self.pattern.scanner(string), self.run))

    def run(self, matches):
        """ Run group functions over matches
        """
        def _run(matches):
            group_starting_pos = 0
            for current_pos, (group_length, group_function) in enumerate(zip(self.group_lengths, self.group_functions)):
                start_pos = current_pos + group_starting_pos
                end_pos = current_pos + group_starting_pos + group_length
                yield group_function(matches[start_pos:end_pos])
                group_starting_pos += group_length - 1
        return self.final_function(list(_run(matches)))

    def build_full_tree(self):
        return '{}|{}({})'.format(sum(self.group_lengths), self.final_function.__name__, ", ".join(self.build_tree()))

    def build_tree(self):
        for length, function in zip(self.group_lengths, self.group_functions):
            if function.__name__ == 'run':
                yield '{}|{}({})'.format(
                    length, function.__self__.final_function.__name__, ", ".join(function.__self__.build_tree())
                )
            else:
                yield '{}|{}()'.format(length, function.__name__)

    @staticmethod
    def _list_add(output, match):
        if type(match) is list:
            output.extend(match)
        else:
            output.append(match)
        return output

    @staticmethod
    def _scanner_to_matches(scanner, processor):
        none_to_blank = lambda _: '' if _ is None else _

        for match in scanner:
            result = processor(map(none_to_blank, match.groups()))
            if result is None:
                continue
            elif type(result) is list:
                yield [result, match.start(), match.end()]
            else:
                yield [[result], match.start(), match.end()]


def AlternatesGroup(expressions, final_function, name=""):
    """ Group expressions using the OR character ``|``
    >>> from collections import namedtuple
    >>> expr = namedtuple('expr', 'regex group_lengths run')('(1)', [1], None)
    >>> grouping = AlternatesGroup([expr, expr], lambda f: None, 'yeah')
    >>> grouping.regex  # doctest: +IGNORE_UNICODE
    '(?:(1))|(?:(1))'
    >>> grouping.group_lengths
    [1, 1]
    """
    inbetweens = ["|"] * (len(expressions) + 1)
    inbetweens[0] = ""
    inbetweens[-1] = ""
    return Group(expressions, final_function, inbetweens, name)


def Group(expressions, final_function, inbetweens, name=""):
    """ Group expressions together with ``inbetweens`` and with the output of a ``final_functions``.
    """
    lengths = []
    functions = []
    regex = ""
    i = 0
    for expression in expressions:
        regex += inbetweens[i]
        regex += "(?:" + expression.regex + ")"
        lengths.append(sum(expression.group_lengths))
        functions.append(expression.run)
        i += 1
    regex += inbetweens[i]

    return Expression(regex, functions, lengths, final_function, name)
