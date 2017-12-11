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
import fnmatch
import contextlib
import mmap
import functools
import random
import string

__version__ = '0.1.0'

PY3 = sys.version_info >= (3, 0)

if PY3:
    ustr = str
    tokenizer = tokenize.tokenize
    PREV_DOC_TOKENS = (tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE, tokenize.ENCODING)
else:
    ustr = unicode  # noqa
    tokenizer = tokenize.generate_tokens
    PREV_DOC_TOKENS = (tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE)


###################
# Helper Functions
###################
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


def random_name_gen(size=6):
    """Generate a random python attribute name."""

    return ''.join(
        [random.choice(string.ascii_uppercase)] +
        [random.choice(string.ascii_uppercase + string.digits) for i in range(size - 1)]
    ) if size > 0 else ''


###################
# Encoding Detect
###################
class DetectEncoding(object):
    """
    Simple detect encoding class.

    Attempts to detect UTF encoding via BOMs.
    Override `special_encode_check` to add additional check logic.
    """

    MAX_GUESS_SIZE = 31457280
    RE_UTF_BOM = re.compile(
        b'^(?:(' +
        codecs.BOM_UTF8 +
        b')[\x00-\xFF]{,2}|(' +
        codecs.BOM_UTF32_BE +
        b')|(' +
        codecs.BOM_UTF32_LE +
        b')|(' +
        codecs.BOM_UTF16_BE +
        b')|(' +
        codecs.BOM_UTF16_LE +
        b'))'
    )

    def _is_very_large(self, size):
        """Check if content is very large."""

        return size >= self.MAX_GUESS_SIZE

    def _verify_encode(self, file_obj, encoding, blocks=1, chunk_size=4096):
        """
        Iterate through the file chunking the data into blocks and decoding them.

        Here we can adjust how the size of blocks and how many to validate. By default,
        we are just going to check the first 4K block.
        """

        good = True
        file_obj.seek(0)
        binary_chunks = iter(functools.partial(file_obj.read, chunk_size), b"")
        try:
            for unicode_chunk in codecs.iterdecode(binary_chunks, encoding):  # noqa
                if blocks:
                    blocks -= 1
                else:
                    break
        except Exception:
            good = False
        return good

    def _has_bom(self, content):
        """Check for UTF8, UTF16, and UTF32 BOMs."""

        encoding = None
        m = self.RE_UTF_BOM.match(content)
        if m is not None:
            if m.group(1):
                encoding = 'utf-8-sig'
            elif m.group(2):
                encoding = 'utf-32'
            elif m.group(3):
                encoding = 'utf-32'
            elif m.group(4):
                encoding = 'utf-16'
            elif m.group(5):
                encoding = 'utf-16'
        return encoding

    def utf_strip_bom(self, encoding):
        """Return an encoding that will ignore the BOM."""

        if encoding == 'utf-8':
            encoding = 'utf-8-sig'
        elif encoding.startswith('utf-16'):
            encoding = 'utf-16'
        elif encoding.startswith('utf-32'):
            encoding = 'utf-32'
        return encoding

    def special_encode_check(self, content, ext):
        """Special encode check."""

        return None

    def _detect_encoding(self, f, ext, file_size):
        """Guess by checking BOM, and checking `_special_encode_check`, and using memory map."""

        encoding = None
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
            # Check for boms
            encoding = self._has_bom(m.read(4))
            m.seek(0)
            # Check file extensions
            if encoding is None:
                encoding = self.utf_strip_bom(self.special_encode_check(m.read(1024), ext))

        return encoding

    def guess(self, filename, verify=True, verify_blocks=1, verify_block_size=4096):
        """Guess the encoding and decode the content of the file."""

        encoding = None

        try:
            ext = os.path.splitext(filename)[1].lower()
            file_size = os.path.getsize(filename)
            # If the file is really big, lets just call it binary.
            # We dont' have time to let Python chug through a massive file.
            if not self._is_very_large(file_size):
                with open(filename, "rb") as f:
                    if file_size == 0:
                        encoding = 'ascii'
                    else:
                        encoding = self._detect_encoding(f, ext, file_size)

                    if verify and encoding and encoding != 'bin':
                        if not self.verify_encode(f, encoding.encode, verify_blocks, verify_block_size):
                            encoding = 'bin'
            else:
                encoding = 'bin'
        except Exception as e:  # pragma: no cover
            encoding = 'bin'
            pass

        return encoding


