""" Example from docs
>>> colortime_parser("~ ~ ~ go to the store ~ buy green at 11pm! ~ ~")
[('green', datetime.time(23, 0))]
"""
# Example stuff -----------------------------------------------------
# Have to add the parent directory just in case you
# run this file in the demo directory without installing RE|PARSE
import sys
sys.path.append('../..')

# If file was imported, include that path
path = ""
if '__file__' in globals():
    import os
    path = str(os.path.dirname(__file__))
    if path:
        path += "/"


# RE|PARSE ----------------------------------------------------------
from examples.colortime.functions import functions
import reparse


colortime_parser = reparse.parser(
    parser_type=reparse.basic_parser,
    expressions_yaml_path=path + "expressions.yaml",
    patterns_yaml_path=path + "patterns.yaml",
    functions=functions
)

if __name__ == "__main__":
    print(colortime_parser("~ ~ ~ go to the store ~ buy green at 11pm! ~ ~"))
