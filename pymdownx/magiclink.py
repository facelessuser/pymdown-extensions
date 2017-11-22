"""
Magic Link.

pymdownx.magiclink
An extension for Python Markdown.
Find http|ftp links and email address and turn them to actual links

MIT license.

Copyright (c) 2014 - 2017 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import LinkPattern, Pattern
from markdown.treeprocessors import Treeprocessor
from markdown import util as md_util
from . import util
from .util import PymdownxDeprecationWarning
import warnings
import re
import os

MAGIC_LINK = 1
MAGIC_AUTO_LINK = 2

RE_MAIL = r'''(?xi)
(
    (?<![-/\+@a-z\d_])(?:[-+a-z\d_]([-a-z\d_+]|\.(?!\.))*)  # Local part
    (?<!\.)@(?:[-a-z\d_]+\.)                                # @domain part start
    (?:(?:[-a-z\d_]|(?<!\.)\.(?!\.))*)[a-z]\b               # @domain.end (allow multiple dot names)
    (?![-@])                                                # Don't allow last char to be followed by these
)
'''

RE_LINK = r'''(?xi)
(
    (?:(?<=\b)|(?<=_))(?:
        (?:ht|f)tps?://(?:(?:[^_\W][-\w]*(?:\.[-\w.]+)+)|localhost)|  # (http|ftp)://
        (?P<www>w{3}\.)[^_\W][-\w]*(?:\.[-\w.]+)+                     # www.
    )
    /?[-\w.?,!'(){}\[\]/+&@%$#=:"|~;]*                                # url path, fragments, and query stuff
    (?:[^_\W]|[-/#@$+=])                                              # allowed end chars
)
'''

RE_GIT_MENTIONS = r'''(?x)
(?P<mention>(?<![a-zA-Z])@(?:(?:github|gitlab|bitbucket):)?[a-zA-Z\d](?:[-a-zA-Z\d_]{0,37}[a-zA-Z\d])?)\b
'''
RE_GIT_REPO_MENTIONS = RE_GIT_MENTIONS + r'/(?P<mention_repo>[-._a-zA-Z\d]{0,99}[a-zA-Z\d])\b'
RE_GIT_REFS = r'''(?x)
(?:
    (?<![@/])(?:(?P<user>\b(?:(?:github|gitlab|bitbucket):)?[a-zA-Z\d](?:[-a-zA-Z\d_]{0,37}[a-zA-Z\d])?)/)?
        (?P<repo>\b[-._a-zA-Z\d]{0,99}[a-zA-Z\d])
        (?:(?P<issue>(?:\#|!)[1-9][0-9]*)|(?P<commit>@[a-f\d]{40})) |
    (?:(?<![a-zA-Z])(?P<issue2>(?:\#|!)[1-9][0-9]*)|(?P<commit2>(?<![@/])\b[a-f\d]{40}))
)\b
'''

RE_AUTOLINK = r'(?i)<((?:ht|f)tps?://[^>]*)>'

RE_REPO_LINK = re.compile(
    r'''(?xi)
    (?:
        (?P<github>(?P<github_base>https://(?:w{3}\.)?github.com/(?P<github_user_repo>[^/]+/[^/]+))/
            (?:issues/(?P<github_issue>\d+)/?|
               pull/(?P<github_pull>\d+)/?|
               commit/(?P<github_commit>[\da-f]{40})/?)) |

        (?P<bitbucket>(?P<bitbucket_base>https://(?:w{3}\.)?bitbucket.org/(?P<bitbucket_user_repo>[^/]+/[^/]+))/
            (?:issues/(?P<bitbucket_issue>\d+)(?:/[^/]+)?/?|
               pull-requests/(?P<bitbucket_pull>\d+)(?:/[^/]+(?:/diff)?)?/?|
               commits/commit/(?P<bitbucket_commit>[\da-f]{40})/?)) |

        (?P<gitlab>(?P<gitlab_base>https://(?:w{3}\.)?gitlab.com/(?P<gitlab_user_repo>[^/]+/[^/]+))/
            (?:issues/(?P<gitlab_issue>\d+)/?|
               merge_requests/(?P<gitlab_pull>\d+)/?|
               commit/(?P<gitlab_commit>[\da-f]{40})/?))
    )
    '''
)

PROVIDER_INFO = {
    "gitlab": {
        "provider": "GitLab",
        "url": "https://gitlab.com",
        "issue": "https://gitlab.com/%s/%s/issues/%s",
        "pull": "https://gitlab.com/%s/%s/merge_requests/%s",
        "commit": "https://gitlab.com/%s/%s/commit/%s",
        "hash_size": 8
    },
    "bitbucket": {
        "provider": "Bitbucket",
        "url": "https://bitbucket.org",
        "issue": "https://bitbucket.org/%s/%s/issues/%s",
        "pull": "https://bitbucket.org/%s/%s/pull-requests/%s",
        "commit": "https://bitbucket.org/%s/%s/commits/commit/%s",
        "hash_size": 7
    },
    "github": {
        "provider": "GitHub",
        "url": "https://github.com",
        "issue": "https://github.com/%s/%s/issues/%s",
        "pull": "https://github.com/%s/%s/pull/%s",
        "commit": "https://github.com/%s/%s/commit/%s",
        "hash_size": 7
    }
}


class _MagiclinkShorthandPattern(Pattern):
    """Base shorthand link class."""

    def __init__(self, pattern, md, user, repo, provider, labels, external=False):
        """Initialize."""

        self.user = user
        self.repo = repo
        self.labels = labels
        self.provider = provider
        self.external = external
        Pattern.__init__(self, pattern, md)


class MagicShortenerTreeprocessor(Treeprocessor):
    """Treeprocessor that finds repo issue and commit links and shortens them."""

    # Repo link types
    ISSUE = 0
    PULL = 1
    COMMIT = 2

    def __init__(self, md, base_url, base_user_url, labels):
        """Initialize."""

        self.base = base_url
        self.base_user = base_user_url
        self.repo_labels = labels
        self.labels = {
            "github": "GitHub",
            "bitbucket": "Bitbucket",
            "gitlab": "GitLab"
        }
        Treeprocessor.__init__(self, md)

    def shorten(self, link, provider, my_repo, my_user, link_type, user_repo, value, url, hash_size):
        """Shorten url."""

        label = PROVIDER_INFO[provider]['provider']
        prov_class = 'magiclink-%s' % provider
        class_attr = link.get('class', '')
        class_name = class_attr.split(' ') if class_attr else []

        if 'magiclink' not in class_name:
            class_name.append('magiclink')

        if prov_class not in class_name:
            class_name.append(prov_class)

        if link_type is self.COMMIT:
            # user/repo@hash
            repo_label = self.repo_labels.get('commit', 'Commit')
            if my_repo:
                text = value[0:hash_size]
            elif my_user:
                text = '%s@%s' % (user_repo.split('/')[1], value[0:hash_size])
            else:
                text = '%s@%s' % (user_repo, value[0:hash_size])
            link.text = md_util.AtomicString(text)

            if 'magiclink-commit' not in class_name:
                class_name.append('magiclink-commit')

            link.set(
                'title',
                '%s %s: %s@%s' % (label, repo_label, user_repo.rstrip('/'), value[0:hash_size])
            )
        else:
            # user/repo#(issue|pull)
            if link_type == self.ISSUE:
                issue_type = self.repo_labels.get('issue', 'Issue')
                separator = '#'
                if 'magiclink-issue' not in class_name:
                    class_name.append('magiclink-issue')
            else:
                issue_type = self.repo_labels.get('pull', 'Pull Request')
                separator = '!'
                if 'magiclink-pull' not in class_name:
                    class_name.append('magiclink-pull')
            if my_repo:
                text = separator + value
            elif my_user:
                text = user_repo.split('/')[1] + separator + value
            else:
                text = user_repo + separator + value
            link.text = md_util.AtomicString(text)
            link.set('title', '%s %s: %s%s%s' % (label, issue_type, user_repo.rstrip('/'), separator, value))
        link.set('class', ' '.join(class_name))

    def get_provider(self, match):
        """Get the provider and hash size."""

        # Set provider specific variables
        if match.group('github'):
            provider = 'github'
        elif match.group('bitbucket'):
            provider = 'bitbucket'
        elif match.group('gitlab'):
            provider = 'gitlab'
        return provider

    def get_type(self, provider, match):
        """Get the link type."""

        # Gather info about link type
        if match.group(provider + '_commit') is not None:
            value = match.group(provider + '_commit')
            link_type = self.COMMIT
        elif match.group(provider + '_pull') is not None:
            value = match.group(provider + '_pull')
            link_type = self.PULL
        else:
            value = match.group(provider + '_issue')
            link_type = self.ISSUE
        return value, link_type

    def is_my_repo(self, provider, match):
        """Check if link is from our specified user and repo."""

        # See if these links are from the specified repo.
        return self.base and match.group(provider + '_base') + '/' == self.base

    def is_my_user(self, provider, match):
        """Check if link is from our specified user."""

        return self.base_user and match.group(provider + '_base').startswith(self.base_user)

    def run(self, root):
        """Shorten popular git repository links."""

        self.hide_protocol = self.config['hide_protocol']

        links = root.iter('a')
        for link in links:
            has_child = len(list(link))
            is_magic = link.attrib.get('magiclink')
            href = link.attrib.get('href', '')
            text = link.text

            if is_magic:
                del link.attrib['magiclink']

            # We want a normal link.  No subelements embedded in it, just a normal string.
            if has_child or not text:  # pragma: no cover
                continue

            # Make sure the text matches the href.  If needed, add back protocol to be sure.
            # Not all links will pass through MagicLink, so we try both with and without protocol.
            if (text == href or (is_magic and self.hide_protocol and ('https://' + text) == href)):
                m = RE_REPO_LINK.match(href)
                if m:
                    provider = self.get_provider(m)
                    my_repo = self.is_my_repo(provider, m)
                    my_user = my_repo or self.is_my_user(provider, m)
                    value, link_type = self.get_type(provider, m)

                    # All right, everything set, let's shorten.
                    self.shorten(
                        link,
                        provider,
                        my_repo,
                        my_user,
                        link_type,
                        m.group(provider + '_user_repo'),
                        value,
                        href,
                        PROVIDER_INFO[provider]['hash_size']
                    )
        return root


class MagiclinkPattern(LinkPattern):
    """Convert html, ftp links to clickable links."""

    def handleMatch(self, m):
        """Handle URL matches."""

        el = md_util.etree.Element("a")
        el.text = md_util.AtomicString(m.group(2))
        if m.group("www"):
            href = "http://%s" % m.group(2)
        else:
            href = m.group(2)
            if self.config['hide_protocol']:
                el.text = md_util.AtomicString(el.text[el.text.find("://") + 3:])
        el.set("href", self.sanitize_url(self.unescape(href.strip())))

        if self.config.get('repo_url_shortener', False):
            el.set('magiclink', md_util.text_type(MAGIC_LINK))

        return el


class MagiclinkAutoPattern(Pattern):
    """Return a link Element given an autolink `<http://example/com>`."""

    def handleMatch(self, m):
        """Return link optionally without protocol."""

        el = md_util.etree.Element("a")
        el.set('href', self.unescape(m.group(2)))
        el.text = md_util.AtomicString(m.group(2))
        if self.config['hide_protocol']:
            el.text = md_util.AtomicString(el.text[el.text.find("://") + 3:])

        if self.config.get('repo_url_shortener', False):
            el.set('magiclink', md_util.text_type(MAGIC_AUTO_LINK))

        return el


class MagicMailPattern(LinkPattern):
    """Convert emails to clickable email links."""

    def email_encode(self, code):
        """Return entity definition by code, or the code if not defined."""
        return "%s#%d;" % (md_util.AMP_SUBSTITUTE, code)

    def handleMatch(self, m):
        """Handle email link patterns."""

        el = md_util.etree.Element("a")
        email = self.unescape(m.group(2))
        href = "mailto:%s" % email
        el.text = md_util.AtomicString(''.join([self.email_encode(ord(c)) for c in email]))
        el.set("href", ''.join([md_util.AMP_SUBSTITUTE + '#%d;' % ord(c) for c in href]))
        return el


class MagiclinkMentionPattern(_MagiclinkShorthandPattern):
    """Convert @mention to links."""

    def handleMatch(self, m):
        """Handle email link patterns."""

        el = md_util.etree.Element("a")
        text = m.group('mention')[1:]
        parts = text.split(':')
        if len(parts) > 1:
            provider = parts[0]
            mention = parts[1]
        else:
            provider = self.provider
            mention = parts[0]

        el.set('href', '%s/%s' % (PROVIDER_INFO[provider]['url'], mention))
        el.set(
            'title',
            "%s %s: %s" % (PROVIDER_INFO[provider]['provider'], self.labels.get('mention', "User"), mention)
        )
        el.set('class', 'magiclink magiclink-%s magiclink-mention' % provider)
        el.text = md_util.AtomicString('@' + mention)
        return el


class MagiclinkRepositoryPattern(_MagiclinkShorthandPattern):
    """Convert @user/repo to links."""

    def handleMatch(self, m):
        """Handle email link patterns."""

        el = md_util.etree.Element("a")
        text = m.group('mention')[1:]
        parts = text.split(':')
        if len(parts) > 1:
            provider = parts[0]
            user = parts[1]
        else:
            provider = self.provider
            user = parts[0]
        repo = m.group('mention_repo')

        el.set('href', '%s/%s/%s' % (PROVIDER_INFO[provider]['url'], user, repo))
        el.set(
            'title',
            "%s %s: %s/%s" % (
                PROVIDER_INFO[provider]['provider'], self.labels.get('repository', 'Repository'), user, repo
            )
        )
        el.set('class', 'magiclink magiclink-%s magiclink-repository' % provider)
        el.text = md_util.AtomicString('%s/%s' % (user, repo))
        return el


class MagiclinkReferencePattern(_MagiclinkShorthandPattern):
    """Convert #1, repo#1, user/repo#1, !1, repo!1, user/repo!1, hash, repo@hash, or user/repo@hash to links."""

    def process_issues(self, el, provider, user, repo, issue):
        """Process issues."""

        issue_type = issue[:1]
        issue_value = issue[1:]

        if issue_type == '#':
            issue_link = PROVIDER_INFO[provider]['issue']
            issue_label = self.labels.get('issue', 'Issue')
            class_name = 'magiclink-issue'
        else:
            issue_link = PROVIDER_INFO[provider]['pull']
            issue_label = self.labels.get('pull', 'Pull Request')
            class_name = 'magiclink-pull'

        if self.my_repo:
            text = '%s%s' % (issue_type, issue_value)
        elif self.my_user:
            text = '%s%s%s' % (repo, issue_type, issue_value)
        else:
            text = '%s/%s%s%s' % (user, repo, issue_type, issue_value)

        el.set('href', issue_link % (user, repo, issue_value))
        el.text = md_util.AtomicString(text)
        el.set('class', 'magiclink magiclink-%s %s' % (provider, class_name))
        el.set(
            'title',
            '%s %s: %s/%s%s%s' % (
                PROVIDER_INFO[provider]['provider'],
                issue_label,
                user,
                repo,
                issue_type,
                issue_value
            )
        )

    def process_commit(self, el, provider, user, repo, commit):
        """Process commit."""

        hash_ref = commit[0:PROVIDER_INFO[provider]['hash_size']]
        if self.my_repo:
            text = hash_ref
        elif self.my_user:
            text = '%s@%s' % (repo, hash_ref)
        else:
            text = '%s/%s@%s' % (user, repo, hash_ref)

        el.set('href', PROVIDER_INFO[provider]['commit'] % (user, repo, commit))
        el.text = md_util.AtomicString(text)
        el.set('class', 'magiclink magiclink-%s magiclink-commit' % provider)
        el.set(
            'title',
            '%s %s: %s/%s@%s' % (
                PROVIDER_INFO[provider]['provider'],
                self.labels.get('commit', 'Commit'),
                user,
                repo,
                hash_ref
            )
        )

    def handleMatch(self, m):
        """Handle email link patterns."""

        self.my_user = False
        self.my_repo = False

        el = md_util.etree.Element("a")
        if m.group('issue') or m.group('commit'):
            # Get issue value and type
            is_commit = m.group('commit')
            value = m.group('commit')[1:] if is_commit else m.group('issue')

            repo = m.group('repo')
            user = m.group('user')
            self.my_repo = not m.group('repo')
            self.my_user = not m.group('user')

            if self.my_user:
                user = self.user

            parts = user.split(':')
            if len(parts) > 1:
                provider = parts[0]
                user = parts[1]
            else:
                provider = self.provider

            self.my_user = user == self.user and provider == self.provider

            if is_commit:
                self.process_commit(el, provider, user, repo, value)
            else:
                self.process_issues(el, provider, user, repo, value)
        else:
            is_commit = m.group('commit2')
            value = m.group('commit2') if is_commit else m.group('issue2')

            repo = self.repo
            user = self.user
            self.my_repo = True
            self.my_user = True
            provider = self.provider
            if is_commit:
                self.process_commit(el, provider, user, repo, value)
            else:
                self.process_issues(el, provider, user, repo, value)
        return el


