# HeaderAnchor {: .doctitle}
Github style header anchors.

---

## Overview
HeaderAnchor adds anchors to headers in the style of GFM&rsquo;s header anchors. The header anchors in this document were all generated with this extension.

## Options
By default, HeaderAnchor will use [Toc&rsquo;s](https://pythonhosted.org/Markdown/extensions/toc.html) settings (if Toc is being used), but HeaderAnchor can be run without Toc.  HeaderAnchor can also be run along side Toc and ignore Toc&rsquo;s settings; though it is advised to keep Toc and HeaderAnchor's settings in sync to ensure header links properly link.

| Option    | Type | Default |Description |
|-----------|------|---------|------------|
| separator | string | '-' | If ignoring Toc&rsquo;s settings, this will specify the word separator used. |
| slugify | function | Default method | If ignoring Toc&rsquo;s settings, this will specify the function to generate anchors based on header text.  By Default, this will use Toc&rsquo;s default, fallback slugify method, but if for any reason Toc is not installed, HeaderAnchor will fall back to an equivalent method. |
| use_toc_settings | bool | True | This specifies whether HeaderAnchor should get its settings from Toc.  This affects `slugify` and `separator`. |

## Alternate Slugify
Python Markdown's default slugify strips out Unicode chars. To better handle Unicode, a couple of optional slugify options have been provided.

### uslugify
In order to get slugs closer to like GFM&rsquo;s slugs (in regards to Unicode chars), a slugify has been included at `pymdownx.headerancor.uslugify`.  This assumes you are encoding your HTML as UTF-8.  UTF-8 Unicode should be okay in your slugs in modern browsers.  You can use this to override Toc's and HeaderAnchor's slugify; it is good to override both if you are using both.

### uslugify_encoded
If you aren't encoding your HTML as UTF-8, or prefer the safer percent encoded Unicode slugs, you can use `uslugify_encoded` which will percent encode non-ASCII word chars.  You can use this to override Toc's and HeaderAnchor's slugify; it is good to override both if you are using both.

## CSS
This is the CSS used for rendering the header anchors in this document. While Font Awesome is used, you can substitute it with [Octicons](https://octicons.github.com/) for even more of a GFM feel, or use something else entirely.

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

| Classes | Description |
|---------|-------------|
| headeranchor-link | This is attached to the actual anchor tag that links to the header. |
| headeranchor | This is the header anchor character you see.  In this case, it is the [link character from Font Awesome](http://fortawesome.github.io/Font-Awesome/icon/link/). |

The CSS below sets the header tags to be `relative`, and the `headeranchor-link` class to be `absolute`.  We then attach a `:before` pseudo element to the `headeranchor` class with the desired character and position.  We play a little bit with padding and margin so when you hover over the header or where the link is supposed to be, the link appears and is accessible without causing the header position to change.

```css
/* Header Anchors */
.markdown-body {
    padding-left: 30px;
}

.markdown-body .headeranchor-link {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  display: block;
  padding-right: 6px;
  padding-left: 30px;
  margin-left: -30px;
}

.markdown-body .headeranchor-link:focus {
  outline: none;
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4,
.markdown-body h5,
.markdown-body h6 {
  position: relative;
}

.markdown-body h1 .headeranchor,
.markdown-body h2 .headeranchor,
.markdown-body h3 .headeranchor,
.markdown-body h4 .headeranchor,
.markdown-body h5 .headeranchor,
.markdown-body h6 .headeranchor {
  display: none;
  color: #000;
  vertical-align: middle;
}

.markdown-body h1:hover .headeranchor-link,
.markdown-body h2:hover .headeranchor-link,
.markdown-body h3:hover .headeranchor-link,
.markdown-body h4:hover .headeranchor-link,
.markdown-body h5:hover .headeranchor-link,
.markdown-body h6:hover .headeranchor-link {
  height: 1em;
  padding-left: 8px;
  margin-left: -30px;
  line-height: 1;
  text-decoration: none;
}

.markdown-body h1:hover .headeranchor-link .headeranchor,
.markdown-body h2:hover .headeranchor-link .headeranchor,
.markdown-body h3:hover .headeranchor-link .headeranchor,
.markdown-body h4:hover .headeranchor-link .headeranchor,
.markdown-body h5:hover .headeranchor-link .headeranchor,
.markdown-body h6:hover .headeranchor-link .headeranchor {
  display: inline-block;
}

.markdown-body .headeranchor {
  font: normal normal 16px FontAwesome;
  line-height: 1;
  display: inline-block;
  text-decoration: none;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.headeranchor:before {
  content: '\f0c1';
}
```

*[GFM]: Github Flavored Markdown
*[Toc]: Table of Contents
