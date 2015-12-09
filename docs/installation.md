# Installation {: .doctitle}
Installation of PyMdown Extensions.

---

## Overview
Pymdown Extensions is built on top of a few requirements.  If installing, the requirements will be installed automatically unless the requirement is optional.

## Requirements
In order for PyMdown Extensions to work, there are a couple of prerequisites.

| Name | Required |Details |
|------|----------|--------|
| [Python Markdown 2.6.0+][py_md] | Yes |Python Markdown must be installed as it is the Markdown parser that is being used. |
| [Pygments 2.0.1+ (optional)][pygments] | No | If Pygments Syntax highlighting is desired, Pygments must be installed.  This can be omitted, and code blocks (if using the CodeHilite extension) will be formatter for use with JavaScript code highlighters. |

## Installation
Installation is easy with pip:

```bash
pip install pymdown-extensions
```

If you want to manually install it, run `#!bash python setup.py build` and `#!bash python setup.py install`.  You should be able to access the extensions in Python Markdown under the namespace `pymdownx.<extension>`.

If you would like to modify the code, you can install it via: `#!bash pip install --editable .`.  This method will allow you to instantly see your changes without reinstalling.  If you want to do this in a virtual machine, you can.

[py_md]: https://pythonhosted.org/Markdown/
[pygments]: http://pygments.org/
