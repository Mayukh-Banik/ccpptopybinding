import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser

PY_LANGUAGE = Language(tscpp.language())

parser = Parser(PY_LANGUAGE)

with open("example.hpp", "rb") as source_file:
    tree = parser.parse(source_file.read())

root_node = tree.root_node

print(str(root_node))