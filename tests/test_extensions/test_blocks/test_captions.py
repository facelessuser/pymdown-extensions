"""Test cases for Blocks (caption)."""
from ... import util


class TestBlocksCaption(util.MdCase):
    """Test Blocks caption cases with default configuration."""

    extension = ['pymdownx.blocks.caption']

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

class TestBlocksCaptionAutoid(util.MdCase):
    """Test Blocks caption cases with enabled `autoid`."""

    extension = ['pymdownx.blocks.caption']
    extension_configs = {
        'pymdownx.blocks.caption': {
            'autoid': True
        }
    }

    def test_caption(self):
        """Test basic caption with autoid."""

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
        """Test consecutive captions with autoid."""

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
        """Test nested captions with autoid."""

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
        """Test nested captions with autoid."""

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
            ''',
            True
        )

class TestBlocksCaptionPrefix(util.MdCase):
    """Test Blocks caption cases with enabled `autoid`."""

    extension = ['pymdownx.blocks.caption']
    extension_configs = {
        'pymdownx.blocks.caption': {
            'prefix': '{}. '
        }
    }

    def test_caption(self):
        """Test basic caption with prefix."""

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
        """Test consecutive captions with prefix."""

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
        """Test nested captions with prefix."""

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
        """Test nested captions with prefix."""

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
            ''',
            True
        )
