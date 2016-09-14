# Tasklist {: .doctitle}
Github style tasklists.

---

## Overview
The Tasklist extension adds GFM style checkbox lists.  They follow the same syntax as GFM.

## Options

| Option    | Type | Default | Description |
|-----------|------|---------|-------------|
| custom_checkbox | bool | False | Inserts an empty `label` tag after the `input` tag to allow styling the checkbox with CSS. |

## Examples

```
Task List

- [X] item 1
    * [X] item A
    * [ ] item B
        more text
        + [x] item a
        + [ ] item b
        + [x] item c
    * [X] item C
- [ ] item 2
- [ ] item 3
```

Task List

- [X] item 1
    * [X] item A
    * [ ] item B
        more text
        + [x] item a
        + [ ] item b
        + [x] item c
    * [X] item C
- [ ] item 2
- [ ] item 3

# CSS
The default HTML structure of tasklists is found below:

```html
<ul class="task-list">
    <li class="task-list-item">
        <input type="checkbox" disabled="" checked="">
        item 1
    </li>
</ul>
```

If `custom_checkbox` is enabled the structure will be as follows:

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

| Classes | Description |
|---------|-------------|
| task-list | Attached to either the `ul` or `ol` tag and represents the entire list element. |
| task-list-item | This is attached the `li` tag and represents a an item in the list. |
| task-list-control | This is attached to the `label` tag and represents the control object. |
| task-list-indicator | This is attached to the `span` directly following the input and is used to style the visual indicator. |

In order to style these we mainly remove the list type style and adjust the margins to align with normal list styles.

```css
.markdown-body .task-list-item {
  list-style-type: none !important;
}

.markdown-body .task-list-item input[type="checkbox"] {
  margin: 0 4px 0.25em -20px;
  vertical-align: middle;
}
```

If custom checkbox icons are desired, custom styles can be used to give a unique look to the checkmarks.  Below is a 
very simple example that creates a light gray square with rounded corners and displays a green Unicode check mark when 
the control is checked.  This can be adapted to use webfonts, images, etc.

!!! note "Note"
    It can be noted that the `task-list-control` class is forced to inline in this example, but that is only because 
    the MkDocs theme used for this document set labels to blocks.  Normally this would not be needed.

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

<div class="custom-task-list" markdown="1">
- [X] item 1
    * [X] item A
    * [ ] item B
        more text
        + [x] item a
        + [ ] item b
        + [x] item c
    * [X] item C
- [ ] item 2
- [ ] item 3
</div>


*[GFM]: Github Flavored Markdown
