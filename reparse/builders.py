from reparse.expression import Group, AlternatesGroup, Expression
from reparse.config import pattern_max_recursion_depth


class ExpressionGroupNotFound(Exception):
    pass


class Function_Builder:
    """
    Function Builder is an on-the-fly builder of functions for expressions

    >>> def t(input):
    ...     return input
    >>> fb = Function_Builder({"hey":t})
    >>> fb.get_function("hey", "") is t
    True
    """

    _functions = {}

    def __init__(self, functions_dict):
        self._functions = functions_dict

    def get_function(self, name, function_type, group_names=None):
        if name in self._functions:
            if function_type is "type":
                def func(input):
                    if not any(input):
                        return None
                    return self._functions[name](input)
            elif function_type is "group":
                def func(input):
                    return self._functions[name](input[0])
            elif function_type is "expression" and group_names is not None:
                def func(input):
                    groups = dict(zip(group_names, input))
                    return self._functions[name](**groups)
            elif function_type is "pattern":
                def func(input):
                    return self._functions[name](*input)
            else:
                func = self._functions[name]

        # DEFAULT FUNCTIONS
        elif function_type is "group":
            def func(input):
                if input:
                    return input[0]
        elif function_type is "type":
            def func(input):
                for i in input:
                    if i is not None:
                        return i
        else:
            def func(input):
                if any(input):
                    return input
        return func

    def add_function(self, name, function):
        self._functions[name] = function


class Expression_Builder:
    """ Expression builder is useful for building
    regex bits with Groups that cascade down::

                 from  GROUP      (group).?,?(group)|(group) (group)
                   to  EXPRESSION        (group)    |   (group)
                   to  TYPE                      (group)
    >>> dummy = lambda input: input
    >>> get_function = lambda *_, **__: dummy
    >>> function_builder = lambda: None
    >>> function_builder.get_function = get_function
    >>> expression = {'greeting':{'greeting':{'Expression': '(hey)|(cool)', 'Groups' : ['greeting', 'cooly']}}}
    >>> eb = Expression_Builder(expression, function_builder)
    >>> eb.get_type("greeting").findall("hey, cool!")
    [[('hey',), ('',)], [('',), ('cool',)]]
    """
    type_db = {}

    def __init__(self, expressions_dict, function_builder):
        for expression_type, expressions in expressions_dict.iteritems():
            type_expressions = []
            for name, expression in expressions.iteritems():
                groups = expression['Groups']
                regex = expression['Expression']
                lengths = [1] * len(groups)
                group_functions = [function_builder.get_function(g, "group") for g in groups]
                expression_final_function = \
                    function_builder.get_function(name, function_type="expression", group_names=groups)
                e = Expression(regex, group_functions, lengths, expression_final_function)
                type_expressions.append(e)
            type_final_function = function_builder.get_function(expression_type, function_type="type")
            self.type_db[expression_type] = AlternatesGroup(type_expressions, type_final_function)

    def get_type(self, type_string):
        if type_string in self.type_db:
            return self.type_db[type_string]

    def add_type(self, expression, type_string):
        self.type_db[type_string] = expression


def build_pattern(pattern_name, pattern_regex, expression_builder, function_builder):
    final_function = function_builder.get_function(pattern_name, "pattern")
    inbetweens, expression_names = separate_string(pattern_regex, "<", ">")
    expressions = []
    for name in expression_names:
        expression = expression_builder.get_type(name)
        if expression is None:
            raise ExpressionGroupNotFound("Expression Group ({}) not Found!".format(name))
        expressions.append(expression)
    return Group(expressions, final_function, inbetweens, pattern_name)


# Utility functions
def separate_string(string, start_delimiter, end_delimiter):
    """
    >>> separate_string("test (2)", "(", ")")
    (['test ', ''], ['2'])
    """
    string_list = string.replace(end_delimiter, start_delimiter).split(start_delimiter)
    return string_list[::2], string_list[1::2]  # Returns even and odd elements


def build_all_from_dict(output_patterns, patterns_dict, expression_builder, function_builder, depth=0):
    extra = {}
    for name, pattern in patterns_dict.iteritems():
        try:
            pat = build_pattern(name, pattern['Pattern'], expression_builder, function_builder)
            pat.order = int(pattern.get('Order', 0))
            output_patterns.append(pat)
            expression_builder.add_type(pat, name)
        except ExpressionGroupNotFound:
            extra[name] = pattern
    if len(extra) > 0 and depth < pattern_max_recursion_depth:
        # Recursive building for patterns inside of patterns
        build_all_from_dict(output_patterns, extra, expression_builder, function_builder, depth + 1)
    elif depth >= pattern_max_recursion_depth:
        raise ExpressionGroupNotFound()
    return output_patterns


