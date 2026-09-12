"""Test cases for Highlight."""
from .. import util
import pymdownx.emoji as emoji
import markdown
import textwrap
from pymdownx.emoji import EMOJIONE_PNG_CDN, TWEMOJI_PNG_CDN


def _new_style_index(options, md):
    """Custom index with arguments (new style)."""

    index = emoji.twemoji({}, None)

    if 'append_alias' in options:
        for alias, original in options['append_alias']:
            index['aliases'][alias] = original

    return index


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
            f'<p><img alt="\U0001f604" class="twemoji" src="{TWEMOJI_PNG_CDN}1f604.png" title=":grin:" /></p>'
        )


class TestEmojiStrict(util.MdCase):
    """Test strict mode."""

    def test_strict(self):
        """Test strict mode."""

        MD1 = ":apple:"

        MD2 = ":apple:\n:bad:\n:whatever:\n\n:yep:\n"

        extension_configs = {
            'pymdownx.emoji': {
                'strict': True
            }
        }

        extensions = ['pymdownx.emoji']
        md = markdown.Markdown(extensions=extensions, extension_configs=extension_configs)
        self.assertEqual(
            md.convert(MD1),
            f"""<p><img alt="🍎" class="emojione" src="{EMOJIONE_PNG_CDN}1f34e.png" title=":apple:" /></p>"""
        )
        md.reset()
        error = ""
        try:
            md.convert(MD2)
        except RuntimeError as e:
            error = str(e)
        self.assertEqual(
            error,
            textwrap.dedent(
                """
                Emoji Extension (strict mode): The following emoji were detected and either had
                their name change, were removed, or have never existed.

                - :bad:
                - :whatever:
                - :yep:
                """
            )
        )

        md.reset()
        self.assertEqual(
            md.convert(MD1),
            f"""<p><img alt="🍎" class="emojione" src="{EMOJIONE_PNG_CDN}1f34e.png" title=":apple:" /></p>"""
        )
