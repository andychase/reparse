# Utility functions
from reparse import pattern_max_recursion_depth
from reparse.builders import build_pattern, ExpressionGroupNotFound, Function_Builder, Expression_Builder
from reparse.util import remove_lower_overlapping
from reparse.validators import expression_pattern_switched, valid_expressions_dict, valid_patterns_dict


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
    """ This parser is able to handle multiple different patterns
        finding stuff in text-- while removing matches that overlap.
    """
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
