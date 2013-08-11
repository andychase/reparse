#!/usr/bin/env python
from distutils.core import setup

setup(name='Reparse',
      version='1.0',
      description='Sane Regular Expression based parsers',
      long_description= \
      """ RE|PARSE provides tools for structuring and using
      regular expressions to perform searching and parsing tasks.
      Basically this library allows you to

      *  build a database of Regular Expressions,
      *  combine them together using Regular Expression Patterns,
      *  & transform / build the output using Python functions.
      """,
      author='Andy Chase',
      url='http://github.com/asperous/reparse',
      download_url="https://github.com/asperous/reparse/archive/master.zip",
      license="MIT",
      packages=['reparse'],
     )