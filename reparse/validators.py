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