class MagiclinkExtension(Extension):
    """Add Easylink extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'hide_protocol': [
                False,
                "If 'True', links are displayed without the initial ftp://, http:// or https://"
                "- Default: False"
            ],
            'repo_url_shortener': [
                False,
                "If 'True' repo commit and issue links are shortened - Default: False"
            ],
            'repo_url_shorthand': [
                False,
                "If 'True' repo shorthand syntax is converted to links - Default: False"
            ],
            'base_repo_url': [
                '',
                'The base repo url to use - Default: ""'
            ],
            'provider': [
                'github',
                'The base provider to use (github, gitlab, bitbucket) - Default: "github"'
            ],
            'labels': [
                {},
                "Title labels - Default: {}"
            ],
            'user': [
                '',
                'The base user name to use - Default: ""'
            ],
            'repo': [
                '',
                'The base repo to use - Default: ""'
            ]
        }
        super(MagiclinkExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Add support for turning html links and emails to link tags."""

        config = self.getConfigs()

        # Setup repo variables
        user = config.get('user', '')
        repo = config.get('repo', '')
        provider = config.get('provider', 'github')
        labels = config.get('labels', {})

        # Setup base URL
        base_url = config.get('base_repo_url', '').rstrip('/')
        base_user_url = os.path.dirname(base_url)
        if base_url:
            base_url += "/"
        if base_user_url:
            base_user_url += "/"

        if base_url:  # pragma: no cover
            warnings.warn(
                "'base_repo_url' is deprecated and will be removed in the future.\n"
                "\nIt is strongly encouraged to migrate to using `provider`, 'user`\n"
                " and 'repo' moving forward.",
                PymdownxDeprecationWarning
            )
        if config.get('repo_url_shorthand', False) or not base_url:
            if user and repo:
                base_url = '%s/%s/%s/' % (PROVIDER_INFO[provider]['url'], user, repo)
                base_user_url = '%s/%s/' % (PROVIDER_INFO[provider]['url'], user)

        # Setup general link patterns
        auto_link_pattern = MagiclinkAutoPattern(RE_AUTOLINK, md)
        auto_link_pattern.config = config
        link_pattern = MagiclinkPattern(RE_LINK, md)
        link_pattern.config = config

        # Add link patterns
        md.inlinePatterns['autolink'] = auto_link_pattern
        md.inlinePatterns.add("magic-link", link_pattern, "<entity")
        md.inlinePatterns.add("magic-mail", MagicMailPattern(RE_MAIL, md), "<entity")

        # Setup URL shortener
        if config.get('repo_url_shorthand', False):
            escape_chars = ['@']
            util.escape_chars(md, escape_chars)
            git_repo = MagiclinkRepositoryPattern(
                RE_GIT_REPO_MENTIONS, md, user, repo, provider, labels
            )
            md.inlinePatterns.add("magic-repo-mention", git_repo, "<entity")
            git_mention = MagiclinkMentionPattern(
                RE_GIT_MENTIONS, md, user, repo, provider, labels
            )
            md.inlinePatterns.add("magic-mention", git_mention, "<entity")
            git_refs = MagiclinkReferencePattern(
                RE_GIT_REFS, md, user, repo, provider, labels
            )
            md.inlinePatterns.add("magic-refs", git_refs, "<entity")

        # Setup link post processor for shortening repository links
        if config.get('repo_url_shortener', False):
            shortener = MagicShortenerTreeprocessor(md, base_url, base_user_url, labels)
            shortener.config = config
            md.treeprocessors.add("magic-repo-shortener", shortener, "<prettify")


def makeExtension(*args, **kwargs):
    """Return extension."""

    return MagiclinkExtension(*args, **kwargs)
