# Development

## Project Layout

There are a number of files for build, test, and continuous integration in the root of the project, but in general, the
project is broken up like so.

```
├── docs
├── pymdownx
├── requirements
├── tests
└── tools
```

Directory      | Description
-------------- | -----------
`docs`         | This contains the source files for the documentation.
`pymdownx`     | This contains the source code for all the extensions.
`requirements` | This contains files with lists of dependencies required dependencies for continuous integration.
`tests`        | This contains the various tests that are run in order to ensure code health.
`tools`        | This contains various tools that are necessary during development.

## Coding Standards

When writing code, the code should roughly conform to PEP8 and PEP257 suggestions.  The PyMdown Extensions project
utilizes the Flake8 linter (with some additional plugins) to ensure code conforms (give or take some of the rules).
When in doubt follow the formatting hints of existing code when adding or modifying files. existing files.  Listed below
are the modules used:

-   @PyCQA/flake8
-   @PyCQA/flake8-docstrings
-   @PyCQA/pep8-naming
-   @ebeweber/flake8-mutable
-   @gforcada/flake8-builtins

Flake8 can be run directly via the command line from the root of the project.

```
flake8
```

## Building and Editing Documents

Documents are in Markdown (with some additional syntax) and converted to HTML via Python Markdown and this
extension bundle. If you would like to build and preview the documentation, you must have these packages installed:

-   @Python-Markdown/markdown: the Markdown parser.
-   @mkdocs/mkdocs: the document site generator.
-   @squidfunk/mkdocs-material: a material theme for MkDocs.
-   @timvink/mkdocs-git-revision-date-localized-plugin: inserts date a page was last updated.
-   @facelessuser/pymdown-extensions: this Python Markdown extension bundle.

These can be installed via:

```
pip install -r requirements/docs.txt
```

In order to build and preview the documents, just run the command below from the root of the project and you should be
able to view the documents at `localhost:8000` in your browser. After that, you should be able to update the documents
and have your browser preview update live.

```
mkdocs serve
```

## Editing Document Theme

