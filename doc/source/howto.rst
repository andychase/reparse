Howto: How to use Reparse
=========================


You will need
-------------

#. A Python environment & some Regular Expression knowledge. Some resources: RegexOne_, Regex-Info_, W3Schools_.

#. Some example texts that you will want to parse and their solutions.
   This will be useful to check your parser and will help you put together the expressions and patterns.

1. Setup Python & Reparse
-------------------------

See :ref:`installation-howto` for instructions on how to install Reparse

2. Layout of an example Reparse parser
--------------------------------------

Reparse needs 3 things in its operation:

1. Functions: A dictionary with String Key -> Function Value mapping.

.. code-block:: python

    {'cool func': func}

2. Expressions: A dictionary with Groups (Dict) -> Expressions (Dict) -> Expression (String/Regex).
   I typically format this in Yaml since it's easy to read and write, but you can do it in json, or even straight
   in Python.

.. code-block:: python

    {'my cool group': {'my cool expression': {'expression': '[a-z]+'}}}

3. Patterns: A dictionary with Patterns (Dict) -> Pattern (String/Regex) (Ditto about the Yaml).

.. code-block:: python

    {'my cool pattern': {'pattern': "<my cool group>.*" }}


As I mentioned I typically just use Yaml so my file structure looks like this::

  my_parser.py <- The actual parser
  functions.py <- All the functions and a dictionary mapping them at the end
  expressions.yaml <- All of the Regex pieces nice and structured
  patterns.yaml <- All the Regex patterns

This isn't forced, you could have them all in one file, or it split up
in many, many files. This is just how I organize my parsing resources.

3. Writing your first expressions.yaml file
-------------------------------------------

*I'll be parsing Phone numbers in this example.*

.. Tip::

    You wanna know a secret? I don't do all the hard work myself, I often borrow Regexs off other sites
    like http://regexlib.com/.

.. code-block:: yaml

    Phone: # <- This is the expression group name, it's like the 'type' of your regex
           #    All the expressions in one group should be able to be substituted for each other
        Senthil Gunabalan: # <- This is the expression
                           # I use the authors name because I couldn't be asked to come up with names for all of them myself
            Expression: |
                [+]([0-9] \d{2}) - (\d{3}) - (\d{4})
            # Whitespace is ignored, so you can use it to make your regexs readable
            Description: This is a basic telephone number validation [...]
            Matches: +974-584-5656 | +000-000-0000 | +323-343-3453
            Non-Matches: 974-584-5656 | +974 000 0000
            Groups:
              - AreaCode
              - Prefix
              - Body
            # The keys in the Groups: field have to match up with the capture groups (stuff in parenthesis ()) in the Expression
            # They are used as keyword arguments to the function that processes this expression
            # (Expression groups 'Phone' and capture groups () are different)

So that's a basic expression file. The hierarchy goes:
    Group:
        Expression:
            Detail:
            Detail:
            Detail:
    Group:
        Expression:
            Detail:
            Detail:
            Detail:
        Expression:
            Detail:

4. Writing your first patterns.yaml file
----------------------------------------

There aren't any capture groups in patterns. All the capture groups should be done
in expressions and merely *combined* in patterns.

.. code-block:: yaml

    Basic Phone:
        Pattern: <Phone>
        Order: 1

    Fax Phone:
        Pattern: |
            Fax: \s <Phone>
        Order: 2
        # I could have used <Basic Phone> instead to use a pattern inside a pattern but it wouldn't have made a difference really (just an extra function call).

The order field tells Reparse which pattern to pick if multiple patterns match.
Generally speaking, the more specific patterns should be ordered higher than the lower ones
(you wouldn't want someone to try and call a fax machine!).

I could have split the expression above into 4 expression groups: Country Code, Area Code, 3-digit prefix, 4-digit body,
and combined them in the patterns file, and that would have looked like this:

.. code-block:: yaml

    Mega International:
        Pattern: [+]<Country Code>-<Area Code>-<3-digit prefix>-<4-digit body>

Done this way, I could have had 3 different formats for Area Code and the pattern would have matched
on any of them. I didn't here because that'd be overkill for phone numbers.

5. Writing your functions.py file
---------------------------------

Reparse matches text and also does some parsing using functions.

The order in which the functions are run and results passed are as follows:

#. The Function mapped to the Expression name is called with keyword arguments named in the ``Groups:`` key
   ('Senthil Gunabalan' in this example).

#. The output of that function is passed to the function mapped to the Expression Group ('Phone' in this example).

#. The output of that function is passed to the function mapped to the Pattern name ('Basic Phone' or 'Fax Phone').

#. (Optional) If you used *Patterns inside Patterns* then the output bubbles up to the top.

#. The output of that function is returned.

.. code-block:: python

    from collections import namedtuple
    Phone = namedtuple('phone', 'area_code prefix body fax')


    def senthill((AreaCode, Prefix, Body):
        return Phone(area_code=AreaCode, prefix=Prefix, body=Body, fax=False)


    def phone(p):
        return p[0]


    def basic_phone(p):
        return p


    def fax_phone(p):
        return p[0]._replace(fax=True)

    functions = {
       'Senthil Gunabalan' : senthill,
       'Phone' : phone,
       'Basic Phone' : basic_phone,
       'Fax Phone' : fax_phone
    }

I used namedtuples here, but you can parse your output anyway you want to.

6. Combining it all together!
-----------------------------

The builder.py module contains some functions to build a Reparse system together.
Here's how I'd put together my phone number parser:

.. code-block:: python

    from examples.phone.functions import functions
    import reparse

    phone_parser = reparse.parser(
        parser_type=reparse.basic_parser,
        expressions_yaml_path=path + "expressions.yaml",
        patterns_yaml_path=path + "patterns.yaml",
        functions=functions
    )


    print(phone_parser('+974-584-5656'))
    # => [phone(area_code='974', prefix='584', body='5656', fax=False)]
    print(phone_parser('Fax: +974-584-5656'))
    # => [phone(area_code='974', prefix='584', body='5656', fax=True)]

7. More info
------------

Yeah, so this was all basically straight out of the examples/phone directory
where you can run it yourself and see if it actually works.

There's more (or at least one more) example in there for further insight.

Happy parsing!

.. _RegexOne: http://regexone.com/
.. _Regex-Info: http://www.regular-expressions.info/tutorial.html
.. _W3Schools: http://w3schools.com/jsref/jsref_obj_regexp.asp
