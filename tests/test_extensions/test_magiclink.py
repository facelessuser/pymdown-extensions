"""Test cases for MagicLink."""
from .. import util
import markdown
import warnings


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
            r'https://x.com/someuser',
            r'<p><a href="https://x.com/someuser">https://x.com/someuser</a></p>'
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
        'pymdownx.magiclink'
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
            r'https://x.com/someuser',
            r'<p><a class="magiclink magiclink-x magiclink-mention" href="https://x.com/someuser" title="X User: someuser">@someuser</a></p>'  # noqa: E501
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
            r'https://x.com/home',
            r'<p><a href="https://x.com/home">https://x.com/home</a></p>'
        )


class TestMagicLinkCustom(util.MdCase):
    """Test cases for custom provider."""

    extension = [
        'pymdownx.magiclink',
        'pymdownx.saneheaders'
    ]

    extension_configs = {
        'pymdownx.magiclink': {
            'repo_url_shorthand': True,
            'repo_url_shortener': True,
            'user': 'facelessuser',
            'repo': 'pymdown-extensions',
            'provider': 'test',
            'custom': {
                'test': {
                    'host': 'http://test.com',
                    'label': 'Test',
                    'type': 'github'
                }
            }
        }
    }

    def test_user(self):
        """Test user in custom repo."""

        self.check_markdown(
            '@facelessuser',
            '<p><a class="magiclink magiclink-test magiclink-mention" href="http://test.com/facelessuser" title="Test User: facelessuser">@facelessuser</a></p>'  # noqa: E501
        )

    def test_repo(self):
        """Test repo in custom repo."""

        self.check_markdown(
            '@facelessuser/pymdown-extensions',
            '<p><a class="magiclink magiclink-test magiclink-repository" href="http://test.com/facelessuser/pymdown-extensions" title="Test Repository: facelessuser/pymdown-extensions">facelessuser/pymdown-extensions</a></p>'  # noqa: E501
        )

    def test_default_issue(self):
        """Test default issue case."""

        self.check_markdown(
            '#2',
            '<p><a class="magiclink magiclink-test magiclink-issue" href="http://test.com/facelessuser/pymdown-extensions/issues/2" title="Test Issue: facelessuser/pymdown-extensions #2">#2</a></p>'  # noqa: E501
        )

    def test_default_pull(self):
        """Test default pull case."""

        self.check_markdown(
            '!2',
            '<p><a class="magiclink magiclink-test magiclink-pull" href="http://test.com/facelessuser/pymdown-extensions/pull/2" title="Test Pull Request: facelessuser/pymdown-extensions #2">!2</a></p>'  # noqa: E501
        )

    def test_default_discussion(self):
        """Test default discussion case."""

        self.check_markdown(
            '?2',
            '<p><a class="magiclink magiclink-test magiclink-discussion" href="http://test.com/facelessuser/pymdown-extensions/discussions/2" title="Test Discussion: facelessuser/pymdown-extensions #2">?2</a></p>'  # noqa: E501
        )

    def test_default_commit(self):
        """Test default commit case."""

        self.check_markdown(
            '3f6b07a8eeaa9d606115758d90f55fec565d4e2a',
            '<p><a class="magiclink magiclink-test magiclink-commit" href="http://test.com/facelessuser/pymdown-extensions/commit/3f6b07a8eeaa9d606115758d90f55fec565d4e2a" title="Test Commit: facelessuser/pymdown-extensions@3f6b07a">3f6b07a</a></p>'  # noqa: E501
        )

    def test_default_compare(self):
        """Test default compare case."""

        self.check_markdown(
            'e2ed7e0b3973f3f9eb7a26b8ef7ae514eebfe0d2...90b6fb8711e75732f987982cc024e9bb0111beac',
            '<p><a class="magiclink magiclink-test magiclink-compare" href="http://test.com/facelessuser/pymdown-extensions/compare/e2ed7e0b3973f3f9eb7a26b8ef7ae514eebfe0d2...90b6fb8711e75732f987982cc024e9bb0111beac" title="Test Compare: facelessuser/pymdown-extensions@e2ed7e0...90b6fb8">e2ed7e0...90b6fb8</a></p>'  # noqa: E501
        )

    def test_user_link(self):
        """Test user link."""

        self.check_markdown(
            'http://test.com/facelessuser',
            '<p><a class="magiclink magiclink-test magiclink-mention" href="http://test.com/facelessuser" title="Test User: facelessuser">@facelessuser</a></p>'  # noqa: E501
        )

    def test_repo_link(self):
        """Test repository link."""

        self.check_markdown(
            'http://test.com/facelessuser/pymdown-extensions',
            '<p><a class="magiclink magiclink-test magiclink-repository" href="http://test.com/facelessuser/pymdown-extensions" title="Test Repository: facelessuser/pymdown-extensions">facelessuser/pymdown-extensions</a></p>'  # noqa: E501
        )

    def test_issue_link(self):
        """Test issue link."""

        self.check_markdown(
            'http://test.com/facelessuser/pymdown-extensions/issues/2',
            '<p><a class="magiclink magiclink-test magiclink-issue" href="http://test.com/facelessuser/pymdown-extensions/issues/2" title="Test Issue: facelessuser/pymdown-extensions #2">#2</a></p>'  # noqa: E501
        )

    def test_pull_link(self):
        """Test issue link."""

        self.check_markdown(
            'http://test.com/facelessuser/pymdown-extensions/pull/2',
            '<p><a class="magiclink magiclink-test magiclink-pull" href="http://test.com/facelessuser/pymdown-extensions/pull/2" title="Test Pull Request: facelessuser/pymdown-extensions #2">!2</a></p>'  # noqa: E501
        )

    def test_discussion_link(self):
        """Test discussion link."""

        self.check_markdown(
            'http://test.com/facelessuser/pymdown-extensions/discussions/2',
            '<p><a class="magiclink magiclink-test magiclink-discussion" href="http://test.com/facelessuser/pymdown-extensions/discussions/2" title="Test Discussion: facelessuser/pymdown-extensions #2">?2</a></p>'  # noqa: E501
        )

    def test_commit_link(self):
        """Test commit link."""

        self.check_markdown(
            'http://test.com/facelessuser/pymdown-extensions/commit/3f6b07a8eeaa9d606115758d90f55fec565d4e2a',
            '<p><a class="magiclink magiclink-test magiclink-commit" href="http://test.com/facelessuser/pymdown-extensions/commit/3f6b07a8eeaa9d606115758d90f55fec565d4e2a" title="Test Commit: facelessuser/pymdown-extensions@3f6b07a">3f6b07a</a></p>'  # noqa: E501
        )

    def test_compare_link(self):
        """Test compare link."""

        self.check_markdown(
            'http://test.com/facelessuser/pymdown-extensions/compare/e2ed7e0b3973f3f9eb7a26b8ef7ae514eebfe0d2...90b6fb8711e75732f987982cc024e9bb0111beac',
            '<p><a class="magiclink magiclink-test magiclink-compare" href="http://test.com/facelessuser/pymdown-extensions/compare/e2ed7e0b3973f3f9eb7a26b8ef7ae514eebfe0d2...90b6fb8711e75732f987982cc024e9bb0111beac" title="Test Compare: facelessuser/pymdown-extensions@e2ed7e0...90b6fb8">e2ed7e0...90b6fb8</a></p>'  # noqa: E501
        )

    def test_external_user(self):
        """Test external user in custom repo."""

        self.check_markdown(
            '@github:facelessuser',
            '<p><a class="magiclink magiclink-github magiclink-mention" href="https://github.com/facelessuser" title="GitHub User: facelessuser">@facelessuser</a></p>'  # noqa: E501
        )

        self.check_markdown(
            '@test:facelessuser',
            '<p><a class="magiclink magiclink-test magiclink-mention" href="http://test.com/facelessuser" title="Test User: facelessuser">@facelessuser</a></p>'  # noqa: E501
        )

    def test_bad_name(self):
        """Test bad name."""

        extension = [
            'pymdownx.magiclink',
            'pymdownx.saneheaders'
        ]

        extension_configs = {
            'pymdownx.magiclink': {
                'repo_url_shorthand': True,
                'repo_url_shortener': True,
                'user': 'facelessuser',
                'repo': 'pymdown-extensions',
                'provider': 'bad-name',
                'custom': {
                    'bad-name': {
                        'host': 'http://bad.com',
                        'label': 'Bad',
                        'type': 'github'
                    }
                }
            }
        }

        with self.assertRaises(ValueError):
            markdown.markdown('', extensions=extension, extension_configs=extension_configs)

