---
icon: lucide/hammer
---
# Development

## Project Layout

There are a number of files for build, test, and continuous integration in the root of the project, but in general, the
project is broken up like so.

```
├── docs
├── pymdownx
├── tests
└── tools
```

Directory      | Description
-------------- | -----------
`docs`         | This contains the source files for the documentation.
`pymdownx`     | This contains the source code for all the extensions.
`tests`        | This contains the various tests that are run in order to ensure code health.
`tools`        | This contains various tools that are necessary during development.

Running tests and building documents is all done with @pypa/hatch. Install as shown below.

```console
$ pip install hatch
```

## Coding Standards

Coding standards are enforced using @astral-sh/ruff. The environment can be setup and run as shown below.

```console
$ hatch run +py=3.14 dev:lint
```

## Building and Editing Documents

Documents are in Markdown (with some additional syntax) and converted to HTML via Python Markdown and this extension
bundle. The documentation site is built with @zensical/zensical.

To build docs:

```console
$ hatch run docs:build
```

To serve docs and to live preview in a browser:

```console
$ hatch run docs:serve
```

To clean the documents:

```console
$ hatch run docs:clean
```

## Editing Document Theme

It isn't expected that people will need to mess with the theme, but if it is needed, a little additional work is
required. The documents use [Zensical][zensical] with some additional local tweaks and additions.  JavaScript additions
are provided in `docs/src/js` and are in es2020 syntax and are converted to es5. Stylesheets are located at
`docs/src/scss` and are written in SCSS, and are converted to CSS.  All conversions are done in a `Node.js` environment.
In order to get up and running, ensure you have a [`Node.js`](https://nodejs.org/en/) version >= 10. Then install the
required modules with:

```console
$ npm install --legacy-peer-deps
```

After that you can begin making changes. When ready, you can run the following commands to get a live preview while you
make edits, lint your changes, or build the final output.

Commands            | Description
------------------- | -----------
`npm run build`     | Build the final output which will package, minimize, and revision the scripts and stylesheets.  It will also update the `zensical.yml` file to point to the new revisioned files.

If you need to make changes to the `zenscial.yml` file, do not update the one in project root directly, but update the
one in `docs/src`. The build environment copies the one in `docs/src` to the project root and injects the revisioned
script name(s) and stylesheet name(s).

## Spell Checking Documents

During validation, we build the docs and run a spell checker on them.  The spell checker uses @facelessuser/pyspelling
and [Aspell][aspell]. As it can be trickier to run Aspell under Windows, it is not expected that everyone will install
and run the spell checker locally.  In order to perform the spell check, just run the following command:

```console
$ hatch run docs:spellcheck
```

## Validation Tests

In order to preserve good code health, a test suite has been put together with pytest (@pytest-dev/pytest). There are
currently two kinds of tests: syntax and targeted.  To run these tests, you can use the following command:

If you wish to run the tests locally, just run:

```console
$ hatch run +py=3.14 dev:tests
```

### Syntax

Syntax tests are essentially text files containing Markdown. They are found under `tests/extensions`.  `test_syntax.py`
scans all the files and converts the files to HTML with the extensions and options defined in
`tests/extensions/tests.yml`.  They are then compared to the current stored HTML output.  If the two differ, the test
fails.

To run **only** these tests, from the root of the project run the following command:

```console
$ python run_tests.py --test-target syntax
```

You could also run them directly with:

```console
$ py.test tests/test_syntax.py
```

To run a specific syntax test:

```console
$ python run_tests.py --test-target syntax --file tests/extensions/arithmatex.txt
```

To accept the differences in tests due to a change(s) you made, you can run the following command:

```console
$ python run_tests.py --update
```

To update and accept the differences in a single test:

```console
$ python run_tests.py --update --file tests/extensions/arithmatex.txt
```

### Targeted

Targeted tests are unit tests that target specific areas in the code and exercises them to ensure proper functionality.
These tests are found in `test_targeted.py`.

You can run **only** these tests from the root of the project with:

```console
$ python run_tests.py --test-target targeted
```

You could also run them directly with:

```console
$ py.test tests/test_targeted.py
```

## Code Coverage

When running the validation tests, it is setup to track code coverage via the Coverage
(@bitbucket:ned/coveragepy) module.  Coverage is run on each Python environment.  If you've made changes to
the code, you can clear the old coverage data, assuming coverage is installed, by running:

```console
$ coverage erase
```

Then run each unit test environment to and coverage will be calculated. All the data from each run is merged together.
HTML is output for each file in `.cov`.  You can use these to see areas that are not covered/exercised yet with testing.

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
