from protocol_code_generator.type.custom_type import CustomType


class StructType(CustomType):
    def __init__(self, name, fixed_size, bounded, source_path):
        self._name = name
        self._fixed_size = fixed_size
        self._bounded = bounded
        self._source_path = source_path

    @property
    def name(self):
        return self._name

    @property
    def fixed_size(self):
        return self._fixed_size

    @property
    def bounded(self):
        return self._bounded

    @property
    def source_path(self):
        return self._source_path
