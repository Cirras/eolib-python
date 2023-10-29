from protocol_code_generator.util.number_utils import try_parse_int


class Length:
    def __init__(self, length_string):
        self._string = length_string
        self._integer = try_parse_int(length_string)

    @classmethod
    def from_string(cls, length_string):
        return cls(length_string)

    @classmethod
    def unspecified(cls):
        return cls(None)

    def as_integer(self):
        return self._integer

    @property
    def specified(self):
        return self._string is not None

    def __str__(self):
        return self._string if self.specified else "[unspecified]"
