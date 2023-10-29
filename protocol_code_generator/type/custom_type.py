from abc import abstractproperty
from protocol_code_generator.type.type import Type


class CustomType(Type):
    @abstractproperty
    def source_path(self):
        pass
