About: Why another tool for parsing?
====================================

Reparse is simply a tool for combining regular expressions together
and using a regular expression engine to scan/search/parse/process input for certain tasks.

Larger parsing tools like YACC/Bison, ANTLR, and others are really
good for structured input like computer code or xml. They aren't specifically
designed for scanning and parsing semi-structured data from unstructured
text (like books, or internet documents, or diaries).

Reparse is designed to work with exactly that kind of stuff, (and is completely
useless for the kinds of tasks any of the above is often used for).

Parsing Spectrum
----------------

Reparse isn't the first parser of it's kind. A hypothetical spectrum
of parsers from pattern-finding only
all the way to highly-featured, structured grammars might look something like this::

                    v- Reparse            v- YACC/Bison
    UNSTRUCTURED |-------------------------| STRUCTURED
                 ^- Regex     ^- Parboiled/PyParsing

Reparse is in fact very featureless. It's only a little better
than plain regular expressions. Still, you might find it ideal
for the kinds of tasks it was designed to deal with (like dates and addresses).


What kind of things might Reparse be useful for parsing?
--------------------------------------------------------

Any kind of semi-structured formats:

- Uris
- Numbers
- Strings
- Dates
- Times
- Addresses
- Phone numbers

Or in other words, anything you might consider parsing with Regex, might consider Reparse,
especially if you are considering combining multiple regular expressions together.

Why Regular Expressions
-----------------------

PyParsing (Python) and Parboiled (JVM) also have use-cases very similar
to Reparse, and they are much more feature-filled. They have their own (much more powerful)
DSL for parsing text.

Reparse uses Regular Expressions which has some advantages:

- Short, minimal Syntax
- Universal (with some minor differences between different engines)
- Standard
- Moderately Easy-to-learn (Though this is highly subjective)
    - Many programmers already know the basics
    - Skills can be carried else where
- **Regular Expressions can be harvested elsewhere and used within Reparse**
- Decent performance over large inputs
- Ability to use fuzzy matching regex engines


Limitations of Reparse
----------------------

Regular Expressions have been known to catch input that was unexpected,
or miss input that was expected due to unforeseen edge cases.
Reparse provides tools to help alleviate this by checking the expressions against expected matching
inputs, and against expected non-matching inputs.

This library is very limited in what it can parse, if you realize
you need something like a recursive grammar, you might want to try PyParsing or something greater
(though Reparse might be helpful as a 'first step' matching and transforming the parse-able data before it is properly
parsed by a different library).