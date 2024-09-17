[:octicons-file-code-24:][_fancylists]{: .source-link }

# FancyLists

## Overview

FancyLists is inspired by [Pandoc's lists][pandoc-lists] list handling. FancyLists extends the list handling formats
to support parenthesis style lists along with additional ordered formats.

-   Support ordered lists as either a trailing dot or single right-parenthesis: `1.` or `1)`.
-   Support ordered lists with roman numeral formats, both lowercase and uppercase. Uppercase is treated as a different
    list type than lowercase.
-   Support ordered lists with alphabetical format, both lowercase and uppercase. Uppercase is treated as a different
    list type than lowercase.
-   Support a generic numerical format via `#.`. Requires [SaneHeaders](./saneheaders.md) to be enabled.
-   Using a different list type will start a new list. Trailing dot vs parenthesis are treated as separate types.
-   Ordered lists are sensitive to the starting value and will start a new list using the specified value.

Additional ordered list formats such as Roman numeral, alphabetical, and generic are optional and can be disabled via
[options](#options).

/// note
We do not support Pandoc's list notation that includes full parentheses (`(marker)`).
///

```py3
import markdown
md = markdown.Markdown(
    extensions=['pymdownx.fancylists']
)

# Add generic ordered styles
md = markdown.Markdown(extensions=['pymdownx.fancylists', 'pymdownx.saneheaders'])
```

## Rules

1.  Lists generally expect to be separated from paragraphs with an empty new line.
2.  A new list will be created if the list type changes. This occurs with:
    a.  A switch from unordered to ordered.
    b.  Change from using trailing dot or single right-parenthesis.
    c.  A change from using uppercase vs lowercase.
    d.  A change in ordered type: numerical, roman numeral, alphabetical, or generic.
3.  If using uppercase list markers, a list marker consisting of a single uppercase letter will require two spaces
    after the marker instead of the usual 1.
4.  The generic ordered list format (`#`) requires [SaneHeaders](./saneheaders.md) to be enabled.
5.  Roman numeral ordered lists require valid roman numerals.
6.  If a roman numeral consisting of a single letter is used within an alphabetical list (assuming trailing symbol and
   case are the same) the list item will be treated as an alphabetical list item.
7.  If a Roman numeral is used to start a list and it consists of a single letter, it will be assumed an alphabetical
    list unless the letter is `i` or `I`.


/// note
Ordered lists will have the type attribute set appropriately on the `ol` tag, but CSS styling can override appearance.
If it is noted that lists are not rendered correctly, make sure you do not have CSS overriding the style.
///

## Examples

Various list types.


```
1.  Item 1
2.  Item 2
    i.  Item 1
    ii. Item 2
        a.  Item 1
        b.  Item 2
            #.  Item 1
            #.  Item 2
```

///// html | div.result
1.  Item 1
2.  Item 2
    i.  Item 1
    ii. Item 2
        a.  Item 1
        b.  Item 2
            #.  Item 1
            #.  Item 2
/////

New lists on type change.

```
1.  Item 1
2.  Item 2

3)  Item 1
4)  Item 2
```

///// html | div.result
1.  Item 1
2.  Item 2

3)  Item 1
4)  Item 2
/////

New list on case change.

```
a.  Item 1
b.  Item 2

C.  Item 1
D.  Item 2
```

///// html | div.result
a.  Item 1
b.  Item 2

C.  Item 1
D.  Item 2
/////

Generic ordered list format.

```
#.  Item 1
#.  Item 2
```

///// html | div.result
#.  Item 1
#.  Item 2
/////

## Options

Option                      | Type     | Default                               | Description
--------------------------- | -------- | ------------------------------------- | ------------
`additional_ordered_styles` | [string] | `#!py3 ['roman', 'alpha', 'generic']` | Add additional ordered list styles. Accepted inputs include `roman`, `alpha`, and `generic`.
