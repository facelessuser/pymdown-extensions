#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup pymdown-extensions."""

from setuptools import setup, find_packages

LONG_DESC = '''
PyMdown Extensions (pymdownx) is a collection of extensions for `Python Markdown`_.
It should work for Python Markdown versions 2.6.0 and greater.
You can check out the list of available extensions and learn more about them by `reading the docs`_.

.. _`Python Markdown`: https://pythonhosted.org/Markdown/
.. _`reading the docs`: http://facelessuser.github.io/pymdown-extensions/

Support
=======

Help and support is available here at the repositories `bug tracker`_.
Please read about `support and contributing`_ before creating issues.

.. _`bug tracker`: https://github.com/facelessuser/pymdown-extensions/issues
.. _`support and contributing`: http://facelessuser.github.io/pymdown-extensions/contributing/
'''

setup(
    name='pymdown-extensions',
    version='1.0.0',
    keywords='markdown extensions',
    description='Extension pack for Python Markdown.',
    long_description=LONG_DESC,
    author='Isaac Muse',
    author_email='Isaac.Muse [at] gmail.com',
    url='https://github.com/facelessuser/pymdown-extensions',
    packages=find_packages(),
    install_requires=[
        'Markdown>=2.6.0,<3'
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
