"""Test cases for MagicLink."""
from .. import util
import markdown
import warnings


class TestMagicLink(util.MdCase):
    """Test cases for direct links."""

    extension = [
        'pymdownx.magiclink'
    ]

    def test_unmatched_closing_parenthesis(self):
        """Keep an unmatched closing parenthesis outside the link."""

        self.check_markdown(
            '(see http://foo.com/blah_blah)',
            '<p>(see <a href="http://foo.com/blah_blah">http://foo.com/blah_blah</a>)</p>'
        )

    def test_balanced_parentheses(self):
        """Keep a matching closing parenthesis in the link."""

        self.check_markdown(
            '(see http://foo.com/blah_(wikipedia))',
            '<p>(see <a href="http://foo.com/blah_(wikipedia)">http://foo.com/blah_(wikipedia)</a>)</p>'
        )

    def test_nested_parentheses(self):
        """Keep nested matching parentheses in a domain link."""

        self.check_markdown(
            'www.example.com/blah_(wikipedia_(again))',
            '<p><a href="http://www.example.com/blah_(wikipedia_(again))">www.example.com/blah_(wikipedia_(again))</a></p>'
        )

    def test_balanced_brackets(self):
        """Keep a matching closing bracket in the link."""

        self.check_markdown(
            '(see http://foo.com/blah_[1])',
            '<p>(see <a href="http://foo.com/blah_[1]">http://foo.com/blah_[1]</a>)</p>'
        )

    def test_unmatched_closing_bracket(self):
        """Keep an unmatched closing bracket outside the link."""

        self.check_markdown(
            '[see http://foo.com/blah_blah]',
            '<p>[see <a href="http://foo.com/blah_blah">http://foo.com/blah_blah</a>]</p>'
        )

    def test_mixed_balanced_closers(self):
        """Keep matching closing parentheses and brackets."""

        self.check_markdown(
            'http://foo.com/blah_[(1)]',
            '<p><a href="http://foo.com/blah_[(1)]">http://foo.com/blah_[(1)]</a></p>'
        )

    def test_more_closers_than_openers(self):
        """Only include as many closing characters as there are openers."""

        self.check_markdown(
            'http://foo.com/blah_(1))]',
            '<p><a href="http://foo.com/blah_(1)">http://foo.com/blah_(1)</a>)]</p>'
        )

    def test_short_domain(self):
        """Hosts without a period are allowed for protocol links, but a protocol alone is not a link."""

        self.check_markdown(
            'http://a http://',
            '<p><a href="http://a">http://a</a> http://</p>'
        )


