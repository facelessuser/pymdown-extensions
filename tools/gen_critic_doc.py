"""Generate critic example for documents."""
import markdown
import sys
import os
import codecs
sys.path.insert(0, os.path.abspath(os.path.join('.', '..')))

critic_markup_example = '''\
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
'''

extensions = {
    'markdown.extensions.tables',
    'pymdownx.inlinehilite',
    'pymdownx.critic'
}

accept_extension_configs = {
    "pymdownx.highlight": {
        "css_class": "codehilite"
    },
    'pymdownx.critic': {
        'mode': 'accept'
    }
}

with codecs.open('docs/src/markdown/_snippets/critic-accept-example.txt', 'w', encoding='utf-8') as f:
    html = markdown.Markdown(
        extensions=extensions, extension_configs=accept_extension_configs
    ).convert(critic_markup_example)
    f.write(html.replace('\n', ''))

with codecs.open('docs/src/markdown/_snippets/critic-preview-example.txt', 'w', encoding='utf-8') as f:
    html = markdown.Markdown(
        extensions=extensions
    ).convert(critic_markup_example)
    f.write(html.replace('\n', ''))
