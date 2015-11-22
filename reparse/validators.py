from __future__ import unicode_literals

# Validators
pattern_key_error = "Pattern [{}] does not contain the 'Pattern' key"
expression_key_error = "Expression Type [{}] Expression [{}] does not contain the 'Expression' key"


def valid_patterns_dict(patterns_dict):
    for name, pattern in patterns_dict.items():
        if 'Pattern' not in pattern:
            return False, pattern_key_error.format(name)
    return True, ""


def valid_expressions_dict(expressions_dict):
    for expression_type_name, expression_type in expressions_dict.items():
        for name, _type in expression_type.items():
            if 'Expression' not in _type:
                return False, expression_key_error.format(expression_type_name, name)
    return True, ""


def expression_pattern_switched(patterns_dict, expressions_dict):
    # It's a common mistake to switch pattern and expression dict -- check for that
    return valid_patterns_dict(expressions_dict)[0] and valid_expressions_dict(patterns_dict)[0]


def validate(patterns, expressions):
    if expression_pattern_switched(patterns, expressions):
        raise Exception("Your expressions and patterns paths are valid, but switched in the arg list "
                        "for the call to build_from_yaml.")

    for test, item in ((valid_expressions_dict, expressions), (valid_patterns_dict, patterns)):
        result, msg = test(item)
        if not result:
            raise Exception(msg)
