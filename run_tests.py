"""Run the unittests or update unitest compare files."""
import tests.test_extensions as tests
import argparse


def main():
    """Main function."""

    parser = argparse.ArgumentParser(prog='run_tests', description='Run extension tests.')
    # Flag arguments
    parser.add_argument('--update', '-u', action='store_true', default=False, help="Update expected HTML output.")
    parser.add_argument('--force-update', '-f', action='store_true', default=False, help="Force all files to update.")
    args = parser.parse_args()

    # Format and Viewing
    if args.update or args.force_update:
        for config, test in tests.gather_test_params():
            tests.compare_results(config, test, True, args.force_update)
    else:
        tests.run()


if __name__ == '__main__':
    main()