class TestMagicLinkGFM(util.MdCase):
    """Test bare links against the GFM extended autolink rules."""

    extension = [
        'pymdownx.magiclink'
    ]

    @staticmethod
    def encode_mail(email):
        """Encode an email the way MagicLink does."""

        return ''.join(f'&#{ord(c)};' for c in email)

    def check_link(self, md, href, text=None, before='', after=''):
        """Check a single link in a paragraph."""

        text = href if text is None else text
        self.check_markdown(md, f'<p>{before}<a href="{href}">{text}</a>{after}</p>')

    def check_email(self, md, email, before='', after=''):
        """Check a single email link in a paragraph."""

        self.check_markdown(
            md,
            f'<p>{before}<a href="{self.encode_mail("mailto:" + email)}">{self.encode_mail(email)}</a>{after}</p>'
        )

    def test_www(self):
        """Test `www` autolinks."""

        self.check_link('www.commonmark.org', 'http://www.commonmark.org', 'www.commonmark.org')
        self.check_link(
            'Visit www.commonmark.org/help for more information.',
            'http://www.commonmark.org/help',
            'www.commonmark.org/help',
            before='Visit ',
            after=' for more information.'
        )

    def test_trailing_punctuation(self):
        """Test trailing punctuation is not part of the link."""

        self.check_link('Visit www.commonmark.org.', 'http://www.commonmark.org', 'www.commonmark.org', 'Visit ', '.')
        self.check_link(
            'Visit www.commonmark.org/a.b.', 'http://www.commonmark.org/a.b', 'www.commonmark.org/a.b', 'Visit ', '.'
        )
        for char in '?!.,:*_~':
            self.check_link(
                f'www.commonmark.org/a{char}', 'http://www.commonmark.org/a', 'www.commonmark.org/a', '', char
            )
        self.check_link('www.commonmark.org/a?b!', 'http://www.commonmark.org/a?b', 'www.commonmark.org/a?b', '', '!')

    def test_parentheses(self):
        """Test unbalanced trailing parentheses."""

        url = 'www.google.com/search?q=Markup+(business)'
        href = 'http://' + url
        self.check_link(url, href, url)
        self.check_link(url + '))', href, url, after='))')
        self.check_link(f'({url})', href, url, '(', ')')
        self.check_link(f'({url}', href, url, '(')
        self.check_link(
            'www.google.com/search?q=(business))+ok',
            'http://www.google.com/search?q=(business))+ok',
            'www.google.com/search?q=(business))+ok'
        )
        self.check_link('(Visit https://a.com/search?q=(b))', 'https://a.com/search?q=(b)', before='(Visit ', after=')')

    def test_brackets(self):
        """Test unbalanced trailing brackets."""

        self.check_link('www.a.com/x[1]', 'http://www.a.com/x[1]', 'www.a.com/x[1]')
        self.check_link('[www.a.com/x]', 'http://www.a.com/x', 'www.a.com/x', '[', ']')

    def test_entity(self):
        """Test entity like suffixes are not part of the link."""

        self.check_link(
            'www.google.com/search?q=commonmark&hl=en',
            'http://www.google.com/search?q=commonmark&amp;hl=en',
            'www.google.com/search?q=commonmark&amp;hl=en'
        )
        self.check_link(
            'www.google.com/search?q=commonmark&hl;',
            'http://www.google.com/search?q=commonmark',
            'www.google.com/search?q=commonmark',
            after='&hl;'
        )

    def test_less_than(self):
        """Test `<` ends a link."""

        self.check_link(
            'www.commonmark.org/he<lp', 'http://www.commonmark.org/he', 'www.commonmark.org/he', '', '&lt;lp'
        )

    def test_protocol(self):
        """Test protocol autolinks."""

        self.check_link('http://commonmark.org', 'http://commonmark.org')
        self.check_link('https://commonmark.org/a_b', 'https://commonmark.org/a_b')

    def test_domain_underscores(self):
        """Test underscores are not allowed in the last two segments of a domain."""

        self.check_markdown('www.foo_bar.com', '<p>www.foo_bar.com</p>')
        self.check_markdown('http://foo.bar_baz.com', '<p>http://foo.bar_baz.com</p>')
        self.check_markdown('www.foo.bar_baz', '<p>www.foo.bar_baz</p>')
        self.check_link('www.foo_bar.baz.com', 'http://www.foo_bar.baz.com', 'www.foo_bar.baz.com')

    def test_boundaries(self):
        """Test a link must follow the start of a line, whitespace, or one of `*_~(`."""

        self.check_markdown('xwww.commonmark.org', '<p>xwww.commonmark.org</p>')
        self.check_markdown('xwww.commonmark.org.x', '<p>xwww.commonmark.org.x</p>')
        self.check_markdown('xhttp://commonmark.org', '<p>xhttp://commonmark.org</p>')
        self.check_link('a\nwww.commonmark.org', 'http://www.commonmark.org', 'www.commonmark.org', 'a\n')
        self.check_link('"www.commonmark.org"', 'http://www.commonmark.org', 'www.commonmark.org', '"', '"')
        self.check_link("'http://commonmark.org/a'", 'http://commonmark.org/a', before="'", after="'")
        self.check_link('~www.commonmark.org', 'http://www.commonmark.org', 'www.commonmark.org', '~')
        self.check_link('`a`www.commonmark.org', 'http://www.commonmark.org', 'www.commonmark.org', '<code>a</code>')

    def test_emphasis(self):
        """Test links wrapped in emphasis."""

        self.check_markdown(
            '*www.commonmark.org* _www.commonmark.org_ **www.commonmark.org**',
            '<p><em><a href="http://www.commonmark.org">www.commonmark.org</a></em> '
            '<em><a href="http://www.commonmark.org">www.commonmark.org</a></em> '
            '<strong><a href="http://www.commonmark.org">www.commonmark.org</a></strong></p>'
        )

    def test_email(self):
        """Test emails."""

        self.check_email('foo@bar.baz', 'foo@bar.baz')
        self.check_markdown(
            "hello@mail+xyz.example isn't valid, but hello+xyz@mail.example is.",
            f'<p>hello@mail+xyz.example isn\'t valid, but <a href="{self.encode_mail("mailto:hello+xyz@mail.example")}">'  # noqa: E501
            f'{self.encode_mail("hello+xyz@mail.example")}</a> is.</p>'
        )
        self.check_email('a.b-c_d@a.b', 'a.b-c_d@a.b')
        self.check_email('a.b-c_d@a.b.', 'a.b-c_d@a.b', after='.')
        self.check_markdown('a.b-c_d@a.b-', '<p>a.b-c_d@a.b-</p>')
        self.check_markdown('a.b-c_d@a.b_', '<p>a.b-c_d@a.b_</p>')


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
