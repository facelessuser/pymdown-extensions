"""Test cases for Blocks (caption)."""
from ... import util


class TestBlocksCaption(util.MdCase):
    """Test Blocks caption cases with default configuration."""

    extension = ['pymdownx.blocks.caption', 'md_in_html', 'pymdownx.blocks.html']
    extension_configs = {
        'pymdownx.blocks.caption': {
            'auto': False
        }
    }

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

    def test_manual_prepend(self):
        """Test manual prepend."""

        self.check_markdown(
            R"""
            Text
            /// caption | <
            Prepended
            ///

            Text
            /// caption | >
            Appended
            ///
            """,
            R"""
            <figure>
            <figcaption>
            <p>Prepended</p>
            </figcaption>
            <p>Text</p>
            </figure>
            <figure>
            <p>Text</p>
            <figcaption>
            <p>Appended</p>
            </figcaption>
            </figure>
            """,
            True
        )

    def test_caption_inline_id(self):
        """Test caption with inline shorthand ID."""

        self.check_markdown(
            R'''
            Paragraph
            /// figure-caption | #custom-id
            Caption text.
            ///
            ''',
            R'''
            <figure id="custom-id">
            <p>Paragraph</p>
            <figcaption>
            <p>Caption text.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_caption_inline_id_prepend(self):
        """Test caption with inline shorthand ID and prepend marker."""

        self.check_markdown(
            R'''
            Text
            /// figure-caption | < #custom-prepend
            Prepended caption.
            ///
            ''',
            R'''
            <figure id="custom-prepend">
            <figcaption>
            <p>Prepended caption.</p>
            </figcaption>
            <p>Text</p>
            </figure>
            ''',
            True
        )

    def test_caption_inline_id_with_extra_token(self):
        """Ensure inline shorthand ID with extra tokens is rejected."""

        self.check_markdown(
            R"""
            Paragraph
            /// figure-caption | #custom-id extra
            Caption text.
            ///
            """,
            """
            <p>Paragraph
            /// figure-caption | #custom-id extra
            Caption text.
            ///</p>
            """,
            True
        )

    def test_caption_inline_id_invalid_identifier(self):
        """Ensure inline shorthand ID with invalid characters is rejected."""

        self.check_markdown(
            R"""
            Paragraph
            /// figure-caption | #invalid!
            Caption text.
            ///
            """,
            """
            <p>Paragraph
            /// figure-caption | #invalid!
            Caption text.
            ///</p>
            """,
            True
        )

    def test_table_caption_inline_id(self):
        """Test table caption with inline shorthand ID."""

        self.check_markdown(
            R'''
            Paragraph
            /// table-caption | #custom-table
            Table caption text.
            ///
            ''',
            R'''
            <figure id="custom-table">
            <p>Paragraph</p>
            <figcaption>
            <p>Table caption text.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_table_caption_multiple_inline_id_not_allowed(self):
        """Ensure multiple inline shorthand IDs are rejected."""

        self.check_markdown(
            R"""
            Paragraph
            /// table-caption | #id1 #id2
            Table caption text.
            ///
            """,
            """
            <p>Paragraph
            /// table-caption | #id1 #id2
            Table caption text.
            ///</p>
            """,
            True
        )

    def test_caption_inline_id_attribute_override(self):
        """Ensure inline shorthand ID does not override attribute-defined ID."""

        self.check_markdown(
            R'''
            Paragraph
            /// figure-caption | #inline-id
                attrs: {id: attribute-id}
            Caption text.
            ///
            ''',
            R'''
            <figure id="attribute-id">
            <p>Paragraph</p>
            <figcaption>
            <p>Caption text.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_caption_inline_class(self):
        """Test caption with inline shorthand class."""

        self.check_markdown(
            R'''
            Paragraph
            /// figure-caption | .custom-class
            Caption text.
            ///
            ''',
            R'''
            <figure class="custom-class">
            <p>Paragraph</p>
            <figcaption>
            <p>Caption text.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_caption_multiple_inline_class(self):
        """Test caption with multiple inline shorthand class."""

        self.check_markdown(
            R'''
            Paragraph
            /// figure-caption | .custom-class1 .custom-class2
            Caption text.
            ///
            ''',
            R'''
            <figure class="custom-class1 custom-class2">
            <p>Paragraph</p>
            <figcaption>
            <p>Caption text.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_caption_inline_class_and_id(self):
        """Test caption with inline shorthand class and id."""

        self.check_markdown(
            R'''
            Paragraph
            /// figure-caption | .custom-class #custom-id
            Caption text.
            ///
            ''',
            R'''
            <figure class="custom-class" id="custom-id">
            <p>Paragraph</p>
            <figcaption>
            <p>Caption text.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_caption_inline_class_attribute_override(self):
        """Ensure inline shorthand class does not override attribute-defined class."""

        self.check_markdown(
            R'''
            Paragraph
            /// figure-caption | .inline-class
                attrs: {class: attribute-class}
            Caption text.
            ///
            ''',
            R'''
            <figure class="attribute-class">
            <p>Paragraph</p>
            <figcaption>
            <p>Caption text.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_bad_header(self):
        """Test a bad header."""

        self.check_markdown(
            R"""
            Test
            /// caption | bad
            ///
            """,
            """
            <p>Test
            /// caption | bad
            ///</p>
            """,
            True
        )


class TestBlocksCaptionClass(util.MdCase):
    """Test caption classes."""

    extension = ['pymdownx.blocks.caption', 'md_in_html', 'pymdownx.blocks.html']
    extension_configs = {
        'pymdownx.blocks.caption': {
            'types': [
                {"name": "figure-class", "classes": "class1 class2"}
            ]
        }
    }

    def test_class_insertion(self):
        """Test class insertion."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-class
            This is the caption.
            ///
            ''',
            R'''
            <figure class="class1 class2">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_class_insertion_existing_figure(self):
        """Test class insertion on existing figure."""

        self.check_markdown(
            R'''
            /// html | figure
            A paragraph with a caption.
            ///
            /// figure-class
            This is the caption.
            ///
            ''',
            R'''
            <figure class="class1 class2">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_class_insertion_existing_class(self):
        """Test class insertion on existing figure with existing class."""

        self.check_markdown(
            R'''
            /// html | figure.class1
            A paragraph with a caption.
            ///
            /// figure-class
            This is the caption.
            ///
            ''',
            R'''
            <figure class="class1 class2">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )


class TestBlocksCaptionPrefix(util.MdCase):
    """Test Blocks caption cases with enabled `auto`."""

    extension = ['pymdownx.blocks.caption', 'md_in_html']
    extension_configs = {
        'pymdownx.blocks.caption': {
            'auto': False
        }
    }

    def test_caption(self):
        """Test basic caption with `auto`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption | 1
            This is the caption.
            ///
            ''',
            R'''
            <figure id="__figure-caption_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_consecutive_captions(self):
        """Test consecutive captions with `auto`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption | 1
            This is the caption.
            ///

            A paragraph with a caption.
            /// figure-caption | 2
            This is the caption.
            ///
            ''',
            R'''
            <figure id="__figure-caption_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> This is the caption.</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_2">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 2.</span> This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_nested_captions(self):
        """Test nested captions with `auto`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption | 1.1.1
            Level 3 caption.
            ///
            /// figure-caption | 1.1
            Level 2 caption.
            ///
            /// figure-caption | 1
            Level 1 caption.
            ///
            ''',
            R'''
            <figure id="__figure-caption_1">
            <figure id="__figure-caption_1_1">
            <figure id="__figure-caption_1_1_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.1.</span> Level 3 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.</span> Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> Level 1 caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_nested_consecutive_captions(self):
        """Test nested captions with `auto`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption | 1.1.1
            Level 3 caption.
            ///
            /// figure-caption | 1.1
            Level 2 caption.
            ///
            /// figure-caption | 1
            Level 1 caption.
            ///

            A paragraph with a caption.
            /// figure-caption | 2.1
            Level 2 caption.
            ///
            /// figure-caption | 2
            Level 1 caption.
            ///
            ''',
            R'''
            <figure id="__figure-caption_1">
            <figure id="__figure-caption_1_1">
            <figure id="__figure-caption_1_1_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.1.</span> Level 3 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.</span> Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> Level 1 caption.</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_2">
            <figure id="__figure-caption_2_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 2.1.</span> Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 2.</span> Level 1 caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_caption_inline_id(self):
        """Test caption with inline shorthand ID."""

        self.check_markdown(
            R'''
            Paragraph
            /// figure-caption | #custom-id
            Caption text.
            ///
            ''',
            R'''
            <figure id="custom-id">
            <p>Paragraph</p>
            <figcaption>
            <p>Caption text.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_caption_inline_id_prepend(self):
        """Test caption with inline shorthand ID and prepend marker."""

        self.check_markdown(
            R'''
            Text
            /// figure-caption | < #custom-prepend
            Prepended caption.
            ///
            ''',
            R'''
            <figure id="custom-prepend">
            <figcaption>
            <p>Prepended caption.</p>
            </figcaption>
            <p>Text</p>
            </figure>
            ''',
            True
        )

    def test_inject_new_p_in_caption(self):
        """Test `auto` cases that require the prefix to be injected in a new paragraph."""

        self.check_markdown(
            R"""
            Test
            /// figure-caption | 1
            ///

            Test
            /// figure-caption | 2
            > blockquote
            ///
            """,
            R"""
            <figure id="__figure-caption_1">
            <p>Test</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span></p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_2">
            <p>Test</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 2.</span></p>
            <blockquote>
            <p>blockquote</p>
            </blockquote>
            </figcaption>
            </figure>
            """,
            True
        )

    def test_empty_paragraph(self):
        """Test `auto` cases that require prefix to inject a new paragraph."""

        self.check_markdown(
            R"""
            Test
            /// figure-caption | 1
            <p markdown></p>
            ///
            """,
            R"""
            <figure id="__figure-caption_1">
            <p>Test</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span></p>
            </figcaption>
            </figure>
            """,
            True
        )

    def test_manual_prepend(self):
        """Test manual prepend."""

        self.check_markdown(
            R"""
            Text
            /// figure-caption | < 2
            Prepended
            ///

            Text
            /// figure-caption | > 5
            Appended
            ///
            """,
            R"""
            <figure id="__figure-caption_2">
            <figcaption>
            <p><span class="caption-prefix">Figure 2.</span> Prepended</p>
            </figcaption>
            <p>Text</p>
            </figure>
            <figure id="__figure-caption_5">
            <p>Text</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 5.</span> Appended</p>
            </figcaption>
            </figure>
            """,
            True
        )

    def test_depth(self):
        """Depth is not really supported in manual, so a generic response is expected."""

        self.check_markdown(
            R"""
            Paragraph
            /// figure-caption
            Caption 1
            ///

            Paragraph
            /// figure-caption | ^1
            Caption 1.1
            ///

            Paragraph
            /// figure-caption | ^2
            Caption 1.1.1
            ///

            Paragraph
            /// figure-caption | ^3
            Caption 1.1.1.1
            ///
            """,
            """
            <figure>
            <p>Paragraph</p>
            <figcaption>
            <p>Caption 1</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_1_1">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.</span> Caption 1.1</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_1_1_1">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.1.</span> Caption 1.1.1</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_1_1_1_1">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.1.1.</span> Caption 1.1.1.1</p>
            </figcaption>
            </figure>
            """,
            True
        )


class TestBlocksCaptionAutoPrefix(util.MdCase):
    """Test Blocks caption cases with enabled `auto`."""

    extension = ['pymdownx.blocks.caption', 'md_in_html']
    extension_configs = {
        'pymdownx.blocks.caption': {
        }
    }

    def test_caption_number_and_id(self):
        """Test captions with IDs and number."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption | 3 #id
            This is the caption.
            ///

            A paragraph with a caption.
            /// figure-caption | < 4 #id2
            This is the caption.
            ///
            ''',
            R'''
            <figure id="id">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 3.</span> This is the caption.</p>
            </figcaption>
            </figure>
            <figure id="id2">
            <figcaption>
            <p><span class="caption-prefix">Figure 4.</span> This is the caption.</p>
            </figcaption>
            <p>A paragraph with a caption.</p>
            </figure>
            ''',
            True
        )

    def test_caption(self):
        """Test basic caption with `auto`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption
            This is the caption.
            ///
            ''',
            R'''
            <figure id="__figure-caption_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_consecutive_captions(self):
        """Test consecutive captions with `auto`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption
            This is the caption.
            ///

            A paragraph with a caption.
            /// figure-caption
            This is the caption.
            ///
            ''',
            R'''
            <figure id="__figure-caption_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> This is the caption.</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_2">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 2.</span> This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_nested_captions(self):
        """Test nested captions with `auto`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption
            Level 3 caption.
            ///
            /// figure-caption
            Level 2 caption.
            ///
            /// figure-caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure id="__figure-caption_1">
            <figure id="__figure-caption_1_1">
            <figure id="__figure-caption_1_1_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.1.</span> Level 3 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.</span> Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> Level 1 caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_nested_consecutive_captions(self):
        """Test nested captions with `auto`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption
            Level 3 caption.
            ///
            /// figure-caption
            Level 2 caption.
            ///
            /// figure-caption
            Level 1 caption.
            ///

            A paragraph with a caption.
            /// figure-caption
            Level 2 caption.
            ///
            /// figure-caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure id="__figure-caption_1">
            <figure id="__figure-caption_1_1">
            <figure id="__figure-caption_1_1_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.1.</span> Level 3 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.</span> Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> Level 1 caption.</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_2">
            <figure id="__figure-caption_2_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 2.1.</span> Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 2.</span> Level 1 caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_manual_prepend(self):
        """Test manual prepend."""

        self.check_markdown(
            R"""
            Text
            /// figure-caption | < 2
            Prepended and number ignored
            ///

            Text
            /// figure-caption | >
            Appended
            ///
            """,
            R"""
            <figure id="__figure-caption_2">
            <figcaption>
            <p><span class="caption-prefix">Figure 2.</span> Prepended and number ignored</p>
            </figcaption>
            <p>Text</p>
            </figure>
            <figure id="__figure-caption_3">
            <p>Text</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 3.</span> Appended</p>
            </figcaption>
            </figure>
            """,
            True
        )

    def test_mixed_captions(self):
        """Test mixed captions with `auto`."""

        self.check_markdown(
            R'''
            Paragraph
            /// caption
            Not numbered
            ///

            Paragraph
            /// figure-caption
            Numbered level 2 caption.
            ///
            /// caption
            Not numbered level 1.
            ///
            /// figure-caption
            Numbered level 1 caption.
            ///
            ''',
            R'''
            <figure>
            <p>Paragraph</p>
            <figcaption>
            <p>Not numbered</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_1">
            <figure>
            <figure id="__figure-caption_1_1">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.</span> Numbered level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p>Not numbered level 1.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> Numbered level 1 caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_existing_fig_caption(self):
        """Test when a figure has a figure caption and we don't know what type it is."""

        self.check_markdown(
            R"""
            <figure markdown>
            Some text.
            <figcaption markdown>
            Caption.
            </figcaption>
            </figure>
            """,
            R"""
            <figure>
            <p>Some text.</p>
            <figcaption>
            <p>Caption.</p>
            </figcaption>
            </figure>
            """,
            True
        )

    def test_inject_new_p_in_caption(self):
        """Test `auto` cases that require the prefix to be injected in a new paragraph."""

        self.check_markdown(
            R"""
            Test
            /// figure-caption
            ///

            Test
            /// figure-caption
            > blockquote
            ///
            """,
            R"""
            <figure id="__figure-caption_1">
            <p>Test</p>
            <figcaption><p><span class="caption-prefix">Figure 1.</span></p></figcaption>
            </figure>
            <figure id="__figure-caption_2">
            <p>Test</p>
            <figcaption><p><span class="caption-prefix">Figure 2.</span></p>
            <blockquote>
            <p>blockquote</p>
            </blockquote>
            </figcaption>
            </figure>
            """,
            True
        )

    def test_empty_paragraph(self):
        """Test `auto` cases that require prefix to inject a new paragraph."""

        self.check_markdown(
            R"""
            Test
            /// figure-caption
            <p markdown></p>
            ///
            """,
            R"""
            <figure id="__figure-caption_1">
            <p>Test</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span></p>
            </figcaption>
            </figure>
            """,
            True
        )

    def test_nested_captions_manual_id(self):
        """Test nested captions with `auto` and `auto` with manual IDs."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption
            Level 4 caption.
            ///
            /// figure-caption
                attrs: {id: test}
            Level 3 caption.
            ///
            /// figure-caption
            Level 2 caption.
            ///
            /// figure-caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure id="__figure-caption_1">
            <figure id="__figure-caption_1_1">
            <figure id="test">
            <figure id="__figure-caption_1_1_1_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.1.1.</span> Level 4 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.1.</span> Level 3 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.</span> Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> Level 1 caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_depth(self):
        """Test level depth."""

        self.check_markdown(
            R"""
            Paragraph
            /// figure-caption
            Caption 1
            ///

            Paragraph
            /// figure-caption
            Caption 1.1.1
            ///

            /// figure-caption | ^1
            Caption 1.1
            ///

            Paragraph
            /// figure-caption | ^1
            Caption 2.1
            ///

            /// figure-caption
            Caption 2
            ///
            """,
            """
            <figure id="__figure-caption_1">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> Caption 1</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_1_1">
            <figure id="__figure-caption_1_1_1">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.1.</span> Caption 1.1.1</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.</span> Caption 1.1</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_2">
            <figure id="__figure-caption_2_1_1">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 2.1.1.</span> Caption 2.1</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 2.</span> Caption 2</p>
            </figcaption>
            </figure>
            """,
            True
        )

    def test_manual_number(self):
        """Test manual number."""

        self.check_markdown(
            R"""
            Paragraph
            /// figure-caption
            Caption 4.2.1
            ///

            /// figure-caption | 4.2
            Caption 4.2
            ///


            Paragraph
            /// figure-caption
            Caption 5.2.1
            ///

            /// figure-caption | 5.2
            Caption 5.2
            ///

            /// figure-caption
            Caption 5
            ///
            """,
            """
            <figure id="__figure-caption_4_2">
            <figure id="__figure-caption_4_2_1">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 4.2.1.</span> Caption 4.2.1</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 4.2.</span> Caption 4.2</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_5">
            <figure id="__figure-caption_5_2">
            <figure id="__figure-caption_5_2_1">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 5.2.1.</span> Caption 5.2.1</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 5.2.</span> Caption 5.2</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 5.</span> Caption 5</p>
            </figcaption>
            </figure>
            """,
            True
        )


    def test_manual_number_increment_levels(self):
        """Test that forced levels and manual numbers with auto works."""

        self.check_markdown(
            R"""
            Paragraph
            /// figure-caption | 1.1
            Caption 1.1
            ///

            Paragraph
            /// figure-caption | ^1
            Caption 1.2
            ///

            Paragraph
            /// figure-caption | 2.1
            Caption 2.1
            ///

            Paragraph
            /// figure-caption | ^1
            Caption 2.2
            ///
            """,
            """
            <figure id="__figure-caption_1_1">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.</span> Caption 1.1</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_1_2">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.2.</span> Caption 1.2</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_2_1">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 2.1.</span> Caption 2.1</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_2_2">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 2.2.</span> Caption 2.2</p>
            </figcaption>
            </figure>
            """,
            True
        )


class TestBlocksCaptionAutoLevel(util.MdCase):
    """Test Blocks caption cases with `auto` level."""

    extension = ['pymdownx.blocks.caption']
    extension_configs = {
        'pymdownx.blocks.caption': {
            'auto_level': 2
        }
    }

    def test_caption(self):
        """Test basic caption with `auto` level."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption
            This is the caption.
            ///
            ''',
            R'''
            <figure id="__figure-caption_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_nested_captions(self):
        """Test nested captions with `auto` level."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption
            Level 3 caption.
            ///
            /// figure-caption
            Level 2 caption.
            ///
            /// figure-caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure id="__figure-caption_1">
            <figure id="__figure-caption_1_1">
            <figure>
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>Level 3 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.</span> Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> Level 1 caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_nested_consecutive_captions(self):
        """Test nested consecutive captions with `auto` level."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption
            Level 3 caption.
            ///
            /// figure-caption
            Level 2 caption.
            ///
            /// figure-caption
            Level 1 caption.
            ///

            A paragraph with a caption.
            /// figure-caption
            Level 2 caption.
            ///
            /// figure-caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure id="__figure-caption_1">
            <figure id="__figure-caption_1_1">
            <figure>
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p>Level 3 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.</span> Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> Level 1 caption.</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_2">
            <figure id="__figure-caption_2_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 2.1.</span> Level 2 caption.</p>
            </figcaption>
            </figure>
            <figcaption>
            <p><span class="caption-prefix">Figure 2.</span> Level 1 caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )

    def test_depth(self):
        """Test depth with auto level limit."""

        self.check_markdown(
            R"""
            Paragraph
            /// figure-caption
            Caption 1
            ///

            Paragraph
            /// figure-caption | ^1
            Caption 1.1
            ///

            Paragraph
            /// figure-caption | ^2
            Caption None
            ///
            """,
            """
            <figure id="__figure-caption_1">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> Caption 1</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_1_1">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.</span> Caption 1.1</p>
            </figcaption>
            </figure>
            <figure>
            <p>Paragraph</p>
            <figcaption>
            <p>Caption None</p>
            </figcaption>
            </figure>
            """,
            True
        )

    def test_manual_numbers(self):
        """Test manual numbers with auto level limit."""

        self.check_markdown(
            R"""
            Paragraph
            /// figure-caption | 1
            Caption 1
            ///

            Paragraph
            /// figure-caption | 2.3
            Caption 2.3
            ///

            Paragraph
            /// figure-caption | 4.3.1
            Caption None
            ///
            """,
            """
            <figure id="__figure-caption_1">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> Caption 1</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_2_3">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 2.3.</span> Caption 2.3</p>
            </figcaption>
            </figure>
            <figure id="__figure-caption_4_3_1">
            <p>Paragraph</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 4.3.1.</span> Caption None</p>
            </figcaption>
            </figure>
            """,
            True
        )


class TestBlocksCaptionAutoLevelPrepend(util.MdCase):
    """Test Blocks caption cases with `auto` level."""

    extension = ['pymdownx.blocks.caption']
    extension_configs = {
        'pymdownx.blocks.caption': {
            'auto_level': 2,
            'prepend': True
        }
    }

    def test_caption(self):
        """Test basic caption with `auto` level and `prepend`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption
            This is the caption.
            ///
            ''',
            R'''
            <figure id="__figure-caption_1">
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> This is the caption.</p>
            </figcaption>
            <p>A paragraph with a caption.</p>
            </figure>
            ''',
            True
        )

    def test_nested_captions(self):
        """Test nested captions with `auto` level and `prepend`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption
            Level 3 caption.
            ///
            /// figure-caption
            Level 2 caption.
            ///
            /// figure-caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure id="__figure-caption_1">
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> Level 1 caption.</p>
            </figcaption>
            <figure id="__figure-caption_1_1">
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.</span> Level 2 caption.</p>
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
        """Test nested consecutive captions with `auto` level and `prepend`."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption
            Level 3 caption.
            ///
            /// figure-caption
            Level 2 caption.
            ///
            /// figure-caption
            Level 1 caption.
            ///

            A paragraph with a caption.
            /// figure-caption
            Level 2 caption.
            ///
            /// figure-caption
            Level 1 caption.
            ///
            ''',
            R'''
            <figure id="__figure-caption_1">
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> Level 1 caption.</p>
            </figcaption>
            <figure id="__figure-caption_1_1">
            <figcaption>
            <p><span class="caption-prefix">Figure 1.1.</span> Level 2 caption.</p>
            </figcaption>
            <figure>
            <figcaption>
            <p>Level 3 caption.</p>
            </figcaption>
            <p>A paragraph with a caption.</p>
            </figure>
            </figure>
            </figure>
            <figure id="__figure-caption_2">
            <figcaption>
            <p><span class="caption-prefix">Figure 2.</span> Level 1 caption.</p>
            </figcaption>
            <figure id="__figure-caption_2_1">
            <figcaption>
            <p><span class="caption-prefix">Figure 2.1.</span> Level 2 caption.</p>
            </figcaption>
            <p>A paragraph with a caption.</p>
            </figure>
            </figure>
            ''',
            True
        )

    def test_manual_prepend(self):
        """Test manual prepend."""

        self.check_markdown(
            R"""
            Text
            /// figure-caption | <
            Prepended
            ///

            Text
            /// figure-caption | >
            Appended
            ///
            """,
            R"""
            <figure id="__figure-caption_1">
            <figcaption>
            <p><span class="caption-prefix">Figure 1.</span> Prepended</p>
            </figcaption>
            <p>Text</p>
            </figure>
            <figure id="__figure-caption_2">
            <p>Text</p>
            <figcaption>
            <p><span class="caption-prefix">Figure 2.</span> Appended</p>
            </figcaption>
            </figure>
            """,
            True
        )


class TestBlocksCaptionCustomPrefix(util.MdCase):
    """Test Blocks caption cases with `auto` level."""

    extension = ['pymdownx.blocks.caption']
    extension_configs = {
        'pymdownx.blocks.caption': {
            'types': [
                'caption',
                {
                    'name': 'figure-caption',
                    'prefix': 'Figure <span class="caption-num">{}</span>.'
                },
                {
                    'name': 'table-caption',
                    'prefix': 'Table <span class="caption-num">{}</span>.'
                }
            ]
        }
    }

    def test_custom_prefix(self):
        """Test custom prefix."""

        self.check_markdown(
            R'''
            A paragraph with a caption.
            /// figure-caption
            This is the caption.
            ///
            ''',
            R'''
            <figure id="__figure-caption_1">
            <p>A paragraph with a caption.</p>
            <figcaption>
            <p><span class="caption-prefix">Figure <span class="caption-num">1</span>.</span> This is the caption.</p>
            </figcaption>
            </figure>
            ''',
            True
        )
