[:octicons-file-code-24:][_tasklist]{: .source-link }

# Tasklist

## Overview

The Tasklist extension adds GFM style task lists.  They follow the same syntax as GFM. Simply start each list item with
a square bracket pair containing either a space (an unchecked item) or a `x` (a checked item).

/// note
All task lists in this documentation are generated with [`custom_checkbox`](#options) enabled.
///

```text title="Tasklist"
Task List

-   [X] item 1
    *   [X] item A
    *   [ ] item B
        more text
        +   [x] item a
        +   [ ] item b
        +   [x] item c
    *   [X] item C
-   [ ] item 2
-   [ ] item 3
```

/// html | div.result
Task List

-   [X] item 1
    *   [X] item A
    *   [ ] item B
        more text
        +   [x] item a
        +   [ ] item b
        +   [x] item c
    *   [X] item C
-   [ ] item 2
-   [ ] item 3
///

The Tasklist extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.tasklist'])
```

## Styling with CSS

The HTML structure of a task list is found below:

/// tab | Default
This is the default output.

```html
<ul class="task-list">
    <li class="task-list-item">
        <input type="checkbox" disabled="" checked="">
        item 1
    </li>
</ul>
```
///

/// tab | Custom
If `custom_checkbox` is enabled, the structure will be as follows:

```html
<ul class="task-list">
    <li class="task-list-item">
        <label class="task-list-control">
            <input type="checkbox" disabled checked="">
            <span class="task-list-indicator"></span>
        </label>
        item 1
    </li>
</ul>
```
///

/// tab | Clickable
If `clickable_checkbox` is enabled, user interaction will be allowed by removing the `disabled` attribute from the
`input` element. `clickable_checkbox` can be a applied to either the default or custom form.

```html
<ul class="task-list">
    <li class="task-list-item">
        <label class="task-list-control">
            <input type="checkbox" checked="">
            <span class="task-list-indicator"></span>
        </label>
        item 1
    </li>
</ul>
```
///

| Classes               | Description                                                                                            |
| --------------------- | ------------------------------------------------------------------------------------------------------ |
| `task-list`           | Attached to either the `ul` or `ol` tag and represents the entire list element.                        |
| `task-list-item`      | This is attached the `li` tag and represents an item in the list.                                      |
| `task-list-control`   | This is attached to the `label` tag and represents the control object.                                 |
| `task-list-indicator` | This is attached to the `span` directly following the input and is used to style the visual indicator. |

/// settings | CSS Setup

//// tab | Basic Tasklist
In order to style these we mainly remove the list type style and adjust the margins to align with normal list
styles.

```css
.markdown-body .task-list-item {
  list-style-type: none !important;
}

.markdown-body .task-list-item input[type="checkbox"] {
  margin: 0 4px 0.25em -20px;
  vertical-align: middle;
}
```
////

//// tab | Custom Tasklist

If custom check box icons are desired, custom styles can be used to give a unique look to the check marks.
Below is a very simple CSS example that creates a light gray square with rounded corners and displays a green
Unicode check mark when the control is checked.  This can be adapted to use web fonts, images, etc.

///// collapse-code
```css
.markdown-body .task-list-item {
  list-style-type: none !important;
}

.markdown-body .task-list-item input[type="checkbox"] {
  margin: 0 4px 0.25em -20px;
  vertical-align: middle;
}

.markdown-body .task-list-control {
  display: inline; /* Ensure label is inline incase theme sets it to block.*/
}

.markdown-body .task-list-control {
  position: relative;
  display: inline-block;
  color: #555;
  cursor: pointer;
}

.markdown-body .task-list-control input[type="checkbox"] {
  position: absolute;
  opacity: 0;
  z-index: -1; /* Put the input behind the label so it doesn't overlay text */
}

.markdown-body .task-list-indicator {
  position: absolute;
  top: -8px;
  left: -18px;
  display: block;
  width:  14px;
  height: 14px;
  color: #eee;
  background-color: #eee;
  border-radius: .25rem;
}

.markdown-body .task-list-control input[type="checkbox"]:checked + .task-list-indicator::before {
  display: block;
  margin-top: -4px;
  margin-left: 2px;
  font-size: 16px;
  line-height: 1;
  content: "✔";
  color: #1EBB52;
}
```
/////
////
///

## Options

Option               | Type | Default      | Description
-------------------- | ---- | ------------ | ------------
`custom_checkbox`    | bool | `#!py3 False` | Generate task lists in such a way as to allow for styling the check box with CSS.
`clickable_checkbox` | bool | `#!py3 False` | Enable user to interact with checkboxes.
