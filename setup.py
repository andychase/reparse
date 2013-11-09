#!/usr/bin/env python
import os
from distutils.core import setup


def readme_or_docstring():
    path = os.path.join(os.path.dirname(__file__), 'readme.rst')
    if os.path.isfile(path):
        return open(path).read()
    else:
        import reparse

        return reparse.__doc__

setup(name='Reparse',
      version='1.1',
      description='Sane Regular Expression based parsers',
      long_description=readme_or_docstring(),
      author='Andy Chase',
      author_email='andy@asperous.us',
      url='http://github.com/asperous/reparse',
      download_url="https://github.com/asperous/reparse/archive/master.zip",
      license="MIT",
      packages=['reparse'],
      install_requires=[
          "regex",
          "pyyaml",
      ],
      classifiers=(
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Text Processing'
      ),
      )
