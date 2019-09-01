"""Generate gemoji index."""
import os
import requests
import json
import argparse
import sys
import shutil
import zipfile
import gen_emoji1
import gen_gemoji
import gen_twemoji
import gen_joypixels

current_dir = os.path.dirname(os.path.abspath(__file__))

GITHUB_API_HEADER = 'application/vnd.github.v3+json'
GITHUB_API = 'https://api.github.com'
GEMOJI = 'github/gemoji'
EMOJIONE = 'joypixels/emojione'
JOYPIXELS = 'joypixels/emoji-toolkit'
TWEMOJI = 'twitter/twemoji'

PY3 = sys.version_info >= (3, 0) and sys.version_info[0:2] < (4, 0)

if PY3:
    get_input = input
else:
    get_input = raw_input  # noqa


def url_join(*args):
    """Join URL parts."""
    return '/'.join(args)


def get_github_emoji():
    """Get GitHub's usable emoji."""
    try:
        resp = requests.get(
            url_join(GITHUB_API, 'emojis'),
            headers={'Accept': GITHUB_API_HEADER},
            timeout=30
        )
    except Exception:
        return None

    return json.loads(resp.text)


def extract_tag(repo, file_location):
    """Extract tag from zip."""
    with zipfile.ZipFile(file_location, "r") as z:
        z.extractall(os.path.dirname(file_location))
    repo_dir = None
    base = os.path.dirname(file_location)
    for x in os.listdir(base):
        fullname = os.path.join(base, x)
        if os.path.isdir(fullname) and x.startswith(repo.replace('/', '-')):
            repo_dir = fullname
            break
    if repo_dir:
        os.rename(repo_dir, os.path.join(base, repo.replace('/', '-')))


def download_tag(repo, tag, url):
    """Download tag."""
    destination = os.path.join(current_dir, 'tags', repo.replace('/', '-'))
    if not os.path.exists(destination):
        os.makedirs(destination)
    else:
        print('Removing old tag...')
        shutil.rmtree(destination)
        os.makedirs(destination)
    file_location = os.path.join(destination, os.path.basename(url) + '.zip')
    print('Downloading: %s --> %s' % (url, file_location))
    resp = requests.get(
        url,
        headers={'Accept': GITHUB_API_HEADER},
        stream=True
    )
    with open(file_location, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    extract_tag(repo, file_location)


def select_tag(repo, no_download):
    """Get GitHub's usable emoji."""
    resp = requests.get(
        url_join(GITHUB_API, 'repos', repo, 'releases'),
        headers={'Accept': GITHUB_API_HEADER},
        timeout=50
    )

    assert resp.status_code == 200, "API call failed to get tag list!"
    tags = json.loads(resp.text)

    print('Select %s tag to use:' % repo)
    num_tags = len(tags)
    text = []
    for index in range(num_tags):
        text.append('    [%d] %s' % (index, tags[index]['tag_name']))
        if (index + 1) % 4 == 0:
            text.append('\n')
    if len(text) == 0 or text[-1] != '\n':
        text.append('\n')
    print(''.join(text))
    user_input = None
    while user_input is None:
        try:
            user_input = int(get_input('Select Tag > '))
        except Exception:
            user_input = None
        if user_input is not None and (user_input < 0 or user_input >= num_tags):
            user_input = None

    if not no_download:
        download_tag(repo, tags[user_input]['tag_name'], tags[user_input]['zipball_url'])
    return tags[user_input]['tag_name']


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='gen_emoji', description='Generate emoji db files.')
    # Flag arguments
    parser.add_argument('--tag', default=None, help="Tag to use.")
    parser.add_argument('--joypixels-tag', default=None, help="Joypixels tag to use for Twemoji.")
    parser.add_argument('--joypixels-no-download', action='store_true', default=False, help="Skip Joypixels download.")
    parser.add_argument('--gemoji', action='store_true', default=False, help="Get Gemoji.")
    parser.add_argument('--emojione', action='store_true', default=False, help="Get Emojione.")
    parser.add_argument('--twemoji', action='store_true', default=False, help="Get Twemoji.")
    parser.add_argument('--no-download', action='store_true', default=False, help="Skip download and use local.")
    args = parser.parse_args()
    os.chdir(current_dir)
    if args.gemoji:
        if args.tag is None:
            tag = select_tag(GEMOJI, args.no_download)
        else:
            tag = args.tag
        gen_gemoji.parse(GEMOJI.replace('/', '-'), tag)
    if args.emojione:
        if args.tag is None:
            tag = select_tag(EMOJIONE, args.no_download)
        else:
            tag = args.tag
        gen_emoji1.parse(EMOJIONE.replace('/', '-'), tag)
    if args.twemoji:
        if args.joypixels_tag is None:
            jtag = select_tag(JOYPIXELS, args.joypixels_no_download)
        else:
            jtag = args.joypixels_tag
        db, aliases = gen_joypixels.parse(JOYPIXELS.replace('/', '-'), jtag)
        if args.tag is None:
            tag = select_tag(TWEMOJI, args.no_download)
        else:
            tag = args.tag
        gen_twemoji.parse(TWEMOJI.replace('/', '-'), tag, jtag, db, aliases)
