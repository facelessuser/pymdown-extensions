"""Spell check with aspell."""
from __future__ import unicode_literals
import subprocess
import os
import sys
import codecs
import bs4
import re
from collections import namedtuple

PY3 = sys.version_info >= (3, 0)

USER_DICT = '.dictionary'
BUILD_DIR = os.path.join('.', 'build', 'docs')
MKDOCS_CFG = 'mkdocs.yml'
COMPILED_DICT = os.path.join(BUILD_DIR, 'dictionary.bin')
MKDOCS_SPELL = os.path.join(BUILD_DIR, MKDOCS_CFG)
MKDOCS_BUILD = os.path.join(BUILD_DIR, 'site')
RE_SELECTOR = re.compile(r'(\#|\.)?[-\w]+')


class IgnoreRule (namedtuple('IgnoreRule', ['tag', 'id', 'classes'])):
    """Ignore rule."""


def console(cmd, input_file=None, input_text=None):
    """Call with arguments."""

    returncode = None
    output = None

    if sys.platform.startswith('win'):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(
            cmd,
            startupinfo=startupinfo,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            shell=False
        )
    else:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            shell=False
        )

    if input_file is not None:
        with open(input_file, 'rb') as f:
            process.stdin.write(f.read())
    if input_text is not None:
        process.stdin.write(input_text)
    output = process.communicate()
    returncode = process.returncode

    assert returncode == 0, "Runtime Error: %s" % (
        output[0].rstrip().decode('utf-8') if PY3 else output[0]
    )

    return output[0].decode('utf-8') if PY3 else output[0]


def build_docs():
    """Build docs with MkDocs."""
    print('Building Docs...')
    print(
        console(
            [
                sys.executable,
                '-m', 'mkdocs', 'build', '--clean',
                '-d', MKDOCS_BUILD
            ]
        )
    )


def compile_dictionary():
    """Compile user dictionary."""
    if os.path.exists(COMPILED_DICT):
        os.remove(COMPILED_DICT)
    print("Compiling Custom Dictionary...")
    print(
        console(
            [
                'aspell',
                '--lang=en',
                '--encoding=utf-8',
                'create',
                'master',
                COMPILED_DICT
            ],
            input_file=USER_DICT
        )
    )


def ignore_rules(*args):
    """
    Process ignore rules.

    Split ignore selector string into tag, id, and classes.
    """

    ignores = []

    for arg in args:
        selector = arg.lower()
        tag = None
        tag_id = None
        classes = set()

        for m in RE_SELECTOR.finditer(selector):
            selector = m.group(0)
            if selector.startswith('.'):
                classes.add(selector[1:])
            elif selector.startswith('#') and tag_id is None:
                tag_id = selector[1:]
            elif tag is None:
                tag = selector
            else:
                raise ValueError('Bad selector!')

        if tag or tag_id or classes:
            ignores.append(IgnoreRule(tag, tag_id, tuple(classes)))

    return ignores


def skip_tag(el, ignore):
    """Determine if tag should be skipped."""

    skip = False
    for rule in ignore:
        if rule.tag and el.name.lower() != rule.tag:
            continue
        if rule.id and rule.id != el.attrs.get('id', '').lower():
            continue
        if rule.classes:
            current_classes = [c.lower() for c in el.attrs.get('class', [])]
            found = True
            for c in rule.classes:
                if c not in current_classes:
                    found = False
                    break
            if not found:
                continue
        skip = True
        break
    return skip


def html_to_text(tree, ignore, attributes, root=True):
    """
    Parse the HTML creating a buffer with each tags content.

    Skip any selectors specified and include attributes if specified.
    Ignored tags will not have their attributes scanned either.
    """

    text = []

    if not skip_tag(tree, ignore):
        for attr in attributes:
            value = tree.attrs.get(attr)
            if value:
                text.append(value)

        for child in tree:
            if isinstance(child, bs4.element.Tag):
                if child.contents:
                    text.extend(html_to_text(child, ignore, attributes, False))
            else:
                text.append(str(child))

    return ' '.join(text) if root else text


def check_spelling():
    """Check spelling."""
    print('Spell Checking...')

    fail = False
    ignores = ignore_rules(
        'code',
        'pre',
        'script',
        'style',
        'a.magiclink-compare',
        'a.magiclink-commit',
        '.MathJax_Preview'
    )
    attrs = {'title', 'alt'}

    for base, dirs, files in os.walk(MKDOCS_BUILD):
        # Remove child folders based on exclude rules
        for f in files:
            if f.endswith('.html'):
                file_name = os.path.join(base, f)
                with codecs.open(file_name, 'r', encoding='utf-8') as file_obj:
                    html = bs4.BeautifulSoup(file_obj.read(), "html5lib")
                    text = html_to_text(
                        html.html,
                        ignores,
                        attrs
                    )

                wordlist = console(
                    [
                        'aspell',
                        'list',
                        '--lang=en',
                        '--mode=url',
                        '--encoding=utf-8',
                        '--extra-dicts=%s' % COMPILED_DICT
                    ],
                    input_text=text.encode('utf-8')
                )

                words = [w for w in sorted(set(wordlist.split('\n'))) if w]

                if words:
                    fail = True
                    print('Misspelled words in %s' % file_name)
                    print('-' * 80)
                    for word in words:
                        print(word)
                    print('-' * 80)
                    print('\n')
    return fail


def main():
    """Main."""
    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)
    build_docs()
    compile_dictionary()
    return check_spelling()


if __name__ == "__main__":
    sys.exit(main())
