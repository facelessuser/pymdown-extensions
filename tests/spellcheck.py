"""Spell check with aspell."""
from __future__ import unicode_literals
import subprocess
import os
import sys
import codecs
import bs4
import yaml
import re
from collections import namedtuple

PY3 = sys.version_info >= (3, 0)


def yaml_load(source, loader=yaml.Loader):
    """
    Wrap PyYaml's loader so we can extend it to suit our needs.

    Load all strings as unicode: http://stackoverflow.com/a/2967461/3609487.
    """

    def construct_yaml_str(self, node):
        """Override the default string handling function to always return Unicode objects."""
        return self.construct_scalar(node)

    class Loader(loader):
        """Define a custom loader to leave the global loader unaltered."""

    # Attach our unicode constructor to our custom loader ensuring all strings
    # will be unicode on translation.
    Loader.add_constructor('tag:yaml.org,2002:str', construct_yaml_str)

    return yaml.load(source, Loader)


def read_config(file_name):
    """Read configuration."""

    config = {}
    with codecs.open(file_name, 'r', encoding='utf-8') as f:
        config = yaml_load(f.read())
    return config


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


class IgnoreRule (namedtuple('IgnoreRule', ['tag', 'id', 'classes'])):
    """Ignore rule."""


class Spelling(object):
    """Spell check object."""

    DICTIONARY = 'dictionary.bin'
    RE_SELECTOR = re.compile(r'(\#|\.)?[-\w]+')

    def __init__(self, config_file):
        """Initialize."""

        config = read_config(config_file)
        self.docs = config.get('docs', [])
        self.dictionary = ('\n'.join(config.get('dictionary', []))).encode('utf-8')
        self.attributes = set(config.get('attributes', []))
        self.ignores = self.ignore_rules(*config.get('ignores', []))
        self.dict_bin = os.path.abspath(self.DICTIONARY)

    def ignore_rules(self, *args):
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

            for m in self.RE_SELECTOR.finditer(selector):
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

    def compile_dictionaries(self):
        """Compile user dictionary."""

        if os.path.exists(self.dict_bin):
            os.remove(self.dict_bin)
        print("Compiling Dictionary...")
        print(
            console(
                [
                    'aspell',
                    '--lang=en',
                    '--encoding=utf-8',
                    'create',
                    'master',
                    os.path.abspath(self.dict_bin)
                ],
                input_text=self.dictionary
            )
        )

    def skip_tag(self, el):
        """Determine if tag should be skipped."""

        skip = False
        for rule in self.ignores:
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

    def html_to_text(self, tree, root=True):
        """
        Parse the HTML creating a buffer with each tags content.

        Skip any selectors specified and include attributes if specified.
        Ignored tags will not have their attributes scanned either.
        """

        text = []

        if not self.skip_tag(tree):
            for attr in self.attributes:
                value = tree.attrs.get(attr)
                if value:
                    text.append(value)

            for child in tree:
                if isinstance(child, bs4.element.Tag):
                    if child.contents:
                        text.extend(self.html_to_text(child, False))
                else:
                    text.append(str(child))

        return ' '.join(text) if root else text

    def check_spelling(self, html_file):
        """Check spelling."""

        fail = False
        with codecs.open(html_file, 'r', encoding='utf-8') as file_obj:
            html = bs4.BeautifulSoup(file_obj.read(), "html5lib")
            text = self.html_to_text(html.html)

        wordlist = console(
            [
                'aspell',
                'list',
                '--lang=en',
                '--mode=url',
                '--encoding=utf-8',
                '--extra-dicts',
                self.dict_bin
            ],
            input_text=text.encode('utf-8')
        )
        words = [w for w in sorted(set(wordlist.split('\n'))) if w]

        if words:
            fail = True
            print('Misspelled words in %s' % html_file)
            print('-' * 80)
            for word in words:
                print(word)
            print('-' * 80)
            print('\n')
        return fail

    def check(self):
        """Walk documents and initiate spell check."""

        self.compile_dictionaries()

        print('Spell Checking...')
        fail = False
        for doc in self.docs:
            if os.path.isdir(doc):
                for base, dirs, files in os.walk(doc):
                    # Remove child folders based on exclude rules
                    for f in files:
                        if f.lower().endswith('.html'):
                            file_name = os.path.join(base, f)
                            if self.check_spelling(file_name):
                                fail = True
            elif doc.lower().endswith('.html'):
                if self.check_spelling(doc):
                    fail = True
        return fail


def main():
    """Main."""

    spelling = Spelling('.spelling.yml')
    return spelling.check()


if __name__ == "__main__":
    sys.exit(main())