class DetectEncodingHTML(DetectEncoding):
    """Detect HTML encoding."""

    RE_HTML_ENCODE = re.compile(
        br'''(?x)
        <meta(?!\s*(?:name|value)\s*=)(?:[^>]*?content\s*=[\s"']*)?(?:[^>]*?)[\s"';]*charset\s*=[\s"']*([^\s"'/>]*)
        '''
    )

    def special_encode_check(self, content, ext):
        """Special HTML encoding check."""

        encode = None
        m = self.RE_HTML_ENCODE.search(content)
        if m:
            enc = m.group(1).decode('ascii')
            try:
                codecs.getencoder(enc)
                encode = enc
            except LookupError:
                pass
        else:
            print('No match')
        return encode


class DetectEncodingPython(DetectEncoding):
    """Detect Python encoding."""

    RE_PY_ENCODE = re.compile(
        br'^[^\r\n]*?coding[:=]\s*([-\w.]+)|[^\r\n]*?\r?\n[^\r\n]*?coding[:=]\s*([-\w.]+)'
    )

    def special_encode_check(self, content, ext):
        """Special Python encoding check."""

        encode = None

        m = self.RE_PY_ENCODE.match(content)
        if m:
            if m.group(1):
                enc = m.group(1).decode('ascii')
            elif m.group(2):
                enc = m.group(2).decode('ascii')
            try:
                codecs.getencoder(enc)
                encode = enc
            except LookupError:
                pass
        if encode is None:
            encode = 'ascii'
        return encode


###################
# Spelling Handlers
###################
class SpellingGeneric(object):
    """Spelling language."""

    LANGUAGE = 'text'
    EXTENSIONS = tuple('*',)
    DECODER = DetectEncoding

    def __init__(self, config, encoding='ascii'):
        """Initialize."""

        self.default_encoding = encoding

    def detect_encoding(self, source_file):
        """Detect encoding."""

        detect = self.DECODER()
        encoding = detect.guess(source_file, verify=False)
        # If we didn't explicitly detect an encoding, assume default.
        if not encoding:
            encoding = self.default_encoding

        return self.default_encoding if not encoding else encoding

    def parse_file(self, source_file):
        """Parse HTML file."""

        encoding = self.detect_encoding(source_file)

        if encoding != 'bin':
            with codecs.open(source_file, 'r', encoding=encoding) as f:
                text = f.read()
        else:
            text = ''
        return [(text, source_file, encoding)]


class SpellingHTML(SpellingGeneric):
    """Spelling Python."""

    LANGUAGE = 'html'
    EXTENSIONS = ('*.html', '*.htm')
    DECODER = DetectEncodingHTML

    def parse_file(self, source_file):
        """Parse HTML file."""

        encoding = self.detect_encoding(source_file)
        try:
            with codecs.open(source_file, 'r', encoding=encoding) as f:
                text = f.read()
            html = [(text, source_file, encoding)]
        except Exception as e:
            html = [('', source_file, 'bin')]
        return html


