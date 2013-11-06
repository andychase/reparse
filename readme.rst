RE|PARSE
========

*Python library/tools for combining and parsing using Regular Expressions in a maintainable way*

[|Build Status| `Download/View Source on Github`_] [`Docs at ReadtheDocs`_]

This library also allows you to:

- Maintain a database of Regular Expressions
- Combine them together using Patterns
- Search, Parse and Output data matched by combined Regex using Python functions.

This library basically just gives you a way to combine Regular Expressions together
and hook them up to some callback functions in Python.

A Taste / Getting Started
=========================

(See the examples/ directory for a full code examples)

Say your fashionista friend must know what colors their friends like at certain times.
Luckily for you two, your friend's friends are blogging fanatics and you have downloaded thousands
of text documents containing their every thought.

So you want to get (color and time) or ``[('green', datetime.time(23, 0))]`` out of text like::

     blah blah blah go to the store to buy green at 11pm! blah blah

If you need scan/search/parse/transform some unstructured input and get some semi-structured data
out of it RE|PARSE might be able to help.

First structure some Regular Expressions (Here, in Yaml)
--------------------------------------------------------

.. code-block:: yaml

    Color:
        Basic Color:
            Expression: (Red|Orange|Yellow|Green|Blue|Violet|Brown|Black)
            Matches: Orange | Green
            Non-Matches: White
            Groups:
              - Color

    Time:
        Basic Time:
            Expression: ([0-9]|[1][0-2]) \s? (am|pm)
            Matches: 8am | 3 pm
            Non-Matches: 8a | 8:00 am | 13pm
            Groups:
              - Hour
              - AMPM

Then structure some Patterns with those expressions (Yaml)
----------------------------------------------------------

.. code-block:: yaml

    BasicColorTime:
      Order: 1
      Pattern: |
        <Color> \s? at \s? <Time>
      # Angle brackets detonate expression groups
      # Multiple expressions in one group are combined together

Some callback functions (in Python)
-----------------------------------

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

Cool!

Intrigued? Learn more how to make the magic happen in `Howto: How to use RE|PARSE`_.

Want to read more about what RE|PARSE is and what it can do? More info in `About: Why another tool for parsing?`_

Info
====

.. _installation-howto:

Installation
------------

pip
~~~~
.. code-block:: python

    pip install reparse

manually
~~~~~~~~

1. If you don't have them already,
   RE|PARSE depends on REGEX_, and PyYaml_.
   Download those and ``python setup.py install`` in their directories.
   If you are on windows, you may have to find binary installers for these, since they
   contain modules that have to be compiled.

2. Download the `Zip off of Github`_ (or clone the repo).

3. Extract and do ``python setup.py install`` in the reparse containing the setup.py file directory.
   You can also just have the reparse/reparse directory in the source tree
   of your project if you don't want to install it.

4. Test with ``python -c "import reparse"``,
   no output means it is probably installed.
   If you get ``ImportError: No module named reparse``
   then you might want to recheck your steps.

Support
-------

Need some help? Send me an email at andy@asperous.us and I'll do my best to help you.

Contribution
------------

The code is located on Github_.
Send me suggestions, issues, and pull requests and I'll gladly review them!

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

.. _Download/View Source on Github: https://github.com/asperous/reparse

.. _Github: https://github.com/asperous/reparse

.. _Docs at Readthedocs: https://reparse.readthedocs.org/en/latest/

.. _`Howto: How to use RE|PARSE`: https://reparse.readthedocs.org/en/latest/howto.html

.. _`About: Why another tool for parsing?`: https://reparse.readthedocs.org/en/latest/about.html

.. _`REGEX`: https://pypi.python.org/pypi/regex

.. _`PyYaml`: https://pypi.python.org/pypi/PyYAML

.. _`Zip off of Github`: https://github.com/asperous/reparse/archive/master.zip
