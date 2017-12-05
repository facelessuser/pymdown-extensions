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
import tokenize

PY3 = sys.version_info >= (3, 0)


def yaml_load(source, loader=yaml.Loader):
    """
    Wrap PyYaml's loader so we can extend it to suit our needs.

    Load all strings as Unicode: http://stackoverflow.com/a/2967461/3609487.
    """

    def construct_yaml_str(self, node):
        """Override the default string handling function to always return Unicode objects."""
        return self.construct_scalar(node)

    class Loader(loader):
        """Define a custom loader to leave the global loader unaltered."""

    # Attach our Unicode constructor to our custom loader ensuring all strings
    # will be Unicode on translation.
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


class Selector(namedtuple('IgnoreRule', ['tag', 'id', 'classes', 'attributes'])):
    """Ignore rule."""

class SelectorAttribute(namedtuple('AttrRule', ['attribute', 'pattern'])):
    """Selector attribute rule."""


class SpellingPython(object):

    DICTIONARY = 'dictionary.bin'

    def __init__(self, config_file):
        """Initialize."""

        config = read_config(config_file).get('python')
        self.options = config.get('options', {})
        self.sources = config.get('src', [])
        self.dictionary = ('\n'.join(config.get('dictionary', []))).encode('utf-8')
        self.dict_bin = os.path.abspath(self.DICTIONARY)
        self.comments = self.options.get('comments', False)

    def source_to_text(self, source):
        """Get docstrings and comments."""

        comments = []
        prev_token_type = tokenize.NEWLINE
        indent = ''
        for token in tokenize.generate_tokens(source.readline):
            token_type = token[0]
            value = token[1]

            if token_type == tokenize.COMMENT:
                # Capture comments
                if self.comments:
                    comments.append(value)
            elif token_type == tokenize.STRING:
                # Capture docstrings
                # If previously we captured an INDENT or NEWLINE previously we probably have a docstring.
                # NL seems to be a different thing.
                if prev_token_type in (tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE):
                    comments.append(value)

            prev_token_type = token_type

        return '\n'.join(comments)

    def check_spelling(self, source_file):
        """Check spelling."""

        fail = False
        with codecs.open(source_file, 'r', encoding='utf-8') as file_obj:
            text = self.source_to_text(file_obj)

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
            print('Misspelled words in %s' % source_file)
            print('-' * 80)
            for word in words:
                print(word)
            print('-' * 80)
            print('\n')
        return fail


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

    def check(self):
        """Walk source and initiate spell check."""

        self.compile_dictionaries()

        print('Spell Checking...')
        fail = False
        for source in self.sources:
            if os.path.isdir(source):
                for base, dirs, files in os.walk(source):
                    for f in files:
                        if f.lower().endswith('.py'):
                            file_name = os.path.join(base, f)
                            if self.check_spelling(file_name):
                                fail = True
            elif source.lower().endswith('.py'):
                if self.check_spelling(source):
                    fail = True
        return fail


class SpellingHtml(object):
    """Spell check object."""

    DICTIONARY = 'dictionary.bin'
    RE_SELECTOR = re.compile(r'''(\#|\.)?[-\w]+|\*|\[([\w\-:]+)(?:([~^|*$]?=)(\"[^"]+\"|'[^']'|[^'"\[\]]+))?\]''')

    def __init__(self, config_file):
        """Initialize."""

        config = read_config(config_file).get('html', {})
        self.docs = config.get('src', [])
        self.dictionary = ('\n'.join(config.get('dictionary', []))).encode('utf-8')
        self.attributes = set(config.get('attributes', []))
        self.selectors = self.process_selectors(*config.get('ignores', []))
        self.dict_bin = os.path.abspath(self.DICTIONARY)

    def process_selectors(self, *args):
        """
        Process selectors.

        We do our own selectors as BeautifulSoup4 has some annoying quirks,
        and we don't really need to do nth selectors or siblings or
        decendents etc.
        """

        selectors = []

        for selector in args:
            tag = None
            tag_id = None
            classes = set()
            attributes = []

            for m in self.RE_SELECTOR.finditer(selector):
                if m.group(2):
                    attr = m.group(2).lower()
                    op = m.group(3)
                    if op:
                        value = m.group(4)[1:-1] if m.group(4).startswith('"') else m.group(4)
                    else:
                        value = None
                    if not op:
                        # Attribute name
                        pattern = None
                    elif op.startswith('^'):
                        # Value start with
                        pattern = re.compile(r'^%s.*' % re.escape(value))
                    elif op.startswith('$'):
                        # Value ends with
                        pattern = re.compile(r'.*?%s$' % re.escape(value))
                    elif op.startswith('*'):
                        # Value contains
                        pattern = re.compile(r'.*?%s.*' % re.escape(value))
                    elif op.startswith('~'):
                        # Value contains word within space separated list
                        pattern = re.compile(r'.*?(?:(?<=^)|(?<= ))%s(?=(?:[ ]|$)).*' % re.escape(value))
                    elif op.startswith('|'):
                        # Value starts with word in dash separated list
                        pattern = re.compile(r'^%s(?=-).*' % re.escape(value))
                    else:
                        # Value matches
                        pattern = re.compile(r'^%s$' % re.escape(value))
                    attributes.append(SelectorAttribute(attr, pattern))
                else:
                    selector = m.group(0).lower()
                    if selector.startswith('.'):
                        classes.add(selector[1:].lower())
                    elif selector.startswith('#') and tag_id is None:
                        tag_id = selector[1:]
                    elif tag is None:
                        tag = selector
                    else:
                        raise ValueError('Bad selector!')

            if tag or tag_id or classes:
                selectors.append(Selector(tag, tag_id, tuple(classes), tuple(attributes)))

        return selectors

    def skip_tag(self, el):
        """Determine if tag should be skipped."""

        skip = False
        for selector in self.selectors:
            if selector.tag and selector.tag not in (el.name.lower(), '*'):
                continue
            if selector.id and selector.id != el.attrs.get('id', '').lower():
                continue
            if selector.classes:
                current_classes = [c.lower() for c in el.attrs.get('class', [])]
                found = True
                for c in selector.classes:
                    if c not in current_classes:
                        found = False
                        break
                if not found:
                    continue
            if selector.attributes:
                found = True
                for a in selector.attributes:
                    value = el.attrs.get(a.attribute)
                    if isinstance(value, list):
                        value = ' '.join(value)
                    if not value:
                        found = False
                        break
                    elif a.pattern is None:
                        continue
                    elif a.pattern.match(value) is None:
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

    def check(self):
        """Walk documents and initiate spell check."""

        self.compile_dictionaries()

        print('Spell Checking...')
        fail = False
        for doc in self.docs:
            if os.path.isdir(doc):
                for base, dirs, files in os.walk(doc):
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

    fail = False
    spelling = SpellingHtml('.spelling.yml')
    if spelling.check():
        fail = True
    spelling = SpellingPython('.spelling.yml')
    if spelling.check():
        fail = True
    return fail


if __name__ == "__main__":
    sys.exit(main())
