from reparse.expression import Group, AlternatesGroup, Expression
from reparse.util import separate_string


class ExpressionGroupNotFound(Exception):
    pass


class Function_Builder(object):
    """
    Function Builder is an on-the-fly builder of functions for expressions

    >>> def t(_):
    ...     return _
    >>> fb = Function_Builder({"hey":t})
    >>> fb.get_function("hey", "") is t
    True
    """

    def __init__(self, functions_dict):
        self._functions = functions_dict

    def get_function(self, name, function_type, group_names=None):
        if name in self._functions:
            if function_type is "type":
                def func(_):
                    if not any(_):
                        return None
                    return self._functions[name](_)
            elif function_type is "group":
                def func(_):
                    return self._functions[name](_[0])
            elif function_type is "expression" and group_names is not None:
                def func(_):
                    groups = dict(zip(group_names, _))
                    return self._functions[name](**groups)
            elif function_type is "pattern":
                def func(_):
                    return self._functions[name](*_)
            else:
                func = self._functions[name]

        # DEFAULT FUNCTIONS
        elif function_type is "group":
            def func(_):
                if _:
                    return _[0]
        elif function_type is "type":
            def func(_):
                for i in _:
                    if i is not None:
                        return i
        else:
            def func(_):
                if any(_):
                    return _
        return func

    def add_function(self, name, function):
        self._functions[name] = function


class Expression_Builder(object):
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

