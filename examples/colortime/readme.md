This directory shows a very basic RE|PARSE setup to help you get started.

    expressions.yaml -- Contains the regular expression building blocks
    patterns.yaml    -- Contains the regular expression "glue"
    functions.py     -- Contains the python instructions for building the output

This example shows the steps to get from:
   blah blah blah go to the store to buy green at 11pm! blah blah

To:
```python
    [('green', datetime.time(23, 0))]
```