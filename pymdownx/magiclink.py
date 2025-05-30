"""
Magic Link.

pymdownx.magiclink
An extension for Python Markdown.
Find HTML, FTP links, and email address and turn them to actual links

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
from markdown import Extension
from markdown.treeprocessors import Treeprocessor
from markdown import util as md_util
from .util import warn_deprecated
import xml.etree.ElementTree as etree
from . import util
import re
from markdown.inlinepatterns import LinkInlineProcessor, InlineProcessor

MAGIC_LINK = 1
MAGIC_AUTO_LINK = 2

DEFAULT_EXCLUDES = {
    "bitbucket": ['dashboard', 'account', 'plans', 'support', 'repo'],
    "github": ['marketplace', 'notifications', 'issues', 'pull', 'sponsors', 'settings', 'support'],
    "gitlab": ['dashboard', '-', 'explore', 'help', 'projects'],
    "twitter": ['i', 'messages', 'bookmarks', 'home'],
    "x": ['i', 'messages', 'bookmarks', 'home']
}

# Bare link/email detection
RE_MAIL = r'''(?xi)
(?P<mail>
    (?<![-/\+@a-z\d_])(?:[-+a-z\d_]([-a-z\d_+]|\.(?!\.))*)  # Local part
    (?<!\.)@(?:[-a-z\d_]+\.)                                # @domain part start
    (?:(?:[-a-z\d_]|(?<!\.)\.(?!\.))*)[a-z]\b               # @domain.end (allow multiple dot names)
    (?![-@])                                                # Don't allow last char to be followed by these
)
'''

RE_LINK = r'''(?xi)
(?P<link>
    (?:(?<=\b)|(?<=_))(?:
        (?:ht|f)tps?://[^_\W][-\w]*(?:\.[-\w.]+)*|          # (http|ftp)://
        (?P<www>w{3}\.)[^_\W][-\w]*(?:\.[-\w.]+)*           # www.
    )
    /?[-\w.?,!'(){}\[\]/+&@%$#=:"|~;]*                      # url path, fragments, and query stuff
    (?:[^_\W]|[-/#@$+=])                                    # allowed end chars
)
'''

RE_AUTOLINK = r'(?i)<((?:ht|f)tps?://[^<>]*)>'

RE_CUSTOM_NAME = re.compile(r'^[a-zA-Z0-9]+$')

# Provider specific user regex rules
RE_TWITTER_USER = r'\w{1,15}'
RE_X_USER = r'\w{1,15}'
RE_GITHUB_USER = r'[a-zA-Z\d](?:[-a-zA-Z\d_]{0,37}[a-zA-Z\d])?'
RE_GITLAB_USER = r'[\.a-zA-Z\d_](?:[-a-zA-Z\d_\.]{0,37}[-a-zA-Z\d_])?'
RE_BITBUCKET_USER = r'[-a-zA-Z\d_]{1,39}'

# External mention patterns
RE_ALL_EXT_MENTIONS = r'''(?x)
(?P<mention>
    (?<![a-zA-Z])@
    (?:{})
)\b
'''

# Internal mention patterns
RE_INT_MENTIONS = r'(?P<mention>(?<![a-zA-Z])@{})\b'

def create_ext_mentions(name, provider_type):
    """Create external mentions by provider type."""

    if provider_type == 'github':
        return fr'{name}:{RE_GITHUB_USER}'
    elif provider_type == 'gitlab':
        return fr'{name}:{RE_GITLAB_USER}'
    elif provider_type == 'bitbucket':
        return fr'{name}:{RE_BITBUCKET_USER}'

RE_TWITTER_EXT_MENTIONS = fr'twitter:{RE_TWITTER_USER}'
RE_X_EXT_MENTIONS = fr'x:{RE_X_USER}'
RE_GITHUB_EXT_MENTIONS = create_ext_mentions('github', 'github')
RE_GITLAB_EXT_MENTIONS = create_ext_mentions('gitlab', 'gitlab')
RE_BITBUCKET_EXT_MENTIONS = create_ext_mentions('bitbucket', 'bitbucket')

# External repo mention patterns
RE_GIT_EXT_REPO_MENTIONS = r'''(?x)
(?P<mention>
    (?<![a-zA-Z])
    @(?:{})
)\b
/(?P<mention_repo>[-._a-zA-Z\d]{{0,99}}[a-zA-Z\d])\b
'''

# Internal repo mention patterns
RE_GIT_INT_REPO_MENTIONS = r'''(?x)
(?P<mention>(?<![a-zA-Z])@{})\b
/(?P<mention_repo>[-._a-zA-Z\d]{{0,99}}[a-zA-Z\d])\b
'''

# External reference patterns (issue, pull request, commit, compare)
RE_GIT_EXT_REFS = r'''(?x)
(?P<all>(?<![@/])(?:(?P<user>\b{})/)
(?P<repo>[-._a-zA-Z\d]{{0,99}}[a-zA-Z\d])
(?:(?P<issue>(?:\#|!|\?)[1-9][0-9]*)|(?P<commit>@[a-f\d]{{40}})(?:\.{{3}}(?P<diff>[a-f\d]{{40}}))?))\b
'''

# Internal reference patterns (issue, pull request, commit, compare)
RE_GIT_INT_EXT_REFS = r'''(?x)
(?P<all>(?<![@/])(?:(?P<user>\b{})/)?
(?P<repo>[-._a-zA-Z\d]{{0,99}}[a-zA-Z\d])
(?:(?P<issue>(?:\#|!|\?)[1-9][0-9]*)|(?P<commit>@[a-f\d]{{40}})(?:\.{{3}}(?P<diff>[a-f\d]{{40}}))?))\b
'''

# Internal reference patterns for default user and repository (issue, pull request, commit, compare)
RE_GIT_INT_MICRO_REFS = r'''(?x)
(?P<all>
    (?:(?<![a-zA-Z])(?P<issue>(?:\#|!|\?)[1-9][0-9]*)|(?P<commit>(?<![@/])\b[a-f\d]{40})(?:\.{3}(?P<diff>[a-f\d]{40}))?)
)\b
'''

RE_WWW = re.compile(r'(https?://)(?:www\\\.)?(.*)')

REPO_LINK_TEMPLATES = {
    'github': (
        r'''
        (?P<github>(?P<github_base>{}/
        (?P<github_user_repo>(?P<github_user>{})/[^/]+))/
            (?:issues/(?P<github_issue>\d+)/?|
                pull/(?P<github_pull>\d+)/?|
                discussions/(?P<github_discuss>\d+)/?|
                commit/(?P<github_commit>[\da-f]{{7,40}})/?|
                compare/(?P<github_diff1>[\da-f]{{7,40}})\.{{3}}
                    (?P<github_diff2>[\da-f]{{7,40}})))''',
        RE_GITHUB_USER
    ),
    'bitbucket': (
        r'''
        (?P<bitbucket>(?P<bitbucket_base>{}/
        (?P<bitbucket_user_repo>(?P<bitbucket_user>{})/[^/]+))/
            (?:issues/(?P<bitbucket_issue>\d+)(?:/[^/]+)?/?|
                pull-requests/(?P<bitbucket_pull>\d+)(?:/[^/]+(?:/diff)?)?/?|
                commits/commit/(?P<bitbucket_commit>[\da-f]{{7,40}})/?|
                branches/commits/(?P<bitbucket_diff1>[\da-f]{{7,40}})
                    (?:\.{{2}}|%0d)(?P<bitbucket_diff2>[\da-f]{{7,40}})\#diff))''',
        RE_BITBUCKET_USER
    ),
    'gitlab': (
        r'''
        (?P<gitlab>(?P<gitlab_base>{}/
        (?P<gitlab_user_repo>(?P<gitlab_user>{})/[^/]+))/(?:-/)?
            (?:issues/(?P<gitlab_issue>\d+)/?|
                merge_requests/(?P<gitlab_pull>\d+)/?|
                commit/(?P<gitlab_commit>[\da-f]{{8,40}})/?|
                compare/(?P<gitlab_diff1>[\da-f]{{8,40}})\.{{3}}
                    (?P<gitlab_diff2>[\da-f]{{8,40}})))''',
        RE_GITLAB_USER
    )
}


def create_repo_link_pattern(provider, host, www=True):
    """Create repository link provider."""

    template = REPO_LINK_TEMPLATES[provider]
    host_pat = re.escape(host.lower().rstrip('/'))
    if www:
        m = RE_WWW.match(host_pat)
        if m:
            host_pat = m.group(1) + r'(?:w{3}\.)?' + m.group(2)
    return template[0].format(host_pat, template[1])


# Repository link shortening pattern
RE_REPO_LINK = re.compile(
    r'''(?xi)^(?:{}|{}|{})/?$'''.format(
        create_repo_link_pattern('github', "https://github.com"),
        create_repo_link_pattern('bitbucket', "https://bitbucket.org"),
        create_repo_link_pattern('gitlab', 'https://gitlab.com'),
    )
)


USER_LINK_TEMPLATES = {
    'github': (
        r'''
        (?P<github>(?P<github_base>{}/
            (?P<github_user_repo>(?P<github_user>{})(?:/(?P<github_repo>[^/]+))?)))
        ''',
        RE_GITHUB_USER
    ),
    'bitbucket': (
        r'''
        (?P<bitbucket>(?P<bitbucket_base>{}/
            (?P<bitbucket_user_repo>(?P<bitbucket_user>{})(?:/(?P<bitbucket_repo>[^/]+)/?)?)))
        ''',
        RE_BITBUCKET_USER
    ),
    'gitlab': (
        r'''
        (?P<gitlab>(?P<gitlab_base>{}/
            (?P<gitlab_user_repo>(?P<gitlab_user>{})(?:/(?P<gitlab_repo>[^/]+))?)))
        ''',
        RE_GITLAB_USER
    )
}


def create_user_link_pattern(provider, host, www=True):
    """Create repository link provider."""

    template = USER_LINK_TEMPLATES[provider]
    host_pat = re.escape(host.lower().rstrip('/'))
    if www:
        m = RE_WWW.match(host_pat)
        if m:
            host_pat = m.group(1) + r'(?:w{3}\.)?' + m.group(2)
    return template[0].format(host_pat, template[1])


# Repository link shortening pattern
RE_USER_REPO_LINK = re.compile(
    r'''(?xi)^(?:{}|{}|{})/?$'''.format(
        create_user_link_pattern('github', 'https://github.com'),
        create_user_link_pattern('bitbucket', '"https://bitbucket.org"'),
        create_user_link_pattern('gitlab', 'https://gitlab.com')
    )
)

RE_SOCIAL_LINK = re.compile(
    r'''(?xi)
    ^(?:
        (?P<twitter>(?P<twitter_base>https://(?:w{{3}}\.)?twitter\.com/(?P<twitter_user>{}))) |
        (?P<x>(?P<x_base>https://(?:w{{3}}\.)?x\.com/(?P<x_user>{})))
    )/?$
    '''.format(RE_TWITTER_USER, RE_X_USER)
)

# Provider specific info (links, names, specific patterns, etc.)
SOCIAL_PROVIDERS = {'x', 'twitter'}

# Templates for providers
PROVIDER_TEMPLATES = {
    "gitlab": {
        "provider": "GitLab",
        "type": "gitlab",
        "url": "{}",
        "user_pattern": RE_GITLAB_USER,
        "issue": "{}/{{}}/{{}}/-/issues/{{}}",
        "pull": "{}/{{}}/{{}}/-/merge_requests/{{}}",
        "commit": "{}/{{}}/{{}}/-/commit/{{}}",
        "compare": "{}/{{}}/{{}}/-/compare/{{}}...{{}}",
        "hash_size": 8
    },
    "bitbucket": {
        "provider": "Bitbucket",
        "type": "bitbucket",
        "url": "{}",
        "user_pattern": RE_BITBUCKET_USER,
        "issue": "{}/{{}}/{{}}/issues/{{}}",
        "pull": "{}/{{}}/{{}}/pull-requests/{{}}",
        "commit": "{}/{{}}/{{}}/commits/commit/{{}}",
        "compare": "{}/{{}}/{{}}/branches/commits/{{}}..{{}}#diff",
        "hash_size": 7
    },
    "github": {
        "provider": "GitHub",
        "type": "github",
        "url": "{}",
        "user_pattern": RE_GITHUB_USER,
        "issue": "{}/{{}}/{{}}/issues/{{}}",
        "pull": "{}/{{}}/{{}}/pull/{{}}",
        "discuss": '{}/{{}}/{{}}/discussions/{{}}',
        "commit": "{}/{{}}/{{}}/commit/{{}}",
        "compare": "{}/{{}}/{{}}/compare/{{}}...{{}}",
        "hash_size": 7
    },
    "twitter": {
        "provider": "Twitter",
        "type": "twitter",
        "url": "{}",
        "user_pattern": RE_TWITTER_USER
    },
    "x": {
        "provider": "X",
        "type": "x",
        "url": "{}",
        "user_pattern": RE_X_USER
    }
}


def create_provider(provider, host):
    """Create the provider with the provided host."""

    entry = PROVIDER_TEMPLATES[provider].copy()
    for key in ('url', 'issue', 'pull', 'commit', 'compare', 'discuss'):
        if key not in entry:
            continue
        entry[key] = entry[key].format(host.lower().rstrip('/'))
    return entry


PROVIDER_INFO = {
    "twitter": create_provider('twitter', "https://twitter.com"),
    "x": create_provider('x', "https://x.com"),
    "gitlab": create_provider('gitlab', 'https://gitlab.com'),
    "bitbucket": create_provider('bitbucket', "https://bitbucket.org"),
    "github": create_provider('github', "https://github.com")
}


class _MagiclinkShorthandPattern(InlineProcessor):
    """Base shorthand link class."""

    def __init__(self, pattern, md, user, repo, provider, labels, normalize, provider_info):
        """Initialize."""

        self.user = user
        self.repo = repo
        self.labels = labels
        self.normalize = normalize
        self.provider_info = provider_info
        self.provider = provider if provider in self.provider_info else ''
        InlineProcessor.__init__(self, pattern, md)


class _MagiclinkReferencePattern(_MagiclinkShorthandPattern):
    """Convert #1, repo#1, user/repo#1, !1, repo!1, user/repo!1, hash, repo@hash, or user/repo@hash to links."""

    def process_issues(self, el, provider, user, repo, issue):
        """Process issues."""

        issue_type = issue[:1]
        issue_value = issue[1:]

        if issue_type == '#':
            issue_link = self.provider_info[provider]['issue']
            issue_label = self.labels.get('issue', 'Issue')
            class_name = 'magiclink-issue'
            icon = issue_type
        elif issue_type == '!':
            issue_link = self.provider_info[provider]['pull']
            issue_label = self.labels.get('pull', 'Pull Request')
            class_name = 'magiclink-pull'
            icon = '#' if self.normalize else issue_type
        elif self.provider_info[provider]['type'] == "github" and issue_type == '?':
            issue_link = self.provider_info[provider]['discuss']
            issue_label = self.labels.get('discuss', 'Discussion')
            class_name = 'magiclink-discussion'
            icon = '#' if self.normalize else issue_type
        else:
            return False

        if self.my_repo:
            el.text = md_util.AtomicString(f'{icon}{issue_value}')
        elif self.my_user:
            el.text = md_util.AtomicString(f'{repo}{icon}{issue_value}')
        else:
            el.text = md_util.AtomicString(f'{user}/{repo}{icon}{issue_value}')

        el.set('href', issue_link.format(user, repo, issue_value))
        el.set('class', f'magiclink magiclink-{provider} {class_name}')
        el.set(
            'title',
            '{} {}: {}/{} #{}'.format(
                self.provider_info[provider]['provider'],
                issue_label,
                user,
                repo,
                issue_value
            )
        )
        return True

    def process_commit(self, el, provider, user, repo, commit):
        """Process commit."""

        hash_ref = commit[0:self.provider_info[provider]['hash_size']]
        if self.my_repo:
            text = hash_ref
        elif self.my_user:
            text = f'{repo}@{hash_ref}'
        else:
            text = f'{user}/{repo}@{hash_ref}'

        el.set('href', self.provider_info[provider]['commit'].format(user, repo, commit))
        el.text = md_util.AtomicString(text)
        el.set('class', f'magiclink magiclink-{provider} magiclink-commit')
        el.set(
            'title',
            '{} {}: {}/{}@{}'.format(
                self.provider_info[provider]['provider'],
                self.labels.get('commit', 'Commit'),
                user,
                repo,
                hash_ref
            )
        )

    def process_compare(self, el, provider, user, repo, commit1, commit2):
        """Process commit."""

        hash_ref1 = commit1[0:self.provider_info[provider]['hash_size']]
        hash_ref2 = commit2[0:self.provider_info[provider]['hash_size']]
        if self.my_repo:
            text = f'{hash_ref1}...{hash_ref2}'
        elif self.my_user:
            text = f'{repo}@{hash_ref1}...{hash_ref2}'
        else:
            text = f'{user}/{repo}@{hash_ref1}...{hash_ref2}'

        el.set('href', self.provider_info[provider]['compare'].format(user, repo, commit1, commit2))
        el.text = md_util.AtomicString(text)
        el.set('class', f'magiclink magiclink-{provider} magiclink-compare')
        el.set(
            'title',
            '{} {}: {}/{}@{}...{}'.format(
                self.provider_info[provider]['provider'],
                self.labels.get('compare', 'Compare'),
                user,
                repo,
                hash_ref1,
                hash_ref2
            )
        )


