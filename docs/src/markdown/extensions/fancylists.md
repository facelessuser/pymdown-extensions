[:octicons-file-code-24:][_fancylists]{: .source-link }

# FancyLists

## Overview

FancyLists is inspired by [Pandoc's lists][pandoc-lists] list handling. FancyLists extends the list handling formats
to support parenthesis style lists along with additional ordered formats. Various ordered formats are controlled by
setting the `type` attribute to the appropriate value on the `#!html <ol>` element.

```
1.  Item 1
2.  Item 2
    i.  Item 1
    ii. Item 2
        a.  Item a
        b.  Item b
            #.  Item 1
            #.  Item 2
```

///// html | div.result
1.  Item 1
2.  Item 2
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
# SaneHeaders required for generic ordered styles `#.` and `#)`
md = markdown.Markdown(extensions=['pymdownx.fancylists', 'pymdownx.saneheaders'])
```

## Syntax

Ordered lists have a number rules to determine when a list item is recognized and when a new list is created vs an item
appended to the previous list.

### Ordered List Rules

1.  A new list will be created if the list type changes. This occurs with:
    a.  A switch between unordered and ordered.

        ```
        -   Item 1
        -   Item 2
        1.  Item 1
        2.  Item 2
        ```

        ///// html | div.result
        -   Item 1
        -   Item 2
        1.  Item 1
        2.  Item 2
        /////

    b.  Change from using trailing dot or single right-parenthesis.

        ```
        1.  Item 1
        1.  Item 2
        1)  Item 1
        2)  Item 2
        ```

        ///// html | div.result
        1.  Item 1
        2.  Item 2
        1)  Item 1
        2)  Item 2
        /////

    c.  A change between using uppercase and lowercase.
        ```
        a.  Item a
        b.  Item a
        A.  Item A
        B.  Item B
        ```

        ///// html | div.result
        a.  Item a
        b.  Item b
        A.  Item A
        B.  Item B
        /////

    d.  A change in ordered type: numerical, roman numeral, alphabetical, or generic.

        ```
        #.  Item 1
        #.  Item 2
        a.  Item a
        b.  Item b
        1.  Item 1
        2.  Item 2
        ```

        ///// html | div.result
        #.  Item 1
        #.  Item 2
        a.  Item a
        b.  Item b
        1.  Item 1
        2.  Item 2
        /////

2.  If using uppercase list markers, a list marker consisting of a single uppercase letter followed by a dot will
    require two spaces after the marker instead of the usual 1 to avoid false positive matches with names that start
    with an initial.

    ```
    B. Russell was an English philosopher.

    A.  This is a list.
    ```

    ///// html | div.result
    B. Russell was an English philosopher.

    A.  This is a list.
    /////

4.  If a roman numeral consisting of a single letter is used within an alphabetical list (assuming no indication of a
    list type change) the list item will be treated as an alphabetical list item.

    ```
    iii. Item 3
    iv.  Item 4
    v.   Item 5

    ---

    v. Item v
    w. Item w
    x. Item x
    ```

    ///// html | div.result
    iii. Item 3
    iv.  Item 4
    v.   Item 5

    ---

    v. Item v
    w. Item w
    x. Item x
    /////

5.  If a single letter is used to start a list, it is assumed to be an alphabetical list unless the first letter is `i`
    or `I`.

    ```
    h. Item h
    i.  Item i
    j.   Item j

    ---

    i.   Item 1
    ii.  Item 2
    iii. Item 3
    ```

    ///// html | div.result
    h. Item h
    i.  Item i
    j.   Item j

    ---

    i.   Item 1
    ii.  Item 2
    iii. Item 3
    /////

### Roman Numeral Rules

Roman numerals have 7 symbols

Numeral | Decimal
------- | -------
I       | 1
V       | 5
X       | 10
L       | 50
C       | 100
D       | 500
M       | 1000

There are 3 rules for combining the Roman numerals.

1. Numerals must be arranged in descending order of size.
2. **M**, **C**, and **X** cannot be equaled or exceeded by smaller denominations.
3. **D**, **L**, and **V** can each only appear once.

Additionally, there are subtractive rules where a smaller denomination can precede a larger value and will be
subtracted from the larger value.

1. Only one **I**, **X**, and **C** can be used as the leading numeral in part of a subtractive pair.
2. **I** can only be placed before **V** and **X**.
3. **X** can only be placed before **L** and **C**.
4. **C** can only be placed before **D** and **M**.

If following the strictest rules you may find on the internet, you will often find an additional rule that limits the
consecutive use of a symbol to three. This was more of a common convention than it was a rule as sometimes presented in
modern times. Such a rule would mean that **III** is valid and **IIII** is invalid. We do not apply this rule as
historically, this wasn't even always followed. As examples, Roman clocks often used **IIII** instead of **IV**, and
the church of Sant'Agnese fuori le Mura, found in Rome, has a tomb inscription dated the year 1606 as **MCCCCCCVI**
instead of the more expected **MDCVI**.

The Roman numeral system evolved over time and was often not as strict as many may insist in modern times. There are
even cases beyond what is described here that deviate with more loose subtractive approaches and other non-standard
conventions. Some may disagree about what is the "most correct", rules, but if we believe the adage, "when in Rome do as
the Romans do," and we look at historical evidence of how Romans wrote their numerals, we clearly have more freedom than
some may like to admit.

We adhere to the rules as stated in this documentation. This slightly more flexible rule set allows us to more easily
resolve issues such as where **V** could be confused as an alphabetical list if it starts a list block where **IIIII**
would not.

```
i. item 1
ii. item 2
iii. item 3
iv. item 4
v. item 5

v) alphabetical list!
w) Another item.

iiiii. Start a new Roman numeral list.
vi. Another item.
```

/// html | div.result
i. item 1
ii. item 2
iii. item 3
iv. item 4
v. item 5

v) alphabetical list!
w) Another item.

iiiii. Start a new Roman numeral list.
vi. Another item.
///

## Options

Option                      | Type     | Default                               | Description
--------------------------- | -------- | ------------------------------------- | ------------
`additional_ordered_styles` | [string] | `#!py3 ['roman', 'alpha', 'generic']` | A list of additional ordered list styles. Accepted inputs: `roman`, `alpha`, and `generic`.
