"""Test quoted attributes on code fences."""
from html.parser import HTMLParser
import markdown
import pytest
from pymdownx.superfences import fence_code_format, fence_div_format
from pymdownx.arithmatex import arithmatex_fenced_format


class AttributeParser(HTMLParser):
    """Collect the attributes exposed by generated HTML."""

    def __init__(self):
        """Initialize the parser."""

        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        """Collect a start tag."""

        self.tags.append((tag, dict(attrs)))


@pytest.mark.parametrize(
    'kind', ['custom-code', 'custom-div', 'arithmatex', 'pygments', 'js-code', 'js-pre', 'pygments-anchors']
)
def test_attributes_round_trip(kind):
    """Preserve complete values without creating stray attributes."""

    source = '''```sample {.extra id='figure"part' data-json='{"x":1}' data-note='A &quot;B&quot; &amp; C'}
print("hello")
```'''
    if kind.startswith('pygments'):
        pytest.importorskip('pygments')
    configs = {}
    if kind.startswith('custom') or kind == 'arithmatex':
        configs['pymdownx.superfences'] = {
            'custom_fences': [{
                'name': 'sample',
                'class': 'sample"custom',
                'format': (
                    arithmatex_fenced_format() if kind == 'arithmatex' else
                    fence_code_format if kind == 'custom-code' else fence_div_format
                )
            }]
        }
    elif kind.startswith('js'):
        configs['pymdownx.highlight'] = {
            'use_pygments': False, 'code_attr_on_pre': kind == 'js-pre', 'css_class': 'sample"custom'
        }
    else:
        configs['pymdownx.highlight'] = {'css_class': 'sample"custom'}
        if kind == 'pygments-anchors':
            configs['pymdownx.highlight'].update(
                line_spans='row', line_anchors='line', linenums=True, anchor_linenums=True
            )
    result = markdown.markdown(
        source,
        extensions=['attr_list', 'pymdownx.superfences', 'pymdownx.highlight'],
        extension_configs=configs
    )
    parser = AttributeParser()
    parser.feed(result)
    matches = [attrs for _, attrs in parser.tags if attrs.get('id') == 'figure"part']
    assert len(matches) == 1
    attrs = matches[0]
    assert attrs['data-json'] == '{"x":1}'
    assert attrs['data-note'] == 'A "B" & C'
    assert set(attrs) == {'id', 'class', 'data-json', 'data-note'}
    assert any('sample"custom' in a.get('class', '') for _, a in parser.tags)
    if kind == 'pygments-anchors':
        assert any(a.get('id') == 'row-figure"part-1' for _, a in parser.tags)
        assert any(a.get('id') == 'line-figure"part-1' for _, a in parser.tags)