class TestMagicLinkWarning(util.MdCase):
    """Test cases for social link shortener."""

    extension = [
        'pymdownx.magiclink'
    ]

    extension_configs = {
        'pymdownx.magiclink': {
            'social_url_shortener': True,
            'social_url_shorthand': True
        }
    }

    def test_deprecated_twitter(self):
        """Test deprecation warning."""

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.

            # Trigger a warning.
            warnings.simplefilter("always")
            self.check_markdown(
                '@twitter:user',
                '<p><a class="magiclink magiclink-twitter magiclink-mention" href="https://twitter.com/user" title="Twitter User: user">@user</a></p>'  # noqa: E501
            )
            target = "The 'twitter' social provider has been deprecated, please use 'x' instead"
            for warn in w:
                if target in str(warn.message):
                    found = True
                    break
            # Verify some things
            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, DeprecationWarning))
            self.assertTrue(found)

    def test_deprecated_twitter_shortener(self):
        """Test shortener deprecation warning."""

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.

            # Trigger a warning.
            warnings.simplefilter("always")
            self.check_markdown(
                'https://twitter.com/user',
                '<p><a class="magiclink magiclink-twitter magiclink-mention" href="https://twitter.com/user" title="Twitter User: user">@user</a></p>'  # noqa: E501
            )
            target = "The 'twitter' social provider has been deprecated, please use 'x' instead"
            for warn in w:
                if target in str(warn.message):
                    found = True
                    break
            # Verify some things
            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, DeprecationWarning))
            self.assertTrue(found)
