"""Generate emojione data."""
import os
import json
import sys
import copy
sys.path.append('../pymdownx/')
current_dir = os.path.dirname(os.path.abspath(__file__))

# Special emoji
special_emoji = {
    # An unoffical emoji supported by very few
    ":pirate_flag:": {
        "category": "flags",
        "name": "pirate flag",
        "unicode": "1f3f4-200d-2620-fe0f"
    },
    # Skier skin tones (not supported by EmojiOne yet)
    ":skier_tone1:": {
        "category": "activity",
        "name": "skier: light skin tone",
        "unicode": "26f7-1f3fb"
    },
    ":skier_tone2:": {
        "category": "activity",
        "name": "skier: medium-light skin tone",
        "unicode": "26f7-1f3fc"
    },
    ":skier_tone3:": {
        "category": "activity",
        "name": "skier: medium skin tone",
        "unicode": "26f7-1f3fd"
    },
    ":skier_tone4:": {
        "category": "activity",
        "name": "skier: medium-dark skin tone",
        "unicode": "26f7-1f3fe"
    },
    ":skier_tone5:": {
        "category": "activity",
        "name": "skier: dark skin tone",
        "unicode": "26f7-1f3ff"
    },
    # Not many support this one
    ":shibuya:": {
        "category": "travel",
        "name": "Shibuya 109",
        "unicode": "e50a"
    }
}


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
            unicode_value = asset[:-3]
            unicode_alt = unicode_value
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
                    emoji_db[k]['unicode'] = unicode_value
                    if 'unicode_alt' in emoji_db[k] and unicode_alt == unicode_value:
                        del emoji_db[k]['unicode_alt']
                    elif unicode_alt != unicode_value:
                        emoji_db[k]['unicode_alt'] = unicode_alt
                    found = True
                    break
            if not found:
                unsupported.append(unicode_value)

    for k, v in emojis.aliases.items():
        if v in emoji_db:
            aliases[k] = v

    # Copy emoji only found in EmojiOne
    for k, v in special_emoji.items():
        if k not in emoji_db and k not in aliases:
            shortnames.add(k)
            emoji_db[k] = copy.copy(v)
            code_point = v.get('unicode_alt', v['unicode'])
            if code_point in unsupported:
                index = unsupported.index(code_point)
                del unsupported[index]

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

    # Print unsupported emoji
    if unsupported:
        print('Unsupported:')
        for code in unsupported:
            print(code)
