"""Dynamically define some metadata."""
import os
from hatchling.metadata.plugin.interface import MetadataHookInterface


def get_version_dev_status(root):
    """Get version_info without importing the entire module."""

    import importlib.util

    path = os.path.join(root, "pymdownx", "__meta__.py")
    spec = importlib.util.spec_from_file_location("__meta__", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version_info__._get_dev_status()


class CustomMetadataHook(MetadataHookInterface):
    """Our metadata hook."""

    def update(self, metadata):
        """See https://ofek.dev/hatch/latest/plugins/metadata-hook/ for more information."""

        metadata["classifiers"] = [
            f"Development Status :: {get_version_dev_status(self.root)}",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3.13",
            "Programming Language :: Python :: 3.14",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Text Processing :: Filters",
            "Topic :: Text Processing :: Markup :: HTML",
        ]
