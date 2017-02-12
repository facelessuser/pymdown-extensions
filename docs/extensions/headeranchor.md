## Overview

!!! warning "Deprecated Extension"
    This extension has been deprecated in version `1.4.0` and will be removed in `3.0`.  The same effect can be accomplished using
    `markdown.extensions.toc` with `permalinks` and some custom CSS.  It doesn't make sense to continue supporting this as nothing is really gained by specifically doing anchors GitHub's way.

HeaderAnchor adds anchors to headers in the style of GFM's header anchors (anchors that appear to the left of the headers when the cursor hovers over the header). The header anchors in this document were all generated with this extension.

## Options

By default, HeaderAnchor will use [Toc's][toc] settings (if Toc is being used), but HeaderAnchor can be run without Toc.  HeaderAnchor can also be run along side Toc and ignore Toc's settings; though it is advised to keep Toc and HeaderAnchor's settings in sync to ensure header links properly link.

Option             | Type     | Default        |Description
------------------ | -------- |--------------- |-----------
`separator`        | string   | `#!py '-'`     | If not using Toc, or ignoring Toc's settings, this will specify the word separator used.
`slugify`          | function | Default method | If not using Toc, or ignoring Toc's settings, this will specify the function to generate anchors based on header text.  By Default, this will use Toc's default, fallback slugify method, but if for any reason Toc is not installed, HeaderAnchor will fall back to an equivalent method.
`use_toc_settings` | bool     | `#!py True`    | This specifies whether HeaderAnchor should get its settings from Toc.  This affects `slugify` and `separator`.

## Alternate Slugify

Python Markdown's default slugify strips out Unicode chars. To better handle Unicode, a couple of optional slugify options have been provided.

!!! note "Note"
    This extension has been deprecated. But for legacy compatibility, you can still reference slugs at `pymdownx.headeranchor`, but slugs are actually found at `pymdownx.slugs` moving forward.

### uslugify

In order to get slugs closer to like GFM's slugs (in regards to Unicode chars), a slugify has been included at `pymdownx.slugs.uslugify`.  This assumes you are encoding your HTML as UTF-8.  UTF-8 Unicode should be okay in your slugs in modern browsers.  You can use this to override Toc's and/or HeaderAnchor's slugify.

### uslugify_encoded

If you aren't encoding your HTML as UTF-8, or prefer the safer percent encoded Unicode slugs, you can use `pymdownx.slugs.uslugify_encoded` which will percent encode non-ASCII word chars.  You can use this to override Toc's and/or HeaderAnchor's slugify.

## CSS

Here we will show some example CSS for rendering the header anchors. While Material Icon font is used in this example, you can substitute it with [Octicons][octicons] for even more of a GFM feel, or use something else entirely.

The HTML tags with classes are set like this:

```html
<h1 id="css">
    <a name="user-content-css" href="#css" class="headeranchor-link" aria-hidden="true">
        <span class="headeranchor"></span>
    </a>
    CSS
</h1>
```

We have two classes to work with:

Classes             | Description
--------------------|------------
`headeranchor-link` | This is attached to the actual anchor tag that links to the header.
`headeranchor`      | This is the span we attach the anchor character to.

The CSS below is an example.

```css
/* Header Anchors */
.markdown-body .headeranchor-link {
  opacity: 0;
  float: left;
  margin-top:  -.5rem;
  padding-right: 4px;
  margin-left: -2.4rem;
  text-decoration: none;
}

.markdown-body .headeranchor-link:not(:hover) {
  color: rgba(0, 0, 0, 0.26);
}

.markdown-body .headeranchor-link:focus {
  outline: none;
}

.markdown-body h1:target .headeranchor-link,
.markdown-body h2:target .headeranchor-link,
.markdown-body h3:target .headeranchor-link,
.markdown-body h4:target .headeranchor-link,
.markdown-body h5:target .headeranchor-link,
.markdown-body h6:target .headeranchor-link {
  opacity: 1;
  text-decoration: none;
  -webkit-transform:translateY(.5rem);
  transform:translateY(.5rem);
}

.markdown-body h1:hover .headeranchor-link,
.markdown-body h2:hover .headeranchor-link,
.markdown-body h3:hover .headeranchor-link,
.markdown-body h4:hover .headeranchor-link,
.markdown-body h5:hover .headeranchor-link,
.markdown-body h6:hover .headeranchor-link {
  opacity: 1;
  text-decoration: none;
  -webkit-transform:translateY(.5rem);
  transform:translateY(.5rem);
  -webkit-transition: color .25s,opacity .125s .25s,-webkit-transform .25s .25s;
  transition: color .25s,opacity .125s .25s,-webkit-transform .25s .25s;
  transition: transform .25s .25s,color .25s,opacity .125s .25s;
  transition: transform .25s .25s,color .25s,opacity .125s .25s,-webkit-transform .25s .25s;
}

.markdown-body .headeranchor {
  vertical-align: middle;
  font: normal normal 2rem "Material Icons";
  line-height: 1;
  display: inline-block;
  text-decoration: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.markdown-body .headeranchor:before {
  content: '\E157';
}
```

--8<-- "refs.md"
