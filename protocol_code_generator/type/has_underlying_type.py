from abc import abstractproperty
from protocol_code_generator.type.type import Type


class HasUnderlyingType(Type):
    @abstractproperty
    def underlying_type(self):
        pass
