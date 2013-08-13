.. include:: ../../readme.rst

Yet another tool for parsing
============================

RE|PARSE is simply a tool for combining regular expressions together
and using a regular expression engine backend for certain tasks.

Larger parsing tools like YACC/Bison, ANTLR, and others are really
good for structured input like computer code. Consequently, they are poor
for scanning and parsing over unstructured input like natural languages.

RE|PARSE is designed to deal with unstructured input, and would be really
poor at dealing with parsing structured input effectively. This is simply
because it's based entirely on regex and can't do recursive
grammars or repetition well.

Parsing Spectrum
----------------

RE|PARSE isn't the first parser of it's kind. If there was a spectrum
of parsers and the kinds of inputs they are able to deal with
it might look like this::

       v- RE|PARSE            v- YACC/Bison
    |-------------------------|
    ^- Regex     ^- Parboiled/PyParsing

RE|PARSE is in fact a very feature-less. It's only a little better
than plain regular expressions. Still, this makes it easy to use
for the kinds of tasks it was designed to deal with (like dates and addresses).


What kind of tasks is this useful for
--------------------------------------

Anything kind of semi-structured formats found in natural language text:

- Uris
- Numbers
- Strings
- Dates
- Times
- Addresses
- Phone numbers

Or in other words, anything you might consider parsing with Regex, might consider RE|PARSE,
especially if you are considering combining multiple regular expressions together.

Why Regular Expressions
--------------------------------

PyParsing (Python) and Parboiled (JVM) also have use-cases very similar
to RE|PARSE, and they are much more feature-filled. Consequently, they have
embedded their own DSL for parsing text.

RE|PARSE was designed to purely use Regular Expressions which has some advantages:

- Short, minimal Syntax
- Universal (with some minor differences between different engines)
- Standard
- Moderately Easy-to-learn (Though this is highly subjective)
    - Many programmers already know the basics
    - Skills can be carried else where
- **Regular Expressions can be harvested elsewhere and used within RE|PARSE**


Limitations of RE|PARSE
-------------------------

Regular Expressions can often catch input that was unexpected,
or miss input that was expected. RE|PARSE provides tools to help
catch what is needed, and keep out what is not.

Also this library is very limited in what in can parse, if you realize
you need something like a recursive grammar, first consider if RE|PARSE
could be used as the first step (such as capturing all the data before it is parsed),
but otherwise you might want to try PyParsing or something greater.

Design of RE|PARSE
====================

The design of RE|PARSE is that one can obtain or write Regular Expressions
from websites such as http://regexlib.com/ and then combine them with patterns.

Best practices for Regular Expressions
-------------------------------------

Take good care of your Regex, and they'll take good care of you, so to speak.
There are several best practices for dealing with Regex so that they are useful,
without getting out of control.

- use whitespace and comments in your regular expression
- maintain a Matches and Non-Matches
    - RE|PARSE can use this to test your Regex to make sure they are working properly
    - Helps maintainers see which regular expressions do what
    - Help show your intention with each expression, so that others can improve or change it
- maintain a description which talks about what you are matching with each regex, and
  possibly a url where they can find more information about that format
- Having each regex author list his name can be a great boon, both because it gives them
  credit for their work, as well as it encourages them to put forth their best effort.
  I often put the author and a short name as the name of the regex, which is an easy way
  to come up with unique names for regexes that are often really similar.


Here are some resources for more info

http://www.codinghorror.com/blog/2008/06/regular-expressions-now-you-have-two-problems.html

Expressions
-----------

Patterns
--------

Functions
---------
