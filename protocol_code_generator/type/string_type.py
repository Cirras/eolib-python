from protocol_code_generator.type.basic_type import BasicType


class StringType(BasicType):
    def __init__(self, name, length):
        self._name = name
        self._length = length

    @property
    def name(self):
        return self._name

    @property
    def fixed_size(self):
        return self._length.as_integer()

    @property
    def bounded(self):
        return self._length.specified
