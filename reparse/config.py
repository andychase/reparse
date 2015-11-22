import regex

# This number should be bigger than the longest
# chain of patterns-inside-patterns
pattern_max_recursion_depth = 10

# The regex engine and settings
regex_flags = regex.VERBOSE | regex.IGNORECASE

def get_expression_compiler():
    return lambda expression: regex.compile(expression, flags=regex_flags)
    
def get_expression_sub(): 
    return lambda expression, sub, string: regex.sub(expression, sub, string, flags=regex_flags)
