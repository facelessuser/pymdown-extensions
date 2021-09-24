"""Library for embedding media and such."""
from markdown import Extension
from markdown.treeprocessors import Treeprocessor
from markdown import util as md_util
import xml.etree.ElementTree as etree
import re
import copy


RE_YOUTUBE = re.compile(
    r"""(?ix)^
    (?:https://(?:www\.)?youtube\.com/embed/|https://youtu\.be/|https://www.youtube.com/watch?v=)
    (?P<id>[a-z0-9-]+)(?P<extra>[?&].*)?$
    """
)

RE_DAILYMOTION = re.compile(
    r"""(?ix)^
    (?:https://(?:www\.)?dailymotion\.com/(?:embed/)?video/)
    (?P<id>[a-z0-9]+)(?P<extra>[?&].*)?$
    """
)

RE_VIMEO = re.compile(
    r"""(?ix)^
    (?:https://(?:www\.)?vimeo\.com/|https://player\.vimeo\.com/video/)
    (?P<id>[0-9]+)(?P<extra>[?&].*)?$
    """
)


def youtube(url):
    """Match YouTube source and return a suitable URL."""

    src = None
    m = RE_YOUTUBE.match(url)
    if m:
        key = m.group('id')
        src = 'https://www.youtube.com/embed/{}'.format(key)
    return src


def dailymotion(url):
    """Match Dailymotion source and return a suitable URL."""

    src = None
    m = RE_DAILYMOTION.match(url)
    if m:
        key = m.group('id')
        src = 'https://www.dailymotion.com/embed/video/{}'.format(key)
    return src


def vimeo(url):
    """Match Vimeo source and return a suitable URL."""

    src = None
    m = RE_VIMEO.match(url)
    if m:
        key = m.group('id')
        src = 'https://player.vimeo.com/video/{}'.format(key)
    return src


SERVICES = {
    "youtube": {
        "handler": youtube,
        "defaults": {"allowfullscreen": '', "frameborder": '0'}
    },
    "dailymotion": {
        "handler": dailymotion,
        "defaults": {"allowfullscreen": '', "frameborder": '0'}
    },
    "vimeo": {
        "handler": vimeo,
        "defaults": {"allowfullscreen": '', "frameborder": '0'}
    }
}


