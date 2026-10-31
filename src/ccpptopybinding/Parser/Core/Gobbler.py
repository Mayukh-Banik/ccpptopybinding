import os
import re


class Gobbler:
    """
    Collect files matching configured patterns for later parsing.

    Each parameter is a tuple of a directory to traverse, a regular
    expression to match against normalized absolute file paths, and an
    optional include-directory prefix for the corresponding relative path.
    Duplicate absolute file paths are included only once.
    """
    def __init__(self, 
                 parameters: list[tuple[str, str, str]]):
        """Initialize the gobbler and immediately collect matching files.

        Args:
            parameters: Tuples of ``(directory, regex, include_dir)``. The
                directory is traversed recursively, ``regex`` is searched
                against each normalized absolute file path, and ``include_dir``
                is prepended to the path relative to the directory when set.

        Attributes:
            parameters: The collection configuration supplied by the caller.
            files: ``(absolute_path, include_relative_path)`` pairs for the
                unique matching files.
        """
        self.parameters = parameters
        self.files: list[tuple[str, str]] = self._gobble()

    def _gobble(self) -> list[tuple[str, str]]:
        """Walk configured directories and return unique matching files.

        Returns:
            A list of ``(absolute_path, include_relative_path)`` pairs. The
            include-relative path is relative to the configured directory,
            optionally prefixed by its ``include_dir`` value.
        """
        matches: dict[str, str] = {}  # keyed by full path to drop duplicates
        for directory, regex, include_dir in self.parameters:
            pattern = re.compile(regex)
            base = os.path.abspath(directory)
            for root, _dirs, filenames in os.walk(directory):
                for name in filenames:
                    full_path = os.path.abspath(os.path.join(root, name))
                    normalized = full_path.replace(os.sep, "/")
                    if pattern.search(normalized):
                        rel = os.path.relpath(full_path, base).replace(os.sep, "/")
                        rel_path = f"{include_dir}/{rel}" if include_dir else rel
                        matches[full_path] = rel_path
        return list(matches.items())


if __name__ == "__main__":
    gobbler = Gobbler([
        ("src", r".*\.py$", "src")
    ])

    if gobbler.files:
        print(f"Found {len(gobbler.files)} file(s):")
        for full, rel in gobbler.files:
            print(f"  {rel}  ->  {full}")
    else:
        print("No matching files found.")