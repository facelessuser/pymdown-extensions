"""Generate gemoji data."""
import sys
import os
import json
current_dir = os.path.dirname(os.path.abspath(__file__))

U_JOIN = 0x200d
U_VARIATION_SELECTOR_16 = 0xfe0f
U_EXTRA = (U_JOIN, U_VARIATION_SELECTOR_16)

if sys.maxunicode == 0xFFFF:

    def get_code_points(s):
        """Get the Unicode code points."""

        pt = []

        def is_full_point(p, point):
            """
            Check if we have a full code point.

            Surrogates are stored in point.
            """
            v = ord(p)
            if 0xD800 <= v <= 0xDBFF:
                del point[:]
                point.append(p)
                return False
            if point and 0xDC00 <= v <= 0xDFFF:
                point.append(p)
                return True
            del point[:]
            return True

        return [(''.join(pt) if pt else c) for c in s if is_full_point(c, pt)]

    def get_ord(c):
        """Get Unicode ordinal number."""

        if len(c) == 2:
            high, low = (ord(p) for p in c)
            ordinal = (high - 0xD800) * 0x400 + low - 0xDC00 + 0x10000
        else:
            ordinal = ord(c)

        return ordinal

else:
    def get_code_points(s):
        """Get the Unicode code points."""

        return list(s)

    def get_ord(c):
        """Get Unicode ordinal number."""

        return ord(c)


def get_unicode(value):
    """Get Unicode."""

    uc = '-'.join(
        ['%04x' % get_ord(point) for point in get_code_points(value['emoji']) if get_ord(point) not in U_EXTRA]
    )

    uc_alt = '-'.join(
        ['%04x' % get_ord(point) for point in get_code_points(value['emoji'])]
    )

    if uc == uc_alt:
        uc_alt = None

    return uc, uc_alt


def get_gemoji_specific(value):
    """Get alternate Unicode form or return the original."""

    return value['aliases'][0]


def parse(repo, tag):
    """Save test files."""
    # Load emoji database
    with open(os.path.join(current_dir, 'tags', repo, repo, 'db', 'emoji.json'), 'r', encoding='utf-8') as f:
        emojis = json.loads(f.read())

    emoji_db = {}
    shortnames = set()
    aliases = {}
    for v in emojis:
        short = v['aliases'][0]
        shortnames.add(':%s:' % short)
        if 'emoji' in v:
            uc, uc_alt = get_unicode(v)
            emoji_db[':%s:' % short] = {
                'name': v.get('description', short),
                'unicode': uc,
                'category': v['category']
            }
            if uc_alt:
                emoji_db[':%s:' % short]['unicode_alt'] = uc_alt
        else:
            emoji_db[':%s:' % short] = {
                'name': v.get('description', short)
            }

        for alias in v['aliases'][1:]:
            aliases[':%s:' % alias] = ':%s:' % short

    # Save test files
    for test in ('png', 'entities'):
        with open('../tests/extensions/emoji/gemoji (%s).txt' % test, 'w') as f:
            f.write('# Emojis\n')
            count = 0
            for emoji in sorted(shortnames):
                f.write(''.join('{} {}<br>\n'.format(emoji[1:-1], emoji)))
                count += 1
                if test != 'png' and count == 10:
                    break

    with open(os.path.join(current_dir, 'tags', repo, repo, 'LICENSE')) as f:
        license_content = f.read()

    # Write out essential info
    with open('../pymdownx/gemoji_db.py', 'w') as f:
        # Dump emoji db to file and strip out PY2 unicode specifiers
        f.write('"""Gemoji autogen.\n\nGenerated from gemoji source. Do not edit by hand.\n\n%s"""\n' % license_content)
        f.write('version = "%s"\n' % tag)
        f.write('name = "gemoji"\n')
        f.write('emoji = %s\n' % json.dumps(emoji_db, sort_keys=True, indent=4, separators=(',', ': ')))
        f.write('aliases = %s\n' % json.dumps(aliases, sort_keys=True, indent=4, separators=(',', ': ')))
