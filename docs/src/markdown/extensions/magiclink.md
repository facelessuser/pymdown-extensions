# MagicLink

## Overview

MagicLink is an extension that provides a number of useful link related features. MagicLink can auto-link HTML, FTP, and email links. It can auto-convert repository links (GitHub, GitLab, and Bitbucket) and display them in a more concise, shorthand format. MagicLink can also be configured to directly auto-link the aforementioned shorthand format.

If you happen to have some conflicts with syntax for a specific case, you can always revert to the old auto-link format as well: `#!md <https://www.link.com>`. If enabled, repository link shortening will be applied to the the angle bracketed auto-link format as well.

## Auto-Linking

MagicLink supports auto-linking HTTP, FTP and email links. You can specify these links in raw text and they should get auto-linked. There are some limitations placed on MagicLink to keep it from aggressively auto-linking text that is not part of links. If you have a link that cannot be detected, you can always use the old style angle bracketed link format: `#!md <https://www.link.com>`.

!!! example "Auto-Linking Example"

    ```
    - Just paste links directly in the document like this: https://google.com.
    - Or even an email address: fake.email@email.com.
    ```

    - Just paste links directly in the document like this: https://google.com.
    - Or even an email address: fake.email@email.com.

## Shorthand Links

MagicLink supports shorthand references for GitHub, GitLab, and Bitbucket issues (#1), pull/merge requests (!13), commits (7d1b1902ea7fe00043a249564ed5032f08dd7152), and compares (e2ed7e0b3973f3f9eb7a26b8ef7ae514eebfe0d2...90b6fb8711e75732f987982cc024e9bb0111beac). You can also reference repositories (@facelessuser/pymdown-extensions) and it supports mentioning users (@facelessuser). Mentions also works for social media (only Twitter is supported at this time).

The syntax for repository providers is actually very similar to GitLab's syntax. GitLab was chosen as its syntax bridges the gaps between the three providers. GitLab and Bitbucket require a pull specific syntax while GitHub does not have one. I also preferred the subtle differences in GitLab's commit references as it was consistent with pull and issue syntax.

### Configuring

To enable shorthand syntax for code repository providers and social media providers, enable `repo_url_shorthand` and `social_url_shorthand` respectively in the [options](#options).

To use this feature you must first specify in the [options](#options) your `provider` to which all shorthand references are relative to, but you will still be able to reference outside of your defaults. And if you are specifying a code repository provider as your default, you must also specify the `user` and `repo` (repository) which adds more context and allows you to shorten the syntax even more for issues relating to your default `user` and/or `repo`. This is useful if you are using MagicLink to write documentation for a project that is hosted on one of the supported code repository providers.

If you are using this extension more generally, it may make more sense to set a social media provider as the default `provider`. There is no need to set a `user` or `repo` for a social media provider as the context is not useful for mentions. You will still be able to reference repository links with shorthand if it enabled, albeit in a longer format.

!!! warning
    Links are not verified, so make sure you are specifying valid issues, repositories, and users as they will be auto-linked even if they are not valid.

### Mentions

Mentions of other users are performed with the following syntax: `@{user}`. To reference a provider other than your default, use the format `@{provider}:{user}`

!!! example "Mention Example"

    ```
    @facelessuser

    @twitter:twitter
    ```

    @facelessuser

    @twitter:twitter

For code repository providers, you can also mention repositories.  This feature is actually inspired by the GitHub only extension @Python-Markdown/github-links, which performs *similar* auto-linking.  The syntax to auto-link a repository with mentioning is very similar to auto-linking a user, except you append the repository to the user name like so: `@{user}/{repo}`. If specifying a non-default provider, the form would look like: `@{provider}:{user}/{repo}`. The output for repository mentions omits the `@` symbol and will just show the user and repository, but you are free to style it with CSS to make it stand out more like has been done in this document.

!!! example "Repository Mention Example"

    ```
    @facelessuser/pymdown-extensions

    @gitlab:pycqa/flake8
    ```

    @facelessuser/pymdown-extensions

    @gitlab:pycqa/flake8

### Issues and Pull Requests

Issues and pull requests are specified with `#{num}` and `!{num}` respectively. To specify an issue for a non-default repository under the default user, prefix the repository: `{repo}#{num}`. And to specify a repository under a non-default user, prefix both the user and repository: `{user}/{repo}#{num}`. And to reference an external provider, use the format `{provider}:{user}/{repo}#{num}`. If the default provider is a social media provider, then only the latter syntax can be used.

!!! example "Issue Example"

    ```
    Issue #1

    Issue backrefs#1

    Issue Python-Markdown/markdown#1

    Issue gitlab:pycqa/flake8#385

    Pull request !13

    Pull request backrefs!4

    Pull request Python-Markdown/markdown!598

    Pull request gitlab:pycqa/flake8!213
    ```

    Issue #1

    Issue backrefs#1

    Issue Python-Markdown/markdown#1

    Issue gitlab:pycqa/flake8#385

    Pull request !13

    Pull request backrefs!4

    Pull request Python-Markdown/markdown!598

    Pull request gitlab:pycqa/flake8!213

!!! note "Note"
    GitHub actually gives pull requests and issues unique values while GitLab and Bitbucket can have pulls with the same ID as an issue. So with GitHub, you can use `#{num}` format for both issues and pulls, and GitHub will redirect you to the appropriate issue or pull.

    GitLab and Bitbucket **must** specify pulls different from issues, hence the `!13` format. Though GitHub doesn't *need* to use the pull format, you can if you like. This format was actually borrowed from GitLab.

### Commits

Commit shorthand syntax is simply the 40 character commit hash value: `{hash}`. And much like issues and pull requests, you can denote a repository under the default user with `{repo}@{hash}` and a repository under a non-default user with `{user}/{repo}@{hash}`. Lastly, to reference an external provider, use the format `{provider}:{user}/{repo}@{hash}`. If the default provider is a social media provider, then only the latter syntax can be used.

!!! example "Commit Example"

    ```
    181c06d1f11fa29961b334e90606ed1f1ec7a7cc

    backrefs@cb4ecc5e7d8f7cdff0bb4482174f2ff0dcc35c61

    Python-Markdown/markdown@de5c696f94e8dde242c29d4be50b7bbf3c17fedb

    gitlab:pycqa/flake8@8acf55e0f85233c51c291816d73d828cc62d30d1
    ```

    181c06d1f11fa29961b334e90606ed1f1ec7a7cc

    backrefs@cb4ecc5e7d8f7cdff0bb4482174f2ff0dcc35c61

    Python-Markdown/markdown@de5c696f94e8dde242c29d4be50b7bbf3c17fedb

    gitlab:pycqa/flake8@8acf55e0f85233c51c291816d73d828cc62d30d1

### Diff/Compare

GitLab offers a useful shorthand to specify links to compare differences between two commits. This has been adopted for all the supported repository providers.

Specifying a compare link is very similar to specifying a commit link except you must specify the older hash and the newer hash separated by `...`: `{hash1}...{hash2}`. To specify a compare for a non-default repository under the default user, prefix the repository: `{repo}@{hash1}...{hash2}`. And to specify a compare under a non-default user, prefix both the user and repository: `{user}/{repo}@{hash1}...{hash2}`. Lastly, to reference an external provider, use the format `{provider}:{user}/{repo}@{hash1}...{hash2}`.

!!! example "Compare Example"

    ```
    e2ed7e0b3973f3f9eb7a26b8ef7ae514eebfe0d2...90b6fb8711e75732f987982cc024e9bb0111beac

    backrefs@88c6238a1c2cf71a96eb9abb4b0213f79d6ca81f...cb4ecc5e7d8f7cdff0bb4482174f2ff0dcc35c61

    Python-Markdown/markdown@007bd2aa4c184b28f710d041a0abe78bffc0ec2e...de5c696f94e8dde242c29d4be50b7bbf3c17fedb

    gitlab:pycqa/flake8@1ecf97005a024391fb07ad8941f4d25c4e0aae6e...9bea7576ac33a8e4f72f87ffa81dfa10256fca6e
    ```

    e2ed7e0b3973f3f9eb7a26b8ef7ae514eebfe0d2...90b6fb8711e75732f987982cc024e9bb0111beac

    backrefs@88c6238a1c2cf71a96eb9abb4b0213f79d6ca81f...cb4ecc5e7d8f7cdff0bb4482174f2ff0dcc35c61

    Python-Markdown/markdown@007bd2aa4c184b28f710d041a0abe78bffc0ec2e...de5c696f94e8dde242c29d4be50b7bbf3c17fedb

    gitlab:pycqa/flake8@1ecf97005a024391fb07ad8941f4d25c4e0aae6e...9bea7576ac33a8e4f72f87ffa81dfa10256fca6e

## Repository Link Shortener

MagicLink can also recognize issue, pull request, commit, and compare links, and render them in the same output format as the [repository shortcut links](#shorthand-links) feature. Unfortunately, mention link shortening is not presently supported due to the fact that MagicLink does not use any of the providers' API to verify user links, and some legitimate links can look like user links, but are not.

If we specify long form URLs from external providers, they will be shortened appropriately.


!!! example "External Provider Example"

    ```
    - https://gitlab.com/pycqa/flake8/issues/385
    - https://bitbucket.org/mrabarnett/mrab-regex/issues/260/extremely-slow-matching-using-ignorecase
    ```

    - https://gitlab.com/pycqa/flake8/issues/385
    - https://bitbucket.org/mrabarnett/mrab-regex/issues/260/extremely-slow-matching-using-ignorecase


When specifying links that reference the configured `provider`, `user`, and `repo`, links will be shortened differently in light of that context.

!!! example "Internal Provider Example"

    ```
    - https://github.com/facelessuser/pymdown-extensions/issues/1
    - https://github.com/facelessuser/pymdown-extensions/pull/13
    - https://github.com/facelessuser/pymdown-extensions/commit/3f6b07a8eeaa9d606115758d90f55fec565d4e2a
    - https://github.com/facelessuser/pymdown-extensions/compare/e2ed7e0b3973f3f9eb7a26b8ef7ae514eebfe0d2...90b6fb8711e75732f987982cc024e9bb0111beac
    - https://github.com/facelessuser/Rummage/commit/181c06d1f11fa29961b334e90606ed1f1ec7a7cc
    ```

    - https://github.com/facelessuser/pymdown-extensions/issues/1
    - https://github.com/facelessuser/pymdown-extensions/pull/13
    - https://github.com/facelessuser/pymdown-extensions/commit/3f6b07a8eeaa9d606115758d90f55fec565d4e2a
    - https://github.com/facelessuser/pymdown-extensions/compare/e2ed7e0b3973f3f9eb7a26b8ef7ae514eebfe0d2...90b6fb8711e75732f987982cc024e9bb0111beac
    - https://github.com/facelessuser/Rummage/commit/181c06d1f11fa29961b334e90606ed1f1ec7a7cc

## CSS

For normal links, no classes are added to the anchor tags. For repository links, `magiclink` will be added as a class. Also, an additional class will be added for each repository link type and provider.

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

## Options

Option                          | Type   | Default         | Description
------------------------------- | ------ | --------------- | -----------
`hide_protocol`                 | bool   | `#!py3 False`    | If `True`, links are displayed without the initial `ftp://`, `http://`, `https://`, or `ftps://`.
`repo_url_shortener`            | bool   | `#!py3 False`    | If `True`, GitHub, Bitbucket, and GitLab commit, pull, and issue links are are rendered in a shorthand syntax.
`repo_url_shorthand`            | bool   | `#!py3 False`    | If `True`, you can directly use a shorthand syntax to represent commit, pull, issue, and mention links for repository providers and they will be auto-linked.
`social_url_shorthand`          | bool   | `#!py3 False`    | If `True`, you can directly use a shorthand syntax to represent mention links for social media providers and they will be auto-linked.
`provider`                      | string | `#!py3 'github'` | The provider to use for repository shorthand syntax and shortener.
`user`                          | string | `#!py3 ''`       | The default user name to use for the specified provider.
`repo`                          | string | `#!py3 ''`       | The default repository name to use for the specified user and provider.
`labels`                        | dict   | `#!py3 {}`       | A dictionary for overriding repository link title text. See [labels](#labels) for more info.

!!! warning "Deprecation 4.2.0"
    In 4.2.0, `base_repo_url` has been deprecated in favor of `provider`, `user`, and `repo`. If `repo_url_shorthand` is enabled, `base_repo_url` will be ignored and `provider`, `user`, and `repo` will be used.

    `base_repo_url` will be removed sometime in the future.  Please migrate to using `provider`, `user`, and `repo`.

### Labels

By default, MagicLink provides titles for the repository links in the form `{provider} {label}: {info}`. You can specify different values for `{label}` by configuring the `labels` option.

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

You only need to provide the options you wish to override. Assume we wanted to adopt the GitLab terminology for pull requests, we could simply set `labels` to:

```js
    {
        'pull': 'Merge Request'
    }
```

--8<-- "refs.md"
