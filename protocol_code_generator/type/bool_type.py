from protocol_code_generator.type.basic_type import BasicType
from protocol_code_generator.type.has_underlying_type import HasUnderlyingType


class BoolType(BasicType, HasUnderlyingType):
    def __init__(self, underlying_type):
        self._underlying_type = underlying_type

    @property
    def name(self):
        return "bool"

    @property
    def fixed_size(self):
        return self._underlying_type.fixed_size

    @property
    def bounded(self):
        return True

    @property
    def underlying_type(self):
        return self._underlying_type
