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
        pass
        