class MagicShortenerTreeprocessor(Treeprocessor):
    """Tree processor that finds repo issue and commit links and shortens them."""

    # Repo link types
    ISSUE = 0
    PULL = 1
    COMMIT = 2
    DISCUSS = 3
    DIFF = 4
    REPO = 5
    USER = 6

    def __init__(
        self,
        md,
        base_url,
        base_user_url,
        labels,
        normalize,
        repo_shortner,
        social_shortener,
        custom_shortners,
        excludes,
        provider,
        provider_info
    ):
        """Initialize."""

        self.base = base_url
        self.repo_shortner = repo_shortner
        self.social_shortener = social_shortener
        self.custom_shortners = custom_shortners
        self.base_user = base_user_url
        self.repo_labels = labels
        self.normalize = normalize
        self.provider = provider
        self.provider_info = provider_info
        self.labels = {
            "github": "GitHub",
            "bitbucket": "Bitbucket",
            "gitlab": "GitLab"
        }
        self.excludes = excludes
        Treeprocessor.__init__(self, md)

    def shorten_repo(self, link, class_name, label, user_repo):
        """Shorten repo link."""

        text = user_repo
        link.text = md_util.AtomicString(text)

        if 'magiclink-repository' not in class_name:
            class_name.append('magiclink-repository')

        link.set(
            'title',
            "{} {}: {}".format(
                label, self.repo_labels.get('repository', 'Repository'), user_repo
            )
        )

    def shorten_user(self, link, class_name, label, user_repo):
        """Shorten user link."""

        link.text = md_util.AtomicString(f'@{user_repo}')

        if 'magiclink-mention' not in class_name:
            class_name.append('magiclink-mention')

        link.set(
            'title',
            "{} {}: {}".format(
                label, self.repo_labels.get('metion', 'User'), user_repo
            )
        )

    def shorten_diff(self, link, class_name, label, user_repo, value, hash_size):
        """Shorten diff/compare links."""

        repo_label = self.repo_labels.get('compare', 'Compare')
        if self.my_repo:
            text = f'{value[0][0:hash_size]}...{value[1][0:hash_size]}'
        elif self.my_user:
            text = '{}@{}...{}'.format(user_repo.split('/')[1], value[0][0:hash_size], value[1][0:hash_size])
        else:
            text = f'{user_repo}@{value[0][0:hash_size]}...{value[1][0:hash_size]}'
        link.text = md_util.AtomicString(text)

        if 'magiclink-compare' not in class_name:
            class_name.append('magiclink-compare')

        link.set(
            'title',
            '{} {}: {}@{}...{}'.format(
                label, repo_label, user_repo.rstrip('/'), value[0][0:hash_size], value[1][0:hash_size]
            )
        )

    def shorten_commit(self, link, class_name, label, user_repo, value, hash_size):
        """Shorten commit link."""

        # user/repo@hash
        repo_label = self.repo_labels.get('commit', 'Commit')
        if self.my_repo:
            text = value[0:hash_size]
        elif self.my_user:
            text = '{}@{}'.format(user_repo.split('/')[1], value[0:hash_size])
        else:
            text = f'{user_repo}@{value[0:hash_size]}'
        link.text = md_util.AtomicString(text)

        if 'magiclink-commit' not in class_name:
            class_name.append('magiclink-commit')

        link.set(
            'title',
            '{} {}: {}@{}'.format(label, repo_label, user_repo.rstrip('/'), value[0:hash_size])
        )

    def shorten_issue(self, provider, link, class_name, label, user_repo, value, link_type):
        """Shorten issue/pull link."""

        # user/repo#(issue|pull)
        provider_type = self.provider_info[provider]['type']
        if link_type == self.ISSUE:
            issue_type = self.repo_labels.get('issue', 'Issue')
            icon = '#'
            if 'magiclink-issue' not in class_name:
                class_name.append('magiclink-issue')
        elif link_type == self.PULL:
            issue_type = self.repo_labels.get('pull', 'Pull Request')
            icon = '#' if self.normalize else '!'
            if 'magiclink-pull' not in class_name:
                class_name.append('magiclink-pull')
        elif provider_type == 'github' and link_type == self.DISCUSS:
            issue_type = self.repo_labels.get('discuss', 'Discussion')
            icon = '#' if self.normalize else '?'
            if 'magiclink-discussion' not in class_name:
                class_name.append('magiclink-discussion')

        if self.my_repo:
            link.text = md_util.AtomicString(f"{icon}{value}")
        elif self.my_user:
            link.text = md_util.AtomicString("{}{}{}".format(user_repo.split('/')[1], icon, value))
        else:
            link.text = md_util.AtomicString(f"{user_repo}{icon}{value}")

        link.set('title', '{} {}: {} #{}'.format(label, issue_type, user_repo.rstrip('/'), value))

    def shorten_issue_commit(self, link, provider, link_type, user_repo, value, hash_size):
        """Shorten URL."""

        label = self.provider_info[provider]['provider']
        prov_class = f'magiclink-{provider}'
        class_attr = link.get('class', '')
        class_name = class_attr.split(' ') if class_attr else []

        if 'magiclink' not in class_name:
            class_name.append('magiclink')

        if prov_class not in class_name:
            class_name.append(prov_class)

        # Link specific shortening logic
        if link_type is self.DIFF:
            self.shorten_diff(link, class_name, label, user_repo, value, hash_size)
        elif link_type is self.COMMIT:
            self.shorten_commit(link, class_name, label, user_repo, value, hash_size)
        else:
            self.shorten_issue(provider, link, class_name, label, user_repo, value, link_type)
        link.set('class', ' '.join(class_name))

    def shorten_user_repo(self, link, provider, link_type, user_repo):
        """Shorten URL."""

        label = self.provider_info[provider]['provider']
        prov_class = f'magiclink-{provider}'
        class_attr = link.get('class', '')
        class_name = class_attr.split(' ') if class_attr else []

        if 'magiclink' not in class_name:
            class_name.append('magiclink')

        if prov_class not in class_name:
            class_name.append(prov_class)

        # Link specific shortening logic
        if link_type is self.REPO:
            self.shorten_repo(link, class_name, label, user_repo)
        else:
            self.shorten_user(link, class_name, label, user_repo)
        link.set('class', ' '.join(class_name))

    def get_provider_type(self, match):
        """Get the provider and hash size."""

        # Set provider specific variables
        if match.group('github'):
            provider = 'github'
        elif match.group('bitbucket'):
            provider = 'bitbucket'
        elif match.group('gitlab'):
            provider = 'gitlab'
        return provider

    def get_social_provider(self, match):
        """Get social provider."""

        if match.group('twitter'):
            provider = 'twitter'

        elif match.group('x'):
            provider = 'x'
        return provider

    def get_type(self, provider, match):
        """Get the link type."""

        try:
            # Gather info about link type
            if match.group(provider + '_diff1') is not None:
                value = (match.group(provider + '_diff1'), match.group(provider + '_diff2'))
                link_type = self.DIFF
            elif match.group(provider + '_commit') is not None:
                value = match.group(provider + '_commit')
                link_type = self.COMMIT
            elif match.group(provider + '_pull') is not None:
                value = match.group(provider + '_pull')
                link_type = self.PULL
            elif provider == "github" and match.group(provider + '_discuss') is not None:
                value = match.group(provider + '_discuss')
                link_type = self.DISCUSS
            else:
                value = match.group(provider + '_issue')
                link_type = self.ISSUE
        except IndexError:
            # Gather info about link type
            found = False
            try:
                if match.group(provider + '_repo') is not None:
                    value = None
                    link_type = self.REPO
                    found = True
            except IndexError:
                pass
            if not found:
                value = None
                link_type = self.USER
        return value, link_type

    def is_my_repo(self, provider_type, match):
        """Check if link is from our specified user and repo."""

        # See if these links are from the specified repo.
        return self.base and match.group(provider_type + '_base') + '/' == self.base

    def is_my_user(self, provider_type, match):
        """Check if link is from our specified user."""

        return self.base_user and match.group(provider_type + '_base').startswith(self.base_user)

    def excluded(self, provider_type, provider, match):
        """Check if user has been excluded."""

        user = match.group(provider_type + '_user')
        return user.lower() in self.excludes.get(provider, set())

    def run(self, root):
        """Shorten popular git repository links."""

        self.hide_protocol = self.config['hide_protocol']

        links = root.iter('a')
        for link in links:
            has_child = len(list(link))
            is_magic = link.attrib.get('magiclink')
            href = link.attrib.get('href', '')
            text = link.text
            found = False

            if is_magic:
                del link.attrib['magiclink']

            # We want a normal link.  No sub-elements embedded in it, just a normal string.
            if has_child or not text:  # pragma: no cover
                continue

            # Make sure the text matches the `href`.  If needed, add back protocol to be sure.
            # Not all links will pass through MagicLink, so we try both with and without protocol.
            if (text == href or (is_magic and self.hide_protocol and ('https://' + text) == href)):
                if self.repo_shortner:
                    m = RE_REPO_LINK.match(href)
                    if m:
                        provider_type = self.get_provider_type(m)
                        provider = provider_type
                        self.my_repo = self.is_my_repo(provider_type, m)
                        self.my_user = self.my_repo or self.is_my_user(provider_type, m)
                        value, link_type = self.get_type(provider_type, m)
                        found = True

                        # All right, everything set, let's shorten.
                        if not self.excluded(provider_type, provider, m):
                            self.shorten_issue_commit(
                                link,
                                provider,
                                link_type,
                                m.group(provider_type + '_user_repo'),
                                value,
                                self.provider_info[provider]['hash_size']
                            )
                if not found and self.repo_shortner:
                    m = RE_USER_REPO_LINK.match(href)
                    if m:
                        provider_type = self.get_provider_type(m)
                        provider = provider_type
                        self.my_repo = self.is_my_repo(provider_type, m)
                        self.my_user = self.my_repo or self.is_my_user(provider_type, m)
                        value, link_type = self.get_type(provider_type, m)
                        found = True

                        if not self.excluded(provider_type, provider, m):
                            # All right, everything set, let's shorten.
                            self.shorten_user_repo(
                                link,
                                provider,
                                link_type,
                                m.group(provider_type + '_user_repo')
                            )
                if not found and self.custom_shortners:
                    for custom, entry in self.custom_shortners.items():
                        m = entry['repo'].match(href)
                        if m:
                            provider = custom
                            provider_type = self.provider_info[custom]['type']
                            self.my_repo = self.is_my_repo(provider_type, m)
                            self.my_user = self.my_repo or self.is_my_user(provider_type, m)
                            value, link_type = self.get_type(provider_type, m)
                            found = True

                            # All right, everything set, let's shorten.
                            if not self.excluded(provider_type, provider, m):
                                self.shorten_issue_commit(
                                    link,
                                    provider,
                                    link_type,
                                    m.group(provider_type + '_user_repo'),
                                    value,
                                    self.provider_info[provider]['hash_size']
                                )
                        if not found:
                            m = entry['user'].match(href)
                            if m:
                                provider = custom
                                provider_type = self.provider_info[custom]['type']
                                self.my_repo = self.is_my_repo(provider_type, m)
                                self.my_user = self.my_repo or self.is_my_user(provider_type, m)
                                value, link_type = self.get_type(provider_type, m)
                                found = True

                                if not self.excluded(provider_type, provider, m):
                                    # All right, everything set, let's shorten.
                                    self.shorten_user_repo(
                                        link,
                                        provider,
                                        link_type,
                                        m.group(provider_type + '_user_repo')
                                    )

                if not found and self.social_shortener:
                    m = RE_SOCIAL_LINK.match(href)
                    if m:
                        provider = self.get_social_provider(m)
                        if provider == 'twitter':
                            warn_deprecated("The 'twitter' social provider has been deprecated, please use 'x' instead")
                        self.my_repo = self.is_my_repo(provider, m)
                        self.my_user = self.my_repo or self.is_my_user(provider, m)
                        value, link_type = self.get_type(provider, m)

                        if not self.excluded(provider, provider, m):
                            # All right, everything set, let's shorten.
                            self.shorten_user_repo(
                                link,
                                provider,
                                link_type,
                                m.group(provider + '_user')
                            )
        return root


