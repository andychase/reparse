"""
RE|PARSE's Regex Building Blocks


This module handles building regex bits and grouping them together.
The magic here is that expressions can be grouped as much as memory allows.
"""
from reparse.config import expression_compiler


class Expression:
    """ Expression is the fundamental unit of RE|PARSE.

    It contains:

    - The finalized regex,
    - the compiled regex (lazily compiled on the first run),
    - Group lengths, functions and names,
    - and the output ``final_function``

    """
    regex = ""
    compiled = ""
    group_lengths = []
    group_functions = []
    group_names = []
    final_function = ""

    def __init__(self, regex, functions, group_lengths, final_function, name=""):
        self.regex = regex
        self.group_functions = functions
        self.group_lengths = group_lengths
        self.final_function = final_function
        self.name = name

    def findall(self, string):
        """ Parse argument string
        """
        if self.compiled == "":
            self.compiled = expression_compiler(self.regex)
        matches = self.compiled.findall(string)
        output = []
        for match in matches:
            match = self.run(match)
            if type(match) is list:
                output.extend(match)
            else:
                output.append(match)
        return output

    def scan(self, string):
        """ Like findall, but return start and ends
        """
        if self.compiled == "":
            self.compiled = expression_compiler(self.regex)
        return list(scanner_to_matches(self.compiled.scanner(string), self.run))

    def run(self, matches):
        """
        Given matches, which is the output of this class's regex
        execute functions & parse.
        """
        j = 0
        results = []
        for i in range(0, len(self.group_functions)):
            length = self.group_lengths[i]
            function_set = matches[(i + j):(i + j + length)]
            results.append(self.group_functions[i](function_set))
            j += length - 1
        return self.final_function(results)


def scanner_to_matches(scanner, processor):
    for match in scanner:
        groups = list(NoneToBlank(match.groups()))
        result = processor(groups)
        if result is None:
            continue
        elif type(result) is list:
            yield [result, match.start(), match.end()]
        else:
            yield [[result], match.start(), match.end()]


def NoneToBlank(arr):
    for item in arr:
        if item is None:
            yield ''
        else:
            yield item


def AlternatesGroup(expressions, final_function, name=""):
    """ Group expressions using the OR regex (``|``)
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
