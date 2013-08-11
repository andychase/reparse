"""
    RE|PARSE Building Blocks

    This module handles building regex bits and grouping them together.
    The magic here is that expressions can be grouped as much as memory allows.

"""
import regex


class Expression:
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
        if self.compiled == "":
            self.compiled = regex.compile(self.regex, regex.VERBOSE | regex.IGNORECASE)
        matches = self.compiled.findall(string)
        output = []
        for match in matches:
            match = self.run(match)
            if type(match) is list:
                output.extend(match)
            else:
                output.append(match)
        return output

    def run(self, matches):
        j = 0
        results = []
        for i in range(0, len(self.group_functions)):
            length = self.group_lengths[i]
            function_set = matches[(i + j):(i + j + length)]
            results.append(self.group_functions[i](function_set))
            j += length - 1
        return self.final_function(results)


def AlternatesGroup(expressions, final_function, name=""):
    inbetweens = ["|"] * (len(expressions) + 1)
    inbetweens[0] = ""
    inbetweens[-1] = ""
    return Group(expressions, final_function, inbetweens, name)


def Group(expressions, final_function, inbetweens, name=""):
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
