"""Test extension libraries."""
from __future__ import unicode_literals
import os
import markdown
import difflib
import codecs
import pytest
import copy
from . import util

CURRENT_DIR = os.path.dirname(__file__)

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


def compare_results(cfg, testfile, update=False, force_update_all=False):
    """Compare test reslts."""

    extension = []
    extension_config = {}
    wrapper = "%s"
    for k, v in cfg['extensions'].items():
        extension.append(k)
        if v:
            extension_config[k] = v
    if 'css' in cfg and len(cfg['css']):
        wrapper = WRAPPER % '\n'.join([CSS_LINK % css for css in cfg['css']])

    if update:
        generate_html(testfile, extension, extension_config, wrapper, force_update_all)
    else:
        check_markdown(testfile, extension, extension_config, wrapper)


def generate_html(testfile, extension, extension_config, wrapper, force_update_all):
    """Generate html from markdown."""

    expected_html = os.path.splitext(testfile)[0] + '.html'
    if (
        force_update_all or
        not os.path.exists(expected_html) or
        os.path.getmtime(expected_html) < os.path.getmtime(testfile)
    ):
        print('Updated: %s' % expected_html)
        with codecs.open(testfile, 'r', encoding='utf-8') as f:
            source = f.read()
        results = wrapper % markdown.Markdown(
            extensions=extension, extension_configs=extension_config
        ).convert(source)
        with codecs.open(expected_html, 'w', encoding='utf-8') as f:
            f.write(results)


def check_markdown(testfile, extension, extension_config, wrapper):
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
        raise Exception(
            'Output from "%s" failed to match expected '
            'output.\n\n%s' % (testfile, ''.join(diff))
        )


def gather_test_params():
    """Gather the test parameters."""

    for filename in os.listdir(CURRENT_DIR):
        directory = os.path.join(CURRENT_DIR, filename)
        if os.path.isdir(directory):
            cfg_path = os.path.join(directory, 'tests.yml')
            if os.path.exists(cfg_path):
                with codecs.open(cfg_path, 'r', encoding='utf-8') as f:
                    cfg = util.yaml_load(f.read())
                for testfile in os.listdir(directory):
                    if testfile.endswith('.txt'):
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
                                        if isinstance(v2, util.string_type):
                                            v1[k2] = v2.replace(
                                                '{{BASE}}', os.path.join(CURRENT_DIR, 'extensions')
                                            ).replace(
                                                '{{RELATIVE}}', os.path.join(CURRENT_DIR)
                                            )
                                test_cfg[k][k1] = v1
                        yield test_cfg, os.path.join(directory, testfile)


def pytest_generate_tests(metafunc):
    """Generate tests."""

    if "compare" in metafunc.funcargnames:
        metafunc.parametrize("compare", gather_test_params())


def test_extensions(compare):
    """Test extensions."""

    compare_results(*compare)


def run():
    """Run pytest."""

    pytest.main()
