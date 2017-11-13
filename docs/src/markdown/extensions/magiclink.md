# MagicLink

## Overview

MagicLink is an extension that provides a number of useful link related features. MagicLink can auto-link HTML, FTP, and email links. It can auto-convert repository links (GitHub, GitLab, and Bitbucket) and display them in a more concise, shorthand format. MagicLink can also be configured to directly auto-link the aforementioned shorthand format.

If you happen to have some conflicts with syntax for a specific case, you can always revert to the old auto-link format as well: `#!md <https://www.link.com>`. If enabled, repository link shortening will be applied to the the angle bracketed auto-link format as well.

## Auto-Linking

MagicLink supports auto-linking HTTP, FTP and email links. You can specify these links in raw text and they should get auto-linked. There are some limitations placed on MagicLink to keep it from aggressively auto-linking text that is not part of links. If you have a link that cannot be detected, you can always use the old style angle bracketed link format: `#!md <https://www.link.com>`.

To use, just paste raw links in your Markdown:

```md
- Just paste links directly in the document like this: https://google.com.
- Or even an email address: fake.email@email.com.
```

They will be auto-linked like this:

- Just paste links directly in the document like this: https://google.com.
- Or even an email address: fake.email@email.com.

## Repository Shorthand Links

MagicLink supports a shorthand syntax for quickly referencing repository issues, pull requests, commits, and even mentioning other users. The syntax is very *similar* to GitHub's, but borrows syntax from GitLab to bridge the differences between the three providers.

