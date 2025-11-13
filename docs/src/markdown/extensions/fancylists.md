---
icon: lucide/list
---
[:octicons-file-code-24:][_fancylists]{: .source-link }

# FancyLists

## Overview

FancyLists is inspired by [Pandoc's list handling][pandoc-lists]. FancyLists extends the list handling formats to
support parenthesis style lists along with additional ordered formats.

```
1)  Item 1
2)  Item 2
    i.  Item 1
    ii. Item 2
        a.  Item a
        b.  Item b
            #.  Item 1
            #.  Item 2
```

///// html | div.result
1)  Item 1
2)  Item 2
    i.  Item 1
    ii. Item 2
        a.  Item a
        b.  Item b
            #.  Item 1
            #.  Item 2
/////

FancyLists adds the following features:

-   Support ordered lists with either a trailing dot or single right-parenthesis: `1.` or `1)`.
-   Support ordered lists with roman numeral formats, both lowercase and uppercase. Uppercase is treated as a different
    list type than lowercase.
-   Support ordered lists with alphabetical format, both lowercase and uppercase. Uppercase is treated as a different
    list type than lowercase.
-   Support a generic ordered list marker via `#.` or `#)`. These can be used in place of numerals and will inherit the
    type of the current list as long as they use the same convention (`.` or `)`). If used to start a list, decimal
    format will be assumed. Requires [SaneHeaders](./saneheaders.md) to be enabled.
-   Using a different list type will start a new list. Trailing dot vs parenthesis are treated as separate types.
-   Ordered lists are sensitive to the starting value and can restart a list or create a new list using the first value
    in the list.

