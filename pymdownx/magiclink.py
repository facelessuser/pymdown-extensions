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
import re

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

RE_AUTOLINK = r'(?i)<((?:ht|f)tps?://[^>]*)>'

RE_REPO_LINK = re.compile(
    r'''(?xi)
    (?:
        (?P<github>(?P<github_base>https://(?:w{3}\.)?github.com/(?P<github_user_repo>[^/]+/[^/]+))/
            (?:issues/(?P<github_issue>\d+)/?|
               commit/(?P<github_commit>[\da-f]+)/?)) |

        (?P<bitbucket>(?P<bitbucket_base>https://(?:w{3}\.)?bitbucket.org/(?P<bitbucket_user_repo>[^/]+/[^/]+))/
            (?:issues/(?P<bitbucket_issue>\d+)(?:/?|/[^/]*/?)|
               commits/commit/(?P<bitbucket_commit>[\da-f]+)/?)) |

        (?P<gitlab>(?P<gitlab_base>https://(?:w{3}\.)?gitlab.com/(?P<gitlab_user_repo>[^/]+/[^/]+))/
            (?:issues/(?P<gitlab_issue>\d+)/? |
               commit/(?P<gitlab_commit>[\da-f]+)/?))
    )
    '''
)


class MagicShortenerTreeprocessor(Treeprocessor):
    """Treeprocessor that finds repo issue and commit links and shortens them."""

    def shorten(self, link, my_repo, is_commit, user_repo, value, url, hash_size):
        """Shorten url."""

        if is_commit:
            # user/repo@`hash`
            text = '' if my_repo else user_repo + '@'
            link.text = md_util.AtomicString(text)

            # Need a root with an element for things to get processed.
            # Send the `value` through and retreive it from the p element.
            # Pop it off and add it to the link.
            el = md_util.etree.Element('div')
            p = md_util.etree.SubElement(el, 'p')
            p.text = '`%s`' % value[0:hash_size]
            el = self.markdown.treeprocessors['inline'].run(el)
            p = list(el)[0]
            for child in list(p):
                link.append(child)
                p.remove(child)
        else:
            # user/repo#issue
            link.text = ('#' + value) if my_repo else (user_repo + '#' + value)

    def run(self, root):
        """Shorten popular git repository links."""

        base = self.config.get('base_repo_url', '').rstrip('/')
        hide_protocol = self.config['hide_protocol']

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
            if text == href or (is_magic and hide_protocol and ('https://' + text) == href):
                m = RE_REPO_LINK.match(href)
                if m:
                    # Set provider specific variables
                    if m.group('github'):
                        provider = 'github'
                        hash_size = 7
                    elif m.group('bitbucket'):
                        provider = 'bitbucket'
                        hash_size = 7
                    elif m.group('gitlab'):
                        provider = 'gitlab'
                        hash_size = 8

                    # See if these links are from the specified repo.
                    my_repo = m.group(provider + '_base') == base
                    if not my_repo and hide_protocol:
                        my_repo = m.group(provider + '_base') == ('https://' + base)

                    # Gather info about link type
                    is_commit = m.group(provider + '_commit') is not None
                    value = m.group(provider + '_commit') if is_commit else m.group(provider + '_issue')

                    # All right, everything set, let's shorten.
                    self.shorten(
                        link,
                        my_repo,
                        is_commit,
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

        shorten = self.config.get('repo_url_shortener', False)
        el = md_util.etree.Element("a")
        el.text = md_util.AtomicString(m.group(2))
        if m.group("www"):
            href = "http://%s" % m.group(2)
        else:
            href = m.group(2)
            if self.config['hide_protocol']:
                el.text = md_util.AtomicString(el.text[el.text.find("://") + 3:])

        if shorten:
            el.set('magiclink', '1')
        el.set("href", self.sanitize_url(self.unescape(href.strip())))
        return el


class MagiclinkAutoPattern(Pattern):
    """Return a link Element given an autolink `<http://example/com>`."""

    def handleMatch(self, m):
        """Return link optionally without protocol."""

        shorten = self.config.get('repo_url_shortener', False)
        el = md_util.etree.Element("a")
        el.set('href', self.unescape(m.group(2)))
        el.text = md_util.AtomicString(m.group(2))
        if self.config['hide_protocol']:
            el.text = md_util.AtomicString(el.text[el.text.find("://") + 3:])
        if shorten:
            el.attrib['magiclink'] = '1'
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
            'base_repo_url': [
                '',
                'The base repo url to use - Default: ""'
            ]
        }
        super(MagiclinkExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Add support for turning html links and emails to link tags."""

        config = self.getConfigs()
        auto_link_pattern = MagiclinkAutoPattern(RE_AUTOLINK, md)
        auto_link_pattern.config = config
        link_pattern = MagiclinkPattern(RE_LINK, md)
        link_pattern.config = config
        md.inlinePatterns['autolink'] = auto_link_pattern
        md.inlinePatterns.add("magic-link", link_pattern, "<entity")
        md.inlinePatterns.add("magic-mail", MagicMailPattern(RE_MAIL, md), "<entity")
        if config.get('repo_url_shortener', False):
            shortener = MagicShortenerTreeprocessor(md)
            shortener.config = config
            md.treeprocessors.add("magic-repo-shortener", shortener, "<prettify")


def makeExtension(*args, **kwargs):
    """Return extension."""

    return MagiclinkExtension(*args, **kwargs)
