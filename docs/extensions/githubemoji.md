# GithubEmoji {: .doctitle}
Github Emoji syntax.

---

## Overview

!!! warning "Deprecated"
    This extension has been deprecated in version `1.3.0`.  Users are encouraged to use the [emoji extension](./emoji.md) instead.  This extension will be removed at some time in the future.

GithubEmoji adds support for GFM emojis.  Using GFM&rsquo;s emoji syntax, this extension will create image links to Github's emoji assets: `:octocat:` --> :octocat:.  It adds support for all of Github's supported emojis (at the time of writing this).

## Options
| Option    | Type | Default |Description |
|-----------|------|---------|------------|
| css_class | string | 'emoji' | Insert the given class name into the img tag.  To disable class name insertion, provide an empty string. |
| offline | bool | True | When enabled, GithubEmoji will use the last generated emoji table from Github at the time of release.  If for some reason Github changes things and you **must** have the latest, you can set this to `False` and GithubEmoji will request the latest table via the [Github API](https://developer.github.com/v3/emojis/).  It does this with the [requests](http://docs.python-requests.org/en/latest/) module, and it will only be in memory.  As requests is not a required module, if you do not have requests installed, this will default back to offline. |

!!! note "Note"
    Since 'online' calls through the Github API are done anonymously, Github will limit the caller to approximately 60 calls in an hour.  There are no plans at this time to add [OAuth support](https://developer.github.com/v3/oauth/).

## Examples
```
Github :octocat: emojis are very useful :thumbsup:.
```

Github :octocat: emojis are very useful :thumbsup:.

*[GFM]:  Github Flavored Markdown
