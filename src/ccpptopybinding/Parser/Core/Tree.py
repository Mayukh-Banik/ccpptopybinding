from enum import Enum, auto

class NodeType(Enum):
    Incomplete = auto()
    File = auto()
    Namespace = auto()


class Node:
    def __init__(
            self,
            type : NodeType,
            parent : Node | None,
            children : list[Node] | None):
        self.type = type
        self.parent = parent
        self.children = children

class File:
    def __init__(
            self,
            absoluteFileLocation : str,
            relativeFileLocation : str,
    ):
        self.absoluteFileLocation = absoluteFileLocation
        self.relativeFileLocation = relativeFileLocation

        
class Tree:
    def __init__(
            self,
            rootNode : Node):
        self.rootNode = rootNode