It isn't expected that people will need to mess with the theme, but if it is needed, a little additional work is
required. The documents use the [Material][mkdocs-material] theme for [MkDocs][mkdocs] with some additional local tweaks
and additions.  JavaScript additions are provided in `docs/src/js` and are in es2020 syntax and are converted to es5.
Stylesheets are located at `docs/src/scss` and are written in SCSS, and are converted to CSS.  All conversions are done
in a `Node.js` environment.  In order to get up and running, ensure you have a [`Node.js`](https://nodejs.org/en/)
version >= 10. Then install the required modules with:

```
npm install
```

After that you can begin making changes. When ready, you can run the following commands to get a live preview while you
make edits, lint your changes, or build the final output.

Commands            | Description
------------------- | -----------
`npm run serve`     | Create a live preview at `localhost:8000` that will pick up your changes as you make them.
`npm run build`     | Build the final output which will package, minimize, and revision the scripts and stylesheets.  It will also update the `mkdocs.yml` file to point to the new revisioned files.
`npm run lint`      | Run just lint on the files.
`npm run clean_all` | This will clean out the generated CSS and JavaScript files. It will also cleanup the generated MkDocs' site.

If you need to make changes to the `mkdocs.yml` file, do not update the one in project root directly, but update the one
in `docs/src`. The build environment copies the one in `docs/src` to the project root and injects the revisioned script
name(s) and stylesheet name(s).

When serving via `npm`, if you want to make sure that the local version of `pymdown-extensions` is used, you need to
configure `npm run serve` to call with Python instead of calling the MkDocs binary:
`npm run serve --mkdocs="python3 -m mkdocs"`.  This is because if you are calling Python, it will look in the current
working directory first for a given module when importing, but if you call the MkDocs binary, it will instead import the
installed `pymdown-extensions`. Configuring the `--mkdocs` option is also useful if `mkdocs` is not in your path, or you
want to call with a specific version of Python.

## Spell Checking Documents

During validation, we build the docs and run a spell checker on them.  The spell checker uses @facelessuser/pyspelling
and [Aspell][aspell]. As it can be trickier to run Aspell under Windows, it is not expected that everyone will install
and run the spell checker locally.  In order to perform the spell check, it is expected you are setup to build the
documents, and that you have Aspell installed in the your system path.

If you wish to run the spell checker locally, the recommended way is with Tox, which is covered in ["Running Validation
With Tox"](#running-validation-with-tox).

You can also run the spell checker by first installing the requirements (assuming a Linux system):

```
pip install -r requirements/docs.txt
sudo apt-get install aspell aspell-en
```

Then build the docs:

```
mkdocs build --clean
```

And then run the spell checker:

```
pyspelling
```

It should print out the files with the misspelled words if any are found.  If you find it prints words that are not
misspelled, you can add them in the dictionary which is found in `docs/src/dictionary`.

## Validation Tests

In order to preserve good code health, a test suite has been put together with pytest (@pytest-dev/pytest). There are
currently two kinds of tests: syntax and targeted.  To run these tests, you can use the following command:

If you wish to run the tests locally, the recommended way is with Tox, which is covered in ["Running Validation With
Tox"](#running-validation-with-tox).

You can also run the tests by first installing the requirements:

```
pip install -r requirements/project.txt
pip install -r requirements/extra.txt
pip install -r requirements/test.txt
```

And then run the tests with:

```
python run_tests.py
```

### Syntax

Syntax tests are essentially text files containing Markdown. They are found under `tests/extensions`.  `test_syntax.py`
scans all the files and converts the files to HTML with the extensions and options defined in
`tests/extensions/tests.yml`.  They are then compared to the current stored HTML output.  If the two differ, the test
fails.

To run **only** these tests, from the root of the project run the following command:

```
python run_tests.py --test-target syntax
```

You could also run them directly with:

```
py.test tests/test_syntax.py
```

To run a specific syntax test:

```
python run_tests.py --test-target syntax --file tests/extensions/arithmatex.txt
```

To accept the differences in tests due to a change(s) you made, you can run the following command:

```
python run_tests.py --update
```

To update and accept the differences in a single test:

```
python run_tests.py --update --file tests/extensions/arithmatex.txt
```

### Targeted

Targeted tests are unit tests that target specific areas in the code and exercises them to ensure proper functionality.
These tests are found in `test_targeted.py`.

You can run **only** these tests from the root of the project with:

```
python run_tests.py --test-target targeted
```

You could also run them directly with:

```
py.test tests/test_targeted.py
```

### Running Validation With Tox

Tox (@tox-dev/tox) is a great way to run the validation tests, spelling checks, and linting in virtual environments so
as not to mess with your current working environment. Tox will use the specified Python version for the given
environment and create a virtual environment and install all the needed requirements (minus Aspell).  You could also
setup your own virtual environments with the Virtualenv module without Tox, and manually do the same.

First, you need to have Tox installed:

```
pip install tox
```

By running Tox, it will walk through all the environments and create them (assuming you have all the python versions on
your machine) and run the related tests.  See `tox.ini` to learn more.

```
tox
```

If you don't have all the Python versions needed to test all the environments, those entries will fail.  You can ignore
those.  Spelling will also fail if you don't have the correct version of Aspell.

To target a specific environment to test, you use the `-e` option to select the environment of interest.  To select
lint:

```
tox -e lint
```

To select Python 3.7 unit tests (or other versions -- change accordingly):

```
tox -e py37
```

To select spelling and document building:

```
tox -e documents
```

## Code Coverage

When running the validation tests through Tox, it is setup to track code coverage via the Coverage
(@bitbucket:ned/coveragepy) module.  Coverage is run on each `pyxx` environment.  If you've made changes to
the code, you can clear the old coverage data:

```
coverage erase
```

Then run each unit test environment to and coverage will be calculated. All the data from each run is merged together.
HTML is output for each file in `.tox/pyXX-unittests/tmp`.  You can use these to see areas that are not
covered/exercised yet with testing.

You can checkout `tox.ini` to see how this is accomplished.

## Generating Emoji Indexes

The Emoji extension has emoji indexes generated from the source of Gemoji, EmojiOne, and Twemoji.  Below is the process
for auto-generating these indexes.  In the case of Twemoji, it will also reference EmojiOne's short name index, so you
may need to do both EmojiOne and Twemoji if the support is not satisfactory.

1.  Ensure you have Requests (@requests/requests) installed: `pip install requests`.
2.  Fork the repository and checkout to your machine.
3.  Navigate to the root of the project.
4.  Call the generator script: `python tools/gen_emoji.py --gemoji`, `python tools/gen_emoji.py --emojione`, or
    `python tools/gen_emoji.py --twemoji`. If you already have the latest tag locally, you can specify `--no-download`.
    It will prompt you to select a tag to download and/or use.  Please pull the latest **official** tag.  Please don't
    pull experimental tags.  This should update the indexes.
5.  Then you want to update the tests.
6.  Force the tests to update via `python run_tests.py --update`.  Make sure only the emoji tests get updated.

Nothing is fool proof.  If they make a breaking change to the files that the script parses, or the location of the files
change, the auto-update tool may need to be updated itself (hopefully this would be a rare occurrence).  If such a
change does occur, and you are feeling brave, a pull request would be appreciated, but in time, they will be resolved
regardless.
