Reparse
=======

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
out of it Reparse might be able to help.

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

Build your parser
-----------------

.. code-block:: python

    from examples.colortime.functions import functions
    import reparse


    colortime_parser = reparse.parser(
        parser_type=reparse.basic_parser,
        expressions_yaml_path=path + "expressions.yaml",
        patterns_yaml_path=path + "patterns.yaml",
        functions=functions
    )

    print(colortime_parser("~ ~ ~ go to the store ~ buy green at 11pm! ~ ~"))

Result
------

.. code-block:: python

    [('green', datetime.time(23, 0))]

Cool!

Intrigued? Learn more how to make the magic happen in `Howto: How to use Reparse`_.

Want to read more about what Reparse is and what it can do? More info in `About: Why another tool for parsing?`_

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
   Reparse depends on REGEX_, and PyYaml_.
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

Need some help? Send me an email at theandychase@gmail.com and I'll do my best to help you.

Contribution
------------

The code is located on Github_.
Send me suggestions, issues, and pull requests and I'll gladly review them!

Versions
--------

- *3.0* InvalidPattern Exception, Allow monkey patching regex arguments. RE|PARSE -> Reparse.
- *2.1* Change `yaml.load` to `yaml.safe_load` for security
- *2.0* Major Refactor, Python 3, Better Parser builders
- *1.1* Fix setup.py
- *1.0* Release

Licence
-------

MIT Licensed! See LICENSE file for the full text.

.. |Build Status| image:: https://travis-ci.org/andychase/reparse.svg?branch=master
   :target: https://travis-ci.org/andychase/reparse

.. _Download/View Source on Github: https://github.com/andychase/reparse

.. _Github: https://github.com/andychase/reparse

.. _Docs at Readthedocs: https://reparse.readthedocs.org/en/latest/

.. _`Howto: How to use Reparse`: https://reparse.readthedocs.org/en/latest/howto.html

.. _`About: Why another tool for parsing?`: https://reparse.readthedocs.org/en/latest/about.html

.. _`REGEX`: https://pypi.python.org/pypi/regex

.. _`PyYaml`: https://pypi.python.org/pypi/PyYAML

.. _`Zip off of Github`: https://github.com/andychase/reparse/archive/master.zip
