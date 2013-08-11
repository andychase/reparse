"""
This file contains the parsing functions related to patterns

The point is that each function can take in a result list and
   use custom logic to parse a meaningful date group from it.
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
# This is the dictionary that is used by the RE|PARSE
# expression builder. The key is the same key used in the patterns.yaml
# file for Function: ~~~. The value is the function.

# Defining functions at each level is often more useful,
#   but there is a catch-all function to save time.

# This has to go last so that the functions are actually defined
# in Python when we get build this.
functions = {
    # Groups
    # Expressions
    # Type
    # Patterns
    'BasicColorTime': color_time
}
