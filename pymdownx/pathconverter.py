"""
Path Converter.

pymdownx.pathconverter
An extension for Python Markdown.

An extension to covert tag paths to relative or absolute:

Given an absolute base and a target relative path, this extension searches for file
references that are relative and converts them to a path relative
to the base path.

-or-

Given an absolute base path, this extension searches for file
references that are relative and converts them to absolute paths.

MIT license.

Copyright (c) 2014 - 2017 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from markdown import Extension
from markdown.postprocessors import Postprocessor
from . import util
import os
import re
from urllib.parse import urlunparse

RE_TAG_HTML = r'''(?xusi)
    (?:
        (?P<avoid>
            (?P<script_open><\s*(?P<script_name>script|style))(?=[\s\/>])
            (?:
                (?P<script_attr>(?:\s+[\w\-:]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s"'`=<>]+))?)*)
                (?:
                    (?P<script_self_close>\s*\/>)|
                    (?P<script_close>\s*>).*?(?:</\s*(?P=script_name)\s*>|\Z)
                )|
                [^>]*\/>|
                [^>]*>.*?(?:</\s*(?P=script_name)\s*>|\Z)
            ) |
            <!--[\s\S]*?(?:-->|\Z)
        )|
        (?P<open><\s*(?P<tag>(?:%s)))
        (?P<attr>(?:\s+[\w\-:]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s"'`=<>]+))?)*)
        (?P<close>\s*(?:\/?)>)
    )
    '''

# Walk the attributes in order so that only real `href`/`src` attributes are converted
# and never something that merely looks like one inside another attribute's value.
RE_TAG_LINK_ATTR = re.compile(
    r'''(?xusi)
    (?:
        (?P<attr>
            (?P<name>\s+(?:href|src)\s*=\s*)
            (?P<path>"[^"]*"|'[^']*')
        )|
        \s+[\w\-:]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s"'`=<>]+))?
    )
    '''
)


def repl_relative(m, base_path, relative_path):
    """Replace path with relative path."""

    link = m.group(0)
    try:
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = util.parse_url(m.group('path')[1:-1])

        if not is_url:
            # Get the absolute path of the file or return
            # if we can't resolve the path
            path = util.url2path(path)
            if (not is_absolute):
                # Convert current relative path to absolute
                path = os.path.relpath(
                    os.path.normpath(os.path.join(base_path, path)),
                    os.path.normpath(relative_path)
                )
                # Convert the path, URL encode it, and format it as a link
                path = util.path2url(path)
                link = '{}"{}"'.format(
                    m.group('name'),
                    urlunparse((scheme, netloc, path, params, query, fragment))
                )
    except Exception:  # pragma: no cover
        # Parsing crashed and burned; no need to continue.
        pass

    return link


def repl_absolute(m, base_path, file_scheme):
    """Replace path with absolute path."""

    link = m.group(0)
    try:
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = util.parse_url(m.group('path')[1:-1])

        if (not is_absolute and not is_url):
            path = util.url2path(path)
            path = os.path.normpath(os.path.join(base_path, path))
            path = util.path2url(path)
            if file_scheme:
                if not path.startswith('/'):
                    path = '/' + path
                link = '{}"{}"'.format(
                    m.group('name'),
                    urlunparse(("file", netloc, path, params, query, fragment))
                )
            else:
                start = '/' if not path.startswith('/') else ''
                link = '{}"{}{}"'.format(
                    m.group('name'),
                    start,
                    urlunparse((scheme, netloc, path, params, query, fragment))
                )
    except Exception:  # pragma: no cover
        # Parsing crashed and burned; no need to continue.
        pass

    return link


def repl(m, base_path, rel_path=None, file_scheme=None, tags=()):
    """Replace."""

    if m.group('avoid'):
        tag = m.group('avoid')
        # Content of `script` and `style` tags and comments is not parsed, but the attributes
        # of the `script` or `style` tag itself are if they are one of the specified tags.
        if m.group('script_attr') is not None and m.group('script_name').lower() in tags:
            close = m.group('script_self_close') or m.group('script_close')
            start = len(m.group('script_open')) + len(m.group('script_attr')) + len(close)
            tag = (
                m.group('script_open') +
                convert_attrs(m.group('script_attr'), base_path, rel_path, file_scheme) +
                close +
                tag[start:]
            )
    else:
        tag = m.group('open')
        tag += convert_attrs(m.group('attr'), base_path, rel_path, file_scheme)
        tag += m.group('close')
    return tag


def convert_attrs(attrs, base_path, rel_path=None, file_scheme=None):
    """Convert the `href` and `src` attributes."""

    if rel_path is None:
        return RE_TAG_LINK_ATTR.sub(
            lambda m2: repl_absolute(m2, base_path, file_scheme) if m2.group('attr') else m2.group(0),
            attrs
        )
    return RE_TAG_LINK_ATTR.sub(
        lambda m2: repl_relative(m2, base_path, rel_path) if m2.group('attr') else m2.group(0),
        attrs
    )


class PathConverterPostprocessor(Postprocessor):
    """Post process to find tag lings to convert."""

    def run(self, text):
        """Find and convert paths."""

        basepath = self.config['base_path']
        relativepath = self.config['relative_path']
        absolute = bool(self.config['absolute'])
        filescheme = bool(self.config['file_scheme'])
        tag_names = self.config['tags'].split()
        tags = re.compile(RE_TAG_HTML % '|'.join(tag_names))
        tag_set = frozenset(t.lower() for t in tag_names)
        if not absolute and basepath and relativepath:
            text = tags.sub(lambda m: repl(m, basepath, rel_path=relativepath, tags=tag_set), text)
        elif absolute and basepath:
            text = tags.sub(lambda m: repl(m, basepath, file_scheme=filescheme, tags=tag_set), text)
        return text


class PathConverterExtension(Extension):
    """PathConverter extension."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'base_path': ["", "Base path used to find files - Default: \"\""],
            'relative_path': ["", "Path that files will be relative to (not needed if using absolute) - Default: \"\""],
            'absolute': [False, "Paths are absolute by default; disable for relative - Default: False"],
            'tags': ["img script a link", "tags to convert src and/or href in - Default: 'img scripts a link'"],
            'file_scheme': [False, "Use file:// scheme for absolute paths - Default: False"],
        }

        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Add post processor to Markdown instance."""

        rel_path = PathConverterPostprocessor(md)
        rel_path.config = self.getConfigs()
        md.postprocessors.register(rel_path, "path-converter", 2)
        md.registerExtension(self)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return PathConverterExtension(*args, **kwargs)
