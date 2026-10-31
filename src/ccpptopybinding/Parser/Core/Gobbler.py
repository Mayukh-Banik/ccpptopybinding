import os
import re


class Gobbler:
    def __init__(self, parameters: list[tuple[str, str]]):
        self.parameters = parameters
        self.files: list[str] = self._gobble()

    def _gobble(self) -> list[str]:
        matches = []
        for directory, regex in self.parameters:
            pattern = re.compile(regex)
            for root, _dirs, filenames in os.walk(directory):
                for name in filenames:
                    full_path = os.path.abspath(os.path.join(root, name))
                    normalized = full_path.replace(os.sep, "/")
                    if pattern.search(normalized):
                        matches.append(full_path)
        return list(dict.fromkeys(matches))


if __name__ == "__main__":
    gobbler = Gobbler([
        ("src", r".*\.py")
    ])

    if gobbler.files:
        print(f"Found {len(gobbler.files)} file(s):")
        for f in gobbler.files:
            print(f"  {f}")
    else:
        print("No matching files found.")