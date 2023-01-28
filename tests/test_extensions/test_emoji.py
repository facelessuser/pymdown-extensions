"""Test cases for Highlight."""
from .. import util
import pymdownx.emoji as emoji
import warnings
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

    def test_old_index(self):
        """Test that index works."""

        self.check_markdown(
            ':smile:',
            '<p><img alt="\U0001f604" class="twemoji" src="https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/1f604.png" title=":smile:" /></p>'  # noqa: E501
        )

    def test_warning(self):
        """Test that warning is raising."""

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            markdown.Markdown(
                extensions=self.extension,
                extension_configs=self.extension_configs
            ).convert(':smile:')

            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, DeprecationWarning))


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
            '<p><img alt="\U0001f604" class="twemoji" src="https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/1f604.png" title=":grin:" /></p>'  # noqa: E501
        )
