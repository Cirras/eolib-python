from protocol_code_generator.type.custom_type import CustomType
from protocol_code_generator.type.has_underlying_type import HasUnderlyingType


class EnumType(CustomType, HasUnderlyingType):
    def __init__(self, name, source_path, underlying_type, values):
        self._name = name
        self._source_path = source_path
        self._underlying_type = underlying_type
        self._values = values

    @property
    def name(self):
        return self._name

    @property
    def source_path(self):
        return self._source_path

    @property
    def fixed_size(self):
        return self.underlying_type.fixed_size

    @property
    def bounded(self):
        return self.underlying_type.bounded

    @property
    def underlying_type(self):
        return self._underlying_type

    @property
    def values(self):
        return self._values

    def get_enum_value_by_ordinal(self, ordinal_value):
        return next((value for value in self.values if value.ordinal_value == ordinal_value), None)

    def get_enum_value_by_name(self, name):
        return next((value for value in self.values if value.name == name), None)


class EnumValue:
    def __init__(self, ordinal_value, name, python_name):
        self._ordinal_value = ordinal_value
        self._name = name
        self._python_name = python_name

    @property
    def ordinal_value(self):
        return self._ordinal_value

    @property
    def name(self):
        return self._name

    @property
    def python_name(self):
        return self._python_name
