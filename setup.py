#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup pymdown-extensions."""

from setuptools import setup, find_packages
import os
import imp

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


def get_version():
    """Get version and version_info without importing the entire module."""

    devstatus = {
        'alpha': '3 - Alpha',
        'beta': '4 - Beta',
        'candidate': '4 - Beta',
        'final': '5 - Production/Stable'
    }
    path = os.path.join(os.path.dirname(__file__), 'pymdownx')
    fp, pathname, desc = imp.find_module('__version__', [path])
    try:
        v = imp.load_module('__version__', fp, pathname, desc)
        return v.version, devstatus[v.version_info[3]]
    finally:
        fp.close()


VER, DEVSTATUS = get_version()


setup(
    name='pymdown-extensions',
    version=VER,
    keywords='markdown extensions',
    description='Extension pack for Python Markdown.',
    long_description=LONG_DESC,
    author='Isaac Muse',
    author_email='Isaac.Muse [at] gmail.com',
    url='https://github.com/facelessuser/pymdown-extensions',
    packages=find_packages(exclude=['tools', 'tests']),
    install_requires=[
        'Markdown>=2.6.0,<3'
    ],
    license='MIT License',
    classifiers=[
        'Development Status :: %s' % DEVSTATUS,
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML',
    ]
)
