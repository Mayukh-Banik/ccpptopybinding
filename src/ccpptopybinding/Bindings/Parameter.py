class Parameter:
    """Describe a single function parameter for a nanobind binding.

    The class captures the parameter type, name, optional default value, and
    nanobind-specific configuration such as ``noconvert`` and ``sig``.
    """

    def __init__(self,
                 type : str,
                 name : str,
                 thereIsADefaultValue : bool = False,
                 defaultValue : str | None = None,
                 noconvert : bool = False,
                 sig : str | None = None):
        """Create a binding parameter definition.

        Args:
            type: The C++ type of the parameter.
            name: The argument name exposed to Python.
            thereIsADefaultValue: Whether the parameter has a default value.
            defaultValue: The default value expression to emit in the binding.
            noconvert: If True, disable implicit conversion for the argument.
            sig: Optional nanobind signature metadata for the argument.
        """
        self.type = type
        self.name = name
        self.thereIsADefaultValue = thereIsADefaultValue
        self.defaultValue = defaultValue
        self.noconvert = noconvert
        self.sig = sig

    def __repr__(self) -> str:
        """Returns all values in Parameter : [Key : Value, ...] format."""
        return f"Parameter : [Name : {self.name}, Type : {self.type}, Default Value : {self.defaultValue}]"

    def __str__(self) -> str:
        """Build the nanobind argument declaration for this parameter.

        Returns:
            A string containing the generated ``nanobind::arg(...)`` expression.
        """
        binding = f'nanobind::arg("{self.name}")'
        if self.noconvert:
            binding += '.noconvert()'
        if self.sig is not None:
            binding += f'.sig({self.sig})'
        if self.thereIsADefaultValue:
            if self.defaultValue is None:
                binding += ' = nanobind::none()'
            else:
                binding += f' = {self.defaultValue}'
        return binding
