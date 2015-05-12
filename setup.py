#!/usr/bin/env python
import os
from setuptools import setup


def readme_or_docstring():
    path = os.path.join(os.path.dirname(__file__), 'readme.rst')
    if os.path.isfile(path):
        return open(path).read()
    else:
        import reparse

        return reparse.__doc__

setup(name='reparse',
      version='2.1',
      description='Sane Regular Expression based parsers',
      long_description=readme_or_docstring(),
      author='Andy Chase',
      author_email='theandychase@gmail.com',
      url='http://github.com/andychase/reparse',
      download_url="https://github.com/andychase/reparse/archive/master.zip",
      license="MIT",
      packages=['reparse'],
      install_requires=["regex"],
      classifiers=(
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Text Processing'
      ),
      )
