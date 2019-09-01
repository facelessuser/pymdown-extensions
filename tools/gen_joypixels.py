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

    return value['code_points']['fully_qualified']


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
            'unicode': v['code_points']['base'],
            'category': v['category']
        }
        alt = get_unicode_alt(v)
        if alt and alt != v['code_points']['base']:
            emoji_db[v['shortname']]['unicode_alt'] = alt

        for alias in v['shortname_alternates']:
            aliases[alias] = v['shortname']

    return emoji_db, aliases
