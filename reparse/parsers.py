""" Contains all the parser types and the parser generator.
"""


def basic_parser(patterns, with_name=None):
    """ Basic ordered parser.
    """
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


def alt_parser(patterns):
    """ This parser is able to handle multiple different patterns
        finding stuff in text-- while removing matches that overlap.
    """
    from reparse.util import remove_lower_overlapping
    get_first = lambda items: [i[0] for i in items]
    get_second = lambda items: [i[1] for i in items]

    def parse(line):
        output = []
        for pattern in patterns:
            results = pattern.scan(line)
            if results and any(results):
                output.append((pattern.order, results))
        return get_first(reduce(remove_lower_overlapping, get_second(sorted(output)), []))

    return parse


def pattern_list(patterns):
    """ You can use this in the parser_type to
        simply get your list of patterns.
    """
    return patterns


def build_tree_parser(patterns):
    """ This parser_type simply outputs an array of [(tree, regex)]
        for use in another language.
    """
    def output():
        for pattern in patterns:
            yield (pattern.build_full_tree(), pattern.regex)
    return list(output())


def parser(parser_type=basic_parser, functions=None, patterns=None, expressions=None, patterns_yaml_path=None,
           expressions_yaml_path=None):
    """ A Reparse parser description.
        Simply provide the functions, patterns, & expressions to build.
        If you are using YAML for expressions + patterns, you can use
        ``expressions_yaml_path`` & ``patterns_yaml_path`` for convenience.

        The default parser_type is the basic ordered parser.
    """
    from reparse.builders import build_all
    from reparse.validators import validate

    def _load_yaml(file_path):
        import yaml
        with open(file_path) as f:
            return yaml.safe_load(f)

    assert expressions or expressions_yaml_path, "Reparse can't build a parser without expressions"
    assert patterns or patterns_yaml_path, "Reparse can't build a parser without patterns"
    assert functions, "Reparse can't build without a functions"

    if patterns_yaml_path:
        patterns = _load_yaml(patterns_yaml_path)
    if expressions_yaml_path:
        expressions = _load_yaml(expressions_yaml_path)
    validate(patterns, expressions)

    return parser_type(build_all(patterns, expressions, functions))
