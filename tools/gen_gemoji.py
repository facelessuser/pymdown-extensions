"""Generate gemoji data."""
import sys
import os
import json
current_dir = os.path.dirname(os.path.abspath(__file__))
PY27 = sys.version_info >= (2, 7) and sys.version_info < (2, 8)

U_JOIN = 0x200d
U_VARIATION_SELECTOR_16 = 0xfe0f
U_EXTRA = (U_JOIN, U_VARIATION_SELECTOR_16)

if PY27:
    # For ease of supporting, just require uniseq for both narrow and wide PY27.
    import uniseg.codepoint

    def get_code_points(s):
        """Get the Unicode code points."""

        return list(uniseg.codepoint.code_points(s))

    def get_ord(c):
        """Get Unicode ord."""

        return uniseg.codepoint.ord(c)

else:
    def get_code_points(s):
        """Get the Unicode code points."""

        return [c for c in s]

    def get_ord(c):
        """Get Unicode ord."""

        return ord(c)


def get_unicode(value):
    """Get alternate Unicode form or return the original."""

    return '-'.join(
        ['%04x' % get_ord(point) for point in get_code_points(value['emoji']) if get_ord(point) not in U_EXTRA]
    )


def get_unicode_alt(value):
    """Get Unicode."""

    return '-'.join(
        ['%04x' % get_ord(point) for point in get_code_points(value['emoji'])]
    )


def get_gemoji_specific(value):
    """Get alternate Unicode form or return the original."""

    return value['aliases'][0]


def parse(repo, tag):
    """Save test files."""
    # Load emoji database
    with open(os.path.join(current_dir, 'tags', repo, repo, 'db', 'emoji.json'), 'r') as f:
        emojis = json.loads(f.read())

    emoji_db = {}
    shortnames = set()
    aliases = {}
    for v in emojis:
        short = v['aliases'][0]
        shortnames.add(':%s:' % short)
        emoji_db[':%s:' % short] = {
            'name': v.get('description', short),
            'unicode': get_unicode(v) if 'emoji' in v else '',
            'unicode_alt': get_unicode_alt(v) if 'emoji' in v else ''
        }
        for alias in v['aliases'][1:]:
            aliases[':%s:' % alias] = ':%s:' % short

    # Save test files
    for test in ('png', 'entities'):
        with open('../tests/extensions/gemoji (%s).txt' % test, 'w') as f:
            f.write('# Emojis\n')
            for emoji in shortnames:
                f.write(''.join('%s %s<br>\n' % (emoji[1:-1], emoji)))
            f.write('\n')

    with open(os.path.join(current_dir, 'tags', repo, repo, 'LICENSE'), 'r') as f:
        license = f.read()

    # Write out essential info
    with open('../pymdownx/gemoji_db.py', 'w') as f:
        # Dump emoji db to file and strip out PY2 unicode specifiers
        f.write('"""Gemoji autogen.\n\nGenerated from gemoji source. Do not edit by hand.\n\n%s"""\n' % license)
        f.write('version = "%s"\n' % tag)
        f.write('emoji = %s\n' % json.dumps(emoji_db, sort_keys=True, indent=4, separators=(',', ': ')))
        f.write('aliases = %s\n' % json.dumps(aliases, sort_keys=True, indent=4, separators=(',', ': ')))
