import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join('.')))

import pymdownx.kbd as kbd

STYLE = '''<style>
/* Text Blocks */

kbd {
  font-family: Consolas, "Liberation Mono", Menlo, Courier, monospace;
  font-size: 12px;
}

kbd {
  padding: .3em .6em .1em .6em;
  border: 1px solid #ccc;
  background-color: #f6f6f6;
  color: #333;
  -moz-box-shadow: 0 1px 0 rgba(0,0,0,0.2),0 0 0 2px #fff inset;
  -webkit-box-shadow: 0 1px 0 rgba(0,0,0,0.2),0 0 0 2px #fff inset;
  box-shadow: 0 1px 0 rgba(0,0,0,0.2),0 0 0 2px #fff inset;
  -webkit-border-radius: 3px;
  -moz-border-radius: 3px;
  border-radius: 3px;
  display: inline-block;
  margin: 0 .1em;
  text-shadow: 0 1px 0 #fff;
}
</style>
'''


def main():
    with open('tests/extensions/kbd.txt', 'w') as f:
        f.write(STYLE)
        f.write('# Keys\n')
        for key in sorted(kbd.keymap.keymap.keys()):
            f.write('++%s++\n' % key)
        f.write('# Aliases\n')
        for key in sorted(kbd.keymap.aliases.keys()):
            f.write('++%s++\n' % key)


if __name__ == "__main__":
    main()