class MagiclinkPattern(LinkInlineProcessor):
    """Convert html, ftp links to clickable links."""

    ANCESTOR_EXCLUDES = ('a',)

    def handleMatch(self, m, data):
        """Handle URL matches."""

        el = etree.Element("a")
        el.text = md_util.AtomicString(m.group('link'))
        if m.group("www"):
            href = "http://{}".format(m.group('link'))
        else:
            href = m.group('link')
            if self.config['hide_protocol']:
                el.text = md_util.AtomicString(el.text[el.text.find("://") + 3:])
        el.set("href", self.unescape(href.strip()))

        if self.config.get('repo_url_shortener', False):
            el.set('magiclink', str(MAGIC_LINK))

        return el, m.start(0), m.end(0)


class MagiclinkAutoPattern(InlineProcessor):
    """Return a link Element given an auto link `<http://example/com>`."""

    def handleMatch(self, m, data):
        """Return link optionally without protocol."""

        el = etree.Element("a")
        el.set('href', self.unescape(m.group(1)))
        el.text = md_util.AtomicString(m.group(1))
        if self.config['hide_protocol']:
            el.text = md_util.AtomicString(el.text[el.text.find("://") + 3:])

        if self.config.get('repo_url_shortener', False):
            el.set('magiclink', str(MAGIC_AUTO_LINK))

        return el, m.start(0), m.end(0)


