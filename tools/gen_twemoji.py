"""Generate emojione data."""
import os
import json
import sys
import copy
sys.path.append('../pymdownx/')
current_dir = os.path.dirname(os.path.abspath(__file__))


def get_unicode_alt(value):
    """Get alternate Unicode form or return the original."""

    return value['code_points']['output']


def parse(repo, tag):
    """Save test files."""
    # Load emoji database
    import emoji1_db as emojis

    asset_path = os.path.join(current_dir, 'tags', repo, repo, '2', 'assets')

    emoji_db = {}
    shortnames = set()
    aliases = {}
    unsupported = []

    for asset in os.listdir(asset_path):
        if os.path.isfile(os.path.join(asset_path, asset)) and asset.endswith('.ai'):
            unicode = asset[:-3]
            unicode_alt = unicode
            codes = unicode_alt.split('-')
            diff = 4 - len(codes[0])
            if diff > 0:
                codes[0] = ('0' * diff) + codes[0]
                unicode_alt = '-'.join(codes)
            found = False
            for k, v in emojis.emoji.items():
                db_unicode = v.get('unicode_alt', v.get('unicode'))
                if (
                    db_unicode and
                    (unicode_alt == db_unicode or unicode_alt.replace('-fe0f', '') == db_unicode.replace('-fe0f', ''))
                ):
                    shortnames.add(k)
                    emoji_db[k] = copy.copy(v)
                    emoji_db[k]['unicode'] = unicode
                    if 'unicode_alt' in emoji_db[k] and unicode_alt == unicode:
                        del emoji_db[k]['unicode_alt']
                    elif unicode_alt != unicode:
                        emoji_db[k]['unicode_alt'] = unicode_alt
                    found = True
                    break
            if not found:
                unsupported.append(unicode)

    for k, v in emojis.aliases.items():
        if v in emoji_db:
            aliases[k] = v

    # Save test files
    for test in ('png', 'svg', 'entities'):
        with open('../tests/extensions/emoji/twemoji (%s).txt' % test, 'w') as f:
            f.write('# Emojis\n')
            count = 0
            for emoji in sorted(shortnames):
                f.write(''.join('%s %s<br>\n' % (emoji[1:-1], emoji)))
                count += 1
                if test != 'png' and count == 10:
                    break

    # Write out essential info
    with open('../pymdownx/twemoji_db.py', 'w') as f:
        # Dump emoji db to file and strip out PY2 unicode specifiers
        f.write('"""Twemoji autogen.\n\nNames from emojione database. Do not edit by hand.\n"""\n')
        f.write('from __future__ import unicode_literals\n')
        f.write('version = "%s"\n' % tag)
        f.write('name = "twemoji"\n')
        f.write('emoji = %s\n' % json.dumps(emoji_db, sort_keys=True, indent=4, separators=(',', ': ')))
        f.write('aliases = %s\n' % json.dumps(aliases, sort_keys=True, indent=4, separators=(',', ': ')))

    print('Unsupported:')
    for code in unsupported:
        print(code)
