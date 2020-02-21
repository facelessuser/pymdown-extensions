"""Generate emojione data."""
import os
import json
current_dir = os.path.dirname(os.path.abspath(__file__))
LICENSE = """
MIT license.

Copyright (c) http://www.emojione.com
"""


def get_unicode_alt(value):
    """Get alternate Unicode form or return the original."""

    return value['unicode_alt']


def parse(repo, tag):
    """Save test files."""
    # Load emoji database
    with open(os.path.join(current_dir, 'tags', repo, repo, 'emoji.json'), 'r') as f:
        emojis = json.loads(f.read())

    emoji_db = {}
    shortnames = set()
    aliases = {}
    for v in emojis.values():
        shortnames.add(v['shortname'])
        emoji_db[v['shortname']] = {
            'name': v['name'],
            'unicode': v['unicode'],
            'category': v['category']
        }
        alt = get_unicode_alt(v)
        if alt:
            emoji_db[v['shortname']]['unicode_alt'] = alt

        for alias in v['aliases']:
            aliases[alias] = v['shortname']

    # Save test files
    for test in ('png', 'png sprite', 'svg', 'svg sprite', 'entities', 'long title', 'no title'):
        with open('../tests/extensions/emoji/emoji1 (%s).txt' % test, 'w') as f:
            f.write('# Emojis\n')
            count = 0
            for emoji in sorted(shortnames):
                f.write(''.join('%s %s<br>\n' % (emoji[1:-1], emoji)))
                count += 1
                if test != 'png' and count == 10:
                    break

    # Write out essential info
    with open('../pymdownx/emoji1_db.py', 'w') as f:
        # Dump emoji db to file and strip out PY2 unicode specifiers
        f.write('"""Emojione autogen.\n\nGenerated from emojione source. Do not edit by hand.\n%s"""\n' % LICENSE)
        f.write('version = "%s"\n' % tag)
        f.write('name = "emojione"\n')
        f.write('emoji = %s\n' % json.dumps(emoji_db, sort_keys=True, indent=4, separators=(',', ': ')))
        f.write('aliases = %s\n' % json.dumps(aliases, sort_keys=True, indent=4, separators=(',', ': ')))
