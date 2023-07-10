[:octicons-file-code-24:][_magiclink]{: .source-link }

# MagicLink

/// note | Icons
This documentation implements additional styling with CSS that inserts icons before special links, such as GitHub,
logos, bug icons, etc. MagicLink does not inject icons or CSS to insert icons, but it is left to the user to
implement (if desired) via the provided [classes](#css). User's are free to reference this
[documentation's source][magiclink-icons] to learn how.
///

## Overview

MagicLink is an extension that provides a number of useful link related features. MagicLink can auto-link HTML, FTP, and
email links. It can auto-convert repository links (GitHub, GitLab, and Bitbucket) and display them in a more concise,
shorthand format. MagicLink can also be configured to directly auto-link the aforementioned shorthand format.

If you happen to have some conflicts with syntax for a specific case, you can always revert to the old auto-link format
as well: `#!md <https://www.link.com>`. If enabled, repository link shortening will be applied to the the angle
bracketed auto-link format as well.

/// tip | SaneHeaders
It is also recommended to use [SaneHeaders](./saneheaders.md) when using MagicLink to avoid problems when specifying
a repository bug (using the syntax `#1`) at the start of a line. Python Markdown, by default, will treat `#1` as a
header if detected at the start of a line without SaneHeaders.
///

The MagicLink extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.magiclink'])
```

## Auto-Linking

MagicLink supports auto-linking HTTP, FTP and email links. You can specify these links in raw text and they should get
auto-linked. There are some limitations placed on MagicLink to keep it from aggressively auto-linking text that is not
part of links. If you have a link that cannot be detected, you can always use the old style angle bracketed link format:
`#!md <https://www.link.com>`.

```text title="Auto-Linking"
- Just paste links directly in the document like this: https://google.com.
- Or even an email address: fake.email@email.com.
```

/// html | div.result
```md-render
---
extensions:
- pymdownx.magiclink
- pymdownx.saneheaders
- markdown.extensions.attr_list

extension_configs:
  pymdownx.magiclink:
    repo_url_shortener: true
    repo_url_shorthand: true
    social_url_shorthand: true
    social_url_shortener: true
    user: facelessuser
    repo: pymdown-extensions
---
-   Just paste links directly in the document like this: https://google.com.
-   Or even an email address: fake.email@email.com{.magiclink-ignore}.
```
///

## Shorthand Links


```md-render
---
extensions:
- pymdownx.magiclink
- pymdownx.saneheaders
- markdown.extensions.attr_list

extension_configs:
  pymdownx.magiclink:
    repo_url_shortener: true
    repo_url_shorthand: true
    social_url_shorthand: true
    social_url_shortener: true
    user: facelessuser
    repo: pymdown-extensions
---
MagicLink supports shorthand references for GitHub, GitLab, and Bitbucket issues (#1{.magiclink-ignore}), pull/merge
requests (!13{.magiclink-ignore}), GitHub Discussion (?1173{.magiclink-ignore}), commits
(7d1b1902ea7fe00043a249564ed5032f08dd7152{.magiclink-ignore}), and compares
(e2ed7e0b3973f3f9eb7a26b8ef7ae514eebfe0d2...90b6fb8711e75732f987982cc024e9bb0111beac{.magiclink-ignore}). You can also
reference repositories (@facelessuser/pymdown-extensions{.magiclink-ignore}) and users
(@facelessuser{.magiclink-ignore}). Mentions also works for social media (only Twitter is supported at this time).
```

The syntax used is actually very similar to GitLab's syntax. GitLab was chosen as its syntax bridges the gaps between
the three providers. GitLab and Bitbucket require a pull specific syntax while GitHub does not have one. Also, while
GitHub uses `#<num>` for issues, pulls, and discussions, the idea of using a different symbol for issue
types gives us the context we need to generate the correct links for issues vs pulls, etc.

### Configuring

To enable shorthand syntax for code repository providers and social media providers, enable `repo_url_shorthand` and
`social_url_shorthand` respectively in the [options](#options).

To use this feature you must first specify in the [options](#options) your `provider` to which all shorthand references
are relative to, but you will still be able to reference outside of your defaults. And if you are specifying a code
repository provider as your default, you must also specify the `user` and `repo` (repository) which adds more context
and allows you to shorten the syntax even more for issues relating to your default `user` and/or `repo`. This is useful
if you are using MagicLink to write documentation for a project that is hosted on one of the supported code repository
providers.

If you are using this extension more generally, it may make more sense to set a social media provider as the default
`provider`. There is no need to set a `user` or `repo` for a social media provider as the context is not useful for
mentions. You will still be able to reference repository links with shorthand if it enabled, albeit in a longer format.

/// warning
Links are not verified, so make sure you are specifying valid issues, repositories, and users as they will be
auto-linked even if they are not valid.
///

### Mentions

Mentions of other users are performed with the following syntax: `@{user}`. To reference a provider other than your
default, use the format `@{provider}:{user}`

```text title="Mentions"
@facelessuser

@twitter:twitter
```

/// html | div.result
```md-render
---
extensions:
- pymdownx.magiclink
- pymdownx.saneheaders
- markdown.extensions.attr_list

extension_configs:
  pymdownx.magiclink:
    repo_url_shortener: true
    repo_url_shorthand: true
    social_url_shorthand: true
    social_url_shortener: true
    user: facelessuser
    repo: pymdown-extensions
---
@facelessuser

@twitter:twitter
```
///

For code repository providers, you can also mention repositories.  This feature is actually inspired by the GitHub only
extension @Python-Markdown/github-links, which performs *similar* auto-linking.  The syntax to auto-link a repository
with mentioning is very similar to auto-linking a user, except you append the repository to the user name like so:
`@{user}/{repo}`. If specifying a non-default provider, the form would look like: `@{provider}:{user}/{repo}`. The
output for repository mentions omits the `@` symbol and will just show the user and repository, but you are free to
style it with CSS to make it stand out more like has been done in this document.

```text title="Repository Mentions"
@facelessuser/pymdown-extensions

@gitlab:pycqa/flake8-engine
```

/// html | div.result
```md-render
---
extensions:
- pymdownx.magiclink
- pymdownx.saneheaders
- markdown.extensions.attr_list

extension_configs:
  pymdownx.magiclink:
    repo_url_shortener: true
    repo_url_shorthand: true
    social_url_shorthand: true
    social_url_shortener: true
    user: facelessuser
    repo: pymdown-extensions
---
@facelessuser/pymdown-extensions{.magiclink-ignore}

@gitlab:pycqa/flake8-engine{.magiclink-ignore}
```
///

### Issues, Pull Requests, and Discussions

Issues, pull requests, and GitHub discussions are specified with `#{num}`, `!{num}`, and `?{num}` respectively. When
specified in this manner, the links will assume the default repository and default user for generated links.

To specify an issue for a non-default repository under the default user, prefix the repository: `{repo}#{num}`.

To specify a repository under a non-default user, prefix both the user and repository: `{user}/{repo}#{num}`.

Lastly, to reference an external provider, use the format `{provider}:{user}/{repo}#{num}`.

The syntax was borrowed and adapted from GitLab as they use `!{num}` for pulls and `#{num}` for issues, `?{num}` is our
own take for discussions. This syntax was
mainly used to ensure we could provide context to the link generator. When rendering the actual links in your documents,
it will use the syntax associated with the specified provider. If this is unsatisfactory, you can override this behavior
with the `icons` option and all links will will use the same specified convention on output regardless of the provider.

```text title="Issues"
#1

backrefs#1

Python-Markdown/markdown#1

gitlab:pycqa/flake8-engine#21

!13

backrefs!4

Python-Markdown/markdown!598

gitlab:pycqa/infrastructure!1
```

/// html | div.result
```md-render
---
extensions:
- pymdownx.magiclink
- pymdownx.saneheaders
- markdown.extensions.attr_list

extension_configs:
  pymdownx.magiclink:
    repo_url_shortener: true
    repo_url_shorthand: true
    social_url_shorthand: true
    social_url_shortener: true
    user: facelessuser
    repo: pymdown-extensions
---
#1{.magiclink-ignore}

backrefs#1{.magiclink-ignore}

Python-Markdown/markdown#1{.magiclink-ignore}

gitlab:pycqa/flake8-engine#21{.magiclink-ignore}

!13{.magiclink-ignore}

backrefs!4{.magiclink-ignore}

Python-Markdown/markdown!598{.magiclink-ignore}

gitlab:pycqa/infrastructure!1{.magiclink-ignore}
```
///


/// note | Note
GitHub actually gives pull requests and issues unique values while GitLab and Bitbucket can have pulls with the same
ID as an issue. So with GitHub, you can use `#{num}` format for both issues and pulls, and GitHub will redirect you
to the appropriate issue or pull.

GitLab and Bitbucket **must** specify pulls different from issues, hence the `!13` format. Though GitHub doesn't
*need* to use the pull format, you can if you like. This format was actually borrowed from GitLab.
///

### Commits

Commit shorthand syntax is simply the 40 character commit hash value: `{hash}`. And much like issues and pull requests,
you can denote a repository under the default user with `{repo}@{hash}` and a repository under a non-default user with
`{user}/{repo}@{hash}`. Lastly, to reference an external provider, use the format `{provider}:{user}/{repo}@{hash}`. If
the default provider is a social media provider, then only the latter syntax can be used.

```text title="Commits"
181c06d1f11fa29961b334e90606ed1f1ec7a7cc

backrefs@cb4ecc5e7d8f7cdff0bb4482174f2ff0dcc35c61

Python-Markdown/markdown@de5c696f94e8dde242c29d4be50b7bbf3c17fedb

gitlab:pycqa/flake8-engine@ee18ac981e3dbaf3365a817663834c7b547f83cb
```

/// html | div.result
```md-render
---
extensions:
- pymdownx.magiclink
- pymdownx.saneheaders
- markdown.extensions.attr_list

extension_configs:
  pymdownx.magiclink:
    repo_url_shortener: true
    repo_url_shorthand: true
    social_url_shorthand: true
    social_url_shortener: true
    user: facelessuser
    repo: pymdown-extensions
---
181c06d1f11fa29961b334e90606ed1f1ec7a7cc{.magiclink-ignore}

backrefs@cb4ecc5e7d8f7cdff0bb4482174f2ff0dcc35c61{.magiclink-ignore}

Python-Markdown/markdown@de5c696f94e8dde242c29d4be50b7bbf3c17fedb{.magiclink-ignore}

gitlab:pycqa/flake8-engine@ee18ac981e3dbaf3365a817663834c7b547f83cb{.magiclink-ignore}
```
///

### Diff/Compare

GitLab offers a useful shorthand to specify links to compare differences between two commits. This has been adopted for
all the supported repository providers.

Specifying a compare link is very similar to specifying a commit link except you must specify the older hash and the
newer hash separated by `...`: `{hash1}...{hash2}`. To specify a compare for a non-default repository under the default
user, prefix the repository: `{repo}@{hash1}...{hash2}`. And to specify a compare under a non-default user, prefix both
the user and repository: `{user}/{repo}@{hash1}...{hash2}`. Lastly, to reference an external provider, use the format
`{provider}:{user}/{repo}@{hash1}...{hash2}`.

```text title="Comparisons"
e2ed7e0b3973f3f9eb7a26b8ef7ae514eebfe0d2...90b6fb8711e75732f987982cc024e9bb0111beac

backrefs@88c6238a1c2cf71a96eb9abb4b0213f79d6ca81f...cb4ecc5e7d8f7cdff0bb4482174f2ff0dcc35c61

Python-Markdown/markdown@007bd2aa4c184b28f710d041a0abe78bffc0ec2e...de5c696f94e8dde242c29d4be50b7bbf3c17fedb

gitlab:pycqa/flake8-engine@0b063a10249558ede919bcd7f67c6aa563ba74ab...ee18ac981e3dbaf3365a817663834c7b547f83cb
```

/// html | div.result
```md-render
---
extensions:
- pymdownx.magiclink
- pymdownx.saneheaders
- markdown.extensions.attr_list

extension_configs:
  pymdownx.magiclink:
    repo_url_shortener: true
    repo_url_shorthand: true
    social_url_shorthand: true
    social_url_shortener: true
    user: facelessuser
    repo: pymdown-extensions
---
e2ed7e0b3973f3f9eb7a26b8ef7ae514eebfe0d2...90b6fb8711e75732f987982cc024e9bb0111beac{.magiclink-ignore}

backrefs@88c6238a1c2cf71a96eb9abb4b0213f79d6ca81f...cb4ecc5e7d8f7cdff0bb4482174f2ff0dcc35c61{.magiclink-ignore}

Python-Markdown/markdown@007bd2aa4c184b28f710d041a0abe78bffc0ec2e...de5c696f94e8dde242c29d4be50b7bbf3c17fedb{.magiclink-ignore}

gitlab:pycqa/flake8-engine@0b063a10249558ede919bcd7f67c6aa563ba74ab...ee18ac981e3dbaf3365a817663834c7b547f83cb{.magiclink-ignore}
```
///

## Repository Link Shortener

MagicLink can also recognize issue, pull request, commit, and compare links, and render them in the same output format
as the [repository shortcut links](#shorthand-links) feature.

If we specify long form URLs from external providers, they will be shortened appropriately.

```text title="External Provider"
-   https://github.com/facelessuser
-   https://github.com/facelessuser/pymdown-extensions
-   https://gitlab.com/pycqa/flake8-engine/-/issues/21
-   https://bitbucket.org/mrabarnett/mrab-regex/issues/260/extremely-slow-matching-using-ignorecase
```

/// html | div.result
```md-render
---
extensions:
- pymdownx.magiclink
- pymdownx.saneheaders
- markdown.extensions.attr_list

extension_configs:
  pymdownx.magiclink:
    repo_url_shortener: true
    repo_url_shorthand: true
    social_url_shorthand: true
    social_url_shortener: true
    user: facelessuser
    repo: pymdown-extensions
---
-   <https://github.com/facelessuser>{.magiclink-ignore}
-   <https://github.com/facelessuser/pymdown-extensions>{.magiclink-ignore}
-   <https://gitlab.com/pycqa/flake8-engine/-/issues/21>{.magiclink-ignore}
-   <https://bitbucket.org/mrabarnett/mrab-regex/issues/260/extremely-slow-matching-using-ignorecase>{.magiclink-ignore}
```
///

When specifying links that reference the configured `provider`, `user`, and `repo`, some links will be shortened
differently in light of that context.

```text title="Internal Provider"
-   https://github.com/facelessuser/pymdown-extensions/issues/1
-   https://github.com/facelessuser/pymdown-extensions/pull/13
-   https://github.com/facelessuser/pymdown-extensions/commit/3f6b07a8eeaa9d606115758d90f55fec565d4e2a
-   https://github.com/facelessuser/pymdown-extensions/compare/e2ed7e0b3973f3f9eb7a26b8ef7ae514eebfe0d2...90b6fb8711e75732f987982cc024e9bb0111beac
-   https://github.com/facelessuser/Rummage/commit/181c06d1f11fa29961b334e90606ed1f1ec7a7cc
```

/// html | div.result
```md-render
---
extensions:
- pymdownx.magiclink
- pymdownx.saneheaders
- markdown.extensions.attr_list

extension_configs:
  pymdownx.magiclink:
    repo_url_shortener: true
    repo_url_shorthand: true
    social_url_shorthand: true
    social_url_shortener: true
    user: facelessuser
    repo: pymdown-extensions
---
-   <https://github.com/facelessuser/pymdown-extensions/issues/1>{.magiclink-ignore}
-   <https://github.com/facelessuser/pymdown-extensions/pull/13>{.magiclink-ignore}
-   <https://github.com/facelessuser/pymdown-extensions/commit/3f6b07a8eeaa9d606115758d90f55fec565d4e2a>{.magiclink-ignore}
-   <https://github.com/facelessuser/pymdown-extensions/compare/e2ed7e0b3973f3f9eb7a26b8ef7ae514eebfe0d2...90b6fb8711e75732f987982cc024e9bb0111beac>{.magiclink-ignore}
-   <https://github.com/facelessuser/Rummage/commit/181c06d1f11fa29961b334e90606ed1f1ec7a7cc>{.magiclink-ignore}
```
///

MagicLink will shorten user name and repository name links, but every site has some links that will conflict, or better
stated, will have links that follow the pattern of user name and repository name links, but are not actually either.
For example, `https://github.com/support` is not a user name, nor are any links under `support` repository names. By
default, MagicLink has provided a list of exclusions for each provider to avoid treating such links as a user name or
repository name. You can override them and add more via the option [`shortener_user_exclude`](#user-excludes).

/// new | New 7.0
MagicLink added user name and repository name link shortening along.
///

## CSS

For normal links, no classes are added to the anchor tags. For repository links, `magiclink` will be added as a class.
Also, an additional class will be added for each repository link type and provider.

Link\ Type           | Class
-------------------- | -----
General              | `magiclink`
Mentions             | `magiclink-mention`
Repository\ Mentions | `magiclink-repository`
Issues               | `magiclink-issue`
Pulls                | `magiclink-pull`
Commits              | `magiclink-commit`
Compares             | `magiclink-compare`
GitHub               | `magiclink-github`
Bitbucket            | `magiclink-bitbucket`
GitLab               | `magiclink-gitlab`
Twitter              | `magiclink-twitter`

/// tip | Styling Links
With a little bit of CSS^[†](#_fn_1)^, you can also add icons in front: 7d1b1902ea7fe00043a249564ed5032f08dd7152,
e2ed7e0b3973f3f9eb7a26b8ef7ae514eebfe0d2...90b6fb8711e75732f987982cc024e9bb0111beac, etc.

You can also use the [`normalize_issue_symbols`](#options) option to make issue type links all render with `#` and
then use CSS^[†](#_fn_1)^ to add fancy icons to distinguish them: #1, !13, and ?1173.

^†^{#\_fn_1} _CSS is not included and the examples are just to illustrate what is possible, and to explain why our
documents will often have links with special icons._
///

## Options

Option                          | Type   | Default                     | Description
------------------------------- | ------ | --------------------------- | -----------
`hide_protocol`                 | bool   | `#!py3 False`               | If `True`, links are displayed without the initial `ftp://`, `http://`, `https://`, or `ftps://`.
`repo_url_shortener`            | bool   | `#!py3 False`               | If `True`, GitHub, Bitbucket, and GitLab commit, pull, and issue links are are rendered in a shorthand syntax.
`social_url_shortener`          | bool   | `#!py3 False`               | if `True`, Twitter user links are rendered in a shorthand syntax.
`shortener_user_exclude`        | dict   | [See below](#user-excludes) | Specifies a list of user names to avoid when attempting to shorten links. See [User Excludes](#user-excludes) for more info.
`repo_url_shorthand`            | bool   | `#!py3 False`               | If `True`, you can directly use a shorthand syntax to represent commit, pull, issue, and mention links for repository providers and they will be auto-linked.
`social_url_shorthand`          | bool   | `#!py3 False`               | If `True`, you can directly use a shorthand syntax to represent mention links for social media providers and they will be auto-linked.
`provider`                      | string | `#!py3 'github'`            | The provider to use for repository shorthand syntax and shortener.
`user`                          | string | `#!py3 ''`                  | The default user name to use for the specified provider.
`repo`                          | string | `#!py3 ''`                  | The default repository name to use for the specified user and provider.
`labels`                        | dict   | `#!py3 {}`                  | A dictionary for overriding repository link title text. See [Labels](#labels) for more info.
`normalize_issue_symbols`       | bool   | `#!py3 False`               | Normalize issue type links (issues, pulls, and discussions) to all use `#` instead of the respective `#`, `!`, and `?`.

### User Excludes

Defaults for `shortener_user_exclude`:

```py
{
    "bitbucket": ['dashboard', 'account', 'plans', 'support', 'repo'],
    "github": ['marketeplace', 'notifications', 'issues', 'pull', 'sponsors', 'settings', 'support'],
    "gitlab": ['dashboard', '-', 'explore', 'help', 'projects'],
    "twitter": ['i', 'messages', 'bookmarks', 'home']
}
```

When overriding, only the providers that are explicitly provided get overridden.

### Labels

By default, MagicLink provides titles for the repository links in the form `{provider} {label}: {info}`. You can specify
different values for `{label}` by configuring the `labels` option.

The default values are:

```js
    {
        'commit': 'Commit',
        'compare': 'Compare',
        'issue': 'Issue',
        'pull': 'Pull Request',
        'mention': 'User',
        'repository': 'Repository'
    }
```

You only need to provide the options you wish to override. Assume we wanted to adopt the GitLab terminology for pull
requests, we could simply set `labels` to:

```js
    {
        'pull': 'Merge Request'
    }
```
