## Overview

!!! warning "Deprecated Extension"
    This extension has been deprecated in version `1.3.0`.  Users are encouraged to use the [Emoji extension](./emoji.md) instead.  This extension will be removed in `3.0`.

GitHubEmoji adds support for GFM emojis.  Using GFM's emoji syntax, this extension will create image links to GitHub's emoji assets.  It adds support for all of GitHub's supported emojis (at the time of writing this).

## Options

Option      | Type   | Default        |Description
----------- | ------ | -------------- |-----------
`css_class` | string | `#!py 'emoji'` | Insert the given class name into the image tag.  To disable class name insertion, provide an empty string.
`offline`   | bool   | `#!py True`    | When enabled, GitHubEmoji will use the last generated emoji table from GitHub at the time of release.  If for some reason GitHub changes things and you **must** have the latest, you can set this to `False` and GitHubEmoji will request the latest table via the [GitHub API][github-api-emoji].  It does this with the [requests][requests] module, and it will only be in memory.  As requests is not a required module, if you do not have requests installed, this will default back to offline.

!!! note "Note"
    Since 'online' calls through the GitHub API are done anonymously, GitHub will limit the caller to approximately 60 calls in an hour.  There are no plans at this time to add [OAuth support][github-api-oauth].

--8<-- "refs.md"
