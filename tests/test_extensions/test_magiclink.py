"""Test cases for MagicLink."""
from .. import util


class TestMagicLinkShortner(util.MdCase):
    """Test cases for repo link shortening."""

    extension = [
        'pymdownx.magiclink',
    ]

    extension_configs = {
        'pymdownx.magiclink': {
            'repo_url_shortener': True
        }
    }

    def test_user(self):
        """Test user shortening."""

        # Test #! original syntax
        self.check_markdown(
            r'https://github.com/facelessuser',
            r'<p><a class="magiclink magiclink-github magiclink-mention" href="https://github.com/facelessuser" title="GitHub User: facelessuser">@facelessuser</a></p>'  # noqa: E501
        )

    def test_repo(self):
        """Test repository shortening."""

        # Test #! original syntax
        self.check_markdown(
            r'https://github.com/facelessuser/pymdown-extensions',
            r'<p><a class="magiclink magiclink-github magiclink-repository" href="https://github.com/facelessuser/pymdown-extensions" title="GitHub Repository: facelessuser/pymdown-extensions">facelessuser/pymdown-extensions</a></p>'  # noqa: E501
        )

    def test_no_social(self):
        """Test that social shortening does not happen."""

        self.check_markdown(
            r'https://twitter.com/someuser',
            r'<p><a href="https://twitter.com/someuser">https://twitter.com/someuser</a></p>'
        )

    def test_excluded_user(self):
        """Test excluded."""

        self.check_markdown(
            r'https://github.com/support',
            r'<p><a href="https://github.com/support">https://github.com/support</a></p>'
        )

    def test_excluded_user_repo(self):
        """Test excluded."""

        self.check_markdown(
            r'https://github.com/support/repo',
            r'<p><a href="https://github.com/support/repo">https://github.com/support/repo</a></p>'
        )

    def test_discuss(self):
        """Test discuss."""

        self.check_markdown(
            r'https://github.com/facelessuser/pymdown-extensions/discussions/1173',
            r'<p><a class="magiclink magiclink-github magiclink-discussion" href="https://github.com/facelessuser/pymdown-extensions/discussions/1173" title="GitHub Discussion: facelessuser/pymdown-extensions #1173">facelessuser/pymdown-extensions?1173</a></p>'  # noqa: E501
        )


class TestMagicLinkShorthand(util.MdCase):
    """Test cases for repo link shortening."""

    extension = [
        'pymdownx.magiclink',
    ]

    extension_configs = {
        'pymdownx.magiclink': {
            'repo_url_shorthand': True,
            'user': 'facelessuser',
            'repo': 'pymdown-extensions'
        }
    }

    def test_discuss(self):
        """Test discuss."""

        self.check_markdown(
            r'?1173',
            r'<p><a class="magiclink magiclink-github magiclink-discussion" href="https://github.com/facelessuser/pymdown-extensions/discussions/1173" title="GitHub Discussion: facelessuser/pymdown-extensions #1173">?1173</a></p>'  # noqa: E501
        )

    def test_bad_discss(self):
        """Test repo that doesn't support discussions."""

        self.check_markdown(
            r'gitlab:user/repo?1173',
            r'<p>gitlab:user/repo?1173</p>'
        )


class TestMagicLinkExternalShorthand(util.MdCase):
    """Test cases for repo link shortening."""

    extension = [
        'pymdownx.magiclink',
    ]

    extension_configs = {
        'pymdownx.magiclink': {
            'repo_url_shorthand': True,
            'user': 'facelessuser',
            'repo': 'pymdown-extensions',
            'provider': 'gitlab'
        }
    }

    def test_bad_discss(self):
        """Test repo that doesn't support discussions."""

        self.check_markdown(
            r'?1173',
            r'<p>?1173</p>'
        )


class TestMagicLinkShortnerSocial(util.MdCase):
    """Test cases for social link shortener."""

    extension = [
        'pymdownx.magiclink',
    ]

    extension_configs = {
        'pymdownx.magiclink': {
            'social_url_shortener': True
        }
    }

    def test_user(self):
        """Test user shortening."""

        # Test #! original syntax
        self.check_markdown(
            r'https://twitter.com/someuser',
            r'<p><a class="magiclink magiclink-twitter magiclink-mention" href="https://twitter.com/someuser" title="Twitter User: someuser">@someuser</a></p>'  # noqa: E501
        )

    def test_no_repo(self):
        """Test that repository shortening does not happen."""

        self.check_markdown(
            r'https://github.com/facelessuser',
            r'<p><a href="https://github.com/facelessuser">https://github.com/facelessuser</a></p>'
        )

    def test_excluded(self):
        """Test excluded user."""

        self.check_markdown(
            r'https://twitter.com/home',
            r'<p><a href="https://twitter.com/home">https://twitter.com/home</a></p>'
        )