class EmbedMediaTreeprocessor(Treeprocessor):
    """
    Find video links and parse them up.

    We'll use the image link syntax to identify our links of interest.
    """

    # Current recognized file extensions
    MIMES = re.compile(r'(?i).*?\.([a-z0-9]+)$')

    # Default MIME types, but can be overridden
    # These are just MIME types we know, but some can be
    # audio or video, and we cannot predict without a type
    # in those cases. So any of these can be overridden if
    # a type is provided, but if none is provided, we take
    # our best guess.
    MIMEMAP = {
        'mp4': 'video/mp4',
        'webm': 'video/webm',
        'mp3': 'audio/mpeg',
        'ogg': 'audio/ogg',
        'wav': 'audio/wav',
        'flac': 'audio/flac'
    }

    def __init__(self, md, video_defaults, audio_defaults, services):
        """Initialize."""

        self.services = copy.deepcopy(SERVICES)
        for k, v in services.items():
            if k not in self.services:
                self.services[k] = copy.deepcopy(v)
            else:
                self.services[k] = {**self.services[k], **copy.deepcopy(v)}
        self.video_defaults = video_defaults
        self.audio_defaults = audio_defaults

        super().__init__(md)

    def process_embedded_media(self, links, parent_map):
        """Process embedded video and audio files."""

        # Evaluate links
        for link in reversed(links):

            # Save the attributes as we will reuse them
            attrib = copy.copy(link.attrib)

            # See if source matches the audio or video mime type
            src = attrib.get('src', '')
            m = self.MIMES.match(src)
            if m is None:
                continue

            # Use whatever audio/video type specified or construct our own
            # Reject any other types
            mime = m.group(1).lower()

            # We don't know what case the attributes are in, so normalize them.
            keys = set([k.lower() for k in attrib.keys()])

            # Identify whether we are working with audio or video and save MIME type
            mtype = ''
            if 'type' in keys:
                v = attrib['type']
                t = v.lower().split('/')[0]
                if t in ('audio', 'video'):
                    mtype = v
                    keys.remove('type')
            else:
                mtype = self.MIMEMAP.get(mime, '')
                attrib['type'] = mtype

            # Doesn't look like audio/video
            if not mtype:
                continue

            # Setup attributess for `<source>` element
            vtype = mtype[:5].lower()
            attrib = {**copy.deepcopy(self.video_defaults if vtype == 'video' else self.audio_defaults), **attrib}
            src_attrib = {'src': src, 'type': mtype}
            del attrib['src']
            del attrib['type']

            # Find any other `<source>` specific attributes and check if there is an `alt`
            alt = ''
            for k in keys:
                key = k.lower()
                if key == 'alt':
                    alt = attrib[k]
                    del attrib[k]
                elif key in ('srcset', 'sizes', 'media'):
                    src_attrib[key] = attrib[k]
                    del attrib[key]

            # Build the source element and apply the right type
            source = etree.Element('source', src_attrib)

            # Find the parent and check if the next sibling is already a media group
            # that we can attach to. If so, the current link will become the primary
            # source, and the existing will become the fallback.
            parent = parent_map[link]
            one_more = False
            sibling = None
            index = -1
            mtype = src_attrib['type'][:5].lower()
            for i, c in enumerate(parent, 0):
                if one_more:
                    # If there is another sibling, see if it is already a video container
                    if c.tag.lower() == mtype and 'fallback' in c.attrib:
                        sibling = c
                    break
                if c is link:
                    # Found where we live, now let's find our sibling
                    index = i
                    one_more = True

            # Attach the media source as the primary source, or construct a new group.
            if sibling is not None:
                # Insert the source at the top
                sibling.insert(0, source)
                # Update container's attributes
                sibling.attrib.clear()
                sibling.attrib.update(attrib)
                # Update fallback link
                last = list(sibling)[-1]
                last.attrib['href'] = src
                last.text = md_util.AtomicString(alt if alt else src)
            else:
                # Create media container and insert source
                media = etree.Element(mtype, attrib)
                media.append(source)
                # Just in case the browser doesn't support `<video>` or `<audio>`
                download = etree.SubElement(media, 'a', {"href": src, "download": ""})
                download.text = md_util.AtomicString(alt if alt else src)
                # Insert media where the old link was
                parent.insert(index, media)

            # Remove the old link
            parent.remove(link)

    def process_embedded_media_service(self, links, parent_map):
        """Process links to embedded media services like YouTube, etc."""

        for link in reversed(links):
            for service in self.services.values():
                src = service['handler'](link.attrib.get('href', ''))
                if src:
                    orig = copy.copy(link.attrib)
                    orig['src'] = src
                    del orig['href']
                    attrib = {**copy.copy(service['defaults']), **orig}
                    el = etree.Element('iframe', attrib)
                    parent = parent_map[link]
                    for index, c in enumerate(list(parent), 0):
                        if c is el:
                            break
                    parent.insert(index, el)
                    parent.remove(link)

    def run(self, root):
        """Shorten popular git repository links."""

        # Grab the elements of interest and form a parent mapping
        images = []
        anchors = []
        parent_map = {c: p for p in root.iter() for c in p}
        for e in root.iter():
            tag = e.tag.lower()
            if tag == 'img':
                images.append(e)
            elif tag == 'a':
                anchors.append(e)

        self.process_embedded_media(images, parent_map)
        self.process_embedded_media_service(anchors, parent_map)

        return root


class EmbedExtension(Extension):
    """Add auto link and link transformation extensions to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            "video_defaults": [
                {'controls': '', 'preload': 'metadata'},
                "Video default attributes - Default: {}"
            ],
            "audio_defaults": [
                {'controls': '', 'preload': 'metadata'},
                "Video default attributes - Default: {}"
            ],
            "services": [{}, "Additional services and service overrides."]
        }
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Add support for turning html links and emails to link tags."""

        config = self.getConfigs()

        media = EmbedMediaTreeprocessor(
            md,
            config['video_defaults'],
            config['audio_defaults'],
            config['services']
        )
        md.treeprocessors.register(media, 'embed', 7.9)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return EmbedExtension(*args, **kwargs)
