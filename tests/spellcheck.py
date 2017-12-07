"""Spell check with Aspell or Hunspell."""
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
import textwrap
import markdown

PY3 = sys.version_info >= (3, 0)

if PY3:
    ustr = str
    tokenizer = tokenize.tokenize
    PREV_DOC_TOKENS = (tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE, tokenize.ENCODING)
else:
    ustr = unicode  # noqa
    tonkenizer = tokenize.generate_tokens
    PREV_DOC_TOKENS = (tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE)


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


class SpellingLanguage(object):
    """Spelling language."""

    LANGUAGE = ''
    EXTENSIONS = tuple()

    def __init__(self, config):
        """Initialize."""
        pass


class SpellingHTML(SpellingLanguage):
    """Spelling Python."""

    LANGUAGE = 'html'
    EXTENSIONS = ('.html', '.htm')

    def parse_file(self, source_file):
        """Parse HTML file."""

        with codecs.open(source_file, 'r', encoding='utf-8') as f:
            text = f.read()
        return [(text, source_file)]


class SpellingPython(SpellingLanguage):
    """Spelling Python."""

    LANGUAGE = 'python'
    EXTENSIONS = ('.py', '.pyw')

    MODULE = 0
    FUNCTION = 1
    CLASS = 2

    def __init__(self, config):
        """Initialization."""

        self.markdown = config.get('markdown', False)
        self.extensions = []
        self.extension_configs = {}
        for k, v in config.get('markdown_extensions', {}).items():
            self.extensions.append(k)
            if v is not None:
                self.extension_configs[k] = v

    def parse_file(self, source_file):
        """Parse Python file returning docstrings."""

        # comments = []
        docstrings = []
        prev_token_type = tokenize.NEWLINE
        indent = ''
        name = None
        stack = [(source_file, 0, self.MODULE)]
        encoding = 'utf-8'
        if self.markdown:
            md = markdown.Markdown(extensions=self.extensions, extension_configs=self.extension_configs)
        else:
            md = None

        with open(source_file, 'rb') as source:
            for token in tokenizer(source.readline):
                token_type = token[0]
                value = token[1]
                line = ustr(token[2][0])

                if PY3 and token_type == tokenize.ENCODING:
                    encoding = value

                value = token[1] if PY3 else token[1].decode(encoding)
                line = ustr(token[2][0])

                # Track function and class ancestry
                if token_type == tokenize.NAME:
                    if value in ('def', 'class'):
                        name = value
                    elif name:
                        parent = stack[-1][2]
                        prefix = ''
                        if parent != self.MODULE:
                            prefix = '.' if parent == self.CLASS else ', '
                        if name == 'class':
                            stack.append(('%s%s' % (prefix, value), len(indent), self.CLASS))
                        elif name == 'def':
                            stack.append(('%s%s()' % (prefix, value), len(indent), self.FUNCTION))
                        name = None

                # if token_type == tokenize.COMMENT:
                #     # Capture comments
                #     if len(stack) > 1:
                #         loc ="%s(%s): %s" % (stack[0][0], line, ''.join([crumb[0] for crumb in stack[1:]]))
                #     else:
                #         loc = "%s(%s)" % (stack[0][0], line)
                #     comments.append((value, loc))
                if token_type == tokenize.STRING:
                    # Capture docstrings
                    # If previously we captured an INDENT or NEWLINE previously we probably have a docstring.
                    # NL seems to be a different thing.
                    if prev_token_type in PREV_DOC_TOKENS:
                        string = textwrap.dedent(eval(value.strip()))
                        if md:
                            string = md.convert(string)
                        md.reset()
                        loc = "%s(%s): %s" % (stack[0][0], line, ''.join([crumb[0] for crumb in stack[1:]]))
                        docstrings.append((string, loc))

                if token_type == tokenize.INDENT:
                    indent = value
                elif token_type == tokenize.DEDENT:
                    indent = indent[:-4]
                    if len(stack) > 1 and len(indent) <= stack[-1][1]:
                        stack.pop()

                prev_token_type = token_type

        # if self.comments:
        #     docstrings.extend(comments)

        return docstrings


