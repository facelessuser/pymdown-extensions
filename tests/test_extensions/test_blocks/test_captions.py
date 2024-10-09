"""Test cases for Blocks (caption)."""
from ... import util


class TestBlocksCaption(util.MdCase):
    """Test Blocks caption cases with default configuration."""

    extension = ['pymdownx.blocks.caption', 'md_in_html', 'pymdownx.blocks.html']

    def test_caption(self):
        """Test basic caption."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            This is the caption.
            ///
            ''',
            R'''
            <figure>
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_caption_with_markdown(self):
        """Test caption with markdown."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            This is the **caption**.
            ///
            ''',
            R'''
            <figure>
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>This is the <strong>caption</strong>.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_image_caption(self):
        """Test image caption."""

        self.check_markdown(
            R'''
            ![Alt text](/path/to/img.jpg)
            /// caption
            This is the caption.
            ///
            ''',
            R'''
            <figure>
            <p><img alt="Alt text" src="/path/to/img.jpg" /></p>
            <figcaption>
            <p>This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_nested_caption(self):
        """Test nested caption."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            This is the nested caption.
            ///
            /// caption
            This is the caption.
            ///
            ''',
            R'''
            <figure>
            <figure>
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>This is the nested caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_caption_in_figure_block(self):
        """Test that captions are injected into existing figures."""

        self.check_markdown(
            R"""
            <figure markdown>
            Some content
            </figure>
            /// caption
            Caption.
            ///

            /// html | figure
            Some content
            ///
            /// caption
            Caption.
            ///
            """,
            """
            <figure>
            <p>Some content</p>
            <figcaption>
            <p>Caption.</p>
            </figcaption>
            </figure>
            <figure>
            <p>Some content</p>
            <figcaption>
            <p>Caption.</p>
            </figcaption>
            </figure>
            """,
            True
        )

    def test_caption_not_in_figure_block(self):
        """Test that captions are not injected into existing figures that already have captions."""

        self.check_markdown(
            R"""
            <figure markdown>
            Some content

            <figcaption markdown>
            Existing caption
            </figcaption>

            </figure>
            /// caption
            Caption.
            ///

            /// html | figure
            Some content
            //// html | figcaption
            Existing caption
            ////
            ///
            /// caption
            Caption.
            ///
            """,
            R"""
            <figure>
            <figure>
            <p>Some content</p>
            <figcaption>
            <p>Existing caption</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>Caption.</p>
            </figcaption>
            </figure>
            <figure>
            <figure>
            <p>Some content</p>
            <figcaption>
            <p>Existing caption</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>Caption.</p>
            </figcaption>
            </figure>
            """,
            True
        )


class TestBlocksCaptionAutoid(util.MdCase):
    """Test Blocks caption cases with enabled `autoid`."""

    extension = ['pymdownx.blocks.caption']
    extension_configs = {
        'pymdownx.blocks.caption': {
            'autoid': True
        }
    }

    def test_caption(self):
        """Test basic caption with `autoid`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            This is the caption.
            ///
            ''',
            R'''
            <figure id="__caption_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_consecutive_captions(self):
        """Test consecutive captions with `autoid`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            This is the caption.
            ///

            A paragraph with a caption.
            /// caption
            This is the caption.
            ///
            ''',
            R'''
            <figure id="__caption_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>This is the caption.</p>
            </figcaption>
            </figure>
            <figure id="__caption_2">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_nested_captions(self):
        """Test nested captions with `autoid`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            Level 3 caption.
            ///
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure id="__caption_1">
            <figure id="__caption_1_1">
            <figure id="__caption_1_1_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>Level 3 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>Level 1 caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_nested_consecutive_captions(self):
        """Test nested captions with `autoid`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            Level 3 caption.
            ///
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///

            A paragraph with a caption.
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure id="__caption_1">
            <figure id="__caption_1_1">
            <figure id="__caption_1_1_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>Level 3 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>Level 1 caption.</p>
            </figcaption>
            </figure>
            <figure id="__caption_2">
            <figure id="__caption_2_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>Level 1 caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

class TestBlocksCaptionPrefix(util.MdCase):
    """Test Blocks caption cases with enabled `autoid`."""

    extension = ['pymdownx.blocks.caption', 'md_in_html']
    extension_configs = {
        'pymdownx.blocks.caption': {
            'prefix': '{}. '
        }
    }

    def test_caption(self):
        """Test basic caption with `prefix`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            This is the caption.
            ///
            ''',
            R'''
            <figure>
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>1. This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_consecutive_captions(self):
        """Test consecutive captions with `prefix`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            This is the caption.
            ///

            A paragraph with a caption.
            /// caption
            This is the caption.
            ///
            ''',
            R'''
            <figure>
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>1. This is the caption.</p>
            </figcaption>
            </figure>
            <figure>
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>2. This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_nested_captions(self):
        """Test nested captions with `prefix`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            Level 3 caption.
            ///
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure>
            <figure>
            <figure>
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>1.1.1. Level 3 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>1.1. Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>1. Level 1 caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_nested_consecutive_captions(self):
        """Test nested captions with `prefix`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            Level 3 caption.
            ///
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///

            A paragraph with a caption.
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure>
            <figure>
            <figure>
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>1.1.1. Level 3 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>1.1. Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>1. Level 1 caption.</p>
            </figcaption>
            </figure>
            <figure>
            <figure>
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>2.1. Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>2. Level 1 caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_inject_new_p_in_caption(self):
        """Test `prefix` cases that require the prefix to be injected in a new paragraph."""

        self.check_markdown(
            R"""
            Test
            /// caption
            ///

            Test
            /// caption
            > blockquote
            ///
            """,
            R"""
            <figure>
            <p>Test</p>
            <figcaption><p>1. </p></figcaption>
            </figure>
            <figure>
            <p>Test</p>
            <figcaption>
            <p>2. </p><blockquote>
            <p>blockquote</p>
            </blockquote>
            </figcaption>
            </figure>
            """,
            True
        )

    def test_empty_paragraph(self):
        """Test `prefix` cases that require prefix to inject a new paragraph."""

        self.check_markdown(
            R"""
            Test
            /// caption
            <p markdown></p>
            ///
            """,
            R"""
            <figure>
            <p>Test</p>
            <figcaption>
            <p>1. </p>
            </figcaption>
            </figure>
            """,
            True
        )


class TestBlocksCaptionPrefixLevel(util.MdCase):
    """Test Blocks caption cases with `prefix` level."""

    extension = ['pymdownx.blocks.caption']
    extension_configs = {
        'pymdownx.blocks.caption': {
            'prefix': '{}. ',
            'prefix_level': 2
        }
    }

    def test_caption(self):
        """Test basic caption with `prefix` level."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            This is the caption.
            ///
            ''',
            R'''
            <figure>
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>1. This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_nested_captions(self):
        """Test nested captions with `prefix` level."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            Level 3 caption.
            ///
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure>
            <figure>
            <figure>
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>Level 3 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>1.1. Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>1. Level 1 caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_nested_consecutive_captions(self):
        """Test nested consecutive captions with `prefix` level."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            Level 3 caption.
            ///
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///

            A paragraph with a caption.
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure>
            <figure>
            <figure>
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>Level 3 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>1.1. Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>1. Level 1 caption.</p>
            </figcaption>
            </figure>
            <figure>
            <figure>
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>2.1. Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>2. Level 1 caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

class TestBlocksCaptionAutoidPrefixLevel(util.MdCase):
    """Test Blocks caption cases with enabled `autoid` and `prefix`."""

    extension = ['pymdownx.blocks.caption']
    extension_configs = {
        'pymdownx.blocks.caption': {
            'autoid': True,
            'prefix': '{}. ',
            'prefix_level': 2
        }
    }

    def test_caption(self):
        """Test basic caption with `autoid` and `prefix`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            This is the caption.
            ///
            ''',
            R'''
            <figure id="__caption_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>1. This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_consecutive_captions(self):
        """Test consecutive captions with `autoid` and `prefix`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            This is the caption.
            ///

            A paragraph with a caption.
            /// caption
            This is the caption.
            ///
            ''',
            R'''
            <figure id="__caption_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>1. This is the caption.</p>
            </figcaption>
            </figure>
            <figure id="__caption_2">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>2. This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_nested_captions(self):
        """Test nested captions with `autoid` and `prefix`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            Level 3 caption.
            ///
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure id="__caption_1">
            <figure id="__caption_1_1">
            <figure id="__caption_1_1_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>Level 3 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>1.1. Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>1. Level 1 caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_nested_consecutive_captions(self):
        """Test nested consecutive captions with `autoid` and `prefix`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            Level 3 caption.
            ///
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///

            A paragraph with a caption.
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure id="__caption_1">
            <figure id="__caption_1_1">
            <figure id="__caption_1_1_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>Level 3 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>1.1. Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>1. Level 1 caption.</p>
            </figcaption>
            </figure>
            <figure id="__caption_2">
            <figure id="__caption_2_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>2.1. Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>2. Level 1 caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )


class TestBlocksCaptionPrefixLevelPrepend(util.MdCase):
    """Test Blocks caption cases with `prefix` level."""

    extension = ['pymdownx.blocks.caption']
    extension_configs = {
        'pymdownx.blocks.caption': {
            'prefix': '{}. ',
            'prefix_level': 2,
            'prepend': True
        }
    }

    def test_caption(self):
        """Test basic caption with `prefix` level and `prepend`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            This is the caption.
            ///
            ''',
            R'''
            <figure>
            <figcaption>
            <p>1. This is the caption.</p>
            </figcaption>
            <p>A paragraph with a caption.</p>
            </figure>
            ''',
            True
        )

    def test_nested_captions(self):
        """Test nested captions with `prefix` level and `prepend`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            Level 3 caption.
            ///
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure>
            <figcaption>
            <p>1. Level 1 caption.</p>
            </figcaption>
            <figure>
            <figcaption>
            <p>1.1. Level 2 caption.</p>
            </figcaption>
            <figure>
            <figcaption>
            <p>Level 3 caption.</p>
            </figcaption>
            <p>A paragraph with a caption.</p>
            </figure>
            </figure>
            </figure>
            ''',
            True
        )

    def test_nested_consecutive_captions(self):
        """Test nested consecutive captions with `prefix` level and `prepend`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            Level 3 caption.
            ///
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///

            A paragraph with a caption.
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure>
            <figcaption>
            <p>1. Level 1 caption.</p>
            </figcaption>
            <figure>
            <figcaption>
            <p>1.1. Level 2 caption.</p>
            </figcaption>
            <figure>
            <figcaption>
            <p>Level 3 caption.</p>
            </figcaption>
            <p>A paragraph with a caption.</p>
            </figure>
            </figure>
            </figure>
            <figure>
            <figcaption>
            <p>2. Level 1 caption.</p>
            </figcaption>
            <figure>
            <figcaption>
            <p>2.1. Level 2 caption.</p>
            </figcaption>
            <p>A paragraph with a caption.</p>
            </figure>
            </figure>
            ''',
            True
        )

class TestBlocksCaptionAutoidPrefixLevelPrepend(util.MdCase):
    """Test Blocks caption cases with enabled `autoid` and `prefix`."""

    extension = ['pymdownx.blocks.caption']
    extension_configs = {
        'pymdownx.blocks.caption': {
            'autoid': True,
            'prefix': '{}. ',
            'prefix_level': 2,
            'prepend': True
        }
    }

    def test_caption(self):
        """Test basic caption with `autoid` and `prefix`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            This is the caption.
            ///
            ''',
            R'''
            <figure id="__caption_1">
            <figcaption>
            <p>1. This is the caption.</p>
            </figcaption>
            <p>A paragraph with a caption.</p>
            </figure>
            ''',
            True
        )

    def test_consecutive_captions(self):
        """Test consecutive captions with `autoid` and `prefix`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            This is the caption.
            ///

            A paragraph with a caption.
            /// caption
            This is the caption.
            ///
            ''',
            R'''
            <figure id="__caption_1">
            <figcaption>
            <p>1. This is the caption.</p>
            </figcaption>
            <p>A paragraph with a caption.</p>
            </figure>
            <figure id="__caption_2">
            <figcaption>
            <p>2. This is the caption.</p>
            </figcaption>
            <p>A paragraph with a caption.</p>
            </figure>
            ''',
            True
        )

    def test_nested_captions(self):
        """Test nested captions with `autoid` and `prefix`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            Level 3 caption.
            ///
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure id="__caption_1">
            <figcaption>
            <p>1. Level 1 caption.</p>
            </figcaption>
            <figure id="__caption_1_1">
            <figcaption>
            <p>1.1. Level 2 caption.</p>
            </figcaption>
            <figure id="__caption_1_1_1">
            <figcaption>
            <p>Level 3 caption.</p>
            </figcaption>
            <p>A paragraph with a caption.</p>
            </figure>
            </figure>
            </figure>
            ''',
            True
        )

    def test_nested_consecutive_captions(self):
        """Test nested consecutive captions with `autoid` and `prefix`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            Level 3 caption.
            ///
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///

            A paragraph with a caption.
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure id="__caption_1">
            <figcaption>
            <p>1. Level 1 caption.</p>
            </figcaption>
            <figure id="__caption_1_1">
            <figcaption>
            <p>1.1. Level 2 caption.</p>
            </figcaption>
            <figure id="__caption_1_1_1">
            <figcaption>
            <p>Level 3 caption.</p>
            </figcaption>
            <p>A paragraph with a caption.</p>
            </figure>
            </figure>
            </figure>
            <figure id="__caption_2">
            <figcaption>
            <p>2. Level 1 caption.</p>
            </figcaption>
            <figure id="__caption_2_1">
            <figcaption>
            <p>2.1. Level 2 caption.</p>
            </figcaption>
            <p>A paragraph with a caption.</p>
            </figure>
            </figure>
            ''',
            True
        )

    def test_nested_captions_manual_id(self):
        """Test nested captions with `autoid` and `prefix` with manual IDs."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// caption
            Level 4 caption.
            ///
            /// caption
                attrs:
                  id: test
            Level 3 caption.
            ///
            /// caption
            Level 2 caption.
            ///
            /// caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure id="__caption_1">
            <figcaption>
            <p>1. Level 1 caption.</p>
            </figcaption>
            <figure id="__caption_1_1">
            <figcaption>
            <p>1.1. Level 2 caption.</p>
            </figcaption>
            <figure id="test">
            <figcaption>
            <p>Level 3 caption.</p>
            </figcaption>
            <figure>
            <figcaption>
            <p>Level 4 caption.</p>
            </figcaption>
            <p>A paragraph with a caption.</p>
            </figure>
            </figure>
            </figure>
            </figure>
            ''',
            True
        )
