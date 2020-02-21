"""Generate emojione data."""
import os
import json
import sys
import copy
sys.path.append('../pymdownx/')
current_dir = os.path.dirname(os.path.abspath(__file__))

ADDITIONAL_ALIASES = {}

# Special emoji
SPECIAL_EMOJI = {
    # An unofficial emoji supported by very few
    ":pirate_flag:": {
        "category": "flags",
        "name": "pirate flag",
        "unicode": "1f3f4-200d-2620-fe0f"
    },
    ":shibuya:": {
        "category": "travel",
        "name": "Shibuya 109",
        "unicode": "e50a"
    },
    # Skier skin tones (not supported by Unicode spec)
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
    # Woman levitate (not supported in Unicode spec)
    ":woman_levitate:": {
        "category": "people",
        "name": "woman in business suit levitating",
        "unicode": "1f574-fe0f-200d-2640-fe0f",
        "aliases": ["woman_in_business_suit_levitating"]
    },
    ":woman_levitate_tone1:": {
        "category": "people",
        "name": "woman in business suit levitating: light skin tone",
        "unicode": "1f574-1f3fb-200d-2640-fe0f",
        "aliases": [
            "woman_in_business_suit_levitating_tone1",
            "woman_in_business_suit_levitating_light_skin_tone"
        ]
    },
    ":woman_leviate_tone2:": {
        "category": "people",
        "name": "woman in business suit levitating: medium-light skin tone",
        "unicode": "1f574-1f3fc-200d-2640-fe0f",
        "aliases": [
            "woman_in_business_suit_levitating_tone2",
            "woman_in_business_suit_levitating_medium_light_skin_tone"
        ]
    },
    ":woman_leviate_tone3:": {
        "category": "people",
        "name": "woman in business suit levitating: medium skin tone",
        "unicode": "1f574-1f3fd-200d-2640-fe0f",
        "aliases": [
            "woman_in_business_suit_levitating_tone3",
            "woman_in_business_suit_levitating_medium_skin_tone"
        ]
    },
    ":woman_leviate_tone4:": {
        "category": "people",
        "name": "woman in business suit levitating: medium-dark skin tone",
        "unicode": "1f574-1f3fe-200d-2640-fe0f",
        "aliases": [
            "woman_in_business_suit_levitating_tone4",
            "woman_in_business_suit_levitating_medium_dark_skin_tone"
        ]
    },
    ":woman_leviate_tone5:": {
        "category": "people",
        "name": "woman in business suit levitating: dark skin tone",
        "unicode": "1f574-1f3ff-200d-2640-fe0f",
        "aliases": [
            "woman_in_business_suit_levitating_tone5",
            "woman_in_business_suit_levitating_dark_skin_tone"
        ]
    },
    # Woman in tuxedo
    ":woman_in_tuxedo:": {
        "category": "people",
        "name": "woman in tuxedo",
        "unicode": "1f935-200d-2640-fe0f"
    },
    ":woman_in_tuxedo_tone1:": {
        "category": "people",
        "name": "woman in tuxedo: light skin tone",
        "unicode": "1f935-1f3fb-200d-2640-fe0f"
    },
    ":woman_in_tuxedo_tone2:": {
        "category": "people",
        "name": "woman in tuxedo: medium-light skin tone",
        "unicode": "1f935-1f3fc-200d-2640-fe0f"
    },
    ":woman_in_tuxedo_tone3:": {
        "category": "people",
        "name": "woman in tuxedo: medium skin tone",
        "unicode": "1f935-1f3fd-200d-2640-fe0f"
    },
    ":woman_in_tuxedo_tone4:": {
        "category": "people",
        "name": "woman in tuxedo: medium-dark skin tone",
        "unicode": "1f935-1f3fe-200d-2640-fe0f"
    },
    ":woman_in_tuxedo_tone5:": {
        "category": "people",
        "name": "woman in tuxedo: dark skin tone",
        "unicode": "1f935-1f3ff-200d-2640-fe0f"
    },

    # Transgender sign
    ":transgender_sign:": {
        "category": "symbols",
        "name": "transgender sign",
        "unicode": "26a7"
    },

    # Transgender flag
    ":transgender_flag:": {
        "category": "flags",
        "name": "transgender flag",
        "unicode": "1f3f3-fe0f-200d-26a7-fe0f"
    }
}

IGNORE_EMOJI = [
    # Alternative man levitating
    # Per spec, "levitate" is already a man,
    # no need to explicitly have a man variant.
    "1f574-fe0f-200d-2642-fe0f",
    "1f574-1f3fb-200d-2642-fe0f",
    "1f574-1f3fc-200d-2642-fe0f",
    "1f574-1f3fd-200d-2642-fe0f",
    "1f574-1f3fe-200d-2642-fe0f",
    "1f574-1f3ff-200d-2642-fe0f",

    # Alternative man in tuxedo
    # Per spec, "tuxedo" is already a man,
    # no need to explicitly have a man variant.
    "1f935-200d-2642-fe0f",
    "1f935-1f3fb-200d-2642-fe0f",
    "1f935-1f3fc-200d-2642-fe0f",
    "1f935-1f3fd-200d-2642-fe0f",
    "1f935-1f3fe-200d-2642-fe0f",
    "1f935-1f3ff-200d-2642-fe0f"
]


def parse(repo, tag, jtag, emojis, emoji_aliases):
    """Save test files."""

    asset_path = os.path.join(current_dir, 'tags', repo, repo, 'assets', 'svg')

    emoji_db = {}
    shortnames = set()
    aliases = {}
    unsupported = []

    for asset in os.listdir(asset_path):
        if os.path.isfile(os.path.join(asset_path, asset)) and asset.endswith('.svg'):
            unicode_value = asset[:-4]
            unicode_alt = unicode_value
            codes = unicode_alt.split('-')
            diff = 4 - len(codes[0])
            if diff > 0:
                codes[0] = ('0' * diff) + codes[0]
                unicode_alt = '-'.join(codes)
            found = False
            for k, v in emojis.items():
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

    for k, v in emoji_aliases.items():
        if v in emoji_db:
            aliases[k] = v

    # Copy emoji only found in EmojiOne
    for k, v in SPECIAL_EMOJI.items():
        if k not in emoji_db and k not in aliases:
            shortnames.add(k)
            copy_emoji = copy.copy(v)
            if 'aliases' in copy_emoji:
                del copy_emoji['aliases']
            emoji_db[k] = copy_emoji
            code_point = v.get('unicode_alt', v['unicode'])
            if code_point in unsupported:
                index = unsupported.index(code_point)
                del unsupported[index]
            special_aliases = v.get('aliases', [])
            for spec_alias in special_aliases:
                if spec_alias not in aliases:
                    aliases[spec_alias] = k

    # Additional aliases
    for k, v in ADDITIONAL_ALIASES.items():
        if k in emoji_db:
            for a in v:
                if a not in aliases:
                    aliases[a] = k

    # Remove ignored emoji from unsupported list
    for ignore in IGNORE_EMOJI:
        if ignore in unsupported:
            index = unsupported.index(ignore)
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
        f.write('version = "%s"\n' % tag)
        f.write('index_version = "%s"\n' % jtag)
        f.write('name = "twemoji"\n')
        f.write('emoji = %s\n' % json.dumps(emoji_db, sort_keys=True, indent=4, separators=(',', ': ')))
        f.write('aliases = %s\n' % json.dumps(aliases, sort_keys=True, indent=4, separators=(',', ': ')))

    # Print unsupported emoji
    if unsupported:
        print('Unsupported:')
        for code in unsupported:
            print(code)
