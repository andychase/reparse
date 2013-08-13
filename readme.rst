RE\|PARSE
=========

*Python library/tools for combining and using Regular Expressions in a maintainable way*

|Build Status|

This library also allows you to:

- Maintain a database of Regular Expressions
- Combine them together using Patterns
- Search, Parse and Output data matched by combined Regex using Python functions.

A Taste / Getting Started
=========================

(See the examples/ directory for more details)

I want to parse this
--------------------

::

     blah blah blah go to the store to buy green at 11pm! blah blah

Expressions written in Yaml
---------------------------

.. code-block:: yaml

    Color:
        Basic Color:
            Expression: (Orange|Green)
            Matches: Orange | Green
            Non-Matches: Blue
            Groups:
              - Color

    Time:
        Basic Time:
            Expression: ([0-9]|[1][0-2]) \s? (am|pm)
            Matches: 8am | 8 am
            Non-Matches: 8a | 8 a | 8:00 am
            Groups:
              - Hour
              - AMPM

Patterns written in Yaml
------------------------

.. code-block:: yaml

    BasicColorTime:
      Order: 1
      Pattern: |
        <Color> (?: \s? at \s? )? <Time>

Functions written in Python
---------------------------

.. code-block:: python

    from datetime import time
    def color_time(Color=None, Time=None):
        Color, Hour, Period = Color[0], int(Time[0]), Time[1]
        if Period == 'pm':
            Hour += 12
        Time = time(hour=Hour)

        return Color, Time

Result
------

.. code-block:: python

    [('green', datetime.time(23, 0))]


Info
====

Support
-------

Need some help? Make issues on Github or send me an email at
andy@asperous.us and I'll do my best to help you.

Contribution
------------

Send me suggestions, issues, and pull requests on Github and I'll gladly
review them!

Licence
-------

The MIT License (MIT)

Copyright (c) 2013 Andrew Chase

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. |Build Status| image:: https://travis-ci.org/asperous/reparse.png?branch=master
   :target: https://travis-ci.org/asperous/reparse
