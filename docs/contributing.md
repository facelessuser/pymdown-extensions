# Contributing &amp; Support {: .doctitle}
Steps for contributing and getting support.

---

## Overview
Contribution from the community is encouraged and can be done in a variety of ways:

- Bug reports.
- Reviewing code.
- Code patches via pull requests.
- Documentation improvements via pull requests.

## Bug Reports

1. Please **read the documentation** and **search the issue tracker** to try to find the answer to your question **before** posting an issue.

2. When creating an issue on the repository, please provide as much info as possible:

    - Version being used.
    - Operating system.
    - Errors in console.
    - Detailed description of the problem.
    - Examples for reproducing the error.  You can post pictures, but if specific text or code is required to reproduce the issue, please provide the text in a plain text format for easy copy/paste.

    The more info provided the greater the chance someone will take the time to answer, implement, or fix the issue.

3. Be prepared to answer questions and provide additional information if required.  Issues in which the creator refuses to respond to follow up questions will be marked as stale and closed.

## Reviewing Code
Take part in reviewing pull requests and/or reviewing direct commits.  Make suggestions to improve the code and discuss solutions to overcome weakness in the algorithm.

## Pull Requests
Pull requests are welcome, and if you plan on contributing directly to the code, there are a couple of things to be mindful of.

Continuous integration tests on are run on all pull requests and commits via Travis CI.  When making a pull request, the tests will automatically be run, and the request must pass to be accepted.  You can (and should) run these tests before pull requesting.  If it is not possible to run these tests locally, they will be run when the pull request is made, but it is strongly suggested that requesters make an effort to verify before requesting to allow for a quick, smooth merge.

Feel free to use a virtual environment if you are concerned about installing any of the Python packages.

### Running Validation Tests

1. Make sure that `tox` is intalled:

    ```
    pip install tox
    ```

2. Run tox:

    ```
    tox
    ```

    Tox should install necessary dependencies and run the tests.

## Documentation Improvements
A ton of time has been spent not only creating and supporting this tool and related extensions, but also spent making this documentation.  If you feel it is still lacking, show your appreciation for the tool and/or extensions by helping to improve the documentation.  Help with documentation is always appreciated and can be done via pull requests.  There shouldn't be any need to run validation tests if only updating documentation.

You don't have to render the docs locally before pull requesting, but if you wish to, I currently use a combination of [mkdocs](http://www.mkdocs.org) with my own custom Python Markdown [extensions](https://github.com/facelessuser/pymdown-extensions) to render the docs.  You can preview the docs if you install these two packages.  The command for previewing the docs is `mkdocs serve` from the root directory.