class SpellingPython(SpellingGeneric):
    """Spelling Python."""

    LANGUAGE = 'python'
    EXTENSIONS = ('*.py', '*.pyw')
    DECODER = DetectEncodingPython

    MODULE = 0
    FUNCTION = 1
    CLASS = 2

    def __init__(self, config, encoding='ascii'):
        """Initialization."""

        self.markdown = config.get('markdown', False)
        self.extensions = []
        self.extension_configs = {}
        for item in config.get('markdown_extensions', []):
            if isinstance(item, ustr):
                self.extensions.append(item)
            else:
                k, v = list(item.items())[0]
                self.extensions.append(k)
                if v is not None:
                    self.extension_configs[k] = v
        super(SpellingPython, self).__init__(config, encoding)

    def detect_encoding(self, source_file):
        """Get default encoding."""

        if PY3:
            # In Py3, the tokenizer will tell us what the encoding is.
            encoding = 'ascii'
        else:
            encoding = self.DECODER().guess(source_file, verify=False)
        return encoding

    def parse_docstrings(self, source_file):
        """Retrieve the Python docstrings."""

        # comments = []
        docstrings = []
        prev_token_type = tokenize.NEWLINE
        indent = ''
        name = None
        stack = [(source_file, 0, self.MODULE)]

        encoding = self.detect_encoding(source_file)

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
                        docstrings.append((string, loc, encoding))

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

    def parse_file(self, source_file):
        """Parse Python file returning docstrings."""

        try:
            docstrings = self.parse_docstrings(source_file)
        except Exception as e:
            print(e)
            docstrings = [('', source_file, 'bin')]
        return docstrings


###################
# Selector Objects
###################
class Selector(namedtuple('IgnoreRule', ['tag', 'id', 'classes', 'attributes'])):
    """Ignore rule."""


class SelectorAttribute(namedtuple('AttrRule', ['attribute', 'pattern'])):
    """Selector attribute rule."""


