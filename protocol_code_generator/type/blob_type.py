from protocol_code_generator.type.type import Type


class BlobType(Type):
    @property
    def name(self):
        return "blob"

    @property
    def fixed_size(self):
        return None

    @property
    def bounded(self):
        return False
