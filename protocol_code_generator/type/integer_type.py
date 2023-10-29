from protocol_code_generator.type.basic_type import BasicType


class IntegerType(BasicType):
    def __init__(self, name, size):
        self._name = name
        self._size = size

    @property
    def name(self):
        return self._name

    @property
    def fixed_size(self):
        return self._size

    @property
    def bounded(self):
        return True
