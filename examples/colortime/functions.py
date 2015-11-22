"""
This file contains the parsing functions related to parsers

The point is that each function can take in part of the results and
use custom logic to parse a meaningful output from it.
"""

from datetime import time


# --------------- Functions ------------------
def color_time(Color=None, Time=None):
    Color, Hour, Period = Color[0], int(Time[0]), Time[1]
    if Period == 'pm':
        Hour += 12
    Time = time(hour=Hour)

    return Color, Time

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
    # Type
    # Patterns
    'BasicColorTime': color_time
}
