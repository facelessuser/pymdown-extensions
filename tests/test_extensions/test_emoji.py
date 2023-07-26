"""Test cases for Highlight."""
from .. import util
import pytest
import pymdownx.emoji as emoji
import markdown


def _old_style_index():
    """Custom index with no arguments (old style)."""

    return emoji.twemoji({}, None)


def _new_style_index(options, md):
    """Custom index with arguments (new style)."""

    index = emoji.twemoji({}, None)

    if 'append_alias' in options:
        for alias, original in options['append_alias']:
            index['aliases'][alias] = original

    return index


class TestEmojiOldIndex(util.MdCase):
    """Test old style index."""

    extension = [
        'pymdownx.emoji'
    ]
    extension_configs = {
        'pymdownx.emoji': {
            'emoji_index': _old_style_index
        }
    }

    @pytest.mark.filterwarnings("ignore")
    def test_old_index(self):
        """Test that index works."""

        with pytest.warns(DeprecationWarning):
            self.assertEqual(
                markdown.Markdown(
                    extensions=self.extension,
                    extension_configs=self.extension_configs
                ).convert(':smile:'),
                '<p><img alt="\U0001f604" class="twemoji" src="https://cdn.jsdelivr.net/gh/jdecked/twemoji@14.1.2/assets/72x72/1f604.png" title=":smile:" /></p>'  # noqa: E501
            )


class TestEmojiNewIndex(util.MdCase):
    """Test new style index."""

    extension = [
        'pymdownx.emoji'
    ]
    extension_configs = {
        'pymdownx.emoji': {
            'emoji_index': _new_style_index,
            'options': {'append_alias': [(':grin:', ":smile:")]}
        }
    }

    def test_new_index(self):
        """Test that we can pass options using the new style."""

        self.check_markdown(
            ':grin:',
            '<p><img alt="\U0001f604" class="twemoji" src="https://cdn.jsdelivr.net/gh/jdecked/twemoji@14.1.2/assets/72x72/1f604.png" title=":grin:" /></p>'  # noqa: E501
        )
