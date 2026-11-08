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
            parameters: Tuples of ``(directory, regex, include_dir)``. 
            Directory - Either absolute or relative path.
            Regex - Regex that is ran at Directory.
            IncludeDir - It should be the folder that will be used in the include
            section, ie if path if "Absolute/Path", then include dir should
            be "Path" so in the Cpp binding file, it is "Path/to/file.hpp".

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
        for directory, regex, _ in self.parameters:
            pattern = re.compile(regex)
            base = os.path.abspath(directory)
            for root, _, filenames in os.walk(directory):
                for name in filenames:
                    full_path = os.path.abspath(os.path.join(root, name))
                    normalized = full_path.replace(os.sep, "/")
                    if pattern.search(normalized):
                        rel = os.path.relpath(full_path, base).replace(os.sep, "/")
                        matches[full_path] = rel
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