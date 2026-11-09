import clang.cindex as ci
from clang.cindex import CursorKind as K
from pathlib import Path


FILES = []

for x in FILES:
    pass

def in_main_file(node: ci.Cursor, tu: ci.TranslationUnit) -> bool:
    f = node.location.file
    return f is not None and f.name == tu.spelling


def walk(node: ci.Cursor):
    yield node
    for child in node.get_children():
        yield from walk(child)


def traverse(tu: ci.TranslationUnit):
    tu.PARSE_INCOMPLETE
    # Only descend into top-level nodes that come from our file,
    # so nothing inside <vector>, <string>, etc. is ever visited.
    for child in tu.cursor.get_children():
        if in_main_file(child, tu):
            yield from walk(child)


def main():
    index = ci.Index.create()
    tu = index.parse(str("example.hpp"), args=["-std=c++20"], options=ci.TranslationUnit.PARSE_INCOMPLETE)

    for node in traverse(tu):
        if node.kind in (K.FUNCTION_DECL, K.CXX_METHOD, K.CONSTRUCTOR):
            params = ", ".join(f"{a.type.spelling} {a.spelling}" for a in node.get_arguments())
            print(f"{node.kind.name}: {node.result_type.spelling} {node.spelling}({params})")
        elif node.kind in (K.VAR_DECL, K.FIELD_DECL, K.PARM_DECL):
            print(f"{node.kind.name}: {node.type.spelling} {node.spelling}")
        else:
            print(f"{node.kind.name}: {node.spelling}")

if __name__ == "__main__":
    main()


class File:
    def __init__(self,
                 *,
                 file,
                 index : ci.Index):
        pass