class MagiclinkMailPattern(InlineProcessor):
    """Convert emails to clickable email links."""

    ANCESTOR_EXCLUDES = ('a',)

    def email_encode(self, code):
        """Return entity definition by code, or the code if not defined."""
        return f"{md_util.AMP_SUBSTITUTE}#{code:d};"

    def handleMatch(self, m, data):
        """Handle email link patterns."""

        el = etree.Element("a")
        email = self.unescape(m.group('mail'))
        href = f"mailto:{email}"
        el.text = md_util.AtomicString(''.join([self.email_encode(ord(c)) for c in email]))
        el.set("href", ''.join([md_util.AMP_SUBSTITUTE + f'#{ord(c):d};' for c in href]))
        return el, m.start(0), m.end(0)


class MagiclinkMentionPattern(_MagiclinkShorthandPattern):
    """Convert @mention to links."""

    ANCESTOR_EXCLUDES = ('a',)

    def handleMatch(self, m, data):
        """Handle email link patterns."""

        text = m.group('mention')[1:]
        parts = text.split(':')
        if len(parts) > 1:
            provider = parts[0]
            mention = parts[1]
        else:
            provider = self.provider
            mention = parts[0]

        if provider == 'twitter':
            warn_deprecated("The 'twitter' social provider has been deprecated, please use 'x' instead")

        el = etree.Element("a")
        el.set('href', '{}/{}'.format(self.provider_info[provider]['url'], mention))
        el.set(
            'title',
            "{} {}: {}".format(self.provider_info[provider]['provider'], self.labels.get('mention', "User"), mention)
        )
        el.set('class', f'magiclink magiclink-{provider} magiclink-mention')
        el.text = md_util.AtomicString(f'@{mention}')

        return el, m.start(0), m.end(0)


