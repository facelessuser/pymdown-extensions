## Overview

MagicLink scans for URLs and emails and generates proper HTML links for them.  No special syntax is required, you just type or paste the links and they get converted.  MagicLink auto-links HTML, FTP, and email links.

If you happen to have some conflicts with syntax for a specific case, you can always revert to the old auto-link format as well: `<https://www.link.com>`.  Additional MagicLink features should work with this form as well.

If you don't like seeing `http://` before all your links and want them stripped out, enable `hide_protocol`.

For even more magic, enable `repo_url_shortener` for shorter concise links for popular source code hosts.  Issue links and commit links will be shortened in the style of GFM. Issues are shortened to `user/repo#1` for repositories external to `base_repo_url` and `#1` for internal links.  For commit links, external commits will show as `` user/repo@`abc1234` `` and internal commits will show as `` `abc1234` ``. Currently supports GitHub, GitLab, and Bitbucket.

## Options

Option                      | Type   | Default      | Description
--------------------------- | ------ | ------------ | -----------
`hide_protocol`             | bool   | `#!py False` | If `True`, links are displayed without the initial `ftp://`, `http://` or `https://`.
`repo_url_shortener`        | bool   | `#!py False` | If `True` GitHub, Bitbucket, and GitLab commit and issue links are shortened.
`base_repo_url`             | string | `#!py ''`    | The base repository URL for repository links.

## Examples

```
Links require no special syntax.

- Just paste links directly in the document like this: https://github.com/facelessuser/pymdown-extensions.
- Or even an email address: fake.email@email.com.

These examples assume the `base_repo_url` of `https://github.com/facelessuser/pymdown-extensions`.

- Process GitHub issue for this project: https://github.com/facelessuser/pymdown-extensions/issues/49.
- Process GitHub commit for this project: https://github.com/facelessuser/pymdown-extensions/commit/6a09fde5c1cad66c660c3aa7792385c52c49e819.
- Process GitHub issue for external project: https://github.com/fake-user/fake-repository/issues/538.
- Process GitHub commit for external project: https://github.com/fake-user/fake-repository/commit/594b25d53798c30735da5a9be19c06cc94052a16.
```

Links require no special syntax.

- Just paste links directly in the document like this: https://github.com/facelessuser/pymdown-extensions.
- Or even an email address: fake.email@email.com.

These examples assume the `base_repo_url` of `https://github.com/facelessuser/pymdown-extensions`.

- Process GitHub issue for this project: https://github.com/facelessuser/pymdown-extensions/issues/49.
- Process GitHub commit for this project: https://github.com/facelessuser/pymdown-extensions/commit/6a09fde5c1cad66c660c3aa7792385c52c49e819.
- Process GitHub issue for external project: https://github.com/fake-user/fake-repository/issues/538.
- Process GitHub commit for external project: https://github.com/fake-user/fake-repository/commit/594b25d53798c30735da5a9be19c06cc94052a16.

--8<-- "refs.md"
