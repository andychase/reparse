import sys
sys.path.append('../..')

from functions import functions
import reparse

patterns_path = "patterns.yaml"
expressions_path = "expressions.yaml"
patterns = reparse.build_from_yaml(functions, expressions_path, patterns_path)


def parse(line):
    output = None
    highest_order = 0
    for pattern in patterns:
        results = pattern.findall(line)
        if results and any(results):
            if pattern.order > highest_order:
                output = results
                highest_order = pattern.order
    return output

print parse(' +974-584-5656 ')
print parse(' Fax: +974-584-5656 ')