Additional ordered list types such as Roman numeral, alphabetical, and generic are optional and can be disabled via
[options](#options).

Ordered types are controlled by setting the `type` attribute to the appropriate value on the `#!html <ol>` element. If
you have CSS that overrides styling, you may not see the appropriate types, so if you want control at the Markdown
level, make sure CSS doesn't override the list styles or see the [styling](#styling) section for more info.

List\ Types             | HTML\ List\ Type
----------------------- | ----------------
Decimal                 | 1
Lowercase Alphabetical  | a
Uppercase Alphabetical  | A
Lowercase Roman Numeral | i
Uppercase Roman Numeral | I

/// note
We do not support Pandoc's list notation that includes full parentheses (`(marker)`).
///

```py3
import markdown
# SaneHeaders required for generic ordered styles `#.` and `#)`
md = markdown.Markdown(extensions=['pymdownx.fancylists', 'pymdownx.saneheaders'])
```

## Syntax

Ordered lists have a number rules to determine when a list item is recognized and when a new list is created/restarted
vs an item appended to the previous list.

### Ordered List Rules

1.  A new list will be created if the list type changes. This occurs with:
    a.  A switch between unordered and ordered.

        ```
        -   Item 1
        -   Item 2
        1.  Item 1
        2.  Item 2
        ```

        /// html | div.result
        -   Item 1
        -   Item 2
        1.  Item 1
        2.  Item 2
        ///

    b.  Change from using trailing dot or single right-parenthesis.

        ```
        1.  Item 1
        1.  Item 2
        1)  Item 1
        2)  Item 2
        ```

        /// html | div.result
        1.  Item 1
        2.  Item 2
        1)  Item 1
        2)  Item 2
        ///

    c.  A change between using uppercase and lowercase.
        ```
        a.  Item a
        b.  Item a
        A.  Item A
        B.  Item B
        ```

        /// html | div.result
        a.  Item a
        b.  Item b
        A.  Item A
        B.  Item B
        ///

    d.  A change in ordered type: numerical, roman numeral, alphabetical, or generic.

        ```
        #.  Item 1
        #.  Item 2
        a.  Item a
        b.  Item b
        1.  Item 1
        2.  Item 2
        ```

        /// html | div.result
        #.  Item 1
        #.  Item 2
        a.  Item a
        b.  Item b
        1.  Item 1
        2.  Item 2
        ///

2.  Generic list items inherit type from the current list and if starting a new list will assume the decimal type. List
    items following a generic list will not cause a new list as long as the list item is consistent with the current
    list type.

    ```
    i.  item i
    #.  item ii
    #.  item iii
    iv. item iv
    ```

    //// html | div.result
    i.  item i
    #.  item ii
    #.  item iii
    iv. item iv
    ////

3.  If using uppercase list markers, a list marker consisting of a single uppercase letter followed by a dot will
    require two spaces after the marker instead of the usual 1 to avoid false positive matches with names that start
    with an initial.

    ```
    B. Russell was an English philosopher.

    A.  This is a list.
    ```

    /// html | div.result
    B. Russell was an English philosopher.

    A.  This is a list.
    ///

4.  If a roman numeral consisting of a single letter is used within an alphabetical list (assuming no indication of a
    list type change) the list item will be treated as an alphabetical list item.  See [special cases](#special-cases)
    on how to navigate these edge cases.

    ```
    iii. Item 3
    iv.  Item 4
    v.   Item 5

    ---

    v. Item v
    w. Item w
    x. Item x
    ```

    /// html | div.result
    iii. Item 3
    iv.  Item 4
    v.   Item 5

    ---

    v. Item v
    w. Item w
    x. Item x
    ///

5.  If a single letter is used to start a list, it is assumed to be an alphabetical list unless the first letter is `i`
    or `I`.  See [special cases](#special-cases)
    on how to navigate these edge cases.

    ```
    h. Item h
    i.  Item i
    j.   Item j

    ---

    i.   Item 1
    ii.  Item 2
    iii. Item 3
    ```

    /// html | div.result
    h. Item h
    i.  Item i
    j.   Item j

    ---

    i.   Item 1
    ii.  Item 2
    iii. Item 3
    ///

### Roman Numeral Rules

The Roman numeral system consists of 7 numerals that are combined to make all the numbers in the system.

Numeral | Decimal
------- | -------
I       | 1
V       | 5
X       | 10
L       | 50
C       | 100
D       | 500
M       | 1000

These numbers, depending on how they are combined, are added and subtracted to make bigger numbers.

In modern day, many assume more strict rules, but looking at historical examples, the system was for less strict.
FancyLists airs on the side of being a little less strict to be more forgiving of user inputs, browsers will always
render them in a more strict form regardless of what the user inputs.

#### Rules of Addition

When Roman numerals are chained in descending order according to denomination, the values are just added together.
With that said, there are a few rules as to how the numerals are allowed to be sequenced.

1. Numerals must be arranged in descending order of size.
2. `D`, `L`, and `V` can each only appear once.
3. `M`, `C`, and `X` cannot be equaled or exceeded by smaller denominations.

It should be noted that while the user is encouraged to generally follow rule 3 as it is outlined, this is the only rule
that FancyLists does not explicitly enforce. FancyLists actually enforces the rule as shown below.

> `M`, `C`, and `X` cannot be exceeded by smaller denominations.

Generally, it is recommended to use higher denomination numerals when possible, like using `X` instead of `VIIIII`.
Despite this recommendation, we allow some flexibility in this area for user input. Additionally, this flexibility makes
it easier to handle certain [special cases](#special-cases) that we will be covered later. Regardless of how the user
inputs the numbers, browsers will use a more strict rendering.

#### Rules of Subtraction

When using only additive rules, many Roman numerals can get quite long. Subtractive rules allow for shortening additive
sequences with shorter subtractive sequences. In subtractive sequences, certain lesser denomination can actually be
placed before larger denominations, and when done, the lesser denomination is subtracted from the larger denomination.
As an example, with subtractive rules, `IIII` can be written more simply as `IV` which subtracts 1 from 5. The rules are
specified below.

1. Only one `I`, `X`, and `C` can be used as the leading numeral in part of a subtractive pair.
2. When `I`, `X`, and `C` are used as the lead in a subtractive pair, they can't be used immediately after the
   subtractive pair. So `IXI` is invalid.
2. `I` can only be placed before `V` and `X`.
3. `X` can only be placed before `L` and `C`.
4. `C` can only be placed before `D` and `M`.

### Special Cases

If you've been paying attention, you may have noticed that when alphabetical lists and Roman numeral lists are **both**
enabled, there arises some ambiguous cases. Currently if `I` occurs in the middle of an alphabetical list, it is assumed
to be an alphabetical list item, but if it starts a list, it is assumed to be a Roman numeral list item. The reverse is
true for `M`, `D`, `C`, `L`, `X`, and `V` where it is assumed that these are Roman numeral list items if they occur in
the middle of a Roman numeral list, but are assumed to be alphabetical list items if they start a list.

/// note
It should be noted that these issues exists in pretty much all implementations that support this way of including both
alphabetically ordered and Roman numeral ordered lists. This is not an issue specific to this implementation.
///

In the example below, we can see that using `v` in the middle of a Roman numeral list works just fine, but if we try
and restart/start a new list with `v`, we get an alphabetically ordered list.

```
iii. item 3
iv. item 4
v. item 5

