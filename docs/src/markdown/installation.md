# Installation

## Requirements

In order for PyMdown Extensions to work, there are a couple of prerequisites.

Name                               | Required | Details
---------------------------------- | -------- | -------
[Python Markdown][python-markdown] | Yes      | Python Markdown must be installed as it is the Markdown parser that is being used.
[Pygments (optional)][pygments]    | No       | If Pygments Syntax highlighting is desired, Pygments must be installed.  This can be omitted, and code blocks will be formatted for use with JavaScript code highlighters.

## Installation

Installation is easy with pip:

```console
$ pip install pymdown-extensions
```

If you want to manually install it, run:

```console
$ python setup.py build
$ python setup.py install
```

After installing, you should be able to access the extensions in Python Markdown under the namespace
`pymdownx.<extension>`.

If you would like to modify the code, you can install it via:

```console
$ pip install --editable .
```

This method will allow you to instantly see your changes without reinstalling.  If you want to do this in a virtual
environment, you can.
