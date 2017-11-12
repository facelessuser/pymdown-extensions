# MagicLink

## Overview

MagicLink is an extension that provides a number of useful link related features. MagicLink can auto-link HTML, FTP, and email links. It can auto-convert repository links (from GitHub, GitLab, and Bitbucket) and display them in a more concise, shorthand format.  MagicLink can also be configured to directly auto-link the aforementioned shorthand format.

If you happen to have some conflicts with syntax for a specific case, you can always revert to the old auto-link format as well: `#!md <https://www.link.com>`. If enabled, repository link shortening will be applied to the the angle bracketed auto-link format as well.

## Auto-Linking

MagicLink supports auto-linking HTTP, FTP and email links. You can specify these links in raw text and they should get auto-linked. There are some limitations placed on MagicLink to keep it from aggressively auto-linking text that is not part of links.

Pasting raw URLs in a list

```md
- Just paste links directly in the document like this: https://google.com.
- Or even an email address: fake.email@email.com.
```

Will be auto-linked like this:

- Just paste links directly in the document like this: https://google.com.
- Or even an email address: fake.email@email.com.

## Repository Shorthand Links

MagicLink supports a shorthand syntax for quickly referencing repository issues, pulls, commits, and even users. The syntax is very similar to GitHub's, but since MagicLink can also be configured for GitLab and Bitbucket, it borrows a little syntax from GitLab to bridge the differences between these three providers. To enable this feature, you must set the `repo_url_shorthand` option to `True`.  It is important to note that no links are verified through the respective repository host's API.

All shorthand links will reference repositories relative to the configured `provider`. In all the examples it is assumed that MagicLink has been configured with `provider` as `github`, `user` as `facelessuser`, and `repo` as `pymdown-extensions`. Below is the supported shorthand reference syntax:

- Mentions: `@Python-Markdown @facelessuser` --> @Python-Markdown @facelessuser.
- Issues: `#1` --> #1.
- Pull/Merge requests: `!13` --> !13.
- Commit: `3f6b07a8eeaa9d606115758d90f55fec565d4e2a` --> 3f6b07a8eeaa9d606115758d90f55fec565d4e2a.

!!! note "Note"
    GitHub actually gives pull requests and issues unique values while GitLab and Bitbucket can have pulls with the same ID as an issue. So with GitHub, you can use `#1` format for both issues and pulls, and GitHub will redirect you to the appropriate issue or pull.

    GitLab and Bitbucket **must** specify pulls different from issues, hence the `!13` format. Though GitHub doesn't *need* to use the pull format, you can if you like. This format was actually borrowed from GitLab.

If we want to reference a different repository under the configured user `facelessuser` than what was originally configured under `repo`, we can prefix the links with the repository.

- Issues: `Rummage#133` --> Rummage#133.
- Pull/Merge requests: `Rummage!141` --> Rummage!141.
- Commit: `Rummage@181c06d1f11fa29961b334e90606ed1f1ec7a7cc` --> Rummage@3f6b07a8eeaa9d606115758d90f55fec565d4e2a.

To reference repositories external to the specified user (but under the same provider), you can prefix with the links with `user/repo`.

- Issues: `Python-Markdown/markdown#575` --> Python-Markdown/markdown#575.
- Pull/Merge requests: `Python-Markdown/markdown!593` --> Python-Markdown/markdown!593.
- Commit: `Python-Markdown/markdown@f018b0ede5a49c8d711351d8e9ff437c97cf3acc` --> Python-Markdown/markdown@f018b0ede5a49c8d711351d8e9ff437c97cf3acc.

## Repository Link Shortener

So previously we showed how you can specify a provider, and then reference links specific to that provider with a shorthand syntax, but you can also have MagicLink take long form repository issue, pull, and commit links and render them in the shorthand format. This actually will work for all three supported providers regardless of how `provider` is configured.

Unfortunately, mention link shortening is not presently supported due to the fact that MagicLink does not use any of the providers' API to verify user links, and some legitimate links can look like user links, but are not.

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
