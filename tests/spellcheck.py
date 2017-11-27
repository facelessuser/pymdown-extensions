"""Spell check with aspell."""
from __future__ import unicode_literals
import subprocess
import os
import sys
import yaml
import codecs
import bs4

PY3 = sys.version_info >= (3, 0)

USER_DICT = '.dictionary'
BUILD_DIR = os.path.join('.', 'build', 'docs')
MKDOCS_CFG = 'mkdocs.yml'
COMPILED_DICT = os.path.join(BUILD_DIR, 'dictionary.bin')
MKDOCS_SPELL = os.path.join(BUILD_DIR, MKDOCS_CFG)
MKDOCS_BUILD = os.path.join(BUILD_DIR, 'site')


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


def yaml_dump(data, stream=None, dumper=yaml.Dumper, **kwargs):
    """Special dumper wrapper to modify the yaml dumper."""

    class Dumper(dumper):
        """Custom dumper."""

    if not PY3:
        # Unicode
        Dumper.add_representer(
            unicode,  # noqa
            lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:str', value)
        )

    return yaml.dump(data, stream, Dumper, **kwargs)


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


def patch_doc_config(config_file):
    """Patch the config file to wrap arithmatex with a tag aspell can ignore."""

    with open(config_file, 'rb') as f:
        config = yaml_load(f)

    index = 0
    for extension in config.get('markdown_extensions', []):
        if isinstance(extension, str if PY3 else unicode) and extension == 'pymdownx.arithmatex':  # noqa
            config['markdown_extensions'][index] = {'pymdownx.arithmatex': {'insert_as_script': True}}
            break
        elif isinstance(extension, dict) and 'pymdownx.arithmatex' in extension:
            if isinstance(extension['pymdownx.arithmatex'], dict):
                extension['pymdownx.arithmatex']['insert_as_script'] = True
            elif extension['pymdownx.arithmatex'] is None:
                extension['pymdownx.arithmatex'] = {'insert_as_script': True}
            break
        index += 1

    with codecs.open(MKDOCS_SPELL, "w", encoding="utf-8") as f:
        yaml_dump(
            config, f,
            width=None,
            indent=4,
            allow_unicode=True,
            default_flow_style=False
        )
    return MKDOCS_SPELL


def build_docs():
    """Build docs with MkDocs."""
    print('Building Docs...')
    print(
        console(
            [
                sys.executable,
                '-m', 'mkdocs', 'build', '--clean',
                '-d', MKDOCS_BUILD,
                '-f', patch_doc_config(MKDOCS_CFG)
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

    - tag
    - tag#id
    - #id
    - tag#id.class1.class2
    - tag.class1.class2
    - #id.class1.class2
    - .class1.class2
    """

    ignores = []

    for arg in args:
        selector = arg.lower()
        tag = None
        tag_id = None
        classes = []

        items = selector.split('#')
        if len(items) > 1:
            if items[0]:
                tag = items[0]
            items2 = items[1].split('.')
            if len(items2) > 1:
                if items2[0]:
                    tag_id = items2[0]
                classes.extend([x for x in items2[1:] if x])
            else:
                tag_id = items[0]
        else:
            items = items[0].split('.')
            if len(items) > 1:
                if items[0]:
                    tag = items[0]
                classes.extend([x for x in items[1:] if x])
            else:
                tag = selector

        if tag or tag_id or classes:
            ignores.append([tag, tag_id, classes])

    return ignores


def skip_tag(el, ignore):
    """Determine if tag should be skipped."""

    for tag, tag_id, classes in ignore:
        if tag and el.name.lower() != tag:
            continue
        if tag_id and tag_id != el.attrs.get('id', '').lower():
            continue
        if classes:
            current_classes = [c.lower() for c in el.attrs.get('class', [])]
            found = True
            for c in classes:
                if c not in current_classes:
                    found = False
                    break
            if not found:
                continue
        return True
    return False


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
    ignores = ignore_rules('code', 'pre', 'script', 'style', 'a.magiclink-compare', 'a.magiclink-commit')
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
