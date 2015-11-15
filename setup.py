#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup pymdown-extensions."""

from setuptools import setup, find_packages

LONG_DESC = '''
This is an extension pack for Python Markdown.

It was written for the the PyMdown project: https://github.com/facelessuser/PyMdown

It adds a number of optional extensions:
- pymdownx.b64
- pymdownx.betterem
- pymdownx.caret
- pymdownx.critic
- pymdownx.github
- pymdownx.githubemoji
- pymdownx.headeranchor
- pymdownx.inlinehilite
- pymdownx.magiclink
- pymdownx.mark
- pymdownx.arithmatex
- pymdownx.pathconverter
- pymdownx.plainhtml
- pymdownx.progressbar
- pymdownx.pymdown
- pymdownx.smartsymbols
- pymdownx.superfences
- pymdownx.tasklist
- pymdownx.tilde
'''

setup(
    name='pymdown-extensions',
    version='1.0.0',
    keywords='markdown extensions',
    description='Markdown extensions for Python Markdown.',
    long_description=LONG_DESC,
    author='Isaac Muse',
    author_email='Isaac.Muse [at] gmail.com',
    url='https://github.com/facelessuser/pymdown-extensions',
    packages=find_packages(),
    install_requires=[
        'Markdown>=2.6.0,<3',
        'requests>=2.7.0'
    ],
    license='MIT License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML',
    ]
)
