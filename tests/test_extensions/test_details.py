"""Test cases for Details."""
from .. import util


class TestDetails(util.MdCase):
    """Test Details."""

    extension = ['pymdownx.details', 'markdown.extensions.def_list']
    extension_configs = {}

    def test_with_preceding_text(self):
        """Test content right before details."""

        expected = r'''
            <p>foo
            <strong>foo</strong></p>
            <details class="note">
            <summary>Details</summary>
            </details>
            '''

        self.check_markdown(
            R'''
            foo
            **foo**
            ??? note "Details"
            ''',
            expected,
            True
        )

    def test_nested(self):
        """Test nested."""

        expected = r'''
            <details>
            <summary>details</summary>
            <p>content</p>
            <details open="open">
            <summary>open nested details</summary>
            <p>content</p>
            <p>more content</p>
            </details>
            </details>
            '''

        self.check_markdown(
            r'''
            ??? "details"
                content

                ???+ "open nested details"
                    content

                    more content
            ''',
            expected,
            True
        )

    def test_class(self):
        """Test class."""

        expected = r'''
            <details class="optional-class">
            <summary>details with class</summary>
            <p>content</p>
            </details>
            '''

        self.check_markdown(
            r'''
            ??? optional-class "details with class"
                content
            ''',
            expected,
            True
        )

    def test_multiple_classes(self):
        """Test multiple classes."""

        expected = r'''
            <details class="multiple optional-class">
            <summary>details with multiple class</summary>
            <p>content</p>
            </details>
            '''

        self.check_markdown(
            r'''
            ??? multiple optional-class "details with multiple class"
                content
            ''',
            expected,
            True
        )

    def test_only_class(self):
        """Test only class."""

        expected = r'''
            <details class="only-class">
            <summary>Only-class</summary>
            <p>content</p>
            </details>
            '''

        self.check_markdown(
            r'''
            ??? only-class
                content
            ''',
            expected,
            True
        )

    def test_only_multiple_classes(self):
        """Test only multiple classes."""

        expected = r'''
            <details class="multiple classes">
            <summary>Multiple</summary>
            <p>content</p>
            </details>
            '''

        self.check_markdown(
            r'''
            ??? multiple classes
                content
            ''',
            expected,
            True
        )

    def test_content_after(self):
        """Test content after details."""

        expected = r'''
            <details>
            <summary>details end test</summary>
            <p>content</p>
            </details>
            <p>other content</p>
            '''

        self.check_markdown(
            r'''
            ??? "details end test"
                content
            other content
            ''',
            expected,
            True
        )

    def test_relaxed_spacing(self):
        """Test relaxed spacing."""

        expected = r'''
            <details class="relaxed spacing">
            <summary>Title</summary>
            <p>content</p>
            </details>
            '''

        self.check_markdown(
            r'''
            ???relaxed  spacing   "Title"
                content
            ''',
            expected,
            True
        )

    def test_relaxed_spacing_no_title(self):
        """Test relaxed spacing and no title."""

        expected = r'''
            <details class="relaxed spacing no title">
            <summary>Relaxed</summary>
            <p>content</p>
            </details>
            '''

        self.check_markdown(
            r'''
            ???relaxed  spacing no  title
                content
            ''',
            expected,
            True
        )

    def test_with_lists(self):
        """Test with lists."""

        self.check_markdown(
            '''
            - List

                ??? note "Details"

                    - Paragraph

                        Paragraph
            ''',

            '''
            <ul>
            <li>
            <p>List</p>
            <details class="note">
            <summary>Details</summary>
            <ul>
            <li>
            <p>Paragraph</p>
            <p>Paragraph</p>
            </li>
            </ul>
            </details>
            </li>
            </ul>
            ''',
            True
        )

    def test_with_big_lists(self):
        """Test details with a longer list."""

        self.check_markdown(
            '''
            - List

                ??? note "Details"

                    - Paragraph

                        Paragraph

                    - Paragraph

                        paragraph
            ''',
            '''
            <ul>
            <li>
            <p>List</p>
            <details class="note">
            <summary>Details</summary>
            <ul>
            <li>
            <p>Paragraph</p>
            <p>Paragraph</p>
            </li>
            <li>
            <p>Paragraph</p>
            <p>paragraph</p>
            </li>
            </ul>
            </details>
            </li>
            </ul>
            ''',
            True
        )

    def test_with_complex_lists(self):
        """Test details in a complex list scenario."""

        self.check_markdown(
            '''
            - List

                ??? note "Details"

                    - Paragraph

                        ??? note "Details"

                            1. Paragraph

                                Paragraph
            ''',
            '''
            <ul>
            <li>
            <p>List</p>
            <details class="note">
            <summary>Details</summary>
            <ul>
            <li>
            <p>Paragraph</p>
            <details class="note">
            <summary>Details</summary>
            <ol>
            <li>
            <p>Paragraph</p>
            <p>Paragraph</p>
            </li>
            </ol>
            </details>
            </li>
            </ul>
            </details>
            </li>
            </ul>
            ''',
            True
        )

    def test_definition_list(self):
        """Test with definition list."""

        self.check_markdown(
            '''
            - List

                ??? note "Details"

                    Term

                    :   Definition

                        More text

                    :   Another
                        definition

                        Even more text
            ''',
            '''
            <ul>
            <li>
            <p>List</p>
            <details class="note">
            <summary>Details</summary>
            <dl>
            <dt>Term</dt>
            <dd>
            <p>Definition</p>
            <p>More text</p>
            </dd>
            <dd>
            <p>Another
            definition</p>
            <p>Even more text</p>
            </dd>
            </dl>
            </details>
            </li>
            </ul>
            ''',
            True
        )

    def test_details_complex_list(self):
        """Test details complex list scenario."""

        self.check_markdown(
            '''
            ???+ "With details block with loose lists"
                - Parent 1

                    - Child 1
                    - Child 2
            ''',
            '''
            <details open="open">
            <summary>With details block with loose lists</summary>
            <ul>
            <li>
            <p>Parent 1</p>
            <ul>
            <li>Child 1</li>
            <li>Child 2</li>
            </ul>
            </li>
            </ul>
            </details>
            ''',
            True
        )

    def test_details_complex_list_unindentd_content(self):
        """Test details complex list scenario with un-indented content."""

        self.check_markdown(
            '''
            ???+ "With details block with loose lists"
                - Parent 1

                    - Child 1
                    - Child 2
            - Parent 2
            ''',
            '''
            <details open="open">
            <summary>With details block with loose lists</summary>
            <ul>
            <li>
            <p>Parent 1</p>
            <ul>
            <li>Child 1</li>
            <li>Child 2</li>
            </ul>
            </li>
            </ul>
            </details>
            <ul>
            <li>Parent 2</li>
            </ul>
            ''',
            True
        )
