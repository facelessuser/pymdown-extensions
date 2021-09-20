"""Test extension syntax."""
import os
import markdown
import difflib
import codecs
import pytest
import copy
from . import util
import warnings

warnings.simplefilter('ignore', DeprecationWarning)

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

CSS_LINK = '<link rel="stylesheet" type="text/css" href="%s"/>'
WRAPPER = '''<!DOCTYPE html>
<head>
<meta charset="utf-8">
%s
</head>
<body>
<div class="markdown-body">
%%s
</div>
</body>
'''

target_file = None


def set_target_file(file_name):
    """Set target test file name."""

    global target_file
    target_file = file_name


def compare_results(cfg, testfile, update=False):
    """Compare test results."""

    extension = []
    extension_config = {}
    wrapper = "%s"
    for k, v in cfg['extensions'].items():
        extension.append(k)
        if v:
            extension_config[k] = v
    if 'css' in cfg and len(cfg['css']):
        wrapper = WRAPPER % '\n'.join([CSS_LINK % css for css in cfg['css']])

    check_markdown(testfile, extension, extension_config, wrapper, update)


def check_markdown(testfile, extension, extension_config, wrapper, update=False):
    """Check the markdown."""

    expected_html = os.path.splitext(testfile)[0] + '.html'
    with codecs.open(testfile, 'r', encoding='utf-8') as f:
        source = f.read()

    results = wrapper % markdown.Markdown(
        extensions=extension, extension_configs=extension_config
    ).convert(source)

    try:
        with codecs.open(expected_html, 'r', encoding='utf-8') as f:
            expected = f.read().replace("\r\n", "\n")
    except Exception:
        expected = ''

    diff = [
        l for l in difflib.unified_diff(
            expected.splitlines(True),
            results.splitlines(True),
            expected_html,
            os.path.join(os.path.dirname(testfile), 'results.html'),
            n=3
        )
    ]
    if diff:
        if update:
            print('Updated: %s' % expected_html)
            with codecs.open(expected_html, 'w', encoding='utf-8') as f:
                f.write(results)
        else:
            raise Exception(
                'Output from "%s" failed to match expected '
                'output.\n\n%s' % (testfile, ''.join(diff))
            )
    elif update:
        print('Skipped: %s' % expected_html)


def gather_test_params():
    """Gather the test parameters."""

    for base, dirs, files in os.walk(CURRENT_DIR):
        [dirs.remove(d) for d in dirs[:] if d.startswith('_')]
        cfg_path = os.path.join(base, 'tests.yml')
        if os.path.exists(cfg_path):
            files.remove('tests.yml')
            [files.remove(file) for file in files[:] if not file.endswith('.txt')]
            with codecs.open(cfg_path, 'r', encoding='utf-8') as f:
                cfg = util.yaml_load(f.read())
            for testfile in files:
                key = os.path.splitext(testfile)[0]
                test_cfg = copy.deepcopy(cfg['__default__'])
                if 'extensions' not in test_cfg:
                    test_cfg['extensions'] = util.OrderedDict()
                if 'css' not in test_cfg:
                    test_cfg['css'] = []
                for k, v in cfg.get(key, util.OrderedDict()).items():
                    if k == 'css':
                        for css in v:
                            test_cfg[k].append(css)
                        continue
                    for k1, v1 in v.items():
                        if v1 is not None:
                            for k2, v2 in v1.items():
                                if isinstance(v2, str):
                                    v1[k2] = v2.replace(
                                        '{{BASE}}', base
                                    ).replace(
                                        '{{RELATIVE}}', CURRENT_DIR
                                    )
                                elif k2 == 'base_path' and isinstance(v2, list):
                                    for i, v3 in enumerate(v2, 0):
                                        v1[k2][i] = v3.replace(
                                            '{{BASE}}', base
                                        ).replace(
                                            '{{RELATIVE}}', CURRENT_DIR
                                        )
                        test_cfg[k][k1] = v1
                target = os.path.join(base, testfile)
                if target_file is not None and target != target_file:
                    continue
                yield test_cfg, os.path.join(base, testfile)


def pytest_generate_tests(metafunc):
    """Generate tests."""

    if "compare" in metafunc.fixturenames:
        metafunc.parametrize("compare", gather_test_params())


def test_extensions(compare):
    """Test extensions."""

    compare_results(*compare)


def run():
    """Run pytest."""

    pytest.main(
        [
            'tests/test_syntax.py',
            '-p', 'no:pytest_cov'
        ]
    )
