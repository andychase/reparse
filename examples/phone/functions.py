"""
This file contains the parsing functions related to parsers

The point is that each function can take in part of the results and
use custom logic to parse a meaningful output from it.
"""
from collections import namedtuple
Phone = namedtuple('phone', 'area_code prefix body fax')


# --------------- Functions ------------------
def senthill(AreaCode, Prefix, Body):
    return Phone(area_code=AreaCode, prefix=Prefix, body=Body, fax=False)


def phone(p):
    return p[0]


def basic_phone(p):
    return p


def fax_phone(p):
    return p._replace(fax=True)

# --------------- Function list ------------------
# This is the dictionary that is used by the Reparse
# expression builder. The key is the same value used in the patterns.yaml
# file under ``Function: ``. The value is a reference to function.

# Defining functions at each level is often useful,
# but there are default functions to save time.

# This has to go last in this file so that the functions are
# actually defined in Python when we get to this point.
functions = {
    # Groups
    # Expressions
    'Senthil Gunabalan': senthill,
    # Type
    'Phone': phone,
    # Patterns
    'Basic Phone': basic_phone,
    'Fax Phone':  fax_phone
}
