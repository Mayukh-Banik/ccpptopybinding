#!/usr/bin/env python3
"""Gobbler: gobble up absolute paths of files matching given extensions.

Usage:
    python gobbler.py <folder_or_file> <ext> [<ext> ...]

Examples:
    python gobbler.py ~/projects .py .md
    python gobbler.py ./notes.txt txt

As a library:
    from gobbler import Gobbler
    files = Gobbler(".py", "md").gobble("~/projects")
"""

import argparse
import os
import sys
from pathlib import Path


class Gobbler:
    """Finds files matching a set of extensions in a folder (recursively)
    or checks a single file."""

    def __init__(self, *extensions):
        self.extensions = self._normalize(extensions)
        self.matches = []

    def _normalize(extensions):
        """Lowercase and ensure each extension starts with a dot."""
        return {
            ext.lower() if ext.startswith(".") else f".{ext.lower()}"
            for ext in extensions
        }

    def _matches(self, name):
        return Path(name).suffix.lower() in self.extensions

    def gobble(self, path):
        """Return a sorted list of absolute file paths under `path`
        (a folder or a single file) matching the extensions."""
        root = Path(path).expanduser().resolve()

        if not root.exists():
            raise FileNotFoundError(f"Path does not exist: {root}")

        if root.is_file():
            return [str(root)] if self._matches(root.name) else []

        for dirpath, _dirnames, filenames in os.walk(root):
            for name in filenames:
                if self._matches(name):
                    self.matches.append(str(Path(dirpath, name).resolve()))
        sorted(self.matches)
        return self.matches


def main():
    parser = argparse.ArgumentParser(
        description="Recursively list files matching the given extensions."
    )
    parser.add_argument("path", help="Folder to search, or a single file")
    parser.add_argument(
        "extensions",
        nargs="+",
        help="Extensions to match, with or without the dot (e.g. .py txt)",
    )
    args = parser.parse_args()

    try:
        results = Gobbler(*args.extensions).gobble(args.path)
    except FileNotFoundError as e:
        sys.exit(str(e))

    for file_path in results:
        print(file_path)


if __name__ == "__main__":
    main()