class MagiclinkRepositoryPattern(_MagiclinkShorthandPattern):
    """Convert @user/repo to links."""

    ANCESTOR_EXCLUDES = ('a',)

    def handleMatch(self, m, data):
        """Handle email link patterns."""

        text = m.group('mention')[1:]
        parts = text.split(':')
        if len(parts) > 1:
            provider = parts[0]
            user = parts[1]
        else:
            provider = self.provider
            user = parts[0]
        repo = m.group('mention_repo')

        el = etree.Element("a")
        el.set('href', '{}/{}/{}'.format(self.provider_info[provider]['url'], user, repo))
        el.set(
            'title',
            "{} {}: {}/{}".format(
                self.provider_info[provider]['provider'], self.labels.get('repository', 'Repository'), user, repo
            )
        )
        el.set('class', f'magiclink magiclink-{provider} magiclink-repository')
        el.text = md_util.AtomicString(f'{user}/{repo}')
        return el, m.start(0), m.end(0)


class MagiclinkExternalRefsPattern(_MagiclinkReferencePattern):
    """Convert repo#1, user/repo#1, repo!1, user/repo!1, repo@hash, or user/repo@hash to links."""

    ANCESTOR_EXCLUDES = ('a',)

    def handleMatch(self, m, data):
        """Handle email link patterns."""

        is_commit = m.group('commit')
        is_diff = m.group('diff')
        value = m.group('commit')[1:] if is_commit else m.group('issue')
        value2 = m.group('diff') if is_diff else None
        repo = m.group('repo')
        user = m.group('user')

        if not user:
            user = self.user

        parts = user.split(':')
        if len(parts) > 1:
            provider = parts[0]
            user = parts[1]
        else:
            provider = self.provider

        # If there is no valid user or provider, reject
        if not user:
            return None, None, None

        self.my_user = user == self.user and provider == self.provider
        self.my_repo = self.my_user and repo == self.repo

        el = etree.Element("a")
        if is_diff:
            self.process_compare(el, provider, user, repo, value, value2)
        elif is_commit:
            self.process_commit(el, provider, user, repo, value)
        else:
            if not self.process_issues(el, provider, user, repo, value):
                return m.group(0), m.start(0), m.end(0)
        return el, m.start(0), m.end(0)


