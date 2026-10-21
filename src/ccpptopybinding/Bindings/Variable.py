class Variable:
    def __init__(self, 
                 type: str, 
                 name: str):
        self.type = type
        self.name = name

    def __repr__(self) -> str:
        """Return in KV format."""
        return f"Type : {self.type}, Name : {self.name}"

    def __str__(self) -> str:
        binding = f'.attr("{self.name}") = &{self.name}'
        return binding