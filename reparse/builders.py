import yaml
from reparse.expression import Group, AlternatesGroup, Expression

patterns_inside_patterns_depth = 10


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
    if len(extra) > 0 and depth < patterns_inside_patterns_depth:
        # Recursive building for patterns inside of patterns
        build_all_from_dict(output_patterns, extra, expression_builder, function_builder, depth + 1)
    elif depth >= patterns_inside_patterns_depth:
        raise ExpressionGroupNotFound()
    return output_patterns


def build_from_yaml(functions_dict, expressions_path, patterns_path):
    def load_yaml(file_path):
        with open(file_path) as f:
            return yaml.load(f)
    function_builder = Function_Builder(functions_dict)
    expression_builder = Expression_Builder(load_yaml(expressions_path), function_builder)
    return build_all_from_dict([], load_yaml(patterns_path), expression_builder, function_builder)
