"""Test cases for Details."""
from __future__ import unicode_literals
from .. import util
from pymdownx import util as pymd_util


class TestDetails(util.MdCase):
    """Test Details."""

    extension = ['pymdownx.details']
    extension_configs = {}

    def test_nested(self):
        """Test nested."""

        if pymd_util.MD3:
            expected = r'''
                <details><summary>details</summary><p>content</p>
                <details open="open"><summary>open nested details</summary><p>content</p>
                <p>more content</p>
                </details>
                </details>
                '''
        else:
            expected = (
                r'<details><summary>details</summary><p>content</p>'
                r'<details open="open"><summary>open nested details</summary><p>content</p>'
                r'<p>more content</p>'
                r'</details>'
                r'</details>'
            )

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

        if pymd_util.MD3:
            expected = r'''
                <details class="optional-class"><summary>details with class</summary><p>content</p>
                </details>
                '''
        else:
            expected = (
                r'<details class="optional-class"><summary>details with class</summary><p>content</p>'
                r'</details>'
            )

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

        if pymd_util.MD3:
            expected = r'''
                <details class="multiple optional-class"><summary>details with multiple class</summary><p>content</p>
                </details>
                '''
        else:
            expected = (
                r'<details class="multiple optional-class"><summary>details with multiple class</summary><p>content</p>'
                r'</details>'
            )

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

        if pymd_util.MD3:
            expected = r'''
                <details class="only-class"><summary>Only-class</summary><p>content</p>
                </details>
                '''
        else:
            expected = (
                r'<details class="only-class"><summary>Only-class</summary><p>content</p>'
                r'</details>'
            )

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

        if pymd_util.MD3:
            expected = r'''
                <details class="multiple classes"><summary>Multiple</summary><p>content</p>
                </details>
                '''
        else:
            expected = (
                r'<details class="multiple classes"><summary>Multiple</summary><p>content</p>'
                r'</details>'
            )

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

        if pymd_util.MD3:
            expected = r'''
                <details><summary>details end test</summary><p>content</p>
                </details>
                <p>other content</p>
                '''
        else:
            expected = (
                r'<details><summary>details end test</summary><p>content</p>'
                r'</details>'
                r'<p>other content</p>'
            )

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

        if pymd_util.MD3:
            expected = r'''
                <details class="relaxed spacing"><summary>Title</summary><p>content</p>
                </details>
                '''
        else:
            expected = (
                r'<details class="relaxed spacing"><summary>Title</summary><p>content</p>'
                r'</details>'
            )

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

        if pymd_util.MD3:
            expected = r'''
                <details class="relaxed spacing no title"><summary>Relaxed</summary><p>content</p>
                </details>
                '''
        else:
            expected = (
                r'<details class="relaxed spacing no title"><summary>Relaxed</summary><p>content</p>'
                r'</details>'
            )

        self.check_markdown(
            r'''
            ???relaxed  spacing no  title
                content
            ''',
            expected,
            True
        )
