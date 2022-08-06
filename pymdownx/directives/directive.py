"""Directive class."""
from abc import ABCMeta, abstractmethod


class Directive(metaclass=ABCMeta):
    """Directive."""

    # Set to something if argument should be split.
    # Arguments will be split and white space stripped.
    ARG_DELIM = ''
    NAME = ''
    ATOMIC = None

    def __init__(self, length, tracker, md):
        """
        Initialize.

        - `store` allows us to store content until all content is found.
        - `length` specifies the length (number of colons) that the header used
        - `tracker` is a persistent storage for the life of the current Markdown page.
          It is a dictionary where we can keep references until the parent extension is reset.
        - `md` is the Markdown object just in case access is needed to something we
          didn't think about.

        """

        self.atomic = self.ATOMIC
        self.length = length
        self.tracker = tracker
        self.md = md
        self.args = []
        self.options = {}

    def is_atomic(self):
        """Check if this is atomic."""

        return self.atomic

    @classmethod
    def on_validate(cls, args):
        """Validate arguments."""

        return True

    def config(self, args, **options):
        """Parse configuration."""

        self.args = []
        if args and self.ARG_DELIM:
            for a in args.split(self.ARG_DELIM):
                a = a.strip()
                if not a:
                    continue
                self.args.append(a)
        elif args:
            self.args = [args]
        self.options = options

    @abstractmethod
    def on_create(self, parent):
        """On create event."""

        return parent

    def on_end(self, el):
        """Perform action on end."""

    def on_add(self, parent):
        """
        Adjust where the content is added.

        Is there a sub-element where this content should go?
        """

        return parent