###################
# Spell Checker
###################
class Spelling(object):
    """Spell check class."""

    DICTIONARY = 'dictionary.dic'
    RE_SELECTOR = re.compile(r'''(\#|\.)?[-\w]+|\*|\[([\w\-:]+)(?:([~^|*$]?=)(\"[^"]+\"|'[^']'|[^'"\[\]]+))?\]''')

    def __init__(self, config, plugins=None, verbose=False):
        """Initialize."""

        # General options
        self.verbose = verbose
        self.dict_bin = os.path.abspath(self.DICTIONARY)
        self.documents = config.get('documents', [])
        self.dictionary = config.get('dictionary', [])
        self.plugins = plugins if plugins else []

    def normalize_utf(self, encoding):
        """Normalize UTF encoding."""

        if encoding == 'utf-8-sig':
            encoding = 'utf-8'
        if encoding.startswith('utf-16'):
            encoding = 'utf-16'
        elif encoding.startswith('utf-32'):
            encoding = 'utf-32'
        return encoding

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
            return '<body>%s %s</body>' % (' '.join(text), ' '.join(attributes))

        return text, attributes

    def apply_delimiters(self, text):
        """Apply context delimiters."""

        new_text = []
        index = 0
        last = 0
        end = len(text)
        while index < end:
            m = self.escapes.match(text, pos=index)
            if m:
                index = m.end(0)
                continue
            handled = False
            for delimiter in self.delimiters:
                m = delimiter[0].match(text, pos=index)
                if m:
                    if self.context_visible_first is True:
                        new_text.append(text[last:m.start(0)])
                    else:
                        new_text.append(m.group(delimiter[1]))
                    index = m.end(0)
                    last = index
                    handled = True
                    break
            if handled:
                continue
            index += 1
        if last < end and self.context_visible_first is True:
            new_text.append(text[last:end])
        return ' '.join(new_text)

    def check_spelling(self, sources, options, personal_dict):
        """Check spelling."""

        fail = False

        for source in sources:
            if source[2] == 'bin':
                print('ERROR: Could not read %s' % source[1])
                continue
            if self.verbose:
                print('CHECK: %s' % source[1])
            if self.attributes or self.selectors:
                html = bs4.BeautifulSoup(source[0], "html5lib")
                text = self.html_to_text(html.html)
            else:
                text = source[0]

            if self.delimiters:
                text = self.apply_delimiters(text)

            if self.spellchecker == 'hunspell':
                cmd = [
                    'hunspell',
                    '-l',
                    '-i', self.normalize_utf(source[2]),
                ]

                if personal_dict:
                    cmd.extend(['-p', personal_dict])

                allowed = {
                    'check-apostrophe', 'check-url',
                    'i', 'd' 'H', 'n', 'o', 'r', 't', 'X'
                }

            else:
                cmd = [
                    'aspell',
                    'list',
                    '--encoding', self.normalize_utf(source[2])
                ]

                if personal_dict:
                    cmd.extend(['--add-extra-dicts', personal_dict])

                allowed = {
                    'conf-dir', 'data-dir', 'add-dict-alias', 'rem-dict-alias', 'dict-dir',
                    'encoding', 'add-filter', 'rem-filter', 'add-filter-path', 'rem-filter-path',
                    'mode', 'e', 'H', 't', 'n', 'add-extra-dicts', 'rem-extra-dicts', 'home-dir',
                    'ingore', 'W', 'dont-ignore-case', 'ignore-case', 'lang', 'l', 'local-data-dir',
                    'd', 'master', 'dont-normalize', 'normalize', 'dont-norm-required',
                    'norm-required', 'norm-form', 'dont-norm-strict', 'norm-strict', 'per-conf',
                    'p', 'personal', 'C', 'B', 'dont-run-together', 'run-together', 'run-together-limit',
                    'run-together-min', 'use-other-dicts', 'dont-use-other-dicts', 'add-variety', 'rem-variety',
                    'add-context-delimiters', 'rem-context-delimiters', 'dont-context-visible-first',
                    'context-visible-first', 'add-email-quote', 'rem-email-quote', 'email-margin',
                    'add-html-check', 'rem-html-check', 'add-html-skip', 'rem-html-skip', 'add-sgml-check',
                    'rem-sgml-check', 'add-sgml-skip', 'rem-sgml-skip', 'dont-tex-check-comments',
                    'tex-check-comments', 'add-tex-command', 'rem-tex-command', 'add-texinfo-ignore',
                    'rem-texinfo-ignore', 'add-texinfo-ignore-env', 'rem-texinfo-ignore-env', 'filter'
                }

            for k, v in options.items():
                if k in allowed:
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

    def skip_target(self, target):
        """Check if target should be skipped."""

        return self.skip_wild_card_target(target) or self.skip_regex_target(target)

    def skip_wild_card_target(self, target):
        """Check if target should be skipped via wildcard patterns."""

        exclude = False
        for pattern in self.excludes:
            if fnmatch.fnmatch(target, pattern):
                exclude = True
                break
        return exclude

    def skip_regex_target(self, target):
        """Check if target should be skipped via regex."""

        exclude = False
        for pattern in self.regex_excludes:
            if pattern.match(target, pattern):
                exclude = True
                break
        return exclude

    def is_extension(self, file_name, extensions):
        """Is extension in current extensions."""

        okay = False
        lowered = file_name.lower()
        for ext in extensions:
            if fnmatch.fnmatch(lowered, ext):
                okay = True
                break
        return okay

    def walk_src(self, targets, plugin):
        """Walk source and parse files."""

        # Override extensions if the user provides their own
        extensions = self.extensions if self.extensions else plugin.EXTENSIONS
        for target in targets:
            if os.path.isdir(target):
                if self.skip_target(target):
                    continue
                for base, dirs, files in os.walk(target):
                    [dirs.remove(d) for d in dirs[:] if self.skip_target(os.path.join(base, d))]
                    for f in files:
                        file_path = os.path.join(base, f)
                        if self.skip_target(file_path):
                            continue
                        if self.is_extension(f, extensions):
                            yield plugin.parse_file(file_path)
            elif self.is_extension(target, extensions):
                if self.skip_target(target):
                    continue
                yield plugin.parse_file(target)

    def setup_spellchecker(self, documents):
        """Setup spell checker."""

        self.spellchecker = documents.get('spell_checker', 'aspell')
        if self.spellchecker == 'hunspell':
            options = documents.get('hunspell', {})
        else:
            options = documents.get('aspell', {})

        return options

    def setup_dictionary(self, documents):
        """Setup dictionary."""

        dictionary_options = documents.get('dictionary', {})
        output = os.path.abspath(dictionary_options.get('output', self.dict_bin))
        lang = dictionary_options.get('lang', 'en' if self.spellchecker == 'aspell' else 'en_US')
        wordlists = dictionary_options.get('wordlists', [])
        if lang and wordlists:
            self.compile_dictionary(lang, dictionary_options.get('wordlists', []), output)
        else:
            output = None
        return output

    def setup_delimiters(self, documents):
        """Setup context delimiters."""

        context_delimiters = documents.get('context_delimiters', {})
        self.context_visible_first = context_delimiters.get('context_visible_first', False)
        self.delimiters = []
        self.escapes = None
        escapes = []
        internal_escapes = []
        for delimiter in context_delimiters.get('delimiters', []):
            if not isinstance(delimiter, dict):
                continue
            for escape in delimiter.get('escapes', []):
                if escape:
                    escapes.append(escape)
            for escape in delimiter.get('internal_escapes', []):
                if escape:
                    internal_escapes.append(escape)
            if internal_escapes:
                content = r'(?:\\(?:%s)|[^\\])*?' % '|'.join([r'\\'] + [re.escape(e) for e in internal_escapes])
            else:
                content = r'[\s\S]*?'
            group = random_name_gen()
            while group in delimiter['open'] or group in delimiter['close']:
                group = random_name_gen()
            pattern = r'%s(?P<%s>%s)(?:%s|\Z)' % (delimiter['open'], group, content, delimiter['close'])
            self.delimiters.append((re.compile(pattern, re.M), group))
        self.escapes = re.compile(r'\\(?:%s)' % '|'.join([r'\\'] + [re.escape(e) for e in escapes]))

    def setup_excludes(self, documents):
        """Setup excludes."""

        # Read excludes
        self.excludes = documents.get('excludes', [])
        self.regex_excludes = [re.compile(exclude) for exclude in documents.get('regex_excludes', [])]

    def setup_html(self, documents):
        """Setup HTML."""

        # Setup HTML options
        html_options = documents.get('html', {})
        self.attributes = set(html_options.get('attributes', []))
        self.selectors = self.process_selectors(*html_options.get('ignores', []))

    def check(self):
        """Walk source and initiate spell check."""

        fail = False
        for documents in self.documents:
            lang = documents['language']
            for plugin in self.plugins:
                if lang == plugin.LANGUAGE:
                    # Setup plugin and variables for the spell check
                    plug = plugin(documents.get('options', {}), documents.get('fallback_encoding', 'ascii'))
                    self.extensions = documents.get('extensions', [])
                    options = self.setup_spellchecker(documents)
                    output = self.setup_dictionary(documents)
                    self.setup_html(documents)
                    self.setup_delimiters(documents)
                    self.setup_excludes(documents)

                    # Perform spell check
                    print('Spell Checking %s...' % documents.get('name', ''))
                    for sources in self.walk_src(documents.get('src', []), plug):
                        if self.check_spelling(sources, options, output):
                            fail = True

                    break
        return fail


if __name__ == "__main__":
    def main():
        """Main."""
        import argparse

        parser = argparse.ArgumentParser(prog='spellcheck', description='Spell checking tool.')
        # Flag arguments
        parser.add_argument('--version', action='version', version=('%(prog)s ' + __version__))
        parser.add_argument('--verbose', '-v', action='store_true', default=False, help="verbose.")
        parser.add_argument('--config', '-c', action='store', default='.spelling.yml', help="Spelling config.")
        args = parser.parse_args()

        fail = False
        config = read_config(args.config)
        spelling = Spelling(config, [SpellingHTML, SpellingPython], verbose=args.verbose)
        if spelling.check():
            fail = True
        return fail

    sys.exit(main())
