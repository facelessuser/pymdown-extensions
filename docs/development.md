## Project Layout

There are a number of files for build, test, and continuous integration in the root of the project, but in general, the project is broken up like so.

```
├── doc_theme
├── docs
├── pymdownx
├── requirements
├── tests
└── tools
```

Directory    | Description
---------    | -----------
doc_theme    | This contains document theme tweaks for the current theme
docs         | This contains the source files for the documentation.
pymdownx     | This contains the source code for all the extensions.
requirements | This contains files with lists of dependencies required dependencies for continuous integration.
tests        | This contains the various tests that are run in order to ensure code health.
tools        | This contains various tools that are necessary during development.

## Coding Standards

When writing code, the code should roughly conform to PEP8 and PEP257 suggestions.  The PyMdown Extensions project utilizes the flake8 linter (with some additional plugins) to ensure code conforms (give or take some of the rules).  When in doubt follow the formatting hints of existing code when adding or modifying files. existing files.  Listed below are the modules used:

- [flake8][1]
- [flake8_docstrings][2]
- [pep8-naming][3]

Flake8 can be run directly via the command line from the root of the project.

```
flake8
```

[1]: https://pypi.python.org/pypi/flake8/3.2.1
[2]: https://pypi.python.org/pypi/flake8-docstrings
[3]: https://pypi.python.org/pypi/pep8-naming

## Building Documents

Documents are in Markdown (with with some additional syntax) and converted to HTML via Python Markdown and this extension bundle. If you would like to build and preview the documentation, you must have these packages installed:

- [Python Markdown][10]: the Markdown parser.
- [MkDocs][11]: the document site generator.
- [Material][12]: a material theme for MkDocs (currently locked to [this][13] version until the official release.)
- pymdown-extensions: this Python Markdown extension bundle.

In order to build and preview the documents, just run the following from the root of the project and you should be able to view the docs at `localhost:8000` in your browser (assuming you have the dependencies installed).

```
mkdocs serve
```

[10]: https://github.com/waylan/Python-Markdown
[11]: https://github.com/mkdocs/mkdocs
[12]: https://github.com/squidfunk/mkdocs-material
[13]: https://github.com/squidfunk/mkdocs-material/tree/2dbf60affd8db8298cd4233002da62429f6427be

## Spell Checking Documents

During validation we build the docs and run a spell checker on them.  The spell checker script uses [aspell][20].  Currently this project uses the latest aspell.  As the latest aspell is not available on Windows, it is not expected that everyone will install and run aspell locally.  In order to perform the spell check, it is expected you are setup to build the documents, and that you have aspell installed in the your system path. To initiate the spell check run the following command from the root of the project:

```
python spelling.py
```

It should print out the files with the misspelled words if any are found.  If you find it prints words that are not misspelled, you can add them in `.dictionary` in the root of the project.

[20]: http://aspell.net/

## Validation Tests

In order to preserve good code health, a test suite has been put together with [pytest][30]. There are currently two kinds of tests: syntax and targeted.  To run these tests, you can use the following command:

```
python run_tests.py
```

### Syntax

Syntax tests are essentially text files containing Markdown. They are found under `tests/extensions`.  `test_syntax.py` scans all the files and converts the files to HTML with the extensions and options defined in `tests/extensions/tests.yml`.  They are then compared to the current stored HTML output.  If the two differ, the test fails.

To run **only** these tests, from the root of the project run the following command:

```
python run_tests.py --test-target syntax
```

You could also run them directly with:

```
py.test tests/test_syntax.py
```

To update (accept) changes for differing files, and overwrite the old HTML with the new ones:

```
python run_tests.py --update
```

When tests are run, only the syntax of the Markdown output is compared, so if you change something like the CSS for a specific test (which are used for visual inspection), those kind of changes won't get detected and won't cause the file to get updated with `--update`.  You can force all files to be updated, by running:

```
python run_tests.py --update --force
```

### Targeted

Targeted tests are unit tests that target specific areas in the code and exercises them to ensure proper functionality.  These tests are found in `test_targeted.py`.

You can run **only** these tests from the root of the project with:

```
python run_tests.py --test-target targeted
```

You could also run them directly with:

```
py.test tests/test_targeted.py
```

[30]: http://doc.pytest.org/en/latest/

### Running Validation With Tox

[Tox][40] is a great way to run the validation tests, spelling checks, and linting in virtual environments so as not to mess with your current working environment. Tox will use the specified Python version for the given environment and create a virtual environment and install all the needed requirements (minus aspell).  You could also setup your own virtual environments with the virtualenv module without tox, and manually do the same.

First, you need to have tox installed:

```
pip install tox
```

By running tox, it will walk through all the environments and create them (assuming you have all the python versions on your machine) and run the related tests.  See `tox.ini` to learn more.

```
tox
```

If you don't have all the Python versions needed to test all the environments, those entries will fail.  You can ignore those.  Spelling will also fail if you don't have the correct version of aspell.

To target a specific environment to test, you use the `-e` option to select the environment of interest.  To select lint:

```
tox -elint
```

To select PY27 unit tests (or other versions -- change accordingly):

```
tox -epy27-unittests
```

To select spelling:

```
tox -espelling
```

[40]: https://pypi.python.org/pypi/tox

## Code Coverage

When running the validation tests through tox, it is setup to track code coverage via the [coverage][50] module.  Coverage is run on each `pyxx-unittests` environment.  If you've made changes to the code, you can clear the old coverage data:

```
coverage erase
```

Then run each unit test environment to and coverage will be calculated. All the data from each run is merged together.  HTML is output for each file in `.tox/pyXX-unittests/tmp`.  You can use these to see areas that are not covered/exercised yet with testing.

You can checkout `tox.ini` to see how this is accomplished.

[50]: https://coverage.readthedocs.io/en/coverage-4.3.1/

## Generating Emoji Indexes

The Emoji extension has emoji indexes generated from the source of Gemoji and EmojiOne.  Below is the process for auto-generating these indexes.

1. Ensure you have [requests][60] installed: `pip install requests`.
2. Fork the repo and checkout to your machine.
3. Navigate to the "tools" directory: `cd pymdown-extensions/tools`.
4. Call the generator script: `python gen_emoji --gemoji` or `python gen_emoji --emojione`.  It will prompt you to select a tag to download.  Please pull the latest **official** tag.  Please don't pull experimental tags.  This should update the indexes.
5. Then you want to update the tests.  Step back out to the root of the project: `cd ..`.
6. Force the tests to update via `python run_tests.py -u`.

Nothing is fool proof.  If they make a breaking change to the files that the script parses, or the location of the files change, the auto-update tool may need to be updated itself (hopefully this would be a rare occurrence).  If such a change does occur, and you are feeling brave, a pull request would be appreciated, but in time, they will be resolved regardless.

[60]: https://pypi.python.org/pypi/requests/
