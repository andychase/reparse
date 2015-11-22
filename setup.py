#!/usr/bin/env python
import os
from setuptools import setup


def readme_or_docstring():
    path = os.path.join(os.path.dirname(__file__), 'readme.rst')
    if os.path.isfile(path):
        return open(path).read()
    else:
        try:
            import reparse
            return reparse.__doc__
        except ImportError:
            return 'Regular Expression based parsers for extracting data from natural language'


setup(
    name='reparse',
    version='3.0',
    description='Regular Expression based parsers for extracting data from natural language',
    long_description=readme_or_docstring(),
    author='Andy Chase',
    author_email='theandychase@gmail.com',
    url='http://github.com/andychase/reparse',
    download_url='https://github.com/andychase/reparse/archive/master.zip',
    license='MIT',
    packages=['reparse'],
    install_requires=[
        'regex',
        'pyyaml'
    ],
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing'
    ),
)
