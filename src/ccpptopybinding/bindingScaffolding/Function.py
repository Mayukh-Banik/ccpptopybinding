from .Parameter import Parameter

class Function:
    """
    A single function binding in nanobind.
    """

    def __init__(self,
                 *,
                 moduleName : str,
                 pythonBindingName : str,
                 fullyQualifiedName : str,
                 parameters : list[Parameter] | None
                 ):
        self.moduleName = moduleName
        self.pythonBindingName = pythonBindingName
        self.fullyQualifiedName = fullyQualifiedName
        self.parameters = parameters

    def __repr__(self):
        return (
            f"Function(moduleName={self.moduleName!r}, "
            f"pythonBindingName={self.pythonBindingName!r}, "
            f"fullyQualifiedName={self.fullyQualifiedName!r}, "
            f"parameters={self.parameters!r})"
        )

    def binding(self) -> str:
        parts = [
            f'"{self.pythonBindingName}"',
            f"&{self.fullyQualifiedName}",
        ]
        if self.parameters:
            parts.extend(p.binding() for p in self.parameters)

        return f"{self.moduleName}.def({', '.join(parts)});"