class Spelling(object):
    """Spell check class."""

    DICTIONARY = 'dictionary.dic'
    RE_SELECTOR = re.compile(r'''(\#|\.)?[-\w]+|\*|\[([\w\-:]+)(?:([~^|*$]?=)(\"[^"]+\"|'[^']'|[^'"\[\]]+))?\]''')

    def __init__(self, config_file, plugins=None):
        """Initialize."""

        # General options
        self.dict_bin = os.path.abspath(self.DICTIONARY)
        config = self.read_config(config_file)
        self.documents = config.get('documents', [])
        self.dictionary = config.get('dictionary', [])
        self.plugins = plugins if plugins else []

    def read_config(self, file_name):
        """Read configuration."""

        config = {}
        with codecs.open(file_name, 'r', encoding='utf-8') as f:
            config = yaml_load(f.read())
        return config

    def process_selectors(self, *args):
        """
        Process selectors.

        We do our own selectors as BeautifulSoup4 has some annoying quirks,
        and we don't really need to do nth selectors or siblings or
        descendants etc.
        """

        selectors = [
            Selector('style', None, tuple(), tuple()),
            Selector('script', None, tuple(), tuple()),
        ]

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
        attributes = []

        if not self.skip_tag(tree):
            for attr in self.attributes:
                value = tree.attrs.get(attr, '').strip()
                if value:
                    attributes.append(value)

            for child in tree:
                if isinstance(child, bs4.element.Tag):
                    if child.contents:
                        t, a = (self.html_to_text(child, False))
                        text.extend(t)
                        attributes.extend(a)
                else:
                    string = ustr(child).strip()
                    if string:
                        text.append(ustr(child))

        if root:
            return '<body>%s %s</body>' % (' '.join(text),  ' '.join(attributes))

        return text, attributes

    def check_spelling(self, sources, options, html_advanced_filter, personal_dict):
        """Check spelling."""

        fail = False

        for source in sources:
            if html_advanced_filter:
                html = bs4.BeautifulSoup(source[0], "html5lib")
                text = self.html_to_text(html.html)
            else:
                text = source[0]

            if self.spellchecker == 'hunspell':
                cmd = [
                    'hunspell',
                    '-l',
                    '-i', 'utf-8',
                ]

                if personal_dict:
                    cmd.extend(['-p', personal_dict])

            else:
                cmd = [
                    'aspell',
                    'list',
                    '--encoding=utf-8'
                ]

                if personal_dict:
                    cmd.extend(['--add-extra-dicts', personal_dict])

            for k, v in options.items():
                key = ('-%s' if len(k) == 1 else '--%s') % k
                if isinstance(v, bool) and v is True:
                    cmd.append(key)
                elif isinstance(v, ustr):
                    cmd.extend([key, v])
                elif isinstance(v, int):
                    cmd.extend([key, ustr(v)])
                elif isinstance(v, list):
                    for value in v:
                        cmd.extend([key, ustr(value)])

            wordlist = console(cmd, input_text=text.encode('utf-8'))
            words = [w for w in sorted(set(wordlist.split('\n'))) if w]

            if words:
                fail = True
                print('Misspelled words:\n%s' % source[1])
                print('-' * 80)
                for word in words:
                    print(word)
                print('-' * 80)
                print('\n')
        return fail

    def compile_dictionary(self, lang, wordlists, output):
        """Compile user dictionary."""

        output_location = os.path.dirname(output)
        if not os.path.exists(output_location):
            os.makedirs(output_location)
        if os.path.exists(output):
            os.remove(output)

        print("Compiling Dictionary...")
        # Read word lists and create a unique set of words
        words = set()
        for wordlist in wordlists:
            with open(wordlist, 'rb') as src:
                for word in src.read().split(b'\n'):
                    words.add(word.replace(b'\r', b''))

        if self.spellchecker == 'hunspell':
            # Sort and create wordlist
            with open(self.dict_bin, 'wb') as dest:
                dest.write(b'\n'.join(sorted(words)) + b'\n')
        else:
            # Compile wordlist against language
            console(
                [
                    'aspell',
                    '--lang', lang,
                    '--encoding=utf-8',
                    'create',
                    'master', output
                ],
                input_text=b'\n'.join(sorted(words)) + b'\n'
            )

    def walk_src(self, targets, plugin):
        """Walk source and parse files."""

        extensions = plugin.EXTENSIONS
        for target in targets:
            if os.path.isdir(target):
                for base, dirs, files in os.walk(target):
                    for f in files:
                        if f.lower().endswith(tuple(extensions)):
                            yield plugin.parse_file(os.path.join(base, f))
            elif target.lower().endswith(tuple(extensions)):
                yield plugin.parse_file(target)

    def check(self):
        """Walk source and initiate spell check."""

        fail = False
        for documents in self.documents:
            lang = documents['language']
            for plugin in self.plugins:
                if lang == plugin.LANGUAGE:
                    # Create instance of plugin
                    plug = plugin(documents.get('options', {}))

                    # Setup spell checker
                    self.spellchecker = documents.get('spell_checker', 'aspell')
                    if self.spellchecker == 'hunspell':
                        options = documents.get('hunspell', {})
                    else:
                        options = documents.get('aspell', {})

                    # Load and combine dictionaries
                    dictionary_options = documents.get('dictionary', {})
                    output = os.path.abspath(dictionary_options.get('output', self.dict_bin))
                    lang = dictionary_options.get('lang', 'en' if self.spellchecker == 'aspell' else 'en_US')
                    wordlists = dictionary_options.get('wordlists', [])
                    if lang and wordlists:
                        self.compile_dictionary(lang, dictionary_options.get('wordlists', []), output)
                    else:
                        output = None

                    # Setup HTML options
                    html_options = documents.get('html', {})
                    html_advanced_filter = html_options.get('advanced_filter', False)
                    self.attributes = set(html_options.get('attributes', []))
                    self.selectors = self.process_selectors(*html_options.get('ignores', []))

                    # Perform spell check
                    print('Spell Checking %s...' % documents.get('name', ''))
                    for sources in self.walk_src(documents.get('src', []), plug):
                        if self.check_spelling(sources, options, html_advanced_filter, output):
                            fail = True

                    break
        return fail


def main():
    """Main."""

    fail = False
    spelling = Spelling('.spelling.yml', [SpellingHTML, SpellingPython])
    if spelling.check():
        fail = True
    return fail


if __name__ == "__main__":
    sys.exit(main())
