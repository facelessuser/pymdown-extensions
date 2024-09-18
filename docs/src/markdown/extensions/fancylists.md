[:octicons-file-code-24:][_fancylists]{: .source-link }

# FancyLists

## Overview

FancyLists is inspired by [Pandoc's lists][pandoc-lists] list handling. FancyLists extends the list handling formats
to support parenthesis style lists along with additional ordered formats.

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

Ordered types are controlled by setting the `type` attribute to the appropriate value on the `#!html <ol>` element. If
you have CSS that overrides styling, you may not see the appropriate types, so if you want allow control at the Markdown
level, make sure CSS doesn't override the list styles.

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

2.  If using uppercase list markers, a list marker consisting of a single uppercase letter followed by a dot will
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

#### Rules of Addition

There are 3 rules for combining the Roman numerals. Using the following rules, the numerals are added together.

1. Numerals must be arranged in descending order of size.
2. **M**, **C**, and **X** cannot be equaled or exceeded by smaller denominations.
3. **D**, **L**, and **V** can each only appear once.

#### Rules of Subtraction

Additionally, there are subtractive rules where a smaller denomination can precede a larger one and will be
subtracted from the larger value.

1. Only one **I**, **X**, and **C** can be used as the leading numeral in part of a subtractive pair.
2. **I** can only be placed before **V** and **X**.
3. **X** can only be placed before **L** and **C**.
4. **C** can only be placed before **D** and **M**.

#### Rule of 3?

If following the strictest rules you may find on the internet, you will often find an additional rule that limits the
repetition of symbols to only 3. In short, if following this rule, **III** is valid and **IIII** is invalid. The problem
with this rule is that it developed more as a common convention than a hard rule. Roman clocks often used **IIII**
instead of **IV**, and the church of Saint Agnes Outside the Walls, found in Rome, has a tomb inscription dated with the
year 1606 as **MCCCCCCVI** instead of the more expected **MDCVI**. Both these cases clearly break this "rule of 3".

The Roman numeral system evolved over time and was often not as strict as many may insist in modern times. There are
even historical cases that break the first rule of subtraction that we follow. Some may disagree about what are the
"most correct" rules, but if we believe the adage, "when in Rome do as the Romans do," and we look at historical
evidence of how Romans wrote their numerals, we clearly have more freedom than some may like to admit.

In short, we do not follow the "rule of 3" as described above, but adhere only to the rules as previously stated. This
does end up coming in handy in a few [special cases](#special-cases).

### Special Cases

If you've been paying attention, you may have noticed that when alphabetical lists and Roman numeral lists are enabled,
there are two conflicts: alphabetical lists can never start with `I` and Romans numeral lists can never start with
single values of `M`, `D`, `C`, `L`, `X`, and `V`. This is true for both uppercase and lowercase. This does not affect
list items in the middle of a list.

/// note
It should be noted that these issues exists in pretty much all implementations that support this way of including both
alphabetically ordered and Roman numeral ordered lists. This is not an issue specific to this implementation.
///

In the example below, we can see that using `v` in the middle of a Roman numeral list works just fine, but if we try
and start a new list with `v`, we get an alphabetically ordered list.

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

Since we do not follow the ["rule of 3"](#rule-of-3) in Roman numerals, we can easily work around this edge case. This
can be applied to `M`, `D`, `C`, `L`, `X`, and `V`.

```
IIIII. Roman numeral V

---

VIIIII. Roman numeral X

---

XXXXX. Roman numeral L

---

XCVIIIII. Roman numeral C

---

CCCCC. Roman numeral D

---

CMXCVIIIII. Roman numeral M
```

/// html | div.result
IIIII. Roman numeral V

---

VIIIII. Roman numeral X

---

XXXXX. Roman numeral L

---

XCVIIIII. Roman numeral C

---

CCCCC. Roman numeral D

---

CMXCVIIIII. Roman numeral M
///

The last issue, where alphabetically ordered lists cannot start with `I`, is not so easy. This issue exists in pretty
much all implementations that support this way of including both alphabetically ordered and Roman numeral ordered lists.

Luckily, if you have the [HTML Block extension](./blocks/plugins/html.md) enabled, you can just wrap the list,
specifying the `start` and `type` manually, and it should work fine.

```
/// html | ol[start="9"][type="a"]
i. item i!
j. item j
///
```

//// html | div.result
/// html | ol[start="9"][type="a"]
i. item i
j. item j
///
////

This approach also works for Roman numeral edge cases if it is found to be more straight forward.

```
/// html | ol[start="5"][type="I"]
V.   item V
VI.  item VI
///
```

//// html | div.result
/// html | ol[start="5"][type="I"]
V.   item V
VI.  item VI
///
////

It may be assumed that the [`md_in_html` plugin][md-in-html] could be used, but due to how Python Markdown process block
tags in that extension, it doesn't quite work as expected.

## Options

Option                      | Type     | Default                               | Description
--------------------------- | -------- | ------------------------------------- | ------------
`additional_ordered_styles` | [string] | `#!py3 ['roman', 'alpha', 'generic']` | A list of additional ordered list styles. Accepted inputs: `roman`, `alpha`, and `generic`.
