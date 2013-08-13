RE\|PARSE
=========

*Sane Regular Expression based parsers*

|Build Status|

Basically this library allows you to - build a database of Regular
Expressions in Yaml, - combine them together using Patterns - backed by
Python functions that build your output in the way that you want it.

A Taste / Getting Started
=========================

(See the demo/ directory for more detail)

I want to parse this
~~~~~~~~~~~~~~~~~~~~

::

     blah blah blah go to the store to buy green at 11pm! blah blah

Expressions written in Yaml
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: yaml

    Color:
        Basic Color:
            Expression: (Orange|Green)
            Matches: Orange | Green
            Non-Matches: Blue
            Groups:
              - Color

    Time:
        Basic Time:
            Expression: ([0-4]{2}):([[0-6][0-9])(am|pm)?
            Matches: 8:05pm | 0:00
            Non-Matches: 13:72
            Non-Matches: Blue
            Groups:
              - Hour
              - Minute
              - Period

Patterns written in Yaml
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: yaml

    BasicColorTime:
      Order: 1
      Pattern: |
        <Color> (?: \s? at \s? )? <Time>

Functions written in Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from datetime import time
    def color_time(Color=None, Time=None):
        Color, Hour, Period = Color[0], int(Time[0]), Time[1]
        if Period == 'pm':
            Hour += 12
        Time = time(hour=Hour)

        return Color, Time

Result
~~~~~~

.. code:: python

    [('green', datetime.time(23, 0))]

Support
=======

Need some help? Make issues on Github or send me an email at
andy@asperous.us and I'll do my best to help you.

Contribution
============

Send me suggestions, issues, and pull requests on Github and I'll gladly
review them!

Licence
=======

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