class MagiclinkInternalRefsPattern(_MagiclinkReferencePattern):
    """Convert #1, !1, and commit_hash."""

    ANCESTOR_EXCLUDES = ('a',)

    def handleMatch(self, m, data):
        """Handle email link patterns."""

        # We don't have a valid provider, user, and repo, reject
        if not self.user or not self.repo:
            return None, None, None

        is_commit = m.group('commit')
        is_diff = m.group('diff')
        value = m.group('commit') if is_commit else m.group('issue')
        value2 = m.group('diff') if is_diff else None

        repo = self.repo
        user = self.user
        provider = self.provider
        self.my_repo = True
        self.my_user = True

        el = etree.Element("a")
        if is_diff:
            self.process_compare(el, provider, user, repo, value, value2)
        elif is_commit:
            self.process_commit(el, provider, user, repo, value)
        else:
            if not self.process_issues(el, provider, user, repo, value):
                return m.group(0), m.start(0), m.end(0)
        return el, m.start(0), m.end(0)


class MagiclinkExtension(Extension):
    """Add auto link and link transformation extensions to Markdown class."""

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
            'social_url_shortener': [
                False,
                "If 'True' social links are shortened - Default: False"
            ],
            'shortener_user_exclude': [
                {
                    "bitbucket": ['dashboard', 'account', 'plans', 'support', 'repo'],
                    "github": ['marketplace', 'notifications', 'issues', 'pull', 'sponsors', 'settings', 'support'],
                    "gitlab": ['dashboard', '-', 'explore', 'help', 'projects'],
                    "twitter": ['i', 'messages', 'bookmarks', 'home'],
                    "x": ['i', 'messages', 'bookmarks', 'home']
                },
                "A list of user names to exclude from URL shortening."
            ],
            'repo_url_shorthand': [
                False,
                "If 'True' repo shorthand syntax is converted to links - Default: False"
            ],
            'social_url_shorthand': [
                False,
                "If 'True' social shorthand syntax is converted to links - Default: False"
            ],
            'provider': [
                'github',
                'The base provider to use (github, gitlab, bitbucket, x) - Default: "github"'
            ],
            'labels': [
                {},
                "Title labels - Default: {}"
            ],
            'normalize_issue_symbols': [
                False,
                'Normalize issue, pull, and discussions symbols all to use # - Default: False'
            ],
            'user': [
                '',
                'The base user name to use - Default: ""'
            ],
            'repo': [
                '',
                'The base repo to use - Default: ""'
            ],
            'custom': [
                {},
                "Custom repositories hosts - Default {}"
            ]
        }
        super().__init__(*args, **kwargs)

    def setup_autolinks(self, md, config):
        """Setup auto links."""

        # Setup general link patterns
        auto_link_pattern = MagiclinkAutoPattern(RE_AUTOLINK, md)
        auto_link_pattern.config = config
        md.inlinePatterns.register(auto_link_pattern, "autolink", 120)

        link_pattern = MagiclinkPattern(RE_LINK, md)
        link_pattern.config = config
        md.inlinePatterns.register(link_pattern, "magic-link", 85)

        md.inlinePatterns.register(MagiclinkMailPattern(RE_MAIL, md), "magic-mail", 84.9)

    def setup_shorthand(self, md):
        """Setup shorthand."""

        # Setup URL shortener
        escape_chars = ['@']
        util.escape_chars(md, escape_chars)

        # Repository shorthand
        if self.git_short:
            git_ext_repo = MagiclinkRepositoryPattern(
                self.re_git_ext_repo_mentions,
                md,
                self.user,
                self.repo,
                self.provider,
                self.labels,
                self.normalize,
                self.provider_info
            )
            md.inlinePatterns.register(git_ext_repo, "magic-repo-ext-mention", 79.9)
            if not self.is_social:
                git_int_repo = MagiclinkRepositoryPattern(
                    RE_GIT_INT_REPO_MENTIONS.format(self.int_mentions),
                    md,
                    self.user,
                    self.repo,
                    self.provider,
                    self.labels,
                    self.normalize,
                    self.provider_info
                )
                md.inlinePatterns.register(git_int_repo, "magic-repo-int-mention", 79.8)

        # Mentions
        pattern = RE_ALL_EXT_MENTIONS.format('|'.join(self.ext_mentions))
        git_mention = MagiclinkMentionPattern(
            pattern,
            md,
            self.user,
            self.repo,
            self.provider,
            self.labels,
            self.normalize,
            self.provider_info
        )
        md.inlinePatterns.register(git_mention, "magic-ext-mention", 79.7)

        git_mention = MagiclinkMentionPattern(
            RE_INT_MENTIONS.format(self.int_mentions),
            md,
            self.user,
            self.repo,
            self.provider,
            self.labels,
            self.normalize,
            self.provider_info
        )
        md.inlinePatterns.register(git_mention, "magic-int-mention", 79.6)

        # Other project refs
        if self.git_short:
            git_ext_refs = MagiclinkExternalRefsPattern(
                self.re_git_ext_refs,
                md,
                self.user,
                self.repo,
                self.provider,
                self.labels,
                self.normalize,
                self.provider_info
            )
            md.inlinePatterns.register(git_ext_refs, "magic-ext-refs", 79.5)
            if not self.is_social:
                git_int_refs = MagiclinkExternalRefsPattern(
                    RE_GIT_INT_EXT_REFS.format(self.int_mentions),
                    md,
                    self.user,
                    self.repo,
                    self.provider,
                    self.labels,
                    self.normalize,
                    self.provider_info
                )
                md.inlinePatterns.register(git_int_refs, "magic-int-refs", 79.4)
                git_int_micro_refs = MagiclinkInternalRefsPattern(
                    RE_GIT_INT_MICRO_REFS,
                    md,
                    self.user,
                    self.repo,
                    self.provider,
                    self.labels,
                    self.normalize,
                    self.provider_info
                )
                md.inlinePatterns.register(git_int_micro_refs, "magic-int-micro-refs", 79.3)

    def setup_shortener(
        self,
        md,
        config
    ):
        """Setup shortener."""

        shortener = MagicShortenerTreeprocessor(
            md,
            self.base_url,
            self.base_user_url,
            self.labels,
            self.normalize,
            self.repo_shortner,
            self.social_shortener,
            self.custom_shortners,
            self.shortener_exclusions,
            self.provider,
            self.provider_info
        )
        shortener.config = config
        md.treeprocessors.register(shortener, "magic-repo-shortener", 9.9)

    def get_base_urls(self, config):
        """Get base URLs."""

        base_url = ''
        base_user_url = ''

        if self.is_social:
            return base_url, base_user_url

        if self.user and self.repo:
            base_url = '{}/{}/{}/'.format(self.provider_info[self.provider]['url'], self.user, self.repo)
            base_user_url = '{}/{}/'.format(self.provider_info[self.provider]['url'], self.user)

        return base_url, base_user_url

    def extendMarkdown(self, md):
        """Add support for turning html links and emails to link tags."""

        config = self.getConfigs()

        # Setup repo variables
        self.user = config.get('user', '')
        self.repo = config.get('repo', '')
        self.provider = config.get('provider', 'github')
        self.labels = config.get('labels', {})
        self.normalize = config.get('normalize_issue_symbols', False)
        self.is_social = self.provider in SOCIAL_PROVIDERS
        self.git_short = config.get('repo_url_shorthand', False)
        self.social_short = config.get('social_url_shorthand', False)
        self.repo_shortner = config.get('repo_url_shortener', False)
        self.social_shortener = config.get('social_url_shortener', False)
        self.shortener_exclusions = {k: set(v) for k, v in DEFAULT_EXCLUDES.items()}

        self.provider_info = PROVIDER_INFO.copy()
        custom_provider = config.get('custom', {})
        excludes = config.get('shortener_user_exclude', {})
        self.custom_shortners = {}
        external_users = [RE_GITHUB_EXT_MENTIONS, RE_GITLAB_EXT_MENTIONS, RE_BITBUCKET_EXT_MENTIONS]
        for custom, entry in custom_provider.items():
            if not RE_CUSTOM_NAME.match(custom):
                raise ValueError(
                    f"Name '{custom}' not allowed, provider name must contain only letters and numbers"
                )
            if custom not in self.provider_info:
                self.provider_info[custom] = create_provider(entry['type'], entry['host'])
                self.provider_info[custom]['provider'] = entry['label']
                self.custom_shortners[custom] = {
                    'repo': re.compile(
                        r'(?xi)^{}/?$'.format(
                            create_repo_link_pattern(entry['type'], entry['host'], entry.get('www', True))
                        )
                    ),
                    'user': re.compile(
                        r'(?xi)^{}/?$'.format(
                            create_user_link_pattern(entry['type'], entry['host'], entry.get('www', True))
                        )
                    )
                }
                if custom not in excludes:
                    excludes[custom] = excludes.get(entry['type'], [])
                external_users.append(create_ext_mentions(custom, entry['type']))

        self.re_git_ext_repo_mentions = RE_GIT_EXT_REPO_MENTIONS.format('|'.join(external_users))
        self.re_git_ext_refs = RE_GIT_EXT_REFS.format('|'.join(external_users))

        for key, value in config.get('shortener_user_exclude', {}).items():
            if key in self.provider_info and isinstance(value, (list, tuple, set)):
                self.shortener_exclusions[key] = {x.lower() for x in value}

        # Ensure valid provider
        if self.provider not in self.provider_info:
            self.provider = 'github'

        self.setup_autolinks(md, config)

        if self.git_short or self.social_short:
            self.ext_mentions = []
            if self.git_short:
                self.ext_mentions.extend(external_users)

            if self.social_short:
                self.ext_mentions.append(RE_X_EXT_MENTIONS)
                self.ext_mentions.append(RE_TWITTER_EXT_MENTIONS)
            self.int_mentions = self.provider_info[self.provider]['user_pattern']
            self.setup_shorthand(md)

        # Setup link post processor for shortening repository links
        if self.repo_shortner or self.social_shortener:
            self.base_url, self.base_user_url = self.get_base_urls(config)
            self.setup_shortener(md, config)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return MagiclinkExtension(*args, **kwargs)
