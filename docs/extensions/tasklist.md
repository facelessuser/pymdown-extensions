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
The HTML structure of tasklists is found below.  It should be noted that there is an empty label tag after the input. 
The empty tag is only included when `custom_checkbox` is set to `true`, and it is included to facilitate more advanced 
styling with webfonts, images, etc.

```html
<ul class="task-list">
    <li class="task-list-item">
        <!-- label tag is optional and is only included when 'custom_checkbox' is 'true' -->
        <input type="checkbox" disabled="" checked=""><label></label>
        item 1
    </li>
</ul>
```

| Classes | Description |
|---------|-------------|
| task-list | Attached to either the `ul` or `ol` tag and represents the entire list element. |
| task-list-item | This is attached the `li` tag and represents a an item in the list. |

In order to style these we mainly remove the list type style and adjust the margins to align with normal list styles.

```css
.markdown-body .task-list-item {
  list-style-type: none;
}

.markdown-body .task-list-item input {
  margin: 0 4px 0.25em -20px;
  vertical-align: middle;
}
```

If custom checkbox icons are desired, they can be configured as shown below. The example will utilize Unicode check marks.

```css
.markdown-body .task-list-item {
  position: relative;
}

.markdown-body .task-list-item input[type="checkbox"] {
  opacity: 0;
}

.markdown-body .task-list-item input[type="checkbox"] + label {
  display: block;
  position: absolute;
  top: 4px;
  left: -24px;
  width: 16px;
  height: 16px;
  border-radius: 2px;
  background: #CCC;
}

.markdown-body .task-list-item input[type="checkbox"]:checked + label::before {
  display: block;
  margin-top: -4px;
  margin-left: 2px;
  font-size: 1.2em;
  line-height: 1;
  border-radius: 2px;
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
