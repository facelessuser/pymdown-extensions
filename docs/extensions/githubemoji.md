# GithubEmoji {: .doctitle}
Github Emoji syntax.

---

## Overview
GithubEmoji adds support for GFM emojis.  Using GFM&rsquo;s emoji syntax, this extension will create image links to Github's emoji assets: `:octocat:` --> :octocat:.  It adds support for all of Github's supported emojis (at the time of writing this).

## Options
| Option    | Type | Default |Description |
|-----------|------|---------|------------|
| css_class | string | 'emoji' | Insert the given class name into the img tag.  To disable class name insertion, provide an empty string. |
| offline | bool | True | When enabled, GithubEmoji will use the last generated emoji table from Github at the time of release.  If for some reason Github changes things and you **must** have the latest, you can set this to `False` and GithubEmoji will request the latest table via the [Github API](https://developer.github.com/v3/emojis/).  It does this with the [requests](http://docs.python-requests.org/en/latest/) module, and it will only be in memory.  As requests is not a required module, if you do not have requests installed, this will default back to offline. |

!!! note "Note"
    Since 'online' calls through the Github API are done anonymously, Github will limit the caller to approximately 60 calls in an hour.  There are no plans at this time to add [OAuth support](https://developer.github.com/v3/oauth/).  If the emoji table gets out of date, it is recommended to either send a pull request, or create an issue that notes it is out of date.

    To update for a pull request:

    1. Fork the project.

    2. From the directory of `githubemoji.py`, run the script directly:

        ```
        python githubemoji.py
        ```

    3. Commit.

    4. Create a pull request.

## Examples
```
Github :octocat: emojis are very useful :thumbsup:.
```

Github :octocat: emojis are very useful :thumbsup:.

*[GFM]:  Github Flavored Markdown
