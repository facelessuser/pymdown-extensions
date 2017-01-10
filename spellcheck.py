"""Spell check with aspell."""
from os import environ
import subprocess
import os
import sys

LINUX_WORKAROUND = '--local-data-dir=/usr/lib/aspell'


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


def compile_dictionary(linux_workaround):
    """Compile user dictionary."""
    print("Compiling Custom Dictionary...")

    cmd = ['aspell', '--lang=en']
    if linux_workaround:
        cmd.append(LINUX_WORKAROUND)
    cmd.extend(['create', 'master', './tmp'])
    print(console(cmd, '.dictionary'))


def check_spelling(linux_workaround):
    """Check spelling."""
    print('Spell Checking...')

    fail = False
    cmd = [
        'aspell',
        'list',
        '--lang=en',
        '--mode=html',
        '--add-html-skip=code',
        '--add-html-skip=pre',
        '--extra-dicts=./tmp'
    ]
    if linux_workaround:
        cmd.append(LINUX_WORKAROUND)

    for base, dirs, files in os.walk('site'):
        # Remove child folders based on exclude rules
        for f in files:
            if f.endswith('.html'):
                file_name = os.path.join(base, f)
                wordlist = console(cmd, file_name).decode('utf-8')
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


def main(linux_workaround):
    """Main."""
    build_docs()
    compile_dictionary(linux_workaround)
    return check_spelling(linux_workaround)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog='spellcheck', description='Spell Check with aspell.')
    # Flag arguments
    parser.add_argument(
        '--linux-workaround',
        action='store_true',
        default=False, help="Fix for 'Error: The language \"en\" is not known' on some Linux systems."
    )
    args = parser.parse_args()
    sys.exit(main(args.linux_workaround))
