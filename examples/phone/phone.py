""" Example of a phone number parser
>>> phone_parser('+974-584-5656')  # doctest: +IGNORE_UNICODE
[phone(area_code='974', prefix='584', body='5656', fax=False)]
>>> phone_parser('Fax: +974-584-5656')  # doctest: +IGNORE_UNICODE
[phone(area_code='974', prefix='584', body='5656', fax=True)]
"""
from __future__ import unicode_literals

# Example stuff -----------------------------------------------------
# Have to add the parent directory just in case you
# run this file in the demo directory without installing Reparse
import sys

sys.path.append('../..')

# If file was imported, include that path
path = ""
if '__file__' in globals():
    import os

    path = str(os.path.dirname(__file__))
    if path:
        path += "/"

# Reparse ----------------------------------------------------------
from examples.phone.functions import functions
import reparse

phone_parser = reparse.parser(
    parser_type=reparse.basic_parser,
    expressions_yaml_path=path + "expressions.yaml",
    patterns_yaml_path=path + "patterns.yaml",
    functions=functions
)

if __name__ == "__main__":
    print(phone_parser(' +974-584-5656 '))
    print(phone_parser(' Fax: +974-584-5656 '))
