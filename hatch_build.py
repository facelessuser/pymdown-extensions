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


def get_requirements(root):
    """Load list of dependencies."""

    install_requires = []
    with open(os.path.join(root, "requirements", "project.txt")) as f:
        for line in f:
            if not line.startswith("#"):
                install_requires.append(line.strip())
    return install_requires


class CustomMetadataHook(MetadataHookInterface):
    """Our metadata hook."""

    def update(self, metadata):
        """See https://ofek.dev/hatch/latest/plugins/metadata-hook/ for more information."""

        metadata["dependencies"] = get_requirements(self.root)
        metadata["classifiers"] = [
            f"Development Status :: {get_version_dev_status(self.root)}",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Text Processing :: Filters",
            "Topic :: Text Processing :: Markup :: HTML",
        ]