def build_from_yaml(functions_dict, expressions_path, patterns_path):
    import yaml

    def load_yaml(file_path):
        with open(file_path) as f:
            return yaml.load(f)

    expressions, patterns = load_yaml(expressions_path), load_yaml(patterns_path)
    if expression_pattern_switched(patterns, expressions):
        raise Exception("Your expressions and patterns paths are valid, but switched in the arg list "
                        "for the call to build_from_yaml.")

    for test, item in ((valid_expressions_dict, expressions), (valid_patterns_dict, patterns)):
        result, msg = test(item)
        if not result:
            raise Exception(msg)

    function_builder = Function_Builder(functions_dict)
    expression_builder = Expression_Builder(load_yaml(expressions_path), function_builder)
    return build_all_from_dict([], load_yaml(patterns_path), expression_builder, function_builder)


def build_parser_from_yaml(functions_dict, expressions_path, patterns_path, with_name=False):
    patterns = build_from_yaml(functions_dict, expressions_path, patterns_path)

    def parse(line):
        output = None
        highest_order = 0
        highest_pattern_name = None
        for pattern in patterns:
            results = pattern.findall(line)
            if results and any(results):
                if pattern.order > highest_order:
                    output = results
                    highest_order = pattern.order
                    if with_name:
                        highest_pattern_name = pattern.name
        if with_name:
            return output, highest_pattern_name
        return output
    return parse


def alt_build_parser_from_yaml(functions_dict, expressions_path, patterns_path):
    """
    This parser is able to handle multiple different patterns
    finding stuff in text-- while removing matches that overlap.
    """
    def overlapping(start1, end1, start2, end2):
        """
        >>> overlapping(0, 5, 6, 7)
        False
        >>> overlapping(1, 2, 0, 4)
        True
        >>> overlapping(5,6,0,5)
        False
        """
        return not ((start1 <= start2 and start1 <= end2 and end1 <= end2 and end1 <= start2) or
                    (start1 >= start2 and start1 >= end2 and end1 >= end2 and end1 >= start2))

    def overlapping_at(start, end, current):
        for current_index, (_, c_start, c_end) in enumerate(current):
            if overlapping(c_start, c_end, start, end):
                yield current_index

    def remove_lower_overlapping(current, higher):
        """
        >>> remove_lower_overlapping([], [('a', 0, 5)])
        [('a', 0, 5)]
        >>> remove_lower_overlapping([('z', 0, 4)], [('a', 0, 5)])
        [('a', 0, 5)]
        >>> remove_lower_overlapping([('z', 5, 6)], [('a', 0, 5)])
        [('z', 5, 6), ('a', 0, 5)]
        """
        for i, (match, h_start, h_end) in enumerate(higher):
            overlaps = list(overlapping_at(h_start, h_end, current))
            for overlap in overlaps:
                del current[overlap]
            if len(overlaps) > 0:
                # Keeps order in place
                current.insert(overlaps[0], (match, h_start, h_end))
            else:
                current.append((match, h_start, h_end))

        return current

    get_first = lambda items: [i[0] for i in items]
    get_second = lambda items: [i[1] for i in items]

    patterns = build_from_yaml(functions_dict, expressions_path, patterns_path)

    def parse(line):
        output = []
        for pattern in patterns:
            results = pattern.scan(line)
            if results and any(results):
                output.append((pattern.order, results))
        return get_first(reduce(remove_lower_overlapping, get_second(sorted(output)), []))

    return parse

# Validators
pattern_key_error = "Pattern [{}] does not contain the 'Pattern' key"
expression_key_error = "Expression Type [{}] Expression [{}] does not contain the 'Expression' key"


def valid_patterns_dict(patterns_dict):
    for name, pattern in patterns_dict.iteritems():
        if 'Pattern' not in pattern:
            return False, pattern_key_error.format(name)
    return True, ""


def valid_expressions_dict(expressions_dict):
    for type_name, type in expressions_dict.iteritems():
        for exp_name, exp in type.iteritems():
            if 'Expression' not in exp:
                return False, expression_key_error.format(type_name, exp_name)
    return True, ""


def expression_pattern_switched(patterns_dict, expressions_dict):
    # It's a common mistake to switch pattern and expression dict -- check for that
    return valid_patterns_dict(expressions_dict)[0] and valid_expressions_dict(patterns_dict)[0]