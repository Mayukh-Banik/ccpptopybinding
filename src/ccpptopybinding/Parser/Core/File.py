from pathlib import Path
import clang.cindex as ci
from clang.cindex import CursorKind as K

class File:
    def __init__(self, filePath: Path):
        self.filePath = Path(filePath).resolve()
        self.index = ci.Index.create()
        self.translationUnit = self.index.parse(str(self.filePath))

    def _isFromThisFile(self, cursor):
        f = cursor.location.file          # None for builtins / the TU cursor itself
        return f is not None and f.name == str(self.filePath)

    def loadAST(self):
        def visit(cursor, depth=0):
            for child in cursor.get_children():
                if not self._isFromThisFile(child):
                    continue              # prune: skip this node and everything under it
                print("  " * depth + f"{child.kind.name} {child.spelling}")
                visit(child, depth + 1)

        visit(self.translationUnit.cursor)