---

v. v
w. w
```

/// html | div.result
iii. item 3
iv. item 4
v. item 5

---

v. item v
w. item w
///

As noted in ["additive rules"](#rules-of-addition), while we encourage users to generally not represent numerals such as
`X` with `VIIIII`, we do not enforce the restriction. The reason is for these specific edge cases. In these few
instances ignoring this rule can help bypass this conflict. If you need to start or restart a Roman numeral list value
consisting of a single numeral (that is not `I`), we can use the flexibility in the rules to mitigate the issue.
Regardless of our input, browsers will render these list items in the more common, strict format.

```
IIIII. Roman numeral V

---

VIIIII. Roman numeral X

---

XXXXX. Roman numeral L

---

LXXXXX. Roman numeral C

---

CCCCC. Roman numeral D

---

DCCCCC. Roman numeral M

```

/// html | div.result
IIIII. Roman numeral V

---

VIIIII. Roman numeral X

---

XXXXX. Roman numeral L

---

LXXXXX. Roman numeral C

---

CCCCC. Roman numeral D

---

DCCCCC. Roman numeral M
///

The reverse case, where alphabetical lists cannot start with `I` (or `i`), cannot be mitigated in the aforementioned
manner, but we can wrap it in a special [Block](./blocks/index.md) and specify the `start` and/or `type` manually. By
setting the `type` to `a`, we will force the creation of a lowercase alphabetic list and the first list item will be
included under it, parsing it under the assumption of a lowercase alphabetical list (if possible). If a `start` is
given, the actual value of the first list item will be ignored.

```
/// fancylists | type=a
i. item i
j. item j
///
```

//// html | div.result
/// fancylists | type=a
i. item i
j. item j
///
////

This can also be applied to generic lists by also adding `start` value to anchor the first value.

```
/// fancylists | type=a start=9
#. item i
#. item j
///
```

//// html | div.result
/// fancylists | type=a start=9
#. item i
#. item j
///
////

If a more "strictly correct" mitigation is desired for the earlier mentioned Roman numeral conflict cases, wrapping
the Roman numeral list will work as well. This allows for the use of more _proper_ Roman numerals.

```
/// fancylists | type=I
V.   item V
VI.  item VI
///
```

//// html | div.result
/// fancylists | type=I
V.   item V
VI.  item VI
///
////

## Styling

By default, browsers should style ordered list types without any issues, but if you are displaying your content in HTML
that already provides CSS for lists, you may have to override the CSS. This can sometimes be difficult, and if you want
to style each type appropriately, CSS is currently lacking as the case sensitive attribute flag is not implemented in
all browsers to properly target `type=a` vs `type=A`.

To make styling easier, if you are struggling with getting the types properly styled, you can enable the `inject_style`
[option](#options) to inject a style attribute on each `#!html <ol>` tag that sets the `list-style-type` to the
appropriate value.

If more advanced CSS styling is desired, and many browsers have not yet implemented the case-sensitive `s` flag for
attribute selectors, it can be very hard to target an uppercase vs lowercase ordered list. To mitigate this issue,
a class indicating the current list type can be injected into the `#!html <ol>` element.

CSS\ Classes             |
------------------------ |
`fancylists-decimal`     |
`fancylists-lower-alpha` |
`fancylists-upper-alpha` |
`fancylists-lower-roman` |
`fancylists-upper-roman` |

## Options

Option                      | Type     | Default                               | Description
--------------------------- | -------- | ------------------------------------- | ------------
`additional_ordered_styles` | [string] | `#!py3 ['roman', 'alpha', 'generic']` | A list of additional ordered list styles. Accepted inputs: `roman`, `alpha`, and `generic`.
`inject_style`              | bool     | `#!py3 False`                         | Inject styling into `ol` for list styling.
`inject_class`              | bool     | `#!py3 False`                         | Inject class into `ol` for list styling.
