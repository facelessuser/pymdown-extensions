"""Spell check with aspell."""
from os import environ
import subprocess
import os
import sys


def console(cmd, input_file=None):
    """Call with arguments."""

    returncode = None
    output = None

    env = environ.copy()
    env['LC_ALL'] = 'en_US'

    if sys.platform.startswith('win'):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(
            cmd,
            startupinfo=startupinfo,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            shell=False,
            env=env
        )
    else:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            shell=False,
            env=env
        )

    if input_file is not None:
        with open(input_file, 'rb') as f:
            process.stdin.write(f.read())
    output = process.communicate()
    returncode = process.returncode

    assert returncode == 0, "Runtime Error: %s" % output[0].rstrip()

    return output[0]


def build_docs():
    """Build docs with MkDocs."""
    print('Building Docs...')
    print(console([sys.executable, '-m', 'mkdocs', 'build', '--clean']))


def compile_dictionary():
    """Compile user dictionary."""
    print("Compiling Custom Dictionary...")
    print(console(['aspell', '--lang=en', 'create', 'master', './tmp'], '.dictionary'))


def check_spelling():
    """Check spelling."""
    print('Spell Checking...')

    fail = False

    for base, dirs, files in os.walk('site'):
        # Remove child folders based on exclude rules
        for f in files:
            if f.endswith('.html'):
                file_name = os.path.join(base, f)
                wordlist = console(
                    [
                        'aspell',
                        'list',
                        '--lang=en',
                        '--mode=html',
                        '--add-html-skip=code',
                        '--add-html-skip=pre',
                        '--extra-dicts=./tmp'
                    ],
                    file_name
                ).decode('utf-8')

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
    build_docs()
    compile_dictionary()
    return check_spelling()


if __name__ == "__main__":
    sys.exit(main())
