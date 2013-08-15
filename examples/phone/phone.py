import sys
sys.path.append('../..')

from functions import functions
import reparse

# If file was imported, include that path
path = ""
if '__file__' in globals():
    import os
    path = str(os.path.dirname(__file__)) + "/"

patterns_path = path + "patterns.yaml"
expressions_path = path + "expressions.yaml"
patterns = reparse.build_from_yaml(functions, expressions_path, patterns_path)


def parse(line):
    """
    >>> parse('+974-584-5656')
    [phone(area_code='974', prefix='584', body='5656', fax=False)]
    >>> parse('Fax: +974-584-5656')
    [phone(area_code='974', prefix='584', body='5656', fax=True)]
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
    print parse(' +974-584-5656 ')
    print parse(' Fax: +974-584-5656 ')