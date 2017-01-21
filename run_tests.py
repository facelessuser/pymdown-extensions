"""Run the unittests or update unitest compare files."""
from __future__ import unicode_literals
import argparse
from tests import test_syntax
from tests import test_targeted
import sys
import os


def main():
    """Main function."""

    parser = argparse.ArgumentParser(prog='run_tests', description='Run extension tests.')
    # Flag arguments
    parser.add_argument('--update', '-u', action='store_true', default=False, help="Update expected HTML output.")
    parser.add_argument(
        '--test-target', '-t', nargs=1, action='store', default="", choices=['syntax', 'targeted'],
        help="Test specific enivronment."
    )
    parser.add_argument(
        '--file', '-f', nargs=1, action='store', default="", help="Test or update specific test."
    )
    args = parser.parse_args()
    sys.argv = sys.argv[0:1]

    if args.file:
        abs_path = os.path.abspath(args.file[0])
        if os.path.exists(abs_path):
            test_syntax.set_target_file(abs_path)

    # Format and Viewing
    if args.update:
        for config, test in test_syntax.gather_test_params():
            test_syntax.compare_results(config, test, args.update)
    else:
        if not args.test_target or args.test_target[0] == 'syntax':
            test_syntax.run()
        if not args.test_target or args.test_target[0] == 'targeted':
            test_targeted.run()


if __name__ == '__main__':
    main()
