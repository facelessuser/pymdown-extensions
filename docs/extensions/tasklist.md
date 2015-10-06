# Tasklist {: .doctitle}
Github style tasklists.

---

## Overview
The Tasklist extension adds GFM style checkbox lists.  They follow the same syntax as GFM.

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
The HTML structure of tasklists is as follows:

```html
<ul class="task-list">
    <li class="task-list-item">
        <input type="checkbox" disabled="" checked="">
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

*[GFM]: Github Flavored Markdown
