[:octicons-file-code-24:][_critic]{: .source-link }

# Critic

## Overview

Critic is an extension that adds handling and support of [Critic Markup][critic-markup] which uses a special syntax to
represent edits to a Markdown document.  This extension runs before all other extensions to parse the critic edits.

Critic allows you to automatically accept edits or reject the edits and render the output accordingly. It also allows
for visually displaying the changes in HTML output ([mileage may vary](#limitations-with-previewing-critic-markup)).

The Critic extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.critic'])
```

## Usage

Critic Markup uses special markup to insert, delete, substitute, highlight, and comment.

To insert or remove text you can use `#!critic-markup {++insert me++}` and `#!critic-markup {--remove me--}`
respectively.  You can also denote a substitution with `#!critic-markup {~~substitute this~>with this~~}`.

You can also highlight specific text with `#!critic-markup {==highlight me==}`. Or even comment, which is generally done
by highlighting text and following it with a comment: `#!critic-markup {==highlight me==}{>>Add a comment<<}`.

!!! example "Critic Markup Accept Example"

    === "Output"
        --8<-- "critic-accept-example.txt"

    === "Markdown"
        ```critic-markup
        Here is some {--*incorrect*--} Markdown.  I am adding this{++ here++}.  Here is some more {--text
         that I am removing--}text.  And here is even more {++text that I 
         am ++}adding.{~~

        ~>  ~~}Paragraph was deleted and replaced with some spaces.{~~  ~>

        ~~}Spaces were removed and a paragraph was added.

        And here is a comment on {==some
         text==}{>>This works quite well. I just wanted to comment on it.<<}. Substitutions {~~is~>are~~} great!

        General block handling.

        {--

        * test remove
        * test remove
        * test remove
            * test remove
        * test remove

        --}

        {++

        * test add
        * test add
        * test add
            * test add
        * test add

        ++}
        ```

When previewing, you can style them to stand out (see [CSS](#css) for more information):

!!! example "Critic Markup Preview Example"

    === "Output"
        --8<-- "critic-preview-example.txt"

    === "Markdown"
        ```critic-markup
        Here is some {--*incorrect*--} Markdown.  I am adding this{++ here++}.  Here is some more {--text
         that I am removing--}text.  And here is even more {++text that I 
         am ++}adding.{~~

        ~>  ~~}Paragraph was deleted and replaced with some spaces.{~~  ~>

        ~~}Spaces were removed and a paragraph was added.

        And here is a comment on {==some
         text==}{>>This works quite well. I just wanted to comment on it.<<}. Substitutions {~~is~>are~~} great!

        General block handling.

        {--

        * test remove
        * test remove
        * test remove
            * test remove
        * test remove

        --}

        {++

        * test add
        * test add
        * test add
            * test add
        * test add

        ++}
        ```

## Limitations with Previewing Critic Markup

Parsing CriticMarkup is very straight forward.  If you need to reject critic marks or accept them, the Critic extension
will work quite well.  But when trying to render the edits visually **and** trying to convert the document to HTML,
things can get ugly.  I think this is the one unfortunate problem with CriticMarkup.  The existence of the critic edits
can alter the actual source.  Its a fantastic idea, but it should be understood that when using CriticMarkup beyond
inline or block paragraphs, there is a possibility that invalid HTML will be created for the preview (especially in
relation to lists or if breaking up Markdown syntax).  I think Fletcher of [MultiMarkdown][multi-markdown] said it best
here:

> I view CriticMarkup as two things:

> 1. A syntax for documenting editing notes and changes, and for collaborating amongst coauthors.

> 2. A means to display those notes/changes in the HTML output.

> I believe that \#1 is a really great idea, and well implemented. \#2 is not so well implemented, largely due to the
  "orthogonal" nature of CriticMarkup and the underlying Markdown syntax.

> CM is designed as a separate layer on top of Markdown/MultiMarkdown. This means that a Markdown span could, for
  example, start in the middle of a CriticMarkup structure, but end outside of it. This means that an algorithm to
  properly convert a CM/Markdown document to HTML would be quite complex, with a huge number of edge cases to consider.
  I've tried a few (fairly creative, in my opinion) approaches, but they didn't work. Perhaps someone else will come up
  with a better solution, or will be so interested that they put the work in to create the complex algorithm. I have no
  current plans to do so.

The Critic extension does its best by employing a preprocessor to inject the critic tags before all other parsing and a
post-processor to clean up some of the weird side effects of the injection (only selected odd cases as others are more
difficult to fix).  It injects some classes into the edit region's HTML output which allows for CSS styling.  There is
probably a lot more post-processing that could be done to fix more issues, but whether this extension will be going
further down that road has not yet been decided.

## CSS

Critic renders the CriticMarkup with the following classes.

Classes   | Description
--------- |------------
`critic`  | This is applied to all critic edits.
`break`   | This is applied to critic inserts or deletes that encompass **only** 2+ newlines.
`block`   | Applied to critic HTML tags that are detected as surrounding a block region.
`comment` | A CriticMarkup comment.

??? settings "Basic CSS Setup"

    ```css
    /* Critic Markup */
    .markdown-body .critic {
      font-family: inherit;
      -webkit-border-radius: 3px;
      -moz-border-radius: 3px;
      border-radius: 3px;
      border-style: solid;
      border-width: 1px;
      padding-top: 0.1em;
      padding-bottom: 0.1em;
      text-decoration: none;
    }

    .markdown-body .critic:before,
    .markdown-body .critic:after {
      content: '\00a0';
      padding-top: 0.1em;
      padding-bottom: 0.1em;
      font-size: initial;
    }

    .markdown-body .block:before,
    .markdown-body .block:after {
      content: '';
    }

    .markdown-body mark.critic {
      border-color: #ff8600;
      background: #ffddaa;
    }

    .markdown-body ins.critic {
      border-color: #00bb00;
      background: #ddffdd;
    }

    .markdown-body del.critic {
      border-color: #dd0000;
      background: #ffdddd;
    }

    .markdown-body ins.break,
    .markdown-body del.break {
      font-size: 0;
      border: none;
    }

    .markdown-body ins.break:before,
    .markdown-body del.break:before {
      content: '\00a0\b6\00a0';
      -webkit-border-radius: 3px;
      -moz-border-radius: 3px;
      border-radius: 3px;
    }

    .markdown-body ins.after,
    .markdown-body del.after {
      content: '';
    }

    .markdown-body ins.break:before {
      color: #00bb00;
      border: 1px solid #00bb00;
      background: #ddffdd;
    }

    .markdown-body del.break:before {
      color: #bb0000;
      border: 1px solid #bb0000;
      background: #ffdddd;
    }

    .markdown-body span.critic {
      background: #ddddff;
      border: 0;
      border-top: 1px solid #0000bb;
      border-bottom: 1px solid #0000bb;
    }

    .markdown-body span.critic:before,
    .markdown-body span.critic:after {
      font-size: inherit;
      background: #ddddff;
      border: 1px solid #0000bb;
    }

    .markdown-body span.critic:before {
      content: '\00a0\bb';
      border-right: none;
      -webkit-border-top-left-radius: 3px;
      -moz-border-top-left-radius: 3px;
      border-top-left-radius: 3px;
      -webkit-border-bottom-left-radius: 3px;
      -moz-border-bottom-left-radius: 3px;
      border-bottom-left-radius: 3px;
    }

    .markdown-body span.critic:after {
      content: '\ab\00a0';
      border-left: none;
      -webkit-border-top-right-radius: 3px;
      -moz-border-top-right-radius: 3px;
      border-top-right-radius: 3px;
      -webkit-border-bottom-right-radius: 3px;
      -moz-border-bottom-right-radius: 3px;
      border-bottom-right-radius: 3px;
    }

    .markdown-body .block {
      display: block;
      padding: .02em;
    }
    ```

## Options

Option    | Type   | Default     | Description
--------- |------- | ----------- | -----------
`mode`    | string | `#!py3 view` | `view` just parses the markup and displays it in its HTML equivalent rendering. `accept` strips out the critic markup and replaces them with the suggested changes.  `reject` rejects all the suggestions and strips the critic markup out replacing it with the original.


--8<-- "links.txt"
