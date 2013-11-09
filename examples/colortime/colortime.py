# Have to add the parent directory just in case you
# run this file in the demo directory without installing RE|PARSE
from examples.colortime.functions import functions
import reparse

# If file was imported, include that path
path = ""
if '__file__' in globals():
    import os
    path = str(os.path.dirname(__file__))
    if path:
        path += "/"

patterns_path = path + "patterns.yaml"
expressions_path = path + "expressions.yaml"
patterns = reparse.build_from_yaml(functions, expressions_path, patterns_path)


def parse(line):
    """
    >>> parse("~ ~ ~ go to the store ~ buy green at 11pm! ~ ~")
    [('green', datetime.time(23, 0))]
    """
    output = None
    highest_order = 0
    for pattern in patterns:
        results = pattern.findall(line)
        if results and any(results):
            if pattern.order > highest_order:
                output = results
                highest_order = pattern.order
    return output

if __name__ == "__main__":
    print parse("~ ~ ~ go to the store ~ buy green at 11pm! ~ ~")