To use this feature you must configure MagicLink for your desired provider and specify the default user and repository via the `provider`, `user`, and `repo` [options](#options).  You must also set `repo_url_shorthand` to `True`.

All shorthand links will be relative to your `provider`, and they do not currently work cross provider. So if your `provider` is set to `github`, all mentions will be generated for GitHub.  If a user name or repository is not specified, the link will use the values found in `user` and `repo` from the extension's [options](#options).

Mentions of other users are performed with the following syntax: `@{user}`.

Issues and pull requests are specified with `#{num}` and `!{num}` respectively. To specify an issue for a non-default repository under the default user, prefix the repository: `{repo}#{num}`. And to specify a repository under a non-default user, prefix both the user and repository: `{user}/{repo}#{num}`.

Commit shorthand syntax is simply the 40 character commit hash value: `{hash}`. And much like issues and pull requests, you can denote a repository under the default user with `{repo}@{hash}` and a repository under a non-default user with `{user}/{repo}@{hash}`.

For reference, the examples below assume the default provider, user, and repository as `github`, `facelessuer`, and `pymdown-extensions` respectively.

Shorthand                                            | Output
---------------------------------------------------- | -----------
`@user`                                              | @user                                              |Mention another user under your `provider`.
`#1`                                                 | #1                                                 |Issue for the default `user` and `repo`.
`repo#1`                                             | repo#1                                             |Issue for a specific project under the default `user`.
`user/repo#1`                                        | user/repo#1                                        |Issue for a specific user and repository.
`!2`                                                 | !2                                                 |Pull request for the default `user` and `repo`.
`repo!2`                                             | repo!2                                             |Pull request for a specific project under the default `user`.
`user/repo!2`                                        | user/repo!2                                        |Pull request for a specific user and repository.
`181c06d1f11fa29961b334e90606ed1f1ec7a7cc`           | 181c06d1f11fa29961b334e90606ed1f1ec7a7cc           |Commit for the default `user` and `repo`.
`repo@181c06d1f11fa29961b334e90606ed1f1ec7a7cc`      | repo@181c06d1f11fa29961b334e90606ed1f1ec7a7cc      |Commit for a specific project under the default `user`.
`user/repo@181c06d1f11fa29961b334e90606ed1f1ec7a7cc` | user/repo@181c06d1f11fa29961b334e90606ed1f1ec7a7cc |Commit for a specific user and repository.

!!! warning
    Links are not be verified, so make sure you are specifying valid issues, repositories, and users as they will be auto-linked even if they are not valid.

!!! note "Note"
    GitHub actually gives pull requests and issues unique values while GitLab and Bitbucket can have pulls with the same ID as an issue. So with GitHub, you can use `#{num}` format for both issues and pulls, and GitHub will redirect you to the appropriate issue or pull.

    GitLab and Bitbucket **must** specify pulls different from issues, hence the `!13` format. Though GitHub doesn't *need* to use the pull format, you can if you like. This format was actually borrowed from GitLab.

## Repository Link Shortener

MagicLink can also recognize issue, pull request, and commit links, and render them in the same output format as the [repository-shortcut-links] feature. Unfortunately, mention link shortening is not presently supported due to the fact that MagicLink does not use any of the providers' API to verify user links, and some legitimate links can look like user links, but are not.

Link shortening is a little different from the link shorthand feature as it can handle all three providers regardless of what the `provider` is set as the information can be directly determined from the links.

If we specify long form URLs from external providers, they will be shortened appropriately.

```md
- https://gitlab.com/pycqa/flake8/issues/385
- https://bitbucket.org/mrabarnett/mrab-regex/issues/260/extremely-slow-matching-using-ignorecase
```

- https://gitlab.com/pycqa/flake8/issues/385
- https://bitbucket.org/mrabarnett/mrab-regex/issues/260/extremely-slow-matching-using-ignorecase


When specifying links that reference the configured `provider` and `user`, links will be shortened differently in light of that context.

```md
- https://github.com/facelessuser/pymdown-extensions/issues/1
- https://github.com/facelessuser/pymdown-extensions/pull/13
- https://github.com/facelessuser/pymdown-extensions/commit/3f6b07a8eeaa9d606115758d90f55fec565d4e2a
- https://github.com/facelessuser/Rummage/commit/181c06d1f11fa29961b334e90606ed1f1ec7a7cc
```

- https://github.com/facelessuser/pymdown-extensions/issues/1
- https://github.com/facelessuser/pymdown-extensions/pull/13
- https://github.com/facelessuser/pymdown-extensions/commit/3f6b07a8eeaa9d606115758d90f55fec565d4e2a
- https://github.com/facelessuser/Rummage/commit/181c06d1f11fa29961b334e90606ed1f1ec7a7cc

## Options

Option                          | Type   | Default         | Description
------------------------------- | ------ | --------------- | -----------
`hide_protocol`                 | bool   | `#!py False`    | If `True`, links are displayed without the initial `ftp://`, `http://`, `https://`, or `ftps://`.
`repo_url_shortener`            | bool   | `#!py False`    | If `True`, GitHub, Bitbucket, and GitLab commit, pull, and issue links are are rendered in a shorthand syntax.
`repo_url_shorthand`            | bool   | `#!py False`    | If `True`, you can directly use a shorthand syntax to represent commit, pull, issue, and mention links and they will be auto-linked.
`provider`                      | string | `#!py 'github'` | The provider to use for repository shorthand syntax and shortener.
`user`                          | string | `#!py ''`       | The default user name to use for the specified provider.
`repo`                          | string | `#!py ''`       | The default repository name to use for the specified user and provider.
~~`base_repo_url`~~             | string | `#!py ''`       | The base repository URL for repository links.

!!! warning "Deprecation 4.2.0"
    in 4.2.0 `base_repo_url` has been deprecated in favor of `provider`, `user`, and `repo`. If `repo_url_shorthand` is enabled, `base_repo_url` will be ignored and `provider`, `user`, and `repo` will be used.

    `base_repo_url` will be removed sometime in the future.  Please migrate to using `provider`, `user`, and `repo`.

## CSS

For normal links, no classes are added to the anchor tags. For repository links `magiclink` will be added as a class.  And an additional class will be added for each repository link type.

Link\ Type | Class
---------- | -----
Mentions   | `magiclink magiclink-mention`
Issues     | `magiclink magiclink-issue`
Pulls      | `magiclink magiclink-pull`
Commits    | `magiclink magiclink-commit`

--8<-- "refs.md"
