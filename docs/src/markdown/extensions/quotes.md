---
icon: lucide/quote
---
[:octicons-file-code-24:][_quotes]{: .source-link }

# Quotes

## Overview

Quotes is an extension that offers a more modern take on blockquotes compared to the one that ships with Python Markdown
by default.

Python Markdown is an old-school parser that aims to follow the original Markdown specification. When implementing
blockquotes, it follows the guidance that describes the ability to lazily specify content under a blockquote as shown
below. Notice that two blocks of text can be specified without having to specify `>` on the empty lines between the
blocks.

```text title="Lazy Blockquote Handling"
> This is a paragraph

> This is another paragraph.
```

/// html | div.result
```md-render
> This is a paragraph

> This is another paragraph.
```
///

The problem with this approach is that if you have a need to have two separate blockquotes, this because difficult.

The Quotes extensions follows logic that is seen in more modern approaches to Markdown.

```text title="Separate Blockquotes"
> This is a paragraph

> This is another paragraph.
```

/// html | div.result
> This is a paragraph

> This is another paragraph.
///

It should be noted that since this extension does not use lazy formatting, you should be stricter with your leading
blockquote `>`. For instance, when using [SuperFences](./superfences.md), you will find that these must be fully
contained in the blockquotes. In the past, the lazy handling would have allowed for 

````text title="Blockquotes and SuperFences"
> ```
> Test
>
> Test
> ```

This will not.

> ```
> Test

> Test
> ```
````

/// html | div.result
This will work.

> ```
> Test
>
> Test
> ```

This will not.

> ```
> Test

> Test
> ```
///

## Callouts

GitHub and [Obsidian](https://obsidian.md/) allow for specifying special alerts/admonitions via a blockquote syntax
called callouts. The Quotes extensions allows you to opt-in to specifying such alerts that mimics Obsidian's approach,
which is GitHub compatible. Quotes will take the special blockquote syntax and output HTML that matches the output
of [Admonitions][admonition] or [Details](./details.md).

To specify normal callouts, simply ensure the that the first line of a blockquote contains the a class name in within
`[!...]`.

```text title="Callout"
> [!note]
> Here is a note
```

/// html | div.result
> [!note]
> Here is a note
///

If you'd like a custom title, simply provide one after the callout class specifier.

```text title="Callout with Custom Title"
> [!tip] Here's a tip
> Use a custom title!
```

/// html | div.result
> [!tip] Here's a tip
> Use a custom title!
///

To make a collapsible callout, just add `+` (open) or `-` (closed) immediately after the class specifier.

```text title="Collapsible Callout"
> [!danger]- Click to see more
> I'm collapsible.
```

/// html | div.result
> [!danger]- Click to see more
> I'm collapsible.
///

## Options

Option               | Type    | Default      | Description
-------------------- | ------- | ------------ |------------
`callouts`           | bool    | `#!py3 False`| Enable the ability to create special callouts using blockquotes.
