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

RE_SHORTHANDS = r'''(?x)
(?:
    (?P<mention>(?<![-\w])@[a-zA-Z\d](?:[-a-zA-Z\d_]{0,37}[a-zA-Z\d])?) |
    (?:(?:(?P<user>(?<![-/_])\b[a-zA-Z\d](?:[-a-zA-Z\d_]{0,37}[a-zA-Z\d])?)/|(?<![/]))(?P<repo>[-._a-zA-Z\d]{1,100}))
        (?:(?P<issue>(?:\#|!)[1-9][0-9]*)|(?P<commit>@[a-f\d]{40}))|
    (?:(?<![-\w])(?P<issue2>(?:\#|!)[1-9][0-9]*)|(?P<commit2>(?<!@)[a-f\d]{40}))
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

GITHUB_URL = 'https://github.com'
GITHUB_ISSUE_URL = "https://github.com/%s/%s/issues/%s"
GITHUB_PULL_URL = "https://github.com/%s/%s/pull/%s"
GITHUB_COMMIT_URL = "https://github.com/%s/%s/commit/%s"

BITBUCKET_URL = 'https://bitbucket.org'
BITBUCKET_ISSUE_URL = "https://bitbucket.org/%s/%s/issues/%s"
BITBUCKET_PULL_URL = "https://bitbucket.org/%s/%s/pull-requests/%s"
BITBUCKET_COMMIT_URL = "https://bitbucket.org/%s/%s/commits/commit/%s"

GITLAB_URL = 'https://gitlab.com'
GITLAB_ISSUE_URL = "https://gitlab.com/%s/%s/issues/%s"
GITLAB_PULL_URL = "https://gitlab.com/%s/%s/merge_requests/%s"
GITLAB_COMMIT_URL = "https://gitlab.com/%s/%s/commit/%s"


class MagicShortenerTreeprocessor(Treeprocessor):
    """Treeprocessor that finds repo issue and commit links and shortens them."""

    # Repo link types
    ISSUE = 0
    PULL = 1
    COMMIT = 2

    def __init__(self, md, base_url, base_user_url):
        """Initialize."""

        self.base = base_url
        self.base_user = base_user_url
        self.labels = {
            "github": "GitHub",
            "bitbucket": "Bitbucket",
            "gitlab": "GitLab"
        }
        Treeprocessor.__init__(self, md)

    def shorten(self, link, label, my_repo, my_user, link_type, user_repo, value, url, hash_size):
        """Shorten url."""

        class_attr = link.get('class', '')
        class_name = class_attr.split(' ') if class_attr else []

        if 'magiclink' not in class_name:
            class_name.append('magiclink')

        if link_type is self.COMMIT:
            # user/repo@hash
            if my_repo:
                text = value[0:hash_size]
            elif my_user:
                text = '%s@%s' % (user_repo.split('/')[1], value[0:hash_size])
            else:
                text = '%s@%s' % (user_repo, value[0:hash_size])
            link.text = md_util.AtomicString(text)

            if 'magiclink-commit' not in class_name:
                class_name.append('magiclink-commit')

            link.set('title', '%s Commit: %s@%s' % (label, user_repo.rstrip('/'), value[0:hash_size]))
        else:
            # user/repo#(issue|pull)
            if link_type == self.ISSUE:
                issue_type = 'Issue'
                separator = '#'
                if 'magiclink-issue' not in class_name:
                    class_name.append('magiclink-issue')
            else:
                issue_type = 'Pull Request'
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
            hash_size = 7
        elif match.group('bitbucket'):
            provider = 'bitbucket'
            hash_size = 7
        elif match.group('gitlab'):
            provider = 'gitlab'
            hash_size = 8
        return provider, hash_size

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
                    provider, hash_size = self.get_provider(m)
                    my_repo = self.is_my_repo(provider, m)
                    my_user = my_repo or self.is_my_user(provider, m)
                    value, link_type = self.get_type(provider, m)

                    # All right, everything set, let's shorten.
                    self.shorten(
                        link,
                        self.labels[provider],
                        my_repo,
                        my_user,
                        link_type,
                        m.group(provider + '_user_repo'),
                        value,
                        href,
                        hash_size
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


class MagiclinkShorthandPattern(Pattern):
    """Convert emails to clickable email links."""

    def __init__(self, pattern, md, user, repo, provider_info):
        """Initialize."""

        self.user = user
        self.repo = repo
        self.provider_info = provider_info
        Pattern.__init__(self, pattern, md)

    def process_mention(self, el, mention):
        """Process mention."""

        el.set('href', '%s/%s' % (self.provider_info['url'], mention[1:]))
        el.set('title', "%s User: %s" % (self.provider_info['provider'], mention[1:]))
        el.set('class', 'magiclink magiclink-mention')
        el.text = md_util.AtomicString(mention)
        return el

    def process_issues(self, el, user, repo, issue):
        """Process issues."""

        issue_value = issue[1:]
        issue_type = issue[:1]

        if issue_type == '#':
            issue_link = self.provider_info['issue']
            issue_label = 'Issue'
            class_name = 'magiclink-issue'
        else:
            issue_link = self.provider_info['pull']
            issue_label = 'Pull Request'
            class_name = 'magiclink-pull'

        if not repo:
            user = self.user
            repo = self.repo
            text = '%s%s' % (issue_type, issue_value)
        else:
            if not user:
                user = self.user
                text = '%s%s%s' % (repo, issue_type, issue_value)
            else:
                text = '%s/%s%s%s' % (user, repo, issue_type, issue_value)

        el.set('href', issue_link % (user, repo, issue_value))
        el.text = md_util.AtomicString(text)
        el.set('class', 'magiclink %s' % class_name)
        el.set(
            'title',
            '%s %s: %s/%s%s%s' % (
                self.provider_info['provider'],
                issue_label,
                user,
                repo,
                issue_type,
                issue_value
            )
        )

    def process_commit(self, el, user, repo, commit):
        """Process commit."""

        if not repo:
            user = self.user
            repo = self.repo
            text = commit[0:self.provider_info['hash_size']]
        else:
            if not user:
                user = self.user
                text = '%s@%s' % (repo, commit[0:self.provider_info['hash_size']])
            else:
                text = '%s/%s@%s' % (user, repo, commit[0:self.provider_info['hash_size']])

        el.set('href', self.provider_info['commit'] % (user, repo, commit))
        el.text = md_util.AtomicString(text)
        el.set('class', 'magiclink magiclink-commit')
        el.set(
            'title',
            '%s Commit: %s/%s@%s' % (
                self.provider_info['provider'],
                user,
                repo,
                commit[0:self.provider_info['hash_size']]
            )
        )

    def handleMatch(self, m):
        """Handle email link patterns."""

        el = md_util.etree.Element("a")
        if m.group('mention'):
            self.process_mention(el, m.group('mention'))
        elif m.group('issue'):
            self.process_issues(el, m.group('user'), m.group('repo'), m.group('issue'))
        elif m.group('issue2'):
            self.process_issues(el, None, None, m.group('issue2'))
        elif m.group('commit'):
            self.process_commit(el, m.group('user'), m.group('repo'), m.group('commit')[1:])
        elif m.group('commit2'):
            self.process_commit(el, None, None, m.group('commit2'))
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

    def get_provider_info(self, provider):
        """Get provider info."""

        provider_info = {}
        if provider == 'gitlab':
            provider_info["provider"] = "GitLab"
            provider_info["url"] = GITLAB_URL
            provider_info["issue"] = GITLAB_ISSUE_URL
            provider_info["pull"] = GITLAB_PULL_URL
            provider_info["commit"] = GITLAB_COMMIT_URL
            provider_info["hash_size"] = 8
        elif provider == 'bitbucket':
            provider_info["provider"] = "Bitbucket"
            provider_info["url"] = BITBUCKET_URL
            provider_info["issue"] = BITBUCKET_ISSUE_URL
            provider_info["pull"] = BITBUCKET_PULL_URL
            provider_info["commit"] = BITBUCKET_COMMIT_URL
            provider_info["hash_size"] = 7
        else:
            provider_info["provider"] = "GitHub"
            provider_info["url"] = GITHUB_URL
            provider_info["issue"] = GITHUB_ISSUE_URL
            provider_info["pull"] = GITHUB_PULL_URL
            provider_info["commit"] = GITHUB_COMMIT_URL
            provider_info["hash_size"] = 7
        return provider_info

    def extendMarkdown(self, md, md_globals):
        """Add support for turning html links and emails to link tags."""

        config = self.getConfigs()

        # Setup repo variables
        user = config.get('user', '')
        repo = config.get('repo', '')
        provider_info = self.get_provider_info(config.get('provider', 'github'))

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
                base_url = '%s/%s/%s/' % (provider_info['url'], user, repo)
                base_user_url = '%s/%s/' % (provider_info['url'], user)

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
            shorthand = MagiclinkShorthandPattern(RE_SHORTHANDS, md, user, repo, provider_info)
            md.inlinePatterns.add("magic-repo-shorthand", shorthand, "<entity")

        # Setup link post processor for shortening repository links
        if config.get('repo_url_shortener', False):
            shortener = MagicShortenerTreeprocessor(md, base_url, base_user_url)
            shortener.config = config
            md.treeprocessors.add("magic-repo-shortener", shortener, "<prettify")


def makeExtension(*args, **kwargs):
    """Return extension."""

    return MagiclinkExtension(*args, **kwargs)
