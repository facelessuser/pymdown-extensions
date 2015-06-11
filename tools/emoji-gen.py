"""Generate a simple markdown file to test all emojis."""
import requests
import json


def get_github_emoji():
    """Get Github's usable emoji."""

    try:
        resp = requests.get(
            'https://api.github.com/emojis',
            timeout=30
        )
    except Exception:
        return None

    return json.loads(resp.text)


if __name__ == "__main__":
    emojis = get_github_emoji()
    if emojis is not None:
        with open('emoji.md', "w") as f:
            f.write('# Emojis\n')
            for emoji in sorted(emojis.keys()):
                f.write(':%s:' % emoji)
            f.write('\n')
