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

[GitHub][github-alerts] and [Obsidian](https://help.obsidian.md/callouts) allow for specifying admonitions (also known
as alerts or callouts) by using a special syntax at the start of a blockquote. While Obsidian does this with a more
feature rich syntax, GitHub offers a more stripped down version.

The Quotes extensions allows you to opt-in approach to specifying admonitions in a similar approach that is compatible
with Obsidian and GitHub if usage is limited to what they offer.

Quotes will take the special blockquote syntax and output HTML that matches the output of [Admonitions][admonition] or
[Details](./details.md).

To specify normal callouts, simply ensure the that the first line of a blockquote contains a class name in within
`[!...]`.

```text title="Callout"
> [!note]
> Here is a note
```

/// html | div.result
> [!note]
> Here is a note
///

/// note
GitHub only supports the simple class notation, and only recognizes the classes: note, tip, important, warning, caution.

There are no restrictions as to which classes you can specify, but if cross compliance is desired, take note of what
GitHub supports. Learn more [here][github-alerts].
///

Borrowing from Obsidian, Quotes also enables a few more advanced features. If you'd like a custom title, simply provide
one on the same line as the class specifier. If one is not provided, a title is sourced from the first the class.

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

Lastly, if you need to specify more multiple classes, you can utilize the Obsidian approach and and separate each class
with `|`. The first class will be used as the main title if no title is provided, but all classes will be applied to the
callout.

```text title="Collapsible Callout"
> [!warning | inline | end]
> Make inline and set at the end.

A paragraph.
```

/// html | div.result
> [!warning | inline | end]
> Make inline and set at the end.

A paragraph.
///

## Options

Option               | Type    | Default      | Description
-------------------- | ------- | ------------ |------------
`callouts`           | bool    | `#!py3 False`| Enable the ability to create special callouts using blockquotes.
